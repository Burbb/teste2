"""Ponto de entrada: python -m rpg"""

import argparse
import glob
import os
import sys

from .jogo import NIVEL_MAXIMO, FimDeJogo, Jogo
from .migracoes import SaveIncompativel
from .sistemas.persistencia import resumo_save
from .ui import UI

def escolher_save(ui, saves):
    """A lista de saves: na tela gráfica, cartões com classe, nível, dia e lugar; no texto, os nomes.
    Devolve o caminho escolhido ou None (voltar)."""
    resumos = [resumo_save(s) for s in saves]
    if ui.painel("saves", {"saves": resumos}):
        ui.meta_opcoes = [{"save": i} for i in range(len(saves))] + [{"voltar": True}]
        try:
            i = ui.escolher("", [r["nome"] for r in resumos] + ["Voltar"])
        finally:
            ui.meta_opcoes = None
    else:
        i = ui.escolher("Qual jogo?", [r["arquivo"] for r in resumos] + ["Voltar"])
    return saves[i] if i < len(saves) else None


def menu_principal(ui, args):
    while True:
        ui.cena("The Unquiet", None, "titulo")
        saves = sorted((s for s in glob.glob(os.path.join(args.saves, "*.json"))
                        if os.path.basename(s) != "legado.json"), key=os.path.getmtime, reverse=True)
        # Só a campanha (o mundo gerado saiu na 1.206.0): o modo (resgate ou hardcore) se escolhe na criação.
        opcoes = ["Novo jogo"] + (["Carregar jogo"] if saves else []) + ["Sair"]
        esc = opcoes[ui.escolher("", opcoes)]
        try:
            if esc == "Novo jogo":
                jogo = Jogo(ui, seed=args.seed, pasta_saves=args.saves)
                jogo.autosalvar = ui.interativo
                ui.jogo = jogo
                if not jogo.novo_jogo():
                    ui.jogo = None
                    continue
                if getattr(args, "dev", None):
                    from .dev import comecar_no_nivel
                    comecar_no_nivel(jogo, args.dev)
                jogo.rodar()
            elif esc == "Carregar jogo":
                caminho = escolher_save(ui, saves)
                if caminho:
                    try:
                        jogo = Jogo.carregar(ui, caminho, args.saves)
                    except (SaveIncompativel, ValueError, KeyError) as erro:
                        ui.dizer(f"Este save não abre: {erro}", "vermelho")
                        ui.pausar()
                        continue
                    jogo.autosalvar = ui.interativo
                    ui.jogo = jogo
                    ui.boas_vindas(jogo.j.nome)
                    jogo.rodar()
            else:
                ui.dizer("Até a próxima jornada!", "magenta")
                return
        except FimDeJogo:
            pass
        ui.jogo = None


def main():
    parser = argparse.ArgumentParser(description="The Unquiet — RPG de texto offline")
    parser.add_argument("--seed", type=int, help="semente do sorteio (o mesmo número repete a partida)")
    parser.add_argument("--terminal", action="store_true",
                        help="joga dentro do terminal, com painéis (precisa do textual)")
    parser.add_argument("--classico", action="store_true",
                        help="interface de terminal simples, sem dependências")
    parser.add_argument("--navegador", action="store_true",
                        help="abre no navegador mesmo se o pywebview (janela própria) estiver instalado")
    parser.add_argument("--sem-abrir", dest="abrir", action="store_false",
                        help="não abre o navegador sozinho (só mostra o endereço)")
    parser.add_argument("--porta", type=int, default=0, help="porta local da interface (padrão: qualquer livre)")
    parser.add_argument("--dev", type=int, metavar="N", choices=range(2, NIVEL_MAXIMO + 1),
                        help="teste: o jogo novo começa no nível N, com equipamento de acordo e pontos de talento")
    parser.add_argument("--sem-cor", action="store_true", help="desativa as cores (interface clássica)")
    parser.add_argument("--rapido", action="store_true", help="sem pausas dramáticas (interface clássica)")
    parser.add_argument("--velocidade", choices=["lento", "normal", "rapido", "instantaneo"], default="normal",
                        help="velocidade em que o texto aparece (F3 muda durante o jogo)")
    parser.add_argument("--saves", default=os.path.join(os.path.expanduser("~"), ".cronicas_da_fenda"),
                        help="pasta onde os jogos salvos ficam")
    args = parser.parse_args()

    if not args.classico and not args.terminal:
        from .web import jogar
        jogar(args, menu_principal)
        return

    if args.terminal and sys.stdout.isatty():
        try:
            from .tui import AppRPG
        except ImportError:
            print("Dica: instale 'textual' (pip install textual) para jogar no terminal com mapa e painéis.\n")
        else:
            AppRPG(args, menu_principal).run()
            return

    ui = UI(cor=False if args.sem_cor else None, rapido=args.rapido)
    ui.jogo = None
    try:
        menu_principal(ui, args)
    except KeyboardInterrupt:
        ui.dizer("\nAté a próxima jornada!", "magenta")


if __name__ == "__main__":
    main()
