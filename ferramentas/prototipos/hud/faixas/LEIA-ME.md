# As faixas de passagem (etapa 2, 24/10/2026; protótipo, nada no jogo)

**Agora: a original refinada (R), candidata em avaliação.** O Jean preferiu a faixa de hoje às propostas A e B, que
ficam como histórico (não aprovadas para integração). A R parte da ORIGINAL, numa cópia no protótipo; as faixas do
jogo não mudaram. A comparação: `folha-original-refinada.png`. A demonstração: `demo.bat` (a linha "R").

## R · a original refinada

**O que fica da original:** a tarja horizontal larga, de lado a lado, a 38% da altura (atravessando as colunas: é um
anúncio sobre a interface); o título na letra de título a 80 px, centralizado, com a sombra dura; a abertura na
vertical; os símbolos dos dois lados; as cores de cada situação (o ouro, o vermelho apagado da queda, o cinza das
sombrias); os tempos (1,6 s; 2,4 s as sombrias; 2,6 s a queda), os sons, os gatilhos, as regras e as partículas da
Vitória.

**O que muda (só o desenho):**

1. **O subtítulo:** de 15–17 px para 20–21 px, com 12 px de espaço sob o título, a sombra dura para ler sobre
   qualquer fundo, e quebra de linha até ~46 em (a saída da capela vai a duas linhas). O título nunca diminui por
   causa dele (fica 80 px em todos, a 1920 e a 1280).
2. **Os símbolos:** a espada aprovada (a família do equipamento, 48 px) no lugar do sprite antigo, a da direita
   espelhada; o "Sair" da doca no lugar do vulto correndo, na saída da capela; o Mestre caçador e a comitiva com as
   cabeças de sempre (já aprovadas, no tamanho delas: 48, sem ampliar), a da direita espelhada. Sem um aprovado que
   corresponda, ficam os de hoje: a caveira (a queda) e a lua (o cansaço).
3. **A tarja:** desenhada em pixel (texels de 3 px): a mesma transparência do miolo (0,94), mas as pontas em seis
   degraus de borda dura em vez do degradê liso (escurece por igual o que está embaixo, sem pontilhado picotando o
   texto das colunas), e um fio de cima quase da cor da tarja, só no miolo. Nada de contorno dourado, recorte
   serrilhado, joia, placa ou raio.
4. **A hierarquia, na mesma família:** a Vitória como hoje; o marco (Guardião, Mestre caçador, quem chega) com um
   acento breve: dois brilhos que correm do centro pelo fio de cima na entrada (~0,5 s) e somem; o peso (Você caiu,
   Exausto) entra descendo devagar em vez de abrir, com as pontas mais longas; a queda, um pouco mais alta; o cansaço
   numa tarja cinza-azulada; a passagem (Saindo da capela) sem acento.
5. **A sobreposição corrigida:** quando uma faixa chega com outra ainda na tela, a anterior sai em 100 ms enquanto a
   nova abre (ela leva ~240 ms para aparecer): nenhuma pausa a mais. Hoje, o "Guardião derrotado!" e o "Mestre
   caçador" ficam inteiros um sobre o outro por ~0,1 s (a animação de 1,6 s passa da espera de 1,5 s).

**Conferido** (no jogo de verdade, `auxiliares/`):
- `fotografar.mjs` (VERSOES=atual,r): Vitória, Guardião, Mestre caçador, Você caiu, Exausto, Saindo da capela e a
  comitiva com o nome longo, a 1920×945 e a 1280×720, com os mesmos dados; o título a 80 px numa linha em todos.
- `gestos.mjs` (a sequência real até o achado): a mesma ordem e os mesmos tempos da de hoje (o Mestre, o espólio, o
  nível e o achado, diferença de até 0,1 s); hoje, duas faixas inteiras juntas; na R, no máximo uma (a anterior sai em
  ~100 ms); cliques e a tecla 1 durante as faixas não escolhem nada (o achado continua esperando); a faixa não recebe
  cliques; com o movimento reduzido, a faixa inteira, parada, o tempo todo, sem animação.

**A avaliação:** a R é a mesma faixa, mais legível e mais limpa; a diferença de longe é pequena, de propósito. O
ganho maior é o subtítulo (o Mestre caçador e a saída da capela se leem no tamanho real) e a troca sem sobreposição. A
limitação: a caveira e a lua continuam os sprites antigos (não há aprovados que correspondam; um desenho próprio
seria outro trabalho); o acento do marco só se vê na entrada (a foto parada não o mostra: ver na demonstração).

**Continua à parte (não muda nesta rodada):** o adiantar não encurta as faixas (só a queda olha o `pular`); e as
duas `@keyframes faixa` do jogo com o mesmo nome (`03-batalha.css`, a das faixas da luta, e `06`, a desta): a de `06`
vence e vale também para as faixas da luta. Só registrado.

# A rodada anterior: A e B (histórico, não aprovadas)

## Os usos reais (o levantamento antes de desenhar)

Todas saem de `Telas.celebrar` (`telas/celebracoes.js`, a função `faixa`), mandadas pelo motor:

| faixa | gatilho (motor) | o que diz | segura a fila | adiantar | o que vem depois |
|---|---|---|---|---|---|
| Vitória | o fim de toda luta vencida (`combate/luta.py`) | "Vitória" | 1,0 s | não | o quadro do espólio |
| Guardião derrotado! | a luta vencida com um chefe | "Guardião derrotado!" | 1,5 s | não | (Mestre caçador, se for o 5º abate) → espólio |
| Mestre caçador | o 5º abate de uma família (`sistemas/confronto.py`) | "Mestre caçador" + "Lobos: +10% de dano contra eles" | 1,8 s | não | o espólio |
| Você caiu / Você morreu | a luta perdida (`luta.py`; morreu no hardcore) | o título | 2,2 s | **sim** (a única) | a página do resgate (ou da morte), sem Continuar |
| Exausto | a noite passou sem dormir (`sistemas/tempo.py`): na vila, o pouso ("Noite no feno do estábulo"); no mato, "Não dá para seguir: é preciso acampar." | título + frase | 2,3 s | não | a cena e a fogueira |
| Saindo da capela | "Sair e acampar" dentro da capela (`missoes.sair_para_acampar`); exausto ali, a mesma faixa com "Exausto" | título + o caminho (até 155 letras) | 2,6 s | não | o acampamento |
| X se junta a você | o recrutamento (`comitiva/grupo.py`) | "Irmã Odette se junta a você" + "clériga desertora" | 1,5 s | não | o menu |

- **A sequência real depois de uma luta com tudo junto** (conferida no jogo): Guardião derrotado → Mestre caçador → o
  quadro do espólio → a subida de nível → o achado (o equipamento vem por último, depois do nível).
- "Exausto" e "Saindo da capela" são faixas de passagem para a ponte (`FAIXAS_DE_PASSAGEM`): não pedem Continuar antes
  da página seguinte.

## As duas direções (A e B)

Comuns às duas: a faixa fica **dentro do palco** (a coluna do meio; nada passa pelas colunas laterais nem pela barra
da vida), apoiada na arte do topo; o título na letra de título no maior tamanho inteiro que cabe (64, 48 ou 32: o nome
longo da comitiva cai para 32 a 1280); o subtítulo a 18–19 px (hoje, 15–17 px); os ícones da família aprovada (a
espada, a cabeça da criatura, a cabeça do companheiro, o "Sair" da doca), um só, nunca dois iguais dos lados; sem
ícone na queda e no cansaço (a família não tem um que ajude). Quatro pesos, pela forma e pelo movimento, não só pela cor:

- **comum** (a Vitória): curta e baixa, um estalo de faíscas, a entrada e a saída rápidas (feita para repetir);
- **marco** (Guardião, Mestre caçador, quem chega): mais larga, o fio claro, raios atrás e faíscas subindo, o anel na
  entrada;
- **peso** (Você caiu, Exausto): sem ouro e sem brilho; a queda em sangue escuro, o cansaço em cinza; entra devagar,
  descendo; a cinza cai (brasa apagando na queda) sobre um escuro em volta;
- **passagem** (Saindo da capela): sem efeito, uma tira estreita e baixa, o título pequeno e o caminho escrito.

**A · a faixa integrada ao palco.** Uma faixa horizontal de base escura com as beiras rasgadas à mão (desníveis de 3
px, a grade dos pixels) e as pontas abertas em degraus, sem a moldura antiga; abre do meio para os lados.

**B · emblema e anúncio.** Uma placa chanfrada de ferro com o aro de latão; nos acontecimentos com símbolo, uma joia em
losango em cima, com o símbolo dentro; no marco, a joia bate (do grande para o lugar, em degraus) com os raios atrás.

**O que não mudou:** o jogo de hoje roda inteiro (`faixas.js` só troca o desenho: quando a faixa antiga nasce, ela sai
e a nova entra no lugar, com os mesmos dados); os tempos, os sons, a ordem, as regras e as recompensas. Os efeitos usam
as peças do `FX` das celebrações só para ler (raios, anel, partículas, o poço escuro); o Estouro e o Relicário não
foram tocados.

## Conferido (no jogo de verdade, `auxiliares/`)

- `fotografar.mjs`: os sete usos (e os dois exaustos a mais, na vila e na capela) nas três versões, a 1920×945 e a
  1280×720, com os mesmos dados: as duas propostas dentro do palco em todos (hoje: a faixa cruza a janela inteira), o
  título numa linha, o subtítulo a 18–19 px; medidas em `capturas/medidas.json`.
- `gestos.mjs`: a sequência real (o lobo guardião, o quinto lobo, o herói a 1 XP): a mesma ordem e os mesmos tempos
  nas três (o Mestre aos ~1,5 s e o espólio aos ~3,3 s da primeira faixa, diferença de até 40 ms): **nenhuma espera a
  mais**; três cliques no palco e a tecla 1 durante as faixas não escolhem nada (o achado continua esperando); a faixa
  não recebe cliques; com o movimento reduzido, a faixa inteira, parada, sem efeitos.
- Os cenários (`cenarios_faixas.py`) começam com um clique ("Começar"), porque o que o motor manda antes de a página
  abrir chega sem animação.

## A avaliação (recomendação: A)

- **A** — o ganho: lê como parte do palco (apoiada na paisagem, sem tampar o texto), é a mais leve para a Vitória que
  se repete a cada luta, e os quatro pesos se distinguem pela forma (curta e baixa, larga com raios, escura descendo,
  tira estreita). A 1280 cabe com folga. A limitação: o perfil rasgado se repete ao longo da faixa (de perto se vê o
  padrão); na noite escura (o Exausto no charco), a beira cinza quase some contra o céu.
- **B** — o ganho: o emblema dá identidade forte aos marcos (a cabeça do lobo, a de Odette) e a batida da joia marca o
  momento. A limitação: a placa do marco é alta (236 px) e, a 1280, desce sobre o texto da página; os raios atrás da
  joia ficam perto demais da linguagem do Estouro (a subida de nível usa raios e placa), e a Vitória comum com joia e
  placa pesa mais do que pede uma faixa que aparece a cada luta.

## Achados à parte (não entram na escolha visual)

- **O adiantar não encurta as faixas:** só a queda olha o clique ou a tecla (o `pular`); as outras seguram a fila pelo
  tempo todo (Vitória 1 s em toda luta, Saindo da capela 2,6 s). A causa: o `await` de tempo fixo em `celebrar`
  (`telas/celebracoes.js`), sem o laço do `pular` que a `queda` tem. Correção separada, se o Jean quiser: o mesmo laço
  nas outras (adiantar encurta; nada é pulado do que o motor manda).
- **Duas faixas ao mesmo tempo, hoje:** a animação antiga (1,6 s) dura mais que a espera do Guardião (1,5 s), e por ~0,1
  s o "Guardião derrotado!" e o "Mestre caçador" ficam um sobre o outro. As duas propostas já trocam uma pela outra.

## A demonstração

`demo.bat` ou `python ferramentas/prototipos/hud/faixas/auxiliares/demo.py`, painel em http://127.0.0.1:8768/: cada
caso nas faixas de hoje, na R (a original refinada) e, como histórico, na A e na B, numa partida de teste com
saves temporários (os seus saves não são tocados).
