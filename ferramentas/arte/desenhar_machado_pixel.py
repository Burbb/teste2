"""O machado do Guerreiro em pixel art (proposta; o jogo ainda usa o sprite 16×16 "machado"). O terceiro objeto do
método do escudo e do unguento (pixel_comum.py), cada tamanho desenhado na própria grade.

O que o jogo diz do item (rpg/itens.py): "Machado", uma das bases de arma do Guerreiro, ao lado da Espada, da Maça, do
Montante e do Martelo, em todos os materiais (Machado de Ferro, de Aço...). O mesmo desenho do jogo é o dos únicos
Lamento de Gharbad e O Açougueiro (o papel de equipamento, que muda junto) e o da habilidade Redemoinho e do estado
Fúria (outros papéis, que não mudam: o item se acha só em Icones.ITEM). O jogo não diz o tipo; o desenho atual é uma
cabeça de lâmina única num cabo comprido, de uma mão (vai com o escudo).

O tipo (a decisão antes das proporções): um machado de guerra de uma mão, de barba (a lâmina desce em gancho junto
do cabo). É a arma de quem luta com escudo; a barba dá a silhueta que nenhuma outra arma da família tem (a espada é
uma linha, a maça é uma bola na ponta), e a cabeça continua pequena perto do cabo, como numa arma de verdade.

A construção, em cada tamanho (32, 40, 48 e 64 px), na própria grade:
  - a composição: o cabo na diagonal, do pé embaixo à esquerda até a cabeça em cima à direita, como a espada e a
    maça da família; a lâmina sai para cima e para a esquerda, com o gume virado para a luz. As medidas são pensadas
    num sistema que gira junto com o cabo (u ao longo dele, v para o lado da lâmina);
  - o ferro (cinza neutro, sem o azul do escudo): a face da lâmina fosca de forja, clareando um pouco do olho para o
    gume (a lâmina afina); o gume afiado numa faixa clara e polida, com o brilho onde a luz bate de frente (perto da
    ponta de cima); a espessura do ferro numa faixa escura por baixo da barba e do olho (a cabeça vista um pouco de
    baixo); o olho (a luva de ferro em volta do cabo) mais grosso que a lâmina, com a borda acesa do lado da luz; o
    talão curto atrás, na sombra;
  - o encaixe: o cabo atravessa o olho e aparece por cima, com o topo da madeira mais claro (em 48 e 64, a cunha);
    logo abaixo do olho, a sombra da cabeça no cabo;
  - o cabo de freixo: madeira clara e quente (a maça tem o cabo escuro), um cilindro em três faixas na diagonal; o
    veio em 48 e 64; o pé alarga um pouco para a mão não escorregar;
  - o desgaste, discreto: em 48 e 64, um dente pequeno no meio do gume e a madeira mais escura onde a mão segura
    (pontos de corrosão na face foram tentados e liam como rebites). Em 32 e 40, nada (seria ruído);
  - a limpeza, o contorno de 1 pixel e as correções são as etapas comuns (pixel_comum.py).
O dobro de cada arquivo é a duplicação exata dos pixels.

    python ferramentas/arte/desenhar_machado_pixel.py <pasta>    (grava noutra pasta: a proposta)
    python ferramentas/arte/desenhar_machado_pixel.py            (grava em rpg/web/static/hud/icones/: só na integração)
"""

import math
import sys

import numpy as np

from pixel_comum import ajustar, contornar, destino, grade, imagem, limpar, salvar

LADOS = (32, 40, 48, 64)  # 32: ficha, mercado, dicas; 40: o corpo e a mochila do Inventário; 48 e 64: o saque

# As rampas, do mais escuro ao mais claro: o ferro forjado (cinza neutro, um pouco frio) e o freixo (claro e quente).
FERRO = ["#0e0f11", "#1a1c20", "#282b31", "#383c44", "#4c5159", "#646a73", "#848b94", "#b0b6bd", "#e4e8ec"]
FREIXO = ["#20150c", "#3a2716", "#583c21", "#77532e", "#946b3c", "#ae844e", "#c49d66", "#d8b886", "#e9d2a6"]

R2 = math.sqrt(2)
# As medidas de cada tamanho, em pixels, no sistema do cabo: a origem (o pé do cabo, x0 e y0, num centro de pixel), o
# comprimento do cabo (L) e a meia largura (hw); o pé que alarga (pe, em quanto, e pe_l, até onde); o olho: o centro
# (ue), a meia altura (he) e a parede (te); o talão (talao); a lâmina: o gume (V, a distância ao eixo do cabo), quanto
# a ponta de cima sobe (ponta) e a barba desce (barba), a meia altura onde a lâmina sai do olho (pescoco), a curva do gume (curva), o gancho da barba (p, maior = mais
# fundo) e a subida da ponta (q); a faixa do gume (fio) e a espessura do ferro (esp). `det` liga os detalhes que só
# cabem nos tamanhos grandes (o veio, a cunha, o dente, a corrosão).
MEDIDAS = {
    32: dict(x0=5.0, y0=29.5, L=28.4, hw=1.1, pe=0.6, pe_l=2.5, ue=25.0, he=2.4, pescoco=1.4, te=0.7, talao=1.0,
             V=10.2, ponta=2.0, barba=8.6, curva=2.6, p=2.8, q=1.4, fio=1.0, esp=1.0, det=0),
}
# Os outros tamanhos: as medidas do 32 na escala de cada grade (a origem no mesmo canto), com o que muda por tamanho.
for _l, _extra in ((40, dict(x0=6.0, y0=37.5, fio=1.2)),
                   (48, dict(x0=7.0, y0=44.5, fio=1.5, esp=1.4, det=1)),
                   (64, dict(x0=9.0, y0=59.5, fio=2.0, esp=1.8, det=2))):
    _e = _l / 32
    MEDIDAS[_l] = {k: (v * _e if k not in ("p", "q", "det") else v) for k, v in MEDIDAS[32].items()} | _extra
    MEDIDAS[_l]["L"] = MEDIDAS[_l]["ue"] + MEDIDAS[_l]["he"] + 1.2   # o cabo sai do olho pouco mais de 1 px
    MEDIDAS[_l]["pe"] = 0.6                                           # o pé alarga 1 px de cada lado, em todos
# Correções feitas olhando cada tamanho: {(x, y): (material ou None, tom)}.
AJUSTES = {32: {}, 40: {}, 48: {}, 64: {}}


def desenhar(lado):
    M = MEDIDAS[lado]
    mat, tom, fixo, x, y = grade(lado)
    dx, dy = x - M["x0"], y - M["y0"]
    u, v = (dx - dy) / R2, (-dx - dy) / R2   # u ao longo do cabo (para a cabeça), v para o lado da lâmina
    hw, ue, he = M["hw"], M["ue"], M["he"]
    v0 = hw + M["te"]                         # onde a lâmina sai do olho

    def cabeca(uu, vv):
        # o olho: um bloco de cantos arredondados em volta do cabo, do talão até onde a lâmina sai
        vc, vr = (v0 - (v0 + M["talao"])) / 2, (2 * v0 + M["talao"]) / 2
        olho = (np.abs(uu - ue) / he) ** 4 + (np.abs(vv - vc) / vr) ** 4 <= 1
        t = np.clip((vv - v0) / (M["V"] - v0), 0, 1)
        pc = M["pescoco"]
        topo = ue + pc + (he - pc + M["ponta"]) * t ** M["q"]
        baixo = ue - pc - (he - pc + M["barba"]) * t ** M["p"]
        uc, us = (ue + he + M["ponta"] + ue - he - M["barba"]) / 2, (M["ponta"] + M["barba"]) / 2 + he
        gume = M["V"] - M["curva"] * ((uu - uc) / us) ** 2
        lamina = (vv > v0 - 0.5) & (vv <= gume) & (uu <= topo) & (uu >= baixo)
        return olho, lamina, gume

    # ---- o cabo: um cilindro de freixo em faixas pela diagonal (a de cima acesa, a de baixo na sombra), o pé que alarga
    larg = hw + M["pe"] * np.clip(1 - u / M["pe_l"], 0, 1)
    cabo = (u >= -0.4) & (u <= M["L"]) & (np.abs(v) <= larg)
    tom_cabo = np.select([v > 0.6 * larg, v > 0, v > -0.6 * larg], [6, 5, 4], 2)
    if M["det"]:
        # o veio: uma linha mais escura em traços ao longo do cabo, a uma altura que muda devagar (um veio só, não
        # listras); e a madeira mais escura onde a mão segura (o desgaste)
        veios = ((1.06, 0.0), (-0.35, 2.1))[:M["det"]]
        for vv, fase in veios:
            veio = (np.abs(v - vv) < 0.1) & (np.sin(u * 0.8 + fase) + 0.6 * np.sin(u * 0.31 + fase) > 0.45)
            tom_cabo = np.where(veio & (u > M["pe_l"]) & (u < ue - he - 2), tom_cabo - 1, tom_cabo)
        mao = (u > M["pe_l"] + 0.5) & (u < M["pe_l"] + 0.28 * M["L"])
        tom_cabo = np.where(mao, np.maximum(2, tom_cabo - 1), tom_cabo)
    mat[cabo], tom[cabo] = "m", tom_cabo[cabo]
    fixo[cabo] = True                                             # as faixas de 1 pixel na diagonal são de propósito
    pe = cabo & (u < 0.6)
    tom[pe] = np.maximum(2, tom[pe] - 1)                         # o fundo do pé, virado para baixo
    topo_cabo = cabo & (u > M["L"] - 0.8)
    tom[topo_cabo] = 7                                            # o topo da madeira, cortado, que sai do olho
    if M["det"] == 2:                                             # a cunha que aperta o cabo no olho
        tom[topo_cabo & (np.abs(v) < 0.4)] = 3
    sombra = cabo & (u < ue - he) & (u > ue - he - 1.6)
    tom[sombra] = np.maximum(1, tom[sombra] - 2)                  # a sombra da cabeça no cabo

    # ---- a cabeça de ferro
    olho, lamina, gume = cabeca(u, v)
    # a espessura: a cabeça vista um pouco de baixo; o que aparece da forma deslocada para o pé, por baixo da barba e
    # do olho, é o lado do ferro
    olho_e, lamina_e, _ = cabeca(u + M["esp"], v)
    lado_ferro = (olho_e | lamina_e) & ~olho & ~lamina & ~(cabo & (u > ue - he - 0.5))
    mat[lado_ferro], tom[lado_ferro] = "f", 2
    # a face da lâmina: fosca, clareando do olho para o gume (a lâmina afina e vira para a luz)
    tv = np.clip((v - v0) / (M["V"] - v0), 0, 1)
    tom_face = np.select([tv > 0.6, tv > 0.2], [5, 4], 3)
    mat[lamina], tom[lamina] = "f", tom_face[lamina]
    # o gume: a faixa polida, mais clara em cima (onde a luz bate) e menos na barba
    fio = lamina & (v > gume - M["fio"])
    tu = np.clip((u - (ue - he - M["barba"])) / (M["barba"] + 2 * he + M["ponta"]), 0, 1)
    tom_fio = np.select([tu > 0.6, tu > 0.25], [8, 7], 6)
    mat[fio], tom[fio] = "f", tom_fio[fio]
    fixo[fio] = True
    # o olho: a luva em volta do cabo, mais grossa (a borda do lado da luz acesa, o talão na sombra)
    mat[olho] = "f"
    tom[olho] = np.select([v[olho] > v0 - 0.8, v[olho] > -hw], [6, 4], 3)
    talao = olho & (v < -(v0 + M["talao"]) + 0.8)
    tom[talao] = 2
    if M["det"]:
        # o desgaste: um dente pequeno no meio do gume (pontos de corrosão na face liam como rebites)
        ud = ue + (M["ponta"] - M["barba"]) / 2
        dente = fio & (np.abs(u - ud) < 0.75) & (v > gume - 0.75)
        mat[dente] = ""

    # ---- a limpeza, o contorno e as correções (pixel_comum.py)
    tom = limpar(mat, tom, fixo)
    contornar(mat)
    ajustar(mat, tom, AJUSTES[lado])
    return imagem(mat, tom, {"f": FERRO, "m": FREIXO})


if __name__ == "__main__":
    saida = destino(sys.argv)
    for lado in [l for l in LADOS if l in MEDIDAS]:
        print(f"machado-{lado}: {salvar(desenhar(lado), saida, 'machado')} cores")
