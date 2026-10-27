"""Encantamento (gravação), proposta de laboratório: as regras candidatas e a ligação com a luta. NÃO é regra aprovada
nem integração; o jogo de produção não importa este arquivo (roadmapIDEIAS/25, seção 5.7).

Decisão do Jean (27/10/2026): uma peça pode ter mais de um espaço de gravação, sorteado no drop, como os outros efeitos.

Hipóteses desta rodada (todas provisórias):
- Cada peça tem de 1 a 3 sulcos (espaços de gravação), sorteados pela raridade quando ela aparece (SULCOS); cada sulco
  guarda uma essência; a mesma essência não entra duas vezes na mesma peça. Reforço e gravação coexistem e não
  interferem um no outro.
- Gravar consome 1 essência (material do grupo, fora da bolsa) e ouro; nunca falha e não rebaixa nada.
- Substituir (gravar num sulco ocupado) custa o mesmo e apaga a gravação daquele sulco: a essência antiga não volta
  (a tela diz isso antes).
- Peças elegíveis: as que aceitam reforço (arma, peito, escudo, foco), de qualquer um do grupo ou da bolsa; cada
  essência diz em que tipo de peça entra.
- A gravação é da peça: vai junto quando ela troca de dono; desmontar a peça perde a gravação.
- O mesmo efeito conta uma vez por corpo (duas peças com Revide num companheiro: um Revide).
- Nenhum efeito secundário dispara outro: o dano de uma Queimadura, de um Revide ou de outra reação não aciona
  gravação nenhuma (os golpes de reação e os tiques não passam pelo gatilho).

Os efeitos entram na luta por `ativar()`: um envoltório do golpe (Golpes.atacar), do início da luta e da morte de
um inimigo, só nesta demonstração. Tudo o que dura é guardado em `cb.memoria` (morre com a luta): nada acumula de uma
luta para a outra.
"""

ESSENCIAS = {
    # dano: um gatilho de estado, com teto por turno
    "brasa": {
        "nome": "Brasa", "material": "essencia_brasa", "tipos": ("arma",), "cor": "#f07a18", "icone": "chama",
        "fx": ["Y", "O", "o", "r"],
        "efeito": "Ao acertar um golpe, 35% de chance de aplicar 1 camada de Queimadura (até 3).",
        "limite": "No máximo 1 vez por turno seu.",
        "ficha": {"alvo": "arma", "gatilho": "golpe do portador que acerta (não reações nem tiques)",
                  "magnitude": "1 camada de Queimadura, valor do portador (mín. 2), 35%", "duracao": "a da Queimadura",
                  "limite": "1 vez por rodada", "interacao": "soma com a Queimadura do Mago (até 3 camadas); o tique não dispara"}},
    # dano: condição de execução
    "carrasco": {
        "nome": "Carrasco", "material": "essencia_carrasco", "tipos": ("arma",), "cor": "#d84a4a", "icone": "caveira",
        "fx": ["W", "R", "r", "D"],
        "efeito": "Causa 30% a mais de dano a inimigos abaixo de 35% da vida.",
        "limite": "",
        "ficha": {"alvo": "arma", "gatilho": "cada golpe do portador num inimigo abaixo de 35% da vida",
                  "magnitude": "+30% de dano", "duracao": "—", "limite": "—",
                  "interacao": "multiplica com os outros bônus de dano; não vale nos tiques"}},
    # habilidades: recurso por abate
    "eco": {
        "nome": "Eco", "material": "essencia_eco", "tipos": ("arma", "foco", "escudo"), "cor": "#a070f0", "icone": "pocao_azul",
        "fx": ["W", "M", "m", "x"],
        "efeito": "Ao abater um inimigo, recupera 25% do recurso máximo.",
        "limite": "Até 2 vezes por luta.",
        "ficha": {"alvo": "arma, foco, escudo", "gatilho": "um inimigo cai pelo golpe do portador",
                  "magnitude": "25% da Mana, Vigor ou Foco máximos", "duracao": "—", "limite": "2 por luta",
                  "interacao": "soma com Colheita e Assassino"}},
    # sobrevivência: início da luta
    "vigilia": {
        "nome": "Vigília", "material": "essencia_vigilia", "tipos": ("peito", "escudo", "foco"), "cor": "#e8c860", "icone": "escudo",
        "fx": ["W", "Y", "y", "c"],
        "efeito": "Começa cada luta com uma barreira de 15% da vida máxima, por 3 turnos seus.",
        "limite": "1 vez por luta.",
        "ficha": {"alvo": "peito, escudo, foco", "gatilho": "começo da luta", "magnitude": "barreira de 15% da vida máxima",
                  "duracao": "3 turnos do portador", "limite": "1 por luta",
                  "interacao": "não soma com outra barreira: vale a maior (Aura de Proteção)"}},
    # sobrevivência/dano: reação
    "revide": {
        "nome": "Revide", "material": "essencia_revide", "tipos": ("peito", "escudo"), "cor": "#b8c0cc", "icone": "espada",
        "fx": ["W", "w", "G", "g"],
        "efeito": "Ao receber um golpe corpo a corpo, 25% de chance de revidar com 60% do Ataque.",
        "limite": "O revide não provoca outro revide.",
        "ficha": {"alvo": "peito, escudo", "gatilho": "golpe corpo a corpo de um inimigo que acerta o portador",
                  "magnitude": "um golpe de 60% do Ataque", "duracao": "—", "limite": "1 resposta por golpe",
                  "interacao": "o revide não aciona outro revide nem a Brasa; não soma com o Contra-ataque no mesmo golpe"}},
    # controle: estado
    "geada": {
        "nome": "Geada", "material": "essencia_geada", "tipos": ("peito",), "cor": "#78c8f0", "icone": "gota",
        "fx": ["W", "M", "U", "u"],
        "efeito": "Ao receber um golpe corpo a corpo, 30% de chance de congelar o atacante: ele perde a próxima vez.",
        "limite": "1 vez por luta.",
        "ficha": {"alvo": "peito", "gatilho": "golpe corpo a corpo de um inimigo que acerta o portador",
                  "magnitude": "congela (perde a próxima vez)", "duracao": "1 turno do atacante", "limite": "1 por luta",
                  "interacao": "chefes e gigantes resistem metade das vezes (a regra do Atordoado)"}},
}
ORDEM = ("brasa", "carrasco", "eco", "vigilia", "revide", "geada")
for _e in ESSENCIAS.values():  # a regra inteira, numa frase só (as dicas e o registro); o efeito e o limite separados (a ficha)
    _e["desc"] = f"{_e['efeito']} {_e['limite']}".strip()
CUSTO_OURO = 30
# quantos sulcos a peça traz, pela raridade (o sorteio do drop): {n: peso}
SULCOS = {"comum": {1: 75, 2: 25}, "magico": {1: 50, 2: 40, 3: 10}, "raro": {1: 25, 2: 50, 3: 25}, "lendario": {2: 50, 3: 50}}


def semente(item):
    """A semente do sorteio dos sulcos, pela própria peça (nome, nível, raridade, base): não gasta o sorteio do jogo e dá o
    mesmo resultado para a mesma peça. Só vale uma vez: depois, os sulcos ficam gravados nela."""
    return f"{item.get('nome', '').split(' +')[0]}|{item.get('nivel')}|{item.get('raridade')}|{sorted((item.get('bonus_base') or item.get('bonus') or {}).items())}"


def sortear_sulcos(item, rng=None):
    """Quando a peça nasce (o drop, o mercado, a recompensa; no laboratório, os envoltórios da criação em demo.py): os
    sulcos dela, vazios. Uma peça que já tem sulcos nunca é sorteada de novo; as telas só leem."""
    if "encantos" not in item:
        import random
        rng = rng or random.Random(semente(item))
        pesos = SULCOS.get(item.get("raridade", "comum"), SULCOS["comum"])
        n = rng.choices(list(pesos), weights=list(pesos.values()))[0]
        item["encantos"] = [None] * n
    return item["encantos"]
MATERIAIS = {e["material"]: {"nome": f"Essência de {e['nome']}", "plural": f"Essências de {e['nome']}", "icone": e["icone"],
                             "desc": f"Grava {e['nome']} numa peça na forja.", "fontes": "Recompensa de teste; baú (às vezes)."}
             for e in ESSENCIAS.values()}


PLURAL = {"arma": "armas", "peito": "peitorais", "escudo": "escudos", "foco": "focos"}


def compativel(essencia):
    """"Compatível com: armas, focos e escudos" (a dica da essência)."""
    nomes = [PLURAL[t] for t in ESSENCIAS[essencia]["tipos"]]
    return "Compatível com: " + (nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1])


def tipo(item):
    from regras import tipo as tipo_reforco
    return tipo_reforco(item)


def motivo(item, essencia=None, sulco=None):
    """Por que esta peça (com esta essência, neste sulco) não pode ser gravada; None quando pode."""
    t = tipo(item)
    if not t:
        return "Só arma, peito, escudo e foco recebem gravação."
    if essencia:
        e = ESSENCIAS[essencia]
        if t not in e["tipos"]:
            return f"Incompatível com {PLURAL[t]}"
        if essencia in (item.get("encantos") or []):
            return f"Esta peça já tem {e['nome']}."
    if sulco is not None and not 0 <= sulco < len(item.get("encantos") or []):
        return "Esse sulco não existe nesta peça."
    return None


def gravar(item, essencia, sulco):
    """Grava (ou substitui) a essência no sulco. Devolve a gravação anterior daquele sulco (ou None)."""
    antes = item["encantos"][sulco]
    item["encantos"][sulco] = essencia
    return antes


# ------------------------------------------------------------------ na luta (só nesta demonstração)
def encantos(u):
    """As gravações de quem luta, cada uma uma vez (o herói e os companheiros vestem `equip`)."""
    equip = getattr(u, "equip", None) or {}
    return {k for it in equip.values() if it for k in (it.get("encantos") or []) if k in ESSENCIAS}


def _conta(cb, chave):
    cb.memoria[chave] = cb.memoria.get(chave, 0) + 1
    return cb.memoria[chave]


def _log(cb, essencia, u):
    """O registro do que disparou (para os testes e a luta de teste conferirem): fica no jogo, por luta."""
    g = getattr(cb, "g", None)
    if g is not None:
        log = getattr(g, "encanto_log", None)
        if log is None:
            log = g.encanto_log = []
        log.append((essencia, getattr(u, "nome", "?")))


def _inimigo(cb, u):
    return u in cb.inimigos


def ao_golpear(cb, u, alvo, dano, alcance, reacao, rotulo):
    """Depois de um golpe que acertou: a Brasa de quem bateu; o Revide e a Geada de quem apanhou."""
    if not dano or reacao or getattr(cb, "_encanto_secundario", False):
        return
    if alvo.vivo and not _inimigo(cb, u) and "brasa" in encantos(u) and _inimigo(cb, alvo):
        chave = ("brasa", id(u), cb.turno)
        if not cb.memoria.get(chave) and cb.rng.random() < 0.35:
            cb.memoria[chave] = True
            valor = max(2, round(max(getattr(u, "atk", 0), getattr(u, "poder", 0)) * 0.25))
            if cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(u) if u is cb.j else 2, valor=valor, acumula=True):
                cb.dizer(f"A Brasa da arma acende {cb.nome(alvo, True)}.", "vermelho")
                _log(cb, "brasa", u)
    if alcance != "corpo" or not _inimigo(cb, u) or _inimigo(cb, alvo) or not alvo.vivo or not u.vivo:
        return
    gravados = encantos(alvo)
    if "geada" in gravados and not cb.memoria.get(("geada", id(alvo))) and cb.rng.random() < 0.30:
        cb.memoria[("geada", id(alvo))] = True
        if cb.aplicar(u, "atordoado", 1, rotulo="congelado"):
            cb.dizer(f"A Geada prende {cb.nome(u, True)} no gelo.", "azul")
            _log(cb, "geada", alvo)
    if "revide" in gravados and u.vivo and cb.rng.random() < 0.25:
        cb._encanto_secundario = True  # o revide não dispara outra gravação (nem o Revide de volta)
        try:
            cb.atacar(alvo, u, 0.6, rotulo="Revide", reacao=True)
        finally:
            cb._encanto_secundario = False
        _log(cb, "revide", alvo)


def mult_carrasco(cb, u, alvo):
    if alvo is not None and alvo.vivo and _inimigo(cb, alvo) and not _inimigo(cb, u) and "carrasco" in encantos(u) \
            and alvo.hp < alvo.max_hp * 0.35:
        _log(cb, "carrasco", u)
        return 1.3
    return 1.0


def no_inicio(cb):
    """Vigília: a barreira de cada um que a tem gravada (o herói e os companheiros)."""
    for u in [cb.j] + [a for a in cb.aliados if getattr(a, "tipo", None) == "comitiva"]:
        if u.vivo and "vigilia" in encantos(u):
            valor = max(1, round(u.max_hp * 0.15))
            u.aplicar("barreira", 3, valor)
            cb.dizer(f"A Vigília gravada ergue uma barreira em {cb.nome(u, True)}. ({valor})", "amarelo")
            _log(cb, "vigilia", u)


def na_morte(cb, alvo, por):
    """Eco: quem derrubou recupera recurso, até 2 vezes por luta."""
    if por is None or _inimigo(cb, por) or "eco" not in encantos(por) or not getattr(por, "max_rec", 0):
        return
    if _conta(cb, ("eco", id(por))) > 2:
        return
    antes = por.rec
    por.rec = min(por.max_rec, por.rec + round(por.max_rec * 0.25))
    cb.recuperou(por, por.rec - antes, "Eco")
    if por is not cb.j:
        cb.dizer(f"O Eco devolve forças a {cb.nome(por, True)}. (+{por.rec - antes})", "magenta")
    _log(cb, "eco", por)


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
