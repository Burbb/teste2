# O Barqueiro do Charco: o estudo nativo de 32 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** o conceito aprovado (o barqueiro morto que continua atravessando os afogados, os passageiros dele;
`../identidades/LEIA-ME.md`) num estudo em 32 nativos, só no protótipo, sem adaptação para 16 e sem integração. A
direção: um velho encharcado, de rosto afundado e pele cinza-esverdeada, com rosto suficiente à mostra para a idade e a
expressão; a rede no pescoço e nos ombros, sem cobrir o rosto; a luz verde da lanterna vindo de baixo; o enquadramento
perto (a cabeça e o começo dos ombros). O gorro, se ajudar a silhueta. A lanterna, o barco e a vara podem ficar fora.

## O que foi feito

- **O estudo `barqueiro-n32`**, à mão (`auxiliares/grade.py`, sem guia):
  1. **o gorro** ficou: dá ao topo uma silhueta redonda, que nenhum retrato vizinho tem, e a barra dobrada recebe um
     brilho da luz de baixo;
  2. **o rosto:** a testa com rugas, as sobrancelhas brancas, os olhos fundos com o brilho verde, o nariz comprido com a
     ponta acesa, as bochechas fundas, o bigode branco ralo sobre a boca fechada, o queixo e o pescoço magro;
  3. **a luz de baixo:** o queixo, o lábio, a ponta do nariz e as pálpebras de baixo acesos em verde; a testa e o gorro
     no escuro;
  4. **a rede:** enrolada no pescoço e caindo sobre os ombros, em losangos, com os nós mais claros perto do centro (onde
     a lanterna está), sobre o casaco escuro.
- **O que não funcionou no caminho** (as passadas ficaram fora do repositório): as sombras das bochechas em linhas
  verticais escuras liam como pintura de guerra; a faixa clara do lábio acima de uma linha escura lia como um sorriso de
  dentes, e um bloco escuro de 4×2 como boca aberta (ficou o bigode caído sobre uma linha só); a rede em xadrez lia como
  camisa (ficou a malha em losangos, mais esparsa); a luz em faixa contínua do queixo ao pescoço lia como uma barra.
- **A fonte, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector sem editor, a janela do Jean não foi tocada): `fontes/barqueiro-n32/barqueiro-n32-32.aseprite`, em camadas
  (casaco, rede, pele, gorro, olhos, contorno), 0 diferentes na releitura, reaberta com as camadas na ordem; a exportação
  igual à grade, alfa só 0 ou 255, o @2x em blocos inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), a 1920×945, com o guardião de verdade: rodadas numa cópia da
  branch `claude/barqueiro-do-charco` (onde o covil do pântano já tem o Barqueiro, ainda sem retrato), `CHEFE=
  barqueiro_do_charco` com um Afogado (o retrato de produção); o modo "atual" (a caveira que a branch mostra) e o estudo,
  trocado só na carta, na página. Sem erro no console. **A folha:** `comparacao.png` (a luta em tamanho real, a carta a
  2×, a fileira com a Ilse, o Profeta, o Afogado, a Hidra, o Lich e o Senhor da Guerra, e a ampliação a 10× sem
  suavização).

## A minha leitura (quem decide é o Jean)

- **A conferência técnica passou;** isso não é aprovação visual.
- **O que funciona:** na carta, lê como um velho morto de gorro com o olhar verde e a luz de baixo; a silhueta redonda do
  gorro e a rede nos ombros o separam da Ilse (o cabelo de algas, a pele azul), do Profeta (o capuz cinza, os olhos
  vendados) e do Lich (a coroa, o violeta). O olhar e a boca fechada dão uma expressão cansada, severa.
- **As limitações visuais:**
  - **perto do Afogado na cor:** os dois têm a pele cinza-esverdeada; o que separa é o gorro, a rede, os olhos acesos e
    a luz de baixo, não a pele. Na fileira a 1×, os dois ficam lado a lado como parentes;
  - **o rosto ainda é duro:** os planos das bochechas e da testa leem como pedra em alguns pontos, e a expressão depende
    muito dos dois pontos verdes; o bigode quase some a 1×;
  - **a rede a 1×** vira um pontilhado dourado no peito, que pode ler como bordado ou cota de malha; a 3× lê como rede;
  - **sem a lanterna no quadro,** o "sobrenatural" vem só da cor da luz e dos olhos.
- **Fora desta rodada:** a adaptação para 16 e qualquer integração.

## Suspenso (23/10/2026)

**Mudança de direção (Jean, 23/10/2026):** o modo "Novo jogo" procedural deve sair no futuro, ficando só a campanha. A retirada não entra agora: pede um levantamento próprio, porque o modo pode compartilhar código com a campanha. **Suspensos** (o que ainda não tinha começado): a adaptação para 16 e a integração do Barqueiro e do antagonista, o retrato do Barqueiro na branch e a junção da branch `claude/barqueiro-do-charco` (com a migração v6→v7 dos covis) à produção. Os estudos e a branch ficam preservados como estão. Os retratos exclusivos do modo procedural não bloqueiam o plano.
