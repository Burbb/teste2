# As folhas atual × proposta (as fotos do fotografar.mjs a 1920x945, em tamanho real) e a prancha sobre o carvão de
# cada lote da noite de 19/10/2026: bandagem_pocao, tonico_antidoto, calca_manto.
# Uso (na raiz): python <esta pasta>/montar.py <lote>
import pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
LOTE = pathlib.Path(__file__).resolve().parents[1].parent      # itens-lote-noite/
RAIZ = LOTE.parents[3]
JOGO = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
try:
    FONTE = ImageFont.truetype("arial.ttf", 13)
except OSError:
    FONTE = ImageFont.load_default()

def folha(pasta, linhas, saida, modos=("atual", "proposta")):
    """linhas: (rótulo, arquivo sem o prefixo do modo, recorte ou None). Um modo por coluna."""
    grupos = []
    for rotulo, nome, corte in linhas:
        ims = [Image.open(pasta / f"{m}-1920x945-{nome}.png").convert("RGB") for m in modos]
        if corte: ims = [i.crop(corte) for i in ims]
        grupos.append((rotulo, ims))
    w = max(i.width for _, ims in grupos for i in ims)
    h = sum(ims[0].height + 22 for _, ims in grupos)
    o = Image.new("RGB", (len(modos) * (w + 10) + 10, h + 8), (245, 245, 245)); d = ImageDraw.Draw(o); y = 4
    for rotulo, ims in grupos:
        d.text((10, y), f"{rotulo}: {' | '.join(modos)} (1920x945, tamanho real)", fill=(0, 0, 0), font=FONTE); y += 16
        for k, i in enumerate(ims): o.paste(i, (10 + k * (w + 10), y))
        y += ims[0].height + 6
    o.save(saida); print(saida, o.size)

def prancha(arquivos, saida):
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), *map(str, arquivos), "-o", str(saida)], check=True)

LOTES = {
    "bandagem_pocao": dict(
        linhas=[("topo: Poção (24) e Bandagem (24)", "topo", (600, 0, 800, 73)),
                ("a bolsa da ficha e os cartões do mercado (32)", "mercado-0", None), ("", "mercado-1", None), ("", "mercado-2", None), ("", "mercado-3", None),
                ("aviso de uma Poção ganha, numa tela (16)", "aviso-pocao_vida", None),
                ("aviso de uma Bandagem ganha (16)", "aviso-bandagem", None),
                ("chips no texto (16)", "chips", None),
                ("bolsa do Inventário (32)", "inventario", (460, 600, 660, 680)),
                ("roda da luta: o comando Itens é a Poção (32)", "luta", (260, 20, 460, 215))],
        prancha=lambda P: [P / "bandagem-16.png", P / "bandagem-24.png", P / "bandagem-32.png", JOGO / "bandagem-32.png",
                           P / "pocao-16.png", P / "pocao-24.png", P / "pocao-32.png", JOGO / "pocao-32.png"]),
    "tonico_antidoto": dict(
        linhas=[("cartões do mercado (32)", "mercado-0", None), ("", "mercado-1", None),
                ("espólio com os dois achados (32)", "espolio", None),
                ("aviso de um Tônico ganho (16)", "aviso-tonico", None), ("aviso de um Antídoto ganho (16)", "aviso-antidoto", None),
                ("chips no texto (16)", "chips", None)],
        prancha=lambda P: [P / "tonico-16.png", P / "tonico-32.png", JOGO / "tonico-32.png",
                           P / "antidoto-16.png", P / "antidoto-32.png", JOGO / "antidoto-32.png",
                           LOTE / "bandagem_pocao" / "proposta" / "pocao-32.png"]),
}

if __name__ == "__main__":
    nome = sys.argv[1]; cfg = LOTES[nome]; base = LOTE / nome
    folha(base / "capturas", cfg["linhas"], base / f"{nome}-no-jogo.png")
    prancha(cfg["prancha"](base / "proposta"), base / "prancha-carvao.png")
