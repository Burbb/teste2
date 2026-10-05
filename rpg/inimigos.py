"""Geração procedural de inimigos e suas habilidades."""

from . import texto as tx
from .dados import AFIXOS, FAMILIAS, GUARDIOES
from .entidades import Inimigo


def escala(nivel):
    return 1 + 0.2 * (nivel - 1)


def criar(rng, familia_id, nivel, afixo=None, nome_unico=None):
    f = FAMILIAS[familia_id]
    m = escala(nivel)
    hp = f["hp"] * m
    atk = f["atk"] * 0.9 * (1 + 0.18 * (nivel - 1))
    defesa = f["defesa"] * (1 + 0.15 * (nivel - 1))
    agi = f["agi"] + (nivel - 1) // 3
    poder = f["poder"] * m
    xp = f["xp"] * (1 + 0.3 * (nivel - 1))
    ouro = rng.randint(*f["ouro"]) * (1 + 0.2 * (nivel - 1))
    tracos = list(f["tracos"])
    habs = list(f["habs"])
    resist = dict(f.get("resist", {}))
    adjetivo = ""
    if afixo:
        a = AFIXOS[afixo]
        hp *= a.get("hp", 1)
        atk *= a.get("atk", 1)
        defesa *= a.get("defesa", 1)
        agi += a.get("agi", 0)
        poder += a.get("poder", 0) * m
        xp *= a.get("xp", 1)
        ouro *= a.get("ouro", 1)
        tracos += [t for t in a.get("tracos", []) if t not in tracos]
        habs += [h for h in a.get("habs", []) if h not in habs]
        resist.update(a.get("resist", {}))
        adjetivo = a[f["g"]]

    nome = tx.maiuscula(f["nome"]) + (f" {tx.maiuscula(adjetivo)}" if adjetivo else "")
    desc = f"{tx.artigo(f['g'], False)} {f['nome']}" + (f" {adjetivo}" if adjetivo else "")
    if nome_unico:
        nome = f"{nome_unico}, {tx.artigo(f['g'])} {nome}"
        desc = nome
        hp *= 1.3
        xp *= 1.5
        ouro = ouro * 1.5 + 10

    e = Inimigo(nome, hp, atk, defesa, agi, poder, f["g"])
    e.familia = familia_id
    e.afixo = afixo
    e.unico = bool(nome_unico)
    e.nivel = nivel
    e.tracos = tracos
    e.habilidades = habs
    e.resist = resist
    e.xp = int(xp)
    e.ouro = int(ouro)
    e.ataque = f.get("ataque", "fisico")
    e.desc = desc
    e.plural = f["plural"]
    return e


def _aplicar_template(e, t, nivel):
    e.tracos = list(t["tracos"])
    e.habilidades = list(t["habs"])
    e.resist = dict(t.get("resist", {}))
    e.ataque = t.get("ataque", "fisico")
    e.fases = [dict(f) for f in t.get("fases", [])]
    e.invoca = t.get("invoca")
    e.chefe = True
    e.unico = True
    e.nivel = nivel


def gerar_guardiao(rng, bioma):
    idx = rng.randrange(len(GUARDIOES[bioma]))
    t = GUARDIOES[bioma][idx]
    nome = f"{tx.nome_proprio(rng)}, {tx.artigo(t['g'])} {t['base']}"
    return {"bioma": bioma, "idx": idx, "nome": nome, "g": t["g"], "derrotado": False, "base": t["base"]}


def instanciar_guardiao(spec, nivel):
    t = GUARDIOES[spec["bioma"]][spec["idx"]]
    m = escala(nivel)
    m_atk = 0.85 * (1 + 0.18 * (nivel - 1))
    e = Inimigo(spec["nome"], t["hp"] * m * 0.75, t["atk"] * m_atk, t["defesa"] * (1 + 0.12 * (nivel - 1)),
                t["agi"] + nivel // 3, t["poder"] * m_atk, t["g"])
    _aplicar_template(e, t, nivel)
    e.xp = int(90 * (1 + 0.35 * (nivel - 1)))
    e.ouro = int(60 * (1 + 0.25 * (nivel - 1)))
    e.desc = spec["nome"]
    e.plural = spec["nome"]
    e.familia = "guardiao"
    return e


def instanciar_antagonista(ant, nivel, corrupcao):
    fator = 1 + corrupcao / 400
    m = escala(nivel) * fator
    m_atk = 0.85 * (1 + 0.18 * (nivel - 1)) * fator
    e = Inimigo(ant["nome"], 125 * m, 10 * m_atk, 7 * (1 + 0.12 * (nivel - 1)), 6 + nivel // 3, 11 * m_atk, ant["g"])
    t = dict(
        tracos=["conjurador"],
        habs=["bola_sombra", "drenar", "grito_terror", "maldicao"],
        resist={"sombra": 0.8, "sagrado": 1.25},
        ataque="sombra",
        invoca="cria_vazio",
        fases=[
            dict(limiar=0.66, texto=f"{ant['nome']} ri. \"Você ainda não entendeu? Eu SOU o Vazio.\" Sombras ganham forma ao redor.",
                 atk=1.15, habs=["invocar"]),
            dict(limiar=0.33, texto=f"A forma de {ant['nome']} se desfaz e se refaz, imensa, um rasgo vivo no mundo!",
                 atk=1.3, poder=1.3, habs=["esmagar"]),
        ],
    )
    _aplicar_template(e, t, nivel)
    e.xp = 500
    e.ouro = 300
    e.desc = ant["nome"]
    e.plural = ant["nome"]
    e.familia = "antagonista"
    return e


# ======================================================================
# Habilidades inimigas: fn(combate, inimigo, alvo) -> False se não usou.
# ======================================================================

def _mordida_sangrenta(cb, e, alvo):
    dano = cb.atacar(e, alvo, 1.0, rotulo="Garras")
    if dano:
        cb.aplicar(alvo, "sangramento", 3, valor=max(1, e.atk * 0.3), chance=0.7)


def _uivo(cb, e, alvo):
    cb.dizer(f"{e.nome} solta um uivo arrepiante. Seus aliados se enchem de fúria!", "vermelho")
    for aliado in cb.inimigos_vivos():
        aliado.aplicar("fortalecido", 2, 0.3)


def _grito_guerra(cb, e, alvo):
    cb.dizer(f"{e.nome} bate a arma no escudo e grita ordens!", "vermelho")
    for aliado in cb.inimigos_vivos():
        aliado.aplicar("fortalecido", 2, 0.3)


def _teia(cb, e, alvo):
    cb.dizer(f"{e.nome} dispara uma teia pegajosa!", "vermelho")
    if not cb.aplicar(alvo, "atordoado", 1, chance=0.55, rotulo="preso na teia"):
        cb.dizer(f"{cb.nome(alvo)} se desvencilha a tempo.", "cinza")


def _veneno(cb, e, alvo):
    dano = cb.atacar(e, alvo, 0.8, rotulo="Picada")
    if dano:
        cb.aplicar(alvo, "veneno", 3, valor=max(1, e.atk * 0.35))


def _golpe_sujo(cb, e, alvo):
    dano = cb.atacar(e, alvo, 1.1, rotulo="Golpe Sujo")
    if dano:
        cb.aplicar(alvo, "enfraquecido", 2, chance=0.35)


def _roubar(cb, e, alvo):
    j = cb.j
    if alvo is not j or j.ouro <= 0 or e.chefe:
        return False
    qtd = min(j.ouro, cb.rng.randint(5, 15) + j.nivel * 2)
    j.ouro -= qtd
    e.roubado += qtd
    cb.dizer(f"{e.nome} enfia a mão na sua bolsa e leva {qtd} moedas!", "vermelho")
    if len(cb.inimigos_vivos()) > 1 and cb.rng.random() < 0.35:
        e.fugiu = True
        e.hp = 0
        cb.dizer(f"{e.nome} gargalha e some no mato com o seu ouro!", "vermelho+negrito")
        cb.g.plantar("ladrao_fugitivo", 3, ouro=e.roubado, nome=e.nome)
    return True


def _investida(cb, e, alvo):
    dano = cb.atacar(e, alvo, 1.3, rotulo="Investida")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.25)


def _esmagar(cb, e, alvo):
    e.carregando = {"mult": 2.2, "rotulo": "GOLPE ESMAGADOR"}
    cb.dizer(f"{e.nome} recua e prepara um golpe devastador! (Defenda-se ou aja rápido!)", "amarelo+negrito")


def _regenerar(cb, e, alvo):
    if e.hp > e.max_hp * 0.7:
        return False
    cura = e.curar(e.max_hp * 0.15)
    cb.dizer(f"As feridas de {e.nome} se fecham diante dos seus olhos. (+{cura})", "vermelho")


def _agarrar(cb, e, alvo):
    dano = cb.atacar(e, alvo, 0.8, rotulo="Agarrão")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.4, rotulo="imobilizado")


def _drenar(cb, e, alvo):
    stat = "poder" if e.poder > e.atk else "atk"
    dano = cb.atacar(e, alvo, 1.0, tipo="sombra", stat=stat, rotulo="Toque Drenante")
    if dano:
        e.curar(dano * 0.6)


def _maldicao(cb, e, alvo):
    cb.dizer(f"{e.nome} murmura uma maldição em uma língua morta.", "magenta")
    cb.aplicar(alvo, "maldito", 3, valor=max(2, e.poder * 0.4))


def _bola_fogo(cb, e, alvo):
    dano = cb.atacar(e, alvo, 1.3, tipo="fogo", alcance="distancia", stat="poder", rotulo="Bola de Fogo")
    if dano:
        cb.aplicar(alvo, "queimadura", 3, valor=max(2, e.poder * 0.3), chance=0.3)


def _bola_sombra(cb, e, alvo):
    cb.atacar(e, alvo, 1.3, tipo="sombra", alcance="distancia", stat="poder", rotulo="Esfera Sombria")


def _cura(cb, e, alvo):
    feridos = [a for a in cb.inimigos_vivos() if a.hp < a.max_hp * 0.6]
    if not feridos:
        return False
    a = min(feridos, key=lambda x: x.hp / x.max_hp)
    cura = a.curar(a.max_hp * 0.3 + e.poder)
    quem = "a si mesmo" if a is e else a.nome
    cb.dizer(f"{e.nome} entoa um cântico e cura {quem}. (+{cura})", "vermelho")


def _grito_terror(cb, e, alvo):
    cb.dizer(f"{e.nome} solta um grito que congela a alma!", "magenta")
    if alvo is cb.j and cb.j.spec == "paladino" and cb.rng.random() < 0.6:
        cb.dizer("Sua fé não vacila.", "amarelo")
        return
    cb.aplicar(alvo, "enfraquecido", 2)


def _mordida_gelida(cb, e, alvo):
    dano = cb.atacar(e, alvo, 1.0, tipo="gelo", rotulo="Mordida Gélida")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.25, rotulo="congelado")


def _invocar(cb, e, alvo):
    if not e.invoca or len(cb.inimigos_vivos()) >= 4:
        return False
    novo = criar(cb.rng, e.invoca, max(1, e.nivel - 2))
    novo.nome = f"{novo.nome} (invocado)"
    novo.xp //= 2
    novo.ouro = 0
    cb.inimigos.append(novo)
    cb.dizer(f"{e.nome} convoca reforços: {novo.desc} entra na luta!", "vermelho+negrito")


HABS_INIMIGO = {
    "mordida_sangrenta": _mordida_sangrenta,
    "uivo": _uivo,
    "grito_guerra": _grito_guerra,
    "teia": _teia,
    "veneno": _veneno,
    "golpe_sujo": _golpe_sujo,
    "roubar": _roubar,
    "investida": _investida,
    "esmagar": _esmagar,
    "regenerar": _regenerar,
    "agarrar": _agarrar,
    "drenar": _drenar,
    "maldicao": _maldicao,
    "bola_fogo": _bola_fogo,
    "bola_sombra": _bola_sombra,
    "cura": _cura,
    "grito_terror": _grito_terror,
    "mordida_gelida": _mordida_gelida,
    "invocar": _invocar,
}

NOMES_HABS_INIMIGO = {
    "mordida_sangrenta": "garras que fazem sangrar", "uivo": "uivo de matilha", "grito_guerra": "grito de guerra",
    "teia": "teia paralisante", "veneno": "veneno", "golpe_sujo": "golpe sujo", "roubar": "rouba ouro",
    "investida": "investida atordoante", "esmagar": "golpe esmagador (avisa antes)", "regenerar": "regeneração",
    "agarrar": "agarrão imobilizante", "drenar": "drena vida", "maldicao": "maldição", "bola_fogo": "bola de fogo",
    "bola_sombra": "esfera sombria", "cura": "cura aliados", "grito_terror": "grito de terror",
    "mordida_gelida": "mordida congelante", "invocar": "invoca reforços",
}
