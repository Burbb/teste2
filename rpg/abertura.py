"""A abertura guiada da campanha (E9, roadmapIDEIAS/18-E9-ABERTURA-GUIADA.md).

Duas partes, separadas de propósito:

- **A abertura**, igual para todos na campanha nova: a despensa da taverna do Vau (dois ratos gigantes, uma luta
  curta e previsível), a caneca por conta da casa (uma vez o serviço de bebida e rumores, sem pagar) e a oportunidade
  de sentar com Morel, pelo evento que já existe (`morel_na_taverna`), só enquanto ele nunca apareceu.
- **As orientações**, que a caixa "Mostrar tutorial" liga: os quadros da primeira luta (C1–C4), o do Mural (V1) e os
  da segunda parte (V2 recuperar, V3 provisões, V4 comitiva, V5 explorar, E1 equipamento, T1 talentos, N1 noite), uma
  por vez, quando fazem sentido. O motor diz qual vale agora e o texto dela; a tela desenha. Ligadas ou não, a
  abertura, as recompensas e o sorteio são os mesmos: nada aqui sorteia, e o que se marca como visto (a ação que a
  orientação ensina aconteceu, ou a ocasião dela passou) não depende da caixa.

O estado mora em `g.mundo["abertura"]` (vai no save com o mundo). Um save sem ele (de antes, ou do mundo gerado) não
tem despensa; a Ajuda pode ligar as orientações nele também.
"""

from . import balanceamento as bal
from . import comitiva as cm
from . import texto as tx
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
    pessoa faz); fora dela, a da vez (proxima). Só com a caixa ligada."""
    if not tutorial(g):
        return None
    j = g.j
    if g.combate_ativo is None:
        return proxima(g)
    if not _combate_pendente(g) or not j.habilidades:
        return None
    hid = hab_inicial(j) if hab_inicial(j) in j.habilidades else j.habilidades[0]
    return {"id": "combate", "passos": {
        "C1": "Clique em **Habilidades** (tecla 2).",
        "C2": f"Clique em **{efetiva(j, hid)['nome']}** (tecla {j.habilidades.index(hid) + 1}).",
        "C3": "Clique num inimigo para escolher o alvo (ou a tecla do número dele).",
        "C4": {h: _c4(j, h) for h in j.habilidades}}, "hab": hid}


# ------------------------------------------------------------------ a segunda parte (V2–V5, E1, T1, N1)
# Uma por vez, na ordem: o que a tela pede agora (o item achado, a viagem) e, nos menus do lugar, preparar e se
# recuperar antes de chamar para coisas novas.
VIDA_BAIXA = 0.7       # V2: abaixo de 70% da vida...
RECURSO_BAIXO = 0.5    # ...ou de metade do recurso
DIAS_DE_COMIDA = 3     # V3: com menos dias de comida que isto (você e a comitiva), o quadro lembra o Mercado
POUCO = {"Mana": "Pouca Mana", "Vigor": "Pouco Vigor", "Foco": "Pouco Foco"}
TODO = {"Mana": "toda a Mana", "Vigor": "todo o Vigor", "Foco": "todo o Foco"}
MOTIVO_EXPLORAR = ("\"O dinheiro de verdade está no que ninguém foi buscar. Desde que a febre fechou a estrada, tem "
                   "coisa largada pelo caminho: carroça tombada, trouxa de quem fugiu. Às vezes alguma coisa presta; "
                   "às vezes só tem lobo.\"")


def contexto(g, qual, dados=None):
    """A tela que pede a sua orientação (o item achado, a escolha do destino): quem abre a pergunta marca, e desmarca
    depois (`contexto(g, None)`). Não vai no save."""
    g.abertura_contexto = (qual, dados) if qual else None


def proxima(g):
    """A orientação da vez fora da luta, com a caixa ligada ou não (o que se cumpre não depende dela). None antes do
    pedido do taverneiro, na luta e quando nada vale."""
    a = estado(g)
    if not a or g.combate_ativo is not None or a.get("despensa") == "nova":
        return None
    ctx = getattr(g, "abertura_contexto", None)
    if ctx:
        f = {"achado": _e1, "viagem": _v3}.get(ctx[0])
        return f(g, a, ctx[1]) if f else None
    for f in (_v2, _n1, _v1, _t1, _v4, _v5):
        o = f(g, a)
        if o:
            return o
    return None


def _pendente(a, oid):
    return oid not in a["vistas"]


def _v1(g, a):
    if _v1_pendente(g):
        return {"id": "V1", "texto": "Clique no **mural** para ver os contratos disponíveis.", "ancora": "mural"}


def preco_dormir(g):
    return g.preco(8 + 2 * g.j.nivel)


def _v2(g, a):
    """Recuperar: vida abaixo de 70% ou recurso abaixo de metade, no menu da vila. Aponta o serviço que resolve o que
    falta e que dá para pagar: a vida no Templo; o recurso (ou a vida, se o Templo não cabe no bolso) na Taverna."""
    j = g.j
    if not _pendente(a, "V2") or g.loc["tipo"] != "vila":
        return None
    vida, rec = j.hp < j.max_hp * VIDA_BAIXA, j.rec < j.max_rec * RECURSO_BAIXO
    if not (vida or rec):
        return None
    r = j.nome_recurso
    dormir = preco_dormir(g)
    dorme = j.ouro >= dormir
    templo = next((o for o in g.opcoes_templo() if o[1][1] is None), None)  # o do herói: ("templo", None, preço, falta)
    cura = templo is not None and j.ouro >= templo[1][2]
    feridas = " Ferimentos, a **Curandeira** trata." if j.ferimentos else ""
    taverna = (f"Dormir na **Taverna** ({dormir} de ouro) devolve {TODO.get(r, r)} e "
               f"{round(bal.TAVERNA_VIDA * 100)}% da vida{' (menos, com fome)' if j.fome else ''}.")
    if vida and cura:
        texto = f"Vida baixa. O **Templo** devolve a vida toda por {templo[1][2]} de ouro."
        if rec and dorme:
            texto += f" {POUCO.get(r, r)}: {taverna[0].lower()}{taverna[1:]}"
        return {"id": "V2", "texto": texto + feridas, "ancora": "predio:templo"}
    if dorme:
        falta = "Vida baixa" + (f" e {POUCO.get(r, r).lower()}" if rec else "") if vida else POUCO.get(r, r)
        return {"id": "V2", "texto": f"{falta}. {taverna}" + (feridas if vida else ""), "ancora": "predio:taverna"}
    return None  # nada que resolva cabe no bolso agora: o quadro espera


def _v3(g, a, _dados=None):
    """Provisões, ao escolher o destino da primeira viagem: o contador do topo, o que se come por dia (você e quem
    anda com você), e o Mercado só se a comida está curta."""
    if not _pendente(a, "V3"):
        return None
    j = g.j
    bocas = 1 + len(cm.membros(g))
    dias = j.provisoes // bocas
    quanto = (f"dá {tx.plural(dias, 'dia')}" if dias else "não dá um dia para todos" if j.provisoes else
              "você não tem nenhuma")
    texto = ("Cada amanhecer come 1 provisão sua" + (" e 1 de cada companheiro" if bocas > 1 else "") +
             f", na vila ou fora: {quanto}. Sem provisão, fome.")
    if dias < DIAS_DE_COMIDA and g.loc["tipo"] == "vila":
        texto += " O **Mercado** vende mais."
    texto += " Dormindo na Taverna, o ensopado é por conta dela."
    return {"id": "V3", "texto": texto, "ancora": "provisoes", "entendi": True}


def _v4(g, a):
    """O primeiro companheiro que anda com você (Morel ou outro), presente aqui: o cartão dele no painel."""
    if not _pendente(a, "V4"):
        return None
    m = next((m for m in cm.membros(g) if not cm.fora(g, m)), None)
    if not m:
        return None
    nome = cm.nome(m["id"])
    texto = f"{nome} anda com você: luta junto e come 1 provisão por dia."
    if m["ferido"]:
        texto += f" Está {cm.flexao(m['id'], 'ferid{a}')}: fora de combate até descansar."
    texto += " **Comitiva**, na barra de baixo: conversar e mandar para o acampamento."
    return {"id": "V4", "texto": texto, "ancora": f"membro:{m['id']}", "entendi": True}


def _v5(g, a):
    """Explorar, na primeira ocasião fora da vila: a ação do menu do lugar."""
    if not _pendente(a, "V5") or g.loc["tipo"] == "vila":
        return None
    return {"id": "V5", "texto": "**Explorar a região** gasta um período. Pode dar luta, um achado, alguém pelo "
                                 "caminho ou nada: é por aí que se acha o que não está nos contratos.",
            "ancora": "opcao:Explorar a região"}


def _e1(g, a, dados):
    """A primeira comparação de equipamento (um item achado que você pode usar, com o que você veste no lugar)."""
    if not _pendente(a, "E1") or not dados or not dados.get("compara"):
        return None
    compara = "A linha \"contra…\" compara o achado com o que você usa (▲ ganha, ▼ perde)."
    if dados.get("cabe"):
        texto = f"{compara} **Equipar** veste o novo e guarda o antigo na mochila; **Guardar** leva o novo na mochila."
    else:
        texto = f"{compara} Com a mochila cheia, **Equipar** deixa o antigo para trás."
    return {"id": "E1", "texto": texto, "ancora": "achado"}


def _t1(g, a):
    """O primeiro ponto de talento por gastar: o atalho da árvore. Ponto já gasto não conta."""
    n = g.j.pontos_talento
    if not _pendente(a, "T1") or n <= 0:
        return None
    return {"id": "T1", "texto": f"Você tem {tx.plural(n, 'ponto')} de talento. **Talentos**, na barra de baixo, "
                                 "abre a árvore.", "ancora": "doca:Talentos", "entendi": True}


def _n1(g, a):
    """A primeira noite fora da vila: o aviso do topo, e a diferença entre a noite e a falta de luz neste lugar."""
    from . import sobrevivencia
    if not _pendente(a, "N1") or g.loc["tipo"] == "vila" or not g.noite:
        return None
    from . import missoes
    sempre = g.bioma in ("ruinas", "cidadela") or missoes.tem_salas(g)
    luz = ("Aqui é escuro até de dia; a tocha resolve a luz, não a noite." if sempre else
           "A tocha resolve o escuro, não a noite.")
    if not sobrevivencia.escuro(g):
        luz = ""
    return {"id": "N1", "texto": f"Noite: **Inimigos +{bal.NOITE_NIVEL} nível**, no topo, vale para as lutas daqui "
                                 f"(o detalhe, com o mouse). {luz}".strip(),
            "ancora": "mod:noite", "entendi": True}


# O que cada menu cumpre ao ser respondido: a ocasião passou (o quadro apareceu e a pessoa seguiu). Os talentos
# também: o quadro aparece uma vez (o ★ do atalho continua avisando) e não segura os outros na fila.
PASSA_NO_MENU = ("N1", "V4", "V5", "T1")


def depois_do_menu(g, antes, op):
    """Depois da resposta a um menu do lugar: `antes` é a orientação que valia quando ele abriu (proxima). Uma
    da ocasião (noite, comitiva, explorar, talentos) passa; a de recuperar, só se o serviço foi usado (ou na partida
    da vila, `partiu`)."""
    if not antes:
        return
    oid = antes["id"]
    if oid in PASSA_NO_MENU or (oid == "V2" and (
            op == "dormir" or (isinstance(op, tuple) and op[0] == "templo"))):
        visto(g, oid)


def partiu(g):
    """A viagem começou: as provisões (V3) já não precisam do quadro; saindo da vila com a vida ou o recurso baixo,
    a recuperação (V2) ficou para trás por escolha da pessoa."""
    a = estado(g)
    if not a:
        return
    visto(g, "V3")
    if a.get("despensa") != "nova" and _v2(g, a):
        visto(g, "V2")


def entendi(g, oid):
    """O "Entendi" da tela: só as informativas (as outras se encerram pela ação)."""
    if oid in ("V3", "V4", "T1", "N1"):
        visto(g, oid)


def motivo_explorar(g, quem):
    """O motivo de explorar, uma vez, na voz de quem está lá: o taverneiro, ao servir a caneca, se Morel não anda com
    você; Morel, na primeira vez fora da vila com ele. Só na campanha com a abertura; igual com e sem tutorial."""
    a = estado(g)
    if not a or "despensa" not in a or a.get("motivo"):
        return
    junto = cm.presente(g, "morel")
    if quem == "taverneiro" and not junto:
        g.narrar(f"Ele baixa a voz. {MOTIVO_EXPLORAR}")
    elif quem == "morel" and junto and g.loc["tipo"] != "vila":
        g.narrar(f"Morel olha em volta, a mão no cabo da espada. {MOTIVO_EXPLORAR}")
    else:
        return
    a["motivo"] = True


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
    r = j.nome_recurso
    for oid, grupo, texto in (
            ("V2", "Vila", f"Vida baixa: o **Templo** devolve a vida por ouro. {POUCO.get(r, r)}: dormir na **Taverna** "
                           f"devolve {TODO.get(r, r)} e {round(bal.TAVERNA_VIDA * 100)}% da vida. Ferimentos: a Curandeira."),
            ("V3", "Estrada", "Cada amanhecer come 1 provisão sua e 1 de cada companheiro, na vila ou fora. O Mercado "
                              "vende; o ensopado da Taverna alimenta sem gastar."),
            ("V4", "Comitiva", "Quem anda com você luta junto e come 1 provisão por dia. **Comitiva**, na barra de "
                               "baixo: conversar e mandar para o acampamento."),
            ("V5", "Estrada", "**Explorar a região** gasta um período: luta, achado, alguém pelo caminho ou nada."),
            ("E1", "Herói", "No item achado, ▲ e ▼ comparam com o que você usa. **Equipar** troca; **Guardar** leva "
                            "na mochila."),
            ("T1", "Herói", "**Talentos**, na barra de baixo, abre a árvore quando há ponto para gastar."),
            ("N1", "Estrada", f"À noite, os inimigos vêm {bal.NOITE_NIVEL} nível acima e batem mais forte. A tocha "
                              "resolve o escuro, não a noite.")):
        if oid in vistas:
            linhas.append({"grupo": grupo, "texto": texto})
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
    elif onde == "vila" and _v1_pendente(g) and (proxima(g) or {}).get("id") == "V1":
        g.dizer("Dica: o \"Mural de contratos\" tem trabalho pago.", "cinza")
    elif onde != "combate":
        o = proxima(g)
        ditos = g.__dict__.setdefault("abertura_ditas", set())  # a sessão de texto: cada dica uma vez
        if o and o["id"] != "V1" and o["id"] not in ditos:
            ditos.add(o["id"])
            g.dizer("Dica: " + o["texto"].replace("**", "\""), "cinza")
