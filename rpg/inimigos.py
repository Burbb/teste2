"""Geração procedural de inimigos e suas habilidades."""

from . import balanceamento as bal
from . import texto as tx
from .dados import AFIXOS, FAMILIAS, GUARDIOES
from .entidades import Inimigo


def escala(nivel):
    """Vida e poder do inimigo por nível."""
    return (1 + bal.INIMIGO_VIDA_POR_NIVEL * (nivel - 1)
            + bal.INIMIGO_CURVA * max(0, nivel - bal.INIMIGO_CURVA_DESDE) ** bal.INIMIGO_CURVA_EXPOENTE)


def escala_atk(nivel):
    """Ataque físico do inimigo por nível."""
    return (1 + bal.INIMIGO_ATK_POR_NIVEL * (nivel - 1)
            + bal.INIMIGO_ATK_CURVA * max(0, nivel - bal.INIMIGO_CURVA_DESDE) ** bal.INIMIGO_CURVA_EXPOENTE)


def criar(rng, familia_id, nivel, afixo=None, nome_unico=None):
    f = FAMILIAS[familia_id]
    m = escala(nivel)
    hp = f["hp"] * m * bal.INIMIGO_VIDA
    atk = f["atk"] * bal.INIMIGO_ATK_BASE * escala_atk(nivel) * bal.INIMIGO_DANO
    defesa = f["defesa"] * (1 + bal.INIMIGO_DEFESA_POR_NIVEL * (nivel - 1))
    agi = f["agi"] + (nivel - 1) // bal.INIMIGO_AGI_A_CADA
    poder = f["poder"] * m * bal.INIMIGO_DANO
    xp = f["xp"] * (1 + bal.INIMIGO_XP_POR_NIVEL * (nivel - 1))
    ouro = rng.randint(*f["ouro"]) * (1 + bal.INIMIGO_OURO_POR_NIVEL * (nivel - 1))
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


def adicionar_afixo(e, afixo):
    """Segundo afixo para inimigos únicos."""
    a = AFIXOS[afixo]
    e.max_hp = int(e.max_hp * a.get("hp", 1))
    e.hp = e.max_hp
    e.atk *= a.get("atk", 1)
    e.defesa *= a.get("defesa", 1)
    e.agi += a.get("agi", 0)
    e.poder += a.get("poder", 0)
    e.xp = int(e.xp * a.get("xp", 1))
    e.tracos += [t for t in a.get("tracos", []) if t not in e.tracos]
    e.habilidades += [h for h in a.get("habs", []) if h not in e.habilidades]
    e.resist.update(a.get("resist", {}))
    e.nome += f" {a[e.g].capitalize()}"


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
    nome = f"{tx.nome_proprio(rng)}, the {t['base']}"
    return {"bioma": bioma, "idx": idx, "nome": nome, "g": t["g"], "derrotado": False, "base": t["base"]}


def instanciar_guardiao(spec, nivel):
    t = GUARDIOES[spec["bioma"]][spec["idx"]]
    m = escala(nivel)
    m_atk = bal.GUARDIAO_ATK * escala_atk(nivel)
    e = Inimigo(spec["nome"], t["hp"] * m * bal.GUARDIAO_VIDA, t["atk"] * m_atk,
                t["defesa"] * (1 + bal.GUARDIAO_DEFESA_POR_NIVEL * (nivel - 1)),
                t["agi"] + nivel // bal.INIMIGO_AGI_A_CADA, t["poder"] * m_atk, t["g"])
    _aplicar_template(e, t, nivel)
    e.xp = int(55 * (1 + bal.INIMIGO_XP_POR_NIVEL * (nivel - 1)))
    e.ouro = int(30 * (1 + bal.INIMIGO_OURO_POR_NIVEL * (nivel - 1)))
    e.desc = spec["nome"]
    e.plural = spec["nome"]
    e.familia = "guardiao"
    return e


def instanciar_antagonista(ant, nivel, corrupcao):
    fator = 1 + corrupcao / 400
    m = escala(nivel) * fator
    m_atk = bal.ANTAGONISTA_ATK * escala_atk(nivel) * fator
    e = Inimigo(ant["nome"], 150 * m, 11 * m_atk, 7 * (1 + bal.GUARDIAO_DEFESA_POR_NIVEL * (nivel - 1)),
                6 + nivel // bal.INIMIGO_AGI_A_CADA, 11 * m_atk, ant["g"])
    t = dict(
        tracos=["conjurador"],
        habs=["bola_sombra", "drenar", "grito_terror", "maldicao", "varredura"],
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
    cb.lance("roubo_ouro", de=cb.uid(e), em="j", valor=qtd)
    cb.dizer(f"{e.nome} enfia a mão na sua bolsa e leva {qtd} moedas!", "vermelho")
    if len(cb.inimigos_vivos()) > 1 and cb.rng.random() < 0.35:
        cb.lance("fuga", de=cb.uid(e))
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
    cb.curou(e, cura, rotulo="Regenerar")
    cb.dizer(f"As feridas de {e.nome} se fecham diante dos seus olhos. (+{cura})", "vermelho")


def _agarrar(cb, e, alvo):
    dano = cb.atacar(e, alvo, 0.8, rotulo="Agarrão")
    if dano:
        cb.aplicar(alvo, "atordoado", 1, chance=0.4, rotulo="imobilizado")


def _drenar(cb, e, alvo):
    stat = "poder" if e.poder > e.atk else "atk"
    dano = cb.atacar(e, alvo, 1.0, tipo="sombra", stat=stat, rotulo="Toque Drenante")
    if dano:
        cb.curou(e, e.curar(dano * 0.6), "roubo", fonte=alvo)


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
    cb.curou(a, cura, de=e, rotulo="Cura")
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


def _varredura(cb, e, alvo):
    alvos = [cb.j] + [a for a in cb.aliados if a.vivo]
    if len(alvos) == 1 and cb.rng.random() < 0.5:
        return False
    cb.dizer(f"{e.nome} desfere um golpe amplo que atinge todos à frente!", "vermelho+negrito")
    for a in alvos:
        cb.atacar(e, a, 0.8, rotulo="Varredura")


def _reviver(cb, e, alvo):
    caidos = [m for m in cb.inimigos if not m.vivo and not m.fugiu and m.familia == "caido" and m is not e]
    if not caidos:
        return False
    m = cb.rng.choice(caidos)
    m.hp = m.max_hp // 2
    m.efeitos = {}
    if m in cb.mortos:
        cb.mortos.remove(m)
    cb.dizer(f"{e.nome} grita palavras profanas: {m.nome} se levanta de novo, rindo!", "vermelho+negrito")


def _devorar(cb, e, alvo):
    if not cb.mortos or e.hp > e.max_hp * 0.75:
        return False
    corpo = cb.mortos.pop()
    cura = e.curar(e.max_hp * 0.35)
    cb.curou(e, cura, "roubo", rotulo="Devorar")
    cb.dizer(f"{e.nome} se ajoelha e arranca pedaços de {corpo.nome} com os dentes. (+{cura})", "vermelho")


def _invocar(cb, e, alvo):
    if not e.invoca or len(cb.inimigos_vivos()) >= 4:
        return False
    novo = criar(cb.rng, e.invoca, max(1, e.nivel - 2))
    # No modo texto, cada invocado tem letra própria ("Esqueleto A", "Esqueleto B") para o menu de alvos;
    # na tela gráfica o alvo é a carta, e a letra só poluiria.
    base = novo.nome
    if getattr(cb.ui, "web", False):
        novo.nome = f"{base} (invocado)"
    else:
        usados = {x.nome for x in cb.inimigos}
        letra = next((l for l in "ABCDEFGHIJKLMNOP" if f"{base} {l} (invocado)" not in usados), "Z")
        novo.nome = f"{base} {letra} (invocado)"
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
    "varredura": _varredura,
    "reviver": _reviver,
    "devorar": _devorar,
}

NOMES_HABS_INIMIGO = {
    "mordida_sangrenta": "garras que fazem sangrar", "uivo": "uivo de matilha", "grito_guerra": "grito de guerra",
    "teia": "teia paralisante", "veneno": "veneno", "golpe_sujo": "golpe sujo", "roubar": "rouba ouro",
    "investida": "investida atordoante", "esmagar": "golpe esmagador (avisa antes)", "regenerar": "regeneração",
    "agarrar": "agarrão imobilizante", "drenar": "drena vida", "maldicao": "maldição", "bola_fogo": "bola de fogo",
    "bola_sombra": "esfera sombria", "cura": "cura aliados", "grito_terror": "grito de terror",
    "mordida_gelida": "mordida congelante", "invocar": "invoca reforços",
    "varredura": "golpe em área (atinge você e seus aliados)",
    "reviver": "ressuscita caídos", "devorar": "devora cadáveres para se curar",
}

# Nomes curtos das habilidades, para a faixa que aparece sobre a carta de quem age.
ROTULOS_HABS_INIMIGO = {
    "mordida_sangrenta": "Mordida Sangrenta", "uivo": "Uivo", "grito_guerra": "Grito de Guerra", "teia": "Teia",
    "veneno": "Veneno", "golpe_sujo": "Golpe Sujo", "roubar": "Roubo", "investida": "Investida",
    "esmagar": "Preparar Golpe", "regenerar": "Regenerar", "agarrar": "Agarrão", "drenar": "Drenar",
    "maldicao": "Maldição", "bola_fogo": "Bola de Fogo", "bola_sombra": "Esfera Sombria", "cura": "Cura",
    "grito_terror": "Grito de Terror", "mordida_gelida": "Mordida Gélida", "invocar": "Invocar",
    "varredura": "Varredura", "reviver": "Reviver", "devorar": "Devorar",
}
