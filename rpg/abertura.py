"""A abertura guiada da campanha (E9, roadmapIDEIAS/18-E9-ABERTURA-GUIADA.md).

Duas partes, separadas de propósito:

- **A abertura**, igual para todos na campanha nova: a despensa da taverna do Vau (dois ratos gigantes, uma luta
  curta e previsível), a caneca por conta da casa (uma vez o serviço de bebida e rumores, sem pagar) e a oportunidade
  de sentar com Morel, pelo evento que já existe (`morel_na_taverna`), só enquanto ele nunca apareceu.
- **As orientações**, que a caixa "Mostrar tutorial" liga: os quadros da primeira luta (C1–C4), o do Mural (V1) e os
  da segunda parte (V2 recuperar, V3 provisões, V4 comitiva, V5 explorar, E1 equipamento, T1 talentos, N1 noite) e
  os ciclos básicos (K1–K4 um contrato do mural ao pagamento, B1 o primeiro baú, S os selos da luta, A1 adiantar a
  apresentação), uma por vez, quando fazem sentido. O motor diz qual vale agora e o texto dela; a tela desenha. Ligadas ou não, a
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
    g.fechar_espolio()  # o relatório da luta (o XP) logo depois dela, antes da cena do taverneiro
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
        return selo_da_vez(g)
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
        f = {"achado": _e1, "viagem": _v3, "mural": _k1, "curandeira": _f4}.get(ctx[0])
        return f(g, a, ctx[1]) if f else None
    # Em volta da fogueira: o ferimento novo, dormir (D3), o baú e a bandagem (o resto espera o menu do lugar).
    # Fora dela: o contrato recém-aceito (K2) vem antes de todas, por ser a consequência do que a pessoa acabou de
    # fazer, e passa na primeira resposta ao menu (ou no Entendi); o ferimento novo (F1), logo depois. Depois,
    # preparar e se recuperar antes de chamar para coisas novas; o acampamento (D2) por último.
    ordem = ((_f1, _d3, _b1, _f2) if getattr(g, "na_fogueira", False) else
             (_k2, _f1, _v2, _n1, _v1, _f2, _f3, _a1, _k3, _k4, _b1, _t1, _v4, _v5, _d2))
    for f in ordem:
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


def _pode_dormir(g):
    """A cama da taverna dá para pagar agora (a mesma regra do cartão: Servicos.motivo_pagar)."""
    return not g.motivo_pagar(preco_dormir(g))


# Os quadros que mandam usar um serviço pago (V2, F3, F4, D1) só aparecem quando ele dá para usar agora: sem ouro, o
# cartão, o preço e o "Ouro insuficiente" continuam, e o quadro fica pendente (não conta como visto) até uma ocasião
# em que dê, sem segurar os outros.


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
    dorme = _pode_dormir(g)
    templo = next((o for o in g.opcoes_templo() if o[1][1] is None), None)  # o do herói: ("templo", None, preço, falta)
    cura = templo is not None and not templo[2].get("motivo")  # a mesma regra do cartão do templo
    # Um quadro, um alvo: o Templo fala da vida (e do grátis, enquanto vale); a Taverna, do recurso. O preço e os
    # números ficam nos cartões; os detalhes, na Ajuda.
    if vida and cura:
        texto = "O **Templo** recupera sua vida." + (" Seu primeiro atendimento é grátis." if not templo[1][2] else "")
        return {"id": "V2", "texto": texto, "ancora": "predio:templo"}
    if dorme:
        return {"id": "V2", "texto": f"Dormir na **Taverna** recupera {TODO.get(r, r)} e parte da vida.",
                "ancora": "predio:taverna"}
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
    texto += " Dormindo na Taverna, nenhuma provisão é consumida."
    return {"id": "V3", "texto": texto, "ancora": "provisoes", "entendi": True}


def _v4(g, a):
    """O primeiro companheiro que anda com você (Morel ou outro), presente aqui: o botão Comitiva, que abre a gestão
    (conversar, a confiança, mandar para o acampamento). Um objetivo só: o texto, o destaque e a seta no mesmo botão."""
    if not _pendente(a, "V4"):
        return None
    m = next((m for m in cm.membros(g) if not cm.fora(g, m)), None)
    if not m:
        return None
    return {"id": "V4", "texto": f"**Comitiva** abre quem anda com você ({cm.nome(m['id'])}): conversar, ver a confiança "
                                 "e mandar para o acampamento.", "ancora": "doca:Comitiva", "entendi": True}


def _v5(g, a):
    """Explorar, na primeira ocasião fora da vila: a ação do menu do lugar."""
    if not _pendente(a, "V5") or g.loc["tipo"] == "vila":
        return None
    from . import missoes
    if not missoes.pode_explorar(g):  # dentro da capela, a opção não existe: o quadro espera o lado de fora
        return None
    return {"id": "V5", "texto": "**Explorar a região** gasta um período: pode dar luta, um achado, alguém pelo "
                                 "caminho ou nada. É assim que se acha o que não está nos contratos.",
            "ancora": "opcao:Explorar a região"}


def _e1(g, a, dados):
    """A primeira comparação de equipamento (um item achado que você pode usar, com o que você veste no lugar)."""
    if not _pendente(a, "E1") or not dados or not dados.get("compara"):
        return None
    compara = "**Na troca** mostra o que muda (▲ ganha, ▼ perde)."
    if dados.get("cabe"):
        texto = f"{compara} **Equipar** veste o novo e guarda o antigo na mochila; **Guardar** leva o novo para a mochila."
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
    """A primeira noite fora da vila: a noite aumenta o perigo (os números já estão nos riscos do lugar) e a tocha
    ilumina o escuro, sem tirar o perigo da noite. Pelas regras do lugar: nas salas (a capela, escura também de dia),
    sem luz o inimigo ataca primeiro, sempre; fora delas, ser pego de surpresa só fica mais provável."""
    from . import missoes
    if not _pendente(a, "N1") or g.loc["tipo"] == "vila" or not g.noite:
        return None
    if missoes.tem_salas(g):
        luz = "Este lugar é escuro também de dia: sem tocha, cada sala começa com o inimigo atacando primeiro."
    elif g.bioma in ("ruinas", "cidadela"):
        luz = "Este lugar é escuro também de dia: sem tocha, ser pego de surpresa fica mais provável."
    else:
        luz = "Sem tocha, ser pego de surpresa fica mais provável."
    # A âncora: os riscos do lugar, à direita (a linha da noite, com os números, e a da tocha).
    return {"id": "N1", "texto": f"À noite, os inimigos ficam mais fortes, com ou sem tocha. {luz}", "ancora": "risco:noite",
            "entendi": True}


# ------------------------------------------------------------------ os ciclos básicos (K1–K4, B1, S, A1)
def _contrato_seguido(g):
    """O contrato que as orientações acompanham: o mais antigo em andamento (abandonado, passa ao seguinte)."""
    return next((c for c in g.contratos if not c.get("concluido")), None)


def _vizinho(g, lid):
    """O lugar `lid` é ligado direto a este por uma estrada (uma viagem só, sem atravessar outro lugar)?"""
    return lid in {int(i) for i in g.loc["con"]}


def _por_onde(g, lid):
    """O primeiro lugar do caminho mais curto daqui até `lid` (pelo grafo das estradas, não pela distância no mapa)."""
    from .mundo import distancias, vizinhos
    ate = distancias(g.mundo["locais"], lid)
    v, _ = min(vizinhos(g.mundo, g.loc), key=lambda vd: (vd[1] + ate.get(vd[0]["id"], 99), vd[0]["id"]))
    return v


def _adequado(g, c):
    """Um contrato bom para aprender: caça de bando (não um alvo de elite) num lugar do nível do herói ou abaixo e
    ligado direto a esta vila, para a primeira viagem ser uma só."""
    from .mundo import nivel_regiao
    return (c["tipo"] == "caca" and nivel_regiao(g.mundo["locais"][c["local"]]) <= g.j.nivel
            and _vizinho(g, c["local"]))


def _k1(g, a, oferta):
    """No Mural, sem contrato aceito ainda: um contrato de caça adequado ao começo (o mais fácil da oferta, se houver;
    a oferta é a de sempre, nada é gerado nem mudado para o tutorial; sem um adequado, o quadro espera outra oferta).
    Aceitar é da pessoa, e qualquer contrato vale."""
    from .mundo import nivel_regiao
    if not _pendente(a, "K1") or not oferta or g.contratos:
        return None
    bons = sorted((c for c in oferta["lista"] if _adequado(g, c)),
                  key=lambda c: (nivel_regiao(g.mundo["locais"][c["local"]]), c["total"]))
    if not bons:
        return None
    # O cartão já diz o alvo, o lugar e a recompensa: o quadro só diz o que fazer com ele.
    return {"id": "K1", "texto": "Aceite este contrato para começar.", "ancora": f"aceitar:{bons[0]['id']}"}


def _k2(g, a):
    """Um contrato aceito e o lugar dele longe daqui: o cartão do contrato, à direita. Ligado direto a este lugar, o
    clique no cartão viaja até lá (como o destino no mapa); mais longe, o clique não leva direto, e o quadro diz por
    onde o caminho passa."""
    c = _contrato_seguido(g)
    if not _pendente(a, "K2") or not _pendente(a, "K4") or not c:
        return None
    lid = c["destino"] if c["tipo"] == "entrega" else c["local"]
    if lid == g.loc["id"]:
        return None
    lugar = g.mundo["locais"][lid]["nome"]
    if _vizinho(g, lid):
        texto = f"Clique neste contrato para viajar até **{lugar}**."
    else:
        texto = f"O contrato é em **{lugar}**. O caminho passa por **{_por_onde(g, lid)['nome']}**."
    return {"id": "K2", "texto": texto, "ancora": f"contrato:{c['id']}", "entendi": True}


def _k3(g, a):
    """No lugar do contrato: a ação dele no menu (caçar o bando, rastrear o alvo)."""
    from . import dados
    if not _pendente(a, "K3") or not _pendente(a, "K4"):
        return None
    c = next(iter(g.contratos_aqui()), None)
    if not c:
        return None
    if c["tipo"] == "alvo":
        texto = "**Rastrear** leva até o alvo do contrato: vencê-lo cumpre o trabalho."
    else:
        f = dados.FAMILIAS[c["familia"]]
        a_ = "a" if f["g"] == "f" else "o"
        texto = (f"**Caçar** segue os rastros d{a_}s {f['plural']} do contrato. {f['plural'].capitalize()} "
                 f"vencid{a_}s ao explorar também contam.")
    return {"id": "K3", "texto": texto, "ancora": "opcao:(contrato"}


def _k4(g, a):
    """O contrato cumprido e ainda não pago: o pagamento vem na chegada a uma vila (a tela mostra quando paga)."""
    c = next((c for c in g.contratos if c.get("concluido")), None)
    if not _pendente(a, "K4") or not c or g.loc["tipo"] == "vila":
        return None
    return {"id": "K4", "texto": f"Contrato cumprido: {c['ouro']} de ouro e {c['xp']} XP, pagos quando você chegar a "
                                 "uma vila.", "ancora": f"contrato:{c['id']}", "entendi": True}


def _b1(g, a):
    """O primeiro baú de verdade na bolsa, onde dá para abri-lo: o espaço dele (a tela mostra o quadro quando o menu
    aceita a abertura, não enquanto a página espera Continuar). Com vários, o clique abre todos."""
    n = g.j.consumiveis.get("bau", 0)
    if not _pendente(a, "B1") or n <= 0 or g.motivo_inutil("bau"):
        return None
    return {"id": "B1", "texto": "Clique no baú para abrir." if n == 1 else f"Clique no baú para abrir os {n}.",
            "ancora": "bolsa:bau"}


def _a1(g, a):
    """A velocidade do texto, uma vez, depois da primeira luta: o botão Texto, no topo (revelar o texto e acelerar as
    animações têm a ocasião delas: APRESENTACAO)."""
    if not _pendente(a, "A1") or "combate" not in a["vistas"]:
        return None
    return {"id": "A1", "texto": "Ajuste a velocidade do texto aqui. Atalho: **V**.", "ancora": "topo:velocidade",
            "entendi": True}


# Revelar o texto (A0) e acelerar as animações da luta (AL): o motor diz se ainda valem e o texto; a ocasião é da
# tela, que sabe quando o texto está correndo (e se a cena acaba num Continuar) e quando a animação está na tela. Não
# entram na fila das outras (não seguram nenhuma) e passam quando aparecem e a pessoa segue.
APRESENTACAO = {
    "A0": "Clique para mostrar o texto inteiro. Depois, use **Continuar** para avançar.",
    "AL": "Clique na tela para acelerar a animação.",
}


def apresentacao(g):
    """As orientações da apresentação que ainda valem (depois da primeira luta, com a caixa ligada)."""
    a = estado(g)
    if not a or not tutorial(g) or "combate" not in a["vistas"]:
        return {}
    return {oid: t for oid, t in APRESENTACAO.items() if _pendente(a, oid)}


def selo_da_vez(g):
    """Na luta, a primeira vez de cada tipo de ícone de efeito numa carta: Firme, um mal e um bem, com o nome e o
    efeito de agora (os números do estado). A duração se explica uma vez, no primeiro. Só o que já aconteceu nesta
    luta; nada é forçado."""
    from .estados import ESTADOS, agora, dano_do_tique
    a = estado(g)
    cb = g.combate_ativo
    if not a or cb is None:
        return None
    unidades = [g.j] + list(getattr(cb, "aliados", None) or []) + list(getattr(cb, "inimigos", None) or [])
    achados = {}
    for u in unidades:
        if not getattr(u, "vivo", True) or getattr(u, "hp", 0) <= 0:
            continue
        for n, ef in (getattr(u, "efeitos", None) or {}).items():
            e = ESTADOS.get(n)
            if not e:
                continue
            oid = "SF" if n == "firme" else "S-" if e["negativo"] else "S+"
            achados.setdefault(oid, (u, n, ef, e))
    for oid in ("SF", "S-", "S+"):
        if oid not in achados or not _pendente(a, oid):
            continue
        u, n, ef, e = achados[oid]
        # O efeito de agora: o dano por turno (veneno, sangramento, chamas) ou a frase com o número do estado.
        if e.get("tique"):
            info = f"{dano_do_tique(cb, n, ef)} de dano por turno" + (f" e {e['dica']}" if e["golpe"] else "")
        elif n == "iniciativa":  # o principal: um turno a mais, só do herói, e o bônus (o do estado) no primeiro golpe
            juntos = bool(getattr(cb, "aliados", None)) or bool(getattr(cb, "companheiro", None))
            info = ("Você ganha um turno extra antes dos inimigos" + (" (só você: comitiva e animal agem a partir do turno seguinte)"
                                                                     if juntos else "") +
                    f". Seu primeiro golpe nessa abertura causa +{round(ef.get('v', 0) * 100)}% de dano")
        else:
            info = agora(n, ef.get("v", 0)) or e["dica"]
            if info.lower().startswith(e["titulo"].lower() + ": "):  # "fúria: +30% de dano", sob o nome Fúria
                info = info[len(e["titulo"]) + 2:]
        info = info[0].upper() + info[1:]
        t = ef["t"]
        if t <= 9 and (e.get("tique") or t > 1):  # o que dura só este turno já diz isso ("deste turno", "agora")
            info += f" · {tx.plural(t, 'turno')} restante{'s' if t != 1 else ''}"
        primeiro = not any(x in a["vistas"] for x in ("SF", "S-", "S+"))
        duracao = "\n_O número no ícone indica quantos turnos o efeito ainda dura." if primeiro else ""
        return {"id": oid, "texto": f"**{e['titulo']}**\n{info}.{duracao}", "ancora": f"selo:{cb.uid(u)}:{n}",
                "entendi": True}
    return None


# ------------------------------------------------------------------ ferimentos (F1–F4) e descanso (D1–D3)
def _ferida_aberta(j):
    """A ferida aberta ainda sem bandagem que uma bandagem enfaixaria agora: a primeira da lista (tratar_com_bandagem
    enfaixa essa, sem escolha)."""
    from .sobrevivencia import ferida_para_bandagem
    return ferida_para_bandagem(j)


def _efeito_ferimento(fid, recurso):
    """O que o ferimento tira, em linguagem direta: "−10% de vida máxima", "−30% de Agilidade"."""
    from .entidades import nome_stat
    from .sobrevivencia import FERIMENTOS
    nomes = {"max_hp": "vida máxima", "max_rec": f"{recurso} máximo" if recurso != "Mana" else "Mana máxima"}
    return tx.lista_natural(f"−{round((1 - v) * 100)}% de {nomes.get(stat) or nome_stat(stat, recurso)}"
                            for stat, v in FERIMENTOS[fid]["mult"].items())


def _f1(g, a):
    """O primeiro ferimento de verdade: o nome, o que ele tira e o que o faz sarar, em três linhas, com a seta na
    ficha. A bandagem e a Curandeira vêm depois (F2, F3), cada uma no alvo dela. Fora da luta (o golpe já passou);
    some sozinho se ele sarar antes."""
    from .sobrevivencia import FERIMENTOS
    j = g.j
    if not _pendente(a, "F1") or not j.ferimentos:
        return None
    f = j.ferimentos[0]
    sara = ("Não sara com descanso: use unguento ou vá à Curandeira." if f["id"] == "infeccao" else
            f"Sara depois de {tx.plural(f['dias'], 'dia')} de descanso, ou na hora, na Curandeira.")
    return {"id": "F1", "texto": f"**{FERIMENTOS[f['id']]['nome']}**\n{_efeito_ferimento(f['id'], j.nome_recurso)}."
                                 f"\n{sara}",
            "ancora": f"ferimento:{f['id']}", "entendi": True}


def _f2(g, a):
    """A primeira ferida aberta sem bandagem: com bandagem na bolsa, o espaço dela (a tela mostra quando o menu aceita o
    uso); sem bandagem, a alternativa, na ferida. Nunca para fratura, concussão ou infecção (a bandagem não trata)."""
    from .sobrevivencia import FERIMENTOS
    j = g.j
    f = _ferida_aberta(j)
    if not _pendente(a, "F2") or not f:
        return None
    if j.tem("bandagem") and not g.motivo_inutil("bandagem"):
        outras = sum(1 for x in j.ferimentos if FERIMENTOS[x["id"]].get("aberto") and not x["tratado"]) > 1
        texto = "A bandagem protege a ferida contra infecção. O ferimento ainda precisa sarar."
        if outras:  # uma bandagem, uma ferida: a primeira da lista, sem escolha
            texto += f" Cada bandagem enfaixa uma ferida, a começar por **{FERIMENTOS[f['id']]['nome']}**."
        return {"id": "F2", "texto": texto, "ancora": "bolsa:bandagem"}
    return {"id": "F2", "texto": "Sem bandagem, a ferida aberta pode infeccionar a cada noite. O **Mercado** vende "
                                 "bandagens; a Curandeira trata na hora.",
            "ancora": f"ferimento:{f['id']}", "entendi": True}


def curandeira_gratis(g):
    """O primeiro tratamento de um ferimento do herói na curandeira, de graça, uma vez por personagem, na campanha
    (com as orientações ligadas ou não). Só se gasta com o tratamento feito; separado do grátis do templo."""
    return bool(g.campanha) and not g.flag("curandeira_gratis_usado")


def _f3(g, a):
    """Na vila, com um ferimento: a Curandeira, e a diferença para o Templo."""
    j = g.j
    if not _pendente(a, "F3") or g.loc["tipo"] != "vila" or not j.ferimentos:
        return None
    if not any(not motivo for _, _, motivo in g.tratamentos()):
        return None  # nenhum tratamento cabe no bolso agora: o quadro espera
    gratis = " O primeiro tratamento é grátis." if curandeira_gratis(g) else ""
    return {"id": "F3", "texto": f"A **Curandeira** trata ferimentos na hora; o Templo só recupera vida.{gratis}",
            "ancora": "predio:curandeiro"}


def _f4(g, a, _dados=None):
    """Na cabana da curandeira: o cartão do primeiro ferimento que dá para tratar agora (o que o F1 mostrou, se der),
    com o preço de agora. Sem nenhum ao alcance do bolso, o quadro espera outra visita."""
    from .sobrevivencia import FERIMENTOS
    if not _pendente(a, "F4"):
        return None
    f = next((f for f, _, motivo in g.tratamentos() if not motivo), None)
    if not f:
        return None
    # O cartão já diz o preço (ou "Primeiro tratamento — grátis"): o quadro só diz o que fazer.
    return {"id": "F4", "texto": f"Clique neste cartão para tratar {FERIMENTOS[f['id']]['curto']}.",
            "ancora": f"tratar:{f['id']}"}


def custo_tratamento(g, f):
    """O preço de sempre da curandeira para um ferimento (a infecção custa mais)."""
    return g.preco((25 + 4 * g.j.nivel) if f["id"] == "infeccao" else (12 + 3 * g.j.nivel))


def _linhas(linhas):
    """As linhas do descanso (Tempo.linhas_descanso) no quadro: "Rótulo: texto"; as notas, apagadas (prefixo _)."""
    return "\n".join(f"{l['rotulo']}: {l['texto']}" if "rotulo" in l else "_" + l["nota"] for l in linhas)


def _d1(g, a):
    """A taverna aberta, com o cartão Dormir à vista (a tela acha a ocasião). O cartão já mostra o custo, a
    recuperação, as provisões e os ferimentos: o quadro só diz o que fazer (e, com ferimento, a Curandeira)."""
    j = g.j
    if not tutorial(g) or not _pendente(a, "D1") or g.loc["tipo"] != "vila" or g.combate_ativo is not None:
        return None
    if not _pode_dormir(g):
        return None  # sem ouro para a cama: o cartão diz isso; o quadro espera uma visita em que dê
    texto = "Clique neste cartão para dormir aqui até o amanhecer."
    if j.ferimentos:
        texto += "\n_A Curandeira trata ferimentos na hora."  # que o descanso ajuda a sarar, o cartão já diz
    return {"id": "D1", "texto": texto, "ancora": "servico:dormir", "entendi": True}


def _d2(g, a):
    """Fora da vila, com algo a recuperar: o Acampar do menu (dormir é lá dentro, na fogueira: D3)."""
    j = g.j
    if not _pendente(a, "D2") or g.loc["tipo"] == "vila" or (j.hp >= j.max_hp and j.rec >= j.max_rec):
        return None
    return {"id": "D2", "texto": f"Acampe para montar uma fogueira. Lá, você pode dormir para recuperar vida e "
                                 f"{j.nome_recurso}.", "ancora": "opcao:Acampar"}


def _d3(g, a):
    """Na fogueira: o Dormir até o amanhecer, em linhas curtas: o que volta e as provisões de verdade (você e a
    comitiva); as condições só quando afetam esta noite."""
    if not _pendente(a, "D3") or not getattr(g, "na_fogueira", False):
        return None
    return {"id": "D3", "texto": "**Dormir até o amanhecer**\n" + _linhas(g.linhas_descanso("fogueira")),
            "ancora": "dormir:fogueira", "entendi": True}


# As que a tela mostra quando o alvo aparece (a taverna aberta), sem segurar a fila das outras.
def contextuais(g):
    a = estado(g)
    if not a or not tutorial(g):
        return []
    return [o for o in (_d1(g, a),) if o]


# O que cada menu cumpre ao ser respondido: a ocasião passou (o quadro apareceu e a pessoa seguiu). Os talentos
# também: o quadro aparece uma vez (o ★ do atalho continua avisando) e não segura os outros na fila.
PASSA_NO_MENU = ("N1", "V4", "V5", "T1", "A1", "K2", "K3", "K4", "F1", "F2", "F3", "D2")


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
    if oid in ("V3", "V4", "T1", "N1", "A1", "K2", "K4", "SF", "S-", "S+", "F1", "F2", "D1", "D3") or oid in APRESENTACAO:
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
            ("V2", "Vila", "O **Templo** devolve a vida toda; o preço depende da vida que falta"
                           + (" (o primeiro atendimento é grátis)" if g.templo_gratis() else "") + ". Dormir na **Taverna** "
                           f"devolve {TODO.get(r, r)} e {round(bal.TAVERNA_VIDA * 100)}% da vida (menos, com fome)."),
            ("V3", "Estrada", "Cada amanhecer come 1 provisão sua e 1 de cada companheiro, na vila ou fora. O Mercado "
                              "vende; dormindo na Taverna, nenhuma provisão é consumida."),
            ("V4", "Comitiva", "**Comitiva**, na barra de baixo, abre quem anda com você: conversar, ver a confiança "
                               "e mandar para o acampamento."),
            ("V5", "Estrada", "**Explorar a região** gasta um período: luta, achado, alguém pelo caminho ou nada."),
            ("E1", "Herói", "No item achado, **Na troca** mostra o que muda (▲ ganha, ▼ perde). **Equipar** troca; "
                            "**Guardar** leva para a mochila."),
            ("T1", "Herói", "**Talentos**, na barra de baixo, abre a árvore quando há ponto para gastar."),
            ("N1", "Estrada", f"À noite, os inimigos vêm {bal.NOITE_NIVEL} nível acima e batem mais forte, com ou sem "
                              "tocha. Sem tocha no escuro, a surpresa fica mais provável (nas salas da capela, certa)."),
            ("F1", "Ferimentos", "Ferimentos ficam depois da luta (o sangramento, não) e reduzem a vida máxima, o "
                                 f"{r} máximo ou atributos até sarar: depois de alguns dias de descanso (a cama conta "
                                 "dobrado; com fome, não saram), ou na hora, na **Curandeira**. A infecção não sara com "
                                 "descanso: só com unguento ou na Curandeira."),
            ("F2", "Ferimentos", "A bandagem enfaixa uma ferida aberta (corte, mordida, queimadura), a primeira da "
                                 "lista, e a protege contra infecção. Não recupera vida nem cura infecção."),
            ("F3", "Vila", "A **Curandeira** trata ferimentos; o **Templo** recupera vida."
                           + (" O primeiro tratamento é grátis." if curandeira_gratis(g) else "")),
            ("D1", "Descanso", "Dormir na **Taverna** vai até o amanhecer, devolve parte da vida e todo o recurso; nenhuma "
                               "provisão é consumida."),
            ("D3", "Descanso", "**Acampar** e dormir na fogueira vai até o amanhecer, devolve parte da vida e do recurso e "
                               "come provisões. Com fome, a vida volta menos e os ferimentos não saram."),
            ("A0", "Apresentação", "Enquanto o texto aparece, um clique mostra o texto inteiro; **Continuar** avança."),
            ("A1", "Apresentação", "**Texto**, no topo (tecla V), ajusta a velocidade do texto."),
            ("AL", "Apresentação", "Na luta, um clique na tela acelera a animação.")):
        if oid in vistas:
            linhas.append({"grupo": grupo, "texto": texto})
    return {"ligado": tutorial(g), "linhas": linhas}


def para_tela(g):
    """O que a tela recebe no estado: a orientação de agora e a Ajuda."""
    if not g.mundo:
        return None
    return {"atual": atual(g), "apresentacao": apresentacao(g), "contextuais": contextuais(g), **ajuda(g)}


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
        o = selo_da_vez(g) if onde == "selo" else proxima(g)
        ditos = g.__dict__.setdefault("abertura_ditas", set())  # a sessão de texto: cada dica uma vez
        if o and o["id"] != "V1" and o["id"] not in ditos:
            ditos.add(o["id"])
            nome, _, resto = o["texto"].replace("**", "\"").replace("\n_", "\n").partition("\n")  # o nome, em cima
            g.dizer("Dica: " + (f"{nome}: {resto.replace(chr(10), ' ')}" if resto else nome), "cinza")
