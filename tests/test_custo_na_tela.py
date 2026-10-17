"""O custo de uma habilidade chega à tela junto do começo da ação (etapa 1B do plano 23).

O motor desconta o recurso (e as flechas) antes de agir, depois de o alvo ser confirmado. A tela só via o valor pago no
próximo estado, que saía depois do texto do golpe ou do fim de uma salva em área: o golpe, e às vezes a cura da própria
habilidade (Drenar Vida, Sede de Sangue), apareciam antes do custo. Aqui, pela ponte de verdade (rpg/web/ponte.py), o
que ela publica: na mira, ainda cancelável, o recurso intacto; voltando, intacto; confirmada, um estado com o custo
pago antes do lance "acao", e nenhum valor que volte atrás."""

import tempfile
import unittest

from rpg import dev
from rpg.combate import Combate
from rpg.jogo import Jogo
from rpg.web.ponte import WebUI


class Roteiro(WebUI):
    """Escolhe Habilidades e a habilidade pedida; na mira, volta uma vez (se pedido) e depois confirma o primeiro alvo.
    Para na pergunta seguinte à ação."""

    def __init__(self, hab, cancelar=False, ataque=False):
        super().__init__()
        self.hab, self.cancelar, self.ataque = hab, cancelar, ataque

    def _perguntar(self, tipo, **d):
        if tipo != "opcoes":
            return None
        p, ops = d.get("pergunta", ""), d.get("opcoes", [])
        self.canal.publicar({"t": "pergunta", "pergunta": p})
        if p == "Sua ação:":
            if any(m["t"] == "lance" and m.get("tipo") == "acao" and m.get("de") == "j" for m in self.canal.mensagens):
                raise StopIteration  # a ação foi feita: o resto da luta não interessa
            alvo = "atacar" if self.ataque else "habilidades"
            return next(i for i, o in enumerate(ops) if (o.get("meta") or {}).get("acao") == alvo)
        if p == "Habilidades:":
            return next(i for i, o in enumerate(ops) if (o.get("meta") or {}).get("habilidade") == self.hab)
        if p == "Alvo:" and self.cancelar:
            self.cancelar = False
            return len(ops) - 1  # Voltar
        return 0


def lutar(classe, spec, hab=None, cancelar=False, ataque=False):
    ui = Roteiro(hab, cancelar, ataque)
    g = Jogo(ui, seed=5, pasta_saves=tempfile.mkdtemp())
    ui.jogo = g
    g.iniciar("Teste", classe, "turvo")
    g.escolher_companheiro = lambda *_: None  # o patrulheiro sem a pergunta do animal
    dev.subir_ate(g, 12, spec=spec)
    g.j.hp, g.j.rec = g.j.max_hp // 2, g.j.max_rec
    inicio = (g.j.rec, g.j.flechas if classe == "arqueiro" else None)  # a tela só manda flechas ao arqueiro
    try:
        Combate(g, [g.inimigo("caido", nivel=9), g.inimigo("caido", nivel=9)]).executar()
    except StopIteration:
        pass
    return ui.canal.mensagens, inicio


def heroi(m):
    return m["estado"]["heroi"]


class TestCustoNaTela(unittest.TestCase):
    def conferir(self, msgs, inicio, gasto_rec, gasto_flechas=0, cancelou=False):
        acao = next(k for k, m in enumerate(msgs) if m["t"] == "lance" and m.get("tipo") == "acao" and m.get("de") == "j")
        mira = [k for k, m in enumerate(msgs) if m["t"] == "pergunta" and m["pergunta"] == "Alvo:"]
        estados = [(k, heroi(m)) for k, m in enumerate(msgs) if m["t"] == "estado" and m["estado"].get("combate")]
        # na mira (e depois de voltar dela), nada foi pago
        for k in mira:
            h = [h for i, h in estados if i < k][-1]
            self.assertEqual((h["rec"], h["flechas"]), inicio, "o recurso mudou com a mira ainda cancelável")
        self.assertEqual(len(mira), 2 if cancelou else len(mira))
        # confirmada: o estado logo antes do lance "acao" já tem o custo pago
        antes = [h for i, h in estados if i < acao][-1]
        pago = (inicio[0] - gasto_rec, (inicio[1] - gasto_flechas) if inicio[1] is not None else None)
        self.assertEqual((antes["rec"], antes["flechas"]), pago, "o custo não chegou à tela antes da ação")
        # e durante a ação nenhum estado devolve o que foi pago (sem desconto visual que volte atrás)
        fim = next(k for k, m in enumerate(msgs) if m["t"] == "lance" and m.get("tipo") == "fim_acao" and k > acao)
        for i, h in estados:
            if acao < i < fim:
                self.assertLessEqual(h["rec"], pago[0] + 10, "o recurso voltou ao valor de antes do custo")

    def test_drenar_vida_mira_cancelar_e_executar(self):
        msgs, inicio = lutar("mago", "necromante", "drenar_vida", cancelar=True)
        self.conferir(msgs, inicio, 14, cancelou=True)
        # a cura da drenagem vem depois do custo na tela
        acao = next(k for k, m in enumerate(msgs) if m["t"] == "lance" and m.get("tipo") == "acao")
        cura = next(k for k, m in enumerate(msgs) if m["t"] == "lance" and m.get("tipo") == "cura" and m.get("em") == "j")
        pago = max(k for k, m in enumerate(msgs) if k < acao and m["t"] == "estado")
        self.assertLess(pago, cura)

    def test_area_com_foco_e_flechas(self):
        msgs, inicio = lutar("arqueiro", "patrulheiro", "chuva_flechas")
        h = next(x for x in msgs if x["t"] == "estado" and x["estado"].get("combate"))
        self.assertIsNotNone(heroi(h)["flechas"])
        self.conferir(msgs, inicio, 20, gasto_flechas=2)

    def test_vigor_com_cura(self):
        msgs, inicio = lutar("guerreiro", "berserker", "sede_sangue")
        self.conferir(msgs, inicio, 12)

    def test_flecha_do_ataque_basico(self):
        msgs, inicio = lutar("arqueiro", "patrulheiro", ataque=True)
        acao = next(k for k, m in enumerate(msgs) if m["t"] == "lance" and m.get("tipo") == "acao" and m.get("de") == "j")
        antes = [heroi(m) for k, m in enumerate(msgs) if k < acao and m["t"] == "estado" and m["estado"].get("combate")][-1]
        self.assertEqual(antes["flechas"], inicio[1] - 1)


if __name__ == "__main__":
    unittest.main()
