"""A FOLHA COMPARATIVA do d20 (protótipo): o jogo atual, A (Marfim) e B (Vidro) lado a lado, com os mesmos dados, em
tamanho real (recortes 1:1 das capturas de fotografar.mjs; a mesma região nas três colunas de cada linha).

    python ferramentas/prototipos/hud/d20/auxiliares/folha.py      # grava folha-1920.png e folha-1280.png em ../
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
CAP = AQUI.parent / "capturas"
FONTE = "C:/Windows/Fonts/arial.ttf"
VERSOES = [("atual", "Jogo atual (1.201.0)"), ("a", "A · Marfim (a conta numa tirinha)"), ("b", "B · Vidro (frente a frente)")]
LINHAS = {
    "1920": [("sucesso", "1-giro", "Rolando: o mesmo caso, durante o giro"),
             ("sucesso", "2-resultado", "Sucesso por 1, dois dígitos (d20 11 + 2 = 13 contra 12) · teste real"),
             ("falha", "2-resultado", "Falha por 1, um dígito (d20 9 + 2 = 11 contra 12) · teste real"),
             ("critico", "2-resultado", "20 natural (22 contra 12) · teste real"),
             ("longo", "2-resultado", "Conta longa, à noite sem tocha (d20 6 + 7 = 13 contra 15) · teste real"),
             ("escuro", "2-resultado", "Bônus negativo, escuridão (d20 14 − 2 = 12 contra 12) · teste real"),
             ("sim_so1", "2-resultado", "SIMULAÇÃO: o 1 natural falha mesmo com 15 contra 12"),
             ("falha", "2-resultado-reduzido", "Movimento reduzido: a falha, no mesmo instante")],
    "1280": [("sucesso", "2-resultado", "Sucesso por 1 · teste real"),
             ("longo", "2-resultado", "Conta longa, à noite · teste real"),
             ("sim_so20", "2-resultado", "SIMULAÇÃO: o 20 natural passa com 21 contra 22")],
}


def arquivo(caso, v, janela, quadro):
    if quadro.endswith("-reduzido"):
        return CAP / f"{caso}-{v}-{janela}-reduzido-{quadro.replace('-reduzido', '')}.png"
    return CAP / f"{caso}-{v}-{janela}-{quadro}.png"


def caixas():
    """As caixas dos grupos (relatorio*.json), por caso, versão e janela."""
    c = {}
    for nome in ("relatorio.json", "relatorio-reduzido.json"):
        f = CAP / nome
        if f.exists():
            for r in json.loads(f.read_text(encoding="utf-8")):
                if "grupo" in r:
                    c[(r["caso"], r["versao"], r["janela"].split("x")[0])] = r["grupo"]
    return c


def folha(janela):
    cx = caixas()
    f1, f2 = ImageFont.truetype(FONTE, 22), ImageFont.truetype(FONTE, 16)
    blocos = []
    for caso, quadro, rotulo in LINHAS[janela]:
        gs = [cx[(caso, v, janela)] for v, _ in VERSOES if (caso, v, janela) in cx]
        x0 = max(0, min(g["x"] for g in gs) - 40); x1 = max(g["x"] + g["w"] for g in gs) + 40
        y0 = max(0, min(g["y"] for g in gs) - 30); y1 = max(g["y"] + g["h"] for g in gs) + 30
        ims = [Image.open(arquivo(caso, v, janela, quadro)).convert("RGB").crop((int(x0), int(y0), int(x1), int(y1))) for v, _ in VERSOES]
        blocos.append((rotulo, ims))
    larg = max(sum(im.width for im in ims) + 16 * 4 for _, ims in blocos)
    alt = 70 + sum(ims[0].height + 46 for _, ims in blocos)
    W = Image.new("RGB", (larg, alt), (20, 18, 16))
    d = ImageDraw.Draw(W)
    d.text((16, 14), f"O d20 a {janela} ({'1920×945' if janela == '1920' else '1280×720'}), tamanho real: o jogo atual, A e B com os mesmos dados", font=f1, fill=(242, 201, 76))
    x = 16
    for (_, nome), im in zip(VERSOES, blocos[0][1]):
        d.text((x, 44), nome, font=f2, fill=(232, 220, 190)); x += im.width + 16
    y = 70
    for rotulo, ims in blocos:
        d.text((16, y + 4), rotulo, font=f2, fill=(200, 188, 160))
        y += 26
        x = 16
        for im in ims:
            W.paste(im, (x, y)); x += im.width + 16
        y += ims[0].height + 20
    W.save(AQUI.parent / f"folha-{janela}.png")
    print(janela, W.size)


if __name__ == "__main__":
    folha("1920")
    folha("1280")
