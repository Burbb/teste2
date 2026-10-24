"""Monta a folha compacta das faixas a partir de ../capturas/ (fotografar.mjs): cada caso numa linha (Vitória,
Guardião, Mestre caçador, Você caiu, Exausto, Saindo da capela, a chegada à comitiva), com a faixa de hoje, a A e a B
lado a lado, recortadas no palco da janela de 1920×945 em meio tamanho (a faixa de hoje atravessa a janela: o recorte
mostra o palco e a beira das colunas); embaixo, o Mestre caçador e a comitiva (o subtítulo e o nome longo) a 1280×720, em meio
tamanho. Grava ../folha-faixas.png. A leitura se julga nas fotos em tamanho real, em ../capturas/.

    python ferramentas/prototipos/hud/faixas/auxiliares/folha.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
FUNDO, TITULO, NOTA = (22, 18, 14), (220, 200, 150), (150, 140, 120)
CASOS = [("vitoria", "Vitória (comum)"), ("guardiao", "Guardião derrotado (marco)"), ("mestre", "Mestre caçador (marco, subtítulo)"),
         ("queda", "Você caiu (peso)"), ("exausto", "Exausto (peso)"), ("saindo", "Saindo da capela (passagem, o texto longo)"),
         ("comitiva", "Irmã Odette se junta a você (marco, o nome longo)")]
VERSOES = [("atual", "hoje"), ("a", "A · faixa no palco"), ("b", "B · emblema")]


def fonte(t):
    try:
        return ImageFont.truetype("georgia.ttf", t)
    except OSError:
        return ImageFont.load_default()


def recorte(jan, v, caso, medidas, meia_altura):
    im = Image.open(CAP / f"{jan}-{v}-{caso}.png").convert("RGB")
    m = medidas.get(f"{jan}-{v}-{caso}") or {}
    x0, w = (m.get("palco") or [0, im.width])
    caixa = m.get("caixa") or [0, im.height // 2 - 50, 0, 100]
    cy = caixa[1] + caixa[3] // 2
    y0 = max(46, min(im.height - 2 * meia_altura, cy - meia_altura))
    return im.crop((x0 - 12, y0, x0 + w + 12, y0 + 2 * meia_altura))


def main():
    medidas = json.loads((CAP / "medidas.json").read_text(encoding="utf-8"))["medidas"]
    meia = lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS)  # noqa: E731
    linhas = [(rot, [meia(recorte("1920", v, c, medidas, 170)) for v, _ in VERSOES]) for c, rot in CASOS]
    baixas = [(f"{rot} · 1280×720", [meia(recorte("1280", v, c, medidas, 150)) for v, _ in VERSOES[1:]])
              for c, rot in (("mestre", "Mestre caçador"), ("comitiva", "a comitiva"))]
    M, ROT = 12, 22
    larg = max(sum(i.width for i in ims) + M * (len(ims) + 1) for _, ims in linhas)
    alt = 70 + sum(max(i.height for i in ims) + ROT + M for _, ims in linhas)
    alt += 30 + max(i.height for _, ims in baixas for i in ims) + ROT + M
    folha = Image.new("RGB", (larg, alt), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 10), "As faixas de passagem: hoje × A (faixa integrada ao palco) × B (emblema e anúncio), com os mesmos dados, "
                    "no jogo (1920×945, a meio tamanho)", fill=TITULO, font=fonte(16))
    x = M
    for _, nome in VERSOES:
        d.text((x, 40), nome, fill=TITULO, font=fonte(15))
        x += linhas[0][1][0].width + M
    y = 64
    for rot, ims in linhas:
        d.text((M, y), rot, fill=NOTA, font=fonte(13))
        x = M
        for im in ims:
            folha.paste(im, (x, y + ROT))
            x += im.width + M
        y += max(i.height for i in ims) + ROT + M
    y += 8
    d.text((M, y), "A 1280×720 (a meio tamanho): A e B com os textos longos", fill=TITULO, font=fonte(15))
    y += 26
    x = M
    for rot, ims in baixas:
        for k, im in enumerate(ims):
            d.text((x, y), f"{rot} · {'AB'[k]}", fill=NOTA, font=fonte(12))
            folha.paste(im, (x, y + ROT))
            x += im.width + M
    folha = folha.crop((0, 0, larg, y + ROT + max(i.height for _, ims in baixas for i in ims) + M))
    folha.save(AQUI.parent / "folha-faixas.png")
    print(folha.size)


if __name__ == "__main__":
    main()
