"""Monta as comparações da rodada 2 (fotografar.mjs) em tamanho real (1×), em capturas/comparacoes/: as telas inteiras
lado a lado, com os mesmos dados:
  baixa-<luta>-habilidades.png      b (custo ao lado) × b2 (custo embaixo), Habilidades com a descrição mais longa;
  baixa-maior-itens.png             b × b2, Itens;
  baixa-<luta>-efeitos-reais.png    b × b2 × r, os efeitos de um momento real do motor, Habilidades aberto;
  normal-maior-efeitos-reais.png    b2 × r em 1500×950 (o registro fica embaixo: há espaço);
  teclado-redimensionar.png         b2: as setas e os três tamanhos com o seletor aberto.

    python ferramentas/prototipos/hud/compacta/rodada2/comparar.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1]))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = AQUI / "capturas"
SAIDA = FOTOS / "comparacoes"
NOMES = {"b": "B da rodada 1, corrigida (o custo ao lado do nome)", "b2": "B refinada (o custo embaixo do nome)",
         "r": "B refinada + o registro na coluna do mundo"}
LUTAS = {"arqueiro": "Arqueiro patrulheiro (4) contra 5 caídos e o xamã", "maior": "Necromante (6) contra 5 caídos e o xamã"}


def lado_a_lado(saida, jan, luta, foto, versoes, titulo):
    fotos = [(FOTOS / f"{jan}-{luta}-{v}-{foto}.png", f"{jan} · {LUTAS[luta]} · {titulo} · {NOMES[v]}") for v in versoes]
    fotos = [(f, t) for f, t in fotos if f.exists()]
    if fotos:
        em_colunas([f for f, _ in fotos], [t for _, t in fotos]).save(SAIDA / saida)
        return saida


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = [lado_a_lado(f"baixa-{luta}-habilidades.png", "baixa", luta, "2-habilidades", ("b", "b2"), "Habilidades, a descrição mais longa")
              for luta in LUTAS]
    feitas.append(lado_a_lado("baixa-maior-itens.png", "baixa", "maior", "3-itens", ("b", "b2"), "Itens"))
    feitas += [lado_a_lado(f"baixa-{luta}-efeitos-reais.png", "baixa", luta, "6-efeitos-reais-habilidades", ("b", "b2", "r"),
                           "efeitos de um momento real, Habilidades aberto") for luta in LUTAS]
    feitas.append(lado_a_lado("normal-maior-efeitos-reais.png", "normal", "maior", "6-efeitos-reais-habilidades", ("b2", "r"),
                              "efeitos de um momento real, Habilidades aberto"))
    tec = [FOTOS / "teclado-b2-1-setas.png"] + sorted(FOTOS.glob("teclado-b2-2-redimensionado-*.png"))
    tec = [f for f in tec if f.exists()]
    if tec and em_linhas([em_colunas([f], [f"b2 · teclado e movimento reduzido · {f.stem.replace('teclado-b2-', '')}"]) for f in tec],
                         SAIDA / "teclado-redimensionar.png"):
        feitas.append("teclado-redimensionar.png")
    print("\n".join(f for f in feitas if f))


if __name__ == "__main__":
    main()
