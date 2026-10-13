"""Ataques em área dos inimigos: quanto do dano inimigo vai para a comitiva e o peso da Varredura (o único golpe em
área de hoje, nos guardiões). Não muda o jogo: só luta e conta (roadmapIDEIAS/21).

    python -m tests.area_inimigos                 # lutas comuns e guardiões com Varredura, níveis 3, 5 e 8
    python -m tests.area_inimigos --lutas 30      # mais lutas por classe

Heróis da arena de equilíbrio (tests/equilibrio.py: subidos até o nível, equipados, com talentos), um por classe
(Berserker, Patrulheiro, Piromante), cada um com um companheiro (Odette, Morel ou Yara, pela semente, aprovação 30), na
região um nível abaixo, como no equilíbrio. Os guardiões: só os que têm a Varredura, um nível acima da região; e os
mesmos sem ela, para comparar. O robô é o lutador da arena.

Colunas: vitórias; a parte do dano dos inimigos que caiu na comitiva (o resto, em você); com que frequência o
companheiro termina a luta caído; turnos; Varreduras por luta; e quanto do dano que a comitiva recebeu veio delas.
"""

import argparse
import copy

from rpg import inimigos as fab
from rpg.combate import Combate
from rpg.dados import GUARDIOES
from tests import arena
from tests import equilibrio as eq

SPECS = (("guerreiro", "berserker"), ("arqueiro", "patrulheiro"), ("mago", "piromante"))
NIVEIS = (3, 5, 8)
COM_VARREDURA = [(b, i) for b, lista in GUARDIOES.items() for i, t in enumerate(lista) if "varredura" in t["habs"]]


def _anotar_golpes():
    """Cada golpe de um inimigo: em quem (você ou a comitiva), quanto e com que rótulo."""
    original = Combate.atacar

    def atacar(self, atacante, alvo, *a, **k):
        dano = original(self, atacante, alvo, *a, **k)
        if atacante in self.inimigos and alvo not in self.inimigos:
            self.g.ui.golpes_inimigos.append(("j" if alvo is self.j else "comitiva", dano or 0, k.get("rotulo")))
        return dano
    Combate.atacar = atacar


def medir(classe, spec, nivel, guardiao, sem_varredura, lutas):
    linhas = []
    for h in range(lutas):
        semente = 7919 * nivel + 104729 * h + 3
        g = eq.heroi(classe, spec, nivel, semente, True)
        if not g.comitiva:
            continue
        cid = g.comitiva[0]["id"]
        nv = max(1, nivel - 1)
        g.nivel_local = lambda n=nv: n
        lugares = eq.regioes(g)
        g.ui.golpes_inimigos = []
        g.j, g.comitiva = copy.deepcopy(g.j), copy.deepcopy(g.comitiva)
        g.mundo["atual"] = lugares[h % len(lugares)]["id"]
        if guardiao:
            bioma, idx = COM_VARREDURA[h % len(COM_VARREDURA)]

            def criar(bioma=bioma, idx=idx):
                e = fab.instanciar_guardiao({"bioma": bioma, "idx": idx, "nome": "Guardião"}, nv + 1)
                if sem_varredura:
                    e.habilidades = [x for x in e.habilidades if x != "varredura"]
                return [e]
            r = arena.lutar(g, criar, titulo="Guardião", seed=semente + 999)
        else:
            r = arena.lutar(g, g.grupo, seed=semente)
        golpes = g.ui.golpes_inimigos
        linhas.append({"cid": cid, "venceu": r["resultado"] == "vitoria", "caiu": bool(g.comitiva[0].get("ferido")),
                       "heroi": sum(d for em, d, _ in golpes if em == "j"),
                       "comitiva": sum(d for em, d, _ in golpes if em == "comitiva"),
                       "turnos": r["turnos"],
                       "varreduras": sum(1 for em, _, rot in golpes if rot == "Varredura" and em == "j"),
                       "varredura_comitiva": sum(d for em, d, rot in golpes if rot == "Varredura" and em == "comitiva")})
    return linhas


def linha(rotulo, ls):
    n = len(ls)
    heroi, comitiva = sum(x["heroi"] for x in ls), sum(x["comitiva"] for x in ls)
    return (f"| {rotulo} | {n} | {sum(x['venceu'] for x in ls) / n:.0%} | {comitiva / max(1, heroi + comitiva):.0%} | "
            f"{sum(x['caiu'] for x in ls) / n:.0%} | {sum(x['turnos'] for x in ls) / n:.1f} | "
            f"{sum(x['varreduras'] for x in ls) / n:.1f} | {sum(x['varredura_comitiva'] for x in ls) / max(1, comitiva):.0%} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lutas", type=int, default=30, help="lutas por classe em cada linha")
    args = ap.parse_args()
    _anotar_golpes()
    print("| Luta | Lutas | Vitórias | Dano na comitiva | Companheiro cai | Turnos | Varreduras/luta | "
          "Dano da comitiva vindo da Varredura |")
    print("|---|---|---|---|---|---|---|---|")
    for nivel in NIVEIS:
        comuns = [x for c, s in SPECS for x in medir(c, s, nivel, False, False, args.lutas)]
        print(linha(f"nv {nivel}, comuns", comuns))
        for cid, nome in (("odete", "Odette"), ("morel", "Morel"), ("yara", "Yara")):
            print(linha(f"nv {nivel}, comuns, com {nome}", [x for x in comuns if x["cid"] == cid]))
        for sem in (False, True):
            ls = [x for c, s in SPECS for x in medir(c, s, nivel, True, sem, args.lutas)]
            print(linha(f"nv {nivel}, guardião" + (" sem a Varredura" if sem else ""), ls))


if __name__ == "__main__":
    main()
