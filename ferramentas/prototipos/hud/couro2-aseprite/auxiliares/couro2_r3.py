"""Rodada 3 do capuz de tecido (o Capuz do Mago): só a passagem do capuz para a pala sobre os ombros. As listas de
pixels por camada que o pintar.lua (ferramentas/arte/aseprite/) escreve no Aseprite pelo MCP. O Python só calcula.

    python ferramentas/prototipos/hud/couro2-aseprite/auxiliares/couro2_r3.py <pasta>

Na rodada 2, a capa abria num degrau (a linha 21 era uma faixa escura de lado a lado), as dobras eram faixas verticais
paralelas e a barra ondulava em pontas: a parte de baixo lia como uma cortininha separada, pendurada no capuz. Aqui:
- a silhueta desce do pescoço para os lados em diagonal contínua, sem degrau (o pano assenta nos ombros);
- sem a faixa horizontal: só uma sombra curta sob o queixo da abertura, que some para os lados;
- as dobras saem do pescoço e abrem para fora, na direção em que o pano se espalha pelos ombros (raios a partir de um
  ponto acima do pescoço), duas de cada lado, em poucos planos: o ombro esquerdo aceso, a frente média, o direito na
  sombra, e o alto de cada ombro um tom acima (o pano vira para cima ali);
- a barra é uma curva lisa (mais alta na frente, mais baixa nos lados), sem ondas nem pontas.
A cabeça (linhas 1 a 18), a abertura, a borda, o interior e a paleta são os da rodada 2. O 32 é a fonte; o 64 é o 32
ampliado 2×.
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[1] / "couro-aseprite" / "auxiliares"))
from couro2_r1 import ABERTURA, N, faixas  # noqa: E402
from couro2_r2 import CABECA_T, FORRO_TECIDO, TECIDO, _abertura_e_borda  # noqa: E402
from couro_r2 import Desenho  # noqa: E402

# a cabeça da rodada 2 até a linha 18; daí, o pano abre em diagonal até os ombros (um pixel por linha de cada lado)
CABECA = {y: v for y, v in CABECA_T.items() if y <= 18}
PALA = {19: (6, 25), 20: (5, 26), 21: (4, 27), 22: (3, 28), 23: (3, 28), 24: (3, 28), 25: (3, 28), 26: (3, 28),
        27: (3, 28), 28: (3, 28)}
CX, CY = 15.5, 13.0                                                   # de onde as dobras abrem (acima do pescoço)


def barra(x):
    """A barra: uma curva lisa, a frente mais alta (26) e os lados mais baixos (28)."""
    return 26 + round(((abs(x - CX) / 12.5) ** 1.6) * 2)


def raio(x, y):
    """A direção do pano a partir do pescoço: 0 no meio, negativa à esquerda, positiva à direita."""
    return (x - CX) / (y - CY)


# as dobras: (raio do vale, lado da crista); o vale escuro com a crista acesa do lado da luz (à esquerda dele)
DOBRAS = (-0.5, 0.75)


def capuz_tecido():
    d = Desenho(N)
    dentro = {(x, y) for y, (a, b) in ABERTURA.items() for x in range(a, b + 1)}

    def tom_pala(x, y):
        if y > barra(x) or (x, y) in dentro: return None
        r = raio(x, y)
        # os planos: o ombro esquerdo de frente para a luz, a frente, o ombro direito virando para a sombra
        t = 4 if r < -0.75 else 3 if r < 0.15 else 2 if r < 0.7 else 1
        # a sombra curta do queixo: logo abaixo da abertura, no meio, some para os lados
        if 19 <= y <= 20 and abs(x - CX) < 4 - (y - 19) * 1.5: t = min(t, 2)   # (segue a curva da abertura)
        # o alto dos ombros, onde o pano vira para cima (a beira da diagonal da silhueta), um tom acima
        a, b = (PALA | CABECA)[y]
        if 20 <= y <= 23 and x - a <= 1 and r < -1.3: t += 1
        # as dobras: o vale um tom abaixo; a crista ao lado, do lado da luz, um tom acima
        for v in DOBRAS:
            dv = r - v
            if y >= 21 and -0.09 <= dv < 0.09: t -= 1
            elif y >= 21 and -0.26 <= dv < -0.09: t += 1
        if y == barra(x) and x >= 17: t -= 1                             # a beira de baixo vira, só do lado da sombra
        return t
    def tom_cabeca(x, y):                                               # a da rodada 2
        if (x, y) in dentro: return None
        t = 4 if x < 12 else 3 if x < 20 else 2
        if x >= 23: t = 1
        if y <= 8 and x < 16: t += 1
        if y >= 16: return tom_pala(x, y)                               # os lados do capuz já descem para os ombros
        return t
    faixas(d, CABECA, "capuz", TECIDO, tom_cabeca)
    faixas(d, PALA, "capa", TECIDO, tom_pala)
    _abertura_e_borda(d, dentro, TECIDO, (6, 5, 3), TECIDO, FORRO_TECIDO)
    d.contornar()
    return d


ORDEM = ["capa", "capuz", "interior", "borda", "contorno"]


def gravar(pasta):
    cam = capuz_tecido().camadas()
    pasta.mkdir(parents=True, exist_ok=True)
    previa = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for c in ORDEM:
        px = cam.get(c, {})
        texto = ";".join(f"{x},{y},{k}" for (x, y), k in sorted(px.items()))
        (pasta / f"{c}.txt").write_text(texto)
        (pasta / f"{c}.lua").write_text(f'return "{texto}"\n')
        for (x, y), k in px.items():
            previa.putpixel((x, y), tuple(int(k[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    previa.save(pasta / "previa.png")
    previa.resize((2 * N, 2 * N), Image.NEAREST).save(pasta / "previa-64.png")
    (pasta / "camadas.txt").write_text(",".join(ORDEM))
    return previa.getbbox(), sum(len(v) for v in cam.values()), len({k for v in cam.values() for k in v.values()})


if __name__ == "__main__":
    print("capuz_tecido", *gravar(pathlib.Path(sys.argv[1]) / "capuz_tecido-32"))
