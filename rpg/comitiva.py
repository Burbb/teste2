"""Comitiva: companheiros de jornada com valores, opinião, história própria e lugar no combate.

Cada companheiro tem VALORES (o que admira e o que despreza). As escolhas do
jogador carregam ETIQUETAS (misericórdia, ganância, magia proibida...). Quando
você escolhe, cada companheiro reage conforme seus valores: a APROVAÇÃO sobe ou
desce, e às vezes ele diz o que pensa. Aprovação alta deixa o companheiro mais
forte e abre a parte final da história dele; aprovação baixa demais o faz ir
embora (e alguns não vão em paz).

Os três companheiros discordam entre si de propósito: agradar a todos é
impossível, e é isso que dá peso às escolhas.
"""

from . import balanceamento as bal
from .telemetria import registrar

LIMITE = 2  # companheiros ao mesmo tempo (fora o animal do patrulheiro)

COMPANHEIROS = {
    "odete": dict(
        nome="Irmã Odette", curto="Odette", g="f", titulo="clériga desertora", papel="cura",
        desc="Fugiu da catedral na noite em que a Fenda se abriu. Fecha feridas; não perdoa crueldade.",
        base=dict(hp=30, atk=4, poder=6, defesa=3, agi=4), cresc=dict(hp=6, atk=0.6, poder=1.2, defesa=0.6),
        valores={"misericordia": 3, "generosidade": 2, "fe": 3, "honestidade": 2, "purificar": 2, "honra": 1,
                 "diplomacia": 1, "crueldade": -4, "ganancia": -2, "trapaca": -2, "sacrilegio": -4,
                 "magia_proibida": -3, "violencia": -1},
        aprova={
            "misericordia": "Odette toca seu braço de leve. \"Ainda existe gente boa neste reino. Às vezes eu esqueço.\"",
            "generosidade": "\"Moedas não descem com a gente para a cova\", diz Odette, quase sorrindo.",
            "fe": "Odette reza junto, baixinho. Pela primeira vez em dias, a voz dela não treme.",
            "honestidade": "\"A verdade custa caro\", diz Odette. \"Mas é a única moeda que não enferruja.\"",
            "purificar": "Odette faz o sinal da Luz sobre as cinzas. \"Que fique queimado.\"",
            None: "Odette acena com a cabeça, em silêncio.",
        },
        desaprova={
            "crueldade": "Odette desvia o olhar. \"Eu fugi de muita coisa. Não vou fugir de dizer que isso foi errado.\"",
            "ganancia": "\"Ouro\", Odette cospe a palavra. \"Foi por ouro que o bispo vendeu as relíquias. Lembra do que veio depois?\"",
            "sacrilegio": "Odette empalidece. \"Os mortos não se defendem. Por isso mesmo merecem respeito.\"",
            "magia_proibida": "\"Isso é a voz da Fenda\", sussurra Odette, apertando o rosário. \"Eu já ouvi essa voz. Não a deixe entrar.\"",
            "trapaca": "Odette não diz nada. Mas não olha mais para você pelo resto do caminho.",
            "violencia": "\"Precisava disso?\", pergunta Odette, limpando o sangue de alguém que nem conhecia.",
            None: "Odette aperta os lábios.",
        },
        partida="Odette para no meio da estrada. \"Prometi a mim mesma que nunca mais ficaria parada vendo o mal "
                "acontecer. Ficar com você é ficar parada.\" Ela se vira e vai embora, sem pressa, sem olhar para trás.",
        ocioso={
            "alto": ["Odette remenda sua capa sem que você peça. \"Assim o frio entra menos. Não discuta.\"",
                     "\"Quando tudo isso acabar\", diz Odette, \"quero ver uma igreja com as portas abertas. Só isso.\""],
            "medio": ["Odette conta as bandagens que restam. \"Poucas. Tente não sangrar tanto.\"",
                      "Odette olha para o norte, para onde ficava a catedral. Não diz nada."],
            "baixo": ["Odette responde com uma palavra só. Depois, nem isso.",
                      "\"Estou aqui pelos feridos que encontramos no caminho\", diz Odette. \"Não por você.\""],
        },
    ),
    "morel": dict(
        nome="Bastian Morel", curto="Morel", g="m", titulo="mercenário", papel="escudo",
        desc="Ex-capitão de uma companhia que não existe mais. Luta por ouro, segura a linha e odeia covardes.",
        base=dict(hp=52, atk=8, poder=0, defesa=6, agi=3), cresc=dict(hp=9, atk=1.5, poder=0, defesa=1.0),
        valores={"coragem": 3, "pragmatismo": 2, "honra": 2, "ganancia": 1, "violencia": 1, "fuga": -4,
                 "cautela": -1, "generosidade": -1, "autoridade": -2, "trapaca": -1, "fe": -1},
        aprova={
            "coragem": "Morel solta uma gargalhada rouca. \"Isso! Os Cães de Ferro teriam gostado de você.\"",
            "pragmatismo": "\"Cabeça fria\", aprova Morel. \"Herói morto não paga dívida nenhuma.\"",
            "ganancia": "Morel conta as moedas junto com você, de olho. \"Agora sim estamos conversando.\"",
            "honra": "Morel bate o punho no peito, à moda antiga. \"Palavra dada. Ainda existe isso.\"",
            "violencia": "\"Rápido e sujo\", diz Morel, limpando a lâmina. \"Do jeito que funciona.\"",
            None: "Morel resmunga algo que soa como aprovação.",
        },
        desaprova={
            "fuga": "\"Correndo de novo?\" Morel não esconde o desprezo. \"Conheço esse caminho. Ele não acaba bem.\"",
            "cautela": "Morel boceja, alto. \"Se for para fugir de toda sombra, melhor virar pastor de cabras.\"",
            "generosidade": "\"Caridade não enche a barriga de ninguém\", resmunga Morel. \"Muito menos a minha.\"",
            "autoridade": "Morel cospe no chão. \"Guarda, nobre, bispo. Tudo a mesma laia. Nunca dobre o joelho.\"",
            "fe": "\"Rezar\", Morel ri sem graça. \"Rezei a noite toda na Ponte de Varn. Ninguém respondeu.\"",
            "trapaca": "\"Trapaça é para quem não sabe lutar\", diz Morel, e se afasta um passo.",
            None: "Morel cruza os braços.",
        },
        partida="Morel pendura a espada nas costas e cospe no chão. \"Já servi a gente pior. Mas não por esse "
                "preço.\" Ele se vai, e leva consigo o que acha que você lhe deve.",
        ocioso={
            "alto": ["Morel afia a sua lâmina junto com a dele, sem perguntar. \"Fio cego mata o dono primeiro.\"",
                     "\"Sabe\", diz Morel, olhando o fogo, \"faz tempo que não confio as costas a ninguém.\""],
            "medio": ["Morel conta e reconta as moedas da bolsa, como quem reza.",
                      "\"Mais um dia vivo\", diz Morel, e bebe à saúde de ninguém."],
            "baixo": ["Morel dorme com a mão no punho da espada. Virado para você.",
                      "\"O soldo\", diz Morel. Só isso. Duas vezes por dia."],
        },
    ),
    "yara": dict(
        nome="Yara", curto="Yara", g="f", titulo="bruxa do brejo", papel="maldicao",
        desc="Quase queimada como bruxa. A Fenda fala com ela, e às vezes ela responde.",
        base=dict(hp=26, atk=3, poder=9, defesa=2, agi=5), cresc=dict(hp=5, atk=0.4, poder=1.7, defesa=0.4),
        valores={"magia_proibida": 3, "curiosidade": 3, "rebeldia": 3, "misericordia": 1, "diplomacia": 1,
                 "fe": -2, "autoridade": -3, "purificar": -3, "crueldade": -2, "fanatismo": -4, "violencia": -1},
        aprova={
            "magia_proibida": "Os olhos de Yara brilham. \"Você sentiu, não sentiu? Poder não é bom nem mau. É só poder.\"",
            "curiosidade": "Yara ri, encantada. \"Finalmente alguém que abre as portas em vez de pregá-las.\"",
            "rebeldia": "\"Bem feito\", diz Yara. \"Quem manda nunca é quem sangra.\"",
            "misericordia": "Yara observa você em silêncio. Depois, baixinho: \"Ninguém fez isso por mim antes de você.\"",
            "diplomacia": "\"Palavras também são feitiços\", sussurra Yara. \"Você sabe usar.\"",
            None: "Yara sorri de canto.",
        },
        desaprova={
            "fe": "Yara revira os olhos. \"Foi rezando que eles empilharam a lenha em volta de mim.\"",
            "autoridade": "\"Obedecer\", repete Yara, como quem prova algo azedo. \"Quase virei cinza por gente obediente.\"",
            "purificar": "Yara encara as chamas com raiva. \"Queimar o que não se entende. Conheço bem esse costume.\"",
            "crueldade": "Yara se afasta de você. \"Os aldeões que me amarraram também achavam que estavam certos.\"",
            "fanatismo": "Yara treme. Por um instante, você vê nos olhos dela a fogueira que quase a levou.",
            "violencia": "\"Tanto sangue por tão pouco\", diz Yara, enojada.",
            None: "Yara estreita os olhos.",
        },
        partida="Yara some numa noite sem lua. De manhã, só há um círculo de cinzas onde ela dormia, e um cheiro "
                "de coisa queimada que não é lenha.",
        ocioso={
            "alto": ["Yara trança ervas no seu cabelo enquanto você cochila. \"Contra pesadelos. Funciona. Às vezes.\"",
                     "\"Antes de você\", diz Yara, \"eu achava que ia morrer sozinha no brejo. Agora acho que vou morrer acompanhada. É uma melhora.\""],
            "medio": ["Yara fala com um sapo por um bom tempo. O sapo parece concordar.",
                      "Yara desenha símbolos na terra e apaga antes que você consiga ler."],
            "baixo": ["Yara dorme longe da fogueira. E longe de você.",
                      "\"Não se preocupe\", diz Yara, sem sorrir. \"Eu ainda não decidi nada.\""],
        },
    ),
}

# Escolhas dos eventos que mexem com a opinião da comitiva: (evento, opção) -> etiquetas.
REACOES = {
    ("circulo_de_fadas", "dancar"): ("curiosidade",), ("circulo_de_fadas", "trocar"): ("curiosidade",),
    ("circulo_de_fadas", "chutar"): ("violencia",), ("circulo_de_fadas", "nao"): ("cautela",),
    ("colmeia_selvagem", "fogo"): ("violencia",),
    ("luzes_fantasmas", "seguir"): ("curiosidade",), ("luzes_fantasmas", "resistir"): ("cautela",),
    ("cabana_da_bruxa", "atacar"): ("fanatismo", "violencia"), ("cabana_da_bruxa", "futuro"): ("curiosidade",),
    ("ninho_de_grifo", "pegar"): ("ganancia", "crueldade"), ("ninho_de_grifo", "domar"): ("coragem",),
    ("espantalho", "fogo"): ("violencia",), ("espantalho", "examinar"): ("curiosidade", "coragem"),
    ("fazenda_em_apuros", "ajudar"): ("generosidade", "misericordia"), ("fazenda_em_apuros", "nao"): ("pragmatismo",),
    ("biblioteca_ruida", "runas"): ("curiosidade",), ("biblioteca_ruida", "forca"): ("violencia", "sacrilegio"),
    ("golem_adormecido", "lutar"): ("coragem",), ("golem_adormecido", "gema"): ("ganancia",),
    ("sussurros_na_nevoa", "falar"): ("misericordia",), ("sussurros_na_nevoa", "prece"): ("fe", "misericordia"),
    ("sussurros_na_nevoa", "prender"): ("magia_proibida", "crueldade"), ("sussurros_na_nevoa", "nao"): ("cautela",),
    ("duelo_de_honra", "aceitar"): ("coragem", "honra"), ("duelo_de_honra", "recusar"): ("cautela",),
    ("veterano_cicatrizes", "treinar"): ("coragem",),
    ("aldeia_assombrada", "consagrar"): ("fe", "coragem", "purificar"), ("aldeia_assombrada", "nao"): ("cautela",),
    ("os_enfermos", "curar"): ("misericordia", "fe"), ("os_enfermos", "remedio"): ("generosidade",),
    ("os_enfermos", "nao"): ("pragmatismo",),
    ("tentacao_do_juramento", "recusar"): ("honestidade", "fe"), ("tentacao_do_juramento", "aceitar"): ("ganancia",),
    ("tentacao_do_juramento", "prender"): ("honestidade", "autoridade"),
    ("chamado_do_sangue", "nuas"): ("violencia", "coragem"), ("chamado_do_sangue", "resistir"): ("cautela",),
    ("contrato_da_irmandade", "aceitar"): ("ganancia",), ("contrato_da_irmandade", "nao"): ("honestidade",),
    ("contrato_da_irmandade", "matar"): ("crueldade", "ganancia"),
    ("contrato_da_irmandade", "poupar"): ("misericordia", "pragmatismo"),
    ("bolsos_alheios", "roubar"): ("trapaca", "ganancia"),
    ("anomalia_arcana", "absorver"): ("magia_proibida", "curiosidade"), ("anomalia_arcana", "estabilizar"): ("purificar",),
    ("grimorio_perdido", "ler"): ("magia_proibida", "curiosidade"), ("grimorio_perdido", "queimar"): ("purificar", "fe"),
    ("aprendiz_em_apuros", "ensinar"): ("generosidade",), ("aprendiz_em_apuros", "entrar"): ("coragem",),
    ("cacadores_de_bruxas", "falar"): ("diplomacia",), ("cacadores_de_bruxas", "lutar"): ("rebeldia", "violencia"),
    ("cacadores_de_bruxas", "fugir"): ("fuga",),
    ("elemental_selvagem", "absorver"): ("magia_proibida",), ("elemental_selvagem", "lutar"): ("violencia",),
    ("incendio", "dominar"): ("coragem",), ("incendio", "evacuar"): ("misericordia", "generosidade"),
    ("incendio", "nao"): ("crueldade",),
    ("cemiterio_antigo", "recrutar"): ("magia_proibida", "sacrilegio"),
    ("cemiterio_antigo", "aprender"): ("magia_proibida", "curiosidade"), ("cemiterio_antigo", "nao"): ("fe",),
    ("aldeoes_temerosos", "ajudar"): ("generosidade", "honestidade"),
    ("aldeoes_temerosos", "assustar"): ("crueldade", "trapaca"),
    ("encontro_hostil", "atacar"): ("coragem",), ("encontro_hostil", "evitar"): ("cautela",),
    ("encontro_hostil", "conversar"): ("diplomacia",),
    ("viajante_ferido", "pocao"): ("misericordia", "generosidade"), ("viajante_ferido", "bandagem"): ("misericordia",),
    ("viajante_ferido", "prece"): ("fe", "misericordia"), ("viajante_ferido", "cacar"): ("coragem", "misericordia"),
    ("viajante_ferido", "roubar"): ("crueldade", "ganancia", "trapaca"), ("viajante_ferido", "ignorar"): ("pragmatismo",),
    ("mercador_golpista", "exigir"): ("honestidade",), ("mercador_golpista", "ajudar"): ("misericordia", "generosidade"),
    ("mercador_golpista", "licao"): ("violencia", "crueldade"),
    ("bau_abandonado", "nao"): ("cautela",),
    ("santuario_antigo", "rezar"): ("fe",), ("santuario_antigo", "oferenda"): ("fe", "generosidade"),
    ("santuario_antigo", "saquear"): ("sacrilegio", "ganancia"),
    ("acampamento_bandidos", "atacar"): ("coragem", "violencia"), ("acampamento_bandidos", "roubar"): ("trapaca", "ganancia"),
    ("acampamento_bandidos", "acordo"): ("diplomacia", "pragmatismo"), ("acampamento_bandidos", "evitar"): ("cautela",),
    ("crianca_perdida", "levar"): ("misericordia", "generosidade"), ("crianca_perdida", "indicar"): ("misericordia",),
    ("crianca_perdida", "ignorar"): ("crueldade",),
    ("cadaver_aventureiro", "revistar"): ("ganancia", "pragmatismo"), ("cadaver_aventureiro", "enterrar"): ("fe", "misericordia"),
    ("jogo_de_dados", "trapacear"): ("trapaca",),
    ("cacadores_de_recompensa", "lutar"): ("coragem",), ("cacadores_de_recompensa", "pagar"): ("pragmatismo",),
    ("pacote_suspeito", "recusar"): ("honestidade",), ("pacote_suspeito", "vender"): ("ganancia",),
    ("peregrinos", "ouvir"): ("fe",), ("peregrinos", "doar"): ("generosidade", "fe"),
    ("refugiados", "escoltar"): ("misericordia", "coragem"), ("refugiados", "doar"): ("generosidade",),
    ("refugiados", "nao"): ("pragmatismo",),
    ("caravana_atacada", "ajudar"): ("coragem", "misericordia"), ("caravana_atacada", "esperar"): ("ganancia", "crueldade"),
    ("tumulo_do_heroi", "honrar"): ("fe", "honra"), ("tumulo_do_heroi", "cavar"): ("sacrilegio", "ganancia"),
    ("visitante_misterioso", "dividir"): ("generosidade", "misericordia"), ("visitante_misterioso", "mandar"): ("cautela",),
    ("ladrao_noturno", "soltar"): ("misericordia",), ("ladrao_noturno", "entregar"): ("autoridade",),
    ("sussurros_do_vazio", "recusar"): ("purificar",), ("sussurros_do_vazio", "ouvir"): ("magia_proibida",),
    ("briga_de_taverna", "separar"): ("coragem",), ("briga_de_taverna", "entrar"): ("violencia",),
    ("briga_de_taverna", "roubar"): ("trapaca", "ganancia"),
    ("festival", "vigilia"): ("fe",), ("festival", "poco"): ("violencia", "coragem"),
    ("pregador_do_vazio", "debater"): ("coragem", "honestidade"), ("pregador_do_vazio", "seguir"): ("curiosidade", "coragem"),
    ("mendigo_misterioso", "dar"): ("generosidade",), ("mendigo_misterioso", "refeicao"): ("generosidade", "misericordia"),
    ("guarda_desconfiado", "pagar"): ("autoridade",), ("guarda_desconfiado", "argumentar"): ("diplomacia", "rebeldia"),
    ("guarda_desconfiado", "cela"): ("autoridade",),
}

NIVEIS = [(-40, "prestes a partir", "partindo"), (-15, "desconfiad{a}", "baixo"), (15, "neutr{a}", "neutro"),
          (45, "confia em você", "bom"), (75, "leal", "alto"), (101, "devotad{a}", "maximo")]

CONVERSAS = {}  # cid -> lista de (etapa, requisitos, função); preenchida por eventos/comitiva.py


def conversa(cid, etapa, dias=0, aprov=-100, cond=None):
    """Registra a conversa número `etapa` de um companheiro."""
    def deco(fn):
        CONVERSAS.setdefault(cid, []).append((etapa, dict(dias=dias, aprov=aprov, cond=cond), fn))
        CONVERSAS[cid].sort(key=lambda c: c[0])
        return fn
    return deco


# ---------------------------------------------------------------- consultas
def dados(cid):
    return COMPANHEIROS[cid]


def membros(g):
    return list(getattr(g, "comitiva", None) or [])


def membro(g, cid):
    return next((m for m in membros(g) if m["id"] == cid), None)


def presente(g, cid):
    return membro(g, cid) is not None


def reserva(g):
    """Quem espera no acampamento: não anda com você, não luta, não come do seu saco e não opina."""
    return list(getattr(g, "reserva", None) or [])


def na_reserva(g, cid):
    return next((m for m in reserva(g) if m["id"] == cid), None)


def disponivel(g, cid):
    """Ainda pode ser encontrado: não está na comitiva nem no acampamento, não morreu, não foi embora."""
    return not presente(g, cid) and not na_reserva(g, cid) and not g.flag(f"comitiva:{cid}")


def nome(cid):
    return COMPANHEIROS[cid]["curto"]


def flexao(cid, texto):
    return texto.replace("{a}", "a" if COMPANHEIROS[cid]["g"] == "f" else "o")


def nivel(m):
    for limite, rotulo, classe in NIVEIS:
        if m["aprovacao"] < limite:
            return flexao(m["id"], rotulo), classe
    return flexao(m["id"], NIVEIS[-1][1]), NIVEIS[-1][2]


def lealdade(m):
    """Multiplicador de força conforme a aprovação: quem confia em você luta melhor."""
    return max(0.6, min(1.35, 0.9 + m["aprovacao"] / 250))


def atributos(g, m):
    d = COMPANHEIROS[m["id"]]
    nv = g.j.nivel - 1
    b, c = d["base"], d["cresc"]
    return {
        "max_hp": int(b["hp"] + c["hp"] * nv),
        "atk": b["atk"] + c["atk"] * nv,
        "poder": b["poder"] + c["poder"] * nv,
        "defesa": int(b["defesa"] + c["defesa"] * nv),
        "agi": b["agi"],
    }


def atualizar_vida_maxima(g):
    for m in membros(g) + reserva(g):
        novo = atributos(g, m)["max_hp"]
        if novo > m["max_hp"]:
            m["hp"] += novo - m["max_hp"]
        m["max_hp"] = novo
        m["hp"] = min(m["hp"], m["max_hp"])


# ---------------------------------------------------------------- entrar e sair
def recrutar(g, cid):
    if presente(g, cid) or na_reserva(g, cid):
        return None
    m = {"id": cid, "aprovacao": 0, "dias": 0, "desde": g.dia, "conversas": 0, "ultima_conversa": -1,
         "missao": 0, "caminho": None, "ferido": False, "hp": 1, "max_hp": 1}
    m["max_hp"] = m["hp"] = atributos(g, m)["max_hp"]
    g.comitiva.append(m)
    d = COMPANHEIROS[cid]
    g.ui.efeito(f"{d['nome']} se junta à comitiva", "aprova")
    g.ui.celebrar("comitiva", {"id": cid, "nome": d["nome"], "titulo": d["titulo"], "desc": d["desc"]})
    registrar(g, "comitiva", acao="entra", id=cid)
    return m


def sair(g, cid, motivo="saiu"):
    m = membro(g, cid)
    if not m:
        return
    g.comitiva.remove(m)
    g.marcar(f"comitiva:{cid}", motivo)
    registrar(g, "comitiva", acao=motivo, id=cid, aprovacao=m["aprovacao"], dias=m["dias"])


def oferecer_vaga(g, cid):
    """Pergunta se o jogador aceita o companheiro (trocando alguém, se a comitiva estiver cheia)."""
    d = COMPANHEIROS[cid]
    ms = membros(g)
    if len(ms) < LIMITE:
        op = g.menu(f"Levar {d['curto']} com você?", [(f"Aceitar {d['curto']} na comitiva", "sim"),
                                                       ("Recusar", "nao")])
        if op == "sim":
            recrutar(g, cid)
            return True
        return False
    opcoes = [(f"Mandar {nome(m['id'])} para o acampamento e levar {d['curto']}", m["id"]) for m in ms]
    opcoes.append((f"{d['curto']} espera no acampamento (troque quando acampar)", "reserva"))
    opcoes.append(("Recusar", None))
    troca = g.menu(f"Sua comitiva está cheia. {d['curto']} quer vir.", opcoes)
    if troca is None:
        return False
    if troca == "reserva":
        recrutar(g, cid)
        para_acampamento(g, cid, silencioso=True)
        return True
    para_acampamento(g, troca, silencioso=True)
    recrutar(g, cid)
    return True


def para_acampamento(g, cid, silencioso=False):
    """Sai da comitiva sem ir embora: espera no acampamento até ser chamado de volta."""
    m = membro(g, cid)
    if not m:
        return
    g.comitiva.remove(m)
    m["ferido"] = False
    g.reserva.append(m)
    if not silencioso:
        g.ui.efeito(f"{nome(cid)} vai esperar no acampamento", "info")
    registrar(g, "comitiva", acao="acampamento", id=cid, aprovacao=m["aprovacao"])


def chamar(g, cid):
    """Do acampamento de volta para a estrada (se houver lugar)."""
    m = na_reserva(g, cid)
    if not m or len(membros(g)) >= LIMITE:
        return False
    g.reserva.remove(m)
    g.comitiva.append(m)
    g.ui.efeito(f"{nome(cid)} volta para a comitiva", "aprova")
    registrar(g, "comitiva", acao="volta", id=cid, aprovacao=m["aprovacao"])
    return True


def dispensar(g, cid, silencioso=False):
    d = COMPANHEIROS[cid]
    if not silencioso:
        g.narrar(f"{d['curto']} junta as coisas sem dizer muito. Na primeira encruzilhada, cada um segue o seu caminho.",
                 "cinza")
    m = na_reserva(g, cid)
    if m:  # quem estava no acampamento também pode ser despedido de vez
        g.reserva.remove(m)
        g.comitiva.append(m)
    sair(g, cid, "dispensado")
    g.ui.efeito(f"{d['nome']} deixa a comitiva", "desaprova")


# ---------------------------------------------------------------- opinião
def mudar_aprovacao(g, cid, delta, mostrar=True, fala=None):
    m = membro(g, cid) or na_reserva(g, cid)  # conversas na fogueira também contam
    if not m or not delta:
        return
    m["aprovacao"] = max(-100, min(100, m["aprovacao"] + delta))
    if mostrar:
        g.ui.opiniao(cid, nome(cid), delta)
    if fala:
        g.ui.fala(cid, nome(cid), fala)
    registrar(g, "comitiva", acao="opiniao", id=cid, delta=delta, aprovacao=m["aprovacao"])


def reagir(g, *etiquetas, forca=1.0):
    """Cada companheiro julga a escolha conforme os próprios valores."""
    if not etiquetas or not membros(g):
        return
    falou = False
    for m in membros(g):
        d = COMPANHEIROS[m["id"]]
        pesos = [(t, d["valores"].get(t, 0)) for t in etiquetas]
        delta = int(round(2 * forca * sum(p for _, p in pesos)))
        delta = max(-12, min(12, delta))
        if not delta:
            continue
        # A fala vem da etiqueta que mais pesou; falas fortes sempre aparecem, as fracas às vezes.
        principal = max(pesos, key=lambda tp: abs(tp[1]))[0]
        banco = d["aprova"] if delta > 0 else d["desaprova"]
        fala = None
        if not falou and (abs(delta) >= 6 or g.chance(0.4)):
            fala = banco.get(principal) or banco[None]
            falou = True
        mudar_aprovacao(g, m["id"], delta, fala=fala)
    verificar_partidas(g)


def reagir_escolha(g, evento_id, chave):
    if isinstance(chave, str):
        etiquetas = REACOES.get((evento_id, chave))
        if etiquetas:
            reagir(g, *etiquetas)


def verificar_partidas(g):
    for m in membros(g):
        if m["aprovacao"] <= -40:
            partir(g, m)


def partir(g, m):
    cid = m["id"]
    d = COMPANHEIROS[cid]
    g.ui.cena(f"{d['curto']} vai embora", None, "evento")
    g.narrar(d["partida"], "vermelho")
    if cid == "morel":
        g.perder_ouro(min(g.j.ouro, 20 + 5 * g.j.nivel))
    if cid == "yara" and m.get("caminho") == "vazio":
        g.marcar("yara_com_ulook", True)
        g.narrar("Você tem um pressentimento ruim sobre onde ela foi parar.", "magenta")
    sair(g, cid, "partiu")
    g.pausar()


# ---------------------------------------------------------------- tempo
def amanhecer(g, descanso, refeicao=False):
    for m in membros(g):
        m["dias"] += 1
        if descanso:
            m["ferido"] = False
    for m in reserva(g):  # no acampamento, todo mundo se recupera
        m["hp"] = m["max_hp"]
        m["ferido"] = False
    return comer(g) if not refeicao else []


def depois_do_amanhecer(g, famintos):
    """O que a comitiva diz quando o dia já raiou: a queixa de quem passou fome, e o soldo do Morel."""
    for cid in famintos:
        mudar_aprovacao(g, cid, -6, fala=f"{nome(cid)} passa o dia sem comer. Não reclama em voz alta.")
    if presente(g, "morel"):
        pagar_soldo(g)


def comer(g):
    """Cada companheiro come uma provisão por dia. Uma comitiva come; fome tem preço (a queixa vem depois, em
    depois_do_amanhecer). Devolve quem passou fome."""
    famintos = []
    for m in membros(g):
        if g.j.provisoes > 0:
            g.j.provisoes -= 1
        else:
            m["hp"] = max(1, m["hp"] - m["max_hp"] // 4)
            g.relatar(None, None, "perigo", m["id"], f"{nome(m['id'])} sem comida: −{m['max_hp'] // 4} vida")
            famintos.append(m["id"])
    return famintos


def pagar_soldo(g):
    m = membro(g, "morel")
    if m["dias"] == 0 or m["dias"] % 7:
        return
    valor = 8 + 3 * g.j.nivel
    g.dizer(f"Morel estende a mão aberta. \"Sete dias. O soldo: {valor} moedas.\"", "amarelo")
    opcoes = [(f"Pagar {valor} ouro", "pagar") if g.j.ouro >= valor else None,
              ("Dizer que não há dinheiro agora", "dever")]
    if g.menu("O soldo de Morel", opcoes) == "pagar":
        g.perder_ouro(valor)
        mudar_aprovacao(g, "morel", 3, fala="Morel morde uma moeda, satisfeito. \"Patrão bom paga em dia.\"")
    else:
        mudar_aprovacao(g, "morel", -10, fala="\"Dívida com mercenário\", diz Morel, \"cobra juros de um jeito ou de outro.\"")
        verificar_partidas(g)


def parte_do_xp(g):
    """A experiência é dividida com quem lutou junto: quem anda só aprende mais rápido."""
    return max(0.6, 1 - 0.12 * len(membros(g)))


def descansar(g, fracao):
    for m in membros(g):
        m["hp"] = min(m["max_hp"], m["hp"] + int(m["max_hp"] * min(1.0, fracao)))


# ---------------------------------------------------------------- conversas
def proxima_conversa(g, m):
    for etapa, req, fn in CONVERSAS.get(m["id"], []):
        if etapa != m["conversas"]:
            continue
        if m["dias"] < req["dias"] or m["aprovacao"] < req["aprov"]:
            return None
        if req["cond"] and not req["cond"](g, m):
            return None
        return fn
    return None


def conversar(g, m):
    fn = proxima_conversa(g, m)
    if fn and m["ultima_conversa"] != g.dia:
        m["ultima_conversa"] = g.dia
        g.ui.cena(f"Conversa com {nome(m['id'])}", g.contexto_cena(), "evento")
        fn(g, m)
        m["conversas"] += 1
        registrar(g, "comitiva", acao="conversa", id=m["id"], etapa=m["conversas"])
        return True
    return False


def noite(g):
    """No acampamento, alguém da comitiva pode puxar conversa. Devolve True se houve conversa."""
    pendentes = [m for m in membros(g) if proxima_conversa(g, m) and m["ultima_conversa"] != g.dia]
    if pendentes and g.chance(0.65):
        return conversar(g, g.sortear(pendentes))
    return False


def fala_ociosa(g, m):
    _, classe = nivel(m)
    faixa = "alto" if classe in ("bom", "alto", "maximo") else "baixo" if classe in ("baixo", "partindo") else "medio"
    return g.sortear(COMPANHEIROS[m["id"]]["ocioso"][faixa])


CARINHO = {
    "lobo": ["{n} deita a cabeça no seu joelho e fecha os olhos. O rabo bate devagar no chão.",
             "Você coça atrás das orelhas de {n}. Ele solta um suspiro longo de cachorro velho."],
    "urso": ["{n} rola de barriga para cima, esperando. Você coça. O chão treme com o ronco de satisfação.",
             "Você encosta na lateral quente de {n}. Ele te puxa com a pata, como se você fosse um filhote."],
    "falcao": ["{n} desce do galho para o seu braço e esfrega a cabeça na sua bochecha. Raro, para um falcão.",
               "Você alisa as penas do peito de {n}. Ele arrepia tudo, finge que não gostou, e fica."],
}


def carinho(g):
    """Uma vez por noite: o animal do patrulheiro acorda animado e entra na próxima luta com +15% de dano.
    (A vida ele já recupera dormindo; o carinho é o laço.)"""
    f = g.j.companheiro
    if f.get("carinho") == g.dia:
        texto = f"{f['nome']} já dorme encostado em você, roncando baixinho."
        g.ui.reacao_animal({"nome": f["nome"], "texto": texto, "repetido": True}, texto, "cinza")
        return
    f["carinho"] = g.dia
    f["animado"] = True
    texto = g.sortear(CARINHO.get(f["tipo"], CARINHO["lobo"])).format(n=f["nome"])
    efeito = "Amanhã, na primeira luta, ele entra animado: +15% de dano."
    g.ui.reacao_animal({"nome": f["nome"], "texto": texto, "efeito": efeito},
                       f"{texto} ({efeito[0].lower()}{efeito[1:-1]})", "verde")


# O que dá para fazer no acampamento além da fogueira (a própria fogueira faz as vezes da Comitiva; viajar, só de dia).
ATALHOS_FOGUEIRA = ("talentos", "personagem", "mapa", "diario", "bestiario", "salvar", "sair")


def fogueira(g, intro=None):
    """O acampamento à noite: quem anda com você e quem espera na reserva, em volta do fogo.
    Conversar, trocar quem vai junto amanhã e, por fim, dormir. Devolve True se houve conversa de história."""
    conversou = False
    ociosos = set()
    primeira = True
    while True:
        ms, rs = membros(g), reserva(g)
        g.ui.cena("Fogueira", g.contexto_cena(), "menu")
        # A frase da noite é parte da tela: quem a desenha mostra de novo a cada volta (carinho, trocar quem vai),
        # senão a página encolhe e pula; no texto, ela sai só uma vez.
        dados = {"ativos": estado(g), "reserva": estado(g, reserva(g)), "limite": LIMITE,
                 "clima": g.clima, "bioma": g.loc["bioma"], "intro": intro}
        fera = getattr(g.j, "companheiro", None)
        if fera:  # o animal do patrulheiro dorme junto do fogo
            dados["fera"] = {"nome": fera["nome"], "tipo": fera["tipo"], "hp": fera["hp"], "max_hp": fera["max_hp"]}
        if not g.ui.painel("acampamento", dados):
            if intro and primeira:
                g.dizer(intro, "cinza")
            for m in ms + rs:
                onde = "na comitiva" if m in ms else "no acampamento"
                g.dizer(f"{nome(m['id'])} ({onde}) — vida {m['hp']}/{m['max_hp']} · {nivel(m)[0]}", "cinza")
        primeira = False
        opcoes = []
        for m in ms + rs:
            tem = proxima_conversa(g, m) and m["ultima_conversa"] != g.dia
            if tem or m["id"] not in ociosos:
                opcoes.append((f"Conversar com {nome(m['id'])}" + ("  ✉" if tem else ""), ("falar", m["id"]),
                               {"conversar": m["id"]}))
        for m in rs:
            if len(ms) < LIMITE:
                opcoes.append((f"Levar {nome(m['id'])} amanhã", ("chamar", m["id"]), {"chamar": m["id"]}))
            else:
                for a in ms:
                    opcoes.append((f"Levar {nome(m['id'])} no lugar de {nome(a['id'])}", ("trocar", m["id"], a["id"]),
                                   {"chamar": m["id"], "sai": a["id"]}))
        for m in ms:
            opcoes.append((f"Deixar {nome(m['id'])} no acampamento", ("reservar", m["id"]), {"reservar": m["id"]}))
        if getattr(g.j, "companheiro", None):
            opcoes.append((f"Fazer carinho em {g.j.companheiro['nome']}", ("carinho", None), {"carinho": "fera"}))
        opcoes.append(("Dormir até o amanhecer", None, {"dormir": True}))
        # Em volta do fogo é a hora de cuidar das coisas: talentos, inventário, diário, salvar (a doca acende)...
        opcoes += [o for o in g.opcoes_comuns() if o and o[1] in ATALHOS_FOGUEIRA]
        # ...e de fazer curativos: a bolsa do painel funciona aqui (bandagem, poção, unguento).
        opcoes += g.opcoes_bolsa()
        op = g.menu("", opcoes)
        if op is None:
            return conversou
        if isinstance(op, str):
            g.executar_comum(op)
            continue
        acao, cid = op[0], op[1]
        if acao in ("usar", "usar_em"):
            g.executar_comum(op)
            continue
        if acao == "carinho":
            carinho(g)
            continue
        m = membro(g, cid) or na_reserva(g, cid)
        if acao == "falar":
            if conversar(g, m):
                conversou = True
            else:
                ociosos.add(cid)
                g.ui.fala(cid, nome(cid), fala_ociosa(g, m))
        elif acao == "chamar":
            chamar(g, cid)
        elif acao == "trocar":
            para_acampamento(g, op[2], silencioso=True)
            chamar(g, cid)
        elif acao == "reservar":
            para_acampamento(g, cid)


def menu(g):
    while True:
        ms = membros(g)
        g.ui.cena("Comitiva", f"{len(ms)}/{LIMITE} companheiros", "menu")
        if not ms:
            rs = reserva(g)
            g.dizer("Ninguém caminha com você agora." + (
                f" {' e '.join(nome(m['id']) for m in rs)} espera{'m' if len(rs) > 1 else ''} no acampamento: "
                "monte a fogueira para chamar." if rs else " Por enquanto."), "cinza")
            g.pausar()
            return
        painel = {"membros": estado(g), "limite": LIMITE, "reserva": estado(g, reserva(g))}
        for m in ([] if g.ui.painel("comitiva", painel) else ms):
            d = COMPANHEIROS[m["id"]]
            rotulo, _ = nivel(m)
            situacao = " · FERID" + ("A" if d["g"] == "f" else "O") + ", fora de combate até descansar" if m["ferido"] else ""
            g.dizer(f"{d['nome']}, {d['titulo']} — vida {m['hp']}/{m['max_hp']} · {rotulo}{situacao}")
            g.dizer(d["desc"], "cinza")
        opcoes = []
        for m in ms:
            novidade = "  (tem algo a dizer)" if proxima_conversa(g, m) and m["ultima_conversa"] != g.dia else ""
            opcoes.append((f"Conversar com {nome(m['id'])}{novidade}", ("falar", m["id"]), {"conversar": m["id"]}))
        for m in ms:
            opcoes.append((f"Mandar {nome(m['id'])} para o acampamento", ("acampamento", m["id"]),
                           {"acampamento": m["id"]}))
        opcoes.append(("Voltar", None))
        op = g.menu("", opcoes)
        if op is None:
            return
        acao, cid = op
        m = membro(g, cid)
        if acao == "falar":
            if not conversar(g, m):
                g.ui.fala(cid, nome(cid), fala_ociosa(g, m))
        else:
            g.narrar(f"{nome(cid)} pega as coisas e volta para o acampamento. Quando você montar a fogueira, "
                     "vai estar lá.", "cinza")
            para_acampamento(g, cid)


# ---------------------------------------------------------------- combate
def preparar_combate(cb):
    """Cria os aliados da comitiva para esta luta. Feridos ficam na retaguarda."""
    from .combate import Aliado
    g = cb.g
    lista = []
    for m in membros(g):
        if m["ferido"] or m["hp"] <= 0:
            continue
        d = COMPANHEIROS[m["id"]]
        at = atributos(g, m)
        f = lealdade(m)
        a = Aliado(d["curto"], m["max_hp"], at["atk"] * f, at["agi"], tipo="comitiva")
        a.hp = m["hp"]
        a.g = d["g"]
        a.poder = at["poder"] * f
        a.defesa = at["defesa"]
        a.cid = m["id"]
        a.membro = m
        a.fe = 2 if m["id"] == "odete" else 0
        lista.append(a)
        cb.aliados.append(a)
    # Inimigos que enfrentam um grupo resistem mais (e chefes, feitos para um herói só, mais ainda).
    for e in cb.inimigos:
        fator = 1 + (bal.COMITIVA_VIDA_CHEFE if e.chefe else bal.COMITIVA_VIDA_INIMIGO) * len(lista)
        e.max_hp = int(e.max_hp * fator)
        e.hp = int(e.hp * fator)
    if lista and len(lista) == len(membros(g)):
        cb.dizer(f"{' e '.join(a.nome for a in lista)} se {'posicionam' if len(lista) > 1 else 'posiciona'} ao seu lado.", "ciano")
    feridos = [m for m in membros(g) if m["ferido"]]
    if feridos:
        cb.dizer(f"{' e '.join(nome(m['id']) for m in feridos)} ainda se recupera{'m' if len(feridos) > 1 else ''} "
                 "e fica para trás.", "cinza")
    return lista


def alvo_inimigo(cb, aliados, e=None):
    """Morel chama a atenção dos inimigos para si (chefes caem menos nessa)."""
    tanque = next((a for a in aliados if getattr(a, "cid", None) == "morel"), None)
    chance = 0.4 if tanque and tanque.membro["aprovacao"] >= 45 else 0.3
    if e is not None and e.chefe:
        chance /= 2
    if tanque and cb.rng.random() < chance:
        return tanque
    return None


# Falas curtas no meio da luta: aparecem em balões, uma por turno no máximo.
GRITOS = {
    "odete": {"cura": ["Fica de pé. Ainda não é hora.", "Respira. Eu tô aqui.", "A Mãe não te quer ainda."],
              "ataque": ["Que a luz te encontre!", "Perdoa. Mas vai doer."]},
    "morel": {"ataque": ["Vem, vem!", "Isso é pelo soldo.", "Olha pra mim, desgraçado!"],
              "atordoa": ["Fica aí no chão.", "Escudo na cara. Funciona sempre."]},
    "yara": {"maldicao": ["Eu vejo teu fio... e corto.", "Tua sorte acabou."],
             "ataque": ["Queima por dentro.", "Hm. Frágil."]},
}


def gritar(cb, a, situacao, chance=0.3):
    banco = GRITOS.get(a.cid, {}).get(situacao)
    if not banco or cb._fala_turno == cb.turno or cb.rng.random() >= chance:
        return
    cb._fala_turno = cb.turno
    cb.ui.fala(a.cid, a.nome, cb.rng.choice(banco))


def agir(cb, a):
    """Ação de um companheiro no turno dos aliados."""
    cid = a.cid
    vivos = cb.inimigos_vivos()
    if cid == "odete":
        feridos = [c for c in [cb.j] + [x for x in cb.aliados if x.vivo] if c.hp < c.max_hp * 0.4]
        if feridos and a.fe > 0:
            alvo = min(feridos, key=lambda c: c.hp / c.max_hp)
            cura = int(a.poder * 2.2 + alvo.max_hp * 0.12)
            ganho = alvo.curar(cura)
            a.fe -= 1
            quem = "você" if alvo is cb.j else alvo.nome
            cb.curou(alvo, ganho, de=a, rotulo="Prece")
            cb.detalhe(f"[Prece] Odette impõe as mãos sobre {quem}: +{ganho} de vida.", "verde")
            gritar(cb, a, "cura", 0.5)
            if a.membro["aprovacao"] >= 75:
                alvo.limpar_negativos()
            return
        cb.atacar(a, cb.rng.choice(vivos), 0.9, tipo="sagrado", rotulo="Odette")
        gritar(cb, a, "ataque", 0.15)
        return
    if cid == "morel":
        alvo = min(vivos, key=lambda e: e.hp)
        dano = cb.atacar(a, alvo, 1.0, rotulo="Morel")
        if dano and cb.rng.random() < 0.2:
            if cb.aplicar(alvo, "atordoado", 1, rotulo="atordoado pelo escudo"):
                gritar(cb, a, "atordoa", 0.6)
                return
        gritar(cb, a, "ataque", 0.15)
        return
    if cid == "yara":
        vazio = a.membro.get("caminho") == "vazio"
        sem_maldicao = [e for e in vivos if not e.efeito("enfraquecido")]
        if sem_maldicao and cb.turno % 3 == 1:
            alvo = max(sem_maldicao, key=lambda e: e.atk)
            cb.lance("feitico", de=cb.uid(a), em=cb.uid(alvo), elemento="sombra", rotulo="Maldição")
            cb.aplicar(alvo, "enfraquecido", 2, rotulo="amaldiçoado por Yara")
            if vazio:
                cb.aplicar(alvo, "maldito", 2)
            gritar(cb, a, "maldicao", 0.4)
            return
        tipo = "sombra" if vazio else "arcano"
        cb.atacar(a, cb.rng.choice(vivos), 1.5 if vazio else 1.0, tipo=tipo, alcance="distancia", stat="poder",
                  rotulo="Yara")
        gritar(cb, a, "ataque", 0.15)


def encerrar_combate(cb, resultado):
    """Devolve a vida aos membros; quem caiu pode ter morrido de verdade."""
    g = cb.g
    for a in cb.aliados:
        m = getattr(a, "membro", None)
        if not m or m not in g.comitiva:
            continue
        if a.vivo:
            m["hp"] = a.hp
            continue
        if resultado == "derrota":
            continue
        cuidado = presente(g, "odete") and m["id"] != "odete" and not membro(g, "odete")["ferido"]
        if g.chance(0.12 if cuidado else 0.25):
            morrer(g, m)
        else:
            m["hp"] = 1
            m["ferido"] = True
            g.dizer(f"{a.nome} está caíd{'a' if a.g == 'f' else 'o'}, mas respira. Vai precisar de uma noite "
                    "de descanso antes de lutar de novo.", "amarelo")
    if presente(g, "yara") and membro(g, "yara").get("caminho") == "vazio" and resultado == "vitoria":
        # o poder da Fenda cobra o seu preço: Yara bebe um pouco da sua vida a cada luta
        g.j.hp = max(1, g.j.hp - max(1, int(g.j.max_hp * bal.YARA_VAZIO_CUSTO)))


def morrer(g, m):
    cid = m["id"]
    d = COMPANHEIROS[cid]
    g.ui.separador("vermelho")
    finais = {
        "odete": "Odette cai de joelhos, as mãos ainda erguidas numa prece que não termina. Quando você chega até ela, "
                 "os olhos já estão parados, voltados para o norte, para a catedral.",
        "morel": "Morel ainda tenta se levantar, apoiado na espada. \"Segura a linha\", ele diz, para ninguém. "
                 "Depois desaba, e a linha que ele segurava era você.",
        "yara": "Yara cai sem um som. Por um instante, a sombra dela continua de pé. Depois se desfaz, como fumaça.",
    }
    g.narrar(finais[cid], "vermelho")
    g.ui.efeito(f"{d['nome']} morreu", "ferimento")
    sair(g, cid, "morto")
    for outro in membros(g):
        if outro["id"] == "odete":
            g.dizer(f"Odette fecha os olhos de {d['curto']} e reza por um bom tempo.", "cinza")
        elif outro["id"] == "morel":
            g.dizer("Morel cava a cova sozinho. Não deixa ninguém ajudar.", "cinza")
        else:
            g.dizer(f"Yara canta baixinho, numa língua que você não conhece, sobre o corpo de {d['curto']}.", "cinza")
        mudar_aprovacao(g, outro["id"], -4, mostrar=False)


# ---------------------------------------------------------------- final
def antes_da_batalha_final(g):
    """A comitiva diante do fim. Devolve inimigos extras (traições), se houver."""
    extras = []
    for m in membros(g):
        cid = m["id"]
        if cid == "yara" and m.get("caminho") == "vazio" and m["aprovacao"] < 40:
            g.narrar("Yara dá um passo à frente, e não para. Atravessa o salão até o trono e se vira para você. "
                     "Os olhos dela agora são dois poços sem fundo.", "magenta")
            g.narrar("\"Desculpe\", diz ela, e parece sincera. \"Ele me prometeu o que você nunca prometeu: "
                     "que eu nunca mais teria medo.\"", "magenta+negrito")
            sair(g, "yara", "traiu")
            extras.append("yara")
        elif m["aprovacao"] >= 45:
            falas = {
                "odete": "Odette aperta seu ombro. \"Desta vez eu não vou fugir.\"",
                "morel": "Morel desembainha a espada e se põe um passo à sua frente. \"Segura a linha. Eu seguro você.\"",
                "yara": "Yara entrelaça os dedos nos seus por um instante. \"Ele vai tentar falar comigo. Não deixa.\"",
            }
            g.narrar(falas[cid], "verde")
    if g.flag("yara_com_ulook") and "yara" not in extras:
        g.narrar("Ao lado do trono, uma figura conhecida, de olhos negros. Yara. Ela encontrou quem a ouvisse.",
                 "magenta")
        extras.append("yara")
    return extras


def explicar_aprovacao(g, m):
    """O que a barra de aprovação significa para este companheiro, agora."""
    d = COMPANHEIROS[m["id"]]
    a = m["aprovacao"]
    rotulo, _ = nivel(m)
    linhas = [f"Vai de −100 a +100. Agora: {a:+d} ({rotulo}).",
              f"Sobe quando você faz o que {d['curto']} admira ({', '.join(_valores(d, True))}); "
              f"desce com o que despreza ({', '.join(_valores(d, False))}).",
              f"Em combate, luta com {lealdade(m) * 100:.0f}% da força (de 60% a 135%, conforme a confiança)."]
    prox = next((req for etapa, req, _ in CONVERSAS.get(m["id"], []) if etapa == m["conversas"]), None)
    if prox and a < prox["aprov"]:
        linhas.append(f"A próxima conversa só se abre com aprovação {prox['aprov']:+d} ou mais.")
    elif prox and m["dias"] < prox["dias"]:
        linhas.append("A próxima conversa precisa de mais alguns dias juntos.")
    if a <= -15:
        linhas.append("Abaixo de −40, vai embora (e nem todos vão em paz).")
    elif a >= 75:
        linhas.append("Lealdade máxima: a história pessoal pode chegar ao fim e há bônus no combate.")
    return linhas


def _valores(d, bons):
    nomes = {"misericordia": "misericórdia", "fe": "fé", "honestidade": "honestidade", "crueldade": "crueldade",
             "sacrilegio": "sacrilégio", "magia_proibida": "magia proibida", "coragem": "coragem",
             "pragmatismo": "pragmatismo", "honra": "honra", "fuga": "fugir", "autoridade": "autoridade",
             "caridade": "caridade", "curiosidade": "curiosidade", "rebeldia": "rebeldia", "fanatismo": "fanatismo",
             "purificar": "purificar", "violencia": "violência", "ganancia": "ganância"}
    itens = sorted(d["valores"].items(), key=lambda kv: -kv[1] if bons else kv[1])
    return [nomes.get(k, k.replace("_", " ")) for k, v in itens if (v > 0) == bons][:3]


def estado(g, quem=None):
    lista = []
    for m in (membros(g) if quem is None else quem):
        d = COMPANHEIROS[m["id"]]
        rotulo, classe = nivel(m)
        lista.append({"id": m["id"], "nome": d["nome"], "titulo": d["titulo"], "desc": d["desc"],
                      "hp": m["hp"], "max_hp": m["max_hp"],
                      "aprovacao": m["aprovacao"], "nivel": rotulo, "classe": classe, "ferido": m["ferido"],
                      "papel": d["papel"], "conversa": bool(proxima_conversa(g, m)) and m["ultima_conversa"] != g.dia,
                      "aprovacao_info": explicar_aprovacao(g, m)})
    return lista
