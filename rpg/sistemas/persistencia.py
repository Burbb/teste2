"""Salvar, carregar e sair."""

import json
import os
import re
from ..entidades import Jogador
from .. import telemetria
from ..migracoes import CAMPOS_SAVE, VERSAO_SAVE, migrar
from ..regras import FimDeJogo


class Persistencia:
    # ================================================================ salvar / carregar
    def sair(self):
        op = self.menu("Sair do jogo?", [("Salvar e sair", "salvar"), ("Sair sem salvar", "sair"),
                                         ("Cancelar", None)])
        if op is None:
            return
        if op == "salvar":
            self.salvar()
        else:
            caminho = telemetria.exportar(self)
            if caminho:
                self.dizer(f"Registro parcial da partida: {caminho}", "cinza")
        raise FimDeJogo()

    def caminho_save(self):
        slug = re.sub(r"[^a-z0-9]+", "_", self.j.nome.lower()).strip("_") or "heroi"
        return os.path.join(self.pasta_saves, f"{slug}.json")

    def salvar(self, silencioso=False):
        os.makedirs(self.pasta_saves, exist_ok=True)
        estado = self.rng.getstate()
        dados = {
            "versao": VERSAO_SAVE,
            "seed": self.seed,
            "rng": [estado[0], list(estado[1]), estado[2]],
            "jogador": self.j.para_dict(),
        }
        for campo in CAMPOS_SAVE:
            dados[campo] = getattr(self, campo)
        caminho = self.caminho_save()
        temporario = caminho + ".tmp"
        with open(temporario, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False)
        os.replace(temporario, caminho)  # nunca deixa um save pela metade
        if silencioso:
            return
        self.dizer(f"Jogo salvo em {caminho}.", "verde")
        registro = telemetria.exportar(self)
        if registro:
            self.dizer(f"Registro parcial da partida: {registro}", "cinza")

    @classmethod
    def carregar(cls, ui, caminho, pasta_saves="saves"):
        """Lê um save de qualquer versão: as migrações o trazem até o formato atual antes de montar o jogo.
        Levanta migracoes.SaveIncompativel se o arquivo for de uma versão mais nova (ou não for um save)."""
        with open(caminho, encoding="utf-8") as f:
            dados = migrar(json.load(f))
        g = cls(ui, dados["seed"], pasta_saves)
        r = dados["rng"]
        g.rng.setstate((r[0], tuple(r[1]), r[2]))
        g.j = Jogador.de_dict(dados["jogador"])
        for campo in CAMPOS_SAVE:  # só o que o jogo conhece; campos estranhos no arquivo são ignorados
            if campo in dados:
                setattr(g, campo, dados[campo])
        return g
