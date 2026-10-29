"""Quem está na taverna, candidata C (estudo estático): cada pessoa desenhada à mão numa grade, na escala do lugar em
que está (desenho.m), sem contorno, três tons por material, o olho de um pixel e as mãos simples.

O que mudou da B: a profundidade contida trouxe o taverneiro e Morel para a faixa do meio (cabeças de 6 px, não de 3 ou
4); cada corpo tem porte próprio, e a construção separa cabeça, pescoço, tronco, braços e mãos (o pescoço em pele
entre a cabeça e a gola, o braço separado do tronco por uma costura ou um vão, a mão em pele no fim do antebraço). Quem
senta tem o quadril no assento, as coxas para a frente e as canelas até o piso, ou escondidas pelo tampo.

Os grupos: na mesa comprida da esquerda, três (a freguesa de três quartos do outro lado, o freguês de costas no banco
da frente, o homem de colete de perfil na ponta); na redonda, dois jogando (um de três quartos, um de perfil), com a
cadeira vazia; o velho junto do fogo; Morel no canto, no banco de espaldar.

A ordem do desenho decide quem está na frente: quem está atrás de um móvel é desenhado antes dele, e o móvel é
redesenhado por cima; as mãos que pousam no tampo vêm depois (`maos`)."""
from . import desenho as D

PELE = {"s": "#c99a78", "S": "#9a6e52", "l": "#e0b494", "e": "#24170f"}
CANECA = {"M": "#a8abb2", "m": "#6e7178"}


def pal(**cores):
    return {**PELE, **CANECA, **cores}


def grade_valida(nome, linhas):
    larg = len(linhas[0])
    for i, l in enumerate(linhas):
        assert len(l) == larg, f"{nome}: a linha {i} tem {len(l)} colunas, não {larg}"
    return linhas


# ---------------------------------------------------------------- o taverneiro, de frente, atrás do balcão
# Corpulento, careca, a barba escura; a camisa de ardósia de mangas arregaçadas e o avental de linho; seca uma caneca
# com o pano em cima do tampo (a área de trabalho). m(71) = 19 px/m: a cabeça de 6, os ombros de 11.
TAVERNEIRO = dict(x=67, y=37, pal=pal(B="#4a3226", b="#33231a", R="#454552", r="#32323c", Q="#5a5a68",
                                      A="#b4aa90", a="#8c826c", W="#e2dac6"), grade=[
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
    "..QR.AAAAa.Rr..",
    "..Qr.AAAAa.rr..",
])
TAVERNEIRO_MAOS = dict(x=67, y=49, grade=[
    "...sS.MMW..Ss..",
    "....l.MmWW.l...",
    "......mm.......",
])

# ---------------------------------------------------------------- a mesa comprida da esquerda: três
# A freguesa, do outro lado, de três quartos (virada para a direita, para quem fala): o lenço de linho, o vestido
# verde com a blusa clara no decote, as duas mãos em volta da caneca. m(79) = 23: a cabeça de 6, os ombros de 10.
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

# O homem de colete, na ponta da direita, de perfil (virado para a esquerda): a barba ruiva, a camisa clara, o colete
# de couro; sentado na cadeira, a coxa para a frente debaixo da mesa, a canela até o piso; a mão na caneca. m(89) = 27.
PONTA = dict(x=94, y=53, pal=pal(K="#7a3e1e", k="#52280f", B="#8a4a24", W="#b8ae96", w="#8e866e", N="#5a3e2a",
                                 n="#3e2a1c", P="#4a4038", p="#332c26", O="#2a1e16"), grade=[
    "..........kKKK..",
    ".........kKKKKKk",
    "........ssKKKKKk",
    "........seKKKKk.",
    ".......sssSKKk..",
    "........ssSKk...",
    "........BBBk....",
    ".........sS.....",
    "........WNNNNn..",
    ".......WWNNNNNn.",
    ".......WwNNNNNn.",
    "......WWwNNNNNn.",
    "......WwwNNNNNn.",
    ".......wwNNNNNn.",
    "........NNNNNNn.",
    "........NNNNNNn.",
    "........NNNNNNn.",
    "........NNNNNNn.",
    "........NNNNNNn.",
    "........NNNNNNn.",
    "........nnnnnnn.",
    "....pPPPPPPPPPp.",
    "...pPPPPPPPPPPp.",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "...pPP..........",
    "..OOOO..........",
])
PONTA_MAOS = dict(x=94, y=64, grade=[
    "..MWWWw.........",
    ".mMsww..........",
    ".mm.............",
])

# O freguês de costas, no banco da frente (m(103) = 34: o maior da cena): o cabelo castanho preso, as orelhas, a nuca,
# o casaco de lã azul-acinzentado com a costura das mangas e a do meio das costas, os cotovelos abertos no tampo; a
# cintura, o cinto e a aba do casaco no banco (cortado pela borda).
COSTAS = dict(x=50, y=58, pal=pal(K="#4a3020", k="#33200f", H="#6a4a30", U="#3e4a5e", u="#2b3343", V="#52607a",
                                  c="#3a2416", C="#6a4a2c"), grade=[
    "........KKKK........",
    ".......KKHKKK.......",
    "......kKKHKKKk......",
    "......kKKKKKKk......",
    "......skKKKKks......",
    "......SkKKKKkS......",
    ".......kKKKKk.......",
    "........kkkk........",
    "........sSSs........",
    ".....VVUUUUUUu......",
    "...VVUUUUUUUUUUu....",
    "..VVUUUUUUUUUUUUu...",
    ".VVUUuUUUUuUUUuUUu..",
    ".VUUUuUUUUuUUUuUUuu.",
    "VVUUUuUUUUuUUUuUUUu.",
    "VUUUUuUUUUuUUUuUUUuu",
    "uuuuuuUUUUuUUUuuuuuu",
    ".....uUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....VUUUUuUUUu.....",
    ".....ccccCcccc......",
    "....VUUUUUuUUUu.....",
    "....VUUUUUuUUUuu....",
    "...VUUUUUUuUUUUu....",
    "...VUUUUUUuUUUUu....",
    "...uuuuuuuuuuuuu....",
])

# ---------------------------------------------------------------- a mesa redonda: dois jogando
# Atrás da mesa, de três quartos (virado para a esquerda, para o outro): o cabelo preto, o casaco ocre; a mão no
# tabuleiro. m(73) = 20: a cabeça de 5.
RODA_ATRAS = dict(x=231, y=46, pal=pal(K="#2a2420", k="#1a1612", B="#2a2420", Y="#86683a", y="#5e4826",
                                       X="#a07e48"), grade=[
    "....KKKk...",
    "...KKKKKk..",
    "...lsKKKk..",
    "...esSKKk..",
    "..sssSKk...",
    "...ssBk....",
    "....sS.....",
    "..XYYYYYy..",
    ".XYYYYYYYy.",
    ".XYyYYYYYy.",
    ".XYyYYYYYy.",
    ".XYyYYYYYy.",
])
RODA_ATRAS_MAOS = dict(x=231, y=58, grade=[
    ".XYs.......",
    "..s........",
])
# Do lado esquerdo, de perfil (virado para a direita, para o tabuleiro): um velho de barba grisalha, o casaco
# verde-escuro, a mão estendida sobre o tampo; no banquinho, a coxa para a frente, a canela até o piso. m(79) = 23.
RODA_LADO = dict(x=207, y=49, pal=pal(K="#8a867e", k="#646058", B="#a8a49a", N="#34483e", n="#24332b", Z="#465e50",
                                      P="#4a4038", p="#332c26", O="#2a1e16", T="#8c6238", t="#47301c"), grade=[
    ".kKKK.........",
    "kKKKKs........",
    "kKKKKes.......",
    "kKKKssss......",
    ".kKSsss.......",
    "..kBBB........",
    "...SBB........",
    "..nNNNZ.......",
    ".nNNNNNZ......",
    ".nNNNNNZ......",
    ".nNNNNNNZ.....",
    ".nNNNNnNNZZ...",
    ".nNNNNnNNZZs..",
    ".nNNNNNNN.....",
    ".nNNNNNN......",
    ".nNNNNNN......",
    ".nNNNNNN......",
    ".nNNNNNN......",
    ".nNNNNNN......",
    ".pPPPPPPPPPp..",
    ".pPPPPPPPPPPp.",
    ".TTTTTT..pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t...pPP..",
    "..t..t..OOOO..",
])

# ---------------------------------------------------------------- junto do fogo, de perfil: aquece as mãos
# Um velho de capuz e capa pardos, no banquinho à direita da lareira, as mãos estendidas para o fogo. m(63) = 16.
JUNTO_FOGO = dict(x=184, y=41, pal=pal(H="#6a5e4c", h="#4a4034", J="#7e7260", P="#3e3630", O="#2a1e16",
                                       T="#8c6238", t="#47301c"), grade=[
    "......JHHH.",
    ".....JHHHHh",
    ".....sHHHHh",
    "....ssHHHHh",
    ".....sHHHh.",
    "....JHHHHh.",
    "..lsJHHHHHh",
    "...JJHHHHHh",
    ".....JHHHHh",
    ".....JHHHHh",
    ".....hHHHHh",
    "....PPPPhhh",
    "...PPPTTTT.",
    "...PP..t.t.",
    "...PP..t.t.",
    "...PP..t.t.",
    "...PP..t.t.",
    "...PP..t.t.",
    "..OOO..t.t.",
    "...........",
    "...........",
    "...........",
])

# ---------------------------------------------------------------- Morel, no canto
# A aparência estabelecida (retratos.js, MOREL_FIGURA), na escala do canto (m(74) = 20) e um pouco acima dela ("um
# homem grande", eventos/comitiva.py): o cabelo e a barba castanhos, a cicatriz clara descendo pelo rosto, a ombreira
# cinza no ombro da frente e a pele no de trás, o couro com o vermelho no peito. No banco de espaldar, de três quartos
# para a mesa (para a esquerda), come o ensopado sem levantar os olhos: a colher na mão, a outra na beira da tigela.
MOREL = dict(x=290, y=43, pal=pal(C="#6a4a2c", c="#4e3420", P="#c09070", p="#9a6c52", x="#e0b8a0", b="#5a3e2a",
                                  B="#3e2a1c", S="#9a9ca4", T="#6e7078", L="#6a4a30", l="#4a3220", R="#8a3428",
                                  F="#6a6058", f="#4e4640", Q="#3e3a36", q="#2a2622", O="#2a1e16"), grade=[
    ".........cCCCc..",
    "........cCCCCCc.",
    ".......PxPCCCCc.",
    "......PePxCCCc..",
    ".....PPPPpxCc...",
    "......PPPpCc....",
    "......bBBBb.....",
    ".......bBb......",
    ".....SSSLRRLFF..",
    "....STSSLRRLLFF.",
    "....STTLLRRLLLFf",
    "....lSLLLRRLLLFf",
    "...LLlLLLRRLLLl.",
    "..LLl.LLLRRLLLl.",
    "......LLLRRLLLl.",
    "......LLLRRLLLl.",
    "......lLLRRLLLl.",
    "......lLLLLLLLl.",
    "......lqqqqqqqq.",
    "..QQQQQQQQQQQQq.",
    ".QQQQQQQQQQQQq..",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    ".Qq.............",
    "OOO.............",
])
MOREL_MAOS = dict(x=284, y=55, grade=[
    "....lPL.........",
    "BwWWWw..........",
    ".BBBB...........",
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
        maos(px, MOREL, MOREL_MAOS, "Morel (mãos)")
    figura(px, RODA_ATRAS, "roda, atrás")
    D.mesa_meio(px)
    maos(px, RODA_ATRAS, RODA_ATRAS_MAOS, "roda, atrás (mãos)")
    figura(px, RODA_LADO, "roda, de lado")
    figura(px, TAVERNEIRO, "taverneiro")
    D.balcao(px)
    maos(px, TAVERNEIRO, TAVERNEIRO_MAOS, "taverneiro (mãos)")
    figura(px, FREGUESA, "freguesa")
    figura(px, PONTA, "ponta")
    D.mesa_frente(px)
    maos(px, FREGUESA, FREGUESA_MAOS, "freguesa (mãos)")
    maos(px, PONTA, PONTA_MAOS, "ponta (mãos)")
    D.banco(px, 34, 92, 104)
    figura(px, COSTAS, "freguês de costas")
