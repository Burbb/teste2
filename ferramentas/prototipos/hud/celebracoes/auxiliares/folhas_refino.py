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


def rodada3():
    """A terceira rodada: A2 × A3 e B2 × B3 (1920, 1200 ms) e as duas em 1280×720 e com movimento reduzido."""
    R3 = BASE / "capturas-r3"
    meio = (360, 0, 1560, 945)
    momentos = [("dois-niveis", "nivel2", "Nível (real)"), ("especializacao", "spec", "Piromante (real)"), ("sigilo", "sigilo", "Sigilo (real)"),
                ("raridades", "comum", "Comum (real)"), ("raridades", "magico", "Mágico (real)"), ("raridades", "raro", "Raro (real)"),
                ("raridades", "lendario", "Lendário (real)"), ("limites", "lendario", "SIMULAÇÃO: nome longo")]
    linhas = [(rot, [quadro(REF / "relicario2" / "1920" / f"{s}-{f}-1200.png", meio, 0.36), quadro(R3 / "relicario3" / "1920" / f"{s}-{f}-1200.png", meio, 0.36),
                     quadro(REF / "estouro2" / "1920" / f"{s}-{f}-1200.png", meio, 0.36), quadro(R3 / "estouro3" / "1920" / f"{s}-{f}-1200.png", meio, 0.36)])
              for s, f, rot in momentos]
    folha(["A2 · anterior", "A3 · Relicário", "B2 · anterior", "B3 · Estouro"], linhas, R3 / "folha-r3.png")
    linhas = [(rot, [quadro(R3 / d / "1280" / f"{s}-{f}-1200.png", None, 0.42) for d in ("relicario3", "estouro3")] +
               [quadro(R3 / d / "reduzido" / f"{s}-{f}-1200.png", meio, 0.3) for d in ("relicario3", "estouro3")])
              for s, f, rot in momentos if (R3 / "relicario3" / "1280" / f"{s}-{f}-1200.png").exists()]
    folha(["A3 · 1280×720", "B3 · 1280×720", "A3 · reduzido", "B3 · reduzido"], linhas, R3 / "folha-r3-apertados.png")


def rodada4():
    """A quarta rodada: as seis especializações nas duas apresentações (a entrada, a sustentação, 1280×720 e o movimento
    reduzido) e o selo dos itens do Estouro, B3 × B4."""
    R4 = BASE / "capturas-r4"
    meio = (480, 40, 1440, 620)
    specs = [("piromante", "Piromante (aprovado)"), ("paladino", "Paladino"), ("berserker", "Berserker"),
             ("patrulheiro", "Patrulheiro"), ("sombra", "Sombra"), ("necromante", "Necromante")]
    linhas = []
    for k, rot in specs:
        ims = []
        for d in ("estouro4", "relicario4"):
            ims += [quadro(R4 / d / "1920" / f"spec-{k}-{k}-{ms}.png", meio, 0.36) for ms in ("0150", "2600")]
        ims += [quadro(R4 / d / "reduzido" / f"spec-{k}-{k}-1500.png", meio, 0.36) for d in ("estouro4", "relicario4")]
        linhas.append((rot, ims))
    folha(["B4 · entrada (150 ms)", "B4 · depois (2,6 s)", "A4 · entrada (150 ms)", "A4 · depois (2,6 s)", "B4 · reduzido", "A4 · reduzido"],
          linhas, R4 / "folha-r4-especializacoes.png")
    linhas = [(rot, [quadro(R4 / d / "1280" / f"spec-{k}-{k}-1500.png", None, 0.42) for d in ("estouro4", "relicario4")]) for k, rot in specs]
    folha(["B4 · 1280×720", "A4 · 1280×720"], linhas, R4 / "folha-r4-especializacoes-1280.png")
    caixa = (480, 200, 1300, 640)
    linhas = [(f"{rot} (real)", [quadro(R4 / f"itens-{d}" / f"itens-estouro-{f}-1500.png", caixa, 0.55) for d in ("estouro3", "estouro4")])
              for f, rot in (("raro1", "Raro, peito"), ("lendario1", "Lendário, anel"), ("raro2", "Raro, pés"), ("lendario2", "Lendário, mãos"))]
    folha(["B3 · antes", "B4 · depois"], linhas, R4 / "folha-r4-itens-estouro.png")


def rodada5():
    """A quinta rodada: as duas identidades de cada especialização, no Estouro (a entrada aos 400 ms e a permanência aos
    3 s) e no Relicário (3 s); e 1280×720 e o movimento reduzido."""
    R5 = BASE / "capturas-r5"
    meio = (480, 20, 1440, 600)
    specs = [("paladino", "Paladino · 1 Luz do alto / 2 Asas"), ("berserker", "Berserker · 1 O nome sangra / 2 Garras"),
             ("patrulheiro", "Patrulheiro · 1 Vendaval / 2 Clareira"), ("sombra", "Sombra · 1 Corte / 2 Invisível"),
             ("necromante", "Necromante · 1 Erguer / 2 Almas")]
    linhas = [(rot, [quadro(R5 / "estouro5a" / "1920" / f"spec-{k}-{k}-0400.png", meio, 0.3), quadro(R5 / "estouro5a" / "1920" / f"spec-{k}-{k}-3000.png", meio, 0.3),
                     quadro(R5 / "estouro5b" / "1920" / f"spec-{k}-{k}-0400.png", meio, 0.3), quadro(R5 / "estouro5b" / "1920" / f"spec-{k}-{k}-3000.png", meio, 0.3),
                     quadro(R5 / "relicario5a" / "1920" / f"spec-{k}-{k}-3000.png", meio, 0.3), quadro(R5 / "relicario5b" / "1920" / f"spec-{k}-{k}-3000.png", meio, 0.3)])
              for k, rot in specs]
    folha(["Estouro 1 · entrada", "Estouro 1 · 3 s", "Estouro 2 · entrada", "Estouro 2 · 3 s", "Relicário 1 · 3 s", "Relicário 2 · 3 s"],
          linhas, R5 / "folha-r5-identidades.png")
    linhas = [(rot, [quadro(R5 / d / "1280" / f"spec-{k}-{k}-1500.png", None, 0.36) for d in ("estouro5a", "estouro5b")] +
               [quadro(R5 / d / "reduzido" / f"spec-{k}-{k}-1500.png", meio, 0.3) for d in ("estouro5a", "estouro5b", "relicario5a", "relicario5b")])
              for k, rot in specs]
    folha(["Estouro 1 · 1280", "Estouro 2 · 1280", "Estouro 1 · reduzido", "Estouro 2 · reduzido", "Relicário 1 · reduzido", "Relicário 2 · reduzido"],
          linhas, R5 / "folha-r5-apertados.png")


def rodada6():
    """A sexta rodada: as candidatas finais, no Estouro e no Relicário (a entrada, o corte da Sombra, a permanência), e
    1280×720 e o movimento reduzido."""
    R6 = BASE / "capturas-r6"
    meio = (480, 0, 1440, 600)
    specs = [("paladino", "Paladino · luz do alto com penas"), ("berserker", "Berserker · garras, sangue líquido"),
             ("patrulheiro", "Patrulheiro · vendaval em verde"), ("sombra", "Sombra · invisível com o corte"),
             ("necromante", "Necromante · erguer com fumaça")]
    linhas = [(rot, [quadro(R6 / d / "1920" / f"spec-{k}-{k}-{ms}.png", meio, 0.3) for d in ("estouro5c", "relicario5c") for ms in ("0200", "1200", "3500")])
              for k, rot in specs]
    folha(["Estouro · 0,2 s", "Estouro · 1,2 s", "Estouro · 3,5 s", "Relicário · 0,2 s", "Relicário · 1,2 s", "Relicário · 3,5 s"],
          linhas, R6 / "folha-r6-finais.png")
    linhas = [(rot, [quadro(R6 / d / "1280" / f"spec-{k}-{k}-1600.png", None, 0.36) for d in ("estouro5c", "relicario5c")] +
               [quadro(R6 / d / "reduzido" / f"spec-{k}-{k}-1600.png", meio, 0.3) for d in ("estouro5c", "relicario5c")])
              for k, rot in specs]
    folha(["Estouro · 1280", "Relicário · 1280", "Estouro · reduzido", "Relicário · reduzido"], linhas, R6 / "folha-r6-apertados.png")


def rodada7():
    """A sétima rodada: as três alternativas do sangue do Berserker (o título ampliado, para ver as gotas) e as três da
    luz do Paladino, no Estouro e no Relicário; e 1280×720 e o movimento reduzido."""
    from PIL import Image
    R7 = BASE / "capturas-r7"
    rot = {"d": "A", "e": "B", "f": "C"}
    titulo = (760, 280, 1160, 440)
    linhas = []
    for v in "def":
        ims = []
        for ms in ("1500", "3100"):
            for d in ("estouro5", "relicario5"):
                q = quadro(R7 / f"{d}{v}" / "1920" / f"spec-berserker-berserker-{ms}.png", titulo if d == "estouro5" else (760, 260, 1160, 420), 1)
                ims.append(q.resize((q.width * 2, q.height * 2), Image.NEAREST) if q else None)
        linhas.append((f"Berserker {rot[v]} (título a 2×, para ver o sangue)", ims))
    folha(["Estouro · 1,5 s", "Relicário · 1,5 s", "Estouro · 3,1 s", "Relicário · 3,1 s"], linhas, R7 / "folha-r7-berserker.png")
    meio = (460, 0, 1460, 560)
    linhas = [(f"Paladino {rot[v]}", [quadro(R7 / f"{d}{v}" / "1920" / f"spec-paladino-paladino-{ms}.png", meio, 0.4) for d in ("estouro5", "relicario5") for ms in ("0300", "3100")])
              for v in "def"]
    folha(["Estouro · 0,3 s", "Estouro · 3,1 s", "Relicário · 0,3 s", "Relicário · 3,1 s"], linhas, R7 / "folha-r7-paladino.png")
    linhas = [(f"{k} {rot[v]}", [quadro(R7 / f"{d}{v}" / "1280" / f"spec-{k}-{k}-1600.png", None, 0.36) for d in ("estouro5", "relicario5")] +
               [quadro(R7 / f"{d}{v}" / "reduzido" / f"spec-{k}-{k}-1600.png", (560, 40, 1360, 500), 0.4) for d in ("estouro5", "relicario5")])
              for k in ("paladino", "berserker") for v in "def"]
    folha(["Estouro · 1280", "Relicário · 1280", "Estouro · reduzido", "Relicário · reduzido"], linhas, R7 / "folha-r7-apertados.png")


def producao():
    """O jogo (1.201.0): cada momento nas duas apresentações (3 s), e 1280×720 e o movimento reduzido."""
    RP = BASE / "capturas-producao"
    meio = (360, 0, 1560, 780)
    momentos = [("dois-niveis", "nivel2", "Nível (dois seguidos)"), ("raridades", "comum", "Comum"), ("raridades", "magico", "Mágico"),
                ("raridades", "raro", "Raro, com a comparação"), ("raridades", "lendario", "Lendário"), ("sigilo", "sigilo", "Sigilo"),
                ("limites", "lendario", "Texto longo (simulação)")] + [(f"spec-{k}", k, k.capitalize()) for k in
                ("piromante", "paladino", "berserker", "patrulheiro", "sombra", "necromante")]
    linhas = [(rot, [quadro(RP / a / "1920" / f"{s}-{f}-3000.png", meio, 0.3) for a in ("estouro", "relicario")] +
               [quadro(RP / a / "1280" / f"{s}-{f}-1500.png", None, 0.28) for a in ("estouro", "relicario")] +
               [quadro(RP / a / "reduzido" / f"{s}-{f}-1500.png", meio, 0.22) for a in ("estouro", "relicario")])
              for s, f, rot in momentos]
    folha(["Estouro · 1920", "Relicário · 1920", "Estouro · 1280", "Relicário · 1280", "Estouro · reduzido", "Relicário · reduzido"],
          linhas, RP / "folha-producao.png")


if __name__ == "__main__":
    import sys
    producao() if "producao" in sys.argv else rodada7() if "r7" in sys.argv else rodada6() if "r6" in sys.argv else rodada5() if "r5" in sys.argv else rodada4() if "r4" in sys.argv else rodada3() if "r3" in sys.argv else main()
