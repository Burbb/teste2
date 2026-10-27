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

import regras as R  # noqa: E402
from rpg import balanceamento as bal  # noqa: E402
from rpg import comitiva, itens  # noqa: E402
from rpg.classes import CLASSES  # noqa: E402
from rpg.combate.eficacia import mult_tracos  # noqa: E402
from rpg.modificadores import mod  # noqa: E402
from rpg.telemetria import registrar  # noqa: E402

FICHA = comitiva.ficha
HEROI = FICHA.HEROI


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
        g.ui.efeito(f"A pilha de {R.MATERIAIS[chave]['plural']} está cheia ({R.PILHA_MAX}).", "info")
        return 0
    m[chave] = m.get(chave, 0) + entra
    d = R.MATERIAIS[chave]
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


def ficha_peca(g, it, quem, s):
    rec = g.j.nome_recurso if quem in (None, HEROI) else comitiva.luta.RECURSO.get(quem, g.j.nome_recurso)
    n = it.get("reforco", 0)
    t = R.tipo(it)
    tem = materiais(g).get("fragmento", 0)
    d = {"uid": it["uid"], "item": itens.ficha(it, rec), "quem": quem, "onde": _nome_quem(g, quem), "espaco": s,
         "reforco": n, "limite": R.LIMITE, "tipo": t,
         "acumulado": R.texto_ganho(R.ganho_total(it, n)) if n else "",
         "veio": {"fio": "Fio", "runas": "Runas"}.get(it.get("veio"))}
    # todas as propriedades da peça, na ordem dela; as que o reforço faz crescer vêm marcadas (a ficha não esconde nada)
    from rpg.entidades import nome_stat
    cresce = {st for st, _, _ in R.linhas(it)}
    d["propriedades"] = [{"stat": st, "nome": nome_stat(st, rec).lstrip("% ")[:1].upper() + nome_stat(st, rec).lstrip("% ")[1:], "valor": v,
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
        # a arma do Guerreiro escolhe o veio no primeiro reforço: um passo para cada caminho
        veios = ["fio", "runas"] if t == "arma" and it.get("classe") == "guerreiro" and not it.get("veio") else [None]
        d["passos"] = []
        for v in veios:
            antigo = it.get("veio")
            if v:
                it["veio"] = v
            ganho = R.proximo(it)
            luta = comparar(g, quem, com_reforco(it, ganho)) if quem else None
            it["veio"] = antigo
            if not antigo:
                it.pop("veio", None)
            linhas = [{"nome": R.NOMES.get(st, st), "antes": it["bonus"].get(st, 0),
                       "depois": it["bonus"].get(st, 0) + v_} for st, v_ in ganho.items()]
            ch = R.chance(it, n + 1)
            d["passos"].append({"veio": v, "rotulo": {"fio": "Fio", "runas": "Runas"}.get(v), "chance": ch,
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
    return d


def painel(g):
    dar_uid(g)
    m = materiais(g)
    abas = [{"id": q, "nome": FICHA.nome_de(g, q), "retrato": g.j.classe if q == HEROI else q}
            for q in FICHA.personagens(g)] + [{"id": "bolsa", "nome": "Bolsa", "retrato": None}]
    return {"ouro": g.j.ouro, "limite": R.LIMITE, "abas": abas, "ultimo": getattr(g, "forja_ultimo", None),
            "materiais": [{"id": k, **R.MATERIAIS[k], "qtd": m.get(k, 0)} for k in R.MATERIAIS],
            "pecas": [ficha_peca(g, it, quem, s) for it, quem, s in pecas(g)]}


# ------------------------------------------------------------------ as ações (a tela pede; tudo é conferido aqui)
def aplicar_nivel(it, n):
    """Leva a peça ao nível +n: as linhas da base ficam com o ganho de +n (subindo ou caindo), e o nome e o preço
    acompanham. Afixos, especiais e o veio não mudam."""
    antes, depois = R.ganho_total(it, it.get("reforco", 0)), R.ganho_total(it, n)
    for st in set(antes) | set(depois):
        it["bonus"][st] = it["bonus"].get(st, 0) + depois.get(st, 0) - antes.get(st, 0)
    it["reforco"] = n
    it["preco"] = R.preco_com_reforco(it)
    base = it["nome"].split(" +")[0]
    it["nome"] = f"{base} +{n}" if n else base


def reforcar(g, uid, veio=None, pedido=None, teste=None):
    """Uma tentativa, resolvida uma única vez. `pedido`: o id que a tela manda; o mesmo id de novo não tenta outra vez.
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
    escolhe = t == "arma" and it.get("classe") == "guerreiro" and not it.get("veio")
    if escolhe and veio not in ("fio", "runas"):
        return False, "Escolha Fio ou Runas."
    ouro, frag = custo_passo(g, n)
    tem = materiais(g).get("fragmento", 0)
    if g.j.ouro < ouro or tem < frag:
        return False, "Faltam recursos para este reforço."
    g.forja_pedido = pedido
    if escolhe:
        it["veio"] = veio  # o caminho fica com a peça, mesmo que ela volte a +0
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
    from rpg.entidades import nome_stat
    linhas = [{"nome": nome_stat(st, rec), "antes": antes.get(st, 0), "depois": it["bonus"].get(st, 0)}
              for st in it["bonus"] if it["bonus"].get(st, 0) != antes.get(st, 0)]
    gasto = it.setdefault("reforco_gasto", {"ouro": 0, "fragmento": 0, "tentativas": 0})
    gasto["ouro"] += ouro
    gasto["fragmento"] += frag
    gasto["tentativas"] = gasto.get("tentativas", 0) + 1
    if quem:
        FICHA.atualizar(g, quem)
    g.forja_ultimo = {"id": getattr(g, "forja_ultimo", {}).get("id", 0) + 1, "tipo": "reforco", "uid": uid,
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
    if it["nome"] != nome:
        return False, "A peça mudou desde a confirmação. Escolha de novo."
    investido, propria = R.desmontar_rende(it)
    total = investido + propria
    if not total:
        return False, "Não rende material."
    if materiais(g).get("fragmento", 0) + total > R.PILHA_MAX:
        return False, f"Fragmentos no máximo ({R.PILHA_MAX})."
    g.j.mochila.remove(it)
    materiais(g)["fragmento"] = materiais(g).get("fragmento", 0) + total
    g.forja_ultimo = {"id": getattr(g, "forja_ultimo", {}).get("id", 0) + 1, "tipo": "desmonte", "nome": it["nome"],
                      "total": total}
    registrar(g, "desmontar", item=it["nome"], fragmentos=total, investimento=investido, da_peca=propria,
              prototipo="reforco")
    return True, f"Desmontado: {it['nome']} · +{total} {'Fragmento' if total == 1 else 'Fragmentos'} de Têmpera"


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
        else:
            continue
        if not ok:  # o sucesso a própria janela mostra (a bancada acende; o topo conta ouro e fragmentos)
            self.ui.efeito(texto, "info")


# ------------------------------------------------------------------ ligar ao jogo, só nesta execução
def ativar():
    from rpg.sistemas import persistencia
    from rpg.sistemas.inventario import Inventario
    from rpg.sistemas.servicos import Servicos
    from rpg.web import estado as web_estado
    if "materiais" not in persistencia.CAMPOS_SAVE:
        persistencia.CAMPOS_SAVE = persistencia.CAMPOS_SAVE + ("materiais",)
    Servicos.ferreiro = forja
    para_tela = itens.para_tela

    def para_tela_com_materiais():
        d = para_tela()
        d.update({k: {"icone": m["icone"], "nome": m["nome"], "desc": m["desc"], "hud": None}
                  for k, m in R.MATERIAIS.items()})
        return d
    itens.para_tela = para_tela_com_materiais
    heroi = web_estado.heroi

    def heroi_com_materiais(g):
        h = heroi(g)
        m = materiais(g)
        h["materiais"] = [{"id": k, "nome": d["nome"], "plural": d["plural"], "icone": d["icone"], "qtd": m.get(k, 0),
                           "desc": d["desc"], "fontes": d["fontes"]} for k, d in R.MATERIAIS.items()]
        return h
    web_estado.heroi = heroi_com_materiais
    sortear = Inventario.sortear_bau

    def sortear_bau(self):  # a exploração também dá material: o baú, metade das vezes, 1 fragmento (hipótese)
        sortear(self)
        if self.chance(0.5):
            dar_material(self, "fragmento", 1, "bau")
    Inventario.sortear_bau = sortear_bau


def preparar(g):
    """O cenário de teste: o Guerreiro no nível 4 no Vau, com Morel e Odette, 380 de ouro e as peças dos exemplos."""
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
    dar_material(g, "fragmento", 2 if os.environ.get("CASOS") else 12, "teste")
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
    if os.environ.get("CASOS"):  # os casos de conferência: a armadura de Morel já no limite (+4); poucos fragmentos
        dar_uid(g)
        ouro = g.j.ouro
        g.j.ouro, materiais(g)["fragmento"] = 9999, 99
        for _ in range(R.LIMITE):
            reforcar(g, FICHA.corpo(g, "morel")["armadura"]["uid"], teste="sucesso")
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
