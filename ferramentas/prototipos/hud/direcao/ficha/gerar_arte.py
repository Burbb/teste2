"""A arte da prova da ficha (em avaliação, nada no jogo): a superfície da coluna com a borda rasgada e o papel gasto
da margem. Procedural e reproduzível (semente fixa), em camadas de ruído de várias escalas:
  - o carvão: a cor base com manchas largas e discretas e um grão fino; sem halo nem moldura;
  - a borda: um limiar que varia ao longo do contorno. Manchas grandes mordem fundo, fibras finas correm ao longo da
    borda (o pincel seco) e em alguns trechos o carvão se desfaz num degradê largo em vez de um corte;
  - respingos de tinta perto da borda, dos dois lados;
  - o papel da margem: um cinza-bege gasto, com riscos verticais e manchas de tinta que avançam sobre ele.
Os tamanhos são os da coluna na janela de referência (1920×945): fotografar.mjs medir.

  python ferramentas/prototipos/hud/direcao/ficha/gerar_arte.py
"""

import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
ARTE = os.path.join(AQUI, "arte")
L, A = 348, 879           # a coluna da ficha (fotografar.mjs medir)
MARGEM_L, MARGEM_A = 120, 1100  # a margem: 71 px à vista, o resto passa por baixo da coluna (e repete na altura)
BEIRA = 71                      # onde a coluna começa (fotografar.mjs medir): o papel encosta no rasgo dela
rng = np.random.default_rng(1117)


def ruido(alt, larg, celula_y, celula_x, oitavas=1, queda=0.5):
    """Ruído de valor suave: grades aleatórias ampliadas (bicúbico), somadas em oitavas. Saída em 0..1."""
    total, peso, soma = np.zeros((alt, larg)), 1.0, 0.0
    cy, cx = celula_y, celula_x
    for _ in range(oitavas):
        g = rng.random((max(2, int(alt / cy) + 3), max(2, int(larg / cx) + 3)))
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((larg + int(3 * cx), alt + int(3 * cy)), Image.BICUBIC)
        oy, ox = rng.integers(0, max(1, int(cy))), rng.integers(0, max(1, int(cx)))
        total += peso * (np.asarray(im, float)[oy:oy + alt, ox:ox + larg] / 255.0)
        soma += peso
        peso *= queda
        cy, cx = max(1, cy / 2), max(1, cx / 2)
    return total / soma


def suave(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def superficie():
    ys, xs = np.mgrid[0:A, 0:L].astype(float)
    # a distância até cada lado; qual lado manda (para a direção das fibras)
    dl, dr, dt, db = xs, L - 1 - xs, ys, A - 1 - ys
    d = np.minimum(np.minimum(dl, dr), np.minimum(dt, db))
    vertical = np.minimum(dl, dr) < np.minimum(dt, db)

    # o limiar da borda: base + manchas grandes + médias + fibras (ao longo da borda)
    grande = ruido(A, L, 160, 160, 2)            # as manchas grandes: onde o rasgo morde fundo
    media = ruido(A, L, 46, 46, 2)
    fibra_v = ruido(A, L, 44, 1.6, 2, 0.6)       # alongadas na vertical (bordas da esquerda e da direita)
    fibra_h = ruido(A, L, 1.6, 44, 2, 0.6)       # alongadas na horizontal (em cima e embaixo)
    fibra = np.where(vertical, fibra_v, fibra_h)
    # o lado de fora (a esquerda, junto ao papel) gasta mais que a emenda com o centro (a direita)
    lado = np.where(dl < dr, 1.0, 0.62)
    miuda = ruido(A, L, 3, 3, 1)                  # o serrilhado miúdo do papel rasgado
    limiar = (6 + 30 * suave(0.45, 0.85, grande) + 9 * media + 10 * (fibra - 0.5) + 3 * (miuda - 0.5)) * lado + 2
    # trechos que se desfazem: onde a mancha média é alta, o corte vira um degradê largo; no resto, o corte é seco
    largura = 0.8 + 18 * suave(0.66, 0.92, media) * suave(0.35, 0.7, grande)
    alfa = suave(limiar - 0.5, limiar + largura, d)
    # o pincel seco: falhas finas dentro da faixa da borda (as fibras abrindo o carvão)
    falha = (fibra < 0.32) & (d < limiar + 16) & (d > limiar - 2)
    alfa = np.where(falha, alfa * 0.15, alfa)

    # o carvão: manchas largas e discretas, grão fino; mais escuro perto da borda, sem cor nenhuma (sem halo marrom)
    mancha = ruido(A, L, 120, 120, 3)
    grao = rng.normal(0, 1, (A, L))
    base = np.array([21.0, 20.0, 23.0])
    pincel = ruido(A, L, 9, 70, 2)                  # passadas largas na horizontal, quase invisíveis
    tom = 1 + 0.2 * (mancha - 0.5) + 0.08 * (pincel - 0.5) + 0.04 * grao
    tom *= 1 - 0.22 * (1 - suave(0, 60, d))         # a borda um pouco mais escura, a tinta se acumulando
    rgb = base[None, None, :] * tom[..., None]
    # riscos claros e raros perto da borda (o carvão arranhado), discretos
    risco = (ruido(A, L, 22, 2.5, 2) > 0.84) & (d < limiar + 26) & (ruido(A, L, 40, 40, 1) > 0.55)
    rgb = np.where(risco[..., None], rgb * 1.16 + 3, rgb)

    # respingos de tinta: pontos e gotas escuras e opacas logo depois do corte (dentro e fora)
    respingo = ruido(A, L, 5, 5, 2) > 0.8
    perto = (d > limiar - 10) & (d < limiar + 4) & (grande > 0.45)
    alfa = np.where(respingo & perto, np.maximum(alfa, 0.95), alfa)
    rgb = np.where((respingo & perto)[..., None], rgb * 0.55, rgb)

    out = np.dstack([np.clip(rgb, 0, 255), np.clip(alfa * 255, 0, 255)]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(ARTE, "ficha-superficie.png"), optimize=True)


def margem():
    """A margem de fora: o papel gasto numa faixa encostada no rasgo da coluna (com grão de pontinhos, não riscos), e
    para fora dela a tinta escura, de recorte serrilhado e com respingos. Na referência o papel fica entre a beira da
    tela e o painel; aqui a mesa tem margem, e o papel acompanha o painel."""
    ys, xs = np.mgrid[0:MARGEM_A, 0:MARGEM_L].astype(float)
    # onde o papel acaba (a partir da beira esquerda), variando ao longo da altura
    grande = ruido(MARGEM_A, 1, 140, 1, 2)[:, 0]
    media = ruido(MARGEM_A, 1, 30, 1, 2)[:, 0]
    # a largura do papel: some em alguns trechos (a tinta cobre tudo), abre até ~40 px em outros
    largura = np.maximum(0, 46 * (suave(0.32, 0.85, grande) - 0.18) + 9 * (media - 0.5))
    limite = BEIRA + 12 - largura   # o papel vai de limite até a coluna (que o cobre a partir de BEIRA, com o rasgo)
    miuda = ruido(MARGEM_A, MARGEM_L, 3, 3, 1)
    tinta = suave(-1.5, 1.5, limite[:, None] - xs + 7 * (miuda - 0.5))
    # debaixo da coluna, além da profundidade do rasgo, é tinta: as falhas do pincel mostram escuro, não papel
    tinta = np.maximum(tinta, suave(BEIRA + 26, BEIRA + 34, xs))
    # o papel: bege acinzentado com manchas largas e um grão de pontinhos
    papel = np.array([152.0, 140.0, 121.0])
    mancha = ruido(MARGEM_A, MARGEM_L, 70, 40, 3)
    grao = rng.normal(0, 1, (MARGEM_A, MARGEM_L))
    tom = 0.78 + 0.35 * (mancha - 0.5) + 0.07 * grao
    rgb = papel[None, None, :] * tom[..., None]
    pontos = rng.random((MARGEM_A, MARGEM_L))
    rgb = np.where((pontos < 0.05)[..., None], rgb * 0.45, rgb)        # pontinhos escuros no papel
    # a tinta: quase preta, com variação mínima; respingos escuros sobre o papel perto do recorte e frestas claras
    # (o papel aparecendo) dentro da tinta perto dele
    cor_tinta = np.array([15.0, 14.0, 14.0]) * (1 + 0.12 * (ruido(MARGEM_A, MARGEM_L, 50, 50, 2) - 0.5))[..., None]
    perto = np.abs(xs - limite[:, None])
    respingo = (ruido(MARGEM_A, MARGEM_L, 4, 4, 2) > 0.78) & (perto < 12) & (xs > limite[:, None])
    fresta = (pontos > 0.985) & (perto < 18) & (xs < limite[:, None])
    t = np.clip(tinta + respingo, 0, 1) * (1 - 0.7 * fresta)
    rgb = rgb * (1 - t[..., None]) + cor_tinta * t[..., None]
    out = np.clip(rgb, 0, 255).astype(np.uint8)
    Image.fromarray(out, "RGB").save(os.path.join(ARTE, "margem-papel.png"), optimize=True)


if __name__ == "__main__":
    os.makedirs(ARTE, exist_ok=True)
    superficie()
    margem()
    print("ok:", sorted(os.listdir(ARTE)))
