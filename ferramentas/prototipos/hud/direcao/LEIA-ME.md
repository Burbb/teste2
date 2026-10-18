# A nova direção visual da HUD principal (estudo não escolhido; nada no jogo)

**Decisão de Jean (18/10/2026), depois de jogar produção × protótipo (`comparar/`): fica a HUD de produção.** Esta pasta
inteira (a proposta abaixo, `ficha/`, `conjunto/`, `topo/`, `comparar/` e as pinturas `Painel vertical em tinta
escura.png` e `topo.png`) fica guardada como estudo não escolhido para a HUD principal.
- **Para outras telas:** pode servir de referência, mas nenhum reaproveitamento está aprovado automaticamente.
- **A ficha:** a aprovação dela valia só como base do estudo. Nada daqui (tipografia, espaçamentos, cores, peças) passa
  para a produção sem um pedido próprio.
- **A dica "Testes do d20":** o refinamento de cores (`direcao.js` e o fim de `conjunto/conjunto.css`) ficou só aqui,
  como pendência independente.

**Pedido de Jean (17/10/2026):** estudar, só no protótipo, a nova direção visual da HUD principal (o topo, a ficha, as
cartas da luta, a coluna do mundo e a relação com os comandos e o seletor em faixas já aprovados). A referência
principal é uma imagem de Jean: carvão e tinta, tipografia com presença, destaques em marfim, borda externa gasta e
contornos retangulares que se desfazem antes de fechar. Clair Obscur entra pela expressividade e pela hierarquia.
Uma proposta só. O jogo e a versão continuam como estão.

**Ferramenta:** CSS direto, nas folhas do jogo. O relatório do pen.dev (`../pen-composicao/LEIA-ME.md`) mostrou que o
ajuste direto no CSS chegou ao mesmo resultado mais depressa. Não houve arte nova: a borda gasta é uma máscara SVG
gerada no próprio CSS (ruído deslocando um retângulo), sem Aseprite.

## Os arquivos

- **`direcao.css`:** a camada do estudo, por cima das folhas 01 a 20. O prefixo `:root:root body` vence o `:root body`
  das camadas atuais sem depender da ordem.
- **`direcao.js`:** só a marcação da dica "Testes do d20" (o total à parte e as duas regras do d20 em destaque). Os
  números e textos são os do motor.
- **`fotografar.mjs`:** atual × proposta com os mesmos dados, a 1920×945 (a área do jogo numa janela maximizada no
  monitor 1920×1080).
  - Exploração: a Capela Afogada de dia, com o arqueiro patrulheiro de nível 5, e a dica dos testes aberta.
  - Luta: o paladino de nível 8 com Morel contra 3 lobos (semente 7), no começo da vez, com o seletor de Habilidades
    aberto e na mira.
- **`abrir.mjs [exploracao|luta] [producao]`:** para jogar com o estudo, ou sem ele, para comparar.

## As decisões: pesos diferentes para cada papel

| papel | antes | no estudo |
|---|---|---|
| superfície | três molduras de aço com filete de latão e rebites; a faixa de ferro no topo | carvão com grão, sem moldura de ferro; a borda externa de cada coluna e a de baixo do topo gastas (máscara de pincel); uma queimadura quente por dentro da borda; o fundo atrás das colunas quente (papel queimado), visível nas emendas e nas falhas da borda |
| organização | caixas fechadas (cartas, rastros, caminhos, retratos) | contorno aberto: dois cantos marcados (em cima à esquerda, embaixo à direita) e os traços deles se apagando antes do meio; os outros dois cantos ficam abertos. O mesmo nas colunas, nos retratos, nas cartas, nos rastros do mundo e nos caminhos |
| leitura | a página e o registro | continuam lisos, sem contorno nem pincel, no mesmo carvão das colunas |
| informação | nomes em letra gótica de pixel (dourado no lugar) | o nome do herói e o do lugar em serifa marfim (Alegreya 600, 32 px); títulos de seção em versal mais espaçada, marfim, com um fio que se apaga; números em marfim |
| seleção | a faixa de marfim dos comandos e do seletor (aprovada) | igual. É o único marfim cheio da tela, e por isso continua o mais forte |
| atenção | latão em vários pontos | latão só em detalhe: a vez (a barra em cima da carta), a sua carta na vez, o nível, o aviso de talento, a missão |

**Peças:**
- **Cartas:**
  - fundo de carvão sem aresta;
  - a marca do lado à esquerda, como antes (latão você, verde-água a comitiva, ferrugem o inimigo);
  - o contorno aberto;
  - na sua vez, os cantos em latão;
  - nas que podem ser alvo, o tracejado e o contorno cheio do jogo (forma além da cor, sem mudança).
- **Mundo:**
  - o mapa com a borda rasgada, como um pedaço de carta;
  - os caminhos com face de carvão, o contorno aberto e a seta › de quem leva a outro lugar.
- **Topo e doca:** o carvão das colunas; na doca, a tela aberta marcada em marfim, com o traço embaixo.
- **Seletor:** as faixas aprovadas não mudam. O painel ganha a mesma superfície da página, para não virar caixa, e o
  título fica em versal espaçada de marfim, com mais presença e ainda abaixo da faixa escolhida.
- **Dicas:** o carvão e uma aresta fina.
- **"Testes do d20":**
  - nomes em marfim e totais em latão;
  - parcelas mais claras;
  - penalidades em vermelho queimado;
  - no rodapé, só "20 sempre passa" e "1 sempre falha" em destaque, e o resto em cinza.

## Os compromissos

- **A borda gasta é contida.** O deslocamento é de ~5 px nas colunas e no topo, menos que na referência. Mais que
  isso começa a comer o retrato, os títulos e o mapa nas bordas.
- **O contorno nunca é a única marca de um estado.** A vez, o alvo, a seleção e o indisponível continuam com as marcas
  de antes (barra, tracejado, contorno cheio, faixa de marfim, cadeado). O foco do teclado é o anel de sempre, por
  fora, que o estudo não toca.
- **Nada mudou de lugar.** A largura das colunas, a mesa (com as margens nos lados, a 1920 px), a arena e a altura do
  registro são as mesmas. A borda transparente das molduras continua lá, agora pintada de carvão, e o conteúdo não se
  mexe.
- **Ficaram como estão:** os cenários, os retratos, os itens, os ícones e o dado. O menu inicial, o Inventário, o
  Grimório aberto, a criação e as celebrações têm etapas próprias.
- **Para a consolidação da HUD:**
  - o aproveitamento da largura a 1920 (a mesa para em 1740 px);
  - a borda de baixo da arena (hoje reta; gasta, ela disputaria com a placa do turno);
  - a janelinha da mira ("escolha o alvo") e as outras janelas pequenas da luta, ainda no acabamento atual.

## Conferido

- Atual × proposta com os mesmos dados (`capturas/representativas/`):
  - `atual-2-dica-testes.png` e `proposta-2-dica-testes.png`: a exploração, com a dica dos testes aberta;
  - `atual-4-seletor.png` e `proposta-4-seletor.png`: a luta, com o seletor de Habilidades aberto;
  - `proposta-5-mira.png`: a mira, com a ficha do lobo e os alvos.
- **Funcionamento** (`capturas/relatorio-*.json`):
  - nenhum erro na página;
  - a dica abre;
  - o seletor abre e Esc volta;
  - a mira marca o alvo, o golpe sai e a luta segue para o turno 2;
  - o Tab leva o foco ao primeiro controle, com o anel de sempre.
- Sem vídeo. Nenhum arquivo do jogo mudou: a suíte, o gabarito e a fumaça valem para o código de produção, que é o
  mesmo da 1.118.0.
