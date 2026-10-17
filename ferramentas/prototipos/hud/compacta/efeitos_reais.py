"""Quantos efeitos as cartas da luta têm de verdade, ao mesmo tempo (protótipo da composição compacta, rodada 2).

O robô de tests/arena.py luta com cada especialização no nível 12, com a comitiva cheia (dois companheiros, os três
pares possíveis), o animal do patrulheiro e os servos do necromante (quantos a build controla, já de pé), contra os maiores bandos que as regras
geram (confronto.grupo: até o máximo da família mais um; os caídos com o xamã de escolta). A cada vez do herói (é
quando os menus abrem), o estado da luta é lido como a tela o recebe (rpg.web.estado.combate) e anotado: quantas
cartas de cada lado têm efeitos e quantos ícones cada uma mostra. Nada no jogo muda; as regras, os sorteios e o
robô são os de sempre.

    python ferramentas/prototipos/hud/compacta/efeitos_reais.py [lutas por combinação, padrão 8]

Grava capturas/efeitos-reais.json: o resumo por combinação e os piores momentos (o estado inteiro das cartas, para a
foto reproduzir um caso real com os mesmos efeitos).
"""
import collections
import json
import pathlib
import random
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))

from rpg import comitiva as cm  # noqa: E402
from rpg import dev  # noqa: E402
from rpg.classes import CLASSES, COMPANHEIROS as ANIMAIS  # noqa: E402
from rpg import especializacao  # noqa: E402
from rpg.modificadores import mod  # noqa: E402
from rpg.web import estado  # noqa: E402
from tests.arena import LutadorUI, lutar, novo_jogo  # noqa: E402

LUTAS = int(sys.argv[1]) if len(sys.argv) > 1 else 8
NIVEL, NIVEL_INIMIGO = 12, 10
# os maiores bandos reais: o máximo da família (dados.FAMILIAS["grupo"]) mais um (a comitiva atrai, a noite junta)
BANDOS = {"caidos e xamã": [("caido", 5), ("xama_caido", 1)], "ratos": [("rato", 5)], "lobos": [("lobo", 4)],
          "cultistas": [("cultista", 4)], "harpias": [("harpia", 4)], "cães infernais": [("cao_infernal", 4)],
          "bandidos": [("bandido", 4)], "lobos gélidos": [("lobo_gelido", 4)], "afogados": [("afogado", 4)],
          "esqueletos": [("esqueleto", 4)]}
PARES = [("morel", "odete"), ("morel", "yara"), ("odete", "yara")]
SAIDA = pathlib.Path(__file__).resolve().parent / "capturas" / "efeitos-reais.json"


def heroi(classe, spec, par, seed):
    g = novo_jogo(seed, classe)
    j = g.j
    if spec == "patrulheiro":
        g.escolher_companheiro = lambda *_: setattr(j, "companheiro", {"nome": ANIMAIS["lobo"]["nome"],
                                                                     **especializacao.animal("lobo", j.nivel)})
    dev.subir_ate(g, NIVEL, spec=spec)
    dev.gastar_talentos(g, random.Random(seed))
    for c in par:
        cm.recrutar(g, c)
    return g


def momento(g):
    """O estado das cartas como a tela recebe: os nomes e os efeitos de cada uma."""
    e = estado.combate(g)
    carta = lambda c: {"nome": c["nome"], "efeitos": c["efeitos"]} if c["vivo"] else None
    return {"turno": e["turno"], "heroi": carta(e["heroi"]),
            "aliados": [x for x in map(carta, e["aliados"]) if x], "inimigos": [x for x in map(carta, e["inimigos"]) if x]}


def main():
    resumo, piores = [], []
    preparar = cm.preparar_combate  # o combate chama o de rpg.comitiva
    for classe, d in CLASSES.items():
        for spec in d["specs"]:
            for bando, comp in BANDOS.items():
                lado = collections.Counter()
                maximo = {"cartas_aliados": 0, "cartas_inimigos": 0, "cartas_com_efeitos_aliados": 0, "cartas_com_efeitos_inimigos": 0, "icones_numa_carta": 0,
                          "icones_no_lado": 0}
                for k in range(LUTAS):
                    seed = 1000 + k
                    g = heroi(classe, spec, PARES[k % 3], seed)
                    if spec == "necromante":  # os servos de pé desde o começo, quantos a build controla (1 + servos_max)
                        def com_servos(cb, n=1 + mod(g.j, "servos_max")):
                            preparar(cb)
                            for _ in range(n):
                                cb.invocar_aliado("Esqueleto (Invocado)", hp=60, atk=8, tipo="servo")
                        cm.preparar_combate = com_servos
                    momentos = []
                    ui = g.ui
                    original = LutadorUI.escolher

                    def espiar(self, pergunta, opcoes, _m=momentos, _o=original):
                        if self.g and self.g.combate_ativo and pergunta == "Sua ação:":
                            _m.append(momento(self.g))
                        return _o(self, pergunta, opcoes)
                    ui.escolher = espiar.__get__(ui)
                    grupo = lambda: [g.inimigo(f, nivel=NIVEL_INIMIGO) for f, n in comp for _ in range(n)]
                    lutar(g, grupo, seed=seed)
                    cm.preparar_combate = preparar
                    for m in momentos:
                        al = [m["heroi"]] + m["aliados"] if m["heroi"] else m["aliados"]
                        ca = sum(1 for c in al if c["efeitos"])
                        ci = sum(1 for c in m["inimigos"] if c["efeitos"])
                        um = max((len(c["efeitos"]) for c in al + m["inimigos"]), default=0)
                        lado_i = sum(len(c["efeitos"]) for c in m["inimigos"])
                        lado_a = sum(len(c["efeitos"]) for c in al)
                        maximo["cartas_aliados"] = max(maximo["cartas_aliados"], len(al))
                        maximo["cartas_inimigos"] = max(maximo["cartas_inimigos"], len(m["inimigos"]))
                        maximo["cartas_com_efeitos_aliados"] = max(maximo["cartas_com_efeitos_aliados"], ca)
                        maximo["cartas_com_efeitos_inimigos"] = max(maximo["cartas_com_efeitos_inimigos"], ci)
                        maximo["icones_numa_carta"] = max(maximo["icones_numa_carta"], um)
                        maximo["icones_no_lado"] = max(maximo["icones_no_lado"], lado_i, lado_a)
                        lado[(len(al), ca, len(m["inimigos"]), ci)] += 1
                        piores.append({"spec": spec, "bando": bando, "seed": seed, "par": PARES[k % 3],
                                       "cartas": (len(al), len(m["inimigos"])), "com_efeitos": (ca, ci),
                                       "icones_numa_carta": um, "momento": m})
                print(f"{spec:12} {bando:15} {maximo}", flush=True)
                resumo.append({"spec": spec, "bando": bando, **maximo,
                               "momentos": sum(lado.values()),
                               "todas_as_cartas_com_efeito": sum(n for (na, ca, ni, ci), n in lado.items()
                                                                 if ca == na and ci == ni)})
    # os piores: a coluna mais alta, em linhas de carta (cada carta uma linha; cada carta com efeitos, mais uma linha de
    # ícones a cada 4: o que cabe numa carta de 1280×720), depois o maior número de ícones numa carta
    linhas = lambda cs: sum(1 + -(-len(c["efeitos"]) // 4) for c in cs if c)
    for p in piores:
        m = p["momento"]
        p["linhas"] = (linhas([m["heroi"]] + m["aliados"]), linhas(m["inimigos"]))
    piores.sort(key=lambda p: (max(p["linhas"]), p["icones_numa_carta"]), reverse=True)
    mais_icones = sorted(piores, key=lambda p: p["icones_numa_carta"], reverse=True)[:5]
    # o pior momento de cada especialização no maior bando (o que a foto reproduz: o necromante e o arqueiro)
    por_spec = {}
    for p in piores:
        if p["bando"] == "caidos e xamã" and p["spec"] not in por_spec:
            por_spec[p["spec"]] = p
    SAIDA.write_text(json.dumps({"lutas_por_combinacao": LUTAS, "nivel": NIVEL, "nivel_inimigo": NIVEL_INIMIGO,
                                 "resumo": resumo, "piores": piores[:12], "mais_icones": mais_icones,
                                 "pior_por_spec": por_spec},
                                ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
