# A forja do Vau: o levantamento e duas direções (etapa 3, 25/10/2026; protótipo, nada no jogo)

A etapa 3 do plano 23 ("Interior da forja"): criar o ambiente e o ferreiro como cena própria, tomando a capela como
referência de atmosfera, iluminação e interação, **com as regras existentes**. O reforço e o encantamento novos
(materiais, chances, custos, perdas) são a etapa 4 e não entram aqui. A folha: `folha-forja.png` (hoje × A × B no jogo,
nas duas janelas; a arte em tamanho real; o ferreiro ampliado só para diagnóstico). A demonstração: `demo.bat` (painel
em http://127.0.0.1:8775/).

## Os fatos do jogo (o que existe hoje)

- **Quem é o ferreiro:** não tem nome nem retrato. O jogo diz dele só: "Um homem sem dois dedos cospe na forja. 'Ouro
  primeiro.'" (o balcão, `telas/servicos.js`; a mesma fala no texto, `sistemas/servicos.py`), "Volta quando tiver o
  dinheiro." (sem ouro, no texto) e, numa oferta única de saves antigos, o broquel que "trouxeram da capela"
  (`missoes.broquel_do_ferreiro`: "É coisa de quem luta, não de quem forja."). Na vila, o prédio "Ferreiro" é a forja
  de chaminé larga, porta em brasa e a bigorna do lado de fora (`vista.js`), com o som do martelo na bigorna (`som.js`).
- **A entrada e a saída:** no Vau, o clique no prédio do ferreiro (ou a opção "Ferreiro: reforçar arma ou armadura" do
  menu) abre a cena "A forja" (uma tela de menu: o "◀ Voltar Esc" e o título na barra de cima, sem arte). O Voltar ou o
  Esc voltam ao menu da vila; o reforço deixa a forja aberta, redesenhada com o ouro novo.
- **O serviço:** reforçar o que se usa: a arma (Ataque; Poder no Mago), o peito (Defesa) e o apoio (Defesa, Ataque ou
  Poder, pela classe), de +1 a +5. O ganho é ~12% do bônus da peça (no mínimo 1); o custo, `preco(40 × (reforço+1)^1,6)`
  (40 no primeiro); o nome ganha "+n". Um cartão por peça vestida, com o preço; sem ouro, o cartão diz "Ouro
  insuficiente." e não reforça; no limite, "No limite (+5)". Não há outro serviço, estado ou horário na forja.
- **O que se pode reaproveitar:** o sistema dos ambientes da capela (`telas/cenas.js`: o quadro de 320×72 das paisagens,
  o pontilhado de Bayer, os pontos clicáveis com balões, o contorno aceso, o "Destacar interações" do F4, a câmera que
  aproxima ao clicar), o balcão e os cartões de serviço de hoje, o ícone do martelo. Não há retrato do ferreiro.

## As duas direções (as propostas, no jogo)

As duas usam o sistema da capela: o motor manda um painel `cena` da forja antes do balcão, a arte ocupa o quadro de
cima (a mesma altura da capela), com dois pontos de nomes sempre à vista, e o balcão de hoje fica embaixo. **Ferreiro**
leva o foco ao cartão de reforço (é com ele que se reforça; o clique, o Enter e o espaço); **Saída** é o Voltar (a
mesma ação do menu; o Esc e o "◀ Voltar" continuam). Com o ambiente, a cena já mostra quem atende: o topo do balcão fica
numa linha (a fala e o ouro, sem o martelo e o título repetidos) e os três cartões vão lado a lado, à vista sem rolar a
1280×720. Os cartões, os preços, os motivos e o reforço são os do jogo. A arte é pintada à mão em grades (um caractere
por pixel) para o ferreiro, a bigorna, a fornalha e os objetos, e em código para as paredes, o chão e a luz (como a
capela), em `forja-arte.js`. Uma animação só: as brasas e as línguas do fogo trocando devagar; com movimento reduzido, o
quadro fica parado.

- **A · a bancada de trabalho.** Perto: o ferreiro grande (57 px no quadro, quase a altura dele), de martelo erguido, a
  tenaz segurando a barra em brasa na bigorna larga; a fornalha cortada pela borda esquerda, só a boca acesa, jogando a
  luz quente nos volumes (o lado esquerdo do corpo aceso, o direito na sombra); à direita, o quadro das ferramentas, a
  bancada com um elmo e uma lâmina em conserto, e a porta entreaberta com a fresta de luz fria. Oficina habitada, de
  frente para o trabalho.
- **B · o interior da oficina.** Mais aberto e em profundidade: o chão de tábuas fugindo para o fundo, a porta à
  esquerda aberta para o dia (a luz fria entrando no chão), a fornalha no fundo, ao centro, com a chaminé subindo ao
  telhado, e o ferreiro na frente dela, em silhueta contra o fogo, batendo a barra na bigorna; à direita, o armazém: o
  suporte com as lâminas e as lanças, o peitoral no cavalete e os barris. Três áreas legíveis (a saída, o trabalho, o
  armazém) e o quente do trabalho contra o frio do resto.

## Conferido (`auxiliares/fotografar.mjs`, no jogo de verdade, hoje, A e B, 1920×945 e 1280×720, tudo certo)

Entrar pelo prédio do ferreiro; a arte no topo (232 px a 1920, 182 a 1280); os dois nomes à vista e dentro da arte; os
três cartões à vista sem rolar; o clique no Ferreiro levando o foco ao cartão; o Tab chegando aos pontos; um reforço de
verdade (300 → 260 de ouro) com a arte continuando; a Saída voltando à vila com a paisagem de sempre; entrar de novo; o
Esc saindo; sem erros na página; com movimento reduzido, duas fotos da arte iguais.

**Só da demonstração.** O cenário (`auxiliares/cenario_forja.py`) monta uma campanha de teste no Vau (o cenário
`tutorial` dos testes: o Guerreiro com arma, peito e escudo, 300 ou 30 de ouro; os saves numa pasta temporária); troca
`WebUI.painel` só nesse processo para mandar a cena da forja antes do balcão; serve `telas/cenas.js` com o registro das
cenas à vista (`window.__CENAS`) para registrar `forja_a` e `forja_b`. O ponto do Ferreiro usa o tipo "de olhar" das
cenas só para ficar ativo, e `forja.js` troca o clique por levar o foco aos cartões (na integração, as cenas ganhariam
esse tipo de ponto). O balcão compacto e os cartões lado a lado são CSS do protótipo (`forja.css`). A economia, os
preços e os saves não mudam.

## A avaliação (recomendação: B)

- **B** — a identidade do lugar: a sala se lê de uma vez (a porta e a luz do dia, a fornalha acesa no fundo, o
  armazém), e o olho vai para o ferreiro pela silhueta contra o fogo, no centro; a saída é a parte mais clara da cena.
  Limitações: o ferreiro tem 34 px, e o martelo descendo vira um bloco cinza na bigorna; sem o contraste do fogo, ele
  se perderia.
- **A** — o personagem: o ferreiro e o ofício de perto, o martelo erguido e a barra em brasa, a luz do fogo modelando o
  corpo. Limitações: a sala quase não aparece (o lado direito é um corredor de objetos menores); o martelo raspa o alto
  do quadro a 1920 (a arte é recortada em cima e embaixo pela altura da vista).
- **Nas duas:** o ferreiro é um desenho simples (o avental chapado, o rosto com os olhos, a barba e a careca; os dois
  dedos que faltam não aparecem nesse tamanho); as paredes continuam pontilhadas (mais calmas depois do tom do meio, mas
  ainda com textura); o desenho foi feito em grades e código nesta sessão, não no Aseprite (o fluxo documentado do
  projeto é o dos ícones). Exportar certo não garante qualidade: as duas pedem o olhar do Jean antes de qualquer
  acabamento.

**Aguardam a aprovação do Jean; a forja não foi integrada.**
