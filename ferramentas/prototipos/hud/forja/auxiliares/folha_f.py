"""As folhas da F (a transposição fiel), a partir do desenho (f/cena_f.py) e das capturas do jogo (fotografar.mjs com
VERSOES=r,f e ciclo_f.mjs):

- ../folha-forja-f.png: a referência × a F no mesmo enquadramento (as duas a 3×, e a referência a 50% por cima da F
  para comparar as proporções e a composição); a R anterior × a F no jogo, a 1920×945 e a 1280×720 (reduzidas à
  metade); a arte da F em tamanho real, recortada do jogo a 1920.
- ../folha-movimento-f.png: os estados do ferreiro ampliados 5× (só diagnóstico), com a duração no ciclo; o ciclo
  inteiro como o jogo mostrou (as 53 fotos de ciclo_f.mjs, a 1920, reduzidas à metade); a pose parada do movimento
  reduzido; e a cena a 3× no golpe.

    python ferramentas/prototipos/hud/forja/auxiliares/folha_f.py
"""
import pathlib
import sys

from PIL import Image, ImageDraw

from folha import fonte

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
sys.path.insert(0, str(AQUI.parent / "f"))
import base_f  # noqa: E402
import cena_f as C  # noqa: E402
from desenhar_f import ESTADOS  # noqa: E402

FUNDO, TINTA, NOTA = (22, 18, 14), (220, 200, 150), (150, 140, 120)


def montar(titulo, linhas, saida):
    M, ROT = 12, 22
    largura = max(sum(im.width for im, _ in ims) + M * (len(ims) + 1) for _, ims in linhas)
    altura = 40 + sum(max(im.height for im, _ in ims) + 2 * ROT + M for _, ims in linhas)
    folha = Image.new("RGB", (largura, altura), FUNDO)
    d = ImageDraw.Draw(folha)
    d.text((M, 10), titulo, fill=TINTA, font=fonte(16))
    y = 40
    for rot, ims in linhas:
        d.text((M, y), rot, fill=TINTA, font=fonte(14))
        x = M
        for im, r in ims:
            d.text((x, y + ROT), r, fill=NOTA, font=fonte(13))
            folha.paste(im, (x, y + 2 * ROT))
            x += im.width + M
        y += max(im.height for im, _ in ims) + 2 * ROT + M
    folha.save(saida, optimize=True)
    print(saida.name, folha.size)


def referencia_3x():
    ref = Image.open(base_f.REFERENCIA).convert("RGB")
    sy = ref.height / 107
    return ref.crop((0, round(base_f.TOPO * sy), ref.width, round((base_f.TOPO + 96) * sy))).resize((960, 288), Image.LANCZOS)


def x3(t):
    return t.imagem().convert("RGB").resize((960, 288), Image.NEAREST)


def folha_forja():
    q_alto = next(q for q in range(C.DURACAO) if C.pose_de(q)["nome"] == "alto")
    ref, f = referencia_3x(), x3(C.quadro(q_alto))
    metade = lambda n: (lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS))(Image.open(CAP / f"{n}.png").convert("RGB"))
    vista = Image.open(CAP / "ciclo-1920-000.png").convert("RGB")
    montar("A forja F: a transposição fiel da referência (protótipo; a R continua a referência do ritmo)", [
        ("a referência (a imagem gerada, no recorte do quadro: 320×96 de 320×107) × a F, no alto do golpe (as duas a 3×)",
         [(ref, "referência"), (f, "F")]),
        ("a referência a 50% por cima da F: as proporções, os planos e a posição de cada coisa",
         [(Image.blend(f, ref, 0.5), "sobreposição")]),
        ("1920×945 · a R anterior × a F, no mesmo contexto (a mesma campanha de teste, o mesmo balcão)",
         [(metade("1920-r-forja"), "R anterior"), (metade("1920-f-forja"), "F")]),
        ("1280×720 · a R anterior × a F", [(metade("1280-r-forja"), "R anterior"), (metade("1280-f-forja"), "F")]),
        ("a F em tamanho real, como o jogo a mostra a 1920 (1064×343: a escala de 3,33)", [(vista, "F")]),
    ], AQUI.parent / "folha-forja-f.png")


def folha_movimento():
    REC, E = (112, 10, 196, 92), 5
    corte = lambda t: t.imagem().convert("RGB").crop(REC).resize(((REC[2] - REC[0]) * E, (REC[3] - REC[1]) * E), Image.NEAREST)
    durs = {}
    for n, d in C.CICLO:
        durs.setdefault(n, set()).add(d * 100)
    poses = []
    for e in ESTADOS:
        nome = "ajuste" if e == "ajuste_virada" else e
        q = next(q for q in range(C.DURACAO) if C.pose_de(q)["nome"] == nome and (e != "ajuste_virada" or C.pose_de(q)["t"] == 1))
        rot = f"{e} · {' / '.join(str(v) for v in sorted(durs[nome]))} ms" if e != "ajuste_virada" else "ajuste, a espada virada (400 ms dos 600)"
        poses.append((corte(C.quadro(q)), rot))
    im0 = Image.open(CAP / "ciclo-1920-000.png")
    e = im0.width / 320
    caixa = (int(112 * e), int(10 * e), int(196 * e), int(92 * e))
    fotos = [Image.open(CAP / f"ciclo-1920-{i:03d}.png").convert("RGB").crop(caixa) for i in range(C.DURACAO)]
    w, h = fotos[0].width // 2, fotos[0].height // 2
    cols = 9
    tira = Image.new("RGB", (cols * (w + 2), ((len(fotos) + cols - 1) // cols) * (h + 2)), FUNDO)
    for i, im in enumerate(fotos):
        t = im.resize((w, h), Image.NEAREST)
        ImageDraw.Draw(t).text((3, 2), str(i), fill=(255, 220, 120), font=fonte(11))
        tira.paste(t, ((i % cols) * (w + 2), (i // cols) * (h + 2)))
    q_golpe = next(q for q in range(C.DURACAO) if C.pose_de(q)["nome"] == "golpe")
    montar("A forja F · o ferreiro forjando: o ritmo da R com as poses novas", [
        ("os estados do ferreiro (5×, só diagnóstico), na ordem do golpe, com a duração no ciclo", poses[:5]),
        ("", poses[5:]),
        (f"o ciclo inteiro como o jogo mostrou a 1920 (as 53 fotos seguidas do relógio de 100 ms, reduzidas à metade; "
         f"{C.DURACAO / 10:.1f} s; o último quadro emenda no primeiro)", [(tira, "")]),
        ("com movimento reduzido: a pose do alto, parada, o fogo parado e sem faíscas (5×) · a cena a 3× no golpe",
         [(corte(C.quadro(0, reduzido=True)), "movimento reduzido"), (x3(C.quadro(q_golpe)), "golpe")]),
    ], AQUI.parent / "folha-movimento-f.png")


if __name__ == "__main__":
    folha_forja()
    folha_movimento()
