"""CENÁRIOS DE TESTE do d20 (etapa 2, 24/10/2026; protótipo, nada no jogo). Cada caso é um teste de verdade: o herói
num lugar selvagem do mundo gerado, Explorar (o caminho do jogo: a cena, a tocha, `eventos.disparar`) cai no baú
abandonado (`bau_abandonado`, um evento do jogo), e a escolha da pessoa leva a `Testes.teste`, que sorteia o d20, soma
o bônus e decide. A semente de cada caso foi achada por `procurar` (a mesma montagem, com uma interface que escolhe
sozinha): ela decide o d20 do motor, nada é forçado depois do sorteio. O TESTE é só pôr o herói ali (a classe, o
nível, a hora e o evento escolhidos); a tela é a do jogo, com o save numa pasta temporária.

    python cenarios_d20.py <caso>          # sobe o servidor e imprime o endereço na primeira linha
    python cenarios_d20.py procurar        # acha as sementes de cada caso (o d20 pedido) e confere as gravadas

Para a demonstração (demo.py): PROPOSTA=a ou b serve d20-dados.js, d20.js e d20.css do protótipo junto do jogo
(PROPOSTA vazia: o jogo como está); PAINEL=<endereço> põe a faixa do painel no canto da página.
"""
import html
import os
import pathlib
import sys
import tempfile
import threading
import time

RAIZ = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(RAIZ))
import rpg.eventos as eventos  # noqa: E402
from rpg.eventos.motor import disparar_id  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402
from rpg.ui import UI  # noqa: E402

PROTO = pathlib.Path(__file__).resolve().parents[1]
DISPARAR = eventos.disparar

# id: (rótulo, classe, nível, período (0 manhã, 3 noite), a escolha no baú, a semente, o d20 que ela dá)
CASOS = {
    "sucesso": ("Sucesso por 1, dois dígitos: guerreiro, Percepção, d20 11", "guerreiro", 1, 0, "Percepção", 11, 11),
    "falha": ("Falha por 1, um dígito: guerreiro, Percepção, d20 9", "guerreiro", 1, 0, "Percepção", 4, 9),
    "critico": ("Crítico: o 20 natural (sempre passa)", "guerreiro", 1, 0, "Percepção", 20, 20),
    "desastre": ("Desastre: o 1 natural (sempre falha)", "guerreiro", 1, 0, "Percepção", 12, 1),
    "forca": ("Força com bônus alto: guerreiro de nível 6, d20 15 (total 24)", "guerreiro", 6, 0, "Força", 19, 15),
    "escuro": ("Bônus negativo: à noite, sem tocha (escuridão −4), d20 14, sucesso no limite", "guerreiro", 1, 3, "Percepção", 40, 14),
    "longo": ("Conta longa: arqueiro de nível 7 à noite (nível, Agilidade, olhos de arqueiro, escuridão), d20 6", "arqueiro",
              7, 3, "Percepção", 31, 6),
}


# SIMULAÇÃO (o laboratório): mensagens do teste montadas à mão, com a regra do jogo (o 20 sempre passa, o 1 sempre
# falha; "precisa" pela conta do motor, Testes.precisa_no_dado), para os casos que o herói de teste não alcança.
# Nada é sorteado e nada acontece depois.
SIMULADOS = {
    "sim_so20": ("o 20 natural decide: Carisma 21 contra 22 (só passa com 20)", "Carisma", 22, 20, 1),
    "sim_so1": ("o 1 natural decide: Força 15 contra 12 (só falha com 1)", "Força", 12, 1, 14),
    "sim_carisma": ("bônus negativo e dois dígitos: Carisma 17 − 3 = 14 contra 13", "Carisma", 13, 17, -3),
}


class Achou(Exception):
    pass


class Robo(UI):
    """Só para `procurar`: começa o teste, escolhe a opção do caso no baú e guarda o d20 do motor."""
    interativo = False

    def __init__(self, escolha):
        super().__init__(cor=False, rapido=True)
        self.escolha = escolha

    def _imprimir(self, linha):
        pass

    def escolher(self, pergunta, opcoes):
        for i, o in enumerate(opcoes):
            if o.startswith("Começar") or self.escolha in o:
                return i
        raise Achou(None)

    def rolagem(self, atributo, cd, d20, mod, total, sucesso, precisa=None):
        raise Achou(dict(atributo=atributo, cd=cd, d20=d20, mod=mod, total=total, sucesso=sucesso, precisa=precisa))

    def perguntar(self, *a, **k):
        raise Achou(None)

    def pausar(self, *a, **k):
        pass


def montar(ui, caso, semente):
    _, classe, nivel, periodo, escolha, _, _ = CASOS[caso]
    g = Jogo(ui, seed=semente, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", classe)
    # um lugar selvagem que não seja sempre escuro (ruínas): a escuridão só vale à noite, nos casos que pedem
    loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem" and l.get("bioma") not in ("ruinas", "cidadela"))
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = periodo, "limpo"
    for _ in range(nivel - 1):
        g.subir_nivel()
    if periodo >= 3:
        g.j.consumiveis.pop("tocha", None)  # à noite, sem tocha: a escuridão vale
    g.j.hp = g.j.max_hp
    original, uma = DISPARAR, [True]

    def forcado(g2, contexto):  # TESTE: o Explorar desta vez cai no baú abandonado
        if contexto != "explorar" or not uma[0]:
            return original(g2, contexto)
        uma[0] = False
        return disparar_id(g2, "bau_abandonado", contexto) or True
    eventos.disparar = forcado
    return g


def rodar(ui, caso):
    rot = CASOS[caso][0]
    g = montar(ui, caso, CASOS[caso][5] or 1)
    try:
        g.menu(f"Cenário de teste do d20: {rot}. No baú, escolha a opção de {CASOS[caso][4]}.",
               [("Começar o teste (Explorar)", True)])
        g.explorar()
        g.rodar()
    except FimDeJogo:
        pass


def laboratorio(ui):
    from rpg.sistemas.testes import Testes
    g = montar(ui, "sucesso", 11)
    try:
        while True:
            op = g.menu("Laboratório do d20 (SIMULAÇÃO: números montados à mão, pela regra do jogo; nada acontece depois)",
                        [(f"SIMULAÇÃO: {r} [{k}]", k) for k, (r, *_) in SIMULADOS.items()] + [("Sair do laboratório", None)])
            if not op:
                break
            _, atributo, cd, d20, mod = SIMULADOS[op]
            total = d20 + mod
            ok = d20 == 20 or (d20 != 1 and total >= cd)
            ui.rolagem(atributo, cd, d20, mod, total, ok, precisa=Testes.precisa_no_dado(cd, mod))
            g.dizer("(Simulação: o motor não sorteou nada.)", "cinza")
    except FimDeJogo:
        pass


def procurar():
    for caso, (rot, *_, semente, quer) in CASOS.items():
        achadas = []
        for s in range(1, 400):
            try:
                g = montar(Robo(CASOS[caso][4]), caso, s)
                g.menu("x", [("Começar", True)])
                g.explorar()
            except Achou as e:
                if e.args[0] and e.args[0]["d20"] == quer:
                    achadas.append((s, e.args[0]))
                    if len(achadas) >= 2:
                        break
            except Exception as e:  # noqa: BLE001
                print(caso, s, "erro", e)
                break
        gravada = "ok" if semente == (achadas[0][0] if achadas else None) else "trocar"
        print(f"{caso}: d20 {quer} -> sementes {[a[0] for a in achadas]} (gravada {semente}: {gravada}); "
              f"{achadas[0][1] if achadas else ''}")


TROCAR = {"app/rolagem.js": None}  # (nada: as propostas entram por scripts próprios, depois de rolagem.js)


def demonstracao(srv, caso):
    """Só no servidor de teste: com PROPOSTA, os arquivos do protótipo entram na página depois de app/rolagem.js; com
    PAINEL, a faixa do painel no canto. Troca o método de arquivos deste processo; nada é gravado no jogo."""
    from rpg.web.servidor import Servidor
    proposta, painel = os.environ.get("PROPOSTA", ""), os.environ.get("PAINEL")
    h = srv.httpd.RequestHandlerClass
    original = h._arquivo
    pasta = pathlib.Path(sys.modules[Servidor.__module__].PASTA)

    def _arquivo(self, relativo):
        if relativo.startswith("prototipo-d20/"):
            nome = relativo.split("/", 1)[1]
            if nome in ("d20-dados.js", "d20.js", "d20.css"):
                tipo = "text/css; charset=utf-8" if nome.endswith(".css") else "text/javascript; charset=utf-8"
                return self._responder(200, (PROTO / nome).read_bytes(), tipo)
        if relativo == "index.html" and (proposta or painel):
            pagina = (pasta / "index.html").read_text(encoding="utf-8")
            if proposta:
                pagina = pagina.replace('<script src="/static/app/rolagem.js"></script>',
                                        '<script src="/static/app/rolagem.js"></script>\n'
                                        '<link rel="stylesheet" href="/static/prototipo-d20/d20.css">\n'
                                        '<script src="/static/prototipo-d20/d20-dados.js"></script>\n'
                                        '<script src="/static/prototipo-d20/d20.js"></script>\n'
                                        f'<script>D20Proto.usar({proposta!r});</script>')
            if painel:
                rotulo = {"": "jogo atual", "a": "A · Marfim (a conta embaixo)", "b": "B · Vidro (frente a frente)"}[proposta]
                repetir = html.escape(f"{painel}iniciar?{os.environ.get('REPETIR', '')}", quote=True)
                faixa = (f'<div id="demo-faixa" style="position:fixed;left:8px;bottom:6px;z-index:99999;font:12px/1.4 sans-serif;'
                         f'background:#000c;color:#e8dcbe;border:1px solid #6b5a3a;padding:3px 8px;border-radius:3px">'
                         f'Demonstração do d20: {html.escape(CASOS.get(caso, ("laboratório (SIMULAÇÃO)",))[0])} · {rotulo} · '
                         f'<a href="{repetir}" style="color:#f2c94c">repetir</a> · '
                         f'<a href="{html.escape(painel, quote=True)}" style="color:#f2c94c">painel</a></div>')
                pagina = pagina.replace("</body>", faixa + "</body>")
            return self._responder(200, pagina.encode("utf-8"), "text/html; charset=utf-8")
        return original(self, relativo)

    h._arquivo = _arquivo


def main():
    caso = sys.argv[1] if len(sys.argv) > 1 else "sucesso"
    if caso == "procurar":
        return procurar()
    alvo = laboratorio if caso == "laboratorio" else (lambda u: rodar(u, caso))
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    demonstracao(srv, caso)
    srv.iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=alvo, args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
