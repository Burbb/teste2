"""A queda de braço no canto da taverna (protótipo; nada no jogo): as poses, a linha do tempo e a fonte.

    python ferramentas/prototipos/taverna/morel/queda-canto/poses.py --previa <pasta> [--guia]   # as poses em PNG
    python ferramentas/prototipos/taverna/morel/queda-canto/poses.py --criar     # monta queda-canto.aseprite (só se
                                                                                  # não existir; --refazer descarta
                                                                                  # os retoques)

**A cena é a do canto, lida do código dela** (`morel/canto/`: o espaço, os objetos, Morel por partes; a fonte
`canto.aseprite` é igual a ele, conferido por `canto/exportar.py --conferir`): a câmera, a parede, o tronco, a gola, a
cabeça (a pose `olha`: os olhos em nós), as ombreiras, a manga e as mãos em bolinha. Nada de Morel é redesenhado; muda
o que a disputa pede:
- **o braço direito dele** pela manga da cena (as juntas da construção, `geometria.py`), com o braço de cima recuando
  meio degrau atrás do antebraço quando os dois se dobram muito (o método da `queda-vista`), e a ombreira clara na
  junta do ombro;
- **o nosso antebraço**, a lã azul-acinzentada das propostas anteriores (fria, para não se confundir com o couro dele),
  em perspectiva: mais grosso perto da câmera, cortado pela borda de baixo antes do cotovelo (o cotovelo fica na
  construção, fora do quadro); deitando com a palma para cima quando perdemos, a face larga virando para a câmera;
- **a pega**: duas mãos simples, construídas como dois volumes no espaço (o punho de cada um na ponta do antebraço dele),
  pintadas com três tons de pele cada, a dele um degrau abaixo da nossa; da mão de trás, só a tira dos dedos sobre o
  dorso que a câmera vê, e um pixel de sombra onde uma passa atrás da outra (o método da `queda-vista`);
- **a mesa**: a tigela deslizada para a direita e para o fundo (fora do caminho dos dois fins), com a colher dentro; a
  mão esquerda dele vai com ela pela borda e depois desce para o colo, atrás do tampo (onde ficaria no tampo, a nossa mão
  cai quando ele vence); a vela, a caneca e o pão ficam.

As poses vêm de `ROTEIRO` (a preparação, a disputa, os dois derrubes e o depois); a linha do tempo, de `TEMPO`."""
import math
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI.parent / "canto"))
sys.path.insert(0, str(AQUI.parent / "vista"))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))
sys.path.insert(0, str(AQUI))

import espaco as ES  # noqa: E402
import juntas as J  # noqa: E402
import manga as MG  # noqa: E402
import morel as MO  # noqa: E402
import objetos as OB  # noqa: E402
import geometria as G  # noqa: E402

FONTE = AQUI / "queda-canto.aseprite"
CAMADAS = ["parede", "espada", "morel_corpo", "morel_cabeca", "morel_esquerdo_atras", "mesa", "objetos", "tigela",
           "morel_esquerdo", "morel_braco", "nosso_braco", "maos", "construcao", "juntas"]
OCULTAS = ("construcao", "juntas")
H = ES.h

# a nossa manga: a lã azul-acinzentada das propostas anteriores, nos degraus do couro dele (j realce, a, b, c, l)
LA = {"j": H("7c889a"), "a": H("5e6878"), "b": H("474f5d"), "c": H("333a45"), "l": H("262b34")}
LA_PUNHO = (H("3a4150"), H("262b34"))
PELE_NOSSA = (H("d6a888"), H("ae7c5e"), H("7a5440"))
PELE_MOREL_PEGA = (H("b4805e"), H("8c5e44"), H("5e3e2c"))  # um degrau abaixo da nossa: duas peles, pelo valor
LUZ_MUNDO = (-0.6, 0.55, -0.58)                            # a vela: à esquerda, um pouco acima, do nosso lado
R_NOSSO = (4.8, 3.3)                                       # o raio do nosso antebraço no cotovelo e no punho (cm)
RAIO_PUNHO = (4.4, 3.6, 3.2)                               # cada mão fechada: ao longo, de lado, de espessura (cm)

# a tigela no fim da preparação: para a direita e para o fundo (a borda de lá dela encosta perto da borda do tampo), fora
# de onde a nossa mão cai quando Morel vence (x ~197, y ~82); a colher solta dentro dela, com o cabo apoiado na borda
TIGELA_FIM = (57, 2)   # varrida para a direita, na mesma profundidade (no tampo, longe da borda de lá)
# o braço esquerdo de Morel: em repouso (o da cena), pegando a tigela pela borda de cá e da direita, e no colo
ESQ_REPOUSO = dict(S=(206, 46), E=(221, 67), W=(209, 74), M=(202, 75))


# ------------------------------------------------------------------ ajudas
def _img(px):
    a = np.zeros((96, 320, 4), np.uint8)
    for (x, y), c in px.items():
        if 0 <= x < 320 and 0 <= y < 96:
            a[y, x] = c
    return Image.fromarray(a, "RGBA")


def _pixels(img, dx=0, dy=0):
    a = np.array(img.convert("RGBA"))
    ys, xs = np.nonzero(a[:, :, 3])
    return {(int(x) + dx, int(y) + dy): tuple(int(v) for v in a[y, x]) for y, x in zip(ys, xs)}


def _mover(px, dx, dy):
    return {(x + dx, y + dy): c for (x, y), c in px.items()}


def _escurece(cor, f=0.68):
    return (int(cor[0] * f), int(cor[1] * f), int(cor[2] * f), 255)


def sombra_de(figura, embaixo, f=0.68):
    """A sombra de um pixel (do lado oposto à vela: para a direita e para baixo) que `figura` faz em `embaixo`."""
    out = {}
    for (x, y) in figura:
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            q = (x + dx, y + dy)
            if q not in figura and q not in out and q in embaixo:
                out[q] = _escurece(embaixo[q], f)
    return out


def ik2(S, W, L1, L2, lado):
    """O cotovelo na tela com o braço e o antebraço de comprimentos L1 e L2, dobrando para o lado `lado` (+1: à
    esquerda de quem vai do ombro à mão, na tela)."""
    d = min(math.dist(S, W), L1 + L2 - 0.01)
    ux, uy = (W[0] - S[0]) / math.dist(S, W), (W[1] - S[1]) / math.dist(S, W)
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d)
    hh = math.sqrt(max(L1 * L1 - a * a, 0))
    nx, ny = uy * lado, -ux * lado
    return (S[0] + ux * a + nx * hh, S[1] + uy * a + ny * hh)


def _ease(t):
    return t * t * (3 - 2 * t)


def _lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


# ------------------------------------------------------------------ a mesa
def tigela_e_colher(off, solta):
    """A tigela (o desenho da cena) deslocada `off`, e a colher solta dentro dela, onde a mão a largou (a da pose de
    repouso da cena: o cabo sobre a borda da esquerda, a ponta mergulhada no caldo)."""
    t = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    OB.tigela(t)
    out = _pixels(t, *off)
    if solta:
        rep = _repouso()
        W, T, d = rep["W"], rep["T"], rep["dir_colher"]
        colher = MO.colher((W[0] + d[0] * 5, W[1] + d[1] * 5), T, mergulha=MO.no_caldo)
        out.update(_mover({q: c for q, c in colher.items() if not MO.atras_da_borda(*q)}, *off))
    return out


def objetos_sem_tigela():
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    OB.castical(im)
    OB.vela(im)
    OB.caneca(im)
    OB.pao(im)
    return _pixels(im)


# ------------------------------------------------------------------ o nosso antebraço
def nosso_antebraco(N, pn, deita=0.0):
    """O nosso antebraço do cotovelo `N` ao punho `pn` (no espaço), em perspectiva: a forma afunilando do cotovelo (perto
    da câmera, grosso) ao punho, a lã em quatro tons pela luz da vela, o punho da manga escuro no fim. `deita` (0 a 1):
    deitando com a palma para cima, a face larga vira para a câmera (o topo largo num tom só aceso, a borda de baixo
    estreita e escura)."""
    A, B = G.tela(N), G.tela(pn)
    ra = R_NOSSO[0] * G.F / N[2]
    rb = R_NOSSO[1] * (1 + 0.2 * deita) * G.F / pn[2]
    L = math.dist(A, B)
    ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
    nx, ny = -uy, ux
    if nx + ny > 0:                    # a normal do lado da luz (para a esquerda e para cima)
        nx, ny = -nx, -ny
    out, ante = {}, set()
    x0, x1 = int(min(A[0], B[0]) - ra - 2), int(max(A[0], B[0]) + ra + 2)
    y0, y1 = int(min(A[1], B[1]) - ra - 2), int(max(A[1], B[1]) + ra + 2)
    for y in range(max(0, y0), min(96, y1 + 1)):
        for x in range(max(0, x0), min(320, x1 + 1)):
            px, py = x + 0.5 - A[0], y + 0.5 - A[1]
            t = max(0.0, min(1.0, (px * ux + py * uy) / L))
            r = ra + (rb - ra) * t
            cx, cy = A[0] + ux * L * t, A[1] + uy * L * t
            dd = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if dd > r:
                continue
            v = ((x + 0.5 - cx) * nx + (y + 0.5 - cy) * ny) / r        # 1 do lado da luz, -1 do outro
            lim = (0.62, -0.25 - 0.4 * deita, -0.72)
            cor = LA["j"] if v > lim[0] else LA["a"] if v > lim[1] else LA["b"] if v > lim[2] else LA["c"]
            if t * L > L - 2.2:
                cor = LA_PUNHO[0] if v > -0.3 else LA_PUNHO[1]                 # o punho da manga
            out[(x, y)] = cor
            ante.add((x, y))
    return out


# ------------------------------------------------------------------ a pega (o método da queda-vista)
def _un(v):
    n = math.sqrt(sum(a * a for a in v))
    return tuple(a / n for a in v)


def _soma(*vs):
    return tuple(sum(c) for c in zip(*vs))


def _vezes(v, s):
    return tuple(a * s for a in v)


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cruz(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def pega(p, firme=True):
    """As duas mãos fechadas uma na outra: {(x, y): cor}. Cada punho é um volume na ponta do antebraço; na tela, cada
    pixel fica com a superfície mais perto da câmera. Os dedos de quem está por trás aparecem como uma tira sobre o
    dorso que a câmera vê, perto dos nós; um pixel de sombra separa as duas peles onde uma passa atrás da outra."""
    T = p["lado_t"]
    P = p["pega"]
    para_camera = _un(_vezes(P, -1))
    maos = {}
    for quem, pulso, mao, sinal in (("morel", p["pulso_m"], p["mao_m"], -1), ("nos", p["pulso_n"], p["mao_n"], 1)):
        eixo = _un(_soma(mao, _vezes(pulso, -1)))
        centro = _soma(mao, _vezes(eixo, -1.2), _vezes(T, -sinal * (1.2 if firme else 0.0)))
        maos[quem] = dict(centro=centro, eixo=eixo, dorso=_vezes(T, sinal))
    px = {}
    for quem, m in maos.items():
        lat = _un(_cruz(m["eixo"], _cruz(T, m["eixo"]))) if abs(_dot(T, m["eixo"])) < 0.99 else T
        prof = _un(_cruz(m["eixo"], lat))
        eixos = ((m["eixo"], RAIO_PUNHO[0]), (lat, RAIO_PUNHO[1]), (prof, RAIO_PUNHO[2]))
        n = 14
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                for k in range(-n, n + 1):
                    u, v, w = i / n, j / n, k / n
                    if u * u + v * v + w * w > 1:
                        continue
                    q = _soma(m["centro"], *[_vezes(e, r * s) for (e, r), s in zip(eixos, (u, v, w))])
                    if q[1] < 0.3:   # nada atravessa o tampo
                        continue
                    x, y = G.tela(q)
                    k2 = (math.floor(x), math.floor(y))
                    if k2 in px and px[k2][0] <= q[2]:
                        continue
                    nrm = _un(_soma(*[_vezes(e, s / r) for (e, r), s in zip(eixos, (u, v, w))])) if (u or v or w) \
                        else eixos[0][0]
                    px[k2] = (q[2], quem, nrm, u)
    pele = {"morel": PELE_MOREL_PEGA, "nos": PELE_NOSSA}
    out, dono = {}, {}
    for q, (z, quem, nrm, u) in px.items():
        s = _dot(nrm, _un(LUZ_MUNDO))
        d = quem
        if firme and _dot(maos[quem]["dorso"], para_camera) > 0.05 and _dot(nrm, maos[quem]["dorso"]) > 0.25 \
                and u > -0.15:
            d = "nos" if quem == "morel" else "morel"   # a tira dos dedos de quem está por trás, sobre este dorso
            s -= 0.15
        dono[q] = d
        cor = pele[d]
        out[q] = cor[0] if s > 0.5 else cor[1] if s > -0.2 else cor[2]
    for (x, y), d in list(dono.items()):
        if any(dono.get(v) not in (None, d) and px[v][0] < px[(x, y)][0] for v in ((x - 1, y), (x, y - 1), (x - 1, y - 1))):
            out[(x, y)] = pele[d][2]
    return out


def recuo(m, ante, S, E, W):
    """Com o braço muito dobrado na tela, o braço de cima recua meio degrau atrás do antebraço, longe da junta, e a
    sombra do antebraço nele fica com dois pixels (o método da queda-vista). Muda `m` no lugar."""
    tons = MO.COURO
    a, b = (S[0] - E[0], S[1] - E[1]), (W[0] - E[0], W[1] - E[1])
    cos = (a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))
    if cos < math.cos(math.radians(50)):
        return
    desce = {tons["j"]: tons["a"], tons["a"]: tons["b"], tons["b"]: tons["c"], tons["c"]: tons["l"]}
    L1 = math.dist(S, E)
    for q, cor in list(m.items()):
        if q in ante or cor not in desce:
            continue
        t, _ = MG._seg((q[0] + 0.5, q[1] + 0.5), S, E)
        if any((q[0] - dx, q[1] - dy) in ante for dx in (1, 2) for dy in (0, 1, 2)):
            m[q] = tons["c"] if cor != tons["l"] else cor
        elif (1 - t) * L1 > 5:
            m[q] = desce[cor]


# ------------------------------------------------------------------ as poses
def _repouso():
    """O braço da colher na pose de repouso da cena (juntas.py, a pose `repousa`)."""
    return next(p for p in J.poses() if p["nome"] == "repousa")


def _un2(a, b):
    n = math.dist(a, b)
    return ((b[0] - a[0]) / n, (b[1] - a[1]) / n)


def _varrida(f):
    """O braço direito varrendo a tigela (f de 0 a 1): o antebraço deitado no tampo, de lado, a mão de cutelo (o lado
    de fora, o do dedo mínimo) encostada na borda da esquerda da tigela, empurrando-a para a direita; o cotovelo
    desliza junto pelo tampo, à frente do corpo (o tronco se inclina para alcançar: `tronco` na pose). Devolve o
    cotovelo, o punho e o centro da mão, na tela."""
    ox = TIGELA_FIM[0] * _ease(f)
    mao = (141.5 + ox, 72.5)          # a mão encostada na borda da esquerda da tigela (x 147,5 + o deslocamento)
    W = (mao[0] - 4.5, mao[1] - 0.5)
    E = (W[0] - 27.0, W[1] - 1.0)      # o antebraço deitado, quase horizontal na tela
    return E, W, mao


def _set_dir():
    """O braço direito pronto para a pega: o cotovelo no tampo, a mão aberta no alto (a pose do meio, antes de fechar)."""
    p = G.pose(0.0)
    t = p["tela"]
    return t["S"], t["E"], t["W"]


def _entrada(t):
    """O nosso punho entrando pela borda de baixo até a mão dele (t de 0 a 1), no espaço: de baixo e de perto até o
    punho da pose do meio."""
    p = G.pose(0.0)
    fim = p["pulso_n"]
    ini = (fim[0] + 4, 14.0, 47.0)
    a = _lerp(ini, fim, _ease(t))
    # o caminho sobe em arco (a mão vem de baixo, não em linha reta pela mesa)
    a = (a[0], a[1] + 4 * math.sin(math.pi * t), a[2])
    return a


ROTEIRO = []   # (nome, dict da pose); preenchido abaixo


def _p(nome, **k):
    ROTEIRO.append((nome, k))


# a preparação: o repouso olhando para nós; a mão solta a colher; a esquerda pega a tigela e a desliza; a esquerda desce
# ao colo; o braço direito vai para o meio; o nosso antebraço entra; a pega se firma
_p("olha", dir="colher", esq="repouso", tigela=0.0, cabeca="olha")
_p("solta", dir=("solta", 0.0), esq="repouso", tigela=0.0, cabeca="baixo")
_p("esq_sai", dir=("solta", 0.0), esq=("sai", 0.5), tigela=0.0, cabeca="baixo")
_p("colo", dir=("solta", 0.0), esq="colo", tigela=0.0, cabeca="baixo")
_p("encosta", dir=("varre", -1.0), esq="colo", tigela=0.0, cabeca="baixo")
for i, f in enumerate((0.0, 0.15, 0.4, 0.68, 0.9, 1.0)):
    _p(f"varre{i + 1}", dir=("varre", f), esq="colo", tigela=f, cabeca="baixo",
       tronco=(round(7 * _ease(f)), 1 if f > 0.3 else 0))
for i, f in enumerate((0.3, 0.65, 1.0)):
    _p(f"apoia{i + 1}", dir=("apoia", f), esq="colo", tigela=1.0, cabeca="olha", nosso=(f * 0.6 if i else None),
       tronco=(round(7 * (1 - _ease(f))), 0))
_p("entra1", dir=("apoia", 1.0), esq="colo", tigela=1.0, cabeca="olha", nosso=0.75)
_p("entra2", dir=("apoia", 1.0), esq="colo", tigela=1.0, cabeca="olha", nosso=1.0)
_p("firma", duelo=0.0, tronco=(0, 0), firme=False)
# a disputa e os derrubes: a fração do caminho até o fim, o lado (-1: nós vencendo, para a esquerda da imagem; +1: Morel
# vencendo), o tronco dele (px na tela: pende 1 px para o lado em que força, cede quando perde, vem por cima quando vence)
_p("disputa", duelo=0.0, tronco=(0, 1))
_p("pende_m1", duelo=0.04, tronco=(1, 1))
_p("pende_m2", duelo=0.08, tronco=(1, 1))
_p("pende_n1", duelo=-0.04, tronco=(0, 1))
_p("pende_n2", duelo=-0.08, tronco=(-1, 1))
for i, f in enumerate((0.13, 0.22, 0.35, 0.52, 0.72, 0.9)):
    _p(f"nos_{i + 1}", duelo=-f, tronco=(-1, 1 + (i >= 3)))
    _p(f"morel_{i + 1}", duelo=f, tronco=(1 + (i >= 2), 1 + (i >= 4)))
_p("nos_fim", duelo=-1.0, tronco=(-1, 2))
_p("morel_fim", duelo=1.0, tronco=(2, 2))
# o depois: soltam as mãos; o nosso antebraço sai por baixo; o braço dele volta a pousar no tampo
for lado in ("nos", "morel"):
    _p(f"{lado}_solta", duelo=-1.0 if lado == "nos" else 1.0, tronco=(0, 1), firme=False, separa=True)
    _p(f"{lado}_sai", depois=0.5, lado=lado)
_p("depois", depois=1.0)
POSES = dict(ROTEIRO)

# A linha do tempo (pose, tiques de 100 ms). A preparação: o olhar e a colher solta sem pressa; a tigela desliza devagar
# no começo e no fim (a mão acompanha); o braço vai ao meio e o nosso entra; a pega se firma e segura. A disputa com
# intenção (o método da queda-vista): quem perde ganha um pouco primeiro e segura, o outro recupera; as poses seguram de
# 3 a 8 tiques. O derrube começa devagar e acelera até o tampo (1 tique cada); a pausa no fim; as mãos se soltam e o
# nosso braço sai por baixo; o depois fica (a conversa continua no texto).
PREPARO = [("olha", 6), ("solta", 4), ("esq_sai", 2), ("colo", 3), ("encosta", 2), ("varre1", 3), ("varre2", 2),
           ("varre3", 2), ("varre4", 2), ("varre5", 2), ("varre6", 3), ("apoia1", 2), ("apoia2", 2), ("apoia3", 3),
           ("entra1", 2), ("entra2", 3), ("firma", 6)]
ESPERA = [("disputa", 4), ("pende_m1", 3), ("disputa", 4), ("pende_n1", 3)]   # enquanto o motor não disse o resultado
_DISPUTA = {
    "nos": [("disputa", 6), ("pende_m1", 3), ("pende_m2", 8), ("pende_m1", 4), ("disputa", 3), ("pende_n1", 3),
            ("pende_n2", 6), ("pende_n1", 4), ("disputa", 5)],
    "morel": [("disputa", 6), ("pende_n1", 3), ("pende_n2", 8), ("pende_n1", 4), ("disputa", 3), ("pende_m1", 3),
              ("pende_m2", 6), ("pende_m1", 4), ("disputa", 5)],
}
_DERRUBE = {
    "nos": [("pende_n1", 2), ("pende_n2", 3), ("nos_1", 2), ("nos_2", 2), ("nos_3", 1), ("nos_4", 1), ("nos_5", 1),
            ("nos_6", 1), ("nos_fim", 22), ("nos_solta", 5), ("nos_sai", 3), ("depois", 1)],
    "morel": [("pende_m1", 2), ("pende_m2", 3), ("morel_1", 2), ("morel_2", 2), ("morel_3", 1), ("morel_4", 1),
              ("morel_5", 1), ("morel_6", 1), ("morel_fim", 22), ("morel_solta", 5), ("morel_sai", 3), ("depois", 1)],
}
TEMPO = {k: _DISPUTA[k] + _DERRUBE[k] for k in _DISPUTA}   # depois da preparação; a última pose fica
# movimento reduzido: a pose do meio enquanto duram a preparação e a disputa, o fim e o depois, sem passagens
REDUZIDO = {k: [("disputa", sum(n for _, n in PREPARO + _DISPUTA[k])),
                (f"{k}_fim", sum(n for _, n in _DERRUBE[k][:-3])), ("depois", 1)] for k in _DISPUTA}


def _pose_duelo(f):
    """A pose da disputa a uma fração `f` do caminho até o fim (negativa: nós vencendo)."""
    return G.pose(f * G.fi_fim())


def construir(nome):
    """As camadas de Morel, da mesa e do nosso braço na pose `nome`: {camada: {(x, y): cor}} e as juntas."""
    k = POSES[nome]
    rep = _repouso()
    tronco = k.get("tronco", (0, 0))
    if "depois" in k:
        tronco = (0, 0)
    dx, dy = tronco
    corpo = _mover(MO.tronco(0), dx, dy)
    cab = k.get("cabeca", "olha")
    c = dict(espada=_mover(MO.espada(0), dx, dy), morel_corpo=corpo,
             morel_cabeca=MO.cabeca(cab, dy if cab != "olha" else dy - 1))
    c["morel_cabeca"] = _mover(c["morel_cabeca"], dx, 0)
    tig = k.get("tigela", 1.0)
    off = tuple(round(v * _ease(tig)) for v in TIGELA_FIM) if tig else (0, 0)
    c["tigela"] = tigela_e_colher(off, solta=k.get("dir") != "colher")
    juntas = {}
    # o braço esquerdo de Morel
    esq = k.get("esq", "colo")
    S_esq = (ESQ_REPOUSO["S"][0] + dx, ESQ_REPOUSO["S"][1] + dy)
    atras = False
    if esq == "repouso":
        E, W, M, mao = ESQ_REPOUSO["E"], ESQ_REPOUSO["W"], ESQ_REPOUSO["M"], (8.0, 5.0)
    elif esq == "colo":
        E, W, M, mao, atras = (214 + dx, 72 + dy), (213 + dx, 94), None, None, True
    else:                                         # saindo: a mão sobe do tampo e volta para o corpo, a caminho do colo
        _, f = esq
        M = _lerp(ESQ_REPOUSO["M"], (216, 71), f)
        W = (M[0] + 5, M[1] - 2)
        E = _lerp(ESQ_REPOUSO["E"], (219, 70), f)
        mao = (7.0, 5.0)
    esq_px, _ = MO.braco(S_esq, E, W, corpo)
    if M is not None:
        esq_px.update(MO.mao(M, *mao))
    esq_px.update(_mover(MO.ombreira_esquerda(0), dx, dy))
    if atras:
        # no colo: o braço desce atrás do tampo (a mesa, por cima, esconde o antebraço); a ombreira fica na frente
        c["morel_esquerdo_atras"] = esq_px
        c["morel_esquerdo"] = _mover(MO.ombreira_esquerda(0), dx, dy)
    else:
        c["morel_esquerdo"] = esq_px
    juntas.update({"S": S_esq, "E": E, "W": W})
    # o braço direito de Morel, a mão, e o nosso
    dir_ = {}
    nosso = {}
    maos = {}
    if k.get("dir") == "colher":
        S, E, W = rep["S"], rep["E"], rep["W"]
        dir_, ante = MO.braco(S, E, W, corpo)
        d = rep["dir_colher"]
        colher = MO.colher((W[0] + d[0] * 5, W[1] + d[1] * 5), rep["T"], mergulha=MO.no_caldo)   # como na cena
        dir_.update({q: cor for q, cor in colher.items() if not MO.atras_da_borda(*q)})
        dir_.update(MO.mao((W[0] + d[0] * 3, W[1] + d[1] * 3), 6.5, 5.5))
    elif "dir" in k:
        modo, f = k["dir"]
        S = (rep["S"][0] + dx, rep["S"][1] + dy)
        W0 = (rep["W"][0] + 1, rep["W"][1] - 3)     # a mão sobe um pouco: largou a colher
        if modo == "solta":
            E, W = rep["E"], W0
            u = _un2(E, W)
            mao_c = (W[0] + u[0] * 4, W[1] + u[1] * 4)
        else:
            E, W, mao_c = _varrida(f if modo == "varre" else 1.0)
            if modo == "varre" and f < 0:           # descendo da colher para o tampo, ao lado da tigela
                E1, W1, m1 = _varrida(0.0)
                E, W, mao_c = _lerp(rep["E"], E1, 0.6), _lerp(W0, W1, 0.6), _lerp((W0[0] + 3, W0[1]), m1, 0.6)
            if modo == "apoia":                     # do fim da varrida ao meio da mesa, pronto para a pega
                Sd, Ed, Wd = _set_dir()
                fe = _ease(f)
                W = _lerp(W, Wd, fe)
                E = _lerp(E, Ed, fe)
                E = (E[0], E[1] - 4 * math.sin(math.pi * f))  # o cotovelo sobe um pouco no caminho e volta a pousar
                u = _un2(E, W)
                mao_c = (W[0] + u[0] * 4, W[1] + u[1] * 4)
        dir_, ante = MO.braco(S, E, W, corpo)
        recuo(dir_, ante, S, E, W)
        dir_.update(MO.mao(mao_c, 6.0, 5.5 if modo == "varre" else 6.5))
        if k.get("nosso") is not None:
            pw = _entrada(k["nosso"])
            nosso = nosso_antebraco(G.COTOVELO_NOSSO, pw)
            q = G.tela(pw)
            ue = _un(_soma(pw, _vezes(G.COTOVELO_NOSSO, -1)))
            mc = G.tela(_soma(pw, _vezes(ue, 4.5)))
            r = 3.4 * G.F / pw[2]
            maos = _bola(mc, r * 1.05, r, PELE_NOSSA)
            juntas.update({"Wn": q})
    elif "duelo" in k:
        p = _pose_duelo(k["duelo"])
        t = p["tela"]
        S = (t["S"][0] + dx, t["S"][1] + dy)
        E, W = t["E"], t["W"]
        dir_, ante = MO.braco(S, E, W, corpo)
        recuo(dir_, ante, S, E, W)
        deita = max(0.0, min(1.0, (k["duelo"] - 0.3) / 0.6))
        nosso = nosso_antebraco(G.COTOVELO_NOSSO, p["pulso_n"], deita)
        if k.get("separa"):
            # as mãos se soltam: cada uma volta a ser uma bolinha na ponta do seu antebraço
            um = _un(_soma(p["mao_m"], _vezes(p["pulso_m"], -1)))
            maos = _bola(G.tela(_soma(p["mao_m"], _vezes(um, -1.0))), 6.0, 5.0, MO.PELE_MAO)
            un_ = _un(_soma(p["mao_n"], _vezes(p["pulso_n"], -1)))
            r = 3.4 * G.F / p["mao_n"][2]
            maos.update(_bola(G.tela(_soma(p["mao_n"], _vezes(un_, -0.5))), r * 1.05, r, PELE_NOSSA))
        else:
            maos = pega(p, firme=k.get("firme", True))
        juntas.update({"Wn": t["Wn"], "P": t["P"]})
    else:   # o depois: o braço dele pousado no tampo, à frente do peito; o nosso saindo por baixo
        f = k["depois"]
        S = (rep["S"][0], rep["S"][1])
        E, W = (128, 70), (150, 73)
        dir_, ante = MO.braco(S, E, W, corpo)
        dir_.update(MO.mao((155, 74), 7.0, 5.0))
        if f < 1.0:
            lado = k["lado"]
            p = _pose_duelo(-0.75 if lado == "nos" else 0.75)
            pw = _lerp(p["pulso_n"], _entrada(0.0), 0.6)
            nosso = nosso_antebraco(G.COTOVELO_NOSSO, pw)
            ue = _un(_soma(pw, _vezes(G.COTOVELO_NOSSO, -1)))
            r = 3.4 * G.F / pw[2]
            maos = _bola(G.tela(_soma(pw, _vezes(ue, 4.5))), r * 1.05, r, PELE_NOSSA)
    for q, cor in MO.ombreira_direita(S).items():
        if q not in ante:
            dir_[q] = cor
    c["morel_braco"] = dir_
    c["nosso_braco"] = nosso
    c["maos"] = maos
    juntas.update({"Sd": S, "Ed": E, "Wd": W})
    return c, juntas


def _bola(c, rx, ry, tons):
    """Uma mão em bolinha (a luz em cima à esquerda, a vela), com os tons dados."""
    out = {}
    for y in range(math.floor(c[1] - ry), math.ceil(c[1] + ry) + 1):
        for x in range(math.floor(c[0] - rx), math.ceil(c[0] + rx) + 1):
            u, v = (x + 0.5 - c[0]) / rx, (y + 0.5 - c[1]) / ry
            if u * u + v * v <= 1:
                s = -u * 0.7 - v * 0.7
                out[(x, y)] = tons[0] if s > 0.3 else tons[1] if s > -0.5 else tons[2]
    return out


# ------------------------------------------------------------------ as camadas, a guia e a fonte
def estaticas():
    parede = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    ES.parede_fundo(parede)
    ES.parede_lateral(parede)
    ES.esteio(parede, *ES.CANTO)
    ES.esteio(parede, *ES.ESTEIO_DIR)
    mesa = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    ES.tampo(mesa)
    return dict(parede=_pixels(parede), mesa=_pixels(mesa), objetos=objetos_sem_tigela())


def guia(nome, juntas):
    """A construção (oculta): os ossos dos dois braços em linha, as juntas em cruz, o círculo da pega e os dois fins,
    e o lugar do nosso cotovelo, fora do quadro."""
    out = {}

    def linha(a, b, cor):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
        for i in range(n + 1):
            out[(round(a[0] + (b[0] - a[0]) * i / n - 0.5), round(a[1] + (b[1] - a[1]) * i / n - 0.5))] = cor
    osso, nosso, circ = (255, 210, 60, 255), (90, 200, 255, 255), (255, 80, 200, 255)
    centro, r, cima, lado, _ = G.circulo()
    fim = G.fi_fim()
    for i in range(121):
        fi = -fim + 2 * fim * i / 120
        q = G.tela(_soma(centro, _vezes(cima, r * math.cos(fi)), _vezes(lado, r * math.sin(fi))))
        out[(round(q[0] - 0.5), round(q[1] - 0.5))] = circ
    if "Ed" in juntas:
        linha(juntas["Sd"], juntas["Ed"], osso)
        linha(juntas["Ed"], juntas["Wd"], osso)
    if "Wn" in juntas:
        linha(G.tela(G.COTOVELO_NOSSO), juntas["Wn"], nosso)
    linha(juntas["S"], juntas["E"], osso)
    linha(juntas["E"], juntas["W"], osso)
    return out


def quadros():
    """[(nome, {camada: Image})], na ordem do ROTEIRO."""
    fix = estaticas()
    out = []
    for nome, _ in ROTEIRO:
        c, jj = construir(nome)
        cam = {n: _img(fix[n]) if n in fix else _img(c.get(n, {})) for n in CAMADAS if n not in OCULTAS}
        cam["construcao"] = _img(guia(nome, jj))
        jp = {}
        for kk, cor in (("Sd", (255, 64, 64, 255)), ("Ed", (48, 255, 96, 255)), ("Wd", (48, 128, 255, 255))):
            if kk in jj:
                jp[(round(jj[kk][0] - 0.5), round(jj[kk][1] - 0.5))] = cor
        cam["juntas"] = _img(jp)
        out.append((nome, cam))
    return out


def compor(c, guias=False):
    im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
    for n in CAMADAS:
        if n in OCULTAS and not (guias and n == "construcao"):
            continue
        im.alpha_composite(c[n])
    return im


def previa(saida, guias=False, so=None):
    saida = pathlib.Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    for i, (nome, c) in enumerate(quadros()):
        if so and nome not in so:
            continue
        compor(c, guias).save(saida / f"{i:02d}-{nome}.png")
    print(f"prévia em {saida}")


_MONTAR = r'''
local D = dofile(app.params["dados"])
local s = Sprite(320, 96, ColorMode.RGB)
s.layers[1].name = D.camadas[1]
for i = 2, #D.camadas do local l = s:newLayer(); l.name = D.camadas[i] end
for i = 2, #D.quadros do s:newEmptyFrame() end
local n = 0
for i, nome in ipairs(D.quadros) do
  local t = s:newTag(i, i); t.name = nome
  s.frames[i].duration = 0.1
  for j, c in ipairs(D.camadas) do
    local arq = app.params["pasta"] .. "/" .. c .. "-" .. (i - 1) .. ".png"
    local f = io.open(arq, "r")
    if f then
      f:close()
      s:newCel(s.layers[j], s.frames[i], Image{ fromFile = arq }, Point(0, 0))
      n = n + 1
    end
  end
end
for _, l in ipairs(s.layers) do
  if D.ocultas[l.name] then l.isVisible = false end
end
s:saveAs(app.params["saida"])
print("montada: " .. n .. " células")
'''


def criar(refazer=False):
    from exportar_aseprite import aseprite
    if FONTE.exists() and not refazer:
        sys.exit(f"{FONTE.name} já existe e é a autoridade; use --refazer para descartar os retoques e montar de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        nomes = []
        for i, (nome, c) in enumerate(quadros()):
            nomes.append(nome)
            for camada in CAMADAS:
                if c[camada].getbbox():
                    c[camada].save(tmp / f"{camada}-{i}.png")
        dados = tmp / "dados.lua"
        dados.write_text("return {camadas={" + ",".join(f'"{c}"' for c in CAMADAS) + "}, quadros={"
                         + ",".join(f'"{q}"' for q in nomes) + "}, ocultas={"
                         + ",".join(f'["{c}"]=true' for c in OCULTAS) + "}}", encoding="utf-8")
        lua = tmp / "montar.lua"
        lua.write_text(_MONTAR, encoding="utf-8")
        r = subprocess.run([aseprite(), "-b", "--script-param", f"dados={dados}", "--script-param", f"pasta={tmp}",
                            "--script-param", f"saida={FONTE}", "--script", str(lua)], capture_output=True, text=True)
        ok = [x for x in r.stdout.splitlines() if x.startswith("montada")]
        if not ok or not FONTE.exists():
            sys.exit(f"o Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(ok[0], f"({len(nomes)} poses)")


if __name__ == "__main__":
    if "--refazer" in sys.argv and "--sem-os-retoques" not in sys.argv:
        sys.exit("A fonte está no jogo desde a 1.220.0 (taverna/jogo.py): refazê-la do código descarta o que foi "
                 "retocado nela. Para isso mesmo, junte --sem-os-retoques.")
    if "--previa" in sys.argv:
        so = [a for a in sys.argv[2:] if not a.startswith("--")][1:] or None
        previa([a for a in sys.argv[2:] if not a.startswith("--")][0], "--guia" in sys.argv, so)
    elif "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
