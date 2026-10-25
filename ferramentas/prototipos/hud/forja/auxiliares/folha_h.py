"""As folhas da H (a G com o ferreiro no estilo das figuras do jogo e o corpo inteiro animado), a partir do desenho
(h/cena_h.py, g/cena_g.py) e das capturas do jogo (fotografar.mjs com VERSOES=g,h; ciclo_f.mjs com VERSAO=h;
estilo.mjs):

- ../folha-forja-h.png: a G × a H no jogo, com os mesmos dados, a 1920×945 e a 1280×720; a H em tamanho real.
- ../folha-estilo-h.png: o ferreiro da H ao lado do mercador e da Ilse, como o jogo os mostra a 1920 (2×), e a H ao
  lado das cenas aprovadas.
- ../folha-corpo-h.png: a G × a H nos mesmos quadros do ciclo (5×): o corpo inteiro no alto, no golpe e no rebote, e
  as pernas e as botas.
- ../folha-movimento-h.png: os estados (5×), o ciclo inteiro como o jogo mostrou, o movimento reduzido.

    python ferramentas/prototipos/hud/forja/auxiliares/folha_h.py
"""
import pathlib

from PIL import Image, ImageDraw

from folha import fonte
from folha_f import FUNDO, montar
from folha_g import CAP, corte, modulo, q_de, rotulo

AQUI = pathlib.Path(__file__).resolve().parent
Cg, Ch = modulo("g", "cena"), modulo("h", "cena")
ESTADOS = modulo("h", "desenhar").ESTADOS


def folha_forja():
    metade = lambda n: (lambda im: im.resize((im.width // 2, im.height // 2), Image.LANCZOS))(Image.open(CAP / f"{n}.png").convert("RGB"))
    montar("A forja H: o ferreiro no estilo das figuras do jogo, o corpo inteiro animado, na oficina da G (protótipo)", [
        ("1920×945 · a G × a H, no jogo, com os mesmos dados", [(metade("1920-g-forja"), "G"), (metade("1920-h-forja"), "H")]),
        ("1280×720 · a G × a H", [(metade("1280-g-forja"), "G"), (metade("1280-h-forja"), "H")]),
        ("a H em tamanho real, como o jogo a mostra a 1920", [(Image.open(CAP / "ciclo-h-1920-000.png").convert("RGB"), "H")]),
    ], AQUI.parent / "folha-forja-h.png")


def folha_estilo():
    h = Image.open(CAP / "ciclo-h-1920-000.png").convert("RGB")
    e = h.width / 320
    dobro = lambda im, r: im.crop(r).resize(((r[2] - r[0]) * 2, (r[3] - r[1]) * 2), Image.NEAREST)
    ferreiro = dobro(h, (int(140 * e), int(26 * e), int(196 * e), int(90 * e)))
    mercador = dobro(Image.open(CAP / "estilo-mercado.png").convert("RGB"), (440, 0, 580, 98))
    ilse = dobro(Image.open(CAP / "estilo-ilse.png").convert("RGB"), (480, 20, 640, 160))
    cenas = [(Image.open(CAP / f"estilo-{n}.png").convert("RGB"), r) for n, r in
             [("capela", "a capela (o ossuário)"), ("ilse", "a prisão da Ilse"), ("cidade", "a cidade (o Vau)")]]
    montar("O ferreiro da H ao lado das figuras do jogo (os pixels da tela a 1920, ampliados 2×): três tons chapados, "
           "sem contorno, o olho de um pixel", [
               ("o ferreiro (H) · o mercador · a Ilse", [(ferreiro, "o ferreiro"), (mercador, "o mercador"), (ilse, "a Ilse")]),
               ("a H ao lado das cenas aprovadas, como o jogo as mostra a 1920", [(h, "H"), (cenas[0][0], cenas[0][1])]),
               ("", [(cenas[1][0], cenas[1][1]), (cenas[2][0], cenas[2][1])]),
           ], AQUI.parent / "folha-estilo-h.png")


def folha_corpo():
    corpo, pernas = (126, 12, 196, 92), (140, 56, 196, 90)
    linhas = []
    for nome, rot in [("alto", "no alto: as pernas estendem, o peito sobe e recua"),
                      ("golpe", "no golpe: os joelhos dobram, o quadril desce, o tronco inclina, a barriga achata"),
                      ("volta", "no rebote: o corpo ainda embaixo, a trança balançando")]:
        linhas.append((f"o corpo {rot} · G (a metade de cima deslizando) × H (o corpo inteiro)",
                       [(rotulo(corte(Cg, q_de(Cg, nome), corpo, 4, True), "G"), ""),
                        (rotulo(corte(Ch, q_de(Ch, nome), corpo, 4, True), "H"), "")]))
    linhas.append(("as pernas e as botas no repouso, no alto e no golpe (H): as coxas saindo da cintura, os joelhos, as canelas "
                   "afinando até o cano da bota; os pés parados",
                   [(rotulo(corte(Ch, q_de(Ch, n), pernas, 4), n), "") for n in ("repouso", "alto", "golpe")]))
    montar("A H · o corpo animado (4×, só diagnóstico; os mesmos quadros do ciclo)", linhas, AQUI.parent / "folha-corpo-h.png")


def folha_movimento():
    REC = (112, 10, 196, 92)
    durs = {}
    for n, d in Ch.CICLO:
        durs.setdefault(n, set()).add(d * 100)
    poses = []
    for est in ESTADOS:
        nome = "ajuste" if est == "ajuste_virada" else est
        q = q_de(Ch, nome, 1 if est == "ajuste_virada" else 0)
        rot = f"{est} · {' / '.join(str(v) for v in sorted(durs[nome]))} ms" if est != "ajuste_virada" else "ajuste, a espada virada (400 ms dos 600)"
        poses.append((corte(Ch, q, REC, faiscas=True), rot))
    im0 = Image.open(CAP / "ciclo-h-1920-000.png")
    e = im0.width / 320
    caixa = (int(112 * e), int(10 * e), int(196 * e), int(92 * e))
    fotos = [Image.open(CAP / f"ciclo-h-1920-{i:03d}.png").convert("RGB").crop(caixa) for i in range(Ch.DURACAO)]
    w, hh = fotos[0].width // 2, fotos[0].height // 2
    tira = Image.new("RGB", (9 * (w + 2), 6 * (hh + 2)), FUNDO)
    for i, im in enumerate(fotos):
        t = im.resize((w, hh), Image.NEAREST)
        ImageDraw.Draw(t).text((3, 2), str(i), fill=(255, 220, 120), font=fonte(11))
        tira.paste(t, ((i % 9) * (w + 2), (i // 9) * (hh + 2)))
    reduzido = Ch.quadro(0, reduzido=True).imagem().convert("RGB").crop(REC)
    montar("A forja H · o ferreiro forjando: o ritmo da R, o corpo inteiro", [
        ("os estados do ferreiro (5×, só diagnóstico), na ordem do golpe, com a duração no ciclo", poses[:5]),
        ("", poses[5:]),
        (f"o ciclo inteiro como o jogo mostrou a 1920 (53 fotos seguidas do relógio de 100 ms, à metade; "
         f"{Ch.DURACAO / 10:.1f} s; o último quadro emenda no primeiro)", [(tira, "")]),
        ("com movimento reduzido: a pose do alto, parada, o fogo parado e sem faíscas (5×)",
         [(reduzido.resize((reduzido.width * 5, reduzido.height * 5), Image.NEAREST), "")]),
    ], AQUI.parent / "folha-movimento-h.png")


if __name__ == "__main__":
    folha_forja()
    folha_estilo()
    folha_corpo()
    folha_movimento()
