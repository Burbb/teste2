"""Monta as comparações do seletor de habilidades a partir de fotografar_seletor.mjs (capturas-seletor/), tudo em
tamanho real (nada ampliado nem reduzido; as telas inteiras e a escolha do alvo ficam nos arquivos de cada versão,
<janela>-<luta>-<versão>-tela.png e -5-alvo.png):
  - <janela>-<luta>-paineis.png: a roda com o painel aberto, o jogo de hoje e as três propostas lado a lado;
  - <janela>-<luta>-interacoes.png: uma linha por versão com o mouse numa habilidade, o mouse numa indisponível (a dica
    e o motivo) e o foco do teclado;

    python ferramentas/prototipos/hud/comparar_seletor.py [pasta]   (padrão: capturas-seletor/)
"""

import pathlib
import sys

from PIL import Image, ImageDraw

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "capturas-seletor"
FUNDO, TEXTO = (17, 18, 21), (214, 205, 186)
VERSOES = (("atual", "o jogo hoje"), ("a", "A · lista integrada"), ("b", "B · grade compacta"), ("c", "C · losangos"))
LUTAS = ("guerreiro", "arqueiro", "capacidade")


def grade(celulas, colunas):
    """celulas: [(imagem, rótulo)], montadas em linhas de `colunas`, cada uma com o rótulo em cima."""
    linhas = [celulas[i:i + colunas] for i in range(0, len(celulas), colunas)]
    larg = [max(c[k][0].width for c in linhas if k < len(c)) for k in range(colunas)]
    alt = [max(i.height for i, _ in ln) for ln in linhas]
    out = Image.new("RGB", (sum(larg) + 16 * (colunas + 1), sum(alt) + 26 * len(linhas) + 16), FUNDO)
    d, y = ImageDraw.Draw(out), 8
    for ln, h in zip(linhas, alt):
        x = 16
        for (img, rot), w in zip(ln, larg):
            d.text((x, y), rot, fill=TEXTO)
            out.paste(img, (x, y + 16))
            x += w + 16
        y += h + 26
    return out


def abrir(nome):
    p = FOTOS / f"{nome}.png"
    return Image.open(p).convert("RGB") if p.exists() else None


def main():
    feitos = 0
    for jan in ("normal", "baixa"):
        for luta in LUTAS:
            base = f"{jan}-{luta}"
            if not abrir(f"{base}-atual-tela"):
                continue
            rot = lambda r, extra="": f"{jan} · {luta} · {r}{extra}"
            grade([(abrir(f"{base}-{v}-1-aberto"), rot(r)) for v, r in VERSOES], 4).save(FOTOS / f"{base}-paineis.png")
            cel = []
            for v, r in VERSOES:
                for estado, nome in (("2-mouse", "mouse"), ("3-indisponivel", "mouse na indisponível"), ("4-teclado", "foco do teclado")):
                    img = abrir(f"{base}-{v}-{estado}")
                    cel.append((img or Image.new("RGB", (10, 10), FUNDO), rot(r, f" · {nome}")))
            grade(cel, 3).save(FOTOS / f"{base}-interacoes.png")
            feitos += 1
    print(f"{feitos} conjuntos de comparações em {FOTOS}")


if __name__ == "__main__":
    main()
