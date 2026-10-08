"""O catálogo de estados: veneno, queimadura, guarda, provocando...

Cada estado declara, num lugar só, tudo o que o jogo precisa saber dele:

    nome        como aparece ("envenenado") · icone/familia: o desenho e a cor do brilho na carta
    negativo    é um mal (a Prece e o "limpar males" tiram)
    tique       dano a cada turno: (rótulo no registro, cor) — o valor vem do próprio estado (v)
    perde_turno quem está assim não age (atordoado, congelado, preso na armadilha)
    depois      o estado que fica quando este faz perder o turno (atordoado deixa "firme": sem trava em sequência)
    protege     estados que não pegam em quem está assim (firme: atordoado)
    imune       quem não pega (veneno não pega em mortos-vivos e construtos...)
    resiste     quem pode resistir na hora, com sorteio (chefes e gigantes contra o atordoamento)
    camadas     acumula até N camadas (queimadura), com o rótulo "em chamas ×N"
    dica        uma frase a mais na dica do ícone
    descrever   como o Grimório escreve uma habilidade que aplica o estado num inimigo
    buff        como o Grimório escreve o estado aplicado em você
    golpe       o que o estado muda num golpe, por etapa da conta (GOLPE_ETAPAS); `v` é o valor do estado

O combate só lê o catálogo: aplicar() pergunta imune/resiste/camadas, processar_efeitos() faz o tique e a
perda de turno, atacar() pergunta cada etapa do golpe (no_golpe), a tela recebe ícone, família e dica.
Estado novo = uma entrada aqui. Dentro de uma etapa, as contas seguem a ordem do catálogo.
"""

from . import balanceamento as bal


def _pct(x):
    return f"{x * 100:.0f}%"


def _num(x):
    return f"{x:.1f}".replace(".", ",").replace(",0", "")


def _turnos(t):
    return f"{t} turno{'s' if t != 1 else ''}"


def _chance(c, texto):
    """'45% de chance de ' + texto, ou o texto com maiúscula quando é certo."""
    return f"{_pct(c)} de chance de {texto}" if c < 1 else texto[0].upper() + texto[1:]


def _quem(todos):
    return "cada inimigo" if todos else "o alvo"


def _origem(escala):
    return f" ({escala})" if escala else ""


# As etapas de Combate.atacar em que um estado pode entrar, na ordem da conta. Quem está assim é o atacante (de
# quem bate) ou o alvo (de quem apanha). O valor: uma função do valor do estado (v), salvo onde diz outra coisa.
GOLPE_ETAPAS = {
    "sem_esquiva":       "alvo: não consegue se esquivar (True)",
    "esquiva":           "alvo: soma à chance de esquiva",
    "dano_causado":      "atacante: multiplica o dano",
    "dano_recebido":     "alvo: multiplica o dano (antes da defesa)",
    "defesa":            "alvo: multiplica a defesa",
    "critico_garantido": "atacante: o golpe é crítico (o motivo que a tela mostra) e o estado se gasta",
    "dano_final":        "alvo: multiplica o dano depois do crítico (antes de arredondar)",
    "absorve":           "alvo: o valor do estado absorve dano e se gasta (True)",
}


def estado(nome, icone, familia, negativo=False, tique=None, perde_turno=False, imune=None, resiste=None,
           camadas=0, rotulo_camadas=None, dica="", descrever=None, buff=None, ajuste_tique=None, golpe=None,
           depois=None, protege=()):
    return dict(nome=nome, icone=icone, familia=familia, negativo=negativo, tique=tique, perde_turno=perde_turno,
                imune=imune, resiste=resiste, camadas=camadas, rotulo_camadas=rotulo_camadas, dica=dica,
                descrever=descrever, buff=buff, ajuste_tique=ajuste_tique, golpe=golpe or {}, depois=depois,
                protege=protege)


def _chuva_apaga(cb, dano):
    """A chuva enfraquece as chamas."""
    return max(1, int(dano * 0.7)) if cb.g.clima == "chuva" else dano


ESTADOS = {
    # --- bênçãos (antes dos males: na conta do golpe, o bônus multiplica primeiro)
    "guarda": estado("em guarda", "escudo", "protecao", dica="recebe menos dano",
                     buff=lambda u, t, v: f"Dano recebido −{_pct(v)} por {_turnos(t)}.",
                     golpe={"dano_final": lambda v: 1 - v}),
    "fortalecido": estado("fortalecido", "espada", "forca", dica="causa mais dano",
                          buff=lambda u, t, v: f"Seu dano +{_pct(v)} por {_turnos(t)}.",
                          golpe={"dano_causado": lambda v: 1 + v}),
    "esquiva": estado("esquivo", "folha", "protecao", dica="mais difícil de acertar", buff=lambda u, t, v: _buff_esquiva(u, t, v),
                      golpe={"esquiva": lambda v: v}),
    "barreira": estado("com barreira", "escudo_azul", "protecao", dica="absorve dano", golpe={"absorve": True}),
    "furtivo": estado("furtivo", "olho", "sombra", dica="o próximo ataque é crítico garantido",
                      buff=lambda u, t, v: _buff_furtivo(u), golpe={"critico_garantido": "Furtivo"}),
    "provocando": estado("provocando", "caveira", "forca", dica="os inimigos atacam ele"),
    # Quem acaba de perder o turno não perde o seguinte (como em Darkest Dungeon e WoW): sem trava em sequência.
    "firme": estado("firme", "cadeado", "protecao", dica="acabou de se soltar: não pode ser atordoado nem congelado agora",
                    protege=("atordoado",)),
    # --- males (dano por turno)
    "veneno": estado(
        "envenenado", "gota_verde", "veneno", negativo=True, tique=("veneno", "verde"),
        imune=lambda a: "morto-vivo" in a.tracos or "construto" in a.tracos,
        descrever=lambda t, v, esc, ch, todos, rot: _chance(ch, f"veneno: {_num(v)} por turno, {_turnos(t)}{_origem(esc)}.")),
    "sangramento": estado(
        "sangrando", "gota", "sangue", negativo=True, tique=("sangramento", "vermelho"),
        imune=lambda a: "construto" in a.tracos or "etereo" in a.tracos,
        descrever=lambda t, v, esc, ch, todos, rot: _chance(ch, f"sangramento: {_num(v)} por turno, {_turnos(t)}{_origem(esc)}.")),
    "queimadura": estado(
        "em chamas", "chama", "fogo", negativo=True, tique=("queimadura", "amarelo"),
        imune=lambda a: a.resist.get("fogo", 1) < 0.5, camadas=bal.MAX_CHAMAS, rotulo_camadas="em chamas ×{s}",
        ajuste_tique=_chuva_apaga, dica="a Combustão detona o que falta arder"),
    "maldito": estado(
        "amaldiçoado", "gota_roxa", "maldicao", negativo=True, tique=("maldição", "magenta"),
        dica="defesa −40%", golpe={"defesa": lambda v: 0.6},
        descrever=lambda t, v, esc, ch, todos, rot: (f"{'Todos os inimigos' if todos else 'O alvo'}: {_num(v)} de dano "
                                                     f"por turno, {_turnos(t)}{_origem(esc)}, e −40% de defesa.")),
    # --- males (controle e fraqueza)
    "atordoado": estado(
        "atordoado", "estrela", "atordoado", negativo=True, perde_turno=True,
        resiste=lambda cb, a: (a.chefe or "gigante" in a.tracos) and cb.rng.random() < 0.5,
        dica="perde o próximo turno (depois fica firme por um turno)", golpe={"sem_esquiva": True}, depois="firme",
        descrever=lambda t, v, esc, ch, todos, rot: (
            _chance(ch, f"congelar {_quem(todos)} (perde o próximo turno).") if rot == "congelado"
            else _chance(ch, f"atordoar {_quem(todos)} por {_turnos(t)}."))),
    "enfraquecido": estado(
        "enfraquecido", "osso", "maldicao", negativo=True, dica="causa −25% de dano",
        golpe={"dano_causado": lambda v: 0.75},
        descrever=lambda t, v, esc, ch, todos, rot: _chance(ch, f"enfraquecer {_quem(todos)} por {_turnos(t)} (causa −25% de dano).")),
    "marcado": estado(
        "marcado", "flecha", "marca", negativo=True, dica="recebe mais dano de todos",
        golpe={"dano_recebido": lambda v: 1 + v},
        descrever=lambda t, v, esc, ch, todos, rot: f"{_quem(todos)[0].upper() + _quem(todos)[1:]} recebe +{_pct(v)} de dano de todos por {_turnos(t)}."),
}


def _buff_esquiva(u, t, v):
    base = min(bal.ESQUIVA_MAX_AGI, u.agi * bal.ESQUIVA_POR_AGI)
    return (f"Esquiva +{_pct(v)} por {_turnos(t)}: de {_pct(base)} para {_pct(min(bal.MAX_ESQUIVA, base + v))} "
            f"(teto de {_pct(bal.MAX_ESQUIVA)}).")


def _buff_furtivo(u):
    from .grimorio import mult_critico
    return f"O próximo ataque é crítico garantido de ×{_num(mult_critico(u, furtivo=True))}."


# Derivados do catálogo (para quem só precisa de uma lista)
NOMES = {k: e["nome"] for k, e in ESTADOS.items()}
NEGATIVOS = tuple(k for k, e in ESTADOS.items() if e["negativo"])
GOLPE = {etapa: [(k, e["golpe"][etapa]) for k, e in ESTADOS.items() if etapa in e["golpe"]] for etapa in GOLPE_ETAPAS}


def no_golpe(u, etapa):
    """(estado de u, o que ele faz nessa etapa) de cada estado que `u` tem e que mexe nessa etapa do golpe."""
    lista = []
    for k, valor in GOLPE[etapa]:
        e = u.efeito(k)
        if e:
            lista.append((k, e, valor))
    return lista


def descrever_aplicar(efeito, turnos, valor, escala, chance, todos, rotulo):
    """A linha do Grimório para uma habilidade que aplica `efeito` num inimigo."""
    e = ESTADOS.get(efeito)
    if e and e["descrever"]:
        return e["descrever"](turnos, valor, escala, chance, todos, rotulo)
    return _chance(chance, f"{efeito} por {_turnos(turnos)}.")


def descrever_buff(u, efeito, turnos, valor):
    """A linha do Grimório para um estado que a habilidade põe em você."""
    e = ESTADOS.get(efeito)
    if e and e["buff"]:
        return e["buff"](u, turnos, valor)
    return f"{(e or {}).get('nome', efeito)} por {_turnos(turnos)}."


def para_tela():
    """O que a interface precisa de cada estado: ícone, família (cor do brilho), nome e dica."""
    return {k: {"icone": e["icone"], "familia": e["familia"], "nome": e["nome"], "dica": e["dica"]}
            for k, e in ESTADOS.items()}
