"""Missões da campanha escrita: um registro por missão, com id estável e etapas explícitas.

E3 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md, seção 5): "A Febre do Turvo" começa com uma cena curta no Vau do Turvo; a
investigação segue a água da fonte nova até o canal no Bosque do Moinho e o canal até a Capela Afogada. Dentro dela, três
salas em sequência (a nave, a sacristia, o ossuário), cada uma uma ação do menu da capela: sair e voltar é só escolher
outra coisa no menu, e a sala vencida fica vencida (a etapa já passou dela). No fundo, a guardiã: Ilse, que em vida
tinha a custódia do Sigilo do Turvo e, afogada pela vila, virou a Bruxa Afogada. Destruí-la ou dar-lhe descanso (o rito,
com a verdade, a fita e as correntes soltas) é um desfecho único e guardado. Depois, a volta ao Vau: uma cena, uma vez,
que conclui a missão (`concluida`, o dia). O que o desfecho muda no Vau mora em consequencias.py. A comporta, Caspar, o
julgamento na praça e a Estrada de Varn ainda não existem.

O estado de cada missão mora no mundo da campanha (`mundo["missoes"]`, vai no save junto com ele):
    {"etapa": "fundo", "cenas": ["abertura"], "pistas": ["agua_do_leste", ...], "preparos": ["corpo_solto", "fita"],
     "desfecho": None, "dia_desfecho": None, "concluida": None}
`pistas` é o que se sabe; `preparos` é o que se fez ou se tem para depois (as correntes soltas, a fita de Ilse). Saber o
nome não prepara nada: o rito pede a verdade (sacristia e Vó Berta), a fita e as correntes. `desfecho`: "destruida" ou
"descansada", uma vez só; com ele vêm o Sigilo e a recompensa, e `dia_desfecho` (de onde sai o estado da fonte nova).
`concluida`: o dia em que a missão terminou (a cena de volta ao Vau); concluída, ela sai do rastreador e do mapa e fica no
Diário. A herança de Berta continua valendo depois da conclusão, até ser entregue.
O mundo gerado não tem missões. Cenas e ações declaram a campanha (pela missão), o lugar (`chave` do lugar) e as
etapas em que valem; o jogo só as oferece no menu do lugar, nunca no meio de uma luta, de uma viagem ou de um evento.
Passar antes por um lugar não adianta nem gasta nada: a cena ou a ação esperam a etapa delas.
"""

from . import texto as tx

MISSOES = {
    "febre_do_turvo": dict(
        nome="A Febre do Turvo",
        campanha="turvo",
        # Em ordem. Cada etapa: o objetivo do Diário e onde ele leva (a chave do lugar, para o rastreador e o mapa).
        etapas={
            "fonte": dict(objetivo="Descobrir de onde vem a febre: examinar a fonte nova, no Vau do Turvo.",
                          lugar="vau_do_turvo"),
            "canal": dict(objetivo="Seguir a água da fonte nova até o canal, no Bosque do Moinho.",
                          lugar="bosque_do_moinho"),
            "capela": dict(objetivo="Entrar na Capela Afogada, no pântano, aonde o canal do moinho leva.",
                           lugar="capela_afogada"),
            "sacristia": dict(objetivo="Atravessar o salão alagado da capela até a sacristia, atrás do altar.",
                              lugar="capela_afogada"),
            "ossuario": dict(objetivo="Descer ao ossuário, a sala dos ossos embaixo da sacristia.",
                             lugar="capela_afogada"),
            "fundo": dict(objetivo="Descer ao fundo alagado da capela, para onde vão as correntes, e enfrentar o que "
                                   "está lá.", lugar="capela_afogada"),
            "retorno": dict(objetivo="Voltar ao Vau do Turvo com o Sigilo.", lugar="vau_do_turvo"),
        },
        pistas={
            "agua_do_leste": "A fonte nova não nasce ali: a água chega por baixo da terra, do leste, do lado do Bosque "
                             "do Moinho, e traz um lodo escuro e fino que água de nascente não tem.",
            "represa": "No ano passado, o dono do moinho fez uma represa no riacho, acima da roda, e abriu um canal "
                       "para leste. O trecho que descia para a vila minguou: é por isso que o poço da praça secou.",
            "canal_da_capela": "O canal do moinho corre até o pântano e entra por um buraco no muro de uma capela "
                               "afundada, a Capela Afogada. Abaixo dela, a terra está encharcada na direção da vila.",
            "agua_da_capela": "Dentro da capela, a água do canal atravessa o salão principal, desce por uma fenda do piso e sai "
                              "por baixo do muro dos fundos, rumo à vila. Entra limpa e sai com o lodo escuro: é a "
                              "água da fonte nova.",
            "ilse": "A capela tinha uma guardiã, Ilse. A vila a acusou de bruxaria e a afogou; o padre que escreveu o "
                    "livro da sacristia diz que ela não fez nada do que disseram.",
            "sigilo_do_turvo": "Em vida, Ilse guardava o Sigilo do Turvo, deixado na capela pela Igreja quando a "
                               "Fenda foi fechada, para não sair dali. Ele foi para a água com ela.",
            "marcados": "Dois homens com uma marca queimada no pulso reviravam a sacristia atrás de alguma coisa. "
                        "Não eram da vila, e não estavam sozinhos.",
            "correntes": "No ossuário, um sarilho velho, o eixo de madeira em que as correntes se enrolam, segura "
                         "correntes que descem ao fundo alagado da capela, amarradas a duas pedras de moinho. Alguma "
                         "coisa está presa lá embaixo.",
            "verdade_de_ilse": "Vó Berta viu, aos oito anos: a vila inteira tirou Ilse de casa, amarrou-a a duas "
                               "pedras de moinho e a desceu ao fundo da capela. O pai dela segurou a corda. Ninguém "
                               "mandou parar.",
            "nome_e_fita": "Berta acredita que Ilse pode descansar se alguém a chamar pelo nome, devolver a fita dela e "
                           "a soltar das pedras. A guardiã não precisaria ser destruída.",
            "relato_de_ilse": "Ilse disse que o Sigilo é um de três, que os três seguram fechada uma porta que agora "
                              "range, e que há mãos procurando juntá-los.",
        },
        # O nome curto de cada pista e preparo: o cartão de novidade (o que a cena acabou de mostrar) usa estes.
        titulos={
            "agua_do_leste": "A água da fonte nova vem do leste, com lodo",
            "represa": "O dono do moinho fez uma represa no riacho e abriu um canal",
            "canal_da_capela": "O canal entra na Capela Afogada",
            "agua_da_capela": "A água suja passa por dentro da capela, rumo à vila",
            "ilse": "Ilse, a guardiã da capela, foi afogada pela vila",
            "sigilo_do_turvo": "O Sigilo do Turvo foi para a água com ela",
            "marcados": "Homens com uma marca no pulso procuram alguma coisa",
            "correntes": "Correntes prendem algo no fundo alagado",
            "verdade_de_ilse": "Vó Berta contou como Ilse morreu",
            "nome_e_fita": "Vó Berta contou como um afogado descansa",
            "relato_de_ilse": "Ilse falou dos três Sigilos",
            "corpo_solto": "As correntes estão soltas",
            "fita": "Você tem a fita de Ilse",
        },
        # O que se faz para depois. Não é saber: conhecer o nome de Ilse é pista, não preparo.
        preparos={
            "corpo_solto": "As correntes do sarilho estão soltas: o que está no fundo da capela não está mais preso às "
                           "pedras de moinho.",
            "fita": "A fita de Ilse, que Vó Berta guardou desde a noite do afogamento e entregou a você.",
        },
    ),
}


def estado_inicial(regiao):
    """As missões de uma campanha no começo: cada uma na primeira etapa, sem cenas vistas nem pistas."""
    return {mid: {"etapa": next(iter(m["etapas"])), "cenas": [], "pistas": [], "preparos": [], "desfecho": None,
                  "dia_desfecho": None, "concluida": None, "historico": []}
            for mid, m in MISSOES.items() if m["campanha"] == regiao}


def completar(estado):
    """Saves de antes dos preparos (1.50–1.51), do desfecho (1.50–1.52) e da conclusão (1.50–1.53): as chaves entram
    vazias. O resto do progresso (etapa, cenas, pistas, as correntes soltas) fica como estava. O dia do desfecho de um
    save que já o tinha é posto por campanha.ajustar_save (é preciso o dia de agora)."""
    for m in estado.values():
        m.setdefault("preparos", [])
        m.setdefault("desfecho", None)
        m.setdefault("dia_desfecho", None)
        m.setdefault("concluida", None)
        # O histórico datado começa nesta versão: um save de antes fica sem ele (as pistas antigas aparecem sem data).


# Dar descanso a Ilse pede três coisas (11-E1-REGIAO-INICIAL.md, seção 6): saber a verdade, ter a fita e ter soltado o
# corpo. Quem ensina isso é Vó Berta ("afogado descansa quando alguém o chama pelo nome e o solta das pedras"; a fita, ela
# entrega): o Diário só mostra a lista depois da conversa, atribuída a ela, e a descida ao fundo só fala do que falta a
# quem já sabe. Cada coisa: o que é, onde (só quando o personagem já viu o lugar; senão None) e se já está feita.
REQUISITOS_DESCANSO = [
    ("Chamá-la pelo nome, sabendo o que fizeram com ela", lambda m: None,
     lambda m: {"ilse", "verdade_de_ilse"} <= set(m["pistas"])),
    ("Devolver a fita que ela deu a Berta", lambda m: None, lambda m: "fita" in m["preparos"]),
    ("Soltá-la das pedras de moinho", lambda m: "as correntes do sarilho, no ossuário" if "correntes" in m["pistas"]
     else None, lambda m: "corpo_solto" in m["preparos"]),
]


def descanso(m):
    """Os requisitos do rito, como a tela e o texto mostram: [(o quê, onde, feito)]."""
    return [(o_que, onde(m), bool(feito(m))) for o_que, onde, feito in REQUISITOS_DESCANSO]


def descanso_pronto(m):
    return all(feito for _, _, feito in descanso(m))


def registro(g, mid):
    return (g.mundo.get("missoes") or {}).get(mid) if g.mundo else None


def avancar(g, mid, de, para):
    """Passa a missão de uma etapa à seguinte. Só avança se ela estiver em `de` (repetir não anda duas vezes)."""
    m = registro(g, mid)
    if not m or m["etapa"] != de or para not in MISSOES[mid]["etapas"]:
        return False
    m["etapa"] = para
    from .telemetria import registrar
    registrar(g, "missao", missao=mid, etapa=para)
    return True


def _lugar(g, chave):
    return next((l for l in g.mundo["locais"] if l.get("chave") == chave), None)


def heranca_pendente(m):
    return m.get("desfecho") == "descansada" and "heranca" not in m["cenas"]


def cartoes(g, todas=False):
    """As missões como o rastreador e o mapa mostram (só as ativas) e como o Diário mostra (`todas`: as concluídas
    também, com o desfecho, as linhas do que mudou e o que ainda espera): nome, objetivo da etapa, lugar e pistas.
    Uma missão numa etapa sem objetivo (ainda não apresentada) não aparece. Cada missão pode declarar `requisitos`
    (o que um caminho pede, com o que falta), `linhas` (o que a conclusão mudou) e `pendente` (o que ainda espera)."""
    from .mundo import distancias
    saida = []
    for mid, m in (g.mundo.get("missoes") or {}).items():
        if m.get("concluida") and not todas:
            continue
        d = MISSOES[mid]
        etapa = d["etapas"][m["etapa"]]
        if not etapa["objetivo"]:
            continue
        obj = objetivo(g, mid, m["etapa"])
        loc = _lugar(g, etapa["lugar"])
        dist = distancias(g.mundo["locais"], g.loc["id"]).get(loc["id"]) if loc else None
        saida.append({"id": mid, "nome": d["nome"], "etapa": m["etapa"], "objetivo": obj,
                      "lugar": loc and loc["nome"], "lugar_id": loc and loc["id"], "lugar_tipo": loc and loc["tipo"],
                      "bioma": loc and loc["bioma"], "distancia": dist,
                      "pistas": [d["pistas"][p] for p in m["pistas"]],
                      "preparos": [d["preparos"][p] for p in m.get("preparos", [])],
                      "desfecho": m.get("desfecho"),
                      "requisitos": None if m.get("concluida") else d.get("requisitos", lambda g, m: None)(g, m),
                      "aguardando": None if m.get("concluida") else d.get("aguardando", lambda g, m: None)(g, m),
                      "perguntas": d.get("perguntas", lambda g, m: [])(g, m),
                      **_historia(g, mid, m),
                      "concluida": m.get("concluida"),
                      # Concluída, o resumo já diz o desfecho: "Mais recente" o repetiria (o histórico continua)
                      **({"recente": None} if m.get("concluida") else {}),
                      **({"conclusao": f"Concluída no dia {m['concluida']}. " + d["conclusoes"][m["desfecho"]],
                          "linhas": [x for x in d.get("linhas", lambda g, m: [])(g, m) if x],
                          "pendente": d.get("pendente", lambda g, m: None)(g, m)}
                         if m.get("concluida") else {})})
    return saida


def _texto(mid, chave):
    d = MISSOES[mid]
    return d["pistas"].get(chave) or d["preparos"].get(chave, chave)


def objetivo(g, mid, etapa):
    """O objetivo de uma etapa, como a tela mostra agora. Pode ser um texto ou uma função do jogo (o que o personagem
    sabe muda o texto: a Vigília não diz o nome de quem Caspar acusa antes de o herói conhecê-la)."""
    o = MISSOES[mid]["etapas"][etapa]["objetivo"]
    return o(g) if callable(o) else o


def _historia(g, mid, m):
    """O mais recente e o histórico da investigação, como o Diário mostra. Com datas só o que o histórico registrou
    (desta versão em diante); o que um save de antes já sabia aparece sem data, na ordem em que foi descoberto."""
    d = MISSOES[mid]
    entradas = m.get("historico", [])
    registrado = {c for e in entradas for c in e["pistas"] + e["preparos"]}
    antigos = [c for c in m["pistas"] + m.get("preparos", []) if c not in registrado]
    historico = ([{"dia": None, "itens": [_texto(mid, c) for c in antigos]}] if antigos else [])
    for e in entradas:
        itens = [_texto(mid, c) for c in e["pistas"] + e["preparos"]]
        if e.get("desfecho"):
            itens.append(d["conclusoes"][e["desfecho"]])
        if e.get("etapa") and d["etapas"][e["etapa"]]["objetivo"] and not e.get("concluida"):
            itens.append("Objetivo: " + objetivo(g, mid, e["etapa"]))
        if e.get("inicio"):
            itens.insert(0, "A missão começou.")
        if itens and historico and historico[-1]["dia"] == e["dia"]:  # o mesmo dia fica junto
            historico[-1]["itens"] += itens
        elif itens:
            historico.append({"dia": e["dia"], "itens": itens})
    recente = None
    for e in reversed(historico):  # a última descoberta ou o último feito (um objetivo novo sozinho não conta)
        achados = [i for i in e["itens"] if not i.startswith("Objetivo: ") and i != "A missão começou."]
        if achados:
            recente = {"dia": e["dia"], "texto": achados[-1]}
            break
    return {"recente": recente, "historico": historico}


def sabe_do_rito(m):
    """O personagem sabe como dar descanso a Ilse: Vó Berta contou (saves de antes incluídos: a pista é a mesma)."""
    return "nome_e_fita" in m["pistas"]


def _requisitos_descanso(g, m):
    """O rito, como Vó Berta o contou: só depois da conversa com ela, e só enquanto a guardiã não foi resolvida."""
    if not sabe_do_rito(m) or m.get("desfecho"):
        return None
    return {"titulo": "Vó Berta contou que um afogado descansa quando alguém o chama pelo nome e o solta das pedras:",
            "itens": [{"texto": o_que, "onde": onde, "feito": feito} for o_que, onde, feito in descanso(m)]}


def _perguntas_febre(g, m):
    """O que o personagem ainda se pergunta, a partir do que já viu (nada de pista nova nem de receita)."""
    if m.get("concluida"):
        return []
    p, feito = set(m["pistas"]), set(m.get("preparos", []))
    return [q for q, vale in (
        ("O livro diz que a vila afogou Ilse. Alguém no Vau ainda se lembra daquela noite?",
         "ilse" in p and "verdade_de_ilse" not in p),
        ("O que as correntes prendem às pedras de moinho, lá no fundo?",
         "correntes" in p and not m.get("desfecho") and "corpo_solto" not in feito and not sabe_do_rito(m)),
        ("Quem são os homens com a marca no pulso, e o que procuravam na sacristia?",
         "marcados" in p and "relato_de_ilse" not in p),
    ) if vale]


def _linhas_febre(g, m):
    from . import consequencias
    return [consequencias.fonte_no_diario(g)]


def _pendente_febre(g, m):
    return "Vó Berta ainda espera você na taverna." if heranca_pendente(m) else None


CONCLUSAO = {
    "descansada": "Ilse descansou: com o nome e a fita, largou o Sigilo do Turvo e afundou em paz.",
    "destruida": "Ilse foi destruída, e o Sigilo do Turvo ficou no fundo da capela até você o pegar.",
}
MISSOES["febre_do_turvo"].update(conclusoes=CONCLUSAO, requisitos=_requisitos_descanso, linhas=_linhas_febre,
                                 pendente=_pendente_febre, perguntas=_perguntas_febre)


# ------------------------------------------------------------------ cenas e ações

def _abertura(g, mid):
    g.ui.cena(MISSOES[mid]["nome"], g.contexto_cena(), "evento")
    g.narrar("No Vau do Turvo há tosse atrás de quase toda porta. A febre começou há poucos meses: primeiro as crianças "
             "e os velhos, depois quem cuidava deles. Unhas escuras, sono pesado, sonhos com água.")
    g.narrar("O poço da praça secou no ano passado, quando o riacho baixou. Na mesma época, uma fonte nova brotou logo "
             "abaixo das últimas casas, e a vila a recebeu como bênção e passou a beber dela.")
    g.narrar("\"Desde que a fonte apareceu\", diz uma mulher enchendo dois baldes, sem levantar os olhos, \"ninguém aqui "
             "dorme direito.\"")
    g.narrar("Marta, a curandeira, também está de cama. Anos atrás, foi ela quem tirou você de uma febre de estrada, "
             "numa cama da casa dela, sem cobrar nada. Agora é Pita, a aprendiz dela, quem atende na cabana.")


# A hora do dia na prosa, pelo período de agora (dados.PERIODOS: Manhã, Tarde, Anoitecer, Noite).
_HORA = ("a manhã", "a tarde", "o anoitecer", "a noite")


def _pista(m, pid):
    if pid not in m["pistas"]:
        m["pistas"].append(pid)


def _examinar_fonte(g, mid):
    m = registro(g, mid)
    g.ui.cena("A fonte nova", g.contexto_cena(), "evento")
    g.narrar("A fonte nova brota entre pedras soltas, num buraco que ninguém cavou. A água é clara à primeira vista e "
             f"fria demais para {_HORA[min(g.periodo, 3)]}.")
    g.narrar({
        "guerreiro": "Você afasta as pedras maiores com as mãos. Por baixo, a terra está mole e afundada numa linha "
                     "reta, como se a água tivesse aberto caminho à força, vinda do leste.",
        "arqueiro": "Você se agacha e segue o fio de água com os olhos, como se segue um rastro. Ele não sobe do chão: "
                    "corre por baixo da terra, vindo do leste, do lado do moinho.",
        "mago": "Você põe a mão na água e sente magia nela, fraca e de um tipo que você não reconhece. Ela não nasce "
                "aqui: chega com a água, do leste.",
    }.get(g.j.classe, "A água não sobe do chão: chega por baixo da terra, vinda do leste."))
    g.narrar("No fundo da bacia, quando a água assenta, fica um lodo escuro e fino. Nascente não deixa isso. Água que "
             "passou por algum lugar parado, sim.")
    _pista(m, "agua_do_leste")
    avancar(g, mid, "fonte", "canal")


def _seguir_canal(g, mid):
    m = registro(g, mid)
    g.ui.cena("O Canal do Moinho", g.contexto_cena(), "evento")
    g.narrar("Você procura o riacho entre as árvores e o segue até o moinho. Acima da roda, uma represa nova de "
             "troncos e pedra segura a água num lago raso. O leito velho, o que descia para o Vau, é um fio entre "
             "pedras secas.")
    g.narrar("Do lado da represa sai um canal recém-cavado, reto como uma régua. Uma comporta de tábuas manda a "
             "água para ele, e ele segue para leste, atravessando o bosque rumo ao pântano.")
    g.narrar({
        "guerreiro": "Você desce ao leito velho e chuta as pedras secas. A marca da água ainda está nelas, um palmo "
                     "acima: o riacho que enchia o poço da vila agora passa quase todo pelo canal.",
        "arqueiro": "Você anda ao lado do canal até onde as árvores rareiam. Nenhum bicho bebe dele: as pegadas na lama "
                    "chegam até a beira e voltam.",
        "mago": "Perto da represa, a água é só água. Rumo ao pântano, você volta a sentir nela a magia da fonte nova, "
                "mais forte a cada passo.",
    }.get(g.j.classe, "Rumo ao pântano, a água do canal fica mais escura e mais fria."))
    g.narrar("Você segue o canal até onde o bosque acaba. Adiante, meio engolida pelo pântano, há uma capela de pedra "
             "com o telhado afundado, e o canal entra por um buraco no muro dela. Do outro lado, a terra encharcada "
             "desce na direção da vila, como o fio que você viu na fonte nova.")
    if g.j.classe == "mago":
        g.narrar("Junto ao muro da capela, essa magia é a mais forte do caminho, e vem lá de dentro.")
    _pista(m, "represa")
    _pista(m, "canal_da_capela")
    avancar(g, mid, "canal", "capela")


def _capela_exterior(g, mid):
    _por_na_sala(g, "exterior")
    g.ui.cena("A Capela Afogada", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_exterior(g, mid))
    g.narrar("A capela está afundada até a metade das janelas. Juncos crescem no que foi o pátio da frente, e a porta "
             "sumiu sob a lama. O sino não está mais na torre.")
    g.narrar("O canal que você seguiu desde o moinho termina aqui: a água entra por um buraco no muro e desaparece "
             "no escuro lá dentro, sem barulho. Do buraco vem um frio que não é do pântano.")
    g.narrar("Na beira da água, os sapos estão quietos. Alguns têm patas a mais.")


# ------------------------------------------------------------------ o interior da capela
# Cada sala: o texto de chegada, a luta (criaturas que já existem, geradas no nível do lugar) e, só com vitória, o que
# se acha e a etapa seguinte. Fuga ou derrota não contam: a sala continua por vencer, e a próxima luta é outra. A
# capela é ruína, sempre escura: cada sala pede uma tocha (sem ela, o escuro pesa como em qualquer lugar).

def _lutar(g, grupo, titulo):
    """A luta da sala. Devolve True só com vitória (a derrota sai daqui como sempre, para o resgate ou o fim)."""
    from . import sobrevivencia
    luz = sobrevivencia.acender_tocha(g, sala=True)
    g.luz_na_sala = "tocha" if luz else None  # a tela gráfica desenha a tocha acesa na cena que vem logo depois
    try:
        r = g.combate(grupo, emboscada=None if luz else "inimigo", titulo=titulo)
    finally:
        g.sem_luz = False
    g.fechar_espolio()
    return r == "vitoria"


# Quem prepara golpe na capela (E5): um dos dois esqueletos do ossuário e um dos dois afogados do sarilho são a mesma
# criatura da espécie, com o Golpe Esmagador que o troll e o mercenário já têm (inimigos.py: `esmagar`): avisa um turno
# antes, atordoar interrompe, guarda, barreira e esquiva reduzem ou evitam. A ficha da luta diz isso (`nota`). Só
# aqui: os esqueletos e afogados do resto do jogo continuam como são.
GOLPE_PREPARADO = ("Prepara um golpe esmagador (×2,2): avisa um turno antes. Atordoar interrompe; guarda, barreira e "
                   "esquiva reduzem ou evitam.")


def _que_prepara(e, nome):
    """A variante da capela: o nome dela no lugar do da espécie (o afixo, se houver, continua) e o golpe preparado."""
    from .dados import FAMILIAS
    especie = FAMILIAS[e.familia]["nome"]
    e.nome = e.nome.replace(tx.maiuscula(especie), nome, 1)
    e.desc = e.desc.replace(especie, nome.lower(), 1)
    e.habilidades = e.habilidades + ["esmagar"]
    e.abre_com = "esmagar"  # a primeira ação dela, quando dá (combate/turnos.py); depois, o sorteio de sempre
    e.nota = GOLPE_PREPARADO
    return e


def grupo_ossuario(g):
    """Os dois esqueletos do ossuário; o primeiro é o de guarda (sorteio igual ao de g.grupo)."""
    grupo = g.grupo("esqueleto", n=2)
    _que_prepara(grupo[0], "Esqueleto de Guarda")
    return grupo


def grupo_sarilho(g):
    """Os dois afogados que o barulho do sarilho chama; o primeiro é o inchado."""
    grupo = g.grupo("afogado", n=2)
    _que_prepara(grupo[0], "Afogado Inchado")
    return grupo


def _recuo(g, titulo, texto, fora=False, sacristia=False):
    """Fuga da sala: a sala continua por vencer. `fora`: o texto termina do lado de fora, pela brecha (a tela mostra o
    exterior). `sacristia`: termina subindo pelo alçapão (o ossuário e o sarilho)."""
    g.ui.cena(titulo, g.contexto_cena(), "evento")
    if fora:
        _por_na_sala(g, "exterior")
        g.ui.painel("cena", cena_exterior(g))
    elif sacristia:
        _por_na_sala(g, "sacristia")
        g.ui.painel("cena", cena_sacristia(g, luz=getattr(g, "luz_na_sala", None)))
    g.narrar(texto)
    g.dizer("A sala continua por vencer. Dá para voltar quando quiser.", "cinza")


def _nave(g, mid):
    m = registro(g, mid)
    g.ui.cena("O Salão Alagado", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_salao(g, mid, agua="inquieta"))
    g.narrar("Você entra pelo buraco no muro, com a água do canal pelos joelhos. Lá dentro, o salão principal da capela "
             "é um lago escuro entre colunas. A água corre devagar entre os bancos podres e some numa fenda do piso, perto do altar.")
    g.narrar("Alguma coisa se mexe entre os bancos. Corpos inchados se levantam da água, e o fundo se enche de "
             "sanguessugas.")
    if not _lutar(g, g.grupo("afogado", n=1) + g.grupo("sanguessuga", n=2), "O Salão Alagado"):
        _recuo(g, "O Salão Alagado", "Você recua pela brecha, de volta ao pântano. Lá dentro, a água se fecha de novo.",
               fora=True)
        return
    _por_na_sala(g, "salao")
    g.ui.cena("O Salão Alagado", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_salao(g, mid, agua="quieta"))
    g.narrar("Com a água quieta, dá para ver o caminho dela. Entra pelo muro rompido, atravessa o salão, desce pela "
             "fenda do piso e, mais adiante, sai por baixo do muro dos fundos, rumo à vila.")
    g.narrar("Na entrada, ela é clara. Na saída, deixa nas pedras o mesmo lodo escuro da fonte nova. A vila bebe "
             "o que passa por baixo desta capela.")
    g.narrar("Atrás do altar, uma porta baixa leva à sacristia.")
    _pista(m, "agua_da_capela")
    g.avancar_periodo()
    avancar(g, mid, "capela", "sacristia")


def _sacristia(g, mid):
    m = registro(g, mid)
    g.ui.cena("A Sacristia", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_sacristia(g, mid, "entrada"))
    g.narrar("A sacristia ficou acima da água: um degrau a mais salvou o chão. Há gente aqui. Dois homens de capa "
             "escura reviram as prateleiras à luz de uma lanterna. Os dois têm a mesma marca queimada no pulso.")
    g.narrar("Um deles ergue a lanterna para o seu rosto. \"Não é ela\", diz. O outro já está com a faca na mão.")
    g.ui.painel("cena", cena_sacristia(g, mid, "luta"))  # na luta, os dois são as cartas: a arte fica sem eles
    if not _lutar(g, g.grupo("cultista", n=2), "A Sacristia"):
        _recuo(g, "A Sacristia", "Você volta pelo salão alagado até a brecha. Atrás de você, a lanterna se apaga.",
               fora=True)
        return
    _por_na_sala(g, "sacristia")
    g.ui.cena("A Sacristia", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_sacristia(g, mid, "vitoria", luz=g.luz_na_sala))
    g.narrar({
        "guerreiro": "As botas deles ainda pingam. Não vieram pela brecha: há uma escada de mão encostada na janela "
                     "alta.",
        "arqueiro": "Na lama da janela alta há pegadas de mais gente do que os dois que caíram. Os outros saíram antes "
                    "de você chegar.",
        "mago": "A marca no pulso deles não é tinta. Foi queimada, e ainda tem um cheiro que não é de fogo.",
    }.get(g.j.classe, "Não vieram pela brecha: há uma escada de mão encostada na janela alta."))
    g.narrar("O que eles procuravam ficou num buraco da parede, embrulhado num couro duro: o livro da capela. As "
             "primeiras páginas são de um padre de letra miúda. Ele anota a chegada de Ilse, \"guardiã desta casa\", "
             "no ano em que a Fenda foi fechada, e o que a Igreja deixou com ela: \"o Sigilo do Turvo, que não deve "
             "sair desta capela nem ir para mão nenhuma\".")
    g.narrar("Anos depois, a letra treme. A vila acusa Ilse de bruxaria: a febre daquele inverno, os sonhos com água, o "
             "gado morto no pântano. O padre escreve que ela não fez nada disso, que só guardava. Na linha seguinte: "
             "\"Entregue à água pela vontade da vila. O Sigilo foi com ela. Que Deus nos perdoe.\"")
    for pid in ("ilse", "sigilo_do_turvo", "marcados"):
        _pista(m, pid)
    g.narrar("Embaixo de um pano, num canto, há um baú pequeno de ferro, trancado. No chão, um alçapão desce para o "
             "ossuário, a sala dos ossos.")
    g.dar("bau")
    g.avancar_periodo()
    avancar(g, mid, "sacristia", "ossuario")


def _ossuario(g, mid):
    m = registro(g, mid)
    g.ui.cena("O Ossuário", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_ossuario(g, mid))  # a sala da luta (os pontos só valem na página do lugar)
    g.narrar("O alçapão dá numa escada de pedra que desce para o frio. O ossuário é uma sala baixa, com ossos "
             "arrumados em buracos nas paredes. Alguns buracos estão vazios. Os ossos que faltam estão de pé, no meio da sala.")
    if not _lutar(g, grupo_ossuario(g), "O Ossuário"):
        _recuo(g, "O Ossuário", "Você sobe a escada de costas e fecha o alçapão. Embaixo, os ossos voltam a se arrumar.",
               sacristia=True)
        return
    _por_na_sala(g, "ossuario")
    g.ui.cena("O Ossuário", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_ossuario(g, mid))  # vencida a sala: o sarilho que o texto vai descrever
    g.narrar("No fundo da sala há um sarilho: um eixo de madeira preta, grosso como um tronco, com correntes "
             "enroladas nele, como num poço. "
             "Elas descem por um buraco no chão até a água parada lá embaixo, e estão esticadas: alguma coisa pesada "
             "as segura no fundo.")
    g.narrar("Com a tocha no buraco, aparece a borda de duas pedras velhas de moinho, presas às correntes. Quem fez "
             "isto quis que nada saísse dali. Do buraco sobe o mesmo frio da entrada da capela, e a água lá embaixo não devolve a luz.")
    _pista(m, "correntes")
    if g.j.classe == "guerreiro" and not g.flag(MARCA_BROQUEL):
        g.narrar("No braço do esqueleto de guarda ficou um broquel de ferro escuro, ainda preso pela correia.")
        dar_broquel(g)
    g.avancar_periodo()
    avancar(g, mid, "ossuario", "fundo")


# O Broquel do Vigia (E7, roadmapIDEIAS/16): o escudo do esqueleto de guarda, para o Guerreiro, uma vez. A marca é
# gravada quando o cartão aparece (guardado, vestido ou deixado para trás): não volta por nenhum caminho. Num save de
# antes da 1.63.0 com o ossuário já vencido, o ferreiro do Vau o oferece uma vez (`broquel_no_ferreiro`).
MARCA_BROQUEL = "e7:broquel_do_vigia"


def dar_broquel(g):
    from .itens import UNICOS_POR_ID, fazer_unico
    g.marcar(MARCA_BROQUEL, True)
    nivel = min(g.nivel_guardiao(_lugar(g, "capela_afogada")), g.j.nivel + 2)  # o do vigia, como a Pele do Penitente
    g.oferecer_equip(fazer_unico(UNICOS_POR_ID["broquel_do_vigia"], nivel))


def broquel_no_ferreiro(g):
    """O save de Guerreiro que já venceu o ossuário e ainda não viu o broquel (pelo estado da missão e pela marca)."""
    if not g.campanha or g.j.classe != "guerreiro" or g.flag(MARCA_BROQUEL) or g.loc.get("chave") != "vau_do_turvo":
        return False
    m = registro(g, "febre_do_turvo")
    return bool(m) and (m["etapa"] in ("fundo", "retorno") or bool(m.get("desfecho")))


def broquel_do_ferreiro(g):
    if not broquel_no_ferreiro(g):
        return
    g.ui.cena("A forja", g.contexto_cena(), "evento")
    g.narrar("O ferreiro aponta com o queixo para um broquel de ferro escuro em cima da bancada. \"Trouxeram da capela, "
             "do ossuário. Ainda tinha um braço de esqueleto preso na correia. É coisa de quem luta, não de quem forja.\"")
    dar_broquel(g)


# Soltar o corpo (o passo D2 do Dar descanso, 11-E1-REGIAO-INICIAL.md seção 6): o caminho geral serve a qualquer
# classe (demora, faz barulho e chama afogados: uma luta a mais); cada classe tem um atalho por teste, que poupa a luta
# quando dá certo. Se o atalho falha, o barulho chama os afogados do mesmo jeito e o resto é o caminho geral.
ATALHOS_CORRENTES = {
    "guerreiro": ("forca", "Você agarra a trava enferrujada e puxa até o ferro ceder. O eixo gira sozinho, rápido, e a "
                           "corrente desce para o fundo antes que o barulho chame alguém."),
    "mago": ("arcano", "Você fala baixo com o ferro da trava, e a ferrugem anda por ele como água em pano. A trava se "
                       "desfaz na sua mão, e a corrente desce sem um som."),
    "arqueiro": ("destreza", "Do pé da escada, você mira o pino que segura a trava. A flecha o arranca limpo, e a "
                             "corrente corre para o fundo antes de o eco voltar."),
}
CD_CORRENTES = 13


# ------------------------------------------------------------------ a capela por dentro (1.79.0, roadmapIDEIAS/20)
# Onde o personagem está na capela, separado do passo da missão. A sequência é a do jogo: exterior ↔ salão alagado ↔
# sacristia ↔ ossuário ↔ fundo. Entrar numa sala ainda por vencer é a ação da missão (a luta e o texto de sempre, com a
# tocha); passar por uma sala já vencida só troca a vista: sem luta, tempo, tocha, texto, cura nem recompensa. Quem
# chega viajando ou sai (viagem, resgate, explorar, acampar) fica do lado de fora.
SALAS = ("exterior", "salao", "sacristia", "ossuario", "fundo")
NOME_SALA = {"exterior": "Do lado de fora", "salao": "Salão alagado", "sacristia": "Sacristia", "ossuario": "Ossuário",
             "fundo": "Fundo alagado"}
# As passagens entre salas vizinhas, com o rótulo do menu. Nenhum atalho: cada sala só leva às do lado.
PASSAGENS = {
    ("exterior", "salao"): "Entrar no salão pelo buraco do muro",
    ("salao", "exterior"): "Sair pela brecha do muro",
    ("salao", "sacristia"): "Ir à sacristia",
    ("sacristia", "salao"): "Voltar ao salão alagado",
    ("sacristia", "ossuario"): "Descer ao ossuário pelo alçapão",
    ("ossuario", "sacristia"): "Subir à sacristia",
    ("ossuario", "fundo"): "Descer ao fundo alagado",
    ("fundo", "ossuario"): "Subir ao ossuário",
}
# Saves de antes da 1.79.0 não guardam a sala: a posição vem do passo da missão (a última sala vencida), sem refazer
# nada nem voltar ao começo.
SALA_DA_ETAPA = {"sacristia": "salao", "ossuario": "sacristia", "fundo": "ossuario"}


def na_capela(g):
    return bool(g.campanha) and g.loc.get("chave") == "capela_afogada" and registro(g, "febre_do_turvo") is not None


def sala_atual(g):
    """A sala da capela em que o personagem está (None fora dela)."""
    if not na_capela(g):
        return None
    m = registro(g, "febre_do_turvo")
    return m["sala"] if m.get("sala") in SALAS else SALA_DA_ETAPA.get(m["etapa"], "exterior")


def _vencida(g, sala):
    """A sala já foi vencida (passar por ela não tem luta). O exterior não tem o que vencer; o fundo, depois da guardiã."""
    m = registro(g, "febre_do_turvo")
    i = ETAPAS_FEBRE.index(m["etapa"])
    return {"exterior": True, "salao": i > ETAPAS_FEBRE.index("capela"), "sacristia": i > ETAPAS_FEBRE.index("sacristia"),
            "ossuario": i > ETAPAS_FEBRE.index("ossuario"), "fundo": bool(m.get("desfecho"))}[sala]


def _por_na_sala(g, sala):
    m = registro(g, "febre_do_turvo")
    if m is not None:
        m["sala"] = sala


def pode_explorar(g):
    """Explorar a região é lá fora: dentro da capela (salão, sacristia, ossuário, fundo), a ação não existe. Para
    explorar, sai-se antes pelas passagens; não há "sair e explorar"."""
    return sala_atual(g) in (None, "exterior")


def saiu_da_capela(g):
    """Viagem, resgate, explorar ou acampar: na próxima vez, o personagem está do lado de fora."""
    _por_na_sala(g, "exterior")


# O caminho de volta de cada sala até a brecha do muro (as passagens ao contrário), para a saída antes de acampar.
CAMINHO_PARA_FORA = {
    "salao": "",
    "sacristia": ", atravessa o salão alagado",
    "ossuario": ": sobe pelo alçapão, atravessa o salão alagado",
    "fundo": ": sobe ao ossuário, passa pelo alçapão, atravessa o salão alagado",
}


def sair_para_acampar(g, exausto=False):
    """A saída da capela antes do acampamento: a mesma para "Sair e acampar" e para a exaustão. Só o deslocamento,
    pelo caminho já aberto (sem tempo, tocha, luta, teste nem sorteio); a fogueira é lá fora, perto da capela, e o
    amanhecer também. Na tela gráfica, a arte do topo passa ao exterior junto com a faixa que conta a saída. Do lado
    de fora (ou longe da capela), não há o que sair: devolve False e o acampamento segue como sempre."""
    sala = sala_atual(g)
    if sala in (None, "exterior"):
        return False
    corpo = (f"volta pelo caminho já aberto{CAMINHO_PARA_FORA[sala]} e sai pela brecha do muro para "
             f"{'descansar' if exausto else 'acampar'}, perto da capela.")
    _por_na_sala(g, "exterior")
    if g.ui.conquistas_na_tela:
        g.ui.painel("cena", cena_exterior(g))
        g.ui.celebrar("retirada", {"texto": (corpo[0].upper() + corpo[1:]) if exausto else "Você " + corpo,
                                   "exausto": exausto})
    else:
        g.dizer(("Você está exausto. " + corpo[0].upper() + corpo[1:]) if exausto else "Você " + corpo, "cinza")
    return True


def passagens(g):
    """As passagens que valem agora, como opções do menu do lugar (a mesma escolha que os pontos da cena fazem)."""
    s = sala_atual(g)
    if s is None or g.combate_ativo is not None or g.na_estrada:
        return []
    return [(rotulo, ("capela", para), {"capela_ir": para}) for (de, para), rotulo in PASSAGENS.items()
            if de == s and _vencida(g, para)]


def ir_na_capela(g, para):
    """Passa para a sala vizinha já vencida. Só a vista muda. Devolve se passou (um clique repetido não faz nada)."""
    if (sala_atual(g), para) not in PASSAGENS or not _vencida(g, para):
        return False
    _por_na_sala(g, para)
    return True


# As cenas interativas da capela (roadmapIDEIAS/20): a tela gráfica desenha o ambiente onde a coisa acontece (o
# exterior, o salão alagado, o ossuário), com pontos clicáveis que fazem as mesmas ações do menu. O motor diz o estado
# (a água do salão inquieta ou quieta, as correntes presas ou soltas) e o que cada ponto faz agora; a tela só desenha.
# Painel da página do lugar (`pagina`): o ambiente do passo da missão, com os pontos ativos quando a ação está no
# menu. Painel dentro de uma cena: o ambiente que o texto descreve, sem ação (a escolha da cena vem pelo menu dela).
# A animação da corrente descendo vem depois de o preparo ser gravado (celebrar "correntes"): mostra, não decide.
ETAPAS_FEBRE = list(MISSOES["febre_do_turvo"]["etapas"])


def _ponto(g, mid, pid, nome, acao_id, estado, pagina):
    """Um ponto da cena: faz a ação `acao_id` do menu (o mesmo rótulo e o mesmo endereço da opção) se ela vale agora e
    o painel é o da página do lugar; senão, só diz o `estado` a quem clica."""
    d = next((d for d in ACOES if d["id"] == acao_id and d["missao"] == mid), None) if acao_id else None
    vale = bool(pagina and d and _vale(g, d))
    return {"id": pid, "nome": nome, "estado": estado,
            "acao": {"missao": mid, "acao_missao": acao_id} if vale else None, "faz": d["rotulo"] if vale else None}


def _passagem(g, mid, pid, nome, para, acao_id, estado, pagina):
    """Um ponto que leva a outra sala: vencida, é a passagem (sem custo); por vencer, a ação da missão que entra nela."""
    if acao_id is None or _vencida(g, para):
        vale = bool(pagina and (sala_atual(g), para) in PASSAGENS and _vencida(g, para) and g.combate_ativo is None)
        rotulo = PASSAGENS.get((sala_atual(g), para))
        return {"id": pid, "nome": nome, "estado": estado, "acao": {"capela_ir": para} if vale else None,
                "faz": rotulo if vale else None}
    return _ponto(g, mid, pid, nome, acao_id, estado, pagina)


# O que se vê de perto num ponto de olhar (o texto curto embaixo da arte enquanto ela está aproximada): só o que a
# arte mostra e a chegada não disse.
OLHAR_SAPOS = "De perto, as patas a mais são finas e tortas, e se mexem junto com as outras."


def cena_exterior(g, mid="febre_do_turvo", pagina=False):
    """A capela vista de fora: afundada, a porta sob a lama, a torre sem sino, o canal entrando pelo buraco do muro e
    os sapos na beira (um ponto só de olhar: aproxima e afasta, sem mexer em nada)."""
    buraco = _passagem(g, mid, "buraco", "Buraco no muro", "salao", "nave",
                       "O buraco no muro, rente à água, por onde o canal entra.", pagina)
    sapos = {"id": "sapos", "nome": "Sapos", "estado": "Sapos quietos na beira da água.", "acao": None,
             "olhar": OLHAR_SAPOS}
    return {"cena": "exterior", "pontos": [buraco, sapos], "titulo": "A Capela Afogada", "pagina": pagina}


def cena_salao(g, mid="febre_do_turvo", agua="quieta", pagina=False):
    """O salão alagado: `agua` "inquieta" (os afogados e as sanguessugas ainda na água, antes da luta) ou "quieta"
    (vencido: dá para ver o caminho da água, do muro rompido até a fenda do piso). Sem o mecanismo das correntes nem
    os ossos: são do ossuário."""
    m = registro(g, mid)
    vencida = m and ETAPAS_FEBRE.index(m["etapa"]) > ETAPAS_FEBRE.index("capela")
    porta = _passagem(g, mid, "porta", "Sacristia", "sacristia", "sacristia",
                      "A porta baixa atrás do altar, que leva à sacristia." if vencida else "Uma porta baixa, atrás do altar.",
                      pagina)
    brecha = _passagem(g, mid, "brecha", "Brecha do muro", "exterior", None,
                       "O buraco no muro por onde o canal entra; dá para o pântano.", pagina)
    return {"cena": "salao", "agua": agua, "pontos": [brecha, porta] if agua == "quieta" else [],
            "titulo": "O Salão Alagado", "pagina": pagina}


def cena_ossuario(g, mid="febre_do_turvo", foco=None, pagina=False):
    m = registro(g, mid)
    soltas = "corpo_solto" in m["preparos"]
    ponto = _ponto(g, mid, "sarilho", "Sarilho", "correntes",
                   "As correntes estão soltas." if soltas else "As correntes estão presas pela trava.",
                   pagina and not foco)
    pg = pagina and not foco
    escada = _passagem(g, mid, "escada", "Escada do alçapão", "sacristia", None, "A escada sobe até o alçapão da sacristia.",
                       pg)
    descida = _passagem(g, mid, "descida", "Descida ao fundo", "fundo", "fundo",
                        "A escada continua descendo até a água do fundo.", pg)
    return {"cena": "ossuario", "correntes": "soltas" if soltas else "presas", "foco": foco,
            "pontos": [escada, ponto, descida], "titulo": "O Ossuário", "pagina": pg}


# O que se vê de perto na sacristia (pontos de olhar, só na página do lugar): o que a arte mostra, sem repetir o livro.
OLHAR_JANELA = "Uma escada de mão, de madeira, encostada na parede até a janela alta."
OLHAR_LIVRO = "O livro da capela, no couro duro. O que ele conta, você já leu."


def cena_sacristia(g, mid="febre_do_turvo", momento="visita", pagina=False, luz=None):
    """A sacristia, acima da água do salão: a porta para ele (um degrau abaixo), as prateleiras reviradas, a janela alta
    com a escada de mão, o buraco na parede onde estava o livro, o baú embaixo do pano e o alçapão do ossuário.
    `momento`: "entrada" (os dois de capa escura nas prateleiras, a lanterna erguida), "luta" (eles são as cartas: a
    arte fica sem eles, a lanterna no chão, ainda acesa), "vitoria" (a lanterna caída e apagada, o livro fora do
    buraco, o baú ainda embaixo do pano, como o texto conta) ou "visita" (o baú já está na bolsa: o pano no chão e o
    canto vazio). `luz`: "tocha" quando a luta acendeu a de quem está ali; sem ela, a janela (o período lá fora)."""
    visita = momento == "visita"
    pontos = []
    if visita:
        porta = _passagem(g, mid, "porta", "Porta do salão", "salao", None,
                          "A porta que volta ao salão alagado, um degrau abaixo.", pagina)
        alcapao = _passagem(g, mid, "alcapao", "Alçapão", "ossuario", "ossuario", "O alçapão no chão desce ao ossuário.",
                            pagina)
        janela = {"id": "janela", "nome": "Janela", "estado": "A janela alta, com uma escada de mão encostada.",
                  "acao": None, "olhar": OLHAR_JANELA if pagina else None}
        livro = {"id": "livro", "nome": "Livro", "estado": "O livro da capela, embrulhado em couro.", "acao": None,
                 "olhar": OLHAR_LIVRO if pagina else None}
        pontos = [porta, janela, livro, alcapao]
    return {"cena": "sacristia", "momento": momento, "luz": "lanterna" if momento in ("entrada", "luta") else luz,
            "bau": "levado" if visita else "coberto", "livro": "no_buraco" if momento in ("entrada", "luta") else "fora",
            "pontos": pontos, "titulo": "A Sacristia", "pagina": pagina}


def cena_neutra(g, sala, pagina=False):
    """Uma sala que ainda não tem arte própria (o fundo): a tela mostra um fundo neutro, escuro, sem
    objetos nem pontos, em vez de mostrar outra sala no lugar dela. O caminho fica nas opções do menu."""
    return {"cena": "neutra", "sala": sala, "pontos": [], "titulo": {"sacristia": "A Sacristia",
                                                                     "fundo": "O Fundo Alagado"}[sala], "pagina": pagina}


def mostrar_cena(g):
    """Na página da Capela Afogada (só na tela gráfica): a sala onde o personagem está (sala_atual), com os pontos
    que valem agora. O fundo, ainda sem arte própria, num fundo neutro."""
    sala = sala_atual(g)
    if sala is None:
        return
    if sala == "sacristia":
        g.ui.painel("cena", cena_sacristia(g, pagina=True))
    elif sala == "fundo":
        g.ui.painel("cena", cena_neutra(g, sala, pagina=True))
    else:
        g.ui.painel("cena", {"exterior": cena_exterior, "salao": cena_salao, "ossuario": cena_ossuario}[sala](
            g, pagina=True))


def _soltar(g, mid):
    """O fim comum: a corrente desce frouxa e o preparo fica registrado. Só depois disso a tela mostra a corrente
    descendo (e, recarregada, já desenha as correntes soltas)."""
    m = registro(g, mid)
    if "corpo_solto" not in m["preparos"]:
        m["preparos"].append("corpo_solto")
        from .telemetria import registrar
        registrar(g, "missao", missao=mid, preparo="corpo_solto")
    if g.ui.conquistas_na_tela:
        g.ui.celebrar("correntes", {"cena": "ossuario"})
    g.narrar("Lá embaixo, a água se mexe uma vez e para: o que estava preso às pedras de moinho está solto.")


def _onda_de_afogados(g, mid):
    """O barulho do sarilho desce pela água e chama os afogados. Só a vitória deixa terminar o trabalho."""
    g.narrar("Da escada vem o som de água se mexendo. Os afogados vieram atrás do barulho.")
    if not _lutar(g, grupo_sarilho(g), "O Sarilho"):
        _recuo(g, "O Sarilho", "Você sobe pelo alçapão e deixa o sarilho como estava. As correntes continuam presas.",
               sacristia=True)
        return
    g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_ossuario(g, mid, foco="sarilho"))
    g.narrar("Com a sala quieta de novo, você termina o trabalho. A última volta da corrente escorrega do eixo e desce, "
             "frouxa, para o fundo.")
    g.avancar_periodo()
    _soltar(g, mid)


def _correntes_a_mao(g, mid, cena=True):
    if cena:
        g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
        g.ui.painel("cena", cena_ossuario(g, mid, foco="sarilho"))
    g.narrar("Você firma os pés e começa a desenrolar a corrente, elo por elo. O sarilho range como um bicho, e o "
             "barulho desce pelo buraco e corre pela água da capela inteira.")
    _onda_de_afogados(g, mid)


def _correntes_atalho(g, mid, cena=True):
    attr, texto = ATALHOS_CORRENTES[g.j.classe]
    if cena:
        g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
        g.ui.painel("cena", cena_ossuario(g, mid, foco="sarilho"))
    if g.j.classe == "arqueiro":
        g.j.flechas -= 1
    if g.teste(attr, CD_CORRENTES):
        g.narrar(texto)
        _soltar(g, mid)
        return
    g.narrar("Não deu: a trava não cede, e o eixo solta um rangido que desce pelo buraco e corre pela água da capela "
             "inteira. Agora vai ter de ser à mão.")
    _onda_de_afogados(g, mid)


# A forma da classe, como a escolha dentro do sarilho a oferece: a ação (com o teste no fim, que a tela anota com o seu
# bônus) e, embaixo, o custo e o risco, para comparar antes de escolher.
METODO_CLASSE = {
    "guerreiro": "Arrancar a trava (Força)",
    "mago": "Apodrecer o ferro da trava (Arcano)",
    "arqueiro": "Acertar o pino da trava (Destreza)",
}
# As notas dizem o que se percebe antes de agir (o tempo, o barulho, o teste, a flecha), não o que vem depois: quem
# ouve o rangido e o que acontece em seguida, a cena mostra.
RISCO_CLASSE = "Silencioso, se a trava ceder. Se não ceder, o eixo range alto."
NOTA_MAO = "Demorado e barulhento: o eixo range, e o som corre pela água da capela inteira."


def _soltar_correntes(g, mid):
    """Uma ação só no menu da capela: aqui se vê o mecanismo e se escolhe como mexer nele. A ligação com o rito só
    aparece para quem já ouviu Vó Berta. Deixar como está não gasta nada (nem tempo, nem flecha, nem sorteio) e não
    pede Continuar: a função devolve False."""
    m = registro(g, mid)
    g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_ossuario(g, mid, foco="sarilho"))  # a tela gráfica enquadra o mecanismo
    g.narrar("As correntes saem do sarilho, um eixo grosso de madeira no fundo do ossuário, e descem pelo buraco do chão "
             "até as duas pedras de moinho, lá embaixo na água. Uma trava de ferro segura o eixo para ele não girar.")
    if sabe_do_rito(m):
        g.narrar("Vó Berta disse que um afogado descansa quando alguém o chama pelo nome e o solta das pedras.")
    from .sobrevivencia import riscos_sala
    # À mão, o barulho sempre chama os afogados: a luta é na sala, com a tocha e a noite de sempre. Pela classe, a luta
    # só vem se a trava não ceder: a nota não promete custo de luz nem perigo da noite que podem não acontecer.
    riscos = riscos_sala(g)
    opcoes = [("Desenrolar as correntes à mão", "mao", {"nota": NOTA_MAO, **({"riscos": riscos} if riscos else {})})]
    if g.j.classe == "arqueiro" and g.j.flechas <= 0:
        g.dizer("Sem flechas, não dá para acertar o pino da trava: sobra o jeito à mão.", "cinza")
    else:
        nota = ("Gasta 1 flecha. " if g.j.classe == "arqueiro" else "") + RISCO_CLASSE
        opcoes.append((METODO_CLASSE[g.j.classe], "classe", {"nota": nota}))
    opcoes.append(("Deixar como está", None))
    op = g.menu("O que você faz com as correntes?", opcoes)
    if op is None:
        return False
    if op == "mao":
        _correntes_a_mao(g, mid, cena=False)
    else:
        _correntes_atalho(g, mid, cena=False)


# ------------------------------------------------------------------ Vó Berta, a guardiã e o desfecho

def _berta(g, mid):
    """A testemunha: o que a vila fez (conhecimento) e a fita (o que se leva). Uma vez só: a ação some com a fita."""
    m = registro(g, mid)
    g.ui.cena("Vó Berta", g.contexto_cena(), "evento")
    g.narrar("Vó Berta tem o canto mais quente da taverna e a caneca mais vazia. Quando você diz o nome de Ilse, ela "
             "fica muito tempo olhando para a mesa.")
    g.narrar("\"Eu tinha oito anos\", diz por fim. \"Foi no inverno da febre, poucos anos depois que fecharam a Fenda. "
             "A Ilse cuidava da capela e de uma coisa que a Igreja tinha deixado com ela. Ninguém sabia o quê. Bastou "
             "para dizerem que era bruxa.\"")
    g.narrar("\"Não foi um homem só. Foi a vila. Tiraram ela de casa de noite, amarraram em duas pedras velhas de "
             "moinho e desceram tudo para o fundo da capela, com corrente e sarilho. Meu pai segurou a corda. Eu vi da porta da capela, e "
             "ninguém mandou ninguém parar.\"")
    g.narrar("\"Na véspera, ela tinha amarrado esta fita no meu cabelo.\" Berta tira do bolso uma fita desbotada, dobrada "
             "com cuidado. \"Guardei esse tempo todo. Dizem que afogado descansa quando alguém o chama pelo nome e o "
             "solta das pedras. Se ela ainda está lá embaixo, que receba de volta o que é dela: o nome e isto. Ela "
             "nunca quis ser o que virou.\"")
    g.narrar("\"Só lhe peço uma coisa: o nome do meu pai, deixe fora disso.\"")
    for pid in ("verdade_de_ilse", "nome_e_fita"):
        _pista(m, pid)
    if "fita" not in m["preparos"]:
        m["preparos"].append("fita")
        from .telemetria import registrar
        registrar(g, "missao", missao=mid, preparo="fita")
    g.ui.efeito("Fita de Ilse", "item")


def _fundo(g, mid):
    """A descida ao fundo: a guardiã. O que falta para o rito é dito antes; o rito só é oferecido com tudo pronto."""
    from .inimigos import instanciar_guardiao
    m = registro(g, mid)
    _por_na_sala(g, "fundo")  # desceu: está no fundo, com Ilse ainda na água (a luta só começa se for escolhida)
    g.ui.cena("O Fundo da Capela", g.contexto_cena(), "evento")
    g.ui.painel("cena", cena_neutra(g, "fundo"))
    g.narrar("A escada do ossuário termina na água. O fundo é um poço escuro, com água pela cintura e um frio que não é "
             "de água. No meio, entre duas pedras de moinho, há uma forma enrolada em correntes.")
    if "corpo_solto" in m["preparos"]:
        g.narrar("As correntes que você soltou pendem frouxas. A forma já não está presa às pedras.")
    g.narrar("Ela abre os olhos. A pele é azulada, os cabelos são algas, e ela começa a cantar uma canção de ninar. É "
             "Ilse, ou o que a vila fez dela: a Bruxa Afogada.")
    pronto = descanso_pronto(m)
    if not pronto and sabe_do_rito(m):
        # A lembrança do que Berta contou, diante do que se vê. Depois de Berta, só as correntes podem faltar (o nome e
        # a fita vêm da conversa); o resto fica no jeito de antes, por garantia.
        if "corpo_solto" not in m["preparos"]:
            g.narrar("Vó Berta disse que era preciso soltá-la das pedras. As correntes ainda a prendem.")
        else:
            falta = [o_que[0].lower() + o_que[1:] for o_que, _, feito in descanso(m) if not feito]
            g.narrar("Do que Vó Berta contou, ainda falta " + tx.lista_natural(falta) + ".")
    g.narrar("Ela ainda não se levantou da água.")
    from .sobrevivencia import riscos_sala
    while True:
        sem_fuga = {"nota": tx.SEM_FUGA, **({"riscos": riscos_sala(g, guardiao=True)} if riscos_sala(g, guardiao=True) else {})}
        # O lodo de Caspar se recolhe aqui, na água, com Ilse ainda quieta: recolher não começa a luta.
        lodo = next((d for d in ACOES if d["id"] == "lodo" and d["missao"] == _caspar.MID and _vale(g, d)), None)
        opcoes = ([("Chamar Ilse pelo nome e tentar dar descanso", "descanso", sem_fuga)] if pronto else []) + [
            ("Lutar para destruí-la", "destruir", sem_fuga)] + (
            [(lodo["rotulo"], "lodo")] if lodo else []) + [("Voltar por enquanto", None)]
        op = g.menu("O que você faz?", opcoes)
        if op != "lodo":
            break
        lodo["fn"](g, lodo["missao"])
        g.narrar("Ilse continua na água, entre as pedras, cantando baixo. Ela ainda não se levantou.")
    if op is None:
        _por_na_sala(g, "ossuario")
        g.narrar("Você sobe a escada de costas. O canto continua lá embaixo.")
        return
    spec = {"bioma": "pantano", "id": "bruxa_afogada", "idx": 1, "nome": "Ilse, a Bruxa Afogada", "g": "f",
            "base": "Bruxa Afogada"}
    chefe = instanciar_guardiao(spec, g.nivel_guardiao(g.loc))
    chefe.chave = "ilse"
    if op == "descanso":
        # O rito garantido (seção 19 do 11): até o momento do rito, nada a leva abaixo do limiar da fase. O que
        # passaria dele fica retido; o momento vem no primeiro ponto seguro (Combate.checar_limiares).
        chefe.piso = max(1, int(chefe.max_hp * chefe.fases[0]["limiar"]))
        chefe.ao_limiar = lambda cb, e: _momento_do_rito(g, cb, e)
        g.narrar("Você segura a fita e espera o momento de dizer o nome dela.")
    from . import sobrevivencia
    luz = sobrevivencia.acender_tocha(g, sala=True)
    try:
        r = g.combate([chefe], emboscada=None if luz else "inimigo", pode_fugir=False,
                      titulo="Guardiã: Ilse, a Bruxa Afogada")
    finally:
        g.sem_luz = False
    g.fechar_espolio()
    if r == "vitoria":
        _por_na_sala(g, "fundo")
        _resolver(g, mid, "descansada" if getattr(chefe, "descansou", False) else "destruida", chefe.nivel)


def _momento_do_rito(g, cb, e):
    """No limiar: a escolha é do motor; a tela só a mostra. Devolver o nome e a fita encerra a luta em paz (ela e o que
    ela chamou da água afundam). Desistir tira o piso: o dano que ele segurou cai na hora e a luta segue para a
    segunda fase, como em qualquer guardião. Nada do que a build faz se perde para quem escolhe destruir."""
    cb.dizer("O canto de Ilse falha. As correntes soltas pendem dos pulsos dela, e os olhos dela vão para a fita na sua "
             "mão.", "ciano+negrito")
    op = g.menu("Este é o momento do rito.", [("Dizer o nome dela e devolver a fita (dar descanso)", "rito"),
                                              ("Desistir do rito e seguir lutando (destruir)", "lutar")])
    if op == "rito":
        e.piso, e.retido, e.descansou = None, 0, True
        cb.lance("fase", em=cb.uid(e))
        cb.dizer("\"Ilse.\" Ela para de cantar. O que ela chamou da água afunda junto com o canto.", "ciano+negrito")
        for o in cb.inimigos:
            o.hp = 0
        cb.ui.atualizar()
        return
    e.piso = None
    dano, e.retido = e.retido, 0
    cb.dizer("Você guarda a fita. Ilse entende antes de você terminar o gesto, e o canto vira um grito.", "vermelho+negrito")
    if dano:
        e.hp = max(0, e.hp - dano)
        cb.lance("golpe", de=None, em=cb.uid(e), dano=dano, crit=False, elemento="fisico", alcance="corpo",
                 absorvido=0, eficacia=None, rotulo="O rito se desfaz", hp=e.hp, max_hp=e.max_hp)
        cb.dizer(f"Sem o rito, os golpes que ela vinha aguentando chegam de uma vez: {dano} de dano.", "amarelo")
        if not e.vivo:
            cb.ao_morrer(e, por=cb.j)


def _resolver(g, mid, desfecho, nivel):
    """O desfecho único da guardiã: guardado antes de tudo, com o Sigilo e a recompensa de cada caminho, uma vez."""
    from . import itens
    m = registro(g, mid)
    if m.get("desfecho"):
        return
    m["desfecho"], m["dia_desfecho"] = desfecho, g.dia
    _caspar.sincronizar(g)  # a resposta a Caspar passa a ser na praça
    from .telemetria import registrar
    registrar(g, "missao", missao=mid, desfecho=desfecho)
    if desfecho == "descansada":
        g.ui.cena("Ilse", g.contexto_cena(), "evento")
        g.ui.painel("cena", cena_neutra(g, "fundo"))
        g.narrar("Por um momento, ela é só uma mulher cansada com a água pela cintura. Ela pega a fita da sua mão e a "
                 "enrola nos dedos.")
        g.narrar("\"Eu era a guardiã dele\", diz, sem raiva. \"É um de três. Os três seguram fechada uma porta que "
                 "nunca devia ter sido aberta, e agora ela range. Há mãos procurando os três. Não deixe os três cair "
                 "nas mãos de quem não entende o que eles mantêm fechado.\"")
        g.narrar("Ela abre a mão. O Sigilo do Turvo, rachado e frio como pedra de rio, passa para a sua. Depois ela "
                 "afunda devagar, com a fita entre os dedos, e a água do fundo fica parada e clara.")
        _pista(m, "relato_de_ilse")
    else:
        g.ui.cena("A Guardiã Destruída", g.contexto_cena(), "evento")
        g.ui.painel("cena", cena_neutra(g, "fundo"))
        g.narrar("Ilse se desfaz na água escura, e o canto vira bolhas. Por um instante, a água que desce para a vila "
                 "corre mais turva.")
        g.narrar("Onde ela esteve, entre as pedras de moinho, sobra o Sigilo do Turvo, rachado e frio como pedra de rio. Presa às "
                 "pedras, há também uma veste de couro endurecido pela água, que ainda guarda a forma de alguém.")
    g.receber_sigilo("turvo", "Ilse, a Bruxa Afogada")
    if desfecho == "destruida":
        g.oferecer_equip(itens.fazer_unico(itens.UNICOS_POR_ID["pele_do_penitente"], min(nivel, g.j.nivel + 2)))
    g.avancar_periodo()
    avancar(g, mid, "fundo", "retorno")


def _retorno(g, mid):
    """A volta ao Vau depois da guardiã, uma vez: o que a água e a vila mostram agora (depende do desfecho e de quantos
    dias passaram, consequencias.estado_fonte) e a conclusão da missão. Volta cedo ou tarde, a cena conta o de agora."""
    from . import consequencias
    m = registro(g, mid)
    fonte = consequencias.estado_fonte(g)
    g.ui.cena("De Volta ao Vau", g.contexto_cena(), "evento")
    g.narrar("Você entra no Vau com o Sigilo do Turvo no bolso, ainda frio como pedra de rio.")
    g.narrar({
        ("descansada", "limpando"): "Na fonte nova, o lodo assentou no fundo da bacia, e a água que corre por cima já "
                                    "sai mais clara." + (" Ninguém piorou de noite." if consequencias.noites(g) else " Ninguém piorou desde então."),
        ("destruida", "escura"): "A fonte nova corre escura, quase preta: o que estava no corpo de Ilse saiu de uma vez. "
                                 "A vila inteira tosse mais desde que a água escureceu, e ninguém enche balde.",
        ("destruida", "limpando"): "A fonte nova ainda tem a cor de chá fraco, mas clareia. Contam que houve uma noite "
                                   "em que a água correu preta e todos pioraram. O pior passou.",
    }.get((m["desfecho"], fonte), "A fonte nova corre clara, e há fila de baldes de novo na praça."))
    if consequencias.marta_de_pe(g):
        g.narrar("Marta está na porta da casa dela, magra e de pé. \"Você de novo\", diz, e quase sorri. \"Da outra vez "
                 "fui eu que cuidei de você.\" Pita, ao lado, não para de falar.")
    elif fonte == "escura":
        g.narrar("Pita passa correndo com dois baldes de água fervida. \"A Marta piorou quando a água escureceu\", diz, sem "
                 "parar. \"Vai ser uma noite longa.\"")
    else:
        g.narrar("Pita vem te encontrar na praça. \"A Marta ainda está de cama, mas " +
                 ("dormiu a noite inteira, pela primeira vez.\"" if consequencias.noites(g) else
                  "a febre dela parou de subir.\""))
    if m["desfecho"] == "descansada" and heranca_pendente(m):
        g.narrar("Na janela da taverna, Vó Berta ergue a caneca para você.")
    m["concluida"] = g.dia
    from .telemetria import registrar
    registrar(g, "missao", missao=mid, concluida=g.dia)


def _heranca(g, mid):
    """Quem deu descanso a Ilse conta a Berta: a herança da família dela, uma vez (a cena fica marcada antes)."""
    from .itens import gerar_equip
    m = registro(g, mid)
    m["cenas"].append("heranca")
    g.ui.cena("Vó Berta", g.contexto_cena(), "evento")
    g.narrar("Berta escuta tudo sem interromper. Quando você conta da fita entre os dedos de Ilse, ela fecha os olhos.")
    g.narrar("\"Minha mãe guardou isto para quando a vila pagasse o que devia\", diz, e empurra um embrulho pela mesa. "
             "\"Ninguém nunca pagou. Fica com você.\"")
    g.oferecer_equip(gerar_equip(g.rng, g.j.classe, g.j.nivel, raridade="raro"))


# Cada cena toca uma vez, quando a pessoa está no menu daquele lugar, naquela etapa. Cada ação é uma opção do menu do
# lugar, com a mesma condição; executar confere tudo de novo. `confirmar`: o texto termina num Continuar de verdade
# (a tela não vira a página sozinha, por tempo, e o clique que adianta o texto não fecha a cena).
CENAS = [
    dict(missao="febre_do_turvo", id="abertura", lugar="vau_do_turvo", etapas=("fonte",), fn=_abertura,
         confirmar=True),
    dict(missao="febre_do_turvo", id="capela_exterior", lugar="capela_afogada", etapas=("capela",),
         fn=_capela_exterior, confirmar=True),
    dict(missao="febre_do_turvo", id="retorno", lugar="vau_do_turvo", etapas=("retorno",), fn=_retorno,
         confirmar=True),
]
# Uma ação pode pedir também uma classe (`classe`), que um preparo ainda falte (`falta`) e uma condição a mais (`pode`).
# `onde`: na capela, a sala em que o personagem precisa estar (ou uma tupla delas; ver sala_atual).
# `abre`: ela leva a outra escolha, de onde se pode voltar (a tela marca com uma seta; o texto, com "›"). `avanca`: é o
# passo que leva a história adiante; fica por último entre as ações da missão, depois do que se pode examinar antes.
ACOES = [
    dict(missao="febre_do_turvo", id="examinar_fonte", rotulo="Examinar a fonte nova", lugar="vau_do_turvo",
         etapas=("fonte",), fn=_examinar_fonte, confirmar=True),
    dict(missao="febre_do_turvo", id="seguir_canal", rotulo="Seguir a água e examinar o canal",
         lugar="bosque_do_moinho", etapas=("canal",), fn=_seguir_canal, confirmar=True),
    dict(missao="febre_do_turvo", id="nave", rotulo="Entrar na capela pelo buraco do canal", lugar="capela_afogada",
         etapas=("capela",), fn=_nave, confirmar=True, sala=True, onde="exterior"),
    dict(missao="febre_do_turvo", id="sacristia", rotulo="Atravessar o salão alagado",
         lugar="capela_afogada", etapas=("sacristia",), fn=_sacristia, confirmar=True, sala=True, onde="salao"),
    dict(missao="febre_do_turvo", id="ossuario", rotulo="Descer ao ossuário", lugar="capela_afogada",
         etapas=("ossuario",), fn=_ossuario, confirmar=True, sala=True, onde="sacristia"),
    dict(missao="febre_do_turvo", id="correntes", rotulo="Soltar as correntes", abre=True,
         lugar="capela_afogada", etapas=("fundo",), falta="corpo_solto", fn=_soltar_correntes, confirmar=True,
         onde="ossuario"),
    dict(missao="febre_do_turvo", id="fundo", rotulo="Descer ao fundo alagado", abre=True, avanca=True,
         lugar="capela_afogada", etapas=("fundo",), fn=_fundo, confirmar=True, onde="ossuario"),
    # Na taverna do Vau: o cartão no balcão, como os serviços (`meta`). Berta depois da sacristia, uma vez; a herança
    # para quem deu descanso a Ilse, uma vez.
    dict(missao="febre_do_turvo", id="berta", rotulo="Taverna: falar com Vó Berta", lugar="vau_do_turvo",
         etapas=("ossuario", "fundo"), falta="fita", pode=lambda g: "ilse" in registro(g, "febre_do_turvo")["pistas"],
         meta={"predio": "taverna", "servico": "berta", "curto": "Falar com Vó Berta",
               "efeito": "Ela estava lá quando a vila afogou Ilse"}, fn=_berta, confirmar=True),
    dict(missao="febre_do_turvo", id="heranca", rotulo="Taverna: contar a Vó Berta", lugar="vau_do_turvo",
         etapas=("retorno",), pode=lambda g: (registro(g, "febre_do_turvo")["desfecho"] == "descansada"
                                              and "heranca" not in registro(g, "febre_do_turvo")["cenas"]),
         meta={"predio": "taverna", "servico": "berta", "curto": "Contar a Vó Berta",
               "efeito": "Ilse descansou com a fita dela"}, fn=_heranca, confirmar=True),
]


def _retrato(g):
    """O que importa para as novidades, missão a missão, antes de uma ação ou cena."""
    return {mid: (m["etapa"], list(m["pistas"]), list(m.get("preparos", [])), m.get("desfecho"), m.get("concluida"),
                  len(m["cenas"]))
            for mid, m in (g.mundo.get("missoes") or {}).items()}


def titulo(mid, chave):
    """O nome curto de uma pista ou preparo (o cartão e o histórico); sem nome curto, o texto inteiro."""
    d = MISSOES[mid]
    return d.get("titulos", {}).get(chave) or d["pistas"].get(chave) or d["preparos"].get(chave, chave)


def anotar_novidades(g, antes):
    """Depois de uma ação ou cena: o que mudou em cada missão entra no histórico dela, com o dia, e vira um cartão só
    (o que se descobriu ou fez e o objetivo novo), no fim do texto. Só o que acabou de acontecer: carregar um save não
    passa por aqui."""
    cartoes = []
    for mid, m in (g.mundo.get("missoes") or {}).items():
        if mid not in antes:
            continue
        etapa, pistas, preparos, desfecho, concluida, cenas = antes[mid]
        d = MISSOES[mid]
        novas = [p for p in m["pistas"] if p not in pistas]
        feitos = [p for p in m.get("preparos", []) if p not in preparos]
        nova_etapa = m["etapa"] if m["etapa"] != etapa else None
        comecou = not cenas and bool(m["cenas"]) and not pistas and not preparos
        desf = m.get("desfecho") if m.get("desfecho") != desfecho else None
        fim = bool(m.get("concluida")) and not concluida
        if not (novas or feitos or nova_etapa or comecou or desf or fim):
            continue
        entrada = {"dia": g.dia, "pistas": novas, "preparos": feitos}
        entrada.update({k: v for k, v in (("etapa", nova_etapa), ("desfecho", desf)) if v})
        if comecou:
            entrada["inicio"] = True
        if fim:
            entrada["concluida"] = True
        m.setdefault("historico", []).append(entrada)
        if not d["etapas"][m["etapa"]]["objetivo"] and not fim:
            continue  # uma missão ainda não apresentada (Caspar, antes da acusação) não aparece: o histórico guarda
        obj = objetivo(g, mid, m["etapa"]) if (nova_etapa or comecou) and not m.get("concluida") else None
        itens = [titulo(mid, p) for p in novas + feitos] + ([d["conclusoes"][desf]] if desf else [])
        cartoes.append({"missao": mid, "nome": d["nome"], "itens": itens, "objetivo": obj, "nova": comecou,
                        "concluida": fim})
    if cartoes:
        g.ui.missao_atualizada(cartoes)


def _vale(g, d):
    m = registro(g, d["missao"])
    return bool(m and g.campanha == MISSOES[d["missao"]]["campanha"] and g.loc.get("chave") == d["lugar"]
                and m["etapa"] in d["etapas"] and g.combate_ativo is None and not g.na_estrada
                and d.get("classe", g.j.classe) == g.j.classe and d.get("falta") not in m.get("preparos", [])
                and _na_sala(g, d.get("onde")) and d.get("pode", lambda _: True)(g))


def _na_sala(g, onde):
    return onde is None or sala_atual(g) in ((onde,) if isinstance(onde, str) else onde)


def _encerrar(g, d):
    """O fim do texto de uma cena ou ação: o Continuar que ela declara, ou a pausa de sempre."""
    if d.get("confirmar"):
        g.fechar_espolio()
        g.ui.continuar(confirmar=True)
    else:
        g.pausar()


def cena_pendente(g):
    """Toca a cena de missão que vale aqui e agora e ainda não foi vista. Devolve True se tocou uma."""
    if not g.campanha:
        return False
    for d in CENAS:
        if _vale(g, d) and d["id"] not in registro(g, d["missao"])["cenas"]:
            antes = _retrato(g)
            registro(g, d["missao"])["cenas"].append(d["id"])  # antes de tocar: se cair numa luta ou num save, não repete
            d["fn"](g, d["missao"])
            anotar_novidades(g, antes)
            _encerrar(g, d)
            return True
    return False


def opcoes(g):
    """As ações de missão que valem no lugar e na etapa de agora, como opções do menu do lugar."""
    if not g.campanha:
        return []
    validas = sorted((d for d in ACOES if _vale(g, d)), key=lambda d: bool(d.get("avanca")))  # estável: o resto na ordem
    return [(d["rotulo"](g) if callable(d["rotulo"]) else d["rotulo"], ("missao", d["missao"], d["id"]),
             {**d.get("meta", {}), "missao": d["missao"], "acao_missao": d["id"], **({"abre": True} if d.get("abre") else {}),
              **_nota_sala(g, d)})
            for d in validas]


def _nota_sala(g, d):
    """A ação que entra direto na luta de uma sala (`sala`) leva os riscos da tocha e da noite (sobrevivencia)."""
    from .sobrevivencia import riscos_sala
    riscos = riscos_sala(g) if d.get("sala") else []
    return {"riscos": riscos} if riscos else {}


def tem_salas(g):
    """O lugar de agora tem lutas de sala (a capela da campanha): o painel do lugar fala delas no escuro."""
    return bool(g.campanha) and any(d.get("sala") and d["lugar"] == g.loc.get("chave") for d in ACOES)


def executar(g, mid, aid):
    """Faz a ação de missão escolhida, se ela ainda vale (um clique repetido numa ação já feita não faz nada)."""
    for d in ACOES:
        if (d["missao"], d["id"]) == (mid, aid) and _vale(g, d):
            antes = _retrato(g)
            voltou = d["fn"](g, mid) is False  # a escolha dentro da ação (o sarilho) pode voltar sem fazer nada
            anotar_novidades(g, antes)
            if not voltou:
                _encerrar(g, d)
            return True
    return False


# ------------------------------------------------------------------ as outras missões da região
# Cada uma num módulo próprio, com os mesmos dados (MISSOES, CENAS, ACOES) e as mesmas regras de lugar e etapa. A ordem
# conta: as cenas da febre vêm antes (a volta ao Vau toca antes da praça de Caspar).
from . import caspar as _caspar  # noqa: E402

MISSOES.update(_caspar.MISSOES)
CENAS += _caspar.CENAS
ACOES += _caspar.ACOES

# O fim do capítulo vem depois de todas as cenas das missões (capitulo.py).
from . import capitulo as _capitulo  # noqa: E402

CENAS.append(_capitulo.CENA)
