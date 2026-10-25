"""CENÁRIO DAS TELAS INICIAIS (protótipo, 24/10/2026; nada no jogo). O título com dois saves numa pasta temporária (um
da campanha e um do mundo gerado, que não abre mais: o cenário `campanha` dos testes), para ver o título, a lista de
saves e a criação do personagem. Os seus saves não são tocados.

    python cenarios_telas.py        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=r2 ou vazia: o jogo como está (desde a 1.208.0, a criação em etapas, R2: rpg/criacao.py, app/criacao.js,
24-criacao.css). Os arquivos criacao-r2.* ficam como o registro da candidata; a troca do motor que ela usava no
protótipo está no histórico do git.
PROPOSTA=r: a criação em cartões (criacao.css e criacao.js do protótipo). Só neste processo, a criação manda os dados
de cada classe e de cada modo junto da opção (o que o motor faria na integração: `meta` com a classe, o recurso, as
especializações, a frase) e não escreve mais a lista das classes no texto; os textos são os de antes. Desde a 1.208.0
a tela gráfica não tem mais a caixa marcável: a R mostra o modo sem a caixa do tutorial (que fica ligado); o registro
dela é a folha.
PAINEL=<endereço> põe a faixa da demonstração no canto.
"""
import html
import os
import pathlib
import sys
import threading
import time

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ))
PROTO = pathlib.Path(__file__).resolve().parents[1]
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}
ROTULOS = {"": "a criação de hoje", "r": "R · a criação em cartões", "r2": "R2 · a criação em etapas (no jogo desde a 1.208.0)"}


def criacao_em_cartoes():
    """Jogo.novo_jogo com os dados de cada opção no `meta` (o texto das classes sai da página: os cartões o mostram)."""
    from rpg import abertura, campanha
    from rpg import balanceamento as bal
    from rpg.classes import CLASSES, SPECS
    from rpg.jogo import Jogo

    def novo_jogo(self, regiao=campanha.INICIO):
        self.ui.cena("Criação de personagem", campanha.nome(regiao), "menu")
        nome = self.ui.perguntar("Qual é o seu nome, aventureiro(a)?", "Aventureiro", voltar=True)
        if nome is None:
            return False
        self.dizer()
        self.dizer(f"Escolha sua classe. No nível {bal.NIVEL_ESPECIALIZACAO} ela se ramifica em uma de duas "
                   "especializações:", "ciano")
        classes = list(CLASSES)
        while True:
            classe = self.menu("Sua classe:", [
                (CLASSES[c]["nome"], c, {"classe": c, "recurso": CLASSES[c]["recurso"], "icone": CLASSES[c]["icone_ataque"],
                                         "specs": [SPECS[s]["nome"] for s in CLASSES[c]["specs"]], "nivel_spec": bal.NIVEL_ESPECIALIZACAO,
                                         "nota": CLASSES[c]["desc"]})
                for c in classes] + [("Voltar", None, {"voltar": True})])
            if classe is None:
                return False
            modo = self.menu("Se você cair (em combate, de fome ou de infecção):", [
                ("Resgate", "resgate", {"modo": "resgate",
                                        "nota": "Alguém da vila te encontra e cuida de você (perde parte do ouro e dois dias)"}),
                ("Hardcore", "hardcore", {"modo": "hardcore", "nota": "A morte é permanente e o save é apagado"}),
                ("Voltar", None, {"voltar": True}),
            ])
            tutorial = True
            if modo:
                break
        self.hardcore = modo == "hardcore"
        self.iniciar(nome, classe, regiao)
        abertura.comecar(self, tutorial)
        self.introducao_campanha()
        return True

    Jogo.novo_jogo = novo_jogo


def demonstracao(srv):
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    faixa_rotulo = ROTULOS[proposta]
    if proposta == "r2":  # integrada na 1.208.0: o jogo como está
        proposta = ""
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-telas/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<link rel="stylesheet" href="/static/css/23-faixas.css">'
                assert marca in pagina, "index.html mudou: não achei 23-faixas.css"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-telas/criacao.css">')
                pagina = pagina.replace("</body>", '<script src="/static/prototipo-telas/criacao.js"></script></body>')
                pagina = pagina.replace("<html", f'<html data-telas="{proposta}"', 1)
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Telas iniciais: {html.escape(faixa_rotulo)} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    if os.environ.get("PROPOSTA") == "r":
        criacao_em_cartoes()
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    from tests.navegador.cenarios import campanha
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=campanha, args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
