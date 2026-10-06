"""Ponto de entrada: python -m rpg"""

import argparse
import glob
import os
import sys

from .jogo import FimDeJogo, Jogo
from .ui import UI

COMO_JOGAR = """\
COMO JOGAR

• Escolha opções pelo número (ou clicando, na interface moderna).
• Cada ação (explorar, viajar um trecho, passear) consome um período do dia:
  manhã, tarde, anoitecer e noite. À noite os inimigos são mais fortes.
• Acampe ou durma na taverna para recuperar vida e começar um novo dia.
• O nível dos inimigos depende da REGIÃO (veja "Nv." no mapa), não do seu.
  Regiões longe do início e a corrupção alta deixam tudo mais perigoso.
• Derrote os 3 guardiões para obter os Sigilos e abrir caminho até a Cidadela.
• A corrupção cresce a cada dia. Se chegar a 100%, o jogo acaba.
  Cada guardião derrotado faz a corrupção recuar.
• No nível 4 sua classe se ramifica em uma de duas especializações.
• Ganhe pontos de talento ao subir de nível e ao derrotar guardiões.
• Escolhas têm consequências: quem você ajuda (ou rouba) pode voltar mais tarde.
• Derrote criaturas para aprender suas fraquezas (veja o Bestiário).
• Ouça rumores nas tavernas: revelam tesouros, feras e pontos fracos.
• A MORTE É PERMANENTE. (Com --brando, você é resgatado ao cair, perdendo
  ouro e dois dias.)
• Coma: cada dia consome 1 provisão. Sem comida você enfraquece e morre.
• Golpes pesados deixam FERIMENTOS que duram dias. Feridas abertas sem
  bandagem podem infeccionar — e infecção mata. Curandeiros tratam tudo.
• À noite, nas ruínas e na cidadela é escuro: leve tochas.
• A mana do mago só volta descansando (ou com tônicos).
• Seus heróis anteriores deixam lendas, estátuas e túmulos nas próximas partidas.
"""


def menu_principal(ui, args):
    while True:
        ui.cena("Crônicas da Fenda", "um RPG de texto onde nenhuma jornada é igual à outra", "titulo")
        saves = sorted(s for s in glob.glob(os.path.join(args.saves, "*.json"))
                       if os.path.basename(s) != "legado.json")
        opcoes = ["Novo jogo"] + (["Carregar jogo"] if saves else []) + ["Como jogar", "Sair"]
        esc = opcoes[ui.escolher("", opcoes)]
        try:
            if esc == "Novo jogo":
                jogo = Jogo(ui, seed=args.seed, pasta_saves=args.saves, hardcore=not args.brando)
                jogo.autosalvar = ui.interativo
                ui.jogo = jogo
                jogo.novo_jogo()
                jogo.rodar()
            elif esc == "Carregar jogo":
                nomes = [os.path.splitext(os.path.basename(s))[0] for s in saves]
                i = ui.escolher("Qual jogo?", nomes + ["Voltar"])
                if i < len(saves):
                    jogo = Jogo.carregar(ui, saves[i], args.saves)
                    jogo.autosalvar = ui.interativo
                    ui.jogo = jogo
                    ui.dizer(f"Bem-vindo de volta, {jogo.j.nome}.", "verde")
                    jogo.rodar()
            elif esc == "Como jogar":
                ui.dizer(COMO_JOGAR)
                ui.pausar()
            else:
                ui.dizer("Até a próxima jornada!", "magenta")
                return
        except FimDeJogo:
            pass
        ui.jogo = None


def main():
    parser = argparse.ArgumentParser(description="Crônicas da Fenda — RPG de texto offline")
    parser.add_argument("--seed", type=int, help="semente do mundo (o mesmo número gera o mesmo reino)")
    parser.add_argument("--terminal", action="store_true",
                        help="joga dentro do terminal, com painéis (precisa do textual)")
    parser.add_argument("--classico", action="store_true",
                        help="interface de terminal simples, sem dependências")
    parser.add_argument("--navegador", action="store_true",
                        help="abre no navegador mesmo se o pywebview (janela própria) estiver instalado")
    parser.add_argument("--sem-abrir", dest="abrir", action="store_false",
                        help="não abre o navegador sozinho (só mostra o endereço)")
    parser.add_argument("--porta", type=int, default=0, help="porta local da interface (padrão: qualquer livre)")
    parser.add_argument("--brando", action="store_true",
                        help="modo brando: ao cair em combate você é resgatado (sem morte permanente)")
    parser.add_argument("--hardcore", action="store_true", help=argparse.SUPPRESS)  # já é o padrão
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
