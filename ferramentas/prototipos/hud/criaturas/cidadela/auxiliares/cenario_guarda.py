"""O cenário "tutorial" dos testes de navegador, com uma troca só do protótipo: ULTIMO_GUARDA=1 faz a luta preparada ser
contra o Último Guarda, criado como sistemas/chefes.py o cria (a família cavaleiro_sombrio, um nome próprio, um nível
acima). Serve para conferir o retrato da família no guarda de nome próprio. Nada do jogo muda.
    PYTHONPATH=<raiz> python cenario_guarda.py tutorial      (com as variáveis do tutorial: GRUPO, NIVEL_LUTA, ...)
"""
import os
import random

from tests.navegador import cenarios

from rpg import texto as tx
from rpg.inimigos import criar

lutar = cenarios.lutar


def lutar_com_o_guarda(g, inimigos, **kw):
    if os.environ.get("ULTIMO_GUARDA"):
        rng = random.Random(7)
        nv = int(os.environ.get("NIVEL_LUTA", "6"))
        inimigos = [criar(rng, "cavaleiro_sombrio", nv + 1, None, tx.nome_proprio(rng))]
    lutar(g, inimigos, **kw)


cenarios.lutar = lutar_com_o_guarda

if __name__ == "__main__":
    cenarios.main()
