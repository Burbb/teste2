# 15 — E6: especificação de uma transformação de habilidade

Revisão 2 — 11/10/2026. **Implementada na 1.62.0** com as decisões de Jean (seção 11). O que foi feito está na seção
12, o que foi medido na 13 e o que depende de Jean jogar na 14. As seções 1 a 10 são a especificação de antes, sobre a
1.61.0, mantida como registro. Onde a decisão mudou a proposta (o "desfazer" da 4.4, a confirmação da compra), vale a
seção 11.

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

## 11. Decisões de Jean (11/10/2026)

- **A transformação:** a Prisão de Gelo, a única da E6.
- **Números iniciais de validação:** 16 de mana, 70% de dano de gelo, sem esquiva, congelar sem o sorteio inicial. O
  `firme` e a resistência de chefes e gigantes continuam. Podem mudar pelos resultados.
- **O talento:** no tronco do Mago, nível 4 (camada 2), 1 ponto.
- **Definitivo, com troca:** a compra não se desfaz, mas a versão se troca na vila ou no acampamento. Na luta, só a
  versão escolhida. Sem reespecialização e sem tela nova: a menor solução dentro do Grimório.
- **Nome e ícone:** "Prisão de Gelo", ícone `gelo`.
- **Fora:** a E7, a dívida do Morel, a revisão de loot e outras transformações.

## 12. O que foi implementado (1.62.0)

- **Motor** (`rpg/habilidades.py`):
  - `VARIANTES` com a Prisão de Gelo, com os blocos de sempre:
    `Dano(0.7, gelo, esquiva=False)` e, se acertar, `Aplicar("atordoado", 1)` sem chance (nenhum sorteio).
  - `efetiva(u, h_id)` resolve a ficha por herói: a variante quando uma fonte libera (`transforma`) **e** o herói
    escolheu levá-la (`versoes`, no personagem); senão, a do catálogo. `HABILIDADES` não muda.
  - `versao` (o id usado), `escolher_versao`, `ficha`, `origem` e `resumo_versao` (os números do herói numa versão,
    lidos da ficha).
- **Talento** (`rpg/talentos.py`): "Prisão de Gelo", tronco, camada 2, 1 ponto, `transforma={"lanca_gelo": "prisao_gelo"}`.
  - A compra (`talentos.aprender`) já leva a Prisão e avisa como voltar.
  - A descrição do nó é calculada das duas fichas com os números do herói (custo, dano médio, esquiva, chance de
    congelar). Nada escrito à mão.
  - `custo_de(j, id)`: o `custo:<id>` vale para o id da versão; a Eficiência vale para as duas.
- **Consultas trocadas por `efetiva`:**
  - o menu e as metas da luta, o bloqueio, a execução e o custo;
  - o Grimório (página, regras gerais, críticos) e o estado da tela;
  - o glossário de cores.
  - A telemetria e a animação recebem o id da versão (`prisao_gelo`).
- **A troca** (`Progressao.opcoes_versao` e `trocar_versao`):
  - na vila e no acampamento, uma opção com meta `versao`;
  - na tela gráfica, ela é escondida e vira o botão "Levar a …" na página da habilidade no Grimório;
  - fora da vila e do acampamento, a página diz onde trocar;
  - no modo texto, é uma linha do menu;
  - a luta não oferece troca;
  - a troca entra no registro da partida (`versao`) e o replay a reproduz.
- **O Grimório** mostra, na página da habilidade transformada, a origem ("Versão liberada pelo talento Prisão de Gelo, no
  lugar da Lança de Gelo"), as duas versões lado a lado com os números do herói e a troca.
- **Saves:** nenhum campo novo para quem não tem o talento. O save antigo carrega a Lança. A escolha volta do save.
  `VERSAO_SAVE` não mudou.
- **O robô lutador** (`tests/arena.py`): antes ele escolhia o ataque mais caro como o mais forte, e passou a usar a
  Prisão como dano principal. Agora usa a Prisão em quem prepara o golpe (a meta `variante`, que só a habilidade
  transformada leva), como uma pessoa faria. Quem não tem a transformação joga igual.
- **Testes:**
  - `tests/test_transformacao.py`, com isolamento entre dois heróis, catálogo intacto, custo com Eficiência,
    prévia, menu e Grimório, congelamento sem esquiva, dano dentro da faixa do Grimório, `firme`, chefe e gigante
    (metade), interrupção do preparo, sem troca na luta, compra, troca na vila e no acampamento, a página do Grimório,
    save e save antigo;
  - a validação de conteúdo para `transforma` em `tests/test_modificadores.py`;
  - as variantes na checagem do catálogo em `tests/test_habilidades.py`.
- **Cenário de comparação:** `capela` com `PRISAO=prisao` ou `PRISAO=lanca` (seção 14).

## 13. Resultados medidos [medido]

**Como:** lutas inteiras no combate real (os inimigos agem de verdade), com roteiros de decisão explícitos. O mesmo
herói (nível, talentos, equipamento mediano de `dev.vestir`) e as mesmas sementes nas duas versões; só a versão e o
roteiro mudam. 200 lutas por célula, sem poções, de dia e com tempo limpo. Luta que passa de 200 turnos conta como
impasse. O script fica fora do repositório, como os das medidas do 14.

- **Heróis:**
  - Piromante e Necromante no nível 4, com dois builds: típico (Potência Arcana 2 e Prisão) e mana (Canalização 2,
    regeneração 7, e Prisão);
  - nível 6 com Canalização 2, Eficiência 2 e Prisão: a Prisão custa 13;
  - nível 7 típico (Potência Arcana 3, Prisão e 2 da especialização) e mana (Canalização 2, Eficiência 2, Prisão e
    Potência 1).
  - Canalização e Eficiência estão sempre no máximo que o nível permite.
- **Condições:**
  - vida cheia, ferido (45%) e metade da mana;
  - com Morel, Odette ou Yara;
  - Necromante com servo, sozinho e com Morel ou Yara.
- **Encontros:**
  - **no Vale:** ossuário e sarilho (preparadores), Ilse (destruir), javali e lobo sozinhos, três lobos, bruxa e
    sapo, os dois cultistas;
  - **depois do Vale:** mercenário sozinho e com bandido, golem, cavaleiro sombrio, troll, abominação, dois
    guardiões (um com golpe preparado), três bandidos, carniçais.
- **Roteiros:**
  - **Dano (Lança):** Bola em quem não queima, a Lança, o Dardo sem mana. Inferno contra três ou mais, Maldição
    contra dois ou mais.
  - **Lança no preparo.**
  - **Dano (Prisão guardada):** só a Bola, que vale para as duas versões.
  - **Prisão no preparo.**
  - **Prisão sempre:** congela o mais perigoso sempre que ele não está firme.
  - **Prisão + Dardo alternados:** a repetição que se paga com o ataque básico.
  - **Prisão no preparo + Meditar.**

**No total:** 315 células (herói × condição × encontro), 7 roteiros cada, cerca de 441 mil lutas.

**Por tipo de encontro** (médias dos heróis; vitória, vida perdida, golpes preparados que acertaram por luta):

| Encontro, condição | Dano (Lança) | Só Bola | Prisão no preparo | Prisão sempre | Prisão + Dardo |
|---|---|---|---|---|---|
| Preparador único, vida cheia | 99%, 32%, 0,20 | 99%, 32%, 0,20 | 100%, 25%, 0,02 | 100%, 24%, 0,01 | 100%, 28%, 0,01 |
| Preparador único, ferido 45% | 71%, 25% | 70%, 26% | **82%**, 22% | **84%**, 19% | 76%, 23% |
| Preparador único, com aliado ou servo | 100%, 18% | 100%, 18% | 100%, 14% | 100%, **12%** | 100%, 14% |
| Preparador único, metade da mana | 99%, 31% | 99%, 32% | 100%, 31% | 98%, 44% | 93%, 54% |
| Gigante, vida cheia | 95%, 49% | 96%, 43% | 96%, 40% | 87%, 50% | 69%, 70% |
| Chefe, vida cheia | 46%, 82% | 60%, 71% | 59%, 70% | 29%, 87% | 1%, 100% |
| Chefe, com aliado ou servo | 58%, 72% | 66%, 63% | 67%, 62% | 48%, 76% | 14%, 96% |
| Inimigo único sem preparo, vida cheia | 100%, 8% | 100%, 8% | 100%, 8% | 100%, 4% | 100%, 6% |
| Grupo, vida cheia | 94%, 49% | 95%, 49% | 95%, 49% | 68%, 73% | 66%, 74% |
| Grupo, com aliado ou servo | 98%, 34% | 98%, 34% | 98%, 34% | 87%, 51% | 86%, 52% |

**Melhor roteiro que usa a Prisão contra o melhor que não usa** (a Lança, ou só a Bola), célula a célula. Conta como
relevante uma diferença de 3 pontos de vitória, ou vitória igual e 5 pontos de vida perdida:

| Encontro | Células | A Prisão é melhor | Equivalente | A outra é melhor |
|---|---|---|---|---|
| Preparador único | 125 | 40 | 84 | 1 |
| Gigante | 46 | 9 | 37 | 0 |
| Chefe | 53 | 2 | 45 | 6 |
| Inimigo único sem preparo | 30 | 6 | 24 | 0 |
| Grupo | 61 | 0 | 61 | 0 |
| **Total** | **315** | **57 (18%)** | **251 (80%)** | **7 (2%)** |

**O que isso diz:**

- **Tem papel próprio.**
  - Contra o inimigo forte que prepara o golpe, a Prisão é a resposta: os golpes preparados que acertam caem de cerca
    de 0,2 para 0,02 por luta, e o herói ferido vence 82% em vez de 71%.
  - Contra gigantes ela ajuda pouco, e contra chefes empata com a Bola, porque eles resistem metade.
- **Não domina.**
  - Em 80% das células, dá no mesmo levar uma ou outra.
  - Em grupos, nunca é melhor.
  - A repetição ("Prisão sempre", "Prisão + Dardo") é pior em todo grupo, gigante e chefe: em 120 das 160 células
    dessas, perde por margem relevante.
  - Ela só vence contra um inimigo único **sem resistência**.
- **O ponto forte: golem e cavaleiro sombrio sozinhos.**
  - Congelar a cada dois turnos tira metade das ações deles.
  - Ferido (45%) no nível 7, o herói vence 89–97% com "Prisão sempre", contra 34–70% sem a Prisão.
  - De vida cheia, com Yara ou o servo, a vida perdida cai de 25–36% para 10–13%.
  - Cabe na função ("eu respondo a inimigos fortes"), mas é o lugar a sentir jogando (seção 14). Se for demais, o
    menor ajuste é a Prisão deixar o alvo firme por 2 turnos em vez de 1. Só a repetição perde; a resposta ao preparo
    continua.
- **Mana:**
  - Canalização e Eficiência no máximo não tornam a repetição mais forte: ela é a melhor em 24% das células de
    preparador tanto no build de mana quanto no típico.
  - Nessas lutas, a mana não é o que limita; limitam o `firme`, a resistência e o pouco dano.
  - Com metade da mana, a repetição piora: perde 44% de vida contra 31%.
- **Nenhum impasse** em 200 turnos, em nenhuma das cerca de 441 mil lutas, inclusive "Prisão + Dardo" contra chefes.
- **Sem a Lança, o Mago não perde nada mensurável em grupos:** a Bola cobre, com um pouco menos de mana ao fim (62%
  contra 66%).
- **A leitura esperada (8.3), conferida:**
  - a resposta ao preparo ganha contra preparadores fortes sozinhos e ganha menos contra gigantes e chefes: **sim**;
  - a repetição perde em todos os grupos, gigantes e chefes: **sim**. Mas ela ganha contra um inimigo único sem
    resistência, o que a hipótese não previa;
  - com aliados ou o servo, a repetição não é a melhor na maioria dos encontros: **sim**, é a melhor em 35% das células
    com aliado ou servo, quase todas de inimigo único, e nunca em gigante ou chefe;
  - em grupos, o Mago transformado perde pouco: **sim**, não perde nada.
- **Os números ficam:** 16 de mana, 70%, sem esquiva, sem sorteio, `firme` e resistência como estavam.

**Equilíbrio e replay** (o ciclo do COMO_CRIAR, antes e depois):

- `tests.equilibrio --spec piromante` e `--spec necromante`, com 30 lutas por nível: as diferenças ficam dentro do
  ruído.
  - Os talentos são sorteados, e o nó novo muda o sorteio.
  - Na média das lutas comuns dos níveis 4 a 12: Piromante 69,7% → 66,8%; Necromante 85,4% → 87,1%.
  - Com 90 lutas por nível, o Piromante fica igual nas lutas comuns: vitória 69,8% → 69,4%, vida perdida
    43,6% → 44,6%.
  - Os guardiões são sempre 6 por nível (54 lutas nos níveis 4 a 12): Piromante 39% → 33%, ou seja, 21 vitórias
    contra 18. Está dentro do ruído, e os heróis também mudam, porque o sorteio dos talentos tem uma opção a mais.
  - Antes de o robô aprender a Prisão, ele a usava como ataque principal (a mais cara), e os guardiões levavam até
    o dobro de turnos para cair. É o erro de uso que a seção 14 pede para observar.
- `tests.replay` (a partida padrão e a do Piromante): **idênticos**. As partidas gravadas não compram o talento.
- O gabarito mudou só pelo esperado:
  - nas partidas sem Mago, a linha do glossário de cores ganhou "Prisão de Gelo";
  - nas do Mago, a divergência começa no nó novo da árvore, porque o robô sorteia com uma opção a mais. Nenhuma das
    partidas do gabarito comprou ou usou a Prisão.

## 14. O que depende de Jean jogar

**Nada abaixo foi validado pelo robô:**

- **A sensação de usar a Prisão contra o Esqueleto de Guarda.** Ela é a resposta certa ou só mais um botão?
- **Golem e cavaleiro sombrio sozinhos.** A Prisão repetida deixa a luta segura demais? É o principal ponto da seção 13.
- **A compra.** O talento já ativa a Prisão. Isso é o que se espera, ou a Lança sumir do menu surpreende?
- **A troca no Grimório.** O botão "Levar a …" é fácil de achar na vila e no acampamento? A página diz claramente onde
  trocar quando não dá?
- **A árvore.** A comparação no nó (custo, dano médio, chance de congelar) é suficiente para decidir a compra?
- **Usar a Prisão como ataque principal.** O robô fez isso antes de aprender. Uma pessoa também faria? (Ela custa
  mais e fere metade.)

**O cenário curto, para comparar as duas versões no mesmo herói** (mesmo equipamento e os outros talentos iguais):

```
CLASSE=mago NIVEL=4 ETAPA=ossuario PRISAO=prisao python -m tests.navegador.cenarios capela
CLASSE=mago NIVEL=4 ETAPA=ossuario PRISAO=lanca  python -m tests.navegador.cenarios capela
```

- Em cada um, desça ao ossuário. O Esqueleto de Guarda prepara o golpe no primeiro turno dele.
- Para ver a troca:
  - acrescente `LUGAR=vau_do_turvo` e abra o Grimório (P) na página da Prisão; o botão "Levar a Lança de Gelo"
    aparece;
  - ou, na capela, escolha "Acampar e descansar até o amanhecer" e troque na fogueira.
- No modo texto, a troca é a linha "Grimório: levar a …" do menu da vila e da fogueira.

