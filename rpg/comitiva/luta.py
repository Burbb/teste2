"""A comitiva na luta: quem entra, quem chama a atenção dos inimigos, os gritos e a ação de cada um."""

from .. import balanceamento as bal
from .catalogo import COMPANHEIROS, GRITOS
from .grupo import atributos, fora, junto, lealdade, membro, nome


def preparar_combate(cb):
    """Cria os aliados da comitiva para esta luta. Feridos ficam na retaguarda; quem não está aqui (grupo.fora), também
    não luta."""
    from ..combate import Aliado
    g = cb.g
    lista = []
    for m in junto(g):
        if m["ferido"] or m["hp"] <= 0:
            continue
        d = COMPANHEIROS[m["id"]]
        at = atributos(g, m)
        f = lealdade(m)
        a = Aliado(d["curto"], m["max_hp"], at["atk"] * f, at["agi"], tipo="comitiva")
        a.hp = m["hp"]
        a.g = d["g"]
        a.poder = at["poder"] * f
        a.defesa = at["defesa"]
        a.cid = m["id"]
        a.membro = m
        # etapa 4 (roadmapIDEIAS/26): você escolhe a ação dela na vez dela; o recurso é dela e volta cheio a cada luta
        a.rec = a.max_rec = bal.RECURSO_COMITIVA
        a.regen = 5
        a.nome_recurso = RECURSO[m["id"]]
        a.vontade = VONTADE[m["id"]]  # a Tenacidade (atributos.tenacidade)
        lista.append(a)
        cb.aliados.append(a)
    # Inimigos que enfrentam um grupo resistem mais (e chefes, feitos para um herói só, mais ainda).
    for e in cb.inimigos:
        fator = 1 + (bal.COMITIVA_VIDA_CHEFE if e.chefe else bal.COMITIVA_VIDA_INIMIGO) * len(lista)
        e.max_hp = int(e.max_hp * fator)
        e.hp = int(e.hp * fator)
    if lista and len(lista) == len(junto(g)):
        cb.dizer(f"{' e '.join(a.nome for a in lista)} se {'posicionam' if len(lista) > 1 else 'posiciona'} ao seu lado.", "ciano")
    feridos = [m for m in junto(g) if m["ferido"]]
    if feridos:
        cb.dizer(f"{' e '.join(nome(m['id']) for m in feridos)} ainda se recupera{'m' if len(feridos) > 1 else ''} "
                 "e fica para trás.", "cinza")
    return lista


def alvo_inimigo(cb, aliados, e=None):
    """Quem protege (`protege` na ficha: Morel) chama a atenção dos inimigos para si (chefes caem menos nessa)."""
    tanque = next((a for a in aliados if COMPANHEIROS.get(getattr(a, "cid", None), {}).get("protege")), None)
    p = COMPANHEIROS[tanque.cid]["protege"] if tanque else {"chance": 0.3}
    chance = p["leal"] if tanque and tanque.membro["aprovacao"] >= p["a_partir"] else p["chance"]
    if e is not None and e.chefe:
        chance /= 2
    if tanque and cb.rng.random() < chance:
        return tanque
    return None


def gritar(cb, a, situacao, chance=0.3):
    banco = GRITOS.get(a.cid, {}).get(situacao)
    if not banco or cb._fala_turno == cb.turno or cb.rng.random() >= chance:
        return
    cb._fala_turno = cb.turno
    cb.ui.fala(a.cid, a.nome, cb.rng.choice(banco))


# ------------------------------------------------------------ o kit de cada um (etapa 4)
# Na vez de um companheiro, você escolhe: Atacar, Defender, Usar item (a bolsa é a do grupo) ou uma habilidade do kit
# dele (heroi.vez_comitiva). O kit é fixo e menor que o seu (roadmapIDEIAS/25, 3.4); números provisórios.
RECURSO = {"odete": "Fé", "morel": "Vigor", "yara": "Mana"}
VONTADE = {"odete": 6, "morel": 3, "yara": 7}
ATAQUE = {  # o golpe de toda vez: (nome, multiplicador, tipo, alcance, stat)
    "odete": ("Bastão", 0.9, "sagrado", "corpo", "atk"),
    "morel": ("Golpe", 1.0, "fisico", "corpo", "atk"),
    "yara": ("Dardo", 1.0, "arcano", "distancia", "poder"),
}


def _prece(cb, a, alvo):
    cura = int(a.poder * 2.2 + alvo.max_hp * 0.12)
    ganho = alvo.curar(cura)
    cb.curou(alvo, ganho, de=a, rotulo="Prece")
    cb.detalhe(f"[Prece] Odette cura {cb.nome(alvo, True)}: +{ganho} de vida.", "verde")
    if a.membro["aprovacao"] >= 75:
        alvo.limpar_negativos()
    gritar(cb, a, "cura", 0.5)


def _escudo_luz(cb, a, alvo):
    v = int(8 + a.poder * 1.2)
    alvo.remover("barreira")
    alvo.aplicar("barreira", 2, v)
    cb.lance("buff", em=cb.uid(alvo), efeitos=["barreira"], rotulo="Escudo de Luz")
    cb.detalhe(f"[Escudo de Luz] {cb.nome(alvo)} fica com uma barreira de {v}.", "ciano")


def _reerguer(cb, a, alvo):
    cb.reerguer(a, alvo, "Reerguer", bal.REERGUER)


def _joelho(cb, a, alvo):
    dano = cb.atacar(a, alvo, 0.6, rotulo="Golpe no Joelho")
    if dano and alvo.vivo:
        if cb.aplicar(alvo, "atordoado", 1, chance=0.7, rotulo="atordoado"):
            gritar(cb, a, "atordoa", 0.6)


def _oportuno(cb, a, alvo):
    brecha = alvo.efeito("atordoado") or getattr(alvo, "carregando", None)
    cb.atacar(a, alvo, 1.2 * (1.6 if brecha else 1.0), rotulo="Golpe Oportuno")


def _proteger_morel(cb, a, alvo):
    from ..habilidades import HABILIDADES
    HABILIDADES["proteger"]["fn"](cb, a, alvo)


def _maldicao_yara(cb, a, alvo):
    cb.lance("feitico", de=cb.uid(a), em=cb.uid(alvo), elemento="sombra", rotulo="Maldição")
    cb.aplicar(alvo, "enfraquecido", 2, rotulo="amaldiçoado por Yara")
    if a.membro.get("caminho") == "vazio":
        cb.aplicar(alvo, "maldito", 2)
    gritar(cb, a, "maldicao", 0.4)


def _runa_yara(cb, a, alvo):
    cb.aplicar(alvo, "fragilizado", 2, 0.25)


def _seta_sombria(cb, a, alvo):
    vazio = a.membro.get("caminho") == "vazio"
    cb.atacar(a, alvo, 1.7 if vazio else 1.5, tipo="sombra" if vazio else "arcano", alcance="distancia", stat="poder",
              rotulo="Seta Sombria")


def _acao(id, nome, custo, alvo, desc, fn, icone, familia, **extra):
    return dict(id=id, nome=nome, custo=custo, alvo=alvo, desc=desc, fn=fn, icone=icone, familia=familia, **extra)


KITS = {
    "odete": [
        _acao("prece", "Prece", 14, "aliado",
              "Cura o aliado em 220% do Poder + 12% da vida máxima dele. Com a aprovação de Odette em 75 ou mais, "
              "também remove os males.", _prece, "coracao", "cura"),
        _acao("escudo_luz", "Escudo de Luz", 12, "aliado",
              "Dá ao aliado uma barreira que absorve 8 + 120% do Poder em dano por 2 turnos dele.",
              _escudo_luz, "escudo_azul", "protecao"),
        _acao("reerguer", "Reerguer", 30, "aliado_caido",
              "Levanta um aliado caído com 30% da vida, no mesmo lugar da ordem. Uma vez por luta.",
              _reerguer, "orbe_luz", "sagrado", uma_vez=True),
    ],
    "morel": [
        _acao("joelho", "Golpe no Joelho", 15, "inimigo",
              "Causa 60% do Ataque em dano físico. Se acertar, 70% de chance de atordoar o alvo: ele perde a "
              "próxima vez e o golpe que preparava.", _joelho, "martelo", "fisico"),
        _acao("oportuno", "Golpe Oportuno", 10, "inimigo",
              "Causa 120% do Ataque em dano físico; 60% a mais em alvo atordoado ou preparando um golpe.",
              _oportuno, "espada", "fisico"),
        _acao("proteger", "Proteger", 8, "aliado",
              "Até a próxima vez de Morel, os golpes contra o aliado escolhido acertam Morel.",
              _proteger_morel, "escudo", "protecao"),
    ],
    "yara": [
        _acao("maldicao", "Maldição", 12, "inimigo",
              "O alvo causa 25% menos dano por 2 turnos dele. Pelo caminho do Vazio, também aplica Maldição: dano "
              "por turno e −40% de defesa.", _maldicao_yara, "orbe_sombra", "sombra"),
        _acao("runa", "Runa da Fragilidade", 10, "inimigo",
              "O alvo recebe 25% mais dano mágico (todo golpe que não é físico) por 2 turnos dele.",
              _runa_yara, "orbe_sombra", "arcano"),
        _acao("seta", "Seta Sombria", 16, "inimigo",
              "Causa 150% do Poder em dano arcano. Pelo caminho do Vazio, 170% em dano de sombra.",
              _seta_sombria, "orbe", "arcano"),
    ],
}


def encerrar_combate(cb, resultado):
    """Devolve a vida aos membros; quem caiu fica desacordado e só volta a lutar depois de descansar."""
    g = cb.g
    for a in cb.aliados:
        m = getattr(a, "membro", None)
        if not m or m not in g.comitiva:
            continue
        if a.vivo:
            m["hp"] = a.hp
            continue
        if resultado == "derrota":
            continue
        m["hp"] = 1
        m["ferido"] = True
        g.dizer(f"{a.nome} está caíd{'a' if a.g == 'f' else 'o'}, mas respira. Vai precisar de uma noite "
                "de descanso antes de lutar de novo.", "amarelo")
    yara = membro(g, "yara")
    if yara and not fora(g, yara) and yara.get("caminho") == "vazio" and resultado == "vitoria":
        # o poder da Fenda cobra o seu preço: Yara bebe um pouco da sua vida a cada luta
        g.j.hp = max(1, g.j.hp - max(1, int(g.j.max_hp * bal.YARA_VAZIO_CUSTO)))
