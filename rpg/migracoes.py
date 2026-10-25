"""Versões do formato do save e as migrações entre elas.

Cada vez que o formato muda (campo novo, campo renomeado, estrutura diferente), sobe-se VERSAO_SAVE e
acrescenta-se uma função `_vN_para_vN1` em MIGRACOES. Um save antigo passa por todas, em ordem, até
chegar à versão atual; assim nenhum código do jogo precisa se defender de saves velhos.
"""

VERSAO_SAVE = 6

# Tudo o que o estado da partida guarda além do jogador, da semente e do gerador aleatório.
CAMPOS_SAVE = ("mundo", "dia", "periodo", "clima", "passos", "flags", "historico", "contagem",
               "impulsos", "sementes", "rumores", "contratos", "ofertas", "lojas", "nemesis", "forcados",
               "proximo_id", "estatisticas", "hardcore", "bestiario", "registro",
               "arquivo_run", "comitiva", "reserva")

ESPACOS_EQUIP = ("cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes", "anel1", "anel2")


class SaveIncompativel(Exception):
    """O save é de uma versão do jogo mais nova do que esta (ou não é um save)."""


def _v1_para_v2(d):
    """Junta num lugar só as correções que o carregamento fazia aos poucos para saves antigos."""
    for loc in d["mundo"]["locais"]:  # mapas antigos não tinham coordenadas
        loc.setdefault("x", 0.03 + 0.9 * (loc["perigo"] - 1) / 4 if loc["id"] else 0.03)
        loc.setdefault("y", 0.08 + 0.84 * ((loc["id"] * 5) % 11) / 10)
    j = d["jogador"]
    j.setdefault("talentos", {})
    j.setdefault("pontos_talento", max(0, j["nivel"] - 1))
    j.setdefault("provisoes", 4)
    j.setdefault("fome", 0)
    j.setdefault("ferimentos", [])
    for s in ESPACOS_EQUIP:  # saves antigos tinham só arma, armadura e amuleto
        j["equip"].setdefault(s, None)
    d.setdefault("comitiva", [])
    d.setdefault("reserva", [])
    return d


def _v2_para_v3(d):
    """A corrupção do reino saiu do jogo (1.16)."""
    d.pop("corrupcao", None)
    return d


def _v3_para_v4(d):
    """O baú da sacristia passou a ser recolhido pela ação (1.85.0). Quem venceu a sacristia antes já o recebeu na
    vitória, aberto ou gasto depois: fica "recolhido", para não vir outro (não se deduz pela bolsa)."""
    m = ((d.get("mundo") or {}).get("missoes") or {}).get("febre_do_turvo")
    if m and (m.get("etapa") in ("ossuario", "fundo", "retorno") or m.get("desfecho") or m.get("concluida")):
        m.setdefault("bau", "recolhido")
    return d


# O Capuz e a Luva de Seda do Mago ganharam desenhos de tecido (1.112.0); os itens guardados antes levam o desenho de
# couro, que continua sendo o do Arqueiro (Capuz, Chapéu de Couro, Braçadeira) e o das Mãos do Estrangulador (sem
# classe). O que decide é o próprio item: o espaço, a classe para a qual foi feito e o desenho que ele guarda.
TECIDO_DO_MAGO = {("cabeca", "capuz"): "capuz_tecido", ("maos", "luva"): "luva_seda"}


def _desenho_de_tecido(no):
    """Percorre o save inteiro (o corpo, a mochila, as lojas, as ofertas, a comitiva, onde houver item) e troca o
    desenho das peças de tecido do Mago. Só o campo "icone" muda; nome, base, bônus, preço, raridade e o resto ficam."""
    if isinstance(no, dict):
        novo = TECIDO_DO_MAGO.get((no.get("slot"), no.get("icone")))
        if novo and no.get("classe") == "mago" and "bonus" in no:
            no["icone"] = novo
        for v in no.values():
            _desenho_de_tecido(v)
    elif isinstance(no, list):
        for v in no:
            _desenho_de_tecido(v)


def _v4_para_v5(d):
    """O Capuz e a Luva de Seda do Mago com os desenhos de tecido (os itens guardados antes estavam com o couro)."""
    _desenho_de_tecido(d)
    return d


# As famílias que mudaram de nome (1.181.0: o ent jovem virou a árvore desperta): o texto dos contratos delas é refeito.
FAMILIAS_RENOMEADAS = ("ent_jovem",)


def _v5_para_v6(d):
    """As árvores vivas com o nome novo (1.181.0): o ent jovem é a árvore desperta; o Ent Ancião, a Árvore Anciã. Os ids
    (`ent_jovem`, `ent_anciao`) ficam, e o progresso também; só o que o save guardou como texto é refeito pelo catálogo:
    o guardião de cada covil (o `base`, o gênero e o nome com o artigo, "Thorn, a Árvore Anciã"; os rumores que citam o
    nome antigo dele) e o texto dos contratos das famílias renomeadas, os aceitos e os do mural. Refazer de novo não
    muda nada: rodar duas vezes dá o mesmo save."""
    import re
    from .inimigos import ficha_guardiao
    from .sistemas.contratos import desc_alvo, desc_caca
    mundo = d.get("mundo") or {}
    locais = {l["id"]: l for l in mundo.get("locais", [])}
    nomes = {}
    for l in locais.values():
        gu = l.get("guardiao")
        if not gu or "bioma" not in gu:
            continue
        t = ficha_guardiao(gu)
        if gu.get("base") == t["base"] and gu.get("g") == t["g"]:
            continue
        proprio = re.split(r", (?:the|o|a) ", gu["nome"], maxsplit=1)[0]
        novo = f"{proprio}, {'o' if t['g'] == 'm' else 'a'} {t['base']}"
        nomes[gu["nome"]] = novo
        gu.update(nome=novo, base=t["base"], g=t["g"])
    for r in d.get("rumores") or []:
        for velho, novo in nomes.items():
            if velho in r.get("texto", ""):
                r["texto"] = r["texto"].replace(velho, novo)
    contratos = list(d.get("contratos") or [])
    ofertas = d.get("ofertas") or {}
    for oferta in ofertas.values() if isinstance(ofertas, dict) else ofertas:  # o mural: {vila: {"dia", "lista"}}
        if isinstance(oferta, dict):
            contratos += oferta.get("lista", [])
    for c in contratos:
        lugar = locais.get(c.get("local"))
        if c.get("familia") not in FAMILIAS_RENOMEADAS or not lugar:
            continue
        if c.get("tipo") == "caca":
            c["desc"] = desc_caca(c["total"], c["familia"], lugar["nome"])
        elif c.get("tipo") == "alvo":
            c["desc"] = desc_alvo(c["nome"], c["familia"], lugar["nome"])
    return d


MIGRACOES = {1: _v1_para_v2, 2: _v2_para_v3, 3: _v3_para_v4, 4: _v4_para_v5, 5: _v5_para_v6}


def migrar(dados):
    """Leva um save de qualquer versão antiga até VERSAO_SAVE."""
    if not isinstance(dados, dict) or "jogador" not in dados or "seed" not in dados:
        raise SaveIncompativel("o arquivo não é um save de The Unquiet.")
    versao = dados.get("versao", 1)
    if versao > VERSAO_SAVE:
        raise SaveIncompativel(f"é de uma versão mais nova do jogo (formato {versao}; "
                               f"este jogo lê até o {VERSAO_SAVE}). Atualize o jogo para continuar.")
    while versao < VERSAO_SAVE:
        dados = MIGRACOES[versao](dados)
        versao += 1
    dados["versao"] = versao
    return dados
