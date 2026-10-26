"""Fotografia do estado do jogo em JSON, para a interface web desenhar painéis, mapa e combate."""

from .. import atributos as atr
from .. import balanceamento as bal
from .. import abertura, capitulo, comitiva, consequencias, grimorio, mapa, missoes, sobrevivencia
from .. import texto as tx
from ..classes import CLASSES
from ..habilidades import HABILIDADES, VARIANTES, descricao_habilidade, efetiva
from .. import estados
from ..estados import NOMES as NOMES_EFEITOS, para_tela
from ..dados import BIOMAS, CLIMAS, PERIODOS, retrato
from .. import itens
from ..itens import CONSUMIVEIS, EM_ALIADO, ficha
from ..mundo import nivel_regiao
from ..jogo import NOMES_TESTE
from ..sistemas.testes import TESTE_DERIVADO
from ..combate import Combate
from ..talentos import custo_habilidade


def _alvo_animal(g, k):
    """O animal do patrulheiro como alvo da poção da bolsa."""
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
            d["por_turno"] = estados.dano_do_tique(cb, n, ef, c)
        if ef.get("s", 1) > 1:
            d["camadas"] = ef["s"]
        d["texto"] = estados.agora(n, ef.get("v", 0))
        lista.append(d)
    return lista


_item = ficha


def _pct(x):
    v = f"{x * 100:.0f}" if abs(x * 100 - round(x * 100)) < 0.05 else f"{x * 100:.1f}".replace(".", ",")
    return v + "%"


def _parte_nos_testes(g, attr, nome):
    """Quanto o atributo de nome dado soma no teste (a parte dele, sem o nível nem a classe): pelas partes do motor."""
    return next((v for r, v in g.partes_fixas_teste(attr) if r.startswith(nome + " ")), 0)


def explicar_testes(g):
    """Os seis testes do d20 para a ficha: o bônus do personagem e de onde vem (nível, atributo, classe), o que a
    situação de agora muda (sem luz) e o total de agora, para que serve, a chance numa dificuldade típica e, se o
    atributo de origem está abaixo do normal (ferimento, fome), o porquê. Tudo do motor (sistemas/testes.py)."""
    penal = penalidades_atributos(g.j)
    saida = {}
    for a, nome in NOMES_TESTE.items():
        fixas, situacao = g.partes_fixas_teste(a), g.situacao_teste(a)
        abaixo = [f"{n} abaixo do normal: {', '.join(p['fontes'])}" for n, p in penal.items()
                  if TESTE_DERIVADO.get(a) == n]
        saida[nome] = {"mod": g.mod_teste(a), "partes": fixas + situacao, "fixo": sum(v for _, v in fixas),
                       "fixas": fixas, "situacao": situacao, "uso": g.USO_TESTE[a],
                       "chance_media": g.chance_teste_media(a), "abaixo": abaixo}
    return saida


# o atributo que soma em cada valor derivado (atributos.POR_PONTO), pelo nome que a ficha mostra
ATRIBUTO_DO_STAT = {"atk": "Força", "poder": "Intelecto", "agi": "Agilidade", "max_hp": "Constituição",
                    "max_rec": "Vontade"}


def composicao(j, stat):
    """De onde vem um valor derivado, pela mesma conta do motor (Jogador.totais e recalcular): a classe e o nível, o
    atributo, o equipamento e os talentos, o total, e as penalidades de ferimento e fome até o valor que vale na luta.
    Devolve a frase ("Classe e nível 8 + Força 6 + equipamento 3 = 17.") e, com penalidade, a segunda ("Ferimentos:
    Perna torcida −30%, ... → 3.")."""
    from ..talentos import bonus_stats
    partes = [("Classe e nível", j.base[stat]),
              (f"atributo {ATRIBUTO_DO_STAT.get(stat, '')}".rstrip(), atr.contribuicao(j).get(stat, 0)),
              ("equipamento", sum(it["bonus"].get(stat, 0) for it in j.equip.values() if it)),
              ("talentos", bonus_stats(j).get(stat, 0))]
    totais, _ = j.totais()
    vale = [(n, v) for n, v in partes if abs(v) >= 0.05]
    texto = " + ".join(f"{n} {_num(round(v, 1))}" for n, v in vale).replace("+ -", "− ")
    # uma parcela só: o nome e o valor, sem a conta ("atributo Agilidade 3")
    frase = f"{texto} = {max(1, int(round(totais[stat])))}." if len(vale) > 1 else f"{texto}."
    fontes = sobrevivencia.fontes_penalidade(j).get(stat)
    if not fontes:
        return frase, None
    return frase, f"{', '.join(f'{n} −{round((1 - v) * 100)}%' for n, v in fontes)} → {getattr(j, stat)} na luta."


def _ate_a_luta(j, stat, nome):
    """O que leva da soma do atributo ao valor que vale na luta, quando não são o mesmo número: os outros
    modificadores e as penalidades (". Com equipamento +1 e ferimentos e fome −37%, a Agilidade é 3.")."""
    from ..talentos import bonus_stats
    outros = [("classe e nível", j.base[stat]),
              ("equipamento", sum(it["bonus"].get(stat, 0) for it in j.equip.values() if it)),
              ("talentos", bonus_stats(j).get(stat, 0))]
    mods = [f"{n} {'+' if v > 0 else '−'}{_num(round(abs(v), 1))}" for n, v in outros if abs(v) >= 0.05]
    fontes = sobrevivencia.fontes_penalidade(j).get(stat)
    if fontes:
        fator = 1.0
        for _, v in fontes:
            fator *= v
        mods.append(f"ferimentos e fome −{round((1 - fator) * 100)}%")
    if not mods:
        return "."
    return f". Com {tx.lista_natural(mods)}, {nome} é {getattr(j, stat)}."


def explicar_atributos(g):
    """Para que serve cada valor derivado, com o valor que vale e de onde ele vem (o que a tela mostra ao passar o
    mouse e no foco). Primeiro o que ele faz, com os números; depois a composição; com ferimento ou fome, a linha da
    penalidade vem primeiro (a tela a pinta de vermelho: inventario.js)."""
    j = g.j
    ataque_usa = CLASSES[j.classe]["ataque"][3]
    reducao = 1 - bal.fator_defesa(j.defesa, j.nivel)
    reducao_mais = 1 - bal.fator_defesa(j.defesa + 1, j.nivel) - reducao
    ataque = ["Dano dos golpes físicos (armas e flechas): +1 de Ataque ≈ +1 de dano por golpe, antes da defesa do "
              "inimigo."]
    ataque.append(f"Base do {CLASSES[j.classe]['ataque'][0]} e das habilidades físicas." if ataque_usa == "atk"
                  else "Suas magias usam Poder.")
    defesa = [f"Reduz em {_pct(reducao)} o dano de um inimigo do seu nível (de nível mais alto, menos; de mais baixo, "
              f"mais). +1 de Defesa reduz cerca de {_pct(reducao_mais)} a mais."]
    esquiva = min(bal.ESQUIVA_MAX_AGI, j.agi * bal.ESQUIVA_POR_AGI)
    agilidade = [f"Esquiva: {_pct(esquiva)} de chance por golpe ({_pct(bal.ESQUIVA_POR_AGI)} por ponto, até "
                 f"{_pct(bal.ESQUIVA_MAX_AGI)}; com habilidades, até {_pct(bal.MAX_ESQUIVA)}).",
                 "Ordem dos turnos e fuga: com mais Agilidade que os inimigos, você age antes e foge com mais "
                 "facilidade."]
    poder = ["Dano e cura das magias e da fé."]
    usam_poder = grimorio.habilidades_que_usam(j, "poder")
    if ataque_usa == "poder":
        queima = max(1, int(Combate.valor_queimadura(None, j)))
        poder += [f"Base das suas magias e do ataque básico; Queimadura de {queima} por turno do alvo, por camada."]
    elif usam_poder:
        poder += [f"Usado por: {tx.lista_natural(usam_poder)}."]
    else:
        poder += ["Nenhuma habilidade sua usa Poder agora (alguns itens e eventos usam)."]
    info = {"Ataque": ataque, "Defesa": defesa, "Agilidade": agilidade, "Poder": poder}
    for nome, stat in ATRIBUTOS_FICHA:
        frase, penal = composicao(j, stat)
        if penal:
            info[nome].insert(0, f"Ferimentos e fome: {penal}")
        info[nome].append(f"De onde vem: {frase}")
    return info


TESTE_DE = {"forca": "forca", "agilidade": "destreza", "intelecto": "arcano", "percepcao": "percepcao",
            "vontade": "vontade", "presenca": "carisma"}


def explicar_atributos_base(g):
    """Os seis atributos e a Presença na ficha (etapa 4, atributos.py): o valor, o que cada ponto dá e quanto soma agora,
    e o teste do d20 que usa cada um. Os números vêm do motor; a tela só desenha."""
    j = g.j
    valores = dict(atr.de(j), presenca=atr.presenca(j))
    soma = atr.contribuicao(j)
    rec = j.nome_recurso
    fem = rec == "Mana"
    # o que cada atributo soma hoje, numa frase (sem "Agora:"; o ganho por ponto entre parênteses, uma vez)
    agora = {
        "forca": f"Soma {_num(soma.get('atk', 0))} ao Ataque (+1 por ponto){_ate_a_luta(j, 'atk', 'o Ataque')}",
        "agilidade": (f"Soma {_num(soma.get('agi', 0))} à Agilidade (+1 por ponto)"
                      f"{_ate_a_luta(j, 'agi', 'a Agilidade de luta')}"),
        "constituicao": (f"Soma {_num(soma.get('max_hp', 0))} à vida máxima (+4 por ponto)"
                         f"{_ate_a_luta(j, 'max_hp', 'a vida máxima')}"),
        "intelecto": f"Soma {_num(soma.get('poder', 0))} ao Poder (+1 por ponto){_ate_a_luta(j, 'poder', 'o Poder')}",
        "percepcao": f"Soma {_pct(atr.critico(j))} ao crítico (+1% por ponto); o crítico total é "
                     f"{_pct(grimorio.chance_critico(j))}.",
        "vontade": (f"Soma {_num(soma.get('max_rec', 0))} {'à' if fem else 'ao'} {rec} {'máxima' if fem else 'máximo'} "
                    f"e {_pct(atr.tenacidade(j))} de Tenacidade (+3 e +4% por ponto; Tenacidade até "
                    f"{_pct(atr.TENACIDADE_TETO)})"
                    + _ate_a_luta(j, "max_rec", f"{'a' if fem else 'o'} {rec} {'máxima' if fem else 'máximo'}")),
    }
    lista = []
    for a in atr.ATRIBUTOS + ("presenca",):
        # primeiro o que ele dá agora; depois o que cada ponto rende; o teste do d20 por último
        linhas = ([agora[a]] if a != "presenca" else
                  [f"Serve para {atr.FUNCAO[a]}. Não vale na luta.", "Não recebe pontos: sobe 1 a cada 3 níveis."])
        if a in TESTE_DE:
            linhas.append(f"Testes de {NOMES_TESTE[TESTE_DE[a]]}: "
                          f"{_parte_nos_testes(g, TESTE_DE[a], atr.NOMES[a]):+d}.")
        # o "+" da ficha: só nos seis, com pontos da subida de nível; o porquê quando não dá
        mais = None if a == "presenca" or not j.pontos_atributo else {"motivo": g.motivo_atributo(a)}
        lista.append({"id": a, "nome": atr.NOMES[a], "sigla": atr.SIGLAS[a], "valor": valores.get(a, 0),
                      "linhas": linhas, "mais": mais})
    return lista


def explicar_conceitos(g):
    """Os valores que nascem dos atributos e têm explicação própria (a dica de cada um, na ficha e no quadro de
    atributos): o crítico (Percepção) e a Tenacidade (Vontade)."""
    j = g.j
    return [
        {"id": "critico", "nome": "Crítico", "valor": _pct(grimorio.chance_critico(j)),
         "linhas": [f"Chance de um golpe seu sair crítico (×{_num(grimorio.mult_critico(j))} de dano).",
                    f"Vem da Percepção ({_pct(atr.critico(j))}), da base de todo herói e de talentos e itens."]},
        {"id": "tenacidade", "nome": "Tenacidade", "valor": _pct(atr.tenacidade(j)),
         "linhas": ["Chance de resistir a atordoar, congelar e prender (você perde a vez se não resistir).",
                    f"Vem da Vontade: {_pct(atr.TENACIDADE_POR_PONTO)} por ponto, até {_pct(atr.TENACIDADE_TETO)}.",
                    "Não reduz dano: a resistência a fogo, gelo e outros tipos é outra coisa."]},
    ]


def _num(v):
    return str(int(v)) if float(v).is_integer() else f"{v:.1f}".replace(".", ",")


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
              f"Nos testes de Carisma, a Reputação dá {_parte_nos_testes(g, 'carisma', 'Reputação'):+d}."]
    if r <= -10:
        linhas.append("Guardas desconfiam de você e caçadores de recompensa podem aparecer.")
    if r >= 20:
        linhas.append("Algumas pessoas vão lembrar do que você fez, até no fim da jornada.")
    return {"titulo": titulo, "linhas": linhas}


def _soma(lista, total):
    """A conta de um número do companheiro: "base 11,6 (nível 3) + equipamento 2 = 13,6"; só a base, sem conta."""
    (rotulo, base), resto = lista[0], lista[1:]
    if not resto:
        return f"a base de {rotulo}"
    return (f"base {_num(round(base, 1))} + " + " + ".join(f"{n} {_num(round(v, 1))}" for n, v in resto)
            ).replace("+ -", "− ") + f" = {_num(round(total, 1))}"


def ficha_companheiro(g, m):
    """A ficha de um companheiro na janela do grupo (1.213.0), no formato da do herói: os números que valem na luta
    (com a lealdade), de onde vêm, os atributos com o "+" dos pontos livres, o crítico, a Tenacidade e as peças."""
    f = comitiva.ficha
    j, cid = g.j, m["id"]
    d = comitiva.COMPANHEIROS[cid]
    f.preparar(m, j.nivel)
    at = comitiva.atributos(g, m)
    leal = comitiva.lealdade(m)
    rec = comitiva.luta.RECURSO[cid]
    fem = rec in ("Fé", "Mana")
    u = f.combatente(g, m)
    valores = {"Ataque": at["atk"] * leal, "Defesa": at["defesa"], "Agilidade": at["agi"], "Poder": at["poder"] * leal}
    reducao = 1 - bal.fator_defesa(at["defesa"], j.nivel)
    esquiva = min(bal.ESQUIVA_MAX_AGI, at["agi"] * bal.ESQUIVA_POR_AGI)
    nome_atk, _, _, _, stat_atk = comitiva.ATAQUE[cid]
    info = {
        "Ataque": ["Dano dos golpes físicos." + (f" Base do {nome_atk}." if stat_atk == "atk" else "")],
        "Defesa": [f"Reduz em {_pct(reducao)} o dano de um inimigo do seu nível."],
        "Agilidade": [f"Esquiva: {_pct(esquiva)} de chance por golpe ({_pct(bal.ESQUIVA_POR_AGI)} por ponto, até "
                      f"{_pct(bal.ESQUIVA_MAX_AGI)}).", "Ordem dos turnos: mais Agilidade, mais cedo na rodada."],
        "Poder": ["Dano e cura das magias e da fé." + (f" Base do {nome_atk}." if stat_atk == "poder" else "")],
    }
    for nome, stat in ATRIBUTOS_FICHA:
        conta = _soma(f.partes(g, m, stat), at[stat])
        if stat in ("atk", "poder") and leal != 1:
            conta += f"; na luta, × {_num(round(leal, 2))} da lealdade (aprovação {m['aprovacao']})"
        info[nome].append(f"De onde vem: {conta}.")
    valores_base = f.atributos_de(m)
    iniciais = f.INICIAIS[cid]
    acima = {a: valores_base[a] - iniciais[a] for a in atr.ATRIBUTOS}
    # os iniciais já estão nos números do catálogo: o que conta é o ponto além deles (sem "Soma 0")
    def soma(a, ganho, alvo, total=""):
        ini = f"do {iniciais[a]} inicial" if iniciais[a] == 1 else f"dos {iniciais[a]} iniciais"
        regra = f"{ganho} por ponto além {ini}"
        if not acima[a]:
            return f"Cada ponto além {ini} soma {ganho.lstrip('+')} {alvo}{total}."
        valor = _pct(acima[a] * atr.CRITICO_POR_PONTO) if ganho == "+1%" else acima[a] * int(ganho.strip("+"))
        return f"Soma {valor} {alvo} ({regra}){total}."
    rec_nome = f"{'à' if fem else 'ao'} {rec} {'máxima' if fem else 'máximo'}"
    agora = {
        "forca": soma("forca", "+1", "ao Ataque"),
        "agilidade": soma("agilidade", "+1", "à Agilidade", f"; a Agilidade de luta é {at['agi']}"),
        "constituicao": soma("constituicao", "+4", "à vida máxima", f"; a vida máxima é {at['max_hp']}"),
        "intelecto": soma("intelecto", "+1", "ao Poder"),
        "percepcao": soma("percepcao", "+1%", "ao crítico", f"; o crítico total é {_pct(grimorio.chance_critico(u))}"),
        "vontade": (f"Dá {_pct(atr.tenacidade(u))} de Tenacidade ({_pct(atr.TENACIDADE_POR_PONTO)} por ponto, até "
                    f"{_pct(atr.TENACIDADE_TETO)}). " + soma("vontade", "+3", rec_nome, f"; o máximo é {at['max_rec']}")),
    }
    base = [{"id": a, "nome": atr.NOMES[a], "sigla": atr.SIGLAS[a], "valor": valores_base[a], "linhas": [agora[a]],
             "mais": {"motivo": f.motivo_atributo(g, cid, a)} if m["pontos_atributo"] else None}
            for a in atr.ATRIBUTOS]
    conceitos = [
        {"id": "critico", "nome": "Crítico", "valor": _pct(grimorio.chance_critico(u)),
         "linhas": [f"Chance de um golpe de {d['curto']} sair crítico (×{_num(grimorio.mult_critico(u))} de dano).",
                    "Vem da Agilidade e da Percepção acima da inicial, e das peças."]},
        {"id": "tenacidade", "nome": "Tenacidade", "valor": _pct(atr.tenacidade(u)),
         "linhas": ["Chance de resistir a atordoar, congelar e prender.",
                    f"Vem da Vontade: {_pct(atr.TENACIDADE_POR_PONTO)} por ponto, até {_pct(atr.TENACIDADE_TETO)}."]},
    ]
    sugestao = " › ".join(atr.SIGLAS[a] for a in f.SUGESTAO[cid])
    return {"id": cid, "nome": d["curto"], "titulo": d["titulo"], "classe": f.CLASSE_PECAS[cid],
            "pecas": f"Usa peças de {f.NOME_CLASSE[f.CLASSE_PECAS[cid]]} e as sem classe.",
            "nivel": j.nivel, "hp": m["hp"], "max_hp": m["max_hp"], "max_rec": at["max_rec"], "recurso": rec,
            "ferido": m["ferido"], "indisponivel": f.motivo_indisponivel(g, cid) if not g.combate_ativo else None,
            "atributos": {k: int(round(v)) for k, v in valores.items()}, "atributos_info": info,
            "atributos_penal": {}, "atributos_base": base, "pontos_atributo": m["pontos_atributo"],
            "sugestao": sugestao, "conceitos": conceitos,
            "equip": {slot: _item(it, rec) for slot, it in f.corpo(g, cid).items()}}


def heroi(g):
    j = g.j
    ferimentos = []
    for f in j.ferimentos:
        d = sobrevivencia.FERIMENTOS[f["id"]]
        ferimentos.append({"id": f["id"], "nome": d["nome"], "dias": f.get("dias") if d["dias"] else None,
                           "aberto": bool(d.get("aberto") and not f.get("tratado")),
                           "explica": sobrevivencia.explicar(f, j.nome_recurso, j)})
    return {
        "nome": j.nome, "classe": j.classe, "classe_nome": CLASSES[j.classe]["nome"], "titulo": j.nome_classe,
        "nivel": j.nivel, "xp": j.xp, "xp_proximo": j.xp_proximo(),
        "hp": j.hp, "max_hp": j.max_hp, "rec": j.rec, "max_rec": j.max_rec, "recurso": j.nome_recurso,
        # a vida máxima que ferimentos e fome bloqueiam agora (None sem bloqueio): a barra mede a vida saudável
        "vida_bloqueio": sobrevivencia.vida_bloqueio(j),
        "vida_por_um_fio": bal.VIDA_POR_UM_FIO,
        "atributos": {"Ataque": j.atk, "Defesa": j.defesa, "Agilidade": j.agi, "Poder": j.poder},
        "atributos_info": explicar_atributos(g), "atributos_penal": penalidades_atributos(j),
        "atributos_base": explicar_atributos_base(g), "pontos_atributo": j.pontos_atributo,
        "conceitos": explicar_conceitos(g),
        "reputacao_info": explicar_reputacao(g),
        "testes": explicar_testes(g),
        "dificuldade_extra": g.dificuldade(0),
        "ouro": j.ouro, "reputacao": j.reputacao, "flechas": j.flechas if j.classe == "arqueiro" else None,
        "max_flechas": g.max_flechas() if j.classe == "arqueiro" else None,
        "provisoes": j.provisoes, "fome": j.fome, "condicoes": sobrevivencia.condicoes(j),
        **{c["hud"]: j.consumiveis.get(k, 0) for k, c in CONSUMIVEIS.items() if c["hud"]},  # tochas, poções...
        "spec": j.spec, "reputacao_txt": "herói do povo" if j.reputacao >= 20 else "temido" if j.reputacao <= -20 else "",
        "bolsa": [{"id": k, "nome": CONSUMIVEIS[k]["nome"], "qtd": v, "desc": itens.descricao(k, j),
                   "motivo": None if k == "tocha" else g.combate_ativo.motivo_item(k) if g.combate_ativo else g.motivo_inutil(k),
                   **(g.o_que_trata(k) or {}),  # "trata": a bolsa chama a atenção (pulsa)
                   "alvos": [{"id": m["id"], "nome": comitiva.nome(m["id"]), "hp": m["hp"], "max_hp": m["max_hp"],
                              "ferido": m["ferido"], "caido": comitiva.flexao(m["id"], "caíd{a}, não luta"),
                              "motivo": g.motivo_inutil(k, m)}
                             for m in comitiva.junto(g)] + _alvo_animal(g, k) if k in EM_ALIADO and not g.combate_ativo else []}
                  for k, v in j.consumiveis.items() if v > 0 and k in CONSUMIVEIS],
        "equip": {slot: _item(it, j.nome_recurso) for slot, it in j.equip.items()},
        "mochila": [_item(it, j.nome_recurso) for it in j.mochila], "limite_mochila": 12,
        "habilidades": [{"nome": efetiva(j, h)["nome"], "custo": custo_habilidade(j, h), "desc": descricao_habilidade(h, j)}
                        for h in j.habilidades],
        "grimorio": grimorio.dados(j),
        # o kit equipado, para a fileira da barra (consulta): nome, ícone, custo, o que faz e se é a ultimate (usada
        # nesta luta, se houver luta)
        "kit": [{"id": h, "nome": efetiva(j, h)["nome"], "icone": efetiva(j, h)["icone"],
                 "familia": efetiva(j, h)["familia"], "custo": custo_habilidade(j, h),
                 "desc": descricao_habilidade(h, j), "ultimate": bool(HABILIDADES[h].get("ultimate")),
                 "usada": bool(g.combate_ativo and HABILIDADES[h].get("ultimate")
                               and "j" in g.combate_ativo.ultimates_usadas)}
                for h in getattr(j, "kit", []) if h in HABILIDADES],
        "ferimentos": ferimentos, "males": sobrevivencia.descrever(j),
        "pontos_talento": j.pontos_talento, "sigilos": len(j.sigilos),
        "companheiro": ({"nome": j.companheiro["nome"], "hp": j.companheiro["hp"], "max_hp": j.companheiro["max_hp"],
                         "tipo": j.companheiro["tipo"], "animado": bool(j.companheiro.get("animado"))}
                        if j.companheiro else None),
        "efeitos": _efeitos(j, g.combate_ativo),
        "comitiva": comitiva.estado(g),
        # a janela do grupo: a ficha de cada companheiro que anda com você (quem espera no acampamento, não)
        "grupo": [ficha_companheiro(g, m) for m in comitiva.membros(g)],
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
        nos.append({
            "id": loc["id"], "n": loc["id"] + 1, "nome": loc["nome"], "x": loc["x"], "y": loc["y"],
            "tipo": loc["tipo"], "bioma": loc["bioma"], "visitado": loc["visitado"], "atual": loc["id"] == atual,
            "distancia": vizinhos.get(loc["id"]), "descricao": mapa.descricao(g, loc),
            # numa vila, o dos arredores (as estradas por onde se chega e se sai); a saída fechada não tem
            "nivel": None if loc.get("fechado") else nivel_regiao(loc),
            # a viagem não chega lá agora ("fechado", a saída que ainda não leva a lugar nenhum): a mesma
            # regra que a viagem usa para recusar (mapa.bloqueio); o mapa desenha a cancela e tira o convite de viagem
            "bloqueio": mapa.bloqueio(g, loc),
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
            "atk": round(max(e.atk, e.poder)), "defesa": round(e.defesa),
            # o que esta criatura faz de diferente da espécie (a variante da capela: o golpe preparado), sempre à vista
            **({"nota": e.nota} if getattr(e, "nota", None) else {})}


def combate(g):
    cb = g.combate_ativo
    if not cb:
        return None

    def ficha(c, lado):
        d = {"uid": cb.uid(c), "nome": c.nome, "hp": max(0, c.hp), "max_hp": c.max_hp, "efeitos": _efeitos(c, cb), "lado": lado,
             "vivo": c.vivo, "tracos": list(getattr(c, "tracos", []) or []), "cid": getattr(c, "cid", None),
             # o aliado invocado traz o dele, escolhido pelo motor ao invocar (1.196.0); os outros, pelos traços e afins
             "retrato": getattr(c, "retrato", None) or retrato(
                 getattr(c, "tracos", []) or [], getattr(c, "familia", None), getattr(c, "chave", None),
                 getattr(c, "guardiao", None), getattr(c, "origem", None)),
             "tipo": getattr(c, "tipo", None),
             # o recurso de quem escolhe a ação (a comitiva, etapa 4): Fé, Vigor ou Mana, na carta
             **({"rec": c.rec, "max_rec": c.max_rec, "recurso": c.nome_recurso}
                if getattr(c, "tipo", None) == "comitiva" and getattr(c, "max_rec", 0) else {}),
             # o desenho da sala que é este inimigo (a sacristia: os dois de capa escura), para a tela seguir a carta
             **({"figura": c.figura} if getattr(c, "figura", None) else {})}
        if lado == "inimigo":
            d.update(nivel=c.nivel, chefe=c.chefe, unico=getattr(c, "unico", False), afixo=c.afixo,
                     invocado=getattr(c, "invocado", False),
                     familia=c.familia, preparando=bool(c.carregando), ficha=_ficha_inimigo(g, c))
        return d

    return {
        "titulo": cb.titulo, "turno": cb.turno,
        # a ordem fixa da luta (etapa 4): quem age, em ordem, quem já passou nesta rodada e quem está fora
        "ordem": cb.ordem_para_tela(),
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
        # O que vale em todo lugar (o +1 inimigo só onde o bando varia; o nível não sobe nos guardiões).
        m.append({"icone": "lua", "texto": f"Inimigos +{bal.NOITE_NIVEL} nível",
                  "detalhe": f"Noite: os inimigos dos encontros e das salas vêm {'um nível' if bal.NOITE_NIVEL == 1 else f'{bal.NOITE_NIVEL} níveis'} acima "
                             "(os guardiões, não). Onde o bando varia, às vezes vem um a mais; nas salas, o número é o "
                             f"mesmo. Todos causam {round((bal.NOITE_INIMIGOS - 1) * 100)}% mais dano."})
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
        fechados["curandeiro"] = g.fala_curandeira_sem_ferimento()
    return fechados


def atendentes(g):
    """Quem atende em cada prédio, quando não é o de sempre (o nome no balcão): só a curandeira do Vau, por ora."""
    quem = consequencias.atendente(g)
    return {"curandeiro": quem["quem"]} if quem else {}


def glossario():
    """A cor de cada nome de habilidade, talento e passiva que a tela realça nos textos de regra ("Bola de Fogo" em
    laranja, "Drenar Vida" em vermelho): o campo `realce` dos catálogos. Quem não declara fica neutro."""
    from ..talentos import PASSIVAS, POR_ID
    fichas = list(HABILIDADES.values()) + list(VARIANTES.values()) + list(POR_ID.values()) + list(PASSIVAS.values())
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
                  "riscos": sobrevivencia.riscos_do_lugar(g, missoes.tem_salas(g)),
                  **({"atendentes": atendentes(g)} if atendentes(g) else {}),  # só no Vau da campanha
                  "estrada": g.na_estrada},  # viajando: a paisagem é a da região, sem a vila
        "mapa": mapa_conhecido(g),
        "combate": combate(g),
        "orientacao": abertura.para_tela(g),  # o quadro de agora e a Ajuda (abertura.py)
        "estados": para_tela(),  # ícone, cor e dica de cada estado (catálogo em estados.py)
        "glossario": glossario(),
        "itens": itens.para_tela(),  # ícone e contador de cada consumível e recurso
        "contratos": [g.cartao_contrato(c) for c in g.contratos],
        "missoes": missoes.cartoes(g),  # a missão da campanha
        **({"capitulo": capitulo.para_tela(g)} if capitulo.concluido(g) else {}),  # o fim do capítulo, no rastreador
    }
