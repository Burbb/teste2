"""As folhas da G (a F corrigida, na arte do jogo), a partir do desenho (g/cena_g.py, f/cena_f.py) e das capturas do jogo
(fotografar.mjs com VERSOES=f,g; ciclo_f.mjs com VERSAO=g; estilo.mjs):

- ../folha-forja-g.png: a F × a G no jogo, com os mesmos dados, a 1920×945 e a 1280×720; a G em tamanho real.
- ../folha-estilo-g.png: a G ao lado da capela (o ossuário), da prisão da Ilse (o fundo), da cidade (o Vau) e do
  mercado, todas como o jogo as mostra a 1920 (a mesma escala de exibição, 1:1), e um recorte de cada a 3× para
  comparar os pixels (a pedra, a madeira, o metal, a luz).
- ../folha-correcoes-g.png: a F × a G nos mesmos quadros do ciclo (5×): os pés e as pernas no alto (o tronco subindo)
  e no golpe; a mão, a tenaz e a espiga no golpe, no rebote e na pausa.
- ../folha-movimento-g.png: os estados (5×), o ciclo inteiro como o jogo mostrou, o movimento reduzido.

    python ferramentas/prototipos/hud/forja/auxiliares/folha_g.py
"""
import importlib
import pathlib
import sys

from PIL import Image, ImageDraw

from folha import fonte
from folha_f import FUNDO, montar

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"


def modulo(versao, nome):
    """O módulo da pasta f/ ou g/ (as duas têm nomes próprios: cena_f, cena_g)."""
    pasta = str(AQUI.parent / versao)
    if pasta not in sys.path:
        sys.path.insert(0, pasta)
    return importlib.import_module(f"{nome}_{versao}")


Cf, Cg = modulo("f", "cena"), modulo("g", "cena")
ESTADOS = modulo("g", "desenhar").ESTADOS


def q_de(C, nome, t=0):
    return next(q for q in range(C.DURACAO) if C.pose_de(q)["nome"] == nome and C.pose_de(q)["t"] == t)


def corte(C, q, rec, e=5, faiscas=False):
    im = C.quadro(q, com_faiscas=faiscas).imagem().convert("RGB").crop(rec)
    return im.resize((im.width * e, im.height * e), Image.NEAREST)


def rotulo(im, texto):
    im = im.copy()
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 8 + 7 * len(texto), 18), fill=(0, 0, 0))
    d.text((4, 2), texto, fill=(255, 220, 120), font=fonte(12))
    return im


def folha_forja():
    metade = lambda n: (lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS))(Image.open(CAP / f"{n}.png").convert("RGB"))
    montar("A forja G: a F com a animação corrigida e a oficina redesenhada na arte do jogo (protótipo)", [
        ("1920×945 · a F × a G, no jogo, com os mesmos dados (a mesma campanha de teste, o mesmo balcão)",
         [(metade("1920-f-forja"), "F"), (metade("1920-g-forja"), "G")]),
        ("1280×720 · a F × a G", [(metade("1280-f-forja"), "F"), (metade("1280-g-forja"), "G")]),
        ("a G em tamanho real, como o jogo a mostra a 1920", [(Image.open(CAP / "ciclo-g-1920-000.png").convert("RGB"), "G")]),
    ], AQUI.parent / "folha-forja-g.png")


def folha_estilo():
    g = Image.open(CAP / "ciclo-g-1920-000.png").convert("RGB")
    cenas = [("capela", "a capela (o ossuário)"), ("ilse", "a prisão da Ilse (o fundo alagado)"),
             ("cidade", "a cidade (o Vau)"), ("mercado", "o mercado (a banca)")]
    ims = {n: Image.open(CAP / f"estilo-{n}.png").convert("RGB") for n, _ in cenas}
    # um recorte de cada a 3× (só a arte, sem os nomes): a parede, a madeira, os objetos, a luz
    recortes = [(g, (330, 60, 530, 200)), (ims["capela"], (600, 0, 800, 140)), (ims["ilse"], (0, 0, 200, 140)),
                (ims["cidade"], (360, 60, 560, 200)), (ims["mercado"], (110, 0, 310, 98))]
    zoom = [rotulo(im.crop(r).resize(((r[2] - r[0]) * 2, (r[3] - r[1]) * 2), Image.NEAREST), n)
            for (im, r), n in zip(recortes, ["G", "capela", "Ilse", "cidade", "mercado"])]
    montar("A forja G ao lado dos ambientes aprovados do jogo, como o jogo os mostra a 1920 (a mesma escala de exibição)", [
        ("a G (a forja) · a capela", [(g, "G"), (ims["capela"], "a capela (o ossuário)")]),
        ("a prisão da Ilse · a cidade", [(ims["ilse"], "a prisão da Ilse (o fundo alagado)"), (ims["cidade"], "a cidade (o Vau)")]),
        ("o mercado (a banca do mercador; a cena do mercado tem a altura dela)", [(ims["mercado"], "o mercado")]),
        ("recortes a 2× (os pixels da tela a 1920): a pedra em blocos com as juntas um tom abaixo, a madeira e o metal em "
         "dois ou três tons, a luz em halo e em degraus pontilhados", [(z, "") for z in zoom[:3]]),
        ("", [(z, "") for z in zoom[3:]]),
    ], AQUI.parent / "folha-estilo-g.png")


def folha_correcoes():
    pernas = (140, 62, 196, 90)
    mao = (134, 46, 176, 66)
    linhas = []
    for nome, t, rot in [("alto", 0, "no alto (o tronco sobe 1 px)"), ("golpe", 0, "no golpe (o tronco desce 1 px)")]:
        linhas.append((f"os pés e as pernas {rot}: F × G",
                       [(rotulo(corte(Cf, q_de(Cf, nome, t), pernas), "F"), ""), (rotulo(corte(Cg, q_de(Cg, nome, t), pernas), "G"), "")]))
    for nome, t, rot in [("golpe", 0, "no golpe"), ("volta", 0, "no rebote"), ("ajuste", 1, "na pausa (a espada virada)")]:
        linhas.append((f"a mão, a tenaz e a espiga {rot}: F × G",
                       [(rotulo(corte(Cf, q_de(Cf, nome, t), mao, faiscas=True), "F"), ""),
                        (rotulo(corte(Cg, q_de(Cg, nome, t), mao, faiscas=True), "G"), "")]))
    montar("A G · as correções da animação (5×, só diagnóstico; os mesmos quadros do ciclo nas duas)", linhas,
           AQUI.parent / "folha-correcoes-g.png")


def folha_movimento():
    REC = (112, 10, 196, 92)
    durs = {}
    for n, d in Cg.CICLO:
        durs.setdefault(n, set()).add(d * 100)
    poses = []
    for e in ESTADOS:
        nome = "ajuste" if e == "ajuste_virada" else e
        q = q_de(Cg, nome, 1 if e == "ajuste_virada" else 0)
        rot = f"{e} · {' / '.join(str(v) for v in sorted(durs[nome]))} ms" if e != "ajuste_virada" else "ajuste, a espada virada (400 ms dos 600)"
        poses.append((corte(Cg, q, REC, faiscas=True), rot))
    im0 = Image.open(CAP / "ciclo-g-1920-000.png")
    e = im0.width / 320
    caixa = (int(112 * e), int(10 * e), int(196 * e), int(92 * e))
    fotos = [Image.open(CAP / f"ciclo-g-1920-{i:03d}.png").convert("RGB").crop(caixa) for i in range(Cg.DURACAO)]
    w, h = fotos[0].width // 2, fotos[0].height // 2
    tira = Image.new("RGB", (9 * (w + 2), 6 * (h + 2)), FUNDO)
    for i, im in enumerate(fotos):
        t = im.resize((w, h), Image.NEAREST)
        ImageDraw.Draw(t).text((3, 2), str(i), fill=(255, 220, 120), font=fonte(11))
        tira.paste(t, ((i % 9) * (w + 2), (i // 9) * (h + 2)))
    reduzido = Cg.quadro(0, reduzido=True).imagem().convert("RGB").crop(REC)
    montar("A forja G · o ferreiro forjando: o ritmo da R, os apoios corrigidos", [
        ("os estados do ferreiro (5×, só diagnóstico), na ordem do golpe, com a duração no ciclo", poses[:5]),
        ("", poses[5:]),
        (f"o ciclo inteiro como o jogo mostrou a 1920 (53 fotos seguidas do relógio de 100 ms, à metade; "
         f"{Cg.DURACAO / 10:.1f} s; o último quadro emenda no primeiro)", [(tira, "")]),
        ("com movimento reduzido: a pose do alto, parada, o fogo parado e sem faíscas (5×)",
         [(reduzido.resize((reduzido.width * 5, reduzido.height * 5), Image.NEAREST), "")]),
    ], AQUI.parent / "folha-movimento-g.png")


if __name__ == "__main__":
    folha_forja()
    folha_estilo()
    folha_correcoes()
    folha_movimento()
