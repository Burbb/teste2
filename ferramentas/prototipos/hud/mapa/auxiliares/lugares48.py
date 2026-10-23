"""O 48 dos ícones de lugar, só para a comparação do mapa grande (1E.4, 23/10/2026; nada no jogo): pelo mesmo processo
que fez o 32 e o 40 do jogo (preparar_hud4p.py: o recorte da folha de referência, a escala do grupo pela área visível e
a redução "paleta"), sem retoque. Antes, confere que o processo refaz o 32 e o 40 do jogo idênticos. Não é desenho
nativo: é mais uma redução, por fator não inteiro, da mesma referência.
    python lugares48.py        # grava ../proposta/lugar-<nome>-48.png e o @2x
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
HUD = AQUI.parents[1]
sys.path.insert(0, str(HUD))
import preparar_hud4p as p4  # noqa: E402
from preparar_hud4c import escalas  # noqa: E402

NOMES = p4.GRUPOS["lugares"][0]
pecas = {n: Image.open(HUD / f"assets4p/pecas/{n}.png").convert("RGBA") for n in NOMES}
for lado in (32, 40):
    fat = escalas(pecas, lado, 0)
    for n in NOMES:
        jogo = Image.open(HUD.parents[2] / f"rpg/web/static/hud/icones/{n}-{lado}.png").convert("RGBA")
        assert p4.no_quadrado(pecas[n], fat[n], lado, "paleta").tobytes() == jogo.tobytes(), (n, lado)
fat = escalas(pecas, 48, 0)
for n in NOMES:
    nome = n.replace("lugar-", "")
    nome = {"caverna": "covil"}.get(nome, nome)  # o protótipo pede pelo desenho do mapa (MapaPx.sprite)
    for dens, suf in ((1, ""), (2, "@2x")):
        p4.no_quadrado(pecas[n], fat[n], 48, "paleta", dens).save(AQUI.parent / f"proposta/lugar-{nome}-48{suf}.png")
print("o processo refaz o 32 e o 40 do jogo idênticos; o 48 gravado em proposta/")
