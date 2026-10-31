"""O combate do protótipo X1 (nada no jogo): ordem fixa por Agilidade, uma vez por rodada para cada combatente, o grupo
inteiro (Jean, Morel e Odette) nas mãos do jogador, os inimigos sorteando como no jogo.

A regra das cadeias (seção 15.2 do 28)
--------------------------------------
- Uma **cadeia** é tudo o que uma ação provoca (ou o começo da vez de alguém: pingos, pavio). Cada cadeia tem um número.
- Um efeito disparado (Estouro, Revide, Fornalha, Sangue Quente, Fôlego...) tem uma **identidade**: (efeito, dono,
  motivo). O motivo é aquilo de que o efeito trata: o morto que explode, o atacante que leva o revide, o inimigo que
  deu o Calor, o alvo que curou o Sangue Quente. **Na mesma cadeia, a mesma identidade acontece uma vez.**
  - Duas mortes são dois motivos: duas explosões, mesmo que atinjam o mesmo sobrevivente.
  - Uma explosão que mata abre um motivo novo: a cadeia continua, e acaba porque cada inimigo morre uma vez.
- **Reações (Revide, espinhos, Escudo de Chamas) respondem a golpes de ação**; o dano de uma reação, de espinhos, de
  Queimadura e de explosão não é golpe de ação. Por isso espinhos e revides não se respondem.
- **Limites por rodada** ficam escritos na descrição de quem os tem (Revide, Fôlego Rubro: uma vez por rodada).
- `LIMITE_ELOS` é só uma rede de segurança: uma cadeia maior que isso é defeito do motor e para a luta com erro.

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
        self.detonadas = 0                      # camadas detonadas no golpe que está em curso (para o Estouro)
        self.calor = 0
        self.prep = None                        # golpe preparado: {"nome", "mult"}
        self.ult_usada = False
        self.efeitos = {}
        self.cura_rodada = -99

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
                         "nos": dict(montagem["nos"]), "nome": montagem.get("nome") or "Livre"}
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
        hd["kit"] = ["atacar"] + list(montagem["kit"]) + [hd["ultimate"], "defender"]
        hd["vida"] += 12 * ef.get("couro", 0)
        hd["recurso_max"] += 12 * ef.get("reserva", 0)
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
        ordem = list(self.c.values())
        self.ordem = sorted(ordem, key=lambda x: -x.agi)  # estável: no empate, o grupo antes e na ordem de criação
        self.rodada, self.idx = 1, -1
        self.eventos, self.decisoes = [], []
        self.cadeia, self.n_cadeia, self.profundidade = None, 0, 0
        self.cadeias = []
        self.rodada_feitos = set()
        self.fim, self.aguardando, self.turno_id = None, None, 0
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
    def conta(self, fonte, alvo, base, tipo, extra=1.0, forca=1.0):
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
            m *= 1.4
            partes.append("Fúria +40%")
        if fonte.ef("braco"):
            m *= 1 + 0.08 * fonte.ef("braco")
            partes.append(f"Braço Pesado +{8 * fonte.ef('braco')}%")
        if fonte.ef("ate_o_fim") and fonte.vida < fonte.vida_max / 2:
            m *= 1.3
            partes.append("Até o Fim +30%")
        if "furia" in alvo.estados:
            m *= 1.4
            partes.append("alvo na Fúria +40%")
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

    def golpe(self, fonte, alvo, base, tipo, causa, reacao=False, extra=1.0, forca=1.0, rotulo=None):
        if not alvo.vivo:
            return 0
        dano, partes = self.conta(fonte, alvo, base, tipo, extra, forca)
        if alvo.fichas["guarda"]:
            alvo.fichas["guarda"] -= 1
        elif alvo.fichas["exposto"]:
            alvo.fichas["exposto"] -= 1
        self._perder_vida(alvo, dano, fonte, causa, golpe=True, reacao=reacao, rotulo=rotulo, partes=partes,
                          tipo=tipo)
        return dano

    def _perder_vida(self, alvo, dano, fonte, causa, golpe=False, reacao=False, rotulo=None, partes=(), tipo="fogo"):
        em_chamas = alvo.queima is not None
        alvo.vida = max(0, alvo.vida - dano)
        direto = golpe or causa in ("estouro", "pavio", "espinhos", "escudo_espinhos", "cinza_fria")
        quem = f"{fonte.nome} → {alvo.nome}" if direto and fonte and fonte is not alvo else alvo.nome
        self.ev("dano", f"{rotulo or causa}: {quem}, {dano} de {C.TIPOS.get(tipo, tipo)}"
                        + (f" ({', '.join(partes)})" if partes else "") + ("" if alvo.vivo else ". Cai."),
                alvo=alvo.id, valor=dano, causa=causa, golpe=golpe, reacao=reacao)
        if fonte and fonte.lado == "aliado" and alvo.lado == "inimigo":
            self.dano_por_causa[causa] = self.dano_por_causa.get(causa, 0) + dano
        if alvo.lado == "aliado":
            self.dano_recebido += dano
        h = self.heroi
        if golpe and fonte is h and "furia" in h.estados and h.ef("sangue_quente"):
            self.disparar("sangue_quente", h, alvo, lambda: self.curar(h, round(dano * 0.15), h, "sangue_quente"),
                          f"Sangue Quente ({alvo.nome})")
        if not alvo.vivo:
            self._morreu(alvo, fonte, causa)
            return
        if golpe and fonte and fonte.lado == "aliado" and fonte is not h and alvo.lado == "inimigo" and em_chamas and (
                h.ef("partilhado") or "marca_partilhada" in alvo.estados):
            self.disparar("partilhado", h, alvo, lambda: self.acender(alvo, 1, fonte, "partilhado"),
                          f"Calor Partilhado: {fonte.nome} acende {alvo.nome}")
        if golpe and fonte and fonte.vivo and (not reacao or self.reacoes_respondem_reacoes):
            self._reagir(alvo, fonte)

    def _reagir(self, alvo, fonte):
        """Quem foi golpeado responde (Revide, espinhos, Escudo de Espinhos, Escudo de Chamas)."""
        h = self.heroi
        if alvo is h and "rancor" in h.estados and fonte.lado == "inimigo" and fonte.id not in h.estados["rancor"]:
            h.estados["rancor"].add(fonte.id)
            self.disparar("revide", h, fonte,
                          lambda: self.golpe(h, fonte, h.poder * 0.6, "fisico", "revide", reacao=True, rotulo="Revide"),
                          f"Provocação com Revide contra {fonte.nome}")
        elif alvo is h and h.ef("revide") and fonte.lado == "inimigo":
            self.disparar("revide", h, fonte,
                          lambda: self.golpe(h, fonte, h.poder * 0.6, "fisico", "revide", reacao=True, rotulo="Revide"),
                          f"Revide contra {fonte.nome}", por_rodada=True)
        if alvo.espinhos and fonte.vivo:
            self.disparar("espinhos", alvo, fonte,
                          lambda: self._perder_vida(fonte, alvo.espinhos, alvo, "espinhos", rotulo="Espinhos",
                                                    tipo="fisico"),
                          f"Espinhos de {alvo.nome}")
        if "espinhos_escudo" in alvo.estados and fonte.lado != alvo.lado and fonte.vivo:
            v = alvo.estados.pop("espinhos_escudo")["valor"]
            self.disparar("escudo_espinhos", h, fonte,
                          lambda: self._perder_vida(fonte, v, alvo, "escudo_espinhos", rotulo="Escudo de Espinhos",
                                                    tipo="fisico"),
                          f"Escudo de Espinhos fere {fonte.nome}")
        if "chamas" in alvo.estados and fonte.lado == "inimigo" and fonte.vivo:
            self.disparar("escudo_chamas", h, fonte, lambda: self.acender(fonte, 1, h, "escudo_chamas"),
                          f"Escudo de Chamas acende {fonte.nome}")
        if alvo.revida and fonte.vivo and alvo.lado == "inimigo":
            self.disparar("revide_inimigo", alvo, fonte,
                          lambda: self.golpe(alvo, fonte, alvo.revida, "fisico", "revide", reacao=True,
                                             rotulo=f"Revide de {alvo.nome}"),
                          f"{alvo.nome} revida contra {fonte.nome}")

    def _morreu(self, alvo, fonte, causa):
        camadas = max(alvo.queima["camadas"] if alvo.queima else 0, alvo.detonadas)
        alvo.queima, alvo.prep, alvo.estados, alvo.detonadas = None, None, {}, 0
        alvo.fichas = {"guarda": 0, "forca": 0, "exposto": 0}
        h = self.heroi
        if alvo.lado == "inimigo":
            if camadas and (h.ef("estouro") or (h.ef("estrondosa") and causa == "combustao")):
                self.disparar("estouro", h, alvo, lambda: self._explodir(alvo, camadas),
                              f"Estouro: {alvo.nome} explode ({camadas} camada{'s' if camadas > 1 else ''})")
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
        for e in [x for x in self.vivos("inimigo")]:
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
        elif not self.vivos("aliado"):
            self.fim = "derrota"
            self.ev("fim", "Derrota.")

    # ------------------------------------------------------------ fogo
    def acender(self, alvo, n, fonte, causa):
        if not alvo.vivo:
            return
        h = self.heroi
        if fonte is h and h.ef("queimar") and h.vida < h.vida_max / 2:
            n += 1
        c0 = alvo.queima["camadas"] if alvo.queima else 0
        c = min(C.CAMADAS_TETO, c0 + n)
        alvo.queima = {"camadas": c, "pingos": C.PINGOS}
        self.ev("acende", f"{alvo.nome}: Queimadura {c0} → {c}.", alvo=alvo.id, causa=causa)

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

    def curar(self, alvo, n, fonte, causa):
        if not alvo.vivo or n <= 0:
            return 0
        real = min(n, alvo.vida_max - alvo.vida)
        alvo.vida += real
        self.ev("cura", f"{causa_nome(causa)}: {alvo.nome} +{real} de vida.", alvo=alvo.id, valor=real)
        if alvo.lado == "aliado":
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
        for x in self.c.values():  # o Proteger de Morel acaba na próxima vez dele
            if x.estados.get("protegido", {}).get("por") == c.id:
                del x.estados["protegido"]
        c.estados.pop("rancor", None)  # a Provocação com Revide vale até a próxima vez de quem provocou
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
        for est, rotulo in (("sangramento", "Sangramento"), ("veneno", "Veneno")):
            s = c.estados.get(est)
            if s:
                self._perder_vida(c, s["valor"], None, est, rotulo=rotulo, tipo="fisico")
                if not c.vivo or self.fim:
                    return
                s["pingos"] -= 1
                if s["pingos"] <= 0:
                    del c.estados[est]
        if c.lado == "aliado" and c.recurso_max:
            self.ganhar_recurso(c, C.REGEN, "regen")

    def _fim_da_vez(self, c):
        for k in ("fortalecido", "enfraquecido", "firme"):
            s = c.estados.get(k)
            if s:
                s["vezes"] -= 1
                if s["vezes"] <= 0:
                    del c.estados[k]

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
        if p and self.c[p["por"]].vivo:
            alvo = self.c[p["por"]]
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
        if h == "maldicao":
            self.ev("acao", f"{e.nome}: Maldição em {alvo.nome}.", ator=e.id)
            alvo.estados["enfraquecido"] = {"vezes": 3}
            self.ev("estado", f"{alvo.nome} fica Enfraquecido (−30%) por 3 vezes.", alvo=alvo.id)
            return
        self.ev("acao", f"{e.nome}: {nome} em {alvo.nome}.", ator=e.id)
        if h == "bola_fogo":
            self.golpe(e, alvo, e.magia * 1.3, "fogo", "inimigo", rotulo="Bola de Fogo")
            return
        mult = {"mordida": 1.0, "golpe_sujo": 1.1, "veneno": 0.8, "agarrar": 0.8}[h]
        self.golpe(e, alvo, e.poder * mult, e.tipo_golpe, "inimigo", rotulo=nome)
        if not alvo.vivo or self.fim:
            return
        if h == "mordida" and self.rng_sorte.random() < 0.7:
            alvo.estados["sangramento"] = {"valor": 2, "pingos": 3}
            self.ev("estado", f"{alvo.nome} sangra (2 por turno, 3 turnos).", alvo=alvo.id)
        elif h == "veneno":
            alvo.estados["veneno"] = {"valor": 2, "pingos": 3}
            self.ev("estado", f"{alvo.nome} fica envenenado (2 por turno, 3 turnos).", alvo=alvo.id)
        elif h == "golpe_sujo" and self.rng_sorte.random() < 0.35:
            alvo.estados["enfraquecido"] = {"vezes": 2}
            self.ev("estado", f"{alvo.nome} fica Enfraquecido (−30%) por 2 vezes.", alvo=alvo.id)
        elif h == "agarrar":
            self.atordoar(alvo, 0.4, "Preso", e)

    # ------------------------------------------------------------ as ações do grupo
    def custo(self, c, hid):
        """(custo em recurso, custo em vida, rótulo) da ação agora, ou None se não dá para pagar."""
        h = C.HABILIDADES[hid]
        if c is not self.heroi:
            return (h["custo"], 0, f"{h['custo']} de {c.recurso_nome}" if h["custo"] else "")
        custo = M.custo_habilidade(c.efeitos, hid)
        fogo = "fogo" in h["etiquetas"]
        if fogo and c.calor >= 3 and custo:
            return (0, 0, "Grátis: 3 Calor")
        if c.recurso >= custo:
            return (custo, 0, f"{custo} de {c.recurso_nome}" if custo else "")
        falta = custo - c.recurso
        if fogo and c.ef("pagar_vida") and c.vida > falta:
            return (c.recurso, falta, f"{c.recurso} de {c.recurso_nome} + {falta} de vida")
        return None

    def _custo_base(self, c, hid):
        return M.custo_habilidade(c.efeitos, hid) if c is self.heroi else C.HABILIDADES[hid]["custo"]

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
            return [x.id for x in self.vivos("inimigo")]
        if a == "aliado":
            return [x.id for x in self.vivos("aliado")]
        if a == "aliado_outro":
            return [x.id for x in self.vivos("aliado") if x is not c]
        return [c.id]

    def _forca_prevista(self, c, hid):
        if hid == "golpe_pesado" and c.ef("acumulado"):
            return 1 + 0.5 * sum(x.fichas["forca"] for x in self.vivos("aliado"))
        return 1.5 if c.fichas["forca"] else 1.0

    def _gastar_forca(self, c, hid):
        f = self._forca_prevista(c, hid)
        if hid == "golpe_pesado" and c.ef("acumulado"):
            n = sum(x.fichas["forca"] for x in self.vivos("aliado"))
            for x in self.vivos("aliado"):
                x.fichas["forca"] = 0
            if n:
                self.ev("ficha", f"Golpe Acumulado consome {n} Força{'s' if n > 1 else ''} do grupo.")
        elif c.fichas["forca"]:
            c.fichas["forca"] -= 1
        return f

    def _golpe_de(self, c, hid, alvo):
        """(base, tipo, extra) do golpe principal da ação, ou None se ela não golpeia agora."""
        h = C.HABILIDADES[hid]
        if hid == "combustao" and c.ef("pavio"):
            return None
        if hid in ("combustao", "conflagracao"):
            return (self.base_detonacao(alvo), "fogo", 1.0)
        if hid == "chuva" and c.ef("chuva_densa"):
            return None
        if hid == "rugido" and c.ef("contido"):
            return None
        if "mult" not in h:
            return None
        mult = h["mult"]
        if hid == "golpe_pesado" and c.ef("desequilibra"):
            mult = 1.1
        if hid == "redemoinho" and c.ef("temerario"):
            mult = 0.75
        extra = 1.0
        if hid == "oportuno" and ("atordoado" in alvo.estados or alvo.prep):
            extra = 1.6
        return (c.poder * mult, h.get("tipo", "fisico"), extra)

    def previsao(self, c, hid, alvo):
        g = self._golpe_de(c, hid, alvo)
        if not g:
            return None
        dano, _ = self.conta(c, alvo, g[0], g[1], g[2], self._forca_prevista(c, hid))
        if hid == "lanca" and c.ef("cinza_fria") and alvo.queima:
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

    def pode_sair_furia(self):
        return self.aguardando == "heroi" and "furia" in self.heroi.estados

    def sair_furia(self):
        if not self.pode_sair_furia():
            return {"ok": False, "motivo": "Jean não está na Fúria"}
        h = self.heroi
        self._nova_cadeia("Jean sai da Fúria")
        del h.estados["furia"]
        self.ev("acao", "Jean sai da Fúria.", ator=h.id)
        self.ganhar_recurso(h, 12, "sair_furia")
        self.dar_ficha(h, "guarda", fonte=h)
        if h.ef("sangue_frio"):
            for a in self.vivos("aliado"):
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
        self._executar(c, acao, self.c[alvo] if alvo else None)
        if not self.fim:
            self._fim_da_vez(c)
            self.aguardando = None
            self._avancar()
        return {"ok": True}

    def _executar(self, c, hid, alvo):
        nome = C.HABILIDADES[hid]["nome"]
        if hid in ("atacar", "bastao"):
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            self.ganhar_recurso(c, C.BASICO_GANHA, "basico")
        elif hid == "defender":
            self.dar_ficha(c, "guarda", fonte=c)
            self.ganhar_recurso(c, C.BASICO_GANHA, "basico")
        elif hid == "golpe_pesado":
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid),
                       rotulo=nome + (" (Desequilibra)" if c.ef("desequilibra") else ""))
            if c.ef("desequilibra") and alvo.vivo:
                self.interromper(alvo, c)
        elif hid == "joelho":
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            if alvo.vivo:
                self.atordoar(alvo, 1.0 if alvo.prep else 0.4, "Atordoado", c)
        elif hid == "quebra_guarda":
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            if alvo.vivo:
                self.dar_ficha(alvo, "exposto", 2 if c.ef("aberto") else 1, fonte=c)
        elif hid in ("erguer_escudo", "barreira"):
            self.dar_ficha(alvo, "guarda", fonte=c)
            if hid == "erguer_escudo" and c.ef("escudo_espinhos"):
                alvo.estados["espinhos_escudo"] = {"valor": round(c.poder * 0.6)}
                self.ev("estado", f"{alvo.nome} fica com o Escudo de Espinhos ({round(c.poder * 0.6)}).")
        elif hid == "provocar":
            for e in self.vivos("inimigo"):
                e.estados["provocado"] = {"por": c.id}
            self.ev("estado", "Todos os inimigos miram Jean na próxima vez deles.")
            self.dar_ficha(c, "guarda", fonte=c)
            if c.ef("provoca_revide"):
                c.estados["rancor"] = set()
                self.ev("estado", "Até a próxima vez de Jean, ele revida o primeiro golpe de cada inimigo.")
        elif hid == "rugido":
            if c.ef("contido"):
                self.dar_ficha(c, "guarda", fonte=c)
            else:
                g = self._golpe_de(c, hid, alvo)
                self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            if c.vivo:
                c.estados["furia"] = {}
                self.ev("estado", "Jean entra em Fúria (causa e recebe +40%).")
            if c.ef("desafiador"):
                for e in self.vivos("inimigo"):
                    e.estados["provocado"] = {"por": c.id}
                self.ev("estado", "Todos os inimigos miram Jean na próxima vez deles.")
        elif hid == "sede":
            g = self._golpe_de(c, hid, alvo)
            d = self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            self.curar(c, round(d * 0.4), c, "sede")
            if c.ef("sede_rubra"):
                self.ganhar_recurso(c, 6, "sede_rubra")
        elif hid == "redemoinho":
            g0 = C.HABILIDADES[hid]
            forca = self._gastar_forca(c, hid)
            for e in self.vivos("inimigo"):
                if e.vivo:
                    g = self._golpe_de(c, hid, e)
                    self.golpe(c, e, g[0], g[1], hid, forca=forca, rotulo=g0["nome"])
            if c.ef("temerario") and c.vivo:
                self.dar_ficha(c, "exposto", fonte=c)
        elif hid == "furia_cega":
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
        elif hid in ("bola_fogo", "brasa"):
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            self.acender(alvo, 2 if hid == "bola_fogo" and c.ef("bola_pesada") else 1, c, hid)
            if hid == "brasa" and c.ef("brasa_partilhada") and alvo.vivo:
                alvo.estados["marca_partilhada"] = {"ate": self.rodada + 1}
        elif hid == "chuva":
            densa = c.ef("chuva_densa")
            forca = 1.0 if densa else self._gastar_forca(c, hid)
            for e in self.vivos("inimigo"):
                if not e.vivo:
                    continue
                if not densa:
                    g = self._golpe_de(c, hid, e)
                    self.golpe(c, e, g[0], g[1], hid, forca=forca, rotulo=nome)
                self.acender(e, 2 if densa else 1, c, hid)
        elif hid == "combustao":
            if c.ef("pavio"):
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
                        self.ev("estado", f"Contágio: {n} camada{'s' if n > 1 else ''} passa{'m' if n > 1 else ''} "
                                          f"para {t.nome}.")
                        c0 = (t.queima or {}).get("camadas", 0)
                        t.queima = {"camadas": min(C.CAMADAS_TETO, c0 + n), "pingos": C.PINGOS}
        elif hid == "conflagracao":
            forca = self._gastar_forca(c, hid)
            for e in self.vivos("inimigo"):
                if e.vivo:
                    self.detonar(e, "conflagracao", forca=forca, rotulo=nome)
        elif hid == "lanca":
            g = self._golpe_de(c, hid, alvo)
            camadas = alvo.queima["camadas"] if (c.ef("cinza_fria") and alvo.queima) else 0
            self.golpe(c, alvo, g[0], g[1], hid, forca=self._gastar_forca(c, hid), rotulo=nome)
            if camadas and alvo.vivo:
                def cinza():
                    alvo.queima = None
                    d = max(1, round(C.DETONA_CAMADA * camadas * alvo.res.get("gelo", 1.0)))
                    self._perder_vida(alvo, d, c, "cinza_fria", rotulo="Cinza Fria", tipo="gelo")
                self.disparar("cinza_fria", c, alvo, cinza, f"Cinza Fria consome {camadas} camadas de {alvo.nome}")
            if alvo.vivo:
                self.atordoar(alvo, 0.35 + 0.15 * camadas, "Congelado", c)
        elif hid == "escudo_chamas":
            self.dar_ficha(alvo, "guarda", fonte=c)
            alvo.estados["chamas"] = {"ate": self.rodada + 1}
            self.ev("estado", f"{alvo.nome} fica com o Escudo de Chamas até o fim da próxima rodada.")
        elif hid == "meditar":
            self.ganhar_recurso(c, 24, "meditar")
        elif hid == "oportuno":
            g = self._golpe_de(c, hid, alvo)
            self.golpe(c, alvo, g[0], g[1], hid, extra=g[2], forca=self._gastar_forca(c, hid), rotulo=nome)
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
                          for x in self.c.values() if x.lado == "aliado"},
                "heroi": {"calor": h.calor, "furia": "furia" in h.estados},
                "inimigos": {x.id: {"vida": x.vida, "camadas": (x.queima or {}).get("camadas", 0),
                                    "prep": bool(x.prep), "fichas": dict(x.fichas)}
                             for x in self.c.values() if x.lado == "inimigo" and x.vivo}}

    def _estados_tela(self, x):
        out = []
        if x.queima:
            fixa = self.heroi.ef("paciente") and x.queima["camadas"] == C.CAMADAS_TETO
            out.append({"id": "queimadura", "texto": f"Queimadura {x.queima['camadas']}"
                        + (" · não expira" if fixa else f" · {x.queima['pingos']} turnos"),
                        "dica": f"Pinga {round(C.PINGO_CAMADA * x.queima['camadas'] * self.chama_viva() * x.res.get('fogo', 1.0))} "
                                "de fogo no começo da vez dele."})
        if x.prep:
            out.append({"id": "prep", "texto": f"Prepara: {x.prep['nome']}",
                        "dica": f"Sai na próxima vez dele: {round(x.poder * x.prep['mult'])} de dano antes de "
                                "Guarda e Fúria. Atordoar interrompe."})
        nomes = {"furia": ("Fúria", "Causa e recebe +40%."),
                 "atordoado": (None, "Perde a próxima vez."),
                 "firme": ("Firme", "Não pode ser atordoado, congelado nem preso."),
                 "fortalecido": ("Fortalecido", "Golpes +30%."),
                 "enfraquecido": ("Enfraquecido", "Golpes −30%."),
                 "sangramento": ("Sangrando", "Perde vida no começo da vez."),
                 "veneno": ("Envenenado", "Perde vida no começo da vez."),
                 "provocado": ("Provocado", "Mira Jean na próxima vez."),
                 "protegido": ("Protegido", "Os golpes vêm para Morel."),
                 "pavio": ("Pavio aceso", "Detona no começo da próxima vez dele, +50%."),
                 "chamas": ("Escudo de Chamas", "Quem o golpear ganha 1 camada."),
                 "espinhos_escudo": ("Escudo de Espinhos", "O próximo inimigo que o golpear leva dano."),
                 "marca_partilhada": ("Brasa Partilhada", "Golpes de Morel e Odette acendem 1 camada."),
                 "rancor": ("Revida", "Revida o primeiro golpe de cada inimigo até a próxima vez dele.")}
        for k, v in x.estados.items():
            if k in nomes:
                rot, dica = nomes[k]
                rot = rot or v.get("rotulo", "Atordoado")
                if "vezes" in v:
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
                             "retrato": x.retrato, "res": x.res}
                            for x in self.c.values()],
            "acoes": self.acoes(), "pode_sair_furia": self.pode_sair_furia(),
            "eventos": self.eventos, "resumo": self.resumo() if self.fim else None,
        }

    def resumo(self):
        usos = {}
        for d in self.decisoes:
            k = f"{self.c[d['ator']].nome}: {C.HABILIDADES[d['acao']]['nome'] if d['acao'] in C.HABILIDADES else 'Sair da Fúria'}"
            usos[k] = usos.get(k, 0) + 1
        maiores = sorted(self.cadeias, key=lambda x: -x["elos"])[:3]
        return {"fim": self.fim, "rodadas": self.rodada if self.fim != "vitoria" else self.rodada,
                "vida_grupo": {x.nome: f"{x.vida}/{x.vida_max}" for x in self.c.values() if x.lado == "aliado"},
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
           "lanca": "Lança de Gelo", "oportuno": "Golpe Oportuno", "queimadura": "Queimadura", "pavio": "Pavio Curto",
           "estouro": "Estouro", "revide": "Revide", "espinhos": "Espinhos", "escudo_espinhos": "Escudo de Espinhos",
           "cinza_fria": "Cinza Fria", "sangue_quente": "Sangue Quente", "prece": "Prece", "regenerar": "Regenerar",
           "cura_inimiga": "Cura", "folego": "Fôlego Rubro", "sair_furia": "Sair da Fúria", "meditar": "Meditar",
           "sede_rubra": "Sede Rubra", "sangramento": "Sangramento", "veneno": "Veneno"}


def causa_nome(k):
    return _CAUSAS.get(k, k)
