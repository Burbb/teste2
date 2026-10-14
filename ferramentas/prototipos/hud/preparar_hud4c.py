"""Prepara os ícones e o retrato da HUD 4 completa a partir das quatro folhas anexadas, que ficam intactas em
assets4c/original/ (lugares e atributos, equipamentos e recursos, atalhos, retrato). Só recorta, limpa o alfa e
reduz: nada é redesenhado.

    python ferramentas/prototipos/hud/preparar_hud4c.py      (precisa do Pillow e do numpy)

Saídas em assets4c/:
  pecas/      cada desenho recortado no tamanho original, com o alfa limpo
  exibicao/   o que a página usa: cada desenho num quadrado do tamanho de uso (e o dobro, para telas densas)
  teste/      folhas de conferência: as reduções lado a lado sobre a superfície da HUD, em tamanho real
              (reducoes-*.png), e o relatório da limpeza (limpeza.txt)

Alfa: as folhas já vêm com o fundo transparente (alfa 0). O que sobra é (1) a parte opaca, que a compressão deixou em
250 a 253 em vez de 255; (2) uma franja escura de alfa 1 a 12 (no máximo 5% de opacidade) em volta de cada desenho e
espalhada pelo fundo em pontinhos, resto do recorte de quem gerou a imagem; (3) a borda de antisserrilhado do próprio
desenho (alfa 13 a 249). A limpeza leva o opaco a 255, zera a franja de até 12 e os pontinhos soltos longe do desenho, e
mantém a borda inteira: os riscos de velocidade da bota, o golpe da espada, as faíscas da chama e a sombra do chão dos
lugares são do desenho e ficam.

Tamanho: cada grupo (atalhos, equipamentos, lugares, atributos) é normalizado pela área visível (alfa acima de 50%),
não pela caixa do recorte: um desenho comprido (a tocha, a espada na diagonal) e um compacto (o escudo, as moedas)
ficam com peso parecido. Nenhum passa do quadrado de uso menos a folga."""

import os
import shutil

import numpy as np
from PIL import Image, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
ANEXOS = os.environ.get("ANEXOS", "")  # a pasta das folhas como vieram (só para a primeira cópia)
SAIDA = os.path.join(AQUI, "assets4c")
ORIGINAL = os.path.join(SAIDA, "original")

# folha: (colunas, linhas, nomes na ordem de leitura)
FOLHAS = {
    "lugares-atributos.webp": (4, 3, [
        "lugar-vila", "lugar-floresta", "lugar-pantano", "lugar-ruinas",
        "lugar-cripta", "lugar-montanha", "attr-ataque", "attr-defesa",
        "attr-agilidade", "attr-poder", "vital-vida", "vital-vigor"]),
    "equipamentos-recursos.webp": (4, 4, [
        "espada", "escudo", "capuz", "armadura-couro",
        "calca-couro", "botas", "adaga", "amuleto",
        "anel-azul", "anel-vermelho", "bandagem", "pocao",
        "moedas", "provisoes", "tocha", "aljava"]),
    "atalhos.webp": (4, 2, [
        "atalho-talentos", "atalho-grimorio", "atalho-inventario", "atalho-mapa",
        "atalho-diario", "atalho-bestiario", "atalho-salvar", "atalho-sair"]),
    "retrato.webp": (1, 1, ["retrato-guerreiro"]),
}
# Nomes dos anexos desta rodada (7 a 10), para a primeira cópia.
ANEXO = {"7.webp": "lugares-atributos.webp", "8.webp": "equipamentos-recursos.webp", "9.webp": "atalhos.webp",
         "10.webp": "retrato.webp"}

FRANJA = 12     # alfa até aqui (5%) é a franja do recorte, não desenho
OPACO = 240     # alfa daqui para cima é opaco (a compressão deixou 250 a 253)

# Grupos e tamanhos de uso (lado do quadrado em px de CSS) que entram na folha de conferência. A folga é o respiro em
# volta do desenho dentro do quadrado.
GRUPOS = {
    "atalhos": ([n for n in FOLHAS["atalhos.webp"][2]], (24, 32, 40), 1),
    "equipamentos": (["espada", "escudo", "capuz", "armadura-couro", "calca-couro", "botas", "amuleto", "anel-azul",
                      "anel-vermelho", "adaga", "aljava"], (24, 32, 40), 1),
    "bolsa": (["pocao", "bandagem", "tocha"], (24, 32, 40), 1),
    "recursos": (["provisoes", "tocha", "moedas", "pocao", "bandagem", "vital-vida", "vital-vigor"], (16, 20, 24), 0),
    "atributos": (["attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder"], (16, 20, 24), 0),
    "lugares": (["lugar-vila", "lugar-floresta", "lugar-pantano", "lugar-ruinas", "lugar-cripta", "lugar-montanha"],
                (32, 40, 48), 0),
}
# O que a página usa: grupo -> tamanhos escolhidos na folha de conferência (ver o LEIA-ME).
USO = {"atalhos": (32, 36), "equipamentos": (32, 48, 64), "bolsa": (32,), "recursos": (20, 24), "atributos": (20, 24),
       "lugares": (32, 40)}
# A média por área com um realce leve: a média sozinha deixa tudo macio; o Lanczos acende um anel em volta das bordas
# fortes (o aço da espada, o ouro dos anéis); o vizinho mais próximo serrilha e perde as linhas finas (a corrente do
# amuleto, os galhos do pântano).
METODO_USO = "area+nitidez"
RETRATO = (80, 64)  # o quadro da ficha: 80 px, 64 em telas baixas


def regioes(mascara):
    """Rótulos das regiões conexas (vizinhança de 4) e o tamanho de cada uma."""
    h, w = mascara.shape
    rotulo = np.zeros((h, w), np.int32)
    tamanhos = [0]
    for y0, x0 in zip(*np.nonzero(mascara)):
        if rotulo[y0, x0]:
            continue
        n = len(tamanhos)
        pilha, tam = [(y0, x0)], 0
        rotulo[y0, x0] = n
        while pilha:
            y, x = pilha.pop()
            tam += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < h and 0 <= xx < w and mascara[yy, xx] and not rotulo[yy, xx]:
                    rotulo[yy, xx] = n
                    pilha.append((yy, xx))
        tamanhos.append(tam)
    return rotulo, tamanhos


def caixa(m):
    ys, xs = np.nonzero(m)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def dilatar(m, raio):
    img = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * raio + 1))
    return np.array(img) > 0


def separar(folha, cols, lins):
    """Os desenhos de uma folha, um por célula da grade, com o alfa limpo, e o que saiu de cada um. As regiões conexas
    são achadas na folha inteira (um desenho pode passar um pouco da sua célula) e cada uma vai para a célula do seu
    centro; ficam a principal e as menores perto dela (faíscas, riscos de velocidade). O resto são pontos soltos."""
    a = np.array(folha)
    alfa = a[:, :, 3].astype(int)
    rot, tam = regioes(alfa > 40)
    cw, ch = folha.width / cols, folha.height / lins
    por_celula = {}
    for n in range(1, len(tam)):
        if tam[n] < 30:
            continue
        ys, xs = np.nonzero(rot == n)
        cel = (min(int(ys.mean() // ch), lins - 1), min(int(xs.mean() // cw), cols - 1))
        por_celula.setdefault(cel, []).append((tam[n], n, (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)))
    saida = []
    for lin in range(lins):
        for col in range(cols):
            regs = sorted(por_celula.get((lin, col), []), reverse=True)
            _, principal, (x0, y0, x1, y1) = regs[0]
            folga = round(0.06 * max(cw, ch))
            fica = rot == principal
            for _, n, (bx0, by0, bx1, by1) in regs[1:]:
                if bx1 >= x0 - folga and bx0 <= x1 + folga and by1 >= y0 - folga and by0 <= y1 + folga:
                    fica |= rot == n
            # a borda de antisserrilhado (alfa entre a franja e 40) encosta no desenho: entra com uma dilatação curta
            X0, Y0 = max(0, x0 - 2 * folga), max(0, y0 - 2 * folga)
            X1, Y1 = min(folha.width, x1 + 2 * folga), min(folha.height, y1 + 2 * folga)
            sub_fica = dilatar(fica[Y0:Y1, X0:X1], 3) & (alfa[Y0:Y1, X0:X1] > FRANJA)
            sub_a = a[Y0:Y1, X0:X1].copy()
            sub_alfa = alfa[Y0:Y1, X0:X1]
            # o que é de outra célula não conta como resto desta
            outro = (rot[Y0:Y1, X0:X1] > 0) & ~fica[Y0:Y1, X0:X1] & np.isin(
                rot[Y0:Y1, X0:X1], [r[1] for k, v in por_celula.items() if k != (lin, col) for r in v[:1]])
            franja = int(((sub_alfa > 0) & (sub_alfa <= FRANJA)).sum())
            solto = int(((sub_alfa > FRANJA) & ~sub_fica & ~dilatar(outro, 3)).sum())
            sub_a[:, :, 3] = np.where(sub_fica, np.where(sub_alfa >= OPACO, 255, sub_alfa), 0).astype(np.uint8)
            sub_a[~sub_fica, :3] = 0
            img = Image.fromarray(sub_a, "RGBA")
            saida.append((img.crop(img.getbbox()), franja, solto))
    return saida


def area_visivel(img):
    return int((np.array(img)[:, :, 3] > 128).sum())


def escalas(pecas, lado, folga):
    """Fator de cada peça para o quadrado `lado`: a mesma área visível para todas, sem nenhuma sair do quadrado. O alvo
    é a mediana do que cada uma alcança cabendo no quadrado: as compridas (que batem na borda antes) ficam um pouco
    abaixo, as compactas descem até ela."""
    util = lado - 2 * folga
    cabe = {n: util / max(p.size) for n, p in pecas.items()}
    lado_visivel = {n: (area_visivel(p) ** 0.5) * cabe[n] for n, p in pecas.items()}
    alvo = float(np.percentile(list(lado_visivel.values()), 50))
    return {n: min(cabe[n], alvo / area_visivel(p) ** 0.5) for n, p in pecas.items()}


def reduzir(img, w, h, metodo):
    """A redução com alfa pré-multiplicado (sem halo escuro na borda). `area`: média da área de cada pixel de destino,
    a que menos inventa; `lanczos`: mais contraste, com algum anel em volta das bordas fortes; `area+nitidez`: a média
    com um realce leve; `vizinho`: o pixel mais próximo, serrilhado (só para comparar)."""
    if metodo == "vizinho":
        return img.resize((w, h), Image.NEAREST)
    pm = img.convert("RGBa")
    if metodo == "lanczos":
        r = pm.resize((w, h), Image.LANCZOS)
    else:
        r = pm.resize((w, h), Image.BOX)
    r = r.convert("RGBA")
    if metodo == "area+nitidez":
        cor = r.convert("RGB").filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
        r = Image.merge("RGBA", (*cor.split(), r.getchannel("A")))
    return r


def no_quadrado(peca, fator, lado, metodo, densidade=1):
    lado_px = lado * densidade
    w = max(1, round(peca.width * fator * densidade))
    h = max(1, round(peca.height * fator * densidade))
    q = Image.new("RGBA", (lado_px, lado_px), (0, 0, 0, 0))
    q.alpha_composite(reduzir(peca, w, h, metodo), ((lado_px - w) // 2, (lado_px - h) // 2))
    return q


def superficie(w, h):
    """O carvão da HUD 4 (textura de painel da HUD 3 com o véu escuro), para conferir sobre o fundo de verdade."""
    t = Image.open(os.path.join(AQUI, "assets3", "exibicao", "textura-painel.png")).convert("RGB")
    s = Image.new("RGB", (w, h))
    for y in range(0, h, t.height):
        for x in range(0, w, t.width):
            s.paste(t, (x, y))
    veu = Image.new("RGB", (w, h), (15, 16, 19))
    return Image.blend(s, veu, 0.55).convert("RGBA")


def folha_conferencia(pecas, grupo, nomes, lados, folga):
    """Uma linha por tamanho e método, os desenhos do grupo lado a lado, em tamanho real (sem ampliar)."""
    metodos = ("area", "area+nitidez", "lanczos", "vizinho")
    passo = max(lados) + 10
    larg = 120 + len(nomes) * passo
    alt = 10 + len(lados) * len(metodos) * passo
    img = superficie(larg, alt)
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    y = 6
    for lado in lados:
        fat = escalas({n: pecas[n] for n in nomes}, lado, folga)
        for m in metodos:
            d.text((6, y + lado // 2 - 6), f"{lado}px {m}", fill=(200, 192, 176))
            for i, n in enumerate(nomes):
                x = 120 + i * passo
                # o espaço de item da HUD 4 (fundo fundo, fio de aresta) atrás de cada desenho
                d.rectangle((x - 2, y - 2, x + lado + 1, y + lado + 1), fill=(10, 11, 13), outline=(58, 61, 67))
                img.alpha_composite(no_quadrado(pecas[n], fat[n], lado, m), (x, y))
            y += passo
    img.convert("RGB").save(os.path.join(SAIDA, "teste", f"reducoes-{grupo}.png"))


def main():
    for p in ("original", "pecas", "exibicao", "teste"):
        os.makedirs(os.path.join(SAIDA, p), exist_ok=True)
    for velho in os.listdir(os.path.join(SAIDA, "exibicao")):  # sem sobras de tamanhos que saíram de uso
        os.remove(os.path.join(SAIDA, "exibicao", velho))
    if ANEXOS:
        for de, para in ANEXO.items():
            shutil.copyfile(os.path.join(ANEXOS, de), os.path.join(ORIGINAL, para))

    pecas, relatorio = {}, []
    for arquivo, (cols, lins, nomes) in FOLHAS.items():
        folha = Image.open(os.path.join(ORIGINAL, arquivo)).convert("RGBA")
        for nome, (peca, franja, solto) in zip(nomes, separar(folha, cols, lins)):
            peca.save(os.path.join(SAIDA, "pecas", nome + ".png"))
            pecas[nome] = peca
            relatorio.append(f"{nome:20s} {peca.width:4d}×{peca.height:<4d} área visível {area_visivel(peca):7d}  "
                             f"franja zerada {franja:6d}  pontos soltos {solto:5d}")
    with open(os.path.join(SAIDA, "teste", "limpeza.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio) + "\n")

    for grupo, (nomes, lados, folga) in GRUPOS.items():
        folha_conferencia(pecas, grupo, nomes, lados, folga)
        for lado in USO[grupo]:
            fat = escalas({n: pecas[n] for n in nomes}, lado, folga)
            for n in nomes:
                for dens, suf in ((1, ""), (2, "@2x")):
                    no_quadrado(pecas[n], fat[n], lado, METODO_USO, dens).save(
                        os.path.join(SAIDA, "exibicao", f"{n}-{lado}{suf}.png"))

    # O retrato: o quadro inteiro (busto), reduzido pela área. A arte tem um pixel de ~4,9 px (256 de lado).
    r = pecas["retrato-guerreiro"]
    lado = max(r.size)
    q = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    q.alpha_composite(r, ((lado - r.width) // 2, lado - r.height))
    for px in RETRATO:
        for dens, suf in ((1, ""), (2, "@2x")):
            reduzir(q, px * dens, px * dens, METODO_USO).save(
                os.path.join(SAIDA, "exibicao", f"retrato-guerreiro-{px}{suf}.png"))
    tira = superficie(4 * 96 + 20, 2 * 96 + 20)
    for j, px in enumerate(RETRATO):
        for i, m in enumerate(("area", "area+nitidez", "lanczos", "vizinho")):
            tira.alpha_composite(reduzir(q, px, px, m), (10 + i * 96, 10 + j * 96))
    tira.convert("RGB").save(os.path.join(SAIDA, "teste", "reducoes-retrato.png"))
    print("\n".join(relatorio))


if __name__ == "__main__":
    main()
