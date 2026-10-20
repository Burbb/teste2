# As folhas atual × proposta (as fotos do fotografar.mjs a 1920x945, em tamanho real) e a prancha sobre o carvão de
# cada lote da noite de 19/10/2026 (bandagem_pocao, tonico_antidoto, calca_manto) e do par seguinte (anel_amuleto).
# Uso (na raiz): python <esta pasta>/montar.py <lote>
import pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
LOTE = pathlib.Path(__file__).resolve().parents[1].parent      # itens-lote-noite/
RAIZ = LOTE.parents[3]
JOGO = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
try:
    FONTE = ImageFont.truetype("arial.ttf", 13)
except OSError:
    FONTE = ImageFont.load_default()

def folha(pasta, linhas, saida, modos=("atual", "proposta")):
    """linhas: (rótulo, arquivo sem o prefixo do modo, recorte ou None[, subpasta]). Um modo por coluna."""
    grupos = []
    for rotulo, nome, corte, *sub in linhas:
        ims = [Image.open(pasta / (sub[0] if sub else "") / f"{m}-1920x945-{nome}.png").convert("RGB") for m in modos]
        if corte: ims = [i.crop(corte) for i in ims]
        grupos.append((rotulo, ims))
    w = max(i.width for _, ims in grupos for i in ims)
    h = sum(ims[0].height + 22 for _, ims in grupos)
    o = Image.new("RGB", (len(modos) * (w + 10) + 10, h + 8), (245, 245, 245)); d = ImageDraw.Draw(o); y = 4
    for rotulo, ims in grupos:
        d.text((10, y), f"{rotulo}: {' | '.join(modos)} (1920x945, tamanho real)", fill=(0, 0, 0), font=FONTE); y += 16
        for k, i in enumerate(ims): o.paste(i, (10 + k * (w + 10), y))
        y += ims[0].height + 6
    o.save(saida); print(saida, o.size)

def prancha(arquivos, saida):
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), *map(str, arquivos), "-o", str(saida)], check=True)

LOTES = {
    "bandagem_pocao": dict(
        linhas=[("topo: Poção (24) e Bandagem (24)", "topo", (600, 0, 800, 73)),
                ("a bolsa da ficha e os cartões do mercado (32)", "mercado-0", None), ("", "mercado-1", None), ("", "mercado-2", None), ("", "mercado-3", None),
                ("aviso de uma Poção ganha, numa tela (16)", "aviso-pocao_vida", None),
                ("aviso de uma Bandagem ganha (16)", "aviso-bandagem", None),
                ("chips no texto (16)", "chips", None),
                ("bolsa do Inventário (32)", "inventario", (460, 600, 660, 680)),
                ("roda da luta: o comando Itens é a Poção (32)", "luta", (260, 20, 460, 215))],
        prancha=lambda P: [P / "bandagem-16.png", P / "bandagem-24.png", P / "bandagem-32.png", JOGO / "bandagem-32.png",
                           P / "pocao-16.png", P / "pocao-24.png", P / "pocao-32.png", JOGO / "pocao-32.png"]),
    "tonico_antidoto": dict(
        linhas=[("cartões do mercado (32)", "mercado-0", None), ("", "mercado-1", None),
                ("espólio com os dois achados (32)", "espolio", None),
                ("aviso de um Tônico ganho (16)", "aviso-tonico", None), ("aviso de um Antídoto ganho (16)", "aviso-antidoto", None),
                ("chips no texto (16)", "chips", None)],
        prancha=lambda P: [P / "tonico-16.png", P / "tonico-32.png", JOGO / "tonico-32.png",
                           P / "antidoto-16.png", P / "antidoto-32.png", JOGO / "antidoto-32.png",
                           LOTE / "bandagem_pocao" / "proposta" / "pocao-32.png"]),
    "calca_manto": dict(
        linhas=[("a ficha do Mago: o equipado (32; o capuz e a luva de seda aprovados ao lado)", "ficha", (18, 362, 272, 472)),
                ("o corpo no Inventário (40)", "inventario", (150, 140, 480, 520)),
                ("o cartão do saque do Manto (64) e o que você usa (48)", "saque", None),
                ("o cartão do saque da Calça de Viagem (64 e 48)", "saque", None, "saque_calca")],
        prancha=lambda P: [P / "calca_tecido-32.png", P / "calca_tecido-40.png", P / "calca_tecido-48.png", P / "calca_tecido-64.png",
                           JOGO / "calca_couro-32.png",
                           P / "manto-32.png", P / "manto-40.png", P / "manto-48.png", P / "manto-64.png",
                           JOGO / "capuz_tecido-32.png", JOGO / "luva_seda-32.png"]),
    "anel_amuleto": dict(                                    # rodada 3 do anel (o amuleto da rodada 2, aprovado, igual)
        linhas=[("a ficha do Mago: um anel vestido, o outro vazio (32)", "ficha", (18, 362, 272, 472)),
                ("o corpo no Inventário (40; o Anel 1 vazio é a silhueta apagada)", "inventario", (150, 140, 480, 520)),
                ("o cartão do saque do anel (64) e o que você usa (48)", "saque", None)],
        modos=("atual", "rodada2", "rodada3"),                 # a produção, a rodada 2 e a rodada 3 do anel
        prancha=lambda P: [JOGO / "anel-32.png", P.parent / "rodada2" / "proposta" / "anel-32.png",
                           P / "anel-32.png", P / "anel-40.png", P / "anel-48.png", P / "anel-64.png",
                           P.parent / "rodada3_liso" / "anel-liso-32.png", P / "amuleto-32.png"]),
    "sandalia_chapeu": dict(                                 # o par do Mago: a prancha junto das peças de tecido aprovadas
        linhas=[("a ficha do Mago: o Chapéu Pontudo e a Sandália vestidos, com o manto, a calça e a luva de seda (32)", "ficha", (18, 362, 272, 472)),
                ("o corpo no Inventário (40)", "inventario", (150, 140, 480, 520)),
                ("o cartão do saque da Sandália (64) e o que você usa (48)", "saque", None),
                ("o cartão do saque do Chapéu Pontudo (64 e 48)", "saque", None, "saque_chapeu")],
        prancha=lambda P: [P / "chapeu-32.png", JOGO / "capuz_tecido-32.png", JOGO / "luva_seda-32.png", JOGO / "manto-32.png",
                           JOGO / "calca_tecido-32.png", P / "sandalia-32.png", JOGO / "bota-32.png",
                           P / "chapeu-40.png", P / "chapeu-48.png", P / "chapeu-64.png",
                           P / "sandalia-40.png", P / "sandalia-48.png", P / "sandalia-64.png"]),
}

def antidoto_base():
    """O Antídoto com a base plana: antes × depois no jogo (tamanho real) e ampliado (a prancha)."""
    base = LOTE / "tonico_antidoto"
    folha(base / "capturas" / "base", [("o cartão do mercado (32)", "mercado-0", None), ("o espólio (32)", "espolio", None),
                                       ("o aviso (16)", "aviso-antidoto", None), ("o chip (16)", "chips", None)],
          base / "antidoto-base-antes-depois.png", ("antes", "depois"))
    antes = base / "recusados" / "antidoto-base-redonda"
    prancha([antes / "antidoto-16.png", base / "proposta" / "antidoto-16.png", antes / "antidoto-32.png", base / "proposta" / "antidoto-32.png"],
            base / "antidoto-base-prancha.png")

def frasco_vazio():
    """O frasco vazio no topo: cheia (o jogo), vazia hoje (o sprite) e vazia proposta."""
    v = LOTE / "bandagem_pocao" / "variantes"
    (v / "capturas" / "vazia" / "cheia-1920x945-topo.png").write_bytes((v / "capturas" / "cheia" / "atual-1920x945-topo.png").read_bytes())
    folha(v / "capturas" / "vazia", [("o topo: com poções | sem poções hoje (o sprite em 32) | sem poções, a proposta (24)", "topo", (440, 0, 800, 73))],
          v / "frasco-cheia-vazia.png", ("cheia", "atual", "proposta"))
    prancha([LOTE / "bandagem_pocao" / "proposta" / "pocao-24.png", v / "proposta" / "frasco_vazio-24.png"], v / "prancha-carvao.png")

def anel_referencia():
    """O anel: a referência principal (sample (2).png) × a rodada 2 × a rodada 3, ampliados 8x e em tamanho real."""
    base = LOTE / "anel_amuleto"
    def sobre(p):
        im = Image.open(p).convert("RGBA"); bg = Image.new("RGBA", im.size, (30, 30, 36, 255)); bg.alpha_composite(im); return bg.convert("RGB")
    ims = [("referência (sample (2).png)", sobre(RAIZ / "ferramentas/arte/referencias/aneis/sample (2).png")),
           ("rodada 2", sobre(base / "rodada2" / "proposta" / "anel-32.png")), ("rodada 3", sobre(base / "proposta" / "anel-32.png"))]
    o = Image.new("RGB", (3 * 266 + 10, 256 + 80), (245, 245, 245)); d = ImageDraw.Draw(o)
    for k, (rot, im) in enumerate(ims):
        o.paste(im.resize((256, 256), Image.NEAREST), (10 + k * 266, 22)); d.text((10 + k * 266, 4), rot, fill=(0, 0, 0), font=FONTE)
        o.paste(im if im.size[0] == 32 else im.resize((32, 32), Image.NEAREST), (10 + k * 266 + 112, 290))
    o.save(base / "anel-referencia-r2-r3.png"); print(base / "anel-referencia-r2-r3.png")

def conjunto_mago():
    """O conjunto de tecido do Mago lado a lado, em 32: em tamanho real (num nicho de 40 sobre o carvão) e a 3× (vizinho
    mais próximo): o Chapéu Pontudo (no jogo desde a 1.141.0), as peças aprovadas e as duas rodadas da Sandália."""
    base = LOTE / "sandalia_chapeu"
    pecas = [("chapéu (no jogo)", JOGO / "chapeu-32.png"), ("capuz", JOGO / "capuz_tecido-32.png"),
             ("manto", JOGO / "manto-32.png"), ("luva de seda", JOGO / "luva_seda-32.png"),
             ("calça de viagem", JOGO / "calca_tecido-32.png"), ("sandália, rodada 1", base / "rodada1" / "proposta" / "sandalia-32.png"),
             ("sandália, rodada 2", base / "rodada2" / "proposta" / "sandalia-32.png")]
    o = Image.new("RGB", (10 + len(pecas) * 110, 202), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real (32 px num nicho de 40 sobre o carvão) e a 3x", fill=(0, 0, 0), font=FONTE)
    for k, (rotulo, arq) in enumerate(pecas):
        im = Image.open(arq).convert("RGBA"); x = 10 + k * 110
        nicho = Image.new("RGBA", (40, 40), (24, 24, 28, 255)); nicho.alpha_composite(im, (4, 4)); o.paste(nicho.convert("RGB"), (x, 24))
        g = Image.new("RGBA", (96, 96), (24, 24, 28, 255)); g.alpha_composite(im.resize((96, 96), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 74))
        d.text((x, 176), rotulo, fill=(0, 0, 0), font=FONTE)
    saida = base / "conjunto-mago-32.png"; o.save(saida); print(saida)

def sandalia_r2():
    """A Sandália: atual (o sprite) × rodada 1 × rodada 2 no jogo (tamanho real), a prancha da rodada 2 e o conjunto."""
    base = LOTE / "sandalia_chapeu"
    folha(base / "capturas" / "r2", [("a ficha do Mago: a Sandália com o chapéu, o manto, a calça e a luva de seda (32)", "ficha", (18, 362, 272, 472)),
                                     ("o corpo no Inventário (40)", "inventario", (150, 140, 480, 520)),
                                     ("o cartão do saque da Sandália (64) e o que você usa (48)", "saque", None)],
          base / "sandalia-r2-no-jogo.png", ("atual", "rodada1", "rodada2"))
    r2 = base / "rodada2"
    prancha([r2 / "proposta" / f"sandalia-{n}.png" for n in (32, 40, 48, 64)] + [r2 / "previa" / "32" / "sandalia_uma_final_32.png",
             base / "rodada1" / "proposta" / "sandalia-32.png", JOGO / "bota-32.png"], r2 / "prancha-carvao.png")
    conjunto_mago()

def fileira(pecas, saida, titulo="tamanho real (32 px num nicho de 40 sobre o carvão) e a 3x"):
    """Uma fileira de peças de 32 lado a lado: em tamanho real (num nicho de 40 sobre o carvão) e a 3×."""
    o = Image.new("RGB", (10 + len(pecas) * 110, 202), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), titulo, fill=(0, 0, 0), font=FONTE)
    for k, (rotulo, arq) in enumerate(pecas):
        im = Image.open(arq).convert("RGBA"); x = 10 + k * 110
        nicho = Image.new("RGBA", (40, 40), (24, 24, 28, 255)); nicho.alpha_composite(im, (4, 4)); o.paste(nicho.convert("RGB"), (x, 24))
        g = Image.new("RGBA", (96, 96), (24, 24, 28, 255)); g.alpha_composite(im.resize((96, 96), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 74))
        d.text((x, 176), rotulo, fill=(0, 0, 0), font=FONTE)
    o.save(saida); print(saida)

def besta_diadema():
    """A Besta Leve e o Diadema: atual × proposta no jogo (tamanho real), as fileiras com as peças vizinhas e a prancha."""
    base = LOTE / "besta_diadema"; P = base / "proposta"
    folha(base / "capturas", [("a ficha do Arqueiro com a Besta Leve na mão (32)", "ficha", (18, 362, 272, 472), "besta"),
                              ("o corpo no Inventário do Arqueiro (40)", "inventario", (150, 140, 480, 520), "besta"),
                              ("o cartão do saque da Besta Leve (64) e o que você usa (48)", "saque", None, "besta"),
                              ("a ficha do Mago com o Diadema (32)", "ficha", (18, 362, 272, 472), "diadema"),
                              ("o corpo no Inventário do Mago (40)", "inventario", (150, 140, 480, 520), "diadema"),
                              ("o cartão do saque do Diadema (64 e 48)", "saque", None, "diadema"),
                              ("o cartão do saque da Coroa dos Afogados (o único, base Diadema; 64 e 48)", "saque", None, "coroa_afogados")],
          base / "besta_diadema-no-jogo.png")
    fileira([("Besta Leve (prop.)", P / "besta-32.png"), ("arco", JOGO / "arco-32.png"), ("aljava", JOGO / "aljava-32.png"),
             ("capuz de couro", JOGO / "capuz-32.png"), ("gibão", JOGO / "gibao-32.png"), ("machado", JOGO / "machado-32.png")],
            base / "fileira-arqueiro-32.png")
    fileira([("Diadema (prop.)", P / "diadema-32.png"), ("Chapéu Pontudo", JOGO / "chapeu-32.png"), ("capuz", JOGO / "capuz_tecido-32.png"),
             ("amuleto", JOGO / "amuleto-32.png"), ("anel", JOGO / "anel-32.png"), ("manto", JOGO / "manto-32.png")],
            base / "fileira-mago-32.png")
    prancha([P / f"besta-{n}.png" for n in (32, 40, 48, 64)] + [P / f"diadema-{n}.png" for n in (32, 40, 48, 64)], base / "prancha-carvao.png")

def diadema_r2():
    """O Diadema, rodada 2: atual (o sprite) × antes (rodada 1) × depois (rodada 2) no jogo, a fileira do Mago e a prancha."""
    base = LOTE / "besta_diadema"; P = base / "proposta"; R1 = base / "diadema_r1" / "proposta"
    folha(base / "capturas", [("a ficha do Mago com o Diadema (32)", "ficha", (18, 362, 272, 472), "diadema"),
                              ("o corpo no Inventário (40)", "inventario", (150, 140, 480, 520), "diadema"),
                              ("o cartão do saque do Diadema (64 e 48)", "saque", None, "diadema"),
                              ("o cartão da Coroa dos Afogados (o mesmo desenho por ora; 64 e 48)", "saque", None, "coroa_afogados")],
          base / "diadema-r2-no-jogo.png", ("atual", "antes", "depois"))
    fileira([("Diadema r2", P / "diadema-32.png"), ("Diadema r1", R1 / "diadema-32.png"),
             ("Chapéu Pontudo", JOGO / "chapeu-32.png"), ("capuz", JOGO / "capuz_tecido-32.png"),
             ("amuleto", JOGO / "amuleto-32.png"), ("anel", JOGO / "anel-32.png"), ("manto", JOGO / "manto-32.png")],
            base / "fileira-mago-32.png")
    prancha([P / f"diadema-{n}.png" for n in (32, 40, 48, 64)] + [R1 / "diadema-32.png"], base / "diadema-prancha-carvao.png")

def espada_maca():
    """A espada e a maça (o começo do remake do ferro): atual × proposta no jogo (tamanho real), a fileira com o machado,
    o escudo e o ícone de Ataque, e a prancha."""
    base = LOTE / "espada_maca"; P = base / "proposta"
    folha(base / "capturas", [("a ficha do Guerreiro com a espada na mão (32)", "ficha", (18, 362, 272, 472), "espada"),
                              ("o corpo no Inventário (40: a proposta só tem o 32 e o 64, e o jogo mostra o 32)", "inventario", (150, 140, 480, 520), "espada"),
                              ("o cartão do saque da espada (64; o 48 do 'você usa' sai do 64 reduzido, sem o 48 próprio)", "saque", None, "espada"),
                              ("a roda da luta: o Atacar do Guerreiro é o desenho da espada (32)", "luta", (250, 10, 470, 225), "espada"),
                              ("a ficha do Guerreiro com a maça (32)", "ficha", (18, 362, 272, 472), "maca"),
                              ("o corpo no Inventário (40, idem)", "inventario", (150, 140, 480, 520), "maca"),
                              ("o cartão do saque da maça (64 e 48, idem)", "saque", None, "maca")],
          base / "espada_maca-no-jogo.png")
    fileira([("espada (prop.)", P / "espada-32.png"), ("maça (prop.)", P / "maca-32.png"), ("machado", JOGO / "machado-32.png"),
             ("escudo", JOGO / "escudo-32.png"), ("Ataque (atributo)", JOGO / "attr-ataque-32.png"),
             ("espada (atual)", JOGO / "espada-32.png"), ("maça (atual)", JOGO / "maca-32.png")],
            base / "fileira-guerreiro-32.png")
    prancha([P / "espada-32.png", P / "espada-64.png", base / "previa" / "espada" / "32" / "espada_silhueta_32.png",
             P / "maca-32.png", P / "maca-64.png", base / "previa" / "maca" / "32" / "maca_silhueta_32.png"], base / "prancha-carvao.png")

def espada_maca_r2():
    """A espada e a maça, rodada 2: a espada contra a referência principal (tamanho real e ampliadas na mesma escala), as
    duas no jogo (atual × rodada 1 × rodada 2) e a fileira com o escudo e o machado."""
    base = LOTE / "espada_maca"; P = base / "proposta"; R1 = base / "rodada1" / "proposta"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/espada/espadasample.png").convert("RGBA").crop((64, 0, 128, 64))
    ims = [("referência (64)", ref), ("rodada 1 (32)", Image.open(R1 / "espada-32.png").convert("RGBA")),
           ("rodada 2 (32)", Image.open(P / "espada-32.png").convert("RGBA"))]
    o = Image.new("RGB", (3 * 300 + 20, 400), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real (sobre o carvão); a referência é a espada de aço da direita de espadasample.png", fill=(0, 0, 0), font=FONTE)
    d.text((10, 104), "ampliadas na mesma escala, sem suavização (a referência 4x, as de 32 8x)", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im) in enumerate(ims):
        x = 10 + k * 300
        fundo = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); fundo.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
        o.paste(fundo.convert("RGB"), (x, 22)); d.text((x + 80, 50), rot, fill=(0, 0, 0), font=FONTE)
        g = Image.new("RGBA", (256, 256), (24, 24, 28, 255)); g.alpha_composite(im.resize((256, 256), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 124))
    o.save(base / "espada-referencia-r1-r2.png"); print(base / "espada-referencia-r1-r2.png")
    modos = ("atual", "rodada1", "rodada2")
    folha(base / "capturas", [("a ficha do Guerreiro com a espada (32)", "ficha", (18, 362, 272, 472), "espada"),
                              ("o cartão do saque da espada (64; o 48 do 'você usa' sai do 64 reduzido, sem o 48 próprio)", "saque", None, "espada"),
                              ("a roda da luta: o Atacar do Guerreiro (32)", "luta", (250, 10, 470, 225), "espada")],
          base / "espada-no-jogo.png", modos)
    folha(base / "capturas", [("a ficha do Guerreiro com a maça (32)", "ficha", (18, 362, 272, 472), "maca"),
                              ("o corpo no Inventário (40: sem o 40 próprio, o jogo mostra o 32)", "inventario", (150, 140, 480, 520), "maca"),
                              ("o cartão do saque da maça (64; o 48 sai do 64 reduzido)", "saque", None, "maca")],
          base / "maca-no-jogo.png", modos)
    fileira([("maça (atual)", JOGO / "maca-32.png"), ("maça r1", R1 / "maca-32.png"), ("maça r2", P / "maca-32.png"),
             ("espada r2", P / "espada-32.png"), ("espada r1", R1 / "espada-32.png"), ("escudo", JOGO / "escudo-32.png"),
             ("machado", JOGO / "machado-32.png")], base / "fileira-guerreiro-32.png")
    prancha([P / "espada-32.png", P / "espada-64.png", base / "previa" / "espada" / "32" / "espada_silhueta_32.png",
             P / "maca-32.png", P / "maca-64.png", base / "previa" / "maca" / "32" / "maca_silhueta_32.png"], base / "prancha-carvao.png")

def espada_ponta():
    """A ponta da espada (rodada 2): a referência × antes × depois, em tamanho real, a espada inteira ampliada na mesma
    escala e a ponta recortada e ampliada; no jogo, antes × depois no saque e no Atacar; a maça com os 40 e 48."""
    base = LOTE / "espada_maca"; P = base / "proposta"; A = base / "rodada2_ponta_antiga" / "proposta"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/espada/espadasample.png").convert("RGBA").crop((64, 0, 128, 64))
    ims = [("referência (64)", ref, 4, (40, 0, 64, 24)), ("antes (32)", Image.open(A / "espada-32.png").convert("RGBA"), 8, (20, 0, 32, 12)),
           ("depois (32)", Image.open(P / "espada-32.png").convert("RGBA"), 8, (20, 0, 32, 12))]
    o = Image.new("RGB", (3 * 300 + 20, 680), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real sobre o carvão; a referência é a espada de aço da direita de espadasample.png", fill=(0, 0, 0), font=FONTE)
    d.text((10, 104), "a espada inteira, ampliada na mesma escala sem suavização (a referência 4x, as de 32 8x)", fill=(0, 0, 0), font=FONTE)
    d.text((10, 392), "a ponta recortada, ampliada na mesma escala (a referência 10x, as de 32 20x)", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im, z, corte) in enumerate(ims):
        x = 10 + k * 300
        fundo = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); fundo.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
        o.paste(fundo.convert("RGB"), (x, 22)); d.text((x + 80, 50), rot, fill=(0, 0, 0), font=FONTE)
        g = Image.new("RGBA", (256, 256), (24, 24, 28, 255)); g.alpha_composite(im.resize((256, 256), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 124))
        pc = im.crop(corte); zz = 240 // pc.width
        g2 = Image.new("RGBA", (240, 240), (24, 24, 28, 255)); g2.alpha_composite(pc.resize((pc.width * zz, pc.height * zz), Image.NEAREST)); o.paste(g2.convert("RGB"), (x, 412))
    o.save(base / "espada-ponta-antes-depois.png"); print(base / "espada-ponta-antes-depois.png")
    folha(base / "capturas", [("o cartão do saque da espada (64; o 48 sai do 64 reduzido)", "saque", None, "espada"),
                              ("a roda da luta: o Atacar do Guerreiro (32)", "luta", (250, 10, 470, 225), "espada"),
                              ("a ficha (32)", "ficha", (18, 362, 272, 472), "espada")],
          base / "espada-ponta-no-jogo.png", ("rodada2", "ponta_nova"))
    folha(base / "capturas", [("o corpo no Inventário: a maça em 40 (atual: o placeholder; tamanhos: a aprovada com o 40)", "inventario", (150, 140, 480, 520), "maca"),
                              ("o cartão do saque: a maça em 64 e o 'você usa' em 48", "saque", None, "maca"),
                              ("a ficha (32)", "ficha", (18, 362, 272, 472), "maca")],
          base / "maca-tamanhos-no-jogo.png", ("atual", "tamanhos"))
    prancha([P / f"maca-{n}.png" for n in (32, 40, 48, 64)] + [P / "espada-32.png", P / "espada-64.png", A / "espada-32.png"],
            base / "prancha-carvao.png")

def espada_ponta3(nova=None):
    """A ponta da espada, terceira tentativa: a referência × a agulha (rodada 2) × a ponta rombuda (723cf8d) × a nova, em
    tamanho real sobre o carvão, a silhueta numa cor (a forma) e a ponta recortada com a luz, ampliadas sem suavização."""
    base = LOTE / "espada_maca"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/espada/espadasample.png").convert("RGBA").crop((64, 0, 128, 64))
    col = [("referência (64)", ref, (36, 0, 64, 28)),
           ("agulha (rodada 2)", Image.open(base / "rodada2_ponta_antiga/proposta/espada-32.png").convert("RGBA"), (18, 0, 32, 14)),
           ("rombuda (723cf8d)", Image.open(base / "rodada2_ponta_r2/proposta/espada-32.png").convert("RGBA"), (18, 0, 32, 14)),
           ("nova", Image.open(nova or base / "proposta/espada-32.png").convert("RGBA"), (18, 0, 32, 14))]
    W = 240
    o = Image.new("RGB", (len(col) * (W + 10) + 10, 22 + 72 + 22 + W + 22 + W + 30), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real sobre o carvão (a referência é a espada de aço da direita de espadasample.png)", fill=(0, 0, 0), font=FONTE)
    y1 = 22 + 72 + 4; d.text((10, y1), "a silhueta da ponta numa cor (a forma), ampliada sem suavização", fill=(0, 0, 0), font=FONTE)
    y2 = y1 + 18 + W + 4; d.text((10, y2), "a ponta com a luz (o fio e os planos), ampliada sem suavização", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im, corte) in enumerate(col):
        x = 10 + k * (W + 10)
        f = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); f.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
        o.paste(f.convert("RGB"), (x, 22)); d.text((x + 78, 50), rot, fill=(0, 0, 0), font=FONTE)
        pc = im.crop(corte); z = W // pc.width
        a = pc.split()[3]; sil = Image.new("RGBA", pc.size, (0, 0, 0, 0))
        sil.paste(Image.new("RGBA", pc.size, (150, 156, 166, 255)), mask=a)
        cont = Image.new("RGBA", pc.size, (0, 0, 0, 0)); px = pc.load(); cpx = cont.load()
        for yy in range(pc.height):
            for xx in range(pc.width):
                if px[xx, yy][3] and sum(px[xx, yy][:3]) < 60: cpx[xx, yy] = (20, 20, 24, 255)
        sil.alpha_composite(cont)
        for img, yy in ((sil, y1 + 18), (pc, y2 + 18)):
            g = Image.new("RGBA", (W, W), (24, 24, 28, 255)); g.alpha_composite(img.resize((pc.width * z, pc.height * z), Image.NEAREST))
            o.paste(g.convert("RGB"), (x, yy))
    saida = base / "espada-ponta3.png"; o.save(saida); print(saida)
    if nova is None:   # no jogo: a ponta rombuda (as fotos "ponta_nova", do 723cf8d) × a nova ("ponta3")
        folha(base / "capturas", [("o cartão do saque da espada (64; o 48 sai do 64 reduzido)", "saque", None, "espada"),
                                  ("a roda da luta: o Atacar do Guerreiro (32)", "luta", (250, 10, 470, 225), "espada"),
                                  ("a ficha (32)", "ficha", (18, 362, 272, 472), "espada")],
              base / "espada-ponta3-no-jogo.png", ("ponta_nova", "ponta3"))

def espada_ponta4(*novas):
    """A ponta da espada, quarta forma: a referência × a anterior (3962b93) × a(s) nova(s): a espada inteira em tamanho
    real sobre o carvão, a silhueta da ponta numa cor com o eixo da lâmina marcado (vermelho) e o acabamento, ampliados
    sem suavização. novas: (rótulo, png) de cada candidata; sem argumento, a proposta."""
    base = LOTE / "espada_maca"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/espada/espadasample.png").convert("RGBA").crop((64, 0, 128, 64))
    novas = novas or (("nova", base / "proposta/espada-32.png"),)
    # o eixo de cada uma: a reta x + y = c (nas coordenadas das bordas dos pixels) no recorte da ponta
    col = [("referência (64)", ref, (36, 0, 64, 28), 65.5 - 36)] +           [("anterior (3962b93)", Image.open(base / "rodada2_ponta_r3/proposta/espada-32.png").convert("RGBA"), (18, 0, 32, 14), 32 - 18)] +           [(r, Image.open(f).convert("RGBA"), (18, 0, 32, 14), 32 - 18) for r, f in novas]
    W = 224
    o = Image.new("RGB", (len(col) * (W + 10) + 10, 22 + 72 + 22 + W + 22 + W + 16), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "a espada inteira em tamanho real sobre o carvão (a referência: a espada de aço da direita de espadasample.png)", fill=(0, 0, 0), font=FONTE)
    y1 = 22 + 72 + 4; d.text((10, y1), "a silhueta da ponta numa cor, com o eixo da lâmina (vermelho), ampliada sem suavização", fill=(0, 0, 0), font=FONTE)
    y2 = y1 + 18 + W + 4; d.text((10, y2), "o acabamento (o fio e os planos do aço), ampliado sem suavização", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im, corte, eixo) in enumerate(col):
        x = 10 + k * (W + 10)
        f = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); f.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
        o.paste(f.convert("RGB"), (x, 22)); d.text((x + 78, 50), rot, fill=(0, 0, 0), font=FONTE)
        pc = im.crop(corte); z = W // pc.width
        sil = Image.new("RGBA", pc.size, (0, 0, 0, 0)); spx = sil.load(); px = pc.load()
        for yy in range(pc.height):
            for xx in range(pc.width):
                if px[xx, yy][3]:
                    spx[xx, yy] = (20, 20, 24, 255) if sum(px[xx, yy][:3]) < 60 and px[xx, yy][:3] == (8, 8, 10) or (pc is not None and sum(px[xx, yy][:3]) < 30) else (150, 156, 166, 255)
        for img, yy, marca in ((sil, y1 + 18, True), (pc, y2 + 18, False)):
            g = Image.new("RGBA", (W, W), (24, 24, 28, 255)); g.alpha_composite(img.resize((pc.width * z, pc.height * z), Image.NEAREST))
            if marca:
                ImageDraw.Draw(g).line([(eixo * z, 0), (0, eixo * z)], fill=(230, 60, 60, 255), width=2)
            o.paste(g.convert("RGB"), (x, yy))
    saida = base / "espada-ponta4.png"; o.save(saida); print(saida)

def espada_tamanhos():
    """A espada aprovada com o 40 e o 48: os quatro tamanhos ampliados (a ponta de cada grade) e, no jogo, atual × a espada
    com os quatro tamanhos no Inventário (40) e na comparação do saque (64 e 48)."""
    base = LOTE / "espada_maca"; P = base / "proposta"
    o = Image.new("RGB", (4 * 250 + 10, 22 + 240 + 22 + 240 + 10), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "a espada nos quatro tamanhos (o 64 é o 32 ampliado 2x), ampliados sem suavização", fill=(0, 0, 0), font=FONTE)
    d.text((10, 22 + 240 + 4), "a ponta de cada grade, recortada e ampliada (o 32 e o 64 são os aprovados)", fill=(0, 0, 0), font=FONTE)
    for k, n in enumerate((32, 40, 48, 64)):
        im = Image.open(P / f"espada-{n}.png").convert("RGBA"); x = 10 + k * 250
        z = 240 // n
        g = Image.new("RGBA", (240, 240), (24, 24, 28, 255)); g.alpha_composite(im.resize((n * z, n * z), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 22))
        c = im.crop((n * 9 // 16, 0, n, n * 7 // 16)); zz = 240 // c.width
        g = Image.new("RGBA", (240, 240), (24, 24, 28, 255)); g.alpha_composite(c.resize((c.width * zz, c.height * zz), Image.NEAREST)); o.paste(g.convert("RGB"), (x, 22 + 240 + 22))
        d.text((x + 4, 26), f"{n}", fill=(230, 230, 230), font=FONTE)
    o.save(base / "espada-tamanhos.png"); print(base / "espada-tamanhos.png")
    folha(base / "capturas", [("o corpo no Inventário: a espada em 40 (atual: o placeholder; tamanhos: a aprovada com o 40)", "inventario", (150, 140, 480, 520), "espada"),
                              ("o cartão do saque: a espada em 64 e o 'você usa' em 48", "saque", None, "espada"),
                              ("a ficha (32)", "ficha", (18, 362, 272, 472), "espada")],
          base / "espada-tamanhos-no-jogo.png", ("atual", "tamanhos"))

def elmo_cota():
    """O elmo e a cota (o remake do ferro, 2): atual × proposta no jogo, a fileira com o escudo e as armas aprovadas e a
    prancha."""
    base = LOTE / "elmo_cota"; P = base / "proposta"
    folha(base / "capturas", [("a ficha do Guerreiro com o elmo e a cota (32)", "ficha", (18, 362, 272, 472)),
                              ("o corpo no Inventário (40: a proposta só tem o 32 e o 64, e o jogo mostra o 32)", "inventario", (150, 140, 480, 520)),
                              ("o cartão do saque do elmo (64; o 48 sai do 64 reduzido, sem o 48 próprio)", "saque", None),
                              ("o cartão do saque da cota (64 e 48, idem)", "saque", None, "saque_cota")],
          base / "elmo_cota-no-jogo.png")
    fileira([("elmo (prop.)", P / "elmo-32.png"), ("cota (prop.)", P / "cota-32.png"), ("escudo", JOGO / "escudo-32.png"),
             ("espada", JOGO / "espada-32.png"), ("maça", JOGO / "maca-32.png"), ("machado", JOGO / "machado-32.png"),
             ("elmo (atual)", JOGO / "elmo-32.png"), ("cota (atual)", JOGO / "cota-32.png")], base / "fileira-guerreiro-32.png")
    prancha([P / "elmo-32.png", P / "elmo-64.png", base / "previa/elmo/32/elmo_silhueta_32.png",
             P / "cota-32.png", P / "cota-64.png", base / "previa/cota/32/cota_silhueta_32.png"], base / "prancha-carvao.png")

def elmo_cota_r2():
    """O capacete e o peito, rodada 2 (pelas referências de ferramentas/arte/referencias/capacete/ e peitoral/): a
    referência principal × a rodada 1 × a nova, em tamanho real sobre o carvão (com o escudo e as armas aprovadas) e
    ampliadas sem suavização."""
    base = LOTE / "elmo_cota"; P = base / "proposta"; R1 = base / "rodada1" / "proposta"
    REF = RAIZ / "ferramentas/arte/referencias"
    refs = {"elmo": Image.open(REF / "capacete/5+N9Nb.png").convert("RGBA").crop((147, 479, 191, 532)),   # o nº 62
            "cota": Image.open(REF / "peitoral/etbij8.png").convert("RGBA").crop((433, 684, 494, 742))}   # o nº 103
    linhas = [(f"{p}", [("referência", refs[p]), ("rodada 1", Image.open(R1 / f"{p}-32.png").convert("RGBA")),
                         ("nova", Image.open(P / f"{p}-32.png").convert("RGBA"))]) for p in ("elmo", "cota")]
    viz = [(r, Image.open(JOGO / f"{n}-32.png").convert("RGBA")) for r, n in (("escudo", "escudo"), ("espada", "espada"),
                                                                               ("maça", "maca"), ("machado", "machado"))]
    W = 250
    o = Image.new("RGB", (10 + 3 * (W + 10) + 4 * 60, 2 * (22 + 72 + 6 + W) + 30), (245, 245, 245)); d = ImageDraw.Draw(o)
    y = 6
    for nome, ims in linhas:
        d.text((10, y), f"{nome}: tamanho real sobre o carvão (a referência no tamanho dela) e ampliado sem suavização; à direita, o escudo e as armas aprovadas", fill=(0, 0, 0), font=FONTE)
        y += 18
        for k, (rot, im) in enumerate(ims):
            x = 10 + k * (W + 10)
            f = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); f.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
            o.paste(f.convert("RGB"), (x, y)); d.text((x + 78, y + 28), rot, fill=(0, 0, 0), font=FONTE)
            z = W // max(im.size)
            g = Image.new("RGBA", (W, W), (24, 24, 28, 255)); g.alpha_composite(im.resize((im.width * z, im.height * z), Image.NEAREST),
                                                                             ((W - im.width * z) // 2, (W - im.height * z) // 2))
            o.paste(g.convert("RGB"), (x, y + 78))
        for k, (rot, im) in enumerate(viz):
            x = 10 + 3 * (W + 10) + k * 60
            f = Image.new("RGBA", (40, 40), (24, 24, 28, 255)); f.alpha_composite(im, (4, 4)); o.paste(f.convert("RGB"), (x, y + 16))
            d.text((x, y + 60), rot, fill=(0, 0, 0), font=FONTE)
        y += 78 + W + 10
    o.save(base / "elmo_cota-referencias-r1-r2.png"); print(base / "elmo_cota-referencias-r1-r2.png")

def elmo_r3():
    """O elmo, rodada 3: a referência principal × a rodada 2 × a nova, em tamanho real sobre o carvão e ampliadas sem
    suavização (com a silhueta numa cor); e a cota com os quatro tamanhos no jogo (o Inventário e o "você usa")."""
    base = LOTE / "elmo_cota"; P = base / "proposta"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/capacete/5+N9Nb.png").convert("RGBA").crop((147, 479, 191, 532))
    col = [("referência (o nº 62)", ref), ("rodada 2", Image.open(base / "elmo_r2/proposta/elmo-32.png").convert("RGBA")),
           ("nova (rodada 3)", Image.open(P / "elmo-32.png").convert("RGBA"))]
    W = 250
    o = Image.new("RGB", (10 + 3 * (W + 10), 22 + 72 + 22 + W + 22 + W + 10), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real sobre o carvão (a referência no tamanho dela)", fill=(0, 0, 0), font=FONTE)
    y1 = 22 + 72 + 4; d.text((10, y1), "a silhueta numa cor, ampliada sem suavização", fill=(0, 0, 0), font=FONTE)
    y2 = y1 + 18 + W + 4; d.text((10, y2), "o acabamento, ampliado sem suavização", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im) in enumerate(col):
        x = 10 + k * (W + 10)
        f = Image.new("RGBA", (72, 72), (24, 24, 28, 255)); f.alpha_composite(im, ((72 - im.width) // 2, (72 - im.height) // 2))
        o.paste(f.convert("RGB"), (x, 22)); d.text((x + 78, 50), rot, fill=(0, 0, 0), font=FONTE)
        sil = Image.new("RGBA", im.size, (0, 0, 0, 0)); sil.paste(Image.new("RGBA", im.size, (150, 156, 166, 255)), mask=im.split()[3])
        z = W // max(im.size)
        for img, yy in ((sil, y1 + 18), (im, y2 + 18)):
            g = Image.new("RGBA", (W, W), (24, 24, 28, 255))
            g.alpha_composite(img.resize((im.width * z, im.height * z), Image.NEAREST), ((W - im.width * z) // 2, (W - im.height * z) // 2))
            o.paste(g.convert("RGB"), (x, yy))
    o.save(base / "elmo-referencia-r2-r3.png"); print(base / "elmo-referencia-r2-r3.png")
    folha(base / "capturas", [("o corpo no Inventário: a cota em 40 (atual: o placeholder; tamanhos: a aprovada com o 40)", "inventario", (150, 140, 480, 520), "cota_tamanhos"),
                              ("o cartão do saque: a cota em 64 e o 'você usa' em 48", "saque", None, "cota_tamanhos")],
          base / "cota-tamanhos-no-jogo.png", ("atual", "tamanhos"))
    prancha([P / f"cota-{n}.png" for n in (32, 40, 48, 64)] + [P / "elmo-32.png", P / "elmo-64.png"], base / "prancha-carvao.png")

def elmo_r4():
    """O elmo, rodada 4: a nova referência principal (a coluna da direita de elmo-frente-jean.webp, o acabamento) × a
    rodada 3 × a nova; em tamanho real sobre o carvão (o 32 e o 64) e ampliadas 8× sem suavização. A referência só é
    reduzida para caber na folha, nunca vira sprite."""
    base = LOTE / "elmo_cota"; P = base / "proposta"
    ref = Image.open(RAIZ / "ferramentas/arte/referencias/capacete/elmo-frente-jean.webp").convert("RGBA").crop((930, 680, 1368, 1115))
    r3 = Image.open(base / "elmo_r3/proposta/elmo-32.png").convert("RGBA"); r4 = Image.open(P / "elmo-32.png").convert("RGBA")
    W = 256
    o = Image.new("RGB", (10 + 3 * (W + 10), 22 + 84 + 22 + W + 10), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 40), "tamanho real sobre o carvão:", fill=(0, 0, 0), font=FONTE)
    d.text((10, 56), "o 32 e o 64 (= 32 ×2)", fill=(0, 0, 0), font=FONTE)
    for k, (rot, im) in enumerate((("rodada 3", r3), ("nova (rodada 4)", r4))):
        x = 10 + (k + 1) * (W + 10)
        f = Image.new("RGBA", (W, 84), (24, 24, 28, 255))
        f.alpha_composite(im, (40, 26)); f.alpha_composite(im.resize((64, 64), Image.NEAREST), (120, 10))
        o.paste(f.convert("RGB"), (x, 22)); d.text((x, 4), rot, fill=(0, 0, 0), font=FONTE)
    y = 22 + 84 + 4; d.text((10, y), "a referência (reduzida só para a folha) e os dois ampliados 8× sem suavização", fill=(0, 0, 0), font=FONTE)
    o.paste(ref.resize((W, W), Image.LANCZOS).convert("RGB"), (10, y + 18))
    for k, im in enumerate((r3, r4)):
        g = Image.new("RGBA", (W, W), (24, 24, 28, 255)); g.alpha_composite(im.resize((W, W), Image.NEAREST))
        o.paste(g.convert("RGB"), (10 + (k + 1) * (W + 10), y + 18))
    o.save(base / "elmo-referencia-r3-r4.png"); print(base / "elmo-referencia-r3-r4.png")

def elmo_tamanhos():
    """O elmo aprovado (b4e920d) com o 40 e o 48: no Inventário (40) e no "você usa" do saque (48), atual × tamanhos; e
    os quatro tamanhos em tamanho real sobre o carvão."""
    base = LOTE / "elmo_cota"; P = base / "proposta"
    folha(base / "capturas", [("o corpo no Inventário: o elmo em 40 (atual: o placeholder; tamanhos: o aprovado com o 40)", "inventario", (150, 140, 480, 520), "elmo_tamanhos"),
                              ("o cartão do saque: o elmo em 64 e o 'você usa' em 48", "saque", None, "elmo_tamanhos")],
          base / "elmo-tamanhos-no-jogo.png", ("atual", "tamanhos"))
    prancha([P / f"elmo-{n}.png" for n in (32, 40, 48, 64)] + [P / f"cota-{n}.png" for n in (32, 40, 48, 64)], base / "prancha-carvao.png")

def manopla_perneiras():
    """A manopla e as perneiras (o remake do ferro, 3; só o 32 e o 64): em tamanho real sobre o carvão ao lado das peças
    aprovadas da família (o elmo, a cota, a espada, a maça, o escudo), o 64 e a ampliação sem suavização; e no jogo, a
    ficha (32) e o saque de cada uma (64 e o "você usa" em 48), atual × proposta."""
    base = LOTE / "manopla_perneiras" / "recusadas_c5fd33b"; P = base / "proposta"; J = RAIZ / "rpg/web/static/hud/icones"   # (guardada)
    fam = [("elmo", LOTE / "elmo_cota/proposta/elmo-32.png"), ("cota", J / "cota-32.png"), ("manopla", P / "manopla-32.png"),
           ("perneiras", P / "perneiras-32.png"), ("espada", J / "espada-32.png"), ("maça", J / "maca-32.png"), ("escudo", J / "escudo-32.png")]
    ims = [(r, Image.open(a).convert("RGBA")) for r, a in fam]
    novos = [Image.open(P / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")]
    r1 = Image.open(base.parent / "perneiras_r1/previa/32/perneiras_final_32.png").convert("RGBA")
    W = 7 * 48 + 20; Z = 8
    o = Image.new("RGB", (max(W, 3 * (32 * Z + 10)) + 20, 22 + 48 + 22 + 72 + 22 + 32 * Z + 30), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real sobre o carvão: " + ", ".join(r for r, _ in ims), fill=(0, 0, 0), font=FONTE)
    f = Image.new("RGBA", (W, 48), (24, 24, 28, 255))
    for k, (_, im) in enumerate(ims):
        f.alpha_composite(im, (10 + k * 48 + 8, 8))
    o.paste(f.convert("RGB"), (10, 22))
    y = 22 + 48 + 6; d.text((10, y), "o 64 (= 32 ×2) da manopla e das perneiras", fill=(0, 0, 0), font=FONTE)
    f = Image.new("RGBA", (2 * 72 + 10, 72), (24, 24, 28, 255))
    for k, im in enumerate(novos):
        f.alpha_composite(im.resize((64, 64), Image.NEAREST), (4 + k * 78, 4))
    o.paste(f.convert("RGB"), (10, y + 16))
    y += 16 + 72 + 6
    d.text((10, y), "ampliadas 8× sem suavização: a manopla, as perneiras e a 1.ª passada das perneiras (recusada: a calça)", fill=(0, 0, 0), font=FONTE)
    for k, im in enumerate(novos + [r1]):
        g = Image.new("RGBA", (32 * Z, 32 * Z), (24, 24, 28, 255)); g.alpha_composite(im.resize((32 * Z, 32 * Z), Image.NEAREST))
        o.paste(g.convert("RGB"), (10 + k * (32 * Z + 10), y + 16))
    o.save(base / "manopla_perneiras-familia.png"); print(base / "manopla_perneiras-familia.png")
    folha(base / "capturas", [("a ficha: a manopla e as perneiras vestidas (32)", "ficha", None),
                              ("o cartão do saque: a manopla em 64 e o 'você usa' em 48 (o 48 ainda pelo 32 ×2 reduzido)", "saque", None),
                              ("o cartão do saque: as perneiras em 64 e o 'você usa' em 48", "saque", None, "saque_perneiras")],
          base / "manopla_perneiras-no-jogo.png")

def manopla_perneiras_r3():
    """A manopla e as perneiras refeitas pelas referências novas (só o 32 e o 64): em tamanho real sobre o carvão ao lado
    das peças de ferro aprovadas (o elmo, a cota, a espada, a maça, o escudo); o 64; as duas ampliadas 8× sem suavização
    ao lado das recusadas do c5fd33b; e a ficha a 1920×945, atual × a rodada nova (o recorte do equipamento)."""
    base = LOTE / "manopla_perneiras" / "rodada3_89be986"; P = base / "proposta"; R = base.parent / "recusadas_c5fd33b/proposta"; J = RAIZ / "rpg/web/static/hud/icones"   # (guardada)
    fam = [LOTE / "elmo_cota/proposta/elmo-32.png", J / "cota-32.png", P / "manopla-32.png", P / "perneiras-32.png",
           J / "espada-32.png", J / "maca-32.png", J / "escudo-32.png"]
    fam = [Image.open(a).convert("RGBA") for a in fam]
    novos = [Image.open(P / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")]
    velhos = [Image.open(R / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")]
    Z = 6; L = 32 * Z
    fichas = [Image.open(base / f"capturas/{m}-1920x945-ficha.png").convert("RGB") for m in ("atual", "rodada3")]
    fichas = [f.crop((20, 370, f.width - 20, 480)) for f in fichas]
    W = 10 + 4 * (L + 10)
    H = 22 + 48 + 22 + 72 + 22 + L + 22 + max(f.height for f in fichas) + 12
    o = Image.new("RGB", (W, H), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real sobre o carvão: elmo, cota, manopla (nova), perneiras (nova), espada, maça, escudo", fill=(0, 0, 0), font=FONTE)
    f = Image.new("RGBA", (7 * 48 + 20, 48), (24, 24, 28, 255))
    for k, im in enumerate(fam):
        f.alpha_composite(im, (10 + k * 48 + 8, 8))
    o.paste(f.convert("RGB"), (10, 22))
    y = 22 + 48 + 6; d.text((10, y), "o 64 (= 32 ×2) das duas", fill=(0, 0, 0), font=FONTE)
    f = Image.new("RGBA", (2 * 72 + 10, 72), (24, 24, 28, 255))
    for k, im in enumerate(novos):
        f.alpha_composite(im.resize((64, 64), Image.NEAREST), (4 + k * 78, 4))
    o.paste(f.convert("RGB"), (10, y + 16))
    y += 16 + 72 + 6
    d.text((10, y), "ampliadas 6× sem suavização: a manopla e as perneiras novas | as recusadas do c5fd33b", fill=(0, 0, 0), font=FONTE)
    for k, im in enumerate(novos + velhos):
        g = Image.new("RGBA", (L, L), (24, 24, 28, 255)); g.alpha_composite(im.resize((L, L), Image.NEAREST))
        o.paste(g.convert("RGB"), (10 + k * (L + 10), y + 16))
    y += 16 + L + 6
    d.text((10, y), "a ficha a 1920×945 (o equipamento, tamanho real): atual | a rodada nova", fill=(0, 0, 0), font=FONTE)
    for k, fi in enumerate(fichas):
        o.paste(fi, (10 + k * (fi.width + 10), y + 16))
    o.save(base / "manopla_perneiras-r3.png"); print(base / "manopla_perneiras-r3.png", o.size)

def manopla_perneiras_r4():
    """A rodada 4 da manopla e das perneiras (só o 32 e o 64): antes (a rodada do 89be986) × depois, em tamanho real
    sobre o carvão junto das peças de ferro aprovadas; ampliadas sem suavização, com o recorte da referência ao lado
    (a imagem do Jean, só reduzida para a folha); e a ficha a 1920×945, antes × depois."""
    base = LOTE / "manopla_perneiras" / "rodada4_9509530"; P = base / "proposta"; A = base.parent / "rodada3_89be986"; J = RAIZ / "rpg/web/static/hud/icones"   # (guardada)
    REF = RAIZ / "ferramentas/arte/referencias"
    ap = [LOTE / "elmo_cota/proposta/elmo-32.png", J / "cota-32.png", J / "espada-32.png", J / "maca-32.png", J / "escudo-32.png"]
    ap = [Image.open(a).convert("RGBA") for a in ap]
    novos = {n: Image.open(P / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")}
    velhos = {n: Image.open(A / f"proposta/{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")}
    def ref(arq):
        r = Image.open(arq).convert("RGBA"); bg = Image.new("RGBA", r.size, (24, 24, 28, 255)); bg.alpha_composite(r)
        return bg.convert("RGB")
    refs = {"perneiras": ref(REF / "calça/perneiras-jean.webp"), "manopla": ref(REF / "Luvas/manopla-jean.webp")}
    Z = 6; L = 32 * Z
    fichas = [Image.open(A / "capturas/rodada3-1920x945-ficha.png").convert("RGB"), Image.open(base / "capturas/rodada4-1920x945-ficha.png").convert("RGB")]
    fichas = [f.crop((20, 370, f.width - 20, 480)) for f in fichas]
    W = 10 + 3 * (L + 10)
    H = 22 + 2 * 52 + 8 + 2 * (22 + L) + 22 + max(f.height for f in fichas) + 12
    o = Image.new("RGB", (W, H), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real, com as peças de ferro aprovadas: antes (89be986) | depois", fill=(0, 0, 0), font=FONTE)
    y = 22
    for rot, par in (("antes", velhos), ("depois", novos)):
        f = Image.new("RGBA", (7 * 48 + 20, 48), (24, 24, 28, 255))
        for k, im in enumerate([ap[0], ap[1], par["manopla"], par["perneiras"]] + ap[2:]):
            f.alpha_composite(im, (10 + k * 48 + 8, 8))
        o.paste(f.convert("RGB"), (10, y)); d.text((7 * 48 + 40, y + 18), rot, fill=(0, 0, 0), font=FONTE); y += 52
    y += 8
    for n in ("perneiras", "manopla"):
        d.text((10, y), f"{n}: referência (reduzida só p/ a folha) | antes | depois (6×, sem suavizar)", fill=(0, 0, 0), font=FONTE)
        r = refs[n]; r.thumbnail((L, L), Image.LANCZOS)
        g = Image.new("RGB", (L, L), (24, 24, 28)); g.paste(r, ((L - r.width) // 2, (L - r.height) // 2)); o.paste(g, (10, y + 16))
        for k, im in enumerate((velhos[n], novos[n])):
            g = Image.new("RGBA", (L, L), (24, 24, 28, 255)); g.alpha_composite(im.resize((L, L), Image.NEAREST))
            o.paste(g.convert("RGB"), (10 + (k + 1) * (L + 10), y + 16))
        y += 16 + L + 6
    d.text((10, y), "a ficha a 1920×945, tamanho real: antes | depois", fill=(0, 0, 0), font=FONTE)
    for k, fi in enumerate(fichas):
        o.paste(fi, (10 + k * (fi.width + 10), y + 16))
    o.save(base / "manopla_perneiras-r4.png"); print(base / "manopla_perneiras-r4.png", o.size)

def manopla_perneiras_r5():
    """A rodada 5 (o recomeço, desenhada à mão no Aseprite; só o 32 e o 64): antes (a rodada 4, 9509530) × depois em
    tamanho real sobre o carvão junto do equipamento aprovado; cada peça com a referência principal escolhida ao lado
    (pixel art, ampliada sem suavização), o antes e o depois ampliados 6× sem suavização."""
    base = LOTE / "manopla_perneiras"; P = base / "proposta"; A = base / "rodada4_9509530/proposta"; J = RAIZ / "rpg/web/static/hud/icones"
    REF = RAIZ / "ferramentas/arte/referencias"
    ap = [LOTE / "elmo_cota/proposta/elmo-32.png", J / "cota-32.png", J / "espada-32.png", J / "maca-32.png", J / "escudo-32.png"]
    ap = [Image.open(a).convert("RGBA") for a in ap]
    novos = {n: Image.open(P / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")}
    velhos = {n: Image.open(A / f"{n}-32.png").convert("RGBA") for n in ("manopla", "perneiras")}
    refs = {"perneiras": Image.open(REF / "calça/perneiras-escuras.png").convert("RGB"),
            "manopla": Image.open(REF / "Luvas/1.gif").convert("RGB").crop((860, 410, 1020, 580))}
    Z = 6; L = 32 * Z
    W = 10 + 3 * (L + 10)
    H = 22 + 2 * 52 + 8 + 2 * (22 + L) + 10
    o = Image.new("RGB", (W, H), (245, 245, 245)); d = ImageDraw.Draw(o)
    d.text((10, 4), "tamanho real, com o equipamento aprovado: antes (9509530) | depois", fill=(0, 0, 0), font=FONTE)
    y = 22
    for rot, par in (("antes", velhos), ("depois", novos)):
        f = Image.new("RGBA", (7 * 48 + 20, 48), (24, 24, 28, 255))
        for k, im in enumerate([ap[0], ap[1], par["manopla"], par["perneiras"]] + ap[2:]):
            f.alpha_composite(im, (10 + k * 48 + 8, 8))
        o.paste(f.convert("RGB"), (10, y)); d.text((7 * 48 + 40, y + 18), rot, fill=(0, 0, 0), font=FONTE); y += 52
    y += 8
    for n, nome_ref in (("perneiras", "perneiras-escuras.png"), ("manopla", "Raven, 2.ª linha, 4.ª")):
        d.text((10, y), f"{n}: referência ({nome_ref}) | antes | depois (6×, sem suavizar)", fill=(0, 0, 0), font=FONTE)
        r = refs[n]; z = max(1, L // max(r.size)); r = r.resize((r.width * z, r.height * z), Image.NEAREST)
        g = Image.new("RGB", (L, L), (24, 24, 28)); g.paste(r, ((L - r.width) // 2, (L - r.height) // 2)); o.paste(g, (10, y + 16))
        for k, im in enumerate((velhos[n], novos[n])):
            g = Image.new("RGBA", (L, L), (24, 24, 28, 255)); g.alpha_composite(im.resize((L, L), Image.NEAREST))
            o.paste(g.convert("RGB"), (10 + (k + 1) * (L + 10), y + 16))
        y += 16 + L + 6
    o.save(base / "manopla_perneiras-r5.png"); print(base / "manopla_perneiras-r5.png", o.size)

def lote_exploracao():
    """O lote de exploração (20/10/2026): duas pranchas, as luvas L1 a L5 e as pernas P1 a P5. Em cada uma: os candidatos
    em tamanho real sobre o carvão ao lado das peças aprovadas (o elmo, a cota, a espada, a maça, o escudo); cada
    candidato ampliado 6× sem suavização com o nome; nas guiadas, a referência principal ao lado (só reduzida para a
    folha); nas luvas, o estudo da mão (a camada estudo_mao, oculta na fonte) por baixo de cada uma."""
    base = LOTE / "manopla_perneiras" / "lote_exploracao"; P = base / "proposta"; J = RAIZ / "rpg/web/static/hud/icones"
    REF = RAIZ / "ferramentas/arte/referencias"
    ASE = r"C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe"
    ap = [Image.open(a).convert("RGBA") for a in (LOTE / "elmo_cota/proposta/elmo-32.png", J / "cota-32.png", J / "espada-32.png", J / "maca-32.png", J / "escudo-32.png")]
    raven = Image.open(REF / "Luvas/1.gif").convert("RGBA").crop((630, 410, 790, 580))
    lion = Image.open(REF / "calça/1.gif").convert("RGBA").crop((430, 170, 560, 300))
    grupos = {
        "luvas": [("L1", "malha (luva-malha)", REF / "Luvas/luva-malha.png"), ("L2", "placas (Raven)", raven),
                  ("L3", "livre em malha", None), ("L4", "livre em placas", None), ("L5", "livre mista", None),
                  ("L6", "a forma de mão pedida", None)],
        "pernas": [("P1", "malha (calca-malha)", REF / "calça/calca-malha.png"), ("P2", "placas (Lion Knight)", lion),
                   ("P3", "livre em malha", None), ("P4", "livre mista", None), ("P5", "livre em placas", None)],
    }
    Z = 6; L = 32 * Z
    for nome, cands in grupos.items():
        luvas = nome == "luvas"
        H = 22 + 52 + 10 + 18 + L + (18 + 128 if luvas else 0) + 26 + L // 2 + 12
        W = 10 + len(cands) * (L + 10)
        o = Image.new("RGB", (W, H), (245, 245, 245)); d = ImageDraw.Draw(o)
        d.text((10, 4), f"{nome}: tamanho real sobre o carvão, com o elmo, a cota, a espada, a maça e o escudo aprovados", fill=(0, 0, 0), font=FONTE)
        ims = [Image.open(P / f"{c}-32.png").convert("RGBA") for c, _, _ in cands]
        f = Image.new("RGBA", ((len(cands) + 5) * 48 + 20, 48), (24, 24, 28, 255))
        for k, im in enumerate(ap[:2] + ims + ap[2:]):
            f.alpha_composite(im, (10 + k * 48 + 8, 8))
        o.paste(f.convert("RGB"), (10, 22))
        for k, (c, _, _) in enumerate(cands):
            d.text((10 + (k + 2) * 48 + 18, 22 + 50), c, fill=(0, 0, 0), font=FONTE)
        y = 22 + 52 + 14
        for k, ((c, rot, _), im) in enumerate(zip(cands, ims)):
            x = 10 + k * (L + 10)
            g = Image.new("RGBA", (L, L), (24, 24, 28, 255)); g.alpha_composite(im.resize((L, L), Image.NEAREST))
            o.paste(g.convert("RGB"), (x, y + 18)); d.text((x, y + 2), f"{c}: {rot} (6×)", fill=(0, 0, 0), font=FONTE)
        y += 18 + L
        if luvas:
            d.text((10, y + 2), "o estudo da mão de cada uma (a camada estudo_mao, oculta na fonte), 4×", fill=(0, 0, 0), font=FONTE)
            for k, (c, _, _) in enumerate(cands):
                tmp = base / f"_estudo_{c}.png"
                subprocess.run([ASE, "-b", "--layer", "estudo_mao", str(base / f"fontes/{c}/{c}-32.aseprite"), "--save-as", str(tmp)], check=True, capture_output=True)
                e = Image.open(tmp).convert("RGBA"); tmp.unlink()
                e.putalpha(e.getchannel("A").point(lambda a: 255 if a else 0))
                g = Image.new("RGBA", (128, 128), (24, 24, 28, 255)); g.alpha_composite(e.resize((128, 128), Image.NEAREST))
                o.paste(g.convert("RGB"), (10 + k * (L + 10), y + 18))
            y += 18 + 128
        d.text((10, y + 4), "a referência principal das guiadas (reduzida só para a folha)", fill=(0, 0, 0), font=FONTE)
        for k, (c, _, r) in enumerate(cands):
            if r is None:
                continue
            r = Image.open(r).convert("RGBA") if not isinstance(r, Image.Image) else r
            bg = Image.new("RGBA", r.size, (24, 24, 28, 255)); bg.alpha_composite(r)
            z = max(1, (L // 2) // max(r.size)); r2 = bg.resize((r.width * z, r.height * z), Image.NEAREST) if z > 1 else bg.copy()
            r2.thumbnail((L // 2, L // 2), Image.LANCZOS)
            o.paste(r2.convert("RGB"), (10 + k * (L + 10), y + 22)); d.text((10 + k * (L + 10) + r2.width + 6, y + 24), c, fill=(0, 0, 0), font=FONTE)
        o.save(base / f"lote-{nome}.png"); print(base / f"lote-{nome}.png", o.size)
    # os favoritos na ficha a 1920×945 (a minha avaliação, não aprovação): A = L3 + P1, B = L2 + P4
    fichas = [Image.open(base / f"capturas/{m}-1920x945-ficha.png").convert("RGB") for m in ("atual", "favoritos-A", "favoritos-B")]
    fichas = [f.crop((20, 370, f.width - 20, 480)) for f in fichas]
    o = Image.new("RGB", (3 * (fichas[0].width + 10) + 10, fichas[0].height + 30), (245, 245, 245)); d = ImageDraw.Draw(o)
    for k, (fi, rot) in enumerate(zip(fichas, ("atual", "A: L3 + P1", "B: L2 + P4"))):
        x = 10 + k * (fi.width + 10); d.text((x, 4), f"{rot} (1920x945, tamanho real)", fill=(0, 0, 0), font=FONTE); o.paste(fi, (x, 22))
    o.save(base / "lote-favoritos-ficha.png"); print(base / "lote-favoritos-ficha.png", o.size)

def sandalia_no_jogo():
    """A Sandália no jogo (1.142.0), em tamanho real: o saque, a ficha e o Inventário depois de "Equipar agora"."""
    pasta = LOTE / "sandalia_chapeu" / "capturas" / "integracao"
    ims = [("o cartão do saque (64) e o que você usa (48)", "no-jogo-1.142.0-1920x945-saque.png"),
           ("a ficha depois de equipar (32)", "no-jogo-1.142.0-1920x945-ficha-equipar.png"),
           ("o corpo no Inventário (40)", "no-jogo-1.142.0-1920x945-inventario-equipar.png")]
    ims = [(r, Image.open(pasta / a).convert("RGB")) for r, a in ims]
    o = Image.new("RGB", (sum(i.width for _, i in ims) + 10 * (len(ims) + 1), max(i.height for _, i in ims) + 30), (245, 245, 245))
    d = ImageDraw.Draw(o); x = 10
    for r, i in ims:
        d.text((x, 6), r, fill=(0, 0, 0), font=FONTE); o.paste(i, (x, 24)); x += i.width + 10
    saida = LOTE / "sandalia_chapeu" / "sandalia-1.142.0-no-jogo.png"; o.save(saida); print(saida)

if __name__ == "__main__" and sys.argv[1] in ("antidoto_base", "frasco_vazio", "anel_referencia", "conjunto_mago", "sandalia_r2",
                                              "sandalia_no_jogo", "besta_diadema", "diadema_r2",
                                              "espada_maca", "espada_maca_r2", "espada_ponta",
                                              "espada_ponta3", "espada_ponta4", "espada_tamanhos",
                                              "elmo_cota", "elmo_cota_r2", "elmo_r3", "elmo_r4", "elmo_tamanhos", "manopla_perneiras", "manopla_perneiras_r3", "manopla_perneiras_r4", "manopla_perneiras_r5", "lote_exploracao"):
    globals()[sys.argv[1]](); sys.exit()
if __name__ == "__main__":
    nome = sys.argv[1]; cfg = LOTES[nome]; base = LOTE / nome
    folha(base / "capturas", cfg["linhas"], base / f"{nome}-no-jogo.png", cfg.get("modos", ("atual", "proposta")))
    prancha(cfg["prancha"](base / "proposta"), base / "prancha-carvao.png")
