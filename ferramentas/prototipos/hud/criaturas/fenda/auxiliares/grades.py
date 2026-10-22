"""O Cão infernal e a Cria do Vazio (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do Bestiário
são o 16 ×2 e ×3. Desenhadas à mão, uma letra por pixel; silhueta e volumes primeiro, a brasa e a Fenda depois.
  O Cão infernal ("Cães de brasa com dentes de obsidiana. O fogo é a casa deles."; demonio e fera; a Mordida
  Sangrenta e a Bola de Fogo): o corpo de carvão quente, com a luz nos planos de cima, as rachaduras de brasa seguindo
  os volumes, a boca acesa por dentro e os dentes negros de obsidiana, com um brilho frio, contra ela.
      A, o que rosna de perfil: a cabeça para a esquerda, a orelha deitada para trás, o focinho comprido com o nariz
          na ponta, a mandíbula aberta com as presas negras em cima e embaixo, a rachadura do olho descendo pela
          mandíbula e outra pelo pescoço;
      B, o mastim de cabeça baixa: de frente, as orelhas curtas para fora, o sobrolho escuro sobre os dois olhos
          acesos, o focinho com o nariz, o rosnado largo com as presas negras nos cantos, a rachadura no meio da
          testa e as brasas no pelo dos ombros.
  A Cria do Vazio ("Pedaços da Fenda que aprenderam a andar. Quanto mais perto dela, mais delas."; corrompido e
  etéreo; a Esfera Sombria e o Toque Drenante; a mesma família quando o antagonista a invoca): o miolo escuro do
  Vazio, o violeta nas bordas, o magenta da Fenda (a cor das visões do Vazio na narração).
      A, o caco da Fenda: um pedaço anguloso e irregular, como vidro escuro quebrado, atravessado de cima a baixo por
          uma rachadura acesa em zigue-zague (a Fenda dentro dela, não um olho), com dois braços e duas pernas de caco;
      B, a fera que anda: magra, de perfil para a esquerda, a cabeça baixa com um olho pequeno e a bocarra em fenda
          acesa, o dorso se desfazendo em fiapos e um buraco de vazio no flanco, as garras acesas.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "cao": {
        "k": "1c1210", "c": "563830", "C": "8a5c46", "d": "34221c",  # o carvão (o escuro, o corpo, a luz, a sombra)
        "r": "9a3416", "o": "d8501a", "O": "ff9a2a", "y": "ffe07a",  # a brasa (funda, viva, a boca, o mais quente)
        "t": "120e18", "T": "6a6488", "e": "ffd040",  # a obsidiana dos dentes e o brilho frio dela; o olho
    },
    "cria": {
        "v": "0e0a16", "V": "2a1e40", "u": "5a4488",  # o Vazio (o miolo, o corpo, a borda)
        "m": "a83a98", "M": "e070d0", "w": "f4e4ff",  # a Fenda (funda, acesa, o mais claro)
        "p": "46356e",  # o plano de luz dos cacos (a A2)
    },
    "cao_t": {  # medidas na referência "Cão infernal em pixel art.png" (o carvão, o couro marrom da luz, a brasa)
        "k": "120c0c", "c": "342628", "C": "4a3836", "b": "5e3424", "B": "8a5236", "L": "b4744a",
        "n": "2c2830", "N": "8a8494",  # o nariz (o negro clareado para não sumir na caixa escura; o brilho)
        "r": "7a1a0a", "o": "d8501a", "O": "ff9a2a", "y": "ffe07a",  # a brasa funda (a gengiva, a orelha), viva, a goela
        "t": "120e18", "T": "6a6488", "e": "ffb030",  # a obsidiana das presas e o reflexo dela; o olho
    },
}

CAO_A = [
    ".........kk.....",
    "........kCCk....",
    ".......kcCck....",
    "......kcCCcck...",
    "....kkCCCCccck..",
    "..kkCCCCeoCccck.",
    "kkCCCCCccccrccck",
    "kcccccccdcccocck",
    ".TOtOtOdrccoccck",
    ".OyyyyyOdcocccck",
    "..tOtOtcccoccccc",
    "...kcccccoccoccc",
    "....kkccccccoccc",
    "......kcCcccccoc",
    ".....kcCccccccoc",
    "....kcCccccccocc",
]
CAO_B = [
    "................",
    "..k..........k..",
    "..kCk......kCk..",
    "..kcCk....kCck..",
    "...kcCkkkkCck...",
    "..kcCCCoCCCcck..",
    ".kcddcCooCcddck.",
    ".kceedcCCcdeeck.",
    ".kcccdcCCcdccck.",
    "..kccdcCCcdcck..",
    "..kcrcckkccrck..",
    "..kctOyyyyOtck..",
    "..kcTtOyyOtTck..",
    "..kkckttttkckk..",
    ".kcoCcckkccCock.",
    "kcCcoccccccocCck",
]
CRIA_A = [
    "......V.........",
    ".....VuV....V...",
    "....VvuuV..VuV..",
    "...VvvmuuVVvuV..",
    "...VvvvMuuuvvuV.",
    "..VvvvvMMuuvvvuV",
    ".VvvvvvvwMuvvvuV",
    ".VvvvvvwMvvvvuV.",
    "VvvvvvMwvvvvvuV.",
    "VVvvvvMvvvvvuuV.",
    ".VVvvvmMvvvuuV..",
    "..VVvvvmvvuuVV..",
    "...VVvvVvvuVuV..",
    "....Vu.VvuV.Vu..",
    "...Vu...Vu...Vu.",
    "..Vu....Vu....V.",
]
CRIA_B = [  # a primeira, de pernas finas e cabeça menor, virava um emaranhado de traços na carta: ficou mais encorpada
    "................",
    "................",
    "...........u..m.",
    "..uuuu....uVu.u.",
    ".uVVVVu..uVVVVu.",
    "uVVMVVVuuVVVVVVu",
    "uVVVVVVVVVmvmVVu",
    "vMmMmMVVVmvvvmVu",
    "vvvvvvuVVVmvmVVu",
    ".uvvvuVVVVVVVVu.",
    "..uu.uVVuuuVVVu.",
    "....uVVu..uVVu..",
    "...uVVu...uVVu..",
    "..uVVu....uVu...",
    ".uVVu.....uVu...",
    ".MMM.....MMM....",
]

# A segunda passada (pedido do Jean; propostas, nada no jogo). As A e B anteriores ficam como estavam.
# A2, a Cria A com volume nos cacos: a silhueta, os fragmentos, a fissura e a paleta da A; cada caco ganha um plano de luz
# (`p`) junto da borda de fora, o da esquerda em cima e o da direita no meio, e o escuro fundo fica junto da fissura,
# como a profundidade da abertura entre eles. Num plano mais escuro (34284f) a diferença quase não aparecia na carta.
CRIA_A2 = [
    "......V.........",
    ".....VuV....V...",
    "....VpuuV..VuV..",
    "...VppmuuVVvuV..",
    "...VppvMuuuvvuV.",
    "..VpppvMMuuvpvuV",
    ".VppvvvvwMuppvuV",
    ".VpvvvvwMvppvuV.",
    "VvpvvvMwvvppvuV.",
    "VVpvvvMvvvpvuuV.",
    ".VVpvvmMvvvuuV..",
    "..VVvvvmvvuuVV..",
    "...VVvvVvvuVuV..",
    "....Vu.VvuV.Vu..",
    "...Vu...Vu...Vu.",
    "..Vu....Vu....V.",
]
# T, o Cão infernal pela referência gerada "Cão infernal em pixel art.png" (ferramentas/arte/referencias/icones/), a
# principal desta tentativa; o A e o B ficam como histórico. Redesenhado à mão medindo na guia oculta
# (guias/cao-infernal-t-guia-16.png: o recorte quadrado de 1200 px a partir de (50, 40), reduzido por média; cada pixel
# vale 75 px) e na silhueta pelo alfa dela. Em três quartos para a esquerda: a orelha dobrada no alto, a testa pesada
# (a faixa de luz) sobre o sobrolho escuro, o olho de trás e o da frente acesos e estreitos sob ele, o focinho largo com
# as rugas do rosnado, o nariz grande (cinza escuro com o brilho: o negro sumia na caixa), o lábio levantado com a
# gengiva, a goela acesa cortada pela presa negra grande e a da frente com o reflexo, a mandíbula e o queixo, a orelha de
# trás à direita com o vermelho dentro e o pescoço escuro com a rachadura em poucos pontos. Na bancada: a primeira tinha a
# metade marrom e a metade de carvão como dois objetos e o nariz sumido; o marrom virou luz em faixas sobre uma massa só;
# a rachadura pontilhada do pescoço caiu pela metade.
CAO_T = [
    "....bk..........",
    "..bbrBbcc.......",
    "..cbBBcCccoc....",
    "...cbbcCCcccCc..",
    "..bLLLBBBCcocck.",
    "..ceckkkkcccorrk",
    "..LBLLbbeyccC..r",
    ".NNcbLBbcccCoc..",
    "nnNbLbbcccccCc..",
    ".nnrrbBbcccccoc.",
    ".TOOrtOrbcccccc.",
    ".tyOOtObcccccCc.",
    "..bBBtBBbccccocc",
    "...bbBBbcccccCc.",
    "......bBccccoc..",
    "......kbcccc....",
]

# Histórico (fora da exportação): a primeira B, de pernas finas, que virava um emaranhado na carta.
CRIA_B_FINA = [
    "................", "................", "...........m..m.", "..........uVu.u.",
    "..uuu....uVVVuu.", ".uVVVu..uVVVVVVu", "uVMVVVuuVVmvmVVu", "uVVVVVVVVmvvvmVu",
    "vMmMmMVVVVmvmVu.", ".uvvvvuVVVVVVuu.", "..uuu.uVuuuuVVu.", "....uVu...uVVu..",
    "...uVu....uVu...", "..uVu.....uVu...", ".uVu......Vu....", ".MM......MM.....",
]

def _camada_cao(x, y, ch):
    if ch in "tT":
        return "dentes"
    if ch in "Oy":
        return "boca"
    if ch == "e":
        return "olhos"
    return "brasa" if ch in "ro" else "corpo"


def _camada_cao_t(x, y, ch):
    if ch in "tT":
        return "dentes"
    if ch in "nN":
        return "nariz"
    if ch == "e" or (ch == "y" and y < 8):
        return "olhos"
    if ch in "Oy" or (ch == "r" and y >= 9):
        return "boca"
    return "brasa" if ch == "o" else "corpo"


def _camada_cria(x, y, ch):
    return "fenda" if ch in "mMw" else "corpo"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "cao-infernal-a": (CAO_A, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cao-infernal-b": (CAO_B, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cria-vazio-a": (CRIA_A, "cria", ["corpo", "fenda"], _camada_cria),
    "cria-vazio-b": (CRIA_B, "cria", ["corpo", "fenda"], _camada_cria),
    "cria-vazio-a2": (CRIA_A2, "cria", ["corpo", "fenda"], _camada_cria),
    "cao-infernal-t": (CAO_T, "cao_t", ["corpo", "nariz", "brasa", "boca", "dentes", "olhos"], _camada_cao_t),
}


def cor(ident, ch):
    return PALETAS[CAMADAS[ident][1]][ch]


def imagem(ident):
    im = Image.new("RGBA", (16, 16))
    for y, l in enumerate(CAMADAS[ident][0]):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(cor(ident, ch)[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ids=None):
    for ident in ids or CAMADAS:
        grade, _, ordem, camada = CAMADAS[ident]
        assert len(grade) == 16 and all(len(l) == 16 for l in grade), (ident, [len(l) for l in grade])
        (base / "grades").mkdir(parents=True, exist_ok=True)
        (base / f"grades/{ident}.txt").write_text("\n".join(grade) + "\n", encoding="utf-8")
        listas = {c: [] for c in ordem}
        for y, l in enumerate(grade):
            for x, ch in enumerate(l):
                if ch != ".":
                    listas[camada(x, y, ch)].append(f"{x},{y},{cor(ident, ch)}")
        d = base / f"listas/{ident}"
        d.mkdir(parents=True, exist_ok=True)
        for k, v in listas.items():
            (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
        (d / "ordem.txt").write_text(",".join(ordem) + "\n", encoding="utf-8")
        print(ident, {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    gravar(pathlib.Path(sys.argv[1]), sys.argv[2:])
