"""O combate do protótipo tático (nada no jogo): a luta do X1 numa grade vista de cima.

A vez de cada um (seção 4 do 29): **uma ação principal e os PM**, gastos antes e depois da ação, em quantos trechos
quiser; "Encerrar a vez" passa adiante. A ordem é a do jogo (Agilidade, fixa). O grupo é controlado pelo jogador; os
inimigos navegam pela grade (`_ia_*`).

Tudo o que a tela mostra (casas alcançáveis, alvos válidos, a área e quem ela atinge) sai das mesmas funções que a ação
usa (`movimentos`, `alvos_validos`, `previa`), para a prévia ser igual ao efeito."""
import random

from . import conteudo as C
from .grade import Arena, alinhado, direcao, distancia

LETRAS = "ABCDEF"
LIMITE_ELOS = 200


def casa_txt(c):
    return f"{c[0]},{c[1]}"


class Unidade:
    def __init__(self, uid, nome, lado, d, pos):
        self.id, self.nome, self.lado, self.pos = uid, nome, lado, tuple(pos)
        self.vida_max = self.vida = d["vida"]
        self.recurso_nome = d.get("recurso")
        self.recurso_max = self.recurso = d.get("recurso_max", 0)
        self.poder, self.agi = d["poder"], d["agi"]
        self.magia = d.get("magia", d["poder"])
        self.pm_max = d.get("pm", 3)
        self.pm = 0
        self.kit = list(d.get("kit", []))
        self.habs = list(d.get("habs", []))
        self.papel = d.get("papel", "perto")
        self.chance_hab = d.get("chance_hab", 0.35)
        self.golpe_nome = d.get("golpe", "Ataque")
        self.tipo_golpe = d.get("tipo", "fisico")
        self.alcance = tuple(d.get("alcance", (1, 1)))
        self.res = dict(d.get("res", {}))
        self.tracos = list(d.get("tracos", []))
        self.retrato = d.get("retrato")
        self.fichas = {"guarda": 0, "forca": 0, "exposto": 0}
        self.estados = {}
        self.queima = None
        self.prep = None
        self.invocacao, self.dono = False, None
        self.acao_usada = False
        self.fogo_vez = -1
        self.cura_rodada = -99
        self.detonadas = 0

    @property
    def vivo(self):
        return self.vida > 0


class Combate:
    def __init__(self, spec, encontro, talentos=(), semente=None, zona=None, inicio=None, mover_depois=None):
        if spec not in C.HEROI or encontro not in C.ENCONTROS:
            raise ValueError("especialização ou encontro desconhecido")
        validos = {o["id"]: par["id"] for par in C.TALENTOS[spec] for o in par["opcoes"]}
        talentos = [t for t in talentos if t]
        if any(t not in validos for t in talentos) or len({validos[t] for t in talentos}) != len(talentos):
            raise ValueError("talentos inválidos: um por par, da especialização")
        self.spec, self.encontro, self.talentos = spec, encontro, set(talentos)
        enc = C.ENCONTROS[encontro]
        self.semente = enc["semente"] if semente is None else int(semente)
        self.zona = C.ZONA_CONTROLE if zona is None else int(zona)
        self.mover_depois = C.MOVER_DEPOIS if mover_depois is None else bool(mover_depois)
        self.rng_ia = random.Random(f"ia-{self.semente}")
        self.rng_sorte = random.Random(f"sorte-{self.semente}")
        self.arena = Arena(C.LARGURA, C.ALTURA, enc["rochas"], enc["agua"])
        self.u = {}
        h = C.HEROI[spec]
        self.heroi = self._nova("heroi", h["nome"], "aliado", dict(h, kit=["atacar"] + h["kit"] + ["defender"]),
                                C.GRUPO_INICIO["heroi"])
        for cid, d in C.COMPANHEIROS.items():
            self._nova(cid, d["nome"], "aliado", dict(d, kit=d["kit"] + ["defender"]), C.GRUPO_INICIO[cid])
        tipos = [t for t, _ in enc["inimigos"]]
        vistos = {}
        for t, pos in enc["inimigos"]:
            vistos[t] = vistos.get(t, 0) + 1
            d = C.INIMIGOS[t]
            nome = d["nome"] + (f" {LETRAS[vistos[t] - 1]}" if tipos.count(t) > 1 else "")
            self._nova(f"{t}#{vistos[t]}", nome, "inimigo", d, pos)
        for uid, mods in (inicio or {}).items():
            un = self.u[uid]
            for k, v in mods.items():
                if k == "pos":
                    un.pos = tuple(v)
                elif k == "camadas":
                    un.queima = {"camadas": v, "pingos": C.PINGOS}
                elif k == "parado":
                    un.estados["parado"] = {}
                elif k == "prep":
                    un.prep = {"nome": "Golpe Esmagador", "mult": 2.2, "casas": [tuple(c) for c in v]}
                else:
                    setattr(un, k, v)
        self.ordem = sorted([x for x in self.u.values()], key=lambda x: -x.agi)
        self.chamas = {}               # casa -> última rodada em que queima (None: até o fim)
        self.rodada, self.idx, self.n_vez = 1, -1, 0
        self.eventos, self.comandos = [], []
        self.cadeia, self.profundidade, self.n_cadeia = None, 0, 0
        self.fim, self.aguardando, self.turno_id = None, None, 0
        self.n_invocadas = 0
        self.caca_vez = -1
        self.m = {k: 0 for k in ("mover", "acao", "encerrar", "casas_grupo", "casas_inimigos", "pm_grupo",
                                 "pm_grupo_disp", "ms_mover", "ms_acao", "ms_encerrar", "vezes_grupo",
                                 "vezes_sem_mover", "vezes_inimigo", "inimigo_sem_acao", "inimigo_parado",
                                 "colisoes", "zona_paga", "empurroes", "dano_grupo", "dano_recebido",
                                 "fogo_chao", "areas_em_aliados")}
        self._moveu = False
        self.ev("rodada", f"Rodada 1. Ordem: {', '.join(x.nome for x in self.ordem)}.")
        self._avancar()

    # ------------------------------------------------------------ montagem
    def _nova(self, uid, nome, lado, d, pos):
        un = Unidade(uid, nome, lado, d, pos)
        self.u[uid] = un
        return un

    def vivos(self, lado=None):
        return [x for x in self.u.values() if x.vivo and (lado is None or x.lado == lado)]

    def grupo(self):
        return [x for x in self.vivos("aliado") if not x.invocacao]

    def ocupantes(self):
        return {x.pos: x.lado for x in self.vivos()}

    def em(self, casa):
        return next((x for x in self.vivos() if x.pos == tuple(casa)), None)

    def tem(self, talento):
        return talento in self.talentos

    # ------------------------------------------------------------ registro e cadeias
    def ev(self, tipo, texto, **extra):
        e = {"tipo": tipo, "texto": texto, "rodada": self.rodada, "cadeia": self.cadeia["n"] if self.cadeia else 0,
             "nivel": self.profundidade, **extra}
        self.eventos.append(e)
        return e

    def _nova_cadeia(self, rotulo):
        self.n_cadeia += 1
        self.cadeia = {"n": self.n_cadeia, "rotulo": rotulo, "feitos": set(), "elos": 0}
        self.profundidade = 0

    def disparar(self, efeito, dono, motivo, fn, texto):
        chave = (efeito, dono.id, motivo.id)
        if chave in self.cadeia["feitos"]:
            self.ev("barrado", f"{texto}: já aconteceu nesta cadeia.", efeito=efeito)
            return False
        self.cadeia["feitos"].add(chave)
        self.cadeia["elos"] += 1
        if self.cadeia["elos"] > LIMITE_ELOS:
            raise RuntimeError("cadeia sem fim")
        self.ev("gatilho", texto, efeito=efeito)
        self.profundidade += 1
        try:
            fn()
        finally:
            self.profundidade -= 1
        return True

    # ------------------------------------------------------------ dano
    def conta(self, fonte, alvo, base, tipo, extra=1.0, forca=1.0):
        m, partes = extra * forca, []
        if forca != 1.0:
            partes.append("Força +50%")
        if extra != 1.0:
            partes.append(f"bônus ×{extra:g}")
        if "fortalecido" in fonte.estados:
            m *= 1.3
            partes.append("Fortalecido +30%")
        if "enfraquecido" in fonte.estados:
            m *= 0.7
            partes.append("Enfraquecido −30%")
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

    def _redirecionar(self, fonte, alvo):
        """Quem recebe um golpe de inimigo mirado num aliado: o Guarda-costas (vizinho) ou quem o Protege (vizinho)."""
        if fonte.lado != "inimigo" or alvo.lado != "aliado":
            return alvo
        h = self.heroi
        if alvo is not h and h.vivo and "guarda_costas" in h.estados and distancia(h.pos, alvo.pos) == 1:
            self.ev("protege", f"Jean (Guarda-costas) recebe o golpe no lugar de {alvo.nome}.")
            return h
        p = alvo.estados.get("protegido")
        if p and self.u[p["por"]].vivo and distancia(self.u[p["por"]].pos, alvo.pos) == 1:
            self.ev("protege", f"{self.u[p['por']].nome} entra na frente de {alvo.nome}.")
            return self.u[p["por"]]
        return alvo

    def golpe(self, fonte, alvo, base, tipo, causa, extra=1.0, forca=1.0, rotulo=None, area=False):
        if not alvo.vivo:
            return 0
        if not area:
            alvo = self._redirecionar(fonte, alvo)
        dano, partes = self.conta(fonte, alvo, base, tipo, extra, forca)
        if alvo.fichas["guarda"]:
            alvo.fichas["guarda"] -= 1
        elif alvo.fichas["exposto"]:
            alvo.fichas["exposto"] -= 1
        self.perder_vida(alvo, dano, fonte, causa, rotulo, partes, tipo)
        return dano

    def perder_vida(self, alvo, dano, fonte, causa, rotulo=None, partes=(), tipo="fisico"):
        alvo.vida = max(0, alvo.vida - dano)
        quem = f"{fonte.nome} → {alvo.nome}" if fonte and fonte is not alvo else alvo.nome
        self.ev("dano", f"{rotulo or causa}: {quem}, {dano} de {C.TIPOS.get(tipo, tipo)}"
                        + (f" ({', '.join(partes)})" if partes else "") + ("" if alvo.vivo else ". Cai."),
                alvo=alvo.id, valor=dano, causa=causa)
        if fonte and fonte.lado == "aliado" and alvo.lado == "inimigo":
            self.m["dano_grupo"] += dano
        if alvo.lado == "aliado" and not alvo.invocacao:
            self.m["dano_recebido"] += dano
        if not alvo.vivo:
            self._caiu(alvo, fonte, causa)

    def _caiu(self, alvo, fonte, causa):
        camadas = max((alvo.queima or {}).get("camadas", 0), alvo.detonadas)
        alvo.queima, alvo.prep, alvo.estados = None, None, {}
        h = self.heroi
        if alvo.lado == "inimigo":
            if camadas and self.tem("estouro"):
                self.disparar("estouro", h, alvo, lambda: self._explodir(alvo, camadas),
                              f"Estouro: {alvo.nome} explode ({camadas} camada{'s' if camadas > 1 else ''})")
            if fonte is h and self.tem("cacador") and self.aguardando == "heroi" and self.caca_vez != self.n_vez:
                self.caca_vez = self.n_vez
                h.pm += 3
                self.ev("gatilho", "Caçador: +3 PM nesta vez.", efeito="cacador")
        if not self.vivos("inimigo"):
            self.fim = "vitoria"
            self.ev("fim", "Vitória.")
        elif not self.grupo():
            self.fim = "derrota"
            self.ev("fim", "Derrota.")

    def _explodir(self, morto, camadas):
        base = 6 + 3 * camadas
        for c in self.arena.cruz(morto.pos, 1):
            x = self.em(c)
            if x and x is not morto and x.vivo:
                if x.lado == "aliado":
                    self.m["areas_em_aliados"] += 1
                self.perder_vida(x, max(1, round(base * x.res.get("fogo", 1.0))), self.heroi, "estouro",
                                 f"Explosão de {morto.nome}", tipo="fogo")
                if x.vivo:
                    self.acender(x, 1)

    def acender(self, alvo, n):
        if not alvo.vivo:
            return
        c0 = (alvo.queima or {}).get("camadas", 0)
        c = min(C.CAMADAS_TETO, c0 + n)
        alvo.queima = {"camadas": c, "pingos": C.PINGOS}
        self.ev("acende", f"{alvo.nome}: Queimadura {c0} → {c}.", alvo=alvo.id)

    def dar_ficha(self, alvo, ficha, n=1):
        oposto = {"guarda": "exposto", "exposto": "guarda"}.get(ficha)
        for _ in range(n):
            if oposto and alvo.fichas[oposto]:
                alvo.fichas[oposto] -= 1
            elif alvo.fichas[ficha] < C.FICHA_TETO:
                alvo.fichas[ficha] += 1
        self.ev("ficha", f"{alvo.nome}: {ficha.capitalize()} ({alvo.fichas[ficha]}).", alvo=alvo.id)

    def curar(self, alvo, n, causa):
        real = min(n, alvo.vida_max - alvo.vida)
        alvo.vida += real
        self.ev("cura", f"{causa}: {alvo.nome} +{real} de vida.", alvo=alvo.id)

    def atordoar(self, alvo, chance, rotulo):
        if not alvo.vivo or "firme" in alvo.estados:
            return False
        if "gigante" in alvo.tracos:
            chance /= 2
        if chance < 1 and self.rng_sorte.random() >= chance:
            self.ev("resiste", f"{alvo.nome} não fica {rotulo.lower()}.", alvo=alvo.id)
            return False
        alvo.estados["atordoado"] = {"rotulo": rotulo}
        if alvo.prep:
            self.ev("interrompe", f"{alvo.nome} perde o {alvo.prep['nome']}.", alvo=alvo.id)
            alvo.prep = None
        self.ev("estado", f"{alvo.nome} fica {rotulo.lower()}: perde a próxima vez.", alvo=alvo.id)
        return True

    # ------------------------------------------------------------ chão em chamas e deslocamentos
    def _fogo_chao(self, un):
        """Entrar numa casa em chamas, ou começar a vez nela: uma vez por vez de cada um."""
        if un.pos not in self.chamas or not un.vivo or un.fogo_vez == self.n_vez:
            return
        un.fogo_vez = self.n_vez
        self.m["fogo_chao"] += 1
        self.perder_vida(un, max(1, round(C.FOGO_CHAO * un.res.get("fogo", 1.0))), None, "chamas", "Chamas no chão",
                         tipo="fogo")
        if un.vivo:
            self.acender(un, 1)

    def andar(self, un, rota):
        """Percorre a rota casa a casa (as chamas pegam quem passa)."""
        for c in rota[1:]:
            if not un.vivo:
                return
            un.pos = c
            self._fogo_chao(un)

    def empurrar(self, un, d, n, fonte):
        if not un.vivo or d == (0, 0):
            return
        for i in range(n):
            nxt = (un.pos[0] + d[0], un.pos[1] + d[1])
            bloqueio = None if self.arena.chao(nxt) and not self.em(nxt) else (self.em(nxt) or "obstáculo")
            if bloqueio:
                falta = n - i
                dano = C.COLISAO_CASA * falta * (2 if self.tem("colisao_brutal") and fonte is self.heroi else 1)
                self.m["colisoes"] += 1
                self.ev("estado", f"{un.nome} bate {'em ' + bloqueio.nome if isinstance(bloqueio, Unidade) else 'num obstáculo'}"
                                  f" ({falta} casa{'s' if falta > 1 else ''} a menos).", alvo=un.id)
                self.perder_vida(un, dano, fonte, "colisao", "Colisão")
                if isinstance(bloqueio, Unidade) and self.tem("arremesso") and fonte is self.heroi:
                    self.perder_vida(bloqueio, dano, fonte, "colisao", "Colisão (Arremesso)")
                if un.vivo and self.tem("colisao_brutal") and fonte is self.heroi:
                    self.atordoar(un, 1.0, "Atordoado")
                return
            un.pos = nxt
            self.m["empurroes"] += 1
            self._fogo_chao(un)
            if not un.vivo:
                return
        self.ev("estado", f"{un.nome} é empurrado para {casa_txt(un.pos)}.", alvo=un.id)

    def puxar(self, un, para):
        d = direcao(un.pos, para)
        while un.vivo and distancia(un.pos, para) > 1:
            nxt = (un.pos[0] + d[0], un.pos[1] + d[1])
            if not self.arena.chao(nxt) or self.em(nxt):
                break
            un.pos = nxt
            self._fogo_chao(un)
        self.ev("estado", f"{un.nome} é puxado para {casa_txt(un.pos)}.", alvo=un.id)

    # ------------------------------------------------------------ a ordem
    def _avancar(self):
        while not self.fim:
            self.idx += 1
            if self.idx >= len(self.ordem):
                self._fim_da_rodada()
                if self.fim:
                    return
                self.idx = 0
            un = self.ordem[self.idx]
            if not un.vivo:
                continue
            self.n_vez += 1
            self._comeco_da_vez(un)
            if self.fim:
                return
            if not un.vivo:
                continue
            if "atordoado" in un.estados:
                st = un.estados.pop("atordoado")
                un.estados["firme"] = {"vezes": 2}
                self.ev("perde", f"{un.nome} ({st['rotulo'].lower()}) perde a vez e fica Firme.", alvo=un.id)
                continue
            if un.lado == "aliado":
                self.aguardando = un.id
                self.turno_id += 1
                self._moveu = False
                self.m["vezes_grupo"] += 1
                self.m["pm_grupo_disp"] += un.pm
                return
            self._agir_inimigo(un)
            if not self.fim:
                self._fim_da_vez(un)

    def _comeco_da_vez(self, un):
        self._nova_cadeia(f"Começo da vez de {un.nome}")
        for k in ("guarda_costas",):
            un.estados.pop(k, None)
        for x in self.u.values():
            if x.estados.get("protegido", {}).get("por") == un.id:
                del x.estados["protegido"]
        un.pm, un.acao_usada = un.pm_max, False
        if un.lado == "inimigo" and any(x.vivo and x.invocacao and distancia(x.pos, un.pos) == 1
                                        for x in self.u.values()):
            un.pm = max(0, un.pm - 1)
            self.ev("estado", f"{un.nome} começa ao lado da Sentinela: 1 PM a menos.", alvo=un.id)
        if un.pos in self.chamas:
            self._fogo_chao(un)
            if not un.vivo or self.fim:
                return
        if un.queima:
            d = max(1, round(C.PINGO_CAMADA * un.queima["camadas"] * un.res.get("fogo", 1.0)))
            self.perder_vida(un, d, self.heroi if un.lado == "inimigo" else None, "queimadura", "Queimadura",
                             tipo="fogo")
            if not un.vivo or self.fim:
                return
            if un.queima:
                un.queima["pingos"] -= 1
                if un.queima["pingos"] <= 0:
                    un.queima = None
        if un.recurso_max:
            un.recurso = min(un.recurso_max, un.recurso + C.REGEN)

    def _fim_da_vez(self, un):
        for k in ("fortalecido", "enfraquecido", "firme"):
            s = un.estados.get(k)
            if s:
                s["vezes"] -= 1
                if s["vezes"] <= 0:
                    del un.estados[k]

    def _fim_da_rodada(self):
        self.rodada += 1
        for c, ate in list(self.chamas.items()):
            if ate is not None and ate < self.rodada:
                del self.chamas[c]
        if self.rodada > C.LIMITE_RODADAS:
            self.fim = "empate"
            self.ev("fim", "Empate: limite de rodadas.")
            return
        self.cadeia = None
        self.ev("rodada", f"Rodada {self.rodada}.")

    # ------------------------------------------------------------ o grupo: movimento
    def movimentos(self, un=None):
        """As casas onde a unidade da vez pode parar, com o custo e o caminho."""
        un = un or self.u.get(self.aguardando)
        if not un:
            return {}
        tab = self.arena.caminhos(un.pos, un.pm, self.ocupantes(), un.lado, self.saida(un))
        ocup = self.ocupantes()
        return {c: {"custo": r, "rota": Arena.rota(tab, c)} for c, (r, _) in tab.items()
                if c != un.pos and c not in ocup}

    def saida(self, un):
        """O custo a mais para `un` sair de uma casa: a zona de controle (vizinho de um adversário) e, para os
        inimigos, a Âncora (vizinho de Jean, +2)."""
        def custo(c):
            viz = [x for x in self.vivos() if x.lado != un.lado and distancia(x.pos, c) == 1]
            if not self.zona or not viz:
                return 0
            extra = self.zona
            if un.lado == "inimigo" and self.tem("ancora") and any(x is self.heroi for x in viz):
                extra += 2
            return extra
        return custo

    def custo_rota(self, un, rota):
        """O custo real de uma rota (com a zona de controle e a Âncora)."""
        f = self.saida(un)
        return sum(1 + f(c) for c in rota[:-1])

    def mover(self, destino, ms=None, turno_id=None):
        un = self.u.get(self.aguardando)
        if not un or self.fim:
            return {"ok": False, "motivo": "Não é a vez de ninguém do grupo"}
        if turno_id is not None and turno_id != self.turno_id:
            return {"ok": False, "motivo": "Comando de outra vez"}
        destino = tuple(destino)
        mov = self.movimentos(un)
        if destino not in mov:
            return {"ok": False, "motivo": "Casa fora do alcance"}
        rota, custo = mov[destino]["rota"], mov[destino]["custo"]
        self._nova_cadeia(f"{un.nome} anda")
        zona = custo - (len(rota) - 1)
        un.pm -= custo
        self.m["mover"] += 1
        self.m["casas_grupo"] += len(rota) - 1
        self.m["pm_grupo"] += custo
        self.m["zona_paga"] += zona
        self.m["ms_mover"] += int(ms or 0)
        self._moveu = True
        self.comandos.append({"rodada": self.rodada, "ator": un.id, "tipo": "mover", "de": casa_txt(rota[0]),
                              "para": casa_txt(destino), "custo": custo, "zona": zona, "ms": ms})
        self.ev("mover", f"{un.nome} anda {len(rota) - 1} casa{'s' if len(rota) > 2 else ''} "
                         f"({custo} PM{f', {zona} da zona de controle' if zona else ''}).", ator=un.id)
        self.andar(un, rota)
        if not un.vivo and self.aguardando == un.id and not self.fim:
            self.aguardando = None
            self._avancar()
        return {"ok": True}

    # ------------------------------------------------------------ o grupo: ações
    def custo_hab(self, un, hid):
        return C.HABILIDADES[hid]["custo"]

    def _alcance_ok(self, un, h, casa):
        d = distancia(un.pos, casa)
        mn, mx = h["alcance"]
        if not mn <= d <= mx:
            return False
        if h["linha"] and d and not alinhado(un.pos, casa):
            return False
        if h["visao"] and d > 1 and not self.arena.visao(un.pos, casa, set(self.ocupantes())):
            return False
        return True

    def _investida_ok(self, un, casa):
        d = direcao(un.pos, casa)
        c = (un.pos[0] + d[0], un.pos[1] + d[1])
        while c != casa:
            if not self.arena.chao(c) or self.em(c):
                return False
            c = (c[0] + d[0], c[1] + d[1])
        return True

    def alvos_validos(self, un, hid):
        h = C.HABILIDADES[hid]
        out = []
        for x in range(self.arena.largura):
            for y in range(self.arena.altura):
                c = (x, y)
                if not self._alcance_ok(un, h, c):
                    continue
                ocup = self.em(c)
                if h["alvo"] == "inimigo" and not (ocup and ocup.lado != un.lado):
                    continue
                if h["alvo"] == "unidade" and not ocup:
                    continue
                if h["alvo"] == "aliado" and not (ocup and ocup.lado == un.lado):
                    continue
                if h["alvo"] == "proprio" and c != un.pos:
                    continue
                if h["alvo"] == "casa" and c in self.arena.rochas:
                    continue
                if h["alvo"] == "casa_vazia" and (ocup or not self.arena.chao(c)):
                    continue
                if hid == "investida" and not self._investida_ok(un, c):
                    continue
                if hid == "proteger" and ocup is un:
                    continue
                out.append(c)
        return out

    def area(self, un, hid, casa):
        """As casas que a ação atinge (a mesma conta para a prévia e para o efeito)."""
        h = C.HABILIDADES[hid]
        a = h.get("area")
        if a == "cruz":
            return self.arena.cruz(casa, 2 if hid == "chuva" and self.tem("labareda") else h.get("raio", 1))
        if a == "ao_redor":
            return self.arena.vizinhas(un.pos, oito=True)
        if a == "vizinhas":
            return self.arena.vizinhas(un.pos)
        if a == "muralha":
            return [c for c in self.arena.linha_perpendicular(un.pos, casa, 3) if self.arena.chao(c)]
        return [casa]

    def atingidos(self, un, hid, casa):
        """Quem a ação atinge na casa escolhida, já com as regras de aliados (Chamas Seletivas, só inimigos)."""
        h = C.HABILIDADES[hid]
        if hid == "muralha_fogo" or h["alvo"] in ("casa_vazia",):
            return []
        out = []
        for c in self.area(un, hid, casa):
            x = self.em(c)
            if not x or (x is un and h.get("area")):
                continue
            if hid == "redemoinho" and x.lado == un.lado:
                continue
            if hid in ("chuva", "explosao_calor") and x.lado == un.lado and self.tem("seletivas"):
                continue
            out.append(x)
        if hid == "combustao" and self.tem("combustao_area"):
            alvo = self.em(casa)
            out += [x for c in self.arena.vizinhas(casa) for x in [self.em(c)]
                    if x and x is not alvo and x.lado != un.lado and x.queima]
        return out

    def previa(self, un, hid, casa):
        h = C.HABILIDADES[hid]
        casas = self.area(un, hid, casa)
        quem = self.atingidos(un, hid, casa)
        dano = {}
        if h.get("mult"):
            forca = 1.5 if un.fichas["forca"] else 1.0
            for x in quem:
                if hid == "combustao":
                    base = un.poder * 0.4 + C.DETONA_CAMADA * (x.queima or {}).get("camadas", 0)
                else:
                    base = un.poder * h["mult"]
                dano[x.id] = self.conta(un, x, base, self._tipo(un, hid), self._extra(un, hid, x), forca)[0]
        return {"casas": [casa_txt(c) for c in casas], "atingidos": [x.id for x in quem], "dano": dano,
                "aliados": [x.id for x in quem if x.lado == un.lado]}

    def _tipo(self, un, hid):
        return C.HABILIDADES[hid].get("tipo", "fisico")

    def _extra(self, un, hid, alvo):
        if hid == "oportuno" and ("atordoado" in alvo.estados or alvo.prep or any(
                x.lado == un.lado and x is not un and distancia(x.pos, alvo.pos) == 1 for x in self.vivos())):
            return 1.6
        return 1.0

    def motivo(self, un, hid):
        if un.acao_usada:
            return "Ação já usada nesta vez"
        if un.recurso < self.custo_hab(un, hid):
            return f"Falta {self.custo_hab(un, hid) - un.recurso} de {un.recurso_nome}"
        if not self.alvos_validos(un, hid):
            return "Nenhum alvo ao alcance"
        return None

    def acoes(self):
        un = self.u.get(self.aguardando)
        if not un:
            return []
        out = []
        for hid in un.kit:
            h = C.HABILIDADES[hid]
            mot = self.motivo(un, hid)
            alvos = self.alvos_validos(un, hid) if not mot else []
            alcance = [casa_txt((x, y)) for x in range(self.arena.largura) for y in range(self.arena.altura)
                       if h["alcance"][0] <= distancia(un.pos, (x, y)) <= h["alcance"][1]
                       and (not h["linha"] or (x, y) == un.pos or alinhado(un.pos, (x, y)))]
            ocup = set(self.ocupantes())
            sem_visao = [c for c in alcance if h["visao"] and distancia(un.pos, tuple(map(int, c.split(",")))) > 1
                         and tuple(map(int, c.split(","))) not in self.arena.rochas
                         and not self.arena.visao(un.pos, tuple(map(int, c.split(","))), ocup)]
            out.append({"id": hid, "nome": h["nome"], "custo": self.custo_hab(un, hid), "sem_visao": sem_visao,
                        "pagamento": f"{self.custo_hab(un, hid)} de {un.recurso_nome}" if self.custo_hab(un, hid) else "Grátis",
                        "desc": self._desc(hid), "notas": self.notas(hid), "disponivel": not mot, "motivo": mot, "alvo": h["alvo"],
                        "alcance_txt": self._alcance_txt(h), "alcance": alcance,
                        "alvos": [casa_txt(c) for c in alvos],
                        "previas": {casa_txt(c): self.previa(un, hid, c) for c in alvos}})
        return out

    def _desc(self, hid):
        return C.HABILIDADES[hid]["desc"]

    def notas(self, hid):
        """As linhas dos talentos escolhidos que mudam a habilidade."""
        return [f"{o['nome']}: {o['texto']}" for par in C.TALENTOS[self.spec] for o in par["opcoes"]
                if o["id"] in self.talentos and hid in o.get("afeta", ())]

    @staticmethod
    def _alcance_txt(h):
        mn, mx = h["alcance"]
        if mx == 0:
            return "Em você"
        txt = f"Alcance {mn}" if mn == mx else f"Alcance {mn} a {mx}"
        if h["linha"]:
            txt += " · em linha reta"
        if not h["visao"] and mx > 1:
            txt += " · sem precisar de visão"
        elif h["visao"] and mx > 1:
            txt += " · com visão"
        return txt

    def agir(self, hid, casa, ms=None, turno_id=None):
        un = self.u.get(self.aguardando)
        if not un or self.fim:
            return {"ok": False, "motivo": "Não é a vez de ninguém do grupo"}
        if turno_id is not None and turno_id != self.turno_id:
            return {"ok": False, "motivo": "Comando de outra vez"}
        if hid not in un.kit:
            return {"ok": False, "motivo": "Ação fora do kit"}
        mot = self.motivo(un, hid)
        if mot:
            return {"ok": False, "motivo": mot}
        casa = tuple(casa) if casa is not None else un.pos
        if casa not in self.alvos_validos(un, hid):
            return {"ok": False, "motivo": "Alvo inválido"}
        h = C.HABILIDADES[hid]
        previa = self.previa(un, hid, casa)
        un.recurso -= self.custo_hab(un, hid)
        un.acao_usada = True
        self.m["acao"] += 1
        self.m["ms_acao"] += int(ms or 0)
        self.m["areas_em_aliados"] += len(previa["aliados"]) if h.get("area") else 0
        self.comandos.append({"rodada": self.rodada, "ator": un.id, "tipo": "acao", "acao": hid,
                              "casa": casa_txt(casa), "de": casa_txt(un.pos), "atingidos": previa["atingidos"],
                              "ms": ms})
        self._nova_cadeia(f"{un.nome}: {h['nome']}")
        alvo_txt = self.em(casa).nome if self.em(casa) and self.em(casa) is not un else casa_txt(casa)
        self.ev("acao", f"{un.nome}: {h['nome']}" + (f" em {alvo_txt}" if casa != un.pos else "") + ".", ator=un.id)
        if not self.mover_depois:
            un.pm = 0  # antes do efeito: o Caçador ainda dá PM para andar depois de um abate
        self._executar(un, hid, casa)
        if un.vivo and hid in ("atacar", "bastao", "defender"):
            un.recurso = min(un.recurso_max, un.recurso + C.BASICO_GANHA)
        return {"ok": True, "previa": previa}

    def encerrar(self, ms=None, turno_id=None):
        un = self.u.get(self.aguardando)
        if not un or self.fim:
            return {"ok": False, "motivo": "Não é a vez de ninguém do grupo"}
        if turno_id is not None and turno_id != self.turno_id:
            return {"ok": False, "motivo": "Comando de outra vez"}
        self.m["encerrar"] += 1
        self.m["ms_encerrar"] += int(ms or 0)
        if not self._moveu:
            self.m["vezes_sem_mover"] += 1
        self.comandos.append({"rodada": self.rodada, "ator": un.id, "tipo": "encerrar", "ms": ms,
                              "pm_sobrando": un.pm, "agiu": un.acao_usada})
        self._fim_da_vez(un)
        self.aguardando = None
        self._avancar()
        return {"ok": True}

    def _executar(self, un, hid, casa):
        h = C.HABILIDADES[hid]
        alvo = self.em(casa)
        forca = 1.0
        if h.get("mult") and un.fichas["forca"]:
            un.fichas["forca"] -= 1
            forca = 1.5
        tipo = self._tipo(un, hid)
        if hid in ("atacar", "bastao", "golpe_pesado", "oportuno", "luz", "bola_fogo"):
            self.golpe(un, alvo, un.poder * h["mult"], tipo, hid, self._extra(un, hid, alvo), forca, h["nome"])
            if hid == "bola_fogo":
                if alvo.vivo:
                    self.acender(alvo, 1)
                if self.tem("rastro"):
                    self.chamas[casa] = self.rodada + C.FOGO_RODADAS - 1
                    self.ev("estado", f"A casa {casa_txt(casa)} pega fogo.")
        elif hid == "defender":
            self.dar_ficha(un, "guarda")
        elif hid == "investida":
            d = direcao(un.pos, casa)
            parada = (casa[0] - d[0], casa[1] - d[1])
            rota = [un.pos]
            while rota[-1] != parada:
                rota.append((rota[-1][0] + d[0], rota[-1][1] + d[1]))
            self.ev("mover", f"{un.nome} avança {len(rota) - 1} casa{'s' if len(rota) > 2 else ''} (sem gastar PM).",
                    ator=un.id)
            self.andar(un, rota)
            if un.vivo:
                self.golpe(un, alvo, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"])
        elif hid == "golpe_escudo":
            d = direcao(un.pos, casa)
            self.golpe(un, alvo, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"])
            if alvo.vivo:
                self.empurrar(alvo, d, 4 if self.tem("arremesso") else h["empurra"], un)
        elif hid == "corrente":
            self.puxar(alvo, un.pos)
            if alvo.vivo:
                self.golpe(un, alvo, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"])
        elif hid == "redemoinho":
            for x in self.atingidos(un, hid, casa):
                self.golpe(un, x, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"], area=True)
        elif hid == "guarda_costas":
            un.estados["guarda_costas"] = {}
            self.ev("estado", "Até a próxima vez de Jean, os golpes contra aliados vizinhos a ele vêm para ele.")
        elif hid == "chuva":
            for x in self.atingidos(un, hid, casa):
                self.golpe(un, x, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"], area=True)
                if x.vivo:
                    self.acender(x, 1)
        elif hid == "muralha_fogo":
            ate = None if self.tem("fogo_eterno") else self.rodada + C.FOGO_RODADAS - 1
            for c in self.area(un, hid, casa):
                self.chamas[c] = ate
            self.ev("estado", f"Fogo no chão em {', '.join(casa_txt(c) for c in self.area(un, hid, casa))}"
                              + (" até o fim da luta." if ate is None else f" até o fim da rodada {ate}."))
        elif hid == "combustao":
            alvos = self.atingidos(un, hid, casa)
            for x in [alvo] + [y for y in alvos if y is not alvo]:
                if not x.vivo:
                    continue
                c = (x.queima or {}).get("camadas", 0)
                x.queima, x.detonadas = None, c
                self.golpe(un, x, un.poder * 0.4 + C.DETONA_CAMADA * c, "fogo", hid, 1.0, forca,
                           f"Combustão ({c} camada{'s' if c != 1 else ''})", area=x is not alvo)
                x.detonadas = 0
        elif hid == "explosao_calor":
            for x in self.atingidos(un, hid, casa):
                d = direcao(un.pos, x.pos)
                self.golpe(un, x, un.poder * h["mult"], tipo, hid, 1.0, forca, h["nome"], area=True)
                if x.vivo:
                    self.empurrar(x, d, h["empurra"], un)
        elif hid == "sentinela":
            for x in self.u.values():
                if x.invocacao and x.vivo and x.dono == un.id:
                    x.vida = 0
                    self.ev("estado", "A Sentinela anterior se desfaz.")
            self.n_invocadas += 1
            s = self._nova(f"sentinela#{self.n_invocadas}", C.SENTINELA["nome"], "aliado", dict(C.SENTINELA), casa)
            s.invocacao, s.dono = True, un.id
            self.ev("estado", f"A Sentinela de Gelo surge em {casa_txt(casa)}.", alvo=s.id)
        elif hid == "proteger":
            alvo.estados["protegido"] = {"por": un.id}
            self.ev("estado", f"Morel protege {alvo.nome} até a próxima vez dele (enquanto estiverem lado a lado).")
        elif hid == "prece":
            self.curar(alvo, h["cura"], "Prece")
        elif hid == "bencao":
            self.dar_ficha(alvo, "forca")
        else:
            raise ValueError(hid)

    # ------------------------------------------------------------ os inimigos
    def _alvos_inimigos(self):
        return self.vivos("aliado")

    def _custo_fogo(self, c):
        return 4 if c in self.chamas else 0

    def _rota_ate(self, e, tab, destino):
        """O trecho da rota que cabe nos PM (para antes, se a casa de parada estiver ocupada)."""
        rota = Arena.rota(tab, destino)
        corte = [c for c in rota if tab[c][0] <= e.pm]
        ocup = self.ocupantes()
        while len(corte) > 1 and corte[-1] in ocup:
            corte.pop()
        return corte

    def _andar_ia(self, e, rota):
        if len(rota) > 1:
            custo = self.custo_rota(e, rota)
            e.pm -= custo
            self.m["casas_inimigos"] += len(rota) - 1
            self.ev("mover", f"{e.nome} anda até {casa_txt(rota[-1])}.", ator=e.id)
            self.andar(e, rota)
            return True
        return False

    def _tabela(self, e, limite=None):
        return self.arena.caminhos(e.pos, limite, self.ocupantes(), e.lado, self.saida(e), self._custo_fogo)

    def _prefere(self, alvo):
        """Ordem de preferência entre alvos de mesmo custo: o grupo antes da Sentinela, depois o mais ferido."""
        return (1 if alvo.invocacao else 0, alvo.vida / alvo.vida_max)

    def _ia_perto(self, e):
        adj = [a for a in self._alvos_inimigos() if distancia(a.pos, e.pos) == 1]
        moveu = False
        if not adj:
            tab = self._tabela(e)
            ocup = self.ocupantes()
            melhor = None
            for a in self._alvos_inimigos():
                for c in self.arena.vizinhas(a.pos):
                    if c in tab and c not in ocup and self.arena.chao(c):
                        chave = (tab[c][0],) + self._prefere(a)
                        if melhor is None or chave < melhor[0]:
                            melhor = (chave, a, c)
            if melhor:
                moveu = self._andar_ia(e, self._rota_ate(e, tab, melhor[2]))
            else:  # sem caminho até ninguém: chega o mais perto possível
                perto = self.arena.caminhos(e.pos, e.pm, self.ocupantes(), e.lado, self.saida(e))
                livres = [c for c in perto if c not in self.ocupantes() or c == e.pos]
                if livres:
                    alvo = min(self._alvos_inimigos(), key=lambda a: distancia(a.pos, e.pos))
                    c = min(livres, key=lambda c: (distancia(c, alvo.pos), perto[c][0]))
                    moveu = self._andar_ia(e, Arena.rota(perto, c))
            if not e.vivo or self.fim:
                return
            adj = [a for a in self._alvos_inimigos() if distancia(a.pos, e.pos) == 1]
        self._acao_perto(e, adj, moveu)

    def _acao_perto(self, e, adj, moveu):
        sorte = self.rng_ia.random()
        globais = [h for h in e.habs if (h in ("uivo", "grito") and any("fortalecido" not in x.estados
                                                                         for x in self.vivos("inimigo")))
                   or (h == "regenerar" and e.vida <= e.vida_max * 0.7)]
        if not adj:
            if globais and sorte < e.chance_hab:
                return self._hab(e, self.rng_ia.choice(globais), None)
            self.m["inimigo_sem_acao"] += 1
            if not moveu:
                self.m["inimigo_parado"] += 1
            self.ev("acao", f"{e.nome} não alcança ninguém.", ator=e.id)
            return
        alvo = min(adj, key=self._prefere)
        habs = globais + [h for h in e.habs if h in ("esmagar", "golpe_sujo")]
        if habs and sorte < e.chance_hab:
            return self._hab(e, self.rng_ia.choice(habs), alvo)
        self.ev("acao", f"{e.nome}: {e.golpe_nome} em {alvo.nome}.", ator=e.id)
        self.golpe(e, alvo, e.poder, e.tipo_golpe, "inimigo", rotulo=e.golpe_nome)

    def _ia_longe(self, e):
        """A bruxa: cura quem precisa, ou procura uma casa com visão de um alvo, longe do grupo."""
        feridos = [x for x in self.vivos("inimigo") if x.vida < x.vida_max * 0.6]
        tab = self._tabela(e, e.pm)
        ocup = self.ocupantes()
        casas = [c for c in tab if c == e.pos or c not in ocup]
        if "cura" in e.habs and feridos and self.rodada - e.cura_rodada >= 3:
            for c in sorted(casas, key=lambda c: tab[c][0]):
                f = [x for x in feridos if distancia(c, x.pos) <= 3]
                if f:
                    self._andar_ia(e, self._rota_ate(e, tab, c) if c != e.pos else [e.pos])
                    alvo = min(f, key=lambda x: x.vida / x.vida_max)
                    e.cura_rodada = self.rodada
                    self.ev("acao", f"{e.nome}: Cura em {alvo.nome}.", ator=e.id)
                    self.curar(alvo, round(alvo.vida_max * 0.25), "Cura")
                    return
        grupo = self._alvos_inimigos()
        mn, mx = e.alcance
        melhor = None
        for c in casas:
            perto = min(distancia(c, a.pos) for a in grupo)
            for a in grupo:
                d = distancia(c, a.pos)
                if mn <= d <= mx and self.arena.visao(c, a.pos, set(ocup) - {e.pos}):
                    nota = (-min(perto, 4), 2 if perto <= 1 else 0, self._custo_fogo(c), self._prefere(a), tab[c][0])
                    if melhor is None or nota < melhor[0]:
                        melhor = (nota, c, a)
        if melhor:
            _, c, a = melhor
            if c != e.pos:
                self._andar_ia(e, self._rota_ate(e, tab, c))
            if not e.vivo or self.fim:
                return
            sorte = self.rng_ia.random()
            if "maldicao" in e.habs and sorte < 0.25 and "enfraquecido" not in a.estados:
                self.ev("acao", f"{e.nome}: Maldição em {a.nome}.", ator=e.id)
                a.estados["enfraquecido"] = {"vezes": 2}
                return
            self.ev("acao", f"{e.nome}: {e.golpe_nome} em {a.nome}.", ator=e.id)
            self.golpe(e, a, e.magia * 1.3, e.tipo_golpe, "inimigo", rotulo=e.golpe_nome)
            return
        # sem visão de ninguém: anda para uma casa a 3 do mais perto
        alvo = min(grupo, key=lambda a: distancia(a.pos, e.pos))
        c = min(casas, key=lambda c: (abs(distancia(c, alvo.pos) - 3), tab[c][0]))
        moveu = c != e.pos and self._andar_ia(e, self._rota_ate(e, tab, c))
        self.m["inimigo_sem_acao"] += 1
        if not moveu:
            self.m["inimigo_parado"] += 1
        self.ev("acao", f"{e.nome} não vê ninguém ao alcance.", ator=e.id)

    def _ia_lingua(self, e):
        """O sapo: se alguém está em linha reta a 2 ou 3 casas e à vista, puxa e morde; senão, vai até alguém."""
        if any(distancia(a.pos, e.pos) == 1 for a in self._alvos_inimigos()):
            return self._ia_perto(e)
        tab = self._tabela(e, e.pm)
        ocup = self.ocupantes()
        melhor = None
        for c in tab:
            if c != e.pos and c in ocup:
                continue
            for a in self._alvos_inimigos():
                d = distancia(c, a.pos)
                if 2 <= d <= 3 and alinhado(c, a.pos) and self.arena.visao(c, a.pos, set(ocup) - {e.pos}):
                    nota = (self._prefere(a), tab[c][0])
                    if melhor is None or nota < melhor[0]:
                        melhor = (nota, c, a)
        if not melhor:
            return self._ia_perto(e)
        _, c, a = melhor
        if c != e.pos:
            self._andar_ia(e, self._rota_ate(e, tab, c))
        if not e.vivo or self.fim or distancia(e.pos, a.pos) not in (2, 3) or not alinhado(e.pos, a.pos):
            return
        self.ev("acao", f"{e.nome}: Língua em {a.nome}.", ator=e.id)
        self.puxar(a, e.pos)
        if a.vivo and distancia(a.pos, e.pos) == 1:
            self.golpe(e, a, e.poder * 0.8, "fisico", "inimigo", rotulo="Língua")

    def _hab(self, e, h, alvo):
        nome = C.HABS_INIMIGO[h].split(":")[0]
        if h in ("uivo", "grito"):
            self.ev("acao", f"{e.nome}: {nome}. Os inimigos ficam Fortalecidos.", ator=e.id)
            for x in self.vivos("inimigo"):
                x.estados["fortalecido"] = {"vezes": 2}
        elif h == "regenerar":
            self.ev("acao", f"{e.nome}: Regenerar.", ator=e.id)
            self.curar(e, round(e.vida_max * 0.15), "Regenerar")
        elif h == "esmagar":
            casas = [c for c in self.arena.cruz(alvo.pos, 1) if c != e.pos and self.arena.chao(c)]
            e.prep = {"nome": "Golpe Esmagador", "mult": 2.2, "casas": casas}
            self.ev("prepara", f"{e.nome} ergue a arma sobre {alvo.nome}: o Golpe Esmagador cai na próxima vez dele "
                               f"nas casas marcadas.", ator=e.id)
        elif h == "golpe_sujo":
            self.ev("acao", f"{e.nome}: {nome} em {alvo.nome}.", ator=e.id)
            self.golpe(e, alvo, e.poder * 1.1, "fisico", "inimigo", rotulo=nome)
            if alvo.vivo and self.rng_sorte.random() < 0.35:
                alvo.estados["enfraquecido"] = {"vezes": 2}
                self.ev("estado", f"{alvo.nome} fica Enfraquecido.", alvo=alvo.id)

    def _agir_inimigo(self, e):
        self._nova_cadeia(f"Vez de {e.nome}")
        self.m["vezes_inimigo"] += 1
        if "parado" in e.estados:
            return
        if e.prep:
            p, e.prep = e.prep, None
            atingidos = [x for x in self.vivos("aliado") if x.pos in p["casas"]]
            self.ev("acao", f"{e.nome} solta o {p['nome']}"
                            + (f": {', '.join(x.nome for x in atingidos)}." if atingidos else ": não pega ninguém."),
                    ator=e.id)
            for x in atingidos:
                self.golpe(e, x, e.poder * p["mult"], e.tipo_golpe, "inimigo", rotulo=p["nome"], area=True)
            return
        {"longe": self._ia_longe, "lingua": self._ia_lingua}.get(e.papel, self._ia_perto)(e)

    # ------------------------------------------------------------ o que a tela e o registro leem
    def _estados_tela(self, x):
        out = []
        if x.queima:
            out.append({"id": "queimadura", "texto": f"Queimadura {x.queima['camadas']}",
                        "dica": f"Pinga {C.PINGO_CAMADA * x.queima['camadas']} de fogo no começo da vez."})
        if x.prep:
            out.append({"id": "prep", "texto": "Prepara o Golpe Esmagador",
                        "dica": f"Na próxima vez dele: {round(x.poder * x.prep['mult'])} em quem estiver nas casas "
                                "marcadas. Atordoar interrompe."})
        nomes = {"atordoado": "Atordoado", "firme": "Firme", "fortalecido": "Fortalecido", "enfraquecido": "Enfraquecido",
                 "protegido": "Protegido", "guarda_costas": "Guarda-costas"}
        for k, v in x.estados.items():
            if k in nomes:
                out.append({"id": k, "texto": nomes[k] if k != "atordoado" else v.get("rotulo", "Atordoado"),
                            "dica": ""})
        return out

    def estado(self):
        un = self.u.get(self.aguardando)
        mov = self.movimentos(un) if un and not self.fim else {}
        marcadas = {}
        for x in self.vivos("inimigo"):
            for c in (x.prep or {}).get("casas", []):
                marcadas[casa_txt(c)] = x.nome
        return {
            "versao": C.VERSAO, "rodada": self.rodada, "fim": self.fim, "aguardando": self.aguardando,
            "turno_id": self.turno_id, "spec": self.spec, "talentos": sorted(self.talentos), "zona": self.zona,
            "mover_depois": self.mover_depois,
            "encontro": self.encontro, "encontro_nome": C.ENCONTROS[self.encontro]["nome"], "semente": self.semente,
            "arena": {"largura": self.arena.largura, "altura": self.arena.altura,
                      "rochas": [casa_txt(c) for c in sorted(self.arena.rochas)],
                      "agua": [casa_txt(c) for c in sorted(self.arena.agua)],
                      "chamas": {casa_txt(c): ate for c, ate in self.chamas.items()}, "marcadas": marcadas},
            "ordem": [{"id": x.id, "nome": x.nome, "lado": x.lado, "vivo": x.vivo, "agiu": i < self.idx,
                       "atual": i == self.idx} for i, x in enumerate(self.ordem)],
            "unidades": [{"id": x.id, "nome": x.nome, "lado": x.lado, "pos": casa_txt(x.pos), "vida": x.vida,
                          "vida_max": x.vida_max, "recurso": x.recurso, "recurso_max": x.recurso_max,
                          "recurso_nome": x.recurso_nome, "pm": x.pm if x.id == self.aguardando else x.pm_max,
                          "pm_max": x.pm_max, "fichas": x.fichas, "estados": self._estados_tela(x),
                          "invocacao": x.invocacao, "retrato": x.retrato, "res": x.res,
                          "acao_usada": x.acao_usada if x.id == self.aguardando else False}
                         for x in self.u.values() if x.vivo],
            "movimento": {casa_txt(c): {"custo": v["custo"], "rota": [casa_txt(r) for r in v["rota"]]}
                          for c, v in mov.items()},
            "acoes": self.acoes() if un and not self.fim else [],
            "eventos": self.eventos, "resumo": self.resumo() if self.fim else None,
        }

    def resumo(self):
        m = self.m
        cmds = m["mover"] + m["acao"] + m["encerrar"]
        return {"fim": self.fim, "rodadas": self.rodada,
                "vida_grupo": {x.nome: f"{x.vida}/{x.vida_max}" for x in self.u.values()
                               if x.lado == "aliado" and not x.invocacao},
                "comandos": cmds, "comandos_por_vez": round(cmds / max(1, m["vezes_grupo"]), 1),
                "metricas": dict(m)}

    def registro(self):
        return {"versao": C.VERSAO, "spec": self.spec, "talentos": sorted(self.talentos), "zona": self.zona,
                "mover_depois": self.mover_depois,
                "encontro": self.encontro, "semente": self.semente, "fim": self.fim, "resumo": self.resumo(),
                "comandos": self.comandos, "eventos": self.eventos}
