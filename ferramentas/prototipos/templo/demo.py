"""Demonstração das candidatas do interior do templo (protótipo; nada disto entra no jogo).

    python ferramentas/prototipos/templo/demo.py      (ou dois cliques em demo.bat)

Abre o jogo de sempre num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados):
o Guerreiro no Vau, com a campanha começada, a vida em 40%, Odette na comitiva, ferida, 120 de ouro e o primeiro
atendimento do templo ainda por usar. Entre no templo pelo prédio da vila. Só nesta execução:

- diante do templo, a vista mostra o interior no lugar da vila aproximada (o jogo faz isso sozinho desde a 1.219.0);
  aqui o desenho é o do protótipo, com a candidata A ou B; o balcão é o de sempre;
- a faixa do alto troca a candidata, o estado do save temporário (ferido com o primeiro atendimento; sem ouro; Odette
  ferida; ninguém precisando) e liga a pose parada.

A porta é `DEMO_PORTA` (padrão 8794: não usa a 8791 do jogo nem a 8793 da curandeira)."""
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

from rpg import comitiva as cm  # noqa: E402
from rpg import missoes  # noqa: E402

TELA = os.path.join(AQUI, "tela")
CAMADAS = os.path.join(AQUI, "camadas")


# ------------------------------------------------------------------ os estados do save temporário
def estado(g, qual):
    """O estado da faixa: quem precisa do templo e com que ouro."""
    j = g.j
    odette = cm.membro(g, "odete") or cm.recrutar(g, "odete")
    j.hp, j.ouro = j.max_hp, 120
    odette["hp"], odette["ferido"] = odette["max_hp"], False
    g.flags.pop("templo_gratis_usado", None)
    if qual in ("ferido", "sem_ouro"):
        j.hp = max(1, round(j.max_hp * 0.4))
    if qual == "sem_ouro":
        g.marcar("templo_gratis_usado")
        j.ouro = 0
    if qual == "comitiva":
        g.marcar("templo_gratis_usado")
        odette["hp"] = max(1, odette["max_hp"] // 3)


class _Trocar(Exception):
    """A faixa trocou o estado: o menu da vila acaba esta volta e o jogo o monta de novo, com os cartões de agora."""


def ativar():
    """O menu da vila com as trocas de estado da faixa (opções que a página não mostra: a faixa as pede)."""
    from rpg.jogo import Jogo
    original = Jogo.menu_vila

    def menu_vila(self):
        menu0 = self.menu

        def menu(pergunta, opcoes, *a, **k):
            extra = [(f"Estado: {e}", ("__tpl", e), {"tpl_estado": e}) for e in ("ferido", "sem_ouro", "comitiva", "ninguem")]
            esc = menu0(pergunta, list(opcoes) + extra, *a, **k)
            if isinstance(esc, tuple) and esc and esc[0] == "__tpl":
                estado(self, esc[1])
                raise _Trocar
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
    g.marcar("curandeira_gratis_usado")
    g.j.nivel = 2
    g.j.recalcular()
    loc = next(lo for lo in g.mundo["locais"] if lo["chave"] == "vau_do_turvo")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 0, "limpo"
    estado(g, "ferido")
    cm.membro(g, "odete")["hp"] = max(1, cm.membro(g, "odete")["max_hp"] // 3)


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
def servir():
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from rpg.web import servidor as mod_srv
    ativar()
    pasta = tempfile.mkdtemp(prefix="templo-")
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, porta=int(os.environ.get("DEMO_PORTA", "8794")),
                   config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    Handler = srv.httpd.RequestHandlerClass
    get = Handler.do_GET

    def do_GET(self):  # o jogo de sempre, com a cena do templo registrada e a faixa da demonstração
        caminho = self.path.split("?")[0]
        if caminho in ("/", "/index.html"):
            with open(os.path.join(mod_srv.PASTA, "index.html"), encoding="utf-8") as f:
                html = f.read()
            # o desenho do protótipo (as duas candidatas) no lugar do de produção (no jogo desde a 1.219.0)
            html = html.replace('<script src="/static/telas/cena-templo.js"></script>',
                                '<script src="/proto-tpl/cena-templo.js"></script>')
            html = html.replace("</head>", '<link rel="stylesheet" href="/proto-tpl/templo.css">\n</head>')
            html = html.replace("</body>", '<script src="/proto-tpl/faixa.js"></script></body>')
            return self._responder(200, html.encode("utf-8"), "text/html; charset=utf-8")
        if caminho.startswith("/proto-tpl/"):
            nome = caminho[len("/proto-tpl/"):]
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
