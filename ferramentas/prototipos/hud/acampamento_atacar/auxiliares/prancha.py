"""A folha do levantamento (levantamento.png): o animal do patrulheiro na fogueira (o lobo, o urso e o falcão, como o
jogo desenha hoje), o recorte em tamanho real e a 4×; o comando Atacar das três classes na roda da luta (o Arqueiro
como está, com o arco aprovado trocado só na página e com a Besta equipada; o Guerreiro e o Mago), em tamanho real e a
4×, sem suavização; os retratos aprovados dos três animais, para a identidade.
    python auxiliares/prancha.py            # levantamento.png
    python auxiliares/prancha.py animais    # animais-cajado.png
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
JOGO = AQUI.parents[4] / "rpg/web/static/hud/icones"
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
REG = json.loads((CAP / "registro.json").read_text(encoding="utf-8"))


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def folha():
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1800), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Levantamento (21/10/2026; nada no jogo): o animal no acampamento e o comando Atacar", fill=TEXTO, font=f)
    y = 40
    d.text((20, y), "1. A fogueira hoje (1920×945; a arte de 320×72 no canvas de 1064×208): o lobo e o urso recebem o sprite "
                    "\"fera\" (a cabeça de lobo do traço), o falcão o \"voador\" (o morcego do traço)", fill=TEXTO, font=f2)
    y += 20
    for j, t in enumerate(("lobo", "urso", "falcao")):
        im = Image.open(CAP / f"fogueira-{t}.png").convert("RGBA")
        rec = im.crop((350, 125, 530, 205))
        d.text((20, y), {"lobo": "Lobo Cinzento", "urso": "Urso Pardo", "falcao": "Falcão Peregrino"}[t] + " — tamanho real | 2×",
               fill=TEXTO2, font=f2)
        out.alpha_composite(rec, (20, y + 16)); out.alpha_composite(amplia(rec, 2), (220, y + 16))
        y += 16 + 160 + 10
    y += 6
    d.text((20, y), "os retratos aprovados (a identidade a seguir, não o desenho da cena): Lobo | Urso | Falcão, a 3×",
           fill=TEXTO, font=f2)
    y += 18
    for j, n in enumerate(("lobo", "urso", "falcao")):
        out.alpha_composite(amplia(Image.open(JOGO / f"retrato-{n}-16.png").convert("RGBA"), 3), (20 + j * 70, y))
    y += 48 + 24
    d.text((20, y), "2. O comando Atacar na roda (o ícone a 32 px na caixa de 34): tamanho real e 4×", fill=TEXTO, font=f2)
    y += 20
    casos = (("roda-arqueiro", "Arqueiro hoje: o sprite \"arco\" 16×16 a 2×"),
             ("roda-arqueiro-arco", "Arqueiro, teste: o arco aprovado (arco-32)"),
             ("roda-arqueiro-besta", "Arqueiro com a Besta: o mesmo sprite \"arco\""),
             ("roda-guerreiro", "Guerreiro: a espada aprovada (espada-32)"),
             ("roda-mago", "Mago: o sprite \"cajado\" 16×16 a 2×"))
    for j, (n, rot) in enumerate(casos):
        im = Image.open(CAP / f"{n}.png").convert("RGBA")
        x0, y0, x1, y1 = REG[n]["icone"]
        rec = im.crop((x0 - 8, y0 - 6, x1 + 8, y1 + 22))
        x = 20 + j * 290
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(rec, (x, y + 18)); out.alpha_composite(amplia(rec, 4), (x, y + 18 + rec.height + 10))
    y += 18 + 60 + 10 + 4 * 60 + 20
    d.text((20, y), "a roda inteira, tamanho real: Arqueiro hoje | com o arco aprovado", fill=TEXTO, font=f2)
    y += 18
    for j, n in enumerate(("roda-arqueiro", "roda-arqueiro-arco")):
        im = Image.open(CAP / f"{n}.png").convert("RGBA")
        out.alpha_composite(im, (20, y)); y += im.height + 8
    out = out.crop((0, 0, 1500, y + 12))
    out.save(PASTA / "levantamento.png")
    print("levantamento.png", out.size)


def folha_animais():
    """Os animais propostos e o cajado (animais-cajado.png): cada animal na fogueira, hoje × proposta (o recorte em
    tamanho real e a 2×), a figura a 8× e o retrato aprovado (a identidade); o Atacar do Mago, hoje × o cajado aprovado,
    em tamanho real e a 4×. Sem suavização."""
    import grades as gr
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Os animais do patrulheiro no acampamento (proposta) e o cajado no Atacar do Mago (teste); nada no jogo",
           fill=TEXTO, font=f)
    y = 38
    for t, nome in (("lobo", "Lobo Cinzento, deitado"), ("urso", "Urso Pardo, sentado"), ("falcao", "Falcão Peregrino, no toco")):
        d.text((20, y), f"{nome} — na fogueira: hoje | proposta (tamanho real), proposta a 2× | a figura a 8× | o retrato aprovado a 3×",
               fill=TEXTO2, font=f2)
        hoje = Image.open(CAP / f"fogueira-{t}.png").convert("RGBA").crop((340, 120, 520, 205))
        nova = Image.open(CAP / f"fogueira-{t}-proposta.png").convert("RGBA").crop((340, 120, 520, 205))
        out.alpha_composite(hoje, (20, y + 18)); out.alpha_composite(nova, (210, y + 18))
        out.alpha_composite(amplia(nova, 2), (400, y + 18))
        fig = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); fig.alpha_composite(gr.imagem(f"animal-{t}"))
        out.alpha_composite(amplia(fig, 8), (770, y + 18))
        out.alpha_composite(amplia(Image.open(JOGO / f"retrato-{t}-16.png").convert("RGBA"), 3), (910, y + 18))
        y += 18 + 170 + 14
    d.text((20, y), "o Atacar do Mago: hoje (o sprite \"cajado\" 16×16 a 2×) | o cajado aprovado (cajado-32), trocado só na página — "
                    "tamanho real e 4×", fill=TEXTO, font=f2)
    y += 20
    for j, n in enumerate(("roda-mago", "roda-mago-cajado")):
        im = Image.open(CAP / f"{n}.png").convert("RGBA")
        x0, y0, x1, y1 = REG[n]["icone"]
        rec = im.crop((x0 - 8, y0 - 6, x1 + 80, y1 + 6))
        out.alpha_composite(rec, (20 + j * 560, y)); out.alpha_composite(amplia(rec, 4), (20 + j * 560, y + rec.height + 8))
    y += 44 + 8 + 4 * 44 + 20
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / "animais-cajado.png")
    print("animais-cajado.png", out.size)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["animais"]:
        folha_animais()
    else:
        folha()
