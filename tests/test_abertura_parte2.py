"""A segunda parte da abertura guiada (roadmapIDEIAS/18, seção 15): V2 recuperar, V3 provisões, V4 comitiva, V5
explorar, E1 equipamento, T1 talentos e N1 noite. Uma por vez, quando fazem sentido; o que se cumpre não depende da
caixa; o jogo, as recompensas e o sorteio iguais com e sem tutorial; salvar e carregar sem repetir."""

import random
import tempfile
import unittest

from rpg import abertura as ab, comitiva as cm, itens
from rpg.jogo import Jogo
from rpg.regras import FimDeJogo
from tests.test_abertura import Jogador, jogo_sem_orientacao, nova, telas
from tests.test_missoes import ir


class Viajante(Jogador):
    """O roteiro nos menus; nos eventos do caminho (que não são menus do lugar), a última opção: recusar, seguir."""

    def escolher(self, pergunta, opcoes):
        try:
            return super().escolher(pergunta, opcoes)
        except FimDeJogo:
            if self.roteiro and not any(o.startswith(("Sair do jogo", "Voltar")) for o in opcoes):
                return len(opcoes) - 1
            raise


def depois_da_despensa(classe="guerreiro", tutorial=True, roteiro=(), pasta=None):
    """A campanha logo depois da despensa: a luta e o Mural já vistos."""
    g = nova(classe, tutorial, roteiro, pasta=pasta)
    a = g.mundo["abertura"]
    a.update(despensa="feita", caneca=False)
    a["vistas"] += ["combate", "V1"]
    g.contagem["morel_na_taverna"] = 1  # já encontrado: a abertura não o apresenta de novo
    return g


def oid(g):
    o = ab.atual(g)
    return o and o["id"]


class TestRecuperar(unittest.TestCase):
    def test_vida_baixa_aponta_o_templo_que_cabe_no_bolso(self):
        g = depois_da_despensa()
        g.j.hp = int(g.j.max_hp * 0.5)
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("V2", "predio:templo"))
        self.assertIn("devolve a vida toda", o["texto"])
        g.j.ouro = ab.preco_dormir(g)  # o templo custa mais do que isso: a taverna devolve parte da vida
        g.j.hp = 5
        o = ab.atual(g)
        self.assertEqual(o["ancora"], "predio:taverna")
        self.assertIn("35% da vida", o["texto"])

    def test_so_recurso_baixo_vai_para_a_taverna_nunca_para_o_templo(self):
        g = depois_da_despensa("mago")
        g.j.rec = 1
        o = ab.atual(g)
        self.assertEqual(o["ancora"], "predio:taverna")
        self.assertTrue(o["texto"].startswith("Pouca Mana. Dormir na **Taverna**"))
        self.assertIn("toda a Mana", o["texto"])
        self.assertNotIn("Templo", o["texto"])

    def test_os_dois_baixos_e_o_que_nao_promete(self):
        g = depois_da_despensa("arqueiro")
        g.j.hp, g.j.rec = int(g.j.max_hp * 0.5), 1
        g.j.ferimentos.append({"id": "perna", "dias": 3, "tratado": False})
        o = ab.atual(g)
        self.assertIn("Templo", o["texto"])
        self.assertIn("Pouco Foco: dormir na **Taverna**", o["texto"])
        self.assertIn("Ferimentos, a **Curandeira** trata.", o["texto"])  # o templo não trata ferimento

    def test_sem_ouro_nao_aponta_nada_e_nao_bloqueia(self):
        g = depois_da_despensa()
        g.j.hp, g.j.ouro = 5, 0
        self.assertNotEqual(oid(g), "V2")

    def test_usar_o_servico_ou_sair_da_vila_cumpre(self):
        g = depois_da_despensa()
        g.j.hp = 5
        antes = ab.proxima(g)
        ab.depois_do_menu(g, antes, "dormir")
        self.assertIn("V2", g.mundo["abertura"]["vistas"])
        g = depois_da_despensa()
        g.j.hp = 5
        ab.partiu(g)  # seguiu outro caminho: o quadro não persegue
        self.assertIn("V2", g.mundo["abertura"]["vistas"])

    def test_preco_de_dormir_e_o_do_menu(self):
        g = depois_da_despensa()
        self.assertEqual(ab.preco_dormir(g), g.preco(8 + 2 * g.j.nivel))


class TestProvisoes(unittest.TestCase):
    def test_na_primeira_viagem_com_o_consumo_da_comitiva(self):
        g = depois_da_despensa()
        self.assertNotEqual(oid(g), "V3")
        cm.recrutar(g, "morel")
        g.j.provisoes = 4
        ab.contexto(g, "viagem")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"], o["entendi"]), ("V3", "provisoes", True))
        self.assertIn("1 provisão sua e 1 de cada companheiro, na vila ou fora: dá 2 dias", o["texto"])
        self.assertIn("**Mercado**", o["texto"])  # dois dias é pouco

    def test_comida_suficiente_nao_empurra_o_mercado(self):
        g = depois_da_despensa()
        g.j.provisoes = 8
        ab.contexto(g, "viagem")
        self.assertNotIn("Mercado", ab.atual(g)["texto"])
        g.j.provisoes = 0
        self.assertIn("você não tem nenhuma", ab.atual(g)["texto"])

    def test_a_viagem_comecada_cumpre(self):
        g = depois_da_despensa()
        ab.partiu(g)
        ab.contexto(g, "viagem")
        self.assertIsNone(ab.atual(g))


class TestComitiva(unittest.TestCase):
    def test_o_primeiro_companheiro_qualquer_que_seja(self):
        g = depois_da_despensa()
        cm.recrutar(g, "odete")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("V4", "doca:Comitiva"))  # texto, destaque e seta no mesmo botão
        self.assertIn(f"**Comitiva** abre quem anda com você ({cm.nome('odete')})", o["texto"])

    def test_reserva_nao_conta(self):
        g = depois_da_despensa()
        cm.recrutar(g, "yara")
        cm.para_acampamento(g, "yara", silencioso=True)
        self.assertNotEqual(oid(g), "V4")
        cm.recrutar(g, "morel")
        self.assertEqual(oid(g), "V4")

    def test_abrir_a_comitiva_cumpre_sem_mexer_na_aprovacao(self):
        g = depois_da_despensa(roteiro=["Voltar"])
        cm.recrutar(g, "morel")
        aprovacao = cm.membro(g, "morel")["aprovacao"]
        g.executar_comum("comitiva")
        self.assertIn("V4", g.mundo["abertura"]["vistas"])
        self.assertEqual(cm.membro(g, "morel")["aprovacao"], aprovacao)


class TestExplorarNoiteTalentos(unittest.TestCase):
    def test_fora_da_vila_explorar_e_passa_com_a_resposta(self):
        g = depois_da_despensa()
        ir(g, "bosque_do_moinho")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("V5", "opcao:Explorar a região"))
        ab.depois_do_menu(g, ab.proxima(g), "acampar")
        self.assertIsNone(ab.atual(g))

    def test_noite_antes_de_explorar_e_a_capela_escura(self):
        g = depois_da_despensa()
        ir(g, "charco_dos_juncos")
        g.periodo = 3
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("N1", "mod:noite"))
        self.assertIn("sem ela, ser pego de surpresa fica mais provável", o["texto"])
        self.assertNotIn("com o mouse", o["texto"])
        ir(g, "capela_afogada")
        self.assertIn("sem tocha, cada sala começa com o inimigo atacando primeiro", ab.atual(g)["texto"])
        self.assertIn("a noite continua perigosa", ab.atual(g)["texto"])  # a tocha não tira a noite
        g.periodo = 1
        self.assertNotEqual(oid(g), "N1")  # de dia, a noite não tem o que dizer

    def test_talentos_so_com_ponto_por_gastar(self):
        g = depois_da_despensa()
        self.assertIsNone(ab.atual(g))
        g.j.pontos_talento = 1
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("T1", "doca:Talentos"))
        g.j.pontos_talento = 0  # gastou antes de ver: nada a apontar
        self.assertIsNone(ab.atual(g))
        g.j.pontos_talento = 2
        ab.depois_do_menu(g, ab.proxima(g), "passear")  # apareceu uma vez e a pessoa seguiu: não insiste
        self.assertIsNone(ab.atual(g))
        g = depois_da_despensa()
        g.j.pontos_talento = 1
        g.ui = Viajante([])
        g.menu_talentos = type(g).menu_talentos.__get__(g)
        g.ui.mostrar_talentos = lambda *a: None
        g.ui.roteiro = ["Voltar"]
        try:
            g.menu_talentos()  # abrir a árvore cumpre
        except FimDeJogo:
            pass
        self.assertIn("T1", g.mundo["abertura"]["vistas"])

    def test_uma_por_vez_preparar_antes_de_novidade(self):
        g = depois_da_despensa()
        cm.recrutar(g, "morel")
        g.j.pontos_talento = 1
        g.j.hp = 5
        g.mundo["abertura"]["vistas"].remove("V1")
        ordem = []
        for _ in range(4):
            o = ab.atual(g)
            ordem.append(o["id"])
            ab.visto(g, o["id"])
        self.assertEqual(ordem, ["V2", "V1", "T1", "V4"])


class TestEquipamento(unittest.TestCase):
    def test_so_na_comparacao_e_a_decisao_cumpre(self):
        g = depois_da_despensa(roteiro=["Guardar"])
        mostrado = []
        menu = g.menu
        g.menu = lambda p, o: (mostrado.append(ab.atual(g)), menu(p, o))[1]
        item = itens.gerar_equip(random.Random(4), g.j.classe, 1, slot="arma")
        g.oferecer_equip(item)
        self.assertEqual(mostrado[0]["id"], "E1")
        self.assertIn("**Equipar** veste o novo e guarda o antigo na mochila", mostrado[0]["texto"])
        self.assertIn("E1", g.mundo["abertura"]["vistas"])
        self.assertIn(item, g.j.mochila)  # a escolha foi da pessoa

    def test_sem_comparacao_nao_aparece(self):
        g = depois_da_despensa(roteiro=["Guardar"])
        mostrado = []
        menu = g.menu
        g.menu = lambda p, o: (mostrado.append(ab.atual(g)), menu(p, o))[1]
        g.oferecer_equip(itens.gerar_equip(random.Random(4), g.j.classe, 1, slot="pes"))  # espaço vazio
        self.assertIsNone(mostrado[0])
        self.assertNotIn("E1", g.mundo["abertura"]["vistas"])


class TestMotivoDeExplorar(unittest.TestCase):
    def test_o_taverneiro_conta_na_caneca_sem_morel(self):
        g = depois_da_despensa()
        g.mundo["abertura"]["caneca"] = True
        g.ouvir_rumores()
        self.assertEqual(sum("O dinheiro de verdade" in d for d in g.ui.ditos), 1)
        ir(g, "bosque_do_moinho")
        cm.recrutar(g, "morel")
        ab.motivo_explorar(g, "morel")
        self.assertEqual(sum("O dinheiro de verdade" in d for d in g.ui.ditos), 1)  # não repete

    def test_com_morel_e_ele_quem_conta_fora_da_vila(self):
        g = depois_da_despensa()
        cm.recrutar(g, "morel")
        g.mundo["abertura"]["caneca"] = True
        g.ouvir_rumores()
        self.assertFalse(any("O dinheiro de verdade" in d for d in g.ui.ditos))
        ir(g, "bosque_do_moinho")
        ab.motivo_explorar(g, "morel")
        self.assertTrue(any(d.startswith("Morel olha em volta") for d in g.ui.ditos))

    def test_sem_a_abertura_nada(self):
        g = depois_da_despensa()
        del g.mundo["abertura"]["despensa"]
        g.mundo["abertura"]["caneca"] = True
        ab.motivo_explorar(g, "taverneiro")
        self.assertFalse(any("O dinheiro de verdade" in d for d in g.ui.ditos))


class TestCaixaSalvarTexto(unittest.TestCase):
    ROTEIRO = ["Taverna: dormir", "Viajar", "[3]", "Explorar a região", "Viajar", "[1]"]

    def test_mesmo_jogo_com_e_sem_tutorial(self):
        for classe in ("guerreiro", "mago", "arqueiro"):
            jogos = []
            for tutorial in (True, False):
                g = depois_da_despensa(classe, tutorial)
                g.ui = Viajante(list(self.ROTEIRO))
                g.j.hp, g.j.pontos_talento = int(g.j.max_hp * 0.5), 1
                cm.recrutar(g, "morel")
                telas(g, 20)
                self.assertEqual(g.ui.roteiro, [], classe)  # foi, explorou e voltou
                jogos.append(jogo_sem_orientacao(g))
            self.assertEqual(jogos[0], jogos[1], classe)
            self.assertTrue({"V2", "V3", "T1"} <= set(g.mundo["abertura"]["vistas"]), classe)

    def test_entendi_so_nas_informativas(self):
        g = depois_da_despensa()
        ir(g, "bosque_do_moinho")
        ab.entendi(g, "V5")
        self.assertNotIn("V5", g.mundo["abertura"]["vistas"])
        ab.entendi(g, "N1")
        self.assertIn("N1", g.mundo["abertura"]["vistas"])

    def test_salvar_e_carregar_com_pendentes(self):
        pasta = tempfile.mkdtemp()
        g = depois_da_despensa(pasta=pasta)
        g.j.pontos_talento = 1
        ab.visto(g, "V3")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        self.assertEqual(oid(h), "T1")  # o que faltava continua
        self.assertIn("V3", h.mundo["abertura"]["vistas"])  # o que já foi não volta
        ab.contexto(h, "viagem")
        self.assertIsNone(ab.atual(h))

    def test_texto_diz_cada_dica_uma_vez(self):
        g = depois_da_despensa()
        g.ui.hud = False
        ir(g, "bosque_do_moinho")
        ab.dica_texto(g, "fora")
        ab.dica_texto(g, "fora")
        self.assertEqual(sum(d.startswith("Dica: \"Explorar a região\"") for d in g.ui.ditos), 1)


if __name__ == "__main__":
    unittest.main()
