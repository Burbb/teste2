"""A vez dos outros: a comitiva, o animal e os servos; os inimigos, com o juízo do que faz sentido agora."""

from ..modificadores import mod
from ..inimigos import HABS, HABS_INIMIGO, ROTULOS_HABS_INIMIGO
from .. import comitiva


class TurnosDosOutros:
    # ------------------------------------------------------------ aliados e inimigos (cada um na sua vez da ordem)
    def vez_aliado(self, a):
        """A vez de quem luta do seu lado. A comitiva age por escolha sua (heroi.vez_comitiva); o animal e os servos,
        sozinhos (o controle deles é decisão separada: roadmapIDEIAS/25, 3.4). Caído, a vez passa."""
        if not a.vivo:
            if a.tipo == "comitiva":
                self.lance("pula", de=self.uid(a), rotulo="caído")
            return
        if not self.inimigos_vivos() or self.processar_efeitos(a):
            return
        if a.tipo == "comitiva":
            self.vez_comitiva(a)
            return
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

    def vez_inimigo(self, e):
        self.checar_limiares()  # o momento de um piso vem antes de qualquer inimigo agir
        if not e.vivo or e.fugiu or not self.j.vivo:
            return
        if self.processar_efeitos(e):
            if e.vivo and e.carregando:  # atordoado no meio da preparação: o golpe devastador se perde
                e.carregando = None
                self.lance("atordoado", em=self.uid(e), rotulo="golpe interrompido!")
                self.dizer(f"Atordoad{'o' if e.g == 'm' else 'a'}, {self.nome(e, True)} perde o golpe que "
                           "preparava!", "verde+negrito")
            return
        self.checar_limiares()  # o efeito periódico do começo da vez pode tê-la levado ao piso
        if not e.vivo:
            return
        self.checar_fase(e)
        self.agir_inimigo(e)

    def fase_inimigos(self, apenas=None):
        """Os inimigos, em sequência (a emboscada: o mais rápido age antes de a ordem começar)."""
        for e in list(self.inimigos):
            if apenas is not None and e is not apenas:
                continue
            self.vez_inimigo(e)

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

    def redirecionar(self, alvo):
        """Quem recebe o golpe mirado em `alvo`: o protetor, se o alvo está Protegido e ele está de pé (Proteger)."""
        p = alvo.efeito("protegido") if alvo else None
        por = p.get("por") if p else None
        if por is not None and por.vivo and por is not alvo:
            self.detalhe(f"{self.nome(por)} entra na frente de {self.nome(alvo, True)}.", "ciano")
            return por
        return alvo

    def agir_inimigo(self, e):
        alvo = self.redirecionar(self.escolher_alvo_inimigo(e))
        if e.carregando:
            c = e.carregando
            e.carregando = None
            with self.agindo(e, c["rotulo"], alvo, hab="carregado"):
                self.atacar(e, alvo, c["mult"], rotulo=c["rotulo"])
            return
        # A variante que abre a luta com uma habilidade (só a campanha põe: missoes._que_prepara, o golpe preparado da
        # capela): na primeira vez em que ela faz sentido, sem sorteio; depois, o sorteio de sempre. Com o alvo a um
        # golpe da morte, espera, como as outras que não ferem.
        abre = getattr(e, "abre_com", None)
        if abre and HABS[abre]["quando"](self, e, alvo) and (HABS[abre]["golpe"] or alvo.hp > self.dano_previsto(e, alvo)):
            e.abre_com = None
            with self.agindo(e, ROTULOS_HABS_INIMIGO.get(abre), alvo, hab=abre, anim=HABS[abre]["anim"]):
                if HABS_INIMIGO[abre](self, e, alvo) is not False:
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
