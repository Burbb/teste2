"""DEMONSTRAÇÃO do d20 (etapa 2, 24/10/2026; protótipo, nada no jogo): um painel local para abrir e repetir os casos
no jogo atual e nas propostas A (Marfim) e B (Vidro), sem preparar partida e sem tocar no save (cada caso roda num
processo próprio, com uma pasta de saves temporária).

    python ferramentas/prototipos/hud/d20/auxiliares/demo.py      # painel em http://127.0.0.1:8766/

Cada botão encerra o caso anterior e sobe outro (cenarios_d20.py, com PROPOSTA=<versão>) numa porta livre; o
navegador vai direto para ele. No canto da página do caso: repetir e voltar ao painel.
"""
import html
import os
import pathlib
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
sys.path.insert(0, str(AQUI))
from cenarios_d20 import CASOS, SIMULADOS  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8766"))
PAINEL = f"http://127.0.0.1:{PORTA}/"
LINHAS = [(k, v[0]) for k, v in CASOS.items()] + [("laboratorio", "Laboratório (SIMULAÇÃO): o 20 e o 1 que decidem "
                                                                   "contra a conta, bônus negativo no Carisma")]
VERSOES = [("", "Jogo atual"), ("a", "A · Marfim"), ("b", "B · Vidro")]
NOMES = dict(VERSOES)
VELOCIDADES = ["normal", "lento", "rapido", "instantaneo"]
trava = threading.Lock()
atual = {"proc": None, "rotulo": ""}


def encerrar():
    p = atual["proc"]
    if p and p.poll() is None:
        p.kill()
        p.wait(timeout=5)
    atual["proc"] = None


def iniciar(caso, versao, velocidade):
    with trava:
        encerrar()
        repetir = urlencode({"caso": caso, "versao": versao, "velocidade": velocidade})
        env = {**os.environ, "PYTHONPATH": str(RAIZ), "PYTHONIOENCODING": "utf-8", "VELOCIDADE": velocidade,
               "PROPOSTA": versao, "PAINEL": PAINEL, "REPETIR": repetir}
        p = subprocess.Popen([sys.executable, str(AQUI / "cenarios_d20.py"), caso], cwd=str(RAIZ), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        atual["proc"] = p
        url = p.stdout.readline().strip()
        if not url.startswith("http"):
            encerrar()
            raise RuntimeError("o caso não subiu")
        atual["rotulo"] = f"{caso} · {NOMES[versao]} · {velocidade}"
        return url


def pagina():
    linhas = []
    for cid, rotulo in LINHAS:
        botoes = " ".join(f'<a class="b{" p" if v else ""}" href="/iniciar?{html.escape(urlencode({"caso": cid, "versao": v, "velocidade": "normal"}))}">{n}</a>'
                          for v, n in VERSOES)
        linhas.append(f"<tr><td>{html.escape(rotulo)}</td><td>{botoes}</td></tr>")
    cens = "".join(f'<option value="{c}">{html.escape(r)}</option>' for c, r in LINHAS)
    vers = "".join(f'<option value="{v}">{html.escape(n)}</option>' for v, n in VERSOES)
    vels = "".join(f"<option>{v}</option>" for v in VELOCIDADES)
    rodando = html.escape(atual["rotulo"]) if atual["proc"] and atual["proc"].poll() is None else "nenhum"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Demonstração do d20</title>
<style>body{{background:#141210;color:#e8dcbe;font:16px/1.5 Georgia,serif;max-width:1100px;margin:32px auto;padding:0 16px}}
h1{{font-size:24px;color:#f2c94c}} table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid #3a3226;padding:10px 6px}}
a.b{{display:inline-block;padding:6px 14px;margin:2px;border:1px solid #6b5a3a;color:#e8dcbe;text-decoration:none;border-radius:3px}}
a.b.p{{border-color:#f2c94c;color:#f2c94c;font-weight:bold}} a.b:hover{{background:#2a2418}} select,button{{font:inherit}}
.nota{{color:#a89878;font-size:14px}}</style></head><body>
<h1>Demonstração do d20 (protótipo, nada no jogo)</h1>
<p class="nota">Cada botão encerra o caso anterior e começa outro do zero, numa partida de teste com saves temporários
(o seu save não é tocado). Na página: "Começar o teste (Explorar)" e, no baú, a opção indicada no topo (Percepção, ou
Força no caso da Força). O d20 é o do motor: a semente de cada caso decide o número, igual nas três versões. No
laboratório, as mensagens são montadas à mão (SIMULAÇÃO), pela regra do jogo. No canto de baixo: "repetir" e
"painel". Pular: clique ou tecla durante o giro. Movimento reduzido: F12 → ⋮ → More tools → Rendering →
prefers-reduced-motion: reduce, e "repetir" (ou "Mostrar animações" desligado no Windows).</p>
<table>{''.join(linhas)}</table>
<form action="/iniciar">Outra velocidade do texto: <select name="caso">{cens}</select> <select name="versao">{vers}</select>
<select name="velocidade">{vels}</select> <button>Abrir</button></form>
<p class="nota">Rodando agora: {rodando}</p></body></html>"""


class Painel(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _enviar(self, codigo, corpo, local=None):
        self.send_response(codigo)
        if local:
            self.send_header("Location", local)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        dados = corpo.encode("utf-8")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            return self._enviar(200, pagina())
        if url.path == "/iniciar":
            q = {k: v[0] for k, v in parse_qs(url.query).items()}
            caso, versao, vel = q.get("caso"), q.get("versao", ""), q.get("velocidade", "normal")
            if caso not in dict(LINHAS) or versao not in NOMES or vel not in VELOCIDADES:
                return self._enviar(400, "pedido inválido")
            try:
                return self._enviar(302, "", local=iniciar(caso, versao, vel))
            except RuntimeError as e:
                return self._enviar(500, str(e))
        self._enviar(404, "nada aqui")


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORTA), Painel)
    srv.daemon_threads = True
    print(PAINEL, flush=True)
    try:
        srv.serve_forever()
    finally:
        encerrar()


if __name__ == "__main__":
    assert SIMULADOS
    try:
        main()
    except KeyboardInterrupt:
        pass
