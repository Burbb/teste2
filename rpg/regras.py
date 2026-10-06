"""Constantes e exceções que o jogo inteiro compartilha."""

from . import itens

VERSAO_SAVE = 1
NOMES_TESTE = {
    "forca": "Força", "destreza": "Destreza", "arcano": "Arcano",
    "percepcao": "Percepção", "vontade": "Vontade", "carisma": "Carisma",
}
NOMES_SLOT = itens.NOMES_SLOT
LIMITE_MOCHILA = 12
# Criaturas que não aparecem em regiões fracas demais (evita lutas impossíveis no começo).
PRECO_FLECHAS = 7  # feixe de 5
NIVEL_MIN_FAMILIA = {
    "bruxa_brejo": 2, "harpia": 2, "espectro": 3, "ent_jovem": 3, "cria_vazio": 3, "cao_infernal": 3,
    "golem": 4, "troll": 4, "grifo": 4, "abominacao": 6, "cavaleiro_sombrio": 6,
}
AMBIENTE_VILA = [
    "Portas pregadas com tábuas. Um X de cal marca as casas da peste.",
    "Uma mulher vende os sapatos do filho morto na praça.",
    "O sino da igreja não toca há meses. O padre foi o primeiro a fugir.",
    "Guardas magros e assustados vigiam a paliçada. Metade não tem botas.",
    "Crianças brincam de enterro. Elas conhecem bem as regras.",
    "Um corpo pende da forca da praça. A placa no pescoço diz: LADRÃO DE PÃO.",
    "O cheiro de fumaça, esterco e medo. Isto é o que sobrou de civilização.",
    "Um pregador grita que o fim chegou. Ninguém discute.",
]
NIVEL_MAXIMO = 12


class FimDeJogo(Exception):
    pass


class Derrota(Exception):
    """Interrompe a ação atual quando o herói cai (fora do modo hardcore)."""
