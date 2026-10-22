"""A folha compacta das integrações da 1.179.0 à 1.181.1 (integracoes-1181.png), só com as capturas do jogo com os
arquivos de produção, a 1920×945, em tamanho real: o Mercenário e o Lobo Gélido na carta, no Bestiário, no cartaz do
mural e no rastreador (criaturas/mercenario_lobo_gelido/capturas-1179); o caixote nos suprimentos esgotados, com o
cadeado nos outros motivos; embaixo, os arquivos a 1× e 3× e a conferência dos nomes num save de antes da troca.
    python prancha_1181.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

HUD = pathlib.Path(__file__).resolve().parents[1]
CAP = HUD / "criaturas/mercenario_lobo_gelido/capturas-1179"
ICONES = HUD.parents[2] / "rpg/web/static/hud/icones"
FOTOS = [
    ("1.179.0 — a carta da luta (32): o Mercenário (MA) e o Lobo Gélido (LA), ao lado do Lobo, do Bandido, do Cultista e do "
     "Esqueleto", "luta.png", (1000, 55, 1475, 240)),
    ("o Bestiário (48)", "bestiario.png", (585, 410, 1295, 602)),
    ("os contratos de caça: o cartaz do mural (48) e o rastreador (32)", "contratos.png", (580, 655, 1060, 800)),
    ("", "contratos-rastreador.png", None),
    ("1.180.0 — o mercado: o caixote nos três \"Esgotado\"; o cadeado nos \"Ouro insuficiente.\"", "mercado.png",
     (435, 415, 1440, 595)),
]
SAVE = [
    "1.181.0 — um save gravado pela 1.178.0 (formato 5), carregado na 1.181.1:",
    "  guardião: \"Vharnar, o Ent Ancião\" → \"Vharnar, a Árvore Anciã\" (também na luta); rumor: \"Vharnar, a Árvore Anciã, vive em "
    "Clareira dos Sussurros.\"",
    "  contrato aceito 23, 1/4: \"Eliminar 4 ents jovens em Bosque da Névoa.\" → \"Eliminar 4 árvores despertas em Bosque da Névoa.\" "
    "(o progresso e o id iguais)",
    "  mural: \"Caçar Vhararmus, um ent jovem enorme…\" → \"Caçar Vhararmus, uma árvore desperta enorme…\"; salvar e carregar de "
    "novo: o mesmo save (formato 6)",
]


def main():
    f = ImageFont.truetype("arial.ttf", 14)
    ims = []
    for t, arq, caixa in FOTOS:
        im = Image.open(CAP / arq).convert("RGBA")
        ims.append((t, im.crop(caixa) if caixa else im))
    icones = [Image.open(ICONES / f"{n}-16.png").convert("RGBA") for n in ("retrato-mercenario", "retrato-lobo-gelido",
                                                                           "motivo-esgotado")]
    w = max(im.width for _, im in ims) + 340
    h = sum(im.height + (26 if t else 8) for t, im in ims) + 90 + 20 * len(SAVE) + 30
    out = Image.new("RGBA", (w, h), (13, 11, 10, 255))
    d = ImageDraw.Draw(out)
    y = 12
    for n, (t, im) in enumerate(ims):
        if t:
            d.text((16, y), t, fill=(210, 210, 214, 255), font=f)
            y += 20
        x = 16
        if n == 3:  # o rastreador ao lado do cartaz
            y -= ims[2][1].height + 8
            x = 16 + ims[2][1].width + 24
        out.alpha_composite(im, (x, y))
        y += im.height + 8
    d.text((16, y), "os arquivos a 1× e a 3× (o retrato 16 e o motivo 16)", fill=(210, 210, 214, 255), font=f)
    y += 20
    for n, im in enumerate(icones):
        out.alpha_composite(im, (16 + n * 80, y + 16))
        out.alpha_composite(im.resize((48, 48), Image.NEAREST), (16 + n * 80 + 22, y))
    y += 64
    for linha in SAVE:
        d.text((16, y), linha, fill=(210, 210, 214, 255), font=f)
        y += 20
    out = out.crop((0, 0, w, y + 10))
    out.save(pathlib.Path(__file__).resolve().parent / "integracoes-1181.png")
    print("integracoes-1181.png", out.size)


if __name__ == "__main__":
    main()
