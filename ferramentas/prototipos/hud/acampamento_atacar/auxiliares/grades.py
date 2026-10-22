"""Os animais do patrulheiro no acampamento (21/10/2026, proposta; nada no jogo): uma figura de 16×16 de corpo inteiro
por animal, de perfil para a direita (o fogo), os pés na linha de baixo como as figuras da fogueira (retratos.js), sem
contorno e com as cores agrupadas; a identidade e a paleta dos retratos aprovados (retrato-lobo, -urso, -falcao). A
luz do fogo vem do jogo (acampamento.js, aquecido); a escala é a dos personagens sentados, sem encher o quadro:
  - lobo: deitado, a cabeça erguida para o fogo, as orelhas em pé, o olho âmbar, o focinho e o peito claros, as patas
    da frente estendidas; o corpo baixo e comprido, a cauda no chão;
  - urso: sentado e pesado, a cabeça grande no alto com as orelhas pequenas e redondas, as costas descendo dela até a
    garupa larga no chão, o focinho claro com o nariz escuro na ponta, a sombra do pescoço, a pata da frente no chão;
    o maior dos três;
  - falcão: pousado num toco, ereto, o capuz escuro, o olho com o anel amarelo, o bico curvo com a ponta para baixo, o
    bigode escuro, a garganta e o peito claros, a asa cinza-azulada cobrindo o lado e as pontas passando da cauda.
    python grades.py <pasta>           # grava grades/<id>.txt, listas/<id>/<camada>.lua e proposta/<id>-16.png
"""
import pathlib
import sys

from PIL import Image

CORES = {
    # o lobo (retrato-lobo): o claro do focinho e do peito, os cinzas, a sombra, o olho, o nariz
    "L": "c8bfae", "l": "9a948a", "m": "78736a", "M": "57534c", "s": "3a3731", "e": "a07a3a", "n": "17140f",
    # o urso (retrato-urso): o focinho, a luz, o pelo, a sombra, a sombra funda, o nariz e o olho
    "B": "c49a6c", "b": "9a6a40", "u": "74502e", "U": "553820", "t": "36240f", "N": "1e1410",
    # o falcão (retrato-falcao): o peito, a barra, a asa clara, a asa, o capuz, o escuro, o amarelo; o toco
    "W": "efe6d2", "w": "c4b89e", "c": "8a9ab8", "C": "4a5674", "k": "2a3040", "K": "1e2230", "y": "d89a1c",
    "T": "6a4a30", "R": "4a3220", "r": "2e1f14",
}
V = "................"
LOBO = [V] * 6 + [
    "...........M.M..",
    "..........lMlM..",
    "..........lmmml.",
    "..........lmeLLn",
    "..........lmmLL.",
    ".........lmLLL..",
    "...mmmmmmlmLL...",
    "..mlllmmmMmLL...",
    ".smMMMMMMMMlLl..",
    "sssMMsssMMsLlLl.",
]
URSO = [V] * 4 + [
    ".........U..U...",
    "........Uubbbu..",
    ".....UUUubbbbbu.",
    "....UuuuUubNbbBB",
    "...UuuuuuUubbBBN",
    "..UuuuuuuuUbbb..",
    "..UuuuuuuuUUU...",
    ".tUuuuuuuuUbu...",
    ".tUuuuuuuuUbu...",
    "ttUuuuuuuUUbu...",
    "ttUUuuuuUUUbuB..",
    ".tttUUUUttUUbBB.",
]
FALCAO = [V] * 4 + [
    "......kKk.......",
    ".....kKKKk......",
    ".....KKKyKc.....",
    ".....CKWKcK.....",
    "....CCCWWK......",
    "....CCCCWw......",
    "...kCCCCwW......",
    "...kCCCcWw......",
    "..kkCCCCw.......",
    ".kk...yTTy......",
    "......TTRR......",
    ".....rTTRRr.....",
]
# A segunda rodada do lobo e do urso (21/10/2026, pedido do Jean; o falcão continua o da primeira):
#   - lobo r2: o mesmo lobo deitado e atento, voltado para o fogo, com a anatomia refeita: o pescoço desce na diagonal
#     da cabeça até as costas (no r1 subia reto), a cabeça à frente do peito, o corpo deitado com seis linhas de volume
#     (no r1 era uma faixa), as patas da frente estendidas no chão, a cauda acomodada atrás; a garganta clara só embaixo
#     do focinho, o peito no tom médio;
#   - urso r2: refeito pelas fotos de urso pardo sentado (Wikimedia Commons, só para a anatomia) e pelo retrato
#     aprovado: a forma de sino (as costas descendo do corcunda até a garupa larga no chão), a cabeça larga em leve três
#     quartos para o fogo, as orelhas pequenas e redondas, o focinho curto e robusto com o nariz na ponta, o pescoço
#     curto, as patas da frente em duas colunas grossas até o chão, a coxa de trás como um plano próprio com o pé à
#     frente. No r1 as costas arredondadas, o focinho fino e a pata pequena davam um roedor.
LOBO_R2 = [V] * 5 + [
    "...........M.M..",
    "...........lMlM.",
    "..........llmmmm",
    "..........lmeLLn",
    ".........llmmLL.",
    "........lllmLl..",
    "......mlllmlLl..",
    "...mmmmlmmmllm..",
    ".mMMMmmmMMMmlLl.",
    "sMMMMMMMMMMslLLl",
    "sssMMMMsssssLLLl",
]
URSO_R2 = [V] * 4 + [
    ".....Ub...bU....",
    ".....uubbbuuu...",
    "...UUuuNbNuuu...",
    "..UUuuubbbBBBB..",
    "..UuuuuubuBBBN..",
    ".UUuuuuuUubbbU..",
    ".UuuuuuuUuubu...",
    "tUuuUUuuUbuUbu..",
    "tUuUuuUuUbuUbu..",
    "tUuUuuuUUbuUbu..",
    "ttUUuuuuUbuUbu..",
    ".ttttBBBtBBtBB..",
]
# A terceira rodada do lobo e do urso (21/10/2026, pedido do Jean): pelas duas referências geradas que ele mandou
# ("Lobo cinzento deitado em pixel art-1.png" e "Urso-pardo sentado em pixel art-2.png", em
# ferramentas/arte/referencias/icones/), a direção principal de anatomia, pose e proporções; medidas na guia (o animal
# recortado pela caixa dele e reduzido: o lobo com 15 px de comprimento, o urso com 12 de altura; guias/, oculta nas
# fontes), redesenhadas à mão com as paletas dos retratos aprovados e o pelo em poucas áreas:
#   - lobo r3: o corpo baixo no chão (as costas retas na linha 12, sem rampa), a cabeça erguida para a direita com as
#     orelhas, o olho âmbar e o focinho comprido, o pescoço saindo dos ombros, o peito claro, a coxa de trás clara, as
#     patas da frente estendidas, a cauda atrás;
#   - urso r3: sentado em leve três quartos para a direita, a cabeça larga com as orelhas pequenas e o focinho claro com
#     o nariz, o pescoço curto, as costas descendo da nuca à garupa, o plano claro do braço, as duas patas da frente
#     grossas até o chão, a coxa de trás com o pé à frente; mais alto e mais volumoso que o lobo.
LOBO_R3 = [V] * 8 + [
    "...........M.M..",
    "..........mlMmM.",
    "..........lmeLLn",
    ".........mlLLm..",
    "....mmmmmmlLL...",
    "..mmlllmmmmlL...",
    ".mmMlLLlMMmMlLLl",
    ".sMMmLLmssMmlLLl",
]
URSO_R3 = [V] * 4 + [
    "........Ub.Ub...",
    "........uuuuuu..",
    ".......UuuuNuu..",
    "......UuuuuuBBB.",
    ".....UuuuUuuBBN.",
    "....UuubbUUuuU..",
    "....UuuubbUuubU.",
    "...UuuUUubbUubU.",
    "..UuuUuuUubUubU.",
    "..UuUuuuuUbUubU.",
    "..UUuuuuUUbUubU.",
    "...tBBUt.BBtBBt.",
]
# A quarta rodada (22/10/2026, pedido do Jean): o refinamento da terceira, julgado na fogueira em tamanho real;
#   - lobo r4: a mesma pose baixa; a coxa no cinza claro médio (era uma mancha clara), o peito sem o bloco claro
#     vertical, as patas da frente numa faixa contínua apoiada no chão (o claro em cima, o meio embaixo), a sombra
#     embaixo do focinho para o nariz escuro ler na ponta;
#   - urso r4: a cabeça mais larga (oito colunas) com as orelhas redondas nos cantos, o focinho curto e claro com o
#     nariz escuro na ponta, a linha escura entre a mandíbula e o peito, o corcunda arredondando o alto das costas (a
#     rampa reta sumiu), o peito num plano claro, as patas da frente com a base larga no chão, a coxa num volume só com
#     um plano de luz e o pé à frente.
LOBO_R4 = [V] * 8 + [
    "...........M.M..",
    "..........mlMmM.",
    "..........lmeLLn",
    ".........mlLlM..",
    "....mmmmmmllL...",
    "..mmlllmmmmlm...",
    ".mmMllmMMmmllLLl",
    ".sMMMmmMssMmmmLl",
]
URSO_R4 = [V] * 4 + [
    ".......Ub...bU..",
    ".......ubbbbbu..",
    ".....UUuubbbbuu.",
    "....UuuuuubNuBBN",
    "....UuuuuuuuuBBU",
    "....UuuuuuUUUU..",
    "...UuuuuuubbbbU.",
    "..UuuuuuuubbbuU.",
    "..UbbbuuuUubbuuU",
    ".UbbbbuuuUubbuuU",
    ".UbbbuuuuUubbuuU",
    "..ttBBttt.uBBBBt",
]
# O lobo r5 (22/10/2026, pedido do Jean): o r4 era achatado demais (o tronco uma faixa no chão, a cabeça pequena). Onze
# linhas de altura: a cabeça maior (seis linhas), com as orelhas, o olho âmbar, o focinho, o nariz na ponta e a linha
# escura da boca e da mandíbula separados; o pescoço curto ligado aos ombros; o tronco deitado mais grosso, com as
# costas planas (sem rampa) e o volume dos ombros; as patas da frente apoiadas no chão e a cauda atrás. O urso r4
# continua mais pesado.
LOBO_R5 = [V] * 5 + [
    "..........M..M..",
    "..........lMmlM.",
    ".........mllmmm.",
    ".........lmemLLn",
    ".........llmlMMs",
    "...mmmmmmllLLl..",
    "..mmllllmlLLl...",
    ".mllllmmmmlLm...",
    ".mmMllmmMMmllLl.",
    "sMMMMmmMMMMmlLLl",
    "ssMMMssMMssMmmmL",
]
CAMADAS = {
    "animal-lobo": (LOBO, ["corpo", "cabeca", "detalhes"],
                    lambda x, y, ch: "detalhes" if ch in "en" else "cabeca" if y <= 11 and x >= 9 else "corpo"),
    "animal-urso": (URSO, ["corpo", "cabeca", "detalhes"],
                    lambda x, y, ch: "detalhes" if ch == "N" else "cabeca" if 4 <= y <= 9 and x >= 8 else "corpo"),
    "animal-lobo-r2": (LOBO_R2, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "en" else "cabeca" if y <= 9 and x >= 9 else "corpo"),
    "animal-urso-r2": (URSO_R2, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch == "N" else "cabeca" if 4 <= y <= 8 and x >= 5 else "corpo"),
    "animal-lobo-r3": (LOBO_R3, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "en" else "cabeca" if y <= 11 and x >= 9 else "corpo"),
    "animal-urso-r3": (URSO_R3, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch == "N" else "cabeca" if y <= 8 and x >= 6 else "corpo"),
    "animal-lobo-r4": (LOBO_R4, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "en" else "cabeca" if y <= 11 and x >= 9 else "corpo"),
    "animal-urso-r4": (URSO_R4, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch == "N" else "cabeca" if y <= 8 and x >= 6 else "corpo"),
    "animal-lobo-r5": (LOBO_R5, ["corpo", "cabeca", "detalhes"],
                       lambda x, y, ch: "detalhes" if ch in "en" else "cabeca" if y <= 9 and x >= 9 else "corpo"),
    "animal-falcao": (FALCAO, ["toco", "corpo", "cabeca", "detalhes"],
                      lambda x, y, ch: "toco" if ch in "TRr" else "detalhes" if ch == "y" else "cabeca" if y <= 7 else "corpo"),
}


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(CORES[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{CORES[ch]}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
