"""Quem está na taverna, candidata E (estudo estático): cada pessoa desenhada à mão no lugar que a projeção da sala dá
para o assento dela (desenho.P), na escala daquele lugar (desenho.m: de 16 a 21 px por metro), sem contorno, três tons
por material, o olho de um pixel. Uma regra para todos: a cabeça com ~0,27 m, quem senta com o quadril a 0,45 m e o
alto da cabeça a ~1,35 m (Morel, "um homem grande", a 1,45 m e mais largo; o taverneiro, de pé, corpulento).

Cada conjunto foi resolvido junto, como na D (o assento, a orientação, o alcance, a atividade), agora com uma escala e
uma câmera só para a sala inteira: as posições saem de `desenho.P` (anotadas em cada figura), não de ajustes à mão.

A ordem do desenho segue a profundidade: quem está atrás de um móvel vem antes dele, e o móvel é redesenhado por cima
(`desenho.mesas(parte=...)`); as mãos que pousam no tampo vêm depois (`maos`)."""
from . import desenho as D

PELE = {"s": "#c99a78", "S": "#9a6e52", "l": "#e0b494", "e": "#24170f"}
CANECA = {"M": "#9a9da4", "m": "#5e6168", "N": "#c4c7cc"}


def pal(**cores):
    return {**PELE, **CANECA, **cores}


def grade_valida(nome, linhas):
    larg = len(linhas[0])
    for i, l in enumerate(linhas):
        assert len(l) == larg, f"{nome}: a linha {i} tem {len(l)} colunas, não {larg}"
    return linhas


# ---------------------------------------------------------------- o taverneiro, de pé atrás do balcão
# P(-6.2, 2.6): os pés em y 70, o alto da cabeça em 40, m = 16,6 (corpulento: os ombros de 9). O balcão (1,05 m) o corta
# na cintura (o tampo em y 54-57). Avental de couro escuro; seca a caneca com o pano na altura do peito.
TAVERNEIRO = dict(x=51, y=40, pal=pal(B="#4a3226", b="#33231a", R="#454552", r="#32323c", Q="#5a5a68",
                                      A="#6a4a30", a="#4e3622", W="#c8b89a"), grade=[
    ".....lss.....",
    "....lsssS....",
    "....seseS....",
    "....BsSsB....",
    ".....BBb.....",
    ".....sSs.....",
    "..QRRRRRRRr..",
    ".QRRAAAAARRr.",
    ".QRRAAAAARRr.",
    ".QR.AAAAa.Rr.",
    ".QRsWNMmAsRr.",
    ".Qrs.WMmmsrr.",
    ".Qr.lWMmm.rr.",
    ".Qr..AAAA.rr.",
    "..r..AAAA..r.",
])

# ---------------------------------------------------------------- a mesa comprida: três conversando
# A freguesa, no banco do outro lado, P(-4.6, 5.1): o assento em y 75, o alto da cabeça em 57, m = 19. De três quartos
# (virada para a direita, para a cabeceira); o tampo a corta em y 71. As duas mãos em volta da caneca, no tampo.
FREGUESA = dict(x=66, y=57, pal=pal(K="#5a3a22", L="#c8bea4", g="#8e866e", G="#4e6a44", v="#3a5032", V="#64804f",
                                    W="#d6ccb4"), grade=[
    "....LLL.....",
    "...gLLLL....",
    "...gLKsl....",
    "...gLesS....",
    "....gLsS....",
    ".....Ss.....",
    "..vGWWGGV...",
    ".vGGGWGGGV..",
    ".vGvGGGvGV..",
    ".vGvGGGvGV..",
    ".vGvGGGvGV..",
    ".vGvGGGvGV..",
    ".vvvGGGvvV..",
    ".vvvGGGvvV..",
])
FREGUESA_MAOS = dict(x=66, y=69, grade=[
    "..vG....Gv..",
    "...vsMMsv...",
    "....smms....",
])

# O homem da cabeceira, na cadeira da direita, P(-1.75, 5.9): o assento em y 78,5, a cabeça em 60,6, m = 20. De
# perfil, virado para os outros dois; a coxa para a frente debaixo da ponta do tampo (o joelho em x 116), a canela até
# o piso (y 87); o antebraço no tampo, a mão na caneca.
CABECEIRA = dict(x=110, y=60, pal=pal(K="#7a3e1e", k="#52280f", B="#8a4a24", W="#b8ae96", w="#8e866e", N="#5a3e2a",
                                      n="#3e2a1c", P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "............kKKk..",
    "...........kKKKKk.",
    "..........ssKKKKk.",
    "..........seKKKk..",
    ".........sssKKk...",
    "..........BBBk....",
    "...........sS.....",
    "..........WNNNn...",
    ".........WWNNNNn..",
    ".........WwNNNNn..",
    "........WWwNNNNn..",
    "......WWw.NNNNNn..",
    "...sWWw...NNNNNn..",
    "..MMs.....NNNNNn..",
    "..mm......NNNNNn..",
    "..........NNNNNn..",
    "..........nnnnnn..",
    "......pPPPPPPPPPp.",
    "......pPPPPPPPPPp.",
    "......pPP.........",
    "......pPP.........",
    "......pPP.........",
    "......pPP.........",
    "......pPP.........",
    "......pPP.........",
    "......pPP.........",
    ".....OOOO.........",
])

# O freguês de costas, no banco da frente, P(-3.3, 6.9): o assento em y 83, a cabeça em 65, m = 21. Os ombros caindo
# do pescoço, os braços curtos (vão para a frente, até os cotovelos no tampo, em y 74), a cintura, o quadril no banco.
COSTAS = dict(x=83, y=65, pal=pal(K="#4a3020", k="#33200f", H="#6a4a30", U="#3e4a5e", u="#2b3343", V="#52607a",
                                  c="#3a2416", C="#6a4a2c"), grade=[
    "......KKKK......",
    ".....KKHKKK.....",
    ".....kKHKKk.....",
    ".....sKKKKs.....",
    ".....SkKKkS.....",
    "......kkkk......",
    "......sSSs......",
    "....VUUUUUUu....",
    "..VVUUUUUUUUuu..",
    ".VVUUuUUUUuUUuu.",
    ".uuUUuUUUUuUUuu.",
    "....VUUUUUUu....",
    "....VUUUUUUu....",
    "....VUUUUUUu....",
    "....VUUUUUUu....",
    "....cccCcccc....",
    "...VUUUUUUUUu...",
    "..VUUUUUUUUUUu..",
    "..uuuuuuuuuuuu..",
])

# ---------------------------------------------------------------- a mesa redonda: dois jogando
# Atrás da mesa, no banquinho, P(2.7, 4.6): o assento em y 72, a cabeça em 55, m = 18,6. De três quartos, virado para o
# outro (para a esquerda); embaixo do tampo, as coxas e as canelas até o piso (y 81): ele está sentado, não suspenso.
RODA_ATRAS = dict(x=205, y=55, pal=pal(K="#2a2420", k="#1a1612", B="#2a2420", Y="#a88a4e", y="#7a6236",
                                       X="#c4a464", P="#3e3a44", p="#2a2830", O="#1e1812"), grade=[
    "....KKKk...",
    "...KKKKKk..",
    "...lsKKKk..",
    "...esSKKk..",
    "...ssBKk...",
    "....sS.....",
    "..XYYYYYy..",
    ".XYYYYYYYy.",
    ".XYyYYYYYy.",
    ".XYyYYYYYy.",
    ".XYyYYYYYy.",
    ".XYYYYYYYy.",
    ".yyyyyyyyy.",
    "..PPPPPPp..",
    "..PPPPPPp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    "..pP...Pp..",
    ".OOO...OOO.",
])
RODA_ATRAS_MAOS = dict(x=205, y=66, grade=[
    "..XYs......",
    "...s.......",
])
# Do lado esquerdo, no banquinho, P(1.85, 5.2): o assento em y 75, a cabeça em 58, m = 19,2. De perfil, virado para
# o tabuleiro; a coxa até o joelho em x 204, a canela até o piso (y 83); o braço estendido até a peça (0,6 m).
RODA_LADO = dict(x=191, y=57, pal=pal(K="#9a968e", k="#6e6a62", B="#b8b4aa", N="#4a6a56", n="#33493c", Z="#628a72",
                                      P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "..kKKK..............",
    ".kKKKKs.............",
    ".kKKKes.............",
    ".kKKssss............",
    "..kKSss.............",
    "...kBBB.............",
    "....SBB.............",
    "..nNNNZ.............",
    ".nNNNNNZ............",
    ".nNNNNNNZZ..........",
    ".nNNNNnNNZZZ........",
    ".nNNNNnNN..ZZZZs....",
    ".nNNNNNN............",
    ".nNNNNNN............",
    ".nNNNNNN............",
    ".nNNNNNN............",
    ".nnnnnnnPPPPp.......",
    "..pPPPPPPPPPPp......",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "............pPP.....",
    "...........OOOO.....",
])

# ---------------------------------------------------------------- junto do fogo: aquece as mãos
# No banquinho à esquerda da laje, P(-0.55, 1.55): o assento em y 58, a cabeça em 45,6, m = 15,6. De perfil, virado
# para a lareira, inclinado; os antebraços estendidos, as palmas abertas para o fogo; as coxas e as canelas até o piso.
JUNTO_FOGO = dict(x=145, y=45, pal=pal(H="#7a6a54", h="#54483a", J="#968466", P="#3e3630", O="#2a1e16"), grade=[
    ".....hHHH.....",
    "....hHHHHH....",
    "....hHHHHs....",
    "....hHHHss....",
    "....hHHHJ.....",
    "...hHHHHHJJ...",
    "...hHHHHHHJJls",
    "...hHHHHHHH.ls",
    "...hHHHHHHH...",
    "...hHHHHHHH...",
    "....hHHHHHH...",
    "....hHHHHHH...",
    "....PPPPPPPPP.",
    "....PPPPPPPPPP",
    "...........PP.",
    "...........PP.",
    "...........PP.",
    "...........PP.",
    "...........PP.",
    "..........OOOO",
])

# ---------------------------------------------------------------- Morel, no banco do canto
# P(7.1, 4.5): o assento em y 71, a cabeça em 53, m = 18,5, desenhado a ~20 (o porte grande, o banco robusto, a mesma
# régua da sala). A aparência estabelecida (retratos.js, MOREL_FIGURA): o cabelo e a barba castanhos, a ombreira cinza
# no ombro da frente, o couro com o vermelho no peito, a pele no ombro de trás (é o que o reconhece de longe; a
# cicatriz é um traço claro só). As costas no espaldar, o quadril no assento, as coxas para a frente até debaixo da
# borda da mesa, as botas no piso; inclinado, a colher na tigela do ensopado.
MOREL = dict(x=276, y=53, pal=pal(C="#6a4a2c", c="#4e3420", P="#c09070", p="#9a6c52", x="#e0b8a0", b="#5a3e2a",
                                  B="#3e2a1c", S="#9a9ca4", T="#6e7078", L="#7a5838", l="#54391f", R="#a03a2c",
                                  F="#7a7064", f="#56504a", Q="#3e3a36", q="#2a2622", O="#2a1e16", w="#c4c7cc"), grade=[
    "............cCCCCc....",
    "...........cCCCCCCc...",
    "...........PPxPCCCc...",
    "..........PePPxCCc....",
    "..........PPPPPxCc....",
    "...........bBBBBb.....",
    "............bBBb......",
    ".........SSSLRRLFFF...",
    "........STSSLRRLLFFf..",
    "........STLLLRRLLLFf..",
    ".......lLLLLLRRLLLLl..",
    ".....lLLlLLLLRRLLLLl..",
    "...wPLl..LLLLRRLLLLl..",
    ".........LLLLRRLLLLl..",
    ".........LLLLLLLLLLl..",
    ".........lccccccccc...",
    "......QQQQQQQQQQQQq...",
    "......QqQQQQQQQQQq....",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "......Qq..............",
    "....OOOq..............",
])


# ---------------------------------------------------------------- o desenho, na ordem da profundidade
def figura(px, f, nome):
    px.grade(f["x"], f["y"], grade_valida(nome, f["grade"]), f["pal"])


def maos(px, f, m_, nome):
    px.grade(m_["x"], m_["y"], grade_valida(nome, m_["grade"]), f["pal"])


def desenhar(px, r, morel=True):
    """As pessoas por cima da sala (desenho.sala), de trás para a frente."""
    figura(px, JUNTO_FOGO, "junto do fogo")
    figura(px, TAVERNEIRO, "taverneiro")
    D.balcao(px)
    if morel:
        figura(px, MOREL, "Morel")
    figura(px, RODA_ATRAS, "roda, atrás")
    D.mesas(px, parte="roda_mesa")
    maos(px, RODA_ATRAS, RODA_ATRAS_MAOS, "roda, atrás (mãos)")
    figura(px, RODA_LADO, "roda, de lado")
    figura(px, FREGUESA, "freguesa")
    D.mesas(px, parte="longa")
    maos(px, FREGUESA, FREGUESA_MAOS, "freguesa (mãos)")
    figura(px, CABECEIRA, "cabeceira")
    D.mesas(px, parte="longa_perto")
    figura(px, COSTAS, "freguês de costas")
