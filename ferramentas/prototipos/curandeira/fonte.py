"""A fonte em camadas da curandeira aprovada (28/10/2026) e as camadas do jogo, como na forja (hud/forja/h2).

    python ferramentas/prototipos/curandeira/fonte.py --criar [--refazer]   # gera a fonte a partir do código
    python ferramentas/prototipos/curandeira/fonte.py [--conferir] [--jogo]  # exporta da fonte

A fonte é `aseprite/curandeira.aseprite` (320×96): as camadas fundo, fogo, baldes, vapor, vapor-forte, pita, marta e
frente, de baixo para cima; cada quadro da fonte é um quadro das tiras (o fogo e os vapores usam os 4 primeiros; pita e
marta, um por desenho da rotina, na ordem de `figuras.quadros`; fundo, baldes e frente, só o primeiro). Depois de
criada, ela é a autoridade: os retoques se fazem nela, e `--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está e monta as tiras em `final/` (com o `rotina.json`, a linha do tempo que sai de
figuras.py). `--conferir` compara `final/` com `camadas/` (a candidata aprovada, exportada do código) pixel a pixel;
depois de um retoque na fonte, as diferenças são o retoque. `--jogo` copia `final/` para rpg/web/static/cenas/curandeira
(lidas por telas/cena-curandeira.js). A arte do jogo sai sempre daqui; não se edita a cópia.

Os scripts do Aseprite são os da forja (montar_forja.lua, exportar_forja.lua: genéricos para 320×96)."""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

import desenho as D  # noqa: E402
import figuras as F  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "curandeira.aseprite"
LUA = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite"
CAMADAS = ["fundo", "fogo", "baldes", "vapor", "vapor-forte", "pita", "marta", "frente"]
FINAL = AQUI / "final"
JOGO = RAIZ / "rpg" / "web" / "static" / "cenas" / "curandeira"


def quadros_do_codigo():
    """{camada: [Tela, ...]}: o que o código desenha, quadro a quadro."""
    return {"fundo": [D.fundo()], "fogo": [D.fogo(i) for i in range(4)], "baldes": [D.baldes()],
            "vapor": [D.vapor(i) for i in range(4)], "vapor-forte": [D.vapor(i, forte=True) for i in range(4)],
            "pita": F.todas("pita"), "marta": F.todas("marta"), "frente": [D.frente()]}


def criar():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    FONTE.parent.mkdir(exist_ok=True)
    q = quadros_do_codigo()
    n = max(len(v) for v in q.values())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for nome, telas in q.items():
            for i, t in enumerate(telas):
                t.imagem().save(tmp / f"{nome}-{i}.png")
        script = tmp / "montar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
        shutil.copy(LUA / "montar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pasta={tmp}", "--script-param",
                            f"camadas={','.join(CAMADAS)}", "--script-param",
                            f"estados={','.join(f'q{i:02d}' for i in range(n))}", "--script-param", f"saida={FONTE}",
                            "--script", str(script)], capture_output=True, text=True)
        if not FONTE.exists() or "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(FONTE.name, r.stdout.strip())


def exportar():
    """As tiras do jogo, lidas da fonte (com os retoques), em final/."""
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    FINAL.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "exportar.lua"
        shutil.copy(LUA / "exportar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                            "--script", str(script)], capture_output=True, text=True)
        if "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não exportou:\n{r.stdout}{r.stderr}")
        for nome in CAMADAS:
            # o nome exato e o número (vapor-*.png também pegaria os quadros de vapor-forte)
            arqs = sorted((p for p in tmp.glob(f"{nome}-*.png") if p.stem.rsplit("-", 1)[0] == nome),
                          key=lambda p: int(p.stem.rsplit("-", 1)[1]))
            if len(arqs) == 1:
                Image.open(arqs[0]).convert("RGBA").save(FINAL / f"{nome}.png", optimize=True)
                continue
            tira = Image.new("RGBA", (D.QW * len(arqs), D.QH))
            for i, a in enumerate(arqs):
                tira.paste(Image.open(a).convert("RGBA"), (D.QW * i, 0))
            tira.save(FINAL / f"{nome}.png", optimize=True)
    shutil.copy(AQUI / "camadas" / "rotina.json", FINAL / "rotina.json")
    print("final:", ", ".join(sorted(p.name for p in FINAL.iterdir())))


def conferir():
    """final/ (da fonte) contra camadas/ (a candidata aprovada, do código), pixel a pixel."""
    dif = []
    for nome in CAMADAS:
        a = Image.open(FINAL / f"{nome}.png").convert("RGBA")
        b = Image.open(AQUI / "camadas" / f"{nome}.png").convert("RGBA")
        if a.size != b.size or a.tobytes() != b.tobytes():
            dif.append(nome)
    iguais = (FINAL / "rotina.json").read_bytes() == (AQUI / "camadas" / "rotina.json").read_bytes()
    print(f"conferido: {len(CAMADAS) - len(dif)} de {len(CAMADAS)} camadas iguais à candidata"
          + (f" (diferem: {', '.join(dif)})" if dif else "") + ("; rotina igual" if iguais else "; ROTINA DIFERENTE"))
    return not dif and iguais


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    exportar()
    if "--conferir" in sys.argv and not conferir():
        sys.exit(1)
    if "--jogo" in sys.argv:
        JOGO.mkdir(parents=True, exist_ok=True)
        for arq in sorted(FINAL.iterdir()):
            shutil.copy(arq, JOGO / arq.name)
        print("no jogo:", os.path.relpath(JOGO, RAIZ))
