# Levantamento: o animal no acampamento e o comando Atacar (21/10/2026; nada no jogo)

**Pedido de Jean:** registrar as duas pendências no plano 23 e conferir os caminhos, os tamanhos e os compartilhamentos
dos dois usos; testar o arco de equipamento aprovado no tamanho real do Atacar do Arqueiro; conferir o desenho do
comando com uma Besta, sem mudar a regra; uma conferência rápida dos ataques básicos das três classes. Só levantamento
e teste visual: nada desenhado para o acampamento, nada integrado.

## 1. O animal do patrulheiro no acampamento

- **O caminho:** `telas/acampamento.js`, `roda()`: `spr: d.fera.tipo === "falcao" ? "voador" : "fera"`, na vaga `FERA`
  (`[120, 66]`, à esquerda do herói, sem assento, com a sombra no chão); `Icones.figura(spr)` cai no sprite do jogo
  (`Sprites.canvas`), aquecido pela luz do fogo (`aquecido`). A arte da cena tem 320×72; a 1920×945 ela ocupa o canvas
  de 1064×208 (cerca de 3,3×). O ponto clicável é a área de 16×19 do desenho (`area`); o balão de reação e os corações
  (`telas/celebracoes.js`) saem de cima dele; o menu (carinho, poção) é o de `telas/comitiva.js`.
- **O que cada um recebe hoje (fotos `capturas/fogueira-*.png`):** o **lobo e o urso o mesmo `fera`**, a cabeça de
  lobo cinza de olhos vermelhos (o urso, então, aparece como um lobo); o **falcão o `voador`**, o morcego de asas
  abertas. Os três são cabeças ou ícones de traço, soltos no chão, ao lado das figuras sentadas de corpo inteiro do
  herói e dos companheiros.
- **Os compartilhamentos que não podem mudar:** o `fera` e o `voador` são os sprites dos traços (`TRACOS` em
  `dados.py`), dos retratos dos inimigos sem retrato próprio, da carta aliada quando falta o retrato do animal
  (`batalha.js`) e do bilhete do nêmesis (`telas/contratos.js`). A troca do acampamento tem de ser um papel próprio,
  pelo tipo do animal, como o `ANIMAL` da carta aliada (`Icones.animal`), e não uma mudança nesses sprites.
- **A proposta (para desenhar depois da avaliação):** uma figura de 16×16 por animal, de corpo inteiro e de perfil
  virado para o fogo (para a direita), na linguagem das figuras da fogueira (o mesmo tamanho, a mesma luz do fogo pelo
  `aquecido`, a sombra no chão), com a identidade e a paleta dos retratos aprovados:
  - **Lobo Cinzento:** deitado com a cabeça erguida, as orelhas em pé, o cinza do `retrato-lobo` com o focinho e o peito
    claros e o olho âmbar de um pixel; a mesma cara do lobo aprovado, o corpo baixo e comprido.
  - **Urso Pardo:** sentado, pesado, ocupando a largura toda do quadro: o marrom do `retrato-urso`, as orelhas redondas,
    o focinho claro e os olhos pequenos e fundos; o volume é o que o separa do lobo.
  - **Falcão Peregrino:** pousado num toco ou numa estaca (para chegar à linha do chão sem flutuar), de perfil, as asas
    fechadas: o dorso cinza-azulado, a máscara escura, a garganta e o peito claros do `retrato-falcao`; menor que os
    outros dois.
  - **Onde entra:** um papel novo de figura pelo tipo (por exemplo, `Icones.figuraAnimal(tipo)` ou um mapa ao lado do
    `ANIMAL`), escolhido em `roda()` pelo `d.fera.tipo`; a vaga, a área clicável e o balão continuam os mesmos.

## 2. O comando Atacar

- **O caminho:** `classes.py` (`icone_ataque`: `espada`, `arco`, `cajado`) → `grimorio.dados` (`basico.icone`) →
  `app/escolhas.js` (`iconeAtaque()`) → `Icones.acao(arma) || spr(arma, 2)`. O papel `ACAO` de `icones.js` só tem a
  espada (o arquivo `espada-32`, aprovado); o arco e o cajado caem no sprite 16×16 a 2×. O ícone aparece a 32 px na
  caixa de 34 (`.rb-icone`, `css/15-hud-luta.css`).
- **Com a Besta:** o ícone é da classe, não da arma: com a Besta Leve equipada (`ARMA=besta`), o comando continua com o
  sprite `arco` (`capturas/roda-arqueiro-besta.png`). A regra fica como está.
- **O teste do arco aprovado** (`capturas/roda-arqueiro-arco.png`, troca só na página): o `arco-32` (o arco de teixo da
  1.101.0, o de equipamento) cabe exato nos 32 px, na diagonal, com a corda fina visível; lê melhor que o sprite (o
  arco de frente em D) e conversa com a espada do Guerreiro. Se aprovado, a integração seria o mesmo caminho da espada:
  `ACAO.arco = "arco"`, sem tocar no sprite (o Tiro Duplo e o contrato de caça continuam com ele).
- **A conferência dos três ataques básicos:**
  - Guerreiro: a espada aprovada (desde a 1.145.0). Em dia.
  - Arqueiro: o sprite antigo `arco` (o teste acima).
  - **Mago: o sprite antigo `cajado`**, 16×16 a 2×, com o mesmo caminho. Existe o cajado de equipamento aprovado
    (1.106.0, `cajado-32`), e ele poderia passar pelo mesmo teste; não testado nesta entrega (fora do lote).
  - Fora da roda: a página do ataque básico no Grimório (`telas/grimorio.js`) usa os sprites 16×16 das três classes
    (a espada inclusive), como as habilidades; fica com os ícones de habilidade, na etapa 8.

## Processo

- `tests/navegador/cenarios.py`, o cenário `fogueira`: `FERA=urso` e `FERA=falcao` além do lobo (`FERA=1`).
- `auxiliares/fotografar.mjs` (a 1920×945; sem erro nem aviso no console em nenhuma situação) e
  `auxiliares/prancha.py`: a folha `levantamento.png` (a fogueira com os três animais em tamanho real e 2×, os
  retratos aprovados, o Atacar das três classes em tamanho real e 4×, sem suavização, e a roda inteira com e sem o arco
  aprovado).

## No jogo desde a 1.169.0: o arco no Atacar do Arqueiro

- **Decisão de Jean:** o teste do arco ficou bom; integrar reutilizando o arquivo existente, com a escolha pela classe
  (com a Besta também).
- `rpg/web/static/icones.js`: `ACAO.arco = "arco"` (o `arco-32` do equipamento, sem arquivo novo). O ícone continua
  vindo de `icone_ataque` da classe; o Tiro Duplo e o contrato de caça continuam com o sprite.
- Conferido no jogo, com os arquivos reais (`capturas-1169/`, o mesmo `fotografar.mjs`): o Arqueiro com o arco e com a
  Besta Leve mostram `arco-32` a 32 px; o Guerreiro a espada; o Mago continua com o sprite (o cajado está em teste).

## Os animais no acampamento (proposta, 21/10/2026; nada no jogo)

- **Pedido de Jean:** uma figura de corpo inteiro por animal, só no protótipo: o lobo deitado, de cabeça erguida,
  voltado para o fogo; o urso sentado, pesado, com anatomia de urso; o falcão pousado num toco, com o bico curvo, a
  máscara escura e o peito claro. A identidade e a paleta dos retratos aprovados, a linguagem das figuras da fogueira,
  uma escala convincente com os personagens (sem encher igual os 16×16).
- **As figuras** (`animal-lobo`, `animal-urso`, `animal-falcao`; 16×16, de perfil para a direita, os pés na linha de
  baixo, sem contorno; as grades e as camadas em `auxiliares/grades.py`):
  - **lobo** (corpo, cabeça, detalhes): deitado e comprido, a cabeça erguida com as orelhas em pé, o olho âmbar, o
    focinho e o peito claros, as patas da frente estendidas, a cauda no chão; o mais baixo dos três;
  - **urso** (corpo, cabeça, detalhes): sentado, a cabeça grande no alto com as orelhas pequenas e redondas, as costas
    descendo até a garupa larga, o focinho claro com o nariz escuro, a sombra do pescoço, a pata da frente; o maior,
    mas abaixo do arqueiro sentado;
  - **falcão** (toco, corpo, cabeça, detalhes): ereto num toco, o capuz escuro, o olho com o anel amarelo, o bico curvo
    com a ponta para baixo, o bigode escuro, a garganta e o peito claros, a asa cinza-azulada e as pontas passando da
    cauda, os pés amarelos.
- **Na bancada:** o urso começou como um castor (o focinho comprido como um bico) e depois parecia um esquilo (o
  corcunda arredondado lia como uma cauda peluda): a cabeça cresceu e subiu, e as costas passaram a descer dela até a
  garupa. O falcão começou como um pinguim (o peito branco largo): a asa passou a cobrir o lado, o peito estreitou e a
  cauda cresceu.
- **Na cena** (`capturas/fogueira-<tipo>-proposta.png`): a figura que a cena pede para o animal vira, só na página, a
  proposta do tipo; a sombra no chão e a luz do fogo (`aquecido`) são as do jogo. Os três ficam menores que o arqueiro
  sentado ao lado, o urso o maior e o falcão o menor.
- **A seleção futura:** um papel próprio pelo tipo (por exemplo, um mapa `FIGURA_ANIMAL` em `icones.js` e
  `Icones.figuraAnimal(tipo)`), pedido em `acampamento.js` (`roda()`, pelo `d.fera.tipo`), com os PNGs em
  `rpg/web/static/hud/icones/` e as fontes em `ferramentas/arte/aseprite/`; os sprites `fera` e `voador` continuam nos
  outros papéis.
- **Processo:** as fontes no editor pelo conector (`pintar.lua`; releitura das camadas contra a grade, 0 diferentes; o
  composto com a soma das camadas: 76, 131 e 69) em `fontes/animal-<tipo>/`; a exportação conferida
  (`auxiliares/exportar.py`: igual à grade, @2x exato); o conector respondendo depois do lote.

## O cajado no Atacar do Mago (teste, 21/10/2026; nada no jogo)

- O `cajado-32` aprovado (o cajado de carvalho com o cristal, 1.106.0) trocado só na página no lugar do sprite
  (`capturas/roda-mago-cajado.png`): cabe exato nos 32 px, na diagonal como o arco e a espada, e o cristal azul
  continua a ler. A integração seria `ACAO.cajado = "cajado"`; o traço Conjurador dos inimigos continua com o sprite.

A folha `animais-cajado.png` (`python auxiliares/prancha.py animais`): cada animal na fogueira, hoje × proposta (tamanho
real e 2×), a figura a 8× e o retrato aprovado; o Atacar do Mago, hoje × o cajado, em tamanho real e 4×.

## A segunda rodada do lobo e do urso (21/10/2026, proposta; nada no jogo)

- **Jean:** o lobo na direção certa (deitado, atento, voltado para o fogo), mas o pescoço muito vertical e o corpo uma
  faixa achatada; o urso parecia um roedor sentado (as costas muito arredondadas, o focinho estreito, a pata pequena).
  O falcão e o teste do cajado ficam como estão.
- **Lobo r2** (`animal-lobo-r2`): o pescoço desce na diagonal da cabeça até as costas, a cabeça à frente do peito, o
  corpo deitado com seis linhas de volume, as patas da frente estendidas no chão para o fogo, a cauda atrás; a garganta
  clara só embaixo do focinho (numa passada, a coluna clara do focinho ao peito lia como uma figura sentada).
- **Urso r2** (`animal-urso-r2`), pelas fotos de urso pardo sentado (Wikimedia Commons, só para a anatomia) e pelo
  retrato aprovado: a forma de sino (as costas descendo do corcunda até a garupa larga no chão; a lateral reta dava uma
  caixa), a cabeça larga em leve três quartos, as orelhas pequenas e redondas, o focinho curto e robusto com o nariz na
  ponta, o pescoço curto, as patas da frente em duas colunas grossas, a coxa de trás como um plano com o pé à frente; a
  cabeça no marrom do retrato (clara demais, virava um bicho de pelúcia).
- **Na bancada, na cena:** cada passada fotografada na fogueira (`ANIMAIS=<pasta>` no `fotografar.mjs`), ao lado do
  arqueiro sentado e com a luz do fogo, antes de ir ao editor.
- **Processo:** as fontes pelo conector (`pintar.lua`; releitura, 0 diferentes; o composto 95 e 140); a exportação
  igual à grade, @2x exato; a primeira rodada preservada (reexportada igual). As fotos `capturas/fogueira-<tipo>-r2.png`.
- A folha `rodada2.png` (`python auxiliares/prancha.py rodada2`): antes × depois do E1, do lobo e do urso.

## A terceira rodada do lobo e do urso, pelas referências geradas (21/10/2026, proposta; nada no jogo)

- **Pedido de Jean:** refazer os dois pelas duas referências geradas (`ferramentas/arte/referencias/icones/Lobo
  cinzento deitado em pixel art-1.png` e `Urso-pardo sentado em pixel art-2.png`), a direção principal de anatomia,
  pose e proporções; o pelo em poucas áreas, as paletas dos retratos aprovados, o acabamento das figuras da fogueira;
  o urso mais volumoso que o lobo e a escala coerente com o personagem sentado.
- **As guias** (`guias/lobo-guia-16.png`, `guias/urso-guia-16.png`): o animal recortado pela caixa dele (sem o halo e o
  fundo) e reduzido pela média só onde há animal; o lobo com 15 px de comprimento (8 de altura), o urso com 12 de altura
  (12 de largura), os pés na linha de baixo. Ocultas nas fontes.
- **Lobo r3** (`animal-lobo-r3`): o corpo baixo no chão, com as costas retas na linha 12 (nada de rampa), a cabeça
  erguida para a direita com as orelhas, o olho âmbar e o focinho comprido, o pescoço saindo dos ombros, o peito claro,
  a coxa de trás clara, as patas da frente estendidas para o fogo, a cauda atrás.
- **Urso r3** (`animal-urso-r3`): sentado em leve três quartos para a direita, a cabeça larga com as orelhas pequenas,
  o olho e o focinho claro com o nariz na ponta, o pescoço curto, as costas descendo da nuca à garupa, o plano claro do
  braço, as duas patas da frente grossas até o chão, a coxa de trás com o pé à frente; 12 linhas de altura (o lobo 8),
  abaixo do arqueiro sentado.
- **Processo:** a primeira passada já conferida na fogueira, com a luz do fogo e ao lado do arqueiro (`ANIMAIS=<pasta>`
  no `fotografar.mjs`); as fontes pelo conector com a guia oculta (`Image{fromFile=...}`; `pintar.lua`, releitura das
  camadas, 0 diferentes; o composto 68 e 119); a exportação igual à grade, @2x exato; a primeira e a segunda rodada, o
  falcão e o cajado reexportados iguais. As fotos `capturas/fogueira-<tipo>-r3.png`.
- A folha `rodada3.png` (`python auxiliares/prancha.py rodada3`): a referência e a guia, antes (r2) × depois (r3) na
  fogueira, em tamanho real e a 2×, e as figuras a 8×.

## A quarta rodada: o refinamento do lobo e do urso (22/10/2026, proposta; nada no jogo)

- **Jean, sobre a r3:** a construção melhorou, mas falta clareza na cena. No lobo, a coxa virou uma mancha clara e o
  peito com as patas parecia um bloco vertical separado do corpo; o nariz precisava ler. No urso, a cabeça lembrava um
  cachorro, as patas eram duas hastes e a coxa tinha divisões internas.
- **Lobo r4** (`animal-lobo-r4`, a mesma silhueta baixa): a coxa no cinza claro médio; o peito sem o bloco claro; as
  patas da frente numa faixa contínua apoiada no chão (o claro em cima, o meio embaixo), saindo do peito para o fogo;
  a sombra embaixo do focinho, para o nariz escuro ler na ponta.
- **Urso r4** (`animal-urso-r4`): a cabeça mais larga (oito colunas), com as orelhas redondas nos cantos; o focinho
  curto e claro com o nariz escuro na ponta; a linha escura entre a mandíbula e o peito; o corcunda arredondando o alto
  das costas (na primeira passada, as costas eram uma rampa reta da orelha à garupa); o peito num plano claro; as patas
  da frente com a base larga no chão; a coxa num volume só, com um plano de luz e o pé à frente. Treze linhas de
  altura, o lobo oito.
- **Na bancada:** duas passadas, cada uma fotografada na fogueira a 1920×945 antes do editor.
- **Processo:** as fontes pelo conector com a guia oculta (`pintar.lua`; releitura das camadas contra a grade, 0
  diferentes; o composto 68 e 137, a soma das camadas); o PNG exportado pela linha de comando (o composto do arquivo
  salvo) igual à grade, @2x exato; as rodadas anteriores, o falcão e o cajado reexportados iguais. As fotos
  `capturas/fogueira-<tipo>-r4.png`; a folha `rodada4.png` (`python auxiliares/prancha.py rodada4`, o mesmo
  enquadramento da `rodada3.png`).
- **A minha leitura em tamanho real:** o lobo lê como um corpo só, da cabeça às patas, e a coxa não salta mais; o nariz
  aparece, mas é um pixel e some um pouco contra o fundo escuro. O urso lê como urso (a cabeça larga, as orelhas, o
  focinho curto) e pesado ao lado do lobo e do arqueiro; o limite é a silhueta, ainda um pouco triangular de longe, e as
  patas, que a 1× se juntam num bloco claro na base.

## O lobo r5, mais alto (22/10/2026, proposta; nada no jogo)

- **Jean, sobre o lobo r4:** achatado demais (o tronco uma faixa no chão, a cabeça pequena para reconhecer o lobo); as
  oito linhas de altura deixam de ser restrição. O urso r4, o falcão e o resto ficam.
- **Lobo r5** (`animal-lobo-r5`, onze linhas): a cabeça maior (seis linhas), com as orelhas, o olho âmbar, o focinho, o
  nariz na ponta e a linha escura da boca e da mandíbula separados; o pescoço curto ligado aos ombros; o tronco mais
  grosso, com o volume dos ombros e as costas planas (na primeira passada, as costas desciam em rampa até a cauda); as
  patas da frente apoiadas no chão e a cauda atrás. Redesenhado na grade, não esticado do r4.
- **A guia** (`guias/lobo-guia-r5-16.png`): a referência na nova escala (onze linhas de altura), presa pela cabeça à
  direita; a ponta da cauda fica fora do quadro (nessa escala o lobo da referência tem 21 px). Oculta na fonte.
- **Processo:** duas passadas na fogueira, ao lado do arqueiro e com o urso r4 na mesma cena; a fonte pelo conector
  (releitura das camadas, 0 diferentes; o composto 107, a soma das camadas); o PNG exportado igual à grade, @2x exato;
  as outras rodadas, o urso r4 e o falcão reexportados iguais. A foto `capturas/fogueira-lobo-r5.png`; a folha
  `lobo-r5.png` (`python auxiliares/prancha.py lobo-r5`).
- **A minha leitura em tamanho real:** um lobo adulto deitado e atento, a cabeça agora reconhecível (as orelhas, o olho,
  o focinho com o nariz); o urso continua mais pesado. O limite: o pescoço e o peito claros ainda se juntam numa faixa
  vertical, na sombra da luz do fogo.
