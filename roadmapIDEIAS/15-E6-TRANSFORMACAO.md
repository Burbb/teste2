# 15 — E6: especificação de uma transformação de habilidade

Revisão 1 — 11/10/2026. Jogo na versão 1.61.0. **Entrega só de design:** nenhum código, habilidade, talento, número ou
save foi alterado. Nada aqui está aprovado: é a proposta para Jean decidir.

Legenda (a mesma do [14](14-E5-DIAGNOSTICO-CLASSES.md)):

- **[código]**: comportamento conferido no código, com o arquivo citado;
- **[medido]**: número tirado do 14, que foi calculado pelas funções do jogo;
- **[proposta]**: regra ou número novo, **não aprovado**;
- **[decidir]**: escolha que cabe a Jean antes da implementação.

## 1. Resumo

- **Recomendação:** a **Lança de Gelo** do Mago ganha uma transformação, a **Prisão de Gelo**. Ela troca dano e preço
  pela certeza de congelar:
  - **Lança de Gelo (hoje):** dano bom e barato, com 35% de chance de congelar.
  - **Prisão de Gelo (proposta):** pouco dano e mais cara, mas o congelamento é certo.
- **Por que esta:**
  - a escolha nova aparece num momento que o Vale já tem: o golpe preparado da capela;
  - a repetição tem limites que já existem no jogo: a mana do Mago, o estado "firme" e a resistência de chefes e gigantes;
  - nenhum alvo novo nem bloco novo é preciso, só o jeito de resolver "qual versão este herói usa".
- **Como se obtém:** um talento do tronco do Mago (nível 4), de 1 ponto, que **substitui** a Lança de Gelo daquele herói
  [proposta]. É a primeira vez em que comprar um talento faz abrir mão de algo, e não só escolher a ordem.
- **Arquitetura mínima:**
  - a variante mora fora do catálogo de habilidades aprendíveis;
  - o personagem continua guardando `lanca_gelo`;
  - quem pergunta "qual ficha usar" passa por uma função que olha os talentos daquele herói. O catálogo global nunca muda.
- **Primeira implementação** (seção 9): só esta transformação, com testes de isolamento entre heróis, a validação da
  seção 8 e as decisões da seção 10 tomadas antes.

## 2. O que já existe

### 2.1 Habilidades e talentos [código]

- **`habilidades.py`.**
  - Cada habilidade é uma ficha `hab(nome, custo, alvo, desc, passos)`.
  - Os passos (Dano, Se, Aplicar, Buff...) executam na luta e se descrevem no Grimório: o número existe num lugar só.
  - `HABILIDADES` é um dicionário de módulo, compartilhado por todos os heróis da sessão.
- **Quem consulta `HABILIDADES[id]` direto:**
  - `combate/heroi.py`: o bloqueio, as metas do menu, o menu e a execução;
  - `grimorio.py`;
  - `web/estado.py`;
  - `talentos.custo_habilidade`;
  - `sistemas/progressao.py`: o texto de "nova habilidade";
  - `especializacao.py`: a comparação da encruzilhada;
  - o bloco `Salva`.

  Nenhum deles sabe de versões por herói. O 04 já registrava isso ("Habilidade efetiva — extensão proposta").
- **Talentos e modificadores (`talentos.py`, `modificadores.py`).**
  - Um talento declara `stats`, `mods`, `mults` e `gatilhos`, e o jogo pergunta `mod(u, chave)` e `disparar(...)`.
  - Os talentos que mexem numa habilidade só mudam **números**: Muralha (`escudo_turnos`, `custo:erguer_escudo`),
    Escudo Rúnico, Ignição, Legião de Ossos, Golpe Sombrio, Matilha.
  - **Nenhum muda alvo, passos ou comportamento** (14, seção 2.4).
- **Não há como desfazer um talento.** Não existe redistribuição, nem templo que devolva pontos (`grep` no código).
- **Personagem.** `j.habilidades` guarda ids (`"lanca_gelo"`); `j.talentos` guarda `{id: rank}`. Os dois vão no save.

### 2.2 As regras de controle que a proposta usa [código]

- **`atordoado`** (`estados.py`):
  - perde o próximo turno;
  - quem está atordoado não esquiva (`sem_esquiva`);
  - **chefes e gigantes resistem metade das vezes** (`resiste`);
  - **interrompe um golpe preparado** (`combate/turnos.py`: o golpe devastador se perde).
- **`firme`**: depois de perder um turno, o alvo fica firme por um turno e **não pode ser atordoado nem congelado de
  novo**. É o que impede travar um inimigo para sempre. A tela já mostra a recusa (lance `efeito_negado`).
- **Lança de Gelo hoje:** 130% de dano de gelo (Poder), à distância, esquivável. Se acertar, 35% de congelar
  (`Aplicar("atordoado", 1, chance=0.35, rotulo="congelado")`). Custa 10 de mana e vem no nível 2 da classe.
- **Mana:** regenera 3 por turno, e só 20% volta depois da luta. É a única classe em que o recurso pesa (14, 2.1).
- **Quem prepara o Golpe Esmagador** (220%, avisado um turno antes):
  - no mundo gerado: troll e abominação (**gigantes**), mercenário, golem e cavaleiro sombrio;
  - na campanha: o Esqueleto de Guarda do ossuário e o Afogado Inchado do sarilho (1.57.0).
- **Quem os inimigos atacam** (`escolher_alvo_inimigo`): o herói, salvo um aliado provocando. Os aliados levam 25% dos
  ataques (45% com o urso; 15% vindos de chefes).

### 2.3 O que o 14 já mediu sobre o Mago [medido]

- **Lança de Gelo no nível 3:** média 19 por 10 de mana (1,9 por ponto). A Bola de Fogo: 22 por 14 (1,6). A Lança rende
  mais por mana; a Bola, mais por turno.
- **O Mago é a classe com mais decisões por turno hoje.** A transformação não precisa "consertar" um botão morto: ela
  abre uma segunda forma de jogar a mesma classe.

## 3. Candidatos comparados (no máximo três)

| | A. Lança de Gelo → **Prisão de Gelo** (Mago) | B. Erguer Escudo → **Desafio** (Guerreiro) | C. Golpe Pesado → **Golpe Varredor** (Guerreiro) |
|---|---|---|---|
| Ideia | Menos dano, mais caro; congela com certeza | O herói provoca (os inimigos o atacam) e a guarda cai de −50% para −30% | 120% no alvo e 60% num segundo inimigo, em vez de 170% num só |
| Decisão que cria | Garantir a interrupção do golpe preparado, ou ferir e torcer pelos 35% | Proteger a comitiva, ou se proteger | Concentrar num inimigo, ou espalhar |
| O que limita a repetição | Mana (3 por turno); `firme` (não congela duas vezes seguidas); chefes e gigantes resistem metade [código] | Quase nada: o Vigor não aperta (6 por turno para 8) [medido] | Nada: o Vigor não aperta [medido] |
| Risco de virar a ação de todo turno | Baixo; precisa ser medido com aliados (seção 8) | Alto com a Muralha (3 turnos por 4 de Vigor), os espinhos e o Contra-ataque | **Alto**: quase toda luta do Vale tem 2 inimigos, e espalhar 180% contra 170% ganharia sempre |
| Valor real no jogo de hoje | Claro: o Vale já tem dois preparadores na capela | **Pequeno**: os aliados só levam 25% dos ataques [código], e a provocação no herói não muda nada (os inimigos já miram o herói) | Médio, e sobreposto ao Tiro Duplo e ao Redemoinho |
| Extensão necessária | Só a resolução da ficha por herói | Provocação no herói (o motor só a lê nos aliados) | Só a resolução da ficha (o bloco `Dano(em="outro")` existe) |
| Veredito | **Recomendado** | Depois, se a comitiva passar a ser mais atacada | Não: repete o problema do Passo Ágil, uma ação melhor quase sempre |

**Por que não B agora:** o motor já faz os inimigos mirarem o herói em 75% das vezes. Um "Desafio" tiraria pouco dos
aliados e cobraria proteção do herói. Ele só faria sentido com outra regra de alvo, fora desta etapa.

**Por que não C:** sem recurso que limite, uma ação que rende mais com dois inimigos vira a escolha de quase toda luta
do Vale. É o que a seção 14 do 14 viu no Passo Ágil.

## 4. A proposta: Prisão de Gelo

### 4.1 Original e transformada

| | Lança de Gelo (existe) [código] | Prisão de Gelo [proposta] |
|---|---|---|
| Classe | Mago (nível 2), nas duas especializações | A mesma, para quem comprar o talento |
| Alvo | Um inimigo | Um inimigo (igual) |
| Custo | 10 de mana | **16 de mana** |
| Dano | 130% gelo (Poder), à distância | **70% gelo** (Poder), à distância |
| Acerto | Pode ser esquivado | **Não pode ser esquivado** (como o Julgamento: `Dano(esquiva=False)`) |
| Controle | Se acertar, **35%** de congelar 1 turno | **Congela 1 turno, sem sorteio**, salvo as regras de sempre (abaixo) |
| Regras que continuam valendo | `firme`; chefes e gigantes resistem metade; congelar interrompe o golpe preparado | As mesmas, sem exceção |
| Ícone e família | `gelo`, `gelo` | `gelo` (ou `cadeado`) [decidir], família `gelo` |

**Médias no nível 4** [estimativa; a implementação confere com os blocos]: Lança cerca de 21; Prisão cerca de 11.

### 4.2 Quando cada uma é a melhor escolha [hipótese, a medir na seção 8]

- **A Prisão de Gelo é melhor quando:**
  - um inimigo forte prepara o Golpe Esmagador (220%) e não é gigante nem chefe: o mercenário, o golem, o cavaleiro
    sombrio, o Esqueleto de Guarda, o Afogado Inchado. A Lança interrompe em 35%; a Prisão, sempre;
  - contra o troll e a abominação (gigantes) e os guardiões (chefes), ela interrompe em 50%, contra 17,5% da Lança;
  - a comitiva ou o servo precisam de um turno sem o inimigo agindo: quem está congelado não esquiva [código];
  - o inimigo esquiva muito, e a Lança erraria.
- **A Lança de Gelo é melhor quando:**
  - ninguém prepara nada: o dano conta mais;
  - há grupos: congelar um de três quase não muda a luta, e a Lança é a magia mais barata por dano;
  - a mana está curta: a Lança custa 10, a Prisão 16;
  - o alvo está firme: a Prisão não congela, e sobra só um golpe fraco.
- **Quem compra o talento perde a Lança.** Os grupos e as lutas sem preparo ficam com a Bola de Fogo (mais cara) e o
  Dardo Arcano. É a perda relevante: a escolha de build diz "eu respondo a inimigos fortes" e paga em eficiência.

### 4.3 Como se obtém e se ativa [proposta]

- **Talento "Prisão de Gelo":**
  - no ramo **tronco** do Mago, camada 2 (nível 4), ao lado do Escudo Rúnico;
  - máximo 1 ponto.
- **Efeito:** a Lança de Gelo daquele herói passa a ser a Prisão de Gelo, no menu, no Grimório e na luta.
- **Sem ativação na luta:** é passiva, como os outros talentos. Não há botão de trocar de versão.
- **Por que no tronco e no nível 4:**
  - vale para Piromante e Necromante;
  - chega quando a capela mostra os preparadores (o Vale termina perto do nível 4);
  - compete com o Escudo Rúnico e com os talentos da especialização no mesmo ponto.
- **Alternativa** [decidir]: camada 1 da base (nível 2, quando a Lança chega). Mais cedo, mas compete com Mente Vasta e
  Potência Arcana, que são números puros.

### 4.4 Desfazer [decidir]

- **Proposta para a primeira implementação: não desfazer.** Como todo talento hoje (2.1), a compra é definitiva.
  - A árvore mostra as duas versões lado a lado **antes** de comprar, com os números do herói, como a encruzilhada já
    faz desde a 1.58.0. Olhar não compra.
  - A compra pede confirmação, como a especialização. Avisa que a Lança de Gelo sai do menu.
- **Por que não desfazer agora:** não há estrutura para isso. Criar uma é um sistema de reespecialização, fora do
  escopo da E6.
- **Alternativas registradas, não propostas agora:**
  - **por item:** um grimório único que declara a transformação; vestir transforma, tirar desfaz. Usa o que já existe
    (`itens.fonte_item` aceita mods de item, e trocar de grimório na luta gasta o turno). Mas é assunto da E7
    (equipamento ligado à build) e da revisão de loot (onde o item cai);
  - **"esquecer" num templo:** uma reespecialização pequena. Fica para quando houver mais de uma transformação.

### 4.5 Menu, Grimório e resultado [proposta]

- **Menu de habilidades** (luta e tela):
  - o botão mostra "Prisão de Gelo", o custo (16 de mana), o ícone e a descrição da variante;
  - com o alvo firme, o botão continua disponível. A dica do alvo já diz "firme". Usar mesmo assim só dá o golpe
    fraco, e isso é decisão do jogador.
- **Grimório:**
  - a ficha é a da variante, com os números do herói;
  - uma linha diz a origem: "Transformada pelo talento Prisão de Gelo (no lugar da Lança de Gelo)";
  - as regras que já valem continuam ditas pelos estados (firme, chefes, golpe preparado).
- **Árvore de talentos:**
  - o nó compara "Lança de Gelo" e "Prisão de Gelo" com os números do herói (custo, dano médio, chance de congelar);
  - a descrição é **calculada** das duas fichas, não escrita à mão. O 04 pede isso para os efeitos novos.
- **Resultado na luta** (com as mensagens e lances que já existem):
  - "Prisão de Gelo" no rótulo da ação;
  - o dano;
  - "congelado" no alvo, ou "resiste" (chefe ou gigante), ou "firme" (recusa).
  - Se o alvo preparava um golpe: "o golpe devastador se perde", a mensagem que já existe.

### 4.6 Interações [código + proposta]

- **Talentos:**
  - **Eficiência** (custo −10% por ponto) vale para a Prisão, como para todas;
  - nenhum outro talento mexe na Lança hoje;
  - **proposta de regra:** um mod `custo:<id>` vale para o id **efetivo**. `custo:lanca_gelo` não pegaria na Prisão,
    e a Prisão teria o seu `custo:prisao_gelo`. Hoje nenhum talento usa `custo:lanca_gelo`, então nada muda.
- **Especializações:**
  - **Piromante:** a Prisão não acende. Congelar e depois Bola e Combustão é uma sequência possível, mas cara em mana.
  - **Necromante:** o servo provoca e a Prisão congela: dois turnos de proteção. Combinação a medir (seção 8).
- **Equipamento:**
  - o Poder escala o dano (70%);
  - crítico e roubo de vida de itens valem para o golpe fraco, como para qualquer golpe;
  - nenhum item muda a chance de congelar.
- **Comitiva:**
  - quem está congelado não esquiva, então os golpes de Morel, Yara e Odette acertam sempre naquele turno;
  - é a sinergia mais forte e o principal risco de repetição (seção 8).
- **Invocações:** o servo (Necromante) e o animal (não se aplica ao Mago) não mudam a regra; só se beneficiam do turno
  sem ataque.
- **Guardiões e o rito de Ilse:**
  - a guardiã é chefe e resiste metade;
  - o piso do rito e o momento dele não mudam, porque congelar não tira vida.

### 4.7 Saves antigos e heróis sem a transformação [proposta]

- **Nenhum campo novo no save.** O talento entra em `j.talentos` como qualquer outro. `j.habilidades` continua com
  `lanca_gelo`.
- **Save antigo:** o herói não tem o talento, então tem a Lança de Gelo. Nada a migrar.
- **Heróis sem o talento**, outras classes, o mundo gerado e o gabarito: a ficha resolvida é a original.
- **O gabarito e a árvore.**
  - Um nó novo na árvore do Mago pode mudar as escolhas do robô, se ele chegar à árvore no nível 4.
  - A implementação confere isso. Se mudar, examina as transcrições e atualiza de propósito.
- **Telemetria:**
  - a contagem de uso por habilidade registra o id **efetivo** (`prisao_gelo`), para as medidas de equilíbrio
    separarem as duas;
  - os outros números do registro não mudam.

## 5. Regras: o que existe e o que é proposto

| Regra | Situação |
|---|---|
| Lança de Gelo: 130%, 35% de congelar, 10 de mana | Existe [código] |
| Atordoado/congelado: perde o turno, não esquiva, interrompe o golpe preparado | Existe [código] |
| Firme depois de perder o turno; não congela de novo | Existe [código] |
| Chefes e gigantes resistem metade | Existe [código] |
| Talentos não se desfazem | Existe [código] |
| A Prisão de Gelo e os números dela (16 de mana, 70%, sem esquiva, sem sorteio) | **Proposta** |
| O talento no tronco, camada 2, de 1 ponto, substituindo a Lança | **Proposta** |
| Mods `custo:<id>` valem para o id efetivo | **Proposta** |
| Uma transformação por habilidade (a validação recusa duas) | **Proposta** |
| Comprar com confirmação e comparação lado a lado | **Proposta**, no padrão da encruzilhada (existe) |

## 6. Arquitetura mínima [proposta]

1. **A variante não entra em `HABILIDADES`.**
   - Ela mora num dicionário próprio, `VARIANTES = {"prisao_gelo": hab(...)}`, em `habilidades.py`, ao lado da Lança e
     com os mesmos blocos (`Dano`, `Se`, `Aplicar`).
   - Assim, as listas de habilidades por classe, a encruzilhada e os testes de conteúdo não a veem como habilidade
     aprendível.
2. **A ficha efetiva por herói: `efetiva(u, h_id)`.**
   - Devolve `VARIANTES[v]` quando uma fonte do herói declara `transforma = {h_id: v}`; senão, `HABILIDADES[h_id]`.
   - Junto vai o id efetivo, para custo, telemetria e animação.
   - É uma consulta, sem cache global e sem alterar dicionários. Dois heróis na mesma sessão resolvem cada um o seu.
3. **`transforma` nas fontes de modificadores.**
   - `modificadores.fontes(u)` já percorre classe, especialização, talentos comprados e itens vestidos.
   - O talento declara `transforma={"lanca_gelo": "prisao_gelo"}`. A única extensão é ler esse campo.
   - A validação de conteúdo (`tests/test_modificadores`) recusa:
     - uma variante que não existe;
     - uma habilidade que não é da classe;
     - duas fontes transformando a mesma habilidade.
4. **Trocar as consultas diretas** (2.1) por `efetiva(j, h_id)`:
   - `motivo_bloqueio`, `metas_habilidades`, `menu_habilidades` e a execução;
   - `custo_habilidade`;
   - o Grimório e a tela;
   - o texto da progressão;
   - a encruzilhada.

   O menu continua respondendo pelo id guardado (`lanca_gelo`). O nome, o ícone, o custo, o alvo, a descrição e a
   execução saem da mesma ficha efetiva, e por isso **descrição, prévia e execução não podem divergir**.
5. **A descrição do talento** é calculada das duas fichas (4.5). Nada de número escrito à mão.

**Fica de fora:** um sistema para centenas de transformações, alvos aliados, preparação de habilidades, árvore com
pré-requisitos e reespecialização. Nenhum hook novo de combate: a Prisão usa só blocos existentes.

## 7. Riscos

- **Repetição com aliados.** Congelar a cada dois turnos (o `firme` impede mais) enquanto a comitiva bate sem errar.
  Contra um inimigo forte sozinho, isso pode virar a política dominante. A mana (16 a cada dois turnos, contra 6 de
  regeneração) deve impedir que dure a luta inteira; é o principal ponto a medir.
- **Transformar a resposta ao preparo numa certeza barata.** O Passo Ágil com desvio mostrou que uma resposta certa,
  usada sempre, vira a ação padrão (14, seção 14). Aqui, o `firme` e o custo seguram. A seção 8 mede a política
  "sempre" justamente para ver isso.
- **Perder a Lança dói demais.** Se o Mago sem a Lança ficar pior em grupos a ponto de ninguém comprar o talento, a
  transformação não cria build nenhuma. A medida da seção 8 diz isso também.
- **Talento definitivo.** Sem desfazer, uma compra por engano pesa. A confirmação e a comparação (4.4) mitigam.

## 8. Validação planejada

**Critério:** demonstrar uma escolha útil, e não uma ação melhor em quase todo encontro. Não julgar por dano isolado nem
só pelo robô: vitória, vida perdida, turnos, mana ao fim, golpes preparados que acertaram e lutas que não acabam (limite
de 200 turnos, a lição da seção 14 do 14).

### 8.1 Cenários (mesma régua para as duas versões)

| Grupo | Encontro | Herói | O que mostra |
|---|---|---|---|
| Alvo único com preparo | Esqueleto de Guarda (ossuário); Afogado Inchado (sarilho) | Mago 3–4, base, Piromante, Necromante | A vantagem no Vale |
| Alvo único com preparo, fora do Vale | Mercenário sozinho; golem; cavaleiro sombrio | Mago 6–7 | Preparador forte sem resistência |
| Gigante e chefe | Troll; abominação; guardião do mundo gerado; Ilse (destruir) | Mago 4 e 7 | A resistência de metade |
| Alvo único sem preparo | Javali; lobo sozinho | Mago 3–4 | Onde a Lança deve ganhar |
| Grupo | Três lobos; três bandidos; carniçais; os dois cultistas da sacristia | Mago 3–7 | Onde a Lança e a Bola devem ganhar |
| Com aliados | Os encontros de alvo único acima, com Morel; com Odette; com Yara | Mago 4 e 7 | A sinergia de quem não esquiva |
| Com servo | Os mesmos, Necromante com servo | Necromante 5–7 | Provocar e congelar juntos |
| Mana curta | Os de alvo único, começando com metade da mana | Mago 4 | O custo de 16 |
| Ferido | Os de alvo único, começando com 45% de vida | Mago 4 | A pressão real do preparo |

### 8.2 Políticas comparadas

1. **Dano:** como hoje (Bola de Fogo e Lança, ataque básico quando a mana falta).
2. **Lança no preparo:** a Lança de Gelo quando o alvo prepara; dano no resto.
3. **Prisão no preparo:** a Prisão quando o alvo prepara; dano no resto (Bola e Dardo).
4. **Prisão sempre:** a Prisão sempre que o alvo não está firme. É a repetição abusiva.
5. **Prisão sempre, com aliados ou servo:** a 4 com a comitiva e o servo.
6. **Prisão no preparo, com Meditar** quando a mana cai abaixo de um terço.

### 8.3 Leitura esperada [hipótese]

- A 3 ganha da 2 contra preparadores fortes sozinhos (vitória ou vida perdida). Contra gigantes e chefes, ganha menos.
- A 4 perde da 1 e da 3 na maioria dos encontros, e perde em todos os grupos.
- A 5 não pode virar a melhor política na maioria dos encontros com aliados. **Se virar, a transformação volta para a
  mesa** (custo maior, ou o alvo firme por mais tempo [decidir]), como o desvio do Passo Ágil.
- Em grupos, sem a Lança, o Mago transformado perde pouco em vitória, mas gasta mais mana. Se perder muito, o talento
  não terá comprador.

### 8.4 Além do robô

- **Testes de regra.** Os números do Grimório batem com a execução. Um herói com o talento e outro sem, na mesma
  sessão, mantêm fichas diferentes, e o catálogo continua idêntico. Também entram nos testes:
  - save e carga;
  - `firme`;
  - chefe e gigante;
  - interrupção do preparo;
  - o save antigo.
- **No navegador**, a 1500 e 1280 px: o menu, o Grimório e a árvore com a comparação; a luta mostrando congelado,
  resiste e firme.
- **Jean jogando:**
  - o cenário `capela` com `CLASSE=mago ETAPA=ossuario` e o talento já comprado (o cenário ganharia a opção);
  - o mesmo sem o talento, para sentir a diferença no Esqueleto de Guarda.
- **Equilíbrio:** `tests.equilibrio` e `tests.replay` antes e depois para o Mago, e as tabelas no registro, pelo ciclo
  do COMO_CRIAR.

## 9. Escopo da primeira implementação [proposta]

1. `habilidades.py`: `VARIANTES` com a Prisão de Gelo; `efetiva(u, h_id)`; descrição pela ficha efetiva.
2. `modificadores.py`: ler `transforma` das fontes; a validação de conteúdo.
3. `talentos.py`: o talento "Prisão de Gelo" (tronco, camada 2, 1 ponto), com descrição calculada; a confirmação da
   compra e a comparação.
4. Trocar as consultas diretas listadas em 6.4.
5. A tela: o nó da árvore com a comparação; a linha de origem no Grimório. O menu e a luta já desenham a partir da ficha.
6. Testes da seção 8.4; o cenário de navegador; as medidas da seção 8 fora do repositório, com as tabelas no registro.
7. O gabarito conferido. Se mudar, só pelo nó novo da árvore do Mago, examinado e atualizado de propósito.

**Fora:**

- desfazer;
- o item;
- outras transformações;
- outras classes;
- alvos aliados;
- preparação de habilidades;
- equilíbrio geral;
- a dívida do Morel;
- loot;
- capítulos novos.

## 10. Decisões para Jean antes de implementar

1. **A candidata:** Prisão de Gelo (recomendada), ou outra.
2. **Os números:** 16 de mana; 70% de dano; sem esquiva; congelar sem sorteio, salvo firme, chefes e gigantes. Todos
   [proposta], a confirmar pela medida da seção 8.
3. **Onde fica o talento:** tronco, nível 4 (recomendado), ou base, nível 2.
4. **Desfazer:** definitivo, com comparação e confirmação (recomendado), ou esperar a E7 e fazer por item.
5. **O nome e o ícone:** "Prisão de Gelo", ícone `gelo` ou `cadeado`.
