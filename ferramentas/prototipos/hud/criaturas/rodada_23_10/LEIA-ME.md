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

# A segunda rodada: a Harpia T, o Grifo GA3 e o Xamã X1r (propostas; nada no jogo)

**A avaliação do Jean:** nenhuma Harpia aprovada (a H3 e a HA foram as mais próximas e ficam como histórico); a nova
referência gerada na conversa, `ferramentas/arte/referencias/icones/Harpia vulturina em pixel art.png`, passa a ser a
principal da Harpia. No GA2 a limpeza melhorou, mas a ponta ficou reta: recuperar o gancho. Do Xamã, o X1 foi escolhido
como direção (ainda não autorizado para o jogo): refinar com contenção. O GA2, as H1 a H3 e os X1 a X3 continuam aqui
como estavam.

## A Harpia T, a transposição da referência (`harpia-t`)

- **A guia** (`guias/harpia-t-guia-16.png`, a camada `guia` oculta na fonte, fora da exportação): o recorte quadrado de
  1000 px a partir de (200, 120) da referência (1254×1254, ampliada; não é uma grade nativa), reduzido a 16 por média,
  sem esticar: cada pixel vale 62,5 px. O recorte tira só a ponta das penas do alto e a borda de baixo, para o rosto
  ocupar umas 7 colunas, como os rostos dos retratos do jogo.
- **Medido na guia e redesenhado à mão:** em três quartos para a esquerda; a testa pálida (colunas 1–5, linhas 2–4); a
  sobrancelha pesada descendo para o nariz e o olho âmbar da frente sob ela (linhas 5–6); o olho de trás num âmbar mais
  escuro, junto da pena da têmpora; o nariz curvo saindo do perfil até a coluna 1 (linhas 7–8); a boca fechada numa
  linha (linha 9); o queixo, a sombra da mandíbula subindo até a orelha; o pescoço na sombra entrando na gola clara
  (colunas 3–12, linhas 10–15); os ombros de penas escuras dos dois lados, o direito ligado ao cabelo.
- **Simplificado de propósito:** os fios das penas viram cinco tufos varrendo para trás a partir das duas têmporas,
  cada um com a luz em cima; as rugas e as marcas da pele saem; a gola vira três tons com tufos.
- **Na bancada:** o primeiro rascunho, tom a tom pela guia, saiu lamacento (o cabelo salpicado de tons médios lia como
  cabelo crespo; os dois olhos iguais, separados pelo nariz, liam como óculos; a gola era uma placa). Mais contraste,
  o olho de trás escuro (perspectiva), os tufos agrupados e os tufos na gola resolveram; o pixel escuro sob o nariz
  alargava a boca e saiu.
- A paleta é a da referência (`PALETAS["harpia_t"]`); as camadas penas, gola, pescoço, cabelo e rosto, mais a guia.

## O Grifo GA3, o gancho do bico (`grifo-ga3`)

- No GA2 a ponta escura ficava em (13,8), embaixo da extremidade (14,7): a ponta terminava num corte vertical.
- **O retoque (dois pixels, só a linha 8):** a mandíbula de baixo termina amarela em (13,8) e a ponta escura desce da
  própria extremidade, em (14,8). O escuro é o marrom do pelo (`q`), porque o `d` sumia contra a caixa escura da
  carta. A mancha da primeira versão não volta; o rosto, o olhar, os tufos, a paleta, o peito e o enquadramento são os
  do GA2.
- Na bancada: com dois escuros (o `d` mantido e o novo) voltava a mancha; com a ponta toda amarela, um bloco reto; com o
  escuro dentro e a ponta amarela embaixo, o bico alongava.

## O Xamã X1r, o X1 refinado (`xama-caido-x1r`)

- **A cabeça é a do X1, pixel a pixel** (as linhas 0 a 10): a tentativa de subir o rosto uma linha para ganhar testa
  alongava a cara e a afastava do CA, sem melhorar a 32; ficou de fora.
- **O colar e a base (linhas 11 a 15):** as contas de osso deixam o V largo que ia do queixo à borda e viram um U
  pequeno de cinco contas logo abaixo do queixo (as de baixo na sombra do osso); a capa de couro fecha a parte de
  baixo. O queixo e o pescoço ganham ar e o colar não domina mais a base. Sem cajado nem fogo.
- Na bancada: com o colar descido até a borda, o pescoço vermelho ficava comprido demais.

## A minha leitura (quem escolhe é o Jean)

- **Harpia T:** a construção da referência aparece a 32 (o rosto pálido de perfil, o olhar âmbar sob a sobrancelha, o
  nariz curvo, as penas varrendo para trás, a gola clara de abutre). **Limitação:** a 32 é mais "mulher de cabelo
  selvagem com gola de penas" do que abutre; o lado ave vem da gola e dos ombros. A crueldade está na sobrancelha e
  na boca, poucos pixels.
- **GA3:** a ponta sugere o gancho descendo e continua limpa. **Limitação:** é sutil a 32 (um pixel).
- **X1r:** a mudança é contida e só embaixo; o rosto é o mesmo do X1. Prefiro o X1r pela base mais calma; se o Jean
  achar que a 32 não faz diferença, o X1 continua disponível.

## Processo desta rodada

- **O conector do Aseprite funcionou:** o bridge desta sessão escutava a 6515, mas o Aseprite estava fechado; aberto o
  Aseprite, a extensão conectou (121 comandos). A janela do Jean que já estava aberta não foi tocada.
- As grades à mão em `auxiliares/grades.py` (`HARPIA_T`, `GA3`, `X1R`; `python grades.py .. harpia-t grifo-ga3
  xama-caido-x1r`). As fontes pelo conector: o sprite RGBA 16×16, as camadas de baixo para cima e o `pintar.lua` em
  cada uma (0 diferentes na releitura), a guia por `Image{fromFile=...}` oculta; o composto do editor com os mesmos
  pixels opacos das camadas visíveis (210, 179, 226). A exportação (`python exportar.py harpia-t grifo-ga3
  xama-caido-x1r`): igual à grade, sem a guia, o @2x exato, o 32 e o 48 em blocos inteiros do 16.
- As fotos: o modo `d` do `fotografar.mjs` (o GA3, a T e o X1r; `MODOS=d`), a 1920×945, sem erro no console; as
  fotos dos outros modos continuam valendo (o jogo não mudou).
- **As três folhas compactas** (`python auxiliares/prancha.py harpia-t grifo-ga3 xama-x1r`): `harpia-t.png` (a
  referência, a guia e a T a 12×; o jogo de hoje × a T na carta e no Bestiário; a fileira com os retratos aprovados),
  `grifo-ga3.png` (GA2 × GA3) e `xama-x1r.png` (X1 × X1r).

## O Grifo no jogo (1.183.0)

- **Aprovado pelo Jean e integrado sem retoque:** o GA3, pela família (`RETRATO_FAMILIA`, o papel `CRIATURA` e os
  `TAMANHOS` em `icones.js`), também o feroz do ninho de grifo. A Harpia (família própria, ainda sem retrato) e o
  Dragão de Gelo continuam no `voador`. O GA e o GA2 ficam como histórico.
- A fonte em `ferramentas/arte/aseprite/retrato-grifo/` (a cópia byte a byte de `fontes/grifo-ga3/`); o 32 e o 48 em
  `DERIVADOS`; os seis PNGs idênticos byte a byte aos de `proposta/grifo-ga3-*`; `exportar_aseprite.py retrato-grifo
  --conferir`: tudo igual ao jogo.
- Conferido a 1920×945 com os arquivos de produção (`capturas-1183/`, `auxiliares/fotografar_jogo.mjs`): a luta (o
  grifo com duas harpias no voador e o lobo gélido), o Bestiário, o cartaz do mural e o rastreador; nenhum pedido a
  `ferramentas/`; sem erro no console. A folha: `ferramentas/prototipos/hud/integracoes-22-10/integracoes-1183.png`.
