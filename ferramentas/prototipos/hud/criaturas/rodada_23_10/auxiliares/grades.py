"""A rodada depois do Caído CA (pedido do Jean; propostas, nada no jogo), 16×16; o 32 da carta e o 48 do Bestiário são o
16 ×2 e ×3. As propostas anteriores (o `harpia_grifo/` e o `caidos/`) ficam como histórico.
  - GA2, o Grifo A com a ponta do bico limpa: a mancha marrom junto da ponta era a ponta escura (`d`) espalhada em cinco
    pixels (um na linha 7, dois na 8, três sob a mandíbula de baixo na 9 e um solto na 10); fica uma ponta escura só, no
    gancho, e o resto do GA igual (a cabeça, o olhar, os tufos, as cores, o enquadramento).
  - Três Harpias do zero ("Metade mulher, metade abutre, inteira cruel."), com o rosto, o pescoço e as penas de um ser só:
      H1, a abutre de rosto humano: de frente e encolhida como um abutre, a cabeça calva de mulher com fios ralos, o
          olhar frio e a boca pequena, o pescoço nu e rosado saindo da gola de penas, as asas fechadas subindo como
          ombros (o pescoço na pele escura, com a ruga em sombra: o rosado lia como língua);
      H2, a da asa erguida: em três quartos para a direita, a asa sobe do ombro por trás dela até o alto, à esquerda,
          e o cabelo escuro se emenda nas penas dela; o pescoço nu, a gola;
      H3, a de bico: de frente, o rosto de mulher (a testa, os olhos, as maçãs e o queixo) com o nariz e a boca
          fundidos num bico curto em gancho, o cabelo longo terminando em penas, a gola e as asas embaixo.
  - Três Xamãs Caídos, da cabeça do Caído CA aprovado (as mesmas proporções, a pele, os chifres, as orelhas, os olhos):
      X1, o velho do capuz: o capuz de couro atrás da cabeça com os chifres furando, a pintura branca descendo dos
          olhos, o sorriso fechado de presas, o colar de contas de osso;
      X2, o do cajado: o cajado de osso com a chama no alto, na mão dele, a boca aberta conjurando, a capa;
      X3, o das penas: o cocar de três penas, o rosto concentrado, uma chama pequena entre as mãos, abaixo do queixo.
    python grades.py <pasta> [<id> ...]     # grava grades/<id>.txt e listas/<id>/<camada>.lua
"""
import importlib.util
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent


def _modulo(pasta):
    spec = importlib.util.spec_from_file_location(pasta, AQUI.parents[1] / pasta / "auxiliares/grades.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_GRIFO = _modulo("harpia_grifo")
_CAIDOS = _modulo("caidos")

PALETAS = {
    "grifo": _GRIFO.PALETAS["grifo"],
    "harpia": {
        "p": "cdb8a2", "P": "967f6c", "x": "644f45",  # a pele de mulher (luz, sombra, sombra funda)
        "h": "2a2020", "H": "4a3a34",  # o cabelo
        "k": "140e0c", "e": "e0a030", "m": "5a2a28",  # o escuro, o olho de ave, a boca
        "y": "dcc48c", "Y": "a08a56", "d": "4a3a24",  # o bico
        "c": "d6c8ae", "C": "a8987e",  # a gola de penas claras
        "B": "2e2420", "b": "4e3c32", "F": "6e5440", "D": "1e1816",  # as penas escuras das asas
    },
    "xama": {**_CAIDOS.PALETAS["a"], "q": "2a1a1a", "Q": "7a2a26"},  # o vermelho do CA; as penas do cocar
    "harpia_t": {  # as cores medidas na referência "Harpia vulturina em pixel art.png"
        "p": "e0c4ac", "P": "b48f78", "x": "86604f", "X": "573a30",  # a pele pálida (luz, meio, sombra, sombra funda)
        "m": "8a5450", "e": "e09a2a", "E": "9a6420", "k": "1c1210",  # a boca; o olho âmbar (o de trás mais escuro)
        "h": "2a1e1a", "H": "4a372d", "j": "735443",  # as penas escuras (o corpo, a luz de cada tufo, a raiz clara)
        "c": "e2d1b5", "C": "b39d82", "Q": "7d6853",  # a gola clara de abutre
    },
}

GA2 = list(_GRIFO.GA)
GA2[7] = ".OwwWWWWyyyyYYY."
GA2[8] = ".qOwwWWWwyyYYd.."
GA2[9] = "..qOwwwwwYY....."
GA2[10] = "..lqOwwwwOq....."

H1 = [
    "B.....hh......B.",
    "BB...ppPPh...BB.",
    "BbB.pppppPP.BbB.",
    "BbBpxxpppxxPBbB.",
    "BbBpkepppkePBbB.",
    "BbBpppPxpppPBbB.",
    "BbBBppkkpPPBBbB.",
    "BbbBBxpppxPBBbbB",
    "BbbbBBxxxxBBbbbB",
    "BbbbBBxPxxBBbbbB",
    "BbbbBcCxPCcBbbbB",
    "BbbBcccCCcccBbbB",
    "BbBcccCccCcccBbB",
    "BbBCcCcCcCcCcBbB",
    "bBBDCDCDCDCDCBBb",
    "BBDDDDDDDDDDDDBB",
]
H2 = [
    "Fb..............",
    "bFb..hhh........",
    "BbFbhHhhhh......",
    "BbbFhhhppppP....",
    ".BbbhhpppppPP...",
    ".BbFhhppkepPP...",
    ".BbbhhpppppPPP..",
    "..BbFhpppmpPP...",
    "..BbbhhPpPPx....",
    "..BbFhhxxxPx....",
    ".BbbFFhxPxcc....",
    "BbbFFFcxxccCc...",
    "BbFFcccCccCcCc..",
    "bbFcccCccCcCcCc.",
    "bFccCcCcCcCcCcC.",
    "FcCcCcCcCcCcCcCc",
]
H3 = [
    "...hhhhhhhhh....",
    "..hhHhhhhHhhh...",
    ".hhHpppppppHhh..",
    ".hHppppppppPHh..",
    "hhHkkppppkkPHhh.",
    "hHpkeppppkePPHh.",
    "hHppppyYpppPPHh.",
    "hHpppyyYYppPPHh.",
    "hHPpppyYYdpPPHh.",
    "hhPPpxYYxpPPhh..",
    "FhhPPpppppPPhhF.",
    "FFhhPPPPPPPhhFF.",
    "BFFhcPPPPPchFFB.",
    "BBFFcccCCcccFFBB",
    "BbBFFcCcCcCFFBbB",
    "BbbBFFCcCcFFBbbB",
]
X1 = [
    "...hCCCCCCCCh...",
    "..hHCccccccCHh..",
    "..CcRrrrrrrRcC..",
    ".CcarrrrrrrrRcC.",
    "aCaakkrrrrkkRRCR",
    "aCaryyrrrryyrRCR",
    ".CawrrrRrrrwRRC.",
    ".CarwrrrrrrwRRC.",
    ".CarrkmmmmkRRCC.",
    ".CCarrkttkrRRCC.",
    "..CCRrrrrrRRCC..",
    ".CcbCRRrrRRCbcC.",
    "CccbcbRRRRbcbccC",
    "CcccbcbRRbcbcccC",
    "CCcccccbbcccccCC",
    "CCCcccccccccCCCC",
]
X2 = [
    ".Ff.............",
    "FYfh........h...",
    ".W.hH......Hh...",
    ".W..hRrrrrRh....",
    ".W.arrrrrrrrR...",
    "aW.arrrrrrrrR.RR",
    ".WaakkrrrrkkRRR.",
    ".WaryyrrrryyrR..",
    ".WarrrrRrrrrRR..",
    ".WarrrkmmkrrRR..",
    ".W.rrkmmkrRRR...",
    ".W.rrrkkrrRR....",
    "aWa.RrrrrrRR....",
    "aWaCCRrrrRRCC...",
    ".WCccCRRRCccC...",
    "CWCcccCCCcccCCC.",
]
X3 = [
    "....Q..Q..Q.....",
    "...hqQ.Qq.Qh....",
    "...hHqQQqQqHh...",
    "....hRrrrrRh....",
    "...arrrrrrrrR...",
    "aa.arrrrrrrrR.RR",
    ".aaakkrrrrkkRRR.",
    "..aryyrrrryyrR..",
    "..arrrrRrrrrRR..",
    "..arrkmmmmkrRR..",
    "...rrtrrrrtRR...",
    "...rrrrrrrRR....",
    "..DRRRfYfRRD....",
    ".DRaafYYfaaRD...",
    "DRRaaFffFaaRRD..",
    "DRRRRRFFRRRRRRDD",
]

# A segunda rodada (pedido do Jean; propostas, nada no jogo). As anteriores ficam como histórico.
# T, a Harpia pela referência nova (ferramentas/arte/referencias/icones/"Harpia vulturina em pixel art.png", imagem
# gerada na conversa com o Jean): redesenhada à mão na grade de 16, medindo na guia oculta (guias/harpia-t-guia-16.png,
# o recorte quadrado de 1000 px a partir de (200, 120), reduzido por média: cada pixel vale 62,5 px da referência). Em
# três quartos para a esquerda, como nela: a testa pálida, a sobrancelha pesada descendo para o nariz (o olhar cruel), o
# olho âmbar da frente sob ela e o de trás mais escuro (em perspectiva; dois iguais liam como óculos), o nariz curvo
# saindo do perfil, a boca fechada numa linha (sem o escuro sob o nariz, que a alargava), o queixo e a sombra da
# mandíbula; as penas escuras nascendo das duas têmporas e varrendo para trás em cinco tufos, cada um com a luz em
# cima (o salpicado de tons lia como cabelo crespo); o pescoço na sombra entrando na gola clara de abutre; os ombros de
# penas escuras ligados ao cabelo pelo lado direito. Os fios e as rugas da referência não cabem: ficam agrupados.
HARPIA_T = [
    "....hHHh..Hh....",
    "..hjjhhhhHhhh...",
    ".hjPpPhHHhhhHH..",
    ".hpppPjhhhHHhhh.",
    ".PpppPjhHHhhhHh.",
    ".hPxXXxjhhhHHh..",
    ".hEpkePjhHHhhhh.",
    "..pPppPxHhhhHh..",
    ".pxPpPPxhhHHhh..",
    "...mmPPxxHhhhh..",
    "...ppPXxPxCCchh.",
    "...QxXXxPxCcccCh",
    "hhHCcCQxPPcCcHhh",
    "hjhcCcQxPcccHjHh",
    "HhhcCcccCccCchjh",
    "hhHCcCccCccCHhhH",
]
# GA3, o gancho do bico do GA2: a ponta escura sai de baixo da mandíbula (13,8), que termina amarela, e desce um pixel
# da própria extremidade (14,8), num marrom do pelo que aparece contra a caixa escura (o `d` sumia nela). O resto é o
# GA2 pixel a pixel.
GA3 = list(GA2)
GA3[8] = ".qOwwWWWwyyYYYq."
# X1r, o X1 refinado: a cabeça igual, pixel a pixel (subir o rosto uma linha para ganhar testa alongava a cara e a
# afastava do CA); o colar encolhe para um U pequeno de cinco contas logo abaixo do queixo, na sombra o de baixo, e a
# capa fecha a parte de baixo: o queixo e o pescoço respiram e o colar deixa de ocupar a base.
X1R = list(X1)
X1R[11:16] = [
    ".CccCRRrrRRCccC.",
    "CcccCbRrrRbCcccC",
    "CcccCHbRRbHCcccC",
    "CCcccCCHHCCcccCC",
    "CCCcccccccccCCCC",
]


def _camada_harpia_t(x, y, ch):
    if ch in "eEkm":
        return "rosto"
    if ch in "pPxX":
        return "pescoco" if y >= 11 or (y >= 9 and x >= 7) else "rosto"
    if ch in "hHj":
        return "cabelo" if y <= 10 else "penas"
    return "gola"


def _camada_harpia(x, y, ch):
    if ch in "ke" or (ch == "m" and y < 12):
        return "rosto"
    if ch in "yYd":
        return "bico"
    if ch in "pPx":
        return "pescoco" if 8 <= y <= 11 else "rosto"  # o pescoço nu na pele escura (H1, H2)
    if ch in "hH":
        return "cabelo"
    return "penas"


def _camada_xama(x, y, ch):
    if ch in "fFY":
        return "fogo"
    if ch in "cCbqQw":
        return "adornos"
    if ch == "W" and x <= 2:
        return "cajado"
    if ch in "hH":
        return "chifres"
    return "olhos" if ch in "yk" and y < 9 else "boca" if ch in "tmk" else "pele"


CAMADAS = {
    "grifo-ga2": (GA2, "grifo", ["pelo", "cabeca", "bico", "olho"], _GRIFO.CAMADAS["grifo-ga"][3]),
    "harpia-h1": (H1, "harpia", ["penas", "pescoco", "cabelo", "rosto"], _camada_harpia),
    "harpia-h2": (H2, "harpia", ["penas", "pescoco", "cabelo", "rosto"], _camada_harpia),
    "harpia-h3": (H3, "harpia", ["penas", "cabelo", "rosto", "bico"],  # o rosto dela desce até o queixo, sem pescoço à vista
                  lambda x, y, ch: "rosto" if _camada_harpia(x, y, ch) == "pescoco" else _camada_harpia(x, y, ch)),
    "xama-caido-x1": (X1, "xama", ["pele", "adornos", "chifres", "olhos", "boca"], _camada_xama),
    "xama-caido-x2": (X2, "xama", ["pele", "adornos", "cajado", "chifres", "olhos", "boca", "fogo"], _camada_xama),
    "xama-caido-x3": (X3, "xama", ["pele", "adornos", "chifres", "olhos", "boca", "fogo"], _camada_xama),
    "harpia-t": (HARPIA_T, "harpia_t", ["penas", "gola", "pescoco", "cabelo", "rosto"], _camada_harpia_t),
    "grifo-ga3": (GA3, "grifo", ["pelo", "cabeca", "bico", "olho"], _GRIFO.CAMADAS["grifo-ga"][3]),
    "xama-caido-x1r": (X1R, "xama", ["pele", "adornos", "chifres", "olhos", "boca"],  # as contas em sombra no colar
                       lambda x, y, ch: "adornos" if ch == "H" and y >= 11 else _camada_xama(x, y, ch)),
}


def cor(ident, ch):
    paleta = PALETAS[CAMADAS[ident][1]]
    if ident in ("xama-caido-x1", "xama-caido-x1r") and ch == "w":
        return "e8dcc0"  # a pintura branca do X1 (o osso do catálogo dos caídos)
    if ident == "xama-caido-x2" and ch == "W":
        return "d8ccac"  # o osso do cajado
    return paleta[ch]


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
