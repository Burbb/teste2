"""A guardiã do Turvo (E3): Vó Berta e a fita, a descida ao fundo, Destruir ou Dar descanso, o piso do rito diante de
tudo o que tira vida (golpe forte, vários golpes, efeito periódico, comitiva, invocação, espinhos, execução), o desfecho
único com o Sigilo e a recompensa, a herança e os saves.

As lutas com a guardiã são de verdade: o robô lutador da arena (tests/arena.py) joga a luta, e só as perguntas da
missão (a descida, o momento do rito, o item achado) são respondidas pelo texto."""

import random
import tempfile
import unittest

from rpg import dev, itens, missoes
from rpg.combate import Combate
from rpg.inimigos import instanciar_guardiao
from rpg.jogo import Jogo
from rpg.regras import Derrota
from tests import arena
from tests.test_missoes import CLASSES, MID, Roteiro, fazer, ir, lutas, na_capela, opcoes_febre

ESPEC = {"bioma": "pantano", "id": "bruxa_afogada", "idx": 1, "nome": "Ilse, a Bruxa Afogada", "g": "f",
         "base": "Bruxa Afogada"}
TUDO = ["agua_do_leste", "represa", "canal_da_capela", "agua_da_capela", "ilse", "sigilo_do_turvo", "marcados",
        "correntes"]


class Lutador(arena.LutadorUI):
    """O robô lutador da arena, que responde as perguntas da missão pelo começo do texto (na ordem de preferência)."""

    def __init__(self, respostas=(), semente=3):
        super().__init__(random.Random(semente))
        self.respostas = list(respostas)
        self.perguntas, self.ditos = [], []

    def dizer(self, texto="", cor=None):
        self.ditos.append(str(texto))

    narrar = dizer

    def escolher(self, pergunta, opcoes):
        self.perguntas.append((pergunta, list(opcoes)))
        for alvo in self.respostas:
            for i, o in enumerate(opcoes):
                if o.startswith(alvo):
                    return i
        return super().escolher(pergunta, opcoes)


def no_fundo(classe="guerreiro", respostas=(), preparos=("corpo_solto",), berta=False, nivel=6, pasta=None):
    """Herói forte o bastante para vencer a guardiã, já no fundo da capela."""
    ui = Lutador(respostas)
    g = Jogo(ui, seed=13, pasta_saves=pasta or tempfile.mkdtemp(), hardcore=False)
    ui.g = g
    g.iniciar("Teste", classe, "turvo")
    dev.subir_ate(g, nivel)
    dev.vestir(g, random.Random(5), nivel)
    g.j.consumiveis["pocao_vida"] = 5
    m = missoes.registro(g, MID)
    m.update(etapa="fundo", cenas=["abertura", "capela_exterior"], pistas=list(TUDO), preparos=list(preparos))
    if berta:
        m["pistas"] += ["verdade_de_ilse", "nome_e_fita"]
    ir(g, "capela_afogada")
    g.periodo = 0
    return g


PRONTO = dict(preparos=("corpo_solto", "fita"), berta=True)
DESCANSO = ["Chamar Ilse pelo nome", "Dizer o nome dela", "Guardar"]
DESTRUIR = ["Lutar para destruí-la", "Guardar"]


class TestBerta(unittest.TestCase):
    def test_berta_so_depois_da_sacristia_e_uma_vez(self):
        g = na_capela(etapa="ossuario")
        ir(g, "vau_do_turvo")
        self.assertNotIn("berta", [o[1][2] for o in missoes.opcoes(g)])  # sem o nome de Ilse, ninguém a procura
        missoes.registro(g, MID)["pistas"].append("ilse")
        opcao = next(o for o in missoes.opcoes(g) if o[1][2] == "berta")
        self.assertEqual((opcao[2]["predio"], opcao[2]["curto"], opcao[2]["missao"]), ("taverna", "Falar com Vó Berta", MID))
        self.assertTrue(missoes.executar(g, MID, "berta"))
        m = missoes.registro(g, MID)
        self.assertEqual(m["pistas"][-2:], ["verdade_de_ilse", "nome_e_fita"])  # o que se sabe...
        self.assertEqual(m["preparos"], ["fita"])  # ...e o que se leva, à parte
        self.assertFalse(missoes.executar(g, MID, "berta"))  # a fita não se entrega duas vezes
        self.assertEqual((m["preparos"], len(m["pistas"])), (["fita"], 6))
        self.assertNotIn("berta", [o[1][2] for o in missoes.opcoes(g)])

    def test_diario_mostra_o_que_falta_para_o_rito(self):
        """O rito aparece no Diário depois de Vó Berta (é ela quem o conta), com o que já está feito marcado."""
        g = na_capela(etapa="ossuario")
        m = missoes.registro(g, MID)
        m["pistas"].append("ilse")
        self.assertIsNone(missoes.cartoes(g)[0]["requisitos"])  # saber de Ilse não ensina o rito
        m["preparos"] += ["corpo_solto"]
        m["pistas"] += ["verdade_de_ilse", "nome_e_fita"]
        lista = missoes.cartoes(g)[0]["requisitos"]["itens"]
        self.assertEqual([r["feito"] for r in lista], [True, False, True])
        m["preparos"] += ["fita"]
        self.assertTrue(missoes.descanso_pronto(m))
        m["desfecho"] = "destruida"
        self.assertIsNone(missoes.cartoes(g)[0]["requisitos"])  # resolvida: a lista some


class TestPisoDoRito(unittest.TestCase):
    """O piso vale para tudo que tira vida; o momento vem uma vez; desistir devolve o dano retido."""

    def luta(self, classe="mago"):
        g = no_fundo(classe)
        chefe = instanciar_guardiao(ESPEC, 4)
        chefe.piso = int(chefe.max_hp * chefe.fases[0]["limiar"])
        momentos = []
        chefe.ao_limiar = lambda cb, e: momentos.append(e.hp)
        cb = Combate(g, [chefe])
        return g, cb, chefe, momentos

    def test_nada_passa_do_piso(self):
        g, cb, e, momentos = self.luta()
        piso = e.piso
        cb.atacar(g.j, e, 50.0)  # um golpe que mataria várias vezes
        self.assertEqual(e.hp, piso)
        self.assertTrue(e.vivo)
        self.assertGreater(e.retido, 0)
        for _ in range(3):  # vários golpes seguidos
            cb.atacar(g.j, e, 2.0)
        e.aplicar("queimadura", 3, 40)  # efeito periódico
        cb.processar_efeitos(e)
        servo = cb.invocar_aliado("Esqueleto", 40, 30)  # invocação
        cb.atacar(servo, e, 3.0)
        e.hp = 0  # execução, roubo de vida ao contrário, o que for: a atribuição é uma só
        self.assertEqual(e.hp, piso)
        cb.checar_limiares()
        cb.checar_limiares()
        self.assertEqual(momentos, [piso])  # o momento vem uma vez
        g.combate_ativo = None

    def test_espinhos_e_comitiva_tambem_param_no_piso(self):
        g, cb, e, _ = self.luta("guerreiro")
        from rpg import comitiva as cm
        cm.recrutar(g, "morel")
        e.hp = e.piso + 1
        g.j.equip["armadura"] = itens.fazer_unico(itens.UNICOS_POR_ID["pele_do_penitente"], 30)  # espinhos
        g.j.recalcular()
        cb.atacar(e, g.j, 1.0)  # o golpe dela volta nos espinhos
        cb.atacar(cb.invocar_aliado("Morel", 80, 200, tipo="comitiva"), e, 5.0)
        self.assertEqual(e.hp, e.piso)
        g.combate_ativo = None

    def test_desistir_devolve_o_dano_e_rito_encerra_em_paz(self):
        for resposta, desfecho in (("Desistir do rito", "lutar"), ("Dizer o nome dela", "rito")):
            g, cb, e, _ = self.luta()
            g.ui.respostas = [resposta]
            afogado = g.inimigo("afogado")
            cb.inimigos.append(afogado)
            cb.atacar(g.j, e, 50.0)
            retido = e.retido
            missoes._momento_do_rito(g, cb, e)
            self.assertIsNone(e.piso)
            if desfecho == "lutar":
                self.assertEqual(e.retido, 0)
                self.assertFalse(e.vivo if retido >= e.max_hp else False)  # o golpe guardado cai inteiro
                self.assertFalse(getattr(e, "descansou", False))
                self.assertTrue(afogado.vivo)
            else:
                self.assertTrue(e.descansou)
                self.assertFalse(e.vivo or afogado.vivo)  # ela e o que ela chamou afundam
                self.assertEqual(cb._checar_fim(), "vitoria")
            g.combate_ativo = None


class TestConfronto(unittest.TestCase):
    def test_tres_classes_dao_descanso(self):
        for classe in CLASSES:
            g = no_fundo(classe, DESCANSO, **PRONTO)
            sigilos, pontos = len(g.j.sigilos), g.j.pontos_talento
            self.assertTrue(missoes.executar(g, MID, "fundo"))
            m = missoes.registro(g, MID)
            self.assertEqual((m["desfecho"], m["etapa"]), ("descansada", "retorno"), classe)
            self.assertIn("relato_de_ilse", m["pistas"])
            self.assertEqual((g.j.sigilos[sigilos:], g.j.pontos_talento), (["turvo"], pontos + 1))
            todos = [it for it in g.j.mochila + list(g.j.equip.values()) if it]
            self.assertFalse(any(it.get("unico") == "pele_do_penitente" for it in todos))
            pergunta = next(p for p in g.ui.perguntas if p[0] == "Este é o momento do rito.")
            self.assertEqual(len(pergunta[1]), 2)
            self.assertFalse(opcoes_febre(g))  # no fundo, nada mais da febre (o lodo, prova para Caspar, continua)
            self.assertFalse(missoes.executar(g, MID, "fundo"))
            self.assertEqual(len(g.j.sigilos), sigilos + 1)

    def test_tres_classes_destroem_sem_preparo(self):
        for classe in CLASSES:
            g = no_fundo(classe, DESTRUIR, preparos=())
            self.assertTrue(missoes.executar(g, MID, "fundo"))
            m = missoes.registro(g, MID)
            self.assertEqual((m["desfecho"], m["etapa"]), ("destruida", "retorno"), classe)
            descida = next(p for p in g.ui.perguntas if p[0].startswith("Ela ainda não se levantou"))
            self.assertEqual(descida[1], ["Lutar para destruí-la", "Voltar por enquanto"])  # sem um rito fadado a falhar
            self.assertFalse(any("ainda falta" in d for d in g.ui.ditos))  # sem Berta, ninguém falou do rito
            self.assertFalse(any(p[0] == "Este é o momento do rito." for p in g.ui.perguntas))
            todos = [it for it in g.j.mochila + list(g.j.equip.values()) if it]
            self.assertEqual(sum(it.get("unico") == "pele_do_penitente" for it in todos), 1)
            self.assertEqual(g.j.sigilos, ["turvo"])

    def test_com_berta_e_sem_as_correntes_diz_o_que_falta(self):
        g = no_fundo("mago", ["Voltar por enquanto"], preparos=("fita",), berta=True)
        missoes.executar(g, MID, "fundo")
        dito = next(d for d in g.ui.ditos if "ainda falta" in d)
        self.assertIn("Vó Berta", dito)
        self.assertIn("soltá-la das pedras de moinho", dito)
        descida = next(p for p in g.ui.perguntas if p[0].startswith("Ela ainda não se levantou"))
        self.assertEqual(descida[1], ["Lutar para destruí-la", "Voltar por enquanto"])

    def test_preparado_e_mesmo_assim_destroi(self):
        g = no_fundo("arqueiro", DESTRUIR, **PRONTO)
        missoes.executar(g, MID, "fundo")
        self.assertEqual(missoes.registro(g, MID)["desfecho"], "destruida")
        self.assertFalse(any(p[0] == "Este é o momento do rito." for p in g.ui.perguntas))  # sem piso, sem momento

    def test_desistir_do_rito_no_momento_destroi(self):
        g = no_fundo("mago", ["Chamar Ilse pelo nome", "Desistir do rito", "Guardar"], **PRONTO)
        missoes.executar(g, MID, "fundo")
        self.assertEqual(missoes.registro(g, MID)["desfecho"], "destruida")

    def test_voltar_por_enquanto_nao_resolve(self):
        g = no_fundo(respostas=["Voltar por enquanto"])
        self.assertTrue(missoes.executar(g, MID, "fundo"))
        m = missoes.registro(g, MID)
        self.assertEqual((m["desfecho"], m["etapa"], g.j.sigilos), (None, "fundo", []))

    def test_derrota_nao_resolve_e_a_guardia_volta_inteira(self):
        g = no_fundo(respostas=DESCANSO, **PRONTO)
        vistas = []

        def cai(grupo, **k):
            vistas.append((grupo[0].hp, grupo[0].max_hp))
            grupo[0].hp = 3  # ela também apanhou...
            raise Derrota()
        g.combate = cai
        with self.assertRaises(Derrota):
            missoes.executar(g, MID, "fundo")
        m = missoes.registro(g, MID)
        self.assertEqual((m["desfecho"], m["etapa"], sorted(m["preparos"])), (None, "fundo", ["corpo_solto", "fita"]))
        g.resgate()
        ir(g, "capela_afogada")
        with self.assertRaises(Derrota):
            missoes.executar(g, MID, "fundo")
        self.assertEqual(vistas[1][0], vistas[1][1])  # ...mas a nova tentativa começa com ela inteira

    def test_save_depois_do_desfecho_nao_repete_nada(self):
        pasta = tempfile.mkdtemp()
        g = no_fundo("guerreiro", DESCANSO, pasta=pasta, **PRONTO)
        missoes.executar(g, MID, "fundo")
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(["Guardar"]), g.caminho_save(), pasta)
        m = missoes.registro(h, MID)
        self.assertEqual((m["desfecho"], m["etapa"], h.j.sigilos), ("descansada", "retorno", ["turvo"]))
        self.assertFalse(opcoes_febre(h))
        self.assertFalse(missoes.executar(h, MID, "fundo"))
        # A herança: na taverna, para quem deu descanso, uma vez.
        ir(h, "vau_do_turvo")
        opcao = next(o for o in missoes.opcoes(h) if o[1][2] == "heranca")
        self.assertEqual(opcao[2]["predio"], "taverna")
        antes = len(h.j.mochila)
        self.assertTrue(missoes.executar(h, MID, "heranca"))
        self.assertEqual(len(h.j.mochila), antes + 1)
        self.assertEqual(h.j.mochila[-1]["raridade"], "raro")
        self.assertFalse(missoes.executar(h, MID, "heranca"))
        h.salvar(silencioso=True)
        k = Jogo.carregar(Roteiro(), h.caminho_save(), pasta)
        ir(k, "vau_do_turvo")
        self.assertFalse([o for o in missoes.opcoes(k) if o[1][2] == "heranca"])
        self.assertEqual(missoes.cartoes(k)[0]["objetivo"], missoes.MISSOES[MID]["etapas"]["retorno"]["objetivo"])

    def test_destruir_nao_tem_heranca(self):
        g = no_fundo("mago", DESTRUIR)
        missoes.executar(g, MID, "fundo")
        ir(g, "vau_do_turvo")
        self.assertFalse(missoes.opcoes(g))

    def test_save_de_antes_do_desfecho_mantem_as_correntes(self):
        """Um save da 1.52 (sem `desfecho`) carrega com as correntes soltas e a guardiã por resolver."""
        pasta = tempfile.mkdtemp()
        g = na_capela(pasta=pasta, etapa="fundo")
        lutas(g, "vitoria")
        fazer(g, "correntes")
        del g.mundo["missoes"][MID]["desfecho"]
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        m = missoes.registro(h, MID)
        self.assertEqual((m["preparos"], m["desfecho"], m["etapa"]), (["corpo_solto"], None, "fundo"))
        self.assertIn("fundo", [o[1][2] for o in missoes.opcoes(h)])


if __name__ == "__main__":
    unittest.main()
