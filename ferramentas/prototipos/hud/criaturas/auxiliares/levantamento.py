"""O levantamento visual das criaturas (21/10/2026): inimigos, chefes, animais, invocações e companheiros, pela fonte de
verdade do jogo (rpg/dados.py, rpg/inimigos.py, rpg/classes.py, rpg/missoes.py e a escolha do desenho em batalha.js e
estado.py). Só lê; não muda nada do jogo.

  - levantamento.md: a tabela por entidade (identificador, arte atual, compartilhamentos, contextos, tamanhos, situação,
    atenção) e as contagens (entidades × desenhos únicos);
  - folhas: tracos.png (os desenhos únicos de criatura e quem usa cada um), compartilhamentos.png (os casos que mais
    pesam) e referencias.png (o que já foi aprovado e serve de estilo).
    python levantamento.py
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[4]
STATIC = RAIZ / "rpg/web/static"
sys.path.insert(0, str(RAIZ))
from rpg import dados  # noqa: E402
from rpg.classes import COMPANHEIROS  # noqa: E402

CARVAO, TEXTO, TEXTO2, AVISO = (13, 11, 10, 255), (210, 210, 214, 255), (140, 140, 148, 255), (230, 150, 90, 255)


def fonte(t=13):
    try:
        return ImageFont.truetype("arial.ttf", t)
    except OSError:
        return ImageFont.load_default()


def _grade(nome, texto):
    m = re.search(rf"\n    {nome}: \[(.*?)\]", texto, re.S) or re.search(rf"\n  S\.{nome} = \[(.*?)\]", texto, re.S)
    if m:
        return re.findall(r'"([^"]+)"', m.group(1))
    m = re.search(rf"S\.{nome} = trocar\(S\.(\w+), \{{(.*?)\}}\)", texto)
    troca = dict(re.findall(r'(\w): "(\w)"', m.group(2)))
    return ["".join(troca.get(c, c) for c in l) for l in _grade(m.group(1), texto)]


def sprite(nome):
    pal = dict(re.findall(r'(\w): "#([0-9a-f]{6})"', re.search(r"const PALETA = \{(.*?)\};",
                          (STATIC / "sprites.js").read_text(encoding="utf-8"), re.S).group(1)))
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(_grade(nome, (STATIC / "sprites-dados.js").read_text(encoding="utf-8"))):
        for x, c in enumerate(l):
            if c in pal:
                im.putpixel((x, y), tuple(int(pal[c][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def amplia(im, z):
    return im.resize((im.width * z, im.height * z), Image.NEAREST)


# --------------------------------------------------------------------------- as entidades e o desenho de cada uma
CONTEXTO_INIMIGO = "carta da luta; ficha (traços); Bestiário; mural e rastreador de contratos; faixa de mestre caçador"
TAM_INIMIGO = "16×16; carta 2× (32 px), Bestiário e mural 3× (48), rastreador 2× (32), faixa 3× (48)"


def entidades():
    """[(grupo, entidade, id, sprite, contextos, tamanhos, situação, atenção)]"""
    linhas = []
    vale = {"pantano", "floresta", "ruinas", "planicie"}   # os biomas dos lugares do Vale do Turvo (campanha.py)
    for k, f in dados.FAMILIAS.items():
        s = dados.retrato(f["tracos"])
        biomas = [b for b, v in dados.BIOMAS.items() if k in v["familias"] or k in v.get("noite", [])]
        aten = []
        if not any(t in dados.RETRATOS for t in f["tracos"]):
            aten.append(f"nenhum traço com retrato ({', '.join(f['tracos'])}): cai na caveira")
        if k == "esqueleto_servo":
            aten.append("não aparece como inimigo (o servo do talento); fora do Bestiário")
        grupo = "inimigo comum" + (" (Vale)" if set(biomas) & vale else "")
        linhas.append((grupo, f["nome"], k, s, CONTEXTO_INIMIGO, TAM_INIMIGO, "sem desenho próprio (o retrato do traço)",
                       "; ".join(aten) or f"traços {', '.join(f['tracos'])}"))
    for bioma, lista in dados.GUARDIOES.items():
        for g in lista:
            s = dados.retrato(g["tracos"])
            fases = [t for fa in g.get("fases", []) for t in fa.get("tracos", [])]
            aten = [f"traços {', '.join(g['tracos'])}"]
            if fases:
                aten.append(f"na fase 2 ganha {', '.join(fases)}: a carta troca para {dados.retrato(g['tracos'] + fases)}")
            if not any(t in dados.RETRATOS for t in g["tracos"]):
                aten.append("cai na caveira")
            linhas.append(("chefe (guardião)", g["base"], g["id"], s, "carta da luta; ficha (sem Bestiário: não é família)",
                           "16×16; carta 2× (32 px)", "sem desenho próprio (o retrato do traço)", "; ".join(aten)))
    linhas.append(("chefe (campanha)", "Ilse, a Bruxa Afogada (guardiã da Capela)", "bruxa_afogada (missoes.py)",
                   dados.retrato(["morto-vivo", "conjurador"]), "carta da luta; a cena do fundo da capela (cenas.js, ilseDesenho)",
                   "carta 16×16 a 2× (32 px); a cena: figura em código na arte do lugar",
                   "a cena: arte integrada (1.84.0); a carta: sem desenho próprio",
                   "na luta ela é a caveira genérica, a mesma do esqueleto e do afogado"))
    linhas.append(("inimigo (campanha)", "os dois de capa escura da Sacristia", "cultista + figura (missoes.FIGURAS_SACRISTIA)",
                   dados.retrato(dados.FAMILIAS["cultista"]["tracos"]),
                   "carta da luta; a cena da sacristia (cenas.js, vulto)", "carta 2× (32 px); a cena: vultos em código",
                   "a cena: arte integrada (1.83.0); a carta: sem desenho próprio", "a carta é o humano genérico (o bandido)"))
    linhas.append(("chefe (antagonista)", "o antagonista do mundo gerado (8 nomes)", "ANTAGONISTAS (inimigos.instanciar_antagonista)",
                   dados.retrato(["conjurador"]), "carta da luta", "carta 2× (32 px)", "sem desenho próprio",
                   "conjurador → o humano genérico; a campanha ainda não tem antagonista"))
    for k, c in COMPANHEIROS.items():
        s = "voador" if k == "falcao" else "fera"
        linhas.append(("animal aliado", c["nome"], f"companheiro {k}", s, "carta da luta; painel da Comitiva",
                       "16×16; carta e painel 2× (32 px)", "sem desenho próprio",
                       "o mesmo desenho dos inimigos com o traço" + (" (o urso e o lobo iguais aos lobos inimigos)" if s == "fera" else "")))
    linhas.append(("invocação aliada", "Esqueleto (Invocado) do Erguer Servo", "tipo servo (habilidades.py)", "caveira",
                   "carta da luta", "carta 2× (32 px)", "sem desenho próprio", "a caveira dos inimigos mortos-vivos"))
    linhas.append(("invocação aliada", "o inimigo que se ergue como servo (talento)", "tipo servo (talentos.py)", "caveira",
                   "carta da luta", "carta 2× (32 px)", "sem desenho próprio", "qualquer criatura (um lobo) vira a caveira"))
    for nome, inv in (("filhotes da Rainha Aracnídea", "aranha"), ("mãos da Bruxa Afogada", "afogado"),
                      ("bandidos do Senhor da Guerra", "bandido"), ("fiéis do Profeta", "cultista"),
                      ("esqueletos do Lich", "esqueleto"), ("crias do antagonista", "cria_vazio")):
        linhas.append(("invocação inimiga", nome, inv, dados.retrato(dados.FAMILIAS[inv]["tracos"]), "carta da luta",
                       "carta 2× (32 px)", "o desenho da família", "nenhuma diferença visual de invocado"))
    for nome, cid in (("Bastian Morel", "morel"), ("Irmã Odette", "odete"), ("Yara", "yara")):
        linhas.append(("companheiro", nome, cid, f"retratos.js {cid}", "carta; painel; topo; cartões; fogueira; ficha",
                       "busto 40×40 (Morel 80×80) a 2×, carta 16×16 a 2× (32 px), cabeça recortada",
                       "aprovado (1.92.0, 7560ce7c)", "preservar; não refazer por extensão"))
    for cls in ("guerreiro", "mago", "arqueiro"):
        linhas.append(("herói", cls.capitalize(), cls, f"retratos.js {cls}", "ficha; topo; carta da luta; fogueira",
                       "busto 40×40 a 2×, carta 16×16 a 2× (32 px)", "aprovado (1.91.0; o guerreiro antes)",
                       "preservar; referência de estilo do retrato"))
    return linhas


def tabela_md(linhas):
    uso = {}
    for l in linhas:
        if not l[3].startswith("retratos.js"):
            uso.setdefault(l[3], []).append(l[1])
    out = ["| Grupo | Entidade | Identificador | Arte atual | Compartilha com | Contextos | Tamanhos | Situação | Atenção |",
           "|---|---|---|---|---|---|---|---|---|"]
    for g, nome, ident, s, ctx, tam, sit, aten in linhas:
        arte = s if s.startswith("retratos.js") else f"sprite `{s}` (sprites-dados.js, 16×16)"
        outros = [n for n in uso.get(s, []) if n != nome]
        comp = f"{len(outros)} outras: " + ", ".join(outros[:6]) + ("…" if len(outros) > 6 else "") if outros else "—"
        out.append(f"| {g} | {nome} | `{ident}` | {arte} | {comp} | {ctx} | {tam} | {sit} | {aten} |")
    return "\n".join(out), uso


# --------------------------------------------------------------------------- as folhas
def folha_tracos(uso):
    f, f2 = fonte(15), fonte(12)
    ordem = sorted(uso, key=lambda s: -len(uso[s]))
    out = Image.new("RGBA", (1700, 120 + 230 * len(ordem)), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 12), f"Os desenhos de criatura hoje: {len(ordem)} sprites de 16×16 para "
                     f"{sum(len(v) for v in uso.values())} entidades (o retrato pelo traço, dados.retrato). Tamanho real "
                     "nos contextos (1×, 2× da carta, 3× do Bestiário e do mural) e 10× sem suavização.", fill=TEXTO, font=f)
    y = 50
    for s in ordem:
        im = sprite(s)
        d.text((20, y), f"`{s}` — {len(uso[s])} entidades", fill=TEXTO, font=f)
        out.alpha_composite(im, (20, y + 30))
        out.alpha_composite(amplia(im, 2), (50, y + 30))
        out.alpha_composite(amplia(im, 3), (100, y + 30))
        out.alpha_composite(amplia(im, 10), (170, y + 26))
        texto = ", ".join(uso[s])
        linhas, linha = [], ""
        for palavra in texto.split(", "):
            if len(linha) + len(palavra) > 120:
                linhas.append(linha); linha = ""
            linha += (", " if linha else "") + palavra
        linhas.append(linha)
        for i, l in enumerate(linhas):
            d.text((350, y + 34 + i * 18), l, fill=TEXTO2, font=f2)
        y += 230
    out.save(PASTA / "tracos.png")


def folha_compartilhamentos():
    f, f2 = fonte(15), fonte(12)
    cap = PASTA / "capturas"
    casos = [("O mesmo rosto de lobo: o Lobo inimigo, o Urso Pardo do herói e a Aranha gigante",
              [("aliados-palco.png", (36, 120, 260, 345), "urso (aliado) e lobo (inimigo, à direita)"),
               ("aliados-palco.png", (826, 160, 1045, 215), ""),
               ("bestiario-pagina.png", (945, 250, 1295, 400), "aranha gigante no Bestiário")]),
             ("A caveira: esqueleto, afogado, troll (sem traço com retrato), Ilse, o Lich, o servo invocado",
              [("luta-mista-a-palco.png", (830, 150, 1045, 205), "esqueleto"),
               ("luta-mista-b-palco.png", (610, 30, 1045, 210), "a segunda luta mista (troll, afogado...)"),
               ("aliados-palco.png", (46, 292, 260, 348), "o servo do Necromante")]),
             ("A Ilse: a arte da cena (aprovada) e a carta dela na luta (a caveira genérica)",
              [("capela-fundo-pagina.png", (780, 140, 1160, 300), "a cena do fundo da capela")])]
    imgs = []
    for titulo, recortes in casos:
        imgs.append(("t", titulo))
        for arq, caixa, rot in recortes:
            p = cap / arq
            if p.exists():
                imgs.append(("i", Image.open(p).convert("RGBA").crop(caixa), rot))
    altura = 30 + sum(40 if k[0] == "t" else k[1].height + 30 for k in imgs)
    out = Image.new("RGBA", (1600, altura), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 8), "Compartilhamentos que mais pesam (capturas a 1920×945, tamanho real)", fill=TEXTO, font=f)
    y = 40
    for k in imgs:
        if k[0] == "t":
            y += 10
            d.text((20, y), k[1], fill=AVISO, font=f)
            y += 30
            continue
        im, rot = k[1], k[2]
        out.alpha_composite(im, (20, y))
        if rot:
            d.text((40 + im.width, y + 4), rot, fill=TEXTO2, font=f2)
        y += im.height + 30
    out.save(PASTA / "compartilhamentos.png")


def folha_referencias():
    f, f2 = fonte(15), fonte(12)
    cap = PASTA / "capturas"
    out = Image.new("RGBA", (1700, 900), CARVAO)
    d = ImageDraw.Draw(out)
    d.text((20, 8), "Referências aprovadas para o estilo das criaturas", fill=TEXTO, font=f)
    y = 40
    ali = Image.open(cap / "aliados-palco.png").convert("RGBA")
    d.text((20, y), "os retratos de carta aprovados (herói e comitiva: 16×16 a 2×, 1.91.0 e 1.92.0), em tamanho real e 2×",
           fill=TEXTO2, font=f2)
    corte = ali.crop((36, 26, 270, 290))
    out.alpha_composite(corte, (20, y + 20)); out.alpha_composite(amplia(corte, 2), (280, y + 20))
    y += 20 + 2 * corte.height + 20
    cena = Image.open(cap / "capela-fundo-pagina.png").convert("RGBA").crop((780, 140, 1160, 300))
    sac = Image.open(cap / "sacristia-pagina.png").convert("RGBA").crop((410, 140, 1470, 370))
    d.text((20, y), "as cenas aprovadas, desenho em código: a Ilse no fundo da capela (1.84.0) e a sacristia (1.83.0; os vultos "
                    "só aparecem na entrada e na luta, não nesta visita)",
           fill=TEXTO2, font=f2)
    out.alpha_composite(cena, (20, y + 20)); out.alpha_composite(sac.resize((sac.width * 3 // 4, sac.height * 3 // 4)), (420, y + 20))
    y += 20 + max(cena.height, sac.height * 3 // 4) + 20
    icones = STATIC / "hud/icones"
    est = [Image.open(icones / f"estado-{k}-16.png").convert("RGBA") for k in
           ("firme", "guarda", "esquiva", "sangramento", "maldito", "marcado", "furtivo", "furia", "queimadura", "fortalecido",
            "enfraquecido", "frenesi", "veneno", "atordoado", "barreira", "provocando", "iniciativa")]
    beste = Image.open(icones / "atalho-bestiario-32.png").convert("RGBA")
    d.text((20, y), "os ícones aprovados de 16 (os 17 estados) e o Bestiário da doca (32), o acabamento do contorno e da luz",
           fill=TEXTO2, font=f2)
    for j, im in enumerate(est):
        out.alpha_composite(amplia(im, 2), (20 + j * 40, y + 24))
    out.alpha_composite(amplia(beste, 2), (20 + len(est) * 40 + 20, y + 10))
    y += 100
    out = out.crop((0, 0, 1700, y))
    out.save(PASTA / "referencias.png")


if __name__ == "__main__":
    linhas = entidades()
    md, uso = tabela_md(linhas)
    inimigas = [l for l in linhas if not l[3].startswith("retratos.js")]
    contagem = (f"- Entidades levantadas: **{len(linhas)}** ({len(inimigas)} com desenho de criatura; "
                f"{len(linhas) - len(inimigas)} heróis e companheiros com retrato aprovado).\n"
                f"- Desenhos únicos de criatura na carta: **{len(uso)}** sprites de 16×16 ({', '.join(sorted(uso))}).\n"
                + "".join(f"  - `{s}`: {len(v)}\n" for s, v in sorted(uso.items(), key=lambda kv: -len(kv[1]))))
    (PASTA / "levantamento.md").write_text("# O levantamento das criaturas (gerado por auxiliares/levantamento.py)\n\n"
                                            + contagem + "\n" + md + "\n", encoding="utf-8")
    folha_tracos(uso)
    folha_compartilhamentos()
    folha_referencias()
    print(contagem)
