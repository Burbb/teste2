# O livro narrativo da capela (etapa 2, 24/10/2026)

**Agora: três propostas no protótipo (A, B e C), aguardando a escolha do Jean.** Nada integrado; o livro de hoje
continua no jogo. As propostas estão na seção "As três propostas", abaixo; o levantamento que as originou vem depois.

## As três propostas

**A direção (Jean):** sentir que se lê algo escrito por uma pessoa daquele mundo; o texto começa como registro e
termina numa confissão de culpa, e a apresentação sustenta essa mudança. O objeto é o livro simples de couro castanho
da sacristia. Textos, pistas, requisitos e releitura iguais aos do jogo.

**O que está estabelecido e foi respeitado:** o autor é "o padre que escreveu o livro da sacristia" (a pista `ilse`),
sem nome; o código diz "duas entradas, anos entre elas"; o documento da região (11) põe o Sigilo há cerca de 58 anos
e o afogamento há cerca de 55. Nada disso aparece como data, nome ou assinatura na página: nenhuma das três inventa
autor, data ou fato.

**A referência (o trabalho da Lettermatic para Pentiment):** dela veio a ideia, não a aparência. A letra faz o papel
da voz de quem escreve; para texto longo, uma escrita humanista legível; e a "habilidade da mão" varia com contenção
(a mesma letra mais ou menos controlada), em vez de letras tortas ao acaso. Nada da interface deles.

**A letra:** Fondamento (Astigmatic, SIL OFL 1.1; `fontes/OFL-Fondamento.txt`), da Fontsource 5.3.0
(`@fontsource/fondamento`, pelo jsDelivr; os arquivos `latin-400-normal` e `latin-400-italic`). Uma escrita humanista
de pena larga, legível a 21–24 px, com os acentos e a pontuação do português; a itálica é a mesma mão mais depressa.
Escolhida num espécime com o texto real, ao lado de Felipa, Bilbo, IM Fell English, Cormorant Garamond, Marck Script,
Mynerve, Sedgwick Ave, Cedarville Cursive e a Alegreya itálica: as cursivas eram difíceis de ler, as de imprensa não
pareciam escritas à mão.

**O livro:** `desenhar_livro.py` desenha o registro aberto visto de cima pelo método das cenas (cada parte em `px`
deliberados; o grão do papel num ladrilho escrito à mão): o couro da cena (#5a3422, a luz #7a4c30), os cantos gastos,
as folhas de baixo saindo pela beira, a dobra escurecendo em três passos sem faixa, o vão em V do couro na dobra e a
marca de umidade nos cantos de baixo (a capela alagada). Escala 3, igual nas duas janelas. O texto é HTML por cima,
nunca imagem (`livro.js`, `livro.css`, só as classes `lv-*`; nada do Grimório).

| | A · registro | B · registro que vira confissão | C · leitura próxima |
|---|---|---|---|
| o livro | as duas páginas, pautadas, 870×510 | as duas páginas, lisas, 870×402 | uma página e a faixa da anterior, 642×468 |
| a 1ª entrada | Fondamento, a tinta castanha, nas linhas | Fondamento, arrumada, com espaço | como a B, a 24 px |
| a 2ª entrada | outra tinta (quase preta), depois de um traço de pena, uma linha abaixo, com recuo próprio | a mesma mão mais depressa (a itálica), mais apertada, a linha oscilando meio pixel por palavra (uma sequência fixa) | como a B, e mais folhas viradas à esquerda |
| ler | as duas de uma vez | as duas de uma vez | uma por vez: Anterior e Próxima, "Entrada 1 de 2" |
| fechar | Fechar, Esc, Enter, espaço, o véu (como hoje) | o mesmo | Fechar e Esc; o véu não fecha (um clique que erra a navegação não fecha o livro) |

Comum às três: "O livro da capela" é a etiqueta da interface, em cima, fora da página; o Fechar é o botão da HUD,
embaixo, longe da escrita; o clique fora dos botões não tira o foco do livro; as teclas do menu não escolhem nada
embaixo; com o movimento reduzido, nada anima. Na C, as setas e PageUp/PageDown mudam de entrada; o foco começa no
Próxima, passa ao Fechar na última entrada e volta ao Próxima na primeira; o Tab circula só nos botões ligados.

**Conferido** (`auxiliares/fotografar.mjs`, `auxiliares/gestos.mjs`, no jogo real, cenário `capela`): as três e o
livro de hoje a 1920×945 e a 1280×720, o livro inteiro na janela e o texto cabendo nas páginas, sem erro na página;
a primeira leitura grava as mesmas pistas que o livro de hoje e mostra o mesmo cartão; reler não muda nada; os gestos
acima, um por um. A folha: `folha-propostas.png` (as três em tamanho real a 1920; as telas de 1280 a um terço).

**A avaliação (recomendação: C, com a mão da B):**

- **A:** o ganho é o documento: a pauta e a margem fazem dele um livro de registro, e a ordem combina com a primeira
  entrada. A limitação: a mudança para a confissão quase não se sente (a mesma letra, só outra tinta), e o traço de
  pena sozinho não diz "anos depois"; a página da esquerda fica com metade das linhas vazias.
- **B:** o ganho é a voz: a mesma mão mais apressada e apertada se percebe de relance como outro momento, mais
  pessoal, e o livro fica do tamanho do texto. A limitação: a itálica a 21 px é a leitura mais densa das três, e nada
  diz quanto tempo passou.
- **C:** o ganho é a leitura e a passagem do tempo: a letra maior (24 px), uma entrada por vez com a página inteira
  para ela, a mudança de mão da B e as folhas viradas à esquerda; a segunda entrada fica a um clique ou uma seta, e
  "Entrada 2 de 2" diz que há mais. A limitação: perde-se a comparação lado a lado das duas mãos, e é um passo a mais
  (quem fecha na primeira entrada não lê a segunda; o Próxima já vem com o foco).

**A cronologia só pela apresentação não fica clara em nenhuma das três** (a C chega mais perto, pelas folhas
viradas). Proposta à parte, para avaliação, sem implementar: uma nota curta da interface antes da segunda entrada,
**"Algumas páginas adiante:"**, a frase que o modo texto do jogo já usa entre as entradas (`_ler_livro`). Fica fora
da escrita do padre (na letra da interface), não inventa data e diz o que o objeto mostra.

**Ajuste editorial:** nenhum outro necessário para esta apresentação; os textos ficaram como estão.

**Demonstração:** `demo.bat` ou `python ferramentas/prototipos/hud/livro-capela/auxiliares/demo.py`, painel em
http://127.0.0.1:8767/: o livro de hoje, A, B e C, na primeira leitura e na releitura, cada caso numa partida de
teste com saves temporários (os seus saves não são tocados).

**Os arquivos:** `desenhar_livro.py` (o livro), `propostas/` (os PNGs e `areas.json`, onde fica o texto), `livro.js`
e `livro.css` (a apresentação), `fontes/` (a Fondamento e a licença), `auxiliares/` (`cenarios_livro.py`, o servidor
que põe o protótipo só na página da demonstração; `demo.py`; `fotografar.mjs`; `gestos.mjs`; `folha.py`),
`capturas/` (as fotos e `medidas.json`).

**Achados à parte (continuam fora desta avaliação):** o atalho da missão que aponta para o livro e a linha repetida
no Histórico (problemas 6 e 7 do levantamento).

# O levantamento (24/10/2026)

**Só o levantamento.** Nada redesenhado, implementado nem mudado no jogo; textos narrativos e regras intocados. Base: a
1.203.0. Visto no jogo pelo cenário `capela` (`ETAPA=ossuario LIVRO=0 SALA=sacristia`: a sacristia vencida, o livro
ainda por ler), a 1920×945 e a 1280×720. A folha: `folha-atual.png`.

O critério do plano (23, etapa 2): "apresentação imersiva do relato. É outro objeto/contexto que o grimório equipado. A
revisão visual não autoriza reescrever a história agora."

## Como funciona hoje

**Onde e quando.** Na sacristia da Capela Afogada, depois de vencer os dois homens marcados. A vitória mostra o achado
("um livro embrulhado num couro duro", no buraco da parede) e dá só a pista `marcados`; o conteúdo não aparece ali. Ler
é uma ação de missão (`acao` `livro` em `rpg/missoes.py`, "Ler o livro da capela", `onde="sacristia"`), oferecida nas
etapas `ossuario`, `fundo` e `retorno`, pelo menu ou pelo ponto "Livro" da cena. Como a etapa fica em `retorno` depois
da conclusão, continua relendo-se na sacristia depois do fim da missão. Nada obriga a ler: dá para descer ao ossuário
sem abrir o livro.

**Conteúdo.** `LIVRO_DA_CAPELA`: o título "O livro da capela" e duas entradas do padre, anos entre elas (a chegada de
Ilse com o Sigilo do Turvo; a acusação, a inocência dela e o afogamento). Sem nome do padre, sem datas.

**Abrir, navegar, fechar.** `_ler_livro` narra a abertura ("Você tira o couro do livro..." / "Você abre de novo o
livro..."), grava as pistas, redesenha a sala com o livro sem o couro e manda a celebração `livro`. A tela
(`telas/cenas.js`, `abrirLeitura`) abre um modal (`#sobre-leitura`) por cima da sala: as duas entradas lado a lado, a
primeira na página da esquerda com o título, a segunda na da direita, em itálico e numa tinta um pouco mais clara. Não
há navegação: as duas cabem de uma vez. Fecha pelo botão "Fechar Esc", por Esc, Enter, espaço ou clique no véu; o foco
fica no Fechar e o Tab não sai dele; as teclas do menu não escolhem nada embaixo. Fechar devolve o texto, que segue para
o Continuar. No modo texto, as entradas viram parágrafos entre aspas, com "Algumas páginas adiante:" entre elas.

**Pistas e progresso.** A primeira leitura grava `ilse` e `sigilo_do_turvo` (uma vez) e mostra o cartão "Diário
atualizado" com os dois títulos; reler não muda nada. A pista `ilse` é a que o resto da missão usa: o nome que os textos
dão à guardiã (`nome_da_guardia`: "Ilse" ou "a Bruxa Afogada"), a pergunta do Diário que leva à Vó Berta e o primeiro
requisito do descanso ("Chamá-la pelo nome, sabendo o que fizeram com ela"). Quem não lê segue com a pergunta "O que diz
o livro que os homens marcados procuravam na sacristia?" no Diário. O Histórico (H) anota "▸ Leu o livro da capela"
(a cada abertura, porque vem da celebração).

**Apresentação.** O livro é a casca do Grimório antigo: as classes `grimorio-livro` e `grimorio-pagina`, mais
`leitura-livro` (`css/06-talentos-avisos.css`). Capa em cor chapada (#3a1f12) com o filete dourado do Grimório, papel em
degradê de CSS, a sombra da dobra em degradê, o título na fonte de título em vinho, o texto em Alegreya 18 px. A
caixa tem 860×360 nas duas janelas (as páginas com 412×326, sem rolagem). O "Fechar Esc" é o botão do Grimório,
encaixado por fora do canto de cima. Abre com o `livro-abre` (escala e esmaecimento; sem animação com o movimento
reduzido). Sem som próprio. Na cena, o livro do buraco é desenhado em pixel art (`cenas.js`): couro castanho embrulhado,
depois a capa castanho-escura (#5a3422) com o corte das folhas e o couro pendendo; sem ferragens nem dourado.

## Problemas observados

1. **A casca do livro não é a linguagem aprovada.** É o único modal narrativo ainda no acabamento do Grimório antigo
   (degradês e bordas de CSS, o filete dourado), ao lado da HUD de ferro, das celebrações e do d20 em pixel art.
2. **Não é o mesmo objeto da cena.** Na sacristia ele é um registro de capela simples, em couro castanho e sem ornamento;
   aberto, ganha a moldura e o dourado do Grimório. O plano pede outro objeto que o grimório; hoje é o mesmo.
3. **Metade das páginas fica vazia.** A altura mínima (360) é maior que o texto: em 1920 e em 1280, cerca de 40% de
   cada página fica em branco, e o livro parece incompleto em vez de "duas entradas num registro".
4. **O salto de anos não se vê.** No modo texto, "Algumas páginas adiante:" separa as entradas; na tela, só o itálico e
   a tinta mais clara. Quem lê não percebe que a segunda entrada é de anos depois (só o conteúdo dá a pista).
5. **O Fechar fica por fora da moldura**, pendurado no canto (herança do Grimório); a 1280 ele encosta no painel da
   direita.
6. **O atalho da missão aponta para o livro.** O painel da missão (o rastreador) transforma em atalho a primeira opção
   de missão do menu, e "Ler o livro da capela" vem antes de "Descer ao ossuário". Com o objetivo "Descer ao ossuário",
   o atalho diz "Ler o livro da capela ▸", antes e **depois** de ler (`app/escolhas.js`, `opcaoMissao`). Não é visual
   do livro, mas confunde o progresso; é uma correção à parte, pequena (por exemplo, a releitura não virar atalho).
7. **O Histórico repete "Leu o livro da capela"** a cada releitura (a celebração é a mesma). Pequeno; anotar junto do 6.

## Sugestões (não são problemas; pedem a decisão do Jean)

- **Reler fora da capela:** hoje só na sacristia. Uma cópia das entradas no Diário, depois da primeira leitura, deixaria
  o jogador reler a fonte do nome de Ilse sem voltar à capela. Muda o que o Diário mostra: fica fora deste escopo.
- **Um som de página** ao abrir (o jogo não tem; o Grimório também não).
- **O modo texto e a tela gráfica com o mesmo separador** entre as entradas, quando o separador visual existir (sem
  texto novo na tela gráfica: um ornamento e o espaço dizem "algumas páginas adiante").

## O escopo proposto (o próximo lote)

Só a apresentação do livro aberto da sacristia, com os mesmos dados do motor (`titulo`, `paginas`) e a mesma interação:

1. **O livro como objeto em pixel art:** o registro aberto, de couro castanho como o da cena (sem filete dourado nem
   pedra), com a lombada, os dois blocos de folhas (o da esquerda mais fino: é o começo do registro; o da direita mais
   grosso), as camadas das folhas nas beiras e a dobra escurecendo de cada lado, pela skill `arte-livros-fenda` (o
   aberto, validado no Diário da doca). A moldura sai de PNGs (cantos e beiras repetidas), não de degradês.
2. **O papel e a escrita:** o pergaminho com o grão em pixel, plano (sem degradê), as duas tintas (a da chegada e a de
   anos depois) e, entre as duas entradas, a marca do salto de tempo: algumas folhas viradas na página da direita e um
   ornamento curto de pena, sem frase nova.
3. **O tamanho pelo texto:** a caixa do tamanho do conteúdo, nas duas janelas, sem metade vazia; a 1280×720 inteira, sem
   rolagem.
4. **O Fechar dentro da moldura**, no padrão dos botões da HUD (como o Continuar do quadro dos baús), com as mesmas
   teclas.
5. **Separar das classes do Grimório:** o livro da capela ganha CSS próprio; a tela do Grimório (etapa 8) não muda.
6. **Abrir:** o livro aparece fechado e abre em poucos quadros (com o movimento reduzido, já aberto).

**Fora:** os textos (do livro, do narrador e das pistas), as regras, quando e onde se lê, a ordem do menu, o Diário, o
Grimório. Os itens 6 e 7 dos problemas vão para uma correção separada, se o Jean quiser.

## A direção visual

Um **registro paroquial gasto**, não um tomo mágico: couro castanho-escuro liso, a lombada costurada, cantos de couro
mais escuro em vez de cantoneiras, o papel amarelado com manchas de umidade nas beiras (a capela está alagada) e a
escrita em tinta ferrogálica (castanho-escuro, a segunda entrada mais desbotada). A moldura em volta é a da HUD de
ferro (a mesma do quadro dos baús abertos), e o livro fica dentro dela como um objeto, não como a janela inteira. O
título na fonte de título, em tinta, sem o vinho do Grimório; o texto em Alegreya, como hoje. Nada de brilho mágico:
o livro só conta o que o padre escreveu.

**Proposta como sempre:** duas variantes (por exemplo, o livro sobre a moldura de ferro com o carvão em volta, ou o
livro sozinho sobre o véu escuro), as fotos a 1920×945 e a 1280×720 com os mesmos dados, e o Jean escolhe.
