"""DEMONSTRAÇÃO do protótipo X1 da etapa 8 (nada no jogo): montar builds, lutar nos encontros compartilhados, repetir
com a mesma semente, redistribuir à vontade e guardar o registro das escolhas, ações e cadeias.

    python ferramentas/prototipos/etapa8-builds/servidor.py

Abre em http://127.0.0.1:8797/ (porta em DEMO_PORTA). Uma luta por vez, na memória. O registro de cada luta terminada
ou abandonada e de cada montagem salva vai para uma pasta temporária nova a cada execução (DEMO_SAVES para fixar); os
saves do jogo não são lidos nem tocados. Os retratos são lidos de rpg/web/static (só leitura)."""
import json
import mimetypes
import os
import pathlib
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
JOGO = RAIZ / "rpg" / "web" / "static"
TELA = AQUI / "tela"
sys.path.insert(0, str(AQUI))
from motor import conteudo as C  # noqa: E402
from motor import montagem as M  # noqa: E402
from motor.combate import Combate  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8797"))
PASTA = pathlib.Path(os.environ.get("DEMO_SAVES") or tempfile.mkdtemp(prefix="etapa8-builds-"))
trava = threading.Lock()
sessao = {"combate": None, "lutas": [], "montagens": []}


def _gravar():
    (PASTA / "registro.json").write_text(json.dumps({"lutas": sessao["lutas"], "montagens": sessao["montagens"]},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")


def _guardar_luta(como):
    cb = sessao["combate"]
    if not cb or getattr(cb, "_guardada", False):
        return
    if not cb.decisoes and not cb.fim:
        return
    cb._guardada = True
    r = cb.registro()
    r.update({"como": como, "hora": time.strftime("%H:%M:%S"), "n": len(sessao["lutas"]) + 1})
    sessao["lutas"].append(r)
    _gravar()


def catalogo():
    return {"pontos": C.PONTOS, "espacos": C.ESPACOS, "estruturas": C.ESTRUTURAS, "tipos": C.NOME_TIPO,
            "requisito_linha": C.REQUISITO_LINHA, "fichas": C.FICHAS, "regras": C.REGRAS_LUTA,
            "specs": {k: {"nome": v["spec"], "classe": v["classe"], "recurso": v["recurso"],
                          "ultimate": C.HABILIDADES[v["ultimate"]]["nome"]} for k, v in C.HEROI.items()},
            "exemplos": C.EXEMPLOS,
            "encontros": {k: {"nome": v["nome"], "semente": v["semente"], "resumo": v["resumo"],
                              "favorece": v["favorece"], "desfavorece": v["desfavorece"],
                              "inimigos": [C.INIMIGOS[i]["nome"] for i in v.get("inimigos", [])]}
                          for k, v in C.ENCONTROS.items() if not k.startswith("_")},
            "inimigos": {k: {"nome": v["nome"], "vida": v["vida"], "habs": [C.HABS_INIMIGO[h] for h in v["habs"]],
                             "res": v.get("res", {}), "tracos": v.get("tracos", [])} for k, v in C.INIMIGOS.items()},
            "companheiros": {k: {"nome": v["nome"], "kit": [{"nome": C.HABILIDADES[h]["nome"],
                                                             "desc": C.HABILIDADES[h]["desc"]} for h in v["kit"]]}
                             for k, v in C.COMPANHEIROS.items()}}


def _montagem(corpo):
    m = corpo.get("montagem") or {}
    return {"estrutura": m.get("estrutura", "t4"), "spec": m.get("spec", "piromante"),
            "kit": [str(h) for h in m.get("kit", [])][:8], "nos": {str(k): int(v) for k, v in m.get("nos", {}).items()},
            "nome": str(m.get("nome") or "Livre")[:60]}


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
        if rota == "/api/catalogo":
            return self._json(200, catalogo())
        if rota == "/api/registro":
            return self._json(200, {"lutas": [{k: v for k, v in x.items() if k not in ("eventos", "decisoes")}
                                              for x in sessao["lutas"]], "montagens": sessao["montagens"],
                                    "pasta": str(PASTA)})
        if rota == "/api/registro.json":
            _gravar()
            return self._arquivo(PASTA / "registro.json", baixar="registro-x1.json")
        if rota.startswith("/static/"):
            alvo = (JOGO / rota[len("/static/"):]).resolve()
            if JOGO.resolve() in alvo.parents:
                return self._arquivo(alvo)
            return self.send_error(404)
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
        if rota == "/api/montagem":
            return self._json(200, M.ficha(_montagem(corpo)))
        if rota == "/api/salvar":
            m = _montagem(corpo)
            sessao["montagens"].append({"hora": time.strftime("%H:%M:%S"), "montagem": m, "erros": M.erros(m),
                                        "nota": str(corpo.get("nota", ""))[:500]})
            _gravar()
            return self._json(200, {"ok": True, "n": len(sessao["montagens"])})
        if rota == "/api/luta":
            m = _montagem(corpo)
            erros = M.erros(m)
            if erros:
                return self._json(400, {"erro": "; ".join(erros)})
            enc = corpo.get("encontro")
            if enc not in C.ENCONTROS:
                return self._json(400, {"erro": "encontro desconhecido"})
            _guardar_luta("abandonada")
            semente = corpo.get("semente")
            sessao["combate"] = Combate(m, enc, None if semente in (None, "") else int(semente))
            return self._json(200, sessao["combate"].estado())
        cb = sessao["combate"]
        if not cb:
            return self._json(409, {"erro": "Nenhuma luta"})
        if rota == "/api/agir":
            r = cb.agir(str(corpo.get("acao", "")), corpo.get("alvo"), corpo.get("turno_id"))
        elif rota == "/api/sair_furia":
            r = cb.sair_furia()
        else:
            return self._json(404, {"erro": "nada aqui"})
        if cb.fim:
            _guardar_luta("terminada")
        return self._json(200, {**r, "estado": cb.estado()})


def servir(porta=PORTA):
    srv = ThreadingHTTPServer(("127.0.0.1", porta), Demo)
    srv.daemon_threads = True
    return srv


def main():
    srv = servir()
    print(f"http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    print(f"registro da sessão em {PASTA}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
