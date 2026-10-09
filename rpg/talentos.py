"""Árvores de talentos.

Cada talento mora num **ramo** e numa **camada**. Os ramos: "base" (para todos, antes da especialização), "tronco"
(para todos, depois) e um por especialização (só ativável com ela). Cada camada exige um nível (NIVEL_CAMADA). Dentro
de um ramo e de uma camada cabem quantos talentos forem precisos, lado a lado, na ordem em que aparecem aqui: a árvore
não tem teto de camadas nem de colunas, e a tela se monta pelos dados. Pontos vêm de subir de nível e de derrotar
guardiões.

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
# Um gatilho que lembra algo durante a luta guarda em `cb.memoria`, pelo id do talento: o combate não tem campo
# para talento nenhum.
def uma_vez_por_luta(chave):
    """O gatilho age no máximo uma vez por luta: quando devolve True (agiu), fica quieto até a próxima."""
    def envolver(fn):
        def gatilho(cb, u, rank, d):
            if not cb.memoria.get(chave) and fn(cb, u, rank, d):
                cb.memoria[chave] = True
        return gatilho
    return envolver


def _aura_protecao(cb, u, rank, d):
    u.aplicar("barreira", 99, int(u.poder * 1.5))
    cb.dizer(f"Uma aura dourada te envolve. (barreira de {int(u.poder * 1.5)})", "amarelo")


def _armadilheiro(cb, u, rank, d):
    alvo = cb.rng.choice(cb.inimigos_vivos())
    cb.dizer(f"{alvo.nome} pisa numa das suas armadilhas!", "verde")
    cb.aplicar(alvo, "atordoado", 1, rotulo="preso na armadilha")
    cb.aplicar(alvo, "sangramento", 3, valor=max(2, u.atk * 0.3))


@uma_vez_por_luta("imortal")
def _imortal(cb, u, rank, d):
    d["dano"] = u.hp - 1
    u.aplicar("furia", 3, 0.5)
    cb.dizer("Um golpe que deveria te matar... mas você se recusa a cair! (Imortal)", "vermelho+negrito")
    return True


@uma_vez_por_luta("martirio")
def _martirio(cb, u, rank, d):
    if u.hp >= u.max_hp * 0.25:
        return False
    cura = u.curar(u.max_hp * 0.4)
    cb.curou(u, cura, rotulo="Martírio")
    cb.dizer(f"Seu sacrifício é visto. Uma luz desce e te restaura. (Martírio, +{cura} vida)", "amarelo+negrito")
    return True


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
    cargas = cb.memoria["frenesi"] = min(3, cb.memoria.get("frenesi", 0) + 1)
    u.aplicar("frenesi", 99, 0)
    u.efeitos["frenesi"]["v"] = 0.1 * rank * cargas  # o próprio estado, que só cresce: não mexe na Fúria nem no Grito
    cb.dizer(f"O sangue ferve: Frenesi x{cargas}!", "vermelho")


def _assassino(cb, u, rank, d):
    antes = u.rec
    u.rec = min(u.max_rec, u.rec + u.max_rec // 2)
    cb.recuperou(u, u.rec - antes)
    u.aplicar("furtivo", 2, 1)
    cb.dizer("Você some antes que o corpo toque o chão. (Assassino)", "magenta")


def _coracao_ardente(cb, u, rank, d):
    c = d["alvo"]
    if d["tipo"] == "fogo" and not cb.memoria.get("explodindo"):  # quem cai na explosão não explode de novo
        cb.memoria["explodindo"] = True
        cb.dizer(f"{c.nome} explode em chamas!", "vermelho+negrito")
        for outro in cb.inimigos_vivos():
            cb.atacar(u, outro, 0.6, tipo="fogo", alcance="distancia", stat="poder", pode_esquivar=False,
                      rotulo="Explosão")
        cb.memoria["explodindo"] = False


# A passiva de cada especialização: vem com ela, sem ponto de talento.
PASSIVAS = {
    "berserker": {"nome": "Pacto de Sangue", "desc": "Até +60% de dano quanto mais ferido você estiver.",
                  "mods": {"dano_ferido": 0.6}, "realce": "sangue"},
    "piromante": {"nome": "Chama Viva", "desc": f"Queimaduras causam {round((bal.QUEIMADURA_PIROMANTE - 1) * 100)}% a mais.",
                  "mults": {"queimadura_mult": bal.QUEIMADURA_PIROMANTE}},
    "necromante": {"nome": "Colheita", "desc": "Cada inimigo que cai devolve 5 de mana.",
                   "gatilhos": {"morte": _colheita}},
}

# O nível que cada camada pede. Camada nova: uma linha aqui (o validador cobra).
NIVEL_CAMADA = {1: 2, 2: 4, 3: 6, 4: 9}
RAMOS_COMUNS = ("base", "tronco")


def _t(id, nome, ramo, camada, maximo, desc, stats=None, mods=None, mults=None, gatilhos=None, ordem=50,
       icone="estrela", realce=None):
    """ramo: "base", "tronco" ou o id de uma especialização (o talento fica exclusivo dela).
    icone: o desenho do nó na árvore; realce: a cor do nome quando aparece num texto de regra (Realce, na tela)."""
    return {"id": id, "nome": nome, "ramo": ramo, "camada": camada, "max": maximo, "desc": desc,
            "spec": None if ramo in RAMOS_COMUNS else ramo, "stats": stats or {}, "mods": mods or {},
            "mults": mults or {}, "gatilhos": gatilhos or {}, "ordem": ordem, "icone": icone, "realce": realce}


TALENTOS = {
    "guerreiro": [
        _t("pele_ferro", "Pele de Ferro", "base", 1, 3, "+2 Defesa e +6 Vida por ponto.",
           stats={"defesa": 2, "max_hp": 6}, icone="escudo"),
        _t("golpe_brutal", "Golpe Brutal", "base", 1, 3, "+6% de dano corpo a corpo por ponto.",
           mods={"dano_corpo": 0.06}, icone="espada"),
        _t("folego", "Fôlego", "base", 1, 2, "+3 de Vigor regenerado por turno, por ponto.",
           stats={"regen": 3}, icone="coracao"),
        _t("luz_curativa", "Luz Curativa", "paladino", 2, 2, "Golpe Sagrado e Prece curam +25% por ponto.",
           mods={"cura_luz": 0.25}, icone="estrela"),
        _t("contra_ataque", "Contra-ataque", "tronco", 2, 2, "15% de chance por ponto de revidar golpes corpo a corpo.",
           mods={"contra_ataque": 0.15}, gatilhos={"golpe_recebido": _contra_ataque}, ordem=20, icone="espada"),
        _t("sede_insaciavel", "Sede Insaciável", "berserker", 2, 2, "Todo dano que você causa cura 5% dele, por ponto.",
           mods={"roubo_vida": 0.05}, icone="gota", realce="sangue"),
        _t("aura_protecao", "Aura de Proteção", "paladino", 3, 1, "Começa cada combate com uma barreira sagrada.",
           gatilhos={"inicio_combate": _aura_protecao}, icone="escudo"),
        _t("muralha", "Muralha", "tronco", 3, 1, "Erguer Escudo dura 1 turno a mais e custa 4 a menos.",
           mods={"escudo_turnos": 1, "custo:erguer_escudo": Fixo(-4)}, icone="escudo"),
        _t("frenesi", "Frenesi", "berserker", 3, 2,
           "Cada inimigo que você abate dá +10% de dano por ponto (acumula 3x).",
           gatilhos={"abate": _frenesi}, icone="chama"),
        _t("martirio", "Martírio", "paladino", 4, 1, "Uma vez por combate, ao cair abaixo de 25% de vida, cura 40%.",
           gatilhos={"golpe_recebido": _martirio}, ordem=10, icone="coracao"),
        _t("imortal", "Imortal", "berserker", 4, 1,
           "Uma vez por combate, sobrevive a um golpe fatal com 1 de vida e entra em fúria.",
           gatilhos={"golpe_fatal": _imortal}, icone="caveira"),
    ],
    "arqueiro": [
        _t("olho_aguia", "Olho de Águia", "base", 1, 3, "+4% de chance de crítico por ponto.",
           mods={"critico": 0.04}, icone="olho"),
        _t("pes_leves", "Pés Leves", "base", 1, 3, "+2 Agilidade por ponto.", stats={"agi": 2}, icone="folha"),
        _t("aljava_funda", "Aljava Funda", "base", 1, 2,
           "+15% de chance por ponto de recuperar flechas e +5 de espaço na aljava.",
           mods={"aljava": bal.ALJAVA_POR_TALENTO, "recolher_flecha": bal.RECOLHER_FLECHA_TALENTO}, icone="aljava"),
        _t("laco_animal", "Laço Animal", "patrulheiro", 2, 3, "Seu companheiro ganha +20% de vida e ataque por ponto.",
           mods={"laco_animal": 0.2}, icone="fera"),
        _t("tiro_abertura", "Tiro de Abertura", "tronco", 2, 1, "Seu primeiro ataque em cada combate é sempre crítico.",
           mods={"abertura": Fixo(1)}, icone="flecha"),
        _t("laminas_envenenadas", "Pontas Venenosas", "sombra", 2, 2,
           "Ataques básicos têm 20% de chance por ponto de envenenar.",
           mods={"veneno_basico": 0.2}, gatilhos={"ataque_basico": _laminas}, icone="gota"),
        _t("armadilheiro", "Armadilheiro", "patrulheiro", 3, 1,
           "Cada combate começa com um inimigo preso numa armadilha.",
           gatilhos={"inicio_combate": _armadilheiro}, icone="cadeado"),
        _t("mira_firme", "Mira Firme", "tronco", 3, 2, "+8% de dano à distância por ponto.",
           mods={"dano_distancia": 0.08}, icone="flecha"),
        _t("golpe_sombras", "Golpe Sombrio", "sombra", 3, 2, "Críticos causam +20% de dano por ponto.",
           mods={"mult_critico": 0.2}, icone="caveira"),
        _t("matilha", "Matilha", "patrulheiro", 4, 1, "Seu companheiro ataca duas vezes por turno.",
           mods={"ataques_fera": Fixo(1)}, icone="fera"),
        _t("assassino", "Assassino", "sombra", 4, 1, "Abater um inimigo devolve metade do Foco e te deixa furtivo.",
           mods={"furtivo_ao_abater": Fixo(1)}, gatilhos={"abate": _assassino}, icone="caveira"),
    ],
    "mago": [
        _t("mente_vasta", "Mente Vasta", "base", 1, 3, "+8 de Mana máxima por ponto.",
           stats={"max_rec": 8}, icone="livro"),
        _t("potencia_arcana", "Potência Arcana", "base", 1, 3, "+2 Poder por ponto.", stats={"poder": 2},
           icone="pocao_azul"),
        _t("canalizacao", "Canalização", "base", 1, 2, "+2 de Mana regenerada por turno, por ponto.",
           stats={"regen": 2}, icone="olho"),
        _t("brasas", "Brasas Eternas", "piromante", 2, 2,
           "Queimaduras causam +20% de dano por ponto e duram 1 turno a mais.",
           mods={"queimadura_dano": bal.QUEIMADURA_BRASAS, "queimadura_turnos": Fixo(1)}, icone="chama"),
        _t("escudo_reflexo", "Escudo Rúnico", "tronco", 2, 1,
           "A Barreira Arcana absorve 30% a mais e dura 1 turno a mais.",
           mods={"barreira_turnos": 1}, mults={"barreira_mult": 1.3}, icone="escudo"),
        _t("pacto_sombrio", "Pacto Sombrio", "necromante", 2, 2,
           "Drenar Vida cura +10% e servos têm +15% de vida, por ponto.",
           mods={"dreno_cura": 0.1, "servo_vida": 0.15}, icone="gota"),
        _t("ignicao", "Ignição", "piromante", 3, 1, "A Bola de Fogo sempre deixa o alvo em chamas.",
           mods={"acender_garantido": Fixo(1)}, icone="chama"),
        _t("eficiencia", "Eficiência", "tronco", 3, 2, "Habilidades custam 10% menos por ponto.",
           mods={"custo_pct": 0.1}, icone="estrela"),
        _t("exercito", "Legião de Ossos", "necromante", 3, 1, "Você pode manter um servo a mais.",
           mods={"servos_max": 1}, icone="caveira"),
        _t("coracao_ardente", "Coração Ardente", "piromante", 4, 1,
           "Inimigos mortos por fogo explodem, ferindo os outros.",
           gatilhos={"abate": _coracao_ardente}, icone="chama"),
        _t("senhor_mortos", "Rei dos Mortos", "necromante", 4, 1,
           "O primeiro inimigo a cair em cada combate se ergue como seu servo.",
           gatilhos={"morte": _senhor_mortos}, icone="caveira"),
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


def ramos(classe):
    """Os ramos da árvore na ordem da tela: as especializações dos lados, o tronco no meio (a base vai por cima)."""
    specs = list(CLASSES[classe]["specs"])
    meio = len(specs) // 2
    return specs[:meio] + ["tronco"] + specs[meio:]


def posicoes(classe):
    """(talento, posição) na ordem do catálogo: a posição é o lugar dele, lado a lado, no seu ramo e na sua camada."""
    contagem = {}
    for t in TALENTOS[classe]:
        chave = (t["ramo"], t["camada"])
        yield t, contagem.get(chave, 0)
        contagem[chave] = contagem.get(chave, 0) + 1


def _sobre_ramo(jogador, r):
    """O título e a situação de um ramo: o tronco é de todos; uma especialização é a sua, a escolher ou a outra."""
    if r == "tronco":
        return {"id": r, "nome": CLASSES[jogador.classe]["nome"], "sub": "para todos", "trancado": False}
    sub = (f"especialização no nível {bal.NIVEL_ESPECIALIZACAO}" if not jogador.spec else
           "sua especialização" if jogador.spec == r else "caminho não escolhido")
    return {"id": r, "nome": SPECS[r]["nome"], "sub": sub, "trancado": jogador.spec != r}


def dados_arvore(jogador):
    """A árvore em dados, para a interface gráfica desenhar: os ramos em ordem, o nível de cada camada usada e cada
    nó com ramo, camada e posição (a tela monta a grade com isso, de qualquer tamanho)."""
    nos = []
    for t, pos in posicoes(jogador.classe):
        est = estado(jogador, t)
        nos.append({"id": t["id"], "nome": t["nome"], "icone": t["icone"], "desc": t["desc"], "ramo": t["ramo"],
                    "camada": t["camada"], "pos": pos, "rank": jogador.tal(t["id"]), "max": t["max"], "estado": est,
                    "motivo": motivo(t, est), "spec": SPECS[t["spec"]]["nome"] if t["spec"] else None})
    camadas = sorted({n["camada"] for n in nos})
    return {"classe": CLASSES[jogador.classe]["nome"], "pontos": jogador.pontos_talento, "nivel": jogador.nivel,
            "spec": jogador.spec, "ramos": [_sobre_ramo(jogador, r) for r in ramos(jogador.classe)],
            "camadas": {str(k): NIVEL_CAMADA[k] for k in camadas}, "nos": nos}


def desenhar(jogador, largura=76):
    """Linhas (pedaços texto/cor) com a árvore: uma coluna por ramo, a base espalhada por cima. Quando um ramo tem
    mais de um talento na mesma camada, a camada ganha mais linhas."""
    rs = ramos(jogador.classe)
    col = (largura - 8) // len(rs)
    cores = {"comprado": "verde+negrito", "disponivel": "amarelo", "nivel": "cinza", "spec": "cinza",
             "bloqueado": "cinza"}
    titulos = ["TRONCO COMUM" if r == "tronco" else ("← " if i < rs.index("tronco") else "") + SPECS[r]["nome"].upper()
               + (" →" if i > rs.index("tronco") else "") for i, r in enumerate(rs)]
    linhas = [[("        ", None)] + [(t.center(col), "ciano+negrito") for t in titulos]]

    def caixa(t):
        if not t:
            return ("·".center(col), "cinza")
        est = estado(jogador, t)
        marca = "✓" if est == "comprado" else ("✗" if est == "bloqueado" else "")
        texto = f"{t['nome'][:col - 6]} {jogador.tal(t['id'])}/{t['max']}{marca}"
        return (f"[{texto}]".center(col), cores[est])

    lista = list(posicoes(jogador.classe))
    camadas = sorted({t["camada"] for t, _ in lista})
    for k, camada in enumerate(camadas):
        # Cada fileira de texto mostra um talento por coluna: os da base se espalham pelas colunas na ordem; os de um
        # ramo ficam na coluna dele, um embaixo do outro.
        base = [t for t, _ in lista if t["camada"] == camada and t["ramo"] == "base"]
        por_ramo = {r: [t for t, _ in lista if t["camada"] == camada and t["ramo"] == r] for r in rs}
        fileiras = [base[i:i + len(rs)] + [None] * (len(rs) - len(base[i:i + len(rs)]))
                    for i in range(0, len(base), len(rs))]
        altura = max((len(v) for v in por_ramo.values()), default=0)
        fileiras += [[por_ramo[r][i] if i < len(por_ramo[r]) else None for r in rs] for i in range(altura)]
        for i, fileira in enumerate(fileiras or [[None] * len(rs)]):
            rotulo = (f"Nv.{NIVEL_CAMADA[camada]:<2}   ", "cinza") if i == 0 else ("        ", None)
            linhas.append([rotulo] + [caixa(t) for t in fileira])
        if k < len(camadas) - 1:
            linhas.append([("        ", None)] + [("│".center(col), "cinza") for _ in rs])
    return linhas
