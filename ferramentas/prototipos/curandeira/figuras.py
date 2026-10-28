"""Quem atende na cabana: Pita e Marta, no estilo das figuras do jogo (sem contorno, três tons por material, o olho de
um pixel, as mãos simples). De lado, voltadas para a esquerda (para o almofariz), na ponta da bancada, as duas de
mangas arregaçadas. O corpo é desenhado pelo contorno de cada linha (a frente e as costas), a cabeça numa grade à mão;
os braços por segmentos com espessura, porque o de longe acompanha o pilão.

Os apoios, decididos antes do giro: o almofariz parado no tampo; a mão de longe segurando a borda dele, parada; a
ponta de baixo do pilão dentro do almofariz, parada; só a ponta de cima do pilão gira numa elipse pequena, e a mão de
perto e o antebraço acompanham (o cotovelo, meio passo). O tronco, a cabeça e a saia não se mexem: o movimento é
contido. O braço que trabalha é o que se vê inteiro (o de perto): os dois braços cruzados na frente do corpo liam como
um "Λ" de palitos."""
from desenho import AL, PES, QH, QW, TAMPO, Pincel, Tela

FIG = {
    "marta": {  # a curandeira: adulta, magra da febre, o lenço na cabeça, o vestido verde-escuro e o avental
        "pele": ("#c49072", "#dcae90", "#946850"),
        "roupa": ("#33402e", "#46573f", "#222b1f"),
        "avental": ("#7e7464", "#958a76", "#5e5649"),
        "cabelo": ("#948a74", "#aca28a", "#665e4e"),  # o lenço de linho (o cabelo escuro aparece na testa)
        "x": 157, "topo": 30,
        "cabeca": [
            "...LKKKk...",
            "..LKKKKKk..",
            ".LKKKKKKkk.",
            ".LLKKKKkkk.",
            "..hhLKKkkk.",
            ".SseSLKkkk.",
            "lsssSKkkkkn",
            ".sssSSkkknn",
            "..SsSS.nn..",
            "..ssS...n..",
            "...sS......",
        ],
        # (y, frente, costas) do tronco, do alto dos ombros à cintura; a saia vai da cintura ao chão, abrindo
        "tronco": [(41, 163, 166), (42, 162, 167), (43, 161, 168), (44, 160, 169), (45, 160, 169), (46, 159, 169),
                   (47, 159, 169), (48, 159, 168), (49, 160, 168), (50, 160, 168), (51, 160, 168), (52, 161, 168),
                   (53, 161, 168), (54, 161, 168)],
        "barra": (156, 172),
        "ombro": (165, 43), "cotovelo": 6, "pega": 0,
    },
    "pita": {  # a aprendiz: uma menina de uns catorze anos, o cabelo castanho preso numa trança, o vestido de lã
        "pele": ("#b87250", "#dc9a70", "#8a4c30"),
        "roupa": ("#5a3e2a", "#765236", "#3a2818"),
        "avental": ("#7e7464", "#958a76", "#5e5649"),
        "cabelo": ("#5a3820", "#76502e", "#3a2414"),
        "x": 157, "topo": 36,
        "cabeca": [
            "...LKKKk..",
            "..LKKKKKk.",
            ".LKKKKKKkk",
            ".KKKKKKkkk",
            ".KssKKKkkk",
            ".SseSKkkk.",
            "lsssSSkk..",
            ".sssSS.kn.",
            "..SsS...n.",
            "..ssS...n.",
        ],
        "tronco": [(46, 162, 166), (47, 161, 167), (48, 160, 167), (49, 160, 167), (50, 160, 167), (51, 160, 167),
                   (52, 160, 167), (53, 160, 167), (54, 161, 167), (55, 161, 167), (56, 161, 167), (57, 161, 167)],
        "barra": (157, 171),
        "ombro": (164, 48), "cotovelo": 4, "pega": 3,  # a menina pega o pilão mais embaixo
    },
}
# a pose de cada quadro: o deslocamento da ponta de cima do pilão numa elipse pequena
GIRO = [(2, 0), (1, 1), (0, 1), (-1, 1), (-2, 0), (-1, -1), (0, -1), (1, -1)]
QUADROS = len(GIRO)
REPOUSO = 0  # a pose parada (movimento reduzido e a pausa): o pilão de pé, a mão nele


def _membro(px, a, b, grossura, cor, luz=None, sombra=None):
    """Um segmento de braço com espessura: a linha repetida para baixo; a de cima na luz, a de baixo na sombra."""
    for k in range(grossura):
        c = luz if (k == 0 and luz) else sombra if (k == grossura - 1 and sombra) else cor
        px.linha(a[0], a[1] + k, b[0], b[1] + k, c)


def figura(quem, i):
    f = FIG[quem]
    t = Tela(QW, QH)
    px = Pincel(t)
    pe, pe_luz, pe_esc = f["pele"]
    ro, ro_luz, ro_esc = f["roupa"]
    av, av_luz, av_esc = f["avental"]
    tronco = f["tronco"]
    y_cint, fr_c, co_c = tronco[-1]
    hx0, hy0 = f["x"], f["topo"]
    # a saia: da cintura ao chão, a frente e as costas abrindo até a barra; a prega de trás no escuro; o avental na frente
    b0, b1 = f["barra"]
    for y in range(y_cint + 1, PES - 1):
        k = (y - y_cint) / (PES - 2 - y_cint)
        a = round(fr_c + (b0 - fr_c) * k)
        b = round(co_c + (b1 - co_c) * k ** 1.4)
        px(a, y, b - a + 1, 1, ro)
        px(b - 1, y, 2, 1, ro_esc)
        if k > 0.25:
            px.p(a + round((b - a) * 0.62), y, ro_esc)
        w = 4 + round(k * 3)
        px(a, y, w, 1, av)
        px(a, y, 1, 1, av_luz)
        px(a + w - 1, y, 1, 1, av_esc)
    px(b0 + 1, PES - 2, b1 - b0 - 1, 1, ro_esc)  # a barra
    px(b0 - 2, PES - 2, 4, 2, "#2a1c12")         # a ponta do sapato
    px(b0 - 2, PES - 2, 2, 1, "#3e2a1a")
    # o tronco, linha a linha: a luz na frente, a sombra nas costas; o avental no peito
    for y, a, b in tronco:
        px(a, y, b - a + 1, 1, ro)
        px(a, y, 1, 1, ro_luz)
        px(b - 1, y, 2, 1, ro_esc)
        if y >= tronco[3][0]:
            px(a, y, 3, 1, av)
            px(a, y, 1, 1, av_luz)
    px(fr_c, y_cint, co_c - fr_c + 2, 1, av_esc)  # a fita da cintura
    px(co_c + 1, y_cint - 1, 2, 3, av)            # o laço atrás
    px.p(co_c + 2, y_cint + 2, av_esc)
    # a cabeça (a grade)
    pal = {"K": f["cabelo"][0], "k": f["cabelo"][2], "L": f["cabelo"][1], "n": f["cabelo"][2],
           "s": pe, "S": pe_esc, "l": pe_luz, "e": "#1a1210", "h": "#2e221c"}
    t.grade(hx0, hy0, f["cabeca"], pal)
    if quem == "pita":  # a trança descendo pelas costas, com a fita na ponta
        alt = len(f["cabeca"])
        for k in range(7):
            px.p(hx0 + 8 + (k % 2), hy0 + alt - 2 + k, f["cabelo"][2 if k % 2 else 0])
        px.p(hx0 + 8, hy0 + alt + 5, "#8a6a44")
    # ---- os braços. O de perto (o esquerdo, o que se vê inteiro) gira o pilão; a mão de longe segura o almofariz,
    # por fora da borda, junto do corpo (o braço dela fica atrás do tronco).
    dx, dy = GIRO[i % QUADROS]
    a, b = AL
    ponta = ((a + b) // 2, TAMPO - 5)                       # a ponta de baixo do pilão, dentro do almofariz
    alto = (ponta[0] + 1 + dx, TAMPO - 12 + dy)             # a ponta de cima
    mao = (alto[0] + round((ponta[0] - alto[0]) * f["pega"] / 7), alto[1] + f["pega"])  # onde a mão pega
    # a mão de longe na borda do almofariz, e o pedaço do antebraço que aparece antes do tronco
    px.linha(b + 4, TAMPO - 3, b + 2, TAMPO - 4, pe_esc)
    px(b, TAMPO - 5, 2, 3, pe_esc)
    # o pilão de madeira clara, da ponta de cima até a boca do almofariz
    px.linha(alto[0], alto[1], ponta[0], ponta[1] - 1, "#8a6a44")
    px.linha(alto[0] + 1, alto[1], ponta[0] + 1, ponta[1] - 1, "#6a4e30")
    # o braço de perto: do ombro, o braço desce e vem para a frente até o cotovelo (que acompanha meio passo do giro);
    # a manga arregaçada acima do cotovelo; o antebraço sobe até a mão fechada no pilão
    om = f["ombro"]
    co = (om[0] - 7 + round(dx / 2), om[1] + f["cotovelo"] + (1 if dy > 0 else 0))
    _membro(px, om, (co[0] + 1, co[1] - 1), 3, ro, ro_luz, ro_esc)
    px(co[0], co[1] - 1, 3, 2, av_luz)                       # a manga arregaçada
    _membro(px, (co[0], co[1]), (mao[0] + 2, mao[1] + 1), 2, pe, pe_luz, pe_esc)
    px(mao[0], mao[1], 3, 2, pe)                             # a mão fechada no pilão
    px(mao[0], mao[1], 1, 1, pe_luz)
    return t
