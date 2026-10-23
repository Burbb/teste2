# A Árvore Desperta e o golem de pedra (22/10/2026, propostas; nada no jogo)

**Pedido do Jean:** o próximo par do plano 23, duas propostas realmente diferentes de cada, só no protótipo, depois de
ler as descrições, os traços, as habilidades e os usos reais. Produção na 1.188.0; nenhum candidato autorizado para
integração. A Árvore Anciã e o Golem Primordial ficam para uma rodada própria: nenhum candidato daqui é atribuído a eles.

## O que vem do jogo (conferido no código)

**Árvore Desperta** (`ent_jovem`, `rpg/dados.py`; o nome desde a 1.181.0): "Árvores que acordaram com raiva. Madeira
verde queima mal — mas queima." Traços `planta` ("queima com facilidade") e `blindado` ("resiste a dano físico"); o Golpe
Esmagador (avisa antes) e o Regenerar; 40 de vida, agilidade 1, sozinha, a partir do nível 3; vive na floresta (com o
lobo, a aranha, o bandido, o javali e o caído). Hoje no sprite `planta`, que também é o da Árvore Anciã (guardiã, pelos
traços).

**Golem de pedra** (`golem`): "Pedra e runas. Lento, mas cada golpe é uma avalanche. A magia racha a pedra." Traços
`construto` ("imune a veneno e sangramento, sensível ao arcano") e `blindado`; o Golpe Esmagador; 60 de vida, agilidade
0, sozinho, a partir do nível 4; vive nas ruínas. O evento `golem_adormecido` (`eventos/biomas.py`): "um golem de pedra
coberto de musgo bloqueia o corredor, imóvel. No peito, uma gema brilha fracamente"; arrancada a gema, "o golem desmorona
em pedregulhos"; acordado, "os olhos do golem se acendem". Hoje no sprite `construto`, que também é o do Golem Primordial.

**Usos de uma futura integração:** pela família, os dois na carta da luta (32), no Bestiário (48), no cartaz e no
rastreador dos contratos e na faixa do mestre caçador, com os afixos (a árvore corrompida perto da Fenda ficaria no
retrato da família). **Dois usos que herdariam o retrato pela família e precisam de decisão na integração:**
- o **Espantalho Possuído** (`eventos/biomas.py`, evento `espantalho`): é criado da família `ent_jovem`, com outro nome e
  descrição ("os números da árvore desperta, mas é o espantalho");
- o **Mímico** (`eventos/comuns.py`): é criado da família `golem`, com o nome, os traços (`construto`) e as habilidades
  (agarrão, mordida) de um baú com boca.
Hoje os dois aparecem com o sprite da família pelos traços (`planta` e `construto`). Nada foi decidido aqui.

**O que continua nos sprites compartilhados:** o `planta` com a Árvore Anciã e o `construto` com o Golem Primordial
(guardiões, pelos traços), até a rodada própria deles.

## A interpretação (minha)

A Árvore como uma árvore inteira que é a cabeça (o tronco é o rosto), com a casca e os nós fazendo a expressão; o Golem
como pedra de verdade, com blocos ou rochedos e juntas, sem as bordas acesas de uma armadura e sem um rosto humano. Os
olhos são ocos escuros (sem brilho), e a textura fica em poucos sulcos e lascas.

## As propostas

**Árvore Desperta** (camadas casca, folhas, rosto; a paleta da casca em cinco valores, as folhas em três).
- **A1, os galhos nus** (`arvore-a1`): de frente, o tronco é a cabeça; três galhos secos sobem em forquilhas, com poucas
  folhas na ponta; as sobrancelhas de casca acesas sobre os olhos de nó, inclinados para dentro (o olhar bravo); a fenda
  larga da boca com duas lascas; as raízes se abrindo embaixo.
- **A2, a copa pesada** (`arvore-a2`): a copa verde redonda caindo sobre os olhos como uma testa, a sombra embaixo dela,
  os olhos de nó inclinados, o toco de galho quebrado como nariz (para a esquerda), a boca de nó com as lascas, o tronco
  largo.
- **Na bancada:** as primeiras tinham as lascas da boca em madeira clara, e elas liam como os olhos (os olhos de verdade
  sumiam); com as lascas no meio-tom e as sobrancelhas acesas, o rosto ficou no lugar.

**Golem de pedra** (camadas pedra, juntas e, no G2, musgo; a pedra em cinco valores).
- **G1, a cantaria** (`golem-g1`): blocos cortados; a cabeça é um bloco só, com a laje da testa sobre as órbitas
  quadradas, uma rachadura e o talho da boca; a junta escura do pescoço; as ombreiras e o peito em blocos brutos, lascados
  nas bordas, e uma rachadura descendo pelo peito.
- **G2, o rochedo** (`golem-g2`): pedras brutas e arredondadas; a cabeça pequena e baixa entre dois ombros enormes, a
  testa saliente sobre as órbitas, o musgo num ombro, o punho de pedra embaixo à esquerda.
- **Na bancada:** o primeiro G1, com um vão escuro no meio do peito e ombreiras de tijolo, lia como a fachada de uma casa
  (o vão, uma porta); depois, uma runa em V no peito virou um segundo rosto; a rachadura diagonal resolveu. O primeiro G2
  era um monte de pedras sem cabeça; a testa saliente e as órbitas fundas a fizeram aparecer.

## A minha leitura (quem escolhe é o Jean)

- **Árvore: prefiro a A2.** A copa lê como árvore na hora, a 32, e a silhueta não se confunde com nenhum retrato
  aprovado; o nariz de galho dá personalidade. **Limitação no tamanho real:** o rosto fica pequeno sob a copa, e o
  conjunto pode ficar simpático demais (um pé de brócolis com cara).
  - A1: o tronco com o rosto é o mais expressivo; **limitação:** a 32 os galhos têm 1 px e o tronco pode ler como uma
    máscara de madeira.
- **Golem: prefiro o G2.** É o mais mineral e o mais pesado, e não lê como armadura nem como humano cinza.
  **Limitação:** a cabeça é pequena e o rosto quase some a 32; o conjunto pode ler como um monte de pedras.
  - G1: os blocos e as juntas se entendem; **limitação:** é escuro na carta, e a cabeça em bloco com a laje pode lembrar
    um robô.

## Processo

- As grades à mão em `auxiliares/grades.py`, rascunhadas e julgadas a 32 (na caixa) e a 48 antes da fonte; sem guia
  (nenhuma referência externa).
- As fontes pelo Aseprite em lote (`python auxiliares/exportar.py --montar`, o `montar_camadas.lua` com o `pintar.lua`;
  o conector continua sem editor e a janela aberta não foi tocada): 0 diferentes e 0 fora da tela na releitura de cada
  camada; a exportação do Aseprite (o composto) igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros do 16.
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, os modos atual, a e b, trocados só na página pelo nome): a luta da
  árvore (com o lobo e o javali), a do golem (com o esqueleto e o carniçal) e o Bestiário; sem erro no console.
- As folhas (`python auxiliares/prancha.py`): `arvore.png` e `golem.png`, com o jogo de hoje × A × B na carta (real e 2×)
  e no Bestiário (48), a fileira com os aprovados e a 12×.
