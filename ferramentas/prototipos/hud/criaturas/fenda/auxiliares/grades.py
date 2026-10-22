"""O Cão infernal e a Cria do Vazio (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do Bestiário
são o 16 ×2 e ×3. Desenhadas à mão, uma letra por pixel; silhueta e volumes primeiro, a brasa e a Fenda depois.
  O Cão infernal ("Cães de brasa com dentes de obsidiana. O fogo é a casa deles."; demonio e fera; a Mordida
  Sangrenta e a Bola de Fogo): o corpo de carvão quente, com a luz nos planos de cima, as rachaduras de brasa seguindo
  os volumes, a boca acesa por dentro e os dentes negros de obsidiana, com um brilho frio, contra ela.
      A, o que rosna de perfil: a cabeça para a esquerda, a orelha deitada para trás, o focinho comprido com o nariz
          na ponta, a mandíbula aberta com as presas negras em cima e embaixo, a rachadura do olho descendo pela
          mandíbula e outra pelo pescoço;
      B, o mastim de cabeça baixa: de frente, as orelhas curtas para fora, o sobrolho escuro sobre os dois olhos
          acesos, o focinho com o nariz, o rosnado largo com as presas negras nos cantos, a rachadura no meio da
          testa e as brasas no pelo dos ombros.
  A Cria do Vazio ("Pedaços da Fenda que aprenderam a andar. Quanto mais perto dela, mais delas."; corrompido e
  etéreo; a Esfera Sombria e o Toque Drenante; a mesma família quando o antagonista a invoca): o miolo escuro do
  Vazio, o violeta nas bordas, o magenta da Fenda (a cor das visões do Vazio na narração).
      A, o caco da Fenda: um pedaço anguloso e irregular, como vidro escuro quebrado, atravessado de cima a baixo por
          uma rachadura acesa em zigue-zague (a Fenda dentro dela, não um olho), com dois braços e duas pernas de caco;
      B, a fera que anda: magra, de perfil para a esquerda, a cabeça baixa com um olho pequeno e a bocarra em fenda
          acesa, o dorso se desfazendo em fiapos e um buraco de vazio no flanco, as garras acesas.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "cao": {
        "k": "1c1210", "c": "563830", "C": "8a5c46", "d": "34221c",  # o carvão (o escuro, o corpo, a luz, a sombra)
        "r": "9a3416", "o": "d8501a", "O": "ff9a2a", "y": "ffe07a",  # a brasa (funda, viva, a boca, o mais quente)
        "t": "120e18", "T": "6a6488", "e": "ffd040",  # a obsidiana dos dentes e o brilho frio dela; o olho
    },
    "cria": {
        "v": "0e0a16", "V": "2a1e40", "u": "5a4488",  # o Vazio (o miolo, o corpo, a borda)
        "m": "a83a98", "M": "e070d0", "w": "f4e4ff",  # a Fenda (funda, acesa, o mais claro)
        "p": "46356e",  # o plano de luz dos cacos (a A2)
    },
    "cao_t": {  # medidas na referência "Cão infernal em pixel art.png" (o carvão, o couro marrom da luz, a brasa)
        "k": "120c0c", "c": "342628", "C": "4a3836", "b": "5e3424", "B": "8a5236", "L": "b4744a",
        "n": "2c2830", "N": "8a8494",  # o nariz (o negro clareado para não sumir na caixa escura; o brilho)
        "r": "7a1a0a", "o": "d8501a", "O": "ff9a2a", "y": "ffe07a",  # a brasa funda (a gengiva, a orelha), viva, a goela
        "t": "120e18", "T": "6a6488", "e": "ffb030",  # a obsidiana das presas e o reflexo dela; o olho
    },
    "cao_n": {  # a terceira: os valores primeiro (a luz nos planos de cima, o escuro nas sombras e no pescoço)
        "k": "1a1214", "d": "2a1e20", "c": "4a3834", "C": "7a5e52", "H": "b08a6e",  # o carvão (do fundo à luz)
        "n": "1a161c", "N": "8e8898",  # o nariz e o brilho dele
        "r": "8a2010", "O": "ff8a2a", "y": "ffd060", "o": "d8501a",  # a gengiva, a goela acesa, a brasa do pescoço
        "t": "16121c", "T": "7a7894", "e": "ffc040",  # a obsidiana das presas e o reflexo; o olho
    },}
PALETAS["cao_n2"] = {**PALETAS["cao_n"], "n": "3a3440"}  # a do N com o nariz num cinza escuro que aparece na caixa
# a da RA2: a cavidade quase negra e o vermelho escuro do fundo dela; a obsidiana da presa um pouco acima da cavidade
PALETAS["cao_ra2"] = {**PALETAS["cao_n2"], "v": "0c0809", "m": "4a120c", "t": "24202c"}
# a da RA3: a obsidiana dos dentes em cinza, com a face iluminada (o quase negro da RA2 sumia na cavidade)
PALETAS["cao_ra3"] = {**PALETAS["cao_ra2"], "g": "a8a4b8", "s": "54505f"}

CAO_A = [
    ".........kk.....",
    "........kCCk....",
    ".......kcCck....",
    "......kcCCcck...",
    "....kkCCCCccck..",
    "..kkCCCCeoCccck.",
    "kkCCCCCccccrccck",
    "kcccccccdcccocck",
    ".TOtOtOdrccoccck",
    ".OyyyyyOdcocccck",
    "..tOtOtcccoccccc",
    "...kcccccoccoccc",
    "....kkccccccoccc",
    "......kcCcccccoc",
    ".....kcCccccccoc",
    "....kcCccccccocc",
]
CAO_B = [
    "................",
    "..k..........k..",
    "..kCk......kCk..",
    "..kcCk....kCck..",
    "...kcCkkkkCck...",
    "..kcCCCoCCCcck..",
    ".kcddcCooCcddck.",
    ".kceedcCCcdeeck.",
    ".kcccdcCCcdccck.",
    "..kccdcCCcdcck..",
    "..kcrcckkccrck..",
    "..kctOyyyyOtck..",
    "..kcTtOyyOtTck..",
    "..kkckttttkckk..",
    ".kcoCcckkccCock.",
    "kcCcoccccccocCck",
]
CRIA_A = [
    "......V.........",
    ".....VuV....V...",
    "....VvuuV..VuV..",
    "...VvvmuuVVvuV..",
    "...VvvvMuuuvvuV.",
    "..VvvvvMMuuvvvuV",
    ".VvvvvvvwMuvvvuV",
    ".VvvvvvwMvvvvuV.",
    "VvvvvvMwvvvvvuV.",
    "VVvvvvMvvvvvuuV.",
    ".VVvvvmMvvvuuV..",
    "..VVvvvmvvuuVV..",
    "...VVvvVvvuVuV..",
    "....Vu.VvuV.Vu..",
    "...Vu...Vu...Vu.",
    "..Vu....Vu....V.",
]
CRIA_B = [  # a primeira, de pernas finas e cabeça menor, virava um emaranhado de traços na carta: ficou mais encorpada
    "................",
    "................",
    "...........u..m.",
    "..uuuu....uVu.u.",
    ".uVVVVu..uVVVVu.",
    "uVVMVVVuuVVVVVVu",
    "uVVVVVVVVVmvmVVu",
    "vMmMmMVVVmvvvmVu",
    "vvvvvvuVVVmvmVVu",
    ".uvvvuVVVVVVVVu.",
    "..uu.uVVuuuVVVu.",
    "....uVVu..uVVu..",
    "...uVVu...uVVu..",
    "..uVVu....uVu...",
    ".uVVu.....uVu...",
    ".MMM.....MMM....",
]

# A segunda passada (pedido do Jean; propostas, nada no jogo). As A e B anteriores ficam como estavam.
# A2, a Cria A com volume nos cacos: a silhueta, os fragmentos, a fissura e a paleta da A; cada caco ganha um plano de luz
# (`p`) junto da borda de fora, o da esquerda em cima e o da direita no meio, e o escuro fundo fica junto da fissura,
# como a profundidade da abertura entre eles. Num plano mais escuro (34284f) a diferença quase não aparecia na carta.
CRIA_A2 = [
    "......V.........",
    ".....VuV....V...",
    "....VpuuV..VuV..",
    "...VppmuuVVvuV..",
    "...VppvMuuuvvuV.",
    "..VpppvMMuuvpvuV",
    ".VppvvvvwMuppvuV",
    ".VpvvvvwMvppvuV.",
    "VvpvvvMwvvppvuV.",
    "VVpvvvMvvvpvuuV.",
    ".VVpvvmMvvvuuV..",
    "..VVvvvmvvuuVV..",
    "...VVvvVvvuVuV..",
    "....Vu.VvuV.Vu..",
    "...Vu...Vu...Vu.",
    "..Vu....Vu....V.",
]
# T, o Cão infernal pela referência gerada "Cão infernal em pixel art.png" (ferramentas/arte/referencias/icones/), a
# principal desta tentativa; o A e o B ficam como histórico. Redesenhado à mão medindo na guia oculta
# (guias/cao-infernal-t-guia-16.png: o recorte quadrado de 1200 px a partir de (50, 40), reduzido por média; cada pixel
# vale 75 px) e na silhueta pelo alfa dela. Em três quartos para a esquerda: a orelha dobrada no alto, a testa pesada
# (a faixa de luz) sobre o sobrolho escuro, o olho de trás e o da frente acesos e estreitos sob ele, o focinho largo com
# as rugas do rosnado, o nariz grande (cinza escuro com o brilho: o negro sumia na caixa), o lábio levantado com a
# gengiva, a goela acesa cortada pela presa negra grande e a da frente com o reflexo, a mandíbula e o queixo, a orelha de
# trás à direita com o vermelho dentro e o pescoço escuro com a rachadura em poucos pontos. Na bancada: a primeira tinha a
# metade marrom e a metade de carvão como dois objetos e o nariz sumido; o marrom virou luz em faixas sobre uma massa só;
# a rachadura pontilhada do pescoço caiu pela metade.
CAO_T = [
    "....bk..........",
    "..bbrBbcc.......",
    "..cbBBcCccoc....",
    "...cbbcCCcccCc..",
    "..bLLLBBBCcocck.",
    "..ceckkkkcccorrk",
    "..LBLLbbeyccC..r",
    ".NNcbLBbcccCoc..",
    "nnNbLbbcccccCc..",
    ".nnrrbBbcccccoc.",
    ".TOOrtOrbcccccc.",
    ".tyOOtObcccccCc.",
    "..bBBtBBbccccocc",
    "...bbBBbcccccCc.",
    "......bBccccoc..",
    "......kbcccc....",
]
# N, a terceira tentativa do Cão (pedido do Jean, depois de recusar o T: "uma massa marrom com pontos de fogo", o focinho
# espremido à esquerda, a parte de trás dominando, a boca sem rosnado). A referência gerada fica só como direção de
# expressão e material; a construção é nova, sem guia, resolvida a 32 px dentro da carta, na ordem: reconhecer o cão,
# entender o rosnado, perceber o material. Em três quartos para a esquerda: as duas orelhas triangulares de cão (a de
# trás menor), a testa clara, o sobrolho escuro sobre o olho de trás (um pixel) e o da frente (dois), a ponte do focinho
# descendo até o nariz, que é escuro com o brilho em cima e fica recortado contra o focinho claro (contra o fundo ele
# sumia), as rugas do focinho, o lábio levantado com a gengiva, a goela acesa com duas presas grandes de obsidiana que se
# cruzam (a de cima com o reflexo), a mandíbula e o queixo claros, e o pescoço mais escuro que a cabeça, com a brasa em
# três pontos. Na bancada: a primeira, com o focinho curto e os olhos iguais, lia como gato; a segunda, em tons médios,
# não formava o focinho; com a luz nos planos de cima a cabeça apareceu; uma presa de três pixels virava uma grade na
# boca.
CAO_N = [
    "............k...",
    "......k....kHk..",
    ".....kHk..kHCk..",
    ".....kHCkkHCCck.",
    "....kHHCCCCCCcck",
    "...kHCkkCCkkCccd",
    "..kHCCeCCcceeccd",
    "NNHHHHCkCcccccdd",
    "nnHCkCkccccccdd.",
    ".nrrrrCccccccddd",
    ".TOOOOkcccccdddd",
    ".tyOtyCccccddodd",
    "..CrtrCcccddoddd",
    "..kCCCkcccdddod.",
    "....kkkcddddddd.",
    "......kddddddd..",
]
# N2, o retoque do rosto do N (pedido do Jean: a forma da cabeça melhorou; o rosto não). A pose, as orelhas, o
# enquadramento, a cabeça e o calor do N ficam; só as linhas 7 a 14, o rosto de baixo, mudam:
# - o risco cinza na altura do nariz era o brilho dele, dois pixels (0,7)(1,7), sobre um nariz negro que sumia contra a
#   caixa; o nariz vira uma ponta sólida de 2×2 num cinza escuro que aparece, com o brilho no canto de cima, ligada à
#   ponte do focinho;
# - o focinho contraído (a ruga escura entre a ponte e o lado claro); o lábio de cima levantado na frente, com a gengiva
#   vermelha à mostra; a abertura estreita e irregular, dois pixels de altura na frente e fechando para trás, com a goela
#   acesa e as presas de obsidiana (a de cima com o reflexo frio, a de baixo subindo), longe da borda para a presa escura
#   ter o quente dos dois lados (encostada na borda, sumia no fundo);
# - a mandíbula clara embaixo e, atrás dela, uma sombra que mostra onde ela termina e o pescoço começa (a bochecha
#   descia contínua e alongava o rosto).
CAO_N2 = list(CAO_N)
CAO_N2[7:15] = [
    "nNHHCkHkCcccccdd",
    "nnCkHCcccccccdd.",
    ".CrrrCccccccdddd",
    ".kTOyOkccccddddd",
    ".kOtkCcdcccddodd",
    "..CCCCdkddddoddd",
    "...kkkkddddddod.",
    "....kkkdddddddd.",
]
# R, três rosnados (pedido do Jean: o N2 ficou limpo, mas a expressão parecia uma careta cômica, o focinho comprimido,
# a boca repuxada e os dentinhos pendurados). Do N2 ficam as orelhas, a orientação e a paleta (`cao_n2`); o crânio sobe e
# recua para a direita, e o focinho ganha de 7 a 8 pixels, com o nariz na ponta: era a proporção do crânio herdado que
# espremia o focinho. Os dentes ficam dentro do calor, como parte da mordida (na borda, sumiam no fundo); os olhos sob o
# sobrolho escuro e a testa clara participam nas três. Na bancada, com o crânio antigo as três liam fraco (uma grelha de
# fogo, um focinho de porco); com o focinho longo, as três leem como cão.
CABECA_R = [
    "........k...k...",
    ".......kHk.kHk..",
    ".......kHCkHCck.",
    "......kHCCCCCcck",
    "....kHHkkCkkCccd",
]
# RA, a bocarra aberta: a mandíbula caída em cunha (mais aberta na frente, fechando na dobra), as presas grandes se
# cruzando dentro da goela acesa (a de cima na frente, uma menor atrás, a de baixo subindo entre elas), a mandíbula clara
# e pesada. Uma fileira de dentes alternados com o fogo virava uma grelha.
CAO_RA = CABECA_R + [
    "nNHHHHCeCCeeCccd",
    "nnHHCCkkcccccccd",
    "kCCCCCCkcccccccd",
    ".rtOOtOOkcccccdd",
    ".OtyOOyOkccccddd",
    ".OOOtOtkcccccdod",
    ".kCCCCCkccccddod",
    "..kCCCkkcccdddd.",
    "....kkkddddddd..",
    "......kdddddddd.",
    "......kdddddd...",
]
# RB, o lábio repuxado: a boca quase fechada, as rugas no dorso do focinho, o lábio de cima levantado com a gengiva
# vermelha de ponta a ponta, os dentes cerrados com o calor entre eles e o reflexo, a presa longa na frente cruzando a de
# baixo, o lábio de baixo claro.
CAO_RB = CABECA_R + [
    "nNHHHHCeCCeeCccd",
    "nnHkHkkccccccccd",
    "kCrrrrrrkccccccd",
    ".tTtOtTtkcccccdd",
    ".tCCCCCCkccccddd",
    "..kCCCCkcccccdod",
    "...kkkkcccccddod",
    "......kccdddddd.",
    "......kddddddd..",
    "......kdddddddd.",
    "......kdddddd...",
]
# RC, a cabeça baixa: o focinho desce em diagonal da testa até o nariz, como quem avança de cabeça baixa; a gengiva à
# mostra embaixo do nariz, a goela acesa com as presas se cruzando, a mandíbula curta e pesada apontando para baixo.
CAO_RC = CABECA_R + [
    "..kHHHCeCCeeCccd",
    "..kHHHCkcccccccd",
    ".kHHCCkccccccccd",
    "nNHCCkcccccccccd",
    "nnrrrrkcccccccdd",
    ".tOyOtOkcccccddd",
    ".OtOyOtkccccddod",
    "..kCCCCkcccdddod",
    "...kCCkkdddddd..",
    "....kkkddddddd..",
    "......kdddddd...",
]
# RA2, a boca da RA refeita (pedido do Jean: a cabeça da RA é a base; a alternância regular de claros e escuros fazia os
# dentes parecerem um aparelho, e a boca tinha divisões demais para o tamanho). A cabeça, as orelhas, o focinho, o olhar
# e o enquadramento da RA ficam; só as linhas 7 a 11 mudam: o lábio de cima levantado na frente, com a gengiva à mostra;
# uma cavidade escura e contínua entre os maxilares, em cunha, mais aberta na frente; uma presa de cima só, dominante e
# afunilada (dois pixels no alto, um na ponta), de obsidiana, com o reflexo frio na borda da frente e o escuro em volta;
# os dentes de baixo apenas sugeridos no vermelho escuro do fundo; o calor no fundo, junto da dobra da mandíbula; a
# mandíbula clara e pesada. Na bancada: uma boca compacta (a presa com o reflexo no alto e na ponta) e outra com a presa
# longa e a gengiva mais alta; a cavidade maior com a gengiva alta leu como a mordida mais ameaçadora na carta.
CAO_RA2 = list(CAO_RA)
CAO_RA2[7:12] = [
    "kCrrCCCkcccccccd",
    ".rTtvvrrkcccccdd",
    ".vTvvvrOkccccddd",
    ".vvvmmOykcccddod",
    ".kCCCCCkkcccddod",
]
# RA3, os dentes da RA2 refeitos (pedido do Jean: a boca da RA2 parecia banguela; a presa quase negra sumia na
# cavidade). A cabeça, a gengiva, a cavidade e o calor da RA2 ficam; mudam só as linhas 8 a 10: a presa de cima sai do
# maxilar com a face iluminada (dois pixels claros descendo) e o corpo em cinza de obsidiana atrás; a de baixo, menor e
# mais para trás, sobe da mandíbula (um pixel claro); o calor discreto no fundo. Sem presas cruzadas nem fileira de
# dentes. Na bancada, a presa que afinava para o corpo escuro perdia a ponta.
CAO_RA3 = list(CAO_RA2)
CAO_RA3[8:11] = [
    ".rgsvvrrkcccccdd",
    ".vgvvvrOkccccddd",
    ".vvvgmrOkcccddod",
]

# Histórico (fora da exportação): a primeira B, de pernas finas, que virava um emaranhado na carta.
CRIA_B_FINA = [
    "................", "................", "...........m..m.", "..........uVu.u.",
    "..uuu....uVVVuu.", ".uVVVu..uVVVVVVu", "uVMVVVuuVVmvmVVu", "uVVVVVVVVmvvvmVu",
    "vMmMmMVVVVmvmVu.", ".uvvvvuVVVVVVuu.", "..uuu.uVuuuuVVu.", "....uVu...uVVu..",
    "...uVu....uVu...", "..uVu.....uVu...", ".uVu......Vu....", ".MM......MM.....",
]

def _camada_cao(x, y, ch):
    if ch in "tT":
        return "dentes"
    if ch in "Oy":
        return "boca"
    if ch == "e":
        return "olhos"
    return "brasa" if ch in "ro" else "corpo"


def _camada_cao_t(x, y, ch):
    if ch in "tT":
        return "dentes"
    if ch in "nN":
        return "nariz"
    if ch == "e" or (ch == "y" and y < 8):
        return "olhos"
    if ch in "Oy" or (ch == "r" and y >= 9):
        return "boca"
    return "brasa" if ch == "o" else "corpo"


def _camada_cao_r(x, y, ch):  # nas cabeças R, todo vermelho é a gengiva (as orelhas não têm), então é da boca, como a
    if ch in "gs":  # os dentes de obsidiana em cinza (a RA3)
        return "dentes"
    return "boca" if ch in "rvm" else _camada_cao_t(x, y, ch)  # cavidade e o fundo dela (a RA2)


def _camada_cria(x, y, ch):
    return "fenda" if ch in "mMw" else "corpo"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "cao-infernal-a": (CAO_A, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cao-infernal-b": (CAO_B, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cria-vazio-a": (CRIA_A, "cria", ["corpo", "fenda"], _camada_cria),
    "cria-vazio-b": (CRIA_B, "cria", ["corpo", "fenda"], _camada_cria),
    "cria-vazio-a2": (CRIA_A2, "cria", ["corpo", "fenda"], _camada_cria),
    "cao-infernal-t": (CAO_T, "cao_t", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_t),
    "cao-infernal-n": (CAO_N, "cao_n", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_t),
    "cao-infernal-n2": (CAO_N2, "cao_n2", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_t),
    "cao-infernal-ra": (CAO_RA, "cao_n2", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_r),
    "cao-infernal-rb": (CAO_RB, "cao_n2", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_r),
    "cao-infernal-rc": (CAO_RC, "cao_n2", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_r),
    "cao-infernal-ra2": (CAO_RA2, "cao_ra2", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_r),
    "cao-infernal-ra3": (CAO_RA3, "cao_ra3", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_r),
}


def cor(ident, ch):
    return PALETAS[CAMADAS[ident][1]][ch]


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(cor(ident, ch)[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, _, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{cor(ident, ch)}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
