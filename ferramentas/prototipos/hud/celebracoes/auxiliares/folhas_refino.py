"""A folha do refinamento (24/10/2026): cada momento na A e na A2, na B e na B2 (1920×945), e as refinadas em 1280×720.
As versões anteriores vêm de ../capturas-v2/ (900 ms); as refinadas, de ../capturas-refino/ (1200 ms).

    python folhas_refino.py
"""
import pathlib

from folhas_v2 import folha, quadro

BASE = pathlib.Path(__file__).resolve().parents[1]
V2, REF = BASE / "capturas-v2", BASE / "capturas-refino"
MOMENTOS = [("dois-niveis", "nivel2", "Nível (real)"), ("especializacao", "spec", "Especialização (real)"),
            ("sigilo", "sigilo", "Sigilo (real)"), ("raridades", "comum", "Comum (real)"), ("raridades", "magico", "Mágico (real)"),
            ("raridades", "raro", "Raro, com a comparação (real)"), ("raridades", "lendario", "Lendário (real)"),
            ("limites", "nivel", "SIMULAÇÃO: textos longos"), ("limites", "lendario", "SIMULAÇÃO: nome longo")]


def main():
    meio = (360, 0, 1560, 945)
    linhas = [(rot, [quadro(V2 / "relicario" / "1920" / f"{s}-{f}-0900.png", meio, 0.36),
                     quadro(REF / "relicario2" / "1920" / f"{s}-{f}-1200.png", meio, 0.36),
                     quadro(V2 / "estouro" / "1920" / f"{s}-{f}-0900.png", meio, 0.36),
                     quadro(REF / "estouro2" / "1920" / f"{s}-{f}-1200.png", meio, 0.36)]) for s, f, rot in MOMENTOS]
    folha(["A · 1ª versão", "A2 · refinado", "B · 1ª versão", "B2 · refinado"], linhas, REF / "folha-refino.png")
    linhas = [(rot, [quadro(REF / d / "1280" / f"{s}-{f}-1200.png", None, 0.42) for d in ("relicario2", "estouro2")])
              for s, f, rot in MOMENTOS if (REF / "relicario2" / "1280" / f"{s}-{f}-1200.png").exists()]
    folha(["A2 · 1280×720", "B2 · 1280×720"], linhas, REF / "folha-refino-1280.png")


if __name__ == "__main__":
    main()
