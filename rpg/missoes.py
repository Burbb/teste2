"""Missões da campanha escrita: um registro por missão, com id estável e etapas explícitas.

E3 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md, seção 5): "A Febre do Turvo" começa com uma cena curta no Vau do Turvo; a
investigação segue a água da Fonte Nova até o canal no Bosque do Moinho e o canal até a Capela Afogada. Dentro dela, três
salas em sequência (a nave, a sacristia, o ossuário), cada uma uma ação do menu da capela: sair e voltar é só escolher
outra coisa no menu, e a sala vencida fica vencida (a etapa já passou dela). Esta parte termina antes do fundo: a
guardiã, o rito, a comporta, Caspar e os desfechos ainda não existem.

O estado de cada missão mora no mundo da campanha (`mundo["missoes"]`, vai no save junto com ele):
    {"etapa": "fundo", "cenas": ["abertura"], "pistas": ["agua_do_leste", ...], "preparos": ["corpo_solto"]}
`pistas` é o que se sabe; `preparos` é o que se fez para depois (soltar o corpo das correntes). Saber o nome de Ilse não
prepara nada: o rito, nas próximas entregas, ainda pede o resto.
O mundo gerado não tem missões. Cenas e ações declaram a campanha (pela missão), o lugar (`chave` do lugar) e as
etapas em que valem; o jogo só as oferece no menu do lugar, nunca no meio de uma luta, de uma viagem ou de um evento.
Passar antes por um lugar não adianta nem gasta nada: a cena ou a ação esperam a etapa delas.
"""

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
            "sigilo_do_turvo": "Ilse guardava o Sigilo do Turvo, deixado na capela pela Igreja quando a Fenda foi "
                               "fechada, para não sair dali. Ele foi para a água com ela.",
            "marcados": "Dois homens com uma marca queimada no pulso reviravam a sacristia atrás de alguma coisa. "
                        "Não eram da vila, e não estavam sozinhos.",
            "correntes": "No ossuário, um sarilho velho prende correntes que descem ao fundo alagado da capela, "
                         "amarradas a duas mós de moinho. Alguma coisa está presa lá embaixo.",
        },
        # O que se faz para depois. Não é saber: conhecer o nome de Ilse é pista, não preparo.
        preparos={
            "corpo_solto": "As correntes do sarilho estão soltas: o que está no fundo da capela não está mais preso às "
                           "mós.",
        },
    ),
}


def estado_inicial(regiao):
    """As missões de uma campanha no começo: cada uma na primeira etapa, sem cenas vistas nem pistas."""
    return {mid: {"etapa": next(iter(m["etapas"])), "cenas": [], "pistas": [], "preparos": []}
            for mid, m in MISSOES.items() if m["campanha"] == regiao}


def completar(estado):
    """Saves de antes dos preparos (1.50–1.51): a chave entra vazia. O resto do progresso fica como estava."""
    for m in estado.values():
        m.setdefault("preparos", [])


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


def cartoes(g):
    """As missões em andamento como o Diário e o rastreador mostram: nome, objetivo da etapa, lugar e pistas."""
    from .mundo import distancias
    saida = []
    for mid, m in (g.mundo.get("missoes") or {}).items():
        d = MISSOES[mid]
        etapa = d["etapas"][m["etapa"]]
        loc = _lugar(g, etapa["lugar"])
        dist = distancias(g.mundo["locais"], g.loc["id"]).get(loc["id"]) if loc else None
        saida.append({"id": mid, "nome": d["nome"], "etapa": m["etapa"], "objetivo": etapa["objetivo"],
                      "lugar": loc and loc["nome"], "lugar_id": loc and loc["id"], "lugar_tipo": loc and loc["tipo"],
                      "bioma": loc and loc["bioma"], "distancia": dist,
                      "pistas": [d["pistas"][p] for p in m["pistas"]],
                      "preparos": [d["preparos"][p] for p in m.get("preparos", [])]})
    return saida


# ------------------------------------------------------------------ cenas e ações

def _abertura(g, mid):
    g.ui.cena(MISSOES[mid]["nome"], g.contexto_cena(), "evento")
    g.narrar("No Vau do Turvo há tosse atrás de quase toda porta. A febre começou há poucos meses: primeiro as crianças "
             "e os velhos, depois quem cuidava deles. Unhas escuras, sono pesado, sonhos com água.")
    g.narrar("O poço da praça secou no ano passado, quando o riacho baixou. Na mesma época brotou uma fonte nova, logo "
             "abaixo das últimas casas. A vila a recebeu como bênção e passou a beber dela.")
    g.narrar("\"Desde que a fonte apareceu\", diz uma mulher enchendo dois baldes, sem levantar os olhos, \"ninguém aqui "
             "dorme direito.\"")
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


# Cada cena toca uma vez, quando a pessoa está no menu daquele lugar, naquela etapa. Cada ação é uma opção do menu do
# lugar, com a mesma condição; executar confere tudo de novo. `confirmar`: o texto termina num Continuar de verdade
# (a tela não vira a página sozinha, por tempo, e o clique que adianta o texto não fecha a cena).
CENAS = [
    dict(missao="febre_do_turvo", id="abertura", lugar="vau_do_turvo", etapas=("fonte",), fn=_abertura,
         confirmar=True),
    dict(missao="febre_do_turvo", id="capela_exterior", lugar="capela_afogada", etapas=("capela",),
         fn=_capela_exterior, confirmar=True),
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
    return [(d["rotulo"], ("missao", d["missao"], d["id"]), {"missao": d["missao"]}) for d in ACOES if _vale(g, d)]


def executar(g, mid, aid):
    """Faz a ação de missão escolhida, se ela ainda vale (um clique repetido numa ação já feita não faz nada)."""
    for d in ACOES:
        if (d["missao"], d["id"]) == (mid, aid) and _vale(g, d):
            d["fn"](g, mid)
            _encerrar(g, d)
            return True
    return False
