"""Monta as comparações das escolhas em faixas (fotografar.mjs) em tamanho real (1×), em capturas/comparacoes/:
  <janela>-<caso>.png: a lista parada antes (1.112.0) e depois (1.113.0), lado a lado; embaixo, os estados do depois
  (o mouse na mais alta, numa com teste, numa indisponível, o pressionado, o foco do teclado).
As telas inteiras ficam em capturas/ (<janela>-<caso>-<versão>-tela.png).

    python ferramentas/prototipos/hud/escolhas-faixas/comparar.py [pasta]   (padrão: capturas/)
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "capturas"
SAIDA = FOTOS / "comparacoes"
ESTADOS = {"2-mouse": "mouse na mais alta", "2b-mouse-teste": "mouse numa com teste", "2c-mouse-indisponivel": "mouse na indisponível",
           "3-pressionado": "pressionado", "4-foco": "foco do teclado"}


def linha(fotos, titulos):
    pares = [(f, t) for f, t in zip(fotos, titulos) if f.exists()]
    return em_colunas([f for f, _ in pares], [t for _, t in pares]) if pares else None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    casos = sorted({p.name.rsplit("-antes-1-parado.png", 1)[0] for p in FOTOS.glob("*-antes-1-parado.png")})
    feitas = []
    for base in casos:
        blocos = [linha([FOTOS / f"{base}-antes-1-parado.png", FOTOS / f"{base}-depois-1-parado.png"], [f"{base} · ANTES (1.112.0)", f"{base} · DEPOIS (1.113.0)"])]
        ests = [(FOTOS / f"{base}-depois-{e}.png", f"DEPOIS · {t}") for e, t in ESTADOS.items()]
        ests = [x for x in ests if x[0].exists()]
        for k in range(0, len(ests), 3):
            blocos.append(linha([f for f, _ in ests[k:k + 3]], [t for _, t in ests[k:k + 3]]))
        if em_linhas(blocos, SAIDA / f"{base}.png"):
            feitas.append(f"{base}.png")
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
