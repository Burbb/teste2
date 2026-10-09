"""Árvores de talentos.

Cada classe tem uma árvore em 3 colunas: a do meio é o tronco comum da classe
e as laterais reforçam cada especialização (só ativáveis com ela). Cada camada
exige um nível mínimo. Pontos vêm de subir de nível e de derrotar guardiões.

Cada talento declara o que faz, ao lado da própria definição:
    stats     somados aos atributos (por ponto)
    mods      modificadores por ponto (veja modificadores.py: dano_corpo, critico, custo_pct...)
    mults     multiplicadores
    gatilhos  reações a acontecimentos (abate, golpe recebido, início do combate...)
O combate e as habilidades só perguntam `mod(u, chave)` e `disparar(...)`: um talento novo não mexe neles.
A passiva de cada especialização (PASSIVAS) segue o mesmo formato.
"""

from . import balanceamento as bal
from .classes import CLASSES, SPECS
from .habilidades import HABILIDADES
from .modificadores import Fixo, mod


# ---------------------------------------------------------------------- gatilhos (reações dos talentos)
def _aura_protecao(cb, u, rank, d):
    u.aplicar("barreira", 99, int(u.poder * 1.5))
    cb.dizer(f"Uma aura dourada te envolve. (barreira de {int(u.poder * 1.5)})", "amarelo")


def _armadilheiro(cb, u, rank, d):
    alvo = cb.rng.choice(cb.inimigos_vivos())
    cb.dizer(f"{alvo.nome} pisa numa das suas armadilhas!", "verde")
    cb.aplicar(alvo, "atordoado", 1, rotulo="preso na armadilha")
    cb.aplicar(alvo, "sangramento", 3, valor=max(2, u.atk * 0.3))


def _imortal(cb, u, rank, d):
    if cb.usou_imortal:
        return
    cb.usou_imortal = True
    d["dano"] = u.hp - 1
    u.aplicar("furia", 3, 0.5)
    cb.dizer("Um golpe que deveria te matar... mas você se recusa a cair! (Imortal)", "vermelho+negrito")


def _martirio(cb, u, rank, d):
    if not cb.usou_martirio and u.hp < u.max_hp * 0.25:
        cb.usou_martirio = True
        cura = u.curar(u.max_hp * 0.4)
        cb.curou(u, cura, rotulo="Martírio")
        cb.dizer(f"Seu sacrifício é visto. Uma luz desce e te restaura. (Martírio, +{cura} vida)", "amarelo+negrito")


def _contra_ataque(cb, u, rank, d):
    de = d["de"]
    if d["alcance"] == "corpo" and de in cb.inimigos and de.vivo and cb.rng.random() < mod(u, "contra_ataque"):
        cb.atacar(u, de, 0.7, rotulo="Contra-ataque", reacao=True)


def _laminas(cb, u, rank, d):
    cb.aplicar(d["alvo"], "veneno", 3, valor=max(2, u.atk * 0.35), chance=0.2 * rank)


def _colheita(cb, u, rank, d):
    antes = u.rec
    u.rec = min(u.max_rec, u.rec + 5)
    cb.recuperou(u, u.rec - antes, "Colheita")


def _senhor_mortos(cb, u, rank, d):
    c = d["alvo"]
    if len(cb.mortos) == 1 and not c.chefe:
        cb.dizer(f"{c.nome} se ergue de novo — agora sob o seu comando!", "magenta")
        cb.invocar_aliado(f"{c.nome} (servo)", hp=int(c.max_hp * 0.4), atk=c.atk * 0.5)


def _frenesi(cb, u, rank, d):
    cb.frenesi = min(3, cb.frenesi + 1)
    u.aplicar("frenesi", 99, 0)
    u.efeitos["frenesi"]["v"] = 0.1 * rank * cb.frenesi  # o próprio estado, que só cresce: não mexe na Fúria nem no Grito
    cb.dizer(f"O sangue ferve: Frenesi x{cb.frenesi}!", "vermelho")


def _assassino(cb, u, rank, d):
    antes = u.rec
    u.rec = min(u.max_rec, u.rec + u.max_rec // 2)
    cb.recuperou(u, u.rec - antes)
    u.aplicar("furtivo", 2, 1)
    cb.dizer("Você some antes que o corpo toque o chão. (Assassino)", "magenta")


def _coracao_ardente(cb, u, rank, d):
    c = d["alvo"]
    if d["tipo"] == "fogo" and not cb.explodindo:
        cb.explodindo = True
        cb.dizer(f"{c.nome} explode em chamas!", "vermelho+negrito")
        for outro in cb.inimigos_vivos():
            cb.atacar(u, outro, 0.6, tipo="fogo", alcance="distancia", stat="poder", pode_esquivar=False,
                      rotulo="Explosão")
        cb.explodindo = False


# A passiva de cada especialização: vem com ela, sem ponto de talento.
PASSIVAS = {
    "berserker": {"nome": "Pacto de Sangue", "desc": "Até +60% de dano quanto mais ferido você estiver.",
                  "mods": {"dano_ferido": 0.6}, "realce": "sangue"},
    "piromante": {"nome": "Chama Viva", "desc": f"Queimaduras causam {round((bal.QUEIMADURA_PIROMANTE - 1) * 100)}% a mais.",
                  "mults": {"queimadura_mult": bal.QUEIMADURA_PIROMANTE}},
    "necromante": {"nome": "Colheita", "desc": "Cada inimigo que cai devolve 5 de mana.",
                   "gatilhos": {"morte": _colheita}},
}

NIVEL_CAMADA = {1: 2, 2: 4, 3: 6, 4: 9}


def _t(id, nome, camada, coluna, maximo, desc, spec=None, stats=None, mods=None, mults=None, gatilhos=None, ordem=50,
       icone="estrela", realce=None):
    """icone: o desenho do nó na árvore; realce: a cor do nome quando aparece num texto de regra (Realce, na tela)."""
    return {"id": id, "nome": nome, "camada": camada, "coluna": coluna, "max": maximo, "desc": desc,
            "spec": spec, "stats": stats or {}, "mods": mods or {}, "mults": mults or {}, "gatilhos": gatilhos or {},
            "ordem": ordem, "icone": icone, "realce": realce}


TALENTOS = {
    "guerreiro": [
        _t("pele_ferro", "Pele de Ferro", 1, 0, 3, "+2 Defesa e +6 Vida por ponto.",
           stats={"defesa": 2, "max_hp": 6}, icone="escudo"),
        _t("golpe_brutal", "Golpe Brutal", 1, 1, 3, "+6% de dano corpo a corpo por ponto.",
           mods={"dano_corpo": 0.06}, icone="espada"),
        _t("folego", "Fôlego", 1, 2, 2, "+3 de Vigor regenerado por turno, por ponto.",
           stats={"regen": 3}, icone="coracao"),
        _t("luz_curativa", "Luz Curativa", 2, 0, 2, "Golpe Sagrado e Prece curam +25% por ponto.", "paladino",
           mods={"cura_luz": 0.25}, icone="estrela"),
        _t("contra_ataque", "Contra-ataque", 2, 1, 2, "15% de chance por ponto de revidar golpes corpo a corpo.",
           mods={"contra_ataque": 0.15}, gatilhos={"golpe_recebido": _contra_ataque}, ordem=20, icone="espada"),
        _t("sede_insaciavel", "Sede Insaciável", 2, 2, 2, "Todo dano que você causa cura 5% dele, por ponto.",
           "berserker", mods={"roubo_vida": 0.05}, icone="gota", realce="sangue"),
        _t("aura_protecao", "Aura de Proteção", 3, 0, 1, "Começa cada combate com uma barreira sagrada.", "paladino",
           gatilhos={"inicio_combate": _aura_protecao}, icone="escudo"),
        _t("muralha", "Muralha", 3, 1, 1, "Erguer Escudo dura 1 turno a mais e custa 4 a menos.",
           mods={"escudo_turnos": 1, "custo:erguer_escudo": Fixo(-4)}, icone="escudo"),
        _t("frenesi", "Frenesi", 3, 2, 2, "Cada inimigo que você abate dá +10% de dano por ponto (acumula 3x).",
           "berserker", gatilhos={"abate": _frenesi}, icone="chama"),
        _t("martirio", "Martírio", 4, 0, 1, "Uma vez por combate, ao cair abaixo de 25% de vida, cura 40%.",
           "paladino", gatilhos={"golpe_recebido": _martirio}, ordem=10, icone="coracao"),
        _t("imortal", "Imortal", 4, 2, 1, "Uma vez por combate, sobrevive a um golpe fatal com 1 de vida e "
                                          "entra em fúria.", "berserker", gatilhos={"golpe_fatal": _imortal},
           icone="caveira"),
    ],
    "arqueiro": [
        _t("olho_aguia", "Olho de Águia", 1, 0, 3, "+4% de chance de crítico por ponto.",
           mods={"critico": 0.04}, icone="olho"),
        _t("pes_leves", "Pés Leves", 1, 1, 3, "+2 Agilidade por ponto.", stats={"agi": 2}, icone="folha"),
        _t("aljava_funda", "Aljava Funda", 1, 2, 2, "+15% de chance por ponto de recuperar flechas e +5 de espaço na aljava.",
           mods={"aljava": bal.ALJAVA_POR_TALENTO, "recolher_flecha": bal.RECOLHER_FLECHA_TALENTO}, icone="aljava"),
        _t("laco_animal", "Laço Animal", 2, 0, 3, "Seu companheiro ganha +20% de vida e ataque por ponto.",
           "patrulheiro", mods={"laco_animal": 0.2}, icone="fera"),
        _t("tiro_abertura", "Tiro de Abertura", 2, 1, 1, "Seu primeiro ataque em cada combate é sempre crítico.",
           mods={"abertura": Fixo(1)}, icone="flecha"),
        _t("laminas_envenenadas", "Pontas Venenosas", 2, 2, 2,
           "Ataques básicos têm 20% de chance por ponto de envenenar.", "sombra",
           mods={"veneno_basico": 0.2}, gatilhos={"ataque_basico": _laminas}, icone="gota"),
        _t("armadilheiro", "Armadilheiro", 3, 0, 1, "Cada combate começa com um inimigo preso numa armadilha.",
           "patrulheiro", gatilhos={"inicio_combate": _armadilheiro}, icone="cadeado"),
        _t("mira_firme", "Mira Firme", 3, 1, 2, "+8% de dano à distância por ponto.",
           mods={"dano_distancia": 0.08}, icone="flecha"),
        _t("golpe_sombras", "Golpe Sombrio", 3, 2, 2, "Críticos causam +20% de dano por ponto.", "sombra",
           mods={"mult_critico": 0.2}, icone="caveira"),
        _t("matilha", "Matilha", 4, 0, 1, "Seu companheiro ataca duas vezes por turno.", "patrulheiro",
           mods={"ataques_fera": Fixo(1)}, icone="fera"),
        _t("assassino", "Assassino", 4, 2, 1, "Abater um inimigo devolve metade do Foco e te deixa furtivo.",
           "sombra", mods={"furtivo_ao_abater": Fixo(1)}, gatilhos={"abate": _assassino}, icone="caveira"),
    ],
    "mago": [
        _t("mente_vasta", "Mente Vasta", 1, 0, 3, "+8 de Mana máxima por ponto.", stats={"max_rec": 8}, icone="livro"),
        _t("potencia_arcana", "Potência Arcana", 1, 1, 3, "+2 Poder por ponto.", stats={"poder": 2},
           icone="pocao_azul"),
        _t("canalizacao", "Canalização", 1, 2, 2, "+2 de Mana regenerada por turno, por ponto.",
           stats={"regen": 2}, icone="olho"),
        _t("brasas", "Brasas Eternas", 2, 0, 2, "Queimaduras causam +20% de dano por ponto e duram 1 turno a mais.",
           "piromante", mods={"queimadura_dano": bal.QUEIMADURA_BRASAS, "queimadura_turnos": Fixo(1)}, icone="chama"),
        _t("escudo_reflexo", "Escudo Rúnico", 2, 1, 1, "A Barreira Arcana absorve 30% a mais e dura 1 turno a mais.",
           mods={"barreira_turnos": 1}, mults={"barreira_mult": 1.3}, icone="escudo"),
        _t("pacto_sombrio", "Pacto Sombrio", 2, 2, 2, "Drenar Vida cura +10% e servos têm +15% de vida, por ponto.",
           "necromante", mods={"dreno_cura": 0.1, "servo_vida": 0.15}, icone="gota"),
        _t("ignicao", "Ignição", 3, 0, 1, "A Bola de Fogo sempre deixa o alvo em chamas.", "piromante",
           mods={"acender_garantido": Fixo(1)}, icone="chama"),
        _t("eficiencia", "Eficiência", 3, 1, 2, "Habilidades custam 10% menos por ponto.",
           mods={"custo_pct": 0.1}, icone="estrela"),
        _t("exercito", "Legião de Ossos", 3, 2, 1, "Você pode manter um servo a mais.", "necromante",
           mods={"servos_max": 1}, icone="caveira"),
        _t("coracao_ardente", "Coração Ardente", 4, 0, 1, "Inimigos mortos por fogo explodem, ferindo os outros.", "piromante",
           gatilhos={"abate": _coracao_ardente}, icone="chama"),
        _t("senhor_mortos", "Rei dos Mortos", 4, 2, 1, "O primeiro inimigo a cair em cada combate se ergue como "
                                                          "seu servo.", "necromante", gatilhos={"morte": _senhor_mortos},
           icone="caveira"),
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
    custo = HABILIDADES[hid]["custo"] + mod(jogador, f"custo:{hid}")
    custo *= 1 - mod(jogador, "custo_pct")
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
        nos.append({"id": t["id"], "nome": t["nome"], "icone": t["icone"], "desc": t["desc"], "camada": t["camada"],
                    "coluna": t["coluna"],
                    "rank": jogador.tal(t["id"]), "max": t["max"], "estado": est, "motivo": motivo(t, est),
                    "spec": SPECS[t["spec"]]["nome"] if t["spec"] else None})
    return {"classe": CLASSES[jogador.classe]["nome"], "pontos": jogador.pontos_talento, "nivel": jogador.nivel,
            "colunas": [SPECS[a]["nome"], CLASSES[jogador.classe]["nome"], SPECS[b]["nome"]], "spec": jogador.spec,
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
