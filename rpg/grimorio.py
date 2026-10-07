"""O Grimório: cada habilidade do herói com os números de agora, para entender o dano e montar a build.

Espelha a conta de Combate.atacar sem rolar dados: atributo × porcentagem (+ bônus), talentos que multiplicam,
variação de ±15% e o crítico. A defesa do inimigo e os efeitos do momento (fortalecido, clima, marcado) ficam de
fora, porque mudam a cada luta; o livro diz isso em vez de esconder.
"""

from . import balanceamento as bal
from .classes import CLASSES
from .habilidades import HABILIDADES, crit_extra
from .modificadores import mod, mult, nomes

NOME_STAT = {"atk": "Ataque", "poder": "Poder", "agi": "Agilidade", "max_hp": "Vida máx."}
ELEMENTO = {"fisico": "físico", "fogo": "fogo", "gelo": "gelo", "sagrado": "sagrado", "sombra": "sombra",
            "arcano": "arcano", "veneno": "veneno"}


def _pct(x):
    return f"{x * 100:.0f}%"


def _num(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def fontes_critico(j):
    """De onde vêm os críticos além da chance da ficha: habilidades com bônus (lido dos próprios golpes delas)
    e críticos garantidos."""
    linhas = [f"{HABILIDADES[h]['nome']}: {round(chance_critico(j, crit_extra(HABILIDADES[h])) * 100)}% de chance."
              for h in j.habilidades if crit_extra(HABILIDADES[h])]
    if mod(j, "abertura"):
        linhas.append(f"{', '.join(nomes(j, 'abertura'))}: o primeiro ataque de cada luta é sempre crítico.")
    if "desaparecer" in j.habilidades or mod(j, "furtivo_ao_abater"):
        linhas.append("Furtivo (Desaparecer, Assassino): o próximo ataque é crítico garantido.")
    linhas.append("Pegar o inimigo de surpresa: o primeiro golpe é crítico.")
    return linhas


def chance_critico(u, extra=0.0):
    """A chance de crítico de um golpe. A conta única: o combate, a ficha e o Grimório usam esta."""
    return min(bal.MAX_CRITICO, bal.CRITICO_BASE + u.agi * bal.CRITICO_POR_AGI + extra + mod(u, "critico")
               + u.especial("critico") / 100)


def mult_critico(u, furtivo=False):
    """Quanto o crítico multiplica (furtivo: o golpe das sombras, mais forte)."""
    return (2.3 if furtivo else 1.6) + mod(u, "mult_critico")


def mult_talentos(u, alcance):
    """O que os modificadores de dano somam a todo golpe desse alcance, e quem são eles (Golpe Brutal, Mira Firme...)."""
    chave = "dano_corpo" if alcance == "corpo" else "dano_distancia"
    return 1 + mod(u, chave), ", ".join(nomes(u, chave)) or None


def golpe(u, mult, stat="atk", alcance="corpo", tipo="fisico", bonus=0.0, bonus_txt=None, crit_extra=0.0, rotulo="Dano",
          extra=1.0, extra_txt=None, nota=None):
    """Uma linha de dano: faixa (±15%), média, crítico e de onde vem cada parte."""
    valor = getattr(u, stat)
    tal, nome_tal = mult_talentos(u, alcance)
    base = valor * mult + bonus
    medio = base * tal * extra
    formula = [f"{NOME_STAT[stat]} {valor} × {_pct(mult)}"]
    if bonus:
        formula.append(f"+ {bonus_txt or 'bônus'} ({_num(bonus)})")
    if nome_tal:
        formula.append(f"× {_num(tal)} ({nome_tal})")
    if extra != 1.0:
        formula.append(f"× {_num(extra)} ({extra_txt})")
    escala = [f"+1 de {NOME_STAT[stat]}: +{_num(mult * tal * extra)} de dano"]
    if bonus_txt and "Poder" in bonus_txt and stat != "poder":
        escala.append(f"+1 de Poder: +{_num(bonus / max(1, u.poder) * tal * extra)}")
    crit = chance_critico(u, crit_extra)
    return {"tipo": "dano", "rotulo": rotulo, "elemento": ELEMENTO.get(tipo, tipo), "alcance": alcance,
            "min": int(medio * 0.85), "max": int(medio * 1.15), "medio": int(medio),
            "critico": int(medio * mult_critico(u)), "chance_critico": round(crit * 100),
            "formula": " ".join(formula), "escala": escala, "nota": nota}


def efeito(texto):
    return {"tipo": "efeito", "texto": texto}


def _queimadura(u, chance):
    from .combate import Combate
    v = Combate.valor_queimadura(None, u)
    t = Combate.duracao_queimadura(None, u)
    origem = [f"Poder × {_pct(bal.QUEIMADURA_POR_PODER)}"]
    if mult(u, "queimadura_mult") != 1:
        origem.append(f"+{_pct(mult(u, 'queimadura_mult') - 1)} {', '.join(nomes(u, 'queimadura_mult'))}")
    if mod(u, "queimadura_dano"):
        origem.append(f"+{_pct(mod(u, 'queimadura_dano'))} {', '.join(nomes(u, 'queimadura_dano'))}")
    return efeito(f"{_pct(chance)} de chance de acender: {_num(v)} de fogo por turno, {t} turnos, acumula até "
                  f"{bal.MAX_CHAMAS} camadas ({', '.join(origem)}).")


# Como os RPGs de turno descrevem o alcance (Final Fantasy, Pokémon): quem, e se é um só ou todos.
ALVOS = {"inimigo": "Inimigo único", "todos": "Todos os inimigos", "proprio": "Você",
         "aliado": "Aliado único", "aliados": "Todos os aliados"}


def dados(j):
    """Tudo o que o livro mostra: o ataque básico, cada habilidade e os números gerais do herói."""
    nome, alcance, tipo, stat, mult = CLASSES[j.classe]["ataque"]
    recupera = max(bal.ATAQUE_RECURSO_MIN, round(j.max_rec * bal.ATAQUE_RECURSO))
    basico = {"id": "ataque", "nome": nome, "custo": 0, "flechas": 1 if j.classe == "arqueiro" else 0,
              "alvo": ALVOS["inimigo"], "desc": "O golpe de sempre. Não custa nada e, quando acerta, devolve um pouco "
                                                f"de {j.nome_recurso.lower()}.",
              "linhas": [golpe(j, mult, stat=stat, alcance=alcance, tipo=tipo),
                         efeito(f"Ao acertar, devolve {recupera} de {j.nome_recurso.lower()} (4% do máximo).")]}
    habs = []
    for h_id in j.habilidades:
        h = HABILIDADES[h_id]
        habs.append({"id": h_id, "nome": h["nome"], "custo": h["custo"], "flechas": h.get("flechas", 0),
                     "alvo": ALVOS.get(h["alvo"], ""), "desc": h["desc"],  # os números de agora vão nas linhas
                     "linhas": h["linhas"](j)})
    tal_corpo, _ = mult_talentos(j, "corpo")
    tal_dist, _ = mult_talentos(j, "distancia")
    gerais = [f"Crítico: {round(chance_critico(j) * 100)}% de chance, dano ×{_num(mult_critico(j))}.",
              "Cada golpe varia ±15%. A defesa do inimigo reduz o dano: defesa 5 tira "
              f"{_pct(1 - 100 / (100 + 5 * bal.DEFESA_FATOR))}, defesa 10 tira {_pct(1 - 100 / (100 + 10 * bal.DEFESA_FATOR))}."]
    if tal_corpo > 1:
        gerais.append(f"Talentos: corpo a corpo ×{_num(tal_corpo)}.")
    if tal_dist > 1:
        gerais.append(f"Talentos: à distância ×{_num(tal_dist)}.")
    gerais += [f"Crítico a mais — {l}" for l in fontes_critico(j)[:-1]]
    roubo_tal, roubo_itens = 100 * mod(j, "roubo_vida"), j.especial("roubo_vida")
    if roubo_tal or roubo_itens:
        partes = ([f"{', '.join(nomes(j, 'roubo_vida'))} {_num(roubo_tal)}%"] if roubo_tal else []) + ([f"itens {_num(roubo_itens)}%"] if roubo_itens else [])
        gerais.append(f"Roubo de vida: {_num(roubo_tal + roubo_itens)}% de todo dano que você causa volta como vida "
                      f"({' + '.join(partes)}).")
    from .talentos import PASSIVAS
    if j.spec in PASSIVAS:
        gerais.append(f"Passiva — {PASSIVAS[j.spec]['nome']}: {PASSIVAS[j.spec]['desc']}")
    return {"recurso": j.nome_recurso, "basico": basico, "habilidades": habs, "gerais": gerais,
            "atributos": {"Ataque": j.atk, "Poder": j.poder, "Agilidade": j.agi}}
