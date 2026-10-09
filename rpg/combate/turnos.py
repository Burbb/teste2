"""A vez dos outros: a comitiva, o animal e os servos; os inimigos, com o juízo do que faz sentido agora."""

from ..modificadores import mod
from ..inimigos import HABS, HABS_INIMIGO, ROTULOS_HABS_INIMIGO
from .. import comitiva


class TurnosDosOutros:
    # ------------------------------------------------------------ aliados e inimigos
    def fase_aliados(self):
        for a in list(self.aliados):
            if not a.vivo or not self.inimigos_vivos():
                continue
            if self.processar_efeitos(a):
                continue
            if a.tipo == "comitiva":
                with self.agindo(a):
                    comitiva.agir(self, a)
                continue
            ataques = 1 + mod(self.j, "ataques_fera") if a is self.companheiro else 1
            for _ in range(ataques):
                if not self.inimigos_vivos():
                    break
                alvo = self.rng.choice(self.inimigos_vivos())
                with self.agindo(a, alvo=alvo):
                    dano = self.atacar(a, alvo, 1.0, alcance=a.alcance, crit_extra=a.crit, rotulo=a.nome)
                    if dano and a.tipo == "lobo":
                        self.aplicar(alvo, "sangramento", 2, valor=max(1, a.atk * 0.3), chance=0.3)
                    elif dano and a.tipo == "urso":
                        self.aplicar(alvo, "atordoado", 1, chance=0.15)

    def fase_inimigos(self, apenas=None):
        for e in list(self.inimigos):
            if apenas is not None and e is not apenas:
                continue
            if not e.vivo or not self.j.vivo:
                continue
            if self.processar_efeitos(e):
                if e.vivo and e.carregando:  # atordoado no meio da preparação: o golpe devastador se perde
                    e.carregando = None
                    self.lance("atordoado", em=self.uid(e), rotulo="golpe interrompido!")
                    self.dizer(f"Atordoad{'o' if e.g == 'm' else 'a'}, {self.nome(e, True)} perde o golpe que "
                               "preparava!", "verde+negrito")
                continue
            self.checar_fase(e)
            self.agir_inimigo(e)

    def checar_fase(self, e):
        while e.fase_atual < len(e.fases) and e.hp <= e.max_hp * e.fases[e.fase_atual]["limiar"]:
            f = e.fases[e.fase_atual]
            e.fase_atual += 1
            self.ui.separador("vermelho")
            self.lance("fase", em=self.uid(e))
            self.dizer(f["texto"], "vermelho+negrito")
            e.atk *= f.get("atk", 1)
            e.poder *= f.get("poder", 1)
            e.defesa *= f.get("defesa", 1)
            e.habilidades += [h for h in f.get("habs", []) if h not in e.habilidades]
            e.tracos += [t for t in f.get("tracos", []) if t not in e.tracos]
            if e.invoca:
                HABS_INIMIGO["invocar"](self, e, None)

    def escolher_alvo_inimigo(self, e=None):
        aliados = [a for a in self.aliados if a.vivo]
        provocador = next((a for a in aliados if a.efeito("provocando")), None)
        if provocador and (e is None or not e.chefe or self.rng.random() < 0.5):
            return provocador  # o urso de pé, rugindo: todo mundo olha para ele (chefes, só às vezes)
        tanque = comitiva.alvo_inimigo(self, aliados, e)
        if tanque:
            return tanque
        if aliados:
            chance = 0.45 if any(a.tipo == "urso" for a in aliados) else 0.25
            if e is not None and e.chefe:
                chance = 0.15  # chefes sabem quem está por trás dos servos
            if self.rng.random() < chance:
                return self.rng.choice(aliados)
        return self.j

    def agir_inimigo(self, e):
        alvo = self.escolher_alvo_inimigo(e)
        if e.carregando:
            c = e.carregando
            e.carregando = None
            with self.agindo(e, c["rotulo"], alvo, hab="carregado"):
                self.atacar(e, alvo, c["mult"], rotulo=c["rotulo"])
            return
        if e.habilidades and self.rng.random() < (0.45 if e.chefe else 0.35):
            # Só o que faz sentido agora (estados.py/inimigos.py: `quando`); e com o alvo a um golpe da morte,
            # só o que fere: ninguém uiva para o bando quando pode acabar a luta.
            uteis = [h for h in e.habilidades if HABS[h]["quando"](self, e, alvo)]
            if alvo.hp <= self.dano_previsto(e, alvo):
                uteis = [h for h in uteis if HABS[h]["golpe"]]
            if uteis:
                h = self.rng.choice(uteis)
                with self.agindo(e, ROTULOS_HABS_INIMIGO.get(h), alvo, area=h == "varredura", hab=h,
                                 anim=HABS[h]["anim"]):
                    if HABS_INIMIGO[h](self, e, alvo) is not False:
                        return
        magico = e.ataque != "fisico" and e.poder > e.atk
        with self.agindo(e, None, alvo, hab="ataque"):
            self.atacar(e, alvo, 1.0, tipo=e.ataque if magico else "fisico",
                        alcance="distancia" if magico else "corpo", stat="poder" if magico else "atk")
