"""A B4: a B3 com o ombro e a manga do braço de cá do de verde suavizados. Todo o resto continua o da B3: a cabeça,
o punho junto da barba, o braço da mesa, as pernas, os móveis, a escala, a posição e o de ocre inteiro. Só semeia o
retoque: `fonte.py --criar` copia a fonte da B3 e troca, na camada verde, só os pixels em que este desenho difere do da
B3.

O problema da B3: a faixa clara contínua no alto do ombro, na aresta da manga e no punho dobrado lia como uma tira ou
uma ombreira, e a coluna escura entre o braço e o peito fazia o braço parecer encaixado no tronco. A correção:
- o ombro sem a calota de luz forte: a luz cai em manchas curtas sobre o tecido (no alto do ombro e no meio da manga,
  onde o braço é mais redondo), quebradas por tons médios;
- o ombro continua no peito e nas costas pelo mesmo tom médio, sem a linha escura no alto;
- entre o braço e o peito, uma sombra de um pixel só onde o braço afasta do corpo (do sovaco ao cotovelo), no tom de
  sombra, não no mais escuro; o peito sem a coluna dupla de sombra;
- o punho dobrado no cotovelo, uma dobra baixa no mesmo tom da manga.
A leitura da B3 fica: o braço desce à frente das costas (a faixa escura das costas atrás dele continua), dobra no
cotovelo e o antebraço vai à mão na coxa.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(AQUI)))

from prova.b2 import desenho as B2  # noqa: E402
from prova.b2.desenho import partes  # noqa: E402
from prova.b3 import desenho as B3  # noqa: E402

W, H, S = B3.W, B3.H, B3.S


def _verde():
    p = B3.verde_partes()
    tronco = {y: [tr for tr in trs if tr != (23, "nn")] for y, trs in p["tronco"].items()}
    for y in range(31, 38):                                         # a sombra do braço no peito: um pixel, no tom médio
        tronco[y].append((23, "n"))
    braco_ca = {24: (19, "nNZZN"), 25: (17, "nNNZZZNN"), 26: (16, "zNNNZZNNN"), 27: (15, "zNNNNZNNN"),
                28: (15, "zNNNNNNN"), 29: (15, "zNNNNZNN"), 30: (15, "zNNNNZZn"), 31: (15, "zNNNNZNn"),
                32: (15, "zNNNNNNn"), 33: (15, "zNNNNNNn"), 34: (15, "zNNNNNNn"), 35: (15, "zNNNNNNn"),
                36: (15, "znNZZNNn"), 37: (15, "znnNNNnn"), 38: (16, "zznnn")}
    ordem = dict(p)
    ordem["tronco"], ordem["braco_ca"] = tronco, braco_ca
    return partes(*ordem.values())


VERDE = _verde()


def camadas():
    """A camada que a B4 muda, já com a luz da sala: {nome: (B3, B4)}."""
    return {"verde": (B3.camada(B3.VERDE, B2.PAL_VERDE), B3.camada(VERDE, B2.PAL_VERDE))}

