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
        # as outras feras e os outros humanos continuam no desenho do traço
        for fam, tr in (("lobo_gelido", "fera"), ("mercenario", "humano")):
            self.assertEqual(retrato(FAMILIAS[fam]["tracos"], fam), tr, fam)

    def test_sapo_e_sanguessuga_pela_familia(self):
        # 1.171.0: o sapo-touro gigante e a sanguessuga gigante pela família; a Hidra do Brejo (guardiã) e as outras
        # feras continuam pelos traços
        self.assertEqual(retrato(FAMILIAS["sapo"]["tracos"], "sapo"), "sapo")
        self.assertEqual(retrato(FAMILIAS["sanguessuga"]["tracos"], "sanguessuga"), "sanguessuga")
        self.assertEqual(retrato(["fera"], "guardiao", "guardiao:3", "hidra_do_brejo"), "fera")
        self.assertEqual(retrato(FAMILIAS["lobo_gelido"]["tracos"], "lobo_gelido"), "fera")

    def test_cultista_bruxa_e_rato_pela_familia(self):
        # 1.172.0: pela família (o cultista também nos fiéis do Profeta e nos da sacristia, que são cultistas); o Profeta
        # das Cinzas (guardião), o mercenário e as outras feras continuam pelos traços
        self.assertEqual(retrato(FAMILIAS["cultista"]["tracos"], "cultista"), "cultista")
        self.assertEqual(retrato(FAMILIAS["bruxa_brejo"]["tracos"], "bruxa_brejo"), "bruxa")
        self.assertEqual(retrato(FAMILIAS["rato"]["tracos"], "rato"), "rato")
        self.assertEqual(retrato(["humano", "conjurador"], "guardiao", "guardiao:4", "profeta_das_cinzas"), "humano")

    def test_javali_e_carnical_pela_familia(self):
        # 1.173.0: pela família; o cavaleiro sombrio e o Lich (mortos-vivos) continuam na caveira
        self.assertEqual(retrato(FAMILIAS["javali"]["tracos"], "javali"), "javali")
        self.assertEqual(retrato(FAMILIAS["carnical"]["tracos"], "carnical"), "carnical")
        self.assertEqual(retrato(FAMILIAS["cavaleiro_sombrio"]["tracos"], "cavaleiro_sombrio"), "caveira")

    def test_espectro_pela_familia(self):
        # 1.174.0: o espectro pela família; a cria do Vazio (etérea) e o Lich, que ganha o etéreo na fase 2, continuam
        # pelos traços
        self.assertEqual(retrato(FAMILIAS["espectro"]["tracos"], "espectro"), "espectro")
        self.assertEqual(retrato(FAMILIAS["cria_vazio"]["tracos"], "cria_vazio"), "etereo")
        self.assertEqual(retrato(["morto-vivo", "conjurador", "etereo"], "guardiao", "guardiao:6", "lich_menor"), "etereo")

    def test_esqueleto_pela_familia(self):
        # 1.175.0: o esqueleto pela família (os do ossuário e os que o Lich invoca, que são da família); o servo
        # esquelético, o servo aliado do Necromante (sem família), o cavaleiro sombrio e o Lich continuam na caveira
        self.assertEqual(retrato(FAMILIAS["esqueleto"]["tracos"], "esqueleto"), "esqueleto")
        import random
        from rpg.inimigos import GUARDIOES, criar
        lich = next(x for lista in GUARDIOES.values() for x in lista if x["id"] == "lich_menor")
        self.assertEqual(lich["invoca"], "esqueleto")  # os invocados do Lich são da família
        invocado = criar(random.Random(3), lich["invoca"], 4)  # como o Invocar do Lich faz
        self.assertEqual(retrato(invocado.tracos, invocado.familia, invocado.chave), "esqueleto")
        self.assertEqual(retrato(FAMILIAS["esqueleto_servo"]["tracos"], "esqueleto_servo"), "caveira")
        self.assertEqual(retrato(["morto-vivo"], None), "caveira")
        self.assertEqual(retrato(["morto-vivo", "conjurador"], "guardiao", "guardiao:6", "lich_menor"), "caveira")
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('esqueleto: "retrato-esqueleto"', icones)
        for lado in (16, 32, 48):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-esqueleto-{lado}{sufixo}.png").exists(), (lado, sufixo))

    def test_troll_pela_familia_e_o_rei_pelo_guardiao(self):
        # o troll da montanha pela família (1.166.0); o Rei Troll pelo id do guardião (1.167.0), em qualquer lugar
        self.assertEqual(retrato(FAMILIAS["troll"]["tracos"], "troll"), "troll")
        self.assertEqual(retrato(["gigante"], "guardiao", "guardiao:5", "rei_troll"), "rei_troll")
        self.assertEqual(retrato(["gigante"], "guardiao", "guardiao:5"), "caveira")

    def test_guardioes_instanciados_guardam_o_id(self):
        from rpg.dados import GUARDIOES
        from rpg.inimigos import instanciar_guardiao
        for bioma, lista in GUARDIOES.items():
            for t in lista:
                e = instanciar_guardiao({"bioma": bioma, "id": t["id"], "idx": 0, "nome": t["base"], "g": t["g"]}, 3)
                ret = retrato(e.tracos, e.familia, e.chave, e.guardiao)
                # o Rei e a Rainha Aracnídea têm o retrato deles; os outros guardiões continuam pelos traços
                proprio = t["id"] in ("rei_troll", "rainha_aracnidea")
                self.assertEqual(ret, t["id"] if proprio else retrato(e.tracos), t["id"])

    def test_aranha_pela_familia_e_as_invocadas(self):
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["aranha"]["tracos"], "aranha"), "aranha")
        invocada = criar(random.Random(3), "aranha", 2)  # como o Invocar da Rainha faz
        self.assertEqual(retrato(invocada.tracos, invocada.familia, invocada.chave), "aranha")

    def test_os_outros_continuam_pelos_tracos(self):
        # os outros mortos-vivos seguem com a caveira (o esqueleto tem a dele desde a 1.175.0); o guardião genérico da
        # Bruxa Afogada também
        self.assertEqual(retrato(FAMILIAS["cavaleiro_sombrio"]["tracos"], "cavaleiro_sombrio"), "caveira")
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
            self.assertIn(f'{nome}: "retrato-{nome}"', papel)
            self.assertIn(f'"retrato-{nome}": [16, 32, 48]', icones)
            for lado in (16, 32, 48):
                for sufixo in ("", "@2x"):
                    self.assertTrue((ESTATICO / f"hud/icones/retrato-{nome}-{lado}{sufixo}.png").exists(), (nome, lado, sufixo))

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
