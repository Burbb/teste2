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
