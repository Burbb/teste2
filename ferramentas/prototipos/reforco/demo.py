"""A demonstração jogável do reforço, dos materiais e da desmontagem (protótipo; roadmapIDEIAS/25, seção 5).

    python ferramentas/prototipos/reforco/demo.py        (ou dois cliques em demo.bat)

Sobe o jogo de verdade num save temporário (uma pasta nova a cada vez; os saves pessoais não são lidos nem tocados),
no Vau, com o herói e a comitiva, e troca só nesta execução (`ativar`) a forja, o espólio do baú, a venda de peça
reforçada e a ficha do inventário pelas regras de regras.py. O jogo de produção não importa esta pasta.
"""

import os
import random
import re
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


def requisito_material(chave, tem, precisa):
    """Um material que a operação consome, no formato comum das telas da forja (16ª versão): disponível/necessário
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
    # a comparação é uma hipótese: não pode deixar rastro. FICHA.atualizar faz a vida acompanhar o máximo para baixo
    # (a regra de quem tira uma peça), e uma peça da bolsa com menos Vida cortava a vida de verdade, que não voltava
    # quando a peça certa era recolocada (a perda de vida ao entrar na forja, 17ª versão). A vida e o recurso de agora
    # voltam exatamente como estavam.
    vida = _vida_de(g, quem)
    desfazer = mudar()
    FICHA.atualizar(g, quem)
    depois = numeros(g, quem)
    desfazer()
    FICHA.atualizar(g, quem)
    _repor_vida(g, quem, vida)
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


def _vida_de(g, quem):
    """A vida e o recurso de quem, como estão (o herói ou o companheiro)."""
    if quem == HEROI:
        return g.j.hp, g.j.rec
    m = comitiva.membro(g, quem)
    return (m["hp"], m.get("rec")) if m else None


def _repor_vida(g, quem, vida):
    if vida is None:
        return
    if quem == HEROI:
        g.j.hp, g.j.rec = vida
        return
    m = comitiva.membro(g, quem)
    m["hp"] = vida[0]
    if vida[1] is not None:
        m["rec"] = vida[1]


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
    # o reforço é um serviço sobre a peça: classe e nível restringem vestir, não reforçar (16ª versão). A prévia vem da
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
                                "tem": tem, "ouro_tem": g.j.ouro, "falta": falta, "motivo": motivo, "luta": luta,
                                # o que a tentativa consome além do ouro (que fica no botão): disponível/necessário
                                "requer": [requisito_material("fragmento", tem, frag)]})
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
    d["encantar"] = {"motivo": E.motivo(it), "dono": FICHA.nome_de(g, quem) if quem else None,
                     "nivel": nivel_de(g, quem) if quem else None, "essencias": essencias, "previsao": prev,
                     "teto": 5, "totais": {}}  # teto e totais: só para as versões guardadas da tela
    d["gravacao_total"] = []
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
            "medida": d["medida"][0], "valor": E.com_unidade(e, v), "nota": d["nota"],
            # só para as versões guardadas da tela (tela/historico), que ainda leem o modelo de níveis: não quebram
            "teto": 5, "textos": [[ef, lim]] * 5, "valores": [E.com_unidade(e, v)] * 5}


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
    # 16ª versão: na prévia da peça escolhida, o nome do efeito basta ("Carrasco", não "Carrasco nesta peça"); o total de
    # quem veste só aparece quando explica uma consequência (o limite que corta a soma). 17ª: o limite aparece no próprio
    # valor final ("60% · limite"), não numa conta do que sobra ("Limite 60%: 8% não valem"); só quando nada muda (já
    # estava no limite) uma nota curta diz isso.
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


def proximo_id(g, consumir=True):
    """O número do próximo resultado da forja: só cresce (os cenários de teste limpam o último resultado, e a numeração
    recomeçando do 1 fazia a tela tomar o resultado novo por um já visto e pular a cena)."""
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
            "custo_encanto": g.preco(E.CUSTO_OURO), "teste": estado_teste(g),
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
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "reforco", "uid": uid,
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
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "desmonte", "nome": it["nome"],
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
    # 16ª: as armaduras do +9 ao +12 para os dois acabamentos candidatos: Jean de ferro (claro) da cabeça aos pés, e
    # Odette com um peito de tecido (escuro); vestidas só se o espaço está vazio (nada some do corpo de ninguém)
    rng = random.Random(16)
    for espaco, n in (("cabeca", 9), ("maos", 10), ("pernas", 11), ("pes", 12)):
        if not g.j.equip.get(espaco):
            g.j.equip[espaco] = com_sulcos(itens.gerar_equip(rng, g.j.classe, 4, slot=espaco, raridade="comum"))
        levar(g.j.equip[espaco], n)
    corpo_o = FICHA.corpo(g, "odete")
    if not corpo_o.get("armadura"):
        corpo_o["armadura"] = com_sulcos(itens.gerar_equip(rng, "mago", 4, slot="armadura", raridade="magico"))
    levar(corpo_o["armadura"], 11)
    dar_uid(g)
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
    g.forja_ultimo = {"id": proximo_id(g), "tipo": "transfere",
                      "origem": origem_uid, "destino": destino_uid, "de_origem": de_o, "de_destino": de_d, "novo": novo,
                      "ouro": ouro}
    registrar(g, "transferir", origem=o["nome"], destino=dd["nome"], de_origem=de_o, de_destino=de_d, novo=novo, ouro=ouro,
              prototipo="reforco")
    return True, f"Transferido: {dd['nome']} · +{novo}"


def essencias_de_teste(g):
    """Composições de essências para comparar (a faixa da demonstração; nada disto é conteúdo). Vestidas, só tier I (o
    grupo está no nível 4): Jean com Brasa I + Brasa I + Carrasco I na arma (Brasa 40%) e Vigília I + Revide I + Geada I
    no peito; Odette com Eco I na arma e Eco I + Eco I no tomo (Eco 30%, entre peças); Morel com três Revides I (36%).
    Na bolsa, preparadas para depois: o Martelo de Aço com Brasa III + Brasa II (64%, o limite 60% corta; requer o
    nível 9) e a Couraça com Vigília II (requer o 5). Os sulcos dessas peças passam a 3 (só no teste) e o grupo recebe
    3 essências de cada tier. Só no save temporário da demonstração."""
    dar_uid(g)
    sulcos_do_grupo(g)

    def gravar(it, lista):
        if it is not None and E.tipo(it):
            it["encantos"] = list(lista) + [None] * (3 - len(lista))
    gravar(g.j.equip.get("arma"), ["brasa", "brasa", "carrasco"])
    gravar(g.j.equip.get("armadura"), ["vigilia", "revide", "geada"])
    gravar(FICHA.corpo(g, "odete").get("secundaria"), ["eco", "eco"])
    gravar(FICHA.corpo(g, "odete").get("arma"), ["eco"])
    gravar(FICHA.corpo(g, "morel").get("armadura"), ["revide", "revide", "revide"])
    for it in g.j.mochila:
        if it.get("slot") == "arma" and "Aço" in it.get("nome", "") and not it.get("unico"):
            gravar(it, ["brasa:3", "brasa:2"])
        elif it.get("slot") == "armadura" and E.tipo(it):
            gravar(it, ["vigilia:2"])
    for k in E.ORDEM:
        for t in E.TIERS:
            materiais(g)[E.material(k, t)] = max(materiais(g).get(E.material(k, t), 0), 3)
    g.j.ouro = max(g.j.ouro, 2000)
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
    g.j.recalcular()
    g.forja_ultimo = None
    registrar(g, "essencias_teste")


def nivel_de_teste(g):
    """Sobe o grupo 4 níveis pelo caminho do jogo (dev.subir_ate: atributos, habilidades, pontos), sem a festa de cada
    nível: para ver os requisitos de tier II (nível 5) e III (nível 9) atendidos. Só no save temporário."""
    from rpg import dev
    from rpg.regras import NIVEL_MAXIMO
    g.ui.celebrar = lambda *a, **k: None
    try:
        dev.subir_ate(g, min(NIVEL_MAXIMO, g.j.nivel + 4), spec=False)
    finally:
        del g.ui.celebrar
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
    g.forja_ultimo = None
    registrar(g, "nivel_teste", nivel=g.j.nivel)


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


# ------------------------------------------------------------------ o painel de testes (16ª versão; só na demonstração)
def estado_teste(g):
    """Os valores que o painel de testes edita, como estão agora: nível, classe, especialização, ouro e cada material,
    e as escolhas possíveis (as especializações de cada classe)."""
    from rpg.classes import SPECS
    m = materiais(g)
    return {"nivel": g.j.nivel, "classe": g.j.classe, "spec": g.j.spec or "", "ouro": g.j.ouro,
            "materiais": [{"id": k, "nome": d["nome"], "qtd": m.get(k, 0), "essencia": d.get("tier") is not None,
                           "numeral": d.get("numeral"), "cor": d.get("cor"), "icone": d["icone"]} for k, d in MATS.items()],
            "classes": [{"id": c, "nome": CLASSES[c]["nome"], "specs": [{"id": s, "nome": SPECS[s]["nome"]}
                                                                       for s in CLASSES[c]["specs"]]} for c in CLASSES],
            "nivel_max": _nivel_max(), "nivel_spec": bal.NIVEL_ESPECIALIZACAO, "pilha": R.PILHA_MAX}


def _nivel_max():
    from rpg.regras import NIVEL_MAXIMO
    return NIVEL_MAXIMO


def _inteiro(v, menor, maior, nome):
    """O valor do painel como inteiro dentro dos limites, ou o motivo de recusar."""
    if isinstance(v, bool) or not isinstance(v, (int, float, str)):
        return None, f"{nome}: valor inválido."
    try:
        n = int(str(v).strip())
    except ValueError:
        return None, f"{nome}: use um número inteiro."
    if not menor <= n <= maior:
        return None, f"{nome}: de {menor} a {maior}."
    return n, None


def validar_sessao(dados):
    """Ouro e materiais do painel: ({ouro, materiais}, None) ou (None, motivo). Nada muda aqui."""
    ouro, motivo = _inteiro(dados.get("ouro"), 0, 999999, "Ouro")
    if motivo:
        return None, motivo
    mats = {}
    for k, v in (dados.get("materiais") or {}).items():
        if k not in MATS:
            return None, f"Material desconhecido: {k}."
        n, motivo = _inteiro(v, 0, R.PILHA_MAX, MATS[k]["nome"])
        if motivo:
            return None, motivo
        mats[k] = n
    return {"ouro": ouro, "materiais": mats}, None


def validar_cenario(dados):
    """Nível, classe e especialização do painel, que só mudam reconstruindo o personagem: ({...}, None) ou (None,
    motivo). A especialização tem de ser da classe e só existe do nível dela em diante (no jogo, a encruzilhada é
    obrigatória ao chegar lá)."""
    nivel, motivo = _inteiro(dados.get("nivel"), 1, _nivel_max(), "Nível")
    if motivo:
        return None, motivo
    classe = dados.get("classe")
    if classe not in CLASSES:
        return None, "Escolha uma classe."
    spec = dados.get("spec") or None
    if nivel < bal.NIVEL_ESPECIALIZACAO:
        if spec:
            return None, f"Especialização só a partir do nível {bal.NIVEL_ESPECIALIZACAO}."
    elif spec not in CLASSES[classe]["specs"]:
        return None, f"Escolha a especialização de {CLASSES[classe]['nome']}."
    return {"nivel": nivel, "classe": classe, "spec": spec}, None


def aplicar_sessao(g, dados):
    """Ouro e materiais na sessão de agora (o personagem e as peças ficam)."""
    v, motivo = validar_sessao(dados)
    if motivo:
        return False, motivo
    g.j.ouro = v["ouro"]
    for k, n in v["materiais"].items():
        materiais(g)[k] = n
    registrar(g, "teste_sessao", ouro=v["ouro"])
    return True, "Valores aplicados."


def reiniciar_cenario(g, dados):
    """Descarta a sessão temporária e monta o cenário de novo com a classe, o nível e a especialização do painel: o
    herói pelo caminho do jogo (Jogador novo, dev.subir_ate: atributos, habilidades, talentos e a especialização na
    encruzilhada), a comitiva recrutada de novo no nível dele e as peças do cenário na classe escolhida. Os sulcos, os
    reforços e as gravações de antes se perdem. O ouro e os materiais do painel entram depois, validados."""
    from rpg import dev
    from rpg.entidades import Jogador
    v, motivo = validar_cenario(dados)
    sessao, motivo_s = validar_sessao(dados) if motivo is None else (None, None)
    if motivo or motivo_s:
        return False, motivo or motivo_s
    classe, nivel, spec = v["classe"], v["nivel"], v["spec"]
    rng = random.Random(11)
    celebrar, efeito, escolher_animal = g.ui.celebrar, g.ui.efeito, g.escolher_companheiro
    g.ui.celebrar = lambda *a, **k: None
    g.ui.efeito = lambda *a, **k: None
    g.escolher_companheiro = lambda tipo=None: escolher_animal(tipo or next(iter(comitiva_animais())))
    try:
        g.j = Jogador(g.j.nome, classe)
        g.j.equip["arma"] = itens.gerar_equip(rng, classe, 1, "arma", qualidade=-2)
        g.j.recalcular()
        dev.subir_ate(g, nivel, spec=spec if spec else False)
        g.comitiva = []
        for cid in ("morel", "odete"):
            comitiva.recrutar(g, cid)
    finally:
        g.ui.celebrar, g.ui.efeito = celebrar, efeito
        del g.escolher_companheiro
    vestir_cenario(g, rng, classe)
    g.materiais = {}
    for k, n in sessao["materiais"].items():
        g.materiais[k] = n
    g.j.ouro = sessao["ouro"]
    g.forja_ultimo = None
    registrar(g, "teste_cenario", classe=classe, nivel=nivel, spec=spec)
    return True, f"Cenário reiniciado: {CLASSES[classe]['nome']}, nível {nivel}."


def comitiva_animais():
    """Os animais da especialização que traz um (o primeiro, no cenário de teste: a escolha seria uma pergunta)."""
    from rpg.classes import COMPANHEIROS as ANIMAIS
    return ANIMAIS


def vestir_cenario(g, rng, classe):
    """As peças do cenário de teste na classe do herói (as mesmas funções de preparar): a arma e o peito vestidos, a
    comitiva com as dela, e na bolsa uma substituta de base melhor, um único da classe, peças incomuns e, quando há
    uma classe que ninguém do grupo usa, uma arma dela (o reforço sem portador)."""
    def peca(c, slot, nivel, raridade="comum"):
        return itens.gerar_equip(rng, c, nivel, slot=slot, raridade=raridade)
    g.j.equip["arma"] = peca(classe, "arma", 2)
    g.j.equip["armadura"] = peca(classe, "armadura", 2)
    FICHA.corpo(g, "morel").update(arma=peca("guerreiro", "arma", 2), armadura=peca("guerreiro", "armadura", 3))
    FICHA.corpo(g, "odete").update(arma=peca("mago", "arma", 3), secundaria=peca("mago", "secundaria", 3))
    unico = next((u for u in itens.UNICOS_POR_ID.values() if u.get("classe") == classe), None)
    sobra = next((c for c in CLASSES if c not in {classe, "guerreiro", "mago"}), None)
    g.j.mochila = [x for x in (
        peca(classe, "arma", 7), itens.fazer_unico(unico, 3) if unico else None, peca(classe, "armadura", 4, "magico"),
        peca(classe, "secundaria", 5, "magico"), peca(sobra, "arma", 3, "magico") if sobra else None,
        peca(classe, "anel", 3, "magico")) if x]
    sulcos_do_grupo(g)
    g.j.equip["arma"]["encantos"] = [None, None]
    g.j.consumiveis["bau"] = 2
    for m in comitiva.membros(g):
        FICHA.atualizar(g, m["id"])
        m["hp"] = m["max_hp"]
    g.j.recalcular()
    g.j.hp, g.j.rec = g.j.max_hp, g.j.max_rec
    dar_uid(g)


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
        # o painel é calculado antes de a cena ser anunciada: a cena nova limpa a página, e com o cálculo no meio o
        # navegador chegava a pintar a oficina sem a janela (a piscada ao reforçar, 16ª versão)
        dados = painel(self)
        self.ui.cena("A forja", self.loc["nome"], "menu")
        self.ui.painel("cena", cena_forja())
        if not self.ui.painel("forja_proto", dados):
            self.dizer("A forja do protótipo só existe na tela gráfica.", "cinza")
            return
        esc = self.menu("", [("Pedido à forja", "forja", {"forja": True}), ("Voltar", "voltar", {"voltar": True, "lugar": True})])
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
        elif d.get("op") == "nivel_teste":
            nivel_de_teste(self)
            continue
        elif d.get("op") == "transferencia_teste":
            transferencia_de_teste(self)
            continue
        elif d.get("op") == "teste_sessao":
            ok, texto = aplicar_sessao(self, d)
        elif d.get("op") == "teste_cenario":
            ok, texto = reiniciar_cenario(self, d)
        elif d.get("op") == "transferir" and d.get("confirmar") is True:
            ok, texto = transferir(self, d.get("origem"), d.get("destino"), d.get("pedido"))
            if texto is None:
                continue
        else:
            continue
        if not ok or d.get("op", "").startswith("teste_"):  # o sucesso a própria janela mostra; o painel, um aviso
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


def descrever_bonus(bonus, recurso=None):
    """'+3 Defesa, +4,5% Crítico': o descrever_bonus do jogo, com a casa decimal em vírgula (16ª versão)."""
    from rpg.entidades import nome_stat
    return ", ".join(f"{'+' if v >= 0 else ''}{R.fmt(v)}{'%' if k in itens.PERCENTUAIS else ''} {nome_stat(k, recurso)}"
                     for k, v in bonus.items())


def _com_fracao(inteiro_jogo, total, fracao):
    """O número do jogo (inteiro) mais a fração que só o equipamento reforçado traz: sem fração, exatamente o de antes."""
    return R.limpo(inteiro_jogo(total - fracao) + fracao) if fracao else inteiro_jogo(total)


def _fracao(v):
    return round(v - int(v), 1) if v > 0 else 0


FRACIONADOS = ("espinhos", "regen_vida", "vida_abate")  # pontos de vida: a luta usa inteiros e acumula a fração
mod_jogo_original = None  # o mod do jogo (modificadores.mod), que mod_com_fracao consulta


def decimais_na_luta():
    """A cadeia da fração do reforço, só nesta execução (16ª versão): a casa decimal das peças chega à ficha e à luta.
    - Ataque, Poder, Defesa e Agilidade do herói e dos companheiros levam a fração das peças (o resto continua como o
      jogo conta: sem peça fracionária, o número é o mesmo de antes). A luta usa o número com a casa (dano, defesa,
      esquiva).
    - Espinhos, Vida por turno e Vida por abate são pontos de vida (inteiros): a fração se acumula a cada disparo, na
      pessoa (2,6 por turno cura 2, 3, 3, 2, 3…, em média 2,6). O teste e a nota do 27 conferem."""
    from rpg import entidades, sobrevivencia
    from rpg.comitiva import ficha as cficha, grupo as cgrupo, luta as cluta
    import rpg.comitiva as pkg_comitiva
    from rpg.combate import golpe as mg, heroi as mh, turnos as mt
    from rpg import modificadores
    global mod_jogo_original
    J = entidades.Jogador
    if getattr(J, "_decimais", False):
        return
    J._decimais = True
    mod_jogo_original = modificadores.mod
    recalcular = J.recalcular

    def recalcular_com_fracao(self):
        recalcular(self)
        totais, _ = self.totais()
        penal = sobrevivencia.multiplicadores(self)
        for st in ("atk", "poder", "defesa", "agi"):
            f = _fracao(sum(it["bonus"].get(st, 0) for it in self.equip.values() if it))
            p = penal.get(st, 1.0)
            setattr(self, st, max(1, _com_fracao(lambda x: int(round(x)), totais[st] * p, f * p)))
    J.recalcular = recalcular_com_fracao
    atributos = cgrupo.atributos

    def atributos_com_fracao(g, m):
        r = atributos(g, m)
        d, nv, ex = cgrupo.COMPANHEIROS[m["id"]], g.j.nivel - 1, cficha.extras(m)
        b, c = d["base"], d["cresc"]
        r["defesa"] = _com_fracao(int, b["defesa"] + c["defesa"] * nv + ex["defesa"], _fracao(ex["defesa"]))
        r["agi"] = b["agi"] + _com_fracao(lambda x: int(round(x)), ex["agi"], _fracao(ex["agi"]))
        for st in ("atk", "poder"):
            r[st] = R.limpo(r[st]) if _fracao(ex[st]) else r[st]
        return r
    cgrupo.atributos = cluta.atributos = pkg_comitiva.atributos = atributos_com_fracao

    def mod_com_fracao(u, chave):
        v = mod_jogo_original(u, chave)
        if chave not in FRACIONADOS or not v or float(v).is_integer():
            return v
        conta = u.__dict__.setdefault("_fracao", {})
        # a cura por turno e por abate é consultada duas vezes no mesmo disparo (se há, quanto): o tique da vez guarda
        # o número; os espinhos, uma vez por golpe
        tique = None if chave == "espinhos" else getattr(u, "_tique", 0)
        e = conta.get(chave)
        if e and tique is not None and e[0] == tique:
            return e[1]
        resto = (e[2] if e else 0.0) + v
        inteiro = int(resto + 1e-9)
        conta[chave] = (tique, inteiro, resto - inteiro)
        return inteiro
    mg.mod = mh.mod = mt.mod = mod_com_fracao

    def tique(u):
        if u is not None:
            u._tique = getattr(u, "_tique", 0) + 1
    fase, vez, morte = mh.AcoesDoHeroi.fase_jogador, mt.TurnosDosOutros.vez_aliado, mg.Golpes.ao_morrer

    def fase_jogador(self, *a, **k):
        tique(self.j)
        return fase(self, *a, **k)

    def vez_aliado(self, aliado, *a, **k):
        tique(aliado)
        return vez(self, aliado, *a, **k)

    def ao_morrer(self, c, por=None, *a, **k):
        tique(por)
        if por is not self.j:
            tique(self.j)
        return morte(self, c, por, *a, **k)
    mh.AcoesDoHeroi.fase_jogador, mt.TurnosDosOutros.vez_aliado, mg.Golpes.ao_morrer = fase_jogador, vez_aliado, ao_morrer
    from rpg.web import estado as web_estado
    companheiro = web_estado.ficha_companheiro

    def ficha_companheiro_com_fracao(g, m):
        d = companheiro(g, m)
        at, leal, ex = cgrupo.atributos(g, m), pkg_comitiva.lealdade(m), cficha.extras(m)
        brutos = {"Ataque": ("atk", at["atk"] * leal), "Defesa": ("defesa", at["defesa"]), "Agilidade": ("agi", at["agi"]),
                  "Poder": ("poder", at["poder"] * leal)}
        for nome, (st, v) in brutos.items():
            if _fracao(ex[st]) and nome in d.get("atributos", {}):
                d["atributos"][nome] = R.fmt(v)
        return d
    web_estado.ficha_companheiro = ficha_companheiro_com_fracao


def ativar():
    from rpg.sistemas import persistencia
    from rpg.sistemas.inventario import Inventario
    from rpg.sistemas.servicos import Servicos
    from rpg.web import estado as web_estado
    if "materiais" not in persistencia.CAMPOS_SAVE:
        persistencia.CAMPOS_SAVE = persistencia.CAMPOS_SAVE + ("materiais",)
    Servicos.ferreiro = forja
    E.ativar()
    decimais_na_luta()
    requisitos_de_nivel(Inventario)
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
        d["bonus"] = descrever_bonus(it["bonus"], recurso)  # "+9,6 Poder" (a casa com vírgula, só quando existe)
        d["reforco"] = it.get("reforco", 0)
        d["requisito"] = E.requisito(it)
        if it.get("encantos") is not None:
            d["encantos"] = [encanto_tela(k) for k in it["encantos"]]
            d["efeitos"] = efeitos_peca(it)  # o que esta peça fornece (os totais de quem veste ficam na prévia)
            d["gravacao_total"] = []  # só para as versões guardadas da tela
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
        # a casa decimal que o reforço traz, com vírgula, nos atributos e nas dicas deles ("Defesa 12,4")
        h["atributos"] = {k: R.fmt(v) if isinstance(v, float) else v for k, v in h.get("atributos", {}).items()}
        virgula = lambda t: re.sub(r"(\d)\.(\d)", r"\1,\2", t) if isinstance(t, str) else t  # noqa: E731
        h["atributos_info"] = {k: [virgula(x) for x in v] for k, v in (h.get("atributos_info") or {}).items()}
        m = materiais(g)
        h["materiais"] = [{"id": k, "nome": d["nome"], "plural": d["plural"], "icone": d["icone"], "qtd": m.get(k, 0),
                           "desc": d["desc"], "fontes": d["fontes"], "numeral": d.get("numeral"), "cor": d.get("cor"),
                           "requisito": d.get("requisito", 1)} for k, d in MATS.items() if k in R.MATERIAIS or m.get(k)]
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


def requisitos_de_nivel(Inventario):
    """O nível mínimo para usar a peça, em todos os caminhos de vestir (só nesta execução): o Inventário (clique duplo,
    menu, arrastar, troca entre personagens) passa por ficha.motivo_nao_veste; o achado, o mercado e a troca de arma na
    luta, por pode_usar. Quem já veste uma peça acima do nível não a perde (nada é tirado sozinho)."""
    if getattr(FICHA, "_requisito", False):
        return
    FICHA._requisito = True
    nao_veste, pode = FICHA.motivo_nao_veste, Inventario.pode_usar
    FICHA._nao_veste_classe = nao_veste  # só a classe (o reforço de uma peça para depois)

    def nao_veste_com_requisito(g, quem, item):
        return nao_veste(g, quem, item) or motivo_requisito(g, quem, item)
    FICHA.motivo_nao_veste = nao_veste_com_requisito

    def pode_usar_com_requisito(self, item):
        return pode(self, item) and not motivo_requisito(self, HEROI, item)
    Inventario.pode_usar = pode_usar_com_requisito
    oferecer = Inventario.oferecer_equip

    def oferecer_com_requisito(self, item):
        """O achado acima do nível: guardar diz por quê ("requer nível 7"), não "para vender"."""
        motivo = pode(self, item) and motivo_requisito(self, HEROI, item)
        if not motivo:
            return oferecer(self, item)
        troca = f" ({motivo.rstrip('.').lower()})"
        rotulo = (lambda t: t.replace(" (para vender)", troca) if isinstance(t, str) else t)
        painel, menu = self.ui.painel, self.menu

        def painel_req(nome, dados=None, *a, **k):
            if nome == "achado" and isinstance(dados, dict):
                dados = {**dados, "acoes": [rotulo(x) for x in dados.get("acoes", [])]}
            return painel(nome, dados, *a, **k)

        def menu_req(titulo, opcoes, *a, **k):
            return menu(titulo, [(rotulo(o[0]),) + tuple(o[1:]) for o in opcoes], *a, **k)
        self.ui.painel, self.menu = painel_req, menu_req
        try:
            return oferecer(self, item)
        finally:
            del self.ui.painel, self.menu
    Inventario.oferecer_equip = oferecer_com_requisito


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
    g.menu("", [("Ir para a vila", None)])


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
