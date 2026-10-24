"""CENÁRIOS DE TESTE da etapa 2 (subida de nível, celebrações e raridade; 23/10/2026): situações possíveis pelas
regras, montadas pelos caminhos reais do motor (o quadro do espólio, `ganhar_xp`, `oferecer_equip`), com as fichas e o XP
reais dos inimigos. Não mudam balanceamento, chances de raridade, recompensas nem progressão; só põem o herói perto do
momento a fotografar. Ficam fora de tests/ (não são testes do jogo) e do jogo.

    python cenarios_teste.py nivel          # TESTE: a vitória sobre dois lobos leva do nível 1 ao 2 (habilidade nova)
    python cenarios_teste.py dois_niveis    # TESTE: o espólio da Capela (a Ilse, nível 3, e dois afogados) leva do 1 ao 3
    python cenarios_teste.py raridades      # TESTE: quatro achados seguidos, um de cada raridade (comum a lendário)

CLASSE (guerreiro, mago, arqueiro). Imprime o endereço na primeira linha, como tests/navegador/cenarios.py.
Para a demonstração (demo.py): PROTOTIPO=1 serve as cópias de ../prototipo/ no lugar de telas/celebracoes.js e
telas/achado.js (só neste servidor de teste; o jogo não muda) e PAINEL=<endereço> põe no canto da página os atalhos
de volta ao painel e de repetir o cenário.
"""
import os
import random
import sys
import tempfile
import threading
import time
import html
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5]))
from rpg.inimigos import instanciar_guardiao  # noqa: E402
from rpg.itens import gerar_equip  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402
from rpg.web.ponte import WebUI  # noqa: E402
from rpg.web.servidor import Servidor  # noqa: E402


def heroi(ui):
    """A campanha no Vau, de manhã, com o herói a 25 de 30 XP do nível 1 (falta pouco para o 2)."""
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    from rpg import abertura as ab
    ab.comecar(g, False)
    g.mundo["abertura"].update(despensa="feita", caneca=False)
    g.mundo["abertura"]["vistas"] = ["combate", "V1"]
    g.periodo, g.clima = 0, "limpo"
    g.j.xp = 25
    # TESTE: uma pergunta de partida, para a festa acontecer com a página aberta (a que chega antes de a página
    # conectar é reposta sem cerimônia, de propósito)
    g.menu("Cenário de teste da etapa 2", [("Começar o teste", True)])
    return g


def espolio(g, inimigos, consumiveis=()):
    """O quadro do espólio de uma vitória sobre `inimigos` (o ouro e o XP deles, como a luta daria) e o que se achou."""
    g.abrir_espolio()
    g.ganhar_ouro(sum(e.ouro for e in inimigos), fonte="lutas")
    g.ganhar_xp(sum(e.xp for e in inimigos))
    for item, qtd in consumiveis:
        g.dar(item, qtd)


def rodar(g):
    try:
        g.rodar()
    except FimDeJogo:
        pass


def nivel(ui):
    g = heroi(ui)
    espolio(g, [g.inimigo("lobo", nivel=1) for _ in range(2)])
    rodar(g)


def dois_niveis(ui):
    g = heroi(ui)
    ilse = instanciar_guardiao({"id": "ilse", "nome": "Ilse"}, 3)
    espolio(g, [ilse] + [g.inimigo("afogado", nivel=3) for _ in range(2)], consumiveis=[("bandagem", 1)])
    rodar(g)


def raridades(ui):
    g = heroi(ui)
    rng = random.Random(9)
    for rar in ("comum", "magico", "raro", "lendario"):
        g.oferecer_equip(gerar_equip(rng, g.j.classe, 3, raridade=rar))
    rodar(g)


CENARIOS = {"nivel": nivel, "dois_niveis": dois_niveis, "raridades": raridades}
PROTOTIPO = pathlib.Path(__file__).resolve().parents[1] / "prototipo"
TROCADOS = {"telas/celebracoes.js": "celebracoes.js", "telas/achado.js": "achado.js"}


def demonstracao(srv, nome):
    """Só na demonstração: as cópias da proposta no lugar das telas do jogo (PROTOTIPO=1) e a faixa do painel no canto
    da página (PAINEL). Troca o método de arquivos do servidor deste processo; nada é gravado no jogo."""
    proposta, painel = bool(os.environ.get("PROTOTIPO")), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo

    def _arquivo(self, relativo):
        if proposta and relativo in TROCADOS:
            return self._responder(200, (PROTOTIPO / TROCADOS[relativo]).read_bytes(), "text/javascript; charset=utf-8")
        if painel and relativo == "index.html":
            pagina = (pathlib.Path(sys.modules[Servidor.__module__].PASTA) / "index.html").read_text(encoding="utf-8")
            versao = "proposta (protótipo)" if proposta else "jogo atual"
            repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
            faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                     f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                     f'Demonstração: {html.escape(nome)} · {versao} · '
                     f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                     f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
            return self._responder(200, pagina.replace("</body>", faixa + "</body>").encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "nivel"
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, nome)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=CENARIOS[nome], args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
