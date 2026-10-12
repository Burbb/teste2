# 18 — Abertura guiada da campanha (E9): especificação

Especificação da abertura guiada (pedido de Jean, 12/10/2026, sobre a 1.65.3), revista por Jean e ajustada antes da
primeira implementação (seção 12: o que foi implementado e como foi conferido). A segunda parte (V2–V5, E1, T1, N1)
continua só especificada.

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
   herói nem as opções; o quadro também não (na luta, ele fica abaixo da arena).
5. **Igual com ou sem tutorial.** Mesmos eventos, lutas, sorteios e recompensas; o motor decide a abertura, a caixa só
   liga os quadros. Um teste confere: para o mesmo roteiro de ações, o estado de jogo, as recompensas e o sorteio são
   os mesmos com a caixa marcada e desmarcada; só os campos das orientações (ligado, vistas) diferem.
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

Opções: **"Descer à despensa"** e **"Agora não"**. A luta: **dois "Ratos da despensa"**, nível 1: a espécie de sempre,
magra (40% do ataque, agilidade 2) e sem a mordida e o veneno, para ser previsível. De dia, com luz. A fuga funciona
como sempre. Os números ficam na ficha do inimigo; nada é escondido (crítico e ferimento seguem as regras de sempre).
Dois ratos, e não um, para a mira (C3) existir: com um inimigo só, o alvo é automático.

- **Razão:** ensinar a luta onde o erro custa pouco. Dois ratos: uma habilidade derruba um, o outro continua, e a luta
  segue sem nada artificial. Se o primeiro golpe acabar com tudo (crítico, ou um rato que já morreu), a luta acaba.
- **Recompensa (decidido por Jean):** o XP de sempre dos dois ratos; sem ouro e sem saque (ratos não carregam nada).
- **A caneca (decidido por Jean):** é o serviço que já existe, "Taverna: pagar uma bebida e ouvir rumores", **uma vez
  sem pagar**. Não é ouro dado ao herói. O cartão do serviço diz "por conta da casa" enquanto a caneca espera. Usada,
  ela faz exatamente o que a bebida paga faz (o limite de duas por dia, o rumor, ou um evento da taverna, inclusive o
  de Morel quando a regra de hoje o chama) e some. Se a pessoa nunca a usar, ela fica.
- **"Agora não":** a ação "Taverna: descer à despensa" fica no menu do Vau até ser feita (marcada como ação do lugar,
  como as de missão), sem prazo. As orientações de combate passam para a primeira luta que acontecer.

### 3.3 Morel, previsível

Vencida a despensa, de volta ao salão:

> O taverneiro olha os dois ratos e cospe de lado. "A primeira caneca é por minha conta, quando você quiser." Ele aponta
> a praça com o queixo. "E se quer trabalho, o mural paga quem limpa a estrada."
>
> No canto, um homem grande come sozinho, de costas para a parede. Assistiu a tudo sem levantar. "Rato é fácil", diz.
> "Senta aqui, se quiser ouvir uma proposta."

(O segundo parágrafo só se Morel ainda não apareceu e está livre.)

A ação **"Taverna: sentar com o homem do canto"** aparece no menu do Vau (uma vez, até usada). Ela toca o evento que já
existe, `morel_na_taverna`, pelo motor de eventos (conta na `contagem`), sem a condição `dia >= 2` só desta vez. As
opções e as regras ficam como são: pagar 40, queda de braço, Carisma ou Recusar. **Encontrar não é recrutar.**

- **Razão:** apresentar a comitiva cedo, com a cara de Morel (o mercenário prático), sem obrigar.
- **Recusou:** valem as regras de hoje (ele volta em outra bebida, até 3 vezes no total, a cada 4 passos ou mais).
- **Duplicar:** a ação chama o mesmo evento e marca a mesma `contagem`. Ela só aparece enquanto Morel nunca apareceu
  (`contagem` zero) e está disponível (não está no grupo, na reserva, nem tem flag de saída). Quem já o encontrou pelos
  rumores, recrutou, recusou ou o perdeu não vê a ação: a apresentação nunca reabre um recrutamento resolvido.
- **A caneca e Morel:** a caneca não é a apresentação de Morel. No dia 1, a bebida não o chama (a regra dele pede o
  dia 2); do dia 2 em diante, a bebida o chama enquanto ele nunca apareceu (regra de hoje). Nos dois casos o evento é
  o mesmo e conta uma vez: se ele aparecer pela bebida, a ação "sentar com o homem do canto" some; se a pessoa sentar
  primeiro, a bebida depois dá um rumor ou outro evento da taverna.

### 3.4 Depois da luta: a vila

Nesta ordem, cada quadro só uma vez e só se a condição valer (se não valer, ele espera a vez dele ou não aparece):

1. **Um prédio clicável (o Mural).** O taverneiro, ao fim da despensa: "o mural paga quem limpa a estrada". Quadro no
   Mural (V1) a partir do menu da vila depois do pedido (despensa feita ou adiada), até o Mural ser aberto. Com o tutorial desligado, o convite que já existe (o Mural piscando,
   "clique: contratos") continua como hoje; com o tutorial ligado, o quadro toma o lugar dele.
2. **Recuperar.** Só se a vida estiver abaixo de 70% ou o recurso abaixo de metade quando o menu da vila voltar: quadro
   no Templo (vida) e na Taverna (dormir). A Curandeira só se houver ferimento.
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
| C1 | botão Habilidades | "Clique em **Habilidades** (tecla 2)." | a roda de ações aparece | a janelinha de Habilidades abre |
| C2 | a linha da habilidade na janelinha | "Clique em **{Bola de Fogo}**." | C1 encerrou | uma habilidade é escolhida |
| C3 | as cartas dos inimigos | "Clique num inimigo para escolher o alvo." | a mira acende | o alvo é escolhido |
| C4 | a barra de recurso na carta do herói | por classe, abaixo | a habilidade é usada | a próxima ação é escolhida, ou a luta acaba |

Os quadros não repetem a descrição da habilidade: a janelinha e a dica já mostram o efeito e o custo. C4 diz só o
custo e o que o **Atacar** faz, pelas regras da classe (o motor monta o texto com os números da ficha e do
balanceamento):

- **Guerreiro:** "{Golpe Pesado} gastou {10} de Vigor. **Atacar** não gasta Vigor e, se acertar, devolve {2}."
- **Mago:** "{Bola de Fogo} gastou {14} de Mana. **Atacar** não gasta Mana e, se acertar, devolve {2}."
- **Arqueiro:** "{Tiro Certeiro} gastou {8} de Foco e 1 flecha. **Atacar** também gasta 1 flecha (sem flechas, vira
  um golpe de adaga mais fraco), não gasta Foco e, se acertar, devolve {2}."

O que se devolve é `max(ATAQUE_RECURSO_MIN, 4% do máximo)`; o custo é o da habilidade que a pessoa usou de fato (se
escolheu outra, o texto é o dela).

- **Esc na janelinha** (fecha como sempre): volta para C1. **Voltar na mira:** volta para C2.
- **Escolheu outra habilidade:** C2 encerra do mesmo jeito (o quadro ensina o caminho, não obriga a habilidade).
- **Atacou em vez de abrir Habilidades:** C1 fica até a próxima vez que a roda aparecer nesta luta; se a luta acabar
  antes, a sequência passa para a luta seguinte. Depois de duas lutas sem abrir Habilidades, C1 para (nada de insistir).
- **O golpe acabou com a luta:** C4 não aparece por cima do espólio (o espólio já fecha a luta). A sequência conta
  como cumprida (a habilidade foi usada) e o texto do C4 fica na Ajuda.

### 4.2 Vila e estrada

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| V1 | o Mural (balão do prédio) | "Os prédios da vila são clicáveis. **Mural**: os contratos." | menu do Vau depois de Morel (3.4.1) | o Mural é aberto |
| V2 | Templo e Taverna | "Vida baixa. O **Templo** cura a vida por ouro. **Dormir na Taverna** devolve 35% da vida e todo o {recurso}, e o ensopado da noite substitui a provisão." | menu do Vau com vida < 70% ou recurso < 50% | um dos dois é usado, ou a pessoa sai da vila |
| V3 | provisões no topo (e o Mercado) | "Cada amanhecer come 1 provisão sua e 1 de cada companheiro, na vila ou fora (você tem {4}). Sem provisão, fome. O ensopado da Taverna e o resgate alimentam sem gastar. O **Mercado** vende mais." | primeira vez em Viajar | a viagem começa, ou o Mercado é aberto |
| V4 | o cartão de Morel na Comitiva | "{Morel} luta com você e come 1 provisão por dia. Clique no cartão para conversar." | primeiro menu com Morel no grupo | o cartão é aberto, ou o menu muda |
| V5 | "Explorar a região" | "**Explorar** gasta um período. Pode dar luta, um achado ou nada." | primeira chegada fora da vila | a pessoa escolhe qualquer opção do menu |

### 4.3 Quando chegar

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| E1 | a comparação na janela do item | "▲ e ▼ comparam com o que você veste. **Equipar** troca; **Guardar** leva na mochila." | a primeira janela de equipamento | a decisão do item |
| T1 | Talentos (na doca) | "Você tem {1} ponto. **Talentos** (tecla T) abre a árvore." | o primeiro ponto de talento | a árvore abre |
| N1 | o modificador "Inimigos +1 nível" no topo | "À noite os inimigos vêm um nível acima e batem mais forte. Sem tocha, a luta começa com eles atacando." | a primeira noite fora da vila | a próxima escolha |

**Dormir na Taverna, pelas regras de hoje:** devolve 35% da vida máxima (menos, com fome), todo o recurso, tira os
efeitos de luta, cura o animal, descansa a comitiva e passa a noite com o ensopado para todos (ninguém gasta provisão;
a fome passa). Ferimentos com prazo andam dois dias de cura. **Não** trata infecção nem enfaixa ferida aberta
(Curandeira, bandagem, unguento) e não devolve a vida toda (Templo).

O N1 só depois dos textos da noite corrigidos (feito na 1.65.4, seção 8).

## 5. Desenho, mouse e teclado

**Reaproveitado:**
- a caixa de dica (`telas/dicas.js`) para o estilo do quadro (fundo, borda, fonte), sem o comportamento de seguir o
  mouse;
- o realce que pisca do convite do Mural (`.predio.convite`, 04-pagina.css) e o pulso da bolsa (`.slot-px.trata`) para o
  destaque, com o mesmo cuidado de movimento reduzido;
- as âncoras que já existem: `.roda-botao[data-slot="habilidades"]`, `.rj-linha[data-hab=…]`, `.carta.alvejavel`, a
  barra de recurso da carta do herói, `#predios .predio[data-predio=…]`, o contador de provisões do topo, o cartão da
  comitiva, as opções do menu do lugar (`meta`), `.achado-cartao`, o atalho de Talentos.

**O quadro:** pequeno (até ~260 px), com uma seta discreta apontando para a âncora; abaixo do texto, em letra menor,
"Dispensar orientações". O destaque é um anel claro em volta da âncora. **Na luta, o quadro fica logo abaixo da
arena**, alinhado ao controle (a seta aponta para cima): ao lado do botão ele cobria a carta do primeiro inimigo. Ali
ele pode cobrir uma linha do texto já lido da página; nunca as cartas, as barras, as ações nem a janelinha. Na janelinha
de Habilidades (C2), ao lado da linha.

**O escurecimento:** um véu leve (cerca de 25%) só nas áreas que não importam naquela hora (as colunas laterais e a doca
durante a luta; o texto da cena durante a vila). Nunca sobre a arena, as cartas, as barras do herói e dos inimigos e o
topo. O véu não recebe clique (`pointer-events: none`): tudo continua clicável.

**Mouse:** o quadro não bloqueia nada; clicar fora dele não o fecha (ele fecha quando a ação acontece).
**Teclado:** as teclas de sempre funcionam (1–4 na roda, os números na mira, Esc, Enter); o quadro diz a tecla quando
existe. O foco não vai para o quadro; "Dispensar orientações" é alcançável com Tab. A Ajuda abre com **F1**.

**Movimento reduzido:** sem piscar; o anel fica aceso.

## 6. Pular, fugir, perder, salvar e carregar; os outros caminhos

- **Dispensar orientações:** desliga todas neste save (o quadro some na hora). Religar: na Ajuda.
- **Ajuda** (item no topo, ao lado de Histórico; F1; Esc ou clique fora fecha): a chave "Mostrar orientações:
  ligado/desligado" e a lista do que já foi visto, por grupo (Luta, Vila). Só texto; nada de tour. Num jogo sem a
  abertura (save de antes, mundo gerado), a chave também liga as orientações; a despensa não aparece.
- **Pular o texto** (clique ou tecla que adianta): não afeta os quadros, que aparecem quando a pergunta aparece.
- **Fugir da despensa:** a luta conta como não feita; a ação "Taverna: descer à despensa" volta; as orientações
  continuam na próxima luta.
- **Perder:** contra estes ratos é improvável (critério: em 1000 lutas simuladas por classe, nenhuma derrota). Se
  acontecer, valem as regras do modo (resgate ou fim no hardcore), sem exceção.
- **Salvar e carregar:** guardados no save `tutorial` (ligado ou não) e as orientações já vistas; a cena da despensa e a
  de Morel usam as cenas vistas da missão, como as outras. No meio de uma luta não há save (o autosave é no menu);
  carregado, o que faltava continua na próxima vez que a condição valer.
- **Saves de antes:** sem o campo, a despensa não aparece (a abertura é para campanha nova) e as orientações começam
  desligadas.
- **Outro caminho:**
  - quem sai do Vau sem descer à despensa: a ação fica lá; a primeira luta da estrada recebe C1–C4;
  - quem não fala com Morel: a ação fica no menu até ser usada; a bebida da taverna continua levando a ele, como hoje;
  - quem não abre o Mural: o convite (ou V1) continua até a primeira visita;
  - Odette continua só na estrada e na exploração (evento `odete_na_estrada`, dias 2 a 8 com peso maior); V5 e o motivo
    de explorar aumentam a chance de cruzar com ela sem forçar.

## 7. Arquitetura proposta (mínima)

- **Motor (feito):** `rpg/abertura.py` guarda o estado em `mundo.abertura`, toca o pedido do taverneiro (uma cena,
  depois da abertura da febre), põe "Taverna: descer à despensa" e "Taverna: sentar com o homem do canto" como cartões
  da taverna, cobra zero na primeira caneca e diz a orientação de agora (`para_tela`, em `estado["orientacao"]`). A
  luta de C1–C4 se cumpre quando o herói usa uma habilidade numa luta (o combate conta); duas lutas sem habilidade e
  ela para. O V1 se cumpre ao abrir o Mural. A apresentação de Morel chama o evento pelo motor de eventos
  (`eventos.disparar_id`), que conta como qualquer disparo.
- **Tela (feito):** `app/orientacao.js` acha a âncora, desenha o quadro, a seta, o anel e o véu a cada quadro de
  animação (acompanha mudanças de tamanho e de tela). Os passos C1–C3 seguem o que está na tela; o C4 vem do lance do
  golpe. A rota `POST /orientacao` (`dispensar` ou `ligar`) fica fora da fila das perguntas.
- **Texto (interface de terminal):** a caixa da criação vira uma pergunta ("Mostrar as orientações do tutorial? Sim /
  Não"); o C vira uma linha cinza no começo da luta ("Dica: na sua vez, "Habilidades" abre a lista. ..."), e o V1 uma
  linha na vila ("Dica: o "Mural de contratos" tem trabalho pago.").

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

**Corrigido na 1.65.4** (antes da abertura guiada, com tutorial ligado ou não; encontros, atributos, horários e
consumo iguais):
- a ação de cada sala da capela (nave, sacristia, ossuário) e as escolhas que levam à luta (o sarilho, a guardiã) têm
  uma nota: "Gasta 1 tocha (você tem N)." ou "Sem tocha: o inimigo mais rápido ataca primeiro.", e à noite "Noite:
  inimigos +1 nível e +10% de dano." (na guardiã, só o dano, porque o nível dela não sobe);
- o painel do lugar e o cabeçalho mantêm o nível-base ("Inimigos Nv.3") e dizem ao lado o que a noite soma ("(+1 à
  noite)" no cabeçalho; "Noite: inimigos +1 nível e +10% de dano" no painel), sem dar um nível exato a cada inimigo;
- no escuro, o painel diz o consumo real: "Escuro: explorar, caçar, viajar e cada sala gastam 1 tocha por vez (você
  tem N)", ou, sem tocha, "Percepção e Destreza −4; nas salas, o inimigo ataca primeiro";
- a dica do modificador "Inimigos +1 nível" não promete mais bando onde o tamanho é fixo: "os inimigos dos encontros
  e das salas vêm um nível acima (os guardiões, não). Onde o bando varia, às vezes vem um a mais; nas salas, o número
  é o mesmo. Todos causam 10% mais dano.";
- sem tocha numa sala: "Sem tocha, você entra às cegas: o inimigo mais rápido ataca antes de você." (certo); fora das
  salas continua "emboscadas mais prováveis" (é só probabilidade).

Fica para depois: a frase "A noite cai" também ao acordar à noite na taverna.

## 9. Primeira implementação (escopo mínimo)

1. A caixa "Mostrar tutorial" (web e texto), o campo no save, "Dispensar orientações" e a Ajuda com a chave.
2. A cena da despensa (igual com e sem tutorial) e a ação de Morel na taverna, chamando o evento que existe.
3. Os quadros C1–C4 (primeira luta) e V1 (Mural), com o véu, a seta e o anel.
4. Testes: o mesmo roteiro de ações com e sem tutorial dá o mesmo estado de jogo, as mesmas recompensas e o mesmo
   sorteio (só os campos das orientações diferem); a despensa não se repete; Morel não aparece duas vezes nem reabre
   um recrutamento resolvido; adiar, fugir, perder, dispensar e carregar; os quadros encerram com a ação; a luta
   avaliada nas três classes com várias formas de jogar (seção 12); a fumaça a 1500 e 1280 px, com mouse e teclado.

V2–V5, E1, T1 e N1 numa segunda entrega, depois do primeiro teste com uma pessoa nova. O N1 só depois de corrigir os
textos da noite (seção 8).

## 10. Decisões de Jean (12/10/2026)

1. O XP dos ratos fica; a caneca é uma vez o serviço de bebida e rumores, sem pagar (seção 3.2).
2. O taverneiro fica sem nome nesta etapa.
3. A Ajuda no topo e o F1, com as orientações já vistas e a chave de ligar e desligar o tutorial.

## 11. Critérios para testar com outra pessoa, sem ajuda

Observar (gravar a tela se der), com a caixa marcada, sem dizer nada além de "jogue a campanha":

| # | O que se espera ver | Como saber |
|---|---|---|
| 1 | descobre Habilidades e consegue usar uma quando precisa (na primeira luta, ou quando uma luta aperta) | registro: `habilidades` nas lutas; observação |
| 2 | (indicador, não exigência) em quantas lutas até o nível 3 usou alguma habilidade | registro |
| 3 | clica num prédio da vila nos primeiros 5 minutos | observação |
| 4 | aceita um contrato até o dia 3 | registro (o contrato aparece no Diário; hoje não há linha própria no registro: anotar) |
| 5 | encontra Morel até o dia 3 (aceitando ou não) | registro: `morel_na_taverna` |
| 6 | compra provisões antes da primeira viagem, ou sabe dizer quantas tem | registro e uma pergunta depois |
| 7 | explora pelo menos uma vez até o dia 5 | registro: um evento de "explorar" |
| 8 | sabe dizer, depois, o que a noite muda | pergunta depois (resposta aceita: inimigos mais fortes) |
| 9 | nenhum momento parado por mais de um minuto sem saber o que fazer | observação |
| 10 | se dispensou as orientações, quando e por quê | observação e pergunta |

O que importa é descobrir e conseguir usar uma habilidade quando faz falta. Jogar só com o Atacar numa luta fácil é
legítimo; o indicador 2 serve para comparar pessoas, não para pedir um jeito de jogar.

Comparação: uma segunda pessoa com a caixa desmarcada, se houver. Os números (1, 2, 4, 5, 7) saem do registro da
partida; os outros, de olhar e perguntar no fim, junto da ficha da seção 9 do 17.

## 12. A primeira implementação (1.66.0)

Feito o escopo mínimo da seção 9: a caixa "Mostrar tutorial", o estado das orientações no save, "Dispensar
orientações" e a Ajuda (F1) com a chave, a despensa, a oportunidade de sentar com Morel, C1–C4 e V1. A segunda parte
(V2–V5, E1, T1, N1) não foi feita.

**A luta da despensa, medida** (6000 lutas simuladas: 500 por classe e por forma de jogar; "ao acaso" escolhe entre
Atacar e uma habilidade qualquer, inclusive Meditar ou Marcar Presa, e um alvo qualquer):

| Classe | Forma de jogar | Derrotas | Vida mínima média | Abaixo de 25% | Ferimento | Turnos (máx.) |
|---|---|---|---|---|---|---|
| Guerreiro | só atacar | 0 | 88% | 0 | 4,0% | 4,2 (7) |
| Guerreiro | o roteiro guiado | 0 | 92% | 0 | 4,0% | 3,2 (6) |
| Guerreiro | alternar | 0 | 88% | 0 | 4,0% | 4,0 (6) |
| Guerreiro | ao acaso | 0 | 86% | 0 | 5,8% | 5,0 (11) |
| Arqueiro | só atacar | 0 | 83% | 0 | 5,2% | 4,6 (9) |
| Arqueiro | o roteiro guiado | 0 | 90% | 0 | 2,8% | 3,2 (7) |
| Arqueiro | alternar | 0 | 86% | 0 | 3,6% | 4,1 (7) |
| Arqueiro | ao acaso | 0 | 78% | 0 | 6,2% | 5,1 (10) |
| Mago | só atacar | 0 | 82% | 0 | 4,0% | 4,0 (6) |
| Mago | o roteiro guiado | 0 | 90% | 0 | 3,4% | 2,7 (7) |
| Mago | alternar | 0 | 82% | 0 | 3,6% | 3,9 (6) |
| Mago | ao acaso | 0 | 75% | 1 | 4,8% | 4,6 (11) |

Com dois ratos gigantes comuns (a proposta de antes), o Mago ao acaso perdia 13% das vezes, o Arqueiro ao acaso 6,6%,
o Mago só atacando 0,6%, e o ferimento ia de 6% a 23%. Com um rato só não havia derrota, mas a mira (C3) sumia. Os
ratos da despensa ficaram dois, magros e à vista; o ferimento que sobra vem quase todo de golpe crítico, pela regra de
sempre (não há proteção escondida).

**Caminhos conferidos** (tests/test_abertura.py): o mesmo roteiro com a caixa marcada e desmarcada dá o mesmo jogo
(herói, mundo menos o campo `tutorial`, sorteio, contagem de eventos, ouro, XP, reputação) nas três classes; a
despensa uma vez, com 12 de XP, sem ouro e sem saque; "Agora não" deixa o cartão na taverna; fugir deixa para depois
e não dá a caneca; perder passa pelo resgate e a despensa fica; Morel pela ação conta uma vez e recusado não reabre;
recrutado, encontrado pelos rumores ou fora do grupo, nem a ação nem a fala aparecem; adiar a despensa e achar Morel
pela bebida do dia 2; a caneca é o serviço uma vez (a segunda é paga) e no dia 1 não chama Morel; os textos de C1–C4
pelas regras de cada classe; C cumprido com habilidade e parado depois de duas lutas sem; V1 depois do pedido e até o
Mural; dispensar e religar pela tela; a Ajuda; salvar e carregar no meio (despensa adiada, tutorial desligado, vistas).

**No navegador** (a 1500 e a 1280 px, com mouse e só com teclado, nas três classes): C1 a C4 aparecem e somem com a
ação, sem cobrir carta, barra ou ação (a fumaça confere); a Ajuda abre com F1, desliga e religa na hora, Esc fecha;
"Dispensar orientações" tira o quadro; o V1 aponta o Mural; a caixa da criação vem marcada e desmarcada dá a mesma
abertura sem quadros.

**Limitações:**
- O quadro da luta, abaixo da arena, pode cobrir uma linha já lida da página.
- O C4 não aparece quando a habilidade encerra a luta (fica na Ajuda).
- O véu é leve de propósito (25%) e só nas colunas e na doca.
- A medição é de robôs com formas de jogar simples; só gente nova jogando diz se a orientação ajuda (seção 11).
- `tests.equilibrio` e `tests.replay` não passam pela campanha: a despensa não mexe neles. O começo da campanha ganha 12
  de XP e uma caneca (3 de ouro) para todos, como decidido.

