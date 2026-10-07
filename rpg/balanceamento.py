"""Os números que decidem o quão difícil e generoso o jogo é, num lugar só.

Mudar algo aqui muda a jogabilidade: rode `python -m tests.gabarito --atualizar` depois, de propósito.
"""

# ---------------------------------------------------------------- progressão
XP_BASE = 30          # XP para sair do nível 1
XP_EXPOENTE = 1.52    # quanto a curva de XP acelera


def xp_para_subir(nivel):
    """XP que falta para subir a partir de `nivel`."""
    return int(XP_BASE * nivel ** XP_EXPOENTE)


# ---------------------------------------------------------------- combate
DEFESA_FATOR = 6              # dano × 100 / (100 + defesa × 6)
ESQUIVA_POR_AGI = 0.012
ESQUIVA_MAX_AGI = 0.4         # teto da esquiva que vem só da Agilidade
MAX_ESQUIVA = 0.6             # teto com habilidades e clima: nem o mais ágil é intocável
CRITICO_BASE = 0.05
CRITICO_POR_AGI = 0.01
MAX_CRITICO = 0.6
NOITE_INIMIGOS = 1.1          # à noite, os monstros batem 10% mais forte

# Fôlego depois da luta: vigor e foco voltam pela metade; a mana do mago, um quinto.
FOLEGO_POS_LUTA = 0.5
MANA_POS_LUTA = 0.2
# O ataque básico que acerta devolve um pouco de mana, vigor ou foco: o golpe simples alimenta o próximo combo.
ATAQUE_RECURSO = 0.04         # do recurso máximo
ATAQUE_RECURSO_MIN = 2

# Queimadura (mago): uma camada arde pouco; o forte é acumular até MAX_CHAMAS e detonar com a Combustão.
MAX_CHAMAS = 3
QUEIMADURA_POR_PODER = 0.12
QUEIMADURA_PIROMANTE = 1.25
QUEIMADURA_BRASAS = 0.2       # por ponto do talento Brasas Eternas
COMBUSTAO_BASE = 1.6          # o que ainda arderia × (1,6 + 0,2 por camada)
COMBUSTAO_POR_CAMADA = 0.2

# Inimigos comuns (chefes e guardiões à parte): mais duros que o herói sem equipamento, para o
# equipamento e os talentos serem vantagem e não atropelo.
INIMIGO_VIDA = 1.15
INIMIGO_DANO = 1.1

# Ferimentos duradouros. Em combate, cada golpe tem chance de deixar marca:
#   base + gravidade × fator (gravidade = dano / vida máxima) + crítico + pouca vida, até o teto.
FERIMENTO_BASE = 0.015
FERIMENTO_GRAVIDADE = 0.45
FERIMENTO_CRITICO = 0.10
FERIMENTO_POUCA_VIDA = 0.08   # quando a vida está abaixo de 25%
FERIMENTO_TETO = 0.45
# Dano de eventos (queda, armadilha, briga...) também pode ferir: chance = gravidade × fator.
FERIMENTO_EVENTO = 1.2

# ---------------------------------------------------------------- arqueiro
FLECHAS_INICIAIS = 20
ALJAVA = 30                   # flechas que cabem
ALJAVA_POR_TALENTO = 5        # Aljava Funda
RECOLHER_FLECHA = 0.35        # chance de recolher cada flecha depois da vitória
RECOLHER_FLECHA_TALENTO = 0.15
PRECO_FLECHAS = 1.4           # por flecha (o antigo feixe de 5 custava 7); com a reputação, arredonda

# ---------------------------------------------------------------- descanso e consumíveis
ACAMPAR_VIDA = 0.3
ACAMPAR_VIDA_RUIM = 0.18      # chuva, neve, tempestade
ACAMPAR_MANA = 0.5
ACAMPAR_FOLEGO = 0.75
TAVERNA_VIDA = 0.65
EXAUSTO_VIDA = 0.15           # dormir no estábulo
EXAUSTO_RECURSO = 0.4
POCAO_VIDA = 0.35             # fração da vida máxima
TONICO = 0.5                  # fração do recurso máximo
BANDAGEM_VIDA = 8

# ---------------------------------------------------------------- contratos
# Peso de cada lugar no mural pela diferença entre o nível dele e o seu.
PESO_NIVEL_CONTRATO = {-1: 1.0, 0: 3.0, 1: 3.0, 2: 1.5}
CONTRATO_OURO_BASE = 10
CONTRATO_OURO_POR_NIVEL = 6
CONTRATO_XP_BASE = 8
CONTRATO_XP_FRACAO = 0.12     # do XP que falta para subir naquele nível
