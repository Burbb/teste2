"""O equipamento e os atributos da comitiva (1.213.0, comitiva/ficha.py): a regra única de vestir, tirar e trocar
peças, a bolsa do grupo, os pontos dos companheiros, a sugestão, o save e quem sai."""

import json
import random
import tempfile
import unittest

from rpg import comitiva
from rpg import atributos as atr
from rpg.combate import Combate
from rpg.comitiva import ficha
from rpg.grimorio import chance_critico
from rpg.jogo import Jogo
from rpg.migracoes import migrar
from rpg.regras import LIMITE_MOCHILA
from rpg.ui import BotUI

H = ficha.HEROI


def peca(nome, slot, classe=None, **bonus):
    return {"nome": nome, "base": nome, "slot": slot, "bonus": bonus or {"defesa": 1}, "classe": classe,
            "raridade": "comum", "icone": "saco", "nivel": 1, "preco": 10}


def jogo(classe="guerreiro", nivel=1, membros=("morel", "odete")):
    g = Jogo(BotUI(random.Random(1), max_decisoes=10 ** 6), seed=1, pasta_saves=tempfile.mkdtemp())
    g.iniciar("Teste", classe)
    g.j.nivel = nivel
    for cid in membros:
        comitiva.recrutar(g, cid)
    g.j.mochila = []
    return g


def todas_as_pecas(g):
    """Cada peça do grupo, pela identidade: na bolsa e nos corpos (nenhuma some, nenhuma se duplica)."""
    lista = list(g.j.mochila)
    for quem in ficha.personagens(g):
        lista += [it for it in ficha.corpo(g, quem).values() if it]
    return lista


class TestVestir(unittest.TestCase):
    def test_da_bolsa_no_companheiro_e_a_que_sai_fica_no_lugar(self):
        g = jogo()
        malha, couraca = peca("Malha", "armadura", "guerreiro", defesa=2), peca("Couraça", "armadura", "guerreiro", defesa=4)
        ficha.corpo(g, "morel")["armadura"] = malha
        g.j.mochila = [peca("Anel", "anel"), couraca, peca("Bota", "pes")]
        antes = comitiva.atributos(g, comitiva.membro(g, "morel"))["defesa"]
        ok, texto = ficha.vestir(g, "morel", couraca)
        self.assertTrue(ok, texto)
        self.assertIs(ficha.corpo(g, "morel")["armadura"], couraca)
        self.assertIs(g.j.mochila[1], malha)  # a que saiu ocupa o lugar exato da que entrou
        self.assertEqual(comitiva.atributos(g, comitiva.membro(g, "morel"))["defesa"], antes + 2)
        self.assertIn("Malha volta para a bolsa", texto)

    def test_classe_errada_explica_e_nada_muda(self):
        g = jogo()
        arco = peca("Arco", "arma", "arqueiro", atk=3)
        g.j.mochila = [arco]
        ok, texto = ficha.vestir(g, "morel", arco)
        self.assertFalse(ok)
        self.assertEqual(texto, "Morel não usa peças de arqueiro.")
        self.assertEqual(g.j.mochila, [arco])
        grimorio = peca("Grimório", "secundaria", "mago", poder=2)
        g.j.mochila.append(grimorio)
        self.assertTrue(ficha.vestir(g, "odete", grimorio)[0])
        self.assertEqual(ficha.vestir(g, H, peca("Sem dono", "pes"))[1], "Essa peça não está com o grupo.")

    def test_tirar_de_outro_personagem_resolve_tudo_ou_nada(self):
        g = jogo()
        elmo_heroi, elmo_morel = peca("Elmo do herói", "cabeca"), peca("Elmo do Morel", "cabeca")
        g.j.equip["cabeca"] = elmo_heroi
        ficha.corpo(g, "morel")["cabeca"] = elmo_morel
        g.j.mochila = [peca(f"P{i}", "pes") for i in range(LIMITE_MOCHILA)]  # cheia
        total = len(todas_as_pecas(g))
        ok, texto = ficha.vestir(g, "morel", elmo_heroi)
        self.assertFalse(ok)
        self.assertIn("A bolsa está cheia", texto)
        self.assertIs(g.j.equip["cabeca"], elmo_heroi)
        self.assertIs(ficha.corpo(g, "morel")["cabeca"], elmo_morel)
        g.j.mochila.pop()
        ok, texto = ficha.vestir(g, "morel", elmo_heroi)
        self.assertTrue(ok, texto)
        self.assertIsNone(g.j.equip["cabeca"])
        self.assertIs(ficha.corpo(g, "morel")["cabeca"], elmo_heroi)
        self.assertIs(g.j.mochila[-1], elmo_morel)
        self.assertIn("(era sua)", texto)
        self.assertEqual(len(todas_as_pecas(g)), total - 1)  # só a que saiu da bolsa antes do segundo pedido
        self.assertEqual(len({id(x) for x in todas_as_pecas(g)}), len(todas_as_pecas(g)))

    def test_aneis_respeitam_o_espaco_escolhido(self):
        g = jogo()
        a1, a2, novo = peca("Anel 1", "anel"), peca("Anel 2", "anel"), peca("Anel novo", "anel")
        ficha.corpo(g, "odete").update(anel1=a1, anel2=a2)
        g.j.mochila = [novo]
        ok, texto = ficha.vestir(g, "odete", novo)
        self.assertFalse(ok)
        self.assertEqual(texto, "Os dois anéis estão ocupados: escolha qual substituir.")
        self.assertTrue(ficha.vestir(g, "odete", novo, "anel2")[0])
        self.assertIs(ficha.corpo(g, "odete")["anel2"], novo)
        self.assertIs(ficha.corpo(g, "odete")["anel1"], a1)
        self.assertEqual(g.j.mochila, [a2])
        # trocar de dedo no mesmo corpo: os dois anéis trocam de lugar, nada vai para a bolsa
        self.assertTrue(ficha.vestir(g, "odete", a1, "anel2")[0])
        self.assertEqual((ficha.corpo(g, "odete")["anel1"], ficha.corpo(g, "odete")["anel2"]), (novo, a1))
        self.assertFalse(ficha.vestir(g, "odete", peca("Bota", "pes"), "anel1")[0])

    def test_tirar_precisa_de_espaco_na_bolsa(self):
        g = jogo()
        bota = peca("Bota", "pes")
        ficha.corpo(g, "morel")["pes"] = bota
        g.j.mochila = [peca(f"P{i}", "maos") for i in range(LIMITE_MOCHILA)]
        ok, texto = ficha.tirar(g, "morel", "pes")
        self.assertFalse(ok)
        self.assertIn("Libere um espaço antes de tirar Bota", texto)
        g.j.mochila.pop()
        self.assertTrue(ficha.tirar(g, "morel", "pes", posicao=0)[0])
        self.assertIs(g.j.mochila[0], bota)

    def test_indisponivel_e_luta(self):
        g = jogo()
        bota = peca("Bota", "pes")
        g.j.mochila = [bota]
        regra = lambda g, m: {"curto": "espera fora do Vau", "texto": "..."} if m["id"] == "odete" else None
        comitiva.AUSENCIAS.append(regra)
        try:
            ok, texto = ficha.vestir(g, "odete", bota)
            self.assertFalse(ok)
            self.assertEqual(texto, "Odette não está aqui: espera fora do Vau.")
        finally:
            comitiva.AUSENCIAS.remove(regra)
        comitiva.membro(g, "odete")["ferido"] = True  # o ferido pode ser equipado
        self.assertTrue(ficha.vestir(g, "odete", bota)[0])
        g.combate_ativo = object()
        try:
            self.assertEqual(ficha.tirar(g, "odete", "pes")[1], "Troque o equipamento fora da luta.")
        finally:
            g.combate_ativo = None

    def test_reordenar_a_bolsa(self):
        g = jogo()
        a, b, c = peca("A", "pes"), peca("B", "pes"), peca("C", "pes")
        g.j.mochila = [a, b, c]
        self.assertTrue(ficha.mover_na_bolsa(g, 0, 2))
        self.assertEqual(g.j.mochila, [b, c, a])
        self.assertFalse(ficha.mover_na_bolsa(g, 5, 0))
        self.assertEqual(g.j.mochila, [b, c, a])


class TestAtributos(unittest.TestCase):
    def test_pontos_na_entrada_tardia_e_por_nivel(self):
        g = jogo(nivel=5, membros=("yara",))
        m = comitiva.membro(g, "yara")
        self.assertEqual(m["pontos_atributo"], 4)  # os níveis que já passaram, livres
        self.assertEqual(m["atributos"], ficha.INICIAIS["yara"])
        g.subir_nivel()
        self.assertEqual(m["pontos_atributo"], 5)

    def test_sem_pontos_gastos_luta_como_antes(self):
        g = jogo(nivel=4)
        for m in comitiva.membros(g):
            d = comitiva.COMPANHEIROS[m["id"]]
            at = comitiva.atributos(g, m)
            self.assertEqual(at["max_hp"], int(d["base"]["hp"] + d["cresc"]["hp"] * 3))
            self.assertEqual(at["atk"], d["base"]["atk"] + d["cresc"]["atk"] * 3)
            self.assertEqual(at["agi"], d["base"]["agi"])
        cb = Combate(g, [g.inimigo("lobo", nivel=2)])
        comitiva.preparar_combate(cb)
        morel = next(a for a in cb.aliados if a.cid == "morel")
        self.assertEqual(morel.vontade, 3)
        self.assertAlmostEqual(atr.tenacidade(morel), 0.12)
        self.assertEqual(morel.max_rec, 40)

    def test_ponto_e_sugestao_so_nos_livres(self):
        g = jogo(nivel=4, membros=("odete",))
        m = comitiva.membro(g, "odete")
        self.assertTrue(ficha.gastar_atributo(g, "odete", "percepcao"))
        self.assertEqual(m["atributos"]["percepcao"], 4)
        self.assertEqual(ficha.distribuir_sugestao(g, "odete"), 2)
        self.assertEqual(m["pontos_atributo"], 0)
        self.assertEqual((m["atributos"]["vontade"], m["atributos"]["intelecto"], m["atributos"]["percepcao"]), (7, 7, 4))
        self.assertEqual(ficha.distribuir_sugestao(g, "odete"), 0)  # sem pontos: nada muda de novo
        self.assertEqual(m["atributos"]["percepcao"], 4)

    def test_atributos_e_pecas_valem_na_luta(self):
        g = jogo(nivel=3, membros=("morel",))
        m = comitiva.membro(g, "morel")
        ficha.gastar_atributo(g, "morel", "constituicao")
        ficha.gastar_atributo(g, "morel", "percepcao")
        self.assertEqual(m["max_hp"], comitiva.atributos(g, m)["max_hp"])
        g.j.mochila = [peca("Lâmina", "arma", "guerreiro", atk=3, critico=5)]
        ficha.vestir(g, "morel", g.j.mochila[0])
        cb = Combate(g, [g.inimigo("lobo", nivel=2)])
        comitiva.preparar_combate(cb)
        a = next(x for x in cb.aliados if x.cid == "morel")
        d = comitiva.COMPANHEIROS["morel"]
        self.assertEqual(a.max_hp, int(d["base"]["hp"] + d["cresc"]["hp"] * 2) + 4)
        sem = chance_critico(type("_", (), {"agi": a.agi, "equip": {}})())
        self.assertAlmostEqual(chance_critico(a) - sem, 0.01 + 0.05)

    def test_pecas_especiais_valem_para_o_companheiro(self):
        from tests.test_broquel import Sorteio
        g = jogo(nivel=3, membros=("morel",))
        g.j.mochila = [peca("Lâmina", "arma", "guerreiro", atk=2, roubo_vida=50),
                       peca("Malha", "armadura", "guerreiro", espinhos=5)]
        ficha.vestir(g, "morel", g.j.mochila[0])
        ficha.vestir(g, "morel", next(it for it in g.j.mochila if it["nome"] == "Malha"))
        lobo = g.inimigo("lobo", nivel=2)
        cb = Combate(g, [lobo])
        comitiva.preparar_combate(cb)
        cb.rng = Sorteio()
        a = next(x for x in cb.aliados if x.cid == "morel")
        a.hp = a.max_hp - 30
        cb.atacar(a, lobo, 1.0)
        self.assertGreater(a.hp, a.max_hp - 30)  # o roubo de vida da lâmina
        antes = lobo.hp
        cb.atacar(lobo, a, 1.0, alcance="corpo")
        self.assertLessEqual(lobo.hp, antes - 5)  # os espinhos da malha


class TestSaveESaida(unittest.TestCase):
    def test_save_antigo_ganha_pontos_livres_e_corpo_vazio(self):
        d = {"versao": 7, "seed": 1, "jogador": {"nivel": 6}, "comitiva": [{"id": "morel", "hp": 50, "max_hp": 50}],
             "reserva": [{"id": "yara", "hp": 30, "max_hp": 30}]}
        d = migrar(json.loads(json.dumps(d)))
        for m in d["comitiva"] + d["reserva"]:
            self.assertEqual(m["pontos_atributo"], 5)
            self.assertEqual(m["atributos"], ficha.INICIAIS[m["id"]])
            self.assertTrue(all(v is None for v in m["equip"].values()))
        de_novo = migrar(json.loads(json.dumps(dict(d, versao=7))))
        self.assertEqual(de_novo["comitiva"], d["comitiva"])

    def test_salvar_e_carregar_mantem_pecas_e_pontos(self):
        g = jogo(nivel=3, membros=("odete",))
        g.j.mochila = [peca("Manto", "armadura", defesa=2)]
        ficha.vestir(g, "odete", g.j.mochila[0])
        ficha.gastar_atributo(g, "odete", "vontade")
        g.salvar(silencioso=True)
        h = Jogo.carregar(BotUI(random.Random(1)), g.caminho_save(), g.pasta_saves)
        m = comitiva.membro(h, "odete")
        self.assertEqual(m["equip"]["armadura"]["nome"], "Manto")
        self.assertEqual((m["atributos"]["vontade"], m["pontos_atributo"]), (7, 1))

    def test_quem_sai_devolve_as_pecas(self):
        g = jogo()
        malha, bota = peca("Malha", "armadura", "guerreiro"), peca("Bota", "pes")
        ficha.corpo(g, "morel").update(armadura=malha, pes=bota)
        g.j.mochila = [peca(f"P{i}", "maos") for i in range(LIMITE_MOCHILA - 1)]
        ofertas = []
        g.oferecer_equip = ofertas.append
        comitiva.dispensar(g, "morel", silencioso=True)
        self.assertIs(g.j.mochila[-1], malha)  # o que cabe vai para a bolsa
        self.assertEqual(ofertas, [bota])  # o resto, como achado: a escolha é de quem joga
        self.assertEqual(len(g.j.mochila), LIMITE_MOCHILA)


if __name__ == "__main__":
    unittest.main()
