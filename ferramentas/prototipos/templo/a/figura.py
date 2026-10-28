"""O clérigo do templo, no estilo das figuras do jogo (sem contorno, três tons por material, o olho de um pixel, as mãos
simples). O que o jogo diz dele: "um clérigo cansado, de mãos firmes", que trata "com unguentos e orações". O resto é
escolha desta candidata: um homem maduro, o alto da cabeça calvo e o cabelo grisalho dos lados, o hábito de lã cinza
com o cordão na cintura, as mangas puxadas até o antebraço. De lado, voltado para a esquerda (para a mesa dos
unguentos), na ponta da mesa.

A atividade, decidida pelos apoios antes dos quadros (skill arte-cenas-fenda, 5b): **enrolar ataduras**.
- **fica parado:** os pés, a barra do hábito, a mesa, a tira de linho estendida no tampo (do rolo para a esquerda);
- **conduz:** as duas mãos girando o rolo, que gira no lugar (a tira vai entrando nele);
- **acompanha:** os cotovelos (o braço tem comprimento fixo; o cotovelo sai da conta), a cabeça olhando as mãos, os
  ombros no puxão de apertar (o tronco recua 1 px) e na hora de alisar a tira mais adiante (o braço não alcança sozinho:
  o peito vai à frente e desce);
- **a pausa:** endireitar as costas com as mãos na beira da mesa, a cabeça subindo para olhar a nave (o cansaço), e
  voltar. Sem ritual nem efeito: é o trabalho do lugar.

A rotina (ROTINA) e o tempo de cada pose ficam em tiques de 100 ms, como na curandeira; o relógio da cena é o mesmo."""
import math

from .desenho import MESA, PES, QH, QW, Pincel, Tela

COR = {
    "pele": ("#b47c5c", "#d09a78", "#86563c"),
    "habito": ("#3e4249", "#52575f", "#2a2d33"),
    "cabelo": ("#8a8680", "#aaa69e", "#5e5a54"),
    "cordao": ("#8a7650", "#5e5034"),
    "linho": ("#b0a68e", "#d2c8b0", "#857b66"),
}
X, TOPO = 224, 44                 # a grade da cabeça (o nariz na coluna 0)
TRONCO = [(53, 228, 232), (54, 227, 233), (55, 226, 234), (56, 226, 234), (57, 225, 234), (58, 225, 234),
          (59, 225, 234), (60, 225, 234), (61, 226, 234), (62, 226, 234), (63, 226, 234), (64, 226, 233),
          (65, 226, 233)]          # (y, frente, costas) do pescoço à cintura
BARRA = (222, 238)                # a barra do hábito no chão (frente, costas)
OMBRO = (231, 55)                 # o ombro de perto; o de longe fica 1 px para a frente e 1 acima
BRACO = (8.5, 9.5)                # braço e antebraço (~0,43 da altura, como os nossos)
ROLO = (220, 62)                  # o centro do rolo (na altura das mãos, logo acima do tampo)
TIRA = 200                        # onde a tira estendida termina, à esquerda, no tampo

# a cabeça de perfil, nas duas inclinações (o nariz na coluna 0): o alto calvo, o cabelo grisalho curto dos lados e
# atrás, a sobrancelha grisalha, o olho de um pixel atrás da ponte do nariz e a olheira embaixo (o cansaço), o nariz
# grande, a boca, o queixo e o pescoço que cai no colarinho. "baixo": olhando as mãos (o rosto um pixel abaixo e o
# queixo recolhido); "alto": endireitado, olhando a nave.
CABECA = {
    "baixo": [
        "...lssK...",
        "..lssssKk.",
        ".lsssssKkk",
        ".lssssSKkk",
        ".swsSSEKk.",
        ".sebSSEk..",
        "lssSSSk...",
        ".msSSs....",
        "..sSSs....",
        "...sSSs...",
    ],
    "alto": [
        "...lssK...",
        "..lssssKk.",
        ".lsssssKkk",
        ".swssSSKkk",
        ".sebSSEKk.",
        "lsssSSEk..",
        ".ssSSSk...",
        ".msSSs....",
        "..ssSs....",
        "...sSSs...",
    ],
}


def _capsula(t, a, b, r, cor, luz, sombra):
    """Um pedaço de braço como forma cheia (a mesma da curandeira): os pixels a até `r` do segmento a-b; em cada coluna
    o de cima na luz e o de baixo na sombra."""
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


def cotovelo(ombro, mao, l1, l2):
    """O cotovelo pelos comprimentos fixos (a dobra para baixo e para trás). A mão fora do alcance é um erro da pose."""
    (sx, sy), (hx, hy) = ombro, mao
    d = math.hypot(hx - sx, hy - sy)
    assert d <= l1 + l2 + 0.05, f"a mão em {mao} não alcança do ombro {ombro} ({d:.1f} > {l1 + l2})"
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    ux, uy = (hx - sx) / d, (hy - sy) / d
    px, py = sx + ux * a, sy + uy * a
    c1, c2 = (px - uy * h, py + ux * h), (px + uy * h, py - ux * h)
    return c1 if c1[1] >= c2[1] else c2


# ---------------------------------------------------------------- as poses
def giro(k):
    """As mãos em volta do rolo na pose k (4 por volta): a de perto e a de longe em lados opostos, trocando de lugar.
    Devolve (mão de perto, mão de longe), relativas ao centro do rolo."""
    a = math.pi / 2 * k
    return (round(1.6 * math.cos(a)), 1 + round(1.2 * math.sin(a))), (round(-1.6 * math.cos(a)), -1 + round(-1.2 * math.sin(a)))


def pose_enrola(k):
    perto, longe = giro(k)
    return {"ombro": (0, 0), "cabeca": (-1, 1, "baixo"), "rolo": (0, 0, k), "perto": perto, "longe": longe}


POSES = {
    # apertar o rolo: as mãos o puxam para perto e o tronco recua (o peso para trás), a cabeça vai junto
    "aperta": {"ombro": (1, 0), "cabeca": (0, 1, "baixo"), "rolo": (1, 0, 0), "perto": (0, 1), "longe": (0, -1)},
    # alisar a tira: a mão de longe segura o rolo; a de perto vai adiante no tampo (o peito à frente e embaixo)
    "estica": {"ombro": (-2, 1), "cabeca": (-2, 2, "baixo"), "rolo": (0, 0, 0), "perto": "tira1", "longe": (0, -1)},
    "alisa": {"ombro": (-3, 2), "cabeca": (-3, 3, "baixo"), "rolo": (0, 0, 0), "perto": "tira2", "longe": (0, -1)},
    # endireitar: o rolo pousado no tampo, as mãos na beira da mesa, as costas sobem, a cabeça olha a nave
    "pousa": {"ombro": (0, 0), "cabeca": (-1, 1, "baixo"), "rolo": (0, 2, 0), "perto": "beira", "longe": "beira"},
    "ergue": {"ombro": (1, -1), "cabeca": (0, 0, "alto"), "rolo": (0, 2, 0), "perto": "beira", "longe": "beira"},
    "olha": {"ombro": (1, -1), "cabeca": (0, -1, "alto"), "rolo": (0, 2, 0), "perto": "beira", "longe": "beira"},
}
ALVOS = {"tira1": (214, 64), "tira2": (212, 64), "beira": (220, 66)}

# a rotina, (pose, tiques de 100 ms): as voltas (4 poses, 2 tiques cada), apertar, alisar a tira mais adiante, voltar a
# enrolar, apertar, pousar o rolo e endireitar as costas para olhar a nave, e voltar a pegar o rolo
VOLTA = [(("enrola", 0), 2), (("enrola", 1), 2), (("enrola", 2), 2), (("enrola", 3), 2)]
ROTINA = (VOLTA * 3 + [(("aperta", None), 4), (("enrola", 0), 2), (("estica", None), 2), (("alisa", None), 5),
                       (("estica", None), 2)] + VOLTA * 2
          + [(("aperta", None), 4), (("pousa", None), 3), (("ergue", None), 3), (("olha", None), 14), (("ergue", None), 3),
             (("pousa", None), 3)])
PARADA = ("olha", None)  # a pose do movimento reduzido: endireitado, as mãos na beira da mesa, olhando a nave


def pose_de(item):
    nome, k = item
    return pose_enrola(k) if nome == "enrola" else POSES[nome]


def quadros():
    """Os desenhos diferentes da rotina, a linha do tempo (o quadro de cada tique) e o índice da pose parada."""
    unicos, tempo = [PARADA], []
    for item, n in ROTINA:
        if item not in unicos:
            unicos.append(item)
        tempo += [unicos.index(item)] * n
    return unicos, tempo, 0


# ---------------------------------------------------------------- o desenho
def figura(pose):
    t = Tela(QW, QH)
    px = Pincel(t)
    pe, pe_luz, pe_esc = COR["pele"]
    ha, ha_luz, ha_esc = COR["habito"]
    li, li_luz, li_esc = COR["linho"]
    sx, sy = pose["ombro"]
    y_cint, fr_c, co_c = TRONCO[-1]
    y_alto = TRONCO[0][0]

    def desvio(y):
        k = (y_cint - y) / (y_cint - y_alto)
        return round(sx * k), round(sy * k)

    rx, ry = ROLO[0] + pose["rolo"][0], ROLO[1] + pose["rolo"][1]
    girou = pose["rolo"][2]

    def mao(qual):
        alvo = pose[qual]
        if isinstance(alvo, str):
            x, y = ALVOS[alvo]
            return (x - (1 if qual == "longe" else 0), y)
        return (rx + alvo[0], ry + alvo[1])

    # ---- a tira de linho no tampo, do rolo até a ponta (parada), e o rolo
    px(TIRA, MESA - 1, rx - TIRA, 1, li)
    px(TIRA, MESA - 1, 3, 1, li_esc)
    px.p(rx - 1, MESA - 1 if ry + 1 >= MESA - 1 else ry + 1, li)
    if ry + 2 < MESA - 1:  # a tira subindo do tampo até o rolo, nas mãos
        px.linha(rx - 2, MESA - 1, rx - 1, ry + 2, li_esc)
    px(rx - 1, ry - 1, 3, 3, li)
    px.p(rx - 1, ry - 1, li_luz)
    px.p(rx, ry, li_esc if girou % 2 else li)  # a espiral: o centro escuro em metade das poses (gira)
    px.p(rx + 1, ry + 1, li_esc)
    # ---- o braço de longe (atrás do corpo): só o antebraço e a mão aparecem
    ol = (OMBRO[0] - 1 + sx, OMBRO[1] - 1 + sy)
    ml = mao("longe")
    co = cotovelo(ol, (ml[0] + 0.5, ml[1] + 0.5), *BRACO)
    _capsula(t, co, (ml[0] + 0.5, ml[1] + 0.5), 1.0, pe_esc, pe, pe_esc)
    px(ml[0], ml[1], 2, 2, pe_esc)
    # ---- o hábito: da cintura ao chão, abrindo até a barra; as pregas; o cordão na cintura com as pontas
    b0, b1 = BARRA
    for y in range(y_cint + 1, PES - 1):
        k = (y - y_cint) / (PES - 2 - y_cint)
        a_ = round(fr_c + (b0 - fr_c) * k)
        b_ = round(co_c + (b1 - co_c) * k ** 1.3)
        px(a_, y, b_ - a_ + 1, 1, ha)
        px(a_, y, 1, 1, ha_luz)
        px(b_ - 1, y, 2, 1, ha_esc)
        if k > 0.2:
            px.p(a_ + round((b_ - a_) * 0.45), y, ha_esc)
            px.p(a_ + round((b_ - a_) * 0.75), y, ha_esc)
    px(b0 + 1, PES - 2, b1 - b0 - 1, 1, ha_esc)          # a barra
    px(b0 - 1, PES - 2, 3, 2, "#2a1c12")                  # a ponta da sandália
    # ---- o tronco, linha a linha: a luz na frente, a sombra nas costas
    for y, a_, b_ in TRONCO:
        dx, dy = desvio(y)
        px(a_ + dx, y + dy, b_ - a_ + 1, 1, ha)
        px(a_ + dx, y + dy, 1, 1, ha_luz)
        px(b_ - 1 + dx, y + dy, 2, 1, ha_esc)
    cor_a, cor_b = COR["cordao"]
    px(fr_c, y_cint, co_c - fr_c + 1, 1, cor_a)           # o cordão
    px(fr_c + 1, y_cint + 1, 1, 6, cor_b)                 # as pontas caindo na frente
    px(fr_c + 2, y_cint + 1, 1, 5, cor_a)
    # ---- a cabeça
    cx, cy, olhar = pose["cabeca"]
    pal = {"K": COR["cabelo"][0], "k": COR["cabelo"][2], "w": COR["cabelo"][0], "E": pe_esc, "s": pe, "S": pe_esc,
           "l": pe_luz, "e": "#1a1210", "b": "#8a5a42", "m": "#7a4434"}
    t.grade(X + cx, TOPO + cy, CABECA[olhar], pal)
    # ---- o braço de perto: o braço no pano do hábito, a manga puxada até o meio do antebraço, a mão
    op = (OMBRO[0] + sx, OMBRO[1] + sy)
    mp = mao("perto")
    co = cotovelo(op, (mp[0] + 0.5, mp[1] + 0.5), *BRACO)
    _capsula(t, op, co, 1.6, ha_luz, ha_luz, ha_esc)
    meio = (co[0] + (mp[0] + 0.5 - co[0]) * 0.35, co[1] + (mp[1] + 0.5 - co[1]) * 0.35)
    _capsula(t, co, meio, 1.5, ha_luz, ha_luz, ha_esc)    # a manga puxada, até o meio do antebraço
    _capsula(t, meio, (mp[0] + 0.5, mp[1] + 0.5), 1.1, pe, pe_luz, pe_esc)
    px(mp[0] - 1, mp[1], 3, 2, pe)
    px(mp[0] - 1, mp[1], 3, 1, pe_luz)
    return t


def todas():
    unicos, _, _ = quadros()
    return [figura(pose_de(it)) for it in unicos]
