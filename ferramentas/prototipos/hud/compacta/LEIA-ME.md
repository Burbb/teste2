# A composição compacta das lutas cheias (protótipo, em avaliação)

> **Rodada 2** em `rodada2/LEIA-ME.md`: a B aprovada como direção, o custo numa linha própria, o registro
> investigado no motor (`efeitos_reais.py`). Correções a esta rodada: a luta "cinco" (5 lobos) não acontece no jogo
> (uma matilha vai a 4); o necromante chega a 7 aliados; o caso "simulado" de efeitos é o que o motor produz; e a B
> daqui deixava o seletor na tela durante a mira.

Pedido do Jean: nas lutas cheias em 1280×720, a arena, o seletor e a descrição juntos, com todas as habilidades da
classe à vista sem rolar a lista e a descrição legível, sem perder o que a 1.111.0 aprovou (as cartas, os nomes, os
números, os retratos, os recursos, os estados, as faixas). Sem carrossel, sem passo a mais para escolher o alvo; abrir
e fechar menus não mexe nas cartas; os alvos não pulam durante a mira; as lutas pequenas como estão.

**Nada disto entrou no jogo.** As alternativas são trocas de texto aplicadas só na página das fotos (`compacta.mjs`,
pelo `page.route` do Playwright) e duas folhas de estilo (`a-arena.css`, `b-seletor.css`). Cada troca procura o
texto exato do `escolhas.js` e do `batalha.js` e para se ele mudou.

## Os grupos reais (as regras de crescimento conferidas no código)

- **Aliados, no máximo 6:** o herói, a comitiva (`LIMITE = 2` companheiros), os servos do necromante (`servos_max` = 1,
  mais 1 com a Legião de Ossos, mais 1 uma vez com o Rei dos Mortos: 3) ou o animal do patrulheiro (só ele). Seis é o
  necromante com comitiva cheia e três servos.
- **Inimigos, no máximo 6:** o bando vai até `hi + 1` e ganha uma escolta (o xamã dos caídos à noite). Um guardião que
  invoca só chama enquanto há menos de 4 vivos, e quem foi invocado e cai sai da arena (1.111.0).
- As lutas das fotos (`tests/navegador/cenarios.py`, as mesmas da produção e das duas alternativas):
  **poucos** (paladino, Morel, um rato e dois lobos de dia), **cinco** (patrulheiro com o lobo, Morel e Odette contra 5
  lobos ao anoitecer), **maior** (necromante, Morel, Odette e 3 esqueletos contra 5 caídos e o xamã à noite, a bolsa com
  5 itens) e **longos** (berserker contra o nome mais longo que o jogo gera e três reforços invocados).

## As duas alternativas

- **A, arena compacta:** a partir de 5 cartas num lado, a arena fica compacta (o espaço entre cartas menor; os efeitos
  na linha do nome em vez da linha própria); se as duas colunas do seletor ainda não couberem embaixo, a lista abre em
  três colunas, com a descrição embaixo de todas.
- **B, seletor na ficha:** a arena e as cartas como estão. Quando o seletor não cabe inteiro embaixo da arena (a lista
  toda, mais 60 px de descrição, a mínima que o seletor já aceita), ele abre sobre a coluna da ficha do herói, à
  esquerda, numa coluna só, com a descrição sempre embaixo da lista. Onde cabe (as lutas pequenas, as janelas maiores),
  abre embaixo como hoje. A escolha é do herói (o que ele sabe e o que carrega), e a ficha é dele.

## As medidas (`capturas/relatorio.json`)

Faixas inteiras à vista no seletor; a altura da descrição; o espaço que sobra ao registro com a luta parada.

| luta, janela | produção | A | B |
|---|---|---|---|
| cinco, 1280×720, Habilidades | 2 de 7, a lista rola; descrição 60 px rolando; registro 123 | 7 de 7 em três colunas; 78 px; registro 288 | 7 de 7 na ficha; 150 px (rola o fim); registro 123 |
| maior, 1280×720, Habilidades | 2 de 7, rola; 60 px rolando; registro 164 | 5 de 7 em três colunas, ainda rola; 60 px; registro 202 | 7 de 7 na ficha; 160 px; registro 164 |
| maior, 1280×720, Itens | 2 de 5 | 5 de 5 (49 px de descrição) | 5 de 5 (105 px) |
| cinco e maior, 1500×950 e 1920×1080 | 7 de 7 embaixo | 7 de 7 embaixo | 7 de 7 embaixo (igual à produção) |
| poucos e longos, todas | 7 de 7 embaixo | 7 de 7 embaixo | 7 de 7 embaixo (igual à produção) |
| SIMULADO: 3 ou 4 efeitos em cada um, 1280×720 | cinco 0 de 7, maior 0 de 7; registro 33 e 0 | cinco 7 de 7, maior 5 de 7; **nomes cortados em todas as cartas** (um "Lobo" com 0 px) | 7 de 7 na ficha nas quatro lutas; nomes inteiros; registro como na produção (33 e 0) |
| SIMULADO, 1500×950 | cinco 6 de 7, maior 4 de 7 | 7 de 7; nomes cortados | 7 de 7 na ficha (179 e 143 px de descrição) |

Em todas as 36 combinações de luta × janela × versão: abrir, alternar e fechar os menus não mexe em nenhuma carta; o
seletor e a mira não cobrem carta; a saída e a entrada SIMULADAS de um inimigo durante a mira não mexem nas outras
cartas; o Voltar devolve a roda. No teclado (a luta maior em 1280×720, com movimento reduzido), nas três versões: a
tecla 2 abre o seletor com o foco na primeira habilidade, as setas chegam à sétima inteira à vista e com o foco
visível, sem animação, e o Esc fecha devolvendo o foco a Habilidades. Sem erro no console.

## Os compromissos

- **A** ganha espaço no lugar certo (a arena encolhe 474→309 px nos 5 lobos e o registro cresce), mas não resolve a
  luta maior (5 de 7, ainda rola) e, com os efeitos na linha do nome, corta os nomes assim que há 3 ou 4 efeitos: viola
  "preservar os nomes". Os efeitos na linha do nome só funcionam com nomes curtos e poucos efeitos; ficam descartados
  como regra geral.
- **B** mostra todas as habilidades e todos os itens em todos os casos reais e simulados, com a descrição mais alta
  que a de hoje, sem mexer na arena (nada pula, nada encolhe). Custa: **enquanto aberto, cobre a ficha do herói** (os
  atributos e o equipamento, que não mudam durante a escolha; a carta do herói na arena continua com a vida, o recurso
  e os efeitos); a coluna é estreita (~250 px), então os nomes de habilidade quebram em duas linhas e, com custo de dois
  recursos (o patrulheiro: foco e flechas), "Chuva de Flechas" e "Fúria da Natureza" quebram em três; a descrição longa
  dos 5 lobos rola no fim. Os vãos da faixa na coluna da ficha apertam (9→5 px, a margem direita 16→8) para isso; a
  letra, o ícone e a tecla são os do seletor.
- **Nas duas**, o registro numa luta com muitos efeitos em 1280×720 continua curto (0 a 33 px no caso simulado
  extremo): o que cresce é a arena, e nenhuma das duas mexe nela de propósito (B) ou o bastante (A).
- Como na produção, a área da descrição fica reservada e vazia até o mouse ou o foco examinar uma habilidade.

**Recomendação:** B, com o gatilho como está (só quando a lista inteira não cabe embaixo). Ela resolve o pedido nos
casos reais sem tocar no que foi aprovado na arena, e nas lutas pequenas e janelas maiores é idêntica à produção. O
que fica para decidir com o Jean jogando: se cobrir a ficha enquanto o seletor está aberto incomoda; se as três linhas
de nome do patrulheiro pedem o custo embaixo do nome nessa coluna. O registro curto com muitos efeitos em 1280×720 é
outro problema (a altura da arena) e pede uma entrega própria, se aparecer jogando.

## Como reproduzir e o tempo da bateria

```
node ferramentas/prototipos/hud/compacta/fotografar.mjs        (PLAYWRIGHT_MODULO no ambiente)
python ferramentas/prototipos/hud/compacta/comparar.py
```

Filtros: `VERSOES=producao,a,b`, `JANELAS=baixa,normal,grande`, `LUTAS=poucos,cinco,maior,longos`; `MANTER=1` não
apaga as fotos e grava `relatorio-parcial.json`.

Cada cenário (uma luta × uma janela × uma versão) leva 15 a 21 s: subir o cenário e gerar o mundo; uma rodada de
ataque (o turno real dos inimigos, para haver registro e efeitos); Habilidades aberto e o mouse em cada habilidade
para achar a descrição mais longa e a mais curta; Itens; fechar; a mira, a saída e a entrada simuladas; os efeitos
simulados e Habilidades de novo; 7 fotos e as medidas. As esperas: 0,6 s depois de abrir um menu (a entrada das faixas,
150 ms mais 18 ms por faixa, e a medida da descrição), 0,7 s depois do ataque (o golpe sair antes de esperar a vez
do herói de novo) e 0,8 s com o mouse fora (o destaque sair e as cartas assentarem antes da foto), 0,12 a 0,3 s por habilidade examinada (a troca da descrição). Não foram mexidas.

- **A bateria inteira:** 4 lutas × 3 janelas × 3 versões = 36 cenários, mais o teclado nas 3 versões: 39 cenários,
  ~12 min (`capturas/logs/bateria.log`).
- **As refeitas:** A e B depois do ajuste do gatilho, 26 cenários em 7 min 12 s (`bateria-ab.log`); B depois dos
  acertos na coluna da ficha, 13 cenários em 3 min 36 s (`bateria-b.log`). A produção não mudou e não foi refeita.
- As ~250 fotos soltas não são versionadas (`capturas/.gitignore`): versionadas só 19 comparações representativas em
  tamanho real (`capturas/comparacoes/`, as três versões lado a lado com os mesmos dados), o relatório e os logs.
  1280×720: todas as lutas com Habilidades, Itens e os efeitos simulados, e a mira da luta maior; 1500×950: cinco e
  maior, Habilidades e efeitos; 1920×1080: a maior; o teclado.

## Simulado (não acontece assim no jogo)

- os 3 ou 4 efeitos em cada combatente (o estado da luta alterado só na tela);
- a saída e a entrada de um inimigo durante a mira (para ver se as outras cartas pulam);
- o nome mais longo (`LONGOS=1`, um único com nome inventado ao limite) e os servos já de pé no começo (`SERVOS=3`).
