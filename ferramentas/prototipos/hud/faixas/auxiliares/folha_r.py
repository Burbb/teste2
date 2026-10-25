"""Monta a comparação da original × a original refinada (R) a partir de ../capturas/ (fotografar.mjs com
VERSOES=atual,r): cada caso numa linha (Vitória, Mestre caçador, Você caiu, Exausto, Saindo da capela, a chegada à
comitiva com o nome longo), a de hoje à esquerda e a R à direita, a faixa inteira (de lado a lado) da janela de
1920×945 em meio tamanho; embaixo, a R a 1280×720 em meio tamanho (os textos longos). Grava ../folha-original-refinada.png.
A leitura se julga nas fotos em tamanho real, em ../capturas/.

    python ferramentas/prototipos/hud/faixas/auxiliares/folha_r.py
    python ferramentas/prototipos/hud/faixas/auxiliares/folha_r.py jogo     # a antiga × o jogo integrado (1.205.0)
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw

from folha import CAP, FUNDO, NOTA, TITULO, fonte

AQUI = pathlib.Path(__file__).resolve().parent
CASOS = [("vitoria", "Vitória"), ("mestre", "Mestre caçador (o subtítulo)"), ("queda", "Você caiu"), ("exausto", "Exausto"),
         ("saindo", "Saindo da capela (o texto longo)"), ("comitiva", "Irmã Odette se junta a você (o nome longo)")]


def faixa(jan, v, caso, medidas, folga=46):
    im = Image.open(CAP / f"{jan}-{v}-{caso}.png").convert("RGB")
    x, y, w, h = (medidas.get(f"{jan}-{v}-{caso}") or {}).get("caixa", [0, im.height // 2 - 60, im.width, 120])
    return im.crop((0, max(0, y - folga), im.width, min(im.height, y + h + folga)))


def main():
    if sys.argv[1:] == ["jogo"]:
        dir_, saida, nome = "jogo", "folha-integrada.png", "o jogo (1.205.0, a R integrada)"
    else:
        dir_, saida, nome = "r", "folha-original-refinada.png", "R · a original refinada"
    medidas = json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"]
    meia = lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS)  # noqa: E731
    linhas = [(rot, [meia(faixa("1920", v, c, medidas)) for v in ("atual", dir_)]) for c, rot in CASOS]
    baixas = [meia(faixa("1280", dir_, c, medidas)) for c in ("comitiva", "saindo", "mestre")]
    M, ROT = 12, 22
    larg = max(sum(i.width for i in ims) + M * 3 for _, ims in linhas)
    alt = 70 + sum(max(i.height for i in ims) + ROT + M for _, ims in linhas) + 40 + sum(i.height + M for i in baixas[:2])
    folha = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 10), f"As faixas: a antiga × {nome}, com os mesmos dados, no jogo (1920×945, a meio tamanho; "
                    "a faixa inteira, de lado a lado)", fill=TITULO, font=fonte(16))
    d.text((M, 40), "a antiga (até a 1.204.1)", fill=TITULO, font=fonte(15))
    d.text((M * 2 + linhas[0][1][0].width, 40), nome, fill=TITULO, font=fonte(15))
    y = 64
    for rot, ims in linhas:
        d.text((M, y), rot, fill=NOTA, font=fonte(13))
        x = M
        for im in ims:
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(i.height for i in ims) + ROT + M
    d.text((M, y + 6), f"{nome} a 1280×720 (a meio tamanho): a comitiva, a saída da capela e o Mestre caçador", fill=TITULO, font=fonte(15))
    y += 32
    x, y0 = M, y
    for k, im in enumerate(baixas):
        if x + im.width > larg:
            x, y0 = M, y0 + baixas[0].height + M
        folha.paste(im, (x, y0))
        x += im.width + M
    folha = folha.crop((0, 0, larg, y0 + baixas[-1].height + M))
    folha.save(AQUI.parent / saida)
    print(folha.size)


if __name__ == "__main__":
    main()
