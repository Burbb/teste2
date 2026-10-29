"""Quem está na taverna, candidata A: o taverneiro atrás do balcão, Morel no canto (enquanto não foi recrutado), quem
se aquece junto do fogo e três mesas ocupadas, no estilo das figuras do jogo (sem contorno, três tons por material, o
olho de um pixel, as mãos simples). Os fregueses não têm nome nem fala: ocupam a sala.

**A construção de cada figura** (as lições do templo e da curandeira):
- o tronco e a cabeça andam como um bloco (a inclinação); o quadril fica no assento e os pés no piso;
- os braços têm comprimento fixo (o cotovelo sai da conta; a mão fora do alcance é um erro, não um braço esticado);
- cada figura tem duas camadas: o corpo (atrás da mesa ou do balcão) e as mãos com o que seguram (na frente); entre as
  duas, a tela desenha a mesa e o balcão (`desenho.frente_moveis`), e ninguém atravessa o tampo;
- as medidas saem da régua do lugar (`desenho.METRO` e `k`): quem está mais perto é maior, na mesma conta do piso.

**As atividades** (skill arte-cenas-fenda, 5b), cada uma com pausas e um ciclo de duração própria, para ninguém
gesticular em sincronia: o taverneiro limpa uma caneca, olha contra a luz e a pousa; Morel come o ensopado sozinho, de
costas para a parede, sem levantar os olhos do prato; quem está junto do fogo estende as mãos, esfrega, se ajeita no banco;
na mesa da esquerda, um bebe e a outra come; na do meio, dois jogam, um de cada vez; na da direita, um conta e o outro
escuta, balança a cabeça e responde."""
import math

from desenho import METRO, Pincel, QH, QW, Tela, k

# ---------------------------------------------------------------- utilidades
def capsula(t, a, b, r, cor, luz, sombra):
    """Um pedaço de braço ou perna como forma cheia (a mesma da curandeira e do templo)."""
    (ax, ay), (bx, by) = a, b
    vx, vy = bx - ax, by - ay
    n2 = vx * vx + vy * vy or 1
    cols = {}
    for y in range(int(min(ay, by) - r - 1), int(max(ay, by) + r + 2)):
        for x in range(int(min(ax, bx) - r - 1), int(max(ax, bx) + r + 2)):
            u = max(0.0, min(1.0, ((x - ax) * vx + (y - ay) * vy) / n2))
            if math.hypot(x - (ax + u * vx), y - (ay + u * vy)) <= r:
                cols.setdefault(x, []).append(y)
    for x, ys in cols.items():
        ys.sort()
        for y in ys:
            t.px(x, y, cor)
        if len(ys) >= 3:
            t.px(x, ys[0], luz)
            t.px(x, ys[-1], sombra)


def cotovelo(ombro, mao, l1, l2, para_baixo=True):
    (sx, sy), (hx, hy) = ombro, mao
    d = math.hypot(hx - sx, hy - sy) or 0.01
    assert d <= l1 + l2 + 0.05, f"a mão em {mao} não alcança do ombro {ombro} ({d:.1f} > {l1 + l2:.1f})"
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    ux, uy = (hx - sx) / d, (hy - sy) / d
    px_, py_ = sx + ux * a, sy + uy * a
    c1, c2 = (px_ - uy * h, py_ + ux * h), (px_ + uy * h, py_ - ux * h)
    return (c1 if c1[1] >= c2[1] else c2) if para_baixo else (c1 if c1[0] <= c2[0] else c2)


PELES = [("#c49072", "#dcae90", "#946850"), ("#b07858", "#cc9676", "#82543a"), ("#8a5a3c", "#a87050", "#5e3a24")]
ROUPAS = {
    "verde": ("#3e4a34", "#526046", "#2a3224"), "marrom": ("#5a3e2a", "#765236", "#3a2818"),
    "vinho": ("#5a2a26", "#743832", "#3c1a18"), "azul": ("#34404e", "#465466", "#232b36"),
    "cinza": ("#4a4844", "#605e58", "#33312e"), "ocre": ("#6a5230", "#866a40", "#47361f"),
    "linho": ("#8a8270", "#a29a86", "#666050"),
}
CALCA = ("#4a3c30", "#5e4c3c", "#30261e")    # um pouco mais clara que o piso: as pernas aparecem
CABELOS = {"castanho": ("#5a3820", "#76502e", "#3a2414"), "preto": ("#2a2420", "#3e3630", "#1a1612"),
           "grisalho": ("#7e7a74", "#9a968e", "#56524c"), "ruivo": ("#7a3e1e", "#9a5428", "#52280f"),
           "loiro": ("#9a804a", "#b89c60", "#6e5a30")}

# as cabeças de perfil, voltadas para a direita (o nariz na última coluna), na escala das mesas da frente (6 linhas);
# K o cabelo, k a sombra dele, s a pele, S a sombra, l a luz, e o olho, B a barba, L o lenço, H o capuz
CABECAS = {
    "curto": ["..KKK.", ".KKKKs", "KKKsls", "KKsses", ".KsSss", "..sSs."],
    "barba": ["..KKK.", ".KKKKs", "KKKsls", "KKsses", ".KBBBs", "..BBB."],
    "careca": ["..sss.", ".slsss", "KKssls", "KKsses", ".KBBBs", "..BBB."],
    "lenco": ["..LLL.", ".LLLLs", "LLLsls", "LLsses", ".LsSss", "..sSs."],
    "capuz": ["..HHH.", ".HHHHH", "HHHsls", "HHsses", "HHsSss", ".HHSs."],
}
# na escala do meio da sala (5 linhas): quem está junto do fogo
CABECAS_MEIO = {"curto": [".KKK.", "KKKKs", "KKses", ".KSss", "..Ss."], "capuz": [".HHH.", "HHHHs", "HHses", "HHSss", ".HSs."]}


def paleta_cabeca(c):
    pe = c["pele"]
    cab = CABELOS[c.get("cabelo", "castanho")]
    pano = ROUPAS[c.get("pano", "linho")]
    return {"K": cab[0], "k": cab[2], "B": cab[2], "s": pe[0], "S": pe[2], "l": pe[1], "e": "#1a1210",
            "L": pano[1], "H": pano[0]}


# ---------------------------------------------------------------- a figura sentada de perfil
class Sentado:
    """Alguém sentado num banquinho, de perfil (voltado para a direita; `lado` -1 espelha), com o quadril em `quadril`
    e os pés no piso em `pe`. A régua: m = METRO · k(pe) pixels por metro."""

    def __init__(self, nome, quadril_x, pe, lado, cores, cabeca, escala=None):
        self.nome, self.lado, self.cores, self.cabeca = nome, lado, cores, cabeca
        self.m = escala or METRO * k(pe)
        self.pe = pe
        m = self.m
        self.assento = round(pe - 0.45 * m)                # o tampo do banquinho
        self.hx, self.hy = quadril_x, self.assento - 1     # o quadril
        self.tronco = round(0.6 * m)                       # do quadril ao ombro (sentado, ~0,3 m acima do tampo)
        self.largura = max(4, round(0.24 * m))
        self.braco = (0.31 * m, 0.31 * m)
        self.coxa, self.canela = 0.42 * m, pe - self.assento

    # o desenho local é voltado para a direita; X() espelha quando a figura olha para a esquerda
    # a pose (`tronco`, `cabeca`) também é local: +x é sempre para a frente, na direção em que a figura olha
    def X(self, x):
        return self.hx + self.lado * (x - self.hx)

    def ombro(self, pose):
        dx, dy = pose.get("tronco", (0, 0))
        return (self.hx + 1 + dx, self.hy - self.tronco + 2 + dy)

    def camadas(self, pose):
        """(corpo, mãos): duas Telas do tamanho do quadro."""
        corpo, maos = Tela(QW, QH), Tela(QW, QH)
        self._corpo(corpo, pose)
        self._maos(maos, pose)
        return corpo, maos

    def _px(self, t):
        """Um pincel que desenha no espaço local (voltado para a direita) e espelha no quadril quando `lado` é -1."""
        base = Pincel(t)
        hx, lado = self.hx, self.lado

        def f(x, y, w=1, h=1, cor=None):
            if lado < 0:
                x = 2 * hx - x - w + 1
            base(x, y, w, h, cor)
        return f

    def _corpo(self, t, pose):
        px = self._px(t)
        c = self.cores
        ro, ro_l, ro_e = ROUPAS[c["roupa"]]
        ca, ca_l, ca_e = CALCA
        dx, dy = pose.get("tronco", (0, 0))
        # o banquinho: o tampo e os pés, no piso
        px(self.hx - 3, self.assento, 7, 1, "madeiraLuz")
        px(self.hx - 3, self.assento + 1, 7, 1, "madeiraMeio")
        for xx in (self.hx - 2, self.hx + 2):
            px(xx, self.assento + 2, 1, self.pe - self.assento - 2, "madeira")
        px(self.hx - 3, self.pe, 7, 1, "contato")
        # as pernas: a coxa para a frente no assento, a canela até o piso, o pé
        joelho = self.hx + round(self.coxa)
        px(self.hx - 1, self.hy - 1, joelho - self.hx + 2, 3, ca)
        px(self.hx - 1, self.hy - 1, joelho - self.hx + 2, 1, ca_l)
        px(joelho - 1, self.hy, 3, self.pe - self.hy - 1, ca)
        px(joelho + 1, self.hy, 1, self.pe - self.hy - 1, ca_e)
        px(joelho - 1, self.pe - 1, 4, 1, "#2a1c12")        # o sapato
        # o tronco, em bloco: do quadril ao ombro, um pouco mais largo no peito
        topo = self.hy - self.tronco + dy
        for i, y in enumerate(range(topo, self.hy + 1)):
            larg = self.largura + (1 if 2 <= i <= self.tronco - 3 else 0)
            d = dx if self.hy - y >= 3 else round(dx * (self.hy - y) / 3)  # o peito em bloco; só a cintura acomoda
            x0 = self.hx - larg // 2 + d
            px(x0, y, larg, 1, ro)
            px(x0 + larg - 1, y, 1, 1, ro_l)                  # a frente (a luz vem da mesa e das velas)
            px(x0, y, 1, 1, ro_e)
        px(self.hx - self.largura // 2, self.hy - 2, self.largura + 1, 1, "#2a1c12")  # o cinto
        # a cabeça
        cab = CABECAS[self.cabeca] if self.m > 18 else CABECAS_MEIO[self.cabeca]
        cx, cy = pose.get("cabeca", (0, 0))
        w = len(cab[0])
        hx0 = self.hx - w // 2 + 1 + dx + cx
        hy0 = topo - len(cab) + cy
        pal = paleta_cabeca(c)
        for yy, linha in enumerate(cab):
            for xx, ch in enumerate(linha):
                if ch in pal:
                    px(hx0 + xx, hy0 + yy, 1, 1, pal[ch])

    def _maos(self, t, pose):
        """Os dois braços e o que as mãos seguram: o de longe (mais escuro) primeiro, o de perto por cima."""
        px = self._px(t)
        pe_, pe_l, pe_e = self.cores["pele"]
        ro, ro_l, ro_e = ROUPAS[self.cores["roupa"]]
        sx, sy = self.ombro(pose)
        loc = lambda p: (self.hx + self.lado * (p[0] - self.hx), p[1])  # o alvo, do mundo para o espaço local
        for qual, cor, luz, sombra, dsx in (("longe", ro_e, ro, ro_e, -1), ("perto", ro, ro_l, ro_e, 0)):
            alvo = pose.get(qual)
            if not alvo:
                continue
            hx, hy = loc(alvo)
            ombro = (sx + dsx, sy)
            co = cotovelo(ombro, (hx + 0.5, hy + 0.5), *self.braco)
            tl = Tela(QW, QH)
            capsula(tl, ombro, co, 1.0, cor, luz, sombra)
            capsula(tl, co, (hx + 0.5, hy + 0.5), 0.9, cor if qual == "longe" else ro, luz, sombra)
            self._copiar(tl, t)
            px(hx, hy, 2, 2, pe_e if qual == "longe" else pe_)
            if qual == "perto":
                px(hx, hy, 1, 1, pe_l)
        for obj in pose.get("objetos", []):
            desenhar_objeto(px, obj, loc)

    def _copiar(self, src, dst):
        """Copia os pixels de uma Tela local para a de saída, espelhando quando preciso."""
        im = src.imagem()
        a = im.load()
        for y in range(QH):
            for x in range(QW):
                if a[x, y][3]:
                    xx = x if self.lado > 0 else 2 * self.hx - x
                    if 0 <= xx < QW:
                        dst.px(xx, y, "#%02x%02x%02x" % a[x, y][:3])


def desenhar_objeto(px, obj, loc):
    """O que está na mão ou no tampo: a caneca (de estanho), o pão, a peça do jogo, a colher, o pano."""
    tipo, (x, y) = obj[0], loc(obj[1])
    x, y = round(x), round(y)
    if tipo == "caneca":
        px(x, y - 3, 3, 3, "estanho"); px(x, y - 3, 1, 3, "estanhoLuz"); px(x + 3, y - 2, 1, 1, "estanhoEsc")
    elif tipo == "caneca_boca":  # inclinada na boca
        px(x, y - 2, 3, 2, "estanho"); px(x, y - 2, 1, 2, "estanhoLuz")
    elif tipo == "pao":
        px(x, y - 2, 4, 2, "pao"); px(x + 1, y - 2, 2, 1, "paoLuz")
    elif tipo == "peca":
        px(x, y - 2, 1, 2, "linhoLuz")
    elif tipo == "colher":
        px(x, y, 1, 1, "estanhoLuz")
    elif tipo == "pano":
        px(x, y, 2, 2, "linhoLuz")
    elif tipo == "tigela":  # a tigela de barro com o ensopado
        px(x, y - 2, 5, 1, "#6a3a1e"); px(x + 1, y - 2, 3, 1, "#8a5a30"); px(x, y - 1, 5, 1, "barro")
        px(x + 1, y, 3, 1, "barro")


# ---------------------------------------------------------------- as poses e as rotinas de cada um
def mesa_y(pe, alto=0.75):
    return round(pe - alto * METRO * k(pe))


PE = 86                 # onde pisam as mesas da frente
TAMPO = mesa_y(PE)      # o tampo delas

ELENCO = []


def pessoa(sentado, poses, rotina):
    ELENCO.append({"fig": sentado, "poses": poses, "rotina": rotina})


# a mesa da esquerda (x 40-88): um homem bebe (à esquerda, voltado para a mesa) e uma mulher come (à direita)
_a = Sentado("esq_a", 33, PE, 1, {"pele": PELES[1], "roupa": "vinho", "cabelo": "castanho"}, "barba")
_cx = 44
pessoa(_a, {
    "apoia": {"perto": (_cx, TAMPO - 1), "longe": (_cx - 1, TAMPO), "objetos": [("caneca", (_cx + 1, TAMPO))]},
    "ergue": {"tronco": (0, 0), "perto": (_cx - 2, TAMPO - 5), "longe": (_cx - 1, TAMPO), "objetos": [("caneca", (_cx - 1, TAMPO - 5))]},
    "bebe": {"tronco": (-1, 0), "cabeca": (-1, -1), "perto": (_cx - 5, TAMPO - 10), "longe": (_cx - 1, TAMPO),
             "objetos": [("caneca_boca", (_cx - 4, TAMPO - 10))]},
    "desce": {"perto": (_cx - 2, TAMPO - 4), "longe": (_cx - 1, TAMPO), "objetos": [("caneca", (_cx - 1, TAMPO - 4))]},
}, [("apoia", 14), ("ergue", 2), ("bebe", 6), ("desce", 2), ("apoia", 20), ("ergue", 2), ("bebe", 4), ("desce", 2)])

_b = Sentado("esq_b", 95, PE, -1, {"pele": PELES[0], "roupa": "verde", "pano": "linho"}, "lenco")
_bx = 84
pessoa(_b, {
    "mesa": {"perto": (_bx, TAMPO - 1), "longe": (_bx + 1, TAMPO), "objetos": [("pao", (_bx - 3, TAMPO))]},
    "pega": {"tronco": (1, 0), "cabeca": (1, 0), "perto": (_bx - 2, TAMPO - 1), "longe": (_bx + 1, TAMPO), "objetos": [("pao", (_bx - 3, TAMPO))]},
    "come": {"cabeca": (0, 1), "perto": (_bx + 3, TAMPO - 8), "longe": (_bx + 1, TAMPO), "objetos": [("pao", (_bx + 2, TAMPO - 8))]},
    "ri": {"tronco": (-1, 0), "cabeca": (-1, -1), "perto": (_bx, TAMPO - 1), "longe": (_bx + 1, TAMPO), "objetos": [("pao", (_bx - 3, TAMPO))]},
}, [("mesa", 18), ("pega", 3), ("come", 8), ("mesa", 16), ("ri", 5), ("mesa", 20)])

# a mesa do meio (x 146-172, curta): dois jogam, um de cada vez; o tabuleiro no meio (na mesa, desenho.py)
_g1 = Sentado("meio_a", 143, PE, 1, {"pele": PELES[2], "roupa": "azul", "cabelo": "preto"}, "curto")
_g2 = Sentado("meio_b", 175, PE, -1, {"pele": PELES[0], "roupa": "ocre", "cabelo": "grisalho"}, "careca")
_tab = 159
pessoa(_g1, {
    "pensa": {"perto": (148, TAMPO - 1), "longe": (147, TAMPO)},
    "estende": {"tronco": (2, 1), "cabeca": (2, 1), "perto": (_tab - 4, TAMPO - 2), "longe": (147, TAMPO)},
    "move": {"tronco": (2, 1), "cabeca": (2, 1), "perto": (_tab - 2, TAMPO - 1), "longe": (147, TAMPO)},
    "queixo": {"tronco": (1, 0), "perto": (147, TAMPO - 9), "longe": (147, TAMPO)},
}, [("pensa", 6), ("estende", 2), ("move", 4), ("estende", 2), ("pensa", 14), ("queixo", 30), ("pensa", 6)])
pessoa(_g2, {
    "pensa": {"perto": (170, TAMPO - 1), "longe": (171, TAMPO)},
    "queixo": {"tronco": (1, 0), "perto": (171, TAMPO - 9), "longe": (171, TAMPO)},
    "estende": {"tronco": (2, 1), "cabeca": (2, 1), "perto": (_tab + 4, TAMPO - 2), "longe": (171, TAMPO)},
    "move": {"tronco": (2, 1), "cabeca": (2, 1), "perto": (_tab + 2, TAMPO - 1), "longe": (171, TAMPO)},
}, [("queixo", 30), ("pensa", 4), ("estende", 2), ("move", 4), ("estende", 2), ("pensa", 22)])

# a mesa da direita (x 216-264): um conta (à esquerda) e o outro escuta, balança a cabeça e responde
_c1 = Sentado("dir_a", 209, PE, 1, {"pele": PELES[1], "roupa": "marrom", "cabelo": "ruivo"}, "curto")
_c2 = Sentado("dir_b", 271, PE, -1, {"pele": PELES[1], "roupa": "cinza", "pano": "verde"}, "capuz")
pessoa(_c1, {
    "mesa": {"perto": (220, TAMPO - 1), "longe": (219, TAMPO), "objetos": [("caneca", (222, TAMPO))]},
    "conta": {"tronco": (1, 0), "perto": (222, TAMPO - 7), "longe": (219, TAMPO), "objetos": [("caneca", (224, TAMPO))]},
    "aponta": {"tronco": (1, -1), "cabeca": (1, -1), "perto": (222, TAMPO - 8), "longe": (219, TAMPO), "objetos": [("caneca", (224, TAMPO))]},
    "escuta": {"cabeca": (0, 1), "perto": (220, TAMPO - 1), "longe": (219, TAMPO), "objetos": [("caneca", (222, TAMPO))]},
}, [("conta", 5), ("aponta", 4), ("conta", 6), ("aponta", 3), ("mesa", 6), ("escuta", 24), ("mesa", 8)])
pessoa(_c2, {
    "escuta": {"perto": (260, TAMPO - 1), "longe": (261, TAMPO), "objetos": [("caneca", (257, TAMPO))]},
    "acena": {"cabeca": (0, 1), "perto": (260, TAMPO - 1), "longe": (261, TAMPO), "objetos": [("caneca", (257, TAMPO))]},
    "responde": {"tronco": (1, 0), "perto": (257, TAMPO - 7), "longe": (261, TAMPO), "objetos": [("caneca", (255, TAMPO))]},
}, [("escuta", 6), ("acena", 2), ("escuta", 4), ("acena", 2), ("escuta", 10), ("responde", 8), ("escuta", 4), ("responde", 6),
    ("escuta", 14)])

# junto do fogo: alguém num banquinho, voltado para a lareira, aquece as mãos e se ajeita
_f = Sentado("fogo", 188, 62, 1, {"pele": PELES[0], "roupa": "verde", "pano": "marrom"}, "capuz")
_fy = 62 - round(0.75 * _f.m)
pessoa(_f, {
    "aquece": {"tronco": (1, 0), "perto": (197, _fy), "longe": (196, _fy - 1)},
    "esfrega": {"tronco": (1, 0), "perto": (196, _fy + 1), "longe": (196, _fy - 1)},
    "ajeita": {"tronco": (-1, 0), "cabeca": (-1, 0), "perto": (191, _fy + 4), "longe": (190, _fy + 4)},
}, [("aquece", 16), ("esfrega", 2), ("aquece", 2), ("esfrega", 2), ("aquece", 24), ("ajeita", 10), ("aquece", 6)])


# ---------------------------------------------------------------- de frente: o taverneiro e Morel
class DeFrente:
    """Alguém de frente para a sala, atrás do balcão (o taverneiro) ou da mesa (Morel): a cabeça, os ombros e o tronco
    acima do móvel (o resto ele cobre), os braços com o comprimento fixo; o corpo como bloco."""

    def __init__(self, nome, cx, topo_cabeca, m, cores, cabeca, largura, tronco_h, braco):
        self.nome, self.cx, self.y0, self.m = nome, cx, topo_cabeca, m
        self.cores, self.cabeca, self.largura, self.tronco_h, self.braco = cores, cabeca, largura, tronco_h, braco

    def ombros(self, pose):
        dx, dy = pose.get("tronco", (0, 0))
        y = self.y0 + len(self.cabeca) + 1 + dy
        return (self.cx - self.largura // 2 + dx, y), (self.cx + self.largura // 2 + dx, y)

    def camadas(self, pose):
        corpo, maos = Tela(QW, QH), Tela(QW, QH)
        px, pm = Pincel(corpo), Pincel(maos)
        c = self.cores
        ro, ro_l, ro_e = c["roupa"]
        dx, dy = pose.get("tronco", (0, 0))
        topo = self.y0 + len(self.cabeca) + dy
        for i in range(self.tronco_h):                  # o tronco: os ombros caídos nas pontas
            y = topo + i
            larg = self.largura + 1 if i else self.largura - 1
            x0 = self.cx - larg // 2 + dx
            px(x0, y, larg, 1, ro)
            px(x0, y, 1, 1, ro_l)
            px(x0 + larg - 1, y, 1, 1, ro_e)
        for (x, y, w, h, cor) in c.get("detalhes", []):  # o avental, as placas da armadura
            px(self.cx + dx + x, topo + y, w, h, cor)
        cx_, cy_ = pose.get("cabeca", (0, 0))
        pal = {"K": c["cabelo"][0], "k": c["cabelo"][2], "s": c["pele"][0], "S": c["pele"][2], "l": c["pele"][1],
               "e": "#1a1210", "B": c["cabelo"][2], **c.get("pal", {})}
        w = len(self.cabeca[0])
        Pincel(corpo).grade(self.cx - w // 2 + dx + cx_, self.y0 + dy + cy_, self.cabeca, pal)
        # os braços: o de cima no tronco (corpo), o antebraço e a mão por cima do móvel (mãos)
        oe, od = self.ombros(pose)
        for ombro, alvo, lado in ((oe, pose["esq"], -1), (od, pose["dir"], 1)):
            co = cotovelo(ombro, (alvo[0] + 0.5, alvo[1] + 0.5), *self.braco, para_baixo=True)
            capsula(corpo, ombro, co, 1.1, ro, ro_l, ro_e)
            capsula(maos, co, (alvo[0] + 0.5, alvo[1] + 0.5), 0.9, ro, ro_l, ro_e)
            pm(alvo[0], alvo[1], 2, 2, c["pele"][0])
            pm(alvo[0], alvo[1], 1, 1, c["pele"][1])
        for obj in pose.get("objetos", []):
            desenhar_objeto(pm, obj, lambda p: p)
        return corpo, maos


# o taverneiro atrás do balcão (x 68-152, o tampo em 41): limpa a caneca, olha contra a luz, pousa e pega outra
_m_bal = METRO * k(56)
_tav = DeFrente("taverneiro", 108, 29, _m_bal, {
    "pele": PELES[0], "roupa": ("#4a3a2c", "#5e4a38", "#33271d"), "cabelo": CABELOS["castanho"],
    "detalhes": [(-2, 2, 5, 8, "#8a8270"), (-2, 2, 5, 1, "#a29a86")],   # o avental de linho
}, [".lsl.", "sssss", "seses", "sBBBs", ".BBB."], 7, 9, (4.2, 4.2))
pessoa(_tav, {
    "esfrega1": {"esq": (105, 38), "dir": (109, 37), "objetos": [("caneca", (105, 38)), ("pano", (109, 36))]},
    "esfrega2": {"esq": (105, 38), "dir": (108, 38), "objetos": [("caneca", (105, 38)), ("pano", (108, 37))]},
    "esfrega3": {"esq": (105, 38), "dir": (109, 39), "objetos": [("caneca", (105, 38)), ("pano", (109, 38))]},
    "olha": {"cabeca": (0, -1), "esq": (102, 32), "dir": (110, 38), "objetos": [("caneca", (101, 32)), ("pano", (110, 38))]},
    "pousa": {"tronco": (0, 1), "cabeca": (0, 1), "esq": (103, 40), "dir": (110, 39), "objetos": [("caneca", (103, 40)), ("pano", (110, 38))]},
}, [("esfrega1", 3), ("esfrega2", 3), ("esfrega3", 3), ("esfrega2", 3), ("esfrega1", 3), ("esfrega2", 3), ("esfrega3", 3),
    ("olha", 10), ("esfrega1", 3), ("esfrega2", 3), ("esfrega3", 3), ("pousa", 6), ("esfrega1", 18)])

# Morel no canto, debaixo da escada (a mesa de x 276-298, o tampo em 46): "come sozinho, de costas para a parede" e
# fala "sem levantar os olhos do prato" (eventos/comitiva.py), então a cabeça fica baixa, no ensopado. A figura segue
# a referência do jogo (retratos.js, MOREL_FIGURA): o cabelo e a barba castanhos, a cicatriz descendo da esquerda para
# a direita, a ombreira cinza num ombro e a pele no outro, o couro com a faixa vermelha no peito.
_m_canto = METRO * k(58)
_morel = DeFrente("morel", 287, 37, _m_canto, {
    "pele": ("#c09070", "#d8aa90", "#9a6c52"), "roupa": ("#6a4a30", "#7e5c3c", "#4a3220"), "cabelo": ("#6a4a2c", "", "#4e3420"),
    "pal": {"C": "#6a4a2c", "c": "#4e3420", "P": "#c09070", "p": "#9a6c52", "x": "#d8aa90", "b": "#5a3e2a", "B": "#3e2a1c"},
    "detalhes": [(-1, 2, 3, 7, "#8a3428"), (0, 2, 1, 7, "#5e241c"),                       # a faixa vermelha
                 (-5, 0, 3, 3, "#9a9ca4"), (-5, 0, 3, 1, "#c4c6cc"), (-5, 2, 3, 1, "#6e7078"),  # a ombreira
                 (2, 0, 3, 2, "#6a6058"), (2, 0, 3, 1, "#7a7064")],                     # a pele no ombro
}, [".CCcc.", "CPxPpc", "PePxep", "PPPpxp", ".bbBB."], 9, 8, (4.4, 4.4))   # o tronco acaba atrás do tampo
pessoa(_morel, {
    "come": {"cabeca": (0, 1), "esq": (283, 45), "dir": (289, 45), "objetos": [("tigela", (285, 46)), ("colher", (289, 44))]},
    "leva": {"cabeca": (0, 1), "esq": (283, 45), "dir": (289, 42), "objetos": [("tigela", (285, 46)), ("colher", (289, 41))]},
    "boca": {"cabeca": (0, 1), "esq": (283, 45), "dir": (288, 41), "objetos": [("tigela", (285, 46)), ("colher", (288, 40))]},
    "mastiga": {"esq": (283, 45), "dir": (290, 45), "objetos": [("tigela", (285, 46)), ("colher", (290, 44))]},
}, [("come", 6), ("leva", 2), ("boca", 4), ("leva", 2), ("come", 8), ("leva", 2), ("boca", 4), ("leva", 2), ("come", 14),
    ("mastiga", 12), ("come", 10)])


def quadros(item):
    """Os desenhos diferentes de uma pessoa (na ordem em que aparecem), a linha do tempo e a pose parada (a primeira)."""
    unicos, tempo = [], []
    for nome, n in item["rotina"]:
        if nome not in unicos:
            unicos.append(nome)
        tempo += [unicos.index(nome)] * n
    return unicos, tempo, 0
