"""Saque do Vale: percursos completos do Vale do Turvo jogados por um robô, medindo o que entra e o que sai.

Mede, por percurso, os baús (quantos, de onde, fixos ou sorteados), os consumíveis (ganhos por origem, usados e
acumulados), os equipamentos (achados, que a classe usa, que melhoram o que se veste), a mochila (vendas, o que ficou
para trás) e o ouro. Não muda o jogo: só o joga e conta.

    python -m tests.saque_vale                     # 3 classes × 2 desfechos × 2 roteiros × 15 sementes
    python -m tests.saque_vale --sementes 30
    python -m tests.saque_vale --detalhe           # também a lista de percursos, um por linha
    python -m tests.saque_vale --estrategia cuidadoso   # o começo com outra estratégia (ESTRATEGIAS, abaixo)
    python -m tests.saque_vale --roteiros nivel6   # quem explora mais e só desce ao fundo no nível 6
    python -m tests.saque_vale --economia          # só a conta de uma luta do começo (Charco e Bosque)

O percurso (o que o robô faz, nesta ordem de prioridade):
- Vila: abre os baús da bolsa; aceita do mural até 2 contratos de caça em lugares do nível do herói (o pagamento
  vem sozinho ao chegar na vila); compra comida até 5 dias; compra no mercado a peça que melhora o que se veste
  (espaço vazio primeiro); veste o que melhora e vende o resto da mochila; compra até a lista do roteiro (tochas 4,
  poções de vida 2, bandagens 2, antídoto 1 e a aljava cheia), se sobrar o preço da taverna;
  faz a ação de missão que houver; dorme na taverna com a vida abaixo de 75% ou à noite; senão, segue viagem.
- Fora da vila: caça o contrato que for dali; com a comida no fim (1 dia ou menos) e ouro para comprar, volta ao Vau; acampa à noite ou com a
  vida abaixo de 85% (sem comida nem ouro, explora em vez de acampar); faz a ação de missão que houver; explora N vezes por
  visita ("direto": 1; "explorador": 3, e passa uma vez pelo Charco dos Juncos), só onde o nível do lugar não passa
  do herói; segue para o objetivo pelo caminho mais curto.
- Nível: as salas da capela pedem nível 3 e o fundo, 4. Antes disso, o robô explora o lugar mais alto que o herói
  aguenta (Charco 1, Bosque 2, Capela 3), ou onde há contrato aberto, até chegar lá.
- Desfecho: "descansada" (fala com Vó Berta, solta as correntes, faz o rito, recebe a herança) ou "destruida"
  (não solta as correntes e luta até o fim). Caspar: a postura da praça é sorteada.
- Luta: o robô lutador da arena (tests/arena.py), que também usa antídoto com veneno, bandagem com sangramento e
  tônico com o recurso abaixo de 25%, e foge (com a bomba de fumaça, se tiver) abaixo de 35% da vida sem poção. Fora da luta: bandagem em ferida aberta, unguento em infecção.
- Equipamento achado: veste se melhora (soma dos bônus com os pesos do preço, PESO_PRECO, sem o atributo de ataque
  que a classe não usa); senão guarda para vender; com a mochila cheia, deixa para trás.
- Recrutamento: aceita quem se oferece, se houver lugar. Eventos, conversas e especialização: ao acaso, como o
  robô de sempre.
O fim: a Febre concluída (com a herança, no rito), a Vigília decidida, ou o dia 45.
"""

import argparse
import random
import statistics
import tempfile

from rpg import caspar, missoes
from rpg import comitiva
from rpg import dev
from rpg.itens import CONSUMIVEIS, PESO_PRECO, espacos
from rpg.jogo import Jogo
from rpg.regras import Derrota, FimDeJogo, LIMITE_MOCHILA
from rpg import sobrevivencia
from rpg.ui import LimiteBot

from tests.arena import LutadorUI

CLASSES = ("guerreiro", "arqueiro", "mago")
DESFECHOS = ("descansada", "destruida")
ROTEIROS = ("direto", "explorador")
EXPLORAR = {"direto": 1, "explorador": 3, "nivel6": 3}
# "nivel6": quem explora mais e só desce ao fundo no nível 6 (com Muralha disponível; não é o padrão da régua)
COMPRAS = {"provisoes": 5, "tocha": 4, "pocao_vida": 2, "bandagem": 2, "antidoto": 1}
FEBRE, VIGILIA = "febre_do_turvo", "vigilia_de_caspar"
DIA_LIMITE = 45
# Estratégias para o começo (E9): o que um jogador informado faria, sem recurso de graça nem saber o que vem.
#   comida_pelo_grupo  leva 3 dias de comida para cada boca (o herói e cada companheiro comem 1 por dia)
#   poupar             antes do nível 3, só compra equipamento para espaço vazio, guardando comida do grupo
#   recrutar_a_partir  aceita companheiro só a partir deste nível (1: sempre, como o roteiro original)
#   contratos          "todos" (bando e alvo nomeado), "bando" (só caça de bando) ou "depois_do_3" (nenhum antes do 3)
_E = dict(comida_pelo_grupo=False, poupar=False, recrutar_a_partir=1, contratos="todos")
ESTRATEGIAS = {
    "atual": _E,
    "comida_do_grupo": dict(_E, comida_pelo_grupo=True),
    "poupar": dict(_E, comida_pelo_grupo=True, poupar=True),
    "so_depois_do_3": dict(_E, comida_pelo_grupo=True, recrutar_a_partir=3),
    "cuidadoso": dict(_E, comida_pelo_grupo=True, poupar=True, recrutar_a_partir=3),
    "so_bando": dict(_E, comida_pelo_grupo=True, contratos="bando"),
    "contrato_depois_do_3": dict(_E, comida_pelo_grupo=True, contratos="depois_do_3"),
}
NIVEL_CAPELA, NIVEL_FUNDO = 3, 4
VIDA_PARA_SAIR = 0.85  # abaixo disto, o roteiro descansa antes de explorar ou lutar
NADA = object()


def nota(it, classe):
    """A força de uma peça para quem a veste: os bônus com os pesos do preço, sem o ataque que a classe não usa."""
    fora = "atk" if classe == "mago" else "poder"
    return sum(PESO_PRECO.get(k, 1.0) * v for k, v in it["bonus"].items() if k != fora)


class PercursoUI(LutadorUI):
    """O lutador da arena, mais uma escolha imposta pelo roteiro (`forcar`) e os itens de luta que ele não usava."""

    def __init__(self, rng):
        super().__init__(rng)
        self.forcar = None
        self.pausas = 0  # cada Continuar ou pausa de leitura
        self.escolhas = {"luta": 0, "fora": 0}

    def pausar(self):
        self.pausas += 1

    def continuar(self, confirmar=False):
        self.pausas += 1

    def escolher(self, pergunta, opcoes):
        self.escolhas["luta" if self.g and self.g.combate_ativo else "fora"] += 1
        if self.forcar is not None:
            i, self.forcar = self.forcar, None
            return i
        return super().escolher(pergunta, opcoes)

    def _acao(self, cb, metas):
        j = cb.j
        itens = next((m["itens"] for m in metas if m.get("acao") == "itens"), [])
        pode = {m.get("usar_item") for m in itens if not m.get("motivo")}
        fugir = next((i for i, m in enumerate(metas) if m.get("acao") == "fugir"), None)
        if j.hp < 0.35 * j.max_hp and "pocao_vida" not in pode:
            if "bomba_fumaca" in pode and fugir is not None:
                self._plano, self._alvo = "bomba_fumaca", None
                return 2
            if fugir is not None:
                return fugir  # sem poção e quase caindo: foge, como uma pessoa fugiria
        for k, quando in (("antidoto", j.efeito("veneno") and j.hp < 0.7 * j.max_hp),
                          ("bandagem", j.efeito("sangramento")),
                          ("tonico", j.rec < 0.25 * j.max_rec)):
            if quando and k in pode:
                self._plano, self._alvo = k, None
                return 2
        return super()._acao(cb, metas)


class Percurso:
    def __init__(self, classe, desfecho, roteiro, semente, estrategia="atual"):
        self.classe, self.desfecho, self.roteiro, self.semente = classe, desfecho, roteiro, semente
        self.estrategia = ESTRATEGIAS[estrategia]
        self.nome_estrategia = estrategia
        self.nivel_fundo = 6 if roteiro == "nivel6" else NIVEL_FUNDO
        self.rotina = self.itens_decididos = 0
        self.trajeto = []  # (dia, período, lugar, ouro, comida, fome, vida/máx, nível, comitiva, ação)
        self.rng = random.Random(f"roteiro:{semente}")
        self.ui = PercursoUI(random.Random(semente))
        g = self.g = Jogo(self.ui, seed=semente, pasta_saves=tempfile.mkdtemp(prefix="saque_"), hardcore=False)
        self.ui.g = g
        g.iniciar("Robô", classe, "turvo")
        self.inicial = dict(g.j.consumiveis)
        self.ctx = ["inicio"]
        self.ganhos = []        # (item, qtd, origem)
        self.do_bau = []        # (suprimento, quanto já havia na bolsa) de cada suprimento que saiu de baú
        self.recursos = []      # (comida|flechas, qtd, origem)
        self.baus = []          # (origem, fixo)
        self.ofertas = []       # dicts por equipamento oferecido
        self.origem_item = {}
        self.item_atual = None
        self.derrotados = []
        self.visita = None
        self.exploradas = 0
        self.charco = roteiro != "explorador"
        self.mochila_max = 0
        self.deixados = 0
        self.vendas = []
        self.compras = []
        self.equip_comprado = []
        self.contratos = 0
        self.postura = None
        self._embrulhar()

    # ------------------------------------------------------------ contar
    def origem(self):
        return "/".join(self.ctx)

    def _embrulhar(self):
        g = self
        jogo = self.g
        menu, dar, dar_prov, dar_fl = jogo.menu, jogo.dar, jogo.dar_provisoes, jogo.dar_flechas
        sortear_bau, saque, oferecer = jogo.sortear_bau, jogo.saque_de_combate, jogo.oferecer_equip

        def com(ctx, fn):
            def f(*a, **k):
                g.ctx.append(ctx)
                try:
                    return fn(*a, **k)
                finally:
                    g.ctx.pop()
            return f

        def _dar(item, qtd=1):
            if item == "bau":
                if g.ctx[-1] == "luta":
                    tipo = ("guardiã" if any(e.chefe for e in g.derrotados) else
                            "inimigo com nome" if any(e.unico for e in g.derrotados) else "sorteado")
                else:
                    tipo = "sacristia" if g.ctx[0] in ("missao:sacristia", "missao:bau") else "outro"  # recolhido (1.85.0)
                g.baus.append((g.origem(), tipo))
            g.ganhos.append((item, qtd, g.origem()))
            if "bau" in g.ctx and item != "bau":
                g.do_bau.append((item, jogo.j.consumiveis.get(item, 0)))  # quanto já carregava ao receber
            return dar(item, qtd)

        def _prov(n):
            antes = jogo.j.provisoes
            r = dar_prov(n)
            g.recursos.append(("comida", jogo.j.provisoes - antes, g.origem()))
            return r

        def _fl(n):
            r = dar_fl(n)
            g.recursos.append(("flechas", r or 0, g.origem()))
            return r

        def _saque(derrotados):
            g.derrotados = derrotados
            return com("luta", saque)(derrotados)

        def _oferecer(item):
            g.origem_item.setdefault(id(item), g.origem())
            if jogo.espolio_aberto is not None:
                return oferecer(item)
            g.item_atual = item
            return oferecer(item)

        def _menu(pergunta, opcoes):
            validas = [o for o in opcoes if o]
            chave = g.decidir(pergunta, validas)
            if chave is not NADA:
                i = next((i for i, o in enumerate(validas) if o[1] == chave), None)
                if i is not None:
                    g.ui.forcar = i
            return menu(pergunta, opcoes)

        jogo.menu, jogo.dar, jogo.dar_provisoes, jogo.dar_flechas = _menu, _dar, _prov, _fl
        jogo.sortear_bau = com("bau", sortear_bau)
        jogo.saque_de_combate = _saque
        jogo.oferecer_equip = _oferecer

    # ------------------------------------------------------------ onde ir
    def febre(self):
        return missoes.registro(self.g, FEBRE)

    def vigilia(self):
        return caspar.registro(self.g)

    def nivel_de(self, chave):
        return next(l["nivel"] for l in self.g.mundo["locais"] if l.get("chave") == chave)

    def treino(self):
        """Onde explorar para subir de nível: o lugar de um contrato aberto, ou o mais alto do Vale que não passa do
        nível do herói."""
        locais = self.g.mundo["locais"]
        for c in self.g.contratos:
            if c["tipo"] in ("caca", "alvo") and not c.get("concluido") and locais[c["local"]]["nivel"] <= self.g.j.nivel:
                return locais[c["local"]]["chave"]
        fora = [l for l in locais if l["tipo"] == "selvagem" and l["nivel"] <= self.g.j.nivel]
        return max(fora, key=lambda l: l["nivel"])["chave"] if fora else "charco_dos_juncos"

    def destino(self):
        f, v = self.febre(), self.vigilia()
        if self.comida_curta() and self.g.j.ouro >= self.g.preco_suprimento("provisoes"):
            return "vau_do_turvo"  # a comida acabando: volta para comprar
        if not self.charco and "abertura" in f["cenas"]:
            return "charco_dos_juncos"
        if f["concluida"]:
            return "vau_do_turvo"
        if (self.desfecho == "descansada" and f["etapa"] in ("ossuario", "fundo") and "ilse" in f["pistas"]
                and "fita" not in f["preparos"]):
            return "vau_do_turvo"
        if v and v["etapa"] == "praca" and not v.get("desfecho") and f["etapa"] == "retorno":
            return "vau_do_turvo"
        lugar = missoes.MISSOES[FEBRE]["etapas"][f["etapa"]]["lugar"]
        precisa = {"capela": NIVEL_CAPELA, "sacristia": NIVEL_CAPELA, "ossuario": NIVEL_CAPELA,
                   "fundo": self.nivel_fundo}.get(f["etapa"], 0)
        if self.g.j.nivel < precisa and self.nivel_de(lugar) > self.g.j.nivel:
            return self.treino()  # a missão espera nível: sobe onde o herói aguenta
        return lugar

    def proximo(self, chave):
        """O vizinho no caminho mais curto até o lugar (o Vale é pequeno: busca em largura)."""
        locais = self.g.mundo["locais"]
        alvo = next(l["id"] for l in locais if l.get("chave") == chave)
        de = self.g.loc["id"]
        anterior, fila = {de: None}, [de]
        while fila:
            a = fila.pop(0)
            for b in locais[a]["con"]:
                b = int(b)
                if b not in anterior and not locais[b].get("fechado"):
                    anterior[b] = a
                    fila.append(b)
        passo = alvo
        while anterior.get(passo) not in (de, None):
            passo = anterior[passo]
        return passo

    # ------------------------------------------------------------ decidir
    def decidir(self, pergunta, validas):
        chaves = [o[1] for o in validas]
        if "explorar" in chaves or pergunta.startswith("Você está em") or pergunta == "Para onde?":
            self.rotina += 1
        elif pergunta == "O que fazer com o item?":
            self.itens_decididos += 1
        if "explorar" in chaves:
            return self.anotar(self.fora(chaves))
        if pergunta.startswith("Você está em"):
            return self.anotar(self.na_vila(chaves))
        if pergunta == "Para onde?":
            alvo = self.proximo(self.destino())
            return next((k for k in chaves if k and k[0]["id"] == alvo), None)
        if pergunta == "O que fazer com o item?":
            return self.achado(chaves)
        if "destruir" in chaves:
            return "descanso" if self.desfecho == "descansada" and "descanso" in chaves else (
                "destruir" if self.desfecho == "destruida" else None)
        if pergunta == "Este é o momento do rito.":
            return "rito" if self.desfecho == "descansada" else "lutar"
        if pergunta == "O que você faz com as correntes?":
            return "classe" if "classe" in chaves else "mao"
        if pergunta.startswith("Levar ") and "sim" in chaves:
            if self.g.j.nivel < self.estrategia["recrutar_a_partir"]:
                return "nao"
            return "sim"  # quem se oferece para vir, vem (com lugar na comitiva)
        if pergunta == "O que você diz diante da vila?":
            self.postura = self.rng.choice([k for k in chaves if k])
            return self.postura
        if any(m and m.get("dormir") for m in (o[2] if len(o) > 2 else None for o in validas)):
            self.abrir_baus()  # na fogueira: os baús, e dormir
            self.ctx[:] = ["descanso"]
            return None
        return NADA

    def anotar(self, acao):
        g, j = self.g, self.g.j
        nome = acao if isinstance(acao, str) else acao[2] if isinstance(acao, tuple) and len(acao) > 2 else str(acao)
        self.trajeto.append((g.dia, g.periodo, g.loc.get("chave"), j.ouro, j.provisoes, j.fome,
                             round(j.hp / j.max_hp, 2), j.nivel, len(comitiva.membros(g)), nome))
        return acao

    def comida_alvo(self):
        """Quantos dias de comida o roteiro leva: 5, ou (comida pelo grupo) 3 dias para cada boca, até 12."""
        if not self.estrategia["comida_pelo_grupo"]:
            return COMPRAS["provisoes"]
        return min(12, 3 * (1 + len(comitiva.membros(self.g))))

    def comida_curta(self):
        bocas = 1 + len(comitiva.membros(self.g)) if self.estrategia["comida_pelo_grupo"] else 1
        return self.g.j.provisoes <= bocas

    def nova_visita(self):
        if self.visita != self.g.loc["id"]:
            self.visita, self.exploradas = self.g.loc["id"], 0

    def missao_aqui(self, chaves):
        f = self.febre()
        for k in chaves:
            if not (isinstance(k, tuple) and k[0] == "missao"):
                continue
            aid = k[2]
            if aid == "correntes" and self.desfecho == "destruida":
                continue
            if aid in ("nave", "sacristia", "ossuario", "correntes") and self.g.j.nivel < NIVEL_CAPELA:
                continue
            if aid == "fundo":
                if self.desfecho == "descansada" and not missoes.descanso_pronto(f):
                    continue
                if self.g.j.nivel < self.nivel_fundo:
                    continue
            return k
        return None

    def fora(self, chaves):
        g, j = self.g, self.g.j
        self.nova_visita()
        self.manter()
        aqui = g.loc.get("chave")
        if self.destino() == "vau_do_turvo" and self.comida_curta() and j.hp >= 0.3 * j.max_hp:
            return self._ctx("viajar", "viagem")
        sem_nada = j.provisoes == 0 and j.ouro < g.preco_suprimento("provisoes")
        if sem_nada and g.loc["nivel"] <= j.nivel and j.hp >= 0.3 * j.max_hp and g.periodo < 3:
            return self._ctx("explorar")  # sem comida nem ouro, acampar só dá fome: vai atrás do que achar
        if g.periodo >= 3 or j.hp < VIDA_PARA_SAIR * j.max_hp:
            return "acampar"
        m = self.missao_aqui(chaves)
        if m:
            self.ctx[:] = ["missao:" + m[2]]
            return m
        cacar = next((k for k in chaves if isinstance(k, str) and k.startswith("cacar:")), None)
        if cacar:
            return self._ctx(cacar, "contrato")
        aguenta = g.loc["nivel"] <= j.nivel
        if aqui == "charco_dos_juncos" and not self.charco and self.exploradas >= EXPLORAR[self.roteiro]:
            self.charco = True
        if aguenta and (self.exploradas < EXPLORAR[self.roteiro] or aqui == self.destino()):
            self.exploradas += 1  # de passagem, N vezes; onde o objetivo espera nível, até chegar lá
            return self._ctx("explorar")
        return self._ctx("viajar", "viagem")

    def _ctx(self, chave, nome=None):
        self.ctx[:] = [nome or chave]
        return chave

    def na_vila(self, chaves):
        g, j = self.g, self.g.j
        self.nova_visita()
        self.manter()
        self.abrir_baus()
        self.aceitar_contratos()
        self.comprar_comida()
        self.comprar_equip()
        self.vender()
        self.comprar()
        m = self.missao_aqui(chaves)
        if m:
            self.ctx[:] = ["missao:" + m[2]]
            return m
        preco = g.preco(8 + 2 * j.nivel)
        if (j.hp < 0.75 * j.max_hp or g.periodo >= 3 or self.esperar()) and j.ouro >= preco:
            return self._ctx("dormir", "descanso")
        if self.esperar():
            return self._ctx("passear", "vila")
        return self._ctx("viajar", "viagem")

    def esperar(self):
        """Na vila, o que falta é só esperar (a Vigília aguarda a febre): o destino é aqui mesmo."""
        return self.destino() == "vau_do_turvo" and self.fim() is None

    # ------------------------------------------------------------ cuidar da bolsa e da mochila
    def manter(self):
        g, j = self.g, self.g.j
        dev.gastar_talentos(g, self.rng)
        if sobrevivencia.tem(j, "infeccao") and j.tem("unguento"):
            self._usar("unguento")
        if j.tem("bandagem") and any(sobrevivencia.FERIMENTOS[f["id"]].get("aberto") and not f["tratado"]
                                     for f in j.ferimentos):
            self._usar("bandagem")
        if j.efeito("veneno") and j.tem("antidoto"):
            self._usar("antidoto")
        self.mochila_max = max(self.mochila_max, len(j.mochila))

    def _usar(self, k):
        self.ctx.append("cuidado")
        try:
            self.g.usar_consumivel(k)
        finally:
            self.ctx.pop()

    def abrir_baus(self):
        if self.g.j.tem("bau") and self.g.lugar_seguro():
            self.ctx[:] = ["abrir_baus"]
            self.g.usar_consumivel("bau")

    def vender(self):
        g = self.g
        g.recompra = []
        for it in list(g.j.mochila):
            if g.pode_usar(it) and self.melhora(it):
                g.equipar(it)
                continue
            self.vendas.append((it.get("raridade", "comum"), it["preco"] // 2, self.origem_item.get(id(it), "?")))
            g.vender_item(it)

    def aceitar_contratos(self):
        """Do mural, até 2 contratos de caça (bando ou alvo) em lugares que o herói aguenta. O mural renova a cada 3 dias,
        como na tela; aceitar é a mesma regra da tela (aceitar_contrato)."""
        g = self.g
        vid = str(g.loc["id"])
        oferta = g.ofertas.get(vid)
        if not oferta or g.dia - oferta["dia"] >= 3:
            oferta = {"dia": g.dia, "lista": [g.gerar_contrato() for _ in range(3)]}
            g.ofertas[vid] = oferta
        locais = g.mundo["locais"]
        politica = self.estrategia["contratos"]
        if politica == "depois_do_3" and g.j.nivel < 3:
            return
        tipos = ("caca",) if politica == "bando" and g.j.nivel < 3 else ("caca", "alvo")
        for c in list(oferta["lista"]):
            if len(g.contratos) >= 2:
                break
            if c["tipo"] in tipos and locais[c["local"]]["nivel"] <= g.j.nivel:
                g.aceitar_contrato(c, oferta)
                self.contratos += 1

    def comprar_comida(self):
        g, j = self.g, self.g.j
        self.ctx[:] = ["compra"]
        falta = min(self.comida_alvo() - j.provisoes, j.ouro // g.preco_suprimento("provisoes"))
        if falta > 0 and g.comprar_suprimento("provisoes", falta):
            self.compras.append(("provisoes", falta))

    def comprar_equip(self):
        """Uma peça do mercado que melhora o que se veste (espaço vazio primeiro), se sobrar o preço da cama."""
        g, j = self.g, self.g.j
        reserva = g.preco(8 + 2 * j.nivel)
        if self.estrategia["poupar"]:  # antes do nível 3, só espaço vazio, e guardando também 3 dias de comida do grupo
            reserva += 3 * (1 + len(comitiva.membros(g))) * g.preco_suprimento("provisoes")
        a_venda = g.estoque()
        boas = [it for it in a_venda if g.pode_usar(it) and self.melhora(it)]
        boas.sort(key=lambda it: (bool(j.equip.get(g.espaco_para(it))), -nota(it, j.classe)))
        for it in boas:
            if self.estrategia["poupar"] and j.nivel < 3 and j.equip.get(g.espaco_para(it)):
                continue
            if j.ouro - g.preco(it["preco"]) >= reserva and len(j.mochila) < LIMITE_MOCHILA and self.melhora(it):
                if g.comprar_equipamento(it, a_venda):
                    self.equip_comprado.append((it.get("raridade", "comum"), g.preco(it["preco"])))
                    if it in j.mochila:
                        g.equipar(it)

    def comprar(self):
        g, j = self.g, self.g.j
        reserva = g.preco(8 + 2 * j.nivel)
        self.ctx[:] = ["compra"]
        tem = {"provisoes": j.provisoes, **{k: j.consumiveis.get(k, 0) for k in COMPRAS if k != "provisoes"}}
        for k, alvo in COMPRAS.items():
            falta = alvo - tem[k]
            # a comida vem antes de tudo, até da taverna; o resto, só se sobrar o preço da cama
            falta = min(falta, (j.ouro - (0 if k == "provisoes" else reserva)) // g.preco_suprimento(k))
            if falta > 0:
                if g.comprar_suprimento(k, falta):
                    self.compras.append((k, falta))
        if j.classe == "arqueiro":
            falta = g.max_flechas() - j.flechas
            caber = (j.ouro - reserva) // max(1, g.preco_suprimento("flechas"))
            if min(falta, caber) > 0:
                g.comprar_suprimento("flechas", min(falta, caber))

    def melhora(self, it):
        j = self.g.j
        atuais = [j.equip.get(s) for s in espacos(it["slot"])]
        pior = min((nota(a, j.classe) if a else 0) for a in atuais)
        return nota(it, j.classe) > pior + 0.01

    def achado(self, chaves):
        it, j = self.item_atual, self.g.j
        usa = self.g.pode_usar(it)
        melhora = usa and self.melhora(it)
        self.ofertas.append({"raridade": it.get("raridade", "comum"), "usa": usa, "melhora": melhora,
                             "origem": self.origem_item.get(id(it), self.origem()), "unico": it.get("unico"),
                             "nivel": it.get("nivel"), "nv_heroi": j.nivel})
        if melhora and "equipar" in chaves:
            return "equipar"
        if "guardar" in chaves:
            return "guardar"
        self.deixados += 1
        return "deixar"

    # ------------------------------------------------------------ jogar
    def fim(self):
        f, v = self.febre(), self.vigilia()
        heranca = f["desfecho"] != "descansada" or "heranca" in f["cenas"]
        if f["concluida"] and heranca and v and v.get("desfecho"):
            return "completo"
        if self.g.dia > DIA_LIMITE:
            return "limite"
        return None

    def jogar(self):
        g = self.g
        motivo = None
        while motivo is None:
            try:
                try:
                    g.tela()
                except Derrota as d:
                    g.resgate(d.causa)
            except (FimDeJogo, LimiteBot):
                motivo = "parou"
                break
            motivo = self.fim()
        self.mochila_max = max(self.mochila_max, len(g.j.mochila))
        return self.medir(motivo)

    def medir(self, motivo):
        g, j = self.g, self.g.j
        ev = g.registro
        usados = {}
        for e in ev:
            if e.get("t") == "consumivel":
                chave = (e["item"], "luta" if e.get("em_combate") else "fora")
                usados[chave] = usados.get(chave, 0) + 1
        f = self.febre()
        return {
            "classe": self.classe, "desfecho": self.desfecho, "roteiro": self.roteiro, "semente": self.semente,
            "fim": motivo, "desfecho_real": f["desfecho"], "dia": g.dia, "nivel": j.nivel,
            "estrategia": self.nome_estrategia, "trajeto": self.trajeto,
            "pausas": self.ui.pausas, "escolhas_luta": self.ui.escolhas["luta"],
            "escolhas_fora": self.ui.escolhas["fora"], "rotina": self.rotina, "itens_decididos": self.itens_decididos,
            "encontros": [tuple(sorted(i["familia"] for i in e["inimigos"])) for e in ev if e.get("t") == "combate"],
            "eventos": [e["id"] for e in ev if e.get("t") == "evento"],
            "talentos": dict(j.talentos), "secundaria": (j.equip.get("secundaria") or {}).get("unico"),
            "causa": g.estatisticas.get("causa"), "etapa": f["etapa"],
            "vigilia": (self.vigilia() or {}).get("etapa"), "postura_fim": (self.vigilia() or {}).get("desfecho"),
            "heranca": "heranca" in f["cenas"], "concluida": f["concluida"], "lugar": g.loc.get("chave"),
            "lutas": sum(1 for e in ev if e.get("t") == "combate"), "quedas": g.estatisticas.get("quedas", 0),
            "resgates": [e["causa"] for e in ev if e.get("t") == "resgate"],  # a causa de cada queda (campanha)
            "dias_com_fome": sum(1 for e in ev if e.get("t") == "dia" and e.get("fome")),
            "inicial": self.inicial, "final": {k: v for k, v in j.consumiveis.items() if v},
            "ganhos": self.ganhos, "do_bau": self.do_bau, "recursos": self.recursos, "baus": self.baus, "ofertas": self.ofertas,
            "usados": usados, "vendas": self.vendas, "compras": self.compras, "equip_comprado": self.equip_comprado, "contratos": self.contratos, "deixados": self.deixados,
            "mochila_max": self.mochila_max, "mochila_fim": len(j.mochila),
            "ouro_fontes": dict(g.estatisticas.get("ouro_fontes", {})),
            "ouro_gastos": dict(g.estatisticas.get("ouro_gastos", {})), "ouro_fim": j.ouro,
            "postura": self.postura, "comitiva": [m["id"] for m in comitiva.membros(g)],
        }


# ================================================================ relatório
def media(xs):
    return statistics.mean(xs) if xs else 0


def fmt(x):
    return f"{x:.1f}"


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


SUPRIMENTOS = [k for k in CONSUMIVEIS if k != "bau"]


def origem_curta(o):
    """A origem de um ganho em poucas classes: baú, luta (explorar/viagem/missão), evento, missão, compra."""
    partes = o.split("/")
    if "bau" in partes:
        return "baú"
    if partes[0] == "compra":
        return "compra"
    if "luta" in partes:
        return "luta da missão" if partes[0].startswith("missao") else "luta"
    if partes[0].startswith("missao"):
        return "missão"
    if partes[0] == "cuidado":
        return "cuidado"
    return "evento"


def usados_total(r, k):
    """Quanto de um suprimento se gastou: o que entrou (início e ganhos) menos o que sobrou. Vale também para a tocha,
    que acende sozinha e não entra no registro de uso."""
    entrou = r["inicial"].get(k, 0) + sum(q for i, q, _ in r["ganhos"] if i == k)
    return entrou - r["final"].get(k, 0)


CAUSAS = (("fome", "fome"), ("infecção", "infec"), ("queda", "caiu"))


def causa_curta(r):
    c = (r.get("causa") or "").lower()
    if r["fim"] != "parou":
        return r["fim"]
    for nome, chave in CAUSAS:
        if chave in c:
            return nome
    return "outra"


def economia_da_luta(classe, chave, n=60, vestido=False):
    """Uma luta comum do começo, no jogo de verdade (o lutador da arena, o herói de partida, inteiro a cada luta, com
    2 poções): o que custa e o que paga. `vestido`: com o equipamento sorteado do nível (dev.vestir), como quem já
    comprou o básico. Devolve médias: vitórias, vida perdida, poções, ouro e XP ganhos, ferimentos, e as noites de
    acampamento (30% da vida cada; cada noite, uma provisão por boca) para voltar à vida de antes."""
    import copy
    vit = vida = pocoes = ouro = xp = ferim = noites = 0
    for s in range(n):
        p = Percurso(classe, "descansada", "direto", 5000 + s)
        g = p.g
        if vestido:
            dev.vestir(g, random.Random(s), 1)
            g.j.recalcular()
        loc = next(l for l in g.mundo["locais"] if l.get("chave") == chave)
        g.mundo["atual"], g.periodo, g.clima = loc["id"], 1, "limpo"
        j = g.j
        j.hp, j.rec = j.max_hp, j.max_rec
        j.consumiveis["pocao_vida"] = 2
        antes = copy.deepcopy((j.ouro, j.xp, j.nivel, len(j.ferimentos)))
        try:
            r = g.combate(g.grupo())
        except Derrota:
            r = "derrota"
        g.fechar_espolio()
        vit += r == "vitoria"
        perdida = max(0.0, 1 - max(0, j.hp) / j.max_hp) if r != "derrota" else 1.0
        vida += perdida
        noites += -(-perdida // 0.3)
        pocoes += 2 - j.consumiveis.get("pocao_vida", 0)
        ouro += j.ouro - antes[0]
        xp += (j.xp - antes[1]) if j.nivel == antes[2] else j.xp + 1
        ferim += len(j.ferimentos) > antes[3]
    return {k: v / n for k, v in dict(vitorias=vit, vida=vida, pocoes=pocoes, ouro=ouro, xp=xp, ferimentos=ferim,
                                      noites=noites).items()}


def comeco(rs):
    """O começo do jogo com todos os percursos, os interrompidos incluídos: até onde cada classe chega, do que
    morre quem para, e o que leva na bolsa e no bolso nessa hora."""
    linhas = []
    for c in CLASSES:
        g = [r for r in rs if r["classe"] == c]
        if not g:
            continue
        parados = [r for r in g if r["fim"] == "parou"]
        causas = {}
        for r in parados:
            causas[causa_curta(r)] = causas.get(causa_curta(r), 0) + 1
        etapas = {}
        for r in g:
            etapas[r["etapa"]] = etapas.get(r["etapa"], 0) + 1
        linhas.append([c, len(g), sum(r["fim"] == "completo" for r in g), sum(r["fim"] == "limite" for r in g),
                       len(parados), ", ".join(f"{k} {v}" for k, v in sorted(causas.items(), key=lambda x: -x[1])),
                       fmt(media([r["nivel"] for r in parados])), fmt(media([r["dia"] for r in parados])),
                       fmt(media([sum(v for k, v in r["final"].items() if k != "bau") for r in parados])),
                       fmt(media([r["ouro_fim"] for r in parados])),
                       ", ".join(f"{k} {v}" for k, v in sorted(etapas.items(), key=lambda x: -x[1]))])
    return ("Começo do jogo, com os interrompidos (por classe):\n\n"
            + tabela(["Classe", "N", "Completos", "No dia limite", "Parados", "Do que param", "Nível ao parar",
                      "Dia ao parar", "Suprimentos na bolsa ao parar", "Ouro ao parar", "Etapa da Febre no fim"],
                     linhas))


def relatorio(rs, titulo="todos"):
    out = []
    n = len(rs)
    if not n:
        return "(nenhum percurso)"
    out.append(f"Percursos ({titulo}): {n} (completos: {sum(r['fim'] == 'completo' for r in rs)}; "
               f"no dia limite: {sum(r['fim'] == 'limite' for r in rs)}; parados: {sum(r['fim'] == 'parou' for r in rs)})")
    out.append("")
    grupos = {}
    for r in rs:
        grupos.setdefault((r["classe"], r["desfecho"], r["roteiro"]), []).append(r)
    linhas = []
    for (c, d, ro), g in sorted(grupos.items()):
        linhas.append([c, d, ro, len(g), fmt(media([r["dia"] for r in g])), fmt(media([r["nivel"] for r in g])),
                       fmt(media([r["lutas"] for r in g])), fmt(media([r["quedas"] for r in g])),
                       fmt(media([r["contratos"] for r in g])), fmt(media([len(r["baus"]) for r in g])),
                       fmt(media([sum(q for k, q, o in r["ganhos"] if k != "bau" and origem_curta(o) != "compra")
                                  for r in g])),
                       fmt(media([sum(usados_total(r, k) for k in SUPRIMENTOS) for r in g])),
                       fmt(media([sum(v for k, v in r["final"].items() if k != "bau") for r in g])),
                       fmt(media([len(r["ofertas"]) for r in g])),
                       fmt(media([sum(o["melhora"] for o in r["ofertas"]) for r in g]))])
    out.append("Por classe, desfecho e roteiro (médias por percurso):")
    out.append("")
    out.append(tabela(["Classe", "Desfecho", "Roteiro", "N", "Dias", "Nível", "Lutas", "Quedas", "Contratos", "Baús",
                       "Supr. achados", "Supr. gastos", "Supr. no fim", "Equip. achados", "Melhoram"], linhas))
    out.append("")

    cont = {}
    for r in rs:
        for o, tipo in r["baus"]:
            cont[tipo] = cont.get(tipo, 0) + 1
    out.append("Baús por origem (média por percurso):")
    out.append("")
    out.append(tabela(["Origem", "Média", "Parte"], [[t, fmt(v / n), f"{100 * v / max(1, sum(cont.values())):.0f}%"]
                                                    for t, v in sorted(cont.items(), key=lambda x: -x[1])]))
    out.append("")

    por = {}
    for r in rs:
        for k, q, o in r["ganhos"]:
            if k != "bau":
                por.setdefault(k, {}).setdefault(origem_curta(o), 0)
                por[k][origem_curta(o)] += q
    origens = ["baú", "luta", "luta da missão", "evento", "compra"]
    linhas = []
    for k in SUPRIMENTOS:
        if k not in por and not any(r["inicial"].get(k) for r in rs):
            continue
        linhas.append([CONSUMIVEIS[k]["nome"], fmt(sum(r["inicial"].get(k, 0) for r in rs) / n)]
                      + [fmt(por.get(k, {}).get(o, 0) / n) for o in origens]
                      + [fmt(sum(r["usados"].get((k, "luta"), 0) for r in rs) / n),
                         fmt(sum(usados_total(r, k) for r in rs) / n),
                         fmt(sum(r["final"].get(k, 0) for r in rs) / n), COMPRAS.get(k, 0)])
    out.append("Suprimentos da bolsa: de onde vêm, quanto se gasta e quanto sobra (média por percurso):")
    out.append("")
    out.append(tabela(["Item", "Início"] + [o.capitalize() for o in origens]
                      + ["Gastos na luta", "Gastos (total)", "No fim", "Alvo da compra"], linhas))
    out.append("")

    linhas = []
    for c in CLASSES:
        for d in DESFECHOS:
            g = [r for r in rs if r["classe"] == c and r["desfecho"] == d]
            if not g:
                continue
            linhas.append([c, d, len(g),
                           fmt(media([sum(q for k, q, o in r["ganhos"] if k != "bau" and origem_curta(o) != "compra")
                                      for r in g])),
                           fmt(media([sum(q for k, q, o in r["ganhos"] if k != "bau" and origem_curta(o) == "baú")
                                      for r in g])),
                           fmt(media([sum(q for k, q, o in r["ganhos"] if k != "bau" and origem_curta(o) == "compra")
                                      for r in g])),
                           fmt(media([sum(usados_total(r, k) for k in SUPRIMENTOS) for r in g])),
                           fmt(media([sum(v for k, v in r["final"].items() if k != "bau") for r in g])),
                           fmt(media([r["final"].get("pocao_vida", 0) for r in g]))])
    out.append("Suprimentos por classe e desfecho (média por percurso):")
    out.append("")
    out.append(tabela(["Classe", "Desfecho", "N", "Achados", "Deles, de baú", "Comprados", "Gastos",
                       "Na bolsa no fim", "Poções no fim"], linhas))
    out.append("")

    linhas = []
    for c in CLASSES:
        g = [r for r in rs if r["classe"] == c]
        ofs = [o for r in g for o in r["ofertas"]]
        if not ofs:
            continue
        por_origem = {}
        for o in ofs:
            por_origem.setdefault(origem_curta(o["origem"]), []).append(o)
        for orig, lista in sorted(por_origem.items()):
            linhas.append([c, orig, fmt(len(lista) / len(g)), f"{100 * sum(o['usa'] for o in lista) / len(lista):.0f}%",
                           f"{100 * sum(o['melhora'] for o in lista) / len(lista):.0f}%",
                           ", ".join(f"{k} {100 * sum(o['raridade'] == k for o in lista) / len(lista):.0f}%" for k in
                                     ("comum", "magico", "raro", "lendario") if any(o['raridade'] == k for o in lista))])
    out.append("Equipamento achado, por classe e origem:")
    out.append("")
    out.append(tabela(["Classe", "Origem", "Por percurso", "A classe usa", "Melhora o vestido", "Raridades"], linhas))
    out.append("")

    linhas = []
    for c in CLASSES:
        for d in DESFECHOS:
            g = [r for r in rs if r["classe"] == c and r["desfecho"] == d]
            if not g:
                continue
            entrou, gastos = {}, {}
            for r in g:
                for k, v in r["ouro_fontes"].items():
                    entrou[k] = entrou.get(k, 0) + v / len(g)
                for k, v in r["ouro_gastos"].items():
                    gastos[k] = gastos.get(k, 0) + v / len(g)
            linhas.append([c, d, fmt(media([len(r["ofertas"]) for r in g])),
                           fmt(media([len(r["vendas"]) for r in g])),
                           fmt(media([sum(v for _, v, _ in r["vendas"]) for r in g])),
                           fmt(media([len(r["equip_comprado"]) for r in g])),
                           fmt(media([r["mochila_max"] for r in g])), fmt(media([r["deixados"] for r in g])),
                           ", ".join(f"{k} {v:.0f}" for k, v in sorted(entrou.items(), key=lambda x: -x[1])),
                           ", ".join(f"{k} {v:.0f}" for k, v in sorted(gastos.items(), key=lambda x: -x[1])),
                           fmt(media([r["ouro_fim"] for r in g]))])
    out.append("Mochila, venda e ouro (média por percurso):")
    out.append("")
    out.append(tabela(["Classe", "Desfecho", "Cartões de item", "Vendidos", "Ouro das vendas", "Comprados (equip.)",
                       "Mochila (máx.)", "Deixados (cheia)", "Ouro entrou", "Ouro saiu", "Ouro no fim"], linhas))
    return "\n".join(out)


def rodar(classes, desfechos, roteiros, sementes, estrategia="atual"):
    rs = []
    for c in classes:
        for d in desfechos:
            for ro in roteiros:
                for s in sementes:
                    rs.append(Percurso(c, d, ro, s, estrategia).jogar())
    return rs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sementes", type=int, default=15)
    p.add_argument("--classes", default=",".join(CLASSES))
    p.add_argument("--desfechos", default=",".join(DESFECHOS))
    p.add_argument("--roteiros", default=",".join(ROTEIROS))
    p.add_argument("--detalhe", action="store_true")
    p.add_argument("--estrategia", default="atual", choices=list(ESTRATEGIAS))
    p.add_argument("--economia", action="store_true", help="só a conta de uma luta do começo (Charco e Bosque)")
    a = p.parse_args()
    if a.economia:
        print("| Classe | Lugar | Equipamento | Vitórias | Vida perdida | Poções | Ouro | Ferimento | Noites para sarar |")
        print("|---|---|---|---|---|---|---|---|---|")
        for c in CLASSES:
            for chave in ("charco_dos_juncos", "bosque_do_moinho"):
                for vestido in (False, True):
                    e = economia_da_luta(c, chave, vestido=vestido)
                    print(f"| {c} | {chave} | {'vestido' if vestido else 'de partida'} | {100 * e['vitorias']:.0f}% | "
                          f"{100 * e['vida']:.0f}% | {e['pocoes']:.2f} | {e['ouro']:.1f} | {100 * e['ferimentos']:.0f}% | "
                          f"{e['noites']:.1f} |")
        return
    rs = rodar(a.classes.split(","), a.desfechos.split(","), a.roteiros.split(","), range(1, a.sementes + 1), a.estrategia)
    print(comeco(rs))
    print()
    print(relatorio(rs))
    print()
    print(relatorio([r for r in rs if r["fim"] == "completo"], "só os completos"))
    if a.detalhe:
        print()
        for r in rs:
            print(r["classe"], r["desfecho"], r["roteiro"], r["semente"], r["fim"], r["desfecho_real"], "dia", r["dia"],
                  "nv", r["nivel"], "baús", len(r["baus"]), "fim", r["final"], "postura", r["postura"])


if __name__ == "__main__":
    main()
