"""O taverneiro animado da G4: o homem da G3 (o desenho da G, com os retoques da G2 e o pano da G3) limpando a caneca,
pose a pose, pelo fluxo da skill `arte-cenas-fenda` (seção 5b).

**A atividade e os apoios.** Ele esfrega a caneca com o pano e, de tempos em tempos, para e olha os fregueses. Limpar
uma caneca é um trabalho de mãos: pouco esforço, alcance curto, a caneca apoiada na outra mão. O que fica (e dá
estabilidade à ação): os pés (fora do quadro), o quadril atrás do balcão, o tronco, a cabeça enquanto ele esfrega (os
olhos baixos, no trabalho). O que mexe: a mão do pano, que dá a volta na caneca (sobe pela parede de cá, atravessa, desce
fazendo força, volta). Ele limpa o lado de fora virado para ele: o pano fica na mão, apertado contra a parede de
cá (não passa pela borda nem entra na caneca), e a mão anda no máximo 1 px para o lado.

**Quem conduz, quem acompanha, quem fica** (a segunda versão; a primeira descia o tronco e a cabeça a cada passada e
lia como o corpo inteiro limpando a caneca: `g4/aseprite-v1/`, `camadas/g4-v1/`).

| Trecho | Conduz | Acompanha | Fica |
|---|---|---|---|
| Esfregar | a mão do pano (até 2 px, uma volta pela parede de cá) | o antebraço do pano (sai do cotovelo); o cotovelo 1 px para dentro quando a mão atravessa a parede e 1 px abaixo na pressão; o ombro do pano 1 px abaixo só na pressão; o pano pendurado (a ponta 1 px atrás do movimento da mão, caindo de volta) | o tronco, a cabeça (os olhos na caneca), a caneca e a mão da asa |
| Ajustar a pega (uma vez, na passada lenta) | a mão da caneca ergue a caneca 1 px | a mão do pano, que vai com ela | o tronco, a cabeça |
| Olhar os fregueses (a pausa: uma ação própria) | os olhos (sobem primeiro) | a cabeça (sobe 1 px um tique depois), depois os olhos vão para o outro lado | as duas mãos paradas na caneca, o tronco |

**As partes andam presas a elas mesmas:** cada parte (o tronco com os braços de cima, a cabeça, o braço do pano com o
pano, a caneca com a mão da asa, o pano apertado na caneca) é desenhada e iluminada na posição da G (`g.desenho.luz`, o
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


def _braco_do_pano(f, dx, dy, cotovelo=(0, 0)):
    """O antebraço do pano, do cotovelo da G (deslocado `cotovelo`) até a mão deslocada (dx, dy)."""
    f.capsula((135 + cotovelo[0], 66 + cotovelo[1]), (151 + dx, 62 + dy), 4.5, 3.4, "pele", luz=0.25, sombra=-0.35)


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


def _tronco(f, ombro_pano=(0, 0), cotovelo_pano=(0, 0), pega=(0, 0)):
    """O tronco, os braços de cima com as mangas e o rolo, o antebraço da caneca e a gola (o desenho da G, sem o
    antebraço do pano). O braço de cima do pano acompanha a mão (o ombro e o cotovelo deslocados); o punho da caneca
    acompanha o ajuste da pega."""
    GT.tronco(f)
    import math
    (ox, oy), (ex, ey), (px_, py_) = ombro_pano, cotovelo_pano, pega
    for ombro, cotovelo, punho, lado in (((141 + ox, 50 + oy), (135 + ex, 66 + ey), None, -1),
                                         ((179, 50), (185, 66), (169 + px_, 62 + py_), 1)):
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
# mão do pano (w), cotovelo (e) e ombro (o) do pano, pega da caneca (c: a caneca, a mão da asa e o punho), atraso da
# ponta do pano (a), olhos e cabeça além do tronco (h). O tronco não se mexe.
POSES = {
    "esfrega0": dict(w=(0, 0), e=(0, 0), o=(0, 0), c=(0, 0), a=0, h=(0, 0, "baixo")),    # a mão na boca da caneca
    "esfrega1": dict(w=(0, -1), e=(0, 0), o=(0, 0), c=(0, 0), a=0, h=(0, 0, "baixo")),   # sobe pela parede de cá
    "esfrega2": dict(w=(1, 0), e=(1, 0), o=(0, 0), c=(0, 0), a=-1, h=(0, 0, "baixo")),   # atravessa a parede; o cotovelo vem
    "esfrega3": dict(w=(1, 2), e=(0, 1), o=(0, 1), c=(0, 0), a=0, h=(0, 0, "baixo")),    # desce pelo lado: a pressão
    "esfrega4": dict(w=(0, 1), e=(0, 0), o=(0, 0), c=(0, 0), a=1, h=(0, 0, "baixo")),    # volta; a ponta cai atrás
    "pega": dict(w=(0, -1), e=(0, 0), o=(0, 0), c=(0, -1), a=0, h=(0, 0, "baixo")),      # a mão da asa ajeita a caneca
    "olha0": dict(w=(0, 0), e=(0, 0), o=(0, 0), c=(0, 0), a=0, h=(0, 0, "lado")),        # os olhos sobem primeiro
    "olha1": dict(w=(0, 0), e=(0, 0), o=(0, 0), c=(0, 0), a=0, h=(0, -1, "lado")),       # a cabeça sobe: olha os fregueses
    "olha2": dict(w=(0, 0), e=(0, 0), o=(0, 0), c=(0, 0), a=0, h=(0, -1, "outro")),      # o olhar vai para o outro lado
}
ORDEM = list(POSES)
PARADA = "olha0"  # o movimento reduzido: a pose da G3 (o olhar de lado, desconfiado)

# a rotina, em tiques de 100 ms: três passadas, uma lenta com o ajuste da pega, a pausa para olhar os fregueses. As
# poses seguram 2 tiques (a pressão 3), como na curandeira; a mão anda até 2 px de uma pose para a outra.
_PASSADA = [("esfrega0", 2), ("esfrega1", 2), ("esfrega2", 2), ("esfrega3", 3), ("esfrega4", 2)]
_LENTA = [("esfrega0", 3), ("esfrega1", 3), ("esfrega2", 3), ("esfrega3", 4), ("esfrega4", 2), ("pega", 4),
          ("esfrega0", 2)]
ROTINA = _PASSADA * 3 + _LENTA + _PASSADA + [("esfrega0", 4), ("olha0", 3), ("olha1", 24), ("olha2", 14),
                                             ("olha1", 6), ("olha0", 3), ("esfrega0", 3)]


def quadro(nome):
    """Uma pose inteira, numa camada 320×96 (RGBA numpy)."""
    p = POSES[nome]
    hx, hy, olhos = p["h"]
    wx, wy = p["w"]
    cx, cy = p["c"]
    q = np.zeros((QH, QW, 4), np.uint8)
    _colar(q, _parte(lambda f: _tronco(f, p["o"], p["e"], p["c"]), (R2.mangas,)), 0, 0)
    _colar(q, _parte(_cabeca(olhos), (R2.pescoco, R2.pele_lisa)), hx, hy)
    _colar(q, _parte(lambda f: (_braco_do_pano(f, wx, wy, p["e"]), _pano_e_mao(f, wx, wy, p["a"])), (R2.pele_lisa,)),
           0, 0)
    _colar(q, _parte(_caneca), cx, cy)
    _colar(q, _parte(lambda f: _pano_na_caneca(f, wx, wy)), 0, 0)
    return q


# o pano na mão, apertado contra a parede de cá da caneca (x 153 a 155, de y 52 a y 59 na pose da G): o volume curto que
# sai de cima dos dedos e desce até a parte que pende; anda com a mão. A borda de cima arredondada, a crista pega a luz,
# a sombra curta separa do metal (à direita) e dos dedos (embaixo do polegar). Ele limpa a caneca por fora: o pano que
# passava por cima da borda (o da G3, de quando o pano entrava na caneca) saiu.
_PANO_NA_MAO = {52: "Lp.", 53: "LpS", 54: "LpS", 55: "LpS", 56: "LpS", 57: "pLS", 58: "SLp", 59: "Spp"}


def _pano_na_caneca(f, wx, wy):
    """O pano que a mão aperta contra a parede de cá da caneca, deslocado com a mão (wx, wy)."""
    cores = {"L": "panoLuz", "p": "pano", "S": "panoSombra"}
    for y, linha in _PANO_NA_MAO.items():
        for k, ch in enumerate(linha):
            if ch != ".":
                f.p(153 + k + wx, y + wy, cores[ch])


def tempo():
    """A linha do tempo: o índice da pose (em ORDEM) a cada tique de 100 ms."""
    t = []
    for nome, n in ROTINA:
        t += [ORDEM.index(nome)] * n
    return t
