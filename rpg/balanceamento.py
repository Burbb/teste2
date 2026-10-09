"""Os números que decidem o quão difícil e generoso o jogo é, num lugar só.

Mudar algo aqui muda a jogabilidade: rode `python -m tests.gabarito --atualizar` depois, de propósito.
"""

# ---------------------------------------------------------------- progressão
XP_BASE = 30          # XP para sair do nível 1
NIVEL_ESPECIALIZACAO = 4      # a encruzilhada: a classe se ramifica numa especialização
XP_EXPOENTE = 1.62    # quanto a curva de XP acelera (era 1,52: do meio para o fim, o herói passava as regiões)


def xp_para_subir(nivel):
    """XP que falta para subir a partir de `nivel`."""
    return int(XP_BASE * nivel ** XP_EXPOENTE)


# XP de um inimigo conforme a diferença de nível (dele − seu): mais forte rende mais, mais fraco rende menos.
XP_POR_NIVEL_ACIMA = 0.08     # até +25%
XP_POR_NIVEL_ABAIXO = 0.15    # até −80%: quem fica caçando em região fraca sobe devagar
XP_MAX = 1.25
XP_MIN = 0.2


def fator_xp(diferenca):
    por_nivel = XP_POR_NIVEL_ACIMA if diferenca > 0 else XP_POR_NIVEL_ABAIXO
    return max(XP_MIN, min(XP_MAX, 1 + por_nivel * diferenca))


# ---------------------------------------------------------------- combate
# Dano geral, físico e mágico: o do herói (golpes e magias; a prévia do Grimório já mostra com isto) e o de
# todos os inimigos (comuns, guardiões e o antagonista: entra no Ataque e no Poder deles, que a ficha mostra).
DANO_HEROI = 0.9
DANO_INIMIGOS = 1.1
# O dano de quem luta ao seu lado: a comitiva (Odete, Morel, Yara) e o animal do Patrulheiro. Os servos do
# Necromante são a build dele e ficam de fora.
DANO_COMITIVA = 0.8
DANO_ANIMAL = 0.8
# Pegar o inimigo de surpresa: um turno livre só seu (a comitiva ainda se ajeita) e o primeiro golpe mais forte.
INICIATIVA_BONUS = 0.25

# Defesa: dano × P / (P + defesa × DEFESA_FATOR). P é quanto o golpe atravessa a armadura: 100 nos golpes do
# herói e dos aliados; nos dos inimigos, cresce com o nível deles. Assim a armadura que bastava no nível 3 não
# basta no 9: sem isso, a defesa do herói (nível + equipamento) anulava o crescimento do ataque inimigo.
DEFESA_FATOR = 6
DEFESA_PENETRACAO = 100
DEFESA_PENETRACAO_POR_NIVEL = 42  # por nível do inimigo acima do 1 (nível 1: 100; nível 11: 520)


def fator_defesa(defesa, nivel_inimigo=None):
    """Quanto do dano passa pela defesa. nivel_inimigo: o nível de quem bate, quando é um inimigo."""
    p = DEFESA_PENETRACAO + DEFESA_PENETRACAO_POR_NIVEL * (nivel_inimigo - 1 if nivel_inimigo else 0)
    return p / (p + defesa * DEFESA_FATOR)


ESQUIVA_POR_AGI = 0.012
ESQUIVA_MAX_AGI = 0.4         # teto da esquiva que vem só da Agilidade
MAX_ESQUIVA = 0.6             # teto com habilidades e clima: nem o mais ágil é intocável
CRITICO_BASE = 0.05
CRITICO_POR_AGI = 0.01
MAX_CRITICO = 0.6
NOITE_INIMIGOS = 1.1          # à noite, os monstros batem 10% mais forte...
NOITE_NIVEL = 1               # ... vêm um nível acima...
NOITE_GRUPO = 0.4             # ... e mais vezes em bando: chance de um a mais no grupo (no começo, sem passar do teto)
ESCURO_TESTES = 4             # sem luz: −4 nos testes de Percepção e Destreza

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

# ---------------------------------------------------------------- a curva: herói × inimigos × equipamento
# O jogo fica fácil quando o herói (com equipamento e talentos) cresce mais rápido que os inimigos.
# Os botões abaixo são essa corrida. Para medir o efeito de uma mudança:
#   python -m tests.equilibrio            robôs jogando, por classe e nível
#   python -m tests.replay <run>.jsonl    a sua partida refeita com os números de agora

# Inimigos comuns (chefes e guardiões à parte): mais duros que o herói sem equipamento, para o
# equipamento e os talentos serem vantagem e não atropelo. Multiplicam tudo, em todos os níveis (a base).
INIMIGO_VIDA = 1.45
INIMIGO_DANO = 1.4

# Quanto o inimigo cresce por nível acima do 1. Vida e poder (magia):
#   1 + VIDA_POR_NIVEL × (nível − 1) + CURVA × (nível − CURVA_DESDE)^CURVA_EXPOENTE
# A parte da CURVA é a que pesa no meio e no fim do jogo.
INIMIGO_VIDA_POR_NIVEL = 0.2
INIMIGO_CURVA = 0.08
INIMIGO_CURVA_DESDE = 3
INIMIGO_CURVA_EXPOENTE = 1.1
INIMIGO_ATK_BASE = 0.9            # o ataque físico da família × isto, antes do nível
INIMIGO_ATK_POR_NIVEL = 0.2       # ataque: 1 + 0,2 × (nível − 1) + ATK_CURVA × (nível − CURVA_DESDE)^CURVA_EXPOENTE
INIMIGO_ATK_CURVA = 0.16
INIMIGO_DEFESA_POR_NIVEL = 0.15
INIMIGO_AGI_A_CADA = 3            # +1 de agilidade a cada 3 níveis
INIMIGO_XP_POR_NIVEL = 0.3
INIMIGO_OURO_POR_NIVEL = 0.2

# Inimigos que curam (cultistas, o Profeta das Cinzas): vida do alvo × VIDA + Poder × PODER, e só uma vez a cada
# RECARGA turnos (sem isso, dois cultistas passavam a luta curando um ao outro).
INIMIGO_CURA_VIDA = 0.2
INIMIGO_CURA_PODER = 0.5
INIMIGO_CURA_RECARGA = 3

# Guardiões (chefes de região) e o antagonista usam a mesma escala de vida, com os próprios fatores.
GUARDIAO_VIDA = 0.9
GUARDIAO_ATK = 0.95
GUARDIAO_DEFESA_POR_NIVEL = 0.12
ANTAGONISTA_ATK = 0.85
ANTAGONISTA_NIVEL = 11
# Yara no caminho do Vazio: depois de cada vitória com ela, você perde esta fração da vida máxima.
YARA_VAZIO_CUSTO = 0.04

# Encontros. Nas regiões de nível até 2 (INICIO) e até 4 (MEIO), chance de o grupo ser um inimigo só; se não for,
# no máximo GRUPO_MAX_CEDO. Um inimigo sozinho contra você e um companheiro morre antes de fazer estrago.
GRUPO_SOZINHO_INICIO = 0.4
GRUPO_SOZINHO_MEIO = 0.15
GRUPO_MAX_CEDO = 3
# Comitiva: cada companheiro chama mais um inimigo com esta chance, e dá aos inimigos esta vida a mais.
COMITIVA_ATRAI = 0.35
COMITIVA_VIDA_INIMIGO = 0.3
COMITIVA_VIDA_CHEFE = 0.3

# Herói: cada classe e especialização declara o próprio crescimento por nível (`cresc` em classes.py);
# isto multiplica todos eles. 0,8 = o herói cresce 20% menos por nível.
HEROI_CRESCIMENTO = 1.0

# Companheiro animal do Patrulheiro: ao ser chamado e a cada nível do herói.
ANIMAL_VIDA_POR_NIVEL = 0.15      # na criação: vida × (1 + 0,15 × (nível − 1))
ANIMAL_ATK_POR_NIVEL = 0.2
ANIMAL_VIDA_SUBIR = 5             # a cada nível do herói
ANIMAL_ATK_SUBIR = 1.5

# Equipamento: força do item = ITEM_FORCA_BASE + ITEM_FORCA_POR_NIVEL × nível (× o material).
ITEM_FORCA_BASE = 1.5
ITEM_FORCA_POR_NIVEL = 0.75
ITEM_AFIXO_POR_NIVEL = 0.3        # afixos (do Urso, da Águia...): base × (1 + 0,3 × nível)
ITEM_AFIXO_FIXO_POR_NIVEL = 0.25  # crítico e roubo de vida: base + 0,25 × nível
ITEM_UNICO_FORCA = 1.3            # lendários: força × 1,3

# Ferimentos duradouros (como em Battle Brothers: arranhão não fere, golpe pesado sim). Em combate:
#   só golpe que tira pelo menos LIMIAR da vida máxima (ou crítico) pode deixar marca; a chance é
#   base + (gravidade − limiar) × fator + crítico + pouca vida, até o teto, e cai pela metade (POR_FERIDA) a cada
#   ferimento que você já carrega (quem está ferido se protege: três ou quatro de uma vez fica raro).
FERIMENTO_LIMIAR = 0.10
FERIMENTO_BASE = 0.03
FERIMENTO_GRAVIDADE = 0.45
FERIMENTO_CRITICO = 0.10
FERIMENTO_POUCA_VIDA = 0.08   # quando a vida está abaixo de 25%
FERIMENTO_TETO = 0.45
FERIMENTO_POR_FERIDA = 0.5
# Dano de eventos (queda, armadilha, briga...) também pode ferir: chance = gravidade × fator.
FERIMENTO_EVENTO = 1.2

# ---------------------------------------------------------------- arqueiro
FLECHAS_INICIAIS = 20
ALJAVA = 30                   # flechas que cabem
ALJAVA_POR_TALENTO = 5        # Aljava Funda
RECOLHER_FLECHA = 0.35        # chance de recolher cada flecha depois da vitória
RECOLHER_FLECHA_TALENTO = 0.15
PRECO_FLECHAS = 1.4           # por flecha (o antigo feixe de 5 custava 7); com a reputação, arredonda

# Vida por um fio: abaixo desta fração da vida máxima, a tela avisa (borda vermelha, batimento) e a barra pisca.
VIDA_POR_UM_FIO = 0.3

# ---------------------------------------------------------------- descanso e consumíveis
ACAMPAR_VIDA = 0.3
ACAMPAR_VIDA_RUIM = 0.18      # chuva, neve, tempestade
ACAMPAR_MANA = 0.5
ACAMPAR_FOLEGO = 0.75
TAVERNA_VIDA = 0.35            # uma cama não fecha ferida: vida de verdade, só o templo (pago)
EXAUSTO_VIDA = 0.15           # dormir no estábulo
EXAUSTO_RECURSO = 0.4
POCAO_VIDA = 0.35             # fração da vida máxima
TONICO = 0.5                  # fração do recurso máximo
BANDAGEM_VIDA = 8

# ---------------------------------------------------------------- mercado
# Quanto cada mercado tem de cada suprimento por dia (mínimo, máximo): sorteado por vila e dia, reabastece toda
# manhã. Comida e flechas também acabam, mas vêm em quantidade: são sobrevivência e munição.
ESTOQUE_MERCADO = {"tocha": (4, 8), "bandagem": (2, 5), "unguento": (0, 2), "pocao_vida": (1, 3), "tonico": (1, 2),
                   "antidoto": (1, 3), "bomba_fumaca": (0, 1), "pena_fenix": (0, 1),
                   "provisoes": (4, 8), "flechas": (15, 30)}

# ---------------------------------------------------------------- saque
# Equipamento depois de uma luta: chance base e a mais por inimigo de elite (afixo ou único). Luta comum dá mais
# vezes, mas quase sempre coisa comum (SAQUE_QUALIDADE_COMUM, no sorteio de raridade); o que é raro vem de elite,
# guardião e baú. Como nos jogos do gênero: muito saque comum, o bom é raro e tem de onde vir.
SAQUE_EQUIP = 0.15
SAQUE_EQUIP_ELITE = 0.2
SAQUE_QUALIDADE_COMUM = -1
# Baú Trancado: cai de guardião e criatura única (sempre), de elite (por inimigo) e, raramente, de luta comum.
# Abre numa vila ou à luz da fogueira: ouro, um ou dois suprimentos e, às vezes, um equipamento melhor.
BAU_ELITE = 0.12
BAU_COMUM = 0.03
BAU_OURO = (12, 24)           # sorteado, mais BAU_OURO_POR_NIVEL × nível (e o mundo é pobre: OURO_MUNDO)
BAU_OURO_POR_NIVEL = 5
BAU_EQUIP = 0.5               # chance de um equipamento (qualidade 1: mágico ou melhor mais vezes)

# ---------------------------------------------------------------- contratos
# O mundo é pobre: de todo ouro achado (saque, eventos), fica esta fração. O contrato já nasce com ela na conta,
# e paga exatamente o que o cartaz promete.
OURO_MUNDO = 0.75
# Peso de cada lugar no mural pela diferença entre o nível dele e o seu.
PESO_NIVEL_CONTRATO = {-1: 1.0, 0: 3.0, 1: 3.0, 2: 1.5}
CONTRATO_OURO_BASE = 10
CONTRATO_OURO_POR_NIVEL = 6
CONTRATO_XP_BASE = 8
CONTRATO_XP_FRACAO = 0.12     # do XP que falta para subir naquele nível
