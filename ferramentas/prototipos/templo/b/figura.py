"""O clérigo da candidata B, no estilo das figuras do jogo, na escala desta câmera (~31 px). O que o jogo diz dele: "um
clérigo cansado, de mãos firmes", que trata "com unguentos e orações". O resto é escolha da candidata (a roupa da
referência é provisória; o avental fica, sem símbolo): o hábito de lã crua, o avental de linho, o cabelo curto e a
barba curta escuros com fios grisalhos, os ombros um pouco caídos. De lado, voltado para a esquerda, na ponta da mesa.

A atividade, pelos apoios (skill arte-cenas-fenda, 5b): **dobrar os panos limpos**, na ponta da mesa, entre o monte
de panos soltos (perto, à esquerda) e a pilha dos dobrados (embaixo das mãos).
- **o alcance:** na escala desta câmera o braço tem ~13 px; no nível do tampo a mão só chega uns 8 px à frente do
  ombro. O trabalho fica na ponta da mesa; para pegar no monte, o tronco vai à frente (o braço não chega sozinho);
- **conduz:** as mãos (pegar, erguer o pano, dobrar, assentar, alisar);
- **acompanha:** os cotovelos (comprimento fixo), o tronco (à frente para pegar, de pé para erguer, um pouco à frente
  para alisar), a cabeça olhando as mãos;
- **fica:** os pés, a barra do hábito, a mesa, o monte e a pilha (o pano dobrado assenta como a camada de cima: a
  pilha não cresce a cada volta);
- **a pausa:** as mãos na beira da mesa, as costas sobem, a cabeça vira para a nave (o cansaço)."""
from ..a.figura import _capsula, cotovelo
from .desenho import PES, QH, QW, Pincel, Tela

COR = {
    "pele": ("#b07858", "#cc9676", "#82543a"),
    "habito": ("#625c52", "#777064", "#46413a"),   # a lã crua acinzentada (o pé da mesa é madeira escura e quente)
    "avental": ("#8f8672", "#a39a84", "#6e675a"),
    "cabelo": ("#3e342c", "#5a5048", "#2a221c"),
    "linho": ("#d4cab2", "#e8e0ca", "#a29882"),
}
X, TOPO = 222, 39
TRONCO = [(47, 225, 228), (48, 224, 229), (49, 223, 230), (50, 223, 230), (51, 223, 230), (52, 223, 230),
          (53, 223, 230), (54, 223, 229), (55, 223, 229)]
BARRA = (220, 233)
OMBRO = (227, 49)
BRACO = (6.0, 7.0)
MONTE = (212, 54)    # o monte de panos soltos, no tampo (o canto de cima à esquerda)
PILHA = (214, 53)    # a pilha dos dobrados, embaixo das mãos (a mesa acaba em x 219; a barra do hábito, em 220)

CABECA = {
    "baixo": [
        "..KKKk..",
        ".KKKKkk.",
        ".lsKKkk.",
        ".seSKk..",
        "lsssSk..",
        ".BgBSk..",
        "..BBk...",
        "...sS...",
    ],
    "alto": [
        "..KKKk..",
        ".KKKKkk.",
        ".lsKKkk.",
        ".seSSKk.",
        "lsssSk..",
        ".BgBSk..",
        "..BBk...",
        "...sS...",
    ],
}

# as poses: os ombros (o tronco), a cabeça, as duas mãos e o pano (onde está e que forma tem)
POSES = {
    "pega": {"ombro": (-3, 1), "cabeca": (-3, 1, "baixo"), "perto": (212, 54), "longe": (213, 53), "pano": None},
    # a passagem da pega para o erguer: o pano saindo do monte, o tronco a meio caminho (sem saltar 3 px num tique)
    "puxa": {"ombro": (-2, 0), "cabeca": (-2, 0, "baixo"), "perto": (213, 50), "longe": (214, 49), "pano": "meio"},
    "ergue": {"ombro": (0, -1), "cabeca": (0, -1, "baixo"), "perto": (215, 47), "longe": (216, 46), "pano": "pendurado"},
    "sacode": {"ombro": (0, -1), "cabeca": (0, -1, "baixo"), "perto": (215, 48), "longe": (216, 47), "pano": "balanca"},
    "dobra": {"ombro": (0, 0), "cabeca": (-1, 1, "baixo"), "perto": (215, 49), "longe": (216, 48), "pano": "meio"},
    "assenta": {"ombro": (-1, 0), "cabeca": (-1, 1, "baixo"), "perto": (215, 52), "longe": (216, 52), "pano": "dobrado"},
    "alisa": {"ombro": (-1, 1), "cabeca": (-1, 1, "baixo"), "perto": (215, 52), "longe": (217, 52), "pano": None},
    "beira": {"ombro": (0, 0), "cabeca": (-1, 1, "baixo"), "perto": (218, 55), "longe": (219, 55), "pano": None},
    "olha": {"ombro": (1, -1), "cabeca": (0, -1, "alto"), "perto": (218, 55), "longe": (219, 55), "pano": None},
}
DOBRA = [("pega", 2), ("puxa", 1), ("ergue", 3), ("sacode", 2), ("ergue", 2), ("dobra", 3), ("assenta", 3), ("alisa", 5)]
ROTINA = DOBRA * 2 + [("beira", 3), ("olha", 14), ("beira", 3)]
PARADA = "olha"


def quadros():
    unicos, tempo = [PARADA], []
    for nome, n in ROTINA:
        if nome not in unicos:
            unicos.append(nome)
        tempo += [unicos.index(nome)] * n
    return unicos, tempo, 0


def figura(nome):
    p = POSES[nome]
    t = Tela(QW, QH)
    px = Pincel(t)
    pe, pe_luz, pe_esc = COR["pele"]
    ha, ha_luz, ha_esc = COR["habito"]
    av, av_luz, av_esc = COR["avental"]
    li, li_luz, li_esc = COR["linho"]
    sx, sy = p["ombro"]
    y_cint, fr_c, co_c = TRONCO[-1]
    y_alto = TRONCO[0][0]

    # A inclinação: o tronco, os ombros e a cabeça andam juntos, como um bloco (sx, sy); quem a absorve é o hábito, da
    # cintura (que vai com o tronco) até a barra (parada no chão), numa diagonal suave. Antes o tronco era fatiado (cada
    # linha andava um pouco) sobre uma cintura parada, e o encaixe aparecia quadro a quadro.
    def desvio(y):
        return sx, sy

    # ---- o monte de panos soltos e a pilha dos dobrados, no tampo (parados)
    mx, my = MONTE
    px(mx - 2, my - 1, 4, 2, li_esc)
    px(mx - 2, my - 2, 3, 1, li)
    px.p(mx - 1, my - 3, li_luz)
    qx, qy = PILHA
    px(qx, qy, 4, 3, li)
    px(qx, qy, 4, 1, li_luz)
    px(qx, qy + 1, 4, 1, li_esc)
    # ---- o braço de longe (atrás do corpo): o antebraço e a mão
    ol = (OMBRO[0] - 1 + sx, OMBRO[1] - 1 + sy)
    ml = p["longe"]
    co = cotovelo(ol, (ml[0] + 0.5, ml[1] + 0.5), *BRACO)
    _capsula(t, co, (ml[0] + 0.5, ml[1] + 0.5), 0.8, pe_esc, pe, pe_esc)
    # ---- o hábito: da cintura ao chão; o avental na frente, até perto da barra
    b0, b1 = BARRA
    cint = y_cint + sy                                     # a cintura, levada pelo tronco
    for y in range(cint + 1, PES - 1):
        k = (y - cint) / (PES - 2 - cint)
        d = sx * (1 - k)                                   # o hábito vai da cintura inclinada à barra parada
        a_ = round(fr_c + (b0 - fr_c) * k + d)             # (um arredondamento só: sem degrau duplo no contorno)
        b_ = round(co_c + (b1 - co_c) * k ** 1.3 + d)
        px(a_, y, b_ - a_ + 1, 1, ha)
        px(b_ - 1, y, 2, 1, ha_esc)
        if k > 0.3:
            px.p(a_ + round((b_ - a_) * 0.6), y, ha_esc)
        if y < PES - 4:
            w = 2 + round(k * 1.4)
            px(a_, y, w, 1, av)
            px(a_, y, 1, 1, av_luz)
            px(a_ + w - 1, y, 1, 1, av_esc)
    px(b0 + 1, PES - 2, b1 - b0 - 1, 1, ha_esc)
    px(b0, PES - 2, 3, 2, "#2a1c12")                       # a ponta da sandália, saindo da barra
    px(b0, PES, b1 - b0 + 1, 1, "#1c1a17")                # a sombra de contato no piso
    # ---- o tronco: o hábito, o peito do avental, o cordão
    for y, a_, b_ in TRONCO:
        dx, dy = desvio(y)
        px(a_ + dx, y + dy, b_ - a_ + 1, 1, ha)
        px(a_ + dx, y + dy, 1, 1, ha_luz)
        px(b_ - 1 + dx, y + dy, 2, 1, ha_esc)
        if y >= y_alto + 2:
            px(a_ + dx, y + dy, 2, 1, av)
            px(a_ + dx, y + dy, 1, 1, av_luz)
    px(fr_c + sx, cint, co_c - fr_c + 1, 1, av_esc)  # a amarra do avental, na cintura
    # ---- a cabeça
    cx, cy, olhar = p["cabeca"]
    pal = {"K": COR["cabelo"][0], "k": COR["cabelo"][2], "B": COR["cabelo"][0], "g": "#6a625a", "s": pe, "S": pe_esc, "l": pe_luz,
           "e": "#140e0a"}
    t.grade(X + cx, TOPO + cy, CABECA[olhar], pal)
    # ---- o pano nas mãos
    hx, hy = p["perto"]
    forma = p["pano"]
    if forma in ("pendurado", "balanca"):  # erguido pelos cantos, caindo na frente do peito
        d = 1 if forma == "balanca" else 0
        px(hx - 2 + d, hy + 1, 4, 6, li)
        px(hx - 2 + d, hy + 1, 1, 6, li_luz)
        px(hx + 1 + d, hy + 2, 1, 5, li_esc)
        px(hx - 2 + d, hy + 6, 4, 1, li_esc)
    elif forma == "meio":  # dobrado ao meio, mais curto e mais grosso
        px(hx - 2, hy + 1, 4, 3, li)
        px(hx - 2, hy + 1, 4, 1, li_luz)
        px(hx - 2, hy + 3, 4, 1, li_esc)
    elif forma == "dobrado":  # assentando na pilha
        px(hx - 1, hy, 4, 2, li_luz)
        px(hx - 1, hy + 1, 4, 1, li)
    # ---- o braço de perto: a manga do hábito até o meio do antebraço, a mão
    op = (OMBRO[0] + sx, OMBRO[1] + sy)
    co = cotovelo(op, (hx + 0.5, hy + 0.5), *BRACO)
    _capsula(t, op, co, 1.2, ha_luz, ha_luz, ha_esc)
    meio = (co[0] + (hx + 0.5 - co[0]) * 0.4, co[1] + (hy + 0.5 - co[1]) * 0.4)
    _capsula(t, co, meio, 1.2, ha_luz, ha_luz, ha_esc)
    _capsula(t, meio, (hx + 0.5, hy + 0.5), 0.8, pe, pe_luz, pe_esc)
    px(hx, hy, 2, 2, pe)
    px.p(hx, hy, pe_luz)
    return t


def todas():
    unicos, _, _ = quadros()
    return [figura(n) for n in unicos]
