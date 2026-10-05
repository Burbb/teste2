"""Ponto de entrada: python -m rpg"""

import argparse
import glob
import os

from .jogo import FimDeJogo, Jogo
from .ui import UI

COMO_JOGAR = """\
COMO JOGAR

• Tudo é escolhido digitando o número da opção e apertando Enter.
• Cada ação (explorar, viajar um trecho, passear) consome um período do dia:
  manhã, tarde, anoitecer e noite. À noite os inimigos são mais fortes.
• Acampe ou durma na taverna para recuperar vida e começar um novo dia.
• Derrote os 3 guardiões para obter os Sigilos e abrir caminho até a Cidadela.
• A corrupção cresce a cada dia (mais rápido enquanto houver guardiões vivos).
  Se chegar a 100%, o jogo acaba.
• No nível 4 sua classe se ramifica em uma de duas especializações.
• Escolhas têm consequências: quem você ajuda (ou rouba) pode voltar mais tarde.
• Se cair em combate, você é resgatado e acorda numa vila, mas perde ouro e
  dois dias (e a corrupção avança). Com --hardcore, a morte é permanente.
• Use "Analisar inimigos" no combate para ver fraquezas e resistências.
• Ouça rumores nas tavernas: eles revelam tesouros, feras e pontos fracos.
"""


def main():
    parser = argparse.ArgumentParser(description="Crônicas da Fenda — RPG de texto offline")
    parser.add_argument("--seed", type=int, help="semente do mundo (o mesmo número gera o mesmo reino)")
    parser.add_argument("--sem-cor", action="store_true", help="desativa as cores do terminal")
    parser.add_argument("--hardcore", action="store_true",
                        help="morte permanente (sem resgate ao cair em combate)")
    parser.add_argument("--rapido", action="store_true", help="sem pausas dramáticas no texto")
    parser.add_argument("--saves", default=os.path.join(os.path.expanduser("~"), ".cronicas_da_fenda"),
                        help="pasta onde os jogos salvos ficam")
    args = parser.parse_args()

    ui = UI(cor=False if args.sem_cor else None, rapido=args.rapido)
    while True:
        ui.titulo("CRÔNICAS DA FENDA", "magenta+negrito")
        ui.dizer("Um RPG de texto onde nenhuma jornada é igual à outra.".center(76), "cinza")
        saves = sorted(glob.glob(os.path.join(args.saves, "*.json")))
        opcoes = ["Novo jogo"] + (["Carregar jogo"] if saves else []) + ["Como jogar", "Sair"]
        esc = opcoes[ui.escolher("", opcoes)]
        try:
            if esc == "Novo jogo":
                jogo = Jogo(ui, seed=args.seed, pasta_saves=args.saves, hardcore=args.hardcore)
                jogo.novo_jogo()
                jogo.rodar()
            elif esc == "Carregar jogo":
                nomes = [os.path.splitext(os.path.basename(s))[0] for s in saves]
                i = ui.escolher("Qual jogo?", nomes + ["Voltar"])
                if i < len(saves):
                    jogo = Jogo.carregar(ui, saves[i], args.saves)
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
        except KeyboardInterrupt:
            ui.dizer("\nAté a próxima jornada!", "magenta")
            return


if __name__ == "__main__":
    main()
