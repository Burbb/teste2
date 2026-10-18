# O conjunto da HUD principal na direção da ficha (em avaliação, nada no jogo)

**Pedido de Jean (18/10/2026):** a ficha com a pintura foi aprovada como base visual. Estender a direção ao centro, ao
painel do mundo e à barra de cima, para avaliar o conjunto. As referências:
- **Material:** a ficha aprovada (`../ficha/`).
- **Composição, hierarquia e contornos incompletos:** a imagem conceitual (`../referencia.png`).

As rodadas anteriores ficam como estavam: `../direcao.css`, `../ficha/` com a arte gerada e com a pintura.

## Como entra

**A ficha aprovada não muda.** São `../ficha/ficha.css` e `pintura.css` com os scripts deles, mais esta camada:
- **`conjunto.css`:** o topo, o centro, o mundo, as cartas, a mira, a doca, o seletor e as dicas.
- **`conjunto.js`:** só põe a pintura espelhada atrás do mundo, como peça à parte (sem clique, `aria-hidden`).
- **`../direcao.js`:** a marcação da dica "Testes do d20" (nomes em marfim, totais em latão e só as duas regras do d20
  em destaque).

**`derivar_pecas.py`** prepara as peças a partir da pintura aprovada (`../Painel vertical em tinta escura.png`), sem
esticar nem alargar pincelada nenhuma:
- **`pecas/pintura-espelhada.png`:** a pintura inteira, espelhada na horizontal. Decora a coluna do mundo, na periferia
  direita, com o desgaste do lado de fora como a ficha à esquerda: escala 0,5 exata, transbordando a caixa.
- **`pecas/carvao.png`:** um ladrilho do miolo da pintura (a tinta preta com as passadas diagonais), reduzido a 0,5
  como a ficha e emendado por espelho (2×2) para repetir sem costura. É a superfície calma do topo, do centro, da
  leitura, da doca, do seletor, da mira e das dicas.
- **`pecas/borda-mascara.png`:** o alfa da pintura reduzido a 0,25. É a máscara de nove partes do mapa, que ganha o
  rasgo da própria pintura.

**`fotografar.mjs [jogo|conjunto]`** faz jogo × conjunto nas cenas das rodadas anteriores, a 1920×945:
- **Exploração:** a Capela Afogada de dia, com a dica dos testes, o mouse num caminho e numa escolha.
- **Luta:** o paladino com Morel contra 3 lobos, com a tela inteira, o seletor aberto, a mira e o golpe.

## As decisões

**A distribuição da pintura:**
- **Periferia:** o desgaste expressivo fica nas colunas da esquerda (a ficha) e da direita (o mundo). As duas
  transbordam a caixa, e o cinza quente do fundo aparece nas bordas de fora da tela.
- **Centro:** sem moldura pintada. A coluna do centro cobre as sobras das duas pinturas, e as emendas com ela ficam
  retas e escuras: as divisões internas, quietas. Não há três molduras igualmente chamativas.

**As peças:**
- **Topo:** sem a faixa de ferro e a sombra pontilhada; o carvão; o logotipo e as informações em marfim.
- **Centro:**
  - o carvão liso;
  - o cenário como está e como protagonista, só com um fio fino embaixo;
  - a leitura (a página, o registro) no mesmo carvão, com um véu que acalma o grão;
  - o retrato do topo com o contorno aberto e o nível em latão;
  - as barras com a aresta fina da ficha (sem a moldura de ferro).
  - **Os recursos:** os números em marfim e as divisões quase sumindo.
- **Mundo:**
  - o nome do lugar em serifa marfim (36 px), como o do herói;
  - os títulos de seção em versal espaçada, com o fio que se apaga (os da ficha);
  - o mapa com o rasgo da pintura;
  - a missão e os contratos sem caixa, com o contorno aberto (a missão com o fio de latão: é atenção);
  - os caminhos com face de carvão, o contorno aberto e a seta ›.
- **Cartas:**
  - fundo de carvão, sem aresta, com o contorno aberto;
  - o lado de cada um pela marca à esquerda (latão você, verde-água a comitiva, ferrugem o inimigo);
  - a vez com a barra de latão em cima, pulsando como hoje;
  - a sua carta na vez com os cantos em latão;
  - o chefe e a proteção com o anel de sempre.
- **Mira:**
  - o tracejado de quem pode ser alvo e o contorno cheio do alvo escolhido, agora em marfim (e a seta ▼ do jogo);
  - a janelinha "escolha o alvo" no carvão, com o contorno aberto e o nome da ação em marfim.
- **Seletor:**
  - as faixas aprovadas não mudam: a seleção marfim continua o destaque mais forte da tela;
  - o painel ganha a superfície da leitura;
  - o título fica grande e espaçado ("H A B I L I D A D E S"), a hierarquia da referência.
- **Doca:** o carvão, as divisões quase sumindo e a tela aberta em marfim, com o traço embaixo.
- **Dicas:** o carvão com uma aresta fina.

**O contorno aberto** (dois cantos marcados e traços que se apagam antes do meio) organiza retratos, cartas, missão,
caminhos e a mira. Nunca é a única marca de um estado.

**Os estados funcionais continuam com as marcas de produção, só no material novo:**
- **Conferidos nas capturas:** os recursos, a vez (barra), o alvo (tracejado e contorno cheio) e a seleção (a faixa
  de marfim).
- **Não aparecem nestas cenas (sem ferida, nada indisponível):**
  - a vida bloqueada e o indisponível das faixas. O estudo só troca a aresta de fora das barras; o que fica dentro
    delas (o preenchimento e a parte bloqueada) e as regras do indisponível não foram tocados;
  - o foco do teclado é o anel de sempre (o estudo não mexe nele).

**Um ajuste local na ficha.** A composição aprovada não muda. Na luta (o aviso de talento, a comitiva com a aprovação),
a coluna passava 51 px da altura e rolava, porque os espaços de item cresciam com a coluna mais larga. Eles ficam em
48 px (os de produção têm ~46) e os vãos ficam alguns pixels menores.

## Conferido (`capturas/relatorio-jogo-conjunto.json`)

**Medidas e erros:**
- o centro e a arena seguem com 1088 px, como no jogo;
- a página, a ficha e o mundo não rolam, na exploração e na luta;
- nenhum erro na página.

**As interações:**
- o mouse num caminho acende o lugar no mapa;
- a dica dos testes abre;
- o seletor abre e Esc volta;
- a mira marca o alvo, o golpe sai e a luta segue para o turno 2.

**Comparações** (`comparacoes/`, tamanho real):
- `jogo-1-exploracao.png` × `conjunto-1-exploracao.png`;
- `jogo-5-seletor.png` × `conjunto-5-seletor.png`;
- `conjunto-4-luta.png`;
- `conjunto-6-mira.png`.

**O que não rodei:** vídeo e a suíte, o gabarito e a fumaça. Nenhum arquivo do jogo mudou.

## As limitações e a peça que falta

**Uma peça complementar para o topo.** A pintura é vertical, e não há como tirar dela uma faixa horizontal longa sem
repetir o mesmo trecho cinco vezes nem alargar as pinceladas. Por isso o topo ficou no carvão liso, com a borda de
baixo reta, e o desgaste das colunas some por baixo dele. Para o topo ter a borda pintada da referência, faltaria uma
pintura horizontal no mesmo material: uma faixa larga, de ~1920×120 px na escala de uso (o dobro no arquivo), com o
rasgo e os respingos na borda de baixo e nos cantos e o miolo limpo.

**A altura da janela.** As duas pinturas têm altura fixa (987 px na escala de uso). Numa janela mais alta, a coluna
passaria do fim delas; adaptar fica para a integração.

**A largura.** A mesa continua com a margem de hoje (o centro não muda). As pinturas ficam junto das colunas, não na
beira da tela.

**Ficaram como estão:** o anúncio e a placa dos turnos, a rolagem no centro e as faixas das escolhas e dos comandos
(já aprovados), além das telas fora da HUD principal.
