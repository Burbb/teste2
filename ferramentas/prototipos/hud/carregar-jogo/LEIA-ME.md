# O "Carregar jogo": o levantamento e uma proposta (25/10/2026; protótipo, nada no jogo)

O título leva à lista de saves pelo "Carregar jogo" (só aparece com algum save na pasta). Este protótipo levanta como
a lista funciona hoje e propõe uma direção só, a R, coerente com a criação em etapas (1.208.0) e a HUD aprovada. A
folha: `folha-saves.png` (hoje × R, os mesmos saves, nas duas janelas). A demonstração: `demo.bat` (painel em
http://127.0.0.1:8772/, saves temporários criados na hora; os seus não são tocados nem lidos).

## O levantamento (hoje, 1920×945 e 1280×720)

**Os dados de cada save** (`resumo_save`, em `rpg/sistemas/persistencia.py`, lendo o arquivo sem montar o jogo): o
nome, a classe, o nível, o dia, o lugar, o modo (resgate ou hardcore), a região e a data do arquivo; o save do mundo
gerado vem marcado `incompativel` e o que não se lê, `ilegivel`. **No arquivo, sem uso na lista hoje:** a
especialização (`jogador.spec`) e as missões (a etapa, se concluída). O motor manda a lista do mais recente ao mais
antigo; o clique no cartão carrega; o do mundo gerado responde com a mensagem curta e o título volta.

| ponto | como está | medido |
|---|---|---|
| a lista | cartões de 340 px em grade, no meio do título, com o título grande em cima | a 1280×720, cabem dois cartões e meio; o Voltar do título fica por cima do fim da lista |
| a hierarquia | o nome em gótico, "classe · nível", a etiqueta "Vale do Turvo · resgate" (igual em todos), "Dia · lugar · quando" | a especialização não aparece; a etiqueta repetida pesa mais que o lugar |
| o que não abre | o cartão apagado (opacidade) e a etiqueta "mundo gerado · não abre mais" | distinguido mais pela cor; o danificado diz "save danificado" |
| o Voltar | a opção "Voltar" do título, depois da lista | usável junto com a lista, mas só opaco ~250 ms depois (a entrada das opções do título) |
| o tempo da lista | o motor lê cada save inteiro para montar o resumo | ~9 ms por save: 25 ms com um, ~110 ms com dez, ~195 ms com 22 (dentro da página, do envio da escolha à lista) |
| o teclado | o Tab vai primeiro aos botões do topo | o primeiro Tab não chega a um cartão; o foco do cartão só clareia a borda |

## A proposta R

- **Uma janela "Carregar jogo"** na família da criação: a moldura das janelas principais sobre a paisagem do título
  (o título grande sai da frente enquanto a lista está aberta), o cabeçalho com a contagem ("10 partidas salvas · 3 não
  abrem"), as partidas **numa coluna que rola dentro da janela** e o **Voltar no rodapé, fora da rolagem**: chega junto
  com a lista, sem animação de entrada.
- **O cartão** (o carvão com a aresta de ferro, como os da criação): à esquerda o retrato da classe (o mesmo da ficha,
  72 px; 56 a 1280), o **nome** em gótico (reticências se for longo; o nome inteiro na dica) e **"classe ·
  especialização · nível"**; à direita, menores, **o lugar e o dia**, **a missão em andamento** (o nome como o
  rastreador mostra; "Primeiro capítulo concluído" no fim do Vale), **o modo** numa etiqueta e quando foi salvo. A
  região saiu da etiqueta (é a mesma em todas as partidas de hoje).
- **O que não abre** diz em texto: a aresta tracejada, o retrato apagado e, no lugar do lugar e da missão, "⊘ Não
  abre" com o motivo ("Do mundo gerado, o modo que saiu do jogo." ou "Save danificado: o arquivo não pôde ser lido.").
  Continua clicável: abre a mensagem de sempre.
- **O teclado**: a partida mais recente chega com o foco; ↑ ↓ (e Home/End) andam pelos cartões, rolando a lista; Enter
  ou o clique carregam; o Tab vai dos cartões (um ponto só) ao Voltar; Esc volta. O mouse acende a aresta em latão
  escuro; o foco, o anel claro de 2 px. O segundo clique de um clique duplo não carrega de novo.

Nada novo além da lista: sem filtros, exclusão, renomeação nem ordem diferente (a do motor, a mais recente primeiro).

## Conferido (`auxiliares/fotografar.mjs`, no jogo de verdade, hoje e R, 1920×945 e 1280×720)

- **Sem saves:** o título não oferece "Carregar jogo" (hoje e na R; a R ainda diz "Nenhuma partida salva." se a lista
  vier vazia).
- **Uma, dez e 22 partidas:** a R sem rolar a página, a lista rolando dentro da janela com dez e 22, nenhum texto
  cortado sem reticências; o Voltar usável e opaco no mesmo instante da lista (hoje, ~250 ms depois); o teclado chega
  ao cartão com o anel (hoje não chega); Esc volta ao título; o save do mundo gerado mostra a mensagem; a campanha de
  Maria carrega e a ficha é a dela; sem erros na página. Uma campanha nova, criada e salva na 1.208.0, carrega pela
  lista de hoje (conferido no roteiro da criação, `telas-iniciais/auxiliares/criacao.mjs`).

**SIMULAÇÃO (identificada).** Os saves são criados pelo motor numa pasta temporária (`cenarios_saves.py`): o nível, a
especialização, o dia, o lugar, a etapa das missões e as datas dos arquivos são escritos direto antes de salvar, sem
jogar até lá; o danificado é um save cortado ao meio; os do mundo gerado, uma campanha sem a `campanha` no mundo (como
nos testes). Carregam pelo jogo de verdade.

**Só da demonstração.** A especialização e a missão em andamento chegam à lista por `resumo_do_save` no cenário (troca
`resumo_save` só nesse processo); na integração, em `resumo_save`, numa leitura só do arquivo (o protótipo lê duas
vezes, por isso a lista dele chega ~10% mais tarde que a de hoje).

**Limitações.** O tempo da lista cresce com o número de saves pelo motor (~9 ms por save, lendo o arquivo inteiro): com
22 saves, ~0,2 s, igual hoje; a proposta não muda isso (pediria guardar um resumo à parte no save, outra decisão). Os
nomes dos saves danificados são o do arquivo (não há outro dado). A missão em andamento repete "A Febre do Turvo" na
maioria das partidas de hoje (o Vale tem uma missão principal); o lugar e o dia é que as distinguem.

## A R integrada na 1.209.0 (25/10/2026)

O Jean aprovou a R; ela entrou sem redesenho: `telas/saves.js`, `css/25-carregar.css` (o CSS da candidata com a mesma
especificidade), a especialização e a missão em `resumo_save` (uma leitura só do arquivo). **Os dois ajustes pedidos:**
o nome cortado ganha a dica com ele inteiro, no mouse e no foco do teclado (o sistema de dicas, como no mercado; quando
a lista rola, a dica do cartão com o foco volta no lugar novo); o foco começa na partida mais recente que abre (as que
não abrem continuam acessíveis e dizem o motivo; sem nenhuma, o foco começa no Voltar, e nada carrega). **Uma correção
achada na conferência:** depois de abrir um save que não abre, a janela ficava na página e empurrava a mensagem e o
Continuar para fora da vista; agora, respondida a lista, ela sai da página. Sem índice ou resumo paralelo dos saves:
a leitura segue ~9 ms por save. `cenarios_saves.py` serve o jogo como está (com `PROPOSTA` ou sem); `saves.css` e
`saves.js` daqui ficam como registro.

**Conferido no jogo** (`auxiliares/conferir.mjs`, 1920×945 e 1280×720, tudo certo): sem saves, uma, dez e 22 partidas,
a mais recente do mundo gerado e nenhuma que abre; o Voltar usável junto com a lista; a janela sem rolar a página; o foco
inicial; o Tab, Shift+Tab, as setas, Home/End; a dica do nome cortado no foco e no mouse (e nenhuma no nome que cabe); o
Esc; o save que não abre (a mensagem, nada carrega); o clique duplo e dois Enter carregando uma vez. Criar, salvar e
carregar uma campanha nova pela lista: `telas-iniciais/auxiliares/criacao.mjs`, nas duas janelas.
