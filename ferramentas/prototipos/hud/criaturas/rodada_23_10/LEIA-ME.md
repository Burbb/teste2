# A rodada depois do Caído CA (23/10/2026, propostas; nada no jogo)

**Pedido de Jean:** integrar o Caído CA (feito na 1.182.0, em `../caidos/`); e, só no protótipo, limpar a ponta do bico
do Grifo A, três Harpias novas do zero e três Xamãs Caídos novos, com o Caído CA como referência da espécie. As
propostas anteriores (`../harpia_grifo/`, `../caidos/`) ficam como histórico.

## O Grifo GA2 (antes × depois)

- **O defeito:** a mancha marrom junto da ponta do bico era a ponta escura (`d`) espalhada em cinco pixels: um na linha
  7, dois na 8, três sob a mandíbula de baixo, na 9, e um solto na 10. Ela engordava a ponta e fazia o bico parecer
  continuar para baixo.
- **A limpeza (`grifo-ga2`):** fica uma ponta escura só, no gancho (linha 8); a mandíbula de baixo termina amarela; o
  pixel solto sai. A cabeça, o olhar, os tufos, as cores e o enquadramento são os do GA, pixel a pixel no resto.
- A folha `grifo.png`: antes × depois na carta (real e 2×), no Bestiário e a 12×.

## As três Harpias (do zero)

- **H1, a abutre de rosto humano** (`harpia-h1`): de frente e encolhida como um abutre; a cabeça calva de mulher com
  fios ralos, as sobrancelhas fechadas, o olhar de ave, a boca fechada; o pescoço nu e escuro saindo da gola de penas
  claras; as asas fechadas subindo como ombros, de cima a baixo do quadro.
- **H2, a da asa erguida** (`harpia-h2`): em três quartos para a direita; a asa sobe do ombro, por trás dela, até o alto
  à esquerda, e o cabelo escuro se emenda nas penas dela; o pescoço nu, a gola.
- **H3, a de bico** (`harpia-h3`): de frente, o rosto de mulher (a testa, os olhos, as maçãs, o queixo) com o nariz e
  a boca fundidos num bico curto em gancho; o cabelo longo terminando em penas; a gola e as asas embaixo.
- **Na bancada:** o pescoço rosado de abutre, logo abaixo da boca, lia como língua nas três primeiras tentativas da H1 e
  da H2 (e numa ruga avermelhada depois); ficou na pele escura. A primeira H2 parecia uma mulher de xale (a asa não lia
  como asa); a asa subiu para o alto. A primeira H3, com o bico grande, era uma coruja; o bico encolheu e o rosto
  ganhou as maçãs e o queixo.

## Os três Xamãs (da cabeça do Caído CA)

- **X1, o velho do capuz** (`xama-caido-x1`): o capuz de couro atrás da cabeça, com os chifres furando; a pintura branca
  descendo dos olhos; o sorriso fechado de presas; o colar de contas de osso.
- **X2, o do cajado** (`xama-caido-x2`): o cajado de osso, na mão dele, com uma chama pequena no alto; a boca aberta
  conjurando; a capa.
- **X3, o das penas** (`xama-caido-x3`): o cocar de três penas; o rosto concentrado de boca fechada; uma chama pequena
  entre as mãos, abaixo do queixo (na primeira, a bola de fogo do peito dominava o retrato).
- O rosto é o do CA nas três (as proporções, os chifres, as orelhas, os olhos, a paleta): o xamã é do mesmo povo.

## A minha leitura (quem escolhe é o Jean)

- **Grifo:** o GA2 resolve o fim do bico sem mudar o resto. **Limitação:** o "leão" continua sendo só o peito dourado.
- **Harpia: prefiro a H1.** A silhueta de abutre encolhido (as asas como ombros, a cabeça calva sobre a gola) é a que
  mais une a mulher e a ave num corpo só, e lê a 32. **Limitação:** o rosto pálido e calvo, sem a boca aberta, pode ser
  lido como um velho ou um monge de capa; a crueldade fica no olhar, que são dois pixels de cada lado.
  - H2: a mais "mulher", com a asa ligada ao corpo; a 32 a asa vira uma massa escura à esquerda e o rosto fica pequeno.
  - H3: a mistura mais explícita (o bico no rosto); a 32 ainda lê mais como ave encapuzada do que como mulher.
- **Xamã: prefiro o X2.** O cajado é a forma mais legível do papel de feiticeiro a 32, fica fora do rosto e deixa o CA
  inteiro à vista, com a boca aberta de quem conjura. **Limitação:** o cajado come a orelha esquerda e um pouco da
  largura; a chama do alto é pequena, então a 32 o cajado lê como "bastão de osso", sem fogo evidente.
  - X1: a personalidade mais forte (o velho ardiloso), mas o capuz escuro e o colar deixam a cabeça menor e mais escura.
  - X3: o cocar lê como crista ou cabelo espetado a 32, e a chama ainda puxa o olho para baixo.

## Processo

- As grades à mão em `auxiliares/grades.py` (o GA2 e o rosto dos xamãs partem das grades aprovadas ou propostas, pelo
  próprio arquivo delas). **O conector do Aseprite continuou indisponível** ("Connection closed", sem ferramentas; a
  porta 6515 livre; religar pelo `/mcp`): as fontes em camadas saíram do Aseprite em lote (`python
  auxiliares/exportar.py --montar`, `montar_camadas.lua` com o `pintar.lua`; releitura 0 diferente); o composto
  exportado igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros. Sem guias.
- As fotos (`auxiliares/fotografar.mjs`, a 1920×945): a luta (o Arqueiro patrulheiro com o Falcão; a Harpia, o Grifo,
  dois Caídos com o retrato de produção e o Xamã) e o Bestiário, nos modos atual, antes (as propostas da rodada
  anterior), A, B e C; trocados só na página pelo nome; sem erro no console.
- As folhas `grifo.png`, `harpia.png` e `xama.png` (`python auxiliares/prancha.py`).
