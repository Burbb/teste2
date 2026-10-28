"""Consolida na fonte editável o gesto do ferreiro aprovado pelo Jean (28/10/2026): a variante "Corpo desce" da
candidata (candidata_gesto.py), com a cabeça do martelo desenhada à mão no contato, a nuca e o calcanhar da bigorna.
Troca só a camada "ferreiro" de aseprite/forja-h2.aseprite (um quadro por estado, na ordem de desenhar_h2.ESTADOS);
o fundo, o fogo, a bigorna, a espada, a frente, as tags e as durações não mudam. Depois, a fonte é a autoridade:
exportar_h2.py lê dela, e nenhum script de desenho em código a sobrescreve (desenhar_h2.py recusa sem --refazer, e o
--refazer agora exige --sem-os-retoques, porque apagaria o gesto aprovado).

Só roda uma vez: se a camada já é a candidata, não faz nada; se ela não é nem a do código antigo nem a candidata (um
retoque à mão no Aseprite), recusa sem --forcar.

    python ferramentas/prototipos/hud/forja/h2/consolidar_gesto.py [--forcar]
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[3] / "arte"))

from desenhar_h2 import ESTADOS, FONTE  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

CANDIDATA = AQUI / "candidata-gesto" / "ferreiro.png"


def camada_da_fonte(tmp):
    """A camada ferreiro como está na fonte: a tira de 9 quadros."""
    script = tmp / "exportar_forja.lua"
    shutil.copy(AQUI / "aseprite" / "exportar_forja.lua", script)
    subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                    "--script", str(script)], capture_output=True, text=True, check=True)
    tira = Image.new("RGBA", (320 * len(ESTADOS), 96))
    for i in range(len(ESTADOS)):
        arq = tmp / f"ferreiro-{i}.png"
        if arq.exists():
            tira.paste(Image.open(arq).convert("RGBA"), (320 * i, 0))
    return tira


def igual(a, b):
    return ImageChops.difference(a.convert("RGBA"), b.convert("RGBA")).getbbox() is None


def main():
    nova = Image.open(CANDIDATA).convert("RGBA")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        hoje = camada_da_fonte(tmp)
        if igual(hoje, nova):
            print("A fonte já tem o gesto aprovado: nada a fazer.")
            return
        codigo = Image.open(AQUI / "camadas" / "ferreiro.png").convert("RGBA")  # a exportação de antes (o código antigo)
        if not igual(hoje, codigo) and "--forcar" not in sys.argv:
            sys.exit("A camada ferreiro da fonte tem retoques que não são nem o código antigo nem a candidata: use --forcar.")
        for i in range(len(ESTADOS)):
            nova.crop((320 * i, 0, 320 * i + 320, 96)).save(tmp / f"ferreiro-{i}.png")
        script = tmp / "trocar_camada.lua"
        shutil.copy(AQUI / "aseprite" / "trocar_camada.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                            "--script-param", "camada=ferreiro", "--script", str(script)], capture_output=True, text=True)
        if f"celulas {len(ESTADOS)}" not in r.stdout:
            sys.exit(f"O Aseprite não trocou a camada:\n{r.stdout}{r.stderr}")
    with tempfile.TemporaryDirectory() as tmp:
        if not igual(camada_da_fonte(pathlib.Path(tmp)), nova):
            sys.exit("A camada salva não confere com a candidata.")
    print(FONTE.name, "com o gesto aprovado (9 quadros conferidos).")


if __name__ == "__main__":
    main()
