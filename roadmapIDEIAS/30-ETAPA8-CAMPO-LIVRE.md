# 30 — Etapa 8: o combate em campo livre (herói em tempo real e tropas pequenas)

**31/10/2026.** Pedido do Jean: depois de jogar o protótipo tático (o [29](29-ETAPA8-COMBATE-TATICO.md)) e gostar do
ganho espacial, **investigar direto o combate em campo livre**: controle direto do herói, em tempo real, no meio de
tropas pequenas que lutam sozinhas, com poucas ordens coletivas. Pesquisa orientada à implementação e um protótipo
isolado. **O combate do jogo não mudou (1.220.0); a integração continua pendente de avaliação.**

Ligações: o [28](28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md) (builds), o [29](29-ETAPA8-COMBATE-TATICO.md) (a grade,
preservada como histórico, sem expansão nesta rodada), o [plano 23](23-PLANO-DE-ARTE-INTERFACE-E-COMBATE.md) e a
[continuidade](00-COMECE-AQUI.md). Protótipo:
[`ferramentas/prototipos/etapa8-campo/`](../ferramentas/prototipos/etapa8-campo/LEIA-ME.md) (`demo.bat`, porta 8801).

| Seção | O que tem | Natureza |
|---|---|---|
| 0 | A decisão e o critério desta entrega | Registro |
| 1 | Pesquisa: referências e o que cada uma deu | Pesquisa com fontes |
| 2 | A implementação: o que foi reaproveitado e o que foi separado | Decisão técnica |
| 3 | Campo, escala e representação | Decisão e medida |
| 4 | Controle direto e o compromisso dos golpes | Regra do protótipo |
| 5 | Os dois kits | Regra do protótipo |
| 6 | O impacto | Regra do protótipo |
| 7 | Tropas, ordens, movimento e ocupação | Regra do protótipo |
| 8 | A batalha | Conteúdo |
| 9 | Verificação: funcionamento | Testes e medidas |
| 10 | Verificação: sensação | Observado e o que só o Jean responde |
| 11 | Desempenho | Medida, com as condições |
| 12 | Limitações conhecidas | Lista |
| 13 | O que esta direção mudaria no jogo (não implementado) | Estimativa |
| 14 | O que avaliar jogando | Para o Jean |

---

## 0. A decisão e o critério

- **Nova direção do experimento:** campo livre com herói em tempo real e tropas pequenas. Substitui, como próximo
  experimento, a expansão do tático; **não** substitui o combate do jogo.
- **O tático fica preservado** (`etapa8-tatico/`, o 29), sem expansão nesta rodada. O X1 (`etapa8-builds/`) também.
- **Fora:** Revezamento e qualquer manipulação da ordem dos turnos (recusados; aqui não há turnos); castelos, reino,
  recrutamento, salários, mapa estratégico, campanha de exércitos; inventário, diálogos, cenas e progressão.
- **Critério principal:** mover o herói e acertar uma habilidade num grupo de soldados pequenos precisa ser fluido,
  legível e satisfatório, com vontade de repetir.

## 1. Pesquisa: referências e o que cada uma deu

As cinco capturas enviadas pelo Jean foram vistas nesta conta: quatro de **Sword & Banner** (o deserto com cavalaria
azul contra infantaria verde, a ponte na neve, o campo com cavalaria vermelha, o cerco à muralha) e uma de
**9 Kings** (o exército roxo diante do rei negro). O que foi aproveitado delas é a **escala e a leitura**: soldados
de uns 8 a 12 px de altura numa ampliação inteira, cor de equipe chapada no corpo, cabeça/elmo claro, a arma como um
risco branco, sombra no chão, piso calmo com poucas manchas, e o conjunto lido como massas de cor. Não foram usados
construções, gerenciamento, formações de centenas, nem nenhum asset.

| Referência | O que foi visto ou lido | O que entrou no protótipo |
|---|---|---|
| **Sword & Banner** (Bitrot Games; [Steam](https://store.steampowered.com/app/4957080), [GamingOnLinux](https://www.gamingonlinux.com/2026/07/mount-blade-meets-total-war-in-the-upcoming-pixel-art-sword-banner/), [Niche Gamer](https://nichegamer.com/sword-banner-is-a-stunningly-pixelated-rts-epic/)) | As capturas; os textos: RTS em pixel, "Mount & Blade meets Total War", unidades individuais, ainda não lançado (playtest) | A escala das unidades, as cores de equipe, a sombra. Ele é RTS (seleção e comando de grupos): o controle direto do herói **não** vem dele |
| **9 Kings** (Sad Socket; [Xbox Wire](https://news.xbox.com/en-us/2025/08/13/9-kings-pc-game-pass-preview/), [Rogueliker](https://rogueliker.com/9-kings-early-access-review/)) | A captura; os textos: autobatalha, o jogador quase não age durante a luta | Unidades miúdas em bloco, o "rei" maior e de outra cor que o resto (aqui: o herói mais claro, com contorno e anel no chão). A passividade dele é o oposto do que se quer |
| **Mount & Blade II: Bannerlord** ([guia de táticas](https://gamerguides.com/mount-and-blade-ii-bannerlord/guide/introduction/useful-gameplay-tips/tactics), [Steam](https://steamcommunity.com/app/261550/discussions/0/2264689848035590880)) | As ordens por F1/F2/F3: seguir, atacar, manter posição; o jogador luta pessoalmente | As três ordens coletivas (Acompanhar, Atacar, Defender aqui), sem seleção de grupos nem formações |
| **Dynasty Warriors / musou** ([wiki da série](https://koei.fandom.com/wiki/File:NPC_8_(DWU).png), [Siliconera](https://www.siliconera.com/here-are-dynasty-warriors-origins-semi-unique-officers/), [TechRadar](https://www.techradar.com/gaming/dynasty-warriors-origins-review)) | Tropa comum é interrompida pelos golpes de um oficial; oficiais têm uma barra de resistência; a crítica recorrente é "sempre o mesmo golpe" | Três camadas: soldado (cai de uma vez), veterano (aguenta um golpe forte) e as ameaças (campeão, porta-estandarte); golpe forte interrompe; o kit varia o golpe (arco, linha, círculo, parede) para não ser só um |
| **Masahiro Sakurai, hitstop** ([Source Gaming, coluna Famitsu 490](https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/), [Nintendo Wire](https://nintendowire.com/news/2022/12/12/this-week-in-sakurai-12-5-12-11-fine-tuning-hit-stop-and-cheating-the-system/)) | A parada curta no impacto, maior para golpe mais forte; vale para todo gênero | A pausa de impacto proporcional (45 a 100 ms) só nos golpes fortes; o básico só congela o alvo (40 a 70 ms), não a tela |
| **Squirrel Eiserloh, "Juicing Your Cameras With Math"** (GDC 2016; [Game Developer](https://www.gamedeveloper.com/programming/video-sprucing-up-cameras-with-math)) | O tremor por "trauma": o golpe soma trauma, ele cai sozinho, o deslocamento é o trauma ao quadrado | O tremor exatamente assim (queda 1,8/s, até 6 px nativos), mais um empurrão curto na direção do golpe; intensidade 0 a 150% |
| **Jan Willem Nijman, "The Art of Screenshake"** (Vlambeer, INDIGO 2013; [Kenney](https://kenney.nl/learn/must-see-videos-for-indie-developers)) | Só a descrição (o vídeo não foi aberto) | A lista de reforços de impacto (clarão no alvo, recuo, partículas, marcas que ficam, som), sem depender de um só |
| **Combate cancelável** ([Game Developer, God of War](https://www.gamedeveloper.com/pc/combat-canceled-i-god-of-war-i-action-game-design), [Aztez](https://aztez.com/blog/2012/05/24/the-amalur-problem/)) | Cancelamento antes e depois do contato; o comando guardado ("buffer") que pode ser trocado | A regra do compromisso (seção 4): a preparação do golpe forte prende; depois do contato, andar ou outra habilidade cortam a recuperação; o comando guardado por 0,2 s |
| **Maddy Thorson, "Celeste & Forgiveness"** ([o texto](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)) | O comando apertado um pouco antes da hora sai quando der | O adiantamento de 0,2 s |
| **Craig Reynolds, steering** ([notas de curso](https://courses.cs.washington.edu/courses/cse457/15au/projects/animator/linkedItems/flocking.pdf)); **Elijah Emerson, flow fields** (Game AI Pro, cap. 23; [CRC](https://www.taylorfrancis.com/books/9780429100277/chapters/10.1201/b16725-29)) | A separação por vizinhos próximos; a grade espacial para achar vizinhos; campos de fluxo para milhares | A separação numa grade espacial (células de 12 px) e alvos com vagas. Campo de fluxo **não** foi preciso: o campo é aberto e sem obstáculos (só a Muralha, tratada como obstáculo macio) |
| **Riot, "Clarity in League"** ([texto](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/), [guia de VFX](https://nexus.leagueoflegends.com/wp-content/uploads/2017/10/VFX_Styleguide_final_public_hidpjqwx7lqyx0pjj3ss.pdf)) | A área desenhada tem de bater com a área que acerta; ruído visual mínimo; efeito alto só quando o impacto é alto | A área pintada pela **mesma função** que decide quem é atingido (seção 9); o clarão da explosão dura ~60 ms; fumaça fraca; marcas discretas |
| **Pixel art miúda** ([Slynyrd, Pixelblog 59](https://www.slynyrd.com/blog/2025/11/28/pixelblog-59-tiny-sci-fi-pixels)) | Poucos quadros com poses fortes; volume constante; não girar sprite pequeno em ângulo livre | Seis poses por tipo; o corpo arremessado gira de 90 em 90° (exato na grade) |

**Limites da pesquisa:** Sword & Banner não está lançado (só capturas e textos de imprensa); de 9 Kings, a captura e
análises; Bannerlord, guias e fóruns (as teclas mudam por versão); o capítulo de Emerson e a palestra de Nijman só por
resumos. A experiência deles não foi jogada nesta conta.

## 2. A implementação: o que foi reaproveitado e o que foi separado

- **Separado:** a simulação é JavaScript no navegador (`tela/sim.js`), com passo fixo de 1/60 s e semente, sem DOM (roda
  igual no Node para os testes). Forçar o motor Python por turnos a simular 60 passos por segundo pela rede local seria
  frágil (latência, estado duplicado, um vaivém por quadro). O servidor do protótipo só serve arquivos.
- **Reaproveitado:** o padrão dos lançadores (versão no topo, porta livre, quem ocupa a porta), a paleta e as fontes da
  interface (`/static/css/01-base.css`, `11-tipografia.css`, `sprites.js` para as variáveis), o modo de som do jogo (Web
  Audio sintetizado, como `rpg/web/static/som.js`), a ideia de "Sensação" do jogo (`sensacao.js`: parada no impacto e
  tremor com os números num lugar só, aqui `IMPACTO` em `conteudo.js`), a semente fixa para repetir (como o X1 e o
  tático), o formato das descrições da skill `texto-regras-fenda` (efeito primeiro; custo e recarga no componente).
- **Não reaproveitado:** as habilidades do jogo (`rpg/habilidades.py`) e as do X1/tático não foram convertidas; os kits
  daqui são pequenos e novos (seção 5). Nenhum retrato em círculo: os combatentes são sprites de corpo inteiro.

## 3. Campo, escala e representação

- **Escala nativa e ampliação:** o canvas tem o tamanho da janela dividido por uma ampliação **inteira**
  (`floor(min(largura/600, altura/300))`): **2× em 1280×720** (640×360 px nativos visíveis) e **3× em 1920×945** (640×315).
  O CSS amplia com `image-rendering: pixelated`: nenhum pixel borrado, nenhuma escala fracionária.
- **O campo** tem 960 × 560 px nativos (maior que a tela: a câmera anda), piso verde com poucas manchas largas e
  pontilhadas, tufos, pedrinhas e flores raras; fora dele, um gramado mais escuro com moitas.
- **Os combatentes** (`tela/sprites.js`, grade de letras desenhada à mão; a folha em `tela/folha.html`): soldado,
  arqueiro e porta-estandarte em 13 × 13 (o corpo tem uns 6 × 11), veterano com escudo maior, campeão em 19 × 17, os
  heróis em 17 × 15 com contorno escuro. Poses: parado, duas passadas, preparo, golpe, recuo; caído e os quatro giros
  do arremesso saem do recuo girado 90°. As mãos são pontinhos de pele (como as figuras de cena). Sem contorno nos
  soldados (a sombra no chão os separa do piso); o **herói** tem contorno, a cor mais clara do campo, um **anel
  dourado** no chão e é **desenhado por cima de todos** (decisão: nunca some na multidão; troca uma imprecisão de
  profundidade pela leitura).
- **O que fica recolhido:** o registro e o diagnóstico (Tab). Na tela ficam só a ficha do herói (vida e recurso), o
  placar com as ordens, as quatro habilidades e uma faixa curta de avisos.

## 4. Controle direto e o compromisso dos golpes

- **Andar:** WASD com aceleração de 1000 px/s² e freio de 1400 px/s²: a velocidade máxima (72 px/s no Guerreiro) em
  5 passos (83 ms) e a parada em 4 (67 ms). O herói olha para o mouse; durante um golpe, para a direção do golpe.
- **Mirar:** cada golpe sai na direção do mouse (arco, faixa) ou no ponto do mouse limitado ao alcance (círculo,
  parede). Nada de procurar alvo nem de clicar em soldado.
- **O compromisso, igual para todos:** golpe forte **prende os pés na preparação** (0,12 a 0,2 s) e não se cancela;
  **depois do contato**, andar ou outra habilidade cortam a recuperação. O básico deixa andar mais devagar (60% no
  Guerreiro, 75% no Mago) e é cortado por qualquer habilidade a qualquer momento.
- **Comando guardado:** uma habilidade apertada durante outra ação espera até 0,2 s e sai quando puder.
- **Pausa** (`P`/`Esc`): o campo para; as ordens funcionam pausado; as opções ficam ali. O jogo não depende dela.

## 5. Os dois kits

Os números estão em `tela/conteudo.js` (e a tela os lê de lá).

| Herói | Botão esquerdo | Botão direito | Espaço | Q |
|---|---|---|---|---|
| **Guerreiro** (vida 260, Fúria 0 a 100) | **Corte**: arco de 110°, 22 px, dano 3; o 3º corte seguido (até 0,9 s) é o **arremate**: 130°, 26 px, dano 8, arremessa | **Varredura**: prepara 0,2 s, arco de 220°, 32 px, dano 13 (derruba soldado), empurra e atordoa; recarga 6 s | **Investida**: 100 px em 0,2 s sem receber dano, joga para os lados quem está no caminho (dano 4), o campeão a segura; recarga 6 s | **Salto Esmagador**: até 130 px, 0,42 s no ar sem receber dano, círculo de 44 px, dano 24, arremessa e atordoa; custa 100 de Fúria (+1 por acerto, +1,5 por derrubado) |
| **Mago** (vida 170, mana 100, +7/s) | **Faísca**: projétil rápido até 175 px, dano 4 no primeiro que encontra | **Bola de Fogo**: prepara 0,18 s, explode no ponto do mouse (até 180 px), círculo de 24 px, dano 13, arremessa; o chão queima 2 s (5/s); 30 de mana, recarga 1,5 s | **Piscar**: reaparece até 95 px; onde estava, uma onda de 28 px empurra e atordoa (dano 3); recarga 6 s | **Muralha de Fogo**: parede de 96 px no ponto do mouse, de lado para o herói, 5 s; desvia os inimigos e queima 14/s; 40 de mana, recarga 9 s |

Por que assim: o Guerreiro tem o ritmo **entrar, varrer, sair** (a Investida para abrir ou fugir, a Varredura como a
grande decisão a cada 6 s, a Fúria guardando a virada); o Mago, **mirar no grupo, manter distância, mudar o terreno**
(a mana limita a Bola a umas três seguidas e depois uma a cada ~4 s; a Muralha divide o exército; o Piscar resolve
quem chegou perto). Os golpes fortes derrubam soldados comuns de uma vez; o veterano (32 de vida) aguenta um golpe forte
e mostra a barra por 1,5 s; o campeão (220) leva, recua pouco e mostra o atordoamento.

## 6. O impacto

| Parte | Como ficou |
|---|---|
| Antecipação e direção | A pose de preparo do herói e a **área no chão** (o arco, o círculo, a faixa) durante a preparação; no voo do Salto, o círculo de chegada; no voo da Bola, o círculo do alvo enchendo |
| Contato | No quadro do contato, todos os de dentro da forma levam o golpe de uma vez; o corte desenha o arco varrendo (borda branca, preenchimento claro) por 90 a 160 ms |
| Reação do alvo | Clarão branco (60 a 90 ms) e o alvo **congela** 45 a 70 ms (a pausa local), depois recua na direção do golpe; golpe forte atordoa e interrompe a preparação (o campeão mostra "interrompido") |
| Arremesso e deslocamento | Quem **morre** num golpe forte vira efeito: voa na direção do impacto com uma parábola, gira de 90 em 90°, quica uma vez com poeira e fica no chão como marca. Quem **vive** é empurrado de verdade (a velocidade de empurrão entra na simulação e afeta a luta: abre espaço, tira do alcance) |
| Morte e queda | Morte fraca: cai no lugar e escorrega um pouco. Arremessado: voa 20 a 45 px. O corpo vira marca no chão, sem cor e escuro, para não se confundir com quem está de pé |
| Fogo, corte e poeira | Brasas que sobem e caem, fumaça fraca (opacidade ≤ 32%), anel de explosão que se abre, a marca queimada discreta; o clarão cheio da explosão dura ~60 ms |
| Pausa de impacto | Só nos golpes fortes: Varredura 45 ms (+8 por derrubado, até 90), Bola 50 (+6, até 85), Salto 100, arremate 25. **Teto de 100 ms e 150 ms de intervalo** entre uma pausa e outra: muitos golpes juntos não travam a tela. Pode ser desligada |
| Tremor | Trauma ao quadrado (seção 1), proporcional ao golpe e ao número de derrubados, com um empurrão curto na direção do golpe. Varredura ~0,26, Bola ~0,30, Salto 0,70, golpe do campeão no herói 0,35. Intensidade 0 a 150%; em 0 a câmera não se mexe, e a força continua legível pela área, pelo arremesso, pelo clarão e pelo "N derrubados" |
| Som | Sintetizado (ruído filtrado e osciladores), volume e mudo; cada som tem intervalo mínimo (doze acertos não viram doze estalos) |

## 7. Tropas, ordens, movimento e ocupação

- **Papéis:** soldado (perto), veterano (perto, resistente), arqueiro (longe: mantém ~105 px, recua se alguém chega a
  46 px, a flecha cai num ponto e pode errar), porta-estandarte (atrás da linha, aura de 70 px: +30% de dano e ataque
  15% mais rápido; derrubado, abala quem está a 120 px por 2 s), campeão (golpe de machado anunciado, interrompível).
- **Escolha do alvo:** a cada 0,3 a 0,6 s; custo = distância + 22 por atacante que já está no alvo; cada alvo tem
  **vagas** (3 num soldado, 7 no herói e no campeão). O excesso procura outro: o grupo envolve em vez de empilhar.
  Chegando perto, cada um abre um pouco para o seu lado. Alvo morto ou fora da ordem: escolhe de novo na hora.
- **Ordens** (teclas 1, 2, 3, também pausado): **Acompanhar** (luta só perto de si ou do herói; sem inimigo, um anel
  solto em volta dele, os arqueiros atrás), **Atacar** (o mais perto, em qualquer lugar), **Defender aqui** (no ponto do
  mouse; luta a até 85 px dali e larga quem passa de 120 px; a bandeira fica no chão).
- **Separação:** grade espacial de 12 px; cada par sobreposto se afasta pela massa. **Regra deliberada do herói:** os
  **aliados abrem caminho** (o herói não perde velocidade por eles); os **inimigos são corpo sólido**: o herói empurra
  pesando como 2,5 soldados e anda mais devagar a cada inimigo encostado (até 45% da velocidade). Atravessa uma linha
  fina apanhando, não a multidão inteira; para isso existe a Investida (e, no ar, o Salto).
- **Sem alvo:** aliados voltam para a ordem; inimigos marcham para o meio do exército aliado; na fuga, correm para a
  borda direita e saem.

## 8. A batalha

Sempre a mesma (semente fixa), para comparar os dois heróis. **Normal:** 42 aliados (30 soldados, 12 arqueiros) e o
herói contra 94 inimigos: a **primeira leva** (28 soldados, 14 veteranos, 12 arqueiros e o porta-estandarte) espera em
formação 2,5 s (ou até ser atacada); a **segunda** (20 soldados, 10 veteranos, 8 arqueiros e o **campeão**) entra pela
direita aos 30 s ou quando a primeira cai a 20%. Com 20% dos inimigos de pé (depois da segunda leva), o resto foge e
vem a **vitória**; o herói caído é a **derrota**. `R` recomeça na hora. **Maior:** o dobro de cada grupo (≈ 270 no
campo, dois campeões e dois porta-estandartes).

O fim mostra: derrubados pelo herói e pelas tropas, os que fugiram, as perdas, o maior golpe e cada habilidade (usos,
atingidos, derrubados).

## 9. Verificação: funcionamento

`node --test testes/sim.test.mjs` (14 testes; `testes/test_campo.py` os roda e confere que o jogo não carrega nada da
pasta):

| O que se pediu conferir | Como foi conferido |
|---|---|
| Área mostrada = alvos atingidos | Varredura, Salto, Bola e Piscar contra uma grade de veteranos parados: o conjunto atingido é exatamente o conjunto dentro da forma. Por construção, o desenho pinta cada pixel testando a mesma função `dentro` |
| Dano aplicado uma vez | Varredura, Salto, Bola e Investida: cada atingido perde exatamente o dano da ação (o fogo do chão começa 0,25 s depois, de propósito) |
| Mortes simultâneas | Um Salto derruba 15 ou mais no mesmo passo; a lista, o placar e as estatísticas batem; nenhum aliado continua mirando um morto |
| Unidades sem alvo | Sem inimigos, as tropas voltam ao ponto de defesa e depois acompanham o herói; nada trava nem vira NaN |
| Grupos concentrados | 80 soldados no mesmo ponto se espalham em 2 s, sem sobreposição maior que 1,5 px |
| Herói entre aliados e inimigos | Atravessa 40 aliados sem perder velocidade; contra um bloco de inimigos, anda menos de 70% e não fica preso |
| Resposta | Acelera em até 5 passos, para em até 4; o golpe começa no passo do aperto; o comando guardado sai depois do contato; um aperto que não pode sair em 0,2 s se perde |
| Compromisso | Andar na preparação não move; depois do contato, andar corta a recuperação |
| Ameaça | O campeão anuncia o golpe; a Varredura o interrompe; o Corte, não |
| Repetição | A mesma semente e a mesma entrada dão a mesma batalha |
| A batalha termina | Com o jogador automático "médio", os dois heróis vencem e as tropas derrubam inimigos; sem o herói, as tropas perdem |
| Pausa, retomada, reinício | No navegador (`ferramentas/medir.mjs pausa`): o tempo de jogo não anda pausado, a ordem funciona pausado, retoma, `R` volta ao começo, `Tab` abre o registro |

**Resposta medida no navegador** (`medir.mjs resposta`, teclado e mouse de verdade): ver a seção 11.

## 10. Verificação: sensação

**Os vídeos** (1280×720, o jogador automático forte, a batalha inteira ou quase, abrem no navegador):
`ferramentas/prototipos/etapa8-campo/videos/guerreiro-1280x720.webm` (30 s), `mago-1280x720.webm` (30 s) e
`guerreiro-maior-1280x720.webm` (22 s, a batalha maior). Mostram os encontros dos grupos, a Varredura, o Salto e a
Investida, a Bola de Fogo e a Muralha, a chegada da segunda leva e o fim. As sequências quadro a quadro
(`capturas/sequencia-varredura.png`, `-salto.png`, `-bola.png`) mostram 30 quadros seguidos a partir da preparação, com
o tempo de jogo e os quadros da pausa de impacto marcados.

O que eu observei nas sequências, nas capturas e nos vídeos:

- **A Varredura num grupo** lê bem: a área aparece branca no chão durante a preparação, o arco varre, a tela para ~90 ms
  e os corpos saem voando em leque na direção do golpe; "14 derrubados" aparece em cima.
- **A Bola de Fogo** lê bem: o círculo do alvo enche durante o voo (0,15 a 0,4 s), o clarão cobre a área por um
  instante, o anel abre e as brasas e a fumaça somem antes de esconder a luta.
- **O Salto** mostra o herói subindo (até 22 px) com a sombra no chão e o círculo de chegada.
- **Ajustes feitos depois de ver:** os corpos arremessados voavam 100 a 200 px e ficavam no chão com as cores vivas,
  espalhados pelo campo como se fossem soldados de pé (agora voam 20 a 45 px e ficam apagados e escuros); o Corte
  empurrava tanto que os soldados nunca acertavam o herói (o empurrão do básico caiu de 60 para 25); as marcas de fogo eram manchas pontilhadas grandes (ficaram discretas); as barras
  de vida dos veteranos poluíam o meio da luta (só por 1,5 s depois do golpe, menores); os arqueiros inimigos se
  espalhavam num anel em volta do Mago (ficam atrás da própria linha); a Bola demorava a chegar (mais rápida); a
  primeira leva esperava parada a explosão (atacada, avança); a ordem dada pausado só aparecia ao continuar; o painel
  da pausa cobria o exército (foi para o canto); o custo das habilidades do Mago saía cortado.
- **O que só o Jean responde:** se o peso do golpe está certo com e sem tremor; se a pausa de impacto ajuda ou atrapalha;
  se o herói se lê no meio da multidão; se as tropas parecem úteis; se dá vontade de repetir (seção 14).

## 11. Desempenho

**Condições:** Windows 10 do Jean (DESKTOP-4KMKFO5), Chromium 130 do Playwright **sem janela** (o canvas desenhado na
CPU), 31/10/2026; cada linha é uma batalha com o jogador automático forte, medida por 20 s a partir do começo (o
contato, as áreas e as mortes em massa estão dentro). 60 quadros por segundo é o teto do `requestAnimationFrame`.
Os números brutos estão em `capturas/medicao.json` (`node ferramentas/medir.mjs desempenho`).

| Janela | Tropas | Herói | Combatentes (máx.) | Partículas (máx.) | Qps | Quadro p95 / máx. | Simulação média / p95 | Desenho média / p95 |
|---|---|---|---|---|---|---|---|---|
| 1280×720 (2×) | normal | Guerreiro | 98 | 52 | 60 | 16,7 / 16,8 ms | 0,18 / 0,4 ms | 1,0 / 2,2 ms |
| 1280×720 (2×) | normal | Mago | 98 | 78 | 60 | 16,7 / 16,8 ms | 0,25 / 0,5 ms | 1,1 / 1,7 ms |
| 1280×720 (2×) | maior | Guerreiro | 195 | 134 | 60 | 16,7 / 16,8 ms | 0,43 / 0,9 ms | 2,0 / 3,4 ms |
| 1280×720 (2×) | maior | Mago | 195 | 90 | 60 | 16,8 / 16,8 ms | 0,25 / 0,5 ms | 1,5 / 2,3 ms |
| 1920×945 (3×) | normal | Guerreiro | 98 | 61 | 60 | 16,7 / 16,8 ms | 0,17 / 0,4 ms | 1,0 / 2,2 ms |
| 1920×945 (3×) | normal | Mago | 98 | 78 | 60 | 16,7 / 16,8 ms | 0,18 / 0,4 ms | 0,8 / 1,3 ms |
| 1920×945 (3×) | maior | Guerreiro | 195 | 124 | 60 | 16,7 / 16,8 ms | 0,31 / 0,7 ms | 1,5 / 3,0 ms |
| 1920×945 (3×) | maior | Mago | 195 | 90 | 60 | 16,7 / 16,8 ms | 0,21 / 0,4 ms | 1,2 / 1,7 ms |

(Os 98 e 195 são a primeira leva com os aliados; a segunda entra depois, até ≈ 137 e ≈ 270.) No Node, o passo da
batalha maior custa em média 0,1 a 0,25 ms (`ferramentas/simular.mjs`; um teste exige menos de 4 ms).

**Resposta** (`medir.mjs resposta`, teclado e mouse de verdade no Chromium): em tempo de jogo, andar começa no primeiro
passo depois da tecla (16,7 ms), chega à velocidade máxima em 83 ms e para em 67 ms; a Varredura começa no primeiro
passo depois do clique e o contato vem 217 ms depois (os 0,2 s de preparo); a Investida começa no primeiro passo. No
relógio, o primeiro quadro depois de uma **tecla** chega 85 a 95 ms depois, porque o Playwright trava a página uns
85 ms ao injetar a tecla (medido: não há quadro nesse intervalo); depois de um clique, 15 a 19 ms.

**Limite técnico × leitura:** o desempenho não é o limite: na batalha maior, simulação e desenho somam uns 4 ms dos
16,7 ms de um quadro, sem quadro perdido. O limite que apareceu é de **leitura**: na maior, a massa do meio vira uma
mancha azul e vermelha e as barras dos veteranos se acumulam (`capturas/maior-*.png`); e de **comportamento**: os
arqueiros inimigos que sobram se espalham pelo campo, e o grupo denso da primeira leva é o alvo óbvio.

## 12. Limitações conhecidas

- **Arte provisória** em grade de letras no código, sem fonte no Aseprite; poucas poses; o veterano e o campeão são
  manchas mais largas; o herói desenhado por cima de todos (decisão de leitura, seção 3).
- **Equilíbrio de teste:** com o jogador automático, a batalha normal acaba em 25 a 30 s e o herói derruba 55 a 75 dos
  94; as tropas derrubam 13 a 25 e perdem 0 a 12 dos 42; o Guerreiro sofre 37 a 57 de dano, o Mago 0 a 6 (ele
  mantém distância e pisca). Sem o herói, as tropas perdem em ~40 s derrubando ~9. Ou seja: o herói é forte demais
  contra um jogador automático preciso, e as tropas pesam pouco. Uma pessoa jogando pela primeira vez deve demorar
  mais e apanhar mais, mas isso não foi medido. Os números estão todos em `conteudo.js`.
- **A primeira leva em formação** ainda é o grupo mais denso da luta: uma Bola ou uma Varredura bem posta ali derruba
  10 a 15 de uma vez (é a "boa oportunidade" mais óbvia; atacada, a leva avança).
- **Sem obstáculos no campo** (nem rios, nem pedras grandes): o movimento não precisa de busca de caminho; um campo com
  obstáculos pediria campo de fluxo ou caminhos.
- **Inimigos sem inteligência de grupo:** não flanqueiam, não recuam juntos, não protegem o porta-estandarte; o campeão
  só prioriza o herói.
- **Fogo amigo desligado:** as áreas do herói não pegam aliados (o tático pegava). Se for preciso, é uma regra a mais.
- **Os vídeos e o desempenho usam o jogador automático** (`robo.js`), que preenche a mesma entrada do teclado e do
  mouse; não é uma pessoa jogando.
- **Sons sintetizados** simples; nenhum arquivo de áudio.

## 13. O que esta direção mudaria no jogo (não implementado)

Se o campo livre seguir, quase tudo do combate muda; o resto do jogo (vila, mapa, eventos, cenas, inventário) pode
ficar, com pontos de contato:

- **A luta vira uma tela própria** (como uma batalha separada em Mount & Blade): a exploração continua por texto e
  cenas; um encontro abre o campo. O motor Python passaria a mandar o encontro (quem, quantos, o terreno) e receber o
  resultado (vida, mortes, espólio); a luta em si roda no navegador. O **gabarito** (24 partidas com semente) precisaria
  de uma forma de jogar a luta sem tela (o `sim.js` já roda no Node; seria portá-lo ou chamá-lo).
- **Habilidades e talentos:** o catálogo de 45 habilidades e os talentos foram pensados para turnos (porcentagem do
  Poder, turnos de duração, cadeias). Em tempo real, cada um vira forma, alcance, preparação, recarga e custo; os
  estados viram segundos; muitos talentos de número continuam, os de ordem de turno somem. O X1 e o tático ajudam a
  escolher quais caminhos (Berserker, Piromante) vale converter primeiro.
- **Comitiva:** Odette, Morel e Yara viram unidades especiais no campo (com IA e talvez uma ordem própria), ou heróis
  controláveis em troca. Decisão do Jean.
- **Inimigos do Vale:** as 17 famílias viram tipos de tropa e ameaças com padrões no chão (o campeão é o modelo:
  anunciar, punir, ser interrompido); os chefes viram encontros com fases.
- **Equipamento e atributos:** continuam, convertidos em vida, dano, velocidade, recarga, alcance; a ficha precisa
  dizer isso em números do motor.
- **Arte:** um conjunto de sprites por tipo (seis poses é pouco para o jogo final), efeitos por elemento, os cenários
  de batalha por região; o pipeline do Aseprite das cenas se aplica.
- **Dificuldade, acessibilidade e ritmo:** a pausa com ordens, a velocidade do jogo, o tremor e a pausa de impacto como
  opções do jogo; o equilíbrio medido com jogadores automáticos de níveis diferentes.

## 14. O que avaliar jogando

Abra `ferramentas/prototipos/etapa8-campo/demo.bat` (o topo diz "Campo Livre 1").

1. **O critério:** andar e acertar uma Varredura ou uma Bola num grupo foi fluido, legível e satisfatório? Deu vontade
   de repetir?
2. **Peso:** o golpe forte parece forte? Teste com o tremor em 100%, em 50% e desligado, e com a pausa no impacto
   ligada e desligada.
3. **Controle:** algum momento pareceu atrasado ou travado? A preparação da Varredura (0,2 s presos) incomoda ou dá
   peso?
4. **Leitura:** você acha o herói na multidão? As áreas no chão e o anúncio do campeão se leem sem pensar?
5. **Tropas:** elas parecem úteis? As ordens (1, 2, 3) mudaram alguma coisa que você quis? Faltou alguma?
6. **Guerreiro contra Mago:** qual sensação está mais perto do jogo que você quer?
7. **Escala:** a batalha normal é o tamanho certo? A maior (opção "Tropas") lê ou vira ruído?
