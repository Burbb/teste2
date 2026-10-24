"""CENÁRIOS DAS FAIXAS DE PASSAGEM (protótipo, 24/10/2026; nada no jogo). Cada caso é o jogo de verdade numa
campanha de teste (os saves numa pasta temporária): a página abre, um clique em "Começar" e o motor faz o
acontecimento pelo caminho de sempre (a luta, a exaustão, a saída da capela, a chegada à comitiva). O que vem antes
de a página abrir chega sem animação ("replay"), por isso tudo começa depois do clique.

    python cenarios_faixas.py <caso>        # sobe o servidor e imprime o endereço na primeira linha

PROPOSTA=a ou b põe faixas.css e faixas.js do protótipo depois de telas/celebracoes.js (vazia: as faixas de hoje);
PAINEL=<endereço> põe a faixa da demonstração no canto. Nada é gravado no jogo.
"""
import html
import os
import pathlib
import random
import sys
import tempfile
import threading
import time

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ))
PROTO = pathlib.Path(__file__).resolve().parents[1]

from rpg import abertura as ab  # noqa: E402
from rpg import comitiva as cm  # noqa: E402
from rpg import missoes  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402
from tests.navegador.cenarios import lutar, vestir_arma  # noqa: E402

# id: (rótulo, o que fazer na página)
CASOS = {
    "vitoria": ("Vitória comum: uma luta curta contra um lobo", "Começar, e Atacar"),
    "sequencia": ("A sequência: o lobo guardião (o quinto lobo) → Guardião derrotado → Mestre caçador → espólio → achado → nível",
                  "Começar, e Atacar; depois o quadro, o achado e o nível"),
    "queda": ("Você caiu: a luta perdida e o resgate", "Começar, e Atacar"),
    "comitiva": ("Quem se junta à comitiva (Irmã Odette, o nome longo)", "Começar"),
    "exausto_mato": ("Exausto no mato (\"Não dá para seguir: é preciso acampar.\")", "Começar"),
    "exausto_vila": ("Exausto na vila (o pouso, \"Noite no feno...\")", "Começar"),
    "exausto_capela": ("Exausto dentro da capela (a saída exausta, o texto do caminho)", "Começar"),
    "saindo": ("Saindo da capela (do fundo: o texto mais longo, 155 letras)", "Sair e acampar"),
}
ROTULOS = {"": "as faixas de hoje", "a": "A · faixa integrada ao palco", "b": "B · emblema e anúncio"}
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".png": "image/png"}


def campanha(ui, lugar="vau_do_turvo", classe="guerreiro"):
    """Uma campanha de teste sem a abertura guiada, no `lugar`, de manhã."""
    g = Jogo(ui, seed=5, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", classe, "turvo")
    ab.comecar(g, False)
    g.mundo["abertura"].update(despensa="feita", caneca=False)
    g.contagem["morel_na_taverna"] = 1
    missoes.registro(g, "febre_do_turvo").update(cenas=["abertura"])
    for l in g.mundo["locais"]:
        l["visitado"] = l["chave"] in ("vau_do_turvo", "charco_dos_juncos", "bosque_do_moinho", lugar)
    g.mundo["atual"] = next(l["id"] for l in g.mundo["locais"] if l["chave"] == lugar)
    g.periodo, g.clima = 0, "limpo"
    vestir_arma(g)
    return g


def comecar(g, frase):
    g.ui.cena(g.loc["nome"], g.contexto_cena(), "evento")
    g.ui.escolher(frase, ["Começar"])


def rodar(g):
    try:
        g.rodar()
    except FimDeJogo:
        pass


def caso_vitoria(ui):
    g = campanha(ui, "bosque_do_moinho")
    comecar(g, "Um lobo sai do mato. Uma luta curta (Atacar).")
    e = g.inimigo("lobo", nivel=1)
    e.hp = e.max_hp = 1
    lutar(g, [e])
    rodar(g)


def caso_sequencia(ui):
    """O lobo guardião (um chefe: sempre deixa equipamento e baú), o quinto lobo do Bestiário (o mestre caçador) e o
    herói a 1 XP de subir: Guardião derrotado → Mestre caçador → o quadro do espólio → o achado → a subida de nível."""
    g = campanha(ui, "bosque_do_moinho")
    g.bestiario["lobo"] = {"vistos": 4, "abates": 4}
    g.j.xp = g.j.xp_proximo() - 1
    comecar(g, "O lobo guardião do bosque (Atacar). Depois: o quadro, o achado e o nível.")
    e = g.inimigo("lobo", nivel=2)
    e.hp = e.max_hp = 1
    e.chefe = True
    lutar(g, [e])
    rodar(g)


def caso_queda(ui):
    g = campanha(ui, "bosque_do_moinho")
    g.j.hp = 1
    comecar(g, "Um lobo enorme, e você por um fio (Atacar).")
    e = g.inimigo("lobo", nivel=6)
    e.hp = e.max_hp = 400
    lutar(g, [e])
    rodar(g)


def caso_comitiva(ui):
    g = campanha(ui)
    comecar(g, "Irmã Odette pede para seguir com você.")
    cm.recrutar(g, "odete")
    rodar(g)


def _exausto(ui, lugar, sala=None):
    g = campanha(ui, lugar, "arqueiro")
    if sala:
        missoes.registro(g, "febre_do_turvo").update(etapa="sacristia", cenas=["abertura", "capela_exterior"], sala=sala,
                                                     pistas=["agua_do_leste", "represa", "canal_da_capela", "agua_da_capela"])
    g.dia = 5
    comecar(g, "A noite passou sem você dormir.")
    g.periodo = 4  # a próxima tela é a da exaustão
    rodar(g)


def caso_exausto_mato(ui):
    _exausto(ui, "charco_dos_juncos")


def caso_exausto_vila(ui):
    _exausto(ui, "vau_do_turvo")


def caso_exausto_capela(ui):
    _exausto(ui, "capela_afogada", "salao")


def caso_saindo(ui):
    from tests.navegador.cenarios import capela
    os.environ.update(ETAPA="fundo", SALA="fundo")  # do fundo: a frase da saída mais longa
    capela(ui)


CENARIOS = {"vitoria": caso_vitoria, "sequencia": caso_sequencia, "queda": caso_queda, "comitiva": caso_comitiva,
            "exausto_mato": caso_exausto_mato, "exausto_vila": caso_exausto_vila,
            "exausto_capela": caso_exausto_capela, "saindo": caso_saindo}


def demonstracao(srv, caso):
    """Só neste servidor: os arquivos do protótipo em /static/prototipo-faixas/ e, com PROPOSTA, a página com eles."""
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-faixas/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<script src="/static/telas/celebracoes.js"></script>'
                assert marca in pagina, "index.html mudou: não achei telas/celebracoes.js"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-faixas/faixas.css">\n'
                                        '<script src="/static/prototipo-faixas/faixas.js"></script>\n'
                                        f'<script>FaixasProto.usar({proposta!r});</script>')
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Faixas: {html.escape(CASOS[caso][0])} · {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    caso = sys.argv[1] if len(sys.argv) > 1 else "vitoria"
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    random.seed(1)
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, caso)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=CENARIOS[caso], args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
