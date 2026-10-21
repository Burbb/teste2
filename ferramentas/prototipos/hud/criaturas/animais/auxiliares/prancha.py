"""As folhas dos animais do patrulheiro: uma por animal (urso.png, falcao.png, lobo-cinzento.png), com a carta aliada na
luta e o ícone no painel da comitiva a 1920×945 (os mesmos dados), atual × as propostas, em tamanho real e a 2×, a 3×
na caixa da carta e a 12× sem suavização; e a fileira dos três (animais.png) junto dos retratos aprovados.
    python prancha.py
"""
import pathlib

from PIL import Image, ImageChops, ImageDraw, ImageFont

from previa import amplia, imagem

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
CAP = PASTA / "capturas"
RAIZ = AQUI.parents[5]
CARVAO, TEXTO, TEXTO2 = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255)
CARTA = (46, 140, 258, 192)        # a carta aliada do animal, no palco
PAINEL = (122, 610, 372, 668)      # a linha do animal no painel da comitiva, na página
INIMIGO = (830, 38, 1042, 90)      # a carta do Lobo inimigo (o retrato integrado na 1.163.0), no palco
ANIMAIS = {
    "urso": dict(titulo="Urso Pardo", modos=(("atual", "atual (fera)"), ("a", "A, de frente"), ("b", "B, de perfil")),
                 ids={"a": "urso-a", "b": "urso-b"}),
    "falcao": dict(titulo="Falcão Peregrino", modos=(("atual", "atual (voador)"), ("a", "A, a cabeça de perfil"),
                                                     ("b", "B, três quartos com a asa")), ids={"a": "falcao-a", "b": "falcao-b"}),
    "lobo": dict(titulo="Lobo Cinzento", modos=(("atual", "atual (fera)"), ("reaproveitado", "o Lobo integrado, sem mudança")),
                 ids={}),
}


def abre(n):
    return Image.open(CAP / n).convert("RGBA")


def caixa_dif(animal, arquivo, area, outro):
    """A caixa de 38 px do retrato em `area`: onde a foto `atual` e a do modo `outro` diferem."""
    a = abre(f"{animal}-atual-{arquivo}.png").crop(area).convert("RGB")
    b = abre(f"{animal}-{outro}-{arquivo}.png").crop(area).convert("RGB")
    bx = ImageChops.difference(a, b).getbbox()
    cx, cy = area[0] + (bx[0] + bx[2]) // 2, area[1] + (bx[1] + bx[3]) // 2
    return (cx - 19, cy - 19, cx + 19, cy + 19)


def lobo_jogo():
    return Image.open(RAIZ / "rpg/web/static/hud/icones/retrato-lobo-16.png").convert("RGBA")


def grade12(im16):
    g = amplia(im16, 12)
    fundo = Image.new("RGBA", g.size, (24, 21, 19, 255))
    fundo.alpha_composite(g)
    dd = ImageDraw.Draw(fundo)
    for i in range(1, 16):
        dd.line([(i * 12, 0), (i * 12, 192)], fill=(40, 36, 34, 255)); dd.line([(0, i * 12), (192, i * 12)], fill=(40, 36, 34, 255))
    return fundo


def folha(animal):
    a = ANIMAIS[animal]
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"{a['titulo']}, o animal do patrulheiro — " + " × ".join(r for _, r in a["modos"]) +
           "; 16×16 a 2× na carta e no painel; proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    outro = a["modos"][1][0]
    nic_c, nic_p = caixa_dif(animal, "palco", CARTA, outro), caixa_dif(animal, "pagina", PAINEL, outro)
    # 1. a carta aliada na luta e a linha do painel, em tamanho real e a 2×
    for j, (modo, rot) in enumerate(a["modos"]):
        x = 20 + j * 560
        carta, painel = abre(f"{animal}-{modo}-palco.png").crop(CARTA), abre(f"{animal}-{modo}-pagina.png").crop(PAINEL)
        d.text((x, y), rot, fill=TEXTO, font=f2)
        out.alpha_composite(carta, (x, y + 18)); out.alpha_composite(painel, (x + carta.width + 20, y + 18))
        out.alpha_composite(amplia(carta, 2), (x, y + 18 + 60))
        out.alpha_composite(amplia(painel, 2), (x, y + 18 + 60 + 2 * carta.height + 10))
    y += 18 + 60 + 2 * 52 + 10 + 2 * 58 + 20
    # 2. a caixa da carta a 3× (a da luta e a do painel) e a 12× das propostas
    d.text((20, y), "a caixa do retrato a 3× (na carta da luta | no painel da comitiva) e a 12× sem suavização", fill=TEXTO, font=f2)
    y += 20
    for j, (modo, rot) in enumerate(a["modos"]):
        x = 20 + j * 560
        d.text((x, y), rot, fill=TEXTO2, font=f2)
        out.alpha_composite(amplia(abre(f"{animal}-{modo}-palco.png").crop(nic_c), 3), (x, y + 16))
        out.alpha_composite(amplia(abre(f"{animal}-{modo}-pagina.png").crop(nic_p), 3), (x + 124, y + 16))
        im = imagem(a["ids"][modo]) if modo in a["ids"] else lobo_jogo() if modo == "reaproveitado" else None
        if im:
            out.alpha_composite(grade12(im), (x + 250, y + 16))
    y += 16 + 192 + 20
    # 3. a luta inteira (o lobo inimigo integrado do outro lado)
    for modo, rot in a["modos"]:
        luta = abre(f"{animal}-{modo}-palco.png").crop((30, 30, 1060, 210))
        d.text((20, y), f"a luta inteira ({rot}) — tamanho real", fill=TEXTO2, font=f2)
        out.alpha_composite(luta, (20, y + 16))
        y += 16 + luta.height + 10
    out = out.crop((0, 0, 1800, y + 10))
    nome = "lobo-cinzento" if animal == "lobo" else animal
    out.save(PASTA / f"{nome}.png")
    print(f"{nome}.png", out.size)


def fileira():
    """Os três animais (atual e propostas) junto dos retratos aprovados: o Morel, a Odette, o herói e o Lobo e o Bandido
    inimigos da 1.163.0, na caixa da carta, em tamanho real e a 3×."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    luta = abre("lobo-atual-palco.png")
    aprovados = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272))),
                 ("o herói", luta.crop((46, 54, 84, 92))), ("Lobo (inimigo)", luta.crop((836, 45, 874, 83))),
                 ("Bandido (inimigo)", luta.crop((836, 103, 874, 141)))]
    animais = []
    for animal, a in ANIMAIS.items():
        nic = caixa_dif(animal, "palco", CARTA, a["modos"][1][0])
        animais += [(f"{a['titulo'].split()[0]}: {rot}", abre(f"{animal}-{modo}-palco.png").crop(nic)) for modo, rot in a["modos"]]
    out = Image.new("RGBA", (1800, 600), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Os animais do patrulheiro junto dos retratos aprovados, na caixa da carta (as fotos a 1920×945) — "
                     "tamanho real e 3×", fill=TEXTO, font=f)
    y = 40
    for linha in (aprovados, animais):
        for j, (rot, cx) in enumerate(linha):
            out.alpha_composite(cx, (20 + j * 46, y))
        y += 50
        for j, (rot, cx) in enumerate(linha):
            out.alpha_composite(amplia(cx, 3), (20 + j * 136, y))
            d.text((20 + j * 136, y + 118), rot[:22], fill=TEXTO2, font=f2)
        y += 3 * 38 + 36
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "animais.png")
    print("animais.png", out.size)


REFS = {"urso": "Retrato pixelado de urso pardo severo-1.png", "falcao": "Falcão-peregrino com máscara ocular em pixel art-2.png"}


def folha_transposicao():
    """A transposição das duas referências geradas (transposicao.png): por animal, a referência, a proposta A anterior ×
    a transposição (t) na carta aliada e no painel da comitiva a 1920×945 (tamanho real e 2×), a caixa a 3×, a 12× com a
    guia; e a fileira com os retratos aprovados."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1800, 2000), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Urso e Falcão: a transposição das referências geradas (t) × a proposta A anterior — 16×16 a 2× na carta "
                     "aliada e no painel; proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    for animal in ("urso", "falcao"):
        a = ANIMAIS[animal]
        ref = Image.open(RAIZ / "ferramentas/arte/referencias/icones" / REFS[animal]).convert("RGBA")
        fundo = Image.new("RGBA", ref.size, CARVAO); fundo.alpha_composite(ref)
        d.text((20, y), f"{a['titulo']}: a referência (reduzida, só para olhar) | a guia a 16 | A anterior × t: 1×, a carta "
                        "(2×), a 12×", fill=TEXTO, font=f2)
        out.alpha_composite(fundo.resize((192, 192), Image.LANCZOS), (20, y + 18))
        guia = Image.open(PASTA / f"guias/{animal}-t-guia-16.png").convert("RGBA")
        g = Image.new("RGBA", (192, 192), CARVAO); g.alpha_composite(amplia(guia, 12)); out.alpha_composite(g, (222, y + 18))
        for j, ident in enumerate((f"{animal}-a", f"{animal}-t")):
            x = 440 + j * 300
            im = imagem(ident)
            cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
            cx.alpha_composite(amplia(im, 2), (3, 3))
            d.text((x, y + 18), "A anterior" if j == 0 else "t, a transposição", fill=TEXTO2, font=f2)
            out.alpha_composite(im, (x, y + 36)); out.alpha_composite(cx, (x + 24, y + 36))
            out.alpha_composite(grade12(im), (x + 70, y + 36))
        y += 18 + 192 + 26
        nic_c, nic_p = caixa_dif(animal, "palco", CARTA, "a"), caixa_dif(animal, "pagina", PAINEL, "a")
        for j, (modo, rot) in enumerate((("atual", a["modos"][0][1]), ("a", "A anterior"), ("t", "t, a transposição"))):
            x = 20 + j * 590
            carta, painel = abre(f"{animal}-{modo}-palco.png").crop(CARTA), abre(f"{animal}-{modo}-pagina.png").crop(PAINEL)
            d.text((x, y), f"{rot} — a carta aliada e o painel da comitiva (1920×945): tamanho real, 2× e a caixa a 3×",
                   fill=TEXTO2, font=f2)
            out.alpha_composite(carta, (x, y + 16)); out.alpha_composite(painel, (x + carta.width + 12, y + 16))
            out.alpha_composite(amplia(carta, 2), (x, y + 16 + 62))
            out.alpha_composite(amplia(abre(f"{animal}-{modo}-palco.png").crop(nic_c), 3), (x, y + 16 + 62 + 112))
            out.alpha_composite(amplia(abre(f"{animal}-{modo}-pagina.png").crop(nic_p), 3), (x + 124, y + 16 + 62 + 112))
        y += 16 + 62 + 112 + 114 + 24
    # a fileira com os retratos aprovados
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    luta = abre("lobo-atual-palco.png")
    caixas = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272))),
              ("o herói", luta.crop((46, 54, 84, 92))), ("Lobo (inimigo)", luta.crop((836, 45, 874, 83))),
              ("Bandido (inimigo)", luta.crop((836, 103, 874, 141))),
              ("Lobo Cinzento (fera)", luta.crop(caixa_dif("lobo", "palco", CARTA, "reaproveitado")))] + \
        [(f"{ANIMAIS[an]['titulo'].split()[0]}: t", abre(f"{an}-t-palco.png").crop(caixa_dif(an, "palco", CARTA, "a")))
         for an in ("urso", "falcao")]
    d.text((20, y), "a fileira, na caixa da carta, com os retratos aprovados — tamanho real e 3×", fill=TEXTO, font=f2)
    y += 20
    for j, (rot, cx) in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(caixas):
        out.alpha_composite(amplia(cx, 3), (20 + j * 136, y))
        d.text((20 + j * 136, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 36
    out = out.crop((0, 0, 1800, y))
    out.save(PASTA / "transposicao.png")
    print("transposicao.png", out.size)


def folha_ajuste():
    """O último ajuste (ajuste.png): antes (t) × depois (t2) na caixa da carta em tamanho real e a 3×, junto dos retratos
    aprovados, e a 12× com os pixels mudados marcados."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)

    def caixa(im):
        cx = Image.new("RGBA", (38, 38), (42, 36, 32, 255)); cx.paste((13, 11, 10, 255), (2, 2, 36, 36))
        cx.alpha_composite(amplia(im, 2), (3, 3))
        return cx
    ali = Image.open(PASTA.parent / "capturas/aliados-palco.png").convert("RGBA")
    luta = abre("lobo-atual-palco.png")
    caixas = [("Morel", ali.crop((46, 176, 84, 214))), ("Odette", ali.crop((46, 234, 84, 272))),
              ("o herói", luta.crop((46, 54, 84, 92))), ("Lobo", luta.crop((836, 45, 874, 83))),
              ("Bandido", luta.crop((836, 103, 874, 141)))] + \
        [(rot, caixa(imagem(i))) for i, rot in (("urso-t", "Urso antes"), ("urso-t2", "Urso depois"),
                                               ("falcao-t", "Falcão antes"), ("falcao-t2", "Falcão depois"))]
    out = Image.new("RGBA", (1400, 700), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O último ajuste: antes (t, cf859322) × depois (t2) — a caixa da carta em tamanho real e a 3×, com os "
                     "retratos aprovados; a 12× com os pixels mudados", fill=TEXTO, font=f)
    y = 40
    for j, (_, cx) in enumerate(caixas):
        out.alpha_composite(cx, (20 + j * 46, y))
    y += 50
    for j, (rot, cx) in enumerate(caixas):
        out.alpha_composite(amplia(cx, 3), (20 + j * 124, y))
        d.text((20 + j * 124, y + 118), rot, fill=TEXTO2, font=f2)
    y += 3 * 38 + 36
    for j, (a, b, rot) in enumerate((("urso-t", "urso-t2", "Urso: o queixo e os cantos da boca"),
                                     ("falcao-t", "falcao-t2", "Falcão: o canto de trás do olho"))):
        x = 20 + j * 680
        ia, ib = imagem(a), imagem(b)
        d.text((x, y), rot, fill=TEXTO, font=f2)
        for k, im in enumerate((ia, ib)):
            g = grade12(im)
            if k:
                dd = ImageDraw.Draw(g)
                for py in range(16):
                    for px in range(16):
                        if ia.getpixel((px, py)) != ib.getpixel((px, py)):
                            dd.rectangle([px * 12, py * 12, px * 12 + 11, py * 12 + 11], outline=(230, 40, 40, 255))
            out.alpha_composite(g, (x + k * 210, y + 18))
        y2 = y + 18 + 192
    out = out.crop((0, 0, 1400, y2 + 16))
    out.save(PASTA / "ajuste.png")
    print("ajuste.png", out.size)


def folha_final():
    """A integração (1.164.0, final.png): os PNGs do jogo × os aprovados (t2); a carta aliada e o painel da comitiva com os
    arquivos de produção (o modo "final", sem troca); o Lobo Cinzento, a aranha e as harpias que continuam no desenho de
    sempre."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    jogo = RAIZ / "rpg/web/static/hud/icones"
    out = Image.new("RGBA", (1500, 1200), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Urso Pardo e o Falcão Peregrino no jogo (1.164.0): o urso-t2 e o falcao-t2, sem retoques", fill=TEXTO, font=f)
    y = 40
    for j, (tipo, aprovado) in enumerate((("urso", "urso-t2"), ("falcao", "falcao-t2"))):
        a, b = imagem(aprovado), Image.open(jogo / f"retrato-{tipo}-16.png").convert("RGBA")
        d.text((20 + j * 470, y), f"{aprovado} (aprovado) | retrato-{tipo}-16 (no jogo): "
               f"{'idênticos' if a.tobytes() == b.tobytes() else 'DIFERENTES'}", fill=TEXTO2, font=f2)
        out.alpha_composite(grade12(a), (20 + j * 470, y + 18)); out.alpha_composite(grade12(b), (230 + j * 470, y + 18))
    y += 18 + 192 + 20
    for animal, rot in (("urso", "Urso Pardo"), ("falcao", "Falcão Peregrino"), ("lobo", "Lobo Cinzento (continua no fera)")):
        carta, painel = abre(f"{animal}-final-palco.png").crop(CARTA), abre(f"{animal}-final-pagina.png").crop(PAINEL)
        d.text((20, y), f"{rot}: a carta aliada e o painel da comitiva (1920×945) — tamanho real e 2×", fill=TEXTO, font=f2)
        out.alpha_composite(carta, (20, y + 18)); out.alpha_composite(painel, (20 + carta.width + 16, y + 18))
        out.alpha_composite(amplia(carta, 2), (540, y + 18)); out.alpha_composite(amplia(painel, 2), (540 + 2 * carta.width + 16, y + 18))
        y += 18 + 2 * carta.height + 18
    luta = abre("voadores-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "o falcão do herói contra duas harpias (o \"voador\" continua) e um lobo (o retrato da 1.163.0) — tamanho real",
           fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    luta = abre("urso-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "o urso do herói contra um lobo, um bandido e uma aranha (o \"fera\" continua) — tamanho real", fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / "final.png")
    print("final.png", out.size)


def folha_lobo_final():
    """O Lobo Cinzento no jogo (1.165.0, lobo-cinzento-final.png): o "fera" de antes × o teste aprovado (a troca na
    página) × o jogo (o arquivo do Lobo inimigo, sem troca), na carta aliada e no painel; e a luta contra três lobos."""
    f, f2 = ImageFont.truetype("arial.ttf", 15), ImageFont.truetype("arial.ttf", 12)
    out = Image.new("RGBA", (1500, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "O Lobo Cinzento no jogo (1.165.0): o mesmo arquivo do Lobo inimigo (retrato-lobo), sem redesenho",
           fill=TEXTO, font=f)
    teste_c, final_c = abre("lobo-reaproveitado-palco.png").crop(CARTA), abre("lobo-final-palco.png").crop(CARTA)
    teste_p, final_p = abre("lobo-reaproveitado-pagina.png").crop(PAINEL), abre("lobo-final-pagina.png").crop(PAINEL)
    igual = teste_c.tobytes() == final_c.tobytes() and teste_p.tobytes() == final_p.tobytes()
    d.text((20, 30), f"o jogo × o teste aprovado (a carta e o painel): {'iguais pixel a pixel' if igual else 'diferentes'}",
           fill=TEXTO2, font=f2)
    y = 56
    for rot, c, p in (("antes (o fera)", abre("lobo-atual-palco.png").crop(CARTA), abre("lobo-atual-pagina.png").crop(PAINEL)),
                      ("no jogo (1.165.0)", final_c, final_p)):
        d.text((20, y), f"{rot}: a carta aliada e o painel da comitiva — tamanho real e 2×", fill=TEXTO, font=f2)
        out.alpha_composite(c, (20, y + 18)); out.alpha_composite(p, (20 + c.width + 16, y + 18))
        out.alpha_composite(amplia(c, 2), (540, y + 18)); out.alpha_composite(amplia(p, 2), (540 + 2 * c.width + 16, y + 18))
        y += 18 + 2 * c.height + 18
    luta = abre("lobos-final-palco.png").crop((30, 30, 1060, 210))
    d.text((20, y), "o Lobo Cinzento contra três lobos: o mesmo rosto de propósito; o lado, o nome e a borda separam os papéis",
           fill=TEXTO, font=f2)
    out.alpha_composite(luta, (20, y + 18))
    y += 18 + luta.height + 16
    out = out.crop((0, 0, 1500, y))
    out.save(PASTA / "lobo-cinzento-final.png")
    print("lobo-cinzento-final.png", out.size, "igual ao teste" if igual else "DIFERENTE do teste")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["lobo"]:
        folha_lobo_final()
    elif sys.argv[1:] == ["final"]:
        folha_final()
    elif sys.argv[1:] == ["ajuste"]:
        folha_ajuste()
    elif sys.argv[1:] == ["t"]:
        folha_transposicao()
    else:
        for animal in ANIMAIS:
            folha(animal)
        fileira()
