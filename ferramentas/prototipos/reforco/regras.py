"""Reforço garantido, materiais do grupo e desmontagem: as regras do protótipo (etapa 4, roadmapIDEIAS/25, seção 5).

O jogo não carrega este arquivo: só a demonstração (demo.py) o liga, num save temporário. Todos os números são
hipóteses desta rodada.

O que o reforço melhora (a função principal da peça, as linhas da BASE, nunca os afixos nem os especiais):
    arma        Guerreiro: Ataque (Fio) ou Poder (Runas, o caminho arcano), escolhido no primeiro reforço;
                Arqueiro: Ataque; Mago: Poder. Piso de +1 por passo (linha única: cada passo se sente)
    peito       Defesa e Vida (a proteção da base)
    escudo      Defesa e Vida            (apoio do Guerreiro)
    tomo/foco   Poder e Mana             (apoio do Mago)
    não aceitam aljava (linhas de 1 e 2: qualquer passo inteiro distorce; a propriedade dela fica para decidir),
                cabeça, mãos, pernas e pés (peças complementares, linhas pequenas), anel e amuleto (a identidade
                deles são os afixos)

O ganho: cada + vale K níveis de peça na linha da base, na mesma proporção que a base tem (a qualidade do material e
o peso da linha): G(N) = arredonda(q × 0,75 × K × N), com q = força da linha por ponto de escala (o material × o
peso da linha no gerador, itens.gerar_equip). K = 1,5 em arma e peito; 3 nos apoios (linhas menores). Uma base
melhor ganha mais por passo; uma peça antiga reforçada alcança uma base nova por um tempo, não para sempre.
"""

import math

from rpg import balanceamento as bal
from rpg import itens

LIMITE = 4
OURO = (25, 50, 90, 140)          # do +0 para o +1, ..., do +3 para o +4 (antes do desconto da reputação)
FRAGMENTOS = (1, 2, 3, 4)
K_PECA, K_APOIO = 1.5, 3.0
DA_PECA = {"comum": 0, "magico": 1, "raro": 2, "lendario": 3}   # o material da própria peça ao desmontar
VENDA_DO_OURO = 0.25              # a venda devolve 25% do ouro investido (o preço da peça sobe metade do gasto)
PILHA_MAX = 99

MATERIAIS = {
    "fragmento": {"nome": "Fragmento de Têmpera", "plural": "Fragmentos de Têmpera", "icone": "saco",
                  "desc": "O ferreiro usa nos reforços de arma, peito e apoio.",
                  "fontes": "Baús, recompensas e a desmontagem de peças."},
}

NOMES = {"atk": "Ataque", "poder": "Poder", "defesa": "Defesa", "max_hp": "Vida", "max_rec": "Mana", "agi": "Agilidade"}
PESO_ARMADURA = {"guerreiro": 0.7, "arqueiro": 0.5, "mago": 0.35}


def _rh(x):
    """Arredonda meio para cima (o round do Python arredonda 0,5 para o par: 2,5 → 2)."""
    return int(math.floor(x + 0.5))


def _escala(nivel):
    return bal.ITEM_FORCA_BASE + bal.ITEM_FORCA_POR_NIVEL * nivel


def _material(item):
    """O multiplicador do material, lido do nome da base ("Espada de Aço" → 1,0); peças sem material, 1,0."""
    base = item.get("base") or ""
    for lista in (itens.MATERIAIS, itens.MATERIAIS_COURO, itens.MATERIAIS_TECIDO):
        for m, f, mult in lista:
            if base.endswith(" " + m) or base.endswith(" " + f):
                return mult
    return 1.0


def tipo(item):
    """arma, peito, escudo, foco, ou None (não aceita reforço)."""
    s = item.get("slot")
    if s == "arma":
        return "arma"
    if s == "armadura":
        return "peito"
    if s == "secundaria":
        return {"guerreiro": "escudo", "mago": "foco"}.get(item.get("classe"))
    return None


def motivo_sem_reforco(item):
    s = item.get("slot")
    if s == "secundaria" and item.get("classe") == "arqueiro":
        return "A aljava não recebe reforço."
    if s in ("anel", "amuleto"):
        return "Anéis e amuletos não recebem reforço."
    if s in ("cabeca", "maos", "pernas", "pes"):
        return "Só arma, peito e apoio recebem reforço."
    return None


def linhas(item):
    """[(stat, q, piso)]: as linhas que o reforço faz crescer, a força de cada uma por ponto de escala e se tem o piso
    de +1 por passo. A arma do Guerreiro segue o veio escolhido (Fio ou Runas)."""
    t = tipo(item)
    if not t:
        return []
    classe = item.get("classe")
    unico = item.get("unico")
    esc = _escala(item.get("nivel") or 1)

    def q(stat, peso):
        if unico:  # o único não tem material: a linha dele é intrínseca
            return max(0.3, item["bonus"].get(stat, 0) / esc)
        return _material(item) * peso
    if t == "arma":
        if classe == "mago":
            return [("poder", q("poder", 1.0), True)]
        if classe == "arqueiro":
            return [("atk", q("atk", 0.8), True)]
        qa = q("atk", 1.0)
        return [("poder" if item.get("veio") == "runas" else "atk", qa, True)]
    if t == "peito":
        return [("defesa", q("defesa", PESO_ARMADURA.get(classe, 0.6)), False), ("max_hp", q("max_hp", 2.0), False)]
    if t == "escudo":
        return [("defesa", q("defesa", 0.65 * 0.55), False), ("max_hp", q("max_hp", 0.65 * 0.8), False)]
    return [("poder", q("poder", 0.65 * 0.45), False), ("max_rec", q("max_rec", 0.65 * 1.5), False)]


def ganho_total(item, n):
    """O que N reforços somam a cada linha: {stat: valor}."""
    k = K_APOIO if tipo(item) in ("escudo", "foco") else K_PECA
    total = {}
    for stat, q, piso in linhas(item):
        v = _rh(q * bal.ITEM_FORCA_POR_NIVEL * k * n)
        total[stat] = max(n, v) if piso else v
    return total


def proximo(item):
    """O ganho do próximo passo, {stat: +x}, ou None no limite / sem reforço."""
    n = item.get("reforco", 0)
    if not tipo(item) or n >= LIMITE:
        return None
    a, b = ganho_total(item, n), ganho_total(item, n + 1)
    return {s: b[s] - a.get(s, 0) for s in b if b[s] - a.get(s, 0)}


def custo(n):
    """O custo do passo de +n para +n+1: (ouro antes da reputação, fragmentos)."""
    return OURO[n], FRAGMENTOS[n]


def texto_ganho(g):
    return ", ".join(f"+{v} {NOMES.get(s, s)}" for s, v in g.items() if v)


def desmontar_rende(item):
    """O que desmontar devolve: (do investimento, da própria peça). Metade dos fragmentos investidos, arredondada
    para cima, mais o material da peça pela raridade."""
    investido = (item.get("reforco_gasto") or {}).get("fragmento", 0)
    return math.ceil(investido / 2), DA_PECA.get(item.get("raridade", "comum"), 0)
