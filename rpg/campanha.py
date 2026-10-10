"""A campanha escrita: regiões de mapa fixo, que o motor percorre como percorre o mundo gerado.

Protótipo da E2 (roadmapIDEIAS/11-E1-REGIAO-INICIAL.md): só o Vale do Turvo, com início, viagem, descoberta e save.
Missão, cenas escritas, encontros fixos da comitiva e finais ainda não existem aqui.

O mundo montado tem o mesmo formato do procedural (mundo.gerar_mundo): lugares com id numérico pela posição na lista,
`con` com as estradas, `visitado`, `perigo`, x/y no mapa. Cada lugar ganha também uma `chave` estável (o id narrativo,
para missões e falas futuras) e um `nivel` fixo. O mundo leva `campanha` (o id da região) e `antagonista` vazio: o vilão
da campanha ainda não foi decidido.
"""

from . import missoes

REGIOES = {
    "turvo": dict(
        nome="Vale do Turvo",
        inicio="vau_do_turvo",
        # (chave, nome, tipo, bioma, nível, perigo, x, y). Nível: o dos inimigos (numa vila, o dos arredores). Perigo:
        # a mesma escala do procedural (afixos, criaturas da Fenda), coerente com o nível.
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

# Eventos do mundo gerado que não cabem na campanha (falam do vilão sorteado, que a campanha ainda não tem). Os
# outros eventos (ambiente, bioma, classe, comitiva, contratos do mural) continuam valendo.
EVENTOS_FORA = frozenset({
    "visao_do_vazio",       # o vilão sorteado e os covis dos guardiões
    "veterano_cicatrizes",  # ouvir as histórias fala do vilão sorteado
    "sonho_profetico",      # o covil e o trono do vilão sorteado
    "sussurros_do_vazio",   # a voz do vilão sorteado na fogueira
    "pregador_do_vazio",    # o vilão sorteado (o pregador da campanha vem na E3)
})


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
    return {"locais": locais, "antagonista": None, "atual": 0, "campanha": regiao,
            "missoes": missoes.estado_inicial(regiao)}


def ajustar_save(g):
    """Saves da campanha de antes das missões (1.48–1.49): a missão entra na primeira etapa, sem cenas vistas. Nada do
    que já existe muda (personagem, bolsa, mapa descoberto, lugar); a cena de abertura toca na próxima vez em que a
    pessoa estiver no Vau do Turvo. O mundo gerado não tem missões."""
    if g.campanha and "missoes" not in g.mundo:
        g.mundo["missoes"] = missoes.estado_inicial(g.campanha)


def nome(regiao):
    return REGIOES[regiao]["nome"] if regiao in REGIOES else None


def eventos_fora(g):
    """Os ids de evento que não valem nesta partida: nenhum no procedural."""
    return EVENTOS_FORA if g.campanha else frozenset()
