# 1E.3: a Rainha Aracnídea e o Esqueleto (proposta, 21/10/2026)

**Pedido de Jean:** o próximo par da 1E.3, duas propostas de cada, só no protótipo. Os retratos aprovados ficam como
estão; nada integrado, regras, atributos e mapeamentos iguais.

## O que os dados dizem, os usos e o alcance previsto

- **Rainha Aracnídea** (o guardião `rainha_aracnidea` da floresta, `GUARDIOES` em `dados.py`): o traço `fera`; 120 de
  vida, ataque 10, agilidade 8, poder 6; teia, veneno e invocar (`invoca="aranha"`); "teias grossas como cordas cobrem
  as árvores; algo enorme desce do alto, com olhos demais para contar"; na fase 2, "guincha e seus filhotes despencam
  das copas" (e ganha a mordida sangrenta). **Usos:** só a carta da luta (32 px, o 16 a 2×); guardião não é família,
  não tem Bestiário nem contrato. Hoje: o `fera`. **Alcance previsto, se aprovada:** só ela, pelo id do guardião
  (`RETRATO_GUARDIAO`, o caminho do Rei Troll na 1.167.0); as aranhas que ela invoca continuam com o retrato da Aranha
  gigante (a família).
- **Esqueleto** (`esqueleto`, morto-vivo; 22 de vida, ataque 7, agilidade 3; investida; "ossos animados por ódio antigo;
  veneno não faz nada; luz sagrada faz muito"): no Vale, nas ruínas e na capela (o Esqueleto de Guarda do ossuário é a
  mesma família com outro nome), nos eventos e nos contratos. **Usos:** a carta da luta e o rastro dos contratos (32),
  o Bestiário, o mural e a faixa do mestre caçador (48). Hoje: a caveira. **Os papéis, separados (conferidos no código e
  nas fotos):**
  - **o esqueleto inimigo** (a família, com os afixos, os líderes, o Esqueleto de Guarda): o alcance previsto, se
    aprovado (`RETRATO_FAMILIA`);
  - **os esqueletos que o Lich Menor invoca** (`invoca="esqueleto"`): saem da mesma família; ficariam com o retrato
    junto, a menos que o Jean decida separar;
  - **o servo do Necromante** (o aliado "Esqueleto (Invocado)", `tipo="servo"`, `habilidades.py`): é outro papel (a carta
    aliada pede a caveira pelo tipo, `batalha.js`), **fora** do alcance; o `esqueleto_servo` dos dados não aparece como
    inimigo;
  - **os chefes** (o Lich Menor, a Bruxa Afogada genérica, o cavaleiro sombrio, o carniçal e os outros mortos-vivos):
    **fora**; continuam na caveira.

## As propostas

Cabeças de 16×16 no formato dos retratos de carta aprovados (sem contorno, cores agrupadas, a luz da esquerda).

- **Rainha A, de frente e enorme** (`rainha-a`; patas, corpo, marca, presas, olhos): o abdome que enche o alto do quadro
  com a ampulheta vermelha, a cabeça menor embaixo com duas fileiras de olhos âmbar, as quelíceras na cor do corpo com as
  presas vermelhas (o veneno), as patas pelos lados. A paleta é a da Aranha gigante (a mesma espécie); o vermelho é a
  marca da rainha. Na bancada, a marca começou como uma cruz e virou a ampulheta.
- **Rainha B, descendo pelo fio** (`rainha-b`; as mesmas camadas): o fio de teia no alto ("desce do alto"), o abdome com
  a marca, a cabeça com os olhos e as presas para baixo, as oito patas abertas em estrela, com dois pixels de espessura
  (na primeira passada eram linhas de um pixel, a trama que o Jean pediu para evitar).
- **Esqueleto A, de frente** (`esqueleto-a`; pescoço, crânio, órbitas): o crânio de osso envelhecido (a luz da esquerda,
  a sombra à direita), as órbitas fundas de três pixels, o nariz, as bochechas encovadas, os dentes de cima, a boca aberta
  e a mandíbula separada, as vértebras do pescoço e as clavículas descendo para os ombros. Na bancada, a primeira, clara
  e simétrica, com as clavículas retas, lembrava a caveira com ossos cruzados.
- **Esqueleto B, em três quartos** (`esqueleto-b`): virado para a esquerda, a órbita de perto maior que a de longe, a
  mandíbula um pouco caída, a coluna e o ombro de lado.

## Processo e conferência

- As grades em `auxiliares/grades.py`; as fontes **no editor pelo MCP** (`pintar.lua`, 0 diferentes na releitura em
  todas as camadas; o composto com a soma das camadas visíveis: 172, 123, 134, 134) em `fontes/<id>/<id>-16.aseprite`; a
  exportação conferida (`auxiliares/exportar.py`: igual à grade, @2x exato) com os derivados dos usos reais: a Rainha só o
  32 (a carta), o Esqueleto o 32 e o 48 (a carta e o Bestiário), em blocos inteiros, com os @2x.
- Fotos a 1920×945 (`auxiliares/fotografar.mjs`, os auxiliares do par anterior adaptados), atual × A × B com os mesmos
  dados: a Rainha com duas aranhas invocadas (o cenário `tutorial` com `CHEFE=rainha_aracnidea` e `INVOCADOS`); o mago
  necromante com o servo de pé contra dois esqueletos, um carniçal e um afogado; o Lich Menor com dois esqueletos
  invocados; o Bestiário com o esqueleto, o carniçal, a aranha e o afogado. A troca é só na página, nas cartas inimigas e
  nos cartões pelo nome ("Rainha Aracnídea" e os que começam por "Esqueleto"): o servo aliado, o carniçal e o Lich ficam
  com o desenho de hoje. Sem erro nem aviso no console.
- As folhas: `rainha.png` e `esqueleto.png` (`python auxiliares/prancha.py`): a carta (tamanho real e 2×); a Rainha ao
  lado da Aranha gigante; o Esqueleto no Bestiário e nos papéis separados; a fileira com os retratos do jogo; a 12×.

## A integração da Rainha (1.168.0)

- **Decisão de Jean:** a Rainha A, sem retoques, inclusive o abdome e a marca vermelha.
- A fonte de produção em `ferramentas/arte/aseprite/retrato-rainha-aracnidea/retrato-rainha-aracnidea-16.aseprite`
  (as mesmas camadas: patas, corpo, marca, presas, olhos); o 32 é o 16 ×2 (`DERIVADOS` do exportador), sem 48 (a
  guardiã não tem Bestiário nem contrato). Os PNGs exportados (16, 32 e os @2x) são idênticos aos da proposta;
  `exportar_aseprite.py retrato-rainha-aracnidea --conferir` fica igual ao jogo.
- No motor, `RETRATO_GUARDIAO` ganhou `rainha_aracnidea`; as aranhas comuns e as que ela invoca continuam pela família
  (o retrato da Aranha gigante). Regras, atributos e medidas iguais.
- A conferência no jogo, com os arquivos reais (o modo `final` de `auxiliares/fotografar.mjs`, só a situação da
  Rainha): a carta da Rainha com `retrato-rainha-aracnidea-32` e as duas invocadas com `retrato-aranha-32`, sem erro no
  console. A folha `rainha-final.png` (`python auxiliares/prancha.py rainha-final`).

## O Esqueleto A2: o A desenvolvido pela referência gerada (21/10/2026, proposta)

- **Pedido de Jean:** o Esqueleto A como direção, melhorado por uma referência gerada na conversa
  (`ferramentas/arte/referencias/icones/Esqueleto frontal em pixel art.png`), só no protótipo. Preservar a cabeça de
  frente, o crânio arredondado, as maçãs angulares, as órbitas fundas e separadas, a cavidade nasal, a mandíbula com
  contorno e o queixo, a coluna cervical ligada às clavículas, o osso envelhecido e a luz dos retratos do jogo; os
  dentes e as vértebras simplificados em grupos (sem grade de dentes, sorriso exagerado nem osso solto).
- **Medido na guia** (a referência reduzida a 16×16 por média, `guias/esqueleto-guia-16.png`): as órbitas são menores
  que as do A (2×2, separadas por uma ponte de 2 px), as têmporas recolhem na altura delas, a mandíbula é estreita
  (6 px, o queixo 4), o pescoço tem uma vértebra e as clavículas sobem para os ombros.
- **O desenho** (`esqueleto-a2`; pescoço, crânio, cavidades; a paleta do A com mais três tons do mesmo osso): o crânio
  redondo com a luz em cima à esquerda; as órbitas de 2×2, a de cima inclinada para dentro; o nariz de dois pixels; a
  luz da maçã embaixo da órbita esquerda; os dentes num grupo claro e a boca como uma faixa escura com dois vãos; o
  queixo; a vértebra ligando o queixo às clavículas.
- **Na bancada:** as primeiras passadas (órbitas de 3 px como as do A) davam óculos escuros ou um rosto simpático, e a
  boca subia nos cantos, como um sorriso; o crânio sem as têmporas ficava um retângulo e depois um triângulo. A guia
  resolveu as proporções; a boca virou uma faixa reta.
- **Processo:** a grade em `auxiliares/grades.py`; a fonte no editor pelo conector (`pintar.lua`, 0 diferentes na
  releitura nas três camadas; a guia por `Image{fromFile=...}`, oculta; o composto com a soma das camadas visíveis, 122)
  em `fontes/esqueleto-a2/esqueleto-a2-16.aseprite`; a exportação conferida (`auxiliares/exportar.py`: igual à grade, o
  @2x exato, o 32 e o 48 em blocos inteiros com os @2x); o conector respondendo depois da exportação em lote.
- **Fotos** (`MODOS=a,a2`, os mesmos dados, 1920×945): a luta do Necromante e a do Lich Menor, e o Bestiário; só os
  Esqueletos inimigos trocam (o servo aliado, o carniçal e o Lich com o sprite de hoje), sem erro nem aviso no console.
  A folha `esqueleto-a2.png` (`python auxiliares/prancha.py esqueleto-a2`): a referência e a guia; A × A2 na carta
  (tamanho real e 2×) e no Bestiário (48 px); as lutas com o A2; a fileira com os retratos do jogo (a Rainha
  inclusive); os PNGs a 16, 32 e 48; a 12×.
- **A minha leitura (quem aprova é o Jean):** o A2 lê como um crânio de verdade, mais magro e mais ameaçador que o A: as
  órbitas pequenas e fundas, a cavidade nasal e o queixo estreito; os dentes deixaram de ser a grade do A. Limites: a
  32 px a boca é só uma faixa escura (os dentes de baixo não aparecem), e o osso continua o retrato mais claro da
  fileira.
- **Continua fora do jogo:** o Esqueleto segue na caveira; o servo aliado do Necromante, o Lich e os outros
  mortos-vivos não mudam.

### O nariz refeito: A2n (21/10/2026, proposta)

- **Pedido de Jean:** no A2 a cavidade nasal ficou um risco estreito e comprido; refazer só essa região, com a abertura
  compacta e mais ou menos triangular da referência, separada das órbitas e da boca, sem parecer um nariz saliente; a
  ponte, as maçãs, o crânio, as órbitas, a mandíbula, o pescoço, as clavículas e a paleta como estão.
- **O ajuste** (`esqueleto-a2n`, seis pixels nas linhas 8 e 9; o A2 continua como estava): o preto do alto à direita,
  que encostava na diagonal da órbita direita, virou sombra (D); a base tem dois pretos; as paredes, n à esquerda e D à
  direita; o osso dos dois lados no alto ficou claro (O, o), separando a abertura das órbitas; a maçã esquerda (O)
  passou da coluna 6 para a 5. Julgado a 32 px na carta e depois a 48 no Bestiário: lê como a abertura de um crânio,
  compacta e mais larga embaixo, com a fileira dos dentes entre ela e a boca. Nas variantes descartadas, o topo preto
  virava um buraco grande (V2) ou uma mancha sem forma (V3).
- **Processo:** uma cópia da fonte do A2 em `fontes/esqueleto-a2n/`, retocada no editor pelo conector (`pintar.lua`:
  o pixel tirado das cavidades e os seis do crânio; releitura das três camadas contra a grade, 0 diferentes; a guia
  oculta intacta; o composto 122); a exportação conferida (igual à grade, @2x exato, 32 e 48 em blocos inteiros); o A2
  reexportado saiu idêntico ao do commit.
- A folha `esqueleto-a2n.png` (`python auxiliares/prancha.py esqueleto-a2n`): a referência × A2 × A2n na carta e no
  Bestiário em tamanho real, a 4× e a 12×, sem suavização. Sem novas fotos de luta (só a cabeça mudou).

## Avaliação (a minha leitura a 32 px; quem aprova é o Jean)

- **Rainha A (minha preferência):** é claramente a mesma espécie da Aranha gigante, maior e mais pesada; a ampulheta
  vermelha e as presas vermelhas dão a identidade de chefe sem coroa. Limite: a 32 px as duas fileiras de olhos e as
  quelíceras ficam juntas, num "rosto" um pouco parecido com uma máscara.
- **Rainha B:** a silhueta mais diferente (a estrela de patas no fio) e a que conta a cena da descrição. Limite: o corpo
  fica pequeno no meio, e as patas, mesmo grossas, ocupam a maior parte da carta.
- **Esqueleto A (minha preferência):** lê como um morto, não como o símbolo: as órbitas fundas, a mandíbula separada e as
  clavículas dão volume e ameaça. Limite: de frente, ainda fica perto de uma caveira de emblema; o osso claro é o retrato
  mais claro da fileira.
- **Esqueleto B:** o três quartos é mais vivo (a cabeça virada, a mandíbula caída). Limite: a 32 px a órbita de longe e o
  nariz se misturam, e a leitura depende da órbita grande.
