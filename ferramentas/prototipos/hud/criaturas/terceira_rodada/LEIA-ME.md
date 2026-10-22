# A terceira rodada (22/10/2026; propostas, nada no jogo)

**Pedido de Jean**, depois da avaliação da segunda rodada (o cultista A, a bruxa B3 e o rato r2 foram para o jogo na
1.172.0): o carniçal A2 com a bochecha direita menos larga (a boca e os dentes aprovados); o javali A2 com a curvatura
de presa de javali (o tamanho e a grossura preservados); o espectro no conceito corporal escolhido (a referência gerada
`ferramentas/arte/referencias/icones/Espectro do Manto Inflado.png`), no retrato de 16×16 com a cabeça e o começo dos
ombros. Uma proposta de cada.

## As propostas

- **Carniçal A3** (`carnical-a3`; corpo, rosto, boca): o A2 com a bochecha direita recolhida. Nas linhas 8 e 9, a
  cabeça ia até a coluna 13, um pixel além do resto (as colunas 3 a 12): o pixel sai e a sombra passa à coluna 12. A boca,
  a mandíbula aberta e o resto iguais. Um retoque local na cópia da fonte do A2 (quatro pixels).
  **Limite:** a mudança é discreta; a 32 px o rosto ainda é largo, porque a boca aberta ocupa a largura toda.
- **Javali A3** (`javali-a3`; corpo, focinho, presas, olhos): o rosto do A com as presas refeitas em arco. A base grossa
  sai da boca ao lado do focinho, abre para fora, sobe na vertical e afina na ponta, que volta para dentro (o arco de
  dente de javali, não a diagonal reta do A2); o tamanho e a grossura das do A2, maiores que as do Troll.
  **Limite:** a 32 px os dois arcos abraçam a cabeça e podem lembrar um par de parênteses; a ponta afinada só se lê bem
  a 48 px.
- **Espectro M** (`espectro-m`; manto, rasgos, cavidade, olho; a guia oculta): pela referência do manto inflado, com a
  identidade do A (o azul-acinzentado, a cavidade escura, o olho único claro). O capuz pequeno no alto, a sombra na base
  dele, o pano que incha nos ombros e desce até a borda de baixo (o corpo continua fora do quadro, nada de tiras
  suspensas), a luz à esquerda, os rasgos escuros em fenda. Na bancada, a primeira passada virou um sino com furos (o
  capuz fundido ao corpo, o olho pequeno): o capuz ganhou a sombra na base e a cavidade cresceu.
  **Limite:** o olho é uma fenda de dois pixels e lê menos que o olho redondo do A; o retrato fica mais claro e mais
  pesado que os da fileira.

## Processo

- As grades em `auxiliares/grades.py`; as fontes no Aseprite pelo conector (`pintar.lua`; a releitura das camadas, 0
  diferentes; o composto igual à soma das camadas; a guia do espectro oculta) em `fontes/<id>/`; a exportação conferida
  (`auxiliares/exportar.py`: igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros).
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`): uma luta e o Bestiário com as três, junto de criaturas integradas
  (o Troll ao lado do javali), nos modos atual, antes e depois, os mesmos dados; trocadas só na página (protótipo). Sem
  erro nem aviso no console.
- As folhas: `carnical.png`, `javali.png`, `espectro.png` (`python auxiliares/prancha.py`).

Nada integrado. O Esqueleto E1r, o urso e o falcão do acampamento, o cajado e as propostas anteriores ficam como estão.

## No jogo desde a 1.173.0: o javali A3 e o carniçal A3

- **Decisão de Jean:** o Javali A3 e o Carniçal A3, sem retoques; o espectro M não foi escolhido.
- As fontes conferidas iguais às do commit da proposta e levadas para `ferramentas/arte/aseprite/retrato-javali/` e
  `retrato-carnical/`; os doze PNGs idênticos byte a byte; `--conferir` igual ao jogo.
- No motor, `RETRATO_FAMILIA` ganhou `javali` e `carnical`; em `icones.js`, o papel `CRIATURA` e os tamanhos;
  `tests/test_retratos.py` confere as famílias e o esqueleto e o cavaleiro na caveira. O gabarito mudou de propósito só
  no valor do retrato dos inimigos nas transcrições -web.
- Conferido nos usos reais com os arquivos do jogo (`capturas-1173/`): a luta e o Bestiário, sem erro no console.

## O espectro AP: o A com o pano até a borda (22/10/2026, proposta; nada no jogo)

- **Decisão de Jean:** o M não foi escolhido; voltar ao `espectro-a` (`../quatro_pares/`), preservando exatamente a
  cabeça, o capuz, a cavidade, o olho, a paleta, a perspectiva e a posição; o único ajuste é o pano da parte de baixo
  continuar até a borda inferior, saindo do quadro. O corpo enorme fica para a arte de cenário; a referência do manto
  inflado fica como conceito do corpo, sem ditar as proporções do ícone.
- **O ajuste** (`espectro-ap`; névoa, vazio): numa cópia da fonte do A, os vãos das linhas 11 a 15 fechados, o pano
  abrindo um pouco até a largura toda embaixo, com as dobras em sombra. Pelo conector: 50 pixels escritos na camada da
  névoa, 0 diferentes na releitura, e o composto do editor mudou só abaixo da linha 11 (0 pixels acima); as linhas 0 a
  10 são idênticas às do A. O composto bate com o PNG exportado; o 32 e o 48 são ampliações inteiras exatas.
- A comparação `espectro-ap.png` (`python auxiliares/espectro_ap.py`): o A × o AP na carta e no Bestiário em tamanho
  real, na fileira e a 12×, com a referência do corpo ao lado. O A e o M ficam como histórico.
- **A minha leitura:** o AP fecha o retrato como os outros bustos da fileira (o pano saindo do quadro, como os ombros do
  afogado e do cultista), sem mudar a cabeça. Limite: embaixo o pano fica uma massa clara sem os rasgos, e a figura perde
  um pouco do ar de coisa que flutua.

## O espectro AP2 (22/10/2026, proposta; nada no jogo)

- **Jean, sobre o AP:** as duas linhas verticais escuras de baixo sugeriam braços ou ombros que o conceito não tem; e a
  abertura do capuz devia ser mais ampla, cercada pelo tecido, como na referência do corpo inteiro.
- **O ajuste** (`espectro-ap2`), numa cópia da fonte do AP: as dobras escuras das colunas 5 e 10 (linhas 12 a 15)
  trocadas pelo pano ao redor, sem abrir transparência; a cavidade alargada de quatro para seis colunas nas linhas 5 a 7
  (e a borda dela nas 4, 8 e 9), com o tecido do capuz em volta e o olho no mesmo lugar (as colunas 7 e 8). Pelo
  conector: 26 pixels no composto, todos nas linhas 4 a 9 e 12 a 15, nenhum transparente novo; 0 diferentes na
  releitura; o composto bate com o PNG exportado; o 32 e o 48 em blocos inteiros.
- A comparação `espectro-ap2.png` (`python auxiliares/espectro_ap.py ap2`): o AP × o AP2 a 32 e 48 px, na fileira e a
  12×, com a referência do corpo ao lado. O A, o M e o AP ficam como histórico.
- **A minha leitura:** a cavidade larga dá mais o vazio dentro do capuz da referência, e o pano sem as dobras deixa de
  sugerir braços. Limite: com a cavidade maior, a borda esquerda do capuz fica com dois pixels de tecido, e a 32 px a
  massa clara de baixo fica lisa.

## No jogo desde a 1.174.0: o espectro AP

- **Decisão de Jean:** o Espectro AP (`d4f34b5e`), sem retoques; não o AP2. O A, o M e o AP2 ficam como histórico.
- A fonte conferida igual à do commit escolhido e levada para `ferramentas/arte/aseprite/retrato-espectro/`
  (`exportar_aseprite.py retrato-espectro`, `DERIVADOS` 32 e 48); os seis PNGs idênticos byte a byte; `--conferir` igual
  ao jogo.
- No motor, `RETRATO_FAMILIA` ganhou `espectro`; em `icones.js`, o papel `CRIATURA` e os tamanhos; `tests/test_retratos.py`
  confere a família, a cria do Vazio e o Lich no `etereo`. O gabarito mudou de propósito só no valor do retrato (uma
  transcrição -web, 30 linhas).
- Conferido na carta e no Bestiário com os arquivos do jogo (`capturas-1174/`), sem erro no console.
- A referência `Espectro do Manto Inflado.png` continua registrada como o conceito do corpo inteiro, para a futura arte
  de cenário.
