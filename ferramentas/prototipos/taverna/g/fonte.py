"""A fonte em camadas da candidata G (o balcão de perto) e as camadas que a demonstração lê, como no templo.

    python ferramentas/prototipos/taverna/g/fonte.py --criar [--refazer]   # gera a fonte a partir do código
    python ferramentas/prototipos/taverna/g/fonte.py [--conferir]           # exporta da fonte para camadas/g

A fonte é `g/aseprite/taverna-g.aseprite` (320×96, 4 quadros): as camadas fundo, fogo, lampiao, caldeirao, taverneiro
e frente, de baixo para cima. O fogo e o lampião usam os 4 quadros; as outras, só o primeiro. Depois de criada, ela é a
autoridade: os retoques se fazem nela, e `--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está e grava em `camadas/g/` o que `tela/cena-taverna-b.js` lê (`estatica("g")`):
- `fundo.png`: o primeiro quadro de fundo, caldeirao, taverneiro e frente, um por cima do outro (e `fundo-sem-morel.png`,
  a mesma imagem: Morel não aparece nesta vista);
- `fogo.png` e `velas.png`: as tiras de 4 quadros das chamas da lareira e do lampião, cortadas onde uma camada de cima
  (o caldeirão, o taverneiro, a frente) as cobre.
`--conferir` compara o que saiu da fonte com o desenho do código, pixel a pixel; depois de um retoque na fonte, as
diferenças são o retoque. Os scripts do Aseprite são os da forja (320×96)."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(AQUI.parent))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from g import desenho as D, taverneiro as T  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "taverna-g.aseprite"
LUA = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite"
CAMADAS = ["fundo", "fogo", "lampiao", "caldeirao", "taverneiro", "frente"]
SAIDA = AQUI.parent / "camadas" / "g"


def quadros_do_codigo():
    """{camada: [imagem, ...]}: o que o código da G desenha, quadro a quadro."""
    return {"fundo": [D.fundo().imagem()], "fogo": [D.fogo(i).imagem() for i in range(4)],
            "lampiao": [D.lampiao_chama(i).imagem() for i in range(4)], "caldeirao": [D.camada_caldeirao().imagem()],
            "taverneiro": [T.camada().imagem()], "frente": [D.frente().imagem()]}


def criar():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    FONTE.parent.mkdir(exist_ok=True)
    q = quadros_do_codigo()
    n = max(len(v) for v in q.values())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for nome, ims in q.items():
            for i, im in enumerate(ims):
                im.save(tmp / f"{nome}-{i}.png")
        script = tmp / "montar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
        shutil.copy(LUA / "montar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pasta={tmp}", "--script-param",
                            f"camadas={','.join(CAMADAS)}", "--script-param",
                            f"estados={','.join(f'q{i:02d}' for i in range(n))}", "--script-param", f"saida={FONTE}",
                            "--script", str(script)], capture_output=True, text=True)
        if not FONTE.exists() or "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
        print(FONTE.name, "celulas", r.stdout.split("celulas")[-1].split()[0])


def ler_fonte():
    """{camada: [imagem, ...]}: as células da fonte, como estão (os retoques inclusive)."""
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "exportar.lua"
        shutil.copy(LUA / "exportar_forja.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                            "--script", str(script)], capture_output=True, text=True)
        if "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não exportou:\n{r.stdout}{r.stderr}")
        q = {}
        for nome in CAMADAS:
            arqs = sorted((p for p in tmp.glob(f"{nome}-*.png") if p.stem.rsplit("-", 1)[0] == nome),
                          key=lambda p: int(p.stem.rsplit("-", 1)[1]))
            q[nome] = [Image.open(a).convert("RGBA") for a in arqs]
            for im in q[nome]:
                im.load()
        return q


def montar(q):
    """As imagens da demonstração: o fundo composto e as tiras das chamas, cortadas pelo que fica na frente delas."""
    fundo = q["fundo"][0].copy()
    frente = Image.new("RGBA", fundo.size)
    for nome in ("caldeirao", "taverneiro", "frente"):
        frente.alpha_composite(q[nome][0])
    fundo.alpha_composite(frente)
    coberto = frente.getchannel("A").point(lambda a: 255 if a else 0)
    tiras = {}
    for nome, arq in (("fogo", "fogo"), ("lampiao", "velas")):
        tira = Image.new("RGBA", (D.QW * len(q[nome]), D.QH))
        for i, im in enumerate(q[nome]):
            livre = im.copy()
            livre.paste((0, 0, 0, 0), mask=coberto)
            tira.paste(livre, (D.QW * i, 0))
        tiras[arq] = tira
    return {"fundo": fundo, "fundo-sem-morel": fundo, **tiras}


def exportar():
    saida = montar(ler_fonte())
    SAIDA.mkdir(parents=True, exist_ok=True)
    for nome, im in saida.items():
        im.save(SAIDA / f"{nome}.png", optimize=True)
    print("camadas/g:", ", ".join(sorted(f"{n}.png" for n in saida)))
    return saida


def conferir(saida):
    """O que saiu da fonte contra o desenho do código, pixel a pixel."""
    codigo = montar(quadros_do_codigo())
    dif = [n for n in saida if saida[n].tobytes() != codigo[n].tobytes()]
    print(f"conferido: {len(saida) - len(dif)} de {len(saida)} imagens iguais ao código"
          + (f" (diferem: {', '.join(dif)}: os retoques da fonte)" if dif else ""))
    return not dif


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    s = exportar()
    if "--conferir" in sys.argv and not conferir(s):
        sys.exit(1)
