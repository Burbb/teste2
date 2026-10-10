"""A escolha de especialização explicada (E5, P3): a prévia dos dois caminhos é a conta de verdade, feita numa cópia;
olhar e voltar não mexem em nada; confirmar aplica uma vez; o modo texto mostra o mesmo; o Grimório diz o que a
execução faz (imunidades, "se acertar", a Marca, a Combustão, o caminho)."""

import copy
import json
import os
import random
import tempfile
import unittest

from rpg import comitiva as cm
from rpg import dev, especializacao, grimorio
from rpg.classes import CLASSES, SPECS
from rpg.combate import Combate
from rpg.entidades import Inimigo
from rpg.eventos import classe as eventos_classe
from rpg.habilidades import HABILIDADES
from rpg.jogo import Jogo
from rpg.talentos import custo_habilidade
from tests.test_missoes import Roteiro

STATS = ("max_hp", "max_rec", "atk", "defesa", "agi", "poder")
ANIMAL = {"patrulheiro": "Lobo"}


def heroi(classe, nivel=4, ui=None, pasta=None):
    g = Jogo(ui or Roteiro(), seed=5, pasta_saves=pasta or tempfile.mkdtemp())
    g.iniciar("Teste", classe, "turvo")
    dev.subir_ate(g, nivel, spec=False)
    return g


def retrato(g):
    """Tudo o que consultar não pode mudar: o herói, o sorteio, a comitiva e os saves."""
    return (json.dumps(g.j.para_dict(), sort_keys=True, default=str), g.rng.getstate(),
            json.dumps(g.comitiva, sort_keys=True), sorted(os.listdir(g.pasta_saves)))


class TestPrevia(unittest.TestCase):
    def test_seis_caminhos_comparaveis(self):
        for classe in CLASSES:
            g = heroi(classe)
            for spec in CLASSES[classe]["specs"]:
                p = especializacao.previa(g.j, spec)
                self.assertEqual([x["agora"] for x in p["habilidades"]], [True, True, False], spec)
                self.assertEqual(p["habilidades"][2]["nivel"], 7)
                self.assertIn("nível de agora (4)", p["referencia"])
                self.assertTrue(p["beneficios"], spec)  # todo caminho diz o que dá, não só o que não tem
                self.assertTrue(p["limites"], spec)
                self.assertTrue(p["talentos"], spec)
                self.assertFalse([b for b in p["beneficios"] + p["limites"] if "sem passiva" in b.lower()])
                json.dumps(p)  # vai para a tela como está

    def test_exemplos_pedidos(self):
        g = heroi("guerreiro")
        b = especializacao.previa(g.j, "berserker")
        defesa = next(a for a in b["atributos"] if a["stat"] == "Defesa")
        self.assertEqual((defesa["delta"], defesa["depois"]), (-2, g.j.defesa - 2))
        p = especializacao.previa(g.j, "paladino")
        self.assertTrue(any("grito de terror" in x for x in p["beneficios"]))
        self.assertTrue(any("Vontade +3" in x and "Carisma +2" in x for x in p["beneficios"]))
        g = heroi("arqueiro")
        pat = especializacao.previa(g.j, "patrulheiro")
        self.assertEqual(len(pat["animais"]), 3)
        self.assertTrue(any("animal luta ao seu lado" in x for x in pat["beneficios"]))
        sombra = especializacao.previa(g.j, "sombra")
        self.assertTrue(any("Veneno" in x and "mortos-vivos nem construtos" in x for x in sombra["limites"]))
        self.assertTrue(any("Agilidade +5" in x and "crítico" in x for x in sombra["beneficios"]))

    def test_previa_e_o_heroi_especializado(self):
        """Os números da prévia são os do herói depois de escolher (mesmo nível, talentos e equipamento)."""
        for classe in CLASSES:
            for spec in CLASSES[classe]["specs"]:
                ui = Roteiro([ANIMAL.get(spec, "")] if spec in ANIMAL else [])
                g = heroi(classe, ui=ui)
                dev.gastar_talentos(g, random.Random(2))
                dev.vestir(g, random.Random(2), 4)
                p = especializacao.previa(g.j, spec)
                g.especializar(spec)
                for a in p["atributos"]:
                    k = next(k for k in STATS if especializacao.nome_stat(k, g.j.nome_recurso) == a["stat"])
                    self.assertEqual(getattr(g.j, k), a["depois"], (spec, k))
                for x in p["habilidades"]:
                    self.assertEqual(x["custo"], custo_habilidade(g.j, x["id"]))
                    if x["id"] != "comando_fera":  # a Ordem muda com o animal, escolhido só ao confirmar
                        self.assertEqual(x["linhas"], HABILIDADES[x["id"]]["linhas"](g.j), (spec, x["id"]))
                if spec == "patrulheiro":
                    a = next(a for a in p["animais"] if a["tipo"] == "lobo")
                    self.assertEqual((g.j.companheiro["max_hp"], g.j.companheiro["atk"]), (a["max_hp"], a["atk"]))

    def test_previa_nao_mexe_no_heroi(self):
        g = heroi("mago")
        antes = retrato(g)
        for spec in ("piromante", "necromante"):
            especializacao.previa(g.j, spec)
        self.assertEqual(retrato(g), antes)
        self.assertIsNone(g.j.spec)


class Espiao(Roteiro):
    """Anota, a cada escolha, o retrato do jogo (para ver que olhar e voltar não mudam nada)."""

    def __init__(self, roteiro, g_ref):
        super().__init__(roteiro)
        self.g_ref, self.retratos, self.perguntas = g_ref, [], []

    def escolher(self, pergunta, opcoes):
        self.perguntas.append((pergunta, list(opcoes), self.meta_opcoes))
        if self.g_ref:
            self.retratos.append(retrato(self.g_ref[0]))
        return super().escolher(pergunta, opcoes)


class TestEscolha(unittest.TestCase):
    def test_olhar_voltar_e_confirmar_uma_vez(self):
        ref = []
        ui = Espiao(["Olhar de perto: Paladino", "Voltar", "Olhar de perto: Berserker", "Voltar",
                     "Olhar de perto: Paladino", "Confirmar: Paladino"], ref)
        g = heroi("guerreiro", ui=ui)
        ref.append(g)
        cm.recrutar(g, "odete")
        aprov = cm.membro(g, "odete")["aprovacao"]
        vida, poder = g.j.max_hp, g.j.poder
        eventos_classe.encruzilhada_guerreiro(g)
        self.assertEqual(len(set(map(str, ui.retratos))), 1)  # nada mudou entre olhar, voltar e olhar de novo
        self.assertEqual(g.j.spec, "paladino")
        self.assertEqual((g.j.max_hp, g.j.poder), (vida + SPECS["paladino"]["bonus"]["max_hp"],
                                                   poder + SPECS["paladino"]["bonus"]["poder"]))  # uma vez só
        self.assertNotEqual(cm.membro(g, "odete")["aprovacao"], aprov)  # a comitiva reage à escolha, não ao olhar
        texto = " ".join(ui.ditos)
        self.assertIn("PALADINO —", texto)
        self.assertIn("BERSERKER —", texto)
        self.assertIn(eventos_classe.DEFINITIVA, texto)
        self.assertIn("Talentos do caminho:", texto)  # o detalhe, ao olhar de perto
        self.assertIn("Você se ajoelha ao lado do cavaleiro", texto)  # a narração de sempre
        perguntas = [p for p, _, _ in ui.perguntas]
        self.assertTrue(all(p for p in perguntas))  # no texto, cada escolha diz o que se escolhe

    def test_tela_grafica_recebe_o_painel(self):
        ref = []
        ui = Espiao(["Olhar de perto: Piromante", "Confirmar: Piromante"], ref)
        paineis = []
        ui.painel = lambda tipo, dados: paineis.append((tipo, copy.deepcopy(dados))) or True
        g = heroi("mago", ui=ui)
        eventos_classe.encruzilhada_mago(g)
        self.assertEqual([t for t, _ in paineis], ["especializacao", "especializacao"])
        self.assertEqual([d["foco"] for _, d in paineis], [None, "piromante"])
        self.assertEqual([c["id"] for c in paineis[0][1]["caminhos"]], ["piromante", "necromante"])
        self.assertEqual([p for p, _, _ in ui.perguntas], ["", ""])  # o painel diz o que fazer
        metas = ui.perguntas[1][2]
        self.assertEqual(metas, [{"confirmar": "piromante"}, {"voltar": True}])
        self.assertEqual(g.j.spec, "piromante")


class TestGrimorio(unittest.TestCase):
    def linhas(self, classe, spec, h, nivel=5):
        ui = Roteiro([ANIMAL[spec]] if spec in ANIMAL else [])
        g = heroi(classe, nivel=1, ui=ui)
        dev.subir_ate(g, nivel, spec=spec)
        return g, [l.get("texto", "") for l in HABILIDADES[h]["linhas"](g.j)]

    def test_textos(self):
        _, ls = self.linhas("arqueiro", "sombra", "flecha_envenenada")
        self.assertIn("Se acertar, veneno", ls[1])
        self.assertIn("não afeta mortos-vivos nem construtos", ls[1])
        _, ls = self.linhas("arqueiro", "sombra", "marcar_presa")
        self.assertIn("os da comitiva e os do animal", ls[0])
        _, ls = self.linhas("arqueiro", "sombra", "desaparecer")
        self.assertIn("continuam mirando você", ls[0])
        _, ls = self.linhas("guerreiro", "berserker", "investida")
        self.assertTrue(ls[1].startswith("Se acertar, 45% de chance de atordoar"))
        _, ls = self.linhas("guerreiro", "berserker", "erguer_escudo")
        self.assertIn("golpe preparado", ls[0])
        g, _ = self.linhas("guerreiro", "paladino", "golpe_sagrado")
        pagina = next(p for p in grimorio.dados(g.j)["passivas"] if p["id"] == "caminho")
        self.assertTrue(any("grito de terror" in l["texto"] for l in pagina["linhas"]))
        self.assertTrue(any(r.startswith("Atordoar ou congelar") for r in grimorio.dados(g.j)["gerais"]))
        texto = "\n".join(grimorio.texto(g.j))
        self.assertIn("Paladino (Caminho)", texto)  # o modo texto mostra o mesmo

    def test_combustao_como_a_execucao(self):
        """As duas linhas de exemplo da Combustão batem com o golpe de verdade nas condições que elas dizem."""
        g, _ = self.linhas("mago", "piromante", "combustao")
        j = g.j
        exemplos = {l["rotulo"]: l for l in HABILIDADES["combustao"]["linhas"](j) if l["tipo"] == "dano"}
        for camadas, rotulo in ((1, "1 camada, acesa no turno anterior"),
                                (3, "3 camadas: três Bolas de Fogo seguidas que acenderam, detonadas logo depois")):
            linha = exemplos[rotulo]
            p = linha["chance_critico"] / 100
            esperado = linha["medio"] * (1 - p) + linha["critico"] * p
            total, n = 0, 3000
            for s in range(n):
                alvo = Inimigo("Boneco", 10 ** 6, 1, 0, 0, 0)
                cb = Combate(g, [alvo], pode_fugir=False)
                for _ in range(camadas):  # cada Bola de Fogo que acendeu (o turno do alvo vem depois da última)
                    cb.aplicar(alvo, "queimadura", cb.duracao_queimadura(j), valor=cb.valor_queimadura(j), acumula=True)
                cb.processar_efeitos(alvo)
                antes = alvo.hp
                g.rng.seed(s)
                HABILIDADES["combustao"]["fn"](cb, j, alvo)
                total += antes - alvo.hp
                g.combate_ativo = None
            self.assertAlmostEqual(total / n, esperado, delta=esperado * 0.03, msg=rotulo)


if __name__ == "__main__":
    unittest.main()
