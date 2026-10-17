"""Monta as comparações da integração em tamanho real (1×), em capturas/comparacoes/:
  <momento>.png        o protótipo aprovado (../rodada2/capturas, versão "r", 5cb517d) ao lado do jogo integrado, com os
                       mesmos dados: o Arqueiro e o necromante em 1280×720 (Habilidades, Itens, a mira, os efeitos reais)
                       e o necromante em 1500×950 (os efeitos reais);
  janelas.png          o jogo: a mesma luta passando por 1500×950, 1280×720, 1050×720, 900×720 e de volta (a tela e o
                       seletor em cada tamanho);
  teclado.png          o jogo, movimento reduzido: as setas em 1280×720 e em 1050×720.
As fotos do protótipo vêm da última execução de ../rodada2/fotografar.mjs (não versionadas); sem elas, só o jogo.

    python ferramentas/prototipos/hud/compacta/integracao/comparar.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1]))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS, PROTO = AQUI / "capturas", AQUI.parent / "rodada2" / "capturas"
SAIDA = FOTOS / "comparacoes"
MOMENTOS = [("baixa-arqueiro", "2-habilidades", "Arqueiro, Habilidades (a descrição mais longa)"),
            ("baixa-maior", "3-itens", "necromante, Itens"),
            ("baixa-maior", "4-mira", "necromante, a mira"),
            ("baixa-arqueiro", "6-efeitos-reais-habilidades", "Arqueiro, efeitos reais, Habilidades"),
            ("baixa-maior", "6-efeitos-reais-habilidades", "necromante, efeitos reais, Habilidades"),
            ("normal-maior", "6-efeitos-reais-habilidades", "necromante 1500×950, efeitos reais, Habilidades")]


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = []
    for caso, momento, titulo in MOMENTOS:
        fotos = [(PROTO / f"{caso}-r-{momento}.png", f"{titulo} · protótipo aprovado (5cb517d)"),
                 (FOTOS / f"{caso}-jogo-{momento}.png", f"{titulo} · o jogo integrado")]
        fotos = [(f, t) for f, t in fotos if f.exists()]
        if fotos:
            nome = f"{caso}-{momento.split('-', 1)[1]}.png"
            em_colunas([f for f, _ in fotos], [t for _, t in fotos]).save(SAIDA / nome)
            feitas.append(nome)
    passos = sorted(FOTOS.glob("janelas-*-tela.png"), key=lambda f: int(f.stem.split("-")[2]))
    blocos = []
    for tela in passos:
        hab = tela.with_name(tela.name.replace("-tela", "-habilidades"))
        tam = tela.stem.split("-")[1]
        blocos.append(em_colunas([tela, hab], [f"{tam} · a luta parada (efeitos reais)", f"{tam} · Habilidades aberto"]))
    if em_linhas(blocos, SAIDA / "janelas.png"):
        feitas.append("janelas.png")
    tec = [f for f in (FOTOS / "teclado-1280x720-setas.png", FOTOS / "teclado-1050x720-setas.png") if f.exists()]
    if tec and em_linhas([em_colunas(tec, [f"{f.stem.split('-')[1]} · teclado e movimento reduzido" for f in tec])], SAIDA / "teclado.png"):
        feitas.append("teclado.png")
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
