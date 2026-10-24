"""Sobrevivência: fome, ferimentos, infecção e escuridão.

Num mundo de fantasia de verdade, o que mata não são só os monstros: é a
fome, a ferida que infecciona, a noite sem luz. Este módulo cuida disso.
"""

from . import balanceamento as bal
from . import texto as tx

FERIMENTOS = {
    "corte": dict(nome="Corte profundo", curto="o corte", dias=4, mult={"max_hp": 0.9}, aberto=True),
    "mordida": dict(nome="Mordida dilacerada", curto="a mordida", dias=4, mult={"max_hp": 0.9, "agi": 0.9}, aberto=True),
    "costelas": dict(nome="Costelas quebradas", curto="as costelas", dias=8, mult={"defesa": 0.75, "max_rec": 0.85}),
    "braco": dict(nome="Braço fraturado", curto="o braço", dias=8, mult={"atk": 0.75, "poder": 0.9}),
    "perna": dict(nome="Perna torcida", curto="a perna", dias=5, mult={"agi": 0.7}),
    "concussao": dict(nome="Concussão", curto="a concussão", dias=3, mult={"poder": 0.75, "max_rec": 0.85}),
    "queimadura": dict(nome="Queimadura grave", curto="a queimadura", dias=5, mult={"max_hp": 0.88}, aberto=True),
    "infeccao": dict(nome="Infecção", curto="a infecção", dias=None, mult={"atk": 0.85, "poder": 0.85, "agi": 0.85}),
}
MAX_PROVISOES = 12
FOME_FATOR = {1: 0.9, 2: 0.8}   # atributos e vida máxima com fome (1º e 2º dia); do 3º em diante, FOME_GRAVE
FOME_GRAVE = 0.65
FOME_DESCANSO = 0.3             # com fome, descansar devolve esta parte da vida
CHANCE_INFECCAO = 0.3


def penalidades(fid, recurso=None):
    """'−25% Ataque, −10% Poder': o que o ferimento tira de você."""
    from .entidades import nome_stat
    return ", ".join(f"−{round((1 - v) * 100)}% {nome_stat(stat, recurso)}" for stat, v in FERIMENTOS[fid]["mult"].items())


def efeito_no_heroi(jogador, fid):
    """O que o ferimento faz nos números DESTE herói (atributos são inteiros: −15% de um Poder 1 não chega a
    tirar nada). Ex.: "No seu herói: Ataque 11 → 9. Poder 1 e Agilidade 3: baixos demais para cair." """
    from .entidades import nome_stat
    totais, _ = jogador.totais()
    caem, ficam = [], []
    for stat, v in FERIMENTOS[fid]["mult"].items():
        normal = max(1, int(round(totais[stat])))
        com = max(1, int(round(totais[stat] * v)))
        (caem if com < normal else ficam).append((nome_stat(stat, jogador.nome_recurso), normal, com))
    partes = [f"{n} {a} → {b}" for n, a, b in caem]
    if ficam:
        nomes = " e ".join(", ".join(f"{n} {a}" for n, a, _ in ficam).rsplit(", ", 1))
        partes.append(f"{nomes}: {'baixo' if len(ficam) == 1 else 'baixos'} demais para cair")
    return "No seu herói: " + ". ".join(partes) + "."


def explicar(f, recurso=None, jogador=None):
    """As linhas que explicam um ferimento do herói: o que ele tira (e, com o herói, o que isso dá nos números
    dele), como sara e o perigo que corre."""
    d = FERIMENTOS[f["id"]]
    linhas = [penalidades(f["id"], recurso) + "."]
    if jogador is not None:
        linhas.append(efeito_no_heroi(jogador, f["id"]))
    if f["id"] == "infeccao":
        linhas += ["Arde em febre: perde 12% da vida a cada amanhecer.",
                   "Não sara sozinha: use um unguento ou vá à Curandeira."]
        return linhas
    if d.get("aberto") and not f.get("tratado"):
        linhas.append(f"Ferida aberta: sem bandagem, {round(CHANCE_INFECCAO * 100)}% de chance de infeccionar a cada "
                      "noite.")
    linhas.append(f"Sara em {f['dias']} dia{'s' if f['dias'] != 1 else ''} de descanso (a cama conta dobrado; com fome "
                  "não sara). A Curandeira trata na hora.")
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
        fator = FOME_FATOR.get(jogador.fome, FOME_GRAVE)
        for stat in ("atk", "poder", "max_hp", "agi"):
            fontes.setdefault(stat, []).append(("Fome", fator))
    return fontes


def vida_bloqueio(jogador):
    """A vida máxima que as penalidades (ferimentos e fome) tiram agora, para a tela mostrar a barra inteira: o que o
    herói teria saudável (base, talentos e equipamento: Jogador.totais), o limite de agora (max_hp, com os fatores
    multiplicados e arredondados como em recalcular) e de onde vem cada parte, na ordem da conta. A perda de cada fonte
    é a diferença que ela faz naquela ordem; a última absorve o arredondamento final, e a soma fecha com saudável −
    limite. None sem bloqueio. Só lê: nada aqui muda a vida nem os atributos."""
    totais, _ = jogador.totais()
    saudavel = max(1, int(round(totais["max_hp"])))
    if jogador.max_hp >= saudavel:
        return None
    fontes, valor = [], float(totais["max_hp"])
    for nome, fator in fontes_penalidade(jogador).get("max_hp", []):
        depois = valor * fator
        fontes.append({"nome": nome, "pct": round((1 - fator) * 100), "perda": round(valor) - round(depois)})
        valor = depois
    if fontes:
        fontes[-1]["perda"] += (saudavel - jogador.max_hp) - sum(f["perda"] for f in fontes)
    bloqueado = saudavel - jogador.max_hp
    # o que devolve cada parte (as regras de hoje: o ferimento sara com descanso ou na Curandeira, que devolve a parte
    # dele também como vida; a bandagem só evita a infecção; a fome passa comendo)
    devolve = []
    if any(f["nome"] != "Fome" for f in fontes):
        devolve.append("A parte de um ferimento volta quando ele sara (descanso ou Curandeira); a bandagem não "
                       "devolve.")
    if any(f["nome"] == "Fome" for f in fontes):
        devolve.append("A da fome volta quando você come.")
    return {"saudavel": saudavel, "limite": jogador.max_hp, "bloqueado": bloqueado, "fontes": fontes,
            "causas": tx.lista_natural([f["nome"] if f["nome"] != "Fome" else "a fome" for f in fontes]),
            "dica": [f"Curas param em {jogador.max_hp}.",
                     f"Saudável: {saudavel}. {' '.join(devolve)}"]}


def tem(jogador, fid):
    return any(f["id"] == fid for f in jogador.ferimentos)


def condicoes(j):
    """As condições do herói fora das barras (a área embaixo da vida e do recurso): hoje, a fome, com o efeito de
    agora na dica. Lista vazia sem nenhuma."""
    if not j.fome:
        return []
    pct = round((1 - FOME_FATOR.get(j.fome, FOME_GRAVE)) * 100)
    dica = [f"Ataque, Poder, Agilidade e vida máxima −{pct}%.",
            f"Descansar devolve só {round(FOME_DESCANSO * 100)}% da vida de sempre, e os ferimentos não saram."]
    if j.fome >= 3:
        dica.append(f"Cada amanhecer sem comer tira {perda_fome(j)} de vida.")
    elif j.fome == 2:  # o próximo amanhecer sem comer é o terceiro: aí o corpo começa a se consumir
        dica.append("Mais um amanhecer sem comer e o corpo começa a se consumir: perde vida a cada dia.")
    dica.append("Passa quando você come: 1 provisão no amanhecer, o ensopado da taverna ou comida comprada.")
    return [{"id": "fome", "icone": "osso_diag", "texto": "Com fome" if j.fome < 3 else "Morrendo de fome",
             "grave": j.fome >= 3, "dica": dica}]


def perda_fome(j):
    """A vida que cada amanhecer sem comer tira, do terceiro dia em diante."""
    return max(3, int(j.max_hp * 0.2))


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
                    + ("enfaixe com bandagem ou pode infeccionar" if d.get("aberto") else
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
    if gravidade < bal.FERIMENTO_LIMIAR and not critico:
        return  # arranhão: dói, mas não marca
    chance = (bal.FERIMENTO_BASE + max(0.0, gravidade - bal.FERIMENTO_LIMIAR) * bal.FERIMENTO_GRAVIDADE
              + (bal.FERIMENTO_CRITICO if critico else 0) + (bal.FERIMENTO_POUCA_VIDA if j.hp < j.max_hp * 0.25 else 0))
    chance = min(bal.FERIMENTO_TETO, chance) * bal.FERIMENTO_POR_FERIDA ** len(j.ferimentos)
    if g.rng.random() >= chance:
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


def ferida_para_bandagem(j):
    """A ferida que uma bandagem enfaixaria agora: a primeira aberta (corte, mordida, queimadura) ainda sem tratar.
    Fratura, perna torcida, concussão e infecção não se enfaixam."""
    return next((f for f in j.ferimentos if FERIMENTOS[f["id"]].get("aberto") and not f["tratado"]), None)


def tratar_com_bandagem(g):
    """Enfaixa a primeira ferida aberta não tratada: ela fica protegida contra infecção e segue sarando no tempo dela
    (a penalidade fica até sarar). Devolve True se enfaixou algo."""
    f = ferida_para_bandagem(g.j)
    if not f:
        return False
    f["tratado"] = True
    g.dizer(f"Você limpa e enfaixa: {FERIMENTOS[f['id']]['nome']}. Não deve infeccionar.", "verde")
    return True


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
            txt += f" ({f['dias']}d" + (", tratado" if f["tratado"] or not d.get("aberto") else ", aberto") + ")"
        partes.append(txt)
    if jogador.fome:
        partes.append("Faminto" if jogador.fome < 3 else "Morrendo de fome")
    return partes


def amanhecer(g, descanso, refeicao=False):
    """Processa a passagem de um dia. descanso: 0 (nenhum), 1 (acampamento), 2 (cama).
    refeicao: alguém já serviu a comida do dia (a taverna); as provisões ficam intactas."""
    j = g.j
    # Comida
    if refeicao:
        if j.fome:
            g.relatar("Você finalmente come. As mãos param de tremer.", "verde", "bom", "pernil", "A fome passou")
        j.fome = 0
    elif j.provisoes > 0:
        j.provisoes -= 1
        if j.fome:
            g.relatar("Você finalmente come. As mãos param de tremer.", "verde", "bom", "pernil", "A fome passou")
        j.fome = 0
    else:
        j.fome += 1
        if j.fome == 1:
            g.relatar("Sem provisões. Você vai dormir com fome. (-10% atributos, quase não se recupera dormindo)",
                      "vermelho", "perigo", "pernil", "Com fome: −10% atributos")
        elif j.fome < 3:
            g.relatar(f"Dia {j.fome} sem comer. Suas mãos tremem e a vista escurece. (-20% atributos)", "vermelho",
                      "perigo", "pernil", f"{j.fome}º dia sem comer: −20% atributos")
        else:
            perda = perda_fome(j)
            g.relatar(f"Dia {j.fome} sem comer. Seu corpo começa a se consumir. (-{perda} vida)", "vermelho+negrito",
                      "perigo", "caveira", f"{j.fome}º dia sem comer: −{perda} vida")
            j.hp -= perda
            if j.hp <= 0:
                j.hp = 0
                g.cair_sem_luta("fome", "Você morreu de fome, sozinho, longe de qualquer lugar que pudesse chamar de "
                                        "casa.")
    if j.provisoes in (1, 2) and not j.fome:
        g.relatar(f"{'Resta' if j.provisoes == 1 else 'Restam'} só {tx.plural(j.provisoes, 'dia')} de provisões.",
                  "amarelo", "aviso", "pernil", quadro=False)  # no quadro, o ícone das provisões já diz quantas restam

    # Ferimentos
    for f in list(j.ferimentos):
        d = FERIMENTOS[f["id"]]
        if f["id"] == "infeccao":
            perda = max(3, int(j.max_hp * 0.12))
            j.hp -= perda
            g.relatar(f"A infecção arde em febre. (-{perda} vida) Procure um curandeiro ou use um unguento!",
                      "vermelho+negrito", "perigo", "gota", f"Febre da infecção: −{perda} vida")
            if j.hp <= 0:
                j.hp = 0
                g.cair_sem_luta("infeccao", "A ferida apodreceu. A febre veio, depois os delírios, depois o "
                                            "silêncio. A infecção te levou.")
            continue
        if d.get("aberto") and not f["tratado"] and g.rng.random() < CHANCE_INFECCAO:
            g.relatar(f"Seu {d['nome'].lower()} está vermelho, quente e cheira mal.", "vermelho+negrito", "perigo",
                      "gota", f"{d['nome']} infeccionou")
            if not tem(j, "infeccao"):
                j.ferimentos.append({"id": "infeccao", "dias": None, "tratado": False})
            f["tratado"] = True  # a ferida em si segue curando; o problema agora é a infecção
        if descanso and j.fome == 0:
            f["dias"] -= descanso
        if f["dias"] is not None and f["dias"] <= 0:
            j.ferimentos.remove(f)
            g.relatar(f"{d['nome']}: curado.", "verde", "bom", "bandagem", f"{d['nome']}: curado")
    antes = j.max_hp
    j.recalcular()
    if j.max_hp > antes:
        j.hp = min(j.max_hp, j.hp)


def escuro(g):
    """Ruínas e a Cidadela são sempre escuras; o resto, só à noite."""
    return g.noite or g.bioma in ("ruinas", "cidadela")


def acender_tocha(g, sala=False):
    """Antes de agir no escuro. Devolve True se há luz. sala: a luta de uma sala escura (a capela), que sem luz começa
    sempre com o inimigo atacando primeiro; fora dela, o escuro só torna a emboscada mais provável (Percepção pior)."""
    if not escuro(g):
        g.sem_luz = False
        return True
    if g.j.tem("tocha"):
        g.j.consumiveis["tocha"] -= 1
        g.dizer(f"Você acende uma tocha. (restam {g.j.consumiveis['tocha']})", "amarelo")
        g.sem_luz = False
        return True
    if sala:
        g.dizer(f"Sem tocha, você entra às cegas: o inimigo mais rápido ataca antes de você. (Percepção e Destreza "
                f"−{bal.ESCURO_TESTES})", "vermelho")
    else:
        g.dizer(f"Sem tocha, você avança às cegas. (Percepção e Destreza −{bal.ESCURO_TESTES}, emboscadas mais "
                "prováveis)", "vermelho")
    g.sem_luz = True
    return False


def _noite(guardiao=False):
    """O que a noite muda numa luta, do balanceamento: o nível (não nos guardiões) e o dano de todos os inimigos."""
    dano = round((bal.NOITE_INIMIGOS - 1) * 100)
    return f"+{dano}% de dano dos inimigos" if guardiao else f"inimigos +{bal.NOITE_NIVEL} nível e +{dano}% de dano"


def riscos_sala(g, guardiao=False):
    """Os riscos da luta de uma sala escura (as da capela), junto da ação, antes de entrar: indicadores curtos (ícone,
    texto, tipo para a cor, dica com o detalhe e `linha` para a interface de texto). A tocha que ela gasta, ou, sem
    tocha, o inimigo que age primeiro; e o que a noite muda (num guardião, só o dano). Lista vazia se nada vale."""
    r = []
    dano = round((bal.NOITE_INIMIGOS - 1) * 100)
    if escuro(g):
        n = g.j.consumiveis.get("tocha", 0)
        if n:
            r.append({"icone": "tocha", "texto": "−1 tocha", "tipo": "custo", "linha": f"Gasta 1 tocha (você tem {n}).",
                      "dica": f"A sala é escura de dia e de noite: entrar acende 1 tocha (você tem {n})."})
        else:
            r.append({"icone": "tocha_apagada", "texto": "Sem luz: inimigo age primeiro", "tipo": "perigo",
                      "linha": "Sem tocha: o inimigo mais rápido ataca primeiro.",
                      "dica": "Sem tocha, o inimigo mais rápido ataca antes de você, e Percepção e Destreza ficam "
                              f"−{bal.ESCURO_TESTES}."})
    if g.noite:
        if guardiao:
            r.append({"icone": "lua", "texto": f"+{dano}% dano", "tipo": "noite", "linha": f"Noite: {_noite(True)}.",
                      "dica": f"Noite: a guardiã causa {dano}% mais dano (o nível dela não muda à noite)."})
        else:
            r.append({"icone": "lua", "texto": f"+{bal.NOITE_NIVEL} nível · +{dano}% dano", "tipo": "noite",
                      "linha": f"Noite: {_noite()}.",
                      "dica": f"Noite: os inimigos da sala vêm {bal.NOITE_NIVEL} nível acima e causam {dano}% mais dano."})
    return r


def nota_sala(g, guardiao=False):
    """Os riscos da sala numa frase (a interface de texto, os testes). None se nada vale."""
    return " ".join(r["linha"] for r in riscos_sala(g, guardiao)) or None


def riscos_do_lugar(g, salas=False):
    """Fora da vila, o que a hora e a luz mudam aqui, em linhas curtas (o cabeçalho e o painel do lugar), ao lado do
    nível-base da região, que continua o mesmo. salas: o lugar tem lutas de sala (a capela)."""
    if g.loc["tipo"] == "vila":
        return []
    r = []
    if g.noite:
        r.append({"icone": "lua", "texto": f"Noite: {_noite()}", "tipo": "noite"})
    if escuro(g):
        n = g.j.consumiveis.get("tocha", 0)
        onde = "explorar, caçar, viajar e cada sala" if salas else "explorar, caçar e viajar"
        r.append({"icone": "tocha" if n else "tocha_apagada",
                  "texto": f"Escuro: {onde} gastam 1 tocha por vez (você tem {n})" if n else
                  f"Escuro e sem tocha: Percepção e Destreza −{bal.ESCURO_TESTES}" +
                  ("; nas salas, o inimigo ataca primeiro" if salas else ""),
                  "tipo": "custo" if n else "perigo"})  # o gasto normal de tocha é neutro; a falta de luz, perigo
    return r
