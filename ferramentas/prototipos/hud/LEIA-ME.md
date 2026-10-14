# Protótipo: a ficha do herói (experimento)

Seis versões na mesma página, com os mesmos dados e a mesma janela: **Anterior** (a HUD atual do jogo, com a ficha
desenhada em código), **Assets** (a ficha com peças recortadas de uma imagem de referência), **HUD 3** (a HUD inteira
com as molduras, as superfícies e os controles de três folhas de referência), **HUD 4** (a rodada seguinte, sobre a
HUD 3), **HUD 4 completa** (a HUD 4 com os ícones e o retrato de quatro folhas novas) e **HUD 4 pixel** (a família
de ferro, de contorno duro, e os atributos sem caixas). O controle "Versão" (ou a tecla
**V**) passa de uma à outra; a página abre na última que você viu (na primeira vez, na HUD 4).

**Experimento, não aprovado nem migrado.** Nada desta pasta é carregado pelo jogo; o motor, os saves, as regras e as
telas de produção não mudaram, nem a versão do jogo. O teste é só a ficha do herói (o painel da esquerda); o topo, a
cena e o painel do mundo em volta são o jogo de hoje, para julgar a ficha na composição.

## Como abrir no Windows

1. **Duplo clique em `index.html`** (nesta pasta). Abre no Edge ou no Chrome direto do disco.
2. Se a página abrir sem as fontes do jogo (letras genéricas, comum no Firefox ao abrir do disco), use o
   **`abrir.bat`**: ele sobe um servidor local com o Python (o mesmo do `python jogar.py`) e abre o navegador em
   `http://localhost:8765/ferramentas/prototipos/hud/index.html`. Para parar, feche a janela "servidor do prototipo".

Na página:

- O quadro claro no canto de baixo à direita são os **controles de demonstração** (fora da interface do jogador):
  a versão (Anterior, Assets, HUD 3, HUD 4, HUD 4 completa ou HUD 4 pixel; **V** passa de uma à outra), o entorno (o Bosque da
  campanha, com a missão e os contratos; o Brejo das duas primeiras tentativas; uma luta do Guerreiro; a capela), a página (o lugar ou a cena de missão, com texto longo), as
  missões (só a missão, ou a missão e os contratos), a janela de comparação do anel (**Esc** fecha), a faixa de
  estados dos controles, nome curto e longo (com PARAIBATRON), nível 1, 6 e 14, equipamento completo, parcial ou vazio, bolsa comum, cheia
  ou vazia, com ou sem ferimentos, com ou sem fome, e os ícones novos ou os atuais (para comparar). **D** esconde e
  mostra o quadro. A escolha fica guardada no navegador.
- Mouse sobre um atributo, espaço, ferimento, item da bolsa ou a reputação mostra a dica, sempre à direita do painel
  (nunca por cima do que ela explica). **Tab** percorre a ficha com o anel de foco; **Esc** fecha a dica.
- Para conferir em 1280 px e janela baixa: diminua a janela (ou F12 e o modo de dispositivo, 1280×720).
- `amostra.html` mostra os assets novos em cada escala, ao lado dos atuais.

## De onde vêm os dados

Tudo o que aparece na ficha vem do motor: `gerar_dados.py` monta um Guerreiro de verdade em cada combinação dos
controles (nível e especialização, equipamento sorteado pelo jogo, os ferimentos e a fome aplicados pelas regras, a
bolsa) e grava o mesmo dicionário que a ficha atual recebe (`rpg.web.estado.heroi`) em `dados.js`. Por isso os
atributos já vêm com a penalidade da fome e das costelas, as dicas são as do jogo e os espaços são os dez de verdade
(Cabeça, Peito, Mãos, Pernas, Pés; Arma, Escudo, Amuleto, Anel 1, Anel 2). Só o nome é livre, como no jogo.
`composicao.js` é o DOM do jogo num lugar real (o Brejo das Cinzas ao anoitecer), fotografado por
`fotografar_composicao.mjs`; a paisagem é desenhada ao vivo pelo `vista.js` do jogo.

Para refazer os dados depois de mudar o jogo: `python ferramentas/prototipos/hud/gerar_dados.py`.

## Decisões visuais (primeira tentativa)

- **Identidade primeiro.** Retrato grande num nicho, o nome na fonte de título e, ao lado, a especialização e o
  nível; a experiência logo embaixo. O nome que não cabe ao lado do retrato ganha uma linha própria em cima (e, se
  nem assim, um passo menor), como a ficha atual já faz.
- **Títulos de seção pequenos.** Versal espaçada, em tom de pedra clara, com um fio discreto até a borda: separam sem
  disputar com o nome nem com a cena (hoje cada seção usa o mesmo título grande e dourado).
- **Números em destaque, rótulos discretos.** Nos atributos, o nome pequeno em cima e o número grande embaixo, para
  caber nos 250 px sem cortar "Agilidade"; a penalidade aparece no próprio número (vermelho, com a porcentagem).
- **Nichos, não caixas douradas.** Espaços de equipamento e da bolsa são buracos na pedra (sombra em cima e à
  esquerda, luz embaixo e à direita), todos do mesmo tamanho, em duas fileiras: o corpo, e as mãos e os adornos. A
  raridade é um filete fino por dentro do nicho (azul, ouro, laranja); o comum não tem.
- **Ouro com moderação.** O dourado ficou nos rebites da moldura, no filete de raridade e no aviso de pontos de
  talento. Ferimentos têm a marca vermelha à esquerda; a fome, âmbar.
- **Moldura reutilizável.** Ferro escurecido com filete de bronze e um rebite por canto, numa imagem de nove partes
  (6 texels por canto): os cantos nunca esticam e as bordas são lisas no comprimento, então serve para qualquer
  tamanho (o painel e as dicas usam a mesma).
- **Assets desenhados em código** (`arte.js`): o retrato do Guerreiro (32×32), a moldura, o espaço de item e quatro
  ícones (espada, escudo, anel, poção). Os ícones são mapas de material (aço, ouro, couro, pano, vidro): o contorno,
  a luz e a sombra saem do mesmo pintor, para terem volume já na escala de uso. O resto vem do catálogo atual.
- **Janela baixa.** O topo da ficha (identidade e experiência) fica parado e o corpo rola, com uma sombra no pé quando
  há mais embaixo; abaixo de 800 px de altura o retrato desce um passo para sobrar espaço.

## O que ainda não convence (primeira tentativa)

- **O retrato** está na escala ×3 (3 px por texel), mais fina que os ícones e a moldura (2 px). O jogo já usa ×3 no
  retrato grande, mas aqui, lado a lado com a moldura nova, a diferença de grão aparece. Desenhar o retrato em 48
  texels a ×2 resolveria, mas é mais arte do que este teste pedia.
- **A espada a ×1** (nos atributos, 16 px) fica fina: a lâmina diagonal de dois texels some um pouco no escuro. A ×2,
  nos espaços, ela lê bem. O escudo, o anel e a poção funcionam nas duas escalas.
- **O pé do painel a 1500×950** sobra vazio (uns 100 px abaixo da reputação). Não estiquei nada para preencher: a
  ficha real tem a comitiva e o animal nessa coluna, que este teste não incluiu.
- **O entorno é fotografia.** A barra de vida e recursos do topo e o painel do mundo são do jogo num momento fixo (o
  herói de nível 1 do cenário), então não acompanham os controles da ficha.

## Segunda tentativa: assets de imagem ("Assets")

As peças vêm da imagem de referência (`assets/original/referencia.webp`, intacta): a moldura, o retrato e os ícones de
espada, escudo, anel e poção. Nada foi redesenhado; `preparar_assets.py` (Pillow e numpy, já disponíveis) só recorta,
limpa o alfa e reduz:

- `assets/pecas/`: cada peça no tamanho original, em PNG com fundo transparente. A referência já tinha o fundo
  transparente, mas trazia uns 2.600 pontinhos soltos (ruído da compressão) e uma franja escura semitransparente em
  volta das peças. Cada peça ficou só com a sua região principal, e o alfa ficou só com 0 e 255 (sem halo nem sombra
  no vazio; conferido).
- `assets/exibicao/`: o que a página usa. A moldura em nove partes (60×60: os quatro cantos de verdade, com 24 px, e
  nas bordas um trecho liso de cada lado, sem rebite), o retrato (100×115) e os ícones em 32 px (espaços e bolsa) e em
  24 px (espada e escudo nos atributos).
- `assets/teste/reducoes.png`: os quatro ícones em 16, 24, 32, 40 e 48 px, para ver onde a leitura se perde.

**Escala.** O "pixel" da arte da referência mede uns 4 pixels da imagem. A moldura e o retrato foram reduzidos 4×, a
mesma escala para os dois: um pixel da arte vira um pixel da tela. Os ícones vêm desenhados com uns 200 pixels, grandes
demais para um espaço de 40 px em qualquer escala comum, então cada um foi para o tamanho de uso. **Limitação:** a 16 px
a espada vira um risco (o escudo, o anel e a poção ainda leem); por isso os atributos usam 24 px, o menor tamanho em
que a espada continua sendo uma espada. A HUD não cresceu: os espaços seguem com 40 px.

**O painel como conjunto.** A superfície agora é lisa, quase preta e morna, sem textura atrás do texto; os títulos de
seção e os fios ficaram mais discretos; as placas dos atributos e os espaços são feitos pela interface (sem moldura
própria), com o dourado só na raridade, no foco e no aviso de talento. A moldura da referência fica só em volta do
painel; a dica ganhou uma borda fina em vez da moldura pesada. Os ícones sem substituto (elmo, peitoral, manopla,
calça, bota, amuleto, a arma do herói e os outros da bolsa) continuam os do jogo.

Capturas comparáveis em `capturas/` (o mesmo estado nas duas versões: `-anterior` e `-assets`), e lado a lado em
`capturas/comparacao-*.png`.

### Avaliação

- **Retrato: o salto é real.** O rosto, o olhar, o elmo com a nasal, a malha e a capa leem a 100 px, e ainda a 80 px
  (janela baixa). É a peça que mais ganha. Só que ele é quase uma pintura: tem mais detalhe e mais gradiente do que
  qualquer outra coisa na tela, incluindo o retrato pequeno do topo (o sprite antigo, de 16 pixels).
- **Ícones: bonitos sozinhos, desiguais no conjunto.** A 32 px os quatro leem melhor que os da primeira tentativa e que
  os do jogo (o escudo com o umbo, o anel com a pedra, a poção com a rolha). Mas a borda deles é suave, sem o contorno
  duro dos sprites; na fileira de baixo, o escudo e os anéis pintados entre a arma e o amuleto em pixel duro parecem de outro jogo.
  A 16 px a espada não serve.
- **Moldura: peso certo, cor errada.** Reduzida 4×, a barra tem uns 12 px e o canto 24 px: um peso que cabe na coluna de
  250 a 290 px, sem esmagar o conteúdo. Mas ela é de aço azulado com filete de ouro, e os painéis do centro e da
  direita são de bronze: a ficha passa a parecer de outro conjunto. Os rebites do meio das laterais ficaram de fora
  (esticados ou repetidos, viravam outra coisa), e a redução deixou o desenho um pouco macio.
- **Combinação com o cenário: o ponto fraco.** A cena é de silhuetas chapadas, em poucos tons e pixel grande; o retrato e
  os ícones são de pintura com muito detalhe e pixel pequeno (1 px de tela contra os 2 px da interface). Isolados,
  ganham; ao lado do Brejo, a ficha fica mais "rica" do que o mundo que ela acompanha.
- **Clareza dos dados: melhor.** A superfície lisa ajudou a leitura dos números e das linhas; os atributos cabem em
  1280 px sem cortar; nada se desloca com PARAIBATRON, com os ferimentos ou com a bolsa cheia. Em janela baixa o
  retrato maior empurra mais conteúdo para a rolagem (186 px contra 157 na primeira tentativa).
- **Diferença de acabamento.** No retrato, grande. Nos ícones, grande quando vistos a 32 px e sozinhos; no conjunto, a
  mistura com o resto do catálogo tira parte do ganho. Na moldura, nenhuma: é outra moldura, não uma melhor. Para essa
  direção funcionar no jogo, o catálogo de itens e as molduras dos outros painéis teriam de vir no mesmo estilo e na
  mesma escala; só trocar estas peças deixa a ficha desencontrada do resto.

## Terceira versão: a HUD inteira com as folhas de molduras, texturas e controles ("HUD 3")

Aqui o teste deixa de ser só a ficha: o topo, a ficha, as barras e recursos, a moldura da cena, a área de leitura e das
ações, o painel do mapa, da missão e dos caminhos, a doca, as dicas e uma janela de comparação de equipamento usam a
mesma família visual. O retrato e os ícones são os da primeira tentativa (desenhados pelo sistema) e os do jogo; o
rosto gerado da segunda não entra. As paisagens são as do jogo.

**De onde vem o entorno.** `fotografar_composicao3.mjs` sobe o jogo em `cenario_hud3.py` (a campanha no Bosque do
Moinho, com a missão da febre e dois contratos de caça) e guarda o DOM do lugar, a página da cena de missão logo depois
(o texto longo) e a janela do anel achado do cenário de teste "aneis" (`composicao3.js`). O topo é redesenhado com o
mesmo estado da ficha (`topo.js`): **a barra de cima e a ficha agora mostram os mesmos números** (antes o topo era a
fotografia fixa do herói de nível 1). Isso vale para as três versões.

**Preparação** (`preparar_hud3.py`, com Pillow e numpy; as folhas ficam intactas em `assets3/original/`):

- cada componente recortado em `assets3/pecas/` (6 molduras, 27 controles, 4 texturas), com o fundo transparente: as
  folhas tinham uns 17 mil pixels de pontinhos soltos e franja, que saíram (alfa só 0 e 255);
- **escala comum**: as texturas têm o "pixel" de uns 4 pixels da folha, e as molduras e os controles são da mesma mão;
  tudo foi reduzido 4×, com os cortes das nove partes em múltiplos de 4. As molduras grandes ficam com a barra de 8 px
  na tela (a estrutura), as pequenas com 4 a 6 px (o secundário);
- **nove partes** para molduras, placas, abas e espaços: os cantos de verdade nunca esticam, e o trecho repetido de
  cada borda é escolhido automaticamente onde não há rebite (com um rebite no trecho, a repetição virava uma fileira
  de pontinhos);
- **barras**: a moldura é a da barra vermelha com o preenchimento apagado (`barra-moldura.png`), e os quatro
  preenchimentos são tiras separadas (`enche-*.png`); o código põe o valor pela largura do preenchimento, sem esticar
  canto nem desenhar número na imagem;
- **texturas**: o miolo de cada quadrado, emendado nas bordas (misturado com ele mesmo deslocado meia volta) e reduzido
  a um ladrilho de 128 px. A folha `assets3/teste/` mostra cada textura repetida antes e depois: a emenda sumiu; fica
  um padrão leve a cada 128 px, coberto pelo véu escuro.

**Onde cada peça foi.** Estrutura (ficha, mundo, cena, janela): as molduras grandes. Topo, barras, mapa, doca e dicas:
as pequenas. Superfícies: a textura superior esquerda nos painéis, a de couro marrom na leitura, a de couro preto
dentro dos espaços de item e das teclas, a de ardósia nos botões, abas e doca, sempre sob um véu escuro. As opções e os
caminhos são placas de ferro; a doca é de abas; os números das opções ficam em nichos.

**Estados** (a faixa "Estados à vista" mostra todos juntos; ao vivo, mouse e teclado fazem o mesmo nas opções, nos
caminhos, na doca e na ficha): normal (placa de ferro); mouse por cima (a placa clareia e o nicho do número ganha as
cantoneiras); pressionado (placa funda e o conteúdo desce 1 px); selecionado (placa de latão e a marca ◆; na aba, o
fio embaixo); indisponível (placa gasta, texto apagado e o cadeado do jogo); foco do teclado (um anel claro por fora).
Nenhum estado importante depende só da cor.

**Composição.** Corredores entre as colunas de 14 para 8 px (6 em 1280), blocos alinhados pelo mesmo quadro, títulos
de seção pequenos em versal, menos ar morto em volta da página. Resultado medido (mesmo estado, mesma janela):

| | Anterior | HUD 3 |
|---|---|---|
| Altura da página de leitura, 1500×950 | 446 px | 473 px |
| Altura da página de leitura, 1280×720 | 244 px | 276 px |
| Rolagem da página no lugar, 1500×950 | 55 px | 10 px |
| Rolagem do painel do mundo, 1280×720 | 385 px | 253 px |
| Rolagem da ficha, 1280×720 (PARAIBATRON, nível 14) | 157 px | 138 px |

Capturas comparáveis em `capturas3/` (cada estado em `-anterior` e `-hud3`, e lado a lado em `comparacao-*.png`): o
lugar, a dica da ficha e a do topo, a janela, os estados, a cena de missão e o foco pelo teclado a 1280×720, o nome
longo a 1280×800. Sem erro no console e sem texto cortado em nenhuma.

### Avaliação da HUD 3

- **Espessura e peso das molduras: melhorou.** A estrutura ganhou um quadro de ferro com cantos de latão que separa as
  três colunas sem pesar (8 px de barra); as molduras pequenas no topo, na doca e nas dicas ficam abaixo dela, e a
  hierarquia se lê. Os cantos ficaram pequenos (14 px): reconhecíveis, mas sem o detalhe da folha.
- **Nitidez no tamanho real: boa, numa escala própria.** Reduzidas 4×, as peças ficam com um pixel da arte por pixel da
  tela: nítidas, mas mais finas que a paisagem, os sprites e o retrato, que andam de 2 a 3 px por pixel. A interface
  parece de um grão e o conteúdo de outro.
- **Textura atrás do texto: no limite certo.** Sob o véu, a pedra dos painéis e o couro da leitura aparecem como
  material, sem manchas atrás das letras; o couro dentro dos espaços quase não se percebe nesse tamanho.
- **Coerência entre as três colunas: melhorou.** O mesmo quadro, a mesma superfície e os mesmos títulos nas três;
  antes, cada coluna tinha títulos grandes e dourados próprios.
- **Espaço útil e rolagem: melhorou** (tabela acima): a página e o painel do mundo rolam menos.
- **Leitura dos controles: melhorou.** As opções viraram botões de verdade (placa, número em nicho), e os estados se
  distinguem pela forma, não só pela cor.
- **Combinação com os cenários: boa no tom, desencontrada no grão.** O ferro escuro e o latão velho combinam com as
  paisagens ao entardecer; o desencontro é a escala do pixel, acima.
- **O que ficou desencontrado:**
  - *Dourado demais nos rebites*: cada placa, aba e espaço traz quatro rebites de latão; somados, o latão aparece em
    toda parte, não só na seleção e no foco. Um conjunto de placas sem rebites (ou com rebite de ferro) resolveria.
  - *O retrato e os ícones antigos* estão em 2 px por pixel dentro de nichos de 1 px por pixel: o nicho parece mais
    fino que o que ele guarda.
  - *O mapa pequeno* ganhou a moldura nova, mas o desenho dele (marcas, rótulos) é o de antes.
  - *A doca* precisa de abas largas (88 px; 80 em 1280) por causa do ombro de 18 px de cada lado da aba: cabe, mas
    com pouca folga se a doca ganhar atalhos.
  - *Os textos dourados de título* (o nome do lugar, o da cena) continuam no estilo antigo, ao lado de títulos de
    seção já discretos.

## Quarta rodada: HUD 4 (sobre a HUD 3)

A direção da HUD 3 (ferro escuro, textura discreta, latão envelhecido) segue; esta rodada muda o que não funcionou nela.
Nenhum asset novo: só as peças já preparadas. Arquivo: `hud4.css` (o corpo leva `v3` e `v4`, então a HUD 4 parte da 3).

- **Molduras com presença, só onde há estrutura.** A moldura da ficha da versão Assets (`assets/exibicao/moldura-nove.png`:
  aço escuro com filete de latão, a face acesa, a sombra por dentro e um rebite em cada canto), na escala em que ela foi
  preparada (barra de uns 10 px, canto de 24 px), vai nos três painéis principais: a ficha, a coluna do centro e o
  mundo. Nada foi engrossado além disso.
- **Uma moldura por coluna.** Na HUD 3, o topo das barras, a cena e a doca eram três caixas empilhadas com bordas
  duplas entre elas. Agora moram dentro da mesma moldura do centro, separados por um fio de sombra e luz.
- **Superfície de carvão em tudo.** A textura dos painéis nas três colunas; a leitura é o mesmo carvão um passo mais
  claro; os botões e a doca, o metal um pouco mais claro. O couro marrom da leitura saiu (papel fica para livro, Diário e
  documento).
- **Controles internos leves.** Opções, caminhos, botões da janela, espaços de item, o retrato, as teclas e os cartões
  da janela são feitos pela interface: aresta fina, face de metal, sem rebite dourado. O latão ficou na seleção, no foco,
  no aviso de talento, na barra da missão e no cartão do item achado.
- **O nome do lugar, uma vez.** A apresentação principal é a do painel do mundo (nome, tipo, perigo). No centro, a
  página do lugar abre só com a linha do momento (tipo, perigo, dia, período, clima) em versal pequena; a cena de
  missão mantém o título dela, menor (32 px), sem o ornamento. Isso conta com o painel do mundo à vista: abaixo de
  1100 px de largura o jogo o esconde, e aí o nome precisaria voltar ao centro.
- **Doca: uma barra só**, com divisões discretas entre os atalhos e um fio mais forte entre os grupos que o jogo já
  separa; nomes, teclas e foco preservados. A aberta tem o fio de latão embaixo.
- **Espaços de equipamento**: nichos escuros de aresta fina, o ícone atual em 32 px (o mesmo ×2 do jogo, sem
  deformar) com folga em volta; 44 px de lado onde a coluna deixa (a partir de 1400 px de largura), 40 px em 1280. O
  item que não serve agora tem o canto cortado em vermelho, além do ícone apagado.
- **O que o motor já distingue** ganhou forma: a missão e o contrato pela marca à esquerda (latão e ferro) e pelo grupo;
  quem abre outra escolha, pela seta › que o jogo já põe. Nada foi inventado.
- **Retrato e ícones**: os atuais do jogo (o retrato do Guerreiro em ×5 na ficha, ×4 com a janela baixa). O rosto e os
  itens pintados da versão Assets não entram.
- **Estados**: normal; mouse (a aresta acende, a face clareia, a tecla vira latão); pressionado (a face afunda e desce
  1 px); selecionado (aresta e barra de latão, e a marca ◆); indisponível (aresta tracejada, face apagada, cadeado e a
  nota escrita); foco do teclado (anel claro por fora).

Capturas em `capturas4/`, com os controles de demonstração escondidos: cada estado nas três composições
(`-anterior`, `-hud3`, `-hud4`) e lado a lado em `comparacao-*.png`; o detalhe das molduras e superfícies da HUD 3 e
da HUD 4 em `detalhe-molduras-superficies.png`. Conferido em 1500×950, 1280×800 e 1280×720: a página do lugar e a
cena de missão (texto longo), nome longo, fome, ferimentos, a missão com dois contratos, os equipamentos, a janela dos
dois anéis, a dica, o foco do teclado e a rolagem. Sem erro no console e sem texto cortado.

| Rolagem (mesmo estado) | Anterior | HUD 3 | HUD 4 |
|---|---|---|---|
| Página do lugar, 1500×950 | 55 px | 10 px | 0 |
| Página do lugar, 1280×720 | 257 px | 207 px | 72 px |
| Cena de missão, 1280×720 | 685 px | 589 px | 510 px |
| Ficha, 1280×720 (PARAIBATRON, nível 14) | 157 px | 138 px | 155 px |
| Painel do mundo, 1280×720 | 385 px | 253 px | 277 px |

### Avaliação da HUD 4

- **Coerência: melhorou.** As três colunas são três peças do mesmo material, com a mesma moldura e a mesma
  superfície; o centro deixou de ser outra cor e outra caixa. As bordas duplicadas sumiram.
- **Presença das molduras: melhorou.** A barra de metal com face acesa e o rebite no canto se leem como estrutura, não
  como linha em volta de caixa; por dentro, só arestas finas.
- **Cenário, leitura e ações: mais espaço.** Sem o título grande no centro e sem as caixas empilhadas, a página ganhou
  altura: no lugar, a 1500×950 as ações cabem sem rolar, e a 1280×720 a rolagem caiu de 207 para 72 px.
- **O que custou:** a moldura mais larga tira uns 20 px das laterais: a ficha e o mundo rolam um pouco mais que na
  HUD 3 em janela baixa (tabela acima).
- **O que ainda ficou desencontrado:**
  - *O grão da moldura*: ela vem da imagem de referência reduzida 4× e é um pouco macia ao lado dos sprites e da
    paisagem, de pixel duro e maior.
  - *O retrato do jogo em ×5* dentro do nicho fino fica grosso; e os anéis do catálogo atual, pequenos no desenho de
    16, continuam miúdos no espaço de 44 px (ampliar só em passo inteiro, ×3, não cabe no espaço).
  - *A doca* ocupa a largura toda, mas os atalhos ficam no meio, com sobra dos lados.
  - *O topo* ainda usa a faixa fina da HUD 3 embaixo; não ganhou a linguagem da moldura principal.
  - *O nome do lugar só no painel do mundo* depende de esse painel estar à vista (ver acima).

## Quinta rodada: HUD 4 completa (ícones e retrato de quatro folhas)

A HUD 4 aprovada (molduras, profundidade, cantos, carvão, doca, cenários) fica como está; esta rodada põe nela uma
família de desenhos: atalhos, equipamentos, recursos, atributos, lugares e o retrato. Arquivos: `preparar_hud4c.py`
(os assets), `icones4c.js` (o que vai onde), `hud4c.css` (o corpo leva `v3 v4 v4c`: só acrescenta à HUD 4),
`composicao4c.js` e `fotografar_composicao4c.mjs` (a luta e a capela). O controle "Ícones" (novos ou atuais) troca os
desenhos sem sair da versão.

### Os assets (`assets4c/`)

- **Originais intactos** em `assets4c/original/` (os quatro anexos, só renomeados: `lugares-atributos.webp`,
  `equipamentos-recursos.webp`, `atalhos.webp`, `retrato.webp`).
- **Alfa conferido antes de mexer**: o fundo já é transparente (alfa 0). O opaco veio em 250 a 253 (compressão) e foi
  levado a 255. Em volta de cada desenho e espalhada pelo fundo há uma franja escura de alfa 1 a 12 (no máximo 5% de
  opacidade), resto do recorte: zerada. Pontos soltos longe do desenho saíram. A borda de antisserrilhado (alfa 13 a
  249) ficou inteira, e com ela o que é do desenho: os riscos da bota, o golpe da espada, as faíscas da chama, o chão e a
  água dos lugares. O relatório de cada peça está em `assets4c/teste/limpeza.txt`.
- **Recorte**: as regiões conexas são achadas na folha inteira e cada uma vai para a célula do seu centro (as peças
  passam um pouco da grade; um recorte pela grade cortava o pé da linha de cima). 37 peças em `assets4c/pecas/`.
- **Normalização pela área visível** (alfa acima de 50%), por grupo: todas com a mesma área, sem nenhuma sair do
  quadrado; as compridas (tocha, espada, raio) batem na borda antes e ficam um pouco abaixo.
- **Redução comparada** em `assets4c/teste/reducoes-*.png`, em tamanho real sobre o carvão e o nicho de item: média
  por área, média com nitidez leve, Lanczos e vizinho mais próximo, em 24/32/40 (atalhos, equipamentos, bolsa), 16/20/24
  (recursos, atributos), 32/40/48 (lugares) e 80/64 (retrato). A média sozinha deixa tudo macio; o Lanczos acende um anel
  nas bordas fortes (aço, ouro); o vizinho serrilha e perde linha fina (a corrente do amuleto, os galhos do pântano).
  Escolhida a **média com nitidez leve**, com o alfa pré-multiplicado (sem halo escuro). Cada tamanho tem o seu arquivo
  e o dobro (`@2x`) para telas densas: o navegador não reescala nada (conferido nas capturas).

| Onde | Tamanho escolhido | Por quê |
|---|---|---|
| Doca | 36 px (caixa de 38, a barra não cresce) | em 32, a mochila, o grimório e a carteira somem no carvão |
| Espaços de equipamento e bolsa | 32 px no nicho de 40/44 | o mesmo tamanho dos ícones da HUD 4 |
| Janela dos anéis | 64 e 48 px | os tamanhos que o jogo já usa nos cartões |
| Atributos | 24 px; 20 em janelas de até 1400 px | em 16 e 20 o escudo e a bota viram mancha; 24 corta "Agilidade" em 1280 |
| Topo: vida e Vigor | 20 px | a altura de uma barra |
| Topo: recursos | 24 px | 32 era o desenho de 16 em ×2 com folga; o novo enche mais a caixa |
| Caminhos | 40 px | em 32 a vila e as ruínas perdem as casas e o arco; 40 não aumenta o cartão |
| Retrato | 80 px; 64 em janelas baixas | o mesmo quadro da HUD 4 |

### O que vai onde (pelo tipo que o motor já manda)

| Desenho | Tipo do jogo | Onde aparece |
|---|---|---|
| Talentos, Grimório, Inventário, Mapa, Diário, Bestiário, Salvar, Sair | os oito atalhos da doca | doca (nomes mantidos; Salvar continua escrito) |
| espada, escudo redondo, amuleto, anel (pedra azul) | `espada`, `escudo`, `amuleto`, `anel` | espaços, dicas, janela dos anéis |
| capuz, armadura de couro, calça de couro, botas, aljava | `capuz`, `gibao`, `calca_couro`, `bota`, `aljava` | só em itens desses tipos; e como silhueta apagada do espaço vazio (Cabeça, Peito, Pernas, Pés) |
| poção, bandagem, tocha | `pocao_vida`, `bandagem`, `tocha` | bolsa e topo |
| pão e trouxa, moedas | provisões, ouro | topo (com estoque) |
| coração, raio | Vida, Vigor (o raio é dourado como a barra do Vigor) | topo |
| espada com golpe, escudo, bota, chama azul | Ataque, Defesa, Agilidade, Poder | atributos (a chama já era o ícone do Poder) |
| vila, floresta, pântano, ruínas, montanha | o desenho do destino (`MapaPx.sprite`: vila ou bioma) | cartões de caminhos |
| retrato | só a classe `guerreiro` | ficha (as outras classes ficam com o desenho delas) |

O jogo separa couro de ferro pela cor do mesmo desenho (calça e calça de couro, bota e bota ferrada, armadura e gibão).
As peças novas são de couro, então não entram nos tipos de ferro: o Guerreiro de demonstração, todo de ferro, mantém
elmo, cota, manopla, perneira e bota ferrada do jogo. Os sprites do jogo têm mais de um papel (a "chama" é o Vigor, o
Poder e a Pena de Fênix): a troca é pelo papel, nunca só pelo nome.

**Sem uso, de propósito:** a adaga (o jogo não tem adaga); o anel vermelho (um tipo, um desenho: a pedra é decoração, e
o vermelho bateria com os avisos); a cripta (nenhum destino é cripta, e o covil do jogo é a caveira de perigo, que a
cripta não diz).

**Faltam (ficou o desenho atual):** elmo, cota/peitoral de metal, manopla e luva, perneira de ferro, bota ferrada; maça,
machado, martelo e as armas das outras classes (arco, besta, cajado, varinha, orbe, livro); tônico, antídoto, unguento,
bomba de fumaça, pena de fênix, baú; os recursos vazios (osso, tocha apagada, bolsa vazia, frasco vazio); Mana e Foco;
planície, cidadela, covil e covil vencido; os retratos das outras classes e o retrato do topo; ferimentos, fome,
reputação, pergaminho da missão, cabeças dos contratos e as notas das opções (a tocha de "−1 tocha").

### Botões centrais

A face das opções, caminhos e botões da janela agora é um degrau mais clara que a página, com luz em cima e sombra
embaixo (relevo discreto) e a aresta um pouco mais viva: o botão se separa do fundo sem o mouse. A tecla continua o
nicho escuro, agora contrastando com a face. O latão ficou só no destaque (missão, selecionado, foco); mouse,
pressionado, indisponível e foco seguem os estados da HUD 4.

### Combate e capela

Dois entornos novos, fotografados do jogo com o mesmo Guerreiro de nível 6 (Paladino): **Combate** (o cenário
"muralha": dois bandidos e um cultista no Bosque do Moinho, depois de uma troca de golpes) e **Capela** (o salão alagado,
de manhã, com a sala desenhada pelo jogo; o protótipo mostra a imagem dela, não a redesenha). A ficha e o topo continuam
o estado dos controles de demonstração (os números da carta de luta são os do herói fotografado). Na luta, como no jogo,
o topo e a doca saem; a roda de ações e as cartas são as de produção.

De passagem: ao trocar de entorno, a paisagem continuava sendo desenhada no canvas da composição anterior (fora da
página) e a nova ficava vazia. Agora o canvas da paisagem é sempre o mesmo.

### Conferência

Capturas em `capturas4c/`, com os controles de demonstração escondidos: cada estado em `-hud4` e `-hud4c`, lado a lado
em `comparacao-*.png` (metade do tamanho) e os detalhes dos ícones em tamanho real em `detalhe-icones-tamanho-real.png`.
Conferido em 1500×950, 1280×800 e 1280×720: página do lugar e cena de missão longa; nome longo, fome, ferimentos e a
missão com dois contratos; equipamento completo, parcial e vazio; bolsa comum, cheia e vazia; a janela dos dois anéis;
mouse (dica do anel, do atributo e da tocha), teclado (foco na opção e nos botões da janela) e rolagem; combate e
capela. Sem erro no console, sem imagem quebrada, sem ícone reescalado pelo navegador e sem texto cortado (o corte de
"Agilidade" em 1280 apareceu e foi resolvido com o tamanho de 20 px). Anterior, Assets, HUD 3 e HUD 4 conferidas pixel a
pixel contra as capturas da rodada passada nas regiões paradas (ficha, página, mundo): iguais.

| Rolagem (mesmo estado) | HUD 4 | HUD 4 completa |
|---|---|---|
| Página do lugar, 1500×950 | 0 | 0 |
| Página do lugar, 1280×720 | 72 px | 72 px |
| Cena de missão, 1280×720 | 510 px | 510 px |
| Ficha, 1280×720 (PARAIBATRON, nível 14) | 155 px | 155 px |
| Ficha, 1280×800 (PARAIBATRON, nível 14) | 75 px | 75 px |
| Painel do mundo, 1280×720 | 277 px | 277 px |
| Luta, página, 1280×720 | 27 px | 27 px |

### Avaliação da HUD 4 completa

O que os testes acima garantem é técnico (sem erro, sem corte, sem rolagem a mais). O acabamento não está aprovado: é
o que esta rodada põe para avaliar.

- **O que melhorou:**
  - *Anéis*: deixaram de ser pontinhos; em 32 no espaço e em 64/48 na janela se leem o aro e a pedra.
  - *Grimório e Diário* se distinguem pela forma (fechado com gema × aberto com pena), não só pela cor.
  - *Bolsa e equipamentos* têm o mesmo peso (32 px, a mesma normalização).
  - *Retrato*: o Guerreiro pintado lê bem em 80 e em 64 e cabe no mesmo quadro; a rolagem da ficha não mudou.
  - *Poção, moedas, tocha, raio e coração* continuam reconhecíveis de relance no topo.
  - *Botões*: a lista de opções se lê como botões mesmo sem o mouse.
- **Perderam leitura ao reduzir:**
  - *Talentos* (36): a árvore de esferas vira um enfeite; sem o nome, não diz "talentos".
  - *Salvar* (36): a carteira com selo e carimbo vira um livro marrom com uma mancha vermelha; só funciona com a palavra
    (mantida).
  - *Provisões* (24): pão e trouxa viram duas manchas claras; o pernil atual lia mais rápido.
  - *Amuleto* (32): a corrente fina some em parte; fica a pedra roxa.
  - *Agilidade e Defesa* (20, em 1280): a bota e o escudo, escuros, quase somem no carvão; em 24 (1500) leem.
  - *Ruínas e pântano* (40): escuros sobre a face do cartão; a vila e a floresta leem melhor.
- **Desencontrados:**
  - *O equipamento do Guerreiro*: metade nova (espada, escudo, amuleto, anéis), metade sprite (elmo, cota, manopla,
    perneira, bota ferrada, maça/martelo). As duas famílias lado a lado são o que mais aparece na ficha.
  - *Dois retratos do mesmo herói*: o pintado na ficha e o sprite ×3 no topo.
  - *Traço*: as peças novas têm sombreado e contorno pintados; os sprites têm pixel duro de 2 px. Em 32 px, lado a lado
    (bolsa cheia, espaços, recursos vazios), a diferença de grão se vê.
  - *Combate*: as cartas, a roda de ações e os ícones das habilidades são os de produção, e agora destoam mais da ficha.
  - *Cores*: a pedra azul do anel tem o azul do "mágico" (a raridade continua na aresta do espaço e no nome, mas a pedra
    pode sugerir raridade); o dourado das peças (anéis, moedas, raio) é mais saturado que o latão da interface e, nos
    anéis grandes da janela, disputa um pouco com o cartão do achado. A chama azul do Poder e a Mana azul colidiriam num
    Mago (o Guerreiro não tem Mana).
- **Faltam**: ver a lista acima. Para a família fechar no Guerreiro, as primeiras são elmo, cota, manopla, perneira,
  bota ferrada e maça/martelo; para o topo, os recursos vazios; depois as outras classes.

## Sexta rodada: HUD 4 pixel (a família de ferro)

As molduras, o carvão, os cenários e os botões da HUD 4 completa ficam como estão; nenhuma moldura nova. Esta rodada
troca a família de desenhos por quatro folhas novas, mais perto da pixel art dos cenários, fecha a ficha do Guerreiro
com as peças de ferro, põe o mesmo rosto no topo e na carta da luta e reorganiza os atributos. Arquivos:
`preparar_hud4p.py` (assets em `assets4p/`), `icones.js` (as duas famílias: a da HUD 4 completa, igual, e a nova),
`hud4p.css` (o corpo leva `v3 v4 v4c v4p`), capturas em `capturas4p/`.

### Os assets (`assets4p/`)

- **Originais intactos** em `assets4p/original/` (`equipamentos-itens.webp`, `atalhos.webp`,
  `lugares-atributos-recursos.webp`, `retrato.webp`).
- **Alfa conferido**: transparência real, como na rodada anterior. Saíram só a franja escura de alfa até 12 (no máximo
  5%) e alguns pontos soltos; contorno e sombras ficaram (`assets4p/teste/limpeza.txt`). As perneiras são duas peças
  separadas por um vão: o recorte agora guarda o par inteiro (`separar(..., par=0.25)`).
- **Sem grade nativa exata**: medida peça a peça, o "pixel" dos ícones fica entre 6 e 9 px da imagem e varia de
  desenho para desenho; o do retrato, uns 11,7 px. Nenhum fator inteiro leva a 32, então não há como "voltar" ao
  original pixel a pixel.
- **Redução comparada em tamanho real** sobre o carvão e o nicho de item (`assets4p/teste/reducoes-*.png`), em cinco
  modos: *macia* (a da rodada anterior, com borda em degradê), *dura* (alfa duro, cor média), *paleta* (alfa duro e, em
  cada pixel, a cor de verdade do desenho mais próxima da média da área), *moda* (a cor mais frequente) e *vizinho*.
  A macia borra o contorno; a moda acende pontos pretos soltos (o elmo, a cota); o vizinho serrilha de forma irregular
  (a grade não bate). Escolhida a **paleta**: contorno duro, só cores que o desenho tem, sem ruído. Cada tamanho tem o
  seu arquivo e o `@2x`.
- **Escala por grupo**, normalizada pela área visível: itens do equipamento e da bolsa juntos (dividem os nichos de
  32), atalhos, recursos, vitais, atributos, lugares.

| Onde | Tamanho |
|---|---|
| Doca | 36 px (na caixa de 38; a barra não cresce) |
| Equipamento e bolsa | 32 px; 64 e 48 na janela dos anéis |
| Atributos | 24 px em todas as larguras |
| Topo | cabeça 48, vida e recurso 20, recursos 24 |
| Luta | cabeça 32 na carta do herói, ações 32 na roda |
| Caminhos | 40 px |
| Ficha | busto 80 px (64 em janelas baixas) |

### O que vai onde (pelo tipo que o motor já manda)

| Desenho | Tipo do jogo |
|---|---|
| elmo, cota de malha, manopla, perneiras, botas de ferro | `elmo`, `armadura`, `manopla`, `calca` (perneira e greva), `bota_ferro` |
| maça, espada, escudo redondo, amuleto, anel (pérola), aljava | `maca`, `espada`, `escudo`, `amuleto`, `anel`, `aljava` |
| poção vermelha, azul, verde; bandagem; baú; tocha | `pocao_vida`, `tonico`, `antidoto`, `bandagem`, `bau`, `tocha` |
| espaço vazio | a silhueta apagada da peça de ferro de cada espaço (agora todos os dez têm desenho) |
| pão e trouxa, osso, moedas | provisões, sem comida (o osso que o jogo já usa), ouro |
| coração, raio, cristal, estrela roxa | Vida, Vigor, Mana, Foco |
| espada, escudo, bota, chama roxa | Ataque, Defesa, Agilidade, Poder |
| vila, floresta, pântano, ruínas, planície, castelo, caverna, montanha | o desenho do destino: vila, os biomas, a cidadela e o covil |
| os oito atalhos | a doca (nomes mantidos; Salvar continua escrito) |
| retrato | só a classe `guerreiro`: o busto na ficha, a cabeça no topo e na carta da luta |
| espada, grimório, poção (na luta) | Atacar (o ataque do Guerreiro), Habilidades, Itens |

O anel tem uma pérola branca: a pedra não lembra nenhuma cor de raridade. A caverna vai para o covil (a toca do
guardião), no lugar da caveira; o covil vencido continua a bandeira do jogo. O martelo não vira maça: fica o desenho do
jogo.

**Ficam com o desenho do jogo:** martelo e machado; as armas e peças das outras classes (arco, besta, cajado, varinha,
orbe, livro; capuz, gibão, calça de couro, bota de caça, luva, manto); unguento, bomba de fumaça, pena de fênix; tocha
apagada, bolsa vazia e frasco vazio do topo; Fugir na roda; os inimigos; o covil vencido; ferimentos, fome, reputação, o
pergaminho da missão, as cabeças dos contratos e as notas das opções.

**Mapeados, mas fora dos dados de demonstração** (não aparecem nas capturas): osso, Mana, Foco, aljava, antídoto, baú,
planície, cidadela, montanha, pântano e covil.

### Atributos

As quatro caixas saíram. Os atributos ficam na superfície da ficha, em duas colunas, separados por um fio claro (entre
as colunas e entre as duas linhas). Em cada um: o ícone de 24 px à esquerda, o nome em 13 px cinza, o valor em 21 px
claro e a penalidade, em vermelho, logo depois do valor (só quando há; o valor também fica vermelho, como no jogo). Em
até 1400 px de largura o nome desce a 12,5 px e o valor a 19, e o ícone continua em 24: "Agilidade" e "33 −25%" cabem
em 1280 sem corte. O mouse e o foco do teclado ainda marcam o atributo, com um véu claro.

### A luta

As linhas dos turnos anteriores do registro ficavam a 35% de opacidade (regra de produção pensada para um fundo claro)
e sumiam no carvão; agora ficam a 70%. A carta do herói mostra a cabeça do retrato; a roda usa a espada, o grimório e a
poção novos. O jogo amplia em 1,12× a carta em foco (`.carta.foco`): ali o rosto amplia em pixel duro, como os sprites.

### Conferência: o que foi capturado e o que foi exercitado

Capturas estáticas, com os controles de demonstração escondidos, em 1500×950, 1280×800 e 1280×720, HUD 4 completa
(`-hud4c`) e HUD 4 pixel (`-hud4p`) com os mesmos dados: página do lugar e cena de missão longa; capela; luta; nome
longo; fome e ferimentos; missão e dois contratos; equipamento completo e vazio; bolsa comum, cheia e vazia; a janela
dos dois anéis. As capturas `-hud4c` dos estados que já existiam ficam em `capturas4c/` (iguais nas regiões paradas);
aqui ficam só as dos estados novos. Lado a lado em `comparacao-*.png`; detalhes em `detalhe-atributos.png` (e `-2x`, só para olhar de
perto), `detalhe-icones-tamanho-real.png` e `ficha-completa.png`. Sem erro no console, sem imagem quebrada, sem texto
cortado, sem ícone reescalado (o único é o da carta em foco, que o jogo amplia).

Exercitado de verdade no navegador (Playwright), não só fotografado:
- mouse sobre um anel equipado, um atributo e a tocha do topo: a dica abriu, com o texto do motor;
- teclado: Tab até um atributo com penalidade (a dica abriu e o foco ficou nele), até uma opção e até os botões da
  janela;
- Esc fecha a janela dos anéis; a tecla V passa pelas seis versões; o controle "Ícones" liga e desliga a família;
- troca de entorno ao vivo (bosque, capela, luta, brejo): a paisagem volta a ser desenhada, a sala da capela aparece;
- rolagem medida em cada estado (tabela).

**Não conferido:** animações (a entrada da roda, o pulso da carta da vez, as transições do mouse), o mouse por cima
da doca e dos botões além do estado fotografado, e qualquer coisa do jogo de verdade: isto é uma fotografia, nada
responde ao clique.

As versões anteriores ficaram iguais: a HUD 4 completa confere pixel a pixel com as capturas da rodada passada nas
regiões paradas, e os assets dela continuam os mesmos. Achado de passagem: na HUD 4 completa, a ponta dos riscos de
velocidade da bota de Agilidade tinha sido cortada no recorte; ela fica como foi avaliada.

| Rolagem (mesmo estado) | HUD 4 completa | HUD 4 pixel |
|---|---|---|
| Página do lugar, 1500×950 | 0 | 0 |
| Página do lugar, 1280×720 | 72 px | 72 px |
| Cena de missão, 1280×720 | 510 px | 510 px |
| Ficha, 1280×720 (PARAIBATRON, nível 14) | 155 px | 153 px |
| Ficha, 1280×800 (PARAIBATRON, nível 14) | 75 px | 73 px |
| Painel do mundo, 1280×720 | 277 px | 277 px |

### Avaliação da HUD 4 pixel

Os testes acima garantem só o técnico. A leitura e o acabamento ficam para avaliar; o pacote não está aprovado.

- **Melhorou:**
  - *Uma família na ficha do Guerreiro*: elmo, cota, manopla, perneiras, botas, espada, escudo, amuleto e anéis do
    mesmo desenho; os espaços vazios também.
  - *Nitidez*: o contorno duro (paleta) fica mais perto do pixel dos cenários e do mapa do que o degradê da rodada
    anterior.
  - *Um rosto só*: ficha, topo e carta da luta mostram o mesmo Guerreiro.
  - *Atributos*: sem as caixas, a ficha respira; o valor manda, a penalidade fica colada nele; ícone de 24 px também
    em 1280.
  - *Recursos do topo*: o coração, o raio, as moedas, a poção e a tocha leem de relance; o pão com a trouxa lê melhor
    que o da rodada anterior.
  - *Texto da luta*: os turnos anteriores voltam a ser legíveis.
  - *Salvar*: a seta entrando no baú diz "guardar" melhor que a carteira (avaliado com o nome à vista).
- **Ainda escuros ou pequenos:**
  - *Grimório* (doca e roda): roxo escuro sobre o carvão e sobre o nicho da roda.
  - *Silhuetas dos espaços vazios*: o ferro cinza apagado quase some.
  - *Talentos*: três esferas ligadas, abstrato; sem o nome, não diz "talentos".
  - *Anel em 48 e 64*: aro fino com o miolo vazio; tem menos massa que o anel anterior.
  - *Bota da Agilidade e manopla*: os detalhes internos viram mancha em 24 e 32.
  - *Bandagem inútil* (sem ferida aberta): o apagado da regra junta com o branco gasto do desenho.
- **Desencontrados:**
  - *O martelo* (a arma do Guerreiro de nível 6) continua o sprite do jogo, no meio das peças novas.
  - *Fugir* na roda, os inimigos e as cartas de produção (molduras douradas e vermelhas) seguem a linguagem antiga.
  - *Frasco vazio, tocha apagada e bolsa vazia* do topo continuam sprites ao lado dos recursos novos.
  - *Retrato pintado × cenários*: o rosto tem mais tons e mais detalhe que os sprites da luta e da paisagem; a cabeça de
    32 px na carta é o ponto em que a diferença menos aparece, o busto de 80 na ficha é onde mais aparece.
- **Faltam:** martelo e machado; as peças e armas das outras classes; unguento, bomba de fumaça, pena de fênix; os
  recursos vazios (tocha apagada, bolsa vazia, frasco vazio); Fugir; o covil vencido.


## Sétima rodada: acabamento da HUD 4 pixel e teste funcional

A HUD 4 pixel foi aprovada como direção visual. Esta rodada não gera outra proposta: acaba a luta e os botões, fecha
as pequenas lacunas de tamanho e liga a HUD ao jogo de verdade, como teste, sem tirar a interface padrão do lugar.

### Acabamento visual

- **A luta** (`hud4p-luta.css`, a mesma folha no protótipo e no jogo): as cartas e a roda ganham o tratamento interno
  dos outros controles da HUD 4 (face de metal escuro, aresta fina, relevo discreto), sem a moldura pesada dos painéis.
  Nome, nível, vida e recurso maiores e mais claros; efeitos em etiquetas finas. Cada estado tem forma, não só cor:

  | Estado | Forma |
  |---|---|
  | lado de cada um | marca de 3 px à esquerda: latão (você), ferro-verde (comitiva), ferrugem (inimigo) |
  | vez de alguém | barra de latão em cima e a marca ▸ antes do nome; o pulso vira um anel que acende e apaga |
  | sua carta, agindo | a mesma barra, a carta à frente (o jogo amplia) e o contorno claro |
  | pode ser alvo | contorno tracejado |
  | alvo escolhido (mouse ou teclado) | contorno cheio claro e a seta ▼ do jogo |
  | fora da luta | aresta tracejada, apagada, com a caveira do jogo |
  | foco do teclado | anel claro por fora |
  | proteção, chefe | o anel por fora do jogo continua (azul, ferrugem) |

  A roda: o medalhão vira um nicho de item, o nome uma placa de metal, a tecla o nicho escuro das opções; latão só
  na ação aberta e no foco. A janelinha de habilidades e itens e as linhas dela seguem a janela leve da HUD 4 (o ícone
  mantém o fio da cor do elemento). Disposição, ações e reações são as do jogo: dano, cura, fuga, derrota, proteção,
  contra-ataque, Revide, efeitos e golpe preparado não mudaram.
- **Fugir** usa a bota com os riscos de movimento (o desenho da Agilidade), com o nome escrito; a porta continua só no
  Sair do jogo.
- **Botões centrais conferidos durante a interação, no jogo** (`capturas-jogo/estados-botoes-jogo.png`): o mouse por
  cima mal se via e o pressionado não descia (a animação de entrada das opções prende `transform: none`). Agora o mouse
  clareia a face um degrau a mais e o pressionado escurece e desce 1 px pela propriedade `translate`. Indisponível
  (aresta tracejada, texto riscado e o motivo) e foco (anel de latão) seguem como estavam.
- **Tamanhos que faltavam** (achados no jogo): a tocha entrou no grupo dos itens (aparece na bolsa do inventário em
  32 px; a mediana do grupo mexeu um pixel em 31 arquivos de itens); a aljava das flechas entrou nos recursos do topo;
  atributos e lugares ganharam 32 px (Fugir, cartões menores). `preparar_hud4p.py` grava `assets4p/exibicao/indice.js`
  com os tamanhos que existem, para a troca nunca pedir um arquivo que não há.

### Teste funcional: a HUD experimental no jogo de verdade

**Como jogar (PowerShell, na pasta do jogo):**

```powershell
git pull
python jogar.py --hud-experimental
```

O jogo abre como sempre (novo jogo, carregar, campanha), com a HUD 4 pixel por cima dos componentes de sempre. Sem a
opção, é a interface padrão. A escolha vale só para aquela sessão: não vai para o save, e um save feito com ela abre
normal sem ela. Para cair direto num cenário de teste (o mesmo motor, uma situação montada):

```powershell
$env:HUD = "experimental"
python -m tests.navegador.cenarios muralha      # luta do Guerreiro (NIVEL=6 pela variável abaixo)
python -m tests.navegador.cenarios capela       # a Capela Afogada
python -m tests.navegador.cenarios mercado      # o mercado do Vale do Corvo
python -m tests.navegador.cenarios aneis        # o anel achado com os dois espaços ocupados
python -m tests.navegador.cenarios tutorial     # a abertura guiada (orientações apontando os controles)
Remove-Item Env:HUD                             # volta à interface padrão
```

Cada cenário mostra um endereço `http://127.0.0.1:...`: abra no navegador; Ctrl+C encerra. Variáveis extras seguem
o mesmo jeito (`$env:NIVEL = "6"` antes da muralha; `$env:NOME = "Aldebarã de Montemor"`, `$env:FOME = "2"`,
`$env:FERIMENTOS = "corte,costelas"` no tutorial) e se apagam com `Remove-Item Env:NOME` etc.

**O ponto de ligação** (o único fora desta pasta, e separado): a opção `--hud-experimental` (`rpg/__main__.py`) chega
ao servidor (`rpg/web/__init__.py` → `Servidor(..., hud_experimental=True)`); nos cenários, `HUD=experimental`. Com
ela, `rpg/web/servidor.py` serve esta pasta em `/experimento/` e põe `<script src="/experimento/jogo/ligar.js">` no
fim da página padrão. Sem ela, a página é a mesma de sempre e a pasta nem é servida (`tests/test_web.py`:
`TestHudExperimental`). Nada no motor, nas regras, nos números, no save ou na versão.

**O que o script faz** (`jogo/`): `ligar.js` carrega as folhas da HUD 4 pixel (`hud3.css` a `hud4p-luta.css`) e
`jogo/jogo.css`, marca o corpo (`v3 v4 v4c v4p hud-experimental`) e carrega `icones.js`, o índice dos tamanhos e
`jogo/papeis.js`. `papeis.js` olha o que o jogo acabou de desenhar e troca só a imagem, pelo papel dela (o recurso do
topo, o atributo pela chave, o espaço pelo nome, a bolsa pelo id, o atalho pelo nome, o caminho pelo desenho do
destino, a ação da roda, o rosto na carta do herói); clique, arrasto, dica e teclado continuam os do jogo. Também
põe a penalidade ao lado do valor do atributo (o número que o motor já manda em `atributos_penal`) e pede ao jogo
para medir de novo o nome depois que o retrato maior entra. `jogo.css` veste o painel real do herói (`#heroi`, com a
comitiva, a bolsa clicável e o aviso de talento) com a moldura, os atributos sem caixa e os nichos de item; e ajusta a
janela do achado à moldura maior. O retrato novo continua só no Guerreiro; as outras classes ficam com o desenho delas.

**Percursos conferidos de verdade** (navegador automático, motor real, HUD experimental):
- a fumaça inteira do jogo (`tests/navegador/fumaca.mjs`, com `HUD=experimental`): 356 conferências, tudo certo. Ela
  cobre os painéis pelos atalhos e pelo mouse, a vila e a capela (aproximação e retorno, salas, baú, sacristia), as
  compras repetidas (clique duplo, Shift, fila), vender e recomprar, o item achado e equipar, a comparação dos dois
  anéis (em 1280×720 e 1280×620), a luta com habilidades, efeitos, comitiva, golpe preparado, Revide e
  contra-ataque, vitória, espólio, relatório e derrota, e o tutorial apontando os controles. A primeira passada achou
  dois problemas nossos, já corrigidos: arquivos de tamanho que faltavam (404) e a janela do anel que empilhava os
  cartões e passava da tela em 1280×720;
- fugir pela roda (a bota nova), até a luta acabar em fuga; Talentos, Grimório, Mapa, Histórico e Ajuda abrindo pela
  tecla e fechando no Esc; Talentos e Mapa pelo clique na doca e pelo Fechar; o Inventário abrindo e voltando pelo mesmo
  atalho;
- os estados dos botões com mouse e teclado de verdade (o pressionado soltando fora não responde);
- as animações da luta, quadro a quadro (`capturas-jogo/animacao-luta-*`), com movimento normal e reduzido: as
  faixas de ação, os números de dano, o clarão do crítico e a roda surgindo não são cortados nem cobrem outra peça
  além do que a interface padrão já faz;
- 1500×950, 1280×800 e 1280×720 com nome longo, fome, ferimentos, contrato, a missão com dois contratos e a cena longa:
  sem texto cortado (o nome longo cortava em 1500 até o jogo medir de novo depois do retrato), e menos rolagem que a
  padrão:

| Rolagem (mesmo cenário) | padrão | experimental |
|---|---|---|
| Nome longo, fome, ferimentos, 1280×800: herói / página / mundo | 84 / 27 / 198 px | 37 / 0 / 130 px |
| Nome longo, fome, ferimentos, 1280×720: herói / página / mundo | 164 / 107 / 278 px | 117 / 0 / 210 px |
| Campanha com missão e dois contratos, 1500×950: página / cena longa | 55 / 322 px | 0 / 179 px |
| A mesma, 1280×800: página / mundo / cena longa | 177 / 265 / 500 px | 0 / 160 / 324 px |
| A mesma, 1280×720: herói / página / mundo / cena longa | 72 / 257 / 345 / 580 px | 10 / 72 / 240 / 404 px |

**Não conferido:** o som; o jogo inteiro de ponta a ponta à mão; a nitidez em telas de densidade 2 (os arquivos `@2x`
existem, mas as capturas são em densidade 1); outras resoluções.

### Lacunas que ficam

**De arte** (não impedem o teste; o desenho do jogo continua no lugar):
- *Guerreiro*: o martelo e o machado (a arma em alguns níveis); os itens únicos com desenho próprio (a cota lendária
  azul, por exemplo) seguem o desenho deles.
- *Outras classes*: o retrato; as armas e peças (arco, besta, cajado, varinha, orbe, livro, capuz, gibão, calça de
  couro, bota de caça, luva, manto); o Atacar da roda (cajado, arco).
- *Bolsa e mercado*: unguento, bomba de fumaça, pena de fênix; as provisões no mercado usam o desenho de 24 px no nicho
  de 32; as moedinhas dos preços.
- *Topo*: tocha apagada, bolsa vazia e frasco vazio.
- *Luta*: os inimigos e as cartas deles (provisórios, como combinado), os ícones das habilidades e dos efeitos.
- *Mundo*: o covil vencido (a bandeira).

**De layout** (achados no teste):
- corrigidos nesta rodada: a janela do anel em 1280×720/620, o nome longo ao lado do retrato maior, a silhueta de
  escudo no espaço do grimório do Mago, os tamanhos que faltavam;
- da interface padrão, não da HUD (acontece igual sem ela): a faixa "Golpe de espada · escolha o alvo" cobre a carta de
  cima enquanto se mira; na luta o registro fica atrás da janelinha de habilidades;
- a barra de experiência ainda usa o desenho de produção (com o fio de baixo), diferente das barras do topo.

## Oitava rodada: componentes uniformes, superfícies e teste de arte

Pedido de Jean: a base da HUD 4 pixel (molduras, composição, atributos) aprovada; uniformizar os componentes que ainda
tinham a aparência anterior, comparar uma superfície mais escura e testar a coerência entre a arte do mundo e a da
HUD com duas peças (o mercador e o baú da sacristia). A interface padrão continua a padrão; nada de regra, número,
save ou versão. Capturas em `capturas-oitava/` (interface e superfícies) e `capturas-arte/` (os pares).

### Componentes uniformes (`jogo/materiais.js`, `jogo/telas.css`)

- **Os materiais do jogo em ferro.** O jogo desenha os anéis, os bicos dos balões e as divisórias com pequenas grades
  de pixel publicadas como variáveis de CSS (`--anel-j`, `--bico-a`, `--fio`, `--ponta`...). `materiais.js` pinta as
  mesmas grades com as cores do ferro e publica no `<body>`: o que ainda usava o bronze (um balão de prédio, um aviso,
  uma dica) passa ao ferro, e os estados que o jogo troca pela variável (o mouse, o convite do mural, o destaque F4)
  continuam funcionando sem código novo. As pontas de ouro das divisórias e o losango dos títulos saíram.
- **A hierarquia** (`telas.css`): janela principal (Mapa, Talentos, Ajuda, Histórico, celebrações, confirmação,
  amanhecer, espólio) com a moldura da HUD 4; janela pequena (dicas, menu de item) com aresta fina e carvão; cartões,
  mercadorias, serviços, comitiva e o quadro do Diário e do mural com aresta fina e a face leve, sem rebite; títulos de
  seção dentro das telas ("Mochila", "Bolsa", "Missão", "Contratos", "Reforçar o que você usa") na versal pequena com o
  fio, como na ficha. Papel continua papel onde é documento: o Grimório, os cartazes de contrato, a missão no Diário.
- **Revisados:** a barra das telas (o fio de ouro com pontas virou o fio de sombra e luz); a experiência na ficha (sem a
  divisória própria: o fio de "Atributos" logo abaixo separa); os recursos do topo (sem a ponta de ouro entre eles); os
  cartões da comitiva; Diário, Inventário, Talentos (os nós num nicho de ferro, os estados por cor e forma), Mapa,
  Bestiário, Histórico e Ajuda (os títulos internos); o mercado (o balcão, a banca, as abas como a doca, as mercadorias:
  o mouse acende a aresta sem pular, o foco é o anel de latão, o que não dá para pagar fica tracejado além de apagado),
  a taverna, o templo e a forja; o mural; o Continuar (a placa de latão); os avisos flutuantes, os cartões de reação da
  comitiva e as linhas do espólio e do amanhecer. Grimório: só o Fechar mudou (o livro é papel).
- **A faixa "escolha o alvo"** (`hud4p-luta.css`, e `papeis.js` tira o ponto que separava as duas partes numa linha):
  no alto da arena ela cobria o nome, o rosto e a vida da carta de cima dos inimigos a 1280 px (também na padrão). Agora
  fica no vão entre as duas fileiras, compacta: o nome da ação, "escolha o alvo" embaixo e o Voltar. Conferido com três
  lobos e com a comitiva (Odette ao lado): nenhuma carta por baixo dela nos três tamanhos.

### Comparação de superfícies (`jogo/superficies.css`, `jogo/desenvolvimento.js`)

Controle de desenvolvimento, não configuração do jogador (não vai para o save): no jogo, `&superficie=escura` (ou
`escura-transicao`) no endereço, ou Ctrl+Alt+S com o jogo aberto; no protótipo, "Superfície (teste)" no painel de
demonstração (HUD 4 pixel). Só os fundos mudam (o véu sobre a textura mais denso); texto, ícones, barras, avisos,
botões e cenários não passam por filtro.

| Medido nas capturas (1500×950, mesmo cenário) | atual | mais escura |
|---|---|---|
| Página abaixo das ações: luminância média / desvio do grão | 20,9 / 1,85 | 16,1 / 1,08 |
| Diferença entre a face de um botão e a página | 21,5 | 26,3 |
| Página × chão da paisagem (floresta / Vau / capela) | 20,9 × 18,1 / 19,6 / 12,1 | 16,1 × 16,7 / 18,2 / 10,7 |

- **Em cima:** a separação da barra de recursos fica igual (o fio do topo não muda; o céu é a arte).
- **Embaixo:** na mais escura a página fica no tom do chão da paisagem (floresta e Vau quase iguais; a capela, um passo
  mais clara), e o salto entre o chão e a área de leitura quase some. A transição curta (18 px na cor do chão, presa
  ao topo da página) quase não acrescenta depois disso: na capela ela escurece a borda, na floresta mal aparece.
- **Botões:** continuam distinguíveis sem o mouse, e um pouco mais (a página escureceu, a face deles não). Seleção,
  foco e indisponível são os mesmos.
- **Minha leitura:** a mais escura, sem a transição. É uma recomendação para a sua avaliação, não uma decisão.

### Teste de arte: mercador e baú (`arte-teste.js`, `arte-teste.html`, `jogo/arte.css`)

Duas peças desenhadas em código pelo método das cenas (uma grade de letras, cada letra uma cor), a partir do que já
existe no mundo, com as mesmas cores. Os cenários não mudaram.

- **Mercador:** o homem da banca (`telas/mercado.js`, a grade `FIGURA` de 21 colunas) num busto de 24×24: mais velho,
  careca com a franja grisalha, sobrancelha pesada e desconfiada, nariz comprido, barba grisalha, o capuz
  verde-acinzentado caído, a túnica de lã crua e o avental de couro; a luz da esquerda, como a lamparina. No jogo, num
  nicho encostado à esquerda do balcão do mercado (48 px, ×2), sem mudar a altura do balcão nem a lista.
- **Baú:** o baú de ferro da sacristia (`telas/cenas.js`, `desenharBau`) de frente, em 16×16, para a bolsa (32 px,
  ×2): a tampa abaulada mais clara, a junta, as duas cintas com rebites, o espelho de latão com a fechadura e a
  ferrugem, com o contorno escuro da família. No jogo, na bolsa da ficha e do Inventário, e no baú que voa até ela
  quando é recolhido. Aquisição, conteúdo, interação e estado do baú são os do jogo.
- **Ver:** `arte-teste.html` (abre direto no navegador) mostra cada par lado a lado, o mundo (recorte do jogo) e a
  interface, no tamanho real e ampliados, e cada candidato no lugar dele; a fotografia está em
  `capturas-arte/pares.png`. No jogo com a HUD experimental o teste vem ligado; `&arte=jogo` ou Ctrl+Alt+A mostram o
  desenho de antes.
- **Minha leitura (não é aprovação):** o mercador se reconhece como o mesmo homem (a careca, a franja e a barba cinza,
  o avental) e lê bem a 48 px; de perto, a barba é uma massa cinza com pouco desenho e os olhos são dois pontos. O baú
  guarda forma, material e ferragens e se lê como baú a 32 px pela fechadura e pelas cintas, mas é o ícone mais escuro
  da bolsa: o ferro do mundo é escuro, e ao lado da poção e da bandagem ele pesa menos que o baú de madeira e latão da
  HUD 4 pixel (`capturas-arte/jogo-bolsa-1500x950.png`, antes e depois). E há uma questão de conteúdo, não de desenho:
  na bolsa o ícone representa todo Baú Trancado, também os que vêm do saque, não só o da sacristia; um baú de ferro
  para todos eles é uma escolha a fazer. Se a direção servir, o próximo passo seria só um degrau de luz no corpo dele,
  sem trocar as cores.
- **No jogo, antes e depois:** `capturas-arte/jogo-balcao-1500x950.png` (o balcão com e sem o mercador) e
  `jogo-bolsa-1500x950.png` (a bolsa da ficha e do Inventário).

### Conferência (jogo de verdade, HUD experimental)

- **Tamanhos:** 1500×950, 1280×800 e 1280×720, com movimento reduzido também em 1280×720. Sem erro de página em nenhum
  percurso.
- **Percursos:** a ficha com nome longo, comitiva, fome e ferimentos (dica da bolsa e da comitiva, foco pelo teclado);
  Inventário (dica do item), Diário, Bestiário, Talentos, Mapa, Histórico e Ajuda (rolada até o fim); a vila (o balão
  do prédio com o mouse), o mural, o mercado (mouse com dica, foco pelo teclado, lista rolada, as três abas), a taverna,
  o templo e a forja; a sacristia (o balão do baú, aproximar pela janela, Afastar, recolher o baú, que voa até a bolsa);
  a luta contra três lobos (a mira, o mouse num lobo com a ficha dele, Esc voltando) e com a comitiva.
- **O retrato do mercador** cabe sem mudar a altura do balcão (a primeira versão tirava 10 px da lista de produtos em
  1280×720; agora são os mesmos 214 px de antes).
- **Fumaça** (`tests/navegador/fumaca.mjs`): 356 conferências, tudo certo, na padrão e com `HUD=experimental`. Na
  experimental, o servidor de teste registrou uma exceção ao atender um pedido no fim do último cenário, quando o
  navegador fecha (o rastro se perdeu com o encerramento do processo); não se repetiu nas conferências e não derrubou
  nenhuma delas. Testes, gabarito e pyflakes iguais.
- **Resolvidos da rodada anterior:** a faixa da mira cobrindo a carta de cima e a barra de experiência com o fio de
  produção (os dois estavam nas lacunas de layout).
- **Não conferido:** o som; densidade 2 (as peças do teste de arte têm a versão ×2 para ela, mas as capturas são em
  densidade 1); o jogo inteiro de ponta a ponta à mão.

**Como ver (PowerShell, na pasta do jogo):**

```powershell
git pull
python jogar.py --hud-experimental
```

Com o jogo aberto: **Ctrl+Alt+S** troca a superfície (atual → mais escura → mais escura com transição) e **Ctrl+Alt+A**
liga e desliga o teste de arte; um aviso curto no pé da tela diz o que ficou. Para cair direto numa situação:

```powershell
$env:HUD = "experimental"
python -m tests.navegador.cenarios vila         # mercado (o mercador no balcão), taverna, templo, forja, mural
python -m tests.navegador.cenarios baus         # três baús na bolsa (o baú novo)
$env:ETAPA = "ossuario"; $env:SALA = "sacristia"; $env:BAU = "1"; $env:NIVEL = "6"
python -m tests.navegador.cenarios capela       # a sacristia com o baú no canto
Remove-Item Env:ETAPA, Env:SALA, Env:BAU, Env:NIVEL
python -m tests.navegador.cenarios broquel      # luta contra três lobos: a mira no vão
Remove-Item Env:HUD                             # volta à interface padrão
```

O endereço que o cenário mostra aceita `&superficie=escura` (ou `escura-transicao`) e `&arte=jogo` no fim, para abrir
já numa das comparações. Os pares do teste de arte: abra `ferramentas\prototipos\hud\arte-teste.html` no navegador.

### Proposta guardada: retratos do herói por classe

Registrada em `docs/ROADMAP.md` (ideias guardadas): uma seleção pequena, de início dois retratos por classe, escolhida
na criação, só cosmética. Nada implementado: nem a tela de escolha, nem recoloração, nem retratos por especialização.

## Depois da aprovação: a HUD de ferro é a interface padrão (1.89.0)

Jean aprovou a HUD para substituir a interface principal, com a superfície "mais escura" (sem a transição). Ela foi
migrada para a estrutura normal do jogo e esta pasta fica como **histórico**: o jogo não carrega mais nada daqui, a
opção `--hud-experimental` e o `HUD=experimental` dos cenários saíram, e `jogo/` (ligar.js, papeis.js, materiais.js,
as folhas de teste) não é mais servido. Onde cada coisa foi parar:

| No protótipo | No jogo |
|---|---|
| hud3 a hud4p, jogo/jogo.css, jogo/telas.css, superfície escura | `rpg/web/static/css/14-hud.css`, `16-hud-telas.css` (camadas consolidadas, sem as regras só do protótipo nem as que eram sobrepostas) |
| hud4p-luta.css | `rpg/web/static/css/15-hud-luta.css` |
| jogo/materiais.js | `Sprites.publicar()` pinta os materiais em ferro (o protótipo chama `Sprites.publicar({ bronze: true })` e segue com o bronze das versões anteriores) |
| jogo/papeis.js e icones.js (Icones4p) | `rpg/web/static/icones.js`: as telas pedem o desenho pelo papel (sem observar a página) |
| assets/, assets3/, assets4p/exibicao/ | `rpg/web/static/hud/` (moldura, texturas, barras) e `hud/icones/` (a família de ferro) |
| arte-teste.js (mercador) | o busto do mercador em `telas/mercado.js`, com as cores da figura da banca |
| arte-teste.js (baú de ferro) | não migrado: o Baú Trancado segue o baú de madeira e latão da família |

Ajustes da migração: a doca um pouco mais escura; as barras do topo até 400 px e, na janela larga, o retrato, as
barras e os recursos juntos no meio da coluna; a animação de equipar e o selo de atributo com o mesmo desenho da
origem e do destino. Detalhes em `docs/ARQUITETURA.md` ("A interface web").

Capturas da migração, tiradas do jogo de verdade (`capturas-migracao/`): `topo-larga.png` (a barra do topo em
1280×720, 1500×950, 1920×1080 e 2560×1440: o grupo das barras para em 400 px e fica no meio com o retrato e os
recursos), `janela-*.png` (a página inteira nesses tamanhos), `doca-estados.png` (normal, mouse, pressionado, tela
aberta, foco de teclado), `mercado-*.png` (com o mercador, mouse e foco), `equipar-achado-*.png` (o voo de "Equipar
agora" quadro a quadro, também com movimento reduzido), `equipar-guardar-e-mochila-1500x950.png` (guardar, e o clique
duplo na mochila, que veste sem voo, como antes) e `baus-*.png` (o baú marrom na bolsa e no relatório).
