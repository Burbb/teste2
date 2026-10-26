"""As regras do protótipo de combate e atributos (25/10/2026; nada no jogo). Um combate por turnos individuais
intercalados, com a ordem calculada uma vez pela Agilidade e preservada a batalha inteira.

Os relógios (dois nomes, nunca "turno" para os dois):
- **turno**: a vez de um combatente. Começa (expira o que dura "até o início do próximo turno" dele, o sangramento
  pinga), e então ele age, perde a vez (atordoado, aterrorizado) ou é pulado (caído, ainda não entrou).
- **rodada**: a ordem inteira, uma vez cada um, inclusive quem perdeu a vez. No fim dela expira o que dura "até o fim
  da rodada N".

Os marcos de cada estado:
- defesa, proteção (o protegido e quem protege): até o início do próximo turno do portador (da proteção: o de quem
  protege);
- abalado: vale no próximo turno do portador e acaba no fim dele;
- atordoado, aterrorizado: a próxima vez do portador é perdida (gastos ao começar o turno dele);
- escudo de luz, marca, comando: até o fim da rodada seguinte à aplicação (ou gastos antes, no golpe);
- sangramento: pinga no início de cada turno do portador, 2 vezes (1 com Constituição 5 ou mais).

Queda e retorno: um aliado a 0 de vida fica caído (pulado na ordem; não morre). Volta só por Reerguer ou pela Pena de
Fênix, na mesma posição: se a vez dele nesta rodada ainda não passou, age nela; se já passou (pulada), só na próxima.
Ninguém recupera a vez perdida. O protagonista caído encerra a luta em derrota.

Invocações: entram no fim da ordem e agem a partir da rodada seguinte, sem mexer na posição de ninguém."""
import random

from . import conteudo as C


def _dist_valida(atr):
    if set(atr) != set(C.ATRIBUTOS):
        return "Faltam atributos."
    if any(not (C.ATRIBUTO_MIN <= v <= C.ATRIBUTO_MAX) for v in atr.values()):
        return f"Cada atributo vai de {C.ATRIBUTO_MIN} a {C.ATRIBUTO_MAX}."
    if sum(atr.values()) != C.PONTOS_PROTAGONISTA:
        return f"A soma tem de ser {C.PONTOS_PROTAGONISTA} (está {sum(atr.values())})."
    return None


# ---------------------------------------------------------------- as fórmulas (provisórias)
def custo_mult(atr):
    """Intelecto: −5% de custo por ponto acima de 3, até −25%. Abaixo de 3 não encarece."""
    return max(0.75, 1 - 0.05 * max(0, atr["intelecto"] - 3))


def critico(atr):
    """Percepção: 5% de crítico, +4% por ponto acima de 3 (de 0% a 25%)."""
    return max(0.0, min(0.25, 0.05 + 0.04 * (atr["percepcao"] - 3)))


def reducao_defesa(atr):
    """Vontade: Defender reduz 40%, +5% por ponto acima de 3 (de 25% a 65%)."""
    return max(0.25, min(0.65, 0.40 + 0.05 * (atr["vontade"] - 3)))


def bonus_comando(atr):
    """Presença: o Grito de Comando dá +15%, +5% por ponto acima de 3 (de 5% a 40%)."""
    return max(0.05, min(0.40, 0.15 + 0.05 * (atr["presenca"] - 3)))


LIMIAR = 5  # a partir de 5: Força resiste ao atordoamento físico; Vontade ao terror; Percepção vê o ponto fraco;
            # Constituição encurta o sangramento
PONTO_FRACO = 0.25
ABALADO = 0.25
CRITICO_MULT = 1.5
GUARDA_MULT = 0.5


class Combatente:
    def __init__(self, cid, lado, d, atributos=None):
        self.id, self.lado, self.d = cid, lado, d
        self.nome, self.retrato = d["nome"], d["retrato"]
        self.papel = d.get("papel", "inimigo")
        self.a = "a" if d.get("feminino") else "o"  # a concordância: atordoad{a}, caíd{a}
        self.estados = {}
        self.caido = False
        self.usadas = set()
        self.entra_rodada = 1
        self.preparando = None
        self.vez_passou = False  # nesta rodada, a posição dele já passou
        if lado == "aliado":
            self.atr = dict(atributos or d["atributos"])
            self.nivel = d["nivel"]
            self.vida_max = d["vida_base"] + 6 * self.nivel + 5 * (self.atr["constituicao"] - 3)
            self.recurso_nome, self.recurso_max = d["recurso"], d["recurso_max"]
            self.recurso = d["recurso_inicio"]
            self.arma, self.protecao, self.kit = d["arma"], d["protecao"], list(d["kit"])
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

    def potencia(self):
        """A potência do golpe: a arma e o nível (não os atributos)."""
        return self.arma + self.nivel


class Combate:
    def __init__(self, encontro, distribuicao="A", atributos=None):
        self.cfg = C.ENCONTROS[encontro]
        self.encontro = encontro
        self.rng = random.Random(self.cfg["semente"])
        atr_heroi = dict(atributos) if atributos else dict(C.DISTRIBUICOES[distribuicao]["atributos"])
        erro = _dist_valida(atr_heroi)
        if erro:
            raise ValueError(erro)
        self.distribuicao = distribuicao if not atributos else "livre"
        self.c = {}
        self.aliados = ["heroi", "odete", "morel"]
        self.c["heroi"] = Combatente("heroi", "aliado", C.GRUPO["heroi"], atr_heroi)
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
        self.resumo = {"dano_recebido": {a: 0 for a in self.aliados}, "quedas": 0, "acoes": {}, "preparos": 0,
                       "preparos_resolvidos": 0, "preparos_desfeitos": 0}
        self._aplicar_inicio(self.cfg.get("inicio", {}))
        # a ordem: calculada uma vez, pela Agilidade (desempate: Percepção, depois aliado antes de inimigo, depois a
        # ordem de entrada). Não muda mais.
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
            if "recurso" in cond:
                c.recurso = cond["recurso"]
            if "vida" in cond:
                c.vida = cond["vida"]
            if cond.get("preparando"):
                p = c.d["preparo"]
                c.preparando = {"id": p["id"], "alvo": self._alvo_menos_vida(), "anunciado": 0}

    def _alvo_menos_vida(self):
        vivos = self.vivos("aliado")
        return min(vivos, key=lambda i: (self.c[i].vida / self.c[i].vida_max, self.aliados.index(i))) if vivos else None

    # ---------------------------------------------------------------- o relógio
    def _inicio_do_turno(self, c):
        """O que expira quando a vez de c começa (em todos: o que é "até o início do próximo turno de c")."""
        for o in self.c.values():
            for e in list(o.estados):
                st = o.estados[e]
                if st.get("marco") == "inicio_turno" and st.get("de") == c.id:
                    del o.estados[e]
                    if e in ("defesa", "protegido", "protegendo"):
                        self.evento("expira", f"{o.nome}: {nome_estado(o, e)} acabou (início do turno de {c.nome}).", alvo=o.id)
        sg = c.estados.get("sangramento")
        if sg and c.vivo and not c.caido:
            self._perder_vida(c, 4, "Sangramento")
            sg["vezes"] -= 1
            if sg["vezes"] <= 0:
                del c.estados["sangramento"]

    def _fim_do_turno(self, c):
        """O que vale só no próximo turno de c (abalado) acaba quando esse turno termina, agindo ou não."""
        for e in [e for e, st in c.estados.items() if st.get("marco") == "fim_turno" and st.get("de") == c.id]:
            del c.estados[e]

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
            if c.lado == "inimigo" and not c.vivo:  # derrotado: some da ordem (a posição dos outros não muda)
                c.vez_passou = True
                self.pos += 1
                continue
            if c.entra_rodada > self.rodada:  # invocado nesta rodada: só age a partir da próxima
                c.vez_passou = True
                self.pos += 1
                continue
            self._inicio_do_turno(c)
            if self._conferir_fim():
                return
            if c.caido:
                self.evento("pula", f"{c.nome} está caíd{c.a}: a vez passa.", ator=c.id)
                self._fim_do_turno(c)
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
                self._fim_do_turno(c)
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
            # a vez de um aliado: espera a escolha do jogador
            self.turno_id += 1
            self.aguardando = c.id
            return

    def _conferir_fim(self):
        if self.c["heroi"].caido:
            self.fim = "derrota"
            self.evento("fim", "Jean caiu. Derrota.")
        elif not self.vivos("inimigo"):
            self.fim = "vitoria"
            self.evento("fim", f"Vitória na rodada {self.rodada}.")
        if self.fim:
            self.aguardando = None
            self.resumo["rodadas"] = self.rodada
        return bool(self.fim)

    # ---------------------------------------------------------------- as ações dos aliados
    def custo(self, c, hid):
        h = C.HABILIDADES[hid]
        return 0 if not h["custo"] else max(1, round(h["custo"] * custo_mult(c.atr)))

    def motivo(self, c, acao):
        """Por que a ação não dá agora (None: dá). acao: um id de habilidade ou "item:<id>"."""
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
        if c.recurso < self.custo(c, acao):
            return f"{c.recurso_nome} insuficiente ({self.custo(c, acao)})."
        if acao == "proteger" and len(self.vivos("aliado")) < 2:
            return "Ninguém para proteger."
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
        if acao.startswith("item:") and acao[5:] not in C.CONSUMIVEIS or not acao.startswith("item:") and acao not in c.kit:
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
        self._fim_do_turno(c)
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
        c.recurso = max(0, min(c.recurso_max, c.recurso - self.custo(c, acao) + h.get("ganha", 0)))
        if h.get("uma_vez"):
            c.usadas.add(acao)
        if acao == "defender":
            red = reducao_defesa(c.atr)
            c.estados["defesa"] = {"marco": "inicio_turno", "de": c.id, "red": red}
            self.evento("acao", f"{c.nome} se defende: −{round(red * 100)}% de dano até o início do próximo turno.", ator=c.id)
        elif acao == "proteger":
            alvo.estados["protegido"] = {"marco": "inicio_turno", "de": c.id, "por": c.id}
            c.estados["protegendo"] = {"marco": "inicio_turno", "de": c.id, "quem": alvo.id}
            self.evento("acao", f"{c.nome} protege {alvo.nome}: os golpes nele vêm para {c.nome} até o início do próximo "
                                f"turno de {c.nome}.", ator=c.id, alvo=alvo.id)
        elif acao == "comando":
            b = bonus_comando(c.atr)
            alvo.estados["comando"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "bonus": b}
            tirou = [e for e in ("aterrorizado", "abalado") if alvo.estados.pop(e, None)]
            self.evento("acao", f"{c.nome} comanda {alvo.nome}: o próximo golpe +{round(b * 100)}%"
                                + (f"; {alvo.nome} não está mais {' nem '.join(nome_estado(alvo, e).lower() for e in tirou)}" if tirou else "") + ".",
                        ator=c.id, alvo=alvo.id)
        elif acao == "curar":
            self._curar(c, alvo, h["cura"], h["nome"])
        elif acao == "escudo_luz":
            alvo.estados["escudo"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "resta": h["escudo"]}
            self.evento("acao", f"{c.nome} põe o Escudo de Luz em {'si' if alvo is c else alvo.nome} (absorve {h['escudo']} até o fim da rodada "
                                f"{self.rodada + 1}).", ator=c.id, alvo=alvo.id)
        elif acao == "reerguer":
            self._reerguer(c, alvo, h["volta"], h["nome"])
        elif acao == "marcar":
            alvo.estados["marca"] = {"marco": "fim_rodada", "rodada": self.rodada + 1, "de": c.id, "bonus": h["marca"]}
            self.evento("acao", f"{c.nome} marca {alvo.nome}: o próximo golpe de outro aliado +{round(h['marca'] * 100)}%.",
                        ator=c.id, alvo=alvo.id)
        else:  # golpes
            self._golpe_aliado(c, alvo, h)

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

    def _golpe_aliado(self, c, alvo, h):
        dano = c.potencia() * h["mult"]
        partes = [f"{c.potencia()} de potência" + (f" × {str(h['mult']).replace('.', ',')}" if h["mult"] != 1 else "")]
        if h.get("rompe") and alvo.guarda:
            tira = min(alvo.guarda, c.atr["forca"])
            alvo.guarda -= tira
            self.evento("guarda", f"{c.nome} rompe {tira} da Guarda de {alvo.nome} (Força {c.atr['forca']}); "
                                  f"{'resta ' + str(alvo.guarda) if alvo.guarda else 'a guarda caiu'}.", ator=c.id, alvo=alvo.id)
        com = c.estados.pop("comando", None)
        if com:
            dano *= 1 + com["bonus"]
            partes.append(f"comando +{round(com['bonus'] * 100)}%")
        mk = alvo.estados.get("marca")
        if mk and mk["de"] != c.id:
            del alvo.estados["marca"]
            dano *= 1 + mk["bonus"]
            partes.append(f"marca +{round(mk['bonus'] * 100)}%")
        if "abalado" in c.estados:
            dano *= 1 - ABALADO
            partes.append(f"abalado −{round(ABALADO * 100)}%")
        if alvo.d.get("ponto_fraco") and c.atr["percepcao"] >= LIMIAR:
            dano *= 1 + PONTO_FRACO
            partes.append(f"ponto fraco +{round(PONTO_FRACO * 100)}%")
        if self.rng.random() < critico(c.atr):
            dano *= CRITICO_MULT
            partes.append("crítico ×1,5")
        if alvo.guarda:
            dano *= GUARDA_MULT
            if not h.get("rompe"):  # o golpe comum também gasta a guarda, de 1 em 1
                alvo.guarda -= 1
            partes.append("guarda: metade" + ("" if h.get("rompe") else f", −1 de Guarda (resta {alvo.guarda})"))
        rot = h["nome"]
        if h.get("interrompe"):
            if alvo.preparando:
                prep = NOME_PREPARO[alvo.preparando['id']]
                self.evento("interrompe", f"{c.nome} acerta o joelho de {alvo.nome}: {prep[0].lower() + prep[1:]} se desfaz.",
                            ator=c.id, alvo=alvo.id)
                alvo.preparando = None
                self.resumo["preparos_desfeitos"] += 1
            if alvo.d.get("firme"):
                self.evento("efeito", f"{alvo.nome} é firme: não fica atordoado.", alvo=alvo.id)
            else:
                alvo.estados["atordoado"] = {"marco": "proxima_vez"}
        self._receber(alvo, dano, f"{c.nome}: {rot} em {{alvo}}", partes, ator=c.id)

    # ---------------------------------------------------------------- receber dano
    def _receber(self, alvo, dano, rotulo, partes, ator=None):
        prot = alvo.estados.get("protegido")
        if prot and alvo.lado == "aliado":
            p = self.c[prot["por"]]
            if p.vivo and not p.caido and p.id != alvo.id:
                self.evento("protege", f"{p.nome} entra na frente de {alvo.nome}.", alvo=p.id)
                alvo = p
        d = dano
        df = alvo.estados.get("defesa")
        if df:
            d *= 1 - df["red"]
            partes = partes + [f"defesa −{round(df['red'] * 100)}%"]
        d = max(1, round(d) - alvo.protecao)
        if alvo.protecao:
            partes = partes + [f"proteção −{alvo.protecao}"]
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
                    self.evento("efeito", f"{NOME_PREPARO[alvo.preparando['id']]} de {alvo.nome} não sai.", alvo=alvo.id)
                    alvo.preparando = None
                    self.resumo["preparos_desfeitos"] += 1
                self.evento("derrota", f"{alvo.nome} cai.", alvo=alvo.id)

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
                                  f"{self.rodada + 1}.", ator=c.id, alvo=iid)
            return
        p = d.get("preparo")
        if p and self.rodada in p["em"]:
            alvo = None if p.get("area") else self._alvo_menos_vida()
            c.preparando = {"id": p["id"], "alvo": alvo, "anunciado": self.rodada}
            self.resumo["preparos"] += 1
            quem = "todo o grupo" if p.get("area") else self.c[alvo].nome
            self.evento("prepara", f"{c.nome} {p['aviso']}: prepara {p['nome']} em {quem}. Resolve na próxima vez dele.",
                        ator=c.id, alvo=alvo)
            return
        vivos = self.vivos("aliado")
        alvo = self.c[self.rng.choice(vivos)]
        self._receber(alvo, d["dano"], f"{c.nome}: {d['golpe']} em {{alvo}}", [f"{d['dano']} de dano"], ator=c.id)

    def _resolver_preparo(self, c):
        p = c.d["preparo"]
        prep = c.preparando
        c.preparando = None
        self.resumo["preparos_resolvidos"] += 1
        if p.get("terror"):
            self.evento("resolve", f"{c.nome} solta o {p['nome']}.", ator=c.id)
            for a in self.vivos("aliado"):
                o = self.c[a]
                if o.atr["vontade"] >= LIMIAR:
                    o.estados["abalado"] = {"marco": "fim_turno", "de": o.id}
                    self.evento("efeito", f"{o.nome} (Vontade {o.atr['vontade']}) fica abalad{o.a}: −25% de dano no próximo "
                                          f"turno d{'ela' if o.a == 'a' else 'ele'}.", alvo=o.id)
                else:
                    o.estados["aterrorizado"] = {"marco": "proxima_vez"}
                    self.evento("efeito", f"{o.nome} (Vontade {o.atr['vontade']}) fica aterrorizad{o.a}: perde a próxima vez.",
                                alvo=o.id)
            return
        alvo = self.c[prep["alvo"]] if prep["alvo"] and self.c[prep["alvo"]].vivo and not self.c[prep["alvo"]].caido \
            else self.c[self._alvo_menos_vida()]
        recebeu = self._receber(alvo, p["dano"], f"{c.nome}: {p['nome']} em {{alvo}}", [f"{p['dano']} de dano"], ator=c.id)
        if recebeu.caido:
            return
        if p.get("atordoa"):
            if recebeu.atr["forca"] >= LIMIAR:
                self.evento("efeito", f"{recebeu.nome} (Força {recebeu.atr['forca']}) aguenta o impacto: não fica atordoad{recebeu.a}.",
                            alvo=recebeu.id)
            else:
                recebeu.estados["atordoado"] = {"marco": "proxima_vez"}
                self.evento("efeito", f"{recebeu.nome} (Força {recebeu.atr['forca']}) fica atordoad{recebeu.a}: perde a próxima vez.",
                            alvo=recebeu.id)
        if p.get("sangra"):
            vezes = 1 if recebeu.atr["constituicao"] >= LIMIAR else 2
            recebeu.estados["sangramento"] = {"marco": "vezes", "vezes": vezes}
            self.evento("efeito", f"{recebeu.nome} (Constituição {recebeu.atr['constituicao']}) sangra: perde 4 no início "
                                  f"de {'1 turno' if vezes == 1 else '2 turnos'} d{'ela' if recebeu.a == 'a' else 'ele'}.", alvo=recebeu.id)

    # ---------------------------------------------------------------- previsões e a ficha
    def prever(self, alvo, dano):
        """O dano que um golpe inimigo de `dano` faria no alvo agora, e se ele se defender (sem sorte: os inimigos não
        têm crítico)."""
        prot = alvo.estados.get("protegido")
        quem = self.c[prot["por"]] if prot and self.c[prot["por"]].vivo and not self.c[prot["por"]].caido else alvo

        def conta(o, red):
            d = max(1, round(dano * (1 - red)) - o.protecao)
            esc = o.estados.get("escudo")
            return max(0, d - (esc["resta"] if esc else 0))
        agora = conta(quem, quem.estados.get("defesa", {}).get("red", 0))
        defendendo = conta(alvo, reducao_defesa(alvo.atr)) if alvo.lado == "aliado" else agora
        return {"quem": quem.id, "agora": agora, "se_defender": defendendo}

    def derivados(self, c):
        a = c.atr
        lin = []

        def L(chave, nome, valor, como):
            lin.append({"id": chave, "nome": nome, "valor": valor, "como": como})
        L("vida", "Vida máxima", c.vida_max, f"{c.d['vida_base']} da classe + 6 × nível {c.nivel} + 5 × (CON {a['constituicao']} − 3)")
        L("recurso", f"{c.recurso_nome} máx.", c.recurso_max, "da classe; o ataque básico recupera 10")
        L("iniciativa", "Posição na ordem", self.ordem.index(c.id) + 1, f"AGI {a['agilidade']} (fixa a luta inteira)")
        L("potencia", "Dano do ataque básico", c.potencia(), f"arma {c.arma} + nível {c.nivel} (sem atributo)")
        L("protecao", "Proteção", c.protecao, "do equipamento: tira isso de cada golpe")
        L("critico", "Crítico", f"{round(critico(a) * 100)}%", f"5% + 4% × (PER {a['percepcao']} − 3); dano ×1,5")
        L("ponto_fraco", "Ponto fraco", "aproveita (+25%)" if a["percepcao"] >= LIMIAR else "não aproveita",
          f"PER {a['percepcao']}: a partir de {LIMIAR}")
        L("defesa", "Defender reduz", f"{round(reducao_defesa(a) * 100)}%", f"40% + 5% × (VON {a['vontade']} − 3), até 65%")
        L("terror", "Contra o Terror", f"fica abalad{c.a}" if a["vontade"] >= LIMIAR else "perde a vez",
          f"VON {a['vontade']}: a partir de {LIMIAR}, só abala")
        L("atordoar", "Golpe que atordoa", "aguenta" if a["forca"] >= LIMIAR else f"fica atordoad{c.a}",
          f"FOR {a['forca']}: a partir de {LIMIAR}, aguenta")
        L("sangra", "Sangramento", "1 vez" if a["constituicao"] >= LIMIAR else "2 vezes",
          f"CON {a['constituicao']}: a partir de {LIMIAR}, 1 vez")
        L("custo", "Custo das habilidades", f"{round(custo_mult(a) * 100)}%", f"−5% × (INT {a['intelecto']} − 3), até −25%")
        if "golpe_pesado" in c.kit:
            L("rompe", "Golpe Pesado rompe", f"{a['forca']} de Guarda", f"FOR {a['forca']}")
        if "comando" in c.kit:
            L("comando", "Grito de Comando", f"+{round(bonus_comando(a) * 100)}%", f"15% + 5% × (PRE {a['presenca']} − 3)")
        return lin

    # ---------------------------------------------------------------- o estado para a tela
    def estado(self):
        def comb(i):
            o = self.c[i]
            e = {"id": i, "nome": o.nome, "lado": o.lado, "papel": o.papel, "a": o.a, "retrato": o.retrato, "vida": o.vida,
                 "vida_max": o.vida_max, "caido": o.caido, "vivo": o.vivo, "guarda": o.guarda,
                 "guarda_max": o.d.get("guarda", 0), "protecao": o.protecao, "firme": bool(o.d.get("firme")),
                 "ponto_fraco": o.d.get("ponto_fraco"),
                 "estados": [{"id": k, "nome": nome_estado(o, k), "ate": self._marco(o, k, v), **({"resta": v["resta"]} if "resta" in v else {}),
                              **({"vezes": v["vezes"]} if "vezes" in v else {})} for k, v in o.estados.items()],
                 "entra_rodada": o.entra_rodada}
            if o.lado == "aliado":
                e.update(recurso=o.recurso, recurso_max=o.recurso_max, recurso_nome=o.recurso_nome, atributos=o.atr,
                         derivados=self.derivados(o))
            return e
        ameacas = []
        for i in self.inimigos:
            o = self.c[i]
            if o.vivo and o.preparando:
                p = o.d["preparo"]
                a = {"de": i, "nome": p["nome"], "area": bool(p.get("area")), "anunciado": o.preparando["anunciado"],
                     "resolve": "na próxima vez de " + o.nome + (" (nesta rodada)" if not o.vez_passou else f" (rodada {self.rodada + 1})")}
                if p.get("area"):
                    a["efeito"] = "Vontade 5 ou mais só abala"
                    a["alvos"] = [{"id": x, "nome": self.c[x].nome,
                                   "resultado": f"fica abalad{self.c[x].a} (−25% no próximo turno)" if self.c[x].atr["vontade"] >= LIMIAR
                                   else "perde a próxima vez"}
                                  for x in self.vivos("aliado")]
                else:
                    alvo = self.c[o.preparando["alvo"]] if o.preparando["alvo"] else None
                    extras = []
                    if alvo and alvo.vivo and not alvo.caido:
                        pv = self.prever(alvo, p["dano"])
                        a.update(alvo=alvo.id, alvo_nome=alvo.nome, previsto=pv)
                        quem = self.c[pv["quem"]]
                        if p.get("atordoa"):
                            extras.append(f"{quem.nome} aguenta o impacto (Força {quem.atr['forca']})"
                                          if quem.atr["forca"] >= LIMIAR else
                                          f"Atordoa: {quem.nome} perde a próxima vez (Força {quem.atr['forca']}; 5 aguenta)")
                        if p.get("sangra"):
                            v = 1 if quem.atr["constituicao"] >= LIMIAR else 2
                            extras.append(f"Sangramento: {quem.nome} perde 4 no início de {'1 turno' if v == 1 else '2 turnos'} "
                                          f"(Constituição {quem.atr['constituicao']}; 5 encurta para 1)")
                    a["efeito"] = ". ".join(extras)
                ameacas.append(a)
        acoes = []
        ativo = self.c[self.aguardando] if self.aguardando else None
        if ativo:
            for hid in ativo.kit:
                h = C.HABILIDADES[hid]
                acoes.append({"id": hid, "nome": h["nome"], "desc": h["desc"], "custo": self.custo(ativo, hid),
                              "recurso": ativo.recurso_nome, "motivo": self.motivo(ativo, hid),
                              "alvo": h["alvo"], "alvos": self.alvos(ativo, hid)})
            for iid, n in self.consumiveis.items():
                it = C.CONSUMIVEIS[iid]
                acoes.append({"id": "item:" + iid, "nome": it["nome"], "desc": it["desc"], "qtd": n, "icone": it["icone"],
                              "motivo": self.motivo(ativo, "item:" + iid), "alvo": it["alvo"],
                              "alvos": self.alvos(ativo, "item:" + iid), "item": True})
        return {"encontro": self.encontro, "nome": self.cfg["nome"], "objetivo": self.cfg["objetivo"],
                "teste": self.cfg.get("teste"), "distribuicao": self.distribuicao, "rodada": self.rodada,
                "pos": self.pos, "turno_id": self.turno_id, "aguardando": self.aguardando, "fim": self.fim,
                "ordem": [{"id": i, "nome": self.c[i].nome, "a": self.c[i].a, "retrato": self.c[i].retrato, "lado": self.c[i].lado,
                           "passou": self.c[i].vez_passou, "atual": i == self.aguardando,
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
        if m == "fim_turno":
            return f"no próximo turno de {self.c[v['de']].nome}"
        if m == "proxima_vez":
            return "perde a próxima vez"
        if m == "vezes":
            return f"mais {v['vezes']} {'vez' if v['vezes'] == 1 else 'vezes'}"
        return ""


NOME_ESTADO = {"defesa": "Defendendo", "protegido": "Protegido", "protegendo": "Protegendo", "abalado": "Abalado",
               "atordoado": "Atordoado", "aterrorizado": "Aterrorizado", "comando": "Comandado", "escudo": "Escudo de Luz",
               "marca": "Marcado", "sangramento": "Sangrando"}


def nome_estado(o, k):
    """O nome do estado concordando com o portador (Odette fica Atordoada)."""
    n = NOME_ESTADO[k]
    return n[:-1] + "a" if o.a == "a" and n.endswith("do") and not n.endswith("ndo") else n


NOME_PREPARO = {"bote": "O Bote", "esmagador": "O Golpe Esmagador", "terror": "O Grito de Terror"}


def situacao(distribuicao="A", atributos=None, escolha=None, ajuda=False):
    """A situação de aventura: as opções com o que o protagonista consegue sozinho e o que um companheiro acrescenta."""
    atr = dict(atributos) if atributos else dict(C.DISTRIBUICOES[distribuicao]["atributos"])
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
                   "como": f"{C.NOME_ATRIBUTO[o['atributo']]} {atr[o['atributo']]} (precisa de {o['minimo']})"}
    return {"titulo": s["titulo"], "texto": s["texto"], "resultado": res,
            "opcoes": [{"id": o["id"], "texto": o["texto"], "atributo": C.NOME_ATRIBUTO[o["atributo"]],
                        "valor": atr[o["atributo"]], "minimo": o["minimo"], "ajuda": o.get("ajuda")} for o in s["opcoes"]]}
