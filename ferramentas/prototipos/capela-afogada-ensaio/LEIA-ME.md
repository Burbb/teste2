# Ensaio da Capela Afogada (histórico, fora do jogo)

Um teste de 12/10/2026, guardado aqui como **histórico**. Ele não é a capela do jogo e não deve ser integrado: a
capela de produção (as cenas em `rpg/web/static/telas/cenas.js` e o que o motor monta para elas) veio depois, por
outro caminho, e não foi tocada por este ensaio.

**O pedido de Jean, na época:** sem mexer no projeto, ver se ficaria agradável representar a Capela Afogada no estilo
das paisagens do jogo e deixar o jogador clicar no cenário para interagir com a missão. Duas vistas: o lado de fora
(a capela afundada até a metade das janelas, os juncos no pátio, a porta sob a lama, a torre sem sino, o canal que
entra pelo buraco no muro, o frio que sai dele, os sapos quietos com patas a mais) e a nave alagada por dentro (o lago
escuro entre colunas, os bancos podres, a água sumindo numa fenda perto do altar, o sarilho que solta a corrente).

## Como abrir

Abra `capela.html` direto no navegador (dois cliques no arquivo, no Windows ou em qualquer sistema). A página é um
arquivo só, com as fontes embutidas, e não precisa do jogo nem de internet. Nela:

- as abas "Lado de fora" e "Nave alagada", e a hora do dia (manhã, tarde, crepúsculo, noite);
- os nomes sobre a cena são pontos clicáveis, como os prédios da vila; alguns aproximam a câmera em dobro (a torre,
  os sapos, o sarilho); as opções numeradas embaixo fazem o mesmo (teclas 1 a 5, Esc afasta);
- na nave, "Soltar a corrente do sarilho" levanta a trava, gira a manivela, a corrente desce pela fenda e a fenda
  acende; "Travar de novo" volta ao começo.

As frases marcadas como "texto de teste" foram escritas para o ensaio; as outras são as do pedido.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `capela.html` | A página pronta (a segunda versão, a que foi mostrada a Jean). |
| `fonte/pagina.html`, `fonte/cena.js` | A página e o desenho das duas vistas (320×72, as mesmas peças de `vista.js`: o céu em faixas pontilhadas, o astro, as silhuetas pelo horizonte, a água do pântano). |
| `fonte/montar.py` | Junta as duas com as fontes do jogo (`rpg/web/static/fontes/`) em `capela.html`: `python ferramentas/prototipos/capela-afogada-ensaio/fonte/montar.py`. Refeito em 15/10/2026, sai idêntico. |
| `fonte/capela-v1.fonte.html` | A primeira versão, recusada pelo próprio ensaio (textura demais, fora do estilo das paisagens), sem as fontes embutidas. |
| `fonte/foto.mjs` | O roteiro das fotos da segunda versão (Playwright): `node fonte/foto.mjs <pasta desta capela>`, com uma pasta `fotos/` dentro. |
| `fotos/v1/`, `fotos/v2/` | As fotos das duas versões (v2: as quatro horas, os pontos, a câmera de perto, o sarilho soltando e solto, a janela de 400 px). |
| `ref/` | As paisagens do jogo usadas como régua do estilo (`ref.html` com cópias de `vista.js`, `sprites.js` e `sprites-dados.js` daquela data; `foto.mjs` tira `pantano-2.png`, `pantano-3.png` e `planicie-2.png`). As cópias ficam como estavam: são referência, não o jogo. |

## O que o ensaio concluiu

Dá para fazer: em 320×72 cabe um ou dois objetos reconhecíveis e clicáveis (a torre, o buraco, o sarilho), e a
câmera em dobro da vila mostra o detalhe pequeno (as patas dos sapos só aparecem de perto). O interior pede paleta
própria (pedra fria), com a cor do céu entrando pelas janelas. Cada lugar desenhado é trabalho à mão, como a vila.
