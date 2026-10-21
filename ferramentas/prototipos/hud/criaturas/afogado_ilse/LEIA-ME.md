# Criaturas, primeiro par: o Afogado e a carta da Ilse (proposta, 21/10/2026)

**Pedido de Jean:** começar as criaturas pelo Afogado e pela carta da Ilse (no lugar do Lobo e do Bandido
recomendados no levantamento, `../LEIA-ME.md`). Só no protótipo: nada integrado, regras e dados iguais.

## O que o jogo diz e o formato

- **Afogado** (`afogado`, morto-vivo do Charco, do Salão Alagado e do sarilho da Capela): "os que o pântano não
  devolveu; agarram e puxam para o fundo"; há o Afogado Inchado, o que prepara o golpe no sarilho. Hoje: a caveira
  genérica (a mesma do esqueleto, do carniçal, do cavaleiro sombrio e da Ilse).
- **Ilse** (a guardiã da Capela, `bruxa_afogada` em `missoes.py`): na cena do fundo, a pele azulada, o cabelo de algas
  com uma mecha molhada cobrindo o olho direito, o vestido escuro (`telas/cenas.js`, `ilseDesenho`, a paleta `CORF`).
  Hoje, na carta da luta, a caveira genérica.
- **Formato:** o dos retratos de carta aprovados da comitiva (`retratos.js`, `ODETE_CARTA` e `YARA_CARTA`): 16×16, a
  cabeça e os ombros enchendo o quadro até a base, sem contorno preto (a caixa da carta é escura), poucos planos, a luz
  da esquerda. O jogo mostra a 2× na carta (32 px) e a 3× no Bestiário e no mural (48 px).

## O desenho

- **Afogado** (`afogado`): a cabeça inchada e larga, a pele cinza-esverdeada de quem ficou na água (quatro tons, a luz
  da esquerda), as órbitas fundas e escuras com um ponto pálido, a boca aberta, fios de alga colados no crânio e caindo
  dos lados, a roupa podre nos ombros. Camadas roupa, pele, olhos, algas.
- **Ilse** (`ilse`): a transposição da figura da cena, com a mesma paleta: o rosto azulado e estreito, o olho esquerdo
  claro, a mecha escura sobre o olho direito, o cabelo de algas em mechas separadas descendo pelos dois lados até o
  peito, o vestido escuro. O cabelo sobe um tom em relação à cena (`#3d5a40` e `#2c4130`), para não sumir na caixa
  escura. Camadas vestido, rosto, cabelo.
- **Na bancada:** a primeira Ilse, com o cabelo como uma massa fechada em volta do rosto, lia como um capuz; o rosto
  ficou mais largo, o cabelo fino no alto da cabeça e as mechas dos lados separadas, com o fundo aparecendo entre elas.

## Processo e conferência

- As grades à mão em `auxiliares/grades.py`; as fontes montadas **no editor pelo MCP** (o `pintar.lua`, 0 diferentes na
  releitura) em `fontes/<id>/<id>-16.aseprite`; a exportação pela linha de comando com a conferência
  (`auxiliares/exportar.py`: o 1× igual à grade, @2x exato, alfa 0/255) em `proposta/`. O conector continuou de pé
  depois da exportação em lote.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`), atual × proposta com os mesmos dados: o Afogado numa luta com um
  esqueleto e uma sanguessuga (o cenário `tutorial` com `GRUPO`) e no Bestiário (o `covil` com `BESTIARIO`); a Ilse na
  luta real do fundo da capela (o cenário `capela`, do ossuário: "Descer ao fundo alagado" e "Lutar para destruí-la").
  Na proposta, só a página troca o retrato das cartas e do Bestiário pelo nome da criatura; o jogo ainda não tem papel
  por espécie. Sem erro nem aviso no console.
- A folha: `afogado-ilse.png` (as cartas em tamanho real e 2×, o Bestiário, a Ilse com a cena dela, as duas cabeças ao
  lado do Morel e da Odette na mesma caixa, e a 12×).

## Avaliação (a minha leitura em tamanho real; quem aprova é o Jean)

- **O Afogado** lê de imediato como um morto da água, separado da caveira do esqueleto que fica ao lado: a cabeça
  larga e verde e a boca aberta. No Bestiário, a 3×, continua firme. O risco é ler como um "zumbi" genérico; a alga e a
  roupa podre puxam para o pântano.
- **A Ilse** é reconhecível como a mulher da cena (o rosto azulado, a mecha, o cabelo de alga, o vestido) e fica
  coerente com ela no mesmo quadro. É a mais frágil das duas: o cabelo e o vestido escuros sobre a caixa escura deixam
  a leitura apoiada só no rosto claro.
- **Para a integração,** quando houver aprovação: dar ao retrato um papel pela espécie e pelo chefe (a carta pede o
  retrato pela família, `afogado`, e pela chave da Ilse), sem mudar os traços nem as regras, como foi o `ESTADO` dos
  estados.

## Segunda rodada: a Ilse com fios de alga e o Afogado B (proposta, 21/10/2026)

**Pedido de Jean:** refinar a Ilse, usando a arte da cena como referência principal: mais volume de algas, "fios de
cabelo jogados avulsos mas juntos", não um maço único, com cabelo na frente do rosto; o rosto azulado, o olho claro e
a mecha sobre o outro olho; vãos e diferenças de tom separando os fios do rosto e dos ombros (nada de capuz); legível
na caixa escura sem só clarear. E uma alternativa do Afogado, preservando a atual, que lia como uma "carinha surpresa"
(cabeça redonda, olhos quadrados, boca central): um morto humano da água, com testa, bochechas e mandíbula, inchaço,
decomposição e alguma assimetria, sem três buracos regulares. As primeiras (`ilse`, `afogado`) ficaram intactas.

- **Ilse ajustada** (`ilse-r2`; camadas vestido, rosto, algas): os fios de alga traçados um a um (de 1 px, em cinco
  tons, da alga iluminada `#4f6e47` à quase preta), repartidos no alto da cabeça e caindo em grupos de dois ou três,
  com o fundo da carta aparecendo entre os grupos; um fio claro solto descendo pela frente da face esquerda, a mecha
  da direita em dois fios escuros juntos sobre o olho, que se abrem embaixo; os fios de trás, mais escuros, até a base
  do quadro, por fora dos ombros. Na bancada ficaram três tentativas: as massas largas de alga (lia como capuz, de
  novo), uma trama de fios em diagonal (lia como rede) e os fios convergindo para o rosto (o rosto sumia).
- **Afogado B** (`afogado-b`; camadas roupa, pele, rosto, algas): a cabeça mais larga embaixo do que em cima (as
  bochechas e a papada inchadas), a testa com a sombra pesada das sobrancelhas, um olho turvo e claro de um lado e a
  pálpebra inchada quase fechada do outro, uma mancha escura na bochecha direita, a narina, a boca frouxa e torta,
  caída para baixo, com o lábio de baixo; a pele e a roupa podre da primeira.
- **Processo:** as grades em `auxiliares/grades.py` (`ILSE_R2`, `AFOGADO_B`; a Ilse montada à mão a partir dos fios,
  de trás para a frente); as fontes no editor pelo MCP (`pintar.lua`, 0 diferentes na releitura) em `fontes/ilse-r2/`
  e `fontes/afogado-b/`; a exportação conferida (`auxiliares/exportar.py`: igual à grade, @2x exato). Fotos a
  1920×945 com os mesmos dados (`auxiliares/fotografar.mjs`, o modo `r2`), sem erro nem aviso no console.
- **A folha:** `afogado-ilse-r2.png` (`python auxiliares/prancha.py r2`): a Ilse da cena a 3× ao lado das duas Ilses
  (1×, a carta a 2×, a caixa a 3× e a 6×); os dois Afogados do mesmo jeito; as quatro cabeças na caixa da comitiva, ao
  lado do Morel e da Odette, em tamanho real e a 3×; a luta, o Bestiário e a carta da Ilse na luta do fundo da capela.

**Avaliação (a minha leitura em tamanho real; quem aprova é o Jean):**

- **A Ilse ajustada** tem mais volume e mais verde que a primeira, e o cabelo agora tem desenho próprio: na carta, a
  2×, lê como cabelo molhado e solto em volta de um rosto pálido, e a mecha escura continua no olho certo. O custo: o
  rosto ficou mais estreito (os fios na frente dele tomam um pixel de cada lado) e a silhueta sobe em ponta no alto da
  cabeça. A 1× os fios viram uma textura; a leitura é a da carta.
- **O Afogado B** deixou de ser a carinha surpresa: a cabeça larga e mole, o olho turvo e o outro inchado tiram a
  simetria, e na luta, ao lado do esqueleto, continua separado da caveira. O risco é a boca torta ler como um sorriso
  bobo a 2×; se for o caso, o próximo passo é fechar mais a boca (uma fenda caída) em vez de abrir.
