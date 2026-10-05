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
        arma = rng.choice([None, g.j.equip["arma"]])
        heroi = {"nome": "Aldric", "classe": classe, "spec": None, "nome_classe": "Guerreiro", "nivel": 7, "dia": 20,
                 "resultado": rng.choice(["morte", "corrupcao", "vitoria"]), "causa": "Você tombou diante de Lobo.",
                 "arma": arma, "antagonista": "Zor, o Rei", "sigilos": 2}
        g.lendas = [heroi]
        g.marcar("tumulo", dict(heroi, local=aqui))
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


class TestSistemas(unittest.TestCase):
    def test_talentos_compraveis(self):
        from rpg import talentos
        for classe, specs in {"guerreiro": ["paladino", "berserker"], "arqueiro": ["patrulheiro", "sombra"],
                              "mago": ["piromante", "necromante"]}.items():
            for spec in specs:
                g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
                g.iniciar("Robô", classe)
                for _ in range(11):
                    g.subir_nivel()
                g.especializar(spec)
                comprados = 0
                while g.j.pontos_talento:
                    ok = [t for t in talentos.TALENTOS[classe] if talentos.estado(g.j, t) == "disponivel"]
                    if not ok:
                        break
                    t = ok[0]
                    g.j.talentos[t["id"]] = g.j.tal(t["id"]) + 1
                    g.j.pontos_talento -= 1
                    comprados += 1
                g.j.recalcular()
                self.assertGreater(comprados, 5)
                outra = [s for s in specs if s != spec][0]
                for t in talentos.TALENTOS[classe]:
                    if t["spec"] == outra:
                        self.assertEqual(talentos.estado(g.j, t), "bloqueado")
                # combate com talentos ativos não quebra
                g.mundo["atual"] = [l for l in g.mundo["locais"] if l["tipo"] == "selvagem"][0]["id"]
                try:
                    g.combate(g.grupo(n=3))
                except (LimiteBot, Derrota, FimDeJogo):
                    pass

    def test_mapa_renderiza(self):
        from rpg import mapa
        for seed in range(60):
            g = Jogo(BotUI(random.Random(seed)), seed=seed, pasta_saves=tempfile.mkdtemp())
            g.iniciar("Robô", "mago")
            for l in g.mundo["locais"]:
                l["visitado"] = seed % 2 == 0
            linhas = mapa.renderizar(g, 46, 15)
            self.assertEqual(len(linhas), 15)
            for linha in linhas:
                self.assertEqual(sum(len(t) for t, _ in linha), 46)
            mapa.legenda(g)

    def test_interface_textual(self):
        try:
            from rpg.tui import AppRPG
        except ImportError:
            self.skipTest("textual não instalado")
        import argparse
        import asyncio
        from rpg.__main__ import menu_principal
        args = argparse.Namespace(seed=5, classico=False, brando=False, hardcore=False, sem_cor=False, rapido=True,
                                  saves=tempfile.mkdtemp())

        async def rodar():
            app = AppRPG(args, menu_principal)
            async with app.run_test(size=(140, 44)) as pilot:
                async def esperar(n=25):
                    for _ in range(n):
                        await pilot.pause(0.02)
                await esperar()
                await pilot.press("1")
                await esperar()
                await pilot.press("enter")  # nome padrão
                await esperar()
                await pilot.press("1")  # guerreiro
                await esperar()
                for _ in range(30):
                    await pilot.press("1")
                    await esperar(6)
                self.assertIsNotNone(app.ui.jogo)
                self.assertGreater(app.ui.jogo.passos, 0)
                await pilot.press("ctrl+q")

        asyncio.run(rodar())
