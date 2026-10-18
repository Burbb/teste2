# Os livros aprovados e os recusados

As soluções e os motivos de cada livro, para consulta. São decisões daqueles livros, tomadas olhando o jogo: o
ângulo, as cores, o emblema, a fita e a presença ou não do fecho não são regras para o próximo.

## O Grimório da doca (aprovado; no jogo desde a 1.126.0)

O atalho Grimório da doca (36) e o comando Habilidades da roda da luta (32), num desenho só.
- **As fontes:** `ferramentas/arte/aseprite/atalho-grimorio/`.
- **O modelo:** `ferramentas/prototipos/hud/itens-lote-noite/doca_r3/auxiliares/grimorio_livro.py <36|32> [construcao]`.

**As referências:** a principal, de construção, é um livro marrom inclinado com o símbolo laranja e a fita. A
secundária, de acabamento, é uma prancha com um livro de olhos e um estrelado. Os dois livros violeta citados para
identidade e simplificação não chegaram anexados, e a identidade saiu do couro violeta da família.

**A construção:** um modelo 3D simples numa projeção só.
- **O ângulo:** o livro girado (a borda de cima sobe para a direita), com a profundidade para baixo e para a esquerda.
- **As faces à vista:**
  - a capa da frente;
  - a lombada redonda à esquerda, que sai um pouco para fora e liga as duas capas;
  - o bloco de folhas embaixo, recuado das beiras;
  - a espessura das duas capas finas e a contracapa por trás das folhas.
- **Como se desenha:** cada pixel vem da face mais à frente, com amostragem de 4×4. O 36 e o 32 saem do mesmo modelo.

**A identidade, desenhada nas coordenadas da capa:**
- **O couro:** violeta, em três planos: o alto e o lado da lombada claros, a beira oposta escura e a quina acesa junto
  do sulco.
- **A lombada:** duas nervuras.
- **A moldura:** em baixo relevo.
- **O emblema:** uma estrela de quatro pontas de latão luminoso, com halo no couro, no centro da área útil da capa.
- **Os cravos:** quatro, nos cantos.
- **A fita:** sai das folhas.
- **O fecho:** não tem, para não disputar o espaço do emblema.

**O que podia ser pior** (dito na entrega): o livro inclinado ocupa o quadro na diagonal, e no 32 o halo vira um
pequeno disco.

### As rodadas recusadas

**A rodada 1** (`doca_r3/grimorio_r1/`): o livro em pé, de frente.
- **O problema:** a lombada aparecia à esquerda, e o bloco de folhas, à direita, num ângulo que não acompanhava a capa
  quase frontal.
- **O emblema:** grande, deslocado para a esquerda.
- **O fecho:** apertado contra o emblema.

**A rodada 2** (`doca_r3/grimorio_r2/`):
- **A tentativa:** corrigiu o ângulo (de cima e da esquerda; a lombada como face lateral, e as folhas em cima, entre as
  capas). O emblema diminuiu e o fecho ganhou folga.
- **O problema:** o livro continuou parecendo um bloco com tampa, porque a "espessura" era uma caixa larga sem capas
  finas.
- **O que mudou:** a geometria foi refeita do zero pela referência, em vez de adaptar as faces.

**A primeira proposta da doca** (`ferramentas/arte/desenhar_doca_pixel.py`, histórico): o Grimório e o Diário eram
chapados, sem volume.

## O Diário da doca (aprovado; no jogo desde a 1.125.0)

Um livro aberto: até agora, o único aberto validado.
- **As fontes:** `ferramentas/arte/aseprite/atalho-diario/`.
- **Os auxiliares:** `ferramentas/prototipos/hud/itens-lote-noite/doca_r3/auxiliares/d36.py`, `d32.py`.

**A construção:** desenhado à mão na grade, largo e baixo, visto um pouco de cima.
- **As páginas:** em arco, altas no meio de cada página e fundas na dobra, que escurece em 2 px de cada lado.
- **As beiras:** as camadas das folhas, e a capa de couro marrom à vista por baixo e em volta.

**A decoração:**
- **As anotações:** poucas linhas de tinta clara, de tamanhos diferentes, acompanhando a curva da página.
- **A fita:** vermelha, saindo da dobra.
- **A pena:** afunilada e recortada, num branco frio contra o papel creme, com a sombra dela na página.

**As tentativas recusadas na mesma rodada:**
- a dobra como uma faixa escura larga, e a escrita como uma tabela;
- a pena como uma lâmina cinza; depois, branca sobre o papel branco, sem se separar.

**A diferença do Grimório:** a silhueta (deitado e aberto, contra em pé e fechado) e a composição (pena e fita, contra
emblema), além da cor.

## O grimório do equipamento (aprovado; no jogo desde a 1.108.0)

A arma Grimório, o apoio Tomo e o único Tomo do Nome Esquecido, em 32, 40, 48 e 64.
- **O script:** `ferramentas/arte/desenhar_grimorio_fechado_pixel.py`.

**A referência:** um grimório fechado, deitado na diagonal, visto de cima em três quartos.

**A construção:** um modelo 3D de polígonos planos numa projeção paralela.
- **As faces à vista:** a capa de cima larga, a lombada à esquerda e o pé do livro, que mostra o bloco de páginas
  recuado.
- **A capa:** em almofada, com três planos, o sulco da dobradiça e o brilho só na aresta da cabeça.
- **A lombada:** um cilindro com dois reforços de latão e o brilho em trechos.
- **O resto:** o fecho, uma tira da capa de trás com a chapa de latão; as cantoneiras; e um losango de latão com o
  crescente, inclinado para conversar com a capa.
- **Os tamanhos:** o 64 foi feito primeiro, e cada tamanho tem o emblema simplificado na própria grade.

### Os candidatos recusados, antes dele (os scripts ficam como histórico em `ferramentas/arte/`)

- **O fechado** (`desenhar_livro_pixel.py`): lembrava uma agenda de couro com fecho, pesado e genérico.
- **O entreaberto** (`desenhar_grimorio_pixel.py`): a pose parecia uma folha apoiada numa capa levantada, com a página
  plana e sem ligação convincente entre a capa, a lombada e o miolo.
- **O aberto de duas páginas** (`desenhar_grimorio_aberto_pixel.py`): o Jean preferiu a pose do entreaberto.
- **O de estudo** (`desenhar_grimorio_estudo_pixel.py`): o entreaberto refeito por uma referência. Não foi o escolhido;
  o aprovado foi o fechado da referência nova.

**A conclusão para o entreaberto:** nenhum foi aprovado, e a pose continua sem validação.
