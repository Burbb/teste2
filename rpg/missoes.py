"""Missões da campanha escrita: um registro por missão, com id estável e etapas explícitas.

Primeira entrega da E3 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md, seção 5): "A Febre do Turvo" começa com uma cena curta
no Vau do Turvo e o primeiro passo da investigação (examinar a Fonte Nova), que aponta o canal no Bosque do Moinho.
Salas da capela, a guardiã, Caspar e os desfechos ainda não existem.

O estado de cada missão mora no mundo da campanha (`mundo["missoes"]`, vai no save junto com ele):
    {"etapa": "fonte", "cenas": ["abertura"], "pistas": ["agua_do_leste"]}
O mundo gerado não tem missões. Cenas e ações declaram a campanha (pela missão), o lugar (`chave` do lugar) e as
etapas em que valem; o jogo só as oferece no menu do lugar, nunca no meio de uma luta, de uma viagem ou de um evento.
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
        },
        pistas={
            "agua_do_leste": "A Fonte Nova não nasce ali: a água chega por baixo da terra, do leste, do lado do Bosque "
                             "do Moinho, e traz um lodo escuro e fino que água de nascente não tem.",
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
# Cada cena: (missão, id, lugar, etapas em que vale). Toca uma vez, quando a pessoa está no menu daquele lugar.
# Cada ação: uma opção no menu do lugar, com a mesma condição; executar confere tudo de novo.

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


def _examinar_fonte(g, mid):
    m = registro(g, mid)
    g.ui.cena("A Fonte Nova", g.contexto_cena(), "evento")
    g.narrar("A Fonte Nova brota entre pedras soltas, num buraco que ninguém cavou. A água é clara à primeira vista e "
             "fria demais para o fim da tarde.")
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
    if "agua_do_leste" not in m["pistas"]:
        m["pistas"].append("agua_do_leste")
    if avancar(g, mid, "fonte", "canal"):
        g.dizer(f"Diário: {MISSOES[mid]['etapas']['canal']['objetivo']}", "ciano")
        g.ui.efeito("Diário atualizado", "info")


CENAS = [("febre_do_turvo", "abertura", "vau_do_turvo", ("fonte",), _abertura)]
ACOES = [("febre_do_turvo", "examinar_fonte", "Examinar a Fonte Nova", "vau_do_turvo", ("fonte",), _examinar_fonte)]


def _vale(g, mid, lugar, etapas):
    m = registro(g, mid)
    return bool(m and g.campanha == MISSOES[mid]["campanha"] and g.loc.get("chave") == lugar
                and m["etapa"] in etapas and g.combate_ativo is None and not g.na_estrada)


def cena_pendente(g):
    """Toca a cena de missão que vale aqui e agora e ainda não foi vista. Devolve True se tocou uma."""
    if not g.campanha:
        return False
    for mid, cid, lugar, etapas, fn in CENAS:
        if _vale(g, mid, lugar, etapas) and cid not in registro(g, mid)["cenas"]:
            registro(g, mid)["cenas"].append(cid)  # antes de tocar: se a cena cair numa luta ou num save, não repete
            fn(g, mid)
            g.pausar()
            return True
    return False


def opcoes(g):
    """As ações de missão que valem no lugar e na etapa de agora, como opções do menu do lugar."""
    if not g.campanha:
        return []
    return [(rotulo, ("missao", mid, aid), {"missao": mid})
            for mid, aid, rotulo, lugar, etapas, _ in ACOES if _vale(g, mid, lugar, etapas)]


def executar(g, mid, aid):
    """Faz a ação de missão escolhida, se ela ainda vale (um clique repetido numa ação já feita não faz nada)."""
    for m_id, a_id, _, lugar, etapas, fn in ACOES:
        if (m_id, a_id) == (mid, aid) and _vale(g, mid, lugar, etapas):
            fn(g, mid)
            g.pausar()
            return True
    return False
