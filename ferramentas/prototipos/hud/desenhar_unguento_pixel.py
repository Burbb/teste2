"""O Unguento de Prata em pixel art (experimento, fora do jogo): o segundo objeto do método do escudo refinado
(desenhar_escudo_pixel.py), para ver se ele se transfere a outro objeto e a outros materiais.

O que o jogo diz do item (rpg/itens.py e os usos): "Unguento de Prata", "Cura uma infecção", 30 de ouro no mercado
(estoque de 0 a 2), usado fora da luta ("O unguento arde como fogo. Horas depois, a febre cede"); a curandeira trata
"com unguentos". Nada de brilho mágico, símbolo ou efeito: um pote de remédio com a pasta dentro.
A identidade vem do desenho atual (o sprite "unguento", 16 x 16, que é também o da curandeira): um pote baixo de
louça clara, de paredes retas, com uma faixa de rótulo azul-esverdeado com uma tira clara no meio. A proposta guarda
isso (a louça, a forma, o rótulo) e abre o pote: sem a tampa, a boca mostra a pasta de prata. O primeiro candidato
(desenhar_itens.py, um pote de barro com espátula) fica só como histórico.

A construção, em cada tamanho (32, 48 e 64 px), na própria grade:
  - o pote: um cilindro visto um pouco de cima (cada volta horizontal é uma elipse, achatada por K); as paredes
    retas, o fundo arredondado pela elipse de baixo, o ombro curto e a boca um pouco mais estreita que o corpo;
  - a louça vidrada: a luz pela normal do cilindro (o lado esquerdo acende, o direito escurece), na rampa da louça; o
    vidrado devolve um reflexo, mas macio: uma faixa vertical estreita um degrau acima, onde o cilindro vira para a
    luz, sem o branco do metal; junto do chão, um degrau mais escuro;
  - a borda: o topo do lábio (um anel em elipse) vira para cima e acende, mais claro atrás à esquerda; a espessura
    do lábio aparece na frente como uma faixa sombreada como o corpo, e embaixo dela, em 48 e 64, o sulco do pescoço;
    a beirada de dentro do lábio, na frente, desce um degrau (separa a borda da pasta);
  - a abertura: a parede de dentro, atrás, em sombra (o lado direito, que vira para a luz, mais claro), e a pasta
    abaixo da borda;
  - a pasta: cinza de prata, fria (a louça é quente), fosca e macia: a luz pela normal de um monte baixo, sem
    especular; a sombra da borda de trás sobre ela; em 48 e 64 a marca rasa de onde já se tirou um pouco;
  - o rótulo: papel, fosco (o reflexo do vidrado para nele); a faixa azul-esverdeada com a tira clara no meio, as
    duas sombreadas pela mesma normal do cilindro, e as bordas curvas como as voltas do pote (é o que dá o volume);
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/prototipos/hud/desenhar_unguento_pixel.py
"""

import pathlib

import numpy as np

from pixel_comum import ANG_LUZ, LUZ, ajustar, contornar, grade, imagem, limpar, salvar

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "unguento-pixel"

# As rampas, do mais escuro ao mais claro. A louça (o bege acinzentado do atual, quente) e o reflexo do vidrado no
# último tom; a pasta de prata (cinza frio, um pouco azulado); o rótulo (o azul-esverdeado e a tira clara do atual).
LOUCA = ["#1e1a16", "#332c26", "#4a4038", "#665b4f", "#857a69", "#a39885", "#c0b8a8", "#d9d3c6", "#efebe2"]
PRATA = ["#1f2329", "#333840", "#4b515a", "#666d77", "#838a94", "#a3a9b2", "#c3c8cf", "#e0e3e7"]
VERDE = ["#0f2224", "#173236", "#214a4f", "#2f666c", "#448a90", "#5ca8ad", "#74c4c9", "#94d8dc"]
PAPEL = ["#3a3428", "#544b3a", "#706550", "#8f8268", "#ad9f80", "#c9bb98", "#e2d4b0", "#f1e4c4"]

# As medidas de cada tamanho, em pixels. O centro (cx) e a meia largura do corpo (a); o achatamento das voltas (K,
# a meia altura de uma volta é a largura vezes K); a borda: o centro (yb), a meia largura de fora (rb) e a largura
# do topo do lábio (labio), a espessura da frente (esp) e o sulco embaixo dela (sulco); o fundo (yf, o centro da
# elipse de baixo); o rótulo: do alto (rt, abaixo do ombro) e a altura (rh), a tira clara (tira, a altura) e até
# onde ele dá a volta (ru); o reflexo do vidrado (largura em u); a pasta: quanto abaixo da borda (fundo) e o monte.
MEDIDAS = {
    32: dict(cx=16.0, a=11.0, K=0.3, yb=7.6, rb=9.6, labio=1.6, esp=1, sulco=False, yf=24.6, rt=3.2, rh=6.0,
             tira=2.0, ru=0.8, barriga=0.0, pe=1.2, reflexo=(-0.62, -0.38), fundo=1.4, monte=0.8, marca=False),
    48: dict(cx=24.0, a=16.5, K=0.3, yb=11.0, rb=14.4, labio=2.3, esp=2, sulco=True, yf=37.2, rt=4.8, rh=9.0,
             tira=3.0, ru=0.8, barriga=0.9, pe=1.8, reflexo=(-0.6, -0.4), fundo=1.8, monte=1.3, marca=False),
    64: dict(cx=32.0, a=22.0, K=0.3, yb=14.6, rb=19.2, labio=3.0, esp=2, sulco=True, yf=49.8, rt=6.4, rh=12.0,
             tira=4.0, ru=0.8, barriga=1.2, pe=2.4, reflexo=(-0.6, -0.42), fundo=2.3, monte=1.7, marca=False),
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 48: {}, 64: {}}


def faixas(v):
    """O tom pela luz recebida, em poucas faixas largas (o mesmo para a louça, o rótulo e a tira)."""
    return np.select([v > 0.66, v > 0.42, v > 0.2, v > 0.06], [6, 5, 4, 3], 2)


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    cx, a, K = M["cx"], M["a"], M["K"]
    dx = x - cx

    def elipse(rx, yc, oy=0.0):
        return (dx / rx) ** 2 + ((y - yc - oy) / (rx * K)) ** 2 <= 1

    # ---- o corpo: o cilindro do ombro ao fundo, a borda de baixo pela elipse do fundo
    yb, rb = M["yb"], M["rb"]
    topo_corpo = yb + M["esp"] + (1 if M["sulco"] else 0)   # onde começa o ombro (abaixo do lábio e do sulco)
    # o ombro: em ~2 px a largura vai da boca à do corpo
    ombro = np.clip((y - topo_corpo) / (1.2 + 0.05 * lado), 0, 1)
    # a louça tem barriga: o corpo abre um pouco no meio (barriga) e fecha junto do fundo (o pé arredondado)
    alto = np.clip((y - topo_corpo) / (M["yf"] - topo_corpo), 0, 1)
    raio = rb - 0.4 + (a - rb + 0.4) * np.sqrt(ombro) + M["barriga"] * np.sin(np.pi * alto)
    chao = M["yf"] + a * K * np.sqrt(np.clip(1 - (dx / a) ** 2, 0, 1))
    raio = raio - M["pe"] * np.clip((y - (M["yf"] - 1.0)) / (a * K + 1.0), 0, 1) ** 2
    corpo = (np.abs(dx) <= raio) & (y >= topo_corpo) & (y <= chao)
    u = np.clip(dx / np.maximum(raio, 0.5), -1, 1)
    nz = np.sqrt(1 - u ** 2)
    sobe = np.where(ombro < 1, 0.5, 0.0)       # o ombro vira um pouco para cima
    nrm = np.stack([u, -sobe, nz], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    v = np.clip(nrm @ LUZ, 0, 1)
    # a louça é fosca por baixo do vidrado: poucos tons largos (a frente clara, a sombra à direita), não as faixas
    # verticais de um metal; as beiradas que viram para longe um degrau abaixo
    tom_corpo = faixas(v) - (np.abs(u) > 0.94)
    mat[corpo], tom[corpo] = "l", tom_corpo[corpo]
    pe = corpo & (y > chao - 1.0)               # junto do chão, um degrau mais escuro
    tom[pe] = np.maximum(1, tom[pe] - 1)

    # ---- o rótulo: papel em volta do corpo, as bordas curvas como as voltas do pote
    curva = a * K * np.sqrt(np.clip(1 - u ** 2, 0, 1))
    r0 = topo_corpo + M["rt"] + curva
    rotulo = corpo & (y >= r0) & (y < r0 + M["rh"]) & (np.abs(u) <= M["ru"])
    meio = r0 + M["rh"] / 2
    tira = rotulo & (np.abs(y - meio) < M["tira"] / 2) & (np.abs(u) <= M["ru"] - 0.22)
    tom_rot = faixas(v) - (np.abs(u) > 0.7)
    mat[rotulo], tom[rotulo] = "v", tom_rot[rotulo]
    mat[tira], tom[tira] = "p", tom_rot[tira]

    # ---- o reflexo do vidrado: uma faixa estreita onde o cilindro vira para a luz, fora do rótulo
    r1, r2 = M["reflexo"]
    brilho = corpo & ~rotulo & (u >= r1) & (u <= r2) & (ombro >= 1) & (y < chao - 1.5)
    tom[brilho], fixo[brilho] = 7, True

    # ---- a borda: o lábio (o topo em anel e a espessura da frente) e o sulco embaixo
    fora = elipse(rb, yb)
    ri = rb - M["labio"]
    boca = elipse(ri, yb)
    frente = np.zeros_like(fora)
    for k in range(1, M["esp"] + 1):
        frente |= elipse(rb, yb, k)
    frente &= ~fora & (y > yb)
    mat[frente], tom[frente] = "l", np.clip(tom_corpo[frente] - 1, 1, 6)
    if M["sulco"]:
        sul = elipse(rb - 0.4, yb, M["esp"] + 1) & ~fora & ~frente & (y > yb)
        mat[sul], tom[sul] = "l", np.clip(tom_corpo[sul] - 3, 0, 4)
    ang = np.arctan2((y - yb) / (rb * K), dx / rb)
    dl = np.abs((ang - ANG_LUZ + np.pi) % (2 * np.pi) - np.pi)
    labio = fora & ~boca
    tom_labio = np.select([dl < 0.8, dl < 1.8, dl < 2.6], [7, 6, 5], 4)
    # a beirada de dentro, na frente, desce para dentro do pote: um degrau mais escura
    beirada = labio & ~elipse(ri + 0.9, yb) & (y > yb)
    tom_labio = np.where(beirada, 4, tom_labio)
    mat[labio], tom[labio] = "l", tom_labio[labio]

    # ---- a abertura: a parede de dentro, atrás, e a pasta abaixo da borda, num monte baixo
    sup = elipse(ri, yb, M["fundo"])
    monte = (dx / (ri * 0.7)) ** 2 + ((y - yb - M["fundo"] + M["monte"] * 0.6) / (ri * K * 0.85 + M["monte"] * 0.5)) ** 2 <= 1
    # o monte não cobre a parede de trás: a linha escura de dentro fica inteira, separando a borda da pasta
    pasta = boca & (sup | (monte & (y > yb - ri * K * 0.35)))
    parede = boca & ~pasta
    mat[parede], tom[parede] = "l", np.where(dx[parede] > 0, 2, 1)
    # a luz da pasta: macia, em volta de um ponto em cima à esquerda do monte (um volume, não um plano espelhado);
    # a frente e a direita, que descem para longe da luz, um degrau abaixo
    lx, ly = cx - 0.3 * ri, yb + M["fundo"] - M["monte"] * 0.4
    dp = np.hypot((dx - (lx - cx)) / ri, (y - ly) / (ri * K + M["monte"]))
    tom_pasta = np.select([dp < 0.45, dp < 1.05], [5, 4], 3)
    mat[pasta], tom[pasta] = "s", tom_pasta[pasta]
    sombra = pasta & ~elipse(ri, yb, M["fundo"] + 0.9) & (y < yb)    # a sombra da borda de trás
    tom[sombra] = np.maximum(1, tom[sombra] - 2)
    # o brilho macio da pasta: um grupo pequeno, um degrau acima, em cima à esquerda do monte
    bx = int(np.floor(cx - 0.3 * ri))
    by = int(np.floor(yb + M["fundo"] - M["monte"] * 0.4))
    grupo = {32: {(0, 0): 6, (1, 0): 6},
             48: {(0, 0): 6, (1, 0): 6, (-1, 0): 5, (2, 0): 5},
             64: {(0, 0): 6, (1, 0): 6, (2, 0): 5, (-1, 0): 5, (0, 1): 5, (1, 1): 5}}[lado]
    for (ox, oy), t_ in grupo.items():
        if mat[by + oy, bx + ox] == "s":
            tom[by + oy, bx + ox], fixo[by + oy, bx + ox] = t_, True
    # a marca de onde já se tirou um pouco (48 e 64): numa cavidade a luz se inverte
    if M["marca"]:
        mx, my = cx + 0.32 * ri, yb + M["fundo"] + 0.2
        rmx, rmy = 0.24 * ri, 0.3 * ri * K + 0.5
        dm = ((x - mx) / rmx) ** 2 + ((y - my) / rmy) ** 2
        cava = pasta & (dm <= 1)
        lado_luz = (x - mx) * LUZ[0] + (y - my) * LUZ[1] > 0
        tom[cava & lado_luz] = np.maximum(1, tom[cava & lado_luz] - 2)
        acesa = cava & ~lado_luz & (dm > 0.35)
        tom[acesa] = np.minimum(6, tom[acesa] + 1)
        fixo[cava] = True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"l": LOUCA, "s": PRATA, "v": VERDE, "p": PAPEL})


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    for lado in (32, 48, 64):
        print(f"unguento-{lado}: {salvar(desenhar(lado), SAIDA, 'unguento')} cores")
