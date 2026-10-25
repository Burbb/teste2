"""A campanha: regiões de mapa fixo (E2, roadmapIDEIAS/11-E1-REGIAO-INICIAL.md). Hoje, o Vale do Turvo. Desde a
1.206.0 é o único modo do jogo (o mundo gerado saiu: roadmapIDEIAS/24-RETIRADA-DO-PROCEDURAL.md).

O mundo montado: lugares com id numérico pela posição na lista, `con` com as estradas, `visitado`, `perigo`, x/y no
mapa, uma `chave` estável (o id narrativo, para missões e falas) e um `nivel` fixo. O mundo leva `campanha` (o id da
região) e as missões dela.
"""

from . import caspar, missoes

INICIO = "turvo"  # a região em que a campanha começa

REGIOES = {
    "turvo": dict(
        nome="Vale do Turvo",
        inicio="vau_do_turvo",
        # (chave, nome, tipo, bioma, nível, perigo, x, y). Nível: o dos inimigos (numa vila, o dos arredores). Perigo:
        # de 1 a 5 (afixos, criaturas da Fenda), coerente com o nível.
        lugares=[
            ("vau_do_turvo", "Vau do Turvo", "vila", "planicie", 1, 1, 0.40, 0.55),
            ("charco_dos_juncos", "Charco dos Juncos", "selvagem", "pantano", 1, 1, 0.14, 0.40),
            ("bosque_do_moinho", "Bosque do Moinho", "selvagem", "floresta", 2, 2, 0.64, 0.36),
            ("capela_afogada", "Capela Afogada", "selvagem", "ruinas", 3, 2, 0.86, 0.20),
            ("estrada_de_varn", "Estrada de Varn", "saida", "planicie", 5, 3, 0.46, 0.92),
        ],
        # (de, para, trechos)
        estradas=[
            ("vau_do_turvo", "charco_dos_juncos", 1),
            ("vau_do_turvo", "bosque_do_moinho", 1),
            ("bosque_do_moinho", "capela_afogada", 1),
            ("vau_do_turvo", "estrada_de_varn", 2),
        ],
        # Lugares que existem no mapa mas ainda não se alcançam, com o porquê (a viagem para antes de sair).
        fechados={
            "estrada_de_varn": "A estrada para Varn desce o vale rumo ao sul. Por enquanto ela não leva a lugar "
                               "nenhum: esta saída abre numa próxima parte da campanha.",
        },
    ),
}

def montar_mundo(regiao):
    """O mundo de uma região escrita, no formato do procedural. O lugar de início é o id 0."""
    r = REGIOES[regiao]
    ordem = sorted(r["lugares"], key=lambda l: l[0] != r["inicio"])  # o início primeiro; o resto na ordem escrita
    ids = {lugar[0]: i for i, lugar in enumerate(ordem)}
    locais = []
    for i, (chave, nome, tipo, bioma, nivel, perigo, x, y) in enumerate(ordem):
        loc = {"id": i, "chave": chave, "nome": nome, "tipo": tipo, "bioma": bioma, "con": {}, "visitado": False,
               "perigo": perigo, "nivel": nivel, "guardiao": None, "x": x, "y": y}
        if chave in r["fechados"]:
            loc["fechado"] = r["fechados"][chave]
        locais.append(loc)
    for a, b, trechos in r["estradas"]:
        locais[ids[a]]["con"][str(ids[b])] = trechos
        locais[ids[b]]["con"][str(ids[a])] = trechos
    return {"locais": locais, "atual": 0, "campanha": regiao,
            "missoes": missoes.estado_inicial(regiao)}


def ajustar_save(g):
    """Saves da campanha de antes das missões (1.48–1.49): a missão entra na primeira etapa, sem cenas vistas. Nada do
    que já existe muda (personagem, bolsa, mapa descoberto, lugar); a cena de abertura toca na próxima vez em que a
    pessoa estiver no Vau do Turvo."""
    if g.campanha and "missoes" not in g.mundo:
        g.mundo["missoes"] = missoes.estado_inicial(g.campanha)
    elif g.campanha:
        for mid, m in missoes.estado_inicial(g.campanha).items():  # missões novas da região (1.55: Caspar)
            g.mundo["missoes"].setdefault(mid, m)
        missoes.completar(g.mundo["missoes"])  # 1.50–1.53: sem `preparos`, `desfecho`, `concluida`
        for m in g.mundo["missoes"].values():
            if m["desfecho"] and m["dia_desfecho"] is None:  # 1.53: resolvida antes do dia ser guardado; conta de hoje
                m["dia_desfecho"] = g.dia
        caspar.sincronizar(g)  # com a guardiã já resolvida, a resposta a Caspar fica para a praça


def nome(regiao):
    return REGIOES[regiao]["nome"] if regiao in REGIOES else None
