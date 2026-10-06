"""Fotografia do estado do jogo em JSON, para a interface web desenhar painéis, mapa e combate."""

from .. import comitiva, mapa, sobrevivencia
from ..classes import CLASSES, HABILIDADES
from ..combate import NOMES_EFEITOS
from ..dados import BIOMAS, CLIMAS, PERIODOS
from ..itens import CONSUMIVEIS, descrever_bonus, rotulo
from ..mundo import nivel_regiao


def _efeitos(c):
    return [{"nome": ef.get("r", NOMES_EFEITOS.get(n, n)), "id": n, "turnos": ef["t"]} for n, ef in c.efeitos.items()]


def _item(it):
    if not it:
        return None
    return {"nome": rotulo(it), "raridade": it.get("raridade", "comum"), "bonus": descrever_bonus(it["bonus"]),
            "nivel": it.get("nivel")}


def heroi(g):
    j = g.j
    ferimentos = []
    for f in j.ferimentos:
        d = sobrevivencia.FERIMENTOS[f["id"]]
        ferimentos.append({"nome": d["nome"], "dias": f.get("dias") if d["dias"] else None,
                           "aberto": bool(d.get("aberto") and not f.get("tratado"))})
    return {
        "nome": j.nome, "classe": j.classe, "classe_nome": CLASSES[j.classe]["nome"], "titulo": j.nome_classe,
        "nivel": j.nivel, "xp": j.xp, "xp_proximo": j.xp_proximo(),
        "hp": j.hp, "max_hp": j.max_hp, "rec": j.rec, "max_rec": j.max_rec, "recurso": j.nome_recurso,
        "atributos": {"Ataque": j.atk, "Defesa": j.defesa, "Agilidade": j.agi, "Poder": j.poder},
        "ouro": j.ouro, "reputacao": j.reputacao, "flechas": j.flechas if j.classe == "arqueiro" else None,
        "provisoes": j.provisoes, "fome": j.fome, "tochas": j.consumiveis.get("tocha", 0),
        "pocoes": j.consumiveis.get("pocao_vida", 0),
        "bolsa": [{"nome": CONSUMIVEIS[k]["nome"], "qtd": v, "desc": CONSUMIVEIS[k]["desc"]}
                  for k, v in j.consumiveis.items() if v > 0 and k in CONSUMIVEIS],
        "equip": {slot: _item(it) for slot, it in j.equip.items()},
        "mochila": [_item(it) for it in j.mochila],
        "habilidades": [{"nome": HABILIDADES[h]["nome"], "custo": HABILIDADES[h]["custo"], "desc": HABILIDADES[h]["desc"]}
                        for h in j.habilidades],
        "ferimentos": ferimentos, "males": sobrevivencia.descrever(j),
        "pontos_talento": j.pontos_talento, "sigilos": len(j.sigilos),
        "companheiro": ({"nome": j.companheiro["nome"], "hp": j.companheiro["hp"], "max_hp": j.companheiro["max_hp"]}
                        if j.companheiro else None),
        "efeitos": _efeitos(j),
        "comitiva": comitiva.estado(g),
    }


def mapa_conhecido(g):
    locais = g.mundo["locais"]
    vistos = mapa.conhecidos(g)
    atual = g.loc["id"]
    vizinhos = {int(i): d for i, d in g.loc["con"].items()}
    nos, estradas = [], []
    for loc in locais:
        if loc["id"] not in vistos:
            continue
        covil = mapa.covil_conhecido(g, loc)
        nos.append({
            "id": loc["id"], "n": loc["id"] + 1, "nome": loc["nome"], "x": loc["x"], "y": loc["y"],
            "tipo": loc["tipo"], "bioma": loc["bioma"], "visitado": loc["visitado"], "atual": loc["id"] == atual,
            "distancia": vizinhos.get(loc["id"]), "descricao": mapa.descricao(g, loc),
            "nivel": None if loc["tipo"] == "vila" else nivel_regiao(loc, g.corrupcao),
            "covil": ("vencido" if loc["guardiao"]["derrotado"] else "ativo") if covil else None,
        })
        for vid in loc["con"]:
            outro = int(vid)
            if loc["id"] < outro and outro in vistos:
                estradas.append({"a": loc["id"], "b": outro, "atual": atual in (loc["id"], outro),
                                 "percorrida": loc["visitado"] and locais[outro]["visitado"]})
    return {"nos": nos, "estradas": estradas}


def combate(g):
    cb = g.combate_ativo
    if not cb:
        return None

    def ficha(c, lado):
        d = {"nome": c.nome, "hp": max(0, c.hp), "max_hp": c.max_hp, "efeitos": _efeitos(c), "lado": lado,
             "vivo": c.vivo}
        if lado == "inimigo":
            d.update(nivel=c.nivel, chefe=c.chefe, unico=getattr(c, "unico", False), afixo=c.afixo,
                     familia=c.familia, preparando=bool(c.carregando))
        return d

    return {
        "titulo": cb.titulo, "turno": cb.turno,
        "inimigos": [ficha(e, "inimigo") for e in cb.inimigos if e.vivo],
        "aliados": [ficha(a, "aliado") for a in cb.aliados if a.vivo],
    }


def estado(g):
    if not (g and g.j and g.mundo):
        return None
    loc = g.loc
    return {
        "heroi": heroi(g),
        "mundo": {"dia": g.dia, "periodo": PERIODOS[min(g.periodo, 3)], "periodo_n": min(g.periodo, 3),
                  "noite": g.noite, "clima": CLIMAS[g.clima]["nome"], "clima_id": g.clima, "corrupcao": g.corrupcao,
                  "escuro": bool(g.sem_luz)},
        "local": {"id": loc["id"], "nome": loc["nome"], "tipo": loc["tipo"], "bioma": loc["bioma"],
                  "bioma_nome": BIOMAS[loc["bioma"]]["nome"], "descricao": mapa.descricao(g, loc),
                  "nivel": None if loc["tipo"] == "vila" else g.nivel_local()},
        "mapa": mapa_conhecido(g),
        "combate": combate(g),
    }
