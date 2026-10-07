"""Arena de equilíbrio: um robô que luta com juízo e as contas que dizem se a luta está fácil demais.

Usada por tests/equilibrio.py (heróis típicos, por classe e nível) e tests/replay.py (a sua partida refeita).
A arena só mede lutas: não dá XP, ouro nem saque, e o herói volta igual depois de cada luta.
"""

import random
import tempfile

from rpg.combate import Combate
from rpg.jogo import Jogo
from rpg.ui import BotUI

# O que conta como "aguentou": as colunas da tabela, na ordem.
COLUNAS = [
    ("lutas", "Lutas"),
    ("nv_inimigo", "Nv inimigo"),
    ("vitorias", "Vitórias"),
    ("turnos", "Turnos"),
    ("vida_perdida", "Vida perdida"),
    ("maior_golpe", "Maior golpe"),
    ("turnos_matar", "Seus turnos p/ matar"),
    ("golpes_cair", "Golpes p/ você cair"),
    ("um_golpe", "Golpes que matam de vida cheia"),
]


class LutadorUI(BotUI):
    """Fora da luta, o robô de sempre (ao acaso). Na luta, joga como gente: habilidade forte quando dá,
    em área quando há vários inimigos, foco no mais ferido, poção quando a vida baixa."""

    def __init__(self, rng):
        super().__init__(rng, max_decisoes=10 ** 9)
        self.g = None
        self._plano = None
        self._usadas = set()  # buffs já usados nesta luta
        self._serie = None
        self.golpes = []      # (dano, vida máxima do alvo) dos seus golpes
        self.recebidos = []   # dano dos golpes inimigos em você

    # ------------------------------------------------------------ medir
    def lance(self, tipo, **d):
        if tipo == "salva":
            for x in d.get("lances", []):
                x = dict(x)
                self.lance(x.pop("tipo", None), **x)
        elif tipo == "golpe":
            if d.get("de") == "j" and d.get("em") != "j":
                self.golpes.append((d["dano"], d.get("max_hp") or 1))
            elif d.get("em") == "j" and d.get("de") not in (None, "j"):
                self.recebidos.append(d["dano"])

    # ------------------------------------------------------------ decidir
    def escolher(self, pergunta, opcoes):
        cb = self.g.combate_ativo if self.g else None
        if cb is None:
            return super().escolher(pergunta, opcoes)
        if cb._serie != self._serie:
            self._serie, self._usadas = cb._serie, set()
        metas = self.meta_opcoes or []
        if pergunta == "Sua ação:":
            return self._acao(cb, metas)
        if pergunta == "Habilidades:":
            ids = [m["habilidade"] if m else None for m in metas]
            return ids.index(self._plano) if self._plano in ids else len(opcoes) - 1
        if pergunta == "Usar qual item?":
            ids = [m.get("usar_item") if m else None for m in metas]
            return ids.index(self._plano) if self._plano in ids else len(opcoes) - 1
        if pergunta.startswith("Em quem usar"):
            return 0 if opcoes[0].startswith("Você") else len(opcoes) - 1
        if pergunta == "Alvo:":
            vivos = cb.inimigos_vivos()
            return min(range(len(vivos)), key=lambda i: vivos[i].hp)
        return super().escolher(pergunta, opcoes)

    def _acao(self, cb, metas):
        j = cb.j
        self._plano = None
        itens = next((m["itens"] for m in metas if m.get("acao") == "itens"), [])
        if j.hp < 0.35 * j.max_hp and any(m.get("usar_item") == "pocao_vida" and not m["motivo"] for m in itens):
            self._plano = "pocao_vida"
            return 2
        habs = next((m["habilidades"] for m in metas if m.get("acao") == "habilidades"), [])
        h = self._habilidade(cb, [m for m in habs if m["pode"]])
        if h:
            self._plano = h
            return 1
        return 0

    def _habilidade(self, cb, habs):
        j = cb.j
        vivos = cb.inimigos_vivos()
        for m in habs:
            if m["habilidade"] == "meditar":
                if j.rec < 0.3 * j.max_rec:
                    return "meditar"
        proprias = [m for m in habs if m["alvo_tipo"] == "proprio" and m["habilidade"] != "meditar"
                    and m["habilidade"] not in self._usadas]
        if proprias and self.rng.random() < 0.4:
            h = self.rng.choice(proprias)["habilidade"]
            self._usadas.add(h)
            return h
        area = [m for m in habs if m["alvo_tipo"] == "todos"]
        if len(vivos) >= 2 and area:
            return max(area, key=lambda m: m["custo"])["habilidade"]
        alvo = [m for m in habs if m["alvo_tipo"] == "inimigo"]
        if alvo:
            return max(alvo, key=lambda m: m["custo"])["habilidade"]
        return None


def novo_jogo(seed, classe, nome="Arena"):
    """Um jogo de verdade (mundo, vila, regras), com o robô lutador e sem XP, ouro ou saque das lutas."""
    ui = LutadorUI(random.Random(seed))
    pasta = tempfile.mkdtemp(prefix="arena_")
    g = Jogo(ui, seed=seed, pasta_saves=pasta, hardcore=False)
    ui.g = g
    g.iniciar(nome, classe)
    g.ganhar_xp = lambda *a, **k: None
    g.ganhar_ouro = lambda *a, **k: None
    g.saque_de_combate = lambda *a, **k: None
    return g


def lutar(g, inimigos, emboscada=None, titulo=None, seed=0):
    """Uma luta medida. `inimigos`: a lista, ou uma função que a cria (com o sorteio já semeado).
    Devolve um dicionário com o que a tabela precisa."""
    ui = g.ui
    g.rng.seed(seed)
    ui.rng.seed(seed + 1)
    if callable(inimigos):
        inimigos = inimigos()
    ui.golpes, ui.recebidos = [], []
    j = g.j
    hp_ini, max_hp = j.hp, j.max_hp
    r = Combate(g, inimigos, emboscada, pode_fugir=False, titulo=titulo).executar()
    tel = next(e for e in reversed(g.registro) if e["t"] == "combate")
    return {
        "resultado": r,
        "nv_inimigo": sum(e.nivel for e in inimigos) / len(inimigos),
        "turnos": tel["turnos"],
        "vida_perdida": max(0, hp_ini - max(0, j.hp)) / max_hp,
        "maior_golpe": max(ui.recebidos, default=0) / max_hp,
        "golpes": list(ui.golpes),
        "recebidos": list(ui.recebidos),
        "vida_inimigos": [e.max_hp for e in inimigos],
        "dano": tel["dano_causado"],
        "max_hp": max_hp,
    }


def turnos_matar(lutas):
    """A vida média de um inimigo ÷ o seu dano por turno (aliados à parte)."""
    vida = [v for x in lutas for v in x["vida_inimigos"]]
    dano, turnos = sum(x["dano"] for x in lutas), sum(x["turnos"] for x in lutas)
    if not vida or not dano:
        return None
    return (sum(vida) / len(vida)) / (dano / turnos)


def agregar(lutas):
    """Junta várias lutas numa linha da tabela."""
    n = len(lutas)
    golpes = [d for x in lutas for d, _ in x["golpes"]]
    recebidos = [d for x in lutas for d in x["recebidos"]]
    max_hp = sum(x["max_hp"] for x in lutas) / n
    media_recebido = sum(recebidos) / len(recebidos) if recebidos else 0
    um_golpe = [1 for x in lutas for d, v in x["golpes"] if d >= v]
    return {
        "lutas": n,
        "nv_inimigo": sum(x["nv_inimigo"] for x in lutas) / n,
        "vitorias": sum(x["resultado"] == "vitoria" for x in lutas) / n,
        "turnos": sum(x["turnos"] for x in lutas) / n,
        "vida_perdida": sum(x["vida_perdida"] for x in lutas) / n,
        "maior_golpe": max(x["maior_golpe"] for x in lutas),
        "turnos_matar": turnos_matar(lutas),
        "golpes_cair": max_hp / media_recebido if media_recebido else None,
        "um_golpe": len(um_golpe) / len(golpes) if golpes else 0,
    }


def formatar(chave, v):
    if v is None:
        return "—"
    if chave in ("vitorias", "vida_perdida", "maior_golpe", "um_golpe"):
        return f"{round(v * 100)}%"
    if chave == "lutas":
        return str(v)
    return f"{v:.1f}"


def tabela(linhas, primeira="Nv"):
    """linhas: lista de (rótulo, agregado). Devolve a tabela em markdown."""
    cab = [primeira] + [t for _, t in COLUNAS]
    out = ["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)]
    for rotulo, a in linhas:
        out.append("| " + " | ".join([str(rotulo)] + [formatar(k, a.get(k)) for k, _ in COLUNAS]) + " |")
    return "\n".join(out)
