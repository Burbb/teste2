"""O ferreiro da forja F, por pose. Careca, gordo e forte, a barba ruiva grande com raiz nas bochechas e no queixo que
afunila numa trança com uma presilha; de três quartos, virado para a espada à esquerda, como na referência. A luz vem
da fornalha, à esquerda e um pouco de trás: a frente do rosto, a borda da barba, o alto do ombro e a metade esquerda
do avental acesos; o lado direito na sombra.

O corpo é desenhado à mão, em grades (um caractere por pixel; as medidas lidas na referência ampliada com a grade do
jogo por cima): a cabeça e a barba (CABECA), o tronco com o ombro e o braço de perto, nu, a braçadeira de couro e a
luva segurando a tenaz, o avental sobre a barriga e a túnica escura das costas (TRONCO), as pernas e as botas
(PERNAS). O braço do martelo (o direito dele, do lado de lá) é desenhado à mão em cada pose (BRACO: o punho fechado
no cabo, a braçadeira, o cotovelo, o bíceps entrando atrás da barba); o martelo, um objeto rígido, sai da geometria
(o cabo e a cabeça atravessada, a face virada para a luz mais clara). As mãos são simples, sem dedos, no padrão das
da Ilse e do mercador; os dois dedos que faltam ficam no texto do balcão.

As poses mexem o braço do martelo, o tronco (desce 1 px no golpe e no rebote, sobe 1 px no alto) e a cabeça com a
barba (um quadro depois do tronco no rebote). As pernas não saem do lugar."""
import math

from paleta_g import RAMPAS as R, K
from tela_g import Tela

QW, QH = 320, 96
CONTATO = (141, 58)  # onde a face do martelo encosta na lâmina (as faíscas nascem aqui)


# ---------------------------------------------------------------- a paleta das grades à mão
PAL = {"k": "#140f0c"}  # o contorno: o escuro quente da oficina, não o preto
PAL.update(zip("123456", R["pele"]))
PAL.update(zip("qrstu", R["barba"]))
PAL.update(zip("ABCDE", R["couro"]))
PAL.update(zip("wxyz", R["pano"]))
PAL.update(zip("fghiIJL", R["ferro"][0:4] + R["ferro"][5:8]))
PAL.update(zip("MNOP", R["madeira"][2:6]))


# ---------------------------------------------------------------- as poses
# `tronco`/`cabeca`: quanto descem (px); `rastro`: o caminho do martelo na descida; `vira`: a pausa da tenaz.
POSES = {
    "repouso": {"tronco": 0, "cabeca": 0},             # o martelo parado na lâmina, o mesmo lugar do golpe
    "sobe1": {"tronco": 0, "cabeca": 0},               # o punho sobe, a cabeça do martelo ainda na frente
    "sobe2": {"tronco": -1, "cabeca": 0},              # quase no alto: o cabo de pé ao lado da cabeça
    "alto": {"tronco": -1, "cabeca": -1},              # a referência: o punho acima da testa, o martelo para trás
    "desce": {"tronco": 0, "cabeca": 0, "rastro": True},  # um quadro: o martelo na frente do rosto
    "golpe": {"tronco": 1, "cabeca": 1, "golpe": True},   # a face do martelo na lâmina, o tronco afunda
    "volta": {"tronco": 1, "cabeca": 1},               # o rebote: o martelo 3 px acima
    "ajuste": {"tronco": 0, "cabeca": 0, "vira": True},   # a pausa: o martelo descansa, a tenaz vira a espada
}


# ---------------------------------------------------------------- o corpo, à mão (x 148 a 191)
# Uma linha por y; '.' não pinta. A cabeça e a barba (CABECA) descem com `cabeca`; o tronco, o ombro, o braço de perto
# e o avental (TRONCO) com `tronco`; as pernas e as botas (PERNAS) ficam.
X_CORPO = 148
CABECA = {  # y: linha
    31: "................kkkkk.......................",
    32: "...............k66554k......................",
    33: "..............k6665544k.....................",
    34: "..............k56655443k....................",
    35: ".............k5555444333k...................",
    36: ".............k6554443234k...................",
    37: ".............k4211123224k...................",
    38: "............k54216243233k...................",
    39: "............k3234544sr2k....................",
    40: "...........ktuts34ssrqCBk...................",
    41: "..........ktsssrsssrqrCBk...................",
    42: "..........kussrssrsqrqCB....................",
    43: ".........ktssrssrsrqrqCB....................",
    44: ".........ktssrssrsqrqk......................",
    45: ".........ktsrssrssrqk.......................",
    46: ".........kssrssrsrqqk.......................",
    47: "..........ktsrssrqqk........................",
    48: "...........kssrsqrk.........................",
    49: "...........ktsrqrk..........................",
    50: "..........kJLJIhgk..........................",
    51: "..........kIJIhgfk..........................",
    52: "...........ktsrqk...........................",
    53: "..........ktusrqk...........................",
    54: "..........kstrsqk...........................",
    55: "...........ksrqk............................",
    56: "............kkk.............................",
}
TRONCO = {
    36: ".........................kkkk...............",
    37: ".........................3445kkkkkk.........",
    38: ".........................3455565544kk.......",
    39: ".........................24556655443k.......",
    40: ".........................345566655443k......",
    41: "........................2345566554433k......",
    42: "........................2344555544332k......",
    43: "........................1334455444332k......",
    44: ".....................BCCB133445444332kk.....",
    45: ".....................BCCB123344443322kwk....",
    46: ".....................BCCB123444433322kxwk...",
    47: "...................BCCCCB122322233221kxwk...",
    48: "..................BCCCCCB134554443321kxwk...",
    49: ".........kD......CCCCCCB134454443321kxxwk...",
    50: ".........kD.......CCCCCCB123444433221kxxwk..",
    51: ".........kD.......CCCCCBB12334433221kxxxwk..",
    52: ".........kD......CCCCCCCCBBk23443321kxxxwk..",
    53: ".........k..CCCCCCCCkkkkkkkkk433221kxxxwk...",
    54: ".........kD.CCCCCCCkEEDDDDCCB32211kxxxxwk...",
    55: ".........kD.CCCkkkkkkkDEDDDCCBB211kxxxxwk...",
    56: ".........kDDCCkDEEDDCADDDDCCCBB11kxxxxxxwk..",
    57: ".........kDDDCkEDDDCCADDCCCCBBAkCCCCCCCxwk..",
    58: ".........kDDDCkDDDCCBACCCCBBBAAkxxDCxxxxwk..",
    59: ".........kEDDkDDCCCBBABBBBAAAkxxxxxCxxxxwk..",
    60: ".........kEDDkDCCCBBBkkkkkkkkkxxxxxDxxxxwk..",
    61: "........kEDDCCkkkkkkkCCCCBBBBAxxxxxCxxxxwk..",
    62: ".......kEDDDDCCCCCBCCCCBBBBBAAxxxxxDxxxxwk..",
    63: ".......kEEDDDDCCCCBCCCCBBBBBAAxxxxxBxxxxwk..",
    64: ".......kEEDDDDDCCCCBCCCCBBBBAAxxxxxxxxxxwk..",
    65: ".......kEEDDDDDCCCCBCCCCBBBBAAxxxxxxxxxxwk..",
    66: ".......kEDDDDDCCCCCBCCCBBBBBAAxxxxxxxxxxwk..",
    67: ".......kEDDDDCCCCCBCCCCBBBBAAAxxxxxxxxxxwk..",
    68: ".......kDDDDCCCCCBCCCCBBBBBAAAxxxxxxxxxwwk..",
    69: "........kDDDCCCCCBCCCBBBBBAAAAxxxxxxxxxwwk..",
    70: "........kDDCCCCCBCCCBBBBBBAAAAxxxxxxxxxwwk..",
    71: "........kDCCCCCBBCCBBBBBBAAAAAxxxxxxxxxwwk..",
    72: "........kDCCCCBBCCBBBBBBAAAAAAxxxxxxxxxwk...",
    73: ".........kDCCCBBCBBBBBBBAAAAAAxxxxxxxxwwk...",
    74: ".........kCCBBBBBBBBBBBBAAAAAkxxxxxxxwwk....",
    75: "..........kBBBBBBBBBBBBBAAAAk.xxxxxxxwk.....",
    76: "...........kkkkkkkkkkkkkkkkk..yxxxxxk.......",
}
PERNAS = {
    77: ".......kyyxxxxwwwk...........kxxxxxwwwwk....",
    78: ".......kyyxxxxwwwk...........kxxxxxwwwwk....",
    79: "........kyxxxxwwwk............kxxxxwwwwk....",
    80: ".........kyxxxwwk..............kxxxwwwk.....",
    81: "........kDEDDCCBBk............kCDCCBBBAk....",
    82: "........kDCCCBBBAk............kDCCBBBAAk....",
    83: "........kEDCCBBBAk...........kDCCBBBBAAk....",
    84: ".......kDDCCBBBBAk..........kDCCBBBBBAAk....",
    85: ".......kAAAAAAAAAk..........kAAAAAAAAAAk....",
    86: "........kkkkkkkkk............kkkkkkkkkk.....",
}

# O braço do martelo, por pose, à mão ("x:caracteres"; a primeira linha é o y de `y0`): o punho fechado no cabo, a
# braçadeira de couro no pulso, o cotovelo e o bíceps entrando atrás da barba. O martelo (o cabo e a cabeça) vem antes,
# por geometria (é um objeto rígido): `cabo` (a ponta de baixo) e `cabeca` (o centro da cabeça), em MARTELO.
PUNHO = ["..kkkkk..",
         ".k66554k.",
         "k5665443k",
         "k5544433k",
         "k5443322k",
         ".k43321k.",
         "..kkkkk.."]
# o punho de lado (o cabo deitado sai dos dois lados); as mãos são simples, sem dedos, como as da Ilse e do mercador
PUNHO_DEITADO = [".kkkkkkk.",
                 "k6655544k",
                 "k5544433k",
                 "k4433322k",
                 "k3332211k",
                 ".kkkkkkk."]


def _punho(x, y, deitado=False):
    return (x, y, PUNHO_DEITADO if deitado else PUNHO)


BRACO = {
    "alto": {"punho": _punho(149, 26), "linhas": (33, [
        "149:kDEEDDCBk",
        "149:kEDDCCBAk",
        "149:kDDCCBBAk",
        "149:kkCCBBAkk",
        "148:k55443322kkkkk",
        "147:k5655443332222k",
        "147:k56554443333222k",
        "147:k55544433332221k",
        "147:k45444333322211k",
        "148:k4443333222111k",
        "148:k33332222111k",
        "149:k222221111k",
        "150:kkkkkkkkk"])},
    "sobe2": {"punho": _punho(146, 31), "linhas": (38, [
        "147:kDEDDCBk",
        "147:kEDCCBAk",
        "147:kkCCBAkk",
        "146:k5544332kkkkk",
        "145:k565544333222k",
        "145:k5554443332221k",
        "145:k4544333322211k",
        "146:k444333222111k",
        "146:k3332222111k",
        "147:kkkkkkkkkk"])},
    "sobe1": {"punho": _punho(147, 40), "linhas": (42, [
        "154:kkk",
        "153:k5543k",
        "152:k55432k",
        "152:kDEDDCBk",
        "153:kEDDCBk",
        "154:kDDCBAk",
        "155:k5432k",
        "156:k432k",
        "157:kkk"])},
    "desce": {"punho": _punho(145, 39), "linhas": (41, [
        "152:kkk",
        "151:k5543k",
        "150:k55432k",
        "150:kDEDDCBk",
        "151:kEDDCBk",
        "152:kDDCBAk",
        "154:k5432k",
        "155:k5432k",
        "156:k432k",
        "157:kkk"])},
    "contato": {"punho": _punho(150, 50, True), "linhas": (42, [
        "158:kk",
        "157:k54k",
        "156:k5543k",
        "155:k55432k",
        "155:k54332k",
        "154:kDEDCBk",
        "154:kEDDCBk",
        "153:kDDCBAk"])},
    "volta": {"punho": _punho(150, 47, True), "linhas": (39, [
        "158:kk",
        "157:k54k",
        "156:k5543k",
        "155:k55432k",
        "155:k54332k",
        "154:kDEDCBk",
        "154:kEDDCBk",
        "153:kDDCBAk"])},
}
BRACO["golpe"] = BRACO["repouso"] = BRACO["ajuste"] = BRACO["contato"]
MARTELO = {
    "alto": ((147.5, 35.8), (161.4, 22.4)),
    "sobe2": ((151.5, 41.0), (150.2, 25.0)),
    "sobe1": ((156.0, 49.0), (145.0, 34.8)),
    "desce": ((156.0, 47.0), (141.0, 36.0)),
    "contato": ((160.0, 52.5), (141.5, 53.5)),
    "volta": ((160.0, 49.5), (141.6, 50.0)),
}
for _p in ("golpe", "repouso", "ajuste"):
    MARTELO[_p] = MARTELO["contato"]


def desenhar_martelo(t, cabo, cabeca, dy=0):
    """O cabo de madeira (1 px com o contorno) da ponta de baixo até a cabeça, e a cabeça de ferro (9 × 5) atravessada,
    com a face virada para a luz (o alto e a esquerda) mais clara."""
    (bx, by), (hx_, hy) = cabo, cabeca
    by += dy
    hy += dy
    ux, uy = hx_ - bx, hy - by
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    vx, vy = -uy, ux
    fim = n - 2.5
    pts = []
    i = 0.0
    while i <= fim:
        pts.append((int(math.floor(bx + ux * i)), int(math.floor(by + uy * i))))
        i += 0.5
    pts = list(dict.fromkeys(pts))
    for x, y in pts:
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + ox, y + oy) not in pts:
                t.px(x + ox, y + oy, K)
    for j, (x, y) in enumerate(pts):
        t.px(x, y, R["madeira"][4] if j % 5 else R["madeira"][3])
    cel = {}
    for x in range(int(hx_ - 7), int(hx_ + 8)):
        for y in range(int(hy - 7), int(hy + 8)):
            px_, py_ = x + 0.5 - hx_, y + 0.5 - hy
            s, u = px_ * vx + py_ * vy, px_ * ux + py_ * uy
            if abs(s) <= 4.5 and abs(u) <= 2.5:
                # a face mais perto: as pontas (de bater) ou os lados
                if abs(s) > 3.4:
                    nx, ny = (vx, vy) if s > 0 else (-vx, -vy)
                else:
                    nx, ny = (ux, uy) if u > 0 else (-ux, -uy)
                    if abs(u) < 1.2:
                        nx, ny = nx * 0.3, ny * 0.3
                d = -(nx * 0.8 + ny * 0.6)
                cel[(x, y)] = R["ferro"][6] if d > 0.55 else R["ferro"][5] if d > 0.25 else R["ferro"][3] if d > -0.05 \
                    else R["ferro"][2] if d > -0.4 else R["ferro"][1]
    for (x, y) in cel:
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + ox, y + oy) not in cel:
                t.px(x + ox, y + oy, K)
    for (x, y), c in cel.items():
        t.px(x, y, c)


def rastro(t, dy=0):
    """A descida: o caminho da cabeça do martelo (do alto, por cima, até a frente do rosto), nítido, de 1 px."""
    for i, (x, y) in enumerate([(160, 18), (156, 17), (152, 18), (148, 21), (145, 25), (143, 29)]):
        t.px(x, y + dy, R["ferro"][3] if i < 3 else R["ferro"][4])
        t.px(x + 1, y + dy, R["ferro"][2] if i < 3 else R["ferro"][3])


# O tronco se divide no cotovelo de perto (y 52): de cima para baixo até ali (os ombros, o bíceps, o peito, a barba)
# acompanha o golpe (`tronco`); dali para baixo (o antebraço, a luva com a tenaz, a barriga, o avental) fica, e o corpo
# absorve o movimento: no golpe a linha do cotovelo se sobrepõe, no alto ela se repete (sem abrir vão).
CORTE_TRONCO = 52
TENAZ = (148, 162, 59)  # das garras (na espiga da espada, paradas) até dentro da luva: x0, x1, a haste de cima


def tenaz(t, virada=False):
    """A tenaz: as duas hastes das garras na espiga até dentro da luva (a mão a segura: as hastes entram nela), paradas
    no balanço do golpe. Virada (a pausa): a lâmina de lado, as garras fechadas nela do mesmo jeito."""
    x0, x1, y = TENAZ
    k, cl, ce, cb = PAL["k"], R["ferro"][5], R["ferro"][3], R["ferro"][1]
    for x in range(x0 + 2, x1 + 1):
        t.px(x, y - 1, k)
        t.px(x, y, cl if x % 4 else ce)
        t.px(x, y + 1, cb)
        t.px(x, y + 2, k)
    for dy in range(-1, 3):  # as garras fechadas na espiga
        t.px(x0, y + dy, k)
        t.px(x0 + 1, y + dy, ce if dy <= 0 else cb)
    # a luva por cima das hastes, nos dois lados: os dedos fechados em volta
    t.px(x1, y - 1, PAL["D"])
    t.px(x1 + 1, y - 1, PAL["D"])
    t.px(x1, y + 2, PAL["C"])
    t.px(x1 + 1, y + 2, PAL["C"])


def figura(pose, quadro=0, virada=False):
    """O ferreiro na pose: uma Tela 320×96 transparente (com a tenaz, que é dele)."""
    p = POSES[pose]
    tr, ca = p["tronco"], p["cabeca"]
    t = Tela(QW, QH)
    if p.get("rastro"):
        rastro(t, tr)
    desenhar_martelo(t, *MARTELO[pose], dy=tr)
    br = BRACO[pose]
    y0, linhas = br["linhas"]
    for i, l in enumerate(linhas):
        x0, cs = l.split(":", 1)
        for j, ch in enumerate(cs):
            if ch in PAL:
                t.px(int(x0) + j, y0 + i + tr, PAL[ch])
    px0, py0, grade = br["punho"]
    for i, l in enumerate(grade):
        for j, ch in enumerate(l):
            if ch in PAL:
                t.px(px0 + j, py0 + i + tr, PAL[ch])
    camadas = [(PERNAS, 0, None), ({y: l for y, l in TRONCO.items() if y >= CORTE_TRONCO}, 0, None),
               ({y: l for y, l in TRONCO.items() if y <= CORTE_TRONCO}, tr, None), (CABECA, ca, None)]
    for i, (grade, dy, _) in enumerate(camadas):
        for y, l in grade.items():
            for j, ch in enumerate(l):
                if ch in PAL:
                    t.px(X_CORPO + j, y + dy, PAL[ch])
        if i == 1:
            tenaz(t, virada)
    return t
