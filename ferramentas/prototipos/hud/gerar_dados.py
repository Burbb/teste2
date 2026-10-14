"""Gera dados.js do protótipo da ficha do herói com o motor de verdade: cada combinação dos controles de
demonstração (nível, equipamento, ferimentos, fome, bolsa) sai de um herói montado pelo jogo e lido por
rpg.web.estado.heroi, o mesmo dicionário que a ficha atual desenha. Nada aqui é inventado na mão.

    python ferramentas/prototipos/hud/gerar_dados.py
"""

import json
import os
import random
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)

from rpg import dev, sobrevivencia  # noqa: E402
from rpg.itens import CONSUMIVEIS, gerar_equip, rolar_raridade  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.ui import BotUI  # noqa: E402
from rpg.web.estado import heroi  # noqa: E402

NIVEIS = {"1": (1, None), "6": (6, "paladino"), "14": (14, "paladino")}
REPUTACAO = {"1": 0, "6": 12, "14": 34}
EQUIP = ("completo", "parcial", "vazio")
BOLSAS = {"comum": {"pocao_vida": 2, "bandagem": 2, "tonico": 1},
          "cheia": {"pocao_vida": 12, "bandagem": 9, "tonico": 3, "antidoto": 4, "bau": 2},
          "vazia": {}}
CAMPOS = ("nome", "classe", "classe_nome", "titulo", "nivel", "xp", "xp_proximo", "hp", "max_hp", "rec", "max_rec",
          "recurso", "atributos", "atributos_info", "atributos_penal", "reputacao", "reputacao_info", "ouro",
          "provisoes", "fome", "condicoes", "bolsa", "equip", "ferimentos", "pontos_talento", "spec")


def montar(nivel, equip, feridas, fome, bolsa):
    g = Jogo(BotUI(random.Random(1)), seed=5, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Jean", "guerreiro")
    n, spec = NIVEIS[nivel]
    dev.subir_ate(g, n, spec=spec)
    j = g.j
    rng = random.Random(40 + n)
    for k, espaco in enumerate(j.equip):
        if equip == "vazio" or (equip == "parcial" and espaco not in ("arma", "armadura", "secundaria", "anel1")):
            j.equip[espaco] = None
            continue
        slot = "anel" if espaco.startswith("anel") else espaco
        j.equip[espaco] = gerar_equip(rng, j.classe, max(1, n - 1), slot, raridade=rolar_raridade(rng))
    j.reputacao = REPUTACAO[nivel]
    j.xp = j.xp_proximo() * 2 // 3
    if feridas:
        for fid in ("corte", "costelas"):
            sobrevivencia.ferir(g, fid)
    j.fome = 2 if fome else 0
    j.consumiveis = {**{k: 0 for k in j.consumiveis}, **BOLSAS[bolsa], "tocha": 3}
    j.recalcular()
    j.hp = max(1, int(j.max_hp * 0.72))
    j.rec = int(j.max_rec * 0.6)
    h = heroi(g)
    return {k: h[k] for k in CAMPOS}


def main():
    dados = {}
    for nivel in NIVEIS:
        for equip in EQUIP:
            for feridas in (0, 1):
                for fome in (0, 1):
                    for bolsa in BOLSAS:
                        dados[f"{nivel}|{equip}|{feridas}|{fome}|{bolsa}"] = montar(nivel, equip, feridas, fome, bolsa)
    destino = os.path.join(os.path.dirname(__file__), "dados.js")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("// Gerado por gerar_dados.py a partir do motor (rpg.web.estado.heroi). Não editar à mão.\n")
        f.write("window.FICHAS = " + json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + ";\n")
        icones = {k: c["icone"] for k, c in CONSUMIVEIS.items()}  # o desenho de cada consumível (como estado["itens"])
        f.write("window.ICONES_BOLSA = " + json.dumps(icones, ensure_ascii=False) + ";\n")
    print(destino, len(dados), "combinações")


if __name__ == "__main__":
    main()
