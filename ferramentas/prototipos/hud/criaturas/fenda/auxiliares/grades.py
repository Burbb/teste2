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


def _camada_cria(x, y, ch):
    return "fenda" if ch in "mMw" else "corpo"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "cao-infernal-a": (CAO_A, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cao-infernal-b": (CAO_B, "cao", ["corpo", "brasa", "boca", "dentes", "olhos"], _camada_cao),
    "cria-vazio-a": (CRIA_A, "cria", ["corpo", "fenda"], _camada_cria),
    "cria-vazio-b": (CRIA_B, "cria", ["corpo", "fenda"], _camada_cria),
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
