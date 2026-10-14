"""Recorta as peças da imagem de referência (assets/original/referencia.webp, que fica intacta) e prepara as
versões de exibição da segunda tentativa da ficha. Só recorta, limpa o alfa e reduz: nenhuma peça é redesenhada.

    python ferramentas/prototipos/hud/preparar_assets.py      (precisa do Pillow e do numpy)

Saídas em assets/:
  pecas/<nome>.png        cada peça no tamanho original, com o fundo transparente e o alfa limpo
  exibicao/...            o que a página usa: a moldura em nove partes, o retrato e os ícones nos tamanhos de uso
  teste/reducoes.png      os ícones em 16, 24, 32, 40 e 48 px, para ver onde a leitura se perde

O alfa da referência já é transparente no fundo, mas traz uns 2.600 pontinhos soltos (o ruído da compressão) e uma
franja de semitransparência escura em volta das peças. Cada peça fica só com a sua região conexa principal; o alfa vira
duro (opaco a partir de 50%), como na pixel art do jogo; e a redução é feita com o alfa pré-multiplicado, para a borda
não puxar cor do vazio (sem halo)."""

import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEM = os.path.join(AQUI, "assets", "original", "referencia.webp")
SAIDA = os.path.join(AQUI, "assets")

# Caixas (x0, y0, x1, y1) de cada peça na referência de 1536×1024, achadas pelas regiões conexas do alfa.
PECAS = {
    "moldura": (40, 20, 785, 1000),
    "retrato": (930, 20, 1365, 505),
    "espada": (885, 520, 1130, 762),
    "escudo": (1190, 505, 1415, 762),
    "anel": (925, 790, 1098, 970),
    "pocao": (1210, 758, 1414, 984),
}


def regiao_principal(alfa):
    """A maior região conexa (vizinhança de 4) dos texels com algum alfa: tira os pontinhos soltos."""
    m = alfa > 0
    h, w = m.shape
    rotulo = np.zeros((h, w), np.int32)
    maior, tam_maior, n = 0, 0, 0
    for y0, x0 in zip(*np.nonzero(m)):
        if rotulo[y0, x0]:
            continue
        n += 1
        pilha, tam = [(y0, x0)], 0
        rotulo[y0, x0] = n
        while pilha:
            y, x = pilha.pop()
            tam += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not rotulo[yy, xx]:
                    rotulo[yy, xx] = n
                    pilha.append((yy, xx))
        if tam > tam_maior:
            maior, tam_maior = n, tam
    return rotulo == maior


def limpar(img):
    a = np.array(img.convert("RGBA"))
    principal = regiao_principal(a[:, :, 3])
    alfa = np.where(principal & (a[:, :, 3] >= 128), 255, 0).astype(np.uint8)
    a[:, :, 3] = alfa
    a[alfa == 0, :3] = 0  # o vazio não guarda cor nenhuma
    out = Image.fromarray(a, "RGBA")
    return out.crop(out.getbbox())


def reduzir(img, w, h):
    """Redução com o alfa pré-multiplicado (sem halo), em área (Lanczos): a borda fica suave, não suja."""
    return img.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")


def caber(img, lado):
    """Reduz para caber num quadrado de `lado`, mantendo a proporção, centrado num quadro transparente."""
    f = lado / max(img.size)
    w, h = max(1, round(img.width * f)), max(1, round(img.height * f))
    quadro = Image.new("RGBA", (lado, lado))
    quadro.alpha_composite(reduzir(img, w, h), ((lado - w) // 2, (lado - h) // 2))
    return quadro


def moldura_nove(moldura, canto, trecho, escala):
    """A moldura em nove partes: os quatro cantos de verdade (o ornamento, `canto` texels da referência) e, nas bordas,
    um trecho liso de cada lado (sem rebite), tirado do meio do caminho entre dois rebites. O miolo fica vazio: a
    superfície é da interface. Reduzida por `escala`, para o CSS cortar em nove (border-image) sem esticar canto."""
    w, h = moldura.size
    c, t = canto, trecho
    lado = 2 * c + t
    nova = Image.new("RGBA", (lado, lado))
    nova.alpha_composite(moldura.crop((0, 0, c, c)), (0, 0))
    nova.alpha_composite(moldura.crop((w - c, 0, w, c)), (c + t, 0))
    nova.alpha_composite(moldura.crop((0, h - c, c, h)), (0, c + t))
    nova.alpha_composite(moldura.crop((w - c, h - c, w, h)), (c + t, c + t))
    meio_x = w // 2
    nova.alpha_composite(moldura.crop((meio_x - t // 2, 0, meio_x - t // 2 + t, c)), (c, 0))          # topo: sem rebite
    nova.alpha_composite(moldura.crop((meio_x - t // 2, h - c, meio_x - t // 2 + t, h)), (c, c + t))  # pé
    y = int(h * 0.28)  # entre o rebite de perto do canto (12%) e o do meio (42%)
    nova.alpha_composite(moldura.crop((0, y, c, y + t)), (0, c))                                       # esquerda
    nova.alpha_composite(moldura.crop((w - c, y, w, y + t)), (c + t, c))                               # direita
    lado_final = round(lado / escala)
    return reduzir(nova, lado_final, lado_final), round(c / escala)


def main():
    ref = Image.open(ORIGEM).convert("RGBA")
    for d in ("pecas", "exibicao", "teste"):
        os.makedirs(os.path.join(SAIDA, d), exist_ok=True)
    pecas = {}
    for nome, caixa in PECAS.items():
        pecas[nome] = limpar(ref.crop(caixa))
        pecas[nome].save(os.path.join(SAIDA, "pecas", f"{nome}.png"))
        print(nome, pecas[nome].size)

    # A escala de exibição: a arte da referência tem o "pixel" com uns 4 texels; reduzida 4×, um pixel dela vira um
    # pixel da tela. A moldura e o retrato ficam nessa escala (a mesma para os dois).
    ESCALA = 4
    nove, corte = moldura_nove(pecas["moldura"], canto=96, trecho=48, escala=ESCALA)
    nove.save(os.path.join(SAIDA, "exibicao", "moldura-nove.png"))
    print("moldura em nove partes:", nove.size, "corte", corte)
    r = pecas["retrato"]
    reduzir(r, round(r.width / ESCALA), round(r.height / ESCALA)).save(os.path.join(SAIDA, "exibicao", "retrato.png"))

    # Os ícones são desenhados bem maiores que um espaço de item (uns 200 texels): não há escala comum que os ponha
    # num espaço de 40 px. Vão para o tamanho de uso de cada lugar: 32 nos espaços (e na bolsa) e 24 nos atributos
    # (a 16, a espada vira um risco: ver teste/reducoes.png).
    for nome in ("espada", "escudo", "anel", "pocao"):
        caber(pecas[nome], 32).save(os.path.join(SAIDA, "exibicao", f"{nome}-32.png"))
    for nome in ("espada", "escudo"):  # os do Ataque e da Defesa
        caber(pecas[nome], 24).save(os.path.join(SAIDA, "exibicao", f"{nome}-24.png"))

    # A folha de teste das reduções: cada ícone em 16, 24, 32, 40 e 48 px, lado a lado, sobre o fundo da ficha.
    tamanhos = (16, 24, 32, 40, 48)
    folha = Image.new("RGBA", (sum(tamanhos) + 12 * len(tamanhos) + 12, 4 * 60 + 12), (18, 17, 16, 255))
    for i, nome in enumerate(("espada", "escudo", "anel", "pocao")):
        x = 12
        for lado in tamanhos:
            folha.alpha_composite(caber(pecas[nome], lado), (x, 12 + i * 60 + (48 - lado)))
            x += lado + 12
    folha.save(os.path.join(SAIDA, "teste", "reducoes.png"))


if __name__ == "__main__":
    main()
