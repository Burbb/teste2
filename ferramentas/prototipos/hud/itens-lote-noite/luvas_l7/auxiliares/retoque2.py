"""O segundo retoque da L7 (20/10/2026, apontado pelo Jean na folha do ba650ddd): o pixel perdido e a ponta de sombra na
beira esquerda do alto do punho da luva da esquerda. O antes fica em anterior_ba650ddd/.
RETOQUE abaixo: (x, y, o pixel esperado antes, o novo, o porquê); o script confere o "antes", grava a grade nova
(grades/L7.txt) e as listas por camada para o pintar.lua (listas/retoque2/<camada>.lua).
    python retoque2.py <pasta da L7>
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from limpeza import camada, cor  # noqa: E402

RETOQUE = [
    (4, 20, "f", "4", "o pixel perdido: o couro claro solto no canto da malha do punho; entra no xadrez da malha, no tom de "
                      "sombra do alto do punho"),
    (2, 20, "#", ".", "a ponta de sombra para a esquerda: o contorno sai, ficando o de (3, 20), alinhado com as linhas de baixo"),
]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g = [list(l) for l in (base / "anterior_ba650ddd/L7.txt").read_text(encoding="utf-8").split("\n")[:32]]
    erros = [(x, y, g[y][x], a) for x, y, a, _, _ in RETOQUE if g[y][x] != a]
    if erros: raise SystemExit(f"o pixel de antes não confere: {erros}")
    listas = {}
    for x, y, a, n, _ in RETOQUE:
        g[y][x] = n
        ca, cn = camada(a), camada(n)
        if ca and ca != cn: listas.setdefault(ca, []).append(f"{x},{y},00000000")
        if cn: listas.setdefault(cn, []).append(f"{x},{y},{cor(n)}")
    (base / "grades/L7.txt").write_text("\n".join("".join(l) for l in g) + "\n", encoding="utf-8")
    d = base / "listas/retoque2"; d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print(len(RETOQUE), "pixels;", {k: len(v) for k, v in listas.items()})
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(g)))
