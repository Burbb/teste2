"""Reforço garantido, materiais do grupo e desmontagem: as regras do protótipo (etapa 4, roadmapIDEIAS/25, seção 5).

O jogo não carrega este arquivo: só a demonstração (demo.py) o liga, num save temporário. Todos os números são
hipóteses desta rodada.

5ª versão: o reforço tem chance (o +1 garantido; falha volta um nível, sem quebrar a peça); ver CHANCE abaixo.

O que o reforço melhora: a peça inteira (decisões do Jean de 27 e 28/10/2026). Todas as linhas dela, da base e dos
afixos, cada uma pela regra de crescimento que o jogo já usa para ela: um + vale "a mesma peça alguns níveis acima".
Todo espaço de equipamento recebe reforço (arma, peito, cabeça, mãos, pernas, pés, apoio, anel e amuleto). O reforço
não mexe nas gravações. Não há caminho a escolher (Fio ou Runas acabou).

O ganho, em forma fechada, sempre a partir da peça original (`bonus_base`), sem arredondamento acumulado: cair e subir
de novo dá exatamente o mesmo número do nível. Cada passo vale um tanto de níveis de peça (PASSO_NIVEIS: 1,5 do +1 ao
+4, 1 do +5 ao +8, 0,75 do +9 ao +12; L(N) é a soma até +N).
- Linha fixa de valor v numa peça de nível n: G(N) = arredonda(v / escala(n) × 0,75 × L(N)), a proporção da escala do
  gerador, com o meio para baixo (1,5 → 1: em valores pequenos o meio ponto virava um salto). Valores pequenos crescem pouco (uma linha de 1 pode passar passos sem subir): nada de +1 imposto.
- Sem regra especial por espaço (28/10): o dobro que os apoios tinham do +1 ao +4 saiu. Com todo espaço recebendo
  reforço, ele dava saltos fora de proporção (o Tomo da Coruja, Poder 5 com o afixo, ia a 13 no +4), e o afixo se
  mistura à base na mesma linha, então não há como dobrar só a base.
- Crítico e roubo de vida, em %: + 0,25 ponto por nível de peça, como os afixos do gerador (+3 no +12), sem passar do
  teto por peça (TETO_PCT). O teto do personagem (60% de crítico) continua no motor.
- A linha principal da arma (a maior) sobe ao menos 1 por passo do +1 ao +4 (a faixa aprovada: cada passo se sente);
  depois, só a proporção.
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
PCT_POR_NIVEL = bal.ITEM_AFIXO_FIXO_POR_NIVEL  # crítico e roubo de vida: 0,25 ponto por nível de peça, como no gerador
TETO_PCT = {"critico": 15, "roubo_vida": 10}  # o máximo que uma peça reforçada chega a ter nessas linhas (hipótese)
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


def _ganho(x):
    """O ganho arredondado com o meio para baixo (1,5 → 1; 1,51 → 2): em linhas pequenas, o meio ponto virava um salto
    (uma aljava de Agilidade 1 ia a 3 no +4)."""
    return max(0, math.ceil(x - 0.5))


def _escala(nivel):
    return bal.ITEM_FORCA_BASE + bal.ITEM_FORCA_POR_NIVEL * nivel


TIPOS = {"arma": "arma", "armadura": "peito", "cabeca": "cabeca", "maos": "maos", "pernas": "pernas", "pes": "pes",
         "anel": "anel", "amuleto": "amuleto"}
APOIOS = {"guerreiro": "escudo", "mago": "foco", "arqueiro": "aljava"}


def tipo(item):
    """arma, peito, cabeca, maos, pernas, pes, anel, amuleto, escudo, foco, aljava (ou apoio); None só para o que não é
    equipamento."""
    s = item.get("slot")
    if s == "secundaria":
        return APOIOS.get(item.get("classe"), "apoio")
    return TIPOS.get(s)


def motivo_sem_reforco(item):
    return None if tipo(item) else "Esta peça não recebe reforço."


def linhas(item):
    """[(stat, q, piso)]: as linhas que o reforço faz crescer (todas as da peça, na ordem dela), a força de cada uma por
    ponto de escala (None nas de %, que crescem por soma) e se tem o piso de +1 por passo até o +4 (a principal da
    arma)."""
    if not tipo(item):
        return []
    base = item.get("bonus_base") or item["bonus"]  # a peça de antes do primeiro reforço (o reforço não a altera)
    esc = _escala(item.get("nivel") or 1)
    fixas = [st for st, v in base.items() if v and st not in itens.PERCENTUAIS]
    principal = max(fixas, key=lambda st: (base[st], st in ("atk", "poder")), default=None) if tipo(item) == "arma" else None
    return [(st, None if st in itens.PERCENTUAIS else v / esc, st == principal) for st, v in base.items() if v]


def niveis_de_peca(n):
    """L(N): os níveis de peça que N reforços valem."""
    return sum(PASSO_NIVEIS[:n])


def ganho_total(item, n):
    """O que N reforços somam a cada linha: {stat: valor}, em forma fechada (sem depender dos níveis do meio)."""
    base = item.get("bonus_base") or item["bonus"]
    total = {}
    for stat, q, piso in linhas(item):
        if q is None:
            g = _ganho(PCT_POR_NIVEL * niveis_de_peca(n))
            g = max(0, min(g, TETO_PCT.get(stat, 99) - base.get(stat, 0)))
        else:
            g = _ganho(q * bal.ITEM_FORCA_POR_NIVEL * niveis_de_peca(n))
        if piso:
            g = max(g, min(n, 4))
        total[stat] = g
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


# ------------------------------------------------------------------ transferência (28/10/2026, regras do Jean para testar)
TRANSFERE_PERDA = 2  # o destino recebe o nível da origem menos 2 (hipótese inicial)


def transferencia(origem, destino):
    """(nível novo do destino, motivo): o nível que o destino passa a ter, ou o motivo de recusar. Mesma raridade e mesmo
    tipo de peça; o nível recebido SUBSTITUI o do destino (não soma) e precisa ser maior que o dele."""
    if origem is destino:
        return None, "Escolha outra peça como destino."
    if not tipo(origem) or tipo(origem) != tipo(destino):
        return None, "Só entre peças do mesmo espaço."
    if origem.get("raridade") != destino.get("raridade"):
        return None, "Só entre peças da mesma raridade."
    novo = origem.get("reforco", 0) - TRANSFERE_PERDA
    if novo <= destino.get("reforco", 0):
        return None, f"O destino não sobe: recebe +{max(0, novo)}, já tem +{destino.get('reforco', 0)}."
    return novo, None


def custo_transferencia(novo):
    """O ouro da transferência (antes da reputação): o preço de uma tentativa do nível que o destino recebe."""
    return OURO[novo - 1]
