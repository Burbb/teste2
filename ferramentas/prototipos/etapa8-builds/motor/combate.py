"""O combate do protótipo X1 (nada no jogo): ordem fixa por Agilidade, uma vez por rodada para cada combatente, o grupo
inteiro (Jean, Morel e Odette) nas mãos do jogador, os inimigos sorteando como no jogo.

A regra das cadeias (seções 15.2 e 16.5 do 28)
----------------------------------------------
- Uma **cadeia** é tudo o que uma ação provoca (ou o começo e o fim da vez de alguém: pingos, pavio, invocações).
- Um efeito disparado tem uma **identidade**: (efeito, dono, motivo). O motivo é aquilo de que o efeito trata: o morto
  que explode, o atacante que leva o revide, a invocação que caiu. **Na mesma cadeia, a mesma identidade acontece uma
  vez.** Duas mortes são dois motivos (duas explosões); uma explosão que mata abre um motivo novo, e a cadeia acaba
  porque cada combatente cai uma vez.
- **Reações (Revide, espinhos, escudos, a Sentinela) respondem a golpes de ação**; o dano de uma reação, das camadas e
  das explosões não é golpe de ação.
- **Limites por rodada** ficam escritos na descrição de quem os tem (Revide, Fôlego Rubro).
- `LIMITE_ELOS` é só uma rede de segurança: uma cadeia maior que isso é defeito do motor e para a luta com erro.

O vocabulário: fichas (Guarda, Força, Exposto), camadas nos inimigos (Queimadura, Sangramento, Frio; Queimadura e Frio
se anulam), invocações (sem vez; agem no fim da vez de quem as chamou; efeito ao cair) e a Fúria.

Os números de dano, cura e previsão saem de `conta` (a mesma conta para a tela e para o golpe)."""
import random

from . import conteudo as C
from . import montagem as M

LIMITE_ELOS = 200
LETRAS = "ABCDEF"


class CadeiaSemFim(RuntimeError):
    pass


class Combatente:
    def __init__(self, cid, nome, lado, d):
        self.id, self.nome, self.lado = cid, nome, lado
        self.vida_max = self.vida = d["vida"]
        self.recurso_nome = d.get("recurso")
        self.recurso_max = self.recurso = d.get("recurso_max", 0)
        self.poder, self.agi = d["poder"], d["agi"]
        self.magia = d.get("magia", d["poder"])
        self.res = dict(d.get("res", {}))
        self.tracos = list(d.get("tracos", []))
        self.kit = list(d.get("kit", []))
        self.habs = list(d.get("habs", []))
        self.chance_hab = d.get("chance_hab", 0.35)
        self.golpe_nome = d.get("golpe", "Ataque")
        self.tipo_golpe = d.get("tipo", "fisico")
        self.espinhos = d.get("espinhos", 0)    # dano fixo em quem o golpeia (no jogo, vem de itens)
        self.revida = d.get("revida", 0)        # inimigo que revida (só nos testes de cadeia)
        self.retrato = d.get("retrato")
        self.fichas = {"guarda": 0, "forca": 0, "exposto": 0}
        self.estados = {}
        self.queima = None                      # {"camadas": n, "pingos": n}
        self.sangra = None                      # {"camadas": n, "pingos": n}
        self.frio = 0
        self.detonadas = 0                      # camadas consumidas no golpe em curso (Estouro, Banho de Sangue)
        self.abertas = 0
        self.calor = 0
        self.prep = None                        # golpe preparado: {"nome", "mult"}
        self.ult_usada = False
        self.efeitos = {}
        self.cura_rodada = -99
        self.invocacao, self.dono, self.tipo_inv, self.desfeita = None, None, None, False

    @property
    def vivo(self):
        return self.vida > 0

    def ef(self, k):
        return self.efeitos.get(k, 0)


class Combate:
    def __init__(self, montagem, encontro, semente=None, inicio=None):
        erros = M.erros(montagem)
        if erros:
            raise ValueError("; ".join(erros))
        if encontro not in C.ENCONTROS:
            raise ValueError("encontro desconhecido")
        self.montagem = {"estrutura": montagem["estrutura"], "spec": montagem["spec"], "kit": list(montagem["kit"]),
                         "ultimate": M.ultimate(montagem), "nos": dict(montagem["nos"]),
                         "nome": montagem.get("nome") or "Livre"}
        self.encontro = encontro
        enc = C.ENCONTROS[encontro]
        self.semente = enc["semente"] if semente is None else int(semente)
        self.rng_ia = random.Random(f"ia-{self.semente}")        # escolhas dos inimigos
        self.rng_sorte = random.Random(f"sorte-{self.semente}")  # chances (atordoar, sangrar, prender)
        lista = enc.get("inimigos") or random.Random(f"grupo-{self.semente}").choice(enc["sorteio"])
        self.c = {}
        spec = montagem["spec"]
        ef = M.efeitos(montagem)
        hd = dict(C.HEROI[spec])
        hd["kit"] = ["atacar"] + list(montagem["kit"]) + [self.montagem["ultimate"], "defender"]
        hd["vida"] += 12 * ef.get("couro", 0)
        hd["recurso_max"] += 12 * ef.get("recurso_extra", 0)
        self.heroi = self._novo("heroi", hd["nome"], "aliado", hd)
        self.heroi.efeitos = ef
        for cid, d in C.COMPANHEIROS.items():
            self._novo(cid, d["nome"], "aliado", d)
        contagem = {t: lista.count(t) for t in lista}
        vistos = {}
        for t in lista:
            vistos[t] = vistos.get(t, 0) + 1
            d = C.INIMIGOS[t]
            nome = d["nome"] + (f" {LETRAS[vistos[t] - 1]}" if contagem[t] > 1 else "")
            self._novo(f"{t}#{vistos[t]}", nome, "inimigo", d)
        for cid, mods in (inicio or {}).items():
            self._aplicar_inicio(self.c[cid], mods)
        self.ordem = sorted(self.c.values(), key=lambda x: -x.agi)  # estável: no empate, o grupo antes
        self.rodada, self.idx = 1, -1
        self.eventos, self.decisoes = [], []
        self.cadeia, self.n_cadeia, self.profundidade = None, 0, 0
        self.cadeias = []
        self.rodada_feitos = set()
        self.fim, self.aguardando, self.turno_id = None, None, 0
        self.hid_atual = None
        self.n_invocadas = 0
        self.gatilhos_extra = []                 # testes: funções (cb, evento, alvo, valor)
        self.reacoes_respondem_reacoes = False   # testes: desliga a regra de tipo para conferir a de identidade
        self.dano_por_causa, self.dano_recebido, self.cura_total = {}, 0, 0
        self.ev("rodada", f"Rodada 1. Ordem: {', '.join(x.nome for x in self.ordem)}.")
        self._avancar()

    # ------------------------------------------------------------ montagem do encontro
    def _novo(self, cid, nome, lado, d):
        c = Combatente(cid, nome, lado, d)
        self.c[cid] = c
        return c

    @staticmethod
    def _aplicar_inicio(c, mods):
        """Condições de teste (só os testes usam)."""
        if "vida_max" in mods:
            c.vida_max = mods["vida_max"]
        if "vida" in mods:
            c.vida = mods["vida"]
        if "camadas" in mods:
            c.queima = {"camadas": mods["camadas"], "pingos": C.PINGOS}
        if "sangra" in mods:
            c.sangra = {"camadas": mods["sangra"], "pingos": C.PINGOS}
        if "frio" in mods:
            c.frio = mods["frio"]
        if "recurso" in mods:
            c.recurso = mods["recurso"]
        if mods.get("parado"):
            c.estados["parado"] = {}
        if mods.get("prep"):
            c.prep = {"nome": "Golpe Esmagador", "mult": 2.2}
        for k in ("agi", "espinhos", "revida", "poder"):
            if k in mods:
                setattr(c, k, mods[k])
        for f, n in mods.get("fichas", {}).items():
            c.fichas[f] = n

    def vivos(self, lado):
        return [x for x in self.c.values() if x.lado == lado and x.vivo]

    def grupo(self):
        """Os aliados que têm vez (sem as invocações)."""
        return [x for x in self.vivos("aliado") if not x.invocacao]

    def invocacoes(self, dono=None):
        return [x for x in self.vivos("aliado") if x.invocacao and (dono is None or x.dono == dono.id)]

    # ------------------------------------------------------------ registro
    def ev(self, tipo, texto, **extra):
        e = {"tipo": tipo, "texto": texto, "rodada": self.rodada,
             "cadeia": self.cadeia["n"] if self.cadeia else 0, "nivel": self.profundidade, **extra}
        self.eventos.append(e)
        return e

    # ------------------------------------------------------------ cadeias
    def _nova_cadeia(self, rotulo):
        self.n_cadeia += 1
        self.cadeia = {"n": self.n_cadeia, "rotulo": rotulo, "rodada": self.rodada, "feitos": set(), "elos": 0,
                       "barrados": 0}
        self.cadeias.append(self.cadeia)
        self.profundidade = 0

    def disparar(self, efeito, dono, motivo, fn, texto, por_rodada=False):
        """Executa um efeito disparado se a identidade (efeito, dono, motivo) ainda não aconteceu nesta cadeia e, nos
        limitados por rodada, se o dono ainda não o usou na rodada. Devolve se aconteceu."""
        if por_rodada and (efeito, dono.id) in self.rodada_feitos:
            self.ev("barrado", f"{texto}: já usado nesta rodada.", efeito=efeito, motivo="rodada")
            self.cadeia["barrados"] += 1
            return False
        chave = (efeito, dono.id, motivo.id)
        if chave in self.cadeia["feitos"]:
            self.ev("barrado", f"{texto}: já aconteceu nesta cadeia ({motivo.nome}).", efeito=efeito, motivo="cadeia")
            self.cadeia["barrados"] += 1
            return False
        self.cadeia["feitos"].add(chave)
        if por_rodada:
            self.rodada_feitos.add((efeito, dono.id))
        self.cadeia["elos"] += 1
        if self.cadeia["elos"] > LIMITE_ELOS:
            raise CadeiaSemFim(f"cadeia {self.cadeia['n']} passou de {LIMITE_ELOS} elos")
        self.ev("gatilho", texto, efeito=efeito, elo=self.cadeia["elos"])
        self.profundidade += 1
        try:
            fn()
        finally:
            self.profundidade -= 1
        return True

    # ------------------------------------------------------------ a conta
    def _frio_penetrante(self):
        h = self.heroi
        return h.ef("frio_penetrante") or (h.ef("sentinela_cortante") and any(
            x.tipo_inv == "sentinela" for x in self.invocacoes(h)))

    def conta(self, fonte, alvo, base, tipo, extra=1.0, forca=1.0, hid=None):
        """O dano de um golpe (sem gastar nada) e as partes da conta, para a tela e para o registro."""
        m, partes = extra * forca, []
        if forca != 1.0:
            partes.append(f"Força ×{forca:g}")
        if extra != 1.0:
            partes.append(f"bônus ×{extra:g}")
        if "fortalecido" in fonte.estados:
            m *= 1.3
            partes.append("Fortalecido +30%")
        if "enfraquecido" in fonte.estados:
            m *= 0.7
            partes.append("Enfraquecido −30%")
        if "furia" in fonte.estados:
            f = 1.6 if fonte.ef("furia_sem_freio") else 1.4
            m *= f
            partes.append(f"Fúria +{round((f - 1) * 100)}%")
        if fonte.ef("braco"):
            m *= 1 + 0.08 * fonte.ef("braco")
            partes.append(f"golpes +{8 * fonte.ef('braco')}%")
        if fonte.vida < fonte.vida_max / 2 and (fonte.ef("ate_o_fim") or (fonte.ef("desesperada") and
                                                                         hid == "furia_cega")):
            m *= 1.3
            partes.append("Até o Fim +30%")
        if "furia" in alvo.estados:
            f = 1.2 if alvo.ef("furia_contida") else 1.4
            m *= f
            partes.append(f"alvo na Fúria +{round((f - 1) * 100)}%")
        if "cerrado" in alvo.estados:
            m *= 0.7
            partes.append("Cerrar os Dentes −30%")
        if alvo.frio and alvo.lado == "inimigo" and self._frio_penetrante():
            m *= 1 + 0.1 * alvo.frio
            partes.append(f"Frio Penetrante +{10 * alvo.frio}%")
        r = alvo.res.get(tipo, 1.0)
        if r != 1.0:
            m *= r
            partes.append(f"{C.TIPOS[tipo]} ×{r:g}")
        if alvo.fichas["guarda"]:
            m *= 0.5
            partes.append("Guarda −50%")
        elif alvo.fichas["exposto"]:
            m *= 1.5
            partes.append("Exposto +50%")
        return max(1, round(base * m)), partes

    def golpe(self, fonte, alvo, base, tipo, causa, reacao=False, extra=1.0, forca=1.0, rotulo=None, area=False,
              hid=None):
        if not alvo.vivo:
            return 0
        dano, partes = self.conta(fonte, alvo, base, tipo, extra, forca, hid)
        if alvo.fichas["guarda"]:
            alvo.fichas["guarda"] -= 1
        elif alvo.fichas["exposto"]:
            alvo.fichas["exposto"] -= 1
        self._perder_vida(alvo, dano, fonte, causa, golpe=True, reacao=reacao, rotulo=rotulo, partes=partes,
                          tipo=tipo, area=area)
        return dano

    def _perder_vida(self, alvo, dano, fonte, causa, golpe=False, reacao=False, rotulo=None, partes=(), tipo="fogo",
                     area=False):
        em_chamas = alvo.queima is not None
        sangrava = alvo.sangra is not None
        alvo.vida = max(0, alvo.vida - dano)
        direto = golpe or causa in ("estouro", "pavio", "espinhos", "escudo_espinhos", "cinza_fria", "fatuo")
        quem = f"{fonte.nome} → {alvo.nome}" if direto and fonte and fonte is not alvo else alvo.nome
        self.ev("dano", f"{rotulo or causa}: {quem}, {dano} de {C.TIPOS.get(tipo, tipo)}"
                        + (f" ({', '.join(partes)})" if partes else "") + ("" if alvo.vivo else ". Cai."),
                alvo=alvo.id, valor=dano, causa=causa, golpe=golpe, reacao=reacao)
        if fonte and fonte.lado == "aliado" and alvo.lado == "inimigo":
            self.dano_por_causa[causa] = self.dano_por_causa.get(causa, 0) + dano
        if alvo.lado == "aliado" and not alvo.invocacao:
            self.dano_recebido += dano
        h = self.heroi
        if golpe and fonte is h and "furia" in h.estados and h.ef("sangue_quente"):
            self.disparar("sangue_quente", h, alvo, lambda: self.curar(h, round(dano * 0.15), h, "sangue_quente"),
                          f"Sangue Quente ({alvo.nome})")
        if not alvo.vivo:
            self._morreu(alvo, fonte, causa)
            return
        if golpe and fonte is h and not area and sangrava and h.ef("fio_cortante") and alvo.lado == "inimigo":
            self.disparar("fio_cortante", h, alvo, lambda: self.sangrar(alvo, 1, h, "fio_cortante"),
                          f"Fio Cortante ({alvo.nome})")
        if golpe and fonte and fonte.lado == "aliado" and alvo.lado == "inimigo" and not reacao:
            if fonte is not h and em_chamas and (h.ef("partilhado") or "marca_partilhada" in alvo.estados):
                self.disparar("partilhado", h, alvo, lambda: self.acender(alvo, 1, fonte, "partilhado"),
                              f"Calor Partilhado: {fonte.nome} acende {alvo.nome}")
            if "flamejante" in fonte.estados and alvo.vivo:
                self.disparar("arma_flamejante", fonte, alvo, lambda: self.acender(alvo, 1, h, "arma_flamejante"),
                              f"Arma Flamejante: {fonte.nome} acende {alvo.nome}")
        if golpe and fonte and fonte.vivo and (not reacao or self.reacoes_respondem_reacoes):
            self._reagir(alvo, fonte)

    def _reagir(self, alvo, fonte):
        """Quem foi golpeado responde (Revide, espinhos, escudos, Cerrar os Dentes, a Sentinela)."""
        h = self.heroi
        if alvo.lado == fonte.lado:
            return
        if alvo is h and "cerrado" in h.estados:
            self.disparar("cerrar", h, fonte, lambda: self.ganhar_recurso(h, 5, "cerrar_dentes"),
                          f"Cerrar os Dentes: +5 de Vigor ({fonte.nome})")
        if alvo is h and "rancor" in h.estados and fonte.id not in h.estados["rancor"]["ja"]:
            h.estados["rancor"]["ja"].append(fonte.id)
            self.disparar("revide", h, fonte,
                          lambda: self.golpe(h, fonte, h.poder * 0.6, "fisico", "revide", reacao=True, rotulo="Revide"),
                          f"Provocação com Revide contra {fonte.nome}")
        elif alvo is h and h.ef("revide"):
            self.disparar("revide", h, fonte,
                          lambda: self.golpe(h, fonte, h.poder * 0.6, "fisico", "revide", reacao=True, rotulo="Revide"),
                          f"Revide contra {fonte.nome}", por_rodada=True)
        if alvo.espinhos and fonte.vivo:
            self.disparar("espinhos", alvo, fonte,
                          lambda: self._perder_vida(fonte, alvo.espinhos, alvo, "espinhos", rotulo="Espinhos",
                                                    tipo="fisico"),
                          f"Espinhos de {alvo.nome}")
        if "espinhos_escudo" in alvo.estados and fonte.vivo:
            v = alvo.estados.pop("espinhos_escudo")["valor"]
            self.disparar("escudo_espinhos", h, fonte,
                          lambda: self._perder_vida(fonte, v, alvo, "escudo_espinhos", rotulo="Escudo de Espinhos",
                                                    tipo="fisico"),
                          f"Escudo de Espinhos fere {fonte.nome}")
        if "chamas" in alvo.estados and fonte.lado == "inimigo" and fonte.vivo:
            self.disparar("escudo_chamas", h, fonte, lambda: self.acender(fonte, 1, h, "escudo_chamas"),
                          f"Escudo de Chamas acende {fonte.nome}")
        if alvo.tipo_inv == "sentinela" and fonte.vivo:
            self.disparar("sentinela", alvo, fonte, lambda: self.resfriar(fonte, 1, h, "sentinela"),
                          f"A Sentinela esfria {fonte.nome}")
        if alvo.revida and fonte.vivo and alvo.lado == "inimigo":
            self.disparar("revide_inimigo", alvo, fonte,
                          lambda: self.golpe(alvo, fonte, alvo.revida, "fisico", "revide", reacao=True,
                                             rotulo=f"Revide de {alvo.nome}"),
                          f"{alvo.nome} revida contra {fonte.nome}")

    def _morreu(self, alvo, fonte, causa):
        camadas = max(alvo.queima["camadas"] if alvo.queima else 0, alvo.detonadas)
        feridas = max(alvo.sangra["camadas"] if alvo.sangra else 0, alvo.abertas)
        alvo.queima, alvo.sangra, alvo.frio, alvo.prep, alvo.estados = None, None, 0, None, {}
        alvo.detonadas = alvo.abertas = 0
        alvo.fichas = {"guarda": 0, "forca": 0, "exposto": 0}
        h = self.heroi
        if alvo.invocacao:
            self._invocacao_caiu(alvo, causa == "sacrificio")
        elif alvo.lado == "inimigo":
            if camadas and (h.ef("estouro") or (h.ef("estrondosa") and causa == "combustao")):
                self.disparar("estouro", h, alvo, lambda: self._explodir(alvo, camadas),
                              f"Estouro: {alvo.nome} explode ({camadas} camada{'s' if camadas > 1 else ''})")
            if feridas and h.ef("banho_sangue"):
                def banho():
                    for e in self.vivos("inimigo"):
                        self.sangrar(e, feridas, h, "banho_sangue", substitui=True)
                self.disparar("banho_sangue", h, alvo, banho,
                              f"Banho de Sangue: as {feridas} camadas de {alvo.nome} passam aos outros")
            if causa == "furia_cega":
                resto = self.vivos("inimigo")
                if resto:
                    t = min(resto, key=lambda x: x.vida)
                    self.disparar("furia_cega", h, alvo,
                                  lambda: self.golpe(h, t, h.poder * 1.2, "fisico", "furia_cega_seguimento",
                                                     rotulo="Fúria Cega (segue)"),
                                  f"Fúria Cega segue para {t.nome}")
        self._conferir_fim()

    def _explodir(self, morto, camadas):
        base = 6 + 3 * camadas
        for e in list(self.vivos("inimigo")):
            if not e.vivo:
                continue
            d = max(1, round(base * e.res.get("fogo", 1.0)))
            self._perder_vida(e, d, self.heroi, "estouro", rotulo=f"Explosão de {morto.nome}")
            if e.vivo:
                self.acender(e, 1, self.heroi, "estouro")
        self._calor(morto)

    def _calor(self, alvo):
        h = self.heroi
        if h.ef("fornalha"):
            def ganha():
                h.calor = min(3, h.calor + 1)
            self.disparar("fornalha", h, alvo, ganha, f"Fornalha Interior: +1 Calor ({alvo.nome})")

    def _conferir_fim(self):
        if self.fim:
            return
        if not self.vivos("inimigo"):
            self.fim = "vitoria"
            self.ev("fim", "Vitória.")
        elif not self.grupo():
            self.fim = "derrota"
            self.ev("fim", "Derrota.")

    # ------------------------------------------------------------ invocações
    def invocar(self, dono, tipo):
        for x in self.invocacoes(dono):
            if x.tipo_inv == tipo:
                x.vida, x.desfeita = 0, True
                self.ev("estado", f"{x.nome} anterior se desfaz (sem efeito).")
        d = C.INVOCACOES[tipo]
        self.n_invocadas += 1
        inv = self._novo(f"{tipo}#{self.n_invocadas}", d["nome"], "aliado", dict(d, retrato=tipo))
        inv.invocacao, inv.dono, inv.tipo_inv = True, dono.id, tipo
        self.ev("estado", f"{dono.nome} invoca {inv.nome} ({inv.vida} de vida).", alvo=inv.id)
        if tipo == "sentinela":
            for e in self.vivos("inimigo"):
                e.estados["provocado"] = {"por": inv.id}
            self.ev("estado", "Os inimigos miram a Sentinela na próxima vez deles.")
        return inv

    def sacrificar(self, inv):
        self.ev("acao", f"{inv.nome} é sacrificado.", ator=inv.id)
        inv.vida = 0
        self._morreu(inv, self.heroi, "sacrificio")

    def _invocacao_caiu(self, inv, sacrificada):
        dono = self.c[inv.dono]
        x = 2 if sacrificada else 1
        if inv.tipo_inv == "fogo_fatuo":
            def explode():
                for e in list(self.vivos("inimigo")):
                    if e.vivo:
                        self._perder_vida(e, max(1, round(8 * x * e.res.get("fogo", 1.0))), inv, "fatuo",
                                          rotulo="Explosão do Fogo-fátuo")
            self.disparar("invocacao_cai", dono, inv, explode,
                          f"O Fogo-fátuo explode{' em dobro' if x > 1 else ''}")
        elif inv.tipo_inv == "sentinela":
            def estilhaca():
                for e in list(self.vivos("inimigo")):
                    self.resfriar(e, x, dono, "sentinela_cai")
            self.disparar("invocacao_cai", dono, inv, estilhaca,
                          f"A Sentinela se estilhaça{' em dobro' if x > 1 else ''}: Frio em cada inimigo")
        if dono.ef("elo_elemental"):
            def elo():
                self.ganhar_recurso(dono, 12, "elo_elemental")
                self.dar_ficha(dono, "forca", fonte=dono)
            self.disparar("elo_elemental", dono, inv, elo, f"Elo Elemental ({inv.nome})")

    def _passivas_invocacoes(self, dono):
        """No fim da vez de quem as chamou, na ordem em que foram chamadas."""
        invs = self.invocacoes(dono)
        if not invs:
            return
        self._nova_cadeia(f"Fim da vez de {dono.nome}: invocações")
        for inv in invs:
            if not inv.vivo or self.fim:
                continue
            inimigos = self.vivos("inimigo")
            if inv.tipo_inv == "estandarte":
                if dono.ef("estandarte_sangrento"):
                    alvos = [e for e in inimigos if "morto-vivo" not in e.tracos]
                    if alvos:
                        t = min(alvos, key=lambda e: ((e.sangra or {}).get("camadas", 0), e.vida))
                        self.ev("acao", f"O Estandarte aponta {t.nome}.", ator=inv.id)
                        self.sangrar(t, 1, dono, "estandarte")
                else:
                    g = self.grupo()
                    t = min(g, key=lambda a: (a.fichas["forca"], self.ordem.index(a)))
                    self.ev("acao", f"O Estandarte inspira {t.nome}.", ator=inv.id)
                    self.dar_ficha(t, "forca", fonte=inv)
            elif inv.tipo_inv == "fogo_fatuo" and inimigos:
                cam = lambda e: (e.queima or {}).get("camadas", 0)  # noqa: E731
                if dono.ef("fatuo_faminto"):
                    cand = [e for e in inimigos if cam(e) < C.CAMADAS_TETO] or inimigos
                    t = max(cand, key=lambda e: (cam(e), -e.vida))
                else:
                    t = min(inimigos, key=lambda e: (cam(e), e.vida))
                self.ev("acao", f"O Fogo-fátuo voa até {t.nome}.", ator=inv.id)
                self.acender(t, 1, dono, "fogo_fatuo")

    # ------------------------------------------------------------ camadas: fogo, frio, sangue
    def acender(self, alvo, n, fonte, causa, hid=None):
        if not alvo.vivo:
            return
        h = self.heroi
        if fonte is h and h.ef("queimar") and h.vida < h.vida_max / 2:
            n += 1
        if alvo.frio:
            if h.ef("vapor") or (h.ef("bola_vapor") and hid == "bola_fogo"):
                f, alvo.frio = alvo.frio, 0
                self.ev("estado", f"Vapor: o Frio de {alvo.nome} vira Exposto.", alvo=alvo.id)
                self.dar_ficha(alvo, "exposto", min(f, 2), fonte=h)
            else:
                tira = min(n, alvo.frio)
                alvo.frio -= tira
                n -= tira
                self.ev("estado", f"O fogo derrete {tira} Frio de {alvo.nome}.", alvo=alvo.id)
        if n <= 0:
            return
        c0 = alvo.queima["camadas"] if alvo.queima else 0
        c = min(C.CAMADAS_TETO, c0 + n)
        alvo.queima = {"camadas": c, "pingos": C.PINGOS}
        self.ev("acende", f"{alvo.nome}: Queimadura {c0} → {c}.", alvo=alvo.id, causa=causa)

    def resfriar(self, alvo, n, fonte, causa, hid=None):
        if not alvo.vivo:
            return
        h = self.heroi
        if alvo.queima:
            if h.ef("cinza_fria") or (h.ef("lanca_termica") and hid == "lanca"):
                c, alvo.queima = alvo.queima["camadas"], None
                d = max(1, round(C.DETONA_CAMADA * c * alvo.res.get("gelo", 1.0)))
                self.disparar("cinza_fria", h, alvo,
                              lambda: self._perder_vida(alvo, d, h, "cinza_fria", rotulo="Cinza Fria", tipo="gelo"),
                              f"Cinza Fria: {c} camada{'s' if c > 1 else ''} de {alvo.nome} viram gelo")
                if not alvo.vivo:
                    return
                n += c
            else:
                tira = min(n, alvo.queima["camadas"])
                alvo.queima["camadas"] -= tira
                n -= tira
                if alvo.queima["camadas"] <= 0:
                    alvo.queima = None
                self.ev("estado", f"O gelo apaga {tira} camada{'s' if tira > 1 else ''} de {alvo.nome}.",
                        alvo=alvo.id)
        if n <= 0:
            return
        f0 = alvo.frio
        alvo.frio = min(C.CAMADAS_TETO, alvo.frio + n)
        self.ev("estado", f"{alvo.nome}: Frio {f0} → {alvo.frio}.", alvo=alvo.id, causa=causa)
        if alvo.frio >= C.CAMADAS_TETO:
            if self.atordoar(alvo, 1.0, "Congelado", fonte):
                alvo.frio = 0
            else:
                alvo.frio = C.CAMADAS_TETO - 1

    def sangrar(self, alvo, n, fonte, causa, substitui=False):
        if not alvo.vivo:
            return
        if "morto-vivo" in alvo.tracos:
            self.ev("resiste", f"{alvo.nome} não sangra.", alvo=alvo.id)
            return
        c0 = alvo.sangra["camadas"] if alvo.sangra else 0
        c = min(C.CAMADAS_TETO, max(c0, n) if substitui else c0 + n)
        if c == c0 and substitui:
            return
        alvo.sangra = {"camadas": c, "pingos": C.PINGOS}
        self.ev("acende", f"{alvo.nome}: Sangramento {c0} → {c}.", alvo=alvo.id, causa=causa)

    def chama_viva(self):
        return 1 + 0.15 * self.heroi.ef("chama_viva")

    def base_detonacao(self, alvo, camadas=None):
        c = (alvo.queima["camadas"] if alvo.queima else 0) if camadas is None else camadas
        return self.heroi.poder * 0.4 + C.DETONA_CAMADA * c * self.chama_viva()

    def detonar(self, alvo, causa, golpe=True, extra=1.0, forca=1.0, rotulo=None):
        h = self.heroi
        c = alvo.queima["camadas"] if alvo.queima else 0
        base = self.base_detonacao(alvo)
        alvo.queima, alvo.detonadas = None, c
        if c:
            self.ev("detona", f"{rotulo or causa}: detona {c} camada{'s' if c > 1 else ''} em {alvo.nome}.",
                    alvo=alvo.id)
        if golpe:
            self.golpe(h, alvo, base, "fogo", causa, extra=extra, forca=forca, rotulo=rotulo)
        else:
            d = max(1, round(base * extra * alvo.res.get("fogo", 1.0)))
            self._perder_vida(alvo, d, h, causa, rotulo=rotulo)
        if c:
            self._calor(alvo)
        alvo.detonadas = 0
        return c

    # ------------------------------------------------------------ fichas, estados, cura
    def dar_ficha(self, alvo, ficha, n=1, fonte=None):
        ganhou = 0
        for _ in range(n):
            oposto = {"guarda": "exposto", "exposto": "guarda"}.get(ficha)
            if oposto and alvo.fichas[oposto]:
                alvo.fichas[oposto] -= 1
                self.ev("ficha", f"{alvo.nome}: {C.FICHAS[ficha]['nome']} anula 1 {C.FICHAS[oposto]['nome']}.")
                continue
            if alvo.fichas[ficha] < C.FICHA_TETO:
                alvo.fichas[ficha] += 1
                ganhou += 1
                self.ev("ficha", f"{alvo.nome} ganha 1 {C.FICHAS[ficha]['nome']} ({alvo.fichas[ficha]}).")
            else:
                self.ev("ficha", f"{alvo.nome} já tem {C.FICHA_TETO} {C.FICHAS[ficha]['nome']}: no teto.")
        h = self.heroi
        if ficha == "exposto" and ganhou and fonte is h and alvo.lado == "inimigo" and h.ef("peso_golpe"):
            self.disparar("peso_golpe", h, alvo, self._peso_do_golpe, f"Peso do Golpe ({alvo.nome} Exposto)")
        if ficha == "guarda" and ganhou and fonte is h and alvo is not h and (
                h.ef("escudeiro") or (h.ef("escudo_duplo") and self.hid_atual == "erguer_escudo")):
            self.disparar("escudeiro", h, alvo, lambda: self.dar_ficha(h, "guarda"), f"Escudeiro ({alvo.nome})")
        return ganhou

    def _proximo_aliado(self):
        i = self.ordem.index(self.heroi)
        for k in range(1, len(self.ordem)):
            x = self.ordem[(i + k) % len(self.ordem)]
            if x.lado == "aliado" and x.vivo and x is not self.heroi:
                return x
        return None

    def _peso_do_golpe(self):
        a = self._proximo_aliado()
        if a:
            self.dar_ficha(a, "forca")

    def interromper(self, alvo, por):
        if not alvo.prep:
            return False
        self.ev("interrompe", f"{alvo.nome} perde o {alvo.prep['nome']}.", alvo=alvo.id)
        alvo.prep = None
        h = self.heroi
        if por is h and h.ef("peso_golpe"):
            self.disparar("peso_golpe", h, alvo, self._peso_do_golpe, f"Peso do Golpe ({alvo.nome} interrompido)")
        return True

    def atordoar(self, alvo, chance, rotulo, por):
        if not alvo.vivo:
            return False
        if "firme" in alvo.estados:
            self.ev("resiste", f"{alvo.nome} está Firme: não fica {rotulo.lower()}.", alvo=alvo.id)
            return False
        if "gigante" in alvo.tracos:
            chance /= 2
        if chance < 1 and self.rng_sorte.random() >= chance:
            self.ev("resiste", f"{alvo.nome} não fica {rotulo.lower()} ({round(chance * 100)}% de chance).",
                    alvo=alvo.id)
            return False
        alvo.estados["atordoado"] = {"rotulo": rotulo}
        self.ev("estado", f"{alvo.nome} fica {rotulo.lower()}: perde a próxima vez.", alvo=alvo.id)
        self.interromper(alvo, por)
        return True

    def entrar_furia(self, c):
        if "furia" in c.estados:
            return
        c.estados["furia"] = {"vezes": 0}
        self.ev("estado", "Jean entra em Fúria.")
        if c.ef("grito_contagiante"):
            def grito():
                for a in self.grupo():
                    if a is not c:
                        self.dar_ficha(a, "forca", fonte=c)
            self.disparar("grito_contagiante", c, c, grito, "Grito Contagiante")

    def curar(self, alvo, n, fonte, causa):
        if not alvo.vivo or n <= 0:
            return 0
        real = min(n, alvo.vida_max - alvo.vida)
        alvo.vida += real
        self.ev("cura", f"{causa_nome(causa)}: {alvo.nome} +{real} de vida.", alvo=alvo.id, valor=real)
        if alvo.lado == "aliado" and not alvo.invocacao:
            self.cura_total += real
        h = self.heroi
        if alvo is h and h.ef("folego") and real > 0:
            self.disparar("folego", h, h, lambda: self.ganhar_recurso(h, 6, "folego"), "Fôlego Rubro",
                          por_rodada=True)
        for g in self.gatilhos_extra:
            g(self, "cura", alvo, n)
        return real

    def ganhar_recurso(self, alvo, n, causa):
        real = min(n, alvo.recurso_max - alvo.recurso)
        alvo.recurso += real
        if causa not in ("regen", "basico"):
            self.ev("recurso", f"{causa_nome(causa)}: {alvo.nome} +{real} de {alvo.recurso_nome}.", alvo=alvo.id)
        for g in self.gatilhos_extra:
            g(self, "recurso", alvo, n)
        return real

    # ------------------------------------------------------------ a ordem
    def _avancar(self):
        while not self.fim:
            self.idx += 1
            if self.idx >= len(self.ordem):
                self._fim_da_rodada()
                if self.fim:
                    return
                self.idx = 0
            c = self.ordem[self.idx]
            if not c.vivo:
                continue
            self._comeco_da_vez(c)
            if self.fim:
                return
            if not c.vivo:
                continue
            if "atordoado" in c.estados:
                st = c.estados.pop("atordoado")
                c.estados["firme"] = {"vezes": 2}
                self.ev("perde", f"{c.nome} ({st['rotulo'].lower()}) perde a vez e fica Firme.", alvo=c.id)
                continue
            if c.lado == "aliado":
                self.aguardando = c.id
                self.turno_id += 1
                return
            self._agir_inimigo(c)
            if not self.fim:
                self._fim_da_vez(c)

    def _comeco_da_vez(self, c):
        self._nova_cadeia(f"Começo da vez de {c.nome}")
        h = self.heroi
        for k in ("rancor", "cerrado", "muralha"):  # valem até a próxima vez de quem os usou
            c.estados.pop(k, None)
        for x in self.c.values():  # o Proteger de Morel acaba na próxima vez dele
            if x.estados.get("protegido", {}).get("por") == c.id:
                del x.estados["protegido"]
        if "pavio" in c.estados or c.queima or c.sangra or "veneno" in c.estados:
            self.ev("inicio", f"Começo da vez de {c.nome}:", alvo=c.id)
        if "pavio" in c.estados:
            p = c.estados.pop("pavio")
            self.detonar(c, "pavio", golpe=False, extra=p["mult"], rotulo="Pavio Curto")
            if not c.vivo or self.fim:
                return
        if c.queima:
            camadas = c.queima["camadas"]
            d = max(1, round(C.PINGO_CAMADA * camadas * self.chama_viva() * c.res.get("fogo", 1.0)))
            self._perder_vida(c, d, h, "queimadura", rotulo="Queimadura")
            if not c.vivo or self.fim:
                return
            if c.queima and not (h.ef("paciente") and c.queima["camadas"] == C.CAMADAS_TETO):
                c.queima["pingos"] -= 1
                if c.queima["pingos"] <= 0:
                    c.queima = None
                    self.ev("apaga", f"A Queimadura de {c.nome} apaga.", alvo=c.id)
        if c.sangra:
            d = C.PINGO_CAMADA * c.sangra["camadas"]
            self._perder_vida(c, d, h if c.lado == "inimigo" else None, "sangramento", rotulo="Sangramento",
                              tipo="fisico")
            if not c.vivo or self.fim:
                return
            if c.sangra:
                c.sangra["pingos"] -= 1
                if c.sangra["pingos"] <= 0:
                    c.sangra = None
                    self.ev("apaga", f"O Sangramento de {c.nome} fecha.", alvo=c.id)
        s = c.estados.get("veneno")
        if s:
            self._perder_vida(c, s["valor"], None, "veneno", rotulo="Veneno", tipo="fisico")
            if not c.vivo or self.fim:
                return
            s["pingos"] -= 1
            if s["pingos"] <= 0:
                del c.estados["veneno"]
        if c.lado == "aliado" and c.recurso_max:
            self.ganhar_recurso(c, C.REGEN, "regen")

    def _fim_da_vez(self, c):
        for k in ("fortalecido", "enfraquecido", "firme", "flamejante"):
            s = c.estados.get(k)
            if s:
                s["vezes"] -= 1
                if s["vezes"] <= 0:
                    del c.estados[k]
        if "furia" in c.estados:
            c.estados["furia"]["vezes"] += 1
        if c is self.heroi and not self.fim:
            self._passivas_invocacoes(c)

    def _fim_da_rodada(self):
        self.rodada += 1
        self.rodada_feitos.clear()
        for x in self.c.values():
            for k in ("chamas", "marca_partilhada"):
                if k in x.estados and x.estados[k]["ate"] < self.rodada:
                    del x.estados[k]
        if self.rodada > C.LIMITE_RODADAS:
            self.fim = "empate"
            self.ev("fim", f"Empate: {C.LIMITE_RODADAS} rodadas.")
            return
        self.cadeia = None
        self.ev("rodada", f"Rodada {self.rodada}.")

    # ------------------------------------------------------------ os inimigos
    def _alvo_inimigo(self, e):
        vivos = self.vivos("aliado")
        alvo = self.rng_ia.choice(vivos)  # sorteia sempre, para a sequência ser a mesma com ou sem provocação
        p = e.estados.pop("provocado", None)
        if p and p["por"] in self.c and self.c[p["por"]].vivo:
            alvo = self.c[p["por"]]
        h = self.heroi
        if "muralha" in h.estados and h.vivo:
            alvo = h
        prot = alvo.estados.get("protegido")
        if prot and self.c[prot["por"]].vivo:
            self.ev("protege", f"{self.c[prot['por']].nome} entra na frente de {alvo.nome}.")
            alvo = self.c[prot["por"]]
        return alvo

    def _hab_util(self, e, h):
        if h in ("uivo", "grito"):
            return any("fortalecido" not in x.estados for x in self.vivos("inimigo"))
        if h == "regenerar":
            return e.vida <= e.vida_max * 0.7
        if h == "cura":
            return self.rodada - e.cura_rodada >= 3 and any(x.vida < x.vida_max * 0.6 for x in self.vivos("inimigo"))
        return True

    def _agir_inimigo(self, e):
        self._nova_cadeia(f"Vez de {e.nome}")
        if "parado" in e.estados:
            self.ev("acao", f"{e.nome} não faz nada (teste).", ator=e.id)
            return
        alvo = self._alvo_inimigo(e)
        if e.prep:
            p, e.prep = e.prep, None
            self.ev("acao", f"{e.nome} solta o {p['nome']} em {alvo.nome}.", ator=e.id)
            self.golpe(e, alvo, e.poder * p["mult"], e.tipo_golpe, "inimigo", rotulo=p["nome"])
            return
        sorte = self.rng_ia.random()
        if e.habs and sorte < e.chance_hab:
            uteis = [h for h in e.habs if self._hab_util(e, h)]
            if uteis:
                self._hab_inimigo(e, self.rng_ia.choice(uteis), alvo)
                return
        self.ev("acao", f"{e.nome}: {e.golpe_nome} em {alvo.nome}.", ator=e.id)
        self.golpe(e, alvo, e.poder, e.tipo_golpe, "inimigo", rotulo=e.golpe_nome)

    def _hab_inimigo(self, e, h, alvo):
        nome = C.HABS_INIMIGO[h].split(":")[0]
        if h in ("uivo", "grito"):
            self.ev("acao", f"{e.nome}: {nome}. Os inimigos ficam Fortalecidos.", ator=e.id)
            for x in self.vivos("inimigo"):
                x.estados["fortalecido"] = {"vezes": 2}
            return
        if h == "esmagar":
            e.prep = {"nome": "Golpe Esmagador", "mult": 2.2}
            self.ev("prepara", f"{e.nome} recua e prepara o Golpe Esmagador (sai na próxima vez dele).", ator=e.id)
            return
        if h == "regenerar":
            self.ev("acao", f"{e.nome}: Regenerar.", ator=e.id)
            self.curar(e, round(e.vida_max * 0.15), e, "regenerar")
            return
        if h == "cura":
            a = min([x for x in self.vivos("inimigo") if x.vida < x.vida_max * 0.6], key=lambda x: x.vida / x.vida_max)
            e.cura_rodada = self.rodada
            self.ev("acao", f"{e.nome}: Cura em {a.nome}.", ator=e.id)
            self.curar(a, round(a.vida_max * 0.25), e, "cura_inimiga")
            return
        if h in ("maldicao", "grito_terror"):
            vezes = 3 if h == "maldicao" else 2
            self.ev("acao", f"{e.nome}: {nome} em {alvo.nome}.", ator=e.id)
            alvo.estados["enfraquecido"] = {"vezes": vezes}
            self.ev("estado", f"{alvo.nome} fica Enfraquecido (−30%) por {vezes} vezes.", alvo=alvo.id)
            return
        self.ev("acao", f"{e.nome}: {nome} em {alvo.nome}.", ator=e.id)
        if h in ("bola_fogo", "bola_sombra"):
            self.golpe(e, alvo, e.magia * 1.3, "fogo" if h == "bola_fogo" else "sombra", "inimigo", rotulo=nome)
            return
        mult = {"mordida": 1.0, "golpe_sujo": 1.1, "veneno": 0.8, "agarrar": 0.8, "investida": 1.3}[h]
        self.golpe(e, alvo, e.poder * mult, e.tipo_golpe, "inimigo", rotulo=nome)
        if not alvo.vivo or self.fim:
            return
        if h == "mordida" and self.rng_sorte.random() < 0.7:
            self.sangrar(alvo, 1, e, "mordida")
        elif h == "veneno":
            alvo.estados["veneno"] = {"valor": 2, "pingos": 3}
            self.ev("estado", f"{alvo.nome} fica envenenado (2 por turno, 3 turnos).", alvo=alvo.id)
        elif h == "golpe_sujo" and self.rng_sorte.random() < 0.35:
            alvo.estados["enfraquecido"] = {"vezes": 2}
            self.ev("estado", f"{alvo.nome} fica Enfraquecido (−30%) por 2 vezes.", alvo=alvo.id)
        elif h == "agarrar":
            self.atordoar(alvo, 0.4, "Preso", e)
        elif h == "investida":
            self.atordoar(alvo, 0.25, "Atordoado", e)

    # ------------------------------------------------------------ as ações do grupo
    def _custo_base(self, c, hid):
        return M.custo_habilidade(c.efeitos, hid) if c is self.heroi else C.HABILIDADES[hid]["custo"]

    def custo(self, c, hid):
        """(custo em recurso, custo em vida, rótulo) da ação agora, ou None se não dá para pagar."""
        h = C.HABILIDADES[hid]
        custo = self._custo_base(c, hid)
        if c is not self.heroi:
            return (custo, 0, f"{custo} de {c.recurso_nome}" if custo else "")
        fogo = "fogo" in h["etiquetas"]
        if fogo and c.calor >= 3 and custo:
            return (0, 0, "Grátis: 3 Calor")
        if c.recurso >= custo:
            return (custo, 0, f"{custo} de {c.recurso_nome}" if custo else "")
        falta = custo - c.recurso
        if fogo and c.ef("pagar_vida") and c.vida > falta:
            return (c.recurso, falta, f"{c.recurso} de {c.recurso_nome} + {falta} de vida")
        return None

    def motivo(self, c, hid):
        h = C.HABILIDADES[hid]
        if h.get("ultimate") and c.ult_usada:
            return "Já usada nesta luta"
        if self.custo(c, hid) is None:
            return f"Falta {self._custo_base(c, hid) - c.recurso} de {c.recurso_nome}"
        if not self.alvos(c, hid):
            return "Sem alvo"
        return None

    def alvos(self, c, hid):
        a = C.HABILIDADES[hid]["alvo"]
        if a in ("inimigo", "inimigos"):
            out = [x.id for x in self.vivos("inimigo")]
            if hid == "combustao" and c.ef("sacrificio"):
                out += [x.id for x in self.invocacoes(c)]
            return out
        if a == "aliado":
            return [x.id for x in self.vivos("aliado")]
        if a == "aliado_outro":
            return [x.id for x in self.grupo() if x is not c]
        return [c.id]

    def _forca_prevista(self, c, hid):
        if hid == "golpe_pesado" and c.ef("acumulado"):
            return 1 + 0.5 * sum(x.fichas["forca"] for x in self.grupo())
        return 1.5 if c.fichas["forca"] else 1.0

    def _gastar_forca(self, c, hid):
        f = self._forca_prevista(c, hid)
        if hid == "golpe_pesado" and c.ef("acumulado"):
            n = sum(x.fichas["forca"] for x in self.grupo())
            for x in self.grupo():
                x.fichas["forca"] = 0
            if n:
                self.ev("ficha", f"Golpe Acumulado consome {n} Força{'s' if n > 1 else ''} do grupo.")
        elif c.fichas["forca"]:
            c.fichas["forca"] -= 1
        return f

    def _tipo_de(self, c, hid):
        if "flamejante" in c.estados and hid in ("atacar", "oportuno", "bastao"):
            return "fogo"
        return C.HABILIDADES[hid].get("tipo", "fisico")

    def _golpe_de(self, c, hid, alvo):
        """(base, tipo, extra) do golpe principal da ação, ou None se ela não golpeia agora."""
        h = C.HABILIDADES[hid]
        if alvo.lado == "aliado":
            return None
        if hid == "combustao" and c.ef("pavio"):
            return None
        if hid in ("combustao", "conflagracao"):
            return (self.base_detonacao(alvo), "fogo", 1.0)
        if hid == "abrir_feridas":
            return (c.poder * 0.4 + C.FERIDA_CAMADA * (alvo.sangra or {}).get("camadas", 0), "fisico", 1.0)
        if hid == "escudo_alto":
            return (c.poder * 0.3 + 12 * c.fichas["guarda"], "fisico", 1.0)
        if hid == "chuva" and c.ef("chuva_densa"):
            return None
        if "mult" not in h:
            return None
        mult = h["mult"]
        if hid == "golpe_pesado" and c.ef("desequilibra"):
            mult = 1.1
        if hid == "redemoinho" and c.ef("redemoinho_sangrento"):
            mult = 0.45
        extra = 1.0
        if hid == "oportuno" and ("atordoado" in alvo.estados or alvo.prep):
            extra = 1.6
        if hid == "lanca" and c.ef("estilhaco") and alvo.estados.get("atordoado", {}).get("rotulo") == "Congelado":
            extra = 2.0
        return (c.poder * mult, self._tipo_de(c, hid), extra)

    def previsao(self, c, hid, alvo):
        g = self._golpe_de(c, hid, alvo)
        if not g:
            return None
        dano, _ = self.conta(c, alvo, g[0], g[1], g[2], self._forca_prevista(c, hid), hid)
        if hid == "lanca" and alvo.queima and (c.ef("cinza_fria") or c.ef("lanca_termica")):
            return f"{dano} + {round(C.DETONA_CAMADA * alvo.queima['camadas'] * alvo.res.get('gelo', 1.0))}"
        return str(dano)

    def acoes(self):
        if not self.aguardando:
            return []
        c = self.c[self.aguardando]
        out = []
        desc = {k["id"]: k for k in M.kit_descrito(self.montagem)} if c is self.heroi else {}
        for hid in c.kit:
            h = C.HABILIDADES[hid]
            custo = self.custo(c, hid)
            mot = self.motivo(c, hid)
            alvos = self.alvos(c, hid) if not mot else []
            d = desc.get(hid)
            out.append({"id": hid, "nome": h["nome"], "versao": d["versao"] if d else None,
                        "pagamento": custo[2] if custo else f"{self._custo_base(c, hid)} de {c.recurso_nome}",
                        "disponivel": not mot, "motivo": mot, "alvo": h["alvo"], "alvos": alvos,
                        "previsao": {a: self.previsao(c, hid, self.c[a]) for a in alvos
                                     if self.c[a].lado == "inimigo"},
                        "desc": d["desc"] if d else h["desc"], "notas": d["notas"] if d else [],
                        "ultimate": bool(h.get("ultimate"))})
        return out

    def motivo_sair_furia(self):
        h = self.heroi
        if self.aguardando != "heroi" or "furia" not in h.estados:
            return "Jean não está na Fúria"
        if h.ef("furia_sem_freio") and h.estados["furia"]["vezes"] < 2:
            return f"Fúria Sem Freio: sai depois de 2 vezes ({h.estados['furia']['vezes']}/2)"
        return None

    def pode_sair_furia(self):
        return self.aguardando == "heroi" and "furia" in self.heroi.estados

    def sair_furia(self):
        mot = self.motivo_sair_furia()
        if mot:
            return {"ok": False, "motivo": mot}
        h = self.heroi
        self._nova_cadeia("Jean sai da Fúria")
        del h.estados["furia"]
        self.ev("acao", "Jean sai da Fúria.", ator=h.id)
        self.ganhar_recurso(h, 12, "sair_furia")
        self.dar_ficha(h, "guarda", fonte=h)
        if h.ef("sangue_frio"):
            for a in self.grupo():
                if a is not h:
                    self.dar_ficha(a, "guarda", fonte=h)
        self.decisoes.append({"rodada": self.rodada, "ator": h.id, "acao": "sair_furia", "alvo": None,
                              "cadeia": self.cadeia["n"]})
        return {"ok": True}

    def agir(self, acao, alvo=None, turno_id=None):
        if self.fim or not self.aguardando:
            return {"ok": False, "motivo": "Não é a vez de ninguém do grupo"}
        if turno_id is not None and turno_id != self.turno_id:
            return {"ok": False, "motivo": "Ação de outra vez (clique repetido)"}
        c = self.c[self.aguardando]
        if acao not in c.kit:
            return {"ok": False, "motivo": "Ação fora do kit"}
        mot = self.motivo(c, acao)
        if mot:
            return {"ok": False, "motivo": mot}
        validos = self.alvos(c, acao)
        if C.HABILIDADES[acao]["alvo"] in ("inimigos", "proprio"):
            alvo = validos[0] if C.HABILIDADES[acao]["alvo"] == "proprio" else None
        elif alvo not in validos:
            return {"ok": False, "motivo": "Alvo inválido"}
        self.decisoes.append(self._foto(c, acao, alvo))
        custo, vida, rotulo = self.custo(c, acao)
        c.recurso -= custo
        if vida:
            c.vida -= vida
        if c is self.heroi and rotulo.startswith("Grátis"):
            c.calor = 0
        if C.HABILIDADES[acao].get("ultimate"):
            c.ult_usada = True
        self._nova_cadeia(f"{c.nome}: {C.HABILIDADES[acao]['nome']}")
        self.decisoes[-1]["cadeia"] = self.cadeia["n"]
        self.ev("acao", f"{c.nome}: {C.HABILIDADES[acao]['nome']}"
                        + (f" em {self.c[alvo].nome}" if alvo and alvo != c.id else "")
                        + (f" ({rotulo})" if rotulo else "") + ".", ator=c.id)
        self.hid_atual = acao
        try:
            self._executar(c, acao, self.c[alvo] if alvo else None)
        finally:
            self.hid_atual = None
        if not self.fim:
            self._fim_da_vez(c)
            self.aguardando = None
            self._avancar()
        return {"ok": True}

    def _bater(self, c, hid, alvo, forca, rotulo=None, area=False):
        g = self._golpe_de(c, hid, alvo)
        return self.golpe(c, alvo, g[0], g[1], hid, extra=g[2], forca=forca, rotulo=rotulo or C.HABILIDADES[hid]["nome"],
                          area=area, hid=hid)

    def _executar(self, c, hid, alvo):
        nome = C.HABILIDADES[hid]["nome"]
        if hid in ("atacar", "bastao", "oportuno", "golpe_pesado", "quebra_guarda", "joelho", "sede", "talho",
                   "furia_cega", "bola_fogo", "brasa"):
            d = self._bater(c, hid, alvo, self._gastar_forca(c, hid),
                            nome + (" (Desequilibra)" if hid == "golpe_pesado" and c.ef("desequilibra") else ""))
            if hid in ("atacar", "bastao"):
                self.ganhar_recurso(c, C.BASICO_GANHA, "basico")
            elif hid == "golpe_pesado" and c.ef("desequilibra") and alvo.vivo:
                self.interromper(alvo, c)
            elif hid == "joelho" and alvo.vivo:
                self.atordoar(alvo, 1.0 if alvo.prep else 0.4, "Atordoado", c)
            elif hid == "quebra_guarda" and alvo.vivo:
                self.dar_ficha(alvo, "exposto", 1, fonte=c)
            elif hid == "sede":
                self.curar(c, round(d * 0.4), c, "sede")
                if c.ef("sede_rubra"):
                    self.ganhar_recurso(c, 6, "sede_rubra")
            elif hid == "talho":
                self.sangrar(alvo, 1, c, "talho")
            elif hid in ("bola_fogo", "brasa"):
                self.acender(alvo, 2 if hid == "bola_fogo" and c.ef("bola_pesada") else 1, c, hid, hid=hid)
        elif hid == "defender":
            self.dar_ficha(c, "guarda", fonte=c)
            self.ganhar_recurso(c, C.BASICO_GANHA, "basico")
        elif hid in ("erguer_escudo", "barreira"):
            self.dar_ficha(alvo, "guarda", fonte=c)
        elif hid == "provocar":
            for e in self.vivos("inimigo"):
                e.estados["provocado"] = {"por": c.id}
            self.ev("estado", "Todos os inimigos miram Jean na próxima vez deles.")
            self.dar_ficha(c, "guarda", fonte=c)
            if c.ef("provoca_revide"):
                c.estados["rancor"] = {"ja": []}
                self.ev("estado", "Até a próxima vez de Jean, ele revida o primeiro golpe de cada inimigo.")
        elif hid == "grito_guerra":
            for a in self.grupo():
                if a is not c:
                    self.dar_ficha(a, "forca", fonte=c)
        elif hid == "escudo_alto":
            n = c.fichas["guarda"]
            forca = self._gastar_forca(c, hid)
            g = self._golpe_de(c, hid, alvo)
            c.fichas["guarda"] = 0
            if n:
                self.ev("ficha", f"Escudo Alto consome {n} Guarda{'s' if n > 1 else ''}.")
            self.golpe(c, alvo, g[0], g[1], hid, forca=forca, rotulo=nome, hid=hid)
        elif hid == "rugido":
            self._bater(c, hid, alvo, self._gastar_forca(c, hid))
            if c.vivo:
                self.entrar_furia(c)
            if c.ef("desafiador"):
                for e in self.vivos("inimigo"):
                    e.estados["provocado"] = {"por": c.id}
                self.ev("estado", "Todos os inimigos miram Jean na próxima vez deles.")
        elif hid == "redemoinho":
            forca = self._gastar_forca(c, hid)
            for e in list(self.vivos("inimigo")):
                if e.vivo:
                    self._bater(c, hid, e, forca, area=True)
                    if c.ef("redemoinho_sangrento"):
                        self.sangrar(e, 1, c, "redemoinho")
        elif hid == "abrir_feridas":
            camadas = (alvo.sangra or {}).get("camadas", 0)
            forca = self._gastar_forca(c, hid)
            g = self._golpe_de(c, hid, alvo)
            alvo.sangra, alvo.abertas = None, camadas
            if camadas:
                self.ev("detona", f"Abrir Feridas: abre {camadas} camada{'s' if camadas > 1 else ''} em {alvo.nome}.",
                        alvo=alvo.id)
            self.golpe(c, alvo, g[0], g[1], hid, forca=forca, rotulo=nome, hid=hid)
            alvo.abertas = 0
            if c.ef("hemorragia") and camadas:
                self.curar(c, 5 * camadas, c, "hemorragia")
        elif hid == "cerrar_dentes":
            c.estados["cerrado"] = {}
            self.ev("estado", "Jean cerra os dentes: recebe −30% e ganha 5 de Vigor por golpe até a próxima vez dele.")
        elif hid == "estandarte":
            self.invocar(c, "estandarte")
        elif hid == "muralha_viva":
            c.estados["muralha"] = {}
            self.ev("estado", "Até a próxima vez de Jean, todos os golpes contra o grupo vêm para ele.")
            self.dar_ficha(c, "guarda", 2, fonte=c)
        elif hid == "lanca":
            congelado = alvo.estados.get("atordoado", {}).get("rotulo") == "Congelado"
            prep = bool(alvo.prep)
            self._bater(c, hid, alvo, self._gastar_forca(c, hid),
                        nome + (" (Estilhaço)" if c.ef("estilhaco") and congelado else ""))
            if alvo.vivo and not c.ef("estilhaco"):
                self.resfriar(alvo, 2 if prep else 1, c, "lanca", hid="lanca")
        elif hid == "nevasca":
            forca = self._gastar_forca(c, hid)
            for e in list(self.vivos("inimigo")):
                if e.vivo:
                    self._bater(c, hid, e, forca, area=True)
                    self.resfriar(e, 1, c, "nevasca", hid="nevasca")
        elif hid == "inverno":
            for e in list(self.vivos("inimigo")):
                self.resfriar(e, 2, c, "inverno", hid="inverno")
            for a in self.vivos("aliado"):
                self.dar_ficha(a, "guarda", fonte=c)
        elif hid == "chuva":
            densa = c.ef("chuva_densa")
            forca = 1.0 if densa else self._gastar_forca(c, hid)
            for e in list(self.vivos("inimigo")):
                if not e.vivo:
                    continue
                if not densa:
                    self._bater(c, hid, e, forca, area=True)
                self.acender(e, 2 if densa else 1, c, hid, hid=hid)
        elif hid == "combustao":
            if alvo.lado == "aliado":
                self.sacrificar(alvo)
            elif c.ef("pavio"):
                alvo.estados["pavio"] = {"mult": 1.5}
                self.ev("estado", f"{alvo.nome}: pavio aceso (detona no começo da próxima vez dele, +50%).",
                        alvo=alvo.id)
            else:
                camadas = self.detonar(alvo, "combustao", forca=self._gastar_forca(c, hid), rotulo=nome)
                if c.ef("contagio") and camadas:
                    outros = [x for x in self.vivos("inimigo") if x is not alvo]
                    if outros:
                        t = max(outros, key=lambda x: ((x.queima or {}).get("camadas", 0), -x.vida))
                        n = (camadas + 1) // 2
                        self.ev("estado", f"Contágio: {n} camada{'s' if n > 1 else ''} para {t.nome}.")
                        self.acender(t, n, c, "contagio")
        elif hid == "conflagracao":
            forca = self._gastar_forca(c, hid)
            for e in list(self.vivos("inimigo")):
                if e.vivo:
                    self.detonar(e, "conflagracao", forca=forca, rotulo=nome)
            if c.ef("sacrificio"):
                for inv in self.invocacoes(c):
                    self.sacrificar(inv)
        elif hid == "alastrar":
            camadas = (alvo.queima or {}).get("camadas", 0)
            if not camadas:
                self.ev("estado", f"{alvo.nome} não está em chamas: nada se alastra.")
            else:
                alvo.queima = None
                self.ev("estado", f"As {camadas} camadas de {alvo.nome} se alastram.")
                for e in list(self.vivos("inimigo")):
                    if e is not alvo:
                        falta = camadas - (e.queima or {}).get("camadas", 0)
                        if falta > 0:
                            self.acender(e, falta, c, "alastrar")
        elif hid == "escudo_chamas":
            self.dar_ficha(alvo, "guarda", fonte=c)
            alvo.estados["chamas"] = {"ate": self.rodada + 1}
            self.ev("estado", f"{alvo.nome} fica com o Escudo de Chamas até o fim da próxima rodada.")
        elif hid == "arma_flamejante":
            alvo.estados["flamejante"] = {"vezes": 1}
            self.ev("estado", f"Até o fim da próxima vez de {alvo.nome}, os golpes dele são de fogo e acendem.")
        elif hid == "fogo_fatuo":
            self.invocar(c, "fogo_fatuo")
        elif hid == "sentinela":
            self.invocar(c, "sentinela")
        elif hid == "sobrecarga":
            self.dar_ficha(c, "forca", 2, fonte=c)
            self.dar_ficha(c, "exposto", 2, fonte=c)
        elif hid == "meditar":
            self.ganhar_recurso(c, 24, "meditar")
        elif hid == "proteger":
            alvo.estados["protegido"] = {"por": c.id}
            self.ev("estado", f"Morel protege {alvo.nome} até a próxima vez dele.")
        elif hid == "prece":
            self.curar(alvo, C.HABILIDADES[hid]["cura"], c, "prece")
        elif hid == "bencao":
            self.dar_ficha(alvo, "forca", fonte=c)
        else:
            raise ValueError(f"ação sem execução: {hid}")

    # ------------------------------------------------------------ o que a tela e o registro leem
    def _foto(self, c, acao, alvo):
        """A decisão e o estado em que ela foi tomada (para a pergunta "a escolha depende do estado?")."""
        h = self.heroi
        return {"rodada": self.rodada, "ator": c.id, "acao": acao, "alvo": alvo,
                "disponiveis": [a["id"] for a in self.acoes() if a["disponivel"]],
                "grupo": {x.id: {"vida": x.vida, "recurso": x.recurso, "fichas": dict(x.fichas)}
                          for x in self.vivos("aliado")},
                "heroi": {"calor": h.calor, "furia": "furia" in h.estados},
                "inimigos": {x.id: {"vida": x.vida, "queimadura": (x.queima or {}).get("camadas", 0),
                                    "sangramento": (x.sangra or {}).get("camadas", 0), "frio": x.frio,
                                    "prep": bool(x.prep), "fichas": dict(x.fichas)}
                             for x in self.vivos("inimigo")}}

    def _estados_tela(self, x):
        out = []
        if x.queima:
            fixa = self.heroi.ef("paciente") and x.queima["camadas"] == C.CAMADAS_TETO
            out.append({"id": "queimadura", "texto": f"Queimadura {x.queima['camadas']}"
                        + (" · não expira" if fixa else f" · {x.queima['pingos']} turnos"),
                        "dica": f"Pinga {round(C.PINGO_CAMADA * x.queima['camadas'] * self.chama_viva() * x.res.get('fogo', 1.0))} "
                                "de fogo no começo da vez dele."})
        if x.sangra:
            out.append({"id": "sangramento", "texto": f"Sangramento {x.sangra['camadas']} · {x.sangra['pingos']} turnos",
                        "dica": f"Pinga {C.PINGO_CAMADA * x.sangra['camadas']} no começo da vez dele."})
        if x.frio:
            out.append({"id": "frio", "texto": f"Frio {x.frio}/3", "dica": "Com 3, congela: perde a próxima vez e o "
                                                                              "golpe preparado."})
        if x.prep:
            out.append({"id": "prep", "texto": f"Prepara: {x.prep['nome']}",
                        "dica": f"Sai na próxima vez dele: {round(x.poder * x.prep['mult'])} de dano antes de "
                                "Guarda e Fúria. Atordoar ou congelar interrompe."})
        nomes = {"furia": ("Fúria", "Causa e recebe mais nos golpes."),
                 "atordoado": (None, "Perde a próxima vez."),
                 "firme": ("Firme", "Não pode ser atordoado, congelado nem preso."),
                 "fortalecido": ("Fortalecido", "Golpes +30%."),
                 "enfraquecido": ("Enfraquecido", "Golpes −30%."),
                 "veneno": ("Envenenado", "Perde vida no começo da vez."),
                 "provocado": ("Provocado", "Mira quem provocou na próxima vez."),
                 "protegido": ("Protegido", "Os golpes vêm para Morel."),
                 "pavio": ("Pavio aceso", "Detona no começo da próxima vez dele, +50%."),
                 "chamas": ("Escudo de Chamas", "Quem o golpear ganha 1 camada."),
                 "espinhos_escudo": ("Escudo de Espinhos", "O próximo inimigo que o golpear leva dano."),
                 "marca_partilhada": ("Brasa Partilhada", "Golpes de Morel e Odette acendem 1 camada."),
                 "rancor": ("Revida", "Revida o primeiro golpe de cada inimigo até a próxima vez dele."),
                 "cerrado": ("Dentes cerrados", "Recebe −30%; cada golpe recebido dá 5 de Vigor."),
                 "muralha": ("Muralha Viva", "Todos os golpes contra o grupo vêm para ele."),
                 "flamejante": ("Arma Flamejante", "Golpes de fogo que acendem 1 camada.")}
        for k, v in x.estados.items():
            if k in nomes:
                rot, dica = nomes[k]
                rot = rot or v.get("rotulo", "Atordoado")
                if k == "furia":
                    rot += f" · {v['vezes']} vez{'es' if v['vezes'] != 1 else ''}"
                elif isinstance(v, dict) and "vezes" in v:
                    rot += f" · {v['vezes']}"
                out.append({"id": k, "texto": rot, "dica": dica})
        return out

    def estado(self):
        atual = self.aguardando
        return {
            "rodada": self.rodada, "fim": self.fim, "aguardando": atual, "turno_id": self.turno_id,
            "semente": self.semente, "encontro": self.encontro, "encontro_nome": C.ENCONTROS[self.encontro]["nome"],
            "montagem": self.montagem,
            "ordem": [{"id": x.id, "nome": x.nome, "vivo": x.vivo, "lado": x.lado,
                       "agiu": i < self.idx, "atual": i == self.idx} for i, x in enumerate(self.ordem)],
            "combatentes": [{"id": x.id, "nome": x.nome, "lado": x.lado, "vida": x.vida, "vida_max": x.vida_max,
                             "recurso": x.recurso, "recurso_max": x.recurso_max, "recurso_nome": x.recurso_nome,
                             "fichas": dict(x.fichas), "estados": self._estados_tela(x), "vivo": x.vivo,
                             "calor": x.calor if x is self.heroi and x.ef("fornalha") else None,
                             "retrato": x.retrato, "res": x.res, "invocacao": bool(x.invocacao),
                             "dono": self.c[x.dono].nome if x.dono else None}
                            for x in self.c.values() if not (x.invocacao and not x.vivo)],
            "acoes": self.acoes(), "pode_sair_furia": self.pode_sair_furia(),
            "motivo_sair_furia": self.motivo_sair_furia() if self.pode_sair_furia() else None,
            "eventos": self.eventos, "resumo": self.resumo() if self.fim else None,
        }

    def resumo(self):
        usos = {}
        for d in self.decisoes:
            k = f"{self.c[d['ator']].nome}: {C.HABILIDADES[d['acao']]['nome'] if d['acao'] in C.HABILIDADES else 'Sair da Fúria'}"
            usos[k] = usos.get(k, 0) + 1
        maiores = sorted(self.cadeias, key=lambda x: -x["elos"])[:3]
        return {"fim": self.fim, "rodadas": self.rodada,
                "vida_grupo": {x.nome: f"{x.vida}/{x.vida_max}" for x in self.c.values()
                               if x.lado == "aliado" and not x.invocacao},
                "dano_por_causa": {causa_nome(k): v for k, v in sorted(self.dano_por_causa.items(), key=lambda kv: -kv[1])},
                "dano_recebido": self.dano_recebido, "cura": self.cura_total,
                "usos": dict(sorted(usos.items(), key=lambda kv: -kv[1])),
                "cadeias": [{"n": x["n"], "rotulo": x["rotulo"], "rodada": x["rodada"], "elos": x["elos"],
                             "barrados": x["barrados"]} for x in maiores if x["elos"]],
                "barrados": sum(x["barrados"] for x in self.cadeias)}

    def registro(self):
        return {"montagem": self.montagem, "encontro": self.encontro, "semente": self.semente,
                "inimigos": [x.nome for x in self.c.values() if x.lado == "inimigo"],
                "fim": self.fim, "resumo": self.resumo(), "decisoes": self.decisoes, "eventos": self.eventos}


_CAUSAS = {"atacar": "Atacar", "bastao": "Bastão", "golpe_pesado": "Golpe Pesado", "joelho": "Golpe no Joelho",
           "quebra_guarda": "Quebra-Guarda", "rugido": "Rugido", "sede": "Sede de Sangue", "redemoinho": "Redemoinho",
           "furia_cega": "Fúria Cega", "furia_cega_seguimento": "Fúria Cega (segue)", "bola_fogo": "Bola de Fogo",
           "brasa": "Brasa", "chuva": "Chuva de Brasas", "combustao": "Combustão", "conflagracao": "Conflagração",
           "lanca": "Lança de Gelo", "nevasca": "Nevasca", "oportuno": "Golpe Oportuno", "queimadura": "Queimadura",
           "pavio": "Pavio Curto", "estouro": "Estouro", "revide": "Revide", "espinhos": "Espinhos",
           "escudo_espinhos": "Escudo de Espinhos", "cinza_fria": "Cinza Fria", "sangue_quente": "Sangue Quente",
           "prece": "Prece", "regenerar": "Regenerar", "cura_inimiga": "Cura", "folego": "Fôlego Rubro",
           "sair_furia": "Sair da Fúria", "meditar": "Meditar", "sede_rubra": "Sede Rubra", "sangramento": "Sangramento",
           "veneno": "Veneno", "talho": "Talho", "abrir_feridas": "Abrir Feridas", "escudo_alto": "Escudo Alto",
           "fatuo": "Fogo-fátuo", "hemorragia": "Hemorragia", "elo_elemental": "Elo Elemental",
           "cerrar_dentes": "Cerrar os Dentes"}


def causa_nome(k):
    return _CAUSAS.get(k, k)
