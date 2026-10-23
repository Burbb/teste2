"""O cenário "tutorial" dos testes de navegador (GRUPO=cria_vazio:1), com uma troca só do protótipo: quando a luta começa,
o antagonista do mundo gerado entra na frente, montado pelo jogo (inimigos.instanciar_antagonista), com o título pedido
(TITULO, G: "Noiva da Peste", "f"), para ver a carta dele ao lado da Cria do Vazio que ele invoca. Nada do jogo muda.
    PYTHONPATH=<raiz> GRUPO=cria_vazio:1 TITULO="Noiva da Peste" G=f python cenario_antagonista.py tutorial
"""
import os

from tests.navegador import cenarios

from rpg import balanceamento as bal
from rpg import comitiva
from rpg.inimigos import instanciar_antagonista

_preparar = comitiva.preparar_combate


def com_o_antagonista(cb):
    _preparar(cb)
    titulo, g = os.environ.get("TITULO", "Noiva da Peste"), os.environ.get("G", "f")
    a = {"nome": f"Vharuk, {titulo}", "curto": titulo, "g": g, "origem": ""}
    cb.inimigos.insert(0, instanciar_antagonista(a, bal.ANTAGONISTA_NIVEL))


comitiva.preparar_combate = com_o_antagonista

if __name__ == "__main__":
    cenarios.main()
