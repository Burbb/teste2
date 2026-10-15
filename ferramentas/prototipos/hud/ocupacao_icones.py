"""O estudo da ocupação dos ícones no inventário (experimento, fora do jogo): os mesmos desenhos num tamanho de
exibição intermediário, entre o 32 de hoje e o 48 que já existe, para os espaços do corpo (60 px) e da mochila (56 px).

A folga não está nos arquivos: os de 32 px têm 1 a 4 px de margem transparente (o desenho ocupa 27 a 30 px). Ela vem
da exibição: a <img> é pedida em 32 px (Icones.item) e centrada num espaço de 56 ou 60 px. Por isso o ajuste é no
tamanho de exibição, com arquivos nativos desse tamanho, sem ampliar os de 32:
  - o anel, a cota e a espada (a família pintada): pelo mesmo caminho dos tamanhos de hoje (preparar_hud4p.py: as
    folhas aprovadas, a mesma escala do grupo de itens, a mesma redução "paleta"); os de 32 e 48 desse caminho saem
    iguais aos do jogo. Nada é redesenhado;
  - o escudo final: pelas mesmas regras de desenhar_escudo_pixel.py, com as medidas entre as de 32 e as de 48 (a
    escada e o reflexo do 48, os cravos de 2x2); é uma prova de tamanho, sem a passagem de acabamento que cada tamanho
    do escudo teve (se o tamanho for aprovado, ela fica por fazer).
Gera ocupacao/<peça>-40.png e o @2x (a duplicação, como nos outros).

    python ferramentas/prototipos/hud/ocupacao_icones.py
"""

import os
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "arte"))  # o escudo saiu do protótipo (1.94.0)
import desenhar_escudo_pixel as escudo  # noqa: E402
from preparar_hud4p import GRUPOS, METODO_USO, escalas, no_quadrado

AQUI = pathlib.Path(__file__).resolve().parent
SAIDA = AQUI / "ocupacao"
LADOS = (40,)  # 44 também foi olhado: o anel passava a dominar e o objeto encostava no espaço
PINTADOS = ("anel", "cota", "espada")
# o escudo em 40: as medidas entre as de 32 e 48 (o raio no centro de pixel, e a margem de 2 px do de 32)
escudo.MEDIDAS[40] = dict(raio=16.45, lado=1, aro=2.4, degrau=1, cupula=3.9, base=0.8, sulco=1.0, cravos=10.1, cravo="2",
                          sombra_peca=1, emendas=True, reflexo=(1.05, 1.7), alcance=0.68, escada=(7, 5, 4, 3, 1))
escudo.AJUSTES[40] = {}  # o estudo é de antes da correção do cravo (ferramentas/arte/desenhar_escudo_pixel.py)
escudo.BRILHO_CUPULA[40] = escudo.BRILHO_CUPULA[48]


def main():
    SAIDA.mkdir(exist_ok=True)
    nomes = GRUPOS["itens"][0]
    pecas = {n: Image.open(AQUI / "assets4p" / "pecas" / f"{n}.png").convert("RGBA") for n in nomes}
    for lado in LADOS:
        fat = escalas(pecas, lado, GRUPOS["itens"][2])  # a escala do grupo inteiro, como nos tamanhos de uso
        for n in PINTADOS:
            for dens, suf in ((1, ""), (2, "@2x")):
                no_quadrado(pecas[n], fat[n], lado, METODO_USO, dens).save(SAIDA / f"{n}-{lado}{suf}.png")
        img = escudo.desenhar(lado)
        img.save(SAIDA / f"escudo-{lado}.png")
        img.resize((2 * lado, 2 * lado), Image.NEAREST).save(SAIDA / f"escudo-{lado}@2x.png")
    print("\n".join(sorted(os.listdir(SAIDA))))


if __name__ == "__main__":
    main()
