"""Árvores de talentos.

Cada classe tem uma árvore em 3 colunas: a do meio é o tronco comum da classe
e as laterais reforçam cada especialização (só ativáveis com ela). Cada camada
exige um nível mínimo. Pontos vêm de subir de nível e de derrotar guardiões.

Os efeitos "stats" são somados aos atributos; os demais talentos são lidos
pelo combate e pelas habilidades através de `jogador.tal("id")`.
"""

from .classes import CLASSES, HABILIDADES, SPECS

NIVEL_CAMADA = {1: 2, 2: 4, 3: 6, 4: 9}


def _t(id, nome, camada, coluna, maximo, desc, spec=None, stats=None):
    return {"id": id, "nome": nome, "camada": camada, "coluna": coluna, "max": maximo, "desc": desc,
            "spec": spec, "stats": stats or {}}


TALENTOS = {
    "guerreiro": [
        _t("pele_ferro", "Pele de Ferro", 1, 0, 3, "+2 Defesa e +6 Vida por ponto.",
           stats={"defesa": 2, "max_hp": 6}),
        _t("golpe_brutal", "Golpe Brutal", 1, 1, 3, "+6% de dano corpo a corpo por ponto."),
        _t("folego", "Fôlego", 1, 2, 2, "+3 de Vigor regenerado por turno, por ponto.",
           stats={"regen": 3}),
        _t("luz_curativa", "Luz Curativa", 2, 0, 2, "Golpe Sagrado e Prece curam +25% por ponto.", "paladino"),
        _t("contra_ataque", "Contra-ataque", 2, 1, 2, "15% de chance por ponto de revidar golpes corpo a corpo."),
        _t("sede_insaciavel", "Sede Insaciável", 2, 2, 2, "Todo dano que você causa cura 5% dele, por ponto.",
           "berserker"),
        _t("aura_protecao", "Aura de Proteção", 3, 0, 1, "Começa cada combate com uma barreira sagrada.", "paladino"),
        _t("muralha", "Muralha", 3, 1, 1, "Erguer Escudo dura 1 turno a mais e custa 4 a menos."),
        _t("frenesi", "Frenesi", 3, 2, 2, "Cada inimigo que você abate dá +10% de dano por ponto (acumula 3x).",
           "berserker"),
        _t("martirio", "Martírio", 4, 0, 1, "Uma vez por combate, ao cair abaixo de 25% de vida, cura 40%.",
           "paladino"),
        _t("imortal", "Imortal", 4, 2, 1, "Uma vez por combate, sobrevive a um golpe fatal com 1 de vida e "
                                          "entra em fúria.", "berserker"),
    ],
    "arqueiro": [
        _t("olho_aguia", "Olho de Águia", 1, 0, 3, "+4% de chance de crítico por ponto."),
        _t("pes_leves", "Pés Leves", 1, 1, 3, "+2 Agilidade por ponto.", stats={"agi": 2}),
        _t("aljava_funda", "Aljava Funda", 1, 2, 2, "+20% de chance por ponto de recuperar flechas."),
        _t("laco_animal", "Laço Animal", 2, 0, 3, "Seu companheiro ganha +20% de vida e ataque por ponto.",
           "patrulheiro"),
        _t("tiro_abertura", "Tiro de Abertura", 2, 1, 1, "Seu primeiro ataque em cada combate é sempre crítico."),
        _t("laminas_envenenadas", "Pontas Venenosas", 2, 2, 2,
           "Ataques básicos têm 20% de chance por ponto de envenenar.", "sombra"),
        _t("armadilheiro", "Armadilheiro", 3, 0, 1, "Cada combate começa com um inimigo preso numa armadilha.",
           "patrulheiro"),
        _t("mira_firme", "Mira Firme", 3, 1, 2, "+8% de dano à distância por ponto."),
        _t("golpe_sombras", "Golpe Sombrio", 3, 2, 2, "Críticos causam +20% de dano por ponto.", "sombra"),
        _t("matilha", "Matilha", 4, 0, 1, "Seu companheiro ataca duas vezes por turno.", "patrulheiro"),
        _t("assassino", "Assassino", 4, 2, 1, "Abater um inimigo devolve metade do Foco e te deixa furtivo.",
           "sombra"),
    ],
    "mago": [
        _t("mente_vasta", "Mente Vasta", 1, 0, 3, "+8 de Mana máxima por ponto.", stats={"max_rec": 8}),
        _t("potencia_arcana", "Potência Arcana", 1, 1, 3, "+2 Poder por ponto.", stats={"poder": 2}),
        _t("canalizacao", "Canalização", 1, 2, 2, "+2 de Mana regenerada por turno, por ponto.",
           stats={"regen": 2}),
        _t("brasas", "Brasas Eternas", 2, 0, 2, "Queimaduras causam +30% de dano por ponto e duram 1 turno a mais.",
           "piromante"),
        _t("escudo_reflexo", "Escudo Rúnico", 2, 1, 1, "A Barreira Arcana absorve 30% a mais e dura 1 turno a mais."),
        _t("pacto_sombrio", "Pacto Sombrio", 2, 2, 2, "Drenar Vida cura +10% e servos têm +15% de vida, por ponto.",
           "necromante"),
        _t("ignicao", "Ignição", 3, 0, 1, "A Bola de Fogo sempre deixa o alvo em chamas.", "piromante"),
        _t("eficiencia", "Eficiência", 3, 1, 2, "Habilidades custam 10% menos por ponto."),
        _t("exercito", "Legião de Ossos", 3, 2, 1, "Você pode manter um servo a mais.", "necromante"),
        _t("coracao_ardente", "Coração Ardente", 4, 0, 1, "Inimigos mortos por fogo explodem, ferindo os outros.",
           "piromante"),
        _t("senhor_mortos", "Rei dos Mortos", 4, 2, 1, "O primeiro inimigo a cair em cada combate se ergue como "
                                                          "seu servo.", "necromante"),
    ],
}

POR_ID = {t["id"]: t for lista in TALENTOS.values() for t in lista}


def bonus_stats(jogador):
    total = {}
    for tid, rank in jogador.talentos.items():
        for stat, v in POR_ID[tid]["stats"].items():
            total[stat] = total.get(stat, 0) + v * rank
    return total


def custo_habilidade(jogador, hid):
    custo = HABILIDADES[hid]["custo"]
    if hid == "erguer_escudo" and jogador.tal("muralha"):
        custo -= 4
    custo *= 1 - 0.1 * jogador.tal("eficiencia")
    return max(0, int(round(custo)))


def estado(jogador, t):
    """'comprado' (no máximo), 'disponivel', 'nivel', 'spec' ou 'bloqueado'."""
    rank = jogador.tal(t["id"])
    if rank >= t["max"]:
        return "comprado"
    if t["spec"] and jogador.spec and jogador.spec != t["spec"]:
        return "bloqueado"
    if t["spec"] and not jogador.spec:
        return "spec"
    if jogador.nivel < NIVEL_CAMADA[t["camada"]]:
        return "nivel"
    return "disponivel"


def motivo(t, est):
    if est == "nivel":
        return f"requer nível {NIVEL_CAMADA[t['camada']]}"
    if est == "spec":
        return f"requer {SPECS[t['spec']]['nome']}"
    if est == "bloqueado":
        return f"exclusivo de {SPECS[t['spec']]['nome']}"
    return ""


def dados_arvore(jogador):
    """A árvore em dados, para a interface gráfica desenhar (colunas: spec A, tronco, spec B)."""
    a, b = CLASSES[jogador.classe]["specs"]
    nos = []
    for t in TALENTOS[jogador.classe]:
        est = estado(jogador, t)
        nos.append({"id": t["id"], "nome": t["nome"], "desc": t["desc"], "camada": t["camada"], "coluna": t["coluna"],
                    "rank": jogador.tal(t["id"]), "max": t["max"], "estado": est, "motivo": motivo(t, est),
                    "spec": SPECS[t["spec"]]["nome"] if t["spec"] else None})
    return {"classe": CLASSES[jogador.classe]["nome"], "pontos": jogador.pontos_talento, "nivel": jogador.nivel,
            "colunas": [SPECS[a]["nome"], "Tronco comum", SPECS[b]["nome"]], "spec": jogador.spec,
            "camadas": {str(k): v for k, v in NIVEL_CAMADA.items()}, "nos": nos}


def desenhar(jogador, largura=76):
    """Linhas (pedaços texto/cor) com a árvore em 3 colunas."""
    col = (largura - 8) // 3
    cores = {"comprado": "verde+negrito", "disponivel": "amarelo", "nivel": "cinza", "spec": "cinza",
             "bloqueado": "cinza"}
    a, b = CLASSES[jogador.classe]["specs"]
    titulos = ["← " + SPECS[a]["nome"].upper(), "TRONCO COMUM", SPECS[b]["nome"].upper() + " →"]
    linhas = [[("        ", None)] + [(t.center(col), "ciano+negrito") for t in titulos]]
    for camada in (1, 2, 3, 4):
        nos = {t["coluna"]: t for t in TALENTOS[jogador.classe] if t["camada"] == camada}
        linha = [(f"Nv.{NIVEL_CAMADA[camada]:<2}   ", "cinza")]
        for c in range(3):
            t = nos.get(c)
            if not t:
                linha.append(("·".center(col), "cinza"))
                continue
            est = estado(jogador, t)
            marca = "✓" if est == "comprado" else ("✗" if est == "bloqueado" else "")
            texto = f"{t['nome'][:col - 6]} {jogador.tal(t['id'])}/{t['max']}{marca}"
            linha.append((f"[{texto}]".center(col), cores[est]))
        linhas.append(linha)
        if camada < 4:
            linhas.append([("        ", None)] + [("│".center(col), "cinza") for _ in range(3)])
    return linhas
