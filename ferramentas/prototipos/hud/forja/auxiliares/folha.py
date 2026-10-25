"""Monta a folha da forja a partir de ../capturas/ (fotografar.mjs) e da bancada a 1× (bancada.html): hoje × A × B no
jogo, a 1920×945 e a 1280×720 (reduzidas à metade); a arte de A e B em tamanho real, recortada do jogo a 1920; e, só
para diagnóstico, o ferreiro de cada uma ampliado 4× a partir do quadro de 320×72. Grava ../folha-forja.png.

    python ferramentas/prototipos/hud/forja/auxiliares/folha.py <pasta com banc-a-1x.png e banc-b-1x.png>
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def main():
    banc = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else CAP
    metade = lambda n: (lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS))(Image.open(CAP / f"{n}.png").convert("RGB"))
    def arte(n):  # o quadro da arte a 1920, em tamanho real (a vista: abaixo do topo da HUD, até a barra da forja)
        return Image.open(CAP / f"{n}.png").convert("RGB").crop((408, 138, 1472, 372))
    def ampliar(n, caixa):
        im = Image.open(banc / f"banc-{n}-1x.png").convert("RGB").crop(caixa)
        return im.resize((im.width * 4, im.height * 4), Image.NEAREST)
    linhas = [
        ("1920×945 · a forja no jogo: hoje × A (a bancada de trabalho) × B (o interior da oficina)",
         [(metade("1920-atual-forja"), "hoje"), (metade("1920-a-forja"), "A"), (metade("1920-b-forja"), "B")]),
        ("1280×720 · hoje × A × B (o balcão numa linha e os cartões lado a lado, com o ambiente)",
         [(metade("1280-atual-forja"), "hoje"), (metade("1280-a-forja"), "A"), (metade("1280-b-forja"), "B")]),
        ("A · a arte em tamanho real (1920), os nomes dos pontos à vista", [(arte("1920-a-forja"), "A")]),
        ("B · a arte em tamanho real (1920)", [(arte("1920-b-forja"), "B")]),
        ("diagnóstico · o ferreiro e a bigorna ampliados 4× do quadro de 320×72 (não é o tamanho de uso)",
         [(ampliar("a", (66, 0, 176, 64)), "A"), (ampliar("b", (104, 22, 172, 66)), "B")]),
    ]
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in linhas)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in linhas)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "A forja do Vau: duas direções no jogo (protótipo), com a campanha de teste e os mesmos serviços",
           fill=(220, 200, 150), font=fonte(16))
    y = 40
    for rot, ims in linhas:
        d.text((M, y), rot, fill=(220, 200, 150), font=fonte(14))
        x = M
        for im, r in ims:
            d.text((x, y + ROT), r, fill=(150, 140, 120), font=fonte(13))
            folha.paste(im, (x, y + 2 * ROT))
            x += im.width + M
        y += max(im.height for im, _ in ims) + 2 * ROT + M
    folha.save(AQUI.parent / "folha-forja.png", optimize=True)
    print(folha.size)


if __name__ == "__main__":
    main()
