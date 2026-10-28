"""Quem atende na cabana: Pita e Marta, no estilo das figuras do jogo (sem contorno, três tons por material, o olho de
um pixel, as mãos simples). De lado, voltadas para a esquerda (para o almofariz), na ponta da bancada, as duas de
mangas arregaçadas. O corpo é desenhado pelo contorno de cada linha (a frente e as costas), a cabeça numa grade à mão;
os braços por segmentos de comprimento fixo (o braço não estica nem encolhe: o que não alcança, o corpo leva).

A atividade (terceira passada, 28/10/2026), decidida pelos apoios antes dos quadros:
- **fica parado:** os pés e a barra da saia; o almofariz no tampo; a mão de longe segurando a borda dele (o antebraço
  de longe aparece entre o corpo e o almofariz); o pé do pilão dentro da boca, enquanto a mão está nele;
- **conduz:** a mão de perto no pilão. A ponta de cima gira numa elipse (vai para longe do corpo, passa na frente,
  volta para o lado do corpo e passa atrás), e a mão vai junto;
- **acompanha:** o cotovelo (a dobra sai do comprimento fixo do braço); os ombros e o peito, que vão 1 px para a frente
  quando o pilão vai longe (o braço sozinho não alcança); a cabeça, um quadro depois dos ombros; o olho sempre no
  almofariz. O quadril e a saia só se mexem quando o corpo todo se inclina (olhar a mistura): o quadril vai para trás e
  o alto da saia acompanha, a barra parada.

A rotina (ROTINA): moer algumas voltas; a última volta desacelera e o pilão para de pé; ela se inclina e olha a
mistura; solta o pilão (que fica encostado na borda), tira uma pitada do almofariz, leva ao nariz e cheira; volta,
pega o pilão de novo, e a primeira pose do giro é a mesma de onde se partiu. Marta e Pita fazem a mesma coisa no
ritmo de cada uma: Marta, adulta e experiente, mói mais devagar (aperta nas pontas da volta) e olha e cheira com mais
tempo; Pita, menor, se inclina mais perto do almofariz e é um pouco mais ligeira, sem pressa."""
import math

from desenho import AL, PES, QH, QW, TAMPO, Pincel, Tela

FIG = {
    "marta": {  # a curandeira: adulta, magra da febre, o lenço na cabeça, o vestido verde-escuro e o avental
        "pele": ("#c49072", "#dcae90", "#946850"),
        "roupa": ("#33402e", "#46573f", "#222b1f"),
        "avental": ("#7e7464", "#958a76", "#5e5649"),
        "cabelo": ("#948a74", "#aca28a", "#665e4e"),  # o lenço de linho
        "fios": ("#3a2a20", "#2a1e16"),               # o cabelo escuro que aparece na testa, e a sobrancelha
        "x": 157, "topo": 30,
        # a cabeça de perfil (o nariz na coluna 0): o lenço justo no crânio com o nó na nuca e as pontas caindo; o
        # cabelo escuro na testa; a sobrancelha, o olho de um pixel atrás da ponte do nariz, a maçã do rosto e o fundo
        # da face (magra da febre, sem exagero), a boca, o queixo e o pescoço. "baixo": o rosto virado para o almofariz
        # (o nariz e o olho um pixel abaixo, o queixo recolhido).
        "cabeca": {
            "frente": [
                "...LLKKk...",
                "..LKKKKKkk.",
                ".LKKKKKKkkk",
                ".HHHKKKKkkk",
                ".lsHHKKKkkk",
                ".lwsSHKKkkn",
                ".sesSSKkkn.",
                "lssssSkkn..",
                ".msSSSs....",
                "..sSSsS....",
                "....sSS....",
            ],
            "baixo": [
                "...LLKKk...",
                "..LKKKKKkk.",
                ".LKKKKKKkkk",
                ".LKKKKKKkkk",
                ".HHHKKKKkkk",
                ".lsHHKKkkkn",
                ".wwsSHKkkn.",
                ".lesSSkkn..",
                "lsssSSs....",
                ".mSSsS.....",
                "...sSS.....",
            ],
        },
        "tronco": [(41, 163, 166), (42, 162, 167), (43, 161, 168), (44, 160, 169), (45, 160, 169), (46, 159, 169),
                   (47, 159, 169), (48, 159, 168), (49, 160, 168), (50, 160, 168), (51, 160, 168), (52, 161, 168),
                   (53, 161, 168), (54, 161, 168)],
        "barra": (156, 172),
        "ombro": (165, 43), "braco": (8.5, 9.5), "pega": 1.5,
        "nariz": (157, 37),  # onde a pitada chega (a ponta do nariz na pose de pé)
    },
    "pita": {  # a aprendiz: uma menina de uns catorze anos, o cabelo castanho preso numa trança, o vestido de lã
        "pele": ("#b87250", "#dc9a70", "#8a4c30"),
        "roupa": ("#5a3e2a", "#765236", "#3a2818"),
        "avental": ("#7e7464", "#958a76", "#5e5649"),
        "cabelo": ("#5a3820", "#7a5430", "#3a2414"),
        "fios": ("#3a2414", "#2a1a10"),
        # o cabelo com volume (o brilho no alto da cabeça, a franja de lado caindo na testa, preso atrás da orelha e
        # juntado na nuca para a trança); o rosto de menina: a testa sob a franja, a sobrancelha fina, o olho, o nariz
        # pequeno, a bochecha cheia com um toque corado, a boca e o queixo curto.
        "cabeca": {
            "frente": [
                "...LLKKk..",
                "..LKKLKKk.",
                ".LKKKKKKkk",
                ".KKKKKKKkk",
                ".KlsKKKkkk",
                ".lwsSKkkkk",
                ".sesSEkkn.",
                "lsrssSkn..",
                ".msSSSn...",
                "..ssSS....",
            ],
            "baixo": [
                "...LLKKk..",
                "..LKKLKKk.",
                ".LKKKKKKkk",
                ".KKKKKKKkk",
                ".KKKKKKkkk",
                ".KlsKKkkkk",
                ".wssSEkkn.",
                ".lesSSkn..",
                "lsrSSn....",
                ".mSSs.....",
            ],
        },
        # de pé no banquinho (a bancada é a de Marta: no chão, o almofariz ficava na altura do peito dela e o braço
        # trabalhava esticado na altura do ombro), 2 px mais perto da ponta da bancada
        "tronco": [(42, 160, 164), (43, 159, 165), (44, 158, 165), (45, 158, 165), (46, 158, 165), (47, 158, 165),
                   (48, 158, 165), (49, 158, 165), (50, 159, 165), (51, 159, 165), (52, 159, 165), (53, 159, 165)],
        "barra": (155, 169),
        "ombro": (162, 44), "braco": (7.5, 8.5), "pega": 2,
        "nariz": (155, 39),
        "x": 155, "topo": 32, "chao": PES - 4, "banquinho": (152, 172),
    },
}

# ---------------------------------------------------------------- o pilão e o giro
PE_PILAO = ((AL[0] + AL[1]) // 2, TAMPO - 5)  # o pé do pilão, dentro da boca do almofariz
COMP_PILAO = 8                                # do pé à ponta de cima: o mesmo em todas as poses
BOCA = TAMPO - 6                              # a linha da boca (o lábio): o pilão some dentro dela


def giro(k):
    """A ponta de cima do pilão na pose k da volta (12 por volta): `dx` para os lados (negativo: longe do corpo) e
    `perto` (1 quando a ponta passa na frente, do lado de quem olha, e aparece 1 px mais baixa). Começa de pé, atrás,
    vai para longe, passa na frente, volta para o lado do corpo e fecha atrás. Nas pontas, três poses quase no mesmo
    lugar: o gesto desacelera para virar."""
    a = 2 * math.pi * k / 12
    return -round(3 * math.sin(a)), 1 if math.cos(a) < -0.6 else 0


def ombros_no_giro(k):
    """O corpo na volta: quando o pilão vai longe, os ombros vão 1 px para a frente (a mão não chega lá só com o braço);
    no trecho de longe e da frente, onde a pedra aperta as ervas, descem 1 px (o peso no pilão). A cabeça vai um
    quadro depois dos ombros. O quadril e a saia ficam: é o peito que trabalha."""
    ombro = (-1 if k in (2, 3, 4) else 0, 1 if k in (3, 4) else 0)
    cabeca = (-1 if k in (3, 4, 5) else 0, 1 if k in (4, 5) else 0)
    return ombro, cabeca


# ---------------------------------------------------------------- as poses
def pose_giro(quem, k):
    dx, perto = giro(k)
    om, (cx, cy) = ombros_no_giro(k)
    return {"ombro": om, "quadril": 0, "cabeca": (cx, cy, "frente"), "pilao": (dx, perto), "mao": "pilao"}


def poses_rotina(quem):
    """As poses fora do giro (as mesmas para as duas; o ritmo é o de cada uma). Pita se inclina mais perto. Em cada
    passagem, uma parte vai na frente e as outras chegam depois (o corpo antes da cabeça, a mão antes do corpo): nada
    muda inteiro de um quadro para o outro."""
    n = FIG[quem]["nariz"]
    perto = 1 if quem == "pita" else 0
    pe = PE_PILAO
    return {
        # inclinar-se para olhar a mistura: o peito vai à frente, depois o quadril vai para trás e o peito desce, e
        # por último o rosto vira para dentro do almofariz
        "inclina": {"ombro": (-1, 0), "quadril": 0, "cabeca": (0, 0, "frente"), "pilao": (0, 0), "mao": "pilao"},
        "abaixa": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-1, 1, "frente"), "pilao": (0, 0), "mao": "pilao"},
        "olha": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-2, 1 + perto, "baixo"), "pilao": (0, 0), "mao": "pilao"},
        # soltar o pilão (encostado na borda de longe) e tirar uma pitada da boca do almofariz
        "solta": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-2, 1 + perto, "baixo"), "pilao": "encostado",
                  "mao": (pe[0] + 3, BOCA - 3)},
        "pitada": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-2, 1 + perto, "baixo"), "pilao": "encostado",
                   "mao": (pe[0] + 2, BOCA - 1), "pinca": True},
        # subir a pitada até o nariz: a mão sobe na frente, o corpo se endireita atrás dela, a cabeça vem encontrar a mão
        "ergue": {"ombro": (-1, 1), "quadril": 1, "cabeca": (-2, 1 + perto, "baixo"), "pilao": "encostado",
                  "mao": (pe[0] + 5, BOCA - 4), "pinca": True},
        "endireita": {"ombro": (-1, 0), "quadril": 0, "cabeca": (-1, 1, "frente"), "pilao": "encostado",
                      "mao": (n[0] + 1, n[1] + 6), "pinca": True},
        "cheira": {"ombro": (0, 0), "quadril": 0, "cabeca": (-1, 1, "frente"), "pilao": "encostado",
                   "mao": (n[0] - 1, n[1] + 3), "pinca": True},
        # afastar a mão do rosto, descer e pegar o pilão de novo (ele volta a ficar quase de pé, onde começa a volta)
        "afasta": {"ombro": (0, 0), "quadril": 0, "cabeca": (-1, 0, "frente"), "pilao": "encostado",
                   "mao": (n[0] + 1, n[1] + 6)},
        "desce": {"ombro": (0, 0), "quadril": 0, "cabeca": (-1, 0, "frente"), "pilao": "encostado",
                  "mao": (pe[0] + 4, BOCA - 4)},
        # a mão chega ao cabo encostado antes de fechar nele (não salta da boca do almofariz para o alto do pilão)
        "alcanca": {"ombro": (0, 0), "quadril": 0, "cabeca": (-1, 0, "frente"), "pilao": "encostado",
                    "mao": (pe[0], BOCA - 5)},
        "pega": {"ombro": (0, 0), "quadril": 0, "cabeca": (-1, 0, "frente"), "pilao": (-2, 0), "mao": "pilao"},
    }


# A volta da moagem, (pose do giro, tiques de 100 ms), partindo da pose 1 (o pilão inclinado, onde a mão o pega de
# novo) e fechando de pé. Quarta passada: poucas poses, cada uma sustentada, e o tempo indo para a pressão. Longe do
# corpo, o peito vai à frente e desce (3) e, enquanto a pedra aperta, a cabeça termina de descer (4): o corpo assenta
# no esforço. Depois a ponta passa na frente (6), volta para o lado do corpo (9), sobe (11) e fica de pé (0). Sete
# poses no lugar de doze; a volta dura o mesmo (Pita 1,2 s, Marta 1,4 s). FREIO: a última meia volta, mais lenta.
VOLTA = {"marta": [(1, 1), (3, 3), (4, 3), (6, 2), (9, 2), (11, 2), (0, 1)],
         "pita": [(1, 1), (3, 2), (4, 2), (6, 2), (9, 2), (11, 2), (0, 1)]}
FREIO = {"marta": [(6, 3), (9, 4), (11, 4), (0, 3)], "pita": [(6, 3), (9, 3), (11, 3), (0, 3)]}
# A terceira passada (a volta contínua: as 12 poses, uma por tique) fica congelada em anterior/terceira.

RITMO = {  # quantos tiques de 100 ms cada parte leva
    "marta": {"voltas": 2, "inclina": 2, "abaixa": 2, "olha": 12, "solta": 2, "pitada": 4, "ergue": 2,
              "endireita": 2, "cheira": 9, "afasta": 2, "desce": 2, "alcanca": 1, "pega": 2},
    "pita": {"voltas": 3, "inclina": 1, "abaixa": 2, "olha": 8, "solta": 2, "pitada": 3, "ergue": 1,
             "endireita": 2, "cheira": 6, "afasta": 2, "desce": 1, "alcanca": 1, "pega": 2},
}


def rotina(quem):
    """A sequência de poses, um item por tique de 100 ms: [(nome da pose, k ou None)]. As voltas (VOLTA), a última
    com a segunda metade mais lenta (FREIO) até o pilão parar de pé; depois o olhar, a pitada e a volta ao pilão. A
    pega deixa o pilão onde a pose 1 o tem: a última pose emenda na primeira."""
    r = RITMO[quem]
    seq = []
    volta = VOLTA[quem]
    for _ in range(r["voltas"]):
        for k, n in volta:
            seq.extend([("giro", k)] * n)
    for k, n in volta[:3] + FREIO[quem]:
        seq.extend([("giro", k)] * n)
    seq.extend([("giro", 0)] * 2)                  # o pilão parado de pé
    for nome in ("inclina", "abaixa", "olha", "solta", "pitada", "ergue", "endireita", "cheira", "afasta", "desce",
                 "alcanca", "pega"):
        seq.extend([(nome, None)] * r[nome])
    return seq


PARADA = ("olha", None)  # a pose do movimento reduzido: inclinada sobre o almofariz, a mão no pilão


def quadros(quem):
    """Os desenhos diferentes da rotina, na ordem em que aparecem, e a linha do tempo em índices deles."""
    unicos, tempo = [], []
    for item in [PARADA] + rotina(quem):
        if item not in unicos:
            unicos.append(item)
        tempo.append(unicos.index(item))
    return unicos, tempo[1:], unicos.index(PARADA)


# ---------------------------------------------------------------- o desenho
def _capsula(t, a, b, r, cor, luz, sombra):
    """Um pedaço de braço como forma cheia: os pixels a até `r` do segmento a-b (as pontas arredondadas). Em cada
    coluna, o de cima na luz e o de baixo na sombra (quando a coluna tem 3 ou mais): sem degraus soltos nem buracos."""
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
    """O cotovelo pelos comprimentos fixos do braço (a dobra para baixo). A mão fora do alcance é um erro da pose:
    o corpo tem de ir junto, não o braço esticar."""
    (sx, sy), (hx, hy) = ombro, mao
    d = math.hypot(hx - sx, hy - sy)
    assert d <= l1 + l2 + 0.05, f"a mão em {mao} não alcança do ombro {ombro} ({d:.1f} > {l1 + l2})"
    a = (l1 * l1 - l2 * l2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    ux, uy = (hx - sx) / d, (hy - sy) / d
    px, py = sx + ux * a, sy + uy * a
    c1, c2 = (px - uy * h, py + ux * h), (px + uy * h, py - ux * h)
    return c1 if c1[1] >= c2[1] else c2


def pilao(pose):
    """O pé e a ponta de cima do pilão. Na mão, o pé fica no meio da boca e a ponta gira; encostado, o pé desliza para
    o lado do corpo dentro da boca e o cabo deita na borda de longe. O comprimento é sempre COMP_PILAO."""
    p = pose["pilao"]
    if p == "encostado":
        pe, dx, perto = (PE_PILAO[0] + 2, PE_PILAO[1]), -4, 0
    else:
        (dx, perto), pe = p, PE_PILAO
    alt = math.sqrt(COMP_PILAO ** 2 - dx * dx) - perto
    return pe, (pe[0] + dx, pe[1] - alt)


def desenhar_pilao(t, pe, alto):
    """O pilão de madeira clara, da ponta de cima até a boca: dois pixels por linha (a luz à esquerda), sem degraus
    soltos."""
    (bx, by), (ax, ay) = pe, alto
    y0, y1 = round(ay), BOCA
    for y in range(y0, y1 + 1):
        u = (y - ay) / ((by - ay) or 1)
        x = round(ax + (bx - ax) * u)
        t.px(x, y, "#8a6a44")
        t.px(x + 1, y, "#6a4e30")


def figura(quem, pose):
    f = FIG[quem]
    t = Tela(QW, QH)
    px = Pincel(t)
    pe, pe_luz, pe_esc = f["pele"]
    ro, ro_luz, ro_esc = f["roupa"]
    av, av_luz, av_esc = f["avental"]
    sx, sy = pose["ombro"]
    qx = pose["quadril"]
    tronco = f["tronco"]
    y_cint, fr_c, co_c = tronco[-1]
    y_alto = tronco[0][0]

    def desvio(y):
        """Quanto a linha y do tronco anda: os ombros com o peito, o quadril embaixo; entre eles, a proporção."""
        k = (y_cint - y) / (y_cint - y_alto)
        return round(sx * k + qx * (1 - k)), round(sy * k)

    chao = f.get("chao", PES)  # onde pisa (Pita, no banquinho)
    if "banquinho" in f:  # o banquinho de madeira: o tampo com a aresta acesa, os dois pés no chão
        x0, x1 = f["banquinho"]
        px(x0, chao, x1 - x0, 1, "madeiraLuz")
        px(x0, chao + 1, x1 - x0, 1, "madeira")
        px(x0, chao + 2, x1 - x0, 1, "madeiraEsc")
        for xx in (x0 + 1, x1 - 3):
            px(xx, chao + 3, 2, PES - chao - 3, "madeira")
            px(xx + 1, chao + 3, 1, PES - chao - 3, "madeiraEsc")
    # ---- o braço de longe: só o antebraço aparece, do corpo até a mão que segura o almofariz (parada)
    a, b = AL
    _capsula(t, (fr_c - 1 + qx, BOCA + 2), (b + 2, BOCA + 1), 1.0, pe_esc, pe, pe_esc)
    # ---- a saia: da cintura (que vai com o quadril) ao chão (parado), abrindo até a barra; o avental na frente
    b0, b1 = f["barra"]
    for y in range(y_cint + 1, chao - 1):
        k = (y - y_cint) / (chao - 2 - y_cint)
        d = round(qx * (1 - k) ** 1.5)
        a_ = round(fr_c + (b0 - fr_c) * k) + d
        b_ = round(co_c + (b1 - co_c) * k ** 1.4) + d
        px(a_, y, b_ - a_ + 1, 1, ro)
        px(b_ - 1, y, 2, 1, ro_esc)
        if k > 0.25:
            px.p(a_ + round((b_ - a_) * 0.62), y, ro_esc)
        w = 4 + round(k * 3)
        px(a_, y, w, 1, av)
        px(a_, y, 1, 1, av_luz)
        px(a_ + w - 1, y, 1, 1, av_esc)
    px(b0 + 1, chao - 2, b1 - b0 - 1, 1, ro_esc)  # a barra
    px(b0 - 2, chao - 2, 4, 2, "#2a1c12")         # a ponta do sapato
    px(b0 - 2, chao - 2, 2, 1, "#3e2a1a")
    # ---- o tronco, linha a linha: a luz na frente, a sombra nas costas; o avental no peito
    for y, a_, b_ in tronco:
        dx, dy = desvio(y)
        yy = y + dy
        px(a_ + dx, yy, b_ - a_ + 1, 1, ro)
        px(a_ + dx, yy, 1, 1, ro_luz)
        px(b_ - 1 + dx, yy, 2, 1, ro_esc)
        if y >= tronco[3][0]:
            px(a_ + dx, yy, 3, 1, av)
            px(a_ + dx, yy, 1, 1, av_luz)
    px(fr_c + qx, y_cint, co_c - fr_c + 2, 1, av_esc)  # a fita da cintura
    px(co_c + 1 + qx, y_cint - 1, 2, 3, av)            # o laço atrás
    px.p(co_c + 2 + qx, y_cint + 2, av_esc)
    # ---- a cabeça (a grade da pose)
    cx, cy, olhar = pose["cabeca"]
    hx, hy = f["x"] + cx, f["topo"] + cy
    linhas = f["cabeca"][olhar]
    pal = {"K": f["cabelo"][0], "k": f["cabelo"][2], "L": f["cabelo"][1], "n": f["cabelo"][2],
           "H": f["fios"][0], "w": f["fios"][1], "E": pe_esc,
           "s": pe, "S": pe_esc, "l": pe_luz, "e": "#1a1210", "m": "#7a4434", "r": "#c87a62"}
    t.grade(hx, hy, linhas, pal)
    if quem == "pita":  # a trança descendo pelas costas, com a fita na ponta (presa na nuca: vai com a cabeça em cima e
        # com as costas embaixo)
        alt = len(linhas)
        for k in range(7):
            d = cx if k < 2 else desvio(y_alto + k)[0]
            px.p(hx - cx + d + 8 + (k % 2), hy + alt - 2 + k, f["cabelo"][2 if k % 2 else 0])
        px.p(hx - cx + desvio(y_alto + 7)[0] + 8, hy + alt + 5, "#8a6a44")
    # ---- os dedos de longe na borda do almofariz (parados)
    px(b - 1, BOCA - 1, 2, 1, pe_esc)
    px(b + 1, BOCA - 1, 1, 3, pe_esc)
    # ---- o pilão e o braço de perto
    p0, p1 = pilao(pose)
    desenhar_pilao(t, p0, p1)
    if pose["mao"] == "pilao":
        k = f["pega"] / COMP_PILAO
        mao = (p1[0] + (p0[0] - p1[0]) * k, p1[1] + (p0[1] - p1[1]) * k)
    else:
        mao = pose["mao"]
    om = (f["ombro"][0] + sx, f["ombro"][1] + sy)
    l1, l2 = f["braco"]
    co = cotovelo(om, (mao[0] + 0.5, mao[1] + 1), l1, l2)
    # o braço, do ombro ao cotovelo, no pano do vestido; a manga arregaçada dobrada acima do cotovelo; o antebraço
    _capsula(t, om, co, 1.5, ro_luz, ro_luz, ro_esc)
    dob = (om[0] + (co[0] - om[0]) * 0.8, om[1] + (co[1] - om[1]) * 0.8)
    _capsula(t, dob, co, 1.6, ro_luz, ro_luz, ro_esc)
    _capsula(t, co, (mao[0] + 0.5, mao[1] + 1), 1.1, pe, pe_luz, pe_esc)
    mx, my = round(mao[0]), round(mao[1])
    if pose.get("pinca"):  # os dedos juntos segurando a pitada (a ponta clara é o pó de ervas)
        px(mx - 1, my, 2, 2, pe)
        px.p(mx - 1, my, pe_luz)
        px.p(mx + 1, my + 1, pe_esc)
        px.p(mx - 2, my, "#5a6a32")
    else:  # a mão fechada em volta do pilão: o punho de 3×3, o pilão aparecendo em cima
        px(mx - 1, my, 3, 3, pe)
        px(mx - 1, my, 3, 1, pe_luz)
        px(mx + 1, my + 1, 1, 2, pe_esc)
    return t


def todas(quem):
    """Os desenhos da rotina (na ordem de `quadros`)."""
    unicos, _, _ = quadros(quem)
    return [figura(quem, pose_de(quem, item)) for item in unicos]


def pose_de(quem, item):
    nome, k = item
    return pose_giro(quem, k) if nome == "giro" else poses_rotina(quem)[nome]
