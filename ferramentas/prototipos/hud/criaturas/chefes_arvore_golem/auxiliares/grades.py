"""A Árvore Anciã e o Golem Primordial, os guardiões (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta da
luta é o 16 ×2 (os guardiões só aparecem na carta: não entram no Bestiário nem nos contratos). Desenhados à mão, uma
letra por pixel; a presença de chefe pela composição e pelos volumes, não por detalhe miúdo.
  A Árvore Anciã (`ent_anciao`: "Uma árvore milenar abre olhos de seiva âmbar e fala com voz de terremoto."; planta e
  blindada; o Golpe Esmagador, o Regenerar, o Agarrão e a Varredura): a linguagem e o material da Árvore Desperta T1.
      AA1, o rosto-rei: de frente e de perto, o tronco na largura toda, a copa de galhos grossos subindo como uma coroa,
          as sobrancelhas pesadas na largura do rosto, os olhos de seiva âmbar fundos e afastados, o nariz, a boca
          longa fechada e a barba de raízes caindo em mechas;
      AA2, a árvore imensa: a árvore inteira, a copa larga de galhos secos ocupando o alto, o tronco estreitando e
          abrindo de novo, o rosto mais baixo no tronco (a escala vem do rosto pequeno diante da árvore), as raízes.
  O Golem Primordial (`golem_primordial`: "O que você pensava ser uma parede se levanta: um golem do tamanho de uma
  casa."; construto e blindado; o Golpe Esmagador, a Investida e a Varredura): o peso e a pedra bruta do G2.
      GP1, a parede que se levanta: a cabeça grande de pedra no meio de uma parede de pedras, a laje por cima, três
          pedras de cada lado e o bloco do peito embaixo, com o vão escuro em volta da cabeça;
      GP2, o ídolo: a cabeça grande esculpida num bloco, a laje mais larga que ela por cima (como um dólmen), a testa,
          as órbitas fundas, o nariz e o talho da boca, sobre o corpo de rochedos do G2.
  A segunda rodada (o Jean deu duas referências novas, em close: o rosto ocupa quase todo o ícone; a AA1/2 e a GP1/2
  ficam como histórico): três tentativas de copiar cada referência (pedido do Jean), medidas na guia oculta (guias/: o
  recorte de 1200 px a partir de (27, 27), reduzido por média, 75 px por pixel), cada uma por um caminho:
      R1, pela guia limpa: a cor de cada pixel parte da guia reduzida à paleta, e a limpeza à mão põe os olhos, o nariz, a
          boca e as bordas no lugar (a mais perto da textura e da luz da referência);
      R2, por volumes: os grandes planos simplificados à mão (a testa, as sobrancelhas, o nariz, a boca, as bochechas);
      R3, pelas linhas: os sulcos e as juntas escuras da referência desenhados (em volta das sobrancelhas e do nariz na
          árvore; entre as placas no golem).
  A Árvore Anciã ("Rosto da árvore ancestral-1.png"): em close, em três quartos para a direita, as sobrancelhas grossas
  de casca, o olho de seiva âmbar grande na cavidade à esquerda e o menor à direita, o nariz nodoso, a boca fechada com
  os cantos caídos, um pouco de musgo à esquerda, os galhos saindo pelo alto; a casca e a paleta da T1.
  O Golem Primordial ("Rosto do Golem de Pedra Primordial-2.png"): em close, em três quartos para a esquerda, a cabeça
  irregular de pedras, a testa pesada, as cavidades dos olhos com um ponto de luz, a rachadura principal no alto, o nariz
  de pedra, o vinco da boca e a mandíbula de pedras brutas, o musgo à direita; a pedra e a paleta do G2.
  Três variações da R2 (pedido do Jean), uma mudança por vez, a mesma guia:
      Árvore: R2a, a luz lateral (a metade esquerda acesa, a direita na sombra: mais volume); R2b, o olhar mais pesado
          (as sobrancelhas mais baixas e escuras, os olhos mais fundos, o franzido da boca mais fundo); R2c, a silhueta
          dos galhos (mais grossos e escuros contra o fundo, as bordas da casca marcadas);
      Golem: R2a, o close mais fechado (a cabeça até as bordas, cortada como na referência); R2b, os três quartos para
          a esquerda (a testa saliente na borda, o rosto deslocado, a bochecha direita maior); R2c, as pedras mais brutas
          (a silhueta em degraus, a mandíbula pesada embaixo).
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua (a guia, do png dela)
"""
import pathlib
import sys

from PIL import Image

PALETAS = {
    "anciaa": {  # a casca da T1, mais funda; a seiva âmbar dos olhos (do texto do jogo)
        "o": "1a120c", "s": "36281e", "m": "54443a", "l": "7a6656", "h": "9e8a74", "k": "100a06", "e": "b88830",
    },
    "anciaa_r": {  # a casca da T1, o âmbar da seiva e o musgo da referência
        "o": "1e140e", "s": "3c2c24", "m": "5c4a3e", "l": "806a5a", "h": "a48c78", "k": "120c08", "e": "c09030",
        "G": "3e4a2e", "g": "5c6a40",
    },
    "primordial_r": {  # a pedra do G2
        "o": "1a1816", "s": "3c3832", "m": "5e5950", "l": "847e72", "h": "a8a294", "k": "0e0c0a", "g": "6a7a44",
    },
    "primordial": {  # a pedra do G2, mais escura e mais velha
        "o": "161412", "s": "34302a", "m": "545048", "l": "787268", "h": "9c968a", "k": "0c0a08", "g": "5a6a3a",
    },
}

ANCIAA_AA1 = [
    ".o...o....o...o.",
    ".mo..ms..sm..om.",
    "..ms.mls.lm.sm..",
    "..smmllhhllmms..",
    ".osmllhhhhllmso.",
    "osmhhhhllhhhhmso",
    "ossskeksskeksso.",
    "osmlsmllllmsmlso",
    "osmllmlhhlmllmso",
    "osmllmlhhlmllmso",
    "osmllssmmsslmmso",
    "osmlkkkkkkkklmso",
    "osmllmllllmllmso",
    "osmlsmlsmlsmlsso",
    "osml.mls.ls.ml.o",
    "osm..ml..ls..mso",
]
ANCIAA_AA2 = [
    ".o..o...o...o...",
    "om.om..om..mo.o.",
    ".ms.ms.ms.sm.sm.",
    "..msmlsmlsmlsm..",
    "...smllmllmlms..",
    "....smllmllms...",
    ".....slhhlms....",
    "....oslhhlmso...",
    "...osmhhhhmmso..",
    "...oskekkeksso..",
    "...osmllhlmmso..",
    "..osmlkkkkmmmso.",
    "..osmllmllmmmso.",
    ".osmllmlllmmmsso",
    "osmllmlmllmmmsso",
    "osml.smlsmls.mso",
]
PRIMORDIAL_GP1 = [
    "ohhlohhhhlmmohlm",
    "olmlollllmmsolms",
    "olmkkkkkkkkkklms",
    "olmkohhhhlloklms",
    "olmkolllllmoklmm",
    "kkkkohhhlhhokkkk",
    "ohlkoskklkkokhlm",
    "olmkolllhmmoklms",
    "olmkolkkkkmoklms",
    "olmkolllmmmoklms",
    "osmkoolmmmookmms",
    "kkkkkooooookkkkk",
    "ohlllmllmmmlhllm",
    "ollmllmmmmmmlmms",
    "olmmmmmmmmmsmmss",
    "osmsmmmsssssssso",
]
PRIMORDIAL_GP2 = [
    "..oooooooooooo..",
    "..ohhhhhhhllmo..",
    "..osssssssssso..",
    "...olllllmmmo...",
    "...ohhhlhhhmo...",
    "...oskklskkso...",
    "...ollllhmmmo...",
    "...olkkkkkkmo...",
    "..oolllmmmmmoo..",
    ".ohhooossssoohgo",
    "ohllllooooollmmo",
    "olllllmmmmmlmmso",
    "ollllmmlmmmmmmso",
    "oolllmmmmmmmmsso",
    "ohhhomllmmmmssso",
    "ohlllommmmmssso.",
]

ANCIAA_R1 = [
    "mmlmm...m.l..sms",
    "ssmmmsmsmmhl.mlm",
    ".smmsmlmlhhlslms",
    ".sssGmllllhlmsms",
    ".sssGhhlhllmlms.",
    "smsGsmlhhhllhls.",
    ".ssmshhhhhshhlm.",
    ".ssGskkekksmhlm.",
    ".sGslmsslhlsskks",
    ".ssmsmlslhhlkeks",
    "sssmmsmslhhlhms.",
    "ssmmmmlshhhhsms.",
    "sGsllmllssmssss.",
    "smsmlmmkkkkkmsm.",
    "smmlmmmkmmmmkssm",
    "mmlmmlslllmmssms",
]
ANCIAA_R2 = [
    "om.....mo.om..mo",
    "mlm...omlolms.ml",
    "smlo.omllllmmoml",
    "ssmmolhhhllmlmmo",
    "smmmlhhhhllllmms",
    "sgGmlhhllhhllmms",
    "smGshhhhhhsllmms",
    "smgmskkekksshhms",
    "smGmlmsslhlsskms",
    "smmmllmslhhskeks",
    "smmmlmlslhhslsms",
    "smmmlmlshhhhsmms",
    "smmlmllssmmssmms",
    "smmlmlmkkkkkmmms",
    "smmlmlkmmmmmkmms",
    "smmlmlmlmmmmmmms",
]
ANCIAA_R3 = [
    "om.....mo.om..mo",
    "mlm...omlolms.ml",
    "smlo.omllllmmoml",
    "ssmmokhhhllmlmmo",
    "smmmlhkkhllllmms",
    "sgGmlhhllhhllmms",
    "smGkhhhhhhkllmms",
    "smgmkkkekkkkhhms",
    "skGmlmkslhlkkkms",
    "smmklmmklhhkkeks",
    "smmklmmklhhhkkms",
    "smmklmlkhhhhkmms",
    "smmklmlskkkksmms",
    "smmklmmkkkkkmmms",
    "smmklmkmmmmmkmms",
    "smmklmlmmmmmmmms",
]
PRIMORDIAL_R1 = [
    "......lhhmm.....",
    "....lhlllmklm...",
    "...hhhhllmkmms..",
    "..lhhhllllkmgs..",
    "..lllhlllmmmgss.",
    ".lhllmmllmmmgsss",
    ".hhllllllmssgss.",
    "mlmskkkmkksskss.",
    ".sskhksssshkssss",
    "..hmmhllmmmmssss",
    ".mhlmhlmmmmsmsss",
    ".smlkkkkkkkslsks",
    ".mslllmlmmssmsss",
    ".hmmmmmmmssmmssm",
    "mlmmlllmmmsssssm",
    "mmmmhmmmmmsskmmm",
]
PRIMORDIAL_R2 = [
    ".....ohhhlo.....",
    "...oohhhhllmo...",
    "..ohhhhllllkmo..",
    "..ohllllllmkgmo.",
    ".ohlllmmmmmkgmso",
    "ohhhlokhhhllkgso",
    "ohlllkhllllmkmso",
    ".oskkkkmlkkkkmso",
    ".oskhkkmlkhkkmso",
    ".olllsmhlsllmsso",
    ".ollmsmhlsmlmsso",
    "..olkkkkkkkkmsso",
    "..ohllllllllsmso",
    ".ohllmmmmmmlssso",
    "ohllmmkmmmmmssso",
    "ollmmmkmmmmmmsso",
]
PRIMORDIAL_R3 = [
    ".....ohhhlo.....",
    "...oohhhhlkmo...",
    "..ohhhhlllkmmo..",
    "..ohllllllkgmo..",
    ".ohlkkkkkkkkgmso",
    "ohhhlkhhhhlkmgso",
    "ohllkllllmmkkmso",
    ".okkkkkmlkkkkmso",
    ".okhkkkmlkhkkmso",
    ".ollkkmhlkkllkso",
    ".ollkmmhlmkllkso",
    "..okkkkkkkkkkkso",
    "..ohllllkllllsso",
    ".ohllmmmkmmmlsso",
    "ohlkkmmmkmmmssso",
    "ollmkmmmkmmmmsso",
]

ANCIAA_R2A = [
    "om.....mo.om..mo",
    "mlm...omlolms.ms",
    "smlo.omllllmmoms",
    "shmmolhhhllmmmso",
    "shlmlhhhhlllmmss",
    "sgGlhhhllhllmmss",
    "shGshhhhhhsmmmss",
    "slgmskkekksssmss",
    "slGllmsslhlsskss",
    "shlllhmslhhskeks",
    "shllllmslhhsmsss",
    "slllllmshhhhssss",
    "shllllmssmmsssss",
    "slllmlmkkkkkmsss",
    "shlllmkmmmmmksss",
    "slllmlmlmmmmmmss",
]
PRIMORDIAL_R2A = [
    "...ohhhhhllmo...",
    "..ohhhhhlllkmo..",
    ".ohhhhllllmkmmo.",
    ".ohlllllllmkgmso",
    "ohhlllmmmmmkgmso",
    "ohhhhlokhhhlkgso",
    "ohllllkhlllmkmso",
    "osskkkkmlkkkkmso",
    "osskhkkmlkhkkmso",
    "olllllsmhlslllmo",
    "ollllmsmhlsmlmso",
    "oollkkkkkkkkmsso",
    ".oohllllllllsmso",
    ".ohllmmmmmmlssso",
    "ohllmmkmmmmmssso",
    "ollmmmkmmmmmmsso",
]
ANCIAA_R2B = [
    "om.....mo.om..mo",
    "mlm...omlolms.ml",
    "smlo.omllllmmoml",
    "ssmmolhhhllmlmmo",
    "smmmlhhhhhllllms",
    "sgGlhhhhhhhhhhms",
    "smGkkhhhhhkkhhms",
    "smgmkkkekkkkkkms",
    "smGmlskkkkslkeks",
    "smmmllmslhhsskks",
    "smmmlmlslhhslsms",
    "smmmlmlshhhhsmms",
    "smmlmllssmmssmms",
    "smmlmlkkkkkkkmms",
    "smmlmkmmmmmmmkms",
    "smmlmlmlmmmmmmms",
]
PRIMORDIAL_R2B = [
    "....ohhhhlo.....",
    "..oohhhhhllmo...",
    ".ohhhhhllllkmo..",
    ".ohllllllllkgmo.",
    "ohhlllmmmmmkgmso",
    "hhhhokhhhlllkgso",
    "ohllkhlllllmkmso",
    ".kkkkmlkkkkmmmso",
    ".khkkmlkhkkmmmso",
    ".ollsmhlslllmmso",
    ".olmsmhlsmllmsso",
    "..okkkkkkkmmmsso",
    "..ohllllllmmsmso",
    ".ohllmmmmmmlssso",
    "ohllmmkmmmmmssso",
    "ollmmmkmmmmmmsso",
]
ANCIAA_R2C = [
    "ko.....ko.ko..ko",
    "kmk...okmokmo.km",
    "smko.okllllmmokm",
    "ssmmolhhhllmlmmo",
    "smmmlhhhhllllmms",
    "sgGmlhhllhhllmms",
    "smGshhhhhhsllmms",
    "smgmskkekksshhms",
    "smGmlmsslhlsskms",
    "smmmllmslhhskeks",
    "smmmlmlslhhslsms",
    "smmmlmlshhhhsmms",
    "smmlmllssmmssmms",
    "smmlmlmkkkkkmmms",
    "smmlmlkmmmmmkmms",
    "ssmssmsmmsmmmsss",
]
PRIMORDIAL_R2C = [
    ".....ohhhlo.....",
    "...oohhhhllmo...",
    "..ohhhhlllllko..",
    ".oohlllllllkgmo.",
    ".ohlllmmmmmkgmso",
    "ohhhlokhhhllkgso",
    "ohlllkhllllmkmso",
    ".oskkkkmlkkkkmso",
    ".oskhkkmlkhkkmso",
    ".ollllsmhlsllmso",
    ".olllmsmhlsmlmso",
    "..olkkkkkkkksmso",
    ".ohhhllllllllsso",
    "ohlllmmmmmmmlsso",
    "ohllmmmkmmmmmsso",
    "olllmmmkmmmmmmso",
]


def _camada_anciaa(x, y, ch):
    if ch in "Gg":
        return "musgo"
    return "rosto" if ch in "ke" else "casca"


def _camada_primordial(x, y, ch):
    if ch == "g":
        return "musgo"
    return "juntas" if ch == "k" else "pedra"


CAMADAS = {  # a grade, a paleta, as camadas de baixo para cima e a camada de cada pixel
    "anciaa-aa1": (ANCIAA_AA1, "anciaa", ["casca", "rosto"], _camada_anciaa),
    "anciaa-aa2": (ANCIAA_AA2, "anciaa", ["casca", "rosto"], _camada_anciaa),
    "primordial-gp1": (PRIMORDIAL_GP1, "primordial", ["pedra", "juntas"], _camada_primordial),
    "primordial-gp2": (PRIMORDIAL_GP2, "primordial", ["pedra", "musgo", "juntas"], _camada_primordial),
}
for _n in (1, 2, 3):
    CAMADAS[f"anciaa-r{_n}"] = (globals()[f"ANCIAA_R{_n}"], "anciaa_r", ["guia", "casca", "musgo", "rosto"], _camada_anciaa)
    CAMADAS[f"primordial-r{_n}"] = (globals()[f"PRIMORDIAL_R{_n}"], "primordial_r", ["guia", "pedra", "musgo", "juntas"],
                                     _camada_primordial)
for _v in "abc":
    CAMADAS[f"anciaa-r2{_v}"] = (globals()[f"ANCIAA_R2{_v.upper()}"], "anciaa_r", ["guia", "casca", "musgo", "rosto"],
                                  _camada_anciaa)
    CAMADAS[f"primordial-r2{_v}"] = (globals()[f"PRIMORDIAL_R2{_v.upper()}"], "primordial_r",
                                      ["guia", "pedra", "musgo", "juntas"], _camada_primordial)
_RS = ("1", "2", "3", "2a", "2b", "2c")
GUIAS = {**{f"anciaa-r{n}": "guias/anciaa-r-guia-16.png" for n in _RS},
         **{f"primordial-r{n}": "guias/primordial-r-guia-16.png" for n in _RS}}  # ocultas na fonte


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
