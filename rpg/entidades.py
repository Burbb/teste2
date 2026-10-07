"""Combatentes: jogador, inimigos e aliados."""

from . import balanceamento as bal
from .classes import CLASSES, SPECS

STATS = ("max_hp", "atk", "defesa", "agi", "poder", "max_rec")
NOMES_STATS = {
    "max_hp": "Vida", "atk": "Ataque", "defesa": "Defesa", "agi": "Agilidade",
    "poder": "Poder", "max_rec": "Mana/Vigor/Foco", "roubo_vida": "roubo de vida", "critico": "chance de crítico",
    "espinhos": "Espinhos", "regen_vida": "Vida por turno", "vida_abate": "Vida por abate",
}
EFEITOS_NEGATIVOS = ("veneno", "sangramento", "queimadura", "atordoado", "enfraquecido", "maldito", "marcado")


def nome_stat(stat, recurso=None):
    """Nome de um atributo para o jogador; o recurso usa a palavra da classe (Mana, Vigor, Foco) quando conhecida."""
    if stat == "max_rec" and recurso:
        return recurso
    return NOMES_STATS[stat]


class Combatente:
    def __init__(self, nome, max_hp, atk, defesa, agi, poder, g="m"):
        self.nome = nome
        self.g = g
        self.max_hp = int(max_hp)
        self.hp = int(max_hp)
        self.atk = atk
        self.defesa = defesa
        self.agi = agi
        self.poder = poder
        self.efeitos = {}
        self.resist = {}
        self.tracos = []
        self.chefe = False
        self.jogador = False

    @property
    def vivo(self):
        return self.hp > 0

    def tal(self, talento):
        """Nível de um talento (só o jogador tem talentos)."""
        return 0

    def especial(self, chave):
        return 0

    def efeito(self, nome):
        return self.efeitos.get(nome)

    def aplicar(self, nome, turnos, valor=0):
        atual = self.efeitos.get(nome)
        if atual:
            atual["t"] = max(atual["t"], turnos)
            atual["v"] = max(atual["v"], valor)
        else:
            self.efeitos[nome] = {"t": turnos, "v": valor}

    def remover(self, nome):
        self.efeitos.pop(nome, None)

    def limpar_negativos(self):
        for nome in EFEITOS_NEGATIVOS:
            self.efeitos.pop(nome, None)

    def curar(self, n):
        n = max(0, min(int(n), self.max_hp - self.hp))
        self.hp += n
        return n


class Inimigo(Combatente):
    def __init__(self, nome, max_hp, atk, defesa, agi, poder, g="m"):
        super().__init__(nome, max_hp, atk, defesa, agi, poder, g)
        self.familia = None
        self.afixo = None
        self.unico = False
        self.desc = nome
        self.plural = nome
        self.nivel = 1
        self.habilidades = []
        self.xp = 0
        self.ouro = 0
        self.ataque = "fisico"
        self.carregando = None
        self.fases = []
        self.fase_atual = 0
        self.invoca = None
        self.roubado = 0
        self.fugiu = False
        self.chave = None  # identificador para guardiões / alvos de contrato / nêmesis


class Jogador(Combatente):
    def __init__(self, nome, classe):
        dados = CLASSES[classe]
        b = dados["base"]
        super().__init__(nome, b["max_hp"], b["atk"], b["defesa"], b["agi"], b["poder"])
        self.jogador = True
        self.classe = classe
        self.spec = None
        self.base = {k: float(b[k]) for k in STATS}
        self.nivel = 1
        self.xp = 0
        self.max_rec = b["max_rec"]
        self.rec = self.max_rec
        self.regen = b["regen"]
        self.ouro = 30
        self.flechas = bal.FLECHAS_INICIAIS if classe == "arqueiro" else 0
        self.consumiveis = {"pocao_vida": 2, "bandagem": 2, "tocha": 3}
        if classe == "mago":
            self.consumiveis["tonico"] = 1
        self.mochila = []
        self.equip = {s: None for s in ("cabeca", "amuleto", "armadura", "maos", "arma", "secundaria", "pernas", "pes",
                                        "anel1", "anel2")}
        self.habilidades = [h for (nv, h) in dados["habilidades"] if nv <= 1]
        self.companheiro = None
        self.reputacao = 0
        self.sigilos = []
        self.talentos = {}
        self.pontos_talento = 0
        self.provisoes = 4
        self.fome = 0
        self.ferimentos = []
        self.recalcular()
        self.hp = self.max_hp

    # ------------------------------------------------------------ atributos
    @property
    def nome_classe(self):
        if self.spec:
            return SPECS[self.spec]["nome"]
        return CLASSES[self.classe]["nome"]

    @property
    def nome_recurso(self):
        return CLASSES[self.classe]["recurso"]

    def xp_proximo(self):
        return bal.xp_para_subir(self.nivel)

    def tal(self, talento):
        return self.talentos.get(talento, 0)

    def especial(self, chave):
        """Soma de um atributo especial dos itens (roubo de vida, crítico, espinhos...)."""
        return sum(item["bonus"].get(chave, 0) for item in self.equip.values() if item)

    def recalcular(self):
        from .sobrevivencia import multiplicadores
        from .talentos import bonus_stats
        extras = bonus_stats(self)
        penal = multiplicadores(self)
        for stat in STATS:
            total = self.base[stat] + extras.get(stat, 0)
            for item in self.equip.values():
                if item:
                    total += item["bonus"].get(stat, 0)
            setattr(self, stat, max(1, int(round(total * penal.get(stat, 1.0)))))
        self.regen = CLASSES[self.classe]["base"]["regen"] + extras.get("regen", 0)
        self.hp = min(self.hp, self.max_hp)
        self.rec = min(self.rec, self.max_rec)

    def tem(self, item_id, qtd=1):
        return self.consumiveis.get(item_id, 0) >= qtd

    # ------------------------------------------------------------ salvar
    def para_dict(self):
        d = dict(vars(self))
        d["efeitos"] = {}
        return d

    @classmethod
    def de_dict(cls, d):
        obj = cls.__new__(cls)
        obj.__dict__.update(d)  # saves antigos já chegam aqui migrados (veja migracoes.py)
        return obj
