"""Encantamento (gravação), proposta de laboratório: as regras candidatas e a ligação com a luta. NÃO é regra aprovada
nem integração; o jogo de produção não importa este arquivo. A especificação inteira da forja está em
roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md.

Decisões do Jean:
- 27/10/2026: uma peça pode ter mais de um sulco (espaço de gravação), sorteado quando ela nasce.
- 28/10/2026: essências em três tiers e repetição permitida. Essência I, II e III ocupam um sulco cada e contribuem com
  1, 2 e 3 níveis do efeito. Repetir é permitido na mesma peça e entre peças. Cada efeito é resolvido uma vez, pelo
  nível total das peças que o próprio personagem veste (a bolsa e as peças dos outros não contam), com teto de 5 níveis
  (hipótese de teste). Não existe um segundo "nível da gravação".

Hipóteses desta rodada (todas provisórias):
- Cada peça gravável (arma, peito, escudo, foco) tem de 1 a 3 sulcos, sorteados pela raridade quando ela nasce
  (SULCOS) e guardados nela para sempre.
- Gravar consome 1 essência e ouro; nunca falha. Substituir apaga a gravação do sulco; a essência antiga não volta.
  Desmontar a peça perde as gravações.
- Em cada tabela, só uma dimensão cresce com o nível; gatilho, alvo, duração e limite ficam (salvo onde dito).
- Nenhum efeito secundário dispara outro: o dano de uma Queimadura, de um Revide ou de outra reação não aciona
  gravação nenhuma. "Rodada": todos agiram (cb.turno no motor); "turno": a vez de um combatente.

Os efeitos entram na luta por `ativar()`: um envoltório do golpe (Golpes.atacar), do início da luta e da morte de
um inimigo, só nesta demonstração. Tudo o que dura é guardado em `cb.memoria` (morre com a luta).
"""

TETO = 5           # níveis por efeito, por personagem (hipótese de teste)
TIERS = (1, 2, 3)  # Essência I, II e III: contribuem com 1, 2 e 3 níveis
NUMERAL = {1: "I", 2: "II", 3: "III"}
CUSTO_OURO = 30    # gravar ou substituir, qualquer tier
GRAVAVEIS = ("arma", "peito", "escudo", "foco")

# As tabelas, nível 1 a 5 (o nível total do personagem, com o teto). Só a dimensão da tabela cresce.
ESSENCIAS = {
    "brasa": {
        "nome": "Brasa", "material": "essencia_brasa", "tipos": ("arma",), "cor": "#f07a18", "icone": "chama",
        "fx": ["Y", "O", "o", "r"], "cresce": "a chance",
        "chance": (25, 32, 39, 46, 53), "medida": ("Chance de Queimadura", "chance", "%"),
        "nota": "Só golpes que acertam; o dano da Queimadura não dispara de novo.",
        "texto": lambda n, t: (f"Ao acertar um golpe, {t['chance'][n - 1]}% de chance de aplicar 1 camada de Queimadura (até 3).",
                               "No máximo 1 vez por rodada."),
        "ficha": {"gatilho": "golpe do portador que acerta um inimigo (não reações nem tiques)", "alvo": "o inimigo atingido",
                  "magnitude": "1 camada de Queimadura do valor do portador (25% do maior entre Ataque e Poder, mín. 2), "
                               "com a duração da Queimadura do herói (2 turnos num companheiro)",
                  "limite": "1 aplicação por rodada (em área ou golpes múltiplos, a primeira que pegar)",
                  "interacao": "soma camadas com a Queimadura do Mago (até 3); o tique não dispara; chefes recebem igual"}},
    "carrasco": {
        "nome": "Carrasco", "material": "essencia_carrasco", "tipos": ("arma",), "cor": "#d84a4a", "icone": "caveira",
        "fx": ["W", "R", "r", "D"], "cresce": "o dano a mais",
        "bonus": (20, 25, 30, 35, 40), "medida": ("Dano a mais", "bonus", "%"),
        "nota": "Vale em cada alvo de um golpe em área; não vale no dano por turno.",
        "texto": lambda n, t: (f"Causa {t['bonus'][n - 1]}% a mais de dano a inimigos abaixo de 35% da vida.", ""),
        "ficha": {"gatilho": "cada golpe do portador num inimigo abaixo de 35% da vida", "alvo": "o inimigo atingido",
                  "magnitude": "o dano a mais da tabela", "limite": "nenhum (vale em cada alvo de um golpe em área)",
                  "interacao": "multiplica com os outros bônus de dano; não vale nos tiques nem nas reações; chefes recebem igual"}},
    "eco": {
        "nome": "Eco", "material": "essencia_eco", "tipos": ("arma", "foco", "escudo"), "cor": "#a070f0", "icone": "pocao_azul",
        "fx": ["W", "M", "m", "x"], "cresce": "o recurso recuperado",
        "pct": (15, 20, 25, 30, 35), "medida": ("Recurso por abate", "pct", "%"),
        "nota": "Num golpe em área, cada inimigo derrubado conta.",
        "texto": lambda n, t: (f"Ao abater um inimigo, recupera {t['pct'][n - 1]}% do recurso máximo.", "Até 2 vezes por luta."),
        "ficha": {"gatilho": "um inimigo cai pelo golpe do portador", "alvo": "o portador",
                  "magnitude": "a % da Mana, Vigor ou Foco máximos", "limite": "2 vezes por luta (fixo: evita recurso sem fim)",
                  "interacao": "um abate em área conta uma vez por inimigo, dentro do limite; invocações não contam como portador"}},
    "vigilia": {
        "nome": "Vigília", "material": "essencia_vigilia", "tipos": ("peito", "escudo", "foco"), "cor": "#e8c860", "icone": "escudo",
        "fx": ["W", "Y", "y", "c"], "cresce": "a barreira",
        "pct": (10, 13, 16, 19, 22), "medida": ("Barreira", "pct", "% da vida"),
        "nota": "Não soma com outra barreira: vale a maior.",
        "texto": lambda n, t: (f"Começa a luta com uma barreira de {t['pct'][n - 1]}% da vida máxima, por 3 turnos seus.",
                               "1 vez por luta."),
        "ficha": {"gatilho": "começo da luta", "alvo": "o portador", "magnitude": "a barreira da tabela",
                  "limite": "1 vez por luta; dura 3 turnos do portador",
                  "interacao": "não soma com outra barreira: vale a maior (Aura de Proteção)"}},
    "revide": {
        "nome": "Revide", "material": "essencia_revide", "tipos": ("peito", "escudo"), "cor": "#b8c0cc", "icone": "espada",
        "fx": ["W", "w", "G", "g"], "cresce": "a chance",
        "chance": (15, 20, 25, 30, 35), "medida": ("Chance de revidar", "chance", "%"),
        "nota": "Só golpes corpo a corpo; o revide não provoca outro revide.",
        "texto": lambda n, t: (f"Ao receber um golpe corpo a corpo, {t['chance'][n - 1]}% de chance de revidar com 60% do Ataque.",
                               "No máximo 2 vezes por rodada."),
        "ficha": {"gatilho": "golpe corpo a corpo de um inimigo que acerta o portador (não à distância, nem tiques)",
                  "alvo": "quem bateu", "magnitude": "um golpe de 60% do Ataque do portador",
                  "limite": "1 resposta por golpe e 2 por rodada",
                  "interacao": "o revide não aciona outro revide nem a Brasa; um golpe em área que pega o portador conta como um golpe"}},
    "geada": {
        "nome": "Geada", "material": "essencia_geada", "tipos": ("peito",), "cor": "#78c8f0", "icone": "gota",
        "fx": ["W", "M", "U", "u"], "cresce": "a chance",
        "chance": (15, 20, 25, 30, 35), "medida": ("Chance de congelar", "chance", "%"),
        "nota": "Chefes e gigantes resistem metade das vezes.",
        "texto": lambda n, t: (f"Ao receber um golpe corpo a corpo, {t['chance'][n - 1]}% de chance de congelar o atacante: "
                               "ele perde a próxima vez.", "1 vez por luta."),
        "ficha": {"gatilho": "golpe corpo a corpo de um inimigo que acerta o portador", "alvo": "quem bateu",
                  "magnitude": "congela (perde a próxima vez)", "limite": "1 vez por luta",
                  "interacao": "chefes e gigantes resistem metade das vezes (a regra do Atordoado)"}},
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


def medida(essencia):
    """(rótulo, [o valor em cada nível, já formatado]) da dimensão que cresce: "Chance de Queimadura", ["25%", ...]."""
    e = ESSENCIAS[essencia]
    rotulo, chave_tabela, unidade = e["medida"]
    return rotulo, [f"{v}{unidade}" for v in e[chave_tabela]]


def nome(essencia, tier=1):
    return f"{ESSENCIAS[essencia]['nome']} {NUMERAL[tier]}"


def texto(essencia, nivel):
    """(efeito, limite) no nível dado (1 a TETO)."""
    e = ESSENCIAS[essencia]
    return e["texto"](max(1, min(TETO, nivel)), e)


MATERIAIS = {material(k, t): {"nome": f"Essência de {nome(k, t)}", "plural": f"Essências de {nome(k, t)}",
                              "icone": e["icone"], "desc": f"Grava {nome(k, t)} (+{t} {'nível' if t == 1 else 'níveis'} do efeito).",
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


def niveis_peca(item):
    """{essência: níveis que esta peça contribui} (a soma dos tiers dos sulcos dela)."""
    soma = {}
    for k in (item or {}).get("encantos") or []:
        e, t = ler(k)
        if e:
            soma[e] = soma.get(e, 0) + t
    return soma


def niveis_equip(equip):
    """{essência: nível total bruto} das peças vestidas (um dicionário espaço → peça), antes do teto."""
    soma = {}
    for it in (equip or {}).values():
        for e, n in niveis_peca(it).items():
            soma[e] = soma.get(e, 0) + n
    return soma


# ------------------------------------------------------------------ na luta (só nesta demonstração)
def nivel(u, essencia):
    """O nível efetivo de um efeito em quem luta: a soma das peças que ele veste, até o teto (0 se não tem)."""
    return min(TETO, niveis_equip(getattr(u, "equip", None) or {}).get(essencia, 0))


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
    n = nivel(u, "brasa") if not _inimigo(cb, u) else 0
    if n and alvo.vivo and _inimigo(cb, alvo):
        k = ("brasa", id(u), cb.turno)  # cb.turno é a rodada
        if not cb.memoria.get(k) and cb.rng.random() * 100 < ESSENCIAS["brasa"]["chance"][n - 1]:
            cb.memoria[k] = True
            valor = max(2, round(max(getattr(u, "atk", 0), getattr(u, "poder", 0)) * 0.25))
            if cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(u) if u is cb.j else 2, valor=valor, acumula=True):
                cb.dizer(f"A Brasa da arma acende {cb.nome(alvo, True)}.", "vermelho")
                _log(cb, "brasa", u, n)
    if alcance != "corpo" or not _inimigo(cb, u) or _inimigo(cb, alvo) or not alvo.vivo or not u.vivo:
        return
    ng = nivel(alvo, "geada")
    if ng and not cb.memoria.get(("geada", id(alvo))) and cb.rng.random() * 100 < ESSENCIAS["geada"]["chance"][ng - 1]:
        cb.memoria[("geada", id(alvo))] = True
        if cb.aplicar(u, "atordoado", 1, rotulo="congelado"):
            cb.dizer(f"A Geada prende {cb.nome(u, True)} no gelo.", "azul")
            _log(cb, "geada", alvo, ng)
    nr = nivel(alvo, "revide")
    if nr and u.vivo and cb.memoria.get(("revide", id(alvo), cb.turno), 0) < 2 \
            and cb.rng.random() * 100 < ESSENCIAS["revide"]["chance"][nr - 1]:
        _conta(cb, ("revide", id(alvo), cb.turno))
        cb._encanto_secundario = True  # o revide não dispara outra gravação (nem o Revide de volta)
        try:
            cb.atacar(alvo, u, 0.6, rotulo="Revide", reacao=True)
        finally:
            cb._encanto_secundario = False
        _log(cb, "revide", alvo, nr)


def mult_carrasco(cb, u, alvo):
    n = nivel(u, "carrasco") if not _inimigo(cb, u) else 0
    if n and alvo is not None and alvo.vivo and _inimigo(cb, alvo) and alvo.hp < alvo.max_hp * 0.35:
        _log(cb, "carrasco", u, n)
        return 1 + ESSENCIAS["carrasco"]["bonus"][n - 1] / 100
    return 1.0


def no_inicio(cb):
    """Vigília: a barreira de cada um que a veste (o herói e os companheiros)."""
    for u in [cb.j] + [a for a in cb.aliados if getattr(a, "tipo", None) == "comitiva"]:
        n = nivel(u, "vigilia")
        if u.vivo and n:
            valor = max(1, round(u.max_hp * ESSENCIAS["vigilia"]["pct"][n - 1] / 100))
            u.aplicar("barreira", 3, valor)
            cb.dizer(f"A Vigília gravada ergue uma barreira em {cb.nome(u, True)}. ({valor})", "amarelo")
            _log(cb, "vigilia", u, n)


def na_morte(cb, alvo, por):
    """Eco: quem derrubou recupera recurso, até 2 vezes por luta."""
    n = nivel(por, "eco") if por is not None and not _inimigo(cb, por) else 0
    if not n or not getattr(por, "max_rec", 0) or _conta(cb, ("eco", id(por))) > 2:
        return
    antes = por.rec
    por.rec = min(por.max_rec, por.rec + round(por.max_rec * ESSENCIAS["eco"]["pct"][n - 1] / 100))
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
