"""O retrato dos dois servos do Necromante (1.196.0). O "Esqueleto (Invocado)" do Erguer Servo e a criatura que o talento
Rei dos Mortos ergue são aliados do mesmo tipo "servo" (as mesmas regras); o desenho da carta vem do retrato que o motor
dá ao invocar, não do nome exibido: o do Erguer Servo, o crânio nu (`servo_esqueletico`); o erguido, o da criatura que
caiu (um lobo erguido continua um lobo). Os aliados só existem durante a luta: o save não os guarda."""

import pathlib
import unittest

from rpg.combate import Combate
from rpg.habilidades import _erguer_servo, _vida_servo
from rpg.web import estado
from tests.test_rei_dos_mortos import cair, necromante

ESTATICO = pathlib.Path(__file__).resolve().parents[1] / "rpg" / "web" / "static"


def ficha_aliado(g, a):
    return next(f for f in estado.combate(g)["aliados"] if f["nome"] == a.nome)


class TestServos(unittest.TestCase):
    def test_erguer_servo_leva_o_cranio_nu(self):
        g = necromante()
        cb = Combate(g, [g.inimigo("esqueleto", nivel=5)])
        g.combate_ativo = cb
        _erguer_servo(cb, g.j, None)
        servo = cb.aliados[-1]
        self.assertEqual((servo.nome, servo.tipo, servo.retrato), ("Esqueleto (Invocado)", "servo", "servo_esqueletico"))
        self.assertEqual(servo.max_hp, int(_vida_servo(g.j)))  # as regras como antes
        self.assertTrue(servo.efeito("provocando"))
        self.assertEqual(ficha_aliado(g, servo)["retrato"], "servo_esqueletico")
        # o esqueleto inimigo da mesma luta continua com o retrato da família
        self.assertEqual(estado.combate(g)["inimigos"][0]["retrato"], "esqueleto")
        # o nome exibido não decide
        servo.nome = "Ossos"
        self.assertEqual(ficha_aliado(g, servo)["retrato"], "servo_esqueletico")

    def test_rei_dos_mortos_mantem_a_criatura(self):
        g = necromante()
        lobo, outro = g.inimigo("lobo", nivel=5), g.inimigo("lobo", nivel=5)
        cb = Combate(g, [lobo, outro])
        g.combate_ativo = cb
        cair(cb, lobo)
        erguido = cb.aliados[-1]
        self.assertEqual((erguido.nome, erguido.tipo, erguido.retrato), (f"{lobo.nome} (servo)", "servo", "lobo"))
        self.assertEqual(erguido.max_hp, int(lobo.max_hp * 0.4))  # as regras como antes
        self.assertEqual(ficha_aliado(g, erguido)["retrato"], "lobo")
        # um esqueleto inimigo erguido é o esqueleto da família, não o servo do Erguer Servo, mesmo com o nome dele
        esq = g.inimigo("esqueleto", nivel=5)
        cb2 = Combate(g, [esq, g.inimigo("esqueleto", nivel=5)])
        g.combate_ativo = cb2
        esq.nome = "Esqueleto (Invocado)"
        cair(cb2, esq)
        self.assertEqual(cb2.aliados[-1].retrato, "esqueleto")

    def test_aliado_sem_retrato_continua_como_antes(self):
        g = necromante()
        cb = Combate(g, [g.inimigo("lobo", nivel=5)])
        g.combate_ativo = cb
        a = cb.invocar_aliado("Esqueleto (Invocado)", hp=60, atk=8, tipo="servo")  # como os cenários antigos
        self.assertIsNone(a.retrato)
        self.assertEqual(ficha_aliado(g, a)["retrato"], "caveira")

    def test_a_tela_desenha_o_que_o_motor_manda(self):
        icones = (ESTATICO / "icones.js").read_text(encoding="utf-8")
        self.assertIn('servo_esqueletico: "retrato-servo-esqueletico"', icones)
        batalha = (ESTATICO / "batalha.js").read_text(encoding="utf-8")
        self.assertIn('c.tipo === "servo" ? (c.retrato || "caveira")', batalha)
        for lado in (16, 32):
            for sufixo in ("", "@2x"):
                self.assertTrue((ESTATICO / f"hud/icones/retrato-servo-esqueletico-{lado}{sufixo}.png").exists(), lado)
        self.assertFalse((ESTATICO / "hud/icones/retrato-servo-esqueletico-48.png").exists())  # sem derivado sem uso


if __name__ == "__main__":
    unittest.main()
