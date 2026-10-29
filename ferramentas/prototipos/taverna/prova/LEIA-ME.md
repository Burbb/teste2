# Prova de qualidade: os jogadores em duas grades (29/10/2026)

As reconstruções completas da taverna estão interrompidas; a F fica como histórico, sem aprovação e sem integração.
Esta prova separa o que vem da resolução do que vem da construção e do acabamento: os dois jogadores, a mesa redonda e
os banquinhos da F, desenhados de novo em duas grades nativas, no mesmo lugar da tela. **Não é a taverna resolvida:** é
o padrão de qualidade a escolher antes de aplicar ao resto da sala. Nada foi animado nem integrado.

## Abrir

`demo.bat` (o mesmo de sempre) abre na prova. No botão **Protótipo**: **Grade A** ou **Grade B** (a troca é imediata, no
mesmo lugar), **Isolado** (um fundo neutro cobre a sala; o conjunto fica no mesmo tamanho, com um trecho de piso) e as
candidatas da F à A. A sala em volta é a F sem o conjunto, só como contexto provisório.

## As duas grades

| | A: a grade atual | B: o dobro |
|---|---|---|
| Nativa | 66×42 pixels (1 por pixel da sala) | 132×84 pixels (2×2 por pixel da sala) |
| Na tela a 1920×945 | 219,4×139,6 px (3,325 px por pixel da A) | o mesmo (1,66 px por pixel da B) |
| Na tela a 1280×720 | 146×92,8 px (2,21 px por pixel da A) | o mesmo (1,11 px por pixel da B) |

As duas ocupam exatamente o recorte R da sala (x 174, y 42, 66×42 pixels da sala), conferido no jogo nas duas janelas
(a posição e o tamanho iguais aos da vista), com a mesma câmera (a projeção da F), as mesmas posições, poses, paleta e
luz (a da sala, calculada no ponto da sala de cada pixel). O navegador as escala sem suavização
(`image-rendering: pixelated`, devicePixelRatio 1 nas conferências).

**O artefato da apresentação:** a escala da vista não é inteira. A 1920, cada pixel da A vira 3 ou 4 px da tela
(como o resto da sala), e cada pixel da B vira 1 ou 2 px: a irregularidade relativa da B é maior (uma linha de 1 pixel
da B sai com 1 ou 2 px de espessura conforme a posição). A 1280, a B fica quase nativa (1 px, com um de 2 a cada ~9).

## Como foi feito (`conjunto.py`)

- Os móveis saem da projeção da F nas duas escalas: o banquinho de quatro pés com o assento grosso, a mesa redonda de
  um pé torneado com a base em cruz, o tampo com a borda e a face de cima, o tabuleiro (quatro casas por lado na A,
  oito na B) com as peças em pé, as duas canecas, o castiçal; as sombras de contato embaixo dos pés.
- As pessoas são desenhadas à mão em cada grade, em trechos por linha; nenhuma é a outra ampliada ou reduzida. O de
  verde, à esquerda, de perfil e inclinado, o cotovelo no tampo e o punho no queixo (pensa); o de ocre, à direita, de
  três quartos, estende o braço e pega uma peça. O quadril no banquinho, as coxas debaixo da borda, as canelas até as
  botas no piso. Portes diferentes: o de verde mais largo, o de ocre mais magro.
- A referência ("entre brasas e sombras") orientou as poses e a relação com os móveis; nada dela foi reduzido.
- A F ganhou uma chave desligada por padrão (`f.desenho.SEM_RODA`) para exportar a sala sem o conjunto; as camadas da F
  continuam idênticas.

## O que a prova mostrou

- **Na grade atual (A):** os dois sentados, a mesa com tampo e pé, os banquinhos, as pernas até o piso e o braço
  estendido do de ocre leem no tamanho do jogo. O gesto do de verde (o punho no queixo, o braço dobrado) cabe em ~5×6
  pixels e só se lê pela manga mais clara; o tabuleiro vira uma mancha com dois pontos; os rostos são um olho e a barba.
- **O que a grade maior permitiu (B):** o braço dobrado inteiro (o braço, o antebraço, o punho fechado debaixo do
  queixo), a mão segurando a peça, as casas e as peças do tabuleiro, a orelha, o nariz e a linha da barba, o cinto, o
  joelho redondo, a panturrilha e o cano das botas. A atividade dos dois se lê sem ampliar.
- **Se a B destoa:** sim, um pouco. Na sala da A em volta, os pixels da B têm metade do tamanho, e o conjunto parece de
  outra escala de acabamento (mais fino que a lareira e a escada ao lado); a 1920 a escala não inteira deixa os
  pixels da B irregulares. Uma sala inteira na B teria o grão uniforme, mas isso muda todos os interiores (a forja, a
  curandeira e o templo estão na grade atual): não é uma decisão desta prova.
- **O que continua nas duas:** os troncos ainda retos demais (falta a curva das costas e do peito no tamanho do jogo);
  as roupas com poucas dobras; os rostos simples; o contraste entre as roupas e o fundo escuro da sala; a luz por cima é
  a da sala, sem um realce próprio da vela da mesa nas pessoas.
