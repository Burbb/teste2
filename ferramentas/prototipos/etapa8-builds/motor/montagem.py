"""A montagem de uma build no protótipo X1: o kit (5 das 14 habilidades da especialização e uma das duas ultimates) e os
talentos (9 pontos numa das duas estruturas). Valida o orçamento, os ranks e as exclusões, diz o que cada nó muda em
cada habilidade do repertório e entrega ao combate as bandeiras de efeito.

Uma montagem é um dicionário: {"estrutura": "t4"|"t1", "spec": "berserker"|"piromante", "kit": [...],
"ultimate": id, "nos": {id: rank}, "nome": opcional}. Não há ordem de compra (sem linhas)."""
from . import conteudo as C


def arvore(m):
    return C.ARVORES[(m["estrutura"], m["spec"])]


def no_por_id(m):
    return {n["id"]: n for n in arvore(m)}


def ultimate(m):
    ults = C.HEROI[m["spec"]]["ultimates"]
    return m.get("ultimate") if m.get("ultimate") in ults else ults[0]


def repertorio(m):
    """As habilidades que a especialização pode levar: as 14 e as duas ultimates."""
    return C.POOL[m["spec"]] + C.HEROI[m["spec"]]["ultimates"]


def equipadas(m):
    return list(m["kit"]) + [ultimate(m)]


def pontos_gastos(m, nos=None):
    idx = no_por_id(m)
    nos = m["nos"] if nos is None else nos
    return sum(idx[i]["custo"] * r for i, r in nos.items() if i in idx)


def erros(m, nos=None):
    """Os problemas da montagem (lista vazia: válida). Mensagens curtas, para a tela."""
    nos = m["nos"] if nos is None else nos
    out = []
    if (m.get("estrutura"), m.get("spec")) not in C.ARVORES:
        return ["Estrutura ou especialização desconhecida"]
    pool = C.POOL[m["spec"]]
    kit = m.get("kit", [])
    if len(set(kit)) != len(kit):
        out.append("Habilidade repetida no kit")
    if any(h not in pool for h in kit):
        out.append("Habilidade de outra especialização no kit")
    if len(kit) > C.ESPACOS:
        out.append(f"Kit com {len(kit)} habilidades: o limite é {C.ESPACOS}")
    if m.get("ultimate") and m["ultimate"] not in C.HEROI[m["spec"]]["ultimates"]:
        out.append("Ultimate de outra especialização")
    idx = no_por_id(m)
    for i, r in nos.items():
        if i not in idx:
            out.append(f"Talento desconhecido: {i}")
        elif not 1 <= r <= idx[i]["ranks"]:
            out.append(f"{idx[i]['nome']}: {r} pontos (o máximo é {idx[i]['ranks']})")
    if out:
        return out
    gasto = pontos_gastos(m, nos)
    if gasto > C.PONTOS:
        out.append(f"{gasto} pontos gastos: o orçamento é {C.PONTOS}")
    grupos = {}
    for i in nos:
        g = idx[i].get("exclui")
        if g:
            grupos.setdefault(g, []).append(idx[i]["nome"])
    for nomes in grupos.values():
        if len(nomes) > 1:
            out.append(f"Não combinam: {' e '.join(nomes)}")
    return out


def efeitos(m):
    """As bandeiras que o combate lê: {bandeira: valor}. Números somam por rank."""
    idx = no_por_id(m)
    out = {}
    for i, r in m["nos"].items():
        for k, v in idx[i]["efeitos"].items():
            out[k] = out.get(k, 0) + v * r
    return out


def _etiquetas(hids):
    tags = set()
    for h in hids:
        tags.update(C.HABILIDADES[h]["etiquetas"])
    return tags


def _muda(n, hid):
    """Se o nó muda a habilidade."""
    if n.get("versao"):
        return n["versao"] == hid
    return bool(set(C.HABILIDADES[hid]["etiquetas"]) & set(n["afeta"]))


def alcance(m, n):
    """O que o nó muda: as habilidades do repertório (com a marca de quais estão equipadas) e o que não depende do kit."""
    eq = equipadas(m)
    habs = [{"id": h, "nome": C.HABILIDADES[h]["nome"], "no_kit": h in eq or h == "atacar"}
            for h in repertorio(m) + ["atacar"] if _muda(n, h)]
    outros = []
    if "aliados" in n["afeta"]:
        outros.append("golpes de Morel e Odette")
    if "recebe" in n["afeta"]:
        outros.append("golpes que você recebe")
    if "sempre" in n["afeta"]:
        outros.append("você")
    return habs, outros


def aviso_no(m, n):
    """O que deixa o nó sem efeito com o kit de agora (uma linha), ou None."""
    eq = equipadas(m)
    if n.get("versao") and n["versao"] not in eq:
        return f"{C.HABILIDADES[n['versao']]['nome']} não está no kit"
    req = n.get("requer_etiqueta")
    if req and req not in _etiquetas(eq):
        return "Só funciona na Fúria: Rugido não está no kit"
    habs, outros = alcance(m, n)
    if not n.get("versao") and not outros and not any(h["no_kit"] for h in habs):
        return "Nada no kit usa isto agora"
    return None


def estado_arvore(m):
    """Cada nó com o que a tela precisa: rank, custo, alcance, e se dá para pôr ou tirar um ponto (e por quê)."""
    idx = no_por_id(m)
    gasto = pontos_gastos(m)
    out = []
    for n in arvore(m):
        r = m["nos"].get(n["id"], 0)
        pode_mais, motivo = True, ""
        if r >= n["ranks"]:
            pode_mais, motivo = False, "No máximo"
        elif gasto + n["custo"] > C.PONTOS:
            falta = gasto + n["custo"] - C.PONTOS
            pode_mais, motivo = False, f"Falta{'m' if falta > 1 else ''} {falta} ponto{'s' if falta > 1 else ''}"
        elif n.get("exclui"):
            rival = next((idx[i]["nome"] for i in m["nos"] if i != n["id"] and idx[i].get("exclui") == n["exclui"]),
                         None)
            if rival:
                pode_mais, motivo = False, f"Não combina com {rival}"
        habs, outros = alcance(m, n)
        props = set(n["props"])
        for h in habs:
            props.update(C.HABILIDADES[h["id"]]["props"])
        out.append({"id": n["id"], "nome": n["nome"], "tipo": n["tipo"], "nome_tipo": C.NOME_TIPO[n["tipo"]],
                    "custo": n["custo"], "ranks": n["ranks"], "rank": r, "texto": n["texto"],
                    "versao": C.HABILIDADES[n["versao"]]["nome"] if n.get("versao") else None,
                    "alcance": habs, "outros": outros, "aviso": aviso_no(m, n), "equivale": n.get("equivale"),
                    "props": sorted(props, key=C.PROPRIEDADES.index), "pode_mais": pode_mais, "motivo_mais": motivo,
                    "pode_menos": r > 0})
    return out


def custo_habilidade(m_efeitos, hid):
    for flag, (alvo, custo) in C.VERSAO_CUSTO.items():
        if alvo == hid and m_efeitos.get(flag):
            return custo
    return C.HABILIDADES[hid]["custo"]


def descrever(m, hid):
    """A habilidade como a montagem a deixa: a descrição (a da versão, se houver) e uma linha por regra que vale para
    ela."""
    idx = no_por_id(m)
    ef = efeitos(m)
    h = C.HABILIDADES[hid]
    desc, versao, notas = h["desc"], None, []
    for i, r in m["nos"].items():
        n = idx[i]
        if n.get("versao") == hid:
            desc, versao = n["nota"], n["nome"]
        elif not n.get("versao") and _muda(n, hid):
            notas.append(n["nota"] if n["tipo"] != "N" else f"{n['nome']} ×{r}: {n['texto'][0].lower()}{n['texto'][1:]}")
    return {"id": hid, "nome": h["nome"], "versao": versao, "custo": custo_habilidade(ef, hid),
            "ultimate": bool(h.get("ultimate")), "alvo": h["alvo"], "tipo": C.TIPOS.get(h.get("tipo")), "desc": desc,
            "notas": notas, "funcao": h["funcao"], "props": h["props"], "origem": h["origem"],
            "no_kit": hid in equipadas(m)}


def kit_descrito(m):
    return [descrever(m, h) for h in equipadas(m)]


def ficha(m):
    """Tudo o que a tela de montagem mostra, de uma vez."""
    e = erros(m)
    base = not any("desconhecid" in x for x in e)
    heroi = C.HEROI[m["spec"]]
    return {"montagem": dict(m, ultimate=ultimate(m)), "erros": e, "valida": not e,
            "pontos": pontos_gastos(m) if base else 0, "orcamento": C.PONTOS, "espacos": C.ESPACOS,
            "arvore": estado_arvore(m) if base else [],
            "kit": kit_descrito(m) if not e else [],
            "repertorio": [descrever(m, h) for h in repertorio(m)] if base else [],
            "classe": heroi["classe"], "spec_nome": heroi["spec"]}


def de_exemplo(eid):
    ex = next(x for x in C.EXEMPLOS if x["id"] == eid)
    return {"estrutura": ex["estrutura"], "spec": ex["spec"], "kit": list(ex["kit"]), "ultimate": ex["ultimate"],
            "nos": dict(ex["nos"]), "nome": ex["nome"]}
