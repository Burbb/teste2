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
        a.fe = d.get("preces", 0)
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


def agir(cb, a):
    """Ação de um companheiro no turno dos aliados: cada um tem a sua (ACOES, logo abaixo)."""
    acao = ACOES.get(a.cid)
    if acao:
        acao(cb, a, cb.inimigos_vivos())


def _odete(cb, a, vivos):
    """Cura quem está mal (as preces da luta); sem ninguém para curar, luz sagrada."""
    feridos = [c for c in [cb.j] + [x for x in cb.aliados if x.vivo] if c.hp < c.max_hp * 0.4]
    if feridos and a.fe > 0:
        alvo = min(feridos, key=lambda c: c.hp / c.max_hp)
        cura = int(a.poder * 2.2 + alvo.max_hp * 0.12)
        ganho = alvo.curar(cura)
        a.fe -= 1
        quem = "você" if alvo is cb.j else alvo.nome
        cb.curou(alvo, ganho, de=a, rotulo="Prece")
        cb.detalhe(f"[Prece] Odette impõe as mãos sobre {quem}: +{ganho} de vida.", "verde")
        gritar(cb, a, "cura", 0.5)
        if a.membro["aprovacao"] >= 75:
            alvo.limpar_negativos()
        return
    cb.atacar(a, cb.rng.choice(vivos), 0.9, tipo="sagrado", rotulo="Odette")
    gritar(cb, a, "ataque", 0.15)


def _morel(cb, a, vivos):
    """Bate no mais fraco; às vezes o escudo atordoa."""
    alvo = min(vivos, key=lambda e: e.hp)
    dano = cb.atacar(a, alvo, 1.0, rotulo="Morel")
    if dano and cb.rng.random() < 0.2:
        if cb.aplicar(alvo, "atordoado", 1, rotulo="atordoado pelo escudo"):
            gritar(cb, a, "atordoa", 0.6)
            return
    gritar(cb, a, "ataque", 0.15)


def _yara(cb, a, vivos):
    """A cada três turnos amaldiçoa o inimigo mais forte; no resto, magia (sombra, se seguiu o Vazio)."""
    vazio = a.membro.get("caminho") == "vazio"
    sem_maldicao = [e for e in vivos if not e.efeito("enfraquecido")]
    if sem_maldicao and cb.turno % 3 == 1:
        alvo = max(sem_maldicao, key=lambda e: e.atk)
        cb.lance("feitico", de=cb.uid(a), em=cb.uid(alvo), elemento="sombra", rotulo="Maldição")
        cb.aplicar(alvo, "enfraquecido", 2, rotulo="amaldiçoado por Yara")
        if vazio:
            cb.aplicar(alvo, "maldito", 2)
        gritar(cb, a, "maldicao", 0.4)
        return
    tipo = "sombra" if vazio else "arcano"
    cb.atacar(a, cb.rng.choice(vivos), 1.5 if vazio else 1.0, tipo=tipo, alcance="distancia", stat="poder",
              rotulo="Yara")
    gritar(cb, a, "ataque", 0.15)


# A ação de cada companheiro na luta. Um companheiro novo declara a dele aqui (e os gritos em GRITOS).
ACOES = {"odete": _odete, "morel": _morel, "yara": _yara}


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
