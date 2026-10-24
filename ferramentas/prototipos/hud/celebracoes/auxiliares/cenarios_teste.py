"""CENÁRIOS DE TESTE da etapa 2 (subida de nível, celebrações e raridade; 23/10/2026): situações possíveis pelas
regras, montadas pelos caminhos reais do motor (o quadro do espólio, `ganhar_xp`, `oferecer_equip`), com as fichas e o XP
reais dos inimigos. Não mudam balanceamento, chances de raridade, recompensas nem progressão; só põem o herói perto do
momento a fotografar. Ficam fora de tests/ (não são testes do jogo) e do jogo.

    python cenarios_teste.py nivel          # TESTE: a vitória sobre dois lobos leva do nível 1 ao 2 (habilidade nova)
    python cenarios_teste.py dois_niveis    # TESTE: o espólio da Capela (a Ilse, nível 3, e dois afogados) leva do 1 ao 3
    python cenarios_teste.py raridades      # TESTE: quatro achados seguidos, um de cada raridade (comum a lendário)

CLASSE (guerreiro, mago, arqueiro). Imprime o endereço na primeira linha, como tests/navegador/cenarios.py.
"""
import os
import random
import sys
import tempfile
import threading
import time
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5]))
from rpg.inimigos import instanciar_guardiao  # noqa: E402
from rpg.itens import gerar_equip  # noqa: E402
from rpg.jogo import FimDeJogo, Jogo  # noqa: E402
from rpg.web.ponte import WebUI  # noqa: E402
from rpg.web.servidor import Servidor  # noqa: E402


def heroi(ui):
    """A campanha no Vau, de manhã, com o herói a 25 de 30 XP do nível 1 (falta pouco para o 2)."""
    g = Jogo(ui, seed=int(os.environ.get("SEMENTE", "5")), pasta_saves=tempfile.mkdtemp(), hardcore=False)
    ui.jogo = g
    g.iniciar("Jean", os.environ.get("CLASSE", "guerreiro"), "turvo")
    from rpg import abertura as ab
    ab.comecar(g, False)
    g.mundo["abertura"].update(despensa="feita", caneca=False)
    g.mundo["abertura"]["vistas"] = ["combate", "V1"]
    g.periodo, g.clima = 0, "limpo"
    g.j.xp = 25
    # TESTE: uma pergunta de partida, para a festa acontecer com a página aberta (a que chega antes de a página
    # conectar é reposta sem cerimônia, de propósito)
    g.menu("Cenário de teste da etapa 2", [("Começar o teste", True)])
    return g


def espolio(g, inimigos, consumiveis=()):
    """O quadro do espólio de uma vitória sobre `inimigos` (o ouro e o XP deles, como a luta daria) e o que se achou."""
    g.abrir_espolio()
    g.ganhar_ouro(sum(e.ouro for e in inimigos), fonte="lutas")
    g.ganhar_xp(sum(e.xp for e in inimigos))
    for item, qtd in consumiveis:
        g.dar(item, qtd)


def rodar(g):
    try:
        g.rodar()
    except FimDeJogo:
        pass


def nivel(ui):
    g = heroi(ui)
    espolio(g, [g.inimigo("lobo", nivel=1) for _ in range(2)])
    rodar(g)


def dois_niveis(ui):
    g = heroi(ui)
    ilse = instanciar_guardiao({"id": "ilse", "nome": "Ilse"}, 3)
    espolio(g, [ilse] + [g.inimigo("afogado", nivel=3) for _ in range(2)], consumiveis=[("bandagem", 1)])
    rodar(g)


def raridades(ui):
    g = heroi(ui)
    rng = random.Random(9)
    for rar in ("comum", "magico", "raro", "lendario"):
        g.oferecer_equip(gerar_equip(rng, g.j.classe, 3, raridade=rar))
    rodar(g)


CENARIOS = {"nivel": nivel, "dois_niveis": dois_niveis, "raridades": raridades}


def main():
    nome = sys.argv[1] if len(sys.argv) > 1 else "nivel"
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, config={"velocidade": os.environ.get("VELOCIDADE", "normal")}).iniciar()
    print(srv.url, flush=True)
    threading.Thread(target=CENARIOS[nome], args=(ui,), daemon=True).start()
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
