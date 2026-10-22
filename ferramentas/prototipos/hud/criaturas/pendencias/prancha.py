"""As propostas que aguardam decisão e os conceitos reservados (22/10/2026), numa folha só, sem redesenhar nada
(pendencias.png): o Esqueleto E1r; o urso r4 e o falcão do acampamento, na fogueira; o cajado aprovado no Atacar do
Mago (trocado só na página: protótipo); e os conceitos reservados (o Esqueleto E2, o Bandido do chapéu).
    python prancha.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
HUD = AQUI.parents[1]
CRI = AQUI.parent
ACA = HUD / "acampamento_atacar"
CARVAO, TEXTO, TEXTO2, AVISO = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255), (214, 170, 90, 255)


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


def nicho(im16, lado):
    cx = Image.new("RGBA", (lado + 6, lado + 6), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, lado + 4, lado + 4))
    cx.alpha_composite(amplia(im16, lado // 16), (3, 3))
    return cx


def oito(im16):
    f = Image.new("RGBA", (16, 16), (24, 21, 19, 255)); f.alpha_composite(im16)
    return amplia(f, 8)


if __name__ == "__main__":
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 1400), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Pendências em 22/10/2026: propostas aguardando decisão e conceitos reservados (nada disto está no jogo)",
           fill=TEXTO, font=f)
    y = 40
    # o Esqueleto E1r
    e1r = Image.open(CRI / "esqueleto_novo/proposta/esqueleto-e1r-16.png").convert("RGBA")
    d.text((20, y), "Esqueleto E1r (esqueleto_novo/esqueleto-e1r) — EM AVALIAÇÃO: a direção escolhida (E1, o guarda morto) com a aba "
                    "do elmo limpa; carta 32 | Bestiário 48 | 8×", fill=AVISO, font=f2)
    out.alpha_composite(nicho(e1r, 32), (20, y + 18)); out.alpha_composite(nicho(e1r, 48), (70, y + 18)); out.alpha_composite(oito(e1r), (140, y + 18))
    y += 18 + 128 + 20
    # o urso r4 e o falcão
    cap = ACA / "capturas"
    for nome, arq, ident, rot in (("Urso Pardo r4", "fogueira-urso-r4.png", "animal-urso-r4", "EM AVALIAÇÃO: o refinamento pelas referências"),
                                  ("Falcão Peregrino", "fogueira-falcao-proposta.png", "animal-falcao", "EM AVALIAÇÃO: a primeira proposta, no toco")):
        d.text((20, y), f"{nome} no acampamento (acampamento_atacar/{ident}) — {rot}; na fogueira, tamanho real | 2× | 8×",
               fill=AVISO, font=f2)
        rec = Image.open(cap / arq).convert("RGBA").crop((340, 120, 520, 205))
        out.alpha_composite(rec, (20, y + 18)); out.alpha_composite(amplia(rec, 2), (210, y + 18))
        out.alpha_composite(oito(Image.open(ACA / f"proposta/{ident}-16.png").convert("RGBA")), (580, y + 18))
        y += 18 + 170 + 16
    # o cajado
    d.text((20, y), "O cajado aprovado no Atacar do Mago (acampamento_atacar, roda-mago-cajado) — EM AVALIAÇÃO; trocado só na página "
                    "(protótipo): hoje | teste, tamanho real e 4×", fill=AVISO, font=f2)
    import json
    reg = json.loads((cap / "registro.json").read_text(encoding="utf-8"))
    for j, n in enumerate(("roda-mago", "roda-mago-cajado")):
        im = Image.open(cap / f"{n}.png").convert("RGBA")
        x0, y0, x1, y1 = reg[n]["icone"]
        rec = im.crop((x0 - 8, y0 - 6, x1 + 80, y1 + 6))
        out.alpha_composite(rec, (20 + j * 560, y + 18)); out.alpha_composite(amplia(rec, 4), (20 + j * 560, y + 18 + rec.height + 8))
    y += 18 + 44 + 8 + 176 + 20
    # os conceitos reservados
    d.text((20, y), "CONCEITOS RESERVADOS (não autorizam criar entidade, regra nem mapeamento): o Esqueleto E2, encapuzado, para um possível "
                    "mago esqueleto | o Bandido do chapéu, para um possível chefe", fill=TEXTO2, font=f2)
    e2 = Image.open(CRI / "esqueleto_novo/proposta/esqueleto-e2-16.png").convert("RGBA")
    ch = Image.open(CRI / "lobo_bandido/proposta/bandido-chapeu-16.png").convert("RGBA")
    for j, im in enumerate((e2, ch)):
        out.alpha_composite(nicho(im, 32), (20 + j * 300, y + 18)); out.alpha_composite(nicho(im, 48), (70 + j * 300, y + 18))
        out.alpha_composite(oito(im), (140 + j * 300, y + 18))
    y += 18 + 128 + 16
    out = out.crop((0, 0, 1500, y))
    out.save(AQUI / "pendencias.png")
    print("pendencias.png", out.size)
