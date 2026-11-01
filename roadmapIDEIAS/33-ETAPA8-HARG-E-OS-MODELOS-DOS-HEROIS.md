# 33 — Etapa 8: Harg como o confronto principal e os modelos novos dos heróis (Campo Livre 8)

**01/11/2026 (data do computador local).** Estudo e protótipo (`ferramentas/prototipos/etapa8-campo/`, versão **Campo
Livre 8**; a 7 fica em `/v7/`), **nada aprovado**. Três frentes pedidas pelo Jean: consolidar a direção sóbria (o
[32](32-ETAPA8-DIRECAO-DE-ARTE-DO-CAMPO.md), seção 0, e a skill `arte-cenas-fenda`), redesenhar as miniaturas dos heróis e
reconstruir o confronto com um herói inimigo (Harg).

| Seção | O que tem |
|---|---|
| 1 | O problema: enfrentar Harg interrompia a diversão |
| 2 | Estudo de confrontos com chefes: observação, explicação de desenvolvedor, hipótese |
| 3 | O novo Harg: repertório, ritmo, fases |
| 4 | Resistência com sensação de progresso: a postura e a confirmação de acerto |
| 5 | Os dois contextos: o treino e a guerra |
| 6 | Os modelos novos dos heróis |
| 7 | Verificação e medições |
| 8 | Limitações, hipóteses e o que avaliar |

## 1. O problema

Nas palavras do Jean: matar tropas é muito divertido; enfrentar um herói inimigo parece uma interrupção, uma unidade maior
e resistente, com ataques pouco ameaçadores e confirmação de acerto fraca. O pedido é um rework do comportamento, não mais
vida, dano ou velocidade; concentrado em Harg; a versão anterior acessível (em `/v7/` e, no 8, nos encontros antigos: o
Harg reconstruído só vale nos encontros com `harg8`).

## 2. Estudo de confrontos com chefes

Três tipos de afirmação, separados: **observação** (o que se vê jogando ou em análises publicadas), **explicação de
desenvolvedor** (dita por quem fez, com a fonte) e **hipótese de adaptação** (o que nós fizemos com isso, a confirmar
jogando).

| Fonte | Tipo | O que diz |
|---|---|---|
| Hidetaka Miyazaki, entrevista à [Xbox Wire](https://news.xbox.com/en-us/2022/05/27/from-softwares-hidetaka-miyazaki-on-the-secrets-of-elden-rings-development/) (2022), lida | desenvolvedor | o cenário decide cedo qual chefe aparece ali, e "a jogabilidade do chefe também pode ser ajustada pelo mapa em que ele aparece"; a sensação de conquista é um tema mantido desde Dark Souls |
| Miyazaki citado pela [Cook and Becker](https://www.cookandbecker.com/en/article/295/elden-ring-it-s-all-about-the-boss.html) (*Dark Souls Design Works*), só o resumo da busca | desenvolvedor | a contradição como elemento do desenho de um chefe |
| Miyazaki sobre a postura de Sekiro influenciando a de Elden Ring ([GamesRadar](https://www.gamesradar.com/how-sekiro-influenced-elden-ring-according-to-hidetaka-miyazaki)), só o resumo da busca | desenvolvedor | o sistema de postura de Sekiro ajudou a formar a mecânica de postura (o equilíbrio que quebra) de Elden Ring |
| Masaru Yamamura (Sekiro) à [GamingBolt](https://gamingbolt.com/sekiro-shadows-die-twice-dev-talks-about-how-combat-differs-from-dark-souls-and-the-challenges-of-developing-it), só o resumo da busca | desenvolvedor | o desvio de Sekiro não é o aparo largo dos jogos de luta: a janela é curta |
| [SuperJump](https://www.superjumpmagazine.com/the-art-and-science-of-sekiros-combat/), *The Art and Science of Sekiro's Combat*, lida | observação | a postura substitui a resistência; esperar dá tempo de o inimigo recuperá-la; atacar sem plano é castigado; com a postura esgotada, a abertura do golpe mortal |
| Os atrasos de Elden Ring virando meme ([Automaton](https://automaton-media.com/en/news/20220316-10577/)), só o título; as discussões de jogadores | observação | os golpes atrasados (a preparação que segura) são uma marca do jogo e um ponto de frustração; as razões são teoria de jogador, não declaração |
| Guias de desenho de chefe ([salt-and-steel](https://salt-and-steel.pages.dev/docs/15/boss-design), [Choost Games](https://choostgames.com/blog/what-makes-a-good-boss-fight/), [uxdesign.cc sobre Black Myth: Wukong](https://uxdesign.cc/how-to-design-an-early-boss-fight-wandering-wight-boss-in-black-myth-wukong-6ec8408d06e0)), só o resumo da busca | observação | aviso, janela de reação e castigo em cada golpe; o aviso cresce com o perigo; o teste de justiça ("vejo o que eu devia ter feito"); a recuperação longa como a abertura |
| O nosso jogo (observação nossa) | — | câmera alta, sprites de 13 a 19 px, hordas ao mesmo tempo, habilidades em área, controle direto simples (andar, mirar, quatro habilidades, a mobilidade); sem esquiva com invulnerabilidade além da Investida e do Piscar |

**O que levamos (hipóteses de adaptação, cada uma testada no protótipo):**
1. **Preparação e leitura:** cada golpe tem o aviso no chão na forma exata do que acerta, do tamanho real; a
   preparação é legível na escala (0,42 a 0,78 s) e a execução é rápida (0,08 a 0,12 s, a Investida a 560 px/s). Nada de
   golpe atrasado depois do aviso: na nossa escala, um atraso escondido seria só injusto.
2. **Compromisso de direção:** ele vira para você só na primeira parte da preparação (35 a 55%), com o giro limitado
   (2 a 3,2 rad/s); depois a direção fica. Vira para onde você está, não para onde você vai.
3. **Variação de ritmo:** golpes curtos e longos misturados em sequências de 1 a 3, pausas sorteadas entre elas, um
   passo de lado às vezes; a Investida de longe.
4. **Aproximação e pressão:** sem golpe pronto, ele anda até o alvo (mais rápido de longe); recuar em linha reta não
   resolve: a Varredura Longa alcança quem só recua e a Investida fecha a distância.
5. **Sequências reconhecíveis e o golpe final:** Talho-Talho, Talho-Martelada, a Varredura sozinha; a Martelada é o
   golpe comprometido que deixa a abertura grande.
6. **Recuperação e contra-ataque:** depois da Martelada (1,25 s) e da Investida (0,65 s), ele fica parado levando +50% e
   o dobro de postura: a janela de castigo de verdade.
7. **Reação ao dano sem interrupção:** acertar mostra (faíscas, o tranco, o número, o trecho claro da barra), sem
   cancelar o golpe; o que o interrompe é a postura cheia (a quebra).
8. **Mudança de comportamento:** abaixo de 55% da vida, o Rugido (a passagem anunciada) e a fase 2, com sequências de
   três golpes, pausas mais curtas e a onda da Martelada; as preparações continuam do mesmo tamanho (muda o ritmo, não a
   leitura).
9. **O arredor como parte do chefe** (a ideia de Miyazaki sobre o mapa): na guerra, ele atravessa a infantaria, derruba
   soldados aos montes e ameaça Odette e os arqueiros; no treino, as árvores e a muralha são as coberturas e os limites.

## 3. O novo Harg

`tela/campo8.js`, números em `conteudo.HARG8`. A escolha de alvo é a do Campo Livre 7 (você, Morel, Odette ou as
tropas, com o tempo mínimo e a inércia): ele não volta a perseguir você para sempre nem abandona o duelo a cada soldado
perto (os golpes dele acertam todos os nossos na forma: os soldados no caminho caem junto).

| Golpe | Para quê | Preparação → execução → recuperação | Forma | No herói / na tropa | Como escapar |
|---|---|---|---|---|---|
| Talho | a pressão | 0,42 s (vira só nos primeiros 55%) → 0,08 s, avança 16 px → 0,32 s | arco de 130°, 30 px | 15 / 18 (um soldado cai) | para trás e para o lado; ou bater antes |
| Varredura Longa | quem só recua | 0,6 s → 0,12 s, avança 30 px → 0,5 s | arco de 150°, 52 px | 22 / 18 | para o lado de trás dele, ou a mobilidade |
| Martelada | o golpe final | 0,78 s → 0,1 s → **1,25 s aberto** (+50%, postura em dobro) | círculo de 30 px, 22 px à frente; na fase 2, a onda até 74 px | 32 / 24 | sair do círculo (e da onda); castigar depois |
| Investida | a aproximação, através da infantaria | 0,48 s (a faixa) → 560 px/s até 210 px; derruba quem está na faixa, para no primeiro herói, num pesado ou numa parede → **0,65 s aberto** | faixa de 11 px | 20 / 18 | sair da faixa |
| Rodopio | contra a tropa que o cerca (4 ou mais) | 0,6 s → 0,1 s → 0,55 s | círculo de 46 px | 24 / 18 | sair do círculo |
| Rugido | a passagem para a fase 2 (uma vez) | 0,8 s → empurra a nossa tropa (não atordoa) → 0,4 s | círculo de 64 px | 0 / 4 | — |

**Ritmo:** fase 1, sequências Talho-Talho, Talho-Martelada, a Varredura, o Talho; pausas de 0,7 a 1,1 s; metade das vezes
um passo de lado. Fase 2, Talho-Talho-Martelada, Varredura-Talho-Martelada, Talho-Varredura, Varredura-Martelada; pausas
de 0,4 a 0,7 s. A sequência continua só enquanto você está ao alcance do golpe seguinte: sair dela é a sua escolha.
**Sem controle encadeado:** os golpes dele empurram e ferem, não atordoam nem imobilizam você.

## 4. A postura e a confirmação de acerto

**A postura** (a barra fina amarela embaixo da vida de Harg, e faíscas nele quando passa de 70%): enche com o seu dano
inteiro, com 60% do de Morel e Odette, 25% do das tropas, metade do contínuo (fogo, sangramento), +6 por golpe forte, +20
por controle (atordoar, imobilizar, interromper, congelar não o prendem: viram postura) e em dobro na abertura. Esvazia
14 por segundo depois de 2 s sem levar nada (bater e fugir não acumula). **Cheia, quebra:** 2,2 s de joelhos, levando
+50%, perdendo o golpe que fazia, com a mensagem, o anel dourado, a pausa de impacto e o tremor. **Depois, firme por 7 s:**
a postura enche a 35% e não quebra de novo; no máximo 2,2 s de joelhos a cada 9,2 s, mesmo apanhando sem parar (o teste
confere). Funciona com todas as builds: o Guerreiro enche com golpes fortes e próximos; o Mago, com a Bola, as áreas, os
controles que viram postura e as explosões dos talentos (o contínuo conta pela metade).

**A confirmação de acerto:** cada acerto do herói em Harg tem faíscas, o som de impacto, o tranco do corpo (1 a 2 px,
sem pará-lo), o número e o trecho claro da barra que escorre depois de 0,35 s (o dano recente à vista). **Na abertura ou
na quebra:** o número dourado grande, o anel dourado, brasas e um tremor curto: a oportunidade bem aproveitada se sente
diferente do acerto comum. **Vida e dano** foram ajustados depois do comportamento: 1700 de vida (era 900) e a postura de
160, para o treino durar 44 a 70 s com o jogador automático que esquiva.

## 5. Os dois contextos

- **"Treino: Harg, o Capitão"** (`?enc=duelo`): só você e ele, do lado de fora da muralha, entre as árvores. Cada golpe se
  explica na primeira vez que aparece (a faixa da tela); `R` recomeça.
- **"Harg entra na batalha"** (`?enc=guerra`): o seu exército (28 soldados, 12 arqueiros, 6 pesados, 6 cavaleiros),
  Morel e Odette diante do portão; ondas de 34 soldados frágeis a cada 10 s até os 100 s; Harg entra pelo portão com a
  guarda aos 18 s (ou antes, se a frente inimiga cair). Enquanto ele estiver de pé, ninguém foge.

## 6. Os modelos novos dos heróis

**Referências** (lidas no 32 e nesta rodada): Slynyrd, *Pixelblog 47* (no muito pequeno, só o que a leitura pede; a
silhueta e um traço de identidade), *22* (o lado espelhado, a passada de poucos quadros, o boneco com a roupa por cima); os guias de leitura de sprites pequenos da [Wayline](https://www.wayline.io/learn/pixel-art/4) (a
silhueta sólida primeiro; conferir no tamanho do jogo e cortar o que vira borrão) e da [Bugnet](https://bugnet.io/blog/how-to-make-pixel-art-that-reads-clearly)
(a clareza vence o detalhe; o contraste entre o que importa e o fundo), e o [arquivo do NESdev](https://nesdev.nes.science/f21/t6892.xhtml)
(o chão de pouco contraste, para só o que importa se destacar), só o resumo da busca.

**O que mudou de fato** (não é troca de paleta: silhueta, equipamento, pose e as pernas desenhadas junto com o corpo em
cada pose, na mesma escala, 17 × 15; Harg 19 × 15):
- **Guerreiro:** a espada longa em diagonal sobre o ombro (a única silhueta inclinada do campo), a capa vermelha atrás, o
  elmo aberto com a crista dourada; a preparação recolhe a espada baixa para trás; o golpe a estica na horizontal, na
  direção do arco, com o pé da frente avançado.
- **Mago:** o chapéu alto de ponta dobrada e a aba larga dourada, o manto azul-escuro até o chão (antes, creme) com a
  faixa dourada, a barba clara, o cajado mais alto que ele com a esfera acesa; a preparação ergue o cajado com a esfera
  maior; o golpe estica o cajado com a esfera na frente.
- **Morel** (reconhecível pelo do jogo: o cabelo e a barba castanhos, as ombreiras largas, a túnica vermelha, a espada):
  o escudo redondo de madeira com o umbo na frente (a parede que ele é), a túnica vermelha embaixo, as ombreiras de ferro;
  a preparação ergue a espada atrás da cabeça; o golpe passa a espada por cima do escudo.
- **Odette** (pela do jogo: a touca branca, o véu escuro roído num ombro, a pequena cruz amarela): a touca clara em volta
  do rosto, o véu escuro caindo atrás com a ponta roída, o hábito comprido, a cruz no peito, o cajado com a luz; a
  preparação ergue a luz; o golpe a estica para a frente.
- **Harg:** curvado para a frente, os chifres de osso, a malha cinza, o manto de pele, a faixa vermelha, o machado de
  duas mãos com a lâmina maior; a preparação ergue o machado acima da cabeça; o golpe o leva baixo e à frente.

**Pose, arma e efeito no contato:** a pose de golpe aparece no mesmo passo em que o corte, o anel ou a explosão sai (o
herói: os primeiros 0,12 s da recuperação; Harg: a execução e os primeiros 0,18 s depois); a arma na pose aponta para o
lado do arco. **A folha comparável:** `capturas/cl8-folha-modelos.png` (os do Campo Livre 7 e os novos, as seis poses, no
tamanho do jogo e ampliados), refeita por `arte/folha.py`. **Em movimento:** `F9` troca os modelos (novos, os do 7, o herói
menor do estudo do 7) no meio da luta. **Fontes:** `arte/fontes/novos/` (uma camada por equipe, um quadro por pose).

**Tamanho:** nenhum mudou. Não apareceu uma necessidade concreta de leitura que pedisse crescer.

## 7. Verificação e medições

- **Regras** (`testes/campo8.test.mjs`, 9 testes): os três tempos e a direção marcada; o Talho acerta quem fica e não quem
  sai na diagonal depois do aviso; a Varredura alcança quem recua em linha reta depois de 0,3 s de reação; a Investida
  derruba a infantaria da faixa e para no herói, com a abertura; a abertura dá +50% e o dobro de postura; a postura quebra
  e depois fica firme (menos de 45% do tempo de joelhos apanhando sem parar) e o controle vira postura; a fase 2 (o
  Rugido, as sequências de três, a onda); na guerra, ele derruba 15 ou mais, troca de alvo e o herói não fica preso; no
  treino, quem sai dos avisos para o lado vence e quem só recua apanha muito mais. Os 77 testes da simulação passam.
- **Sem tela** (`ferramentas/harg8.mjs`, o jogador automático: o forte sai dos avisos para o lado, o médio recua em linha
  reta, os dois batem nas aberturas):

| Batalha | Forte (esquiva de lado) | Médio (recua reto) |
|---|---|---|
| treino, Guerreiro | vitória em 44 s, perde 23 de vida, 5 quebras, 54% do dano em Harg na abertura ou na quebra | derrota em 38 s (8 Talhos, 3 Marteladas, 3 Varreduras) |
| treino, Mago | vitória em 70 s, perde 68, 6 quebras, 61% na abertura | derrota em 64 s |
| guerra, Guerreiro | vitória, Harg derruba 45 dos nossos; em você 56% do tempo, Morel 28%, tropas 16% | vitória, ele derruba 16 |
| guerra, Mago | vitória, ele derruba 28; em você 51%, tropas 36%, Morel 13% | vitória, ele derruba 25 |

  Nenhum controle no herói vindo de Harg (0 s). Isto mede as regras; se o duelo é divertido, é o Jean jogando.
- **No navegador** (`ferramentas/conferir8.mjs`, 1920 × 1080 e 1280 × 720): os padrões (a sóbria, a violência intensa, os
  modelos novos); o treino com o golpe na barra, a postura, a quebra e o dano escorrendo; a guerra com Harg entrando e
  derrubando; a seleção e o comando com a câmera estável; o `/v7/`; sem erros no console; a guerra a 2× a 60 qps
  (simulação 1,4 a 1,5 ms, desenho 2,2 a 2,4 ms).

## 8. Limitações, hipóteses e o que avaliar

**Hipóteses (tudo):** o repertório, os tempos, a postura, a fase 2, os números; os modelos novos (pendentes da aprovação
artística).

**Limitações:** só Harg foi refeito (Ardis e o campeão continuam como antes); a Investida de Harg não tem pose própria
(usa a de golpe); os modelos novos têm as mesmas seis poses (sem quadros intermediários de golpe) e o caído continua o
recuo girado; o jogador automático esquiva melhor que uma pessoa no Talho (reage em 0,15 s); a tropa nossa sai dos avisos
de Harg como saía dos do Capitão (a regra de antes), então ele derruba menos do que derrubaria parada.

**Para o Jean avaliar, jogando o treino e depois a guerra:** (1) enfrentar Harg virou o confronto principal, e não uma
barra que atrasa a vitória? (2) dá para reconhecer cada golpe pelo aviso, a tempo, no tamanho real? (3) as aberturas
(depois da Martelada e da Investida, e a quebra) são aproveitáveis com o Guerreiro e com o Mago? (4) a confirmação de
acerto (as faíscas, o trecho claro, o dourado da abertura) dá sensação de progresso? (5) a fase 2 se nota pelo
comportamento? (6) na guerra, ele muda a batalha (abre a linha, derruba, ameaça) sem largar o duelo a cada soldado? (7) os
modelos novos: os cinco se reconhecem no tamanho do jogo, e Morel e Odette continuam os do jogo?
