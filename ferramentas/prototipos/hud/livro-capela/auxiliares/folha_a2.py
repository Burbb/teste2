"""Monta a comparação A × A refinada a partir de ../capturas/ (fotografar.mjs com VERSOES=a,a2): em cima, os dois
livros na janela de 1920×945 em tamanho real; no meio, o mesmo trecho (o alto da página da esquerda, as primeiras
linhas e a beira) ampliado 2× para ver o papel e a letra na pauta (a ampliação só acha o pixel; julga-se pelo de
cima); embaixo, as duas telas de 1280×720 a um terço. Grava ../folha-a2.png.

    python ferramentas/prototipos/hud/livro-capela/auxiliares/folha_a2.py
"""
import json
import pathlib

from PIL import Image, ImageDraw

from folha import CAP, FUNDO, NOTA, TITULO, fonte, recorte

AQUI = pathlib.Path(__file__).resolve().parent


def main():
    quadros = {k: v["quadro"] for k, v in json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"].items()}
    grandes = [("A (como estava)", recorte("1920-a", quadros)), ("A refinada", recorte("1920-a2", quadros))]

    def detalhe(nome):  # o alto da página da esquerda: a beira de cima e de fora, três linhas e a margem
        x, y, _, _ = quadros[nome]
        im = Image.open(CAP / f"{nome}.png").convert("RGB").crop((x + 10, y + 50, x + 330, y + 170))
        return im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    detalhes = [("A · detalhe 2×", detalhe("1920-a")), ("A refinada · detalhe 2×", detalhe("1920-a2"))]
    pequenas = [(r, Image.open(CAP / f"1280-{v}.png").convert("RGB")) for v, r in (("a", "A"), ("a2", "A refinada"))]
    pequenas = [(r, im.resize((im.width // 3, im.height // 3), Image.LANCZOS)) for r, im in pequenas]
    M, ROT = 16, 26
    linhas = [grandes, detalhes, pequenas]
    largura = max(sum(im.width for _, im in ln) + M * (len(ln) + 1) for ln in linhas)
    altura = 44 + sum(max(im.height for _, im in ln) + ROT + M for ln in linhas)
    folha = Image.new("RGB", (largura, altura), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 12), "O livro da capela: A × A refinada (o papel calmo no centro, a letra apoiada na pauta), com o texto "
                    "real no jogo; protótipo", fill=TITULO, font=fonte(17))
    y = 44
    for i, ln in enumerate(linhas):
        x = M
        for rotulo, im in ln:
            sufixo = (" · 1920×945, tamanho real", "", " · 1280×720 (a 1/3)")[i]
            d.text((x, y), rotulo + sufixo, fill=NOTA, font=fonte(14))
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(im.height for _, im in ln) + ROT + M
    folha.save(AQUI.parent / "folha-a2.png")
    print(folha.size)


if __name__ == "__main__":
    main()
