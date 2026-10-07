"""Sobrevivência: fome, ferimentos, infecção e escuridão.

Num mundo de fantasia de verdade, o que mata não são só os monstros: é a
fome, a ferida que infecciona, a noite sem luz. Este módulo cuida disso.
"""

from . import balanceamento as bal

FERIMENTOS = {
    "corte": dict(nome="Corte profundo", dias=4, mult={"max_hp": 0.9}, aberto=True),
    "mordida": dict(nome="Mordida dilacerada", dias=4, mult={"max_hp": 0.9, "agi": 0.9}, aberto=True),
    "costelas": dict(nome="Costelas quebradas", dias=8, mult={"defesa": 0.75, "max_rec": 0.85}),
    "braco": dict(nome="Braço fraturado", dias=8, mult={"atk": 0.75, "poder": 0.9}),
    "perna": dict(nome="Perna torcida", dias=5, mult={"agi": 0.7}),
    "concussao": dict(nome="Concussão", dias=3, mult={"poder": 0.75, "max_rec": 0.85}),
    "queimadura": dict(nome="Queimadura grave", dias=5, mult={"max_hp": 0.88}, aberto=True),
    "infeccao": dict(nome="INFECÇÃO", dias=None, mult={"atk": 0.85, "poder": 0.85, "agi": 0.85}),
}
MAX_PROVISOES = 12
CHANCE_INFECCAO = 0.3


def penalidades(fid, recurso=None):
    """'−25% Ataque, −10% Poder': o que o ferimento tira de você."""
    from .entidades import nome_stat
    return ", ".join(f"−{round((1 - v) * 100)}% {nome_stat(stat, recurso)}" for stat, v in FERIMENTOS[fid]["mult"].items())


def explicar(f, recurso=None):
    """As linhas que explicam um ferimento do herói: o que ele tira, como sara e o perigo que corre."""
    d = FERIMENTOS[f["id"]]
    linhas = [penalidades(f["id"], recurso) + "."]
    if f["id"] == "infeccao":
        linhas += ["Arde em febre: perde 12% da vida a cada amanhecer.",
                   "Não passa sozinha: use um unguento ou pague um curandeiro."]
        return linhas
    if d.get("aberto") and not f.get("tratado"):
        linhas.append(f"Ferida aberta: uma bandagem trata. Sem tratar, {round(CHANCE_INFECCAO * 100)}% de chance de "
                      "infeccionar a cada noite.")
    linhas.append(f"Sara em {f['dias']} dia{'s' if f['dias'] != 1 else ''} de descanso (dormir numa cama conta dobrado; "
                  "com fome não sara). Um curandeiro resolve na hora.")
    return linhas


def multiplicadores(jogador):
    """Penalidades de ferimentos e fome sobre os atributos."""
    mult = {}
    for stat, fontes in fontes_penalidade(jogador).items():
        for _, v in fontes:
            mult[stat] = mult.get(stat, 1.0) * v
    return mult


def fontes_penalidade(jogador):
    """De onde vem cada penalidade, na ordem em que entram na conta: {atributo: [(nome, fator), ...]}."""
    fontes = {}
    for f in jogador.ferimentos:
        for stat, v in FERIMENTOS[f["id"]]["mult"].items():
            fontes.setdefault(stat, []).append((FERIMENTOS[f["id"]]["nome"], v))
    if jogador.fome:
        fator = {1: 0.9, 2: 0.8}.get(jogador.fome, 0.65)
        for stat in ("atk", "poder", "max_hp", "agi"):
            fontes.setdefault(stat, []).append(("Fome", fator))
    return fontes


def tem(jogador, fid):
    return any(f["id"] == fid for f in jogador.ferimentos)


def ferir(g, fid, motivo=""):
    """Aplica (ou agrava) um ferimento duradouro."""
    from .telemetria import registrar
    j = g.j
    d = FERIMENTOS[fid]
    registrar(g, "ferimento", id=fid)
    existente = next((f for f in j.ferimentos if f["id"] == fid), None)
    if existente:
        if d["dias"]:
            existente["dias"] += d["dias"] // 2
        existente["tratado"] = False
        g.ui.efeito(f"Ferimento piora: {d['nome']}{motivo}", "ferimento")
    else:
        j.ferimentos.append({"id": fid, "dias": d["dias"], "tratado": False})
        g.ui.efeito(f"FERIMENTO: {d['nome']}{motivo} ({penalidades(fid, j.nome_recurso)}) — "
                    + ("trate com bandagem ou pode infeccionar" if d.get("aberto") else
                       "só o tempo ou um curandeiro resolvem"), "ferimento")
    antes_hp = j.hp
    j.recalcular()
    j.hp = min(antes_hp, j.max_hp)


def talvez_ferir(g, dano, tipo, critico, atacante):
    """Chamado quando o herói leva um golpe. Golpes pesados deixam marcas."""
    j = g.j
    if not j.vivo or dano <= 0:
        return
    gravidade = dano / max(1, j.max_hp)
    chance = (bal.FERIMENTO_BASE + gravidade * bal.FERIMENTO_GRAVIDADE + (bal.FERIMENTO_CRITICO if critico else 0)
              + (bal.FERIMENTO_POUCA_VIDA if j.hp < j.max_hp * 0.25 else 0))
    if g.rng.random() >= min(bal.FERIMENTO_TETO, chance):
        return
    if tipo == "fogo":
        fid = "queimadura"
    elif tipo in ("sombra", "arcano", "gelo"):
        fid = g.rng.choice(["concussao", "costelas"])
    elif "fera" in getattr(atacante, "tracos", []) or "demonio" in getattr(atacante, "tracos", []):
        fid = g.rng.choice(["mordida", "mordida", "perna", "braco"])
    else:
        fid = g.rng.choice(["corte", "corte", "costelas", "braco", "perna", "concussao"])
    ferir(g, fid)


# O que cada tipo de acidente costuma causar (dano de eventos, fora do combate).
FERIMENTOS_POR_MOTIVO = (
    (("queda", "avalanche", "desliz", "escorreg"), ("perna", "braco", "costelas")),
    (("armadilha", "espinho", "lâmina", "lamina", "vidro"), ("corte", "perna")),
    (("queimadura", "fogo", "chama", "brasa"), ("queimadura",)),
    (("mordida", "ferroada", "picada"), ("mordida",)),
    (("soco", "briga", "pancada", "pedra"), ("concussao", "costelas")),
)


def ferir_por_evento(g, dano, motivo=""):
    """Dano de cenário (queda, armadilha, briga) também pode deixar um ferimento que combina com o acidente."""
    j = g.j
    if not j.vivo or dano <= 0:
        return
    if g.rng.random() >= (dano / max(1, j.max_hp)) * bal.FERIMENTO_EVENTO:
        return
    texto = motivo.lower()
    opcoes = next((ids for chaves, ids in FERIMENTOS_POR_MOTIVO if any(k in texto for k in chaves)),
                  ("corte", "costelas", "concussao", "perna"))
    ferir(g, g.rng.choice(opcoes))


def tratar_com_bandagem(g):
    """Trata o primeiro ferimento aberto não tratado. Devolve True se tratou algo."""
    j = g.j
    for f in j.ferimentos:
        if FERIMENTOS[f["id"]].get("aberto") and not f["tratado"]:
            f["tratado"] = True
            g.dizer(f"Você limpa e enfaixa: {FERIMENTOS[f['id']]['nome']}. Não deve infeccionar.", "verde")
            return True
    return False


def curar_ferimento(g, fid):
    g.j.ferimentos = [f for f in g.j.ferimentos if f["id"] != fid]
    antes = g.j.max_hp
    g.j.recalcular()
    g.j.hp += max(0, g.j.max_hp - antes)


def descrever(jogador):
    partes = []
    for f in jogador.ferimentos:
        d = FERIMENTOS[f["id"]]
        txt = d["nome"]
        if d["dias"]:
            txt += f" ({f['dias']}d" + (", tratado" if f["tratado"] or not d.get("aberto") else ", ABERTO") + ")"
        partes.append(txt)
    if jogador.fome:
        partes.append("FAMINTO" if jogador.fome < 3 else "MORRENDO DE FOME")
    return partes


def amanhecer(g, descanso, refeicao=False):
    """Processa a passagem de um dia. descanso: 0 (nenhum), 1 (acampamento), 2 (cama).
    refeicao: alguém já serviu a comida do dia (a taverna); as provisões ficam intactas."""
    j = g.j
    # Comida
    if refeicao:
        if j.fome:
            g.dizer("Você finalmente come. As mãos param de tremer.", "verde")
        j.fome = 0
    elif j.provisoes > 0:
        j.provisoes -= 1
        if j.fome:
            g.dizer("Você finalmente come. As mãos param de tremer.", "verde")
        j.fome = 0
    else:
        j.fome += 1
        if j.fome == 1:
            g.dizer("Sem provisões. Você vai dormir com fome. (-10% atributos, quase não se recupera dormindo)",
                    "vermelho")
        elif j.fome < 3:
            g.dizer(f"Dia {j.fome} sem comer. Suas mãos tremem e a vista escurece. (-20% atributos)", "vermelho")
        else:
            perda = max(3, int(j.max_hp * 0.2))
            g.dizer(f"Dia {j.fome} sem comer. Seu corpo começa a se consumir. (-{perda} vida)", "vermelho+negrito")
            j.hp -= perda
            if j.hp <= 0:
                j.hp = 0
                g.fim_de_jogo("Você morreu de fome, sozinho, longe de qualquer lugar que pudesse chamar de casa.")
    if j.provisoes in (1, 2) and not j.fome:
        g.dizer(f"Restam só {j.provisoes} dia(s) de provisões.", "amarelo")

    # Ferimentos
    for f in list(j.ferimentos):
        d = FERIMENTOS[f["id"]]
        if f["id"] == "infeccao":
            perda = max(3, int(j.max_hp * 0.12))
            j.hp -= perda
            g.dizer(f"A infecção arde em febre. (-{perda} vida) Procure um curandeiro ou use um unguento!",
                    "vermelho+negrito")
            if j.hp <= 0:
                j.hp = 0
                g.fim_de_jogo("A ferida apodreceu. A febre veio, depois os delírios, depois o silêncio. "
                              "A infecção te levou.")
            continue
        if d.get("aberto") and not f["tratado"] and g.rng.random() < CHANCE_INFECCAO:
            g.dizer(f"Seu {d['nome'].lower()} está vermelho, quente e cheira mal.", "vermelho+negrito")
            if not tem(j, "infeccao"):
                j.ferimentos.append({"id": "infeccao", "dias": None, "tratado": False})
            f["tratado"] = True  # a ferida em si segue curando; o problema agora é a infecção
        if descanso and j.fome == 0:
            f["dias"] -= descanso
        if f["dias"] is not None and f["dias"] <= 0:
            j.ferimentos.remove(f)
            g.dizer(f"{d['nome']}: curado.", "verde")
    antes = j.max_hp
    j.recalcular()
    if j.max_hp > antes:
        j.hp = min(j.max_hp, j.hp)


def escuro(g):
    """Ruínas e a Cidadela são sempre escuras; o resto, só à noite."""
    return g.noite or g.bioma in ("ruinas", "cidadela")


def acender_tocha(g):
    """Antes de agir no escuro. Devolve True se há luz."""
    if not escuro(g):
        g.sem_luz = False
        return True
    if g.j.tem("tocha"):
        g.j.consumiveis["tocha"] -= 1
        g.dizer(f"Você acende uma tocha. (restam {g.j.consumiveis['tocha']})", "amarelo")
        g.sem_luz = False
        return True
    g.dizer("Sem tocha, você avança às cegas. (percepção e destreza -4, emboscadas mais prováveis)", "vermelho")
    g.sem_luz = True
    return False
