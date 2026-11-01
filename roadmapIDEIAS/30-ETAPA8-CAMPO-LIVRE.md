# 30 — Etapa 8: o combate em campo livre (herói em tempo real e tropas pequenas)

**31/10/2026 (rodada 1) e 01/11/2026 (rodadas 2 a 4).** A rodada 4 (Campo Livre 4: o ataque básico assistido, o
impacto dos acertos, o Capitão perigoso, os arqueiros e as ordens, a horda e as intenções de progressão) vem primeiro;
depois a rodada 3 (Campo Livre 3: a câmera parada no modo de
comando, o Capitão que enfrenta o herói, as escalas 1×, 2× e 4× e duas habilidades novas por herói); depois
a rodada 2 (Campo Livre 2: números de dano, o líder inimigo, o modo de comando e a seleção, a leitura do choque, três
encontros e quatro versões de habilidade); por fim as seções 0 a 14, a rodada 1 (Campo Livre 1). **A direção foi
aprovada pelo Jean para continuar no protótipo, sem integração.**

## Rodada 4 (01/11/2026): Campo Livre 4

**O pedido do Jean** (depois de jogar a v3, que ele aprovou como direção: "batalhas maiores ficaram mais divertidas"):
preservar o protagonista poderoso varrendo tropas e melhorar quatro pontos, nesta ordem: o ataque básico (prazeroso e
assistido, útil mesmo com o recurso cheio), o impacto dos acertos (sincronizado, a direção e o peso do golpe no herói,
reação visual separada da interrupção), o Capitão (forte, rápido, perigoso para o herói e para o campo, com preparação
legível e janelas de resposta) e a utilidade das tropas e ordens (arqueiros que participam, ordens distintas, atacar um
alvo). Durante a rodada, acrescentou: **um modo com muito mais tropa, ou poder acrescentar quantidades maiores para
testar, pela sensação de destruir várias tropas, "pique Dynasty Warriors, só que de cima"**. Também pediu para registrar
intenções de progressão (R4.7), sem implementar campanha. Vídeos só sob pedido (nenhum nesta rodada).

**Em teste nesta rodada (nada aprovado ainda).** A v1 continua em `/v1/`; a v2 está em `31ea8778` e a v3 em `298dc4bc`.

| Seção | O que tem |
|---|---|
| R4.1 | O ataque básico assistido |
| R4.2 | O impacto: sincronia, reação e interrupção, o golpe no herói |
| R4.3 | O Capitão: o que travava e o que mudou |
| R4.4 | Os arqueiros e as alas |
| R4.5 | As ordens |
| R4.6 | A horda (o pedido do meio da rodada) |
| R4.7 | Progressão: intenções registradas (não implementado) |
| R4.8 | Verificação: o que foi conferido agora e o que foi reaproveitado |
| R4.9 | Limitações conhecidas e o que precisa da avaliação do Jean |

### R4.1. O ataque básico assistido

**A assistência** (`alvoAssistido` em `sim.js`, a mesma função que desenha a marca): o alvo é o inimigo vivo mais perto
da direção do mouse, dentro do alcance, num cone (Faísca: 15° para cada lado, até 175 px; Corte: 40°, até 36 px); entre
dois quase na mesma direção, o mais perto. Sem ninguém no cone, o golpe sai para onde o mouse aponta. **A tela marca o
alvo** com dois cantos claros no pé (só fora do modo de comando).

- **Faísca:** sai para o alvo e o persegue, virando no máximo 14 rad/s (anda até 30 px a mais pela curva). **Se o alvo
  cai no caminho, ela segue reta no último rumo e só acerta quem tocar até o fim do alcance; nunca procura outro alvo**
  (que poderia estar longe, fora do que o jogador apontou).
- **Corte:** vira para o alvo; se ele está além de 70% do arco, o herói dá **um passo de até 12 px na preparação
  (0,07 s)**, parando antes de encostar. **Nunca** para trás (o alvo está no cone do mouse), nunca contra a direção em que
  o jogador anda (o passo some se as teclas apontam para o outro lado), nunca através de quem está no meio (o golpe vai
  nesse, sem passo). No máximo 12 px a cada 0,27 s (≈ 44 px/s, menos que andar, 72): não vira transporte. O passo
  termina no contato (sem deslizar além). Segurar o botão continua repetindo.
- **A função de cada um**, poucas e coerentes: **o Corte** ficou um combo de 3, 4 e o arremate de 9 (era 3, 3, 8) num
  arco um pouco mais largo (120°; o arremate, 160° e 28 px), o que derruba um pequeno grupo de soldados no terceiro
  golpe; **a Faísca** deixa uma **Fagulha** por 3 s (um pontinho laranja no alvo): o próximo golpe de habilidade do Mago
  nele (Bola, Corrente, Piscar, Gelo ao surgir) causa +6 e a consome. É o motivo para atirar mesmo com a Mana cheia:
  faíscas antes de uma Bola num veterano (32 de vida) o derrubam (4 + 13 + 6 + o fogo). O recurso continua subindo
  como antes (a Fúria por acerto), agora como recompensa a mais.

### R4.2. O impacto: sincronia, reação e interrupção, o golpe no herói

**A sincronia, conferida:** no mesmo passo em que um golpe acerta (o contato da arma, a chegada do projétil, o pouso),
saem juntos o dano na vida, o evento do número (o mesmo valor que saiu da vida), o clarão no alvo, a faísca do acerto e
o som; a barra de vida e o número aparecem no quadro seguinte. Nenhum caminho novo desta rodada mudou isso (os testes
de "número = vida que saiu" continuam, e há um novo para o herói).

**Reação visual separada da interrupção mecânica:**
- **Tranco:** todo acerto em herói e em ameaça (o Capitão, o campeão, o porta-estandarte) dá um tranco de 1 px (fraco)
  ou 2 px (forte) na direção do golpe, por 0,08 a 0,12 s, **só no desenho**: o Capitão reage a uma faísca sem parar.
- **Firme:** uma ameaça que tem uma preparação interrompida fica **firme** por 2,5 s (o campeão, 2 s): nesse tempo o
  golpe forte só a faz reagir ("firme" escrito sobre ela, o anel do Capitão fica claro e a barra dele diz "Firme"). Nada
  de cadeia de interrupções. Medido: com uma Bola de Fogo a cada recarga por 10 s, o Capitão fica atordoado menos de 20%
  do tempo (teste).
- **Os soldados** continuam recuando, estremecendo, caindo e sendo arremessados como antes.

**O golpe no herói** (direção e peso, sem mais tremor): uma **marca vermelha no anel do herói, do lado de quem bateu**
(mais longa e grossa quanto mais pesou, some em 0,35 a 0,65 s); o **número vermelho** do dano que ele levou, nos golpes
de 6 ou mais (o valor que saiu da vida); nos golpes de 15 ou mais, a **borda da tela do lado do golpe fica vermelha** por
um instante (some em 0,3 s) e toca o choque. O tremor e os controles dele não mudaram, e o modo de comando continua
estável (R4.8).

### R4.3. O Capitão: o que travava e o que mudou

**A investigação, antes de mexer** (v3, `ferramentas/lider.mjs` com o tempo por estado, jogador automático médio):

| v3 | Vivo | A menos de 40 px do herói | Onde o tempo foi |
|---|---|---|---|
| contra o Guerreiro | 48 s | 42 s | **parado 23 s** (ao lado do herói, esperando a recarga de 2,4 s do machado), machado 10 s, atordoado 4 s, andando 6 s |
| contra o Mago | 40 s | 2 s | andando 15 s, **cravado/ofegante 8 s**, reunir e carga 7 s, arremetida e no ar 6 s, machado 1 s |

Ou seja: perto do Guerreiro ele esperava mais do que batia; longe do Mago passava o tempo andando e se recuperando; e o
dano era baixo (26 no machado, 20 na Arremetida). Contra as tropas, mirava o herói 92 a 97% do tempo (o foco da v3), o
que deixava o campo livre para elas.

**O que mudou** (números em `conteudo.js`, regras em `sim.js`, `decidirLider`):
- **A escolha (foco revisto):** duela com o herói quando ele está a até 150 px ou o feriu nos últimos 4 s (o herói
  chegando perto passa à frente da escolha, como uma provocação); senão, vai no **grupo nosso mais denso a até 170 px**
  (4 ou mais a 40 px uns dos outros; **arqueiro vale 1,5**); senão, persegue o herói a até 320 px; senão, a tropa mais
  perto. Cada escolha dura pelo menos 3 s (1 s quando não há grupo para atacar). A barra diz "Atrás de você" ou "Nas
  suas tropas", e a faixa avisa quando muda.
- **Mais rápido e mais forte:** andar 40 → 54 (o herói anda 68 a 72: alcançar exige as habilidades); machado 30 no
  herói (era 26), arco de 160° e 36 px, **recarga 1,6 s** (era 2,4), anunciado 0,8 s.
- **Rodopio (novo):** quando 3 ou mais dos nossos estão colados nele (o herói conta 2), um círculo de 46 px anunciado
  0,75 s: 34 no herói, 14 nas tropas. Abre caminho e pune quem se amontoa em volta dele, também enquanto persegue.
- **Arremetida** mais longa (até 220 px, recarga 6 s, 0,7 s anunciada, 30 no herói) e **também no meio de um grupo**
  das nossas tropas (os arqueiros recuam do machado, não de um salto). Ao cair, 0,5 s cravado (+50%) e **o machado
  seguinte se anuncia em 0,6 s** (o golpe de sequência).
- **Carga** a cada 8 s (30 no herói, 16 nas tropas), ofegante 0,9 s depois (era 1,2).
- **Nas tropas:** 14 por golpe: dois derrubam um soldado nosso, um derruba um arqueiro. Vida 480 → 500.
- **Mantido:** a preparação de tudo anunciada no chão (nada corrige a direção depois de marcado; a Arremetida mira o
  caminho do herói no começo e fica), golpe fraco não o faz cambalear, golpe forte interrompe (com a janela firme
  depois), os soldados dele abrem caminho, o machado através da tropa no caminho do herói.

| v4, três sementes | Resultado | Capitão vivo | A < 40 px | Parado | Machado (no herói) | Rodopio | Arremetida (no herói) | Dano no herói | Dano nas tropas |
|---|---|---|---|---|---|---|---|---|---|
| Guerreiro, jogador forte | 3 vitórias, vida 140 a 205 | 43 a 55 s | 30 a 36 s | 15 a 20 s | 13 a 14 (0 a 1) | 4 a 5 | 2 a 3 (1 a 2) | 30 a 94 | 450 a 520 |
| Mago, jogador forte | 3 vitórias, vida 80 a 140 | 36 a 40 s | 3 a 5 s | 1 a 3 s | 1 a 2 (0) | 2 | 5 a 6 (1 a 3) | 30 a 90 | 340 a 410 |
| Guerreiro, jogador médio | **2 derrotas**, 1 vitória (vida 23) | 31 a 55 s | 23 a 46 s | — | 9 a 19 (4) | 2 a 3 (1 a 2) | 1 a 3 (1 a 2) | 218 a 248 | 310 a 340 |
| Mago, jogador médio | 3 vitórias, vida 110 a 170 | 36 a 48 s | 0,5 a 11 s | — | 1 a 6 (0) | 1 | 5 a 6 (0 a 1) | 0 a 30 | 240 a 340 |

O jogador médio vê os avisos com 0,35 s de atraso e não recua; contra ele, o Capitão vence o Guerreiro. Isso é de
propósito (o pedido: um adversário capaz de enfrentar o protagonista), mas é o primeiro ponto para o Jean avaliar
(R4.9). O jogador automático agora desvia quando está dentro do arco desenhado (antes, só a 34 px do centro, menos que
o alcance novo).

### R4.4. Os arqueiros e as alas

**A investigação:** medindo "arqueiro sem alvo e parado" (o tempo entre um tiro e outro não conta), só a **retaguarda
do Capitão** ficava parada: 42% do tempo em 1× e **71% em 4×** na v3 (ela só mirava quem estivesse a até 180 px do posto,
e a frente luta a 200 a 270 px dele). Os outros arqueiros tinham alvo, mas duas regras os seguravam: os inimigos
"voltavam para trás da linha" quando o alvo estava longe (em 4×, as alas de fora iam para o meio e esperavam), e os
nossos, acompanhando o herói, só miravam a até 75 px deles mesmos.

**O que mudou:** o arqueiro **avança até a distância de tiro** (90% do alcance, na linha do alvo) **sem passar dela e
sem sair da coleira** (a da ordem, ou o posto); procura alvo até 420 px quando nada o prende; recua de quem chega perto
(também dentro da coleira; encurralado na beira dela, fica e atira). A retaguarda pode **sair até 90 px do posto** para
alcançar a frente e, com o Capitão derrubado, deixa o posto. Em 4×, as alas de fora começam com **Atacar** (lutam na
frente delas) em vez de Defender (que as deixava paradas esperando).

| Sem alvo e parados (5 a 40 s, jogador médio) | v3, retaguarda | v4, retaguarda | Tiros por arqueiro × minuto (retaguarda) |
|---|---|---|---|
| O Capitão, 1× | 42% | 25% | 14 → 18 |
| O Capitão, 4× | 71% | 40% | 11 → 16 |

Nos outros encontros e nas nossas tropas, 0 a 2% nas duas versões. A retaguarda ainda espera quando a luta está a mais
de 240 px do posto: é a função dela (proteger o fundo), agora sem ficar fora da batalha inteira.

### R4.5. As ordens

**Antes de acrescentar ordens, as três ficaram distintas** (cada uma com uma âncora e uma coleira; `ORDENS` em
`conteudo.js`, `ancoraDe` e `alvoValido` em `sim.js`):

| Ordem | Âncora | Quem luta perto | Quem atira | Para quê |
|---|---|---|---|---|
| **1 Acompanhar** (o padrão) | o herói | luta com quem está a até 90 px do herói | fica 30 px atrás do herói (do lado oposto aos inimigos) e atira em quem alcança de lá (até 50 px dela + o alcance) | avançar junto, arqueiros atrás da infantaria |
| **2 Atacar** | nenhuma | vai aos inimigos mais perto | avança até a distância de tiro do alvo | a luta livre, a linha inteira |
| **3 Defender aqui** | o ponto | luta com quem chega a até 70 px do ponto | fica 30 px atrás do ponto e atira em quem alcança dali | segurar uma ala, preservar uma posição |
| **Atacar um alvo** (novo) | o alvo | vai nele; trancado por um inimigo colado no caminho, luta com esse; com o alvo cheio (vagas), luta com quem está a 30 px dele | atira só nele, avançando até o alcance | concentrar fogo no porta-estandarte, no Capitão, num veterano |

- **Ir sem parar:** uma ordem cuja âncora está longe (mais que a coleira + 30 px) faz a tropa ir até lá **sem parar para
  lutar** até chegar perto (60% da coleira). É como tirar um grupo do caminho de uma ameaça.
- **Atacar um alvo** (no modo de comando, com Shift ou pausado): **botão direito num inimigo** (no vazio continua sendo
  "Defender ali") ou **2 com o mouse num inimigo**. Vale para a seleção (sem seleção, para todos). Na tela: uma **mira
  vermelha** em volta do alvo, e no placar "Alvo: porta-estandarte 12". **Quando acaba:** o alvo derrubado ou fugido, ou
  mais de 280 px longe de onde a ordem foi dada por 2 s, encerra a ordem para o grupo todo, e **cada um volta à ordem que
  tinha**; a faixa diz o motivo.
- **As tropas sabem ler o chão:** dentro de uma área anunciada pelo Capitão ou pelo campeão (o arco, o círculo, a
  faixa) há 0,3 s ou mais, saem dela, deixando o que faziam (mais devagar que o herói: nem todas escapam). Sem isso, o
  Capitão matava quase todo o exército que acompanhava o herói no duelo.
- **Preservado:** F1/F2 por tipo, F4 todos (F3 continua sem tipo), o arrasto, a câmera parada com Shift, as ordens só
  para os selecionados, o controle direto do herói.

**As consequências, medidas** (`ferramentas/ordens.mjs`: a mesma batalha e o mesmo jogador automático forte, só as
ordens mudam; um roteiro dá as ordens como uma pessoa daria). Na primeira batalha o herói faz quase tudo e as ordens mudam
pouco (0 a 7 perdas em qualquer caso). No Capitão, elas decidem:

| O Capitão, jogador forte | Guerreiro: resultado · perdas de 42 · arqueiros vivos | Mago: resultado · perdas · arqueiros vivos |
|---|---|---|
| Sem ordens (acompanham) | derrota (o herói caiu aos 51 s) · 39 · 3 | vitória · 26 · 7 |
| Atacar aos 6 s (o padrão do jogador automático) | vitória · 30 · 12 | vitória · 20 · 10 |
| Os arqueiros no Capitão | vitória · 38 · 4 | vitória · 21 · 12 |
| Quem está perto dele recua quando ele chega | vitória · 31 · 8 | vitória · 40 · 2 |
| O exército segura um ponto a 250 px dele enquanto ele duela com o herói | derrota · 34 · 8 | **vitória · 1 · 12** |

Leitura: **mandar as tropas para longe do duelo salva o exército** quando o herói segura o Capitão (o Mago: 1 perda);
com o Guerreiro automático, que larga o Capitão para ir aos grupos, a mesma ordem coloca o ponto no meio do exército
inimigo e piora. **Não há ordem mágica; há consequências**, a favor e contra, e depender delas não é obrigatório (Atacar
sozinho já vence). Os números variam bastante de uma estratégia para outra porque a batalha é caótica (uma semente):
comparam consequências, não medem a dificuldade para uma pessoa.

**O que as tropas fazem além de derrubar** continua no fim da batalha (inimigos ocupados, dano que seguraram, flechas,
e agora "flechas barradas" e o dano do Capitão nelas). **Mudança honesta:** com o herói parado e as tropas sozinhas, na
primeira batalha elas derrubam 4 ou 5 (eram 11 na v3), porque os arqueiros inimigos agora avançam e atiram e o Acompanhar
segura os soldados perto do herói; com Atacar elas aguentam mais (47 s contra 38) e ocupam quase o dobro.

### R4.6. A horda (o pedido do meio da rodada)

- **A tecla H** (em qualquer encontro, também pausado): uma **horda de inimigos comuns** (um veterano a cada dez) entra
  em bloco **na direção do mouse**, a 220 px do herói (ou na borda), já lutando. A quantidade fica nas opções ("Horda (H)",
  de 20 a 200, começa em 60). Os inimigos chamados entram na contagem da vitória.
- **O encontro "A horda":** o herói e as tropas no meio do campo; a cada 9 s, por 100 s, uma onda de 60 (× a escala:
  120 em 2×, 240 em 4×) chega por um lado (oeste, norte, leste, sul). Enquanto vêm ondas, ninguém foge. É o modo "muita
  gente frágil para derrubar de uma vez".
- **Limite:** no máximo **1200 combatentes** no campo (a tecla avisa quando o campo está cheio). Medido no navegador
  (Chromium sem janela, desenho na CPU, o computador do Jean):

| Situação | Combatentes | Qps | Quadro p95 / máx. | Simulação média / p95 | Desenho média / p95 |
|---|---|---|---|---|---|
| Horda 4× + 3 × H, 1920×945 | 661 | 59,7 | 16,7 / 33 ms | 2,1 / 5,2 ms | 2,8 / 4,8 ms |
| Horda 4× + 3 × H, 1280×720 | 660 | 59,4 | 16,8 / 50 ms | 2,4 / 5,1 ms | 2,5 / 4,9 ms |
| Horda 4× + 12 × H de 200 (antes do limite) | 1406 | 53 | 33 / 67 ms | 5,1 / 14 ms | 4,9 / 7,8 ms |

  Por isso o limite ficou em 1200 (não medido exatamente nesse ponto; entre os dois acima).
- **A sensação:** o Guerreiro automático derruba 580 a 620 na horda em 1× e cerca de 2500 em 4×, com até 86 (1×) e 159
  (4×) num golpe só (o Salto Esmagador); em 20 s de horda 4× no navegador, 412 a 566. O Mago automático pode perder (é de
  sobrevivência). Captura: `capturas/cl4-horda-4x-1920.png`.

### R4.7. Progressão: intenções registradas (não implementado)

Pedido do Jean para orientar o design futuro, sem implementar campanha, recrutamento, economia nem heróis novos, e sem
fixar uma curva antes de estudar a campanha:

- **Batalhas massivas são parte importante da experiência.**
- **O começo já deve permitir atingir vários soldados com habilidades** (o herói nasce capaz de golpes em área).
- **A progressão pode aumentar** a quantidade, a diversidade, a resistência de algumas tropas e a presença de heróis
  aliados e inimigos.
- **Soldados frágeis continuam existindo nas batalhas avançadas** (a sensação de varrer gente não some com o progresso).
- **Veteranos, elites e heróis** são quem oferece resistência e confronto mais prolongado.
- **Nem toda batalha precisa ser maior que a anterior:** confrontos menores e intensos também têm lugar.

### R4.8. Verificação: o que foi conferido agora e o que foi reaproveitado

**Conferido nesta rodada:**
- **37 testes da simulação** (`node --test testes/sim.test.mjs`): os 27 da v3 (sete ajustados à mudança de regra, cada
  um explicado no próprio teste: a horda fora do laço "todo encontro é vencido" (ela é de sobrevivência), a escolha do Capitão no lugar do foco, as alas de fora atacando em 4×, o grupo nosso
  entrando na lista antes da escolha do Capitão, os grupos espalhados vencíveis só pelas tropas perdendo mais de um terço,
  o Capitão vencido pelo jogador forte, as tropas sozinhas conferidas com Atacar) e mais 10: a assistência (o da frente e
  não o do lado; nada fora do cone; a Faísca persegue; o alvo cai e ela não troca de alvo), o Corte (o passo de até
  12 px; nenhum passo andando para trás, através de quem está no meio, ou para trás do herói; o combo 3, 4, 9), a
  Fagulha (+6 uma vez), o golpe no herói (o valor = a vida que saiu, a direção, o tranco), o Capitão firme (a segunda
  interrupção na janela não acontece; depois dela, volta; uma chuva de Bolas o deixa atordoado menos de 20% do tempo),
  o Capitão nas tropas (escolhe os arqueiros longe do herói e derruba ao menos metade), os arqueiros dos dois lados
  atirando (85% ou mais dos que existiram 15 s, em 1×, 2× e 4×; a retaguarda dentro do posto), as ordens (arqueiros atrás
  da infantaria no Acompanhar; Defender longe vai sem parar e segura), atacar um alvo (só nele; derrubado, voltam à ordem
  de antes; longe por 2 s, encerra) e a horda (dentro do campo, na contagem, o limite, as ondas no tempo).
- **No navegador** (`ferramentas/conferir4.mjs` e `conferir3.mjs camera`): a ordem de atacar um alvo com teclado e mouse
  de verdade (pausado, F2, botão direito num veterano: os 12 arqueiros nele, os soldados não, o placar "Alvo: veterano
  12"; derrubado, todos de volta a Acompanhar na hora); o golpe do Capitão no herói (30 de dano, o número 30, a borda
  direita, a marca no anel do lado dele); a horda nas duas janelas e perto do limite; **a câmera e o modo de comando de
  novo, sem regressão** (os mesmos números da R3.1: 0,05 px com Shift, 0 px no arrasto, a seleção igual ao retângulo, 0
  golpes, maior passo de 7 px ao sair). Sem erros no console.
- **Batalhas sem tela:** `lider.mjs` (forte e médio, 1×), `ordens.mjs` (as cinco estratégias), as comparações com a v3
  (contribuição das tropas, arqueiros parados) e a horda em 1× e 4×.
- **O jogo não mudou** (`rpg/` e `tests/` intocados): suíte, gabarito e pyflakes rodados de novo nesta rodada; a fumaça,
  reaproveitada.

**Reaproveitado:** o custo do 4× nos encontros normais (R3.3; a horda mediu mais que isso), a resposta comparada com a v1
(o laço não mudou), as capturas da escolha e das habilidades da v3. **Sem vídeos.**

**Capturas** (`capturas/cl4-*.png`): `cl4-alvo-ordem-1920` (a ordem dada, a mira vermelha, o placar),
`cl4-golpe-no-heroi-1920` (o golpe do Capitão: a marca, o número, a borda) e `cl4-horda-4x-1920`.

### R4.9. Limitações conhecidas e o que precisa da avaliação do Jean

- **O Capitão vence o jogador automático médio com o Guerreiro** (2 de 3) e destrói tropas que ficam em volta do duelo
  (240 a 520 de dano nelas por batalha). É o pedido, mas o ponto de equilíbrio para uma pessoa só se descobre jogando.
  Os números a mexer: `danoHeroi` (30), `recarga` do machado (1,6 s), `rodopio`, `foco.grupo`.
- **As tropas derrubam menos que na v3** nos encontros comuns (o herói assistido derruba mais rápido, os arqueiros
  inimigos agora atiram, o Capitão caça tropas). As ordens mudam o resultado, mas só no Capitão de forma clara.
- **A retaguarda do Capitão ainda espera** quando a luta está longe do posto (40% do tempo em 4×).
- **A horda acima de ~700 combatentes** perde fluidez (1400: 53 qps, quadros de 33 ms); o limite está em 1200.
- **A Fagulha e o passo do Corte** não foram medidos por uma pessoa: o passo pode parecer "puxar" o herói; o cone de 40°
  é o número a mexer (`assist.cone`).
- **O porta-estandarte, atrás da linha, quase nunca está na tela** quando o herói está na frente: a ordem de atacar um
  alvo exige vê-lo (rolar a câmera não existe neste protótipo).
- **Para o Jean avaliar:** (1) o básico ficou prazeroso? a marca do alvo ajuda ou atrapalha? o passo do Corte parece
  natural? (2) dá para sentir cada acerto, e saber de onde veio e quanto pesou o golpe no herói? (3) o Capitão está forte
  na medida, com janelas para responder? ele te alcança e ameaça o campo? (4) as ordens (principalmente atacar um alvo e
  Defender longe) fazem diferença perceptível? (5) a horda e a tecla H dão a sensação de destruir exércitos?

## Rodada 3 (01/11/2026): Campo Livre 3

**O pedido do Jean** (depois de jogar a v2): a câmera não pode andar com o mouse enquanto ele comanda com Shift; o
Capitão tem de enfrentar o herói de verdade (inclusive o Mago que mantém distância), com preparação legível e chance de
esquiva, sem perseguição perfeita, teletransporte sem aviso, controle permanente nem imunidade; escalas de exército para
teste (1×, 2× e 4×, este experimental), com as quantidades à vista antes da luta; duas habilidades alternativas por
herói, com funções novas, sem aumentar a barra. Preservar o que ele gostou (resposta, tropas miúdas, herói muito mais
forte, golpes amplos, explosões, arremessos, números, tremor máximo, seleção, campo simples). **Vídeos só quando ele
pedir**; capturas pontuais; nada de repetir baterias sem mudança.

**Em teste nesta rodada (nada aprovado ainda).** A v1 continua em `/v1/`; a v2 está no commit `31ea8778`.

| Seção | O que tem |
|---|---|
| R3.1 | A câmera no modo de comando |
| R3.2 | O Capitão: o que estava errado e o repertório novo |
| R3.3 | As escalas do exército |
| R3.4 | As habilidades novas |
| R3.5 | Verificação: o que foi conferido agora e o que foi reaproveitado |
| R3.6 | Limitações conhecidas e o que precisa da avaliação do Jean |

### R3.1. A câmera no modo de comando

- **A causa:** a câmera segue o herói olhando até 110 px para o lado do mouse; com Shift, mover o mouse para arrastar
  também mexia esse olhar, e o retângulo (desenhado na tela) passava a cobrir outro pedaço do campo durante o arrasto.
- **Agora:** com Shift segurado (ou pausado), **o olhar para o lado do mouse fica parado** onde estava; a câmera
  continua acompanhando o herói se ele andar (WASD). **Durante o arrasto a câmera não se mexe de jeito nenhum**: o
  retângulo mostrado é exatamente a região selecionada. **O tremor se acalma** no modo de comando (vai a zero em ~0,1 s;
  a intensidade escolhida nas opções não muda, e o tremor volta em ~0,3 s ao sair). Ao soltar o Shift (ou despausar), o
  olhar **volta para o mouse em ~0,5 s**, suavizado, em vez de pular.
- **Ataques:** no modo de comando o botão esquerdo nunca ataca (já era assim); o golpe que já tinha começado (uma
  Varredura) termina normalmente, e nada novo sai até o próximo clique fora do comando.
- **Medido** (`ferramentas/conferir3.mjs camera`, teclado e mouse de verdade, tremor 150% com trauma no máximo o tempo
  todo, 1280×720):

| Situação | Resultado |
|---|---|
| Sem Shift, o mouse atravessa a tela | a câmera anda 157 px (a referência) |
| Com Shift, o mesmo movimento | a câmera anda 0,06 px; tremor a 0 |
| Arrasto com Shift | a câmera anda 0 px; o tremor fica em 0; a seleção é exatamente o conjunto dentro do retângulo; 0 golpes |
| Soltar o Shift | o olhar volta 159 px, com o maior passo de 7 px por quadro (o mouse comum, sem Shift, dá 9) |
| Shift no meio da Varredura | a Varredura sai e acerta; 0 ataques básicos; a câmera anda 4 px (o resto da suavização) |
| Pausado | a câmera anda 0 px com o mouse; o arrasto seleciona; ao continuar, maior passo de 3 px |

### R3.2. O Capitão: o que estava errado e o repertório novo

**A investigação antes de mexer** (`ferramentas/lider.mjs`: três sementes, jogador automático forte, "O Capitão",
v2 de antes da mudança). O Capitão escolhia o alvo como um soldado comum (distância + fila), com só um pequeno desconto
para o herói, e reavaliava a cada 0,3 a 0,6 s; andava a 32 (o herói anda a 68 a 72); a Carga ia sempre no grupo nosso
mais denso; e as faíscas do Mago (atordoamento curto, a 4 por segundo) o mantinham cambaleando.

| v2 (vida 380) | Mira o herói | Trocas de alvo | Distância média | Machado (no herói) | Carga (no herói) |
|---|---|---|---|---|---|
| contra o Guerreiro | 33 a 43% do tempo | 13 a 25 por minuto | 173 a 220 px | 5 a 7 (1 ou 2) | 1 ou 2 (0) |
| contra o Mago | 20 a 32% | 15 a 20 por minuto | 172 a 208 px | 4 ou 5 (0) | 1 ou 2 (0); nunca chegou a 40 px dele |

**O repertório agora** (números em `conteudo.js`, regras em `sim.js`, `decidirLider`):

| | Como funciona | Como responder |
|---|---|---|
| **Foco** | Mira no herói quando ele está a até 240 px, **ou quando o herói o fere ou derruba alguém a até 200 px dele** (por 5 s); mantém a escolha por pelo menos 3 s e só larga com o herói a mais de 340 px. A barra dele diz "Atrás de você" ou "Com as tropas"; ao ligar, a faixa avisa "vem atrás de você" | Afastar-se de verdade, ou enfrentá-lo |
| **Machado** (o de antes) | O arco anunciado no chão por 0,7 s. **Se uma tropa nossa está entre ele e o herói, ele golpeia através dela** em vez de parar para duelar com ela | Sair do arco; um golpe forte na preparação interrompe |
| **Arremetida** (nova: alcançar) | Marca um **círculo vermelho de 28 px** no caminho do herói (onde ele estaria com 60% da preparação andando como anda) a 40 a 190 px; **0,75 s depois** salta (0,45 s no ar, por cima de quem estiver no caminho) e cai: 20 no herói, 8 nos soldados, arremessa. Recarga 7 s | Sair do círculo, mudar de direção ou parar; um golpe forte na preparação interrompe; ao cair, fica **0,7 s com o machado cravado, levando +50%** |
| **Carga** (melhorada: pressionar e comandar) | Com o foco no herói, a faixa vai **na direção dele** (um pouco à frente, 0,3 s) e passa 30 px além, até 210 px; reúne até 8 soldados por 0,9 s, que correm junto e chegam com ímpeto. Sem o foco, vai no nosso grupo mais denso, como antes. Recarga 9 s | Sair da faixa; um golpe forte na reunião a desfaz; depois, ofegante 1,2 s, levando +50% |
| **Presença** (a de antes) | A até 90 px, os soldados dele atacam 33% mais rápido, são menos empurrados e não se abalam | Tirá-lo de perto da tropa |

- **Ritmo:** pelo menos 2 s entre duas habilidades; as recargas correm também enquanto ele golpeia ou cambaleia (antes
  só corriam quando ele estava livre). Na prática, uma habilidade a cada 4 a 5 s.
- **Obstáculos:** os soldados dele abrem caminho (como os nossos para o herói); as tropas nossas no caminho levam o
  machado. Nas medições, nenhum tempo travado.
- **Diferença dos comuns, sem imunidade:** golpe fraco (faísca, corte básico) **não o faz cambalear nem estremecer**;
  golpe forte o atordoa (reduzido, como as outras ameaças) e interrompe as preparações. No ar, a Arremetida não para.
- **Vida 380 → 480:** com o foco, ele passa a batalha no alcance do herói e caía em ~30 s contra o Mago; com 480 o duelo
  dura o mesmo que antes (abaixo). Dano e velocidade de golpe não mudaram; andar passou de 32 para 40 (o herói segue
  bem mais rápido).

| Agora (vida 480), três sementes | Mira o herói | Trocas | Vivo | Arremetidas (no herói) | Cargas (no herói) | Machados (no herói) | Dano dele no herói |
|---|---|---|---|---|---|---|---|
| Guerreiro, jogador forte | 95 a 96% | 0 | 48 a 55 s | 4 (1 a 3) | 1 ou 2 (0 ou 1) | 12 a 13 (1 ou 2) | 72 a 94 |
| Mago, jogador forte | 93% | 0 | 34 a 39 s | 3 ou 4 (1 a 3) | 2 a 4 (0 ou 1) | 1 a 7 (0) | 20 a 82 |
| Guerreiro, jogador médio | 93 a 95% | 0 | 35 a 48 s | 1 a 3 (0 a 2) | 0 | 9 a 13 (7) | 182 a 222 |
| Mago, jogador médio | 92 a 93% | 0 | 36 a 41 s | 3 a 5 (1 a 4) | 2 a 4 (0) | 1 a 4 (0) | 20 a 80 |

O jogador automático vê os avisos do Capitão com 0,15 s (forte) ou 0,35 s (médio) de atraso, como uma pessoa; mesmo
assim desvia de quase tudo, então os números de dano são um piso. O médio, que encara o Guerreiro de frente, leva 7
machadadas por batalha (≈ 200 de 260). Em 4× o comportamento é o mesmo (mira 93 a 97%, 0 trocas, 4 a 7 Arremetidas).

### R3.3. As escalas do exército

Na escolha, **Exército: 1× (o encontro normal), 2× ou 4× (experimental)**, e logo abaixo as quantidades reais, contadas
no mesmo mundo que a batalha usa ("Aliados 168 · Inimigos 281: 233 no começo e 48 depois. Capitão, campeão e
porta-estandarte continuam um só."). Parâmetro de endereço: `?qtd=1|2|4` ("normal" e "maior", da v2, valem 1 e 2).

- **O que multiplica:** só os comuns (soldados, veteranos, arqueiros, dos dois lados e das levas). Capitão, campeão e
  porta-estandarte ficam um só; ninguém ganha vida ou dano.
- **Onde ficam:** cada bloco se repete em **alas** a 130 px uma da outra, ao longo da frente (na vertical; os blocos da
  borda de cima ou de baixo, para os lados), e o conjunto é empurrado para dentro do campo se uma ala sairia. A linha
  fica mais longa, não mais grossa no mesmo ponto; a distância entre os exércitos não muda (sem caminhada a mais). Nos
  grupos espalhados, cada grupo cresce no próprio lugar (alas atravessariam os outros grupos). O campo continua 960 × 560
  e os sprites do mesmo tamanho.
- **Com 4×,** as alas aliadas longe do herói (mais de 100 px) **começam defendendo o próprio lugar** e as de perto o
  acompanham: a linha fica inteira em vez de correr toda para ele. O placar mostra ("Acompanhar 84 · Defender aqui 84");
  F4 e 1 trazem todos.
- A 1× é exatamente a v2: as quatro batalhas do jogador automático deram os mesmos números da tabela da R2.7.

| Encontro | 1× aliados / inimigos | 2× | 4× |
|---|---|---|---|
| A primeira batalha | 42 / 94 | 84 / 186 | 168 / 370 |
| Grupos espalhados | 42 / 67 | 84 / 133 | 168 / 265 |
| Duas frentes | 42 / 64 | 84 / 126 | 168 / 250 |
| O Capitão e a retaguarda | 42 / 71 | 84 / 141 | 168 / 281 |

**Custo no navegador, 4×** (`conferir3.mjs escalas`; Chromium 130 sem janela, desenho na CPU, o computador do Jean;
20 s de batalha com o jogador automático forte, já no choque):

| Janela | Herói · encontro · kit | Combatentes (máx.) | Qps | Quadro p95 / máx. | Simulação média / p95 | Desenho média / p95 | Números ao mesmo tempo (máx.) |
|---|---|---|---|---|---|---|---|
| 1920×945 | Guerreiro · primeira batalha · Escudo + Turbilhão | 386 | 60 | 16,8 / 16,8 ms | 0,82 / 1,8 ms | 1,29 / 2,6 ms | 70 (o teto) |
| 1920×945 | Mago · Capitão · Raios + Gelo | 401 | 60 | 16,7 / 16,8 ms | 1,28 / 1,6 ms | 1,17 / 2,1 ms | 10 |
| 1280×720 | Guerreiro · primeira batalha · Escudo + Turbilhão | 386 | 60 | 16,7 / 16,8 ms | 0,77 / 1,4 ms | 1,21 / 2,4 ms | 70 (o teto) |
| 1280×720 | Mago · Capitão · Raios + Gelo | 401 | 60 | 16,7 / 16,8 ms | 1,28 / 1,6 ms | 1,20 / 2,2 ms | 10 |

As linhas do Mago foram medidas antes do ajuste da Corrente de Raios (R3.4: 8 alvos, depois 12); a diferença no custo do quadro é desprezível e não foi medida de novo. No Node, o passo de 4× custa 0,8 a 1,6 ms (`simular.mjs 1 4`). **O limite real de 4× é de leitura, não de
desempenho:** numa área que derruba 30 a 40 de uma vez, os números batem no teto de 70 e os mais velhos somem antes do
tempo, e duas mensagens "N derrubados" se sobrepõem. A quantidade escolhida nunca é reduzida.

### R3.4. As habilidades novas

Escolhidas na tela inicial como as versões da v2 (um botão por versão em cada tecla); a barra continua com quatro
botões. As descrições na tela seguem a skill `texto-regras-fenda`, com os números de `conteudo.js`.

| Herói · tecla | Nova | O que faz | Função |
|---|---|---|---|
| Guerreiro · Espaço (no lugar da Investida ou do Grito) | **Avanço de Escudo** | Por 2,5 s, anda a 70% com o escudo virado para o mouse: barra as flechas inimigas que cruzam o arco (30 px, 150°) vindo da frente, empurra quem está nele (2 de dano na primeira vez) e os aliados a até 50 px levam metade do dano. Outra habilidade o encerra. Recarga 9 s | Avançar com as tropas atrás, contra a retaguarda de arqueiros |
| Guerreiro · Q (no lugar do Salto) | **Turbilhão** | 50 de Fúria (o Salto custa 100). Prende os pés 0,35 s puxando os inimigos comuns a até 70 px para perto (o campeão e o Capitão, não) e golpeia o monte: 9 de dano num círculo de 30 px, arremessa e atordoa | Juntar para o golpe seguinte (Varredura, arremate) |
| Mago · botão direito (no lugar da Bola) | **Corrente de Raios** | 16 de Mana, recarga 1 s. Um raio na direção do mouse (faixa de 170 px) pega o primeiro inimigo e salta para o mais perto ainda não atingido (até 48 px), até 12 alvos: 14 de dano, 1 a menos por salto, no mínimo 7; arremessa quem cai | Linhas, grupos esparsos, a fila que avança; sem chão em chamas |
| Mago · Q (no lugar da Muralha ou do Anel) | **Campo de Gelo** | 35 de Mana, recarga 9 s. Um círculo de 44 px no ponto do mouse (até 170 px) por 5 s: ao surgir, 5 de dano e atordoa 0,3 s; dentro, os inimigos andam a 35% e atacam com 50% da frequência (campeão e Capitão, 60% e 75%) | Segurar uma região: frear a carga, um flanco, a linha que chega |

Ajuste feito durante a rodada: a primeira Corrente (10 de dano, 8 alvos, 22 de Mana) não derrubava um soldado (12 de
vida) e o jogador automático perdia com ela em 2× e 4×; ficou com 14, 12 alvos e 16 de Mana, o que deixa o dano por
Mana perto do da Bola, com outro alcance. Com o kit novo, o jogador automático vence os 12 encontros × escalas.

| Encontro, 1× | Original | Escudo + Turbilhão | Original (Mago) | Raios + Gelo |
|---|---|---|---|---|
| A primeira batalha | 24 s · herói 70 / tropas 12 | 17 s · 84 / 0 · flechas no herói 9 (nas tropas 0) | 25 s · 72 / 11 | 21 s · 68 / 21 |
| Grupos espalhados | 42 s · 29 / 29 | 43 s · 21 / 35 | 37 s · 44 / 15 | 33 s · 38 / 24 |
| Duas frentes | 23 s · 41 / 16 | 25 s · 35 / 18 | 32 s · 40 / 12 | 26 s · 34 / 21 |
| O Capitão | 54 s · 45 / 25 | 42 s · 55 / 16 | 39 s · 16 / 44 | 39 s · 13 / 48 |

(`node ferramentas/simular.mjs 1 1`; derrubados pelo herói / pelas tropas. Em 4×, a mesma tabela em `simular.mjs 1 4`:
todos vencem; o Mago na primeira batalha leva ~100 s e perde as 168 tropas com qualquer kit.)

### R3.5. Verificação: o que foi conferido agora e o que foi reaproveitado

**Conferido nesta rodada:**
- **27 testes da simulação** (`node --test testes/sim.test.mjs`): os 22 da v2 e mais 5: o Capitão (foco estável por
  3 s mesmo com o herói a 300 px depois de feri-lo; o círculo da Arremetida no herói; quem sai não apanha, quem fica
  leva os 20; o machado cravado; um golpe forte interrompe), o caminho (os soldados dele não o empurram; o machado
  atravessa a tropa nossa no caminho), as escalas (contagem exata por tipo nos quatro encontros, especiais um só, vida
  igual, ninguém fora do campo nem a menos de 3 px de outro, alas de fora defendendo só em 4×), 4× até o fim sem NaN com
  o passo médio abaixo de 6 ms, e as quatro habilidades (flecha da frente barrada e a de trás não, aliado com metade do
  dano, puxão sem o campeão, a Fúria gasta, a corrente com 12 alvos e o dano de cada salto = vida que saiu, o gelo
  deixando o passo abaixo da metade).
- **No navegador** (`conferir3.mjs`): a câmera (R3.1), o custo do 4× nas duas janelas (R3.3), a escolha com as
  quantidades nas duas janelas, e um quadro pausado de cada habilidade nova e da Arremetida. Sem erros no console.
- **Batalhas sem tela:** `simular.mjs` em 1×, 2× e 4× com os três kits de cada herói (todas vencidas com o herói);
  `lider.mjs` em 1× e 4×, jogador forte e médio.
- **O jogo não mudou** (`rpg/` e `tests/` intocados): suíte, gabarito e pyflakes rodados de novo nesta rodada; a fumaça
  da interface do jogo, reaproveitada (nada da interface do jogo mudou desde a última passagem).

**Reaproveitado da v2, sem repetir:** a resposta comparada com a v1 (o laço e o controle não mudaram), as conferências de
seleção e ordens por tipo (o código delas não mudou; o arrasto foi conferido de novo com a câmera parada), o desempenho
de 1× e 2× da R2.8. **Sem vídeos e sem folhas quadro a quadro** nesta rodada.

**Capturas** (`capturas/cl3-*.png`): `cl3-escolha-1920` e `-1280` (a escolha com 4× e os kits novos),
`cl3-4x-1920-9s` (o choque em 4×, um Turbilhão de 37), `cl3-arremetida-1920` (o círculo marcado no caminho do Mago),
`cl3-escudo`, `cl3-turbilhao`, `cl3-raios`, `cl3-gelo` (recortes 1280×720).

### R3.6. Limitações conhecidas e o que precisa da avaliação do Jean

- **O Capitão foi medido contra um jogador automático que desvia de quase tudo;** para uma pessoa, a Arremetida que
  mira o caminho (60% da preparação) pode pegar mais do que o esperado. Se parecer injusta, o número a mexer é
  `arremetida.adianta` (0 = mira onde o herói está) ou `preparo`.
- **Ele bate bastante nas tropas** (50 a 360 de dano nelas por batalha em 1×), porque o machado atravessa quem está no
  caminho do herói: é o pedido ("não ficar ocupado com um soldado"), mas as tropas sentem.
- **Turbilhão + Varredura é muito forte:** na primeira batalha, 17 s e quase todos os derrubados são do herói. Está de
  acordo com o pedido de não enfraquecer o herói; avaliar se tira o papel das tropas.
- **O jogador automático quase não usa o Campo de Gelo** (foge antes de juntar cinco perto), então o gelo não foi medido
  em batalha, só nos testes e na captura.
- **4× é experimental:** 60 qps, mas o teto de 70 números e as mensagens sobrepostas nas mortes em massa; o Mago perde
  todas as tropas na primeira batalha em 4×. Nada foi reduzido em silêncio.
- **A câmera, no comando, ainda acompanha o herói se ele andar** (fora do arrasto); se atrapalhar, dá para pará-la de
  todo enquanto o Shift está apertado.
- **Arte provisória:** o escudo e o gelo são formas pintadas no chão; o Capitão no ar é o mesmo sprite, levantado.
- **Para o Jean avaliar:** (1) segurar Shift e arrastar ficou estável, com o tremor no máximo? a volta ao soltar é
  suave? (2) o Capitão agora te enfrenta de verdade, com o Guerreiro e com o Mago? dá para ler e desviar a Arremetida e a
  Carga? ele ficou forte demais ou de menos? (3) as batalhas 2× e 4× ficam legíveis, e os comandos respondem bem nelas?
  (4) as quatro habilidades novas mudam o jeito de jogar? alguma é forte ou fraca demais?

Rodada 1. Pedido do Jean: depois de jogar o protótipo tático (o [29](29-ETAPA8-COMBATE-TATICO.md)) e gostar do
ganho espacial, **investigar direto o combate em campo livre**: controle direto do herói, em tempo real, no meio de
tropas pequenas que lutam sozinhas, com poucas ordens coletivas. Pesquisa orientada à implementação e um protótipo
isolado. **O combate do jogo não mudou (1.220.0); a integração continua pendente de avaliação.**

Ligações: o [28](28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md) (builds), o [29](29-ETAPA8-COMBATE-TATICO.md) (a grade,
preservada como histórico, sem expansão nesta rodada), o [plano 23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) e a
[continuidade](00-COMECE-AQUI.md). Protótipo:
[`ferramentas/prototipos/etapa8-campo/`](../ferramentas/prototipos/etapa8-campo/LEIA-ME.md) (`demo.bat`, porta 8801).

| Seção | O que tem | Natureza |
|---|---|---|
| 0 | A decisão e o critério desta entrega | Registro |
| 1 | Pesquisa: referências e o que cada uma deu | Pesquisa com fontes |
| 2 | A implementação: o que foi reaproveitado e o que foi separado | Decisão técnica |
| 3 | Campo, escala e representação | Decisão e medida |
| 4 | Controle direto e o compromisso dos golpes | Regra do protótipo |
| 5 | Os dois kits | Regra do protótipo |
| 6 | O impacto | Regra do protótipo |
| 7 | Tropas, ordens, movimento e ocupação | Regra do protótipo |
| 8 | A batalha | Conteúdo |
| 9 | Verificação: funcionamento | Testes e medidas |
| 10 | Verificação: sensação | Observado e o que só o Jean responde |
| 11 | Desempenho | Medida, com as condições |
| 12 | Limitações conhecidas | Lista |
| 13 | O que esta direção mudaria no jogo (não implementado) | Estimativa |
| 14 | O que avaliar jogando | Para o Jean |


## Rodada 2 (01/11/2026): Campo Livre 2

**O que o Jean aprovou** (depois de jogar o Campo Livre 1): a direção, "extremamente divertido", para continuar **no
protótipo, sem integração**. Gostou especialmente das tropas pequenas, do herói muito mais forte que um soldado, dos
golpes que derrubam vários, dos arremessos e explosões e do **tremor no máximo** (150%). Pediu para não reduzir o poder
do herói por ele matar muito (o desafio vem das ameaças, do posicionamento e de onde intervir) e para ampliar leitura,
confrontos, escolhas de habilidades e comando de tropas sem perder a fluidez e o impacto.

**Em teste nesta rodada (nada aprovado ainda):** os números de dano, o líder inimigo, o modo de comando e a seleção, as
mudanças de leitura, os três encontros novos e as quatro versões de habilidade. A primeira versão fica congelada em
`tela-v1/` e abre em `/v1/` (o link está na tela de escolha), para comparar.

| Seção | O que tem |
|---|---|
| R2.1 | Números de dano |
| R2.2 | O líder inimigo: Harg, o Capitão |
| R2.3 | Modo de comando, seleção e ordens por grupo |
| R2.4 | Leitura do choque das tropas |
| R2.5 | Os encontros |
| R2.6 | As versões das habilidades |
| R2.7 | O que as tropas fazem além de matar |
| R2.8 | Verificação e desempenho |
| R2.9 | Limitações conhecidas e o que precisa da avaliação do Jean |

### R2.1. Números de dano

- **Só o dano do herói**, no momento do impacto, nascendo em cima do alvo atingido (a 13 px do pé, com 3 px de
  variação para os lados), subindo 10 px e indo um pouco na direção do golpe; somem em 0,7 s. Nenhum número do dano
  entre soldados.
- **O valor é o dano do golpe que entrou na conta** (o mesmo `ferir` que tira a vida, um evento por acerto). Num alvo
  que morre, a vida para em 0 e o número mostra o golpe inteiro (13 num soldado de 12): é o valor que a habilidade
  causa, não um número inventado. Os testes conferem um número por atingido e, em quem sobrevive, número = vida que saiu.
- **Distinção sem legenda:** básico em branco; golpe forte (Varredura, Salto, Bola, arremate, Investida) em amarelo;
  **crítico** maior (algarismos com o dobro do tamanho), laranja, com "!" e um quadro branco no nascimento. O crítico é
  uma regra nova e real: **10% de chance por acerto de 1,5× (arredondado)** nos golpes diretos do herói, nos dois
  heróis; aparece na ficha de cada um na escolha.
- **Dano contínuo** (o fogo do chão, a Muralha, o Anel, o Sangramento) agora é **inteiro e de meio em meio segundo**
  (3, 7, 4 e 3 por tique, os mesmos totais de antes). Na tela, **soma por alvo**: um tique que chega até 0,6 s depois do
  anterior entra no mesmo número, que se renova; fogo em laranja-claro, sangue em vermelho.
- **Fonte própria:** algarismos de 3 × 5 pixels desenhados à mão com contorno escuro de 1 px; nítidos em qualquer
  ampliação e legíveis sobre o fogo e o piso. Desenhados **por cima dos efeitos** (a explosão não os cobre); o herói e o
  líder são **redesenhados depois**, para os números nunca os esconderem. No máximo 70 números ao mesmo tempo.
- **Durante o tremor**, os números tremem junto com o campo (estão presos ao lugar do acerto); a mira, o retângulo de
  seleção e a HUD não tremem (R2.3).

### R2.2. O líder inimigo: Harg, o Capitão

No encontro "O Capitão e a retaguarda". Não é um soldado com muita vida: tem três ferramentas e uma função de comando.

| | Como funciona | Como responder |
|---|---|---|
| **Machado** | O golpe do campeão: arco de 150° anunciado no chão por 0,7 s; 26 no herói, 8 nos soldados (e os arremessa) | Sair do arco; um golpe forte na preparação o interrompe |
| **Carga** (comando) | A cada 11 s (a primeira aos 6 s), escolhe o nosso grupo mais denso entre 50 e 170 px (o herói vale três), **reúne até 10 soldados** perto dele por 1 s e marca a **faixa** de 150 px no chão; depois corre a faixa a 150 px/s atropelando quem está nela (14 nos soldados, 22 no herói, empurrão de lado) e os reunidos correm junto e chegam com **ímpeto** (dano dobrado por 2 s) | Sair da faixa; **um golpe forte na reunião desfaz a carga** e solta os reunidos; depois da carga ele fica **ofegante por 1,2 s**, parado e levando **+50% de dano** |
| **Presença** (comando) | A até 90 px (o círculo vermelho tracejado), os soldados dele atacam 33% mais rápido, são empurrados pela metade e **não se abalam** | Tirá-lo de perto da tropa, ou derrubá-lo |

- **Reconhecível:** armadura escura, chifres dourados, capa e **contorno vermelhos** (o único inimigo com contorno),
  anel vermelho no chão, barra de vida maior, a **barra do Capitão no alto da tela** com o estado ("Reúne 8 para a
  carga!", "Ofegante: leva +50% de dano", "Presença: 12 soldados firmes"), e seta vermelha na borda quando sai da tela.
- **Vida 380**, massa 7 (pouco empurrado), atordoamento reduzido como as outras ameaças, mas interrompível.
- **Consequência da derrota** (aparece na apresentação do encontro): **a tropa a até 150 px dele foge do campo; o resto
  se abala por 3 s; a batalha continua.** E, enquanto ele estiver de pé, **ninguém foge** (a vitória por 20% só vale
  depois que ele cai).
- **A escolha:** as cargas vão para onde as nossas tropas estão juntas; ir atrás dele deixa a frente com os soldados, e
  ficar com eles deixa a carga sair. Com a Varredura Sangrenta (que não interrompe), a mesma batalha ficou muito mais
  difícil para o jogador automático (107 s e 36 tropas perdidas, contra 45 s e 19 com a original; seção R2.7).

### R2.3. Modo de comando, seleção e ordens por grupo

**A solução:** **Shift segurado** liga o modo de comando (temporário: soltou, voltou ao combate); **pausado, o mouse já
está em modo de comando**. Escolhi segurar em vez de alternar porque a ordem dura um instante e o herói continua andando
com WASD enquanto o Shift está apertado: não há um estado esquecido ligado que transforme um clique de ataque em
seleção. O estado aparece embaixo da ficha ("Combate · segure Shift para comandar" / "Comando: arraste para
selecionar…") e a mira troca a cruz por quatro cantos claros.

| No modo de combate | No modo de comando (Shift ou pausado) |
|---|---|
| botão esquerdo: ataque básico (como antes) | botão esquerdo **arrastado**: retângulo que seleciona as tropas aliadas dentro dele, sem golpe nenhum; um clique numa tropa seleciona só ela; um clique no vazio limpa; com Ctrl, soma |
| botão direito: habilidade | botão direito: **Defender ali** (para a seleção ou, sem seleção, para todos) |

- **Por tipo:** **F1 Soldados, F2 Arqueiros, F4 Todos, X limpa, Ctrl soma** (funcionam em qualquer modo, também
  pausado). **F3 fica indisponível** ("—" no placar e um aviso curto): este exército só tem dois tipos, e não se criou
  um terceiro para preencher a tecla. F1 a F4 não abrem a ajuda nem a busca do navegador (`preventDefault` e o evento
  `help`).
- **As ordens** (1 Acompanhar, 2 Atacar, 3 Defender no ponto do mouse) **valem para a seleção; sem seleção, para o
  exército inteiro** (o jeito rápido de comandar todos continua o de antes). Quem não recebeu a ordem mantém a sua.
  Cada tropa guarda a própria ordem; os anéis em volta do herói e dos pontos de defesa são contados dentro de cada grupo.
- **Na tela:** colchete claro em volta do pé de cada selecionado; no placar, os tipos com quantos há, a seleção com
  quantos e de que tipo, e as ordens com **quantos cumprem cada uma** ("Acompanhar 16 · Atacar 14 · Defender aqui 12");
  uma bandeira por ponto de defesa em uso (o alcance aparece pausado, logo depois da ordem e quando aquele grupo está
  selecionado).
- **A seleção não passa o controle do herói** (o herói nunca entra nela). **Mortos saem da seleção** no passo seguinte.
- **O tremor:** a mira, o retângulo e a conversão do mouse para o campo usam a câmera **sem** o tremor (o tremor é só
  visual): com trauma 1 e intensidade 150%, o mouse aponta para o mesmo ponto e o mesmo arrasto pega as mesmas tropas
  (medido, R2.8).

### R2.4. Leitura do choque das tropas

- **Herói:** além do contorno, do anel dourado e de ser desenhado por cima, uma **seta dourada** em cima da barra.
- **Lados:** a sombra no pé ficou **tingida** (azul nos nossos, vermelha nos deles): no meio do choque, o pé diz o lado.
- **Separação:** entre lados diferentes, o vão mínimo passou de 0,4 para **1,6 px**: as duas linhas encostam sem se
  misturar; dentro do mesmo lado continua 0,4 (os grupos seguem densos para as áreas).
- **Barras:** sempre nas ameaças (o Capitão maior); no veterano, **5 px por 0,8 s** depois de apanhar (eram 6 px por
  1,5 s): o choque não vira uma faixa de barras.
- **Golpes preparados:** o arco do machado e a faixa da carga são pintados no chão e **redesenhados por cima dos corpos**
  (só a borda): não se escondem atrás da multidão.
- **Estados à vista em 1 px:** gota vermelha (sangrando), brilho dourado (inspirado pelo Grito), "!" vermelho
  (reunido para a carga), estrelas (atordoado ou ofegante).
- **Corrigido de passagem:** a barra de vida do herói na ficha **sumia** depois do primeiro golpe recebido (também na
  v1): a animação usava o nome `dor`, que o CSS do jogo já usa com `opacity: 0`. Na v2 o nome é próprio; a v1 ficou como
  estava (congelada).

### R2.5. Os encontros

Escolhidos na tela inicial, cada um sempre igual (mesma semente). A apresentação mostra a descrição e a regra.

| Encontro | O que é | O que muda para o jogador |
|---|---|---|
| **A primeira batalha** | A do Campo Livre 1, preservada (mesmo código de montagem) | A referência |
| **Grupos espalhados** | 7 grupos pequenos (soldados, veteranos, dois postos de arqueiros, o porta-estandarte com escolta) longe uns dos outros, acordando em tempos diferentes, quando alguém chega a 80 px ou quando um dos seus apanha; aos 35 s, mais um grupo pelo norte | Cada área pega menos; quem decide é onde o herói está e qual grupo ele acorda; "Defender" segura um grupo enquanto o herói vai a outro |
| **Duas frentes** | Herói e tropas no meio; um exército vem do oeste, outro do leste (com o porta-estandarte), e o campeão chega pelo sul aos 25 s | É preciso dividir: F2 + Defender num lado, os soldados no outro, o herói onde a linha cede |
| **O Capitão e a retaguarda** | Linha de 18 soldados e 8 veteranos, Harg com a guarda de 10, e uma **retaguarda de 22 arqueiros que atira do posto** (não avança); reforço de 12 aos 40 s | Mergulhar nos arqueiros (as tropas seguram a frente) ou enfrentar Harg; tirar as tropas da faixa da carga |

Na opção "Maior", cada bloco comum dobra (líder, campeão e porta-estandarte não).

### R2.6. As versões das habilidades

Escolhidas na tela inicial, por herói; a original continua como opção. Cada uma muda o uso, não só os números.

| Herói · tecla | Original | Versão | O que muda |
|---|---|---|---|
| Guerreiro · botão direito | **Varredura**: 13, empurra e atordoa, arremessa quem cai | **Varredura Sangrenta**: 7 no golpe + Sangramento de 3 a cada 0,5 s por 3 s (18), quase sem empurrão, sem atordoar | Os inimigos ficam onde estão (as tropas os seguram), morrem 1 a 2 s depois; **não interrompe** o machado nem a carga |
| Guerreiro · Espaço | **Investida**: 100 px, joga para os lados | **Grito de Guerra**: aliados a até 70 px atacam 67% mais rápido e recuperam 2 de vida por segundo por 6 s; abala por 1,5 s os inimigos comuns colados (45 px); recarga 10 s | Troca a mobilidade por apoio: o herói luta **junto** das tropas em vez de abrir caminho sozinho |
| Mago · botão direito | **Bola de Fogo**: 13, arremessa, chão de 2 s | **Bola Incendiária**: 6 no impacto, sem arremesso, chão de 38 px por 4 s (3 a cada 0,5 s) que os inimigos **contornam** | De explosão que limpa para **terreno que nega passagem**: tampar um vão, proteger as tropas |
| Mago · Q | **Muralha de Fogo**: parede de 96 px | **Anel de Fogo**: anel de 32 px de raio por 5 s; **ninguém atravessa a linha** (dentro fica dentro), a linha queima 4 a cada 0,5 s | **Prender** um grupo (ou o Capitão, longe da guarda) para as Bolas, ou cercar as tropas |

### R2.7. O que as tropas fazem além de matar

O fim de cada batalha mostra, além dos derrubados: **inimigos ocupados pelas tropas** (soma do tempo em que cada inimigo
estava atacando uma tropa, não o herói), **dano que as tropas seguraram** e **flechas inimigas nas tropas e no herói**.
Medido com `ferramentas/simular.mjs` (jogador automático forte, batalha normal, uma semente):

| Encontro · herói · kit | Resultado | Tempo | Derrubados herói / tropas | Perdas | Inimigos ocupados (inimigo × s) | Dano que as tropas seguraram | Flechas nas tropas / no herói |
|---|---|---|---|---|---|---|---|
| Primeira batalha · guerreiro · original | vitória | 24 s | 70 / 12 | 0 de 42 | 500 | 135 | 25 / 10 |
| Primeira batalha · guerreiro · sangrenta+grito | vitória | 29 s | 57 / 23 | 0 de 42 | 660 | 219 | 37 / 8 |
| Primeira batalha · mago · original | vitória | 25 s | 72 / 11 | 2 de 42 | 536 | 290 | 22 / 2 |
| Primeira batalha · mago · incendiaria+anel | vitória | 27 s | 55 / 24 | 14 de 42 | 659 | 425 | 18 / 1 |
| Primeira batalha · só as tropas | derrota | 45 s | 0 / 11 | 39 de 42 | 2199 | 581 | 38 / 54 |
| Grupos espalhados · guerreiro · original | vitória | 42 s | 29 / 29 | 3 de 42 | 515 | 241 | 18 / 0 |
| Grupos espalhados · guerreiro · sangrenta+grito | vitória | 44 s | 35 / 26 | 7 de 42 | 629 | 260 | 12 / 0 |
| Grupos espalhados · mago · original | vitória | 37 s | 44 / 15 | 3 de 42 | 442 | 209 | 25 / 0 |
| Grupos espalhados · mago · incendiaria+anel | vitória | 40 s | 21 / 36 | 1 de 42 | 532 | 216 | 13 / 0 |
| Grupos espalhados · só as tropas | vitória | 90 s | 0 / 54 | 32 de 42 | 934 | 518 | 3 / 0 |
| Duas frentes · guerreiro · original | vitória | 23 s | 41 / 16 | 2 de 42 | 394 | 144 | 7 / 0 |
| Duas frentes · guerreiro · sangrenta+grito | vitória | 25 s | 38 / 15 | 0 de 42 | 454 | 89 | 13 / 1 |
| Duas frentes · mago · original | vitória | 32 s | 40 / 12 | 3 de 42 | 652 | 241 | 16 / 0 |
| Duas frentes · mago · incendiaria+anel | vitória | 27 s | 34 / 20 | 0 de 42 | 604 | 199 | 11 / 0 |
| Duas frentes · só as tropas | derrota | 38 s | 0 / 17 | 41 de 42 | 1388 | 602 | 26 / 31 |
| O Capitão · guerreiro · original | vitória | 45 s | 47 / 24 | 19 de 42 | 342 | 431 | 0 / 6 |
| O Capitão · guerreiro · sangrenta+grito | vitória | 107 s | 48 / 22 | 36 de 42 | 460 | 649 | 4 / 44 |
| O Capitão · mago · original | vitória | 31 s | 56 / 15 | 13 de 42 | 291 | 358 | 0 / 2 |
| O Capitão · mago · incendiaria+anel | vitória | 37 s | 43 / 28 | 30 de 42 | 358 | 591 | 1 / 1 |
| O Capitão · só as tropas | derrota | 92 s | 0 / 35 | 36 de 42 | 1265 | 575 | 0 / 0 |

Leitura: **as versões mudam o papel das tropas** mais que o resultado. Com Sangrenta + Grito, as tropas derrubam 23 na
batalha original (12 com o kit original) e ficam mais tempo ocupando inimigos (660 contra 500); com Incendiária + Anel,
24 a 36 (11 a 15 com o original), porque o herói prende e nega terreno e elas acabam o serviço. No Capitão, as tropas
**seguram** o dobro do dano (431 a 649) e perdem muito mais: é onde a carga cai. Sem o herói, as tropas ocupam muito os
inimigos (1265 a 2199) e perdem, exceto nos grupos espalhados (vencem em 90 s perdendo 32 de 42). Os números são de um
jogador automático preciso: comparam encontros e kits entre si, não preveem uma partida de uma pessoa.

### R2.8. Verificação e desempenho

**Testes da simulação** (`node --test testes/sim.test.mjs`, 22): os 14 da v1 e mais: o número é o dano do golpe (um por
atingido; vida que saiu = número em quem sobrevive); uma explosão em 15+ veteranos dá um número por atingido e a soma
bate; os tiques do fogo são inteiros; crítico perto de 10% e = 1,5× arredondado; a ordem chega só à seleção (sem
seleção, a todos; os outros mantêm a sua; a soma de seleção; o morto sai dela); duas ordens ao mesmo tempo (arqueiros
num ponto, soldados acompanhando); o líder reúne, a carga atropela quem está na faixa e não o herói fora dela, a
Varredura desfaz a reunião e solta os reunidos; ofegante leva +50%; enquanto ele vive ninguém foge; derrubado, a tropa
perto foge e a longe não; as quatro versões (sangramento de 6 tiques, anel que prende, grito que inspira e abala, chão
que empurra para fora); os quatro encontros terminam com vitória (jogador automático médio, com os kits originais e
com as versões do Mago) e, sem o herói, com derrota (nos grupos espalhados as tropas podem vencer sozinhas, mas perdendo
25 ou mais).

**No navegador, com teclado e mouse de verdade** (`ferramentas/medir.mjs selecao`): F2 seleciona os 12 arqueiros e o
placar diz "Seleção: 12 (arqueiros 12)"; 3 manda só eles defender; F3 avisa que não há terceiro tipo; Shift + arrasto
seleciona 14 soldados **sem nenhum golpe** (o contador de usos do Corte ficou em 0); empurrão sem dano (o fim da Investida) não mostra número; 2 os manda atacar (ficam 12
defendendo, 14 atacando, 16 acompanhando); X limpa; pausado, o arrasto seleciona sem Shift, F4 pega os 42 e 1 os
manda acompanhar; com trauma 1 a 150%, o ponto do mouse no campo não muda e o mesmo arrasto pega as mesmas 21 tropas;
nenhuma aba nova (F1 a F4 não abriram nada do navegador). Pausa, retomada e reinício como na v1.

**Resposta comparada com a v1** (três rodadas de cada, mesmo roteiro, tempo de jogo): andar começa no primeiro passo
(16,7 ms) nas duas; velocidade máxima em 83 a 100 ms nas duas; parada em 67 a 83 ms nas duas; a Varredura começa no
primeiro passo e acerta em 217 ms nas duas. **Sem regressão de controle.**

**Desempenho** (`medir.mjs desempenho`; Chromium 130 sem janela, desenho na CPU, o computador do Jean, 01/11/2026;
20 s de batalha com o jogador automático forte, que chega ao contato, às áreas e às mortes em massa):

| Janela | Tropas | Herói · encontro | Combatentes (máx.) | Qps | Quadro p95 / máx. | Simulação média / p95 | Desenho média / p95 |
|---|---|---|---|---|---|---|---|
| 1280×720 | normal | Guerreiro · original | 98 | 60 | 16,7 / 16,8 ms | 0,34 / 0,7 ms | 1,25 / 2,5 ms |
| 1280×720 | normal | Mago · Capitão | 102 | 60 | 16,7 / 16,8 ms | 0,28 / 0,6 ms | 1,42 / 3,6 ms |
| 1280×720 | maior | Guerreiro · original | 195 | 60 | 16,7 / 16,8 ms | 0,53 / 1,1 ms | 1,44 / 3,2 ms |
| 1280×720 | maior | Mago · Capitão | 202 | 60 | 16,7 / 16,8 ms | 0,53 / 0,9 ms | 1,66 / 3,9 ms |
| 1920×945 | normal | Guerreiro · original | 98 | 59,9 | 16,7 / 33,4 ms | 0,27 / 0,6 ms | 1,18 / 2,7 ms |
| 1920×945 | normal | Mago · Capitão | 102 | 59,8 | 16,7 / 50 ms | 0,27 / 0,5 ms | 1,48 / 4,0 ms |
| 1920×945 | maior | Guerreiro · original | 195 | 60 | 16,7 / 16,8 ms | 0,53 / 1,3 ms | 1,56 / 3,5 ms |
| 1920×945 | maior | Mago · Capitão | 202 | 60 | 16,8 / 16,8 ms | 0,68 / 1,2 ms | 1,96 / 4,6 ms |

A primeira medida da v2 deu desenho com p95 de até 7 ms e quadros de 100 ms: os contornos grandes (a presença de 90 px
do Capitão, a aura do estandarte) eram pintados pixel a pixel a cada quadro, e cada corpo pousado passava por um filtro
de canvas. Os dois passaram a ser feitos uma vez e guardados (as áreas de golpe continuam pintadas exatas a cada quadro).
Sobraram **quadros isolados de 33 a 50 ms em 2 das 8 medições**, uma vez por batalha, sem repetir; a causa não foi
isolada (pode ser a criação desses guardados ou as próprias chamadas da medição). No Node, o passo custa 0,07 a 0,3 ms.

**Vídeos** (`videos/`, 1280×720): `area-numeros-mago` e `area-numeros-guerreiro` (golpes em área com os números,
jogador automático, batalha original), `lider-capitao` (o confronto com Harg: as reuniões, as cargas, a queda),
`selecao-e-duas-ordens` (teclado e mouse de verdade: F2 e Defender ao norte, Shift + arrasto nos soldados do oeste e
Atacar, o herói andando e atacando, pausa, F4 e Acompanhar). Os da v1 ficaram em `videos/campo-livre-1/`; as capturas
da v1, em `capturas/campo-livre-1/`. Sequências quadro a quadro: `capturas/sequencia-bola.png` (a explosão com os 15
números e um crítico), `-varredura`, `-salto`, `-lider` (a faixa enchendo e a carga).

### R2.9. Limitações conhecidas e o que precisa da avaliação do Jean

- **O jogador automático é forte** e vence quase tudo em 20 a 45 s; o equilíbrio para uma pessoa não foi medido. O herói
  não foi enfraquecido (pedido do Jean); a dificuldade nova está no Capitão, nas duas frentes e na retaguarda.
- **Com a Varredura Sangrenta, o Capitão fica muito mais difícil** (ela não interrompe): é o tipo de diferença que se
  queria, mas pode ser demais. Avaliar jogando.
- **Os grupos espalhados podem ser vencidos só pelas tropas** (devagar e perdendo 25 a 32 de 42): a concentração ganha
  de grupos isolados. Pode ser bom (as tropas importam) ou pedir grupos que se juntem.
- **O Capitão só escolhe o grupo mais denso** para a carga e não protege a retaguarda; os arqueiros da retaguarda não
  recuam juntos.
- **Os números** no meio de uma área de 15 se amontoam um pouco (cada um em cima do seu soldado); o crítico se destaca.
- **Arte do Capitão provisória** (a mesma grade do campeão, recolorida, com chifres e capa).
- **Desempenho:** 60 qps nas oito medições, com quadros isolados de 33 a 50 ms em duas (R2.8).
- **Para o Jean avaliar:** (1) os números ajudam ou poluem, e o crítico se lê sem legenda? (2) o Capitão cria um
  confronto que dá vontade de enfrentar, e a escolha entre ele e as tropas aparece? a regra da derrota ficou clara? (3)
  Shift segurado para comandar é fluido, ou preferiria alternar com uma tecla? (4) as ordens a dois grupos foram úteis em
  "Duas frentes"? (5) as versões mudaram a maneira de jogar o mesmo encontro? (6) as sombras tingidas e o vão entre as
  linhas resolveram a faixa ilegível do choque?

---

## Rodada 1 (31/10/2026): Campo Livre 1

## 0. A decisão e o critério

- **Nova direção do experimento:** campo livre com herói em tempo real e tropas pequenas. Substitui, como próximo
  experimento, a expansão do tático; **não** substitui o combate do jogo.
- **O tático fica preservado** (`etapa8-tatico/`, o 29), sem expansão nesta rodada. O X1 (`etapa8-builds/`) também.
- **Fora:** Revezamento e qualquer manipulação da ordem dos turnos (recusados; aqui não há turnos); castelos, reino,
  recrutamento, salários, mapa estratégico, campanha de exércitos; inventário, diálogos, cenas e progressão.
- **Critério principal:** mover o herói e acertar uma habilidade num grupo de soldados pequenos precisa ser fluido,
  legível e satisfatório, com vontade de repetir.

## 1. Pesquisa: referências e o que cada uma deu

As cinco capturas enviadas pelo Jean foram vistas nesta conta: quatro de **Sword & Banner** (o deserto com cavalaria
azul contra infantaria verde, a ponte na neve, o campo com cavalaria vermelha, o cerco à muralha) e uma de
**9 Kings** (o exército roxo diante do rei negro). O que foi aproveitado delas é a **escala e a leitura**: soldados
de uns 8 a 12 px de altura numa ampliação inteira, cor de equipe chapada no corpo, cabeça/elmo claro, a arma como um
risco branco, sombra no chão, piso calmo com poucas manchas, e o conjunto lido como massas de cor. Não foram usados
construções, gerenciamento, formações de centenas, nem nenhum asset.

| Referência | O que foi visto ou lido | O que entrou no protótipo |
|---|---|---|
| **Sword & Banner** (Bitrot Games; [Steam](https://store.steampowered.com/app/4957080), [GamingOnLinux](https://www.gamingonlinux.com/2026/07/mount-blade-meets-total-war-in-the-upcoming-pixel-art-sword-banner/), [Niche Gamer](https://nichegamer.com/sword-banner-is-a-stunningly-pixelated-rts-epic/)) | As capturas; os textos: RTS em pixel, "Mount & Blade meets Total War", unidades individuais, ainda não lançado (playtest) | A escala das unidades, as cores de equipe, a sombra. Ele é RTS (seleção e comando de grupos): o controle direto do herói **não** vem dele |
| **9 Kings** (Sad Socket; [Xbox Wire](https://news.xbox.com/en-us/2025/08/13/9-kings-pc-game-pass-preview/), [Rogueliker](https://rogueliker.com/9-kings-early-access-review/)) | A captura; os textos: autobatalha, o jogador quase não age durante a luta | Unidades miúdas em bloco, o "rei" maior e de outra cor que o resto (aqui: o herói mais claro, com contorno e anel no chão). A passividade dele é o oposto do que se quer |
| **Mount & Blade II: Bannerlord** ([guia de táticas](https://gamerguides.com/mount-and-blade-ii-bannerlord/guide/introduction/useful-gameplay-tips/tactics), [Steam](https://steamcommunity.com/app/261550/discussions/0/2264689848035590880)) | As ordens por F1/F2/F3: seguir, atacar, manter posição; o jogador luta pessoalmente | As três ordens coletivas (Acompanhar, Atacar, Defender aqui), sem seleção de grupos nem formações |
| **Dynasty Warriors / musou** ([wiki da série](https://koei.fandom.com/wiki/File:NPC_8_(DWU).png), [Siliconera](https://www.siliconera.com/here-are-dynasty-warriors-origins-semi-unique-officers/), [TechRadar](https://www.techradar.com/gaming/dynasty-warriors-origins-review)) | Tropa comum é interrompida pelos golpes de um oficial; oficiais têm uma barra de resistência; a crítica recorrente é "sempre o mesmo golpe" | Três camadas: soldado (cai de uma vez), veterano (aguenta um golpe forte) e as ameaças (campeão, porta-estandarte); golpe forte interrompe; o kit varia o golpe (arco, linha, círculo, parede) para não ser só um |
| **Masahiro Sakurai, hitstop** ([Source Gaming, coluna Famitsu 490](https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/), [Nintendo Wire](https://nintendowire.com/news/2022/12/12/this-week-in-sakurai-12-5-12-11-fine-tuning-hit-stop-and-cheating-the-system/)) | A parada curta no impacto, maior para golpe mais forte; vale para todo gênero | A pausa de impacto proporcional (45 a 100 ms) só nos golpes fortes; o básico só congela o alvo (40 a 70 ms), não a tela |
| **Squirrel Eiserloh, "Juicing Your Cameras With Math"** (GDC 2016; [Game Developer](https://www.gamedeveloper.com/programming/video-sprucing-up-cameras-with-math)) | O tremor por "trauma": o golpe soma trauma, ele cai sozinho, o deslocamento é o trauma ao quadrado | O tremor exatamente assim (queda 1,8/s, até 6 px nativos), mais um empurrão curto na direção do golpe; intensidade 0 a 150% |
| **Jan Willem Nijman, "The Art of Screenshake"** (Vlambeer, INDIGO 2013; [Kenney](https://kenney.nl/learn/must-see-videos-for-indie-developers)) | Só a descrição (o vídeo não foi aberto) | A lista de reforços de impacto (clarão no alvo, recuo, partículas, marcas que ficam, som), sem depender de um só |
| **Combate cancelável** ([Game Developer, God of War](https://www.gamedeveloper.com/pc/combat-canceled-i-god-of-war-i-action-game-design), [Aztez](https://aztez.com/blog/2012/05/24/the-amalur-problem/)) | Cancelamento antes e depois do contato; o comando guardado ("buffer") que pode ser trocado | A regra do compromisso (seção 4): a preparação do golpe forte prende; depois do contato, andar ou outra habilidade cortam a recuperação; o comando guardado por 0,2 s |
| **Maddy Thorson, "Celeste & Forgiveness"** ([o texto](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)) | O comando apertado um pouco antes da hora sai quando der | O adiantamento de 0,2 s |
| **Craig Reynolds, steering** ([notas de curso](https://courses.cs.washington.edu/courses/cse457/15au/projects/animator/linkedItems/flocking.pdf)); **Elijah Emerson, flow fields** (Game AI Pro, cap. 23; [CRC](https://www.taylorfrancis.com/books/9780429100277/chapters/10.1201/b16725-29)) | A separação por vizinhos próximos; a grade espacial para achar vizinhos; campos de fluxo para milhares | A separação numa grade espacial (células de 12 px) e alvos com vagas. Campo de fluxo **não** foi preciso: o campo é aberto e sem obstáculos (só a Muralha, tratada como obstáculo macio) |
| **Riot, "Clarity in League"** ([texto](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/), [guia de VFX](https://nexus.leagueoflegends.com/wp-content/uploads/2017/10/VFX_Styleguide_final_public_hidpjqwx7lqyx0pjj3ss.pdf)) | A área desenhada tem de bater com a área que acerta; ruído visual mínimo; efeito alto só quando o impacto é alto | A área pintada pela **mesma função** que decide quem é atingido (seção 9); o clarão da explosão dura ~60 ms; fumaça fraca; marcas discretas |
| **Pixel art miúda** ([Slynyrd, Pixelblog 59](https://www.slynyrd.com/blog/2025/11/28/pixelblog-59-tiny-sci-fi-pixels)) | Poucos quadros com poses fortes; volume constante; não girar sprite pequeno em ângulo livre | Seis poses por tipo; o corpo arremessado gira de 90 em 90° (exato na grade) |

**Limites da pesquisa:** Sword & Banner não está lançado (só capturas e textos de imprensa); de 9 Kings, a captura e
análises; Bannerlord, guias e fóruns (as teclas mudam por versão); o capítulo de Emerson e a palestra de Nijman só por
resumos. A experiência deles não foi jogada nesta conta.

## 2. A implementação: o que foi reaproveitado e o que foi separado

- **Separado:** a simulação é JavaScript no navegador (`tela/sim.js`), com passo fixo de 1/60 s e semente, sem DOM (roda
  igual no Node para os testes). Forçar o motor Python por turnos a simular 60 passos por segundo pela rede local seria
  frágil (latência, estado duplicado, um vaivém por quadro). O servidor do protótipo só serve arquivos.
- **Reaproveitado:** o padrão dos lançadores (versão no topo, porta livre, quem ocupa a porta), a paleta e as fontes da
  interface (`/static/css/01-base.css`, `11-tipografia.css`, `sprites.js` para as variáveis), o modo de som do jogo (Web
  Audio sintetizado, como `rpg/web/static/som.js`), a ideia de "Sensação" do jogo (`sensacao.js`: parada no impacto e
  tremor com os números num lugar só, aqui `IMPACTO` em `conteudo.js`), a semente fixa para repetir (como o X1 e o
  tático), o formato das descrições da skill `texto-regras-fenda` (efeito primeiro; custo e recarga no componente).
- **Não reaproveitado:** as habilidades do jogo (`rpg/habilidades.py`) e as do X1/tático não foram convertidas; os kits
  daqui são pequenos e novos (seção 5). Nenhum retrato em círculo: os combatentes são sprites de corpo inteiro.

## 3. Campo, escala e representação

- **Escala nativa e ampliação:** o canvas tem o tamanho da janela dividido por uma ampliação **inteira**
  (`floor(min(largura/600, altura/300))`): **2× em 1280×720** (640×360 px nativos visíveis) e **3× em 1920×945** (640×315).
  O CSS amplia com `image-rendering: pixelated`: nenhum pixel borrado, nenhuma escala fracionária.
- **O campo** tem 960 × 560 px nativos (maior que a tela: a câmera anda), piso verde com poucas manchas largas e
  pontilhadas, tufos, pedrinhas e flores raras; fora dele, um gramado mais escuro com moitas.
- **Os combatentes** (`tela/sprites.js`, grade de letras desenhada à mão; a folha em `tela/folha.html`): soldado,
  arqueiro e porta-estandarte em 13 × 13 (o corpo tem uns 6 × 11), veterano com escudo maior, campeão em 19 × 17, os
  heróis em 17 × 15 com contorno escuro. Poses: parado, duas passadas, preparo, golpe, recuo; caído e os quatro giros
  do arremesso saem do recuo girado 90°. As mãos são pontinhos de pele (como as figuras de cena). Sem contorno nos
  soldados (a sombra no chão os separa do piso); o **herói** tem contorno, a cor mais clara do campo, um **anel
  dourado** no chão e é **desenhado por cima de todos** (decisão: nunca some na multidão; troca uma imprecisão de
  profundidade pela leitura).
- **O que fica recolhido:** o registro e o diagnóstico (Tab). Na tela ficam só a ficha do herói (vida e recurso), o
  placar com as ordens, as quatro habilidades e uma faixa curta de avisos.

## 4. Controle direto e o compromisso dos golpes

- **Andar:** WASD com aceleração de 1000 px/s² e freio de 1400 px/s²: a velocidade máxima (72 px/s no Guerreiro) em
  5 passos (83 ms) e a parada em 4 (67 ms). O herói olha para o mouse; durante um golpe, para a direção do golpe.
- **Mirar:** cada golpe sai na direção do mouse (arco, faixa) ou no ponto do mouse limitado ao alcance (círculo,
  parede). Nada de procurar alvo nem de clicar em soldado.
- **O compromisso, igual para todos:** golpe forte **prende os pés na preparação** (0,12 a 0,2 s) e não se cancela;
  **depois do contato**, andar ou outra habilidade cortam a recuperação. O básico deixa andar mais devagar (60% no
  Guerreiro, 75% no Mago) e é cortado por qualquer habilidade a qualquer momento.
- **Comando guardado:** uma habilidade apertada durante outra ação espera até 0,2 s e sai quando puder.
- **Pausa** (`P`/`Esc`): o campo para; as ordens funcionam pausado; as opções ficam ali. O jogo não depende dela.

## 5. Os dois kits

Os números estão em `tela/conteudo.js` (e a tela os lê de lá).

| Herói | Botão esquerdo | Botão direito | Espaço | Q |
|---|---|---|---|---|
| **Guerreiro** (vida 260, Fúria 0 a 100) | **Corte**: arco de 110°, 22 px, dano 3; o 3º corte seguido (até 0,9 s) é o **arremate**: 130°, 26 px, dano 8, arremessa | **Varredura**: prepara 0,2 s, arco de 220°, 32 px, dano 13 (derruba soldado), empurra e atordoa; recarga 6 s | **Investida**: 100 px em 0,2 s sem receber dano, joga para os lados quem está no caminho (dano 4), o campeão a segura; recarga 6 s | **Salto Esmagador**: até 130 px, 0,42 s no ar sem receber dano, círculo de 44 px, dano 24, arremessa e atordoa; custa 100 de Fúria (+1 por acerto, +1,5 por derrubado) |
| **Mago** (vida 170, mana 100, +7/s) | **Faísca**: projétil rápido até 175 px, dano 4 no primeiro que encontra | **Bola de Fogo**: prepara 0,18 s, explode no ponto do mouse (até 180 px), círculo de 24 px, dano 13, arremessa; o chão queima 2 s (5/s); 30 de mana, recarga 1,5 s | **Piscar**: reaparece até 95 px; onde estava, uma onda de 28 px empurra e atordoa (dano 3); recarga 6 s | **Muralha de Fogo**: parede de 96 px no ponto do mouse, de lado para o herói, 5 s; desvia os inimigos e queima 14/s; 40 de mana, recarga 9 s |

Por que assim: o Guerreiro tem o ritmo **entrar, varrer, sair** (a Investida para abrir ou fugir, a Varredura como a
grande decisão a cada 6 s, a Fúria guardando a virada); o Mago, **mirar no grupo, manter distância, mudar o terreno**
(a mana limita a Bola a umas três seguidas e depois uma a cada ~4 s; a Muralha divide o exército; o Piscar resolve
quem chegou perto). Os golpes fortes derrubam soldados comuns de uma vez; o veterano (32 de vida) aguenta um golpe forte
e mostra a barra por 1,5 s; o campeão (220) leva, recua pouco e mostra o atordoamento.

## 6. O impacto

| Parte | Como ficou |
|---|---|
| Antecipação e direção | A pose de preparo do herói e a **área no chão** (o arco, o círculo, a faixa) durante a preparação; no voo do Salto, o círculo de chegada; no voo da Bola, o círculo do alvo enchendo |
| Contato | No quadro do contato, todos os de dentro da forma levam o golpe de uma vez; o corte desenha o arco varrendo (borda branca, preenchimento claro) por 90 a 160 ms |
| Reação do alvo | Clarão branco (60 a 90 ms) e o alvo **congela** 45 a 70 ms (a pausa local), depois recua na direção do golpe; golpe forte atordoa e interrompe a preparação (o campeão mostra "interrompido") |
| Arremesso e deslocamento | Quem **morre** num golpe forte vira efeito: voa na direção do impacto com uma parábola, gira de 90 em 90°, quica uma vez com poeira e fica no chão como marca. Quem **vive** é empurrado de verdade (a velocidade de empurrão entra na simulação e afeta a luta: abre espaço, tira do alcance) |
| Morte e queda | Morte fraca: cai no lugar e escorrega um pouco. Arremessado: voa 20 a 45 px. O corpo vira marca no chão, sem cor e escuro, para não se confundir com quem está de pé |
| Fogo, corte e poeira | Brasas que sobem e caem, fumaça fraca (opacidade ≤ 32%), anel de explosão que se abre, a marca queimada discreta; o clarão cheio da explosão dura ~60 ms |
| Pausa de impacto | Só nos golpes fortes: Varredura 45 ms (+8 por derrubado, até 90), Bola 50 (+6, até 85), Salto 100, arremate 25. **Teto de 100 ms e 150 ms de intervalo** entre uma pausa e outra: muitos golpes juntos não travam a tela. Pode ser desligada |
| Tremor | Trauma ao quadrado (seção 1), proporcional ao golpe e ao número de derrubados, com um empurrão curto na direção do golpe. Varredura ~0,26, Bola ~0,30, Salto 0,70, golpe do campeão no herói 0,35. Intensidade 0 a 150%; em 0 a câmera não se mexe, e a força continua legível pela área, pelo arremesso, pelo clarão e pelo "N derrubados" |
| Som | Sintetizado (ruído filtrado e osciladores), volume e mudo; cada som tem intervalo mínimo (doze acertos não viram doze estalos) |

## 7. Tropas, ordens, movimento e ocupação

- **Papéis:** soldado (perto), veterano (perto, resistente), arqueiro (longe: mantém ~105 px, recua se alguém chega a
  46 px, a flecha cai num ponto e pode errar), porta-estandarte (atrás da linha, aura de 70 px: +30% de dano e ataque
  15% mais rápido; derrubado, abala quem está a 120 px por 2 s), campeão (golpe de machado anunciado, interrompível).
- **Escolha do alvo:** a cada 0,3 a 0,6 s; custo = distância + 22 por atacante que já está no alvo; cada alvo tem
  **vagas** (3 num soldado, 7 no herói e no campeão). O excesso procura outro: o grupo envolve em vez de empilhar.
  Chegando perto, cada um abre um pouco para o seu lado. Alvo morto ou fora da ordem: escolhe de novo na hora.
- **Ordens** (teclas 1, 2, 3, também pausado): **Acompanhar** (luta só perto de si ou do herói; sem inimigo, um anel
  solto em volta dele, os arqueiros atrás), **Atacar** (o mais perto, em qualquer lugar), **Defender aqui** (no ponto do
  mouse; luta a até 85 px dali e larga quem passa de 120 px; a bandeira fica no chão).
- **Separação:** grade espacial de 12 px; cada par sobreposto se afasta pela massa. **Regra deliberada do herói:** os
  **aliados abrem caminho** (o herói não perde velocidade por eles); os **inimigos são corpo sólido**: o herói empurra
  pesando como 2,5 soldados e anda mais devagar a cada inimigo encostado (até 45% da velocidade). Atravessa uma linha
  fina apanhando, não a multidão inteira; para isso existe a Investida (e, no ar, o Salto).
- **Sem alvo:** aliados voltam para a ordem; inimigos marcham para o meio do exército aliado; na fuga, correm para a
  borda direita e saem.

## 8. A batalha

Sempre a mesma (semente fixa), para comparar os dois heróis. **Normal:** 42 aliados (30 soldados, 12 arqueiros) e o
herói contra 94 inimigos: a **primeira leva** (28 soldados, 14 veteranos, 12 arqueiros e o porta-estandarte) espera em
formação 2,5 s (ou até ser atacada); a **segunda** (20 soldados, 10 veteranos, 8 arqueiros e o **campeão**) entra pela
direita aos 30 s ou quando a primeira cai a 20%. Com 20% dos inimigos de pé (depois da segunda leva), o resto foge e
vem a **vitória**; o herói caído é a **derrota**. `R` recomeça na hora. **Maior:** o dobro de cada grupo (≈ 270 no
campo, dois campeões e dois porta-estandartes).

O fim mostra: derrubados pelo herói e pelas tropas, os que fugiram, as perdas, o maior golpe e cada habilidade (usos,
atingidos, derrubados).

## 9. Verificação: funcionamento

`node --test testes/sim.test.mjs` (14 testes; `testes/test_campo.py` os roda e confere que o jogo não carrega nada da
pasta):

| O que se pediu conferir | Como foi conferido |
|---|---|
| Área mostrada = alvos atingidos | Varredura, Salto, Bola e Piscar contra uma grade de veteranos parados: o conjunto atingido é exatamente o conjunto dentro da forma. Por construção, o desenho pinta cada pixel testando a mesma função `dentro` |
| Dano aplicado uma vez | Varredura, Salto, Bola e Investida: cada atingido perde exatamente o dano da ação (o fogo do chão começa 0,25 s depois, de propósito) |
| Mortes simultâneas | Um Salto derruba 15 ou mais no mesmo passo; a lista, o placar e as estatísticas batem; nenhum aliado continua mirando um morto |
| Unidades sem alvo | Sem inimigos, as tropas voltam ao ponto de defesa e depois acompanham o herói; nada trava nem vira NaN |
| Grupos concentrados | 80 soldados no mesmo ponto se espalham em 2 s, sem sobreposição maior que 1,5 px |
| Herói entre aliados e inimigos | Atravessa 40 aliados sem perder velocidade; contra um bloco de inimigos, anda menos de 70% e não fica preso |
| Resposta | Acelera em até 5 passos, para em até 4; o golpe começa no passo do aperto; o comando guardado sai depois do contato; um aperto que não pode sair em 0,2 s se perde |
| Compromisso | Andar na preparação não move; depois do contato, andar corta a recuperação |
| Ameaça | O campeão anuncia o golpe; a Varredura o interrompe; o Corte, não |
| Repetição | A mesma semente e a mesma entrada dão a mesma batalha |
| A batalha termina | Com o jogador automático "médio", os dois heróis vencem e as tropas derrubam inimigos; sem o herói, as tropas perdem |
| Pausa, retomada, reinício | No navegador (`ferramentas/medir.mjs pausa`): o tempo de jogo não anda pausado, a ordem funciona pausado, retoma, `R` volta ao começo, `Tab` abre o registro |

**Resposta medida no navegador** (`medir.mjs resposta`, teclado e mouse de verdade): ver a seção 11.

## 10. Verificação: sensação

**Os vídeos** (1280×720, o jogador automático forte, a batalha inteira ou quase, abrem no navegador):
`ferramentas/prototipos/etapa8-campo/videos/guerreiro-1280x720.webm` (30 s), `mago-1280x720.webm` (30 s) e
`guerreiro-maior-1280x720.webm` (22 s, a batalha maior). Mostram os encontros dos grupos, a Varredura, o Salto e a
Investida, a Bola de Fogo e a Muralha, a chegada da segunda leva e o fim. As sequências quadro a quadro
(`capturas/sequencia-varredura.png`, `-salto.png`, `-bola.png`) mostram 30 quadros seguidos a partir da preparação, com
o tempo de jogo e os quadros da pausa de impacto marcados.

O que eu observei nas sequências, nas capturas e nos vídeos:

- **A Varredura num grupo** lê bem: a área aparece branca no chão durante a preparação, o arco varre, a tela para ~90 ms
  e os corpos saem voando em leque na direção do golpe; "14 derrubados" aparece em cima.
- **A Bola de Fogo** lê bem: o círculo do alvo enche durante o voo (0,15 a 0,4 s), o clarão cobre a área por um
  instante, o anel abre e as brasas e a fumaça somem antes de esconder a luta.
- **O Salto** mostra o herói subindo (até 22 px) com a sombra no chão e o círculo de chegada.
- **Ajustes feitos depois de ver:** os corpos arremessados voavam 100 a 200 px e ficavam no chão com as cores vivas,
  espalhados pelo campo como se fossem soldados de pé (agora voam 20 a 45 px e ficam apagados e escuros); o Corte
  empurrava tanto que os soldados nunca acertavam o herói (o empurrão do básico caiu de 60 para 25); as marcas de fogo eram manchas pontilhadas grandes (ficaram discretas); as barras
  de vida dos veteranos poluíam o meio da luta (só por 1,5 s depois do golpe, menores); os arqueiros inimigos se
  espalhavam num anel em volta do Mago (ficam atrás da própria linha); a Bola demorava a chegar (mais rápida); a
  primeira leva esperava parada a explosão (atacada, avança); a ordem dada pausado só aparecia ao continuar; o painel
  da pausa cobria o exército (foi para o canto); o custo das habilidades do Mago saía cortado.
- **O que só o Jean responde:** se o peso do golpe está certo com e sem tremor; se a pausa de impacto ajuda ou atrapalha;
  se o herói se lê no meio da multidão; se as tropas parecem úteis; se dá vontade de repetir (seção 14).

## 11. Desempenho

**Condições:** Windows 10 do Jean (DESKTOP-4KMKFO5), Chromium 130 do Playwright **sem janela** (o canvas desenhado na
CPU), 31/10/2026; cada linha é uma batalha com o jogador automático forte, medida por 20 s a partir do começo (o
contato, as áreas e as mortes em massa estão dentro). 60 quadros por segundo é o teto do `requestAnimationFrame`.
Os números brutos estão em `capturas/medicao.json` (`node ferramentas/medir.mjs desempenho`).

| Janela | Tropas | Herói | Combatentes (máx.) | Partículas (máx.) | Qps | Quadro p95 / máx. | Simulação média / p95 | Desenho média / p95 |
|---|---|---|---|---|---|---|---|---|
| 1280×720 (2×) | normal | Guerreiro | 98 | 52 | 60 | 16,7 / 16,8 ms | 0,18 / 0,4 ms | 1,0 / 2,2 ms |
| 1280×720 (2×) | normal | Mago | 98 | 78 | 60 | 16,7 / 16,8 ms | 0,25 / 0,5 ms | 1,1 / 1,7 ms |
| 1280×720 (2×) | maior | Guerreiro | 195 | 134 | 60 | 16,7 / 16,8 ms | 0,43 / 0,9 ms | 2,0 / 3,4 ms |
| 1280×720 (2×) | maior | Mago | 195 | 90 | 60 | 16,8 / 16,8 ms | 0,25 / 0,5 ms | 1,5 / 2,3 ms |
| 1920×945 (3×) | normal | Guerreiro | 98 | 61 | 60 | 16,7 / 16,8 ms | 0,17 / 0,4 ms | 1,0 / 2,2 ms |
| 1920×945 (3×) | normal | Mago | 98 | 78 | 60 | 16,7 / 16,8 ms | 0,18 / 0,4 ms | 0,8 / 1,3 ms |
| 1920×945 (3×) | maior | Guerreiro | 195 | 124 | 60 | 16,7 / 16,8 ms | 0,31 / 0,7 ms | 1,5 / 3,0 ms |
| 1920×945 (3×) | maior | Mago | 195 | 90 | 60 | 16,7 / 16,8 ms | 0,21 / 0,4 ms | 1,2 / 1,7 ms |

(Os 98 e 195 são a primeira leva com os aliados; a segunda entra depois, até ≈ 137 e ≈ 270.) No Node, o passo da
batalha maior custa em média 0,1 a 0,25 ms (`ferramentas/simular.mjs`; um teste exige menos de 4 ms).

**Resposta** (`medir.mjs resposta`, teclado e mouse de verdade no Chromium): em tempo de jogo, andar começa no primeiro
passo depois da tecla (16,7 ms), chega à velocidade máxima em 83 ms e para em 67 ms; a Varredura começa no primeiro
passo depois do clique e o contato vem 217 ms depois (os 0,2 s de preparo); a Investida começa no primeiro passo. No
relógio, o primeiro quadro depois de uma **tecla** chega 85 a 95 ms depois, porque o Playwright trava a página uns
85 ms ao injetar a tecla (medido: não há quadro nesse intervalo); depois de um clique, 15 a 19 ms.

**Limite técnico × leitura:** o desempenho não é o limite: na batalha maior, simulação e desenho somam uns 4 ms dos
16,7 ms de um quadro, sem quadro perdido. O limite que apareceu é de **leitura**: na maior, a massa do meio vira uma
mancha azul e vermelha e as barras dos veteranos se acumulam (`capturas/maior-*.png`); e de **comportamento**: os
arqueiros inimigos que sobram se espalham pelo campo, e o grupo denso da primeira leva é o alvo óbvio.

## 12. Limitações conhecidas

- **Arte provisória** em grade de letras no código, sem fonte no Aseprite; poucas poses; o veterano e o campeão são
  manchas mais largas; o herói desenhado por cima de todos (decisão de leitura, seção 3).
- **Equilíbrio de teste:** com o jogador automático, a batalha normal acaba em 25 a 30 s e o herói derruba 55 a 75 dos
  94; as tropas derrubam 13 a 25 e perdem 0 a 12 dos 42; o Guerreiro sofre 37 a 57 de dano, o Mago 0 a 6 (ele
  mantém distância e pisca). Sem o herói, as tropas perdem em ~40 s derrubando ~9. Ou seja: o herói é forte demais
  contra um jogador automático preciso, e as tropas pesam pouco. Uma pessoa jogando pela primeira vez deve demorar
  mais e apanhar mais, mas isso não foi medido. Os números estão todos em `conteudo.js`.
- **A primeira leva em formação** ainda é o grupo mais denso da luta: uma Bola ou uma Varredura bem posta ali derruba
  10 a 15 de uma vez (é a "boa oportunidade" mais óbvia; atacada, a leva avança).
- **Sem obstáculos no campo** (nem rios, nem pedras grandes): o movimento não precisa de busca de caminho; um campo com
  obstáculos pediria campo de fluxo ou caminhos.
- **Inimigos sem inteligência de grupo:** não flanqueiam, não recuam juntos, não protegem o porta-estandarte; o campeão
  só prioriza o herói.
- **Fogo amigo desligado:** as áreas do herói não pegam aliados (o tático pegava). Se for preciso, é uma regra a mais.
- **Os vídeos e o desempenho usam o jogador automático** (`robo.js`), que preenche a mesma entrada do teclado e do
  mouse; não é uma pessoa jogando.
- **Sons sintetizados** simples; nenhum arquivo de áudio.

## 13. O que esta direção mudaria no jogo (não implementado)

Se o campo livre seguir, quase tudo do combate muda; o resto do jogo (vila, mapa, eventos, cenas, inventário) pode
ficar, com pontos de contato:

- **A luta vira uma tela própria** (como uma batalha separada em Mount & Blade): a exploração continua por texto e
  cenas; um encontro abre o campo. O motor Python passaria a mandar o encontro (quem, quantos, o terreno) e receber o
  resultado (vida, mortes, espólio); a luta em si roda no navegador. O **gabarito** (24 partidas com semente) precisaria
  de uma forma de jogar a luta sem tela (o `sim.js` já roda no Node; seria portá-lo ou chamá-lo).
- **Habilidades e talentos:** o catálogo de 45 habilidades e os talentos foram pensados para turnos (porcentagem do
  Poder, turnos de duração, cadeias). Em tempo real, cada um vira forma, alcance, preparação, recarga e custo; os
  estados viram segundos; muitos talentos de número continuam, os de ordem de turno somem. O X1 e o tático ajudam a
  escolher quais caminhos (Berserker, Piromante) vale converter primeiro.
- **Comitiva:** Odette, Morel e Yara viram unidades especiais no campo (com IA e talvez uma ordem própria), ou heróis
  controláveis em troca. Decisão do Jean.
- **Inimigos do Vale:** as 17 famílias viram tipos de tropa e ameaças com padrões no chão (o campeão é o modelo:
  anunciar, punir, ser interrompido); os chefes viram encontros com fases.
- **Equipamento e atributos:** continuam, convertidos em vida, dano, velocidade, recarga, alcance; a ficha precisa
  dizer isso em números do motor.
- **Arte:** um conjunto de sprites por tipo (seis poses é pouco para o jogo final), efeitos por elemento, os cenários
  de batalha por região; o pipeline do Aseprite das cenas se aplica.
- **Dificuldade, acessibilidade e ritmo:** a pausa com ordens, a velocidade do jogo, o tremor e a pausa de impacto como
  opções do jogo; o equilíbrio medido com jogadores automáticos de níveis diferentes.

## 14. O que avaliar jogando

Abra `ferramentas/prototipos/etapa8-campo/demo.bat` (o topo diz "Campo Livre 1").

1. **O critério:** andar e acertar uma Varredura ou uma Bola num grupo foi fluido, legível e satisfatório? Deu vontade
   de repetir?
2. **Peso:** o golpe forte parece forte? Teste com o tremor em 100%, em 50% e desligado, e com a pausa no impacto
   ligada e desligada.
3. **Controle:** algum momento pareceu atrasado ou travado? A preparação da Varredura (0,2 s presos) incomoda ou dá
   peso?
4. **Leitura:** você acha o herói na multidão? As áreas no chão e o anúncio do campeão se leem sem pensar?
5. **Tropas:** elas parecem úteis? As ordens (1, 2, 3) mudaram alguma coisa que você quis? Faltou alguma?
6. **Guerreiro contra Mago:** qual sensação está mais perto do jogo que você quer?
7. **Escala:** a batalha normal é o tamanho certo? A maior (opção "Tropas") lê ou vira ruído?
