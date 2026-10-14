"""Prepara os assets da terceira versão do protótipo (HUD 3) a partir das três folhas de referência, que ficam intactas
em assets3/original/ (molduras, texturas e controles). Só recorta, limpa o alfa, emenda e reduz: nada é redesenhado.

    python ferramentas/prototipos/hud/preparar_hud3.py      (precisa do Pillow e do numpy)

Saídas em assets3/:
  pecas/      cada componente recortado, no tamanho original, com o fundo transparente e o alfa limpo
  exibicao/   o que a página usa, na escala de exibição (1/4): as molduras e os controles em nove partes, as texturas
              sem emenda, a moldura das barras e os preenchimentos separados
  teste/      folhas de conferência: as texturas repetidas lado a lado (antes e depois da emenda) e todas as peças de
              exibição em tamanho real e ampliadas

Escala: as texturas têm o "pixel" de uns 4 pixels da imagem; as molduras e os controles foram desenhados na mesma mão.
Tudo é reduzido 4×, e os cortes das nove partes são múltiplos de 4: um pixel da arte vira um pixel da tela, e as peças
de folhas diferentes ficam na mesma escala. As molduras grandes (barra de uns 8 px na tela) ficam para a estrutura; as
pequenas (4 a 6 px), para o secundário.

Limpeza: as folhas já vêm com o fundo transparente, mas com pontinhos soltos (ruído da compressão) e franja de
semitransparência. Cada peça fica só com a sua região conexa principal (alfa acima de 50%), com o alfa só 0 ou 255."""

import os

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGINAL = os.path.join(AQUI, "assets3", "original")
SAIDA = os.path.join(AQUI, "assets3")
ESCALA = 4

# As caixas (x0, y0, x1, y1) de cada componente nas folhas, achadas pelas regiões conexas do alfa (acima de 50%).
MOLDURAS = {  # folha 1 (molduras.webp)
    "moldura-alta": (63, 19, 540, 844),
    "moldura-larga": (649, 35, 1471, 411),
    "moldura-pequena": (692, 464, 1089, 656),
    "moldura-quadrada": (1189, 440, 1428, 685),
    "moldura-media": (733, 702, 1493, 984),
    "moldura-faixa": (50, 884, 689, 987),
}
TEXTURAS = {  # folha 2 (texturas.webp): quadrados opacos
    "textura-painel": (69, 68, 595, 594),
    "textura-leitura": (659, 68, 1184, 594),
    "textura-espaco": (68, 659, 595, 1184),
    "textura-botao": (659, 659, 1184, 1184),
}
CONTROLES = {  # folha 3 (controles.webp)
    "placa-ferro": (26, 75, 378, 169), "placa-latao": (402, 75, 755, 169),
    "placa-funda": (780, 75, 1133, 169), "placa-gasta": (1158, 75, 1511, 169),
    "aba-ferro": (38, 212, 414, 317), "aba-ferro-2": (441, 212, 815, 317), "aba-latao": (837, 213, 1210, 318),
    "botao-fechar": (1259, 224, 1356, 318), "botao-seta": (1410, 224, 1504, 318),
    "espaco-ferro": (67, 360, 246, 535), "espaco-latao": (294, 360, 472, 535),
    "espaco-cantos": (521, 359, 701, 536), "espaco-indisponivel": (748, 360, 928, 535),
    "rolagem": (992, 346, 1044, 565), "barra-vazia": (40, 586, 1496, 675),
    "barra-vermelha": (46, 702, 755, 752), "barra-laranja": (780, 702, 1490, 752),
    "barra-azul": (46, 770, 755, 822), "barra-roxa": (780, 770, 1489, 822),
    "trilho-latao": (41, 870, 799, 900), "trilho-ferro": (41, 925, 799, 954),
    "tecla-1": (853, 864, 943, 954), "tecla-2": (964, 864, 1055, 954), "tecla-3": (1085, 864, 1174, 954),
    "tecla-4": (1201, 864, 1290, 954), "seta": (1340, 877, 1381, 939), "seta-baixo": (1429, 891, 1492, 932),
}

# As nove partes de cada peça usada como moldura: (canto esquerdo, de cima, direito, de baixo), em pixels da folha,
# múltiplos de 4. As bordas repetem um trecho tirado de `fracao` do comprimento (longe dos rebites do meio).
NOVE = {
    "moldura-alta": (56, 56, 56, 56), "moldura-larga": (56, 56, 56, 56), "moldura-media": (56, 56, 56, 56),
    "moldura-faixa": (40, 40, 40, 40), "moldura-quadrada": (36, 36, 36, 36), "moldura-pequena": (28, 28, 28, 28),
    "placa-ferro": (32, 32, 32, 32), "placa-latao": (32, 32, 32, 32), "placa-funda": (32, 32, 32, 32),
    "placa-gasta": (32, 32, 32, 32),
    "aba-ferro": (72, 60, 72, 24), "aba-ferro-2": (72, 60, 72, 24), "aba-latao": (72, 60, 72, 24),  # o rebite de cima no canto
    "espaco-ferro": (32, 32, 32, 32), "espaco-latao": (32, 32, 32, 32), "espaco-cantos": (40, 40, 40, 40),
    "espaco-indisponivel": (44, 44, 44, 44),
    "barra-vazia": (32, 20, 32, 20),
}
# As barras: o retângulo do preenchimento dentro de cada uma (na folha), achado pela saturação da cor.
PREENCHIMENTO = {
    "barra-vermelha": (66, 711, 735, 741), "barra-laranja": (800, 711, 1470, 741),
    "barra-azul": (66, 780, 735, 809), "barra-roxa": (800, 780, 1468, 809),
}


def regiao_principal(mascara):
    h, w = mascara.shape
    rotulo = np.zeros((h, w), np.int32)
    maior, tam_maior, n = 0, 0, 0
    for y0, x0 in zip(*np.nonzero(mascara)):
        if rotulo[y0, x0]:
            continue
        n += 1
        pilha, tam = [(y0, x0)], 0
        rotulo[y0, x0] = n
        while pilha:
            y, x = pilha.pop()
            tam += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and mascara[yy, xx] and not rotulo[yy, xx]:
                    rotulo[yy, xx] = n
                    pilha.append((yy, xx))
        if tam > tam_maior:
            maior, tam_maior = n, tam
    return rotulo == maior


def recortar(folha, caixa, margem=3):
    x0, y0, x1, y1 = caixa
    a = np.array(folha.crop((x0 - margem, y0 - margem, x1 + 1 + margem, y1 + 1 + margem)).convert("RGBA"))
    fica = regiao_principal(a[:, :, 3] > 128)
    a[:, :, 3] = np.where(fica, 255, 0)
    a[~fica, :3] = 0
    img = Image.fromarray(a, "RGBA")
    return img.crop(img.getbbox())


def reduzir(img, w=None, h=None):
    w = w or round(img.width / ESCALA)
    h = h or round(img.height / ESCALA)
    return img.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")


def nove_partes(peca, cortes, trecho=128, fracao=0.3, miolo=True):
    """Monta a peça em nove partes: os quatro cantos de verdade, um trecho de cada borda (o mais limpo de rebites) e, com
    `miolo`, um trecho do meio. Devolve a imagem reduzida e os cortes na escala de exibição."""
    cl, ct, cr, cb = cortes
    w, h = peca.size
    # O trecho repetido de cada borda: o mais longo que a peça dá (até `trecho`), em múltiplos de 4. Curto, a textura
    # da barra de ferro repetia a cada poucos pixels e virava um pontilhado.
    tx = min(trecho, (w - cl - cr) // 4 * 4)
    ty = min(trecho, (h - ct - cb) // 4 * 4)
    nova = Image.new("RGBA", (cl + tx + cr, ct + ty + cb))
    cola = lambda caixa, onde: nova.alpha_composite(peca.crop(caixa), onde)
    cola((0, 0, cl, ct), (0, 0))
    cola((w - cr, 0, w, ct), (cl + tx, 0))
    cola((0, h - cb, cl, h), (0, ct + ty))
    cola((w - cr, h - cb, w, h), (cl + tx, ct + ty))
    # O trecho de cada borda: onde ele tiver menos rebite (pixel de latão: claro e saturado). Esticado ou repetido, um
    # rebite no trecho virava uma fileira de pontinhos.
    a = np.asarray(peca).astype(int)
    rgb, alfa = a[:, :, :3], a[:, :, 3]
    latao = ((rgb.max(axis=2) - rgb.min(axis=2)) > 60) & (rgb.max(axis=2) > 120) & (alfa > 0)

    def trecho_limpo(perfil, ini, fim, padrao, t):
        melhor, pos = None, padrao
        for p in range(ini, max(ini + 1, fim - t + 1), 2):
            n = perfil[p:p + t].sum()
            if melhor is None or n < melhor or (n == melhor and abs(p - padrao) < abs(pos - padrao)):
                melhor, pos = n, p
        return pos
    por_coluna = latao[:ct, :].sum(axis=0) + latao[h - cb:, :].sum(axis=0)
    por_linha = latao[:, :cl].sum(axis=1) + latao[:, w - cr:].sum(axis=1)
    xb = trecho_limpo(por_coluna, cl, w - cr, min(max(cl, int(w * fracao)), w - cr - tx), tx)
    yb = trecho_limpo(por_linha, ct, h - cb, min(max(ct, int(h * fracao)), h - cb - ty), ty)
    cola((xb, 0, xb + tx, ct), (cl, 0))
    cola((xb, h - cb, xb + tx, h), (cl, ct + ty))
    cola((0, yb, cl, yb + ty), (0, ct))
    cola((w - cr, yb, w, yb + ty), (cl + tx, ct))
    if miolo:
        cola((w // 2 - tx // 2, h // 2 - ty // 2, w // 2 - tx // 2 + tx, h // 2 - ty // 2 + ty), (cl, ct))
    return reduzir(nova), tuple(c // ESCALA for c in cortes)


def sem_emenda(img, horizontal=True, vertical=True):
    """Emenda as bordas: mistura a textura com ela mesma deslocada meia volta, com o peso indo a zero nas bordas. Onde
    a original tem a borda (que não casa com a do outro lado), quem aparece é a deslocada, que ali é miolo contínuo."""
    a = np.asarray(img.convert("RGB")).astype(float)
    h, w = a.shape[:2]
    rolada = np.roll(np.roll(a, h // 2 if vertical else 0, axis=0), w // 2 if horizontal else 0, axis=1)
    sx = 1 - np.abs(np.linspace(-1, 1, w)) if horizontal else np.ones(w)
    sy = 1 - np.abs(np.linspace(-1, 1, h)) if vertical else np.ones(h)
    peso = np.clip(np.outer(sy, sx) * 3, 0, 1)[:, :, None]   # o miolo fica inteiro; só as faixas da borda misturam
    return Image.fromarray((a * peso + rolada * (1 - peso)).round().astype(np.uint8), "RGB")


def ladrilhar(img, n=3, zoom=1):
    w, h = img.size
    out = Image.new("RGB", (w * n, h * n))
    for i in range(n):
        for j in range(n):
            out.paste(img.convert("RGB"), (i * w, j * h))
    return out.resize((w * n * zoom, h * n * zoom), Image.NEAREST)


def main():
    for d in ("pecas", "exibicao", "teste"):
        os.makedirs(os.path.join(SAIDA, d), exist_ok=True)
    folhas = {n: Image.open(os.path.join(ORIGINAL, f"{n}.webp")).convert("RGBA") for n in ("molduras", "texturas", "controles")}
    pecas = {}
    for nome, caixa in MOLDURAS.items():
        pecas[nome] = recortar(folhas["molduras"], caixa)
    for nome, caixa in CONTROLES.items():
        pecas[nome] = recortar(folhas["controles"], caixa)
    for nome, p in pecas.items():
        p.save(os.path.join(SAIDA, "pecas", f"{nome}.png"))

    exib = {}
    for nome, cortes in NOVE.items():
        miolo = not nome.startswith(("moldura", "barra-vazia"))
        img, c = nove_partes(pecas[nome], cortes, miolo=miolo)
        img.save(os.path.join(SAIDA, "exibicao", f"{nome}.png"))
        exib[nome] = (img, c)
        print(f"{nome}: {img.size}, cortes {c}")

    # As barras: a moldura (a vermelha, com o preenchimento apagado) e os quatro preenchimentos, separados. O código
    # controla o valor pela largura do preenchimento, por baixo da moldura; nada de número dentro da imagem.
    vermelha = recortar(folhas["controles"], CONTROLES["barra-vermelha"], margem=0)
    a = np.array(vermelha)
    x0, y0 = CONTROLES["barra-vermelha"][0], CONTROLES["barra-vermelha"][1]
    fx0, fy0, fx1, fy1 = PREENCHIMENTO["barra-vermelha"]
    a[fy0 - y0 - 1: fy1 - y0 + 2, fx0 - x0 - 1: fx1 - x0 + 2, 3] = 0  # um pixel a mais: nada do vermelho na beira
    moldura_barra = Image.fromarray(a, "RGBA")
    img, c = nove_partes(moldura_barra, (24, 12, 24, 12), trecho=128, fracao=0.5, miolo=False)
    img.save(os.path.join(SAIDA, "exibicao", "barra-moldura.png"))
    print("barra-moldura:", img.size, "cortes", c)
    for nome, (fx0, fy0, fx1, fy1) in PREENCHIMENTO.items():
        faixa = folhas["controles"].crop((fx0 + 2, fy0 + 2, fx1 - 1, fy1 - 1)).convert("RGB")
        faixa = sem_emenda(faixa.crop((0, 0, 256, faixa.height)), vertical=False)  # um trecho de 256, emendado
        reduzir(faixa.convert("RGBA"), 64, 7).save(os.path.join(SAIDA, "exibicao", f"{nome.replace('barra', 'enche')}.png"))

    # Texturas: o miolo de cada quadrado (512 da folha), emendado nas bordas e reduzido 4× (ladrilho de 128).
    for nome, (x0, y0, x1, y1) in TEXTURAS.items():
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        bruto = folhas["texturas"].crop((cx - 256, cy - 256, cx + 256, cy + 256)).convert("RGB")
        bruto.save(os.path.join(SAIDA, "pecas", f"{nome}.png"))
        emendada = sem_emenda(bruto)
        reduzir(emendada.convert("RGBA")).convert("RGB").save(os.path.join(SAIDA, "exibicao", f"{nome}.png"))
        ladrilhar(reduzir(bruto.convert("RGBA")), 3, 2).save(os.path.join(SAIDA, "teste", f"{nome}-antes.png"))
        ladrilhar(reduzir(emendada.convert("RGBA")), 3, 2).save(os.path.join(SAIDA, "teste", f"{nome}-depois.png"))

    # Peças pequenas usadas inteiras (sem nove partes), na mesma escala.
    for nome in ("botao-fechar", "botao-seta", "tecla-1", "seta", "seta-baixo", "trilho-latao", "trilho-ferro", "rolagem"):
        reduzir(pecas[nome]).save(os.path.join(SAIDA, "exibicao", f"{nome}.png"))

    # Folha de conferência: todas as peças de exibição, em tamanho real e ampliadas 4×, sobre o fundo escuro.
    arquivos = sorted(f for f in os.listdir(os.path.join(SAIDA, "exibicao")) if f.endswith(".png") and not f.startswith("textura"))
    imgs = [Image.open(os.path.join(SAIDA, "exibicao", f)).convert("RGBA") for f in arquivos]
    larg = max(i.width for i in imgs) * 5 + 40
    alt = sum(i.height * 4 + 12 for i in imgs) + 12
    folha = Image.new("RGBA", (larg, alt), (18, 17, 16, 255))
    y = 12
    for i in imgs:
        folha.alpha_composite(i, (12, y))
        folha.alpha_composite(i.resize((i.width * 4, i.height * 4), Image.NEAREST), (24 + i.width, y))
        y += i.height * 4 + 12
    folha.save(os.path.join(SAIDA, "teste", "pecas-exibicao.png"))


if __name__ == "__main__":
    main()
