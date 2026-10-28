"""Candidata do gesto do martelo (18ª; para o Jean avaliar na demonstração: o jogo e a fonte aseprite/forja-h2.aseprite
não mudam). Parte do desenho em código (ferreiro_h2.figura, igual ao quadro do jogo pixel a pixel), com os retoques da
17ª que não mexem no braço (a nuca e o calcanhar da bigorna à frente da barriga, de candidata_ferreiro.py), e grava a
tira em candidata-gesto/ferreiro.png, que a demonstração da forja mostra com "Ferreiro: candidata" no painel de testes.

A leitura de guidão vinha da cadeia ombro → cotovelo → punho → cabo, não da mão:
  - na preparação (sobe2, alto), o braço ia para a frente na altura do ombro (o cotovelo 15 a 16 px à esquerda do ombro,
    na mesma linha), com o antebraço e o cabo em pé: os dois braços de um guidão;
  - a mão pegava o cabo pelo meio: um toco de 5 a 7 px sobrava atrás do punho (no repouso, no golpe, na descida);
  - a descida era quase vertical (a cabeça do martelo caía em x 141 de y 36 a 53), de cima, não de lado.
Agora:
  - a pegada fica na ponta do cabo (a ponta sai 2,5 px atrás do punho, em todas as poses), o cabo como continuação da mão;
  - na preparação, o cotovelo sobe na diagonal até a altura da testa, à frente do rosto, o antebraço dobra para trás e a
    mão passa por cima da cabeça; no alto, o martelo fica armado atrás da cabeça (a cabeça do martelo em x 169,5, acima
    da nuca), sem crescer o quadro: a altura máxima do martelo é a de antes (y 18);
  - na descida, o braço estica para a frente na altura do ombro e o martelo vem em arco pela frente (o rastro do arco
    passa pelos pontos que já existiam), até o mesmo contato na lâmina;
  - no contato (2ª passada, pela avaliação do Jean: a subida ficou certa, o fim não), o braço continua estendido para a
    frente (a mão a 12 px do ombro, à frente do corpo) e o cabo desce em ângulo da mão até a espada; antes, a mão
    terminava colada ao peito com o cotovelo dobrado para trás e o cabo na horizontal, o que não dá para fazer de
    verdade e lia como guidão. Vale para o golpe, a volta, o repouso e o ajuste (o martelo apoiado na lâmina).
Os apoios (as botas, a luva na tenaz, a tenaz na espiga), o corpo, a cabeça, o enquadramento e o ritmo (53 quadros de
100 ms, as mesmas poses na mesma ordem) não mudam.

    python ferramentas/prototipos/hud/forja/h2/candidata_gesto.py
"""
import math
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import candidata_ferreiro as C17  # noqa: E402
import ferreiro_h2 as F  # noqa: E402
from desenhar_h2 import ESTADOS  # noqa: E402

SAIDA = AQUI / "candidata-gesto"
PEGA = 2.5  # quanto a ponta do cabo sai atrás do punho


def com_pegada(punho, cabeca_m):
    """A ponta do cabo, PEGA px atrás do punho, na linha da cabeça do martelo para o punho."""
    (wx, wy), (hx, hy) = punho, cabeca_m
    n = math.hypot(wx - hx, wy - hy)
    return (round(wx + (wx - hx) / n * PEGA, 1), round(wy + (wy - hy) / n * PEGA, 1))


# o braço do martelo de cada pose: o cotovelo, o punho e a cabeça do martelo (a ponta do cabo vem da pegada)
BRACO = {
    # no contato (o golpe, a volta, o repouso e o ajuste com o martelo na lâmina), o braço estendido para a frente e o
    # cabo descendo em ângulo da mão até a espada; antes (1ª passada), a mão ficava colada ao peito (9 px do ombro) com o
    # cotovelo dobrado para trás e o cabo na horizontal: o guidão que o Jean ainda via no fim do golpe
    "repouso": {"cotovelo": (157.5, 48.5), "punho": (151.5, 49.5), "cabeca_m": (141.5, 53.5)},
    "sobe1": {"cotovelo": (158.5, 45.5), "punho": (152, 41), "cabeca_m": (145.5, 30.3)},
    "sobe2": {"cotovelo": (156, 37), "punho": (157, 29.5), "cabeca_m": (162.6, 18.4)},
    "alto": {"cotovelo": (155, 33), "punho": (159.5, 25.5), "cabeca_m": (169.5, 18)},
    "desce": {"cotovelo": (157, 40), "punho": (151, 38.5), "cabeca_m": (141.6, 30.3)},
    "golpe": {"cotovelo": (157, 48.5), "punho": (151, 49.5), "cabeca_m": (141.5, 53.5)},
    "volta": {"cotovelo": (157, 47), "punho": (151, 46.5), "cabeca_m": (141.6, 50)},
    "ajuste": {"cotovelo": (157.5, 48.5), "punho": (151.5, 49.5), "cabeca_m": (141.5, 53.5)},
}
POSES = {k: dict(F.POSES[k], **b, cabo=com_pegada(b["punho"], b["cabeca_m"])) for k, b in BRACO.items()}
# o rastro da descida, pelo arco do alto até a frente (os pontos de antes, mais o começo atrás da cabeça)
RASTRO = [(166, 17), (162, 17), (158, 17), (154, 18), (150, 20), (147, 23), (145, 26)]


def rastro(f):
    for i, (x, y) in enumerate(RASTRO):
        f.p(x, y, "ferro" if i < 4 else "ferroLuz")


def figura(estado):
    """O quadro do ferreiro com o braço novo e os retoques da 17ª que não são do braço (a nuca)."""
    pose = "ajuste" if estado == "ajuste_virada" else estado
    guardadas, rastro_antes = dict(F.POSES), F.rastro
    F.POSES.update(POSES)
    F.rastro = rastro
    try:
        t = F.figura(pose, virada=estado == "ajuste_virada")
    finally:
        F.POSES.clear()
        F.POSES.update(guardadas)
        F.rastro = rastro_antes
    p = POSES[pose]
    sx, sy = p["ombro"]
    cx_, cy_ = p["cabeca"]
    hx, hy = 159 + sx + cx_, 31 + sy + cy_
    for dy, linha in enumerate(C17.NUCA):
        for dx, ch in enumerate(linha):
            x, y = hx + C17.NUCA_ORIGEM[0] + dx, hy + C17.NUCA_ORIGEM[1] + dy
            if ch in C17.PAL_NUCA and t.get(x, y)[3] == 0:
                t.px(x, y, F.COR[C17.PAL_NUCA[ch]])
    return t.imagem()


def tira():
    """A tira de 9 quadros (a ordem de desenhar_h2.ESTADOS), com o calcanhar da bigorna à frente da barriga."""
    bigorna = Image.open(C17.CAMADAS / "bigorna.png").convert("RGBA")
    x0, x1, y0, y1 = C17.CALCANHAR
    saida = Image.new("RGBA", (320 * len(ESTADOS), 96))
    for i, e in enumerate(ESTADOS):
        q = figura(e)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if bigorna.getpixel((x, y))[3]:
                    q.putpixel((x, y), (0, 0, 0, 0))
        saida.paste(q, (320 * i, 0))
    return saida


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    nova = tira()
    nova.save(SAIDA / "ferreiro.png", optimize=True)
    print("candidata:", SAIDA / "ferreiro.png")
