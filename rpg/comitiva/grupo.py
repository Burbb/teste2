"""Quem está no grupo e na reserva, entrar e sair, a aprovação e o que o tempo cobra (comida, soldo)."""

from ..telemetria import registrar
from .catalogo import COMPANHEIROS, LIMITE, NIVEIS, REACOES


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
    falou = None
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
        if not falou and (abs(delta) >= 6 or g.chance(0.4)):
            falou = (m["id"], banco.get(principal) or banco[None])
        mudar_aprovacao(g, m["id"], delta)
    # Quem fala, fala depois de todos reagirem: as aprovações chegam juntas, sem a espera da leitura entre elas.
    if falou:
        g.ui.fala(falou[0], nome(falou[0]), falou[1])
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
        g.perder_ouro(min(g.j.ouro, 20 + 5 * g.j.nivel), destino="comitiva")
    if cid == "yara" and m.get("caminho") == "vazio":
        g.marcar("yara_com_ulook", True)
        g.narrar("Você tem um pressentimento ruim sobre onde ela foi parar.", "magenta")
    sair(g, cid, "partiu")
    g.pausar()


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
        g.perder_ouro(valor, destino="comitiva")
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


def cuidar(g, m):
    """O templo (ou quem mais cuidar dela): a vida cheia e de pé de novo, sem esperar a noite."""
    m["hp"] = m["max_hp"]
    m["ferido"] = False
