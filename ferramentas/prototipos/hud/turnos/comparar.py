"""Monta as folhas do protótipo da etapa 1C (fotografar.mjs) em tamanho real (1×), em capturas/comparacoes/: a produção
e a proposta lado a lado, com os mesmos dados, em cada momento.
  iniciativa.png   o turno 1 com a sua iniciativa; a vez (a iniciativa à vista); o golpe que a usa; o turno 2
  emboscada.png    a emboscada deles (o lobo mais rápido antes do turno 1) e o turno 1
  cheia.png        a luta cheia: a iniciativa que passa (Meditar no turno livre); o turno 3 com a Maldição em todos
  janelas.png      a proposta em 1500×950 (a luta pequena e a cheia) e com movimento reduzido

    python ferramentas/prototipos/hud/turnos/comparar.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = AQUI / "capturas"
SAIDA = FOTOS / "comparacoes"


def par(caso, momento, titulo):
    fotos = [(FOTOS / f"{caso.format(v=v)}-{momento}.png", f"{titulo} · {nome}") for v, nome in (("producao", "produção"), ("proposta", "proposta"))]
    fotos = [(f, t) for f, t in fotos if f.exists()]
    return em_colunas([f for f, _ in fotos], [t for _, t in fotos]) if fotos else None


def so(arquivos):
    fotos = [(FOTOS / f, t) for f, t in arquivos if (FOTOS / f).exists()]
    return em_colunas([f for f, _ in fotos], [t for _, t in fotos]) if fotos else None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    folhas = {
        "iniciativa.png": [par("iniciativa-{v}-1280x720", "1-turno1", "1280×720 · o turno 1, com a sua iniciativa (250 ms depois da mensagem)"),
                           par("iniciativa-{v}-1280x720", "2-iniciativa-disponivel", "a sua vez, a iniciativa ainda à mão"),
                           par("iniciativa-{v}-1280x720", "5-golpe", "o ataque que usa a iniciativa (+25%)"),
                           par("iniciativa-{v}-1280x720", "6-turno2", "o turno 2")],
        "emboscada.png": [par("emboscada-{v}-1280x720", "1-emboscada", "1280×720 · a emboscada deles: o lobo mais rápido ataca antes do turno 1"),
                          par("emboscada-{v}-1280x720", "2-turno1", "o turno 1")],
        "cheia.png": [par("cheia-{v}-1280x720", "2-iniciativa-passou", "1280×720 · luta cheia: o turno livre gasto em Meditar (a iniciativa passa)"),
                      par("cheia-{v}-1280x720", "3-turno3-efeitos", "o turno 3, com a Maldição em todos os inimigos"),
                      par("cheia-{v}-1280x720", "5-habilidades", "Habilidades aberto no turno 3")],
        "janelas.png": [so([("iniciativa-proposta-1500x950-1-turno1.png", "proposta · 1500×950 · o turno 1 com a iniciativa"),
                            ("cheia-proposta-1500x950-3-turno3-efeitos.png", "proposta · 1500×950 · luta cheia, o turno 3")]),
                        so([("iniciativa-proposta-1280x720-reduzido-1-turno1.png", "proposta · movimento reduzido · o turno 1"),
                            ("iniciativa-proposta-1280x720-reduzido-2-iniciativa-disponivel.png", "movimento reduzido · a vez, a placa com a iniciativa")])],
    }
    feitas = [nome for nome, linhas in folhas.items() if em_linhas(linhas, SAIDA / nome)]
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
