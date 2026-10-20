"""O segundo e o terceiro retoques da L7 (20/10/2026, apontados pelo Jean nas folhas):
  - o segundo (RETOQUE, na folha do ba650ddd; o antes em anterior_ba650ddd/): o pixel perdido e a ponta de sombra na
    beira esquerda do alto do punho da luva da esquerda;
  - o terceiro (RETOQUE_3, na folha do 9a9e2281; o antes em anterior_9a9e2281/): o pixel prata na borda da malha da
    direita, junto da faixa de couro do pulso.
Cada item: (x, y, o pixel esperado antes, o novo, o porquê); o script confere o "antes", grava a grade nova
(grades/L7.txt) e as listas por camada para o pintar.lua (listas/retoque2/ ou listas/retoque3/<camada>.lua).
    python retoque2.py <pasta da L7>        # o segundo
    python retoque2.py <pasta da L7> 3      # o terceiro
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
RETOQUE_3 = [
    (20, 21, "3", "#", "o pixel prata solto abaixo da malha das costas da mão da direita, na linha da faixa de couro do "
                       "pulso: contorno preto, fechando a beira da malha com a faixa (sugestão do Jean)"),
]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    terceiro = len(sys.argv) > 2 and sys.argv[2] == "3"
    lista = RETOQUE_3 if terceiro else RETOQUE
    antes = "anterior_9a9e2281" if terceiro else "anterior_ba650ddd"
    g = [list(l) for l in (base / antes / "L7.txt").read_text(encoding="utf-8").split("\n")[:32]]
    erros = [(x, y, g[y][x], a) for x, y, a, _, _ in lista if g[y][x] != a]
    if erros: raise SystemExit(f"o pixel de antes não confere: {erros}")
    listas = {}
    for x, y, a, n, _ in lista:
        g[y][x] = n
        ca, cn = camada(a), camada(n)
        if ca and ca != cn: listas.setdefault(ca, []).append(f"{x},{y},00000000")
        if cn: listas.setdefault(cn, []).append(f"{x},{y},{cor(n)}")
    (base / "grades/L7.txt").write_text("\n".join("".join(l) for l in g) + "\n", encoding="utf-8")
    d = base / ("listas/retoque3" if terceiro else "listas/retoque2"); d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print(len(lista), "pixels;", {k: len(v) for k, v in listas.items()})
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(g)))
