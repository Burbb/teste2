"""O ferreiro da forja H, pose a pose, no estilo das figuras do jogo (o mercador, a Ilse): cada material em três tons
chapados (a luz do lado da fornalha, o meio, a sombra do outro lado), sem contorno, o olho de um pixel escuro, a barba
em dois ou três tons. O mesmo homem da F e da G: careca, gordo e forte, a barba ruiva que afunila numa trança com a
presilha, o avental de couro, as mãos simples.

A animação é do corpo inteiro: cada pose é redesenhada a partir dos apoios, que não se mexem (as botas no chão; a luva
fechada na tenaz, que prende a espiga da espada na bigorna). O resto se acomoda a eles: no golpe o quadril desce
dobrando os joelhos, o tronco inclina para a frente, a barriga achata e alarga, a cabeça e a barba vão junto e a
trança balança; no alto as pernas estendem e o peito sobe e recua; o cotovelo do braço da tenaz dobra ou estica para
a mão ficar onde está. As coxas e as canelas vão do quadril ao joelho e ao tornozelo em cada pose, sem emenda.

`POSES` dá, por pose: `ombro` (o deslocamento dos ombros e do peito, x e y), `quadril` (quanto o quadril desce),
`cabeca` (o deslocamento da cabeça além dos ombros), `barriga` (achatar: 1), `tranca` (o balanço da ponta da trança),
e o braço do martelo (`cotovelo`, `punho`) com o martelo (`cabo`: a ponta de baixo; `cabeca_m`: o centro da cabeça)."""
import math

from tela_h2 import Tela

QW, QH = 320, 96
CONTATO = (141, 58)  # onde a face do martelo encosta na lâmina (as faíscas nascem aqui)

COR = {
    # a pele (as do mercador, um pouco mais quentes pela fornalha)
    "peleLuz": "#d89c6e", "pele": "#b47852", "peleSombra": "#7e5034", "peleEscura": "#5a3622",
    # a barba ruiva
    "barbaLuz": "#c86a32", "barba": "#9a4624", "barbaSombra": "#682c16",
    "olho": "#120c08", "sobrancelha": "#682c16",
    # o avental de couro
    "aventalLuz": "#7c5638", "avental": "#5a3e28", "aventalSombra": "#3e2a1a",
    # a braçadeira, a luva e as botas
    "couroLuz": "#6e4c30", "couro": "#4e3420", "couroSombra": "#34220f",
    # a túnica das costas e a calça
    "panoLuz": "#555a6a", "pano": "#3e4250", "panoSombra": "#2c2f3a",
    # a presilha e o martelo
    "ferroBrilho": "#c8cad0", "ferroLuz": "#9a9ca6", "ferro": "#6a6c74", "ferroSombra": "#45474e",
    "madeiraLuz": "#8a6a44", "madeira": "#6a4e30",
}
# a luz vem da esquerda e de cima (a fornalha)
LX, LY = -0.85, -0.5


class Figura:
    """Os pixels da figura, por cima uns dos outros na ordem em que as partes entram."""

    def __init__(self):
        self.px = {}

    def p(self, x, y, cor):
        if cor:
            self.px[(int(x), int(y))] = COR.get(cor, cor)

    def tons(self, base):
        return base + "Luz", base, base + "Sombra"

    def capsula(self, a, b, r, base, luz_lim=0.35, sombra_lim=-0.3):
        """Um membro de a até b (as pontas redondas), em três tons pelo lado virado para a luz."""
        luz, meio, sombra = self.tons(base)
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy or 1
        for y in range(int(min(ay, by) - r) - 1, int(max(ay, by) + r) + 2):
            for x in range(int(min(ax, bx) - r) - 1, int(max(ax, bx) + r) + 2):
                cx, cy = x + 0.5, y + 0.5
                t = max(0, min(1, ((cx - ax) * dx + (cy - ay) * dy) / l2))
                ox, oy = cx - (ax + t * dx), cy - (ay + t * dy)
                d = math.hypot(ox, oy)
                if d <= r:
                    s = (ox * LX + oy * LY) / r
                    self.p(x, y, luz if s > luz_lim else sombra if s < sombra_lim else meio)

    def afunilado(self, a, b, ra, rb, base, luz_lim=0.35, sombra_lim=-0.3):
        """Um membro que afina de a (raio ra) até b (raio rb): a coxa e a canela."""
        luz, meio, sombra = self.tons(base)
        (ax, ay), (bx, by) = a, b
        dx, dy = bx - ax, by - ay
        l2 = dx * dx + dy * dy or 1
        r = max(ra, rb)
        for y in range(int(min(ay, by) - r) - 1, int(max(ay, by) + r) + 2):
            for x in range(int(min(ax, bx) - r) - 1, int(max(ax, bx) + r) + 2):
                cx, cy = x + 0.5, y + 0.5
                t = max(0, min(1, ((cx - ax) * dx + (cy - ay) * dy) / l2))
                rr = ra + (rb - ra) * t
                ox, oy = cx - (ax + t * dx), cy - (ay + t * dy)
                if math.hypot(ox, oy) <= rr:
                    sv = (ox * LX + oy * LY) / rr
                    self.p(x, y, luz if sv > luz_lim else sombra if sv < sombra_lim else meio)

    def elipse(self, cx, cy, rx, ry, base, luz_lim=0.4, sombra_lim=-0.25):
        luz, meio, sombra = self.tons(base)
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                ox, oy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if ox * ox + oy * oy <= 1:
                    s = ox * LX + oy * LY
                    self.p(x, y, luz if s > luz_lim else sombra if s < sombra_lim else meio)

    def poligono(self, pts, base, luz_px=2, sombra_px=3, sombra_cor=None):
        """Um polígono com a faixa de luz na borda esquerda de cada linha e a de sombra na direita."""
        luz, meio, sombra = self.tons(base)
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            cy = y + 0.5
            xs = []
            for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
                if (ay <= cy < by) or (by <= cy < ay):
                    xs.append(ax + (cy - ay) * (bx - ax) / (by - ay))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                x0, x1 = int(math.ceil(a - 0.5)), int(math.floor(b - 0.5))
                for x in range(x0, x1 + 1):
                    self.p(x, y, luz if x < x0 + luz_px else (sombra_cor or sombra) if x > x1 - sombra_px else meio)

    def grade(self, x0, y0, linhas, pal):
        for dy, l in enumerate(linhas):
            for dx, ch in enumerate(l):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])

    def tela(self):
        t = Tela(QW, QH)
        for (x, y), c in self.px.items():
            t.px(x, y, c)
        return t


# ---------------------------------------------------------------- as poses
POSES = {
    "repouso": {"ombro": (0, 0), "quadril": 0, "cabeca": (0, 0), "barriga": 0, "tranca": 0,
                "cotovelo": (159, 48), "punho": (154, 53.5), "cabo": (161, 53.5), "cabeca_m": (141.5, 53.5)},
    "sobe1": {"ombro": (0, -1), "quadril": 0, "cabeca": (0, 0), "barriga": 0, "tranca": 0,
              "cotovelo": (158, 47), "punho": (151.5, 43.5), "cabo": (156, 49), "cabeca_m": (145, 34.8)},
    "sobe2": {"ombro": (1, -2), "quadril": -1, "cabeca": (0, -1), "barriga": 0, "tranca": 1,
              "cotovelo": (150, 42), "punho": (150.5, 34.5), "cabo": (151.5, 41), "cabeca_m": (150.2, 25)},
    "alto": {"ombro": (1, -2), "quadril": -1, "cabeca": (1, -1), "barriga": 0, "tranca": 1,
             "cotovelo": (151, 38), "punho": (153.5, 29.5), "cabo": (147.5, 35.8), "cabeca_m": (161.4, 22.4)},
    "desce": {"ombro": (-1, 0), "quadril": 0, "cabeca": (0, 0), "barriga": 0, "tranca": 0, "rastro": True,
              "cotovelo": (156, 46), "punho": (149.5, 42.5), "cabo": (156, 47), "cabeca_m": (141, 36)},
    "golpe": {"ombro": (-2, 2), "quadril": 1, "cabeca": (-1, 1), "barriga": 1, "tranca": -1, "golpe": True,
              "cotovelo": (158, 49), "punho": (154, 53.5), "cabo": (161, 53.5), "cabeca_m": (141.5, 53.5)},
    "volta": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-1, 1), "barriga": 1, "tranca": -2,
              "cotovelo": (158, 47), "punho": (154, 50.5), "cabo": (161, 50.5), "cabeca_m": (141.6, 50)},
    "ajuste": {"ombro": (-1, 1), "quadril": 0, "cabeca": (-1, 1), "barriga": 0, "tranca": 0, "vira": True,
               "cotovelo": (159, 48), "punho": (154, 53.5), "cabo": (161, 53.5), "cabeca_m": (141.5, 53.5)},
}

# os apoios (não se mexem): as botas no chão e a luva na tenaz
BOTA_F, BOTA_T = (155, 164), (177, 186)       # x de cada bota (a da frente fica ao lado do toco, sem cobri-lo)
CHAO = 86                                     # a sola
TORNOZELO_F, TORNOZELO_T = (160.5, 81), (181.5, 81)
MAO = (166, 58.5)                             # a luva fechada nas hastes da tenaz
TENAZ = (148, 162, 59)                        # das garras na espiga até dentro da luva


# ---------------------------------------------------------------- a cabeça e a barba (à mão, no estilo do mercador)
# A cabeça careca de três quartos, virada para a espada: a luz na testa e na frente do rosto, a sobrancelha pesada,
# o olho de um pixel, o nariz, a orelha do lado da sombra; a barba nasce nas bochechas e no queixo, mais larga que o
# rosto, e afunila até a trança (que vem à parte, para balançar). O ponto (0, 0) da grade é o alto da testa.
CABECA = [
    "....LLLss.....",
    "..LLLLssssd...",
    ".LLLLsssssdd..",
    ".LLLssssssddd.",
    "LLLwwwsssdEdd.",
    "LLsdessssdEd..",
    "nLssssssddd...",
    "LsHBssssbBd...",
    ".HHBBBsBBBbb..",
    "HBHBBBBBBbbb..",
    "HBHBBBBBBBbb..",
    ".HBHBBBBBBbb..",
    ".HBHBBBBBbb...",
    "..HBHBBBBbb...",
    "...HBHBBbb....",
    "....HBBbb.....",
]
PAL_CABECA = {"L": "peleLuz", "s": "pele", "d": "peleSombra", "D": "peleEscura", "w": "sobrancelha", "e": "olho",
              "n": "peleSombra", "E": "peleEscura", "H": "barbaLuz", "B": "barba", "b": "barbaSombra"}
TRANCA = [  # a trança, a presilha e a ponta solta
    ".HBb.",
    ".BHb.",
    ".HBb.",
    "FfgG.",
    ".HBb.",
    "HBBbb",
    ".H.b.",
]
PAL_TRANCA = {"H": "barbaLuz", "B": "barba", "b": "barbaSombra", "F": "ferroBrilho", "f": "ferroLuz", "g": "ferro",
              "G": "ferroSombra"}


def desenhar_martelo(f, cabo, cabeca):
    """O cabo de madeira e a cabeça de ferro (9 × 5) atravessada, a face para a luz mais clara (sem contorno)."""
    (bx, by), (hx, hy) = cabo, cabeca
    ux, uy = hx - bx, hy - by
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    vx, vy = -uy, ux
    i = 0.0
    while i <= n - 2.5:
        f.p(math.floor(bx + ux * i), math.floor(by + uy * i), "madeiraLuz" if int(i) % 5 else "madeira")
        i += 0.5
    for x in range(int(hx - 7), int(hx + 8)):
        for y in range(int(hy - 7), int(hy + 8)):
            ox, oy = x + 0.5 - hx, y + 0.5 - hy
            s, u = ox * vx + oy * vy, ox * ux + oy * uy
            if abs(s) <= 4.5 and abs(u) <= 2.5:
                if abs(s) > 3.4:
                    nx, ny = (vx, vy) if s > 0 else (-vx, -vy)
                else:
                    nx, ny = (ux, uy) if u > 0 else (-ux, -uy)
                d = nx * LX + ny * LY
                f.p(x, y, "ferroBrilho" if d > 0.5 else "ferroLuz" if d > 0.1 else "ferro" if d > -0.4 else "ferroSombra")


def rastro(f):
    for i, (x, y) in enumerate([(160, 18), (156, 17), (152, 18), (148, 21), (145, 25), (143, 29)]):
        f.p(x, y, "ferro" if i < 3 else "ferroLuz")


def tenaz(f, virada=False):
    """A tenaz: as hastes das garras na espiga (paradas) até dentro da luva; a luva fecha por cima e por baixo."""
    x0, x1, y = TENAZ
    for x in range(x0 + 2, x1 + 1):
        f.p(x, y, "ferroLuz" if x % 4 else "ferro")
        f.p(x, y + 1, "ferroSombra")
    for dy in range(-1, 3):
        f.p(x0 + 1, y + dy, "ferro" if dy <= 0 else "ferroSombra")
        f.p(x0, y + dy, "ferroSombra")


def figura(pose, quadro=0, virada=False):
    p = POSES[pose]
    sx, sy = p["ombro"]
    hq = p["quadril"]
    cx_, cy_ = p["cabeca"]
    f = Figura()
    # 1. o braço do martelo (do lado de lá): o ombro atrás da barba, o cotovelo, o punho; o martelo
    if p.get("rastro"):
        rastro(f)
    desenhar_martelo(f, p["cabo"], p["cabeca_m"])
    ombro_l = (165 + sx, 44 + sy)
    f.capsula(ombro_l, p["cotovelo"], 3.6, "pele")
    f.capsula(p["cotovelo"], p["punho"], 3.0, "pele")
    # a braçadeira no pulso: o trecho do antebraço junto do punho
    (ex, ey), (px_, py_) = p["cotovelo"], p["punho"]
    f.capsula((px_ + (ex - px_) * 0.25, py_ + (ey - py_) * 0.25), (px_ + (ex - px_) * 0.55, py_ + (ey - py_) * 0.55), 3.1, "couro")
    f.elipse(px_, py_, 3.3, 3.0, "pele")
    # 2. as pernas, firmes e abertas: a coxa do quadril (que desce no golpe) ao joelho (para fora e, quando dobra, para a
    # frente), a canela afinando até o tornozelo (parado), a calça enfiada no cano da bota
    dobra = max(0, hq)
    quadril_f, quadril_t = (164, 72 + hq), (181, 68 + hq)
    joelho_f, joelho_t = (158.5 - dobra, 77.5 + hq * 0.5), (184 - dobra * 0.5, 77 + hq * 0.5)
    pernas = [(quadril_t, joelho_t, TORNOZELO_T, BOTA_T), (quadril_f, joelho_f, TORNOZELO_F, BOTA_F)]
    for q, j_, tz, (x0, x1) in pernas:
        f.afunilado(q, j_, 5.2 if q is quadril_t else 4.6, 3.8, "pano")
        f.afunilado(j_, tz, 3.9, 2.6, "pano")
        # a bota: o cano com a borda dobrada (a calça entra nele), o peito do pé, a ponta para a frente e a sola
        f.poligono([(tz[0] - 3, 80), (tz[0] + 3.5, 80), (x1 - 0.5, 83), (x1, CHAO), (x0, CHAO), (x0, 84.5), (tz[0] - 3, 82)],
                   "couro", luz_px=2, sombra_px=2)
        for x in range(int(tz[0] - 3), int(tz[0] + 4)):
            f.p(x, 80, "couroLuz")
        for x in range(x0, x1 + 1):
            f.p(x, CHAO, "couroSombra")
    # 3. o tronco: as costas (a túnica escura) do ombro ao quadril
    f.poligono([(164 + sx, 42 + sy), (185 + sx, 40 + sy), (189 + sx * 0.5, 55 + sy * 0.5), (187.5, 62 + hq),
                (185, 66 + hq), (167, 67 + hq), (163 + sx * 0.5, 57 + sy * 0.5)], "pano", luz_px=0, sombra_px=3)
    for x in range(176, 189):
        f.p(x, 65 + hq, "couroSombra")
    # 4. o avental: o peitilho, a barriga redonda (achata e alarga no golpe) e a saia até a barra
    rx, ry = 9.5 + p["barriga"], 10.5 - p["barriga"]
    bcx, bcy = 165 + sx * 0.6, 63 + (sy + hq) * 0.5 + p["barriga"]
    f.poligono([(161 + sx, 44 + sy), (173 + sx, 43 + sy), (178.5 + sx * 0.4, 53 + sy * 0.6), (179, 70 + hq),
                (178, 77 + hq), (159, 78 + hq), (157, 74 + hq), (bcx - 6, bcy - 6)], "avental", luz_px=2, sombra_px=4)
    f.elipse(bcx, bcy, rx, ry, "avental", luz_lim=0.45, sombra_lim=-0.2)
    for x0, y0 in ((166, bcy + 4), (172, bcy + 2)):  # as dobras do couro, da barriga para a barra
        for y in range(int(y0), 77 + hq):
            f.p(x0 + (y - y0) // 6, y, "aventalSombra")
    for x in range(159, 178):  # a barra
        f.p(x, 77 + hq, "aventalSombra")
    # a amarra nas costas: o laço e as pontas
    f.p(182 + sx // 2, 58 + (sy + hq) // 2, "couroLuz")
    f.p(183 + sx // 2, 58 + (sy + hq) // 2, "couro")
    for y in range(59, 64):
        f.p(182 + sx // 2, y + (sy + hq) // 2, "couro" if y % 2 else "couroLuz")
    # 5. o braço de perto, nu: o ombro, o bíceps até o cotovelo (que dobra para a mão ficar), a braçadeira e a luva
    ombro_p = (180 + sx, 45 + sy)
    cotovelo_p = (181 + sx * 0.5, 55 + sy * 0.4 + hq * 0.3)
    # o trapézio: do pescoço ao ombro, sem o ombro subir como uma bola
    f.poligono([(169 + sx, 41 + sy), (177 + sx, 39 + sy), (184 + sx, 41 + sy), (185 + sx, 46 + sy), (170 + sx, 47 + sy)],
               "pele", luz_px=1, sombra_px=2)
    f.elipse(ombro_p[0], ombro_p[1] + 1, 5.6, 5.4, "pele", luz_lim=0.62, sombra_lim=-0.12)
    f.capsula((ombro_p[0] + 0.5, ombro_p[1] + 4), cotovelo_p, 4.0, "pele", luz_lim=0.55, sombra_lim=-0.1)
    mao = (MAO[0], MAO[1] - (0 if not virada else 0))
    f.capsula(cotovelo_p, mao, 3.3, "couro")
    tenaz(f, virada)
    f.elipse(mao[0], mao[1], 3.6, 3.5, "couro", luz_lim=0.3, sombra_lim=-0.4)
    for x in range(int(mao[0]) - 3, int(mao[0]) + 1):  # os dedos fechados em volta das hastes
        f.p(x, int(mao[1]) + 1, "couroSombra")
    # a alça do avental, do peitilho até atrás do pescoço
    for i in range(6):
        f.p(171 + sx + i // 3, 43 + sy - i, "aventalLuz" if i % 2 else "avental")
    # 6. a cabeça e a barba, e a trança com a presilha (a ponta balança)
    hx, hy = 159 + sx + cx_, 31 + sy + cy_
    f.grade(hx, hy, CABECA, PAL_CABECA)
    f.grade(hx + 3 + p["tranca"] // 2, hy + len(CABECA), TRANCA[:4], PAL_TRANCA)
    f.grade(hx + 3 + p["tranca"], hy + len(CABECA) + 4, TRANCA[4:], PAL_TRANCA)
    return f.tela()
