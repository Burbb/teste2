"""Monta a folha compacta das três propostas do livro da capela a partir de ../capturas/ (fotografar.mjs):
em cima, A e B; no meio, a C nas duas entradas, tudo recortado da janela de 1920×945 em tamanho real (a leitura se
julga assim); embaixo, as quatro telas inteiras de 1280×720 (o livro de hoje, A, B e C) reduzidas a um terço, só
para o contexto da sacristia. Grava ../folha-propostas.png.

    python ferramentas/prototipos/hud/livro-capela/auxiliares/folha.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
FUNDO, TITULO, NOTA = (22, 18, 14), (220, 200, 150), (150, 140, 120)


def fonte(tam):
    for nome in ("georgia.ttf", "DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(nome, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def recorte(nome, quadros, folga=10):
    x, y, w, h = quadros[nome]
    return Image.open(CAP / f"{nome}.png").convert("RGB").crop((x - folga, y - folga, x + w + folga, y + h + folga))


def main():
    quadros = {k: v["quadro"] for k, v in json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"].items()}
    linhas = [
        [("A · registro pautado (a 2ª entrada em outra tinta, depois de um traço)", recorte("1920-a", quadros)),
         ("B · registro que vira confissão (a 2ª na mesma mão, mais depressa)", recorte("1920-b", quadros))],
        [("C · leitura próxima, entrada 1 de 2", recorte("1920-c", quadros)),
         ("C · entrada 2 de 2 (mais folhas viradas à esquerda)", recorte("1920-c-2", quadros))],
    ]
    pequenas = [(r, Image.open(CAP / f"1280-{v}.png").convert("RGB")) for v, r in
                (("atual", "hoje"), ("a", "A"), ("b", "B"), ("c", "C"))]
    pequenas = [(r, im.resize((im.width // 3, im.height // 3), Image.LANCZOS)) for r, im in pequenas]
    M, ROT = 16, 26
    largura = max(sum(im.width for _, im in ln) + M * (len(ln) + 1) for ln in linhas)
    largura = max(largura, sum(im.width for _, im in pequenas) + M * 5)
    altura = 44 + sum(max(im.height for _, im in ln) + ROT + M for ln in linhas) + ROT + pequenas[0][1].height + M
    folha = Image.new("RGB", (largura, altura), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 12), "O livro da capela: as três propostas no jogo, na sacristia, com os mesmos dados (protótipo; o jogo "
                    "não mudou)", fill=TITULO, font=fonte(17))
    y = 44
    for ln in linhas:
        x = M
        for rotulo, im in ln:
            d.text((x, y), rotulo + " · 1920×945, tamanho real", fill=NOTA, font=fonte(14))
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(im.height for _, im in ln) + ROT + M
    x = M
    for rotulo, im in pequenas:
        d.text((x, y), f"1280×720 · {rotulo} (a 1/3)", fill=NOTA, font=fonte(14))
        folha.paste(im, (x, y + ROT))
        x += im.width + M
    folha.save(AQUI.parent / "folha-propostas.png")
    print(folha.size)


if __name__ == "__main__":
    main()
