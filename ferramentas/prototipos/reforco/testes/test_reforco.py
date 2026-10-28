"""O protótipo do reforço: as regras, as ações conferidas e os ciclos de recursos.

    python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
"""

import os
import random
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = os.path.dirname(AQUI)
RAIZ = os.path.normpath(os.path.join(PASTA, "..", "..", ".."))
for p in (RAIZ, PASTA):
    if p not in sys.path:
        sys.path.insert(0, p)

import demo as D  # noqa: E402
import regras as R  # noqa: E402
from rpg import itens  # noqa: E402
from rpg.jogo import Jogo  # noqa: E402
from rpg.regras import LIMITE_MOCHILA  # noqa: E402
from rpg.ui import BotUI  # noqa: E402

D.ativar()


def jogo():
    g = Jogo(BotUI(random.Random(1), max_decisoes=10 ** 6), seed=11, pasta_saves=tempfile.mkdtemp(), hardcore=False)
    g.iniciar("Jean", "guerreiro", "turvo")
    D.preparar(g)
    D.materiais(g)["fragmento"] = 8
    D.dar_uid(g)
    return g


def peca(classe, slot, nivel, material=None, raridade="comum"):
    rng = random.Random(5)
    while True:
        it = itens.gerar_equip(rng, classe, nivel, slot=slot, raridade=raridade)
        if not material or material in (it.get("base") or ""):
            return it


class TestFormula(unittest.TestCase):
    def test_todo_espaco_cresce_sem_cair_e_a_arma_sente_cada_passo_ate_o_4(self):
        espacos = [(c, s) for c in ("guerreiro", "arqueiro", "mago")
                   for s in ("arma", "armadura", "secundaria", "cabeca", "maos", "pernas", "pes", "anel", "amuleto")]
        for classe, slot in espacos:
            for nivel in (1, 3, 6, 9, 12):
                for rar in ("comum", "magico", "raro"):
                    it = peca(classe, slot, nivel, raridade=rar)
                    self.assertTrue(R.tipo(it), it["nome"])
                    anterior = {}
                    for n in range(1, R.LIMITE + 1):
                        g = R.ganho_total(it, n)
                        self.assertTrue(all(g[st] >= anterior.get(st, 0) for st in g), (it["nome"], n, g))
                        if slot == "arma" and n <= 4:  # a principal da arma: +1 por passo na faixa aprovada
                            principal = [st for st, _, piso in R.linhas(it) if piso][0]
                            self.assertGreater(g[principal], anterior.get(principal, 0), (it["nome"], n))
                        anterior = g
                    total = R.ganho_total(it, R.LIMITE)  # a % não passa do teto da peça
                    for st, teto in R.TETO_PCT.items():
                        self.assertLessEqual((it.get("bonus_base") or it["bonus"]).get(st, 0) + total.get(st, 0), max(teto, it["bonus"].get(st, 0)))

    def test_forma_fechada_sem_deriva_ao_cair_e_subir(self):
        for classe, slot in (("guerreiro", "secundaria"), ("arqueiro", "secundaria"), ("mago", "secundaria"), ("guerreiro", "anel")):
            it = peca(classe, slot, 5, raridade="raro")
            base = dict(it["bonus"])
            it["bonus_base"] = dict(base)
            vistos = {}
            for n in (3, 7, 6, 5, 6, 7, 12, 11, 0, 7):  # quedas e subidas
                D.aplicar_nivel(it, n)
                vistos.setdefault(n, dict(it["bonus"]))
                self.assertEqual(it["bonus"], vistos[n], (it["nome"], n))
            D.aplicar_nivel(it, 0)
            self.assertEqual(it["bonus"], base)

    def test_arma_inicial_alcanca_uma_base_mais_nova_por_um_tempo(self):
        velha = peca("guerreiro", "arma", 1, "Enferrujad")  # Ataque 2
        self.assertEqual(velha["bonus"]["atk"], 2)
        self.assertEqual(R.ganho_total(velha, 4)["atk"], 4)  # +4: 6, como uma de Aço do nível 6
        nova = peca("guerreiro", "arma", 6, "de Aço")
        self.assertGreater(nova["bonus"]["atk"] + R.ganho_total(nova, R.LIMITE)["atk"], 6 + 3)

    def test_a_peca_inteira_cresce_cada_linha_pela_sua_regra(self):
        it = peca("guerreiro", "armadura", 4)
        it["bonus"].update(poder=3, critico=4)  # os afixos também crescem (12ª versão)
        g12 = R.ganho_total(it, R.LIMITE)
        self.assertEqual(set(g12), {"defesa", "max_hp", "poder", "critico"})
        self.assertEqual(g12["critico"], 3.2)  # em %: 0,25 ponto por nível de peça (13 no +12: 3,25), em décimos de ponto
        self.assertGreater(g12["max_hp"], g12["defesa"])  # cada linha na proporção do próprio valor

    def test_sem_caminho_na_arma(self):
        it = peca("guerreiro", "arma", 6)
        self.assertEqual([st for st, _, piso in R.linhas(it) if piso], ["atk"])  # a principal tem o piso de +1

    def test_todo_espaco_recebe_reforco(self):
        for slot, classe, t in (("cabeca", "guerreiro", "cabeca"), ("anel", None, "anel"), ("amuleto", None, "amuleto"),
                                ("secundaria", "arqueiro", "aljava"), ("secundaria", "guerreiro", "escudo")):
            it = {"slot": slot, "classe": classe, "bonus": {"defesa": 1}, "nome": "x"}
            self.assertEqual(R.tipo(it), t)
            self.assertIsNone(R.motivo_sem_reforco(it))

    def test_transferencia(self):
        g = jogo()
        g.ui.efeito = lambda *a, **k: None
        D.transferencia_de_teste(g)
        o, dd, p6, p0 = g.j.mochila[:4]
        base_o, sulcos_o, grav_d = dict(o["bonus_base"]), list(o["encantos"]), list(dd["encantos"])
        venda_antes = o["preco"] // 2 + dd["preco"] // 2
        rende_antes = sum(sum(R.desmontar_rende(x)) for x in (o, dd))
        ouro = g.j.ouro
        custo = g.preco(R.custo_transferencia(8))
        ok, txt = D.transferir(g, o["uid"], dd["uid"], pedido="t1")
        self.assertTrue(ok, txt)
        self.assertEqual((o["reforco"], dd["reforco"], g.j.ouro), (0, 8, ouro - custo))
        self.assertEqual((o["bonus"], o["encantos"], dd["encantos"]), (base_o, sulcos_o, grav_d))  # nada mais se move
        self.assertFalse(D.transferir(g, o["uid"], dd["uid"], pedido="t1")[0])  # o mesmo pedido: nada
        self.assertEqual(g.j.ouro, ouro - custo)
        # nada se cria: a venda e a desmontagem das duas valem menos que antes
        self.assertLess(o["preco"] // 2 + dd["preco"] // 2, venda_antes)
        self.assertLessEqual(sum(sum(R.desmontar_rende(x)) for x in (o, dd)), rende_antes)
        # recusas: sem subir, outra raridade, outro espaço, a origem +0
        self.assertEqual(R.transferencia(p6, dd)[1], "Só entre peças do mesmo espaço.")
        self.assertIsNotNone(R.transferencia(o, dd)[1])  # a origem +0 não dá nada
        # em cadeia: +8 → (destino +6), e o destino de antes fica +0
        self.assertTrue(D.transferir(g, dd["uid"], o["uid"], pedido="t3")[0])
        self.assertEqual((dd["reforco"], o["reforco"]), (0, 6))
        self.assertEqual(R.transferencia(p6, p0), (4, None))


class TestReforcar(unittest.TestCase):
    def test_primeiro_garantido_paga_e_aplica(self):
        g = jogo()
        arma = g.j.equip["arma"]
        ouro, atk = g.j.ouro, arma["bonus"]["atk"]
        ok, texto = D.reforcar(g, arma["uid"], teste="falha")  # o +1 é garantido, até forçando a falha
        self.assertTrue(ok, texto)
        self.assertEqual(g.j.ouro, ouro - g.preco(R.OURO[0]))
        self.assertEqual(D.materiais(g)["fragmento"], 8 - R.FRAGMENTOS[0])
        self.assertEqual(arma["reforco"], 1)
        self.assertGreaterEqual(arma["bonus"]["atk"] - atk, 1)  # a principal da arma: ao menos 1 por passo até o +4
        self.assertTrue(g.forja_ultimo["sucesso"])

    def test_oferta_e_resultado_com_os_mesmos_nomes(self):
        # o recurso pelo nome de quem leva a peça: o tomo na bolsa do Guerreiro oferece e entrega "Vigor" (não "Mana")
        g = jogo()
        D.materiais(g)["fragmento"], g.j.ouro = 99, 9999
        vistos = 0
        for p in D.painel(g)["pecas"]:
            passos = p.get("passos") or []
            if not passos:
                continue
            x = passos[0]
            ok, texto = D.reforcar(g, p["uid"], x["veio"], teste="sucesso")
            self.assertTrue(ok, texto)
            self.assertEqual([l["nome"] for l in x["linhas"]], [l["nome"] for l in g.forja_ultimo["linhas"]], p["item"]["nome"])
            vistos += any(l["nome"] == g.j.nome_recurso for l in x["linhas"])
        self.assertGreater(vistos, 0)  # alguma peça com o recurso entrou na conferência

    def test_chance_exibida_e_a_calculada(self):
        g = jogo()
        for p in D.painel(g)["pecas"]:
            for x in p.get("passos") or []:
                it = D.achar(g, p["uid"])[0]
                self.assertEqual(x["chance"], R.chance(it, p["reforco"] + 1))
        self.assertEqual([R.chance({"raridade": r}, 4) for r in ("comum", "magico", "raro", "lendario")], [55, 51, 47, 43])
        self.assertEqual(R.chance({"raridade": "lendario"}, 1), 100)
        # a raridade pesa menos que um degrau de nível
        self.assertLess(max(R.PENA_RARIDADE.values()), min(R.CHANCE[k] - R.CHANCE[k + 1] for k in (2, 3)))

    def test_falha_desce_um_cobra_e_preserva(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 50
        it = next(x for x in g.j.mochila if x.get("raridade") == "magico" and R.tipo(x) == "peito")
        base = dict(it["bonus"])
        D.reforcar(g, it["uid"])
        D.reforcar(g, it["uid"], teste="sucesso")
        self.assertEqual(it["reforco"], 2)
        ouro, frag = g.j.ouro, D.materiais(g)["fragmento"]
        ok, texto = D.reforcar(g, it["uid"], teste="falha")
        self.assertTrue(ok)
        self.assertEqual(texto, "Reforço falhou · +2 → +1")
        self.assertEqual(it["reforco"], 1)
        self.assertEqual(g.j.ouro, ouro - g.preco(R.OURO[2]))  # a tentativa custou, mesmo falhando
        self.assertEqual(D.materiais(g)["fragmento"], frag - R.FRAGMENTOS[2])
        D.reforcar(g, it["uid"], teste="falha")
        self.assertEqual(it["reforco"], 0)
        self.assertEqual(it["bonus"], base)  # de volta a +0: a base inteira, afixos e especiais intactos
        self.assertFalse(it["nome"].endswith("+0"))

    def test_falha_volta_e_recupera_os_mesmos_numeros(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 50
        arma = g.j.equip["arma"]
        base = dict(arma["bonus"])
        D.reforcar(g, arma["uid"])
        D.reforcar(g, arma["uid"], teste="sucesso")
        dois = dict(arma["bonus"])
        D.reforcar(g, arma["uid"], teste="falha")
        D.reforcar(g, arma["uid"], teste="falha")
        self.assertEqual((arma["reforco"], arma["bonus"]), (0, base))  # no +0, a peça original (nada some, nada sobra)
        D.reforcar(g, arma["uid"])
        D.reforcar(g, arma["uid"], teste="sucesso")
        self.assertEqual(arma["bonus"], dois)

    def test_mesmo_pedido_nao_tenta_de_novo(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 50
        arma = g.j.equip["arma"]
        self.assertTrue(D.reforcar(g, arma["uid"], "fio", pedido="p1")[0])
        ouro = g.j.ouro
        self.assertEqual(D.reforcar(g, arma["uid"], "fio", pedido="p1"), (False, None))
        self.assertEqual((g.j.ouro, arma["reforco"]), (ouro, 1))
        self.assertTrue(D.reforcar(g, arma["uid"], "fio", pedido="p2", teste="sucesso")[0])
        self.assertEqual(arma["reforco"], 2)

    def test_sorteio_normal_segue_a_chance(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 10 ** 6, 99
        it = next(x for x in g.j.mochila if x.get("raridade") == "comum" and R.tipo(x) == "arma")
        D.reforcar(g, it["uid"], "fio")
        acertos = tentativas = 0
        for _ in range(2000):  # sempre tentando o +2 a partir do +1
            if it["reforco"] != 1:
                D.aplicar_nivel(it, 1)
            D.materiais(g)["fragmento"] = 99
            D.reforcar(g, it["uid"])
            tentativas += 1
            acertos += it["reforco"] == 2
        self.assertAlmostEqual(acertos / tentativas, R.chance(it, 2) / 100, delta=0.03)

    def test_falta_recurso_nao_cobra_nada(self):
        g = jogo()
        arma = g.j.equip["arma"]
        D.materiais(g)["fragmento"] = 0
        antes = (g.j.ouro, dict(arma["bonus"]), arma.get("reforco", 0))
        self.assertFalse(D.reforcar(g, arma["uid"], "fio")[0])
        self.assertEqual((g.j.ouro, dict(arma["bonus"]), arma.get("reforco", 0)), antes)

    def test_limite(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 99
        arma = g.j.equip["arma"]
        for _ in range(R.LIMITE):
            self.assertTrue(D.reforcar(g, arma["uid"], "fio", teste="sucesso")[0])
        ok, texto = D.reforcar(g, arma["uid"], "fio")
        self.assertFalse(ok)
        self.assertIn("limite", texto)

    def test_unico_cresce_pela_base_original(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 99
        lam = next(x for x in g.j.mochila if x.get("unico"))
        atk = lam["bonus"]["atk"]
        for _ in range(3):
            D.reforcar(g, lam["uid"], "fio", teste="sucesso")
        self.assertEqual(lam["bonus"]["atk"], atk + R.ganho_total(lam, 3)["atk"])
        for _ in range(2):  # no +3, tentar o +4 e falhar duas vezes: +3 → +2 → +1
            D.reforcar(g, lam["uid"], "fio", teste="falha")
        self.assertEqual(lam["reforco"], 1)
        self.assertEqual(lam["bonus"]["atk"], atk + R.ganho_total(lam, 1)["atk"])

    def test_companheiro_e_peca_que_ninguem_usa(self):
        g = jogo()
        cajado = D.FICHA.corpo(g, "odete")["arma"]
        poder = D.comitiva.atributos(g, D.comitiva.membro(g, "odete"))["poder"]
        self.assertTrue(D.reforcar(g, cajado["uid"])[0])
        self.assertGreater(D.comitiva.atributos(g, D.comitiva.membro(g, "odete"))["poder"], poder)
        # 16ª versão: classe e nível restringem vestir, não o serviço; a prévia vem da peça, sem portador
        arco = next(it for it in g.j.mochila if it.get("classe") == "arqueiro")
        ficha = next(p for p in D.painel(g)["pecas"] if p["uid"] == arco["uid"])
        self.assertNotIn("sem_reforco", ficha)
        self.assertTrue(ficha["passos"][0]["linhas"])
        self.assertTrue(D.reforcar(g, arco["uid"])[0])
        self.assertEqual(arco["reforco"], 1)
        self.assertTrue(D.FICHA.motivo_nao_veste(g, D.HEROI, arco))  # vestir continua recusado


class TestGanhoReal(unittest.TestCase):
    """16ª versão: todo sucesso melhora a peça de verdade (o arredondamento a inteiro escondia o ganho de passos
    inteiros nos acessórios, elmos, luvas e botas)."""

    def test_todo_passo_de_todo_espaco_melhora_alguma_linha(self):
        rng = random.Random(5)
        pecas = [itens.gerar_equip(rng, c, n, slot=s, raridade=r)
                 for c in ("guerreiro", "arqueiro", "mago")
                 for s in ("arma", "armadura", "cabeca", "maos", "pernas", "pes", "secundaria", "anel", "amuleto")
                 for n in (1, 3, 6, 9, 12) for r in ("comum", "magico", "raro")]
        pecas += [itens.fazer_unico(u, 4) for u in itens.UNICOS_POR_ID.values()]
        for it in pecas:
            for n in range(R.LIMITE):
                a, b = R.ganho_total(it, n), R.ganho_total(it, n + 1)
                self.assertTrue(any(b[s] > a[s] for s in b), (it["nome"], it["bonus"], n))
                piso = {s for s, _, p in R.linhas(it) if p}  # a principal da arma: +1 por passo até o +4 (aprovado)
                for s, v in b.items():  # nunca uma casa que o motor não usa; nunca mais de um degrau à frente da conta
                    q = R.PRECISAO.get(s, 1)
                    self.assertAlmostEqual(round(v / q), v / q, places=6)
                    if s not in piso:
                            self.assertLessEqual(v - R.exato(it, n + 1)[s], q + 1e-9, (it["nome"], s, n))

    def test_elmo_pequeno_e_o_cajado_do_10_ao_11(self):
        elmo = {"slot": "cabeca", "classe": "guerreiro", "nivel": 1, "nome": "Barbuta Enferrujada",
                "bonus": {"defesa": 1, "max_hp": 1}}
        self.assertEqual([R.ganho_total(elmo, n)["defesa"] for n in range(5)], [0, 0.5, 1, 1.5, 2])
        cajado = {"slot": "arma", "classe": "mago", "nivel": 2, "nome": "Cajado de Ferro", "bonus": {"poder": 3}}
        self.assertEqual(R.proximo({**cajado, "reforco": 10}), {"poder": 0.6})  # antes: vazio (9 → 9)

    def test_teto_preservado_e_peca_toda_no_teto_nao_cobra(self):
        anel = {"slot": "anel", "nivel": 40, "nome": "Anel da Precisão", "bonus": {"critico": 14.9}}
        self.assertEqual(R.ganho_total(anel, 12)["critico"], 0.1)  # o teto da peça (15%) fica
        g = jogo()
        anel = {"slot": "anel", "nivel": 40, "nome": "Anel da Precisão", "raridade": "comum", "preco": 50,
                "bonus": {"critico": 15}}
        g.j.mochila.append(anel)
        D.dar_uid(g)
        ouro, frag = g.j.ouro, D.materiais(g).get("fragmento", 0)
        ok, texto = D.reforcar(g, anel["uid"])
        self.assertFalse(ok)
        self.assertIn("Sem ganho", texto)
        self.assertEqual((g.j.ouro, D.materiais(g).get("fragmento", 0), anel.get("reforco", 0)), (ouro, frag, 0))
        ficha = next(p for p in D.painel(g)["pecas"] if p["uid"] == anel["uid"])
        self.assertIn("Sem ganho", ficha["sem_reforco"])

    def test_cair_e_subir_volta_ao_mesmo_numero_com_casas(self):
        it = peca("guerreiro", "cabeca", 3)
        it["bonus_base"] = dict(it["bonus"])
        D.aplicar_nivel(it, 7)
        sete = dict(it["bonus"])
        for n in (6, 5, 6, 7):
            D.aplicar_nivel(it, n)
        self.assertEqual(it["bonus"], sete)

    def test_a_fracao_chega_a_ficha_e_a_luta(self):
        g = jogo()
        arma = g.j.equip["arma"]
        arma["bonus"]["atk"] = arma["bonus"]["atk"] + 0.6
        g.j.recalcular()
        self.assertAlmostEqual(g.j.atk % 1, 0.6, places=6)  # o Ataque do herói leva a casa da peça
        from rpg.web import estado
        self.assertIn(",6", estado.heroi(g)["atributos"]["Ataque"])  # na tela, com vírgula
        arma["bonus"]["atk"] = round(arma["bonus"]["atk"] - 0.6)
        g.j.recalcular()
        self.assertIsInstance(g.j.atk, int)  # sem peça fracionária, o número do jogo de sempre

    def test_vida_por_turno_fracionada_acumula(self):
        from rpg.combate import heroi as mh
        u = type("U", (), {})()
        u.equip = {}
        mod_jogo = D.mod_jogo_original
        try:
            D.mod_jogo_original = lambda x, k: 2.6 if k == "regen_vida" else 0
            curas = []
            for _ in range(5):
                u._tique = getattr(u, "_tique", 0) + 1
                mh.mod(u, "regen_vida")  # a pergunta "há?" e o "quanto" no mesmo tique dão o mesmo número
                curas.append(mh.mod(u, "regen_vida"))
            self.assertEqual(sum(curas), 13)  # 2,6 × 5
            self.assertEqual(sorted(set(curas)), [2, 3])
        finally:
            D.mod_jogo_original = mod_jogo


class TestCasosDaDemonstracao(unittest.TestCase):
    def test_depois_dos_casos_de_conferencia_a_tentativa_funciona(self):
        g = jogo()
        g.forja_ultimo = None  # como o CASOS=1 deixa
        g.j.ouro, D.materiais(g)["fragmento"] = 999, 9
        self.assertTrue(D.reforcar(g, g.j.equip["arma"]["uid"], "runas", pedido="x")[0])
        self.assertEqual(g.forja_ultimo["id"], 1)


class TestDesmontar(unittest.TestCase):
    def test_recupera_pelo_nivel_conservado(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 9999, 60
        it = next(x for x in g.j.mochila if x.get("raridade") == "magico" and R.tipo(x) == "peito")
        D.reforcar(g, it["uid"])
        for teste in ("sucesso", "falha", "sucesso", "sucesso"):  # 5 tentativas, termina no +3
            D.reforcar(g, it["uid"], teste=teste)
        self.assertEqual(it["reforco"], 3)
        self.assertEqual(R.desmontar_rende(it), (2, 1))  # metade de 1+1+2, para cima; as falhas não contam
        antes = D.materiais(g)["fragmento"]
        nome = it["nome"]
        ok, texto = D.desmontar(g, it["uid"], nome)
        self.assertTrue(ok, texto)
        self.assertEqual(D.materiais(g)["fragmento"], antes + 3)
        self.assertNotIn(it, g.j.mochila)
        self.assertEqual((g.forja_ultimo["tipo"], g.forja_ultimo["nome"], g.forja_ultimo["total"]), ("desmonte", nome, 3))

    def test_selecao_antiga_ou_peca_vestida_nao_desmonta(self):
        g = jogo()
        alvo = next(x for x in g.j.mochila if x.get("raridade") == "magico")
        self.assertFalse(D.desmontar(g, alvo["uid"], "outro nome")[0])
        self.assertIn(alvo, g.j.mochila)
        self.assertFalse(D.desmontar(g, g.j.equip["arma"]["uid"], g.j.equip["arma"]["nome"])[0])
        n = len(g.j.mochila)
        self.assertTrue(D.desmontar(g, alvo["uid"], alvo["nome"])[0])
        self.assertFalse(D.desmontar(g, alvo["uid"], alvo["nome"])[0])
        self.assertEqual(len(g.j.mochila), n - 1)

    def test_peca_comum_sem_reforco_nao_rende(self):
        g = jogo()
        comum = next(x for x in g.j.mochila if x.get("raridade") == "comum")
        self.assertEqual(D.desmontar(g, comum["uid"], comum["nome"]), (False, "Não rende material."))

    def test_pilha_cheia_e_bolsa_cheia(self):
        g = jogo()
        while len(g.j.mochila) < LIMITE_MOCHILA:
            g.j.mochila.append(peca("guerreiro", "anel", 3))
        self.assertEqual(D.dar_material(g, "fragmento", 5, "teste"), 5)
        self.assertEqual(len(g.j.mochila), LIMITE_MOCHILA)
        D.materiais(g)["fragmento"] = R.PILHA_MAX
        self.assertEqual(D.dar_material(g, "fragmento", 1, "teste"), 0)
        lendaria = next(x for x in g.j.mochila if x.get("raridade") == "lendario")
        self.assertFalse(D.desmontar(g, lendaria["uid"], lendaria["nome"])[0])
        self.assertIn(lendaria, g.j.mochila)


class TestCiclos(unittest.TestCase):
    def test_tentar_cair_desmontar_ou_vender_nunca_rende(self):
        """Qualquer sequência de tentativas (com quedas) e depois desmontar ou vender deixa o grupo com menos ouro e
        com no máximo o material da própria peça a mais."""
        import itertools
        for seq in itertools.product(("sucesso", "falha"), repeat=5):
            for fim in ("desmontar", "vender"):
                g = jogo()
                g.j.ouro, D.materiais(g)["fragmento"] = 5000, 60
                it = next(x for x in g.j.mochila if R.tipo(x) == "peito")
                preco0 = it["preco"]
                ouro0, frag0 = g.j.ouro, D.materiais(g)["fragmento"]
                D.reforcar(g, it["uid"])
                for t in seq:
                    if it["reforco"] < R.LIMITE:
                        D.reforcar(g, it["uid"], teste=t)
                if fim == "desmontar":
                    D.desmontar(g, it["uid"], it["nome"])
                    volta = 0
                else:
                    volta = it["preco"] // 2 - preco0 // 2
                    g.j.mochila.remove(it)
                self.assertLess(g.j.ouro + volta, ouro0, (seq, fim))
                self.assertLessEqual(D.materiais(g)["fragmento"], frag0 + R.DA_PECA[it["raridade"]], (seq, fim))

    def test_preco_acompanha_o_nivel_conservado(self):
        g = jogo()
        g.j.ouro, D.materiais(g)["fragmento"] = 5000, 60
        it = next(x for x in g.j.mochila if R.tipo(x) == "peito")
        p0 = it["preco"]
        D.reforcar(g, it["uid"])
        D.reforcar(g, it["uid"], teste="sucesso")
        self.assertEqual(it["preco"], p0 + int(R.nominal(2)[0] * R.VENDA_DO_OURO * 2))
        D.reforcar(g, it["uid"], teste="falha")
        D.reforcar(g, it["uid"], teste="falha")
        self.assertEqual(it["preco"], p0)


class TestIsolamento(unittest.TestCase):
    def test_o_jogo_nao_carrega_o_prototipo(self):
        codigo = ("import sys, rpg.jogo, rpg.web.servidor, rpg.web.estado; "
                  "print(any('prototipos' in (getattr(m, '__file__', '') or '') for m in list(sys.modules.values())))")
        saida = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        self.assertEqual(saida, "False")


if __name__ == "__main__":
    unittest.main()
