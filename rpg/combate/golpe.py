"""Golpes, estados e mortes: a conta de um golpe (esquiva, traços, estados, crítico, defesa), o que fica
depois dele (aplicar um estado, queimadura em camadas) e o que acontece quando alguém cai."""

import re

from ..grimorio import chance_critico, mult_critico
from ..modificadores import disparar, mod, mult, nomes
from ..estados import ESTADOS, NOMES, NOMES as NOMES_EFEITOS, no_golpe
from ..dados import CLIMAS
from ..forja import encanto, fracao
from ..forja.fracao import mod_pontos
from .. import sobrevivencia, telemetria
from .. import balanceamento as bal
from .eficacia import mult_tracos


class Golpes:
    MAX_CHAMAS = bal.MAX_CHAMAS  # o mesmo teto de camadas do catálogo (estados.py)

    def valor_queimadura(self, u):
        """Dano por turno de UMA camada de chamas. É pouco de propósito: o fogo do mago rende quando as
        camadas se acumulam (até 3) e a Combustão as detona de uma vez."""
        v = max(2, u.poder * bal.QUEIMADURA_POR_PODER)
        v *= mult(u, "queimadura_mult")
        return v * (1 + mod(u, "queimadura_dano"))

    def camadas(self, alvo):
        ef = alvo.efeito("queimadura")
        return ef.get("s", 1) if ef else 0

    def restante_queimadura(self, alvo):
        """Quanto a queimadura ainda causaria se ardesse até o fim (é o que a Combustão detona)."""
        ef = alvo.efeito("queimadura")
        return int(ef["v"]) * ef["t"] if ef else 0

    def duracao_queimadura(self, u):
        return 3 + mod(u, "queimadura_turnos")

    # ------------------------------------------------------------ dano
    def atacar(self, u, alvo, mult, tipo="fisico", alcance="corpo", stat="atk", crit_extra=0.0, bonus=0,
               rotulo=None, pode_esquivar=True, detalhar=True, reacao=False):
        """Um golpe, com as gravações da forja (rpg/forja/encanto.py): o Carrasco aumenta o dano contra o inimigo
        ferido; depois de acertar, a Brasa de quem bateu, e o Revide e a Geada de quem apanhou. Uma reação (o Revide, o
        contra-ataque) não dispara gravação nenhuma."""
        if not reacao and not getattr(self, "_encanto_secundario", False):
            mult *= encanto.mult_carrasco(self, u, alvo)
        dano = self.golpear(u, alvo, mult, tipo, alcance, stat, crit_extra, bonus, rotulo, pode_esquivar, detalhar, reacao)
        encanto.ao_golpear(self, u, alvo, dano, alcance, reacao, rotulo)
        return dano

    def golpear(self, u, alvo, mult, tipo="fisico", alcance="corpo", stat="atk", crit_extra=0.0, bonus=0,
                rotulo=None, pode_esquivar=True, detalhar=True, reacao=False):
        """A conta do golpe (sem as gravações). reacao: um golpe que sai sozinho, fora da vez de quem o dá (o
        contra-ataque): a tela põe o nome dele na cabeça de quem golpeia, como põe o das habilidades."""
        if alvo is None or not alvo.vivo:
            return 0
        reage = {"reacao": True} if reacao else {}
        prefixo = f"[{rotulo}] " if rotulo else ""
        quem = self.nome(u)
        # Os estados entram na conta pelo catálogo (estados.py, campo `golpe`), cada um na sua etapa.
        if pode_esquivar and not no_golpe(alvo, "sem_esquiva"):
            esq = min(bal.ESQUIVA_MAX_AGI, alvo.agi * bal.ESQUIVA_POR_AGI)
            for _, e, f in no_golpe(alvo, "esquiva"):
                esq += f(e["v"])
            esq += CLIMAS[self.g.clima].get("esquiva", 0)
            esq = min(bal.MAX_ESQUIVA, esq)
            if self.rng.random() < esq:
                self.lance("erro", de=self.uid(u), em=self.uid(alvo), motivo="esquiva", rotulo=rotulo, **reage)
                if detalhar:
                    self.detalhe(f"{prefixo}{quem} erra — {self.nome(alvo, True)} se esquiva!", "cinza")
                return 0
        eficacia = mult_tracos(alvo, tipo, alcance)
        if eficacia == 0:
            self.lance("erro", de=self.uid(u), em=self.uid(alvo), motivo="imune", rotulo=rotulo, **reage)
            self.detalhe(f"{prefixo}{self.nome(alvo)} é imune!", "cinza")
            return 0
        m = eficacia
        for _, e, f in no_golpe(u, "dano_causado"):
            m *= f(e["v"])
        ferido = mod(u, "dano_ferido") if u.jogador else 0
        if ferido:
            m *= 1 + ferido * (1 - u.hp / u.max_hp)
        if not u.jogador and u not in self.aliados and self.g.noite:
            m *= bal.NOITE_INIMIGOS
        clima = CLIMAS[self.g.clima].get("dano", {})
        m *= clima.get(tipo, 1)
        if alcance == "distancia":
            m *= clima.get("distancia", 1)
        for _, e, f in no_golpe(alvo, "dano_recebido"):
            m *= f(e["v"])
        fragil = alvo.efeito("fragilizado")
        if fragil and tipo != "fisico":  # só o dano mágico (estados.py)
            m *= 1 + fragil["v"]
        if getattr(alvo, "chave", None) and self.g.flag(f"fraqueza:{alvo.chave}"):
            m *= 1.25
        if u.jogador and self.g.mestre_caca(getattr(alvo, "familia", None)):
            m *= 1.1
        bonus_motivo = None  # um bônus que não é crítico, mas a tela anuncia (a iniciativa)
        if u.jogador:
            m *= 1 + mod(u, "dano_corpo" if alcance == "corpo" else "dano_distancia")
            m *= bal.DANO_HEROI
            if u.efeito("iniciativa"):  # pegou o inimigo de surpresa: o golpe do turno livre sai mais forte
                u.remover("iniciativa")
                m *= 1 + bal.INICIATIVA_BONUS
                bonus_motivo = "Iniciativa!"
        elif u is self.companheiro:
            m *= bal.DANO_ANIMAL
        elif getattr(u, "tipo", None) == "comitiva":
            m *= bal.DANO_COMITIVA

        fator_def = 1.0
        for _, e, f in no_golpe(alvo, "defesa"):
            fator_def *= f(e["v"])
        defesa = alvo.defesa * fator_def
        garantido = no_golpe(u, "critico_garantido")  # furtivo
        abertura = u.jogador and self.abertura
        self.abertura = self.abertura and not u.jogador
        chance_crit = chance_critico(u, crit_extra)  # a mesma conta que o Grimório e a ficha mostram
        crit = bool(garantido) or abertura or self.rng.random() < chance_crit
        # Crítico garantido diz de onde veio: sem isso, parece que a sorte ignora a chance da ficha.
        motivo_crit = (garantido[0][2] if garantido else self.motivo_abertura or "Iniciativa") if (garantido or abertura) else None
        base = getattr(u, stat) * mult + bonus
        inimigo = not u.jogador and u not in self.aliados
        dano = base * m * self.rng.uniform(0.85, 1.15) * bal.fator_defesa(defesa, u.nivel if inimigo else None)
        if crit:
            dano *= mult_critico(u, furtivo=bool(garantido))
        for k, _, _ in garantido:
            u.remover(k)
        for _, e, f in no_golpe(alvo, "dano_final"):
            dano *= f(e["v"])
        dano = max(1, round(dano))
        absorvido = 0
        for k, e, _ in no_golpe(alvo, "absorve"):
            parte = min(e["v"], dano)
            e["v"] -= parte
            dano -= parte
            absorvido += parte
            if e["v"] <= 0:
                alvo.remover(k)
        if alvo is self.j and dano >= alvo.hp:
            dano = disparar(self, alvo, "golpe_fatal", dano=dano, de=u)["dano"]  # Imortal...
        alvo.hp = max(0, alvo.hp - dano)
        telemetria.contabilizar_dano(self, u, alvo, dano, crit)

        txt = f"{prefixo}{quem} atinge {self.nome(alvo, True)}: {dano} de dano"
        if tipo != "fisico":
            txt += f" ({tipo})"
        if crit:
            txt = (f"CRÍTICO ({motivo_crit})! " if motivo_crit else "CRÍTICO! ") + txt
        if bonus_motivo:
            txt = f"{bonus_motivo} " + txt
        if absorvido:
            txt += f" [{absorvido} absorvido]"
        if eficacia >= 1.3:
            txt += " — super eficaz!"
        elif eficacia <= 0.7:
            txt += " — pouco eficaz."
        defensor = alvo is self.j or alvo in self.aliados
        self.lance("golpe", de=self.uid(u), em=self.uid(alvo), dano=dano, crit=crit, crit_motivo=motivo_crit, elemento=tipo,
                   alcance=alcance, absorvido=absorvido, eficacia="super" if eficacia >= 1.3 else "pouco" if eficacia <= 0.7 else None,
                   rotulo=rotulo, hp=max(0, alvo.hp), max_hp=alvo.max_hp, **reage,
                   **({"bonus_motivo": bonus_motivo} if bonus_motivo else {}), **self.peso_do_golpe(alvo))
        if detalhar:
            self.detalhe(txt, "vermelho" if defensor else "amarelo")
        else:
            self.ui.atualizar()
        if (u is self.j or veste(u)) and dano:  # o herói e a comitiva: as peças dela valem como as suas
            roubo = mod(u, "roubo_vida")
            if roubo:
                # arredonda (e pelo menos 1): truncar zerava o roubo dos golpes pequenos e a build parecia não funcionar
                self.curou(u, u.curar(max(1, round(dano * roubo))), "roubo", fonte=alvo,
                           rotulo=(nomes(u, "roubo_vida") or ["Roubo de vida"])[0])
        espinhos = (mod_pontos(alvo, "espinhos") if (alvo is self.j or veste(alvo)) and dano and alcance == "corpo"
                    and u in self.inimigos else 0)
        if espinhos and u.vivo:
            u.hp = max(0, u.hp - espinhos)
            self.lance("golpe", de=None, em=self.uid(u), dano=espinhos, crit=False, elemento="fisico", alcance="corpo",
                       absorvido=0, eficacia=None, rotulo="Espinhos", hp=u.hp, max_hp=u.max_hp,
                       refletido=self.uid(alvo))
            self.detalhe(f"Espinhos ferem {u.nome}. ({espinhos})", "amarelo")
            if not u.vivo:
                self.ao_morrer(u, por=alvo)
        if (alvo is self.j or veste(alvo)) and alvo.vivo:
            disparar(self, alvo, "golpe_recebido", de=u, alcance=alcance, dano=dano)  # Martírio, Contra-ataque...
        ret = alvo.efeito("retaliando") if alvo.vivo and not reacao else None
        if ret and dano and alcance == "corpo" and u in self.inimigos and u.vivo:  # o Contragolpe (estados.py)
            self.atacar(alvo, u, ret["v"], rotulo="Contragolpe", pode_esquivar=False, reacao=True)
        if alvo is self.j and dano:
            sobrevivencia.talvez_ferir(self.g, dano, tipo, crit, u)
        if not alvo.vivo:
            self.ao_morrer(alvo, por=u, tipo=tipo)
        return dano

    def peso_do_golpe(self, alvo):
        """O que o golpe significa para a luta (a tela dá o peso): derrubou alguém (abate) e, se era o último
        inimigo de pé, encerrou a luta (final). Só vai no lance quando é verdade."""
        if alvo.vivo:
            return {}
        if alvo in self.inimigos and not self.inimigos_vivos():
            return {"abate": True, "final": True}
        return {"abate": True}

    def dano_previsto(self, u, alvo):
        """Quanto o ataque comum de `u` tira de `alvo`, em média (sem sorteio, sem crítico): o juízo dos inimigos.
        Segue as etapas de atacar() que não dependem de sorte: estados de quem bate e de quem apanha, e a defesa."""
        magico = getattr(u, "ataque", "fisico") != "fisico" and u.poder > u.atk
        dano = u.poder if magico else u.atk
        inimigo = not u.jogador and u not in self.aliados
        if inimigo and self.g.noite:
            dano *= bal.NOITE_INIMIGOS
        for _, e, f in no_golpe(u, "dano_causado"):
            dano *= f(e["v"])
        for _, e, f in no_golpe(alvo, "dano_recebido"):
            dano *= f(e["v"])
        fator_def = 1.0
        for _, e, f in no_golpe(alvo, "defesa"):
            fator_def *= f(e["v"])
        dano *= bal.fator_defesa(alvo.defesa * fator_def, u.nivel if inimigo else None)
        for _, e, f in no_golpe(alvo, "dano_final"):
            dano *= f(e["v"])
        return dano - sum(e["v"] for _, e, _ in no_golpe(alvo, "absorve"))

    def aplicar(self, alvo, efeito, turnos, valor=0, chance=1.0, rotulo=None, acumula=False):
        if not alvo.vivo:
            return False
        if chance < 1 and self.rng.random() >= chance:
            return False
        est = ESTADOS[efeito]
        if est["perde_turno"] and (alvo is self.j or alvo in self.aliados):
            # a Tenacidade (atributos.py): uma chance, com teto, de o aliado resistir ao controle; um sorteio só
            from .. import atributos
            ten = atributos.tenacidade(alvo)
            if ten and self.rng.random() < ten:
                self.lance("efeito_negado", em=self.uid(alvo), efeito=efeito, por="tenacidade",
                           rotulo=f"resistiu ({round(ten * 100)}%)")
                self.detalhe(f"{self.nome(alvo)} resiste pela Tenacidade "
                             f"({round(ten * 100)}% de chance).", "cinza")
                return False
        if est["imune"] and est["imune"](alvo):  # o motivo real vai junto, para a tela mostrar no alvo
            self.lance("efeito_negado", em=self.uid(alvo), efeito=efeito, por="imune", rotulo="imune")
            self.detalhe(f"{self.nome(alvo)} não é afetad{'o' if alvo.g == 'm' else 'a'} ({NOMES_EFEITOS[efeito]}).",
                         "cinza")
            return False
        if est["resiste"] and est["resiste"](self, alvo):
            self.lance("efeito_negado", em=self.uid(alvo), efeito=efeito, por="resiste", rotulo="resistiu")
            self.detalhe(f"{self.nome(alvo)} resiste ao {'atordoamento' if efeito == 'atordoado' else est['nome']}!", "cinza")
            return False
        guarda = next((k for k in alvo.efeitos if efeito in ESTADOS.get(k, {}).get("protege", ())), None)
        if guarda:
            self.lance("efeito_negado", em=self.uid(alvo), efeito=efeito, por=guarda, rotulo=NOMES[guarda])
            self.detalhe(f"{self.nome(alvo)} acabou de se soltar e não fica {rotulo or NOMES_EFEITOS[efeito]} de novo.",
                         "cinza")
            return False
        atual = alvo.efeitos.get(efeito)
        if est["perde_turno"] and atual and atual["t"] >= turnos:
            # Travar de novo quem já está travado não soma: ele perde o próximo turno uma vez só (e depois fica firme).
            # A tela diz isso, em vez de anunciar um congelamento novo que não muda nada.
            ja = atual.get("r") or NOMES_EFEITOS[efeito]
            self.lance("efeito", em=self.uid(alvo), efeito=efeito, rotulo=f"já {ja}")
            self.detalhe(f"{self.nome(alvo)} já está {_no_genero(ja, alvo)}: não soma, perde só o próximo turno.", "cinza")
            return True
        if acumula and atual and est["camadas"]:
            # Mais uma camada: o dano por turno soma (até o teto) e a duração se renova.
            s = min(est["camadas"], atual.get("s", 1) + 1)
            base = max(atual.get("b", atual["v"]), valor)
            atual.update(s=s, b=base, v=base * s, t=max(atual["t"], turnos))
            rotulo = est["rotulo_camadas"].format(s=s)
        else:
            alvo.aplicar(efeito, turnos, valor)
            if acumula and est["camadas"]:
                alvo.efeitos[efeito].setdefault("s", 1)
                alvo.efeitos[efeito].setdefault("b", valor)
        if rotulo:
            alvo.efeitos[efeito]["r"] = rotulo
        self.lance("efeito", em=self.uid(alvo), efeito=efeito, rotulo=rotulo or NOMES_EFEITOS[efeito])
        self.detalhe(f"{self.nome(alvo)} fica {_no_genero(rotulo or NOMES_EFEITOS[efeito], alvo)}!", "magenta")
        return True

    def ao_morrer(self, c, por=None, tipo=None):
        fracao.tique(por)  # a vida por abate de peças reforçadas acumula a fração (forja/fracao.py)
        if por is not self.j:
            fracao.tique(self.j)
        if c is self.j:
            return
        if c in self.aliados:
            self.dizer(f"{c.nome} cai!", "vermelho")
            return
        if c in self.mortos:
            return
        self.mortos.append(c)
        o = "o" if c.g == "m" else "a"
        self.dizer(self.rng.choice([
            f"{c.nome} desaba sem um som.", f"{c.nome} cai num jorro de sangue escuro.",
            f"{c.nome} se contorce no chão e fica imóvel.", f"{c.nome} é derrubad{o} e não se levanta mais.",
            f"{c.nome} solta um último grito gorgolejante.",
        ]), "verde+negrito")
        j = self.j
        disparar(self, j, "morte", alvo=c, por=por, tipo=tipo)  # Colheita, Rei dos Mortos...
        encanto.na_morte(self, c, por)  # o Eco gravado de quem derrubou
        if por is not j:
            if veste(por) and mod_pontos(por, "vida_abate"):  # a peça de um companheiro: a vida é de quem derrubou
                self.curou(por, por.curar(mod_pontos(por, "vida_abate")),
                           rotulo=(nomes(por, "vida_abate") or ["Vida por abate"])[0], conta=False)
            return
        if mod_pontos(j, "vida_abate"):  # a tela mostra de onde veio a vida (antes, a barra só subia no redesenho)
            self.curou(j, j.curar(mod_pontos(j, "vida_abate")), rotulo=(nomes(j, "vida_abate") or ["Vida por abate"])[0],
                       conta=False)
        disparar(self, j, "abate", alvo=c, tipo=tipo)  # Frenesi, Assassino, Coração Ardente...


def veste(u):
    """Um companheiro da comitiva: as peças dele (ficha.py) valem na luta como as do herói."""
    return getattr(u, "tipo", None) == "comitiva"


def _no_genero(rotulo, u):
    """O estado concordando com quem o recebe: "envenenado" vira "envenenada" para Odette e Yara (o particípio no
    começo do rótulo: "presa na teia", "congelada")."""
    if getattr(u, "g", "m") != "f":
        return rotulo
    return re.sub(r"^(\w+?)(ad|id|es)o\b", r"\1\2a", rotulo)
