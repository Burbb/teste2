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

## Segunda rodada: a criação em etapas (R2), a candidata (25/10/2026; protótipo, nada no jogo)

O Jean gostou da direção dos três cartões, mas na R o conteúdo ficava pequeno no alto do painel genérico das telas de
menu, com muito vazio embaixo, as descrições apertadas, as faces cinzas dos botões antigos e, no modo, as perguntas e
respostas anteriores acumuladas como uma conversa. A R fica como estava (`PROPOSTA=r`, `criacao.css`/`criacao.js`),
para comparar. A folha: `folha-criacao-r2.png` (R × R2 com os mesmos dados, Ana e o Arqueiro, nas duas janelas; depois
os estados da R2 e a campanha começando). A demonstração: `demo.bat`, botão "R2".

**Como os jogos do gênero fazem (e o que a R2 segue).** A criação é uma tela própria, não um trecho da página: um
assistente curto sobre o cenário do menu, de tamanho fixo, com a etapa atual marcada, o que já se escolheu num resumo e
um único botão que confirma; escolher e confirmar são gestos separados; nada se grava até o último botão, então voltar
não perde nada.

**R2 · o que muda da R**
- **Uma área própria, no centro, sobre a paisagem do título** (a noite e as brasas continuam atrás): a moldura das
  janelas principais, 1100 px de largura (a 1280, a janela inteira menos a margem), mais larga e menos alta que o painel
  genérico. Título, etapas, escolha, resumo e botão formam um conjunto; as três etapas têm a mesma altura (moram na
  mesma célula, as outras invisíveis e inertes), então nada pula ao avançar.
- **As etapas "1 Nome → 2 Classe → 3 Modo"**, discretas, à direita do título; a atual em latão, as feitas voltam com o
  clique. No lugar do histórico de perguntas e respostas, **o resumo** no rodapé, junto do botão: "Ana", depois
  "Ana · Arqueiro · Resgate".
- **Os cartões de classe** na ordem pedida: 1. o retrato da ficha (80 px, o mesmo tamanho dela) e o nome; 2. uma frase
  de como a classe joga; 3. o ataque (o ícone da roda, o nome, o alcance) e o recurso (o ícone, o total e quanto
  recupera por turno de luta); 4. "No nível 4: Paladino ou Berserker", discreto. O carvão com a aresta de ferro, sem as
  faces cinzas: o mouse acende a aresta em latão escuro; escolhido, a aresta de latão em dobro, a face aquecida, o
  número aceso e "Escolhida" no canto (fica depois que o mouse sai); o foco do teclado, o anel claro por fora.
- **O modo**: "Se você cair (em combate, de fome ou de infecção):" e os dois cartões com as consequências da derrota em
  linhas curtas (os textos de hoje, sem "fácil" nem "difícil"); o Resgate escolhido de início, como hoje. Logo abaixo,
  "Mostrar tutorial" numa faixa própria, com uma nota; fecha com o resumo e **"Começar campanha"**, o botão maior.
- **Interação**: o clique num cartão, as teclas 1–3, as setas e o espaço **só escolhem**; **Avançar** (ou Enter) passa
  à etapa seguinte, desligado enquanto não há escolha; **Voltar** (ou Esc) revisa sem perder nome, classe, modo nem
  tutorial; na primeira etapa, volta ao título. O Enter só vale apertado de novo depois de solto (o segurado não
  atravessa etapas), o botão de uma etapa nova espera 400 ms (o segundo clique de um clique duplo não avança de novo) e o
  "Começar campanha" espera 700 ms e vai uma vez só. O Tab segue a tela: os cartões (um ponto só, as setas dentro), o
  Voltar, o Avançar.

**Os textos** (conferidos nas regras, sem promessa nova): as frases saem da `desc` de cada classe sem o que as linhas de
baixo já dizem ("Muita vida e defesa: aguenta o tranco."; "Ágil e preciso, ótimo contra voadores. As flechas podem
acabar." — os voadores sofrem 1,25× à distância, `dados.py`; "Frágil, mas devastador: magias elementais exploram
fraquezas."). O ataque e o alcance vêm de `CLASSES[...]["ataque"]`; o recurso, de `base` (Vigor 30 e 6 por turno,
Foco 25 e 5, Mana 40 e 3: o que `luta.py` soma no fim de cada rodada, no nível 1); as especializações e o nível, de
`SPECS` e `NIVEL_ESPECIALIZACAO`. Os modos: os textos de hoje em duas linhas. A nota do tutorial ("Orientações curtas nas
primeiras ações. A Ajuda (F1) desliga ou religa.") é nova e segue o que a Ajuda faz.

**Conferido** (`auxiliares/criacao_r2.mjs`, no jogo de verdade, 1920×945 e 1280×720, tudo certo): o painel cabe sem rolar
nem cortar nas três etapas, com a mesma altura (599 e 583 px); o campo chega com o foco; o Enter segurado no nome para
na Classe; a Classe chega sem escolha e com o Avançar desligado; o clique, a tecla 3 e a seta escolhem sem avançar; a
escolha continua à vista sem o mouse; o anel de 2 px no cartão e no Avançar; o Tab cartões → Voltar → Avançar; as três
classes; o clique duplo no Avançar para no Modo; Hardcore e o tutorial desligado; o Esc e o Voltar preservam tudo; a
barra de etapas volta; o nome longo com acento (40 letras) e o resumo sem invadir o botão; o Esc no nome volta ao título;
o nome em branco vira "Aventureiro"; três campanhas começadas, e o motor recebe exatamente o que se escolheu (Ana,
Arqueiro, Resgate, tutorial; o nome longo, Mago, Hardcore, sem tutorial, e nenhum quadro de orientação; Aventureiro,
Guerreiro, Resgate); sem erros na página.

**Só da demonstração (não é a integração).** O motor da criação está trocado no cenário (`criacao_em_etapas` em
`cenarios_telas.py`, só com a tela gráfica): uma pergunta "criacao" com tudo o que a tela mostra (`dados_da_criacao`),
devolvida inteira no "Começar campanha" e conferida pelo motor; o `nucleo.js` é servido com o tipo novo de pergunta e o
gancho que desmonta a tela; as frases curtas moram no cenário (`FRASES`); a linha `[criacao]` no stderr existe só para o
roteiro ler o que o motor recebeu. **Na integração:** a pergunta numa função da ponte (`WebUI`), o texto e o teste por
robô (`BotUI`, o gabarito) com as perguntas de sempre, as frases em `classes.py`, os arquivos `criacao-r2.*` num CSS e
num JS do jogo, e a fumaça e os cenários que passam pela criação de hoje (o nome, os botões de classe) ajustados.

**Limitações e decisões para o Jean.** O resumo diz "Ana · Arqueiro": o jogo não tem nomes de classe no feminino (nada
inventado aqui). Os números do recurso são os do nível 1 (talentos mudam a recuperação). O céu da paisagem atrás muda
com a hora do título (o mesmo desenho do menu). O nome mora numa etapa curta dentro da altura da classe: fica um vazio
em volta do campo, de propósito (o painel não pula). O Enter também começa a campanha na última etapa (solto e
apertado de novo, depois da espera).

## A R2 integrada na 1.208.0 (25/10/2026)

O Jean aprovou a R2; ela entrou no jogo sem retoques: `rpg/criacao.py` (os dados que a tela mostra e a conferência da
resposta), `Jogo.novo_jogo` (a tela gráfica numa pergunta só, `WebUI.criar_personagem`; o texto e o robô com as
perguntas de sempre), as frases curtas em `classes.py`, `app/criacao.js` e `css/24-criacao.css` (o mesmo CSS, com a
mesma especificidade). Saíram as adaptações da demonstração: a troca do motor no cenário, o `nucleo.js` servido, o log
`[criacao]`, as frases no cenário; e, sem uso, a caixa marcável da tela gráfica. **Uma diferença pedida pelo Jean:** a
espera por tempo do Avançar e do Começar saiu; a tecla segurada e as repetições passam pelo `Gesto` do jogo (a tecla que
vinha apertada da etapa anterior não vale até ser solta) e o segundo clique de um clique duplo (`detail` 2) não avança:
um Enter novo responde na hora.

**Conferido no jogo** (`folha-criacao-integrada.png`; `auxiliares/criacao.mjs`, antes `criacao_r2.mjs`, nas duas janelas, tudo certo): o mesmo
desenho da candidata (as fotos iguais às da folha), as três classes, os dois modos, o tutorial ligado e desligado, o
nome longo com acento, avançar, voltar e preservar, o Enter segurado, o clique duplo no Avançar e no Começar, dois
Enter seguidos (soltos) respondendo em ~15 ms, uma resposta só ao motor (o que a página manda ao `/responder`), a
campanha começando com o que se escolheu (o estado do jogo) e, depois da abertura, salvar e sair pela doca e carregar
o save pela lista (o cartão com a região e o modo; a ficha do mesmo herói). `PROPOSTA=r2` serve o jogo como está; a R
(cartões no painel) ainda roda, sem a caixa do tutorial (saiu da tela gráfica): o registro dela é a folha.
