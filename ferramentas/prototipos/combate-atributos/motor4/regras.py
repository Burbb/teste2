"""As regras da quarta versão do protótipo de combate e atributos (26/10/2026; nada no jogo): a terceira (motor3/,
congelada) com o refinamento da seção 3.9 do 25 (sem a Marca, com o Golpe Oportuno do Morel e a Chuva de Brasas). As
versões anteriores (motor/, motor2/, motor3/) ficam congeladas para comparar.

Os relógios (dois nomes, nunca "turno" para os dois):
- **turno**: a vez de um combatente. Começa (o aliado recupera 6 do recurso; expira o que dura "até o início do
  próximo turno" dele; Sangramento e Queimadura pingam), e então ele age, perde a vez (atordoado, aterrorizado) ou é
  pulado (caído, ainda não entrou).
- **rodada**: a ordem inteira, uma vez cada um. No fim dela expira o que dura "até o fim da rodada N".

A conta de um golpe (a mesma na previsão e no golpe de verdade, `conta_golpe`):
1. potência = valor de base (arma, foco ou nada) + nível + Σ coeficiente × atributo (ou × vida máxima);
2. × o multiplicador da habilidade;
3. + o que a habilidade consome (Combustão: 200% do que a Queimadura do alvo ainda faria, sem resistência ainda);
4. × (1 + a soma dos bônus: comando, ponto fraco, estado do alvo, alvo vulnerável);
5. × 1,5 se crítico;
6. × 0,5 se o golpe é físico e o alvo tem Guarda;
7. × (1 − as reduções do alvo: defesa, desafio, juramento), quando o alvo é aliado;
8. a defesa do tipo, uma só: físico − (proteção − o que o golpe ignora, nunca abaixo de 0); arcano e fogo ×
   (1 − resistência efetiva), resistência efetiva = resistência do tipo − penetração do golpe, entre 0 e 60%;
9. arredonda, mínimo 1; o Escudo de Luz absorve depois.
A Queimadura pinga pelo valor cru × (1 − resistência ao fogo do portador); a Tenacidade (controle) não entra na
conta de dano.

Os atributos (provisórios, graduais, sem desbloqueio por pontuação): a Força e o Intelecto entram na potência das
habilidades que dizem escalar com eles; Percepção dá crítico (2%/ponto, até 25%) e ponto fraco (+3%/ponto, até
+30%); Constituição dá vida (4/ponto) e resistência corporal ao Sangramento (−4%/ponto, até −40%); Vontade dá
recurso máximo (+3/ponto) e Tenacidade (4%/ponto, até 40%); Agilidade só a ordem; Presença nada na luta.

As preparações dos inimigos contam os turnos em que eles agem: na v2 elas estavam presas ao número da rodada e um
atordoamento na rodada certa apagava a preparação (o caso do Bruto com zero preparações). Aqui, o turno perdido não
conta: o controle adia. Interromper desfaz a preparação, a não ser que ela seja ininterruptível (sinalizada; o Bruto
furioso, abaixo da metade da vida). Não há mais a regra geral de "firme depois da primeira interrupção".

A ultimate: uma utilização por combatente por luta, disponível desde o início, gasta a ação e recurso; queda e retorno
não devolvem o uso.

Hipóteses operacionais mantidas (não decisões): a queda do protagonista encerra a luta; o desempate da ordem
(Percepção, aliado antes de inimigo, entrada); o invocado entra no fim da ordem e age a partir da rodada seguinte."""
import random

from . import conteudo as C

CRITICO_POR_PONTO, CRITICO_TETO, CRITICO_MULT = 0.02, 0.25, 1.5
PONTO_FRACO_POR_PONTO, PONTO_FRACO_TETO = 0.03, 0.30
VIDA_POR_PONTO, VIDA_POR_NIVEL = 4, 6
CORPORAL_POR_PONTO, CORPORAL_TETO = 0.04, 0.40
TENACIDADE_POR_PONTO, TENACIDADE_TETO = 0.04, 0.40
DEFESA, DESAFIO, JURAMENTO = 0.40, 0.25, 0.50
GUARDA_MULT = 0.5
QUEIMA_FRACAO, QUEIMA_PILHAS, QUEIMA_VEZES = 0.30, 3, 3


def pct(x):
    return f"{round(x * 100)}%"


def fmt(x):
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x).replace(".", ",")


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


def recurso_max(nivel, atr):
    return C.RECURSO_BASE + C.RECURSO_NIVEL * nivel + C.RECURSO_VONTADE * atr["vontade"]


def tenacidade_de(c):
    if c.lado == "inimigo":
        return c.d.get("tenacidade", 0.0)
    return min(TENACIDADE_TETO, TENACIDADE_POR_PONTO * c.atr["vontade"])


def descrever(h):
    """O tipo, a escala e a defesa de uma habilidade, para a tela."""
    if "tipo" not in h:
        return None
    partes = []
    base = {"arma": "arma", "foco": "foco", None: None}[h.get("base")]
    if base:
        partes.append(base)
    partes.append("nível")
    partes += [f"{fmt(k)} × {C.NOME_ATRIBUTO[a]}" if k != 1 else C.NOME_ATRIBUTO[a] for a, k in h["escala"].items()]
    defesa = C.DEFESA_TIPO[h["tipo"]]
    if h.get("ignora"):
        defesa += f", ignora {h['ignora']}"
    if h.get("penetra"):
        defesa += f", ignora {pct(h['penetra'])}"
    if h["tipo"] == "fisico" and not h.get("rompe"):
        defesa += "; a Guarda corta à metade"
    return {"tipo": C.TIPOS[h["tipo"]], "tipo_id": h["tipo"], "escala": " + ".join(partes) + (f", × {fmt(h['mult'])}" if h["mult"] != 1 else ""),
            "defesa": defesa}


class Combatente:
    def __init__(self, cid, lado, d, atributos=None, equip=None):
        self.id, self.lado, self.d = cid, lado, d
        self.nome, self.retrato = d["nome"], d["retrato"]
        self.papel = d.get("papel", "inimigo")
        self.a = "a" if d.get("feminino") else "o"
        self.estados = {}
        self.caido = False
        self.usadas = set()
        self.entra_rodada = 1
        self.preparando = None
        self.vez_passou = False
        self.turnos_agidos = 0     # inimigo: os turnos em que agiu (a cadência das preparações)
        self.turnos = 0            # aliado: os turnos em que pôde escolher
        self.ultimate_usada = False
        self.parado = False
        if lado == "aliado":
            self.atr = dict(atributos or d["atributos"])
            self.nivel = d["nivel"]
            self.vida_max = d["vida_base"] + VIDA_POR_NIVEL * self.nivel + VIDA_POR_PONTO * self.atr["constituicao"]
            self.recurso_nome = d["recurso"]
            self.recurso_max = recurso_max(self.nivel, self.atr)
            self.recurso = self.recurso_max  # a reserva começa cheia
            self.protecao = d["protecao"]
            self.res = {}
            if equip:
                self.equip = dict(equip)
                self.arma = C.EQUIPAMENTO["arma"][equip["arma"]]["valor"]
                self.foco = C.EQUIPAMENTO["foco"][equip["foco"]]["valor"]
                self.res = dict(C.EQUIPAMENTO["manto"][equip["manto"]]["res"])
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
            self.res = dict(d.get("res", {}))
        self.vida = self.vida_max

    @property
    def vivo(self):
        return self.vida > 0

    def resistencia(self, tipo, penetra=0.0):
        """A resistência efetiva a um tipo (arcano, fogo): a do combatente menos a penetração, entre 0 e o teto."""
        return max(0.0, min(C.RESISTENCIA_TETO, self.res.get(tipo, 0.0) - penetra))

    def potencia(self, h):
        base = {"arma": self.arma, "foco": self.foco, None: 0}[h.get("base")]
        total = base + self.nivel
        for a, k in h["escala"].items():
            total += k * (self.vida_max if a == "vida" else self.atr[a])
        return int(total) if total == int(total) else round(total, 1)

    def origem_potencia(self, h):
        partes = []
        if h.get("base") == "arma":
            partes.append(f"arma {self.arma}")
        if h.get("base") == "foco":
            partes.append(f"foco {self.foco}")
        partes.append(f"nível {self.nivel}")
        for a, k in h["escala"].items():
            v = self.vida_max if a == "vida" else self.atr[a]
            partes.append(f"{fmt(k)} × {C.SIGLA[a]} {v}" if k != 1 else f"{C.SIGLA[a]} {v}")
        return " + ".join(partes)

    def acoes(self):
        return list(C.BASICOS) + self.kit

    def ultimate(self):
        return next((k for k in self.kit if C.HABILIDADES[k].get("ultimate")), None)


class Combate:
    def __init__(self, encontro, build="forca", atributos=None, kit=None, equip=None, presenca=None, soma_exata=True):
        self.cfg = C.ENCONTROS[encontro]
        self.encontro = encontro
        self.rng = random.Random(self.cfg["semente"])
        b = C.BUILDS[build] if build in C.BUILDS else None
        atr_heroi = dict(atributos) if atributos else dict(b["atributos"])
        erro = validar_atributos(atr_heroi)
        if erro and (soma_exata or not erro.startswith("A soma")):
            raise ValueError(erro)
        kit_heroi = list(kit) if kit is not None else list(b["kit"])
        erro = validar_kit(kit_heroi)
        if erro:
            raise ValueError(erro)
        equip = dict(C.EQUIPAMENTO_PADRAO, **(equip or {}))
        if any(equip.get(p) not in C.EQUIPAMENTO[p] for p in C.EQUIPAMENTO):
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
        for iid in self.inimigos:
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
                       "ameacas": [], "adiamentos": [],
                       "controles": {"aliados": {"sofridos": 0, "resistidos": 0}, "inimigos": {"sofridos": 0, "resistidos": 0}},
                       "ultimates": {a: {"equipada": self.c[a].ultimate(), "turnos_disponivel": 0, "turnos_sem_recurso": 0,
                                         "turnos_ja_usada": 0, "uso": None} for a in self.aliados},
                       "linha": []}
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
            if "agilidade" in cond:
                c.atr["agilidade"] = cond["agilidade"]
            for k in ("vida_max", "vida", "recurso", "guarda", "parado"):
                if k in cond:
                    setattr(c, k, cond[k])
            if cond.get("preparando"):
                p = c.d["preparo"]
                c.preparando = {"id": p["id"], "alvo": self._alvo_menos_vida(), "anunciado": 0, "ininterruptivel": False}
                self._ameaca_nova(c, c.preparando)

    def _alvo_menos_vida(self):
        vivos = self.vivos("aliado")
        return min(vivos, key=lambda i: (self.c[i].vida / self.c[i].vida_max, self.aliados.index(i))) if vivos else None

    def _atraente(self):
        """Quem puxa os golpes de alvo único: Desafio ou Avanço do Baluarte."""
        h = self.c["heroi"]
        return h if any(k in h.estados for k in ("desafio", "atrai")) and h.vivo and not h.caido else None

    # ---------------------------------------------------------------- telemetria das ameaças
    def _ameaca_nova(self, c, prep):
        p = c.d["preparo"]
        reg = {"de": c.id, "inimigo": c.nome, "nome": p["nome"], "rodada": self.rodada, "alvo": prep["alvo"],
               "ininterruptivel": prep["ininterruptivel"], "resultado": None, "rodada_fim": None, "dano": None,
               "aparada": False}
        self.resumo["ameacas"].append(reg)
        prep["reg"] = len(self.resumo["ameacas"]) - 1

    def _ameaca_fim(self, prep, resultado, dano=None, aparada=False):
        reg = self.resumo["ameacas"][prep["reg"]]
        reg.update(resultado=resultado, rodada_fim=self.rodada, dano=dano, aparada=aparada)

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
        if not c.vivo or c.caido:
            return
        sg = c.estados.get("sangramento")
        if sg:
            self._perder_vida(c, sg["dano"], "Sangramento")
            sg["vezes"] -= 1
            if sg["vezes"] <= 0 and "sangramento" in c.estados:
                del c.estados["sangramento"]
        qm = c.estados.get("queimadura")
        if qm and c.vivo and not c.caido:
            cru = qm["pilhas"] * qm["pingo"]
            r = c.resistencia("fogo")
            d = max(1, round(cru * (1 - r)))
            self._perder_vida(c, d, f"Queimadura ({qm['pilhas']} × {fmt(qm['pingo'])}" + (f", fogo −{pct(r)}" if r else "") + ")",
                          fonte=qm.get("de"))
            qm["vezes"] -= 1
            if qm["vezes"] <= 0 and "queimadura" in c.estados:
                del c.estados["queimadura"]

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
            if c.lado == "inimigo" and not c.vivo or c.entra_rodada > self.rodada:
                c.vez_passou = True
                self.pos += 1
                continue
            self._inicio_do_turno(c)
            if self._conferir_fim():
                return
            if c.caido or not c.vivo:
                if c.lado == "aliado":
                    self.evento("pula", f"{c.nome} está caíd{c.a}: a vez passa.", ator=c.id)
                c.vez_passou = True
                self.pos += 1
                continue
            perde = next((e for e in ("atordoado", "aterrorizado") if e in c.estados), None)
            if perde:
                del c.estados[perde]
                txt = f"{c.nome} está {nome_estado(c, perde).lower()}: perde a vez."
                if c.preparando:
                    txt += f" {nome_preparo(c.preparando['id'], True)} se desfaz."
                    self._ameaca_fim(c.preparando, "desfeita: perdeu a vez")
                    c.preparando = None
                elif c.lado == "inimigo":
                    txt += " Não conta como turno agido: a preparação dele só atrasa."
                    self.resumo["adiamentos"].append({"rodada": self.rodada, "de": c.id, "inimigo": c.nome, "estado": perde})
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
            c.turnos += 1
            self._anotar_ultimate(c)
            self.turno_id += 1
            self.aguardando = c.id
            return

    def _anotar_ultimate(self, c):
        u = c.ultimate()
        if not u:
            return
        reg = self.resumo["ultimates"][c.id]
        m = self.motivo(c, u)
        if m is None:
            reg["turnos_disponivel"] += 1
        elif "usada" in m:
            reg["turnos_ja_usada"] += 1
        else:
            reg["turnos_sem_recurso"] += 1

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
        if h.get("ultimate") and c.ultimate_usada:
            return "Ultimate já usada nesta luta."
        if h.get("uma_vez") and acao in c.usadas:
            return "Já usada nesta luta."
        if h["alvo"] == "aliado_caido" and not any(self.c[a].caido for a in self.aliados):
            return "Ninguém caído."
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
        return [c.id]

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
        antes = c.recurso
        self._executar(c, acao, self.c[alvo])
        self.resumo["linha"].append({"rodada": self.rodada, "ator": c.id, "turno": c.turnos, "acao": acao, "alvo": alvo,
                                     "antes": antes, "depois": c.recurso})
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
        if h.get("ultimate"):
            c.ultimate_usada = True
            self.resumo["ultimates"][c.id]["uso"] = {"rodada": self.rodada, "turno": c.turnos, "id": acao}
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
            self.evento("acao", f"{c.nome} faz o Juramento (ultimate): o grupo recebe −{pct(JURAMENTO)} e não sofre "
                                f"controle até o início do próximo turno de {c.nome}.", ator=c.id)
        elif acao == "luz_restauradora":
            n = h["cura"] + c.d.get("simbolo", 0)
            self.evento("acao", f"{c.nome} chama a Luz Restauradora (ultimate).", ator=c.id)
            for a in self.vivos("aliado"):
                o = self.c[a]
                tirou = [e for e in ("queimadura", "sangramento") if o.estados.pop(e, None)]
                self._curar(c, o, n, "Luz Restauradora", tirou)
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
        elif h["alvo"] == "inimigos":
            self.evento("acao", f"{c.nome} solta {h['nome']}" + (" (ultimate)." if h.get("ultimate") else "."), ator=c.id)
            for i in list(self.vivos("inimigo")):
                self._golpe_aliado(c, self.c[i], h)
            c.estados.pop("comando", None)
        else:
            self._golpe_aliado(c, alvo, h)

    def valor_cura(self, c):
        return C.HABILIDADES["curar"]["cura"] + 2 * c.nivel + c.d.get("simbolo", 0)

    def _curar(self, c, alvo, n, rotulo, tirou=()):
        antes = alvo.vida
        alvo.vida = min(alvo.vida_max, alvo.vida + n)
        self.evento("cura", f"{c.nome}: {rotulo} em {'si' if alvo is c else alvo.nome}, +{alvo.vida - antes} de vida"
                    + (f"; sem {' nem '.join(NOME_ESTADO[e].lower() for e in tirou)}" if tirou else "") + ".",
                    ator=c.id, alvo=alvo.id)

    def _reerguer(self, c, alvo, fracao, rotulo):
        alvo.caido = False
        alvo.vida = max(1, round(alvo.vida_max * fracao))
        alvo.estados = {}
        dele = "dela" if alvo.a == "a" else "dele"
        quando = (f"age ainda nesta rodada, na posição {dele}" if not alvo.vez_passou
                  else f"a vez {dele} nesta rodada já passou: age na próxima")
        ult = " A ultimate dela continua gasta nesta luta." if alvo.ultimate_usada and alvo.a == "a" else \
            (" A ultimate dele continua gasta nesta luta." if alvo.ultimate_usada else "")
        self.evento("retorno", f"{c.nome}: {rotulo}. {alvo.nome} volta com {alvo.vida} de vida e {quando}.{ult}",
                    ator=c.id, alvo=alvo.id)

    # ---------------------------------------------------------------- a conta do golpe (a mesma na previsão e no real)
    @staticmethod
    def queima_restante(o):
        """O dano cru que a Queimadura de o ainda faria (pilhas × pingo × pingos restantes), antes da resistência."""
        q = o.estados.get("queimadura")
        return round(q["pilhas"] * q["pingo"] * q["vezes"], 2) if q else 0

    def conta_golpe(self, c, alvo, h, critico_sim, guarda=None):
        """O dano de um golpe aliado num inimigo, com crítico ou sem, e as partes da conta (ver a ordem no topo)."""
        tipo = h["tipo"]
        pot = c.potencia(h)
        dano = pot * h["mult"]
        partes = [f"{fmt(pot)} de potência ({c.origem_potencia(h)})" + (f" × {fmt(h['mult'])}" if h["mult"] != 1 else "")]
        if h.get("consome"):
            q = self.queima_restante(alvo)
            if q:
                dano += h["consome"] * q
                partes.append(f"+ {pct(h['consome'])} da Queimadura restante ({fmt(q)})")
        bonus = []
        com = c.estados.get("comando")
        if com:
            bonus.append(("comando", com["bonus"]))
        if alvo.d.get("ponto_fraco") and c.atr["percepcao"]:
            bonus.append((f"ponto fraco (PER {c.atr['percepcao']})", ponto_fraco(c.atr)))
        if h.get("contra_estado") and any(k in alvo.estados for k in ("atordoado", "queimadura")):
            bonus.append(("alvo atordoado ou queimando", h["contra_estado"]))
        if h.get("contra_vulneravel") and ("atordoado" in alvo.estados or alvo.preparando):
            bonus.append(("alvo atordoado ou preparando", h["contra_vulneravel"]))
        if h.get("contra_preparo") and alvo.preparando:
            bonus.append(("alvo preparando", h["contra_preparo"]))
        if bonus:
            dano *= 1 + sum(b for _, b in bonus)
            partes.append("bônus " + " + ".join(f"{n} {pct(b)}" for n, b in bonus))
        if critico_sim:
            dano *= CRITICO_MULT
            partes.append("crítico × 1,5")
        g = alvo.guarda if guarda is None else guarda
        if g and tipo == "fisico":
            dano *= GUARDA_MULT
            partes.append("guarda: metade")
        if tipo == "fisico":
            prot = max(0, alvo.protecao - h.get("ignora", 0))
            final = max(1, round(dano) - prot)
            if alvo.protecao:
                partes.append(f"proteção −{prot}" + (f" (ignora {h['ignora']})" if h.get("ignora") else ""))
        else:
            r = alvo.resistencia(tipo, h.get("penetra", 0.0))
            final = max(1, round(dano * (1 - r)))
            if alvo.res.get(tipo):
                partes.append(f"resistência {C.TIPOS[tipo].lower()} {pct(alvo.res[tipo])}"
                              + (f" − {pct(h['penetra'])}" if h.get("penetra") else "") + f" = −{pct(r)}")
        return final, partes

    def prever_golpe(self, c, alvo, h):
        g = alvo.guarda
        if h.get("rompe") and g:
            g = max(0, g - c.atr["forca"])
        normal, partes = self.conta_golpe(c, alvo, h, False, g)
        crit, _ = self.conta_golpe(c, alvo, h, True, g)
        return {"normal": normal, "critico": crit, "chance": round(critico(c.atr), 2), "conta": ", ".join(partes)}

    def prever_queima(self, c, alvo, h):
        """A Queimadura que o golpe deixa no alvo: pilhas depois, pingo cru, pingos e quanto cada pingo tira (já com a
        resistência ao fogo do alvo)."""
        q = alvo.estados.get("queimadura")
        pilhas = min(QUEIMA_PILHAS, (q["pilhas"] if q else 0) + 1)
        pingo = max(round(QUEIMA_FRACAO * c.potencia(h), 1), q["pingo"] if q else 0)
        por = max(1, round(pilhas * pingo * (1 - alvo.resistencia("fogo"))))
        return {"pilhas": pilhas, "pingo": pingo, "vezes": QUEIMA_VEZES, "por_pingo": por, "total": por * QUEIMA_VEZES}

    def _golpe_aliado(self, c, alvo, h):
        if h.get("rompe") and alvo.guarda:
            tira = min(alvo.guarda, c.atr["forca"])
            alvo.guarda -= tira
            self.evento("guarda", f"{c.nome} rompe {tira} da Guarda de {alvo.nome} (Força {c.atr['forca']}); "
                                  f"{'resta ' + str(alvo.guarda) if alvo.guarda else 'a guarda caiu'}.", ator=c.id, alvo=alvo.id)
        crit = self.rng.random() < critico(c.atr)
        dano, partes = self.conta_golpe(c, alvo, h, crit)
        if h["alvo"] == "inimigo":
            c.estados.pop("comando", None)
        if h.get("consome") and alvo.estados.pop("queimadura", None):
            partes.append("a Queimadura foi consumida")
        if alvo.guarda and h["tipo"] == "fisico" and not h.get("rompe"):
            alvo.guarda -= 1
            partes.append(f"−1 de Guarda (resta {alvo.guarda})")
        if h.get("atrai"):
            c.estados["atrai"] = {"marco": "inicio_turno", "de": c.id}
        self._receber(alvo, dano, f"{c.nome}: {h['nome']} em {{alvo}}", partes, ator=c.id, ja_contado=True)
        if not alvo.vivo:
            return
        if h.get("queima"):
            pingo = round(QUEIMA_FRACAO * c.potencia(h), 1)
            q = alvo.estados.get("queimadura")
            pilhas = min(QUEIMA_PILHAS, (q["pilhas"] if q else 0) + 1)
            alvo.estados["queimadura"] = {"marco": "vezes", "pilhas": pilhas, "vezes": QUEIMA_VEZES,
                                          "pingo": max(pingo, q["pingo"] if q else 0), "de": c.id}
            self.evento("efeito", f"{alvo.nome} queima: {pilhas} pilha{'s' if pilhas > 1 else ''} × {fmt(alvo.estados['queimadura']['pingo'])} "
                                  f"no início dos {QUEIMA_VEZES} próximos turnos dele (antes da resistência ao fogo).", alvo=alvo.id)
        if h.get("interrompe"):
            self._interromper(c, alvo, h)
        if h.get("desfaz_todas") and alvo.preparando and not alvo.preparando["ininterruptivel"]:
            self.evento("interrompe", f"{h['nome']} desfaz {nome_preparo(alvo.preparando['id'])} de {alvo.nome}.",
                        ator=c.id, alvo=alvo.id)
            self._ameaca_fim(alvo.preparando, "interrompida")
            alvo.preparando = None

    def _interromper(self, c, alvo, h):
        prep = alvo.preparando
        if prep and prep["ininterruptivel"]:
            self.evento("efeito", f"{nome_preparo(prep['id'], True)} de {alvo.nome} é ininterruptível: não se desfaz, "
                                  f"e {alvo.nome} está firme enquanto prepara.", alvo=alvo.id)
            return
        if prep:
            self.evento("interrompe", f"{c.nome} acerta {alvo.nome}: {nome_preparo(prep['id'])} se desfaz.",
                        ator=c.id, alvo=alvo.id)
            self._ameaca_fim(prep, "interrompida")
            alvo.preparando = None
        self._controlar(alvo, h["controle"], h["aplicacao"], c.nome)

    def chance_resistir(self, alvo, aplicacao):
        return max(0.0, round(tenacidade_de(alvo) - aplicacao, 2))

    def _controlar(self, alvo, estado, aplicacao, origem):
        lado = "aliados" if alvo.lado == "aliado" else "inimigos"
        if "juramento" in alvo.estados:
            self.evento("efeito", f"{alvo.nome} está sob o Juramento: não sofre controle.", alvo=alvo.id)
            return False
        if alvo.preparando and alvo.preparando.get("ininterruptivel"):
            self.evento("efeito", f"{alvo.nome} está firme enquanto prepara o golpe ininterruptível.", alvo=alvo.id)
            return False
        ch = self.chance_resistir(alvo, aplicacao)
        if ch > 0 and self.rng.random() < ch:
            self.resumo["controles"][lado]["resistidos"] += 1
            self.evento("efeito", f"{alvo.nome} resiste: não fica {nome_estado(alvo, estado).lower()} (chance {pct(ch)}: "
                                  f"Tenacidade {pct(tenacidade_de(alvo))} − aplicação {pct(aplicacao)}).", alvo=alvo.id)
            return False
        alvo.estados[estado] = {"marco": "proxima_vez"}
        self.resumo["controles"][lado]["sofridos"] += 1
        self.evento("efeito", f"{alvo.nome} fica {nome_estado(alvo, estado).lower()}: perde a próxima vez"
                              + (f" (resistia com {pct(ch)})." if ch else " (sem chance de resistir)."), alvo=alvo.id)
        return True

    # ---------------------------------------------------------------- receber dano
    def _redirecionar(self, alvo):
        prot = alvo.estados.get("protegido")
        if prot and alvo.lado == "aliado":
            p = self.c[prot["por"]]
            if p.vivo and not p.caido and p.id != alvo.id:
                return p
        return alvo

    def reducoes(self, o):
        return [(k, o.estados[k]["red"]) for k in ("defesa", "desafio", "juramento") if k in o.estados]

    def dano_inimigo(self, o, dano, tipo="fisico"):
        """O dano que um golpe inimigo de `dano` (do tipo) faz em o, antes do escudo, e as partes."""
        d = dano
        partes = [f"{dano} de dano {C.TIPOS[tipo].lower()}"]
        for k, red in self.reducoes(o):
            d *= 1 - red
            partes.append(f"{NOME_ESTADO[k].lower()} −{pct(red)}")
        if tipo == "fisico":
            d = max(1, round(d) - o.protecao)
            if o.protecao:
                partes.append(f"proteção −{o.protecao}")
        else:
            r = o.resistencia(tipo)
            d = max(1, round(d * (1 - r)))
            if r:
                partes.append(f"resistência {C.TIPOS[tipo].lower()} −{pct(r)}")
        return d, partes

    def _receber(self, alvo, dano, rotulo, partes, ator=None, ja_contado=False, tipo="fisico"):
        if ja_contado:
            d = dano
        else:
            quem = self._redirecionar(alvo) if alvo.lado == "aliado" else alvo
            if quem is not alvo:
                self.evento("protege", f"{quem.nome} entra na frente de {alvo.nome}.", alvo=quem.id)
            alvo = quem
            d, partes = self.dano_inimigo(alvo, dano, tipo)
        esc = alvo.estados.get("escudo")
        absorvido = 0
        if esc:
            absorvido = min(esc["resta"], d)
            esc["resta"] -= absorvido
            d -= absorvido
            if esc["resta"] <= 0:
                del alvo.estados["escudo"]
        texto = rotulo.format(alvo=alvo.nome) + f": {d} de dano" + (f" ({absorvido} no escudo)" if absorvido else "")
        self.evento("dano", texto, ator=ator, alvo=alvo.id, conta=", ".join(partes), valor=d + absorvido)
        self._perder_vida(alvo, d, None)
        return alvo

    def _perder_vida(self, alvo, d, rotulo, fonte=None):
        if rotulo:
            self.evento("dano", f"{rotulo}: {alvo.nome} perde {d}.", alvo=alvo.id, periodico=True, fonte=fonte,
                        valor=d)
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
                    self._ameaca_fim(alvo.preparando, "desfeita: inimigo caiu")
                    alvo.preparando = None
                self.evento("derrota", f"{alvo.nome} cai.", alvo=alvo.id)

    # ---------------------------------------------------------------- os inimigos
    @staticmethod
    def _na_cadencia(k, regra):
        return k == regra["primeiro"] or (k > regra["primeiro"] and (k - regra["primeiro"]) % regra["cada"] == 0)

    def _agir_inimigo(self, c):
        d = c.d
        if c.parado:
            self.evento("pula", f"{c.nome} não ataca (condição de teste).", ator=c.id)
            return
        c.turnos_agidos += 1
        k = c.turnos_agidos
        if c.preparando:
            self._resolver_preparo(c)
            return
        inv = d.get("invoca")
        if inv and self._na_cadencia(k, inv) and len([i for i in self.vivos("inimigo") if self.c[i].tipo == inv["quem"]]) < inv["max"]:
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
        if p and self._na_cadencia(k, p):
            alvo = None if p.get("area") else self._alvo_menos_vida()
            furioso = bool(p.get("furioso")) and c.vida < p["furioso"] * c.vida_max
            c.preparando = {"id": p["id"], "alvo": alvo, "anunciado": self.rodada, "ininterruptivel": furioso}
            self._ameaca_nova(c, c.preparando)
            quem = "todo o grupo" if p.get("area") else self.c[alvo].nome
            extra = " Furioso: este não pode ser interrompido, e ele fica firme até soltar." if furioso else ""
            self.evento("prepara", f"{c.nome} {p['aviso']}: prepara {p['nome']} em {quem}. Resolve na próxima vez dele."
                        + extra, ator=c.id, alvo=alvo)
            return
        alvo = self._atraente() or self.c[self.rng.choice(self.vivos("aliado"))]
        self._receber(alvo, d["dano"], f"{c.nome}: {d['golpe']} em {{alvo}}", None, ator=c.id, tipo=d.get("tipo", "fisico"))

    def alvo_do_preparo(self, prep):
        des = self._atraente()
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
        tipo = p.get("tipo", "fisico")
        if p.get("area"):
            self.evento("resolve", f"{c.nome} solta o {p['nome']}.", ator=c.id)
            total = 0
            aparada = False
            for a in self.vivos("aliado"):
                o = self.c[a]
                aparada = aparada or any(k in o.estados for k in ("defesa", "juramento", "escudo"))
                if p.get("dano"):
                    antes = o.vida
                    self._receber(o, p["dano"], f"{c.nome}: {p['nome']} em {{alvo}}", None, ator=c.id, tipo=tipo)
                    total += antes - o.vida
                if o.caido:
                    continue
                if p.get("controle"):
                    self._controlar(o, p["controle"], p["aplicacao"], c.nome)
                if p.get("queima"):
                    o.estados["queimadura"] = {"marco": "vezes", "pilhas": 1, "vezes": QUEIMA_VEZES, "pingo": p["queima"],
                                               "de": c.id}
                    self.evento("efeito", f"{o.nome} queima: {p['queima']} no início dos {QUEIMA_VEZES} próximos turnos "
                                          f"(menos a resistência ao fogo, {pct(o.resistencia('fogo'))}).", alvo=o.id)
            self._ameaca_fim(prep, "resolvida", total, aparada)
            return
        mira, recebe = self.alvo_do_preparo(prep)
        if not recebe:
            return
        aparado = recebe is not mira or any(k in recebe.estados for k in ("defesa", "desafio", "juramento", "escudo"))
        self.evento("resolve", f"{c.nome} solta {p['nome']}.", ator=c.id)
        if recebe is mira:
            recebeu = self._receber(recebe, p["dano"], f"{c.nome}: {p['nome']} em {{alvo}}", None, ator=c.id, tipo=tipo)
        else:
            self.evento("protege", f"{recebe.nome} entra na frente de {mira.nome}.", alvo=recebe.id)
            d, partes = self.dano_inimigo(recebe, p["dano"], tipo)
            recebeu = self._receber(recebe, d, f"{c.nome}: {p['nome']} em {{alvo}}", partes, ator=c.id, ja_contado=True)
        dano = next((e for e in reversed(self.eventos) if e["tipo"] == "dano"), {}).get("texto", "")
        self._ameaca_fim(prep, "resolvida", int(dano.split(": ")[-1].split(" ")[0]) if ": " in dano else None, aparado)
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

    # ---------------------------------------------------------------- previsões e a ficha
    def prever_ameaca(self, c):
        p = c.d["preparo"]
        tipo = p.get("tipo", "fisico")
        if p.get("area"):
            alvos = []
            for a in self.vivos("aliado"):
                o = self.c[a]
                x = {"id": a, "nome": o.nome}
                if p.get("dano"):
                    d, _ = self.dano_inimigo(o, p["dano"], tipo)
                    esc = o.estados.get("escudo")
                    x["agora"] = max(0, d - (esc["resta"] if esc else 0))
                if p.get("controle"):
                    x.update(self._previsao_controle(o, p))
                if p.get("queima"):
                    x["queima"] = max(1, round(p["queima"] * (1 - o.resistencia("fogo"))))
                alvos.append(x)
            return {"alvos": alvos, "tipo": C.TIPOS[tipo]}
        mira, recebe = self.alvo_do_preparo(c.preparando)
        if not recebe:
            return {}
        d, _ = self.dano_inimigo(recebe, p["dano"], tipo)
        esc = recebe.estados.get("escudo")
        agora = max(0, d - (esc["resta"] if esc else 0))
        se_def = None
        if mira is recebe and "defesa" not in mira.estados:
            mira.estados["defesa"] = {"red": DEFESA}
            dd, _ = self.dano_inimigo(mira, p["dano"], tipo)
            del mira.estados["defesa"]
            se_def = max(0, dd - (esc["resta"] if esc else 0))
        r = {"mira": mira.id, "quem": recebe.id, "agora": agora, "se_defender": se_def, "tipo": C.TIPOS[tipo]}
        if p.get("controle"):
            r.update(self._previsao_controle(recebe, p))
        if p.get("sangra"):
            r["sangra"] = max(1, round(p["sangra"] * (1 - corporal(recebe.atr))))
        return r

    def _previsao_controle(self, o, p):
        if "juramento" in o.estados:
            return {"controle": p["controle"], "resiste": 1.0, "juramento": True}
        return {"controle": p["controle"], "resiste": self.chance_resistir(o, p["aplicacao"])}

    def estado_ultimate(self, c):
        u = c.ultimate()
        if not u:
            return None
        m = self.motivo(c, u)
        est = "disponivel" if m is None else "usada" if "usada" in m else "recurso" if "insuficiente" in m else "alvo"
        return {"id": u, "nome": C.HABILIDADES[u]["nome"], "custo": C.HABILIDADES[u]["custo"], "estado": est, "motivo": m}

    def derivados(self, c):
        a = c.atr
        lin = []

        def L(chave, nome, valor, como):
            lin.append({"id": chave, "nome": nome, "valor": valor, "como": como})
        L("vida", "Vida máxima", c.vida_max,
          f"{c.d['vida_base']} da classe + {VIDA_POR_NIVEL} × nível {c.nivel} + {VIDA_POR_PONTO} × CON {a['constituicao']}")
        L("iniciativa", "Posição na ordem", self.ordem.index(c.id) + 1, f"AGI {a['agilidade']} (fixa a luta inteira)")
        L("recurso_max", f"{c.recurso_nome} máximo", c.recurso_max,
          f"{C.RECURSO_BASE} da classe + {C.RECURSO_NIVEL} × nível {c.nivel} + {C.RECURSO_VONTADE} × VON {a['vontade']}; começa cheio")
        L("regeneracao", "Regeneração", f"+{C.RECURSO_TURNO} por turno", f"e +{C.RECURSO_BASICO} no ataque básico (sem atributo)")
        L("fisico", "Potência física (Atacar)", c.potencia(C.HABILIDADES["atacar"]), c.origem_potencia(C.HABILIDADES["atacar"]))
        arc = {"base": "foco", "escala": {"intelecto": 1.0}}
        L("arcano", "Potência arcana e de fogo", c.potencia(arc), c.origem_potencia(arc))
        L("critico", "Crítico", pct(critico(a)), f"2% × PER {a['percepcao']} (até 25%); dano × 1,5")
        L("ponto_fraco", "Contra ponto fraco", f"+{pct(ponto_fraco(a))}", f"3% × PER {a['percepcao']} (até 30%)")
        L("protecao", "Proteção", c.protecao, "da armadura: subtrai de cada golpe físico")
        for t in ("fogo", "arcano"):
            r = c.resistencia(t)
            if c.equip:
                peca = C.EQUIPAMENTO["manto"][c.equip["manto"]]["nome"]
                como = f"do {peca} (teto {pct(C.RESISTENCIA_TETO)})" if r else f"o {peca} não dá; outro manto daria"
            else:
                como = "nenhuma peça de resistência"
            L(f"res_{t}", f"Resistência {C.TIPOS[t].lower()}", pct(r), como)
        L("corporal", "Resistência corporal", f"−{pct(corporal(a))}", f"4% × CON {a['constituicao']} no Sangramento (até 40%)")
        L("tenacidade", "Tenacidade", pct(tenacidade_de(c)), f"4% × VON {a['vontade']} (até 40%): chance de resistir a controle")
        L("defesa", "Defender reduz", pct(DEFESA), "da regra (sem atributo)")
        u = c.ultimate()
        L("ultimate", "Ultimate", C.HABILIDADES[u]["nome"] if u else "sem ultimate equipada",
          (f"uma vez por luta, {C.HABILIDADES[u]['custo']} de {c.recurso_nome}, desde o início" if u else "nenhuma no kit"))
        if "curar" in c.kit:
            L("cura", "Curar", self.valor_cura(c), f"{C.HABILIDADES['curar']['cura']} + 2 × nível + símbolo {c.d.get('simbolo', 0)}")
        return lin

    def tabela_dano(self, c, alvo):
        lin = []
        for hid in c.acoes():
            h = C.HABILIDADES[hid]
            if "mult" in h:
                p = self.prever_golpe(c, alvo, h)
                lin.append({"id": hid, "nome": h["nome"], "custo": self.custo(c, hid), "tipo": C.TIPOS[h["tipo"]],
                            "ultimate": bool(h.get("ultimate")), **p})
        return lin

    # ---------------------------------------------------------------- o estado para a tela
    def estado(self):
        def comb(i):
            o = self.c[i]
            e = {"id": i, "nome": o.nome, "lado": o.lado, "papel": o.papel, "a": o.a, "retrato": o.retrato,
                 "vida": o.vida, "vida_max": o.vida_max, "caido": o.caido, "vivo": o.vivo, "guarda": o.guarda,
                 "guarda_max": o.d.get("guarda", 0) if o.guarda or o.d.get("guarda") else 0, "protecao": o.protecao,
                 "ponto_fraco": o.d.get("ponto_fraco"), "tenacidade": round(tenacidade_de(o), 2),
                 "res": {C.TIPOS[t]: round(v, 2) for t, v in o.res.items() if v},
                 "estados": [{"id": k, "nome": nome_estado(o, k), "ate": self._marco(o, k, v),
                              **({"resta": v["resta"]} if "resta" in v else {}),
                              **({"pilhas": v["pilhas"]} if "pilhas" in v else {})}
                             for k, v in o.estados.items()],
                 "entra_rodada": o.entra_rodada}
            if o.lado == "aliado":
                e.update(recurso=o.recurso, recurso_max=o.recurso_max, recurso_nome=o.recurso_nome, atributos=o.atr,
                         derivados=self.derivados(o), ultimate=self.estado_ultimate(o))
            else:
                e.update(golpe_tipo=C.TIPOS[o.d.get("tipo", "fisico")])
            return e
        ameacas = []
        for i in self.inimigos:
            o = self.c[i]
            if o.vivo and o.preparando:
                p = o.d["preparo"]
                a = {"de": i, "nome": p["nome"], "area": bool(p.get("area")), "anunciado": o.preparando["anunciado"],
                     "ininterruptivel": o.preparando["ininterruptivel"], "dano": p.get("dano"),
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
                     "basico": bool(h.get("basico")), "ultimate": bool(h.get("ultimate")), "tier": h.get("tier"),
                     "info": descrever(h)}
                if "mult" in h:
                    x["previsoes"] = {i: self.prever_golpe(ativo, self.c[i], h) for i in self.vivos("inimigo")}
                if h.get("queima"):
                    x["queima"] = {i: self.prever_queima(ativo, self.c[i], h) for i in self.vivos("inimigo")}
                if h.get("controle"):
                    x["resiste"] = {i: self.chance_resistir(self.c[i], h["aplicacao"]) for i in self.vivos("inimigo")}
                if hid == "curar":
                    x["cura"] = self.valor_cura(ativo)
                acoes.append(x)
            for iid, n in self.consumiveis.items():
                it = C.CONSUMIVEIS[iid]
                acoes.append({"id": "item:" + iid, "nome": it["nome"], "desc": it["desc"], "qtd": n, "icone": it["icone"],
                              "motivo": self.motivo(ativo, "item:" + iid), "alvo": it["alvo"],
                              "alvos": self.alvos(ativo, "item:" + iid), "item": True, "basico": True})
        h = self.c["heroi"]
        return {"versao": 3, "encontro": self.encontro, "nome": self.cfg["nome"], "objetivo": self.cfg["objetivo"],
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
                "resumo": self.resumo}

    def _marco(self, o, k, v):
        m = v.get("marco")
        if m == "inicio_turno":
            return f"até o início do próximo turno de {self.c[v['de']].nome}"
        if m == "fim_rodada":
            return f"até o fim da rodada {v['rodada']}"
        if m == "proxima_vez":
            return "perde a próxima vez"
        if m == "vezes" and k == "queimadura":
            return f"{v['pilhas']} × {fmt(v['pingo'])} no início de {v['vezes']} turno{'s' if v['vezes'] > 1 else ''}"
        if m == "vezes":
            return f"−{v['dano']} no início de {v['vezes']} {'turno' if v['vezes'] == 1 else 'turnos'}"
        return ""


NOME_ESTADO = {"defesa": "Defendendo", "protegido": "Protegido", "protegendo": "Protegendo", "desafio": "Desafiando",
               "atrai": "Atraindo os golpes", "juramento": "Juramento", "atordoado": "Atordoado",
               "aterrorizado": "Aterrorizado", "comando": "Comandado", "escudo": "Escudo de Luz",
               "sangramento": "Sangrando", "queimadura": "Queimando"}
NOME_PREPARO = {"bote": "O Bote", "esmagador": "O Golpe Esmagador", "terror": "O Grito de Terror",
                "sopro": "O Sopro de Brasa"}


def nome_estado(o, k):
    n = NOME_ESTADO[k]
    return n[:-1] + "a" if o.a == "a" and n.endswith("do") and not n.endswith("ndo") else n


def nome_preparo(pid, maiuscula=False):
    n = NOME_PREPARO[pid]
    return n if maiuscula else n[0].lower() + n[1:]


# ---------------------------------------------------------------- a ficha das construções (fora da luta)
ALVOS_REFERENCIA = ("bruto", "xama", "cao")
DANO_HEROI = ("atacar", "corte", "golpe_pesado", "escudo_golpe", "avanco", "brasa", "chuva", "lamina", "combustao",
              "furia", "tempestade", "conflagracao")


def _alvo_ref(tipo):
    o = Combatente(tipo + "#ref", "inimigo", C.INIMIGOS[tipo])
    o.tipo = tipo
    return o


def combo_tabela(cb, h, alvo):
    """A combinação de queimadura no mesmo alvo parado: separadas ou em sequência (dano total, turnos, custo). Os
    pingos acontecem no turno do alvo, entre os turnos de Jean."""
    H = C.HABILIDADES

    def golpe(hid):
        d, _ = cb.conta_golpe(h, alvo, H[hid], False)
        if H[hid].get("consome"):
            alvo.estados.pop("queimadura", None)
        if H[hid].get("queima"):
            q = alvo.estados.get("queimadura")
            alvo.estados["queimadura"] = {"marco": "vezes", "pilhas": min(QUEIMA_PILHAS, (q["pilhas"] if q else 0) + 1),
                                          "vezes": QUEIMA_VEZES, "pingo": round(QUEIMA_FRACAO * h.potencia(H[hid]), 1)}
        return d

    def pingo():
        q = alvo.estados.get("queimadura")
        if not q:
            return 0
        d = max(1, round(q["pilhas"] * q["pingo"] * (1 - alvo.resistencia("fogo"))))
        q["vezes"] -= 1
        if q["vezes"] <= 0:
            del alvo.estados["queimadura"]
        return d

    linhas = []
    for rot, seq in (("Brasa e esperar os 3 pingos", ["brasa", None, None]),
                     ("Combustão sozinha", ["combustao"]),
                     ("Brasa → Combustão", ["brasa", "combustao"]),
                     ("Brasa → Brasa → Combustão", ["brasa", "brasa", "combustao"]),
                     ("Lâmina Rúnica ×2 (para comparar)", ["lamina", "lamina"])):
        alvo.estados = {}
        total, custo = 0, 0
        for i, hid in enumerate(seq):
            if hid:
                total += golpe(hid)
                custo += H[hid]["custo"]
            if i < len(seq) - 1 or not hid:
                total += pingo()
        while alvo.estados.get("queimadura"):  # o que sobra depois ainda pinga
            total += pingo()
        linhas.append({"rotulo": rot, "turnos": len(seq), "custo": custo, "dano": total})
    alvo.estados = {}
    return linhas


def ficha(atributos, kit, equip=None, presenca=None, build="livre"):
    """O que a construção faz, para escolher e comparar: atributos, derivados, o dano previsto de cada golpe nos três
    alvos de referência (Bruto: proteção 2 e ponto fraco; Xamã: 30% arcano; Cão: 60% fogo), custos, o kit e a
    combinação de queimadura. Usa as regras de verdade."""
    cb = Combate("e2", atributos=atributos, kit=kit, equip=equip, presenca=presenca, soma_exata=False)
    h = cb.c["heroi"]
    der = cb.derivados(h)
    next(d for d in der if d["id"] == "iniciativa")["como"] += " · no encontro 2"
    alvos = {t: _alvo_ref(t) for t in ALVOS_REFERENCIA}
    dano = []
    for hid in h.acoes():
        hh = C.HABILIDADES[hid]
        if "mult" in hh:
            dano.append({"id": hid, "nome": hh["nome"], "custo": hh["custo"], "info": descrever(hh),
                         "ultimate": bool(hh.get("ultimate")),
                         "alvos": {t: cb.prever_golpe(h, a, hh) for t, a in alvos.items()}})
    tem_combo = "brasa" in h.kit or "combustao" in h.kit
    return {"build": build, "atributos": h.atr, "presenca": cb.presenca, "kit": h.kit, "equip": h.equip,
            "pontos_kit": pontos_kit(h.kit), "derivados": der, "dano": dano,
            "alvos": {t: {"nome": a.nome, "protecao": a.protecao, "res": {C.TIPOS[k]: v for k, v in a.res.items() if v},
                          "ponto_fraco": a.d.get("ponto_fraco")} for t, a in alvos.items()},
            "ultimate": cb.estado_ultimate(h),
            "combo": {t: combo_tabela(cb, h, alvos[t]) for t in ("bruto", "cao")} if tem_combo else None,
            "custos": [{"id": k, "nome": C.HABILIDADES[k]["nome"], "custo": C.HABILIDADES[k]["custo"],
                        "pontos": C.PONTOS_TIER[C.HABILIDADES[k]["tier"]], "tier": C.HABILIDADES[k]["tier"]} for k in h.kit],
            "ordem_e2": [cb.c[i].nome for i in cb.ordem]}


def comparar_builds(equip=None):
    colunas = []
    for bid, b in C.BUILDS.items():
        f = ficha(b["atributos"], b["kit"], equip, build=bid)
        cb = Combate("e2", atributos=b["atributos"], kit=[], equip=equip)
        h = cb.c["heroi"]
        alvos = {t: _alvo_ref(t) for t in ALVOS_REFERENCIA}
        f["dano_todos"] = [{"id": k, "nome": C.HABILIDADES[k]["nome"],
                            "alvos": {t: cb.prever_golpe(h, a, C.HABILIDADES[k]) for t, a in alvos.items()}}
                           for k in DANO_HEROI]
        f.update(nome=b["nome"], frase=b["frase"], ganha=b["ganha"], abre_mao=b["abre_mao"])
        colunas.append(f)
    return {"colunas": colunas}


def comparar_equipamento(atributos, kit, peca):
    """A mesma construção, nível e alvo, mudando uma peça: arma e foco no dano previsto (no Bruto); o manto no dano
    recebido do Sopro de Brasa e da Garra sombria."""
    linhas = []
    for oid, o in C.EQUIPAMENTO[peca].items():
        equip = dict(C.EQUIPAMENTO_PADRAO, **{peca: oid})
        cb = Combate("e2", atributos=atributos, kit=kit, equip=equip, soma_exata=False)
        h = cb.c["heroi"]
        if peca == "manto":
            sopro = C.INIMIGOS["cao"]["preparo"]
            d1, _ = cb.dano_inimigo(h, sopro["dano"], "fogo")
            d2, _ = cb.dano_inimigo(h, C.INIMIGOS["xama"]["dano"], "arcano")
            linhas.append({"id": oid, "nome": o["nome"], "valor": o["res"], "recebido": [
                {"nome": "Sopro de Brasa (16 fogo)", "dano": d1},
                {"nome": "Queimadura do Sopro (4 por pingo)", "dano": max(1, round(sopro["queima"] * (1 - h.resistencia("fogo"))))},
                {"nome": "Garra sombria (12 arcano)", "dano": d2}]})
            continue
        alvo = _alvo_ref("bruto")
        dano = [{"id": k, "nome": C.HABILIDADES[k]["nome"], "normal": cb.prever_golpe(h, alvo, C.HABILIDADES[k])["normal"]}
                for k in h.acoes() if "mult" in C.HABILIDADES[k] and C.HABILIDADES[k].get("base") == peca]
        linhas.append({"id": oid, "nome": o["nome"], "valor": o["valor"], "dano": dano})
    return {"peca": peca, "linhas": linhas}


def situacao(atributos, presenca, escolha=None, ajuda=False):
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


# ---------------------------------------------------------------- a comparação do fogo (lutas de verdade, alvos parados)
SEQUENCIAS_FOGO = (
    ("um", "t6", "Brasa → Combustão", ["brasa", "combustao"]),
    ("um", "t6", "Brasa → Brasa → Combustão", ["brasa", "brasa", "combustao"]),
    ("um", "t6", "Chuva de Brasas → Combustão (área num alvo só)", ["chuva", "combustao"]),
    ("um", "t6", "Chuva de Brasas e esperar", ["chuva"]),
    ("grupo", "t7", "Chuva de Brasas → Conflagração", ["chuva", "conflagracao"]),
    ("grupo", "t7", "Brasa em cada um (3) → Conflagração", ["brasa@1", "brasa@2", "brasa@3", "conflagracao"]),
    ("grupo", "t7", "Chuva de Brasas e esperar", ["chuva"]),
    ("resistente", "t8", "Chuva de Brasas → Conflagração", ["chuva", "conflagracao"]),
    ("resistente", "t8", "Brasa → Combustão", ["brasa", "combustao"]),
)


def simular_fogo(atributos, kit, encontro, seq, equip=None):
    """Joga a sequência de Jean num teste de alvos parados (os companheiros se defendem) e soma, pelos eventos, o dano
    direto de Jean e o periódico das Queimaduras dele até a última apagar ou ser consumida."""
    cb = Combate(encontro, atributos=atributos, kit=kit, equip=equip, soma_exata=False)
    h = cb.c["heroi"]
    inicio, n0 = h.recurso, len(cb.eventos)
    alvos = list(cb.inimigos)
    acoes = 0
    for passo in seq:
        while cb.aguardando != "heroi":
            cb.agir(cb.turno_id, "defender", cb.aguardando)
        hid, _, k = passo.partition("@")
        alvo = alvos[int(k) - 1] if k else (alvos[0] if C.HABILIDADES[hid]["alvo"] == "inimigo" else None)
        r = cb.agir(cb.turno_id, hid, alvo)
        assert r["ok"], (passo, r)
        acoes += 1
    gasto = sum(C.HABILIDADES[p.partition("@")[0]]["custo"] for p in seq)
    for _ in range(40):  # deixa as Queimaduras restantes pingarem até o fim
        if not any("queimadura" in cb.c[i].estados for i in alvos):
            break
        cb.agir(cb.turno_id, "defender", cb.aguardando)
    ev = cb.eventos[n0:]
    direto = sum(e["valor"] for e in ev if e["tipo"] == "dano" and e.get("ator") == "heroi" and e.get("alvo") in alvos)
    periodico = sum(e["valor"] for e in ev if e.get("periodico") and e.get("fonte") == "heroi" and e.get("alvo") in alvos)
    return {"acoes": acoes, "custo": gasto, "recurso_antes": inicio, "direto": direto, "periodico": periodico,
            "total": direto + periodico, "alvos": len(alvos)}


def comparar_fogo(atributos, kit, equip=None):
    linhas = []
    for grupo, enc, rotulo, seq in SEQUENCIAS_FOGO:
        if not all(p.partition("@")[0] in kit for p in seq):
            continue
        linhas.append({"grupo": grupo, "encontro": enc, "rotulo": rotulo, **simular_fogo(atributos, kit, enc, seq, equip)})
    return linhas
