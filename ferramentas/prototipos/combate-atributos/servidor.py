"""DEMONSTRAÇÃO do combate e dos atributos (protótipo, 25/10/2026; nada no jogo). Um servidor local que roda as regras de
motor/regras.py e serve a tela da demo (tela/), com os retratos, os ícones, as fontes e os materiais do jogo lidos de
rpg/web/static (só leitura: nada do jogo carrega arquivos daqui, e daqui nada se grava no jogo).

    python ferramentas/prototipos/combate-atributos/servidor.py      # a demo em http://127.0.0.1:8781/

Uma luta por vez, na memória. Os "saves" da demo (o resultado de cada luta terminada ou reiniciada, para comparar as
construções) vão para uma pasta temporária nova a cada execução; os saves do jogo não são lidos nem tocados.
"""
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
from motor.regras import Combate, situacao, _dist_valida  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8781"))
PASTA_SAVES = pathlib.Path(os.environ.get("DEMO_SAVES") or tempfile.mkdtemp(prefix="combate-atributos-"))
trava = threading.Lock()
sessao = {"combate": None, "resultados": []}


def _guardar_resultado(cb, como):
    """Anota a luta (terminada ou interrompida) na lista da sessão e no arquivo temporário."""
    if cb is None or cb.resumo.get("anotado"):
        return
    cb.resumo["anotado"] = True
    r = {"encontro": cb.encontro, "nome": cb.cfg["nome"], "distribuicao": cb.distribuicao,
         "atributos": cb.c["heroi"].atr, "fim": cb.fim or como, "rodadas": cb.rodada, "quedas": cb.resumo["quedas"],
         "dano_recebido": cb.resumo["dano_recebido"], "acoes": cb.resumo["acoes"], "preparos": cb.resumo["preparos"],
         "preparos_resolvidos": cb.resumo["preparos_resolvidos"], "preparos_desfeitos": cb.resumo["preparos_desfeitos"],
         "hora": time.strftime("%H:%M:%S")}
    sessao["resultados"].append(r)
    (PASTA_SAVES / "resultados.json").write_text(json.dumps(sessao["resultados"], ensure_ascii=False, indent=1),
                                                encoding="utf-8")


def _atributos(corpo):
    atr = corpo.get("atributos")
    if not atr:
        return None
    atr = {k: int(atr[k]) for k in C.ATRIBUTOS}
    erro = _dist_valida(atr)
    if erro:
        raise ValueError(erro)
    return atr


def catalogo():
    return {"encontros": [{"id": k, "nome": v["nome"], "tipo": v["tipo"], "objetivo": v["objetivo"], "teste": v.get("teste")}
                          for k, v in C.ENCONTROS.items()],
            "distribuicoes": [{"id": k, "nome": v["nome"], "resumo": v["resumo"], "atributos": v["atributos"]}
                              for k, v in C.DISTRIBUICOES.items()],
            "atributos": [{"id": a, "nome": C.NOME_ATRIBUTO[a], "sigla": C.SIGLA[a]} for a in C.ATRIBUTOS],
            "pontos": C.PONTOS_PROTAGONISTA, "min": C.ATRIBUTO_MIN, "max": C.ATRIBUTO_MAX,
            "saves": str(PASTA_SAVES)}


def comparar(atr_livre=None):
    """Os valores derivados do protagonista em cada distribuição, no mesmo nível, equipamento e grupo (o primeiro
    encontro só para ter a ordem)."""
    colunas = []
    for k in C.DISTRIBUICOES:
        cb = Combate("e1", k)
        colunas.append({"id": k, "nome": C.DISTRIBUICOES[k]["nome"], "atributos": cb.c["heroi"].atr,
                        "derivados": cb.derivados(cb.c["heroi"]),
                        "ordem": [cb.c[i].nome for i in cb.ordem]})
    if atr_livre:
        cb = Combate("e1", atributos=atr_livre)
        colunas.append({"id": "livre", "nome": "Livre", "atributos": cb.c["heroi"].atr, "derivados": cb.derivados(cb.c["heroi"]),
                        "ordem": [cb.c[i].nome for i in cb.ordem]})
    return {"colunas": colunas}


class Demo(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, codigo, obj):
        dados = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def _arquivo(self, base, rel):
        alvo = (base / unquote(rel)).resolve()
        if base.resolve() not in alvo.parents or not alvo.is_file():
            return self._json(404, {"erro": "nada aqui"})
        dados = alvo.read_bytes()
        tipo = mimetypes.guess_type(alvo.name)[0] or "application/octet-stream"
        if alvo.suffix in (".js", ".css", ".html"):
            tipo += "; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            return self._arquivo(TELA, "index.html")
        if url.path.startswith("/tela/"):
            return self._arquivo(TELA, url.path[len("/tela/"):])
        if url.path.startswith("/static/"):
            return self._arquivo(JOGO, url.path[len("/static/"):])
        with trava:
            if url.path == "/api/catalogo":
                return self._json(200, catalogo())
            if url.path == "/api/estado":
                cb = sessao["combate"]
                return self._json(200, cb.estado() if cb else {"vazio": True})
            if url.path == "/api/resultados":
                return self._json(200, {"resultados": sessao["resultados"], "pasta": str(PASTA_SAVES)})
        self._json(404, {"erro": "nada aqui"})

    def do_POST(self):
        url = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            corpo = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            return self._json(400, {"erro": "pedido inválido"})
        with trava:
            try:
                if url.path == "/api/iniciar":
                    enc = corpo.get("encontro")
                    if enc not in C.ENCONTROS:
                        return self._json(400, {"erro": "encontro desconhecido"})
                    dist = corpo.get("distribuicao", "A")
                    if dist not in C.DISTRIBUICOES and dist != "livre":
                        return self._json(400, {"erro": "distribuição desconhecida"})
                    _guardar_resultado(sessao["combate"], "reiniciado")
                    sessao["combate"] = Combate(enc, dist if dist != "livre" else "A", _atributos(corpo))
                    return self._json(200, sessao["combate"].estado())
                if url.path == "/api/agir":
                    cb = sessao["combate"]
                    if not cb:
                        return self._json(409, {"ok": False, "motivo": "Nenhuma luta."})
                    r = cb.agir(corpo.get("turno_id"), str(corpo.get("acao", "")), corpo.get("alvo"))
                    if cb.fim:
                        _guardar_resultado(cb, cb.fim)
                    return self._json(200, {**r, "estado": cb.estado()})
                if url.path == "/api/comparar":
                    return self._json(200, comparar(_atributos(corpo)))
                if url.path == "/api/situacao":
                    return self._json(200, situacao(corpo.get("distribuicao", "A"), _atributos(corpo),
                                                    corpo.get("escolha"), bool(corpo.get("ajuda"))))
            except ValueError as e:
                return self._json(400, {"erro": str(e)})
        self._json(404, {"erro": "nada aqui"})


def servir(porta=PORTA):
    srv = ThreadingHTTPServer(("127.0.0.1", porta), Demo)
    srv.daemon_threads = True
    return srv


def main():
    srv = servir()
    print(f"http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    print(f"resultados da sessão em {PASTA_SAVES}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
