"""As regras da segunda versão do protótipo de combate e atributos (26/10/2026; nada no jogo). A primeira (motor/) fica
congelada para comparar; esta parte dela e muda o que a revisão da seção 3.7 do 25 pediu.

Os relógios (dois nomes, nunca "turno" para os dois):
- **turno**: a vez de um combatente. Começa (recupera 8 do recurso; expira o que dura "até o início do próximo turno"
  dele; o sangramento pinga), e então ele age, perde a vez (atordoado, aterrorizado) ou é pulado (caído, ainda não
  entrou).
- **rodada**: a ordem inteira, uma vez cada um, inclusive quem perdeu a vez. No fim dela expira o que dura "até o fim
  da rodada N".

Os marcos de cada estado:
- Defendendo, Protegido/Protegendo, Desafiando, Juramento: até o início do próximo turno de quem os pôs;
- Atordoado, Aterrorizado: a próxima vez do portador é perdida (gastos ao começar o turno dele);
- Escudo de Luz, Marcado, Comandado: até o fim da rodada seguinte à aplicação (ou gastos antes, no golpe);
- Sangrando: pinga no início de cada turno do portador, 2 vezes.

Os atributos (provisórios, graduais, sem desbloqueio por pontuação; tetos de segurança só):
- Força: + a potência física, ponto a ponto. Intelecto: + a potência sobrenatural, ponto a ponto.
- Percepção: crítico (2% por ponto, até 25%) e ponto fraco (+4% de dano por ponto contra quem tem um, até +40%).
- Constituição: vida (4 por ponto) e resistência corporal (−4% do sangramento por ponto, até −40%).
- Vontade: Tenacidade (4% por ponto, até 40%) = a chance de resistir a controle. A chance final é a Tenacidade do alvo
  menos a aplicação de quem controla, nunca abaixo de 0; conta uma vez só, no sorteio do controle. Não reduz duração
  nem dano.
- Agilidade: a ordem inicial, calculada uma vez. Presença: nenhum efeito na luta.

Queda e retorno: um aliado a 0 de vida fica caído (pulado na ordem; não morre). Volta só por Reerguer ou pela Pena de
Fênix, na mesma posição: se a vez dele nesta rodada ainda não passou, age nela; se já passou (pulada), só na próxima.
Ninguém recupera a vez perdida. Hipótese operacional (não decisão): o protagonista caído encerra a luta em derrota.

Invocações (hipótese operacional): entram no fim da ordem e agem a partir da rodada seguinte, sem mexer na posição de
ninguém."""
import random

from . import conteudo as C

CRITICO_POR_PONTO, CRITICO_TETO, CRITICO_MULT = 0.02, 0.25, 1.5
PONTO_FRACO_POR_PONTO, PONTO_FRACO_TETO = 0.04, 0.40
VIDA_POR_PONTO, VIDA_POR_NIVEL = 4, 6
CORPORAL_POR_PONTO, CORPORAL_TETO = 0.04, 0.40
TENACIDADE_POR_PONTO, TENACIDADE_TETO = 0.04, 0.40
DEFESA = 0.40
DESAFIO = 0.25
JURAMENTO = 0.50
GUARDA_MULT = 0.5


def pct(x):
    return f"{round(x * 100)}%"


def validar_atributos(atr):
    if set(atr) != set(C.ATRIBUTOS):
        return "Faltam atributos."
    if any(not (C.ATRIBUTO_MIN <= v <= C.ATRIBUTO_MAX) for v in atr.values()):
        return f"Cada atributo vai de {C.ATRIBUTO_MIN} a {C.ATRIBUTO_MAX}."
    if sum(atr.values()) != C.ORCAMENTO:
        return f"A soma tem de ser {C.ORCAMENTO} (está {sum(atr.values())})."
    return None


def pontos_kit(kit):
    return sum(C.PONTOS_TIER[C.HABILIDADES[h]["tier"]] for h in kit)


def validar_kit(kit):
    """None se o kit cabe: só habilidades de escolher, sem repetir, até 10 pontos, 6 espaços e uma ultimate."""
    if any(h not in C.HABILIDADES or "tier" not in C.HABILIDADES[h] for h in kit):
        return "Só habilidades do protagonista (Atacar, Defender e os itens já vêm fora do kit)."
    if len(set(kit)) != len(kit):
        return "Habilidade repetida."
    if len(kit) > C.KIT_ESPACOS:
        return f"No máximo {C.KIT_ESPACOS} habilidades."
    if sum(C.HABILIDADES[h]["tier"] == "ultimate" for h in kit) > 1:
        return "No máximo uma ultimate."
    if pontos_kit(kit) > C.KIT_PONTOS:
        return f"O kit custa {pontos_kit(kit)} pontos; o orçamento é {C.KIT_PONTOS}."
    return None


# ---------------------------------------------------------------- as fórmulas (provisórias)
def critico(atr):
    return min(CRITICO_TETO, CRITICO_POR_PONTO * atr["percepcao"])


def ponto_fraco(atr):
    return min(PONTO_FRACO_TETO, PONTO_FRACO_POR_PONTO * atr["percepcao"])


def corporal(atr):
    return min(CORPORAL_TETO, CORPORAL_POR_PONTO * atr["constituicao"])


def tenacidade_de(c):
    if c.lado == "inimigo":
        return c.d.get("tenacidade", 0.0)
    return min(TENACIDADE_TETO, TENACIDADE_POR_PONTO * c.atr["vontade"])


class Combatente:
    def __init__(self, cid, lado, d, atributos=None, equip=None):
        self.id, self.lado, self.d = cid, lado, d
        self.nome, self.retrato = d["nome"], d["retrato"]
        self.papel = d.get("papel", "inimigo")
        self.a = "a" if d.get("feminino") else "o"  # a concordância: atordoad{a}, caíd{a}
        self.estados = {}
        self.caido = False
        self.usadas = set()
        self.entra_rodada = 1
        self.preparando = None
        self.interrompido = False  # o inimigo já teve uma preparação interrompida: a próxima é firme
        self.vez_passou = False
        self.impeto = 0
        if lado == "aliado":
            self.atr = dict(atributos or d["atributos"])
            self.nivel = d["nivel"]
            self.vida_max = d["vida_base"] + VIDA_POR_NIVEL * self.nivel + VIDA_POR_PONTO * self.atr["constituicao"]
            self.recurso_nome, self.recurso_max = d["recurso"], C.RECURSO_MAX
            self.recurso = C.RECURSO_INICIO
            self.protecao = d["protecao"]
            if equip:  # o protagonista: a arma e o foco escolhidos
                self.equip = dict(equip)
                self.arma = C.EQUIPAMENTO["arma"][equip["arma"]]["valor"]
                self.foco = C.EQUIPAMENTO["foco"][equip["foco"]]["valor"]
            else:
                self.equip = None
                self.arma, self.foco = d["arma"], d["foco"]
            self.kit = list(d.get("kit", []))
            self.guarda = 0
        else:
            self.atr = {"agilidade": d["agi"], "percepcao": d["per"]}
            self.vida_max = d["vida"]
            self.protecao = d["protecao"]
            self.guarda = d.get("guarda", 0)
        self.vida = self.vida_max

    @property
    def vivo(self):
        return self.vida > 0

    def potencia(self, tipo):
        """Física: arma + nível + Força. Sobrenatural: foco + nível + Intelecto."""
        if tipo == "sobrenatural":
            return self.foco + self.nivel + self.atr["intelecto"]
        return self.arma + self.nivel + self.atr["forca"]

    def origem_potencia(self, tipo):
        if tipo == "sobrenatural":
            return f"foco {self.foco} + nível {self.nivel} + INT {self.atr['intelecto']}"
        return f"arma {self.arma} + nível {self.nivel} + FOR {self.atr['forca']}"

    def acoes(self):
        """O que ele pode escolher: os básicos (fora do kit) e o kit."""
        return list(C.BASICOS) + self.kit


class Combate:
    def __init__(self, encontro, build="forca", atributos=None, kit=None, equip=None, presenca=None, soma_exata=True):
        self.cfg = C.ENCONTROS[encontro]
        self.encontro = encontro
        self.rng = random.Random(self.cfg["semente"])
        b = C.BUILDS[build] if build in C.BUILDS else None
        atr_heroi = dict(atributos) if atributos else dict(b["atributos"])
        erro = validar_atributos(atr_heroi)
        if erro and (soma_exata or not erro.startswith("A soma")):  # a ficha mostra a construção enquanto se distribui
            raise ValueError(erro)
        kit_heroi = list(kit) if kit is not None else list(b["kit"])
        erro = validar_kit(kit_heroi)
        if erro:
            raise ValueError(erro)
        equip = dict(equip or C.EQUIPAMENTO_PADRAO)
        if equip.get("arma") not in C.EQUIPAMENTO["arma"] or equip.get("foco") not in C.EQUIPAMENTO["foco"]:
            raise ValueError("Equipamento desconhecido.")
        self.build = build if (b and atr_heroi == b["atributos"]) else "livre"
        self.presenca = presenca if presenca is not None else C.PRESENCA_PADRAO
        self.c = {}
        self.aliados = ["heroi", "odete", "morel"]
        self.c["heroi"] = Combatente("heroi", "aliado", C.GRUPO["heroi"], atr_heroi, equip)
        self.c["heroi"].kit = kit_heroi
        for cid in ("odete", "morel"):
            self.c[cid] = Combatente(cid, "aliado", C.GRUPO[cid])
        self.inimigos = []
        cont = {}
        for tipo in self.cfg["inimigos"]:
            cont[tipo] = cont.get(tipo, 0) + 1
            iid = f"{tipo}#{cont[tipo]}"
            self.c[iid] = Combatente(iid, "inimigo", C.INIMIGOS[tipo])
            self.c[iid].tipo = tipo
            self.inimigos.append(iid)
        self.cont_tipos = cont
        for iid in self.inimigos:  # dois do mesmo tipo: o número no nome, para o alvo nunca ser ambíguo
            if cont[self.c[iid].tipo] > 1:
                self.c[iid].nome += " " + iid.split("#")[1]
        self.consumiveis = dict(self.cfg.get("consumiveis", {}))
        self.eventos = []
        self.rodada = 1
        self.pos = 0
        self.turno_id = 0
        self.aguardando = None
        self.fim = None
        self.resumo = {"dano_recebido": {a: 0 for a in self.aliados}, "quedas": 0, "acoes": {},
                       "recurso": {a: {"gasto": 0, "turno": 0, "basico": 0} for a in self.aliados},
                       "preparos": 0, "preparos_resolvidos": 0, "preparos_desfeitos": 0, "preparos_aparados": 0,
                       "controles": {"resistidos": 0, "sofridos": 0}, "ultimate": 0}
        self._aplicar_inicio(self.cfg.get("inicio", {}))
        todos = self.aliados + self.inimigos
        self.ordem = sorted(todos, key=lambda i: (-self.c[i].atr["agilidade"], -self.c[i].atr["percepcao"],
                                                  0 if self.c[i].lado == "aliado" else 1, todos.index(i)))
        self.evento("rodada", f"Rodada 1. A ordem fica fixa: {', '.join(self.c[i].nome for i in self.ordem)}.")
        self._avancar()

    # ---------------------------------------------------------------- utilidades
    def evento(self, tipo, texto, **extra):
        self.eventos.append({"n": len(self.eventos), "rodada": self.rodada, "tipo": tipo, "texto": texto, **extra})

    def vivos(self, lado):
        ids = self.aliados if lado == "aliado" else self.inimigos
        return [i for i in ids if self.c[i].vivo and not self.c[i].caido]

    def _aplicar_inicio(self, inicio):
        for cid, cond in inicio.items():
            c = self.c[cid]
            for e in cond.get("estados", []):
                c.estados[e] = {"marco": "proxima_vez"}
            if cond.get("caido"):
                c.vida, c.caido = 0, True
            for k in ("agilidade",):
                if k in cond:
                    c.atr[k] = cond[k]
            for k in ("recurso", "vida", "impeto"):
                if k in cond:
                    setattr(c, k, cond[k])
            if cond.get("preparando"):
                p = c.d["preparo"]
                c.preparando = {"id": p["id"], "alvo": self._alvo_menos_vida(), "anunciado": 0, "firme": False}

    def _alvo_menos_vida(self):
        vivos = self.vivos("aliado")
        return min(vivos, key=lambda i: (self.c[i].vida / self.c[i].vida_max, self.aliados.index(i))) if vivos else None

    def _desafiante(self):
        h = self.c["heroi"]
        return h if "desafio" in h.estados and h.vivo and not h.caido else None

    def _impeto(self, motivo):
        h = self.c["heroi"]
        if not any(C.HABILIDADES[k].get("impeto") for k in h.kit) or h.impeto >= C.IMPETO_ULTIMATE:
            return
        h.impeto += 1
        self.evento("impeto", f"Ímpeto de Jean: {h.impeto} de {C.IMPETO_ULTIMATE} ({motivo}).", alvo="heroi")

    # ---------------------------------------------------------------- o relógio
    def _inicio_do_turno(self, c):
        for o in self.c.values():
            for e in list(o.estados):
                st = o.estados[e]
                if st.get("marco") == "inicio_turno" and st.get("de") == c.id:
                    del o.estados[e]
                    self.evento("expira", f"{o.nome}: {nome_estado(o, e)} acabou (início do turno de {c.nome}).", alvo=o.id)
        if c.lado == "aliado" and not c.caido:
            ganho = min(C.RECURSO_TURNO, c.recurso_max - c.recurso)
            c.recurso += ganho
            self.resumo["recurso"][c.id]["turno"] += ganho
        sg = c.estados.get("sangramento")
        if sg and c.vivo and not c.caido:
            self._perder_vida(c, sg["dano"], "Sangramento")
            sg["vezes"] -= 1
            if sg["vezes"] <= 0 and "sangramento" in c.estados:
                del c.estados["sangramento"]

    def _fim_da_rodada(self):
        for o in self.c.values():
            for e in list(o.estados):
                if o.estados[e].get("marco") == "fim_rodada" and o.estados[e].get("rodada") == self.rodada:
                    del o.estados[e]
                    self.evento("expira", f"{o.nome}: {nome_estado(o, e)} acabou (fim da rodada {self.rodada}).", alvo=o.id)
        self.rodada += 1
        self.pos = 0
        for o in self.c.values():
            o.vez_passou = False
        self.evento("rodada", f"Rodada {self.rodada}.")

    def _avancar(self):
        while not self.fim:
            if self.pos >= len(self.ordem):
                self._fim_da_rodada()
                continue
            c = self.c[self.ordem[self.pos]]
            if c.lado == "inimigo" and not c.vivo:
                c.vez_passou = True
                self.pos += 1
                continue
            if c.entra_rodada > self.rodada:
                c.vez_passou = True
                self.pos += 1
                continue
            self._inicio_do_turno(c)
            if self._conferir_fim():
                return
            if c.caido:
                self.evento("pula", f"{c.nome} está caíd{c.a}: a vez passa.", ator=c.id)
                c.vez_passou = True
                self.pos += 1
                continue
            perde = next((e for e in ("atordoado", "aterrorizado") if e in c.estados), None)
            if perde:
                del c.estados[perde]
                txt = f"{c.nome} está {nome_estado(c, perde).lower()}: perde a vez."
                if c.preparando:
                    txt += f" {NOME_PREPARO[c.preparando['id']]} se desfaz."
                    c.preparando = None
                    self.resumo["preparos_desfeitos"] += 1
                    self.evento("perde", txt, ator=c.id)
                    self._impeto("uma preparação desfeita")
                else:
                    self.evento("perde", txt, ator=c.id)
                c.vez_passou = True
                self.pos += 1
                continue
            if c.lado == "inimigo":
                self._agir_inimigo(c)
                c.vez_passou = True
                self.pos += 1
                if self._conferir_fim():
                    return
                continue
            self.turno_id += 1
            self.aguardando = c.id
            return

    def _conferir_fim(self):
        if self.c["heroi"].caido:
            self.fim = "derrota"
            self.evento("fim", "Jean caiu. Derrota (hipótese operacional: a queda do protagonista encerra a luta).")
        elif not self.vivos("inimigo"):
            self.fim = "vitoria"
            self.evento("fim", f"Vitória na rodada {self.rodada}.")
        if self.fim:
            self.aguardando = None
            self.resumo["rodadas"] = self.rodada
        return bool(self.fim)

    # ---------------------------------------------------------------- as ações dos aliados
    def custo(self, c, hid):
        return C.HABILIDADES[hid]["custo"]

    def motivo(self, c, acao):
        if acao.startswith("item:"):
            iid = acao[5:]
            if self.consumiveis.get(iid, 0) <= 0:
                return "Nenhum na bolsa."
            if C.CONSUMIVEIS[iid]["alvo"] == "aliado_caido" and not any(self.c[a].caido for a in self.aliados):
                return "Ninguém caído."
            return None
        h = C.HABILIDADES[acao]
        if h.get("uma_vez") and acao in c.usadas:
            return "Já usada nesta luta."
        if h["alvo"] == "aliado_caido" and not any(self.c[a].caido for a in self.aliados):
            return "Ninguém caído."
        if h.get("impeto") and c.impeto < C.IMPETO_ULTIMATE:
            return f"Ímpeto {c.impeto} de {C.IMPETO_ULTIMATE}: sobe quando um inimigo cai ou uma ameaça é desfeita ou aparada."
        if c.recurso < self.custo(c, acao):
            return f"{c.recurso_nome} insuficiente ({self.custo(c, acao)})."
        if acao in ("proteger", "comando") and len(self.vivos("aliado")) < 2:
            return "Ninguém para isso."
        return None

    def alvos(self, c, acao):
        tipo = C.CONSUMIVEIS[acao[5:]]["alvo"] if acao.startswith("item:") else C.HABILIDADES[acao]["alvo"]
        if tipo == "inimigo":
            return self.vivos("inimigo")
        if tipo == "aliado":
            vivos = self.vivos("aliado")
            return [a for a in vivos if a != c.id] if acao in ("proteger", "comando") else vivos
        if tipo == "aliado_caido":
            return [a for a in self.aliados if self.c[a].caido]
        return [c.id]  # proprio, inimigos (todos), grupo: sem escolha

    def agir(self, turno_id, acao, alvo=None):
        """Uma ação do aliado da vez. turno_id: o da vez que o jogador viu (um clique repetido chega com o id velho e é
        recusado sem fazer nada)."""
        if self.fim:
            return {"ok": False, "motivo": "A luta acabou."}
        if turno_id != self.turno_id or not self.aguardando:
            return {"ok": False, "motivo": "Essa vez já passou."}
        c = self.c[self.aguardando]
        if acao.startswith("item:") and acao[5:] not in C.CONSUMIVEIS or not acao.startswith("item:") and acao not in c.acoes():
            return {"ok": False, "motivo": "Ação desconhecida."}
        m = self.motivo(c, acao)
        if m:
            return {"ok": False, "motivo": m}
        validos = self.alvos(c, acao)
        if alvo is None and len(validos) == 1:
            alvo = validos[0]
        if alvo not in validos:
            return {"ok": False, "motivo": "Alvo inválido."}
        self.aguardando = None
        self._executar(c, acao, self.c[alvo])
        self.resumo["acoes"][acao] = self.resumo["acoes"].get(acao, 0) + 1
        c.vez_passou = True
        self.pos += 1
        if not self._conferir_fim():
            self._avancar()
        return {"ok": True}

    def _executar(self, c, acao, alvo):
        if acao.startswith("item:"):
            iid = acao[5:]
            it = C.CONSUMIVEIS[iid]
            self.consumiveis[iid] -= 1
            if "cura" in it:
                self._curar(c, alvo, it["cura"], it["nome"])
            else:
                self._reerguer(c, alvo, it["volta"], it["nome"])
            return
        h = C.HABILIDADES[acao]
        custo = self.custo(c, acao)
        ganho = min(h.get("ganha", 0), c.recurso_max - (c.recurso - custo))
        c.recurso = c.recurso - custo + ganho
        self.resumo["recurso"][c.id]["gasto"] += custo
        self.resumo["recurso"][c.id]["basico"] += ganho
        if h.get("uma_vez"):
            c.usadas.add(acao)
        if h.get("impeto"):
            c.impeto = 0
            self.resumo["ultimate"] += 1
        if acao == "defender":
            c.estados["defesa"] = {"marco": "inicio_turno", "de": c.id, "red": DEFESA}
            self.evento("acao", f"{c.nome} se defende: −{pct(DEFESA)} de dano até o início do próximo turno.", ator=c.id)
        elif acao == "proteger":
            alvo.estados["protegido"] = {"marco": "inicio_turno", "de": c.id, "por": c.id}
            c.estados["protegendo"] = {"marco": "inicio_turno", "de": c.id, "quem": alvo.id}
            self.evento("acao", f"{c.nome} protege {alvo.nome}: os golpes {'nela' if alvo.a == 'a' else 'nele'} vêm "
                                f"para {c.nome} até o início do próximo turno de {c.nome}.", ator=c.id, alvo=alvo.id)
        elif acao == "desafio":
            c.estados["desafio"] = {"marco": "inicio_turno", "de": c.id, "red": DESAFIO}
            self.evento("acao", f"{c.nome} desafia: os golpes e as preparações de alvo único miram {c.nome}, que recebe "
                                f"−{pct(DESAFIO)}, até o início do próximo turno dele.", ator=c.id)
        elif acao == "juramento":
            for a in self.vivos("aliado"):
                self.c[a].estados["juramento"] = {"marco": "inicio_turno", "de": c.id, "red": JURAMENTO}
            self.evento("acao", f"{c.nome} faz o Juramento: o grupo recebe −{pct(JURAMENTO)} e não sofre controle até o "
                                f"início do próximo turno de {c.nome}.", ator=c.id)
        elif acao == "comando":
            alvo.estados["comando"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "bonus": h["bonus"]}
            tirou = alvo.estados.pop("aterrorizado", None)
            self.evento("acao", f"{c.nome} comanda {alvo.nome}: o próximo golpe +{pct(h['bonus'])}"
                                + (f"; {alvo.nome} não está mais {nome_estado(alvo, 'aterrorizado').lower()}" if tirou else "")
                                + ".", ator=c.id, alvo=alvo.id)
        elif acao == "curar":
            self._curar(c, alvo, self.valor_cura(c), h["nome"])
        elif acao == "escudo_luz":
            alvo.estados["escudo"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "resta": h["escudo"]}
            self.evento("acao", f"{c.nome} põe o Escudo de Luz em {'si' if alvo is c else alvo.nome} (absorve "
                                f"{h['escudo']} até o fim da rodada {self.rodada + 1}).", ator=c.id, alvo=alvo.id)
        elif acao == "reerguer":
            self._reerguer(c, alvo, h["volta"], h["nome"])
        elif acao == "marcar":
            alvo.estados["marca"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "de": c.id, "bonus": h["marca"]}
            self.evento("acao", f"{c.nome} marca {alvo.nome}: o próximo golpe de outro aliado +{pct(h['marca'])}.",
                        ator=c.id, alvo=alvo.id)
        elif h["alvo"] == "inimigos":
            self.evento("acao", f"{c.nome} solta {h['nome']}.", ator=c.id)
            for i in list(self.vivos("inimigo")):
                self._golpe_aliado(c, self.c[i], h)
        else:
            self._golpe_aliado(c, alvo, h)

    def valor_cura(self, c):
        return C.HABILIDADES["curar"]["cura"] + 2 * c.nivel + c.d.get("simbolo", 0)

    def _curar(self, c, alvo, n, rotulo):
        antes = alvo.vida
        alvo.vida = min(alvo.vida_max, alvo.vida + n)
        self.evento("cura", f"{c.nome}: {rotulo} em {'si' if alvo is c else alvo.nome}, +{alvo.vida - antes} de vida.",
                    ator=c.id, alvo=alvo.id)

    def _reerguer(self, c, alvo, fracao, rotulo):
        alvo.caido = False
        alvo.vida = max(1, round(alvo.vida_max * fracao))
        alvo.estados = {}
        dele = "dela" if alvo.a == "a" else "dele"
        quando = (f"age ainda nesta rodada, na posição {dele}" if not alvo.vez_passou
                  else f"a vez {dele} nesta rodada já passou: age na próxima")
        self.evento("retorno", f"{c.nome}: {rotulo}. {alvo.nome} volta com {alvo.vida} de vida e {quando}.",
                    ator=c.id, alvo=alvo.id)

    # ---------------------------------------------------------------- a conta do golpe (a mesma na previsão e no real)
    def conta_golpe(self, c, alvo, h, critico_sim, guarda=None):
        """O dano de um golpe aliado no inimigo, com crítico ou sem, e as partes da conta. Não muda nada: a previsão e o
        golpe de verdade usam esta mesma função."""
        tipo = h["tipo"]
        pot = c.potencia(tipo)
        dano = pot * h["mult"]
        partes = [f"{pot} de potência ({c.origem_potencia(tipo)})" + (f" × {fmt(h['mult'])}" if h["mult"] != 1 else "")]
        com = c.estados.get("comando")
        if com:
            dano *= 1 + com["bonus"]
            partes.append(f"comando +{pct(com['bonus'])}")
        mk = alvo.estados.get("marca")
        if mk and mk["de"] != c.id:
            dano *= 1 + mk["bonus"]
            partes.append(f"marca +{pct(mk['bonus'])}")
        if alvo.d.get("ponto_fraco") and c.atr["percepcao"]:
            pf = ponto_fraco(c.atr)
            dano *= 1 + pf
            partes.append(f"ponto fraco +{pct(pf)} (PER {c.atr['percepcao']})")
        if critico_sim:
            dano *= CRITICO_MULT
            partes.append("crítico ×1,5")
        g = alvo.guarda if guarda is None else guarda
        if g and tipo == "fisico":
            dano *= GUARDA_MULT
            partes.append("guarda: metade")
        prot = max(0, alvo.protecao - h.get("ignora", 0))
        final = max(1, round(dano) - prot)
        if alvo.protecao:
            partes.append(f"proteção −{prot}" + (f" (ignora {h['ignora']})" if h.get("ignora") else ""))
        return final, partes

    def prever_golpe(self, c, alvo, h):
        """O que a tela mostra: o dano normal, o crítico e a chance (o rompimento do Golpe Pesado acontece antes)."""
        g = alvo.guarda
        if h.get("rompe") and g:
            g = max(0, g - c.atr["forca"])
        normal, _ = self.conta_golpe(c, alvo, h, False, g)
        crit, _ = self.conta_golpe(c, alvo, h, True, g)
        return {"normal": normal, "critico": crit, "chance": round(critico(c.atr), 2)}

    def _golpe_aliado(self, c, alvo, h):
        if h.get("rompe") and alvo.guarda:
            tira = min(alvo.guarda, c.atr["forca"])
            alvo.guarda -= tira
            self.evento("guarda", f"{c.nome} rompe {tira} da Guarda de {alvo.nome} (Força {c.atr['forca']}); "
                                  f"{'resta ' + str(alvo.guarda) if alvo.guarda else 'a guarda caiu'}.", ator=c.id, alvo=alvo.id)
        crit = self.rng.random() < critico(c.atr)
        dano, partes = self.conta_golpe(c, alvo, h, crit)
        c.estados.pop("comando", None)
        mk = alvo.estados.get("marca")
        if mk and mk["de"] != c.id:
            del alvo.estados["marca"]
        if alvo.guarda and h["tipo"] == "fisico" and not h.get("rompe"):
            alvo.guarda -= 1
            partes.append(f"−1 de Guarda (resta {alvo.guarda})")
        if h.get("interrompe"):
            self._interromper(c, alvo, h)
        self._receber(alvo, dano, f"{c.nome}: {h['nome']} em {{alvo}}", partes, ator=c.id, ja_contado=True)

    def _interromper(self, c, alvo, h):
        prep = alvo.preparando
        if prep and prep.get("firme"):
            self.evento("efeito", f"{alvo.nome} já foi interrompido uma vez: {nome_preparo(prep['id'])} está firme e "
                                  f"não se desfaz.", alvo=alvo.id)
            return
        if prep:
            self.evento("interrompe", f"{c.nome} acerta {alvo.nome}: {nome_preparo(prep['id'])} se desfaz.",
                        ator=c.id, alvo=alvo.id)
            alvo.preparando = None
            alvo.interrompido = True
            self.resumo["preparos_desfeitos"] += 1
            self._impeto("uma preparação desfeita")
        self._controlar(alvo, h["controle"], h["aplicacao"], c.nome)

    def chance_resistir(self, alvo, aplicacao):
        """A chance final de resistir: a Tenacidade do alvo menos a aplicação de quem controla (de 0 ao teto)."""
        return max(0.0, round(tenacidade_de(alvo) - aplicacao, 2))

    def _controlar(self, alvo, estado, aplicacao, origem):
        if "juramento" in alvo.estados:
            self.evento("efeito", f"{alvo.nome} está sob o Juramento: não sofre controle.", alvo=alvo.id)
            return False
        ch = self.chance_resistir(alvo, aplicacao)
        if ch > 0 and self.rng.random() < ch:
            self.resumo["controles"]["resistidos"] += alvo.lado == "aliado"
            self.evento("efeito", f"{alvo.nome} resiste: não fica {nome_estado(alvo, estado).lower()} (chance {pct(ch)}: "
                                  f"Tenacidade {pct(tenacidade_de(alvo))} − aplicação {pct(aplicacao)}).", alvo=alvo.id)
            return False
        alvo.estados[estado] = {"marco": "proxima_vez"}
        self.resumo["controles"]["sofridos"] += alvo.lado == "aliado"
        self.evento("efeito", f"{alvo.nome} fica {nome_estado(alvo, estado).lower()}: perde a próxima vez"
                              + (f" (resistia com {pct(ch)})." if ch else "."), alvo=alvo.id)
        return True

    # ---------------------------------------------------------------- receber dano
    def _redirecionar(self, alvo):
        """Quem recebe o golpe de um inimigo no alvo: o protetor, se houver; o Desafio já mudou o alvo antes."""
        prot = alvo.estados.get("protegido")
        if prot and alvo.lado == "aliado":
            p = self.c[prot["por"]]
            if p.vivo and not p.caido and p.id != alvo.id:
                return p
        return alvo

    def reducoes(self, o):
        """As reduções de dano do aliado agora (multiplicam): defesa, desafio, juramento."""
        r = []
        for k in ("defesa", "desafio", "juramento"):
            if k in o.estados:
                r.append((k, o.estados[k]["red"]))
        return r

    def dano_inimigo(self, o, dano):
        """O dano que um golpe inimigo de `dano` faz em o (sem o escudo), e as partes."""
        d = dano
        partes = [f"{dano} de dano"]
        for k, red in self.reducoes(o):
            d *= 1 - red
            partes.append(f"{NOME_ESTADO[k].lower()} −{pct(red)}")
        d = max(1, round(d) - o.protecao)
        if o.protecao:
            partes.append(f"proteção −{o.protecao}")
        return d, partes

    def _receber(self, alvo, dano, rotulo, partes, ator=None, ja_contado=False):
        if ja_contado:
            d = dano
        else:
            quem = self._redirecionar(alvo) if alvo.lado == "aliado" else alvo
            if quem is not alvo:
                self.evento("protege", f"{quem.nome} entra na frente de {alvo.nome}.", alvo=quem.id)
            alvo = quem
            d, partes = self.dano_inimigo(alvo, dano)
        esc = alvo.estados.get("escudo")
        absorvido = 0
        if esc:
            absorvido = min(esc["resta"], d)
            esc["resta"] -= absorvido
            d -= absorvido
            if esc["resta"] <= 0:
                del alvo.estados["escudo"]
        texto = rotulo.format(alvo=alvo.nome) + f": {d} de dano" + (f" ({absorvido} no escudo)" if absorvido else "")
        self.evento("dano", texto, ator=ator, alvo=alvo.id, conta=", ".join(partes))
        self._perder_vida(alvo, d, None)
        return alvo

    def _perder_vida(self, alvo, d, rotulo):
        if rotulo:
            self.evento("dano", f"{rotulo}: {alvo.nome} perde {d}.", alvo=alvo.id)
        if alvo.lado == "aliado":
            self.resumo["dano_recebido"][alvo.id] += min(d, alvo.vida)
        alvo.vida = max(0, alvo.vida - d)
        if alvo.vida <= 0:
            if alvo.lado == "aliado":
                alvo.caido = True
                alvo.estados = {}
                self.resumo["quedas"] += 1
                self.evento("queda", f"{alvo.nome} cai: fica incapacitad{alvo.a} (não morre).", alvo=alvo.id)
            else:
                if alvo.preparando:
                    self.evento("efeito", f"{nome_preparo(alvo.preparando['id'], True)} de {alvo.nome} não sai.", alvo=alvo.id)
                    alvo.preparando = None
                    self.resumo["preparos_desfeitos"] += 1
                    self._impeto("uma preparação desfeita")
                self.evento("derrota", f"{alvo.nome} cai.", alvo=alvo.id)
                self._impeto(f"{alvo.nome} caiu")

    # ---------------------------------------------------------------- os inimigos
    def _agir_inimigo(self, c):
        d = c.d
        if c.preparando:
            self._resolver_preparo(c)
            return
        inv = d.get("invoca")
        if inv and self.rodada in inv["em"] and len([i for i in self.vivos("inimigo") if self.c[i].tipo == inv["quem"]]) < inv["max"]:
            tipo = inv["quem"]
            self.cont_tipos[tipo] = self.cont_tipos.get(tipo, 0) + 1
            iid = f"{tipo}#{self.cont_tipos[tipo]}"
            n = Combatente(iid, "inimigo", C.INIMIGOS[tipo])
            n.tipo, n.entra_rodada = tipo, self.rodada + 1
            n.nome += " " + str(self.cont_tipos[tipo])
            self.c[iid] = n
            self.inimigos.append(iid)
            self.ordem.append(iid)
            self.evento("invoca", f"{c.nome} chama um {n.nome}: entra no fim da ordem e age a partir da rodada "
                                  f"{self.rodada + 1} (hipótese operacional).", ator=c.id, alvo=iid)
            return
        p = d.get("preparo")
        if p and self.rodada in p["em"]:
            alvo = None if p.get("area") else self._alvo_menos_vida()
            c.preparando = {"id": p["id"], "alvo": alvo, "anunciado": self.rodada, "firme": c.interrompido}
            self.resumo["preparos"] += 1
            quem = "todo o grupo" if p.get("area") else self.c[alvo].nome
            firme = " Já interrompido uma vez: desta vez não se desfaz." if c.interrompido else ""
            self.evento("prepara", f"{c.nome} {p['aviso']}: prepara {p['nome']} em {quem}. Resolve na próxima vez dele."
                        + firme, ator=c.id, alvo=alvo)
            return
        des = self._desafiante()
        alvo = des or self.c[self.rng.choice(self.vivos("aliado"))]
        self._receber(alvo, d["dano"], f"{c.nome}: {d['golpe']} em {{alvo}}", None, ator=c.id)

    def alvo_do_preparo(self, prep):
        """Em quem a preparação vai cair agora: o Desafio puxa para Jean; senão o anunciado (ou o mais ferido, se ele
        caiu); depois a proteção."""
        des = self._desafiante()
        if des:
            mira = des
        elif prep["alvo"] and self.c[prep["alvo"]].vivo and not self.c[prep["alvo"]].caido:
            mira = self.c[prep["alvo"]]
        else:
            m = self._alvo_menos_vida()
            mira = self.c[m] if m else None
        return mira, (self._redirecionar(mira) if mira else None)

    def _resolver_preparo(self, c):
        p = c.d["preparo"]
        prep, c.preparando = c.preparando, None
        self.resumo["preparos_resolvidos"] += 1
        if p.get("area"):
            self.evento("resolve", f"{c.nome} solta o {p['nome']}.", ator=c.id)
            for a in self.vivos("aliado"):
                self._controlar(self.c[a], p["controle"], p["aplicacao"], c.nome)
            return
        mira, recebe = self.alvo_do_preparo(prep)
        if not recebe:
            return
        aparado = recebe is not mira or any(k in recebe.estados for k in ("defesa", "desafio", "juramento", "escudo"))
        self.evento("resolve", f"{c.nome} solta {p['nome']}.", ator=c.id)
        recebeu = self._receber(recebe, p["dano"], f"{c.nome}: {p['nome']} em {{alvo}}", None, ator=c.id, ja_contado=False) \
            if recebe is mira else self._receber_direto(recebe, mira, p["dano"], c, p)
        if aparado:
            self.resumo["preparos_aparados"] += 1
            self._impeto("uma ameaça aparada")
        if recebeu.caido:
            return
        if p.get("controle"):
            self._controlar(recebeu, p["controle"], p["aplicacao"], c.nome)
        if p.get("sangra"):
            dano = max(1, round(p["sangra"] * (1 - corporal(recebeu.atr))))
            recebeu.estados["sangramento"] = {"marco": "vezes", "vezes": 2, "dano": dano}
            self.evento("efeito", f"{recebeu.nome} sangra: perde {dano} no início dos 2 próximos turnos "
                                  f"({p['sangra']} − {pct(corporal(recebeu.atr))} pela Constituição {recebeu.atr['constituicao']}).",
                        alvo=recebeu.id)

    def _receber_direto(self, recebe, mira, dano, c, p):
        """O golpe que o protetor recebe no lugar do alvo (já redirecionado)."""
        self.evento("protege", f"{recebe.nome} entra na frente de {mira.nome}.", alvo=recebe.id)
        d, partes = self.dano_inimigo(recebe, dano)
        return self._receber(recebe, d, f"{c.nome}: {p['nome']} em {{alvo}}", partes, ator=c.id, ja_contado=True)

    # ---------------------------------------------------------------- previsões e a ficha
    def prever_ameaca(self, c):
        p = c.d["preparo"]
        if p.get("area"):
            return {"alvos": [{"id": a, "nome": self.c[a].nome, **self._previsao_controle(self.c[a], p)}
                              for a in self.vivos("aliado")]}
        mira, recebe = self.alvo_do_preparo(c.preparando)
        if not recebe:
            return {}
        d, _ = self.dano_inimigo(recebe, p["dano"])
        esc = recebe.estados.get("escudo")
        agora = max(0, d - (esc["resta"] if esc else 0))
        se_def = max(0, max(1, round(p["dano"] * (1 - DEFESA)) - mira.protecao) - (esc["resta"] if esc else 0)) \
            if mira is recebe and "defesa" not in mira.estados else None
        r = {"mira": mira.id, "quem": recebe.id, "agora": agora, "se_defender": se_def}
        if p.get("controle"):
            r.update(self._previsao_controle(recebe, p))
        if p.get("sangra"):
            r["sangra"] = max(1, round(p["sangra"] * (1 - corporal(recebe.atr))))
        return r

    def _previsao_controle(self, o, p):
        if "juramento" in o.estados:
            return {"controle": p["controle"], "resiste": 1.0, "juramento": True}
        return {"controle": p["controle"], "resiste": self.chance_resistir(o, p["aplicacao"])}

    def derivados(self, c):
        a = c.atr
        lin = []

        def L(chave, nome, valor, como):
            lin.append({"id": chave, "nome": nome, "valor": valor, "como": como})
        L("vida", "Vida máxima", c.vida_max,
          f"{c.d['vida_base']} da classe + {VIDA_POR_NIVEL} × nível {c.nivel} + {VIDA_POR_PONTO} × CON {a['constituicao']}")
        L("iniciativa", "Posição na ordem", self.ordem.index(c.id) + 1, f"AGI {a['agilidade']} (fixa a luta inteira)")
        L("fisico", "Potência física", c.potencia("fisico"), c.origem_potencia("fisico"))
        L("sobrenatural", "Potência sobrenatural", c.potencia("sobrenatural"), c.origem_potencia("sobrenatural"))
        L("critico", "Crítico", pct(critico(a)), f"2% × PER {a['percepcao']} (até 25%); dano ×1,5")
        L("ponto_fraco", "Contra ponto fraco", f"+{pct(ponto_fraco(a))}", f"4% × PER {a['percepcao']} (até 40%)")
        L("protecao", "Proteção", c.protecao, "da armadura: tira isso de cada golpe")
        L("corporal", "Resistência corporal", f"−{pct(corporal(a))}", f"4% × CON {a['constituicao']} no sangramento (até 40%)")
        L("tenacidade", "Tenacidade", pct(tenacidade_de(c)), f"4% × VON {a['vontade']} (até 40%): chance de resistir a controle")
        L("defesa", "Defender reduz", pct(DEFESA), "da regra (sem atributo)")
        L("recurso", c.recurso_nome, f"{C.RECURSO_INICIO} de {C.RECURSO_MAX}",
          f"+{C.RECURSO_TURNO} no início de cada turno; o ataque básico, +{C.RECURSO_BASICO}")
        if "curar" in c.kit:
            L("cura", "Curar", self.valor_cura(c), f"{C.HABILIDADES['curar']['cura']} + 2 × nível + símbolo {c.d.get('simbolo', 0)}")
        return lin

    def tabela_dano(self, c, alvo):
        """O dano previsto de cada golpe que c pode dar (os básicos e o kit) no alvo, normal e crítico."""
        lin = []
        for hid in c.acoes():
            h = C.HABILIDADES[hid]
            if "mult" in h:
                p = self.prever_golpe(c, alvo, h)
                lin.append({"id": hid, "nome": h["nome"], "custo": self.custo(c, hid), "tipo": h["tipo"],
                            "ultimate": h.get("tier") == "ultimate", **p})
        return lin

    # ---------------------------------------------------------------- o estado para a tela
    def estado(self):
        def comb(i):
            o = self.c[i]
            e = {"id": i, "nome": o.nome, "lado": o.lado, "papel": o.papel, "a": o.a, "retrato": o.retrato,
                 "vida": o.vida, "vida_max": o.vida_max, "caido": o.caido, "vivo": o.vivo, "guarda": o.guarda,
                 "guarda_max": o.d.get("guarda", 0), "protecao": o.protecao, "ponto_fraco": o.d.get("ponto_fraco"),
                 "tenacidade": round(tenacidade_de(o), 2),
                 "estados": [{"id": k, "nome": nome_estado(o, k), "ate": self._marco(o, k, v),
                              **({"resta": v["resta"]} if "resta" in v else {}),
                              **({"vezes": v["vezes"], "dano": v["dano"]} if "vezes" in v else {})}
                             for k, v in o.estados.items()],
                 "entra_rodada": o.entra_rodada}
            if o.lado == "aliado":
                e.update(recurso=o.recurso, recurso_max=o.recurso_max, recurso_nome=o.recurso_nome, atributos=o.atr,
                         derivados=self.derivados(o), impeto=o.impeto if i == "heroi" else None,
                         tem_ultimate=any(C.HABILIDADES[k].get("impeto") for k in o.kit))
            else:
                e.update(interrompido=o.interrompido)
            return e
        ameacas = []
        for i in self.inimigos:
            o = self.c[i]
            if o.vivo and o.preparando:
                p = o.d["preparo"]
                a = {"de": i, "nome": p["nome"], "area": bool(p.get("area")), "anunciado": o.preparando["anunciado"],
                     "firme": o.preparando.get("firme", False), "dano": p.get("dano"),
                     "resolve": "na próxima vez de " + o.nome + (" (nesta rodada)" if not o.vez_passou else f" (rodada {self.rodada + 1})"),
                     **self.prever_ameaca(o)}
                for k in ("mira", "quem"):
                    if a.get(k):
                        a[k + "_nome"] = self.c[a[k]].nome
                ameacas.append(a)
        acoes = []
        ativo = self.c[self.aguardando] if self.aguardando else None
        if ativo:
            for hid in ativo.acoes():
                h = C.HABILIDADES[hid]
                al = self.alvos(ativo, hid)
                x = {"id": hid, "nome": h["nome"], "desc": h["desc"], "custo": self.custo(ativo, hid),
                     "recurso": ativo.recurso_nome, "motivo": self.motivo(ativo, hid), "alvo": h["alvo"], "alvos": al,
                     "basico": bool(h.get("basico")), "ultimate": h.get("tier") == "ultimate",
                     "tier": h.get("tier")}
                if "mult" in h:
                    x["previsoes"] = {i: self.prever_golpe(ativo, self.c[i], h) for i in self.vivos("inimigo")}
                if hid == "curar":
                    x["cura"] = self.valor_cura(ativo)
                acoes.append(x)
            for iid, n in self.consumiveis.items():
                it = C.CONSUMIVEIS[iid]
                acoes.append({"id": "item:" + iid, "nome": it["nome"], "desc": it["desc"], "qtd": n, "icone": it["icone"],
                              "motivo": self.motivo(ativo, "item:" + iid), "alvo": it["alvo"],
                              "alvos": self.alvos(ativo, "item:" + iid), "item": True, "basico": True})
        h = self.c["heroi"]
        return {"versao": 2, "encontro": self.encontro, "nome": self.cfg["nome"], "objetivo": self.cfg["objetivo"],
                "teste": self.cfg.get("teste"), "build": self.build, "kit": h.kit, "equip": h.equip,
                "presenca": self.presenca, "rodada": self.rodada,
                "pos": self.pos, "turno_id": self.turno_id, "aguardando": self.aguardando, "fim": self.fim,
                "ordem": [{"id": i, "nome": self.c[i].nome, "a": self.c[i].a, "retrato": self.c[i].retrato,
                           "lado": self.c[i].lado, "passou": self.c[i].vez_passou, "atual": i == self.aguardando,
                           "fora": (self.c[i].lado == "inimigo" and not self.c[i].vivo) or self.c[i].caido,
                           "entra": self.c[i].entra_rodada if self.c[i].entra_rodada > self.rodada else None}
                          for i in self.ordem],
                "aliados": [comb(i) for i in self.aliados], "inimigos": [comb(i) for i in self.inimigos],
                "ameacas": ameacas, "acoes": acoes, "consumiveis": self.consumiveis, "eventos": self.eventos,
                "resumo": self.resumo, "impeto_max": C.IMPETO_ULTIMATE}

    def _marco(self, o, k, v):
        m = v.get("marco")
        if m == "inicio_turno":
            return f"até o início do próximo turno de {self.c[v['de']].nome}"
        if m == "fim_rodada":
            return f"até o fim da rodada {v['rodada']}"
        if m == "proxima_vez":
            return "perde a próxima vez"
        if m == "vezes":
            return f"−{v['dano']} no início de {v['vezes']} {'turno' if v['vezes'] == 1 else 'turnos'}"
        return ""


def fmt(x):
    return str(x).replace(".", ",")


NOME_ESTADO = {"defesa": "Defendendo", "protegido": "Protegido", "protegendo": "Protegendo", "desafio": "Desafiando",
               "juramento": "Juramento", "atordoado": "Atordoado", "aterrorizado": "Aterrorizado",
               "comando": "Comandado", "escudo": "Escudo de Luz", "marca": "Marcado", "sangramento": "Sangrando"}
NOME_PREPARO = {"bote": "O Bote", "esmagador": "O Golpe Esmagador", "terror": "O Grito de Terror"}


def nome_estado(o, k):
    """O nome do estado concordando com o portador (Odette fica Atordoada)."""
    n = NOME_ESTADO[k]
    return n[:-1] + "a" if o.a == "a" and n.endswith("do") and not n.endswith("ndo") else n


def nome_preparo(pid, maiuscula=False):
    n = NOME_PREPARO[pid]
    return n if maiuscula else n[0].lower() + n[1:]


# ---------------------------------------------------------------- a ficha das construções (fora da luta)
ALVO_REFERENCIA = "bruto"


def ficha(atributos, kit, equip=None, presenca=None, build="livre"):
    """O que a construção faz, para escolher e comparar: atributos, derivados, o dano previsto de cada golpe no mesmo
    alvo (o Bandido Bruto, proteção 2, ponto fraco), custos, e o kit. Usa as regras de verdade (um Combate do encontro 2
    só para ter a ordem e o alvo)."""
    cb = Combate("e2", atributos=atributos, kit=kit, equip=equip, presenca=presenca, soma_exata=False)
    h = cb.c["heroi"]
    alvo = cb.c["bruto#1"]
    der = cb.derivados(h)
    next(d for d in der if d["id"] == "iniciativa")["como"] += " · no encontro 2"
    return {"build": build, "atributos": h.atr, "presenca": cb.presenca, "kit": h.kit, "equip": h.equip,
            "pontos_kit": pontos_kit(h.kit), "derivados": der, "dano": cb.tabela_dano(h, alvo),
            "alvo": {"nome": alvo.nome, "protecao": alvo.protecao, "ponto_fraco": alvo.d.get("ponto_fraco")},
            "custos": [{"id": k, "nome": C.HABILIDADES[k]["nome"], "custo": C.HABILIDADES[k]["custo"],
                        "pontos": C.PONTOS_TIER[C.HABILIDADES[k]["tier"]], "tier": C.HABILIDADES[k]["tier"]} for k in h.kit],
            "ordem_e2": [cb.c[i].nome for i in cb.ordem]}


DANO_HEROI = ("atacar", "corte", "golpe_pesado", "lamina", "escudo_golpe", "furia", "tempestade")


def comparar_builds(equip=None):
    """As construções prontas lado a lado, no mesmo nível, equipamento e alvo: a ficha de cada uma (com o kit sugerido)
    e o dano previsto de todos os golpes do protagonista no Bandido Bruto, levando o golpe no kit ou não."""
    colunas = []
    for bid, b in C.BUILDS.items():
        f = ficha(b["atributos"], b["kit"], equip, build=bid)
        cb = Combate("e2", atributos=b["atributos"], kit=[], equip=equip)
        h, alvo = cb.c["heroi"], cb.c["bruto#1"]
        f["dano_todos"] = [{"id": k, "nome": C.HABILIDADES[k]["nome"], **cb.prever_golpe(h, alvo, C.HABILIDADES[k])}
                           for k in DANO_HEROI]
        f.update(nome=b["nome"], frase=b["frase"], ganha=b["ganha"], abre_mao=b["abre_mao"])
        colunas.append(f)
    return {"colunas": colunas}


def comparar_equipamento(atributos, kit, peca):
    """A mesma construção, nível e alvo, mudando só a arma ou só o foco: o dano previsto de cada golpe."""
    linhas = []
    for oid, o in C.EQUIPAMENTO[peca].items():
        equip = dict(C.EQUIPAMENTO_PADRAO, **{peca: oid})
        f = ficha(atributos, kit, equip)
        f["dano"] = [x for x in f["dano"] if x["tipo"] == ("fisico" if peca == "arma" else "sobrenatural")]
        linhas.append({"id": oid, "nome": o["nome"], "valor": o["valor"], "dano": f["dano"]})
    return {"peca": peca, "linhas": linhas}


def situacao(atributos, presenca, escolha=None, ajuda=False):
    """A situação de aventura: as opções com o que o protagonista consegue sozinho e o que um companheiro acrescenta."""
    atr = dict(atributos, presenca=presenca)
    s = C.SITUACAO
    res = None
    if escolha:
        o = next(x for x in s["opcoes"] if x["id"] == escolha)
        if ajuda and o.get("ajuda"):
            quem = C.GRUPO[o["ajuda"]["quem"]]
            res = {"ok": True, "texto": o["ok"] if o["id"] != "erguer" else o["ok"] + " Mas o barulho desce a escada.",
                   "como": f"{quem['nome']} ajuda"}
        else:
            ok = atr[o["atributo"]] >= o["minimo"]
            res = {"ok": ok, "texto": o["ok"] if ok else o["nao"],
                   "como": f"{C.NOME_ATRIBUTO[o['atributo']]} {atr[o['atributo']]} (a situação pede {o['minimo']})"}
    return {"titulo": s["titulo"], "texto": s["texto"], "resultado": res,
            "opcoes": [{"id": o["id"], "texto": o["texto"], "atributo": C.NOME_ATRIBUTO[o["atributo"]],
                        "valor": atr[o["atributo"]], "minimo": o["minimo"], "ajuda": o.get("ajuda")} for o in s["opcoes"]]}
