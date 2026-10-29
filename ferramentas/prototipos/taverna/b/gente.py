"""Quem está na taverna, candidata B (estudo estático): cada pessoa desenhada à mão numa grade, na escala da distância
em que está (desenho.m), sem contorno, três tons por material, o olho de um pixel e as mãos simples.

Por que à mão: na A, as figuras saíam de uma fórmula (um tronco de largura fixa e uma cabeça de perfil) e ficaram todas
estreitas, parecidas e de perfil. Aqui cada uma tem silhueta e porte próprios e um ângulo: de frente, de três quartos,
de costas, de perfil. As medidas vêm da régua: a cabeça ~0,24 m, os ombros 0,40 a 0,50 m, quem senta tem o quadril no
assento e os pés no piso (ou escondidos pelo tampo ou pela borda do quadro).

A ordem do desenho decide quem está na frente: quem está atrás de um móvel é desenhado antes dele, e o móvel é
redesenhado por cima; as mãos que pousam no tampo vêm depois (`maos`). Estudo estático: uma pose de atividade por
pessoa; a animação vem depois de a construção ser aprovada (os ciclos da A ficam no histórico)."""
from . import desenho as D

# as letras comuns: s a pele, S a sombra dela, l a luz; e o olho; K e k o cabelo; B e b a barba
PELE = {"s": "#c99a78", "S": "#9a6e52", "l": "#e0b494", "e": "#24170f"}


def pal(**cores):
    return {**PELE, **cores}


def grade_valida(nome, linhas):
    larg = len(linhas[0])
    for i, l in enumerate(linhas):
        assert len(l) == larg, f"{nome}: a linha {i} tem {len(l)} colunas, não {larg}"
    return linhas


# ---------------------------------------------------------------- o taverneiro, de frente, atrás do balcão
# Corpulento, careca, a barba escura; a camisa de ardósia com as mangas arregaçadas e o avental de linho; limpa uma
# caneca com o pano, as mãos na altura do peito, acima do tampo (1,05 m). A escala: m(61) = 17 px/m.
TAVERNEIRO = dict(x=74, y=31, pal=pal(K="#3a2a20", B="#4a3226", b="#33231a", R="#454552", r="#32323c", Q="#5a5a68",
                                      A="#b4aa90", a="#8c826c", M="#a8abb2", m="#6e7178", W="#e2dac6"), grade=[
    ".....lss.....",
    "....lsssS....",
    "....KeseK....",
    "....ssSsS....",
    "....BBBBB....",
    ".....BBb.....",
    "..QRRRBRRRr..",
    ".QRRAAAAARRr.",
    ".QR.AAAAa.Rr.",
    ".QR.MMWAa.Rr.",
    ".sssMmWWsss..",
])

# ---------------------------------------------------------------- a freguesa da mesa da frente, de três quartos
# Do outro lado da mesa comprida, virada para quem está de costas (para a direita): o lenço de linho, o vestido verde
# com a blusa clara no decote; o braço de perto no tampo com a caneca, o outro na tábua do pão. m(94) = 33 px/m.
FREGUESA = dict(x=141, y=50, pal=pal(K="#5a3a22", L="#c8bea4", g="#8e866e", G="#4e6a44", v="#3a5032", V="#64804f",
                                     W="#d6ccb4"), grade=[
    ".....gLLLL......",
    "....gLLLLLL.....",
    "...gLLKKKKLL....",
    "...gLKslsss.....",
    "...gLKesses.....",
    "...gLssSssl.....",
    "....gLSsss......",
    ".....LSss.......",
    "......Ss........",
    "...vGGWWWGGGV...",
    "..vGGGGWGGGGGV..",
    "..vGGGGGGGGGGV..",
    "..vGvGGGGGGvGV..",
    "..vGvGGGGGGvGGV.",
    "..vGvGGGGGGvGGV.",
    "..vGvGGGGGGvGGV.",
    "..vGvGGGGGGvGGV.",
    "..vvvGGGGGGvvvV.",
])
# as mãos no tampo, por cima da mesa: a de perto na caneca, a outra no pão
FREGUESA_MAOS = dict(x=141, y=66, grade=[
    "..vGG.......GGV.",
    "...ss........ss.",
])

# ---------------------------------------------------------------- o freguês de costas, na beira da mesa da frente
# O maior da cena (m(104) = 38 px/m): a nuca e o cabelo castanho preso, as orelhas, o casaco de lã azul-acinzentado
# com a costura das mangas, os cotovelos abertos no tampo; o cinto e a aba do casaco no banco (cortado pela borda).
FREGUES_COSTAS = dict(x=171, y=54, pal=pal(K="#4a3020", k="#33200f", U="#3e4a5e", u="#2b3343", V="#52607a",
                                           c="#3a2416", C="#6a4a2c"), grade=[
    ".........KKKK.........",
    "........KKKKKK........",
    ".......kKKKKKKk.......",
    ".......kKKKKKKk.......",
    ".......skKKKKks.......",
    ".......SkKKKKkS.......",
    "........kKKKKk........",
    ".........kkkk.........",
    ".........sSSs.........",
    "......VUUUUUUUUu......",
    "....VVUUUUUUUUUUuu....",
    "...VVUUUUUUUUUUUUuu...",
    "..VVUUuUUUUUUUUuUUuu..",
    "..VVUUuUUUUUUUUuUUuu..",
    ".VVUUUuUUUUUUUUuUUUuu.",
    ".VVUUUuUUUUUUUUuUUUuu.",
    "VVUUUuUUUUUUUUUUuUUUuu",
    "VVUUUuUUUUUUUUUUuUUUuu",
    "VUUUUuUUUUUUUUUUuUUUUu",
    "uuuuuuUUUUUUUUUUuuuuuu",
    "......UUUUUUUUUU......",
    "......UUUUUUUUUu......",
    "......VUUUUUUUUu......",
    "......VUUUUUUUUu......",
    "......VUUUUUUUUu......",
    "......cccccCcccc......",
    "......VUUUUUUUUu......",
    ".....VUUUUUUUUUUu.....",
    ".....VUUUUUUUUUUu.....",
    ".....VUUUUUUUUUUu.....",
    "....VUUUUUUUUUUUUu....",
    "....uuuuuuuuuuuuuu....",
])


# ---------------------------------------------------------------- o freguês de pé no balcão, de perfil
# Encostado na frente do balcão, virado para o taverneiro (para a direita), a caneca na altura do peito; a túnica cor
# de vinho, o cinto, as calças e as botas, as pernas um pouco abertas. De pé: 1,72 m em m(69) = 21 px/m.
FREGUES_BALCAO = dict(x=46, y=33, pal=pal(K="#6a4428", k="#4a2e18", B="#6a4428", R="#6e2e2a", r="#4e1e1c",
                                          Q="#8a3e36", c="#2a1c12", P="#4e4a44", p="#36332f", O="#2e2018",
                                          M="#a8abb2", m="#6e7178"), grade=[
    "...kKKK.....",
    "..kKKKKs....",
    "..kKKsse....",
    "..kKsssss...",
    "...kSsss....",
    "...kBBS.....",
    "....sS......",
    "...rRRRQ....",
    "..rRRRRRQ...",
    "..rRRRrRQ...",
    "..rRRRrRRQ..",
    "..rRRRrRRsMM",
    "..rRRRRRRsMm",
    "..rRRRRRQ.mm",
    "..rRRRRRQ...",
    "..rRRRRRQ...",
    "..ccccccc...",
    "..pPPPPPP...",
    "..pPPPpPP...",
    "..pPPPpPP...",
    "..pPP.pPP...",
    "..pPP.pPP...",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..pPP..pPP..",
    "..OOO..OOO..",
    ".OOOO..OOOO.",
])

# ---------------------------------------------------------------- a mesa redonda do meio: dois homens conversando
# Atrás da mesa, de três quartos (virado para o outro): o cabelo preto, o casaco ocre, a mão na caneca. m(67) = 20.
MEIO_ATRAS = dict(x=234, y=40, pal=pal(K="#2a2420", k="#1a1612", B="#2a2420", Y="#86683a", y="#5e4826",
                                       X="#a07e48", M="#a8abb2", m="#6e7178"), grade=[
    "...kKKK....",
    "..kKKKKK...",
    "..kKslss...",
    "..kseSse...",
    "..kssSss...",
    "...BBss....",
    "....sS.....",
    "..yYYYYYX..",
    ".yYYYYYYYX.",
    ".yYYyYYYYX.",
    ".yYYyYYYYX.",
    ".yYYyYYYYX.",
    ".yYYyYYYYX.",
    ".yYYyYYYYX.",
])
MEIO_ATRAS_MAOS = dict(x=234, y=53, grade=[
    ".....yYsMM.",
    "........mm.",
])
# Do lado direito, de perfil (virado para a esquerda): um velho de barba grisalha, o casaco verde-escuro, o antebraço
# no tampo com a caneca; sentado no banquinho, a coxa para a frente, a canela até o piso. m(72) = 22.
MEIO_LADO = dict(x=245, y=42, pal=pal(K="#8a867e", k="#646058", B="#a8a49a", N="#34483e", n="#24332b", Z="#465e50",
                                      P="#4a4038", p="#332c26", O="#2a1e16", T="#8c6238", t="#47301c",
                                      M="#a8abb2", m="#6e7178"), grade=[
    "........kKKK..",
    ".......kKKKKk.",
    "......seKKKKk.",
    ".....sssKKKk..",
    "......sSsKk...",
    "......BBBk....",
    ".......BBS....",
    "........ZNNn..",
    ".......ZNNNNn.",
    ".......ZNNNNn.",
    "......ZNNNNNn.",
    ".....ZNNNNNNn.",
    "...ZZNNnNNNNn.",
    "..MsZNNnNNNNn.",
    "..mm..NNNNNNn.",
    "......NNNNNNn.",
    "......NNNNNNn.",
    "......NNNNNNn.",
    "......NNNNNNn.",
    "....pPPPPPPPp.",
    "...pPPPPPPPPp.",
    "...pPP.TTTTTT.",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "...pPP..t..t..",
    "..OOOO..t..t..",
])

# ---------------------------------------------------------------- junto do fogo, de perfil: aquece as mãos
# Um velho de capuz e capa pardos, no banquinho à direita da lareira, as mãos estendidas para o fogo. m(53) = 13.
JUNTO_FOGO = dict(x=187, y=35, pal=pal(H="#6a5e4c", h="#4a4034", J="#7e7260", P="#3e3630", O="#2a1e16",
                                       T="#8c6238", t="#47301c"), grade=[
    "......JHH.",
    ".....JHHHh",
    ".....sHHHh",
    "......HHHh",
    ".....JHHHh",
    "....JHHHHh",
    ".lsJHHHHHh",
    "...JHHHHHh",
    "....JHHHHh",
    "....JHHHHh",
    "....hHHHHh",
    "...PPPPhhh",
    "..PPPTTTT.",
    "..PP..t.t.",
    "..PP..t.t.",
    "..PP..t.t.",
    "..PP..t.t.",
    ".OOO..t.t.",
])

# ---------------------------------------------------------------- Morel, no canto debaixo da galeria
# A aparência estabelecida (retratos.js, MOREL_FIGURA), na escala do fundo (m(50) = 12) e um pouco acima dela ("um
# homem grande", eventos/comitiva.py): o cabelo e a barba castanhos, a cicatriz clara descendo pelo rosto, a ombreira
# cinza num ombro e a pele no outro, o couro com o vermelho no peito. Come sozinho, de costas para a parede, a cabeça
# baixa no prato.
MOREL = dict(x=283, y=33, pal=pal(C="#6a4a2c", c="#4e3420", P="#c09070", p="#9a6c52", x="#e0b8a0", b="#5a3e2a",
                                  B="#3e2a1c", S="#9a9ca4", T="#6e7078", L="#6a4a30", l="#4a3220", R="#8a3428",
                                  F="#6a6058", f="#4e4640", w="#8a5a30", W="#5a3018"), grade=[
    "...cCCCCc....",
    "..cCCPPCCc...",
    "..CPxPPePc...",
    "..cPPxPPpc...",
    "...bBPpBb....",
    "....bBBb.....",
    ".SSSLRRLFFF..",
    "SSSTLRRLLFFf.",
    "STTLLRRLLLFf.",
    ".lLLLRRLLLl..",
    ".lLLLRRLLLl..",
])
MOREL_MAOS = dict(x=283, y=43, grade=[
    ".lPL.....LPl.",
    "...wWWWWw....",
])


# ---------------------------------------------------------------- o desenho, na ordem da profundidade
def figura(px, f, nome):
    px.grade(f["x"], f["y"], grade_valida(nome, f["grade"]), f["pal"])


def maos(px, f, m_, nome):
    px.grade(m_["x"], m_["y"], grade_valida(nome, m_["grade"]), f["pal"])


def desenhar(px, r, morel=True):
    """As pessoas por cima da sala (desenho.sala), de trás para a frente, com os móveis que ficam na frente delas
    redesenhados por cima e as mãos que pousam nos tampos depois deles."""
    if morel:
        figura(px, MOREL, "Morel")
        D.mesa_canto(px)
        maos(px, MOREL, MOREL_MAOS, "Morel (mãos)")
    figura(px, JUNTO_FOGO, "junto do fogo")
    figura(px, MEIO_ATRAS, "meio, atrás")
    D.mesa_meio(px)
    maos(px, MEIO_ATRAS, MEIO_ATRAS_MAOS, "meio, atrás (mãos)")
    figura(px, MEIO_LADO, "meio, de lado")
    figura(px, TAVERNEIRO, "taverneiro")
    D.balcao(px)
    figura(px, FREGUES_BALCAO, "freguês do balcão")
    figura(px, FREGUESA, "freguesa")
    D.mesa_frente(px)
    maos(px, FREGUESA, FREGUESA_MAOS, "freguesa (mãos)")
    D.banco(px, 158, 214, 104)
    figura(px, FREGUES_COSTAS, "freguês de costas")
