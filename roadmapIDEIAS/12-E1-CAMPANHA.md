# 12 — E1: campanha, cronologia, protagonista e transição

Proposta de design, 10/10/2026, sobre a versão 1.47.1 (commit `622b1b6`). Complementa [11-E1-REGIAO-INICIAL.md](11-E1-REGIAO-INICIAL.md). Não altera a história nem o jogo. Legenda: **[existe]** conferido no código; **[hipótese]** aceita por Jean como hipótese de trabalho; **[proposta]** depende de aprovação.

## 1. Cronologia: Fenda antiga e reabertura recente

### A hipótese avaliada

Uma Fenda original antiga, selada, e uma reabertura recente na catedral, presenciada por Odette.

### Compatibilidade com o conteúdo existente

| Trecho | Onde | Com a hipótese |
|---|---|---|
| "Há cem anos uma Fenda se abriu sob a catedral, e desde então o reino apodrece devagar" | `jogo.py:212` | **Compatível** como Fenda original; "apodrece devagar" vira o vazamento lento da cicatriz. Falta citar a reabertura |
| Origem do vilão: "que abriu a Fenda há cem anos" | `dados.py:421` | Compatível para um vilão antigo |
| Origem do vilão: "o bispo que abriu as catacumbas da catedral procurando Deus" | `dados.py:420` | **Combina muito** com a reabertura |
| Odette desaprova ganância: "Foi por ouro que o bispo vendeu as relíquias. Lembra do que veio depois?" | `comitiva/catalogo.py` | **Combina muito**: relíquias vendidas = selo rompido = reabertura |
| Ficha da Odette: "Fugiu da catedral na noite em que a Fenda se abriu" | `comitiva/catalogo.py:12` | Conflito só literal: vira "se reabriu" |
| Confissão: "Antes do chão abrir… Tranquei a porta da cripta… Os acólitos estavam lá dentro" | `eventos/comitiva.py:95` | Compatível: o chão abriu de novo |
| Mãe de Thomas ainda acende vela pelo filho | `eventos/comitiva.py` | Exige evento recente: compatível |
| Yara: "Desde que a Fenda abriu, eu ouço uma voz… Ulook" | `eventos/comitiva.py:457` | Yara é jovem: só funciona com a reabertura. Conflito literal ("abriu") |
| Morel: Ponte de Varn contra crias do Vazio; Theodore "procurou por dois invernos" | `eventos/comitiva.py` | Compatível com reabertura há 2–4 anos |
| Veterano de uma perna: "Lutei na Primeira Fenda" | `eventos/classe.py:101` | **Conflito real com "cem anos"**: ninguém vivo lutou há cem anos. Compatível se a Primeira Fenda estiver na memória viva |
| "Meu avô enfrentou {guardião} e voltou vivo" | `eventos/vila.py:30` | Compatível com guardiões antigos; forçado com cem anos, natural com duas gerações |
| Três Sigilos "que selam o caminho" | `jogo.py:215` | Compatível: os Sigilos viram pedaços do selo antigo |

### Conclusão

A hipótese funciona. Ela explica melhor o que já está escrito do que uma Fenda única: a venda das relíquias, a idade da Yara, a mãe de Thomas, a Ponte de Varn e o termo "Primeira Fenda". O único conflito real é o **número "cem anos"** com o veterano vivo, e com o avô de forma menos grave.

### Recomendação [proposta]

| Quando | O quê |
|---|---|
| ~60 anos atrás (duas gerações) | **A Primeira Fenda** abre sob o lugar onde depois ergueram a catedral. Guerra curta e terrível. O selo é feito em três **Sigilos**, guardados em três lugares. A catedral é construída sobre a cicatriz e guarda as relíquias que mantêm o selo |
| Décadas seguintes | O reino "apodrece devagar": a cicatriz vaza; criaturas deformadas viram os guardiões. Medo e caça às bruxas (é a época da Ilse, na região 1) |
| ~3 anos atrás | **A Reabertura.** O bispo vende as relíquias. A cripta se abre. Odette ouve a voz, tranca a porta e foge. A voz começa a falar com a Yara. As crias do Vazio descem; a Ponte de Varn cai |
| Agora | A campanha |

Por que 60 e não 100 anos: com 60, a Primeira Fenda ainda está na **memória viva**. O veterano lutou nela, o avô enfrentou um guardião e a Vó Berta era menina quando afogaram a Ilse. A região 1 depende disso: a vila repete um crime de que ainda há testemunha. Com 100 anos, a frase do veterano teria que mudar e a região perderia essa testemunha.

**Alternativa**, se Jean preferir manter "cem anos": a estrutura de dois tempos continua igual. Nesse caso, o veterano "lutou na noite da Reabertura" e a testemunha da Ilse passa a ser um diário, não uma pessoa.

### Ulook e o vilão gerado

Hoje o vilão é sorteado entre 8 títulos e 5 origens (`dados.py:411–422`), mas a Yara sempre cita **Ulook** [existe]. Numa campanha escrita isso precisa de uma explicação só.

Proposta:
- **Ulook** é a coisa do outro lado, a voz.
- **O bispo**, hoje o Arcebispo Profanado, é o rosto humano: quem vendeu as relíquias e quem procura os Sigilos.

Os dois títulos e as origens que combinam já existem no catálogo.

Nada disso muda a história agora. A correção do texto do jogo depende da aprovação de Jean e fica em tarefa própria.

## 2. Protagonista: motivação local e concreta [proposta]

**O herói volta para casa.**

- A irmã, **Marta**, curandeira do Vau do Turvo, escreve: "A febre voltou. Não venha." O herói vem.
- O motivo inicial é pessoal e pequeno: salvar a irmã e a vila onde cresceu.
- Uma linha por classe explica por que o herói saiu de lá e já prepara a campanha:
  - **Guerreiro:** foi recrutado pelo duque. Ouviu falar da Ponte de Varn (região 2, Morel).
  - **Arqueiro:** caçava nesse vale e conhece as trilhas. Partiu como batedor de caravanas.
  - **Mago:** foi mandado à escola da catedral. Estava longe na noite da Reabertura e sabe quem era o bispo (Odette).

O motivo cresce aos poucos:
1. **Região 1:** "minha irmã tem febre" vira "a água passa por um selo rachado".
2. **Fim da região 1:** a Ilse, ao entregar o Sigilo, diz que **outra pessoa perguntou por ele**: homens com a marca do bispo. Os cultistas da sacristia confirmam.
3. **Região 2:** o selo não é um problema local; os três lugares estão sangrando.
4. **Região 3:** a voz da Yara sabe o nome do herói.
5. **Final:** quem juntar os três Sigilos abre a catedral. O herói precisa chegar lá primeiro.

O herói não é escolhido nem profetizado [existe no tom atual: "Não houve profecia"]. Ele continua porque cada resposta cria um problema mais perto de casa.

## 3. Arco da campanha: início, meio e fim [proposta]

A estrutura existente já é "três guardiões com Sigilos, depois a Cidadela, chefe no nível 11" (`balanceamento.py`, `ANTAGONISTA_NIVEL = 11`) [existe]. A proposta é dar uma região escrita a cada Sigilo, em vez de inventar outra estrutura.

| Ato | Região | Níveis | Conflito local | Companheiro em destaque | Sigilo |
|---|---|---|---|---|---|
| **I — Início** | Vale do Turvo | 1–4 | A febre e a bruxa afogada | Yara (encontro), Odette (Caspar) | 1º |
| **II — Meio** | Terras de Varn (planície/montanha) | 5–7 | O duque que não mandou a coluna; desertores dos Cães de Ferro; uma cidade com a mãe de Thomas | Morel (Theodore), Odette (mãe de Thomas) | 2º |
| **II — Meio** | Brejo das Pedras Negras (pântano/ruínas) | 7–9 | Seguidores do bispo; o círculo de pedras negras | Yara (voz de Ulook, círculo negro) | 3º |
| **III — Fim** | Catedral Partida (a Cidadela) | 10–11 | O bispo e Ulook | Os três, conforme os caminhos | — |

Ordem das regiões do Ato II: fixa na primeira versão, porque o nível dos inimigos depende do lugar. Escolher a ordem é melhoria futura.

**Revelação do meio** (fim da região 2): os Sigilos são chave e selo ao mesmo tempo. Juntá-los abre o caminho para a catedral, que é o que Ulook quer. O herói não tem como devolvê-los. A pergunta deixa de ser "como entrar" e passa a ser "o que fazer lá dentro".

### Como o jogo pode terminar

Dois finais principais e uma variante. Os epílogos vêm das decisões de cada região, não de um final por combinação.

1. **Selar.** Os três Sigilos refazem o selo. Alguém precisa ficar como tranca:
   - o próprio herói;
   - Odette, se seguiu o caminho penitente;
   - Yara, se se libertou da voz.

   Final agridoce.
2. **Romper.** Destruir os Sigilos e o selo. A catedral desaba sobre a Fenda; Ulook perde a porta, e a voz da Yara e certas magias também se calam. Custo coletivo, ninguém fica para trás.
3. **Variante sombria (opcional).** Tomar o lugar do bispo. Só existe se o jogador tiver se aproximado do Vazio, por exemplo com a Yara em "vazio" ou ouvindo os sussurros. Pode ser cortada.

**Epílogos:**
- Vau do Turvo (fogueira ou memorial);
- Terras de Varn (Cães de Ferro e duque);
- Brejo (o círculo);
- Odette, Morel e Yara, cada um pelo seu caminho [os caminhos existem: `penitente`/`calada`, `redencao`/`capitao`/`adiado`/`quites`, `liberta`/`vazio`];
- Marta.

**Aliados no confronto final:** a ideia guardada em `docs/ROADMAP.md` ("poucos aliados, ganhos por arcos inteiros, que aparecem na luta") cabe aqui. Os Cães de Ferro vêm se o Morel teve o caminho `adiado` ou `redencao`. É opcional e fica para o Ato III.

**Tamanho:** quatro regiões, a última curta. A duração real só se estima depois de jogar a região 1 (E9).

## 4. Derrota na campanha [hipótese]

Hipótese de trabalho aceita por Jean, sem decisão definitiva e sem autorização para mudar o padrão atual:
- **Campanha:** cair em combate leva ao resgate, como no modo brando (`jogo.py:248`): perde parte do ouro e dois dias. Na região 1, quem resgata é a Marta.
- **Masmorra:** salas vencidas continuam vencidas; a guardiã volta inteira.
- **Hardcore:** opção explícita na criação da campanha.
- **Texto:** o prólogo e a interface precisam dizer o modo de verdade. Hoje o prólogo sempre diz "a morte é permanente" (ver [13-PENDENCIAS-FORA-DA-CAMPANHA.md](13-PENDENCIAS-FORA-DA-CAMPANHA.md)).

Pontos que dependem de Jean antes da E9: o custo exato; se o resgate muda alguma cena; e saves e pontos de retorno no hardcore.

## 5. Transição do procedural [hipótese de trabalho, com proposta de regras]

Jean pediu: preservar o funcionamento atual até a campanha ser validada, sem virar obrigação de manter duas experiências completas.

**Proposta de regras:**

1. **Duas portas de entrada, um motor.** A campanha começa por um novo início de partida. O procedural continua como está. Combate, itens, comitiva, sobrevivência e interface são os mesmos.
2. **Procedural congelado.** Recebe só correção de defeito. Nenhum conteúdo novo da campanha precisa funcionar no procedural, e nada é portado para ele.
3. **Gabarito como cerca.** As partidas atuais do gabarito são procedurais. Mudança em código compartilhado feita para a campanha precisa manter o gabarito idêntico, ou explicar a diferença como mudança de propósito. A campanha ganha cenários próprios de teste.
4. **Conteúdo novo marcado.** Cenas da campanha só disparam na campanha. Eventos aleatórios existentes podem rodar nas duas, filtrados por lugar e nível.
5. **Decisão depois da E9.** Com a região validada, Jean escolhe: aposentar o procedural ou mantê-lo congelado como "modo livre", sem novos recursos. Recomendação: aposentar quando a campanha cobrir o jogo do começo ao fim (E11). Até lá, congelado.

O que não vira obrigação:
- legado entre partidas (túmulo e estátua);
- nomes e vilão sorteados;
- mapa gerado.

Esses recursos continuam só no procedural. A campanha não os herda até alguém decidir que precisa.

## 6. O que precisa da aprovação de Jean

| # | Ponto | Recomendação |
|---|---|---|
| 1 | Cronologia | Primeira Fenda há ~60 anos e Reabertura há ~3 anos, em vez de "cem anos" |
| 2 | Ulook e o vilão | Ulook é a voz; o bispo (Arcebispo Profanado) é o rosto humano; vilão fixo na campanha |
| 3 | Protagonista | Volta para casa; irmã Marta; uma linha de passado por classe |
| 4 | Região 1 | Vale do Turvo, conforme o documento 11 |
| 5 | Soluções | Destruir ou Dar descanso, e as consequências da tabela |
| 6 | Estrutura | Uma região escrita por Sigilo, mais a Catedral |
| 7 | Finais | Selar ou Romper; a variante sombria é opcional |
| 8 | Tempo | Sem prazo duro na região 1 |
| 9 | Regras da transição | As cinco acima |

Não precisa ser decidido agora:
- raças e origens (E8);
- preparação de habilidades e transformações (E6);
- facções (só se a região 2 pedir);
- duração exata (depois da E9);
- detalhes do custo da derrota (E9).
