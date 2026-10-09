# Roadmap

Onde estamos e para onde vamos. Atualize a cada etapa concluída.

## A meta

Um RPG de texto com a liberdade de Baldur's Gate: árvores de talentos enormes, centenas de habilidades,
especializações e especializações de elite, história com ramificações e personagens fixos, cidades e masmorras,
e cada partida diferente da anterior. Para chegar lá, primeiro um núcleo que aguenta escala.

## Refatoração do núcleo (antes de expandir)

Cada etapa mantém o gabarito de regressão idêntico: nada de jogo muda, só onde as coisas moram.

| Etapa | O quê | Situação |
|---|---|---|
| **A** | Habilidades como dados: blocos que executam e se descrevem; Grimório gerado; conta de crítico única | ✅ feito |
| **B** | Modificadores e gatilhos: talentos e passivas de especialização declaram "+x% de dano corpo a corpo", "ao matar", "no início da luta"... e o combate só pergunta `mod`/`disparar`. Zero `tal("...")` fora de `talentos.py` (eram 28 talentos em 5 arquivos). Chaves validadas por teste. Falta: itens e estados como fontes (hoje `especial()`), e as verificações de spec fora do combate (testes de atributo, eventos). | ✅ feito |
| **C** | Catálogo de estados (`rpg/estados.py`): nome, ícone e cor, mal ou bênção, dano por turno, perda de turno, imunidade, resistência, camadas e descrição. `aplicar` e `processar_efeitos` genéricos; a tela recebe ícones e dicas do motor; o Grimório descreve pelo catálogo. Falta: o efeito dos estados na conta de dano (fortalecido, guarda, marcado...) ainda é perguntado à mão em `atacar`; vira modificador junto com os itens. | ✅ feito |
| **D** (próxima) | Mundo e narrativa como dados: flags com nome, facções, reputação por facção, missões com etapas; eventos e diálogos com condições e consequências declaradas; validador de conteúdo (referências existem, ramos alcançáveis). | quando a história começar |
| **E** | Front-end: `telas.js` dividido por tela; animação de habilidade como campo de dados (hoje há casos fixos em `batalha.js`). | |

## Equilíbrio (1.13)

Réguas para mexer na dificuldade com números: o simulador por especialização e nível (`tests.equilibrio`), o
replay das partidas de verdade (`tests.replay`, com a do Xatuba em `tests/runs/`) e o `--dev N`. Primeiro ajuste:
base um pouco mais dura e a curva bem mais dura do meio para o fim (defesa que perde força contra inimigos de nível
alto, ataque e vida dos inimigos com curva, equipamento crescendo menos, XP mais lento e menor de inimigos fracos).
Em 1.14, o padrão virou hardcore com metas declaradas (em COMO_CRIAR): grupos maiores cedo, companheiro que custa
caro (mais inimigos e mais vida neles), inimigos mais duros desde a base, curva do meio mais forte e a do fim mais
plana (menos pico, mais desgaste); Paladino menos invulnerável, Barreira do mago crescendo com o Poder, servo do
Necromante que provoca. O simulador mede também "lutas até descansar".
Em 1.15: dano geral do herói ×0,9 e dos inimigos ×1,1; a iniciativa dá +25% no primeiro golpe (era crítico
garantido); a taverna devolve 35% da vida (era 65%), deixando o templo como a cura de verdade.
Pendente: passe por especialização (Paladino ainda fácil; Sombra, Piromante e Necromante duras no fim); um modo
mais brando para quem quiser; um robô de mapa que jogue partidas inteiras com juízo, para medir o ritmo de nível.

## Depois do núcleo

- Sistemas gerais (não de uma classe): reputação por facção, missões encadeadas, diálogo com testes de atributo
  como opções, consequências que voltam dias depois.
- Conteúdo: história fixa, personagens, mapa, cidades, masmorras com mapa interno.
- Classes: árvores grandes, novas especializações, elites.

## Ideias guardadas (não agora)

- Domar o grifo como quarto animal do Patrulheiro (com Ordem própria).
- Comida para o animal (descartado por ora: provisões ficariam apertadas demais).
- Ícones próprios para cada habilidade.
- "Ordens" leves para a comitiva.
- Armazém para guardar mais coisa, quando a gama de itens crescer (junto com o saque de ARPG: mais drop, mais
  variedade). Como Titan Quest (a Caravana) e Diablo/Path of Exile/Grim Dawn: só nas vilas, nunca no acampamento
  (a mochila de 12 é a tensão da viagem), e o mesmo conteúdo em todas as vilas (uma carroça de caravaneiro leva
  suas coisas de uma para outra). Outro nome que não "baú", para não confundir com o Baú Trancado (o saque que se
  abre na vila ou na fogueira, que fica). Junto dele, "Vender o lixo" no mercado (o jogo marca o que é comum e
  pior que o equipado, você desmarca o que quiser), com um plin por item.
