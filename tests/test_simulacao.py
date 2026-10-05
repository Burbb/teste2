"""Testes de fumaça: um robô joga partidas inteiras com escolhas aleatórias.

Rode com:  python -m unittest discover tests
"""

import random
import tempfile
import unittest

from rpg.classes import CLASSES
from rpg.eventos import REGISTRO
from rpg.jogo import Derrota, FimDeJogo, Jogo
from rpg.ui import BotUI, LimiteBot


def jogar(seed, classe, decisoes=600, pasta=None):
    rng = random.Random(seed * 7 + 1)
    ui = BotUI(rng, max_decisoes=decisoes)
    g = Jogo(ui, seed=seed, pasta_saves=pasta or tempfile.mkdtemp())
    g.iniciar("Robô", classe)
    try:
        g.rodar()
    except LimiteBot:
        pass
    return g


class TestSimulacao(unittest.TestCase):
    def test_partidas_aleatorias(self):
        with tempfile.TemporaryDirectory() as pasta:
            for seed in range(45):
                classe = list(CLASSES)[seed % 3]
                with self.subTest(seed=seed, classe=classe):
                    jogar(seed, classe, pasta=pasta)

    def test_todo_evento_roda(self):
        """Prepara um estado rico e executa cada evento em todas as classes e especializações."""
        specs = {"guerreiro": ["paladino", "berserker"], "arqueiro": ["patrulheiro", "sombra"],
                 "mago": ["piromante", "necromante"]}
        executados = set()
        for classe, lista in specs.items():
            for spec in [None] + lista:
                for ev in REGISTRO:
                    for tentativa in range(8):
                        rng = random.Random(f"{ev.id}{classe}{spec}{tentativa}")
                        g = self._estado_rico(rng, classe, spec, ev.contextos)
                        if ev.cond and not ev.cond(g):
                            continue
                        executados.add(ev.id)
                        with self.subTest(evento=ev.id, classe=classe, spec=spec):
                            try:
                                ev.fn(g)
                            except (LimiteBot, FimDeJogo, Derrota):
                                pass
        nunca = {ev.id for ev in REGISTRO} - executados
        self.assertFalse(nunca, f"eventos nunca executados: {sorted(nunca)}")

    @staticmethod
    def _estado_rico(rng, classe, spec, contextos):
        ui = BotUI(rng, max_decisoes=150)
        g = Jogo(ui, seed=rng.randrange(10 ** 6), pasta_saves=tempfile.mkdtemp())
        g.iniciar("Robô", classe)
        g.j.nivel = 5
        if spec:
            g.especializar(spec)
        g.j.ouro = 200
        g.j.reputacao = rng.choice([-30, 0, 30])
        g.corrupcao = rng.choice([10, 55, 80])
        g.clima = rng.choice(["limpo", "chuva", "nevoa", "tempestade", "neve"])
        g.periodo = rng.choice([0, 3])
        tipos = ["vila"] if contextos == ("vila",) else ["selvagem", "covil", "cidadela"]
        g.mundo["atual"] = rng.choice([l for l in g.mundo["locais"] if l["tipo"] in tipos])["id"]
        aqui = g.loc["id"]
        vila = next(l for l in g.mundo["locais"] if l["tipo"] == "vila")
        for sid, dados in [("viajante_grato", dict(nome="Ana", g="f", prof="pastora")),
                           ("mercador_golpista", dict(nome="Tito", preco=40)),
                           ("bandido_poupado", dict(lider="Zorvek", tipo="acordo")),
                           ("ladrao_fugitivo", dict(nome="Ligeiro", ouro=30)),
                           ("familia_grata", dict(nome="Nina", vila=aqui)),
                           ("aprendiz_grato", dict(nome="Caio")),
                           ("pacote_suspeito", dict(contrato=1)),
                           ("irmandade_cobra", {}), ("ladrao_redimido", {})]:
            g.plantar(sid, 0, **dados)
        g.nemesis = {"familia": "lobo", "afixo": "feroz", "nome": "Presa-Rubra", "nivel": 5, "pronto": 0,
                     "vezes": 0}
        g.contratos = [
            {"id": 1, "tipo": "entrega", "destino": vila["id"], "objeto": "um baú", "ouro": 30, "xp": 20,
             "desc": "Levar um baú."},
            {"id": 2, "tipo": "alvo", "local": aqui, "familia": "lobo", "nome": "Uivo", "chave": "alvo:2",
             "ouro": 40, "xp": 30, "desc": "Caçar Uivo."},
        ]
        for ev_id in ("tesouro_escondido", "fera_lendaria", "mercador_raro"):
            g.rumores.append({"texto": "teste", "evento": ev_id, "local": aqui, "expira": 99, "familia": "lobo",
                              "nome": "Bocarra"})
        return g

    def test_salvar_e_carregar(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = jogar(3, "arqueiro", decisoes=200, pasta=pasta)
            if g.j.hp <= 0:
                return
            g.salvar()
            ui = BotUI(random.Random(1), max_decisoes=200)
            g2 = Jogo.carregar(ui, g.caminho_save(), pasta)
            self.assertEqual(g2.j.nivel, g.j.nivel)
            self.assertEqual(g2.dia, g.dia)
            self.assertEqual(g2.rng.random(), g.rng.random())
            try:
                g2.rodar()
            except LimiteBot:
                pass

    def test_mundo_conectado(self):
        from rpg.mundo import _distancias, gerar_mundo
        for seed in range(200):
            m = gerar_mundo(random.Random(seed))
            dist = _distancias(m["locais"])
            self.assertEqual(len(dist), len(m["locais"]), f"mundo desconexo com seed {seed}")
            self.assertEqual(sum(1 for l in m["locais"] if l["tipo"] == "covil"), 3)


if __name__ == "__main__":
    unittest.main()
