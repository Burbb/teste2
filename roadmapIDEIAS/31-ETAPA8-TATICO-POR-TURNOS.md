# 31 — Etapa 8: o combate tático por turnos (Dofus como referência principal)

**01/11/2026.** Pedido do Jean: estudar o combate de Dofus (e, como complemento, Baldur's Gate 3) e construir uma
batalha tática por turnos jogável: casas em losango, turnos claros, movimento e habilidades com custo explícito, áreas e
linha de visão, posicionamento que importa e montagem de habilidades antes da luta. Escala: o herói (Guerreiro, Mago ou
Arqueiro), Morel e Odette, os três controlados pelo jogador na vez de cada um, contra cinco inimigos. **Protótipo
isolado, em avaliação, junto com o campo livre (o [30](30-ETAPA8-CAMPO-LIVRE.md)); o combate do jogo não mudou.**

Ligações: o [29](29-ETAPA8-COMBATE-TATICO.md) (o primeiro estudo de grade e o Tático 1, preservado), o
[28](28-ETAPA8-HABILIDADES-TALENTOS-E-BUILDS.md) (builds e talentos), a [continuidade](00-COMECE-AQUI.md).
Protótipo: [`ferramentas/prototipos/etapa8-tatico2/`](../ferramentas/prototipos/etapa8-tatico2/LEIA-ME.md) (`demo.bat`,
versão **Tático 2**).

| Seção | O que tem |
|---|---|
| 1 | A pesquisa: o que foi consultado e o que cada fonte deu |
| 2 | As regras: o que entrou, o que foi adaptado e o que ficou de fora |
| 3 | A representação: losangos e sprites pequenos |
| 4 | Classes, kits, talentos e companheiros |
| 5 | Encontros e a IA |
| 6 | Verificação |
| 7 | Decisões provisórias, limitações e o que avaliar |

---

## 1. A pesquisa

**O que foi consultado** (páginas abertas e lidas nesta rodada; o 29 já tinha o devblog do tacle, a nota de empurrão e
as referências de Wakfu, Into the Breach e Divinity):

| Fonte | Versão | O que deu |
|---|---|---|
| JeuxOnLine, ["Les bases du combat"](https://dofus.jeuxonline.info/article/1720/bases-combat) | Dofus 2.x (2014, revisto em 2016) | 6 PA e 3 PM no começo; feitiço custa PA, andar custa PM (uma casa por PM); com 0 de vida, em luta de grupo, o combatente sai e o time continua |
| JeuxOnLine, ["Devblog: Tacle déterministe"](https://dofus.jeuxonline.info/actualite/30452/devblog-tacle-deterministe) | Dofus 2.1 (2011) | sair do contato custa uma fração dos PA e PM, sem sorteio: com Fuga igual ao Tacle, perde-se a metade; para não perder nada, Fuga > 2 × Tacle + 2 |
| Breakflip, fichas de feitiços (Eniripsa, Crâ, Eliotrope) | Dofus 2.x/3 (sem data por ficha) | as propriedades de um feitiço: alcance mínimo e máximo, "alcance modificável", "lançar em linha", com ou sem linha de visão, limite por turno, limite por alvo, intervalo de relance (recarga) e o global; as zonas: cruz, círculo, linha, diagonal, cada uma com tamanho; empurrar e atrair são efeitos à parte da forma |
| Methodwakfu (guia de ordem) e um guia de Kolossium | Wakfu e Dofus | a ordem sai da iniciativa, por equipe, no começo, e fica fixa; quem morre sai da fila sem recalcular; os lados alternam |
| Millenium, nota de equilíbrio do empurrão | Dofus 2.x, não datada | o dano de empurrão deixou de ser aleatório e cresce com as casas que faltaram |
| JeuxOnLine, "Le bouclier de Féca" | Dofus 2.x | glifos: zonas no chão que afetam quem está nelas; um deles impede empurrar e atrair |
| Gamosaurus e Millenium, Dofus 3 (Unity) | lançado em dezembro de 2024 | a mudança de motor; não achei nota oficial de mudança das regras básicas de combate nessa passagem |
| bg3.wiki: [Actions](https://bg3.wiki/wiki/Actions) | Baldur's Gate 3 (1.0+) | três recursos por vez: Ação, Ação bônus e Reação (a reação na vez dos outros); Empurrar é ação bônus |
| bg3.wiki: [Concentration](https://bg3.wiki/wiki/Concentration) | idem | uma concentração por vez; o dano força um teste (CD 10 ou metade do dano, o maior); cair, ficar Caído ou incapacitado a quebra |
| bg3.wiki: [Surfaces](https://bg3.wiki/wiki/Surfaces) | idem | superfícies com efeito ao pisar e por turno (fogo, água eletrificada, gelo, graxa); interações (água + raio, fogo + óleo, gelo derretendo); quem já está na casa não é afetado pela superfície nova até se mover |
| bg3.wiki, High Ground e guias | idem | o terreno elevado dá bônus a ataques à distância; as fontes divergem (+2 ou vantagem) |

**Limites:** não consultei documentação oficial da Ankama (as fichas são de sites de fãs e guias); as regras de Dofus
variam por versão e a regra exata de visão em cantos e a fórmula atual do empurrão não foram confirmadas. A ordem
alternada vem de guias, não de texto oficial. Nada foi copiado: nenhum nome, número, texto ou imagem dos jogos.

## 2. As regras

| Regra | Em Dofus / BG3 | No Tático 2 | Por quê |
|---|---|---|---|
| PA e PM | 6 PA, 3 PM; gastos em qualquer ordem | **6 PA; 3 PM (4 no Arqueiro)**; andar, agir, andar de novo | É o centro do modelo e dá a decisão "andar antes ou depois" |
| Custo das habilidades | 2 a 6 PA | **1 a 4 PA**: 2 a 3 ações por vez | Várias ações por vez, sem virar uma fila de cliques |
| Alcance | mínimo, máximo, modificável, em linha, com ou sem visão | **igual**; "modificável" vira Ofuscado (−2) e Olho de Águia (+2) | Dá papéis (perto, longe, alinhado) |
| Linha de visão | obstáculos e combatentes bloqueiam | **pilares, barris e combatentes bloqueiam; água e rocha baixa deixam ver**; canto permissivo | Onde parar e quem fica na frente importam |
| Limites | por turno, por alvo, recarga, global | **por turno, por alvo, recarga em turnos seus** (sem o global) | Fazem sentido com várias ações por vez |
| Áreas | cruz, círculo, linha, diagonal… | **alvo, cruz, círculo (o losango), raio (em linha a partir de quem lança, para no pilar) e atravessada** | O suficiente para juntar e separar |
| Bloqueio e fuga | Tacle e Fuga como atributos; perde fração de PA e PM | **+1 PM por inimigo vizinho ao sair da casa; 2 se ele é pesado** (Morel, Brutamontes) ou tem Muralha Viva; o lobo e Pés Leves ignoram | Determinístico como o tacle atual, sem atributo novo; a fração de PA tiraria ações inteiras |
| Deslocamento forçado | empurrão com dano por casas que faltaram; atrair | **empurrar: 4 por casa que faltou, metade a quem foi atingido; puxar: sem dano**; não sofre bloqueio | Sem sorteio (a prévia é exata) |
| Ordem | iniciativa por equipe, fixa, alternando | **igual**; quem cai sai da fila | Clara e previsível |
| Zonas no chão | glifos e armadilhas | **armadilha invisível ao inimigo** (Arqueiro) e **chão em chamas ou envenenado** | Controle de espaço |
| Superfícies (BG3) | efeito ao pisar e por turno; interações | **fogo e veneno: dano ao entrar ou ao começar a vez na casa**; o chão novo não fere quem já está nela | A parte de BG3 que mais muda o espaço |
| Interação ambiental (BG3) | óleo explode com fogo | **barril de óleo**: dano de fogo direto numa área o explode (8 na cruz, chão em chamas, encadeia) | Uma interação clara por arena |
| Golpe preparado | (do 29, Into the Breach) | **o Brutamontes marca 3 casas e bate no começo da vez seguinte**; quem sai escapa | Ameaça legível que pede posicionamento |
| Dano | faixa e crítico | **fixo** | A prévia mostra o número exato |
| Ação bônus, reação | BG3 | **fora** | O PA já dá a economia; reação exige interromper a vez dos outros (mais cliques e leitura para três personagens) |
| Concentração | BG3 | **fora**; os efeitos sustentados têm duração fixa (Escudo Erguido, Cobrir) | Mais um recurso a acompanhar em três personagens |
| Terreno elevado | BG3 | **fora** (registrado) | Pede arte com alturas e regra de visão em 3D |
| Fase de posicionamento, invocações, roubo de PA e PM | Dofus | **fora** | Escopo; o roubo de PM aparece só como Lento, Desequilibrado e Congelado |
| Revezamento, doação de ações, troca na ordem | — | **fora** (rejeitados antes) | Pedido do Jean |

**Duração dos estados:** "por N turnos dele" conta no fim da vez de quem carrega (Lento, Marcado, Imobilizado...); as
proteções contam no começo da vez seguinte de quem carrega ("até o começo da sua próxima vez"); o Cobrir de Morel conta
na vez de Morel. O chão dura em rodadas (a rodada em que foi criado conta).

## 3. A representação

**Comparação:** o Tático 1 é visto de cima (quadrados), o mais barato e o mais legível para regra; o campo livre usa a
mesma vista com sprites em três quartos. Dofus usa losangos com sprites em três quartos, o que dá profundidade e
"tabuleiro" sem 3D. **Escolha:** losangos de 32 × 16 px com os sprites do campo livre (13 a 19 px de largura, 12 a 15
de altura), ampliados por um fator inteiro (3 em 1920 × 1080, 2 em 1280 × 720). A regra continua na grade quadrada (a
vista é só a projeção); a casa sob o mouse é calculada no chão, e o contorno dela é desenhado por último, por cima de
tudo, então nenhuma casa fica ambígua atrás de um corpo.

- **Altura e sobreposição:** pilares de 30 px com topo e duas faces; desenho por profundidade (x + y). Pilares e barris
  ficam translúcidos quando há alguém (ou a casa sob o mouse) logo atrás.
- **Grade:** discreta em repouso; mais forte ao andar ou mirar. Alcance em azul, sem visão hachurado, área em vermelho
  (amarelo onde há aliado), caminho em amarelo com o custo em PM, golpe preparado em listras vermelhas.
- **Combatentes:** o sprite inteiro, com a sombra e um losango fino da cor do lado no chão; a vida em barra curta
  acima. Na ordem dos turnos, o próprio sprite (sem retrato em círculo).
- **Arte nova:** Arqueiro, Morel, Odette, lobo, xamã e bruxa, desenhados à mão na mesma grade de texto do campo livre
  (uma letra por pixel; mãos em pontinhos de pele), com as cores da paleta dos sprites do jogo. **Provisória:** a fonte
  editável é a grade em `tela/sprites.js`, não um arquivo do Aseprite; o fluxo completo das skills de arte fica para
  quando a direção for escolhida.

## 4. Classes, kits, talentos e companheiros

**Tamanho do kit: 6 de 10.** Em Dofus o personagem tem quase todos os feitiços sempre, mas o PA limita a 2 ou 3 por
vez; aqui, com 6 PA e custos de 1 a 4, cada vez usa 2 a 3 habilidades. Seis espaços deixam a escolha antes da luta
pesar (4 de 10 ficam de fora), cabem na barra com as teclas 1 a 6 e mantêm a leitura de três personagens. **Talentos:
2 de 5 por classe**, cada um mudando o uso de uma habilidade ou do espaço.

| Classe | Vida · PA · PM | Habilidades (10) | Montagens prontas |
|---|---|---|---|
| Guerreiro | 64 · 6 · 3 | Golpe de Espada, Investida, Escudo Erguido, Golpe de Escudo (empurra 3), Corrente (puxa 4), Redemoinho, Provocar, Fenda no Chão (raio 3), Grito de Guerra, Golpe no Joelho | **Muralha** (Escudo, Provocar, Golpe de Escudo, Golpe no Joelho, Grito; Muralha Viva + Guardião): segura e protege. **Arremesso** (Investida, Golpe de Escudo, Corrente, Redemoinho, Fenda; Impacto + Embalo): move e esmaga contra os outros |
| Mago | 44 · 6 · 3 | Faísca, Bola de Fogo (deixa chamas), Lança de Gelo (raio 5), Corrente de Raios, Muralha de Fogo, Piscar, Repulsão, Toque Gélido, Combustão (consome chamas), Barreira Arcana | **Piromante** (Bola, Muralha, Combustão, Piscar, Barreira; Chamas Seletivas + Labareda): prepara o chão e o detona. **Criomante** (Lança, Toque Gélido, Raios, Repulsão, Piscar; Estilhaçar + Condutor): congela e consome o gelo |
| Arqueiro | 48 · 6 · 4 | Flecha, Tiro Perfurante, Chuva de Flechas, Flecha Repulsiva, Salto para Trás, Marca do Caçador, Armadilha, Tiro em Parábola (sem visão), Olho de Águia, Flecha nas Pernas | **Atirador** (Perfurante, Chuva, Olho, Salto, Parábola; Olho Treinado + Emboscada): dano de longe. **Caçador** (Marca, Armadilha, Flecha nas Pernas, Repulsiva, Salto; Perseguidor + Armadilheiro): prende, marca e controla o caminho |

**Morel** (Vida 72, pesado: bloqueio 2): Lâmina Curta, Avanço de Ombro (avança e empurra 1), Cobrir (metade do dano de
um aliado vai para ele até a próxima vez de Morel), Grito dos Cães de Ferro (provoca a até 2 casas), Golpe Baixo.
**Odette** (Vida 46): Luz Ardente, Prece de Cura (12, uma por alvo), Bênção (absorve 8), Clarão (cruz, só inimigos,
Ofusca), Purificar (tira os estados ruins). Kits fixos, próprios: Morel protege e segura; Odette sustenta e responde
(nenhum é o herói enfraquecido). As regras do campo livre (o principal a cada segundo, o recurso que regenera rápido, a
destruição em massa) não vieram para cá.

**Inimigos:** Bandido (perto, Faca e Rasteira), Lobo (rápido, 5 PM, sem bloqueio; +3 com a matilha), Brutamontes
(pesado, Soco e Golpe Esmagador preparado), Atirador (longe; Flecha e Flecha nas Pernas), Xamã (apoio: Seiva, Pele de
Casca, Espinhos), Bruxa (área: Nuvem Venenosa, Maldição, Dardo).

## 5. Encontros e a IA

| Encontro | Arena | Os cinco |
|---|---|---|
| Campo aberto | poucas rochas e dois pilares | três lobos, um bandido, um atirador |
| A passagem | dois muros com três aberturas, barris, água | brutamontes, dois bandidos, bruxa, atirador |
| Perto, longe e apoio | pilares, água, rochas e barris | brutamontes e bandido na frente, dois atiradores, xamã |

**A IA** (`ia.js`, a mesma para os inimigos e para o jogador automático dos testes): a cada decisão, compara todas as
opções "andar até uma casa alcançável e lançar uma habilidade num alvo válido dali", avaliando cada uma pela **prévia
de verdade** (a mesma conta da ação): dano pesado pela vida que falta e pela fragilidade do alvo, abates, estados úteis,
cura só até a vida que falta, proteção só em quem está ameaçado, aliados feridos pesando contra; mais o valor da casa
para o papel (o corpo a corpo perto do alvo; quem atira a 4 ou 5 casas, longe do alcance do corpo a corpo e com visão;
o apoio perto dos seus; todos evitam chão em chamas e as casas do golpe preparado). Repete enquanto houver PA e uma
opção que valha; no fim, usa os PM que sobraram para se posicionar. **Sem turnos perdidos por caminho:** o corpo a
corpo segue a distância a pé de verdade até o alvo, contornando muros e passando "através" dos próprios aliados com
custo (eles saem do caminho). **Alvo coerente:** mantém o foco no último que feriu, salvo um abate melhor; Provocado,
só ataca quem provocou. **Não vê as armadilhas** do Arqueiro.

**Medição** (`ferramentas/simular.mjs`: as 18 combinações de encontro e montagem, o jogador automático nos aliados):
| Encontro | Resultado | Rodadas | Observação |
|---|---|---|---|
| Campo aberto | 6 de 6 vitórias | 3 a 6 | o mais fácil: os lobos chegam em pedaços |
| A passagem | 5 vitórias, 1 derrota (Guerreiro Arremesso) | 6 a 9 | o brutamontes na abertura e a bruxa cobram tempo |
| Perto, longe e apoio | 3 vitórias, 3 derrotas (Guerreiro Muralha e Arremesso, Arqueiro Caçador) | 5 a 14 | a xamã cura e os atiradores castigam quem avança |

IA: 18 a 73 ms por vez em média, pior vez 346 ms (Node). Vezes inimigas sem ação nem movimento: 0 a 2 por luta (a causa de cada uma não foi investigada).

## 6. Verificação

- **18 testes das regras e da IA** (`node --test testes/regras.test.mjs`): a ordem alternada com Morel e Odette;
  custos, recargas, vezes por turno e por alvo; caminhos sem atravessar ninguém, o bloqueio (1, 2 com pesado ou Muralha
  Viva, 0 no lobo); o chão em chamas ao andar; a linha de visão (pilar e combatente bloqueiam, água e rocha não, o canto
  permissivo); as áreas; empurrão com colisão e a metade em quem foi atingido; puxar e avançar sem bloqueio; a duração
  dos estados; Cobrir e Bênção; talentos (validação e efeito: Labareda, Chamas Seletivas, Estilhaçar, Embalo);
  barril; armadilha; golpe preparado (quem sai escapa, e o bloqueio do pesado limita a fuga); **a prévia igual ao
  efeito em todas as habilidades das seis montagens**; a IA (sai do contato para atirar, não cura quem está cheio, cura
  o ferido, contorna o muro, obedece à provocação); os três encontros terminam.
- **No navegador** (`ferramentas/conferir.mjs`, Playwright, 1920 × 1080 e 1280 × 720): a preparação monta (3
  encontros, 3 classes, 10 habilidades, 5 talentos, os kits dos companheiros); Mago Criomante no encontro misto pela
  tela; a barra com o kit; o caminho mostra o custo em PM e andar gasta exatamente isso; a mira mostra alcance e prévia,
  e a vida depois de lançar é a da prévia; a vez passa por Odette e Morel; os cinco inimigos agem na primeira rodada;
  nada da HUD fora da janela; sem erros no console. Capturas: `capturas/t2-*.png`.
- **O jogo não mudou** (nada em `rpg/` nem em `tests/`).

## 7. Decisões provisórias, limitações e o que avaliar

**Provisório:** todos os números; o bloqueio simplificado; o dano fixo; os seis espaços e os dois talentos; as arenas
de 14 × 14; os kits fixos de Morel e Odette; a arte à mão na grade.

**Limitações:** a IA não planeja duas ações combinadas com outro inimigo (cada um decide sozinho); avalia a posição de
depois de agir, mas não prevê a resposta do jogador; o lobo e o bandido às vezes se amontoam na mesma abertura; o
campo aberto está fácil e o misto difícil para o Guerreiro (pelo jogador automático); sem fase de posicionamento; sem
desfazer; a animação é simples (deslizar e piscar).

**Para o Jean avaliar:** (1) a economia PA/PM e o bloqueio criam decisões ou trabalho? (2) os losangos e os sprites
pequenos leem bem? (3) controlar os três na vez de cada um é bom ou cansa? (4) as duas montagens de cada classe jogam
diferente? (5) a prévia (número, cai, estados, fantasma do empurrão) deixa claro o que vai acontecer? (6) os inimigos
parecem jogar (posição, foco, preparação)?
