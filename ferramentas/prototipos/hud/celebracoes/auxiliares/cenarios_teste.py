"""CENÁRIOS DE TESTE da etapa 2 (subida de nível, celebrações e raridade; 23/10/2026): situações possíveis pelas
regras, montadas pelos caminhos reais do motor (o quadro do espólio, `ganhar_xp`, `oferecer_equip`), com as fichas e o XP
reais dos inimigos. Não mudam balanceamento, chances de raridade, recompensas nem progressão; só põem o herói perto do
momento a fotografar. Ficam fora de tests/ (não são testes do jogo) e do jogo.

    python cenarios_teste.py nivel          # TESTE: a vitória sobre dois lobos leva do nível 1 ao 2 (habilidade nova)
    python cenarios_teste.py dois_niveis    # TESTE: o espólio da Capela (a Ilse, nível 3, e dois afogados) leva do 1 ao 3
    python cenarios_teste.py raridades      # TESTE: quatro achados seguidos, um de cada raridade (comum a lendário)
    python cenarios_teste.py nivel4         # TESTE: do 3 ao 4, o nível da encruzilhada (o aviso da especialização)
    python cenarios_teste.py sigilo         # TESTE: o Sigilo de um guardião (receber_sigilo, como no rito da Ilse)
    python cenarios_teste.py especializacao # TESTE: no nível 4, a especialização escolhida (especializar)
    python cenarios_teste.py nivel_especializacao  # TESTE (sequência para os vídeos): do 3 ao 4 e, em seguida, a
                                                   # especialização escolhida
    python cenarios_teste.py raridades_sigilo      # TESTE (sequência para os vídeos): as quatro raridades e o Sigilo
    python cenarios_teste.py limites        # SIMULAÇÃO: dados fora do jogo para testar os limites da tela (nomes e
                                            # textos longos, seis ganhos de dois dígitos); não acontece nas regras

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
from rpg.habilidades import HABILIDADES  # noqa: E402
from rpg.itens import gerar_equip  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402
from rpg.web.ponte import WebUI  # noqa: E402
from rpg.web.servidor import Servidor  # noqa: E402


def heroi(ui, niveis=0, titulo="Cenário de teste da etapa 2"):
    """A campanha no Vau, de manhã, com o herói a 5 XP do próximo nível (25 de 30 no nível 1). `niveis`: quantos níveis
    ele sobe antes de a página abrir (pelo caminho do jogo; essas festas chegam sem cerimônia)."""
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    from rpg import abertura as ab
    ab.comecar(g, False)
    g.mundo["abertura"].update(despensa="feita", caneca=False)
    g.mundo["abertura"]["vistas"] = ["combate", "V1"]
    g.periodo, g.clima = 0, "limpo"
    for _ in range(niveis):
        g.subir_nivel()
    g.j.xp = g.j.xp_proximo() - 5
    # TESTE: uma pergunta de partida, para a festa acontecer com a página aberta (a que chega antes de a página
    # conectar é reposta sem cerimônia, de propósito)
    g.menu(titulo, [("Começar o teste", True)])
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


def nivel4(ui):
    g = heroi(ui, niveis=2)
    espolio(g, [g.inimigo("lobo", nivel=3)])
    rodar(g)


def sigilo(ui):
    g = heroi(ui)
    g.receber_sigilo("pantano", "Ilse")
    rodar(g)


ESPECIALIZACAO = {"guerreiro": "paladino", "mago": "piromante", "arqueiro": "sombra"}  # sem a escolha do companheiro


def especializacao(ui):
    g = heroi(ui, niveis=3)
    g.especializar(ESPECIALIZACAO[g.j.classe])
    rodar(g)


def nivel_especializacao(ui):
    """TESTE: duas festas reais em sequência, para um vídeo só: o nível 4 (o espólio de um lobo) e a especialização."""
    g = heroi(ui, niveis=2)
    espolio(g, [g.inimigo("lobo", nivel=3)])
    g.fechar_espolio()  # o quadro e o nível agora, como depois de uma luta; a especialização vem em seguida
    g.especializar(ESPECIALIZACAO[g.j.classe])
    rodar(g)


def raridades_sigilo(ui):
    """TESTE: os quatro achados e o Sigilo em sequência, para um vídeo só."""
    g = heroi(ui)
    rng = random.Random(9)
    for rar in ("comum", "magico", "raro", "lendario"):
        g.oferecer_equip(gerar_equip(rng, g.j.classe, 3, raridade=rar))
    g.receber_sigilo("pantano", "Ilse")
    rodar(g)


def limites(ui):
    """SIMULAÇÃO (não acontece nas regras): a festa e o achado com textos no limite, para ver a tela aguentar."""
    g = heroi(ui, titulo="SIMULAÇÃO de limites (dados fora das regras)")
    g.ui.celebrar("nivel", {"nivel": 12, "pontos": 3, "especializacao": True,
                            "ganhos": {"Vida": 14, g.j.nome_recurso: 11, "Ataque": 12, "Defesa": 10, "Agilidade": 10, "Poder": 13},
                            "habilidades": [{"nome": "Lâmina do Juramento Partido", "desc": "Golpe de 180% de dano que, se acertar um inimigo sangrando, espalha o sangramento para os vizinhos e devolve 15% do dano como vida."},
                                            {"nome": "Grito da Muralha Antiga", "desc": "Por 3 turnos, os aliados recebem 25% menos dano e você atrai os ataques."}]})
    it = gerar_equip(random.Random(4), g.j.classe, 3, raridade="lendario")
    it["nome"] = "Égide Rachada do Último Guardião das Margens do Turvo"
    g.oferecer_equip(it)
    rodar(g)


CENARIOS = {"nivel": nivel, "dois_niveis": dois_niveis, "raridades": raridades, "nivel4": nivel4, "sigilo": sigilo,
            "especializacao": especializacao, "limites": limites, "nivel_especializacao": nivel_especializacao,
            "raridades_sigilo": raridades_sigilo}
PROTOTIPOS = pathlib.Path(__file__).resolve().parents[1]
TROCADOS = {"telas/celebracoes.js": "celebracoes.js", "telas/achado.js": "achado.js"}


def com_icones(ui):
    """PROTÓTIPO (só neste servidor de teste): a festa do nível e a da especialização levam o ícone de cada habilidade
    nova, o mesmo do Grimório (HABILIDADES[...]["icone"]). O evento do jogo só manda nome e descrição, e a página ainda
    tem o estado de antes do nível; na integração, o campo entra no motor (progressao.py)."""
    original = ui.celebrar
    icones = {h["nome"]: h.get("icone") for h in HABILIDADES.values()}

    def celebrar(tipo, dados=None, *a, **k):
        if tipo in ("nivel", "spec") and dados:
            dados = {**dados, "habilidades": [{**x, "icone": icones.get(x["nome"])} for x in dados.get("habilidades", [])]}
        return original(tipo, dados, *a, **k)
    ui.celebrar = celebrar


def demonstracao(srv, nome):
    """Só na demonstração: as cópias da proposta no lugar das telas do jogo (PROTOTIPO=1) e a faixa do painel no canto
    da página (PAINEL). Troca o método de arquivos do servidor deste processo; nada é gravado no jogo."""
    # PROTOTIPO=1 (ou "brilho"): a primeira proposta (../prototipo/); o nome de uma direção da segunda rodada:
    # ../prototipo-v2/<direção>/ (montada por montar_v2.py)
    qual, painel = os.environ.get("PROTOTIPO", ""), os.environ.get("PAINEL")
    proposta = bool(qual)
    pasta = PROTOTIPOS / ("prototipo" if qual in ("1", "brilho") else f"prototipo-v2/{qual}")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo

    def _arquivo(self, relativo):
        if proposta and relativo in TROCADOS:
            return self._responder(200, (pasta / TROCADOS[relativo]).read_bytes(), "text/javascript; charset=utf-8")
        if painel and relativo == "index.html":
            pagina = (pathlib.Path(sys.modules[Servidor.__module__].PASTA) / "index.html").read_text(encoding="utf-8")
            versao = os.environ.get("ROTULO") or ("proposta (protótipo)" if proposta else "jogo atual")
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
    com_icones(ui)
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, nome)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=CENARIOS[nome], args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
