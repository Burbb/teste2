"""Monta as comparações dos comandos da luta e da amostra da exploração (comandos/) a partir das fotos de
fotografar_comandos.mjs (capturas-comandos/), tudo em tamanho real (1×), na pasta comparacoes/ dentro dela:
  - luta-<janela>-<luta>.png: a arena depois de uma rodada, com os mesmos dados: o jogo de hoje, os comandos novos com as
    cartas de hoje e os comandos novos com o acabamento contido das cartas;
  - estados-<janela>-<luta>.png: os estados da roda (parado, mouse, pressionado, foco do teclado, Habilidades aberto,
    foco e aberto juntos, Itens aberto, a volta da mira), uma linha por estado, as três versões lado a lado;
  - golpe-<janela>-<luta>.png: o golpe no meio (o número e o efeito que passam da moldura);
  - exploracao-<janela>-<lugar>.png: as escolhas de hoje e a amostra, paradas; e os estados da amostra (mouse na mais
    alta, pressionado, foco do teclado);
  - comportamentos.png: a entrada e o movimento reduzido.
As telas inteiras ficam nos arquivos de capturas-comandos/ (<janela>-<luta>-<versão>-tela.png e -tela-aberto.png).

    python ferramentas/prototipos/hud/comparar_comandos.py [pasta]   (padrão: capturas-comandos/)
"""
import pathlib
import sys

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comparar_varinha import FUNDO, em_colunas  # noqa: E402

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "capturas-comandos"
SAIDA = FOTOS / "comparacoes"
VERSOES = {"atual": "o jogo de hoje", "comandos": "comandos novos, cartas de hoje", "cartas": "comandos novos, cartas contidas"}
ESTADOS = {"1-normal": "parado", "2-mouse": "mouse em Atacar", "3-pressionado": "pressionado", "4-foco": "foco do teclado (Tab)",
           "5-aberto": "Habilidades aberto", "6-foco-aberto": "foco e aberto juntos", "7-itens": "Itens aberto (alternou)",
           "9-volta": "de volta da mira"}


def em_linhas(blocos, saida):
    """Empilha imagens (já com títulos) de cima para baixo."""
    blocos = [b for b in blocos if b]
    if not blocos:
        return False
    img = Image.new("RGB", (max(b.width for b in blocos), sum(b.height + 8 for b in blocos) + 8), FUNDO)
    y = 8
    for b in blocos:
        img.paste(b, (0, y)); y += b.height + 8
    img.save(saida)
    return True


def linha(fotos, titulos):
    pares = [(f, t) for f, t in zip(fotos, titulos) if f.exists()]
    return em_colunas([f for f, _ in pares], [t for _, t in pares]) if pares else None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = []
    nomes = {p.name for p in FOTOS.glob("*.png")}
    lutas = sorted({n.split("-")[1] for n in nomes if n.endswith("-arena.png")} - {"explora"})
    janelas = [j for j in ("normal", "baixa", "grande", "escala") if any(n.startswith(j + "-") for n in nomes)]
    for jan in janelas:
        for luta in lutas:
            vs = [v for v in VERSOES if (FOTOS / f"{jan}-{luta}-{v}-arena.png").exists()]
            if not vs:
                continue
            for sufixo, nome in (("arena", "luta"), ("0-golpe", "golpe")):
                b = linha([FOTOS / f"{jan}-{luta}-{v}-{sufixo}.png" for v in vs], [f"{jan} · {luta} · {VERSOES[v]}" for v in vs])
                if b:
                    b.save(SAIDA / f"{nome}-{jan}-{luta}.png"); feitas.append(f"{nome}-{jan}-{luta}.png")
            blocos = [linha([FOTOS / f"{jan}-{luta}-{v}-{e}.png" for v in vs], [f"{rot} · {VERSOES[v]}" for v in vs])
                      for e, rot in ESTADOS.items()]
            if em_linhas(blocos, SAIDA / f"estados-{jan}-{luta}.png"):
                feitas.append(f"estados-{jan}-{luta}.png")
        lugares = sorted({n.split("-")[2] for n in nomes if n.startswith(f"{jan}-explora-")})
        for lugar in lugares:
            base = f"{jan}-explora-{lugar}"
            blocos = [linha([FOTOS / f"{base}-atual-1-normal.png", FOTOS / f"{base}-comandos-1-normal.png"],
                            [f"{jan} · {lugar} · o jogo de hoje", "a amostra"]),
                      linha([FOTOS / f"{base}-comandos-{e}.png" for e in ("2-mouse", "3-pressionado", "4-foco")],
                            ["mouse (na mais alta)", "pressionado", "foco do teclado"])]
            if em_linhas(blocos, SAIDA / f"exploracao-{jan}-{lugar}.png"):
                feitas.append(f"exploracao-{jan}-{lugar}.png")
    entradas = [linha([FOTOS / f"comportamento-{v}-{e}.png" for v in VERSOES], [f"{rot} · {VERSOES[v]}" for v in VERSOES])
                for e, rot in (("entrada", "a roda entrando"), ("reduzido-entrada", "movimento reduzido, entrando"),
                               ("reduzido-pressionado", "movimento reduzido, pressionado"))]
    if em_linhas(entradas, SAIDA / "comportamentos.png"):
        feitas.append("comportamentos.png")
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
