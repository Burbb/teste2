"""Testes de fumaça: um robô joga partidas inteiras com escolhas aleatórias.

Rode com:  python -m unittest discover tests
"""

import random
import tempfile
import unittest

from rpg import comitiva
from rpg.classes import CLASSES
from rpg.itens import CONSUMIVEIS
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
        g.dia = 6
        if rng.random() < 0.85:  # uma comitiva em algum ponto da história
            for cid in rng.sample(list(comitiva.COMPANHEIROS), 2):
                m = comitiva.recrutar(g, cid)
                m.update(aprovacao=rng.choice([-20, 20, 60]), missao=rng.choice([0, 1, 2, 3]), dias=10,
                         conselho=rng.choice(["cortar", "usar"]),
                         caminho=rng.choice([None, "vazio", "liberta", "penitente", "capitao"]))
            g.plantar("teodoro_ruivo", 0)
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

    def test_lances_de_combate(self):
        """O combate conta à interface quem agiu, em quem, com que elemento, e o Redemoinho gira quatro vezes."""
        lances, falas = [], []

        class Gravador(BotUI):
            def lance(self, tipo, **dados):
                lances.append((tipo, dados))

            def fala(self, cid, nome, texto):
                falas.append((cid, texto))

        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(Gravador(random.Random(3), max_decisoes=300), seed=3, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            for cid in ("odete", "morel"):
                comitiva.recrutar(g, cid)
            g.j.spec = "berserker"
            g.j.habilidades = ["redemoinho"]
            g.j.rec = g.j.max_rec
            escolhas = iter([1, 0])  # Habilidades → Redemoinho
            g.ui.escolher = lambda pergunta, opcoes: next(escolhas, 0)
            inimigos = [g.inimigo("bandido", nivel=1) for _ in range(2)]
            for e in inimigos:
                e.hp = e.max_hp = 500
            g.combate_ativo = None
            from rpg.combate import Combate
            cb = Combate(g, inimigos)
            comitiva.preparar_combate(cb)
            cb.turno = 1
            cb.fase_jogador()
            tipos = [t for t, _ in lances]
            self.assertEqual(tipos[0], "acao")
            self.assertEqual(lances[0][1]["hab"], "redemoinho")
            self.assertTrue(lances[0][1]["area"])
            self.assertEqual(tipos[-1], "fim_acao")
            # Os giros saem numa salva só: a tela anima cada giro cortando todos ao mesmo tempo.
            salva = next(d for t, d in lances if t == "salva")["lances"]
            internos = [x["tipo"] for x in salva]
            from rpg.habilidades import GIROS_REDEMOINHO
            self.assertEqual(internos.count("giro"), GIROS_REDEMOINHO)
            self.assertEqual(internos.count("golpe") + internos.count("erro"), 2 * GIROS_REDEMOINHO)
            golpe = next(x for x in salva if x["tipo"] == "golpe")
            self.assertEqual(golpe["de"], "j")
            self.assertIn(golpe["em"], {cb.uid(e) for e in inimigos})
            cb.fase_aliados()
            self.assertTrue(any(d.get("de") == cb.uid(a) for t, d in lances for a in cb.aliados if t == "acao"))
            g.combate_ativo = None

    def test_chamas_acumulam_e_combustao_detona(self):
        """O fogo do mago rende em camadas (até 3) e a Combustão transforma o que falta arder em dano na hora."""
        from rpg.habilidades import HABILIDADES
        from rpg.combate import Combate
        lances = []

        class Gravador(BotUI):
            def lance(self, tipo, **dados):
                lances.append((tipo, dados))

        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(Gravador(random.Random(7), max_decisoes=50), seed=7, pasta_saves=pasta)
            g.iniciar("Robô", "mago")
            g.j.spec = "piromante"
            g.clima = "limpo"
            alvo = g.inimigo("bandido", nivel=3)
            alvo.hp = alvo.max_hp = 2000
            alvo.agi = 0
            cb = Combate(g, [alvo])
            base = cb.valor_queimadura(g.j)
            self.assertLess(base, g.j.poder * 0.2)  # uma camada é pouco: o forte é acumular e detonar
            for _ in range(4):
                cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(g.j), valor=base, acumula=True)
            self.assertEqual(cb.camadas(alvo), Combate.MAX_CHAMAS)
            self.assertAlmostEqual(alvo.efeito("queimadura")["v"], base * Combate.MAX_CHAMAS)
            restante = cb.restante_queimadura(alvo)
            antes = alvo.hp
            HABILIDADES["combustao"]["fn"](cb, g.j, alvo)
            self.assertIsNone(alvo.efeito("queimadura"))
            self.assertGreater(antes - alvo.hp, restante * 0.5)
            # Meditar mostra a mana voltando na carta.
            g.j.rec = 0
            HABILIDADES["meditar"]["fn"](cb, g.j, None)
            rec = [d for t, d in lances if t == "recurso"]
            self.assertTrue(rec and rec[-1]["valor"] > 0 and rec[-1]["em"] == "j")
            g.combate_ativo = None

    def test_cacada_de_contrato_sempre_acha_o_bicho(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(5), max_decisoes=200), seed=5, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            loc = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")
            g.mundo["atual"] = loc["id"]
            from rpg.dados import BIOMAS
            fam = BIOMAS[loc["bioma"]]["familias"][0]
            c = {"id": 991, "tipo": "caca", "local": loc["id"], "familia": fam, "total": 3, "feito": 0,
                 "ouro": 10, "xp": 10, "desc": "teste"}
            g.contratos.append(c)
            vistos = []

            def escolher(pergunta, opcoes):
                vistos.append(list(opcoes))
                return next(i for i, o in enumerate(opcoes) if o.startswith("Caçar"))
            g.ui.escolher = escolher
            grupos = []

            def combate(grupo, **kw):  # vitória instantânea: só interessa quem apareceu
                grupos.append(grupo)
                g.registrar_abates(grupo)
                return "vitoria"
            g.combate = combate
            while not c.get("concluido"):
                g.menu_selvagem()
                self.assertLessEqual(len(grupos), 3)
            self.assertTrue(any(o.startswith("Caçar") for o in vistos[0]))
            self.assertTrue(all(grupo[0].familia == fam for grupo in grupos))
            self.assertEqual(g.contratos_aqui(), [])

    def test_resumo_da_run_tem_versao(self):
        from rpg import telemetria
        with tempfile.TemporaryDirectory() as pasta:
            g = jogar(11, "arqueiro", decisoes=80, pasta=pasta)
            caminho = telemetria.exportar(g)
            with open(caminho, encoding="utf-8") as f:
                topo = f.read(600)
            self.assertNotIn("Jogo: ?", topo)
            self.assertIn("Interface: BotUI", topo)

    def test_area_acerta_todos_juntos(self):
        """Habilidade em área vira um lance "salva" com os golpes de todos os alvos (a tela anima tudo junto)."""
        from rpg.habilidades import HABILIDADES
        from rpg.combate import Combate
        lances = []

        class Gravador(BotUI):
            def lance(self, tipo, **dados):
                lances.append((tipo, dados))

        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(Gravador(random.Random(9), max_decisoes=50), seed=9, pasta_saves=pasta)
            g.iniciar("Robô", "arqueiro")
            inimigos = [g.inimigo("bandido", nivel=1) for _ in range(3)]
            for e in inimigos:
                e.hp = e.max_hp = 500
            cb = Combate(g, inimigos)
            with cb.agindo(g.j, "Chuva de Flechas", area=True, hab="chuva_flechas"):
                HABILIDADES["chuva_flechas"]["fn"](cb, g.j, None)
            tipos = [t for t, _ in lances]
            self.assertEqual(tipos, ["acao", "salva", "fim_acao"])
            golpes = [x for x in lances[1][1]["lances"] if x["tipo"] in ("golpe", "erro")]
            self.assertEqual({x["em"] for x in golpes}, {cb.uid(e) for e in inimigos})
            g.combate_ativo = None

    def test_aljava_tem_limite(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(3), max_decisoes=50), seed=3, pasta_saves=pasta)
            g.iniciar("Robô", "arqueiro")
            g.dar_flechas(500)
            self.assertEqual(g.j.flechas, g.max_flechas())

    def test_contratos_na_faixa_do_heroi(self):
        from rpg.mundo import nivel_regiao
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(4), max_decisoes=50), seed=4, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            for nivel in (1, 3, 5):
                g.j.nivel = nivel
                niveis = [nivel_regiao(g.mundo["locais"][c["local"]])
                          for c in (g.gerar_contrato() for _ in range(40)) if c["tipo"] != "entrega"]
                existentes = {nivel_regiao(l) for l in g.mundo["locais"] if l["tipo"] in ("selvagem", "covil")}
                if any(-1 <= n - nivel <= 2 for n in existentes):
                    self.assertTrue(all(-1 <= n - nivel <= 2 for n in niveis), (nivel, niveis))
            # Contrato mais difícil paga mais.
            self.assertLess(g.recompensa_contrato(1)[1], g.recompensa_contrato(7)[1])

    def test_grupo_sem_repeticao(self):
        from rpg import texto as tx
        from rpg.inimigos import criar
        r = random.Random(1)
        self.assertEqual(tx.descrever_grupo([criar(r, "harpia", 3, "flamejante"), criar(r, "harpia", 3, "flamejante")]),
                         "duas harpias flamejantes")

    def test_consumiveis_inuteis_e_comitiva(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(2), max_decisoes=50), seed=2, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            g.j.consumiveis.update(pocao_vida=1, bandagem=1)
            self.assertFalse(g.usar_consumivel("pocao_vida"))  # vida cheia: não gasta
            self.assertEqual(g.j.consumiveis["pocao_vida"], 1)
            m = comitiva.recrutar(g, "odete")
            m["hp"], m["ferido"] = 1, True
            self.assertTrue(g.usar_em_companheiro("bandagem", "odete"))
            self.assertFalse(m["ferido"])
            self.assertEqual(g.j.consumiveis["bandagem"], 0)

    def test_mercado_quantidade_e_auto_equipar(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(2), max_decisoes=50), seed=2, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            g.j.ouro = 500
            tochas = g.j.consumiveis.get("tocha", 0)
            preco = g.preco(CONSUMIVEIS["tocha"]["preco"])
            g.ui.escolher = lambda pergunta, opcoes: opcoes.index("Comprar Tocha")
            g.ui.extra_resposta = {"qtd": 3}
            self.assertFalse(g._loja_web([]))
            self.assertEqual(g.j.consumiveis["tocha"], tochas + 3)
            self.assertEqual(g.j.ouro, 500 - 3 * preco)
            # Equipamento comprado com o espaço do corpo vazio já sai vestido.
            from rpg.itens import gerar_equip
            elmo = gerar_equip(random.Random(1), "guerreiro", 2, slot="cabeca")
            g.j.equip["cabeca"] = None
            g.ui.escolher = lambda pergunta, opcoes: opcoes.index(f"Comprar {elmo['nome']}")
            g._loja_web([elmo])
            self.assertIs(g.j.equip["cabeca"], elmo)
            self.assertNotIn(elmo, g.j.mochila)

    def test_acampamento_e_reserva(self):
        """Quem sai da comitiva espera no acampamento; na fogueira dá para trocar quem vai junto."""
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(4), max_decisoes=200), seed=4, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            comitiva.recrutar(g, "odete")
            comitiva.recrutar(g, "morel")
            g.ui.escolher = lambda pergunta, opcoes: next(i for i, o in enumerate(opcoes) if "espera no acampamento" in o)
            self.assertTrue(comitiva.oferecer_vaga(g, "yara"))
            self.assertIsNotNone(comitiva.na_reserva(g, "yara"))
            self.assertFalse(comitiva.presente(g, "yara"))
            self.assertFalse(comitiva.disponivel(g, "yara"))
            # Na reserva não come nem opina.
            comitiva.reagir(g, "magia_proibida")
            self.assertEqual(comitiva.na_reserva(g, "yara")["aprovacao"], 0)
            # Na fogueira: troca a Yara pela Odette e dorme.
            passos = iter(["Levar Yara no lugar de Odette", "Dormir até o amanhecer"])
            alvo = {"t": next(passos)}

            def escolher(pergunta, opcoes):
                i = next(i for i, o in enumerate(opcoes) if o.startswith(alvo["t"]))
                alvo["t"] = next(passos, "Dormir até o amanhecer")
                return i
            g.ui.escolher = escolher
            comitiva.fogueira(g)
            self.assertTrue(comitiva.presente(g, "yara"))
            self.assertIsNotNone(comitiva.na_reserva(g, "odete"))
            # Salvar e carregar mantém a reserva.
            g.salvar(silencioso=True)
            g2 = Jogo.carregar(BotUI(random.Random(1)), g.caminho_save(), pasta)
            self.assertEqual([m["id"] for m in g2.reserva], ["odete"])

    def test_mural_web(self):
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(6), max_decisoes=50), seed=6, pasta_saves=pasta)
            g.iniciar("Robô", "arqueiro")
            oferta = {"dia": g.dia, "lista": [g.gerar_contrato() for _ in range(3)]}
            dados = g.dados_mural(oferta)
            self.assertEqual(len(dados["oferta"]), 3)
            for c in dados["oferta"]:
                self.assertTrue({"lugar", "ouro", "xp", "distancia", "tipo"} <= set(c))
            primeiro = oferta["lista"][0]
            g.ui.escolher = lambda pergunta, opcoes: opcoes.index(f"Aceitar: {primeiro['desc']}")
            self.assertFalse(g._mural_web(oferta))
            self.assertIn(primeiro, g.contratos)
            self.assertEqual(len(oferta["lista"]), 2)

    def test_comitiva(self):
        """Opinião, partida, conversas, combate e salvar/carregar da comitiva."""
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(5), max_decisoes=400), seed=5, pasta_saves=pasta)
            g.iniciar("Robô", "guerreiro")
            for cid in ("odete", "yara"):
                comitiva.recrutar(g, cid)
            # A escolha feita num evento chega à comitiva pelo menu do jogo.
            g.evento_atual = "viajante_ferido"
            g.ui.escolher = lambda pergunta, opcoes: opcoes.index("Revistar os bolsos")
            g.menu("?", [("Ajudar", "pocao"), ("Revistar os bolsos", "roubar")])
            g.evento_atual = None
            self.assertLess(comitiva.membro(g, "odete")["aprovacao"], -5)
            del g.ui.escolher
            comitiva.membro(g, "odete")["aprovacao"] = 0
            comitiva.membro(g, "yara")["aprovacao"] = 0
            comitiva.reagir(g, "magia_proibida")
            self.assertLess(comitiva.membro(g, "odete")["aprovacao"], 0)
            self.assertGreater(comitiva.membro(g, "yara")["aprovacao"], 0)
            for _ in range(5):
                comitiva.reagir(g, "magia_proibida", "sacrilegio")
            self.assertFalse(comitiva.presente(g, "odete"), "Odette deveria ter ido embora")
            self.assertEqual(g.flag("comitiva:odete"), "partiu")
            self.assertFalse(comitiva.disponivel(g, "odete"))
            # Todas as conversas de todos são alcançáveis com aprovação alta e missões concluídas.
            for cid in ("morel", "odete"):
                g.flags.pop(f"comitiva:{cid}", None)
            g.comitiva = []
            for cid in comitiva.COMPANHEIROS:
                g.comitiva = []
                m = comitiva.recrutar(g, cid)
                for etapa in range(len(comitiva.CONVERSAS[cid])):
                    m.update(aprovacao=60, dias=20, missao=3 if etapa == 2 else m["missao"],
                             caminho=m["caminho"] or "liberta", ultima_conversa=-1)
                    self.assertTrue(comitiva.conversar(g, m), f"{cid} etapa {etapa}")
                    self.assertTrue(comitiva.presente(g, cid))
            # Combates e uma partida jogada com comitiva completa.
            g.comitiva = []
            for cid in ("morel", "yara"):
                comitiva.recrutar(g, cid)
            try:
                for _ in range(40):
                    g.tela()
            except (LimiteBot, FimDeJogo, Derrota):
                pass
            g.salvar(silencioso=True)
            g2 = Jogo.carregar(BotUI(random.Random(1)), g.caminho_save(), pasta)
            self.assertEqual([m["id"] for m in g2.comitiva], [m["id"] for m in g.comitiva])

    def test_equipamento_completo(self):
        """Dez espaços, anéis duplos, tirar e largar, e saves antigos com só três espaços."""
        from rpg import itens
        with tempfile.TemporaryDirectory() as pasta:
            g = Jogo(BotUI(random.Random(2)), seed=2, pasta_saves=pasta)
            g.iniciar("Robô", "mago")
            r = random.Random(4)
            for slot in itens.PESO_SLOT:
                it = itens.gerar_equip(r, "mago", 5, slot=slot)
                self.assertEqual(it["slot"], slot if it["raridade"] != "lendario" else it["slot"])
                g.equipar(it)
            g.equipar(itens.gerar_equip(r, "mago", 5, slot="anel", raridade="magico"))
            self.assertTrue(g.j.equip["anel1"] and g.j.equip["anel2"])
            self.assertEqual(set(g.j.equip), set(itens.SLOTS))
            antes = g.j.defesa
            g.desequipar("armadura")
            self.assertIsNone(g.j.equip["armadura"])
            self.assertLessEqual(g.j.defesa, antes)
            item = g.j.mochila[-1]
            g.largar(item)
            self.assertNotIn(item, g.j.mochila)
            dados = g.j.para_dict()
            dados["equip"] = {"arma": dados["equip"]["arma"], "armadura": None, "amuleto": None}
            from rpg.entidades import Jogador
            from rpg.migracoes import migrar
            velho = Jogador.de_dict(migrar({"versao": 1, "seed": 1, "mundo": {"locais": []}, "jogador": dados})["jogador"])
            self.assertEqual(set(velho.equip), set(itens.SLOTS))
            for _ in range(300):  # toda geração produz itens válidos em todas as classes
                for classe in ("guerreiro", "arqueiro", "mago"):
                    it = itens.gerar_equip(r, classe, r.randint(1, 12))
                    self.assertIn(it["slot"], itens.PESO_SLOT)
                    self.assertTrue(it["bonus"])

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

    def test_ferimentos(self):
        """Arranhão não marca; golpe pesado pode; quem já carrega um ferimento se fere menos; a dica diz o que o
        ferimento faz nos números deste herói (−15% de um Poder 1 não tira nada)."""
        from rpg import balanceamento as bal, sobrevivencia

        class Sorteio:  # tira sempre o mesmo número
            def __init__(self, x):
                self.x = x

            def random(self):
                return self.x

            def choice(self, seq):
                return seq[0]

        g = Jogo(BotUI(random.Random(1)), seed=1, pasta_saves=tempfile.mkdtemp())
        g.iniciar("Robô", "guerreiro")
        j = g.j
        g.rng = Sorteio(0.0)
        sobrevivencia.talvez_ferir(g, int(j.max_hp * bal.FERIMENTO_LIMIAR) - 1, "fisico", False, None)
        self.assertEqual(j.ferimentos, [])
        pesado = int(j.max_hp * 0.3)
        chance = bal.FERIMENTO_BASE + (pesado / j.max_hp - bal.FERIMENTO_LIMIAR) * bal.FERIMENTO_GRAVIDADE
        g.rng = Sorteio(chance * 0.75)  # fere quem está inteiro, não quem já está ferido
        sobrevivencia.talvez_ferir(g, pesado, "fisico", False, None)
        self.assertEqual(len(j.ferimentos), 1)
        antes = [dict(f) for f in j.ferimentos]
        sobrevivencia.talvez_ferir(g, pesado, "fisico", False, None)
        self.assertEqual(j.ferimentos, antes)

        linhas = sobrevivencia.explicar({"id": "infeccao", "dias": None}, j.nome_recurso, j)
        self.assertEqual(linhas[0], "−15% Ataque, −15% Poder, −15% Agilidade.")
        totais, _ = j.totais()
        atk, poder, agi = (int(round(totais[s])) for s in ("atk", "poder", "agi"))
        self.assertEqual((poder, agi), (1, 3))  # o guerreiro novo: pouco Poder e pouca Agilidade
        self.assertEqual(linhas[1], f"No seu herói: Ataque {atk} → {int(round(totais['atk'] * 0.85))}. "
                                    "Poder 1 e Agilidade 3: baixos demais para cair.")

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


class TestSaves(unittest.TestCase):
    def _save_v1(self, pasta):
        """Monta um save no formato antigo (versão 1): sem coordenadas, 3 espaços de equipamento, sem talentos."""
        import json
        import os
        g = jogar(5, "guerreiro", decisoes=60, pasta=pasta)
        g.salvar(silencioso=True)
        caminho = g.caminho_save()
        with open(caminho, encoding="utf-8") as f:
            d = json.load(f)
        d["versao"] = 1
        for loc in d["mundo"]["locais"]:
            loc.pop("x", None)
            loc.pop("y", None)
        d["jogador"]["equip"] = {k: d["jogador"]["equip"].get(k) for k in ("arma", "armadura", "amuleto")}
        for k in ("talentos", "pontos_talento", "provisoes", "fome", "ferimentos"):
            d["jogador"].pop(k, None)
        d.pop("comitiva", None)
        d.pop("reserva", None)
        d["campo_que_nao_existe_mais"] = 123
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(d, f)
        return caminho, os

    def test_save_antigo_e_migrado(self):
        from rpg.migracoes import VERSAO_SAVE
        with tempfile.TemporaryDirectory() as pasta:
            caminho, os = self._save_v1(pasta)
            g = Jogo.carregar(BotUI(random.Random(1), max_decisoes=80), caminho, pasta)
            self.assertTrue(all("x" in l and "y" in l for l in g.mundo["locais"]))
            self.assertEqual(len(g.j.equip), 10)
            self.assertEqual(g.j.talentos, {})
            self.assertEqual(g.reserva, [])
            self.assertFalse(hasattr(g, "campo_que_nao_existe_mais"))
            try:
                g.rodar()  # e o jogo segue normalmente a partir dele
            except LimiteBot:
                pass
            g.salvar(silencioso=True)
            import json
            with open(g.caminho_save(), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["versao"], VERSAO_SAVE)

    def test_save_mais_novo_avisa(self):
        import json
        from rpg.migracoes import SaveIncompativel, VERSAO_SAVE
        with tempfile.TemporaryDirectory() as pasta:
            caminho, _ = self._save_v1(pasta)
            with open(caminho, encoding="utf-8") as f:
                d = json.load(f)
            d["versao"] = VERSAO_SAVE + 1
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(d, f)
            with self.assertRaises(SaveIncompativel):
                Jogo.carregar(BotUI(random.Random(1)), caminho, pasta)


class TestGabarito(unittest.TestCase):
    def test_partidas_identicas_ao_gabarito(self):
        """Refatorações não podem mudar a jogabilidade: as partidas de referência saem iguais, evento por evento.
        Se a mudança de jogabilidade foi de propósito: python -m tests.gabarito --atualizar"""
        import json
        from tests import gabarito
        with open(gabarito.ARQUIVO, encoding="utf-8") as f:
            esperado = json.load(f)
        atual = gabarito.calcular()
        self.assertEqual(sorted(esperado), sorted(atual))
        diferentes = [n for n in esperado if esperado[n] != atual[n]]
        self.assertEqual(diferentes, [], "partidas diferentes do gabarito (veja python -m tests.gabarito --mostrar)")
