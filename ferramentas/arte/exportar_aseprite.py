"""Exporta os ícones cuja fonte final é um .aseprite (ferramentas/arte/aseprite/<peça>/<peça>-<lado>.aseprite) para os
PNGs do jogo: o 1× pela linha de comando do Aseprite (o composto das camadas visíveis) e o @2x pela duplicação exata
(vizinho mais próximo), como o `salvar` de pixel_comum.py. Os tamanhos que uma peça tira de outro por ampliação inteira
exata (DERIVADOS: no gibão e nas botas, o 64 é o 32 ampliado 2×), ou o centram num quadro transparente maior (o 40 e o
48 da manopla são o 32 no meio), saem do PNG exportado da fonte, sem retoque; a pasta da peça não tem fonte desse tamanho
(os desenhados à parte ficam em aseprite/historico/, fora da exportação).

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


# lado derivado: (lado da fonte, fator inteiro) para a ampliação exata, ou (lado da fonte, CENTRO) para o desenho da fonte
# sem redimensionar, no centro de um quadro transparente do lado (deslocado (lado - fonte) / 2 px). Só as peças listadas;
# as outras exportam cada fonte que têm.
CENTRO = "centro"
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
    "manopla": {40: (32, CENTRO), 48: (32, CENTRO), 64: (32, 2)},  # 1.151.0: as luvas L7 (a M5 da 1.147.0 em historico/):
                                     # o 40 e o 48 são o 32 centrado (4 e 8 px), o 64 é o 32 ×2
    "elmo": {40: (32, CENTRO), 48: (32, CENTRO), 64: (32, 2)},  # 1.153.0: o capacete com malha C1 (o elmo de frente da
                                     # 1.148.0 em historico/): o 40 e o 48 são o 32 centrado, o 64 é o 32 ×2
    "perneiras": {40: (32, CENTRO), 48: (32, CENTRO), 64: (32, 2)},  # 1.152.0: a P7 (a P4 da 1.148.0 em historico/):
                                     # o 40 e o 48 são o 32 centrado, como na manopla; o 64 é o 32 ×2
    "botas-ferro": {64: (32, 2)},    # 1.154.0: as botas de ferro com o acabamento A1 (a B3 da 1.150.0 em historico/); o 64 é o 32 ×2
    # 1.162.0: as cabeças das criaturas (16×16, como os retratos de carta da comitiva): o 32 é a carta da luta (×2) e
    # o 48 o Bestiário, o mural e a faixa do mestre caçador (×3). O Afogado C e a Ilse R3 (as alternativas no protótipo)
    "retrato-afogado": {32: (16, 2), 48: (16, 3)},
    "retrato-ilse": {32: (16, 2), 48: (16, 3)},
    # 1.163.0: o Lobo (o "só a base" da segunda rodada, sem as três sobras soltas) e o Bandido da faca
    "retrato-lobo": {32: (16, 2), 48: (16, 3)},
    "retrato-bandido": {32: (16, 2), 48: (16, 3)},
    # 1.164.0: o Urso Pardo e o Falcão Peregrino do patrulheiro (o urso-t2 e o falcao-t2, a transposição das referências
    # geradas, com a guia oculta); só o 32 (o 16 ×2: a carta aliada e o painel do animal), que é o único uso
    "retrato-urso": {32: (16, 2)},
    "retrato-falcao": {32: (16, 2)},
    # 1.166.0: o Troll da montanha (o troll-1 da segunda rodada, de carne, com a guia oculta): a carta e o rastro (32,
    # o 16 ×2) e o Bestiário, o mural e a faixa do mestre caçador (48, o 16 ×3)
    "retrato-troll": {32: (16, 2), 48: (16, 3)},
    # 1.167.0: o Rei Troll (o rei-troll-ouro2: o Troll 2 com a coroa dourada; só a carta, pelo id do guardião) e a Aranha
    # gigante (a aranha-2b; a carta, o Bestiário, o mural e o rastro, pela família)
    "retrato-rei-troll": {32: (16, 2), 48: (16, 3)},
    "retrato-aranha": {32: (16, 2), 48: (16, 3)},
    # 1.168.0: a Rainha Aracnídea (a rainha-a; pelo id da guardiã): só a carta da luta, o 32 (o 16 ×2)
    "retrato-rainha-aracnidea": {32: (16, 2)},
    # 1.171.0: o sapo-touro gigante e a sanguessuga gigante (o sapo-a e a sanguessuga-a, pela família)
    "retrato-sapo": {32: (16, 2), 48: (16, 3)},
    "retrato-sanguessuga": {32: (16, 2), 48: (16, 3)},
    # 1.172.0: o cultista (o cultista-a dos quatro pares), a bruxa do pântano (a bruxa-b3) e o rato gigante (o rato-r2 da
    # segunda rodada), pela família
    "retrato-cultista": {32: (16, 2), 48: (16, 3)},
    "retrato-bruxa": {32: (16, 2), 48: (16, 3)},
    "retrato-rato": {32: (16, 2), 48: (16, 3)},
    # 1.173.0: o javali selvagem e o carniçal (o javali-a3 e o carnical-a3 da terceira rodada), pela família
    "retrato-javali": {32: (16, 2), 48: (16, 3)},
    "retrato-carnical": {32: (16, 2), 48: (16, 3)},
    # 1.174.0: o espectro (o espectro-ap da terceira rodada: o A com o pano até a borda de baixo), pela família
    "retrato-espectro": {32: (16, 2), 48: (16, 3)},
    # 1.175.0: o esqueleto (o E1r do esqueleto_novo: o guarda morto de elmo, com a aba limpa), pela família
    "retrato-esqueleto": {32: (16, 2), 48: (16, 3)},
    # 1.179.0: o mercenário (o MA: o chapéu de ferro) e o lobo gélido (o LA: o lobo da geada), pela família
    "retrato-mercenario": {32: (16, 2), 48: (16, 3)},
    "retrato-lobo-gelido": {32: (16, 2), 48: (16, 3)},
    # 1.182.0: o caído (o CA: o diabrete que ri), pela família; o xamã caído continua no "demonio"
    "retrato-caido": {32: (16, 2), 48: (16, 3)},
    # 1.183.0: o grifo (o GA3: a águia-leão com o gancho do bico), pela família; a harpia continua no "voador"
    "retrato-grifo": {32: (16, 2), 48: (16, 3)},
    # 1.184.0: a harpia (a T2: o rosto de mulher, as penas da cabeça e a gola de abutre; a guia oculta fica fora da
    # exportação) e o xamã caído (o X1r2: o capuz, a pintura branca e o colar de osso), pela família
    "retrato-harpia": {32: (16, 2), 48: (16, 3)},
    "retrato-xama-caido": {32: (16, 2), 48: (16, 3)},
    # 1.185.0: a cria do Vazio (a A2: o caco da Fenda com volume nos cacos), pela família, com as que o antagonista invoca
    "retrato-cria-vazio": {32: (16, 2), 48: (16, 3)},
    # 1.186.0: o cão infernal (a P1: o cão de carvão de perfil com a bocarra de presas), pela família
    "retrato-cao-infernal": {32: (16, 2), 48: (16, 3)},
    # 1.187.0: o cavaleiro sombrio (o P3: a cúpula com a crista afundada no gorjal alto), pela família, com o Último Guarda
    "retrato-cavaleiro-sombrio": {32: (16, 2), 48: (16, 3)},
    # 1.188.0: a abominação (a C3: a boca enorme sustentada pelas bochechas, o Vazio no fundo), pela família
    "retrato-abominacao": {32: (16, 2), 48: (16, 3)},
    # 1.189.0: a árvore desperta (a T1, a transposição da referência 1, com a guia oculta) e o golem de pedra (o G2, o
    # rochedo), pelas famílias; o Espantalho Possuído e o Mímico continuam nos traços
    "retrato-arvore-desperta": {32: (16, 2), 48: (16, 3)},
    "retrato-golem": {32: (16, 2), 48: (16, 3)},
}
# O martelo (1.149.0) só tem fontes do 40 e do 48 (aseprite/martelo/): o 32 e o 64 são a grade de desenhos.js, no
# jogo, e não saem daqui.


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
        if fator == CENTRO:
            assert (lado - base) % 2 == 0, f"{peca}: {base} não centra em {lado}"
            der = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
            der.paste(im, ((lado - base) // 2,) * 2)
        else:
            der = im.resize((im.width * fator, im.height * fator), Image.NEAREST)
        assert der.size == (lado, lado), f"{peca}: {base}×{fator} não dá {lado}"
        der.save(pasta / f"{peca}-{lado}.png")
        der.resize((lado * 2, lado * 2), Image.NEAREST).save(pasta / f"{peca}-{lado}@2x.png")
        feitos += [f"{peca}-{lado}.png", f"{peca}-{lado}@2x.png"]
    return feitos


def recupera(peca):
    """Cada derivado do jogo volta exatamente à sua fonte? A ampliação, reduzida pegando um pixel de cada bloco
    fator×fator; o centrado, recortado no meio (e a beira toda transparente)."""
    ok = []
    for lado, (base, fator) in DERIVADOS.get(peca, {}).items():
        der, src = Image.open(JOGO / f"{peca}-{lado}.png").convert("RGBA"), Image.open(JOGO / f"{peca}-{base}.png").convert("RGBA")
        if fator == CENTRO:
            d = (lado - base) // 2
            miolo = list(der.crop((d, d, d + base, d + base)).getdata()) == list(src.getdata())
            beira = all(der.getpixel((x, y))[3] == 0 for y in range(lado) for x in range(lado)
                        if not (d <= x < d + base and d <= y < d + base))
            print(f"{peca}-{lado}: o miolo {'= ' if miolo else '≠ '}{peca}-{base} (deslocado {d} px); a beira "
                  f"{'transparente' if beira else 'NÃO transparente'}")
            ok.append(miolo and beira)
            continue
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
