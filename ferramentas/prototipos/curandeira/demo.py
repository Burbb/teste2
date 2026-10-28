"""Demonstração da candidata A do interior da curandeira (protótipo; nada disto entra no jogo).

    python ferramentas/prototipos/curandeira/demo.py      (ou dois cliques em demo.bat)

Abre o jogo de sempre num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados):
o Guerreiro no Vau, com a campanha começada, um corte e uma mordida para tratar e 120 de ouro. Entre na curandeira
pelo prédio da vila. Só nesta execução:

- a cabana ganha o ambiente (o quadro de cima, pelo sistema das cenas, como a forja): `cena_curandeira` descreve a
  cena para a tela (quem atende pela história, a água da fonte, os dois pontos) e `tela/cena-curandeira.js` desenha
  as camadas de `camadas/` (exportadas por `exportar.py`);
- o serviço é o de produção (`Servicos.curandeiro`), sem mudar: os cartões, os preços, quem atende e o que diz;
- a faixa do alto troca o estado da história no save temporário (Pita com Marta de cama; Pita na noite da água
  escura; Marta de pé), liga o movimento reduzido para ver a pose parada e mostra, para comparar, a moagem da
  terceira passada (`anterior/terceira`) ou a segunda passada inteira (`anterior/camadas`).

A porta é `DEMO_PORTA` (padrão 8793: não usa a 8791 do jogo nem a da demonstração da forja)."""
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

from rpg import consequencias, missoes  # noqa: E402
from rpg.sistemas.servicos import Servicos  # noqa: E402

# ------------------------------------------------------------------ a cena (o que o motor diria à tela)
ESTADOS = {  # o estado da história no save temporário: (desfecho da missão, dias desde o desfecho)
    "pita": (None, None),             # a chegada: a febre, Marta de cama, Pita mói ervas no lugar dela
    "pita_escura": ("destruida", 0),  # a noite em que a fonte corre escura: Pita ferve água para os doentes
    "marta": ("descansada", 3),       # a água limpou: Marta de pé, atendendo
}
NOMES = {"pita": "Pita (Marta de cama)", "pita_escura": "Pita (a água escura)", "marta": "Marta (de pé)"}


def cena_curandeira(g):
    """A cabana para a interface gráfica: quem atende (pela história: Pita enquanto Marta está de cama; Marta depois
    que a água limpa), a água da fonte (na noite escura, os baldes e a fervura forte) e os dois pontos. Quem atende leva
    aos cartões do tratamento; a Saída é o Voltar do menu."""
    marta = consequencias.marta_de_pe(g)
    escura = consequencias.estado_fonte(g) == "escura"
    nome = "Marta" if marta else "Pita"
    return {"cena": "curandeira", "titulo": "A curandeira", "pagina": True, "quem": "marta" if marta else "pita",
            "agua": "escura" if escura else None, "pontos": [
                {"id": "curandeira", "nome": nome, "faz": "tratar os ferimentos",
                 "estado": "Marta, no almofariz." if marta else "Pita, no almofariz.", "servicos": True},
                {"id": "saida", "nome": "Saída", "faz": "voltar à vila", "estado": "A porta para a rua do Vau.",
                 "acao": {"voltar": True}},
            ]}


def mudar_estado(g, estado):
    desfecho, dias = ESTADOS[estado]
    m = missoes.registro(g, consequencias.MISSAO)
    m["desfecho"] = desfecho
    m["dia_desfecho"] = None if dias is None else g.dia - dias


class _Trocar(Exception):
    """A faixa trocou o estado: a cabana se abre de novo, com quem atende agora."""


def ativar():
    """A cabana com o ambiente e a troca de estado, por cima do serviço de produção (que não muda)."""
    original = Servicos.curandeiro

    def curandeiro(self):
        ui = self.ui
        cena0 = ui.cena

        def cena(titulo, *a, **k):
            cena0(titulo, *a, **k)
            if titulo == "A curandeira":
                ui.painel("cena", cena_curandeira(self))

        def menu(pergunta, opcoes, *a, **k):
            extra = [(f"Estado: {NOMES[e]}", ("__estado", e), {"cur_estado": e}) for e in ESTADOS]
            esc = type(self).menu(self, pergunta, list(opcoes) + extra, *a, **k)
            if isinstance(esc, tuple) and esc and esc[0] == "__estado":
                mudar_estado(self, esc[1])
                raise _Trocar
            return esc
        ui.cena, self.menu = cena, menu
        try:
            while True:
                try:
                    return original(self)
                except _Trocar:
                    continue
        finally:
            del ui.cena
            del self.menu
    Servicos.curandeiro = curandeiro


# ------------------------------------------------------------------ o save temporário
def preparar(g):
    from rpg import sobrevivencia
    missoes.registro(g, "febre_do_turvo")["cenas"].append("abertura")
    g.marcar("templo_gratis_usado")
    g.marcar("curandeira_gratis_usado")
    g.j.nivel = 2
    g.j.ouro = 120
    for fid in ("corte", "mordida"):
        sobrevivencia.ferir(g, fid)
    g.j.recalcular()
    g.j.hp = g.j.max_hp
    loc = next(lo for lo in g.mundo["locais"] if lo["chave"] == "vau_do_turvo")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 0, "limpo"
    mudar_estado(g, os.environ.get("ESTADO", "pita"))


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
TELA = os.path.join(AQUI, "tela")
CAMADAS = os.path.join(AQUI, "camadas")
ANTERIOR = os.path.join(AQUI, "anterior")  # as passadas anteriores, guardadas para comparar (só leitura)


def servir():
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from rpg.web import servidor as mod_srv
    ativar()
    pasta = tempfile.mkdtemp(prefix="curandeira-")
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, porta=int(os.environ.get("DEMO_PORTA", "8793")),
                   config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    Handler = srv.httpd.RequestHandlerClass
    get = Handler.do_GET

    def do_GET(self):  # o jogo de sempre, com a cena da cabana e a faixa da demonstração
        caminho = self.path.split("?")[0]
        if caminho in ("/", "/index.html"):
            with open(os.path.join(mod_srv.PASTA, "index.html"), encoding="utf-8") as f:
                html = f.read()
            html = html.replace('<script src="/static/telas/cenas.js"></script>',
                                '<script src="/proto-cur/cena-curandeira.js"></script>\n'
                                '<script src="/static/telas/cenas.js"></script>')
            html = html.replace("</head>", '<link rel="stylesheet" href="/proto-cur/curandeira.css">\n</head>')
            html = html.replace("</body>", '<script src="/proto-cur/faixa.js"></script></body>')
            return self._responder(200, html.encode("utf-8"), "text/html; charset=utf-8")
        if caminho == "/static/telas/cenas.js":  # a cena "curandeira" registrada ao lado da forja
            with open(os.path.join(mod_srv.PASTA, "telas", "cenas.js"), encoding="utf-8") as f:
                js = f.read()
            js = js.replace("    forja: window.CenaForja,\n",
                            "    forja: window.CenaForja,\n    curandeira: window.CenaCurandeira,  // a demonstração\n")
            return self._responder(200, js.encode("utf-8"), "text/javascript; charset=utf-8")
        if caminho.startswith("/proto-cur/"):
            nome = caminho[len("/proto-cur/"):]
            pasta, _, resto = nome.partition("/")
            base = {"camadas": CAMADAS, "anterior": ANTERIOR}.get(pasta)
            if base is None:
                base, resto = TELA, nome
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
