"""Salvar, carregar e sair."""

import json
import os
import re
from ..entidades import Jogador
from .. import telemetria
from ..regras import VERSAO_SAVE, FimDeJogo


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
        for campo in ("mundo", "dia", "periodo", "clima", "corrupcao", "passos", "flags", "historico", "contagem",
                      "impulsos", "sementes", "rumores", "contratos", "ofertas", "lojas", "nemesis",
                      "aliados_finais", "forcados", "proximo_id", "estatisticas", "hardcore", "bestiario", "lendas",
                      "registro", "arquivo_run", "comitiva", "reserva"):
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
        with open(caminho, encoding="utf-8") as f:
            dados = json.load(f)
        g = cls(ui, dados["seed"], pasta_saves)
        r = dados.pop("rng")
        g.rng.setstate((r[0], tuple(r[1]), r[2]))
        g.j = Jogador.de_dict(dados.pop("jogador"))
        dados.pop("versao", None)
        dados.pop("seed", None)
        for campo, valor in dados.items():
            setattr(g, campo, valor)
        # Saves da versão anterior não tinham coordenadas no mapa.
        for loc in g.mundo["locais"]:
            loc.setdefault("x", 0.03 + 0.9 * (loc["perigo"] - 1) / 4 if loc["id"] else 0.03)
            loc.setdefault("y", 0.08 + 0.84 * ((loc["id"] * 5) % 11) / 10)
        return g
