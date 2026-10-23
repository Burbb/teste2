"""As folhas da 1E.4 (23/10/2026), das capturas de fotografar.mjs (capturas/atual, capturas/proposta-a e
capturas/proposta-b, a 1920×945) e das peças de proposta/. Ampliações sempre por vizinho mais próximo (sem suavizar);
uma redução só onde a legenda diz, para caber a página inteira.

  - levantamento.png: onde o mapa aparece na campanha, o minimapa e o mapa grande em tamanho real, as peças de hoje
    (os símbolos, as estradas, as marcas e os estados) em contexto e ampliadas, e o que é de cada modo;
  - pecas.png: as peças novas a 1× e a 4×, ao lado dos ícones aprovados de 32 e 40 com que convivem;
  - comparacao.png: atual × direção A × direção B, nas três situações da campanha, com os mesmos dados (o minimapa a
    2× e o mapa grande a 1×).
    python folhas.py
"""
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
PASTA = AQUI.parent
RAIZ = AQUI.parents[4]
ICONES = RAIZ / "rpg/web/static/hud/icones"
CAP = PASTA / "capturas"
FUNDO, CARVAO, TEXTO, TEXTO2, OURO, AVISO, BOM = ((13, 11, 10), (26, 23, 20), (214, 210, 200), (150, 144, 134),
                                                (232, 190, 80), (236, 120, 96), (130, 200, 120))
SITUACOES = [("vau-manha", "No Vau, de manhã (Charco e Bosque visitados; Capela e Estrada de Varn só conhecidas; "
                           "missão no Vau, contrato no Bosque)"),
             ("bosque-noite", "No Bosque, à noite (a Capela a um trecho, com a missão)"),
             ("praca-tudo", "Depois da praça (tudo visitado menos a Estrada de Varn, fechada)")]


def fonte(t=15, negrito=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if negrito else "arial.ttf", t)
    except OSError:
        return ImageFont.load_default()


def amplia(im, f):
    return im.resize((im.width * f, im.height * f), Image.NEAREST)


def reduz(im, f):
    """Só para caber a página inteira numa folha (a legenda avisa); nunca é o tamanho de avaliação."""
    return im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)


def abrir(p):
    return Image.open(p).convert("RGB")


def registro(pasta):
    return json.loads((CAP / pasta / "registro.json").read_text(encoding="utf-8"))


def centro(pasta, sit, onde, lugar):
    m = next(m for m in registro(pasta)[sit]["medidas"] if m["onde"] == onde)
    return next(l["centro"] for l in m["lugares"] if l["rotulo"].startswith(lugar))


def recorte(im, c, w, h):
    x, y = c
    return im.crop((x - w // 2, y - h // 2, x - w // 2 + w, y - h // 2 + h))


class Folha:
    def __init__(self, largura):
        self.l, self.y, self.itens = largura, 0, []

    def texto(self, t, tam=15, cor=TEXTO, negrito=False, x=24, passo=None):
        self.itens.append(("t", x, self.y, t, tam, cor, negrito))
        self.y += passo or tam + 8

    def linhas(self, ts, tam=14, cor=TEXTO, x=24):
        for t in ts:
            self.texto(t, tam, cor, x=x, passo=tam + 6)

    def imagens(self, lista, x=24, gap=18, legenda=13):
        """Uma fileira de (imagem, legenda); a legenda vai em cima."""
        alto = max(im.height for im, _ in lista)
        for im, leg in lista:
            if leg:
                self.itens.append(("t", x, self.y, leg, legenda, TEXTO2, False))
            self.itens.append(("i", x, self.y + legenda + 6, im))
            x += max(im.width, round(fonte(legenda).getlength(leg or "")) + 4) + gap
        self.y += alto + legenda + 6 + 22

    def espaco(self, n=14):
        self.y += n

    def gravar(self, caminho):
        img = Image.new("RGB", (self.l, self.y + 20), FUNDO)
        d = ImageDraw.Draw(img)
        for it in self.itens:
            if it[0] == "t":
                _, x, y, t, tam, cor, neg = it
                d.text((x, y), t, fill=cor, font=fonte(tam, neg))
            else:
                _, x, y, im = it
                img.paste(im, (x, y))
        img.save(caminho)
        print(caminho.name, img.size)


def nicho(im, lado, f=1, cor=CARVAO):
    """A peça num quadrado de carvão (como fica sobre o mapa escuro), a 1× ou ampliada f×."""
    q = Image.new("RGB", (lado, lado), cor)
    q.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2), im)
    return amplia(q, f)


def levantamento():
    f = Folha(1980)
    f.texto("1E.4 — levantamento do mapa e do minimapa da campanha (produção 1.199.3, 23/10/2026)", 24, OURO, True)
    f.texto("Capturas a 1920×945 (a janela principal). Ampliações por vizinho mais próximo, sem suavizar. "
            "O desenho do mapa é rpg/web/static/mapa.js (MapaPx), o mesmo nos dois modos.", 14, TEXTO2)
    f.espaco()
    f.texto("1. Onde aparece: o minimapa no painel do mundo (sempre à vista) e o mapa grande (M ou o atalho Mapa)", 18, TEXTO, True)
    f.imagens([(reduz(abrir(CAP / "atual/vau-manha-pagina.png"), 0.5), "a página no Vau (reduzida a 50%, só para caber)"),
               (reduz(abrir(CAP / "atual/vau-manha-mapa.png"), 0.5), "o mapa grande aberto (reduzido a 50%)")])
    f.texto("2. Em tamanho real (1×) e o minimapa a 3×", 18, TEXTO, True)
    mini = abrir(CAP / "atual/vau-manha-mini.png")
    f.imagens([(abrir(CAP / "atual/vau-manha-mundo.png").crop((0, 0, 330, 360)), "o painel do mundo, 1×"),
               (amplia(mini, 3), "o minimapa a 3×: canvas 224×128 exibido em 284×162 (×1,27)"),
               (abrir(CAP / "atual/bosque-noite-mini.png"), "à noite no Bosque, 1×")])
    f.imagens([(abrir(CAP / "atual/vau-manha-grande.png"), "o mapa grande, 1×: canvas 352×201 exibido em 928×530 (×2,64)"),
               (amplia(recorte(abrir(CAP / "atual/bosque-noite-grande.png"),
                               centro("atual", "bosque-noite", "mapa grande", "Bosque do Moinho"), 340, 260), 2),
                "à noite no Bosque, 2×: onde você está? (o anel some; só o nome em ouro)")])

    f.texto("3. As peças de hoje", 18, TEXTO, True)
    spr = {}
    for nome in ["vila", "pantano", "floresta", "ruinas", "planicie", "montanha", "cidadela", "covil", "vencido"]:
        spr[nome] = Image.open(CAP / f"sprites/{nome}.png").convert("RGBA")
    f.imagens([(nicho(spr[n], 20, 4), f"{n}{' (só procedural)' if n in ('montanha', 'cidadela', 'covil', 'vencido') else ''}")
               for n in spr], gap=14)
    f.texto("   ↑ os símbolos do mapa: os sprites 16×16 do jogo (sprites-dados.js), a 4×. Desenho provisório, de antes da HUD; "
            "no minimapa entram reduzidos a 14 px com suavização e depois ampliados ×1,27.", 13, TEXTO2)
    f.espaco(6)
    cm = lambda lugar: centro("atual", "vau-manha", "minimapa", lugar)  # noqa: E731
    cg = lambda lugar: centro("atual", "vau-manha", "mapa grande", lugar)  # noqa: E731
    grande = abrir(CAP / "atual/vau-manha-grande.png")
    f.imagens([(amplia(recorte(mini, cm(n), 34, 34), 4), f"{n} no minimapa, 4×") for n in
               ["Vau do Turvo", "Charco dos Juncos", "Bosque do Moinho", "Capela Afogada", "Estrada de Varn"]] +
              [(amplia(recorte(grande, cg("Capela Afogada"), 60, 50), 2), "Capela no mapa grande, 2× (×2,64 irregular)")], gap=14)
    lugares = [Image.open(ICONES / f"lugar-{n}-40.png").convert("RGBA") for n in
               ["vila", "pantano", "floresta", "ruinas", "planicie", "montanha", "cidadela", "caverna"]]
    f.imagens([(nicho(im, 44, 2), n) for im, n in zip(lugares, ["vila 40", "pântano 40", "floresta 40", "ruínas 40",
                                                                 "planície 40", "montanha 40", "cidadela 40", "caverna 40 (covil)"])], gap=12)
    f.texto("   ↑ os ícones de lugar APROVADOS da família da HUD (lugar-*-32/40, assets4c), a 2×: hoje só na lista de Caminhos. "
            "O mapa e a lista mostram o mesmo lugar com dois desenhos.", 13, TEXTO2)
    f.espaco(6)
    vau, bosque, capela, varn = (cg(n) for n in ["Vau do Turvo", "Bosque do Moinho", "Capela Afogada", "Estrada de Varn"])
    meio = lambda a, b: ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)  # noqa: E731
    f.imagens([(amplia(recorte(grande, meio(vau, bosque), 70, 40), 4), "que sai daqui (ouro), 4×"),
               (amplia(recorte(grande, meio(bosque, capela), 70, 40), 4), "só conhecida (pontilhada escura), 4×"),
               (amplia(recorte(grande, meio(vau, varn), 50, 50), 4), "para a saída fechada (igual às outras), 4×"),
               (amplia(recorte(abrir(CAP / "atual/praca-tudo-grande.png"),
                               meio(*(centro("atual", "praca-tudo", "mapa grande", n) for n in ["Bosque do Moinho", "Capela Afogada"])),
                               70, 40), 4), "percorrida (bege), 4×")], gap=14)
    f.imagens([(amplia(recorte(mini, cm("Vau do Turvo"), 40, 40), 4), "missão no Vau: o \"!\" de texto, solto no canto do botão"),
               (amplia(recorte(mini, cm("Bosque do Moinho"), 40, 40), 4), "contrato no Bosque: o mesmo \"!\"; o destino clicável"),
               (amplia(recorte(mini, cm("Estrada de Varn"), 40, 40), 4), "Estrada de Varn: fechada, mas com o convite de viagem")], gap=14)

    f.texto("4. O que o levantamento achou (detalhes no LEIA-ME)", 18, TEXTO, True)
    f.linhas([
        "DEFEITOS DE LEITURA",
        " • Posição do jogador: não há marca permanente. O anel de \"você está aqui\" cresce e some (1,5 s); na foto e em boa parte do tempo, só o nome",
        "   em ouro diz onde você está. No minimapa só o nome do lugar atual aparece, e à noite no Bosque ele cai ao lado do quadrado do Vau.",
        " • Escala fracionária: ×1,27 no minimapa e ×2,64 no mapa grande. Pixels de larguras diferentes nas estradas, no pontilhado e nos símbolos.",
        " • Símbolos borrados no minimapa: o sprite de 16 desenhado em 14 com suavização, depois ampliado. A Capela e a Estrada de Varn quase somem.",
        " • Estradas: atravessam o símbolo; a só conhecida (Bosque→Capela) quase não aparece no escuro; a saída fechada parece um destino aberto",
        "   (estrada em ouro, quadrado tracejado de \"clique para viajar\"), e só o texto diz que está fechada.",
        " • Missão e contrato com a mesma marca \"!\" (texto de 11/14 px numa caixa de ouro), presa ao canto do botão e não do desenho.",
        "PROVISÓRIOS (não aprovados): os nove sprites 16 do mapa; o traço das estradas; o \"!\" em CSS; o anel e o tracejado de destino.",
        "APROVADOS que já servem ao mapa: os ícones lugar-*-32/40 da família da HUD (a lista de Caminhos), o atalho Mapa da doca.",
        "ESTADOS QUE EXISTEM: atual (anel + nome em ouro); clicável (tracejado pulsando, 28/40 px); destacado (contorno, ao passar na lista);",
        "   conhecido não visitado (60% e névoa; nome apagado); perigo (nome vermelho se o nível ≥ o seu + 2); estrada daqui / percorrida /",
        "   conhecida; covil ativo e vencido (só procedural). NÃO EXISTEM: missão concluída no mapa (a marca some), lugar bloqueado (só no texto).",
        "TAMANHOS: minimapa 284×162 (botão 28, símbolo ~18 px); mapa grande 928×530 (botão 40, símbolo ~42 px); legenda 16; Diário e opções de",
        "   viagem com o sprite 16. Sem zoom: o quadro se ajusta aos lugares conhecidos (enquadrar), o mesmo nos dois tamanhos com 5 lugares.",
        "COMPARTILHAMENTOS: MapaPx desenha o minimapa, o mapa grande e o mapa na página; MapaPx.sprite escolhe o desenho também na lista de",
        "   Caminhos (Icones.lugar), no Diário (missão e contrato), nas opções de viagem e na legenda. Tudo vale igual para o procedural.",
    ], 14)
    f.espaco(8)
    f.linhas([
        "PRIORIDADE (frequência × problema): 1) a posição do jogador; 2) os caminhos (escala, estados, a saída fechada); 3) os símbolos dos",
        "   lugares (trocar pela família aprovada); 4) as marcas de missão e contrato. Depois: o Diário e as opções de viagem com o mesmo",
        "   desenho, a legenda só com o que existe, a missão concluída e o perigo também no símbolo.",
        "DEPENDÊNCIAS DO PROCEDURAL: o covil (ativo e vencido) e a cidadela só existem lá, junto da \"selada\" na descrição; a legenda lista os",
        "   nove desenhos dos dois modos; MapaPx.sprite cai no bioma para o tipo \"saida\" da campanha (planície). Ao retirar o procedural,",
        "   o covil, a cidadela, o vencido, a legenda fixa e GLIFO_TIPO/BIOMA (mapa.py, a interface de texto) saem ou mudam juntos; a",
        "   campanha precisa de um desenho e de um estado próprios para a saída (o \"fechado\" ainda não chega à tela como campo).",
    ], 14, OURO)
    f.gravar(PASTA / "levantamento.png")


def pecas():
    p = PASTA / "proposta"
    f = Folha(1500)
    f.texto("1E.4 — as peças novas do primeiro lote (proposta; nada no jogo)", 22, OURO, True)
    f.texto("Desenhadas à mão em grade, montadas no Aseprite em lote (fontes/, camadas corpo, marca, contorno). "
            "1:1 na tela, sobre o carvão; a 4× por vizinho mais próximo.", 14, TEXTO2)
    f.espaco()
    pares = [("posicao", "você está aqui (A)"), ("missao", "missão"), ("contrato", "contrato"), ("cancela", "saída fechada")]
    viz40 = Image.open(ICONES / "lugar-vila-40.png").convert("RGBA")
    viz32 = Image.open(ICONES / "lugar-vila-32.png").convert("RGBA")
    f.texto("Mapa grande (ao lado do ícone de lugar de 40)", 17, TEXTO, True)
    f.imagens([(nicho(viz40, 48, 1), "vila 40")] + [(nicho(Image.open(p / f"{n}.png").convert("RGBA"), 24, 1), t) for n, t in pares] +
              [(nicho(viz40, 48, 4), "vila 40, 4×")] + [(nicho(Image.open(p / f"{n}.png").convert("RGBA"), 24, 4), f"{t}, 4×") for n, t in pares], gap=16)
    f.texto("Minimapa (ao lado do ícone de lugar de 32)", 17, TEXTO, True)
    f.imagens([(nicho(viz32, 40, 1), "vila 32")] + [(nicho(Image.open(p / f"{n}-mini.png").convert("RGBA"), 18, 1), t) for n, t in pares] +
              [(nicho(viz32, 40, 4), "vila 32, 4×")] + [(nicho(Image.open(p / f"{n}-mini.png").convert("RGBA"), 18, 4), f"{t}, 4×") for n, t in pares], gap=16)
    f.texto("Direção B do \"você está aqui\": a plaqueta com a figura 16 do herói (a aprovada, de retratos.js)", 17, TEXTO, True)
    plaq = Image.open(p / "posicao-plaqueta.png").convert("RGBA")
    figs = {}
    for c in ["guerreiro", "mago", "arqueiro"]:
        figs[c] = Image.open(CAP / f"sprites/figura-{c}.png").convert("RGBA")
    linha = []
    for c, fig in figs.items():
        t = plaq.copy()
        t.alpha_composite(fig, (2, 2))
        linha += [(nicho(t, 28, 1), f"{c}, 1×"), (nicho(t, 28, 4), f"{c}, 4× (no mapa grande vai a 2×)")]
    f.imagens([(nicho(plaq, 28, 4), "a plaqueta vazia, 4×")] + linha, gap=16)
    f.gravar(PASTA / "pecas.png")


def comparacao():
    f = Folha(2030)
    f.texto("1E.4 — atual × proposta, com os mesmos dados (o minimapa a 2×; o mapa grande a 1×)", 22, OURO, True)
    f.texto("Proposta: escala inteira (×2 no minimapa, ×3 no mapa grande), os ícones aprovados de lugar (32 no minimapa, 40 no grande) "
            "em 1:1, as estradas por estado, a saída fechada, as marcas de missão e contrato e o \"você está aqui\" "
            "(A: a seta; B: o herói na plaqueta). Clique, destinos e regras iguais.", 14, TEXTO2)
    f.espaco()
    for sit, desc in SITUACOES:
        f.texto(desc, 18, TEXTO, True)
        f.imagens([(amplia(abrir(CAP / f"{v}/{sit}-mini.png"), 2), r) for v, r in
                   [("atual", "atual (1.199.3)"), ("proposta-a", "proposta, direção A (a seta)"), ("proposta-b", "proposta, direção B (o herói)")]], gap=20)
        ga, gb = abrir(CAP / f"atual/{sit}-grande.png"), abrir(CAP / f"proposta-a/{sit}-grande.png")
        f.imagens([(ga, "atual, mapa grande"), (gb, "proposta A, mapa grande")], gap=20)
        atual = next(l for l in registro("proposta-b")[sit]["medidas"][1]["lugares"] if "atual" in l["classes"].split())["centro"]
        f.imagens([(amplia(recorte(abrir(CAP / f"proposta-a/{sit}-grande.png"), atual, 200, 130), 2), "A no lugar atual, 2×"),
                   (amplia(recorte(abrir(CAP / f"proposta-b/{sit}-grande.png"), atual, 200, 130), 2), "B no lugar atual, 2×"),
                   (amplia(recorte(abrir(CAP / f"atual/{sit}-grande.png"), atual, 200, 130), 2), "atual no lugar atual, 2×")], gap=20)
    f.texto("A legenda do mapa grande na proposta (só o que o mapa conhecido mostra, e as marcas)", 18, TEXTO, True)
    janela = abrir(CAP / "proposta-a/vau-manha-janela.png")
    f.imagens([(janela.crop((0, janela.height - 70, janela.width, janela.height)), "proposta A"),
               ], gap=20)
    jat = abrir(CAP / "atual/vau-manha-janela.png")
    f.imagens([(jat.crop((0, jat.height - 70, jat.width, jat.height)), "atual: os nove desenhos dos dois modos")], gap=20)
    f.gravar(PASTA / "comparacao.png")


if __name__ == "__main__":
    levantamento()
    pecas()
    comparacao()
