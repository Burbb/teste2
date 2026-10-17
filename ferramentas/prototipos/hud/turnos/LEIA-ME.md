# A iniciativa e a passagem dos turnos (etapa 1C: protótipo aprovado, integrado na 1.116.0)

Pedido do Jean: o jogador deve perceber quando tem a vantagem de iniciativa, enquanto ela ainda vale e quando começa
um turno novo, com impacto e sem perder a velocidade. O protótipo abaixo foi aprovado e entrou no jogo na 1.116.0
("A integração", no fim).

## O que o motor diz (a fonte de tudo)

- **A sua iniciativa** (`Combate.executar`, `emboscada == "jogador"`):
  - o herói recebe o estado `iniciativa` (+25%, `bal.INICIATIVA_BONUS`), com o texto do motor "+25% de dano no
    primeiro golpe deste turno";
  - sai o lance `surpresa`, de `j`, com os inimigos como alvos;
  - **o turno 1 é só seu:** os inimigos, a comitiva e o animal entram no turno 2 (`pular_inimigos`);
  - o primeiro golpe seu sai +25% e consome o estado (`golpe.py`: o lance do golpe leva `bonus_motivo: "Iniciativa!"`,
    também dentro de uma salva em área);
  - se o turno livre for gasto noutra coisa (Meditar, uma poção, um buff), o estado é removido no fim da sua vez: a
    iniciativa **passa** sem bônus.
- **A emboscada deles** (`emboscada == "inimigo"`): o lance `surpresa` sai do inimigo mais ágil, que ataca sozinho
  antes do turno 1. Não é uma rodada do bando inteiro, e não conta turno.
- **O turno:** `self.turno += 1` no começo de cada volta do laço da luta, e `mostrar_estado` chama `ui.novo_turno(n)`
  logo no começo da sua vez, uma vez por volta, inclusive quando você a perde atordoado. A ponte manda a mensagem
  `turno` e o número em `estado.combate.turno`.
  - A comitiva, o animal, os servos e os inimigos agem dentro da mesma volta e não geram mensagem.
  - Hoje, a tela só escreve um divisor "turno N" no registro.

O protótipo só lê esses acontecimentos. Não conta mensagens nem animações, e não tem contador próprio.

## A proposta (`turnos.js`, `turnos.css`)

- **O anúncio:** uma faixa de pincel larga, a mesma das faixas aprovadas (as pontas do seletor e dos comandos,
  carvão, marfim e latão). Entra em ~150 ms e sai em ~1,1 s.
  - "Turno N", a cada mensagem de turno do motor.
  - No turno 1 com a iniciativa, um anúncio só: "Iniciativa!", com "Turno 1 · só você age agora" e o texto do motor
    ("+25% de dano no primeiro golpe deste turno"), em latão.
  - "Emboscada!", "Lobo ataca antes de você", em vermelho, quando o golpe livre deles vem antes do turno 1.
- **A placa:** uma faixa pequena com o turno de agora ("TURNO 3"), que fica para consulta.
  - Enquanto a iniciativa vale, ela ganha uma segunda linha: "Iniciativa: +25% no 1º golpe".
  - Quando a iniciativa acaba, a linha diz o que houve e sai: "Iniciativa usada (+25%)", em verde, ou "Iniciativa
    passou", riscada.
- **O lugar** é escolhido medindo, para nunca cobrir carta, comando, mira, seletor ou o aviso da cena.
  - **Na luta cheia** (ou onde a faixa dos comandos tem vão): o anúncio entra no vão embaixo da roda, e a placa fica no
    pé da faixa.
  - **Na luta pequena,** em que a roda ocupa a faixa inteira: o anúncio entra logo abaixo da arena, por cima do começo
    do registro (por ~1 s), e a placa fica presa à borda de baixo da arena. Ela some enquanto o seletor abre embaixo
    da arena, no mesmo lugar, e volta quando ele fecha.
  - O lugar da placa é decidido uma vez por luta e tamanho de janela, com a roda já medida: ela não muda de lugar
    quando a roda some na vez dos inimigos.
- **Sem espera:** a camada não recebe o mouse, e nada segura a fila de mensagens. A vez fica clicável no mesmo tempo da
  produção (medido: 9 a 62 ms depois da mensagem do turno, nas duas versões).
- **Movimento reduzido:** nada se desloca nem escala; o anúncio aparece inteiro e fica 1,8 s, e a placa continua (o fim
  da iniciativa fica 2,4 s).

## Conferido (`fotografar.mjs`, `comparar.py`; 9 lutas reais, ~110 s)

As lutas são de verdade: o cenário `tutorial` com `EMBOSCADA` e `LUTA_APOS_ESCOLHA` (novo, em
`tests/navegador/cenarios.py`: a luta começa num clique, com a página aberta). Sem isso, o começo da luta chegava
antes da página e era relido sem animar, então nem a produção mostrava a surpresa. Nada é simulado.

| luta | o que acontece | anúncios / mensagens do motor | cobre |
|---|---|---|---|
| paladino e Morel × 3 lobos, a sua iniciativa | turno 1 só seu; Habilidades, a mira e o Voltar; o ataque usa a iniciativa ("usada"); turno 2 | 2 / 2 | nada |
| a mesma, com a emboscada deles | "Emboscada!" com o lobo mais rápido; turno 1 | 1 + emboscada / 1 | nada |
| necromante, Morel, Odette e 3 servos × 5 caídos e o xamã, a sua iniciativa | turno livre em Meditar ("passou"); a comitiva e os servos agem sem anúncio; Maldição em área (efeitos em todos); turno 3; Habilidades | 3 / 3 | nada |

As lutas valem em 1280×720 (produção e proposta), e a proposta também em 1500×950 (a pequena e a cheia) e com
movimento reduzido. Folhas em tamanho real em `capturas/comparacoes/`: `iniciativa.png`, `emboscada.png`, `cheia.png`
e `janelas.png`. O ritmo está nos vídeos de `capturas/videos/`:
- `iniciativa-producao-1280x720.webm` e `iniciativa-proposta-1280x720.webm`: a mesma luta;
- `emboscada-proposta-1280x720.webm`;
- `iniciativa-proposta-1280x720-reduzido.webm`.

## Como abrir

    PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/turnos/abrir.mjs iniciativa
    (ou emboscada, cheia; "… cheia producao" abre sem o protótipo; REDUZIDO=1 para movimento reduzido)

Abre uma janela do Chromium de 1280×720 com a luta e o protótipo anexado à página; o jogo não muda. Clique em
"Começar a luta". Os vídeos abrem em qualquer navegador.

## Limites e o que fica para decidir

- **Na luta pequena,** o anúncio cobre o começo do registro por ~1 s (é o único lugar livre fora da arena). A
  alternativa seria um anúncio menor dentro da arena, sobre o cenário, mas a roda ocupa a faixa dos comandos inteira.
- **"Turno N" a cada turno:** numa luta longa, o anúncio repete sempre. Se cansar, o anúncio pode ficar só para o
  turno 1 e para a iniciativa, com a placa mostrando os seguintes.
- **Turnos perdidos:** pelo código (`fase_jogador` chama `mostrar_estado` antes de `processar_efeitos`), o turno em que
  você está atordoado também é anunciado, porque é uma volta da luta. O aviso de perder a vez continua o do jogo. Nestas
  lutas não houve atordoamento: isso não foi visto na tela.
- **Dentro da arena,** no instante em que ela se acomoda (uma carta entrando), a ponta transparente da faixa pode
  encostar numa carta que ainda desliza; a medida usa o lugar final das cartas.
- **Fora desta rodada:** o dado, a consulta aos atributos e a família visual comum com eles (plano 23, itens 1.4 e 1.6).

## A integração (1.116.0)

O que entrou no jogo, sem nada desta pasta:
- `rpg/web/static/turnos.js` (o módulo `Turnos`): a lógica do protótipo, chamada pelos pontos normais em vez de
  interceptar funções:
  - `paineis.aplicarEstado` chama `Turnos.aoEstado`;
  - `pagina.turno` chama `Turnos.aoTurno` (refazendo a página, só a placa: sem anúncios repetidos ao recarregar);
  - a fila de lances (`nucleo.js`) chama `Turnos.aoLance`.
- `rpg/web/static/css/19-turnos.css`: a folha do protótipo, fora da trava de pixel art, como as faixas.
- **O turno que você perde** (ficou sem cobertura no protótipo): o catálogo de estados que a tela recebe ganhou
  `perde_turno` (`estados.para_tela`, o que o motor já usa para tirar a vez). No começo de um turno em que um estado
  seu tira a vez, o anúncio diz "Turno 2 · Preso na teia: você perde este turno". A roda de comandos não aparece
  nesse turno (é o motor que não pergunta), então nada sugere que você pode agir. A contagem segue a do motor: o
  turno perdido é uma volta da luta, e o seguinte é o 3.

**O estouro de pixels** que aparecia logo antes da luta, nos vídeos:
- **O que era:** as partículas da festa de nível (`telas/celebracoes.js`, `particulas`). O cenário sobe o herói de
  nível antes da luta. Ao abrir, a página relê as mensagens da cena e passa cada festa "sem cerimônia" (a janela não
  aparece), mas o som e as partículas eram disparados antes dessa linha. Saíam 90 partículas por nível, 720 de uma
  vez.
- **Onde mais acontecia no jogo:** no texto "instantâneo" e ao recarregar a página.
- **A correção:** nas festas de nível, de Sigilo e de especialização, o som e as partículas passaram para depois da
  linha que encerra a festa sem cerimônia, como a vitória já fazia.
- **O que fica igual:** a festa de nível jogando, com a janela, o som e as 90 partículas. Nada a substitui.

Conferido (`integracao.mjs`; 10 cenários em ~100 s, lutas reais; `capturas-integracao/`):

| luta | anúncios / mensagens de turno do motor | partículas desde o carregamento | cobre |
|---|---|---|---|
| a sua iniciativa, 1280×720, 1500×950 e movimento reduzido (Habilidades, mira e Voltar, o ataque que a usa) | 2 / 2 ("Iniciativa!" com +25%, "Turno 2") | 0 (antes: 720) | nada |
| a emboscada deles | "Emboscada!" + 1 / 1 | 0 | nada |
| sem vantagem | 1 / 1 | 0 | nada |
| luta cheia com comitiva e 3 servos, 1280×720 e 1500×950 (Meditar: a iniciativa passa; Maldição em área) | 3 / 3 | 0 | nada |
| 3 aranhas, semente 7, normal e reduzido: preso na teia no turno 2 | 4 / 4 ("Turno 2 · Preso na teia: você perde este turno"; 0 comandos à vista) | 0 | nada |
| a festa de nível ao vivo / refazendo a página | — | 90 / 0 | — |

- **A vez clicável:** de 9 a 34 ms depois da mensagem do turno. Na luta das aranhas, ~320 ms nos turnos 3 e 4, pelas
  animações da vez delas e do "firme" depois da teia; o anúncio não espera nada.
- **Gravações** (`capturas-integracao/videos/`): `iniciativa-jogo-1280x720.webm`, `emboscada-jogo-1280x720.webm`,
  `atordoado-1280x720.webm` e `iniciativa-jogo-1280x720-reduzido.webm`.
