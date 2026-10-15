"""O teste do escudo (experimento, fora do jogo): uma alternativa ao escudo atual da HUD
(rpg/web/static/hud/icones/escudo-*.png), com o mesmo tipo de escudo, a mesma forma, os mesmos materiais e o mesmo
enquadramento: redondo, a face de ferro azulado em gomos, o aro de latão, a bossa de latão em cúpula no meio e os oito
cravos de latão. O que se busca é o volume e o acabamento:
  - o aro com espessura: um rolo de latão (luz em cima à esquerda, sombra embaixo à direita) e a lateral do escudo
    aparecendo embaixo e à direita, como num objeto de verdade visto quase de frente;
  - a frente, a borda e o que sobressai separados: um degrau escuro entre a face e o aro, um sulco em volta da base
    da bossa, a bossa e os cravos projetando sombra na face;
  - a construção à mostra: os oito gomos planos de ferro, cada um num plano de luz, com a emenda entre eles;
  - reflexos controlados: um brilho especular só onde a luz bate de frente (a cúpula, o rolo do aro, o gomo de cima à
    esquerda) e um reflexo de ambiente fraco, de metal;
  - a silhueta: o aro claro e um contorno escuro de 1 pixel em cada tamanho.

O processo: o escudo é um relevo (uma altura por ponto), iluminado como superfície (normal, luz difusa, especular,
sombra projetada e oclusão nos sulcos), renderizado em 8× o tamanho final e reduzido por média de área. Cada tamanho
de uso é renderizado à parte, com as medidas que precisam sobreviver nele (sulcos, cravos e aro com pelo menos o
pixel que os mostra). A saída tem os mesmos nomes do jogo (escudo-32.png, escudo-32@2x.png...), em escudo-teste/.

    python ferramentas/prototipos/hud/desenhar_escudo.py
"""

import pathlib

import numpy as np
from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "escudo-teste"

# As cores, tiradas do escudo atual (o latão e o ferro azulado dele), em escuro, base e brilho.
FERRO = (np.array([16, 19, 28]), np.array([66, 74, 95]), np.array([232, 236, 242]))
LATAO = (np.array([52, 31, 9]), np.array([186, 132, 52]), np.array([255, 232, 160]))
LATERAL = np.array([74, 47, 16])  # a espessura do aro, vista de lado (latão na sombra)
LUZ = np.array([-0.55, -0.65, 0.75]); LUZ = LUZ / np.linalg.norm(LUZ)
MEIO = (LUZ + np.array([0, 0, 1.0])); MEIO = MEIO / np.linalg.norm(MEIO)

# O enquadramento do atual: o escudo ocupa 101 de 128 px (79%), centrado.
RAIO = 0.79


def borrar(a, r):
    """Média num quadrado de lado 2r+1 (separável), para a oclusão e a textura."""
    if r < 1:
        return a
    k = np.ones(2 * r + 1) / (2 * r + 1)
    a = np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, "valid"), 0, a)
    return np.apply_along_axis(lambda x: np.convolve(np.pad(x, r, mode="edge"), k, "valid"), 1, a)


def renderizar(lado, sobra=8):
    """O escudo em `lado` px (RGBA). `sobra`: quantas vezes maior se renderiza antes da redução."""
    n = lado * sobra
    px = 2 / n  # o tamanho de um pixel do render, em unidades do quadro (-1..1)
    pf = 2 / lado / RAIO  # o tamanho de um pixel final, em unidades do raio do escudo
    y, x = np.mgrid[0:n, 0:n]
    u = (x + 0.5) * px - 1
    v = (y + 0.5) * px - 1
    # a lateral (a espessura do escudo) aparece embaixo e à direita: o disco da frente fica um pouco acima e à esquerda
    deslocamento = max(0.045, 1.8 * pf) * RAIO
    fu, fv = u + deslocamento * 0.55, v + deslocamento * 0.8
    r = np.hypot(fu, fv) / RAIO
    t = np.arctan2(fv, fu)

    # medidas (em unidades do raio); as finas nunca menores que o pixel do tamanho final
    m = lambda base, minimo=1.0: max(base, minimo * pf)
    r_cupula, r_base = 0.25, 0.25 + m(0.06, 1.2)
    r_sulco = r_base + m(0.04, 1.0)
    largura_aro = m(0.12, 2.4)
    r_aro = 1 - largura_aro
    r_cravo, r_cravos = m(0.058, 0.85), r_aro - m(0.085, 1.7)

    h = np.zeros_like(r)
    mat = np.zeros(r.shape, dtype=np.int8)  # 0 fora, 1 ferro, 2 latão
    # a face de ferro: oito gomos planos (uma pirâmide rasa de oito lados), emendas a 22,5° dos cravos
    passo = np.pi / 4
    centro_gomo = np.round(t / passo) * passo
    face = (r >= r_sulco) & (r < r_aro)
    # o plano de cada gomo, misturado a uma cúpula rasa: o reflexo corre dentro do gomo em vez de acender a chapa inteira
    h_face = 0.62 * (0.36 - 0.34 * r * np.cos(t - centro_gomo)) + 0.38 * (0.36 - 0.3 * r ** 2)
    # as marcas do martelo: um relevo leve e irregular
    rng = np.random.default_rng(7)
    martelo = borrar(rng.standard_normal(r.shape), max(1, n // 48)) * 0.004
    h = np.where(face, h_face + martelo, h)
    mat[face] = 1
    # o degrau: a face desce um pouco antes do aro (a sombra que separa frente e borda)
    degrau = face & (r > r_aro - m(0.03, 0.7))
    h = np.where(degrau, h - 0.06, h)
    # o sulco em volta da base da bossa
    sulco = (r >= r_base) & (r < r_sulco)
    h = np.where(sulco, 0.0, h)
    mat[sulco] = 1
    # a base da bossa: um disco de latão em rampa, com a borda arredondada
    base = (r >= r_cupula) & (r < r_base)
    s = (r - r_cupula) / (r_base - r_cupula)
    h = np.where(base, 0.42 - 0.06 * s - 0.08 * s ** 4, h)
    mat[base] = 2
    # a cúpula
    cup = r < r_cupula
    h = np.where(cup, 0.42 + 0.2 * np.sqrt(np.clip(1 - (r / r_cupula) ** 2, 0, 1)), h)
    mat[cup] = 2
    # o aro: um rolo de latão
    aro = (r >= r_aro) & (r <= 1)
    c = (r - (r_aro + 1) / 2) / (largura_aro / 2)
    h = np.where(aro, 0.0 + 0.13 * np.sqrt(np.clip(1 - c ** 2, 0, 1)), h)
    mat[aro] = 2
    # os cravos: oito cúpulas de latão sobre a face, nos ângulos dos gomos
    for k in range(8):
        a = k * passo
        cu, cv = r_cravos * np.cos(a), r_cravos * np.sin(a)
        d = np.hypot(r * np.cos(t) - cu, r * np.sin(t) - cv) / r_cravo
        dentro = d < 1
        h = np.where(dentro, np.maximum(h, h_face + 0.04 * np.sqrt(np.clip(1 - d ** 2, 0, 1)) + 0.01), h)
        mat[dentro] = 2

    # a normal a partir da altura (a altura em unidades do raio; o passo do pixel também)
    passo_px = px / RAIO
    gy, gx = np.gradient(h, passo_px)
    nrm = np.stack([-gx, -gy, np.ones_like(h)], axis=-1)
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
    difusa = np.clip(nrm @ LUZ, 0, 1)
    especular = np.clip(nrm @ MEIO, 0, 1)
    # o reflexo de ambiente: o céu claro em cima, o chão escuro embaixo, no vetor refletido
    refl_y = 2 * nrm[..., 2] * nrm[..., 1]
    ambiente = np.clip(0.5 - 0.9 * refl_y, 0, 1)

    # a sombra projetada: de cada ponto, anda na direção da luz; se o relevo ali passa acima do raio, há sombra
    sombra = np.zeros_like(h)
    rumo = LUZ[:2] / np.linalg.norm(LUZ[:2])  # para onde fica a luz, no plano (cima e esquerda)
    subida = LUZ[2] / np.linalg.norm(LUZ[:2])  # quanto o raio sobe por unidade andada
    for k in range(1, int(0.25 / passo_px)):
        dx, dy = int(round(-rumo[0] * k)), int(round(-rumo[1] * k))  # np.roll(a, s)[i] = a[i - s]
        alt = np.roll(np.roll(h, dy, axis=0), dx, axis=1)
        sombra = np.maximum(sombra, np.clip((alt - h - k * passo_px * subida) * 60, 0, 1))
    luz_util = 1 - 0.75 * sombra
    # a oclusão: o que está abaixo da vizinhança escurece (sulcos, degrau, pé dos cravos)
    oclusao = np.clip(1 - 9 * (borrar(h, max(1, sobra)) - h), 0.35, 1)

    cor = np.zeros(h.shape + (3,))
    for idx, (escuro, base_c, brilho), expo, forca, amb in ((1, FERRO, 48, 1.35, 0.05), (2, LATAO, 22, 1.7, 0.06)):
        sel = mat == idx
        d = (difusa * luz_util * oclusao)[..., None]
        e = ((especular ** expo) * luz_util)[..., None]
        val = escuro + (base_c - escuro) * np.clip(0.12 + 0.85 * d, 0, 1.15) + (brilho - base_c) * np.clip(forca * e, 0, 1)
        val = val + (brilho - escuro) * (amb * ambiente * oclusao)[..., None]
        cor[sel] = val[sel]
    # a emenda entre os gomos: uma linha escura fina na face
    emenda = face & (np.abs(np.abs(t - centro_gomo) - passo / 2) * r < 0.6 * pf) & (r > r_sulco + 0.02)
    cor[emenda] = cor[emenda] * 0.85
    # a lateral (espessura) embaixo e à direita, atrás da frente
    r_tras = np.hypot(u, v) / RAIO
    lateral = (r_tras <= 1) & (mat == 0)
    sombra_lado = np.clip(0.55 + 0.45 * ((u + v) / (2 * RAIO)), 0.35, 1)[..., None]
    cor[lateral] = (LATERAL * sombra_lado)[lateral]
    mat[lateral] = 3
    alfa = (mat > 0).astype(float)

    img = np.dstack([np.clip(cor, 0, 255), alfa * 255]).astype(np.float64)
    # a redução por média de área (pré-multiplicada, para a borda não escurecer nem clarear)
    pre = img.copy(); pre[..., :3] *= alfa[..., None]
    pre = pre.reshape(lado, sobra, lado, sobra, 4).mean(axis=(1, 3))
    a = pre[..., 3:4] / 255
    rgb = np.where(a > 0, pre[..., :3] / np.maximum(a, 1e-6), 0)
    final = np.dstack([rgb, pre[..., 3]])
    # o contorno escuro de 1 pixel em volta da silhueta (para ler sobre o carvão)
    dentro = final[..., 3] > 128
    viz = np.zeros_like(dentro)
    for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        viz |= np.roll(np.roll(dentro, ddy, 0), ddx, 1)
    borda = viz & (final[..., 3] < 200)
    final[borda, :3] = final[borda, :3] * 0.35 + np.array([10, 9, 8]) * 0.65
    final[borda, 3] = np.maximum(final[borda, 3], 200)
    return Image.fromarray(np.clip(final, 0, 255).astype(np.uint8), "RGBA")


def nitidez(img, forca):
    """Um realce leve dos contrastes locais, para o tamanho pequeno não ficar mole depois da redução."""
    a = np.asarray(img).astype(float)
    borr = np.stack([borrar(a[..., c], 1) for c in range(3)], axis=-1)
    a[..., :3] = np.clip(a[..., :3] + forca * (a[..., :3] - borr), 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA")


if __name__ == "__main__":
    SAIDA.mkdir(exist_ok=True)
    # os arquivos do jogo: 32, 48 e 64, cada um com o dobro
    for lado, nome, realce in ((32, "escudo-32", 0.45), (64, "escudo-32@2x", 0.2), (48, "escudo-48", 0.3),
                               (96, "escudo-48@2x", 0.1), (64, "escudo-64", 0.2), (128, "escudo-64@2x", 0.0)):
        img = renderizar(lado, sobra=8 if lado <= 64 else 6)
        if realce:
            img = nitidez(img, realce)
        img.save(SAIDA / f"{nome}.png")
        print(nome, img.size)
