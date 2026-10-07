"""O Grimório: cada habilidade do herói com os números de agora, para entender o dano e montar a build.

Espelha a conta de Combate.atacar sem rolar dados: atributo × porcentagem (+ bônus), talentos que multiplicam,
variação de ±15% e o crítico. A defesa do inimigo e os efeitos do momento (fortalecido, clima, marcado) ficam de
fora, porque mudam a cada luta; o livro diz isso em vez de esconder.
"""

from . import balanceamento as bal
from .classes import CLASSES, HABILIDADES, ganho_meditar

NOME_STAT = {"atk": "Ataque", "poder": "Poder", "agi": "Agilidade", "max_hp": "Vida máx."}
ELEMENTO = {"fisico": "físico", "fogo": "fogo", "gelo": "gelo", "sagrado": "sagrado", "sombra": "sombra",
            "arcano": "arcano", "veneno": "veneno"}


def _pct(x):
    return f"{x * 100:.0f}%"


def _num(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def chance_critico(u, extra=0.0):
    return min(bal.MAX_CRITICO, bal.CRITICO_BASE + u.agi * bal.CRITICO_POR_AGI + extra + 0.04 * u.tal("olho_aguia")
               + u.especial("critico") / 100)


def mult_critico(u, furtivo=False):
    return (2.3 if furtivo else 1.6) + 0.2 * u.tal("golpe_sombras")


def mult_talentos(u, alcance):
    """O que os talentos de dano somam a todo golpe desse alcance (Golpe Brutal no corpo a corpo, Mira Firme à distância)."""
    if alcance == "corpo":
        return 1 + 0.06 * u.tal("golpe_brutal"), "Golpe Brutal" if u.tal("golpe_brutal") else None
    return 1 + 0.08 * u.tal("mira_firme"), "Mira Firme" if u.tal("mira_firme") else None


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
    if u.spec == "piromante":
        origem.append(f"+{_pct(bal.QUEIMADURA_PIROMANTE - 1)} piromante")
    if u.tal("brasas"):
        origem.append(f"+{_pct(bal.QUEIMADURA_BRASAS * u.tal('brasas'))} Brasas Eternas")
    return efeito(f"{_pct(chance)} de chance de acender: {_num(v)} de fogo por turno, {t} turnos, acumula até "
                  f"{bal.MAX_CHAMAS} camadas ({', '.join(origem)}).")


def _linhas(h_id, u):
    j = u
    if h_id == "golpe_pesado":
        return [golpe(j, 1.7)]
    if h_id == "erguer_escudo":
        return [efeito(f"Dano recebido −50% por {2 + j.tal('muralha')} turnos.")]
    if h_id == "investida":
        return [golpe(j, 1.2), efeito("45% de chance de atordoar o alvo por 1 turno.")]
    if h_id == "grito_guerra":
        return [efeito("Seu dano +30% por 3 turnos."),
                efeito("80% de chance de enfraquecer cada inimigo por 2 turnos (eles causam −25%).")]
    if h_id == "golpe_sagrado":
        return [golpe(j, 1.3, tipo="sagrado", bonus=j.poder * 0.8, bonus_txt="Poder × 80%"),
                efeito(f"Cura {_pct(0.35 * (1 + 0.25 * j.tal('luz_curativa')))} do dano causado.")]
    if h_id == "prece":
        cura = (j.max_hp * 0.3 + j.poder * 1.5) * (1 + 0.25 * j.tal("luz_curativa"))
        return [efeito(f"Cura {int(cura)} de vida (30% da vida máxima + Poder × 150%) e remove os males.")]
    if h_id == "julgamento":
        return [golpe(j, 1.2, tipo="sagrado", alcance="distancia", bonus=j.poder, bonus_txt="Poder × 100%",
                      rotulo="Em cada inimigo", nota="Não pode ser esquivado.")]
    if h_id == "sede_sangue":
        return [golpe(j, 1.4), efeito("Rouba 40% do dano causado como vida."),
                efeito(f"Sangramento: {_num(max(2, j.atk * 0.3))} por turno, 3 turnos (Ataque × 30%).")]
    if h_id == "redemoinho":
        return [golpe(j, 1.1, rotulo="Em cada inimigo (5 giros de 22%)")]
    if h_id == "furia_cega":
        return [efeito(f"Custa {int(j.max_hp * 0.15)} de vida (15% da máxima)."), efeito("Seu dano +60% por 3 turnos."),
                golpe(j, 1.3, extra=1.6, extra_txt="Fúria", rotulo="Golpe (já com a Fúria)")]
    if h_id == "tiro_certeiro":
        return [golpe(j, 1.7, alcance="distancia", crit_extra=0.3)]
    if h_id == "marcar_presa":
        return [efeito("O alvo recebe +25% de dano de todos por 3 turnos.")]
    if h_id == "chuva_flechas":
        return [golpe(j, 1.0, alcance="distancia", rotulo="Em cada inimigo")]
    if h_id == "passo_agil":
        base = min(bal.ESQUIVA_MAX_AGI, j.agi * bal.ESQUIVA_POR_AGI)
        return [efeito(f"Esquiva +30% por 2 turnos: de {_pct(base)} para {_pct(min(bal.MAX_ESQUIVA, base + 0.3))} "
                       f"(teto de {_pct(bal.MAX_ESQUIVA)}).")]
    if h_id == "tiro_duplo":
        return [golpe(j, 0.9, alcance="distancia", rotulo="Cada um dos 2 disparos")]
    if h_id == "comando_fera":
        fera = getattr(j, "companheiro", None)
        if not fera:
            return [efeito("Seu companheiro animal ataca com 200% do ataque dele.")]
        atk = fera["atk"] if isinstance(fera, dict) else fera.atk
        return [efeito(f"{fera['nome'] if isinstance(fera, dict) else fera.nome} ataca: {int(atk * 2 * 0.85)}–"
                       f"{int(atk * 2 * 1.15)} de dano (ataque dele {atk} × 200%). Lobo faz sangrar; urso atordoa.")]
    if h_id == "furia_natureza":
        return [golpe(j, 1.3, alcance="distancia", rotulo="Em cada inimigo"),
                efeito(f"50% de chance de sangramento: {_num(max(2, j.atk * 0.3))} por turno, 3 turnos."),
                efeito("Cura o companheiro animal por completo.")]
    if h_id == "desaparecer":
        return [efeito(f"O próximo ataque é crítico garantido de ×{_num(mult_critico(j, furtivo=True))}."),
                efeito("+50% de esquiva por 1 turno.")]
    if h_id == "flecha_envenenada":
        return [golpe(j, 1.0, alcance="distancia"),
                efeito(f"Veneno: {_num(max(3, j.atk * 0.45 + j.agi * 0.2))} por turno, 4 turnos "
                       "(Ataque × 45% + Agilidade × 20%).")]
    if h_id == "execucao":
        return [golpe(j, 1.2, alcance="distancia", crit_extra=0.2, rotulo="Alvo com mais de 35% de vida"),
                golpe(j, 3.2, alcance="distancia", crit_extra=0.2, rotulo="Alvo abaixo de 35% de vida")]
    if h_id == "bola_fogo":
        return [golpe(j, 1.5, stat="poder", alcance="distancia", tipo="fogo"),
                _queimadura(j, 1.0 if j.tal("ignicao") else 0.6)]
    if h_id == "meditar":
        return [efeito(f"Recupera {ganho_meditar(j)} de mana (6 + 12% do máximo). Gasta o turno.")]
    if h_id == "lanca_gelo":
        return [golpe(j, 1.3, stat="poder", alcance="distancia", tipo="gelo"),
                efeito("35% de chance de congelar o alvo (perde o próximo turno).")]
    if h_id == "barreira":
        valor = int((j.max_hp * 0.15 + j.poder * 0.2) * (1.3 if j.tal("escudo_reflexo") else 1))
        return [efeito(f"Absorve {valor} de dano por {2 + j.tal('escudo_reflexo')} turnos "
                       "(15% da vida máxima + Poder × 20%). Não acumula.")]
    if h_id == "inferno":
        return [golpe(j, 0.6, stat="poder", alcance="distancia", tipo="fogo", rotulo="Em cada inimigo"),
                _queimadura(j, 0.5)]
    if h_id == "combustao":
        from .combate import Combate
        v = Combate.valor_queimadura(None, j)
        t = Combate.duracao_queimadura(None, j)
        cheio = v * t * bal.MAX_CHAMAS
        bonus = cheio * (bal.COMBUSTAO_BASE + bal.COMBUSTAO_POR_CAMADA * bal.MAX_CHAMAS)
        return [golpe(j, 0.8, stat="poder", alcance="distancia", tipo="fogo", rotulo="Sem chamas no alvo"),
                golpe(j, 1.0, stat="poder", alcance="distancia", tipo="fogo", bonus=bonus,
                      bonus_txt=f"{bal.MAX_CHAMAS} camadas recém-acesas", crit_extra=0.05 * bal.MAX_CHAMAS,
                      rotulo=f"Detonando {bal.MAX_CHAMAS} camadas novas",
                      nota="O que as chamas ainda queimariam × (1,6 + 0,2 por camada). Quanto mais camadas e "
                           "mais cedo, maior a explosão.")]
    if h_id == "fenix":
        return [golpe(j, 2.5, stat="poder", alcance="distancia", tipo="fogo"),
                efeito(f"Cura {int(j.max_hp * 0.2)} de vida (20% da máxima).")]
    if h_id == "drenar_vida":
        return [golpe(j, 1.2, stat="poder", alcance="distancia", tipo="sombra"),
                efeito(f"Cura {_pct(0.4 + 0.1 * j.tal('pacto_sombrio'))} do dano causado.")]
    if h_id == "erguer_servo":
        vida = (j.poder * 1.2 + 8) * (1 + 0.15 * j.tal("pacto_sombrio"))
        return [efeito(f"Invoca um servo com {int(vida)} de vida e {int(j.poder * 0.3) + 2} de ataque "
                       f"(no máximo {1 + j.tal('exercito')} ao mesmo tempo).")]
    if h_id == "maldicao":
        return [efeito(f"Todos os inimigos: {_num(max(3, j.poder * 0.4))} de dano por turno, 4 turnos (Poder × 40%), "
                       "e −40% de defesa.")]
    return [efeito(HABILIDADES[h_id]["desc"])]


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
                     "linhas": _linhas(h_id, j)})
    tal_corpo, _ = mult_talentos(j, "corpo")
    tal_dist, _ = mult_talentos(j, "distancia")
    gerais = [f"Crítico: {round(chance_critico(j) * 100)}% de chance, dano ×{_num(mult_critico(j))}.",
              "Cada golpe varia ±15%. A defesa do inimigo reduz o dano: defesa 5 tira "
              f"{_pct(1 - 100 / (100 + 5 * bal.DEFESA_FATOR))}, defesa 10 tira {_pct(1 - 100 / (100 + 10 * bal.DEFESA_FATOR))}."]
    if tal_corpo > 1:
        gerais.append(f"Talentos: corpo a corpo ×{_num(tal_corpo)}.")
    if tal_dist > 1:
        gerais.append(f"Talentos: à distância ×{_num(tal_dist)}.")
    if j.spec == "berserker":
        gerais.append("Pacto de Sangue: até +60% de dano quanto mais ferido você estiver.")
    return {"recurso": j.nome_recurso, "basico": basico, "habilidades": habs, "gerais": gerais,
            "atributos": {"Ataque": j.atk, "Poder": j.poder, "Agilidade": j.agi}}
