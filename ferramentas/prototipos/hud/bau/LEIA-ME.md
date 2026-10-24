# O baú: duas propostas para a arte do Baú Trancado (protótipo, 24/10/2026)

**Nada disto está no jogo.** O jogo continua com o baú de hoje (o placeholder da família de ferro, em
`rpg/web/static/hud/icones/bau-*.png`). Aguarda a escolha do Jean.

## O levantamento: onde o baú aparece

O desenho é o do consumível `bau` (o Baú Trancado), por `Icones.consumivel("bau")` (`CONSUMIVEL` em `icones.js`).

| lugar | tamanho | onde no código |
|---|---|---|
| a bolsa do painel do herói (com o anel dourado onde dá para abrir) | 32 | `app/paineis.js` |
| a bolsa do Inventário | 32 | `telas/inventario.js` |
| o baú ganho voando até a bolsa | 32 (a animação encolhe; não é tamanho parado) | `app/pagina.js` (`itemVoa`) |
| o chip do espólio quando um baú sai de uma luta ou evento | 32 | `sensacao.js` |
| a pilha de vários baús abertos juntos ("Baús abertos ×3") | 48 | `sensacao.js` |

- **O 64** está no catálogo (`TAMANHOS`), mas nenhuma tela pede o baú em 64 hoje.
- **Os estados:** só o fechado. Abrir é a pilha e o quadro do espólio; o "pronto" da bolsa é o anel dourado do
  espaço, não outro desenho. Não há baú aberto a desenhar.
- **Não são este baú (não mudam):** o retrato do Mímico (`retrato-mimico`, a caixa de frente com a boca, aprovado na
  1.192.0), o Salvar da doca (`atalho-salvar`, o baú aberto com a seta) e o baú da sacristia (a cena da capela,
  `telas/cenas.js`).

## As propostas

Desenhadas à mão, uma grade de texto por proposta (um caractere por pixel: `grades_a.py`, `grades_b.py`), na luz de
sempre (de cima e da esquerda) e com o contorno de 1 px. As fontes em camadas (uma por material) em
`fontes/bau-a/bau-a-32.aseprite` e `fontes/bau-b/bau-b-32.aseprite`, montadas em lote pelo `montar_fontes.py` e o
`pintar.lua` (sem tocar em janela aberta do Aseprite); o `.aseprite` exportado sai igual, pixel a pixel, à grade.

**A · a identidade de sempre (16 cores).** O baú de hoje refeito em pixel art nativo: a tampa abaulada em três
quartos, a frente à esquerda e a ponta à direita com o arco e o aro de ferro, as tábuas castanhas, as cintas de ferro
nas quinas (a da esquerda subindo pela tampa até a cumeeira), os cravos e o espelho de latão com a fechadura.

**B · o baú trancado (15 cores).** Construção livre: de frente e um pouco de cima (o tampo à vista), carvalho mais
escuro, cantoneiras de latão nos quatro cantos e um cadeado de ferro pendurado na aldraba, já que o item é o "Baú
Trancado". O tampo e o cadeado o separam do retrato do Mímico (de frente, sem tampo, com a boca).

## Os arquivos

`auxiliares/exportar.py` grava, em `propostas/bau-a/` e `propostas/bau-b/`, os nomes do jogo:

- `bau-32` (e o @2x, a duplicação exata): o desenho;
- `bau-48`: o 32 centrado com margem de 8 px, sem redimensionar (a pilha);
- `bau-64`: o 32 ampliado 2× (sem lugar no jogo hoje; só para o conjunto ficar completo).

## Como foi conferido

- **No tamanho real e no contexto:** o cenário `baus` dos testes (a vila com três baús na bolsa), trocando só os
  arquivos do baú pela página, a 1920×945 e a 1280×720: a bolsa (32) e a pilha dos baús abertos (48). A folha
  `folha-contexto.png` tem o atual, A e B lado a lado, nos mesmos lugares.
- **A prancha:** `folha-propostas.png`, o 32 no nicho da bolsa ao lado da poção e da bandagem, ampliado 8× para achar
  o pixel, e o Mímico ao lado para conferir que não se confundem.

## Limites percebidos no tamanho real

- **A pilha (48) fica menor que hoje:** o 32 centrado ocupa 32 de 48, e o placeholder ocupava o espaço quase todo. Lê
  bem, mas perde presença. Depois da escolha, a escolhida pode ganhar um 48 próprio, desenhado na grade de 48 a partir
  do 32 aprovado (as mesmas formas), se o Jean quiser a pilha do tamanho de antes.
- **O cadeado do B** em 32 é pequeno: lê como "uma peça de ferro na frente"; a forma de cadeado aparece melhor ampliada.
  Se o B for o escolhido, vale conferir de perto antes de integrar.
- **O A** é mais largo que alto (26×22), como o baú de hoje; o B, 26×23.

## Para integrar (só depois da escolha)

Copiar os PNGs escolhidos para `rpg/web/static/hud/icones/` (os nomes já são os do jogo), levar a fonte para
`ferramentas/arte/aseprite/bau/` (renomeando para `bau-32.aseprite`) e registrar o 48 e o 64 como `DERIVADOS` no
`exportar_aseprite.py` (o 48 centrado, o 64 o 32 ×2), ou desenhar o 48 próprio.
