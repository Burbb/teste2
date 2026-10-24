"""Monta as cópias da segunda rodada (24/10/2026) em ../prototipo-v2/<direção>/: telas/achado.js e
telas/celebracoes.js da produção com a festa e o achado entregues à direção (ver ../v2/). O achado.js carrega antes do
celebracoes.js na página, então leva o FX, a Festa e a direção na frente; o celebracoes.js só passa o nível, o Sigilo e a
especialização para a Festa. Nada é gravado no jogo.

    python montar_v2.py            # as direções que existem em ../v2/
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
V2 = AQUI.parent / "v2"
SAIDA = AQUI.parent / "prototipo-v2"
DIRECOES = ["relicario", "estouro", "estandarte", "relicario2", "estouro2", "relicario3", "estouro3", "relicario4", "estouro4",
            "relicario5a", "relicario5b", "estouro5a", "estouro5b",
            "relicario5c", "estouro5c"]  # 5c: as candidatas finais  # 5a/5b: a mesma apresentação, a identidade 1 ou 2  # as de número 2: a rodada de refinamento


def trocar(s, a, b):
    assert a in s, a[:80]
    return s.replace(a, b, 1)


def main():
    achado = (RAIZ / "rpg/web/static/telas/achado.js").read_text(encoding="utf-8")
    celebracoes = (RAIZ / "rpg/web/static/telas/celebracoes.js").read_text(encoding="utf-8")
    achado = trocar(achado, "Object.assign(Telas, { abrirAchado, acoesDoAchado, fecharAchado, revelarAchado });",
                    "Object.assign(Telas, { abrirAchado: Festa.abrirAchado, acoesDoAchado, fecharAchado, revelarAchado });"
                    "  // PROTÓTIPO: a direção")
    ini = celebracoes.index('    let html = "", festa = null;')
    fim = celebracoes.index("  /** Contratos cumpridos:")
    celebracoes = (celebracoes[:ini] + "    return Festa.celebrar(m, caixa, instantaneo);  // PROTÓTIPO: a direção\n  }\n\n"
                   + celebracoes[fim:])
    base = "\n".join((V2 / f).read_text(encoding="utf-8") for f in ("fx.js", "festas.js", "identidade.js", "identidades.js", "identidades2.js")) + "\n"
    for nome in DIRECOES:
        variante = nome[-1] if nome[-2:-1].isdigit() and nome[-1] in "abc" else None
        fonte = V2 / f"{nome[:-1] if variante else nome}.js"
        if not fonte.exists():
            continue
        pasta = SAIDA / nome
        pasta.mkdir(parents=True, exist_ok=True)
        cab = (f"/* PROTÓTIPO da etapa 2, segunda rodada, direção {nome} (montado por auxiliares/montar_v2.py; nada no "
               f"jogo). */\n")
        prefixo = f'const IDENTIDADE_VARIANTE = "{variante}";\n' if variante else ""
        (pasta / "achado.js").write_text(cab + prefixo + base + fonte.read_text(encoding="utf-8") + "\n" + achado, encoding="utf-8")
        (pasta / "celebracoes.js").write_text(cab + celebracoes, encoding="utf-8")
        print("montado:", nome)


if __name__ == "__main__":
    sys.exit(main())
