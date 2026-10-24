"""As folhas da segunda rodada (24/10/2026), a partir de ../capturas-v2/ (fotografar.mjs):

    folha-v2.png            cada momento: o jogo atual e as direções A, B e C, no mesmo instante (900 ms)
    folha-v2-ritmo.png      o nível e o lendário de cada direção nos seis instantes (60 a 2400 ms)
    folha-v2-apertados.png  1280×720 e movimento reduzido, nas três

    python folhas_v2.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

CAP = pathlib.Path(__file__).resolve().parents[1] / "capturas-v2"
DIRECOES = [("relicario", "A · Relicário"), ("estouro", "B · Estouro"), ("estandarte", "C · Estandarte")]
MOMENTOS = [("nivel", "nivel", "Um nível (real)"), ("dois-niveis", "nivel3", "Dois níveis: o 3 (real)"),
            ("nivel4", "nivel", "Nível 4, a encruzilhada (real)"), ("sigilo", "sigilo", "Sigilo (real)"),
            ("especializacao", "spec", "Especialização (real)"), ("raridades", "comum", "Comum (real)"),
            ("raridades", "magico", "Mágico (real)"), ("raridades", "raro", "Raro (real)"),
            ("raridades", "lendario", "Lendário (real)"), ("limites", "nivel", "SIMULAÇÃO: nível com textos longos"),
            ("limites", "lendario", "SIMULAÇÃO: lendário com nome longo")]
INSTANTES = ["0060", "0250", "0500", "0900", "1600", "2400"]
FUNDO, TINTA, APAGADO = (14, 13, 12), (232, 220, 190), (150, 140, 120)
try:
    FONTE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
except OSError:
    FONTE = ImageFont.load_default()


def quadro(caminho, caixa, esc):
    if not caminho.exists():
        return None
    im = Image.open(caminho).convert("RGB")
    if caixa:
        im = im.crop(caixa)
    return im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)


def folha(cabecalho, linhas, saida, larg_vazio=300):
    gap, topo = 10, 30
    alturas = [max((i.height for i in ims if i), default=40) for _, ims in linhas]
    larguras = [max((ims[k].width for _, ims in linhas if k < len(ims) and ims[k]), default=larg_vazio)
                for k in range(max(len(ims) for _, ims in linhas))]
    W = sum(larguras) + gap * (len(larguras) + 1)
    H = topo + sum(alturas) + (topo + gap) * len(linhas) + gap
    f = Image.new("RGB", (W, H), FUNDO)
    d = ImageDraw.Draw(f)
    x = gap
    for k, rot in enumerate(cabecalho):
        d.text((x, 4), rot, fill=TINTA, font=FONTE)
        x += larguras[k] + gap
    y = topo
    for (rot, ims), alt in zip(linhas, alturas):
        d.text((gap, y + 4), rot, fill=TINTA, font=FONTE)
        y += topo
        x = gap
        for k, i in enumerate(ims):
            if i:
                f.paste(i, (x, y))
            else:
                d.text((x, y + 10), "(sem captura)", fill=APAGADO, font=FONTE)
            x += larguras[k] + gap
        y += alt + gap
    f.save(saida, optimize=True)
    print(saida.name, f.size)


def main():
    meio = (360, 0, 1560, 945)
    linhas = [(rot, [quadro(CAP / d / "1920" / f"{s}-{foto}-0900.png", meio, 0.4) for d in ["atual"] + [x for x, _ in DIRECOES]])
              for s, foto, rot in MOMENTOS]
    folha(["Jogo atual"] + [n for _, n in DIRECOES], linhas, CAP / "folha-v2.png")
    linhas = []
    for d, nome in DIRECOES:
        for s, foto, rot in [("nivel", "nivel", "nível"), ("raridades", "lendario", "lendário")]:
            linhas.append((f"{nome}, {rot}", [quadro(CAP / d / "1920" / f"{s}-{foto}-{ms}.png", meio, 0.3) for ms in INSTANTES]))
    folha([f"{int(ms)} ms" for ms in INSTANTES], linhas, CAP / "folha-v2-ritmo.png")
    linhas = []
    for d, nome in DIRECOES:
        linhas.append((nome, [quadro(CAP / d / "1280" / "dois-niveis-nivel2-0900.png", None, 0.45),
                              quadro(CAP / d / "1280" / "limites-nivel-0900.png", None, 0.45),
                              quadro(CAP / d / "1280" / "raridades-lendario-0900.png", None, 0.45),
                              quadro(CAP / d / "reduzido" / "nivel-nivel-0900.png", meio, 0.36),
                              quadro(CAP / d / "reduzido" / "raridades-lendario-0900.png", meio, 0.36)]))
    folha(["1280: dois níveis", "1280: SIMULAÇÃO limites", "1280: lendário", "reduzido: nível", "reduzido: lendário"],
          linhas, CAP / "folha-v2-apertados.png")


if __name__ == "__main__":
    main()
