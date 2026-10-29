"""A fonte em camadas da B2 (os dois jogadores refinados na grade 132×84) e a camada da prova.

    python ferramentas/prototipos/taverna/prova/b2/fonte.py --criar [--refazer]   # gera a fonte a partir do desenho.py
    python ferramentas/prototipos/taverna/prova/b2/fonte.py [--conferir]           # exporta da fonte

A fonte é `aseprite/b2.aseprite` (132×84, um quadro): as camadas guia, bancos, mesa, verde e ocre, de baixo para cima.
A guia é a referência "Jogo de tabuleiro na taverna" posta na grade (alinhada pela mesa: o centro do tampo em x 61,
y 40, 13 pixels da referência por pixel da grade), oculta e meio transparente: orienta o desenho e nunca é exportada.
Depois de criada, a fonte é a autoridade: os retoques se fazem nela, e `--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está e compõe as camadas visíveis, menos a guia, em `camadas/prova/b2.png` (com o piso da
vista isolada, `chao-b2.png`, o mesmo da B). `--conferir` compara a exportação com o que o desenho.py desenha; depois
de um retoque na fonte, as diferenças são o retoque."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI.parents[1]))
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))

from prova.b2 import desenho as B  # noqa: E402
from prova import conjunto as C  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "b2.aseprite"
REFERENCIA = RAIZ / "ferramentas" / "arte" / "referencias" / "cenarios internos" / "Jogo de tabuleiro na taverna.png"
SAIDA = pathlib.Path(C.CAMADAS)
GUIA = (13.0, (790, 490), (61, 40))      # pixels da referência por pixel da grade; o centro do tampo nas duas


def guia():
    """A referência na grade da B2 (só para orientar o desenho; a média de cada bloco, não um resultado)."""
    e, (cx, cy), (gx, gy) = GUIA
    x0, y0 = cx - gx * e, cy - gy * e
    im = Image.open(REFERENCIA).convert("RGBA")
    return im.crop((round(x0), round(y0), round(x0 + B.W * e), round(y0 + B.H * e))).resize((B.W, B.H), Image.BOX)


def criar():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    FONTE.parent.mkdir(exist_ok=True)
    camadas = {"guia": guia(), **{n: t.imagem() for n, t in B.camadas().items()}}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for nome, im in camadas.items():
            im.save(tmp / f"{nome}.png")
        script = tmp / "montar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
        shutil.copy(AQUI / "aseprite" / "montar.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pasta={tmp}", "--script-param",
                            f"camadas={','.join(camadas)}", "--script-param", f"largura={B.W}", "--script-param",
                            f"altura={B.H}", "--script-param", f"saida={FONTE}", "--script", str(script)],
                           capture_output=True, text=True)
        if not FONTE.exists() or "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
    print(FONTE.name, "camadas:", ", ".join(camadas), "(a guia oculta)")


def exportar():
    """O conjunto lido da fonte (com os retoques), sem a guia nem as camadas ocultas."""
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "exportar.lua"
        shutil.copy(AQUI / "aseprite" / "exportar.lua", script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                            "--script", str(script)], capture_output=True, text=True)
        lidas = [ln.split()[1:] for ln in r.stdout.splitlines() if ln.startswith("camada ")]
        if not lidas:
            sys.exit(f"O Aseprite não exportou:\n{r.stdout}{r.stderr}")
        im = Image.new("RGBA", (B.W, B.H))
        usadas = []
        for nome, visivel in lidas:
            if nome == "guia" or visivel != "1":
                continue
            im.alpha_composite(Image.open(tmp / f"{nome}.png").convert("RGBA"))
            usadas.append(nome)
    SAIDA.mkdir(parents=True, exist_ok=True)
    im.save(SAIDA / "b2.png", optimize=True)
    C.conjunto(2, com_chao=True).imagem().save(SAIDA / "chao-b2.png")
    print("b2.png de", ", ".join(usadas))
    return im


def conferir(im):
    """A exportação (da fonte) contra o desenho.py, pixel a pixel."""
    cod = B.composto().imagem().convert("RGBA")
    a, b = im.tobytes(), cod.tobytes()
    dif = sum(a[i:i + 4] != b[i:i + 4] for i in range(0, len(a), 4))
    print(f"conferido: {dif} pixels diferentes do desenho.py" + (" (os retoques da fonte)" if dif else ""))
    return dif


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    im = exportar()
    if "--conferir" in sys.argv:
        conferir(im)
