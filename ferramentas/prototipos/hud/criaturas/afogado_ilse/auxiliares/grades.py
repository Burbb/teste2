"""O primeiro par das criaturas (21/10/2026, escolha do Jean): a carta do Afogado e a carta da Ilse, cabeças de 16×16
no formato dos retratos de carta aprovados (retratos.js: ODETE_CARTA, YARA_CARTA): cabeça e ombros que enchem o quadro
até a base, sem contorno preto (a caixa da carta é escura), poucos planos, a luz da esquerda. O jogo mostra a 2× na
carta da luta (32 px) e a 3× no Bestiário e no mural (48 px).

  - Afogado (`afogado`, morto-vivo do Charco e da Capela: "os que o pântano não devolveu; agarram e puxam para o
    fundo"): um homem afogado, a cabeça inchada e larga, a pele cinza-esverdeada de quem ficou na água, as órbitas fundas
    e escuras com um ponto pálido, a boca aberta, fios de alga colados no crânio e caindo dos lados, a roupa podre nos
    ombros. Diferente da Ilse pela cabeça mais larga e redonda, sem cabelo comprido, e pela pele verde, não azul.
  - Ilse (a carta da guardiã da Capela): a transposição da figura dela na cena do fundo (telas/cenas.js, ilseDesenho, a
    paleta CORF): o rosto estreito azulado, o cabelo de algas comprido dos dois lados, a mecha molhada que cobre o olho
    direito, o olho esquerdo claro, o vestido escuro. O cabelo sobe um tom em relação à cena, para não sumir na caixa
    escura da carta.
Grava grades/<id>.txt e listas/<id>/<camada>.lua (com ordem.txt) para o pintar.lua.
    python grades.py <pasta da proposta>
"""
import pathlib
import sys

CORES = {
    # o afogado: a pele, os olhos, a boca, as algas e a roupa
    "P": "93a48c", "p": "73866f", "o": "53654f", "O": "37463a",
    "e": "121814", "E": "c8d6c0", "m": "1e1614",
    "A": "4c6a40", "a": "2c4130", "b": "1c2b1f",
    "R": "4e4234", "r": "362d22", "q": "241e17",
    # a Ilse: a paleta da cena (CORF), com o cabelo um tom acima
    "S": "a0b8c2", "s": "7d98a6", "z": "55707e", "W": "c4d4da",
    "H": "3d5a40", "h": "2c4130", "g": "1c2b1f", "G": "0d160f",
    "V": "3a3430", "v": "25211e",
    # os fios de alga da Ilse R2: o fio iluminado um pouco mais verde, sem subir muito o brilho
    "I": "4f6e47",
    # o Afogado B: a pele manchada e a carne mais escura do inchaço
    "M": "5f6f55", "n": "2a332b",
}

AFOGADO = [
    "................",
    ".....aAAa.......",
    "....aPPPPpab....",
    "...aPPPPPppoa...",
    "...PPPPPPppoob..",
    "..aPeePPPeepooa.",
    "..aPeEPPPeEpoob.",
    "..aPPPPppppooob.",
    "..b.PPpmmmppoo..",
    "..a.pPpmmmpooO..",
    "..b..ppoooooOO..",
    "..a...ooooOO.b..",
    "..RRRRooooORRR..",
    ".RRRrRRoooRRrRr.",
    "RRRrrRRRORRrrrrq",
    "RRrrrrRRrRrrrrqq",
]
ILSE = [
    "................",
    "......gggg......",
    ".....ghhhhg.....",
    ".....hSSssgg....",
    "....hgSSsGGgh...",
    "....h.SWsGzg.h..",
    "...H.hSSsGzzh.g.",
    "...H.hSSssGzh.g.",
    "...h.hSSzszh..h.",
    "..H..h.Sssz.h.g.",
    "..H.h...ss...hg.",
    "..h.hVVVssVVVhg.",
    ".H.hVVVVVVVVvvhg",
    ".h.hVVVVVVVvvvhg",
    "H.hVVVVVVVvvvvvg",
    "h.hVVVVVVVvvvvvg",
]

# A segunda rodada (21/10/2026, pedido do Jean): a Ilse com fios de alga soltos (traçados um a um, de trás para a
# frente) e o Afogado com outra construção do rosto
ILSE_R2 = [
    "................",
    ".....hHIhGh.....",
    "....hIIhGGGh....",
    "...hHISSSGG.hH..",
    "..ghHISSSGG.hH..",
    "..ghHISWSGG.hHg.",
    ".gh.HISSsGG.h.H.",
    ".ghH..ISGszGh.Hg",
    ".ghH..ISsszGh.Hg",
    ".ghH.I.Ssz.G.hHg",
    "g.hH.I..sz.G.hHg",
    "gh.HVVV.sz.VVhHg",
    "ghHVVVVVssVVVhvg",
    "ghVVVVVVVVVvvhvg",
    "gVVVVVVVVVvvvvvg",
    "VVVVVVVVVvvvvvvv",
]
AFOGADO_B = [
    "................",
    ".....baAAa......",
    "....aPPPPPpa....",
    "...aPPPPPPppa...",
    "...PPPPPPPppob..",
    "..aPnnPPpnnpob..",
    "..aPnEnPpneopob.",
    "..PPPnPPpppMoob.",
    ".aPPPPPPoppMooo.",
    ".bPPPPpppppoooO.",
    "..PPPpnmmmnpoOO.",
    "..aPppmmmmpoOOb.",
    "...poppnnpoOO...",
    ".RRRooooooORRR..",
    "RRRrRRoooRRrrRrq",
    "RRrrrRRRORRrrrqq",
]

CAMADAS = {
    "afogado": (AFOGADO, ["roupa", "pele", "olhos", "algas"],
                lambda x, y, ch: "roupa" if ch in "Rrq" else "olhos" if ch in "eEm" else "algas" if ch in "Aab" else "pele"),
    "ilse": (ILSE, ["vestido", "rosto", "cabelo"],
             lambda x, y, ch: "vestido" if ch in "Vv" else "rosto" if ch in "SsW" or (ch == "z" and y >= 4) else "cabelo"),
    "ilse-r2": (ILSE_R2, ["vestido", "rosto", "algas"],
                lambda x, y, ch: "vestido" if ch in "Vv" else "rosto" if ch in "SsWz" else "algas"),
    "afogado-b": (AFOGADO_B, ["roupa", "pele", "rosto", "algas"],
                  lambda x, y, ch: "roupa" if ch in "Rrq" else "rosto" if ch in "eEmn" else "algas" if ch in "Aab" else "pele"),
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
