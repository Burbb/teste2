# A Árvore Anciã e o Golem Primordial (23/10/2026, propostas; nada no jogo)

**Pedido do Jean:** começar os chefes por esses dois, duas propostas de cada, só no protótipo, depois de conferir as
descrições, as habilidades, os eventos e os usos reais. Produção na 1.189.0; nenhum candidato autorizado. A T1 da Árvore
Desperta é a referência de linguagem e material da Anciã; o G2 original, a de peso e material do Primordial. O
antagonista, os outros chefes, o servo, o Espantalho, o Mímico e o mapa ficam para as próximas rodadas.

## O que vem do jogo (conferido no código)

**Árvore Anciã** (guardiã `ent_anciao` da floresta, `GUARDIOES` em `rpg/dados.py`; o nome desde a 1.181.0, antes "Ent
Ancião"): 160 de vida, ataque 12, defesa 8, agilidade 1, poder 4; traços `planta` e `blindado`; o Golpe Esmagador, o
Regenerar, o Agarrão e a Varredura; resiste pouco ao fogo (×1,6). A entrada: "A floresta inteira parece se mover. Uma
árvore milenar abre olhos de seiva âmbar e fala com voz de terremoto." A fase 2, a 40% da vida: "A casca da árvore racha e
uma luz verde e furiosa escapa das fendas!" (o ataque sobe, a defesa cai, ganha a Investida). O rumor da floresta: "As
árvores aqui têm rostos. Todos virados na mesma direção." (`eventos/comuns.py`).

**Golem Primordial** (guardião `golem_primordial` das ruínas): 180 de vida, ataque 13, defesa 11, agilidade 0; traços
`construto` e `blindado`; o Golpe Esmagador, a Investida e a Varredura. A entrada: "Runas se acendem no chão. O que você
pensava ser uma parede se levanta: um golem do tamanho de uma casa." A fase 2, a 50%: "As placas de pedra caem e o núcleo
pulsante do golem fica exposto!" (a defesa cai, o ataque sobe). O rumor: "O chão treme em intervalos regulares. Passos."

**Usos reais:** um guardião só aparece na **carta da luta** (32 px), pelo id dele (`RETRATO_GUARDIAO`, como o Rei Troll e
a Rainha Aracnídea); a família é `guardiao`, que não entra no Bestiário, no mural nem no rastreador. Por isso os
derivados são o 16 e o 32, com os @2x (como os da Rainha). Hoje os dois estão nos sprites dos traços: o `planta` e o
`construto`, os mesmos de antes da Árvore Desperta e do golem comuns terem os deles.

## A interpretação (minha)

A Anciã com a mesma casca e o mesmo âmbar apagado da T1, mas outra estrutura: o comando vem do rosto inteiro de frente
(a autoridade) ou da árvore inteira (a escala), não de musgo ou de mais galhos. O Primordial com a pedra bruta do G2, mais
velha e mais escura, e a cabeça grande (a carta precisa reconhecer uma cabeça), sem runas, rachaduras nem brilho. As
fases 2 (a luz verde nas fendas, o núcleo pulsante) não entram no retrato.

## As propostas

**Árvore Anciã** (camadas casca, rosto; a paleta da T1, um passo mais funda, com a seiva âmbar dos olhos do texto).
- **AA1, o rosto-rei** (`anciaa-aa1`): de frente e de perto, o tronco na largura toda do quadro; a copa de galhos grossos
  sobe como uma coroa; as sobrancelhas pesadas atravessam o rosto; os olhos de seiva âmbar, fundos e afastados; o nariz
  aceso; a boca longa e fechada; a barba de raízes caindo em mechas até a borda.
- **AA2, a árvore imensa** (`anciaa-aa2`): a árvore inteira; a copa larga de galhos secos ocupa o alto, o tronco estreita e
  volta a abrir, e o rosto fica mais baixo no tronco (os olhos âmbar, o nariz, a boca fechada), com as raízes embaixo. A
  escala vem do rosto pequeno diante da árvore.
- **Na bancada:** a primeira AA2, a cabeça curvada de perfil, não lia como árvore (parecia um bicho).

**Golem Primordial** (camadas pedra, juntas e, no GP2, musgo; a pedra do G2, mais escura).
- **GP1, a parede que se levanta** (`primordial-gp1`): a cabeça grande de pedra no meio de uma parede (uma laje por cima,
  três pedras de cada lado, o bloco do peito embaixo), com o vão escuro em volta da cabeça; a testa, as órbitas fundas, o
  nariz e o talho da boca.
- **GP2, o ídolo** (`primordial-gp2`): a cabeça grande esculpida num bloco, a laje mais larga que ela por cima (como um
  dólmen), a sombra sob a laje, a testa, as órbitas, o nariz e a boca, sobre o corpo de rochedos do G2.
- **Na bancada:** o primeiro GP1 (blocos de cantaria) virou uma torre de tijolos; o seguinte, com os ombros subindo acima
  da cabeça, leu como dois dedos; o primeiro GP2 tinha duas pedras em pé que viravam orelhas; a parede com juntas em
  xadrez ficou ruidosa a 32 e foi simplificada em pedras grandes.

## A minha leitura (quem escolhe é o Jean)

- **Árvore Anciã: prefiro a AA1.** O rosto inteiro de frente dá a autoridade e a consciência (o olhar âmbar direto), e a
  coroa de galhos e a barba de raízes a separam da Árvore Desperta pela estrutura. **Limitação no tamanho real:** a casca e
  o âmbar são os da T1, e a 32, ao lado da comum, a diferença é a largura, a coroa e a barba, não a cor; pode ler como uma
  máscara de madeira.
  - AA2: a escala de árvore imensa; **limitação:** a 32 o rosto fica pequeno (os olhos são dois pontos).
- **Golem Primordial: prefiro o GP2.** A cabeça de ídolo com a laje é a mais reconhecível e a mais ancestral, e o corpo de
  rochedos o liga ao golem comum. **Limitação:** a laje pode ler como um chapéu, e o rosto esculpido reto pode lembrar uma
  estátua mais do que um ser.
  - GP1: o texto do jogo (a parede que se levanta); **limitação:** a 32 lê como um rosto numa moldura ou numa porta de
    pedra, e as juntas pesam.

## Processo

- As grades à mão em `auxiliares/grades.py`, julgadas a 32 (na caixa) ao lado do comum e dos chefes aprovados; sem guia.
- As fontes pelo Aseprite em lote (`python auxiliares/exportar.py --montar`; o conector continua sem editor e a janela
  aberta não foi tocada): 0 diferentes e 0 fora da tela na releitura de cada camada; a exportação do Aseprite (o composto)
  igual à grade, o @2x exato, o 32 em blocos inteiros do 16 (só o 32: o uso real do guardião).
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`, os modos atual, a e b, trocados só na página pelo nome): a luta de
  cada guardião (`CHEFE=`, com o nome e a chave dele) com o comum correspondente e outro da região; sem erro no console.
- As folhas (`python auxiliares/prancha.py`): `anciaa.png` e `primordial.png`, com o jogo de hoje × 1 × 2 na luta (o grupo
  em tamanho real e a carta do guardião a 2×), a fileira com o comum, os chefes aprovados e um comum da região (real e 3×)
  e a 12×.
