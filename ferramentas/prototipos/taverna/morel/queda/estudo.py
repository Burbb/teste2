"""O estudo de construção da queda de braço (protótipo): formas simples sobre a vista de Morel, antes de vestir.

    python ferramentas/prototipos/taverna/morel/queda/estudo.py --criar     # monta estudo-queda.aseprite (só se não existir)
    python ferramentas/prototipos/taverna/morel/queda/estudo.py             # exporta a folha de inspeção

Pela skill `arte-personagens-fenda` (passo 3): a cabeça, o tronco (um ovo), a barra das clavículas com os ombros nas
pontas, os braços em cápsulas de cores (o braço de cima, o antebraço, a mão; Morel em vermelho e laranja, nós em azul),
o tampo, a tigela no lugar novo, e numa camada `guia` as juntas (o ombro, o cotovelo, o pulso, o meio da pega) e o arco
que a pega pode percorrer (o círculo de `juntas.py`, de um fim ao outro, passando pelo alto). As juntas saem de
`juntas.py`; ninguém posiciona o cotovelo ou a mão na tela à mão. Nada de roupa, textura ou luz.

Os quadros (um por etiqueta):
1. `disputa`, 2. `vitoria_jogador`, 3. `vitoria_morel`: as poses sobre a vista escurecida (a camada `referencia`);
4. `planta`: a mesa vista de cima (o tampo, os cotovelos, a linha entre eles, o caminho da pega no chão do tampo, os
   dois fins, a tigela empurrada, a vela, a caneca e o pão), para conferir o espaço e o lado de cada vitória;
5. `pega`: as duas mãos na pega, ampliadas (cada pixel do quadro é ~1/3 de um pixel da cena), desenhadas à mão em grade:
   o nosso dorso na frente, os nossos dedos dobrados sobre o dorso da mão dele (à esquerda), os dedos dele sobre o
   nosso dorso (à direita), os polegares cruzados em cima (o nosso por cima), os punhos continuando os antebraços.
   É a pega que funciona; a da cena é ela simplificada em bolinhas de pele (a memória "mãos de cena sem dedos")."""
import math
import pathlib
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import fonte_aseprite as fa  # noqa: E402
import juntas as J  # noqa: E402

FONTE = AQUI / "estudo-queda.aseprite"
VISTA = AQUI.parents[1] / "camadas" / "morel-vista"
SAIDA = VISTA / "queda-estudo.png"
QUADROS = ["disputa", "vitoria_jogador", "vitoria_morel", "planta", "pega"]
CAMADAS = ["referencia", "mesa", "corpo", "morel_braco", "morel_antebraco", "morel_mao", "nosso_braco",
           "nosso_antebraco", "nossa_mao", "objetos", "guia"]
COR = {
    "mesa": (120, 96, 60), "borda": (170, 140, 90), "corpo": (110, 110, 130), "cabeca": (150, 150, 170),
    "clavicula": (200, 200, 220), "morel_braco": (200, 60, 50), "morel_antebraco": (235, 130, 50),
    "morel_mao": (250, 210, 80), "nosso_braco": (40, 70, 160), "nosso_antebraco": (70, 130, 230),
    "nossa_mao": (130, 220, 240), "tigela": (150, 90, 160), "objeto": (90, 160, 90),
    "junta": (255, 255, 255), "arco": (255, 240, 120), "linha": (255, 120, 220),
}
# os raios das cápsulas na tela (px), pelo porte: Morel tem braços de 11 px (a vista aprovada); o nosso antebraço está
# mais perto da câmera, mais grosso no cotovelo do que no pulso
RAIO = {"morel_braco": (5.5, 5.0), "morel_antebraco": (5.0, 3.8), "morel_mao": 3.6,
        "nosso_braco": (7.0, 7.5), "nosso_antebraco": (6.5, 4.4), "nossa_mao": 3.9}
# o braço esquerdo de Morel (sem juntas calculadas: ele só se apoia): o ombro e o cotovelo do corpo aprovado (do ombro
# em (238, 35) ao cotovelo em (247, 61), deslocados com o tronco) e a mão plantada no tampo à direita do nosso
# antebraço, diante do pão (as mesmas de poses.py)
_MAO_ESQ = {"disputa": (264, 70), "vitoria_jogador": (262, 71), "vitoria_morel": (265, 70)}


def _esquerdo(nome):
    s = J.tela(J.OMBRO_MOREL[nome])
    dx, dy = round((round(s[0]) - 198) / 2), round((round(s[1]) - 35) / 2)
    return (238 + dx, 35 + dy), (247 + dx, 61 + dy), _MAO_ESQ[nome]


# a tigela empurrada para a direita dele, rente à borda de lá (o retângulo dela na tela)
TIGELA = (150, 63, 188, 82)


def _capsula(px, cor, a, b, ra, rb):
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    L2 = max(dx * dx + dy * dy, 1e-6)
    r = max(ra, rb)
    for y in range(int(min(ay, by) - r) - 1, int(max(ay, by) + r) + 2):
        for x in range(int(min(ax, bx) - r) - 1, int(max(ax, bx) + r) + 2):
            t = max(0.0, min(1.0, ((x + 0.5 - ax) * dx + (y + 0.5 - ay) * dy) / L2))
            rr = ra + (rb - ra) * t
            if (x + 0.5 - ax - t * dx) ** 2 + (y + 0.5 - ay - t * dy) ** 2 <= rr * rr:
                px[(x, y)] = cor


def _disco(px, cor, c, r):
    _capsula(px, cor, c, c, r, r)


def _linha(px, cor, a, b, passo=1):
    (x0, y0), (x1, y1) = a, b
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for k in range(0, int(n) + 1, passo):
        px[(round(x0 + (x1 - x0) * k / n), round(y0 + (y1 - y0) * k / n))] = cor


def _cruz(px, cor, c):
    x, y = round(c[0]), round(c[1])
    for d in (-1, 0, 1):
        px[(x + d, y)] = cor
        px[(x, y + d)] = cor


def _referencia():
    """A vista sem Morel nem a mesa posta, escurecida: a sala e o tampo vazio, só para situar."""
    fundo = Image.open(VISTA / "fundo.png").convert("RGBA")
    a = np.array(fundo).astype(float)
    a[:, :, :3] *= 0.45
    return {(x, y): tuple(int(v) for v in a[y, x]) for y in range(96) for x in range(320) if a[y, x, 3] > 0}


def _pose(nome, ref):
    p = J.poses()[nome]
    T = lambda q: J.tela(q)  # noqa: E731
    c = {k: {} for k in CAMADAS}
    c["referencia"] = ref
    # o tampo: as quatro bordas (a de lá em y 62, a de cá em y 92, a da direita até a quina) e o plano em pontilhado
    for y in range(62, 93):
        for x in range(0, 286):
            if (x + y) % 6 == 0:
                c["mesa"][(x, y)] = COR["mesa"]
    _linha(c["mesa"], COR["borda"], (160, 62), (256, 62))
    _linha(c["mesa"], COR["borda"], (0, 92), (286, 92))
    _linha(c["mesa"], COR["borda"], (256, 62), (286, 92))
    # Morel: a cabeça, o pescoço, o tronco (um ovo), as clavículas com os ombros nas pontas (o tronco acompanha o ombro
    # direito, 1 px por 2 dele)
    so = T(p["ombro_m"])
    dx, dy = round((so[0] - 198) / 2), round((so[1] - 35) / 2)
    _disco(c["corpo"], COR["cabeca"], (218 + dx, 15 + dy), 10.5)
    for y in range(26, 64):
        for x in range(196, 246):
            if ((x - 221 - dx) / 23) ** 2 + ((y - 50 - dy) / 22) ** 2 <= 1:
                c["corpo"][(x, y)] = COR["corpo"]
    _linha(c["corpo"], COR["clavicula"], (round(so[0]), round(so[1])), _esquerdo(nome)[0])
    # o braço direito de Morel: o braço de cima, o antebraço, a mão na pega
    _capsula(c["morel_braco"], COR["morel_braco"], so, T(p["cotovelo_m"]), *RAIO["morel_braco"])
    _capsula(c["morel_antebraco"], COR["morel_antebraco"], T(p["cotovelo_m"]), T(p["pulso_m"]), *RAIO["morel_antebraco"])
    _disco(c["morel_mao"], COR["morel_mao"], T(p["pega"]), RAIO["morel_mao"])
    # o esquerdo: o braço de cima, o antebraço e a mão plantada
    o, e, m = _esquerdo(nome)
    _capsula(c["morel_braco"], COR["morel_braco"], o, e, 5.0, 4.6)
    _capsula(c["morel_antebraco"], COR["morel_antebraco"], e, m, 4.6, 3.6)
    _disco(c["morel_mao"], COR["morel_mao"], m, 3.2)
    # nós: o braço de cima saindo pela borda de baixo, o antebraço, a mão na pega (na frente da dele)
    _capsula(c["nosso_braco"], COR["nosso_braco"], T(p["cotovelo_n"]), J.OMBRO_NOSSO_TELA, *RAIO["nosso_braco"])
    _capsula(c["nosso_antebraco"], COR["nosso_antebraco"], T(p["cotovelo_n"]), T(p["pulso_n"]), *RAIO["nosso_antebraco"])
    _disco(c["nossa_mao"], COR["nossa_mao"], T(p["pega"]), RAIO["nossa_mao"])
    # os objetos: a tigela empurrada, a vela, a caneca, o pão
    x0, y0, x1, y1 = TIGELA
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ((x + 0.5 - (x0 + x1) / 2) / ((x1 - x0) / 2)) ** 2 + ((y + 0.5 - (y0 + y1) / 2) / ((y1 - y0) / 2)) ** 2 <= 1:
                c["objetos"][(x, y)] = COR["tigela"]
    for (a, b, w, h) in ((105, 58, 24, 26), (134, 58, 16, 28), (250, 76, 33, 14)):
        for y in range(b, b + h):
            for x in range(a, a + w):
                if x in (a, a + w - 1) or y in (b, b + h - 1):
                    c["objetos"][(x, y)] = COR["objeto"]
    # a guia: o arco da pega (de um fim ao outro, pelo alto), a linha entre os cotovelos, as juntas
    A, B = J.COTOVELO_MOREL, J.COTOVELO_NOSSO
    fim1, _ = J.pega(-1)
    fim2, _ = J.pega(1)
    alto, r = J.pega(0)
    u = J._un(J._sub(B, A))
    centro = J._sub(alto, (0.0, r, 0.0))
    lado = J._un((-u[2], 0.0, u[0]))
    for k in range(-90, 91, 2):
        a = math.radians(k)
        q = J._add(centro, J._add(J._mul((0.0, 1.0, 0.0), r * math.cos(a)), J._mul(lado, r * math.sin(a))))
        if q[1] >= J.TAMPO_MAO - 0.01:
            x, y = T(q)
            c["guia"][(round(x), round(y))] = COR["arco"]
    _linha(c["guia"], COR["linha"], tuple(round(v) for v in T(A)), tuple(round(v) for v in T(B)), passo=2)
    for q in (fim1, fim2):
        _cruz(c["guia"], COR["arco"], T(q))
    for q in (p["ombro_m"], p["cotovelo_m"], p["pulso_m"], p["cotovelo_n"], p["pulso_n"], p["pega"]):
        _cruz(c["guia"], COR["junta"], T(q))
    return c


def _planta():
    """A mesa vista de cima: X (cm) para a direita, a profundidade para cima (longe em cima). 2 px por cm."""
    c = {k: {} for k in CAMADAS}
    P = lambda X, z: (round(160 + X * 1.4), round(92 - (z - 74.5) * 1.15))  # noqa: E731
    for z in (74.5, 144.5):
        _linha(c["mesa"], COR["borda"], P(-110, z), P(40, z))
    _linha(c["mesa"], COR["borda"], P(40, 74.5), P(40, 144.5))
    A, B = J.COTOVELO_MOREL, J.COTOVELO_NOSSO
    _linha(c["guia"], COR["linha"], P(A[0], A[2]), P(B[0], B[2]), passo=2)
    alto, r = J.pega(0)
    fim1, _ = J.pega(-1)
    fim2, _ = J.pega(1)
    _linha(c["guia"], COR["arco"], P(fim1[0], fim1[2]), P(fim2[0], fim2[2]))
    for q, cor in ((A, "morel_antebraco"), (B, "nosso_antebraco")):
        _disco(c[cor], COR[cor], P(q[0], q[2]), 2.5)
    for q in (fim1, fim2, alto):
        _cruz(c["guia"], COR["junta"], P(q[0], q[2]))
    # a tigela empurrada, a vela, a caneca, o pão (os centros, pela vista: z pela linha da tela, X pela coluna)
    def xz(sx, sy):
        z = J.F * J.ALTURA / (sy - J.HOR)
        return (sx - J.CX) * z / J.F, z
    for (sx, sy, rr, cor) in ((169, 73, 9, "tigela"), (142, 84, 3, "objeto"), (117, 82, 4, "objeto"), (266, 86, 5, "objeto")):
        X, z = xz(sx, sy)
        _disco(c["objetos"], COR[cor], P(X, z), rr)
    # os ombros de Morel e o nosso (este, embaixo da câmera, fora do quadro da vista)
    for nome in ("disputa", "vitoria_jogador", "vitoria_morel"):
        o = J.OMBRO_MOREL[nome]
        c["corpo"][P(o[0], o[2])] = COR["morel_braco"]
    return c


# a pega ampliada, à mão: N o nosso dorso, n os nossos dedos (por cima do dorso dele, à esquerda), P o nosso polegar,
# W o nosso antebraço; M a mão dele (o que aparece atrás da nossa), m os dedos dele (sobre o nosso dorso, à direita),
# T o polegar dele, V o antebraço dele. Vista de onde estamos sentados, na disputa.
PEGA = [
    "........................",
    "..........TT............",
    ".........TTPP...........",
    "........TTPPPP..........",
    ".......nMMNNNPP.........",
    "......nnMMNNNNNm........",
    "......nnMMNNNNNmm.......",
    "......nnMMNNNNNmm.......",
    "......nnMMNNNNNmm.......",
    ".......nMMNNNNNm........",
    ".......VVMNNNNN.........",
    "......VVVVNNNNW.........",
    ".....VVVV..WWWWW........",
    "....VVVV...WWWWWW.......",
    "...VVVV.....WWWWWW......",
    "..VVVV.......WWWWWW.....",
    ".VVVV.........WWWWWW....",
    "VVVV...........WWWWWW...",
    "VVV.............WWWWWW..",
    "VV...............WWWWWW.",
]
_PEGA_COR = {"N": ("nossa_mao", (130, 220, 240)), "n": ("nossa_mao", (190, 245, 255)), "P": ("nossa_mao", (60, 170, 255)),
             "W": ("nosso_antebraco", COR["nosso_antebraco"]), "M": ("morel_mao", (250, 210, 80)),
             "m": ("morel_mao", (255, 150, 90)), "T": ("morel_mao", (255, 240, 160)),
             "V": ("morel_antebraco", COR["morel_antebraco"])}


def _pega():
    c = {k: {} for k in CAMADAS}
    E, ox, oy = 4, 112, 8  # cada caractere 4×4 px no quadro, para ler no tamanho nativo da folha
    for y, linha in enumerate(PEGA):
        for x, ch in enumerate(linha):
            if ch in _PEGA_COR:
                cam, cor = _PEGA_COR[ch]
                for dy in range(E):
                    for dx in range(E):
                        c[cam][(ox + x * E + dx, oy + y * E + dy)] = cor
    return c


def criar(refazer=False):
    ref = _referencia()
    pixels = [_pose(n, ref) for n in QUADROS[:3]] + [_planta(), _pega()]
    print(fa.montar(FONTE, 320, 96, CAMADAS, QUADROS, pixels, refazer=refazer))


def exportar():
    """A folha de inspeção: os cinco quadros da fonte, um embaixo do outro, no tamanho nativo (o painel amplia)."""
    with tempfile.TemporaryDirectory() as tmp:
        qs = fa.quadros(FONTE, tmp)
        folha = Image.new("RGBA", (320, 96 * len(qs)), (24, 22, 20, 255))
        for i, q in enumerate(qs):
            folha.alpha_composite(Image.open(q).convert("RGBA"), (0, 96 * i))
    folha.save(SAIDA, optimize=True)
    print(f"{SAIDA.name}: {len(qs)} quadros")


if __name__ == "__main__":
    if "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
    else:
        exportar()
