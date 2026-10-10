"""O segundo eixo do Vale do Turvo (E4): Irmão Caspar e a perseguição à Yara (11-E1-REGIAO-INICIAL.md, seção 7).

Uma missão própria, "A Vigília de Caspar", ao lado de "A Febre do Turvo" e independente dela: a postura diante de Caspar
não depende de Ilse ter sido destruída ou ter descansado, e a febre, já concluída, não reabre.

    antes     → escondida (sem objetivo). Na investigação, voltando ao Vau depois do canal, a cena da acusação.
    acusacao  → Caspar acusou Yara; a resposta fica para quando a febre acabar (objetivo sem marcador).
    praca     → a guardiã foi resolvida: na praça, Caspar reivindica o fim da febre (uma cena, uma vez; quem não o
                conhecia o conhece aqui). Apoiar, Denunciar (com prova) ou Calar; ou deixar para depois e voltar à praça.
    desfecho  → "apoiar", "denunciado", "denuncia_falhou" ou "calar": guardado para o que vier depois, e a missão
                concluída sai do rastreador e do mapa e fica no Diário.

A prova da denúncia (seção 7): o caminho geral serve a qualquer classe e não se perde, o frasco do lodo da cripta
(recolhido no fundo da capela a qualquer momento depois de chegar lá, inclusive em saves com Ilse já resolvida) e o
canal (o que se viu no Bosque e na nave). A prova forte (a análise do mago ao recolher o lodo, ou as ervas da Yara, se
ela estiver no grupo na hora) facilita o teste de Carisma com que a praça recebe a denúncia.

Os números (reputação de cada postura, a dificuldade do teste) são calibragem desta entrega; a seção 7 diz só a direção.
"""

from . import comitiva as cm


def _missoes():
    """missoes.py importa este módulo no fim dele (as missões da região se juntam lá): daqui, só na hora de usar."""
    from . import missoes
    return missoes

MID = "vigilia_de_caspar"
FEBRE = "febre_do_turvo"
CD_DENUNCIA = 13          # Carisma, com a escala de nível de todo teste
CD_DENUNCIA_FORTE = 10    # com a prova forte
REPUTACAO = {"apoiar": 3, "denunciado": 3, "denuncia_falhou": -2, "calar": 0}

MISSOES = {
    MID: dict(
        nome="A Vigília de Caspar",
        campanha="turvo",
        etapas={
            "antes": dict(objetivo=None, lugar=None),
            "acusacao": dict(objetivo="Caspar acusa Yara, a moça do brejo, de trazer a febre. Quando a febre acabar, "
                                      "a praça vai querer uma resposta.", lugar=None),
            "praca": dict(objetivo="Responder a Caspar na praça do Vau.", lugar="vau_do_turvo"),
        },
        pistas={},
        preparos={
            "lodo": "Um frasco do lodo da cripta da capela: a mesma sujeira que a Fonte Nova trazia.",
            "analise": "Você analisou o lodo: é água parada que passou pelo que vazava na cripta, não feitiço de "
                       "ninguém.",
        },
    ),
}


def registro(g):
    return _missoes().registro(g, MID)


def _febre(g):
    return _missoes().registro(g, FEBRE)


# ------------------------------------------------------------------ Yara
def situacao_yara(g):
    """Onde está a Yara agora, para os textos: "grupo", "reserva", "morta", "recusou" ou "desconhecida"."""
    if cm.membro(g, "yara"):
        return "grupo"
    if cm.na_reserva(g, "yara"):
        return "reserva"
    return {"morto": "morta", "recusou": "recusou"}.get(g.flag("comitiva:yara"), "desconhecida")


def yara_barrada(g):
    """Apoiada, a vigília de Caspar não deixa a Yara entrar no Vau: ela espera do lado de fora (continua no grupo)."""
    m = registro(g) if g.campanha else None
    return bool(m and m.get("desfecho") == "apoiar" and situacao_yara(g) in ("grupo", "reserva"))


def _fora_do_vau(g, m):
    """A regra de ausência (comitiva.fora): barrada, a Yara que anda com você espera do lado de fora enquanto você está
    no Vau. Na estrada, ela volta para o seu lado; continua na comitiva o tempo todo."""
    if m["id"] != "yara" or g.na_estrada or not g.campanha or g.loc.get("chave") != "vau_do_turvo":
        return None
    if cm.membro(g, "yara") is not m or not yara_barrada(g):
        return None
    return {"curto": "espera fora do Vau",
            "texto": "Espera fora do Vau, na beira do brejo: a vigília de Caspar não a deixa entrar. Na estrada, volta "
                     "para o seu lado."}


cm.AUSENCIAS.append(_fora_do_vau)


def fogueira_possivel(g):
    """O evento da fogueira (eventos/comitiva.py: o pregador queima a moça no brejo) só cabe enquanto Caspar tem a
    praça: depois de denunciado (aceito ou não, a vigília acabou), ele não acontece mais. No mundo gerado, sempre."""
    m = registro(g) if g.campanha else None
    return not (m and m.get("desfecho") in ("denunciado", "denuncia_falhou"))


# ------------------------------------------------------------------ a prova
def prova(g):
    """(geral, forte): o lodo e o canal; a análise do mago ou as ervas da Yara no grupo."""
    m, f = registro(g), _febre(g)
    canal = bool({"canal_da_capela", "agua_da_capela"} & set(f["pistas"]))
    geral = "lodo" in m["preparos"] and canal
    forte = geral and ("analise" in m["preparos"] or situacao_yara(g) == "grupo")
    return geral, forte


def _requisitos(g, m):
    if m["etapa"] == "antes" or m.get("desfecho"):
        return None
    f = _febre(g)
    canal = bool({"canal_da_capela", "agua_da_capela"} & set(f["pistas"]))
    return {"titulo": "Para denunciar Caspar, você precisa de prova:", "itens": [
        {"texto": "O caminho da água, do canal à Fonte Nova", "onde": "o canal do Bosque do Moinho", "feito": canal},
        {"texto": "Um frasco do lodo da cripta", "onde": "o fundo da Capela Afogada", "feito": "lodo" in m["preparos"]},
    ]}


# ------------------------------------------------------------------ o que mudou (Diário e vila)
def linha_ilse(g):
    f, m = _febre(g), registro(g)
    if f.get("desfecho") == "destruida":
        return ("Ilse: os ossos dela foram tirados do fundo e queimados na praça, com Caspar rezando."
                if m.get("desfecho") == "apoiar" else "Ilse: os ossos dela ficaram no fundo da capela, sem nome.")
    if f.get("desfecho") == "descansada":
        return "Ilse: Vó Berta pôs uma pedra com o nome dela junto à fonte" + (
            "; Caspar finge não ver." if m.get("desfecho") == "apoiar" else ".")
    return None


LINHA_CASPAR = {
    "apoiar": "Caspar: conduz uma vigília na praça toda noite, e a vila gosta de você por isso.",
    "denunciado": "Caspar: perdeu a praça e foi embora do Vau.",
    "denuncia_falhou": "Caspar: ficou, mas ninguém volta à vigília; metade da vila olha torto para você.",
    "calar": "Caspar: segue pregando na praça, como antes.",
}


def linha_yara(g):
    m, onde = registro(g), situacao_yara(g)
    if onde == "morta":
        return "Yara: morreu na fogueira do brejo." + (" A praça sabe agora que ela não trouxe a febre."
                                                       if m.get("desfecho") == "denunciado" else "")
    postura = m.get("desfecho")
    if onde in ("grupo", "reserva"):
        return {"apoiar": "Yara: continua com você, mas a vigília não a deixa entrar no Vau. Quando você está na vila, "
                          "ela espera do lado de fora, na beira do brejo.",
                "denunciado": "Yara: anda livre pelo Vau.",
                "denuncia_falhou": "Yara: pode entrar no Vau, mas é vigiada.",
                "calar": "Yara: entra no Vau, mas evita a praça; ninguém a defende."}.get(postura)
    livre = postura in ("denunciado", "denuncia_falhou")
    if onde == "recusou":
        return "Yara: vive por conta própria no brejo, " + ("sem ninguém atrás dela." if livre else
                                                             "e a vigília ainda fala dela.")
    return ("Yara: a moça do brejo, que você não conhece, não é mais procurada por ninguém. Vive no Charco dos Juncos."
            if livre else
            "Yara: a moça do brejo, que você não conhece, segue acusada" + (" e procurada pela vigília."
                                                                            if postura == "apoiar" else "."))


def _linhas(g, m):
    return [linha_ilse(g), LINHA_CASPAR.get(m.get("desfecho")), linha_yara(g)]


FRASE_PRACA = {
    "apoiar": "Na praça, Caspar e uma dúzia de velas mantêm a vigília contra a bruxa.",
    "denunciado": "Onde ficava a tenda de Caspar, a praça está vazia.",
    "denuncia_falhou": "Caspar ainda prega na praça, para menos gente, e ninguém acende vela na vigília.",
    "calar": "Caspar segue pregando na praça, e a vila segue ouvindo.",
}


def frase_da_praca(g):
    """A frase da praça depois da decisão, e a da Yara barrada, se for o caso (consequencias.frase_da_vila)."""
    m = registro(g) if g.campanha else None
    if not m or not m.get("desfecho"):
        return None
    frase = FRASE_PRACA[m["desfecho"]]
    if yara_barrada(g) and situacao_yara(g) == "grupo":
        frase += " Yara espera do lado de fora, na beira do brejo: a vigília não a deixa entrar."
    return frase


CONCLUSOES = {
    "apoiar": "Você apoiou Caspar diante da vila.",
    "denunciado": "Você denunciou a perseguição, com prova, e a praça acreditou.",
    "denuncia_falhou": "Você denunciou a perseguição, com prova, mas a praça não quis ouvir.",
    "calar": "Você se calou diante da praça.",
}
MISSOES[MID].update(conclusoes=CONCLUSOES, requisitos=_requisitos, linhas=_linhas)


# ------------------------------------------------------------------ cenas e ações
def sincronizar(g):
    """Com a guardiã resolvida, a resposta a Caspar fica para a praça (também nos saves de antes desta entrega)."""
    m, f = registro(g), _febre(g)
    if m and f and f.get("desfecho") and m["etapa"] in ("antes", "acusacao"):
        m["etapa"] = "praca"


def _caspar_e_quem(g):
    return ("Na praça, um homem de batina remendada fala alto em cima de um caixote. É o Irmão Caspar. Veio da "
            "catedral, diz, e perdeu a mulher para a febre no inverno. Acredita em cada palavra que diz.")


def _acusacao(g, mid):
    """Na investigação, de volta ao Vau: Caspar acusa a Yara. Nada se decide aqui."""
    yara = situacao_yara(g)
    g.ui.cena("Irmão Caspar", g.contexto_cena(), "evento")
    g.narrar(_caspar_e_quem(g))
    if yara == "morta":
        g.narrar("\"Nós queimamos a bruxa do brejo\", grita ele, \"e a febre não passou! Então havia mais de uma. Olhem "
                 "para os vizinhos. Olhem para quem chega de fora.\"")
    else:
        g.narrar("\"A febre tem nome\", grita ele. \"Tem uma moça no brejo que fala com sapos e conhece toda erva que "
                 "mata. Yara. Desde que ela apareceu no Charco, o gado morre e as crianças queimam de febre.\"")
    g.narrar({
        "grupo": "Então ele vê Yara ao seu lado, e a praça inteira vê junto. \"E agora anda com gente armada\", diz "
                 "Caspar, mais baixo. Yara não abaixa os olhos.",
        "reserva": "Yara está no acampamento. Caspar ainda não sabe que ela anda com você.",
    }.get(yara, "Algumas pessoas concordam com a cabeça. Outras olham para o chão."))
    g.narrar("\"Quando a febre acabar\", promete Caspar, \"a vila vai saber de quem era a culpa. E quem estava do lado "
             "dela.\"")
    _missoes().avancar(g, mid, "antes", "acusacao")
    g.dizer(f"Diário: {MISSOES[MID]['etapas']['acusacao']['objetivo']}", "ciano")
    g.ui.efeito(f"Missão: {MISSOES[MID]['nome']}", "info")


def _praca(g, mid):
    """A guardiã foi resolvida: Caspar reivindica o fim da febre. A cena toca uma vez; a decisão pode ficar para depois
    (a ação "Ir à praça responder a Caspar" continua até a decisão)."""
    m = registro(g)
    f = _febre(g)
    yara = situacao_yara(g)
    g.ui.cena("A Praça do Vau", g.contexto_cena(), "evento")
    if "acusacao" not in m["cenas"]:  # quem não passou pelo Vau na investigação conhece Caspar aqui
        g.narrar(_caspar_e_quem(g) + " Faz semanas que ele culpa uma moça do brejo, Yara, pela febre.")
    g.narrar({
        "destruida": "\"A bruxa da capela foi destruída no fundo da água!\", grita Caspar para a vila reunida. \"Deus "
                     "fez justiça pelas mãos deste viajante. E a febre está indo embora com ela.\"",
        "descansada": "\"Rezamos, e a febre está cedendo!\", grita Caspar para a vila reunida. \"As nossas velas "
                      "fizeram a bruxa recuar.\"",
    }[f["desfecho"]])
    g.narrar("\"A fogueira no brejo fez o resto\", completa, e ninguém responde." if yara == "morta" else
             "\"Agora falta a do brejo\", completa. \"Yara. Enquanto ela andar solta, a febre volta.\"")
    if yara == "grupo":
        g.narrar("Ele aponta para Yara, ao seu lado, e a praça inteira se vira para ela. Yara não se mexe.")
    g.narrar("A praça olha para você, que voltou da capela.")
    _decidir(g)


def _ir_a_praca(g, mid):
    g.ui.cena("A Praça do Vau", g.contexto_cena(), "evento")
    g.narrar("Caspar continua no caixote, pregando contra a bruxa do brejo. Quando você chega, a praça se vira para "
             "ouvir.")
    _decidir(g)


def _decidir(g):
    m = registro(g)
    geral, forte = prova(g)
    if not geral:
        falta = [r["texto"][0].lower() + r["texto"][1:] for r in _requisitos(g, m)["itens"] if not r["feito"]]
        g.dizer("Para denunciar Caspar, falta prova: " + _lista(falta) + ". Dá para responder depois.", "cinza")
    opcoes = [
        ("Apoiar Caspar: foi a fé da vila", "apoiar"),
        ("Denunciar a perseguição: a febre veio da água, não da Yara (Carisma)", "denunciar") if geral else None,
        ("Calar-se", "calar"),
        ("Ainda não: responder depois", None),
    ]
    op = g.menu("O que você diz diante da vila?", [o for o in opcoes if o])
    if op is None:
        g.narrar("Você não diz nada por enquanto. Caspar continua pregando; a praça volta aos baldes.")
        g.dizer("Diário: responder a Caspar na praça do Vau, quando quiser.", "ciano")
        return
    _resolver(g, op, forte)


def _lista(itens):
    from . import texto as tx
    return tx.lista_natural(itens)


def _resolver(g, postura, forte=False):
    m = registro(g)
    if m.get("desfecho"):
        return
    yara = situacao_yara(g)
    if postura == "denunciar":
        g.narrar("Você ergue o frasco do lodo da cripta e conta o caminho da água: a represa, o canal, a capela "
                 "afundada, a Fonte Nova. A febre veio do que todos beberam, não de uma moça no brejo.")
        if forte:
            g.narrar("Yara mostra as ervas que a água da fonte matava em um dia." if yara == "grupo" else
                     "Você conta o que viu no lodo: água parada, nenhum feitiço de ninguém.")
        aceita = g.teste("carisma", CD_DENUNCIA_FORTE if forte else CD_DENUNCIA)
        postura = "denunciado" if aceita else "denuncia_falhou"
        if aceita:
            g.narrar("Um a um, os rostos mudam. Alguém apaga a primeira vela. Caspar olha a praça esvaziar e entende "
                     "antes de todos. Recolhe as velas e a tenda ali mesmo, diante de todos, e pega a estrada.")
        else:
            g.narrar("Metade da praça escuta; a outra metade cospe no chão. Caspar fica, mas ninguém volta à vigília, e "
                     "você sente os olhares quando passa.")
    elif postura == "apoiar":
        g.narrar("Você não desmente. Caspar te abraça diante da vila e chama todos para a vigília desta noite.")
        if _febre(g).get("desfecho") == "destruida":
            g.narrar("Ele manda buscar os ossos da bruxa no fundo da capela, para queimá-los na praça.")
    else:
        g.narrar("Você não diz nada. Caspar toma o silêncio como resposta, e a praça também.")
    if REPUTACAO[postura]:
        g.mudar_reputacao(REPUTACAO[postura])
    # A comitiva reage pelo que cada um valoriza (só quem está na praça com você); a Yara, se estiver com você, também
    # pelo que isto faz com ela. Antes de guardar o desfecho: apoiada a vigília, a Yara já não estaria "aqui" (fora do
    # Vau), mas ela estava na praça e viu.
    cm.reagir(g, *{"apoiar": ("fanatismo", "autoridade"), "denunciado": ("honestidade", "rebeldia"),
                   "denuncia_falhou": ("honestidade", "rebeldia"), "calar": ("cautela",)}[postura])
    if postura == "denunciado" and yara in ("grupo", "reserva"):
        cm.mudar_aprovacao(g, "yara", 5)
    m["desfecho"], m["dia_desfecho"] = postura, g.dia
    m["yara_na_praca"] = yara  # a conversa de depois sabe se ela viu ou ficou sabendo
    from .telemetria import registrar
    registrar(g, "missao", missao=MID, desfecho=postura)
    if postura in ("denunciado", "denuncia_falhou") and yara == "desconhecida":
        g.narrar("Ninguém mais procura a moça do brejo. Dizem que ela vive no Charco dos Juncos, entre os sapos.")
    if yara_barrada(g):
        g.narrar("Yara entende antes de você explicar. \"Eu espero do lado de fora\", diz, seca. \"Na beira do brejo. "
                 "Como sempre.\"" if yara == "grupo" else
                 "Quando voltar ao acampamento, você vai ter de contar à Yara que ela não entra mais no Vau.")
    m["concluida"] = g.dia
    g.dizer(f"Missão concluída: {MISSOES[MID]['nome']}. O que mudou fica no Diário.", "ciano")
    g.ui.efeito(f"Missão concluída: {MISSOES[MID]['nome']}", "info")


def _recolher_lodo(g, mid):
    """O frasco do lodo, no fundo da capela: a prova geral. A qualquer momento depois de chegar ao fundo."""
    m = registro(g)
    g.ui.cena("O Fundo da Capela", g.contexto_cena(), "evento")
    g.narrar("Você desce até a água da cripta e enche um frasco com o lodo escuro e fino do fundo, o mesmo que a Fonte "
             "Nova trazia.")
    if "lodo" not in m["preparos"]:
        m["preparos"].append("lodo")
    if g.j.classe == "mago" and "analise" not in m["preparos"]:
        g.narrar("À luz da tocha, você lê o lodo como se lê uma página: água parada, podre, que passou pelo que vazava "
                 "na cripta. Nenhum feitiço de ninguém. Isso a praça vai entender.")
        m["preparos"].append("analise")
    g.dizer("Diário: o frasco do lodo, prova para a praça.", "ciano")
    g.ui.efeito("Frasco do lodo da cripta", "info")


def _yara_no_charco(g, mid):
    """Denunciada a perseguição (aceita ou não, a vigília acabou), a fogueira do brejo não acontece mais: quem ainda não
    conhece a Yara a encontra livre no Charco, uma vez, na primeira chegada lá. Mesma apresentação e mesma oferta de
    vaga da fogueira (eventos/comitiva.py: yara_na_fogueira), sem a execução."""
    postura = registro(g)["desfecho"]
    g.ui.cena("A Moça do Brejo", g.contexto_cena(), "evento")
    g.narrar("Entre os juncos, uma moça de cabelo sujo de lama separa ervas em cima de uma pedra, com os pés na água. Os "
             "sapos em volta não fogem dela. Ela vê você chegar muito antes de você chegar perto.")
    g.narrar("\"Você é quem mostrou o lodo na praça\", diz. \"Caspar pegou a estrada. Aqui no brejo a notícia chega "
             "antes da poeira baixar.\"" if postura == "denunciado" else
             "\"Você é quem falou por mim na praça\", diz. \"Não convenceu todo mundo. Mas ninguém mais acende vela "
             "contra mim.\"")
    g.narrar("\"Yara\", diz, e enxuga as mãos na saia. \"Eu não tenho para onde ir que não seja este brejo.\" Um "
             "sorriso torto. \"E você tem cara de quem precisa de alguém que fale com sapos.\"")
    if cm.oferecer_vaga(g, "yara"):
        cm.mudar_aprovacao(g, "yara", SIMPATIA_CHARCO[postura], mostrar=False)
    else:
        g.narrar("Yara assente e some no brejo, entre a névoa, sem fazer barulho nenhum.", "cinza")
        g.marcar("comitiva:yara", "recusou")


# A aprovação com que a Yara do Charco começa (na fogueira, de -2 a 12 conforme o resgate): calibragem desta entrega.
SIMPATIA_CHARCO = {"denunciado": 5, "denuncia_falhou": 3}


def _chegou_ao_fundo(g):
    """O lodo está lá desde que se chega ao fundo, e continua lá depois da guardiã: não se perde a chance."""
    return _febre(g)["etapa"] in ("fundo", "retorno") and not registro(g).get("desfecho")


CENAS = [
    dict(missao=MID, id="acusacao", lugar="vau_do_turvo", etapas=("antes",), fn=_acusacao, confirmar=True,
         pode=lambda g: _febre(g)["etapa"] in ("capela", "sacristia", "ossuario", "fundo")
         and not _febre(g).get("desfecho")),
    # Depois da volta ao Vau (a cena `retorno` da febre vem antes, na ordem das cenas).
    dict(missao=MID, id="praca", lugar="vau_do_turvo", etapas=("praca",), fn=_praca, confirmar=True,
         pode=lambda g: "retorno" in _febre(g)["cenas"] and not registro(g).get("desfecho")),
    # Depois da decisão: a Yara que você ainda não conhece, livre no Charco (a fogueira não acontece mais).
    dict(missao=MID, id="yara_no_charco", lugar="charco_dos_juncos", etapas=("praca",), fn=_yara_no_charco,
         confirmar=True, pode=lambda g: not fogueira_possivel(g) and cm.disponivel(g, "yara")),
]
ACOES = [
    dict(missao=MID, id="lodo", rotulo="Recolher um frasco do lodo da cripta (prova)", lugar="capela_afogada",
         etapas=("antes", "acusacao", "praca"), falta="lodo", pode=_chegou_ao_fundo, fn=_recolher_lodo,
         confirmar=True),
    dict(missao=MID, id="praca", rotulo="Ir à praça responder a Caspar", lugar="vau_do_turvo", etapas=("praca",),
         pode=lambda g: "praca" in registro(g)["cenas"] and not registro(g).get("desfecho"), fn=_ir_a_praca,
         confirmar=True),
]


# ------------------------------------------------------------------ a conversa da Yara sobre a praça
# Uma vez, quando ela puder conversar (na comitiva ou na fogueira; não enquanto espera fora do Vau). Fala do que ela
# viu na praça (estava ao seu lado) ou ficou sabendo depois (no acampamento, ou antes de vocês se conhecerem). Não muda
# a aprovação: a reação dela à decisão já veio na praça.
FALA_PRACA = {
    ("apoiar", True): "\"Na praça, você olhou para mim e depois para ele\", diz Yara, sem tirar os olhos do fogo. \"E "
                      "escolheu ele. Eu entendo a conta: a vila gosta de você agora. Só não me peça para gostar da "
                      "vigília.\"",
    ("apoiar", False): "\"Fiquei sabendo da praça\", diz Yara, sem tirar os olhos do fogo. \"O pregador ganhou a vila, e "
                       "você ficou do lado dele. Agora eu durmo do lado de fora do Vau.\"",
    ("denunciado", True): "\"Ninguém nunca tinha falado por mim numa praça\", diz Yara, girando um graveto no fogo. \"Eu "
                          "fiquei esperando alguém gritar 'bruxa' de novo. Ninguém gritou.\"",
    ("denunciado", False): "\"Fiquei sabendo da praça\", diz Yara, girando um graveto no fogo. \"Caspar foi embora, e "
                           "dizem que foi você que mostrou o lodo. Ninguém nunca tinha falado por mim.\"",
    ("denuncia_falhou", True): "\"Metade da praça cuspiu no chão quando você falou\", diz Yara. \"A outra metade me "
                               "olhava como se olha um cachorro bravo. Mesmo assim, ninguém acendeu vela depois.\"",
    ("denuncia_falhou", False): "\"Fiquei sabendo da praça\", diz Yara. \"Você falou por mim e não adiantou. Adiantou um "
                                "pouco: a vigília apagou.\"",
    ("calar", True): "\"Na praça, você não disse nada\", diz Yara, sem tom nenhum. \"Eu também não. Mas era eu que estava "
                     "sendo acusada, então o meu silêncio era outra coisa.\"",
    ("calar", False): "\"Fiquei sabendo da praça\", diz Yara, sem tom nenhum. \"Caspar disse o meu nome para a vila "
                      "inteira, e você não disse nada.\"",
}
RESPOSTAS_PRACA = {
    "apoiar": [("\"Era o que a vila precisava ouvir para ter paz.\"",
                "\"Paz\", repete ela. \"A paz deles tem uma fogueira no meio. Eu fico do lado de fora, como sempre "
                "fiquei.\""),
               ("\"Foi um erro. Eu sinto muito.\"",
                "Ela fica quieta um tempo. \"Sentir não abre a porteira da vila. Mas é mais do que eles disseram.\"")],
    "denunciado": [("\"Eu só disse a verdade.\"",
                    "\"A verdade eu também dizia\", diz ela. \"A diferença é quem fala.\""),
                   ("\"Você não me deve nada por isso.\"",
                    "Um sorriso torto. \"Não devo. Mas lembro.\"")],
    "denuncia_falhou": [("\"Eu devia ter falado melhor.\"",
                         "\"Você falou\", diz ela. \"Já é mais do que eu esperava daquela vila.\""),
                        ("\"Eles não queriam ouvir.\"",
                         "\"Nunca querem\", diz Yara. \"Mas agora sabem que alguém disse.\"")],
    "calar": [("\"Não era a hora de brigar com a vila.\"",
               "\"Para mim nunca é a hora\", diz ela. \"É sempre a hora de outra pessoa.\""),
              ("\"Eu não tinha certeza de nada.\"",
               "\"E agora tem?\", pergunta ela, e não espera a resposta.")],
}


def _quer_falar_da_praca(g, m):
    c = registro(g) if g.campanha else None
    if not c or not c.get("desfecho"):
        return False
    # Quem a conheceu depois da praça (no Charco, na fogueira) fala dela num outro dia, não junto com a apresentação.
    return c.get("yara_na_praca") in ("grupo", "reserva") or m.get("desde", g.dia) < g.dia


@cm.avulsa("yara", "praca", _quer_falar_da_praca)
def _yara_fala_da_praca(g, m):
    c = registro(g)
    postura = c["desfecho"]
    g.dizer(FALA_PRACA[(postura, c.get("yara_na_praca") == "grupo")])
    respostas = RESPOSTAS_PRACA[postura]
    op = g.menu("O que diz?", [(r, i) for i, (r, _) in enumerate(respostas)])
    g.dizer(respostas[op or 0][1], "cinza")
