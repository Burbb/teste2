"""Sobrevivência: fome, ferimentos, infecção e escuridão.

Num mundo de fantasia de verdade, o que mata não são só os monstros: é a
fome, a ferida que infecciona, a noite sem luz. Este módulo cuida disso.
"""

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


def multiplicadores(jogador):
    """Penalidades de ferimentos e fome sobre os atributos."""
    mult = {}
    for f in jogador.ferimentos:
        for stat, v in FERIMENTOS[f["id"]]["mult"].items():
            mult[stat] = mult.get(stat, 1.0) * v
    if jogador.fome:
        for stat in ("atk", "poder", "max_hp"):
            mult[stat] = mult.get(stat, 1.0) * (0.9 if jogador.fome < 3 else 0.8)
    return mult


def tem(jogador, fid):
    return any(f["id"] == fid for f in jogador.ferimentos)


def ferir(g, fid, motivo=""):
    """Aplica (ou agrava) um ferimento duradouro."""
    j = g.j
    d = FERIMENTOS[fid]
    existente = next((f for f in j.ferimentos if f["id"] == fid), None)
    if existente:
        if d["dias"]:
            existente["dias"] += d["dias"] // 2
        existente["tratado"] = False
        g.dizer(f"Seu ferimento piora: {d['nome']}!{motivo}", "vermelho+negrito")
    else:
        j.ferimentos.append({"id": fid, "dias": d["dias"], "tratado": False})
        g.dizer(f"FERIMENTO: {d['nome']}{motivo}. "
                + ("Precisa ser tratado com bandagem ou pode infeccionar." if d.get("aberto") else
                   "Só o tempo ou um curandeiro resolvem."), "vermelho+negrito")
    antes_hp = j.hp
    j.recalcular()
    j.hp = min(antes_hp, j.max_hp)


def talvez_ferir(g, dano, tipo, critico, atacante):
    """Chamado quando o herói leva um golpe. Golpes pesados deixam marcas."""
    j = g.j
    if not j.vivo or dano <= 0:
        return
    gravidade = dano / max(1, j.max_hp)
    chance = max(0.0, (gravidade - 0.15) * 1.4) + (0.12 if critico else 0) + (0.1 if j.hp < j.max_hp * 0.25 else 0)
    if g.rng.random() >= min(0.55, chance):
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


def amanhecer(g, descanso):
    """Processa a passagem de um dia. descanso: 0 (nenhum), 1 (acampamento), 2 (cama)."""
    j = g.j
    # Comida
    if j.provisoes > 0:
        j.provisoes -= 1
        if j.fome:
            g.dizer("Você finalmente come. As mãos param de tremer.", "verde")
        j.fome = 0
    else:
        j.fome += 1
        if j.fome == 1:
            g.dizer("Sem provisões. Você vai dormir com fome. (-10% força e vida, não se recupera dormindo)",
                    "vermelho")
        elif j.fome < 3:
            g.dizer(f"Dia {j.fome} sem comer. Seu estômago dói o tempo todo.", "vermelho")
        else:
            perda = max(2, int(j.max_hp * 0.12))
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
