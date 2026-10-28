"""Os objetos que dão à cabana o ar de botica de curandeira: o que ela guarda, destila e pendura (pedido do Jean em
28/10/2026: mais personalidade, uma aura de mandinga e de alquimia com coisas naturais, sem virar bruxaria nem
laboratório de mago). Tudo natural e do ofício: potes de vidro com o que se guarda dentro (a cobra em líquido, as
sanguessugas, a raiz, os cogumelos), tinturas com etiqueta, velas escorridas, o alambique sobre a lamparina, o crânio de
cervo, a estrela de palha de proteção sobre a porta e o amuleto de osso e penas. Cada objeto é construído na grade:
o vidro pela borda e por um brilho de um pixel, o conteúdo por duas ou três manchas de forma reconhecível."""

C = {
    "vidro": "#3a4a46", "vidroBorda": "#566862", "vidroBrilho": "#b8c8c0",
    "ambar": "#8a5a1e", "ambarLuz": "#b07a2a", "turva": "#2a3a26", "turvaLuz": "#3e5236", "clara": "#4e5e50",
    "rubi": "#6a1a1e", "rubiLuz": "#8e2a2a", "mel": "#9a7024",
    "cobra": "#4a4e22", "cobraLuz": "#6e7232", "cobraEsc": "#2c2e12",
    "sanguessuga": "#141410", "raiz": "#8a6a48", "raizLuz": "#a88660", "raizEsc": "#5e4630",
    "cogumelo": "#a89878", "cogumeloLuz": "#c8b898", "cogumeloEsc": "#6e5e48",
    "osso": "#b8ae96", "ossoLuz": "#d6ccb2", "ossoEsc": "#7e765f", "galhada": "#9a8c70",
    "cera": "#c8bc96", "ceraEsc": "#948a6a", "pavio": "#2a2018",
    "rotulo": "#b0a282", "rotuloEsc": "#7e7258", "barbante": "#6e6450",
    "pena": "#5a5048", "penaLuz": "#8a7e70",
    "baga": "#6a2420", "bagaLuz": "#8e3428", "bagaEsc": "#45160f",
}


def pote(px, x, base, w, h, liquido=None, nivel=0.7, tampa="rolha", rotulo=True):
    """Um pote de vidro de pé na tábua (`base` é a linha da tábua): a borda e o fundo um tom acima, o líquido até o
    `nivel`, a tampa (rolha ou pano amarrado), a etiqueta de pergaminho e o brilho de um pixel. Devolve o miolo
    (x0, y0, x1, y1) para o conteúdo."""
    y0 = base - h
    px(x, y0 + 1, w, h - 1, "vidro")
    if liquido:
        top = y0 + 1 + round((h - 2) * (1 - nivel))
        px(x + 1, top, w - 2, base - 1 - top, liquido)
        px(x + 1, top, w - 2, 1, liquido + "Luz" if liquido + "Luz" in C else liquido)
    px(x, y0 + 1, 1, h - 1, "vidroBorda")
    px(x + w - 1, y0 + 1, 1, h - 1, "vidroBorda")
    px(x, base - 1, w, 1, "vidroBorda")
    px(x + 1, y0 + 2, 1, max(1, h // 3), "vidroBrilho")  # o brilho
    if tampa == "rolha":
        px(x + 1, y0 - 1, w - 2, 2, "raizEsc")
        px(x + 1, y0 - 1, w - 2, 1, "raiz")
    else:  # o pano amarrado com barbante
        px(x - 1, y0, w + 2, 2, "rotulo")
        px(x, y0 - 1, w, 1, "rotulo")
        px(x, y0 + 1, w, 1, "barbante")
    if rotulo and w >= 6:
        px(x + 2, base - 1 - h // 2, w - 4, 2, "rotulo")
        px(x + 2, base - h // 2, w - 4, 1, "rotuloEsc")
    return x + 1, y0 + 2, x + w - 2, base - 2


def cobra(px, miolo):
    """A cobra enrolada no líquido: duas voltas e a cabeça por cima."""
    x0, y0, x1, y1 = miolo
    cx = (x0 + x1) // 2
    for k, y in enumerate((y1 - 1, y1 - 3, y1 - 5)):
        px(x0 + 1, y, x1 - x0 - 1, 1, "cobra")
        px(x0 + 1 + k % 2, y, 2, 1, "cobraLuz")
        px.p(x1 - 1, y + 1, "cobraEsc")
        px.p(x0 + 1, y + 1, "cobraEsc")
    px(cx - 1, y1 - 7, 3, 2, "cobra")   # a cabeça
    px.p(cx - 1, y1 - 7, "cobraLuz")
    px.p(cx + 1, y1 - 6, "cobraEsc")


def sanguessugas(px, miolo):
    """As sanguessugas na água turva: três vírgulas escuras."""
    x0, y0, x1, y1 = miolo
    for (dx, dy) in [(0, 4), (2, 1), (1, 6)]:
        x, y = x0 + dx, y0 + dy
        px(x, y, 2, 1, "sanguessuga")
        px.p(x + 2, y + 1, "sanguessuga")


def raiz(px, miolo):
    """A raiz bifurcada como um corpinho (a mandrágora do povo): o tronco, as duas pernas e as folhas saindo por cima."""
    x0, y0, x1, y1 = miolo
    cx = (x0 + x1) // 2
    px(cx - 1, y0 + 2, 2, 4, "raiz")
    px.p(cx - 1, y0 + 2, "raizLuz")
    px.p(cx - 2, y1, "raizEsc")
    px.p(cx - 2, y1 - 1, "raiz")
    px.p(cx + 1, y1, "raizEsc")
    px.p(cx + 1, y1 - 1, "raiz")
    px.p(cx - 2, y0 + 3, "raizEsc")  # os braços
    px.p(cx + 1, y0 + 3, "raizEsc")


def cogumelos(px, miolo):
    """Cogumelos secos empilhados: os chapéus claros, o pé embaixo."""
    x0, y0, x1, y1 = miolo
    for k, y in enumerate((y1 - 1, y1 - 4, y1 - 7)):
        if y < y0:
            break
        x = x0 + (k % 2)
        px(x, y, 3, 1, "cogumeloLuz")
        px(x, y + 1, 3, 1, "cogumeloEsc")
        px.p(x + 1, y + 2, "cogumelo")


def frasco(px, x, base, h, liquido):
    """Um frasco estreito de tintura: o gargalo, a rolha e o líquido de cor funda."""
    px(x, base - h + 3, 4, h - 3, liquido)
    px(x, base - h + 3, 1, h - 3, "vidroBorda")
    px(x + 1, base - h + 4, 1, 2, "vidroBrilho")
    px(x + 1, base - h + 1, 2, 2, "vidro")
    px(x + 1, base - h, 2, 1, "raiz")
    px(x, base - 4, 4, 2, "rotulo")


def vela(px, x, base, h):
    """Uma vela gasta com a cera escorrida pela lateral."""
    px(x, base - h, 3, h, "cera")
    px(x + 2, base - h, 1, h, "ceraEsc")
    px.p(x - 1, base - 1, "cera")      # a poça de cera
    px.p(x + 3, base - 2, "ceraEsc")   # o pingo escorrido
    px.p(x + 1, base - h - 1, "pavio")


def prateleiras(px):
    """As duas tábuas da botica: em cima, a cobra no âmbar, as sanguessugas, a raiz e uma vela; embaixo, os cogumelos, as
    tinturas (rubi, mel e turva), o crânio de passarinho e o maço de penas num copo."""
    for y in (24, 38):
        px(178, y, 44, 2, "madeira")
        px(178, y, 44, 1, "madeiraLuz")
        for xx in (181, 216):
            px(xx, y + 2, 2, 4, "madeiraEsc")
            px(xx + 1, y + 2, 1, 1, "madeira")
    cobra(px, pote(px, 179, 24, 10, 14, "ambar", 0.85))
    sanguessugas(px, pote(px, 191, 24, 7, 10, "turva", 0.9, tampa="pano", rotulo=False))
    raiz(px, pote(px, 200, 24, 7, 11, "clara", 0.75, rotulo=False))
    vela(px, 210, 24, 6)  # a acesa (a chama vem depois do escuro, em desenho.fundo)
    vela(px, 215, 24, 4)
    cogumelos(px, pote(px, 179, 38, 7, 10, None, tampa="pano", rotulo=False))
    frasco(px, 188, 38, 9, "rubi")
    frasco(px, 193, 38, 7, "mel")
    frasco(px, 198, 38, 8, "turva")
    # o crânio de passarinho deitado: a caixa, a órbita e o bico
    px(204, 35, 4, 3, "osso")
    px(204, 35, 4, 1, "ossoLuz")
    px.p(205, 36, "ossoEsc")
    px(208, 37, 3, 1, "osso")
    px.p(210, 36, "ossoEsc")
    # o copo de barro com as penas
    px(213, 33, 4, 5, "barro")
    px(213, 33, 1, 5, "barroLuz")
    for (x, y, c) in [(213, 28, "pena"), (214, 27, "penaLuz"), (215, 29, "pena"), (216, 28, "penaLuz"), (214, 30, "pena"),
                      (215, 31, "pena"), (213, 29, "penaLuz"), (216, 30, "pena")]:
        px.p(x, y, c)
    # o ramo pendurado na ponta da tábua de baixo
    for k in range(9):
        px(220 + (k % 2), 40 + k, 2, 1, "erva" if k % 3 else "ervaLuz")


def armario(px):
    """O armário da direita: potes de barro com etiqueta, um pote de vidro com o sapo seco e o cesto no alto."""
    px(298, 10, 2, 72, "madeira")
    px(298, 10, 1, 72, "madeiraLuz")
    for y in (26, 44, 62):
        px(298, y, 22, 2, "madeira")
        px(298, y, 22, 1, "madeiraLuz")
    for y, potes in [(26, [(301, 7, 5), (315, 6, 5)]), (44, [(302, 8, 5), (309, 6, 4), (314, 9, 6)]),
                     (62, [(301, 6, 6), (309, 8, 5)])]:
        for x, h, w in potes:
            px(x, y - h, w, h, "barro")
            px(x, y - h, 1, h, "barroLuz")
            px(x + w - 1, y - h, 1, h, "barroEsc")
            px(x + 1, y - h - 1, w - 2, 1, "barroEsc")
            if w >= 5:
                px(x + 1, y - h + 2, w - 2, 2, "rotulo")
    # o sapo seco no vidro: o corpo achatado e as patas
    x0, y0, x1, y1 = pote(px, 307, 26, 7, 9, "clara", 0.8, rotulo=False)
    px(x0 + 1, y1 - 2, 3, 2, "cobra")
    px.p(x0, y1, "cobraEsc")
    px.p(x0 + 4, y1, "cobraEsc")
    px.p(x0 + 2, y1 - 3, "cobraLuz")
    px(300, 2, 18, 8, "palha")
    px(300, 2, 18, 1, "palhaLuz")
    for x in range(301, 318, 3):
        px(x, 3, 1, 7, "palhaEsc")


def alambique(px):
    """O alambique de vidro sobre a lamparina, na ponta da bancada: o balão redondo com o líquido verde num tripé de
    ferro, o bico que sobe e desce até o frasco que recebe as gotas. A chama da lamparina vem depois do escuro."""
    t0 = 54  # o tampo
    # o frasco que recebe, com o fundo âmbar
    px(96, 45, 5, 9, "vidro")
    px(96, 45, 1, 9, "vidroBorda")
    px(100, 45, 1, 9, "vidroBorda")
    px(97, 50, 3, 3, "ambar")
    px(97, 50, 3, 1, "ambarLuz")
    px.p(97, 46, "vidroBrilho")
    px(97, 44, 3, 1, "vidroBorda")
    # a lamparina de barro debaixo do balão
    px(109, t0 - 3, 7, 3, "barro")
    px(109, t0 - 3, 7, 1, "barroLuz")
    # o tripé
    px.linha(107, 47, 105, t0 - 1, "ferro")
    px.linha(117, 47, 119, t0 - 1, "ferro")
    px(106, 47, 13, 1, "ferroLuz")
    # o balão: redondo, o líquido na metade de baixo, a borda e o brilho
    cx, cy, r = 112, 42, 4.6
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if d <= r:
                px.p(x, y, "vidroBorda" if d > r - 1 else ("turvaLuz" if y == int(cy) + 1 else "turva") if y > cy else "vidro")
    px(110, 39, 1, 2, "vidroBrilho")
    # o gargalo e o bico: sobe do balão e desce até a boca do frasco
    px(111, 36, 2, 2, "vidroBorda")
    px.linha(111, 36, 106, 35, "vidroBorda")
    px.linha(106, 35, 99, 43, "vidroBorda")
    px.linha(106, 34, 100, 42, "vidroBrilho")


def cranio(px):
    """O crânio de cervo com a galhada, preso na parede entre a coifa e o esteio, perto do fogo: o focinho para baixo, as
    órbitas escuras e os galhos abrindo para os lados."""
    cx = 251
    px(cx - 2, 12, 5, 4, "osso")      # a caixa
    px(cx - 2, 12, 5, 1, "ossoLuz")
    px(cx - 1, 16, 3, 4, "osso")      # o focinho
    px.p(cx, 19, "ossoEsc")
    px.p(cx - 2, 14, "pavio")         # as órbitas
    px.p(cx + 2, 14, "pavio")
    px.p(cx, 17, "ossoEsc")
    for s_ in (-1, 1):                 # a galhada
        px.linha(cx + 2 * s_, 12, cx + 4 * s_, 7, "galhada")
        px.linha(cx + 4 * s_, 7, cx + 4 * s_, 4, "galhada")
        px.linha(cx + 3 * s_, 9, cx + 6 * s_, 8, "galhada")
        px.p(cx + 6 * s_, 7, "galhada")
        px.p(cx + 4 * s_, 4, "ossoLuz")
    px(cx - 1, 11, 3, 1, "madeiraEsc")  # o prego e a tira de couro


def protecoes(px):
    """O que protege a casa: a estrela de palha trançada sobre a porta e o amuleto de osso e penas pendurado no batente."""
    cx, cy = 25, 6
    for d in range(-2, 3):
        px.p(cx + d, cy, "palha")
        px.p(cx, cy + d, "palha")
        px.p(cx + d, cy + d, "palhaEsc" if abs(d) == 2 else "palhaLuz")
        px.p(cx + d, cy - d, "palhaEsc" if abs(d) == 2 else "palhaLuz")
    px.p(cx, cy, "baga")  # o nó de linha vermelha
    # o amuleto: o fio, o ossinho atravessado, a pedra furada e duas penas
    px(41, 11, 1, 6, "barbante")
    px(39, 17, 5, 1, "osso")
    px.p(39, 17, "ossoLuz")
    px(40, 19, 3, 2, "pedra")
    px.p(41, 19, "pavio")
    px(40, 21, 1, 4, "pena")
    px(42, 21, 1, 3, "penaLuz")


def enfiada(px):
    """A enfiada de cogumelos secos pendurada na ponta da vara das ervas."""
    px(145, 12, 1, 18, "barbante")
    for k, y in enumerate((14, 18, 22, 26)):
        x = 143 + (k % 2)
        px(x, y, 4, 1, "cogumeloLuz")
        px(x, y + 1, 4, 1, "cogumeloEsc")
    px.p(145, 30, "barbante")
