"""Encantamento (gravação), proposta de laboratório: as regras candidatas e a ligação com a luta. NÃO é regra aprovada
nem integração; o jogo de produção não importa este arquivo. A especificação inteira da forja está em
roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md.

Decisões do Jean:
- 27/10/2026: uma peça pode ter mais de um sulco (espaço de gravação), sorteado quando ela nasce.
- 28/10/2026: essências em três tiers e repetição permitida, na mesma peça e entre peças.
- 15ª rodada (substitui a soma de níveis até 5): Essência I, II e III são versões de potência diferente do mesmo efeito,
  cada uma com o seu valor. Não existe mais "nível do efeito". Repetir soma só a propriedade que cresce (a chance da
  Brasa, do Revide e da Geada; a magnitude do Carrasco, do Eco e da Vigília), até um limite próprio de cada efeito; o
  gatilho, a duração, o dano do golpe e a frequência não mudam com a repetição. Cada efeito dispara uma vez por
  personagem (não uma vez por cópia), pelas peças que ele veste; a bolsa e as peças dos outros não contam.
- Cada tier tem um nível mínimo (REQUISITO); a peça gravada pede o maior entre o dela e o das gravações.

Hipóteses desta rodada (todas provisórias):
- Cada peça gravável (arma, peito, escudo, foco) tem de 1 a 3 sulcos, sorteados pela raridade quando ela nasce
  (SULCOS) e guardados nela para sempre.
- Gravar consome 1 essência e ouro; nunca falha. Substituir apaga a gravação do sulco; a essência antiga não volta.
  Desmontar a peça perde as gravações.
- As tabelas (valor por tier, limite por efeito) e os requisitos por tier são números de teste.
- Nenhum efeito secundário dispara outro: o dano de uma Queimadura, de um Revide ou de outra reação não aciona
  gravação nenhuma. "Rodada": todos agiram (cb.turno no motor); "turno": a vez de um combatente.

Os efeitos entram na luta por `ativar()`: um envoltório do golpe (Golpes.atacar), do início da luta e da morte de
um inimigo, só nesta demonstração. Tudo o que dura é guardado em `cb.memoria` (morre com a luta).
"""

TIERS = (1, 2, 3)  # Essência I, II e III: a mesma essência em três potências
NUMERAL = {1: "I", 2: "II", 3: "III"}
REQUISITO = {1: 1, 2: 5, 3: 9}  # o nível mínimo de quem veste a peça gravada (provisório: o tier do conteúdo)
CUSTO_OURO = 30    # gravar ou substituir, qualquer tier
GRAVAVEIS = ("arma", "peito", "escudo", "foco")

# Cada essência: o valor da propriedade que cresce em cada tier (I, II, III), o limite da soma de quem veste (a
# repetição soma só essa propriedade) e o texto com o valor. O resto (gatilho, alvo, duração, frequência) é fixo.
ESSENCIAS = {
    "brasa": {
        "nome": "Brasa", "material": "essencia_brasa", "tipos": ("arma",), "cor": "#f07a18", "icone": "chama",
        "fx": ["Y", "O", "o", "r"], "valores": (20, 28, 36), "limite": 60, "medida": ("Chance de Queimadura", "%"),
        "nota": "Só golpes que acertam; o dano da Queimadura não dispara de novo.",
        "texto": lambda v: (f"Ao acertar um golpe, {v}% de chance de aplicar 1 camada de Queimadura (até 3).",
                            "No máximo 1 vez por rodada.")},
    "carrasco": {
        "nome": "Carrasco", "material": "essencia_carrasco", "tipos": ("arma",), "cor": "#d84a4a", "icone": "caveira",
        "fx": ["W", "R", "r", "D"], "valores": (15, 22, 30), "limite": 50, "medida": ("Dano a mais", "%"),
        "nota": "Vale em cada alvo de um golpe em área; não vale no dano por turno.",
        "texto": lambda v: (f"Causa {v}% a mais de dano a inimigos abaixo de 35% da vida.", "")},
    "eco": {
        "nome": "Eco", "material": "essencia_eco", "tipos": ("arma", "foco", "escudo"), "cor": "#a070f0", "icone": "pocao_azul",
        "fx": ["W", "M", "m", "x"], "valores": (10, 15, 20), "limite": 35, "medida": ("Recurso por abate", "%"),
        "nota": "Num golpe em área, cada inimigo derrubado conta.",
        "texto": lambda v: (f"Ao abater um inimigo, recupera {v}% do recurso máximo.", "Até 2 vezes por luta.")},
    "vigilia": {
        "nome": "Vigília", "material": "essencia_vigilia", "tipos": ("peito", "escudo", "foco"), "cor": "#e8c860", "icone": "escudo",
        "fx": ["W", "Y", "y", "c"], "valores": (8, 11, 14), "limite": 25, "medida": ("Barreira", "% da vida"),
        "nota": "Não soma com outra barreira: vale a maior.",
        "texto": lambda v: (f"Começa a luta com uma barreira de {v}% da vida máxima, por 3 turnos seus.", "1 vez por luta.")},
    "revide": {
        "nome": "Revide", "material": "essencia_revide", "tipos": ("peito", "escudo"), "cor": "#b8c0cc", "icone": "espada",
        "fx": ["W", "w", "G", "g"], "valores": (12, 18, 24), "limite": 40, "medida": ("Chance de revidar", "%"),
        "nota": "Só golpes corpo a corpo; o revide não provoca outro revide.",
        "texto": lambda v: (f"Ao receber um golpe corpo a corpo, {v}% de chance de revidar com 60% do Ataque.",
                            "No máximo 2 vezes por rodada.")},
    "geada": {
        "nome": "Geada", "material": "essencia_geada", "tipos": ("peito",), "cor": "#78c8f0", "icone": "gota",
        "fx": ["W", "M", "U", "u"], "valores": (12, 18, 24), "limite": 40, "medida": ("Chance de congelar", "%"),
        "nota": "Chefes e gigantes resistem metade das vezes.",
        "texto": lambda v: (f"Ao receber um golpe corpo a corpo, {v}% de chance de congelar o atacante: ele perde a "
                            "próxima vez.", "1 vez por luta.")},
}
ORDEM = ("brasa", "carrasco", "eco", "vigilia", "revide", "geada")
# quantos sulcos a peça traz, pela raridade, quando nasce: {n: peso} (raridade maior, mais chance de 3; nunca garantido)
SULCOS = {"comum": {1: 75, 2: 25}, "magico": {1: 50, 2: 40, 3: 10}, "raro": {1: 25, 2: 50, 3: 25}, "lendario": {2: 50, 3: 50}}
PLURAL = {"arma": "armas", "peito": "peitorais", "escudo": "escudos", "foco": "focos"}


# ------------------------------------------------------------------ as gravações: "brasa" (I), "brasa:2", "brasa:3"
def chave(essencia, tier=1):
    return essencia if tier == 1 else f"{essencia}:{tier}"


def ler(k):
    """(essência, tier) de uma gravação ou de um pedido; (None, 0) se não for uma."""
    if not k:
        return None, 0
    e, _, t = str(k).partition(":")
    t = int(t) if t.isdigit() else 1
    return (e, t) if e in ESSENCIAS and t in TIERS else (None, 0)


def material(essencia, tier=1):
    return ESSENCIAS[essencia]["material"] + ("" if tier == 1 else f"_{tier}")


def nome(essencia, tier=1):
    return f"{ESSENCIAS[essencia]['nome']} {NUMERAL[tier]}"


def valor_tier(essencia, tier):
    """O valor da propriedade que cresce numa gravação deste tier (Brasa II: 28, a chance em %)."""
    return ESSENCIAS[essencia]["valores"][tier - 1]


def com_unidade(essencia, v):
    """"28%", "11% da vida"."""
    return f"{v}{ESSENCIAS[essencia]['medida'][1]}"


def texto(essencia, v):
    """(efeito, limite de frequência) com o valor dado (o chamador já aplicou o limite da soma, quando é o caso)."""
    return ESSENCIAS[essencia]["texto"](v)


MATERIAIS = {material(k, t): {"nome": f"Essência de {nome(k, t)}", "plural": f"Essências de {nome(k, t)}",
                              "icone": e["icone"], "cor": e["cor"], "tier": t, "numeral": NUMERAL[t], "requisito": REQUISITO[t],
                              "desc": f"Grava {nome(k, t)}: {e['medida'][0].lower()} {com_unidade(k, valor_tier(k, t))}.",
                              "fontes": "Lutas e chefes (pela criatura), baús."}
             for k, e in ESSENCIAS.items() for t in TIERS}


def semente(item):
    """A semente do sorteio dos sulcos, pela própria peça (nome, nível, raridade, base): não gasta o sorteio do jogo e dá o
    mesmo resultado para a mesma peça. Só vale uma vez: depois, os sulcos ficam gravados nela."""
    return f"{item.get('nome', '').split(' +')[0]}|{item.get('nivel')}|{item.get('raridade')}|{sorted((item.get('bonus_base') or item.get('bonus') or {}).items())}"


def sortear_sulcos(item, rng=None):
    """Quando a peça nasce: os sulcos dela, vazios. Uma peça que já tem sulcos nunca é sorteada de novo."""
    if "encantos" not in item:
        import random
        rng = rng or random.Random(semente(item))
        pesos = SULCOS.get(item.get("raridade", "comum"), SULCOS["comum"])
        n = rng.choices(list(pesos), weights=list(pesos.values()))[0]
        item["encantos"] = [None] * n
    return item["encantos"]


def compativel(essencia):
    """"Compatível com: armas, focos e escudos" (a dica da essência)."""
    nomes = [PLURAL[t] for t in ESSENCIAS[essencia]["tipos"]]
    return "Compatível com: " + (nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1])


def tipo(item):
    """O tipo gravável da peça (arma, peito, escudo, foco), ou None. As outras peças recebem reforço, não gravação."""
    from regras import tipo as tipo_reforco
    t = tipo_reforco(item)
    return t if t in GRAVAVEIS else None


def motivo(item, gravacao=None, sulco=None):
    """Por que esta peça (com esta essência, neste sulco) não pode ser gravada; None quando pode. Repetir é permitido."""
    t = tipo(item)
    if not t:
        return "Só arma, peito, escudo e foco recebem gravação."
    if gravacao:
        e, _ = ler(gravacao)
        if e is None:
            return "Escolha uma essência."
        if t not in ESSENCIAS[e]["tipos"]:
            return f"Incompatível com {PLURAL[t]}"
    if sulco is not None and not 0 <= sulco < len(item.get("encantos") or []):
        return "Esse sulco não existe nesta peça."
    return None


def gravar(item, gravacao, sulco):
    """Grava (ou substitui) no sulco. Devolve a gravação anterior daquele sulco (ou None)."""
    antes = item["encantos"][sulco]
    item["encantos"][sulco] = gravacao
    return antes


def soma_peca(item):
    """{essência: soma bruta dos valores das gravações desta peça} (sem o limite)."""
    soma = {}
    for k in (item or {}).get("encantos") or []:
        e, t = ler(k)
        if e:
            soma[e] = soma.get(e, 0) + valor_tier(e, t)
    return soma


def soma_equip(equip):
    """{essência: soma bruta} das peças vestidas (um dicionário espaço → peça), antes do limite."""
    soma = {}
    for it in (equip or {}).values():
        for e, v in soma_peca(it).items():
            soma[e] = soma.get(e, 0) + v
    return soma


def limitado(essencia, v):
    return min(ESSENCIAS[essencia]["limite"], v)


# ------------------------------------------------------------------ requisitos de nível (provisórios)
def requisito_base(item):
    """O nível mínimo para usar a peça sem gravações: um abaixo do nível em que ela foi gerada (o achado nasce no
    nível do herói ou um acima, e serve na hora), nunca menos de 1. O nível da geração continua no item ("nivel")."""
    return max(1, int((item or {}).get("nivel") or 1) - 1)


def requisito_gravacoes(item):
    """O maior requisito entre as gravações da peça (0 sem gravação)."""
    return max([REQUISITO[ler(k)[1]] for k in (item or {}).get("encantos") or [] if ler(k)[0]] or [0])


def requisito(item, encantos=None):
    """O requisito da peça: o maior entre o dela e o das gravações. `encantos`: uma lista no lugar da da peça (a
    gravação ainda por fazer). O reforço não muda o requisito."""
    if encantos is not None:
        item = {**item, "encantos": encantos}
    return max(requisito_base(item), requisito_gravacoes(item))


# ------------------------------------------------------------------ na luta (só nesta demonstração)
def valor(u, essencia):
    """O valor do efeito em quem luta: a soma das peças que ele veste, até o limite do efeito (0 se não tem)."""
    return limitado(essencia, soma_equip(getattr(u, "equip", None) or {}).get(essencia, 0))


def _conta(cb, k):
    cb.memoria[k] = cb.memoria.get(k, 0) + 1
    return cb.memoria[k]


def _log(cb, essencia, u, n=0):
    """O registro do que disparou (para os testes e a luta de teste conferirem): fica no jogo, por luta."""
    g = getattr(cb, "g", None)
    if g is not None:
        log = getattr(g, "encanto_log", None)
        if log is None:
            log = g.encanto_log = []
        log.append((essencia, getattr(u, "nome", "?"), n))


def _inimigo(cb, u):
    return u in cb.inimigos


def ao_golpear(cb, u, alvo, dano, alcance, reacao, rotulo):
    """Depois de um golpe que acertou: a Brasa de quem bateu; o Revide e a Geada de quem apanhou."""
    if not dano or reacao or getattr(cb, "_encanto_secundario", False):
        return
    n = valor(u, "brasa") if not _inimigo(cb, u) else 0
    if n and alvo.vivo and _inimigo(cb, alvo):
        k = ("brasa", id(u), cb.turno)  # cb.turno é a rodada
        if not cb.memoria.get(k) and cb.rng.random() * 100 < n:
            cb.memoria[k] = True
            forca = max(2, round(max(getattr(u, "atk", 0), getattr(u, "poder", 0)) * 0.25))
            if cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(u) if u is cb.j else 2, valor=forca, acumula=True):
                cb.dizer(f"A Brasa da arma acende {cb.nome(alvo, True)}.", "vermelho")
                _log(cb, "brasa", u, n)
    if alcance != "corpo" or not _inimigo(cb, u) or _inimigo(cb, alvo) or not alvo.vivo or not u.vivo:
        return
    ng = valor(alvo, "geada")
    if ng and not cb.memoria.get(("geada", id(alvo))) and cb.rng.random() * 100 < ng:
        cb.memoria[("geada", id(alvo))] = True
        if cb.aplicar(u, "atordoado", 1, rotulo="congelado"):
            cb.dizer(f"A Geada prende {cb.nome(u, True)} no gelo.", "azul")
            _log(cb, "geada", alvo, ng)
    nr = valor(alvo, "revide")
    if nr and u.vivo and cb.memoria.get(("revide", id(alvo), cb.turno), 0) < 2 \
            and cb.rng.random() * 100 < nr:
        _conta(cb, ("revide", id(alvo), cb.turno))
        cb._encanto_secundario = True  # o revide não dispara outra gravação (nem o Revide de volta)
        try:
            cb.atacar(alvo, u, 0.6, rotulo="Revide", reacao=True)
        finally:
            cb._encanto_secundario = False
        _log(cb, "revide", alvo, nr)


def mult_carrasco(cb, u, alvo):
    n = valor(u, "carrasco") if not _inimigo(cb, u) else 0
    if n and alvo is not None and alvo.vivo and _inimigo(cb, alvo) and alvo.hp < alvo.max_hp * 0.35:
        _log(cb, "carrasco", u, n)
        return 1 + n / 100
    return 1.0


def no_inicio(cb):
    """Vigília: a barreira de cada um que a veste (o herói e os companheiros)."""
    for u in [cb.j] + [a for a in cb.aliados if getattr(a, "tipo", None) == "comitiva"]:
        n = valor(u, "vigilia")
        if u.vivo and n:
            barreira = max(1, round(u.max_hp * n / 100))
            u.aplicar("barreira", 3, barreira)
            cb.dizer(f"A Vigília gravada ergue uma barreira em {cb.nome(u, True)}. ({barreira})", "amarelo")
            _log(cb, "vigilia", u, n)


def na_morte(cb, alvo, por):
    """Eco: quem derrubou recupera recurso, até 2 vezes por luta."""
    n = valor(por, "eco") if por is not None and not _inimigo(cb, por) else 0
    if not n or not getattr(por, "max_rec", 0) or _conta(cb, ("eco", id(por))) > 2:
        return
    antes = por.rec
    por.rec = min(por.max_rec, por.rec + round(por.max_rec * n / 100))
    cb.recuperou(por, por.rec - antes, "Eco")
    if por is not cb.j:
        cb.dizer(f"O Eco devolve forças a {cb.nome(por, True)}. (+{por.rec - antes})", "magenta")
    _log(cb, "eco", por, n)


def ativar():
    """Liga os efeitos à luta, só nesta execução (a demonstração chama uma vez)."""
    from rpg.combate import golpe as mod_golpe, luta as mod_luta
    Golpes = mod_golpe.Golpes
    if getattr(Golpes, "_encanto", False):
        return
    Golpes._encanto = True
    atacar = Golpes.atacar

    def atacar_com_encanto(self, u, alvo, mult, *a, **k):
        if not k.get("reacao") and not getattr(self, "_encanto_secundario", False):
            mult *= mult_carrasco(self, u, alvo)
        dano = atacar(self, u, alvo, mult, *a, **k)
        alcance = k.get("alcance", a[1] if len(a) > 1 else "corpo")
        ao_golpear(self, u, alvo, dano, alcance, k.get("reacao", False), k.get("rotulo"))
        return dano
    Golpes.atacar = atacar_com_encanto

    def com_encanto(original):
        def disparar(cb, u, evento, **dados):
            r = original(cb, u, evento, **dados)
            if evento == "inicio_combate":
                no_inicio(cb)
            elif evento == "morte":
                na_morte(cb, dados.get("alvo"), dados.get("por"))
            return r
        return disparar
    mod_luta.disparar = com_encanto(mod_luta.disparar)
    mod_golpe.disparar = com_encanto(mod_golpe.disparar)
