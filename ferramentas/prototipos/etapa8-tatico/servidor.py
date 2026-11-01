"""DEMONSTRAÇÃO do protótipo tático da etapa 8 (nada no jogo): o combate numa grade vista de cima.

    python ferramentas/prototipos/etapa8-tatico/servidor.py

Tenta a porta 8799 (ou DEMO_PORTA). Se ela estiver ocupada, diz quem está nela (outra versão deste protótipo, outro
programa) e usa a próxima livre, abrindo o navegador na porta certa: um servidor antigo não se passa pela entrega nova.
A versão aparece no terminal, no título e no topo da página. DEMO_SEM_NAVEGADOR=1 não abre o navegador.

O registro de cada luta vai para uma pasta temporária nova a cada execução (DEMO_SAVES para fixar). Os saves do jogo
não são lidos nem tocados; os retratos e as fontes vêm de rpg/web/static (só leitura)."""
import json
import mimetypes
import os
import pathlib
import socket
import sys
import tempfile
import threading
import time
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
JOGO = RAIZ / "rpg" / "web" / "static"
TELA = AQUI / "tela"
sys.path.insert(0, str(AQUI))
from motor import conteudo as C  # noqa: E402
from motor.combate import Combate  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8799"))
PASTA = pathlib.Path(os.environ.get("DEMO_SAVES") or tempfile.mkdtemp(prefix="etapa8-tatico-"))
trava = threading.Lock()
sessao = {"combate": None, "lutas": []}


def _gravar():
    (PASTA / "registro.json").write_text(json.dumps({"versao": C.VERSAO, "lutas": sessao["lutas"]},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")


def _guardar(como):
    cb = sessao["combate"]
    if not cb or getattr(cb, "_guardada", False) or (not cb.comandos and not cb.fim):
        return
    cb._guardada = True
    r = cb.registro()
    r.update({"como": como, "hora": time.strftime("%H:%M:%S"), "n": len(sessao["lutas"]) + 1})
    sessao["lutas"].append(r)
    _gravar()


def catalogo():
    return {"versao": C.VERSAO, "largura": C.LARGURA, "altura": C.ALTURA,
            "regras": {"zona": C.ZONA_CONTROLE, "mover_depois": C.MOVER_DEPOIS, "colisao": C.COLISAO_CASA,
                       "fogo_chao": C.FOGO_CHAO, "fogo_rodadas": C.FOGO_RODADAS},
            "specs": {k: {"nome": v["spec"], "kit": [{"id": h, "nome": C.HABILIDADES[h]["nome"],
                                                      "desc": C.HABILIDADES[h]["desc"],
                                                      "custo": C.HABILIDADES[h]["custo"],
                                                      "funcao": C.HABILIDADES[h].get("funcao", ""),
                                                      "alcance": Combate._alcance_txt(C.HABILIDADES[h])}
                                                     for h in v["kit"]],
                          "recurso": v["recurso"], "pm": v["pm"]} for k, v in C.HEROI.items()},
            "companheiros": {k: {"nome": v["nome"], "kit": [{"nome": C.HABILIDADES[h]["nome"],
                                                             "desc": C.HABILIDADES[h]["desc"],
                                                             "alcance": Combate._alcance_txt(C.HABILIDADES[h])}
                                                            for h in v["kit"]]} for k, v in C.COMPANHEIROS.items()},
            "talentos": C.TALENTOS,
            "encontros": {k: {"nome": v["nome"], "objetivo": v["objetivo"], "semente": v["semente"], "x1": v["x1"],
                              "inimigos": [C.INIMIGOS[t]["nome"] for t, _ in v["inimigos"]]}
                          for k, v in C.ENCONTROS.items() if not k.startswith("_")},
            "inimigos": {k: {"nome": v["nome"], "vida": v["vida"], "pm": v["pm"],
                             "habs": [C.HABS_INIMIGO[h] for h in v["habs"]]} for k, v in C.INIMIGOS.items()}}


class Demo(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, codigo, dados):
        corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def _arquivo(self, caminho, baixar=None):
        if not caminho.is_file():
            self.send_error(404)
            return
        dados = caminho.read_bytes()
        self.send_response(200)
        tipo = mimetypes.guess_type(str(caminho))[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo in ("application/javascript", "application/json"):
            tipo += "; charset=utf-8"
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.send_header("Cache-Control", "no-store")
        if baixar:
            self.send_header("Content-Disposition", f'attachment; filename="{baixar}"')
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        rota = unquote(urlparse(self.path).path)
        if rota in ("/", "/index.html"):
            return self._arquivo(TELA / "index.html")
        if rota == "/api/versao":
            return self._json(200, {"prototipo": "etapa8-tatico", "versao": C.VERSAO})
        if rota == "/api/catalogo":
            return self._json(200, catalogo())
        if rota == "/api/registro":
            return self._json(200, {"lutas": [{k: v for k, v in x.items() if k not in ("eventos", "comandos")}
                                              for x in sessao["lutas"]], "pasta": str(PASTA)})
        if rota == "/api/registro.json":
            _gravar()
            return self._arquivo(PASTA / "registro.json", baixar="registro-tatico.json")
        if rota.startswith("/static/"):
            alvo = (JOGO / rota[len("/static/"):]).resolve()
            return self._arquivo(alvo) if JOGO.resolve() in alvo.parents else self.send_error(404)
        alvo = (TELA / rota.lstrip("/")).resolve()
        if TELA.resolve() in alvo.parents:
            return self._arquivo(alvo)
        self.send_error(404)

    def do_POST(self):
        rota = urlparse(self.path).path
        n = int(self.headers.get("Content-Length") or 0)
        try:
            corpo = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self._json(400, {"erro": "JSON inválido"})
        with trava:
            return self._post(rota, corpo)

    def _post(self, rota, corpo):
        if rota == "/api/luta":
            _guardar("abandonada")
            try:
                semente = corpo.get("semente")
                sessao["combate"] = Combate(str(corpo.get("spec")), str(corpo.get("encontro")),
                                            [str(t) for t in corpo.get("talentos", []) if t],
                                            None if semente in (None, "") else int(semente),
                                            corpo.get("zona"), mover_depois=corpo.get("mover_depois"))
            except (ValueError, TypeError) as erro:
                return self._json(400, {"erro": str(erro)})
            return self._json(200, sessao["combate"].estado())
        cb = sessao["combate"]
        if not cb:
            return self._json(409, {"erro": "Nenhuma luta"})
        casa = corpo.get("casa")
        casa = tuple(int(v) for v in casa.split(",")) if isinstance(casa, str) else None
        if rota == "/api/mover":
            r = cb.mover(casa, corpo.get("ms"), corpo.get("turno_id"))
        elif rota == "/api/agir":
            r = cb.agir(str(corpo.get("acao", "")), casa, corpo.get("ms"), corpo.get("turno_id"))
        elif rota == "/api/encerrar":
            r = cb.encerrar(corpo.get("ms"), corpo.get("turno_id"))
        else:
            return self._json(404, {"erro": "nada aqui"})
        if cb.fim:
            _guardar("terminada")
        return self._json(200, {**r, "estado": cb.estado()})


def _quem_esta(porta):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{porta}/api/versao", timeout=1) as r:
            d = json.loads(r.read())
            return f"{d.get('prototipo')} · {d.get('versao')}"
    except Exception:
        return "outro programa (sem /api/versao)"


def _livre(porta):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", porta)) != 0


def servir(porta=PORTA, tentativas=11):
    for p in range(porta, porta + tentativas):
        if not _livre(p):
            print(f"porta {p} ocupada por: {_quem_esta(p)}", flush=True)
            continue
        srv = ThreadingHTTPServer(("127.0.0.1", p), Demo)
        srv.daemon_threads = True
        return srv
    raise SystemExit(f"nenhuma porta livre entre {porta} e {porta + tentativas - 1}")


def main():
    srv = servir()
    url = f"http://127.0.0.1:{srv.server_address[1]}/"
    print(f"Protótipo tático · {C.VERSAO}", flush=True)
    print(url, flush=True)
    print(f"registro da sessão em {PASTA}", flush=True)
    if not os.environ.get("DEMO_SEM_NAVEGADOR"):
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
