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

## Como Jean testa

1. Numa vila, entre no mercado: a banca aparece num pontilhado, e a aba Suprimentos já está aberta.
2. Compre a mesma coisa algumas vezes: o "Você tem" sobe, o "À venda" desce, o ouro do topo acompanha. Esgote um
   item e veja o motivo escrito no cartão.
3. Troque de aba com o mouse e com as setas (foco numa aba). A lista de cada aba lembra onde estava.
4. Em Vender, venda alguma coisa e vá para Suprimentos e volte: a recompra continua lá, pelo mesmo preço.
5. Saia (Esc) e entre de novo: volta a Suprimentos, sem a recompra da visita anterior.
6. Num monitor menor (ou com a janela estreita), a banca vira uma faixa em cima.
