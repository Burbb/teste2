"""Os símbolos de lugar em grade nativa (1E.4, 23/10/2026; protótipo, nada no jogo): a vila e a floresta, refeitas à
mão em 32×32 (e, para o mapa grande, a adaptação à mão em 48×48), no lugar das reduções da folha de referência da HUD 4
pixel (os lugar-*-32/40 do jogo; ver o LEIA-ME, "A origem dos ícones de lugar"). A redução antiga serviu de guia para
a composição e a identidade (a vila: a casa grande de enxaimel com a empena à esquerda, o telhado vermelho e a
chaminé, a casa pequena à direita, a janela acesa; a floresta: três pinheiros de alturas diferentes, o do meio mais
alto). O desenho é outro: as formas na grade, cores agrupadas, sem os detalhes miúdos nem a suavidade da imagem grande.

Como foi feito (registrado no LEIA-ME): a floresta pelas linhas de cada camada de copa escritas à mão (a largura e a
luz de cada linha, as árvores da frente por cima da do meio); a vila por uma construção à mão das formas (o telhado,
a empena, as paredes, as vigas, as janelas), depois limpa pixel a pixel na grade (a chaminé estreitada, as vigas
aliviadas, os contornos que faltavam). Uma letra por pixel; o contorno faz parte do desenho. A luz vem de cima e da
esquerda.
    python lugares.py .. [<id> ...]      # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "vila": {"a": "140c08",
             "1": "6e1e14", "2": "9a2e1c", "3": "b23a22", "4": "d0603a", "R": "8a2a1a",  # o telhado, do escuro ao claro
             "w": "c8b48a", "W": "a8906a",  # a parede caiada: a da empena, na luz, e a lateral, na sombra (baixada à noite)
             "b": "4a2e1a", "d": "3a2414",  # as vigas do enxaimel e a porta
             "y": "f2c050", "Y": "c8822a",  # a janela acesa
             "G": "7e7e86", "g": "5e5e66",  # a chaminé
             "V": "3f6f36", "v": "244628"},  # os arbustos
    "floresta": {"a": "0b130d",
                 "1": "17301c", "2": "244628", "3": "35602e", "4": "4f8038", "5": "7fa848",  # as copas
                 "t": "3e2614", "T": "6e4626"},  # os troncos
}
CAMADAS = {
    "vila": (["paredes", "enxaimel", "janelas", "telhado", "chamine", "plantas", "contorno"],
             {"a": "contorno", "1": "telhado", "2": "telhado", "3": "telhado", "4": "telhado", "R": "telhado",
              "w": "paredes", "W": "paredes", "b": "enxaimel", "d": "enxaimel", "y": "janelas", "Y": "janelas",
              "G": "chamine", "g": "chamine", "V": "plantas", "v": "plantas"}),
    "floresta": (["troncos", "copas", "luz", "contorno"],
                 {"a": "contorno", "1": "copas", "2": "copas", "3": "copas", "4": "luz", "5": "luz", "t": "troncos", "T": "troncos"}),
}
DESENHOS = {
    "lugar-vila-n32": ("vila", [
        "................................",
        "................................",
        "................................",
        "...............aaa..............",
        "...............aGa..............",
        "...............aGa..............",
        "......aaaaaaaaaaGaaaaa..........",
        ".....aR33333333aGa333a..........",
        "....aRWR3333333aGa3333a.........",
        "...aRwWWR22222211122222a........",
        "..aRwwbWWR22222222222222a.......",
        ".aRwwwbWWWR22222222222222a......",
        "aRwwwwbWWWWR11111111111111a.....",
        "aRbbbbbbbbbbR11111111111111a....",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaa....",
        "abbbbbbbbbbbbbbbbbbbbbbbbba.....",
        "abwwwbwwwwwbWWWWWWWbWWWWWa1a....",
        "abYyybwwwwwbWWYYYYWbWWWWa421a...",
        "abyyybwwwwwbWWyyyyWbWWWa42221a..",
        "abyyYbwwwwwbWWyyyyWbWWa4222221a.",
        "abwwwbwwwwwbWWWWWWWbWa422222221a",
        "abbbbbbbbbbbbbbbbbbba4222222221a",
        "abwwwbwwwwwbWWWWWWWaaaaaaaaaaaaa",
        "abwwwbwbbwwbWWWWWWWbabbbbbbbbbba",
        "abwwwbwddwwbWWWWWWWbabwwwwwwwwba",
        "abwwwbwddwwbWWWWWWWbabwYyywddwba",
        "abwwwbwddwwbWWWWWWWbabwyyywddwba",
        "abwwwbwddwwbWWWWWWWbabwyyywddwba",
        "abwwwbwddwVbWWWWWWVbabwwwwwddwba",
        "aaaaaaaaaVVVaaaaaVVVabwwwwwddwba",
        "....................aaaaaaaaaaaa",
        "................................",
    ]),
    "lugar-floresta-n32": ("floresta", [
        "................................",
        "................................",
        "...............aa...............",
        "..............a54a..............",
        "..............a43a..............",
        ".............a5432a.............",
        "............a544322a............",
        "...........a22111111a...........",
        "...........aa544322aa...........",
        "...........a54433222a...aa......",
        "..........a5443332221a.a54a.....",
        ".........a544433322211a5432a....",
        "......aa.a22111111111a221111a...",
        ".....a54aaaa54433322aaa5432aa...",
        "....a5432aa5444333222a544322a...",
        "...a221111a444433332a54433222a..",
        "...aa5432aa44443333a2211111111a.",
        "...a544322a11111111aaa544322aaa.",
        "..a54433222a44433322a54433222a..",
        ".a2211111111a443333a5444333222a.",
        ".aaa544322aaa44333a544443333222a",
        "..a54433222a444333a221111111111a",
        ".a5444333222a43333aaa54433322aaa",
        "a544443333222a11111a5444333222a.",
        "a221111111111aatTaa544443333222a",
        "aaaaaatTaaaaaaatTaa221111111111a",
        ".....atTa.....atTaaaaaaatTaaaaaa",
        ".....atTa.....atTa.....atTa.....",
        ".....atTa.....atTa.....atTa.....",
        ".....atTa.....aaaa.....atTa.....",
        ".....aaaa..............aaaa.....",
        "................................",
    ]),
    # a adaptação à mão em 48 nativos para o mapa grande: a mesma composição, as formas escritas para a grade de 48
    "lugar-vila-n48": ("vila", [
        "................................................",
        "................................................",
        "................................................",
        "......................aaaa......................",
        "......................aaaa......................",
        "......................aGga......................",
        "......................aGga......................",
        "......................aGga......................",
        "......................aGga......................",
        ".........aaaaaaaaaaaaaaGgaaaaaaa................",
        "........aR333333333333aGga33333a................",
        ".......aRWR33333333333aGga333333a...............",
        "......aRwWWR333333333333333333333a..............",
        ".....aRwwbWWRRRRRRRRRRRRRRRRRRRRRRa.............",
        "....aRwwwbWWWR222222222222222222222a............",
        "...aRwwwwbWWWWR222222222222222222222a...........",
        "..aRbbbbbbbbbbbR222222222222222222222a..........",
        ".aRwwwwwwbWWWWWWR111111111111111111111a.........",
        "aRwwwwwwwbWWWWWWWR111111111111111111111a........",
        "aRwwwwwwwbWWWWWWWWR111111111111111111111a.......",
        "abbbbbbbbbbbbbbbbba.............................",
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa......",
        "abbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbba........",
        "abwwwwwwwbwwwwwwwwbWWWWWWWWWWbWWWWWWWWba........",
        "abwYYYYwwbwwwwwwwwbWWWYYbYYWWbWWWWWWWWa1a.......",
        "abwYyyywwbwwwwwwwwbWWWYybyyWWbWWWWWWWa421a......",
        "abwbbbbwwbwwwwwwwwbWWWYybyyWWbWWWWWWa42221a.....",
        "abwYyyywwbwwwwwwwwbWWWYybyyWWbWWWWWa4222221a....",
        "abwYyyywwbwwwwwwwwbWWWYybyyWWbWWWWa422222221a...",
        "abwwwwwwwbwwwwwwwwbWWWWWWWWWWbWWWa42222222221a..",
        "abwwwwwwwbwwwwwwwwbWWWWWWWWWWbWWa4222222222221a.",
        "abwwwwwwwbwwwwwwwwbWWWWWWWWWWbWa422222222222221a",
        "abbbbbbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaaaaaaaaa",
        "abwwwwwwwbwbbbbwwwbWWWWWWWWWWbWWabbbbbbbbbbbbba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwwwwwwwwwwwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwYYYYwwwwwwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwYyyywwwwwwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwYyyywwdddwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwYyyywwdddwba.",
        "abwwwwwwwbwddydwwwbWWWWWWWWWWbWWabwwwwwwwdddwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwwwwwwwdddwba.",
        "abwwwwwwwbwddddwwwbWWWWWWWWWWbWWabwwwwwwwdddwba.",
        "abwwwwwwwbwddddwVwbWWWWWWWWWWVWWabwwwwwwwdddwba.",
        "abwwwwwwwbwddddVVwbWWWWWWWWWVVVWabwwwwwwwdddwba.",
        "aaaaaaaaaaaaaavVVvaaaaaaaaavVVVvaaaaaaaaaaaaaaa.",
        "................................................",
        "................................................",
        "................................................",
    ]),
    "lugar-floresta-n48": ("floresta", [
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        ".......................aa.......................",
        "......................a54a......................",
        ".....................a5432a.....................",
        "....................a544331a....................",
        "...................a54433221a...................",
        "..................a2211111111a..................",
        "..................aa54433221aa..................",
        "..................a5444333221a..................",
        ".................a544443333221a.................",
        "................a54444333322221a................",
        "...............a2211111111111111a..aa...........",
        "...............aaa544443333221aaa.a54a..........",
        "............aa..a54444333322221a.a5432a.........",
        "...........a54aa5444443333322221a221111a........",
        "..........a5432a4444433333222222aa5432aa........",
        ".........a221111a444433333322222a544331a........",
        ".........aa5432aa11111111111111a54433221a.......",
        ".........a544331a4444433333222a2211111111a......",
        "........a54433221a444333332222aa54433221aa......",
        ".......a2211111111a44333333222a5444333221a......",
        ".......aa54433221aa4433333332a544443333221a.....",
        ".......a5444333221a433333332a22111111111111a....",
        "......a544443333221a11111111aaa5444333221aaa....",
        ".....a22111111111111a33333322a544443333221a.....",
        ".....aaa5444333221aaa3333333a54444333322221a....",
        "......a544443333221a3333333a5444443333322221a...",
        ".....a54444333322221a33333a544444333332222221a..",
        "....a5444443333322221a333a22111111111111111111a.",
        "...a544444333332222221a11aaaaaaaaaatTaaaaaaaaaa.",
        "..a22111111111111111111aTTaaaaaaaaatTaa.........",
        "..aaaaaaaaaatTaaaaaaaaaaTTa.......atTa..........",
        "...........atTa.......atTTa.......atTa..........",
        "...........atTa.......atTTa.......atTa..........",
        "...........atTa.......aaaaa.......atTa..........",
        "...........atTa...................aaaa..........",
        "...........aaaa.................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
        "................................................",
    ]),
}


def tipo(ident):
    return DESENHOS[ident][0]


def ordem(ident):
    return CAMADAS[tipo(ident)][0]


def lado(ident):
    g = DESENHOS[ident][1]
    return len(g[0]), len(g)


def imagem(ident):
    g, pal = DESENHOS[ident][1], PALETAS[tipo(ident)]
    w, h = lado(ident)
    im = Image.new("RGBA", (w, h))
    for y, l in enumerate(g):
        for x, ch in enumerate(l):
            if ch != ".":
                im.putpixel((x, y), tuple(int(pal[ch][i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    return im


def gravar(base, ident):
    g, pal = DESENHOS[ident][1], PALETAS[tipo(ident)]
    w, h = lado(ident)
    assert all(len(l) == w for l in g), (ident, [len(l) for l in g])
    (base / "grades").mkdir(parents=True, exist_ok=True)
    (base / f"grades/{ident}.txt").write_text("\n".join(g) + "\n", encoding="utf-8")
    nomes, por_letra = CAMADAS[tipo(ident)]
    listas = {c: [] for c in nomes}
    for y, l in enumerate(g):
        for x, ch in enumerate(l):
            if ch != ".":
                listas[por_letra[ch]].append(f"{x},{y},{pal[ch]}")
    d = base / f"listas/{ident}"
    d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    (d / "ordem.txt").write_text(",".join(nomes) + "\n", encoding="utf-8")
    print(ident, f"{w}×{h}", {k: len(v) for k, v in listas.items()})


if __name__ == "__main__":
    for ident in sys.argv[2:] or DESENHOS:
        gravar(pathlib.Path(sys.argv[1]), ident)
