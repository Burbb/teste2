"""A limpeza localizada da L7 (20/10/2026, pedido do Jean): a mesma luva, mais limpa, sem mudar a silhueta, a pose, os
dedos nem a malha. A imagem gerada (ferramentas/arte/referencias/Luvas/luvas-par-gerada.webp) é a referência de
acabamento: quais sombras são dobras do couro e como os planos se ligam. A versão anterior fica em
anterior_8a844975/.
LIMPEZA abaixo: (x, y, o pixel esperado antes, o novo, o porquê). O script confere o "antes" na grade, grava a grade nova
(grades/L7.txt) e as listas por camada para o pintar.lua aplicar na fonte (listas/limpeza/<camada>.lua: o pixel novo
na sua camada e o apagamento, com alfa 0, na camada que ele deixa).
    python limpeza.py <pasta da L7>
"""
import pathlib
import sys

FERRO = ["0e0f11", "1a1c20", "282b31", "383c44", "4c5159", "646a73", "848b94", "b0b6bd", "e4e8ec"]
COURO = dict(b="251412", c="3a1f1a", d="522c23", e="6b3b2d", f="86503c")

TOCO = "o toco escuro entre as pontas dos dedos da esquerda (sobra da captura): sai, ficando o vão entre os dedos"
PALMA = "a faixa cinza no meio da palma da esquerda: a sombra do couro (a dobra da palma, na imagem gerada)"
DEDO = "o ponto cinza no dedo: a sombra do couro do mesmo dedo"
RECORTE = "o recorte preto acidental no couro: a sombra escura do couro (o vão de dedo não continua na palma)"
BEIRA = "o preto que engrossava a beira do polegar: a sombra do couro, ficando o contorno de 1 px"
FAIXA = "a faixa de couro do pulso da direita, contínua (os pretos a cortavam): a sombra da malha em cima"
MALHA = "a fileira de pontos quase pretos no punho da direita: o xadrez da malha, como as fileiras vizinhas"
FURO = "o furo na malha do punho da direita: o xadrez da malha"
BAINHA = "a beirada de couro de baixo do punho da direita, contínua (os pretos e o claro solto a cortavam)"
JUNCAO = "o pixel solto na junção da malha com o couro: o contorno da junção"
LIMPEZA = [
    (13, 1, "#", ".", TOCO), (13, 2, "2", ".", TOCO),
    (11, 12, "2", "c", PALMA), (11, 13, "3", "c", PALMA), (12, 13, "2", "b", PALMA), (11, 14, "2", "b", PALMA),
    (12, 14, "3", "c", PALMA), (11, 15, "3", "c", PALMA), (7, 12, "2", "c", PALMA),
    (14, 5, "2", "c", DEDO), (15, 8, "2", "c", DEDO), (21, 6, "2", "c", DEDO), (21, 7, "1", "c", DEDO), (21, 8, "1", "c", DEDO),
    (15, 9, "1", "c", RECORTE), (13, 13, "#", "b", RECORTE), (13, 14, "#", "b", RECORTE), (10, 18, "#", "b", RECORTE),
    (8, 17, "#", "b", RECORTE), (10, 21, "1", "c", RECORTE), (13, 22, "2", "c", RECORTE), (5, 24, "1", "c", RECORTE),
    (9, 9, "1", "c", BEIRA), (9, 10, "1", "c", BEIRA),
    (21, 21, "#", "b", FAIXA), (22, 21, "#", "c", FAIXA), (23, 21, "#", "c", FAIXA), (24, 21, "#", "b", FAIXA),
    (26, 20, "#", "c", FAIXA), (27, 20, "#", "d", FAIXA),
    (19, 24, "3", "3", MALHA), (20, 24, "5", "6", MALHA), (21, 24, "1", "4", MALHA), (22, 24, "6", "6", MALHA),
    (23, 24, "1", "4", MALHA), (24, 24, "6", "6", MALHA), (25, 24, "1", "4", MALHA), (26, 24, "6", "6", MALHA),
    (27, 24, "4", "4", MALHA), (28, 24, "1", "6", MALHA), (29, 24, "5", "3", MALHA),
    (24, 27, "#", "4", FURO),
    (18, 28, "1", "#", BAINHA), (19, 28, "e", "e", BAINHA), (20, 28, "d", "d", BAINHA), (21, 28, "4", "d", BAINHA),
    (22, 28, "6", "d", BAINHA), (23, 28, "#", "d", BAINHA), (24, 28, ".", "d", BAINHA), (25, 28, "#", "d", BAINHA),
    (26, 28, "7", "d", BAINHA), (27, 28, "d", "c", BAINHA), (28, 28, "d", "c", BAINHA),
    (24, 29, "#", "c", BAINHA), (21, 29, "d", "c", BAINHA), (22, 29, "d", "c", BAINHA), (23, 29, "d", "c", BAINHA),
    (25, 29, "d", "c", BAINHA), (26, 29, "d", "c", BAINHA),
    (19, 23, "5", "#", JUNCAO), (20, 23, "b", "#", JUNCAO), (28, 23, "5", "#", JUNCAO),
]


def camada(ch):
    return None if ch == "." else "contorno" if ch == "#" else "malha" if ch.isdigit() else "couro"


def cor(ch):
    return "08080a" if ch == "#" else FERRO[int(ch)] if ch.isdigit() else COURO[ch]


if __name__ == "__main__":
    base = pathlib.Path(sys.argv[1])
    g = [list(l) for l in (base / "anterior_8a844975/L7.txt").read_text(encoding="utf-8").split("\n")[:32]]
    erros = [(x, y, g[y][x], a) for x, y, a, _, _ in LIMPEZA if g[y][x] != a]
    if erros: raise SystemExit(f"o pixel de antes não confere: {erros}")
    listas = {}
    for x, y, a, n, _ in LIMPEZA:
        g[y][x] = n
        ca, cn = camada(a), camada(n)
        if ca and ca != cn: listas.setdefault(ca, []).append(f"{x},{y},00000000")
        if cn: listas.setdefault(cn, []).append(f"{x},{y},{cor(n)}")
    (base / "grades/L7.txt").write_text("\n".join("".join(l) for l in g) + "\n", encoding="utf-8")
    d = base / "listas/limpeza"; d.mkdir(parents=True, exist_ok=True)
    for k, v in listas.items():
        (d / f"{k}.lua").write_text(f'return "{";".join(v)}"\n', encoding="utf-8")
    print(len(LIMPEZA), "pixels;", {k: len(v) for k, v in listas.items()})
    print("\n".join(f"{y:2d} {''.join(l)}" for y, l in enumerate(g)))
