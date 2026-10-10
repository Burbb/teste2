"""Missões da campanha escrita: um registro por missão, com id estável e etapas explícitas.

E3 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md, seção 5): "A Febre do Turvo" começa com uma cena curta no Vau do Turvo; a
investigação segue a água da Fonte Nova até o canal no Bosque do Moinho e o canal até a Capela Afogada. Dentro dela, três
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
"descansada", uma vez só; com ele vêm o Sigilo e a recompensa, e `dia_desfecho` (de onde sai o estado da Fonte Nova).
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
            "fonte": dict(objetivo="Descobrir de onde vem a febre: examinar a Fonte Nova, no Vau do Turvo.",
                          lugar="vau_do_turvo"),
            "canal": dict(objetivo="Seguir a água da Fonte Nova até o canal, no Bosque do Moinho.",
                          lugar="bosque_do_moinho"),
            "capela": dict(objetivo="Investigar a Capela Afogada, onde o canal do moinho entra no brejo.",
                           lugar="capela_afogada"),
            "sacristia": dict(objetivo="Examinar a sacristia da Capela Afogada, atrás do altar.",
                              lugar="capela_afogada"),
            "ossuario": dict(objetivo="Descer ao ossuário da Capela Afogada, embaixo da sacristia.",
                             lugar="capela_afogada"),
            "fundo": dict(objetivo="Descer ao fundo alagado da Capela Afogada, para onde vão as correntes.",
                          lugar="capela_afogada"),
            "retorno": dict(objetivo="Voltar ao Vau do Turvo com o Sigilo.", lugar="vau_do_turvo"),
        },
        pistas={
            "agua_do_leste": "A Fonte Nova não nasce ali: a água chega por baixo da terra, do leste, do lado do Bosque "
                             "do Moinho, e traz um lodo escuro e fino que água de nascente não tem.",
            "represa": "No ano passado, o moleiro represou o riacho acima do moinho e abriu um canal para leste. O "
                       "trecho que descia para a vila minguou: é por isso que o poço da praça secou.",
            "canal_da_capela": "O canal do moinho corre até o brejo e entra por um rombo no muro de uma capela "
                               "afundada, a Capela Afogada. Abaixo dela, a terra está encharcada na direção da vila.",
            "agua_da_capela": "Dentro da capela, a água do canal atravessa a nave, desce por uma fenda do piso e sai "
                              "por baixo do muro dos fundos, rumo à vila. Entra limpa e sai com o lodo escuro: é a "
                              "água da Fonte Nova.",
            "ilse": "A capela tinha uma guardiã, Ilse. A vila a acusou de bruxaria e a afogou; o padre que escreveu o "
                    "livro da sacristia diz que ela não fez nada do que disseram.",
            "sigilo_do_turvo": "Em vida, Ilse tinha a custódia do Sigilo do Turvo, deixado na capela pela Igreja quando a "
                               "Fenda foi fechada, para não sair dali. Ele foi para a água com ela.",
            "marcados": "Dois homens com uma marca queimada no pulso reviravam a sacristia atrás de alguma coisa. "
                        "Não eram da vila, e não estavam sozinhos.",
            "correntes": "No ossuário, um sarilho velho prende correntes que descem ao fundo alagado da capela, "
                         "amarradas a duas mós de moinho. Alguma coisa está presa lá embaixo.",
            "verdade_de_ilse": "Vó Berta viu, aos oito anos: a vila inteira tirou Ilse de casa, amarrou-a às mós do "
                               "moinho e a desceu na cripta. O pai dela segurou a corda. Ninguém mandou parar.",
            "nome_e_fita": "Berta acredita que Ilse pode descansar se alguém a chamar pelo nome, devolver a fita dela e "
                           "a soltar das pedras. A guardiã não precisaria ser destruída.",
            "relato_de_ilse": "Ilse disse que o Sigilo é um de três, que os três seguram fechada uma porta que agora "
                              "range, e que há mãos procurando juntá-los.",
        },
        # O que se faz para depois. Não é saber: conhecer o nome de Ilse é pista, não preparo.
        preparos={
            "corpo_solto": "As correntes do sarilho estão soltas: o que está no fundo da capela não está mais preso às "
                           "mós.",
            "fita": "A fita de Ilse, que Vó Berta guardou desde a noite do afogamento e entregou a você.",
        },
    ),
}


def estado_inicial(regiao):
    """As missões de uma campanha no começo: cada uma na primeira etapa, sem cenas vistas nem pistas."""
    return {mid: {"etapa": next(iter(m["etapas"])), "cenas": [], "pistas": [], "preparos": [], "desfecho": None,
                  "dia_desfecho": None, "concluida": None}
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


# Dar descanso a Ilse pede três coisas (11-E1-REGIAO-INICIAL.md, seção 6): saber a verdade, ter a fita e ter soltado o
# corpo. Cada uma: o que é, onde se consegue, e se já está feita. O Diário mostra a lista depois da sacristia (é lá que
# se descobre que há alguém a quem dar descanso); a descida ao fundo diz o que falta.
REQUISITOS_DESCANSO = [
    ("A verdade sobre a morte de Ilse", "Vó Berta, na taverna do Vau, estava lá",
     lambda m: {"ilse", "verdade_de_ilse"} <= set(m["pistas"])),
    ("A fita de Ilse", "quem a viu morrer guardou alguma coisa dela", lambda m: "fita" in m["preparos"]),
    ("O corpo solto das pedras", "o sarilho, no ossuário da capela", lambda m: "corpo_solto" in m["preparos"]),
]


def descanso(m):
    """Os requisitos do rito, como a tela e o texto mostram: [(o quê, onde, feito)]."""
    return [(o_que, onde, bool(feito(m))) for o_que, onde, feito in REQUISITOS_DESCANSO]


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
        loc = _lugar(g, etapa["lugar"])
        dist = distancias(g.mundo["locais"], g.loc["id"]).get(loc["id"]) if loc else None
        saida.append({"id": mid, "nome": d["nome"], "etapa": m["etapa"], "objetivo": etapa["objetivo"],
                      "lugar": loc and loc["nome"], "lugar_id": loc and loc["id"], "lugar_tipo": loc and loc["tipo"],
                      "bioma": loc and loc["bioma"], "distancia": dist,
                      "pistas": [d["pistas"][p] for p in m["pistas"]],
                      "preparos": [d["preparos"][p] for p in m.get("preparos", [])],
                      "desfecho": m.get("desfecho"),
                      "requisitos": None if m.get("concluida") else d.get("requisitos", lambda g, m: None)(g, m),
                      "concluida": m.get("concluida"),
                      **({"conclusao": f"Concluída no dia {m['concluida']}. " + d["conclusoes"][m["desfecho"]],
                          "linhas": [x for x in d.get("linhas", lambda g, m: [])(g, m) if x],
                          "pendente": d.get("pendente", lambda g, m: None)(g, m)}
                         if m.get("concluida") else {})})
    return saida


def _requisitos_descanso(g, m):
    """O caminho do rito: só depois de saber de Ilse, e só enquanto a guardiã não foi resolvida."""
    if "ilse" not in m["pistas"] or m.get("desfecho"):
        return None
    return {"titulo": "Para dar descanso a Ilse, em vez de destruí-la:",
            "itens": [{"texto": o_que, "onde": onde, "feito": feito} for o_que, onde, feito in descanso(m)]}


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
                                 pendente=_pendente_febre)


# ------------------------------------------------------------------ cenas e ações

def _abertura(g, mid):
    g.ui.cena(MISSOES[mid]["nome"], g.contexto_cena(), "evento")
    g.narrar("No Vau do Turvo há tosse atrás de quase toda porta. A febre começou há poucos meses: primeiro as crianças "
             "e os velhos, depois quem cuidava deles. Unhas escuras, sono pesado, sonhos com água.")
    g.narrar("O poço da praça secou no ano passado, quando o riacho baixou. Na mesma época brotou uma fonte nova, logo "
             "abaixo das últimas casas. A vila a recebeu como bênção e passou a beber dela.")
    g.narrar("\"Desde que a fonte apareceu\", diz uma mulher enchendo dois baldes, sem levantar os olhos, \"ninguém aqui "
             "dorme direito.\"")
    g.narrar("Marta, a curandeira, também está de cama. Anos atrás, foi ela quem tirou você de uma febre de estrada, "
             "numa cama da casa dela, sem cobrar nada. Agora é Pita, a aprendiz dela, quem atende na cabana.")
    g.dizer(f"Diário: {MISSOES[mid]['etapas']['fonte']['objetivo']}", "ciano")
    g.ui.efeito(f"Missão: {MISSOES[mid]['nome']}", "info")


# A hora do dia na prosa, pelo período de agora (dados.PERIODOS: Manhã, Tarde, Anoitecer, Noite).
_HORA = ("a manhã", "a tarde", "o anoitecer", "a noite")


def _pista(m, pid):
    if pid not in m["pistas"]:
        m["pistas"].append(pid)


def _examinar_fonte(g, mid):
    m = registro(g, mid)
    g.ui.cena("A Fonte Nova", g.contexto_cena(), "evento")
    g.narrar("A Fonte Nova brota entre pedras soltas, num buraco que ninguém cavou. A água é clara à primeira vista e "
             f"fria demais para {_HORA[min(g.periodo, 3)]}.")
    g.narrar({
        "guerreiro": "Você afasta as pedras maiores com as mãos. Por baixo, a terra está mole e afundada numa linha "
                     "reta, como se a água tivesse aberto caminho à força, vinda do leste.",
        "arqueiro": "Você se agacha e segue o fio de água com os olhos, como se segue um rastro. Ele não sobe do chão: "
                    "corre por baixo da terra, vindo do leste, do lado do moinho.",
        "mago": "Você põe a mão na água e algo nela não se deixa ler, como uma palavra apagada. A sensação vem de longe, "
                "do leste, por onde a água chega.",
    }.get(g.j.classe, "A água não sobe do chão: chega por baixo da terra, vinda do leste."))
    g.narrar("No fundo da bacia, quando a água assenta, fica um lodo escuro e fino. Nascente não deixa isso. Água que "
             "passou por algum lugar parado, sim.")
    _pista(m, "agua_do_leste")
    if avancar(g, mid, "fonte", "canal"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['canal']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


def _seguir_canal(g, mid):
    m = registro(g, mid)
    g.ui.cena("O Canal do Moinho", g.contexto_cena(), "evento")
    g.narrar("Você procura o riacho entre as árvores e o segue até o moinho. Acima da roda, uma represa nova de "
             "troncos e pedra segura a água num lago raso. O leito velho, o que descia para o Vau, é um fio entre "
             "pedras secas.")
    g.narrar("Do lado da represa sai um canal recém-cavado, reto como uma régua. Uma comporta de tábuas manda a "
             "água para ele, e ele segue para leste, atravessando o bosque rumo ao brejo.")
    g.narrar({
        "guerreiro": "Você desce ao leito velho e chuta as pedras secas. A marca da água ainda está nelas, um palmo "
                     "acima: o riacho que enchia o poço da vila agora passa quase todo pelo canal.",
        "arqueiro": "Você anda ao lado do canal até onde as árvores rareiam. Nenhum bicho bebe dele: as pegadas na lama "
                    "chegam até a beira e voltam.",
        "mago": "Perto da represa a água é só água. Mais adiante, rumo ao brejo, volta aquela sensação da Fonte Nova: "
                "uma palavra apagada, cada vez mais perto.",
    }.get(g.j.classe, "Rumo ao brejo, a água do canal fica mais escura e mais fria."))
    g.narrar("Você segue o canal até onde o bosque acaba. Adiante, meio engolida pelo brejo, há uma capela de pedra "
             "com o telhado afundado, e o canal entra por um rombo no muro dela. Do outro lado, a terra encharcada "
             "desce na direção da vila, como o fio que você viu na Fonte Nova.")
    _pista(m, "represa")
    _pista(m, "canal_da_capela")
    if avancar(g, mid, "canal", "capela"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['capela']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


def _capela_exterior(g, mid):
    g.ui.cena("A Capela Afogada", g.contexto_cena(), "evento")
    g.narrar("A capela está afundada até a metade das janelas. Juncos crescem no que foi o adro, e a porta da frente "
             "sumiu sob a lama. O sino não está mais na torre.")
    g.narrar("O canal que você seguiu desde o moinho termina aqui: a água entra pelo rombo no muro e desaparece no "
             "escuro lá dentro, sem barulho. Do rombo vem um frio que não é do brejo.")
    g.narrar("Na beira da água, os sapos estão quietos. Alguns têm patas a mais.")


# ------------------------------------------------------------------ o interior da capela
# Cada sala: o texto de chegada, a luta (criaturas que já existem, geradas no nível do lugar) e, só com vitória, o que
# se acha e a etapa seguinte. Fuga ou derrota não contam: a sala continua por vencer, e a próxima luta é outra. A
# capela é ruína, sempre escura: cada sala pede uma tocha (sem ela, o escuro pesa como em qualquer lugar).

def _lutar(g, grupo, titulo):
    """A luta da sala. Devolve True só com vitória (a derrota sai daqui como sempre, para o resgate ou o fim)."""
    from . import sobrevivencia
    luz = sobrevivencia.acender_tocha(g)
    try:
        r = g.combate(grupo, emboscada=None if luz else "inimigo", titulo=titulo)
    finally:
        g.sem_luz = False
    g.fechar_espolio()
    return r == "vitoria"


def _recuo(g, titulo, texto):
    g.ui.cena(titulo, g.contexto_cena(), "evento")
    g.narrar(texto)
    g.dizer("A sala continua por vencer. Dá para voltar quando quiser.", "cinza")


def _nave(g, mid):
    m = registro(g, mid)
    g.ui.cena("A Nave Alagada", g.contexto_cena(), "evento")
    g.narrar("Você entra pelo rombo, com a água do canal pelos joelhos. Lá dentro, a nave é um lago escuro entre "
             "colunas. A água corre devagar entre os bancos podres e some numa fenda do piso, perto do altar.")
    g.narrar("Alguma coisa se mexe entre os bancos. Corpos inchados se levantam da água, e o fundo se enche de "
             "sanguessugas.")
    if not _lutar(g, g.grupo("afogado", n=1) + g.grupo("sanguessuga", n=2), "A Nave Alagada"):
        _recuo(g, "A Nave Alagada", "Você recua pela brecha, de volta ao brejo. Lá dentro, a água se fecha de novo.")
        return
    g.ui.cena("A Nave Alagada", g.contexto_cena(), "evento")
    g.narrar("Com a água quieta, dá para ver o caminho dela. Entra pelo muro rompido, atravessa a nave, desce pela "
             "fenda do piso e, mais adiante, sai por baixo do muro dos fundos, rumo à vila.")
    g.narrar("Na boca do rombo, ela é clara. Na saída, deixa nas pedras o mesmo lodo escuro da Fonte Nova. A vila bebe "
             "o que passa por baixo desta capela.")
    g.narrar("Atrás do altar, uma porta baixa leva à sacristia.")
    _pista(m, "agua_da_capela")
    g.avancar_periodo()
    if avancar(g, mid, "capela", "sacristia"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['sacristia']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


def _sacristia(g, mid):
    m = registro(g, mid)
    g.ui.cena("A Sacristia", g.contexto_cena(), "evento")
    g.narrar("A sacristia ficou acima da água: um degrau a mais salvou o chão. Há gente aqui. Dois homens de capa "
             "escura reviram as prateleiras à luz de uma lanterna. Os dois têm a mesma marca queimada no pulso.")
    g.narrar("Um deles ergue a lanterna para o seu rosto. \"Não é ela\", diz. O outro já está com a faca na mão.")
    if not _lutar(g, g.grupo("cultista", n=2), "A Sacristia"):
        _recuo(g, "A Sacristia", "Você volta pela nave até a brecha. Atrás de você, a lanterna se apaga.")
        return
    g.ui.cena("A Sacristia", g.contexto_cena(), "evento")
    g.narrar({
        "guerreiro": "As botas deles ainda pingam. Não vieram pela brecha: há uma escada de mão encostada na janela "
                     "alta.",
        "arqueiro": "Na lama da janela alta há pegadas de mais gente do que os dois que caíram. Os outros saíram antes "
                    "de você chegar.",
        "mago": "A marca no pulso deles não é tinta. Foi queimada, e ainda tem um cheiro que não é de fogo.",
    }.get(g.j.classe, "Não vieram pela brecha: há uma escada de mão encostada na janela alta."))
    g.narrar("O que eles procuravam ficou num nicho da parede, embrulhado num couro duro: o livro da capela. As "
             "primeiras páginas são de um padre de letra miúda. Ele anota a chegada de Ilse, \"guardiã desta casa\", "
             "no ano em que a Fenda foi fechada, e o que a Igreja deixou com ela: \"o Sigilo do Turvo, que não deve "
             "sair desta capela nem ir para mão nenhuma\".")
    g.narrar("Anos depois, a letra treme. A vila acusa Ilse de bruxaria: a febre daquele inverno, os sonhos com água, o "
             "gado morto no brejo. O padre escreve que ela não fez nada disso, que só guardava. Na linha seguinte: "
             "\"Entregue à água pela vontade da vila. O Sigilo foi com ela. Que Deus nos perdoe.\"")
    for pid in ("ilse", "sigilo_do_turvo", "marcados"):
        _pista(m, pid)
    g.narrar("Embaixo de um pano, num canto, há um baú pequeno de ferro, trancado. No chão, um alçapão desce para o "
             "ossuário.")
    g.dar("bau")
    g.avancar_periodo()
    if avancar(g, mid, "sacristia", "ossuario"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['ossuario']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


def _ossuario(g, mid):
    m = registro(g, mid)
    g.ui.cena("O Ossuário", g.contexto_cena(), "evento")
    g.narrar("O alçapão dá numa escada de pedra que desce para o frio. O ossuário é uma sala baixa, com nichos de ossos "
             "arrumados nas paredes. Alguns nichos estão vazios. Os ossos que faltam estão de pé, no meio da sala.")
    if not _lutar(g, g.grupo("esqueleto", n=2), "O Ossuário"):
        _recuo(g, "O Ossuário", "Você sobe a escada de costas e fecha o alçapão. Embaixo, os ossos voltam a se arrumar.")
        return
    g.ui.cena("O Ossuário", g.contexto_cena(), "evento")
    g.narrar("No fundo da sala há um sarilho de madeira preta, grosso como um tronco, com correntes enroladas no eixo. "
             "Elas descem por um buraco no chão até a água parada lá embaixo, e estão esticadas: alguma coisa pesada "
             "as segura no fundo.")
    g.narrar("Com a tocha no buraco, aparece a borda de duas mós velhas de moinho, presas às correntes. Quem fez isto "
             "quis que nada saísse dali. Do buraco sobe o mesmo frio do rombo, e a água lá embaixo não devolve a luz.")
    _pista(m, "correntes")
    g.avancar_periodo()
    if avancar(g, mid, "ossuario", "fundo"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['fundo']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")
    g.dizer("As correntes podem ser soltas daqui, antes de descer.", "cinza")
    g.ui.efeito("Protótipo: o fundo da capela fica para a próxima parte da missão.", "info")


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


def _soltar(g, mid):
    """O fim comum: a corrente desce frouxa e o preparo fica registrado."""
    m = registro(g, mid)
    if "corpo_solto" not in m["preparos"]:
        m["preparos"].append("corpo_solto")
        from .telemetria import registrar
        registrar(g, "missao", missao=mid, preparo="corpo_solto")
    g.narrar("Lá embaixo, a água se mexe uma vez e para.")
    g.dizer("Diário: as correntes estão soltas.", "ciano")
    g.ui.efeito("Diário atualizado", "info")


def _onda_de_afogados(g, mid):
    """O barulho do sarilho desce pela água e chama os afogados. Só a vitória deixa terminar o trabalho."""
    g.narrar("Da escada vem o som de água se mexendo. Os afogados vieram atrás do barulho.")
    if not _lutar(g, g.grupo("afogado", n=2), "O Sarilho"):
        _recuo(g, "O Sarilho", "Você sobe pelo alçapão e deixa o sarilho como estava. As correntes continuam presas.")
        return
    g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
    g.narrar("Com a sala quieta de novo, você termina o trabalho. A última volta da corrente escorrega do eixo e desce, "
             "frouxa, para o fundo.")
    g.avancar_periodo()
    _soltar(g, mid)


def _correntes_a_mao(g, mid):
    g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
    g.narrar("Você firma os pés e começa a desenrolar a corrente, elo por elo. O sarilho range como um bicho, e o "
             "barulho desce pelo buraco e corre pela água da capela inteira.")
    _onda_de_afogados(g, mid)


def _correntes_atalho(g, mid):
    attr, texto = ATALHOS_CORRENTES[g.j.classe]
    g.ui.cena("O Sarilho", g.contexto_cena(), "evento")
    if g.j.classe == "arqueiro":
        g.j.flechas -= 1
    if g.teste(attr, CD_CORRENTES):
        g.narrar(texto)
        _soltar(g, mid)
        return
    g.narrar("Não deu: a trava não cede, e o eixo solta um rangido que desce pelo buraco e corre pela água da capela "
             "inteira. Agora vai ter de ser à mão.")
    _onda_de_afogados(g, mid)


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
    g.narrar("\"Não foi um homem só. Foi a vila. Tiraram ela de casa de noite, amarraram nas mós velhas do moinho e "
             "desceram tudo pela cripta, com corrente e sarilho. Meu pai segurou a corda. Eu vi da porta da capela, e "
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
    g.dizer("Diário: a verdade sobre Ilse e a fita dela.", "ciano")
    g.ui.efeito("Fita de Ilse", "info")


def _fundo(g, mid):
    """A descida ao fundo: a guardiã. O que falta para o rito é dito antes; o rito só é oferecido com tudo pronto."""
    from .inimigos import instanciar_guardiao
    m = registro(g, mid)
    g.ui.cena("O Fundo da Capela", g.contexto_cena(), "evento")
    g.narrar("A escada do ossuário termina na água. A cripta é um poço escuro, com água pela cintura e um frio que não é "
             "de água. No meio, entre duas mós de moinho, há uma forma enrolada em correntes.")
    if "corpo_solto" in m["preparos"]:
        g.narrar("As correntes que você soltou pendem frouxas. A forma já não está presa às pedras.")
    g.narrar("Ela abre os olhos. A pele é azulada, os cabelos são algas, e ela começa a cantar uma canção de ninar. É "
             "Ilse, ou o que a vila fez dela: a Bruxa Afogada.")
    pronto = descanso_pronto(m)
    if not pronto:
        falta = [o_que[0].lower() + o_que[1:] for o_que, _, feito in descanso(m) if not feito]
        g.dizer("Para tentar dar descanso a Ilse ainda falta: " + tx.lista_natural(falta) + ". Sem isso, só resta "
                "destruí-la.", "cinza")
    opcoes = ([("Chamar Ilse pelo nome e tentar dar descanso", "descanso")] if pronto else []) + [
        ("Lutar para destruí-la", "destruir"), ("Voltar por enquanto", None)]
    op = g.menu("Ela ainda não se levantou da água. Depois de começar, não há como recuar.", opcoes)
    if op is None:
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
    luz = sobrevivencia.acender_tocha(g)
    try:
        r = g.combate([chefe], emboscada=None if luz else "inimigo", pode_fugir=False,
                      titulo="Guardiã: Ilse, a Bruxa Afogada")
    finally:
        g.sem_luz = False
    g.fechar_espolio()
    if r == "vitoria":
        _resolver(g, mid, "descansada" if getattr(chefe, "descansou", False) else "destruida", chefe.nivel)


def _momento_do_rito(g, cb, e):
    """No limiar: a escolha é do motor; a tela só a mostra. Devolver o nome e a fita encerra a luta em paz (ela e o que
    ela chamou da água afundam). Desistir tira o piso: o dano que ele segurou cai na hora e a luta segue para a
    segunda fase, como em qualquer guardião. Nada do que a build faz se perde para quem escolhe destruir."""
    cb.dizer("Ilse vacila à metade. As correntes soltas pendem dos pulsos dela, e os olhos dela vão para a fita na sua "
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
        g.narrar("Por um momento, ela é só uma mulher cansada com a água pela cintura. Ela pega a fita da sua mão e a "
                 "enrola nos dedos.")
        g.narrar("\"Eu tinha a custódia dele\", diz, sem raiva. \"É um de três. Os três seguram fechada uma porta que "
                 "nunca devia ter sido aberta, e agora ela range. Há mãos procurando os três. Não os deixe juntar por "
                 "quem não sabe o que está fechando.\"")
        g.narrar("Ela abre a mão. O Sigilo do Turvo, rachado e frio como pedra de rio, passa para a sua. Depois ela "
                 "afunda devagar, com a fita entre os dedos, e a água da cripta fica parada e clara.")
        _pista(m, "relato_de_ilse")
    else:
        g.ui.cena("A Guardiã Destruída", g.contexto_cena(), "evento")
        g.narrar("Ilse se desfaz na água escura, e o canto vira bolhas. Por um instante, a água que desce para a vila "
                 "corre mais turva.")
        g.narrar("Onde ela esteve, entre as mós, sobra o Sigilo do Turvo, rachado e frio como pedra de rio. Presa às "
                 "pedras, há também uma veste de couro endurecido pela água, que ainda guarda a forma de alguém.")
    g.receber_sigilo("turvo", "Ilse, a Bruxa Afogada")
    if desfecho == "destruida":
        g.oferecer_equip(itens.fazer_unico(itens.UNICOS_POR_ID["pele_do_penitente"], min(nivel, g.j.nivel + 2)))
    g.avancar_periodo()
    if avancar(g, mid, "fundo", "retorno"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['retorno']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


def _retorno(g, mid):
    """A volta ao Vau depois da guardiã, uma vez: o que a água e a vila mostram agora (depende do desfecho e de quantos
    dias passaram, consequencias.estado_fonte) e a conclusão da missão. Volta cedo ou tarde, a cena conta o de agora."""
    from . import consequencias
    m = registro(g, mid)
    fonte = consequencias.estado_fonte(g)
    g.ui.cena("De Volta ao Vau", g.contexto_cena(), "evento")
    g.narrar("Você entra no Vau com o Sigilo do Turvo no bolso, ainda frio como pedra de rio.")
    g.narrar({
        ("descansada", "limpando"): "Na Fonte Nova, o lodo assentou no fundo da bacia, e a água que corre por cima já "
                                    "sai mais clara." + (" Ninguém piorou de noite." if consequencias.noites(g) else " Ninguém piorou desde então."),
        ("destruida", "escura"): "A Fonte Nova corre escura, quase preta: o que estava no corpo de Ilse saiu de uma vez. "
                                 "A vila inteira tosse mais desde que a água escureceu, e ninguém enche balde.",
        ("destruida", "limpando"): "A Fonte Nova ainda tem a cor de chá fraco, mas clareia. Contam que houve uma noite "
                                   "em que a água correu preta e todos pioraram. O pior passou.",
    }.get((m["desfecho"], fonte), "A Fonte Nova corre clara, e há fila de baldes de novo na praça."))
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
    g.dizer(f"Missão concluída: {MISSOES[mid]['nome']}. O que aconteceu fica no Diário.", "ciano")
    g.ui.efeito(f"Missão concluída: {MISSOES[mid]['nome']}", "info")


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
ACOES = [
    dict(missao="febre_do_turvo", id="examinar_fonte", rotulo="Examinar a Fonte Nova", lugar="vau_do_turvo",
         etapas=("fonte",), fn=_examinar_fonte, confirmar=True),
    dict(missao="febre_do_turvo", id="seguir_canal", rotulo="Seguir a água e examinar o canal",
         lugar="bosque_do_moinho", etapas=("canal",), fn=_seguir_canal, confirmar=True),
    dict(missao="febre_do_turvo", id="nave", rotulo="Entrar na capela pela brecha do canal", lugar="capela_afogada",
         etapas=("capela",), fn=_nave, confirmar=True),
    dict(missao="febre_do_turvo", id="sacristia", rotulo="Atravessar a nave até a sacristia", lugar="capela_afogada",
         etapas=("sacristia",), fn=_sacristia, confirmar=True),
    dict(missao="febre_do_turvo", id="ossuario", rotulo="Descer ao ossuário", lugar="capela_afogada",
         etapas=("ossuario",), fn=_ossuario, confirmar=True),
    dict(missao="febre_do_turvo", id="correntes", rotulo="Soltar as correntes do sarilho à mão (demora e faz barulho)",
         lugar="capela_afogada", etapas=("fundo",), falta="corpo_solto", fn=_correntes_a_mao, confirmar=True),
    dict(missao="febre_do_turvo", id="correntes_forca", rotulo="Arrancar a trava do sarilho (Força)",
         lugar="capela_afogada", etapas=("fundo",), falta="corpo_solto", classe="guerreiro", fn=_correntes_atalho,
         confirmar=True),
    dict(missao="febre_do_turvo", id="correntes_arcano", rotulo="Apodrecer o ferro da trava (Arcano)",
         lugar="capela_afogada", etapas=("fundo",), falta="corpo_solto", classe="mago", fn=_correntes_atalho,
         confirmar=True),
    dict(missao="febre_do_turvo", id="correntes_tiro", rotulo="Um tiro no pino da trava (Destreza, 1 flecha)",
         lugar="capela_afogada", etapas=("fundo",), falta="corpo_solto", classe="arqueiro",
         pode=lambda g: g.j.flechas > 0, fn=_correntes_atalho, confirmar=True),
    dict(missao="febre_do_turvo", id="fundo", rotulo="Descer ao fundo da capela (a guardiã)", lugar="capela_afogada",
         etapas=("fundo",), fn=_fundo, confirmar=True),
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


def _vale(g, d):
    m = registro(g, d["missao"])
    return bool(m and g.campanha == MISSOES[d["missao"]]["campanha"] and g.loc.get("chave") == d["lugar"]
                and m["etapa"] in d["etapas"] and g.combate_ativo is None and not g.na_estrada
                and d.get("classe", g.j.classe) == g.j.classe and d.get("falta") not in m.get("preparos", [])
                and d.get("pode", lambda _: True)(g))


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
            registro(g, d["missao"])["cenas"].append(d["id"])  # antes de tocar: se cair numa luta ou num save, não repete
            d["fn"](g, d["missao"])
            _encerrar(g, d)
            return True
    return False


def opcoes(g):
    """As ações de missão que valem no lugar e na etapa de agora, como opções do menu do lugar."""
    if not g.campanha:
        return []
    return [(d["rotulo"], ("missao", d["missao"], d["id"]), {**d.get("meta", {}), "missao": d["missao"]})
            for d in ACOES if _vale(g, d)]


def executar(g, mid, aid):
    """Faz a ação de missão escolhida, se ela ainda vale (um clique repetido numa ação já feita não faz nada)."""
    for d in ACOES:
        if (d["missao"], d["id"]) == (mid, aid) and _vale(g, d):
            d["fn"](g, mid)
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
