"""Monta a folha comparativa dos quadros de orientação a partir de ../capturas/ (fotografar.mjs): cada caso numa linha
(no alto, nas laterais, embaixo, na página, na janela do achado, na luta e na luta guiada; curtos e longos), os de hoje,
a B e a B refinada (R) lado a lado, em tamanho real, recortados em volta do quadro e do controle que ele explica (o
mesmo recorte nas três). Em cima a janela de 1920×945; embaixo, cinco casos a 1280×720. Grava ../folha-orientacao.png
(a folha da primeira rodada, hoje × A × B, ficou no histórico do git).

    python ferramentas/prototipos/hud/orientacao/auxiliares/folha.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
FUNDO, TITULO, NOTA = (22, 18, 14), (220, 200, 150), (150, 140, 120)
VERSOES = [("atual", "hoje"), ("b", "B · chamada contextual"), ("r", "R · a B refinada (candidata)")]
CASOS_1920 = [("v1", "V1 · o mural (na página)"), ("c1", "C1 · luta guiada: Habilidades"),
              ("c2", "C2 · luta guiada: a habilidade (abaixo da linha)"), ("c3", "C3 · luta guiada: o alvo"),
              ("c4", "C4 · luta guiada: o que gastou (Entendi)"), ("a1", "A1 · no alto (o botão Texto)"), ("b1", "B1 · lateral esquerda, curto (o baú)"),
              ("k2", "K2 · lateral direita (o contrato)"), ("n1", "N1 · lateral direita, longo (a noite)"),
              ("v2", "V2 · na página (o Templo)"), ("v4", "V4 · embaixo, longo (a Comitiva)"),
              ("e1", "E1 · abaixo da janela do achado"), ("al", "AL · na luta, sem seta")]
CASOS_1280 = [("v1", "V1"), ("c2", "C2"), ("c4", "C4"), ("n1", "N1"), ("v4", "V4")]


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def caixa_comum(jan, caso, medidas, folga=26):
    """O retângulo que cobre o quadro e o controle nas três versões (o mesmo recorte para comparar)."""
    xs, ys = [], []
    for v, _ in VERSOES:
        m = medidas.get(f"{jan}-{v}-{caso}")
        if not m:
            continue
        for r in (m["caixa"], m.get("alvo")):
            if r:
                xs += [r[0], r[0] + r[2]]
                ys += [r[1], r[1] + r[3]]
    W, H = (1920, 945) if jan == "1920" else (1280, 720)
    return (max(0, min(xs) - folga), max(0, min(ys) - folga), min(W, max(xs) + folga), min(H, max(ys) + folga))


def main():
    medidas = json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"]
    blocos = []
    for jan, casos in (("1920", CASOS_1920), ("1280", CASOS_1280)):
        for caso, rot in casos:
            box = caixa_comum(jan, caso, medidas)
            ims = []
            for v, _ in VERSOES:
                arq = CAP / f"{jan}-{v}-{caso}.png"
                ims.append(Image.open(arq).convert("RGB").crop(box) if arq.exists() else None)
            blocos.append((f"{rot} · {jan}", ims))
    M, ROT = 12, 20
    largura = max(sum(i.width for i in ims if i) + M * 4 for _, ims in blocos)
    altura = 64 + sum(max(i.height for i in ims if i) + ROT + M for _, ims in blocos)
    folha = Image.new("RGB", (largura, altura), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "Os quadros de orientação: hoje × B (chamada contextual) × R (a B refinada), com o mesmo estado, no jogo "
                    "(tamanho real)", fill=TITULO, font=fonte(16))
    x = M
    for _, nome in VERSOES:
        d.text((x, 36), nome, fill=TITULO, font=fonte(14))
        x += blocos[0][1][0].width + M
    y = 58
    for rot, ims in blocos:
        d.text((M, y), rot, fill=NOTA, font=fonte(13))
        x = M
        for im in ims:
            if im:
                folha.paste(im, (x, y + ROT))
                x += im.width + M
        y += max(i.height for i in ims if i) + ROT + M
    folha.save(AQUI.parent / "folha-orientacao.png")
    print(folha.size)


if __name__ == "__main__":
    main()
