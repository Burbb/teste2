"""DEMONSTRAÇÃO da etapa 2 (24/10/2026): um painel local para abrir e repetir os cenários de teste no navegador, no
jogo atual, nas três direções da segunda rodada (A Relicário, B Estouro, C Estandarte; ../v2/) ou na primeira proposta
(o histórico), sem preparar partida e sem tocar no save (cada cenário roda num processo próprio, com uma pasta de saves
temporária). Nada disto está no jogo. Antes de abrir, monta as direções (montar_v2.py).

    python ferramentas/prototipos/hud/celebracoes/auxiliares/demo.py      # painel em http://127.0.0.1:8765/

Cada "abrir" encerra o cenário anterior e sobe outro (cenarios_teste.py, com PROTOTIPO=<versão>) numa porta
livre; o navegador vai direto para ele. No canto da página do cenário: repetir e voltar ao painel.
"""
import html
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[4]
PORTA = int(os.environ.get("DEMO_PORTA", "8765"))
PAINEL = f"http://127.0.0.1:{PORTA}/"
CENARIOS = [("nivel", "Um nível (do 1 ao 2, dois lobos)", "guerreiro"),
            ("dois_niveis", "Dois níveis seguidos (do 1 ao 3, a Ilse e dois afogados)", "mago"),
            ("raridades", "As quatro raridades (comum, mágico, raro, lendário)", "arqueiro"),
            ("nivel4", "Nível 4, a encruzilhada (o aviso da especialização)", "arqueiro"),
            ("sigilo", "O Sigilo de um guardião", "guerreiro"),
            ("especializacao", "A especialização escolhida", "mago"),
            ("limites", "SIMULAÇÃO de limites: textos longos e seis ganhos (fora das regras)", "guerreiro"),
            ("nivel_especializacao", "Sequência: nível 4 e, em seguida, a especialização (a dos vídeos)", "mago"),
            ("raridades_sigilo", "Sequência: as quatro raridades e o Sigilo (a dos vídeos)", "arqueiro")]
# as versões: o valor de PROTOTIPO (vazio: o jogo como está) e o rótulo
VERSOES = [("relicario2", "A2 · Relicário refinado"), ("estouro2", "B2 · Estouro refinado"), ("", "Jogo atual"),
           ("relicario", "A · 1ª versão"), ("estouro", "B · 1ª versão"), ("estandarte", "C · reservada"),
           ("brilho", "1ª proposta")]
NOMES = dict(VERSOES)
CLASSES = ["guerreiro", "mago", "arqueiro"]
trava = threading.Lock()
atual = {"proc": None, "rotulo": ""}


def encerrar():
    p = atual["proc"]
    if p and p.poll() is None:
        p.kill()
        p.wait(timeout=5)
    atual["proc"] = None


def iniciar(cenario, versao, classe):
    """Sobe o cenário e devolve o endereço da página (ou levanta RuntimeError)."""
    with trava:
        encerrar()
        repetir = urlencode({"cenario": cenario, "versao": versao, "classe": classe})
        env = {**os.environ, "PYTHONPATH": str(RAIZ), "PYTHONIOENCODING": "utf-8", "VELOCIDADE": "normal",
               "CLASSE": classe, "PAINEL": PAINEL, "REPETIR": repetir}
        env.pop("PROTOTIPO", None)
        if versao:
            env["PROTOTIPO"] = versao
        env["ROTULO"] = NOMES[versao]
        p = subprocess.Popen([sys.executable, str(AQUI / "cenarios_teste.py"), cenario], cwd=str(RAIZ), env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        atual["proc"] = p
        url = p.stdout.readline().strip()
        if not url.startswith("http"):
            encerrar()
            raise RuntimeError("o cenário não subiu")
        atual["rotulo"] = f"{cenario} · {NOMES[versao]} · {classe}"
        return url


def pagina():
    linhas = []
    for cid, rotulo, classe in CENARIOS:
        botoes = " ".join(
            f'<a class="b{" p" if v in ("relicario2", "estouro2") else " h" if v in ("relicario", "estouro", "estandarte", "brilho") else ""}" href="/iniciar?{html.escape(urlencode({"cenario": cid, "versao": v, "classe": classe}))}">{nome}</a>'
            for v, nome in VERSOES)
        linhas.append(f"<tr><td>{html.escape(rotulo)}<br><small>classe: {classe}</small></td><td>{botoes}</td></tr>")
    opcoes = "".join(f"<option>{c}</option>" for c in CLASSES)
    versoes = "".join(f'<option value="{v}">{html.escape(n)}</option>' for v, n in VERSOES)
    cens = "".join(f'<option value="{c}">{html.escape(r)}</option>' for c, r, _ in CENARIOS)
    rodando = html.escape(atual["rotulo"]) if atual["proc"] and atual["proc"].poll() is None else "nenhum"
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Demonstração da etapa 2</title>
<style>body{{background:#141210;color:#e8dcbe;font:16px/1.5 Georgia,serif;max-width:1180px;margin:32px auto;padding:0 16px}}
h1{{font-size:24px;color:#f2c94c}} table{{border-collapse:collapse;width:100%}} td{{border-top:1px solid #3a3226;padding:10px 6px}}
small{{color:#a89878}} a.b{{display:inline-block;padding:6px 14px;margin:2px;border:1px solid #6b5a3a;color:#e8dcbe;text-decoration:none;border-radius:3px}}
a.b.p{{border-color:#f2c94c;color:#f2c94c;font-weight:bold}} a.b.h{{color:#8a8070;border-color:#3a3226}} a.b:hover{{background:#2a2418}} form{{margin-top:12px}} select,button{{font:inherit}}
.nota{{color:#a89878;font-size:14px}}</style></head><body>
<h1>Demonstração da etapa 2 (protótipo, nada no jogo)</h1>
<p class="nota">Cada botão encerra o cenário anterior e começa outro do zero, numa partida de teste com saves
temporários (o seu save não é tocado). Na página, clique em "Começar o teste"; no canto de baixo, "repetir" e "painel".
A2 e B2 são as versões refinadas (em destaque); "A · 1ª versão", "B · 1ª versão", "C · reservada" e "1ª proposta"
são o histórico, em cinza. Movimento
reduzido: F12 → ⋮ → More tools → Rendering → prefers-reduced-motion: reduce, e "repetir".</p>
<table>{''.join(linhas)}</table>
<form action="/iniciar">Outra classe: <select name="cenario">{cens}</select> <select name="classe">{opcoes}</select>
<select name="versao">{versoes}</select>
<button>Abrir</button></form>
<p class="nota">Rodando agora: {rodando}</p></body></html>"""


class Painel(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _enviar(self, codigo, corpo, tipo="text/html; charset=utf-8", local=None):
        self.send_response(codigo)
        if local:
            self.send_header("Location", local)
        self.send_header("Content-Type", tipo)
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
            cenario, versao, classe = q.get("cenario"), q.get("versao", ""), q.get("classe", "guerreiro")
            if cenario not in {c for c, _, _ in CENARIOS} or versao not in NOMES or classe not in CLASSES:
                return self._enviar(400, "pedido inválido")
            try:
                return self._enviar(302, "", local=iniciar(cenario, versao, classe))
            except RuntimeError as e:
                return self._enviar(500, str(e))
        self._enviar(404, "nada aqui")


def main():
    subprocess.run([sys.executable, str(AQUI / "montar_v2.py")], cwd=str(RAIZ), check=True, stdout=subprocess.DEVNULL)
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
