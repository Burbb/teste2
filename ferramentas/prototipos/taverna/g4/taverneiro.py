"""O taverneiro animado da G4: o homem da G3 (o desenho da G, com os retoques da G2 e o pano da G3) limpando a caneca,
pose a pose, pelo fluxo da skill `arte-cenas-fenda` (seção 5b).

**A atividade e os apoios.** Ele esfrega a caneca com o pano e, de tempos em tempos, para e olha os fregueses. O que
fica: os pés (fora do quadro), o quadril atrás do balcão, a mão de lá segurando a caneca pela asa, a caneca (o mesmo
tamanho, a mesma pega, presa ao tronco). O que mexe: a mão do pano, que dá a volta na caneca (entra pela boca, desce
pelo lado, volta).

**Quem conduz, quem acompanha, quem fica.**

| Trecho | Conduz | Acompanha | Fica |
|---|---|---|---|
| Esfregar | a mão do pano (até 2 px) | o pano pendurado (um tique depois, a ponta para o outro lado), o tronco 1 px para baixo na passada de baixo, a cabeça 1 px um tique depois do tronco | a caneca e a mão da asa (com o tronco), o quadril |
| Olhar os fregueses | os olhos (sobem primeiro) | a cabeça (sobe 1 px um tique depois), depois os olhos vão para o outro lado | as duas mãos paradas na caneca, o tronco |

**As partes andam presas a elas mesmas:** cada parte (o tronco com os braços de cima, a cabeça, o braço do pano com o
pano, a caneca com a mão da asa, o pano na boca da caneca) é desenhada e iluminada na posição da G (`g.desenho.luz`, o
pontilhado da G), retocada como na G2 (`pele_lisa`, `mangas`, `pescoco`) e só depois deslocada: o pontilhado anda com
a parte e não cintila. O antebraço do pano é o único redesenhado a cada pose (do cotovelo à mão)."""
import numpy as np

from g import desenho as G, taverneiro as GT
from g2 import retoques as R2
from g3 import retoques as R3
from tela_h2 import Tela

QW, QH, BT = G.QW, G.QH, G.BT
OLHOS = ("lado", "baixo", "outro")


def _figura():
    return GT.Figura()


def _parte(desenhar, retocar=()):
    """Desenha uma parte na posição da G, ilumina (o pontilhado preso a ela) e retoca; devolve o numpy RGBA."""
    f = _figura()
    desenhar(f)
    t = Tela(QW, QH)
    for (x, y), c in f.px.items():
        t.px(x, y, c)
    G.luz(t)
    a = t.a
    for r in retocar:
        r(a)
    return a


def _olhos(f, modo):
    """Os olhos da G em três modos: `lado` (os da G: o branco à esquerda, a pupila olhando para a direita de quem vê,
    para os fregueses), `outro` (o olhar para o outro lado) e `baixo` (a pálpebra baixa, a pupila embaixo: a caneca)."""
    cx = GT.CX
    if modo == "lado":
        return
    if modo == "outro":
        for x, c in ((cx - 5, "olho"), (cx - 4, "olho"), (cx - 3, "branco"), (cx + 3, "olho"), (cx + 4, "olho"),
                     (cx + 5, "branco")):
            f.p(x, 27, c)
        return
    for x in (cx - 5, cx - 4, cx - 3, cx + 3, cx + 4, cx + 5):  # baixo: a pálpebra cobre, a pupila espia embaixo
        f.p(x, 27, "peleEscura")
    for x, c in ((cx - 5, "pele"), (cx - 4, "olho"), (cx - 3, "pele"), (cx + 3, "peleSombra"), (cx + 4, "olho"),
                 (cx + 5, "peleSombra")):
        f.p(x, 28, c)


def _braco_do_pano(f, dx, dy):
    """O antebraço do pano, do cotovelo da G (parado) até a mão deslocada (dx, dy)."""
    f.capsula((135, 66), (151 + dx, 62 + dy), 4.5, 3.4, "pele", luz=0.25, sombra=-0.35)


def _pano_e_mao(f, dx, dy, atraso):
    """O pano pendurado (preso no punho; da metade para baixo atrasado `atraso` px, a ponta balança para o outro lado)
    e a mão do pano, deslocados (dx, dy)."""
    g = _figura()
    R3._pano_pendente(g)
    for (x, y), c in g.px.items():
        des = atraso if y >= 66 else (atraso // 2 if y >= 63 else 0)
        f.px[(x + dx + des, y + dy)] = c
    m = _figura()
    R3._mao(m)
    for (x, y), c in m.px.items():
        f.px[(x + dx, y + dy)] = c


def _tronco(f):
    """O tronco, os braços de cima com as mangas e o rolo, o antebraço da caneca e a gola (o desenho da G, sem o
    antebraço do pano)."""
    GT.tronco(f)
    import math
    for ombro, cotovelo, punho, lado in (((141, 50), (135, 66), None, -1), ((179, 50), (185, 66), (169, 62), 1)):
        f.capsula(ombro, cotovelo, 7, 6, "camisa", luz=0.45 if lado < 0 else 0.7)
        (ax, ay), (bx, by) = ombro, cotovelo
        comp = math.hypot(bx - ax, by - ay)
        nx, ny = -(by - ay) / comp * lado, (bx - ax) / comp * lado
        for k in range(24):
            t = 0.3 + 0.7 * k / 23
            r = 7 - t
            x, y = ax + (bx - ax) * t - nx * (r - 0.5), ay + (by - ay) * t - ny * (r - 0.5)
            f.p(round(x - 0.5), round(y - 0.5), "camisaSombra")
        rx, ry = cotovelo[0] + (1 if lado < 0 else -1), cotovelo[1] - 4
        for d in range(-6, 7):
            f.p(rx + d, ry, "camisaSombra")
            f.p(rx + d, ry - 1, "camisaLuz" if d < 2 else "camisa")
        if punho:
            f.capsula(cotovelo, punho, 4.5, 3.4, "pele", luz=0.25, sombra=-0.35)
    GT.dobras(f)


def _caneca(f):
    GT.caneca(f)
    GT.mao_esquerda(f)


def _cabeca(modo):
    def desenhar(f):
        GT.cabeca(f)
        _olhos(f, modo)
    return desenhar


def _colar(quadro, a, dx, dy):
    """Põe a parte (numpy RGBA) deslocada no quadro, cortada no tampo de trás do balcão."""
    ys, xs = np.nonzero(a[:, :, 3])
    for y, x in zip(ys, xs):
        X, Y = x + dx, y + dy
        if 0 <= X < QW and 0 <= Y < BT:
            quadro[Y, X] = a[y, x]


# ---------------------------------------------------------------- as poses
# tronco (tx, ty), cabeça além do tronco (hx, hy, olhos), mão do pano (wx, wy), atraso da ponta do pano
POSES = {
    "esfrega0": dict(t=(0, 0), h=(0, 0, "baixo"), w=(0, 0), a=0),     # a mão na boca da caneca
    "esfrega1": dict(t=(0, 0), h=(0, 0, "baixo"), w=(1, -1), a=-1),   # empurra o pano para dentro
    "esfrega2": dict(t=(0, 0), h=(0, 0, "baixo"), w=(1, 1), a=0),     # desce pelo lado
    "esfrega3": dict(t=(0, 1), h=(0, 0, "baixo"), w=(0, 2), a=1),     # embaixo: o tronco desce 1 px
    "esfrega4": dict(t=(0, 1), h=(0, 1, "baixo"), w=(0, 2), a=1),     # a cabeça acompanha um tique depois
    "olha0": dict(t=(0, 0), h=(0, 0, "lado"), w=(0, 0), a=0),         # os olhos sobem primeiro
    "olha1": dict(t=(0, 0), h=(0, -1, "lado"), w=(0, 0), a=0),        # a cabeça sobe: olha os fregueses
    "olha2": dict(t=(0, 0), h=(0, -1, "outro"), w=(0, 0), a=0),       # o olhar vai para o outro lado
}
ORDEM = list(POSES)
PARADA = "olha0"  # o movimento reduzido: a pose da G3 (o olhar de lado, desconfiado)

# a rotina, em tiques de 100 ms: quatro passadas de esfregar (a última mais lenta), a pausa para olhar os fregueses
_PASSADA = [("esfrega0", 3), ("esfrega1", 3), ("esfrega2", 2), ("esfrega3", 2), ("esfrega4", 2), ("esfrega2", 2)]
_LENTA = [("esfrega0", 4), ("esfrega1", 4), ("esfrega2", 3), ("esfrega3", 3), ("esfrega4", 3), ("esfrega2", 3)]
ROTINA = _PASSADA * 3 + _LENTA + [("esfrega0", 4), ("olha0", 3), ("olha1", 24), ("olha2", 14), ("olha1", 6),
                                  ("olha0", 3), ("esfrega0", 3)]


def quadro(nome):
    """Uma pose inteira, numa camada 320×96 (RGBA numpy)."""
    p = POSES[nome]
    tx, ty = p["t"]
    hx, hy, olhos = p["h"]
    wx, wy = p["w"]
    q = np.zeros((QH, QW, 4), np.uint8)
    _colar(q, _parte(_tronco, (R2.mangas,)), tx, ty)
    _colar(q, _parte(_cabeca(olhos), (R2.pescoco, R2.pele_lisa)), tx + hx, ty + hy)
    _colar(q, _parte(lambda f: (_braco_do_pano(f, wx, wy), _pano_e_mao(f, wx, wy, p["a"])), (R2.pele_lisa,)), tx, ty)
    _colar(q, _parte(_caneca), tx, ty)
    _colar(q, _parte(lambda f: _pano_na_caneca(f, wx, wy)), tx, ty)
    return q


def _pano_na_caneca(f, dx, dy):
    g = _figura()
    R3._pano_na_caneca(g)
    for (x, y), c in g.px.items():
        f.px[(x + dx, y + dy)] = c


def tempo():
    """A linha do tempo: o índice da pose (em ORDEM) a cada tique de 100 ms."""
    t = []
    for nome, n in ROTINA:
        t += [ORDEM.index(nome)] * n
    return t
