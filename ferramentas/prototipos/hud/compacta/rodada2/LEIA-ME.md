# A composição compacta, rodada 2 (protótipo, em avaliação)

O Jean aprovou a direção B (o seletor sobre a ficha quando não há espaço embaixo da arena) e pediu duas coisas antes
de integrar: o custo numa linha própria na coluna estreita e uma investigação do registro sem espaço. **Nada disto
entrou no jogo**; regras, custos, sorteios e versão intactos. As trocas ficam em `r2.mjs` (sobre as da rodada 1, em
`../compacta.mjs`), as folhas em `b2-seletor.css` e `r-registro.css`, o registro em `r-registro.js`.

## As versões, com os mesmos dados

- **b, a B da rodada 1, corrigida.** A rodada 1 tinha um defeito que as medidas não pegaram: o seletor, movido para o
  fim da página, ficava na tela depois de escolher a habilidade (durante a mira), porque a limpeza da roda não o
  alcançava. Corrigido aqui, junto com o resto do funcionamento pedido: a ficha coberta fica inerte (sem clique nem
  foco por trás); o seletor entra logo depois da ficha, e o Tab segue dele para a arena; redimensionar acompanha a
  coluna da ficha.
- **b2, a B refinada:** na coluna da ficha, o custo numa linha própria, embaixo do nome, e o motivo de não poder
  embaixo do custo; o "Esc · Voltar" sobe para a linha do título (o que a produção já faz na janela baixa). Letra,
  ícones, teclas, pontas da faixa e vãos são os do seletor; nada diminuiu. Embaixo da arena, o seletor é o de sempre.
- **r, a b2 com o registro na coluna do mundo** (a proposta para o registro, abaixo).

## 1. O custo numa linha própria (b × b2, 1280×720)

| | b (custo ao lado) | b2 (custo embaixo) |
|---|---|---|
| Arqueiro: nomes em 3 linhas | "Chuva de Flechas", "Fúria da Natureza" (esta estoura a coluna) | nenhum; só esses dois em 2 linhas |
| Arqueiro: custos alinhados | não (cada um onde o nome acaba) | sim, numa coluna |
| Arqueiro: lista / descrição | 437 / 150 px, a linha do dano do Tiro Duplo fica escondida | 448 / 163 px, o texto inteiro à vista |
| Necromante: lista / descrição | 412 / 160 px | 430 / 160 px |
| Itens (5) | 5 de 5 | 5 de 5 |

**Escolha: b2.** Em tamanho real, os nomes se leem de uma vez, e os custos se comparam descendo pela mesma coluna. A
lista cresce 11 a 18 px, mas o Voltar no título devolve isso à descrição, que fica igual ou maior. Todas as habilidades
e todos os itens continuam à vista sem rolar.

**O funcionamento (b2, a luta maior em 1280×720, movimento reduzido):**
- **Teclado:** a tecla 2 abre o seletor com o foco na primeira habilidade. As setas chegam à quinta, inteira à vista,
  com o foco visível e a descrição dela. Sem animação.
- **A ficha coberta:** os pontos da ficha caem no seletor, e a ficha fica inerte. Os controles abaixo da vista (a
  bolsa, onde a ficha rola) também ficam inertes. Um clique na área neutra do seletor não abre nada da ficha e não
  fecha o seletor.
- **Tab:** seletor → seletor → arena → … → mundo; nunca a ficha.
- **Redimensionar** (1366×768, 1280×650, de volta a 1280×720): o seletor cobre a ficha certinho, a habilidade
  examinada e o foco ficam como estavam, e as cartas estão no mesmo lugar com o seletor aberto e fechado.
- **Esc** fecha e devolve o foco a Habilidades. Clicar fora fecha. Escolher uma habilidade tira o seletor e devolve
  a ficha (antes da correção, o seletor ficava na tela).
- **A carta do herói** continua com vida, recurso e estados durante tudo isso.

## 2. O registro sem espaço: o que o motor produz de verdade

`../efeitos_reais.py` faz o robô de `tests/arena.py` lutar com as 6 especializações no nível 12, com a comitiva cheia
(os três pares possíveis de companheiros), o animal do patrulheiro e os servos que cada build controla, contra os 10
maiores bandos reais (o máximo da família mais um; os caídos com o xamã de escolta). São 20 lutas por combinação, 1.200
lutas em ~14 s. A cada vez do herói, lê as cartas como a tela as recebe: 7.364 momentos (`../capturas/efeitos-reais.json`).

- **O caso simulado da rodada 1 não é extremo:** uma linha de efeitos em cada carta é o que acontece numa luta cheia.
  Contra 5 caídos e o xamã, as 6 cartas inimigas ficam com efeito ao mesmo tempo com o paladino e o berserker
  (enfraquecer em área), o piromante (chamas), o necromante (Maldição) e o patrulheiro (5 de 5 vivos, sangramento da
  Chuva de Flechas), já no turno 2 ou 3. Os ícones de uma carta vão a no máximo 4, que cabem numa linha: o que cresce
  é o número de cartas com efeito, não as linhas de cada uma.
- **A altura real:** a mesma da simulação (uma linha de ~28 px por carta). Com os efeitos de um momento real
  (necromante, semente 1013, turno 2: Maldição nos 6), a arena vai de 433 a 578 px em 1280×720, e o registro fica com
  **19 px**. Com o arqueiro (semente 1013, sangramento nos 5 vivos), fica com **51 px, ~1 linha**. Em 1500×950 sobram
  245 px (~7 linhas).
- **Achado nas regras de crescimento** (registro, sem mudar nada): o necromante chega a **7 aliados vivos**. São os
  servos da build, mais o "Senhor dos Mortos" (o primeiro inimigo morto se levanta como servo). A conta dele usa
  `len(cb.mortos) == 1`: quando o xamã revive um caído, a lista de mortos encolhe, e a próxima morte conta de novo
  como a primeira (2 servos a mais em 2 das 20 lutas). Fica para o Jean decidir se é a regra pretendida.
  - Correção à rodada 1: a luta "cinco" (5 lobos) não acontece no jogo; uma matilha vai a 4. Ratos e caídos vão a 5,
    e os caídos com o xamã, a 6.

**A proposta (r):** no começo de cada luta, uma vez, o protótipo projeta a coluna mais alta com uma linha de efeitos
em cada carta. Se isso deixasse menos de 140 px (~5 linhas) para o registro embaixo, o registro passa, para a luta
inteira, para a coluna do mundo, embaixo do nome do lugar, da região, do nível e dos avisos da noite. Ele fica por cima
do minimapa, da missão e dos caminhos, que ficam inertes e voltam quando a luta acaba.
- **Medido:** 424 × 270 px, ~13 linhas, com ou sem efeitos (antes: 164 px parado, e 0 a 1 linha com os efeitos
  reais). A quantidade de texto à vista é parecida com a de hoje parado (~5 linhas largas contra ~13 estreitas), mas
  não some quando os efeitos aparecem.
- **Nada some da luta:** nomes, recursos, estados e alvos ficam inteiros; nenhuma letra diminuiu; as cartas não se
  mexem por causa dele; ele não troca de lugar no meio da luta.
- **Em 1500×950** não é acionado (há espaço), e o registro fica embaixo.

**Os compromissos para decidir:**
- **O que fica coberto:** durante uma luta cheia em janela baixa, o minimapa, a missão e os caminhos ficam cobertos
  (nenhum deles se usa na luta).
- **Mais quebras:** o registro fica mais estreito, então as linhas quebram mais (um ferimento ocupa 4 linhas).
- **Decisão por luta:** a escolha vale para a luta inteira, então o registro muda de lugar mesmo antes de os efeitos
  aparecerem; decidir no meio da luta faria o registro pular.
- **Espaço livre:** embaixo da arena sobra um vão (~50 px) que ninguém usa.
- **Janelas estreitas:** abaixo de 1100 px a coluna do mundo não existe e nada muda. Lá o problema continua, e a
  saída seria outra (o Histórico, no topo, já guarda o registro inteiro).

**Recomendação:** integrar a b2 e o registro na coluna do mundo juntos, com o gatilho como está. As alternativas
descartadas sem protótipo:
- esconder efeitos ou diminuir letras (pedido);
- as cartas mais juntas ou os efeitos na linha do nome (a rodada 1 mostrou que cortam nomes);
- a lista de inimigos rolando (esconde alvos);
- o registro sobre a ficha (é onde o seletor abre).

## Como reproduzir e o tempo

```
python ferramentas/prototipos/hud/compacta/efeitos_reais.py 20
node ferramentas/prototipos/hud/compacta/rodada2/fotografar.mjs      (PLAYWRIGHT_MODULO no ambiente)
python ferramentas/prototipos/hud/compacta/rodada2/comparar.py
```

- **A bateria:** 9 cenários em ~130 s (`capturas/logs/bateria.log`).
  - Em 1280×720: o arqueiro e o necromante × b, b2 e r (Habilidades, Itens, a mira, os efeitos reais).
  - Em 1500×950: só os efeitos reais, b2 e r.
  - Mais o cenário do teclado, da ficha e do redimensionar.
- **Sem repetir o que a rodada 1 já cobriu:** a produção e a A, as lutas pequenas, 1920×1080, a saída e a entrada
  simuladas.
- **As esperas** são as da rodada 1, com o mesmo diagnóstico: 0,6 s depois de abrir um menu (a entrada das faixas e a
  medida da descrição); 0,7 s depois de redimensionar (o batalha.js reacomoda 150 ms depois do último resize).
- **Versionadas:** só as 7 comparações em tamanho real (`capturas/comparacoes/`), o relatório e o log.
