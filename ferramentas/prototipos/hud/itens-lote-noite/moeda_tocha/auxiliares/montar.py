# junta as fotos de fotografar.mjs (moeda, tocha) em folhas atual × proposta, em tamanho real (1×), e a prancha sobre o
# carvão (a moeda, já no jogo, e a tocha: o jogo, a rodada 1 e a rodada 2). Uso (na raiz): python <esta pasta>/montar.py
# (com `variantes`: só as folhas e a prancha das variantes da tocha, o 16 e a apagada, em variantes/)
import pathlib, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
AQUI = pathlib.Path(__file__).resolve().parents[1]
RAIZ = AQUI.parents[4]

try:
    FONTE = ImageFont.truetype("arial.ttf", 13)
except OSError:
    FONTE = ImageFont.load_default()

def folha(pasta, linhas, saida, modos=("atual", "proposta")):
    """linhas: (rótulo, arquivo sem o prefixo do modo, recorte ou None). Um modo por coluna, na ordem dada."""
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

M = AQUI / "capturas" / "moeda"
folha(M, [("preços do mercado (16)", "precos-cartoes", None), ("preço de um serviço, o ferreiro (16)", "servico-cartoes", None),
          ("chip de ouro no texto (16)", "chip", None), ("espólio (32)", "espolio", None),
          ("pagamento de contrato: o cartaz e os ganhos (16)", "contratos", (0, 330, 880, 529)),
          ("prêmio dos cartazes do mural (16)", "mural-cartazes", None),
          ("as moedas voando do chip ao ouro do topo, 150 ms (16, a animação do jogo)", "voo-1", (560, 60, 1100, 480)),
          ("o mesmo voo, 300 ms", "voo-2", (560, 60, 1100, 480))], AQUI / "moeda-no-jogo.png")
T = AQUI / "capturas" / "tocha"
folha(T, [("topo (24)", "topo", (440, 0, 800, 73)), ("cartão do mercado (32)", "mercado-0", None),
          ("bolsa do Inventário (32)", "inventario", (460, 600, 660, 680))], AQUI / "tocha-no-jogo.png",
      ("atual", "rodada1", "rodada2"))
V = AQUI / "variantes"
if "variantes" in sys.argv[1:]:                               # as variantes da tocha: o 16 e a apagada
    folha(V / "capturas" / "tocha16", [("aviso flutuante de um item ganho, numa tela (16)", "aviso", None),
                                       ("chip de um item ganho, no texto (16)", "chip", None),
                                       ("risco da escolha que entra na sala escura (16)", "riscos", None)], V / "tocha16-no-jogo.png")
    folha(V / "capturas" / "apagada", [("topo sem tochas (hoje o sprite em 32; a proposta em 24)", "topo", (440, 0, 800, 73)),
                                       ("risco \"Sem luz\" da escolha, sem tochas (16)", "riscos", None)], V / "apagada-no-jogo.png")
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), str(V / "proposta" / "tocha-16.png"),
                    str(RAIZ / "rpg" / "web" / "static" / "hud" / "icones" / "tocha-24.png"), str(V / "proposta" / "tocha_apagada-16.png"),
                    str(V / "proposta" / "tocha_apagada-24.png"), "-o", str(V / "prancha-carvao.png")], check=True)
    sys.exit()                                                # as folhas de antes ficam como estavam
P = AQUI / "proposta"; J = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
with tempfile.TemporaryDirectory() as tmp:                    # o atual com outro nome, para a prancha distinguir
    def copia(origem, rotulo, n):
        d = pathlib.Path(tmp) / f"{rotulo}-{n}"; shutil.copy(origem / n, d); return str(d)
    tochas = [copia(o, r, n) for n in ("tocha-24.png", "tocha-32.png") for o, r in ((J, "atual"), (AQUI / "tocha_r1" / "proposta", "rodada1"), (P, "rodada2"))]
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), str(J / "moeda-16.png"), str(J / "moeda-32.png"),
                    str(J / "moedas-24.png"), *tochas, "-o", str(AQUI / "prancha-carvao.png")], check=True)
