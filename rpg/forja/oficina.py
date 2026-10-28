"""A forja (etapa 4, integrada na 1.215.0): as peças do grupo, os materiais, o reforço, a gravação, a remoção, a
transferência e a desmontagem, e o painel que a tela desenha (telas/forja.js). Tudo o que muda o jogo é conferido aqui;
a tela só pede. A especificação inteira está em roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md.

- Cada peça tem um id estável (`uid`, "p7"): a tela pede pelo id, nunca pelo nome.
- Cada pedido traz um número (`pedido`): o mesmo número de novo (clique duplo, tecla segurada) não age outra vez; uma
  confirmação traz também o que a tela mostrou (o nome, a gravação), e se isso mudou, nada acontece.
- Os materiais são pilhas do grupo (`g.materiais`), fora da bolsa, de até 99 cada, no save.
"""

from .. import comitiva, itens
from ..telemetria import registrar
from . import encanto as E
from . import regras as R

FICHA = comitiva.ficha
HEROI = FICHA.HEROI
MATS = {**R.MATERIAIS, **E.MATERIAIS}  # os fragmentos do reforço e as essências do encantamento


# ------------------------------------------------------------------ materiais do grupo
def materiais(g):
    if not isinstance(getattr(g, "materiais", None), dict):
        g.materiais = {}
    return g.materiais


def dar_material(g, chave, n, origem):
    """Materiais para o grupo: numa pilha fora da bolsa (não ocupam espaço). Com o quadro do espólio aberto, entram nele
    (nome, ícone e quantidade); senão, o aviso de sempre. Devolve quanto entrou (a pilha para em 99)."""
    m = materiais(g)
    entra = max(0, min(n, R.PILHA_MAX - m.get(chave, 0)))
    if not entra:
        g.ui.efeito(f"A pilha de {MATS[chave]['plural']} está cheia ({R.PILHA_MAX}).", "info")
        return 0
    m[chave] = m.get(chave, 0) + entra
    d = MATS[chave]
    if not g.achou(chave, d["nome"], entra):
        g.ui.efeito(f"+{entra} {d['nome'] if entra == 1 else d['plural']}", "ganho")
    registrar(g, "material", id=chave, qtd=entra, origem=origem)
    return entra


def requisito_material(chave, tem, precisa):
    """Um material que a operação consome, no formato comum das telas da forja: disponível/necessário
    ("14/2"), a falta marcada no valor e a dica que diz a ordem dos números. O ouro não entra: o preço fica no botão."""
    d = MATS[chave]
    falta = tem < precisa
    return {"id": chave, "nome": d["nome"], "icone": d["icone"], "cor": d.get("cor"), "numeral": d.get("numeral"),
            "tem": tem, "precisa": precisa, "falta": falta, "valor": f"{tem}/{precisa}",
            "dica": f"Disponível {tem} · necessário {precisa}" + (f" · faltam {precisa - tem}" if falta and precisa - tem > 1
                                                                   else " · falta 1" if falta else "")}


# ------------------------------------------------------------------ as peças do grupo
def pecas(g):
    """(item, quem, espaço): o que está no corpo de cada um (o herói e a comitiva) e na bolsa (quem None)."""
    lista = []
    for quem in FICHA.personagens(g):
        for s, it in FICHA.corpo(g, quem).items():
            if it:
                lista.append((it, quem, s))
    lista += [(it, None, None) for it in g.j.mochila]
    return lista


def dar_uid(g):
    """Cada peça ganha um id estável: o pedido da tela diz QUAL peça, e uma seleção antiga não pega outra."""
    usados = [int(it["uid"][1:]) for it, _, _ in pecas(g) if str(it.get("uid", "")).startswith("p")]
    prox = max(usados, default=0) + 1
    for it, _, _ in pecas(g):
        if "uid" not in it:
            it["uid"] = f"p{prox}"
            prox += 1


def achar(g, uid):
    return next(((it, quem, s) for it, quem, s in pecas(g) if it.get("uid") == uid), (None, None, None))


# ------------------------------------------------------------------ a ficha de cada peça para a tela
def _nome_quem(g, quem):
    return "Bolsa do grupo" if quem is None else FICHA.nome_de(g, quem)


def custo_passo(g, n):
    ouro, frag = R.custo(n)
    return g.preco(ouro), frag


def nome_linha(st, rec):
    """O nome de uma linha como a ficha escreve ("Crítico", "Roubo de vida", e o recurso de quem leva: Vigor, Mana, Foco)."""
    from rpg.entidades import nome_stat
    n = nome_stat(st, rec).lstrip("% ")
    return n[:1].upper() + n[1:]


def valor_tela(st, v):
    """O valor de uma propriedade como a tela escreve: "4,5%", "12", "3,4" (a casa só quando existe)."""
    return f"{R.fmt(v)}{'%' if st in itens.PERCENTUAIS else ''}"


def linhas_ganho(it, ganho, rec):
    """As linhas que mudam, antes → depois, na ordem da peça, prontas para a tela."""
    return [{"nome": nome_linha(st, rec), "antes": valor_tela(st, it["bonus"].get(st, 0)),
             "depois": valor_tela(st, it["bonus"].get(st, 0) + v)}
            for st, v in ganho.items() if R.limpo(v)]


def ficha_peca(g, it, quem, s):
    rec = g.j.nome_recurso if quem in (None, HEROI) else comitiva.luta.RECURSO.get(quem, g.j.nome_recurso)
    n = it.get("reforco", 0)
    t = R.tipo(it)
    tem = materiais(g).get("fragmento", 0)
    d = {"uid": it["uid"], "item": itens.ficha(it, rec), "quem": quem, "onde": _nome_quem(g, quem), "espaco": s,
         "reforco": n, "limite": R.LIMITE, "tipo": t,
         "acumulado": R.texto_ganho(R.ganho_total(it, n)) if n else ""}
    # todas as propriedades da peça, na ordem dela; as que o reforço faz crescer vêm marcadas (a ficha não esconde nada)
    cresce = {st for st, _, _ in R.linhas(it)}
    d["propriedades"] = [{"stat": st, "nome": nome_linha(st, rec), "valor": v, "texto": valor_tela(st, v),
                          "pct": st in itens.PERCENTUAIS, "cresce": st in cresce}
                         for st, v in it["bonus"].items() if v]
    d["efeito"] = (itens.unico_de(it) or {}).get("efeito")
    # o reforço é um serviço sobre a peça: classe e nível restringem vestir, não reforçar. A prévia vem da
    # própria peça, com ou sem alguém do grupo que a use.
    if not t:
        d["sem_reforco"] = R.motivo_sem_reforco(it)
    elif n >= R.LIMITE:
        d["no_limite"] = True
    elif R.motivo_sem_ganho(it):
        d["sem_reforco"] = R.motivo_sem_ganho(it)
    else:
        ouro, frag = custo_passo(g, n)
        longe = FICHA.motivo_indisponivel(g, quem) if quem not in (None, HEROI) else None
        falta = [x for x in (f"{ouro - g.j.ouro} de ouro" if g.j.ouro < ouro else None,
                             f"{frag - tem} {'Fragmento' if frag - tem == 1 else 'Fragmentos'}"
                             if tem < frag else None) if x]
        # "Faltam 2 Fragmentos", "Falta 1 Fragmento", "Faltam 40 de ouro e 2 Fragmentos": a frase inteira, sem parágrafo
        plural = len(falta) > 1 or (falta and not falta[0].startswith("1 "))
        motivo = longe or (f"{'Faltam' if plural else 'Falta'} {' e '.join(falta)}" if falta else None)
        # a peça inteira melhora (todas as linhas): um passo só
        ganho = R.proximo(it)
        ch = R.chance(it, n + 1)
        d["passos"] = [{"veio": None, "rotulo": None, "chance": ch, "falha": None if ch >= 100 else max(0, n - 1),
                        "ganho": R.texto_ganho(ganho), "linhas": linhas_ganho(it, ganho, rec), "ouro": ouro,
                        "fragmentos": frag, "tem": tem, "ouro_tem": g.j.ouro, "falta": falta, "motivo": motivo,
                        # o que a tentativa consome além do ouro (que fica no botão): disponível/necessário
                        "requer": [requisito_material("fragmento", tem, frag)]}]
    if quem is None:
        investido, propria = R.desmontar_rende(it)
        total = investido + propria
        cheia = materiais(g).get("fragmento", 0) + total > R.PILHA_MAX
        d["desmontar"] = {"investimento": investido, "da_peca": propria, "total": total,
                          "motivo": ("Não rende material." if not total else
                                     f"Fragmentos no máximo ({R.PILHA_MAX})."
                                     if cheia else None)}
        d["venda"] = it.get("preco", 0) // 2
    else:
        d["desmontar"] = {"equipada": True}
    d["aba"] = quem or "bolsa"
    d["encantos"] = [encanto_tela(k) for k in it.get("encantos") or []]
    d["efeitos"] = efeitos_peca(it)
    d["requisito"] = E.requisito(it)
    d["transferir"] = transferencias(g, it)
    essencias = [{**encanto_tela(E.chave(k, t)), "compativel": E.compativel(k),
                  "qtd": materiais(g).get(E.material(k, t), 0), "motivo": E.motivo(it, E.chave(k, t)),
                  "requer": requisito_material(E.material(k, t), materiais(g).get(E.material(k, t), 0), 1)}
                 for k in E.ORDEM for t in E.TIERS]
    # a prévia de cada essência compatível em cada sulco ("1|brasa:2"), calculada aqui (a tela só desenha)
    prev = {f"{s_}|{x['id']}": previsao(g, it, quem, s_, x["id"]) for s_ in range(len(it.get("encantos") or []))
            for x in essencias if not x["motivo"]} if E.tipo(it) else {}
    # a prévia da remoção de cada sulco ocupado ("2": o que muda ao deixá-lo vazio)
    rem = {str(s_): previsao_remocao(g, it, quem, s_) for s_, k in enumerate(it.get("encantos") or []) if k} if E.tipo(it) else {}
    d["encantar"] = {"motivo": E.motivo(it), "dono": FICHA.nome_de(g, quem) if quem else None,
                     "nivel": nivel_de(g, quem) if quem else None, "essencias": essencias, "previsao": prev, "remocao": rem}
    return d


def encanto_tela(k):
    """Uma gravação (ou uma essência a gravar) para a tela: o nome com o tier, a cor, o símbolo, o requisito e o efeito
    com o valor deste tier (Brasa II: 28% de chance)."""
    e, t = E.ler(k)
    if not e:
        return None
    d = E.ESSENCIAS[e]
    v = E.valor_tier(e, t)
    ef, lim = E.texto(e, v)
    return {"id": k, "essencia": e, "tier": t, "numeral": E.NUMERAL[t], "nome": d["nome"], "titulo": E.nome(e, t),
            "cor": d["cor"], "icone": d["icone"], "efeito": ef, "limite": lim, "fx": d["fx"], "requisito": E.REQUISITO[t],
            "medida": d["medida"][0], "valor": E.com_unidade(e, v), "nota": d["nota"]}


def efeitos_peca(it):
    """O que a peça fornece, um efeito por essência (as repetições somadas na propriedade que cresce, até o limite do
    efeito): [{id, nome, cor, efeito, limite, valor, excede, teto}]. É a descrição da peça, igual na bolsa e no corpo."""
    soma = E.soma_peca(it)
    out = []
    for e in E.ORDEM:
        if e not in soma:
            continue
        v = E.limitado(e, soma[e])
        ef, lim = E.texto(e, v)
        out.append({"id": e, "nome": E.ESSENCIAS[e]["nome"], "cor": E.ESSENCIAS[e]["cor"], "efeito": ef, "limite": lim,
                    "valor": E.com_unidade(e, v), "excede": soma[e] > E.ESSENCIAS[e]["limite"],
                    "teto": E.com_unidade(e, E.ESSENCIAS[e]["limite"]), "nota": E.ESSENCIAS[e]["nota"]})
    return out


def nivel_de(g, quem):
    """O nível de quem vai vestir: o herói e os companheiros (no jogo, os companheiros crescem com o nível do herói:
    comitiva.grupo.atributos)."""
    return g.j.nivel


def motivo_requisito(g, quem, it, encantos=None):
    """"Requer nível 9." quando quem não tem o nível que a peça (com estas gravações) pede; None quando tem."""
    req = E.requisito(it, encantos)
    return f"Requer nível {req}." if nivel_de(g, quem) < req else None


def _fmt(e, v):
    return E.com_unidade(e, v) if v else "—"


def previsao(g, it, quem, sulco, k):
    """O que muda ao gravar `k` no `sulco` da peça, pronto para a tela: as linhas que mudam (a peça; quem veste, só
    quando outra peça dele também soma ou o limite corta), a troca, o requisito e o bloqueio. Os números são do motor."""
    e, t = E.ler(k)
    antes_k = it["encantos"][sulco]
    if antes_k == k:
        return {"bloqueio": "Já gravado.", "linhas": [], "requisito": E.REQUISITO[t]}
    novos = list(it["encantos"])
    novos[sulco] = k
    ea, _ = E.ler(antes_k)
    afetadas = [e] + ([ea] if ea and ea != e else [])
    p_antes, p_depois = E.soma_peca(it), E.soma_peca({"encantos": novos})
    linhas, aviso = [], None
    # na prévia da peça escolhida, o nome do efeito basta ("Carrasco", não "Carrasco nesta peça"); o total de quem
    # veste só aparece quando explica uma consequência (o limite que corta a soma); o limite aparece no próprio valor
    # final ("60% · limite"); só quando nada muda (já estava no limite) uma nota curta diz isso.
    def valor(x, v, cortou):
        return f"{_fmt(x, v)} · limite" if cortou else _fmt(x, v)
    for x in afetadas:
        a, b = E.limitado(x, p_antes.get(x, 0)), E.limitado(x, p_depois.get(x, 0))
        if a != b:
            linhas.append({"rotulo": E.ESSENCIAS[x]["nome"], "antes": _fmt(x, a),
                           "depois": valor(x, b, p_depois.get(x, 0) > E.ESSENCIAS[x]["limite"]), "melhor": b > a})
    if quem is not None:
        corpo = FICHA.corpo(g, quem)
        depois = {s: ({**x, "encantos": novos} if x is it else x) for s, x in corpo.items()}
        q_antes, q_depois = E.soma_equip(corpo), E.soma_equip(depois)
        for x in afetadas:
            lim = E.ESSENCIAS[x]["limite"]
            if q_depois.get(x, 0) <= lim:
                continue
            a, b = E.limitado(x, q_antes.get(x, 0)), E.limitado(x, q_depois.get(x, 0))
            if q_antes.get(x, 0) != p_antes.get(x, 0) and a != b:  # outra peça dele também soma: o total esbarra no limite
                linhas.append({"rotulo": f"Total em {FICHA.nome_de(g, quem)}", "antes": _fmt(x, a), "depois": valor(x, b, True),
                               "melhor": b > a})
            if a == b:
                aviso = f"{E.ESSENCIAS[x]['nome']} já está no limite ({E.com_unidade(x, lim)})"
    elif p_depois.get(e, 0) > E.ESSENCIAS[e]["limite"] and not linhas:
        aviso = f"{E.ESSENCIAS[e]['nome']} já está no limite ({E.com_unidade(e, E.ESSENCIAS[e]['limite'])})"
    req = E.requisito(it, novos)
    bloqueio, nivel = None, None
    if quem is not None:  # vestida: o nível de quem veste é requisito da operação
        falta = nivel_de(g, quem) < req
        bloqueio = f"Requer nível {req}" if falta else None
        if req > E.requisito(it):
            nivel = {"id": "nivel", "valor": f"Nível {req}", "falta": falta,
                     "dica": f"{FICHA.nome_de(g, quem)} está no nível {nivel_de(g, quem)}." if falta
                     else f"{FICHA.nome_de(g, quem)} já está no nível {nivel_de(g, quem)}."}
    nota = None
    if quem is None and req > E.requisito(it):  # na bolsa, a consequência para depois (não impede a gravação)
        nota = f"A peça passa a requerer nível {req}"
    return {"linhas": linhas, "aviso": aviso, "nota": nota, "requisito": E.REQUISITO[t], "requisito_peca": req,
            "bloqueio": bloqueio, "nivel": nivel}


def previsao_remocao(g, it, quem, sulco):
    """O que muda ao remover a gravação do `sulco`, pronto para a tela: o valor do efeito na peça e, quando outra
    peça de quem veste também soma e o limite cortava, o total dele; o requisito novo da peça, quando cai."""
    k = it["encantos"][sulco]
    e, _ = E.ler(k)
    if not e:
        return None
    novos = list(it["encantos"])
    novos[sulco] = None
    a, b = E.limitado(e, E.soma_peca(it).get(e, 0)), E.limitado(e, E.soma_peca({"encantos": novos}).get(e, 0))
    linhas = [{"rotulo": E.ESSENCIAS[e]["nome"], "antes": _fmt(e, a), "depois": _fmt(e, b), "melhor": False}] if a != b else []
    if quem is not None:
        corpo = FICHA.corpo(g, quem)
        depois = {s_: ({**x, "encantos": novos} if x is it else x) for s_, x in corpo.items()}
        q_antes, q_depois = E.soma_equip(corpo).get(e, 0), E.soma_equip(depois).get(e, 0)
        qa, qb = E.limitado(e, q_antes), E.limitado(e, q_depois)
        if q_antes != E.soma_peca(it).get(e, 0) and qa != qb:  # outra peça dele também soma: o total que ele fica
            linhas.append({"rotulo": f"Total em {FICHA.nome_de(g, quem)}", "antes": _fmt(e, qa), "depois": _fmt(e, qb), "melhor": False})
        elif q_antes != E.soma_peca(it).get(e, 0) and qa == qb:  # o limite cortava: quem veste não perde nada
            linhas.append({"rotulo": f"Total em {FICHA.nome_de(g, quem)}", "antes": _fmt(e, qa), "depois": f"{_fmt(e, qb)} · limite", "melhor": False})
    req_antes, req = E.requisito(it), E.requisito(it, novos)
    return {"linhas": linhas, "nota": f"A peça passa a requerer nível {req}" if req < req_antes else None,
            "requisito_peca": req, "sai": encanto_tela(k)}


def remover_encanto(g, uid, sulco, pedido=None, remove=None):
    """Remove a gravação do `sulco`: o sulco fica vazio, a essência se perde, nada volta e não custa
    nada. `remove`: a gravação que a tela mostrou naquele sulco; se ela mudou desde então (outra remoção, uma gravação),
    nada acontece. Um pedido repetido (clique duplo, tecla segurada) não remove de novo."""
    if pedido is not None and pedido == getattr(g, "forja_pedido", None):
        return False, None
    it, quem, _ = achar(g, uid)
    if it is None:
        return False, "Essa peça não está mais com o grupo."
    if not isinstance(sulco, int) or not 0 <= sulco < len(it.get("encantos") or []):
        return False, "Esse sulco não existe nesta peça."
    antes = it["encantos"][sulco]
    if not antes:
        return False, "O sulco já está vazio."
    if antes != remove:
        return False, "A gravação da peça mudou. Escolha de novo."
    g.forja_pedido = pedido
    E.gravar(it, None, sulco)
    if quem:
        FICHA.atualizar(g, quem)
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "remove", "uid": uid, "sulco": sulco, "de": encanto_tela(antes)}
    registrar(g, "remover_encanto", item=it["nome"], essencia=antes, sulco=sulco, em=quem or "bolsa")
    return True, f"Removido: {E.nome(*E.ler(antes))} · {it['nome']}"


def dono_de(g, it):
    """Quem veste esta peça (o id do personagem), ou None (bolsa ou fora do grupo). Pela identidade, não pelo nome."""
    for q in FICHA.personagens(g):
        if any(x is it for x in FICHA.corpo(g, q).values()):
            return q
    return None


def transferencias(g, origem):
    """Os destinos possíveis de uma transferência a partir desta peça: cada peça do grupo do mesmo tipo e raridade, com
    o resultado das duas e o preço, ou o motivo de não poder."""
    if not origem.get("reforco"):
        return {"motivo": "Esta peça não tem reforço para transferir.", "destinos": []}
    lista = []
    for it, quem, s in pecas(g):
        if it is origem or R.tipo(it) != R.tipo(origem) or it.get("raridade") != origem.get("raridade"):
            continue
        novo, motivo = R.transferencia(origem, it)
        lista.append({"uid": it["uid"], "nome": it["nome"], "onde": _nome_quem(g, quem), "de": it.get("reforco", 0),
                      "novo": novo, "ouro": g.preco(R.custo_transferencia(novo)) if novo else None, "motivo": motivo,
                      "icone": itens.icone_de(it), "raridade": it.get("raridade", "comum")})
    return {"motivo": None if lista else "Nenhuma peça do mesmo espaço e da mesma raridade no grupo.", "destinos": lista}


def proximo_id(g, consumir=True):
    """O número do próximo resultado da forja: só cresce (a tela reconhece um resultado novo pelo número; recomeçando
    do 1, ela tomaria o novo por um já visto e pularia a cena)."""
    n = max(getattr(g, "forja_seq", 0), (getattr(g, "forja_ultimo", None) or {}).get("id", 0)) + 1
    if consumir:
        g.forja_seq = n
    return n


def painel(g):
    dar_uid(g)
    m = materiais(g)
    abas = [{"id": q, "nome": FICHA.nome_de(g, q), "retrato": g.j.classe if q == HEROI else q}
            for q in FICHA.personagens(g)] + [{"id": "bolsa", "nome": "Bolsa", "retrato": None}]
    return {"ouro": g.j.ouro, "limite": R.LIMITE, "abas": abas, "ultimo": getattr(g, "forja_ultimo", None),
            "proximo_id": proximo_id(g, consumir=False),
            "materiais": [{"id": k, **MATS[k], "qtd": m.get(k, 0)} for k in MATS],
            "custo_encanto": g.preco(E.CUSTO_OURO),
            "pecas": [ficha_peca(g, it, quem, s) for it, quem, s in pecas(g)]}


# ------------------------------------------------------------------ as ações (a tela pede; tudo é conferido aqui)
def aplicar_nivel(it, n):
    """Leva a peça ao nível +n: cada linha fica com a da peça de antes do primeiro reforço mais o ganho de +n (subindo
    ou caindo), e o nome e o preço acompanham. Contado sempre da peça original: uma regra de ganho nova vale inteira
    também para a peça que já tinha níveis."""
    base, ganho = it.setdefault("bonus_base", dict(it["bonus"])), R.ganho_total(it, n)
    for st in set(base) | set(ganho) | set(it["bonus"]):
        v = R.limpo(base.get(st, 0) + ganho.get(st, 0))
        if v:
            it["bonus"][st] = v
        else:
            it["bonus"].pop(st, None)
    it["reforco"] = n
    it["preco"] = R.preco_com_reforco(it)
    base = it["nome"].split(" +")[0]
    it["nome"] = f"{base} +{n}" if n else base


def reforcar(g, uid, pedido=None):
    """Uma tentativa, resolvida uma única vez. `pedido`: o id que a tela manda; o mesmo id de novo não tenta outra
    vez."""
    if pedido is not None and pedido == getattr(g, "forja_pedido", None):
        return False, None  # repetição da mesma entrada: nada
    it, quem, s = achar(g, uid)
    if it is None:
        return False, "Essa peça não está mais com o grupo."
    t, n = R.tipo(it), it.get("reforco", 0)
    if not t:
        return False, R.motivo_sem_reforco(it)
    if n >= R.LIMITE:
        return False, f"{it['nome']} já está no limite (+{R.LIMITE})."
    if R.motivo_sem_ganho(it):  # um sucesso que não melhora nada não é oferecido nem cobrado
        return False, R.motivo_sem_ganho(it)
    if quem not in (None, HEROI) and FICHA.motivo_indisponivel(g, quem):
        return False, FICHA.motivo_indisponivel(g, quem)
    ouro, frag = custo_passo(g, n)
    tem = materiais(g).get("fragmento", 0)
    if g.j.ouro < ouro or tem < frag:
        return False, "Faltam recursos para este reforço."
    g.forja_pedido = pedido
    it.setdefault("bonus_base", dict(it["bonus"]))
    it.setdefault("preco_base", it.get("preco", 0))
    # cobra a tentativa (o custo informado, qualquer que seja o resultado); o aviso de ouro do jogo não cobre a janela
    efeito, g.ui.efeito = g.ui.efeito, (lambda *a, **k: None)
    try:
        g.perder_ouro(ouro, destino="ferreiro")
    finally:
        g.ui.efeito = efeito
    materiais(g)["fragmento"] = tem - frag
    chance = R.chance(it, n + 1)
    sucesso = True if n == 0 else g.rng.random() * 100 < chance  # o primeiro é garantido
    antes = dict(it["bonus"])
    para = n + 1 if sucesso else max(0, n - 1)
    aplicar_nivel(it, para)
    rec = g.j.nome_recurso if quem in (None, HEROI) else comitiva.luta.RECURSO.get(quem, g.j.nome_recurso)
    linhas = linhas_ganho({"bonus": antes}, {st: it["bonus"].get(st, 0) - antes.get(st, 0) for st in it["bonus"]}, rec)
    gasto = it.setdefault("reforco_gasto", {"ouro": 0, "fragmento": 0, "tentativas": 0})
    gasto["ouro"] += ouro
    gasto["fragmento"] += frag
    gasto["tentativas"] = gasto.get("tentativas", 0) + 1
    if quem:
        FICHA.atualizar(g, quem)
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "reforco", "uid": uid,
                      "sucesso": sucesso, "de": n, "para": para, "chance": chance, "linhas": linhas}
    registrar(g, "ferreiro", item=it["nome"], sucesso=sucesso, de=n, para=para, chance=chance, ouro=ouro,
              fragmentos=frag, em=quem or "bolsa")
    return True, (f"Reforço bem-sucedido · +{para}" if sucesso else f"Reforço falhou · +{n} → +{para}")


def desmontar(g, uid, nome):
    """A peça sai da bolsa e os fragmentos entram. `nome`: o nome que a tela mostrou na confirmação; se a peça com
    esse id não tem mais esse nome (outra seleção, outra peça), nada acontece."""
    it, quem, _ = achar(g, uid)
    if it is None or quem is not None:
        return False, "Só se desmonta uma peça da bolsa." if it else "Essa peça não está mais na bolsa."
    if nome not in (it["nome"], itens.rotulo(it)):  # a tela mostra o rótulo (o único vem com ★ e o tipo)
        return False, "A peça mudou desde a confirmação. Escolha de novo."
    investido, propria = R.desmontar_rende(it)
    total = investido + propria
    if not total:
        return False, "Não rende material."
    if materiais(g).get("fragmento", 0) + total > R.PILHA_MAX:
        return False, f"Fragmentos no máximo ({R.PILHA_MAX})."
    g.j.mochila.remove(it)
    materiais(g)["fragmento"] = materiais(g).get("fragmento", 0) + total
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "desmonte", "nome": it["nome"],
                      "total": total}
    registrar(g, "desmontar", item=it["nome"], fragmentos=total, investimento=investido, da_peca=propria)
    return True, f"Desmontado: {it['nome']} · +{total} {'Fragmento' if total == 1 else 'Fragmentos'} de Têmpera"


def encantar(g, uid, essencia, sulco=0, pedido=None, substitui=None):
    """Grava `essencia` no `sulco` da peça, uma vez por pedido. `substitui`: a gravação que a tela mostrou naquele sulco
    (None se vazio); se ela mudou desde então, nada acontece. Cobra 1 essência e o ouro; nunca falha."""
    if pedido is not None and pedido == getattr(g, "forja_pedido", None):
        return False, None
    it, quem, _ = achar(g, uid)
    if it is None:
        return False, "Essa peça não está mais com o grupo."
    if not E.ler(essencia)[0]:
        return False, "Escolha uma essência."
    if not isinstance(sulco, int):
        return False, "Escolha um sulco."
    motivo = E.motivo(it, essencia, sulco)
    if motivo:
        return False, motivo
    if (it["encantos"][sulco] or None) != (substitui or None):
        return False, "A gravação da peça mudou. Escolha de novo."
    if it["encantos"][sulco] == essencia:  # a mesma essência no mesmo tier: nada mudaria (sem cobrança)
        return False, "Já gravado."
    if quem is not None:  # vestida: a gravação não pode deixar a peça acima do nível de quem a usa
        bloqueio = previsao(g, it, quem, sulco, essencia)["bloqueio"]
        if bloqueio:
            return False, bloqueio
    mat, ouro = E.material(*E.ler(essencia)), g.preco(E.CUSTO_OURO)
    if materiais(g).get(mat, 0) < 1 or g.j.ouro < ouro:
        return False, "Faltam recursos para esta gravação."
    g.forja_pedido = pedido
    efeito, g.ui.efeito = g.ui.efeito, (lambda *a, **k: None)
    try:
        g.perder_ouro(ouro, destino="ferreiro")
    finally:
        g.ui.efeito = efeito
    materiais(g)[mat] -= 1
    antes = E.gravar(it, essencia, sulco)
    if quem:
        FICHA.atualizar(g, quem)
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "encanto", "uid": uid,
                      "sulco": sulco, "de": encanto_tela(antes), "para": encanto_tela(essencia)}
    registrar(g, "encantar", item=it["nome"], essencia=essencia, sulco=sulco, substituiu=antes, ouro=ouro, em=quem or "bolsa")
    return True, f"Gravado: {E.nome(*E.ler(essencia))} · {it['nome']}"


def transferir(g, origem_uid, destino_uid, pedido=None):
    """Transfere o reforço (garantido): a origem fica +0 (conserva o resto: base, afixos, sulcos e gravações); o destino
    recebe o nível da origem menos 2, no lugar do dele. Cobra o ouro uma vez por pedido."""
    if pedido is not None and pedido == getattr(g, "forja_pedido", None):
        return False, None
    o, qo, _ = achar(g, origem_uid)
    dd, qd, _ = achar(g, destino_uid)
    if o is None or dd is None:
        return False, "A peça não está mais com o grupo."
    novo, motivo = R.transferencia(o, dd)
    if motivo:
        return False, motivo
    ouro = g.preco(R.custo_transferencia(novo))
    if g.j.ouro < ouro:
        return False, f"Faltam {ouro - g.j.ouro} de ouro."
    g.forja_pedido = pedido
    efeito, g.ui.efeito = g.ui.efeito, (lambda *a, **k: None)
    try:
        g.perder_ouro(ouro, destino="ferreiro")
    finally:
        g.ui.efeito = efeito
    de_o, de_d = o.get("reforco", 0), dd.get("reforco", 0)
    for it in (o, dd):
        it.setdefault("bonus_base", dict(it["bonus"]))
        it.setdefault("preco_base", it.get("preco", 0))
    aplicar_nivel(o, 0)
    aplicar_nivel(dd, novo)
    for q in {qo, qd} - {None}:
        FICHA.atualizar(g, q)
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "transfere",
                      "origem": origem_uid, "destino": destino_uid, "de_origem": de_o, "de_destino": de_d, "novo": novo,
                      "ouro": ouro}
    registrar(g, "transferir", origem=o["nome"], destino=dd["nome"], de_origem=de_o, de_destino=de_d, novo=novo, ouro=ouro)
    return True, f"Transferido: {dd['nome']} · +{novo}"


# ------------------------------------------------------------------ ligar ao jogo, só nesta execução
def com_sulcos(it):
    if it and E.tipo(it):
        E.sortear_sulcos(it)
    return it


def sulcos_do_grupo(g):
    """As peças do grupo que ainda não têm sulcos (as que vieram de fora da criação de equipamento): os delas, uma vez."""
    for it, _, _ in pecas(g):
        com_sulcos(it)


def descrever_bonus(bonus, recurso=None):
    """'+3 Defesa, +4,5% Crítico': a casa decimal (do reforço) em vírgula, só quando existe."""
    from rpg.entidades import nome_stat
    return ", ".join(f"{'+' if v >= 0 else ''}{R.fmt(v)}{'%' if k in itens.PERCENTUAIS else ''} {nome_stat(k, recurso)}"
                     for k, v in bonus.items())


# ------------------------------------------------------------------ de onde vêm os materiais (as chances são provisórias)
# a essência que cada criatura deixa: a fonte identificável de cada efeito (quem quer Geada caça lobos gélidos e afogados)
ESSENCIA_DA_FAMILIA = {
    "cao_infernal": "brasa", "cultista": "brasa", "caido": "brasa", "xama_caido": "brasa",
    "bandido": "carrasco", "mercenario": "carrasco", "cavaleiro_sombrio": "carrasco", "carnical": "carrasco",
    "espectro": "eco", "bruxa_brejo": "eco", "cria_vazio": "eco", "harpia": "eco",
    "golem": "vigilia", "ent_jovem": "vigilia", "troll": "vigilia", "esqueleto": "vigilia",
    "javali": "revide", "grifo": "revide", "abominacao": "revide", "rato": "revide", "aranha": "revide",
    "lobo_gelido": "geada", "afogado": "geada", "sapo": "geada", "sanguessuga": "geada", "lobo": "geada",
}


def tier_do_nivel(nivel):
    """O tier pelo nível do conteúdo: I até o 4, II do 5 ao 8, III do 9 em diante."""
    return 1 if nivel < 5 else 2 if nivel < 9 else 3


def materiais_da_luta(g, derrotados):
    """O que uma luta vencida deixa, pelo caminho real do saque: fragmentos (a luta comum às vezes, a elite mais, o chefe
    sempre) e, mais raro, a essência da criatura, do tier do nível dela (o chefe, um tier acima, sempre)."""
    if not derrotados:
        return
    chefe = any(e.chefe for e in derrotados)
    elites = sum(1 for e in derrotados if e.afixo or e.unico)
    forte = max(derrotados, key=lambda e: e.nivel)
    if chefe:
        dar_material(g, "fragmento", 2 + (forte.nivel >= 6), "chefe")
    elif g.chance(0.25 + 0.15 * elites):
        dar_material(g, "fragmento", 1, "luta")
    if chefe or g.chance(0.06 + 0.2 * elites):
        essencia = ESSENCIA_DA_FAMILIA.get(forte.familia) or g.rng.choice(E.ORDEM)
        tier = min(3, tier_do_nivel(forte.nivel) + chefe)
        dar_material(g, E.material(essencia, tier), 1, "chefe" if chefe else "luta")


# ------------------------------------------------------------------ o serviço
def forja(g):
    """O ferreiro: a oficina no quadro de cima e, no balcão, a forja (telas/forja.js). Cada pedido da tela chega como
    uma resposta ao menu, com a operação; o motor confere e resolve, e a tela mostra o resultado (g.forja_ultimo) no
    desenho seguinte. Sem a tela gráfica, só o reforço, numa lista (forja_em_texto)."""
    from ..sistemas.servicos import cena_forja
    while True:
        # o painel é calculado antes de a cena ser anunciada: a cena nova limpa a página, e com o cálculo no meio o
        # navegador chegava a pintar a oficina sem a janela (uma piscada a cada pedido)
        dados = painel(g)
        g.ui.cena("A forja", g.loc["nome"], "menu")
        g.ui.painel("cena", cena_forja())
        if not g.ui.painel("forja", dados):
            forja_em_texto(g)
            return
        esc = g.menu("", [("Pedido à forja", "forja", {"forja": True}), ("Voltar", "voltar", {"voltar": True, "lugar": True})])
        if esc == "voltar":
            return
        d = getattr(g.ui, "extra_resposta", None) or {}
        op = d.get("op")
        if op == "reforcar":
            ok, texto = reforcar(g, d.get("uid"), d.get("pedido"))
        elif op == "desmontar" and d.get("confirmar") is True:
            ok, texto = desmontar(g, d.get("uid"), d.get("nome"))
        elif op == "encantar":
            ok, texto = encantar(g, d.get("uid"), d.get("essencia"), d.get("sulco"), d.get("pedido"), d.get("substitui"))
        elif op == "remover_encanto":
            ok, texto = remover_encanto(g, d.get("uid"), d.get("sulco"), d.get("pedido"), d.get("remove"))
        elif op == "transferir" and d.get("confirmar") is True:
            ok, texto = transferir(g, d.get("origem"), d.get("destino"), d.get("pedido"))
        else:
            continue
        if texto is None:  # o mesmo pedido de novo: nada
            continue
        if not ok:  # o sucesso, a própria janela mostra
            g.ui.efeito(texto, "info")


def forja_em_texto(g):
    """A forja sem a tela gráfica: o reforço das peças do grupo, numa lista com a chance e o custo. A gravação, a
    remoção, a transferência e a desmontagem precisam da tela gráfica."""
    g.dizer("O ferreiro, um homem sem dois dedos, cospe na forja. \"Ouro primeiro.\" Gravar, transferir e desmontar "
            "só na tela gráfica.", "cinza")
    while True:
        dar_uid(g)
        tem = materiais(g).get("fragmento", 0)
        opcoes = []
        for it, quem, _ in pecas(g):
            n = it.get("reforco", 0)
            if not R.tipo(it) or n >= R.LIMITE or R.motivo_sem_ganho(it):
                continue
            ouro, frag = custo_passo(g, n)
            opcoes.append((f"{itens.rotulo(it)} ({_nome_quem(g, quem)}) +{n} → +{n + 1}: {R.chance(it, n + 1)}% · "
                           f"{ouro} de ouro e {frag} {'Fragmento' if frag == 1 else 'Fragmentos'}", it["uid"]))
        esc = g.menu(f"Reforçar (ouro {g.j.ouro}, Fragmentos de Têmpera {tem})", opcoes + [("Voltar", "voltar")])
        if esc in (None, "voltar"):
            return
        ok, texto = reforcar(g, esc)
        if texto:
            g.dizer(texto, "verde" if ok and texto.startswith("Reforço bem") else "amarelo" if ok else "vermelho")


def materiais_tela(g):
    """A seção Materiais do Inventário: o Fragmento de Têmpera sempre e as essências que o grupo tem."""
    m = materiais(g)
    return [{"id": k, "nome": d["nome"], "plural": d["plural"], "icone": d["icone"], "qtd": m.get(k, 0), "desc": d["desc"],
             "fontes": d["fontes"], "numeral": d.get("numeral"), "cor": d.get("cor"), "requisito": d.get("requisito", 1)}
            for k, d in MATS.items() if k in R.MATERIAIS or m.get(k)]
