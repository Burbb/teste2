"""Comparação jogável da direção visual da HUD: produção × protótipo, com os mesmos dados (em avaliação, nada no jogo).

Abre o jogo como `python jogar.py` (a janela própria do pywebview, a de sempre), mas com uma pasta de saves só do
teste, onde entra uma CÓPIA do save escolhido. O save original não é tocado e o que se salvar no teste fica na pasta
do teste, uma para cada versão (as duas começam do mesmo ponto e não se misturam):

  %USERPROFILE%\\.cronicas_da_fenda_teste_hud\\producao\\
  %USERPROFILE%\\.cronicas_da_fenda_teste_hud\\prototipo\\

No protótipo, o estudo completo entra por cima do jogo, só neste processo: ao entregar app/controles.js, o servidor
acrescenta as folhas e os scripts do estudo (a ficha com a pintura, o conjunto e o topo), e entrega a arte em
/proto-ficha, /proto-conjunto e /proto-topo. Nenhum arquivo do jogo muda; em produção, nada é acrescentado.

  python ferramentas/prototipos/hud/direcao/comparar/jogar_comparacao.py producao
  python ferramentas/prototipos/hud/direcao/comparar/jogar_comparacao.py prototipo
  ... [--save turvo_chimpa] [--recomecar] [--navegador]

--save: o nome do save (sem .json) na pasta de sempre (padrão: o mais recente quando a pasta do teste foi criada,
turvo_dadad). --recomecar: copia o save de novo por cima do da pasta do teste (volta ao ponto de partida).
"""

import argparse
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DIRECAO = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(DIRECAO, "..", "..", "..", ".."))
SAVES = os.path.join(os.path.expanduser("~"), ".cronicas_da_fenda")
TESTE = os.path.join(os.path.expanduser("~"), ".cronicas_da_fenda_teste_hud")

# o estudo completo, na ordem em que as camadas se sobrepõem
CSS = ["ficha/ficha.css", "ficha/pintura.css", "conjunto/conjunto.css", "topo/topo.css"]
JS = ["ficha/ficha.js", "ficha/pintura.js", "conjunto/conjunto.js", "direcao.js"]
ARTE = {"/proto-ficha/": os.path.join(DIRECAO, "ficha", "arte"), "/proto-conjunto/": os.path.join(DIRECAO, "conjunto", "pecas"),
        "/proto-topo/": os.path.join(DIRECAO, "topo", "pecas")}
PINTURA = os.path.join(DIRECAO, "Painel vertical em tinta escura.png")   # /proto-ficha/painel-tinta.png


def ler(rel):
    with open(os.path.join(DIRECAO, rel), encoding="utf-8") as f:
        return f.read()


def preparar_saves(versao, save, recomecar):
    origem = os.path.join(SAVES, f"{save}.json")
    if not os.path.isfile(origem):
        sys.exit(f"Save não encontrado: {origem}")
    pasta = os.path.join(TESTE, versao)
    os.makedirs(pasta, exist_ok=True)
    destino = os.path.join(pasta, f"{save}.json")
    if recomecar or not os.path.exists(destino):
        shutil.copy2(origem, destino)   # só lê o original
        print(f"Cópia do save: {origem} -> {destino}")
    else:
        print(f"Continuando o save do teste: {destino} (--recomecar volta ao original)")
    return pasta


def instalar_prototipo():
    """Troca, só neste processo, a fábrica do servidor HTTP do jogo por uma que acrescenta o estudo."""
    from http.server import ThreadingHTTPServer
    from rpg.web import servidor

    extra_css = "\n".join(ler(c) for c in CSS)
    extra_js = "\n".join(ler(j) for j in JS)
    import json
    injecao = (f"\n;(() => {{ const s = document.createElement('style'); s.id = 'estudo-hud'; "
               f"s.textContent = {json.dumps(extra_css)}; document.head.appendChild(s); }})();\n{extra_js}\n").encode("utf-8")

    def envolver(Handler):
        class ComEstudo(Handler):
            def do_GET(self):
                caminho = self.path.split("?")[0]
                for prefixo, pasta in ARTE.items():
                    if caminho.startswith(prefixo):
                        nome = os.path.basename(caminho)
                        arquivo = PINTURA if nome == "painel-tinta.png" else os.path.join(pasta, nome)
                        if not os.path.isfile(arquivo):
                            return self._responder(404)
                        with open(arquivo, "rb") as f:
                            return self._responder(200, f.read(), "image/png")
                return super().do_GET()

            def _arquivo(self, relativo):
                if relativo.replace("\\", "/") != "app/controles.js":
                    return super()._arquivo(relativo)
                with open(os.path.join(servidor.PASTA, "app", "controles.js"), "rb") as f:
                    corpo = f.read() + injecao
                self._responder(200, corpo, "text/javascript; charset=utf-8")
        return ComEstudo

    servidor.ThreadingHTTPServer = lambda endereco, Handler: ThreadingHTTPServer(endereco, envolver(Handler))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("versao", choices=["producao", "prototipo"])
    p.add_argument("--save", default="turvo_dadad")
    p.add_argument("--recomecar", action="store_true")
    p.add_argument("--navegador", action="store_true", help="abre no navegador em vez da janela própria")
    p.add_argument("--sem-abrir", action="store_true", help="só sobe o jogo e mostra o endereço (para conferir)")
    a = p.parse_args()
    pasta = preparar_saves(a.versao, a.save, a.recomecar)
    sys.path.insert(0, RAIZ)
    if a.versao == "prototipo":
        instalar_prototipo()
    print(f"Versão: {a.versao.upper()} · saves do teste em {pasta}. No menu: Carregar jogo.")
    sys.argv = ["jogar.py", "--saves", pasta] + (["--navegador"] if a.navegador or a.sem_abrir else []) + (["--sem-abrir"] if a.sem_abrir else [])
    from rpg.__main__ import main as jogo
    jogo()


if __name__ == "__main__":
    main()
