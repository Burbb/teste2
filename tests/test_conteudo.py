"""Validador de conteúdo: toda referência entre catálogos existe.

Conteúdo é dado, e dado escrito à mão erra o nome: uma habilidade de família que não está em HABS, um bioma que
chama uma família que não existe, um título de evento para um evento que mudou de nome, um ícone sem desenho. Sem
este teste, o erro aparece só na partida (ou nunca: uma reação da comitiva com o nome errado simplesmente não
acontece). Cada teste aqui diz o que falta e onde.
"""

import os
import re
import unittest

from rpg import comitiva
from rpg.dados import AFIXOS, BIOMAS, FAMILIAS, GUARDIOES, LORE, TRACOS
from rpg.eventos import motor
from rpg.eventos.titulos import TITULOS
from rpg.classes import CLASSES
from rpg.habilidades import ANIMACOES, FAMILIAS_TELA, HABILIDADES
from rpg import balanceamento as bal
from rpg.inimigos import HABS
from rpg import itens
from rpg.itens import CONSUMIVEIS, RECURSOS
from rpg.regras import NIVEL_MIN_FAMILIA
from rpg.sistemas.confronto import CRIATURAS_DA_FENDA
from rpg.talentos import NIVEL_CAMADA, PASSIVAS, RAMOS_COMUNS, TALENTOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESTATICO = os.path.join(RAIZ, "rpg", "web", "static")


def _ler(*partes):
    with open(os.path.join(ESTATICO, *partes), encoding="utf-8") as f:
        return f.read()


def _sprites():
    """Os nomes de todo desenho: os da grade (`nome: [`) e os derivados (`S.nome = trocar(...)`)."""
    js = _ler("sprites-dados.js")
    return set(re.findall(r"^\s{4}(\w+):\s*\[", js, re.M)) | set(re.findall(r"\bS\.(\w+)\s*=", js))


def _mapa_js(arquivo, nome):
    """Um mapa {id: "ícone"} declarado em JS, como dicionário Python (os que ainda moram na tela)."""
    js = _ler(*arquivo.split("/"))
    m = re.search(rf"const {nome}\s*=\s*\{{(.*?)\}};", js, re.S)
    assert m, f"{arquivo}: mapa {nome} não encontrado"
    return dict(re.findall(r"\"?([\w-]+)\"?:\s*\[?\"(\w+)\"", m.group(1)))


class Catalogo(unittest.TestCase):
    def existe(self, chave, catalogo, msg):
        """assertIn sem despejar o catálogo inteiro na falha: só a mensagem que diz o que falta e onde."""
        if chave not in catalogo:
            self.fail(msg)


class TestInimigos(Catalogo):
    def test_habilidades_citadas_existem(self):
        citadas = {f"família {k}": f.get("habs", []) for k, f in FAMILIAS.items()}
        citadas.update({f"afixo {k}": a.get("habs", []) for k, a in AFIXOS.items()})
        for bioma, lista in GUARDIOES.items():
            for i, t in enumerate(lista):
                citadas[f"guardião {bioma}[{i}]"] = t.get("habs", [])
                for n, fase in enumerate(t.get("fases", [])):
                    citadas[f"guardião {bioma}[{i}] fase {n}"] = fase.get("habs", [])
        for onde, habs in citadas.items():
            for h in habs:
                self.existe(h, HABS, f"{onde}: habilidade '{h}' não existe em HABS (rpg/inimigos.py)")

    def test_familias_citadas_existem(self):
        for bioma, b in BIOMAS.items():
            for f in b["familias"]:
                self.existe(f, FAMILIAS, f"bioma {bioma}: família '{f}' não existe")
        for f in NIVEL_MIN_FAMILIA:
            self.existe(f, FAMILIAS, f"NIVEL_MIN_FAMILIA: família '{f}' não existe")
        for _, f in CRIATURAS_DA_FENDA:
            self.existe(f, FAMILIAS, f"CRIATURAS_DA_FENDA: família '{f}' não existe")
        for bioma, lista in GUARDIOES.items():
            for t in lista:
                if t.get("invoca"):
                    self.existe(t["invoca"], FAMILIAS, f"guardião de {bioma}: invoca '{t['invoca']}' não existe")
        for bioma in GUARDIOES:
            self.existe(bioma, BIOMAS, f"GUARDIOES: bioma '{bioma}' não existe")

    def test_toda_familia_que_aparece_tem_lore(self):
        """O bestiário conta e descreve pelo LORE: uma família que aparece sem lore fica sem texto e desconta o total."""
        aparecem = {f for b in BIOMAS.values() for f in b["familias"]}
        aparecem |= {f for _, f in CRIATURAS_DA_FENDA} | {"espectro", "xama_caido"}
        aparecem |= {t["invoca"] for lista in GUARDIOES.values() for t in lista if t.get("invoca")}
        for f in sorted(aparecem):
            self.existe(f, LORE, f"família '{f}' aparece no mundo mas não tem LORE (rpg/dados.py)")


    def test_tracos_citados_existem(self):
        for k, f in FAMILIAS.items():
            for t in f.get("tracos", []):
                self.existe(t, TRACOS, f"família {k}: traço '{t}' não existe em TRACOS (rpg/dados.py)")
        for bioma, lista in GUARDIOES.items():
            for t in lista:
                for tr in t.get("tracos", []) + [x for fase in t.get("fases", []) for x in fase.get("tracos", [])]:
                    self.existe(tr, TRACOS, f"guardião de {bioma}: traço '{tr}' não existe em TRACOS")


class TestTalentos(Catalogo):
    def test_ramo_e_camada_de_cada_talento(self):
        """O ramo é a base, o tronco ou uma especialização da própria classe; a camada tem nível em NIVEL_CAMADA."""
        for classe, lista in TALENTOS.items():
            validos = set(RAMOS_COMUNS) | set(CLASSES[classe]["specs"])
            for t in lista:
                self.existe(t["ramo"], validos, f"talento '{t['id']}' ({classe}): ramo '{t['ramo']}' não é base, "
                                                f"tronco nem especialização de {classe}")
                self.existe(t["camada"], NIVEL_CAMADA, f"talento '{t['id']}': camada {t['camada']} sem nível em "
                                                       "NIVEL_CAMADA (rpg/talentos.py)")

    def test_ids_unicos(self):
        ids = [t["id"] for lista in TALENTOS.values() for t in lista]
        self.assertEqual(sorted({i for i in ids if ids.count(i) > 1}), [], "talentos com o mesmo id")


class TestEventos(Catalogo):
    def test_titulos_e_reacoes_apontam_para_eventos_que_existem(self):
        ids = {ev.id for ev in motor.REGISTRO}
        for k in TITULOS:
            self.existe(k, ids, f"TITULOS: evento '{k}' não existe (o título nunca aparece)")
        for evento, _opcao in comitiva.REACOES:
            self.existe(evento, ids, f"REACOES: evento '{evento}' não existe (a comitiva nunca reage)")

    def test_ids_de_evento_unicos(self):
        ids = [ev.id for ev in motor.REGISTRO]
        repetidos = sorted({i for i in ids if ids.count(i) > 1})
        self.assertEqual(repetidos, [], f"eventos com o mesmo id: {repetidos}")


class TestApresentacao(Catalogo):
    """Como o conteúdo aparece na tela: todo ícone tem desenho, toda cor e animação é uma que a tela sabe fazer. Sem
    isso, uma habilidade nova aparece com a estrela genérica, calada (ou sem a cor, ou sem o jeito de animar)."""

    @classmethod
    def setUpClass(cls):
        cls.sprites = _sprites()
        css = "".join(open(os.path.join(ESTATICO, "css", f), encoding="utf-8").read()
                      for f in os.listdir(os.path.join(ESTATICO, "css")))
        cls.cores_texto = set(re.findall(r"\.rx-([a-z]+)", css))
        cls.cores_carta = set(re.findall(r"\.el-([a-z]+)", css))

    def _confere(self, mapa, onde):
        for k, icone in mapa.items():
            self.existe(icone, self.sprites, f"{onde}: '{k}' usa o ícone '{icone}', que não tem desenho")

    def test_habilidades(self):
        for k, h in HABILIDADES.items():
            onde = f"habilidade '{k}' (rpg/habilidades.py)"
            self.existe(h.get("icone"), self.sprites, f"{onde}: ícone '{h.get('icone')}' sem desenho")
            self.existe(h.get("familia"), FAMILIAS_TELA, f"{onde}: família '{h.get('familia')}' fora de FAMILIAS_TELA")
            self.existe(h["familia"], self.cores_carta, f"{onde}: a cor el-{h['familia']} não existe no CSS")
            if h.get("anim"):
                self.existe(h["anim"], ANIMACOES, f"{onde}: anim '{h['anim']}' fora de ANIMACOES")
            if h.get("realce"):
                self.existe(h["realce"], self.cores_texto, f"{onde}: realce '{h['realce']}' sem cor .rx- no CSS")
        for k, h in HABS.items():
            if h.get("anim"):
                self.existe(h["anim"], ANIMACOES, f"habilidade de inimigo '{k}': anim '{h['anim']}' fora de ANIMACOES")
        for k, c in CLASSES.items():
            self.existe(c.get("icone_ataque"), self.sprites, f"classe '{k}': icone_ataque sem desenho")

    def test_animacoes_que_a_tela_sabe_fazer(self):
        js = _ler("batalha.js")
        for a in ANIMACOES:
            self.existe(f'm.anim === "{a}"', js, f"anim '{a}' em ANIMACOES, mas batalha.js não sabe animá-la")

    def test_talentos(self):
        fichas = [(t["id"], t) for lista in TALENTOS.values() for t in lista] + list(PASSIVAS.items())
        for k, t in fichas:
            if "camada" in t:  # nó da árvore (a passiva não aparece na árvore)
                self.existe(t.get("icone"), self.sprites, f"talento '{k}': ícone '{t.get('icone')}' sem desenho")
            if t.get("realce"):
                self.existe(t["realce"], self.cores_texto, f"talento '{k}': realce '{t['realce']}' sem cor .rx-")

    def test_tracos(self):
        mapa = _mapa_js("batalha.js", "ICONE_TRACO")
        self._confere(mapa, "ICONE_TRACO")
        for t in TRACOS:
            self.existe(t, mapa, f"traço '{t}' sem ícone em ICONE_TRACO (batalha.js)")

    def test_equipamentos(self):
        """Toda base e todo único têm desenho; ids de único não se repetem."""
        for base, icone in itens._ICONE_BASE.items():
            self.existe(icone, self.sprites, f"base '{base}': ícone '{icone}' sem desenho")
        for u in itens.UNICOS:
            self.existe(u.get("icone"), self.sprites, f"único '{u['nome']}': ícone '{u.get('icone')}' sem desenho")
        ids = [u["id"] for u in itens.UNICOS]
        self.assertEqual(sorted({i for i in ids if ids.count(i) > 1}), [], "únicos com o mesmo id")
        for icone in itens.ICONE_ESPACO.values():
            self.existe(icone, self.sprites, f"ICONE_ESPACO: '{icone}' sem desenho")

    def test_consumiveis(self):
        """Todo consumível tem desenho; o mercado tem estoque de tudo o que vende; o contador do topo existe."""
        hud = _ler("app/paineis.js")
        fichas = list(CONSUMIVEIS.items()) + list(RECURSOS.items())
        for k, c in fichas:
            self.existe(c.get("icone"), self.sprites, f"consumível '{k}': ícone '{c.get('icone')}' sem desenho")
            if c.get("hud"):
                self.existe(f'recurso("{c["hud"]}"', hud, f"consumível '{k}': contador '{c['hud']}' não existe no topo")
        for k, c in CONSUMIVEIS.items():
            if c["mercado"]:
                self.existe(k, bal.ESTOQUE_MERCADO, f"o mercado vende '{k}', mas falta o estoque em ESTOQUE_MERCADO")
            if c["em_aliado"]:
                self.assertTrue(c["luta"] or c["fora"], f"'{k}' serve num aliado, mas não se usa em lugar nenhum")


if __name__ == "__main__":
    unittest.main()
