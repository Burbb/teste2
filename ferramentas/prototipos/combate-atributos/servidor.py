"""DEMONSTRAÇÃO do combate e dos atributos (protótipo; nada no jogo). Um servidor local com as duas versões, para
comparar:

- **v4** (26/10/2026, a atual) em http://127.0.0.1:8781/ : motor4/ e tela4/ (a v3 sem a Marca, com o Golpe Oportuno
  do Morel e a Chuva de Brasas);
- **v3** (26/10/2026, congelada) em http://127.0.0.1:8781/v3/ : motor3/ e tela3/ (tipos de dano, resistências, o
  Avanço do Baluarte, a Queimadura e a Combustão, Vontade no recurso, a ultimate de uso único);
- **v2** (26/10/2026, congelada) em http://127.0.0.1:8781/v2/ : motor2/ e tela2/;
- **v1** (25/10/2026, congelada) em http://127.0.0.1:8781/v1/ : motor/ e tela/.

Os retratos, os ícones, as fontes e os materiais do jogo são lidos de rpg/web/static (só leitura: nada do jogo carrega
arquivos daqui, e daqui nada se grava no jogo).

    python ferramentas/prototipos/combate-atributos/servidor.py

Uma luta por versão, na memória. Os "saves" da demo (o resultado de cada luta terminada ou reiniciada) vão para uma
pasta temporária nova a cada execução; os saves do jogo não são lidos nem tocados.
"""
import json
import mimetypes
import os
import pathlib
import re
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
JOGO = RAIZ / "rpg" / "web" / "static"
TELA, TELA2, TELA3, TELA4 = AQUI / "tela", AQUI / "tela2", AQUI / "tela3", AQUI / "tela4"
sys.path.insert(0, str(AQUI))
from motor import conteudo as C  # noqa: E402
from motor.regras import Combate, situacao, _dist_valida  # noqa: E402
from motor2 import conteudo as C2  # noqa: E402
from motor2 import regras as R2  # noqa: E402
from motor3 import conteudo as C3  # noqa: E402
from motor3 import regras as R3  # noqa: E402
from motor4 import conteudo as C4  # noqa: E402
from motor4 import regras as R4  # noqa: E402

PORTA = int(os.environ.get("DEMO_PORTA", "8781"))
PASTA_SAVES = pathlib.Path(os.environ.get("DEMO_SAVES") or tempfile.mkdtemp(prefix="combate-atributos-"))
trava = threading.Lock()
sessao = {"combate": None, "resultados": [], "combate2": None, "resultados2": [], "combate3": None, "resultados3": [],
          "combate4": None, "resultados4": []}


def _gravar():
    (PASTA_SAVES / "resultados.json").write_text(json.dumps({"v1": sessao["resultados"], "v2": sessao["resultados2"],
                                                             "v3": sessao["resultados3"], "v4": sessao["resultados4"]},
                                                            ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------- v1 (congelada)
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
    _gravar()


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


# ---------------------------------------------------------------- v2
def _guardar_resultado2(cb, como):
    if cb is None or cb.resumo.get("anotado"):
        return
    cb.resumo["anotado"] = True
    h = cb.c["heroi"]
    r = {"encontro": cb.encontro, "nome": cb.cfg["nome"], "build": cb.build, "atributos": h.atr, "presenca": cb.presenca,
         "kit": h.kit, "kit_nomes": [C2.HABILIDADES[k]["nome"] for k in h.kit], "equip": h.equip,
         "fim": cb.fim or como, "rodadas": cb.rodada, "quedas": cb.resumo["quedas"],
         "dano_recebido": cb.resumo["dano_recebido"], "acoes": cb.resumo["acoes"], "recurso": cb.resumo["recurso"],
         "preparos": cb.resumo["preparos"], "preparos_resolvidos": cb.resumo["preparos_resolvidos"],
         "preparos_desfeitos": cb.resumo["preparos_desfeitos"], "preparos_aparados": cb.resumo["preparos_aparados"],
         "controles": cb.resumo["controles"], "ultimate": cb.resumo["ultimate"], "hora": time.strftime("%H:%M:%S")}
    sessao["resultados2"].append(r)
    _gravar()


def _atr2(corpo, exata=True):
    atr = corpo.get("atributos")
    if not atr:
        b = C2.BUILDS.get(corpo.get("build") or "forca")
        return dict(b["atributos"]) if b else None
    atr = {k: int(atr[k]) for k in C2.ATRIBUTOS}
    erro = R2.validar_atributos(atr)
    if erro and (exata or not erro.startswith("A soma")):
        raise ValueError(erro)
    return atr


def _presenca(corpo):
    p = int(corpo.get("presenca") or C2.PRESENCA_PADRAO)
    if not (C2.ATRIBUTO_MIN <= p <= C2.ATRIBUTO_MAX):
        raise ValueError("Presença vai de 1 a 10.")
    return p


def catalogo2():
    return {"versao": 2,
            "encontros": [{"id": k, "nome": v["nome"], "tipo": v["tipo"], "objetivo": v["objetivo"], "teste": v.get("teste")}
                          for k, v in C2.ENCONTROS.items()],
            "builds": [{"id": k, **v} for k, v in C2.BUILDS.items()],
            "atributos": [{"id": a, "nome": C2.NOME_ATRIBUTO[a], "sigla": C2.SIGLA[a], "funcao": C2.FUNCAO[a]}
                          for a in C2.ATRIBUTOS],
            "orcamento": C2.ORCAMENTO, "min": C2.ATRIBUTO_MIN, "max": C2.ATRIBUTO_MAX, "presenca": C2.PRESENCA_PADRAO,
            "habilidades": [{"id": k, "nome": h["nome"], "tier": h["tier"], "pontos": C2.PONTOS_TIER[h["tier"]],
                             "custo": h["custo"], "desc": h["desc"], "tipo": h.get("tipo"), "alvo": h["alvo"]}
                            for k, h in C2.HABILIDADES.items() if "tier" in h],
            "basicos": [{"id": k, "nome": C2.HABILIDADES[k]["nome"], "desc": C2.HABILIDADES[k]["desc"]} for k in C2.BASICOS],
            "kit_pontos": C2.KIT_PONTOS, "kit_espacos": C2.KIT_ESPACOS, "impeto": C2.IMPETO_ULTIMATE,
            "equipamento": {p: [{"id": k, **o} for k, o in v.items()] for p, v in C2.EQUIPAMENTO.items()},
            "equip_padrao": C2.EQUIPAMENTO_PADRAO,
            "recurso": {"max": C2.RECURSO_MAX, "inicio": C2.RECURSO_INICIO, "turno": C2.RECURSO_TURNO,
                        "basico": C2.RECURSO_BASICO},
            "saves": str(PASTA_SAVES)}


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
            return self._arquivo(TELA4, "index.html")
        if url.path in ("/v3", "/v3/"):
            return self._arquivo(TELA3, "index.html")
        if url.path.startswith("/tela4/"):
            return self._arquivo(TELA4, url.path[len("/tela4/"):])
        if url.path in ("/v2", "/v2/"):
            return self._arquivo(TELA2, "index.html")
        if url.path.startswith("/tela3/"):
            return self._arquivo(TELA3, url.path[len("/tela3/"):])
        if url.path in ("/v1", "/v1/"):
            return self._arquivo(TELA, "index.html")
        if url.path.startswith("/tela/"):
            return self._arquivo(TELA, url.path[len("/tela/"):])
        if url.path.startswith("/tela2/"):
            return self._arquivo(TELA2, url.path[len("/tela2/"):])
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
            if url.path == "/api2/catalogo":
                return self._json(200, catalogo2())
            if url.path == "/api2/estado":
                cb = sessao["combate2"]
                return self._json(200, cb.estado() if cb else {"vazio": True})
            if url.path == "/api2/resultados":
                return self._json(200, {"resultados": sessao["resultados2"], "pasta": str(PASTA_SAVES)})
            m = re.match(r"^/api([34])/(catalogo|estado|resultados)$", url.path)
            if m:
                n, rota = int(m.group(1)), m.group(2)
                if rota == "catalogo":
                    return self._json(200, catalogo_n(n))
                if rota == "estado":
                    cb = sessao[f"combate{n}"]
                    return self._json(200, cb.estado() if cb else {"vazio": True})
                return self._json(200, {"resultados": sessao[f"resultados{n}"], "pasta": str(PASTA_SAVES)})
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
                if url.path.startswith("/api2/"):
                    return self._post2(url.path[len("/api2/"):], corpo)
                m = re.match(r"^/api([34])/(\w+)$", url.path)
                if m:
                    return _post_n(int(m.group(1)), self, m.group(2), corpo)
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

    def _post2(self, rota, corpo):
        build = corpo.get("build") if corpo.get("build") in C2.BUILDS else None
        if rota == "ficha":
            atr = _atr2(corpo, exata=False)
            kit = corpo.get("kit", C2.BUILDS[build]["kit"] if build else [])
            erro_kit = R2.validar_kit(kit)
            f = R2.ficha(atr, [] if erro_kit else kit, corpo.get("equip"), _presenca(corpo), build or "livre")
            f["erro_kit"] = erro_kit
            f["erro_atributos"] = R2.validar_atributos(atr)
            f["equipamento"] = {p: R2.comparar_equipamento(atr, [] if erro_kit else kit, p) for p in ("arma", "foco")}
            return self._json(200, f)
        if rota == "comparar":
            return self._json(200, R2.comparar_builds(corpo.get("equip")))
        if rota == "iniciar":
            enc = corpo.get("encontro")
            if enc not in C2.ENCONTROS:
                return self._json(400, {"erro": "encontro desconhecido"})
            atr = _atr2(corpo) if corpo.get("atributos") else None
            _guardar_resultado2(sessao["combate2"], "reiniciado")
            sessao["combate2"] = R2.Combate(enc, build or "forca", atr, corpo.get("kit"), corpo.get("equip"),
                                            _presenca(corpo))
            return self._json(200, sessao["combate2"].estado())
        if rota == "agir":
            cb = sessao["combate2"]
            if not cb:
                return self._json(409, {"ok": False, "motivo": "Nenhuma luta."})
            r = cb.agir(corpo.get("turno_id"), str(corpo.get("acao", "")), corpo.get("alvo"))
            if cb.fim:
                _guardar_resultado2(cb, cb.fim)
            return self._json(200, {**r, "estado": cb.estado()})
        if rota == "situacao":
            return self._json(200, R2.situacao(_atr2(corpo, exata=False), _presenca(corpo), corpo.get("escolha"),
                                               bool(corpo.get("ajuda"))))
        return self._json(404, {"erro": "nada aqui"})


# ---------------------------------------------------------------- v3 e v4 (as mesmas rotas, cada uma com o seu motor)
MOTORES = {3: (C3, R3), 4: (C4, R4)}


def _guardar_resultado_n(n, cb, como):
    if cb is None or cb.resumo.get("anotado"):
        return
    cb.resumo["anotado"] = True
    C, _ = MOTORES[n]
    h = cb.c["heroi"]
    r = {"encontro": cb.encontro, "nome": cb.cfg["nome"], "build": cb.build, "atributos": h.atr, "presenca": cb.presenca,
         "kit": h.kit, "kit_nomes": [C.HABILIDADES[k]["nome"] for k in h.kit], "equip": h.equip,
         "fim": cb.fim or como, "rodadas": cb.rodada, "quedas": cb.resumo["quedas"],
         "dano_recebido": cb.resumo["dano_recebido"], "acoes": cb.resumo["acoes"], "recurso": cb.resumo["recurso"],
         "ameacas": cb.resumo["ameacas"], "adiamentos": cb.resumo["adiamentos"], "controles": cb.resumo["controles"],
         "ultimates": cb.resumo["ultimates"], "linha": cb.resumo["linha"], "hora": time.strftime("%H:%M:%S")}
    sessao[f"resultados{n}"].append(r)
    _gravar()


def _atr_n(n, corpo, exata=True):
    C, R = MOTORES[n]
    atr = corpo.get("atributos")
    if not atr:
        b = C.BUILDS.get(corpo.get("build") or "forca")
        return dict(b["atributos"]) if b else None
    atr = {k: int(atr[k]) for k in C.ATRIBUTOS}
    erro = R.validar_atributos(atr)
    if erro and (exata or not erro.startswith("A soma")):
        raise ValueError(erro)
    return atr


def _presenca_n(n, corpo):
    C, _ = MOTORES[n]
    p = int(corpo.get("presenca") or C.PRESENCA_PADRAO)
    if not (C.ATRIBUTO_MIN <= p <= C.ATRIBUTO_MAX):
        raise ValueError("Presença vai de 1 a 10.")
    return p


def catalogo_n(n):
    C, R = MOTORES[n]
    return {"versao": n,
            "encontros": [{"id": k, "nome": v["nome"], "tipo": v["tipo"], "objetivo": v["objetivo"], "teste": v.get("teste")}
                          for k, v in C.ENCONTROS.items()],
            "builds": [{"id": k, **v} for k, v in C.BUILDS.items()],
            "atributos": [{"id": a, "nome": C.NOME_ATRIBUTO[a], "sigla": C.SIGLA[a], "funcao": C.FUNCAO[a]}
                          for a in C.ATRIBUTOS],
            "orcamento": C.ORCAMENTO, "min": C.ATRIBUTO_MIN, "max": C.ATRIBUTO_MAX, "presenca": C.PRESENCA_PADRAO,
            "habilidades": [{"id": k, "nome": h["nome"], "tier": h["tier"], "pontos": C.PONTOS_TIER[h["tier"]],
                             "custo": h["custo"], "desc": h["desc"], "alvo": h["alvo"], "origem": h["origem"],
                             "info": R.descrever(h)}
                            for k, h in C.HABILIDADES.items() if "tier" in h],
            "origens": C.ORIGEM,
            "basicos": [{"id": k, "nome": C.HABILIDADES[k]["nome"], "desc": C.HABILIDADES[k]["desc"]} for k in C.BASICOS],
            "kit_pontos": C.KIT_PONTOS, "kit_espacos": C.KIT_ESPACOS,
            "equipamento": {p: [{"id": k, **o} for k, o in v.items()] for p, v in C.EQUIPAMENTO.items()},
            "equip_padrao": C.EQUIPAMENTO_PADRAO,
            "recurso": {"base": C.RECURSO_BASE, "nivel": C.RECURSO_NIVEL, "vontade": C.RECURSO_VONTADE,
                        "turno": C.RECURSO_TURNO, "basico": C.RECURSO_BASICO},
            "saves": str(PASTA_SAVES)}


def _post_n(n, self, rota, corpo):
    C, R = MOTORES[n]
    build = corpo.get("build") if corpo.get("build") in C.BUILDS else None
    if rota == "ficha":
        atr = _atr_n(n, corpo, exata=False)
        kit = corpo.get("kit", C.BUILDS[build]["kit"] if build else [])
        erro_kit = R.validar_kit(kit)
        f = R.ficha(atr, [] if erro_kit else kit, corpo.get("equip"), _presenca_n(n, corpo), build or "livre")
        f["erro_kit"] = erro_kit
        f["erro_atributos"] = R.validar_atributos(atr)
        f["equipamento"] = {p: R.comparar_equipamento(atr, [] if erro_kit else kit, p) for p in C.EQUIPAMENTO}
        if hasattr(R, "comparar_fogo") and not erro_kit:
            f["fogo"] = R.comparar_fogo(atr, kit, corpo.get("equip"))
        return self._json(200, f)
    if rota == "comparar":
        return self._json(200, R.comparar_builds(corpo.get("equip")))
    if rota == "iniciar":
        enc = corpo.get("encontro")
        if enc not in C.ENCONTROS:
            return self._json(400, {"erro": "encontro desconhecido"})
        atr = _atr_n(n, corpo) if corpo.get("atributos") else None
        _guardar_resultado_n(n, sessao[f"combate{n}"], "reiniciado")
        sessao[f"combate{n}"] = R.Combate(enc, build or "forca", atr, corpo.get("kit"), corpo.get("equip"),
                                          _presenca_n(n, corpo))
        return self._json(200, sessao[f"combate{n}"].estado())
    if rota == "agir":
        cb = sessao[f"combate{n}"]
        if not cb:
            return self._json(409, {"ok": False, "motivo": "Nenhuma luta."})
        r = cb.agir(corpo.get("turno_id"), str(corpo.get("acao", "")), corpo.get("alvo"))
        if cb.fim:
            _guardar_resultado_n(n, cb, cb.fim)
        return self._json(200, {**r, "estado": cb.estado()})
    if rota == "situacao":
        return self._json(200, R.situacao(_atr_n(n, corpo, exata=False), _presenca_n(n, corpo), corpo.get("escolha"),
                                          bool(corpo.get("ajuda"))))
    return self._json(404, {"erro": "nada aqui"})


def servir(porta=PORTA):
    srv = ThreadingHTTPServer(("127.0.0.1", porta), Demo)
    srv.daemon_threads = True
    return srv


def main():
    srv = servir()
    print(f"http://127.0.0.1:{srv.server_address[1]}/", flush=True)
    print(f"v3, v2 e v1 em http://127.0.0.1:{srv.server_address[1]}/v3/, /v2/ e /v1/", flush=True)
    print(f"resultados da sessão em {PASTA_SAVES}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
