# 18 — Abertura guiada da campanha (E9): especificação

Especificação da abertura guiada (pedido de Jean, 12/10/2026, sobre a 1.65.3), revista por Jean e ajustada antes da
primeira implementação (seção 12: o que foi implementado e como foi conferido; seções 13 e 14: o acabamento). A segunda
parte (V2–V5, E1, T1, N1) foi feita na 1.67.0 (seção 15); as tabelas da seção 4 trazem os textos finais.

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
   Mural (V1) a partir do menu da vila depois do pedido (despensa feita ou adiada), até o Mural ser aberto. Com o tutorial desligado, o convite que já existe (o balão do Mural
   piscando, sem legenda desde a 1.66.3) continua; com o tutorial ligado, o quadro toma o lugar dele.
2. **Recuperar.** Só se a vida estiver abaixo de 70% ou o recurso abaixo de metade quando o menu da vila voltar: quadro
   no Templo (vida) e na Taverna (dormir). A Curandeira só se houver ferimento.
3. **Provisões.** Na primeira vez que a pessoa abrir "Viajar" (ou clicar na Estrada): quadro no contador de provisões
   do topo e no Mercado, antes de sair. Se ela já tiver comprado, o quadro não aparece.
4. **Morel e o cartão da comitiva.** Na primeira vez que o menu volta com Morel no grupo: quadro no cartão dele.
5. **Explorar.** O motivo, uma vez, na voz de quem está lá: "O dinheiro de verdade está no que ninguém foi buscar.
   Desde que a febre fechou a estrada, tem coisa largada pelo caminho: carroça tombada, trouxa de quem fugiu. Às vezes
   alguma coisa presta; às vezes só tem lobo." O taverneiro diz ao servir a caneca, se Morel não anda com você; com
   Morel junto, é ele quem diz, na primeira vez fora da vila (sem lugar fixo nem achado garantido: os eventos de
   carroça e de achado são os que já existem, sorteados). Na primeira ocasião fora da vila, quadro em "Explorar a
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
| C4 | a barra de recurso na carta do herói | por classe, abaixo | depois do golpe, quando a pessoa pode agir de novo | **Entendi**, ou a próxima ação é escolhida; não aparece se a luta acabou |

Os quadros não repetem a descrição da habilidade: a janelinha e a dica já mostram o efeito e o custo. C4 diz só o
custo e o que o **Atacar** faz, pelas regras da classe (o motor monta as partes com os números da ficha e do
balanceamento; a tela só pinta). Três linhas curtas: o nome da habilidade; o que ela gastou, com o ícone e a cor do
recurso; o Atacar (desde a 1.66.2, seção 13):

- **Guerreiro:** "Golpe Pesado" / "−10 Vigor" / "Atacar não gasta Vigor. Ao acertar, +2 Vigor."
- **Mago:** "Bola de Fogo" / "−14 Mana" / "Atacar não gasta Mana. Ao acertar, +2 Mana."
- **Arqueiro:** "Tiro Certeiro" / "−8 Foco −1 flecha" / "Atacar: −1 flecha, sem Foco. Ao acertar, +2 Foco. Sem
  flechas, vira um golpe de adaga mais fraco."

O que se devolve é `max(ATAQUE_RECURSO_MIN, 4% do máximo)`; o custo é o da habilidade que a pessoa usou de fato (se
escolheu outra, o texto é o dela).

- **Esc na janelinha** (fecha como sempre): volta para C1. **Voltar na mira:** volta para C2.
- **Escolheu outra habilidade:** C2 encerra do mesmo jeito (o quadro ensina o caminho, não obriga a habilidade).
- **Atacou em vez de abrir Habilidades:** C1 fica até a próxima vez que a roda aparecer nesta luta; se a luta acabar
  antes, a sequência passa para a luta seguinte. Depois de duas lutas sem abrir Habilidades, C1 para (nada de insistir).
- **Entendi** fecha só o C4 (o clique e o Enter não escolhem ação da luta); **Encerrar tutorial**, no mesmo quadro,
  desliga todas as orientações (a Ajuda religa).
- **O golpe acabou com a luta:** C4 não aparece por cima do espólio (o espólio já fecha a luta). A sequência conta
  como cumprida (a habilidade foi usada) e o texto do C4 fica na Ajuda.

### 4.2 Vila e estrada

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| V1 | o Mural (o prédio; o quadro numa faixa abaixo do cenário) | "Clique no **mural** para ver os contratos disponíveis." | menu do Vau depois do pedido da despensa (3.4.1) | o Mural é aberto |
| V2 | o Templo (vida, se o ouro dá) ou a Taverna (o recurso; ou a vida, se o Templo não cabe no bolso) | vida: "Vida baixa. O **Templo** devolve a vida toda por {13} de ouro." (+ "Pouco Foco: dormir na **Taverna** ({10} de ouro) devolve todo o Foco e 35% da vida." se o recurso também está baixo); recurso: "Pouca Mana. Dormir na **Taverna** ({10} de ouro) devolve toda a Mana e 35% da vida."; com ferimento: "Ferimentos, a **Curandeira** trata." | menu da vila com vida < 70% ou recurso < 50%, e o serviço ao alcance do ouro | o serviço é usado, ou a viagem começa |
| V3 | provisões no topo | "Cada amanhecer come 1 provisão sua e 1 de cada companheiro, na vila ou fora: dá {2} dias. Sem provisão, fome." (+ "O **Mercado** vende mais." só com menos de 3 dias, na vila) "Dormindo na Taverna, o ensopado é por conta dela." | a primeira escolha de destino (Viajar ou a Estrada) | **Entendi**, ou a viagem começa |
| V4 | o botão **Comitiva** da barra de baixo (desde a 1.67.1; antes, o cartão) | "**Comitiva** abre quem anda com você ({Morel}): conversar, ver a confiança e mandar para o acampamento." | o primeiro menu com alguém na comitiva, presente (reserva e ausência não contam) | **Entendi**, a Comitiva aberta, ou a resposta ao menu |
| V5 | "Explorar a região" | "**Explorar a região** gasta um período. Pode dar luta, um achado, alguém pelo caminho ou nada: é por aí que se acha o que não está nos contratos." | o primeiro menu fora da vila | a resposta ao menu |

### 4.3 Quando chegar

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| E1 | a linha "contra…" do achado | "A linha "contra…" compara o achado com o que você usa (▲ ganha, ▼ perde). **Equipar** veste o novo e guarda o antigo na mochila; **Guardar** leva o novo na mochila." (mochila cheia: "Com a mochila cheia, **Equipar** deixa o antigo para trás.") | o primeiro item achado que você pode usar, com um equipado no lugar | a decisão do item |
| T1 | Talentos (na doca; só a seta: o atalho já acende com ★) | "Você tem {1} ponto de talento. **Talentos**, na barra de baixo, abre a árvore." | um menu com ponto por gastar (gasto antes, não aparece) | **Entendi**, a árvore aberta, ou a resposta ao menu |
| N1 | o aviso "Inimigos +1 nível" no topo | "Noite: os inimigos ficam mais fortes (**Inimigos +1 nível**, no topo)." + fora: "No escuro, a tocha ilumina o caminho; sem ela, ser pego de surpresa fica mais provável. A noite continua perigosa com ou sem luz."; na capela: "Este lugar é escuro também de dia: sem tocha, cada sala começa com o inimigo atacando primeiro. A tocha ilumina, mas a noite continua perigosa." (texto da 1.67.1) | o primeiro menu fora da vila, à noite | **Entendi**, ou a resposta ao menu |

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

**O quadro:** pequeno (até ~290 px; o C4, 360), com uma seta discreta apontando para a âncora; abaixo do texto, em
letra menor, "Encerrar tutorial" (e, no C4, o botão "Entendi"). O destaque é um contorno fino que segue a forma do
controle, com um brilho que pulsa devagar (2,4 s; nada de piscar). **Na luta, o quadro fica numa faixa reservada
logo abaixo da arena** (ou acima das cartas, se ali couber), parado: não acompanha o avanço nem o tremor da carta e
só muda de lugar quando o passo muda ou a janela muda de tamanho. Não cobre cartas, barras, ações, a janelinha nem o
texto da página (seção 13). Na janelinha de Habilidades (C2), ao lado dela, do lado que tem espaço.

**O escurecimento:** um véu leve (cerca de 25%) só nas áreas que não importam naquela hora (as colunas laterais e a doca
durante a luta; o texto da cena durante a vila). Nunca sobre a arena, as cartas, as barras do herói e dos inimigos e o
topo. O véu não recebe clique (`pointer-events: none`): tudo continua clicável.

**Mouse:** o quadro não bloqueia nada; clicar fora dele não o fecha (ele fecha quando a ação acontece).
**Teclado:** as teclas de sempre funcionam (1–4 na roda, os números na mira, Esc, Enter); o quadro diz a tecla quando
existe. O foco não vai para o quadro, menos no C4, em que vai para "Entendi" (Enter ou espaço fecham só o quadro); "Encerrar
tutorial" é alcançável com Tab. A Ajuda abre com **F1**.

**Movimento reduzido:** sem pulso; o contorno fica aceso, parado.

## 6. Pular, fugir, perder, salvar e carregar; os outros caminhos

- **Encerrar tutorial** (antes "Dispensar orientações"): desliga todas neste save (o quadro some na hora). Religar:
  na Ajuda.
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

## 13. Acabamento (1.66.1 e 1.66.2)

Pedido de Jean depois da 1.66.0, antes da segunda parte. Regras, custos, recompensas, sorteio e dificuldade iguais
(gabarito idêntico nas duas versões).

**1.66.1, os riscos da capela em indicadores.** A nota de texto de cada sala virou o nome da ação em destaque e, embaixo,
indicadores curtos com os ícones de pixel do jogo (`sobrevivencia.riscos_sala`, a tela só desenha):

| Situação | Indicador | Dica (ao passar o mouse) |
|---|---|---|
| com tocha | tocha: "−1 tocha" | a sala é escura de dia e de noite; entrar acende 1 tocha (você tem N) |
| sem tocha | tocha apagada, em vermelho: "Sem luz: inimigo age primeiro" | o mais rápido ataca antes de você; Percepção e Destreza −4 |
| noite (sala) | lua, alerta discreto: "+1 nível · +10% dano" | os inimigos da sala vêm 1 nível acima e causam 10% mais dano |
| noite (guardiã) | lua: "+10% dano" | a guardiã causa 10% mais dano; o nível dela não muda à noite |

Os atalhos do sarilho mostram só o que vale para cada um (forçar o mecanismo leva à luta e tem os indicadores; o
caminho da classe, não). A interface de texto lê as mesmas linhas, numa frase. Na barra do topo a 1280 px, a Ajuda e o
modificador da noite cabiam só quebrando a linha: abaixo de 1360 px os botões ficam mais estreitos, sem a tecla.

**1.66.2, os quadros da abertura.**
- **Destaque:** o anel grosso e branco que piscava virou um contorno fino que copia o arredondado do controle, com um
  brilho que pulsa devagar; some quando a ação acontece; um controle por vez; com movimento reduzido, parado.
- **Lugar estável na luta:** os quadros moram numa faixa reservada entre a arena e o texto, com a altura do maior C4
  da classe, criada quando a primeira orientação da luta aparece e tirada quando a luta acaba (ou quando a pessoa
  encerra o tutorial). Se acima das cartas houver espaço (140 px ou mais), vão para lá e a faixa não existe. O lugar
  é calculado só quando o passo muda ou a tela muda de tamanho; o avanço, o tremor e a volta da carta não o mexem. Na
  janelinha de Habilidades (C2), o quadro fica ao lado dela, do lado em que cabe (a 1280 px, à esquerda).
- **C1 a C3** acabam com a própria ação (abrir Habilidades, escolher a habilidade, escolher o alvo). **C4** aparece
  quando o golpe já aconteceu e a roda volta (um momento parado de leitura); tem "Entendi" (fecha só ele; o foco vai
  para ele, e o Enter ou o clique não escolhem ação nem fecham a cena seguinte) e "Encerrar tutorial". Escolher uma
  ação também o fecha. Se a habilidade acaba com a luta, não aparece, e o espólio segue como sempre.
- **C4 em linhas:** o nome; o custo real da habilidade usada com a cor e o ícone do recurso e o nome escrito
  ("−14 Mana"; no Arqueiro também "−1 flecha"); o Atacar pela classe (o que devolve ao acertar; as flechas do Arqueiro).
  Cada habilidade do herói tem o seu (se usou Meditar ou Erguer Escudo, o texto é dela).
- **A cena depois da despensa** espera o "Continuar" (com ou sem tutorial), e o taverneiro diz: "A primeira caneca é
  por minha conta. Se quiser mais trabalho, dê uma olhada no mural de contratos, na praça." Quem já encontrou Morel não
  ouve a apresentação de novo; a caneca e o XP continuam uma vez.

**Conferido:** testes (os quatro C4 pelas classes, a cena com e sem Morel já encontrado), gabarito sem diferença,
pyflakes, fumaça (C1–C4 sem cobrir carta nem ação, o C4 em linhas, "Entendi" sem mudar a pergunta da luta, a cena que
espera o Continuar, "Encerrar tutorial" e religar pela Ajuda). No navegador, nas três classes, com mouse e teclado, a
1500 e 1280 px: a posição do quadro durante os golpes (medida a cada lance: parada), nenhum quadro sobre cartas, barras,
ações, janelinha ou texto visível; o C4 e o "Entendi" (clique e Enter); a habilidade que acaba com a luta (com os ratos
de 1 de vida: nenhum C4, o espólio normal, a sequência contada na Ajuda); a capela de dia e de noite, com e sem tocha;
salvar e carregar sem repetir caneca, XP nem a apresentação de Morel.

**Limitações:**
- A faixa reservada empurra o texto da página para baixo durante a primeira luta guiada (a altura do maior C4 da
  classe; a do Arqueiro é a maior); some quando a luta acaba.
- O C4 só aparece se houver uma próxima vez de agir; quem acaba a luta com a habilidade lê o custo na Ajuda.
- Os indicadores da capela usam ícones que já existiam; o detalhe (quem ataca primeiro, −4 nos testes) fica na dica,
  que no toque não aparece.

## 14. Ajustes pontuais de apresentação (1.66.3)

Pedido de Jean sobre a 1.66.2, para fechar os ajustes da primeira parte. Regras, custos, recompensas, sorteio e
dificuldade iguais; as transcrições do gabarito mudam só nos campos novos que a tela recebe (abaixo).

- **Ícones do C4:** o valor ("−1 flecha", "−14 Mana", "+2 Vigor") deixou de ser um bloco flexível, que subia em
  relação ao texto em volta; agora fica na linha do texto, com o ícone centrado na altura das letras. Medido nas três
  classes, a 1500 e a 1280 px: o centro do ícone a menos de 1 px do centro do número, e o número na mesma linha que
  "Atacar:". Sem espaço sobrando antes da vírgula e do ponto.
- **V1:** "Clique no **mural** para ver os contratos disponíveis." O contorno fica no desenho do prédio; o quadro mora
  numa faixa logo abaixo do cenário, com a seta subindo até o mural. Ele não cobre o desenho nem o nome do prédio, nem
  o texto da página. A faixa entra assim que a vila aparece com o V1 valendo (o texto não pula quando o menu chega) e
  sai quando o Mural abre, quando a pessoa encerra o tutorial ou quando o cenário sai da tela. A posição é refeita só
  quando o passo, o tamanho da janela ou a posição do prédio muda (a câmera da vila assentando). Pelo teclado, o prédio
  recebe foco com Tab e abre com Enter (o menu numerado continua igual).
- **Sem "clique: contratos":** a legenda sumiu do balão do Mural com o tutorial ligado ou não. O nome, a resposta ao
  mouse, o foco e o convite piscando (tutorial desligado, Mural nunca aberto) continuam. Com o V1 à vista, o convite
  descansa: um destaque só sobre o prédio, também quando a pessoa religa o tutorial pela Ajuda na vila e com
  movimento reduzido.
- **Fogueira:** embaixo do palco, a instrução ("Clique num companheiro para conversar ou ajustar a comitiva."), o
  contador ("Comitiva 1/2", do motor), "Vai com você:" e "No acampamento:" por escrito, com o estado de cada um
  ("ferido, fora de combate", na concordância do motor) e, na linha do acampamento, a nota: "Descansa, não come das
  suas provisões e não opina nas suas escolhas." No menu de cada companheiro, a mesma nota vai embaixo de "Deixar no
  acampamento" (e de "Mandar para o acampamento", na Comitiva); quem está no acampamento vê "Fica no acampamento." com
  ela. Sem janela de confirmação nova.
- **Fome fora da barra:** o selo "com fome" saiu de cima da barra de vida. Embaixo das duas barras há uma linha de
  condições, sempre com a mesma altura (a fome chegar ou passar não mexe no painel): ícone e "Com fome" ("Morrendo de
  fome" do terceiro dia em diante), com a dica do efeito de agora, montada pelo motor (`sobrevivencia.condicoes`):
  atributos e vida máxima −10/−20/−35%, descanso devolvendo 30% do normal e ferimentos sem sarar, o que vem se
  continuar e como passa. Os números saem das mesmas constantes que as regras usam (`FOME_FATOR`, `FOME_GRAVE`,
  `FOME_DESCANSO`, `perda_fome`), sem mudar conta nenhuma.

**Gabarito:** as 9 partidas web mudam só em campos novos: `condicoes` no estado do herói, `contador` e
`nota_acampamento` no painel da fogueira, `ferido_txt` no companheiro ferido. Sem eles, cada linha das transcrições é
idêntica (escolhas, lances, herói, painéis); as outras 15 não mudam.

**Conferido:** testes (`test_condicoes`: a dica pelos dias de fome; some ao comer no amanhecer, com o ensopado da
taverna, com comida comprada e no resgate; o contador e a nota vindos do motor; a concordância do ferido), gabarito,
pyflakes, fumaça (o V1 abaixo do cenário e sem a legenda; um cenário novo da fogueira com fome: o rodapé, a nota no
menu, a fome sumindo no amanhecer sem mudar a altura do painel). No navegador, a 1500 e 1280 px, mouse e teclado: o C4
nas três classes; o V1 visível e clicável (mouse e Tab + Enter), com o tutorial ligado, desligado e religado pela
Ajuda; a fogueira com dois companheiros juntos e um no acampamento, e com um junto (ferido) e dois no acampamento; a
fome presente, ausente, depois de dormir e depois de salvar e carregar; a tela Comitiva.

**Limitações:**
- A faixa do V1 (96 px) fica abaixo do cenário também nas cenas da vila antes do menu, enquanto o V1 vale (a cena da
  taverna depois da despensa, por exemplo): troca-se um espaço vazio por um texto que não pula.
- Pelo teclado, chegar ao prédio do Mural com Tab leva muitos toques (o foco passa pelo topo e pelos painéis antes);
  o menu numerado da página continua sendo o caminho rápido.
- A linha de condições mostra só a fome; ferimentos continuam no ícone dos recursos e no painel do herói.

### 14.1 Últimos detalhes (1.66.4)

- **Fome:** a linha embaixo das barras virou uma etiqueta compacta (fundo vermelho escuro, borda discreta, ícone e
  texto claros, 18 px de altura, a mesma da área reservada). "Morrendo de fome" (do terceiro dia) acende mais: fundo
  mais vivo e borda clara (o motor manda `grave`). Dica e regras iguais.
- **Fogueira:** a nota "Descansa, não come das suas provisões e não opina nas suas escolhas." saiu do rodapé; fica no
  menu de cada companheiro, junto de "Deixar no acampamento" (e de "Mandar para o acampamento", na Comitiva). O
  rodapé mantém a instrução, o contador e as listas.
- **Avisos do lugar:** o motor diz o tipo de cada linha (`noite`, `custo`, `perigo`) e a tela pinta: a noite em
  amarelo, o gasto normal de tocha na cor neutra do texto, a falta de luz em vermelho. O painel não mudou de forma.
- **Gabarito:** as 9 partidas web mudam só nos campos novos (`grave` na fome, `tipo` nos avisos do lugar); sem eles,
  as transcrições são idênticas.

## 15. A segunda parte (1.67.0)

Pedido de Jean sobre a 1.66.4: V2–V5, E1, T1 e N1, apresentando o que faz sentido na hora, uma coisa por vez, sem
passeio obrigatório pela tela. C1–C4, V1, a despensa e Morel ficaram como estavam.

**Uma por vez, nesta ordem** (`abertura.proxima`): primeiro o que a tela de agora pede (o item achado: E1; a escolha
do destino: V3); nos menus do lugar, preparar e se recuperar antes de chamar para novidades: V2, N1, V1, T1, V4, V5.
Depois de um "Entendi", a próxima espera a cena seguinte: nada de fila de quadros na mesma tela.

**O que se cumpre não depende da caixa:** o motor marca a orientação como vista quando a ação dela acontece (o
serviço usado, a viagem começada, a árvore aberta, a Comitiva aberta, o item decidido) ou quando a ocasião passa (a
resposta ao menu em que ela valia: noite, comitiva, explorar, talentos). O "Entendi" (V3, V4, T1, N1, as
informativas) também marca. As outras se encerram pela ação. Assim, com a caixa ligada ou não, o jogo é o mesmo, e
quem religa o tutorial pela Ajuda não revê o que já passou.

**Onde cada quadro mora** (nada de controle, barra, personagem ou narrativa por baixo):
- na vila, numa faixa logo abaixo do cenário (como o V1): V2, e o V4 quando o cenário é a vila;
- fora da vila, sobre a paisagem (o cenário fora da vila é só paisagem), do lado do controle: N1, V5, T1 e V4, quando o
  quadro cabe nela; quando não cabe (o cenário encolhe com muito texto na página), na faixa (na 1.67.1, sempre na
  faixa: sobre a paisagem o quadro trocava de lugar durante a leitura, seção 16);
- sem cenário (a escolha do destino), numa faixa no alto da página: V3;
- embaixo, junto da doca, quando o controle mora embaixo e não há paisagem: V5 e T1;
- no item achado, logo abaixo da janela dele, acima do véu: E1.
As faixas entram com a orientação, antes de o texto correr, e só saem quando a cena muda (também depois do
"Entendi"): a página não pula. O quadro fica parado; a posição só muda com a etapa, o tamanho da janela ou o lugar do
controle. Um destaque por controle: o T1 não põe contorno nos Talentos, que já acendem com ★.

**Regras conferidas para os textos:** o Templo devolve a vida toda pelo preço dele (metade do que falta) e não trata
ferimento; dormir na Taverna custa {8 + 2 × nível} (com o desconto da reputação), devolve todo o recurso e 35% da vida
(menos com fome) e serve o ensopado (ninguém gasta provisão naquele amanhecer); cada amanhecer come 1 provisão do
herói e 1 de cada companheiro presente, na vila ou fora; Equipar guarda o antigo na mochila (cheia, deixa para trás);
à noite os inimigos vêm 1 nível acima e causam 10% mais dano, e a tocha só resolve o escuro (Percepção e Destreza,
quem ataca primeiro nas salas).

**Interface de texto:** cada orientação vira uma linha "Dica: …" uma vez por sessão, no menu em que vale (o V1
continua como antes).

**Gabarito:** sem diferença (as 24 partidas não passam pela abertura; nada novo sorteia).

**Conferido:**
- testes (`tests/test_abertura_parte2.py`): o serviço certo para cada falta (vida no Templo, recurso na Taverna, os
  dois, sem ouro nada), o que o V2 não promete, cumprir pelo serviço ou pela partida; as provisões com e sem
  comitiva, com pouca e muita comida, sem nenhuma; o primeiro companheiro (Odette antes de Morel), a reserva que não
  conta, o ferido; explorar e a noite (e a capela escura de dia); os talentos só com ponto por gastar; a ordem; o E1
  só com comparação e a escolha preservada; o motivo de explorar uma vez, pelo taverneiro ou por Morel; o mesmo jogo
  com e sem tutorial nas três classes (dormir, viajar, explorar, voltar); o "Entendi" só nas informativas; salvar e
  carregar com orientações pendentes e cumpridas; a dica de texto uma vez;
- fumaça: um cenário novo (E1 pelo teclado, V2 no Templo, V3 com Entendi sem quadro novo na mesma tela, N1 sobre a
  paisagem e cumprido pela resposta), além dos de antes (C1–C4, V1, fogueira, fome);
- no navegador, a 1500 e 1280 px, mouse e teclado (cenário `tutorial`): cada quadro sem cobrir controle, barra,
  cartão, prédio ou página; V2 com vida baixa, recurso baixo, os dois e ferimento; V3 com e sem comitiva; V4 de Morel
  e de Odette, ferido, na vila e fora; V5 e T1 sobre a paisagem; N1 no Charco e na Capela (sem tocha); E1 sobre a
  janela do item; Encerrar tutorial; tutorial desligado sem quadro nenhum.

**Limitações:**
- Na vila e na escolha do destino, a faixa empurra o texto da página para baixo enquanto a orientação vale (90 a 190
  px, conforme o texto e a largura).
- O "Entendi" de uma informativa e a resposta ao menu valem como vista: quem ignora o quadro não o vê de novo (a Ajuda
  guarda o texto).
- O V2 só aparece com o serviço ao alcance do ouro; sem ouro, nenhum quadro (a dica do Templo e da Taverna continua
  nos cartões dos prédios).
- O V4 fala do primeiro companheiro presente; quem só tem gente no acampamento não vê o quadro até alguém andar junto.
- Teste técnico não mostra que uma pessoa nova entendeu os sistemas: a E9 continua aberta até os testes com gente
  nova (seção 11).

## 16. Interação, posicionamento e feedback (1.67.1)

Primeira de duas entregas pedidas por Jean sobre a 1.67.0. Regras de combate, sorteio e equilíbrio iguais (o
gabarito muda só pelo lance novo da fuga e pelos dois textos corrigidos; sem eles, escolhas, lances e herói
idênticos).

**Reproduzido antes de corrigir, e o que mudou:**
1. **Alvo fora da área visível.** Reproduzido: "Explorar a região" abaixo da dobra com a faixa de baixo, e o quadro
   que aparecia sobre a paisagem e pulava para a faixa quando o cenário encolhia com o texto (posição mudando durante
   a leitura). Agora o quadro de fora da luta só aparece quando o texto da cena terminou; a página rola só o
   necessário para o controle aparecer inteiro, uma vez por etapa (quem rolar depois fica onde rolou); fora da luta o
   quadro mora sempre na faixa (no alto ou embaixo), que entra antes de o texto correr e não troca de lugar. Rolar a
   página não move o quadro (só a posição horizontal do controle conta). Conferido com a página rolada para o alto
   antes de o quadro aparecer, a 1280×800, 1280×640 e 1500×950: o alvo à vista, nenhuma escolha coberta.
2. **Comitiva.** O texto mandava abrir Comitiva e o destaque estava no cartão. Agora o V4 tem um objetivo só: abrir
   a gestão da comitiva. Texto, destaque e seta no botão **Comitiva** da barra de baixo ("**Comitiva** abre quem anda
   com você (Morel): conversar, ver a confiança e mandar para o acampamento."). Quando o botão já acende (✉), fica só
   a seta.
3. **Noite.** Sem "(o detalhe, com o mouse)" nem "a tocha resolve o escuro, não a noite". Fora: "Noite: os inimigos
   ficam mais fortes (**Inimigos +1 nível**, no topo). No escuro, a tocha ilumina o caminho; sem ela, ser pego de
   surpresa fica mais provável. A noite continua perigosa com ou sem luz." Na capela: "Este lugar é escuro também de
   dia: sem tocha, cada sala começa com o inimigo atacando primeiro. A tocha ilumina, mas a noite continua
   perigosa." Nas ruínas sem salas, a surpresa provável.
4. **Textos.** Odette: "uma mulher de roupas chamuscadas", "Você pergunta pelas roupas chamuscadas", "Chamuscadas,
   não queimadas." Lobos no Bestiário: "Caçam em matilha. Durante a luta, seu uivo fortalece o grupo." (o uivo já
   fortalecia os presentes; nenhuma habilidade mudou).
5. **Fuga.** O motor manda um lance `fuga_heroi` (concluída ou não). Concluída: a faixa "Fugiu!" verde, a carta do
   herói sai pela esquerda e some, e um som curto de passos que se afastam (uma vez: os lances não voltam ao
   redesenhar nem ao carregar; segue o som ligado ou desligado). Fracassada: a faixa "Cercado!" vermelha, a carta
   recua um passo e volta. A linha do histórico continua. Sem Continuar, recompensa ou mudança na chance.
6. **Atalhos.** Reproduzido: T abria os Talentos e não fechava (e a árvore aberta travava as outras teclas); I, C, D
   e B abriam e não fechavam, porque a letra no menu do lugar respondia direto, sem a doca saber qual tela abriu. Agora
   a letra faz o que o botão da doca faz, a doca lembra a tela aberta enquanto ela tem Voltar, e a mesma tecla fecha
   pelo Voltar dela (ou, nos Talentos, pelo fechamento da árvore). Mapa (M), Grimório (P), Histórico (H) e Ajuda (F1)
   já alternavam. Tecla segurada não repete.
7. **Adiantar e Continuar.** Reproduzido: depois de adiantar, cliques explícitos no Continuar a cada ~250 ms
   prolongavam a guarda indefinidamente (a cena não avançava). Agora não há guarda de tempo: o gesto que adianta só
   revela e para no Continuar; o próximo clique (ou Enter/espaço) explícito avança na hora. Não contam: o clique cujo
   toque começou antes de a tela aparecer, o segundo clique de um clique duplo, a tecla repetida de quem a segura e a
   tecla que já estava apertada quando a tela chegou (vale também para as escolhas e os números da tela seguinte).
   Nada de Continuar novo onde não havia.

**Conferido:** testes (`tests/test_fuga.py`; V4 e N1 em `tests/test_abertura_parte2.py`), gabarito examinado, pyflakes,
fumaça (com as conferências de adiantar reescritas para a regra nova: clique duplo e Enter segurado revelam e param
no Continuar; um Enter novo continua). No navegador: os casos de adiantar (clique, clique duplo, Enter segurado,
clique duplo no Continuar e Enter segurado nele: uma resposta só, nenhuma escolha atravessada); as teclas T, I, C,
D, B, P, M, H e F1 abrindo e fechando; a fuga ("Fugiu!", a carta saindo, o som uma vez e nenhuma vez ao recarregar).

## 17. Os ciclos básicos (1.68.0)

_Os textos e o posicionamento destes quadros foram revistos na 1.68.1 (seção 18)._

Segunda entrega do mesmo pedido: completar o aprendizado dos sistemas básicos, uma orientação por vez, perto do
alvo, seguindo o estado real. Combate, sorteio e equilíbrio iguais; a única mudança de economia é a autorizada (o
templo). O gabarito não muda (as partidas de referência são do mundo gerado, sem a campanha).

| # | Âncora | Texto | Aparece | Encerra |
|---|---|---|---|---|
| A1 | o botão **Texto** do topo | "Enquanto o texto aparece, um clique ou uma tecla mostra o resto de uma vez (na luta, acelera as animações). **Texto**, no topo (tecla V), deixa tudo mais rápido. Só a apresentação acelera: turnos, custos e escolhas continuam os mesmos." | o primeiro menu depois da primeira luta | **Entendi**, ou a resposta ao menu |
| K1 | **Aceitar** de um contrato de caça adequado, no Mural | "Contrato de caça: {2 bandidos} em {Charco dos Juncos}. **Aceitar** o põe no Diário; cumprido, ele paga {12} de ouro quando você voltar a uma vila." | no Mural, sem contrato aceito, com uma caça (não um alvo de elite) num lugar do nível do herói ou abaixo na oferta de sempre | aceitar um contrato (qualquer um) |
| K2 | a linha do contrato em Contratos, à direita | "O contrato é em **{Bosque do Moinho}**: a linha dele, em Contratos, à direita, e o "!" no mapa mostram onde. Clique na linha (ou em Viajar) para ir." | um menu longe do lugar do contrato seguido (o mais antigo em andamento) | **Entendi**, a resposta ao menu, ou a chegada ao lugar |
| K3 | a ação do contrato no menu ("Caçar … (contrato, 0/3)", "Rastrear …") | "**Caçar** segue os rastros dos {lobos} do contrato: cada um abatido aqui conta ({0/3}), também os que aparecerem explorando." (alvo: "**Rastrear** leva até o alvo do contrato: vencê-lo cumpre o trabalho.") | o primeiro menu no lugar do contrato | a resposta ao menu |
| K4 | a linha do contrato cumprido | "Contrato cumprido. A recompensa ({17} de ouro e {21} XP) é paga quando você chegar a uma vila." | um menu fora da vila com um contrato cumprido e não pago | **Entendi**, a resposta ao menu, ou o pagamento |
| B1 | o baú na **Bolsa**, à esquerda (só a seta: ele já tem o anel dourado) | "Um baú trancado na **Bolsa**, à esquerda: clique nele para abrir." (vários: "um clique abre os {2} de uma vez") | um menu com baú de verdade na bolsa, onde ele abre | abrir |
| SF, S-, S+ | o selo na carta (luta) | "**Firme** ({Lobo}): acabou de se soltar: não pode ser atordoado nem congelado agora." / "**Sangrando** (você): 2 de dano por turno." / "**Esquivo** (você): esquiva +20%." + "O número no selo é quantos turnos faltam (2)." | a primeira vez de cada tipo numa carta, num momento parado da luta (depois da sequência C1–C4) | **Entendi**, ou a ação seguinte |

**Ordem nos menus:** V2, N1, V1, A1, K2, K3, K4, B1, T1, V4, V5 (desde a 1.68.2, o K2 vem antes de todas: seção 19). O Mural (K1), a viagem (V3) e o item achado (E1)
valem na tela deles; os selos, na luta.

**8. Primeiro atendimento grátis no templo** (`Jogo.templo_gratis`, autorizado por Jean): na campanha, a primeira cura
de vida do herói no templo não cobra, uma vez por personagem, com as orientações ligadas ou não. O serviço diz
"Primeiro atendimento — grátis" (o preço, "grátis"); só se gasta quando a cura acontece (entrar no templo ou ler o
quadro, não); a marca vai no save (carregar e religar o tutorial não renovam). A comitiva paga como sempre; nenhum
tratamento novo. O V2 diz que, depois, o preço depende da vida que falta (e, quando já pago, mostra o valor de agora
entre parênteses, não como tarifa).

**9. Um contrato do começo ao pagamento** (K1–K4): os contratos e os estados de sempre (aceito, progresso, cumprido,
pago na chegada a uma vila); nada é gerado, garantido ou recompensado a mais. Desvios: o quadro acompanha o contrato
mais antigo em andamento; abandonado, passa ao seguinte; sem contrato, nada; derrota e resgate seguem as regras (o
cumprido paga na vila do resgate, e isso fecha o ciclo); salvar e carregar continuam do estado real. Pago o primeiro,
o ciclo não se repete. Não segura a história: cada quadro passa com a resposta ao menu.

**10. Primeiro baú** (B1): o primeiro baú de verdade (nenhum é dado para o tutorial); o saque e a comparação seguem
como sempre (o E1 aparece se vier equipamento para comparar).

**11. Selos** (SF, S-, S+): só o que aconteceu na luta (nada é forçado nem sorteado); o efeito de agora, o mesmo da
carta (o dano por turno; a esquiva com o número; Firme pela regra).

**12. Adiantar** (A1): os controles de verdade (o clique ou a tecla durante o texto, que também acelera as animações
da luta, e o botão Texto/V); diz que só a apresentação acelera.

**Conferido:** testes (`tests/test_abertura_ciclos.py`: o templo uma vez, só na cura, só o herói, sem renovar ao
carregar ou religar, igual com e sem tutorial, só na campanha; o contrato adequado e nada quando não há; aceitar
qualquer um; K2→K3→K4 pelo estado; pagamento fecha; abandonar segue o próximo; o menu passa as ocasiões; o baú; a
ordem dos selos com o efeito real; o adiantar só depois da primeira luta), gabarito sem diferença, pyflakes, fumaça
(um cenário dos ciclos: o V2 com o grátis, o serviço "Primeiro atendimento — grátis", a cura sem cobrar, o K1 e o
aceite). No navegador, a 1500 e 1280 px: A1, V2 com o grátis e o cartão do templo, B1 (um e dois baús), K1 no Mural,
K2 na vila (com Entendi), K3 no lugar (respondido pelo teclado), K4 cumprido; os selos nas três classes (chamas no
lobo, sangramento no herói), sem cobrir carta nem ação.

**Limitações:**
- O K1 só aparece se a oferta do Mural tiver uma caça adequada; sem ela, o quadro espera a próxima visita (a oferta
  renova a cada 3 dias).
- Os selos aparecem um de cada tipo; outros estados (congelado, atordoado, barreira) não têm quadro próprio, só o
  primeiro de cada tipo que acontecer.
- A faixa dos selos entra na luta quando o primeiro selo aparece (a página abaixo da arena desce uma vez).


## 18. Revisão pontual (1.68.1)

Pedido de Jean sobre a 1.68.0: textos do tutorial, posicionamento dos quadros e a derrota no cenário de teste. Sem
ampliar o tutorial nem mexer em combate, economia, recompensas ou sorteio; adiantar e Continuar funcionam como na
1.67.1. Os textos da tabela da seção 17 ficam substituídos por estes:

| # | Âncora | Texto |
|---|---|---|
| K1 | o cartão do contrato no Mural (o Aceitar está nele) | "Aceite este contrato para começar." (o cartão já mostra alvo, lugar e recompensa) |
| K2 | o cartão do contrato em Contratos, à direita | "Clique neste contrato para viajar até **{Bosque do Moinho}**." (o clique viaja direto até lá, como o destino no mapa: conferido) |
| K3 | a ação do contrato no menu | "**Caçar** segue os rastros dos {lobos} do contrato. {Lobos} vencidos ao explorar também contam." |
| K4 | o cartão do contrato cumprido | "Contrato cumprido: {17} de ouro e {21} XP, pagos quando você chegar a uma vila." |
| B1 | o baú na Bolsa | "Clique no baú para abrir." (vários: "Clique no baú para abrir os {2}.") |
| SF, S-, S+ | o ícone de efeito na carta | o nome e o efeito de agora, numa linha cada: "**Sangramento**" / "{3} de dano por turno · {2} turnos restantes."; "**Iniciativa**" / "+{25}% de dano no primeiro golpe deste turno."; no primeiro, uma linha a mais: "O número no ícone indica quantos turnos o efeito ainda dura." |
| A0 | o texto correndo; depois, o Continuar | "Clique para mostrar o texto inteiro. Depois, use **Continuar** para avançar." |
| A1 | o botão **Texto** do topo | "Ajuste a velocidade do texto aqui. Atalho: **V**." |
| AL | (a luta, sem controle) | "Clique na tela para acelerar a animação." |
| N1 | os riscos do lugar, à direita (a linha da noite e a da tocha) | "A noite deixa os inimigos mais fortes." + a frase da luz de antes (capela, ruínas, o resto) |

**Textos.** Cada quadro diz a ação de agora; o que o cartão ou a tela já mostram não se repete. Nos efeitos, "ícone"
no lugar de "selo"; a duração se explica uma vez, no primeiro; o "(você)" saiu (o destaque já mostra a carta). O nome
vem de um campo novo do catálogo (`titulo` em `estados.py`: "Sangramento", "Chamas", "Iniciativa"...), e os números
do estado de agora; o texto da Iniciativa na carta passou a dizer "de dano" ("+25% de dano no primeiro golpe deste
turno") e o da Esquiva, "+20% de chance de esquiva". Adiantar foi separado pela ocasião: revelar o texto (A0) com o
texto correndo numa cena que acaba em Continuar (a dica de rodapé "qualquer tecla ou clique adianta o texto" se
esconde enquanto ele está à vista); a velocidade (A1) no botão Texto; acelerar a animação (AL) na luta, com a vez dos
outros correndo, até a próxima ação da pessoa. A0 e AL não entram na fila das outras (não seguram nenhuma).

**Posicionamento.** O quadro encosta no controle, com a ponta da seta nele, quando o controle mora numa coluna (o
cartão do contrato, o baú, os riscos do lugar: dentro da coluna, acima ou abaixo), no topo (o botão Texto, logo
abaixo, sem cobrir as barras do herói; a 1280 px ele estreita para caber à direita delas) ou no Mural (acima do
cartão). Ele acompanha o controle quando a coluna ou a página rola e espera ele voltar se sair de vista; se o
controle começa fora de vista, a coluna rola só o necessário, uma vez. Na luta, o quadro do ícone continua parado na
faixa (as cartas andam e tremem) e ganha uma haste da seta até o ícone; é estreito, para caber ao lado da janelinha de
Habilidades aberta (sem lado livre, espera ela fechar). A faixa da luta cresce uma vez se um quadro maior chega
depois (o do ícone depois do da animação). O A0 mora na faixa de baixo e, quando o Continuar chega, a haste vai até
ele. O N1 saiu do aviso do topo (abaixo dele, o quadro cobria as barras do herói) para os riscos do lugar, à direita,
que já dizem a noite e a tocha.

**Baú.** Com a página esperando Continuar, o clique no baú não abre (o menu ainda não aceita a ação): o B1 só aparece
quando o menu de agora tem a abertura.

**Derrota no cenário `tutorial`.** A luta preparada (`LUTA=`) era chamada antes de `g.rodar()`, onde a derrota vira
resgate; cair nela parava o cenário com `rpg.regras.Derrota: combate`. Agora as lutas preparadas dos cenários passam
por `lutar()` (`tests/navegador/cenarios.py`), que leva a derrota ao `resgate` de sempre e segue o cenário. Nenhuma
regra da campanha mudou.

**Reproduzido antes de corrigir:**
- a derrota na luta preparada (`LUTA=lobo QUANTOS=3 VIDA=0.08`): a exceção no console do servidor e a tela parada;
- nas capturas da 1.68.0: a seta do contrato (K2) e a do baú (B1) apontando dezenas de pixels acima do cartão e do
  ícone (o quadro na faixa do alto, a seta limitada à altura dele); a do Mural (K1) parando no título do quadro de
  contratos, longe do Aceitar destacado; a do ícone de efeito a uns 90 px dele;
- o quadro do sangramento sobre a lista de Habilidades: medido a 1280 px, a janelinha ocupa x 550–800 sobre a faixa,
  e o quadro de 330 px, alinhado ao ícone, ia de 284 a 614;
- o clique no baú com a página esperando Continuar não abre (o menu ainda não tem a ação); o B1 da 1.68.0 pedia só uma
  pergunta qualquer, então aparecia também nesse momento (pela leitura do código).

**Conferido na tela** (1500×950 e 1280×800; o baú e o contrato também a 1280×600):
- K1 no Mural, K2 na vila (antes e depois de rolar a coluna da direita), B1 (um e dois baús; a 600 px a coluna da
  esquerda rola até o baú), A1 no topo, V3 nas provisões, N1 no charco e na capela: a ponta da seta encosta no
  destaque (0 px) e o quadro não cobre ação, carta, barra nem a página;
- o clique no contrato (K2): a viagem começa e chega ao Bosque do Moinho, com a ação "Caçar … (contrato, 0/3)";
- o baú com Continuar pendente: nenhum B1 (aparece o A0); de volta ao menu, o B1 volta;
- os ícones na luta nas três classes (sangramento no herói) e com Morel (Firme no lobo): a haste encosta no ícone;
  com Habilidades aberta, o quadro fica ao lado da janelinha sem cobri-la (com Morel, sem lado livre, espera ela
  fechar); Esc fecha a janelinha e o quadro volta; Entendi fecha;
- o AL durante a animação do lobo, sem seta, na faixa;
- o A0 com o texto correndo, revelado por clique e por Enter (o Continuar chega em ~110 ms) e esperando o texto
  acabar sozinho: a seta passa ao Continuar; depois dele, o A0 não volta;
- a luta preparada: vitória (espólio), fuga (de volta ao menu) e derrota (resgate, de volta ao Vau com o contrato).

**Verificações:** testes (os textos novos, a Iniciativa, o formato dos ícones, a apresentação separada), gabarito
examinado (só o campo `apresentacao` no estado e o texto da Iniciativa na carta; nenhuma escolha, lance ou número
mudou), pyflakes, fumaça completa (com um cenário novo: o A0 e a derrota na luta preparada; o K1 e o K2 conferem a
seta encostando no cartão e a rolagem da coluna).

**Roteiro (PowerShell).** As variáveis ficam valendo na janela até serem removidas: um `LUTA` esquecido põe uma luta
no teste seguinte. Cada linha abaixo limpa antes só as variáveis dos cenários (ou abra uma janela nova por teste):

```powershell
function Limpar-Cenario { 'CLASSE','LUGAR','PERIODO','VIDA','REC','OURO','PROVISOES','TOCHAS','PONTOS','COMITIVA','RESERVA','FERIDO','ITEM','BAUS','CONTRATO','CONTRATO_EM','LUTA','QUANTOS','VISTAS','TUTORIAL','ETAPA','SEMENTE' | ForEach-Object { Remove-Item "Env:$_" -ErrorAction SilentlyContinue } }
Limpar-Cenario; python -m tests.navegador.cenarios tutorial                                    # Texto/V no topo (A1)
Limpar-Cenario; $env:VISTAS="A1"; python -m tests.navegador.cenarios tutorial                  # Mural (K1); "Examinar a fonte nova" mostra o A0
Limpar-Cenario; $env:VISTAS="A1"; $env:CONTRATO="aceito"; python -m tests.navegador.cenarios tutorial   # o contrato à direita (K2): o clique viaja
Limpar-Cenario; $env:VISTAS="A1"; $env:BAUS="2"; python -m tests.navegador.cenarios tutorial   # o baú (B1)
Limpar-Cenario; $env:VISTAS="A1"; $env:LUTA="lobo"; $env:CLASSE="mago"; python -m tests.navegador.cenarios tutorial   # ícones e animação (abra Habilidades)
Limpar-Cenario; $env:VISTAS="A1"; $env:LUTA="lobo"; $env:QUANTOS="3"; $env:VIDA="0.08"; $env:CONTRATO="aceito"; python -m tests.navegador.cenarios tutorial   # derrota e resgate
Limpar-Cenario; $env:VISTAS="A1"; $env:LUGAR="charco"; $env:PERIODO="3"; python -m tests.navegador.cenarios tutorial  # a noite (N1)
```

**Limitações:**
- O quadro encostado numa coluna cobre o vizinho dele (o cartão da missão acima do contrato, os Ferimentos acima do
  baú, o minimapa abaixo dos riscos) enquanto estiver à vista; Entendi ou a ação o fecham.
- A haste do ícone pode cruzar outra carta da mesma coluna (2 px), quando o ícone é da carta de cima.
- Com Habilidades aberta e o ícone atrás da janelinha, o quadro espera ela fechar.

## 19. Três correções (1.68.2)

Pedido de Jean depois de testar a 1.68.1. Sem ampliar o tutorial nem mexer em combate, recuperação, economia ou
sorteio.

**1. O contrato aceito.** *Reproduzido* no fluxo real, desde a criação: a despensa com a habilidade (C1–C4), a vila
(V1), o Mural, aceitar, Voltar, sem outra ação. De volta à vila, aparecia o A1 (o botão Texto), que ainda não tinha
sido visto e vinha antes do K2 na fila; o K2 só vinha depois de uma resposta ao menu (o Passear), que passava o A1.
Começar o cenário com `CONTRATO=aceito` não mostrava isso. *Corrigido:* o K2 vem antes de todas as orientações do
menu (é a consequência do que a pessoa acabou de fazer) e passa, como antes, na primeira resposta ao menu ou no
Entendi; as outras seguem na ordem de antes. Dentro do Mural nada muda: o cartão à direita só viaja fora dele, o
Mural não fecha sozinho, outros contratos continuam podendo ser aceitos e nenhum quadro cobre a mensagem do aceite.

**2. Entendi no quadro da animação (AL).** O quadro ganhou o Entendi (Encerrar tutorial continua ao lado, menor). Ele
recebe o foco ao aparecer: Enter ou espaço fecham só o quadro, sem adiantar a animação nem escolher ação; o clique
nele também (o quadro é dele); o segundo clique de um clique duplo não escolhe nada na roda (a guarda do Gesto). A
luta não espera: sem Entendi, o quadro fica da vez dos inimigos até a próxima ação do herói, e um ícone de efeito
novo espera ele sair (antes, o ícone o tirava da tela). Se a luta acaba com ele à vista, ele volta na próxima.

**3. A derrota.** *Reproduzido:* a luta acabava, a arena sumia e ficava a vila clara, com o herói em 0 de vida, "Você
tombou diante de…" e o Continuar. *Corrigido:* na derrota que encerra a luta (`Combate.fim`), o motor manda
`celebrar("derrota", {morte})`, ainda com a arena à vista; a tela faz uma sequência curta (~1,3 s, adiantável pelo
clique ou tecla de sempre): a carta do herói afunda, inclina e se apaga; a tela pulsa vermelho (a mesma camada da
dor); a faixa diz "Você caiu" (vem o resgate) ou "Você morreu" (modo hardcore); um som curto (baque e três notas
graves), que respeita o botão de som. Depois, o cenário fica escuro e sem os prédios enquanto o herói está caído; a
luz volta com o amanhecer do resgate (quando o painel já mostra o herói tratado) ou com o próximo menu (o título,
depois da morte). A Pena de Fênix e a proteção do mendigo, que levantam o herói, não chegam a `Combate.fim`: nada
disso aparece. Nenhuma penalidade, recuperação ou estado do herói mudou; nenhum Continuar novo. No replay (recarregar
a página no meio) e no texto instantâneo, só o escuro, sem som nem faixa. O histórico ganha "▸ Você caiu" / "▸ Você
morreu".

**Cenário de teste:** `tutorial` aceita `HARDCORE=1`, `PENA=n` e `PROTECAO=mendigo`; a morte no hardcore, já na luta
preparada, vai ao título como no jogo.

**Conferido na tela (1500 e 1280 px):**
- o fluxo real desde a despensa: aceito o contrato e Voltar, o K2 na hora, com a seta no cartão;
- o AL: aparece com a vez dos lobos, o foco no Entendi; Enter, clique e clique duplo fecham só ele (a vez do herói
  chega no mesmo turno, sem ação escolhida, e ele não volta); sem Entendi, fica até a ação do herói e então sai;
- a derrota com resgate: a faixa "Você caiu" com a arena à vista, a carta caída, o pulso vermelho, o cenário escuro
  com o herói em 0 e o Continuar de sempre; o "Tudo escurece…" com o amanhecer, a luz de volta, o menu do Vau;
- a morte no hardcore: "Você morreu", a cena da morte no escuro, o título;
- a Pena de Fênix e o mendigo: o herói em 0, de pé com 30, a vitória; nenhuma faixa de derrota, nenhum escuro;
- vitória e fuga como antes; com o tutorial desligado, a mesma derrota;
- o som: uma vez por derrota; recarregando a página no meio da queda, nenhum som nem faixa de novo (o escuro fica).

**Verificações:** testes (o K2 antes do A1 e do V2 logo depois do aceite), gabarito examinado (só a linha nova
`CELEBRAR derrota` antes de cada queda, 37 nas 24 partidas; nada mais mudou), pyflakes, fumaça completa (com o AL pelo
teclado e a faixa e o escuro da derrota). Duas rodadas completas pararam no cenário da fogueira (o botão "Dormir até o
amanhecer" flutua sem parar, a animação `boiar`, e o clique do teste esperava ele ficar parado); sozinho, ele
passava. O teste agora clica sem esperar a parada (o botão anda 4 px e o clique no centro o acerta); a rodada
completa seguinte passou inteira.

**Limitações:**
- O som "morte" da carta (quando a vida chega a 0, de antes) toca junto do novo, um pouco antes dele.
- Fora do combate (a fome e a infecção que derrubam), não há a sequência: o pedido é só para a derrota da luta.

## 20. Ferimentos, descanso e o fim da derrota (1.69.0)

Pedido de Jean: concluir o fluxo visual da derrota e apresentar ferimentos, tratamentos e descanso. Combate, sorteio e
regras de recuperação iguais; a única mudança de economia autorizada é o primeiro tratamento grátis de um ferimento do
herói na curandeira.

**1. Da derrota ao resgate.** *Reproduzido:* a faixa "Você caiu" sumia em ~1,3 s e ficava a página dos registros da
luta, rolada para baixo, com "Você tombou diante de…" e um Continuar. *Corrigido:* a queda dura ~2,2 s (a faixa, ~2,6
s), adiantável como antes; depois, a cena do resgate (ou da morte) abre página nova, com a rolagem no início, sem a
confirmação dos registros (`WebUI.depois_da_queda`: a troca de cena seguinte à derrota não para para ler). Nada do
resgate deixa de acontecer (ouro, dias, tratamentos, contratos, estado); os registros da luta ficam no Histórico. A
recuperação segue como já era: o amanhecer, o texto do despertar e, na volta à vila, a página que vira sozinha. No
Hardcore, a cena da morte, com o Continuar dela, e o título. A Pena de Fênix e a proteção continuam sem derrota.

**2–5. Ferimentos.**

| # | Âncora | Texto (números do ferimento real) | Aparece | Encerra |
|---|---|---|---|---|
| F1 | o ferimento na ficha (Ferimentos, à esquerda) | "**{Corte profundo}** fica na ficha depois da luta (não passa como o sangramento): {−10% Vida}. {Sara em 4 dias de descanso, mas, aberta, pode infeccionar à noite. A **Curandeira** trata na hora.}" (infecção: "Não passa sozinha: um unguento cura, e a Curandeira trata na hora.") | o primeiro menu fora da luta com um ferimento (na luta, espera) | **Entendi** ou a resposta ao menu |
| F2 | a bandagem da bolsa | "A bandagem protege a ferida contra infecção. O ferimento ainda precisa sarar." (duas abertas: "Cada bandagem enfaixa uma ferida, a começar por **{Mordida dilacerada}**.") | a primeira ferida aberta sem bandagem, com bandagem na bolsa e o menu aceitando o uso | usar a bandagem, ou a resposta ao menu |
| F2 (sem bandagem) | a ferida na ficha | "Sem bandagem, a ferida aberta pode infeccionar a cada noite. O **Mercado** vende bandagens; a Curandeira trata na hora." | o mesmo, sem bandagem | **Entendi** ou a resposta ao menu |
| F3 | o prédio da Curandeira | "A **Curandeira** trata ferimentos na hora; o Templo só recupera vida. O primeiro tratamento é grátis." | na vila, com um ferimento | entrar nela, ou a resposta ao menu |
| F4 | o cartão do ferimento do F1, na cabana | "Clique no cartão para tratar **{Corte profundo}** agora: o primeiro tratamento é grátis." (depois: "custa {15} de ouro") | dentro da cabana | tratar ou sair |

Nada provoca ferimento nem muda a chance dele. A bandagem nunca aparece para fratura, concussão ou infecção (o F2 espera
a primeira ferida aberta). A bandagem enfaixa a primeira ferida aberta da lista, sem escolha: o quadro diz qual, e a
dica da bolsa passou a dizer só essa (antes, "Trata: corte profundo e mordida dilacerada" prometia as duas). Depois do
uso, a ficha mostra a ferida sem "aberto" (o estado confirma; nenhum aviso a mais). Se o ferimento sara ou o resgate o
resolve antes, as orientações que pediam tratamento não aparecem (seguem o estado de agora).

**Primeiro tratamento grátis** (`abertura.curandeira_gratis`): na campanha, uma vez por personagem, com as orientações
ligadas ou não. Enquanto vale, cada cartão diz "Primeiro tratamento — grátis"; a pessoa escolhe qual; só um sai de
graça e só quando o tratamento acontece (abrir, sair, salvar, carregar ou religar não gastam nem renovam). Depois, os
outros cartões voltam ao preço de sempre na mesma tela. Separado do grátis do templo; nenhum preço mudou.

**Descanso.**

| # | Âncora | Texto (números das regras de agora) | Aparece | Encerra |
|---|---|---|---|---|
| D1 | o cartão Dormir, na taverna aberta | "Dormir aqui custa {10} de ouro e vai até amanhã: devolve {21} de vida e todo o {Vigor}. O ensopado é por conta da casa: nenhuma provisão gasta." (+ "Com fome, a vida volta menos."; com ferimento: "Descansar ajuda os ferimentos a sararem com o tempo; a Curandeira trata na hora.") | a taverna aberta, sem outra orientação à vista (não segura a fila: a tela acha a ocasião) | **Entendi** ou dormir |
| D2 | o Acampar do menu | "**Acampar** monta a fogueira aqui; lá, dormir passa a noite e recupera vida e {Vigor}." | fora da vila, com vida ou recurso a recuperar, depois das outras | acampar, ou a resposta ao menu |
| D3 | o Dormir até o amanhecer, na fogueira | "**Dormir até o amanhecer** devolve {18} de vida e {22} de {Vigor}; o amanhecer come 1 provisão sua (e 1 de cada companheiro) (você tem {3})." (mau tempo: "a vida volta menos"; sem provisão: "você acorda com fome"; fome e ferimentos como no D1) | na fogueira | **Entendi** ou dormir |

Os números saem de `abertura.recuperacao`, a mesma conta de `Tempo.descansar` (a fome multiplica a vida; o recurso,
não). Ordem nos menus agora: K2, F1, V2, N1, V1, F2, F3, A1, K3, K4, B1, T1, V4, V5, D2; na fogueira, F1, D3, B1, F2. O
V2 deixou de citar a Curandeira (é o F3, com a diferença para o Templo).

**Posição.** A haste da seta vale também para os prédios da vila e para as opções acima da faixa de baixo (o quadro
continua parado na faixa, a ponta encosta no alvo). Na bolsa, o quadro fica abaixo do espaço quando cabe (acima ficam os
ferimentos que a bandagem trata). Na página, quando não cabe acima, ele sobe sobre o cenário em vez de descer sobre o
Voltar e a doca.

**Cenário de teste:** `tutorial` aceita `FERIMENTOS=corte,costelas`, `BANDAGENS=n` e `FOME=n`.

**Conferido na tela (1500 e 1280 px):**
- a derrota: a faixa ~2,6 s, a página do resgate limpa e no topo, nenhum Continuar com o herói em 0, os registros no
  Histórico; no Hardcore, a cena da morte e o título;
- F1 e F2 com bandagem (a seta na ferida e depois na bandagem; usada, a ficha mostra a ferida tratada), sem bandagem (a
  alternativa, na ferida, sem destacar item), com concussão (sem bandagem) e com infecção (unguento ou Curandeira);
- a Curandeira com dois ferimentos e zero de ouro: F3 no prédio (a haste até ele), F4 no cartão, os dois cartões com
  "Primeiro tratamento — grátis", um tratado de graça, o outro de volta aos 15 de ouro sem sair da tela; com o tutorial
  desligado, nenhum quadro e o grátis igual;
- o descanso, vida e recurso antes e depois: taverna 30 → 51 e o Vigor cheio (com fome, 30 → 36); acampamento +18 de
  vida e +22 de Vigor, 1 provisão (com fome, +5; com Morel e Odette, 3 provisões); os números iguais aos do quadro.

**Verificações:** testes (`tests/test_abertura_feridas.py`: F1–F4, a bandagem na primeira ferida, o grátis uma vez só,
com zero de ouro, separado do templo, sem renovar ao carregar ou religar, só na campanha; D1–D3 com os números e a
fome; nada com o tutorial desligado), gabarito examinado (só os campos novos `contextuais` e o `id` dos ferimentos),
pyflakes, fumaça completa (um cenário novo: F1, F2, a Curandeira e o D1; a derrota sem o Continuar dos registros). O
teste da curandeira do Vau (`test_retorno`), que confere o preço de sempre, agora marca o grátis como já usado.

**Limitações:**
- Depois de um Entendi, a próxima orientação espera a cena seguinte (como sempre): o F2 vem depois de o jogador fazer
  alguma coisa.
- A recuperação do resgate vira a página sozinha na volta à vila (como já era); o texto do despertar fica o tempo de ler.


## 21. Acabamento dos textos e da apresentação (1.69.1)

Pedido de Jean, sobre a 1.69.0: acabar textos e apresentação sem acrescentar etapas nem mexer em regras, recuperação,
preços, benefícios gratuitos ou sorteios. Critério: **o quadro ensina a ação; o cartão mostra custo e resultado; a Ajuda
guarda os detalhes.**

**1. Curandeira.** O F4 diz só a ação, com o ferimento real em linguagem natural: "Clique neste cartão para tratar o
corte." (o nome curto mora em `FERIMENTOS[...]["curto"]`: o corte, a mordida, as costelas, o braço, a perna, a
concussão, a queimadura, a infecção). O grátis fica no cartão ("Primeiro tratamento — grátis"). Saiu a fala "Ela não
cobra: é o seu primeiro tratamento aqui." (a narração seguinte e o cartão já dizem); o retorno do tratamento ficou igual.

**2. Templo.** O V2 do Templo fala só do Templo: "O **Templo** recupera sua vida. Seu primeiro atendimento é grátis."
enquanto o benefício vale; depois, só "O **Templo** recupera sua vida." Taverna, Vigor, fome e hospedagem saíram dele.
Quando o alvo é a Taverna (vida cheia, recurso baixo): "Dormir na **Taverna** recupera {todo o Vigor | todo o Foco | toda
a Mana} e parte da vida." O preço que depende da vida que falta ficou na Ajuda.

**3. Dormir na Taverna.** O cartão Dormir passou a mostrar os dados em linhas curtas, com os ícones e as cores dos
cartões:

    Dormir até o amanhecer
    Custo: 10 ouro
    Recuperação: +21 vida · Vigor completo
    Provisões: nenhuma consumida

Os números e o nome do recurso vêm de `Tempo.linhas_descanso("taverna")`, com a mesma conta de `Tempo.descansar`
(`Tempo.previsao_descanso`). Vida cheia: só "Vigor completo" (sem "+0 vida"). Com fome, "Recuperação de vida reduzida
pela fome." só quando a fome de fato reduz (vida cheia: sem a nota). Com ferimento: "Ferimentos: o descanso ajuda a
sarar com o tempo." Saiu "O ensopado é por conta da casa" (no cartão, na Ajuda e na nota de provisões do V3): fica o
fato, "nenhuma provisão é consumida". O D1 diz só a ação: "Clique neste cartão para dormir aqui até o amanhecer." (com
ferimento: "A Curandeira trata ferimentos na hora.", apagado), sem repetir o cartão.

**Zero com vida faltando:** não acontece no nível 1. A menor conta é a da fogueira com mau tempo e fome (18% × 30% da
vida máxima); com a menor vida máxima do nível 1 (o mago, 42), dá 2. O teste `test_nunca_zero_com_vida_faltando`
confere as três classes.

**4. Acampamento.** D2: "Acampe para montar uma fogueira. Lá, você pode dormir para recuperar vida e {Vigor | Foco |
Mana}." Na fogueira, o D3 destaca o Dormir e mostra as mesmas linhas:

    Dormir até o amanhecer
    Recuperação: +18 vida · +22 Vigor
    Provisões: 3 consumidas (você e 2 companheiros) · restam 0

Provisões de verdade: sem comitiva, "1 consumida · restam 2"; sem provisão, "nenhuma: você acorda com fome" (ou "todos
acordam com fome"); se não dão para todos, "{n} consumidas: não dão para todos". As condições só quando afetam esta
noite: a fome que reduz a vida, o mau tempo que reduz a vida, e os ferimentos ("o descanso ajuda a sarar com o tempo";
sem provisão, "Ferimentos: sem comer, não saram esta noite."). Recuperar vida e um ferimento sarar seguem separados.

**Achado na revisão:** a nota antiga dizia "com fome, os ferimentos não saram" sempre que o herói estava com fome. No
amanhecer a comida vem antes dos ferimentos: na Taverna (o ensopado) e na fogueira com provisão, o herói come e o
ferimento sara. A nota agora segue isso (teste `test_ferimentos_saram_quando_ha_comida`).

**Posição.** Na fogueira, o quadro do D3 (mais alto, com as notas) cobria a comitiva a 1280 px. Agora ele fica à
esquerda do botão, sobre o céu, mais largo (até 420 px) para caber em menos linhas: não cobre o herói, os companheiros
nem os nomes deles.

**Conferido na tela (1500 e 1280 px):**
- Curandeira com corte, costelas e perna e 100 de ouro: o F4 "Clique neste cartão para tratar o corte."; os três
  cartões com "Primeiro tratamento — grátis"; depois do primeiro, os outros a 15 (100 → 85 → 70); uma mensagem de
  tratamento por vez, sem sobreposição;
- Templo com o benefício (com a frase do grátis) e já usado (sem ela); a Taverna como alvo (o mago com pouca Mana);
- cartão Dormir nas três classes, com vida cheia e faltando (+21 vida · Vigor completo; +18 · Foco; +14 · Mana), com
  fome (+6 vida e a nota) e com fome de vida cheia (sem nota), com ferimento;
- fogueira nas três classes com recurso baixo (+22 Vigor, +18 Foco, +20 Mana), vida cheia e faltando, com fome, sem
  provisão e com ferimento, sem comitiva, com Morel e com Morel e Odette (3 provisões): o quadro sem cobrir figuras.

**Verificações:** testes (`test_abertura_feridas`, `_ciclos`, `_parte2`: textos novos, as linhas iguais à conta do
descanso, a fome só quando reduz, nunca zero, os ferimentos com e sem comida), gabarito examinado (só o meta do Dormir:
`curto` e `linhas` no lugar de `efeito` e `tempo`; nenhuma outra linha), pyflakes, fumaça completa.
