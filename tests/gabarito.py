"""Gabarito de regressão: partidas jogadas pelo robô com sementes fixas.

Cada partida vira uma transcrição completa (texto, opções oferecidas, escolhas, lances de combate,
efeitos, o que a tela gráfica recebe e o save final). O hash de cada transcrição fica guardado em tests/gabarito.json. Uma
refatoração que não muda a jogabilidade precisa reproduzir as mesmas transcrições, evento por evento.

Rode com:
    python -m tests.gabarito            # confere (o mesmo que o teste faz)
    python -m tests.gabarito --mostrar  # grava as transcrições em /tmp para comparar com diff
    python -m tests.gabarito --atualizar  # quando a jogabilidade mudou DE PROPÓSITO
"""

import hashlib
import json
import os
import random
import re
import sys
import tempfile

from rpg.jogo import Jogo
from rpg.ui import BotUI, InterfaceGrafica, LimiteBot

ARQUIVO = os.path.join(os.path.dirname(__file__), "gabarito.json")
CLASSES = ("guerreiro", "arqueiro", "mago")
SEMENTES = (3, 17, 42)
DECISOES = 700


class Gravador(BotUI):
    """O robô de sempre, mas anotando tudo o que a interface recebe."""

    def __init__(self, rng, web=False):
        super().__init__(rng, max_decisoes=DECISOES)
        self.linhas = []
        self.web = web  # web=True: o motor segue os caminhos da interface gráfica (painéis, metadados)

    def _imprimir(self, linha):
        self.linhas.append(linha)

    def escolher(self, pergunta, opcoes):
        metas = self.meta_opcoes
        voltar = [k for k, o in enumerate(opcoes) if o.startswith(("Voltar", "Sair do mercado"))]
        if self.web and voltar and self.rng.random() < 0.5:
            # Nas telas da interface gráfica há dezenas de ações; sem isso o robô passaria a partida no inventário.
            self.decisoes += 1
            if self.decisoes > self.max_decisoes:
                raise LimiteBot()
            i = voltar[0]
        else:
            i = super().escolher(pergunta, opcoes)
        self.linhas.append("ESCOLHA " + json.dumps({"p": pergunta, "o": opcoes, "m": metas, "i": i},
                                                   ensure_ascii=False, sort_keys=True, default=str))
        return i

    def lance(self, tipo, **dados):
        self.linhas.append("LANCE " + json.dumps({"t": tipo, **dados}, ensure_ascii=False, sort_keys=True,
                                                 default=str))

    def fala(self, cid, nome, texto):
        self.linhas.append(f"FALA {cid} {texto}")

    def opiniao(self, cid, nome, delta):
        self.linhas.append(f"OPINIAO {cid} {delta}")

    def celebrar(self, tipo, dados):
        self.linhas.append("CELEBRAR " + json.dumps({"t": tipo, "d": dados}, ensure_ascii=False, sort_keys=True,
                                                    default=str))

    def mostrar_mapa(self, grande=False):
        self.linhas.append(f"MAPA {grande}")

    def painel(self, tipo, dados):
        if not self.web:
            return False
        self.linhas.append("PAINEL " + json.dumps({"t": tipo, "d": dados}, ensure_ascii=False, sort_keys=True,
                                                  default=str))
        return True


class GravadorWeb(InterfaceGrafica, Gravador):
    """O robô imitando a tela gráfica: os mesmos caminhos do motor que a WebUI segue.

    Antes de cada escolha, anota o estado que a tela estaria desenhando (HUD, mundo, lugar, luta, contratos), parte
    por parte e só quando a parte mudou. É a rede da tela: os números que ela mostra vêm prontos daqui."""

    jogo = None
    _vistos = {}

    def escolher(self, pergunta, opcoes):
        from rpg.web.estado import estado
        e = estado(self.jogo) if self.jogo else None
        for parte, valor in sorted((e or {}).items()):
            linha = json.dumps(valor, ensure_ascii=False, sort_keys=True, default=str)
            if self._vistos.get(parte) != linha:
                self._vistos[parte] = linha
                self.linhas.append(f"ESTADO {parte} {linha}")
        return super().escolher(pergunta, opcoes)

    def arvore_talentos(self, dados):
        self.linhas.append("ARVORE " + json.dumps(dados, ensure_ascii=False, sort_keys=True, default=str))


def transcrever(seed, classe, web=False):
    from rpg import combate
    combate._SERIE[0] = 0  # numeração dos combates (ids das cartas): cada partida começa do zero
    with tempfile.TemporaryDirectory() as pasta:
        ui = (GravadorWeb if web else Gravador)(random.Random(seed * 7 + 1), web=web)
        # A semente 3 joga no hardcore (morte permanente); as outras no modo brando, para partidas mais longas.
        g = Jogo(ui, seed=seed, pasta_saves=pasta, hardcore=seed == 3)
        if web:
            ui.jogo, ui._vistos = g, {}
        g.iniciar("Robô", classe)
        try:
            g.rodar()
        except LimiteBot:
            pass
        # O nome do registro da run leva data e hora: fora isso, tudo tem de bater.
        linhas = [re.sub(r"\d{4}-\d{2}-\d{2}_\d{4}", "<DATA>", x.replace(pasta, "<PASTA>")) for x in ui.linhas]
        # O estado final inteiro, do jeito que vai para o save.
        g.salvar(silencioso=True)
        for nome in sorted(os.listdir(pasta)):
            if nome.endswith(".json") and nome != "legado.json":
                with open(os.path.join(pasta, nome), encoding="utf-8") as f:
                    dados = json.load(f)
                if isinstance(dados, dict):
                    dados.pop("arquivo_run", None)
                linhas.append("SAVE " + json.dumps(dados, ensure_ascii=False, sort_keys=True))
        return linhas


def transcrever_comitiva(seed):
    """Lutas com a comitiva (o robô quase nunca a recruta nas partidas acima): Odette e Morel, Morel e Yara (do Vazio
    nas sementes ímpares), Odette e Yara, cada dupla com um herói de uma classe, três lutas seguidas."""
    from rpg import combate, comitiva
    combate._SERIE[0] = 0
    with tempfile.TemporaryDirectory() as pasta:
        ui = Gravador(random.Random(seed))
        g = Jogo(ui, seed=seed, pasta_saves=pasta, hardcore=False)
        g.iniciar("Robô", CLASSES[seed % 3])
        for _ in range(3):
            g.subir_nivel()
        dupla = [["odete", "morel"], ["morel", "yara"], ["odete", "yara"]][seed % 3]
        for cid in dupla:
            comitiva.recrutar(g, cid)
        if "yara" in dupla and seed % 2:
            comitiva.membro(g, "yara")["caminho"] = "vazio"
        g.mundo["atual"] = next(l for l in g.mundo["locais"] if l["tipo"] == "selvagem")["id"]
        for _ in range(3):
            try:
                g.combate(g.grupo(), pode_fugir=False)
            except Exception as e:  # a derrota encerra a sequência (o nome dela entra na transcrição)
                ui.linhas.append(f"FIM {type(e).__name__}")
                break
            g.j.hp = g.j.max_hp
        return [re.sub(r"\d{4}-\d{2}-\d{2}_\d{4}", "<DATA>", x.replace(pasta, "<PASTA>")) for x in ui.linhas]


SEMENTES_COMITIVA = (1, 2, 3, 4, 5, 6)


def casos():
    for seed in SEMENTES:
        for classe in CLASSES:
            for web in (False, True):
                yield f"{classe}-{seed}-{'web' if web else 'texto'}", seed, classe, web
    for seed in SEMENTES_COMITIVA:
        yield f"comitiva-{seed}", seed, "comitiva", False


def resumo_hash(linhas):
    return hashlib.sha256("\n".join(linhas).encode("utf-8")).hexdigest()


def transcricao(seed, classe, web):
    return transcrever_comitiva(seed) if classe == "comitiva" else transcrever(seed, classe, web)


def calcular():
    return {nome: resumo_hash(transcricao(seed, classe, web)) for nome, seed, classe, web in casos()}


def main():
    if "--atualizar" in sys.argv:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(calcular(), f, indent=1, sort_keys=True)
        print("gabarito atualizado")
        return
    if "--mostrar" in sys.argv:
        destino = tempfile.mkdtemp(prefix="gabarito_")
        for nome, seed, classe, web in casos():
            with open(os.path.join(destino, nome + ".txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(transcricao(seed, classe, web)))
        print("transcrições em", destino)
        return
    with open(ARQUIVO, encoding="utf-8") as f:
        esperado = json.load(f)
    atual = calcular()
    ruins = [n for n in set(esperado) | set(atual) if esperado.get(n) != atual.get(n)]
    print("OK" if not ruins else "DIFERENTE: " + ", ".join(ruins))


if __name__ == "__main__":
    main()
