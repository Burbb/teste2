"""Exporta os ícones cuja fonte final é um .aseprite (ferramentas/arte/aseprite/<peça>/<peça>-<lado>.aseprite) para os
PNGs do jogo: o 1× pela linha de comando do Aseprite (o composto das camadas visíveis) e o @2x pela duplicação exata
(vizinho mais próximo), como o `salvar` de pixel_comum.py. Os tamanhos que uma peça tira de outro por ampliação inteira
exata (DERIVADOS: no gibão e nas botas, o 64 é o 32 ampliado 2×) saem do PNG exportado da fonte, sem retoque; a pasta
da peça não tem fonte desse tamanho (os 64 desenhados à parte ficam em aseprite/historico/, fora da exportação).

    python ferramentas/arte/exportar_aseprite.py varinha                 # grava em rpg/web/static/hud/icones/
    python ferramentas/arte/exportar_aseprite.py varinha <pasta>         # grava numa pasta qualquer (proposta)
    python ferramentas/arte/exportar_aseprite.py varinha --conferir      # exporta numa pasta temporária e compara
                                                                         # com os do jogo, byte a byte e pixel a pixel
    python ferramentas/arte/exportar_aseprite.py todas --conferir        # todas as peças (as pastas com fontes)

O Aseprite vem de ASEPRITE=<executável>; sem a variável, de `aseprite` no PATH ou do lugar de instalação comum (Steam
no Windows, macOS e Linux). O jogo nunca lê nada daqui: só os PNGs exportados.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parents[2]
FONTES = RAIZ / "ferramentas" / "arte" / "aseprite"
# --fontes=<pasta>: as fontes de uma proposta (a pasta tem <peça>/<peça>-<lado>.aseprite), fora de aseprite/: o
# exportador grava os PNGs numa pasta dada, e o --conferir de uma proposta é contra ela, não contra o jogo
for _a in sys.argv[1:]:
    if _a.startswith("--fontes="):
        FONTES = pathlib.Path(_a.split("=", 1)[1]).resolve()
JOGO = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
LUGARES = [
    pathlib.Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam/steamapps/common/Aseprite/Aseprite.exe",
    pathlib.Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Aseprite/Aseprite.exe",
    pathlib.Path("/Applications/Aseprite.app/Contents/MacOS/aseprite"),
    pathlib.Path.home() / "Library/Application Support/Steam/steamapps/common/Aseprite/Aseprite.app/Contents/MacOS/aseprite",
    pathlib.Path.home() / ".steam/steam/steamapps/common/Aseprite/aseprite",
]


# lado derivado: (lado da fonte, fator inteiro). Só as peças listadas; as outras exportam cada fonte que têm.
DERIVADOS = {
    "gibao": {64: (32, 2)},     # 1.110.0: o 64 é o 32 final ampliado 2× (o 64 desenhado à parte é histórico)
    "bota": {64: (32, 2)},
    "capuz": {64: (32, 2)},          # 1.112.0: a cabeça e as mãos de couro e de tecido, o 64 também é o 32 ampliado 2×
    "luva": {64: (32, 2)},
    "capuz_tecido": {64: (32, 2)},
    "luva_seda": {64: (32, 2)},
    "calca_couro": {64: (32, 2)},    # 1.119.0: a Calça de Couro do Arqueiro, o 64 também é o 32 ampliado 2×
    "attr-ataque": {64: (32, 2)},    # 1.120.0: os atributos Ataque e Defesa (24 e 32 das fontes); o 64 do selo é o 32 ×2
    "attr-defesa": {64: (32, 2)},
    "attr-agilidade": {64: (32, 2)},  # 1.121.0: a Agilidade (a bota em passada, também o Fugir); o 64 do selo é o 32 ×2
    "aljava": {64: (32, 2)},          # 1.122.0: a aljava (24 e 32 aprovados; 40 e 48 derivados); o 64 é o 32 ×2
    "attr-poder": {64: (32, 2)},     # 1.123.0: o Poder (a chama violeta); o 64 do selo é o 32 ×2
    "calca_tecido": {64: (32, 2)},   # 1.138.0: a Calça de Viagem e o Manto do Mago (32, 40, 48 das fontes); o 64 é o 32 ×2
    "manto": {64: (32, 2)},
    "anel": {64: (32, 2)},           # 1.140.0: o anel (a rodada 3) e o amuleto (a gema violeta); o 64 é o 32 ×2
    "amuleto": {64: (32, 2)},
    "chapeu": {64: (32, 2)},         # 1.141.0: o Chapéu Pontudo do Mago (32, 40, 48 das fontes); o 64 é o 32 ×2
    "sandalia": {64: (32, 2)},
    "besta": {64: (32, 2)},          # 1.143.0: a Besta Leve do Arqueiro (32, 40, 48 das fontes); o 64 é o 32 ×2
    "diadema": {64: (32, 2)},        # 1.144.0: o Diadema do Mago (a rodada 2, de frente; 32, 40, 48); o 64 é o 32 ×2
    "espada": {64: (32, 2)},         # 1.145.0: o remake do ferro, a espada e a maça (32, 40, 48 das fontes); o 64 é o 32 ×2
    "maca": {64: (32, 2)},
    "cota": {64: (32, 2)},           # 1.146.0: a cota de malha do Guerreiro (32, 40, 48 das fontes); o 64 é o 32 ×2
    "manopla": {64: (32, 2)},        # 1.147.0: a manopla de malha (a M5, da glove_04 da Dungeon Crawl, CC0); o 64 é o 32 ×2
    "elmo": {64: (32, 2)},           # 1.148.0: o elmo de frente (a rodada 4) e as perneiras de malha com placas (a P4); o 64 é o 32 ×2
    "perneiras": {64: (32, 2)},
}


def pecas():
    """As peças com fontes (as pastas de aseprite/, menos o histórico)."""
    return sorted(p.name for p in FONTES.iterdir() if p.is_dir() and p.name != "historico" and any(p.glob("*.aseprite")))


def aseprite():
    if os.environ.get("ASEPRITE"):
        return os.environ["ASEPRITE"]
    achado = shutil.which("aseprite") or next((str(p) for p in LUGARES if p.exists()), None)
    if not achado:
        sys.exit("Não achei o Aseprite: defina ASEPRITE=<executável>.")
    return achado


def fontes(peca):
    lista = sorted(FONTES.joinpath(peca).glob(f"{peca}-*.aseprite"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    if not lista:
        sys.exit(f"Sem fontes em {FONTES / peca}.")
    return lista


def exportar(peca, pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    exe, feitos = aseprite(), []
    for fonte in fontes(peca):
        png = pasta / f"{fonte.stem}.png"
        r = subprocess.run([exe, "-b", str(fonte), "--save-as", str(png)], capture_output=True, text=True)
        if r.returncode or not png.exists():
            sys.exit(f"O Aseprite não exportou {fonte.name}:\n{r.stdout}{r.stderr}")
        im = Image.open(png).convert("RGBA")
        im.resize((im.width * 2, im.height * 2), Image.NEAREST).save(pasta / f"{fonte.stem}@2x.png")
        feitos += [png.name, f"{fonte.stem}@2x.png"]
    for lado, (base, fator) in DERIVADOS.get(peca, {}).items():
        im = Image.open(pasta / f"{peca}-{base}.png").convert("RGBA")
        der = im.resize((im.width * fator, im.height * fator), Image.NEAREST)
        assert der.size == (lado, lado), f"{peca}: {base}×{fator} não dá {lado}"
        der.save(pasta / f"{peca}-{lado}.png")
        der.resize((lado * 2, lado * 2), Image.NEAREST).save(pasta / f"{peca}-{lado}@2x.png")
        feitos += [f"{peca}-{lado}.png", f"{peca}-{lado}@2x.png"]
    return feitos


def recupera(peca):
    """Cada derivado do jogo, reduzido pegando um pixel de cada bloco fator×fator, volta exatamente à sua fonte?"""
    ok = []
    for lado, (base, fator) in DERIVADOS.get(peca, {}).items():
        der, src = Image.open(JOGO / f"{peca}-{lado}.png").convert("RGBA"), Image.open(JOGO / f"{peca}-{base}.png").convert("RGBA")
        blocos = all(len({der.getpixel((x * fator + i, y * fator + j)) for i in range(fator) for j in range(fator)}) == 1
                     for y in range(base) for x in range(base))
        volta = all(der.getpixel((x * fator, y * fator)) == src.getpixel((x, y)) for y in range(base) for x in range(base))
        print(f"{peca}-{lado}: blocos {fator}×{fator} {'uniformes' if blocos else 'NÃO uniformes'}; reduzido "
              f"{'= ' if volta else '≠ '}{peca}-{base}")
        ok.append(blocos and volta)
    return all(ok)


def conferir(peca):
    with tempfile.TemporaryDirectory() as tmp:
        diferentes = []
        for nome in exportar(peca, pathlib.Path(tmp)):
            novo, jogo = pathlib.Path(tmp) / nome, JOGO / nome
            if not jogo.exists():
                diferentes.append(f"{nome}: não está no jogo")
                continue
            pixels = list(Image.open(novo).convert("RGBA").getdata()) == list(Image.open(jogo).convert("RGBA").getdata())
            bytes_ = novo.read_bytes() == jogo.read_bytes()
            print(f"{nome}: pixels {'iguais' if pixels else 'DIFERENTES'}, bytes {'iguais' if bytes_ else 'diferentes'}")
            if not pixels:
                diferentes.append(nome)
        return diferentes


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if "--conferir" in sys.argv:
        dif, derivados = [], True
        for peca in (pecas() if args == ["todas"] else args):
            print(f"== {peca}")
            dif += conferir(peca)
            derivados &= recupera(peca)
        print("tudo igual ao jogo" if not dif and derivados else "DIFERENTE: " + ", ".join(dif or ["derivado"]))
        sys.exit(1 if dif or not derivados else 0)
    peca = args[0]
    pasta = pathlib.Path(args[1]) if len(args) > 1 else JOGO
    print("\n".join(str(pasta / n) for n in exportar(peca, pasta)))


if __name__ == "__main__":
    main()
