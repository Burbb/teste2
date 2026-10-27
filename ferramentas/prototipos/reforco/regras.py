"""Reforço garantido, materiais do grupo e desmontagem: as regras do protótipo (etapa 4, roadmapIDEIAS/25, seção 5).

O jogo não carrega este arquivo: só a demonstração (demo.py) o liga, num save temporário. Todos os números são
hipóteses desta rodada.

5ª versão: o reforço tem chance (o +1 garantido; falha volta um nível, sem quebrar a peça); ver CHANCE abaixo.

O que o reforço melhora: a peça inteira (12ª versão, pedido do Jean em 27/10/2026). Todas as linhas dela, da base e dos
afixos (Ataque, Poder, Defesa, Vida, Mana, Agilidade, Espinhos, Regeneração, Vida por abate, Crítico, Roubo de vida),
cada uma pela regra de crescimento que o jogo já usa para ela: um + vale "a mesma peça alguns níveis acima".
    arma, peito, escudo (apoio do Guerreiro), tomo/foco (apoio do Mago)
    não aceitam aljava (linhas de 1 e 2: qualquer passo inteiro distorce; a propriedade dela fica para decidir),
                cabeça, mãos, pernas e pés (peças complementares, linhas pequenas), anel e amuleto (a identidade
                deles são os afixos)
Não há mais o caminho escolhido na arma do Guerreiro (Fio ou Runas): cresce o que a arma tem.

O ganho: cada passo vale um tanto de níveis de peça (PASSO_NIVEIS: 1,5 do +1 ao +4, 1 do +5 ao +8, 0,75 do +9 ao +12;
L(N) é a soma até +N). Uma linha fixa de valor v numa peça de nível n cresce na proporção da escala do gerador:
G(N) = arredonda(v / escala(n) × 0,75 × L(N)); nas linhas da base dos apoios (pequenas), os passos do +1 ao +4 valem o
dobro. Crítico e roubo de vida, em %,
crescem como no gerador: + 0,25 ponto por nível de peça, G(N) = arredonda(0,25 × L(N)) (o +12: +3%). A linha principal
da arma (a maior) ganha pelo menos 1 por passo; todo passo melhora alguma linha. Uma peça melhor ganha mais por passo; uma
peça antiga reforçada alcança uma base nova por um tempo, não para sempre.

12ª versão (27/10/2026): o limite candidato passa de +4 a +12, com as mesmas regras (o +1 garantido, a falha volta um
nível, sem quebrar). Os números do +1 ao +4 ficam; os do +5 ao +12 são uma curva provisória (simular.py e o LEIA-ME).
"""

import math

from rpg import balanceamento as bal
from rpg import itens

LIMITE = 12
# 5ª versão (26/10/2026): o reforço tem chance (roadmapIDEIAS/25, 5.6). Cada TENTATIVA custa o preço do nível
# pretendido, dê certo ou não. Hipóteses calibradas contra tentativas perdidas e quedas (LEIA-ME, "Chances e custos").
# 12ª versão: do +5 ao +12, a curva provisória (os do +1 ao +4 não mudaram).
OURO = (20, 35, 55, 80, 110, 145, 185, 230, 280, 335, 395, 460)  # tentar o +1, ..., o +12 (antes da reputação)
FRAGMENTOS = (1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6)
CHANCE = {1: 100, 2: 85, 3: 70, 4: 55,                           # % de sucesso pelo nível pretendido (o +1, garantido)
          5: 52, 6: 50, 7: 48, 8: 46, 9: 44, 10: 42, 11: 40, 12: 38}
PENA_RARIDADE = {"comum": 0, "magico": 4, "raro": 8, "lendario": 12}  # pontos a menos (menos que um degrau de nível)
# acima do +4, metade: a queda de um nível compõe a diferença a cada passo (com 4/8/12, o +12 de um lendário pedia
# umas 8 vezes as tentativas de um comum; com 2/4/6, umas 3 vezes; simular.py)
PENA_RARIDADE_ALTA = {"comum": 0, "magico": 2, "raro": 4, "lendario": 6}
# os níveis de peça que cada passo vale (arma e peito; o dobro nos apoios): o passo alto rende menos, para um
# equipamento do começo reforçado não ficar à frente das bases novas para sempre
PASSO_NIVEIS = (1.5,) * 4 + (1.0,) * 4 + (0.75,) * 4
APOIO = 2.0  # as linhas da base dos apoios (escudo, tomo): o dobro do +1 ao +4
BASE_APOIO = {"escudo": ("defesa", "max_hp"), "foco": ("poder", "max_rec")}
PCT_POR_NIVEL = bal.ITEM_AFIXO_FIXO_POR_NIVEL  # crítico e roubo de vida: 0,25 ponto por nível de peça, como no gerador
DA_PECA = {"comum": 0, "magico": 1, "raro": 2, "lendario": 3}   # o material da própria peça ao desmontar
VENDA_DO_OURO = 0.25              # a venda devolve 25% do ouro nominal dos níveis que a peça CONSERVA
PILHA_MAX = 99

MATERIAIS = {
    "fragmento": {"nome": "Fragmento de Têmpera", "plural": "Fragmentos de Têmpera", "icone": "saco",
                  "desc": "O ferreiro usa nos reforços de arma, peito e apoio.",
                  "fontes": "Baús, recompensas e a desmontagem de peças."},
}

NOMES = {"atk": "Ataque", "poder": "Poder", "defesa": "Defesa", "max_hp": "Vida", "max_rec": "Mana", "agi": "Agilidade",
         "critico": "Crítico", "roubo_vida": "Roubo de vida", "espinhos": "Espinhos", "regen_vida": "Regeneração",
         "vida_abate": "Vida por abate"}


def _rh(x):
    """Arredonda meio para cima (o round do Python arredonda 0,5 para o par: 2,5 → 2)."""
    return int(math.floor(x + 0.5))


def _escala(nivel):
    return bal.ITEM_FORCA_BASE + bal.ITEM_FORCA_POR_NIVEL * nivel


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
    """[(stat, q, piso)]: as linhas que o reforço faz crescer (todas as da peça, na ordem dela), a força de cada uma por
    ponto de escala (None nas de %, que crescem por soma) e se tem o piso de +1 por passo (a principal da arma)."""
    if not tipo(item):
        return []
    base = item.get("bonus_base") or item["bonus"]  # a peça de antes do primeiro reforço (o reforço não a altera)
    esc = _escala(item.get("nivel") or 1)
    fixas = [st for st, v in base.items() if v and st not in itens.PERCENTUAIS]
    principal = max(fixas, key=lambda st: (base[st], st in ("atk", "poder")), default=None) if tipo(item) == "arma" else None
    return [(st, None if st in itens.PERCENTUAIS else max(0.3, v / esc), st == principal) for st, v in base.items() if v]


def ganho_total(item, n):
    """O que N reforços somam a cada linha: {stat: valor}."""
    dobra = BASE_APOIO.get(tipo(item), ())  # as linhas da base do apoio (os afixos dele crescem como em qualquer peça)
    ls = linhas(item)
    total = {stat: 0 for stat, _, _ in ls}
    for i in range(1, n + 1):  # passo a passo: cada um melhora alguma linha (também onde o passo alto vale menos)
        antes = dict(total)
        L = sum(PASSO_NIVEIS[:i])
        # os apoios valem o dobro do +1 ao +4 (linhas pequenas: cada passo se sente); do +5, como as outras peças
        Lf = L + sum(PASSO_NIVEIS[:min(i, 4)]) * (APOIO - 1)
        for stat, q, piso in ls:
            w = _rh(PCT_POR_NIVEL * L) if q is None else _rh(q * bal.ITEM_FORCA_POR_NIVEL * (Lf if stat in dobra else L))
            total[stat] = max(antes[stat] + 1, w) if piso else max(antes[stat], w)
        fixas = [(q, st) for st, q, _ in ls if q is not None]
        if fixas and total == antes:  # as linhas pequenas não subiram: a maior linha fixa ganha 1
            total[max(fixas)[1]] += 1
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


def chance(item, alvo):
    """A chance de sucesso (inteiro, %) de tentar o +alvo: o primeiro é garantido; depois, a do nível pretendido menos
    a pena da raridade."""
    if alvo <= 1:
        return 100
    pena = PENA_RARIDADE if alvo <= 4 else PENA_RARIDADE_ALTA
    return CHANCE[alvo] - pena.get(item.get("raridade", "comum"), 0)


def nominal(n):
    """O custo nominal dos níveis +1..+n (um passo de cada, sem as tentativas perdidas): (ouro, fragmentos)."""
    return sum(OURO[:n]), sum(FRAGMENTOS[:n])


def desmontar_rende(item):
    """O que desmontar devolve: (do reforço, da própria peça). Metade dos fragmentos nominais dos níveis que a peça
    conserva, arredondada para cima, mais o material da peça pela raridade. Tentativas que falharam não contam."""
    return math.ceil(nominal(item.get("reforco", 0))[1] / 2), DA_PECA.get(item.get("raridade", "comum"), 0)


def preco_com_reforco(item):
    """O preço da peça com os níveis que ela conserva: a venda (metade do preço) devolve 25% do ouro nominal deles."""
    base = item.get("preco_base", item.get("preco", 0))
    return base + int(nominal(item.get("reforco", 0))[0] * VENDA_DO_OURO * 2)
