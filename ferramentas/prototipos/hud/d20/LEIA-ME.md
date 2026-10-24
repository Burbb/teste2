# O d20: o redesenho do dado dos testes (etapa 2, protótipo, 24/10/2026)

**Nada disto está no jogo.** O jogo nunca lê `ferramentas/`. As propostas só existem nas páginas do servidor de teste
desta pasta: a demonstração e as do fotógrafo. A base é a 1.201.0, com as celebrações integradas, que não mudam.
Aguarda a escolha do Jean.

## Testar no navegador (a demonstração)

`demo.bat` abre o painel em **http://127.0.0.1:8766/**. O mesmo painel abre com:

```
python ferramentas/prototipos/hud/d20/auxiliares/demo.py
```

Cada linha é um caso, e os três botões são as versões: **Jogo atual**, **A · Marfim** e **B · Vidro**. Cada botão
encerra o caso anterior e sobe outro do zero, numa partida de teste com saves numa pasta temporária. O save do jogo não
é tocado.

**Como jogar um caso:**
1. Na página, escolha "Começar o teste (Explorar)".
2. No baú, escolha a opção indicada no topo: Percepção, ou Força no caso da Força.
3. No canto de baixo, "repetir" sobe o mesmo caso de novo e "painel" volta à lista.

**Outras velocidades:** o formulário no fim do painel abre um caso com outra velocidade do texto (lento, rápido,
instantâneo).

**Movimento reduzido:** no Chrome ou no Edge, F12 → ⋮ → More tools → Rendering → `prefers-reduced-motion: reduce`, e
"repetir". Também vale "Mostrar animações" desligado no Windows.

**Se o servidor parar:** feche a janela do `demo.bat` (ou encerre o `python` do painel) e abra de novo. A porta muda
com `DEMO_PORTA=<porta>`. Os casos usam portas livres próprias e terminam junto com o painel.

## O levantamento: onde o d20 aparece e como funciona hoje

### O motor

Só há um sorteio de d20 no jogo: `Testes.teste` (`rpg/sistemas/testes.py`). Ele é chamado em 73 lugares:

| onde | chamadas |
|---|---|
| eventos de classe | 21 |
| eventos comuns | 17 |
| biomas | 12 |
| comitiva | 10 |
| vila | 5 |
| noite | 5 |
| Caspar | 1 |
| missões (as correntes) | 1 |
| contratos (a Percepção automática ao cruzar com inimigos) | 1 |

**Os números do teste:**
- **O dado:** `randint(1, 20)`.
- **O bônus:** as parcelas fixas (o nível, o atributo de origem, a classe e a especialização) mais a da situação (a
  escuridão: −4 em Percepção e Destreza, sem luz).
- **A dificuldade:** a pedida pelo evento, +1 a cada dois níveis.

**As regras especiais valem em todos os testes:** o 20 natural sempre passa e o 1 natural sempre falha. Não existe
outro teste com outra regra, nem outro uso do d20. "Crítico!" e "Desastre" são só os nomes que a tela dá ao 20 e ao 1.
O evento recebe apenas passou ou não passou: não há consequência extra para um crítico ou um desastre.

**A mensagem `rolagem`:** atributo, `cd` (a dificuldade final), `d20`, `mod`, `total`, `sucesso` e `precisa`, o menor
d20 que passa (`precisa_no_dado`). A tela não decide nada.

### A tela: três apresentações

**1. O centro** (`app/rolagem.js`, `css/20-rolagem.css`, 1.117.0) aparece fora da luta, com o texto em velocidade
normal, lenta ou rápida.
- **O véu:** escurece a área principal.
- **O cabeçalho:** o nome do teste e "Dificuldade N".
- **O dado:** o SVG de `D20`, em `app/nucleo.js`, com 128 px.
  - Gira 950 ms, em quatro passos por volta, e pisca números ao acaso, que são enfeite.
  - Pousa no d20 do motor, com a borda verde, vermelha ou dourada.
- **A tirinha de pincel:**
  - durante o giro: "d20 + 2", "precisa de 10 ou mais" e as parcelas;
  - no pouso: "9 + 2 = 11" e "contra 12".
- **A faixa de resultado** (aprovada):
  - Sucesso: marfim inteira;
  - Falha: carvão rasgada;
  - Crítico! e Desastre: as mesmas, com mais peso.
- **O fim:** o resultado fica `ritmo(650)` à vista, e o grupo desce até a tirinha do texto.
- **Os sons:** dado; depois sucesso, falha ou crítico.

**2. A tirinha do texto** (`.rolagem`, `css/04-pagina.css`) usa o mesmo SVG em 60 px. Ela é o registro que fica na
página. Sozinha, sem o centro, ela gira e pousa:
- na luta (`estado.combate`);
- no texto instantâneo;
- ao refazer a página (`replay`).

**3. O ícone da ficha** ("Testes do d20", `telas/inventario.js`): o mesmo SVG em 22 px, sem número.

**Fora do desenho:**
- os rótulos das escolhas ("(Percepção +2 no d20)", da dica das escolhas);
- a linha do histórico ("▸ Percepção 13 contra 12 — sucesso (d20 11)").

**O que compartilha a apresentação:** o centro e a tirinha mostram o mesmo dado, o mesmo resultado e os mesmos sons.
O grupo do centro desce até a tirinha.

**O que tem comportamento próprio:**
- a tirinha sozinha (na luta, no texto instantâneo e ao refazer a página): sem o centro;
- a ficha: só o desenho, parado.

### Os comandos (o que não muda)

- **Pular:** um clique ou o Esc durante a rolagem corta o giro e o tempo do resultado.
- **O que não atravessa:** a proteção do jogo (`Gesto`, `app/nucleo.js`) não deixa um clique, um clique duplo ou uma
  tecla segurada responder a tela seguinte.
- **Sem clique novo:** não há clique para fechar o dado.
- **Movimento reduzido:** sem giro nem descida; o mesmo tempo.

### O escopo (plano 23)

O redesenho artístico do d20 entra no acabamento visual da HUD. A apresentação central, o ritmo e as faixas de sucesso
e falha já aprovados ficam.

## As duas propostas

As duas trocam só a função `rolagem` da página (`d20.js` e `d20.css`, carregados depois de `app/rolagem.js`). Recebem
a mesma mensagem, não sorteiam nada, mantêm o tempo e os sons e usam o véu, o cabeçalho, o pincel e as faixas de
resultado aprovados.

**O dado** é pixel art no tamanho nativo, ampliado 2× sem suavização:

| onde | nativo | na tela | antes |
|---|---|---|---|
| o centro | 70 px | 140 px | 128 px |
| a tirinha | 30 px | 60 px | 60 px |
| a ficha | 22 px | 22 px (1×) | 22 px |

**O número** sai de algarismos desenhados à mão e fica gravado na face da frente: 8×13 com traço de 2 no centro,
26 px de altura na tela; 3×5 na tirinha.

### A construção do dado (`desenhar_d20.py` → `d20-dados.js`)

Os tipos de operação, separados:
- **Calculado:**
  - a geometria do icosaedro de verdade (os 12 vértices e as 20 faces), visto de frente para uma face, um pouco de
    cima e da esquerda;
  - no repouso, os vértices da face da frente se abrem 12% (`FRENTE`), para dois dígitos caberem com folga, sem mudar
    a ligação das faces;
  - os seis quadros do giro (meia volta em torno de um eixo de simetria: o laço fecha), com o tom tirado da luz comum
    em faixas. É movimento: cada quadro fica 60 ms.
- **Escolhido à mão:**
  - o tom de cada face do repouso (`TONS`), pela luz comum de cima e da esquerda;
  - as quinas desenhadas (`ARESTAS`): o fio de luz, um tom acima da face mais clara, ou a sombra, um tom abaixo da
    mais escura;
  - os brilhos (`AJUSTES`);
  - os algarismos (`ALG_G`, `ALG_P`).
- **A conferência:** `prancha_d20.py` monta `pranchas/construcao.png` (o dado sozinho, nos estados e nos tamanhos). As
  fotos no jogo são a prova.

Os algarismos dão um traço de 4 px de espessura na tela, mais grosso que o Alegreya fino de hoje. O número ganha peso
sem precisar de brilho.

### A · Marfim (a conta numa tirinha)

- **O dado:** osso polido, marfim quente (o marfim da faixa de Sucesso). A face da frente é clara, as de cima mais
  claras, as de baixo caem para o castanho.
- **O número:** entalhado em tinta escura, com o lábio de baixo e da direita pegando a luz. A tinta segue o resultado:
  - escura no pouso neutro;
  - verde-musgo no Sucesso;
  - vinho na Falha;
  - castanho-ouro no Crítico, com o lábio dourado;
  - quase preta no Desastre.
- **O movimento:** o dado tomba de verdade (os seis quadros, com as marcas dos números nas faces que olham para a
  frente) e pousa caindo dois pixels. No pouso:
  - dois punhados de poeira;
  - no Crítico, estrelas douradas (quatro quadros, 270 ms).
- **A conta:** numa tirinha só, em quatro casas com rótulo: **dado + bônus = total, contra dificuldade**.
  - No giro, "? + 2 = ? contra 12".
  - Embaixo, "precisa de 10 ou mais" e as parcelas.
  - A dificuldade sai do cabeçalho: fica ao lado do total, onde a comparação acontece.

### B · Vidro (frente a frente)

- **O dado:** vidro fumê violeta (o violeta do arcano das celebrações, escurecido). Três coisas dizem "vidro":
  - as quinas de trás aparecem através das faces;
  - a luz que atravessa sai pela borda de baixo e da direita, em faixas;
  - um reflexo de janela na face de cima.
- **O número:** aceso por dentro, com o miolo claro e um brilho em volta. Pisca enquanto o dado tomba, como hoje. A cor
  segue o resultado:
  - marfim no neutro;
  - verde no Sucesso;
  - vermelho na Falha;
  - ouro no Crítico;
  - vermelho escuro no Desastre.
- **O pouso:** um anel hexagonal de pixels se abre na cor do resultado; no Crítico, as estrelas.
- **Frente a frente:**
  - à esquerda, uma placa com o **bônus** ("+2, somado ao d20"), que vira o **total** no pouso ("13, 11 no dado + 2");
  - à direita, a **dificuldade** ("12, precisa de 10 ou mais");
  - o dado fica no meio, e as parcelas embaixo.

### Nas duas

- **A nota da regra:** aparece embaixo da faixa só quando o 20 ou o 1 natural decidiu contra a conta:
  - "o 20 natural sempre passa", quando o total não chegava;
  - "o 1 natural sempre falha", quando o total chegava.

  A tela compara o resultado do motor (`sucesso`) com a conta (`total >= cd`). Na integração, o motor poderia mandar
  isso pronto.
- **A tirinha do texto:**
  - o dado pequeno tomba junto (no B, com o número piscando por dentro) e pousa no d20 do motor;
  - sozinha (na luta, no texto instantâneo e ao refazer a página), faz o mesmo de hoje com o dado novo.
- **A ficha:** o ícone pequeno do mesmo dado.
- **O movimento reduzido:**
  - o dado não tomba: fica no repouso e o número ainda troca, como hoje;
  - sem pulo, poeira, anel nem estrelas;
  - o resultado aparece de vez;
  - o tempo é o mesmo.

## Como foi conferido

### Os casos

Os casos reais são **testes de verdade**:
- o herói fica num lugar selvagem do mundo gerado;
- o Explorar (o caminho do jogo: a cena, a tocha, `eventos.disparar`) cai no baú abandonado, um evento do jogo;
- a escolha leva a `Testes.teste`.

O TESTE é só pôr o herói ali: a classe, o nível, a hora e o evento escolhidos. A semente de cada caso, achada por
`cenarios_d20.py procurar`, decide o d20 do motor; nada é forçado depois do sorteio.

| caso | o que mostra | o teste |
|---|---|---|
| sucesso | dois dígitos | guerreiro, Percepção: 11 + 2 = 13 contra 12 |
| falha | um dígito | 9 + 2 = 11 contra 12 |
| critico | o 20 natural | 20 + 2 = 22 contra 12 |
| desastre | o 1 natural | 1 + 2 = 3 contra 12 |
| forca | bônus alto | guerreiro de nível 6, Força: 15 + 9 = 24 contra 14 |
| escuro | bônus negativo | à noite, sem tocha: 14 − 2 = 12 contra 12, sucesso no limite |
| longo | a conta mais longa | arqueiro de nível 7 à noite: 6 + 7 = 13 contra 15; parcelas "nível +3 · Agilidade 16 +5 · olhos de arqueiro +3 · escuridão −4" |

**O laboratório (SIMULAÇÃO)** monta mensagens à mão, pela regra do jogo, para o que o herói de teste não alcança. Nada
é sorteado e nada acontece depois.

| simulação | a conta | o que mostra |
|---|---|---|
| `sim_so20` | Carisma 20 + 1 = 21 contra 22 | só passa com 20 |
| `sim_so1` | Força 1 + 14 = 15 contra 12 | só falha com 1 |
| `sim_carisma` | 17 − 3 = 14 contra 13 | bônus negativo |

### Fotos (`auxiliares/fotografar.mjs`, `capturas/`)

- **O que fotografa:** todos os casos, nas três versões, a 1920×945 (a área do jogo no monitor do Jean) e a 1280×720.
  Em cada um:
  - o giro;
  - o resultado;
  - a tirinha que fica depois.
- **Movimento reduzido:** a falha, o 20 natural e o 1 que decide, a 1920.
- **A velocidade lenta do jogo:** as fotos usam essa velocidade. A imagem é a mesma; só dá tempo para a câmera.

**As folhas** (`folha-1920.png` e `folha-1280.png`, por `auxiliares/folha.py`) trazem recortes 1:1, com a mesma região
nas três colunas.

As capturas cruas não vão para o repositório (126 MB; `.gitignore`). Ficam os relatórios `capturas/relatorio*.json` e
`capturas/gestos.json`, e o `fotografar.mjs` refaz as fotos.

### Gestos (`auxiliares/gestos.mjs`, `capturas/gestos.json`)

Os mesmos casos e gestos nas três versões, na velocidade normal. Ver "Resultados" abaixo.

## Resultados

### Gestos (`gestos.mjs`, 1920×945, velocidade normal)

27 de 27 conferências ok: 9 por versão (atual, A e B).

| conferência | atual | A | B |
|---|---|---|---|
| da tirinha à consequência (sucesso, falha, 20 natural) | 1622–1633 ms | 1629–1635 ms | 1636–1637 ms |
| pular com um clique: o centro some depois de | 123 ms | 84 ms | 85 ms |
| pular com o Esc: o centro some depois de | 65 ms | 68 ms | 89 ms |
| movimento reduzido: da tirinha à consequência | 1627 ms | 1631 ms | 1633 ms |

- **O ritmo:** 950 ms de giro, `ritmo(650)` e o texto, nas três. A diferença é de alguns milissegundos, menos de um
  quadro: é o desenho do canvas a cada 60 ms.
- **O número:** o canvas do resultado é, pixel a pixel, o dado desenhado com o d20 da mensagem (11, 9 e 20).
- **Pular:** o resultado é o mesmo, e nada responde a tela seguinte.
- **Gestos que não atravessam:** quatro cliques a 90 ms e o Enter segurado durante a rolagem. Nenhuma resposta sai
  sozinha; a pausa depois do baú continua esperando.
- **Movimento reduzido:** nenhum efeito de pouso nem animação no dado.
- **Texto instantâneo:** nada no centro; a tirinha sai com o d20 do motor.
- **Nada acumula:** nenhum centro nem efeito de pouso fica na página depois de cada rolagem.

Os sons são os mesmos de hoje, chamados nos mesmos momentos. Não foram ouvidos nesta máquina.

### Fotos

Todas sem erro na página. O resultado do histórico é igual nas três versões, caso a caso.

### Verificações do jogo

O jogo não mudou: `unittest` (689 ok, 1 pulado), gabarito ok e pyflakes só com os avisos conhecidos. A fumaça não
rodou, porque nada fora desta pasta mudou.

## A recomendação: A · Marfim

**Por que A:**
- **O número lê de longe.** O dado claro com o número escuro é o elemento mais claro sobre o véu, e o contraste não
  depende de brilho.
- **A conta fica clara.** Uma linha com rótulo (dado + bônus = total, contra dificuldade) organiza os quatro dados que o
  jogo mostra, na ordem em que se lê. A dificuldade fica ao lado do total, onde a comparação acontece.
- **Ela preserva a apresentação aprovada.** A coluna é a mesma, a largura também (440 px contra 400), e a descida até a
  tirinha é natural.
- **O material conversa com a HUD.** O marfim é o da faixa de Sucesso e das escolhas marcadas.
- **O tombo é físico.** Ele diz "dado" sem piscar números.

**O que B faz melhor:** o frente a frente compara o total e a dificuldade de um olhar só, e o número aceso tem mais
festa. Mas B tem custos:
- traz um violeta novo para a HUD (o da Fenda, que hoje só aparece nas celebrações do arcano);
- o grupo tem 600 px, quase toda a área principal a 1280×720;
- as placas usam letra de 12,5 px.

Material e composição são independentes: dá para levar o dado de um com a conta do outro.

## Limitações percebidas no tamanho real

- **O número da tirinha do texto é menor que o de hoje.** Os algarismos de 3×5 a 2× dão 10 px de altura; o SVG de hoje
  tem uns 15 (a fonte de 21 px). A conta ao lado repete o número.
  - Uma saída medida: o dado da tirinha com 34 px nativos (68 na tela) e algarismos de 4×6 (12 px).
  - Ganha pouco e alarga a linha do texto. Fica para a integração, se fizer falta.
- **O ícone da ficha (22 px, 1×)** lê como um d20 pela silhueta e pelos tons. Os detalhes não aparecem nesse tamanho.
- **O Crítico do A** tem a tinta castanho-ouro, mais contida que o dourado de hoje. A festa vem da faixa e das estrelas
  (270 ms).
- **O dado do centro tem 140 px, 12 a mais que hoje,** para o número de dois dígitos ter 26 px de altura.
- **Os quadros do giro saem da geometria**, sem retoque: são movimento e ficam 60 ms cada. O repouso tem os tons, as
  quinas e os brilhos escolhidos à mão. Se uma proposta for aprovada, o repouso pode ganhar acabamento pixel a pixel
  no Aseprite antes da integração (`pintar.lua`), como as peças da HUD.
- **Com zoom não inteiro no navegador (125%),** os pixels de 2× ficam com larguras desiguais, como no mapa.
- **O B a 1280×720:** as placas e o dado ocupam quase toda a largura da área principal; o texto de trás aparece nas
  bordas da poça.

## Arquivos

| arquivo | o que é |
|---|---|
| `desenhar_d20.py` | a construção; grava `d20-dados.js` e `pranchas/` |
| `numero.json` | a tinta do número por estado |
| `prancha_d20.py` | a prancha de construção |
| `d20.js`, `d20.css` | as propostas, só no servidor de teste |
| `auxiliares/cenarios_d20.py` | os casos reais, o laboratório e a procura das sementes |
| `auxiliares/demo.py`, `demo.bat` | o painel |
| `auxiliares/fotografar.mjs`, `auxiliares/gestos.mjs` | as fotos e os gestos |
| `auxiliares/folha.py` | as folhas |
