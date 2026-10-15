"""Os tamanhos de uso da família de ferro da HUD (os itens pintados: o equipamento e os itens da bolsa), a partir das
peças aprovadas, que ficam intactas em familia-ferro/ (recortadas das folhas da HUD 4 pixel, com o alfa limpo, por
ferramentas/prototipos/hud/preparar_hud4p.py). Só reduz: nada é redesenhado. É o mesmo processo que fez os arquivos
de 32, 48 e 64 px que o jogo usa desde a 1.89.0 (a escala do grupo inteiro pela área visível, a redução "paleta" com
a borda dura), aqui fora do protótipo, com o 40 px do Inventário (1.95.0) para o equipamento.

    python ferramentas/arte/familia_ferro.py              (grava os de 40 px em rpg/web/static/hud/icones/)
    python ferramentas/arte/familia_ferro.py --conferir   (refaz todos os tamanhos e compara com os do jogo, sem gravar)
    python ferramentas/arte/familia_ferro.py --todos      (grava todos os tamanhos, se uma peça mudar)

O escudo é do grupo (entra na conta da escala, como sempre), mas o arquivo dele é desenhado por regras
(desenhar_escudo_pixel.py) e não sai daqui. Precisa do Pillow e do numpy."""

import pathlib
import sys

import numpy as np
from PIL import Image

from pixel_comum import ICONES

PECAS = pathlib.Path(__file__).resolve().parent / "familia-ferro"
# Os itens da bolsa e os do equipamento dividem os mesmos nichos: um grupo só, com a mesma escala visual (a tocha
# também é item da bolsa). A ordem é a das folhas e não importa para a conta.
GRUPO = ["elmo", "cota", "manopla", "perneiras", "botas-ferro", "maca", "espada", "escudo", "amuleto", "anel", "aljava",
         "bandagem", "pocao", "tonico", "antidoto", "bau", "tocha"]
FOLGA = 1  # pixels livres em volta do maior desenho, em cada tamanho
EQUIPAMENTO = ["elmo", "cota", "manopla", "perneiras", "botas-ferro", "maca", "espada", "amuleto", "anel", "aljava"]
LADOS = {n: (32, 48, 64) for n in GRUPO}  # os de sempre: a bolsa, a mochila, o mercado, o voo, o cartão do saque
for n in EQUIPAMENTO:
    LADOS[n] = (32, 40, 48, 64)           # o 40: o corpo e a mochila do Inventário
DESENHADOS = {"escudo"}                   # os que saem de um desenho por regras, não daqui


def area_visivel(img):
    return int((np.array(img)[:, :, 3] > 128).sum())


def escalas(pecas, lado, folga):
    """O fator de cada peça para o quadrado `lado`: a mesma área visível para todas, sem nenhuma sair do quadrado. O
    alvo é a mediana do que cada uma alcança cabendo no quadrado: as compridas (que batem na borda antes) ficam um pouco
    abaixo, as compactas descem até ela."""
    util = lado - 2 * folga
    cabe = {n: util / max(p.size) for n, p in pecas.items()}
    lado_visivel = {n: (area_visivel(p) ** 0.5) * cabe[n] for n, p in pecas.items()}
    alvo = float(np.percentile(list(lado_visivel.values()), 50))
    return {n: min(cabe[n], alvo / area_visivel(p) ** 0.5) for n, p in pecas.items()}


def blocos(n_origem, n_destino):
    """As bordas (inteiras) de cada pixel de destino na origem."""
    b = np.linspace(0, n_origem, n_destino + 1)
    return np.floor(b[:-1]).astype(int), np.maximum(np.ceil(b[1:]).astype(int), np.floor(b[:-1]).astype(int) + 1)


def reduzir(img, w, h):
    """A redução "paleta": o alfa duro (cada pixel é desenho ou fundo, pela cobertura de metade) e, na cor, a média da
    área trocada pela cor de verdade mais próxima dentro dela (só cores que o desenho tem, como numa pixel art reduzida
    à mão)."""
    a = np.array(img.convert("RGBA")).astype(np.float64)
    W, H = img.size
    x0, x1 = blocos(W, w)
    y0, y1 = blocos(H, h)
    saida = np.zeros((h, w, 4), np.uint8)
    for j in range(h):
        for i in range(w):
            bloco = a[y0[j]:y1[j], x0[i]:x1[i]].reshape(-1, 4)
            alfa = bloco[:, 3] / 255
            if alfa.mean() < 0.5:
                continue
            cheio = bloco[alfa > 0.5]
            media = (bloco[:, :3] * alfa[:, None]).sum(0) / alfa.sum()
            saida[j, i, :3] = np.clip(np.round(cheio[np.argmin(((cheio[:, :3] - media) ** 2).sum(1)), :3]), 0, 255)
            saida[j, i, 3] = 255
    return Image.fromarray(saida, "RGBA")


def no_quadrado(peca, fator, lado, densidade=1):
    """A peça reduzida, centrada num quadrado transparente de `lado` (vezes a densidade: 2 para o @2x, que é desenhado
    em dobro a partir da peça, não a duplicação do 1x, como os outros da família)."""
    lado_px = lado * densidade
    w = max(1, round(peca.width * fator * densidade))
    h = max(1, round(peca.height * fator * densidade))
    q = Image.new("RGBA", (lado_px, lado_px), (0, 0, 0, 0))
    q.alpha_composite(reduzir(peca, w, h), ((lado_px - w) // 2, (lado_px - h) // 2))
    return q


def arquivos(pecas, so_lado=None):
    """{nome do arquivo: imagem} de todos os tamanhos de uso (ou só de `so_lado`)."""
    saida = {}
    for lado in sorted({x for v in LADOS.values() for x in v}):
        if so_lado and lado != so_lado:
            continue
        fat = escalas(pecas, lado, FOLGA)  # a escala do grupo inteiro, como sempre
        for n in GRUPO:
            if n in DESENHADOS or lado not in LADOS[n]:
                continue
            for dens, suf in ((1, ""), (2, "@2x")):
                saida[f"{n}-{lado}{suf}.png"] = no_quadrado(pecas[n], fat[n], lado, dens)
    return saida


def main(argv):
    pecas = {n: Image.open(PECAS / f"{n}.png").convert("RGBA") for n in GRUPO}
    if "--conferir" in argv:
        dif = 0
        for nome, img in arquivos(pecas).items():
            atual = ICONES / nome
            if not atual.exists():
                print(f"{nome}: falta no jogo")
                continue
            a, b = np.asarray(img), np.asarray(Image.open(atual).convert("RGBA"))
            n = int((a != b).any(-1).sum()) if a.shape == b.shape else -1
            dif += n != 0
            print(f"{nome}: {'igual' if n == 0 else f'{n} pixels diferentes' if n > 0 else 'outro tamanho'}")
        print("tudo igual" if not dif else f"{dif} arquivos diferentes")
        return
    for nome, img in arquivos(pecas, None if "--todos" in argv else 40).items():
        img.save(ICONES / nome)
        print(nome)


if __name__ == "__main__":
    main(sys.argv)
