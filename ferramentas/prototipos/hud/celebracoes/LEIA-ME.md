# Etapa 2, primeiro lote: subida de nível, celebrações e raridade (protótipo)

**Nada disto está no jogo.** O jogo nunca lê `ferramentas/`; as propostas só existem nas páginas do servidor de teste
(a demonstração) e nas do fotógrafo. A base é a 1.200.1.

## Testar no navegador (a demonstração)

`demo.bat` (ou `python ferramentas/prototipos/hud/celebracoes/auxiliares/demo.py`) monta as direções e abre o painel em
**http://127.0.0.1:8765/**. Cada cenário abre em **A · Relicário**, **B · Estouro**, **C · Estandarte**, no **jogo
atual** ou na **1ª proposta** (o histórico, abaixo); um formulário troca a classe. Cada botão encerra o cenário anterior e
sobe outro do zero, num processo com saves temporários (o save do jogo não é tocado); na página, "Começar o teste"; no
canto de baixo, "repetir" e "painel" (essa faixa só existe na demonstração). O servidor de teste (`cenarios_teste.py`,
`PROTOTIPO=<direção>`) serve `telas/celebracoes.js` e `telas/achado.js` montados em `prototipo-v2/<direção>/`.
Movimento reduzido: no Chrome/Edge, F12 → ⋮ → More tools → Rendering → "Emulate CSS media feature
prefers-reduced-motion" → reduce, e "repetir" (ou "Mostrar animações" desligado no Windows, para o sistema todo).

## Segunda rodada (24/10/2026): três direções

O Jean achou a primeira proposta contida demais: gostava dos feixes girando atrás, o problema era o acabamento de
vetor. Pedido: três direções completas, mais carregadas, em pixel art, com o modal livre para ser refeito.

### Referências vistas (imagens reais; nada copiado)

- **Vampire Survivors**, o baú (miniaturas de vídeos de jogo): feixes largos saindo em leque do baú, moedas voando e o
  prêmio subindo pelo feixe. Ensina que a luz pode nascer de onde o prêmio vem, que o excesso funciona se a moldura
  segura o centro, e que o ritmo cresce em degraus (quanto mais prêmios, mais fanfarra), sempre pulável.
- **Sea of Stars**, a subida de nível (captura da IGN): tela inteira escura, o título em cima, medalhões com halo em
  pixel e uma barra de números embaixo com os "+N" coloridos. Ensina a hierarquia título → símbolos → números, e que o
  fundo escuro deixa o brilho ser lido sem ofuscar o texto.
- **Diablo III**, o lendário (imagem do Diablo Wiki): uma coluna de luz da cor da raridade. Ensina que a raridade se
  lê de longe pela cor e pela forma (a coluna), antes do texto.
- **Pokémon (Gold/Silver/Crystal)**, a evolução (miniatura): raios de luz em volta do sprite, o momento cerimonial
  que segura a atenção e revela. Ensina o centro como altar e a luz como moldura.
- **Octopath Traveler**, o resultado da batalha: a cena continua visível e a lista dos ganhos fica de lado, em
  tipografia contida. Ensina a não esconder o mundo e a ler os números numa coluna.
- **Blasphemous**, o item recebido: uma faixa escura atravessando a tela com o nome em fonte gótica. Ensina a
  apresentação de "título de ato", sóbria e solene, que combina com o tom do The Unquiet.
- A busca no Game UI Database pedia verificação anti-robô; ficou de fora.

### As três direções

Todas usam o mesmo motor de efeitos (`v2/fx.js`): um palco de baixa resolução (texels de 3 px, ampliado sem
suavização, 15 quadros por segundo), só cores da paleta do jogo, degradê só por pontilhado ordenado e faixas de cor, e
partículas desenhadas à mão como grades de texto (cruz, estrela, brilho, lasca, caco, brasa). O comum de cada uma
(`v2/festas.js`): os gestos, a janela do achado e os textos (os ganhos com os ícones da HUD, o ponto de talento com o
atalho, a raridade num selo próprio e fora da linha do tipo). `auxiliares/montar_v2.py` junta tudo com os arquivos de
produção em `prototipo-v2/<direção>/`.

- **A · Relicário (cerimonial).** O ganho posto num altar: uma medalha em pixel com o número (ou o item, ampliado 2×)
  no centro de um sol de raios que gira devagar enquanto a janela está aberta (raios largos e finos em sentidos
  contrários, os que descem mais curtos), e embaixo uma placa com a moldura da HUD. Entrada: o clarão na medalha, o
  sol se abrindo, as faíscas; depois só o giro e um cintilar. Raridade = tamanho do sol: comum, só o halo; mágico, oito
  raios frios; raro, doze de ouro; lendário, dois sóis de brasa, o clarão e as brasas subindo.
- **B · Estouro (explosivo).** O ganho chega como um golpe: clarão de dois quadros, a tela treme, anéis de choque
  correm, linhas de velocidade e estilhaços voam e caem; o número bate (carimbo em quatro quadros) no meio de uma
  estrela de pontas, com uma fita vermelha atravessada. Ganhos em fichas grossas que estalam uma a uma. Depois, a
  estrela respira e solta brasas. Raridade = força do golpe: comum, poeira; mágico, anel e faíscas; raro, uma coluna
  de luz cai no item e quebra; lendário, a coluna larga, a tela pisca e treme, dois anéis e a chuva de cacos.
- **C · Estandarte (apresentação de palco).** Uma faixa de lado a lado da tela, como o título de um ato: abre de um
  corte de luz, barras de cinema escurecem o alto e o pé, e holofotes em pixel nascem atrás da faixa e varrem para
  cima e para baixo, cruzando-se; a luz vaza pelos fios. Na faixa: quem (o retrato do herói em 160 px, ou o item no
  pedestal sob a coluna de luz), o quê (o nível; o nome e a raridade) e o quanto (os ganhos; os números e a
  comparação). Raridade = luz do palco: comum, a faixa sem luz; mágico, uma coluna fria; raro, a coluna e dois
  holofotes; lendário, a coluna de brasa, cinco holofotes, as barras, o corte e as brasas.

### O que vale nas três

- **Ler sem esperar:** o nível, os ganhos, o item, a raridade e a comparação estão na tela desde o primeiro quadro; o
  efeito é em volta. Na B, só o desenho do item raro e lendário espera a coluna bater (160 ms).
- **Gestos:** o Continuar, o Enter, o Espaço e o Esc fecham a festa a qualquer momento; um clique fora durante a
  entrada a completa; não contam o toque que começou antes da festa, o 2º clique de um clique duplo nem a tecla
  segurada; o gesto não atravessa para a festa seguinte nem seleciona texto. No achado, um clique ou tecla durante a
  entrada a encurta e não escolhe nada (os botões ainda não estão lá).
- **Os botões do achado** chegam quando a entrada termina: medidos na página (1920×945, do cartão aos botões),
  comum / mágico / raro / lendário: A 0,22 / 0,34 / 0,49 / 0,64 s; B 0,21 / 0,28 / 0,43 / 0,57 s; C 0,23 / 0,32 /
  0,44 / 0,58 s; o jogo atual 0,55 / 0,55 / 2,3 / 2,7 s. Um clique logo que o cartão surge leva os botões a ~0,09 s
  nas três (medido na página: o fotógrafo clica tarde demais para mostrar isso).
- **Movimento reduzido:** a mesma composição parada (os raios, a estrela, os holofotes num quadro só), sem clarão,
  tremor, partículas nem entrada.
- **Telas baixas (1280×720):** A e B compactam a medalha, a estrela e as caixas; a janela rola se ainda faltar espaço.

### Cenários

`auxiliares/cenarios_teste.py`. **Casos reais** (pelos caminhos do jogo, sem mudar regras): um nível (dois lobos),
dois níveis seguidos (a Ilse e dois afogados), as quatro raridades (`gerar_equip` com a raridade pedida), o nível 4
da encruzilhada, o Sigilo (`receber_sigilo`) e a especialização (`especializar`). **Simulação** (identificada assim
no jogo e no painel): `limites`, uma festa de nível 12 com seis ganhos de dois dígitos e duas habilidades de nome e
texto longos, e um lendário de nome longo; não acontece nas regras, só testa a tela.

### Capturas

`capturas-v2/`: `folha-v2.png` (cada momento: o jogo atual, A, B e C), `folha-v2-ritmo.png` (o nível e o lendário em
seis instantes), `folha-v2-apertados.png` (1280×720 e movimento reduzido); por direção, `1920/` (vídeos `.webm` do
ciclo e os quadros), `1280/`, `reduzido/` e `rapido/` (o clique rápido). Refazer: `auxiliares/fotografar.mjs` com
`PROTOTIPO=<direção>` e `PULAR_TEXTO=1` (o texto de abertura adiantado por uma tecla), depois `auxiliares/folhas_v2.py`.

### Limitações vistas

- **Som:** é o atual (subir, achado, achado raro, fanfarra), tocado no primeiro quadro (na B, no impacto da coluna).
  Não foi ouvido nesta máquina; o sincronismo foi conferido pelos tempos do código, não pelo ouvido.
- **A entrada nas fotos:** o fotógrafo pega a janela 0,1 a 0,2 s depois de ela abrir; o clarão e os primeiros quadros
  só aparecem nos vídeos e na demonstração.
- **A:** o sol cobre a tela inteira, a HUD inclusive (de propósito); o comum tem só um halo discreto e pode parecer
  pouco ao lado do resto.
- **B:** o tremor move a tela inteira por ~0,4 s no nível e no lendário (no raro, menos); pode cansar se os níveis
  vierem em sequência. A fita vermelha e as fichas grossas puxam para um tom mais de fliperama que o resto do jogo.
- **C:** os holofotes que descem passam sobre o texto da página (escurecido); em 1920 a faixa fica larga e vazia nas
  laterais; o retrato é o busto do herói ampliado 2× (fator inteiro).
- **As formas grandes** (o sol, a estrela, os holofotes) são geradas por regra em baixa resolução; as partículas são
  desenhadas à mão. Se uma direção for aprovada, a medalha ou a estrela podem virar peças desenhadas no Aseprite.
- **Dois níveis seguidos:** cada nível tem a sua festa inteira; a segunda não é mais curta.
- **Fora deste lote:** a vitória, os contratos, o mestre caçador e as faixas continuam como no jogo.
- **Desempenho:** ~5 ms por quadro no pior caso (A, no navegador de teste, sem placa de vídeo); não medido numa
  máquina fraca.

## O levantamento (o que existe hoje; vale para as duas rodadas)

- **Como o jogador avança:** o XP vem das lutas (o quadro do espólio, `Jogo.abrir_espolio`/`ganhar_xp`), dos contratos
  e das missões; cada nível dá vida, recurso e atributos pela classe, um ponto de talento e, em alguns níveis, uma
  habilidade nova e o aviso da especialização. O motor manda o evento `celebracao` (`tipo: nivel`) com os ganhos
  prontos; vários níveis de uma vez viram festas seguidas.
- **A festa de nível** (`#celebracao`, compartilhada com o **Sigilo** e a **especialização**): raios cônicos em CSS,
  um anel borrado, partículas em `div` soltas, os ganhos com os sprites 16 antigos contando de zero, e as teclas
  ignoradas por 600 ms. O Continuar fechava; o clique duplo já fechava uma festa só.
- **As fagulhas soltas** (`particulas`): a mesma função na vitória, nos contratos, no Sigilo e na especialização.
- **O achado** (`telas/achado.js`): a raridade só na cor do nome e na linha do tipo ("Peito · Lendário"); raro e
  lendário esperam o feixe inteiro (1 a 1,4 s) e mais 0,55 a 0,9 s com o cartão sozinho antes da comparação e dos
  botões. Nada adianta isso.
- **O quadro do espólio:** já segue a regra do gesto (`Gesto`) e não muda neste lote.
- **Movimento reduzido:** quase não tratado (os raios e as partículas continuavam).


# Primeira rodada (23/10/2026): o Brilho (histórico)

Recusada como contida demais (24/10/2026); fica como referência no painel ("1ª proposta"), em `prototipo/` e em
`capturas/`.

## A proposta da primeira rodada

Uma direção só: **o efeito em pixel da HUD (o Brilho) e o ganho legível na primeira olhada**.

- **O Brilho** (`prototipo/brilho.js`): um canvas de baixa resolução (texel de 3 px, 15 quadros por segundo), com o
  pontilhado ordenado do `Sprites` e paletas agrupadas (ouro, mágico, raro, lendário, arcano, Sigilo). Uma aura em
  volta do que importa (o número do nível, a arte do item, o "Sigilo n/3") e um estouro curto; nada de disco ou coluna
  atrás de texto. Dura 0,9 s e apaga em degraus.
- **A festa de nível:** "Nível N" com o número carimbado; os ganhos em placas com os ícones da HUD (os vitais em 20, os
  atributos em 24), já com o valor final (sem contar de zero); o ponto de talento com o ícone dos Talentos e o atalho
  (T); a habilidade nova; a cascata leva ~0,6 s.
- **Os gestos** (sem bloqueio de clique e sem espera para clicar de novo): o Continuar, o Enter, o Espaço e o Esc
  fecham a qualquer momento; um clique fora durante a revelação só a completa; como no espólio, não contam o toque que
  começou antes de a festa abrir, o 2º clique de um clique duplo nem a tecla segurada, e o gesto que fecha não
  atravessa para a festa seguinte. A seleção de texto que o clique duplo deixava no botão da festa seguinte (no jogo
  também) sai.
- **A raridade no achado:** um selo com o nome da raridade abaixo de "Você encontrou" (a linha do tipo fica só com o
  espaço, sem repetir); intensidade proporcional: comum, só o cartão e as faíscas; mágico, a aura leve; raro, a aura e
  o feixe; lendário, a aura maior e o feixe. O cartão aparece quando o feixe bate (0,43 s), e um clique ou tecla
  adianta tudo (o gesto não escolhe: os botões ainda não estão lá).
- **O Sigilo e a especialização** usam o mesmo Brilho (paletas Sigilo e arcano); as fagulhas da vitória e dos
  contratos viram o estouro em pixel.
- **Movimento reduzido:** sem cascata, sem estouro, sem feixe; a aura fica parada, as informações e o selo iguais.

## Os números (do `registro.json` de cada pasta, 1920×945)

| Do anterior fechado até os botões | atual | proposta | proposta, movimento reduzido |
|---|---|---|---|
| comum, mágico | ~0,37 s | ~0,36 s | ~0,36 s |
| raro | 2,2 s | 1,2 s | 0,37 s |
| lendário | 2,8 s | 1,2 s | 0,37 s |
| raro/lendário com um clique logo que surgem (`rapido-*`) | 0,5 a 0,9 s | ~0,14 s | — |

A festa de nível chega no mesmo tempo nos dois (o motor manda); o que muda é que ela pode ser fechada na hora.

## As capturas

- `capturas/folha-estados.png`: cada momento, atual × proposta, em 1× (o meio da tela, 900 ms depois de aparecer).
- `capturas/folha-ritmo.png`: os cinco instantes (60, 250, 500, 900, 1600 ms), atual e proposta.
- `capturas/folha-apertados.png`: 1280×720 e movimento reduzido, atual × proposta.
- `capturas/<atual|proposta>[-1280|-reduzido]/`: os vídeos (`.webm`, o ritmo), o registro e os quadros de 250 e 900 ms
  (1920) ou de 900 ms (os outros); os demais instantes foram tirados depois de montar as folhas (refazer: rodar o
  fotógrafo e `auxiliares/folhas.py`).
- `capturas/rapido-<atual|proposta>/`: o clique rápido, em vídeo e registro.

## Os cenários de teste

`auxiliares/cenarios_teste.py` (**cenários de teste**, fora do jogo e de `tests/`): o herói a 25 de 30 XP no Vau e os
caminhos reais do motor. `nivel`: dois lobos (nível 2, Investida). `dois_niveis`: a Ilse (nível 3) e dois afogados
(do 1 ao 3, a festa duas vezes, o clique duplo na primeira, o Enter na segunda). `raridades`: quatro achados seguidos,
um de cada raridade, pelo `gerar_equip` com a raridade pedida. Nenhuma chance, recompensa ou progressão muda.

```
PLAYWRIGHT_MODULO=<file:// do index.mjs> PROTOTIPO=1 node auxiliares/fotografar.mjs <raiz> capturas/proposta
#   MOVIMENTO=reduzido, JANELA=1280x720; sem PROTOTIPO, o jogo atual; "rapido,rapido-nivel" para o clique rápido
python auxiliares/folhas.py capturas
```

## Limitações vistas no uso

- **O Sigilo e a especialização** não têm cenário aqui: usam o mesmo código e o mesmo Brilho, mas não foram
  fotografados. Nem as fagulhas da vitória e dos contratos.
- **O som** é o de antes (subir, fanfarra, o da raridade): nada foi feito para ele.
- **A aura do achado** é pequena a 1920 (o cartão tem 300 px); a diferença entre raro e lendário está mais no feixe e
  na cor do que no tamanho.
- **Movimento reduzido:** a aura parada ainda tem pontos em volta da arte (estáticos); se preferir nada, é tirar.
- **A especialização no nível 5** e uma habilidade de nome longo na festa não apareceram nos cenários; o nome longo
  de item ("Lamento do Corvo (Besta Leve Enferrujada)") quebra em três linhas no cartão, como no atual.
- Os tempos da tabela incluem as esperas do fotógrafo entre um gesto e outro (iguais nos dois lados).
