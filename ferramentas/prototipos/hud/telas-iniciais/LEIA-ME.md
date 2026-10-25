# As telas iniciais: o levantamento e a criação em cartões (24/10/2026; protótipo, nada no jogo)

Depois da retirada do mundo gerado (1.206.0, `roadmapIDEIAS/24-RETIRADA-DO-PROCEDURAL.md`), o título, os saves e a
criação já funcionam só com a campanha (no jogo). Este protótipo levanta o que falta de acabamento e propõe uma
direção só para o que pede redesenho: a criação do personagem. A folha: `folha-telas-iniciais.png` (as páginas
inteiras, reduzidas à metade; as capturas em tamanho real saem de novo por `auxiliares/fotografar.mjs`, fora do git).
A demonstração: `demo.bat` (painel em http://127.0.0.1:8770/, saves numa pasta temporária).

## O levantamento (no jogo de hoje, 1920×945 e 1280×720)

| tela | como está | avaliação |
|---|---|---|
| o título | "The Unquiet" e as três opções (Novo jogo, Carregar jogo, Sair) na letra gótica grande sobre a paisagem do castelo | funciona e combina com a arte do título; sem redesenho agora |
| os saves | cartões com o busto da classe, nível, a etiqueta da região e do modo, dia, lugar e quando; o do mundo gerado apagado, com "mundo gerado · não abre mais"; o Voltar na letra do título | legível nas duas janelas; o cartão é o acabamento antigo (o fio marrom fino), mas não atrapalha o uso: registrado para a consolidação da HUD, sem proposta agora |
| o save recusado | a mensagem curta na página ("Este save não abre: é do mundo gerado...") e o Continuar | claro; nada a mudar |
| o nome | o campo e o Confirmar da HUD | já na linguagem aprovada |
| a classe | um texto corrido: "Guerreiro → Paladino \| Berserker" e a frase de cada classe em itálico, e embaixo três botões só com o nome | **pede redesenho**: a escolha principal da criação está separada da informação dela (lê-se em cima, clica-se embaixo), sem os desenhos de classe que o jogo já tem e com a barra "\|" de texto técnico |
| o modo | dois botões longos (a 1280, o Resgate quebra em duas linhas) e a caixa "Mostrar tutorial" | o mesmo problema, menor: o nome do modo e a explicação na mesma linha |

## A candidata R · a criação em cartões

Os cartões são os botões da página de sempre (a face de ferro, a aresta que acende com o mouse e o foco, o número da
tecla no canto), lado a lado:

- **a classe:** três cartões com o busto da ficha (o mesmo desenho e o mesmo nicho do painel do herói), o nome na letra
  do título, o ataque da roda (a espada, o arco, o cajado) com o recurso (Vigor, Foco, Mana), "No nível 4" e as duas
  especializações, e a frase da classe (a de hoje). A lista em texto sai da página: os cartões a mostram.
- **o modo:** dois cartões, "Resgate" e "Hardcore", cada um com a explicação de hoje embaixo; a caixa "Mostrar
  tutorial" continua logo abaixo, marcada.

Textos, ordem das perguntas, teclas (1, 2, 3; Esc volta) e a caixa: os de hoje. **Na integração**, o motor manda os
dados de cada opção no `meta` (a classe, o recurso, o ícone do ataque, as especializações, o nível delas e a frase;
o modo e a explicação), como `auxiliares/cenarios_telas.py` faz só no protótipo, e para de escrever a lista das
classes no texto (a interface de texto continua escrevendo); a tela só desenha. As regras de `criacao.css` passam na
trava do estilo (cores sólidas, sem transparência nem borrado).

**Conferido** (`fotografar.mjs`, hoje e R, nas duas janelas): os três cartões cabem lado a lado a 1280×720, sem corte
nem rolagem; o modo em dois cartões, sem quebra no nome; sem erros na página; a escolha pelo clique e pelas teclas é a
de sempre (o mesmo botão).

**Avaliação.** O ganho: a escolha e a informação no mesmo lugar, com os desenhos do jogo, e a criação inteira numa
tela só, sem rolar. A limitação: a frase de cada classe continua a de hoje (curta, sem números); números de vida e
ataque por classe seriam outra decisão (o motor tem a base), não feita aqui.
