"""Monta as comparações da HUD integrada e das lutas cheias (fotografar_lutas_cheias.mjs) em tamanho real (1×), na pasta
comparacoes/ de capturas-lutas-cheias/, sempre o jogo de antes (1.110.0) ao lado do de agora, com os mesmos dados:
  - luta-<janela>-<luta>.png: a arena parada depois de uma rodada; embaixo, a mira (o lembrete e o Voltar);
  - estados-<janela>-<luta>.png: o mouse, o pressionado, o foco do teclado, Itens aberto (alternou), a mira com o mouse
    num alvo e a volta da mira; no depois, a saída e a entrada SIMULADAS (marcadas) e a invocação real, quando há;
  - golpe-<janela>-<luta>.png: o golpe no meio (o número e o efeito que passam da moldura);
  - exploracao-<janela>-<lugar>.png: as escolhas paradas, antes e depois; os estados do depois; o teste de esforço vem
    marcado como SIMULADO (na Capela, a tela depois de escolher a ação real fica em capturas-lutas-cheias/);
  - comportamentos.png: o movimento reduzido.
As telas inteiras ficam em capturas-lutas-cheias/ (<janela>-<luta>-<versão>-tela.png).

    python ferramentas/prototipos/hud/comparar_lutas_cheias.py [pasta]   (padrão: capturas-lutas-cheias/)
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "capturas-lutas-cheias"
SAIDA = FOTOS / "comparacoes"
VERSOES = {"antes": "ANTES (1.110.0)", "depois": "DEPOIS (integrado)"}
LUTAS = {"poucos": "2 lobos, Morel", "noite": "3 lobos à noite, Morel e Odette", "cinco": "5 lobos, comitiva e o lobo do patrulheiro",
         "maior": "o maior real: 6 aliados × 6 inimigos", "longos": "4 esqueletos com os nomes mais longos"}
ESTADOS = {"2-mouse": "mouse em Atacar", "3-pressionado": "pressionado", "4-foco": "foco do teclado (Tab)", "5-itens": "Itens aberto (alternou)",
           "7-mira-mouse": "mira, mouse num alvo", "9-volta": "de volta da mira"}
SO_DEPOIS = {"8-saida-simulada": "SIMULADO: um inimigo sai durante a mira (fica a vaga)",
             "9b-entrada-simulada": "SIMULADO: um reforço entra (no fim da coluna)", "10-invocacao": "Erguer Servo (invocação real)"}
LUGARES = {"esforco": "TESTE DE ESFORÇO: 1ª opção com texto SIMULADO (o jogo não tem)", "capela": "Capela à noite, com tocha (ação real)",
           "escura": "Capela à noite, sem tocha (ação real, o risco mais longo)", "bosque": "Bosque", "charco": "Charco com contrato",
           "covil": "covil"}


def linha(fotos, titulos):
    pares = [(f, t) for f, t in zip(fotos, titulos) if f.exists()]
    return em_colunas([f for f, _ in pares], [t for _, t in pares]) if pares else None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = []
    nomes = {p.name for p in FOTOS.glob("*.png")}
    for jan in ("baixa", "normal", "grande", "escala"):
        for luta, rot in LUTAS.items():
            base = f"{jan}-{luta}"
            if not any(n.startswith(base + "-") for n in nomes):
                continue
            tit = lambda v, extra="": f"{jan} · {rot} · {VERSOES[v]}{extra}"  # noqa: E731
            blocos = [linha([FOTOS / f"{base}-{v}-1-normal.png" for v in VERSOES], [tit(v) for v in VERSOES]),
                      linha([FOTOS / f"{base}-{v}-6-mira.png" for v in VERSOES], [tit(v, " · a mira") for v in VERSOES])]
            if em_linhas(blocos, SAIDA / f"luta-{base}.png"):
                feitas.append(f"luta-{base}.png")
            b = linha([FOTOS / f"{base}-{v}-0-golpe.png" for v in VERSOES], [tit(v, " · o golpe") for v in VERSOES])
            if b:
                b.save(SAIDA / f"golpe-{base}.png"); feitas.append(f"golpe-{base}.png")
            blocos = [linha([FOTOS / f"{base}-{v}-{e}.png" for v in VERSOES], [f"{r} · {VERSOES[v]}" for v in VERSOES]) for e, r in ESTADOS.items()]
            blocos += [linha([FOTOS / f"{base}-depois-{e}.png" for e in SO_DEPOIS], [f"{r} · {VERSOES['depois']}" for r in SO_DEPOIS.values()])]
            if em_linhas(blocos, SAIDA / f"estados-{base}.png"):
                feitas.append(f"estados-{base}.png")
        for lugar, rot in LUGARES.items():
            base = f"{jan}-explora-{lugar}"
            if not any(n.startswith(base + "-") for n in nomes):
                continue
            blocos = [linha([FOTOS / f"{base}-{v}-1-normal.png" for v in VERSOES], [f"{jan} · {rot} · {VERSOES[v]}" for v in VERSOES]),
                      linha([FOTOS / f"{base}-depois-{e}.png" for e in ("2-mouse", "3-pressionado", "4-foco")],
                            [f"{VERSOES['depois']} · {t}" for t in ("mouse na mais alta", "pressionado", "foco do teclado")])]
            if em_linhas(blocos, SAIDA / f"exploracao-{base}.png"):
                feitas.append(f"exploracao-{base}.png")
    b = linha([FOTOS / f"comportamento-{v}-reduzido-entrada.png" for v in VERSOES], [f"movimento reduzido · {VERSOES[v]}" for v in VERSOES])
    if b:
        b.save(SAIDA / "comportamentos.png"); feitas.append("comportamentos.png")
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
