"""Missões da campanha escrita: um registro por missão, com id estável e etapas explícitas.

E3 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md, seção 5): "A Febre do Turvo" começa com uma cena curta no Vau do Turvo; a
investigação segue a água da Fonte Nova até o canal no Bosque do Moinho e o canal até a Capela Afogada, onde esta parte
termina, do lado de fora. Salas da capela, a comporta, a guardiã, Caspar e os desfechos ainda não existem.

O estado de cada missão mora no mundo da campanha (`mundo["missoes"]`, vai no save junto com ele):
    {"etapa": "canal", "cenas": ["abertura"], "pistas": ["agua_do_leste"]}
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
        },
        pistas={
            "agua_do_leste": "A Fonte Nova não nasce ali: a água chega por baixo da terra, do leste, do lado do Bosque "
                             "do Moinho, e traz um lodo escuro e fino que água de nascente não tem.",
            "represa": "No ano passado, o moleiro represou o riacho acima do moinho e abriu um canal para leste. O "
                       "trecho que descia para a vila minguou: é por isso que o poço da praça secou.",
            "canal_da_capela": "O canal do moinho corre até o brejo e entra por um rombo no muro de uma capela "
                               "afundada, a Capela Afogada. Abaixo dela, a terra está encharcada na direção da vila.",
        },
    ),
}


def estado_inicial(regiao):
    """As missões de uma campanha no começo: cada uma na primeira etapa, sem cenas vistas nem pistas."""
    return {mid: {"etapa": next(iter(m["etapas"])), "cenas": [], "pistas": []}
            for mid, m in MISSOES.items() if m["campanha"] == regiao}


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
                      "pistas": [d["pistas"][p] for p in m["pistas"]]})
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
    g.ui.efeito("Protótipo: o interior da capela abre numa próxima parte da missão.", "info")


# Cada cena toca uma vez, quando a pessoa está no menu daquele lugar, naquela etapa. Cada ação é uma opção do menu do
# lugar, com a mesma condição; executar confere tudo de novo. `confirmar`: o texto termina num Continuar de verdade
# (a tela não vira a página sozinha, por tempo, e o clique que adianta o texto não fecha a cena).
CENAS = [
    dict(missao="febre_do_turvo", id="abertura", lugar="vau_do_turvo", etapas=("fonte",), fn=_abertura,
         confirmar=True),
    dict(missao="febre_do_turvo", id="capela_exterior", lugar="capela_afogada", etapas=("capela",),
         fn=_capela_exterior, confirmar=True),
]
ACOES = [
    dict(missao="febre_do_turvo", id="examinar_fonte", rotulo="Examinar a Fonte Nova", lugar="vau_do_turvo",
         etapas=("fonte",), fn=_examinar_fonte, confirmar=True),
    dict(missao="febre_do_turvo", id="seguir_canal", rotulo="Seguir a água e examinar o canal",
         lugar="bosque_do_moinho", etapas=("canal",), fn=_seguir_canal, confirmar=True),
]


def _vale(g, d):
    m = registro(g, d["missao"])
    return bool(m and g.campanha == MISSOES[d["missao"]]["campanha"] and g.loc.get("chave") == d["lugar"]
                and m["etapa"] in d["etapas"] and g.combate_ativo is None and not g.na_estrada)


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
