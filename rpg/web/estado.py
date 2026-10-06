"""Fotografia do estado do jogo em JSON, para a interface web desenhar painéis, mapa e combate."""

from .. import comitiva, mapa, sobrevivencia
from ..classes import CLASSES, HABILIDADES
from ..combate import NOMES_EFEITOS
from ..dados import BIOMAS, CLIMAS, PERIODOS
from ..itens import CONSUMIVEIS, descrever_bonus, rotulo
from ..mundo import nivel_regiao
from ..jogo import NOMES_TESTE


def _efeitos(c):
    return [{"nome": ef.get("r", NOMES_EFEITOS.get(n, n)), "id": n, "turnos": ef["t"]} for n, ef in c.efeitos.items()]


def _item(it):
    if not it:
        return None
    return {"nome": rotulo(it), "raridade": it.get("raridade", "comum"), "bonus": descrever_bonus(it["bonus"]),
            "nivel": it.get("nivel"), "slot": it.get("slot"), "base": it.get("base"), "bonus_bruto": it["bonus"],
            "classe": it.get("classe"), "lore": it.get("lore")}


def _pct(x):
    v = f"{x * 100:.0f}" if abs(x * 100 - round(x * 100)) < 0.05 else f"{x * 100:.1f}".replace(".", ",")
    return v + "%"


def explicar_atributos(g):
    """Para que serve cada atributo, com os números de agora (o que a tela mostra ao passar o mouse)."""
    j = g.j
    ataque_usa = CLASSES[j.classe]["ataque"][3]
    reducao = 1 - 100 / (100 + j.defesa * 6)
    reducao_mais = 1 - 100 / (100 + (j.defesa + 1) * 6) - reducao
    esquiva = min(0.4, j.agi * 0.012)
    critico = 0.05 + j.agi * 0.01 + 0.04 * j.tal("olho_aguia") + j.especial("critico") / 100
    ataque = ["Força dos golpes de arma: quanto maior, mais dano físico."]
    if ataque_usa == "atk":
        ataque.append(f"É a base do seu ataque básico ({CLASSES[j.classe]['ataque'][0]}) e das habilidades físicas.")
    else:
        ataque.append("Pouco importa para você: suas magias usam Poder.")
    ataque += [f"Testes de Força: {g.mod_teste('forca'):+d} no d20.", "+1 de Ataque ≈ +1 de dano por golpe, antes da defesa do inimigo."]
    defesa = [f"Reduz todo dano recebido em {_pct(reducao)}.",
              f"Cada ponto a mais reduz cerca de {_pct(reducao_mais)} a mais (o ganho diminui aos poucos).",
              f"Testes de Vontade: {g.mod_teste('vontade'):+d} no d20."]
    agilidade = [f"Chance de se esquivar de um golpe: {_pct(esquiva)} (máximo 40%).",
                 f"Chance de acerto crítico: {_pct(critico)}.",
                 "Mais fácil fugir de uma luta.",
                 f"Testes de Destreza: {g.mod_teste('destreza'):+d}, Percepção: {g.mod_teste('percepcao'):+d}.",
                 "+1 de Agilidade = +1,2% de esquiva e +1% de crítico."]
    poder = ["Força da magia e da fé."]
    if j.classe == "mago":
        poder += ["É a base de todas as suas magias e do ataque básico.",
                  f"Queimaduras causam {max(2, int(j.poder * 0.4))} por turno."]
    elif j.spec == "paladino":
        poder += ["Aumenta o Golpe Sagrado, o Julgamento e a cura da Prece."]
    else:
        poder += ["Pouco importa para a sua classe (alguns itens e eventos usam)."]
    poder.append(f"Testes de Arcano: {g.mod_teste('arcano'):+d} no d20.")
    return {"Ataque": ataque, "Defesa": defesa, "Agilidade": agilidade, "Poder": poder}


def explicar_reputacao(g):
    r = g.j.reputacao
    titulo = ("Herói do povo" if r >= 30 else "Respeitado" if r >= 10 else "Temido" if r <= -30
              else "Malvisto" if r <= -10 else "Desconhecido")
    desconto = r / 200
    linhas = ["O que o povo pensa de você. Sobe ajudando, protegendo e cumprindo a palavra; "
              "cai roubando, ameaçando e matando quem não devia.",
              (f"Mercados e serviços {_pct(desconto)} mais baratos." if r > 0 else
               f"Mercados e serviços {_pct(-desconto)} mais caros." if r < 0 else "Preços normais."),
              f"Testes de Carisma: {g.mod_teste('carisma'):+d} no d20."]
    if r <= -10:
        linhas.append("Guardas desconfiam de você e caçadores de recompensa podem aparecer.")
    if r >= 20:
        linhas.append("Algumas pessoas vão lembrar do que você fez, até no fim da jornada.")
    return {"titulo": titulo, "linhas": linhas}


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
        "atributos_info": explicar_atributos(g), "reputacao_info": explicar_reputacao(g),
        "testes": {NOMES_TESTE[a]: {"mod": g.mod_teste(a), "partes": g.partes_teste(a)} for a in NOMES_TESTE},
        "dificuldade_extra": g.dificuldade(0),
        "ouro": j.ouro, "reputacao": j.reputacao, "flechas": j.flechas if j.classe == "arqueiro" else None,
        "provisoes": j.provisoes, "fome": j.fome, "tochas": j.consumiveis.get("tocha", 0),
        "pocoes": j.consumiveis.get("pocao_vida", 0), "bandagens": j.consumiveis.get("bandagem", 0),
        "spec": j.spec, "reputacao_txt": "herói do povo" if j.reputacao >= 20 else "temido" if j.reputacao <= -20 else "",
        "bolsa": [{"id": k, "nome": CONSUMIVEIS[k]["nome"], "qtd": v, "desc": CONSUMIVEIS[k]["desc"]}
                  for k, v in j.consumiveis.items() if v > 0 and k in CONSUMIVEIS],
        "equip": {slot: _item(it) for slot, it in j.equip.items()},
        "mochila": [_item(it) for it in j.mochila], "limite_mochila": 12,
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


def _ficha_inimigo(g, e):
    """O que você sabe deste inimigo: traços sempre; fraquezas e golpes só se você já conhece a espécie."""
    from ..combate import mult_tracos
    from ..dados import TRACOS
    from ..inimigos import NOMES_HABS_INIMIGO
    conhecido = g.conhece(e.familia)
    mult = {}
    if conhecido:
        for tipo in ("fisico", "fogo", "gelo", "sagrado", "sombra", "arcano", "veneno"):
            mult[tipo] = round(mult_tracos(e, tipo, "corpo"), 2)
        mult["distancia"] = round(mult_tracos(e, "fisico", "distancia"), 2)
    return {"conhecido": conhecido, "tracos": [{"id": t, "texto": TRACOS.get(t, t)} for t in e.tracos],
            "mult": mult, "habilidades": [NOMES_HABS_INIMIGO.get(h, h) for h in e.habilidades] if conhecido else [],
            "ponto_fraco": bool(getattr(e, "chave", None) and g.flag(f"fraqueza:{e.chave}")),
            "atk": round(max(e.atk, e.poder)), "defesa": round(e.defesa)}


def combate(g):
    cb = g.combate_ativo
    if not cb:
        return None

    def ficha(c, lado):
        d = {"uid": cb.uid(c), "nome": c.nome, "hp": max(0, c.hp), "max_hp": c.max_hp, "efeitos": _efeitos(c), "lado": lado,
             "vivo": c.vivo, "tracos": list(getattr(c, "tracos", []) or []), "cid": getattr(c, "cid", None),
             "tipo": getattr(c, "tipo", None)}
        if lado == "inimigo":
            d.update(nivel=c.nivel, chefe=c.chefe, unico=getattr(c, "unico", False), afixo=c.afixo,
                     familia=c.familia, preparando=bool(c.carregando), ficha=_ficha_inimigo(g, c))
        return d

    return {
        "titulo": cb.titulo, "turno": cb.turno,
        "inimigos": [ficha(e, "inimigo") for e in cb.inimigos if e.vivo or not e.fugiu],
        "aliados": [ficha(a, "aliado") for a in cb.aliados],
        "heroi": dict(ficha(g.j, "aliado"), nome=g.j.nome, classe=g.j.classe, nivel=g.j.nivel),
    }


def modificadores(g):
    """Efeitos do clima e da hora que valem agora (os mesmos números do combate e dos testes)."""
    m = []
    clima = g.clima
    if clima == "chuva":
        m += [{"icone": "gota_azul", "texto": "Fogo −20%", "detalhe": "Chuva: magias e golpes de fogo causam 20% menos dano, gelo 10% mais. Queimaduras ardem menos."},
              {"icone": "gelo", "texto": "Gelo +10%", "detalhe": "Chuva: o gelo causa 10% mais dano."}]
    elif clima == "neve":
        m += [{"icone": "floco", "texto": "Fogo −15%", "detalhe": "Neve: o fogo causa 15% menos dano."},
              {"icone": "gelo", "texto": "Gelo +20%", "detalhe": "Neve: o gelo causa 20% mais dano."}]
    elif clima == "tempestade":
        m.append({"icone": "raio", "texto": "Distância −15%", "detalhe": "Tempestade: o vento desvia flechas e magias de longe (−15% de dano à distância)."})
    elif clima == "nevoa":
        m.append({"icone": "olho", "texto": "Esquiva +5%", "detalhe": "Névoa: todo mundo erra mais (+5% de esquiva para todos)."})
    if g.noite:
        m.append({"icone": "lua", "texto": "Inimigos +10%", "detalhe": "Noite: os inimigos causam 10% mais dano. É a hora deles."})
    if g.sem_luz:
        m.append({"icone": "tocha_apagada", "texto": "Escuro −4", "detalhe": "Sem luz: −4 nos testes de Percepção e Destreza. Acenda uma tocha."})
    return m


def estado(g):
    if not (g and g.j and g.mundo):
        return None
    loc = g.loc
    return {
        "heroi": heroi(g),
        "mundo": {"dia": g.dia, "periodo": PERIODOS[min(g.periodo, 3)], "periodo_n": min(g.periodo, 3),
                  "noite": g.noite, "clima": CLIMAS[g.clima]["nome"], "clima_id": g.clima, "corrupcao": g.corrupcao,
                  "escuro": bool(g.sem_luz), "modificadores": modificadores(g)},
        "local": {"id": loc["id"], "nome": loc["nome"], "tipo": loc["tipo"], "bioma": loc["bioma"],
                  "bioma_nome": BIOMAS[loc["bioma"]]["nome"], "descricao": mapa.descricao(g, loc),
                  "nivel": None if loc["tipo"] == "vila" else g.nivel_local()},
        "mapa": mapa_conhecido(g),
        "combate": combate(g),
        "contratos": [g.cartao_contrato(c) for c in g.contratos],
    }
