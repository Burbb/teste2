"""Quem está na taverna, candidata F (estudo estático): as poses da referência aprovada ("Taverna medieval entre
brasas e sombras"), redesenhadas à mão na grade do jogo, cada pessoa no ponto que a projeção da sala dá ao assento
dela (desenho.P, anotado em cada figura) e na escala daquele lugar (de 17 a 28 px por metro). Sem contorno, três tons
por material, o olho de um pixel, rostos simples.

Cada conjunto foi construído junto com o móvel (a lição da D): o quadril no assento, o tronco e as pernas para a mesma
atividade, as coxas debaixo do tampo, as mãos nos objetos, os pés no piso quando aparecem. A ordem do desenho segue a
profundidade: quem está atrás de um móvel vem antes dele, o móvel é redesenhado por cima, e as mãos que pousam no tampo
vêm depois (`maos`).

Morel segue a aparência do jogo (retratos.js, MOREL_FIGURA), não a da imagem gerada (sem a capa vermelha, as armas e
as placas de armadura dela)."""
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


def espelho(linhas):
    return [l[::-1] for l in linhas]


# ---------------------------------------------------------------- o taverneiro, de pé atrás do balcão
# P(-4.2, 1.4): os pés em y 64,5, o alto da cabeça em 33, m = 17,5 (corpulento). O balcão o corta na cintura (o tampo
# em y 49-51). O cabelo e a barba grisalhos, a camisa clara de mangas arregaçadas, o avental de couro escuro (a caneca
# e o pano se leem contra ele): seca a caneca com o pano, na altura do peito.
TAVERNEIRO = dict(x=79, y=33, pal=pal(K="#8a867e", k="#6a665e", B="#8a8278", W="#c4bca6", w="#9a927c", A="#5a3e28",
                                      a="#3e2a1a", C="#e2dac6"), grade=[
    "......KKK.....",
    ".....KsssK....",
    ".....seseS....",
    ".....BsSsB....",
    "......BBb.....",
    "......sSs.....",
    "...WWWWWWWw...",
    "..WWAAAAAWWw..",
    "..WWAAAAAWWw..",
    "..Ww.AAAA.Ww..",
    "..WwsCMMmsWw..",
    "..Ww.lCMmmww..",
    "..Ww..AAa..w..",
    "..ww..AAa..w..",
    "......AAa.....",
    "......AAa.....",
])

# ---------------------------------------------------------------- a mesa da frente: três conversando
# A freguesa, no banco do outro lado, na ponta esquerda, P(-5.4, 3.9): o assento em y 72,6, a cabeça em 52, m = 24.
# De três quartos (virada para a direita, para os outros dois); o cabelo preso, o vestido verde com a blusa clara; o
# cotovelo direito no tampo e a mão no queixo, a outra mão na borda da mesa. O tampo a corta em y 68.
FREGUESA = dict(x=25, y=52, pal=pal(K="#6a4428", k="#4a2e18", G="#4e6a44", v="#3a5032", V="#64804f", W="#d6ccb4",
                                    g="#44603c"), grade=[
    ".....KKKK.....",
    "....kKKKKK....",
    "...kKKKssl....",
    "...kKsesSs....",
    "...kKssSs.....",
    "....ksSsll....",
    ".....sSsll....",
    "...vGWWGgG....",
    "..vGGGWGgGV...",
    "..vGGGGGgGV...",
    "..vGvGGGgGV...",
    "..vGvGGGgGV...",
    "..vGvGGGgGV...",
    "..vGvGGGgGV...",
    "..vGvGGGgGV...",
    "..vvvGGGggV...",
])
FREGUESA_MAOS = dict(x=25, y=67, grade=[
    "..vG....gG....",
    "...ss...gg....",
])

# O freguês de costas, no banco da frente, P(-3.6, 5.7): o assento em y 84, a cabeça em 58,6, m = 28 (o maior da sala).
# A cabeça, a nuca, o pescoço e os ombros acima da mesa; os ombros caindo do pescoço, os braços curtos (vão para a
# frente até os cotovelos no tampo, em y 72), a cintura, o cinto e o quadril largo assentado no banco.
COSTAS = dict(x=49, y=59, pal=pal(K="#2e2620", k="#1e1814", H="#463a30", U="#34405a", u="#232c40", V="#485678",
                                  c="#3a2416", C="#6a4a2c"), grade=[
    "........KKKK........",
    ".......KKHKKK.......",
    "......kKKHKKKk......",
    "......kKKKKKKk......",
    "......sKKKKKKs......",
    "......SkKKKKkS......",
    ".......kKKKKk.......",
    "........kkkk........",
    "........sSSs........",
    "......VUUUUUUu......",
    "....VVUUUUUUUUuu....",
    "..VVUUuUUUUUUuUUuu..",
    ".VVUUUuUUUUUUuUUUuu.",
    ".uuUUuuUUUUUUuuUUuu.",
    "...uu.VUUUUUUu.uu...",
    "......VUUUUUUu......",
    "......VUUUUUUu......",
    "......VUUUUUUu......",
    "......VUUUUUUu......",
    "......VUUUUUUu......",
    "......ccccCccc......",
    ".....VUUUUUUUUu.....",
    "....VUUUUUUUUUUu....",
    "....VUUUUUUUUUUu....",
    "...VUUUUUUUUUUUUu...",
    "...uuuuuuuuuuuuuu...",
])

# O homem da cabeceira, na cadeira de espaldar da ponta direita, P(-1.8, 4.7): o assento em y 77, a cabeça em 54, m = 26.
# De três quartos, virado para os outros dois; o colete de couro claro sobre a camisa (separado do balcão escuro); ergue a caneca na mão de cá, o
# antebraço de lá no tampo; as coxas para a frente debaixo da ponta da mesa, as canelas até o piso (y 89).
CABECEIRA = dict(x=99, y=54, pal=pal(K="#6a4428", k="#4a2e18", B="#6a4428", W="#d0c6ac", w="#a49a82", N="#8a6440",
                                     n="#5e4228", P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "..........kKKKk...",
    ".........kKKKKKk..",
    "........ssKKKKKk..",
    "........seKKKKk...",
    ".......sssKKKk....",
    "........sBBBk.....",
    ".........BBB......",
    "..........sS......",
    "........WNNNNn....",
    "......MMWNNNNNn...",
    "......mMsNNNNNn...",
    "......mmWNNNNNn...",
    ".......WWNNNNNn...",
    "........NNNNNNn...",
    "........NNNNNNn...",
    "........NNNNNNn...",
    "........NNNNNNn...",
    "........NNNNNNn...",
    "........nnnnnnn...",
    "........NNNNNNn...",
    "...pPPPPPPPPPPPp..",
    "...pPPPPPPPPPPPp..",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    "..pPP.............",
    ".OOOO.............",
])
CABECEIRA_MAOS = dict(x=99, y=66, grade=[
    "...sWWw...........",
    "..sWw.............",
])

# ---------------------------------------------------------------- a mesa redonda: dois jogando
# O de verde, no banquinho da esquerda, P(1.25, 3.3): o assento em y 69, a cabeça em 49, m = 22. De perfil, virado
# para o tabuleiro, inclinado; o cotovelo no tampo e a mão no queixo (pensa a jogada); a coxa até o joelho debaixo da
# borda, a canela até o piso (y 79).
VERDE = dict(x=181, y=49, pal=pal(K="#3a2a1e", k="#24190f", B="#3a2a1e", N="#4a6a46", n="#33493a", Z="#628a5c",
                                  P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "...kKKKk........",
    "..kKKKKKs.......",
    "..kKKKKes.......",
    "..kKKKssss......",
    "...kKBBss.......",
    "....kBBBl.......",
    ".....sSZls......",
    "...nNNNZZ.......",
    "..nNNNNNZZ......",
    "..nNNNNNNZ......",
    "..nNNNNNNZZ.....",
    "..nNNNNNNNZZ....",
    "..nNNNNNNN.ZZs..",
    "..nNNNNNNN......",
    "..nNNNNNNN......",
    "..nNNNNNNN......",
    "..nnnnnnnn......",
    "..pPPPPPPPPPPp..",
    "..pPPPPPPPPPPPp.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "............pPP.",
    "...........OOOO.",
])
# O de ocre, no banquinho da direita, P(2.75, 3.3): o assento em y 69, a cabeça em 49, m = 22. De três quartos, virado
# para o tabuleiro; estende a mão até a peça (a jogada); a outra mão na borda; as pernas como as do outro, espelhadas.
OCRE = dict(x=213, y=49, pal=pal(K="#7a5228", k="#523416", B="#7a5228", Y="#a88a4e", y="#7a6236", X="#c4a464",
                                 P="#3e3a44", p="#2a2830", O="#1e1812"), grade=[
    "........kKKKk...",
    ".......sKKKKKk..",
    ".......seKKKKk..",
    "......ssssKKKk..",
    ".......ssBBKk...",
    "........BBBk....",
    "........sS......",
    ".......XYYYYy...",
    "......XYYYYYYy..",
    ".....XYYYYYYYy..",
    "....XXYYYYYYYy..",
    "..sXX.YYYYYYYy..",
    "......YYYYYYYy..",
    "......YYYYYYYy..",
    "......YYYYYYYy..",
    "......YYYYYYYy..",
    "......yyyyyyyy..",
    ".pPPPPPPPPPPp...",
    "pPPPPPPPPPPPp...",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "pPP.............",
    "OOOO............",
])

# ---------------------------------------------------------------- junto do fogo: aquece as mãos
# No banquinho à esquerda da boca, P(-1.55, 1.15): o assento em y 56, a cabeça em 42, m = 17. De perfil, virado para o
# fogo, inclinado: os antebraços estendidos, as palmas abertas; as coxas e as canelas até o piso (y 62,6).
JUNTO_FOGO = dict(x=128, y=42, pal=pal(H="#4a5a44", h="#33402f", J="#5e7058", P="#3e3630", O="#2a1e16",
                                       K="#9a968e"), grade=[
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

# ---------------------------------------------------------------- Morel, na cadeira de espaldar
# P(5.25, 3.6): o assento em y 70, a cabeça em 47, m = 23, desenhado um pouco acima (o porte grande). Na cadeira robusta,
# as costas no espaldar (à esquerda dele), o quadril no assento, as coxas para a frente debaixo da borda da mesa, as
# botas no piso (y 81); inclinado para a tigela, a colher na mão de cá. A aparência do jogo: o cabelo e a barba
# castanhos, o traço claro da cicatriz, a ombreira cinza, a pele no outro ombro, o couro com o vermelho no peito.
MOREL = dict(x=270, y=47, pal=pal(C="#6a4a2c", c="#4e3420", P="#c09070", p="#9a6c52", x="#e0b8a0", b="#5a3e2a",
                                  B="#3e2a1c", S="#9a9ca4", T="#6e7078", L="#7a5838", l="#54391f", R="#a03a2c",
                                  F="#7a7064", f="#56504a", Q="#3e3a36", q="#2a2622", O="#2a1e16", w="#c4c7cc"), grade=[
    ".........cCCCCc.........",
    "........cCCCCCCc........",
    "........cCCCPxPP........",
    ".........CCxPPeP........",
    ".........cCxPPPPP.......",
    ".........cbBPPPPb.......",
    "..........bBBBBb........",
    "...........bBBb.........",
    ".......SSSLRRLFFF.......",
    "......STSSLRRLLFFf......",
    "......STSLLRRLLLFf......",
    "......STLLLRRLLLLlL.....",
    "......lLLLLRRLLLLlLl....",
    "......lLLLLRRLLLL.lLl...",
    "......lLLLLRRLLLL...lPw.",
    "......lLLLLRRLLLL....P..",
    "......lLLLLRRLLLL.......",
    "......lLLLLLLLLLL.......",
    "......lLLLLLLLLLL.......",
    "......lccccccccc........",
    "......qQQQQQQQQQQQ......",
    ".......qQQQQQQQQQQQQ....",
    ".......qQQQQQQQQQQqQ....",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "....................qQ..",
    "...................qOOOO",
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
    D.mesas(px, parte="balcao_banquinhos")
    if not D.SEM_RODA:                                       # a prova de qualidade desenha os jogadores à parte
        figura(px, VERDE, "jogador de verde")
        figura(px, OCRE, "jogador de ocre")
        D.mesas(px, parte="roda_mesa")
        maos(px, VERDE, dict(x=181, y=60, grade=["..........ZZs..."]), "verde (mão)")
        maos(px, OCRE, dict(x=213, y=59, grade=["..sXX..........."]), "ocre (mão)")
    if morel and not D.SEM_CANTO:                            # a prova (../prova/m1) desenha Morel à parte
        figura(px, MOREL, "Morel")
        maos(px, MOREL, dict(x=270, y=61, grade=["....................lPw.", ".....................P.."]),
             "Morel (mão)")
    figura(px, FREGUESA, "freguesa")
    D.mesas(px, parte="longa_mesa")
    maos(px, FREGUESA, FREGUESA_MAOS, "freguesa (mãos)")
    figura(px, CABECEIRA, "cabeceira")
    maos(px, CABECEIRA, CABECEIRA_MAOS, "cabeceira (mãos)")
    D.mesas(px, parte="longa_perto")
    figura(px, COSTAS, "freguês de costas")
