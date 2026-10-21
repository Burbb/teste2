# Criaturas, segundo par: o Lobo e o Bandido (proposta, 21/10/2026)

**Pedido de Jean:** duas propostas distintas de cada, para escolher a direção antes de refinar uma só; só no protótipo.
O Afogado e a Ilse (1.162.0, `7a9bdc7a`) ficam como estão. Nada integrado: regras, dados e mapeamentos iguais.

## O que os dados dizem e o alcance previsto

- **Lobo** (`lobo`, `dados.py`: fera; "caçam em matilha; durante a luta, seu uivo fortalece o grupo"): no Bosque e na
  Planície, nos eventos de lobos (a emboscada, a matilha da estrada), nos contratos de caça e na fera lendária quando
  ela sorteia um lobo. Hoje o retrato é o `fera`, um rosto de lobo de olhos vermelhos que serve a 12 entidades.
- **Bandido** (`bandido`: humano; "desertores, camponeses arruinados e gente pior; gostam mais do seu ouro do que de
  lutar"): no Bosque, no Charco, na Montanha e na Planície, em muitos eventos (os salteadores da estrada, os líderes com
  nome próprio, a turba da comitiva) e nos que o Senhor da Guerra invoca. Hoje o retrato é o `humano`, o rosto com o
  lenço vermelho no lugar da boca.
- **O alcance, se um for aprovado** (o mesmo caminho da 1.162.0: `RETRATO_FAMILIA` em `dados.py` e o papel `CRIATURA`
  em `icones.js`): só as famílias `lobo` e `bandido`, com as variantes de afixo, os líderes de nome próprio (a mesma
  família) e os invocados. **Continuam como estão:** o `fera` do Lobo Cinzento e do Urso Pardo do patrulheiro (o animal
  do herói), do lobo gélido (outra família), da aranha, do javali, do rato, do sapo, da sanguessuga, da Rainha
  Aracnídea e da Hidra; o `humano` do cultista, do mercenário, da bruxa do brejo, dos chefes humanos, do antagonista e
  dos vultos da sacristia. Nenhum dos dois substitui o sprite globalmente.

## As propostas

Cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno, cores agrupadas, a luz da esquerda), a 2× na
carta e a 3× no Bestiário; nenhum desenho nativo de 32 nem de 48. Na escala da comitiva (Morel, Odette, os heróis).

- **Lobo A, de frente** (`lobo-a`; camadas pelagem, focinho, detalhes): as orelhas altas e pontudas com o fundo
  escuro, a testa larga, os olhos âmbar naturais, o focinho claro que afina até o nariz, as bochechas e a pelagem do
  pescoço até a base; a sombra do lado direito. Na bancada, a primeira tinha o focinho curto e lia como gato: o focinho
  ganhou duas linhas e ficou mais estreito que a cabeça.
- **Lobo B, de perfil** (`lobo-b`; as mesmas camadas): virado para a esquerda, a cabeça um pouco erguida, o focinho
  comprido com o nariz escuro na ponta e a boca, a mandíbula e a garganta claras, a orelha em pé, o pescoço e o peito em
  pelagem até a base. Na bancada, o focinho todo claro parecia um bico: o alto do focinho ficou na cor do pelo.
- **Bandido A, o desertor** (`bandido-a`; roupa, lenço, pele, cabelo, rosto): de frente, a cabeça raspada com o cabelo
  curto no alto, as sobrancelhas carregadas, o nariz claro, a barba por fazer, a boca fechada; o lenço vermelho do
  desenho de hoje passa para o pescoço; o gibão de couro. Na bancada, uma versão de barba cheia ficou parecida demais
  com o Morel.
- **Bandido B, a salteadora** (`bandido-b`; capuz, cabelo, pele, rosto): o capuz de pano pardo que desce até os
  ombros, a franja escura, o rosto à luz com os olhos e a boca, a trança caindo no ombro esquerdo.

## Processo e conferência

- As grades em `auxiliares/grades.py`; as fontes **no editor pelo MCP** (`pintar.lua`, 0 diferentes na releitura) em
  `fontes/<id>/<id>-16.aseprite`; a exportação com a conferência (`auxiliares/exportar.py`: o 1× igual à grade, @2x
  exato, alfa 0/255) em `proposta/`. Os auxiliares são os do primeiro par (`../afogado_ilse/auxiliares/`), adaptados.
- As skills de arte do repositório são de itens (anéis, espadas, livros, luvas) e não cobrem retratos; segui o mesmo
  fluxo (proposta, fotos com os mesmos dados, avaliação) e a linguagem dos retratos de `retratos.js`.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`), atual × A × B com os mesmos dados: uma luta com dois lobos, uma aranha,
  dois bandidos e um cultista, com o patrulheiro e o Lobo Cinzento dele (o cenário `tutorial` com `GRUPO`, `NIVEL=4` e
  `ANIMAL=lobo`); e o Bestiário com as mesmas espécies (o `covil` com `BESTIARIO`). A troca é só na página, nas cartas
  inimigas e nos cartões cujo nome começa por "Lobo" ou "Bandido": o Lobo Cinzento, a aranha e o cultista ficam com o
  desenho do traço. Sem erro nem aviso no console (`capturas/registro.json`).
- As folhas: `lobo.png` e `bandido.png` (`python auxiliares/prancha.py`): a carta na luta (tamanho real e 2×), o
  Bestiário (o retrato a 3×) com a vizinha que não troca, a fileira na caixa da carta ao lado do Morel, da Odette e do
  herói (tamanho real e 3×), a luta inteira e a 12×.

## Avaliação (a minha leitura em tamanho real; quem aprova é o Jean)

- **Lobo A (minha preferência):** lê como lobo na hora, na carta e no Bestiário: as orelhas, o focinho claro e o nariz
  aparecem a 2×; o animal é comum e convincente, sem os olhos vermelhos. Fraco: de frente, é um desenho "de brasão",
  parado; perto do Lobo Cinzento do herói (que continua no `fera`, também de frente) os dois ficam parecidos na mesma
  luta, ainda que o novo seja mais claro e mais lobo.
- **Lobo B:** tem mais movimento e caráter (a cabeça erguida lembra o uivo que fortalece o grupo) e separa bem o
  inimigo do animal do herói. Fraco: a 2× o focinho de perfil é pequeno e a leitura depende da silhueta; a cabeça
  erguida também pode ler como um lobo uivando para a lua, não atacando.
- **Bandido A (minha preferência):** um rosto de verdade, rude e reconhecível, na mesma escala e luz do Morel; o lenço
  vermelho no pescoço mantém a ligação com o bandido de hoje. Fraco: sem o capuz ou a máscara, ele depende da expressão
  e da barba por fazer, que a 2× também pode ler como sujeira; fica perto de um "camponês".
- **Bandido B:** a silhueta do capuz é a mais diferente de todos os retratos humanos e diz "salteador de estrada". Fraco:
  o capuz pardo ocupa quase todo o quadro e escurece a carta; a trança mal aparece a 2×, então a leitura de que é uma
  mulher depende da franja e do rosto; o capuz chega perto do cultista e dos vultos de capa da sacristia.
