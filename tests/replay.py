"""Replay humano: uma partida de verdade refeita com os números de agora.

O registro da partida (o .jsonl que o jogo grava em <saves>/runs/) diz, em ordem, cada nível, talento,
especialização, equipamento vestido, companheiro e luta. O replay remonta o seu herói a cada luta e repete
a mesma luta (mesmos inimigos, níveis, afixos, aliados, clima e emboscada) com o robô lutador, várias vezes.

Assim dá para ver se uma mudança de balanceamento deixaria a SUA partida mais difícil, e onde.

    python -m tests.replay                         # a partida guardada em tests/runs/ (Xatuba, arqueiro)
    python -m tests.replay caminho/da/run.jsonl    # outra
    python -m tests.replay --vezes 50              # mais repetições por luta (padrão: 20)
    python -m tests.replay --lutas                 # também luta por luta
    python -m tests.replay --ficha                 # confere o herói remontado contra o registrado

Limites: o robô não joga igual a você (a linha "você" serve de régua); o equipamento é o que você vestiu,
com a força corrigida pela curva de equipamento de agora (ITEM_FORCA_*); a vida no começo de cada luta é a
que você tinha; poções: 2 por luta; bônus permanentes de eventos (santuários etc.) não estão no registro.
"""

import argparse
import copy
import glob
import json
import os

from rpg import balanceamento as bal
from rpg import comitiva
from rpg.comitiva import COMPANHEIROS as MEMBROS
from rpg.classes import COMPANHEIROS as ANIMAIS
from rpg.dados import AFIXOS, GUARDIOES
from rpg import inimigos as fab

from tests import arena

PASTA_RUNS = os.path.join(os.path.dirname(__file__), "runs")

# A curva de equipamento de quando as runs guardadas foram jogadas: com os números de agora iguais a estes,
# os itens entram exatamente como você os vestiu.
REF_ITEM_FORCA_BASE = 1.5
REF_ITEM_FORCA_POR_NIVEL = 0.9
ESCALAVEIS = ("atk", "defesa", "agi", "poder", "max_hp", "max_rec")


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def ajustar_item(bonus, nivel):
    """Os bônus do item, com a força corrigida pela curva de equipamento de agora."""
    fator = ((bal.ITEM_FORCA_BASE + nivel * bal.ITEM_FORCA_POR_NIVEL)
             / (REF_ITEM_FORCA_BASE + nivel * REF_ITEM_FORCA_POR_NIVEL))
    if fator == 1:
        return dict(bonus)
    return {k: (max(1, round(v * fator)) if k in ESCALAVEIS and v > 0 else v) for k, v in bonus.items()}


def _guardiao(nome, nivel):
    base = nome.split(", the ", 1)[-1]
    for bioma, lista in GUARDIOES.items():
        for idx, t in enumerate(lista):
            if t["base"] == base:
                return fab.instanciar_guardiao({"bioma": bioma, "idx": idx, "nome": nome}, nivel)
    return None


def _inimigo(g, x):
    """Refaz um inimigo do registro com as regras de agora."""
    if x["familia"] == "guardiao":
        return _guardiao(x["nome"], x["nivel"])
    if x["familia"] == "antagonista":
        return fab.instanciar_antagonista(g.antagonista, x["nivel"], g.corrupcao)
    unico = None
    if ", " in x["nome"]:
        unico = x["nome"].split(", ")[0]
    e = fab.criar(g.rng, x["familia"], x["nivel"], x["afixo"], nome_unico=unico)
    if unico:  # o segundo afixo dos únicos aparece no nome
        resto = x["nome"].lower()
        for k, a in AFIXOS.items():
            if k != x["afixo"] and (a["m"] in resto.split() or a["f"] in resto.split()):
                fab.adicionar_afixo(e, k)
                break
    if x["nome"].startswith(("Campeão ", "Campeã ")):
        e.max_hp = int(e.max_hp * 1.25)
        e.hp = e.max_hp
    return e


def _animal(eventos):
    """O animal do Patrulheiro (tipo e nome), visto na primeira luta em que ele aparece."""
    for ev in eventos:
        if ev["t"] == "combate":
            for a in ev.get("aliados", []):
                if a["tipo"] in ANIMAIS:
                    return a["tipo"], a["nome"]
    return None


def refazer(eventos, vezes=20):
    """Percorre o registro remontando o herói e refaz cada luta `vezes` vezes.
    Devolve uma lista de (evento da luta real, [lutas do robô], ficha remontada)."""
    cab = next(e for e in eventos if e["t"] == "cabecalho")
    ini = next(e for e in eventos if e["t"] == "inicio")
    g = arena.novo_jogo(cab["seed"], cab["classe"], ini.get("nome", "Herói"))
    animal = _animal(eventos)
    aprovacao = {}
    curto = {d["curto"]: cid for cid, d in MEMBROS.items()}
    resultado = []
    for ev in eventos:
        t, j = ev["t"], g.j  # cada luta devolve uma cópia do herói: sempre o g.j de agora
        if t == "nivel":
            g.subir_nivel()
        elif t == "talento":
            j.talentos[ev["id"]] = ev["rank"]
            j.pontos_talento = max(0, j.pontos_talento - 1)
            j.recalcular()
        elif t == "spec":
            g.especializar(ev["spec"])
            if animal and ev["spec"] == "patrulheiro":
                g.escolher_companheiro(animal[0])
                j.companheiro["nome"] = animal[1]
        elif t == "equipar":
            slot = ev["slot"]
            j.equip[slot] = {"nome": ev["item"], "slot": "anel" if slot.startswith("anel") else slot,
                             "raridade": ev.get("raridade", "comum"), "bonus": ajustar_item(ev["bonus"], ev["nv"]),
                             "classe": None if slot.startswith("anel") or slot == "amuleto" else j.classe}
            j.recalcular()
        elif t == "comitiva" and "aprovacao" in ev:
            aprovacao[ev["id"]] = ev["aprovacao"]
        elif t == "comitiva" and ev.get("acao") == "entra":
            aprovacao.setdefault(ev["id"], 0)
        elif t == "combate":
            lutas = _refazer_luta(g, ev, aprovacao, curto, vezes)
            ficha = {k: getattr(g.j, k) for k in ("atk", "defesa", "agi", "poder", "max_hp")}
            resultado.append((ev, lutas, ficha))
            # o bestiário segue a partida real (mestre caçador: +10% depois de 5 abates da família)
            for x in ev["inimigos"]:
                if x["morto"] and x["familia"] in g.bestiario:
                    g.bestiario[x["familia"]]["abates"] += 1
    return resultado


def _refazer_luta(g, ev, aprovacao, curto, vezes):
    j = g.j
    salvo = copy.deepcopy(j), copy.deepcopy(g.bestiario)
    lutas = []
    for k in range(vezes):
        g.j = j = copy.deepcopy(salvo[0])
        g.bestiario = copy.deepcopy(salvo[1])
        st = ev.get("stats_inicio") or {}
        j.hp = max(1, round(ev["hp_inicio"] / max(1, st.get("max_hp", ev["hp_max"])) * j.max_hp))
        j.rec = min(j.max_rec, max(0, round(ev["rec_inicio"] / max(1, st.get("max_rec", ev["rec_max"])) * j.max_rec)))
        j.flechas = max(j.flechas, 30)
        j.consumiveis["pocao_vida"] = 2
        j.consumiveis["bandagem"] = 2
        j.ferimentos, j.fome, j.efeitos = [], 0, {}
        j.recalcular()
        g.clima, g.periodo, g.sem_luz = ev.get("clima", "limpo"), ev.get("periodo", 0), ev.get("sem_luz", False)
        # quem lutou ao seu lado nesta luta
        g.comitiva = []
        nomes = {a["nome"]: a for a in ev.get("aliados", [])}
        for nome, a in nomes.items():
            if a["tipo"] == "comitiva" and nome in curto:
                m = comitiva.recrutar(g, curto[nome])
                if m:
                    m["aprovacao"] = aprovacao.get(curto[nome], 0)
        if j.companheiro:
            presente = any(a["tipo"] in ANIMAIS for a in ev.get("aliados", []))
            j.companheiro["hp"] = j.companheiro["max_hp"] if presente else 0
        fila = [x for x in ev["inimigos"] if "(invocado)" not in x["nome"]]
        lutas.append(arena.lutar(g, lambda: [e for e in (_inimigo(g, x) for x in fila) if e],
                                 emboscada=ev.get("emboscada"), titulo=ev.get("titulo"), seed=1000 * ev["passo"] + k))
    g.j = copy.deepcopy(salvo[0])
    g.bestiario = salvo[1]
    g.comitiva = []
    return lutas


def real(ev):
    """A luta como ela aconteceu, no formato da arena (o que o registro permite saber)."""
    st = ev.get("stats_inicio") or {}
    max_hp = st.get("max_hp", ev["hp_max"])
    vida = [x["hp_max"] for x in ev["inimigos"] if "(invocado)" not in x["nome"]]
    return {"resultado": ev["resultado"], "nv_inimigo": sum(x["nivel"] for x in ev["inimigos"]) / len(ev["inimigos"]),
            "turnos": ev["turnos"], "vida_perdida": max(0, ev["hp_inicio"] - ev["hp_fim"]) / max_hp,
            "maior_golpe": ev["maior_golpe"] / max_hp, "golpes": [], "dano": ev["dano_causado"],
            "recebidos": [], "vida_inimigos": vida, "max_hp": max_hp}


def agregar_real(lutas):
    a = arena.agregar(lutas)
    a["golpes_cair"] = a["um_golpe"] = None  # o registro não guarda golpe a golpe
    return a


def relatorio(caminho, vezes=20, por_luta=False, ficha=False):
    eventos = ler(caminho)
    total = sum(1 for e in eventos if e["t"] == "combate")
    cab = next(e for e in eventos if e["t"] == "cabecalho")
    ini = next(e for e in eventos if e["t"] == "inicio")
    res = refazer(eventos, vezes)
    linhas = [f"# Replay: {ini.get('nome')} ({cab['classe']}), {total} lutas × {vezes} repetições",
              "",
              "Cada nível tem duas linhas: **você** (como a luta foi de verdade) e **robô** (a mesma luta, com a",
              "sua build, refeita com os números de agora). Compare o robô antes e depois de mexer em",
              "`rpg/balanceamento.py`; a linha \"você\" é a régua de quanto o robô joga pior ou melhor.",
              "",
              "- Seus turnos p/ matar: a vida média de um inimigo ÷ o seu dano por turno (sem os aliados).",
              "- Golpes p/ você cair: sua vida máxima ÷ o dano médio de um golpe inimigo em você.",
              "- Golpes que matam de vida cheia: quantos dos seus golpes derrubariam um inimigo inteiro.",
              ""]
    niveis = sorted({ev["nv"] for ev, _, _ in res})
    tab = []
    for nv in niveis:
        do_nivel = [(ev, lutas) for ev, lutas, _ in res if ev["nv"] == nv]
        tab.append((f"{nv} você", agregar_real([real(ev) for ev, _ in do_nivel])))
        tab.append((f"{nv} robô", arena.agregar([x for _, lutas in do_nivel for x in lutas])))
    tab.append(("todas você", agregar_real([real(ev) for ev, _, _ in res])))
    tab.append(("todas robô", arena.agregar([x for _, lutas, _ in res for x in lutas])))
    linhas.append(arena.tabela(tab))
    if por_luta:
        linhas += ["", "## Luta por luta", ""]
        tab = []
        for i, (ev, lutas, _) in enumerate(res, 1):
            nomes = ", ".join(f"{x['nome']} {x['nivel']}" for x in ev["inimigos"])
            tab.append((f"{i}. nv {ev['nv']} vs {nomes} (você)", agregar_real([real(ev)])))
            tab.append((f"{i}. robô", arena.agregar(lutas)))
        linhas.append(arena.tabela(tab, "Luta"))
    if ficha:
        linhas += ["", "## Ficha: registrada × remontada", "",
                   "| Luta | Nv | Ataque | Defesa | Agilidade | Vida |", "|---|---|---|---|---|---|"]
        for i, (ev, _, f) in enumerate(res, 1):
            st = ev.get("stats_inicio") or {}
            linhas.append(f"| {i} | {ev['nv']} | " + " | ".join(
                f"{st.get(k, '?')} → {f[k]}" for k in ("atk", "defesa", "agi", "max_hp")) + " |")
    return "\n".join(linhas)


def main():
    p = argparse.ArgumentParser(description="Refaz uma partida registrada com os números de agora.")
    p.add_argument("run", nargs="?", help="o .jsonl da partida (padrão: as de tests/runs/)")
    p.add_argument("--vezes", type=int, default=20, help="repetições por luta")
    p.add_argument("--lutas", action="store_true", help="mostra luta por luta")
    p.add_argument("--ficha", action="store_true", help="confere o herói remontado contra o registrado")
    a = p.parse_args()
    runs = [a.run] if a.run else sorted(glob.glob(os.path.join(PASTA_RUNS, "*.jsonl")))
    for caminho in runs:
        print(relatorio(caminho, a.vezes, a.lutas, a.ficha))
        print()


if __name__ == "__main__":
    main()
