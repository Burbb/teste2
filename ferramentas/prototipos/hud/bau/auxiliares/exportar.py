"""As propostas do baú (protótipo; nada no jogo): das grades desenhadas à mão (grades_a.py, grades_b.py) para as fontes
em camadas (fontes/<peça>/<peça>-32.aseprite, uma camada por material, pelo montar_fontes.py e o pintar.lua) e para os
PNGs dos lugares em que o baú fica parado no jogo: o 32 (a bolsa, a bolsa do Inventário, o ganho que voa, o chip do
espólio) e o 48 (a pilha de vários baús abertos juntos), este o 32 centrado com margem, sem redimensionar. O 64 do
catálogo não tem lugar no jogo hoje (nenhuma tela pede o baú em 64): sai o 32 ampliado 2×, só para o conjunto ficar
completo. Os @2x são a duplicação exata. Confere que o .aseprite exportado sai igual, pixel a pixel, à grade.

    python ferramentas/prototipos/hud/bau/auxiliares/exportar.py
"""
import importlib.util
import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops

AQUI = pathlib.Path(__file__).resolve().parent.parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(RAIZ / "ferramentas" / "arte"))
sys.argv.append(f"--fontes={AQUI / 'fontes'}")
import exportar_aseprite as ex  # noqa: E402
import montar_fontes  # noqa: E402

PROPOSTAS = {"bau-a": "grades_a.py", "bau-b": "grades_b.py", "bau-a2": "grades_a2.py"}


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, AQUI / nome)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def imagem(m, grade=None):
    grade = grade or m.G32
    n = len(grade)
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    for y, linha in enumerate(grade):
        assert len(linha) == n, (y, len(linha))
        for x, c in enumerate(linha):
            if c != ".":
                im.putpixel((x, y), tuple(int(m.PALETA[c][i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    return im


def listas(m, pasta, grade=None):
    """Uma lista por camada (o material de cada caractere), no formato do pintar.lua; de baixo para cima."""
    grade = grade or m.G32
    pasta.mkdir(parents=True, exist_ok=True)
    for camada, chars in m.CAMADAS.items():
        px = [f"{x},{y},{m.PALETA[c][1:].upper()}" for y, l in enumerate(grade) for x, c in enumerate(l) if c in chars]
        (pasta / f"{camada}.lua").write_text(f'return "{";".join(px)}"\n', encoding="utf-8")
    (pasta / "ordem.txt").write_text(",".join(m.CAMADAS) + "\n", encoding="utf-8")


def salvar(im, pasta, nome):
    im.save(pasta / f"{nome}.png")
    im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(pasta / f"{nome}@2x.png")


for peca, arq in PROPOSTAS.items():
    m = carregar(arq)
    base = imagem(m)
    saida = AQUI / "propostas" / peca
    saida.mkdir(parents=True, exist_ok=True)
    salvar(base, saida, "bau-32")
    if hasattr(m, "G48"):  # a A2: o 48 próprio, desenhado na grade de 48 com a construção do 32
        salvar(imagem(m, m.G48), saida, "bau-48")
    else:  # A e B: o 32 centrado com margem
        centro = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
        centro.paste(base, (8, 8))
        salvar(centro, saida, "bau-48")
    salvar(base.resize((64, 64), Image.NEAREST), saida, "bau-64")
    grades = {32: m.G32, **({48: m.G48} if hasattr(m, "G48") else {})}
    with tempfile.TemporaryDirectory() as tmp:
        for lado, grade in grades.items():
            listas(m, pathlib.Path(tmp) / f"{peca}-{lado}", grade)
        montar_fontes.montar(peca, pathlib.Path(tmp))
        for lado, grade in grades.items():
            fonte = AQUI / "fontes" / peca / f"{peca}-{lado}.aseprite"
            png = pathlib.Path(tmp) / f"conferir-{lado}.png"
            subprocess.run([ex.aseprite(), "-b", str(fonte), "--save-as", str(png)], check=True, capture_output=True)
            igual = ImageChops.difference(Image.open(png).convert("RGBA"), imagem(m, grade)).getbbox() is None
            im = imagem(m, grade)
            print(f"{peca} {lado}: {len({p for p in im.getdata() if p[3]})} cores, ocupa {im.getchannel('A').getbbox()}; "
                  f"a fonte em camadas exporta igual à grade: {igual}")
