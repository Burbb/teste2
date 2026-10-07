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
| **C** (próxima) | Catálogo de estados: cada estado declara nome, ícone, efeito por turno, se acumula, como se descreve. Tira a sequência de `if` de `processar_efeitos`. | |
| **D** | Mundo e narrativa como dados: flags com nome, facções, reputação por facção, missões com etapas; eventos e diálogos com condições e consequências declaradas; validador de conteúdo (referências existem, ramos alcançáveis). | quando a história começar |
| **E** | Front-end: `telas.js` dividido por tela; animação de habilidade como campo de dados (hoje há casos fixos em `batalha.js`). | |

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
