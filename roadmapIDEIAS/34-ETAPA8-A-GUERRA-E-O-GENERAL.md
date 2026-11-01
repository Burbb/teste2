# 34 — Etapa 8: a guerra nova, as variações dos heróis inimigos e o General (Campo Livre 9)

**01/11/2026. Protótipo, nada no jogo.** O jogo integrado não muda. A versão **Campo Livre 9** abre na raiz do servidor do
protótipo (`ferramentas/prototipos/etapa8-campo/`, `demo.bat`); o Campo Livre 8 fica congelado em `tela-v8/` e abre em
`/v8/` para comparar. O estudo anterior, sobre o Harg resistente e os modelos dos heróis, é o
[33](33-ETAPA8-HARG-E-OS-MODELOS-DOS-HEROIS.md); a série do campo livre está no [30](30-ETAPA8-CAMPO-LIVRE.md).

## 0. A mudança de direção (aprovada pelo Jean)

Jogando o Campo Livre 8, o Jean achou que os duelos com os heróis inimigos continuavam demorados e pouco divertidos. A
direção aprovada, que substitui a do 33 (cada herói comum como um duelo prolongado):

- **Os heróis inimigos comuns ficam frágeis e letais:** confrontos rápidos no meio da guerra, não barras longas.
- **Variações sorteadas** mudam as habilidades e as ameaças de cada herói (uma ou duas por herói).
- **Mais variedade de tropas** nas ondas.
- **Sem fuga automática** das tropas inimigas.
- **O General:** depois de derrotados todos os inimigos previstos, aparece um General maior e muito mais forte, com
  áreas grandes, controles e execuções rápidas. É o confronto final; **a vitória é a queda dele.**
- **Inabalável** (imune a controle e empurrão) foi pedido explicitamente nesta direção e fica, apesar das recomendações
  anteriores contra imunidade genérica.

O resto deste estudo separa o que está **aprovado** (a direção acima), os **números provisórios** (todos os da seção 2
em diante) e as **questões para o Jean** (seção 9).

## 1. Como jogar

- **Abrir:** `demo.bat` (ou `python ferramentas/prototipos/etapa8-campo/servidor.py`). O título da aba, o topo da escolha e
  o selo dizem **Campo Livre 9**; na luta, o selo mostra também o número da guerra ("guerra nº 48213").
- **A guerra** ("A guerra", o encontro inicial): o seu exército, Morel e Odette diante do portão; ondas a cada 11 s até os
  90 s; os três heróis inimigos entram aos 20, 46 e 72 s (o último com duas variações); com o campo vazio, o General
  atravessa o portão.
- **O treino** ("Treino: os heróis e o General"): só você; os três heróis um por vez (cada um 2 s depois de o anterior
  cair), a sua vida volta cheia a cada um e de novo quando o General entra.
- **`R`** começa outra guerra com **outro sorteio**. **`T`** repete **a mesma guerra**: o mesmo número, o mesmo herói e a
  mesma montagem (também nos botões da pausa e do fim). `?sorteio=N` no endereço começa pela guerra de número N.
- **As opções** ficam numa chave própria do 9 (`campo-livre-9-opcoes`): as do 8 não são lidas (o encontro, o herói e a
  montagem de antes não entram por engano).

## 2. A guerra (campo9.js; os números em conteudo.js)

**O sorteio.** Um número por guerra decide as ondas (o pelotão de cada uma), a ordem dos três heróis e as variações; o
acaso da luta usa o mesmo número. Mesmo número e mesmas ações: a mesma guerra (um teste confere).

**As ondas.** Oito, alternando portão, norte e sul; cada uma sorteia um pelotão:

| Pelotão | Composição (× a escala) |
|---|---|
| Soldados e lanceiros | 18 soldados, 10 lanceiros |
| Furiosos e cães | 14 furiosos, 10 cães |
| Besteiros atrás dos pesados | 6 pesados, 10 soldados, 10 besteiros |
| Sapadores no meio da infantaria | 16 soldados, 6 sapadores, 4 veteranos |
| A matilha | 22 cães |
| Cavalaria e lanceiros | 10 cavaleiros, 6 lanceiros |
| Infantaria e arqueiros | 14 soldados, 6 veteranos, 8 arqueiros |

**As tropas novas** (só do lado inimigo; as figuras são provisórias, para identificação, não arte aprovada): o
**lanceiro** (a lança alcança 12 px, por cima da primeira fila; golpe lento), o **besteiro** (atira pouco e forte: 6, 9
no herói), o **furioso** (corre a 50 e bate rápido, sem armadura), o **cão de guerra** (o mais rápido do campo, 68; cai
com qualquer golpe) e o **sapador** (leva o barril até o grupo nosso mais perto, acende o pavio e o barril explode 0,9 s
depois, ferindo os nossos; **derrubado, o barril cai e explode 0,45 s depois ferindo qualquer lado**: derrubar o sapador
no meio dos dele leva os dele junto).

**Os heróis inimigos, frágeis e letais.** Caem em segundos de ataque; cada golpe anunciado tira um quarto a um terço da
sua vida.

| Herói | Vida | O que dói (no herói) |
|---|---|---|
| Harg, o Capitão | 320 (era 1700) | Talho 27, Varredura Longa 40, Martelada 58, Investida 36, Rodopio 40; sem a fase 2; postura curta |
| Ardis, a Feiticeira de Guerra | 200 (era 600) | Coluna de Fogo 42, Corrente Arcana 24; o dardo a cada 1,8 s (12); o Passo Sombrio a cada 9 s |
| Vesna, a Lâmina (nova) | 200 | Corte Duplo 24 (0,32 s), Leque de Facas 22 (três faixas estreitas a ±20°), Bote 30 (pela linha; depois, aberta +50%); colada em você, some e reaparece a 95 px (a cada 5 s) |

**As variações** (uma ou duas por herói, sem repetir no mesmo herói):

| Variação | Regra | Símbolo (forma + cor) |
|---|---|---|
| Gélido | cada golpe deixa lento 2 s; dois acertos em 4 s congelam (atordoado 0,9 s, pela proteção contra repetição) | floco, azul-claro |
| Inabalável | não fica atordoado, preso, lento nem provocado, não é empurrado, a postura não quebra; só o dano o derruba | escudo, areia |
| Venenoso | cada golpe envenena: 3 de dano por segundo por 3 s, até 3 doses | gota, verde |
| Rastro Explosivo | as investidas, os saltos e os sumiços deixam cargas que explodem 0,8 s depois (só nos nossos) | estilhaços, laranja |
| Vampírico | recupera metade do dano que causa (não com o veneno) | presas, vermelho |
| Implacável | anda 25% mais rápido; recargas e pausas passam 60% mais rápido (Ardis no máximo a 62, abaixo do Mago) | setas duplas, amarelo |

## 3. O General

Grande (o maior do campo), 3000 de vida, postura 380 (quebra: 3 s de joelhos levando +50%), anda a 58 (70 longe de
você). A mesma máquina de golpes de Harg (preparação no chão, execução rápida, recuperação), com golpes em estágios, o
salto no ponto do alvo, o puxão e os controles no contato.

| Golpe | Forma | Preparação → estoura | Dano no herói | Depois |
|---|---|---|---|---|
| Ceifa | arco de 150°, 42 px (com o avanço de 10) | 0,40 → 0,48 s | 34 | — |
| Estocada | faixa de 150 × 20 px | **0,40** (era 0,30) → 0,47 s | 30 | — |
| Correntes | faixa de 210 × 18 px | 0,38 → 0,44 s | 10, puxa até a frente dele e prende 0,35 s | a Estocada com 0,55 s de preparação |
| Terremoto | três anéis: 0–58, 58–118, 118–185 px, a cada 0,3 s | 0,55 → 0,55 / 0,85 / 1,15 s | 26, atordoa 0,8 s | aberto 0,9 s |
| Salto | círculo de **56 px** (era 60) onde você estava | 0,70 (segue você só no primeiro **quarto**, era a metade) + **0,45 s no ar** (era 0,28) → 1,15 s | 40, atordoa 0,8 s | aberto 1,1 s |
| Brado Gélido | círculo de 220 px (abre a fase 2, abaixo de metade da vida) | 0,70 s | lento 50% por 2,5 s | — |
| Cruz de Lâminas (fase 2) | a cruz e depois o X, braços de 300 × 22 px | 0,55 → 0,55 / 0,90 s | 32 | — |

As sequências (fase 1): Ceifa e Estocada; Correntes; Ceifa e Ceifa; Terremoto; Estocada e Ceifa. Na fase 2, mais longas
(até três golpes) e com pausas de 0,3–0,5 s (eram 0,5–0,8). O Terremoto também vem contra a tropa que o cerca.

**O que mudou nesta sessão e por quê:** a Estocada e o Salto não tinham saída a pé para ninguém mirado (a seção 7); só
os tempos mudaram (o dano, as áreas, as pausas e as sequências ficaram).

## 4. A leitura na tela

- **O aviso é o que acerta.** O contato dos golpes da máquina (Harg, Vesna, o General) passou a usar exatamente as formas
  mostradas no chão. Antes, o aviso ficava no pé dele e o golpe acertava depois do avanço (até 30 px adiante na Varredura
  Longa). O avanço do Talho ficou em 13 px: a tabela dizia 16, mas a conta por passo só andava 13, e foi esse o alcance
  jogado. As cargas usam a mesma regra do círculo desenhado (antes, metade do corpo de quem estava na borda contava).
- **Golpes em estágios:** todos os estágios aparecem desde o começo; o próximo a estourar enche e tem a borda cheia; os
  seguintes ficam claros, com a borda tracejada. Cada forma pisca ao estourar. O Salto continua marcado enquanto ele está
  no ar. O Leque mostra as três faixas.
- **Cargas e barris:** o círculo enche até explodir; o barril aceso (fere os nossos) tem a borda laranja; o barril caído
  (fere qualquer lado) tem a borda listrada de amarelo e preto; o barril e o pavio aparecem no chão.
- **A corrente** fica desenhada entre o General e quem ele puxou enquanto a pessoa está presa.
- **As variações:** um símbolo para cada uma em cima da barra do herói (a forma diz qual; a cor ajuda), o anel tracejado
  no chão e, na barra de cima, a etiqueta com o símbolo e o nome. Na escolha, as seis com a regra (passando o mouse); na
  pausa e no fim, as do sorteio com a regra inteira.
- **As explicações não interrompem:** a faixa de cima explica cada variação e cada golpe novo **uma vez por sessão**;
  depois, só os nomes. Nada pausa a luta.
- **As barras de cima:** até duas (os heróis de pé, na ordem em que entraram) ou só o General (mais largo, borda dupla):
  o nome, as variações, a vida com o dano recente escorrendo, a postura (não no Inabalável) e o golpe que ele prepara.
  A faixa de avisos desce para baixo da barra quando ela está no topo.
- **A linha da guerra,** no placar: "Ondas 3 de 8 · heróis inimigos caídos: 1 de 3", depois "Faltam N inimigos; depois,
  o General", "Campo vazio: o General atravessa o portão", "O General: derrube-o para vencer" (o texto vem pronto do
  motor, `campo9.estado9`).
- **As transições:** a faixa e a trompa quando cada herói entra e cai ("Vesna caiu (2 de 3)"), quando o campo fica vazio e
  quando o General entra; a queda dele para a luta por um instante; o fim mostra "Vitória: o General caiu" e o painel da
  guerra (o número, os heróis com as variações e quando caíram, o tempo do General, as ondas).

**Defeito herdado corrigido:** a parte vermelha da barra de cima não aparecia desde o Campo Livre 8 (só o trecho claro do
dano recente); agora aparece nas duas barras.

## 5. A chegada do General

"Campo vazio" quer dizer que os inimigos previstos foram derrotados: **nenhuma onda marcada para depois** (a condição
passou de "o tempo das ondas passou" para "a próxima onda passou do limite"), **os três heróis entraram e caíram** e
**ninguém do lado inimigo de pé**. Então, 3 s depois (2 s no treino), o General entra pelo portão. Ele é criado uma vez;
a vitória vem uma vez; caído antes, a derrota fica (o General cair depois não a troca); caído depois da vitória, a vitória
fica. Ninguém foge (`semFuga`): nem a tropa de Harg, nem Ardis sozinha. O General não invoca ninguém.

**O caso que travava a guerra (resolvido pela causa):** em 16 guerras sem tela, uma (o Mago, sorteio 5) não terminava em
400 s: um cão encurralou Odette no canto do campo; ela só fugia (e não saía do lugar), se curava, e o cão mordia, para
sempre. Odette agora, encurralada, fica e atira a luz. Depois disso, as 16 terminaram com o General vindo uma vez.
**O que ainda demora:** inimigos lentos perseguindo um arqueiro nosso que foge pelo mapa (até 60 s no pior sorteio). Não é
alguém preso: para não depender de achar alguém num canto, sem ondas por vir e sem heróis, **os últimos inimigos (até 8)
ganham seta na borda da tela** e a linha da guerra diz quantos faltam.

## 6. Verificação

- **Testes da simulação: 85** (77 de antes, revalidados, e 8 novos em `testes/campo9.test.mjs`): as variações aplicadas;
  as 15 combinações de duas variações em três sorteios, sem NaN e sem uma regra chamando a outra sem fim; o barril aceso,
  o caído e a borda do círculo; **o que acerta é o que o aviso mostrou**, golpe a golpe do General e estágio a estágio,
  com a tropa espalhada em volta; a chegada do General (uma vez, só com o campo vazio, sem fuga), inclusive no sorteio do
  cão; o sorteio que se repete; os golpes de Vesna e do General sem erro; a derrota em cada fase (ondas, herói, General) e
  a vitória que não vira derrota. Os 77 de antes passam sem alteração.
- **Sem tela, a guerra** (`ferramentas/guerra9.mjs`, 8 sorteios): Guerreiro forte 8/8, médio 0/8; Mago forte 7/8,
  médio 6/8. Os heróis caíram em 2,6 a 20 s na maioria (casos de 27 a 44 s com Implacável ou Rastro Explosivo, e dois
  que ficaram de pé quando o herói caiu); o General durou 55 a 89 s com o exército. O maior tempo seguido sob controle: 1 s.
- **No navegador** (`ferramentas/conferir9.mjs`, 1920 × 1080 e 1280 × 720, tudo certo, console sem erros): a escolha (a
  guerra escolhida, as opções do 8 ignoradas, as seis variações), a guerra com o Guerreiro e com o Mago, a barra com uma e
  com duas variações, a linha da guerra, o General uma vez, a vitória uma vez e o painel do fim, `R` e `T`, a pausa, a
  seleção, a ordem e o comando com o olhar parado, o Leque, os anéis do Terremoto (o primeiro e o segundo), a Cruz, o
  Salto no ar, as Correntes e a corrente, as cargas, o `/v8/`; 58 qps na guerra 1× (simulação 0,5 ms, desenho 1,2 ms).
  Capturas pontuais em `capturas/cl9-*.png`; sem vídeos.

## 7. A investigação do Mago

**O que foi relatado:** no treino, o Mago perdia todas para o General. **O que se mediu** (`ferramentas/general9.mjs`, a
cada golpe do General: a distância em que começou, se acertou e se havia saída a pé ou com a mobilidade, com 0,25 s de
reação):

1. **O robô (a maior parte).** O Mago luta a ~70 px dele; ali, o Terremoto tem saída a pé em 12 de 12 vezes, e o robô
   apanhava em 11: nos anéis, ele saía para o anel de fora e depois voltava justamente para o anel que ainda ia estourar.
   E parava de desviar na execução do golpe (os últimos 0,07 s da Estocada). Corrigido o robô (é a ferramenta de medição,
   não o jogo), o Terremoto passou a acertar o Mago em 4 de 15 e o Mago forte passou a vencer o treino em 3 de 6.
2. **Golpes sem saída (o jogo).** Independente do robô, com você parado e mirado: a **Estocada** estourava em 0,37 s
   (com 0,25 s de reação sobram ~8 px de passo; a faixa pede 10) e o **Salto** seguia você até 0,35 s e caía em 0,98 s
   (a pé, ~43 px; o círculo tinha 60). Ninguém tinha resposta a pé; agora têm (a seção 3). **O Terremoto colado nele**
   (dentro dos 58 px do meio) continua sem saída a pé: a resposta é a mobilidade (a Investida tem invulnerabilidade; o
   Piscar leva 95 px), que recarrega em 4–5 s, contra 9 s do Terremoto. Ficou de propósito; é a questão 9.2.
3. **A montagem não decide:** "Gelo que estilhaça" e "Fogo em cadeia" deram o mesmo 3 de 6 no treino.
4. **O alcance:** o General anda a 70 longe de você e o Mago a 68: não dá para manter distância andando; o Salto (110 a
   300 px) fecha a distância. O Mago luta perto dele por necessidade, e é onde as áreas pegam.
5. **A leitura, a câmera e a escala:** o General tem 25 × 22 px (75 px na tela de 1920); os avisos ficam em volta de você
   e a borda que importa para a saída está sempre à vista. O anel de fora do Terremoto (185 px) e os braços da Cruz (300
   px) passam da tela, mas a parte deles perto de você aparece. O Salto pode vir de fora da tela: o círculo cai em você e
   a seta vermelha na borda mostra de onde ele vem.

**A tabela de saídas** (`node ferramentas/general9.mjs tabela 0.25`; você parado, mirado; "a pé": há saída andando; "mob":
só com a mobilidade):

| Quem | Golpe | Estoura | Colado (Guerreiro/Mago) | Onde ele começa o golpe |
|---|---|---|---|---|
| General | Ceifa | 0,48 s | a pé / a pé | a pé (52 px) |
| General | Estocada | 0,47 s | a pé / a pé | a pé (140 px) |
| General | Correntes | 0,44 s | a pé / a pé | a pé (200 px; com 0,3 s de reação, o Mago só com a mobilidade) |
| General | Terremoto | 0,55 / 0,85 / 1,15 s | **mob / mob** | a pé (110 px) |
| General | Salto | 1,15 s | a pé / a pé | a pé |
| General | Cruz de Lâminas | 0,55 / 0,90 s | a pé / a pé | a pé (160 px) |
| Vesna | Corte Duplo, Leque, Bote | 0,36 a 0,50 s | a pé | a pé |
| Harg | Rodopio | 0,70 s | **mob** | a pé (46 px) |

**Com o robô depois das correções** (treino, 6 sorteios): Guerreiro forte 5/6, médio 0/6; Mago forte 3/6, médio 0/6. O
General continua muito forte: o médio perde por recuar em linha reta (a Ceifa e a Estocada castigam) e por não guardar a
mobilidade para o Terremoto. **Números de robô são indícios, não aprovação de dificuldade nem de diversão.**

## 8. O que mudou fora da guerra

- `campo8.js` (a máquina de Harg): o contato usa o aviso; o corpo avança exatamente o que o aviso mostrou. Afeta também os
  encontros do 8 que continuam na tela nova (o treino e a guerra de Harg); os testes do 8 passam como estavam.
- `campo6.js` (Odette): encurralada, revida. Afeta todos os encontros com Odette; os testes do 6 e do 7 passam.
- `robo.js`: a esquiva continua na execução; a dos anéis; a mobilidade no Terremoto colado. Muda as medições, não o jogo.

## 9. Limitações, números provisórios e questões para o Jean

**Provisório:** todos os números das seções 2 e 3; as figuras das tropas novas, de Vesna e do General (para identificar,
não arte final; o redesenho, se a guerra for aprovada, segue a `arte-personagens-fenda`); os símbolos das variações.
**Limitações:** o robô anda em linha reta (sem rota) e às vezes encosta na muralha atrás de um inimigo; o cálculo de saída
ignora paredes e corpos; o Salto não tem altura desenhada (ele desliza do ponto de partida ao círculo em 0,45 s).

**Para avaliar jogando:**

1. Os heróis comuns ficaram rápidos e perigosos o bastante, ou ainda viram duelo (Ardis com Rastro Explosivo durou 44 s
   num sorteio)?
2. **O Terremoto colado** deve continuar exigindo a mobilidade (castiga quem abraça o General) ou o círculo do meio deve
   diminuir para ter saída a pé (com 40 px, sairia a pé de quase todo lugar)?
3. A Estocada a 0,40 s e o Salto mais lento ainda passam a sensação de "rápido"? Algum golpe ficou previsível demais?
4. As variações se leem no meio da guerra (o símbolo em cima da cabeça, a etiqueta na barra)? Alguma combinação ficou
   injusta ou sem graça (Inabalável com Implacável, Vampírico com Venenoso)?
5. O barril caído ferindo os dois lados aparece a tempo de ser usado de propósito?
6. A espera pelo General (o "Faltam N inimigos" e as setas) incomoda? Preferiria que os últimos viessem até você?
7. O ritmo da guerra inteira (cerca de 2,5 minutos até o General e 1 minuto com ele) está bom?
