"""A folha compacta do protótipo de combate e atributos: as capturas que os roteiros conferir*.mjs gravam
(capturas/1920-*.png e v2/v3/v4-1920-*.png), reduzidas lado a lado com um rótulo, numa imagem só para ver de relance.

    python ferramentas/prototipos/combate-atributos/auxiliares/folha.py        # a v1: grava folha.png
    python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v2     # a v2: grava folha-v2.png
    python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v3     # a v3: grava folha-v3.png
    python ferramentas/prototipos/combate-atributos/auxiliares/folha.py v4     # a v4: grava folha-v4.png
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PROTO = AQUI.parent
CAPT = PROTO / "capturas"
QUADROS = [("1920-2-ameaca", "1 · O Bote anunciado: alvo, dano previsto, quando resolve"),
           ("1920-3-alvo", "Escolha de alvo (clique ou número; Esc volta)"),
           ("1920-5-esmagador", "2 · O Golpe Esmagador: várias respostas"),
           ("1920-7-terror", "3 · Grito de Terror: A perde a vez (Vontade 3); Odette só abala"),
           ("1920-4-ficha", "Ficha: atributos e o que mudam, com a conta"),
           ("1920-11-comparar", "Comparar A, B, C e a livre"),
           ("1920-8-retorno-antes", "Teste: Pena antes da posição de Morel"),
           ("1920-9-retorno-depois", "Teste: Reerguer depois da posição"),
           ("1920-12-fora-da-luta", "Fora da luta: o companheiro acrescenta")]
QUADROS_V2 = [("v2-1920-1-preparar-forca", "Preparar: a Força, o kit de 10 pontos e o que ela faz"),
              ("v2-1920-2-preparar-precisao", "A Precisão: a ficha e o dano previsto mudam"),
              ("v2-1920-3-preparar-arma", "Só a arma trocada: o dano sobe na tabela"),
              ("v2-1920-5-alvo-previsto", "Na luta, o dano previsto em cada alvo"),
              ("v2-1920-6-ameaca-tenacidade", "A ameaça com a chance final de resistir"),
              ("v2-1920-7-ultimate", "A ultimate com 3 de Ímpeto (teste)"),
              ("v2-1920-9-comparar", "Comparar as quatro builds no mesmo alvo"),
              ("v2-1920-10-fora-da-luta", "Fora da luta: a Presença"),
              ("v2-1920-11-resultados", "Resultados: build, kit, recurso, ameaças")]
QUADROS_V3 = [("v3-1920-1-preparar-chama", "Preparar: tipo e escala de cada golpe, dano por alvo, a combinação"),
              ("v3-1920-2-preparar-baluarte", "O Baluarte e o Avanço (dano pela vida)"),
              ("v3-1920-4-alvo-previsto", "Na luta, o dano previsto por alvo (a conta no mouse)"),
              ("v3-1920-5-ultimate-usada", "A ultimate: uma vez por luta, \"já usada\" depois"),
              ("v3-1920-6-ameaca", "O Bruto: o golpe anunciado e a chance de resistir"),
              ("v3-1920-7-caes", "Os Cães de Brasa: 60% de fogo"),
              ("v3-1920-9-comparar", "Comparar as cinco builds nos três alvos"),
              ("v3-1920-10-resultados", "Resultados: ultimate, ameaças, recurso antes e depois"),
              ("v3-1920-8-fim", "O fim: ameaças e o uso da ultimate")]
QUADROS_V4 = [("v4-1920-1-preparar-chama", "Preparar: a Chama com a Chuva e a comparação do fogo"),
              ("v4-1920-2-chuva-no-grupo", "Encontro 3: a Chuva pôs Queimadura em cada inimigo"),
              ("v4-1920-3-conflagracao", "A Conflagração consome as Queimaduras; Morel com o Golpe Oportuno"),
              ("v4-1920-9-caes", "Os Cães de Brasa: a Queimadura pega, o dano cai"),
              ("v4-1920-4-preparar-baluarte", "O Baluarte (igual à v3)"),
              ("v4-1920-7-ultimate-usada", "A ultimate: uma vez por luta"),
              ("v4-1920-8-ameaca", "O Bruto anunciando o golpe"),
              ("v4-1920-11-comparar", "Comparar as builds"),
              ("v4-1920-12-resultados", "Resultados com os detalhes")]
COLUNAS, LARGURA, MARGEM, ROTULO = 3, 760, 16, 30


def fonte(t):
    for nome in ("C:/Windows/Fonts/georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(nome, t)
        except OSError:
            pass
    return ImageFont.load_default()


def main():
    versao = (sys.argv[1:] or ["v1"])[0]
    quadros = {"v1": QUADROS, "v2": QUADROS_V2, "v3": QUADROS_V3, "v4": QUADROS_V4}[versao]
    ims = [(Image.open(CAPT / f"{n}.png").convert("RGB"), r) for n, r in quadros if (CAPT / f"{n}.png").exists()]
    alt = round(LARGURA * ims[0][0].height / ims[0][0].width)
    linhas = (len(ims) + COLUNAS - 1) // COLUNAS
    folha = Image.new("RGB", (COLUNAS * (LARGURA + MARGEM) + MARGEM, 60 + linhas * (alt + ROTULO + MARGEM)), (18, 17, 16))
    d = ImageDraw.Draw(folha)
    titulo = {"v1": "primeira versão", "v2": "segunda versão", "v3": "terceira versão", "v4": "quarta versão"}[versao]
    d.text((MARGEM, 16), f"Protótipo de combate e atributos, {titulo} (nada no jogo) · 1920×945", fill=(242, 201, 76),
           font=fonte(26))
    for k, (im, rotulo) in enumerate(ims):
        x = MARGEM + (k % COLUNAS) * (LARGURA + MARGEM)
        y = 60 + (k // COLUNAS) * (alt + ROTULO + MARGEM)
        d.text((x, y + 4), rotulo, fill=(232, 220, 190), font=fonte(18))
        folha.paste(im.resize((LARGURA, alt), Image.LANCZOS), (x, y + ROTULO))
    saida = PROTO / ("folha.png" if versao == "v1" else f"folha-{versao}.png")
    folha.save(saida, optimize=True)
    print(saida, folha.size)


if __name__ == "__main__":
    main()
