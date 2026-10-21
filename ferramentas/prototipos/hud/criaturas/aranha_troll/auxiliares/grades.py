"""O par da 1E.3 depois dos animais (21/10/2026, pedido do Jean): a Aranha Gigante e o Troll, duas propostas de cada,
cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno preto, cores agrupadas, a luz da esquerda). O
jogo mostra a 2× na carta da luta e no rastro dos contratos (32 px) e a 3× no Bestiário, no mural e na faixa do mestre
caçador (48 px); não há desenho nativo de 32 nem de 48.

  - Aranha gigante (`aranha`, fera do Bosque: "tecem armadilhas entre as árvores; seu veneno paralisa antes de matar"):
    marrom-escura e peluda, os olhos pretos com um brilho frio (sem nada de mágico), as quelíceras com as presas de
    ponta avermelhada. A, de frente e de perto: o abdome atrás da cabeça com a marca clara, a carapaça, os olhos em
    fileira, as quelíceras e as presas, os palpos e as patas em arco dos dois lados. B, de lado, em ameaça: a cabeça
    à esquerda com os olhos e as presas, as patas da frente erguidas, o abdome grande atrás com a marca em cruz, as
    outras patas descendo até a base.
  - Troll da montanha (`troll`, gigante: "regeneram quase tudo, menos o fogo"; lento, muito forte, da montanha): a pele
    cinza-esverdeada de pedra, o musgo crescendo nele, os olhos pequenos e amarelos no fundo das órbitas. A, de frente:
    a cabeça enorme que enche o quadro, a testa baixa com a sombra das sobrancelhas, o nariz grande, a boca fechada e
    caída com as presas de baixo, o musgo no alto e nos ombros. B, de perfil para a esquerda: a cabeça baixa e pequena
    na frente de uma corcunda de musgo e pedra, o nariz comprido, a sobrancelha pesada, o queixo projetado com a presa.

    python grades.py <pasta do par> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

CORES = {
    # a aranha: o corpo do escuro ao claro, a marca, o olho e o brilho frio, as presas
    "k": "1e1813", "K": "3a2e24", "M": "5c4a38", "L": "7e664c", "H": "a68a64", "a": "b09a5a", "E": "060505", "x": "8a8a84", "F": "d2c09a", "f": "7a3a24",
    # o troll: a pele de pedra, a luz do nariz, as sombras, o musgo, os olhos, a boca, as presas
    "G": "8a8f80", "J": "a6ac98", "g": "6a7062", "d": "4c5248", "D": "30342e", "O": "5e6a3e", "o": "3e4a2c", "y": "c0a040", "e": "0e0c0a", "m": "2a1a14", "T": "d8d0b4",
}

ARANHA_A = [
    "................",
    ".....kKKKKk.....",
    "....kKaKKaKk....",
    ".HM.kKKaaKKk.MH.",
    "M..MLHLLLLHLM..M",
    "M.HMEMLLLLMEMH.M",
    "MM.MLxEMMxELM.MM",
    "M.MMLEEKKEELMM.M",
    "M.M.MHKKKHKM.M.M",
    ".M.M.KHkkHK.M.M.",
    ".M.M.FK..KF.M.M.",
    ".M...f....f...M.",
    ".M............M.",
    "................",
    "................",
    "................",
]
ARANHA_B = [
    "...H............",
    "..M.H...kKKKk...",
    "..M.M..kKKaKKk..",
    ".M..M.kKKaaaKKk.",
    ".M.M..kKKKaKKKKk",
    "..M.MLkKKaaaKKKk",
    "...MLHLHkKaKKKKk",
    "..MLExELKkKKKKKk",
    ".MHLLLLLMKKKKKk.",
    "FMKKKKKKMkKKKk..",
    "f.M.M.M.KkkkK...",
    ".M..M.M..M..M...",
    "M..M..M...M..M..",
    "M..M...M..M...M.",
    "..M....M...M..M.",
    "..M.....M..M....",
]
TROLL_A = [
    "................",
    "...OoO...OOo....",
    "..OGGGGGGGGgo...",
    ".oGGGGGGGGGggd..",
    ".GGdDDGGGDDdgdd.",
    ".GGDyeDGGDeyDdd.",
    ".GGGddJJGGddgdD.",
    ".oGGGGJGGggggdD.",
    "..GGGdGGdgggdgD.",
    "..dGGTmmmTgddD..",
    "..dGmGGGGGmgdD..",
    "...dGGGGGggddD..",
    "...ddGGGggddD...",
    ".OoodddddddDDooO",
    "OoOOoodddDDoOoOO",
    "OOoOOOoooooOOoOO",
]
TROLL_B = [
    "................",
    "................",
    "......OoO.......",
    "....oGGGGo...OO.",
    "...GGGGGGgd.OoOo",
    "..dDDGGGggdOoOOo",
    ".GDyeDGgggdOOoOo",
    "GJJGGGGgggdOoOoO",
    "GJGGdGGggdOOoOOO",
    ".dGGTGGgddOoOOoO",
    ".dmmmGGgddOoOoOo",
    "..dGGGgdddDoOOoO",
    "...dddddDDoOOoOO",
    ".OoOooDDDoOoOOoO",
    "OoOOoOoOoOOoOoOO",
    "OOoOOoOOOoOOoOOO",
]


def _aranha(patas):
    return lambda x, y, ch: "olhos" if ch in "Ex" else "presas" if ch in "Ff" else "patas" if patas(x, y) else "corpo"


TROLL = lambda x, y, ch: "musgo" if ch in "Oo" else "rosto" if ch in "yemT" else "pele"
CAMADAS = {
    "aranha-a": (ARANHA_A, ["patas", "corpo", "presas", "olhos"], _aranha(lambda x, y: x <= 3 or x >= 12)),
    "aranha-b": (ARANHA_B, ["patas", "corpo", "presas", "olhos"],
                 _aranha(lambda x, y: (y <= 6 and x <= 5) or (y >= 10 and not (y == 10 and 8 <= x <= 12)))),
    "troll-a": (TROLL_A, ["musgo", "pele", "rosto"], TROLL),
    "troll-b": (TROLL_B, ["musgo", "pele", "rosto"], TROLL),
}


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
