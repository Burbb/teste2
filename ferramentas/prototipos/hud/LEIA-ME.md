# Protótipo: a ficha do herói (experimento)

Duas tentativas na mesma página, com os mesmos dados e a mesma janela: **Anterior** (assets desenhados em código) e
**Assets** (peças recortadas de uma imagem de referência). O controle "Versão" (ou a tecla **V**) alterna as duas.

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
  a versão (Anterior ou Assets; **V** alterna), nome curto e longo (com PARAIBATRON), nível 1, 6 e 14, equipamento completo, parcial ou vazio, bolsa comum, cheia
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
