"""As folhas da 1E.4 (23/10/2026), das capturas de fotografar.mjs (capturas/atual, capturas/proposta-b, -b48 e -a,
a 1920×945) e das peças de proposta/. Ampliações sempre por vizinho mais próximo (sem suavizar);
uma redução só onde a legenda diz, para caber a página inteira.

  - levantamento.png: onde o mapa aparece na campanha, o minimapa e o mapa grande em tamanho real, as peças de hoje
    (os símbolos, as estradas, as marcas e os estados) em contexto e ampliadas, e o que é de cada modo;
  - pecas.png: as peças da proposta revisada a 1× e a 4× (a cancela antes e agora, a plaqueta B, as marcas, a seta A);
  - comparacao.png: atual × B (a escolhida) × A (a alternativa), nas quatro situações da campanha, com os mesmos
    dados (o minimapa a 2× e o mapa grande a 1×);
  - origem-lugares.png: de onde vêm os ícones de lugar de 32 e 40 (a folha de referência, o recorte, as reduções);
  - presenca-lugares.png: o mapa grande com o 40 aprovado e com um 48 pelo mesmo processo (capturas/proposta-b48);
  - nativos.png: a vila e a floresta refeitas em grade nativa (32 e 48), antigo × novo, e o nome perto da borda.
    python folhas.py [nativos ...]   # sem nomes, todas
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
    f = Folha(1600)
    f.texto("1E.4 — as peças da proposta revisada (protótipo; nada no jogo)", 22, OURO, True)
    f.texto("Desenhadas à mão em grade, montadas no Aseprite em lote (fontes/, camadas corpo, marca, contorno). "
            "1:1 na tela, sobre o carvão; a 4× por vizinho mais próximo.", 14, TEXTO2)
    f.espaco()
    um = lambda n: Image.open(p / f"{n}.png").convert("RGBA")  # noqa: E731
    sp = lambda n: Image.open(CAP / f"sprites/{n}.png").convert("RGBA")  # noqa: E731
    f.texto("A cancela: a barricada de madeira envelhecida (postes e tábuas em X), no lugar da faixa vermelha e branca", 17, TEXTO, True)
    f.imagens([(nicho(sp("cancela-mini-r1"), 20, 4), "antes, minimapa, 4×"), (nicho(um("cancela-mini"), 20, 4), "agora, minimapa, 4×"),
               (nicho(um("cancela-mini"), 20, 1), "agora, minimapa, 1×"),
               (nicho(sp("cancela-r1"), 24, 4), "antes, mapa grande, 4×"), (nicho(um("cancela"), 24, 4), "agora, mapa grande, 4×"),
               (nicho(um("cancela"), 24, 1), "agora, mapa grande, 1×")], gap=16)
    f.texto("O \"você está aqui\", direção B (a escolhida): a plaqueta com a figura 16 da classe (a aprovada, de retratos.js)", 17, TEXTO, True)
    plaq, lado = um("posicao-plaqueta"), um("posicao-plaqueta-lado")
    linha = []
    for c in ["guerreiro", "mago", "arqueiro"]:
        t = plaq.copy()
        t.alpha_composite(sp(f"figura-{c}"), (2, 2))
        linha += [(nicho(t, 28, 1), f"{c}, 1×"), (nicho(t, 28, 4), f"{c}, 4× (no mapa grande vai a 2×)")]
    f.imagens(linha, gap=16)
    t = lado.copy()
    t.alpha_composite(sp("figura-arqueiro"), (2, 2))
    d = lado.transpose(Image.FLIP_LEFT_RIGHT)
    d.alpha_composite(sp("figura-arqueiro"), (4, 2))
    f.imagens([(nicho(t, 28, 4), "de lado, à esquerda do lugar (sem espaço acima), 4×"),
               (nicho(d, 28, 4), "espelhada, à direita (sem espaço à esquerda), 4×"), (nicho(t, 28, 1), "1×")], gap=16)
    f.texto("As outras marcas (como na primeira rodada) e a alternativa A, a seta, preservada", 17, TEXTO, True)
    f.imagens([(nicho(um(n), 24, 4), f"{t}, 4×") for n, t in
               [("missao", "missão, mapa grande"), ("contrato", "contrato, mapa grande"), ("missao-mini", "missão, minimapa"),
                ("contrato-mini", "contrato, minimapa"), ("posicao", "A: a seta, mapa grande"), ("posicao-mini", "A: a seta, minimapa")]], gap=16)
    f.gravar(PASTA / "pecas.png")


SITUACOES_B = SITUACOES[:2] + [("capela-tarde", "Na Capela, à tarde, com o Arqueiro (o lugar atual perto da borda de cima do mapa)")] + SITUACOES[2:]


def comparacao():
    f = Folha(2030)
    f.texto("1E.4 — atual × proposta B (a escolhida) × A (a alternativa), com os mesmos dados", 22, OURO, True)
    f.texto("O minimapa a 2× e o mapa grande a 1× (vizinho mais próximo). Proposta: a escala inteira, os ícones de lugar (32 e 40) em 1:1, "
            "as estradas por estado, a barricada na saída fechada, as marcas de missão e contrato e o herói na plaqueta. "
            "Clique, destinos e regras iguais.", 14, TEXTO2)
    f.espaco()
    for sit, desc in SITUACOES_B:
        f.texto(desc, 18, TEXTO, True)
        f.imagens([(amplia(abrir(CAP / f"{v}/{sit}-mini.png"), 2), r) for v, r in
                   [("atual", "atual (1.199.3)"), ("proposta-b", "proposta B (o herói na plaqueta)"), ("proposta-a", "alternativa A (a seta)")]], gap=20)
        f.imagens([(abrir(CAP / f"atual/{sit}-grande.png"), "atual, mapa grande"), (abrir(CAP / f"proposta-b/{sit}-grande.png"), "proposta B, mapa grande")], gap=20)
        atual = next(l for l in registro("proposta-b")[sit]["medidas"][1]["lugares"] if "atual" in l["classes"].split())["centro"]
        f.imagens([(amplia(recorte(abrir(CAP / f"{v}/{sit}-grande.png"), atual, 210, 140), 2), r) for v, r in
                   [("proposta-b", "B no lugar atual, 2×"), ("proposta-a", "A no lugar atual, 2×"), ("atual", "atual no lugar atual, 2×")]], gap=20)
    f.texto("A legenda do mapa grande (só o que o mapa conhecido mostra, e as marcas)", 18, TEXTO, True)
    for v, r in [("proposta-b", "proposta B"), ("atual", "atual: os nove desenhos dos dois modos")]:
        j = abrir(CAP / f"{v}/vau-manha-janela.png")
        f.imagens([(j.crop((0, j.height - 70, j.width, j.height)), r)], gap=20)
    f.gravar(PASTA / "comparacao.png")


def origem():
    """De onde vêm os ícones de lugar de 32 e 40: a folha de referência, o recorte, as duas reduções."""
    hud = AQUI.parents[1]
    f = Folha(1700)
    f.texto("1E.4 — a origem dos ícones de lugar de 32 e 40 (lugar-*, rpg/web/static/hud/icones/)", 22, OURO, True)
    f.texto("Refeitos pelo script preparar_hud4p.py: os 16 arquivos (8 lugares × 32 e 40) saem idênticos, byte a byte, aos do jogo.", 14, TEXTO2)
    f.espaco()
    folha = Image.open(hud / "assets4p/original/lugares-atributos-recursos.webp").convert("RGBA")
    fundo = Image.new("RGBA", folha.size, (*CARVAO, 255))
    fundo.alpha_composite(folha)
    peca = Image.open(hud / "assets4p/pecas/lugar-vila.png").convert("RGBA")
    pc = Image.new("RGBA", peca.size, (*CARVAO, 255))
    pc.alpha_composite(peca)
    f.imagens([(reduz(fundo.convert("RGB"), 0.4), "1. a referência: lugares-atributos-recursos.webp, 1122×1402 (reduzida a 40% só aqui)"),
               (pc.convert("RGB"), "2. o recorte da vila (assets4p/pecas), 265×203, 1×"),
               (amplia(pc.convert("RGB").crop((60, 40, 150, 110)), 4), "o recorte a 4×: o \"pixel\" mede 6 a 9 px e não segue uma grade")], gap=20)
    cel = []
    for lado, fat in ((32, "÷8,28"), (40, "÷6,63")):
        im = Image.open(ICONES / f"lugar-vila-{lado}.png").convert("RGBA")
        cel += [(nicho(im, lado + 8, 1), f"{lado}, 1×"), (nicho(im, lado + 8, 6), f"{lado}, 6×: redução {fat} do recorte")]
    f.imagens(cel, gap=20)
    f.linhas([
        "• A referência: uma das quatro folhas anexadas na rodada \"HUD 4 pixel\" (14/10/2026, commit 32e3823c), guardada intacta em",
        "  ferramentas/prototipos/hud/assets4p/original/. Os registros a tratam como folha anexada que imita pixel art sem grade nativa exata;",
        "  não dizem com que ferramenta foi feita. O aspecto (\"pixel\" irregular de 6 a 9 px, sem paleta fixa) é o de uma imagem gerada.",
        "• O processo (preparar_hud4p.py): recorte por região conexa, limpeza do alfa (só a franja de até 5% e os pontos soltos), a escala",
        "  do grupo dos lugares pela área visível (sem folga), e a redução \"paleta\": cada pixel é a média do bloco trocada pela cor mais",
        "  próxima que o desenho tem, com o alfa duro. Nada foi redesenhado nem retocado; não há fonte .aseprite nem grade nativa.",
        "• Cada tamanho é uma redução própria do mesmo recorte, por fator não inteiro (o 32 a ÷7,9–9,3; o 40 a ÷6,4–7,4). O 40 não é o 32",
        "  com margem nem o 32 ampliado: os dois ocupam o quadrado inteiro (a vila: 32×25 em 32, 40×31 em 40) e têm 300 a 770 cores.",
        "• O @2x de cada um também é outra redução (a 64 e a 80), não a duplicação exata.",
        "• Pela skill de itens de hoje, redução por fator não inteiro não vale como acabamento; estes entraram com a HUD 4 pixel, antes",
        "  dessa regra, e são os aprovados da família. Não redesenhei: o que fazer com eles é decisão do Jean.",
    ], 14)
    f.gravar(PASTA / "origem-lugares.png")


def presenca():
    """O tamanho dos ícones de lugar no mapa grande: o 40 (o aprovado) e o 48 (a mesma redução do mesmo recorte)."""
    f = Folha(1940)
    f.texto("1E.4 — a presença dos lugares no mapa grande: o 40 aprovado × um 48 pelo mesmo processo (proposta B)", 22, OURO, True)
    f.texto("O 48 sai do mesmo recorte pela mesma redução \"paleta\" (auxiliares/lugares48.py); é mais uma redução, não um desenho. "
            "O botão continua com 40 px; o tracejado de destino acompanha o símbolo maior.", 14, TEXTO2)
    f.espaco()
    for sit, desc in SITUACOES_B[:2]:
        f.texto(desc, 17, TEXTO, True)
        f.imagens([(abrir(CAP / f"proposta-b/{sit}-grande.png"), "40 (o aprovado)"), (abrir(CAP / f"proposta-b48/{sit}-grande.png"), "48")], gap=20)
        cs = [centro("proposta-b", sit, "mapa grande", n) for n in ["Vau do Turvo", "Bosque do Moinho"]]
        f.imagens([(amplia(recorte(abrir(CAP / f"{v}/{sit}-grande.png"), c, 120, 100), 2), f"{r}, 2×") for c in cs
                   for v, r in [("atual", "atual (sprite 16 a ×2,64)"), ("proposta-b", "40"), ("proposta-b48", "48")]], gap=14)
    f.gravar(PASTA / "presenca-lugares.png")


def nativos():
    """A vila e a floresta refeitas em grade nativa: as peças (antigo × novo, a grade e o tamanho exibido), a silhueta,
    o minimapa de dia e à noite, o mapa grande com a plaqueta B (o 40 antigo, o 32 nativo, o 48 nativo) e o nome da
    Capela perto da borda, antes e depois."""
    p = PASTA / "proposta"
    f = Folha(1960)
    f.texto("1E.4 — a vila e a floresta em grade nativa (proposta; nada no jogo)", 22, OURO, True)
    f.texto("Capturas a 1920×945 com os mesmos dados; ampliações por vizinho mais próximo. \"Antigo\": os ícones de lugar do jogo "
            "(reduções da folha de referência). \"Novo\": desenhados à mão na grade (lugares.py, fontes em camadas).", 14, TEXTO2)
    f.espaco()
    um = lambda n: Image.open(p / f"{n}.png").convert("RGBA")  # noqa: E731
    jogo = lambda n: Image.open(ICONES / f"{n}.png").convert("RGBA")  # noqa: E731

    def silhueta(im):
        s = Image.new("RGBA", im.size)
        for y in range(im.height):
            for x in range(im.width):
                if im.getpixel((x, y))[3]:
                    s.putpixel((x, y), (40, 36, 30, 255) if im.getpixel((x, y))[:3] in ((20, 12, 8), (11, 19, 13)) else (200, 190, 170, 255))
        return s
    for lugar in ("vila", "floresta"):
        f.texto(f"A {lugar}: as peças", 18, TEXTO, True)
        pecas_ = [(jogo(f"lugar-{lugar}-32"), "antigo 32: redução, sem grade; exibido 32"),
                  (um(f"lugar-{lugar}-n32"), "NOVO 32: grade 32×32; exibido 32 (minimapa)"),
                  (jogo(f"lugar-{lugar}-40"), "antigo 40: redução; exibido 40 (mapa grande)"),
                  (um(f"lugar-{lugar}-n48"), "NOVO 48: grade 48×48, à mão; exibido 48 (mapa grande)")]
        f.imagens([(nicho(im, im.width + 8, 1), t.split(":")[0] + ", 1×") for im, t in pecas_], gap=24)
        f.imagens([(nicho(im, im.width + 4, 6 if im.width <= 32 else 5), t) for im, t in pecas_], gap=18, legenda=12)
        f.imagens([(nicho(silhueta(um(f"lugar-{lugar}-n32")), 36, 4), "silhueta do novo 32, 4×"),
                   (nicho(silhueta(um(f"lugar-{lugar}-n48")), 52, 3), "silhueta do novo 48, 3×")], gap=24)
    f.texto("O minimapa (o 32 em 1:1; o mapa a ×2): antigo × novo, de dia no Vau e à noite no Bosque", 18, TEXTO, True)
    for sit in ("vau-manha", "bosque-noite"):
        f.imagens([(amplia(abrir(CAP / f"{v}/{sit}-mini.png"), 2), f"{r}, 2×") for v, r in
                   (("proposta-b", f"{sit}: antigo"), ("proposta-n32", f"{sit}: novo"))] +
                  [(abrir(CAP / f"{v}/{sit}-mini.png"), f"{r}, 1×") for v, r in (("proposta-b", "antigo"), ("proposta-n32", "novo"))], gap=20)
    f.texto("O mapa grande, com a plaqueta B: o 40 antigo × o 32 novo em 1:1 × o 48 novo (a recomendação)", 18, TEXTO, True)
    for sit in ("vau-manha", "bosque-noite"):
        cs = [centro("proposta-n48", sit, "mapa grande", n) for n in ("Vau do Turvo", "Bosque do Moinho")]
        f.imagens([(amplia(recorte(abrir(CAP / f"{v}/{sit}-grande.png"), c, 150, 120), 2), f"{r}, 2×") for c in cs
                   for v, r in (("proposta-b", "antigo 40"), ("proposta-n32", "novo 32"), ("proposta-n48", "novo 48"))], gap=10, legenda=12)
    f.imagens([(abrir(CAP / "proposta-b/vau-manha-grande.png"), "antigo 40, 1×"), (abrir(CAP / "proposta-n48/vau-manha-grande.png"), "novo 48, 1×")], gap=20)
    f.texto("O nome perto da borda: a Capela atual no minimapa (o nome procura um lugar livre: embaixo, em cima, à esquerda, à direita)", 18, TEXTO, True)
    f.imagens([(amplia(abrir(CAP / "sprites/capela-tarde-mini-antes.png"), 2), "antes (a revisão anterior): o nome invade o Bosque, 2×"),
               (amplia(abrir(CAP / "proposta-n48/capela-tarde-mini.png"), 2), "agora: nome, plaqueta e ruínas na mesma linha, 2×")], gap=20)
    f.gravar(PASTA / "nativos.png")


if __name__ == "__main__":
    import sys
    pedidas = sys.argv[1:] or ["levantamento", "pecas", "comparacao", "origem", "presenca", "nativos"]
    for nome in pedidas:
        globals()[nome]()
