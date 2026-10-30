"""Demonstração do interior da taverna (protótipo: a G, o balcão de perto, a composição escolhida, e a G refinada;
como histórico, a H e, do salão panorâmico, a prova de qualidade, o M1 e as candidatas da F à A; nada disto entra no
jogo).

    python ferramentas/prototipos/taverna/demo.py      (ou dois cliques em demo.bat)

Abre o jogo de sempre num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados):
o Guerreiro no Vau, com a campanha começada. Entre na taverna pelo prédio da vila. Só nesta execução:

- diante da taverna, a vista mostra o interior no lugar da vila aproximada, como o templo faz no jogo desde a 1.219.0
  (o motor manda a cena em estado.local.interiores; aqui, `cena_taverna` entra nessa lista); o balcão é o de sempre,
  com os cartões que já existem (dormir, a bebida e os rumores, a despensa e o homem do canto da abertura);
- os pontos da cena levam a esses cartões: o Taverneiro à bebida, a Escada ao Dormir, a Despensa (só enquanto ela
  espera) ao Descer à despensa, o Homem do canto (só enquanto o cartão existe) ao Sentar com ele; a Saída volta à vila.
  O motor manda todos; a cena à vista mostra só os que ela desenha (a G, a G2 e a H: o Taverneiro e a Despensa). Para um ponto
  levar a um cartão certo, a demonstração serve o telas/cenas.js com `servicos: "<serviço>"` aceito (no jogo,
  `servicos: true` leva ao primeiro cartão) e com os pontos filtrados pela cena (`cenas_js`);
- Morel aparece no canto do salão (as candidatas antigas) só quando `morel_no_canto` diz (abaixo); recrutado, não está
  lá; a G, a G2 e a H não mostram o canto;
- o botão Protótipo, na barra do alto, troca entre a G refinada (o padrão), a G original, a H, a prova de qualidade (a B4 e o Morel M1, com a A, a
  B, a B2, a B3 e o canto da F para comparar e a vista isolada) e as candidatas da F à A, o estado do save temporário
  e liga a pose parada; o botão diz as versões à vista.

**O encontro à mesa de Morel** (30/10/2026): o evento de sempre (`morel_na_taverna`, pelo cartão "Sentar com o homem do
canto" da abertura ou pela bebida, com as condições dele) abre a vista diante de Morel no lugar do balcão, com as opções
do evento embaixo; nada do evento muda (os textos, os preços, os testes, as consequências). `a_mesa` só manda a cena ao
começar e de novo quando o ouro sai de fato (`perder_ouro`, a cobrança do motor): é isso que lança as moedas na mesa,
uma vez por pagamento. Terminado o evento, o balcão da taverna continua aberto (a meta `balcao`, como o templo faz) até
o Voltar à vila. Os casos de teste da faixa (o ouro, o dado da queda de braço, Morel na próxima bebida) só valem quando
as regras do evento já deixam.

A porta é `DEMO_PORTA` (padrão 8795: não usa a 8791 do jogo, a 8793 da curandeira nem a 8794 do templo)."""
import os
import random
import sys
import tempfile
import threading
import time
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)

from rpg import abertura  # noqa: E402
from rpg import comitiva as cm  # noqa: E402
from rpg import missoes  # noqa: E402

TELA = os.path.join(AQUI, "tela")
CAMADAS = os.path.join(AQUI, "camadas")


# ------------------------------------------------------------------ o que o motor mandaria
def morel_no_canto(g):
    """Morel come no canto enquanto ainda pode ser encontrado ali: livre (fora da comitiva), com o evento da taverna
    ainda possível (`morel_na_taverna` acontece até 3 vezes, a partir do dia 2) ou com a abertura esperando por ele (no
    dia 1, ele assiste à luta da despensa). Proposta para o Jean avaliar; no jogo, a regra moraria no motor."""
    vezes = g.contagem.get(abertura.MOREL, 0)
    return cm.disponivel(g, "morel") and vezes < 3 and (g.dia >= 2 or abertura.morel_esperando(g))


def cena_taverna(g):
    """Os pontos da taverna: cada um leva a um cartão que já existe; a Despensa e o Homem do canto só com o cartão."""
    a = abertura.estado(g) or {}
    pontos = [
        {"id": "taverneiro", "nome": "Taverneiro", "faz": "uma bebida e os rumores", "estado": "O taverneiro, atrás do balcão.",
         "servicos": "rumores"},
        {"id": "escada", "nome": "Escada", "faz": "dormir até o amanhecer", "estado": "A escada para os quartos.",
         "servicos": "dormir"},
    ]
    if a.get("despensa") == "adiada":
        pontos.append({"id": "despensa", "nome": "Despensa", "faz": "descer à despensa",
                       "estado": "A porta da despensa.", "servicos": "despensa"})
    if a.get("despensa") == "feita" and abertura.morel_esperando(g):
        pontos.append({"id": "morel", "nome": "Homem do canto", "faz": "sentar com ele",
                       "estado": "Um homem grande come sozinho no canto.", "servicos": "morel"})
    pontos.append({"id": "saida", "nome": "Saída", "faz": "voltar à vila", "estado": "A porta para a rua.",
                   "acao": {"local": "voltar"}})
    return {"cena": "taverna", "titulo": "A taverna", "pagina": True, "morel": morel_no_canto(g), "pontos": pontos}


# ------------------------------------------------------------------ o encontro à mesa de Morel
def mesa_de_morel(g):
    """A vista diante de Morel durante o evento dele: sem pontos (as escolhas são as do evento, embaixo). Conhecido é
    quem já tinha falado com ele antes desta vez (o evento já contou esta)."""
    conhecido = g.contagem.get(abertura.MOREL, 0) > 1
    return {"cena": "taverna_mesa", "pagina": False, "pontos": [], "pagamentos": 0,
            "titulo": "A mesa de Morel" if conhecido else "A mesa do homem do canto"}


def a_mesa(fn):
    """O evento de Morel com a vista da mesa: a cena ao começar e, a cada ouro que o motor cobra de fato, a mesma cena
    com mais um pagamento (a tela lança as moedas uma vez por pagamento; repetir a mensagem não lança de novo). Ao
    terminar, o balcão da taverna continua aberto."""
    def evento(g):
        d = mesa_de_morel(g)
        g.ui.painel("cena", dict(d))
        cobrar = g.perder_ouro

        def perder_ouro(n, destino="eventos"):
            pago = cobrar(n, destino)
            if pago:
                d["pagamentos"] += 1
                g.ui.painel("cena", dict(d))
            return pago
        g.perder_ouro = perder_ouro
        try:
            return fn(g)
        finally:
            del g.perder_ouro
            g.tav_balcao = True
    return evento


# ------------------------------------------------------------------ os estados do save temporário
ESTADOS = ("despensa", "homem_do_canto", "pouco_ouro", "quase_sem_ouro", "conhecido", "recrutado", "sem_ouro")
DADOS = {"sorteio": None, "ganhar": 20, "perder": 1}  # o dado da queda de braço (só nela; 20 e 1 decidem sozinhos)


def estado(g, qual):
    """O estado da faixa: o ponto da abertura, Morel no canto ou na comitiva, e o ouro."""
    a = abertura.estado(g)
    m = cm.membro(g, "morel")
    if m and qual != "recrutado":
        g.comitiva.remove(m)
    g.contagem.pop(abertura.MOREL, None)
    g.historico.pop(abertura.MOREL, None)  # conhecido há tempo: o intervalo do evento já passou
    g.j.ouro, g.dia = 60, 1
    g.tav_balcao = False
    a["despensa"], a["caneca"] = "feita", False
    if qual == "despensa":                     # a despensa adiada; Morel no canto, esperando a luta
        a["despensa"] = "adiada"
    elif qual in ("homem_do_canto", "pouco_ouro", "quase_sem_ouro"):  # a primeira caneca e o homem do canto
        a["caneca"] = True
        g.j.ouro = {"pouco_ouro": 30, "quase_sem_ouro": 10}.get(qual, 60)  # 30: só os 25; 10: nem os 25
    elif qual in ("conhecido", "sem_ouro"):    # já falou com Morel e recusou; ele continua no canto
        g.contagem[abertura.MOREL] = 1
        g.dia = 3
        if qual == "sem_ouro":
            g.j.ouro = 0
    elif qual == "recrutado":
        g.contagem[abertura.MOREL] = 1
        cm.recrutar(g, "morel")


class _Trocar(Exception):
    """A faixa trocou o estado: o menu da vila acaba esta volta e o jogo o monta de novo, com os cartões de agora."""


def ativar():
    """O interior da taverna na lista do motor, o evento de Morel à mesa dele e o menu da vila com as trocas de estado
    e os casos de teste da faixa."""
    from rpg.eventos import motor
    from rpg.jogo import Jogo
    from rpg.web import estado as mod_estado
    interiores0 = mod_estado.interiores

    def interiores(g):
        r = interiores0(g)
        if g.loc["tipo"] == "vila":
            r["taverna"] = cena_taverna(g)
        return r
    mod_estado.interiores = interiores
    ev = next(e for e in motor.REGISTRO if e.id == abertura.MOREL)
    ev.fn = a_mesa(ev.fn)

    # O dado da queda de braço (caso de teste): só no teste de Força do evento de Morel, e o resto da conta é a do motor
    # (o modificador, a dificuldade, a rolagem na tela). Um 20 vence e um 1 perde, como em qualquer teste.
    teste0 = Jogo.teste

    def teste(self, attr, cd):
        d = getattr(self, "tav_dado", None)
        if not d or attr != "forca" or self.evento_atual != abertura.MOREL:
            return teste0(self, attr, cd)
        sortear = self.rng.randint
        self.rng.randint = lambda a, b: d
        try:
            return teste0(self, attr, cd)
        finally:
            self.rng.randint = sortear
    Jogo.teste = teste

    # Morel na próxima bebida (caso de teste): só quando o evento é candidato agora (a condição, o intervalo, as três
    # vezes); a chance de a bebida virar evento e o sorteio entre os eventos da taverna é que ficam de fora.
    rumores0 = Jogo.ouvir_rumores

    def ouvir_rumores(self):
        if not (getattr(self, "tav_bebida_morel", False)
                and any(e.id == abertura.MOREL for e, _ in motor.candidatos(self, "taverna"))):
            return rumores0(self)
        self.forcados.insert(0, abertura.MOREL)
        self.chance = lambda p: True
        try:
            return rumores0(self)
        finally:
            del self.chance
            if abertura.MOREL in self.forcados:  # a bebida não chegou ao sorteio (sem ouro, os fregueses já contaram tudo)
                self.forcados.remove(abertura.MOREL)
    Jogo.ouvir_rumores = ouvir_rumores
    original = Jogo.menu_vila

    def menu_vila(self):
        menu0 = self.menu

        def menu(pergunta, opcoes, *a, **k):
            extra = [(f"Estado: {e}", ("__tav", e), {"tav_estado": e}) for e in ESTADOS]
            extra += [(f"Dado: {e}", ("__dado", e), {"tav_dado": e}) for e in DADOS]
            extra += [(f"Bebida: {e}", ("__bebida", e), {"tav_bebida": e}) for e in ("morel", "sorteio")]
            if getattr(self, "tav_balcao", False):  # depois da mesa de Morel, o balcão continua aberto (como o templo)
                extra.append(("Voltar à vila", ("__balcao",), {"voltar": True, "lugar": True, "balcao": "taverna"}))
            opcoes = list(opcoes)
            esc = menu0(pergunta, opcoes + extra, *a, **k)
            if isinstance(esc, tuple) and esc and esc[0] == "__tav":
                estado(self, esc[1])
                raise _Trocar
            if isinstance(esc, tuple) and esc and esc[0] == "__dado":
                self.tav_dado = DADOS[esc[1]]
                raise _Trocar
            if isinstance(esc, tuple) and esc and esc[0] == "__bebida":
                self.tav_bebida_morel = esc[1] == "morel"
                raise _Trocar
            if isinstance(esc, tuple) and esc and esc[0] == "__balcao":
                self.tav_balcao = False
                raise _Trocar
            meta = next((o[2] for o in opcoes if o and len(o) > 2 and o[1] == esc), None) or {}
            if meta.get("predio") != "taverna" or meta.get("servico") == "dormir":
                self.tav_balcao = False  # saiu da taverna por outro caminho (outro prédio, dormir)
            return esc
        self.menu = menu
        try:
            return original(self)
        except _Trocar:
            return None
        finally:
            del self.menu
    Jogo.menu_vila = menu_vila


def preparar(g):
    missoes.registro(g, "febre_do_turvo")["cenas"].append("abertura")
    if abertura.estado(g) is None:
        abertura.comecar(g, False)
    loc = next(lo for lo in g.mundo["locais"] if lo["chave"] == "vau_do_turvo")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 0, "limpo"
    estado(g, "homem_do_canto")


def rodar(ui, pasta):
    from rpg.jogo import FimDeJogo, Jogo
    from rpg.ui import BotUI
    g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    preparar(g)
    g.ui, ui.jogo = ui, g
    try:
        g.rodar()
    except FimDeJogo:
        pass


# ------------------------------------------------------------------ o servidor
def cenas_js(texto):
    """O telas/cenas.js do jogo com a taverna registrada, `servicos: "<serviço>"` aceito (o ponto leva àquele cartão) e
    os pontos da taverna filtrados pela candidata à vista."""
    a = "    templo: window.CenaTemplo,\n"
    assert a in texto
    texto = texto.replace(a, a + "    // a taverna (protótipo): ferramentas/prototipos/taverna/tela/cena-taverna.js\n"
                                 "    taverna: window.CenaTaverna,\n"
                                 "    // a mesa de Morel durante o evento dele: uma cena à parte, que a volta da vila não\n"
                                 "    // tira (o vila.js tira os interiores quando aparece outro menu)\n"
                                 "    taverna_mesa: window.CenaTavernaMorel,\n")
    b = '        const cartoes = [...document.querySelectorAll("#folha .servico")];\n'
    assert b in texto
    texto = texto.replace(b, '        const cartoes = [...document.querySelectorAll("#folha .servico")]\n'
                             '          .filter((c) => typeof p.servicos !== "string" || c.dataset.servico === p.servicos);\n')
    # a candidata à vista decide quais pontos existem (a G não desenha a escada, a porta da rua nem Morel): o ponto que
    # a cena não tem não aparece. A lista inteira do motor fica guardada (`todos`), para a troca de vista pelo painel
    # filtrar de novo a partir dela. No jogo, o motor mandaria só os pontos da cena integrada.
    c = "    if (!def) { limpar(); return; }\n"
    assert c in texto
    return texto.replace(c, c + '    if (d.cena === "taverna") { const todos = d.todos || d.pontos; '
                                'd = Object.assign({}, d, { todos, pontos: todos.filter((p) => def.pontos[p.id]) }); }\n')


def servir():
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from rpg.web import servidor as mod_srv
    ativar()
    pasta = tempfile.mkdtemp(prefix="taverna-")
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, porta=int(os.environ.get("DEMO_PORTA", "8795")),
                   config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    Handler = srv.httpd.RequestHandlerClass
    get = Handler.do_GET

    def do_GET(self):  # o jogo de sempre, com a cena da taverna registrada e a faixa da demonstração
        caminho = self.path.split("?")[0]
        if caminho in ("/", "/index.html"):
            with open(os.path.join(mod_srv.PASTA, "index.html"), encoding="utf-8") as f:
                html = f.read()
            a = '<script src="/static/telas/cenas.js"></script>'
            assert a in html
            html = html.replace(a, '<script src="/proto-tav/cena-taverna.js"></script>\n'
                                   '<script src="/proto-tav/cena-taverna-b.js"></script>\n'
                                   '<script src="/proto-tav/cena-taverna-prova.js"></script>\n'
                                   '<script src="/proto-tav/cena-taverna-anim.js"></script>\n'
                                   '<script src="/proto-tav/cenas.js"></script>')
            html = html.replace("</head>", '<link rel="stylesheet" href="/proto-tav/taverna.css">\n</head>')
            html = html.replace("</body>", '<script src="/proto-tav/faixa.js"></script>\n'
                                           '<script src="/proto-tav/balcao.js"></script>\n'
                                           '<script src="/proto-tav/rolagem-queda.js"></script></body>')
            return self._responder(200, html.encode("utf-8"), "text/html; charset=utf-8")
        if caminho == "/proto-tav/cenas.js":
            with open(os.path.join(mod_srv.PASTA, "telas", "cenas.js"), encoding="utf-8") as f:
                return self._responder(200, cenas_js(f.read()).encode("utf-8"), "text/javascript; charset=utf-8")
        if caminho.startswith("/proto-tav/"):
            nome = caminho[len("/proto-tav/"):]
            base = CAMADAS if nome.startswith("camadas/") else TELA
            resto = nome[len("camadas/"):] if base == CAMADAS else nome
            arq = os.path.normpath(os.path.join(base, resto))
            if not arq.startswith(base + os.sep) or not os.path.isfile(arq):
                return self._responder(404)
            tipo = ("image/png" if arq.endswith(".png") else "text/css; charset=utf-8" if arq.endswith(".css")
                    else "application/json" if arq.endswith(".json") else "text/javascript; charset=utf-8")
            with open(arq, "rb") as f:
                return self._responder(200, f.read(), tipo)
        return get(self)
    Handler.do_GET = do_GET
    srv.iniciar()
    print(srv.url, flush=True)
    print(f"Saves temporários em {pasta}", flush=True)
    threading.Thread(target=rodar, args=(ui, pasta), daemon=True).start()
    if not os.environ.get("SEM_NAVEGADOR"):
        webbrowser.open(srv.url)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    servir()
