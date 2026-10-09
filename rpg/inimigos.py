"""Geração procedural de inimigos e suas habilidades."""

from . import balanceamento as bal
from . import texto as tx
from .dados import AFIXOS, FAMILIAS, GUARDIOES
from .entidades import Inimigo
from .modificadores import mod


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
    atk = f["atk"] * bal.INIMIGO_ATK_BASE * escala_atk(nivel) * bal.INIMIGO_DANO * bal.DANO_INIMIGOS
    defesa = f["defesa"] * (1 + bal.INIMIGO_DEFESA_POR_NIVEL * (nivel - 1))
    agi = f["agi"] + (nivel - 1) // bal.INIMIGO_AGI_A_CADA
    poder = f["poder"] * m * bal.INIMIGO_DANO * bal.DANO_INIMIGOS
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
    nome = f"{tx.nome_proprio(rng)}, {'o' if t['g'] == 'm' else 'a'} {t['base']}"  # "Kalra, o Rei Troll"
    return {"bioma": bioma, "id": t["id"], "idx": idx, "nome": nome, "g": t["g"], "derrotado": False,
            "base": t["base"]}


def ficha_guardiao(spec):
    """O guardião do catálogo de um covil: pelo id (que não muda se a lista ganhar guardiões novos), ou pela posição
    na lista nos saves de antes do id."""
    lista = GUARDIOES[spec["bioma"]]
    return next((t for t in lista if t["id"] == spec.get("id")), None) or lista[spec["idx"]]


def instanciar_guardiao(spec, nivel):
    t = ficha_guardiao(spec)
    m = escala(nivel)
    m_atk = bal.GUARDIAO_ATK * escala_atk(nivel) * bal.DANO_INIMIGOS
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


def instanciar_antagonista(ant, nivel):
    m = escala(nivel)
    m_atk = bal.ANTAGONISTA_ATK * escala_atk(nivel) * bal.DANO_INIMIGOS
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
    cb.dizer(f"{e.nome} enfia a mão na sua bolsa e leva {tx.plural(qtd, 'moeda')}!", "vermelho")
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
    cb.dizer(f"{e.nome} recua e prepara um golpe devastador! (Defenda-se, ou atordoe para interromper!)", "amarelo+negrito")


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
    """Cura o inimigo mais ferido. Sem mana, mas com fôlego curto: uma vez a cada INIMIGO_CURA_RECARGA turnos."""
    if cb.turno - getattr(e, "curou_turno", -99) < bal.INIMIGO_CURA_RECARGA:
        return False
    feridos = [a for a in cb.inimigos_vivos() if a.hp < a.max_hp * 0.6]
    if not feridos:
        return False
    e.curou_turno = cb.turno
    a = min(feridos, key=lambda x: x.hp / x.max_hp)
    cura = a.curar(a.max_hp * bal.INIMIGO_CURA_VIDA + e.poder * bal.INIMIGO_CURA_PODER)
    cb.curou(a, cura, de=e, rotulo="Cura")
    quem = "a si mesmo" if a is e else a.nome
    cb.dizer(f"{e.nome} entoa um cântico e cura {quem}. (+{cura})", "vermelho")


def _grito_terror(cb, e, alvo):
    cb.dizer(f"{e.nome} solta um grito que congela a alma!", "magenta")
    resiste = mod(alvo, "resiste_terror") if alvo is cb.j else 0
    if resiste and cb.rng.random() < resiste:
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


def _caidos_para_reviver(cb, e):
    """Os mortos da família que esta levanta (`revive` na ficha: o xamã ergue os caídos)."""
    revive = FAMILIAS.get(e.familia, {}).get("revive")
    return [m for m in cb.inimigos if not m.vivo and not m.fugiu and m.familia == revive and m is not e]


def _reviver(cb, e, alvo):
    caidos = _caidos_para_reviver(cb, e)
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
    # Cada invocado tem letra própria ("Esqueleto A", "Esqueleto B") quando é a letra que diferencia os alvos.
    base = novo.nome
    if not cb.ui.letras_nos_alvos:
        novo.nome = f"{base} (invocado)"
    else:
        usados = {x.nome for x in cb.inimigos}
        letra = next((l for l in "ABCDEFGHIJKLMNOP" if f"{base} {l} (invocado)" not in usados), "Z")
        novo.nome = f"{base} {letra} (invocado)"
    novo.xp //= 2
    novo.ouro = 0
    cb.inimigos.append(novo)
    cb.dizer(f"{e.nome} convoca reforços: {novo.desc} entra na luta!", "vermelho+negrito")


# ----------------------------------------------------------------------
# Juízo: quando cada habilidade faz sentido. Sem isto o inimigo sorteava qualquer uma, e um lobo já furioso
# uivava de novo em vez de morder quem estava a um golpe da morte.
# ----------------------------------------------------------------------

def _sem(estado):
    """O alvo ainda não está assim, nem protegido disso (firme não pode ser travado de novo)."""
    from .estados import ESTADOS

    def ok(cb, e, alvo):
        return not alvo.efeito(estado) and not any(estado in ESTADOS.get(k, {}).get("protege", ()) for k in alvo.efeitos)
    return ok


def _alguem_sem(estado):
    """Algum do bando ainda sem o bônus (uivar com todos já furiosos é perder a vez)."""
    return lambda cb, e, alvo: any(not a.efeito(estado) for a in cb.inimigos_vivos())


def _cura_serve(cb, e, alvo):
    return (cb.turno - getattr(e, "curou_turno", -99) >= bal.INIMIGO_CURA_RECARGA
            and any(a.hp < a.max_hp * 0.6 for a in cb.inimigos_vivos()))


def hab_inimigo(fn, rotulo, nome, quando=None, golpe=False, anim=None):
    """Uma habilidade inimiga. rotulo: a faixa sobre a carta; nome: a ficha (Analisar, bestiário).
    quando(cb, e, alvo): se faz sentido agora (sem ela, sempre). golpe: causa dano (vale quando dá para matar).
    anim: o jeito de a tela animar (o mesmo vocabulário das habilidades do herói: "grito"...)."""
    return dict(fn=fn, rotulo=rotulo, nome=nome, quando=quando or (lambda cb, e, alvo: True), golpe=golpe, anim=anim)


HABS = {
    "mordida_sangrenta": hab_inimigo(_mordida_sangrenta, "Mordida Sangrenta", "garras que fazem sangrar", golpe=True),
    "uivo": hab_inimigo(_uivo, "Uivo", "uivo de matilha", quando=_alguem_sem("fortalecido")),
    "grito_guerra": hab_inimigo(_grito_guerra, "Grito de Guerra", "grito de guerra", quando=_alguem_sem("fortalecido"),
                                anim="grito"),
    "teia": hab_inimigo(_teia, "Teia", "teia paralisante", quando=_sem("atordoado")),
    "veneno": hab_inimigo(_veneno, "Veneno", "veneno", golpe=True),
    "golpe_sujo": hab_inimigo(_golpe_sujo, "Golpe Sujo", "golpe sujo", golpe=True),
    "roubar": hab_inimigo(_roubar, "Roubo", "rouba ouro", quando=lambda cb, e, alvo: alvo is cb.j and cb.j.ouro > 0),
    "investida": hab_inimigo(_investida, "Investida", "investida atordoante", golpe=True),
    "esmagar": hab_inimigo(_esmagar, "Preparar Golpe", "golpe esmagador (avisa antes)"),
    "regenerar": hab_inimigo(_regenerar, "Regenerar", "regeneração", quando=lambda cb, e, alvo: e.hp <= e.max_hp * 0.7),
    "agarrar": hab_inimigo(_agarrar, "Agarrão", "agarrão imobilizante", golpe=True),
    "drenar": hab_inimigo(_drenar, "Drenar", "drena vida", golpe=True),
    "maldicao": hab_inimigo(_maldicao, "Maldição", "maldição", quando=_sem("maldito")),
    "bola_fogo": hab_inimigo(_bola_fogo, "Bola de Fogo", "bola de fogo", golpe=True),
    "bola_sombra": hab_inimigo(_bola_sombra, "Esfera Sombria", "esfera sombria", golpe=True),
    "cura": hab_inimigo(_cura, "Cura", "cura aliados", quando=_cura_serve),
    "grito_terror": hab_inimigo(_grito_terror, "Grito de Terror", "grito de terror", quando=_sem("enfraquecido")),
    "mordida_gelida": hab_inimigo(_mordida_gelida, "Mordida Gélida", "mordida congelante", golpe=True),
    "invocar": hab_inimigo(_invocar, "Invocar", "invoca reforços",
                           quando=lambda cb, e, alvo: bool(e.invoca) and len(cb.inimigos_vivos()) < 4),
    "varredura": hab_inimigo(_varredura, "Varredura", "golpe em área (atinge você e seus aliados)", golpe=True),
    "reviver": hab_inimigo(_reviver, "Reviver", "ressuscita caídos",
                           quando=lambda cb, e, alvo: bool(_caidos_para_reviver(cb, e))),
    "devorar": hab_inimigo(_devorar, "Devorar", "devora cadáveres para se curar",
                           quando=lambda cb, e, alvo: bool(cb.mortos) and e.hp <= e.max_hp * 0.75),
}

# Derivados do catálogo (para quem só precisa de uma lista)
HABS_INIMIGO = {k: h["fn"] for k, h in HABS.items()}
NOMES_HABS_INIMIGO = {k: h["nome"] for k, h in HABS.items()}
ROTULOS_HABS_INIMIGO = {k: h["rotulo"] for k, h in HABS.items()}  # a faixa sobre a carta de quem age
