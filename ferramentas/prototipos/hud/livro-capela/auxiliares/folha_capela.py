"""Monta a comparação base limpa × livro da capela deteriorado a partir de ../capturas/ (fotografar.mjs com
VERSOES=a2,capela): em cima, os dois na janela de 1920×945 em tamanho real; no meio, as duas telas de 1280×720 a
metade; embaixo, os rasgos ampliados 3× (só para conferir papel, pauta e tinta juntos; julga-se pelo tamanho real):
o rasgo da direita que tira o alto de "do", a mordida da esquerda no pé do "n" de "nem" e o canto arrancado (a folha
de baixo, o couro por dentro e a capa que falta). Grava ../folha-capela.png.

    python ferramentas/prototipos/hud/livro-capela/auxiliares/folha_capela.py
"""
import json
import pathlib

from PIL import Image, ImageDraw

from folha import CAP, FUNDO, NOTA, TITULO, fonte, recorte

AQUI = pathlib.Path(__file__).resolve().parent


def main():
    quadros = {k: v["quadro"] for k, v in json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"].items()}
    grandes = [("Base limpa (a A refinada, aprovada) · 1920×945, tamanho real", recorte("1920-a2", quadros)),
               ("Livro da capela, deteriorado (candidata) · 1920×945, tamanho real", recorte("1920-capela", quadros))]
    medias = [(f"{r} · 1280×720 (a 1/2)", Image.open(CAP / f"1280-{v}.png").convert("RGB")) for v, r in
              (("a2", "Base limpa"), ("capela", "Livro da capela"))]
    medias = [(r, im.resize((im.width // 2, im.height // 2), Image.LANCZOS)) for r, im in medias]
    x0, y0, _, _ = quadros["1920-capela"]
    livro = (x0, y0 + 34)  # o canto do livro dentro do quadro (a etiqueta em cima)
    tela = Image.open(CAP / "1920-capela.png").convert("RGB")

    def det(rotulo, art):  # um trecho do livro, nas coordenadas do desenho (escala 3), ampliado 3×
        ax0, ay0, ax1, ay1 = art
        im = tela.crop((livro[0] + ax0 * 3, livro[1] + ay0 * 3, livro[0] + ax1 * 3, livro[1] + ay1 * 3))
        return rotulo, im.resize((im.width * 3, im.height * 3), Image.NEAREST)
    detalhes = [det("o rasgo da direita: o alto de \"do\" (3×)", (232, 36, 282, 66)),
                det("a mordida: o pé do \"n\" de \"nem\" (3×)", (2, 66, 52, 100)),
                det("o canto arrancado: a folha de baixo, o couro, sem capa (3×)", (0, 112, 62, 170))]
    M, ROT = 16, 26
    linhas = [grandes, medias, detalhes]
    largura = max(sum(im.width for _, im in ln) + M * (len(ln) + 1) for ln in linhas)
    altura = 44 + sum(max(im.height for _, im in ln) + ROT + M for ln in linhas)
    folha = Image.new("RGB", (largura, altura), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 12), "O livro da capela: a base limpa × o livro deteriorado (candidata), com o texto real no jogo; "
                    "protótipo", fill=TITULO, font=fonte(17))
    y = 44
    for ln in linhas:
        x = M
        for rotulo, im in ln:
            d.text((x, y), rotulo, fill=NOTA, font=fonte(14))
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(im.height for _, im in ln) + ROT + M
    folha.save(AQUI.parent / "folha-capela.png")
    print(folha.size)


if __name__ == "__main__":
    main()
