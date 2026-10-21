"""As folhas do lote da madrugada (21/10/2026). Cada ícone entra pelo nome e pelo arquivo, nunca pela posição.
  python prancha.py lote <n>   -> lote<n>.png:
    - a fileira da carta em chips escuros, tamanho real e 2×: Firme · Em guarda · Esquiva (os finais do jogo) e os dois
      estados do lote, atual (o sprite do jogo) × proposta;
    - atual e proposta a 12× sem suavização, com a grade (só para inspecionar o pixel);
    - as cartas na luta a 1920×945 com os mesmos dados (fotografar.mjs), atual × proposta, em tamanho real e a 2×.
  python prancha.py geral      -> geral.png: os 17 estados identificados (os 3 finais e os 14 candidatos), em tamanho real
    e a 2×, e a comparação dos estados de dano (Fortalecido, Fúria, Frenesi, Iniciativa, com o Enfraquecido ao lado).
"""
import sys

from PIL import Image, ImageDraw

from comum import (ATUAL, CARVAO, FINAIS, LOTE, LOTES, TEXTO, TEXTO2, TITULO, abre, amplia, final, fonte, grade_px,
                   proposta, sprite)

CHIP = (10, 11, 13, 255)
Z = 12


def chip(out, d, im, x, y, borda=(60, 60, 66, 255)):
    d.rectangle([x, y, x + 19, y + 19], fill=CHIP, outline=borda)
    out.alpha_composite(im, (x + 2, y + 2))


def cartas(n):
    """As fotos do lote: [(situação, [(modo, [cartas])])]."""
    pasta = LOTE / f"capturas/lote{n}"
    sits = sorted({p.name.split("-atual-")[0] for p in pasta.glob("*-atual-carta*.png")})
    return [(s, [(m, [abre(p) for p in sorted(pasta.glob(f"{s}-{m}-carta*.png"))]) for m in ("atual", "proposta")])
            for s in sits]


def folha_lote(n):
    ids = LOTES[n]
    fotos = cartas(n)
    f, f2 = fonte(14), fonte(12)
    # medidas
    larg_cartas = max(sum(c.width + 16 for c in cs) for _, ms in fotos for _, cs in ms) if fotos else 0
    alt_fotos = sum(30 + max(c.height for _, cs in ms for c in cs) * 3 + 40 for _, ms in fotos)
    W = max(60 + 2 * (2 * (16 * Z) + 60), 40 + 2 * larg_cartas * 2 + 60, 900)
    H = 80 + 150 + 40 + 16 * Z + 60 + alt_fotos + 40
    out = Image.new("RGBA", (W, H), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), f"Lote {n}: {' e '.join(TITULO[i] for i in ids)} — 16 px (o chip da carta e o selo); "
                     "proposta, nada no jogo", fill=TEXTO, font=f)
    y = 44
    finais = [final(k) for k, _ in FINAIS]
    for k, (rot, lado) in enumerate((("atual", [sprite(ATUAL[i]) for i in ids]),
                                     ("proposta", [proposta(f"estado-{i}") for i in ids]))):
        yy = y + k * 70
        d.text((20, yy + 4), rot, fill=TEXTO, font=f2)
        fila = finais + lado
        for j, im in enumerate(fila):
            chip(out, d, im, 100 + j * 24, yy)
            out.alpha_composite(amplia(im, 2), (260 + j * 40, yy - 6))
        d.text((480, yy + 4), "Firme · Em guarda · Esquiva · " + " · ".join(TITULO[i] for i in ids), fill=TEXTO2, font=f2)
    # as tentativas guardadas do lote (proposta/estado-<id>-<nome>-16.png), fora da proposta principal
    tent = [(p.name[:-7], abre(p)) for i in ids for p in sorted((LOTE / "proposta").glob(f"estado-{i}-*-16.png"))]
    if tent:
        d.text((20, y + 144), "tentativas guardadas (recusadas na bancada):", fill=TEXTO2, font=f2)
        for j, (nome, im) in enumerate(tent):
            chip(out, d, im, 300 + j * 200, y + 140)
            out.alpha_composite(amplia(im, 2), (326 + j * 200, y + 134))
            d.text((364 + j * 200, y + 144), nome.replace("estado-", ""), fill=TEXTO2, font=f2)
        y += 40
    y += 150
    d.text((20, y), "a 12×, só para achar o pixel (o julgamento é no tamanho real)", fill=TEXTO2, font=f2)
    y += 22
    x = 20
    for i in ids:
        for rot, im in (("atual", sprite(ATUAL[i])), ("proposta", proposta(f"estado-{i}"))):
            d.text((x, y), f"{TITULO[i]} ({rot})", fill=TEXTO, font=f2)
            out.alpha_composite(grade_px(im, Z), (x, y + 18))
            x += 16 * Z + 20
    y += 16 * Z + 40
    for sit, ms in fotos:
        h = max(c.height for _, cs in ms for c in cs)
        d.text((20, y), f"{sit}: a carta na luta a 1920×945, os mesmos dados — atual | proposta (tamanho real e 2×)",
               fill=TEXTO, font=f2)
        y += 22
        x = 20
        for m, cs in ms:
            for c in cs:
                out.alpha_composite(c, (x, y)); x += c.width + 16
            x += 30
        y += h + 10
        x = 20
        for m, cs in ms:
            for c in cs:
                out.alpha_composite(amplia(c, 2), (x, y)); x += 2 * c.width + 16
            x += 30
        y += 2 * h + 30
    out = out.crop((0, 0, W, y + 10))
    out.save(LOTE / f"lote{n}.png")
    print(f"lote{n}.png", out.size)


def folha_geral():
    f, f2 = fonte(14), fonte(12)
    grupos = [("finais (no jogo)", [(t, final(k)) for k, t in FINAIS])] + [
        (f"lote {n}", [(TITULO[i], proposta(f"estado-{i}")) for i in ids]) for n, ids in LOTES.items()]
    out = Image.new("RGBA", (1400, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 10), "Os 17 estados: os 3 finais e os 14 candidatos (proposta, nada aprovado). Tamanho real em chips "
                     "e a 2×; a 4× só para inspecionar.", fill=TEXTO, font=f)
    y = 44
    for rot, ims in grupos:
        d.text((20, y + 4), rot, fill=TEXTO2, font=f2)
        x = 150
        for t, im in ims:
            if im is None:
                d.text((x, y + 4), f"{t}: falta", fill=TEXTO2, font=f2); x += 180; continue
            chip(out, d, im, x, y)
            out.alpha_composite(amplia(im, 2), (x + 28, y - 6))
            out.alpha_composite(amplia(im, 4), (x + 68, y - 22))
            d.text((x + 136, y + 4), t, fill=TEXTO, font=f2)
            x += 260
        y += 74
    # a fileira inteira como uma carta mostraria, em tamanho real
    y += 10
    d.text((20, y), "todos lado a lado, tamanho real (em chips) e 2×:", fill=TEXTO2, font=f2)
    y += 22
    todos = [im for _, ims in grupos for _, im in ims if im is not None]
    for j, im in enumerate(todos):
        chip(out, d, im, 20 + j * 24, y)
        out.alpha_composite(amplia(im, 2), (20 + j * 40, y + 30))
    y += 90
    d.text((20, y), "os estados de dano juntos (o que mais pode confundir): tamanho real, 2× e 6×", fill=TEXTO2, font=f2)
    y += 22
    dano = [(k, TITULO[k]) for k in ("fortalecido", "furia", "frenesi", "iniciativa", "enfraquecido")]
    x = 20
    for k, t in dano:
        im = proposta(f"estado-{k}")
        if im is None:
            continue
        chip(out, d, im, x, y)
        out.alpha_composite(amplia(im, 2), (x + 26, y - 6))
        out.alpha_composite(amplia(im, 6), (x, y + 34))
        d.text((x, y + 34 + 96 + 4), t, fill=TEXTO, font=f2)
        x += 150
    y += 34 + 96 + 30
    out = out.crop((0, 0, 1400, y))
    out.save(LOTE / "geral.png")
    print("geral.png", out.size)


if __name__ == "__main__":
    if sys.argv[1] == "lote":
        folha_lote(int(sys.argv[2]))
    else:
        folha_geral()
