# Os 14 estados restantes (lote da madrugada, 21/10/2026)

Pedido de Jean: uma proposta por estado para os 14 estados que ainda usam os sprites do jogo, em sete lotes, **só no
protótipo**. Nada daqui está aprovado nem integrado; o jogo não lê nada desta pasta. Firme (R2), Em guarda (G1) e
Esquiva (E6), já no jogo, são a referência de acabamento e não foram redesenhados.

## Como foi feito

- **Tamanho:** 16 px de arte e o @2x pela duplicação exata. É o tamanho do chip da carta e do selo do estado que chega
  (`.ef img.sprite { --s: 16 }`, ~18 px de tela a 1920×945 pelo zoom da HUD). Nenhum outro tamanho.
- **Desenho:** as grades à mão em `auxiliares/icones16.py` (uma letra por pixel; a paleta no topo do arquivo; o
  contorno de 1 px pelos lados, escrito à mão ou pelo `com_contorno`). As grades de um lote ainda não entregue, no mesmo
  arquivo, são rascunhos até o commit daquele lote. `auxiliares/previa.py` é a bancada (o 1× em
  chips escuros ao lado dos três finais, o 2× e a 12×).
- **Aseprite:** o conector do MCP (`aseprite-bridge`) **não conectou nesta sessão** ("Connection closed", conferido no
  começo; não foi reinstalado nem reconfigurado). As fontes saíram pelo caminho já registrado da linha de comando
  (`ferramentas/arte/montar_fontes.py`: o `montar_camadas.lua` com o `pintar.lua`, que relê cada pixel gravado), pelo
  `auxiliares/montar.py`:
  1. `icones16.py` grava `grades/<id>.txt` e `listas/<id>/<camada>.lua` (com `ordem.txt`);
  2. o Aseprite (`-b`) monta `fontes/<id>/<id>-16.aseprite`, uma camada por parte, o contorno por cima;
  3. o Aseprite exporta `proposta/<id>-16.png` (o composto das camadas visíveis); o @2x pelo Pillow (vizinho mais
     próximo);
  4. a conferência: 16×16 RGBA, fundo transparente, nenhum pixel parcial, o 1× igual pixel a pixel à grade, o @2x igual
     ao 1× ampliado.
  Operações: o desenho (as grades) é à mão; montar, pintar e exportar são do Aseprite pela linha de comando; o @2x, as
  folhas e as fotos são cálculos fora do editor.
- **Fotos:** `auxiliares/fotografar.mjs` (derivado de `flechas_firme/auxiliares/fotografar_luta.mjs`) sobe os cenários
  dos testes de navegador (`covil` com `EFEITOS`/`EFEITOS_INIMIGO`; `tutorial` para o servo do Necromante) a 1920×945,
  com as situações de cada lote em `auxiliares/situacoes.json` (cada estado onde ele de fato aparece: no herói, no
  inimigo ou no aliado). Na proposta, **só a página** troca a imagem do chip daquele estado
  (`.ef[data-ef="<id>"] img.sprite`); os sprites do jogo e os outros papéis deles ficam intactos. O selo de chegada
  (`.faixa-acao.selos`) não tem seletor por estado e não foi trocado nas fotos.
- **Folhas:** `auxiliares/prancha.py lote <n>` → `lote<n>.png` (a fileira da carta com os três finais, atual ×
  proposta, 1× e 2×; as tentativas guardadas; a 12× com a grade; as cartas na luta, atual × proposta, 1× e 2×);
  `prancha.py geral` → `geral.png` (os 17 identificados e os estados de dano lado a lado).

## As regras conferidas no código (`rpg/estados.py`, `rpg/inimigos.py`, `rpg/habilidades.py`, `rpg/talentos.py`)

| Estado | O que faz de fato | Onde aparece |
|---|---|---|
| Veneno (`veneno`) | dano por turno; não pega em mortos-vivos nem construtos | no herói (aranha, rato, lagarto, afixo "venenoso") e no inimigo (Flecha Envenenada) |
| Sangramento (`sangramento`) | dano por turno; não pega em construtos nem etéreos | no herói (Mordida Sangrenta de lobos e ratos) e no inimigo (Sede de Sangue, o lobo do Patrulheiro) |
| Chamas (`queimadura`) | dano por turno, acumula camadas ("em chamas ×N"); a chuva enfraquece; a Combustão detona o que falta arder | no herói (Bola de Fogo de cultistas e demônios) e no inimigo (Bola de Fogo, Inferno) |
| Maldição (`maldito`) | dano por turno e −40% de defesa | no herói (a maldição de cultistas, afogados, chefes) e no inimigo (Drenar Vida e a Maldição do Necromante) |

## Lote 1: Veneno e Sangramento

- **Veneno — a serpente** (`estado-veneno`): uma cobra verde em S, a cabeça no alto voltada para a esquerda, o olho
  escuro e a língua bifurcada vermelha; camadas corpo, olho, lingua, contorno. Silhueta sem gota: não depende do verde
  para se separar do Sangramento.
- **Sangramento — as gotas de sangue** (`estado-sangramento`): a gota grande à direita (junto do número do chip) e uma
  gota pequena atrás, no alto, à esquerda; camadas gotas, contorno.
- **Tentativa guardada:** `estado-veneno-presas` (as duas presas pingando veneno). Recusada na bancada: na carta, em
  tamanho real, lia como "!!" (colidiria com a exclamação da Iniciativa). Antes dela, as bolhas sobre uma poça (liam
  como uma barra e bolas) e as presas presas a uma gengiva (liam como "π") não chegaram a fonte.
- **Correção vista na carta:** a primeira versão do Sangramento tinha a gota pequena embaixo, à direita; colada no
  número, lia como ponto decimal ("2.2"). A gota pequena passou para o alto, à esquerda.
- **Fotos:** o herói contra ratos (envenenado e sangrando, os dois do rato) e os lobos envenenados pelo Arqueiro.
  Sem erro nem aviso no console. Folha: `lote1.png`.
- **Avaliação sincera:** a serpente é a leitura mais forte do lote (lê como cobra no 1×); o Sangramento continua na
  família da gota do jogo, agora com duas gotas: claro, mas pouco novo.

## Lote 2: Chamas e Maldição

- **Chamas — as três línguas de fogo** (`estado-queimadura`): a língua do meio mais alta, duas menores dos lados, o
  miolo claro embaixo e a borda vermelha; camadas chamas, miolo, contorno. Continua sendo fogo (o estado é fogo), mas
  aberto em línguas separadas, em vez da bola de fogo do sprite `chama` (que fica no Vigor, no Poder e na Pena de
  Fênix).
- **Maldição — a caveira roxa** (`estado-maldito`): o crânio de osso tingido de roxo, as órbitas escuras com um ponto
  magenta aceso e os dentes; camadas cranio, olhos, contorno. Não é uma chama recolorida: outra silhueta (crânio) e
  outra cor.
- **Na bancada:** a primeira caveira tinha dois fios de fumaça em cima e lia como um inseto de antenas; a fumaça saiu e
  as órbitas cresceram (3×3, com o ponto aceso).
- **Fotos:** o herói contra cultistas (em chamas e amaldiçoado, os dois do cultista) e os lobos em chamas pelo Mago. Sem
  erro nem aviso no console. Folha: `lote2.png`.
- **Avaliação sincera:** a caveira é inconfundível em tamanho real; o risco é a leitura de "morte" mais que de
  "maldição" (a cor roxa e os olhos acesos ajudam). As Chamas leem como fogo de imediato, mas ficaram próximas do sprite
  atual: a mudança é de acabamento, não de conceito. A queda de 40% de defesa da Maldição não aparece no ícone (a dica
  diz).
