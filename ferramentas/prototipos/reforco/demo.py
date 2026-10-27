"""A demonstração jogável do reforço, dos materiais e da desmontagem (protótipo; roadmapIDEIAS/25, seção 5).

    python ferramentas/prototipos/reforco/demo.py        (ou dois cliques em demo.bat)

Sobe o jogo de verdade num save temporário (uma pasta nova a cada vez; os saves pessoais não são lidos nem tocados),
no Vau, com o herói e a comitiva, e troca só nesta execução (`ativar`) a forja, o espólio do baú, a venda de peça
reforçada e a ficha do inventário pelas regras de regras.py. O jogo de produção não importa esta pasta.
"""

import os
import random
import sys
import tempfile
import threading
import time
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", "..", ".."))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import encanto as E  # noqa: E402
import regras as R  # noqa: E402
from rpg import balanceamento as bal  # noqa: E402
from rpg import comitiva, itens  # noqa: E402
from rpg.classes import CLASSES  # noqa: E402
from rpg.combate.eficacia import mult_tracos  # noqa: E402
from rpg.modificadores import mod  # noqa: E402
from rpg.telemetria import registrar  # noqa: E402

FICHA = comitiva.ficha
HEROI = FICHA.HEROI
MATS = {**R.MATERIAIS, **E.MATERIAIS}  # os fragmentos do reforço e as essências do encantamento (laboratório)


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


# ------------------------------------------------------------------ a comparação na luta (sem sorte, sem crítico)
def _alvo(g):
    """O mesmo alvo em todas as comparações: um Esqueleto do nível do herói, com o sorteio fixo."""
    from rpg.inimigos import criar
    return criar(random.Random(7), "esqueleto", g.j.nivel)


def numeros(g, quem):
    """Os números de luta de alguém agora: atk, poder, defesa, vida máxima, o multiplicador de dano e o ataque comum."""
    if quem == HEROI:
        j = g.j
        nome, alcance, tipo, stat, mult = CLASSES[j.classe]["ataque"]
        md = bal.DANO_HEROI * (1 + mod(j, "dano_corpo" if alcance == "corpo" else "dano_distancia"))
        return {"atk": j.atk, "poder": j.poder, "defesa": j.defesa, "max_hp": j.max_hp, "md": md,
                "ataque": (nome, mult, tipo, alcance, stat), "nome": "você"}
    m = comitiva.membro(g, quem)
    at, leal = comitiva.atributos(g, m), comitiva.lealdade(m)
    return {"atk": at["atk"] * leal, "poder": at["poder"] * leal, "defesa": at["defesa"], "max_hp": at["max_hp"],
            "md": bal.DANO_COMITIVA, "ataque": comitiva.ATAQUE[quem], "nome": comitiva.nome(quem)}


def golpe(n, alvo, stat=None, mult=None, nome=None, tipo=None, alcance=None):
    a_nome, a_mult, a_tipo, a_alcance, a_stat = n["ataque"]
    stat, mult = stat or a_stat, mult or a_mult
    tipo, alcance = tipo or a_tipo, alcance or a_alcance
    dano = n[stat] * mult * n["md"] * mult_tracos(alvo, tipo, alcance) * bal.fator_defesa(alvo.defesa)
    return nome or a_nome, round(max(1.0, dano), 1)


def recebido(n, alvo):
    return round(max(1.0, alvo.atk * bal.fator_defesa(n["defesa"], alvo.nivel)), 1)


def comparar(g, quem, mudar):
    """Antes e depois de `mudar` (uma função que altera e devolve como desfazer), nos números de quem: o golpe comum
    (ou a Lâmina Rúnica, quando o que muda é o Poder de um Guerreiro), o golpe que ele recebe e a vida máxima."""
    alvo = _alvo(g)
    antes = numeros(g, quem)
    desfazer = mudar()
    FICHA.atualizar(g, quem)
    depois = numeros(g, quem)
    desfazer()
    FICHA.atualizar(g, quem)
    linhas = []
    usa_poder = depois["poder"] != antes["poder"] and antes["ataque"][4] == "atk"
    if usa_poder and quem == HEROI and g.j.classe == "guerreiro":
        kw = dict(stat="poder", mult=1.6, nome="Lâmina Rúnica", tipo="arcano", alcance="corpo")
    else:
        kw = {}
    if depois["atk"] != antes["atk"] or depois["poder"] != antes["poder"]:
        nome, a = golpe(antes, alvo, **kw)
        _, b = golpe(depois, alvo, **kw)
        if a != b or not kw:
            quem_bate = "" if quem == HEROI else f" de {antes['nome']}"
            linhas.append({"rotulo": f"{nome}{quem_bate} no {alvo.nome}", "antes": a, "depois": b, "melhor": b > a})
        if usa_poder and not kw:
            linhas.append({"rotulo": f"Poder de {antes['nome']} (curas e magias)", "antes": R._rh(antes["poder"]),
                           "depois": R._rh(depois["poder"]), "melhor": depois["poder"] > antes["poder"]})
    if depois["defesa"] != antes["defesa"]:
        a, b = recebido(antes, alvo), recebido(depois, alvo)
        linhas.append({"rotulo": f"Golpe do {alvo.nome} em {antes['nome']}", "antes": a, "depois": b, "melhor": b < a})
    if depois["max_hp"] != antes["max_hp"]:
        linhas.append({"rotulo": f"Vida máxima de {antes['nome']}", "antes": antes["max_hp"], "depois": depois["max_hp"],
                       "melhor": depois["max_hp"] > antes["max_hp"]})
    return {"alvo": f"{alvo.nome} nível {alvo.nivel}, defesa {R._rh(alvo.defesa)}", "linhas": linhas}


def com_reforco(it, ganho):
    def mudar():
        antes = dict(it["bonus"])
        for s, v in ganho.items():
            it["bonus"][s] = it["bonus"].get(s, 0) + v

        def desfazer():
            it["bonus"].clear()
            it["bonus"].update(antes)  # exatamente como estava (sem deixar "Poder 0" na peça)
        return desfazer
    return mudar


def vestida_em(g, quem, espaco, it):
    """Vestir `it` no espaço exato (o da peça que se compara; o anel no dedo dela). Desfeito em seguida."""
    def mudar():
        eq = FICHA.corpo(g, quem)
        velho = eq[espaco]
        eq[espaco] = it

        def desfazer():
            eq[espaco] = velho
        return desfazer
    return mudar


def vestida(g, quem, it):
    """Vestir `it` no lugar do que `quem` usa no espaço dele (para comparar; desfeito em seguida)."""
    def mudar():
        eq = FICHA.corpo(g, quem)
        s = FICHA.espaco_para(g, quem, it) or itens.espacos(it["slot"])[0]
        velho = eq[s]
        eq[s] = it

        def desfazer():
            eq[s] = velho
        return desfazer
    return mudar


# ------------------------------------------------------------------ a ficha de cada peça para a tela
def _nome_quem(g, quem):
    return "Bolsa do grupo" if quem is None else FICHA.nome_de(g, quem)


def custo_passo(g, n):
    ouro, frag = R.custo(n)
    return g.preco(ouro), frag


def ninguem_usa(g, it):
    """Por que reforçar esta peça não serve a ninguém do grupo (ou None): a classe dela não é de ninguém aqui."""
    if any(not FICHA.motivo_nao_veste(g, q, it) for q in FICHA.personagens(g)):
        return None
    return f"Ninguém do grupo usa peças de {FICHA.NOME_CLASSE.get(it.get('classe'), it.get('classe'))}."


def nome_linha(st, rec):
    """O nome de uma linha como a ficha escreve ("Crítico", "Roubo de vida", e o recurso de quem leva: Vigor, Mana, Foco)."""
    from rpg.entidades import nome_stat
    n = nome_stat(st, rec).lstrip("% ")
    return n[:1].upper() + n[1:]


def linhas_ganho(it, ganho, rec):
    """As linhas que mudam, antes → depois, na ordem da peça (a de %, com o %)."""
    pct = lambda st, v: f"{v}%" if st in itens.PERCENTUAIS else v  # noqa: E731
    return [{"nome": nome_linha(st, rec), "antes": pct(st, it["bonus"].get(st, 0)), "depois": pct(st, it["bonus"].get(st, 0) + v)}
            for st, v in ganho.items() if v]


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
    d["propriedades"] = [{"stat": st, "nome": nome_linha(st, rec), "valor": v,
                          "pct": st in itens.PERCENTUAIS, "cresce": st in cresce}
                         for st, v in it["bonus"].items() if v]
    d["efeito"] = (itens.unico_de(it) or {}).get("efeito")
    if not t:
        d["sem_reforco"] = R.motivo_sem_reforco(it)
    elif ninguem_usa(g, it):
        d["sem_reforco"] = ninguem_usa(g, it)
    elif n >= R.LIMITE:
        d["no_limite"] = True
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
        d["passos"] = []
        for v in (None,):
            ganho = R.proximo(it)
            luta = comparar(g, quem, com_reforco(it, ganho)) if quem else None
            # o recurso pelo nome de quem leva a peça (Vigor, Mana, Foco), como a ficha e o resultado
            linhas = linhas_ganho(it, ganho, rec)
            ch = R.chance(it, n + 1)
            d["passos"].append({"veio": v, "rotulo": None, "chance": ch,
                                "falha": None if ch >= 100 else max(0, n - 1),
                                "ganho": R.texto_ganho(ganho), "linhas": linhas, "ouro": ouro, "fragmentos": frag,
                                "tem": tem, "ouro_tem": g.j.ouro, "falta": falta, "motivo": motivo, "luta": luta})
    if quem is None:
        investido, propria = R.desmontar_rende(it)
        total = investido + propria
        cheia = materiais(g).get("fragmento", 0) + total > R.PILHA_MAX
        d["desmontar"] = {"investimento": investido, "da_peca": propria, "total": total,
                          "motivo": ("Não rende material." if not total else
                                     f"Fragmentos no máximo ({R.PILHA_MAX})."
                                     if cheia else None)}
        d["venda"] = it.get("preco", 0) // 2
        # a substituta: vestida em cada um que pode usar, no lugar do que ele usa
        d["trocas"] = []
        for q in FICHA.personagens(g):
            if FICHA.motivo_nao_veste(g, q, it) or (q != HEROI and FICHA.motivo_indisponivel(g, q)):
                continue
            s_q = FICHA.espaco_para(g, q, it) or itens.espacos(it["slot"])[0]
            atual = FICHA.corpo(g, q)[s_q]
            c = comparar(g, q, vestida(g, q, it))
            if c["linhas"]:
                d["trocas"].append({"quem": FICHA.nome_de(g, q), "no_lugar": atual and itens.rotulo(atual), **c})
    else:
        d["desmontar"] = {"equipada": True}
        # as substitutas: as peças da bolsa que quem usa esta poderia vestir no lugar dela
        d["substitutas"] = []
        for sub in g.j.mochila:
            if sub.get("slot") != it.get("slot") or FICHA.motivo_nao_veste(g, quem, sub):
                continue
            c = comparar(g, quem, vestida_em(g, quem, s, sub))
            d["substitutas"].append({"uid": sub["uid"], "nome": itens.rotulo(sub), "item": itens.ficha(sub, rec), **c})
    d["aba"] = quem or "bolsa"
    d["encantos"] = [encanto_tela(k) for k in it.get("encantos") or []]
    d["gravacao_total"] = gravacao_total(g, quem)
    d["transferir"] = transferencias(g, it)
    d["encantar"] = {"motivo": E.motivo(it), "teto": E.TETO, "dono": FICHA.nome_de(g, quem) if quem else None,
                     "totais": E.niveis_equip(FICHA.corpo(g, quem)) if quem else {},
                     "essencias": [{**encanto_tela(E.chave(k, t)), "compativel": E.compativel(k),
                                    "qtd": materiais(g).get(E.material(k, t), 0), "motivo": E.motivo(it, E.chave(k, t))}
                                   for k in E.ORDEM for t in E.TIERS]}
    return d


def encanto_tela(k):
    """Uma gravação (ou uma essência a gravar) para a tela: o nome com o tier, a cor, o símbolo e o texto do efeito em
    cada nível de 1 ao teto (a tela escolhe pelo nível: o desta peça, o total de quem veste)."""
    e, t = E.ler(k)
    if not e:
        return None
    d = E.ESSENCIAS[e]
    ef, lim = E.texto(e, t)
    return {"id": k, "essencia": e, "tier": t, "numeral": E.NUMERAL[t], "nome": d["nome"], "titulo": E.nome(e, t),
            "cor": d["cor"], "icone": d["icone"], "efeito": ef, "limite": lim, "fx": d["fx"],
            "textos": [list(E.texto(e, n)) for n in range(1, E.TETO + 1)], "teto": E.TETO, "cresce": d["cresce"],
            "detalhe": d["ficha"]}


JOGO = [None]  # a partida desta execução (as fichas das telas precisam de quem veste a peça)


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


def gravacao_total(g, quem):
    """O nível total de cada efeito em quem: [{id, nome, cor, total, efetivo, efeito, limite}] (só as peças vestidas)."""
    if quem is None:
        return []
    soma = E.niveis_equip(FICHA.corpo(g, quem))
    out = []
    for e in E.ORDEM:
        if e in soma:
            ef, lim = E.texto(e, min(E.TETO, soma[e]))
            out.append({"id": e, "nome": E.ESSENCIAS[e]["nome"], "cor": E.ESSENCIAS[e]["cor"], "total": soma[e],
                        "efetivo": min(E.TETO, soma[e]), "efeito": ef, "limite": lim, "quem": FICHA.nome_de(g, quem)})
    return out


def painel(g):
    dar_uid(g)
    m = materiais(g)
    abas = [{"id": q, "nome": FICHA.nome_de(g, q), "retrato": g.j.classe if q == HEROI else q}
            for q in FICHA.personagens(g)] + [{"id": "bolsa", "nome": "Bolsa", "retrato": None}]
    return {"ouro": g.j.ouro, "limite": R.LIMITE, "abas": abas, "ultimo": getattr(g, "forja_ultimo", None),
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
        v = base.get(st, 0) + ganho.get(st, 0)
        if v:
            it["bonus"][st] = v
        else:
            it["bonus"].pop(st, None)
    it["reforco"] = n
    it["preco"] = R.preco_com_reforco(it)
    base = it["nome"].split(" +")[0]
    it["nome"] = f"{base} +{n}" if n else base


def reforcar(g, uid, veio=None, pedido=None, teste=None):
    """Uma tentativa, resolvida uma única vez (`veio`: ignorado desde a 12ª versão; a peça inteira melhora). `pedido`: o id que a tela manda; o mesmo id de novo não tenta outra vez.
    `teste`: "sucesso" ou "falha" forçados (só os casos de teste da demonstração; o +1 continua garantido)."""
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
    if ninguem_usa(g, it):
        return False, ninguem_usa(g, it)
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
    if n == 0:
        sucesso = True  # o primeiro é garantido, até nos casos de teste
    elif teste in ("sucesso", "falha"):
        sucesso = teste == "sucesso"
    else:
        sucesso = g.rng.random() * 100 < chance
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
    g.forja_ultimo = {"id": (getattr(g, "forja_ultimo", None) or {}).get("id", 0) + 1, "tipo": "reforco", "uid": uid,
                      "sucesso": sucesso, "de": n, "para": para, "chance": chance, "linhas": linhas,
                      "teste": teste if n and teste in ("sucesso", "falha") else None}
    registrar(g, "ferreiro", item=it["nome"], sucesso=sucesso, de=n, para=para, chance=chance, ouro=ouro,
              fragmentos=frag, em=quem or "bolsa", teste=g.forja_ultimo["teste"], prototipo="reforco")
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
    g.forja_ultimo = {"id": (getattr(g, "forja_ultimo", None) or {}).get("id", 0) + 1, "tipo": "desmonte", "nome": it["nome"],
                      "total": total}
    registrar(g, "desmontar", item=it["nome"], fragmentos=total, investimento=investido, da_peca=propria,
              prototipo="reforco")
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
    g.forja_ultimo = {"id": (getattr(g, "forja_ultimo", None) or {}).get("id", 0) + 1, "tipo": "encanto", "uid": uid,
                      "sulco": sulco, "de": encanto_tela(antes), "para": encanto_tela(essencia)}
    registrar(g, "encantar", item=it["nome"], essencia=essencia, sulco=sulco, substituiu=antes, ouro=ouro, em=quem or "bolsa",
              prototipo="encanto")
    return True, f"Gravado: {E.nome(*E.ler(essencia))} · {it['nome']}"


def niveis_de_teste(g):
    """Os níveis altos de teste (a faixa da demonstração; nada disto é conteúdo): peças do grupo levadas direto a +4, +8,
    +9, +11 e +12, duas com os sulcos cheios (três gravações), e ouro e fragmentos de sobra para tentar o resto. Só
    no save temporário da demonstração."""
    dar_uid(g)
    sulcos_do_grupo(g)

    def levar(it, n, gravacoes=()):
        if not it or not R.tipo(it):
            return
        it.setdefault("bonus_base", dict(it["bonus"]))
        it.setdefault("preco_base", it.get("preco", 0))
        aplicar_nivel(it, n)
        if gravacoes:
            it["encantos"] = list(gravacoes)
    levar(g.j.equip.get("arma"), 11, ("brasa", "carrasco", "eco"))          # tentar o +12 (o máximo)
    levar(FICHA.corpo(g, "morel").get("armadura"), 12, ("vigilia", "revide", "geada"))  # +12 com três gravações
    for it, n in zip(g.j.mochila, (8, 4, 9, 12)):                           # a bolsa: um de cada faixa
        levar(it, n)
    levar(FICHA.corpo(g, "odete").get("arma"), 5)
    levar(FICHA.corpo(g, "odete").get("secundaria"), 7)
    g.j.ouro = max(g.j.ouro, 99999)
    materiais(g)["fragmento"] = R.PILHA_MAX
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
    g.j.recalcular()
    g.forja_ultimo = None
    registrar(g, "niveis_teste")


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
    g.forja_ultimo = {"id": (getattr(g, "forja_ultimo", None) or {}).get("id", 0) + 1, "tipo": "transfere",
                      "origem": origem_uid, "destino": destino_uid, "de_origem": de_o, "de_destino": de_d, "novo": novo,
                      "ouro": ouro}
    registrar(g, "transferir", origem=o["nome"], destino=dd["nome"], de_origem=de_o, de_destino=de_d, novo=novo, ouro=ouro,
              prototipo="reforco")
    return True, f"Transferido: {dd['nome']} · +{novo}"


def essencias_de_teste(g):
    """Composições de essências para comparar (a faixa da demonstração; nada disto é conteúdo): Jean com a arma em
    Brasa II + Brasa I + Carrasco I (Brasa 3) e o peito em Vigília III + Revide II + Geada I; Odette com Eco III + Eco II
    no tomo e Eco II na arma (Eco 7, acima do teto 5); Morel com Revide nas duas peças. Os sulcos dessas peças passam a
    3 (só no teste) e o grupo recebe 3 essências de cada tier. Só no save temporário da demonstração."""
    dar_uid(g)
    sulcos_do_grupo(g)

    def gravar(it, lista):
        if it is not None and E.tipo(it):
            it["encantos"] = list(lista) + [None] * (3 - len(lista))
    gravar(g.j.equip.get("arma"), ["brasa:2", "brasa", "carrasco"])
    gravar(g.j.equip.get("armadura"), ["vigilia:3", "revide:2", "geada"])
    gravar(FICHA.corpo(g, "odete").get("secundaria"), ["eco:3", "eco:2"])
    gravar(FICHA.corpo(g, "odete").get("arma"), ["eco:2"])
    gravar(FICHA.corpo(g, "morel").get("armadura"), ["revide:2"])
    for k in E.ORDEM:
        for t in E.TIERS:
            materiais(g)[E.material(k, t)] = max(materiais(g).get(E.material(k, t), 0), 3)
    g.j.ouro = max(g.j.ouro, 2000)
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
    g.j.recalcular()
    g.forja_ultimo = None
    registrar(g, "essencias_teste")


def transferencia_de_teste(g):
    """Peças para testar a transferência (a faixa da demonstração): na bolsa, duas armas comuns de Guerreiro, uma +10 e
    outra +2 (com uma gravação, que não se move), e um peito incomum +6 com outro incomum +0. Ouro de sobra."""
    dar_uid(g)
    rng = random.Random(28)

    def peca(slot, raridade, n, gravacao=None):
        while True:
            it = itens.gerar_equip(rng, "guerreiro", 5, slot=slot, raridade=raridade)
            if it.get("raridade") == raridade and not it.get("unico"):
                break
        com_sulcos(it)
        it.setdefault("bonus_base", dict(it["bonus"]))
        it.setdefault("preco_base", it.get("preco", 0))
        aplicar_nivel(it, n)
        if gravacao and it.get("encantos"):
            it["encantos"][0] = gravacao
        return it
    novas = [peca("arma", "comum", 10), peca("arma", "comum", 2, "brasa"), peca("armadura", "magico", 6), peca("armadura", "magico", 0)]
    from rpg.regras import LIMITE_MOCHILA
    g.j.mochila = (novas + g.j.mochila)[:LIMITE_MOCHILA]
    dar_uid(g)
    g.j.ouro = max(g.j.ouro, 5000)
    g.forja_ultimo = None
    registrar(g, "transferencia_teste")


def luta_de_teste(g):
    """A luta de teste do laboratório: dois Esqueletos do nível do herói, sem fuga perdida nem saque, e o grupo volta
    como estava (vida, recurso, experiência): só para ver as gravações agindo."""
    from rpg.inimigos import criar
    from rpg.sistemas.confronto import Derrota
    guarda = {"hp": g.j.hp, "rec": g.j.rec, "xp": g.j.xp, "ouro": g.j.ouro,
              "comitiva": [(m, m.get("hp")) for m in comitiva.membros(g)]}
    g.encanto_log = []
    rng = random.Random(len(getattr(g, "lutas_teste", [])) + 3)
    inimigos = [criar(rng, "esqueleto", g.j.nivel) for _ in range(2)]
    try:
        g.combate(inimigos, pode_fugir=True, titulo="Luta de teste (laboratório)", saque=False)
    except Derrota:
        pass
    g.lutas_teste = getattr(g, "lutas_teste", []) + [list(g.encanto_log)]
    g.j.hp, g.j.rec, g.j.xp, g.j.ouro = guarda["hp"], guarda["rec"], guarda["xp"], guarda["ouro"]
    for m, hp in guarda["comitiva"]:
        m["hp"] = hp
    g.j.efeitos.clear()
    contagem = {}
    for k, *_ in g.encanto_log:
        contagem[k] = contagem.get(k, 0) + 1
    resumo = ", ".join(f"{E.ESSENCIAS[k]['nome']} ×{n}" for k, n in contagem.items()) or "nenhuma gravação disparou"
    g.ui.efeito(f"Luta de teste: {resumo}.", "info")


def forja(self):
    """A forja do protótipo: a mesma oficina no quadro de cima; no balcão, as peças do grupo, o reforço com o ganho, o
    custo, a posse e a falta antes de pagar, a comparação na luta e a desmontagem com confirmação."""
    from rpg.sistemas.servicos import cena_forja
    while True:
        self.ui.cena("A forja", self.loc["nome"], "menu")
        self.ui.painel("cena", cena_forja())
        if not self.ui.painel("forja_proto", painel(self)):
            self.dizer("A forja do protótipo só existe na tela gráfica.", "cinza")
            return
        esc = self.menu("", [("Pedido à forja", "forja", {"forja": True}), ("Voltar", "voltar", {"voltar": True})])
        if esc == "voltar":
            return
        d = getattr(self.ui, "extra_resposta", None) or {}
        if d.get("op") == "reforcar":
            ok, texto = reforcar(self, d.get("uid"), d.get("veio"), d.get("pedido"), d.get("teste"))
            if texto is None:
                continue
        elif d.get("op") == "desmontar" and d.get("confirmar") is True:
            ok, texto = desmontar(self, d.get("uid"), d.get("nome"))
        elif d.get("op") == "encantar":
            ok, texto = encantar(self, d.get("uid"), d.get("essencia"), d.get("sulco"), d.get("pedido"), d.get("substitui"))
            if texto is None:
                continue
        elif d.get("op") == "luta_teste":
            luta_de_teste(self)
            continue
        elif d.get("op") == "niveis_teste":
            niveis_de_teste(self)
            continue
        elif d.get("op") == "essencias_teste":
            essencias_de_teste(self)
            continue
        elif d.get("op") == "transferencia_teste":
            transferencia_de_teste(self)
            continue
        elif d.get("op") == "transferir" and d.get("confirmar") is True:
            ok, texto = transferir(self, d.get("origem"), d.get("destino"), d.get("pedido"))
            if texto is None:
                continue
        else:
            continue
        if not ok:  # o sucesso a própria janela mostra (a bancada acende; o topo conta ouro e fragmentos)
            self.ui.efeito(texto, "info")


# ------------------------------------------------------------------ ligar ao jogo, só nesta execução
def com_sulcos(it):
    if it and E.tipo(it):
        E.sortear_sulcos(it)
    return it


def criar_peca():
    """Os sulcos nascem com a peça: a criação de equipamento (o drop, o mercado, as recompensas, os únicos) passa a
    sortear os sulcos da peça nova, pela semente dela (o sorteio do jogo não muda). Os módulos que importaram a função
    pelo nome também são trocados. As peças que já existiam ganham os delas ao começar e ao carregar (sulcos_do_grupo)."""
    import rpg.dev
    import rpg.eventos.biomas
    import rpg.eventos.classe
    import rpg.eventos.comuns
    import rpg.jogo
    import rpg.sistemas.confronto
    import rpg.sistemas.loja
    if getattr(itens, "_sulcos", False):
        return
    itens._sulcos = True
    gerar, unico = itens.gerar_equip, itens.fazer_unico

    def gerar_com_sulcos(*a, **k):
        return com_sulcos(gerar(*a, **k))

    def unico_com_sulcos(*a, **k):
        return com_sulcos(unico(*a, **k))
    itens.gerar_equip, itens.fazer_unico = gerar_com_sulcos, unico_com_sulcos
    for m in (rpg.dev, rpg.eventos.biomas, rpg.eventos.classe, rpg.eventos.comuns, rpg.jogo,
              rpg.sistemas.confronto, rpg.sistemas.loja):
        if getattr(m, "gerar_equip", None) is gerar:
            m.gerar_equip = gerar_com_sulcos


def sulcos_do_grupo(g):
    """As peças que nasceram antes do laboratório (o cenário, um save antigo): os sulcos delas, uma vez."""
    for it, _, _ in pecas(g):
        com_sulcos(it)


def ativar():
    from rpg.sistemas import persistencia
    from rpg.sistemas.inventario import Inventario
    from rpg.sistemas.servicos import Servicos
    from rpg.web import estado as web_estado
    if "materiais" not in persistencia.CAMPOS_SAVE:
        persistencia.CAMPOS_SAVE = persistencia.CAMPOS_SAVE + ("materiais",)
    Servicos.ferreiro = forja
    E.ativar()
    carregar = persistencia.Persistencia.carregar.__func__ if hasattr(persistencia, "Persistencia") else None
    if carregar:
        def carregar_com_sulcos(cls, *a, **k):
            g = carregar(cls, *a, **k)
            sulcos_do_grupo(g)
            return g
        persistencia.Persistencia.carregar = classmethod(carregar_com_sulcos)
    ficha_item = itens.ficha

    def ficha_com_gravacao(it, recurso=None, **extra):
        """A ficha das telas (achado, mercado, inventário, dicas, forja) com o estado da peça: o nível de reforço e os
        sulcos (`encantos`: uma entrada por sulco, None no vazio). A tela desenha a partir disso, nunca do nome. Uma peça
        que pode ser gravada e ainda não tem sulcos ganha os dela aqui, uma vez (no lugar do drop)."""
        d = ficha_item(it, recurso, **extra)
        if not d:
            return d
        d["reforco"] = it.get("reforco", 0)
        if it.get("encantos") is not None:
            d["encantos"] = [encanto_tela(k) for k in it["encantos"]]
            g = JOGO[0]
            if g is not None:  # o total de quem veste a peça (só as peças vestidas por ele contam)
                quem = dono_de(g, it)
                d["gravacao_total"] = gravacao_total(g, quem)
        return d
    itens.ficha = ficha_com_gravacao
    criar_peca()
    web_estado._item = ficha_com_gravacao
    para_tela = itens.para_tela

    def para_tela_com_materiais():
        d = para_tela()
        d.update({k: {"icone": m["icone"], "nome": m["nome"], "desc": m["desc"], "hud": None}
                  for k, m in MATS.items()})
        return d
    itens.para_tela = para_tela_com_materiais
    heroi = web_estado.heroi

    def heroi_com_materiais(g):
        JOGO[0] = g
        h = heroi(g)
        m = materiais(g)
        h["materiais"] = [{"id": k, "nome": d["nome"], "plural": d["plural"], "icone": d["icone"], "qtd": m.get(k, 0),
                           "desc": d["desc"], "fontes": d["fontes"]} for k, d in MATS.items() if k in R.MATERIAIS or m.get(k)]
        return h
    web_estado.heroi = heroi_com_materiais
    sortear = Inventario.sortear_bau

    def sortear_bau(self):  # a exploração também dá material: o baú, metade das vezes, 1 fragmento (hipótese)
        sortear(self)
        if self.chance(0.5):
            dar_material(self, "fragmento", 1, "bau")
        if self.chance(0.25):  # e, às vezes, uma essência qualquer, do tier do nível do herói (hipótese do laboratório)
            dar_material(self, E.material(self.rng.choice(E.ORDEM), tier_do_nivel(self.j.nivel)), 1, "bau")
    Inventario.sortear_bau = sortear_bau
    from rpg.sistemas.confronto import Confronto
    if not getattr(Confronto, "_materiais", False):  # uma vez só, mesmo se ativar() for chamado de novo
        Confronto._materiais = True
        saque = Confronto.saque_de_combate

        def saque_com_materiais(self, derrotados):
            saque(self, derrotados)
            materiais_da_luta(self, derrotados)
        Confronto.saque_de_combate = saque_com_materiais


# ------------------------------------------------------------------ de onde vêm os materiais (hipóteses do laboratório)
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


def preparar(g):
    """O cenário de teste (CASOS=1: a armadura de Morel já no +4, três peças da bolsa no +1, +2 e +3 e 1 fragmento, para
    a falta de material no segundo passo): o Guerreiro no nível 4 no Vau, com Morel e Odette, 380 de ouro e as peças dos exemplos."""
    from rpg import missoes
    rng = random.Random(11)
    missoes.registro(g, "febre_do_turvo")["cenas"].append("abertura")
    g.marcar("templo_gratis_usado")
    g.marcar("curandeira_gratis_usado")
    g.j.nivel = 4
    for cid in ("morel", "odete"):
        comitiva.recrutar(g, cid)

    def peca(classe, slot, nivel, raridade="comum", evitar=None):
        """Uma peça do gerador do jogo (sorteio fixo); `evitar`: um pedaço de nome que ela não pode ter (a substituta
        não pode se chamar como a arma que substitui)."""
        while True:
            it = itens.gerar_equip(rng, classe, nivel, slot=slot, raridade=raridade)
            if not evitar or evitar not in it["nome"]:
                return it
    # o investimento inicial: a espada que o herói usa desde o começo
    g.j.equip["arma"] = peca("guerreiro", "arma", 2)
    g.j.equip["armadura"] = peca("guerreiro", "armadura", 2)
    FICHA.corpo(g, "morel").update(arma=peca("guerreiro", "arma", 2), armadura=peca("guerreiro", "armadura", 3))
    FICHA.corpo(g, "odete").update(arma=peca("mago", "arma", 3), secundaria=peca("mago", "secundaria", 3))
    # na bolsa: a substituta de base melhor (uma simulação de achado futuro), a peça especializada que compensa manter,
    # e peças para vender ou desmontar
    g.j.mochila = [
        peca("guerreiro", "arma", 7, evitar="Ferro"),                     # substituta: base de nível 7 (simulação)
        itens.fazer_unico(itens.UNICOS_POR_ID["lamento_de_gharbad"], 3),  # especializada: roubo de vida e vida por abate
        peca("guerreiro", "armadura", 4, "magico"),
        peca("mago", "secundaria", 5, "magico"),
        peca("arqueiro", "arma", 3, "magico"),                            # ninguém do grupo usa: vender ou desmontar
        peca("guerreiro", "anel", 3, "magico"),
    ]
    # o laboratório do encantamento: a arma do herói com 2 sulcos (as outras peças sorteiam os delas ao aparecer)
    g.j.equip["arma"]["encantos"] = [None, None]
    g.j.ouro = 380
    g.j.consumiveis["bau"] = 2
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
        m["hp"] = m["max_hp"]
    g.j.recalcular()
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    loc = next(l for l in g.mundo["locais"] if l["chave"] == "vau_do_turvo")
    g.mundo["atual"], loc["visitado"] = loc["id"], True
    g.periodo, g.clima = 0, "limpo"


def recompensa_de_teste(g):
    """A recompensa de demonstração (cenário de teste, não conteúdo da campanha): o quadro do espólio com os materiais."""
    g.ui.cena("Cenário de teste", "Recompensa de demonstração", "evento")
    g.abrir_espolio(titulo="recompensa de teste",
                    frase="Cenário de teste: uma caixa do ferreiro do Vau, para experimentar o reforço.")
    dar_material(g, "fragmento", 1 if os.environ.get("CASOS") else 12, "teste")
    for k in E.ORDEM:  # o laboratório do encantamento: 2 essências I de cada (recurso de teste)
        dar_material(g, E.material(k, 1), 2, "teste")
    g.fechar_espolio()
    # a página espera quem joga (o navegador abre depois do jogo começar: a cena atual é a desta recompensa)
    g.menu("Os fragmentos ficam na seção Materiais do Inventário, fora dos 12 espaços da bolsa.",
           [("Ir para a vila", None)])


CONECTOU = threading.Event()  # a página abriu: só então a recompensa de teste (o quadro não se repete depois)


def rodar(ui, pasta):
    from rpg.jogo import FimDeJogo, Jogo
    from rpg.ui import BotUI
    g = Jogo(BotUI(random.Random(1)), seed=11, pasta_saves=pasta, hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    preparar(g)
    sulcos_do_grupo(g)
    if os.environ.get("CASOS"):  # os casos de conferência: a armadura de Morel já no limite (+4); poucos fragmentos
        dar_uid(g)
        ouro = g.j.ouro
        g.j.ouro, materiais(g)["fragmento"] = 9999, 99
        for _ in range(R.LIMITE):
            reforcar(g, FICHA.corpo(g, "morel")["armadura"]["uid"], teste="sucesso")
        # e peças da bolsa reforçadas de verdade (+1, +2, +3), para conferir o reflexo de cada nível lado a lado
        for it, n in zip(g.j.mochila[:3], (1, 2, 3)):
            for _ in range(n):
                reforcar(g, it["uid"], teste="sucesso")
        g.j.ouro, materiais(g)["fragmento"] = ouro, 0
        g.forja_ultimo = None
    g.ui, ui.jogo = ui, g
    g.ui.cena("Cenário de teste", "Recompensa de demonstração", "evento")
    g.ui.atualizar()
    CONECTOU.wait()
    time.sleep(1.0)
    recompensa_de_teste(g)
    try:
        g.rodar()
    except FimDeJogo:
        pass


def servir():
    from rpg.web.ponte import WebUI
    from rpg.web.servidor import Servidor
    ativar()
    pasta = tempfile.mkdtemp(prefix="reforco-")
    ui = WebUI()
    ui.jogo = None
    srv = Servidor(ui, porta=int(os.environ.get("DEMO_PORTA", "8791")),
                   config={"velocidade": os.environ.get("VELOCIDADE", "normal")})
    Handler = srv.httpd.RequestHandlerClass
    get = Handler.do_GET
    tela = os.path.join(AQUI, "tela")

    def do_GET(self):  # o jogo de sempre, com o script e o estilo do protótipo no fim da página
        caminho = self.path.split("?")[0]
        if caminho in ("/", "/index.html"):
            from rpg.web import servidor as mod_srv
            with open(os.path.join(mod_srv.PASTA, "index.html"), encoding="utf-8") as f:
                html = f.read()
            extra = '<script src="/proto/carregar.js"></script></body>'  # a faixa da demonstração e a tela escolhida
            return self._responder(200, html.replace("</body>", extra).encode("utf-8"), "text/html; charset=utf-8")
        if caminho.startswith("/proto/"):
            arq = os.path.normpath(os.path.join(tela, caminho[len("/proto/"):]))
            if not arq.startswith(tela + os.sep) or not os.path.isfile(arq):
                return self._responder(404)
            tipo = "text/css" if arq.endswith(".css") else "text/javascript"
            with open(arq, "rb") as f:
                return self._responder(200, f.read(), tipo + "; charset=utf-8")
        return get(self)
    Handler.do_GET = do_GET
    eventos = Handler._eventos

    def _eventos(self):
        CONECTOU.set()
        return eventos(self)
    Handler._eventos = _eventos
    srv.iniciar()
    print(srv.url, flush=True)
    print(f"Saves temporários em {pasta}", flush=True)
    threading.Thread(target=rodar, args=(ui, pasta), daemon=True).start()
    if not os.environ.get("SEM_NAVEGADOR"):
        webbrowser.open(srv.url)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    servir()
