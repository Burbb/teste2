"""Quem está na taverna, candidata D (estudo estático): cada pessoa desenhada à mão junto do assento, da mesa e do que
ela faz, na escala do lugar em que está (desenho.m), sem contorno, três tons por material, o olho de um pixel.

A lição da C: as figuras estavam certas uma a uma e erradas em conjunto (Morel na ponta do banco longe do espaldar,
o jogador de amarelo sem assento, o homem de marrom sentado ao mesmo tempo na mesa e no balcão). Aqui cada conjunto
foi resolvido junto, nesta ordem: o assento (onde o quadril pousa), a orientação do quadril, do tronco e das pernas, o
alcance até a mesa ou o objeto (o braço de 0,6 m), e a atividade. As partes visíveis explicam a pose; as escondidas
(atrás do tampo, embaixo do quadro) não a contradizem.

A ordem do desenho decide quem está na frente: quem está atrás de um móvel é desenhado antes dele, e o móvel é
redesenhado por cima; as mãos que pousam no tampo vêm depois (`maos`)."""
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


# ---------------------------------------------------------------- o taverneiro, de frente, atrás do balcão
# Corpulento, careca, a barba escura; a camisa de ardósia de mangas arregaçadas e o avental de couro (escuro: a caneca
# clara e as mãos se leem contra ele, não somem num claro só). Seca a caneca na altura do peito: a mão de lá a segura
# pela asa, a de cá esfrega com o pano. m(71) = 19: a cabeça de 6, os ombros de 11.
TAVERNEIRO = dict(x=67, y=37, pal=pal(B="#4a3226", b="#33231a", R="#454552", r="#32323c", Q="#5a5a68",
                                      A="#6a4a30", a="#4e3622", W="#c8b89a"), grade=[
    "......lss......",
    ".....lsssS.....",
    ".....seseS.....",
    ".....BsSsB.....",
    ".....BBBBB.....",
    "......BBb......",
    "......sSs......",
    "...QRRRRRRRr...",
    "..QRRAAAAARRr..",
    "..QRRAAAAARRr..",
    "..QRsWNMmAsRr..",
    "..Qrs.WMmmsrr..",
    "..Qr.lWMmm.rr..",
])

# ---------------------------------------------------------------- a mesa comprida da esquerda: três conversando
# A freguesa, do outro lado, de três quartos (virada para a direita, para a cabeceira): o lenço, o vestido verde, as
# duas mãos em volta da caneca. m(79) = 23.
FREGUESA = dict(x=30, y=49, pal=pal(K="#5a3a22", L="#c8bea4", g="#8e866e", G="#4e6a44", v="#3a5032", V="#64804f",
                                    W="#d6ccb4"), grade=[
    "....LLLL....",
    "...gLLLLL...",
    "...gLKKsl...",
    "...gLseSe...",
    "...gLssSs...",
    "....gLss....",
    ".....Ss.....",
    "..vGGWWGGV..",
    ".vGGGGWGGGV.",
    ".vGGGGGGGGV.",
    ".vGvGGGGvGV.",
    ".vGvGGGGvGV.",
    ".vGvGGGGvGV.",
    ".vGvGGGGvGV.",
    ".vGvGGGGvGV.",
    ".vvvGGGGvvV.",
])
FREGUESA_MAOS = dict(x=30, y=64, grade=[
    "..vG....Gv..",
    "...vs..sv...",
    "....s..s....",
])

# Na cabeceira da direita, de perfil (virado para a esquerda, para os outros dois): o homem de barba ruiva, a camisa
# clara, o colete de couro, sentado numa cadeira de lado (o encosto atrás das costas, longe do balcão, que termina
# antes dele). O quadril no assento, a coxa para a frente debaixo da ponta da mesa, a canela até o piso; o antebraço
# no tampo, a mão na caneca. m(88) = 27.
CABECEIRA = dict(x=88, y=52, pal=pal(K="#7a3e1e", k="#52280f", B="#8a4a24", W="#b8ae96", w="#8e866e", N="#5a3e2a",
                                     n="#3e2a1c", P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "..............kKKKk.....",
    ".............kKKKKKk....",
    "............ssKKKKKk....",
    "............seKKKKk.....",
    "...........sssSKKk......",
    "............ssSKk.......",
    "............BBBk........",
    ".............sS.........",
    "............WNNNNn......",
    "...........WWNNNNNn.....",
    "...........WwNNNNNn.....",
    "..........WWwNNNNNn.....",
    ".........WWwNNNNNNn.....",
    "........WWw.NNNNNNn.....",
    "............NNNNNNn.....",
    "............NNNNNNn.....",
    "............NNNNNNn.....",
    "............NNNNNNn.....",
    "............NNNNNNn.....",
    "............NNNNNNn.....",
    "............nnnnnnn.....",
    ".......pPPPPPPPPPPPp....",
    "......pPPPPPPPPPPPPp....",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    "......pPP...............",
    ".....OOOO...............",
])
CABECEIRA_MAOS = dict(x=88, y=65, grade=[
    "....WWw.................",
    "..Mls...................",
    "..Mm....................",
])

# O freguês de costas, no banco da frente (m(103) = 33): a nuca, o cabelo preso, as orelhas; os ombros caindo do
# pescoço (não uma barra), os braços separados do tronco pela costura e descendo até os cotovelos, apoiados na borda
# da mesa; a cintura, o cinto, e o quadril mais largo assentado no banco, com a aba do casaco.
COSTAS = dict(x=52, y=59, pal=pal(K="#4a3020", k="#33200f", H="#6a4a30", U="#3e4a5e", u="#2b3343", V="#52607a",
                                  c="#3a2416", C="#6a4a2c"), grade=[
    ".......KKKK.......",
    "......KKHKKK......",
    ".....kKKHKKKk.....",
    ".....kKKKKKKk.....",
    ".....sKKKKKKs.....",
    ".....SkKKKKkS.....",
    "......kKKKKk......",
    ".......kkkk.......",
    ".......sSSs.......",
    ".....VUUUUUUu.....",
    "...VVUUUUUUUUuu...",
    "..VVUUUUUUUUUUuu..",
    "..VUUuUUUUUUuUUu..",
    ".VVUUuUUUUUUuUUuu.",
    ".VUUUuUUUUUUuUUUu.",
    ".uUUuuUUUUUUuuUUu.",
    "..uu.uUUUUUUu.uu..",
    ".....VUUUUUUu.....",
    ".....VUUUUUUu.....",
    ".....VUUUUUUu.....",
    ".....VUUUUUUu.....",
    ".....VUUUUUUu.....",
    ".....ccccCccc.....",
    "....VUUUUUUUUu....",
    "...VUUUUUUUUUUu...",
    "...VUUUUUUUUUUu...",
    "..VUUUUUUUUUUUUu..",
    "..VUUUUUUUUUUUUu..",
    "..uuuuuuuuuuuuuu..",
])

# ---------------------------------------------------------------- a mesa redonda: dois jogando
# Atrás da mesa, de três quartos (virado para a esquerda, para o outro), no banquinho: o casaco ocre mais claro (para
# se separar da madeira e do piso); embaixo do tampo, as coxas e as canelas dele e os pés do banquinho (ele está
# sentado, não suspenso); a mão no tabuleiro. m(72) = 20.
RODA_ATRAS = dict(x=227, y=46, pal=pal(K="#2a2420", k="#1a1612", B="#2a2420", Y="#a88a4e", y="#7a6236",
                                       X="#c4a464", P="#3e3a44", p="#2a2830", O="#1e1812"), grade=[
    ".....KKKk...",
    "....KKKKKk..",
    "....lsKKKk..",
    "....esSKKk..",
    "...sssSKk...",
    "....ssBk....",
    ".....sS.....",
    "...XYYYYYy..",
    "..XYYYYYYYy.",
    "..XYyYYYYYy.",
    "..XYyYYYYYy.",
    "..XYyYYYYYy.",
    "..XYyYYYYYy.",
    "..XYYYYYYYy.",
    "..XYYYYYYYy.",
    "..yyyyyyyyy.",
    "...PPPPPPp..",
    "...pPPPPPp..",
    "...pP...Pp..",
    "...pP...Pp..",
    "...pP...Pp..",
    "...pP...Pp..",
    "...pP...Pp..",
    "..OOO..OOO..",
])
RODA_ATRAS_MAOS = dict(x=227, y=57, grade=[
    "..XYs.......",
    "...s........",
])
# Do lado esquerdo, de perfil (virado para a direita, para o tabuleiro): o velho de barba grisalha, o casaco
# verde-musgo mais claro; no banquinho, o quadril no assento, a coxa até debaixo da borda, a canela até o piso; o braço
# estendido até a peça no tabuleiro (0,5 m do ombro à mão). m(79) = 23.
RODA_LADO = dict(x=202, y=49, pal=pal(K="#9a968e", k="#6e6a62", B="#b8b4aa", N="#4a6a56", n="#33493c", Z="#628a72",
                                      P="#4a4038", p="#332c26", O="#2a1e16", T="#8c6238", t="#47301c"), grade=[
    "..kKKK................",
    ".kKKKKs...............",
    ".kKKKes...............",
    ".kKKssss..............",
    "..kKSss...............",
    "...kBBB...............",
    "....SBB...............",
    "...nNNNZ..............",
    "..nNNNNNZ.............",
    "..nNNNNNNZ............",
    "..nNNNNnNNZZ..........",
    "..nNNNNnNNNZZZZ.......",
    "..nNNNNNNN....ZZZs....",
    "..nNNNNNN.............",
    "..nNNNNNN.............",
    "..nNNNNNN.............",
    "..nNNNNNN.............",
    "..nNNNNNN.............",
    "..nnnnnnn.............",
    "...pPPPPPPPPPPPp......",
    "...pPPPPPPPPPPPPp.....",
    "..TTTTTTTT.....pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t......pPP....",
    "...t....t.....OOOO....",
])

# ---------------------------------------------------------------- junto do fogo: aquece as mãos
# Um velho de capuz, no banquinho baixo à direita da laje, inclinado para a lareira: os antebraços estendidos para a
# boca, as palmas abertas para o fogo; as coxas para a frente, as canelas até o piso. A ação explica o corpo. m(63) = 16.
JUNTO_FOGO = dict(x=176, y=41, pal=pal(H="#7a6a54", h="#54483a", J="#968466", P="#3e3630", O="#2a1e16",
                                       T="#8c6238", t="#47301c"), grade=[
    "...........HHHh...",
    "..........HHHHHh..",
    ".........sHHHHHh..",
    ".........ssHHHHh..",
    "..........JHHHHh..",
    ".........JHHHHHHh.",
    ".......JJHHHHHHHh.",
    "...lsJJJHHHHHHHHh.",
    "...ls..JHHHHHHHHh.",
    "........HHHHHHHHh.",
    "........JHHHHHHHh.",
    ".........HHHHHHHh.",
    ".........hHHHHHHh.",
    "........PPPPPPPhh.",
    ".......PPPPTTTTTT.",
    ".......PP..t....t.",
    ".......PP..t....t.",
    ".......PP..t....t.",
    ".......PP..t....t.",
    ".......PP..t....t.",
    "......OOO..t....t.",
])

# ---------------------------------------------------------------- Morel, no canto
# A aparência estabelecida (retratos.js, MOREL_FIGURA) e o porte de "um homem grande" (eventos/comitiva.py), um pouco
# acima da régua (m(76) = 21, desenhado a 24): o cabelo e a barba castanhos, a ombreira cinza no ombro da frente e a
# pele no de trás, o couro com o vermelho no peito (o que o reconhece de longe; a cicatriz é um traço claro só). No
# banco de espaldar, as costas no espaldar, o quadril no assento, as coxas para a frente e as botas no piso; inclinado
# para a mesa, a colher na tigela do ensopado e a outra mão na borda (come "sem levantar os olhos do prato").
MOREL = dict(x=285, y=43, pal=pal(C="#6a4a2c", c="#4e3420", P="#c09070", p="#9a6c52", x="#e0b8a0", b="#5a3e2a",
                                  B="#3e2a1c", S="#9a9ca4", T="#6e7078", L="#7a5838", l="#54391f", R="#a03a2c",
                                  F="#7a7064", f="#56504a", Q="#3e3a36", q="#2a2622", O="#2a1e16", w="#c4c7cc"), grade=[
    "..............cCCCCc.........",
    ".............cCCCCCCc........",
    ".............PPxPCCCc........",
    "............PePPxCCCc........",
    "............PPPPPxCc.........",
    ".............bBBBBbc.........",
    "..............bBBBb..........",
    "...........SSSSLRRLLFFF......",
    "..........STTSSLRRLLLFFf.....",
    "..........STSSLLRRLLLLFf.....",
    "..........SSLLLLRRLLLLLf.....",
    ".........lLLlLLLRRLLLLLl.....",
    ".......lLLl.LLLLRRLLLLLl.....",
    ".....PlLl...LLLLRRLLLLLl.....",
    "...wPLl.....LLLLRRLLLLLl.....",
    "............LLLLRRLLLLLl.....",
    "............LLLLLLLLLLLl.....",
    "............lLLLLLLLLLLl.....",
    "............lcccccccccc......",
    "...........QQQQQQQQQQQQq.....",
    "..........QQQQQQQQQQQQQq.....",
    ".........QQQQQQQQQQQQQQq.....",
    ".........QqQQQQQQQQQQQq......",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".........Qq..................",
    ".......OOOq..................",
    ".......OOOO..................",
])


# ---------------------------------------------------------------- o desenho, na ordem da profundidade
def figura(px, f, nome):
    px.grade(f["x"], f["y"], grade_valida(nome, f["grade"]), f["pal"])


def maos(px, f, m_, nome):
    px.grade(m_["x"], m_["y"], grade_valida(nome, m_["grade"]), f["pal"])


def desenhar(px, r, morel=True):
    """As pessoas por cima da sala (desenho.sala), de trás para a frente, com os móveis que ficam na frente delas
    redesenhados por cima e as mãos que pousam nos tampos depois deles."""
    figura(px, JUNTO_FOGO, "junto do fogo")
    if morel:
        figura(px, MOREL, "Morel")
    figura(px, RODA_ATRAS, "roda, atrás")
    D.mesa_meio(px)
    maos(px, RODA_ATRAS, RODA_ATRAS_MAOS, "roda, atrás (mãos)")
    figura(px, RODA_LADO, "roda, de lado")
    figura(px, TAVERNEIRO, "taverneiro")
    D.balcao(px)
    figura(px, FREGUESA, "freguesa")
    D.cadeira_lado(px)
    figura(px, CABECEIRA, "cabeceira")
    D.mesa_frente(px)
    maos(px, FREGUESA, FREGUESA_MAOS, "freguesa (mãos)")
    maos(px, CABECEIRA, CABECEIRA_MAOS, "cabeceira (mãos)")
    D.banco(px, 34, 92, 104)
    figura(px, COSTAS, "freguês de costas")
