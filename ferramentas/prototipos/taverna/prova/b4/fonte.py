"""A fonte em camadas da B4 (a B3 com o ombro de cá do de verde suavizado) e a camada da prova.

    python ferramentas/prototipos/taverna/prova/b4/fonte.py --criar [--refazer]   # copia a fonte da B3 e retoca
    python ferramentas/prototipos/taverna/prova/b4/fonte.py [--conferir]           # exporta da fonte

A B3 fica como está, para comparar. `--criar` copia `../b3/aseprite/b3.aseprite` para `aseprite/b4.aseprite` e troca, só
na camada verde, os pixels em que o desenho.py da B4 difere do da B3 (o ombro, a manga e a borda do peito do braço de
cá); o resto vem da fonte da B3, pixel por pixel (com os retoques da B2 e da B3). A guia segue oculta e fora da
exportação. Depois de criada, a fonte é a autoridade: `--criar` não a sobrescreve sem `--refazer`.

Exportar compõe as camadas visíveis, menos a guia, em `camadas/prova/b4.png` (com `chao-b4.png`, o piso da B).
`--conferir` compara a exportação com a B3 da fonte mais o retoque: as diferenças são retoques feitos depois na fonte."""
import pathlib
import shutil
import subprocess
import sys
import tempfile

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1]))

from prova.b4 import desenho as B4  # noqa: E402
from prova.b3.fonte import TROCAR, aseprite, compor, ler  # noqa: E402
from prova import conjunto as C  # noqa: E402

FONTE = AQUI / "aseprite" / "b4.aseprite"
FONTE_B3 = AQUI.parent / "b3" / "aseprite" / "b3.aseprite"
SAIDA = pathlib.Path(C.CAMADAS)


def retoque():
    """{camada: Image}: a camada da fonte da B3 com os pixels em que a B4 difere do desenho da B3."""
    da_b3 = {n: im for n, _, im in ler(FONTE_B3)}
    r = {}
    for nome, (velho, novo) in B4.camadas().items():
        a, b, im = velho.imagem().convert("RGBA"), novo.imagem().convert("RGBA"), da_b3[nome].copy()
        n = 0
        for y in range(B4.H):
            for x in range(B4.W):
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
    shutil.copy(FONTE_B3, FONTE)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        script = tmp / "trocar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
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
    print(FONTE.name, "criada da B3, com o retoque na camada", ", ".join(camadas))


def exportar():
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    camadas = ler(FONTE)
    im = compor(camadas)
    SAIDA.mkdir(parents=True, exist_ok=True)
    im.save(SAIDA / "b4.png", optimize=True)
    C.conjunto(2, com_chao=True).imagem().save(SAIDA / "chao-b4.png")
    print("b4.png de", ", ".join(n for n, v, _ in camadas if n != "guia" and v))
    return im


def conferir(im):
    """A exportação contra a B3 da fonte com o retoque do ombro."""
    ret = retoque()
    esperado = compor([(n, v, ret.get(n, c)) for n, v, c in ler(FONTE_B3)])
    a, b = im.tobytes(), esperado.tobytes()
    dif = sum(a[i:i + 4] != b[i:i + 4] for i in range(0, len(a), 4))
    print(f"conferido: {dif} pixels diferentes da B3 com o retoque do ombro" + (" (retoques feitos na fonte)" if dif else ""))
    return dif


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    im = exportar()
    if "--conferir" in sys.argv:
        conferir(im)
