# O Caído e o Xamã Caído (22/10/2026, propostas; nada no jogo)

**Pedido de Jean:** duas propostas por criatura, só no protótipo; antes, conferir o que "Caído" é no nosso mundo e dar
aos dois uma identidade comum, com o papel do xamã visível no retrato.

## O que "Caído" é no jogo

- **Diabretes, não humanos corrompidos.** O traço é `demonio` ("cria do Inferno; o sagrado o queima, o fogo pouco o
  fere"), e o Bestiário diz: "Diabretes covardes que atacam em bando, rindo. Mate o xamã primeiro, ou eles voltam."
  São também a primeira das criaturas da Fenda (aparecem fora do bioma em lugares de perigo 3+).
- **Caído** (`caido`, família): fraco (13 de vida), Golpe Sujo; em bando de 2 a 4, na floresta, na planície e nas
  ruínas; o maior bando real é de caídos à noite com a comitiva, mais o xamã de escolta.
- **Xamã Caído** (`xama_caido`, família própria): "Pequeno feiticeiro dos caídos. Cospe fogo e ergue os irmãos mortos
  do chão."; demônio e conjurador; Bola de Fogo e Reviver (duas vezes). Vem como escolta dos caídos (35% até o nível
  4, 60% depois) e só levanta os caídos (o `revive` dele): não invoca outra entidade.
- **Hoje** os dois saem do traço `demonio`, o mesmo do Cão infernal (fora deste par).
- **Alcance, se aprovado:** cada um pela sua família (`RETRATO_FAMILIA`, o papel `CRIATURA`): a carta (32), o Bestiário
  (48), o cartaz do mural e o rastreador, a faixa do mestre caçador, os afixos; o caído revivido é o mesmo caído. O Cão
  infernal e os outros demônios continuam no `demonio`.

## A identidade comum e as propostas (16×16; o 32 e o 48 são o 16 ×2 e ×3)

A pele vermelha, os chifres curtos, as orelhas pontudas para fora, os olhos amarelos, o riso. O xamã é da mesma
cabeça e se distingue pelo que veste e pelo fogo (a Bola de Fogo), não pela cor do olho.

- **CA, o que ri** (`caido-ca`; camadas pele, chifres, olhos, boca): de frente, a cabeça redonda, as orelhas abertas,
  os olhos apertados de riso, a boca aberta cheia de dentes, os ombros curvados.
- **CB, o que se esgueira** (`caido-cb`): em três quartos para a esquerda, mais escuro, os chifres longos para trás, o
  olhar de lado, o sorriso torto com uma presa.
- **XA, o do crânio** (`xama-caido-xa`; camadas pele, couro, chifres, crânio, olhos, boca, fogo): a cabeça do CA com o
  crânio de uma fera por cima (as órbitas, o focinho, os chifres dele), o fogo na boca aberta e a capa de couro com
  contas de osso.
- **XB, o do capuz** (`xama-caido-xb`; camadas pele, couro, chifres, olhos, boca, fogo): a cabeça do CB num capuz de
  couro com o chifre furando, a gola de contas de osso e a chama alta na mão erguida.

## A minha leitura (quem escolhe é o Jean)

- **Caído: prefiro o CA.** Lê de longe como diabrete que ri, e o bando de três CA na carta fica claro. **Limitação no
  tamanho real:** é o mais parecido com o desenho genérico de hoje (um rosto vermelho de chifres), só que construído;
  o ganho está no riso, nas orelhas e nos ombros, não na ideia.
- **Xamã: prefiro o XA.** O crânio claro é a maior forma do retrato e separa o xamã do bando na hora, e o fogo na boca é
  o "cospe fogo" da descrição. **Limitação:** a 32 o crânio e os chifres dele tomam o alto da cabeça e o rosto do
  diabrete fica menor; o fogo na boca pode ser lido como "boca brilhando" por quem não lê a descrição.
- **O par B** (CB e XB) é mais sombrio e mais "de feiticeiro", mas o escuro perde contraste a 32: o rosto de lado do CB
  fica pouco legível, e o XB depende da chama no canto.

## Histórico da bancada

- XB: a primeira chama era um ponto alaranjado no canto (o "ponto brilhante" que o Jean pediu para evitar); virou uma
  chama alta saindo da mão, de três linhas.

## Processo

- As grades à mão em `auxiliares/grades.py`. **O conector do Aseprite estava indisponível nesta sessão** (o mesmo
  registro do `harpia_grifo/`): as fontes em camadas saíram do Aseprite em lote (`python auxiliares/exportar.py
  --montar`, `montar_camadas.lua` com o `pintar.lua`; releitura 0 diferente); o composto exportado igual à grade, o @2x
  exato, o 32 e o 48 em blocos inteiros. Sem guias.
- As fotos (`auxiliares/fotografar.mjs`, a 1920×945): o bando (três caídos com o xamã, o Cultista e o Troll) e o
  Bestiário, nos modos atual, A e B, trocados só na página pelo nome; sem erro no console.
- As folhas `caido.png` e `xama_caido.png` (`python auxiliares/prancha.py`); na fileira do xamã, os dois caídos
  propostos ao lado.

## A escolha e o jogo (1.182.0)

- **O CA, o que ri, aprovado pelo Jean sem retoque**, integrado pela família (`RETRATO_FAMILIA`: `caido`; o papel
  `CRIATURA`): os caídos comuns, os afixos, os do bando e os que o xamã ergue (o Reviver levanta o mesmo caído morto,
  com o mesmo retrato). O Xamã Caído (família própria) e o Cão infernal continuam no sprite de demônio.
- A fonte em `ferramentas/arte/aseprite/retrato-caido/` (a cópia da `fontes/caido-ca/`); os seis PNGs idênticos byte a
  byte aos de `proposta/`. Conferido com os arquivos de produção (`auxiliares/fotografar_jogo.mjs`, `capturas-1182/`,
  a 1920×945): o bando na carta, o Bestiário, o cartaz do mural e o rastreador; nenhum pedido a `ferramentas/`; sem erro
  no console.
- **O CB não foi escolhido; o XA e o XB ficam como histórico** (o XA: o crânio claro lia como um segundo rosto acima do
  verdadeiro, e o crânio, os olhos e a chama disputavam a atenção). A rodada nova do xamã está em `../rodada_23_10/`.
