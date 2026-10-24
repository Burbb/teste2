# O livro narrativo da capela: o levantamento (etapa 2, 24/10/2026)

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
