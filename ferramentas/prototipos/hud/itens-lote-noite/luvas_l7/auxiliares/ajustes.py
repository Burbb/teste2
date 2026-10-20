"""Os ajustes da L7 sobre o rascunho (grades/rascunho.txt): o resultado é grades/L7.txt, a fonte das camadas.
  1. o halo: o pixel de fora do contorno com a cor da mistura do desenho com o fundo da captura sai; o pixel da beira
     que sobra vira contorno (na referência o par é todo contornado; o borrão da captura apagava o preto em alguns lados);
  2. a malha: como na cota e na M5, o tom do volume (pela luminosidade média da vizinhança de malha na guia) com o
     xadrez de um tom acima e um abaixo
     (a mediana da captura apagava o xadrez das costas da mão; não se tenta reproduzir cada anel);
  3. os ajustes pixel a pixel (AJUSTES), cada um com o porquê.
    python ajustes.py <pasta da L7>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import transpor as T  # noqa: E402

MINIMO = "o dedo mínimo da luva da direita, em couro com o contorno dos lados (a marca d'água '©' do recorte o clareava)"
AJUSTES = [   # (y, x0, trecho, porquê); " " no trecho mantém o pixel
    (6, 27, "###", MINIMO), (7, 26, "e fe#", MINIMO), (8, 26, "d ee#", MINIMO), (9, 26, "d ed#", MINIMO),
    (10, 26, "c#dd#", MINIMO), (11, 27, "cdc#", MINIMO), (12, 29, "#", MINIMO)]


def malha(c):
    """Um pixel da guia é malha (ou ferragem) se for cinza: sem o tom quente do couro e fora do preto do contorno."""
    r, g, b = c
    return not (r - b > 25) and 0.3 * r + 0.59 * g + 0.11 * b >= 40


def tom(l):
    return min(range(2, 8), key=lambda t: abs(0.3 * T.PALETA[str(t)][0] + 0.59 * T.PALETA[str(t)][1] + 0.11 * T.PALETA[str(t)][2] - l))


def ajustar(base):
    guia = np.array(Image.open(base / "previa/guia-32.png").convert("RGBA")).astype(float)
    g = [list(l) for l in (base / "grades/rascunho.txt").read_text(encoding="utf-8").split("\n")[:32]]
    vazio = lambda x, y: not (0 <= x < 32 and 0 <= y < 32) or g[y][x] == "."
    # 1. o halo (duas passadas: o borrão tem até 2 px)
    halo = 0
    for _ in range(2):
        tira = [(x, y) for y in range(32) for x in range(32) if g[y][x] not in ".#"
                and any(vazio(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                and np.sqrt(((guia[y, x, :3] - T.FUNDO) ** 2).sum()) < 80]
        for x, y in tira: g[y][x] = "."
        halo += len(tira)
    # o contorno: na referência o par é todo contornado; o pixel da beira que o borrão deixou cinza vira contorno
    beira = [(x, y) for y in range(32) for x in range(32) if g[y][x] not in ".#"
             and any(vazio(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in beira: g[y][x] = "#"
    # 2. a malha: o volume pela luminosidade, o xadrez dos anéis por cima
    n = 0
    lum = guia[..., :3] @ [0.3, 0.59, 0.11]
    e_malha = [[g[y][x].isdigit() and guia[y, x, 3] >= 128 and malha(guia[y, x, :3]) for x in range(32)] for y in range(32)]
    for y in range(32):
        for x in range(32):
            if g[y][x] in ".#" or not e_malha[y][x]: continue
            # o tom do volume pela média da vizinhança de malha (a captura já traz um xadrez irregular, que um pixel
            # sozinho não dá o volume)
            viz = [lum[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                   if 0 <= x + dx < 32 and 0 <= y + dy < 32 and e_malha[y + dy][x + dx]]
            t = tom(sum(viz) / len(viz))
            g[y][x] = str(min(t + 1, 7) if (x + y) % 2 == 0 else max(t - 1, 2)); n += 1
    for y, x0, trecho, _ in AJUSTES:
        for k, ch in enumerate(trecho):
            if ch != " ": g[y][x0 + k] = ch
    return ["".join(l) for l in g], halo, n, len(beira)


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g, halo, n, beira = ajustar(base)
    (base / "grades/L7.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    print(f"halo: {halo} pixels saíram; beira em contorno: {beira}; malha: {n} pixels; {len(AJUSTES)} ajustes à mão")
    print("\n".join(f"{y:2d} {l}" for y, l in enumerate(g)))
