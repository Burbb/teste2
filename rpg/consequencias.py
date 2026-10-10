"""Consequências locais da campanha escrita (E4): o que o desfecho de uma missão muda no lugar, e quem atende ali.

Primeira consequência: o Vau do Turvo depois da guardiã. Nada aqui é simulação: o estado da Fonte Nova sai de dois
números guardados na missão (o desfecho e o dia em que ele aconteceu, `missoes.registro(...)["dia_desfecho"]`) e da
passagem de dias que o jogo já tem (`g.dia`). Dele saem a frase da vila, quem atende na curandeira (Pita enquanto
Marta está de cama; Marta depois que a água limpa) e o que o Diário diz da Fonte.

    sem desfecho  → a febre de sempre: Pita atende, a frase da vila é a de sempre
    descansada    → "limpando" por 2 dias (o lodo assenta, sem piora) e depois "limpa"
    destruida     → "escura" no dia do confronto (a água corre turva, a febre piora uma noite),
                    "limpando" até o 3º dia e depois "limpa"

A comporta ainda não existe como ação: nenhum caminho aqui supõe que ela foi fechada (11-E1, seção 4: com ela fechada,
destruir não teria a noite pior). O mundo gerado não tem nada disto.
"""

from . import missoes

MISSAO = "febre_do_turvo"

# Dias depois do desfecho em que a Fonte muda de estado: (até este dia, estado). Depois do último, "limpa".
FONTE = {
    "descansada": [(2, "limpando")],
    "destruida": [(1, "escura"), (3, "limpando")],
}


def _missao(g):
    return missoes.registro(g, MISSAO) if g.campanha else None


def estado_fonte(g):
    """None (sem campanha ou antes do desfecho), "escura", "limpando" ou "limpa"."""
    m = _missao(g)
    if not m or not m.get("desfecho") or m.get("dia_desfecho") is None:
        return None
    dias = g.dia - m["dia_desfecho"]
    for ate, estado in FONTE[m["desfecho"]]:
        if dias < ate:
            return estado
    return "limpa"


def marta_de_pe(g):
    """Marta adoeceu com a vila; levanta quando a água limpa."""
    return estado_fonte(g) == "limpa"


def no_vau(g):
    return bool(_missao(g)) and g.loc.get("chave") == "vau_do_turvo"


# ------------------------------------------------------------------ a curandeira
# Quem atende na cabana da curandeira do Vau. O serviço e as regras são os de sempre (Servicos.curandeiro); muda quem
# está atrás do balcão e o que diz. Marta ajudou o herói no passado: a frase da primeira vez lembra isso.

def atendente(g):
    """{"quem", "fala", "fechado"} da curandeira do Vau, ou None (fora do Vau da campanha: a curandeira de sempre)."""
    if not no_vau(g):
        return None
    m = _missao(g)
    if marta_de_pe(g):
        fala = ("Marta, ainda magra da febre, arregaça as mangas. \"Pita me contou o que você fez lá embaixo. Senta.\""
                if m.get("desfecho") == "descansada" else
                "Marta, ainda magra da febre, arregaça as mangas. \"Aquela noite quase me levou. Senta, deixa eu ver.\"")
        return {"quem": "Marta, a curandeira", "fala": fala,
                "fechado": "Marta ergue os olhos das ervas e sorri, cansada. \"Nada para tratar em você hoje.\""}
    piora = estado_fonte(g) == "escura"
    return {"quem": "Pita, a aprendiz de Marta",
            "fala": ("Pita, uma menina de uns catorze anos, ferve água para os doentes. \"A Marta piorou de noite. "
                     "Mas eu sei o que ela faria. Deixa eu ver isso.\"" if piora else
                     "Pita, uma menina de uns catorze anos, mói ervas no lugar de Marta, que está de cama. \"Eu sei o "
                     "que ela faria. Deixa eu ver isso.\""),
            "fechado": "Pita ergue os olhos das ervas. \"A Marta está de cama. Se precisar de cuidados, sou eu que "
                       "atendo.\""}


# ------------------------------------------------------------------ a frase da vila
# A frase que a vila mostra ao chegar e quando o tempo passa. Depois do desfecho, a do Vau fala da Fonte. A diferença
# entre os desfechos fica pequena e à vista: quem deu descanso a Ilse encontra a fita amarrada na pedra da fonte; quem
# a destruiu encontra a vila que não fala da capela.

FRASES = {
    ("descansada", "limpando"): "Na Fonte Nova, o lodo assentou e a água corre mais clara. \"Ninguém piorou esta "
                                "noite\", diz uma mulher enchendo o balde. \"A primeira desde o verão.\"",
    ("descansada", "limpa"): "A Fonte Nova corre clara. Alguém amarrou uma fita desbotada na pedra da fonte, e ninguém "
                             "tira.",
    ("destruida", "escura"): "A Fonte Nova corre escura, quase preta. Ninguém enche balde: Pita ferve água do rio para "
                             "os doentes. \"Pioraram todos de noite\", diz alguém na porta da taverna.",
    ("destruida", "limpando"): "A Fonte Nova clareia devagar. \"O pior passou\", diz o homem da ponte, \"mas aquela "
                               "noite foi feia.\"",
    ("destruida", "limpa"): "A Fonte Nova corre clara de novo. As crianças voltam à praça; ninguém fala da capela.",
}


def frase_da_vila(g):
    """A frase de ambiente do Vau depois do desfecho, ou None (a de sempre)."""
    if not no_vau(g):
        return None
    estado = estado_fonte(g)
    return FRASES.get((_missao(g)["desfecho"], estado)) if estado else None


# ------------------------------------------------------------------ o Diário
FONTE_DIARIO = {
    "escura": "A Fonte Nova corre escura: a noite depois do confronto foi pior para os doentes.",
    "limpando": "A Fonte Nova está limpando.",
    "limpa": "A Fonte Nova está limpa, e Marta voltou a atender.",
}


def fonte_no_diario(g):
    estado = estado_fonte(g)
    return FONTE_DIARIO.get(estado) if estado else None
