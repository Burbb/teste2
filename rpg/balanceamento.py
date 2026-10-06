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

# Queimadura (mago): uma camada arde pouco; o forte é acumular até MAX_CHAMAS e detonar com a Combustão.
MAX_CHAMAS = 3
QUEIMADURA_POR_PODER = 0.12
QUEIMADURA_PIROMANTE = 1.25
QUEIMADURA_BRASAS = 0.2       # por ponto do talento Brasas Eternas
COMBUSTAO_BASE = 1.6          # o que ainda arderia × (1,6 + 0,2 por camada)
COMBUSTAO_POR_CAMADA = 0.2

# ---------------------------------------------------------------- arqueiro
FLECHAS_INICIAIS = 20
ALJAVA = 30                   # flechas que cabem
ALJAVA_POR_TALENTO = 5        # Aljava Funda
RECOLHER_FLECHA = 0.35        # chance de recolher cada flecha depois da vitória
RECOLHER_FLECHA_TALENTO = 0.15
PRECO_FLECHAS = 7             # feixe de 5

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
