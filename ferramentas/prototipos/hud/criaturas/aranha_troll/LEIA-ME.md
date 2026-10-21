# 1E.3: a Aranha Gigante e o Troll (proposta, 21/10/2026)

**Pedido de Jean:** o próximo par da 1E.3, duas direções de cada, só no protótipo. Os retratos aprovados (Afogado, Ilse,
Lobo, Bandido, os três animais, os heróis e a comitiva) ficam como estão; nada integrado, regras, atributos e
mapeamentos iguais. O Rei Troll fica fora.

## O que os dados dizem e o alcance previsto

- **Aranha gigante** (`aranha`, `dados.py`: fera; 18 de vida, agilidade 7; teia e veneno; "tecem armadilhas entre as
  árvores; seu veneno paralisa antes de matar"): nos bosques (com o lobo, o bandido, o javali, o ent jovem e o caído),
  nos contratos de caça e nas que a **Rainha Aracnídea** invoca (`invoca="aranha"`). Hoje o retrato é o `fera`, o rosto
  de lobo de olhos vermelhos.
- **Troll da montanha** (`troll`: gigante; 55 de vida, ataque 10, agilidade 1; esmagar e regenerar; resiste pouco ao
  fogo, `resist fogo 1.4`; a partir do nível 4 da região; "regeneram quase tudo, menos o fogo; fique longe quando ele
  recuar para golpear"): nas montanhas e nos contratos. Hoje cai na **caveira** (o traço `gigante` não tem retrato).
- **O alcance, se um for aprovado** (o caminho da 1.162.0 e da 1.163.0: `RETRATO_FAMILIA` em `dados.py` e o papel
  `CRIATURA` em `icones.js`): só as famílias `aranha` e `troll`, com os afixos, os líderes de nome próprio e as
  invocadas (as aranhas da Rainha). **Continuam como estão:** a **Rainha Aracnídea** (guardiã, no `fera`) e o **Rei
  Troll** (guardião, na caveira; não presumir que use o retrato do Troll comum), o `fera` das outras feras (o javali, o
  rato, o sapo, a sanguessuga, o lobo gélido, a Hidra) e a caveira dos mortos-vivos. Nenhum sprite trocado globalmente.
- **Onde aparece:** a carta da luta e o rastro dos contratos (32 px, o 16 a 2×), o Bestiário, o mural e a faixa do
  mestre caçador (48 px, a 3×).

## As propostas

Cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno, cores agrupadas, a luz da esquerda),
desenhadas pela silhueta e o volume primeiro; nenhum desenho nativo de 32 nem de 48.

- **Aranha A, de frente** (`aranha-a`; patas, corpo, presas, olhos): de perto, o abdome atrás da cabeça com a marca
  clara, a carapaça peluda, os olhos pretos em fileira com um brilho frio cinza (sem branco, para não ficar simpática),
  as quelíceras e as presas de ponta avermelhada, os palpos e as patas em arco dos dois lados. Na bancada: estava escura
  demais na carta (o corpo e as patas clarearam um tom) e os brilhos brancos dos olhos davam um ar fofo.
- **Aranha B, de lado em ameaça** (`aranha-b`; as mesmas camadas): a cabeça à esquerda com os olhos e a presa, as patas
  da frente erguidas, o abdome grande atrás com a marca clara em cruz, as outras patas descendo até a base. Na bancada:
  a primeira ficava pequena no quadro e o abdome listrado lembrava abelha; uma versão de frente com um olho grande no
  meio lia como um bicho de um olho só.
- **Troll A, de frente** (`troll-a`; musgo, pele, rosto): a cabeça enorme que enche o quadro, a pele cinza-esverdeada
  de pedra, a testa baixa com a sombra das sobrancelhas, os olhos pequenos e amarelos no fundo, o nariz grande, a boca
  fechada com as presas de baixo, o musgo no alto e nos ombros. Na bancada: sem o nariz lia como crocodilo, e a boca
  reta lia como sorriso.
- **Troll B, de perfil com a corcunda** (`troll-b`; as mesmas camadas): a cabeça baixa e pequena virada para a esquerda,
  na frente de uma corcunda de musgo e pedra que enche o quadro, o nariz comprido, a sobrancelha pesada, o olho amarelo,
  o queixo projetado com a presa. Na bancada, a boca aberta parecia falar; ficou fechada.

## Processo e conferência

- As grades em `auxiliares/grades.py`; as fontes **no editor pelo MCP** (`pintar.lua`, 0 diferentes na releitura) em
  `fontes/<id>/<id>-16.aseprite`, o composto de cada uma com exatamente os pixels das camadas (116, 139, 191, 188); a
  exportação com a conferência (`auxiliares/exportar.py`: o 1× igual à grade, @2x exato, alfa 0/255) em `proposta/`, e
  os derivados que a produção usaria: o 32 e o 48 (o 16 ×2 e ×3, em blocos inteiros) com os @2x. Os auxiliares são os
  do par Lobo e Bandido, adaptados.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`), atual × A × B com os mesmos dados: uma luta do guerreiro com duas
  aranhas, um troll e um lobo (o cenário `tutorial` com `GRUPO`); e o Bestiário com as duas espécies, o Lobo e o Afogado
  (o `covil` com `BESTIARIO`). A troca é só na página, nas cartas inimigas e nos cartões cujo nome começa por "Aranha"
  ou "Troll". O registro (`capturas/registro.json`) guarda a caixa de cada carta e de cada cartão; sem erro nem aviso no
  console.
- As folhas: `aranha.png` e `troll.png` (`python auxiliares/prancha.py`): a carta (tamanho real e 2×), o Bestiário com o
  vizinho aprovado, a fileira na caixa da carta com os retratos aprovados (Morel, Odette, Afogado, Ilse, Lobo, Bandido,
  Urso, Falcão) e o atual, A e B (tamanho real e 3×), a luta e a 12×.

## Avaliação (a minha leitura a 32 px; quem aprova é o Jean)

- **Aranha A (minha preferência):** lê como aranha na hora (as patas em arco dos dois lados, os olhos em fileira e as
  presas), sem ar simpático, e funciona igual na carta e no Bestiário. Limite: é escura (uma aranha marrom no fundo
  escuro), e as patas finas viram uma textura a 1×.
- **Aranha B:** a pose de ameaça e o abdome grande dão mais ação e uma silhueta própria. Limite: a cabeça e os olhos são
  pequenos; a 2× a leitura depende da silhueta, e as patas de baixo se misturam.
- **Troll A (minha preferência):** grande e bruto, enche o quadro como o Urso; o nariz, a testa baixa e as presas de
  baixo dizem "troll" e não "homem grande". Limite: de frente, chega perto de um ogro; o musgo é o que o liga à
  montanha.
- **Troll B:** a silhueta mais diferente de todos os retratos (a corcunda de pedra e musgo com a cabeça pequena na
  frente), e o perfil com o nariz comprido é o mais "troll de conto". Limite: o rosto ocupa só um terço do quadro; a 2×
  o olho e a presa são pequenos, e a corcunda pode ler como uma pedra.

## Segunda rodada: três de cada pelas referências geradas (21/10/2026)

**Pedido de Jean:** as propostas A e B não foram escolhidas (ficam aqui como histórico). Três propostas livres de cada
pelas duas referências geradas na conversa, que ele deixou em `ferramentas/arte/referencias/icones/` (registradas no
`LEIA-ME.md` de lá): a aranha de frente (os olhos agrupados, as quelíceras fortes, as presas separadas, as patas
articuladas) e o troll **de carne** (a referência substitui a direção de pedra e musgo: a testa baixa, o nariz largo, a
mandíbula pesada, o pescoço grosso, duas presas saindo da mandíbula de baixo; bruto e pouco inteligente, sem caricatura).
A Rainha Aracnídea e o Rei Troll continuam fora. Nada integrado.

- **Aranha 1, a transposição de frente** (`aranha-1`; patas, corpo, quelíceras, presas, olhos): o abdome atrás, a
  carapaça, os olhos âmbar em duas fileiras, as quelíceras cinza com as presas claras separadas, e as patas grossas
  (segmentos de 2 px com as juntas claras) subindo para os cantos de cima e descendo pelos lados.
- **Aranha 2, o rosto de perto** (`aranha-2`): os olhos e as quelíceras grandes, as presas compridas até embaixo, só a
  ponta das patas nos cantos.
- **Aranha 3, as patas erguidas em arco** (`aranha-3`): as patas da frente erguidas por cima da cabeça, de canto a canto,
  o corpo menor embaixo no meio, os olhos e as presas.
- **Troll 1, a transposição em três quartos** (`troll-1`; roupa, pele, presas, rosto): a orelha à esquerda, a testa baixa
  com a sombra sobre os olhos pálidos, o nariz largo, a boca caída nos cantos, as duas presas subindo da mandíbula por
  cima do lábio, o pescoço grosso e a roupa de couro nos ombros.
- **Troll 2, de frente** (`troll-2`): a cabeça estreita em cima e a mandíbula larga embaixo, a testa baixa, as presas dos
  dois lados da boca caída, o pescoço que vira os ombros.
- **Troll 3, de perfil para a esquerda** (`troll-3`): a testa saliente, o olho pálido, o nariz, a boca inclinada para
  baixo, o queixo projetado com a presa, a nuca pequena e o pescoço grosso com a roupa.
- **Na bancada:** as patas finas da primeira passada viravam linhas (o que o Jean pediu para evitar) e ficaram com 2 px e
  as juntas claras; os trolls sorriam (a boca reta de ponta a ponta, o olho com brilho branco e o verde claro demais
  davam um sapo simpático): a pele escureceu, a boca encurtou e caiu nos cantos, o olho virou um ponto pálido na sombra
  e as presas passaram por cima do lábio; o perfil, que lia como uma massa verde, ganhou a testa, o nariz e o queixo.
- **Processo:** a referência reduzida a 16×16 por média (`guias/aranha-guia-16.png`, `guias/troll-guia-16.png`) para
  medir, e as grades redesenhadas à mão em `auxiliares/grades.py` (letras próprias; as cores das propostas A e B não
  mudam). As fontes pelo MCP (`pintar.lua`, 0 diferentes na releitura em todas as camadas; a guia oculta); o composto do
  editor com exatamente a soma das camadas visíveis; a exportação conferida (igual à grade, @2x exato, o 32 e o 48 em
  blocos inteiros com os @2x). Fotos a 1920×945 com os mesmos dados (`MODOS=r2-1,r2-2,r2-3`: a aranha e o troll de
  mesmo número juntos), sem erro nem aviso no console.
- **As folhas:** `aranha-r2.png` e `troll-r2.png` (`python auxiliares/prancha.py r2`): a referência e a guia; as três na
  carta a 32 px (tamanho real e 2×) e no Bestiário a 48 px; a fileira com os retratos aprovados; a 12×.

**Avaliação (a minha leitura a 32 px; quem aprova é o Jean):**

- **Aranha 1:** a mais fiel à referência e a mais completa (as patas dos dois lados dizem "aranha" de longe). Limite: a
  6 px de largura o rosto fica pequeno, e os olhos âmbar viram uma faixa laranja.
- **Aranha 2 (minha preferência):** a mais ameaçadora a 32 px: as presas compridas e os olhos grandes leem na hora, e as
  pontas das patas nos cantos bastam para a espécie. Limite: sem as patas inteiras, depende das presas; de longe pode
  lembrar uma máscara com presas.
- **Aranha 3:** a pose de ataque, com as patas em arco, tem a silhueta mais forte. Limite: o corpo e os olhos ficam
  pequenos no meio, e as patas, com as juntas claras, ganham mais peso que o rosto.
- **Troll 1 (minha preferência):** o mais próximo da referência: a mandíbula pesada com as presas, a testa baixa e a
  orelha dão o tamanho e a brutalidade. Limite: a 32 px o olho é um ponto só, e a expressão vem mais da boca e das presas
  do que do olhar.
- **Troll 2:** o de frente é o mais imponente na carta (a mandíbula de lado a lado). Limite: de frente e simétrico,
  chega mais perto de um ogro genérico; a orelha some.
- **Troll 3:** a silhueta mais diferente (a testa e o queixo projetados), e o perfil reforça a ideia de pouca
  inteligência. Limite: o rosto ocupa a metade de cima à esquerda; a 32 px a presa é pequena e o nariz se confunde com a
  testa.

## Integração do Troll (1.166.0)

**Escolha de Jean:** o **Troll 1**, em três quartos (`troll-1`, do `4d43ce10`), sem retoques, pela família `troll`. O
Rei Troll fica fora do mapeamento (continua na caveira); a Aranha segue no protótipo.

- **A fonte de produção:** `ferramentas/arte/aseprite/retrato-troll/retrato-troll-16.aseprite`, aberta do `troll-1` pelo
  MCP, com a guia oculta. A exportação: `exportar_aseprite.py retrato-troll` (`DERIVADOS`: o 32 é o 16 ×2 e o 48 o 16 ×3,
  cada um com o @2x); `--conferir`: tudo igual ao jogo. O 16 é igual pixel a pixel ao `proposta/troll-1-16.png`.
- **No jogo:** `RETRATO_FAMILIA` com `troll` (`dados.py`) e `CRIATURA` com `retrato-troll` (`icones.js`): a família
  inteira, com os afixos, os líderes de nome próprio e o nêmesis. O **Rei Troll** é um guardião (família `guardiao`, o
  traço `gigante`) e continua na caveira (conferido no teste e na foto). Traços, regras, atributos e medidas iguais.
- **Fotos a 1920×945** (o modo `final`, sem troca): a carta (32 px de um arquivo de 32) e o Bestiário (48 de 48), com a
  aranha no `fera` e o lobo e o afogado com os retratos deles; uma luta nova com o Rei Troll (o cenário `tutorial`
  ganhou `CHEFE=<id>`, o guardião pelo `instanciar_guardiao`), um troll e uma aranha. Sem erro nem aviso no console. A
  folha: `troll-final.png` (`python auxiliares/prancha.py troll`).
