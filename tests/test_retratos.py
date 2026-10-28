"""O retrato das criaturas (dados.retrato): as cabeças próprias pela chave e pela família, o resto pelos traços."""

import pathlib
import re
import unittest

from rpg.dados import FAMILIAS, RETRATO_CHAVE, RETRATO_FAMILIA, retrato

ESTATICO = pathlib.Path(__file__).resolve().parents[1] / "rpg" / "web" / "static"


class TestRetratos(unittest.TestCase):
    def test_afogado_pela_familia(self):
        self.assertEqual(retrato(FAMILIAS["afogado"]["tracos"], "afogado"), "afogado")

    def test_ilse_pela_chave_antes_dos_tracos(self):
        # a Ilse é morta-viva e conjuradora (a caveira pelos traços); a família dela é "guardiao"
        self.assertEqual(retrato(["morto-vivo", "conjurador"], "guardiao", "ilse"), "ilse")

    def test_lobo_e_bandido_pela_familia(self):
        self.assertEqual(retrato(FAMILIAS["lobo"]["tracos"], "lobo"), "lobo")
        self.assertEqual(retrato(FAMILIAS["bandido"]["tracos"], "bandido"), "bandido")
        # os guardiões sem retrato próprio continuam no desenho do traço (a fera e o humano sem id)
        self.assertEqual(retrato(["fera"], "guardiao", "guardiao:3"), "fera")
        self.assertEqual(retrato(["humano", "conjurador"], "guardiao", "guardiao:4"), "humano")

    def test_sapo_e_sanguessuga_pela_familia(self):
        # 1.171.0: o sapo-touro gigante e a sanguessuga gigante pela família; as outras feras continuam pelos traços (a
        # Hidra do Pântano, guardiã, tem o dela pelo id desde a 1.197.0)
        self.assertEqual(retrato(FAMILIAS["sapo"]["tracos"], "sapo"), "sapo")
        self.assertEqual(retrato(FAMILIAS["sanguessuga"]["tracos"], "sanguessuga"), "sanguessuga")
        self.assertEqual(retrato(["fera"], "guardiao", "guardiao:3", "hidra_do_brejo"), "hidra_do_brejo")
        self.assertEqual(retrato(["fera"]), "fera")

    def test_cultista_bruxa_e_rato_pela_familia(self):
        # 1.172.0: pela família (o cultista também nos fiéis do Profeta e nos da sacristia, que são cultistas); o Profeta
        # das Cinzas (guardião) tem o dele pelo id desde a 1.198.0
        self.assertEqual(retrato(FAMILIAS["cultista"]["tracos"], "cultista"), "cultista")
        self.assertEqual(retrato(FAMILIAS["bruxa_brejo"]["tracos"], "bruxa_brejo"), "bruxa")
        self.assertEqual(retrato(FAMILIAS["rato"]["tracos"], "rato"), "rato")
        self.assertEqual(retrato(["humano", "conjurador"], "guardiao", "guardiao:4", "profeta_das_cinzas"), "profeta_das_cinzas")

    def test_javali_e_carnical_pela_familia(self):
        # 1.173.0: pela família (o cavaleiro sombrio tem o dele desde a 1.187.0; o Lich, o dele pelo id desde a 1.199.0)
        self.assertEqual(retrato(FAMILIAS["javali"]["tracos"], "javali"), "javali")
        self.assertEqual(retrato(FAMILIAS["carnical"]["tracos"], "carnical"), "carnical")

    def test_espectro_pela_familia(self):
        # 1.174.0: o espectro pela família; a cria do Vazio, também etérea, tem o retrato dela desde a 1.185.0; o Lich, que
        # ganha o etéreo na fase 2, tem o dele pelo id desde a 1.199.0, e o guardião etéreo sem id continua no traço
        self.assertEqual(retrato(FAMILIAS["espectro"]["tracos"], "espectro"), "espectro")
        self.assertEqual(retrato(FAMILIAS["cria_vazio"]["tracos"], "cria_vazio"), "cria_vazio")
        self.assertEqual(retrato(["morto-vivo", "conjurador", "etereo"], "guardiao", "guardiao:6", "lich_menor"), "lich_menor")
        self.assertEqual(retrato(["morto-vivo", "conjurador", "etereo"], "guardiao", "guardiao:6"), "etereo")

    def test_esqueleto_pela_familia(self):
        # 1.175.0: o esqueleto pela família (os do ossuário e os que o Lich invoca, que são da família); o guardião
        # morto-vivo sem id continua na caveira; o Lich tem o dele desde a 1.199.0 (a família `esqueleto_servo`, que nada
        # criava, saiu do catálogo na 1.199.1)
        self.assertEqual(retrato(FAMILIAS["esqueleto"]["tracos"], "esqueleto"), "esqueleto")
        import random
        from rpg.inimigos import GUARDIOES, criar
        lich = next(x for lista in GUARDIOES.values() for x in lista if x["id"] == "lich_menor")
        self.assertEqual(lich["invoca"], "esqueleto")  # os invocados do Lich são da família
        invocado = criar(random.Random(3), lich["invoca"], 4)  # como o Invocar do Lich faz
        self.assertEqual(retrato(invocado.tracos, invocado.familia, invocado.chave), "esqueleto")
        self.assertEqual(retrato(["morto-vivo"], None), "caveira")
        self.assertEqual(retrato(["morto-vivo", "conjurador"], "guardiao", "guardiao:6", "lich_menor"), "lich_menor")
        self.assertEqual(retrato(["morto-vivo", "conjurador"], "guardiao", "guardiao:6"), "caveira")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('esqueleto: "retrato-esqueleto"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-esqueleto-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_mercenario_e_lobo_gelido_pela_familia(self):
        # 1.179.0: pela família, com os de nome próprio da família (o Invicto da ponte, o Theodore dos Cães de Ferro) e
        # os afixos; o Senhor da Guerra (guardião humano, com o dele pelo id desde a 1.194.0) não é da família
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["mercenario"]["tracos"], "mercenario"), "mercenario")
        self.assertEqual(retrato(FAMILIAS["lobo_gelido"]["tracos"], "lobo_gelido"), "lobo_gelido")
        for fam, afixo, nome in (("mercenario", None, "Theodore, o Ruivo"), ("mercenario", "feroz", "Varn"),
                                 ("lobo_gelido", "feroz", None)):
            e = criar(random.Random(2), fam, 4, afixo, nome)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), fam, (fam, afixo, nome))
        self.assertEqual(retrato(["humano", "blindado"], "guardiao", "guardiao:5", "senhor_da_guerra"), "senhor_da_guerra")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        for papel, arquivo in (("mercenario", "retrato-mercenario"), ("lobo_gelido", "retrato-lobo-gelido")):
            self.assertIn(f'{papel}: "{arquivo}"', icones)
            for lado in (16, 32, 48):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/{arquivo}-{lado}{sufixo}.png").exists(), (arquivo, lado))

    def test_caido_pela_familia(self):
        # 1.182.0: o caído pela família, com os que o xamã ergue (o Reviver levanta o mesmo caído morto); o xamã caído
        # (família própria) tem o retrato dele desde a 1.184.0; o cão infernal, desde a 1.186.0
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["caido"]["tracos"], "caido"), "caido")
        self.assertEqual(FAMILIAS["xama_caido"]["revive"], "caido")
        caido = criar(random.Random(5), "caido", 3, "feroz")
        self.assertEqual(retrato(caido.tracos, caido.familia, caido.chave), "caido")
        self.assertEqual(retrato(FAMILIAS["cao_infernal"]["tracos"], "cao_infernal"), "cao_infernal")
        # o reerguido: o Reviver do xamã levanta o mesmo caído morto, que continua com o retrato da família
        from rpg.inimigos import HABS_INIMIGO
        xama = criar(random.Random(6), "xama_caido", 3)
        caido.hp = 0

        class Luta:
            inimigos, mortos, rng = [xama, caido], [caido], random.Random(1)

            def dizer(self, *_):
                pass
        luta = Luta()
        HABS_INIMIGO["reviver"](luta, xama, None)
        self.assertTrue(caido.vivo and caido not in luta.mortos)
        self.assertEqual(retrato(caido.tracos, caido.familia, caido.chave), "caido")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('caido: "retrato-caido"', icones)

    def test_grifo_pela_familia(self):
        # 1.183.0: o grifo pela família, também o feroz do ninho; o guardião voador sem retrato próprio continua no "voador"
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["grifo"]["tracos"], "grifo"), "grifo")
        grifo = criar(random.Random(4), "grifo", 4, "feroz")  # como o ninho de grifo faz
        self.assertEqual(retrato(grifo.tracos, grifo.familia, grifo.chave), "grifo")
        self.assertEqual(retrato(["voador"], "guardiao", "guardiao:4"), "voador")  # o voador sem retrato próprio
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('grifo: "retrato-grifo"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-grifo-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_harpia_e_xama_caido_pela_familia(self):
        # 1.184.0: a harpia e o xamã caído pela família, com os afixos; o xamã que escolta o bando de caídos é da
        # família dele (o retrato do xamã ao lado dos caídos); o voador sem retrato próprio continua nos traços
        import random
        from rpg.inimigos import criar
        self.assertEqual(FAMILIAS["caido"]["escolta"]["familia"], "xama_caido")
        for fam, afixo in (("harpia", None), ("harpia", "flamejante"), ("xama_caido", None), ("xama_caido", "feroz")):
            e = criar(random.Random(7), fam, 4, afixo)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), fam, (fam, afixo))
        self.assertEqual(retrato(["voador"], "guardiao", "guardiao:4"), "voador")  # o voador sem retrato próprio
        self.assertEqual(retrato(["demonio", "fera"], None), "demonio")  # o demônio sem família continua no sprite
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        for papel, arquivo in (("harpia", "retrato-harpia"), ("xama_caido", "retrato-xama-caido")):
            self.assertIn(f'{papel}: "{arquivo}"', icones)
            for lado in (16, 32, 48):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/{arquivo}-{lado}{sufixo}.png").exists(), (arquivo, lado))

    def test_cria_do_vazio_pela_familia_e_invocada(self):
        # 1.185.0: a cria do Vazio pela família, com os afixos, o "Gato do Vazio" do aprendiz (a família com outro nome) e
        # as que o antagonista invoca (o Invocar cria pela mesma família); o antagonista continua no "humano" e quem só
        # tem o traço etéreo continua no "etereo"
        import random
        from rpg.inimigos import _invocar, criar, instanciar_antagonista
        for afixo in (None, "feroz"):
            e = criar(random.Random(8), "cria_vazio", 4, afixo)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), "cria_vazio", afixo)
        # um do catálogo (guardado para a expansão desde a retirada do mundo gerado)
        ant = instanciar_antagonista({"nome": "Vharuk, o Rei Enforcado", "curto": "o Rei Enforcado", "g": "m",
                                      "origem": "um herói que voltou errado"}, 6)
        self.assertEqual(retrato(ant.tracos, ant.familia, getattr(ant, "chave", None)), "humano")

        class Luta:
            inimigos, rng = [ant], random.Random(1)

            class ui:
                letras_nos_alvos = True

            def inimigos_vivos(self):
                return self.inimigos

            def dizer(self, *_):
                pass
        luta = Luta()
        _invocar(luta, ant, None)
        invocada = luta.inimigos[-1]
        self.assertTrue(invocada.invocado and "(invocado)" in invocada.nome)
        self.assertEqual(retrato(invocada.tracos, invocada.familia, invocada.chave), "cria_vazio")
        self.assertEqual(retrato(["etereo"], None), "etereo")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('cria_vazio: "retrato-cria-vazio"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-cria-vazio-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_cao_infernal_pela_familia(self):
        # 1.186.0: o cão infernal pela família, com os afixos; quem tem o traço demônio sem família continua no sprite
        import random
        from rpg.inimigos import criar
        for afixo in (None, "feroz", "flamejante"):
            e = criar(random.Random(9), "cao_infernal", 4, afixo)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), "cao_infernal", afixo)
        self.assertEqual(retrato(["demonio"], None), "demonio")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('cao_infernal: "retrato-cao-infernal"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-cao-infernal-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_cavaleiro_sombrio_pela_familia(self):
        # 1.187.0: o cavaleiro sombrio pela família, com os afixos e o Último Guarda (chefes.py: o cavaleiro de nome
        # próprio da mesma família); os outros mortos-vivos sem retrato próprio continuam na caveira
        import random
        from rpg.inimigos import criar
        for afixo in (None, "feroz"):
            e = criar(random.Random(11), "cavaleiro_sombrio", 6, afixo)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), "cavaleiro_sombrio", afixo)
        guarda = criar(random.Random(12), "cavaleiro_sombrio", 9, None, "Varn")  # como o Último Guarda é criado
        self.assertEqual(retrato(guarda.tracos, guarda.familia, guarda.chave), "cavaleiro_sombrio")
        self.assertEqual(retrato(["morto-vivo"], None), "caveira")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('cavaleiro_sombrio: "retrato-cavaleiro-sombrio"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-cavaleiro-sombrio-{lado}{sufixo}.png").exists(),
                                (lado, sufixo))

    def test_abominacao_pela_familia(self):
        # 1.188.0: a abominação pela família, com os afixos; o sprite "corrompido" continua para quem tem o traço sem
        # retrato próprio (desde a 1.189.0 a Árvore Desperta tem o dela; o Espantalho Possuído corrompido segue no sprite)
        import random
        from rpg.inimigos import criar
        for afixo in (None, "feroz", "corrompido"):
            e = criar(random.Random(13), "abominacao", 6, afixo)
            self.assertEqual(retrato(e.tracos, e.familia, e.chave), "abominacao", afixo)
        self.assertEqual(retrato(["planta", "blindado", "corrompido"], None), "corrompido")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('abominacao: "retrato-abominacao"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-abominacao-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_arvore_desperta_e_golem_pela_familia(self):
        # 1.189.0: a árvore desperta e o golem de pedra pela família, com os afixos e o líder de nome próprio; a Árvore
        # Anciã tem o dela desde a 1.190.0 e o Golem Primordial desde a 1.191.0 (pelo id)
        import random
        from rpg.inimigos import criar
        for fam, desenho in (("ent_jovem", "arvore_desperta"), ("golem", "golem")):
            for afixo in (None, "feroz", "corrompido"):
                e = criar(random.Random(15), fam, 5, afixo)
                self.assertEqual(retrato(e.tracos, e.familia, e.chave, e.guardiao, e.origem), desenho, (fam, afixo))
            lider = criar(random.Random(16), fam, 6, "feroz", "Varn")
            self.assertEqual(retrato(lider.tracos, lider.familia, lider.chave, lider.guardiao, lider.origem), desenho)
        self.assertEqual(retrato(["planta", "blindado"], "guardiao", "guardiao:2", "ent_anciao"), "arvore_ancia")
        self.assertEqual(retrato(["construto", "blindado"], "guardiao", "guardiao:5", "golem_primordial"), "golem_primordial")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        for papel, arquivo in (("arvore_desperta", "retrato-arvore-desperta"), ("golem", "retrato-golem")):
            self.assertIn(f'{papel}: "{arquivo}"', icones)
            for lado in (16, 32, 48):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/{arquivo}-{lado}{sufixo}.png").exists(), (arquivo, lado))

    def test_espantalho_e_mimico_pela_origem(self):
        # 1.189.0: a origem que o evento marca (não o nome exibido) tira o retrato da família do Espantalho Possuído (os
        # números da árvore desperta) e do Mímico (os do golem); a família e os números continuam os dela. 1.192.0: o
        # Mímico tem o dele, pela origem; 1.195.0: o Espantalho também (antes, pelos traços)
        import random
        from rpg.eventos.biomas import espantalho
        from rpg.eventos.comuns import bau_abandonado
        from rpg.inimigos import criar

        class Jogo:  # o bastante dos dois eventos: as escolhas, a sorte e a luta, que só guarda o inimigo
            def __init__(self, escolha, perigo=2):
                self.rng, self.escolha, self.loc, self.lutas = random.Random(4), escolha, {"perigo": perigo}, []
                self.j = type("J", (), {"nivel": 5, "classe": "guerreiro"})()

            def dizer(self, *a, **k):
                pass

            def menu(self, texto, opcoes):
                return self.escolha

            def chance(self, p):
                return True

            def sortear(self, lista):
                return lista[0]

            def inimigo(self, familia, afixo=None):
                return criar(self.rng, familia, 5, afixo)

            def combate(self, inimigos, **k):
                self.lutas.append(inimigos[0])

        for perigo in (2, 5):  # feroz longe da Fenda, corrompido perto: o mesmo retrato
            g = Jogo("fogo", perigo)
            espantalho(g)
            e = g.lutas[0]
            self.assertEqual((e.familia, e.origem, e.nome), ("ent_jovem", "espantalho", "Espantalho Possuído"))
            self.assertEqual(retrato(e.tracos, e.familia, e.chave, e.guardiao, e.origem), "espantalho")
        g = Jogo("cuidado")
        bau_abandonado(g)
        m = g.lutas[0]
        self.assertEqual((m.familia, m.origem, m.nome), ("golem", "mimico", "Mímico"))
        self.assertEqual(retrato(m.tracos, m.familia, m.chave, m.guardiao, m.origem), "mimico")
        # o nome exibido não decide: um golem comum chamado "Mímico" continua com o retrato do golem; e a ficha da luta
        # (a carta) repassa a origem ao retrato
        golem = criar(random.Random(17), "golem", 5)
        golem.nome = "Mímico"
        self.assertEqual(retrato(golem.tracos, golem.familia, golem.chave, golem.guardiao, golem.origem), "golem")
        estado = (ESTATICO.parent / "estado.py").read_text(encoding="utf-8")
        self.assertIn('getattr(c, "guardiao", None), getattr(c, "origem", None))', estado)

    def test_arvore_ancia_pelo_guardiao(self):
        # 1.190.0: a Árvore Anciã pelo id da guardiã (ent_anciao), como o guardião é instanciado no covil, em qualquer
        # nome próprio; a árvore desperta comum e o Espantalho Possuído continuam como estavam
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Thorn, a Árvore Anciã", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "ent_anciao")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual((g.familia, g.guardiao), ("guardiao", "ent_anciao"))
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "arvore_ancia")
        self.assertEqual(retrato(["planta", "blindado"], "ent_jovem"), "arvore_desperta")
        self.assertEqual(retrato(["planta", "blindado"], "ent_jovem", origem="espantalho"), "espantalho")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('arvore_ancia: "retrato-arvore-ancia"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-arvore-ancia-{lado}{sufixo}.png").exists(), (lado, sufixo))
        self.assertFalse((ESTATICO / "hud/icones/retrato-arvore-ancia-48.png").exists())  # sem derivado sem uso

    def test_golem_primordial_pelo_guardiao(self):
        # 1.191.0: o Golem Primordial pelo id do guardião, em qualquer nome próprio; o golem de pedra comum e o Mímico
        # continuam como estavam
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Morn, o Golem Primordial", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "golem_primordial")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "golem_primordial")
        self.assertEqual(retrato(["construto", "blindado"], "golem"), "golem")
        self.assertEqual(retrato(["construto"], "golem", origem="mimico"), "mimico")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('golem_primordial: "retrato-golem-primordial"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-golem-primordial-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-golem-primordial-48.png").exists())  # sem derivado sem uso

    def test_mimico_pela_origem(self):
        # 1.192.0: o Mímico pela origem, não pelo nome nem pela família (que continua a do golem, com os números, os
        # contratos e o Bestiário dele); outra origem sem retrato próprio continua nos traços
        self.assertEqual(retrato(["construto", "blindado"], "golem", origem="mimico"), "mimico")
        self.assertEqual(retrato(["construto", "blindado"], "golem"), "golem")
        self.assertEqual(retrato(["planta"], "ent_jovem", origem="espantalho"), "espantalho")
        self.assertEqual(retrato(["planta"], "ent_jovem", origem="outra"), "planta")  # origem sem retrato: os traços
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('mimico: "retrato-mimico"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-mimico-{lado}{sufixo}.png").exists(), (lado, sufixo))
        self.assertFalse((ESTATICO / "hud/icones/retrato-mimico-48.png").exists())  # sem derivado sem uso

    def test_dragao_de_gelo_pelo_guardiao(self):
        # 1.193.0: o Dragão de Gelo pelo id do guardião, em qualquer nome próprio; o grifo e a harpia (os outros voadores)
        # continuam com os deles, e o voador sem retrato próprio no sprite do traço
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Vyr, o Dragão de Gelo", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "dragao_de_gelo")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "dragao_de_gelo")
        self.assertEqual(retrato(FAMILIAS["grifo"]["tracos"], "grifo"), "grifo")
        self.assertEqual(retrato(["voador"]), "voador")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('dragao_de_gelo: "retrato-dragao-de-gelo"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-dragao-de-gelo-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-dragao-de-gelo-48.png").exists())  # sem derivado sem uso

    def test_senhor_da_guerra_pelo_guardiao(self):
        # 1.194.0: o Senhor da Guerra pelo id do guardião, em qualquer nome próprio; o mercenário e o bandido continuam com
        # os deles, e o antagonista (humano sem retrato próprio) no sprite do traço; o Profeta tem o dele desde a 1.198.0
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Varn, o Senhor da Guerra", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "senhor_da_guerra")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "senhor_da_guerra")
        self.assertEqual(retrato(FAMILIAS["mercenario"]["tracos"], "mercenario"), "mercenario")
        self.assertEqual(retrato(FAMILIAS["bandido"]["tracos"], "bandido"), "bandido")
        self.assertEqual(retrato(["humano", "conjurador"], "guardiao", "guardiao:4"), "humano")  # o humano sem retrato
        self.assertEqual(retrato(["humano"]), "humano")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('senhor_da_guerra: "retrato-senhor-da-guerra"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-senhor-da-guerra-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-senhor-da-guerra-48.png").exists())  # sem derivado sem uso

    def test_espantalho_pela_origem(self):
        # 1.195.0: o Espantalho Possuído pela origem que o evento do milharal marca, não pelo nome nem pela família (que
        # continua a da árvore desperta, com os números dela); a árvore desperta comum continua com o retrato da família
        self.assertEqual(retrato(["planta", "blindado"], "ent_jovem", origem="espantalho"), "espantalho")
        self.assertEqual(retrato(["corrompido", "planta"], "ent_jovem", origem="espantalho"), "espantalho")
        self.assertEqual(retrato(["planta", "blindado"], "ent_jovem"), "arvore_desperta")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('espantalho: "retrato-espantalho"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-espantalho-{lado}{sufixo}.png").exists(), (lado, sufixo))
        self.assertFalse((ESTATICO / "hud/icones/retrato-espantalho-48.png").exists())  # sem derivado sem uso

    def test_urso_pardo_do_abrigo_pela_origem(self):
        # 1.201.5: o Urso Pardo do abrigo da tempestade é um javali robusto com outro nome (a família, os números e as
        # habilidades do javali); o retrato vinha da família e mostrava o javali. Pela origem que o evento marca, ele tem
        # a cabeça do urso (o arquivo do urso do patrulheiro); o sapo do pântano, o javali comum e o urso aliado não mudam
        import random
        from rpg.eventos.biomas import abrigo_da_tempestade
        from rpg.inimigos import criar

        class Jogo:  # o bastante do evento: a sorte, o lugar e a luta, que só guarda o inimigo
            def __init__(self, bioma):
                self.rng, self.bioma, self.lutas = random.Random(4), bioma, []
                self.j = type("J", (), {"nivel": 3, "spec": None, "max_hp": 40})()

            def dizer(self, *a, **k):
                pass

            def chance(self, p):
                return True

            def inimigo(self, familia, afixo=None):
                return criar(self.rng, familia, 3, afixo)

            def combate(self, inimigos, **k):
                self.lutas.append(inimigos[0])

        g = Jogo("floresta")
        abrigo_da_tempestade(g)
        urso = g.lutas[0]
        self.assertEqual((urso.nome, urso.familia, urso.origem), ("Urso Pardo", "javali", "urso"))
        self.assertEqual(retrato(urso.tracos, urso.familia, urso.chave, urso.guardiao, urso.origem), "urso")
        javali = criar(random.Random(4), "javali", 3, "robusto")  # os mesmos números do javali robusto de antes
        self.assertEqual((urso.max_hp, urso.atk, urso.agi, urso.tracos, urso.habilidades),
                         (javali.max_hp, javali.atk, javali.agi, javali.tracos, javali.habilidades))
        self.assertEqual(retrato(javali.tracos, javali.familia, javali.chave, javali.guardiao, javali.origem), "javali")
        g = Jogo("pantano")
        abrigo_da_tempestade(g)
        sapo = g.lutas[0]
        self.assertEqual((sapo.familia, sapo.origem), ("sapo", None))
        self.assertEqual(retrato(sapo.tracos, sapo.familia, sapo.chave, sapo.guardiao, sapo.origem), "sapo")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('urso: "retrato-urso"', re.search(r"const CRIATURA = \{([^}]*)\}", icones).group(1))
        self.assertIn('urso: "retrato-urso"', re.search(r"const ANIMAL = \{([^}]*)\}", icones).group(1))
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-urso-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_hidra_do_brejo_pelo_guardiao(self):
        # 1.197.0: a Hidra do Pântano pelo id da guardiã, em qualquer nome próprio; o sapo e a sanguessuga (os outros do
        # pântano) continuam com os deles, e a fera sem retrato próprio no sprite do traço
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Nhaga, a Hidra do Pântano", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "hidra_do_brejo")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "hidra_do_brejo")
        self.assertEqual(retrato(FAMILIAS["sapo"]["tracos"], "sapo"), "sapo")
        self.assertEqual(retrato(["fera"]), "fera")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('hidra_do_brejo: "retrato-hidra-do-brejo"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-hidra-do-brejo-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-hidra-do-brejo-48.png").exists())  # sem derivado sem uso

    def test_profeta_das_cinzas_pelo_guardiao(self):
        # 1.198.0: o Profeta das Cinzas pelo id do guardião, em qualquer nome próprio; o cultista (os fiéis que ele
        # invoca) continua com o dele, e o humano sem retrato próprio (o antagonista) no sprite do traço
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        spec = next(dict(s, nome="Asmun, o Profeta das Cinzas", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "profeta_das_cinzas")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "profeta_das_cinzas")
        self.assertEqual(retrato(FAMILIAS["cultista"]["tracos"], "cultista"), "cultista")
        self.assertEqual(retrato(["humano", "conjurador"]), "humano")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('profeta_das_cinzas: "retrato-profeta-das-cinzas"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-profeta-das-cinzas-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-profeta-das-cinzas-48.png").exists())  # sem derivado sem uso

    def test_lich_menor_pelo_guardiao_nas_duas_fases(self):
        # 1.199.0: o Lich Menor pelo id do guardião, em qualquer nome próprio; na fase 2 ele ganha o traço etéreo, e o
        # retrato continua o dele (o id vem antes dos traços); os esqueletos que ele invoca continuam com o da família
        import random
        from rpg.combate import Combate
        from rpg.dados import GUARDIOES
        from rpg.inimigos import criar, instanciar_guardiao
        from tests.test_rei_dos_mortos import necromante
        spec = next(dict(s, nome="Morgath, o Lich Menor", bioma=b) for b, ls in GUARDIOES.items() for s in ls
                    if s["id"] == "lich_menor")
        g = instanciar_guardiao(spec, 6)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "lich_menor")
        jogo = necromante()
        cb = Combate(jogo, [g])
        g.hp = int(g.max_hp * 0.4)  # abaixo do limiar da fase 2
        cb.checar_fase(g)
        self.assertIn("etereo", g.tracos)
        self.assertEqual(retrato(g.tracos, g.familia, g.chave, g.guardiao, g.origem), "lich_menor")
        invocado = criar(random.Random(3), spec["invoca"], 4)  # como o Invocar do Lich faz
        self.assertEqual(retrato(invocado.tracos, invocado.familia, invocado.chave), "esqueleto")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('lich_menor: "retrato-lich-menor"', icones)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-lich-menor-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-lich-menor-48.png").exists())  # sem derivado sem uso

    def test_troll_pela_familia_e_o_rei_pelo_guardiao(self):
        # o troll da montanha pela família (1.166.0); o Rei Troll pelo id do guardião (1.167.0), em qualquer lugar
        self.assertEqual(retrato(FAMILIAS["troll"]["tracos"], "troll"), "troll")
        self.assertEqual(retrato(["gigante"], "guardiao", "guardiao:5", "rei_troll"), "rei_troll")
        self.assertEqual(retrato(["gigante"], "guardiao", "guardiao:5"), "caveira")

    def test_guardioes_instanciados_guardam_o_id(self):
        from rpg.dados import GUARDIOES, RETRATO_GUARDIAO
        from rpg.inimigos import instanciar_guardiao
        self.assertEqual(set(RETRATO_GUARDIAO), {"rei_troll", "rainha_aracnidea", "ent_anciao", "golem_primordial",
                                                 "dragao_de_gelo", "senhor_da_guerra", "hidra_do_brejo",
                                                 "profeta_das_cinzas", "lich_menor"})
        for bioma, lista in GUARDIOES.items():
            for t in lista:
                e = instanciar_guardiao({"bioma": bioma, "id": t["id"], "idx": 0, "nome": t["base"], "g": t["g"]}, 3)
                ret = retrato(e.tracos, e.familia, e.chave, e.guardiao)
                # o Rei, a Rainha Aracnídea, a Árvore Anciã (1.190.0), o Golem Primordial (1.191.0), o Dragão de Gelo (1.193.0)
                # o Senhor da Guerra (1.194.0), a Hidra do Pântano (1.197.0), o Profeta das Cinzas (1.198.0) e o Lich Menor
                # (1.199.0) têm o retrato deles,
                # pelo id; os outros guardiões
                # continuam pelos traços
                self.assertEqual(ret, RETRATO_GUARDIAO.get(t["id"]) or retrato(e.tracos), t["id"])

    def test_aranha_pela_familia_e_as_invocadas(self):
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["aranha"]["tracos"], "aranha"), "aranha")
        invocada = criar(random.Random(3), "aranha", 2)  # como o Invocar da Rainha faz
        self.assertEqual(retrato(invocada.tracos, invocada.familia, invocada.chave), "aranha")

    def test_os_outros_continuam_pelos_tracos(self):
        # os outros mortos-vivos seguem com a caveira (o esqueleto tem a dele desde a 1.175.0 e o cavaleiro sombrio desde
        # a 1.187.0); o guardião genérico da Bruxa Afogada também
        self.assertEqual(retrato(["morto-vivo", "blindado"], None), "caveira")
        self.assertEqual(retrato(["morto-vivo", "conjurador"], "guardiao", "guardiao:3"), "caveira")
        self.assertEqual(retrato(["fera"]), "fera")
        self.assertEqual(retrato([]), "caveira")
        for fam, f in FAMILIAS.items():
            if fam not in RETRATO_FAMILIA:
                self.assertEqual(retrato(f["tracos"], fam), retrato(f["tracos"]), fam)

    def test_cada_cabeca_propria_tem_arquivos_e_papel(self):
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        papel = re.search(r"const CRIATURA = \{([^}]*)\}", icones).group(1)
        for nome in set(RETRATO_CHAVE.values()) | set(RETRATO_FAMILIA.values()):
            arquivo = "retrato-" + nome.replace("_", "-")  # o arquivo com hífen, como o retrato-rainha-aracnidea
            self.assertIn(f'{nome}: "{arquivo}"', papel)
            self.assertIn(f'"{arquivo}": [16, 32, 48]', icones)
            for lado in (16, 32, 48):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/{arquivo}-{lado}{sufixo}.png").exists(), (nome, lado, sufixo))

    def test_animais_do_patrulheiro_pelo_tipo(self):
        # os três animais do herói têm cabeça (Icones.animal): o urso e o falcão próprias (1.164.0), o lobo o mesmo
        # arquivo do Lobo inimigo (1.165.0)
        from rpg.classes import COMPANHEIROS
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        papel = re.search(r"const ANIMAL = \{([^}]*)\}", icones).group(1)
        self.assertEqual(set(COMPANHEIROS), {"lobo", "urso", "falcao"})
        for tipo in COMPANHEIROS:
            self.assertIn(f'{tipo}: "retrato-{tipo}"', papel)
            self.assertRegex(icones, rf'"retrato-{tipo}": \[16, 32[\],]')
            for lado in (16, 32):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/retrato-{tipo}-{lado}{sufixo}.png").exists(), (tipo, lado))

    def test_figura_do_lobo_na_fogueira_pelo_tipo(self):
        # 1.170.0: o lobo do patrulheiro tem figura própria na fogueira (Icones.figuraAnimal, pelo tipo); 1.176.0: o urso e
        # o falcão também (os sprites "fera" e "voador" continuam para os traços e a carta sem retrato)
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        papel = re.search(r"const FIGURA_ANIMAL = \{([^}]*)\}", icones).group(1)
        self.assertEqual(papel.strip(), 'lobo: "figura-lobo", urso: "figura-urso", falcao: "figura-falcao"')
        for tipo in ("lobo", "urso", "falcao"):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/figura-{tipo}-16{sufixo}.png").exists(), (tipo, sufixo))
        acampamento = (ESTATICO / "telas" / "acampamento.js").read_text(encoding="utf-8")
        self.assertIn("Icones.figuraAnimal(f.tipo)", acampamento)
        self.assertIn('spr: d.fera.tipo === "falcao" ? "voador" : "fera", tipo: d.fera.tipo', acampamento)

    def test_atacar_pela_classe_com_os_arquivos_aprovados(self):
        # o Atacar da roda pelo icone_ataque da classe (com a Besta, o arco; com o Orbe, o cajado): a espada, o arco
        # (1.169.0) e o cajado (1.177.0) dos equipamentos, no papel ACAO
        from rpg.classes import CLASSES
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        papel = re.search(r"const ACAO = \{([^}]*)\}", icones).group(1)
        for classe, c in CLASSES.items():
            desenho = c["icone_ataque"]
            self.assertIn(f'{desenho}: "{desenho}"', papel, classe)
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/{desenho}-32{sufixo}.png").exists(), (classe, sufixo))


if __name__ == "__main__":
    unittest.main()
