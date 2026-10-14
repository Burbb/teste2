# Protótipo: a ficha do herói (experimento)

Três versões na mesma página, com os mesmos dados e a mesma janela: **Anterior** (a HUD atual do jogo, com a ficha
desenhada em código), **Assets** (a ficha com peças recortadas de uma imagem de referência) e **HUD 3** (a HUD inteira
com as molduras, as superfícies e os controles de três folhas de referência). O controle "Versão" (ou a tecla **V**)
passa de uma à outra.

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
  a versão (Anterior, Assets ou HUD 3; **V** passa de uma à outra), o entorno (o Bosque da campanha, com a missão e os
  contratos, ou o Brejo das duas primeiras tentativas), a página (o lugar ou a cena de missão, com texto longo), as
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
