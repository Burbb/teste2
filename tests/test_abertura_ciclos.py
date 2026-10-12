"""Os ciclos básicos da abertura guiada (roadmapIDEIAS/18, seção 17): o primeiro atendimento grátis do templo, um
contrato do mural ao pagamento (K1–K4), o primeiro baú (B1), os selos da luta (SF, S-, S+) e adiantar a apresentação
(A1). As orientações seguem o estado real, uma por vez, e o que se cumpre não depende da caixa."""

import tempfile
import unittest

from rpg import abertura as ab
from rpg.jogo import Jogo
from rpg.combate import Combate
from tests.test_abertura import Jogador
from tests.test_abertura_parte2 import depois_da_despensa, oid
from tests.test_missoes import ir


def contrato(g, chave="bosque_do_moinho", familia="lobo", feito=0, total=3):
    lid = next(l["id"] for l in g.mundo["locais"] if l["chave"] == chave)
    c = {"id": g.novo_id(), "tipo": "caca", "local": lid, "familia": familia, "total": total, "feito": feito,
         "ouro": 15, "xp": 10, "desc": f"Eliminar {total} lobos.", **({"concluido": True} if feito >= total else {})}
    g.contratos.append(c)
    return c


class TestTemplo(unittest.TestCase):
    def herói(self, g):
        return next(o for o in g.opcoes_templo() if o[1][1] is None)

    def test_primeiro_atendimento_gratis_uma_vez_so_na_cura(self):
        g = depois_da_despensa()
        g.j.hp = 10
        o = self.herói(g)
        self.assertEqual((o[0], o[1][2], o[2]["curto"]), ("Templo: cuidar da vida (primeiro atendimento — grátis)", 0,
                                                          "Primeiro atendimento — grátis"))
        self.herói(g)  # ver o serviço (entrar no templo, ler a orientação) não gasta
        self.assertTrue(g.templo_gratis())
        ouro = g.j.ouro
        g.templo(*o[1][1:])
        self.assertEqual((g.j.hp, g.j.ouro, g.templo_gratis()), (g.j.max_hp, ouro, False))
        g.j.hp = 10
        o = self.herói(g)
        self.assertEqual(o[1][2], g.preco(max(1, (g.j.max_hp - 10) // 2)))  # depois, o preço de sempre

    def test_so_o_heroi_e_nao_renova_ao_carregar_nem_ao_religar(self):
        pasta = tempfile.mkdtemp()
        g = depois_da_despensa(pasta=pasta)
        from rpg import comitiva as cm
        cm.recrutar(g, "morel")
        cm.membro(g, "morel")["hp"] = 5
        precos = {o[2].get("alvo"): o[1][2] for o in g.opcoes_templo()}
        self.assertGreater(precos["morel"], 0)  # a comitiva paga
        g.j.hp = 10
        g.templo(*self.herói(g)[1][1:])
        g.salvar(silencioso=True)
        h = Jogo.carregar(Jogador(), g.caminho_save(), pasta)
        ab.ligar(h, False)
        ab.ligar(h, True)
        self.assertFalse(h.templo_gratis())

    def test_igual_com_e_sem_tutorial_e_so_na_campanha(self):
        self.assertTrue(depois_da_despensa(tutorial=False).templo_gratis())
        g = Jogo(Jogador(), seed=3, pasta_saves=tempfile.mkdtemp(), hardcore=False)
        g.iniciar("Teste", "mago")  # o mundo gerado: preços de sempre
        self.assertFalse(g.templo_gratis())


class TestContrato(unittest.TestCase):
    def test_no_mural_um_contrato_de_caca_adequado(self):
        g = depois_da_despensa()
        perto = contrato(g, "charco_dos_juncos")  # nível 1
        longe = contrato(g, "bosque_do_moinho")  # nível 2: acima do herói de nível 1
        alvo = dict(perto, id=g.novo_id(), tipo="alvo")
        g.contratos = []
        ab.contexto(g, "mural", {"lista": [longe, alvo, perto]})
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("K1", f"aceitar:{perto['id']}"))  # nem o elite nem o difícil
        self.assertEqual(o["texto"], "Aceite este contrato para começar.")  # o cartão já diz alvo e recompensa
        ab.contexto(g, "mural", {"lista": [longe, alvo]})
        self.assertIsNone(ab.atual(g))  # sem nada adequado, nada se força (e a oferta não muda)

    def test_aceito_o_contrato_o_k2_vem_antes_das_outras(self):
        # O fluxo de Jean: o Texto (A1) e a vida baixa (V2) ainda pendentes; aceito o contrato, a volta à vila mostra o
        # contrato, sem esperar outra resposta ao menu.
        g = depois_da_despensa()
        g.mundo["abertura"]["vistas"].remove("A1")
        g.j.hp = int(g.j.max_hp * 0.4)
        c = contrato(g, "charco_dos_juncos")
        g.contratos = []
        g.aceitar_contrato(c, {"lista": [c]})
        self.assertEqual(oid(g), "K2")
        ab.depois_do_menu(g, ab.proxima(g), "passear")  # respondido o menu, a fila segue
        self.assertEqual(oid(g), "V2")

    def test_aceitar_qualquer_um_cumpre_k1(self):
        g = depois_da_despensa()
        c = contrato(g)
        g.contratos = []
        g.aceitar_contrato(c, {"lista": [c]})
        self.assertIn("K1", g.mundo["abertura"]["vistas"])

    def test_onde_fica_cacar_e_cumprido_seguem_o_estado_real(self):
        g = depois_da_despensa()
        c = contrato(g, "charco_dos_juncos")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("K2", f"contrato:{c['id']}"))
        self.assertEqual(o["texto"], "Clique neste contrato para viajar até **Charco dos Juncos**.")
        ir(g, "charco_dos_juncos")
        self.assertEqual(oid(g), "K3")
        self.assertIn("**Caçar**", ab.atual(g)["texto"])
        c["feito"], c["concluido"] = 3, True
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("K4", f"contrato:{c['id']}"))
        self.assertIn("15 de ouro e 10 XP", o["texto"])
        ir(g, "vau_do_turvo")
        g.receber_contratos()  # o pagamento fecha o ciclo
        self.assertIn("K4", g.mundo["abertura"]["vistas"])
        contrato(g)
        self.assertNotIn(oid(g), ("K2", "K3", "K4"))  # o próximo contrato não refaz o ciclo

    def test_abandonar_segue_o_proximo_e_nao_trava(self):
        g = depois_da_despensa()
        a = contrato(g, "charco_dos_juncos")
        b = contrato(g, "bosque_do_moinho")
        g.contratos.remove(a)  # abandonado
        self.assertEqual(ab.atual(g)["ancora"], f"contrato:{b['id']}")
        g.contratos = []
        self.assertIsNone(ab.atual(g))  # sem contrato, nada: a história segue

    def test_chegar_ao_lugar_cumpre_k2_e_o_menu_passa_k3(self):
        g = depois_da_despensa()
        contrato(g, "charco_dos_juncos")
        ir(g, "charco_dos_juncos")
        g.ui.roteiro = ["Mapa"]  # uma resposta qualquer (o mapa, e de volta)
        g.menu_selvagem()
        self.assertIn("K2", g.mundo["abertura"]["vistas"])
        self.assertIn("K3", g.mundo["abertura"]["vistas"])  # a resposta ao menu (qualquer) passou a ocasião


class TestBauSelosAdiantar(unittest.TestCase):
    def test_primeiro_bau_real_e_abrir_cumpre(self):
        g = depois_da_despensa()
        self.assertNotEqual(oid(g), "B1")
        g.j.consumiveis["bau"] = 1
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"], o["texto"]), ("B1", "bolsa:bau", "Clique no baú para abrir."))
        g.j.consumiveis["bau"] = 3
        self.assertEqual(ab.atual(g)["texto"], "Clique no baú para abrir os 3.")
        g.j.consumiveis["bau"] = 1
        g.executar_comum(("usar", "bau"))
        self.assertIn("B1", g.mundo["abertura"]["vistas"])

    def luta(self, g):
        cb = Combate(g, [g.inimigo("lobo", nivel=1)], None, titulo="Teste")
        g.combate_ativo = cb
        return cb

    def test_selos_firme_antes_do_mal_antes_do_bem_com_o_efeito_real(self):
        g = depois_da_despensa()
        cb = self.luta(g)
        self.assertIsNone(ab.atual(g))  # nada aconteceu: nada a mostrar
        lobo = cb.inimigos[0]
        g.j.efeitos["esquiva"] = {"t": 2, "v": 0.2}
        lobo.efeitos["veneno"] = {"t": 3, "v": 4}
        lobo.efeitos["firme"] = {"t": 1}
        o = ab.atual(g)
        self.assertEqual(o["id"], "SF")
        # O nome, o efeito de agora e, só no primeiro, a duração (o número do ícone).
        self.assertEqual(o["texto"], "**Firme**\nAcabou de se soltar: não pode ser atordoado nem congelado agora.\n"
                                     "O número no ícone indica quantos turnos o efeito ainda dura.")
        ab.visto(g, "SF")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("S-", f"selo:{cb.uid(lobo)}:veneno"))
        self.assertEqual(o["texto"], "**Veneno**\n4 de dano por turno · 3 turnos restantes.")
        ab.visto(g, "S-")
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("S+", "selo:j:esquiva"))
        self.assertEqual(o["texto"], "**Esquiva**\n+20% de chance de esquiva · 2 turnos restantes.")

    def test_iniciativa_diz_de_que_e_do_primeiro_golpe(self):
        g = depois_da_despensa()
        self.luta(g)
        g.j.efeitos["iniciativa"] = {"t": 1, "v": 0.25}
        self.assertEqual(ab.atual(g)["texto"], "**Iniciativa**\n+25% de dano no primeiro golpe deste turno.\n"
                                               "O número no ícone indica quantos turnos o efeito ainda dura.")

    def test_adiantar_depois_da_primeira_luta_e_sem_prometer_pular(self):
        g = nova_sem_a1()
        o = ab.atual(g)
        self.assertEqual((o["id"], o["ancora"]), ("A1", "topo:velocidade"))
        self.assertEqual(o["texto"], "Ajuste a velocidade do texto aqui. Atalho: **V**.")
        # Revelar o texto e acelerar a animação: à parte (a ocasião é da tela), sem segurar a fila das outras.
        self.assertEqual(set(ab.para_tela(g)["apresentacao"]), {"A0", "AL"})
        ab.entendi(g, "A0")
        self.assertEqual(set(ab.para_tela(g)["apresentacao"]), {"AL"})
        g.mundo["abertura"]["vistas"].remove("combate")
        self.assertNotEqual(oid(g), "A1")  # antes de qualquer luta, não
        self.assertEqual(ab.para_tela(g)["apresentacao"], {})


def nova_sem_a1():
    g = depois_da_despensa()
    g.mundo["abertura"]["vistas"].remove("A1")
    return g


if __name__ == "__main__":
    unittest.main()
