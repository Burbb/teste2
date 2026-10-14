# Protótipo: a ficha do herói (experimento)

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
  nome curto e longo (com PARAIBATRON), nível 1, 6 e 14, equipamento completo, parcial ou vazio, bolsa comum, cheia
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

## Decisões visuais

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

## O que ainda não convence

- **O retrato** está na escala ×3 (3 px por texel), mais fina que os ícones e a moldura (2 px). O jogo já usa ×3 no
  retrato grande, mas aqui, lado a lado com a moldura nova, a diferença de grão aparece. Desenhar o retrato em 48
  texels a ×2 resolveria, mas é mais arte do que este teste pedia.
- **A espada a ×1** (nos atributos, 16 px) fica fina: a lâmina diagonal de dois texels some um pouco no escuro. A ×2,
  nos espaços, ela lê bem. O escudo, o anel e a poção funcionam nas duas escalas.
- **O pé do painel a 1500×950** sobra vazio (uns 100 px abaixo da reputação). Não estiquei nada para preencher: a
  ficha real tem a comitiva e o animal nessa coluna, que este teste não incluiu.
- **O entorno é fotografia.** A barra de vida e recursos do topo e o painel do mundo são do jogo num momento fixo (o
  herói de nível 1 do cenário), então não acompanham os controles da ficha.
