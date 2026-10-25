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

## A transposição fiel (F), a candidata (25/10/2026; protótipo, nada no jogo)

O Jean gostou da fluidez, do ritmo e da sensação de trabalho da R, mas não do desenho do ferreiro (a anatomia e as
proporções estranhas, a barba como um saco no rosto, o corpo caricato) e mandou uma imagem gerada como a referência
principal da aparência (`ferramentas/arte/referencias/forja/`, com a origem e o hash). A F transpõe essa imagem: a
mesma oficina, o mesmo ferreiro (careca, gordo e forte, a barba trançada com a presilha) e o **ritmo da R sem mudança**
(a mesma linha do tempo: 53 quadros de 100 ms). A R, a A e a B ficam como histórico. Folhas: `folha-forja-f.png` (a
referência × a F, a sobreposição das duas, a R × a F no jogo nas duas janelas, a F em tamanho real) e
`folha-movimento-f.png` (os estados ampliados, o ciclo inteiro como o jogo mostrou, o movimento reduzido). A
demonstração: `demo.bat` (o botão F vem primeiro).

### O quadro mais alto (96)

A referência é 3 × 1; nos 320×72 das paisagens, o ferreiro e a fornalha não cabiam sem cortar a composição. A F usa
**320×96** (a redução de 320×107 sem as 4 linhas de cima, só a viga, e as 7 de baixo, a ponta das silhuetas). O pixel
continua o do jogo (320 de largura; 3,33 a 1920, 2,22 a 1280); só a altura da vista cresce, na mesma proporção, sem
esticar: **343 px a 1920×945** (a R: 232) e **236 px a 1280×720** (a R: 182). Os cartões continuam à vista sem rolar
nas duas; a 1280 sobram 15 px de página para rolar abaixo deles (o fim dos cartões em 606, o da página em 627; a R não
rolava). Só no cenário da demonstração, `cenario_forja.py` faz a vista (`vista.js`) usar a altura do ambiente à vista
(cada troca conferida: se o `vista.js` mudar, o cenário para) e `forja.css` dá a altura nova só com o ambiente da F
(`:has(... forja_f)`); na integração, a vista ganharia isso de verdade.

### Como a arte é feita (as fontes e o fluxo)

Em `f/`: `paleta_f.py` (as rampas por material), `base_f.py` (o fundo), `ambiente_f.py` (a bigorna, a espada, a tenaz,
o fogo, o primeiro plano), `ferreiro_f.py` (o ferreiro e as poses), `cena_f.py` (a cena montada quadro a quadro, a
linha do tempo e as faíscas).

- **O fundo** é a referência reduzida por área à grade do jogo, realçada (a média por bloco tira contraste e cor), em
  superpixels (os planos inteiros, as bordas no lugar) e mapeada na paleta. Antes da redução, a área do ferreiro é
  repintada na resolução da referência com a pedra e o chão de perto, para o remendo ter a mesma textura; o suporte de
  ferramentas continua atrás da cabeça dele, desenhado. **É a parte que mais deve à redução**: a porta, a fornalha, as
  vigas, as prateleiras e a bancada vêm da referência assim, limpas pelos superpixels, sem redesenho objeto a objeto.
- **À mão:** o ferreiro inteiro (as grades da cabeça e da barba, do tronco com o avental e o braço de perto, das
  pernas; o braço do martelo em cada pose), lido na referência ampliada com a grade do jogo por cima; a bigorna e o
  toco; a lâmina e a tenaz. **Em código, com desenho escolhido:** o martelo (um objeto rígido: o cabo e a cabeça
  atravessada, a face virada para a luz mais clara), o fogo (o fundo da boca, seis línguas que mudam de altura e
  balanço em 4 quadros, o leito de brasas) e as faíscas (a mesma conta da R).
- **A fonte em camadas:** `python f/desenhar_f.py` gera `f/aseprite/forja-f.aseprite` (320×96; as camadas fundo, fogo,
  bigorna, espada, ferreiro e frente; um quadro por estado, com a tag: repouso, sobe1, sobe2, alto, desce, golpe, volta,
  ajuste, ajuste_virada). **Daqui em diante a fonte é o .aseprite:** os retoques se fazem nele, e o script se recusa a
  sobrescrevê-lo sem `--refazer`. `python f/exportar_f.py` tira dele as camadas do jogo (`f/camadas/`: fundo, bigorna,
  frente, e as tiras fogo, espada e ferreiro); `--conferir` monta os 53 quadros com elas e compara com `cena_f.py`
  (hoje: 53 de 53 iguais; depois de um retoque, as diferenças serão o retoque). As faíscas ficam no código.
- **No jogo:** `forja-f.js` só escolhe o quadro de cada camada pelo relógio das cenas e desenha as faíscas.

### O ferreiro e o golpe

- **Da referência:** a cabeça careca (11 px de largura, com o nariz), o rosto à mostra e separado da barba (a
  sobrancelha pesada, o olho, o nariz, a orelha), a barba com raiz nas bochechas e no queixo, mais larga que o rosto,
  em mechas, afunilando numa trança com a presilha de ferro e a ponta solta; o pescoço e o trapézio, o ombro enorme e o
  bíceps do braço de perto, nu; a braçadeira e a luva segurando a tenaz; a barriga redonda sob o avental, que acompanha
  o corpo; a túnica escura nas costas com a amarra do avental; as pernas firmes e as botas grandes. Escala de
  personagem no ambiente: **~55 px dos pés ao alto da cabeça**, o martelo no alto a 70 (a R: 44).
- **As mãos são simples, sem dedos**, no padrão das da Ilse e do mercador (pedido do Jean durante esta entrega); os
  dois dedos que faltam continuam no texto do balcão. O antebraço da tenaz tem o porte do bíceps (~8 px; também pedido
  dele: estava fino).
- **O ciclo:** o da R, quadro a quadro (o repouso na lâmina, sobe em dois tempos, o alto segurado de 200 a 400 ms, a
  descida num quadro com o rastro, o golpe com o tronco afundando 1 px e as faíscas no contato, o rebote 3 px acima, o
  repouso variando; quatro golpes e a pausa de 600 ms em que a tenaz vira a espada). As poses foram refeitas para o
  corpo novo: em cada uma, o punho fechado no cabo, a braçadeira, o cotovelo e o bíceps entrando atrás da barba (no
  golpe e no rebote, o antebraço desce do lado da barba até o punho). A cabeça e a barba descem um quadro depois do
  tronco no rebote; o avental vai com o tronco; os pés não saem do lugar. A face do martelo encosta na lâmina sempre no
  mesmo ponto, onde as faíscas nascem. Movimento reduzido: a pose do alto, parada, o fogo parado.

### Conferido

- `auxiliares/fotografar.mjs` (VERSOES=r,f; o jogo de verdade, campanha temporária), **as duas janelas, tudo certo**:
  a arte no topo; os nomes Ferreiro e Saída à vista e dentro da arte (o Ferreiro na parede à direita dele, longe da
  cabeça, da barba, do martelo e da espada; a Saída na porta); os três cartões à vista; o Ferreiro levando o foco ao
  cartão; o Tab nos pontos; um reforço de verdade (300 → 260); a arte depois do reforço; a Saída e a volta; entrar de
  novo sem relógio novo; o Esc; sem erros; o movimento reduzido parado (duas fotos iguais).
- `auxiliares/ciclo_f.mjs`: dois ciclos inteiros (106 quadros) fotografados no jogo, um por passo do relógio, nas duas
  janelas: **um relógio só, a 100 ms**; as 53 primeiras fotos estão na folha do movimento. Regras, preços, o reforço até
  +5 e os serviços não mudaram; não há som novo.

### A avaliação (o que se preservou e o que se simplificou)

- **Preservado:** a composição inteira da referência (a porta fria, a fornalha atrás e à esquerda, o ferreiro no meio
  voltado para a espada, a bigorna no toco, o armazém e a bancada, as silhuetas da frente; a sobreposição na folha mostra
  os planos no mesmo lugar), o contraste do fogo com o escuro, as proporções do ferreiro (a cabeça, a barba trançada, o
  ombro, a barriga, as pernas) e o ritmo da R.
- **Simplificado:** as texturas miúdas (as pedras, as tábuas, as ferramentas da parede) ficam na resolução do jogo, como
  manchas limpas; as mãos são blocos; a barba tem as mechas e a trança, não cada fio; o braço do martelo no alto é menor
  e menos musculoso que o da referência; a bigorna e o toco são mais simples (a face sem a textura).
- **Os limites:** o fundo vem da redução (limpa, mas não redesenhada objeto a objeto: a porta, a coifa e as prateleiras
  têm a borda da redução, não um contorno escolhido); o remendo atrás do ferreiro, que só aparece entre as poses, é
  pedra lisa; a espada virando na pausa continua sutil (como na R). **Aguarda a aprovação do Jean; a forja não foi
  integrada.**

## A G: a F corrigida, na arte do jogo, a candidata (25/10/2026; protótipo, nada no jogo)

A F não foi aprovada. O Jean manteve o design do ferreiro, pediu os apoios e as ligações da animação corrigidos e o
cenário reconstruído na linguagem dos ambientes aprovados do jogo (a imagem gerada continua só como composição).
A F fica como estava (`f/`, `forja-f.js`); a G mora em `g/` e `forja-g.js`. Folhas: `folha-forja-g.png` (F × G no jogo,
com os mesmos dados, nas duas janelas), `folha-estilo-g.png` (a G ao lado da capela, da prisão da Ilse, da cidade e do
mercado, como o jogo os mostra a 1920), `folha-correcoes-g.png` (F × G nos mesmos quadros: os pés, as pernas, a mão, a
tenaz e a espiga) e `folha-movimento-g.png`. A demonstração: `demo.bat` (o botão G vem primeiro).

### Os defeitos da animação: as causas e as correções

Reproduzidos na F, quadro a quadro (`folha-correcoes-g.png`, a coluna F):

- **As pernas se descolavam no alto:** o tronco inteiro subia 1 px (`tronco: -1`) e as pernas ficavam; abria uma linha
  vazia entre o avental e a calça. **Correção:** o tronco se divide no cotovelo (`CORTE_TRONCO`, y 52): de lá para cima
  (os ombros, o bíceps, o peito, a cabeça e a barba) acompanha o golpe; de lá para baixo (o antebraço, a luva, a
  barriga, o avental) fica. No golpe a linha do cotovelo se sobrepõe; no alto ela se repete. O corpo absorve o
  movimento e as pernas nunca se separam.
- **O pé atravessava o toco e os pés eram grandes:** a bota da frente tinha 13 px e começava em x 152, por cima da
  borda do toco (x 153). **Correção:** as pernas redesenhadas com o tornozelo e botas de 9 e 10 px; a da frente começa
  em x 155, ao lado do toco, sem cobri-lo. Os pés não saem do chão em nenhuma pose.
- **A espiga subia com o balanço e a mão não segurava a tenaz:** a tenaz era desenhada em `59 + tronco` (subia e descia
  com o tronco, e as garras saíam da espiga) e terminava no contorno da luva. **Correção:** a tenaz é do ferreiro,
  parada: as garras fechadas na espiga (x 148) e as hastes entrando na luva, com os dedos por cima e por baixo
  (`tenaz` em `ferreiro_g.py`); a lâmina fica deitada na bigorna. Na pausa, a espada vira de lado com as garras nela,
  separada do balanço dos golpes.
- O martelo encosta na lâmina no mesmo ponto em todos os golpes, e as faíscas nascem ali (x 141, y 58).

O ritmo continua o da R (53 quadros de 100 ms). Nenhum deslocamento precisou mudar além desses.

### O cenário: o que foi reconstruído

Antes, as cenas aprovadas foram fotografadas no jogo, no tamanho real (`auxiliares/estilo.mjs`). O que elas
compartilham, e a G segue: a pedra em blocos regulares com as juntas um tom abaixo (quase sem textura); a madeira, o
ferro e o tijolo em dois ou três tons chapados (a aresta acesa, o lado escuro, o brilho de um pixel); os objetos lidos
pela silhueta e pelo valor, quase sem contorno preto; a luz feita por cima (o halo quente em anéis em volta da fonte e
a sala escurecendo em degraus pontilhados longe dela, como a tocha do ossuário e a lanterna da sacristia); uma paleta
escura e pouco saturada com o acento quente do fogo. Uma particularidade de uma cena só ficou de fora: o céu da cidade e
a água da Ilse.

**Tudo o que é fundo foi redesenhado em `g/oficina_g.py`, nada vem da redução:** a parede em blocos, o teto, o chão de
lajes; o esteio grande com as duas mãos-francesas subindo até a viga, o esteio e o batente da porta; a porta com o dia
frio (a torre com a cruz, os telhados, a neve) e a folha aberta com as ferragens; a prateleira com a vela e os potes, a
tenaz e a argola penduradas, o barril com o bloco de ferro, o atiçador e a pá, a tina do carvão com as brasas; a
fornalha (a chaminé e a coifa simétricas no eixo da boca, a borda rebitada, o tijolo, as aduelas do arco, a fuligem, o
parapeito), o balde com as tenazes e a corrente; o suporte de ferramentas e a prateleira dos cabos; a lanterna presa ao
esteio; a tina de têmpera com a água e a tenaz; as prateleiras do armazém (as caixas, o baú, os lingotes, o elmo, a
caixa), o cavalete das espadas apoiado na bancada (os montantes, a trave e o trilho), a bancada com o martelo, as
barras e o pano, o saco e o barril embaixo; as silhuetas da frente (o jarro, as caixas, o rebolo, a roda). As
correções pedidas no caminho: a coifa estava torta (a chaminé e a coifa em outro eixo que a borda), havia objetos no
ar e encostados (o cavalete sem os pés, as barras tocando as pontas das espadas, uma ripa e uma roldana soltas) e as
mãos-francesas não faziam sentido (uma descia até o suporte de ferramentas).

**O ferreiro, a bigorna e o toco** passaram para o contorno escuro quente da oficina (não o preto), e a bigorna e o toco
para as cores da oficina; o desenho deles é o da F. O ferreiro continua com mais tons que o resto da cena (o rosto, a
barba, o corpo): é o centro da cena, e o mercador do mercado também tem mais cuidado que a banca em volta.

### Conferido

- `g/exportar_g.py --conferir`: os 53 quadros montados das camadas exportadas da fonte (`g/aseprite/forja-g.aseprite`)
  iguais ao desenho em código.
- `auxiliares/fotografar.mjs` (VERSOES=f,g), **as duas janelas, tudo certo**: os nomes Ferreiro e Saída à vista, fora
  do ferreiro e da ação; os três cartões; o Ferreiro levando ao cartão; o Tab; um reforço de verdade; a Saída e a
  volta; entrar de novo sem relógio novo; o Esc; sem erros; o movimento reduzido parado.
- `auxiliares/ciclo_f.mjs` (VERSAO=g): dois ciclos inteiros fotografados no jogo, um por passo do relógio, nas duas
  janelas: um relógio só, a 100 ms.
- **Sem rolagem vazia:** a 1280×720, a F e a G deixavam 15 px de página para rolar abaixo dos cartões (o respiro de
  baixo da folha). A forja com ambiente fica sem ele, como o mercado (`forja.css`); agora 0 px nas duas.

### O que continua

- Nada do fundo vem da redução. O ferreiro e a bigorna foram desenhados à mão sobre a leitura da referência (na F) e
  continuam assim.
- A luz da G é feita por cima com transparência (como nas cenas do jogo): as cores finais não ficam presas à paleta.
- A espada virando na pausa continua sutil.
- **Aguarda a avaliação do Jean; nada integrado.**

## A H: o ferreiro no estilo das figuras do jogo, o corpo inteiro animado, a candidata (25/10/2026; protótipo)

Na G, o Jean viu as pernas descoladas e a metade de cima do corpo subindo e descendo por cima da de baixo (o corte no
cotovelo aparecia), e pediu uma animação de corpo de verdade e o ferreiro conferido com o estilo do mercador, da Ilse
e do resto do jogo. A G fica como estava; a H mora em `h/` e `forja-h.js`, na oficina da G (`h/oficina_h.py`, a mesma).
Folhas: `folha-forja-h.png` (G × H no jogo, com os mesmos dados, nas duas janelas), `folha-estilo-h.png` (o ferreiro
ao lado do mercador e da Ilse, os pixels da tela a 1920; a H ao lado das cenas aprovadas), `folha-corpo-h.png` (G × H
nos mesmos quadros: o corpo no alto, no golpe e no rebote; as pernas e as botas) e `folha-movimento-h.png`. A
demonstração: `demo.bat` (o botão H vem primeiro).

### O estilo

O código do mercador (`telas/mercado.js`, a FIGURA e as cores) e a Ilse mostram o padrão das figuras do jogo: cada
material em três tons chapados (luz, meio, sombra), **sem contorno**, o olho de um pixel escuro, a barba em dois ou
três tons, as mãos em bloco. O ferreiro da F e da G tinha contorno escuro em volta de tudo, muitos tons e a barba em
fios miúdos: estava fora. O da H (`h/ferreiro_h.py`) segue o padrão, com as cores de pele do mercador um pouco mais
quentes pela fornalha; continua o mesmo homem (careca, gordo e forte, a barba ruiva afunilando numa trança com a
presilha, o avental de couro).

### A animação do corpo

Cada pose é desenhada inteira a partir dos apoios, que ficam parados: as botas no chão e a luva fechada na tenaz, que
prende a espiga na bigorna. O resto se acomoda a eles, sem nenhuma parte deslizando por cima de outra:

- **no golpe** os joelhos dobram e o quadril desce, o tronco inclina para a frente e para baixo, a barriga achata e
  alarga, a cabeça e a barba vão junto e a ponta da trança balança para a frente;
- **no alto** as pernas estendem, o quadril sobe, o peito sobe e recua, a trança volta;
- **no rebote** o corpo continua embaixo, a trança ainda balançando; no repouso tudo assenta;
- o braço da tenaz dobra ou estica o cotovelo para a mão ficar onde está; as coxas saem da cintura, o joelho fica
  para fora (a base firme), a canela afina até o cano da bota, onde a calça entra.

Correções do Jean no caminho: a perna "quadrada" por cima da bota (só 4 px de calça reta entre a barra do avental e a
bota; agora a canela afunila, o joelho abre e a calça entra no cano) e o bloco azul atrás do avental (a túnica descia
até o quadril e se emendava na coxa; agora fecha na cintura e a coxa sai arredondada).

O ritmo é o da R (53 quadros de 100 ms); o martelo bate sempre no mesmo ponto da lâmina; os apoios da G (a tenaz presa,
a lâmina parada, as botas longe do toco) continuam.

### Conferido

`h/exportar_h.py --conferir` (53 de 53 iguais ao desenho em código); `fotografar.mjs` (VERSOES=g,h), **as duas janelas,
tudo certo** (os nomes, os cartões, o reforço, a saída e a volta, o Esc, sem relógio novo, o movimento reduzido);
`ciclo_f.mjs` (VERSAO=h): dois ciclos quadro a quadro, um relógio só a 100 ms; sem rolagem vazia a 1280.

### O que continua

- **A escala:** o ferreiro tem ~55 px de altura no quadro (a da referência); a Ilse e o mercador são bem menores na
  tela. O estilo agora é o mesmo; o tamanho é uma decisão sua (diminuir o ferreiro mudaria o enquadramento da oficina).
- O corpo é montado por partes com a luz em três tons (como as figuras do jogo, que são grades e retângulos); o rosto,
  a barba e a trança são grades à mão.
- **Aguarda a avaliação do Jean; nada integrado.**

## A H2: a H com o olho ajustado, a candidata (25/10/2026; protótipo)

O Jean aprovou na H a oficina, o enquadramento, o corpo, a barriga, o estilo e o movimento, e manteve a escala do
ferreiro (os enquadramentos da forja, da Ilse e do mercador são diferentes). Faltava o rosto: no tamanho real, o escuro
do olho encostava na transição para o nariz e a construção olho/sobrancelha confundia. A H fica como estava; a H2
(`h2/`, `forja-h2.js`) muda só a cabeça (`CABECA` em `h2/ferreiro_h2.py`, duas linhas): o olho um pixel mais para trás,
a órbita mais escura entre a ponte do nariz e o olho, a sobrancelha logo acima, o olhar para a espada. Três variantes
foram testadas no tamanho real nas poses do alto, do golpe e do rebote (recuar com a órbita entre a ponte e o olho;
recuar com a órbita só sob a sobrancelha, que apagava o olho; manter o olho e separar a ponte, que continuava apertado);
ficou a primeira. A barriga, a escala, a oficina e o ritmo não mudaram. Folha: `folha-rosto-h2.png` (H e H2 nas três
poses, no tamanho do jogo e a 8×, e no jogo a 1920). Conferido: `exportar_h2.py --conferir` (53 de 53),
`fotografar.mjs` com H e H2 nas duas janelas (tudo certo) e `ciclo_f.mjs` com a H2 (um relógio só). A demonstração:
`demo.bat`, o botão H2 primeiro. **Aguarda a avaliação do Jean; nada integrado.**

O processo da forja ficou registrado na skill `arte-cenas-fenda` (`.claude/skills/arte-cenas-fenda/`, com a forja como
estudo de caso em `forja.md`), para os próximos interiores.
