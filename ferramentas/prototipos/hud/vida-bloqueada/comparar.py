"""Monta as folhas do protótipo da vida bloqueada (fotografar.mjs) em tamanho real (1×), em capturas/comparacoes/:
  estados.png    o topo nos três estados (sem penalidade; no limite; abaixo do limite) e depois de vestir a peça;
  mudancas.png   o topo antes e depois de tratar na Curandeira e de vestir a peça com +vida máxima;
  luta.png       a tela da luta (a carta do herói) antes e depois de uma rodada em que o herói apanha;
  telas.png      a tela inteira no limite (1280×720 e 1500×950) e abaixo do limite com a dica aberta.

    python ferramentas/prototipos/hud/vida-bloqueada/comparar.py
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
from comparar_comandos import em_colunas, em_linhas  # noqa: E402

FOTOS = AQUI / "capturas"
SAIDA = FOTOS / "comparacoes"


def linha(arquivos_titulos):
    fotos = [(FOTOS / f, t) for f, t in arquivos_titulos if (FOTOS / f).exists()]
    return em_colunas([f for f, _ in fotos], [t for _, t in fotos]) if fotos else None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    feitas = []
    folhas = {
        "estados.png": [[("saudavel-topo.png", "sem penalidade: 146/146 (a barra de sempre)")],
                        [("limite-topo.png", "no limite: 104 de vida, limite 104, saudável 146 (corte, queimadura e fome: −42)")],
                        [("abaixo-topo.png", "abaixo do limite: 62 de vida (42 recuperáveis, 42 bloqueados)")],
                        [("equipar-depois-topo.png", "depois de vestir a peça com +vida máxima: saudável 171, limite 154")]],
        "mudancas.png": [[("curandeira-antes-topo.png", "Curandeira, antes: 91 de vida, limite 131 (corte −15)"),
                          ("curandeira-depois-topo.png", "depois de tratar o corte: o motor devolve os 15 (106/146)")],
                         [("equipar-antes-1280x720.png", "a peça oferecida no achado (antes de vestir)"),
                          ("equipar-depois-topo.png", "vestida: 91/171, bloqueio −17")]],
        "luta.png": [[("luta-antes-1280x720.png", "na luta, 1280×720: a carta do herói (62 de vida, limite 104, saudável 146)"),
                      ("luta-depois-1280x720.png", "depois da rodada: 46 (só desce; o bloqueio fica)")]],
        "telas.png": [[("limite-1280x720.png", "no limite, 1280×720"), ("limite-1500x950.png", "no limite, 1500×950")],
                      [("abaixo-dica-1280x720.png", "abaixo do limite, a dica da vida aberta")]],
    }
    for nome, linhas in folhas.items():
        if em_linhas([linha(x) for x in linhas], SAIDA / nome):
            feitas.append(nome)
    print("\n".join(feitas))


if __name__ == "__main__":
    main()
