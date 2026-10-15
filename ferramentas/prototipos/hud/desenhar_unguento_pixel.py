"""O Unguento de Prata em pixel art (experimento, fora do jogo): o segundo objeto do método do escudo refinado
(desenhar_escudo_pixel.py). Esta é a segunda proposta, com o conceito novo do recipiente.

O que o jogo diz do item (rpg/itens.py e os usos): "Unguento de Prata", "Cura uma infecção", 30 de ouro no mercado
(estoque de 0 a 2), usado fora da luta ("O unguento arde como fogo. Horas depois, a febre cede"); a curandeira trata
"com unguentos". Nada de brilho mágico, símbolo ou efeito: um pote de remédio com a pasta dentro. O nome, a descrição,
o preço e as regras não mudam; só o desenho.

O conceito (decisão de Jean): a embalagem do desenho atual (as paredes retas e o rótulo azul-esverdeado) lembra uma
embalagem moderna. O recipiente passa a ser um pequeno pote de cerâmica de boticário: o corpo baixo e arredondado, a
boca mais estreita que o corpo, a borda espessa, a abertura legível, barro bege acinzentado e a pasta cinza-prateada
à vista. O primeiro candidato (desenhar_itens.py, o pote de barro) serve de referência de conceito; a primeira
proposta (o pote de louça com rótulo, unguento-pixel-v1/) fica como histórico. A tampa ao lado foi pensada e ficou
de fora: em 32 px ela tirava largura do pote sem ajudar a ler o objeto.

A construção, em cada tamanho (32 e 64 px), na própria grade:
  - o pote: uma forma de revolução vista um pouco de cima (cada volta horizontal é uma elipse, achatada por K): a
    barriga é uma superelipse (o raio de cada linha), o pescoço um cilindro curto mais estreito, o fundo cortado na
    elipse de baixo (o pote assenta);
  - o barro: fosco, a luz pela normal da forma (o ombro e o lado esquerdo acendem, o de baixo e o direito escurecem),
    em poucas faixas largas da rampa; sem reflexo de metal nem de vidrado (um grupo de brilho no ombro foi tentado e
    lia como um cisco); junto do chão, um degrau mais escuro;
  - a borda: um lábio grosso; o topo (um anel em elipse) vira para cima e acende, mais claro atrás à esquerda; a
    espessura aparece na frente, sombreada como o corpo; embaixo dela, a sombra do lábio no pescoço; a beirada de
    dentro, na frente, desce um degrau (separa a borda da pasta);
  - a abertura: a parede de dentro, atrás, em sombra (o lado direito, que vira para a luz, mais claro);
  - o unguento: cinza de prata, frio (o barro é quente), fosco e macio, num monte baixo com a ponta de onde a
    espátula saiu: a luz em volta de um ponto em cima à esquerda, a sombra da borda de trás sobre ele;
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/prototipos/hud/desenhar_unguento_pixel.py
"""

import pathlib

import numpy as np

from pixel_comum import ANG_LUZ, LUZ, ajustar, contornar, grade, imagem, limpar, salvar

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "unguento-pixel"

# As rampas, do mais escuro ao mais claro: o barro (bege acinzentado, quente) e a pasta de prata (cinza frio).
BARRO = ["#1d1712", "#32281f", "#4a3c2f", "#655240", "#816a53", "#9c8467", "#b59d7e", "#cbb596", "#ddcbb0"]
PRATA = ["#1f2329", "#333840", "#4b515a", "#666d77", "#838a94", "#a3a9b2", "#c3c8cf", "#e0e3e7"]

# As medidas de cada tamanho, em pixels. O centro (cx) e o achatamento das voltas (K); a barriga: o centro (by), a
# meia largura (a), a meia altura (b) e o expoente (exp, maior = mais cheia); o fundo (yf, o centro da elipse de baixo);
# o pescoço (rn, a meia largura); a borda: o centro (yb), a meia largura de fora (rb), a largura do topo do lábio
# (labio) e a espessura da frente (esp); a pasta: quanto abaixo da borda (fundo), o monte, a ponta e o brilho,
# desenhado por tamanho.
MEDIDAS = {
    32: dict(cx=16.0, K=0.44, by=20.2, a=13.0, b=8.6, exp=2.3, yf=26.0, rn=7.6, yb=9.6, rb=9.0, labio=2.0, esp=1,
             fundo=1.2, monte=1.0, ponta=1,
             brilho={(0, 0): 6, (1, 0): 5}),
    64: dict(cx=32.0, K=0.44, by=40.4, a=26.0, b=17.2, exp=2.3, yf=52.0, rn=15.2, yb=19.2, rb=18.0, labio=3.6, esp=2,
             fundo=2.2, monte=2.0, ponta=2,
             brilho={(0, 0): 6, (1, 0): 6, (2, 0): 5, (-1, 0): 5, (0, 1): 5, (1, 1): 5}),
}
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 64: {}}


def faixas(v):
    """O tom do barro pela luz recebida, em poucas faixas largas (fosco)."""
    return np.select([v > 0.66, v > 0.4, v > 0.14], [6, 5, 4], 3) - (v < 0.03)


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    cx, K = M["cx"], M["K"]
    dx = x - cx

    def elipse(rx, yc, oy=0.0):
        return (dx / rx) ** 2 + ((y - yc - oy) / (rx * K)) ** 2 <= 1

    # ---- o corpo: a barriga (superelipse girada), o pescoço e o fundo
    def raio_barriga(yy):
        t = np.clip((yy - M["by"]) / M["b"], -1, 1)
        return M["a"] * np.clip(1 - np.abs(t) ** M["exp"], 0, 1) ** (1 / M["exp"])
    rbar = raio_barriga(y)
    yb, rb = M["yb"], M["rb"]
    pescoco_ate = M["by"] - M["b"] * 0.55     # o pescoço desce até dentro da barriga (o ombro sai da barriga)
    raio = np.where((y >= yb) & (y <= pescoco_ate), np.maximum(rbar, M["rn"]), rbar)
    rf = float(raio_barriga(np.array(M["yf"])))
    chao = M["yf"] + rf * K * np.sqrt(np.clip(1 - (dx / rf) ** 2, 0, 1))
    corpo = (np.abs(dx) <= raio) & (y >= yb) & ((y <= M["yf"]) | ((np.abs(dx) <= rf) & (y <= chao)))
    # a normal: (u, -r'(y), nz) da forma de revolução; no pescoço, um cilindro
    passo = 0.5
    dr = (raio_barriga(y + passo) - rbar) / passo
    dr = np.where(rbar < M["rn"], 0.0, dr)
    # abaixo do centro do fundo, a forma continua a da linha do fundo (senão o raio da barriga, já fechando, deixava o
    # fundo de lado e acendia a última linha)
    dr_f = float((raio_barriga(np.array(M["yf"] + passo)) - rf) / passo)
    dr = np.where(y > M["yf"], dr_f, dr)
    raio = np.where(y > M["yf"], rf, raio)
    u = np.clip(dx / np.maximum(raio, 0.5), -1, 1)
    nz = np.sqrt(1 - u ** 2)
    nrm = np.stack([u, -np.clip(dr, -2.5, 2.5) * nz, nz + 0.1], -1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    v = np.clip(nrm @ LUZ, 0, 1)
    tom_corpo = faixas(v) - (np.abs(u) > 0.95)
    mat[corpo], tom[corpo] = "b", tom_corpo[corpo]
    pe = corpo & (y > chao - 1.0) & (y > M["yf"] - 0.5)
    tom[pe] = np.maximum(1, tom[pe] - 1)
    # ---- a borda: o lábio grosso (o topo em anel e a espessura da frente) e a sombra dele no pescoço
    fora = elipse(rb, yb)
    ri = rb - M["labio"]
    boca = elipse(ri, yb)
    frente = np.zeros_like(fora)
    for k in range(1, M["esp"] + 1):
        frente |= elipse(rb, yb, k)
    frente &= ~fora & (y > yb)
    uf = np.clip(dx / rb, -1, 1)
    vf = np.clip(np.stack([uf, np.zeros_like(uf), np.sqrt(1 - uf ** 2)], -1) @ LUZ, 0, 1)
    mat[frente], tom[frente] = "b", np.clip(faixas(vf)[frente] - 1, 1, 5)
    sombra_labio = corpo & ~fora & ~frente & elipse(rb, yb, M["esp"] + 1) & (y > yb)
    tom[sombra_labio] = np.maximum(0, tom[sombra_labio] - 2)
    ang = np.arctan2((y - yb) / (rb * K), dx / rb)
    dl = np.abs((ang - ANG_LUZ + np.pi) % (2 * np.pi) - np.pi)
    labio = fora & ~boca
    tom_labio = np.select([dl < 0.8, dl < 1.8, dl < 2.6], [7, 6, 5], 4)
    beirada = labio & ~elipse(ri + 0.9, yb) & (y > yb)   # a beirada de dentro, na frente, desce para dentro
    tom_labio = np.where(beirada, 4, tom_labio)
    mat[labio], tom[labio] = "b", tom_labio[labio]

    # ---- a abertura e o unguento: a parede de dentro, atrás, e a pasta abaixo da borda, num monte com a ponta
    sup = elipse(ri, yb, M["fundo"])
    monte = (dx / (ri * 0.7)) ** 2 + ((y - yb - M["fundo"] + M["monte"] * 0.6) / (ri * K * 0.85 + M["monte"] * 0.5)) ** 2 <= 1
    pasta = boca & (sup | (monte & (y > yb - ri * K * 0.35)))
    parede = boca & ~pasta
    mat[parede], tom[parede] = "b", np.where(dx[parede] > 0, 2, 1)
    lx, ly = cx - 0.3 * ri, yb + M["fundo"] - M["monte"] * 0.4
    dp = np.hypot((x - lx) / ri, (y - ly) / (ri * K + M["monte"]))
    tom_pasta = np.select([dp < 0.45, dp < 1.05], [5, 4], 3)
    mat[pasta], tom[pasta] = "s", tom_pasta[pasta]
    sombra = pasta & ~elipse(ri, yb, M["fundo"] + 0.9) & (y < yb)    # a sombra da borda de trás
    tom[sombra] = np.maximum(1, tom[sombra] - 2)
    # o brilho macio da pasta (em cima à esquerda do monte) e a ponta de onde a espátula saiu (no meio, acima da
    # superfície: o lado da luz um degrau acima, o outro um abaixo)
    bx, by_ = int(np.floor(lx)), int(np.floor(ly))
    for (ox, oy), t_ in M["brilho"].items():
        if mat[by_ + oy, bx + ox] == "s":
            tom[by_ + oy, bx + ox], fixo[by_ + oy, bx + ox] = t_, True
    px_, py_ = int(np.floor(cx + 0.15 * ri)), int(np.floor(yb + M["fundo"] - M["monte"] * 0.6))
    for k in range(M["ponta"]):
        for ox, t_ in ((0, 5), (1, 3)):
            yy, xx = py_ - k, px_ + ox
            if mat[yy, xx] in ("s", "b") and boca[yy, xx]:
                mat[yy, xx], tom[yy, xx], fixo[yy, xx] = "s", t_ + (1 if k else 0), True

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"b": BARRO, "s": PRATA})


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    for velho in SAIDA.glob("unguento-48*.png"):   # o conceito novo tem 32 e 64 (o 48 era da primeira proposta)
        velho.unlink()
    for lado in (32, 64):
        print(f"unguento-{lado}: {salvar(desenhar(lado), SAIDA, 'unguento')} cores")
