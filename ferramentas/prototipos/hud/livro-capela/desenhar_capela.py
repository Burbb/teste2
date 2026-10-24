"""O livro da capela deteriorado (protótipo, 24/10/2026; candidata, nada no jogo): a base aprovada dos livros
(`livro-a2.png`, a A refinada) depois de anos numa capela úmida e abandonada. A base não muda: este script lê uma
cópia dela e desenha os danos por cima, cada forma escolhida à mão (os vértices dos rasgos, os níveis da água, as
colônias de bolor), poucos e assimétricos, em vez de uma camada de ruído.

    python desenhar_capela.py      # grava propostas/livro-capela.png, as máscaras e "capela" em areas.json

- **O que falta de papel** (`FALTA`: a folha de cima arrancada) mostra a folha de baixo, pautada e sem escrita, com a
  sombra da beira rasgada; onde faltam também as de baixo (`FUNDO`), o couro por dentro; onde falta a capa (`SEM_CAPA`),
  nada. A beira que ficou ganha o fio claro do papel rasgado.
- **A água:** três níveis na página da esquerda (a mais molhada) e um baixo na da direita, cada um tingindo o papel que
  já estava lá (o grão continua), com a linha da marca escura no alto; a água que correu pela dobra da direita.
- **O bolor:** colônias verde-acinzentadas e castanhas nas beiras e junto da encadernação.
- **O couro:** mais escuro, gasto nas quinas e nas beiras, sem o canto de baixo da esquerda (onde as folhas também se
  foram) e com bolor perto da lombada.
- **As máscaras** (`mascara-capela-<lado>.png`, na escala 3, do tamanho do bloco de texto de cada página): o que a
  página escreve por cima (a pauta e a tinta, `livro.css`) some onde falta papel (0) e desbota sob o bolor e a água
  (entre 0 e 1). Assim o rasgo tira papel, pauta e tinta juntos, e o dano fica preso à página na rolagem.
"""
import json
import pathlib

from PIL import Image, ImageDraw

AQUI = pathlib.Path(__file__).resolve().parent
P = AQUI / "propostas"
ESCALA = 3

COR = {
    "folha_baixo": (214, 198, 156), "folha_baixo_pauta": (198, 180, 136), "sombra_rasgo": (168, 150, 108),
    "fibra": (242, 232, 200),
    "couro_dentro": (52, 32, 24),
    "agua1": (227, 209, 163), "agua2": (220, 199, 151), "agua3": (211, 188, 139), "agua_dobra": (210, 186, 136),
    "marca1": (200, 174, 124), "marca2": (190, 161, 112), "marca3": (176, 145, 100),
    # o bolor, apagado: verde-acinzentado escuro e médio, castanho e a penugem clara
    "halo": (218, 206, 164), "halo_miolo": (198, 188, 146),
    "d": (80, 84, 68), "v": (114, 120, 98), "m": (116, 94, 70), "c": (166, 164, 138),
}
PAPEL = (232, 217, 175)
# o couro da base, escurecido; a quina gasta fica mais pálida
COURO = {(90, 52, 34): (68, 41, 29), (122, 76, 48): (90, 60, 41), (58, 32, 22): (43, 26, 19),
         (138, 96, 66): (112, 88, 66), (26, 15, 10): (20, 12, 8)}
GASTO = (100, 74, 54)

E = (8, 6, 143, 160)       # a página da esquerda (a folha de cima), como na base
D = (143, 6, 279, 160)     # a da direita

# ------------------------------------------------------------------ os danos, à mão (coordenadas do desenho)
FALTA = [
    # E · o canto de baixo de fora, arrancado (as folhas de baixo também, mais perto da quina: FUNDO)
    [(5, 116), (9, 118), (11, 121), (10, 125), (14, 128), (17, 127), (19, 131), (23, 133), (22, 137), (27, 140),
     (30, 139), (33, 144), (37, 146), (36, 150), (41, 153), (44, 152), (47, 157), (50, 160), (52, 163), (5, 163)],
    # E · a mordida na beira de fora: entra até a primeira letra da última linha ("nem"), só o pé do traço
    [(5, 72), (8, 72), (10, 74), (13, 75), (17, 76), (20, 77), (22, 78), (23, 80), (22, 81), (20, 83), (21, 87),
     (18, 90), (15, 93), (12, 95), (9, 97), (5, 99)],
    # E · duas falhas pequenas na beira de cima
    [(59, 6), (61, 8), (64, 9), (67, 8), (70, 7), (72, 6)],
    [(100, 6), (101, 7), (103, 8), (105, 7), (106, 6)],
    # D · o rasgo que entra pela beira de fora, estreitando, e a fenda fina que continua
    [(282, 42), (279, 42), (274, 44), (269, 45), (264, 48), (259, 51), (256, 53), (254, 55), (252, 56), (251, 57),
     (253, 57), (256, 56), (259, 55), (263, 54), (268, 52), (273, 51), (279, 50), (282, 50)],
    # D · o canto de cima de fora, arrancado
    [(282, 6), (260, 6), (263, 7), (266, 10), (271, 12), (270, 15), (273, 18), (277, 20), (276, 24), (279, 26),
     (282, 27)],
    # D · duas falhas na beira de baixo
    [(189, 163), (190, 160), (192, 157), (195, 158), (197, 155), (200, 157), (203, 160), (204, 163)],
    [(229, 163), (230, 160), (231, 158), (234, 158), (235, 160), (236, 163)],
]
FUNDO = [
    [(5, 133), (9, 137), (12, 142), (17, 146), (19, 151), (25, 155), (28, 163), (5, 163)],
    [(282, 6), (272, 6), (275, 10), (279, 15), (282, 16)],
]
SEM_CAPA = [
    [(0, 147), (3, 150), (4, 154), (7, 157), (9, 162), (13, 166), (14, 170), (0, 170)],
    [(139, 168), (140, 166), (143, 165), (146, 166), (148, 168), (148, 170), (139, 170)],
]
# a água: (o contorno de cima, da esquerda para a direita; a cor de dentro; a da marca). Fecha pela beira de baixo.
AGUA = [
    (E, [(8, 102), (20, 100), (35, 103), (50, 99), (66, 104), (82, 101), (98, 106), (112, 103), (126, 108),
         (138, 105), (143, 107)], "agua1", "marca1"),
    (E, [(8, 118), (24, 114), (40, 119), (58, 115), (74, 121), (92, 117), (110, 123), (128, 119), (143, 124)],
     "agua2", "marca2"),
    (E, [(8, 140), (30, 136), (52, 142), (76, 138), (100, 145), (124, 141), (143, 146)], "agua3", "marca3"),
    (D, [(143, 146), (160, 143), (180, 147), (200, 144), (220, 149), (240, 145), (260, 150), (279, 147)],
     "agua1", "marca1"),
]
# a água que desceu pela dobra da direita: a largura da faixa (a partir da dobra) em cada altura
AGUA_DOBRA = [(30, 2), (40, 4), (52, 6), (64, 5), (76, 7), (88, 6), (100, 8), (112, 6), (124, 7), (136, 5), (146, 3)]

# o bolor: colônias desenhadas à mão ('.' nada) e onde ficam (x, y do canto de cima, espelhar)
MOFO = {
    "grande": ["......c...c.....",
               "...c.cvc.cvvc...",
               "..cvvvdvvvdvvc..",
               ".cvddmmdvddmvvc.",
               "cvdmmddmmddmdvc.",
               ".vdmdddmdmmddvvc",
               "cvvdmmddmdddmvc.",
               ".cvdddmmdmmdvc..",
               "..cvvdvvmdvvc...",
               "...c.cvc.cvc....",
               ".....c...c......"],
    "faixa": ["..c..c...c....c..",
              ".cvc.vvcvvc..cvc.",
              "cvdvvdmvdmvvcvdvc",
              ".vmddmdmddvdvmdv.",
              "cvdvmvdvmvvdmvvc.",
              ".c.cvc.cvc.cvc.c."],
    "media": ["..c.v..",
              ".cvvmc.",
              "cvmdmvc",
              ".vdmdv.",
              "c.vmvc.",
              "..c.c.."],
    "pequena": [".cv.",
                "cvdv",
                ".vmc",
                "..c."],
    "fio": ["c.v..c.v",
            "vdmvvdmv",
            ".c.vc..c"],
}
# o bolor no papel: manchas com contorno próprio (o papel tingido, o miolo mais escuro, os esporos ralos na mancha e
# densos no miolo). (contorno, miolo)
MANCHAS = [
    # E: junto da encadernação, embaixo (a maior)
    ([(118, 128), (124, 124), (131, 126), (137, 121), (143, 123), (143, 160), (126, 160), (120, 154), (122, 147),
      (116, 141), (119, 135)],
     [(127, 140), (133, 135), (140, 137), (143, 142), (143, 156), (134, 157), (128, 151)]),
    # E: na beira do canto arrancado
    ([(40, 146), (46, 143), (54, 146), (60, 152), (58, 160), (48, 160), (43, 155)],
     [(46, 150), (52, 149), (55, 154), (52, 159), (47, 157)]),
    # D: junto da encadernação, em cima
    ([(143, 6), (158, 6), (161, 10), (157, 15), (158, 22), (152, 30), (146, 34), (143, 34)],
     [(143, 6), (152, 6), (153, 12), (148, 18), (143, 20)]),
    # D: o canto de baixo de fora
    ([(250, 146), (258, 141), (268, 143), (279, 140), (279, 160), (256, 160), (250, 154)],
     [(262, 148), (272, 146), (279, 149), (279, 158), (266, 158)]),
]
RALO = ["..v.....",
        "......c.",
        "...d....",
        "c.......",
        ".....m..",
        ".v......",
        "....c...",
        "d......v"]
DENSO = ["vdm.cvd.",
         "d.vdm.vc",
         ".mdv.dmv",
         "cv.mdv.d",
         "dvm.vdm.",
         ".dvcm.dv",
         "mv.dvc.m",
         "vd.mv.dv"]
# satélites (colônias pequenas, à mão) perto das manchas, e o bolor no couro
COLONIAS = [
    ("pequena", 112, 132, False), ("pequena", 63, 150, True), ("pequena", 246, 150, True),
    ("pequena", 273, 56, False),
    ("media", 150, 162, False), ("pequena", 126, 163, True), ("pequena", 15, 162, False),
]
# quinas e beiras do couro mais gastas (pálidas), à mão: (x, y, largura, altura)
GASTOS = [(4, 1, 9, 1), (2, 3, 1, 6), (240, 1, 14, 1), (285, 40, 1, 9), (285, 120, 1, 6), (60, 167, 12, 1),
          (200, 167, 8, 1), (284, 158, 2, 6)]


def poligonos(lista, w, h):
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for pts in lista:
        d.polygon(pts, fill=255)
    return {(x, y) for y in range(h) for x in range(w) if im.getpixel((x, y))}


def dentro(r, x, y):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]


def tingir(rgb, alvo):
    return tuple(min(255, round(c * a / p)) for c, a, p in zip(rgb, alvo, PAPEL))


def main():
    im = Image.open(P / "livro-a2.png").convert("RGBA")
    W, H = im.size
    px = im.load()
    falta, fundo, sem_capa = poligonos(FALTA, W, H), poligonos(FUNDO, W, H), poligonos(SEM_CAPA, W, H)
    pagina = lambda x, y: dentro(E, x, y) or dentro(D, x, y)  # noqa: E731
    lavado = {}  # (x, y) -> quanto da pauta e da tinta fica (0 a 1); 1 onde nada muda

    # o couro, escurecido, com as quinas gastas (antes dos danos, que podem tirá-lo)
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a == 255 and not pagina(x, y) and (r, g, b) in COURO:
                px[x, y] = COURO[(r, g, b)] + (255,)
    for gx, gy, gw, gh in GASTOS:
        for y in range(gy, gy + gh):
            for x in range(gx, gx + gw):
                if px[x, y][3] == 255 and not pagina(x, y):
                    px[x, y] = GASTO + (255,)

    # a água: cada nível tinge o papel que já estava lá; a marca no alto, um pixel mais escura
    for r, contorno, dentro_, marca in AGUA:
        poli = contorno + [(contorno[-1][0], r[3]), (contorno[0][0], r[3])]
        area = poligonos([poli], W, H)
        topo = {}
        for (x, y) in area:
            if dentro(r, x, y):
                topo[x] = min(topo.get(x, y), y)
        for (x, y) in area:
            if dentro(r, x, y) and px[x, y][3] == 255:
                px[x, y] = tingir(px[x, y][:3], COR[dentro_]) + (255,)
                lavado[(x, y)] = min(lavado.get((x, y), 1), 0.88)
        for x, y in topo.items():
            px[x, y] = tingir(px[x, y][:3], COR[marca]) + (255,)
            if y + 1 <= r[3] and x % 5:  # a marca engrossa aqui e ali (não em toda parte)
                px[x, y + 1] = tingir(px[x, y + 1][:3], COR[marca]) + (255,)
    for i in range(len(AGUA_DOBRA) - 1):
        (y0, l0), (y1, l1) = AGUA_DOBRA[i], AGUA_DOBRA[i + 1]
        for y in range(y0, y1):
            larg = round(l0 + (l1 - l0) * (y - y0) / (y1 - y0))
            for x in range(D[0] + 4, D[0] + 4 + larg):
                px[x, y] = tingir(px[x, y][:3], COR["agua_dobra"]) + (255,)
            px[D[0] + 4 + larg, y] = tingir(px[D[0] + 4 + larg, y][:3], COR["marca2"]) + (255,)

    # o papel que falta: a folha de baixo (pautada, sem escrita) ou, mais fundo, o couro por dentro; sem capa, nada
    for (x, y) in falta | fundo:
        if (x, y) in fundo:
            px[x, y] = COR["couro_dentro"] + (255,)
        else:
            pauta = y >= 25 and (y - 25) % 11 == 0 and y <= 146
            px[x, y] = (COR["folha_baixo_pauta"] if pauta else COR["folha_baixo"]) + (255,)
    # a sombra da folha de cima na de baixo (a luz vem de cima e da esquerda) e o fio do papel rasgado na beira
    for (x, y) in falta - fundo:
        if (x - 1, y) not in falta and pagina(x - 1, y) or (x, y - 1) not in falta and pagina(x, y - 1):
            px[x, y] = COR["sombra_rasgo"] + (255,)
    for y in range(H):
        for x in range(W):
            if pagina(x, y) and (x, y) not in falta and any(v in falta for v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                px[x, y] = COR["fibra"] + (255,)
                lavado[(x, y)] = min(lavado.get((x, y), 1), 0.6)
    for (x, y) in falta:
        lavado[(x, y)] = 0
    for (x, y) in sem_capa:
        px[x, y] = (0, 0, 0, 0)

    # o bolor, por cima de tudo o que ficou (papel, folha de baixo, couro); a pauta e a tinta desbotam embaixo dele.
    # As manchas: o papel tingido, o miolo mais escuro, os esporos (ralos na mancha, densos no miolo)
    for contorno, miolo in MANCHAS:
        mancha, centro = poligonos([contorno], W, H), poligonos([miolo], W, H)
        for (x, y) in mancha:
            if not pagina(x, y) or (x, y) in falta:
                continue
            no_miolo = (x, y) in centro
            px[x, y] = tingir(px[x, y][:3], COR["halo_miolo" if no_miolo else "halo"]) + (255,)
            lavado[(x, y)] = min(lavado.get((x, y), 1), 0.6 if no_miolo else 0.82)
            c = (DENSO if no_miolo else RALO)[y % 8][x % 8]
            if c != ".":
                px[x, y] = COR[c] + (255,)
                lavado[(x, y)] = min(lavado.get((x, y), 1), 0.55 if c == "c" else 0.3)
    for nome, cx, cy, esp in COLONIAS:
        for j, linha in enumerate(MOFO[nome]):
            for i, c in enumerate(linha[::-1] if esp else linha):
                x, y = cx + i, cy + j
                if c == "." or not (0 <= x < W and 0 <= y < H) or px[x, y][3] == 0:
                    continue
                px[x, y] = COR[c] + (255,)
                lavado[(x, y)] = min(lavado.get((x, y), 1), 0.55 if c == "c" else 0.25)

    im.save(P / "livro-capela.png")

    # as máscaras do bloco de texto de cada página, na escala da tela
    areas = json.loads((P / "areas.json").read_text(encoding="utf-8"))
    capela = json.loads(json.dumps(areas["a2"]))
    capela["mascaras"] = {}
    for lado, r in capela["reguas"].items():
        x0, y0, x1, y1 = r["caixa"]
        m = Image.new("LA", (x1 - x0, y1 - y0), (255, 255))
        for y in range(y0, y1):
            for x in range(x0, x1):
                m.putpixel((x - x0, y - y0), (255, round(255 * lavado.get((x, y), 1))))
        m = m.resize((m.width * ESCALA, m.height * ESCALA), Image.NEAREST)
        nome = f"mascara-capela-{lado}.png"
        m.save(P / nome)
        capela["mascaras"][lado] = nome
    areas["capela"] = capela
    (P / "areas.json").write_text(json.dumps(areas, indent=1), encoding="utf-8")
    print("livro-capela.png", im.size, {k: v for k, v in capela["mascaras"].items()})


if __name__ == "__main__":
    main()
