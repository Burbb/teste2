"""Fotografia do estado do jogo em JSON, para a interface web desenhar painéis, mapa e combate."""

from .. import balanceamento as bal
from .. import comitiva, grimorio, mapa, sobrevivencia
from .. import texto as tx
from ..classes import CLASSES
from ..habilidades import HABILIDADES, descricao_habilidade
from .. import estados
from ..estados import NOMES as NOMES_EFEITOS, para_tela
from ..dados import BIOMAS, CLIMAS, PERIODOS, retrato
from .. import itens
from ..itens import CONSUMIVEIS, EM_ALIADO, ficha
from ..mundo import nivel_regiao
from ..jogo import NOMES_TESTE
from ..combate import Combate
from ..talentos import custo_habilidade


def _alvo_animal(g, k):
    """O animal do patrulheiro como alvo da poção e da bandagem da bolsa."""
    f = g.j.companheiro
    if not f:
        return []
    return [{"id": "fera", "nome": f["nome"], "hp": f["hp"], "max_hp": f["max_hp"], "ferido": f["hp"] <= 0,
             "caido": "ferido, não luta", "motivo": g.motivo_inutil(k, f)}]


def _efeitos(c, cb=None):
    lista = []
    for n, ef in c.efeitos.items():
        d = {"nome": ef.get("r", NOMES_EFEITOS.get(n, n)), "id": n, "turnos": ef["t"]}
        if estados.ESTADOS.get(n, {}).get("tique"):
            d["por_turno"] = estados.dano_do_tique(cb, n, ef)
        if ef.get("s", 1) > 1:
            d["camadas"] = ef["s"]
        d["texto"] = estados.agora(n, ef.get("v", 0))
        lista.append(d)
    return lista


_item = ficha


def _pct(x):
    v = f"{x * 100:.0f}" if abs(x * 100 - round(x * 100)) < 0.05 else f"{x * 100:.1f}".replace(".", ",")
    return v + "%"


def explicar_atributos(g):
    """Para que serve cada atributo, com os números de agora (o que a tela mostra ao passar o mouse)."""
    j = g.j
    ataque_usa = CLASSES[j.classe]["ataque"][3]
    reducao = 1 - bal.fator_defesa(j.defesa, j.nivel)
    reducao_mais = 1 - bal.fator_defesa(j.defesa + 1, j.nivel) - reducao
    esquiva = min(bal.ESQUIVA_MAX_AGI, j.agi * bal.ESQUIVA_POR_AGI)
    critico = grimorio.chance_critico(j)
    ataque = ["Força dos golpes de arma: quanto maior, mais dano físico."]
    if ataque_usa == "atk":
        ataque.append(f"É a base do seu ataque básico ({CLASSES[j.classe]['ataque'][0]}) e das habilidades físicas.")
    else:
        ataque.append("Pouco importa para você: suas magias usam Poder.")
    ataque += [f"Testes de Força: {g.mod_teste('forca'):+d} no d20.", "+1 de Ataque ≈ +1 de dano por golpe, antes da defesa do inimigo."]
    defesa = [f"Reduz o dano de um inimigo do seu nível em {_pct(reducao)}. Inimigos de nível mais alto "
              "atravessam mais a armadura; os de nível mais baixo, menos.",
              f"Cada ponto a mais reduz cerca de {_pct(reducao_mais)} a mais (o ganho diminui aos poucos).",
              f"Testes de Vontade: {g.mod_teste('vontade'):+d} no d20."]
    agilidade = [f"Chance de se esquivar de um golpe: {_pct(esquiva)} (máximo {_pct(bal.ESQUIVA_MAX_AGI)} só pela "
                 f"Agilidade; com habilidades, até {_pct(bal.MAX_ESQUIVA)}).",
                 f"Chance de acerto crítico: {_pct(critico)} (máximo {_pct(bal.MAX_CRITICO)}).",
                 "Mais fácil fugir de uma luta.",
                 f"Testes de Destreza: {g.mod_teste('destreza'):+d}, Percepção: {g.mod_teste('percepcao'):+d}.",
                 f"+1 de Agilidade = +{_pct(bal.ESQUIVA_POR_AGI)} de esquiva e +{_pct(bal.CRITICO_POR_AGI)} de crítico."]
    poder = ["Força da magia e da fé."]
    usam_poder = grimorio.habilidades_que_usam(j, "poder")
    if ataque_usa == "poder":
        queima = max(1, int(Combate.valor_queimadura(None, j)))
        poder += ["É a base de todas as suas magias e do ataque básico.",
                  f"Cada camada de queimadura arde {queima} por turno (acumula até {bal.MAX_CHAMAS} camadas)."]
    elif usam_poder:
        poder += [f"Aumenta {tx.lista_natural(usam_poder)}."]
    else:
        poder += ["Pouco importa para a sua classe (alguns itens e eventos usam)."]
    poder.append(f"Testes de Arcano: {g.mod_teste('arcano'):+d} no d20.")
    info = {"Ataque": ataque, "Defesa": defesa, "Agilidade": agilidade, "Poder": poder}
    for nome, p in penalidades_atributos(j).items():  # abaixo do normal: a primeira linha diz por quê
        info[nome].insert(0, f"Abaixo do normal: {', '.join(p['fontes'])} (sem isso, {p['normal']}).")
    return info


ATRIBUTOS_FICHA = (("Ataque", "atk"), ("Defesa", "defesa"), ("Agilidade", "agi"), ("Poder", "poder"))


def penalidades_atributos(j):
    """Atributos abaixo do normal por ferimento ou fome: o percentual somado, o valor normal e de onde vem cada
    parte ("Perna torcida −30%", "Fome −10%")."""
    fontes = sobrevivencia.fontes_penalidade(j)
    totais, _ = j.totais()
    saida = {}
    for nome, stat in ATRIBUTOS_FICHA:
        normal = max(1, int(round(totais[stat])))
        if stat not in fontes or getattr(j, stat) >= normal:
            continue
        fator = 1.0
        for _, v in fontes[stat]:
            fator *= v
        saida[nome] = {"pct": round((1 - fator) * 100), "normal": normal,
                       "fontes": [f"{n} −{round((1 - v) * 100)}%" for n, v in fontes[stat]]}
    return saida


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
                           "aberto": bool(d.get("aberto") and not f.get("tratado")),
                           "explica": sobrevivencia.explicar(f, j.nome_recurso, j)})
    return {
        "nome": j.nome, "classe": j.classe, "classe_nome": CLASSES[j.classe]["nome"], "titulo": j.nome_classe,
        "nivel": j.nivel, "xp": j.xp, "xp_proximo": j.xp_proximo(),
        "hp": j.hp, "max_hp": j.max_hp, "rec": j.rec, "max_rec": j.max_rec, "recurso": j.nome_recurso,
        "vida_por_um_fio": bal.VIDA_POR_UM_FIO,
        "atributos": {"Ataque": j.atk, "Defesa": j.defesa, "Agilidade": j.agi, "Poder": j.poder},
        "atributos_info": explicar_atributos(g), "atributos_penal": penalidades_atributos(j),
        "reputacao_info": explicar_reputacao(g),
        "testes": {NOMES_TESTE[a]: {"mod": g.mod_teste(a), "partes": g.partes_teste(a)} for a in NOMES_TESTE},
        "dificuldade_extra": g.dificuldade(0),
        "ouro": j.ouro, "reputacao": j.reputacao, "flechas": j.flechas if j.classe == "arqueiro" else None,
        "max_flechas": g.max_flechas() if j.classe == "arqueiro" else None,
        "provisoes": j.provisoes, "fome": j.fome,
        **{c["hud"]: j.consumiveis.get(k, 0) for k, c in CONSUMIVEIS.items() if c["hud"]},  # tochas, poções...
        "spec": j.spec, "reputacao_txt": "herói do povo" if j.reputacao >= 20 else "temido" if j.reputacao <= -20 else "",
        "bolsa": [{"id": k, "nome": CONSUMIVEIS[k]["nome"], "qtd": v, "desc": CONSUMIVEIS[k]["desc"],
                   "motivo": None if k == "tocha" else g.combate_ativo.motivo_item(k) if g.combate_ativo else g.motivo_inutil(k),
                   "alvos": [{"id": m["id"], "nome": comitiva.nome(m["id"]), "hp": m["hp"], "max_hp": m["max_hp"],
                              "ferido": m["ferido"], "caido": comitiva.flexao(m["id"], "caíd{a}, não luta"),
                              "motivo": g.motivo_inutil(k, m)}
                             for m in comitiva.membros(g)] + _alvo_animal(g, k) if k in EM_ALIADO and not g.combate_ativo else []}
                  for k, v in j.consumiveis.items() if v > 0 and k in CONSUMIVEIS],
        "equip": {slot: _item(it, j.nome_recurso) for slot, it in j.equip.items()},
        "mochila": [_item(it, j.nome_recurso) for it in j.mochila], "limite_mochila": 12,
        "habilidades": [{"nome": HABILIDADES[h]["nome"], "custo": custo_habilidade(j, h), "desc": descricao_habilidade(h, j)}
                        for h in j.habilidades],
        "grimorio": grimorio.dados(j),
        "ferimentos": ferimentos, "males": sobrevivencia.descrever(j),
        "pontos_talento": j.pontos_talento, "sigilos": len(j.sigilos),
        "companheiro": ({"nome": j.companheiro["nome"], "hp": j.companheiro["hp"], "max_hp": j.companheiro["max_hp"],
                         "tipo": j.companheiro["tipo"], "animado": bool(j.companheiro.get("animado"))}
                        if j.companheiro else None),
        "efeitos": _efeitos(j, g.combate_ativo),
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
            # numa vila, o dos arredores (as estradas por onde se chega e se sai); a saída fechada não tem
            "nivel": None if loc.get("fechado") else nivel_regiao(loc),
            "covil": ("vencido" if loc["guardiao"]["derrotado"] else "ativo") if covil else None,
        })
        for vid in loc["con"]:
            outro = int(vid)
            if loc["id"] < outro and outro in vistos:
                estradas.append({"a": loc["id"], "b": outro, "atual": atual in (loc["id"], outro),
                                 "percorrida": loc["visitado"] and locais[outro]["visitado"]})
    return {"nos": nos, "estradas": estradas}


def _ficha_inimigo(g, e):
    """O que você sabe deste inimigo, conforme o bestiário da espécie: traços sempre; as fraquezas depois de
    conhecer a espécie; as resistências só com mais caçadas."""
    from ..combate import eficacias
    from ..dados import TRACOS, TRACOS_FICHA
    conhecido = g.conhece(e.familia)
    resistencias = g.conhece_resistencias(e.familia)
    fraco, resiste = eficacias(e)
    return {"conhecido": conhecido, "resistencias": resistencias, "progresso": g.progresso_bestiario(e.familia),
            "mestre": g.mestre_caca(e.familia), "abates": g.bestiario.get(e.familia, {}).get("abates", 0),
            "mestre_em": g.MESTRE_ABATES,
            "tracos": [{"id": t, "texto": TRACOS.get(t, t), "icone": TRACOS_FICHA[t]["icone"]} for t in e.tracos],
            "fraco": fraco if conhecido else None, "resiste": resiste if resistencias else None,
            "ponto_fraco": bool(getattr(e, "chave", None) and g.flag(f"fraqueza:{e.chave}")),
            "atk": round(max(e.atk, e.poder)), "defesa": round(e.defesa)}


def combate(g):
    cb = g.combate_ativo
    if not cb:
        return None

    def ficha(c, lado):
        d = {"uid": cb.uid(c), "nome": c.nome, "hp": max(0, c.hp), "max_hp": c.max_hp, "efeitos": _efeitos(c, cb), "lado": lado,
             "vivo": c.vivo, "tracos": list(getattr(c, "tracos", []) or []), "cid": getattr(c, "cid", None),
             "retrato": retrato(getattr(c, "tracos", []) or []),
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


# Como cada número do clima aparece no selo: nome curto, quem sofre (para a dica) e o ícone quando ajuda.
DANO_CLIMA = {"fogo": ("Fogo", "magias e golpes de fogo causam", "chama"),
              "gelo": ("Gelo", "o gelo causa", "gelo"),
              "distancia": ("Distância", "flechas e magias de longe causam", "flecha")}


def _variacao(f):
    return f"{'+' if f > 1 else '−'}{round(abs(f - 1) * 100)}%"


def modificadores(g):
    """Efeitos do clima e da hora que valem agora: os números vêm do catálogo CLIMAS e do balanceamento, os mesmos
    que o combate e os testes usam."""
    m = []
    clima = CLIMAS[g.clima]
    for k, f in clima.get("dano", {}).items():
        nome, quem, icone = DANO_CLIMA[k]
        detalhe = f"{clima['nome']}: {quem} {round(abs(f - 1) * 100)}% {'mais' if f > 1 else 'menos'} dano."
        if k == "fogo" and clima.get("queimadura"):
            detalhe += f" Queimaduras ardem {round((1 - clima['queimadura']) * 100)}% menos."
        m.append({"icone": icone if f > 1 else clima["icone"], "texto": f"{nome} {_variacao(f)}", "detalhe": detalhe})
    if clima.get("esquiva"):
        pct = round(clima["esquiva"] * 100)
        m.append({"icone": clima["icone"], "texto": f"Esquiva +{pct}%",
                  "detalhe": f"{clima['nome']}: todo mundo erra mais (+{pct}% de esquiva para todos)."})
    if g.noite:
        m.append({"icone": "lua", "texto": f"Inimigos +{bal.NOITE_NIVEL} nível",
                  "detalhe": f"Noite: os inimigos vêm {'um nível' if bal.NOITE_NIVEL == 1 else f'{bal.NOITE_NIVEL} níveis'} acima, mais vezes em bando, e "
                             f"causam {round((bal.NOITE_INIMIGOS - 1) * 100)}% mais dano. É a hora deles."})
    if g.sem_luz:
        m.append({"icone": "tocha_apagada", "texto": f"Escuro −{bal.ESCURO_TESTES}",
                  "detalhe": f"Sem luz: −{bal.ESCURO_TESTES} nos testes de Percepção e Destreza. Acenda uma tocha."})
    return m


def predios_fechados(g):
    """Na vila, os prédios sem serviço agora (o templo com a vida cheia, a curandeira sem ferimento para tratar) e o
    que eles dizem a quem chega: a tela gráfica deixa o prédio clicável mesmo assim."""
    if g.loc["tipo"] != "vila":
        return {}
    fechados = {}
    if not g.opcoes_templo():
        fechados["templo"] = "O templo está em silêncio. Ninguém aqui precisa de cuidados agora."
    if not g.j.ferimentos:
        fechados["curandeiro"] = "A curandeira ergue os olhos e volta às ervas. \"Nada para tratar em você.\""
    return fechados


def glossario():
    """A cor de cada nome de habilidade, talento e passiva que a tela realça nos textos de regra ("Bola de Fogo" em
    laranja, "Drenar Vida" em vermelho): o campo `realce` dos catálogos. Quem não declara fica neutro."""
    from ..talentos import PASSIVAS, POR_ID
    fichas = list(HABILIDADES.values()) + list(POR_ID.values()) + list(PASSIVAS.values())
    return {f["nome"]: f["realce"] for f in fichas if f.get("realce")}


def estado(g):
    if not (g and g.j and g.mundo):
        return None
    loc = g.loc
    return {
        "heroi": heroi(g),
        "mundo": {"dia": g.dia, "periodo": PERIODOS[min(g.periodo, 3)], "periodo_n": min(g.periodo, 3),
                  "noite": g.noite, "clima": CLIMAS[g.clima]["nome"], "clima_id": g.clima,
                  "escuro": bool(g.sem_luz), "modificadores": modificadores(g)},
        "local": {"id": loc["id"], "nome": loc["nome"], "tipo": loc["tipo"], "bioma": loc["bioma"],
                  "bioma_nome": BIOMAS[loc["bioma"]]["nome"], "descricao": mapa.descricao(g, loc),
                  "nivel": g.nivel_local(), "predios_fechados": predios_fechados(g),
                  "estrada": g.na_estrada},  # viajando: a paisagem é a da região, sem a vila
        "mapa": mapa_conhecido(g),
        "combate": combate(g),
        "estados": para_tela(),  # ícone, cor e dica de cada estado (catálogo em estados.py)
        "glossario": glossario(),
        "itens": itens.para_tela(),  # ícone e contador de cada consumível e recurso
        "contratos": [g.cartao_contrato(c) for c in g.contratos],
    }
