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

## A B refinada (R), a candidata (25/10/2026; protótipo, nada no jogo)

O Jean escolheu desenvolver a B (A e B ficam como histórico, em `forja-arte.js`): a melhor ideia de espaço, mas vazia e
esquemática. A R (`forja-r.js`) mantém a profundidade e reconstrói a oficina, com um ferreiro novo trabalhando numa
espada sem parar. A folha B anterior × R no mesmo contexto: `folha-forja-r.png`; o movimento: `folha-movimento.png`
(as poses-chave ampliadas, o ciclo quadro a quadro, a pose do movimento reduzido, a cena no tamanho de uso). A
demonstração: `demo.bat` (o botão R vem primeiro).

### As referências consultadas (e o que se viu de fato)

- **O André de Dark Souls, num GIF do Tenor** (`media.tenor.com/YMxHNb3e6LAAAAAC/martillo-black-smith.gif`, um trecho
  do jogo): **observado quadro a quadro** (18 quadros de 50 ms, decodificados no navegador). Aproveitado: o ritmo, que
  não é de metrônomo: o martelo fica no alto cerca de 400 ms quase parado, desce em cerca de 100 ms, o tronco e a
  cabeça afundam com o golpe, as faíscas explodem no contato e se abrem em riscos longos, ele fica uns 200 ms embaixo
  assentando o martelo e só então sobe num tempo médio. A aparência dele não foi usada.
- **Blacksmith Craft, da Craftpix** (`free-game-assets.itch.io/blacksmith-craft-pixel-art-game-assets`, o GIF de
  demonstração): **observado quadro a quadro** (16 quadros de 100 ms). Aproveitado, em pixel art de tamanho parecido:
  quatro poses bastam para ler o golpe (o repouso, o martelo sobre o ombro, atrás da cabeça, o golpe), o corpo inclina
  para a bigorna no golpe e a faísca nasce no ponto de contato. Evitado: todas as poses no mesmo tempo (100 ms cada).
- **Consultadas sem ver a animação** (só a página ou a descrição): o Animated NPC Sprites da finalbossblues (a página
  do ferreiro não mostra a animação), o Pixel People: The Badass Blacksmith (16×16), o Blacksmith da kanmandev (as
  faíscas e a forja animadas, a martelada não) e o [LPC] Blacksmith da OpenGameArt (as marteladas em andamento). Nada
  delas entrou no desenho.

### O ferreiro e o golpe

- **O ferreiro**: gordo e forte (a barriga projetada com o avental em quatro tons, a borda acesa pela brasa da lâmina),
  os ombros largos curvados sobre o trabalho, o cabelo grisalho à vista, a barba grande e ruiva saindo do queixo na
  silhueta; o corpo a três quartos, um pouco de costas, e a cabeça de perfil para a esquerda (o ângulo ajustado: vista
  de costas, a barba lia como cabelo comprido). Concentrado na espada, sem olhar para quem joga. Os dois dedos que
  faltam não cabem na mão de 3 px: ficam no texto do balcão, sem desenho e sem mudar a história.
- **O ciclo** (o relógio das cenas, 100 ms por quadro; 53 quadros, 5,3 s): assentado na lâmina → sobe em dois tempos
  (o martelo por trás do ombro, sem cobrir o rosto) → segura no alto (200 a 400 ms, variando) → desce num quadro (um
  rastro nítido de 1 px no caminho, sem borrão) → o golpe (a face do martelo encosta na lâmina sempre no mesmo ponto; o
  tronco afunda 1 px; as faíscas nascem do contato) → o rebote (o martelo 3 px acima, as faíscas se abrindo) → assenta
  (100 a 400 ms). Quatro golpes e uma pausa de 600 ms em que a mão da tenaz sobe e a espada vira de lado. O ombro, o
  cotovelo e o punho mudam em cada pose, e o tronco e a cabeça descem com o peso (a cabeça um quadro depois do tronco).
  As pernas não saem do lugar. O último quadro emenda no primeiro (o repouso).
- **A espada em fabricação**: a ponta afinando, o fio aceso em cima e o sulco no meio, a espiga estreita presa na
  tenaz, sem guarda nem cabo; o trecho batido em brasa, mais vivo logo depois do golpe.

### A oficina, por zonas

A porta à esquerda com a rua e a luz fria do dia entrando no chão; a tina de têmpera e o balde perto da bigorna; a
bigorna no toco com dois martelos diferentes encostados e lascas de ferro no chão; a fornalha no fundo, com a fuligem
na chaminé e em volta da boca, as lajes na frente, o monte de carvão com brasas e as duas tenazes penduradas (de bico
longo e de bico chato); o armazém à direita: o cabideiro com uma espada pronta, uma lâmina por terminar, um machado e um
martelo, a prateleira com os lingotes, o feixe de barras de grossuras diferentes, o barril com um elmo por consertar,
duas lâminas encostadas e o escudo. A parede é de taipa e madeira em cima, calma, e de pedra irregular embaixo; o chão
é de terra batida, sem tábuas. A luz quente da fornalha e a fria da porta separam os planos; o foco é o ferreiro, a
espada e a bigorna.

### Conferido (no jogo, `auxiliares/fotografar.mjs` com VERSOES=b,r, as duas janelas, tudo certo)

Os mesmos pontos da B: os nomes à vista e dentro da arte (o Ferreiro sobre a parede, à esquerda da bigorna, longe do
rosto, do martelo e da espada); os três cartões sem rolar a 1280; o Ferreiro levando ao cartão; o Tab nos pontos; um
reforço de verdade; a Saída e a volta; o Esc; **entrar de novo não cria outro relógio** (a arte anda no relógio único
da vista: a contagem dos `setInterval` da página não muda); com movimento reduzido, a pose do alto, parada (duas fotos
iguais). Na bancada (`auxiliares/bancada-r.html`), o ciclo inteiro e as poses.

### A avaliação e os limites

- **O ganho**: o ferreiro tem personalidade e trabalho (a barriga, a barba, a curva das costas, o peso do golpe), o
  olho vai direto para ele, para a espada e para as faíscas, e a oficina tem lugares e usos em vez de uma parede vazia.
- **Os limites**: os braços são construídos por juntas (o contorno e a luz calculados, não pintados pixel a pixel em
  cada pose) e o martelo é desenhado pelo ângulo: lê no tamanho do jogo, mas um acabamento à mão de cada pose daria mais
  forma ao punho e ao antebraço. A espada virando na pausa é sutil (1 px). O ferreiro tem 44 px no quadro: a barba e a
  postura leem a 1920; a 1280 a barba fica pequena, mas a silhueta e o golpe continuam legíveis. A cabeça de perfil
  sobre o corpo a três quartos é uma escolha de leitura. A parede entre a porta e a bigorna fica calma de propósito.
- **Aguarda a aprovação do Jean; a forja não foi integrada.**
