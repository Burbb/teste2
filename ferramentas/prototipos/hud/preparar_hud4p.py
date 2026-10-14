"""Prepara a família de ícones e o retrato da HUD 4 pixel a partir das quatro folhas anexadas, que ficam intactas em
assets4p/original/ (equipamentos de ferro e itens da bolsa, atalhos, lugares/atributos/recursos, retrato). Só recorta,
limpa o alfa e reduz: nada é redesenhado.

    python ferramentas/prototipos/hud/preparar_hud4p.py      (precisa do Pillow e do numpy)

Saídas em assets4p/:
  pecas/      cada desenho recortado no tamanho original, com o alfa limpo
  exibicao/   o que a página usa: cada desenho num quadrado do tamanho de uso (e o dobro, para telas densas)
  teste/      folhas de conferência em tamanho real sobre a superfície da HUD (reducoes-*.png) e o relatório da
              limpeza (limpeza.txt)

Alfa: como nas folhas da rodada anterior, o fundo é transparente de verdade; sai só a franja escura de alfa até 12
(no máximo 5%) e os pontos soltos longe do desenho (preparar_hud4c.separar). O contorno e as sombras ficam.

Redução: os desenhos imitam pixel art, mas não têm uma grade nativa exata (o "pixel" varia de 6 a 9 px da imagem
conforme a peça, e não cai em 32). Por isso não há um fator inteiro que sirva; a folha de conferência compara, em
tamanho real, a redução macia da rodada anterior com três que mantêm a borda dura (ver `reduzir`)."""

import json
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from preparar_hud4c import area_visivel, escalas, separar, superficie

AQUI = os.path.dirname(os.path.abspath(__file__))
ANEXOS = os.environ.get("ANEXOS", "")  # a pasta das folhas como vieram (só para a primeira cópia)
SAIDA = os.path.join(AQUI, "assets4p")
ORIGINAL = os.path.join(SAIDA, "original")

FOLHAS = {
    "equipamentos-itens.webp": (4, 4, [
        "elmo", "cota", "manopla", "perneiras",
        "botas-ferro", "maca", "espada", "escudo",
        "amuleto", "anel", "bandagem", "pocao",
        "tonico", "antidoto", "bau", "aljava"]),
    "atalhos.webp": (4, 2, [
        "atalho-talentos", "atalho-grimorio", "atalho-inventario", "atalho-mapa",
        "atalho-diario", "atalho-bestiario", "atalho-salvar", "atalho-sair"]),
    "lugares-atributos-recursos.webp": (4, 5, [
        "lugar-vila", "lugar-floresta", "lugar-pantano", "lugar-ruinas",
        "lugar-planicie", "lugar-cidadela", "lugar-caverna", "lugar-montanha",
        "attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder",
        "vital-vida", "vital-vigor", "vital-mana", "vital-foco",
        "moedas", "provisoes", "tocha", "osso"]),
    "retrato.webp": (1, 1, ["retrato-guerreiro"]),
}
ANEXO = {"11.webp": "equipamentos-itens.webp", "12.webp": "atalhos.webp", "13.webp": "lugares-atributos-recursos.webp",
         "14.webp": "retrato.webp"}

# Grupos: o que aparece junto tem a mesma escala visual (normalizado pela área visível). Os itens da bolsa e os do
# equipamento dividem os mesmos nichos de 32 px: um grupo só.
ITENS = ["elmo", "cota", "manopla", "perneiras", "botas-ferro", "maca", "espada", "escudo", "amuleto", "anel", "aljava",
         "bandagem", "pocao", "tonico", "antidoto", "bau", "tocha"]  # a tocha também é item da bolsa (no inventário)
GRUPOS = {  # grupo: (peças, tamanhos na folha de conferência, folga, tamanhos de uso)
    "atalhos": (FOLHAS["atalhos.webp"][2], (32, 36, 40), 1, (32, 36)),  # 36 na doca, 32 na roda da luta
    "itens": (ITENS, (24, 32, 40), 1, (32, 48, 64)),
    "recursos": (["provisoes", "osso", "tocha", "moedas", "pocao", "bandagem", "aljava"], (20, 24, 28), 0, (24,)),  # aljava: flechas
    "vitais": (["vital-vida", "vital-vigor", "vital-mana", "vital-foco"], (16, 20, 24), 0, (20,)),
    "atributos": (["attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder"], (20, 24, 28), 0, (24, 32)),  # 32: Fugir
    "lugares": (["lugar-vila", "lugar-floresta", "lugar-pantano", "lugar-ruinas", "lugar-planicie", "lugar-cidadela",
                 "lugar-caverna", "lugar-montanha"], (32, 40, 48), 0, (32, 40)),
}
METODOS = ("macia", "dura", "paleta", "moda", "vizinho")
METODO_USO = "paleta"
RETRATO = (80, 64)          # a ficha: 80 px, 64 em telas baixas
CABECA = (48, 32)           # o topo (48) e a carta de luta (32): só a cabeça
CORTE_CABECA = (0.2, 0.0, 0.82, 0.74)  # a cabeça no retrato: x0, y0, x1, y1 em fração do recorte (elmo ao queixo)


def blocos(n_origem, n_destino):
    """As bordas (inteiras) de cada pixel de destino na origem."""
    b = np.linspace(0, n_origem, n_destino + 1)
    return np.floor(b[:-1]).astype(int), np.maximum(np.ceil(b[1:]).astype(int), np.floor(b[:-1]).astype(int) + 1)


def reduzir(img, w, h, metodo):
    """`macia`: a média por área com nitidez leve (a da rodada anterior), com borda de alfa em degradê. As outras deixam
    o alfa duro (cada pixel é desenho ou fundo, pela cobertura de metade) e diferem na cor: `dura`, a média da área;
    `paleta`, a média trocada pela cor de verdade mais próxima dentro da área (só cores que o desenho tem, como numa
    pixel art reduzida à mão); `moda`, a cor mais frequente da área. `vizinho`: o pixel mais próximo, sem média."""
    if metodo == "macia":
        from preparar_hud4c import reduzir as macia
        return macia(img, w, h, "area+nitidez")
    if metodo == "vizinho":
        return img.resize((w, h), Image.NEAREST)
    a = np.array(img.convert("RGBA")).astype(np.float64)
    W, H = img.size
    x0, x1 = blocos(W, w)
    y0, y1 = blocos(H, h)
    saida = np.zeros((h, w, 4), np.uint8)
    for j in range(h):
        for i in range(w):
            bloco = a[y0[j]:y1[j], x0[i]:x1[i]].reshape(-1, 4)
            alfa = bloco[:, 3] / 255
            if alfa.mean() < 0.5:
                continue
            cheio = bloco[alfa > 0.5]
            media = (bloco[:, :3] * alfa[:, None]).sum(0) / alfa.sum()
            if metodo == "dura":
                cor = media
            elif metodo == "paleta":
                cor = cheio[np.argmin(((cheio[:, :3] - media) ** 2).sum(1)), :3]
            else:  # moda: a cor (quantizada em 4 bits por canal) mais frequente; dela, a média de verdade
                q = (cheio[:, :3] // 16).astype(int)
                chave = q[:, 0] * 256 + q[:, 1] * 16 + q[:, 2]
                valores, contagem = np.unique(chave, return_counts=True)
                cor = cheio[chave == valores[np.argmax(contagem)], :3].mean(0)
            saida[j, i, :3] = np.clip(np.round(cor), 0, 255)
            saida[j, i, 3] = 255
    return Image.fromarray(saida, "RGBA")


def no_quadrado(peca, fator, lado, metodo, densidade=1):
    lado_px = lado * densidade
    w = max(1, round(peca.width * fator * densidade))
    h = max(1, round(peca.height * fator * densidade))
    q = Image.new("RGBA", (lado_px, lado_px), (0, 0, 0, 0))
    q.alpha_composite(reduzir(peca, w, h, metodo), ((lado_px - w) // 2, (lado_px - h) // 2))
    return q


FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def rotulo(d, xy, texto):
    try:
        f = ImageFont.truetype(FONTE, 12)
    except OSError:
        f = None
    d.text(xy, texto, fill=(200, 192, 176), font=f)


def folha_conferencia(pecas, grupo, nomes, lados, folga):
    """Uma linha por tamanho e método, os desenhos do grupo lado a lado, em tamanho real (sem ampliar), cada um no
    nicho escuro de item da HUD 4 sobre o carvão."""
    passo = max(lados) + 10
    alt = 10 + len(lados) * len(METODOS) * passo
    img = superficie(130 + len(nomes) * passo, alt)
    d = ImageDraw.Draw(img)
    y = 6
    for lado in lados:
        fat = escalas({n: pecas[n] for n in nomes}, lado, folga)
        for m in METODOS:
            rotulo(d, (6, y + lado // 2 - 7), f"{lado}px {m}")
            for i, n in enumerate(nomes):
                x = 130 + i * passo
                d.rectangle((x - 2, y - 2, x + lado + 1, y + lado + 1), fill=(10, 11, 13), outline=(58, 61, 67))
                img.alpha_composite(no_quadrado(pecas[n], fat[n], lado, m), (x, y))
            y += passo
    img.convert("RGB").save(os.path.join(SAIDA, "teste", f"reducoes-{grupo}.png"))


def quadrado(img, caixa=None):
    """O recorte (inteiro, ou a `caixa` em frações) num quadrado transparente, encostado embaixo (o busto apoia na
    base do quadro)."""
    if caixa:
        W, H = img.size
        img = img.crop((round(caixa[0] * W), round(caixa[1] * H), round(caixa[2] * W), round(caixa[3] * H)))
        img = img.crop(img.getbbox())
    lado = max(img.size)
    q = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    q.alpha_composite(img, ((lado - img.width) // 2, lado - img.height))
    return q


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
        for nome, (peca, franja, solto) in zip(nomes, separar(folha, cols, lins, par=0.25)):
            peca.save(os.path.join(SAIDA, "pecas", nome + ".png"))
            pecas[nome] = peca
            relatorio.append(f"{nome:20s} {peca.width:4d}×{peca.height:<4d} área visível {area_visivel(peca):7d}  "
                             f"franja zerada {franja:6d}  pontos soltos {solto:5d}")
    with open(os.path.join(SAIDA, "teste", "limpeza.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio) + "\n")

    for grupo, (nomes, lados, folga, uso) in GRUPOS.items():
        folha_conferencia(pecas, grupo, nomes, lados, folga)
        for lado in uso:
            fat = escalas({n: pecas[n] for n in nomes}, lado, folga)
            for n in nomes:
                for dens, suf in ((1, ""), (2, "@2x")):
                    no_quadrado(pecas[n], fat[n], lado, METODO_USO, dens).save(
                        os.path.join(SAIDA, "exibicao", f"{n}-{lado}{suf}.png"))

    # O índice do que existe (peça: tamanhos), para a HUD no jogo nunca pedir um arquivo que não há.
    indice = {}
    for arq in sorted(os.listdir(os.path.join(SAIDA, "exibicao"))):
        if arq.endswith(".png") and "@2x" not in arq:
            peca, lado = arq[:-4].rsplit("-", 1)
            indice.setdefault(peca, []).append(int(lado))

    # O retrato: o busto inteiro na ficha; só a cabeça no topo e na carta de luta.
    r = pecas["retrato-guerreiro"]
    busto, cabeca = quadrado(r), quadrado(r, CORTE_CABECA)
    for nome, fonte, tamanhos in (("retrato-guerreiro", busto, RETRATO), ("cabeca-guerreiro", cabeca, CABECA)):
        for px in tamanhos:
            for dens, suf in ((1, ""), (2, "@2x")):
                reduzir(fonte, px * dens, px * dens, METODO_USO).save(
                    os.path.join(SAIDA, "exibicao", f"{nome}-{px}{suf}.png"))
            indice.setdefault(nome, []).append(px)
    with open(os.path.join(SAIDA, "exibicao", "indice.js"), "w", encoding="utf-8") as f:
        f.write("// Gerado por preparar_hud4p.py: os tamanhos de cada desenho em exibicao/ (sem os @2x).\n"
                "window.ASSETS4P = " + json.dumps({k: sorted(v) for k, v in sorted(indice.items())}) + ";\n")
    tira = superficie(len(METODOS) * 96 + 20, 4 * 90 + 20)
    for j, (fonte, px) in enumerate(((busto, 80), (busto, 64), (cabeca, 48), (cabeca, 32))):
        for i, m in enumerate(METODOS):
            tira.alpha_composite(reduzir(fonte, px, px, m), (10 + i * 96, 10 + j * 90))
    tira.convert("RGB").save(os.path.join(SAIDA, "teste", "reducoes-retrato.png"))
    print("\n".join(relatorio))


if __name__ == "__main__":
    main()
