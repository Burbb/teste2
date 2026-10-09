"""Golpes, estados e mortes: a conta de um golpe (esquiva, traços, estados, crítico, defesa), o que fica
depois dele (aplicar um estado, queimadura em camadas) e o que acontece quando alguém cai."""

from ..grimorio import chance_critico, mult_critico
from ..modificadores import disparar, mod, mult, nomes
from ..estados import ESTADOS, NOMES, NOMES as NOMES_EFEITOS, no_golpe
from ..dados import CLIMAS
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
        """reacao: um golpe que sai sozinho, fora da vez de quem o dá (o contra-ataque): a tela põe o nome dele na
        cabeça de quem golpeia, como põe o das habilidades."""
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
        if u is self.j and dano:
            roubo = mod(u, "roubo_vida")
            if roubo:
                # arredonda (e pelo menos 1): truncar zerava o roubo dos golpes pequenos e a build parecia não funcionar
                self.curou(u, u.curar(max(1, round(dano * roubo))), "roubo", fonte=alvo,
                           rotulo=(nomes(u, "roubo_vida") or ["Roubo de vida"])[0])
        espinhos = mod(alvo, "espinhos") if alvo is self.j and dano and alcance == "corpo" and u in self.inimigos else 0
        if espinhos and u.vivo:
            u.hp = max(0, u.hp - espinhos)
            self.lance("golpe", de=None, em=self.uid(u), dano=espinhos, crit=False, elemento="fisico", alcance="corpo",
                       absorvido=0, eficacia=None, rotulo="Espinhos", hp=u.hp, max_hp=u.max_hp,
                       refletido=self.uid(alvo))
            self.detalhe(f"Espinhos ferem {u.nome}. ({espinhos})", "amarelo")
            if not u.vivo:
                self.ao_morrer(u, por=alvo)
        if alvo is self.j and alvo.vivo:
            disparar(self, alvo, "golpe_recebido", de=u, alcance=alcance, dano=dano)  # Martírio, Contra-ataque...
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
        if est["imune"] and est["imune"](alvo):
            self.detalhe(f"{self.nome(alvo)} não é afetad{'o' if alvo.g == 'm' else 'a'} ({NOMES_EFEITOS[efeito]}).",
                         "cinza")
            return False
        if est["resiste"] and est["resiste"](self, alvo):
            self.detalhe(f"{self.nome(alvo)} resiste ao {'atordoamento' if efeito == 'atordoado' else est['nome']}!", "cinza")
            return False
        guarda = next((k for k in alvo.efeitos if efeito in ESTADOS.get(k, {}).get("protege", ())), None)
        if guarda:
            self.lance("efeito_negado", em=self.uid(alvo), efeito=efeito, por=guarda, rotulo=NOMES[guarda])
            self.detalhe(f"{self.nome(alvo)} acabou de se soltar e não fica {rotulo or NOMES_EFEITOS[efeito]} de novo.",
                         "cinza")
            return False
        atual = alvo.efeitos.get(efeito)
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
        self.detalhe(f"{self.nome(alvo)} fica {rotulo or NOMES_EFEITOS[efeito]}!", "magenta")
        return True

    def ao_morrer(self, c, por=None, tipo=None):
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
        if por is not j:
            return
        if mod(j, "vida_abate"):
            j.curar(mod(j, "vida_abate"))
        disparar(self, j, "abate", alvo=c, tipo=tipo)  # Frenesi, Assassino, Coração Ardente...
