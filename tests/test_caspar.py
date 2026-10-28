"""O segundo eixo do Vale do Turvo (E4): Irmão Caspar e a perseguição à Yara. A acusação na investigação, a praça
depois da guardiã, a prova (geral e forte), as três posturas em combinação com os dois desfechos de Ilse, a situação da
Yara (desconhecida, no grupo, na reserva, morta), a comitiva, os saves e a fogueira do charco. E a coerência do "mesmo
dia" nos textos da volta ao Vau."""

import tempfile
import unittest

from rpg import caspar, comitiva as cm, consequencias, missoes
from rpg.jogo import Jogo
from rpg.web.estado import estado
from tests.test_missoes import MID as FEBRE, Roteiro, campanha, ir

CASPAR = caspar.MID
PISTAS = ["agua_do_leste", "represa", "canal_da_capela", "agua_da_capela", "ilse"]


def investigando(etapa="capela", ui=None, classe="guerreiro"):
    g = campanha(classe, ui)
    missoes.registro(g, FEBRE).update(etapa=etapa, cenas=["abertura"], pistas=list(PISTAS))
    ir(g, "vau_do_turvo")
    return g


def resolvida(desfecho, ui=None, pasta=None, classe="guerreiro", lodo=False, dias=1):
    """A guardiã resolvida e a volta ao Vau já vista (o que acontece em _resolver e na cena de retorno)."""
    g = campanha(classe, ui, pasta)
    g.dia = 10
    f = missoes.registro(g, FEBRE)
    f.update(etapa="retorno", cenas=["abertura", "capela_exterior", "retorno"], pistas=list(PISTAS),
             preparos=["corpo_solto", "fita"], desfecho=desfecho, dia_desfecho=g.dia - dias, concluida=g.dia)
    caspar.sincronizar(g)
    if lodo:
        caspar.registro(g)["preparos"].append("lodo")
    ir(g, "vau_do_turvo")
    return g


def com_yara(g, onde="grupo"):
    if onde in ("grupo", "reserva"):
        cm.recrutar(g, "yara")
        if onde == "reserva":
            m = cm.membro(g, "yara")
            g.comitiva.remove(m)
            g.reserva = [m]
    elif onde == "morta":
        g.marcar("comitiva:yara", "morto")
    return g


def ate_o_ossuario(g):
    """Da porta da capela até o ossuário, pelas salas já vencidas (1.79.0: a sala em que se está conta)."""
    for sala in ("salao", "sacristia", "ossuario"):
        assert missoes.ir_na_capela(g, sala), sala

class TestAcusacao(unittest.TestCase):
    def test_acusacao_na_investigacao_uma_vez(self):
        ui = Roteiro()
        g = investigando(ui=ui)
        self.assertEqual([c["id"] for c in estado(g)["missoes"]], [FEBRE])  # escondida antes
        self.assertTrue(missoes.cena_pendente(g))
        self.assertEqual(ui.cenas[-1], "Irmão Caspar")
        self.assertIn("uma moça no Charco dos Juncos", " ".join(ui.ditos))
        self.assertNotIn("Yara", " ".join(ui.ditos))  # ainda não a conhece: nem a cena nem o cartão dizem o nome
        m = caspar.registro(g)
        self.assertEqual((m["etapa"], m["cenas"]), ("acusacao", ["acusacao"]))
        cartao = next(c for c in estado(g)["missoes"] if c["id"] == CASPAR)
        self.assertIsNone(cartao["lugar_id"])  # nada a fazer ainda: objetivo sem marcador
        self.assertEqual(cartao["objetivo"], "Caspar acusa uma mulher de causar a febre.")
        self.assertNotIn("Yara", str(cartao))
        self.assertFalse(missoes.cena_pendente(g))
        self.assertEqual(ui.continuares[-1], ("Irmão Caspar", True))

    def test_nem_antes_do_canal_nem_fora_do_vau(self):
        for etapa in ("fonte", "canal"):
            g = investigando(etapa)
            g.mundo["missoes"][FEBRE]["cenas"].append("abertura")
            self.assertFalse(missoes.cena_pendente(g) and missoes.registro(g, CASPAR)["etapa"] == "acusacao")
        g = investigando()
        ir(g, "bosque_do_moinho")
        self.assertFalse(missoes.cena_pendente(g))

    def test_acusacao_conforme_a_yara(self):
        casos = {"grupo": "a praça inteira vê", "reserva": "Yara está no acampamento", "morta": "queimamos a bruxa",
                 "desconhecida": "concordam com a cabeça"}
        for onde, trecho in casos.items():
            ui = Roteiro()
            g = com_yara(investigando(ui=ui), onde)
            self.assertEqual(caspar.situacao_yara(g), onde)
            missoes.cena_pendente(g)
            self.assertIn(trecho, " ".join(ui.ditos), onde)

    def test_o_nome_so_depois_de_conhece_la(self):
        """Quem já a conhece (encontrou-a, anda com ela, ou ela morreu) ouve o nome; quem não conhece, quando a encontra,
        passa a ver o nome no Diário."""
        for onde in ("grupo", "reserva", "recusou", "morta"):
            ui = Roteiro()
            g = investigando(ui=ui)
            if onde == "recusou":
                g.marcar("comitiva:yara", "recusou")
            else:
                com_yara(g, onde)
            missoes.cena_pendente(g)
            if onde != "morta":  # morta, Caspar fala da bruxa que queimaram
                self.assertIn("erva que mata. Yara.", " ".join(ui.ditos), onde)
            cartao = next(c for c in estado(g)["missoes"] if c["id"] == CASPAR)
            self.assertEqual(cartao["objetivo"], "Caspar acusa Yara de causar a febre.", onde)
            self.assertIn("e não de Yara", cartao["requisitos"]["titulo"], onde)
        g = investigando()
        missoes.cena_pendente(g)
        cartao = next(c for c in estado(g)["missoes"] if c["id"] == CASPAR)
        self.assertIn("e não da mulher acusada", cartao["requisitos"]["titulo"])
        g.marcar("comitiva:yara", "recusou")  # a fogueira: ela disse o nome e foi embora
        cartao = next(c for c in estado(g)["missoes"] if c["id"] == CASPAR)
        self.assertEqual(cartao["objetivo"], "Caspar acusa Yara de causar a febre.")
        self.assertIn("Objetivo: Caspar acusa Yara de causar a febre.", str(cartao["historico"]))


class TestPraca(unittest.TestCase):
    def test_praca_nao_entrega_o_nome_de_quem_nao_conhece(self):
        """A praça (com ou sem a acusação antes), a opção de denunciar e o Diário falam da moça do Charco."""
        for onde, nome in (("desconhecida", False), ("grupo", True), ("recusou", True)):
            ui = Roteiro(["Ainda não"])
            g = resolvida("descansada", ui, lodo=True)
            if onde == "recusou":
                g.marcar("comitiva:yara", "recusou")
            else:
                com_yara(g, onde)
            missoes.cena_pendente(g)
            tela = " ".join(ui.ditos) + " ".join(ui.ofertas[-1]) + str(estado(g)["missoes"])
            self.assertEqual("Yara" in tela, nome, onde)
            self.assertIn("não da Yara (Carisma" if nome else "não da moça do Charco (Carisma", " ".join(ui.ofertas[-1]))

    def test_sem_prova_nao_ha_denuncia_e_da_para_responder_depois(self):
        ui = Roteiro(["Ainda não"])
        g = resolvida("destruida", ui)
        self.assertTrue(missoes.cena_pendente(g))
        self.assertEqual(ui.cenas[-1], "A Praça do Vau")
        self.assertIn("É o Irmão Caspar", " ".join(ui.ditos))  # não o conhecia: é apresentado aqui
        self.assertIn("falta prova", " ".join(ui.ditos))
        self.assertFalse(any(o.startswith("Denunciar") for o in ui.ofertas[-1]))
        m = caspar.registro(g)
        self.assertIsNone(m["desfecho"])
        cartao = next(c for c in estado(g)["missoes"] if c["id"] == CASPAR)
        self.assertEqual(cartao["lugar_id"], g.loc["id"])  # responder na praça: marcador no Vau
        self.assertEqual([o[1][2] for o in missoes.opcoes(g)], ["praca"])
        self.assertFalse(missoes.cena_pendente(g))  # a cena não repete; a ação fica

    def test_lodo_e_prova_e_nao_se_perde(self):
        """Recolhível no fundo antes ou depois da guardiã; o mago o analisa (prova forte)."""
        for classe, forte in (("guerreiro", False), ("mago", True)):
            g = resolvida("descansada", classe=classe)
            ir(g, "capela_afogada")
            self.assertEqual([o[1][2] for o in missoes.opcoes(g)], [])  # do lado de fora: o lodo é lá embaixo (1.79.0)
            ate_o_ossuario(g)
            self.assertEqual([o[1][2] for o in missoes.opcoes(g)], [])  # nem no ossuário: na água do fundo (1.80.0)
            self.assertTrue(missoes.ir_na_capela(g, "fundo"))
            self.assertEqual([o[1][2] for o in missoes.opcoes(g)], ["lodo"])
            self.assertTrue(missoes.executar(g, CASPAR, "lodo"))
            self.assertFalse(missoes.executar(g, CASPAR, "lodo"))
            self.assertEqual(caspar.prova(g), (True, forte))
        g = investigando("fundo")
        ir(g, "capela_afogada")  # (um save sem a sala: na etapa do fundo, o ossuário)
        g.ui.roteiro = ["Recolher uma amostra do lodo", "Voltar por enquanto"]
        lutas_vistas = []
        g.combate = lambda *a, **k: lutas_vistas.append(a)  # recolher não começa a luta com Ilse
        self.assertTrue(missoes.executar(g, FEBRE, "fundo"))  # no fundo, antes da guardiã também
        self.assertEqual((caspar.registro(g)["preparos"], lutas_vistas), (["lodo"], []))
        self.assertEqual(missoes.sala_atual(g), "ossuario")  # e o recuo sobe ao ossuário
        g = investigando("ossuario")
        ir(g, "capela_afogada")
        self.assertNotIn("lodo", [o[1][2] for o in missoes.opcoes(g)])

    def test_yara_no_grupo_e_prova_forte(self):
        g = com_yara(resolvida("destruida", lodo=True))
        self.assertEqual(caspar.prova(g), (True, True))

    def test_resposta_depois_pela_acao_da_praca(self):
        ui = Roteiro(["Ainda não", "Calar"])
        g = resolvida("descansada", ui)
        missoes.cena_pendente(g)
        self.assertTrue(missoes.executar(g, CASPAR, "praca"))
        self.assertEqual(caspar.registro(g)["desfecho"], "calar")
        self.assertFalse([o for o in missoes.opcoes(g) if o[1][1] == CASPAR])  # a herança de Berta segue à parte


class TestCombinacoes(unittest.TestCase):
    def decidir(self, desfecho, resposta, yara="desconhecida", aceita=True, lodo=True, classe="guerreiro"):
        ui = Roteiro([resposta])
        g = com_yara(resolvida(desfecho, ui, lodo=lodo, classe=classe), yara)
        testes = []
        g.teste = lambda attr, cd: testes.append((attr, cd)) or aceita
        rep = g.j.reputacao
        missoes.cena_pendente(g)
        return g, ui, testes, g.j.reputacao - rep

    def test_destruir_e_denunciar(self):
        g, ui, testes, rep = self.decidir("destruida", "Denunciar")
        m = caspar.registro(g)
        self.assertEqual((m["desfecho"], m["concluida"]), ("denunciado", g.dia))
        self.assertEqual(testes, [("carisma", caspar.CD_DENUNCIA)])
        self.assertEqual(rep, caspar.REPUTACAO["denunciado"])
        linhas = missoes.cartoes(g, todas=True)[1]["linhas"]
        self.assertEqual(linhas, ["Ilse: os ossos dela ficaram no fundo da capela, sem nome.",
                                  caspar.LINHA_CASPAR["denunciado"],
                                  "A moça do Charco: você não a conhece. Ninguém mais a procura."])
        self.assertFalse(caspar.fogueira_possivel(g))  # o pregador não queima ninguém depois disso
        self.assertEqual([c["id"] for c in estado(g)["missoes"]], [])  # nada ativo
        self.assertIn("a praça está vazia", consequencias.frase_da_vila(g))

    def test_descanso_e_apoiar_com_yara_no_grupo(self):
        g, ui, testes, rep = self.decidir("descansada", "Apoiar", yara="grupo")
        m = caspar.registro(g)
        self.assertEqual(m["desfecho"], "apoiar")
        self.assertEqual((testes, rep), ([], caspar.REPUTACAO["apoiar"]))
        self.assertTrue(cm.membro(g, "yara"))  # continua no grupo...
        self.assertTrue(caspar.yara_barrada(g))  # ...mas não entra no Vau, e o jogo diz isso
        self.assertLess(cm.membro(g, "yara")["aprovacao"], 0)
        linhas = missoes.cartoes(g, todas=True)[1]["linhas"]
        self.assertEqual(linhas[0], "Ilse: Vó Berta pôs uma pedra com o nome dela junto à fonte; Caspar finge não ver.")
        self.assertIn("a vigília não a deixa entrar no Vau", linhas[2])
        frase = consequencias.frase_da_vila(g)
        self.assertIn("vigília contra a bruxa", frase)
        self.assertIn("Yara espera do lado de fora", frase)
        self.assertTrue(caspar.fogueira_possivel(g))

    def test_destruir_e_apoiar_queima_os_ossos(self):
        g, *_ = self.decidir("destruida", "Apoiar")
        self.assertIn("queimados na praça", missoes.cartoes(g, todas=True)[1]["linhas"][0])

    def test_denuncia_recusada(self):
        g, ui, testes, rep = self.decidir("descansada", "Denunciar", yara="reserva", aceita=False)
        self.assertEqual(caspar.registro(g)["desfecho"], "denuncia_falhou")
        self.assertEqual(rep, caspar.REPUTACAO["denuncia_falhou"])
        self.assertFalse(caspar.fogueira_possivel(g))
        self.assertFalse(caspar.yara_barrada(g))
        self.assertIn("vigiada", missoes.cartoes(g, todas=True)[1]["linhas"][2])

    def test_calar_com_yara_morta(self):
        g, ui, testes, rep = self.decidir("destruida", "Calar", yara="morta")
        self.assertEqual((caspar.registro(g)["desfecho"], rep), ("calar", 0))
        self.assertEqual(missoes.cartoes(g, todas=True)[1]["linhas"][2], "Yara: morreu na fogueira de Caspar.")
        self.assertIn("fogueira no Charco fez o resto", " ".join(ui.ditos))

    def test_prova_forte_facilita(self):
        g, ui, testes, rep = self.decidir("descansada", "Denunciar", classe="mago")
        self.assertEqual(testes, [("carisma", caspar.CD_DENUNCIA)])  # o lodo foi dado pronto, sem a análise
        g, ui, testes, rep = self.decidir("descansada", "Denunciar", yara="grupo")
        self.assertEqual(testes, [("carisma", caspar.CD_DENUNCIA_FORTE)])

    def test_comitiva_reage_so_quem_anda_com_voce(self):
        ui = Roteiro(["Denunciar"])
        g = resolvida("destruida", ui, lodo=True)
        cm.recrutar(g, "odete")
        g.teste = lambda attr, cd: True
        antes = cm.membro(g, "odete")["aprovacao"]
        missoes.cena_pendente(g)
        self.assertGreater(cm.membro(g, "odete")["aprovacao"], antes)  # honestidade
        self.assertFalse(cm.membro(g, "yara") or cm.na_reserva(g, "yara"))  # ninguém foi recrutado
        self.assertIsNone(cm.membro(g, "morel"))

    def test_decisao_nao_repete(self):
        g, *_ = self.decidir("descansada", "Apoiar")
        rep = g.j.reputacao
        self.assertTrue(missoes.cena_pendente(g))  # a praça não volta: a próxima cena é o fim do capítulo
        self.assertEqual(g.ui.cenas[-1], "O Vale do Turvo")
        self.assertFalse(missoes.cena_pendente(g))
        self.assertFalse(missoes.executar(g, CASPAR, "praca"))
        caspar._resolver(g, "denunciar")
        self.assertEqual((caspar.registro(g)["desfecho"], g.j.reputacao), ("apoiar", rep))


class TestSaves(unittest.TestCase):
    def test_save_guarda_a_decisao(self):
        pasta = tempfile.mkdtemp()
        ui = Roteiro(["Denunciar"])
        g = resolvida("destruida", ui, pasta=pasta, lodo=True)
        g.teste = lambda attr, cd: True
        missoes.cena_pendente(g)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        self.assertEqual(caspar.registro(h)["desfecho"], "denunciado")
        self.assertTrue(missoes.cena_pendente(h))  # só o fim do capítulo, que o save ainda não viu
        self.assertEqual(h.ui.cenas, ["O Vale do Turvo"])
        self.assertFalse(missoes.cena_pendente(h))
        self.assertFalse(caspar.fogueira_possivel(h))

    def test_save_da_154_com_ilse_resolvida(self):
        """Um save da 1.54 (sem a missão de Caspar, febre concluída): carrega com Caspar na praça, a cena toca na
        próxima vez no Vau, e a prova se consegue voltando ao fundo da capela."""
        pasta = tempfile.mkdtemp()
        g = resolvida("descansada", pasta=pasta)
        del g.mundo["missoes"][CASPAR]
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(["Ainda não"]), g.caminho_save(), pasta)
        self.assertEqual(caspar.registro(h)["etapa"], "praca")
        self.assertTrue(missoes.cena_pendente(h))
        self.assertEqual(h.ui.cenas[-1], "A Praça do Vau")
        self.assertIn("É o Irmão Caspar", " ".join(h.ui.ditos))
        self.assertEqual(missoes.registro(h, FEBRE)["concluida"], g.dia)  # a febre não reabre
        ir(h, "capela_afogada")
        ate_o_ossuario(h)
        missoes.ir_na_capela(h, "fundo")
        self.assertEqual([o[1][2] for o in missoes.opcoes(h)], ["lodo"])

class TestMesmoDia(unittest.TestCase):
    """Voltando ao Vau no mesmo dia do confronto, nenhum texto conta uma noite que ainda não veio."""

    def textos(self, desfecho, dias):
        from tests.test_retorno import resolvida as volta
        ui = Roteiro()
        g = volta(desfecho, ui, dias=dias)
        missoes.cena_pendente(g)
        partes = list(ui.ditos) + [consequencias.frase_da_vila(g) or "", consequencias.atendente(g)["fala"],
                                   consequencias.fonte_no_diario(g) or ""]
        return " ".join(partes)

    def test_mesmo_dia_sem_noite_passada(self):
        for desfecho in ("destruida", "descansada"):
            texto = self.textos(desfecho, 0)
            for proibido in ("de noite", "esta noite", "noite inteira", "aquela noite", "a noite depois"):
                self.assertNotIn(proibido, texto, (desfecho, proibido))

    def test_no_dia_seguinte_a_noite_conta(self):
        self.assertIn("de noite", self.textos("descansada", 1))
        self.assertIn("noite inteira", self.textos("descansada", 1))
        self.assertIn("noite", self.textos("destruida", 2))


if __name__ == "__main__":
    unittest.main()


class TestDiarioConcluidas(unittest.TestCase):
    """O Diário com missões concluídas: as em andamento primeiro, a pendência à vista, as concluídas no fim, sem
    repetir o desfecho em "Mais recente" nem os preparos já no histórico (1.62.4)."""

    def texto(self, g):
        g.ui.ditos = []
        g._diario_texto()
        return g.ui.ditos

    def test_ativa_pendencia_e_concluida(self):
        g = resolvida("descansada")
        cartao = next(c for c in missoes.cartoes(g, todas=True) if c["id"] == FEBRE)
        self.assertIsNone(cartao["recente"])
        self.assertTrue(cartao["historico"])  # o histórico continua para consultar
        ditos = self.texto(g)
        ordem = [d for d in ditos if d.startswith(("Missão:", "Pendente:", "Concluídas"))]
        self.assertEqual(ordem, ["Missão: A Vigília de Caspar", "Pendente: A Febre do Turvo. Vó Berta ainda espera você "
                                 "na taverna.", "Concluídas (1):", "Missão: A Febre do Turvo (concluída)"])
        febre = ditos[ditos.index("Missão: A Febre do Turvo (concluída)"):]
        self.assertFalse(any(d.startswith("  Mais recente") or d == "  O que você já fez:" for d in febre))
        self.assertTrue(any(d.startswith("  Concluída no dia") for d in febre))

    def test_heranca_recebida_e_todas_concluidas(self):
        pasta = tempfile.mkdtemp()
        g = resolvida("descansada", pasta=pasta)
        missoes.registro(g, FEBRE)["cenas"].append("heranca")
        caspar.registro(g).update(desfecho="calar", concluida=g.dia)
        g.salvar(silencioso=True)
        h = Jogo.carregar(Roteiro(), g.caminho_save(), pasta)
        ditos = self.texto(h)
        self.assertFalse(any(d.startswith("Pendente:") for d in ditos))
        self.assertIn("Concluídas (2):", ditos)
        self.assertEqual([d for d in ditos if d.startswith("Missão:")],
                         ["Missão: A Febre do Turvo (concluída)", "Missão: A Vigília de Caspar (concluída)"])
