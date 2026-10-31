"""A montagem de uma build no protótipo X1: o kit (5 das 8 habilidades da especialização, mais a ultimate fixa) e os
talentos (7 pontos numa das duas estruturas). Valida o orçamento, os ranks, as linhas e as exclusões, diz o que cada
nó muda nas habilidades equipadas e entrega ao combate as bandeiras de efeito.

Uma montagem é um dicionário: {"estrutura": "t4"|"t1", "spec": "berserker"|"piromante", "kit": [...],
"nos": {id: rank}, "nome": opcional}."""
from . import conteudo as C


def arvore(m):
    return C.ARVORES[(m["estrutura"], m["spec"])]


def no_por_id(m):
    return {n["id"]: n for n in arvore(m)}


def pontos_gastos(m, nos=None):
    idx = no_por_id(m)
    nos = m["nos"] if nos is None else nos
    return sum(idx[i]["custo"] * r for i, r in nos.items() if i in idx)


def _pontos_ate(m, nos, linha):
    """Pontos gastos nas linhas anteriores a `linha`."""
    idx = no_por_id(m)
    return sum(idx[i]["custo"] * r for i, r in nos.items() if i in idx and idx[i].get("linha", 1) < linha)


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
    for i in nos:
        n = idx[i]
        req = C.REQUISITO_LINHA.get(n.get("linha", 1), 0)
        if req and _pontos_ate(m, nos, n["linha"]) < req:
            out.append(f"{n['nome']}: a linha {n['linha']} pede {req} pontos nas linhas anteriores")
    grupos = {}
    for i in nos:
        g = idx[i].get("exclui")
        if g:
            grupos.setdefault(g, []).append(idx[i]["nome"])
    for nomes in grupos.values():
        if len(nomes) > 1:
            out.append(f"Versões da mesma habilidade: {' e '.join(nomes)}")
    return out


def efeitos(m):
    """As bandeiras que o combate lê: {bandeira: valor}. Números somam por rank."""
    idx = no_por_id(m)
    out = {}
    for i, r in m["nos"].items():
        for k, v in idx[i]["efeitos"].items():
            out[k] = out.get(k, 0) + v * r
    return out


def _etiquetas_kit(m):
    tags = set()
    for h in m["kit"] + [C.HEROI[m["spec"]]["ultimate"], "atacar"]:
        tags.update(C.HABILIDADES[h]["etiquetas"])
    return tags


def afeta_no_kit(m, n):
    """Os nomes das habilidades do kit (com a ultimate e o Atacar) que o nó muda, ou o alcance quando não depende do kit."""
    if n.get("versao"):
        return [C.HABILIDADES[n["versao"]]["nome"]] if n["versao"] in m["kit"] else []
    nomes = []
    for h in m["kit"] + [C.HEROI[m["spec"]]["ultimate"], "atacar"]:
        if set(C.HABILIDADES[h]["etiquetas"]) & set(n["afeta"]):
            nomes.append(C.HABILIDADES[h]["nome"])
    if "aliados" in n["afeta"]:
        nomes.append("golpes de Morel e Odette")
    if "recebe" in n["afeta"]:
        nomes.append("golpes que você recebe")
    if "sempre" in n["afeta"] and not nomes:
        nomes.append("você")
    return nomes


def aviso_no(m, n):
    """O que deixa o nó sem efeito com o kit de agora (uma linha), ou None."""
    if n.get("versao") and n["versao"] not in m["kit"]:
        return f"{C.HABILIDADES[n['versao']]['nome']} não está no kit"
    req = n.get("requer_etiqueta")
    if req and req not in _etiquetas_kit(m):
        return "Só funciona na Fúria: Rugido não está no kit"
    if not n.get("versao") and not afeta_no_kit(m, n):
        return "Nada no kit usa isto agora"
    return None


def estado_arvore(m):
    """Cada nó com o que a tela precisa: rank, custo, se dá para comprar ou tirar mais um ponto e por quê."""
    idx = no_por_id(m)
    gasto = pontos_gastos(m)
    out = []
    for n in arvore(m):
        r = m["nos"].get(n["id"], 0)
        mais = dict(m["nos"], **{n["id"]: r + 1})
        menos = dict(m["nos"])
        if r > 1:
            menos[n["id"]] = r - 1
        else:
            menos.pop(n["id"], None)
        pode_mais, motivo_mais = True, ""
        if r >= n["ranks"]:
            pode_mais, motivo_mais = False, "No máximo"
        elif gasto + n["custo"] > C.PONTOS:
            falta = gasto + n["custo"] - C.PONTOS
            pode_mais, motivo_mais = False, f"Falta{'m' if falta > 1 else ''} {falta} ponto{'s' if falta > 1 else ''}"
        else:
            req = C.REQUISITO_LINHA.get(n.get("linha", 1), 0)
            if req and _pontos_ate(m, m["nos"], n["linha"]) < req:
                pode_mais, motivo_mais = False, f"Requer {req} pontos nas linhas anteriores"
            elif n.get("exclui"):
                rival = next((idx[i]["nome"] for i in m["nos"] if i != n["id"] and idx[i].get("exclui") == n["exclui"]),
                             None)
                if rival:
                    pode_mais, motivo_mais = False, f"Exclui {rival}"
        pode_menos, motivo_menos = r > 0, ""
        if r > 0 and erros(m, menos):
            linhas = sorted({idx[i]["linha"] for i in menos if idx[i].get("linha", 1) > n.get("linha", 1)
                             and C.REQUISITO_LINHA[idx[i]["linha"]] > _pontos_ate(m, menos, idx[i]["linha"])})
            pode_menos = False
            motivo_menos = f"Sustenta a linha {linhas[0]}" if linhas else "Sustenta outro talento"
        out.append({"id": n["id"], "nome": n["nome"], "tipo": n["tipo"], "nome_tipo": C.NOME_TIPO[n["tipo"]],
                    "custo": n["custo"], "ranks": n["ranks"], "rank": r, "linha": n.get("linha"),
                    "texto": n["texto"], "versao": C.HABILIDADES[n["versao"]]["nome"] if n.get("versao") else None,
                    "afeta": afeta_no_kit(m, n), "aviso": aviso_no(m, n),
                    "pode_mais": pode_mais and not erros(m, mais), "motivo_mais": motivo_mais,
                    "pode_menos": pode_menos, "motivo_menos": motivo_menos})
    return out


def custo_habilidade(m_efeitos, hid):
    h = C.HABILIDADES[hid]
    for flag, (alvo, custo) in C.VERSAO_CUSTO.items():
        if alvo == hid and m_efeitos.get(flag):
            return custo
    return h["custo"]


def kit_descrito(m):
    """As habilidades equipadas como a montagem as deixa: a descrição (a da versão, se houver) e as linhas das regras
    que valem para cada uma."""
    idx = no_por_id(m)
    ef = efeitos(m)
    out = []
    for hid in m["kit"] + [C.HEROI[m["spec"]]["ultimate"]]:
        h = C.HABILIDADES[hid]
        desc, versao, notas = h["desc"], None, []
        for i in m["nos"]:
            n = idx[i]
            if n.get("versao") == hid:
                desc, versao = n["nota"], n["nome"]
            elif not n.get("versao") and set(h["etiquetas"]) & set(n["afeta"]):
                notas.append(n["nota"] if n["tipo"] != "N" else f"{n['nome']} ×{m['nos'][i]}: {n['texto']}")
        out.append({"id": hid, "nome": h["nome"], "versao": versao, "custo": custo_habilidade(ef, hid),
                    "ultimate": bool(h.get("ultimate")), "alvo": h["alvo"], "tipo": C.TIPOS.get(h.get("tipo")),
                    "desc": desc, "notas": notas})
    return out


def ficha(m):
    """Tudo o que a tela de montagem mostra, de uma vez."""
    e = erros(m)
    return {"montagem": m, "erros": e, "valida": not e, "pontos": pontos_gastos(m) if not any(
        "desconhecid" in x for x in e) else 0, "orcamento": C.PONTOS, "espacos": C.ESPACOS,
            "arvore": estado_arvore(m) if not any("desconhecid" in x for x in e) else [],
            "kit": kit_descrito(m) if not e else [],
            "pool": [{"id": h, "nome": C.HABILIDADES[h]["nome"], "custo": C.HABILIDADES[h]["custo"],
                      "desc": C.HABILIDADES[h]["desc"], "no_kit": h in m["kit"]} for h in C.POOL[m["spec"]]]}


def de_exemplo(eid):
    ex = next(x for x in C.EXEMPLOS if x["id"] == eid)
    return {"estrutura": ex["estrutura"], "spec": ex["spec"], "kit": list(ex["kit"]), "nos": dict(ex["nos"]),
            "nome": ex["nome"]}
