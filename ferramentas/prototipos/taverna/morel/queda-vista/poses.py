"""A queda de braço na vista aprovada (o "queda 1" refinado; protótipo, nada no jogo): as poses e a fonte.

    python ferramentas/prototipos/taverna/morel/queda-vista/poses.py --previa <pasta>  # as poses recompostas em PNG
    python ferramentas/prototipos/taverna/morel/queda-vista/poses.py --criar           # monta queda-vista.aseprite
                                                                                       # (só se não existir;
                                                                                       # --refazer descarta retoques)

**A base é a vista aprovada, lida da fonte de agora** (`morel/vista/morel-vista.aseprite`, com a manga de uma peça e as
duas ombreiras): a sala, o fogo, o taverneiro (parado: a taverna para para ver), a cadeira, o tronco e a cabeça de
Morel da pose `olha` (os olhos em nós), a mesa e a luz (`sombra` em multiplicar, `brilho` em somar). O tronco e a cabeça
andam com o ombro (1 px a cada 2), como uma peça só; o rosto, a cicatriz, a barba, o colete, as fivelas, a espada e a
ombreira esquerda são os pixels aprovados.

**O que é desenhado aqui:**
- o braço direito de Morel pela função da manga aprovada (`vista/manga.py`: uma forma só do ombro ao punho, a curva por
  fora do cotovelo, a dobra curta por dentro, a luz de uma superfície só, o antebraço escurecendo depois da junta, a
  sombra de um pixel no peito e no tampo) e a ombreira direita aprovada, que acompanha a junta do ombro; com o braço
  muito dobrado na tela (a disputa), o braço de cima recua meio degrau atrás do antebraço (`recuo`);
- o nosso braço pela mesma função, com outro tecido (a lã azul-acinzentada do queda 1, fria, para não se confundir com o
  couro dele) e os raios de quem está mais perto da câmera; o braço de cima sai pela borda de baixo;
- a pega (`pega`): duas mãos simples, sem dedos desenhados, construídas como dois volumes no espaço dos braços (o punho
  de cada um na ponta do antebraço dele, separados pelo lado em que as palmas se encostam) e pintadas com três tons de
  pele cada; a de Morel mais escura e quente. Dos dedos, só o que explica a pega: a faixa dos dedos de quem está por
  trás sobre o dorso que a câmera vê (na disputa, os nossos sobre o dorso dele; nos fins, os de quem perde sobre o
  dorso de quem vence) e um pixel de sombra onde uma mão passa atrás da outra. Os retoques à mão, pose a pose, ficam
  em `RETOQUES`;
- a mesa: a tigela deslizada para trás da vela e o pão levado para a esquerda da caneca (fora do caminho dos dois fins), o lugar dela com as tábuas e as juntas
  pelas linhas de fuga (o método do queda 1); o antebraço esquerdo de Morel sai do tampo (a mão vai para o colo);
- a luz da sala sobre os braços e as mãos num tom só por parte (`luz_nas_figuras`): os degraus pontilhados da camada
  `sombra` cruzavam o nosso braço e liam como textura do tecido.

A construção (as cápsulas dos braços em cores lisas e a pega) fica na camada `guia`, oculta e fora da exportação; as
juntas, um pixel de cor cada, na `juntas`. Depois de montada, a fonte é a autoridade (`exportar.py` só lê dela)."""
import math
import pathlib
import sys
import tempfile

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "queda"))
sys.path.insert(0, str(AQUI.parent / "vista"))

import geometria as G  # noqa: E402
import fonte_aseprite as fa  # noqa: E402
import manga as MG  # noqa: E402

FONTE = AQUI / "queda-vista.aseprite"
VISTA = AQUI.parent / "vista" / "morel-vista.aseprite"
OLHA = 19                      # a pose da vista em que Morel olha para quem está à mesa (o quadro da fonte menos 1)
CAMADAS = ["parede", "fundo_bar", "fogo", "caldeirao", "taverneiro", "balcao", "cadeira", "morel_corpo",
           "morel_cabeca", "mesa", "morel_braco", "nosso_braco", "maos", "sombra", "brilho", "chamas", "guia", "juntas"]
FIXAS = ["parede", "fundo_bar", "caldeirao", "balcao", "cadeira"]
FAIXAS_SOMBRA = (255, 230, 204, 179)  # os degraus da luz da sala (a camada `sombra` da vista)
MODOS = {"sombra": 14, "brilho": 29}

H = MG.H
# a nossa manga: a lã azul-acinzentada do queda 1, nos mesmos degraus do couro dele (j realce, a, b, c, l)
LA = {"j": H("7c889a"), "a": H("5e6878"), "b": H("474f5d"), "c": H("333a45"), "l": H("262b34")}
LA_PUNHO = (H("3a4150"), H("262b34"))
# as peles: a dele (a da vista aprovada) e a nossa, um pouco mais clara e fria
PELE_MOREL = (H("c09070"), H("9a6c52"), H("6c4a38"))
PELE_NOSSA = (H("d6a888"), H("ae7c5e"), H("7a5440"))
# na pega, a mão dele um degrau abaixo da nossa em tudo (a luz da vista só no ponto mais aceso): duas peles parecidas
# se separam pelo valor, não pelo contorno
PELE_MOREL_PEGA = (H("b4805e"), H("8c5e44"), H("5e3e2c"))
# os raios na tela: os dele são os da vista aprovada (vista/manga.py); os nossos, de quem está mais perto (o antebraço a
# uns 95 cm da câmera, o dele a 125: 1,3 vez), com o braço de cima mais grosso ainda na borda de baixo
R_NOSSO = {"ombro": 7.4, "cotovelo": 6.0, "cotoveloPerto": 6.0, "antebraco": 5.5, "punho": 3.9}
# a tigela deslizada para trás da vela: o deslocamento na tela (a mesma linha do tampo)
TIGELA_DX, TIGELA_DY = -62, -5  # (a tigela fica atrás da vela, com a base acima do pires dela)
# o pão, tirado da direita (onde o nosso braço deita quando Morel vence) para a esquerda da caneca, na mesma faixa
PAO, PAO_DX = ((263.5, 82.5), (17.0, 9.0)), -182


# ------------------------------------------------------------------ a mesa
def mesa_sem_tigela(mesa):
    """A camada `mesa` sem o que Morel tirou do caminho da disputa. A tigela é levada TIGELA_DX px para a esquerda e TIGELA_DY para o fundo: o lugar dela ganha
    as tábuas e as juntas pelas linhas que fogem para (238, 30) (cada pixel copia o da mesma linha de fuga mais perto
    de nós); a tigela e a sombra dela vão para o lugar novo só onde há madeira ou nada (a vela, mais perto, fica na
    frente)."""
    a = np.array(mesa)
    buraco = {(x, y) for y in range(60, 86) for x in range(190, 242)
              if ((x + 0.5 - 215.5) / 21.5) ** 2 + ((y + 0.5 - 73) / 10.5) ** 2 <= 1 and a[y, x, 3]}
    out = a.copy()
    for (x, y) in buraco:
        u = (x - 238) / (y - 30)
        for yy in range(87, 92):
            xx = round(238 + u * (yy - 30))
            if a[yy, xx, 3]:
                out[y, x] = a[yy, xx]
                break
    madeira = {tuple(a[y, x]) for y in range(62, 92) for x in range(238, 250) if a[y, x, 3]}
    for (x, y) in buraco:
        if tuple(a[y, x]) != tuple(out[y, x]) and y > 63:  # a aresta da borda de lá fica (não vai com a tigela)
            q = (x + TIGELA_DX, y + TIGELA_DY)
            if tuple(out[q[1], q[0]]) in madeira or not out[q[1], q[0], 3]:  # a madeira, ou acima da borda de lá
                out[q[1], q[0]] = a[y, x]
    # o pão: o lugar dele com as tábuas pelas mesmas linhas de fuga (copiadas de mais longe, porque ele encosta na
    # borda de cá) e o pão com a sombra na madeira à esquerda da caneca
    (cx, cy), (rx, ry) = PAO
    pao = {(x, y) for y in range(int(cy - ry), int(cy + ry) + 1) for x in range(int(cx - rx), int(cx + rx) + 1)
           if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1 and a[y, x, 3]}
    antes = out.copy()
    for (x, y) in pao:
        u = (x - 238) / (y - 30)
        for yy in range(70, 62, -1):
            xx = round(238 + u * (yy - 30))
            if a[yy, xx, 3] and (xx, yy) not in pao:
                out[y, x] = a[yy, xx]
                break
    madeira |= {tuple(a[y, x]) for y in range(66, 92) for x in range(10, 60) if a[y, x, 3]}
    for (x, y) in pao:
        if tuple(antes[y, x]) != tuple(out[y, x]):
            q = (x + PAO_DX, y)
            if tuple(out[q[1], q[0]]) in madeira:
                out[q[1], q[0]] = antes[y, x]
    return out


def _pixels(img, dx=0, dy=0):
    a = np.array(img.convert("RGBA"))
    ys, xs = np.nonzero(a[:, :, 3])
    return {(int(x) + dx, int(y) + dy): tuple(int(v) for v in a[y, x]) for y, x in zip(ys, xs)}


def _sombra(cor):
    r, g, b = cor[:3]
    return (int(r * 0.68), int(g * 0.68), int(b * 0.68), 255)


def sombra_de(figura, embaixo):
    """A sombra de um pixel (do lado oposto à luz) que `figura` faz no que está embaixo (uma lista de {(x, y): cor}, o
    primeiro que tiver o pixel)."""
    out = {}
    for (x, y) in figura:
        for dx, dy in ((1, 0), (0, 1), (1, 1)):
            q = (x + dx, y + dy)
            if q in figura or q in out:
                continue
            for camada in embaixo:
                if q in camada:
                    out[q] = _sombra(camada[q])
                    break
    return out


# ------------------------------------------------------------------ os braços (a manga aprovada)
def recuo(m, ante, S, E, W, tons):
    """Com o braço muito dobrado na tela (o antebraço subindo na frente do braço de cima, como na disputa), o braço de
    cima recua atrás dele: meio degrau abaixo longe da junta (a curva do cotovelo continua uma peça só) e a sombra que o
    antebraço faz nele com dois pixels (com um, os dois se fundiam no tamanho do jogo). Muda `m` no lugar."""
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
        perto = any((q[0] - dx, q[1] - dy) in ante for dx in (1, 2) for dy in (0, 1, 2))
        if perto:
            m[q] = tons["c"] if cor != tons["l"] else cor
        elif (1 - t) * L1 > 5:
            m[q] = desce[cor]


def braco_morel(t, corpo, mesa):
    """O braço direito de Morel: a manga de vista/manga.py nas juntas da pose, a sombra de um pixel no peito e no tampo
    e a ombreira direita por cima (atrás do antebraço, se ele passar na frente do ombro)."""
    S, E, W = t["S"], t["E"], t["W"]
    m = MG.manga(S, E, W, lambda x, y: (x, y) in corpo)
    ante = set(MG.manga.antebraco)
    recuo(m, ante, S, E, W, MG.COURO)
    out = dict(m)
    out.update(sombra_de(m, [mesa, corpo]))
    calota = MG.ombreira_direita((S[0] + 0.5, S[1] + 0.5))
    for q, cor in calota.items():
        if q not in ante:
            out[q] = cor
    # acima da ponta esquerda da calota, nada da manga passa para fora dela (como na vista aprovada)
    placa = {q for q, cor in calota.items() if cor != MG.COURO["c"]}
    ponta = min(placa, key=lambda q: (q[0], -q[1]))[1]
    for y in range(min(yy for _, yy in placa) - 3, ponta):
        xs = [x for x, yy in placa if yy == y]
        faixa = range(min(xs) - 5, min(xs)) if xs else range(min(xx for xx, _ in placa), max(xx for xx, _ in placa) + 1)
        for x in faixa:
            if (x, y) in out and (x, y) not in ante:
                del out[(x, y)]
    return out, ante


def braco_nosso(t, supina=0.0):
    """O nosso braço: a mesma manga, com a lã e os raios de quem está perto; o ombro fora do quadro, embaixo. `supina`
    (0 a 1): o antebraço girando com a palma para cima ao deitar (perdendo): a face larga dele, a de dentro, vira para
    cima e para a câmera, e o antebraço visto de cima alarga (de lado, na disputa, a câmera vê a face estreita)."""
    r0 = dict(MG.R4)
    MG.R4.update(R_NOSSO)
    MG.R4["antebraco"] *= 1 + 0.25 * supina
    MG.R4["punho"] *= 1 + 0.2 * supina
    try:
        m = MG.manga(t["Sn"], t["En"], t["Wn"], lambda x, y: True)
    finally:
        MG.R4.clear()
        MG.R4.update(r0)
    ante = set(MG.manga.antebraco)
    troca = {MG.COURO[k]: LA[k] for k in MG.COURO}
    troca.update({MG.PUNHO[0]: LA_PUNHO[0], MG.PUNHO[1]: LA_PUNHO[1]})
    out = {q: troca.get(c, c) for q, c in m.items() if 0 <= q[0] < 320 and 0 <= q[1] < 96}
    if supina >= 0.5:
        deitado(out, ante, t["En"], t["Wn"], supina)
    return out


def deitado(out, ante, E, W, supina):
    """O antebraço deitado com a palma para cima: a face de dentro, larga, vira para cima e para a câmera. A forma lê
    achatada: o topo largo num tom só aceso (a face que pega a luz da vela), a borda de cima um fio claro, a de baixo
    (a face estreita, de lado) num degrau escuro e a sombra no tampo; perto do cotovelo, a dobra de dentro por cima
    (um traço curto com o fio aceso da crista) e a ponta do cotovelo, virada para baixo e para trás, sem o realce que
    a fazia ler como um joelho. Muda `out` no lugar; o punho da manga fica."""
    ex, ey = W[0] - E[0], W[1] - E[1]
    L = math.hypot(ex, ey)
    ux, uy = ex / L, ey / L
    nx, ny = -uy, ux                       # a normal na tela; o lado "de cima" é o de y menor
    if ny > 0:
        nx, ny = -nx, -ny
    punho = {LA_PUNHO[0], LA_PUNHO[1]}
    for q in list(out):
        if q not in ante or out[q] in punho:
            continue
        px, py = q[0] + 0.5 - E[0], q[1] + 0.5 - E[1]
        t = (px * ux + py * uy) / L        # 0 no cotovelo, 1 no pulso
        v = px * nx + py * ny              # > 0 do lado de cima
        larg = R_NOSSO["antebraco"] * (1 + 0.25 * supina) * (1 - t) + R_NOSSO["punho"] * (1 + 0.2 * supina) * t
        e = v / max(larg, 1.0)
        if t < 0.12:
            continue                       # a junta: a forma unida da manga
        out[q] = LA["j"] if e > 0.62 else LA["a"] if e > -0.45 else LA["b"] if e > -0.8 else LA["c"]
    # a dobra de dentro por cima do cotovelo: dois pixels escuros ao longo do antebraço, logo depois da junta, no lado
    # de cima, e o fio aceso da crista acima deles
    for k, tom in ((2.5, "c"), (3.5, "c")):
        bx, by = E[0] + ux * k + nx * 2.4, E[1] + uy * k + ny * 2.4
        q = (math.floor(bx), math.floor(by))
        if q in out:
            out[q] = LA[tom]
        c = (math.floor(bx + nx), math.floor(by + ny))
        if c in out:
            out[c] = LA["j"]
    # a ponta do cotovelo (o lado de fora da curva, virado para baixo e para trás): um degrau abaixo, sem realce
    for q, cor in list(out.items()):
        if q in ante or math.dist((q[0] + 0.5, q[1] + 0.5), E) > R_NOSSO["cotovelo"] + 1.5:
            continue
        if cor in (LA["j"], LA["a"]):
            out[q] = LA["b"]


# ------------------------------------------------------------------ a pega
# os punhos: ao longo do antebraço, para o lado da palma, de frente (as bolinhas da vista; maiores, com o nó do polegar
# como uma terceira forma, liam como um calombo); quanto cada um vem para o meio da pega no desenho (as mãos fechadas
# uma na outra se sobrepõem; só encostadas, liam como duas bolas empilhadas); a faixa dos dedos de quem está por trás
RAIO_PUNHO = (2.3, 1.9, 1.8)
APROXIMA = 1.0
FAIXA_DEDOS = True
LUZ_MUNDO = (-0.6, 0.55, -0.58)  # a luz da vista (vista/manga.py: x à direita, y para baixo, z para quem olha) no espaço


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


def pega(p):
    """A pega da pose `p` (geometria.pose): {(x, y): cor}. Cada punho é um volume na ponta do antebraço (o comprimento
    ao longo dele, a largura no lado em que as palmas se encostam, a espessura); na tela, cada pixel fica com a
    superfície mais perto da câmera. Os dedos de quem está por trás aparecem como uma tira estreita sobre o dorso que a
    câmera vê, perto dos nós; um pixel de sombra separa as duas peles onde uma passa atrás da outra."""
    T = p["lado_t"]                                                         # da mão dele para a nossa
    P = p["pega"]
    para_camera = _un(_vezes(P, -1))
    maos = {}
    for quem, pulso, mao, sinal in (("morel", p["pulso_m"], p["mao_m"], -1), ("nos", p["pulso_n"], p["mao_n"], 1)):
        eixo = _un(_soma(mao, _vezes(pulso, -1)))                          # do pulso para a mão
        # o desenho aproxima os dois punhos do meio (as mãos fechadas uma na outra se sobrepõem; encostadas, liam como
        # duas bolas empilhadas)
        centro = _soma(mao, _vezes(eixo, -0.8), _vezes(T, -sinal * (APROXIMA if p["firme"] else 0.2)))
        maos[quem] = dict(centro=centro, eixo=eixo, dorso=_vezes(T, sinal))
    # cada volume: (quem pinta, centro, eixos com os raios, a cor de quem); a faixa dos dedos sobre o dorso visível
    vol = []
    for quem, m in maos.items():
        lat = _un(_cruz(m["eixo"], _cruz(T, m["eixo"]))) if abs(_dot(T, m["eixo"])) < 0.99 else T
        prof = _un(_cruz(m["eixo"], lat))
        vol.append((quem, m["centro"], ((m["eixo"], RAIO_PUNHO[0]), (lat, RAIO_PUNHO[1]), (prof, RAIO_PUNHO[2]))))
    px = {}
    for quem, c, eixos in vol:
        n = 14
        for i in range(-n, n + 1):
            for j in range(-n, n + 1):
                for k in range(-n, n + 1):
                    u, v, w = i / n, j / n, k / n
                    if u * u + v * v + w * w > 1:
                        continue
                    q = _soma(c, *[_vezes(e, r * s) for (e, r), s in zip(eixos, (u, v, w))])
                    if q[1] < 0.3:   # nada atravessa o tampo
                        continue
                    x, y = G.tela(q)
                    k2 = (math.floor(x), math.floor(y))
                    z = q[2] - 0.0 * _dot(q, para_camera)
                    if k2 in px and px[k2][0] <= z:
                        continue
                    nrm = _un(_soma(*[_vezes(e, s / r) for (e, r), s in zip(eixos, (u, v, w))])) if (u or v or w) else eixos[0][0]
                    px[k2] = (z, quem, nrm, u)
    pele = {"morel": PELE_MOREL_PEGA, "nos": PELE_NOSSA}
    out, dono = {}, {}
    for q, (z, quem, nrm, u) in px.items():
        s = _dot(nrm, _un(LUZ_MUNDO))
        d = quem
        # a faixa dos dedos de quem está por trás, sobre o dorso que a câmera vê (perto dos nós)
        if quem in maos and _dot(maos[quem]["dorso"], para_camera) > 0.05 and _dot(nrm, maos[quem]["dorso"]) > 0.25 \
                and u > -0.15:
            d = "nos" if quem == "morel" else "morel"
            s -= 0.15
        dono[q] = d
        cor = pele[d]
        out[q] = cor[0] if s > 0.5 else cor[1] if s > -0.2 else cor[2]
    # um pixel de sombra na pele de quem está atrás, onde a outra mão passa na frente (do lado oposto à luz)
    for (x, y), d in list(dono.items()):
        if any(dono.get(v) not in (None, d) and px[v][0] < px[(x, y)][0] for v in ((x - 1, y), (x, y - 1), (x - 1, y - 1))):
            out[(x, y)] = pele[d][2]
    return out


# ------------------------------------------------------------------ a luz
def luz_nas_figuras(sombra, brilho, partes):
    """A luz da sala sobre as figuras num tom só por parte (o braço dele, o nosso, as mãos): a camada `sombra` da vista
    tem degraus com pontilhado na passagem (230 e 204 bem onde os braços cruzam), e o pontilhado sobre uma figura no meio
    da cena lia como textura do tecido (a lição do balcão: quem está no meio da cena recebe a luz num tom só). Cada parte
    fica com o degrau mais perto da média da luz embaixo dela e com o brilho médio; o resto da sala, como está."""
    s, b = dict(sombra), dict(brilho)
    feito = set()
    for parte in partes:
        qs = [q for q in parte if q in sombra and q not in feito]
        if not qs:
            continue
        media = sum(sombra[q][0] for q in qs) / len(qs)
        v = min(FAIXAS_SOMBRA, key=lambda f: abs(f - media))
        mb = round(sum(brilho.get(q, (0, 0, 0, 0))[0] if brilho.get(q, (0, 0, 0, 0))[3] else 0 for q in qs) / len(qs))
        for q in qs:
            s[q] = (v, v, v, 255)
            if mb:
                b[q] = (mb, round(mb * 0.62), round(mb * 0.3), 255) if q not in brilho else _tom_brilho(brilho, mb)
            else:
                b.pop(q, None)
            feito.add(q)
    return s, b


def _tom_brilho(brilho, v):
    """A cor do brilho com o vermelho `v` (o brilho é quente: as outras componentes na proporção das que existem)."""
    for cor in brilho.values():
        if cor[3] and cor[0] == v:
            return cor
    return (v, round(v * 0.62), round(v * 0.3), 255)


# ------------------------------------------------------------------ a construção (a guia oculta)
def _capsula(a, b, ra, rb, cor, out):
    x0, x1 = int(min(a[0], b[0]) - max(ra, rb) - 1), int(max(a[0], b[0]) + max(ra, rb) + 2)
    y0, y1 = int(min(a[1], b[1]) - max(ra, rb) - 1), int(max(a[1], b[1]) + max(ra, rb) + 2)
    for y in range(y0, y1):
        for x in range(x0, x1):
            t, d = MG._seg((x + 0.5, y + 0.5), a, b)
            if d <= ra + (rb - ra) * t and 0 <= x < 320 and 0 <= y < 96:
                out[(x, y)] = cor


def construcao(t):
    """A construção da pose em formas simples e cores lisas (a camada `guia`, oculta e fora da exportação): o braço e o
    antebraço dele (vermelho e laranja), os nossos (azuis), as mãos (amarelo), o arco possível da pega (pontos) e os
    contatos dos cotovelos no tampo (verde)."""
    out = {}
    _capsula(t["S"], t["E"], 5.6, 4.6, (200, 70, 50, 255), out)
    _capsula(t["E"], t["W"], 4.6, 3.3, (240, 140, 60, 255), out)
    _capsula(t["Sn"], t["En"], 7.4, 6.0, (60, 80, 150, 255), out)
    _capsula(t["En"], t["Wn"], 5.5, 3.9, (100, 140, 220, 255), out)
    _capsula(t["W"], t["P"], 2.6, 2.6, (230, 200, 60, 255), out)
    _capsula(t["Wn"], t["P"], 3.0, 3.0, (250, 230, 120, 255), out)
    for k in range(-90, 91, 6):
        q = G.pose(math.radians(k) * G.fi_fim() / (math.pi / 2), (0, 0))["tela"]["P"]
        out[(math.floor(q[0]), math.floor(q[1]))] = (255, 255, 255, 255)
    for k in ("contato_m", "contato_n"):
        out[tuple(math.floor(v) for v in t[k])] = (40, 255, 90, 255)
    return out


# ------------------------------------------------------------------ a montagem
RETOQUES = {}  # pose: {(x, y): "rrggbb" ou "."}


def poses(cel):
    """Os quadros da fonte: {camada: {(x, y): cor}} por pose, na ordem de geometria.POSES."""
    L = lambda n, q=OLHA: Image.open(cel / f"{n}-{q}.png").convert("RGBA")  # noqa: E731
    mesa = mesa_sem_tigela(L("mesa"))
    mesa_cor = {(x, y): tuple(int(v) for v in mesa[y, x]) for y in range(96) for x in range(320) if mesa[y, x, 3]}
    fixas = {n: _pixels(L(n)) for n in FIXAS}
    fogo, chamas, tav = _pixels(L("fogo", 1)), _pixels(L("chamas", 1)), _pixels(L("taverneiro"))
    corpo0, cabeca0 = L("morel_corpo"), L("morel_cabeca")
    sombra0, brilho0 = _pixels(L("sombra")), _pixels(L("brilho"))
    out = []
    for nome, p in G.todas().items():
        t = p["tela"]
        dx, dy = p["tronco"]  # o tronco debruçado e o esforço (geometria.POSES); a cabeça desce mais
        corpo = _pixels(corpo0, dx, dy)
        c = dict(fixas)
        c.update(fogo=fogo, chamas=chamas, taverneiro=tav, mesa=mesa_cor, morel_corpo=corpo,
                 morel_cabeca=_pixels(cabeca0, dx, dy + p["cabeca"]))
        dele, ante = braco_morel(t, corpo, mesa_cor)
        c["morel_braco"] = dele
        nosso = braco_nosso(t, p["supina"])
        c["nosso_braco"] = dict(nosso)
        c["nosso_braco"].update(sombra_de(nosso, [dele, mesa_cor, corpo]))
        maos = pega(p)
        maos.update({q: v for q, v in sombra_de(maos, [nosso, dele, mesa_cor, corpo]).items()})
        for q, v in RETOQUES.get(nome, {}).items():
            if v == ".":
                maos.pop(q, None)
            else:
                maos[q] = H(v)
        c["maos"] = maos
        c["sombra"], c["brilho"] = luz_nas_figuras(sombra0, brilho0, [dele, c["nosso_braco"], maos])
        c["guia"] = construcao(t)
        c["juntas"] = {tuple(math.floor(v) for v in t[k]): cor + (255,) for k, cor in (
            ("S", (255, 64, 64)), ("E", (48, 255, 96)), ("W", (48, 128, 255)), ("En", (48, 255, 96)),
            ("Wn", (48, 128, 255)), ("P", (255, 224, 48)))}
        out.append((nome, c))
    return out


def recompor(c):
    """A pose achatada como o Aseprite a achata (para a prévia): as camadas na ordem, `sombra` multiplicando e `brilho`
    somando, sem as chamas, a guia e as juntas."""
    a = np.zeros((96, 320, 3), float)
    for n in CAMADAS:
        if n in ("chamas", "guia", "juntas"):
            continue
        for (x, y), cor in c.get(n, {}).items():
            if not (0 <= x < 320 and 0 <= y < 96) or (len(cor) > 3 and cor[3] == 0):
                continue
            if n == "sombra":
                a[y, x] = a[y, x] * np.array(cor[:3]) / 255
            elif n == "brilho":
                a[y, x] = np.minimum(255, a[y, x] + np.array(cor[:3]))
            else:
                a[y, x] = cor[:3]
    return Image.fromarray(a.astype(np.uint8), "RGB").convert("RGBA")


def previa(saida):
    saida = pathlib.Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cel = fa.celulas(VISTA, pathlib.Path(tmp) / "cel")
        for i, (nome, c) in enumerate(poses(cel)):
            recompor(c).save(saida / f"{i:02d}-{nome}.png")
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
  if D.modos[l.name] then l.blendMode = D.modos[l.name] end
end
s:saveAs(app.params["saida"])
print("montada: " .. n .. " células")
'''


def criar(refazer=False):
    """Monta queda-vista.aseprite (uma pose por quadro, com a etiqueta do nome), a partir da vista aprovada e do que é
    desenhado aqui. Depois de montada, a fonte é a autoridade: não é refeita sem --refazer."""
    import subprocess
    from exportar_aseprite import aseprite
    if FONTE.exists() and not refazer:
        sys.exit(f"{FONTE.name} já existe e é a autoridade; use --refazer para descartar os retoques e montar de novo.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        cel = fa.celulas(VISTA, tmp / "cel")
        png = tmp / "png"
        png.mkdir()
        nomes = []
        for i, (nome, c) in enumerate(poses(cel)):
            nomes.append(nome)
            for camada in CAMADAS:
                px = c.get(camada) or {}
                if not px:
                    continue
                im = Image.new("RGBA", (320, 96), (0, 0, 0, 0))
                a = np.array(im)
                for (x, y), cor in px.items():
                    if 0 <= x < 320 and 0 <= y < 96:
                        a[y, x] = cor if len(cor) == 4 else tuple(cor) + (255,)
                Image.fromarray(a, "RGBA").save(png / f"{camada}-{i}.png")
        dados = tmp / "dados.lua"
        dados.write_text("return {camadas={" + ",".join(f'"{c}"' for c in CAMADAS) + "}, quadros={"
                         + ",".join(f'"{q}"' for q in nomes) + "}, ocultas={[\"guia\"]=true, [\"juntas\"]=true},"
                         + " modos={" + ",".join(f'["{c}"]={v}' for c, v in MODOS.items()) + "}}", encoding="utf-8")
        lua = tmp / "montar.lua"
        lua.write_text(_MONTAR, encoding="utf-8")
        r = subprocess.run([aseprite(), "-b", "--script-param", f"dados={dados}", "--script-param", f"pasta={png}",
                            "--script-param", f"saida={FONTE}", "--script", str(lua)], capture_output=True, text=True)
        ok = [x for x in r.stdout.splitlines() if x.startswith("montada")]
        if not ok or not FONTE.exists():
            sys.exit(f"o Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(ok[0], f"({len(nomes)} poses)")


if __name__ == "__main__":
    if "--previa" in sys.argv:
        previa(sys.argv[-1])
    elif "--criar" in sys.argv or "--refazer" in sys.argv:
        criar("--refazer" in sys.argv)
