"""Níveis, talentos, habilidades, especialização e companheiro animal."""

from .. import balanceamento as bal
from ..classes import CLASSES, COMPANHEIROS, SPECS, habilidades_ate
from ..habilidades import HABILIDADES
from ..entidades import NOMES_STATS
from .. import comitiva
from .. import talentos
from .. import telemetria
from ..telemetria import registrar


class Progressao:
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
            j.base[k] += v * bal.HEROI_CRESCIMENTO
        j.recalcular()
        j.hp = min(j.max_hp, j.hp + max(0, j.max_hp - antes_hp))  # só ganha o que o máximo aumentou
        comitiva.atualizar_vida_maxima(self)
        j.rec = min(j.max_rec, j.rec + max(0, j.max_rec - antes_rec))
        registrar(self, "nivel", stats=telemetria.instantaneo(j))
        if j.companheiro:
            j.companheiro["max_hp"] += bal.ANIMAL_VIDA_SUBIR
            j.companheiro["atk"] += bal.ANIMAL_ATK_SUBIR
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
            self.dizer("Você sente que uma encruzilhada se aproxima. Talvez ela venha na próxima noite de descanso...",
                       "magenta")

    def ganhar_ponto_talento(self, n=1):
        self.j.pontos_talento += n
        self.dizer(f"+{n} ponto de talento! (use em \"Talentos\" — você tem {self.j.pontos_talento})",
                   "amarelo+negrito")

    def menu_talentos(self):
        while True:
            j = self.j
            self.ui.mostrar_talentos(lambda: talentos.dados_arvore(j), lambda: talentos.desenhar(j),
                                     f"{j.nome_classe} · pontos disponíveis: {j.pontos_talento}")
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
                self.ui.talento_aprendido(t["nome"], j.tal(t["id"]), t["max"])

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
        if SPECS[spec].get("reage"):
            comitiva.reagir(self, *SPECS[spec]["reage"], forca=1.5)
        if SPECS[spec].get("companheiro"):
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
        hp = int(c["hp"] * (1 + bal.ANIMAL_VIDA_POR_NIVEL * (nv - 1)))
        self.j.companheiro = {"nome": nome, "tipo": tipo, "max_hp": hp, "hp": hp,
                              "atk": c["atk"] * (1 + bal.ANIMAL_ATK_POR_NIVEL * (nv - 1)), "agi": c["agi"],
                              "alcance": c["alcance"], "crit": c["crit"]}
        self.dizer(f"{nome} agora caminha ao seu lado.", "verde+negrito")
