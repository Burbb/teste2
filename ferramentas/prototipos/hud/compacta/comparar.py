"""Monta as comparações da composição compacta (fotografar.mjs) em tamanho real (1×), em capturas/comparacoes/: as telas
inteiras da produção e das duas alternativas lado a lado, com os mesmos dados, em cada momento:
  <janela>-<luta>-habilidades.png   Habilidades aberto, o mouse na habilidade de descrição mais longa;
  <janela>-<luta>-itens.png         Itens aberto (alternou de Habilidades);
  <janela>-<luta>-mira.png          a mira (o lembrete e o Voltar);
  <janela>-<luta>-efeitos.png       SIMULADO: três ou quatro efeitos em cada combatente, com Habilidades aberto.
Em 1920×1080 só o primeiro momento (as telas são largas). O teclado (a luta maior, 1280×720) em teclado.png.

    python ferramentas/prototipos/hud/compacta/comparar.py [pasta]   (padrão: capturas/)
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else AQUI / "capturas"
SAIDA = FOTOS / "comparacoes"
VERSOES = {"producao": "PRODUÇÃO (1.113.0)", "a": "A · arena compacta", "b": "B · seletor na ficha"}
MOMENTOS = {"habilidades": ("2-habilidades-longa", "Habilidades, a descrição mais longa"), "itens": ("4-itens", "Itens"),
            "mira": ("5-mira", "a mira"), "efeitos": ("7-efeitos-simulados-habilidades", "SIMULADO: 3 ou 4 efeitos em cada um, Habilidades aberto")}
LUTAS = {"poucos": "poucos (2 aliados, 3 inimigos)", "cinco": "5 lobos, 4 aliados", "maior": "o maior real: 6 × 6",
         "longos": "nomes longos (4 esqueletos)"}


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = []
    for jan in ("baixa", "normal", "grande"):
        for luta, rot in LUTAS.items():
            for chave, (arq, titulo) in MOMENTOS.items():
                if jan == "grande" and chave != "habilidades":
                    continue
                fotos = [(FOTOS / f"{jan}-{luta}-{v}-{arq}.png", f"{jan} · {rot} · {titulo} · {nome}") for v, nome in VERSOES.items()]
                fotos = [(f, t) for f, t in fotos if f.exists()]
                if not fotos:
                    continue
                img = em_colunas([f for f, _ in fotos], [t for _, t in fotos])
                img.save(SAIDA / f"{jan}-{luta}-{chave}.png")
                feitas.append(f"{jan}-{luta}-{chave}.png")
    tec = [(FOTOS / f"teclado-{v}.png", f"teclado e movimento reduzido · {nome}") for v, nome in VERSOES.items()]
    tec = [(f, t) for f, t in tec if f.exists()]
    if tec and em_linhas([em_colunas([f for f, _ in tec], [t for _, t in tec])], SAIDA / "teclado.png"):
        feitas.append("teclado.png")
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
