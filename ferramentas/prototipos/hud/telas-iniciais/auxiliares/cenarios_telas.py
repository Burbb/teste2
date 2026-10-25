"""CENÁRIO DAS TELAS INICIAIS (protótipo, 24/10/2026; nada no jogo). O título com dois saves numa pasta temporária (um
da campanha e um do mundo gerado, que não abre mais: o cenário `campanha` dos testes), para ver o título, a lista de
saves e a criação do personagem. Os seus saves não são tocados.

    python cenarios_telas.py        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=r2: a candidata refinada, a criação em etapas (criacao-r2.css e criacao-r2.js): uma pergunta só do motor
("criacao", criacao_em_etapas) com tudo o que a tela mostra; a tela anda por Nome, Classe e Modo e devolve as escolhas
juntas no "Começar campanha". O nucleo.js servido ganha a pergunta nova; o arquivo do jogo não muda.
PROPOSTA=r: a criação em cartões (criacao.css e criacao.js do protótipo). Só neste processo, a criação manda os dados
de cada classe e de cada modo junto da opção (o que o motor faria na integração: `meta` com a classe, o recurso, as
especializações, a frase) e não escreve mais a lista das classes no texto; os textos são os de hoje. Vazia: hoje.
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
ROTULOS = {"": "a criação de hoje", "r": "R · a criação em cartões", "r2": "R2 · a criação em etapas (a candidata)"}


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
            self.ui.caixa = {"id": "tutorial", "rotulo": "Mostrar tutorial", "marcada": True,
                             "pergunta": "Mostrar as orientações do tutorial?"}
            try:
                modo = self.menu("Se você cair (em combate, de fome ou de infecção):", [
                    ("Resgate", "resgate", {"modo": "resgate",
                                            "nota": "Alguém da vila te encontra e cuida de você (perde parte do ouro e dois dias)"}),
                    ("Hardcore", "hardcore", {"modo": "hardcore", "nota": "A morte é permanente e o save é apagado"}),
                    ("Voltar", None, {"voltar": True}),
                ])
                tutorial = self.ui.ler_caixa() if modo else None
            finally:
                self.ui.caixa = None
            if modo:
                break
        self.hardcore = modo == "hardcore"
        self.iniciar(nome, classe, regiao)
        abertura.comecar(self, tutorial)
        self.introducao_campanha()
        return True

    Jogo.novo_jogo = novo_jogo


# R2: as frases curtas de cada classe (como a classe joga), tiradas da `desc` de CLASSES sem a parte que a linha do
# ataque e a do recurso já dizem. Na integração, um campo da classe em classes.py.
FRASES = {
    "guerreiro": "Muita vida e defesa: aguenta o tranco.",
    "arqueiro": "Ágil e preciso, ótimo contra voadores. As flechas podem acabar.",
    "mago": "Frágil, mas devastador: magias elementais exploram fraquezas.",
}
ALCANCE = {"corpo": "corpo a corpo", "distancia": "à distância"}


def dados_da_criacao(regiao):
    """Tudo o que a criação mostra, pronto do motor (a tela só desenha): o nome, as classes, os modos e o tutorial."""
    from rpg import balanceamento as bal
    from rpg import campanha
    from rpg.classes import CLASSES, SPECS
    classes = []
    for c, d in CLASSES.items():
        classes.append({
            "id": c, "nome": d["nome"], "frase": FRASES[c],
            "ataque": {"nome": d["ataque"][0], "alcance": ALCANCE[d["ataque"][1]], "icone": d["icone_ataque"]},
            "recurso": {"nome": d["recurso"], "total": d["base"]["max_rec"], "regen": d["base"]["regen"]},
            "specs": [SPECS[s]["nome"] for s in d["specs"]], "nivel_spec": bal.NIVEL_ESPECIALIZACAO,
        })
    return {
        "regiao": campanha.nome(regiao),
        "nome": {"pergunta": "Qual é o seu nome, aventureiro(a)?", "padrao": "Aventureiro", "max": 40},
        "classes": classes,
        "modo": {"pergunta": "Se você cair (em combate, de fome ou de infecção):", "padrao": "resgate", "opcoes": [
            {"id": "resgate", "nome": "Resgate", "linhas": ["Alguém da vila te encontra e cuida de você.",
                                                            "Custa parte do ouro e dois dias."]},
            {"id": "hardcore", "nome": "Hardcore", "linhas": ["A morte é permanente.", "O save é apagado."]},
        ]},
        "tutorial": {"rotulo": "Mostrar tutorial", "marcada": True,
                     "nota": "Orientações curtas nas primeiras ações. A Ajuda (F1) desliga ou religa."},
    }


def criacao_em_etapas():
    """R2: a criação é uma pergunta só ("criacao"), com os dados de `dados_da_criacao`; a tela anda pelas etapas (Nome,
    Classe, Modo) e devolve tudo junto quando a pessoa aperta "Começar campanha" ({"nome", "classe", "modo",
    "tutorial"}), ou {"voltar": true} na primeira etapa. O motor confere e começa como hoje. A interface de texto
    continua com as perguntas de sempre."""
    from rpg import abertura, campanha
    from rpg.classes import CLASSES
    from rpg.jogo import Jogo
    from rpg.web.ponte import WebUI
    original = Jogo.novo_jogo

    def novo_jogo(self, regiao=campanha.INICIO):
        if not isinstance(self.ui, WebUI):
            return original(self, regiao)
        dados = dados_da_criacao(regiao)
        modos = {o["id"] for o in dados["modo"]["opcoes"]}
        while True:
            r = self.ui._perguntar("criacao", **dados)
            if isinstance(r, dict) and r.get("voltar"):
                self.ui.escolhas_na_cena += 1
                return False
            if isinstance(r, dict) and r.get("classe") in CLASSES and r.get("modo") in modos:
                break
        nome = str(r.get("nome") or "").strip()[:dados["nome"]["max"]] or dados["nome"]["padrao"]
        self.ui.escolhas_na_cena += 1
        # só da demonstração: o que o motor recebeu, para o roteiro de conferência (criacao_r2.mjs) ler
        print(f"[criacao] nome={nome!r} classe={r['classe']} modo={r['modo']} tutorial={bool(r.get('tutorial', True))}",
              file=sys.stderr, flush=True)
        self.hardcore = r["modo"] == "hardcore"
        self.iniciar(nome, r["classe"], regiao)
        abertura.comecar(self, bool(r.get("tutorial", True)))
        self.introducao_campanha()
        return True

    Jogo.novo_jogo = novo_jogo


# R2: o nucleo.js servido com a pergunta "criacao" (o arquivo do jogo não muda)
NUCLEO_TRATAR = "  switch (m.t) {\n    case \"estado\":"
NUCLEO_PERGUNTA = "    case \"pergunta\": Gesto.novaTela();"


def demonstracao(srv):
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo == "app/nucleo.js" and proposta == "r2":
            js = (pasta / "app" / "nucleo.js").read_text(encoding="utf-8")
            assert NUCLEO_TRATAR in js and NUCLEO_PERGUNTA in js, "nucleo.js mudou: não achei o switch de tratar"
            js = js.replace(NUCLEO_TRATAR, '  if (typeof CriacaoR2 !== "undefined") CriacaoR2.aoMensagem(m);\n' + NUCLEO_TRATAR)
            js = js.replace(NUCLEO_PERGUNTA, '    case "criacao": Gesto.novaTela(); CriacaoR2.mostrar(m); break;\n' + NUCLEO_PERGUNTA)
            return self._responder(200, js.encode("utf-8"), TIPOS[".js"])
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
                arq = "criacao" if proposta == "r" else "criacao-r2"
                pagina = pagina.replace(marca, marca + f'\n<link rel="stylesheet" href="/static/prototipo-telas/{arq}.css">')
                pagina = pagina.replace("</body>", f'<script src="/static/prototipo-telas/{arq}.js"></script></body>')
                pagina = pagina.replace("<html", f'<html data-telas="{proposta}"', 1)
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Telas iniciais: {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    if os.environ.get("PROPOSTA") == "r":
        criacao_em_cartoes()
    elif os.environ.get("PROPOSTA") == "r2":
        criacao_em_etapas()
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
