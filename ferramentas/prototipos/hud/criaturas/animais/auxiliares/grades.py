"""Os animais do patrulheiro (21/10/2026, pedido do Jean): o Urso Pardo e o Falcão Peregrino, duas propostas de cada,
cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno preto, cores agrupadas, a luz da esquerda). O
jogo mostra o animal a 2× (32 px) na carta da luta e no painel da comitiva; hoje os dois usam os sprites `fera` e
`voador`, que continuam como estão para todos os outros usos.

  - Urso Pardo (`urso`, classes.COMPANHEIROS: "lento e resistente; atrai golpes e às vezes atordoa"): o urso marrom, a
    cabeça larga, as orelhas pequenas e redondas, o focinho claro e o volume do pelo; o começo do pescoço sem ombros
    nem peito (o problema corrigido no lobo). A, de frente: a cabeça larga que enche o quadro, as orelhas nos cantos, a
    sombra da testa sobre os olhos pequenos, o focinho claro com o nariz, o pescoço que desce para trás. B, de perfil
    para a esquerda: o focinho comprido na cor do pelo com a ponta clara e o nariz, a orelha redonda, a linha da boca, a
    nuca e o pescoço grosso indo para a direita.
  - Falcão Peregrino (`falcao`: "frágil, mas veloz e certeiro"): o capacete cinza-escuro na cabeça e a faixa escura
    descendo do olho (o "bigode" do peregrino), o anel amarelo do olho e a cera amarela do bico, o bico curvo cinza com
    a ponta escura, a garganta clara e o peito creme com as pintas. A, de perfil para a esquerda, em close: a cabeça
    grande no quadro, o bico curvo na frente, o começo do pescoço. B, em três quartos: a cabeça menor no alto à
    esquerda, o peito e a asa dobrada em cinza-azulado à direita.

    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import pathlib
import sys

CORES = {
    # o urso: o pelo do claro ao escuro, o focinho claro, o nariz e o olho, o fundo da orelha
    "B": "9a6a40", "b": "74502e", "d": "553820", "D": "36240f", "Z": "b89668", "z": "8e6e4a", "k": "17140f", "n": "3a2618",
    # o falcão: o cinza-azulado, o capacete escuro, a garganta e o peito, as pintas, o amarelo, o bico, o olho
    "S": "7a8494", "s": "58626f", "h": "2a2f38", "c": "e2d8c0", "C": "a8a08c", "y": "d8b040", "g": "6a6e76", "E": "101216",
    # a transposição das referências geradas (21/10/2026): o urso severo e o falcão de máscara
    "O": "b8844e", "N": "241812", "Q": "c49a6c", "q": "9a7450", "K": "1e1410", "a": "b07a40", "L": "8a9ab8", "V": "667694", "v": "4a5674", "m": "1e2230", "W": "efe6d2", "w": "c4b89e", "I": "f4cc3a", "J": "d89a1c", "e": "0c0c10", "G": "6a7a96", "R": "3e4a62", "X": "2a3040",
}

URSO_A = [
    "................",
    "..bdb......bdb..",
    ".bBnbbbbbbbbnbd.",
    ".bBBbbbbbbbbbbd.",
    "bBBbbdbbbbdbbbdd",
    "bBBbbkbbbbkbbddD",
    "bBbbbbZZZZbbbddD",
    "dbbbbZZkkZZbbddD",
    "dbbbbZzzzzZbbdD.",
    ".dbbbbzzzzbbbdD.",
    ".ddbbbbbbbbbddD.",
    "..ddbbbbbbbddD..",
    "...dbbbbbbddDD..",
    "....dbbbbdddDDd.",
    "....dbbbdddDDDd.",
    "...dbbbbddddDDDd",
]
URSO_B = [
    "................",
    "................",
    "........bdb.....",
    ".......bBndd....",
    "......bBbbbbbd..",
    ".....bBkbbbbbbd.",
    "..ZBBBbbbbbbbbdd",
    ".kZbbbbbbbbbbbdd",
    "..ddbbbbbbbbbddD",
    "...dbbbbbbbbbddD",
    "....dbbbbbbbbddD",
    ".....dbbbbbbbddD",
    "......dbbbbbbddD",
    ".....dbbbbbbbddD",
    "....dbbbbbbbbddD",
    "...dbbbbbbbbbddD",
]
FALCAO_A = [
    "................",
    ".......hhhhh....",
    ".....hhSSSSsh...",
    "....hSSSSSSssh..",
    "...hhSSSSSSsssh.",
    "..gyhyEyhsssssh.",
    ".ggghhyhhcssssh.",
    ".gEg.hhccccsssh.",
    "..E..hhcccccssh.",
    ".....hhcccccsssh",
    "......hcccccssh.",
    "......ccccccsssh",
    ".....cCcccCcsssh",
    ".....cccCcccsssh",
    "....cCcccCccsssh",
    "....ccccCcccsssh",
]
FALCAO_B = [
    "................",
    "....hhhh........",
    "...hSSSsh.......",
    "..hSSSSssh......",
    ".ghyEyhssh......",
    "gyhhhhhcssh.....",
    "gE.hhcccssh.....",
    ".E.hhcccsssh....",
    "....ccccsssSh...",
    "....cCccssSSSh..",
    "...ccccCsSSSSsh.",
    "...cCcccsSSSssh.",
    "...cccCcsSSsssh.",
    "..cCccccsSSssshh",
    "..ccCcccssSsshhh",
    "..cccCccssssshhh",
]

# A transposição das duas referências geradas na conversa (21/10/2026), em ferramentas/arte/referencias/icones/: o
# "Retrato pixelado de urso pardo severo-1.png" e o "Falcão-peregrino com máscara ocular em pixel art-2.png". A
# construção, as proporções e a expressão delas na grade de 16, à mão, com a referência reduzida como guia oculta
# (guias/). O urso: de frente, as orelhas redondas, as órbitas fundas com a sombra da testa e o ponto âmbar do olho, o
# focinho claro e forte com o nariz, a faixa clara e a boca fechada, o queixo, e o pescoço que recua para o corpo fora do
# quadro (sem ombros). O falcão: de perfil para a esquerda, o bico curto com o gancho, a cera amarela, o anel amarelo à
# esquerda e embaixo do olho, a máscara escura que envolve o olho e segue para a nuca (sem descer pela bochecha), o
# queixo e a garganta claros, a asa e a nuca em cinza-azulado, poucas pintas no peito.
URSO_T = [
    "................",
    "..bb........bb..",
    ".bNNb......bNNd.",
    ".bNbbdbBBbdbbNd.",
    ".dbBOBBBBBBbbbd.",
    "bbBOBBbBBbBBbbdd",
    "bBBDDDbBBbDDDbdd",
    "bBbbDaDbbDaDbbdd",
    "dbBbbQQQQQqbbbdd",
    "dbbbQQKKKKQqbbdd",
    "dbbbQQqKKqQqbbd.",
    ".dbbQQQQQQQqbdd.",
    ".ddbbQddddqbbdd.",
    "..ddbbQQQqbbdd..",
    "...ddbbbbbbddD..",
    "....ddbbbbbdDD..",
]
FALCAO_T = [
    "................",
    "......vVVVv.....",
    ".....vLLLVVv....",
    "....vLLVVVVvv...",
    "...vVmmmmmmvvv..",
    "..IJmJemmmmmvvv.",
    ".GRJmmJmmmvvvvX.",
    ".GGRWWWWvvvvvvX.",
    "..X.WWWWWWvvvvX.",
    "....WWWWWWWvvvXX",
    "....WWWWWWLvvvXX",
    "...WWWWWWvLLvvXX",
    "...WwWWWWWvLLvXX",
    "..WWWWwWWWvLvvXX",
    "..WwWWWWwWvvvvXX",
    "..WWWWwWWWvvvXXX",
]

URSO = lambda x, y, ch: "focinho" if ch in "Zz" else "detalhes" if ch in "kn" else "pelagem"
FALCAO = lambda x, y, ch: "peito" if ch in "cC" else "bico" if ch == "g" or (ch in "Ey" and x <= 3) else "olho" if ch in "Ey"     else "plumagem"
CAMADAS = {
    "urso-a": (URSO_A, ["pelagem", "focinho", "detalhes"], URSO),
    "urso-b": (URSO_B, ["pelagem", "focinho", "detalhes"], URSO),
    "falcao-a": (FALCAO_A, ["plumagem", "peito", "bico", "olho"], FALCAO),
    "falcao-b": (FALCAO_B, ["plumagem", "peito", "bico", "olho"], FALCAO),
    "urso-t": (URSO_T, ["pelagem", "focinho", "detalhes"],
               lambda x, y, ch: "focinho" if ch in "Qq" else "detalhes" if ch in "KNa" else "pelagem"),
    "falcao-t": (FALCAO_T, ["plumagem", "mascara", "peito", "bico", "olho"],
                 lambda x, y, ch: "peito" if ch in "Ww" else "mascara" if ch == "m" else "bico" if ch in "GRI" or (ch in "XJ" and x <= 3)
                 else "olho" if ch in "Je" else "plumagem"),
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
