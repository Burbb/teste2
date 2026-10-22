"""O cenário "tutorial" dos testes de navegador, com uma troca só do protótipo: ANTAGONISTA=1 faz a luta preparada ser
contra o antagonista do mundo gerado (o campanha não tem um) e duas crias do Vazio invocadas, criadas como o Invocar
dele as cria (inimigos._invocar: a família cria_vazio, dois níveis abaixo, com a letra e "(invocado)" no nome). Serve
para conferir a cria como invocação, com o mesmo retrato da família. Nada do jogo muda.
    PYTHONPATH=<raiz> python cenario_vazio.py tutorial      (com as variáveis do tutorial: GRUPO, NIVEL_LUTA, ...)
"""
import os
import random

from tests.navegador import cenarios

from rpg.inimigos import criar, instanciar_antagonista
from rpg.mundo import gerar_mundo

lutar = cenarios.lutar


def lutar_com_o_antagonista(g, inimigos, **kw):
    if os.environ.get("ANTAGONISTA"):
        nv = int(os.environ.get("NIVEL_LUTA", "6"))
        ant = instanciar_antagonista(gerar_mundo(random.Random(5))["antagonista"], nv)
        crias = [criar(random.Random(k), "cria_vazio", max(1, nv - 2)) for k in range(2)]
        for letra, c in zip("AB", crias):
            c.nome = f"{c.nome} {letra} (invocado)"
            c.invocado = True
        inimigos = [ant] + crias
    lutar(g, inimigos, **kw)


cenarios.lutar = lutar_com_o_antagonista

if __name__ == "__main__":
    cenarios.main()
