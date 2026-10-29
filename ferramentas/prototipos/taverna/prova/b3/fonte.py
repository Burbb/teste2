"""A fonte em camadas da B3 (a B2 com os ombros e os braços redesenhados) e a camada da prova.

    python ferramentas/prototipos/taverna/prova/b3/fonte.py --criar [--refazer]   # copia a fonte da B2 e retoca
    python ferramentas/prototipos/taverna/prova/b3/fonte.py [--conferir]           # exporta da fonte

A B2 fica como está, para comparar. `--criar` copia `../b2/aseprite/b2.aseprite` (com os retoques dela: as sombras de
contato do cotovelo e das botas) para `aseprite/b3.aseprite` e troca, só nas camadas verde e ocre, os pixels em que o
desenho.py da B3 difere do da B2 (os ombros, os braços e o tronco em volta deles); o resto de cada camada vem da fonte
da B2, pixel por pixel. A guia (a referência na grade, oculta) segue fora da exportação. Depois de criada, a fonte é a
autoridade: os retoques se fazem nela, e `--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está e compõe as camadas visíveis, menos a guia, em `camadas/prova/b3.png` (com o piso da
vista isolada, `chao-b3.png`, o mesmo da B). `--conferir` compara a exportação com a B2 exportada mais o retoque dos
braços: as diferenças são os retoques feitos depois na fonte da B3."""
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

from prova.b3 import desenho as B3  # noqa: E402
from prova import conjunto as C  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "b3.aseprite"
FONTE_B2 = AQUI.parent / "b2" / "aseprite" / "b2.aseprite"
EXPORTAR = AQUI.parent / "b2" / "aseprite" / "exportar.lua"
TROCAR = RAIZ / "ferramentas" / "prototipos" / "hud" / "forja" / "h2" / "aseprite" / "trocar_camada.lua"
SAIDA = pathlib.Path(C.CAMADAS)


def ler(fonte):
    """[(nome, visível, Image)] das camadas da fonte, de baixo para cima, como estão no arquivo."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "exportar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
        shutil.copy(EXPORTAR, script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={fonte}", "--script-param", f"pasta={tmp}",
                            "--script", str(script)], capture_output=True, text=True)
        lidas = [ln.split()[1:] for ln in r.stdout.splitlines() if ln.startswith("camada ")]
        if not lidas:
            sys.exit(f"O Aseprite não leu {fonte.name}:\n{r.stdout}{r.stderr}")
        return [(n, v == "1", Image.open(tmp / f"{n}.png").convert("RGBA").copy()) for n, v in lidas]


def retoque():
    """{camada: Image}: a camada da fonte da B2 com os pixels em que a B3 difere do desenho da B2."""
    da_b2 = {n: im for n, _, im in ler(FONTE_B2)}
    r = {}
    for nome, (velho, novo) in B3.camadas().items():
        a, b, im = velho.imagem().convert("RGBA"), novo.imagem().convert("RGBA"), da_b2[nome].copy()
        n = 0
        for y in range(B3.H):
            for x in range(B3.W):
                if a.getpixel((x, y)) != b.getpixel((x, y)):
                    im.putpixel((x, y), b.getpixel((x, y)))
                    n += 1
        r[nome] = im
        print(f"{nome}: {n} pixels retocados")
    return r


def criar():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    FONTE.parent.mkdir(exist_ok=True)
    camadas = retoque()
    shutil.copy(FONTE_B2, FONTE)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "trocar.lua"
        shutil.copy(TROCAR, script)
        for nome, im in camadas.items():
            im.save(tmp / f"{nome}-0.png")
            r = subprocess.run([aseprite(), "-b", "--script-param", f"fonte={FONTE}", "--script-param", f"pasta={tmp}",
                                "--script-param", f"camada={nome}", "--script", str(script)],
                               capture_output=True, text=True)
            if "celulas 1" not in r.stdout:
                sys.exit(f"O Aseprite não trocou a camada {nome}:\n{r.stdout}{r.stderr}")
    lidas = {n: im for n, _, im in ler(FONTE)}                      # confere o que salvou
    for nome, im in camadas.items():
        assert lidas[nome].tobytes() == im.tobytes(), f"a camada {nome} não saiu como o retoque"
    print(FONTE.name, "criada da B2, com o retoque nas camadas", ", ".join(camadas))


def compor(camadas):
    im = Image.new("RGBA", (B3.W, B3.H))
    for nome, visivel, c in camadas:
        if nome != "guia" and visivel:
            im.alpha_composite(c)
    return im


def exportar():
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    camadas = ler(FONTE)
    im = compor(camadas)
    SAIDA.mkdir(parents=True, exist_ok=True)
    im.save(SAIDA / "b3.png", optimize=True)
    C.conjunto(2, com_chao=True).imagem().save(SAIDA / "chao-b3.png")
    print("b3.png de", ", ".join(n for n, v, _ in camadas if n != "guia" and v))
    return im


def conferir(im):
    """A exportação contra a B2 da fonte com o retoque dos braços."""
    ret = retoque()
    esperado = compor([(n, v, ret.get(n, c)) for n, v, c in ler(FONTE_B2)])
    a, b = im.tobytes(), esperado.tobytes()
    dif = sum(a[i:i + 4] != b[i:i + 4] for i in range(0, len(a), 4))
    print(f"conferido: {dif} pixels diferentes da B2 com o retoque dos braços" + (" (retoques feitos na fonte)" if dif else ""))
    return dif


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    im = exportar()
    if "--conferir" in sys.argv:
        conferir(im)
