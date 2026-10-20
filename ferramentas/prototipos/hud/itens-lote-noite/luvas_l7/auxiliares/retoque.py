"""O retoque localizado da L7 (20/10/2026, pedido do Jean), sobre a limpeza do 10772117: a forma e a composição ficam.
A imagem gerada (ferramentas/arte/referencias/Luvas/luvas-par-gerada.webp) é o apoio para as dobras do couro. A versão
anterior fica em anterior_10772117/.
RETOQUE abaixo: (x, y, o pixel esperado antes, o novo, o porquê). O script confere o "antes", grava a grade nova
(grades/L7.txt) e as listas por camada para o pintar.lua (listas/retoque/<camada>.lua).
    python retoque.py <pasta da L7>
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from limpeza import camada, cor  # noqa: E402

DOBRA = "a dobra da base do polegar na palma da esquerda, contínua em diagonal (como na imagem gerada)"
SOLTO = "o escuro solto na palma, fora da dobra: o tom médio do couro"
SOMBRA = "a sombra logo abaixo da dobra (o volume)"
PULSO = "a costura do encontro da palma com o pulso, contínua em marrom escuro (o preto e o marrom alternados a serrilhavam)"
PUNHO = ("o canto de cima da malha do punho da esquerda: o mesmo xadrez da malha, com os tons de sombra do alto do punho "
         "(o claro solto ao lado de um quase preto chamava a atenção sozinho)")
RETOQUE = [
    (12, 14, "c", "b", DOBRA), (11, 15, "c", "b", DOBRA),
    (7, 12, "c", "d", SOLTO), (11, 12, "c", "d", SOLTO), (13, 12, "c", "d", SOLTO), (12, 13, "b", "d", SOLTO),
    (11, 14, "b", "d", SOLTO), (13, 15, "c", "d", SOLTO),
    (13, 14, "b", "c", SOMBRA), (14, 15, "b", "c", SOMBRA),
    (11, 19, "#", "b", PULSO), (12, 19, "#", "b", PULSO), (14, 19, "c", "b", PULSO), (15, 19, "#", "b", PULSO),
    (16, 19, "#", "b", PULSO),
    (5, 19, "5", "4", PUNHO), (6, 19, "3", "2", PUNHO), (7, 19, "2", "4", PUNHO), (5, 20, "3", "2", PUNHO),
    (6, 20, "1", "4", PUNHO), (7, 20, "3", "2", PUNHO),
]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g = [list(l) for l in (base / "anterior_10772117/L7.txt").read_text(encoding="utf-8").split("\n")[:32]]
    erros = [(x, y, g[y][x], a) for x, y, a, _, _ in RETOQUE if g[y][x] != a]
    if erros: raise SystemExit(f"o pixel de antes não confere: {erros}")
    listas = {}
    for x, y, a, n, _ in RETOQUE:
        g[y][x] = n
        ca, cn = camada(a), camada(n)
        if ca and ca != cn: listas.setdefault(ca, []).append(f"{x},{y},00000000")
        if cn: listas.setdefault(cn, []).append(f"{x},{y},{cor(n)}")
    (base / "grades/L7.txt").write_text("\n".join("".join(l) for l in g) + "\n", encoding="utf-8")
    d = base / "listas/retoque"; d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print(len(RETOQUE), "pixels;", {k: len(v) for k, v in listas.items()})
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(g)))
