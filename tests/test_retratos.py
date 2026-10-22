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
        for fam, tr in (("lobo_gelido", "fera"), ("javali", "fera"), ("cultista", "humano"), ("mercenario", "humano")):
            self.assertEqual(retrato(FAMILIAS[fam]["tracos"], fam), tr, fam)

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
                # o Rei tem o retrato dele; a Rainha Aracnídea e os outros continuam pelos traços
                self.assertEqual(ret, "rei_troll" if t["id"] == "rei_troll" else retrato(e.tracos), t["id"])

    def test_aranha_pela_familia_e_as_invocadas(self):
        import random
        from rpg.inimigos import criar
        self.assertEqual(retrato(FAMILIAS["aranha"]["tracos"], "aranha"), "aranha")
        invocada = criar(random.Random(3), "aranha", 2)  # como o Invocar da Rainha faz
        self.assertEqual(retrato(invocada.tracos, invocada.familia, invocada.chave), "aranha")

    def test_os_outros_continuam_pelos_tracos(self):
        # o esqueleto e os outros mortos-vivos seguem com a caveira; o guardião genérico da Bruxa Afogada também
        self.assertEqual(retrato(FAMILIAS["esqueleto"]["tracos"], "esqueleto"), "caveira")
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


if __name__ == "__main__":
    unittest.main()
