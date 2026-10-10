# 13 — Pendências fora da campanha

Divergências entre documentação e código, e um texto do jogo que contradiz o modo escolhido. Encontradas na conferência de 10/10/2026, sobre a versão 1.47.1 (commit `622b1b6`). Cada item foi conferido no código.

**Regra:** estas correções não fazem parte da campanha (E1–E11). Corrigir em tarefa própria, quando Jean pedir, sem misturar com a implementação de região, missão ou história. O item da cronologia não está aqui: é decisão de design, tratada em [12-E1-CAMPANHA.md](12-E1-CAMPANHA.md).

## Texto do jogo

| # | Onde | O que diz | O que acontece | Tipo |
|---|---|---|---|---|
| 1 | `rpg/jogo.py:221` (prólogo) | "A fome mata. Feridas infeccionam. A noite cega. E a morte é permanente." | A frase sai sempre, inclusive com `--brando`, em que cair leva ao resgate (`jogo.py:248`) | Mudança de jogo: pede atualização do gabarito, explicada no commit |

Lido no código; não executado no modo brando.

## README principal

| # | Trecho | Situação no código |
|---|---|---|
| 2 | "Aliados na batalha final: muitas boas ações recrutam ajuda" (linha ~422) e `g.aliado_final` na lista de ferramentas (linha ~520) | Não existe `aliado_final` em `rpg/`. `docs/ROADMAP.md` registra que o sistema saiu na 1.45 |
| 3 | Fontes: "Jacquard 24 nos títulos… Jersey 15 nos números" (linha ~83) | Títulos em Alagard (`--titulo: "Titulo"`, Jacquard só como reserva); números em Alegreya (`--num`); Jersey 15 declarada e não usada (`css/01-base.css`). `docs/ARQUITETURA.md` já está certo |
| 4 | "18 partidas" do gabarito (linhas ~484 e ~494) | `tests/gabarito.json` tem 24 (18 do robô e 6 sequências com a comitiva), como dizem CLAUDE.md e ARQUITETURA |
| 5 | "88 eventos" (linha ~412) | 98 funções registradas em `rpg/eventos/motor.REGISTRO`. Pode ser critério de contagem diferente (encruzilhadas e cenas da comitiva); conferir antes de trocar o número |
| 6 | Estrutura do código: `combate.py` e `comitiva.py` como arquivos (linhas ~461–462) | Viraram os pacotes `rpg/combate/` e `rpg/comitiva/` na Etapa H |

## Documentação técnica

| # | Onde | Situação no código |
|---|---|---|
| 7 | `docs/ARQUITETURA.md:101`: "Itens ainda usam `especial()`…" | Não existe `especial()`. Itens entram como fonte por `itens.fonte_item` (`modificadores.py:86–89`) |
| 8 | `docs/ROADMAP.md`, etapas B e C: "Falta: itens e estados como fontes (hoje `especial()`)" e estados "perguntados à mão em `atacar`" | Estados entram pelo golpe com `estados.no_golpe` (`combate/golpe.py`). O que ainda vale da etapa B: verificações de especialização fora do combate (há 16 comparações `spec ==`/`spec in` fora de `talentos.py` e `classes.py`) |
| 9 | `docs/ROADMAP.md`, "A meta": "centenas de habilidades… especializações de elite… cada partida diferente" | Diverge da direção de `roadmapIDEIAS` (campanha escrita, três classes, sem cota de habilidades). A Etapa I ("mundo e narrativa como dados") se sobrepõe às E2–E4. Combinar qual documento manda no técnico e apontar um para o outro |

## Observações sem correção pedida

- Existe a branch `claude/rpg-texto-offline-classes-apgl62` no GitHub, na versão 1.12.1, com último commit em 07/10/2026. Está bem atrás da branch de trabalho. Não usar como referência.
- O teste da interface Textual é pulado quando `textual` não está instalado (ambiente da nuvem).

## Quando corrigir

Sugestão: uma tarefa curta de documentação para os itens 2 a 9, sem tocar no jogo, e outra para o item 1, que muda o jogo e o gabarito. As duas são independentes da campanha e podem ser feitas antes ou depois da E2.
