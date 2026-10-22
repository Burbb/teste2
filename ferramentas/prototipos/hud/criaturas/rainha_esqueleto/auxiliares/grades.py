"""O par da 1E.3 depois do Rei Troll e da Aranha (21/10/2026, pedido do Jean): a Rainha Aracnídea e o Esqueleto, duas
propostas de cada, cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno preto, cores agrupadas, a
luz da esquerda), vistas a 2× na carta (32 px) e, o Esqueleto, a 3× no Bestiário e no mural (48 px).

  - Rainha Aracnídea (o guardião `rainha_aracnidea` da floresta: "teias grossas como cordas cobrem as árvores; algo
    enorme desce do alto, com olhos demais para contar"; teia, veneno, invocar aranhas; na fase 2, "guincha e seus
    filhotes despencam das copas"): da mesma espécie que a Aranha gigante da 1.167.0 (a mesma paleta marrom, as
    quelíceras e as patas articuladas), com a identidade de chefe na construção e no vermelho do veneno. A, de frente e
    enorme: o abdome que enche o alto do quadro com a ampulheta vermelha, a cabeça menor embaixo com duas fileiras de
    olhos, as quelíceras com as presas vermelhas, as patas pelos lados. B, descendo do alto: o fio de teia no topo, o
    abdome com a marca, a cabeça com os olhos e as presas para baixo, as oito patas abertas em estrela, grossas.
  - Esqueleto (`esqueleto`, morto-vivo: "ossos animados por ódio antigo; veneno não faz nada; luz sagrada faz muito"): o
    osso envelhecido (a luz da esquerda, a sombra à direita), as órbitas fundas e vazias, o nariz, os dentes e a mandíbula
    separada, sem brilho nos olhos nem nada mágico. A, de frente: o crânio, as bochechas encovadas, as vértebras do
    pescoço e as clavículas descendo para os ombros. B, em três quartos para a esquerda: a órbita de perto maior que a de
    longe, a mandíbula um pouco caída, a coluna e o ombro de lado.

    python grades.py <pasta do par> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

CORES = {
    # a Rainha: o corpo da Aranha gigante (o escuro, o meio, a luz, as juntas, os olhos), o vermelho da marca e do veneno
    "Q": "17120f", "R": "3a2f28", "S": "5e4c40", "U": "86705e", "V": "b8a48e", "P": "e08a34", "u": "b06a28", "k": "0e0b08", "G": "7a2018", "g": "b8402e",
    # o Esqueleto: o osso do claro ao escuro e as órbitas
    "W": "cfc6b0", "O": "d6cba6", "o": "aa9e7c", "d": "766a50", "D": "3e3628",
}

RAINHA_A = [
    "V..QRRSSSSRRQ..V",
    "SV.RSSgGGgSSR.VS",
    ".SQRSSSGGSSSRQS.",
    ".VQRSSgGGgSSRQV.",
    "VS.QRSSSSSSRQ.SV",
    "SQ..QRRSSRRQ..QS",
    "Q.VQRUUUUUURQV.Q",
    ".VSRPQPQQPQPRSV.",
    "VSQRUuPQQPuURQSV",
    "SQ.RSUSRRSUSR.QS",
    "Q..RUSSRRSSUR..Q",
    "...QSSRRRRSSQ...",
    "...QRgS..SgRQ...",
    "....Rg....gR....",
    "................",
    "................",
]
RAINHA_B = [
    ".V.....V.....V..",
    ".SV....V....VS..",
    "..SS..kRk..SS...",
    "...SS.RggR.SS...",
    "VS..SRgGGgRS..SV",
    ".SSS.RSggSR.SSS.",
    "...SQRUUUURQS...",
    ".VSSRPQPPQPRSSV.",
    "VS..RuPQQPuR..SV",
    "...SRSUSSUSRS...",
    "..SS.QSRRSQ.SS..",
    ".SS..RgSSgR..SS.",
    "VS...Rg..gR...SV",
    ".....g....g.....",
    "................",
    "................",
]
ESQUELETO_A = [
    "................",
    ".....dOOOod.....",
    "....oOWWOOod....",
    "...oOWOOOOood...",
    "...OOOOOOOoodd..",
    "...OkkkOOkkkdd..",
    "...okkkdOkkkdd..",
    "...dOkdOOdkodd..",
    "....dOOkkoodd...",
    "....dOdkdood....",
    "....oOkOkokd....",
    "....DDDDDDDD....",
    "....dokOkokd....",
    ".....doooodd....",
    "..dd...dd...dd..",
    ".oOod.dOOd.doOo.",
]
ESQUELETO_B = [
    "................",
    "......dOOOd.....",
    ".....oOWOOOd....",
    "....oOWOOOOod...",
    "...oOOOOOOOood..",
    "...kkkOOOkkood..",
    "..dkkkdOOkkodd..",
    "..OOkdOOdoood...",
    "..ddkkOOoodd....",
    "..OkOkOkood.....",
    "..DDDDDDdd......",
    "...dkOkOod......",
    "....doooddd.oo..",
    "........dOd.OOo.",
    ".......dOdOOooOo",
    "......dOdOoooooO",
]


def _rainha(patas, marca_ate):
    return lambda x, y, ch: ("olhos" if ch in "Pu" else "marca" if ch in "Gg" and y <= marca_ate else "presas" if ch in "Gg"
                             else "patas" if patas(x, y, ch) else "corpo")


def _esqueleto(ossos):
    return lambda x, y, ch: "orbitas" if ch == "k" else "pescoco" if ossos(x, y) else "cranio"


CAMADAS = {
    "rainha-a": (RAINHA_A, ["patas", "corpo", "marca", "presas", "olhos"],
                 _rainha(lambda x, y, ch: x <= 2 or x >= 13, 5)),
    "rainha-b": (RAINHA_B, ["patas", "corpo", "marca", "presas", "olhos"],
                 _rainha(lambda x, y, ch: not 4 <= x <= 11 or ch == "V", 5)),
    "esqueleto-a": (ESQUELETO_A, ["pescoco", "cranio", "orbitas"], _esqueleto(lambda x, y: y >= 14)),
    "esqueleto-b": (ESQUELETO_B, ["pescoco", "cranio", "orbitas"], _esqueleto(lambda x, y: y >= 13 or (y == 12 and x >= 11))),
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
