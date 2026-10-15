# As soluções de cada objeto aprovado

O que funcionou no escudo e no unguento, para consulta. São decisões daqueles objetos, tomadas olhando o jogo; servem
de exemplo de raciocínio, não de receita. Outro objeto pede a própria forma, as próprias rampas e as próprias medidas.

## O escudo (ferro azulado, aro e peça central de latão)

`ferramentas/arte/desenhar_escudo_pixel.py`; 32, 40, 48 e 64 px. Aprovado e encerrado: não redesenhar.

- **Ponto de partida:** o escudo pintado da família (redondo, gomos de ferro, aro e bossa de latão, oito cravos) como
  referência de presença e contraste no pequeno; um render de relevo (`ferramentas/prototipos/hud/desenhar_escudo.py`)
  como referência de construção. Reduzir o render perdia para o atual em 32; o desenho na grade ganhou.
- **Silhueta:** dois discos em centro de pixel, a frente e a lateral deslocada pela diagonal (1 px no total: 1 em x e
  1 em y engordava o canto de baixo à direita).
- **Aro como rolo:** o tom pelo ângulo até a luz, a fileira de fora e a de dentro um degrau abaixo do lado em que
  viram, o brilho num arco curto só onde a luz bate de frente (um anel claro na volta toda ficava chapado).
- **Face em gomos:** cada gomo num tom só, pela direção dele (a `escada` de cada tamanho); a emenda como linha de pixel
  só em 48 e 64; o reflexo do gomo da luz como mancha de três tons, desenhado depois das sombras (antes, elas o
  apagavam), maior em 48 e 64.
- **Peça central:** sulco, base (só em 48 e 64: em 32 fazia dentes), cúpula em faixas e o brilho desenhado por tamanho
  (`BRILHO_CUPULA`; a conta de um disco saía em cruz).
- **Cravos por tamanho:** 1 px em 32, 2×2 com sombra em 40 e 48, cabeça redonda de 3×3 em 64 (em cruz pareciam
  estrelas).
- **O 40:** medidas entre as de 32 e 48. O cravo de cima à esquerda caiu no meio do reflexo e a sombra escura dele
  partia o reflexo em dois; a correção (em `AJUSTES[40]`) clareou a sombra para um ferro claro e subiu um tom do canto
  do cravo, sem mexer no resto.
- **Paleta:** 9 tons de ferro, 9 de latão e o contorno; 17 a 18 cores por arquivo.

## O Unguento de Prata (pote de cerâmica de boticário)

`ferramentas/arte/desenhar_unguento_pixel.py`; 32 e 64 px (o 48 do voo é o 32 a 2× reduzido pelo navegador).

- **Conceito:** o pote de louça de paredes retas com rótulo azul-esverdeado lembrava embalagem moderna (decisão do
  Jean); virou um pote baixo e arredondado de cerâmica, com a boca espessa e a pasta cinza-prateada à vista, sem
  rótulo. A tampa ao lado ficou de fora: em 32 tirava largura do pote sem ajudar a ler.
- **Forma de revolução:** cada volta horizontal é uma elipse achatada por `K`; a barriga em superelipse, o pescoço
  curto, o fundo cortado na elipse de baixo. Visto um pouco de cima (`K` 0,44): com menos, a pasta virava uma faixa
  no tamanho real.
- **Barro fosco:** quatro faixas largas de luz, sem reflexo (faixas finas liam como veios; um brilho no ombro, como um
  cisco); a última linha do fundo não acende.
- **Boca:** lábio grosso com o topo aceso, a espessura na frente e a sombra no pescoço; a parede de dentro escura,
  para a abertura ler no 32 (a pasta desceu um degrau e mais parede aparece).
- **Pasta:** cinza frio contra o barro quente, luz macia em volta de um ponto, a ponta de onde a espátula saiu; sem
  especular.
- **Papel:** o desenho "unguento" do jogo é também a Curandeira; o item se acha só pelo id (`SO_PELO_ID`).
- **Paleta:** barro (9 tons) e prata (8); 14 cores por arquivo.

## O que se repetiu nos dois (e por isso está no SKILL.md)

Ler o jogo antes de desenhar; a grade de cada tamanho com as medidas numa tabela; uma rampa e uma regra de luz por
material; o que é de um tamanho decidido naquele tamanho; conferir em 1× sobre o carvão e no jogo, não só ampliado;
fotografar com o jogo intacto. O histórico completo das rodadas está em `ferramentas/prototipos/hud/LEIA-ME.md`
("Teste do escudo" em diante) e a comparação lado a lado em `ferramentas/prototipos/hud/itens-icones-teste.html`.
