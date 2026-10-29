"""O taverneiro da candidata G, parado, atrás do balcão: um homem gordo e forte, desconfiado, que limpa uma caneca com
um pano e olha de lado para quem chegou. No estilo das figuras do jogo (cada material em três tons chapados, a luz da
lareira pela esquerda, sem contorno, as mãos simples, sem dedos), na escala da câmera de perto (a cabeça com a barba
tem ~23 px; a régua no lugar dele é de ~80 px por metro).

A pose, do apoio para fora:
- os pés no chão, atrás do balcão (fora do quadro): o balcão (1,05 m) fica na altura da barriga, logo abaixo dos
  cotovelos; o corpo inteiro (1,72 m) dá a cabeça a 19 px do alto e os ombros a 44;
- o tronco de frente, a barriga larga; a cabeça um pouco virada para a direita dele, o olhar indo de lado para a esquerda
  dele (a direita de quem olha), a sobrancelha baixa daquele lado;
- os braços saem dos ombros, os cotovelos abertos e um pouco para trás, os antebraços vêm para a frente e se encontram
  no meio, na altura do peito: a mão de cá (a direita dele, à esquerda de quem olha) aperta o pano dentro da caneca, a
  outra segura a caneca pela asa; o pano pende da mão até perto do tampo;
- a camisa de linho cru com as mangas arregaçadas acima dos cotovelos, o avental de couro com o peitilho, as alças e as
  fivelas.

`camada()` devolve a figura numa camada 320×96, já com a luz da cena."""
import math

from . import desenho as D
from tela_h2 import Tela

COR = {
    "peleLuz": "#d89c6e", "pele": "#b47852", "peleSombra": "#7e5034", "peleEscura": "#5a3622", "rosado": "#c27458",
    "cabeloLuz": "#5a4232", "cabelo": "#3e2c20", "cabeloSombra": "#261a12",
    "barbaLuz": "#5e4632", "barba": "#3e2c1e", "barbaSombra": "#241810",
    "olho": "#120c08", "branco": "#c8b8a4",
    "camisaLuz": "#d6c8aa", "camisa": "#b2a282", "camisaSombra": "#82725a",
    "aventalLuz": "#644630", "avental": "#48321f", "aventalSombra": "#2e2014",
    "fivela": "#b08a3a", "fivelaLuz": "#e0bc60",
    "panoLuz": "#e6dfcc", "pano": "#c4bba4", "panoSombra": "#958b74",
}
LX, LY = -0.8, -0.6  # a luz vem da esquerda e de cima (a lareira e o lampião do teto)

CX = 160          # o meio do corpo
OMBRO = 44        # a linha dos ombros
CANECA = (156, 51, 9, 13)  # x, y, largura, altura do corpo da caneca


class Figura:
    def __init__(self):
        self.px = {}

    def p(self, x, y, cor):
        if cor:
            self.px[(int(x), int(y))] = COR.get(cor, cor)

    def tons(self, base):
        return base + "Luz", base, base + "Sombra"

    def capsula(self, a, b, ra, rb, base, luz=0.35, sombra=-0.3):
        """Um membro de a até b que afina de ra a rb, em três tons pelo lado virado para a luz."""
        cl, cm, cs = self.tons(base)
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
                    s = (ox * LX + oy * LY) / rr
                    self.p(x, y, cl if s > luz else cs if s < sombra else cm)

    def elipse(self, cx, cy, rx, ry, base, luz=0.4, sombra=-0.3, so=None):
        cl, cm, cs = self.tons(base)
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                ox, oy = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if ox * ox + oy * oy <= 1 and (so is None or so(x, y)):
                    s = ox * LX + oy * LY
                    self.p(x, y, cl if s > luz else cs if s < sombra else cm)

    def poligono(self, pts, base, luz_px=2, sombra_px=3):
        cl, cm, cs = self.tons(base)
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
                    self.p(x, y, cl if x < x0 + luz_px else cs if x > x1 - sombra_px else cm)

    def grade(self, x0, y0, linhas, pal):
        for dy, linha in enumerate(linhas):
            for dx, ch in enumerate(linha):
                if ch in pal:
                    self.p(x0 + dx, y0 + dy, pal[ch])

    def tela(self):
        t = Tela(D.QW, D.QH)
        for (x, y), c in self.px.items():
            if y < D.BT:  # o corpo some atrás do tampo do balcão
                t.px(x, y, c)
        return t


# ---------------------------------------------------------------- o corpo
def tronco(f):
    """A camisa (os ombros caídos e redondos, a barriga larga), o avental com o peitilho, as alças e as fivelas."""
    # o tronco: dos ombros à barriga, que alarga até o tampo
    f.poligono([(150, OMBRO - 2), (170, OMBRO - 2), (178, OMBRO + 1), (184, 52), (187, 74), (133, 74), (136, 52),
                (142, OMBRO + 1)], "camisa", 4, 5)
    # os ombros redondos
    f.elipse(142, OMBRO + 6, 7, 6.5, "camisa")
    f.elipse(178, OMBRO + 6, 7, 6.5, "camisa", luz=0.6)
    # a gola aberta: o vão em V com a pele do peito
    for y in range(OMBRO - 1, OMBRO + 5):
        meia = max(0, 4 - (y - OMBRO + 1) * 0.8)
        for x in range(round(CX - meia), round(CX + meia) + 1):
            f.p(x, y, "peleSombra" if x > CX else "pele")
    f.p(CX - 5, OMBRO - 1, "camisaLuz")
    f.p(CX + 4, OMBRO - 1, "camisaSombra")
    # o avental: o peitilho, que desce e alarga até a cintura, de couro escuro
    f.poligono([(151, OMBRO + 5), (169, OMBRO + 5), (172, 60), (175, 74), (145, 74), (148, 60)], "avental", 2, 3)
    f.p(151, OMBRO + 5, "aventalLuz")
    for x in range(152, 169):
        f.p(x, OMBRO + 5, "aventalLuz")
    # as alças: dos cantos do peitilho, por cima dos ombros, para trás
    for (x0, y0), (x1, y1) in (((151, OMBRO + 5), (145, OMBRO - 1)), ((168, OMBRO + 5), (175, OMBRO - 1))):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
            f.p(x, y, "avental")
            f.p(x + (1 if x0 < CX else -1), y, "aventalSombra" if x0 < CX else "aventalLuz")
    # as fivelas de latão nos cantos do peitilho
    for x in (150, 168):
        f.grade(x, OMBRO + 5, ["FF", "Ff"], {"F": "fivelaLuz", "f": "fivela"})
    # a costura do bolso do avental, embaixo
    for x in range(152, 168):
        f.p(x, 70, "aventalSombra")


def bracos(f):
    """Os braços: o de cima na manga de linho (arregaçada acima do cotovelo, com o rolo da manga), o antebraço em pele,
    os pelos em poucos pixels; os cotovelos abertos, os antebraços vindo para o meio."""
    for ombro, cotovelo, punho, lado in (((141, 50), (135, 66), (151, 62), -1), ((179, 50), (185, 66), (169, 62), 1)):
        f.capsula(ombro, cotovelo, 7, 6, "camisa", luz=0.45 if lado < 0 else 0.7)
        # a dobra entre o braço e o tronco: o lado de dentro da manga em sombra, do sovaco ao cotovelo
        (ax, ay), (bx, by) = ombro, cotovelo
        comp = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / comp * lado, (bx - ax) / comp * lado
        for k in range(24):
            t = 0.3 + 0.7 * k / 23
            r = 7 - t
            x, y = ax + (bx - ax) * t - nx * (r - 0.5), ay + (by - ay) * t - ny * (r - 0.5)
            f.p(round(x - 0.5), round(y - 0.5), "camisaSombra")
        # o rolo da manga, logo acima do cotovelo
        rx, ry = cotovelo[0] + (1 if lado < 0 else -1), cotovelo[1] - 4
        for dx in range(-6, 7):
            f.p(rx + dx, ry, "camisaSombra")
            f.p(rx + dx, ry - 1, "camisaLuz" if dx < 2 else "camisa")
        # o antebraço, grosso no cotovelo, afinando no punho
        f.capsula(cotovelo, punho, 4.5, 3.4, "pele", luz=0.25, sombra=-0.35)


def dobras(f):
    """As dobras do linho: as rugas das mangas descendo para a dobra do cotovelo, o puxado da camisa no sovaco, e a gola
    aberta, em pé dos dois lados do pescoço."""
    for (x0, y0), (x1, y1) in (((137, 58), (140, 55)), ((139, 60), (142, 57)), ((183, 58), (180, 55)),
                               ((181, 60), (178, 57)), ((147, 52), (145, 57)), ((173, 52), (175, 57))):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            f.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), "camisaSombra")
    # a gola: as duas abas em pé em volta do pescoço, abrindo em V até o peitilho
    f.grade(150, OMBRO - 4, ["LL...", "LLL..", ".LLs.", "..Ls.", "...s."], {"L": "camisaLuz", "s": "camisaSombra"})
    f.grade(166, OMBRO - 4, ["...mm", "..mmm", ".smm.", ".sm..", ".s..."], {"m": "camisa", "s": "camisaSombra"})


def caneca(f):
    """A caneca de estanho que ele limpa: o corpo com a aresta acesa e o brilho, a boca vista um pouco de baixo, os
    aros e a asa à direita."""
    x, y, w, h = CANECA
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            u = (xx - x) / (w - 1)
            f.p(xx, yy, "#9a9ca4" if u < 0.2 else "#45474e" if u > 0.78 else "#6e7078")
    f.p(x + 1, y + 2, "#cfd1d6")
    f.p(x + 1, y + 3, "#cfd1d6")
    f.p(x + 2, y + 8, "#cfd1d6")
    for xx in range(x, x + w):
        f.p(xx, y, "#9a9ca4")
        f.p(xx, y + h - 2, "#45474e")
    # a borda de cima, um pouco mais larga, com a boca escura atrás dela
    for xx in range(x - 1, x + w + 1):
        f.p(xx, y - 1, "#9a9ca4" if xx < x + 3 else "#6e7078")
    for xx in range(x + 1, x + w - 1):
        f.p(xx, y - 2, "#24252a")
    f.p(x, y - 2, "#6e7078")
    f.p(x + w - 1, y - 2, "#45474e")
    # o aro do meio
    for xx in range(x, x + w):
        f.p(xx, y + 6, "#45474e" if xx > x + 1 else "#6e7078")
    # a asa
    f.grade(x + w, y + 2, ["aa.", "..a", "..a", "..a", "..a", "..a", ".a."], {"a": "#45474e"})


def mao_direita(f):
    """A mão de cá (a direita dele): aperta o pano contra a caneca, a palma por fora; o pano embolado sai entre a mão e a
    caneca e pende até perto do tampo."""
    # o pano pendurado, atrás da mão: largo e com dobras
    for y in range(57, 73):
        u = (y - 57) / 15
        a = round(150 - 2 * u)
        b = round(157 - 1 * u)
        for x in range(a, b):
            dobra = (x - a + y // 3) % 4
            f.p(x, y, "panoLuz" if x - a < 1 else "panoSombra" if dobra == 0 or b - x <= 1 else "pano")
    # o bolo do pano entre a mão e a caneca
    f.grade(154, 53, [".pp", "PppS", "Ppp", "PpS"], {"P": "panoLuz", "p": "pano", "S": "panoSombra"})
    # a mão: o dorso arredondado, o polegar por cima, a sombra embaixo
    f.grade(148, 55, [
        ".lll.",
        "lllmm",
        "lmmmm",
        "lmmms",
        "mmmss",
        ".mss.",
    ], {"l": "peleLuz", "m": "pele", "s": "peleSombra"})
    f.p(152, 55, "peleSombra")  # a junta do polegar


def mao_esquerda(f):
    """A outra mão segura a caneca pela asa: os dedos em volta da asa e do corpo, o polegar por cima."""
    f.grade(164, 54, [
        ".ll..",
        "lmmm.",
        "lmmmm",
        "mmmms",
        "mmmss",
        "smmss",
        ".sss.",
    ], {"l": "peleLuz", "m": "pele", "s": "peleSombra"})
    f.p(164, 57, "peleSombra")  # a divisa dos dedos na frente da caneca
    f.p(164, 59, "peleSombra")


# ---------------------------------------------------------------- a cabeça
def cabeca(f):
    """A cabeça grande e larga, sem pescoço à mostra (a barba encosta na gola): o crânio com a calva, o cabelo escuro e
    crespo nos lados e atrás, as orelhas, as bochechas cheias, a barba curta da costeleta ao queixo, o bigode; o rosto
    desconfiado (a sobrancelha de lá baixa sobre o olho apertado, a de cá um pouco erguida, o olhar de lado, a boca
    fechada com os cantos para baixo)."""
    cx = CX
    # o pescoço grosso, logo atrás da barba
    for y in range(38, OMBRO + 2):
        for x in range(cx - 7, cx + 8):
            f.p(x, y, "peleSombra" if x > cx + 3 else "pele")
    # o cabelo de trás, por fora do rosto
    f.elipse(cx, 27, 10.4, 8.6, "cabelo", luz=0.55, sombra=-0.2)
    # o crânio e as bochechas (largas, caindo para a barba)
    f.elipse(cx, 27, 8.6, 10.2, "pele", luz=0.25, sombra=-0.25)
    f.elipse(cx, 33, 10.2, 7.6, "pele", luz=0.3, sombra=-0.2, so=lambda x, y: y >= 29)
    # o cabelo das têmporas: a calva entra até o alto, o cabelo fica dos lados, acima das orelhas
    for y in range(20, 31):
        for x in range(cx - 11, cx + 12):
            d = abs(x + 0.5 - cx)
            if d > 6.6 - max(0, 24 - y) * 0.8 and (x, y) in f.px and d > 5.0 and y < 30:
                if f.px[(x, y)] in (COR["peleLuz"], COR["pele"], COR["peleSombra"]):
                    f.p(x, y, "cabeloLuz" if (x + 2 * y) % 4 == 0 and x < cx else "cabelo" if x < cx else "cabeloSombra")
    # a calva: o brilho no alto, à esquerda
    f.grade(cx - 4, 19, ["ll.", "lll", ".l."], {"l": "peleLuz"})
    # as orelhas, na altura dos olhos ao nariz
    for x, lado in ((cx - 10, -1), (cx + 10, 1)):
        for y in range(27, 32):
            f.p(x, y, "pele" if lado < 0 and y < 30 else "peleSombra")
        f.p(x - lado, 29, "peleEscura")
    # a testa: uma ruga de leve em cima do nariz
    f.p(cx, 24, "peleSombra")
    f.p(cx + 1, 24, "peleSombra")
    # as sobrancelhas grossas: a de cá, um pouco erguida por fora; a de lá, baixa, apertando o olho
    for x, y in ((cx - 6, 24), (cx - 5, 24), (cx - 4, 25), (cx - 3, 25), (cx - 2, 26)):
        f.p(x, y, "cabeloSombra")
        f.p(x, y + 1, "cabelo" if x < cx - 3 else None)
    for x, y in ((cx + 2, 26), (cx + 3, 26), (cx + 4, 26), (cx + 5, 26), (cx + 6, 26), (cx + 7, 27)):
        f.p(x, y, "cabeloSombra")
    # os olhos: o de cá aberto (o branco e a pupila no canto de lá: o olhar de lado); o de lá apertado sob a
    # sobrancelha, só a pupila
    f.p(cx - 6, 27, "peleSombra")
    f.p(cx - 5, 27, "branco")
    f.p(cx - 4, 27, "olho")
    f.p(cx - 3, 27, "olho")
    f.p(cx + 3, 27, "branco")
    f.p(cx + 4, 27, "olho")
    f.p(cx + 5, 27, "olho")
    f.p(cx + 6, 27, "peleSombra")
    # as bolsas embaixo dos olhos
    for x in (cx - 5, cx - 4, cx - 3):
        f.p(x, 28, "pele")
    for x in (cx + 3, cx + 4, cx + 5):
        f.p(x, 28, "peleSombra")
    # o nariz grosso: a ponte clara, a ponta larga, as narinas
    for y in range(26, 31):
        f.p(cx - 1, y, "peleLuz")
        f.p(cx, y, "pele")
        f.p(cx + 1, y, "peleSombra" if y > 27 else "pele")
    f.grade(cx - 2, 30, [".llms", "llmms", "dmmsd"], {"l": "peleLuz", "m": "pele", "s": "peleSombra", "d": "peleEscura"})
    # as bochechas coradas
    f.p(cx - 6, 30, "rosado")
    f.p(cx - 5, 30, "rosado")
    f.p(cx - 6, 31, "rosado")
    f.p(cx + 5, 30, "rosado")
    # a barba curta e cheia: das costeletas às bochechas, ao queixo e até a gola
    for y in range(28, 44):
        for x in range(cx - 12, cx + 13):
            ox, oy = (x + 0.5 - cx) / 10.6, (y + 0.5 - 33.0) / 9.2
            dentro = ox * ox + (oy if oy < 0 else oy * 1.25) ** 2 <= 1 and y >= 28  # curta: o queixo largo e baixo
            face = ((x + 0.5 - cx) / 7.0) ** 2 + ((y + 0.5 - 30.0) / 4.6) ** 2 <= 1  # o rosto que fica de fora
            costeleta = abs(x + 0.5 - cx) > 8.5 and y >= 28
            if dentro and (not face or costeleta):
                s = ox * LX + oy * LY
                if y >= 41 and abs(x + 0.5 - cx) > 7:
                    continue
                cor = "barbaLuz" if s > 0.4 else "barbaSombra" if s < -0.25 else "barba"
                if (x * 7 + y * 3) % 6 == 0 and cor == "barba":  # o crespo
                    cor = "barbaSombra"
                if (x * 5 + y * 11) % 7 == 0 and cor == "barba" and x < cx:
                    cor = "barbaLuz"
                f.p(x, y, cor)
    # o bigode, por cima da boca, caindo nos cantos
    for x in range(cx - 5, cx + 6):
        f.p(x, 33, "barba" if x < cx else "barbaSombra")
    f.p(cx - 3, 33, "barbaLuz")
    f.p(cx - 2, 33, "barbaLuz")
    f.p(cx - 5, 34, "barba")
    f.p(cx + 5, 34, "barbaSombra")
    # a boca fechada, os cantos para baixo; o lábio de baixo
    for x in range(cx - 2, cx + 3):
        f.p(x, 34, "peleEscura")
    f.p(cx - 3, 35, "peleEscura")
    f.p(cx + 3, 35, "peleEscura")
    f.p(cx - 1, 35, "pele")
    f.p(cx, 35, "pele")
    f.p(cx + 1, 35, "peleSombra")


def figura():
    f = Figura()
    tronco(f)
    cabeca(f)
    bracos(f)
    dobras(f)
    mao_direita(f)
    caneca(f)
    mao_esquerda(f)
    return f


def camada():
    return D.luz(figura().tela())
