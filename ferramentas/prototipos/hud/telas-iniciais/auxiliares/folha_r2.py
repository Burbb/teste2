"""Monta a folha da criação em etapas (R2) a partir de ../capturas/ (fotografar.mjs com VERSOES=r e criacao_r2.mjs):
R × R2 com os mesmos dados (Ana, Arqueiro, Resgate), a classe e o modo, nas duas janelas; depois os estados da R2 (o
nome, a classe sem escolha, o mouse, o foco do teclado, o Hardcore sem tutorial, o nome longo) e a campanha começando.
As páginas a 1920 reduzidas à metade e as de 1280 a três quartos (a mesma largura). Grava ../folha-criacao-r2.png.

    python ferramentas/prototipos/hud/telas-iniciais/auxiliares/folha_r2.py
"""
import pathlib

from PIL import Image, ImageDraw

from folha import fonte

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
LINHAS = [
    ("1920×945 · a classe (Ana escolhendo o Arqueiro): R × R2", [("1920-r-5-classe", "R"), ("1920-r2-2-classe-arqueiro", "R2")]),
    ("1920×945 · o modo: R × R2", [("1920-r-6-modo", "R"), ("1920-r2-3-modo", "R2")]),
    ("1280×720 · a classe: R × R2", [("1280-r-5-classe", "R"), ("1280-r2-2-classe-arqueiro", "R2")]),
    ("1280×720 · o modo: R × R2", [("1280-r-6-modo", "R"), ("1280-r2-3-modo", "R2")]),
    ("R2 · o nome e a classe ainda sem escolha (o Avançar desligado)", [("1920-r2-1-nome", "1920 · nome"), ("1920-r2-2-classe-sem-escolha", "1920 · classe sem escolha")]),
    ("R2 · a passagem do mouse (o Guerreiro) e o foco do teclado (o Arqueiro escolhido pela seta)",
     [("1920-r2-2-classe-mouse", "1920 · mouse"), ("1920-r2-2-classe-foco-teclado", "1920 · foco do teclado")]),
    ("R2 · Hardcore com o tutorial desligado; o nome longo com acento (40 letras) no resumo",
     [("1920-r2-3-modo-hardcore-sem-tutorial", "1920 · Hardcore, sem tutorial"), ("1280-r2-5-modo-nome-longo", "1280 · nome longo, Mago, Hardcore")]),
    ("R2 · Começar campanha: a abertura no Vau", [("1920-r2-4-campanha", "1920 · Ana, Arqueiro"), ("1280-r2-6-campanha-guerreiro", "1280 · Aventureiro, Guerreiro")]),
]


def reduzir(im):
    f = 0.5 if im.width > 1600 else 0.75
    return im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)


def main():
    blocos = [(rot, [(reduzir(Image.open(CAP / f"{n}.png").convert("RGB")), r) for n, r in ims]) for rot, ims in LINHAS]
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in blocos)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in blocos)
    folha = Image.new("RGB", (largura, altura), (22, 18, 14))
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "A criação do personagem: a R (cartões no painel genérico) × a R2 (a criação em etapas, a candidata), os mesmos dados",
           fill=(220, 200, 150), font=fonte(16))
    y = 40
    for rot, ims in blocos:
        d.text((M, y), rot, fill=(220, 200, 150), font=fonte(14))
        x = M
        for im, r in ims:
            d.text((x, y + ROT), r, fill=(150, 140, 120), font=fonte(13))
            folha.paste(im, (x, y + 2 * ROT))
            x += im.width + M
        y += max(im.height for im, _ in ims) + 2 * ROT + M
    folha.save(AQUI.parent / "folha-criacao-r2.png", optimize=True)
    print(folha.size)


if __name__ == "__main__":
    main()
