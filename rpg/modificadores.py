"""Modificadores e gatilhos: como talentos, especializações, itens (e, adiante, estados) mudam o jogo
sem que o combate precise saber de cada um.

O combate só faz duas perguntas:

    mod(u, "dano_corpo")                    quanto somam os modificadores dessa chave (+6% por ponto de Golpe Brutal...)
    disparar(cb, u, "abate", alvo=c, ...)   quem reage a esse acontecimento (Frenesi, Assassino, Coração Ardente...)

Quem responde são as **fontes**: a passiva da especialização, cada talento comprado (na ordem em que foram
declarados) e cada item vestido (na ordem dos espaços). Cada fonte é um dicionário com:

    mods      {chave: valor por ponto}   (Fixo(v): vale v uma vez, com qualquer número de pontos)
    mults     {chave: fator}             multiplicadores (mult(u, chave) = produto dos fatores)
    gatilhos  {evento: função(cb, u, rank, dados)}   e `ordem` (menor primeiro) quando a ordem importa

Para um talento novo, basta declarar os efeitos dele em talentos.py: nenhum outro arquivo muda, a menos que a
chave seja nova (aí o lugar do jogo que a usa pergunta por ela uma vez, e qualquer fonte futura também vale).
Itens: os bônus especiais (`ESPECIAIS` em itens.py: crítico, roubo de vida, espinhos...) viram mods do item, e um
item único pode declarar mods, mults e gatilhos próprios no catálogo (itens.fonte_item).

Chaves em uso (o que cada uma significa):
    dano_corpo, dano_distancia    +x de dano por golpe desse alcance
    dano_ferido                   +x de dano no máximo, proporcional à vida perdida (Pacto de Sangue)
    critico, mult_critico         +chance de crítico; +multiplicador do crítico
    roubo_vida                    fração do dano causado que volta como vida
    abertura                      o primeiro ataque de cada luta é crítico
    furtivo_ao_abater             abater deixa furtivo (só para descrever; o efeito é o gatilho)
    custo_pct, custo:<habilidade>  −x% no custo de todas; ±x no custo de uma
    escudo_turnos, barreira_turnos, queimadura_turnos   turnos a mais
    queimadura_dano, cura_luz, dreno_cura, servo_vida   +x (fração) nesses números
    acender_garantido             a Bola de Fogo sempre acende
    servos_max, ataques_fera, laco_animal               +1 servo, +1 ataque do animal, +x de vida/ataque do animal
    aljava, recolher_flecha       +espaço na aljava; +chance de recolher flecha
    contra_ataque, veneno_basico  chance de revidar corpo a corpo; chance do ataque básico envenenar
    espinhos                      dano devolvido a quem acerta você corpo a corpo
    regen_vida, vida_abate        vida no começo de cada turno seu; vida a cada inimigo que você abate
mults:
    queimadura_mult, barreira_mult

Eventos (gatilhos): inicio_combate · golpe_fatal (dados: dano; pode mudar) · golpe_recebido (de, alcance) ·
ataque_basico (alvo; só quando acertou) · morte (alvo, por, tipo; qualquer inimigo que cai) · abate (alvo, tipo; você matou)
"""


# As chaves e eventos que o jogo pergunta. Um talento com uma chave fora daqui não faria nada (erro de digitação):
# tests/test_modificadores.py recusa. Chave nova? Acrescente aqui e no lugar do jogo que a usa.
CHAVES = {"dano_corpo", "dano_distancia", "dano_ferido", "critico", "mult_critico", "roubo_vida", "abertura",
          "furtivo_ao_abater", "custo_pct", "escudo_turnos", "barreira_turnos", "queimadura_turnos",
          "queimadura_dano", "cura_luz", "dreno_cura", "servo_vida", "acender_garantido", "servos_max",
          "ataques_fera", "laco_animal", "aljava", "recolher_flecha", "contra_ataque", "veneno_basico",
          "espinhos", "regen_vida", "vida_abate"}
PREFIXOS = ("custo:",)  # custo:<id da habilidade>
MULTS = {"queimadura_mult", "barreira_mult"}
EVENTOS = {"inicio_combate", "golpe_fatal", "golpe_recebido", "ataque_basico", "morte", "abate"}


class Fixo:
    """Um modificador que vale uma vez, não por ponto (ex.: Muralha: o escudo custa 4 a menos)."""

    def __init__(self, valor):
        self.valor = valor


def fontes(u):
    """(nome, fonte, pontos) de quem modifica este combatente: a passiva da especialização, os talentos comprados
    e os itens vestidos."""
    lista = []
    talentos = getattr(u, "talentos", None)
    if talentos is not None:
        from .talentos import PASSIVAS, TALENTOS
        spec = getattr(u, "spec", None)
        if spec in PASSIVAS:
            lista.append((PASSIVAS[spec]["nome"], PASSIVAS[spec], 1))
        for t in TALENTOS.get(getattr(u, "classe", None), []):
            rank = talentos.get(t["id"], 0)
            if rank:
                lista.append((t["nome"], t, rank))
    equip = getattr(u, "equip", None)
    if equip:
        from .itens import fonte_item
        for item in equip.values():
            if item:
                f = fonte_item(item)
                if f:
                    lista.append((item["nome"], f, 1))
    return lista


def _valor(v, rank):
    return v.valor if isinstance(v, Fixo) else v * rank


def mod(u, chave):
    """A soma dos modificadores dessa chave (0 quando ninguém mexe nela)."""
    total = 0
    for _, f, rank in fontes(u):
        v = f.get("mods", {}).get(chave)
        if v is not None:
            total += _valor(v, rank)
    return total


def mult(u, chave):
    """O produto dos multiplicadores dessa chave (1 quando ninguém mexe nela)."""
    total = 1
    for _, f, rank in fontes(u):
        v = f.get("mults", {}).get(chave)
        if v is not None:
            total *= v.valor if isinstance(v, Fixo) else v
    return total


def contribuicoes(u, chave):
    """(nome, valor) de cada fonte que mexe nessa chave, na ordem: para dizer de onde vem cada pedaço do número."""
    return [(nome, _valor(f["mods"][chave], rank)) for nome, f, rank in fontes(u) if chave in f.get("mods", {})]


def nomes(u, chave):
    """Quem contribui para essa chave (para o Grimório e as dicas dizerem de onde vem o número)."""
    return [nome for nome, f, _ in fontes(u) if chave in f.get("mods", {}) or chave in f.get("mults", {})]


def disparar(cb, u, evento, **dados):
    """Avisa as fontes de `u` que algo aconteceu. Cada gatilho recebe (cb, u, pontos, dados) e pode mudar `dados`
    (o golpe fatal do Imortal reduz o dano, por exemplo). Devolve `dados`."""
    reacoes = [(f.get("ordem", 50), i, fn, rank) for i, (_, f, rank) in enumerate(fontes(u))
               for ev, fn in f.get("gatilhos", {}).items() if ev == evento]
    for _, _, fn, rank in sorted(reacoes, key=lambda r: (r[0], r[1])):
        fn(cb, u, rank, dados)
    return dados
