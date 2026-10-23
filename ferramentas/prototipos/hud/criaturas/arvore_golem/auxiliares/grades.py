"""A Árvore Desperta e o golem de pedra (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do
Bestiário são o 16 ×2 e ×3. Desenhados à mão, uma letra por pixel; silhueta, volumes e expressão primeiro.
  A Árvore Desperta (`ent_jovem`: "Árvores que acordaram com raiva. Madeira verde queima mal — mas queima."; planta e
  blindada; o Golpe Esmagador e o Regenerar): a casca, os nós e os galhos formando o rosto.
      A1, os galhos nus: de frente, o tronco é a cabeça, os galhos secos subindo em forquilhas com poucas folhas na
          ponta, as sobrancelhas de casca sobre os olhos de nó inclinados (bravos), a fenda da boca com as lascas e as
          raízes se abrindo embaixo;
      A2, a copa pesada: a copa verde redonda caindo sobre os olhos como uma testa, o toco de galho quebrado como
          nariz, a boca de nó com as lascas, o tronco largo.
  O golem de pedra (`golem`: "Pedra e runas. Lento, mas cada golpe é uma avalanche. A magia racha a pedra."; construto
  e blindado; o Golpe Esmagador): peso e construção mineral, blocos e juntas legíveis.
      G1, a cantaria: blocos cortados, a cabeça um bloco só com a laje da testa e as órbitas quadradas, a junta escura
          do pescoço, as ombreiras e o peito em blocos brutos, a rachadura descendo pelo peito;
      G2, o rochedo: pedras brutas e arredondadas, a cabeça pequena e baixa entre dois ombros enormes, a testa saliente
          sobre as órbitas, o musgo num ombro, o punho de pedra embaixo à esquerda.
  A segunda rodada (o Jean recusou a A1 e a A2; o G2 bem encaminhado): as duas Árvores pelas referências geradas na
  conversa com o Jean (ferramentas/arte/referencias/icones/), medidas na guia oculta (guias/: o recorte de 1200 px a
  partir de (27, 27), reduzido por média, 75 px por pixel) e redesenhadas à mão; e o G2 refinado.
      T1, pela "Retrato pixelado da árvore ancestral.png": o tronco alongado, as sobrancelhas pesadas de casca, o olhar
          fundo, o nariz, a boca fechada com os cantos caídos, os galhos secos subindo e o lado esquerdo na sombra;
      T2, pela "Árvore anciã severa em pixel art.png" (a direção preferida): a velha austera em três quartos, a testa
          pesada, os olhos fundos, o nariz retorcido para a esquerda, a boca torta, o musgo caindo pela esquerda, o oco
          da casca na lateral direita e os galhos;
      G2r, o G2 com a cabeça separada dos ombros por um vão escuro dos lados e sob o queixo, o queixo aceso; o peso, a
          pose e os grandes volumes do G2.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "arvore": {
        "o": "1a120c", "s": "3a2a1c", "m": "5e4630", "l": "86684a", "h": "a88a62",  # a casca (contorno à luz)
        "k": "0e0a08",  # os ocos: os olhos de nó, a boca
        "G": "2e4a22", "g": "4e7032", "y": "76984a",  # as folhas
    },
    "arvore_t1": {  # a casca cinza-marrom da referência 1
        "o": "1e140e", "s": "3c2c24", "m": "5c4a3e", "l": "806a5a", "h": "a48c78", "k": "120c08", "e": "a07838",
    },
    "arvore_t2": {  # a casca marrom e o musgo da referência 2
        "o": "1c120e", "s": "3a2a22", "m": "5c4436", "l": "7c5c48", "h": "9a7458", "k": "140c0a", "e": "a07838",
        "G": "2e3220", "g": "4a5430", "y": "66703e",
    },
    "golem": {
        "o": "1a1816", "s": "3c3832", "m": "5e5950", "l": "847e72", "h": "a8a294",  # a pedra (contorno à luz)
        "k": "0e0c0a",  # as juntas, as órbitas, a rachadura
        "g": "6a7a44",  # o musgo
    },
}

ARVORE_A1 = [
    ".g......g....g..",
    ".go....og...ogy.",
    "..mo..oms..omg..",
    "..oms.oms.omso..",
    "...ommmlmmmmo...",
    "..olllhllmmmso..",
    "..olhhlmlhhmso..",
    "..olkklmlkkmso..",
    "..ollklmlkmsso..",
    "..ollmlhmmmsso..",
    "..olkkkkkkksso..",
    "..olklkkklksso..",
    "..ollkkkkkmsso..",
    ".oolllmlmmmssoo.",
    "ollllmlmmmmsssso",
    "olmlomlmsomssoso",
]
ARVORE_A2 = [
    ".....GggyG......",
    "...GggyygggG....",
    "..GgggyggggyG...",
    ".GgggggggggggGG.",
    ".GgGgggGggggGgG.",
    "..GGoGGGGGoGGG..",
    "...osssssssso...",
    "...oskkmmkkso...",
    ".ohhmlkmlkmso...",
    "..oolmlhmmmso...",
    "...olkkkkkmso...",
    "...olklkklmso...",
    "..ollmkkkmmsso..",
    ".olllmlmmmmssso.",
    "olllmmlmmmmmssso",
    "olmmmmmmmmmmssso",
]
GOLEM_G1 = [
    "................",
    "....oooooooo....",
    "....ohhhlllmo...",
    "....ollllllmo...",
    "....ossssssso...",
    "....okkllmkko...",
    "....olllkmmmo...",
    "....olmkkkmso...",
    ".oooookkkkkoooo.",
    "ohhhlohhllmohllo",
    "ollllolkmmmollmo",
    "olllmollkmmolmso",
    "ollmmollkmmommso",
    "ommmsollmksomsso",
    "osmsoolmmmsoosso",
    "oo.ooolmmmsoo.oo",
]
GOLEM_G2 = [
    "................",
    "......oooo......",
    ".....ohhllo.....",
    "....ohhhhlmo....",
    "..oooskmksoooo..",
    ".ohhlolmmmolhgo.",
    "ohllloommmoollgo",
    "ohllllooooollmmo",
    "olllllmmmmmlmmso",
    "ollllmmlmmmmmmso",
    "oolllmmmmmmmmsso",
    "ohhhomllmmmmssso",
    "ohlllommmmmssso.",
    "ollllommmmmsso..",
    "ollmmoommmsso...",
    ".oooo.oommoo....",
]

ARVORE_T1 = [
    "...o............",
    ".o.mo....o.o..o.",
    ".ms.ml..omom.om.",
    "..smlmo.mlmlmmo.",
    "...smllmlhllmms.",
    "...smmlhllllmmo.",
    "...smlhhhhmhhho.",
    "...smlskeshkeso.",
    "...smllsmlhsmso.",
    "...smlmmllhhsmo.",
    "...smmlmlhhhmmo.",
    "..osmmlmkkkksmo.",
    "..osmlmkhllmkso.",
    ".osmllmmlhmmlsso",
    "osmlmmlmlhmmlmso",
    "osmlsmlmmlmsmlmo",
]
ARVORE_T2 = [
    "gG.os...........",
    ".gGsml......om..",
    "..gGsml....omlom",
    "...gGgmllmmmlmo.",
    "...Ggsmlllmmmmo.",
    "..gGsmhhhllmmmso",
    "..gGshhhhlmsmmso",
    "..gskkksklmmkmso",
    "..gsekmhesmmkkso",
    "..gsmlhhlsmmmkso",
    "..gsmhhhsmmmmmso",
    "...smsslhmlmmmso",
    "...smkkkkmlmmmso",
    "..osklhhlkmmmmso",
    ".osmllmmlmmlmmso",
    "osmlmmlmmlmmlmmo",
]
GOLEM_G2R = [
    "................",
    "......oooo......",
    ".....ohhllo.....",
    "....ohhhhllo....",
    "..ookskmksskoo..",
    ".ohhklmmmlmkhgo.",
    "ohllkolmmsokllgo",
    "ohlllkkkkkkllmmo",
    "olllllmmmmmlmmso",
    "ollllmmlmmmmmmso",
    "oolllmmmmmmmmsso",
    "ohhhomllmmmmssso",
    "ohlllommmmmssso.",
    "ollllommmmmsso..",
    "ollmmoommmsso...",
    ".oooo.oommoo....",
]


def _camada_arvore(x, y, ch):
    if ch in "Ggy":
        return "folhas"
    return "rosto" if ch in "ke" else "casca"


def _camada_golem(x, y, ch):
    if ch == "g":
        return "musgo"
    return "juntas" if ch == "k" else "pedra"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "arvore-a1": (ARVORE_A1, "arvore", ["casca", "folhas", "rosto"], _camada_arvore),
    "arvore-a2": (ARVORE_A2, "arvore", ["casca", "folhas", "rosto"], _camada_arvore),
    "golem-g1": (GOLEM_G1, "golem", ["pedra", "juntas"], _camada_golem),
    "golem-g2": (GOLEM_G2, "golem", ["pedra", "musgo", "juntas"], _camada_golem),
    "arvore-t1": (ARVORE_T1, "arvore_t1", ["guia", "casca", "rosto"], _camada_arvore),
    "arvore-t2": (ARVORE_T2, "arvore_t2", ["guia", "casca", "folhas", "rosto"], _camada_arvore),
    "golem-g2r": (GOLEM_G2R, "golem", ["pedra", "musgo", "juntas"], _camada_golem),
}
GUIAS = {"arvore-t1": "guias/arvore-r1-guia-16.png", "arvore-t2": "guias/arvore-r2-guia-16.png"}  # ocultas na fonte


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
        if ident in GUIAS:
            g = Image.open(base / GUIAS[ident]).convert("RGBA")
            listas["guia"] = [f"{x},{y},{''.join(f'{v:02x}' for v in g.getpixel((x, y)))}" for y in range(16)
                              for x in range(16) if g.getpixel((x, y))[3]]
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
