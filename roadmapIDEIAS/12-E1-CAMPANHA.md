# 12 — E1: campanha, cronologia, Sigilos, protagonista e transição

Revisão 2 — 10/10/2026, sobre a versão 1.47.1. Complementa [11-E1-REGIAO-INICIAL.md](11-E1-REGIAO-INICIAL.md). Não altera a história nem o jogo.

Legenda:
- **[existe]**: conferido no código.
- **[hipótese]**: aceita por Jean como hipótese de trabalho.
- **[proposta]**: depende de aprovação.

**Revisão 2:**
- linha do tempo para testar a cronologia;
- lógica dos Sigilos;
- ganhos e limites do laço do herói com Marta;
- decisões separadas pelo momento em que precisam ser fechadas.

## 1. Linha do tempo para testar a cronologia [proposta]

Hipótese: uma Fenda original antiga e uma reabertura recente presenciada por Odette. A coluna "Origem" diz se o fato já está no jogo ou se é sugestão.

| Quando (antes de agora) | Acontecimento | Origem |
|---|---|---|
| ~60 anos | **A Primeira Fenda** se abre sob a catedral. Guerra curta e terrível | **Fato** no jogo: abertura sob a catedral (`jogo.py:212`) e o termo "Primeira Fenda" (`eventos/classe.py:101`). **Sugestão:** 60 anos em vez de "cem anos" |
| ~58 anos | A Igreja fecha a Fenda: relíquias no centro (cripta da catedral) e três Sigilos levados a três lugares, cada um com um guardião | **Sugestão.** Base existente: os Sigilos "selam o caminho" (`jogo.py:215`) |
| ~55 anos | O Vau do Turvo afoga Ilse, guardiã da capela, como bruxa. Berta tem 8 anos | **Sugestão** (região 1) |
| décadas | O selo vaza devagar; os guardiões se deformam. O "avô" de alguém enfrenta um guardião e volta vivo | **Fato:** "o reino apodrece devagar" (`jogo.py:212`), "guardiões, deformados pela Fenda" (`jogo.py:215`), "Meu avô enfrentou…" (`eventos/vila.py:30`) |
| ~3 anos | **A Reabertura.** O bispo vende as relíquias; a cripta se abre; Odette ouve a voz, tranca a porta com 40 acólitos dentro e foge. A voz começa a falar com Yara | **Fato:** a venda das relíquias (fala da Odette, `comitiva/catalogo.py`), a cripta e os acólitos (`eventos/comitiva.py:95`), a voz de Ulook (`eventos/comitiva.py:457`). **Sugestão:** o nome "Reabertura" e trocar "se abriu"/"abriu" por "reabriu" na ficha da Odette e na fala da Yara |
| ~2–3 anos | Crias do Vazio; a Ponte de Varn cai; Morel recua | **Fato:** Ponte de Varn, crias do Vazio, Theodore procura Morel "há dois invernos" (`eventos/comitiva.py`) |
| ~1 ano | Anselmo represa o riacho e abre o canal; o poço seca; surge a Fonte Nova | **Fato:** poço seco e moleiro (texto da Yara). **Sugestão:** canal, cripta e Fonte Nova |
| este ano | Febre no Vau; dois pescadores levados por afogados | **Fato:** "as crianças têm febre" (texto da Yara). **Sugestão:** o resto |
| agora | A carta de Marta | **Sugestão** |

### Testes de idade

| Personagem | Com 60 e 3 anos | Com "cem anos" |
|---|---|---|
| Veterano que lutou na Primeira Fenda (fato) | Lutou com ~16; tem ~76 hoje | Teria ~116: impossível |
| Vó Berta (sugestão) | 8 anos então; ~63 hoje | ~108: precisaria virar um diário |
| "Avô" que enfrentou um guardião (fato) | Uns 40 anos atrás: natural | Possível, mas forçado |
| Odette, irmã de vigília na Reabertura (fato) | Adulta há 3 anos: natural | Natural (a reabertura não muda) |
| Mãe de Thomas viva (fato) | Natural | Natural |
| Yara, jovem, ouve a voz "desde que a Fenda abriu" (fato) | Natural, com "reabriu" | Natural, com "reabriu" |

### Conclusão

A estrutura de dois tempos funciona com o conteúdo atual. Ela explica a venda das relíquias, a idade da Yara, a mãe de Thomas e a Ponte de Varn. O que quebra é só o número "cem anos", diante do veterano vivo.

**Recomendação:** Primeira Fenda há ~60 anos e Reabertura há ~3 anos.

**Alternativa**, se Jean quiser manter "cem anos": o veterano passa a ter lutado na Reabertura, e a testemunha da Ilse vira um diário.

Mudanças de texto que a recomendação exigirá, em tarefa própria e só depois de aprovada:
- "cem anos" no prólogo e na origem do vilão (`jogo.py:212`, `dados.py:421`);
- "se abriu" na ficha da Odette;
- "abriu" na fala da Yara.

## 2. Ulook e o vilão [proposta]

Hoje o vilão é sorteado entre 8 títulos e 5 origens (`dados.py:411–422`), mas a Yara sempre cita **Ulook** [existe].

Proposta para a campanha:
- **Ulook** é a voz do outro lado.
- **O bispo**, hoje Arcebispo Profanado, é o rosto humano: vendeu as relíquias e procura os Sigilos.

O vilão é fixo. O título "Arcebispo Profanado" e a origem "o bispo que abriu as catacumbas" já existem no catálogo.

## 3. O protagonista e Marta [proposta, não aprovada]

**Proposta:** o herói nasceu no Vau do Turvo, é irmão ou irmã de Marta, saiu do vale há anos e volta por causa da carta ("A febre voltou. Não venha.").

**O que essa origem fixa ganha:**
- Motivo imediato e concreto, sem exposição longa.
- O herói conhece a vila e é reconhecido. A consequência na volta pesa mais porque é a casa dele.
- Marta serve de âncora para o resgate, o atendimento e o epílogo.
- Uma linha de passado por classe liga o herói à campanha:
  - **Guerreiro:** recrutado pelo duque; ouviu falar de Varn.
  - **Arqueiro:** caçava no vale; conhece as trilhas.
  - **Mago:** estudou na escola da catedral; sabe quem era o bispo.

**O que ela limita:**
- Fixa lugar de nascimento e família. Toda origem futura (E8) teria que caber em "nasceu no Turvo e tem uma irmã curandeira". Forasteiro, nobre de longe ou outra raça ficam difíceis.
- Tira a interpretação do "estranho sem laços", que muitos jogadores escolhem.
- Parentesco de sangue tende a puxar cenas de família (pais, casa, herança) e aumenta o escopo.
- Se o jogador não se importar com Marta, o motivo inicial fica fraco. Por isso a febre também ameaça a vila inteira.

**Recomendação:** manter a **função** de Marta e não o **sangue**.
- Marta é quem escreveu, e o laço é uma linha de texto escolhida pela origem.
- Enquanto não houver origens, o padrão é um laço só. Jean escolhe entre: irmã; quem criou o herói; amiga de infância a quem o herói deve a vida.
- **Regra:** nenhuma cena depende de parentesco de sangue (nada de pais nem herança); só as falas mudam.

Uma origem futura troca a frase sem reescrever a região. Exemplo: "forasteiro: Marta salvou sua vida na estrada e você prometeu voltar".

**Atendimento e resgate enquanto Marta está doente:**
- Pita, a aprendiz, mantém o serviço da curandeira com as mesmas regras.
- O resgate leva o herói à casa de Marta, chamado por Pita.

Detalhes no [11](11-E1-REGIAO-INICIAL.md), seção 12.

## 4. A lógica dos Sigilos [proposta]

Esboço suficiente para a região 1 não contradizer as seguintes.

1. **O selo.** Depois da Primeira Fenda, a Igreja fechou a passagem com um selo de duas partes:
   - **o centro:** as relíquias, na cripta da catedral;
   - **três Sigilos:** prendem o selo de longe, como três pregos de uma tampa.

   Os Sigilos foram levados para lugares distantes, para que ninguém os juntasse. Quem leva os três ao centro comanda o selo: pode refazê-lo ou abri-lo.
2. **Os guardiões.** Cada Sigilo ficou com um guardião, pessoa ou ordem. Um Sigilo puxa a Fenda para quem o segura. Em décadas, os guardiões se deformaram, ou morreram e foram substituídos por coisas que se agarraram ao Sigilo. Isso é o que o jogo já diz: "Três guardiões, deformados pela Fenda, guardam os Sigilos" [existe]. Ilse é o caso humano: guardiã afogada, deformada com o Sigilo no peito.
3. **A Reabertura.** O bispo vendeu as relíquias. Sem o centro, a Fenda reabriu em parte e toda a carga caiu sobre os três Sigilos. Eles racharam e vazam por onde estão presos:
   - no Turvo, a febre;
   - perto de Varn, as crias do Vazio;
   - nas Pedras Negras, as vozes.
4. **Por que o herói os tira.** Preso a um corpo ou lugar, o Sigilo rachado vaza ali. Na mão de um vivo, ele se aquieta e o vazamento local para. Mas cada Sigilo retirado afrouxa um pouco mais o selo na catedral, e a Fenda cresce: é a escalada do Ato III.

   Na região 1, deixá-lo seria pior: a febre continuaria e os cultistas do bispo, que já estão na sacristia, o levariam.
5. **O interesse de Ulook.** Do outro lado, Ulook não pode tocar os Sigilos, porque o selo o repele. Precisa de mãos vivas que os levem ao centro:
   - tentou com o bispo (relíquias vendidas, cultistas);
   - fala com a Yara;
   - não se importa com quem os leva: o herói também serve.

   A muralha de sombras que só se abre com os três Sigilos [existe: `sistemas/navegacao.py:42`] é exatamente isso: só quem leva os três chega ao centro.
6. **Selar.** No centro, com os três Sigilos, refazer o selo. As relíquias foram vendidas, então alguém precisa ocupar o lugar delas: uma vontade viva que fica. Pode ser o herói; a Odette, se seguiu o caminho penitente; ou a Yara, se se libertou da voz.

   Ideia guardada, não obrigatória: recuperar relíquias vendidas na região 2 muda quem precisa ficar.
7. **Romper.** Quebrar os três Sigilos dentro da Fenda aberta. O selo deixa de existir, e a porta também: a passagem desaba sobre si mesma e Ulook perde o caminho. Só é possível agora, porque só com a Fenda aberta se chega ao centro; por isso a Igreja não fez isso há 60 anos.

   Custo proposto, só nos epílogos: a catedral cai e o que veio do Vazio se cala (a voz da Yara, os afogados, a força do caminho `vazio`). As habilidades das classes não mudam.
8. **Abrir (variante sombria, opcional).** Entregar os três a Ulook. Pode ser cortada.

**Revelação do meio** (fim da região 2): o herói descobre que está fazendo o que Ulook quer. Não há como devolver os Sigilos, porque os lugares já vazam. A pergunta muda de "como entrar" para "o que fazer lá dentro".

## 5. Arco da campanha: início, meio e fim [proposta]

A estrutura atual já é "três guardiões com Sigilos, depois a Cidadela, chefe no nível 11" [existe: `balanceamento.py`, `ANTAGONISTA_NIVEL = 11`]. A proposta é uma região escrita por Sigilo.

| Ato | Região | Níveis | Conflito local | Companheiro em destaque | Sigilo |
|---|---|---|---|---|---|
| **I — Início** | Vale do Turvo | 1–4 | A febre, Ilse e Caspar | Yara (encontro), Odette (Caspar) | 1º |
| **II — Meio** | Terras de Varn (planície/montanha) | 5–7 | O duque que não mandou a coluna; desertores dos Cães de Ferro; a cidade da mãe de Thomas | Morel (Theodore), Odette | 2º |
| **II — Meio** | Brejo das Pedras Negras (pântano/ruínas) | 7–9 | Seguidores do bispo; o círculo de pedras negras | Yara (Ulook, círculo negro) | 3º |
| **III — Fim** | Catedral Partida (a Cidadela) | 10–11 | O bispo e Ulook; selar ou romper | Os três, conforme os caminhos | — |

A ordem das regiões do Ato II é fixa na primeira versão, porque o nível dos inimigos depende do lugar.

**Epílogos:**
- Vau do Turvo (os dois eixos);
- Varn;
- Pedras Negras;
- Odette, Morel e Yara pelos caminhos que já existem: `penitente`/`calada`, `redencao`/`capitao`/`adiado`/`quites`, `liberta`/`vazio`;
- Marta.

Não há um final por combinação. A ideia guardada de aliados no confronto final cabe aqui como opcional: por exemplo, os Cães de Ferro vêm se o Morel teve o caminho `adiado` ou `redencao`.

**Tamanho:** quatro regiões, a última curta. A duração real só se estima depois de jogar a região 1 (E9).

## 6. Derrota na campanha [hipótese]

Hipótese aceita por Jean, sem decisão definitiva e sem autorização para mudar o padrão atual:
- **Campanha:** resgate com as perdas atuais (`jogo.py:248`). Na região 1, o resgate leva à casa de Marta, chamado por Pita.
- **Masmorra:** salas vencidas continuam vencidas; a guardiã volta inteira.
- **Hardcore:** opção explícita na criação da campanha.
- **Texto:** o prólogo da campanha diz o modo verdadeiro. A frase atual sobre morte permanente está em [13](13-PENDENCIAS-FORA-DA-CAMPANHA.md).

## 7. Transição do procedural [hipótese, com regras propostas]

1. **Duas portas de entrada, um motor.** A campanha começa por um novo início; o procedural continua como está.
2. **Procedural congelado.** Só recebe correção de defeito. Nada da campanha precisa funcionar nele.
3. **Gabarito como cerca.** As partidas atuais do gabarito são procedurais. Mudança em código compartilhado mantém o gabarito, ou explica a diferença como mudança de propósito. A campanha ganha cenários de teste próprios.
4. **Conteúdo marcado.** Cenas da campanha só disparam na campanha. Eventos aleatórios existentes podem rodar nas duas.
5. **Decisão depois da E9.** Aposentar o procedural ou mantê-lo congelado como "modo livre". Recomendação: aposentar quando a campanha cobrir o jogo inteiro (E11).

Legado entre partidas, nomes sorteados, vilão sorteado e mapa gerado ficam só no procedural.

## 8. O que decidir, e quando

**Antes da E2** (carregar a região fixa). Só três:

| # | Decisão | Recomendação |
|---|---|---|
| 1 | Geografia da região: quatro lugares, saída fechada, ligações e faixas de nível. Nomes podem seguir provisórios | Como no [11](11-E1-REGIAO-INICIAL.md), seção 2 |
| 2 | Campanha como novo início, com o procedural congelado | As regras da seção 7 |
| 3 | Modo da campanha ao começar | Resgate por padrão e hardcore como opção. O prólogo provisório da E2 diz isso |

**Antes da E3** (escrever as cenas da missão):
- a causa da febre (seção 4 do 11);
- os dois eixos e os três passos do Dar descanso;
- a cronologia de 60 e 3 anos;
- o laço padrão com Marta.

**Antes da região 2:**
- a lógica dos Sigilos;
- Ulook e o bispo como vilão fixo;
- os finais;
- a ordem das regiões.

**Não precisa agora:**
- raças e origens (E8);
- preparação e transformações (E6);
- facções;
- duração exata;
- detalhes do custo da derrota (E9).
