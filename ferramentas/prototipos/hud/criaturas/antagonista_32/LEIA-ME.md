# O antagonista do mundo gerado: o estudo nativo de 32 (23/10/2026, protótipo; nada no jogo)

**Pedido do Jean:** a direção A de `../identidades/LEIA-ME.md` (o humano que a Fenda está apagando) num estudo em 32
nativos, só no protótipo, sem adaptação para 16 e sem integração: um rosto humano de traços ambíguos, parcialmente
desfeito por uma fissura irregular, com o Vazio interrompendo a face; a expressão e a deterioração carregam a
identidade. Sem diadema nem coroa; sem a divisão reta em duas metades; servindo aos títulos masculinos e femininos e às
cinco origens, sem acessório de nenhum deles; o conteúdo do jogo como base, sem virar regra nem fato novo.

## O que foi feito

- **O estudo `antagonista-n32`**, à mão (`auxiliares/grade.py`, sem guia):
  1. **o rosto:** magro, sem idade marcada, sem barba e sem marca de gênero; o cabelo escuro partido ao meio, caindo até a
     gola; as sobrancelhas tristes (o canto de dentro mais alto), um olho humano de frente, cansado, o nariz e a boca
     fechada;
  2. **a fissura:** irregular, em diagonal: sai do cabelo na têmpora, abre um buraco no lugar do outro olho (o trecho mais
     largo), desce ao lado do nariz e corta o canto da boca até a mandíbula; dentro, o preto e o violeta escuro da Cria do
     Vazio, sem estrelas nem brilho; a borda de cima com uma linha violeta, a de baixo escura; lascas claras na borda e
     rachaduras finas; três lascas se soltando da cabeça, para cima e para a direita (o "se desfaz como cinza" do fim);
  3. **a gola alta** escura, de quem já teve posto, sem insígnia.
- **O que não funcionou no caminho** (as passadas ficaram fora do repositório): a primeira fissura descia na vertical,
  na borda do rosto, e o dividia em duas metades (o que o Jean pediu para evitar); virou a diagonal; depois, a diagonal de
  largura igual lia como um corte ou um raio, e ganhou largura variável, saltos, o buraco maior no olho e as lascas. As
  sobrancelhas com as pálpebras escuras formavam um "X" (ficaram só as sobrancelhas tristes).
- **A fonte, pelo Aseprite em lote** (`python auxiliares/grade.py ..` e `python auxiliares/exportar.py --montar`; o
  conector sem editor, a janela do Jean não foi tocada): `fontes/antagonista-n32/antagonista-n32-32.aseprite`, em camadas
  (gola, cabelo, rosto, vazio, lascas, contorno), 0 diferentes na releitura, reaberta com as camadas na ordem; a
  exportação igual à grade, alfa só 0 ou 255, o @2x em blocos inteiros que voltam ao original.
- **As fotos** (`auxiliares/fotografar.mjs`, `capturas/`), a 1920×945: o antagonista montado pelo jogo
  (`inimigos.instanciar_antagonista`, pelo `auxiliares/cenario_antagonista.py`, que só o põe na luta) ao lado da Cria do
  Vazio (o retrato de produção); o jogo hoje (o sprite humano), o estudo com "Noiva da Peste" e com "Rei Enforcado",
  trocado só na carta, na página. Sem erro no console. **A folha:** `comparacao.png` (a luta em tamanho real, a carta a
  2× nos três modos, a fileira com a Cria do Vazio, o Caído, o Profeta, o Lich, a Ilse e o Senhor da Guerra, e a
  ampliação a 10× sem suavização).

## A minha leitura (quem decide é o Jean)

- **A conferência técnica passou;** isso não é aprovação visual.
- **O que funciona:** na carta, lê como um rosto humano pálido rasgado pelo Vazio, com o buraco no olho como o ponto
  mais forte; serve igual à "Noiva da Peste" e ao "Rei Enforcado"; a cor do rasgo liga o antagonista à Cria do Vazio que
  ele invoca, e nada nele lembra a coroa do Lich.
- **As limitações visuais:**
  - **a moldura escura do cabelo** em volta do rosto claro lembra, a 1×, o capuz do Profeta das Cinzas (a mesma massa:
    um oval claro dentro de um escuro);
  - **o rasgo ainda é uma diagonal** com começo e fim claros: lê como fissura, mas pode ler como cicatriz ou corte;
  - **a expressão é sutil:** o olho humano é pequeno a 1×, e o cansaço e a tristeza aparecem mais na ampliação do que na
    carta;
  - **as lascas soltas** são pixels isolados; a 1× podem passar por ruído.
- **Fora desta rodada:** a adaptação para 16 e qualquer integração (o papel seria pela família `antagonista`, sem mudança
  de save).

## Suspenso (23/10/2026)

**Mudança de direção (Jean, 23/10/2026):** o modo "Novo jogo" procedural deve sair no futuro, ficando só a campanha. A retirada não entra agora: pede um levantamento próprio, porque o modo pode compartilhar código com a campanha. **Suspensos** (o que ainda não tinha começado): a adaptação para 16 e a integração do Barqueiro e do antagonista, o retrato do Barqueiro na branch e a junção da branch `claude/barqueiro-do-charco` (com a migração v6→v7 dos covis) à produção. Os estudos e a branch ficam preservados como estão. Os retratos exclusivos do modo procedural não bloqueiam o plano.
