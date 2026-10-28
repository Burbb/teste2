"""O "não" de quem tenta pagar sem ouro: o motor manda o motivo de cada serviço e compra (forja, curandeira, taverna,
templo, mercado), e só o que falta de fato. A tela mostra o aviso no controle e não manda a escolha ao motor (a
tentativa não gasta ouro, tempo nem sorteio: fumaca.mjs confere na tela)."""

import unittest

from rpg import sobrevivencia
from tests.test_abertura_parte2 import depois_da_despensa


class Parou(Exception):
    pass


class Anotador:
    """Troca o menu do jogo por um que anota as opções (rótulo e meta) e responde com `responder`; sem ele, para ali
    (só se queria ver as opções)."""

    def __init__(self, g, responder=None):
        self.g, self.menu, self.metas, self.responder = g, g.menu, [], responder
        g.menu = self

    def __call__(self, pergunta, opcoes):
        validas = [o for o in opcoes if o]
        self.metas.append({o[0]: (o[2] if len(o) > 2 else None) for o in validas})
        if not self.responder:
            raise Parou()
        return self.responder(validas)


def opcoes_da_vila(g):
    a = Anotador(g)
    try:
        g.menu_vila()
    except Parou:
        pass
    finally:
        g.menu = a.menu
    return a.metas[0]


def meta_de(metas, comeco):
    return next(m for rotulo, m in metas.items() if rotulo.startswith(comeco))


class TestMotivos(unittest.TestCase):
    def test_taverna_e_templo_dizem_ouro_insuficiente_so_quando_falta(self):
        g = depois_da_despensa()
        g.j.hp = g.j.max_hp // 2
        g.marcar("templo_gratis_usado")
        for ouro, motivo in ((0, "Ouro insuficiente."), (500, None)):
            g.j.ouro = ouro
            metas = opcoes_da_vila(g)
            for comeco in ("Taverna: dormir", "Taverna: pagar uma bebida", "Templo: cuidar da vida"):
                self.assertEqual(meta_de(metas, comeco).get("motivo"), motivo, (ouro, comeco))

    def test_rumores_esgotados_dizem_isso_e_nao_ouro(self):
        g = depois_da_despensa()
        g.j.ouro = 0
        g.marcar(f"rumores:{g.dia}:{g.loc['id']}", 2)
        self.assertEqual(meta_de(opcoes_da_vila(g), "Taverna: pagar uma bebida")["motivo"],
                         "Os fregueses já contaram tudo o que sabiam hoje.")

    def test_caneca_por_conta_da_casa_sem_motivo(self):
        g = depois_da_despensa()
        g.mundo["abertura"]["caneca"] = True
        g.j.ouro = 0
        self.assertNotIn("motivo", meta_de(opcoes_da_vila(g), "Taverna: uma bebida e os rumores (por conta da casa)"))

    def test_forja_e_curandeira_mandam_o_motivo_no_painel(self):
        g = depois_da_despensa()
        g.marcar("curandeira_gratis_usado")
        g.j.ferimentos.append({"id": "corte", "dias": sobrevivencia.FERIMENTOS["corte"]["dias"], "tratado": False})
        paineis = []
        g.ui.painel = lambda tipo, dados: paineis.append((tipo, dados)) or True
        g.materiais = {"fragmento": 99}  # a forja: o que falta é só o ouro
        for ouro, motivo in ((0, "Ouro insuficiente."), (999, None)):
            g.j.ouro = ouro
            voltar = Anotador(g, lambda opcoes: next(o[1] for o in opcoes if o[2] and o[2].get("voltar")))
            g.ferreiro()
            g.curandeiro()
            g.menu = voltar.menu
            forja = next(d for t, d in reversed(paineis) if t == "forja")
            cabana = next(d for t, d in reversed(paineis) if t == "curandeira")
            # na forja, o motivo de cada reforço diz quanto ouro falta ("Faltam 20 de ouro"), no próprio passo
            motivos = {p["passos"][0]["motivo"] for p in forja["pecas"] if p.get("passos")}
            if motivo:
                self.assertTrue(motivos and all(m and m.endswith("de ouro") for m in motivos), motivos)
            else:
                self.assertEqual(motivos, {None})
            self.assertEqual({f["motivo"] for f in cabana["ferimentos"]}, {motivo})

    def test_mercado_diz_o_motivo_de_cada_um(self):
        # o motivo que o aviso repete: ouro, estoque e capacidade não se confundem
        g = depois_da_despensa()
        g.j.ouro = 0
        d = g.dados_loja()
        motivos = {c["id"]: c["motivo"] for c in d["consumiveis"]}
        self.assertEqual(motivos["tocha"], "Ouro insuficiente.")
        estoque = g.estoque_suprimentos()
        g.lojas.setdefault(g._chave_vendidos(), {})["tocha"] = estoque["tocha"]  # esgotada hoje
        g.j.ouro = 999
        self.assertEqual(next(c for c in g.dados_loja()["consumiveis"] if c["id"] == "tocha")["motivo"], "Esgotado")
        # o Esgotado diz qual motivo é (o ícone próprio, o caixote); os outros motivos não têm id (ficam no cadeado)
        ids = {c["id"]: c["motivo_id"] for c in g.dados_loja()["consumiveis"]}
        self.assertEqual(ids["tocha"], "esgotado")
        g.j.ouro = 0
        self.assertEqual({c["motivo_id"] for c in g.dados_loja()["consumiveis"] if c["motivo"] == "Ouro insuficiente."}, {None})
        g.j.ouro = 999
        import pathlib
        estatico = pathlib.Path(__file__).resolve().parents[1] / "rpg/web/static"
        self.assertIn('MOTIVO = { esgotado: "motivo-esgotado" }', (estatico / "icones.js").read_text(encoding="utf-8"))
        self.assertIn('Icones.motivo(id)) || S("cadeado", 1)', (estatico / "telas/mercado.js").read_text(encoding="utf-8"))
        for sufixo in ("", "@2x"):
            self.assertTrue((estatico / f"hud/icones/motivo-esgotado-16{sufixo}.png").exists())
        g.j.provisoes = sobrevivencia.MAX_PROVISOES
        self.assertEqual(next(c for c in g.dados_loja()["consumiveis"] if c["id"] == "provisoes")["motivo"],
                         "Você já carrega o máximo de comida.")


if __name__ == "__main__":
    unittest.main()
