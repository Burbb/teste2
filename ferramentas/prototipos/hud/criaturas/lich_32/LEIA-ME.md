# O Lich Menor: o estudo nativo de 32 e a adaptação para 16 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** o Lich pelo caminho do Dragão (primeiro em 32 nativos, depois à mão em 16), com a L1b como base de
identidade: a coroa antiga, o crânio exposto, os olhos verdes sobrenaturais e o manto violeta; um feiticeiro morto antigo,
severo e consciente, com presença de chefe. Na L1b, a cabeça parecia uma placa comprida e quase retangular. Sem livro nem
acessórios. A L1, a L1b e a L2 ficam como estão em `chefes_e_especiais/`.

## O que vem do jogo

O guardião das ruínas (`lich_menor`): 115 de vida, `morto-vivo` e `conjurador`; Bola de Sombra, Maldição, Invocar
(esqueletos), Drenar. "Um esqueleto coroado ergue os olhos de um grimório. Duas chamas verdes acendem nas órbitas." Só
aparece na carta da luta (32); hoje sai do sprite do traço. **Para uma integração futura:** um papel pelo id do guardião
(`RETRATO_GUARDIAO`), como os outros chefes; os esqueletos que ele invoca continuam com o retrato da família.

## Como foi feito

- **Sem guia:** o desenho parte da identidade da L1b (a mesma paleta, com um realce do osso, um violeta claro na gola, um
  ouro claro na coroa e um verde escuro no fundo das órbitas), não de uma referência externa. As fontes não têm camada de
  guia.
- **O estudo nativo de 32** (`lich-n32`), à mão, em close:
  1. a primeira passada já tinha a coroa pesada (três pontas, a faixa com as pedras violeta e a verde) e a gola alta, mas
     **o crânio continuava uma placa**: a mesma largura da testa ao queixo, as órbitas retangulares e os dentes claros
     numa faixa que lia como sorriso;
  2. o crânio refeito pela anatomia: a testa larga sob a coroa, as têmporas recolhidas, as maçãs salientes, a face
     estreitando até a mandíbula fina e o queixo; as órbitas fundas descendo para o nariz, com um ponto verde claro e o
     halo escuro, contidos; a cavidade do nariz separada das órbitas; a mordida fechada numa linha escura, com os dentes
     discretos em grupos;
  3. **o que não funcionou:** entre a mandíbula e a gola ficava um vazio preto, e a cabeça flutuava; o interior da gola
     ganhou o violeta escuro do manto, por trás do crânio, e o peito, o fecho de ouro.
- **A adaptação para 16** (`lich-n16`), à mão, com o 32 reduzido a 2:1 como mapa: a coroa (as três pontas e a faixa com as
  pedras), a testa, a sombra da testa, as órbitas com o verde, o nariz, as maçãs, os dentes em dois grupos, a mordida, o
  queixo, a gola e o manto. **Na bancada:** os olhos em verde claro viravam duas luzes acesas (ficou o verde médio, dentro
  das órbitas), e o fecho em cruz chamava mais atenção que o rosto (ficou um ponto de ouro).
- **As fontes, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector sem editor, a janela aberta do Jean não foi tocada): uma para cada tamanho, em camadas (manto, crânio, coroa,
  olhos, contorno), 0 diferentes na releitura, reabertas com as camadas na ordem; a exportação igual ao composto, alfa só
  0 ou 255, os derivados em blocos inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), pelo guardião na luta (`CHEFE=lich_menor`) com o Esqueleto
  inimigo e o servo aliado do Erguer Servo de verdade (o `cenario_lich.py` de `chefes_e_especiais`), os dois com os
  retratos de produção, a 1920×945, com os mesmos dados nos quatro modos (o jogo, a L1b, o N32 e o N16), sem erro no
  console. **A folha:** `comparacao.png`.

## A minha leitura (quem decide é o Jean)

- **Conferência técnica** passou; isso não é aprovação visual.
- **O N32** é um rei-morto em close: a coroa pesa sobre a testa, o crânio tem volume (as têmporas, as maçãs, a mandíbula
  fina), o olhar é um ponto verde no fundo das órbitas e a boca fecha severa; a gola sustenta o busto. Ao lado do servo
  (o crânio nu, claro, violeta nos olhos) e do Esqueleto (o elmo), não se confunde.
- **O N16 preservou** a coroa com as três pontas e as pedras, o crânio afunilado até o queixo, as órbitas com o verde
  contido, o nariz, a mordida em dois grupos de dentes e a gola do manto. **Perdeu** as têmporas recolhidas (a 16 o crânio
  é um afunilamento simples), o oco das maçãs e o halo das órbitas; o olhar fica um ponto verde em cada órbita, menos
  intenso que no 32.
- **Na fileira:** o N16 tem o grão dos vizinhos; o N32 destoa, como os outros estudos de 32.
