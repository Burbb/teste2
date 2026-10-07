"""Atalhos de desenvolvimento: um herói já no nível N, com o equipamento que se teria por lá.

Usado por `python jogar.py --dev N` (para sentir o meio e o fim do jogo sem jogar horas até lá) e pelo
simulador de equilíbrio (tests/equilibrio.py), que monta heróis típicos de cada classe e nível.
"""

from .itens import gerar_equip, rolar_raridade
from .mundo import nivel_regiao
from . import talentos

# Quantos dos espaços de equipamento um herói costuma ter ocupados em cada nível (fora a arma, sempre):
# no nível 3, uns cinco; do 7 em diante, todos (é o que a partida do Xatuba mostra).
OCUPACAO_BASE = 0.15
OCUPACAO_POR_NIVEL = 0.13
ATRASO_EQUIPAMENTO = 1  # o equipamento vem de inimigos e lojas um pouco abaixo do seu nível


def subir_ate(g, nivel, spec=None, animal=None):
    """Sobe de nível como no jogo (atributos, habilidades, pontos de talento). No 4, especializa: `spec`, ou
    a primeira da classe se nenhuma for dada; com `spec=False`, deixa a encruzilhada acontecer no jogo."""
    j = g.j
    while j.nivel < nivel:
        g.subir_nivel()
        if j.nivel >= 4 and not j.spec and spec is not False:
            from .classes import CLASSES
            g.especializar(spec or CLASSES[j.classe]["specs"][0])
            if animal and j.companheiro and j.companheiro["tipo"] != animal:
                g.escolher_companheiro(animal)
            enc = f"encruzilhada_{j.classe}"
            if enc in g.forcados:
                g.forcados.remove(enc)


def gastar_talentos(g, rng):
    """Gasta os pontos ao acaso entre os talentos disponíveis (uma build qualquer, mas possível)."""
    j = g.j
    while j.pontos_talento:
        livres = [t for t in talentos.TALENTOS[j.classe] if talentos.estado(j, t) == "disponivel"]
        if not livres:
            return
        t = rng.choice(livres)
        j.pontos_talento -= 1
        j.talentos[t["id"]] = j.tal(t["id"]) + 1
    j.recalcular()


def vestir(g, rng, nivel):
    """Equipamento sorteado como o do jogo, no nível de quem chegou até aqui."""
    j = g.j
    nv_item = max(1, nivel - ATRASO_EQUIPAMENTO)
    ocupacao = min(1.0, OCUPACAO_BASE + OCUPACAO_POR_NIVEL * nivel)
    for espaco in j.equip:
        if espaco != "arma" and rng.random() >= ocupacao:
            continue
        slot = "anel" if espaco.startswith("anel") else espaco
        j.equip[espaco] = gerar_equip(rng, j.classe, nv_item, slot, raridade=rolar_raridade(rng))
    j.recalcular()
    j.hp, j.rec = j.max_hp, j.max_rec


def ir_para_regiao(g, nivel):
    """Leva o herói à vila mais perigosa que ainda fica abaixo do nível dele (onde alguém do nível N estaria)."""
    vilas = [l for l in g.mundo["locais"] if l["tipo"] == "vila"]
    alvo = max((l for l in vilas if nivel_regiao(l) < nivel), key=nivel_regiao, default=vilas[0])
    g.mundo["atual"] = alvo["id"]
    alvo["visitado"] = True


def comecar_no_nivel(g, nivel):
    """O `--dev N`: o herói recém-criado vira um herói de nível N. Os pontos de talento ficam para você gastar
    e a especialização vem pela encruzilhada, como no jogo."""
    j = g.j
    subir_ate(g, nivel, spec=False)
    vestir(g, g.rng, nivel)
    j.ouro += 40 * (nivel - 1)
    j.consumiveis["pocao_vida"] = j.consumiveis.get("pocao_vida", 0) + 2
    j.provisoes += 4
    ir_para_regiao(g, nivel)
    g.dizer(f"[dev] Você começa no nível {j.nivel}, em {g.loc['nome']}, com {j.pontos_talento} pontos de talento "
            "para gastar.", "magenta")
