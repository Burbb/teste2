"""Legado entre partidas e o bestiário."""

from .. import texto as tx
from ..dados import FAMILIAS, LORE, TRACOS
from .. import legado


class Bestiario:
    # ================================================================ legado e bestiário
    def preparar_legado(self):
        """Heróis de partidas anteriores deixam marcas neste mundo."""
        self.lendas = legado.carregar(self.pasta_saves)[-6:]
        if not self.lendas:
            return
        ultimo = self.lendas[-1]
        if ultimo["resultado"] == "vitoria":
            self.marcar("estatua", ultimo)
            self.j.reputacao += 5
        else:
            selvagens = [l for l in self.mundo["locais"] if l["tipo"] == "selvagem"]
            self.marcar("tumulo", dict(ultimo, local=self.sortear(selvagens)["id"]))

    def registrar_legado(self, resultado, causa):
        j = self.j
        legado.registrar(self.pasta_saves, {
            "nome": j.nome, "classe": j.classe, "spec": j.spec, "nome_classe": j.nome_classe, "nivel": j.nivel,
            "dia": self.dia, "resultado": resultado, "causa": causa, "arma": j.equip["arma"],
            "antagonista": self.antagonista["nome"], "sigilos": len(j.sigilos),
        })

    def ver_criatura(self, familia):
        if familia in FAMILIAS:
            b = self.bestiario.setdefault(familia, {"vistos": 0, "abates": 0})
            b["vistos"] += 1

    def conhece(self, familia):
        """Fraquezas e habilidades ficam visíveis após 2 abates (magos estudam à primeira vista)."""
        if familia not in FAMILIAS:
            return True
        return self.j.classe == "mago" or self.bestiario.get(familia, {}).get("abates", 0) >= 2

    def conhece_resistencias(self, familia):
        """As resistências pedem mais estudo: 4 abates (2 para magos)."""
        if familia not in FAMILIAS:
            return True
        precisa = 2 if self.j.classe == "mago" else 4
        return self.bestiario.get(familia, {}).get("abates", 0) >= precisa

    def progresso_bestiario(self, familia):
        """O que falta aprender desta espécie, para a ficha do inimigo."""
        if familia not in FAMILIAS:
            return None
        abates = self.bestiario.get(familia, {}).get("abates", 0)
        if not self.conhece(familia):
            return f"Derrote {2 - abates} para descobrir as fraquezas ({abates}/2)."
        if not self.conhece_resistencias(familia):
            return f"Derrote {4 - abates} para descobrir as resistências ({abates}/4)."
        if abates < 5:
            return f"Mais {5 - abates} e você vira mestre caçador desta espécie (+10% de dano)."
        return "Mestre caçador: +10% de dano contra esta espécie."

    def mestre_caca(self, familia):
        return self.bestiario.get(familia, {}).get("abates", 0) >= 5

    def ver_bestiario(self):
        self.ui.cena("Bestiário", f"{len(self.bestiario)}/{len(LORE)} criaturas", "menu")
        fichas = []
        for fam, b in sorted(self.bestiario.items(), key=lambda x: FAMILIAS[x[0]]["nome"]):
            f = FAMILIAS[fam]
            conhece = self.conhece(fam)
            fichas.append({"id": fam, "nome": tx.maiuscula(f["nome"]), "abates": b["abates"], "lore": LORE.get(fam, ""),
                           "conhecido": conhece, "mestre": self.mestre_caca(fam), "tracos": f["tracos"],
                           "tracos_nomes": [TRACOS[t].split(":")[0] for t in f["tracos"]] if conhece else [],
                           "fraquezas": [k for k, v in f.get("resist", {}).items() if v > 1] if conhece else [],
                           "resiste": [k for k, v in f.get("resist", {}).items() if v < 1] if conhece else []})
        if self.ui.painel("bestiario", {"fichas": fichas, "total": len(LORE)}):
            self.pausar()
            return
        if not self.bestiario:
            self.dizer("Você ainda não enfrentou nenhuma criatura.", "cinza")
        for fam, b in sorted(self.bestiario.items(), key=lambda x: FAMILIAS[x[0]]["nome"]):
            f = FAMILIAS[fam]
            selo = "  ★ mestre caçador: +10% de dano" if self.mestre_caca(fam) else ""
            self.dizer(f"{tx.maiuscula(f['nome'])} — abates: {b['abates']}{selo}", "amarelo+negrito")
            self.dizer(f"  {LORE.get(fam, '')}", "cinza")
            if self.conhece(fam):
                tracos = ", ".join(TRACOS[t].split(":")[0] for t in f["tracos"])
                fracos = [k for k, v in f.get("resist", {}).items() if v > 1]
                info = f"  Traços: {tracos}"
                if fracos:
                    info += f" · fraco contra {', '.join(fracos)}"
                self.dizer(info)
            else:
                self.dizer("  Detalhes: ??? (derrote mais destas criaturas para aprender)", "cinza")
        self.pausar()
