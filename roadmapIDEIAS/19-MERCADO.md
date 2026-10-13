# 19 — O mercado com abas e a banca (1.71.0)

Pedido de Jean (13/10/2026): preservar a identidade do mercado, mas tirar a necessidade de percorrer uma página
inteira para comprar suprimentos, procurar equipamento e vender; e mostrar a banca e o comerciante no estilo das
paisagens. Durante o trabalho, Jean precisou: a banca não é o prédio da vila (aquele só representa a função); é o lado
de dentro, mais perto e mais detalhado, com o comerciante na bancada mexendo nas coisas.

## Decisões

- **Três abas, só da tela:** Suprimentos (inicial), Equipamentos e Vender.
  - Trocar de aba não fala com o motor: não passa tempo, não gera estoque, não reinicia o mercado nem mexe em
    sorteio.
  - Sem quarta aba de recompra: ela mora no alto da aba Vender, numa faixa fixa ("Vendidos agora"), que existe
    mesmo vazia. Assim, vender não empurra a lista para baixo.
- **Estrutura fixa:** o título e o Sair (na barra da tela, como já era), o ouro e as abas ficam parados; só a lista
  da aba rola. A tela mede a altura visível da página e ocupa exatamente ela.
- **O motor diz o motivo** de cada coisa que não se compra agora, já escrito (`Loja.dados_loja`):
  - suprimento esgotado ("Esgotado: o mercador reabastece amanhã cedo."), comida cheia ("Você já carrega o máximo
    de comida."), aljava cheia ("A aljava está cheia.") e ouro insuficiente;
  - peça à venda com ouro insuficiente ou mochila cheia (`motivo_compra_equip`: a mesma conta de
    `comprar_equipamento`, que só olha a mochila quando a peça não vai direto para um espaço vazio do corpo);
  - recompra com ouro insuficiente ou mochila cheia (`motivo_recompra`).
  - A tela mostra o motivo no cartão, com um ícone (não só pela cor).
- **Dois números, dois nomes:** em cada suprimento, "Você tem N" (na comida e nas flechas, "N de 12" / "N de 30",
  com `teto` do motor) e "À venda N" (o estoque do mercador). Saiu o número sem rótulo no canto do ícone.
- **Nada de economia nova:** estoque, preços, reposição, capacidade, recompra pelo mesmo preço na visita, limites
  de compra e as regras de texto ficaram iguais.
- **A banca:**
  - É um interior pixel art no estilo das paisagens e do protótipo da capela: parede de tábuas, duas prateleiras com
    potes, sacos e frascos, ervas penduradas na viga, a lamparina que treme (mais forte à noite), a balança e as
    moedas na bancada.
  - Atrás do balcão, o mercador (desenhado em pixel, não o sprite pequeno): respira, pisca e, a cada oito segundos,
    pega um frasco da bancada, ergue contra a luz e devolve.
  - Retrato ao lado dos produtos (58×78, pixel 3×) quando há largura; com menos largura (a página com menos de
    700 px), uma faixa baixa em cima dos produtos (pixel 2×), para não apertar os cartões.
  - Ao entrar, a banca se revela num pontilhado que se fecha (como a câmera da vila) e a coluna dos produtos chega
    junto. Ao sair, a banca apaga no tempo da página. Nada se repete a cada compra ou troca de aba.
  - Com movimento reduzido, a banca fica parada e não há transição.
  - Sem falas novas.
- **Cliques acidentais:** o `Gesto` (o mesmo do prompt) passou a valer para os cartões do mercado e da recompra. O
  clique que começou antes do redesenho e o segundo clique de um clique duplo não compram nem vendem o item que caiu
  no lugar do outro.

## Implementação

- `rpg/sistemas/loja.py`: `dados_loja` com `teto`, `motivo` nos suprimentos, nas peças e na recompra;
  `motivo_compra_equip` e `motivo_recompra`. As funções de compra, venda e recompra não mudaram.
- `rpg/web/static/telas/mercado.js`: as abas (`role="tablist"`, setas, Home/End), uma lista por aba (cada uma lembra
  a própria rolagem enquanto durar a visita), a altura medida (`ajustar`, que também tira o que ainda sobrar na
  página), a banca (`banca()`: retrato ou faixa, a entrada pontilhada, o ritmo de 10 quadros por segundo).
  - Mantidos: a quantidade por suprimento, segurar +/−, Shift+clique compra 5, Enter compra (e +/− no teclado com o
    foco no cartão), clique vende, botão direito equipa, arrastar até a banca vende, as moedas voando até o ouro.
- `rpg/web/static/app/nucleo.js`: o `Gesto` cobre `.tela.loja .mercadoria` e a recompra.
- `css/08-mercado.css`: o layout de duas colunas, a faixa (`@container`, menos de 700 px), a altura curta
  (`max-height: 760px`: a frase do mercador sai).
- `tests/navegador/cenarios.py`: o cenário `mercado` (CLASSE, OURO, MOCHILA, PROVISOES).

## Validação

- **Testes:** `tests/test_mercado.py` (você tem × estoque, os motivos com as regras concordando, a compra que
  atualiza os dois números, a peça com mochila cheia, a recompra) e os de antes.
- **Gabarito examinado:** só os painéis do mercado das partidas web mudaram, e só com os campos novos (`motivo`,
  `teto`); tirando os dois, nenhuma linha difere.
- **Fumaça:**
  - o cenário da vila: abas por teclado e mouse, trocar de aba não passa tempo, vender mantém a aba Vender,
    recomprar depois de trocar de aba;
  - o cenário novo `cenarioMercado`, em 1280×700: só a lista rola, com abas, ouro e Sair à vista; o motivo escrito;
    "Você tem" e "À venda" separados; Enter compra; clique duplo vende um só; sair e voltar.
- **Conferido na tela (1500×950, 1500×700, 1280×800, 1280×700, 1100×800):**
  - o retrato e a faixa;
  - compras repetidas de tocha (estoque 4 → 1, você tem 3 → 6, ouro descendo);
  - a quantidade e o total, limitados pelo estoque;
  - a aba pelo teclado;
  - venda no fim da lista (a rolagem fica onde dá);
  - recompra depois de trocar de aba;
  - sair e voltar (aba e recompra recomeçam);
  - movimento reduzido (a banca parada);
  - nenhum erro no console.

## Limitações

- A 1280×700 a lista mostra duas fileiras de cartões por vez. É o que sobra com a faixa da banca, o ouro e as abas;
  a lista rola.
- O aviso flutuante de cada operação ("Vendeu …: +7 ouro") é o de sempre e passa por cima das abas por um instante.
- O som do mercado é o de antes (moedas, falha). Não há som novo para a banca.
- Jean ainda não viu: teste humano pendente.

## Acabamento (1.73.0)

Pedido de Jean (13/10/2026): a estrutura com abas está aprovada; refinar a banca e o mercador, a linha das
quantidades e o cartão esgotado. Preços, estoque, limites, reposição e sorteios não mudaram.

- **A banca:**
  - O retrato passou de 58×78 para 64×84, ainda em pixel 3× inteiro (a coluna mede 192 px mais a borda).
  - A composição abre um pouco: a parede do lado em perspectiva, com a janela (luz do dia ou azul da noite), e a
    ponta do balcão com o chão e um barril.
  - O balcão ganhou profundidade: o tampo à vista, com a borda de trás no escuro, veios e a quina da frente na luz;
    embaixo da quina, a sombra; na frente, a lousa de preços pendurada.
  - A luz vem da lamparina, à esquerda. Longe dela, a parede escurece num pontilhado (só no retrato: na faixa larga,
    pesaria).
  - Na faixa, a porta dos fundos com a cortina; as prateleiras param nela.
- **O mercador:**
  - Desenhado por linhas (`FIGURA`), não por retângulos: chapéu de aba com a fita vermelha (a aba faz sombra na
    testa), barba, lenço vermelho, túnica com ombros caídos e avental de couro com bolso.
  - O lado da luz é mais claro no rosto e na túnica; o outro, na sombra.
  - Uma mão apoiada no balcão, com o antebraço até o cotovelo; a outra mexe nas coisas.
  - Os movimentos de antes, ajustados ao desenho: respira, pisca e, a cada oito segundos, pega o frasco, ergue contra
    a luz e devolve. Com movimento reduzido, fica parado.
- **Quantidades:**
  - "Na bolsa: 0 · Estoque: 5"; com capacidade, "Na bolsa: 17/30 · Estoque: 29" (os mesmos `tem`, `teto` e
    `estoque` do motor).
  - O rótulo é discreto e o número claro. Bolsa cheia pinta o número de ouro; estoque zero, de vermelho.
  - Sem espaço, a segunda informação desce inteira e o ponto que separava some do começo da linha.
  - A quantidade a comprar continua no seletor embaixo.
- **Esgotado:**
  - O motor manda `motivo: "Esgotado"` e `detalhe: "O mercador reabastece amanhã cedo."` (só nos suprimentos: as
    peças de equipamento não têm reposição).
  - O cartão mostra só "Esgotado"; a dica junta os dois.
  - Os outros motivos (ouro insuficiente, aljava cheia, comida no máximo, mochila cheia) ficam inteiros no cartão.
- **A dica com o teclado:** no mercado, o foco do teclado num cartão também abre a dica (antes, só o mouse). No resto
  do jogo, as dicas seguem só no mouse.
- **Validação:**
  - Testes: `test_mercado.py`, com o motivo curto e o detalhe só no esgotado.
  - Gabarito examinado: só os painéis do mercado das partidas web mudaram. Com o motivo antigo trocado por
    "Esgotado" e sem o campo `detalhe`, as transcrições ficam idênticas.
  - Fumaça: `cenarioMercado` confere "Na bolsa"/"Estoque" e que o cartão não traz a reposição.
  - Conferido na tela (1500×950, 1500×700, 1280×700):
    - a banca e a faixa, com a animação quadro a quadro e com movimento reduzido;
    - compras repetidas até esgotar tocha, bandagem e antídoto, com a bolsa subindo, o estoque descendo e o ouro
      acompanhando;
    - cinco esgotados de uma vez; comida cheia (12/12) e flechas 20/30;
    - nomes longos ("Tônico Restaurador", "Provisões (1 dia)"), sem corte nem sobreposição nas três colunas da faixa;
    - a dica pelo mouse e pelo foco;
    - nenhum erro no console.
- **Falta:** Jean conferir.

## A faixa única e a vendinha do Vale (1.74.0)

Pedido de Jean (13/10/2026): ele prefere a arte horizontal que aparecia na janela menor; usá-la em todas as larguras,
inclusive maximizado. E a loja deve parecer um pequeno comércio de vila do Vale do Turvo, não uma bancada genérica
com muitos frascos iguais. Só composição e ambientação: textos dos cartões, quantidades, preços, estoque, compras,
vendas, recompra e regras não mudaram.

- **Composição:** a banca é uma faixa em cima do cabeçalho do mercador, das abas e da lista, em qualquer largura; o
  retrato vertical saiu.
  - 96 px de altura (80 px com a janela baixa, abaixo de 760 px), pixel 2× inteiro.
  - Mais largura mostra mais da loja, nunca o desenho esticado.
  - A lista ganhou a largura toda: os cartões a partir de 196 px, três colunas de 1100 a 1920 px de janela.
  - O ouro, as abas, o Sair e a rolagem da lista seguem iguais.
  - Os produtos agora chegam de baixo, junto da faixa que se revela.
- **A loja (vãos):**
  - A parede de tábuas velhas, de tons e larguras diferentes, é dividida por postes em vãos, cada um com um grupo
    reconhecível:
    - curativos: rolos de bandagem, dois frascos, potes de barro;
    - provisões: pães, queijo, provisões embrulhadas em pano e amarradas, carne seca e um odre pendurados;
    - proteção: um gibão de couro no cabide e um broquel;
    - arco: o arco pendurado, a aljava e um feixe de flechas;
    - tochas: um caixote de tochas e uma tocha apagada no suporte;
    - sacos: corda, machadinha, martelo, sacos e caixote;
    - cestos: réstia de alho, maçãs e nabos;
    - ferramentas: martelo, torquês, serrote, lanterna e caixa de pregos;
    - caixas: caixotes empilhados e um barril.
  - Entre os grupos, parede vazia (descanso), a porta dos fundos com a cortina remendada e uma janela.
  - Atrás do mercador, a parede fica lisa.
  - Os dois lados têm ordens diferentes, para os grupos repetidos ficarem longe um do outro.
  - No balcão: livro de contas, balança, moedas, um embrulho, uma faca, um feixe de flechas e sacos; na frente, a
    cinta de ferro com rebites.
  - Nada disso é clicável nem vira mercadoria: é ambientação.
- **Luz:**
  - De dia, a janela clara e a fresta de luz embaixo da porta.
  - À noite, a lamparina mais forte, a janela azul com uma estrela e a loja escurecendo em anéis em volta dela (pixel
    inteiro, sem degradê nem pontilhado).
- **O comerciante:**
  - Um homem mais velho: careca de franja grisalha, sobrancelha desconfiada, nariz comprido, barba grisalha.
  - Túnica de lã crua com o capuz caído nos ombros e avental de couro gasto, com manchas.
  - Cinto de fivela com a bolsa e as chaves.
  - Saíram o chapéu de aba, o lenço vermelho e a túnica azul (pareciam de atendente moderno).
  - Ele pende a cabeça para o lado da mão apoiada no balcão.
  - Os movimentos seguem: respira, pisca e, a cada oito segundos, pega o frasco vermelho, ergue contra a luz e devolve.
- **Animação contínua:** o relógio do mercador é o da visita. Uma compra (que redesenha a tela) não recomeça o gesto
  nem a entrada; trocar de aba nem redesenha a faixa. Com movimento reduzido, tudo parado.
- **Validação:**
  - Testes, pyflakes, gabarito idêntico, fumaça completa (`cenarioMercado` confere a faixa em cima, larga e em pixel
    2×).
  - Conferido na tela, nas janelas 1920×1080 (maximizada), 1500×950, 1500×700, 1280×800, 1280×700 e 1100×800:
    escala 2 sempre, três colunas, a página sem rolar (só a lista).
  - Também: dia e noite, movimento reduzido, e uma compra no meio do gesto (ele continua e ergue o frasco no tempo
    certo, sem repetir a entrada).
  - O cenário `mercado` aceita `PERIODO` (3 é noite).
- **Limitação:** com a janela baixa (700 px), a lista mostra duas fileiras de cartões por vez.
- **Falta:** Jean conferir.

## Quatro ajustes sobre a faixa (1.75.0)

Pedido de Jean (13/10/2026), com a composição horizontal e a loja aprovadas. Compras, vendas, recompra, preços,
estoque, limites, sorteios e navegação não mudaram.

- **As ervas sobre os frascos saíram.** Os dois tufos verdes pendurados em cima dos curativos não tinham forma nessa
  escala. O espaço ficou vazio, sem decoração no lugar.
- **A luz de fora segue o período do jogo** (`periodo_n` do estado, não o relógio do computador). Muda só a janela,
  a fresta da porta, a força da lamparina e o escuro longe dela; o resto da loja guarda as cores.
  - Manhã: vidro claro e suave, fresta fraca.
  - Tarde: vidro mais claro, fresta mais forte.
  - Anoitecer: vidro laranja e fraco, fresta quente, a lamparina mais forte e a loja escurecendo de leve longe dela.
  - Noite: vidro azul com uma estrela, sem fresta, a lamparina no máximo e os anéis de escuro inteiros.
  - O período vem do estado a cada desenho. Comprar redesenha com o mesmo período, e trocar de aba não redesenha
    a faixa: nada pisca.
- **A mão apoiada:**
  - Antes, o antebraço saía em diagonal e a palma ficava solta à esquerda do corpo.
  - Agora o braço desce até o cotovelo (a manga arregaçada), o antebraço curto desce na frente dele, o punho encosta
    no tampo e a palma fica espalmada logo embaixo, com a sombra no balcão.
  - O gesto do frasco foi conferido quadro a quadro: parado, indo, erguendo, erguido, devolvendo e de volta. A mão
    segue ligada ao braço, sem atravessar o balcão.
- **Vender é a grade da mochila:**
  - Como no inventário: os 12 espaços, os vazios apagados e fora do Tab, e "Mochila N/12" com a ocupação e a
    capacidade reais.
  - Cada item mostra o ícone, a raridade (a cor da borda) e, no canto, o que o mercador paga.
  - A ficha e a comparação (com Shift) seguem na dica, pelo mouse e pelo foco do teclado.
  - Clique vende; botão direito equipa; arrastar até a banca vende; Enter vende pelo teclado.
  - O `Gesto` cobre as células: o segundo clique de um clique duplo não vende o item que cai no lugar.
  - "Vendidos agora" e a explicação saíram. Depois da primeira venda aparece, embaixo e separada, a seção
    "Recomprar", com os itens e o preço de cada um (o mesmo da venda, até sair do mercado, inclusive trocando de
    aba). Saíram também os cartões grandes da venda.
- **Validação:**
  - Testes, pyflakes, gabarito idêntico, fumaça completa (a vila confere a grade, "Mochila N/12", os vazios fora do
    Tab, a recompra só depois da venda e o título "Recomprar").
  - Conferido na tela (1500×950 e 1280×700):
    - mochila vazia, com 1, 8 e 12 itens;
    - venda (a grade, a ocupação e o ouro atualizam), clique duplo vendendo um só;
    - troca de aba e recompra pelo mesmo preço;
    - dica pelo mouse e pelo teclado;
    - os quatro períodos, o gesto quadro a quadro e o movimento reduzido;
    - nenhum erro no console.
- **Falta:** Jean conferir.

## Como Jean testa

1. Numa vila, entre no mercado: a banca aparece num pontilhado, e a aba Suprimentos já está aberta.
2. Compre a mesma coisa algumas vezes: o "Você tem" sobe, o "À venda" desce, o ouro do topo acompanha. Esgote um
   item e veja o motivo escrito no cartão.
3. Troque de aba com o mouse e com as setas (foco numa aba). A lista de cada aba lembra onde estava.
4. Em Vender, venda alguma coisa e vá para Suprimentos e volte: a recompra continua lá, pelo mesmo preço.
5. Saia (Esc) e entre de novo: volta a Suprimentos, sem a recompra da visita anterior.
6. Num monitor menor (ou com a janela estreita), a banca vira uma faixa em cima.
7. (1.73.0) Repare no mercador (chapéu, lenço, a mão apoiada no balcão) e espere uns oito segundos: ele pega o frasco
   e ergue contra a luz. Compre até esgotar algo: o cartão diz só "Esgotado"; passe o mouse (ou chegue com Tab) para
   ler quando o mercador reabastece.
8. (1.74.0) Abra o mercado maximizado e numa janela menor: a loja é sempre a faixa em cima. Repare nos grupos da
   parede (bandagens, pães, gibão, arco, tochas, cestos, caixotes) e no mercador de avental de couro. Para a noite:
   `$env:PERIODO="3"; python -m tests.navegador.cenarios mercado`.
9. (1.75.0) Troque `PERIODO` por 0, 1, 2 e 3 (manhã, tarde, anoitecer, noite) e repare na janela e na porta. Olhe a
   mão apoiada e espere o frasco. Na aba Vender, venda um item e veja a grade, "Mochila N/12", o ouro e a seção
   "Recomprar" aparecendo; troque de aba e recompre. Para mochila vazia ou cheia: `$env:MOCHILA="0"` ou `"12"`.
