"""Protótipo da vida máxima bloqueada (etapa 1B do plano 23): o cenário de teste do jogo (tests/navegador/cenarios.py)
com o estado do herói acrescido do que a tela precisa para mostrar o bloqueio. Nada aqui muda regra: os números vêm das
contas do motor e só são lidos.

  vida_bloqueio = {"saudavel": a vida máxima sem as penalidades (Jogador.totais: base + talentos + equipamento),
                   "limite": a vida máxima de agora (max_hp, com ferimentos e fome),
                   "fontes": [{"nome", "pct", "perda"}, ...] (sobrevivencia.fontes_penalidade, na ordem da conta)}

Só existe quando o limite está abaixo do saudável; sem penalidade, o estado é o de sempre. A perda de cada fonte é a
diferença que ela faz na ordem em que entra na conta (as penalidades se multiplicam), e a soma fecha exatamente com
saudavel − limite.

    python ferramentas/prototipos/hud/vida-bloqueada/cenario.py tutorial   (o mesmo ambiente do cenário: FERIMENTOS=corte...)
Além do ambiente do cenário: PECA_VIDA=1 oferece, na chegada, uma peça de pernas com +vida máxima (gerada pelo jogo), na
janela do achado de sempre, para conferir a troca de equipamento.
"""
import os
import pathlib
import random
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))

from rpg import itens, sobrevivencia  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.web import estado as estado_web  # noqa: E402
from tests.navegador import cenarios  # noqa: E402


def vida_bloqueio(j):
    totais, _ = j.totais()
    saudavel = max(1, int(round(totais["max_hp"])))
    if j.max_hp >= saudavel:
        return None
    fontes, valor = [], float(totais["max_hp"])
    for nome, fator in sobrevivencia.fontes_penalidade(j).get("max_hp", []):
        depois = valor * fator
        fontes.append({"nome": nome, "pct": round((1 - fator) * 100), "perda": round(valor) - round(depois)})
        valor = depois
    # o arredondamento final do motor (max(1, round(total × fatores))) fecha a soma
    if fontes:
        fontes[-1]["perda"] += (saudavel - j.max_hp) - sum(f["perda"] for f in fontes)
    return {"saudavel": saudavel, "limite": j.max_hp, "fontes": fontes}


_heroi = estado_web.heroi


def heroi(g):
    d = _heroi(g)
    b = vida_bloqueio(g.j)
    if b:
        d["vida_bloqueio"] = b
    return d


estado_web.heroi = heroi

if os.environ.get("PECA_VIDA"):
    _rodar = Jogo.rodar

    def rodar(self, *a, **k):
        r = random.Random(1)
        peca = next(e for e in iter(lambda: itens.gerar_equip(r, self.j.classe, self.j.nivel, slot="pernas"), None)
                    if e["bonus"].get("max_hp", 0) >= 6)
        self.oferecer_equip(peca)  # a janela do achado, com o Equipar de sempre (as regras de vestir do jogo)
        return _rodar(self, *a, **k)
    Jogo.rodar = rodar

if __name__ == "__main__":
    cenarios.main()
