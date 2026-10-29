"""A fonte em camadas do M1 (Morel, a cadeira e a mesa dele, na densidade da B4) e as camadas da prova.

    python ferramentas/prototipos/taverna/prova/m1/fonte.py --criar [--refazer]   # gera a fonte a partir do desenho.py
    python ferramentas/prototipos/taverna/prova/m1/fonte.py [--conferir]           # exporta da fonte

A fonte é `aseprite/m1.aseprite` (144×112, um quadro): as camadas guia, cadeira, mesa, morel e frente (o montante do
espaldar que passa na frente das costas dele), de baixo para cima. A guia é o canto da referência geral ("entre brasas e
sombras") posto na grade (a cabeça de Morel no lugar da dele, 5,3 pixels da referência por pixel da grade), oculta e
meio transparente: orienta e nunca é exportada. Depois de criada, a fonte é a autoridade: os retoques se fazem nela, e
`--criar` não a sobrescreve sem `--refazer`.

Exportar lê a fonte como está (as camadas visíveis, menos a guia) e grava em `camadas/prova/`:
- `m1.png`: Morel no canto (cadeira, mesa, morel, frente);
- `m1-sem.png`: recrutado (cadeira, mesa e frente: sem nada dele, nem a tigela);
- `fundo-m1.png` e `velas-m1.png`: a sala da F sem a mesa redonda e sem o canto de Morel, com a chama da vela dele no
  castiçal novo (as duas saem do código da F, não da fonte).
`--conferir` compara `m1.png` e `m1-sem.png` com o que o desenho.py desenha; depois de um retoque na fonte, as
diferenças são o retoque."""
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

from prova.m1 import desenho as M  # noqa: E402
from prova.b3.fonte import ler  # noqa: E402
from prova import conjunto as C  # noqa: E402
from f import desenho as D, gente as G  # noqa: E402
from exportar_aseprite import aseprite  # noqa: E402

FONTE = AQUI / "aseprite" / "m1.aseprite"
MONTAR = AQUI.parent / "b2" / "aseprite" / "montar.lua"
REFERENCIA = RAIZ / "ferramentas" / "arte" / "referencias" / "cenarios internos" / "Taverna medieval entre brasas e sombras.png"
SAIDA = pathlib.Path(C.CAMADAS)
GUIA = (5.3, (2060, 325), (62, 24))      # pixels da referência por pixel da grade; o alto da cabeça de Morel nas duas


def guia():
    e, (cx, cy), (gx, gy) = GUIA
    x0, y0 = cx - gx * e, cy - gy * e
    im = Image.open(REFERENCIA).convert("RGBA")
    return im.crop((round(x0), round(y0), round(x0 + M.W * e), round(y0 + M.H * e))).resize((M.W, M.H), Image.BOX)


def compor(camadas):
    """As camadas visíveis, menos a guia, no quadro do M1."""
    im = Image.new("RGBA", (M.W, M.H))
    for nome, visivel, c in camadas:
        if nome != "guia" and visivel:
            im.alpha_composite(c)
    return im


def criar():
    if FONTE.exists() and "--refazer" not in sys.argv:
        sys.exit(f"{FONTE.name} já existe: os retoques dela se perderiam. Use --refazer para gerar de novo.")
    FONTE.parent.mkdir(exist_ok=True)
    camadas = {"guia": guia(), **{n: t.imagem() for n, t in M.camadas().items()}}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        for nome, im in camadas.items():
            im.save(tmp / f"{nome}.png")
        script = tmp / "montar.lua"  # copiado: com espaço no caminho, o Aseprite não roda o script
        shutil.copy(MONTAR, script)
        r = subprocess.run([aseprite(), "-b", "--script-param", f"pasta={tmp}", "--script-param",
                            f"camadas={','.join(camadas)}", "--script-param", f"largura={M.W}", "--script-param",
                            f"altura={M.H}", "--script-param", f"saida={FONTE}", "--script", str(script)],
                           capture_output=True, text=True)
        if not FONTE.exists() or "celulas" not in r.stdout:
            sys.exit(f"O Aseprite não montou a fonte:\n{r.stdout}{r.stderr}")
    print(FONTE.name, "camadas:", ", ".join(camadas), "(a guia oculta)")


def sala():
    """A sala da F sem a roda e sem o canto, com a vela de Morel no castiçal novo: o fundo e a tira das velas."""
    D.SEM_RODA, D.SEM_CANTO, D.VELA_MOREL = True, True, M.vela_sala()
    try:
        t = D.Tela(D.QW, D.QH)
        px = D.Pincel(t)
        r = D.sala(px)
        G.desenhar(px, r, morel=True)
        D.luz(t, r["chamas"], r["boca"])
        velas = [D.velas(i).imagem() for i in range(4)]
    finally:
        D.SEM_RODA, D.SEM_CANTO, D.VELA_MOREL = False, False, None
    tira = Image.new("RGBA", (D.QW * 4, D.QH))
    for i, v in enumerate(velas):
        tira.paste(v, (D.QW * i, 0))
    return t.imagem(), tira


def exportar():
    if not FONTE.exists():
        sys.exit(f"Sem a fonte {FONTE}: crie com --criar.")
    camadas = ler(FONTE)
    com = compor([(n, v, c) for n, v, c in camadas if n in M.PRESENTE])
    sem = compor([(n, v, c) for n, v, c in camadas if n in M.AUSENTE])
    SAIDA.mkdir(parents=True, exist_ok=True)
    com.save(SAIDA / "m1.png", optimize=True)
    sem.save(SAIDA / "m1-sem.png", optimize=True)
    fundo, velas = sala()
    fundo.save(SAIDA / "fundo-m1.png")
    velas.save(SAIDA / "velas-m1.png")
    print("m1.png de", ", ".join(n for n, v, _ in camadas if n in M.PRESENTE and v), "; m1-sem.png, fundo-m1.png, velas-m1.png")
    return com, sem


def conferir(com, sem):
    cs = M.camadas()
    dif = 0
    for im, nomes in ((com, M.PRESENTE), (sem, M.AUSENTE)):
        a, b = im.tobytes(), M.composto(cs, nomes).imagem().convert("RGBA").tobytes()
        dif += sum(a[i:i + 4] != b[i:i + 4] for i in range(0, len(a), 4))
    print(f"conferido: {dif} pixels diferentes do desenho.py" + (" (os retoques da fonte)" if dif else ""))
    return dif


if __name__ == "__main__":
    if "--criar" in sys.argv:
        criar()
        sys.exit(0)
    com, sem = exportar()
    if "--conferir" in sys.argv:
        conferir(com, sem)
