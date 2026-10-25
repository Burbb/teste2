"""CENÁRIO DO "CARREGAR JOGO" (protótipo, 25/10/2026; nada no jogo). O título com saves numa pasta temporária, criados
na hora pelo motor (Jogo.iniciar e salvar): os seus saves não são tocados nem lidos.

    python cenarios_saves.py        # sobe o servidor e imprime o endereço na primeira linha

CASO (os saves da pasta temporária):
    vazia   nenhum save (o título não oferece "Carregar jogo")
    uma     uma campanha (Maria, Arqueiro, nível 1, dia 1, no Vau)
    varias  dez partidas: as três classes, níveis e especializações, dias e lugares, os dois modos, uma do capítulo
            concluído, dois nomes longos, dois saves do mundo gerado (que não abrem) e um danificado
    muitas  as dez e mais doze campanhas (a lista rola)
SIMULAÇÃO: o nível, a especialização, o dia, o lugar, a etapa das missões e a data dos saves são escritos direto no
jogo antes de salvar (sem jogar até lá); o save danificado é um arquivo cortado ao meio; os do mundo gerado são o save
de uma campanha sem a `campanha` no mundo (tests/navegador/cenarios.py). Os saves são de verdade: carregam pelo jogo.

PROPOSTA=r: o "Carregar jogo" proposto (saves.css e saves.js do protótipo); a lista recebe do motor, só neste processo,
também a especialização e a missão em andamento (`resumo_do_save`, o que a integração faria em resumo_save). Vazia:
o de hoje. PAINEL=<endereço> põe a faixa da demonstração no canto.
"""
import html
import json
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
TIPOS = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8"}
ROTULOS = {"": "o Carregar jogo de hoje", "r": "R · a proposta"}
CASOS = {"vazia": "nenhum save", "uma": "uma campanha", "varias": "dez partidas (duas do mundo gerado, uma danificada)",
         "muitas": "22 partidas (a lista rola)"}
HORA = 3600
# (nome, classe, nível, especialização, dia, lugar, hardcore, etapa da Febre, capítulo concluído, há quantas horas)
VARIAS = [
    ("Maria", "arqueiro", 1, None, 1, "vau_do_turvo", False, "fonte", False, 0.02),
    ("Bento", "guerreiro", 3, None, 4, "bosque_do_moinho", False, "canal", False, 2),
    ("Iara", "mago", 5, "piromante", 9, "capela_afogada", True, "sacristia", False, 20),
    ("Teodoro", "guerreiro", 6, "paladino", 15, "vau_do_turvo", False, "retorno", True, 50),
    ("Maria da Conceição Albuquerque de Figuei", "mago", 4, "necromante", 7, "charco_dos_juncos", True, "capela", False, 30),
    ("Sebastião Valadares Montenegro", "arqueiro", 4, "sombra", 6, "estrada_de_varn", False, "capela", False, 75),
    ("Nádia", "arqueiro", 7, "patrulheiro", 21, "bosque_do_moinho", False, "fundo", False, 200),
]


def _salvar(pasta, nome, classe, nivel, spec, dia, lugar, hardcore, etapa, concluido, horas, seed):
    """Uma campanha salva pelo motor, com o progresso escrito direto (SIMULAÇÃO) e a data do arquivo recuada."""
    from rpg.jogo import Jogo
    from rpg.ui import BotUI
    g = Jogo(BotUI(random.Random(seed), max_decisoes=10), seed=seed, pasta_saves=pasta, hardcore=hardcore)
    g.iniciar(nome, classe, "turvo")
    g.j.nivel, g.j.spec, g.dia = nivel, spec, dia
    g.mundo["atual"] = next(i for i, l in enumerate(g.mundo["locais"]) if l.get("chave") == lugar)
    febre = g.mundo["missoes"]["febre_do_turvo"]
    febre["etapa"] = etapa
    if concluido:
        for m in g.mundo["missoes"].values():
            m["concluida"] = True
    g.salvar(silencioso=True)
    t = time.time() - horas * HORA
    os.utime(g.caminho_save(), (t, t))


def montar(caso):
    """A pasta temporária com os saves do caso."""
    from tests.navegador.cenarios import save_do_mundo_gerado
    pasta = tempfile.mkdtemp(prefix="saves-prototipo-")
    if caso == "vazia":
        return pasta
    linhas = VARIAS[:1] if caso == "uma" else list(VARIAS)
    if caso == "muitas":
        nomes = ["Abel", "Bia", "Caio", "Dora", "Elias", "Fia", "Gil", "Hilda", "Ivo", "Joana", "Lino", "Mira"]
        for k, n in enumerate(nomes):
            linhas.append((n, ["guerreiro", "arqueiro", "mago"][k % 3], 1 + k % 5, None, 2 + k, "vau_do_turvo", k % 4 == 0,
                           "canal", False, 300 + 24 * k))
    for k, linha in enumerate(linhas):
        _salvar(pasta, *linha, seed=10 + k)
    if caso in ("varias", "muitas"):
        for nome, classe, horas in (("Jean", "guerreiro", 400), ("Rafaela", "mago", 900)):
            caminho = save_do_mundo_gerado(pasta, nome, classe)
            t = time.time() - horas * HORA
            os.utime(caminho, (t, t))
        danificado = os.path.join(pasta, "turvo_gabriel.json")  # SIMULAÇÃO: um save cortado ao meio
        with open(os.path.join(pasta, os.listdir(pasta)[0]), encoding="utf-8") as f:
            texto = f.read()
        with open(danificado, "w", encoding="utf-8") as f:
            f.write(texto[: len(texto) // 2])
        t = time.time() - 120 * HORA
        os.utime(danificado, (t, t))
    return pasta


def resumo_do_save(caminho):
    """O resumo de hoje (resumo_save) e, só no protótipo, a especialização e a missão em andamento: o nome dela como o
    rastreador mostra (a primeira não concluída, já apresentada) ou o fim do capítulo. Na integração, em resumo_save."""
    from rpg import missoes
    from rpg.classes import SPECS
    from rpg.sistemas.persistencia import resumo_save
    r = resumo_save(caminho)
    if r.get("ilegivel") or r.get("incompativel"):
        return r
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)
    spec = d["jogador"].get("spec")
    if spec in SPECS:
        r["spec_nome"] = SPECS[spec]["nome"]
    ms = d["mundo"].get("missoes") or {}
    if ms and all(m.get("concluida") for m in ms.values()):
        r["progresso"] = "Primeiro capítulo concluído"
    else:
        for mid, m in ms.items():
            if not m.get("concluida") and missoes.MISSOES[mid]["etapas"][m["etapa"]]["objetivo"]:
                r["progresso"] = missoes.MISSOES[mid]["nome"]
                break
    return r


def demonstracao(srv, caso):
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-saves/"):
            alvo = (PROTO / relativo.split("/", 1)[1]).resolve()
            if PROTO in alvo.parents and alvo.suffix in TIPOS and alvo.is_file():
                return self._responder(200, alvo.read_bytes(), TIPOS[alvo.suffix])
            return self._responder(404, b"")
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                marca = '<link rel="stylesheet" href="/static/css/24-criacao.css">'
                assert marca in pagina, "index.html mudou: não achei 24-criacao.css"
                pagina = pagina.replace(marca, marca + '\n<link rel="stylesheet" href="/static/prototipo-saves/saves.css">')
                pagina = pagina.replace("</body>", '<script src="/static/prototipo-saves/saves.js"></script></body>')
                pagina = pagina.replace("<html", f'<html data-saves="{proposta}"', 1)
            if painel:
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Carregar jogo: {html.escape(CASOS[caso])} · {html.escape(ROTULOS[proposta])} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    import argparse
    caso = os.environ.get("CASO", "varias")
    pasta = montar(caso)
    if os.environ.get("PROPOSTA") == "r":
        import rpg.__main__ as principal
        principal.resumo_save = resumo_do_save  # só neste processo: a lista com a especialização e a missão
    from rpg.__main__ import menu_principal
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, caso)
    srv.iniciar()
    print(srv.url, flush=True)
    print(f"saves temporários em {pasta}", file=sys.stderr, flush=True)
    threading.Thread(target=menu_principal, args=(ui, argparse.Namespace(seed=1, saves=pasta)), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
