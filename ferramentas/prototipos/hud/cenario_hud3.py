"""Cenário só do protótipo (não é teste nem jogo): a campanha num lugar com paisagem, com a missão da febre e dois
contratos de caça aceitos, para fotografar o painel do mundo com mais de um rastreio. Sobe o servidor do jogo como os
cenários de tests/navegador/cenarios.py:

    python ferramentas/prototipos/hud/cenario_hud3.py hud3
"""

import os
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, RAIZ)

from tests.navegador import cenarios as C  # noqa: E402
from rpg import missoes  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402


def hud3(ui):
    g = Jogo(ui, seed=8, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", "guerreiro", "turvo")
    m = missoes.registro(g, "febre_do_turvo")
    m.update(etapa="canal", cenas=["abertura"], pistas=["agua_do_leste"])
    bosque = next(l for l in g.mundo["locais"] if l["chave"] == "bosque_do_moinho")
    g.mundo["atual"], bosque["visitado"] = bosque["id"], True
    outro = next(l for l in g.mundo["locais"] if l["tipo"] != "vila" and l["id"] != bosque["id"])
    g.contratos += [
        {"id": 901, "tipo": "caca", "local": bosque["id"], "familia": "lobo", "total": 4, "feito": 1,
         "ouro": 40, "xp": 60, "desc": f"Eliminar 4 lobos em {bosque['nome']}."},
        {"id": 902, "tipo": "caca", "local": outro["id"], "familia": "javali", "total": 3, "feito": 0,
         "ouro": 35, "xp": 50, "desc": f"Eliminar 3 javalis em {outro['nome']}."},
    ]
    g.periodo, g.clima = int(os.environ.get("PERIODO", "2")), "limpo"
    try:
        g.rodar()
    except FimDeJogo:
        pass


C.CENARIOS["hud3"] = hud3
if __name__ == "__main__":
    C.main()
