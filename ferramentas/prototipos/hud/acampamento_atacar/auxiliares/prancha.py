"""A folha do levantamento (levantamento.png): o animal do patrulheiro na fogueira (o lobo, o urso e o falcão, como o
jogo desenha hoje), o recorte em tamanho real e a 4×; o comando Atacar das três classes na roda da luta (o Arqueiro
como está, com o arco aprovado trocado só na página e com a Besta equipada; o Guerreiro e o Mago), em tamanho real e a
4×, sem suavização; os retratos aprovados dos três animais, para a identidade.
    python auxiliares/prancha.py            # levantamento.png
    python auxiliares/prancha.py animais    # animais-cajado.png
    python auxiliares/prancha.py rodada2    # rodada2.png
    python auxiliares/prancha.py rodada3    # rodada3.png
    python auxiliares/prancha.py rodada4    # rodada4.png
    python auxiliares/prancha.py lobo-r5    # lobo-r5.png
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


def folha_rodada2():
    """A segunda rodada (rodada2.png): antes × depois do Esqueleto E1 (o elmo limpo; a carta e o Bestiário em tamanho
    real, a 4× e a 12×) e do lobo e do urso na fogueira (o recorte em tamanho real e a 2×, ao lado do arqueiro sentado,
    e a figura a 8×). Sem suavização."""
    import grades as gr
    esq = AQUI.parents[1] / "criaturas/esqueleto_novo/proposta"
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1500), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Antes × depois (proposta; nada no jogo): o Esqueleto E1 e o lobo e o urso do acampamento", fill=TEXTO, font=f)

    def nicho(im16, lado):
        cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
        cx.alpha_composite(amplia(im16, lado // 16), (3, 3)); return cx
    y = 38
    d.text((20, y), "E1 (o guarda morto) × E1r (a ponta direita da aba limpa: o pixel da coluna 14 sai) — 32 e 48 em tamanho real, "
                    "a 4× e a 12×", fill=TEXTO2, font=f2)
    y += 18
    for j, n in enumerate(("esqueleto-e1", "esqueleto-e1r")):
        im = Image.open(esq / f"{n}-16.png").convert("RGBA")
        x = 20 + j * 600
        out.alpha_composite(nicho(im, 32), (x, y)); out.alpha_composite(nicho(im, 48), (x + 44, y))
        out.alpha_composite(amplia(nicho(im, 48), 4), (x, y + 60))
        g = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); g.alpha_composite(im)
        out.alpha_composite(amplia(g, 12), (x + 230, y + 60))
    y += 60 + 216 + 20
    for t, nome in (("lobo", "Lobo Cinzento"), ("urso", "Urso Pardo")):
        d.text((20, y), f"{nome} — na fogueira: a primeira rodada | a segunda (tamanho real), a segunda a 2× | as figuras a 8×: "
                        "primeira | segunda", fill=TEXTO2, font=f2)
        antes = Image.open(CAP / f"fogueira-{t}-proposta.png").convert("RGBA").crop((340, 120, 520, 205))
        depois = Image.open(CAP / f"fogueira-{t}-r2.png").convert("RGBA").crop((340, 120, 520, 205))
        out.alpha_composite(antes, (20, y + 18)); out.alpha_composite(depois, (210, y + 18))
        out.alpha_composite(amplia(depois, 2), (400, y + 18))
        for k, ident in enumerate((f"animal-{t}", f"animal-{t}-r2")):
            fig = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); fig.alpha_composite(gr.imagem(ident))
            out.alpha_composite(amplia(fig, 8), (770 + k * 140, y + 18))
        y += 18 + 170 + 16
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / "rodada2.png")
    print("rodada2.png", out.size)


def folha_rodada(r_antes, r_depois, saida, titulo):
    """Uma rodada do lobo e do urso (`saida`): a referência gerada (reduzida) e a guia; na fogueira, a rodada
    `r_antes` × a `r_depois` (o recorte em tamanho real e a 2×, ao lado do arqueiro sentado, com a luz do fogo); as
    figuras a 8× (segunda | terceira). Sem suavização."""
    import grades as gr
    refs = AQUI.parents[4] / "ferramentas/arte/referencias/icones"
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), titulo,
           fill=TEXTO, font=f)
    y = 38
    for t, nome, arq in (("lobo", "Lobo Cinzento, deitado", "Lobo cinzento deitado em pixel art-1.png"),
                         ("urso", "Urso Pardo, sentado", "Urso-pardo sentado em pixel art-2.png")):
        d.text((20, y), f"{nome} — a referência (reduzida) | a guia a 8× | na fogueira: antes | depois (tamanho real), "
                        "depois a 2× | as figuras a 8×: antes | depois", fill=TEXTO2, font=f2)
        ref = Image.open(refs / arq).convert("RGBA")
        fundo = Image.new("RGBA", ref.size, (24, 21, 19, 255)); fundo.alpha_composite(ref)
        fundo.thumbnail((128, 128), Image.LANCZOS)
        out.alpha_composite(fundo, (20, y + 18))
        g = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); g.alpha_composite(Image.open(PASTA / f"guias/{t}-guia-16.png").convert("RGBA"))
        out.alpha_composite(amplia(g, 8), (160, y + 18))
        antes = Image.open(CAP / f"fogueira-{t}-{r_antes}.png").convert("RGBA").crop((340, 120, 520, 205))
        depois = Image.open(CAP / f"fogueira-{t}-{r_depois}.png").convert("RGBA").crop((340, 120, 520, 205))
        out.alpha_composite(antes, (300, y + 18)); out.alpha_composite(depois, (490, y + 18))
        out.alpha_composite(amplia(depois, 2), (680, y + 18))
        for k, ident in enumerate((f"animal-{t}-{r_antes}", f"animal-{t}-{r_depois}")):
            fig = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); fig.alpha_composite(gr.imagem(ident))
            out.alpha_composite(amplia(fig, 8), (1050 + k * 140, y + 18))
        y += 18 + 170 + 16
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / saida)
    print(saida, out.size)


def folha_lobo_r5():
    """O lobo r5 (lobo-r5.png): na fogueira, o r4 × o r5 (tamanho real e 2×) e, para a escala, o urso r4 na mesma cena;
    as figuras a 8× (r4 | r5 | o urso r4). Sem suavização."""
    import grades as gr
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 500), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O lobo: antes (r4, bab7afba) × depois (r5, mais alto), na fogueira a 1920×945; o urso r4 para a escala; "
                     "proposta, nada no jogo", fill=TEXTO, font=f)
    y = 38
    d.text((20, y), "na fogueira: lobo r4 | lobo r5 | urso r4 (tamanho real); o lobo r5 a 2×", fill=TEXTO2, font=f2)
    rec = lambda n: Image.open(CAP / f"{n}.png").convert("RGBA").crop((340, 120, 520, 205))
    for k, n in enumerate(("fogueira-lobo-r4", "fogueira-lobo-r5", "fogueira-urso-r4")):
        out.alpha_composite(rec(n), (20 + k * 190, y + 18))
    out.alpha_composite(amplia(rec("fogueira-lobo-r5"), 2), (600, y + 18))
    y += 18 + 170 + 16
    d.text((20, y), "as figuras a 8×: lobo r4 | lobo r5 | urso r4", fill=TEXTO2, font=f2)
    for k, ident in enumerate(("animal-lobo-r4", "animal-lobo-r5", "animal-urso-r4")):
        fig = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); fig.alpha_composite(gr.imagem(ident))
        out.alpha_composite(amplia(fig, 8), (20 + k * 140, y + 18))
    y += 18 + 128 + 16
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / "lobo-r5.png")
    print("lobo-r5.png", out.size)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["animais"]:
        folha_animais()
    elif sys.argv[1:] == ["rodada2"]:
        folha_rodada2()
    elif sys.argv[1:] == ["rodada3"]:
        folha_rodada("r2", "r3", "rodada3.png", "O lobo e o urso pelas referências geradas: antes (segunda rodada) × depois "
                     "(terceira); proposta, nada no jogo")
    elif sys.argv[1:] == ["lobo-r5"]:
        folha_lobo_r5()
    elif sys.argv[1:] == ["rodada4"]:
        folha_rodada("r3", "r4", "rodada4.png", "O lobo e o urso refinados: antes (terceira rodada, 23bb15bb) × depois "
                     "(quarta), na fogueira a 1920×945; proposta, nada no jogo")
    else:
        folha()
