"""Os guardiões: o nível deles e o Sigilo de quem vence um (a guardiã da campanha). O covil do mundo gerado e a
batalha final saíram na 1.206.0; o catálogo de guardiões e de antagonistas fica em inimigos.py e dados.py."""

from ..mundo import nivel_regiao


class Chefes:
    # ================================================================ chefes
    def nivel_guardiao(self, loc):
        return nivel_regiao(loc) + 1

    def receber_sigilo(self, sigilo, guardiao):
        """A recompensa de progressão de um guardião vencido: o Sigilo, reputação, um ponto de talento e a festa.
        Serve à guardiã da campanha (que pode ser vencida sem morrer: o rito)."""
        self.j.sigilos.append(sigilo)
        self.estatisticas["chefes"] += 1
        festa = self.ui.conquistas_na_tela  # a festa do Sigilo já mostra a runa e o ponto de talento
        if not festa:
            self.ui.titulo(f"SIGILO OBTIDO ({len(self.j.sigilos)}/3)", "amarelo+negrito")
            self.dizer("Uma runa ardente se grava na palma da sua mão.", "amarelo")
        self.mudar_reputacao(5)
        self.ganhar_ponto_talento(anunciar=not festa)
        self.ui.celebrar("sigilo", {"sigilos": len(self.j.sigilos), "guardiao": guardiao,
                                    "pontos": self.j.pontos_talento})
