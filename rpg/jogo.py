"""Estado do jogo, ciclo principal e ações do jogador."""

import json
import os
import random
import re

from . import eventos
from . import texto as tx
from .classes import CLASSES, COMPANHEIROS, HABILIDADES, SPECS, habilidades_ate
from .combate import Combate
from .dados import BIOMAS, CLIMAS, FAMILIAS, GUARDIOES, LORE, PERIODOS, PESOS_CLIMA, TRACOS
from .entidades import NOMES_STATS, Jogador
from .eventos.vila import ouvir_rumor
from . import inimigos
from .inimigos import criar, instanciar_antagonista, instanciar_guardiao
from . import itens
from .itens import CONSUMIVEIS, descrever_bonus, gerar_equip
from . import comitiva
from . import legado
from . import mapa
from . import sobrevivencia
from . import talentos
from . import telemetria
from .telemetria import registrar
from .mundo import gerar_mundo, nivel_regiao, vizinhos

VERSAO_SAVE = 1
NOMES_TESTE = {
    "forca": "Força", "destreza": "Destreza", "arcano": "Arcano",
    "percepcao": "Percepção", "vontade": "Vontade", "carisma": "Carisma",
}
NOMES_SLOT = {"arma": "Arma", "armadura": "Armadura", "amuleto": "Amuleto"}
LIMITE_MOCHILA = 8
# Criaturas que não aparecem em regiões fracas demais (evita lutas impossíveis no começo).
NIVEL_MIN_FAMILIA = {
    "bruxa_brejo": 2, "harpia": 2, "espectro": 3, "ent_jovem": 3, "cria_vazio": 3, "cao_infernal": 3,
    "golem": 4, "troll": 4, "grifo": 4, "abominacao": 6, "cavaleiro_sombrio": 6,
}
AMBIENTE_VILA = [
    "Portas pregadas com tábuas. Um X de cal marca as casas da peste.",
    "Uma mulher vende os sapatos do filho morto na praça.",
    "O sino da igreja não toca há meses. O padre foi o primeiro a fugir.",
    "Guardas magros e assustados vigiam a paliçada. Metade não tem botas.",
    "Crianças brincam de enterro. Elas conhecem bem as regras.",
    "Um corpo pende da forca da praça. A placa no pescoço diz: LADRÃO DE PÃO.",
    "O cheiro de fumaça, esterco e medo. Isto é o que sobrou de civilização.",
    "Um pregador grita que o fim chegou. Ninguém discute.",
]
NIVEL_MAXIMO = 12


class FimDeJogo(Exception):
    pass


class Derrota(Exception):
    """Interrompe a ação atual quando o herói cai (fora do modo hardcore)."""


class Jogo:
    def __init__(self, ui, seed=None, pasta_saves="saves", hardcore=True):
        self.ui = ui
        self.hardcore = hardcore
        self.seed = seed if seed is not None else random.randrange(1_000_000_000)
        self.rng = random.Random(self.seed)
        self.pasta_saves = pasta_saves
        self.j = None
        self.mundo = None
        self.dia = 1
        self.periodo = 0
        self.clima = "limpo"
        self.corrupcao = 0
        self.passos = 0
        self.flags = {}
        self.historico = {}
        self.contagem = {}
        self.impulsos = {}
        self.sementes = []
        self.rumores = []
        self.contratos = []
        self.ofertas = {}
        self.lojas = {}
        self.nemesis = None
        self.aliados_finais = []
        self.forcados = []
        self.proximo_id = 1
        self.combate_ativo = None
        self.autosalvar = False  # ligado pelo menu principal quando há uma pessoa jogando
        self.comitiva = []
        self.evento_atual = None
        self.sem_luz = False
        self.registro = []
        self.arquivo_run = None
        self.bestiario = {}
        self.lendas = []
        self.estatisticas = {"abates": 0, "eventos": 0, "ouro_ganho": 0, "chefes": 0, "quedas": 0}

    # ================================================================ atalhos
    @property
    def loc(self):
        return self.mundo["locais"][self.mundo["atual"]]

    @property
    def bioma(self):
        return self.loc["bioma"]

    @property
    def noite(self):
        return self.periodo >= 3

    @property
    def antagonista(self):
        return self.mundo["antagonista"]

    def dizer(self, texto="", cor=None):
        self.ui.dizer(texto, cor)

    def narrar(self, texto, cor=None):
        self.ui.narrar(texto, cor)

    def pausar(self):
        self.ui.pausar()

    def chance(self, p):
        return self.rng.random() < p

    def sortear(self, seq):
        return self.rng.choice(list(seq))

    def npc(self):
        return tx.npc(self.rng)

    def flag(self, nome, padrao=None):
        return self.flags.get(nome, padrao)

    def marcar(self, nome, valor=True):
        self.flags[nome] = valor

    def novo_id(self):
        self.proximo_id += 1
        return self.proximo_id

    def menu(self, pergunta, opcoes):
        """opcoes: lista de (rótulo, chave) ou None (opção indisponível)."""
        validas = [o for o in opcoes if o]
        rotulos = [self._anotar_teste(o[0]) for o in validas]
        metas = [o[2] if len(o) > 2 else None for o in validas]
        self.ui.meta_opcoes = metas if any(metas) else None
        try:
            esc = self.ui.escolher(pergunta, rotulos)
        finally:
            self.ui.meta_opcoes = None
        chave = validas[esc][1]
        if self.evento_atual and self.comitiva:
            comitiva.reagir_escolha(self, self.evento_atual, chave)
        return chave

    def _anotar_teste(self, rotulo):
        """'(Destreza)' vira '(Destreza +3)': mostra quanto você soma ao dado."""
        if not self.j or "(" not in rotulo:
            return rotulo
        for attr, nome in NOMES_TESTE.items():
            marca = f"({nome})"
            if marca in rotulo:
                mod = self.mod_teste(attr) - (4 if self.sem_luz and attr in ("percepcao", "destreza") else 0)
                rotulo = rotulo.replace(marca, f"({nome} {mod:+d} no d20)")
        return rotulo

    def ambiente(self):
        return self.sortear(BIOMAS[self.bioma]["ambiente"])

    # ================================================================ testes
    def mod_teste(self, attr):
        j = self.j
        base = j.nivel // 2
        if attr == "forca":
            return base + j.atk // 3
        if attr == "destreza":
            return base + j.agi // 2
        if attr == "arcano":
            return base + j.poder // 3
        if attr == "percepcao":
            return base + j.agi // 3 + (3 if j.classe == "arqueiro" else 0) + (2 if j.spec == "patrulheiro" else 0)
        if attr == "vontade":
            return base + j.defesa // 4 + (3 if j.spec == "paladino" else 0) + (2 if j.classe == "mago" else 0)
        if attr == "carisma":
            return base + j.reputacao // 10 + (2 if j.spec == "paladino" else 0)
        return base

    def teste(self, attr, cd):
        d = self.rng.randint(1, 20)
        mod = self.mod_teste(attr)
        if self.sem_luz and attr in ("percepcao", "destreza"):
            mod -= 4
        total = d + mod
        ok = d == 20 or (d != 1 and total >= cd)
        self.ui.rolagem(NOMES_TESTE[attr], cd, d, mod, total, ok)
        return ok

    # ================================================================ recompensas e perdas
    def ganhar_ouro(self, n):
        n = int(n * 0.75)  # o mundo é pobre: ninguém carrega muito ouro
        if n <= 0:
            return
        self.j.ouro += n
        self.estatisticas["ouro_ganho"] += n
        self.ui.efeito(f"+{n} ouro", "ouro")

    def perder_ouro(self, n):
        n = min(self.j.ouro, int(n))
        self.j.ouro -= n
        if n:
            self.ui.efeito(f"−{n} ouro", "perda")
        return n

    def ganhar_xp(self, n):
        n = int(n)
        if n <= 0 or self.j.nivel >= NIVEL_MAXIMO:
            return
        self.j.xp += n
        self.ui.efeito(f"+{n} XP", "xp")
        while self.j.nivel < NIVEL_MAXIMO and self.j.xp >= self.j.xp_proximo():
            self.j.xp -= self.j.xp_proximo()
            self.subir_nivel()

    def ferir(self, n, motivo=""):
        n = int(n)
        if n <= 0:
            return
        self.j.hp = max(1, self.j.hp - n)
        self.ui.efeito(f"−{n} vida{motivo} ({self.j.hp}/{self.j.max_hp})", "dano")

    def curar(self, n):
        c = self.j.curar(n)
        if c:
            self.ui.efeito(f"+{c} vida ({self.j.hp}/{self.j.max_hp})", "cura")

    def restaurar_recurso(self, n):
        j = self.j
        ganho = max(0, min(int(n), j.max_rec - j.rec))
        j.rec += ganho
        if ganho:
            self.ui.efeito(f"+{ganho} {j.nome_recurso}", "cura")

    def dar(self, item, qtd=1):
        self.j.consumiveis[item] = self.j.consumiveis.get(item, 0) + qtd
        self.ui.efeito(f"{CONSUMIVEIS[item]['nome']} ×{qtd}", "item")

    def bonus_permanente(self, stat, valor):
        """Bônus de atributo vindo de eventos, com teto por partida (evita acumular sem fim)."""
        teto = {"max_hp": 15, "max_rec": 15}.get(stat, 4)
        ganhos = self.flags.setdefault("bonus_eventos", {})
        ganho = max(0, min(valor, teto - ganhos.get(stat, 0)))
        if not ganho:
            self.dizer("(Você sente que já tirou tudo o que podia desse tipo de experiência.)", "cinza")
            return 0
        ganhos[stat] = ganhos.get(stat, 0) + ganho
        self.j.base[stat] += ganho
        self.j.recalcular()
        self.ui.efeito(f"+{ganho} {NOMES_STATS[stat]} permanente", "nivel")
        return ganho

    def dar_provisoes(self, n):
        antes = self.j.provisoes
        self.j.provisoes = min(sobrevivencia.MAX_PROVISOES, antes + n)
        if self.j.provisoes > antes:
            self.ui.efeito(f"+{self.j.provisoes - antes} dia(s) de comida (total {self.j.provisoes})", "item")

    def dar_flechas(self, n):
        if self.j.classe != "arqueiro" or n <= 0:
            return
        self.j.flechas += n
        self.ui.efeito(f"+{n} flechas (total {self.j.flechas})", "item")

    def mudar_reputacao(self, d):
        antes = self.j.reputacao
        self.j.reputacao = max(-50, min(50, antes + d))
        if self.j.reputacao > antes:
            self.ui.efeito(f"Reputação +{self.j.reputacao - antes}", "rep")
        elif self.j.reputacao < antes:
            self.ui.efeito(f"Reputação −{antes - self.j.reputacao}", "perda")

    def corromper(self, d, silencioso=False):
        antes = self.corrupcao
        self.corrupcao = max(0, min(100, antes + d))
        if not silencioso:
            if d < 0:
                self.dizer(f"A corrupção do reino recua. ({self.corrupcao}%)", "verde")
            elif d > 0:
                self.dizer(f"A corrupção do reino aumenta. ({self.corrupcao}%)", "magenta")
        for limiar, texto in ((25, "As colheitas murcham e os animais andam inquietos. A sombra de {a} se espalha."),
                              (50, "Crias do Vazio são vistas em plena luz do dia. Os sinos das vilas tocam sem ninguém puxar as cordas."),
                              (75, "O céu tem cor de hematoma. Rumores dizem que {a} está prestes a atravessar a Fenda."),
                              (90, "O mundo range como um navio prestes a afundar. Resta pouco tempo!")):
            if antes < limiar <= self.corrupcao:
                self.ui.separador("magenta")
                self.dizer(texto.format(a=self.antagonista["curto"]), "magenta+negrito")
        if self.corrupcao >= 100:
            self.fim_de_jogo(f"A corrupção consumiu o reino. {tx.maiuscula(self.antagonista['curto'])} atravessou a "
                             f"Fenda, e o mundo que você conhecia deixou de existir.")

    # ---------------------------------------------------------------- sementes (consequências futuras)
    def plantar(self, id, atraso=4, **dados):
        self.sementes.append({"id": id, "pronto": self.passos + atraso, "dados": dados})

    def semente(self, id):
        for s in self.sementes:
            if s["id"] == id and s["pronto"] <= self.passos:
                return s
        return None

    def colher(self, id):
        s = self.semente(id)
        if s:
            self.sementes.remove(s)
            return s["dados"]
        return None

    def aliado_final(self, nome, texto, efeito, valor):
        if any(a["nome"] == nome for a in self.aliados_finais):
            return
        self.aliados_finais.append({"nome": nome, "texto": texto, "efeito": efeito, "valor": valor})
        self.dizer(f"({nome} pode ajudar você quando a hora final chegar.)", "ciano")

    def rumor_aqui(self, evento):
        for r in self.rumores:
            if r.get("evento") == evento and r.get("local") == self.loc["id"]:
                return r
        return None

    def consumir_rumor(self, evento):
        r = self.rumor_aqui(evento)
        if r:
            self.rumores.remove(r)
            self.impulsos.pop(evento, None)
        return r

    def evento_forcado(self, contexto):
        if self.forcados:
            return self.forcados.pop(0)
        return None

    # ================================================================ inimigos e combate
    def nivel_inimigo(self, bonus=0):
        variacao = [-1, 0, 0] if self.nivel_local() <= 2 else [-1, 0, 0, 1]
        n = self.nivel_local() + self.rng.choice(variacao) + bonus
        return max(1, min(15, n))

    def mundo_vizinhos(self):
        return vizinhos(self.mundo, self.loc)

    def nivel_local(self):
        return nivel_regiao(self.loc, self.corrupcao)

    def inimigo(self, familia, bonus=0, afixo=None, nome_unico=None, nivel=None):
        return criar(self.rng, familia, nivel or self.nivel_inimigo(bonus), afixo, nome_unico)

    def afixo_aleatorio(self):
        p = 0.10 + self.loc["perigo"] * 0.03 + self.corrupcao / 400
        if self.j.nivel <= 1 or not self.chance(p):
            return None
        if self.corrupcao >= 30 and self.chance(self.corrupcao / 150):
            return "corrompido"
        return self.sortear(["feroz", "robusto", "agil", "venenoso", "anciao", "flamejante"])

    def familias_locais(self):
        nv = self.nivel_local()
        familias = [f for f in BIOMAS[self.bioma]["familias"] if NIVEL_MIN_FAMILIA.get(f, 1) <= nv]
        if self.corrupcao >= 30:
            familias += ["caido"] + (["cao_infernal"] if nv >= 3 else [])
        if self.corrupcao >= 40:
            familias.append("cria_vazio")
        if self.corrupcao >= 70:
            familias.append("abominacao")
        if self.noite and self.bioma in ("ruinas", "pantano", "planicie"):
            familias.append("espectro")
        return familias

    def grupo(self, familia=None, n=None, bonus=0):
        """Gera um encontro: grupo comum, bando de campeões ou um único nomeado com escolta."""
        familia = familia or self.sortear(self.familias_locais())
        f = FAMILIAS[familia]
        nv = self.nivel_local()
        tipo = "normal"
        if n is None:
            lo, hi = f["grupo"]
            n = self.rng.randint(lo, hi)
            if nv <= 2:
                n = 1 if self.chance(0.75) else min(n, 2)
            elif nv <= 4:
                n = 1 if self.chance(0.5) else min(n, 2)
            for _ in self.comitiva:  # uma comitiva chama atenção: mais inimigos aparecem
                if self.chance(0.45):
                    n = min(n + 1, hi + 1)
            r = self.rng.random()
            if nv >= 5 and r < 0.03 + nv * 0.006:
                tipo = "unico"
            elif nv >= 4 and r < 0.08 + nv * 0.012:
                tipo = "campeoes"

        if tipo == "campeoes":
            afixo = self.sortear(["feroz", "robusto", "agil", "venenoso", "flamejante", "corrompido"])
            grupo = [self.inimigo(familia, bonus, afixo) for _ in range(max(2, min(n, 3)))]
            for e in grupo:
                e.max_hp = int(e.max_hp * 1.25)
                e.hp = e.max_hp
                e.xp = int(e.xp * 1.4)
                e.nome = "Campeão " + e.nome if e.g == "m" else "Campeã " + e.nome
            self.dizer("Um bando de CAMPEÕES: eles se movem juntos, com um brilho azulado nos olhos.",
                       "azul+negrito")
        elif tipo == "unico":
            a1, a2 = self.rng.sample(["feroz", "robusto", "agil", "venenoso", "anciao", "flamejante", "corrompido"], 2)
            chefe = self.inimigo(familia, bonus + 1, a1, nome_unico=tx.nome_proprio(self.rng))
            inimigos.adicionar_afixo(chefe, a2)
            escolta = []
            if f["grupo"][1] > 1:
                escolta = [self.inimigo(familia, bonus) for _ in range(self.rng.randint(1, 2))]
            grupo = [chefe] + escolta
            self.dizer(f"Um nome sussurrado com medo nas vilas: {chefe.nome}. Uma criatura ÚNICA.",
                       "amarelo+negrito")
        else:
            grupo = [self.inimigo(familia, bonus, self.afixo_aleatorio()) for _ in range(n)]
            if n == 1 and f["grupo"][1] == 1 and nv >= 3 and self.chance(0.25):
                outra = self.sortear(BIOMAS[self.bioma]["familias"])
                if FAMILIAS[outra]["grupo"][1] > 1:
                    grupo.append(self.inimigo(outra, bonus))
        if familia == "caido" and self.chance(0.35 if nv <= 4 else 0.6):
            grupo.append(self.inimigo("xama_caido", bonus))
        return grupo

    def combate(self, inimigos, emboscada=None, pode_fugir=True, titulo=None):
        r = Combate(self, inimigos, emboscada, pode_fugir, titulo).executar()
        if r == "derrota":
            causa = f"Você tombou diante de {tx.lista_natural([e.nome for e in inimigos])}."
            if self.hardcore:
                self.fim_de_jogo(causa)
            self.dizer(causa, "vermelho+negrito")
            raise Derrota()
        if r == "fuga" and not self.nemesis:
            elite = next((e for e in inimigos if e.vivo and (e.afixo or e.unico) and not e.chefe
                          and e.familia in FAMILIAS and not e.chave), None)
            if elite:
                nome = elite.nome.split(",")[0] if elite.unico else tx.nome_proprio(self.rng)
                self.nemesis = {"familia": elite.familia, "afixo": elite.afixo or "feroz", "nome": nome,
                                "nivel": elite.nivel + 1, "pronto": self.passos + 4, "vezes": 0}
                self.dizer("Enquanto foge, você ouve um rugido às suas costas. Algo te marcou como presa. "
                           "Você ainda vai rever essa criatura...", "magenta")
        return r

    def registrar_abates(self, derrotados):
        self.estatisticas["abates"] += len(derrotados)
        for e in derrotados:
            if e.familia in self.bestiario:
                self.bestiario[e.familia]["abates"] += 1
                if self.bestiario[e.familia]["abates"] == 5:
                    self.dizer(f"Você agora conhece {FAMILIAS[e.familia]['plural']} como ninguém. "
                               f"(mestre caçador: +10% de dano contra eles)", "verde")
            if e.chave == "nemesis":
                self.nemesis = None
                self.dizer("Seu nêmesis finalmente tomba. Você sente um peso sair dos ombros.", "verde+negrito")
                self.ganhar_ouro(30 + 10 * self.j.nivel)
            for c in self.contratos:
                if c.get("concluido"):
                    continue
                if c["tipo"] == "caca" and e.familia == c["familia"] and self.loc["id"] == c["local"]:
                    c["feito"] += 1
                    if c["feito"] >= c["total"]:
                        c["concluido"] = True
                        self.dizer(f"Contrato concluído: {c['desc']} Receba a recompensa em qualquer vila.", "verde")
                elif c["tipo"] == "alvo" and e.chave == c["chave"]:
                    c["concluido"] = True
                    self.dizer(f"Contrato concluído: {c['desc']} Receba a recompensa em qualquer vila.", "verde")

    def saque_de_combate(self, derrotados):
        elites = sum(1 for e in derrotados if e.afixo or e.unico)
        chefe = any(e.chefe for e in derrotados)
        if any("humano" in e.tracos for e in derrotados) and self.chance(0.35):
            self.dizer("Nos alforjes dos mortos, um pouco de comida.", "cinza")
            self.dar_provisoes(1)
        if self.chance(0.15 + 0.1 * elites):
            self.dar(self.sortear(["bandagem", "bandagem", "tocha", "tocha", "pocao_vida", "tonico", "antidoto"]))
        if self.j.classe == "arqueiro" and any(e.familia in ("bandido", "mercenario") for e in derrotados) \
                and self.chance(0.5):
            self.dizer("Você encontra uma aljava com flechas entre os pertences dos inimigos.", "verde")
            self.dar_flechas(self.rng.randint(3, 8))
        if chefe or self.chance(0.07 + 0.2 * elites):
            nivel = min(max(e.nivel for e in derrotados), self.j.nivel + 2)
            self.oferecer_equip(gerar_equip(self.rng, self.j.classe, nivel, qualidade=1 if chefe else 0))

    # ================================================================ equipamento e itens
    def oferecer_equip(self, item):
        raridade = itens.NOMES_RARIDADE[item.get("raridade", "comum")]
        self.dizer(f"Você encontrou: {itens.rotulo(item)} [{NOMES_SLOT[item['slot']]}, {raridade}]",
                   itens.cor(item) or "branco+negrito")
        self.dizer(f"  {descrever_bonus(item['bonus'])}", itens.cor(item))
        if item.get("lore"):
            self.dizer(f"  \"{item['lore']}\"", "cinza")
        atual = self.j.equip[item["slot"]]
        if atual:
            self.dizer(f"  Equipado agora: {itens.rotulo(atual)} — {descrever_bonus(atual['bonus'])}", "cinza")
        op = self.menu("O que fazer com o item?", [
            ("Equipar agora", "equipar"),
            ("Guardar na mochila (para vender ou usar depois)", "guardar") if len(self.j.mochila) < LIMITE_MOCHILA
            else None,
            ("Deixar para trás", "deixar"),
        ])
        if op == "equipar":
            self.equipar(item)
        elif op == "guardar":
            self.j.mochila.append(item)
            self.dizer("Guardado na mochila.", "cinza")

    def equipar(self, item):
        j = self.j
        antigo = j.equip[item["slot"]]
        j.equip[item["slot"]] = item
        if item in j.mochila:
            j.mochila.remove(item)
        if antigo:
            if len(j.mochila) < LIMITE_MOCHILA:
                j.mochila.append(antigo)
            else:
                self.dizer(f"Mochila cheia: {antigo['nome']} fica para trás.", "cinza")
        j.recalcular()
        self.dizer(f"Você equipa {item['nome']}.", "verde")
        registrar(self, "equipar", item=item["nome"], slot=item["slot"], raridade=item.get("raridade", "comum"),
                  bonus=item["bonus"])

    def usar_consumivel(self, k):
        j = self.j
        if not j.tem(k):
            return False
        j.consumiveis[k] -= 1
        nome = CONSUMIVEIS[k]["nome"]
        registrar(self, "consumivel", item=k, em_combate=self.combate_ativo is not None)
        if k == "pocao_vida":
            c = j.curar(j.max_hp * 0.35)
            self.dizer(f"Você bebe a {nome}. (+{c} vida)", "verde")
        elif k == "tonico":
            ganho = min(j.max_rec - j.rec, j.max_rec // 2)
            j.rec += ganho
            self.dizer(f"Você bebe o {nome}. (+{ganho} {j.nome_recurso})", "azul")
        elif k == "antidoto":
            j.remover("veneno")
            self.dizer("O veneno deixa seu corpo.", "verde")
        elif k == "bandagem":
            sangrando = j.efeito("sangramento")
            j.remover("sangramento")
            tratou = sobrevivencia.tratar_com_bandagem(self)
            c = j.curar(8)
            if not tratou and not sangrando:
                self.dizer(f"Você troca as faixas velhas. (+{c} vida)", "verde")
            elif sangrando:
                self.dizer(f"O sangramento para. (+{c} vida)", "verde")
        elif k == "unguento":
            if not sobrevivencia.tem(j, "infeccao"):
                j.consumiveis[k] += 1
                self.dizer("Você não tem nenhuma infecção para tratar.", "cinza")
                return False
            sobrevivencia.curar_ferimento(self, "infeccao")
            self.dizer("O unguento arde como fogo. Horas depois, a febre cede. Infecção curada.", "verde+negrito")
        else:
            j.consumiveis[k] += 1
            self.dizer("Isso não tem uso agora.", "cinza")
            return False
        return True

    # ================================================================ progressão
    def subir_nivel(self):
        j = self.j
        j.nivel += 1
        cresc = dict(CLASSES[j.classe]["cresc"])
        if j.spec:
            for k, v in SPECS[j.spec]["cresc"].items():
                cresc[k] = cresc.get(k, 0) + v
        antes_hp, antes_rec = j.max_hp, j.max_rec
        antes = {k: getattr(j, k) for k in ("max_hp", "max_rec", "atk", "defesa", "agi", "poder")}
        for k, v in cresc.items():
            j.base[k] += v
        j.recalcular()
        j.hp = min(j.max_hp, j.hp + max(0, j.max_hp - antes_hp))  # só ganha o que o máximo aumentou
        comitiva.atualizar_vida_maxima(self)
        j.rec = min(j.max_rec, j.rec + max(0, j.max_rec - antes_rec))
        registrar(self, "nivel", stats=telemetria.instantaneo(j))
        if j.companheiro:
            j.companheiro["max_hp"] += 5
            j.companheiro["atk"] += 1.5
            j.companheiro["hp"] = j.companheiro["max_hp"]
        self.ui.titulo(f"NÍVEL {j.nivel}!", "verde+negrito")
        self.dizer("Você se sente mais forte. (Subir de nível não cura feridas: isso, só o descanso.)", "verde")
        self.ganhar_ponto_talento()
        novas = self._aprender_habilidades()
        ganhos = {NOMES_STATS.get(k, k) if k != "max_rec" else j.nome_recurso: getattr(j, k) - v
                  for k, v in antes.items() if getattr(j, k) > v}
        self.ui.celebrar("nivel", {"nivel": j.nivel, "ganhos": ganhos, "pontos": j.pontos_talento,
                                   "habilidades": [{"nome": HABILIDADES[h]["nome"], "desc": HABILIDADES[h]["desc"]}
                                                   for h in novas],
                                   "especializacao": j.nivel >= 4 and not j.spec})
        if j.nivel >= 4 and not j.spec and f"encruzilhada_{j.classe}" not in self.forcados:
            self.forcados.append(f"encruzilhada_{j.classe}")
            self.dizer("Você sente que uma encruzilhada se aproxima em seu caminho...", "magenta")

    def ganhar_ponto_talento(self, n=1):
        self.j.pontos_talento += n
        self.dizer(f"+{n} ponto de talento! (use em \"Talentos\" — você tem {self.j.pontos_talento})",
                   "amarelo+negrito")

    def menu_talentos(self):
        while True:
            j = self.j
            self.ui.cena("Talentos", f"{j.nome_classe} · pontos disponíveis: {j.pontos_talento}", "menu")
            if getattr(self.ui, "web", False):
                self.ui.arvore_talentos(talentos.dados_arvore(j))
            else:
                self.ui.desenhar(talentos.desenhar(j))
                self.dizer("verde = aprendido · amarelo = disponível · cinza = bloqueado", "cinza")
            opcoes = []
            for t in talentos.TALENTOS[j.classe]:
                est = talentos.estado(j, t)
                texto = f"{t['nome']} {j.tal(t['id'])}/{t['max']} — {t['desc']}"
                if est == "disponivel" and j.pontos_talento:
                    texto = "▶ " + texto
                elif est != "disponivel":
                    texto += f" ({talentos.motivo(t, est) or 'completo'})"
                opcoes.append((texto, t, {"talento": t["id"]}))
            t = self.menu("Escolha um talento para aprender:", opcoes + [("Voltar", None, {"voltar": True})])
            if t is None:
                return
            est = talentos.estado(j, t)
            if est != "disponivel":
                self.dizer(f"Indisponível: {talentos.motivo(t, est) or 'já está no máximo'}.", "vermelho")
            elif not j.pontos_talento:
                self.dizer("Você não tem pontos de talento. Suba de nível ou derrote guardiões.", "vermelho")
            else:
                j.pontos_talento -= 1
                j.talentos[t["id"]] = j.tal(t["id"]) + 1
                registrar(self, "talento", id=t["id"], nome=t["nome"], rank=j.tal(t["id"]))
                antes = j.max_hp
                j.recalcular()
                j.hp += max(0, j.max_hp - antes)
                self.dizer(f"Você aprendeu {t['nome']} ({j.tal(t['id'])}/{t['max']}).", "verde+negrito")

    def _aprender_habilidades(self):
        j = self.j
        novas = []
        for h in habilidades_ate(j.classe, j.spec, j.nivel):
            if h not in j.habilidades:
                j.habilidades.append(h)
                novas.append(h)
                self.dizer(f"Nova habilidade: {HABILIDADES[h]['nome']} — {HABILIDADES[h]['desc']}", "amarelo+negrito")
        return novas

    def especializar(self, spec):
        j = self.j
        j.spec = spec
        registrar(self, "spec", spec=spec)
        for k, v in SPECS[spec]["bonus"].items():
            j.base[k] += v
        j.recalcular()
        j.hp = j.max_hp
        j.rec = j.max_rec
        self.ui.titulo(f"VOCÊ AGORA É {SPECS[spec]['nome'].upper()}", "magenta+negrito")
        self.dizer(SPECS[spec]["desc"], "magenta")
        novas = self._aprender_habilidades()
        self.ui.celebrar("spec", {"nome": SPECS[spec]["nome"], "desc": SPECS[spec]["desc"],
                                  "habilidades": [{"nome": HABILIDADES[h]["nome"], "desc": HABILIDADES[h]["desc"]}
                                                  for h in novas]})
        etiquetas = {"necromante": ("magia_proibida", "sacrilegio"), "paladino": ("fe", "honra"),
                     "piromante": ("curiosidade",), "berserker": ("violencia", "coragem"), "sombra": ("trapaca",)}
        if spec in etiquetas:
            comitiva.reagir(self, *etiquetas[spec], forca=1.5)
        if spec == "patrulheiro":
            self.escolher_companheiro()

    def escolher_companheiro(self, tipo=None):
        if tipo is None:
            tipos = list(COMPANHEIROS)
            esc = self.ui.escolher("Qual animal atende ao seu chamado?",
                                   [f"{COMPANHEIROS[t]['nome']} — {COMPANHEIROS[t]['desc']}" for t in tipos])
            tipo = tipos[esc]
        c = COMPANHEIROS[tipo]
        nv = self.j.nivel
        nome = self.ui.perguntar(f"Como vai chamar seu {c['nome'].split()[0].lower()}? (Enter para '{c['nome']}')",
                                 c["nome"])
        hp = int(c["hp"] * (1 + 0.15 * (nv - 1)))
        self.j.companheiro = {"nome": nome, "tipo": tipo, "max_hp": hp, "hp": hp,
                              "atk": c["atk"] * (1 + 0.2 * (nv - 1)), "agi": c["agi"],
                              "alcance": c["alcance"], "crit": c["crit"]}
        self.dizer(f"{nome} agora caminha ao seu lado.", "verde+negrito")

    # ================================================================ tempo e clima
    def rolar_clima(self):
        pesos = PESOS_CLIMA.get(self.bioma, PESOS_CLIMA["padrao"])
        self.clima = self.rng.choices(list(pesos), weights=list(pesos.values()))[0]

    def avancar_periodo(self):
        self.passos += 1
        self.periodo += 1
        if self.periodo == 3:
            self.dizer("A noite cai. Algo começa a se mover nas trevas, e não é gente.", "magenta")

    def novo_dia(self, descanso=1):
        self.dia += 1
        self.periodo = 0
        restantes = sum(1 for l in self.mundo["locais"] if l["tipo"] == "covil" and not l["guardiao"]["derrotado"])
        self.rolar_clima()
        self.rumores = [r for r in self.rumores if r["expira"] >= self.dia]
        self.impulsos = {}
        for r in self.rumores:
            if r.get("evento"):
                self.impulsos[r["evento"]] = self.impulsos.get(r["evento"], 1) * 3
        self.ui.separador()
        self.dizer(f"Amanhece o dia {self.dia}. {CLIMAS[self.clima]['desc']}", "amarelo")
        self.corromper(2 if restantes else 1, silencioso=True)
        sobrevivencia.amanhecer(self, descanso)
        comitiva.amanhecer(self, descanso)
        registrar(self, "dia", descanso=descanso, provisoes=self.j.provisoes, fome=self.j.fome,
                  corrupcao=self.corrupcao, ferimentos=len(self.j.ferimentos), local=self.loc["nome"])

    def descansar(self, fracao, mana=1.0):
        """Descanso devolve pouca vida: ferimentos de verdade levam dias. Com fome, quase nada."""
        j = self.j
        if j.fome:
            fracao *= 0.3
        cura = j.curar(j.max_hp * fracao)
        if cura:
            self.dizer(f"Você recupera {cura} de vida. ({j.hp}/{j.max_hp})", "verde")
        if j.classe == "mago":
            j.rec = min(j.max_rec, j.rec + int(j.max_rec * mana))
        else:
            j.rec = j.max_rec
        j.efeitos = {}
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]
        comitiva.descansar(self, fracao)

    # ================================================================ início
    def novo_jogo(self):
        self.ui.cena("Criação de personagem", None, "menu")
        nome = self.ui.perguntar("Qual é o seu nome, aventureiro(a)?", "Aventureiro")
        self.dizer()
        self.dizer("Escolha sua classe. No nível 4 ela se ramifica em uma de duas especializações:", "ciano")
        classes = list(CLASSES)
        for c in classes:
            d = CLASSES[c]
            specs = " | ".join(SPECS[s]["nome"] for s in d["specs"])
            self.dizer(f"  {d['nome']} → {specs}", d["cor"] + "+negrito")
            self.dizer(f"    {d['desc']}", "cinza")
        esc = self.ui.escolher("Sua classe:", [CLASSES[c]["nome"] for c in classes])
        self.iniciar(nome, classes[esc])
        self.introducao()

    def iniciar(self, nome, classe):
        self.j = Jogador(nome, classe)
        self.mundo = gerar_mundo(self.rng)
        self.loc["visitado"] = True
        self.rolar_clima()
        self.j.equip["arma"] = gerar_equip(self.rng, classe, 1, "arma", qualidade=-2)
        self.j.recalcular()
        self.j.hp = self.j.max_hp
        self.preparar_legado()
        registrar(self, "inicio", nome=nome, classe=classe, seed=self.seed, hardcore=self.hardcore,
                  stats=telemetria.instantaneo(self.j))

    # ================================================================ legado e bestiário
    def preparar_legado(self):
        """Heróis de partidas anteriores deixam marcas neste mundo."""
        self.lendas = legado.carregar(self.pasta_saves)[-6:]
        if not self.lendas:
            return
        ultimo = self.lendas[-1]
        if ultimo["resultado"] == "vitoria":
            self.marcar("estatua", ultimo)
            self.j.reputacao += 5
        else:
            selvagens = [l for l in self.mundo["locais"] if l["tipo"] == "selvagem"]
            self.marcar("tumulo", dict(ultimo, local=self.sortear(selvagens)["id"]))

    def registrar_legado(self, resultado, causa):
        j = self.j
        legado.registrar(self.pasta_saves, {
            "nome": j.nome, "classe": j.classe, "spec": j.spec, "nome_classe": j.nome_classe, "nivel": j.nivel,
            "dia": self.dia, "resultado": resultado, "causa": causa, "arma": j.equip["arma"],
            "antagonista": self.antagonista["nome"], "sigilos": len(j.sigilos),
        })

    def ver_criatura(self, familia):
        if familia in FAMILIAS:
            b = self.bestiario.setdefault(familia, {"vistos": 0, "abates": 0})
            b["vistos"] += 1

    def conhece(self, familia):
        """Fraquezas e habilidades ficam visíveis após 2 abates (magos estudam à primeira vista)."""
        if familia not in FAMILIAS:
            return True
        return self.j.classe == "mago" or self.bestiario.get(familia, {}).get("abates", 0) >= 2

    def mestre_caca(self, familia):
        return self.bestiario.get(familia, {}).get("abates", 0) >= 5

    def ver_bestiario(self):
        self.ui.cena("Bestiário", f"{len(self.bestiario)}/{len(LORE)} criaturas", "menu")
        fichas = []
        for fam, b in sorted(self.bestiario.items(), key=lambda x: FAMILIAS[x[0]]["nome"]):
            f = FAMILIAS[fam]
            conhece = self.conhece(fam)
            fichas.append({"id": fam, "nome": tx.maiuscula(f["nome"]), "abates": b["abates"], "lore": LORE.get(fam, ""),
                           "conhecido": conhece, "mestre": self.mestre_caca(fam), "tracos": f["tracos"],
                           "tracos_nomes": [TRACOS[t].split(":")[0] for t in f["tracos"]] if conhece else [],
                           "fraquezas": [k for k, v in f.get("resist", {}).items() if v > 1] if conhece else [],
                           "resiste": [k for k, v in f.get("resist", {}).items() if v < 1] if conhece else []})
        if self.ui.painel("bestiario", {"fichas": fichas, "total": len(LORE)}):
            self.pausar()
            return
        if not self.bestiario:
            self.dizer("Você ainda não enfrentou nenhuma criatura.", "cinza")
        for fam, b in sorted(self.bestiario.items(), key=lambda x: FAMILIAS[x[0]]["nome"]):
            f = FAMILIAS[fam]
            selo = "  ★ mestre caçador: +10% de dano" if self.mestre_caca(fam) else ""
            self.dizer(f"{tx.maiuscula(f['nome'])} — abates: {b['abates']}{selo}", "amarelo+negrito")
            self.dizer(f"  {LORE.get(fam, '')}", "cinza")
            if self.conhece(fam):
                tracos = ", ".join(TRACOS[t].split(":")[0] for t in f["tracos"])
                fracos = [k for k, v in f.get("resist", {}).items() if v > 1]
                info = f"  Traços: {tracos}"
                if fracos:
                    info += f" · fraco contra {', '.join(fracos)}"
                self.dizer(info)
            else:
                self.dizer("  Detalhes: ??? (derrote mais destas criaturas para aprender)", "cinza")
        self.pausar()

    def introducao(self):
        a = self.antagonista
        self.ui.cena("O reino à beira do Vazio", "prólogo", "evento")
        self.narrar("Não houve profecia. Não há escolhido. Há cem anos uma Fenda se abriu sob a catedral, e desde "
                    "então o reino apodrece devagar, como um corpo que ainda não percebeu que morreu.", "cinza")
        self.narrar(f"Do outro lado fala {a['nome']}, {a['origem']}.")
        self.narrar("Três guardiões, deformados pela Fenda, guardam os Sigilos que selam o caminho até "
                    f"a {self.mundo['locais'][-1]['nome']}. Cavaleiros melhores que você já tentaram. Os corvos "
                    "ainda se lembram do gosto deles.")
        self.narrar("A cada dia a corrupção avança. Quando chegar a 100%, não haverá mais reino para salvar.")
        self.narrar(f"Você, {self.j.nome}, {self.j.nome_classe.lower()}, parte de {self.loc['nome']} com "
                    f"{self.j.provisoes} dias de comida, {self.j.ouro} moedas e nenhuma garantia de voltar.")
        self.dizer("A fome mata. Feridas infeccionam. A noite cega. E a morte é permanente.", "vermelho+negrito")
        estatua = self.flag("estatua")
        if estatua:
            self.narrar(f"Na praça da vila há uma estátua nova: {estatua['nome']}, {estatua['nome_classe'].lower()}, "
                        f"que derrotou {estatua['antagonista']} em outra era. O povo olha para você com "
                        f"esperança. (reputação +5)", "amarelo")
        elif self.flag("tumulo"):
            t = self.flag("tumulo")
            self.narrar(f"Dizem que, em algum lugar destas terras, está o túmulo de {t['nome']}, quem tentou "
                        f"antes de você.", "cinza")
        self.dizer("Dica: compre provisões e tochas antes de sair, trate feridas abertas com bandagens e não vá "
                   "aonde o mapa diz que os inimigos são fortes demais. Suas escolhas voltarão para você.", "cinza")
        self.pausar()

    # ================================================================ ciclo principal
    def rodar(self):
        try:
            while True:
                try:
                    self.tela()
                except Derrota:
                    self.resgate()
        except FimDeJogo:
            return

    def resgate(self):
        """Fora do modo hardcore, cair em combate custa ouro e tempo (e o tempo alimenta a corrupção)."""
        j = self.j
        self.estatisticas["quedas"] += 1
        locais = self.mundo["locais"]
        from .mundo import _distancias
        dist = _distancias(locais, self.loc["id"])
        vila = min((l for l in locais if l["tipo"] == "vila"), key=lambda l: dist.get(l["id"], 99))
        p = self.npc()
        self.ui.cena("Tudo escurece...", None, "evento")
        self.narrar(f"Você acorda numa cama de palha em {vila['nome']}, com o corpo enfaixado. {p['um'].capitalize()} "
                    f"{p['prof']} {p['traco']} te encontrou desacordado na estrada e te arrastou até "
                    f"aqui. Dois dias se passaram.", "cinza")
        perda = self.perder_ouro(j.ouro * 0.3)
        if perda:
            self.dizer("Parte do seu ouro sumiu enquanto você estava desacordado.", "cinza")
        self.mundo["atual"] = vila["id"]
        vila["visitado"] = True
        j.efeitos = {}
        j.rec = j.max_rec
        if j.companheiro:
            j.companheiro["hp"] = j.companheiro["max_hp"]
        j.hp = max(j.hp, int(j.max_hp * 0.4))
        self.novo_dia(descanso=0)
        self.novo_dia(descanso=1)
        self.pausar()

    def contexto_cena(self):
        return (f"{self.loc['nome']} · dia {self.dia}, {PERIODOS[min(self.periodo, 3)].lower()} · "
                f"{CLIMAS[self.clima]['nome'].lower()}")

    def cabecalho(self):
        j = self.j
        loc = self.loc
        ui = self.ui
        tipo = {"vila": "Vila", "selvagem": BIOMAS[loc["bioma"]]["nome"], "covil": BIOMAS[loc["bioma"]]["nome"],
                "cidadela": "Cidadela"}[loc["tipo"]]
        perigo = "" if loc["tipo"] == "vila" else f" · inimigos Nv.{self.nivel_local()}"
        ui.cena(loc["nome"], f"{tipo}{perigo} · dia {self.dia}, {PERIODOS[min(self.periodo, 3)].lower()} · "
                             f"{CLIMAS[self.clima]['nome'].lower()} · corrupção {self.corrupcao}%", "local")
        if getattr(ui, "hud", False):
            return  # o painel lateral já mostra o resto
        ui.dizer(f" {j.nome}, {j.nome_classe} Nv.{j.nivel}  (XP {j.xp}/{j.xp_proximo()})  "
                 f"Sigilos {len(j.sigilos)}/3", "ciano")
        linha = (f" Vida {ui.barra(j.hp, j.max_hp, 14)} {j.hp}/{j.max_hp}   {j.nome_recurso} {j.rec}/{j.max_rec}"
                 f"   Ouro {j.ouro}")
        if j.classe == "arqueiro":
            linha += f"   Flechas {j.flechas}"
        ui._imprimir(linha)
        if j.companheiro:
            c = j.companheiro
            ui._imprimir(f" {c['nome']} {ui.barra(c['hp'], c['max_hp'], 8, 'ciano')} {c['hp']}/{c['max_hp']}")
        males = sobrevivencia.descrever(j)
        ui.dizer(f" Provisões {j.provisoes}  Tochas {j.consumiveis.get('tocha', 0)}"
                 + (f"  |  {', '.join(males)}" if males else ""), "vermelho" if males else "cinza")
        ui.separador()

    def tela(self):
        if self.autosalvar:
            try:
                self.salvar(silencioso=True)
            except OSError:
                pass
        if self.periodo > 3:
            self.exausto()
        self.cabecalho()
        tipo = self.loc["tipo"]
        if tipo == "vila":
            self.menu_vila()
        else:
            self.menu_selvagem()

    def opcoes_comuns(self):
        pontos = self.j.pontos_talento
        return [
            ("Viajar", "viajar"),
            ("Talentos" + (f"  ★ {pontos} ponto(s) para gastar!" if pontos else ""), "talentos"),
            ("Personagem e inventário", "personagem"),
            (f"Comitiva ({len(self.comitiva)})" + ("  ✉ alguém quer conversar" if any(
                c["conversa"] for c in comitiva.estado(self)) else ""), "comitiva") if self.comitiva else None,
            ("Mapa", "mapa"),
            ("Diário (contratos, rumores, aliados)", "diario"),
            ("Bestiário", "bestiario"),
            ("Salvar jogo", "salvar"),
            ("Sair do jogo", "sair"),
        ]

    def executar_comum(self, op):
        acoes = {"viajar": self.viajar, "personagem": self.personagem, "comitiva": lambda: comitiva.menu(self), "talentos": self.menu_talentos, "bestiario": self.ver_bestiario, "mapa": self.mapa,
                 "diario": self.diario, "salvar": self.salvar, "sair": self.sair}
        acoes[op]()

    def menu_selvagem(self):
        loc = self.loc
        opcoes = []
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            opcoes.append((f"Enfrentar {loc['guardiao']['nome']} (guardião)", "chefe"))
        if loc["tipo"] == "cidadela":
            opcoes.append((f"Invadir o salão do trono e enfrentar {self.antagonista['curto']}", "final"))
        opcoes.append(("Explorar a região" + (" (à noite é mais perigoso)" if self.noite else ""), "explorar"))
        opcoes.append(("Acampar e descansar até o amanhecer", "acampar"))
        op = self.menu("O que você faz?", opcoes + self.opcoes_comuns())
        if op == "chefe":
            self.enfrentar_guardiao()
        elif op == "final":
            self.batalha_final()
        elif op == "explorar":
            self.explorar()
        elif op == "acampar":
            self.acampar()
        else:
            self.executar_comum(op)

    def menu_vila(self):
        j = self.j
        preco_dormir = self.preco(8 + 2 * j.nivel)
        faltando = j.max_hp - j.hp
        preco_templo = self.preco(max(1, faltando // 2)) if faltando else 0
        opcoes = [
            ("Passear pela vila", "passear"),
            (f"Taverna: dormir até amanhã ({preco_dormir} ouro)", "dormir"),
            (f"Taverna: pagar uma bebida e ouvir rumores ({self.preco(3)} ouro)", "rumores"),
            ("Mercado", "loja"),
            ("Mural de contratos", "mural"),
            (f"Templo: cuidar da vida ({preco_templo} ouro)", "templo") if faltando else None,
            ("Curandeiro: tratar ferimentos e infecções", "curandeiro") if j.ferimentos else None,
            ("Ferreiro: reforçar arma ou armadura", "ferreiro"),
        ]
        self.dizer(self.sortear(AMBIENTE_VILA), "cinza")
        op = self.menu(f"Você está em {self.loc['nome']}. O que faz?", opcoes + self.opcoes_comuns())
        if op == "passear":
            if not eventos.disparar(self, "vila"):
                self.dizer("A vila segue sua rotina. Nada de especial acontece.", "cinza")
            self.avancar_periodo()
            self.pausar()
        elif op == "dormir":
            self.dormir_taverna(preco_dormir)
        elif op == "rumores":
            self.ouvir_rumores()
        elif op == "loja":
            self.loja()
        elif op == "mural":
            self.mural()
        elif op == "curandeiro":
            self.curandeiro()
        elif op == "ferreiro":
            self.ferreiro()
        elif op == "templo":
            if self.j.ouro < preco_templo:
                self.dizer("Você não tem ouro suficiente.", "vermelho")
            else:
                self.perder_ouro(preco_templo)
                self.curar(faltando)
                self.dizer("Um clérigo trata suas feridas com unguentos e orações.", "verde")
        else:
            self.executar_comum(op)

    def ferreiro(self):
        j = self.j
        self.ui.cena("A forja", self.loc["nome"], "menu")
        while True:
            opcoes = []
            for slot, stat in (("arma", "poder" if j.classe == "mago" else "atk"), ("armadura", "defesa")):
                item = j.equip[slot]
                if not item:
                    continue
                ref = item.get("reforco", 0)
                if ref >= 5:
                    opcoes.append((f"{itens.rotulo(item)} — já está no limite (+5)", None))
                    continue
                custo = self.preco(int(40 * (ref + 1) ** 1.6))
                ganho = max(1, round(item["bonus"].get(stat, 0) * 0.12))
                opcoes.append((f"{itens.rotulo(item)} +{ref} → +{ref + 1}: +{ganho} {NOMES_STATS[stat]} — {custo} ouro",
                               (item, stat, ganho, custo)))
            esc = self.menu(f"O ferreiro, um homem sem dois dedos, cospe na forja. \"Ouro primeiro.\" "
                            f"(você tem {j.ouro})", opcoes + [("Voltar", "voltar")])
            if esc == "voltar":
                return
            if esc is None:
                continue
            item, stat, ganho, custo = esc
            if j.ouro < custo:
                self.dizer("\"Volta quando tiver o dinheiro.\"", "vermelho")
                continue
            self.perder_ouro(custo)
            item["bonus"][stat] = item["bonus"].get(stat, 0) + ganho
            item["reforco"] = item.get("reforco", 0) + 1
            item["nome"] = item["nome"].split(" +")[0] + f" +{item['reforco']}"
            j.recalcular()
            registrar(self, "ferreiro", item=item["nome"], stat=stat, ganho=ganho, custo=custo)
            self.dizer(f"Faíscas, marteladas, água fervendo. {item['nome']}: +{ganho} {NOMES_STATS[stat]}.", "verde")

    def curandeiro(self):
        j = self.j
        self.ui.cena("A curandeira", self.loc["nome"], "menu")
        while j.ferimentos:
            opcoes = []
            for f in j.ferimentos:
                d = sobrevivencia.FERIMENTOS[f["id"]]
                custo = self.preco((25 + 4 * j.nivel) if f["id"] == "infeccao" else (12 + 3 * j.nivel))
                opcoes.append((f"{d['nome']} — {custo} ouro", (f["id"], custo)))
            esc = self.menu("A curandeira, uma velha de mãos manchadas de sangue seco, examina você. "
                            "\"O que vai ser?\"", opcoes + [("Voltar", None)])
            if not esc:
                return
            fid, custo = esc
            if j.ouro < custo:
                self.dizer("\"Sem ouro, sem cura. Ninguém aqui faz caridade mais.\"", "vermelho")
                continue
            self.perder_ouro(custo)
            sobrevivencia.curar_ferimento(self, fid)
            self.dizer(f"Ela costura, cauteriza e enfaixa sem anestesia. Você grita. "
                       f"{sobrevivencia.FERIMENTOS[fid]['nome']}: tratado.", "verde")

    def preco(self, base):
        fator = 1 - self.j.reputacao / 200
        return max(1, int(round(base * fator)))

    def exausto(self):
        self.ui.separador()
        if self.loc["tipo"] == "vila":
            self.dizer("Exausto, você pede abrigo num estábulo e dorme sobre o feno, entre ratos.", "cinza")
            self.descansar(0.15, mana=0.4)
            self.novo_dia(descanso=1)
        else:
            self.dizer("Você está exausto demais para continuar. É preciso acampar.", "cinza")
            self.acampar()

    # ================================================================ ações no mundo
    def explorar(self):
        self.ui.cena("Explorando", self.contexto_cena(), "evento")
        self.narrar(self.ambiente(), "cinza")
        sobrevivencia.acender_tocha(self)
        try:
            if not eventos.disparar(self, "explorar"):
                self.dizer("Você vasculha a área, mas não encontra nada digno de nota.", "cinza")
        finally:
            self.sem_luz = False
        self.avancar_periodo()
        self.pausar()

    def acampar(self):
        self.ui.cena("Acampamento", self.contexto_cena(), "evento")
        self.dizer("Você junta gravetos, acende uma fogueira fraca e se enrola na capa. O frio entra mesmo assim.",
                   "cinza")
        if not comitiva.noite(self) and self.chance(0.45):
            eventos.disparar(self, "acampamento")
        fracao = 0.4
        if self.clima in ("chuva", "tempestade", "neve"):
            fracao = 0.25
            self.dizer("Você dorme encharcado e tremendo. Quase não descansa.", "vermelho")
        self.descansar(fracao, mana=0.5)
        self.novo_dia(descanso=1)
        self.pausar()

    def dormir_taverna(self, preco):
        if self.j.ouro < preco:
            self.dizer("Sem ouro suficiente. O taverneiro aponta para a porta.", "vermelho")
            return
        self.ui.cena("A taverna", self.contexto_cena(), "evento")
        self.perder_ouro(preco)
        self.dizer("Uma cama de palha sem pulgas demais e um ensopado ralo. É o melhor que este mundo oferece.",
                   "verde")
        if self.j.provisoes < sobrevivencia.MAX_PROVISOES:
            self.j.provisoes += 1  # a refeição da taverna conta como o dia de comida
        self.descansar(0.8)
        self.novo_dia(descanso=2)
        self.pausar()

    def viajar(self):
        self.ui.cena("Viagem", self.contexto_cena(), "menu")
        self.desenhar_mapa()
        opcoes = []
        for loc, dist in sorted(vizinhos(self.mundo, self.loc), key=lambda v: v[0]["id"]):
            web = getattr(self.ui, "web", False)  # na web, o mapa é clicável e desenha os próprios ícones
            numero = "" if web else f"[{loc['id'] + 1}] {mapa.glifo(self, loc)} "
            texto = f"{numero}{loc['nome']} — {mapa.descricao(self, loc)}"
            if loc["tipo"] != "vila":
                nv = nivel_regiao(loc, self.corrupcao)
                texto += f" · Nv.{nv}"
                if nv >= self.j.nivel + 2:
                    texto += " (PERIGOSO!)"
            texto += f" · {dist} trecho{'s' if dist > 1 else ''}"
            if not loc["visitado"]:
                texto += " · inexplorado"
            opcoes.append((texto, (loc, dist), {"local": loc["id"]}))
        opcoes.append(("Voltar", None))
        destino = self.menu("Para onde?", opcoes)
        if not destino:
            return
        loc, dist = destino
        nv = nivel_regiao(loc, self.corrupcao)
        if loc["tipo"] != "vila" and nv >= self.j.nivel + 3:
            if not self.menu(f"{loc['nome']} tem inimigos de nível {nv}. Você é nível {self.j.nivel}. "
                             f"Lá, quase qualquer encontro pode te matar. Ir mesmo assim?",
                             [("Não, voltar", False), ("Sim, eu sei o que estou fazendo", True)]):
                return
        if loc["tipo"] == "cidadela" and len(self.j.sigilos) < 3:
            self.dizer(f"Uma muralha de sombras bloqueia o caminho. Você precisa dos três Sigilos "
                       f"({len(self.j.sigilos)}/3).", "magenta")
            return
        for trecho in range(dist):
            if self.periodo > 3:
                self.dizer("A noite está avançada demais para seguir viagem.", "cinza")
                self.acampar()
            if trecho >= dist / 2:
                self.mundo["atual"] = loc["id"]
            self.ui.cena(f"Rumo a {loc['nome']}", f"trecho {trecho + 1} de {dist} · {self.contexto_cena()}", "evento")
            sobrevivencia.acender_tocha(self)
            try:
                if self.chance(0.65):
                    eventos.disparar(self, "viagem")
                else:
                    self.dizer(self.ambiente() + " A viagem segue sem incidentes.", "cinza")
            finally:
                self.sem_luz = False
            self.avancar_periodo()
        self.chegar(loc)

    def chegar(self, loc):
        self.mundo["atual"] = loc["id"]
        registrar(self, "chegada", local=loc["nome"], tipo_local=loc["tipo"], nivel_regiao=self.nivel_local(),
                  primeira=not loc["visitado"])
        primeira = not loc["visitado"]
        loc["visitado"] = True
        if self.chance(0.5):
            self.rolar_clima()
        self.ui.separador()
        self.dizer(f"Você chega a {loc['nome']}.", "amarelo+negrito")
        if primeira and loc["tipo"] != "vila":
            self.dizer(self.ambiente(), "cinza")
        if loc["tipo"] == "covil" and not loc["guardiao"]["derrotado"]:
            g = loc["guardiao"]
            self.dizer(f"Este é o covil de {g['nome']} (Nv.{self.nivel_guardiao(loc)}). Um dos Sigilos está aqui.",
                       "magenta")
        if loc["tipo"] != "vila" and self.nivel_local() >= self.j.nivel + 3:
            self.dizer("Um arrepio sobe pela espinha. As criaturas daqui são muito mais fortes do que você.",
                       "vermelho+negrito")
        if loc["tipo"] == "cidadela":
            self.dizer(f"Os três Sigilos ardem em sua mão e a muralha de sombras se abre. "
                       f"{tx.maiuscula(self.antagonista['curto'])} sabe que você chegou.", "magenta+negrito")
        if loc["tipo"] == "vila":
            self.receber_contratos()
            if self.chance(0.35):
                eventos.disparar(self, "vila")
        self.pausar()

    # ================================================================ vila: rumores, loja, mural
    def ouvir_rumores(self):
        chave = f"rumores:{self.dia}:{self.loc['id']}"
        if self.flag(chave, 0) >= 2:
            self.dizer("Os fregueses já contaram tudo o que sabiam hoje.", "cinza")
            return
        preco = self.preco(3)
        if self.j.ouro < preco:
            self.dizer("Sem ouro nem para uma caneca.", "vermelho")
            return
        self.perder_ouro(preco)
        self.marcar(chave, self.flag(chave, 0) + 1)
        ouvir_rumor(self)

    def estoque(self):
        chave = f"{self.loc['id']}:{self.dia // 3}"
        if chave not in self.lojas:
            prefixo = f"{self.loc['id']}:"
            self.lojas = {k: v for k, v in self.lojas.items() if not k.startswith(prefixo)}
            estoque = [gerar_equip(self.rng, self.j.classe, self.j.nivel + self.rng.choice([-1, 0, 0, 1]), qualidade=-1)
                       for _ in range(4)]
            self.lojas[chave] = estoque
        return self.lojas[chave]

    def loja(self):
        while True:
            j = self.j
            self.ui.cena("Mercado", f"{self.loc['nome']} · seu ouro: {j.ouro}", "menu")
            a_venda = self.estoque()
            opcoes = []
            for k in ("tocha", "bandagem", "unguento", "pocao_vida", "tonico", "antidoto", "bomba_fumaca",
                      "pena_fenix"):
                c = CONSUMIVEIS[k]
                opcoes.append((f"{c['nome']} — {self.preco(c['preco'])} ouro (você tem {j.consumiveis.get(k, 0)})",
                               ("consumivel", k)))
            opcoes.append((f"Provisões para 1 dia — {self.preco(4)} ouro (você tem {j.provisoes}/"
                           f"{sobrevivencia.MAX_PROVISOES})", ("provisoes",)))
            if j.classe == "arqueiro":
                opcoes.append((f"Feixe de 10 flechas — {self.preco(10)} ouro (você tem {j.flechas})", ("flechas",)))
            for it in a_venda:
                opcoes.append((f"{itens.rotulo(it)} [{NOMES_SLOT[it['slot']]}] {descrever_bonus(it['bonus'])} — "
                               f"{self.preco(it['preco'])} ouro", ("equip", it)))
            if j.mochila:
                opcoes.append(("Vender itens da mochila", ("vender",)))
            opcoes.append(("Sair do mercado", None))
            op = self.menu("Comprar o quê?", [(o[0].replace("Sair do mercado", "Voltar"), o[1]) for o in opcoes])
            if op is None:
                return
            if op[0] == "vender":
                self.vender()
                continue
            preco = self.preco({"consumivel": lambda: CONSUMIVEIS[op[1]]["preco"], "flechas": lambda: 10,
                                "provisoes": lambda: 4, "equip": lambda: op[1]["preco"]}[op[0]]())
            if op[0] == "provisoes" and j.provisoes >= sobrevivencia.MAX_PROVISOES:
                self.dizer("Você não consegue carregar mais comida.", "vermelho")
                continue
            if j.ouro < preco:
                self.dizer("Ouro insuficiente.", "vermelho")
                continue
            if op[0] == "equip" and len(j.mochila) >= LIMITE_MOCHILA:
                self.dizer("Sua mochila está cheia.", "vermelho")
                continue
            self.perder_ouro(preco)
            if op[0] == "consumivel":
                self.dar(op[1])
            elif op[0] == "flechas":
                self.dar_flechas(10)
            elif op[0] == "provisoes":
                j.provisoes += 1
                self.dizer(f"Pão duro, carne seca e um odre de água. (provisões: {j.provisoes})", "verde")
            else:
                a_venda.remove(op[1])
                self.oferecer_equip_comprado(op[1])

    def oferecer_equip_comprado(self, item):
        if self.menu(f"Equipar {item['nome']} agora?", [("Sim", True), ("Não, guardar na mochila", False)]):
            self.equipar(item)
        else:
            self.j.mochila.append(item)

    def vender(self):
        j = self.j
        opcoes = [(f"{it['nome']} — {descrever_bonus(it['bonus'])} — vende por {it['preco'] // 2}", it)
                  for it in j.mochila]
        it = self.menu("Vender o quê?", opcoes + [("Voltar", None)])
        if it:
            j.mochila.remove(it)
            self.ganhar_ouro(it["preco"] // 2)

    def gerar_contrato(self):
        j = self.j
        selvagens = [l for l in self.mundo["locais"] if l["tipo"] in ("selvagem", "covil")]
        vilas = [l for l in self.mundo["locais"] if l["tipo"] == "vila" and l["id"] != self.loc["id"]]
        tipo = self.sortear(["caca", "caca", "alvo", "alvo", "entrega"])
        cid = self.novo_id()
        ouro = int((18 + 8 * j.nivel) * self.rng.uniform(0.9, 1.3))
        xp = 20 + 12 * j.nivel
        if tipo == "entrega" and vilas:
            dest = self.sortear(vilas)
            objeto = self.sortear(["um baú lacrado", "uma carta com selo de cera negra", "um frasco de remédio",
                                   "um embrulho que se mexe às vezes", "as escrituras de uma fazenda",
                                   "um anel de noivado"])
            return {"id": cid, "tipo": "entrega", "destino": dest["id"], "objeto": objeto, "ouro": ouro, "xp": xp,
                    "desc": f"Levar {objeto} até {dest['nome']}."}
        loc = self.sortear(selvagens)
        fam = self.sortear(BIOMAS[loc["bioma"]]["familias"])
        f = FAMILIAS[fam]
        if tipo == "alvo":
            nome = tx.nome_proprio(self.rng)
            return {"id": cid, "tipo": "alvo", "local": loc["id"], "familia": fam, "nome": nome,
                    "chave": f"alvo:{cid}", "ouro": int(ouro * 1.5), "xp": int(xp * 1.5),
                    "desc": f"Caçar {nome}, {tx.artigo(f['g'], False)} {f['nome']} enorme que aterroriza "
                            f"{loc['nome']}."}
        total = self.rng.randint(2, 4)
        return {"id": cid, "tipo": "caca", "local": loc["id"], "familia": fam, "total": total, "feito": 0,
                "ouro": ouro, "xp": xp, "desc": f"Eliminar {total} {f['plural']} em {loc['nome']}."}

    def mural(self):
        vid = str(self.loc["id"])
        oferta = self.ofertas.get(vid)
        if not oferta or self.dia - oferta["dia"] >= 3:
            oferta = {"dia": self.dia, "lista": [self.gerar_contrato() for _ in range(3)]}
            self.ofertas[vid] = oferta
        while True:
            self.ui.cena("Mural de contratos", f"{self.loc['nome']} · contratos ativos: {len(self.contratos)}/3", "menu")
            opcoes = [(f"{c['desc']} (recompensa: {c['ouro']} ouro, {c['xp']} XP)", c) for c in oferta["lista"]]
            c = self.menu("Aceitar qual contrato?", opcoes + [("Voltar", None)])
            if not c:
                return
            if len(self.contratos) >= 3:
                self.dizer("Você já tem contratos demais.", "vermelho")
                continue
            oferta["lista"].remove(c)
            self.contratos.append(c)
            self.dizer("Contrato aceito.", "verde")
            if c["tipo"] == "alvo":
                self.marcar(f"conhecido:{c['local']}")
            if c["tipo"] == "entrega":
                self.plantar("pacote_suspeito", 3, contrato=c["id"])

    def receber_contratos(self):
        for c in list(self.contratos):
            entregue = c["tipo"] == "entrega" and c["destino"] == self.loc["id"]
            if entregue or c.get("concluido"):
                self.contratos.remove(c)
                self.dizer(f"Recompensa de contrato: {c['desc']}", "verde+negrito")
                self.ganhar_ouro(c["ouro"])
                self.mudar_reputacao(3)
                self.ganhar_xp(c["xp"])

    def contrato_alvo_aqui(self):
        for c in self.contratos:
            if c["tipo"] == "alvo" and c["local"] == self.loc["id"] and not c.get("concluido"):
                return c
        return None

    # ================================================================ telas de informação
    def personagem(self):
        while True:
            j = self.j
            self.ui.cena(j.nome, f"{j.nome_classe} nível {j.nivel}", "menu")
            if not self.ui.painel("personagem", {}):
                self._personagem_texto()
            op = self.menu("", [
                ("Usar item da bolsa", "usar"),
                ("Equipar item da mochila", "equipar") if j.mochila else None,
                ("Voltar", None),
            ])
            if op is None:
                return
            if op == "usar":
                usaveis = [k for k in ("bandagem", "unguento", "pocao_vida", "tonico", "antidoto") if j.tem(k)]
                k = self.menu("Usar:", [(CONSUMIVEIS[k]["nome"], k, {"item": k}) for k in usaveis] + [("Voltar", None)])
                if k:
                    self.usar_consumivel(k)
            else:
                it = self.menu("Equipar:", [(f"{it['nome']} [{NOMES_SLOT[it['slot']]}] "
                                             f"{descrever_bonus(it['bonus'])}", it, {"mochila": i})
                                            for i, it in enumerate(j.mochila)] + [("Voltar", None)])
                if it:
                    if it["classe"] and it["classe"] != j.classe:
                        self.dizer("Você não sabe usar isso.", "vermelho")
                    else:
                        self.equipar(it)

    def _personagem_texto(self):
        j = self.j
        self.dizer(f"Vida {j.hp}/{j.max_hp}   {j.nome_recurso} {j.rec}/{j.max_rec}   Ataque {j.atk}   "
                   f"Defesa {j.defesa}   Agilidade {j.agi}   Poder {j.poder}")
        self.dizer(f"Provisões: {j.provisoes} dia(s)   Tochas: {j.consumiveis.get('tocha', 0)}", "amarelo")
        males = sobrevivencia.descrever(j)
        self.dizer("Condição: " + (", ".join(males) if males else "sem ferimentos"),
                   "vermelho" if males else "verde")
        self.dizer(f"Reputação: {j.reputacao:+d}   Ouro: {j.ouro}" +
                   (f"   Flechas: {j.flechas}" if j.classe == "arqueiro" else ""))
        self.dizer("Equipamento:", "ciano")
        for slot, it in j.equip.items():
            self.dizer(f"  {NOMES_SLOT[slot]}: " + (f"{itens.rotulo(it)} ({descrever_bonus(it['bonus'])})" if it
                                                    else "—"), itens.cor(it) if it else None)
        self.dizer("Habilidades: " + ", ".join(HABILIDADES[h]["nome"] for h in j.habilidades), "ciano")
        cons = [f"{CONSUMIVEIS[k]['nome']} x{v}" for k, v in j.consumiveis.items() if v > 0]
        self.dizer("Bolsa: " + (", ".join(cons) if cons else "vazia"), "ciano")
        if j.mochila:
            self.dizer(f"Mochila ({len(j.mochila)}/{LIMITE_MOCHILA}): " +
                       ", ".join(it["nome"] for it in j.mochila), "ciano")
        if j.companheiro:
            c = j.companheiro
            self.dizer(f"Companheiro: {c['nome']} — vida {c['hp']}/{c['max_hp']}, ataque {int(c['atk'])}", "ciano")

    def mapa(self):
        self.ui.cena("Mapa do reino", self.contexto_cena(), "menu")
        if self.desenhar_mapa(grande=True):
            self.pausar()
            return
        self.dizer(mapa.SIMBOLOS, "cinza")
        self.ui.separador()
        for rotulo, texto, cor in mapa.legenda(self):
            self.dizer(f"{rotulo:>2}  {texto}", cor)
        self.pausar()

    def desenhar_mapa(self, grande=False):
        """A interface web desenha o próprio mapa (em SVG); as de terminal, em caracteres."""
        if getattr(self.ui, "web", False):
            self.ui.mostrar_mapa(grande)
            return True
        self.ui.desenhar(mapa.renderizar(self))
        return False

    def diario(self):
        self.ui.cena("Diário", f"dia {self.dia}", "menu")
        a = self.antagonista
        n = self.nemesis
        dados = {
            "antagonista": {"nome": a["nome"], "origem": a["origem"]}, "sigilos": len(self.j.sigilos),
            "corrupcao": self.corrupcao, "dia": self.dia,
            "contratos": [{"desc": c["desc"], "tipo": c["tipo"], "concluido": bool(c.get("concluido")),
                           "progresso": f"{c['feito']}/{c['total']}" if c["tipo"] == "caca" else None,
                           "ouro": c.get("ouro")} for c in self.contratos],
            "rumores": [{"texto": r["texto"], "expira": r["expira"] - self.dia} for r in self.rumores],
            "nemesis": {"nome": n["nome"], "familia": FAMILIAS[n["familia"]]["nome"]} if n else None,
            "aliados": [{"nome": x["nome"], "texto": x["texto"]} for x in self.aliados_finais],
        }
        if not self.ui.painel("diario", dados):
            self._diario_texto(a)
        pendentes = [c for c in self.contratos if not c.get("concluido")]
        if pendentes:
            c = self.menu("", [("Fechar o diário", None)] +
                          [(f"Abandonar: {c['desc']}", c) for c in pendentes])
            if c:
                self.abandonar_contrato(c)
        else:
            self.pausar()

    def _diario_texto(self, a):
        self.dizer(f"Inimigo final: {a['nome']}, {a['origem']}.", "magenta")
        self.dizer(f"Sigilos: {len(self.j.sigilos)}/3   Corrupção: {self.corrupcao}%   Dia {self.dia}", "magenta")
        self.dizer("Contratos:", "ciano")
        if not self.contratos:
            self.dizer("  nenhum", "cinza")
        for c in self.contratos:
            prog = f" ({c['feito']}/{c['total']})" if c["tipo"] == "caca" else ""
            estado = " — CONCLUÍDO, receba numa vila" if c.get("concluido") else ""
            self.dizer(f"  • {c['desc']}{prog}{estado}")
        self.dizer("Rumores:", "ciano")
        if not self.rumores:
            self.dizer("  nenhum", "cinza")
        for r in self.rumores:
            self.dizer(f"  • {r['texto']}")
        if self.nemesis:
            n = self.nemesis
            self.dizer(f"Nêmesis: {n['nome']}, {FAMILIAS[n['familia']]['nome']} que te persegue.", "vermelho")
        if self.aliados_finais:
            self.dizer("Aliados para a batalha final: " + ", ".join(x["nome"] for x in self.aliados_finais), "verde")

    def abandonar_contrato(self, c):
        penalidade = 6 if c["tipo"] == "entrega" else 3
        aviso = " Você fica com a encomenda, mas vira ladrão aos olhos de todos." if c["tipo"] == "entrega" else ""
        if not self.menu(f"Abandonar \"{c['desc']}\"? (reputação -{penalidade}){aviso}",
                         [("Sim, abandonar", True), ("Não", False)]):
            return
        self.contratos.remove(c)
        self.dizer("Você risca o contrato do diário. Alguém, em algum lugar, vai saber que você desistiu.", "cinza")
        self.mudar_reputacao(-penalidade)

    # ================================================================ chefes
    def nivel_guardiao(self, loc):
        return nivel_regiao(loc, self.corrupcao) + 1

    def enfrentar_guardiao(self):
        loc = self.loc
        gspec = loc["guardiao"]
        t = GUARDIOES[gspec["bioma"]][gspec["idx"]]
        self.ui.cena(gspec["nome"], f"guardião · {loc['nome']}", "chefe")
        self.narrar(t["intro"], "vermelho")
        chave = f"guardiao:{loc['id']}"
        if self.flag(f"fraqueza:{chave}"):
            self.dizer("Você se lembra do que ouviu sobre o ponto fraco desta criatura.", "verde")
        if not self.menu("Não haverá como fugir depois de começar.", [("Lutar!", True), ("Recuar por enquanto",
                                                                                         False)]):
            return
        nivel = self.nivel_guardiao(loc)
        chefe = instanciar_guardiao(gspec, nivel)
        chefe.chave = chave
        r = self.combate([chefe], pode_fugir=False, titulo=f"GUARDIÃO: {gspec['nome']}")
        if r == "vitoria":
            gspec["derrotado"] = True
            self.j.sigilos.append(loc["bioma"])
            self.estatisticas["chefes"] += 1
            self.ui.titulo(f"SIGILO OBTIDO ({len(self.j.sigilos)}/3)", "amarelo+negrito")
            self.dizer("Uma runa ardente se grava na palma da sua mão.", "amarelo")
            self.corromper(-15)
            self.mudar_reputacao(5)
            self.ganhar_ponto_talento()
            self.ui.celebrar("sigilo", {"sigilos": len(self.j.sigilos), "guardiao": gspec["nome"],
                                        "pontos": self.j.pontos_talento})
            if len(self.j.sigilos) >= 3:
                self.dizer(f"Os três Sigilos pulsam juntos. O caminho para {self.mundo['locais'][-1]['nome']} "
                           f"está aberto!", "magenta+negrito")
        self.avancar_periodo()
        self.pausar()

    def batalha_final(self):
        a = self.antagonista
        j = self.j
        self.ui.cena(a["nome"], "o salão do trono", "chefe")
        falas = {
            "guerreiro": "Tanto aço, tanta coragem. Eu também empunhei uma espada, um dia.",
            "arqueiro": "Você mira bem. Mas como se acerta o que não tem coração?",
            "mago": "Você sente, não sente? O poder do Vazio chamando por você. Somos iguais.",
        }
        self.narrar(f"No topo da escadaria, {a['curto']} te espera num trono de pedra rachada.", "magenta")
        self.narrar(f"\"{j.nome}. {falas[j.classe]}\"", "magenta+negrito")
        if j.reputacao <= -20:
            self.narrar("\"E que reputação a sua! Matou, roubou, mentiu. Junte-se a mim — você já está no "
                        "meio do caminho.\"", "magenta")
        if j.reputacao >= 20:
            self.narrar("\"Herói do povo, é? Vamos ver se as preces deles te salvam.\"", "magenta")
        self.pausar()

        guarda = self.inimigo("cavaleiro_sombrio", nome_unico=tx.nome_proprio(self.rng),
                             nivel=self.nivel_local() + 1)
        self.dizer("Um cavaleiro de armadura negra se coloca entre vocês.", "vermelho")
        self.combate([guarda], pode_fugir=False, titulo="O ÚLTIMO GUARDA")

        chefe = instanciar_antagonista(a, 11 + self.corrupcao // 34, self.corrupcao)
        traidores = comitiva.antes_da_batalha_final(self)
        extras = []
        if "yara" in traidores:
            yara = self.inimigo("bruxa_brejo", nome_unico="Yara", nivel=chefe.nivel - 1)
            yara.nome = "Yara, Voz da Fenda"
            yara.max_hp = yara.hp = int(yara.max_hp * 1.6)
            yara.poder = int(yara.poder * 1.4)
            extras.append(yara)
        if self.aliados_finais:
            self.ui.separador("verde")
            self.dizer("Mas você não está só.", "verde+negrito")
            dano_max = int(chefe.max_hp * 0.45)  # os aliados ajudam, mas o golpe final é seu
            for al in self.aliados_finais:
                self.narrar(al["texto"], "verde")
                if al["efeito"] == "dano":
                    perda = min(int(chefe.max_hp * al["valor"]), dano_max - (chefe.max_hp - chefe.hp))
                    if perda > 0:
                        chefe.hp -= perda
                        self.dizer(f"  ({a['curto']} perde {perda} de vida)", "verde")
                elif al["efeito"] == "cura":
                    j.hp = j.max_hp
                    self.dizer("  (vida restaurada)", "verde")
                elif al["efeito"] == "forca":
                    atual = j.efeito("fortalecido")
                    bonus = min(0.3, (atual["v"] if atual else 0) + 0.1)
                    j.aplicar("fortalecido", 99, bonus)
                    j.efeitos["fortalecido"]["v"] = bonus
                    self.dizer(f"  (seu dano aumenta em {int(bonus * 100)}% nesta batalha)", "verde")
            self.pausar()
        j.hp = max(j.hp, j.max_hp // 2)
        self.combate([chefe] + extras, pode_fugir=False, titulo="O FIM DE TODAS AS COISAS")
        self.vitoria()

    # ================================================================ finais
    def resumo(self):
        e = self.estatisticas
        j = self.j
        self.dizer(f"{j.nome}, {j.nome_classe} nível {j.nivel} — {self.dia} dias de jornada.", "ciano")
        self.dizer(f"Inimigos derrotados: {e['abates']}  ·  Guardiões: {e['chefes']}  ·  "
                   f"Eventos vividos: {e['eventos']}  ·  Ouro ganho: {e['ouro_ganho']}  ·  "
                   f"Quedas: {e.get('quedas', 0)}", "ciano")
        self.dizer(f"Semente do mundo: {self.seed} (use --seed para jogar o mesmo reino de novo)", "cinza")
        caminho = telemetria.exportar(self)
        if caminho:
            self.dizer(f"Registro da partida salvo em: {caminho} (e o .jsonl ao lado). "
                       f"Mande esses arquivos para análise de equilíbrio.", "ciano")

    def fim_de_jogo(self, motivo):
        self.registrar_legado("corrupcao" if self.corrupcao >= 100 else "morte", motivo)
        self.estatisticas["causa"] = motivo
        registrar(self, "fim", resultado="corrupcao" if self.corrupcao >= 100 else "morte", causa=motivo,
                  corrupcao=self.corrupcao)
        if self.hardcore:  # morte permanente de verdade: o save vai junto
            try:
                os.remove(self.caminho_save())
            except OSError:
                pass
        self.ui.cena("Você morreu" if self.corrupcao < 100 else "O reino caiu", f"dia {self.dia}", "morte")
        self.narrar(motivo, "vermelho")
        epitafio = self.sortear([
            "Ninguém veio buscar o corpo. Os lobos vieram.",
            "Seu nome será esquecido antes do próximo inverno.",
            "Em alguma taverna, alguém pergunta por você. Ninguém sabe responder.",
            "O próximo a tentar encontrará seus ossos — e talvez aprenda com eles.",
        ])
        self.narrar(epitafio, "cinza")
        self.resumo()
        self.pausar()
        raise FimDeJogo()

    def vitoria(self):
        j = self.j
        a = self.antagonista
        self.registrar_legado("vitoria", f"derrotou {a['nome']}")
        self.estatisticas["venceu"] = True
        registrar(self, "fim", resultado="vitoria", causa=f"derrotou {a['nome']}", corrupcao=self.corrupcao)
        self.ui.cena("Vitória", f"dia {self.dia}", "vitoria")
        self.narrar(f"{tx.maiuscula(a['curto'])} se desfaz como cinza ao vento. A Fenda se fecha com um "
                    f"suspiro que ecoa por todo o reino.", "amarelo")
        epilogos = {
            "paladino": "Os templos acendem velas em seu nome. Você se torna o escudo do reino.",
            "berserker": "Bardos cantam sobre a fúria que nem o Vazio conseguiu conter.",
            "patrulheiro": "Você volta às matas, onde cada árvore parece saudar seu retorno.",
            "sombra": "Ninguém sabe ao certo quem salvou o reino. É exatamente como você prefere.",
            "piromante": "Por anos, o céu sobre a Fenda brilha em tons de brasa. Sua marca.",
            "necromante": "Os vivos te temem, os mortos te agradecem. Você aprendeu a conviver com os dois.",
        }
        self.narrar(epilogos.get(j.spec, "Você volta para casa, mais velho do que os dias de viagem explicam."))
        if j.reputacao >= 20:
            self.narrar("Em cada vila por onde passa, crianças brincam de ser você.")
        elif j.reputacao <= -20:
            self.narrar("O reino está salvo, mas as portas se fecham quando você passa. Heróis nem sempre são amados.")
        if self.corrupcao >= 70:
            self.narrar("A vitória veio tarde: cicatrizes do Vazio marcarão estas terras por gerações.")
        elif self.corrupcao <= 25:
            self.narrar("A vitória veio a tempo: em poucas estações, nem parece que a sombra esteve aqui.")
        self.resumo()
        self.pausar()
        raise FimDeJogo()

    # ================================================================ salvar / carregar
    def sair(self):
        op = self.menu("Sair do jogo?", [("Salvar e sair", "salvar"), ("Sair sem salvar", "sair"),
                                         ("Cancelar", None)])
        if op is None:
            return
        if op == "salvar":
            self.salvar()
        else:
            caminho = telemetria.exportar(self)
            if caminho:
                self.dizer(f"Registro parcial da partida: {caminho}", "cinza")
        raise FimDeJogo()

    def caminho_save(self):
        slug = re.sub(r"[^a-z0-9]+", "_", self.j.nome.lower()).strip("_") or "heroi"
        return os.path.join(self.pasta_saves, f"{slug}.json")

    def salvar(self, silencioso=False):
        os.makedirs(self.pasta_saves, exist_ok=True)
        estado = self.rng.getstate()
        dados = {
            "versao": VERSAO_SAVE,
            "seed": self.seed,
            "rng": [estado[0], list(estado[1]), estado[2]],
            "jogador": self.j.para_dict(),
        }
        for campo in ("mundo", "dia", "periodo", "clima", "corrupcao", "passos", "flags", "historico", "contagem",
                      "impulsos", "sementes", "rumores", "contratos", "ofertas", "lojas", "nemesis",
                      "aliados_finais", "forcados", "proximo_id", "estatisticas", "hardcore", "bestiario", "lendas",
                      "registro", "arquivo_run", "comitiva"):
            dados[campo] = getattr(self, campo)
        caminho = self.caminho_save()
        temporario = caminho + ".tmp"
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        os.replace(temporario, caminho)  # nunca deixa um save pela metade
        if silencioso:
            return
        self.dizer(f"Jogo salvo em {caminho}.", "verde")
        registro = telemetria.exportar(self)
        if registro:
            self.dizer(f"Registro parcial da partida: {registro}", "cinza")

    @classmethod
    def carregar(cls, ui, caminho, pasta_saves="saves"):
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        g = cls(ui, dados["seed"], pasta_saves)
        r = dados.pop("rng")
        g.rng.setstate((r[0], tuple(r[1]), r[2]))
        g.j = Jogador.de_dict(dados.pop("jogador"))
        dados.pop("versao", None)
        dados.pop("seed", None)
        for campo, valor in dados.items():
            setattr(g, campo, valor)
        # Saves da versão anterior não tinham coordenadas no mapa.
        for loc in g.mundo["locais"]:
            loc.setdefault("x", 0.03 + 0.9 * (loc["perigo"] - 1) / 4 if loc["id"] else 0.03)
            loc.setdefault("y", 0.08 + 0.84 * ((loc["id"] * 5) % 11) / 10)
        return g
