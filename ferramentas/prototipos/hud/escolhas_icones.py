"""As amostras pequenas dos itens nas escolhas de evento (experimento; o jogo não lê esta pasta). Hoje a opção que gasta
um consumível ("Estancar o sangue com uma bandagem", "Deixar remédios na porta") mostra o sprite 16×16 do jogo em 1×
(escolhas.js, meta.gasta e meta.item); a bolsa mostra o desenho aprovado em 32. As amostras, em escolhas-pixel/:

  - 16 px (o lugar de hoje, sem mudar a altura da opção):
      bomba-16: desenhada na grade de 16 por desenhar_bomba_pixel.py (as medidas de 16 ficam aqui até a aprovação),
        com o que cabe: o pote preto, o brilho, o tufo de pano, o pavio enrolado; sem a rede de cordão (ruído em 16);
      pocao-16, bandagem-16: a poção e a bandagem pintadas da família, pelo processo da família
        (familia_ferro.py: a escala do grupo e a redução "paleta"), como os outros tamanhos delas;
  - 24 px (a outra saída, só para comparar): pocao-24 e bandagem-24, que já existem no jogo (os recursos do topo),
    e bomba-24, desenhada na grade de 24.

    python ferramentas/prototipos/hud/escolhas_icones.py     (grava em escolhas-pixel/ e monta a prancha)
"""

import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

import desenhar_bomba_pixel as bomba  # noqa: E402
import familia_ferro as familia  # noqa: E402
from pixel_comum import ICONES, salvar  # noqa: E402

SAIDA = AQUI / "escolhas-pixel"

# A bomba em 16 e em 24, cada uma na própria grade (as medidas de 32 estão em desenhar_bomba_pixel.MEDIDAS)
bomba.MEDIDAS[16] = dict(cx=8.0, K=0.4, by=10.2, a=5.7, b=5.3, exp=2.0, yf=14.4, rn=1.5, yt=2.6, rt=2.4, yc=5.0, rs=2.5,
                         ys=5.9,
                         pavio=[((8, 2), 3), ((9, 1), 4), ((10, 1), 5), ((11, 2), 6)],
                         nos=[((10, 5), 3)],
                         brilho={(0, 0): 8, (1, 0): 7, (0, 1): 6})
bomba.MEDIDAS[24] = dict(cx=12.0, K=0.4, by=14.8, a=8.6, b=8.0, exp=2.0, yf=21.2, rn=2.3, yt=4.4, rt=3.0, yc=7.0,
                         rs=3.6, ys=8.2, anel=-1.6, alca=0.5,
                         pavio=[((11, 4), 3), ((12, 4), 2), ((12, 3), 4), ((13, 2), 5), ((14, 2), 4), ((15, 2), 3),
                                ((15, 3), 5), ((16, 3), 6)],
                         nos=[((14, 7), 4), ((15, 7), 2), ((15, 8), 3)],
                         brilho={(0, 0): 8, (1, 0): 7, (0, 1): 7, (2, -1): 6, (-1, 1): 6})


def familia_em(lado, nomes):
    """Os itens pintados da família em `lado`, pela escala do grupo inteiro e a redução "paleta" (familia_ferro.py)."""
    pecas = {n: Image.open(familia.PECAS / f"{n}.png").convert("RGBA") for n in familia.GRUPO}
    fat = familia.escalas(pecas, lado, familia.FOLGA)
    for n in nomes:
        for dens, suf in ((1, ""), (2, "@2x")):
            familia.no_quadrado(pecas[n], fat[n], lado, dens).save(SAIDA / f"{n}-{lado}{suf}.png")


def main():
    SAIDA.mkdir(exist_ok=True)
    for lado in (16, 24):
        print(f"bomba-{lado}: {salvar(bomba.desenhar(lado), SAIDA, 'bomba')} cores")
    familia_em(16, ["pocao", "bandagem"])
    for n in ("pocao", "bandagem"):  # os de 24 do jogo, copiados para a prancha
        for suf in ("", "@2x"):
            Image.open(ICONES / f"{n}-24{suf}.png").save(SAIDA / f"{n}-24{suf}.png")
    print("escolhas-pixel/:", ", ".join(sorted(p.name for p in SAIDA.glob("*.png") if "@" not in p.name)))


if __name__ == "__main__":
    main()
