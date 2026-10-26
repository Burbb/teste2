"""Os atributos do personagem (etapa 4, a integração do combate; roadmapIDEIAS/25, seções 3.7–3.10, e 26).

Seis atributos de combate e a Presença, que só vale fora da luta. Cada ponto soma um pouco, sem degrau: não há
desbloqueio por atingir um número. Os atributos entram nos valores derivados de sempre (Ataque, Poder, Vida, recurso,
Agilidade da ordem), que continuam sendo a conta do golpe; a Percepção soma no crítico e a Vontade dá a Tenacidade.

Números provisórios (26, "Escolhas operacionais"):
    Força         +1 de Ataque (a potência física) por ponto
    Intelecto     +1 de Poder (a potência arcana e elemental) por ponto
    Constituição  +4 de vida máxima por ponto
    Vontade       +3 de recurso máximo e +4% de Tenacidade por ponto (teto 40%)
    Percepção     +1% de crítico por ponto
    Agilidade     +1 de Agilidade: a ordem dos turnos e a esquiva de sempre (1,2% por ponto, até 40%); não dá dano
    Presença      só os testes de Carisma, fora da luta
"""

ATRIBUTOS = ("forca", "agilidade", "constituicao", "intelecto", "percepcao", "vontade")
NOMES = {"forca": "Força", "agilidade": "Agilidade", "constituicao": "Constituição", "intelecto": "Intelecto",
         "percepcao": "Percepção", "vontade": "Vontade", "presenca": "Presença"}
SIGLAS = {"forca": "FOR", "agilidade": "AGI", "constituicao": "CON", "intelecto": "INT", "percepcao": "PER",
          "vontade": "VON", "presenca": "PRE"}
FUNCAO = {"forca": "+1 de Ataque (dano físico)", "agilidade": "+1 de Agilidade (esquiva, ordem dos turnos e fuga)",
          "constituicao": "+4 de vida máxima", "intelecto": "+1 de Poder (dano mágico)",
          "percepcao": "+1% de crítico", "vontade": "+3 de recurso máximo e +4% de Tenacidade",
          "presenca": "convencer, negociar e intimidar, fora da luta"}

# Os 24 pontos iniciais de cada classe (a Presença começa em 3 para todas).
INICIAIS = {
    "guerreiro": dict(forca=6, agilidade=3, constituicao=5, intelecto=2, percepcao=3, vontade=5),
    # o arqueiro com mais Percepção que Agilidade: o crítico dele vem dela (antes vinha da Agilidade)
    "arqueiro": dict(forca=5, agilidade=6, constituicao=3, intelecto=2, percepcao=6, vontade=2),
    "mago": dict(forca=1, agilidade=4, constituicao=3, intelecto=9, percepcao=3, vontade=4),
}
PRESENCA_INICIAL = 3
PONTOS_POR_NIVEL = 2
PRESENCA_A_CADA = 3          # +1 de Presença a cada 3 níveis, sozinha
ATRIBUTO_MAX = 20

POR_PONTO = {"forca": ("atk", 1.0), "intelecto": ("poder", 1.0), "constituicao": ("max_hp", 4.0),
             "vontade": ("max_rec", 3.0), "agilidade": ("agi", 1.0)}
CRITICO_POR_PONTO = 0.01
TENACIDADE_POR_PONTO, TENACIDADE_TETO = 0.04, 0.40

# Para quem distribui sozinho (o robô dos testes, a migração de um save antigo): a ordem de preferência da classe.
PREFERENCIA = {
    "guerreiro": ("forca", "constituicao", "vontade", "forca", "constituicao", "percepcao"),
    "arqueiro": ("percepcao", "forca", "agilidade", "constituicao", "percepcao", "forca"),
    "mago": ("intelecto", "vontade", "constituicao", "intelecto", "percepcao", "intelecto"),
}


def iniciais(classe):
    return dict(INICIAIS[classe])


def de(u):
    """Os atributos de um combatente (o herói os tem; companheiros e inimigos, os do catálogo ou nenhum)."""
    return getattr(u, "atributos", None) or {}


def contribuicao(u):
    """O que os atributos somam aos valores derivados: {stat: valor}."""
    atr = de(u)
    soma = {}
    for a, (stat, k) in POR_PONTO.items():
        if a in atr:
            soma[stat] = soma.get(stat, 0) + atr[a] * k
    return soma


def critico(u):
    return de(u).get("percepcao", 0) * CRITICO_POR_PONTO


def tenacidade(u):
    """A chance de resistir a um controle (atordoar, congelar, prender), de 0 ao teto. Só aliados a têm por atributo;
    a dos inimigos continua nas regras deles (estados.py, `resiste`)."""
    v = de(u).get("vontade", getattr(u, "vontade", 0) or 0)
    return min(TENACIDADE_TETO, TENACIDADE_POR_PONTO * v)


def presenca(u):
    return getattr(u, "presenca", PRESENCA_INICIAL)


def distribuir_sozinho(classe, n, atuais, rng=None):
    """n pontos pela preferência da classe (ciclando); com rng, um pouco de variação (o robô)."""
    pref = list(PREFERENCIA[classe])
    escolhidos = []
    for i in range(n):
        a = rng.choice(pref) if rng else pref[(sum(atuais.values()) + i) % len(pref)]
        escolhidos.append(a)
    return escolhidos
