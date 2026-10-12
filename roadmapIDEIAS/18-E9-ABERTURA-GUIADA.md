# 18 — Abertura guiada da campanha (E9): especificação

Especificação para revisão, antes de implementar (pedido de Jean, 12/10/2026, sobre a 1.65.3). A direção já foi
aprovada por Jean; este documento detalha a sequência, os textos e o escopo da primeira implementação. Nada aqui
muda o jogo ainda.

**O que se quer:** uma orientação **opcional**, para testar se ela ajuda quem nunca jogou. A abertura (a luta curta, o
encontro com Morel) é a mesma para todos; a caixa "Mostrar tutorial" controla só os quadros de orientação.

**O que não entra:** classe, região, árvore de talentos ou sistema amplo de tutorial novos; mudança de equilíbrio,
preços, recompensas gerais ou recursos iniciais; mudança nos encontros da noite (só a investigação, seção 8).

## 1. Por que (evidência e limite)

Da partida da Quibia (17, seção 19.1), separando fato de leitura:

| O que se viu | De onde | O que a abertura faz com isso |
|---|---|---|
| Não percebeu Habilidades até Jean apontar | sessão; o registro confirma: nas 4 primeiras lutas, só o ataque básico | a primeira luta ensina Habilidades com a ação de verdade |
| Não entendeu que a vila era clicável | sessão | um prédio indicado, uma vez, com um motivo |
| Seguiu contratos depois de uma dica | sessão | o Mural indicado depois da luta |
| Conheceu Morel no dia 17 | registro (`morel_na_taverna`, dia 17) | Morel na taverna da abertura, previsível |
| Não encontrou Odette | registro | nada novo: ela segue na estrada (seção 6) |
| Exploração tarde | registro: os eventos de "explorar" só nos dias 16 e 24 | um motivo para explorar, dito por Morel, e um quadro na primeira vez fora da vila |
| Perdeu o Salão Alagado de dia (nível 2) e à noite (nível 5) | registro | a noite: seção 8 (investigação, sem mudar encontros) |

Uma jogadora não dá a frequência desses problemas no público. Por isso a orientação é opcional e se mede (seção 11).

**Por que Morel aparecia tarde:** ele já é garantido na primeira "Taverna: pagar uma bebida e ouvir rumores" a partir
do dia 2 (`servicos.ouvir_rumores`: enquanto ninguém o conheceu, toda bebida sorteia o evento dele). Nada leva o
jogador até essa opção; quem não pede bebida não o encontra.

## 2. Princípios

1. **Aprender fazendo.** Cada quadro aparece quando a ação que ele ensina está disponível e some quando ela acontece.
   Sem "OK" para confirmar o que a pessoa acabou de fazer.
2. **Uma coisa por vez, na hora em que importa.** Nada de percorrer os ícones da tela. Equipamento e talentos só
   quando chegam.
3. **A instrução fica na interface; o personagem fala da situação.** O quadro diz "Clique em Habilidades"; o
   taverneiro diz por que há ratos na despensa. Nomes reais da interface (Habilidades, Atacar, Mural, Mercado,
   Explorar a região, Talentos, Comitiva).
4. **Nada esconde o que importa.** O escurecimento é leve e nunca cobre a arena (vida, inimigos, efeitos), as barras do
   herói nem o texto da cena.
5. **Igual com ou sem tutorial.** Mesmos eventos, lutas, sorteios e recompensas; o motor decide a abertura, a caixa só
   liga os quadros. Um teste confere: a mesma semente com a caixa marcada e desmarcada dá o mesmo save no fim.
6. **O motor decide, a tela desenha.** O motor diz qual orientação vale agora (id, texto, âncora); a tela desenha o
   quadro, a seta e o escurecimento.

## 3. A sequência narrativa

### 3.1 Criação

Na criação da campanha, depois de "Se você cair…" (Resgate ou Hardcore), uma caixa **"Mostrar tutorial"**, marcada.
Na web, uma linha marcável na mesma tela da escolha do modo; no texto, uma pergunta curta ("Mostrar as orientações do
tutorial? Sim / Não"). Guardado no save (`tutorial`).

### 3.2 Chegada e a luta curta (dia 1, manhã)

Depois do prólogo e da cena de abertura da febre (como hoje), uma cena nova, **"A Despensa da Taverna"**, toca uma
vez, no primeiro menu do Vau:

> O taverneiro do Vau te para na porta. "Você tem cara de quem sabe usar isso aí", diz, olhando para a sua arma. "Desde
> que a febre derrubou meu ajudante, ninguém desce na despensa. Os ratos tomaram conta. Se der um jeito neles, a
> primeira caneca é por minha conta."

Opções: **"Descer à despensa"** e **"Agora não"**. A luta: **dois ratos gigantes de nível 1**, sem a mordida e o veneno
(só nesta luta, para ser previsível), de dia, com luz. A fuga funciona como sempre.

- **Razão:** ensinar a luta onde o erro custa pouco. Dois ratos: uma habilidade derruba um, o outro continua, e a luta
  segue sem nada artificial. Se o primeiro golpe acabar com tudo (crítico, ou um rato que já morreu), a luta acaba.
- **Recompensa:** o XP de sempre dos dois ratos (6 cada); sem ouro e sem saque (ratos não carregam nada). A "caneca por
  minha conta" é a próxima "bebida e rumores", grátis uma vez (3 de ouro; é o que leva a Morel, 3.3).
  **Decisão para Jean:** é a única mudança de economia (12 de XP e uma caneca de 3 ouro no dia 1). Recomendo manter;
  se não, a caneca sai e fica só o XP. Antes e depois: `tests.equilibrio` e `tests.replay`.
- **"Agora não":** a ação "Taverna: descer à despensa" fica no menu do Vau até ser feita (marcada como ação do lugar,
  como as de missão), sem prazo. As orientações de combate passam para a primeira luta que acontecer.

### 3.3 Morel, previsível

Vencida a despensa, de volta ao salão:

> No canto, um homem grande come sozinho, de costas para a parede. Assistiu a tudo sem levantar. "Rato é fácil", diz.
> "Bebe a tua caneca e senta aqui, se quiser ouvir uma proposta."

A ação **"Taverna: sentar com o homem do canto"** aparece no menu do Vau (uma vez, até usada). Ela toca o evento que já
existe, `morel_na_taverna`, pelo motor de eventos (conta na `contagem`), sem a condição `dia >= 2` só desta vez. As
opções e as regras ficam como são: pagar 40, queda de braço, Carisma ou Recusar. **Encontrar não é recrutar.**

- **Razão:** apresentar a comitiva cedo, com a cara de Morel (o mercenário prático), sem obrigar.
- **Recusou:** valem as regras de hoje (ele volta em outra bebida, até 3 vezes no total, a cada 4 passos ou mais).
- **Duplicar:** a cena chama o mesmo evento e marca a mesma `contagem`; o sorteio garantido da bebida
  (`morel_esperando`) só vale enquanto a contagem é zero, então a cena e o sorteio não se somam. Aceito, `disponivel`
  fica falso e o evento some.

### 3.4 Depois da luta: a vila

Nesta ordem, cada quadro só uma vez e só se a condição valer (se não valer, ele espera a vez dele ou não aparece):

1. **Um prédio clicável (o Mural).** Morel, ao fim da conversa (aceito ou não): "Contrato no mural paga pouco, mas
   paga. Eu começaria por ali." Quadro no Mural. Com o tutorial desligado, o convite que já existe (o Mural piscando,
   "clique: contratos") continua como hoje; com o tutorial ligado, o quadro toma o lugar dele.
2. **Recuperar.** Só se a vida estiver abaixo de 70% ou o recurso abaixo de metade quando o menu da vila voltar: quadro
   na Curandeira e na Taverna (dormir).
3. **Provisões.** Na primeira vez que a pessoa abrir "Viajar" (ou clicar na Estrada): quadro no contador de provisões
   do topo e no Mercado, antes de sair. Se ela já tiver comprado, o quadro não aparece.
4. **Morel e o cartão da comitiva.** Na primeira vez que o menu volta com Morel no grupo: quadro no cartão dele.
5. **Explorar.** O motivo vem de Morel na conversa: "O dinheiro de verdade está no que ninguém foi buscar. Desde que
   a febre fechou a estrada, tem carroça largada no bosque. Às vezes tem alguma coisa; às vezes só lobo." Sem Morel, o
   taverneiro diz o mesmo ao servir a caneca. Na primeira chegada a um lugar fora da vila, quadro em "Explorar a
   região".

Equipamento e talentos ficam para quando chegarem (seção 4.3). A noite, para a primeira noite fora da vila (4.3).

## 4. Os quadros: texto, quando aparecem, o que os encerra

Textos curtos, da interface, com os nomes que estão na tela. `{…}` vem do motor (o nome e o custo da habilidade da
classe, o recurso, a tecla).

### 4.1 Primeira luta (a despensa, ou a primeira luta se a pessoa disse "Agora não")

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| C1 | botão Habilidades | "Suas habilidades ficam aqui. Clique em **Habilidades** (tecla {2})." | a roda de ações aparece | a janelinha de Habilidades abre |
| C2 | a linha da habilidade na janelinha | "**{Golpe Pesado}**: {170% de dano} por {10} de {Vigor}. Clique nela." | C1 encerrou | a habilidade é escolhida |
| C3 | as cartas dos inimigos | "Escolha o alvo: clique num inimigo (ou na tecla do número dele)." | a mira acende | o alvo é escolhido |
| C4 | a barra de {Vigor} na carta do herói | "O golpe gastou {10} de {Vigor}. **Atacar** não gasta e devolve um pouco." | o golpe é desenhado (lance) | a próxima ação é escolhida, ou o quadro do fim da luta abre |

Por classe: Guerreiro, **Golpe Pesado** (10 de Vigor, 170% de dano); Arqueiro, **Tiro Certeiro** (8 de Foco, 170% de
dano e mais chance de crítico); Mago, **Bola de Fogo** (14 de Mana). Os números saem da ficha (`habilidades.efetiva`),
como na janelinha.

- **Esc na janelinha** (fecha como sempre): volta para C1. **Voltar na mira:** volta para C2.
- **Escolheu outra habilidade:** C2 encerra do mesmo jeito (o quadro ensina o caminho, não obriga a habilidade).
- **Atacou em vez de abrir Habilidades:** C1 fica até a próxima vez que a roda aparecer nesta luta; se a luta acabar
  antes, a sequência passa para a luta seguinte. Depois de duas lutas sem abrir Habilidades, C1 para (nada de insistir).
- **O golpe acabou com a luta:** C4 não aparece por cima do espólio (o espólio já fecha a luta); fica para a próxima
  luta em que a pessoa usar uma habilidade, uma vez.

### 4.2 Vila e estrada

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| V1 | o Mural (balão do prédio) | "Os prédios da vila são clicáveis. **Mural**: os contratos." | menu do Vau depois de Morel (3.4.1) | o Mural é aberto |
| V2 | Curandeira e Taverna | "Vida baixa. A **Curandeira** cuida por ouro; **dormir na Taverna** recupera tudo até amanhã." | menu do Vau com vida < 70% ou recurso < 50% | um dos dois é usado, ou a pessoa sai da vila |
| V3 | provisões no topo (e o Mercado) | "Cada dia fora come 1 provisão (você tem {4}). O **Mercado** vende mais." | primeira vez em Viajar | a viagem começa, ou o Mercado é aberto |
| V4 | o cartão de Morel na Comitiva | "{Morel} luta com você e come 1 provisão por dia. Clique no cartão para conversar." | primeiro menu com Morel no grupo | o cartão é aberto, ou o menu muda |
| V5 | "Explorar a região" | "**Explorar** gasta um período. Pode dar luta, um achado ou nada." | primeira chegada fora da vila | a pessoa escolhe qualquer opção do menu |

### 4.3 Quando chegar

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| E1 | a comparação na janela do item | "▲ e ▼ comparam com o que você veste. **Equipar** troca; **Guardar** leva na mochila." | a primeira janela de equipamento | a decisão do item |
| T1 | Talentos (na doca) | "Você tem {1} ponto. **Talentos** (tecla T) abre a árvore." | o primeiro ponto de talento | a árvore abre |
| N1 | o modificador "Inimigos +1 nível" no topo | "À noite os inimigos vêm um nível acima e batem mais forte. Sem tocha, a luta começa com eles atacando." | a primeira noite fora da vila | a próxima escolha |

O N1 depende do texto da noite estar certo (seção 8): hoje a dica diz "mais vezes em bando", que não vale nas salas.

## 5. Desenho, mouse e teclado

**Reaproveitado:**
- a caixa de dica (`telas/dicas.js`) para o estilo do quadro (fundo, borda, fonte), sem o comportamento de seguir o
  mouse;
- o realce que pisca do convite do Mural (`.predio.convite`, 04-pagina.css) e o pulso da bolsa (`.slot-px.trata`) para o
  destaque, com o mesmo cuidado de movimento reduzido;
- as âncoras que já existem: `.roda-botao[data-slot="habilidades"]`, `.rj-linha[data-hab=…]`, `.carta.alvejavel`, a
  barra de recurso da carta do herói, `#predios .predio[data-predio=…]`, o contador de provisões do topo, o cartão da
  comitiva, as opções do menu do lugar (`meta`), `.achado-cartao`, o atalho de Talentos.

**O quadro:** pequeno (até ~260 px), ao lado da âncora, com uma seta discreta apontando para ela; abaixo do texto, em
letra menor, "Dispensar orientações". O destaque é um anel claro em volta da âncora.

**O escurecimento:** um véu leve (cerca de 25%) só nas áreas que não importam naquela hora (as colunas laterais e a doca
durante a luta; o texto da cena durante a vila). Nunca sobre a arena, as cartas, as barras do herói e dos inimigos e o
topo. O véu não recebe clique (`pointer-events: none`): tudo continua clicável.

**Mouse:** o quadro não bloqueia nada; clicar fora dele não o fecha (ele fecha quando a ação acontece).
**Teclado:** as teclas de sempre funcionam (1–4 na roda, os números na mira, Esc, Enter); o quadro diz a tecla quando
existe. O foco não vai para o quadro; "Dispensar orientações" é alcançável com Tab. A Ajuda abre com **F1**.

**Movimento reduzido:** sem piscar; o anel fica aceso.

## 6. Pular, fugir, perder, salvar e carregar; os outros caminhos

- **Dispensar orientações:** desliga todas neste save (o quadro some na hora). Religar: na Ajuda.
- **Ajuda** (novo item discreto no topo, ao lado de Histórico; F1): a lista curta dos quadros já vistos, agrupados
  (Luta, Vila, Estrada, Comitiva, Itens), e a chave "Mostrar orientações: ligado/desligado". Só texto; nada de tour.
- **Pular o texto** (clique ou tecla que adianta): não afeta os quadros, que aparecem quando a pergunta aparece.
- **Fugir da despensa:** a luta conta como não feita; a ação "Taverna: descer à despensa" volta; as orientações
  continuam na próxima luta.
- **Perder:** contra estes ratos é improvável (critério: em 1000 lutas simuladas por classe, nenhuma derrota). Se
  acontecer, valem as regras do modo (resgate ou fim no hardcore), sem exceção.
- **Salvar e carregar:** guardados no save `tutorial` (ligado ou não) e as orientações já vistas; a cena da despensa e a
  de Morel usam as cenas vistas da missão, como as outras. No meio de uma luta não há save (o autosave é no menu);
  carregado, o que faltava continua na próxima vez que a condição valer.
- **Saves de antes:** sem o campo, `tutorial` é falso e a despensa não aparece (a abertura é para campanha nova).
- **Outro caminho:**
  - quem sai do Vau sem descer à despensa: a ação fica lá; a primeira luta da estrada recebe C1–C4;
  - quem não fala com Morel: a ação fica no menu até ser usada; a bebida da taverna continua levando a ele, como hoje;
  - quem não abre o Mural: o convite (ou V1) continua até a primeira visita;
  - Odette continua só na estrada e na exploração (evento `odete_na_estrada`, dias 2 a 8 com peso maior); V5 e o motivo
    de explorar aumentam a chance de cruzar com ela sem forçar.

## 7. Arquitetura proposta (mínima)

- **Motor:** `rpg/orientacoes.py`: as orientações como dados (id, texto com campos, âncora, condição de aparecer e de
  encerrar) e uma função que diz qual vale agora. O estado da tela (`web/estado.py`) leva `orientacao: {id, texto,
  ancora}` quando há uma. As que dependem de clique na tela (C1, C2, a janelinha) avançam na própria tela e avisam o
  motor quando a sequência fecha. Hoje a tela só fala com o motor por `/responder` (a resposta da pergunta em
  aberto); é preciso uma rota pequena nova (`/orientacao`, com `feito` ou `dispensar`), tratada pela ponte fora da fila
  das perguntas.
- **Conteúdo:** a cena da despensa e a ação de Morel como `CENAS`/`ACOES` da campanha (`missoes.py`, como a herança de
  Berta), chamando o evento que já existe.
- **Tela:** um módulo pequeno (`app/orientacao.js`) que acha a âncora, desenha o quadro, a seta, o anel e o véu, e
  reposiciona ao redimensionar.
- **Texto (interface de terminal):** os quadros viram uma linha cinza antes do menu, uma vez cada ("Dica: as
  habilidades ficam em Habilidades."); a caixa da criação vale também ali.

## 8. A noite: como o jogador percebe hoje (investigação; sem mudar encontros)

**Regras de hoje** (código conferido):
- à noite (período 3), os inimigos dos grupos sorteados vêm **+1 nível** (`NOITE_NIVEL`) e batem **×1,1**
  (`NOITE_INIMIGOS`); grupo de tamanho livre tem 40% de chance de +1 inimigo; espectros entram no pântano, na planície
  e nas ruínas; o encontro hostil fica mais provável (peso 38 contra 28) e a Percepção para evitá-lo, mais difícil (+3);
- as **salas da capela** têm tamanho fixo: à noite vêm +1 nível e batem ×1,1, **sem** inimigo a mais nem espectros. A
  capela é ruína: **sempre escura**, gasta tocha de dia também; sem tocha, a sala começa com o inimigo mais rápido
  atacando primeiro;
- no caminho natural, a noite cai **dentro** da capela: vencer a nave avança o período, e a sacristia já é à noite.

**O que avisa hoje:** a frase "A noite cai. Algo começa a se mover nas trevas…" quando o período chega à noite (não sai
quando a noite vem dormindo na taverna); "(à noite é mais perigoso)" em "Explorar a região"; o topo com "Noite" e o
modificador **"Inimigos +1 nível"** (dica: "um nível acima, mais vezes em bando, e causam 10% mais dano"); a tela mais
escura; "Escuro −4" sem tocha.

**O que não avisa ou avisa errado:**
- o "inimigos Nv.3" do cabeçalho e do mapa não soma o +1 da noite;
- as ações da capela não dizem nada da noite nem da tocha antes de entrar (a tocha só aparece na hora da luta);
- "mais vezes em bando" não vale nas salas, nos eventos com inimigos escritos e nos guardiões;
- "emboscadas mais prováveis" sem tocha, quando na sala a emboscada é certa;
- a capela gasta tocha de dia também.

**Leitura (hipótese):** quem entra na capela à tarde não percebe que a sacristia vai ser à noite, e quem vê "Nv.3" não
sabe que vai enfrentar nível 4. A Quibia perdeu o Salão à noite no nível 5 contra inimigos de nível 4 e 5.

**Propostas para depois (não fazem parte desta entrega e não mexem em encontros):** a nota da ação da sala dizer
"à noite: inimigos +1 nível" e "gasta 1 tocha"; o nível do cabeçalho mostrar o da hora ("Nv.3, Nv.4 à noite"); a dica
do modificador dizer só o que vale em todo lugar; a frase da noite também ao acordar à noite. O N1 (4.3) depende disso.

## 9. Primeira implementação (escopo mínimo)

1. A caixa "Mostrar tutorial" (web e texto), o campo no save, "Dispensar orientações" e a Ajuda com a chave.
2. A cena da despensa (igual com e sem tutorial) e a ação de Morel na taverna, chamando o evento que existe.
3. Os quadros C1–C4 (primeira luta) e V1 (Mural), com o véu, a seta e o anel.
4. Testes: a mesma semente com e sem tutorial dá o mesmo save; a despensa não se repete; Morel não aparece duas vezes
   (cena e bebida); fugir e carregar; os quadros encerram com a ação; a fumaça a 1500 e 1280 px, com mouse e teclado.

V2–V5, E1, T1 e N1 numa segunda entrega, depois do primeiro teste com uma pessoa nova. O N1 só depois de corrigir os
textos da noite (seção 8).

## 10. Decisões para Jean

1. A caneca grátis do taverneiro (3 de ouro) e o XP dos ratos (12): manter (recomendo) ou ficar só com o XP.
2. O nome do taverneiro: deixo sem nome ("o taverneiro do Vau") ou um nome inventado.
3. A Ajuda no topo (F1) com a lista do que já foi visto: aprovar o lugar.

## 11. Critérios para testar com outra pessoa, sem ajuda

Observar (gravar a tela se der), com a caixa marcada, sem dizer nada além de "jogue a campanha":

| # | O que se espera ver | Como saber |
|---|---|---|
| 1 | usa uma habilidade na primeira luta | registro: `habilidades` na luta 1 |
| 2 | usa habilidade em pelo menos metade das lutas até o nível 3 | registro |
| 3 | clica num prédio da vila nos primeiros 5 minutos | observação |
| 4 | aceita um contrato até o dia 3 | registro (o contrato aparece no Diário; hoje não há linha própria no registro: anotar) |
| 5 | encontra Morel até o dia 3 (aceitando ou não) | registro: `morel_na_taverna` |
| 6 | compra provisões antes da primeira viagem, ou sabe dizer quantas tem | registro e uma pergunta depois |
| 7 | explora pelo menos uma vez até o dia 5 | registro: um evento de "explorar" |
| 8 | sabe dizer, depois, o que a noite muda | pergunta depois (resposta aceita: inimigos mais fortes) |
| 9 | nenhum momento parado por mais de um minuto sem saber o que fazer | observação |
| 10 | se dispensou as orientações, quando e por quê | observação e pergunta |

Comparação: uma segunda pessoa com a caixa desmarcada, se houver. Os números (1, 2, 4, 5, 7) saem do registro da
partida; os outros, de olhar e perguntar no fim, junto da ficha da seção 9 do 17.
