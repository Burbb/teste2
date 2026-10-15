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

Correção da 1.89.1: na janela larga, o retrato, as barras e os recursos encostam no começo da coluna (12 px, o recuo
do topo), e a sobra fica à direita, em vez de ficarem no meio. As barras continuam em até 400 px. Capturas:
`capturas-migracao/topo-alinhado-1920x1080.png` (a janela maximizada) e `topo-alinhado-classes.png` (Guerreiro, Mago
e Arqueiro em 1280×720, 1920×1080 e 2560×1440).

## Teste do retrato: o Guerreiro de capacete fechado (experimento, sem versão)

Jean escolheu a direção do primeiro retrato no estilo do mundo: o Guerreiro de capacete fechado, sem rosto. Um
candidato só, para avaliação, no protótipo; o retrato de produção (`rpg/web/static/hud/icones/`) não mudou.

**O desenho** (`arte-teste.js`, peças `guerreiro` e `guerreiro-carta`, pelo método do mercador e das cenas: uma grade
de letras, cada letra uma cor, cada pixel da arte um quadrado inteiro da tela):

- Capacete fechado de ferro: a calota arredondada, a cruz de reforço (a tira do meio e a de cima da fresta), a fresta
  da viseira em duas aberturas, a borda de baixo na sombra e um amassado na calota (o desgaste). Nenhum olho, pele ou
  rosto. Uma primeira versão tinha três furos de respirar na face; juntos com a fresta, pareciam um rostinho, e saíram.
- A gola alta de gibão, a capa de lã nos ombros (as bordas marcadas no V) e a correia da espada atravessando o peito.
- As cores do mundo: o ferro com os cinzas do baú e da capela, o gibão com os da túnica do mercador, a capa num
  azul-acinzentado perto da do retrato de hoje. Luz da esquerda (como a lamparina da banca), em poucos planos: o
  plano da luz com um filete de brilho, a frente, o plano da sombra e a borda. Sem contorno claro: o tom mais escuro só
  na fresta e embaixo do capacete, e o capacete fica em cinzas médios, legível no carvão.

**Os tamanhos**, todos de um desenho só de 40×40, sempre a ×2 (nada reamostrado): o busto da ficha é ele inteiro
(80 px); o da janela baixa (64 px) e a cabeça do topo (48 px) são recortes dele (32×32 e 24×24). A carta da luta
(32 px) tem a versão de 16×16, redesenhada com a mesma silhueta (calota, cruz, fresta, gola, correia) e sem o amassado,
que lá vira um ponto parecido com um olho.

**Para ver:** `retrato-teste.html` (ampliado, os tamanhos reais ao lado do retrato de hoje e as fotografias do jogo).
As fotografias (`capturas-retrato/`) são do jogo de verdade, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_retrato.mjs`: a capela
(ficha e topo ao lado da sala), a banca do mercado (com o busto do mercador logo abaixo) e uma luta (a carta), em
janela normal (1500×950) e baixa (1280×720), com o retrato de hoje e com o candidato. O candidato entra só na página
fotografada (`retrato-no-jogo.js`, que troca as três imagens nos mesmos lugares e com as mesmas classes).

**Avaliação:**

- *Mesmo mundo:* sim, mais do que o retrato gerado. Ao lado da sala da capela, da banca e do busto do mercador, tem a
  mesma linguagem: formas chapadas, poucos tons, a luz de um lado só. Fica mais simples que os ícones de ferro da
  ficha (o elmo do equipamento, logo abaixo, tem mais tons); a diferença é de família (cenário × ícone), não de mundo.
- *Pequeno:* reconhecível em todos. Na carta (32 px; 36 na vez do herói, quando ela cresce) a calota, a cruz e a fresta
  continuam lá; no topo (48 px) o capacete ocupa a moldura inteira.
- *Acabamento:* sem corte, sem sobreposição, sem erro no console nas seis fotografias; as medidas são as do jogo
  (ficha 80 e 64, topo 48, carta 32). A carta do herói na vez dele é ampliada 1,125× pelo jogo e os pixels ficam
  levemente desiguais, como já acontece com o retrato de hoje.
- *Para decidir:* no busto, o capacete ocupa metade da largura e a capa ocupa o resto; se o capacete tiver de ser o
  centro maior, o desenho cresce (e a cabeça do topo passa a ser um recorte menos folgado). A capa é lisa de propósito
  (sem textura miúda); se parecer vazia, uma dobra ou uma borda a mais resolve sem mudar a direção.

Nada implementado além disso: nem seleção de retratos, nem recoloração, nem diferenças por gênero, nem as outras
classes, nem troca pelo elmo equipado. A proposta guardada (`docs/ROADMAP.md`, ideias) registra a direção.

**Aprovado (1.90.0):** o candidato foi para o jogo como está, em `rpg/web/static/retratos.js` (as mesmas grades, sem
detalhe a mais), pintado por `Sprites.grade`; os PNG do retrato gerado saíram de `hud/icones/` (as cópias continuam em
`assets4p/exibicao/`, e `retrato-teste.html` passou a apontar para elas).

## Teste dos retratos: Mago e Arqueiro, junto do Guerreiro aprovado (experimento, sem versão)

Com o Guerreiro de capacete fechado aprovado (no jogo desde a 1.90.0), um candidato para cada uma das outras classes
básicas, só aqui: `arte-teste.js` ganhou as peças `mago` e `arqueiro` (40×40) com os recortes de 64 e 48 px e a carta
(16×16) de cada um. O mesmo método (uma grade de letras, cada letra uma cor, pintada pixel a pixel) e o mesmo
enquadramento do Guerreiro: a cabeça na mesma região, para os mesmos recortes servirem às três classes.

- **Mago:** capuz alto de pano azul apagado, com a ponta mole caída para trás; o manto do capuz nos ombros, em
  triângulo; o rosto na sombra do capuz, só a metade de baixo à luz da esquerda (sem olhos à mostra, sem chapéu, sem
  joia, sem brilho).
- **Arqueiro:** capuz curto e redondo de pano verde apagado, rente à cabeça, que acaba numa capinha nos ombros; o rosto
  à mostra; o gibão de couro marrom, uma correia só e a boca da aljava com duas penas curtas atrás do ombro direito (a
  silhueta fica torta de um lado, onde a do Mago é um triângulo e a do Guerreiro uma caixa).
- **A carta** de cada um é redesenhada em 16×16 (nada reduzido por suavização): o capuz, o rosto e, no Arqueiro, a
  aljava; conferida também a 36 px, a ampliação da vez do herói.

**Para ver:** `retratos-classes.html` (os três ampliados, nos tamanhos reais, e as fotografias do jogo). As fotografias
(`capturas-retratos-classes/`) são do jogo de verdade, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_retratos_classes.mjs`:
para cada classe, em 1500×950 e 1280×720, a ficha e o topo ao lado da capela e da vila (fotografias paradas) e a luta
(interações: a vez do herói, com a carta a 36 px, e a mira aberta pela tecla 1). Os candidatos entram só na página
fotografada (`retrato-no-jogo.js`, agora pela classe do herói).

**Avaliação:**

- *Classes distintas sem depender da cor:* sim, pela silhueta: a caixa do capacete, o triângulo do capuz alto e o
  capuz redondo com a aljava saindo de um lado. Em tons de cinza, as três continuam diferentes.
- *Peso semelhante:* próximo. O Guerreiro tem o cinza mais claro do capacete; o Mago é o mais escuro e mais de uma cor
  só (o azul do capuz e do manto); o Arqueiro tem o rosto e o couro mais quentes. O couro foi apagado uma vez para não
  pesar mais que os outros. Se o Mago parecer apagado demais ao lado dos outros dois, o próximo passo é clarear a borda
  do capuz, não acrescentar detalhe.
- *Sobre o carvão:* os três legíveis nos quatro tamanhos; o Mago depende da borda clara do capuz e do rosto.
- *Mesmo mundo:* sim; o mesmo método, poucos tons, a luz da esquerda, as cores contidas, junto do mercador e das
  figuras dos cenários.
- *Interações verificadas* (não só fotografias): a vez do herói chegou e a carta foi medida a 36 px nas seis lutas; a
  tecla 1 abriu a mira com o retrato no lugar; nenhum erro no console. As fichas, os topos e as páginas inteiras são
  fotografias paradas.

Nada mudou no jogo: os retratos de produção seguem o de `retratos.js` (o Guerreiro) e o desenho da classe (Mago e
Arqueiro). Nem seleção, nem recoloração, nem gênero, nem retratos por especialização, nem troca pelo equipamento.

**Aprovados (1.91.0):** o Mago e o Arqueiro foram para o jogo como estão, em `rpg/web/static/retratos.js` (as mesmas
grades). A carta de 16×16 de cada classe virou também a figura do herói na fogueira (`Icones.figura`).

## Teste da comitiva: Morel, Odette e Yara (experimento, sem versão)

Um candidato de cada companheiro, no método e no enquadramento dos heróis (`arte-teste.js`): o busto de 40×40, o recorte
da cabeça (24×24, a 48 px) e a versão de 16×16 (a carta). Em produção eles seguem com os sprites de sempre.

**O que serviu de referência** (o texto do jogo manda; o sprite antigo só onde o texto não diz nada):

- *Morel* (`rpg/eventos/comitiva.py`, `rpg/abertura.py`): "um homem grande", "cicatriz de orelha a orelha", "armadura
  remendada com pedaços de outras armaduras"; o cabelo castanho e a barba do sprite. Daí o tronco largo, as ombreiras
  de peças diferentes e a espada atravessada nas costas. A cicatriz é uma linha vermelho-escura que corta o rosto na
  diagonal: de orelha a orelha, na horizontal, a 40×40 lia como boca ou faixa.
- *Odette* (`rpg/eventos/comitiva.py`, `rpg/comitiva/catalogo.py`): clériga desertora, "roupas chamuscadas"
  ("chamuscadas, não queimadas"); a touca branca e o véu escuro do sprite. As queimaduras ficam nas pontas do véu e num
  ombro, em manchas, não numa linha (que lia como cinto). Sem a cruz, que só o sprite tinha. O rosário que ela usa no
  pescoço ficou de fora porque, num dos caminhos, ela o entrega ao herói, e o retrato é um só; se preferir, ele entra
  como um fio claro no peito.
- *Yara* (`rpg/caspar.py`, `rpg/eventos/comitiva.py`, `rpg/comitiva/catalogo.py`): "uma moça de cabelo sujo de lama",
  olhos castanhos ("castanhos de novo", depois da maldição); o vestido verde do sprite, em pano apagado. Sem o violeta
  nos olhos e no cabelo que o sprite tinha, que contradiz o texto. Cabelo solto e sem capuz, para não repetir o Mago e o
  Arqueiro.
- Nenhuma idade, roupa, símbolo ou acessório além disso. Uma diferença de nome que não é desta entrega: o catálogo
  chama Yara de "bruxa do pântano"; as cenas, de "bruxa do Charco".

**As peças** (`morel`, `morel-cabeca`, `morel-carta`, e o mesmo para `odette` e `yara`): o busto para uma ficha de
companheiro que venha a existir; a cabeça para a tela da Comitiva, o cartão da reação e a faixa de quem chega (48 px);
a carta para o painel e a luta (32 px) e para a fogueira (16 px).

**Proposta para a fogueira:** a fogueira desenha bustos de 16×16, não corpos inteiros, e o herói já usa a carta dele
(`Icones.figura`). A correspondência proposta é a mesma: a carta de 16×16 de cada companheiro vira a figura dele na
fogueira, no mesmo lugar e na mesma escala. Bastaria pôr os três em `retratos.js`; nada disso foi feito no jogo.

**Para ver:** `comitiva-teste.html` (ampliados com as referências, nos tamanhos reais ao lado dos três heróis, e as
fotografias do jogo). As fotografias (`capturas-comitiva/`, com `folha-fogueiras.png` e `folha-lutas.png` juntando os
pares) são do jogo de verdade, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_comitiva.mjs`: em 1500×950
e 1280×720, hoje e com os candidatos, a fogueira com cada herói (Morel e Odette, Yara no acampamento, Morel ferido), o
painel da comitiva, a tela da Comitiva (tecla C) e duas lutas (Morel e Odette; Yara e Morel). Os candidatos entram só
na página fotografada (`comitiva-no-jogo.js`).

**Avaliação:**

- *Identidade própria:* sim, pela silhueta antes da cor: Morel é o mais largo, de cabeça descoberta, barba e ombreiras
  desiguais; Odette é a forma fechada do véu com o oval claro da touca; Yara é o cabelo solto e escuro caindo nos
  ombros. Nenhum capuz, nenhuma paleta trocada de outro.
- *Os mesmos personagens em todos os tamanhos:* a 80 e a 48 px, sim. A 32 px a cicatriz do Morel some (fica a barba e
  a espada); a touca da Odette continua lendo. A 16 px, na fogueira, os três ficam mais escuros e com menos contraste
  que os sprites antigos (que tinham contorno claro): a Odette se reconhece pela touca, o Morel pela forma larga, a
  Yara é a mais apagada. Se for para a fogueira, o próximo passo é clarear o rosto e a borda do cabelo dela na carta,
  não acrescentar detalhe.
- *Ao lado dos heróis:* mesmo método, mesma luz da esquerda, cores contidas; os heróis têm o capacete e os capuzes,
  os companheiros o rosto à mostra, o que ajuda a separar quem é o jogador.
- *Nomes longos, vida, aprovação, ferimento:* "Bastian Morel" e "Irmã Odette" cabem nos cartões; a vida, a aprovação e
  o Morel ferido aparecem como hoje (o retrato não toca nisso).
- *Foco do teclado:* os cartões da tela da Comitiva não recebem foco (já é assim em produção; o Tab vai para a doca).
  Não mexi; fica anotado.
- *Interações verificadas:* a tela da Comitiva aberta pela tecla C, o Tab, o Acampar até a fogueira, as lutas até a
  vez do herói; nenhum erro no console. As fichas, os painéis e as fogueiras são fotografias paradas.

Nada mudou no jogo nem nas regras da comitiva.

### Revisão dos três (segunda versão, experimento, sem versão)

Jean gostou da base e pediu só alguns traços; enquadramento, roupas e estilo ficaram. A primeira versão está guardada em
`comitiva-v1.js` (as peças `<nome>-v1`), para a comparação; as fotografias dela ficaram em `capturas-comitiva/` com
`v1` no nome.

- *Yara:* o cabelo ganhou silhueta própria. De um lado (o esquerdo de quem olha), solto, irregular, mais comprido, com
  três mechas grudadas pela lama (faixas barrentas que descem juntas, não pontos); do outro, puxado para trás da orelha
  (a orelha aparece) e preso num nó atrás da cabeça, com uma ponta curta descendo atrás do pescoço. A pedido de Jean,
  o cabelo é roxo apagado, como no sprite antigo: a cor vira o traço dela, e a lama continua barrenta por cima (o texto
  não diz a cor do cabelo; os olhos seguem castanhos, como o texto diz). Olhos castanhos, sem brilho, joia nem chapéu. A erva na gola foi
  testada e descartada: a 40×40 lia como broche (pareceria joia) e sumia a 48 e 32 px
  (`capturas-comitiva/proposta-erva-yara.png`).
- *Odette:* a pequena cruz amarela do sprite voltou ao peito, em amarelo envelhecido (dois tons), abaixo da touca; na
  carta, uma cruz de 3×3 no mesmo lugar. As manchas soltas do chamuscado saíram; a queimadura passou a ser a borda do
  véu roída e escurecida num ombro, uma forma só, na borda. O rosário continua fora.
- *Morel:* a cicatriz primeiro virou uma linha fina de orelha a orelha por baixo do nariz, mas ainda parecia um traço
  estranho para quem não sabe que é cicatriz. A pedido de Jean, é um corte na diagonal, da linha do cabelo até a
  barba, cortando a sobrancelha e o nariz, num tom de pele repuxada (mais claro e rosado); na carta, três pixels em
  diagonal. O texto ("de orelha a orelha") não mudou: o desenho deixou de segui-lo ao pé da letra; se quiser, a frase
  se ajusta depois. A espada foi
  redesenhada num eixo só, longe do rosto: pomo, empunhadura enfaixada, guarda atravessada e a lâmina sumindo atrás da
  ombreira; na carta, o mesmo em miniatura (pomo, cabo, guarda, lâmina). Os remendos soltos no pano e os rebites das
  ombreiras saíram (liam como sujeira); a armadura remendada continua nas duas ombreiras diferentes.

**Conferência:** `comitiva-teste.html` mostra v1 × revisão ampliados, nos tamanhos reais (busto 80, cabeça 48, carta
32, fogueira 16) com os heróis na mesma régua, a fogueira (hoje × v1 × revisão, de perto e inteira, com cada herói), a
tela da Comitiva e as lutas. Na luta, o companheiro não tem vez própria (a ampliação de 36 px é só do herói): a
fotografia é do passo à frente dele, quando a carta avança com a borda acesa (as animações param para a fotografia).

**Avaliação:**

- *Yara:* deixou de ser genérica; a assimetria do cabelo e o nó leem a 80 e 48 px, e a 32 px ainda se vê o lado solto
  contra o lado preso. Na fogueira ela continua a figura mais escura (está longe do fogo, e a cena escurece com a
  distância), mas o cabelo roxo agora se separa do fundo e a distingue dos outros dois. Não mexi na luz da cena.
- *Odette:* a cruz se lê em todos os tamanhos sem dominar (na fogueira é um ponto amarelo no peito). A borda queimada é
  discreta: some abaixo de 48 px, o que é aceitável; se ainda parecer sujeira, sai.
- *Morel:* a cicatriz agora se lê como cicatriz (o corte atravessa a sobrancelha); a espada tem forma de espada a 80 px e a 32 px.
  Continua reconhecível pela barba, o porte e as ombreiras diferentes.
- *Interações verificadas:* tela da Comitiva (tecla C e Tab), Acampar até a fogueira, a vez do herói, o ataque pela
  tecla 1 com o alvo e o passo à frente de um companheiro; nenhum erro no console. O jogo não mudou.

## Experimento de resolução: martelo, Pena de Fênix e Morel 80×80 (experimento, sem versão)

Antes de integrar a comitiva e fazer o lote de itens: outra resolução melhora a apresentação sem sair da linguagem dos
cenários? Três amostras desenhadas em código (`resolucao-teste.js`), cada uma nas duas resoluções nativas; nada foi
ampliado ou reduzido para virar a outra.

- **Martelo** (`martelo-32`, `martelo-64`; itens.py: "Martelo", arma do Guerreiro, de Ferro/Aço...): na diagonal como a
  maça e a espada aprovadas, cabo de madeira, cabeça de ferro atravessada, colar e pomo de latão, empunhadura de couro;
  luz de cima-esquerda. O de 64 acrescenta a cinta que prende a cabeça ao cabo, os dois anéis do colar, um veio na
  madeira e o brilho do pomo; a aresta acesa e o contorno continuam de 1 pixel.
- **Pena de Fênix** (`pena-32`, `pena-64`; "Revive você com metade da vida", "arde em chamas douradas"): pena de voo
  curva, cálamo marfim, do vermelho fundo da base ao dourado da ponta, a cor correndo pelas barbas (as faixas em ponta
  de flecha, não cortes retos). O de 64 tem uma falha a mais na borda e a borda do lado da luz um tom abaixo.
- **Morel 80×80** (`morel-80`, com `morel-80-baixo` de 64, `morel-80-cabeca` de 48 e a carta própria `morel-80-carta`
  de 32×32): o aprovado ampliado por Scale2x (as diagonais em degrau de 1 pixel, sem suavizar) e redesenhado onde a
  resolução ajuda: a cicatriz de 1 pixel com a borda afundada, as sobrancelhas carregadas descendo para o nariz (a cara
  fechada), os olhos fundos, o nariz, a boca no meio da barba, duas mechas da barba, a aresta das ombreiras e a junta das
  placas, a guarda acesa. Mesmo enquadramento, roupa, espada e cicatriz. Odette e Yara não mudaram.

**Para ver:** `resolucao-teste.html`. Os botões trocam no mesmo lugar o desenho dos itens (32×32 ou 64×64) e o Morel
(40×40 a 2× ou 80×80 a 1×); cada quadro diz a resolução nativa e o tamanho exibido. Itens em espaços de 32 e de 64 px
ao lado dos ícones aprovados, ampliados com os pixels à vista (e o de 64 reduzido a 32 pelo navegador), o Morel nos
espaços de 80, 64, 48, 32 e 36 px, e as fotografias do jogo. As fotografias (`capturas-resolucao/`) são do jogo de
verdade, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_resolucao.mjs`: capela
(ficha e topo), mercado (a pena na bolsa e na prateleira, os martelos na mochila da aba Vender; o cenário `mercado` ganhou
`AMOSTRAS=1`, que põe um Martelo e uma Pena de Fênix) e luta (a carta na vez), em 1500×950 e 1280×720, nas versões
`atual` (32 e 40) e `maior` (64 e 80). O Morel ocupa o lugar do retrato do herói (não há ficha de companheiro); as
amostras entram só na página fotografada (`resolucao-no-jogo.js`).

**O custo de reduzir o de 64 a 32** (o navegador, pixel a pixel, sem suavizar; contado na grade):

- *Martelo:* o contorno sobra em 16 de 63 pixels da borda (no desenho de 32, em 61 de 61): o cabo fica sem contorno
  quase todo e se separa do fundo pela cor só. A aresta acesa da cabeça cai de 29 para 8 pixels, em pontos soltos; a
  cinta e os anéis do colar ficam em pixels avulsos.
- *Pena:* a raque e o cálamo caem de 89 para 23 pixels claros e afinam para 1 pixel na diagonal, que lê como
  pontilhado (no desenho de 32 são 43, com 2 pixels de largura); as falhas da borda viram dentes isolados; o contorno
  sobra em 44 de 55.
- Conclusão: um desenho de 64 não serve de ícone de 32. Se houver apresentação em 64, são dois desenhos.

**Avaliação:**

- *Reconhecimento rápido* (no tamanho de uso): nos espaços de 32, o desenho de 32 ganha (o contorno inteiro, a forma
  limpa); o de 64 reduzido lê como o mesmo objeto, mas mais fraco e sujo. Nos de 64, o desenho de 64 é mais limpo que o
  de 32 a 2× (as diagonais em degrau de 1 pixel), mas a diferença de reconhecimento é pequena. O Morel é reconhecido
  igual nas duas versões em todos os espaços: quem carrega a identidade é a silhueta, a barba, a cicatriz e as cores.
- *Leitura de detalhe e expressão:* é onde o 80×80 ganha. Na ficha (80) e na ficha baixa (64), a cara fechada, a boca e
  a cicatriz fina leem melhor; na cabeça (48) o ganho diminui; na carta, a de 32×32 própria mostra a cicatriz e as
  sobrancelhas que a de 16×16 não tem espaço para mostrar. Nos itens, o detalhe a mais do 64 (cinta, anéis, veio, falha)
  só aparece em 64 e não muda o que o objeto é.
- *O mesmo mundo:* os cenários (capela, mercado) são desenhados com pixels de 2 a 3 px na tela, e o Morel de 40×40 a 2×
  tem o pixel do mesmo tamanho. O de 80×80 a 1× tem pixels com metade do tamanho de tudo em volta: ainda parece o mesmo
  personagem e o mesmo mundo (poucos tons, poucos planos de luz, nada de textura nas áreas grandes), mas fica mais fino
  que a cena ao lado. Nos itens a questão não existe: os ícones aprovados já são de 1 pixel por pixel de tela, em 32 e
  em 64, e as amostras de 32 e de 64 ficam na mesma densidade deles. As amostras são mais simples que os ícones
  aprovados (menos brilho e volume); isso é o desenho, não a resolução.
- *Custo:* o 80×80 dá quatro vezes mais pixels para decidir e pede as versões menores próprias (a carta de 32×32 teve
  de ser redesenhada; os recortes de 64 e 48 funcionam como recortes). Nos itens, dois desenhos por item se houver
  apresentação em 64.
- *Estático × interação:* as fotografias são paradas (a página do mercado, a aba Vender, a capela, a vez do herói na
  luta); nenhum erro no console.

**Recomendação:** itens nascem em 32×32, que é onde vivem (bolsa, mochila, mercado); uma versão de 64×64 só para os que
tiverem apresentação grande, desenhada à parte, nunca reduzida para 32. Retratos continuam no mestre de 40×40 a 2×,
que tem o pixel dos cenários; do 80×80 vale trazer para o 40×40 o que dá expressão sem mudar a resolução (as
sobrancelhas descendo para o nariz, a boca marcada), e para a carta de 32 px um desenho próprio de 32×32, que mostra a
cicatriz e a cara fechada. Nada mudou no jogo.

### Segunda rodada: a carta pequena do Morel e a espada (experimento, sem versão)

Decisões de Jean: os itens de 32×32 são a base da bolsa, da mochila e do mercado; o Morel de 80×80 é o candidato da
apresentação grande; a cabeça e a carta pedem adaptação própria. "Nunca reduzir uma imagem maior" não vira regra
geral: neste experimento, os desenhos próprios de 32 leram melhor. As versões anteriores ficam em `morel-anterior.js`
(`morel-ant…`, `morel-80-ant…`) para a comparação.

**A carta parecia comprimida: componente ou desenho?** Medido no jogo (`capturas-carta/medidas.json`): a imagem da
carta é quadrada, 32×32, no nicho de 36 px, sem recorte nem proporção torta. O que muda o tamanho é a vez do herói: o
jogo amplia a carta inteira 1,12× (`.carta.foco`), e o rosto de 32 px vira 35,84 px, com pixels de 1 ou 2 de espessura
(`capturas-carta/nitidez-36.png`); as cores não se misturam (23 cores na captura, as do desenho). O aperto do rosto é
do desenho: o enquadramento da carta pegava peito, ombreiras e espada, e o rosto ficava com 8 a 12 pixels de altura
para sobrancelha, olho, cicatriz, nariz, bigode e boca.

**A carta nova** (`morel-80-carta`, nativa de 32×32): perto da cabeça (o rosto ocupa as linhas 2 a 23), menos peito,
ombreira e espada (só o punho atrás do ombro). Cada traço com folga: sobrancelha (linhas 9 e 10), pálpebra (11), olho
(12), nariz (12 a 16), bigode (17 e 18), boca (19), barba até o queixo (23). A cara fechada pelas sobrancelhas descendo
para o nariz; a cicatriz só sugerida, quatro pixels na testa e na sobrancelha e dois na bochecha do outro lado. As
cores e os traços do 80×80; nenhum contorno claro.

**A redução do 40×40 a 32** (`morel-40-32`, o vizinho mais perto, como o navegador): o mesmo enquadramento largo, o
rosto ainda menor que na carta anterior e a cicatriz em degraus irregulares. Fica como comparação; não é candidata.

**32 ou 36 px.** Só a carta do herói passa pela ampliação: o foco é dele (`Batalha.foco("j")`). A carta do Morel
companheiro mede 32 px sempre, nas duas janelas, e não recebe foco; ali não há o que corrigir. Os 36 px do Morel nas
fotografias existem só porque o teste o põe no lugar do herói. Para o herói, o teste mantém o rosto em 32 px inteiros
dentro da carta ampliada (só neste protótipo, `resolucao-no-jogo.js` com `inteiro`: o rosto desfaz a ampliação, a
moldura, o nome e as barras continuam com o destaque): todos os pixels iguais, nas duas janelas, com movimento normal e
reduzido; a tecla 1 continua abrindo a mira, e o foco, a seleção e as áreas clicáveis não mudam. A posição na tela fica
fracionada (x = 354,52), o que não borra (as mesmas cores) mas desloca o desenho meio pixel; se for para a produção,
vale alinhar o nicho ao pixel inteiro. Nada mudou nas animações do jogo.

**A cabeça e a ficha baixa.** A cabeça de 48 px é o mesmo recorte do 80×80, sem os pedaços da guarda que entravam pela
borda (liam como um traço solto). A ficha baixa de 64 px desceu o recorte 4 pixels para a esquerda: a espada aparece
inteira (o pomo perde 2 pixels) em vez de cortada no meio, e o rosto fica 4 pixels à direita do centro.

**A espada do Morel, refeita em todas as artes** (40×40 e as cartas em `arte-teste.js`, 80×80 em `resolucao-teste.js`):
encaixada nas costas, uma reta numa leve diagonal, o pomo para fora e para cima, 1 pixel de degrau a cada 3 linhas (no
80×80, a cada 3 linhas também, com o dobro da largura), a empunhadura com largura constante e as voltas do couro em
faixas regulares (antes o degrau ia e voltava, em zigue-zague), a guarda de través apoiada na ombreira e a lâmina
sumindo atrás dela. Na carta de 16×16 (a figura da fogueira), o mesmo em miniatura.

**Ao lado dos outros.** Nos mesmos espaços (80, 48, 32), o Morel de 80×80 tem o pixel com metade do tamanho do de
Odette, Yara e dos heróis (40×40 a 2×): a diferença aparece no retrato grande, nas mechas da barba, na cicatriz fina e
nas arestas das ombreiras, e quase some na cabeça e na carta. Não incomoda na ficha, que mostra um retrato por vez; vai
aparecer onde houver dois retratos grandes lado a lado (uma ficha da comitiva, por exemplo). Os outros não foram
redesenhados.

**Os itens escolhidos.** O martelo e a Pena de Fênix de 32×32, em tamanho real, ao lado da espada, do anel e do baú
atuais (`resolucao-teste.html`). Nenhum outro item nem versão grande.

**Para ver:** a primeira seção de `resolucao-teste.html` (as quatro cartas em 32 px e ampliadas; a carta no jogo em
36 e em 32 px; a do companheiro; o conjunto novo e o anterior; os vizinhos; a ficha e o topo na capela; os itens).
As fotografias (`capturas-carta/`) são do jogo de verdade, a mesma luta e os mesmos dados para todas as versões,
refeitas com `PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_carta.mjs`.
O jogo não mudou: a comitiva e os itens continuam fora da produção, e o ajuste do texto da cicatriz, já autorizado,
fica para a integração.

## O padrão das cartas de combate: os três heróis e os três companheiros (experimento, sem versão)

**A referência** é o Morel "40 reduzido a 32": o busto aprovado de 40×40 inteiro, reduzido a 32 px. A carta nativa de
32×32 com o rosto aproximado foi rejeitada e fica só no histórico (`resolucao-teste.html` e o fim de
`cartas-teste.html`).

**O padrão (para os seis e para personagens futuros):** a carta de combate mostra 32 px de retrato com a cabeça e parte
dos ombros, nas proporções do busto (a cabeça ocupa mais ou menos a metade de cima, os ombros enchem a largura de
baixo), sem rosto aumentado para caber olho, cicatriz ou detalhe: quem identifica é o conjunto (silhueta, cor, o
traço principal). Peso parecido entre os personagens e a borda visível sobre o fundo escuro do nicho (`#0a0b0d`). O
padrão é de apresentação, não de método: aqui saiu da redução do busto, mas um personagem futuro pode ter a carta
desenhada à mão, desde que caia nesse enquadramento.

**Como os seis chegaram nele** (`cartas-teste.js`, as peças `<nome>-c32`): o busto aprovado de cada um reduzido a 32
pelo vizinho mais perto, como foi feito com o Morel, e ajuste pontual só onde a redução apagou um traço que identifica.
A redução de 40 para 32 tira uma linha e uma coluna a cada cinco, e alguns traços caíram exatamente nelas:

- *Guerreiro:* a fenda do visor (a linha 12 do busto) sumia; volta no lugar da linha lisa de cima dela.
- *Odette:* o braço de cima da cruz e os dois olhos (as colunas 17 e 22) sumiam; voltam no lugar correspondente, do
  mesmo tamanho. A borda dela tinha metade do contraste dos outros sobre o fundo da carta (o véu quase preto); na
  carta, os quatro tons do véu sobem um degrau, na mesma ordem (o contraste médio da borda vai de 1,52 para 1,79; os
  outros ficam entre 2,1 e 3,3).
- *Yara:* os dois olhos caíam nas mesmas colunas da Odette; voltam do mesmo jeito.
- *Mago, Arqueiro:* a redução direta já servia. *Morel:* a referência, sem mudança.

O que identifica cada um continua: o capacete fechado com o visor, o capuz azul alto e fundo, o capuz verde curto com a
aljava, a barba, a cicatriz e a espada nas costas, a touca branca com a cruz amarela, o cabelo roxo assimétrico.

**No jogo** (`capturas-cartas/`, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_cartas.mjs`): três
composições (o Guerreiro com Morel e Odette, o Mago com Yara e Morel, o Arqueiro com Odette e Yara), a anterior e a
candidata, em 1500×950 e 1280×720, com movimento normal e reduzido, na vez do herói, com nome, vida e recurso nas
cartas. As cartas entram só na página fotografada (`cartas-no-jogo.js`).

**O herói em foco.** O jogo amplia a carta do herói 1,12× na vez dele. Neste teste o nicho (a moldura de 36 px e o rosto
de 32) desfaz a ampliação e é alinhado ao pixel inteiro da tela, enquanto o nome, as barras e a borda da carta continuam
ampliados; usa as propriedades `scale` e `translate`, que não brigam com as animações da carta (que usam `transform`).
Medido nas 24 fotografias: o nicho e o rosto em posições inteiras, com 36 e 32 px; a tecla 1 abre a mira e o Esc volta
à roda em todas. Os companheiros não recebem foco e ficam sempre em 32 px. Achado à parte: a carta deles cai em meio
pixel na vertical em parte das janelas (y = 166,5), já no jogo de hoje; como o desenho é pixel a pixel, não mistura
cores (conferido na captura), só desloca. Não mexi.

**Avaliação no tamanho real:**

- *Legíveis e proporcionais:* sim. Os seis leem como busto (cabeça e ombros), sem cabeça grande; o Guerreiro e o Mago
  pela silhueta, o Arqueiro pelo capuz e a aljava, o Morel pela barba e a ombreira, a Odette pela touca e a cruz, a
  Yara pelo cabelo roxo. As cartas anteriores (16×16 a 2×) tinham a cabeça enchendo o nicho e pixels de 2 px; as
  candidatas têm o pixel de 1 px, o mesmo dos ícones da HUD ao lado.
- *Consistentes entre si:* o enquadramento é o mesmo (todos vêm de bustos do mesmo tamanho). O Mago e a Yara são os
  mais escuros; o Guerreiro (o aço) e a Odette (a touca branca) os mais claros, sem destoar no conjunto.
- *Na luta:* o rosto do herói em foco fica nítido e do mesmo tamanho dos companheiros; nas três composições as cartas
  de cima e de baixo têm o mesmo peso.

**Decisões já tomadas, registradas aqui para a integração:** o Morel grande em 80×80; a carta dele, "40 reduzido a
32"; Odette e Yara revisadas aprovadas; o ajuste do texto da cicatriz autorizado; o martelo e a Pena de Fênix de 32×32
escolhidos. Nada disso entrou no jogo ainda. Não mudaram nesta rodada os retratos grandes, o topo, o Inventário nem as
figuras da fogueira.

**Para ver:** `cartas-teste.html`.

## Integrados (1.92.0): a comitiva no jogo e a escolha final das cartas

**A escolha final das cartas de combate:** Guerreiro, Mago, Arqueiro, Odette e Yara com a carta de 16×16 a 2× (a
fileira "anterior" de `cartas-teste.html`); o Morel com o busto de 40×40 reduzido a 32 ("40 reduzido a 32"). Reduzir
todos os bustos deixou cabeças pequenas demais; a carta aproximada do Morel continua rejeitada. **Critério para os
próximos personagens:** coerência é leitura, identidade e peso visual compatíveis no tamanho em que a carta aparece;
não exige a mesma resolução de origem nem a mesma proporção entre cabeça e ombros.

**No jogo** (`rpg/web/static/retratos.js`, pelo `Icones`): Morel (busto 80×80, ficha baixa 64 e cabeça 48 já
adaptadas, a espada encaixada, a carta "40 reduzido a 32", a figura de 16×16 na fogueira), Odette (a revisada, com a
cruz e o véu roído) e Yara (o cabelo roxo assimétrico com lama, os olhos castanhos), em todos os lugares deles: o
painel da ficha, a tela da Comitiva, a carta e o cartão de reação na luta, a faixa de quem chega, o aviso, o chip de
aprovação no texto e a fogueira (as figuras de 16×16, na escala e no lugar de sempre). Os retratos grandes dos heróis
não mudaram. O texto do Morel diz agora "uma cicatriz atravessa o rosto dele".

**Conferência** (`capturas-integracao/`, refeitas com
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_integracao.mjs`, o jogo
sem nenhum arquivo do protótipo): os três heróis com pares diferentes (Guerreiro com Morel e Odette, Mago com Yara e
Morel, Arqueiro com Odette e Yara) em 1500×950 e 1280×720, com movimento normal e reduzido; o rosto do herói na vez
dele em 32 px no pixel inteiro em todas; a tecla 1 e o Esc; um companheiro avançando; o cartão de reação; o painel,
a tela da Comitiva, o aviso, a faixa e a fogueira com cada herói. Nenhuma imagem com o sprite antigo dos três em
nenhuma tela. O cartão de reação, a faixa e o aviso foram chamados direto (os componentes do jogo, com os dados de
verdade), porque nenhum cenário chega neles sem um caminho longo de escolhas.

**Achado, sem mexer:** com movimento reduzido, a faixa de celebração (quem se junta, vitória, mestre caçador) some na
hora: a regra de movimento reduzido encurta a animação para 0,001 ms e a faixa sai quando a animação acaba. Já era
assim antes desta entrega.

O martelo e a Pena de Fênix de 32×32 continuam guardados para o próximo lote de itens.

## Itens, ícones e acabamento da roda (experimento, sem versão)

Primeira etapa do plano de apresentação (`docs/ROADMAP.md`, "Apresentação e serviços"). Nada daqui está no jogo: os
candidatos esperam a avaliação do Jean.

**Os desenhos** (`desenhar_itens.py` → `itens-icones-teste.js`, gerado; não editar à mão): cada peça é uma função do
lado, montada com formas simples (traço grosso, disco, polígono) pintadas com as letras da paleta do martelo e da Pena
(ferro, madeira, latão, couro) e mais o que cada uma pede (barro, prata, fumaça, couro vermelho, folhas); o contorno
escuro de 1 pixel sai sozinho e a luz vem de cima e da esquerda. `python ferramentas/prototipos/hud/desenhar_itens.py
--png <pasta>` também faz a folha ampliada.
- **Machado** (a base "Machado" do Guerreiro): cabo de madeira na diagonal, como o martelo, punho de couro e a lâmina
  em meia-lua caindo para a direita, com o fio claro no arco e o talão atrás do cabo.
- **Unguento de Prata** ("Cura uma infecção"): o pote baixo de barro, de barriga larga, com o cordão no gargalo, a boca
  aberta e o unguento de prata em monte, com a espátula de madeira. Hoje é o sprite da curandeira.
- **Bomba de Fumaça** ("Garante a fuga de um combate"): a bola de barro escuro com a corda, o tampão de madeira, o
  pavio aceso e a fumaça clara saindo pela base (sem contorno escuro: com ele, os rolos viravam pedras). Hoje é a
  caveira, a mesma da morte e do bestiário.
- **Espada, escudo e anel** (candidatos no estilo do mundo, ao lado dos pintados da HUD): a espada reta com o sulco,
  guarda e pomo de latão e punho de couro; o escudo redondo de tábuas com o aro de ferro, cravos de latão e a bossa de
  ferro (o escudo de bico fica para a Defesa, e os dois deixam de se confundir); o sinete de latão com o selo gravado
  (sem pedra: nenhuma cor de raridade).
- **Grimório** (doca e Habilidades da roda, 32 e 36): o livro de couro vermelho-escuro com as folhas à mostra, cantos
  e fecho de latão (hoje, roxo com a pedra). **Talentos** (32 e 36): a árvore de madeira com três nós de latão (os
  ramos da árvore de talentos; hoje, só os três nós).
- **Ataque e Defesa** (ficha, 24 e 32): duas espadas cruzadas (hoje, a mesma espada do item) e o escudo de bico em dois
  planos com a borda de latão. **Fugir** (roda, 32): a bota em passo largo com a poeira e os rastros, sem o raio, que é
  da Agilidade (hoje, Fugir e Agilidade usam a mesma bota).

**A roda** (`roda-alternativa.css`): só cor, aresta e sombra; tamanhos, recuos, disposição, mira, fluxo e áreas
clicáveis são os de hoje. O que muda e por quê está no cabeçalho da folha (o mouse quase invisível, a tecla solta por
cima do canto do nicho, as placas mais claras que o carvão, o indisponível só apagado).

**Como fotografar** (o jogo não carrega nada daqui; os roteiros põem os arquivos na página):
`PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_itens_icones.mjs`
(ficha, doca, Inventário, Mercado, Itens na luta e perto da capela, atual × candidatos; o cenário `tutorial` com
`VITRINE=1`) e `.../fotografar_roda.mjs` (cada estado da roda: atual, com os ícones, com o acabamento). A comparação
está em `itens-icones-teste.html`.

**Fotografias** (`capturas-itens-icones/` e `capturas-roda/`, em 1500×950 e 1280×720): ficha, doca, Inventário,
Mercado do Vau, a roda com a janelinha de Itens e a tela inteira perto da Capela Afogada; a roda em sete estados
(parada, mouse, pressionada, Habilidades e Itens abertas, indisponível simulado, foco do teclado), atual, com os ícones
e com o acabamento. Ajustes feitos depois da primeira volta: o mouse da roda alternativa era fraco demais (agora a
placa clareia e corre um fio de latão de 2 px); a troca do unguento e da bomba precisava achar o item pelo id na
bolsa, na janelinha e no Mercado (o jogo usa os mesmos desenhos para a curandeira, a morte e o Largar).

**Avaliação** (a tabela inteira em `itens-icones-avaliacao.js`, nos seis critérios pedidos): integrar o machado, o
unguento, o escudo de madeira, o Grimório, os Talentos, o Ataque, o Fugir e o acabamento da roda; a bomba depois de
clarear a bola (some no nicho escuro); a espada candidata só se a família de equipamento inteira migrar para o estilo
dos cenários (sozinha, briga com o elmo, a cota e as botas pintados); o anel atual fica (o selo do candidato vira
mancha em 32 px e a silhueta do espaço vazio vira bolha); a Defesa nova é opcional, junto do escudo.

**Decisão do Jean (10/2026):** o lote não foi aprovado. Os desenhos atuais têm mais volume, personalidade e
acabamento; a aproximação com os cenários simplificou demais os itens. Ficam os itens e ícones atuais e a Pena de
Fênix; nenhum candidato é integrado. O acabamento alternativo da roda fica para uma avaliação separada. A direção dos
itens se ajusta antes de produzir outros: o próximo teste é um escudo só, com o atual como referência.

## Teste do escudo: o atual como referência (experimento, sem versão)

**O pedido:** uma alternativa ao escudo atual da HUD com o mesmo escudo (redondo, face de ferro azulado em gomos, aro
de latão, bossa de latão em cúpula, oito cravos), no mesmo enquadramento e no mesmo tamanho aparente, sem trocar
material nem acrescentar nada, buscando o volume e o acabamento: o aro com espessura, frente, borda e partes
salientes separadas, sombras que mostram a construção, reflexos de metal controlados e a silhueta no carvão. Sem
limitar tons nem resolução de origem; sem efeito no espaço para compensar o desenho.

**O processo** (`desenhar_escudo.py` → `escudo-teste/`, com os nomes e tamanhos do jogo): o escudo é um relevo (a
face em oito gomos planos misturados a uma cúpula rasa, o degrau antes do aro, o aro em rolo, o sulco e a base da
bossa, a cúpula, os cravos), iluminado como superfície (luz de cima-esquerda, difusa, especular, reflexo de ambiente
fraco, sombra projetada e oclusão nos sulcos), com a lateral do escudo embaixo e à direita, renderizado em 8× e
reduzido por média de área, cada tamanho à parte (sulcos, cravos e aro nunca menores que o pixel de cada um) e com um
contorno escuro de 1 pixel. Rodadas até a proposta: os gomos chapados viraram planos de luz; o reflexo de uma cunha
branca virou um gradiente dentro do gomo; o aro ganhou altura e a lateral; os cravos foram para junto do aro; a
bossa cresceu.

**Fotografias** (`fotografar_escudo.mjs` → `capturas-escudo/`, o jogo intacto: o roteiro responde aos pedidos de
`/static/hud/icones/escudo-*.png` com o candidato): ficha, Inventário, Mercado (Vender) em 32 px; voo ao equipar em
48; cartão do saque em 64; a tela inteira da vila e do Inventário; em 1500×950 e 1280×720. Na página
`itens-icones-teste.html`, a primeira seção.

**Avaliação** (`escudo-avaliacao.js`): o atual continua melhor em 32 px, o tamanho que mais aparece (lê mais limpo,
tem mais presença e conversa com a família pintada); o candidato ganha em 48 e 64 na construção (espessura e lateral
do aro, base e sombra da bossa, gomos como planos), mas a cúpula tem menos brilho e o conjunto parece de outra família.
Se a direção servir, o caminho é levar ao atual só o que lhe falta de perto, não trocar o escudo.

### O escudo refinado em pixel art (experimento, sem versão)

**O pedido:** continuar com o candidato do escudo e refinar a linguagem de pixel art: o candidato como referência de
construção, espessura e sombra, o atual como referência de presença dos reflexos e de contraste no pequeno; a luz,
a sombra e o contorno como grupos de pixels deliberados; cada tamanho (32, 48, 64) tratado na própria grade, sem
redução automática, quantização ou filtro de pixel como acabamento; paleta organizada, sem limite arbitrário.

**O processo** (`desenhar_escudo_pixel.py` → `escudo-pixel/`, com os nomes do jogo; o dobro é a duplicação exata):
regras na grade final, descritas no cabeçalho do arquivo, com as medidas de cada tamanho em `MEDIDAS` e as correções
manuais em `AJUSTES`. A silhueta são dois discos em centro de pixel (a frente e a lateral, 1 pixel embaixo e à
direita), no enquadramento do atual; o aro é um rolo por regras (o tom pelo ângulo até a luz, a fileira de fora e a de
dentro um degrau abaixo do lado em que viram, o brilho num arco curto); o degrau é a sombra do aro, com um toque da
parede acesa embaixo à direita; cada gomo da face tem um tom só (a `escada` de cada tamanho, em `MEDIDAS`), com o reflexo do gomo da luz em
três tons e as emendas só em 48 e 64; a peça central tem o sulco, a base (em 48 e 64), a cúpula em faixas e o brilho
desenhado por tamanho; os cravos são pinos por tamanho; uma limpeza tira pixels sozinhos; o contorno tem 1 pixel, só
pelos lados. Paleta: 9 tons de ferro, 9 de latão e o contorno (17 a 18 cores por arquivo).

**As rodadas** (cada uma olhando os três tamanhos e o jogo): o aro claro na volta toda virou tom médio com o brilho
num arco curto; a peça central diminuiu e, em 32, perdeu a base separada (fazia dentes); o reflexo do gomo foi para
depois das sombras (elas o apagavam) e cresceu; os cravos em cruz viraram cabeças redondas; a pedido do Jean, o canto
de baixo à direita, que somava parede, aro e lateral de 2 px, ficou com a lateral de 1 px e a parede só num toque;
e, numa segunda revisão (32 e 48 ainda pesavam), a lateral passou a se deslocar pela diagonal (1 px em x e 1 em y
davam 1,4 px na diagonal) e o toque da parede ficou só em 64: o canto fica 1 px mais grosso que o resto do aro. Por fim, o toque da parede saiu também de 64, onde
virava um risco solto por dentro do aro: o degrau é escuro a volta toda.

**Fotos** (`fotografar_escudo.mjs`, agora com as três versões; `VERSOES=refinado` refaz só uma): a ficha, o
Inventário e o Mercado em 32, o voo em 48, o cartão do saque em 64 e as telas inteiras, em 1500×950 e 1280×720.

**Avaliação** (`escudo-avaliacao.js`): o refinado ganha na organização dos pixels, na silhueta e na espessura, nos
reflexos localizados do aro e na leitura limpa em 32; perde para o atual no tamanho do reflexo do gomo (mais em 64)
e na face de 64, mais clara e chapada.

### O método em dois objetos: o escudo final e o Unguento de Prata (experimento, sem versão)

**O pedido:** encerrar o escudo com uma passagem curta de acabamento e testar o método num segundo objeto, o Unguento
de Prata, sem levar nada à produção.

**O escudo final** (`escudo-pixel/`; o aprovado antes da passagem fica em `escudo-pixel-v1/`): os gomos de trás um
degrau mais escuros em 48 e 64 (a `escada` passou a ser de cada tamanho: 32 `7,5,4,3,2`, 48 `7,5,4,3,1`, 64
`7,5,4,2,1`) e o reflexo do gomo da luz maior em 48 e 64 (`reflexo` e `alcance` em `MEDIDAS`). O 32 saiu igual ao
aprovado, pixel a pixel. Estrutura, enquadramento, paleta, aro, peça central e cravos não mudaram.

**O unguento** (`desenhar_unguento_pixel.py` → `unguento-pixel/`, 32 como prioridade, 48 e 64 como apresentação; o
dobro é a duplicação exata). Antes de desenhar, o que o jogo diz: "Unguento de Prata", "Cura uma infecção", 30 de ouro,
usado fora da luta ("O unguento arde como fogo. Horas depois, a febre cede"); nenhum brilho, símbolo ou efeito. A
identidade vem do sprite atual (um pote baixo de louça clara, de paredes retas, com tampa e um rótulo azul-esverdeado
com uma tira clara; é também o desenho da curandeira). A proposta guarda a louça, a forma e o rótulo e abre o pote:
a borda (o lábio em elipse, aceso atrás à esquerda, com a espessura na frente), a parede de dentro em sombra e a pasta
abaixo da borda. A primeira tentativa desta rodada seguiu o primeiro candidato (um pote de barro barrigudo) e perdia a
identidade do atual; foi descartada. Rodadas até a proposta: o corpo em muitas faixas verticais com um reflexo branco
lia como lata de metal (virou poucos tons largos e um reflexo de vidrado um degrau acima, sem branco); a pasta escura
e ruidosa lia como pedra (virou cinza frio com a luz em volta de um ponto); no tamanho real a pasta e a borda tinham o
mesmo valor e a boca sumia (a pasta desceu um degrau e mais da parede escura de dentro aparece). Rampas: louça (9
tons, o último é o reflexo), pasta de prata (8), rótulo (8) e papel (8); 24 cores por arquivo.

**O comum aos dois** (`pixel_comum.py`, que os dois usam): a luz (de cima e da esquerda, um pouco de frente), a grade
em duas camadas (material e tom) com o que é desenhado de propósito protegido, a limpeza de pixels sozinhos, o
contorno de 1 pixel só pelos lados, as correções manuais por tamanho (`AJUSTES`), a imagem pelas rampas e o @2x por
duplicação. O escudo foi refeito sobre ele sem mudar um pixel.

**O que foi de cada material:** o metal (ferro, latão) leva reflexo especular forte e localizado (o arco do aro, a
mancha do gomo, o ponto da cúpula) e vai do quase preto ao quase branco; a louça vidrada, a luz da forma em poucas
faixas largas e um reflexo baixo e estreito; o papel do rótulo, só a luz da forma (o reflexo para nele); a pasta, cinza
frio contra a louça quente, luz macia em volta de um ponto, nenhum especular. A quantidade de cores não é regra: o
escudo usa 17 a 18, o unguento 24.

**O que foi de cada tamanho:** no escudo, as emendas e a base da peça só em 48 e 64, os cravos por tamanho, a escada
e o reflexo por tamanho; no unguento, a espessura do lábio (1 px em 32, 2 em 48 e 64), o sulco do pescoço só em 48 e
64, a barriga só em 48 e 64 (em 32 virava um degrau solto na silhueta), o grupo de brilho da pasta desenhado por
tamanho, e a pasta mais funda em 32 (para a parede de dentro aparecer).

**Etapas reutilizáveis:** ler o que o jogo diz do objeto e o desenho atual antes de desenhar; montar a forma na grade
final por regras (as medidas de cada tamanho numa tabela); dar a cada material a sua rampa e a sua regra de luz;
conferir em 32 no tamanho real, no jogo, e não só ampliado; corrigir o que for de um tamanho na tabela ou em
`AJUSTES`; fotografar com o jogo intacto, trocando só os arquivos (`fotografar_escudo.mjs`,
`fotografar_unguento.mjs` com `unguento-no-jogo.js`). Ainda não é uma skill: o método foi provado em dois objetos.

**Fotos:** `fotografar_escudo.mjs` com `VERSOES=v1,refinado` (o anterior × o final: saque em 64, voo em 48,
Inventário, Mercado e ficha em 32, telas inteiras); `fotografar_unguento.mjs` → `capturas-unguento/` (atual, primeiro
candidato e proposta, esta com o escudo final: o Inventário, o Mercado em Suprimentos, a ficha e as telas inteiras),
em 1500×950 e 1280×720. Na página `itens-icones-teste.html`, a primeira seção, com a avaliação dos dois juntos
(`unguento-avaliacao.js`).

### O conceito novo do unguento e a ocupação dos ícones (experimento, sem versão)

**O escudo final** foi aprovado como referência; a revisão artística dele está encerrada (o desenho de 32, 48 e 64
não muda). Para o estudo abaixo, a tabela do brilho da cúpula saiu de dentro de `desenhar` para `BRILHO_CUPULA` (o
mesmo conteúdo; os seis arquivos saem idênticos), para um tamanho novo poder ser pedido de fora.

**O unguento, conceito novo** (`desenhar_unguento_pixel.py` → `unguento-pixel/`, 32 e 64 px; o pote de louça com
rótulo da rodada anterior ficou em `unguento-pixel-v1/`, e o código dele no commit 75cefb9). Decisão de Jean: as
paredes retas e o rótulo azul-esverdeado lembravam uma embalagem moderna; o recipiente passa a ser um pote de cerâmica
de boticário. A construção: uma forma de revolução (a barriga em superelipse, o pescoço curto, o fundo na elipse de
baixo), vista um pouco mais de cima que o pote anterior (K 0,44 em vez de 0,3: com 0,36, no tamanho real a pasta era
só uma faixa); o barro bege acinzentado e fosco em quatro faixas largas de luz, sem reflexo; o lábio grosso com o topo
aceso, a espessura na frente e a sombra no pescoço; a parede de dentro escura; a pasta de prata (a mesma rampa e a
mesma luz macia da rodada anterior) com a ponta de onde a espátula saiu. Rodadas: as faixas finas da luz liam como
veios (ficaram quatro, largas); a última linha do fundo acendia (a normal do fundo passou a ser a da linha do fundo);
um grupo de brilho no ombro lia como um cisco num material fosco (saiu). A tampa ao lado ficou de fora: o pote já
ocupa 27 dos 32 px e ela obrigaria a encolhê-lo. 14 cores por arquivo. Fotos: `fotografar_unguento.mjs`, agora com
quatro versões (atual, primeiro, anterior, conceito).

**A ocupação dos ícones no Inventário** (`ocupacao_icones.py` → `ocupacao/`, `ocupacao-no-jogo.js`,
`fotografar_ocupacao.mjs` → `capturas-ocupacao/`, cenário tutorial com `VITRINE=2`: o escudo, o anel e a armadura
vestidos, sem o machado). As quatro medidas, separadas: o espaço tem 60 px no corpo, 56 na mochila e 52 na bolsa; a
imagem exibida tem 32 px em todos (Icones.item pede 32 e a regra `.slot-px img.desenho` de `14-hud.css` fixa 32); o
desenho ocupa 27 a 30 px do arquivo; a margem transparente no arquivo é de 1 a 4 px. A folga nasce na exibição: um
desenho de 32 num espaço de 60 ocupa cerca de metade da largura. A alternativa (uma só) mostra o equipamento do corpo
e da mochila em 40 px, com arquivos nativos de 40: o anel, a cota e a espada pelo caminho dos tamanhos de hoje
(`preparar_hud4p.py`: as folhas aprovadas, a escala do grupo, a redução "paleta"; os de 32 e 48 desse caminho são iguais
aos do jogo), o escudo pelas regras dele com medidas entre as de 32 e 48 (uma prova de tamanho, sem acabamento). O
escudo passa de 48% a 62% da largura útil do espaço do corpo, o anel de 52% a 66%, a armadura de 47% a 59%. 44 px
foi olhado e descartado (o anel dominava e a mochila ficava justa). A bolsa, a doca, os atributos e a luta não mudam.

**Recomendação** (`ocupacao-recomendacao.js`, na página): adotar 40 px no corpo e na mochila. Comum à família: cada
tamanho de exibição com o seu arquivo nativo, o desenho usando o quadro (1 a 2 px de margem), a mesma luz, contorno e
rampas. Por objeto: a área ocupada dentro do quadro (as silhuetas diferentes ficam). Por contexto: o tamanho de
exibição, pelo tipo de espaço. Para adotar faltam os arquivos de 40 de todo o equipamento pintado, a passagem de
acabamento do escudo em 40 e uma decisão para os itens que ainda são sprites 16×16 (40 não é múltiplo de 16).

## Integrados (1.94.0): o escudo final e o Unguento de Prata

O escudo final (com o 40 px corrigido: a sombra do cravo de cima à esquerda não parte mais o reflexo) e o pote de
cerâmica do unguento foram para o jogo. `pixel_comum.py`, `desenhar_escudo_pixel.py` e `desenhar_unguento_pixel.py`
saíram daqui para `ferramentas/arte/`, que grava direto em `rpg/web/static/hud/icones/` (ou numa pasta dada na linha
de comando); `ocupacao_icones.py` os importa de lá e continua gerando o estudo como era (o 40 de antes da correção).
As pastas `escudo-pixel/`, `escudo-pixel-v1/`, `unguento-pixel/` e `unguento-pixel-v1/` ficam como histórico da
avaliação. A conferência no jogo: `ferramentas/arte/fotografar_itens.mjs`.

## O Mago na fogueira e o Morel nas versões pequenas (proposta, sem versão)

**O pedido:** uma figura do Mago só para a fogueira (a de hoje, a carta da luta, tem a base inclinada e o capuz
torto em relação ao corpo) e as versões pequenas e intermediárias do Morel (a "40 reduzido a 32" ficou com a cabeça
pequena e traços finos ao lado dos outros). Sem mexer no busto de 80×80 nem na ficha baixa do Morel, na figura dele
na fogueira, nos retratos do Mago fora da fogueira, nem nos outros personagens. Só no protótipo.

**O que cada componente usa** (pelo `Icones`, em `rpg/web/static/retratos.js`):
- a figura de 16×16 (`figura`): a fogueira (o canvas da cena, `Icones.figura`) e o chip de 16 px do texto. Para o
  Mago e os heróis, a figura é a própria carta da luta;
- a carta (`carta`, 32 px): a carta da luta, o painel da comitiva e o aviso (`Telas.toast`). Os outros: 16×16 a 2×;
  o Morel: 32×32 a 1× (o busto de 40 reduzido);
- a cabeça (`cabeca`, 48 px): os cartões da tela da Comitiva, o cartão de reação (`Batalha.opiniao`) e a faixa de
  quem chega. Os outros: o recorte de 24×24 do busto, a 2×; o Morel: 48×48 a 1×.

**A proposta** (`personagens/`: `candidatos.py` com as três grades, nas paletas do jogo, sem cor nova):
- **Mago na fogueira** (16×16, só o papel `figura` na fogueira): sentado, o capuz com a ponta mole caída para trás e
  a cabeça no meio dos ombros, a capa assentando numa base reta, os antebraços cruzados no colo com as mãos à luz. A
  mesma escala e luz das outras figuras da roda; a cena não muda. A carta da luta, o busto, a cabeça e o chip ficam.
- **Carta do Morel** (16×16 a 2×, como a dos outros): a cabeça ocupando o quadro como a do Guerreiro e a da Odette,
  o cabelo castanho, as sobrancelhas, a cicatriz em diagonal (da testa à bochecha, entre os olhos), a barba, o punho e
  a guarda da espada atrás do ombro esquerdo, a ombreira de aço remendada e a de couro gasto, o tabardo vermelho. Não
  é a carta de rosto aproximado recusada: é busto, com ombros e espada.
- **Cabeça do Morel** (24×24 a 2×, como a dos outros; `desenhar_cabeca.py` monta as camadas): as sobrancelhas
  carregadas e puxadas para o meio (a expressão fechada), a cicatriz, a barba cheia escura com a boca fechada, as
  duas ombreiras e o tabardo. Sem a guarda da espada, como a cabeça aprovada de hoje.
- Nada foi reduzido nem ampliado do busto: as três grades foram desenhadas pixel a pixel, olhando o tamanho real.

**Comparação** (`personagens/fotografar_personagens.mjs` → `personagens/capturas-personagens/`, atual × candidata,
1500×950 e 1280×720, sem erro no console): a fogueira com o Mago sozinho e com a comitiva (Morel e Odette na roda,
Yara no acampamento); o painel da comitiva; a tela da Comitiva; o cartão de reação, a faixa de quem chega e o aviso
(pelas chamadas do próprio jogo); a luta com o Guerreiro, o Morel e a Odette (a vez do herói em destaque; o Morel
avançando) e com o Arqueiro e o Morel. Na candidata, o roteiro acrescenta `personagens-teste.js` e
`personagens-no-jogo.js` ao fim de `/static/retratos.js` só naquela página (troca os três papéis; o jogo não muda).
`personagens-teste.html` mostra as três grades ao lado das atuais e dos vizinhos, abrindo o arquivo no navegador.

**Leitura:** o Mago sentado fica estável e centrado, com a presença do de hoje, e lê como alguém descansando ao lado
do fogo; a carta e a cabeça do Morel passam a ter o peso e o tamanho de pixel dos outros (a cabeça grande no quadro,
massas de rosto, barba e armadura em blocos), mantendo a cicatriz, a barba, o cabelo, as ombreiras e a espada. Perde
um pouco: a cicatriz fina e as sobrancelhas desenhadas do 48 de hoje viram blocos de 2 px; a carta de 16 não mostra o
remendo da ombreira. As posições, as áreas clicáveis, o avanço das cartas e o destaque da vez do herói são os mesmos
(medidos nas fotos: os retratos nos mesmos pontos, em 32 e 48 px inteiros).

**Para integrar (se aprovado):** em `retratos.js`, a carta do Morel passa a ser a de 16×16 e a cabeça a de 24×24
(a escala sai do tamanho do desenho, como nos outros); o Mago ganha um papel só da fogueira (por exemplo
`fogueira`, pedido por `Icones.figura`), para o chip e a carta da luta continuarem com o desenho de hoje.
