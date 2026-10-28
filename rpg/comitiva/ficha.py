"""O equipamento e os atributos de cada companheiro, e a regra única de vestir, tirar e trocar peças (1.213.0).

A bolsa é do grupo: a mochila do herói, os mesmos 12 espaços (regras.LIMITE_MOCHILA); ninguém ganha outra. Cada
companheiro tem o próprio corpo (`m["equip"]`, os mesmos espaços do herói) e veste as peças de uma classe (Odette e
Yara, as de mago; Morel, as de guerreiro) e as sem classe.

Toda forma de vestir (o botão da ficha, os dois cliques, o menu do botão direito, o arrasto) passa por `vestir`, e
toda forma de tirar por `tirar`: a mesma validação (quem veste, se ele está aqui, a classe da peça, o espaço, a bolsa
cheia, a luta) e o mesmo destino para a peça que sai, decidido antes de mexer em qualquer coisa. Ou a troca acontece
inteira, ou nada muda; nenhuma peça some nem se duplica.

Atributos (números provisórios, roadmapIDEIAS/26): os seis do herói, 24 pontos iniciais pela identidade de cada um e
1 ponto livre por nível do herói (a metade dos dele). Quem entra tarde chega com os pontos dos níveis que já passaram,
livres. Os números de sempre (catálogo × nível) continuam a base; os atributos somam o que mudou desde os iniciais, então
um companheiro sem pontos gastos luta como antes. A Vontade inicial é a Tenacidade que cada um já tinha (4% por ponto).
A sugestão só gasta os pontos livres, quando o jogador pede, e nunca mexe no que ele já distribuiu.
"""

from .. import atributos as atr
from .. import itens
from ..regras import LIMITE_MOCHILA, NOMES_SLOT
from ..telemetria import registrar
from .catalogo import COMPANHEIROS

CLASSE_PECAS = {"odete": "mago", "morel": "guerreiro", "yara": "mago"}
NOME_CLASSE = {"guerreiro": "guerreiro", "arqueiro": "arqueiro", "mago": "mago"}

INICIAIS = {
    "odete": dict(forca=2, agilidade=3, constituicao=4, intelecto=6, percepcao=3, vontade=6),
    "morel": dict(forca=7, agilidade=3, constituicao=7, intelecto=1, percepcao=3, vontade=3),
    "yara": dict(forca=1, agilidade=3, constituicao=3, intelecto=7, percepcao=3, vontade=7),
}
# a ordem da sugestão (cíclica): a identidade de cada um
SUGESTAO = {"odete": ("vontade", "intelecto", "constituicao"), "morel": ("constituicao", "forca", "vontade"),
            "yara": ("intelecto", "percepcao", "vontade")}
PONTOS_POR_NIVEL = 1
# os valores que as peças e os atributos mudam (os especiais, como o crítico, entram pelos modificadores do item)
STATS = ("max_hp", "atk", "poder", "defesa", "agi", "max_rec")

HEROI = "heroi"


# ------------------------------------------------------------ campos do membro
def preparar(m, nivel_heroi):
    """Os campos novos de um membro (recrutado agora ou de um save antigo): o corpo vazio, os atributos iniciais e os
    pontos dos níveis que o herói já subiu, livres. Rodar de novo não muda nada."""
    m.setdefault("equip", {s: None for s in itens.SLOTS})
    for s in itens.SLOTS:
        m["equip"].setdefault(s, None)
    if "atributos" not in m:
        m["atributos"] = dict(INICIAIS[m["id"]])
        m["pontos_atributo"] = max(0, nivel_heroi - 1) * PONTOS_POR_NIVEL
    m.setdefault("pontos_atributo", 0)
    return m


def atributos_de(m):
    return m.get("atributos") or INICIAIS[m["id"]]


def equip_de(m):
    return m.get("equip") or {}


def extras(m):
    """O que somam aos números do catálogo: os atributos acima dos iniciais e as peças vestidas. {stat: valor}"""
    agora = atr.contribuicao(type("_", (), {"atributos": atributos_de(m)})())
    antes = atr.contribuicao(type("_", (), {"atributos": INICIAIS[m["id"]]})())
    soma = {s: agora.get(s, 0) - antes.get(s, 0) for s in STATS}
    for it in equip_de(m).values():
        if it:
            for s in STATS:
                soma[s] += it["bonus"].get(s, 0)
    return soma


def critico_extra(m):
    """A Percepção acima da inicial (+1% por ponto); o resto do crítico é o de sempre (grimorio.chance_critico)."""
    return (atributos_de(m)["percepcao"] - INICIAIS[m["id"]]["percepcao"]) * atr.CRITICO_POR_PONTO


# ------------------------------------------------------------ quem é quem
def nome_de(g, quem):
    return g.j.nome if quem == HEROI else COMPANHEIROS[quem]["curto"]


def membro_de(g, quem):
    from .grupo import membro
    return membro(g, quem)


def personagens(g):
    """Quem aparece na janela: o herói e a comitiva (quem espera no acampamento, não)."""
    from .grupo import membros
    return [HEROI] + [m["id"] for m in membros(g)]


def corpo(g, quem):
    if quem == HEROI:
        return g.j.equip
    m = membro_de(g, quem)
    return preparar(m, g.j.nivel)["equip"] if m else None


def classe_pecas(g, quem):
    return g.j.classe if quem == HEROI else CLASSE_PECAS[quem]


def motivo_indisponivel(g, quem):
    """Por que não dá para mexer no equipamento de alguém agora (ou None). O ferido pode ser equipado; quem não está
    aqui (grupo.fora), não. Na luta, a janela não troca nada (a arma do herói se troca na roda, na vez dele)."""
    if getattr(g, "combate_ativo", None) is not None:
        return "Troque o equipamento fora da luta."
    if quem == HEROI:
        return None
    from .grupo import fora
    m = membro_de(g, quem)
    if not m:
        return f"{nome_de(g, quem)} não está na comitiva."
    motivo = fora(g, m)  # {"curto": "espera fora do Vau", "texto": ...} (caspar.py) ou um texto
    if not motivo:
        return None
    return f"{nome_de(g, quem)} não está aqui: {motivo['curto'] if isinstance(motivo, dict) else motivo}."


def motivo_nao_veste(g, quem, item):
    """A peça é de uma classe que esta pessoa não usa, ou pede um nível que ela não tem (o requisito da forja), ou None.
    Vale em todos os caminhos de vestir do Inventário (clique duplo, menu, arrastar, troca entre personagens)."""
    from ..forja.oficina import motivo_requisito
    return motivo_classe(g, quem, item) or motivo_requisito(g, quem, item)


def motivo_classe(g, quem, item):
    """A peça é de uma classe que esta pessoa não usa (ou None): só a classe, sem o nível."""
    if not item.get("classe") or item["classe"] == classe_pecas(g, quem):
        return None
    if quem == HEROI:
        return "Você não sabe usar isso."
    return f"{nome_de(g, quem)} não usa peças de {NOME_CLASSE.get(item['classe'], item['classe'])}."


def onde_esta(g, item):
    """("bolsa", índice) ou (quem, espaço) de uma peça, pela identidade (duas peças iguais são duas peças)."""
    for i, it in enumerate(g.j.mochila):
        if it is item:
            return ("bolsa", i)
    for quem in personagens(g):
        for s, it in (corpo(g, quem) or {}).items():
            if it is item:
                return (quem, s)
    return None


def espaco_para(g, quem, item, destino=None):
    """O espaço onde a peça entra: o pedido (se serve), o único do tipo, ou o anel vazio. Com os dois anéis ocupados e
    nenhum pedido, None: quem joga escolhe qual sai."""
    opcoes = itens.espacos(item["slot"])
    if destino is not None:
        return destino if destino in opcoes else None
    if len(opcoes) == 1:
        return opcoes[0]
    eq = corpo(g, quem)
    return next((s for s in opcoes if not eq.get(s)), None)


# ------------------------------------------------------------ depois de mexer
def atualizar(g, quem):
    """Os números de quem mudou de peça ou de atributo. A vida acompanha o máximo para baixo (como no herói); o que o
    máximo ganha não cura."""
    if quem == HEROI:
        g.j.recalcular()
        return
    from .grupo import atributos
    m = membro_de(g, quem) or _na_reserva(g, quem)
    if not m:
        return
    m["max_hp"] = atributos(g, m)["max_hp"]
    m["hp"] = min(m["hp"], m["max_hp"])


def _na_reserva(g, quem):
    from .grupo import na_reserva
    return na_reserva(g, quem)


# ------------------------------------------------------------ vestir, tirar, reordenar
def avaliar_vestir(g, quem, item, destino=None):
    """O plano de vestir `item` em `quem` (no espaço `destino`, se dado), sem mexer em nada. Devolve (plano, motivo):
    com motivo, não dá. O plano diz de onde a peça sai, o espaço, a que está lá e para onde ela vai."""
    motivo = motivo_indisponivel(g, quem)
    if motivo:
        return None, motivo
    origem = onde_esta(g, item)
    if origem is None:
        return None, "Essa peça não está com o grupo."
    motivo = motivo_nao_veste(g, quem, item)
    if motivo:
        return None, motivo
    espaco = espaco_para(g, quem, item, destino)
    if espaco is None:
        if destino is not None:
            return None, f"{item['nome']} não vai em {NOMES_SLOT.get(destino, destino)}."
        return None, "Os dois anéis estão ocupados: escolha qual substituir."
    if origem == (quem, espaco):
        return None, f"{item['nome']} já está aí."
    dono = origem[0] if origem[0] != "bolsa" else None
    if dono is not None and dono != quem:
        motivo = motivo_indisponivel(g, dono)
        if motivo:
            return None, motivo
    antigo = corpo(g, quem)[espaco]
    # para onde vai a peça que estava no espaço: para o lugar de onde a nova saiu (na bolsa ou, no mesmo corpo, o
    # outro anel); de outra pessoa, para a bolsa, se houver espaço
    if antigo is None:
        destino_antigo = None
    elif origem[0] == "bolsa":
        destino_antigo = ("bolsa", origem[1])
    elif dono == quem:
        destino_antigo = (quem, origem[1])
    elif len(g.j.mochila) < LIMITE_MOCHILA:
        destino_antigo = ("bolsa", None)
    else:
        return None, (f"A bolsa está cheia ({LIMITE_MOCHILA} de {LIMITE_MOCHILA}): {antigo['nome']}, que "
                      f"{nome_de(g, quem) if quem != HEROI else 'você'} usa, não teria para onde ir.")
    return {"quem": quem, "item": item, "origem": origem, "espaco": espaco, "antigo": antigo,
            "destino_antigo": destino_antigo}, None


def vestir(g, quem, item, destino=None):
    """Veste a peça (da bolsa ou de outra pessoa) em `quem`. Devolve (ok, texto): o texto diz o que aconteceu ou por
    que não. Tudo validado antes; depois, as mudanças acontecem juntas."""
    plano, motivo = avaliar_vestir(g, quem, item, destino)
    if motivo:
        return False, motivo
    origem, espaco, antigo, para = plano["origem"], plano["espaco"], plano["antigo"], plano["destino_antigo"]
    eq = corpo(g, quem)
    if origem[0] == "bolsa":
        if para == ("bolsa", origem[1]):
            g.j.mochila[origem[1]] = antigo  # a que sai fica no lugar exato da que entrou
        else:
            del g.j.mochila[origem[1]]
    else:
        corpo(g, origem[0])[origem[1]] = None
    eq[espaco] = item
    if para is not None and para[0] == "bolsa" and para[1] is None:
        g.j.mochila.append(antigo)
    elif para is not None and para[0] not in ("bolsa",):
        corpo(g, para[0])[para[1]] = antigo
    atualizar(g, quem)
    if origem[0] not in ("bolsa", quem):
        atualizar(g, origem[0])
    quem_txt = "Você equipa" if quem == HEROI else f"{nome_de(g, quem)} equipa"
    partes = [f"{quem_txt} {item['nome']}"]
    if origem[0] not in ("bolsa", quem):
        partes[0] += f" (era {'sua' if origem[0] == HEROI else 'de ' + nome_de(g, origem[0])})"
    if antigo is not None:
        partes.append(f"{antigo['nome']} {'volta para a bolsa' if para[0] == 'bolsa' else 'vai para ' + NOMES_SLOT[para[1]]}")
    registrar(g, "equipar" if quem == HEROI else "comitiva_equipar", item=item["nome"], slot=espaco,
              raridade=item.get("raridade", "comum"), bonus=item["bonus"], **({} if quem == HEROI else {"em": quem}),
              **({"de": origem[0]} if origem[0] != "bolsa" else {}))
    return True, "; ".join(partes) + "."


def avaliar_tirar(g, quem, espaco):
    motivo = motivo_indisponivel(g, quem)
    if motivo:
        return motivo
    eq = corpo(g, quem)
    if eq is None or espaco not in eq:
        return "Esse espaço não existe."
    if eq[espaco] is None:
        return f"{NOMES_SLOT.get(espaco, espaco)} já está vazio."
    if len(g.j.mochila) >= LIMITE_MOCHILA:
        return f"A bolsa está cheia ({LIMITE_MOCHILA} de {LIMITE_MOCHILA}). Libere um espaço antes de tirar {eq[espaco]['nome']}."
    return None


def tirar(g, quem, espaco, posicao=None):
    """Tira a peça e guarda na bolsa (na posição pedida, se houver: o arrasto até uma célula)."""
    motivo = avaliar_tirar(g, quem, espaco)
    if motivo:
        return False, motivo
    eq = corpo(g, quem)
    item = eq[espaco]
    eq[espaco] = None
    if posicao is None or not 0 <= posicao <= len(g.j.mochila):
        g.j.mochila.append(item)
    else:
        g.j.mochila.insert(posicao, item)
    atualizar(g, quem)
    registrar(g, "desequipar", item=item["nome"], slot=espaco, **({} if quem == HEROI else {"em": quem}))
    return True, f"{item['nome']} volta para a bolsa."


def mover_na_bolsa(g, de, para):
    """Reordena a bolsa: a peça da posição `de` vai para a posição `para` (as outras andam uma casa)."""
    mochila = g.j.mochila
    if not (0 <= de < len(mochila)) or not (0 <= para < LIMITE_MOCHILA) or de == para:
        return False
    item = mochila.pop(de)
    mochila.insert(min(para, len(mochila)), item)
    return True


# ------------------------------------------------------------ atributos
def motivo_atributo(g, quem, a):
    m = membro_de(g, quem)
    if not m:
        return f"{nome_de(g, quem)} não está na comitiva."
    if getattr(g, "combate_ativo", None) is not None:
        return "Distribua fora da luta."
    longe = motivo_indisponivel(g, quem)
    if longe:
        return longe
    if a not in atr.ATRIBUTOS:
        return "Esse atributo não recebe pontos."
    if not preparar(m, g.j.nivel)["pontos_atributo"]:
        return "Sem pontos para distribuir."
    if m["atributos"][a] >= atr.ATRIBUTO_MAX:
        return f"{atr.NOMES[a]} já está no máximo ({atr.ATRIBUTO_MAX})."
    return None


def gastar_atributo(g, quem, a):
    """Um ponto livre num atributo do companheiro. A vida que o máximo ganha vem junto (como no herói)."""
    if motivo_atributo(g, quem, a):
        return False
    m = membro_de(g, quem)
    antes = m["max_hp"]
    m["atributos"] = dict(m["atributos"], **{a: m["atributos"][a] + 1})
    m["pontos_atributo"] -= 1
    atualizar(g, quem)
    m["hp"] = min(m["max_hp"], m["hp"] + max(0, m["max_hp"] - antes))
    registrar(g, "ponto_atributo", atributo=a, valor=m["atributos"][a], em=quem)
    return True


def sugestao(quem, n, atuais):
    """Onde a sugestão poria n pontos (a ordem da identidade, cíclica; pula o que chegou ao máximo)."""
    ordem = SUGESTAO[quem]
    valores = dict(atuais)
    escolhidos = []
    k = 0
    while len(escolhidos) < n and k < n * len(ordem) + len(ordem):
        a = ordem[k % len(ordem)]
        k += 1
        if valores[a] < atr.ATRIBUTO_MAX:
            valores[a] += 1
            escolhidos.append(a)
    return escolhidos


def distribuir_sugestao(g, quem):
    """Gasta os pontos livres pela sugestão. Só os livres: o que já foi distribuído fica como está. Devolve quantos."""
    m = membro_de(g, quem)
    if not m or motivo_indisponivel(g, quem):  # na luta ou longe: nada muda
        return 0
    n = 0
    for a in sugestao(quem, m.get("pontos_atributo", 0), atributos_de(m)):
        if gastar_atributo(g, quem, a):
            n += 1
    return n


# ------------------------------------------------------------ quem sai
def devolver_pecas(g, m):
    """Quem deixa a comitiva de vez (dispensado, foi embora) devolve as peças à bolsa do grupo: elas são do grupo. O
    que não couber chega como um achado, uma peça de cada vez, na janela de sempre (vestir, guardar ou, sem espaço,
    deixar para trás: a escolha é do jogador). Nenhuma peça some sem ele decidir. Devolve as peças que voltaram."""
    pecas = [it for it in equip_de(m).values() if it]
    for s in list(equip_de(m)):
        m["equip"][s] = None
    if not pecas:
        return []
    cabem = pecas[:max(0, LIMITE_MOCHILA - len(g.j.mochila))]
    g.j.mochila.extend(cabem)
    nome = COMPANHEIROS[m["id"]]["curto"]
    if cabem:
        g.dizer(f"{nome} deixa o que usava do grupo: {', '.join(it['nome'] for it in cabem)} "
                f"{'volta' if len(cabem) == 1 else 'voltam'} para a bolsa.", "cinza")
    registrar(g, "comitiva", acao="devolve", id=m["id"], pecas=len(pecas), na_bolsa=len(cabem))
    for it in pecas[len(cabem):]:
        g.dizer(f"A bolsa está cheia: {it['nome']}, que {nome} usava, fica com você para decidir.", "cinza")
        g.oferecer_equip(it)
    return pecas


# ------------------------------------------------------------ para a ficha da tela
def partes(g, m, stat):
    """De onde vem um número do companheiro, pela mesma conta de grupo.atributos: o catálogo no nível do herói, os
    pontos de atributo acima dos iniciais e as peças. [(rótulo, valor)], sem as partes zeradas."""
    from ..balanceamento import RECURSO_COMITIVA
    d = COMPANHEIROS[m["id"]]
    nv = g.j.nivel - 1
    chave = {"max_hp": "hp", "atk": "atk", "poder": "poder", "defesa": "defesa", "agi": "agi"}.get(stat)
    base = RECURSO_COMITIVA if stat == "max_rec" else d["base"][chave] + d["cresc"].get(chave, 0) * nv
    agora = atr.contribuicao(type("_", (), {"atributos": atributos_de(m)})())
    antes = atr.contribuicao(type("_", (), {"atributos": INICIAIS[m["id"]]})())
    lista = [(f"{d['curto']} no nível {g.j.nivel}", base), ("pontos de atributo", agora.get(stat, 0) - antes.get(stat, 0)),
             ("equipamento", sum(it["bonus"].get(stat, 0) for it in equip_de(m).values() if it))]
    return [p for p in lista if abs(p[1]) >= 0.05 or p is lista[0]]


def combatente(g, m):
    """O companheiro como a luta o monta (luta.preparar_combate), para a ficha mostrar o crítico e a Tenacidade de
    verdade: os números, as peças e a Percepção acima da inicial."""
    from .grupo import atributos
    at = atributos(g, m)
    return type("_", (), {"agi": at["agi"], "equip": equip_de(m), "critico_atributo": critico_extra(m),
                          "vontade": atributos_de(m)["vontade"]})()
