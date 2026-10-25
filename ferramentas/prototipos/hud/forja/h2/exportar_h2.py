"""Exporta da fonte (aseprite/forja-h2.aseprite) as camadas que o jogo lê, em camadas/: fundo.png, bigorna.png e
frente.png (320×96), e as tiras fogo.png (os 4 quadros do fogo), espada.png e ferreiro.png (um quadro de 320×96 por
estado, na ordem de desenhar_h2.ESTADOS). Lê o .aseprite como está, com os retoques.

    python ferramentas/prototipos/hud/forja/h2/exportar_h2.py [--conferir] [--jogo]

--jogo: copia as camadas exportadas para o jogo (rpg/web/static/cenas/forja/, lidas por telas/cena-forja.js desde a
1.210.0). A arte do jogo sai sempre daqui, da fonte; não se edita a cópia.

--conferir: monta os 53 quadros do ciclo com as tiras exportadas (como forja-h2.js monta) e compara com cena_h2.quadro,
o desenho em código; só vale enquanto a fonte não foi retocada (depois de um retoque, as diferenças são o retoque).
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parents[4] / "ferramentas" / "arte"))

from desenhar_h2 import ESTADOS, FONTE  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

SAIDA = AQUI / "camadas"
TIRAS = {"fogo": 4, "espada": len(ESTADOS), "ferreiro": len(ESTADOS)}


def exportar():
    SAIDA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "exportar_forja.lua"
        shutil.copy(AQUI / "aseprite" / "exportar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                            "--script", str(script)], capture_output=True, text=True)
        if "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não exportou:\n{r.stdout}{r.stderr}")
        for nome in ("fundo", "bigorna", "frente"):
            Image.open(tmp / f"{nome}-0.png").convert("RGBA").save(SAIDA / f"{nome}.png", optimize=True)
        for nome, n in TIRAS.items():
            tira = Image.new("RGBA", (320 * n, 96))
            for i in range(n):
                tira.paste(Image.open(tmp / f"{nome}-{i}.png").convert("RGBA"), (320 * i, 0))
            tira.save(SAIDA / f"{nome}.png", optimize=True)
    print("camadas:", ", ".join(sorted(p.name for p in SAIDA.glob("*.png"))))


def estado_de(p):
    """O estado (o quadro das tiras) da pose: a pausa com a espada virada é um estado próprio."""
    if p["nome"] == "ajuste" and 1 <= p["t"] < 5:
        return ESTADOS.index("ajuste_virada")
    return ESTADOS.index(p["nome"])


def montar(q, im):
    """O quadro q com as tiras exportadas, na ordem de forja-h2.js (sem as faíscas, que o jogo desenha em código)."""
    import cena_h2 as C
    p = C.pose_de(q)
    e = estado_de(p)
    c = im["fundo"].copy()
    for nome, i in (("fogo", (q // 2) % 4), ("bigorna", None), ("espada", e), ("ferreiro", e), ("frente", None)):
        camada = im[nome] if i is None else im[nome].crop((320 * i, 0, 320 * i + 320, 96))
        c.alpha_composite(camada)
    return c


def conferir():
    import cena_h2 as C
    im = {n: Image.open(SAIDA / f"{n}.png").convert("RGBA") for n in ("fundo", "bigorna", "frente", *TIRAS)}
    dif = 0
    for q in range(C.DURACAO):
        a = montar(q, im)
        # as faíscas o jogo desenha em código: a comparação é sem elas
        if a.tobytes() != C.quadro(q, com_faiscas=False).imagem().tobytes():
            dif += 1
    print(f"conferido: {C.DURACAO - dif} de {C.DURACAO} quadros iguais ao desenho em código")
    return dif == 0


JOGO = AQUI.parents[4] / "rpg" / "web" / "static" / "cenas" / "forja"


if __name__ == "__main__":
    exportar()
    if "--jogo" in sys.argv:
        JOGO.mkdir(parents=True, exist_ok=True)
        for arq in sorted(SAIDA.glob("*.png")):
            shutil.copy(arq, JOGO / arq.name)
        print("no jogo:", JOGO)
    if "--conferir" in sys.argv:
        sys.exit(0 if conferir() else 1)
