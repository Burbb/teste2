"""Simulador de equilíbrio: heróis típicos de cada especialização, nível a nível, contra o que o jogo sorteia.

Para cada especialização e nível, monta vários heróis (níveis subidos como no jogo, talentos ao acaso,
equipamento sorteado no nível de quem chegou até ali, um companheiro da comitiva a partir do nível 3) e põe
cada um para lutar contra grupos do próprio jogo numa região um pouco abaixo do nível dele, e contra um
guardião. O robô lutador (tests/arena.py) joga as lutas.

    python -m tests.equilibrio                    # todas as especializações, níveis 1 a 12
    python -m tests.equilibrio --spec patrulheiro # só uma
    python -m tests.equilibrio --lutas 60         # mais lutas por nível (padrão: 30)
    python -m tests.equilibrio --atraso 2         # região 2 níveis abaixo do herói (padrão: 1)
    python -m tests.equilibrio --sozinho          # sem comitiva

Use para comparar antes e depois de mexer em rpg/balanceamento.py. Os números absolutos dependem do
robô; a direção e o tamanho da mudança é que contam.
"""

import argparse
import copy
import random

from rpg import comitiva
from rpg.classes import CLASSES, COMPANHEIROS as ANIMAIS, SPECS
from rpg import dev
from rpg import inimigos as fab
from rpg.dados import GUARDIOES

from tests import arena

NIVEIS = range(1, 13)
HEROIS = 6          # heróis diferentes (equipamento e talentos) por nível
MEMBROS = ("odete", "morel", "yara")


def heroi(classe, spec, nivel, semente, com_comitiva=True):
    g = arena.novo_jogo(semente, classe)
    rng = random.Random(semente)
    animal = rng.choice(list(ANIMAIS)) if spec == "patrulheiro" else None
    dev.subir_ate(g, nivel, spec=spec, animal=animal)
    dev.gastar_talentos(g, rng)
    dev.vestir(g, rng, nivel)
    g.comitiva = []
    if com_comitiva and nivel >= 3:
        m = comitiva.recrutar(g, MEMBROS[semente % len(MEMBROS)])
        m["aprovacao"] = 30
    return g


def regioes(g):
    """Lugares de luta do mundo (fora vilas e a cidadela), um de cada bioma."""
    vistos, lista = set(), []
    for l in g.mundo["locais"]:
        if l["tipo"] not in ("vila", "cidadela") and l["bioma"] not in vistos:
            vistos.add(l["bioma"])
            lista.append(l)
    return lista


def medir(classe, spec, nivel, lutas, atraso, com_comitiva):
    comuns, chefes = [], []
    por_heroi = max(1, lutas // HEROIS)
    for h in range(HEROIS):
        semente = 7919 * nivel + 104729 * h + list(SPECS).index(spec)
        g = heroi(classe, spec, nivel, semente, com_comitiva)
        nv_regiao = max(1, nivel - atraso)
        g.nivel_local = lambda n=nv_regiao: n
        lugares = regioes(g)
        salvo = g.j, g.comitiva, g.bestiario
        for k in range(por_heroi + 1):
            g.j, g.comitiva, g.bestiario = copy.deepcopy(salvo[0]), copy.deepcopy(salvo[1]), copy.deepcopy(salvo[2])
            g.clima, g.periodo = "limpo", 1
            if k < por_heroi:
                g.mundo["atual"] = lugares[k % len(lugares)]["id"]
                comuns.append(arena.lutar(g, g.grupo, seed=semente + k))
            else:  # um guardião da região, um nível acima dela (como no jogo)
                bioma = lugares[h % len(lugares)]["bioma"]
                spec_g = {"bioma": bioma, "idx": h % len(GUARDIOES[bioma]), "nome": "Guardião"}
                chefes.append(arena.lutar(g, lambda: [fab.instanciar_guardiao(spec_g, nv_regiao + 1)],
                                          titulo="Guardião", seed=semente + 999))
    return arena.agregar(comuns), arena.agregar(chefes)


def relatorio(specs, lutas=30, atraso=1, com_comitiva=True):
    linhas = [f"# Equilíbrio: {lutas} lutas comuns e {HEROIS} guardiões por nível; região {atraso} nível(is) "
              f"abaixo do herói; {'com' if com_comitiva else 'sem'} comitiva", ""]
    for spec in specs:
        classe = SPECS[spec]["classe"]
        tab_c, tab_g = [], []
        for nv in NIVEIS:
            c, ch = medir(classe, spec, nv, lutas, atraso, com_comitiva)
            tab_c.append((nv, c))
            tab_g.append((nv, ch))
        linhas += [f"## {CLASSES[classe]['nome']} → {SPECS[spec]['nome']}", "", "Lutas comuns:", "",
                   arena.tabela(tab_c), "", "Guardiões:", "", arena.tabela(tab_g), ""]
    return "\n".join(linhas)


def main():
    p = argparse.ArgumentParser(description="Heróis típicos de cada especialização lutando, nível a nível.")
    p.add_argument("--spec", choices=list(SPECS), action="append", help="só esta especialização (pode repetir)")
    p.add_argument("--lutas", type=int, default=30, help="lutas comuns por nível")
    p.add_argument("--atraso", type=int, default=1, help="quantos níveis a região fica abaixo do herói")
    p.add_argument("--sozinho", action="store_true", help="sem comitiva")
    a = p.parse_args()
    print(relatorio(a.spec or list(SPECS), a.lutas, a.atraso, not a.sozinho))


if __name__ == "__main__":
    main()
