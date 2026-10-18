---
name: arte-itens-fenda
description: Desenhar, revisar ou avaliar a arte de itens e ícones de Crônicas da Fenda (equipamento, consumíveis, ícones da HUD) em pixel art em cada tamanho de uso, e levar um desenho aprovado ao jogo pelo Icones. Use quando o Jean pedir um item novo ou refeito, uma proposta de ícone, a comparação de candidatos, um tamanho novo de um desenho existente ou a integração de um desenho aprovado. Não serve para cenários (vista.js), retratos (retratos.js) nem regras de item.
---

# Arte de itens de Crônicas da Fenda

O processo que produziu o escudo final e o Unguento de Prata (1.94.0). Ele ajuda a fazer e a conferir um desenho; quem
aprova é o Jean, olhando o jogo. Nenhum passo daqui declara um resultado aprovado: entregue a proposta com as fotos e
pare para a conferência.

Caminhos relativos à raiz do repositório. O que é de um objeto só (as medidas do escudo, a forma do pote) está em
[exemplos.md](exemplos.md); não transforme aquilo em regra.

## Antes de desenhar

1. **O que o jogo diz do item.** Leia o nome, a descrição, o preço, o tipo e os usos em `rpg/itens.py` e onde o item
   aparece no texto (`grep -rn "<id>" rpg`). O desenho mostra o que o jogo diz; não acrescente brilho mágico,
   símbolo ou efeito que o jogo não tem. Nome, descrição, preço e regras não mudam por causa do desenho.
2. **O desenho atual e os papéis dele.** Veja o que `rpg/web/static/icones.js` (`Icones`) entrega hoje: o arquivo da
   família (`rpg/web/static/hud/icones/`), um desenho em código (`desenhos.js`) ou o sprite 16×16 do jogo
   (`sprites-dados.js`). Um sprite pode ter vários papéis: a "chama" é Vigor, Poder e Pena de Fênix; o "unguento" é o
   item e a Curandeira. Trocar um desenho não pode trocar outro papel; se o desenho é compartilhado, o item novo se
   acha só pelo id (`SO_PELO_ID` em `icones.js`).
3. **Onde ele aparece e em que tamanho.** O tamanho de exibição vem do lugar parado: 32 px na bolsa, mochila do
   mercado, ficha, dicas e quadro do baú; 40 px no corpo e na mochila do Inventário (equipamento); 48 no cartão
   compacto do saque e na pilha de baús; 64 no cartão do saque. Desenhe para os tamanhos em que ele de fato fica
   parado na tela; o mais visto (em geral o 32) tem prioridade. Veja abaixo o que é leitura parada e o que é animação.
4. **Silhueta, materiais e identidade.** Escreva em poucas linhas: a forma que se reconhece no tamanho pequeno, os
   materiais (cada um terá rampa e regra de luz), as características que o fazem ser este objeto e não outro, e o
   que o atual tem de bom e precisa ficar (volume, presença, personalidade). Se o pedido muda o conceito (o pote de
   louça com rótulo virou cerâmica de boticário), confirme o conceito antes de refinar.
5. **As referências aprovadas.** Abra em tamanho real os dois objetos aprovados pelo método, que mostram o nível de
   acabamento esperado e convivem com a família pintada:
   - o escudo: `rpg/web/static/hud/icones/escudo-32.png`, `-40`, `-48`, `-64` (metal, reflexo especular localizado);
   - o unguento: `rpg/web/static/hud/icones/unguento-32.png`, `-64` (cerâmica fosca, pasta macia).
   Compare também com os vizinhos da família (`espada-32.png`, `anel-32.png`, `pocao-32.png`): o novo precisa caber
   ao lado deles.

**Símbolos da interface não são equipamentos.** Os ícones de atributo, da doca, dos recursos e das ações são
símbolos funcionais: a skill orienta o acabamento e a coerência com a família, mas eles não precisam copiar
literalmente um equipamento do jogo. A bota da Agilidade, por exemplo, pode ter pose própria para comunicar movimento
em vez de repetir a bota de couro de perfil. Volume, personalidade e leitura do material contam mais que a semelhança
com a peça (decisão do Jean, 18/10/2026, ao recusar as propostas chapadas dos atributos e da doca).

## Desenhar

O desenho é um script Python em `ferramentas/arte/`, um por objeto, com as etapas comuns de
`ferramentas/arte/pixel_comum.py`. Copie a estrutura de `desenhar_unguento_pixel.py` (forma de revolução) ou de
`desenhar_escudo_pixel.py` (disco com partes); não crie outra biblioteca.

- **Do 32 para os outros tamanhos** (o processo desde a 1.110.0). Comece pela arte principal em 32, o tamanho mais
  visto, e avalie a leitura dela no jogo antes de fazer os outros. Aprovada a leitura:
  - a apresentação maior (o 64 do cartão do saque) pode ser a ampliação inteira exata do 32 (2×, vizinho mais
    próximo, sem retoque), quando o resultado no jogo for aprovado;
  - os tamanhos intermediários (40, 48) se derivam da fonte aprovada: as mesmas formas e medidas na grade do tamanho
    (`MEDIDAS`), retocando contornos ou detalhes onde for preciso;
  - a construção, a silhueta e a identidade do objeto são as mesmas em todos (ver "Um objeto só" abaixo);
  - uma versão própria mais detalhada de um tamanho só quando o ganho visual justificar o trabalho: compare no jogo,
    no mesmo espaço e com os mesmos dados, a versão detalhada com a ampliação inteira antes de decidir.
  Um arquivo final no tamanho de uso não precisa ter sido redesenhado do zero. Não vale como acabamento: filtro,
  suavização, quantização, "pixelização" ou redução por fator não inteiro. O @2x é a duplicação exata (`salvar`). Os
  itens aprovados antes desta orientação ficam com os arquivos que têm; trocar algum deles pede comparação própria.
- **Leitura parada × animação.** São duas coisas diferentes:
  - *leitura parada* é onde o desenho fica para ser lido (a bolsa, o corpo, a mochila, a prateleira, o cartão do
    saque, o quadro do baú). Cada tamanho desses tem arquivo nativo (desenhado na grade dele ou derivado da fonte
    aprovada, como acima): é ali que vale tudo o que esta skill pede;
  - *transformação de animação* é o que uma animação faz com uma imagem enquanto ela anda e some em menos de um
    segundo: o consumível que voa até a bolsa é o arquivo de 32 com `scale` de 1,3 a 0,8 no caminho (`itemVoa`, em
    `app/pagina.js`); o item que voa até o corpo encolhe até 0,45 (`voarIcone`, em `telas/celebracoes.js`). Isso não é
    acabamento do desenho, não pede arquivo próprio e não muda com um item novo: as animações ficam como estão.
  - O que já existe e se apoia na redução do navegador para um tamanho parado (o martelo e a Pena de Fênix em 48, a 2×
    reduzida, em `desenhos.js`; um pedido de tamanho sem arquivo, que `Icones` serve com o mais perto) é herança, não
    regra. Um desenho novo não usa a redução do navegador como acabamento: se ele fica parado num tamanho, esse
    tamanho tem arquivo próprio (desenhado ou derivado por ampliação inteira).
- **Duas camadas.** `mat` (o material de cada pixel; `"c"` é o contorno) e `tom` (o índice na rampa do material);
  `fixo` protege o que foi desenhado de propósito (um brilho, um cravo) da limpeza.
- **Luz deliberada.** A luz é a de `pixel_comum.LUZ` (de cima e da esquerda, um pouco de frente), igual para todos os
  objetos. Decida a luz e a sombra em grupos de pixels por parte do objeto: o tom pela direção da superfície em poucas
  faixas largas, as sombras que mostram a construção (o que está por baixo, a borda que vira), o reflexo como uma
  mancha desenhada onde a luz bate. Cada material tem a sua rampa (do escuro ao claro) e a sua regra: metal leva
  especular forte e localizado; vidrado, um reflexo baixo e estreito; fosco (barro, papel, couro), só a luz da forma;
  pasta, luz macia em volta de um ponto. A quantidade de cores sai do desenho, não de um limite (o escudo usa 17 a 18,
  o unguento 14).
- **Contorno.** 1 pixel, só pelos lados (`contornar`), na cor comum (`CONTORNO`).
- **Limpeza.** `limpar` tira pixels sozinhos de um tom no meio de outro; depois, as correções olhando cada tamanho vão
  em `AJUSTES` (`{(x, y): (material, tom)}`), com um comentário dizendo o porquê.
- **Adaptar por tamanho.** O detalhe que não cabe sai do tamanho pequeno em vez de virar ruído: uma emenda, uma base,
  um sulco, a barriga de um pote podem existir só em 48 e 64. A espessura de uma borda pode ser 1 px em 32 e 2 em 64.
  Uma silhueta que ganha um degrau solto num tamanho perde aquele detalhe naquele tamanho.
- **Um objeto só em todos os tamanhos.** Simplificar por tamanho (menos faces, um reflexo de 1 px, um detalhe que
  sai) é diferente de mudar a construção do objeto (outro corte de pedra, outra forma de cabo, outra proporção entre
  comprimento e largura). A simplificação é esperada; a mudança de construção num tamanho só é um defeito, mesmo num
  tamanho já aprovado: a silhueta, o afunilamento e o formato das partes principais são os mesmos nos quatro.
- **Grave fora do jogo enquanto for proposta:** `python ferramentas/arte/desenhar_<objeto>_pixel.py <pasta>` grava
  numa pasta qualquer (use o scratchpad ou uma pasta do protótipo); sem a pasta, grava em `rpg/web/static/hud/icones/`,
  o que só se faz na integração.

Para os itens pintados da família de ferro (as peças em `ferramentas/arte/familia-ferro/`), um tamanho novo sai de
`python ferramentas/arte/familia_ferro.py` (a mesma escala do grupo e a redução "paleta" de sempre; `--conferir` refaz
todos e compara com os do jogo). Isso não é redesenho: é o processo de preparação da família, que preserva o desenho.

### Desenhar no Aseprite (pelo MCP)

Quando o desenho é feito no Aseprite (a varinha, 1.109.0), a fonte final é o `.aseprite`, não um script. O conector
(um servidor MCP com uma extensão do Aseprite; o testado foi o `aseprite-mcp-bridge`) é da máquina de quem desenha,
não do repositório: confira as ferramentas da sessão antes e, sem elas, use o caminho dos scripts acima. Detalhes e
uso em `ferramentas/arte/aseprite/LEIA-ME.md`.

- **Três tipos de operação, registrados separados:** as *ferramentas do conector* (criar documento, camadas, salvar,
  abrir, exportar, a captura do editor), as *operações em Lua* pelo `execute_script` (a pintura e a leitura) e os
  *cálculos auxiliares fora do editor* (as listas de pixels por regra, as pranchas, o @2x). No registro da proposta,
  diga qual foi qual.
- **Pintar pelo `ferramentas/arte/aseprite/pintar.lua`, nunca pelo `put_pixels`.** O `put_pixels` da extensão (1.0.0)
  descarta em silêncio o pixel fora do retângulo da cel (a cel que o lápis do Aseprite cria, uma cel deslocada ou fora
  da tela) e responde com o total pedido; e escreve sem gerar desfazer. O `pintar.lua` troca a imagem da cel por uma
  que cobre a cel e a tela, numa transação (um passo de desfazer), recusa e lista o que cai fora da tela e relê cada
  pixel depois de gravar. As listas entram por `dofile` (um `.lua` que faz `return "<lista>"`): `io.open` e
  `saveCopyAs` para PNG num script abrem uma janela do Aseprite e travam o conector.
- **Camadas úteis:** uma por parte do objeto que alguém vá querer mexer depois (na varinha, oito; o número é do
  objeto, não regra), o contorno por cima. Guarde em `ferramentas/arte/aseprite/<peça>/<peça>-<lado>.aseprite`.
- **Exportar e comparar:** `python ferramentas/arte/exportar_aseprite.py <peça> [<pasta>]` (o 1× pela linha de comando
  do Aseprite, o @2x pela duplicação exata; sem pasta, grava no jogo, o que só se faz na integração);
  `--conferir` exporta numa pasta temporária e compara com os do jogo. Um tamanho tirado de outro por ampliação inteira
  (o 64 do couro, o 32 ampliado 2×) fica explícito por peça na tabela `DERIVADOS` do exportador, sem fonte própria. Na proposta, reabra cada `.aseprite` e confira
  que o composto exportado é igual, pixel a pixel, à imagem do editor e ao que as listas pediam.

## Conferir

1. **A silhueta numa cor só, antes da cor.** Pinte cada tamanho numa cor (preenchimento claro, contorno escuro) e
   confira lado a lado: as mesmas partes com a mesma forma, afunilamentos num sentido só (sem barrigas nem o eixo indo
   e voltando), as larguras de cada parte proporcionais ao tamanho. Ajuda medir o perfil de través parte por parte.
   Depois, o desenho completo.
2. **Tamanho real sobre o carvão.** `python ferramentas/arte/prancha.py <png> [<png>...] -o <saida.png>` monta cada
   arquivo em 1× num nicho de item sobre o carvão da HUD, com a ampliação ao lado para achar o pixel. Julgue pelo 1×:
   a ampliação engana (o que parece limpo de perto pode virar mancha, e um degrau solto só aparece de longe). Olhe o
   novo ao lado do atual e dos vizinhos da família.
3. **Dentro das telas.** Suba o jogo nos lugares onde o item aparece, em janela normal (1500×950) e baixa (1280×720):
   `ferramentas/arte/fotografar_itens.mjs` fotografa o mercado, o cartão do saque com a comparação, o voo ao equipar,
   o baú aberto, o voo de um consumível até a bolsa, o Inventário (anéis, arrastar, dois cliques, teclado) e conta o
   arquivo e o tamanho de cada desenho em cada lugar. Para um item novo, acrescente o lugar dele (um cenário em
   `tests/navegador/cenarios.py`) em vez de criar outro roteiro. Para uma proposta, troque só os arquivos pedidos pela
   página (`page.route` em `/static/hud/icones/<peça>-*.png`, como em `ferramentas/prototipos/hud/fotografar_escudo.mjs`),
   com o jogo intacto.
4. **O mesmo objeto no cenário e na interface.** Quando o objeto existe também no mundo (as cenas da capela em
   `rpg/web/static/telas/cenas.js`, as paisagens de `vista.js`, a banca do mercador em `telas/mercado.js`), fotografe
   as duas representações lado a lado (o cenário pelo cenário de teste dele, como `capela` em
   `tests/navegador/cenarios.py`): o item pode ter mais detalhe, mas material, cor e identidade precisam ser os mesmos.
5. **Papéis separados.** Confira que só o papel pedido mudou: equipamento, atributo, consumível e personagem são
   papéis diferentes, ainda que o jogo use o mesmo sprite.

## Entregar

- Proposta: as fotos em tamanho real (normal e baixa), o atual ao lado, uma avaliação curta do que melhorou e do que
  piorou, e pare. Não integre nem descarte candidatos sem o Jean.
- Integração (só do que o Jean aprovou): grave em `rpg/web/static/hud/icones/` pelo script (ou, com fonte no
  Aseprite, pelo `exportar_aseprite.py`, guardando os `.aseprite` finais em `ferramentas/arte/aseprite/`); registre os tamanhos em
  `TAMANHOS` de `icones.js` e o papel (`ITEM`, `CONSUMIVEL`, `SO_PELO_ID`); confirme que os arquivos aprovados saem
  idênticos (compare pixel a pixel com os da proposta); rode as verificações do `CLAUDE.md` e
  `fotografar_itens.mjs`; atualize as lacunas em `docs/ARQUITETURA.md` ("A interface web"). O jogo nunca lê nada de
  `ferramentas/`.
- Registre em `roadmapIDEIAS/00-COMECE-AQUI.md` o que entrou, o que ficou como proposta e o que continua antigo.
