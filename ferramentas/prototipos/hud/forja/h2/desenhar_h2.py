"""Gera a primeira versão da fonte em camadas da forja H2: aseprite/forja-h2.aseprite (320×96; as camadas fundo, fogo,
bigorna, espada, ferreiro e frente; um quadro por estado do ferreiro, com a tag do nome). Depois de gerada, a fonte é
o .aseprite: os retoques se fazem nele e o exportar_h2.py tira dele as tiras do jogo. Por isso este script não
sobrescreve uma fonte que já existe (um retoque se perderia), a menos que se peça --refazer.

    python ferramentas/prototipos/hud/forja/f/desenhar_h2.py [--refazer]
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[4] / "ferramentas" / "arte"))

import ambiente_h2 as A  # noqa: E402
import ferreiro_h2 as F  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "forja-h2.aseprite"
CAMADAS = ["fundo", "fogo", "bigorna", "espada", "ferreiro", "frente"]
# os estados do ferreiro (um quadro cada): as poses do ciclo e a pausa com a espada virada
ESTADOS = ["repouso", "sobe1", "sobe2", "alto", "desce", "golpe", "volta", "ajuste", "ajuste_virada"]


def camadas_do_estado(i, estado, paradas):
    pose = "ajuste" if estado == "ajuste_virada" else estado
    fogo = A.Tela(A.QW, A.QH)
    A.fogo(fogo, i % 4)
    espada = A.Tela(A.QW, A.QH)
    A.espada(espada, F.CONTATO[0], pose in ("golpe", "volta"), estado == "ajuste_virada")
    return {"fundo": paradas["fundo"], "fogo": fogo, "bigorna": paradas["bigorna"], "espada": espada,
            "ferreiro": F.figura(pose, virada=estado == "ajuste_virada"), "frente": paradas["frente"]}


def main():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    fundo = A.desenhar_fundo()
    paradas = {"fundo": fundo, "bigorna": A.bigorna(), "frente": A.frente()}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for i, e in enumerate(ESTADOS):
            for nome, t in camadas_do_estado(i, e, paradas).items():
                t.imagem().save(tmp / f"{nome}-{i}.png")
        script = tmp / "montar_forja.lua"
        shutil.copy(AQUI / "aseprite" / "montar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pasta={tmp}", "--script-param", f"camadas={','.join(CAMADAS)}",
                            "--script-param", f"estados={','.join(ESTADOS)}", "--script-param", f"saida={FONTE}",
                            "--script", str(script)], capture_output=True, text=True)
        if not FONTE.exists() or "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(FONTE.name, r.stdout.strip())


if __name__ == "__main__":
    main()
