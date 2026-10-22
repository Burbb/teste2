# A segunda rodada dos quatro pares (22/10/2026; propostas, nada no jogo)

**Pedido de Jean**, depois da avaliação do lote `../quatro_pares/` (o sapo A e a sanguessuga A foram para o jogo na
1.171.0): três capuzes para o cultista a partir do A; três rostos para a bruxa a partir da A; o carniçal A com a boca e
os dentes refeitos; o espectro A desenvolvido como a entidade de olho único; o javali A com as presas grandes e grossas;
três reconstruções do rato a partir da direção A. As propostas do primeiro lote ficam como estão.

## Processo

- As grades à mão em `auxiliares/grades.py` (cada uma com a paleta do primeiro lote e poucos tons a mais), julgadas na
  caixa da carta ao lado dos retratos integrados; as fontes no Aseprite pelo conector (`pintar.lua`; a releitura das
  camadas contra a grade, 0 diferentes; o composto do editor igual à soma das camadas) em `fontes/<id>/`; a exportação
  conferida (`auxiliares/exportar.py`: o PNG exportado igual à grade, o @2x exato, o 32 e o 48 em blocos inteiros).
- As fotos a 1920×945 (`auxiliares/fotografar.mjs`): uma luta e o Bestiário com as seis criaturas, nos modos atual (o
  jogo), base (a escolhida no primeiro lote) e v1, v2, v3 (as variações; as criaturas com uma proposta só a repetem),
  os mesmos dados; as propostas trocadas só na página (protótipo). Sem erro nem aviso no console.
- As folhas por criatura (`python auxiliares/prancha.py`): `cultista.png`, `bruxa.png`, `carnical.png`, `espectro.png`,
  `javali.png`, `rato.png`.
- **A referência do rato:** fotos de ratos-marrons (*Rattus norvegicus*) no Wikimedia Commons, vistas no navegador só
  para estudar a anatomia (a cabeça em cunha até o nariz, o olho pequeno a um terço do focinho, a orelha redonda e
  recuada, a cabeça emendada no pescoço grosso, os incisivos alaranjados); nenhuma imagem foi copiada nem guardada.

## Cultista (`cultista.png`): três capuzes

- **c1, o capuz pontudo** (`cultista-c1`): o bico alto caindo para trás, a abertura estreita, o rosto quase todo na
  sombra (só o nariz e a boca), a marca na testa e no peito.
- **c2, o capuz largo** (`cultista-c2`): a abertura emoldurando o rosto, os olhos escuros sob a marca vertical na
  testa. (Na bancada, a marca horizontal sobre os olhos virava óculos.)
- **c3, o capuz que avança** (`cultista-c3`): a aba projetada cobre os olhos numa faixa de sombra, e a marca fica
  bordada na testa do capuz.
- **A minha preferência: o c1.** Forte: a silhueta pontuda é a mais misteriosa e diferente de todos os capuzes do jogo,
  e o rosto sumido na sombra faz a ameaça. Limite: o rosto quase não existe; quem lê o cultista é o capuz e a marca. O
  c3 é o mais ameaçador de perto (a sombra nos olhos), mas a silhueta fica parecida com o A.

## Bruxa do pântano (`bruxa.png`): três rostos, o chapéu da A

- **b1, o nariz adunco** (`bruxa-b1`): o nariz comprido para o lado, o olho apertado, o sorriso torto com um dente.
- **b2, o olho leitoso** (`bruxa-b2`): um olho saltado e branco e o outro fechado, o nariz verruguento, a careta; o
  chapéu de ponta torta.
- **b3, o sorriso banguela** (`bruxa-b3`): o rosto comprido de faces fundas e o sorriso largo de poucos dentes, sob a aba
  caída com junco.
- A pele passou ao tom do brejo (um cinza-esverdeado), para a bruxa não ser só o chapéu.
- **A minha preferência: a b1.** Forte: o nariz adunco e o sorriso torto dão a fisionomia de bruxa de imediato, sem
  depender de acessório. Limite: a 32 px o nariz vira uma mancha clara saindo do rosto; o perfil do nariz pede o 48 para
  ler bem. A b2 tem a personalidade mais estranha (o olho), mas o chapéu torto puxa a atenção.

## Carniçal A2 (`carnical.png`): a boca refeita

- **`carnical-a2`:** a boca aberta com a gengiva escura, os dentes de cima presos à arcada (as presas nos cantos), a
  garganta escura, os dentes de baixo na mandíbula caída e o sangue escorrendo; o resto do A.
- **Leitura:** a fome e a ferocidade agora vêm da abertura da boca e da arcada inteira, não de peças claras soltas.
  **Limite:** a boca muito aberta e redonda pode ler como um grito de susto em vez de mordida.

## Espectro A2 (`espectro.png`): o olho único

- **`espectro-a2`:** o trapo suspenso e irregular, a cavidade escura funda no centro e o olho dentro dela (a íris pálida
  em volta da pupila), as pontas rasgadas em comprimentos diferentes, flutuando (a linha de baixo vazia).
- **Leitura:** o olho é o foco, e o trapo que o envolve forma uma silhueta suspensa; não é uma esfera nem tem
  tentáculos. **Limite:** a íris pálida é o ponto mais claro da fileira e, a 32 px, o olho domina a ponto de o trapo
  parecer só uma moldura.

## Javali A2 (`javali.png`): as presas

- **`javali-a2`:** as presas grossas (dois pixels) nascendo ao lado do focinho e subindo em curva para fora até a altura
  dos olhos, o nariz entre elas; comparadas ao lado do Troll e do Rei Troll, bem maiores e mais grossas.
- **Leitura:** as presas dão a ameaça da investida e o focinho continua legível no centro. **Limite:** a 32 px as duas
  curvas abertas, saindo dos lados, lembram um bigode largo ou um par de chifres; a raiz junto ao focinho é o que segura
  a leitura de presa.

## Rato gigante (`rato.png`): três reconstruções

- **r1, de perfil farejando** (`rato-r1`): a cabeça baixa em cunha, o nariz e os incisivos embaixo, a orelha redonda no
  alto, o pescoço maciço enchendo o quadro.
- **r2, de frente, a cabeça baixa** (`rato-r2`): as orelhas redondas no alto, o focinho comprido descendo até o nariz e
  os incisivos, a massa dos ombros embaixo. (Na bancada, com os ombros erguidos nas pontas, virava um morcego.)
- **r3, sibilando** (`rato-r3`): em três quartos para a direita, a boca aberta com os incisivos, o nariz na ponta, a
  orelha atrás.
- **A minha preferência: o r1.** Forte: a cunha da cabeça com o nariz e os incisivos é a silhueta de rato mais
  inequívoca, e a massa do pescoço dá o tamanho de rato gigante. Limite: o olho é uma conta pequena e a expressão é
  pouca; a ameaça vem do volume. O r2 é o mais imponente de frente, mas ainda lembra um pouco um urso; o r3 tem a ação
  (o sibilo), mas a boca aberta escura confunde com o focinho.

## O que fica de fora

Nada integrado nesta rodada; os chefes, os aliados e os sprites compartilhados não mudaram. O Esqueleto E1r, o urso e o
falcão do acampamento e o cajado continuam como estavam.
