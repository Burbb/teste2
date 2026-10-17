# O custo do recurso na tela (etapa 1B, 1.114.1)

Relato do Jean: ao usar uma habilidade, os efeitos (a vida voltando na Drenar Vida) apareciam antes de a Mana ser
paga, como se conjurar e pagar fossem momentos separados.

## O diagnóstico

**O motor não desconta tarde.** `rpg/combate/heroi.py`, `menu_habilidades`:
- desconta o recurso e as flechas depois de o alvo ser confirmado (na mira, que ainda se cancela, nada é pago);
- desconta antes de abrir a ação (`agindo`).

**O que a tela recebia era tardio.** A ponte web (`rpg/web/ponte.py`) só manda o estado (onde moram o recurso, as
flechas e a vida da HUD e da carta) junto de um texto (`dizer`). O lance `acao` não leva o recurso. Por isso o valor
pago chegava à tela só no primeiro texto da ação:
- **numa habilidade de alvo único**, o texto do golpe vem depois da animação do golpe;
- **numa habilidade em área**, o estado fica segurado até o fim da salva inteira (`iniciar_salva`/`fim_salva`). Uma
  cura ou um roubo de vida dentro da salva aparecia antes do custo.

A sequência das mensagens foi registrada pela ponte de verdade (um canal que só anota) e, na página, quadro a quadro
(`linha_do_tempo.mjs`: os números da HUD e da carta do herói a cada `requestAnimationFrame`, e o começo e o fim de
cada lance e de cada estado). Tempo, em ms, contado do clique que confirma a ação:

| habilidade | começo da ação | antes: custo na tela | depois: custo na tela | o efeito do herói |
|---|---|---|---|---|
| Drenar Vida (Mana, alvo único, cura) | 132 / 190 | 666, depois do golpe | 208, no começo | a cura na carta: 1159 / 1209 |
| Sede de Sangue (Vigor, alvo único, cura) | 110 / 127 | 619, depois do golpe | 138, no começo | a cura: 1259 / 1260 |
| Chuva de Flechas (Foco e 2 flechas, área) | 65 / 67 | 1012, depois da salva inteira | 74, no começo | — |

Na mira e depois de cancelar (Voltar), o recurso fica intacto nas três (`capturas/linha-*.txt` e `.json`).

## A correção (a menor que a causa pede)

Depois do desconto, `self.ui.atualizar()`. A ponte manda o estado com o recurso e as flechas já pagos antes do lance
`acao`, então a HUD e a carta mostram o custo junto do começo da ação. O ataque básico do Arqueiro tem o mesmo fluxo
com a flecha e recebe a mesma linha.

O que não muda:
- custos, contas, sorteios, a ordem das reações e a ordem dos lances (o gabarito sai idêntico);
- nenhum valor é antecipado: o estado é o do motor naquele instante, e nada volta atrás. A mira continua sem pagar;
- os estados seguintes trazem o mesmo valor, e a tela não redesenha o que não mudou.

## A verificação

`tests/test_custo_na_tela.py`, pela ponte de verdade, sem navegador:
- Drenar Vida com a mira cancelada e depois confirmada;
- Chuva de Flechas (Foco e flechas, em área);
- Sede de Sangue (Vigor, com cura);
- o ataque básico do Arqueiro.

Em cada um, confere que:
- na mira o recurso fica intacto;
- o estado logo antes do lance `acao` já traz o custo;
- nenhum estado durante a ação devolve o valor.

Os quatro falham sem a correção. Também rodaram a suíte, o gabarito (sem mudança), o pyflakes e a fumaça (uma vez,
`capturas/fumaca.log`).

    PLAYWRIGHT_MODULO=<caminho>/index.mjs HAB=drenar_vida CLASSE=mago ESPEC=necromante node ferramentas/prototipos/hud/custo-recurso/linha_do_tempo.mjs depois
