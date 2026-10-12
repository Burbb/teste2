"""A abertura guiada da campanha (E9, roadmapIDEIAS/18-E9-ABERTURA-GUIADA.md).

Duas partes, separadas de propósito:

- **A abertura**, igual para todos na campanha nova: a despensa da taverna do Vau (dois ratos gigantes, uma luta
  curta e previsível), a caneca por conta da casa (uma vez o serviço de bebida e rumores, sem pagar) e a oportunidade
  de sentar com Morel, pelo evento que já existe (`morel_na_taverna`), só enquanto ele nunca apareceu.
- **As orientações**, que a caixa "Mostrar tutorial" liga: os quadros da primeira luta (C1–C4) e o do Mural (V1). O
  motor diz qual vale agora e o texto dela; a tela desenha. Ligadas ou não, a abertura, as recompensas e o sorteio são
  os mesmos: nada aqui sorteia, e o que se marca como visto não depende da caixa.

O estado mora em `g.mundo["abertura"]` (vai no save com o mundo). Um save sem ele (de antes, ou do mundo gerado) não
tem despensa; a Ajuda pode ligar as orientações nele também.
"""

from . import balanceamento as bal
from . import comitiva as cm
from .classes import CLASSES
from .habilidades import efetiva
from .talentos import custo_habilidade

MOREL = "morel_na_taverna"
VAU = "vau_do_turvo"
LUTAS_SEM_HABILIDADE = 2  # depois de tantas lutas sem abrir Habilidades, o quadro para de insistir


def estado(g):
    return (g.mundo or {}).get("abertura")


def comecar(g, tutorial):
    """Uma campanha nova (Jogo.novo_jogo): a despensa espera no Vau; as orientações conforme a caixa."""
    g.mundo["abertura"] = {"tutorial": bool(tutorial), "despensa": "nova", "caneca": False, "vistas": [],
                           "lutas_sem_habilidade": 0}


def _registro(g):
    """O estado, criado vazio se ainda não há (um save de antes, o mundo gerado): sem despensa."""
    return g.mundo.setdefault("abertura", {"tutorial": False, "vistas": [], "lutas_sem_habilidade": 0})


def tutorial(g):
    a = estado(g)
    return bool(a and a.get("tutorial"))


def ligar(g, valor):
    """A Ajuda (ou "Encerrar tutorial", com False): liga ou desliga as orientações deste save."""
    _registro(g)["tutorial"] = bool(valor)


def visto(g, oid):
    """Uma orientação cumprida (a ação que ela ensina aconteceu): não volta, com a caixa ligada ou não."""
    a = estado(g)
    if a is not None and oid not in a["vistas"]:
        a["vistas"].append(oid)


# ------------------------------------------------------------------ a despensa
def _no_vau(g):
    return (bool(g.campanha) and g.loc.get("chave") == VAU and g.combate_ativo is None and not g.na_estrada)


def cena_pendente(g):
    """O pedido do taverneiro, uma vez, no primeiro menu do Vau depois da abertura da febre."""
    a = estado(g)
    if not a or a.get("despensa") != "nova" or not _no_vau(g):
        return False
    a["despensa"] = "adiada"  # se a pessoa disser "Agora não" (ou cair na luta), a ação fica na taverna
    g.ui.cena("A Despensa da Taverna", g.contexto_cena(), "evento")
    g.narrar("O taverneiro do Vau te para na porta. \"Você tem cara de quem sabe usar isso aí\", diz, olhando para a "
             "sua arma. \"Desde que a febre derrubou meu ajudante, ninguém desce na despensa. Os ratos tomaram conta. "
             "Se der um jeito neles, a primeira caneca é por minha conta.\"")
    if g.menu("O que você faz?", [("Descer à despensa", "descer"), ("Agora não", None)]):
        descer(g)
    else:
        g.dizer("O pedido fica de pé: a despensa está na Taverna quando você quiser.", "cinza")
    return True


# Os ratos da despensa: a espécie de sempre, nível 1, mas magros (40% do ataque, pouca agilidade) e sem a mordida e
# o veneno, para a primeira luta ensinar com pouco risco. Medido em 3600 lutas simuladas (três classes; só atacar,
# o roteiro guiado, alternar e escolhas ao acaso): nenhuma derrota (18, seção 12). O nome e a ficha mostram que são
# outros ratos; nada é escondido (o golpe crítico e o ferimento seguem as regras de sempre).
RATO_ATK = 0.4
RATO_AGI = 2


def _rato(g):
    e = g.inimigo("rato", nivel=1)
    e.nome = e.nome.replace("Rato gigante", "Rato da despensa", 1)
    e.atk *= RATO_ATK
    e.agi = RATO_AGI
    e.habilidades = []
    e.ouro = 0
    return e


def descer(g):
    a = _registro(g)
    g.ui.cena("A Despensa da Taverna", g.contexto_cena(), "evento")
    g.narrar("A despensa é um porão baixo, com cheiro de cebola e palha molhada. Dois ratos do tamanho de gatos se "
             "viram para a luz.")
    r = g.combate([_rato(g), _rato(g)], titulo="A Despensa", saque=False)
    if r != "vitoria":  # fugiu: a despensa continua lá (a derrota sai daqui para o resgate, com ela adiada)
        g.dizer("Os ratos continuam lá embaixo. A despensa está na Taverna quando você quiser.", "cinza")
        g.pausar()
        return
    a["despensa"], a["caneca"] = "feita", True
    g.ui.cena("A Taverna do Vau", g.contexto_cena(), "evento")
    g.narrar("O taverneiro olha os dois ratos e cospe de lado. \"A primeira caneca é por minha conta. Se quiser mais "
             "trabalho, dê uma olhada no mural de contratos, na praça.\"")
    if morel_esperando(g):  # quem já encontrou Morel (por qualquer caminho) não ouve a apresentação de novo
        g.narrar("No canto, um homem grande come sozinho, de costas para a parede. Assistiu a tudo sem levantar. "
                 "\"Rato é fácil\", diz. \"Senta aqui, se quiser ouvir uma proposta.\"")
    g.ui.continuar(confirmar=True)  # a cena espera o Continuar, com ou sem tutorial: há o que ler


# ------------------------------------------------------------------ Morel e a caneca
def morel_esperando(g):
    """Morel ainda não apareceu (por nenhum caminho) e está livre: só então a abertura o apresenta."""
    return g.contagem.get(MOREL, 0) == 0 and cm.disponivel(g, "morel")


def caneca(g):
    a = estado(g)
    return bool(a and a.get("caneca"))


def usar_caneca(g):
    estado(g)["caneca"] = False


def opcoes(g):
    """As ações da abertura no menu do Vau, como cartões da Taverna."""
    a = estado(g)
    if not a or not _no_vau(g):
        return []
    r = []
    if a.get("despensa") == "adiada":
        r.append(("Taverna: descer à despensa", ("abertura", "despensa"),
                  {"predio": "taverna", "servico": "despensa", "curto": "Descer à despensa",
                   "efeito": "Os ratos que o taverneiro quer fora", "nota": "Luta: dois ratos da despensa."}))
    if a.get("despensa") == "feita" and morel_esperando(g):
        r.append(("Taverna: sentar com o homem do canto", ("abertura", "morel"),
                  {"predio": "taverna", "servico": "morel", "curto": "Sentar com o homem do canto",
                   "efeito": "Ele assistiu à luta da despensa"}))
    return r


def executar(g, aid):
    if aid == "despensa" and estado(g).get("despensa") == "adiada":
        descer(g)
    elif aid == "morel" and morel_esperando(g):
        from . import eventos
        eventos.disparar_id(g, MOREL, "taverna")  # o mesmo evento da bebida: conta uma vez, com as regras dele
        g.pausar()


# ------------------------------------------------------------------ as orientações
def hab_inicial(j):
    """A habilidade ofensiva do nível 1 da classe (Golpe Pesado, Tiro Certeiro, Bola de Fogo)."""
    return next(h for n, h in CLASSES[j.classe]["habilidades"] if n == 1)


def devolve(j):
    """Quanto o Atacar devolve do recurso ao acertar (heroi.ataque_basico)."""
    return max(bal.ATAQUE_RECURSO_MIN, round(j.max_rec * bal.ATAQUE_RECURSO))


def _custo(j, hid, verbo="gastou"):
    """O que a habilidade gasta, nas regras da classe: o recurso e, no Arqueiro, as flechas (e o que o Atacar faz)."""
    h = efetiva(j, hid)
    rec = j.nome_recurso
    gasto = f"{custo_habilidade(j, hid)} de {rec}"
    if h.get("flechas_por_alvo"):
        gasto += " e uma flecha por inimigo"
    elif h.get("flechas"):
        gasto += f" e {h['flechas']} flecha{'s' if h['flechas'] > 1 else ''}"
    if j.classe == "arqueiro":
        return (f"{h['nome']} {verbo} {gasto}. **Atacar** também gasta 1 flecha (sem flechas, vira um golpe de adaga "
                f"mais fraco), não gasta {rec} e, se acertar, devolve {devolve(j)}.")
    return f"{h['nome']} {verbo} {gasto}. **Atacar** não gasta {rec} e, se acertar, devolve {devolve(j)}."


def _c4(j, hid):
    """O C4 em partes curtas, para a tela separar o nome, os custos e o Atacar: cada parte é texto puro (`t`) ou um
    valor com o ícone e a cor do recurso (`rec`: Vigor, Mana, Foco) ou da flecha (`flecha`). O nome do recurso
    continua escrito; a cor reforça. Custo real da habilidade (a ficha do herói) e o Atacar pelas regras da classe."""
    h = efetiva(j, hid)
    rec = j.nome_recurso
    gasto = [{"rec": rec, "t": f"−{custo_habilidade(j, hid)} {rec}"}]
    if h.get("flechas_por_alvo"):
        gasto.append({"flecha": True, "t": "−1 flecha por inimigo"})
    elif h.get("flechas"):
        gasto.append({"flecha": True, "t": f"−{h['flechas']} flecha{'s' if h['flechas'] > 1 else ''}"})
    volta = {"rec": rec, "t": f"+{devolve(j)} {rec}"}
    if j.classe == "arqueiro":
        atacar = [{"t": "Atacar: "}, {"flecha": True, "t": "−1 flecha"}, {"t": f", sem {rec}. Ao acertar, "}, volta,
                  {"t": ". Sem flechas, vira um golpe de adaga mais fraco."}]
    else:
        atacar = [{"t": f"Atacar não gasta {rec}. Ao acertar, "}, volta, {"t": "."}]
    return {"nome": h["nome"], "gasto": gasto, "atacar": atacar}


def _combate_pendente(g):
    a = estado(g)
    return bool(a and "combate" not in a["vistas"] and a.get("lutas_sem_habilidade", 0) < LUTAS_SEM_HABILIDADE)


def depois_da_luta(g, usou_habilidade):
    """O fim de uma luta (Combate.fim): quem usou uma habilidade cumpriu C1–C4; quem não usou conta uma luta a mais
    (depois de duas, o quadro para). Vale com a caixa ligada ou não: o que se aprendeu não depende dela."""
    a = estado(g)
    if not a or "combate" in a["vistas"]:
        return
    if usou_habilidade:
        visto(g, "combate")
    else:
        a["lutas_sem_habilidade"] = a.get("lutas_sem_habilidade", 0) + 1


def _v1_pendente(g):
    a = estado(g)
    return bool(a and "V1" not in a["vistas"] and g.loc["tipo"] == "vila" and g.combate_ativo is None
                and a.get("despensa") not in ("nova",))


def atual(g):
    """A orientação que vale agora, ou None. Na luta, a sequência C1–C4 (a tela avança passo a passo pelo que a
    pessoa faz); na vila, o V1. Só com a caixa ligada."""
    if not tutorial(g):
        return None
    j = g.j
    if g.combate_ativo is not None:
        if not _combate_pendente(g) or not j.habilidades:
            return None
        hid = hab_inicial(j) if hab_inicial(j) in j.habilidades else j.habilidades[0]
        return {"id": "combate", "passos": {
            "C1": "Clique em **Habilidades** (tecla 2).",
            "C2": f"Clique em **{efetiva(j, hid)['nome']}** (tecla {j.habilidades.index(hid) + 1}).",
            "C3": "Clique num inimigo para escolher o alvo (ou a tecla do número dele).",
            "C4": {h: _c4(j, h) for h in j.habilidades}}, "hab": hid}
    if _v1_pendente(g):
        return {"id": "V1", "texto": "Clique no **mural** para ver os contratos disponíveis.", "ancora": "mural"}
    return None


# O que a Ajuda lista, de cada orientação já vista (com a caixa ligada ou não).
def ajuda(g):
    a = estado(g) or {}
    j = g.j
    vistas = a.get("vistas", [])
    linhas = []
    if "combate" in vistas or a.get("lutas_sem_habilidade"):
        hid = hab_inicial(j)
        linhas.append({"grupo": "Luta", "texto": "Na sua vez, **Habilidades** (tecla 2) abre a lista; clique numa "
                                                 "habilidade e depois no alvo."})
        linhas.append({"grupo": "Luta", "texto": _custo(j, hid, "gasta")})
    if "V1" in vistas:
        linhas.append({"grupo": "Vila", "texto": "Clique no **mural** para ver os contratos disponíveis."})
    return {"ligado": tutorial(g), "linhas": linhas}


def para_tela(g):
    """O que a tela recebe no estado: a orientação de agora e a Ajuda."""
    if not g.mundo:
        return None
    return {"atual": atual(g), **ajuda(g)}


def dica_texto(g, onde):
    """Na interface de texto, cada orientação vira uma linha cinza, uma vez por luta (C) ou por visita (V1)."""
    if not tutorial(g) or g.ui.hud:
        return
    if onde == "combate" and _combate_pendente(g) and g.j.habilidades:
        hid = hab_inicial(g.j)
        custo = _custo(g.j, hid, "gasta").replace("**", "\"")
        g.dizer(f"Dica: na sua vez, \"Habilidades\" abre a lista. {custo}", "cinza")
    elif onde == "vila" and _v1_pendente(g):
        g.dizer("Dica: o \"Mural de contratos\" tem trabalho pago.", "cinza")
