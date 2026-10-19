# junta as fotos de fotografar.mjs (moeda, tocha) em folhas atual × proposta, em tamanho real (1×), e a prancha dos
# arquivos da proposta sobre o carvão. Uso (na raiz): python <esta pasta>/montar.py
import pathlib, shutil, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont
AQUI = pathlib.Path(__file__).resolve().parents[1]
RAIZ = AQUI.parents[4]

try:
    FONTE = ImageFont.truetype("arial.ttf", 13)
except OSError:
    FONTE = ImageFont.load_default()

def folha(pasta, linhas, saida):
    """linhas: (rótulo, arquivo sem o prefixo do modo, recorte ou None). Atual à esquerda, proposta à direita."""
    pares = []
    for rotulo, nome, corte in linhas:
        a, p = (Image.open(pasta / f"{m}-1920x945-{nome}.png").convert("RGB") for m in ("atual", "proposta"))
        if corte: a, p = a.crop(corte), p.crop(corte)
        pares.append((rotulo, a, p))
    w = max(a.width for _, a, _ in pares)
    h = sum(a.height + 22 for _, a, _ in pares)
    o = Image.new("RGB", (2 * w + 30, h + 8), (245, 245, 245)); d = ImageDraw.Draw(o); y = 4
    for rotulo, a, p in pares:
        d.text((10, y), f"{rotulo}: atual | proposta (1920x945, tamanho real)", fill=(0, 0, 0), font=FONTE); y += 16
        o.paste(a, (10, y)); o.paste(p, (w + 20, y)); y += a.height + 6
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
          ("bolsa do Inventário (32)", "inventario", (460, 600, 660, 680))], AQUI / "tocha-no-jogo.png")
P = AQUI / "proposta"; J = RAIZ / "rpg" / "web" / "static" / "hud" / "icones"
with tempfile.TemporaryDirectory() as tmp:                    # o atual com outro nome, para a prancha distinguir
    atual = {n: pathlib.Path(tmp) / f"atual-{n}" for n in ("tocha-24.png", "tocha-32.png")}
    for n, d in atual.items(): shutil.copy(J / n, d)
    subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "arte" / "prancha.py"), str(P / "moeda-16.png"), str(P / "moeda-32.png"),
                    str(J / "moedas-24.png"), str(atual["tocha-24.png"]), str(P / "tocha-24.png"), str(atual["tocha-32.png"]), str(P / "tocha-32.png"),
                    "-o", str(AQUI / "prancha-carvao.png")], check=True)
