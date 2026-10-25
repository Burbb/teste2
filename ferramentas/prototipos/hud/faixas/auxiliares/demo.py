"""DEMONSTRAÇÃO das faixas de passagem (protótipo, 24/10/2026; nada no jogo): um painel local para ver as faixas no jogo
de verdade, as de hoje e as propostas A e B, em cada acontecimento, sem preparar partida e sem tocar no save
(cada caso roda num processo próprio, com uma pasta de saves temporária).

    python ferramentas/prototipos/hud/faixas/auxiliares/demo.py      # painel em http://127.0.0.1:8768/

Cada botão encerra o caso anterior e sobe outro (cenarios_faixas.py, com PROPOSTA=<versão>) numa porta livre; o
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
from cenarios_faixas import CASOS, ROTULOS  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8768"))
PAINEL = f"http://127.0.0.1:{PORTA}/"
VERSOES = ["", "r", "a", "b"]
trava = threading.Lock()
atual = {"proc": None, "rotulo": ""}


def encerrar():
    p = atual["proc"]
    if p and p.poll() is None:
        p.kill()
        p.wait(timeout=5)
    atual["proc"] = None


def iniciar(caso, versao):
    with trava:
        encerrar()
        repetir = urlencode({"caso": caso, "versao": versao})
        env = {**os.environ, "PYTHONPATH": str(RAIZ), "PYTHONIOENCODING": "utf-8", "PROPOSTA": versao, "PAINEL": PAINEL,
               "REPETIR": repetir}
        p = subprocess.Popen([sys.executable, str(AQUI / "cenarios_faixas.py"), caso], cwd=str(RAIZ), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        atual["proc"] = p
        url = p.stdout.readline().strip()
        if not url.startswith("http"):
            encerrar()
            raise RuntimeError("o caso não subiu")
        atual["rotulo"] = f"{CASOS[caso][0]} · {ROTULOS[versao]}"
        return url


def pagina():
    linhas = []
    for cid, (rotulo, fazer) in CASOS.items():
        botoes = " ".join(f'<a class="b{" p" if v else ""}" href="/iniciar?{html.escape(urlencode({"caso": cid, "versao": v}))}">'
                          f'{html.escape(ROTULOS[v])}</a>' for v in VERSOES)
        linhas.append(f"<tr><td>{html.escape(rotulo)}<br><small class=\"nota\">{html.escape(fazer)}</small></td><td>{botoes}</td></tr>")
    rodando = html.escape(atual["rotulo"]) if atual["proc"] and atual["proc"].poll() is None else "nenhum"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Demonstração das faixas de passagem</title>
<style>body{{background:#141210;color:#e8dcbe;font:16px/1.5 Georgia,serif;max-width:1100px;margin:32px auto;padding:0 16px}}
h1{{font-size:24px;color:#f2c94c}} table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid #3a3226;padding:10px 6px}}
a.b{{display:inline-block;padding:6px 14px;margin:2px;border:1px solid #6b5a3a;color:#e8dcbe;text-decoration:none;border-radius:3px}}
a.b.p{{border-color:#f2c94c;color:#f2c94c;font-weight:bold}} a.b:hover{{background:#2a2418}}
.nota{{color:#a89878;font-size:14px}}</style></head><body>
<h1>Demonstração das faixas de passagem (protótipo, nada no jogo)</h1>
<p class="nota">Cada botão encerra o caso anterior e começa outro do zero, numa partida de teste com saves temporários
(o seu save não é tocado). Na página: "Começar" e o que a coluna da esquerda diz (Atacar até a luta acabar; no caso da
capela, "Sair e acampar"). As três versões fazem o mesmo, no mesmo tempo: só o desenho da faixa muda. A sequência
mostra o ritmo inteiro: as duas faixas, o quadro do espólio, a subida de nível e o achado. Velocidade do texto: a
tecla V. No canto de baixo: "repetir" e "painel". Movimento reduzido: F12 → ⋮ → More tools → Rendering →
prefers-reduced-motion: reduce, e "repetir".</p>
<table>{''.join(linhas)}</table>
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
            caso, versao = q.get("caso"), q.get("versao", "")
            if caso not in CASOS or versao not in VERSOES:
                return self._enviar(400, "pedido inválido")
            try:
                return self._enviar(302, "", local=iniciar(caso, versao))
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
    try:
        main()
    except KeyboardInterrupt:
        pass
