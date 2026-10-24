# Etapa 2, primeiro lote: subida de nível, celebrações e raridade (protótipo, 23/10/2026)

**Nada disto está no jogo.** As cópias em `prototipo/` substituem `telas/celebracoes.js` e `telas/achado.js` só nas
páginas do fotógrafo (`page.route`); o jogo nunca lê `ferramentas/`. A base é a 1.200.1.

## Testar no navegador (a demonstração)

`demo.bat` (ou `python ferramentas/prototipos/hud/celebracoes/auxiliares/demo.py`) abre o painel em
**http://127.0.0.1:8765/**: os três cenários, cada um na proposta ou no jogo atual. Cada botão encerra o cenário
anterior e sobe outro do zero (um processo com saves temporários: o save do jogo não é tocado); na página, "Começar o
teste"; no canto de baixo, "repetir" e "painel". A proposta é servida por esse servidor de teste (`PROTOTIPO=1` em
`cenarios_teste.py` troca `telas/celebracoes.js` e `telas/achado.js` pelas cópias de `prototipo/`); a faixa do canto
só existe na demonstração. Movimento reduzido: no Chrome/Edge, F12 → ⋮ → More tools → Rendering → "Emulate CSS media
feature prefers-reduced-motion" → reduce, e repetir o cenário (ou o "Mostrar animações" desligado no Windows, que vale
para o sistema todo).

## O levantamento (o que existe hoje)

- **Como o jogador avança:** o XP vem das lutas (o quadro do espólio, `Jogo.abrir_espolio`/`ganhar_xp`), dos contratos
  e das missões; cada nível dá vida, recurso e atributos pela classe, um ponto de talento e, em alguns níveis, uma
  habilidade nova e o aviso da especialização. O motor manda o evento `celebracao` (`tipo: nivel`) com os ganhos
  prontos; vários níveis de uma vez viram festas seguidas.
- **A festa de nível** (`#celebracao`, compartilhada com o **Sigilo** e a **especialização**): raios cônicos em CSS,
  um anel borrado, partículas em `div` soltas, os ganhos com os sprites 16 antigos contando de zero, e as teclas
  ignoradas por 600 ms. O Continuar fechava; o clique duplo já fechava uma festa só.
- **As fagulhas soltas** (`particulas`): a mesma função na vitória, nos contratos, no Sigilo e na especialização.
- **O achado** (`telas/achado.js`): a raridade só na cor do nome e na linha do tipo ("Peito · Lendário"); raro e
  lendário esperam o feixe inteiro (1 a 1,4 s) e mais 0,55 a 0,9 s com o cartão sozinho antes da comparação e dos
  botões. Nada adianta isso.
- **O quadro do espólio:** já segue a regra do gesto (`Gesto`) e não muda neste lote.
- **Movimento reduzido:** quase não tratado (os raios e as partículas continuavam).

## A proposta

Uma direção só: **o efeito em pixel da HUD (o Brilho) e o ganho legível na primeira olhada**.

- **O Brilho** (`prototipo/brilho.js`): um canvas de baixa resolução (texel de 3 px, 15 quadros por segundo), com o
  pontilhado ordenado do `Sprites` e paletas agrupadas (ouro, mágico, raro, lendário, arcano, Sigilo). Uma aura em
  volta do que importa (o número do nível, a arte do item, o "Sigilo n/3") e um estouro curto; nada de disco ou coluna
  atrás de texto. Dura 0,9 s e apaga em degraus.
- **A festa de nível:** "Nível N" com o número carimbado; os ganhos em placas com os ícones da HUD (os vitais em 20, os
  atributos em 24), já com o valor final (sem contar de zero); o ponto de talento com o ícone dos Talentos e o atalho
  (T); a habilidade nova; a cascata leva ~0,6 s.
- **Os gestos** (sem bloqueio de clique e sem espera para clicar de novo): o Continuar, o Enter, o Espaço e o Esc
  fecham a qualquer momento; um clique fora durante a revelação só a completa; como no espólio, não contam o toque que
  começou antes de a festa abrir, o 2º clique de um clique duplo nem a tecla segurada, e o gesto que fecha não
  atravessa para a festa seguinte. A seleção de texto que o clique duplo deixava no botão da festa seguinte (no jogo
  também) sai.
- **A raridade no achado:** um selo com o nome da raridade abaixo de "Você encontrou" (a linha do tipo fica só com o
  espaço, sem repetir); intensidade proporcional: comum, só o cartão e as faíscas; mágico, a aura leve; raro, a aura e
  o feixe; lendário, a aura maior e o feixe. O cartão aparece quando o feixe bate (0,43 s), e um clique ou tecla
  adianta tudo (o gesto não escolhe: os botões ainda não estão lá).
- **O Sigilo e a especialização** usam o mesmo Brilho (paletas Sigilo e arcano); as fagulhas da vitória e dos
  contratos viram o estouro em pixel.
- **Movimento reduzido:** sem cascata, sem estouro, sem feixe; a aura fica parada, as informações e o selo iguais.

## Os números (do `registro.json` de cada pasta, 1920×945)

| Do anterior fechado até os botões | atual | proposta | proposta, movimento reduzido |
|---|---|---|---|
| comum, mágico | ~0,37 s | ~0,36 s | ~0,36 s |
| raro | 2,2 s | 1,2 s | 0,37 s |
| lendário | 2,8 s | 1,2 s | 0,37 s |
| raro/lendário com um clique logo que surgem (`rapido-*`) | 0,5 a 0,9 s | ~0,14 s | — |

A festa de nível chega no mesmo tempo nos dois (o motor manda); o que muda é que ela pode ser fechada na hora.

## As capturas

- `capturas/folha-estados.png`: cada momento, atual × proposta, em 1× (o meio da tela, 900 ms depois de aparecer).
- `capturas/folha-ritmo.png`: os cinco instantes (60, 250, 500, 900, 1600 ms), atual e proposta.
- `capturas/folha-apertados.png`: 1280×720 e movimento reduzido, atual × proposta.
- `capturas/<atual|proposta>[-1280|-reduzido]/`: os vídeos (`.webm`, o ritmo), o registro e os quadros de 250 e 900 ms
  (1920) ou de 900 ms (os outros); os demais instantes foram tirados depois de montar as folhas (refazer: rodar o
  fotógrafo e `auxiliares/folhas.py`).
- `capturas/rapido-<atual|proposta>/`: o clique rápido, em vídeo e registro.

## Os cenários de teste

`auxiliares/cenarios_teste.py` (**cenários de teste**, fora do jogo e de `tests/`): o herói a 25 de 30 XP no Vau e os
caminhos reais do motor. `nivel`: dois lobos (nível 2, Investida). `dois_niveis`: a Ilse (nível 3) e dois afogados
(do 1 ao 3, a festa duas vezes, o clique duplo na primeira, o Enter na segunda). `raridades`: quatro achados seguidos,
um de cada raridade, pelo `gerar_equip` com a raridade pedida. Nenhuma chance, recompensa ou progressão muda.

```
PLAYWRIGHT_MODULO=<file:// do index.mjs> PROTOTIPO=1 node auxiliares/fotografar.mjs <raiz> capturas/proposta
#   MOVIMENTO=reduzido, JANELA=1280x720; sem PROTOTIPO, o jogo atual; "rapido,rapido-nivel" para o clique rápido
python auxiliares/folhas.py capturas
```

## Limitações vistas no uso

- **O Sigilo e a especialização** não têm cenário aqui: usam o mesmo código e o mesmo Brilho, mas não foram
  fotografados. Nem as fagulhas da vitória e dos contratos.
- **O som** é o de antes (subir, fanfarra, o da raridade): nada foi feito para ele.
- **A aura do achado** é pequena a 1920 (o cartão tem 300 px); a diferença entre raro e lendário está mais no feixe e
  na cor do que no tamanho.
- **Movimento reduzido:** a aura parada ainda tem pontos em volta da arte (estáticos); se preferir nada, é tirar.
- **A especialização no nível 5** e uma habilidade de nome longo na festa não apareceram nos cenários; o nome longo
  de item ("Lamento do Corvo (Besta Leve Enferrujada)") quebra em três linhas no cartão, como no atual.
- Os tempos da tabela incluem as esperas do fotógrafo entre um gesto e outro (iguais nos dois lados).
