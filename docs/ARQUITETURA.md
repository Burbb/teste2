# Arquitetura

Como o motor de *Crônicas da Fenda* funciona e onde cada coisa mora. Para criar conteúdo, veja
[COMO_CRIAR.md](COMO_CRIAR.md); para o que vem pela frente, [ROADMAP.md](ROADMAP.md).

## A ideia central: o motor fala, a tela desenha

O jogo é um programa Python (só biblioteca padrão) que **não sabe** se está num terminal ou num navegador.
Ele chama uma interface (`ui`) com pedidos de alto nível: `cena`, `dizer`, `escolher`, `painel`, `lance`,
`celebrar`. Há três interfaces:

| Interface | Arquivo | Para quê |
|---|---|---|
| Web (principal) | `rpg/web/ponte.py` + `rpg/web/static/` | cada pedido vira uma mensagem JSON (SSE) que a página anima |
| Terminal | `rpg/ui.py`, `rpg/tui.py` | texto colorido, menus numerados |
| Robô | `rpg/ui.py` (`BotUI`) | joga sozinho nos testes, simulações e no gabarito |

Quando o jeito de mostrar muda de uma interface para outra, o motor não pergunta "é a web?". Ele pergunta o
que a interface **sabe fazer** (atributos em `UI`: `hud`, `letras_nos_alvos`, `analisar_no_menu`,
`numerar_destinos`, `fogueira_sozinho`, `bolsa_clicavel`, `conversa_no_painel`, `conquistas_na_tela`,
`surpresa_na_tela`) ou entrega o conteúdo e deixa ela mostrar
(`desenhar_mapa`, `mostrar_talentos`, `talento_aprendido`, `reacao_animal`, `boas_vindas`). `efeito(texto, tipo,
item=)` leva o id do que se ganhou (a tela manda o ícone até onde ele mora) e `continuar()` é um Continuar de
verdade, onde a pausa normal viraria a página sozinha (o fim do prólogo). A classe `UI` faz do
jeito do texto; o mixin `InterfaceGrafica` faz do jeito gráfico e é usado pela `WebUI` e pelo robô do gabarito
quando imita a tela web. Uma interface nova (celular, outra tela) escolhe as capacidades, sem tocar no motor.

Regra: **a regra do jogo mora no motor**, a tela só desenha. Quando a tela precisa de um número (dano de uma
habilidade, preço, chance), ele vem pronto do motor (metadados das opções ou `rpg/web/estado.py`).

## O laço do jogo

`Jogo` (`rpg/jogo.py`) junta os sistemas (mixins em `rpg/sistemas/`): navegação, contratos, loja, inventário,
progressão, tempo, confronto, testes de atributo, recompensas, bestiário, persistência. O laço é:

```
tela() → menu do lugar (vila ou região) → ação → (viagem, evento, combate, mercado...) → tela()
```

Eventos (`rpg/eventos/`) são funções registradas com `@evento(contextos, peso, cooldown, cond)`; o motor
sorteia entre os que valem para o contexto.

## Combate

`Combate` (pacote `rpg/combate/`) roda turnos: sua ação → aliados (comitiva, animal, servos) → inimigos. A classe
junta partes por responsabilidade, como o `Jogo` junta os sistemas: `luta.py` (quem está na luta, o laço, os lances,
o fim), `golpe.py` (a conta de um golpe, os estados que ele deixa, as mortes), `heroi.py` (a sua vez), `turnos.py` (a
vez da comitiva, do animal, dos servos e dos inimigos) e `eficacia.py` (traços e resistências). Quem usa importa do
pacote: `from rpg.combate import Combate`.

- `atacar()` é **a** conta de dano (esquiva, eficácia, modificadores, defesa, crítico, barreira, roubo de vida).
- **Piso de vida** (`Inimigo.piso`, `retido`, `ao_limiar` em `entidades.py`): com piso, nenhuma atribuição a `hp`
  (golpe, vários golpes, efeito periódico, comitiva, servo, espinhos, execução) a leva abaixo dele; o excesso fica em
  `retido`. `Combate.checar_limiares` chama `ao_limiar` uma vez, no primeiro ponto seguro (depois da sua vez, da vez
  dos aliados, e antes de cada inimigo agir). Hoje só o rito da guardiã do Turvo usa (`missoes._momento_do_rito`):
  dar descanso encerra a luta; desistir tira o piso e o retido cai na hora. Sem piso, nada muda.
- `Chefes.receber_sigilo` é a recompensa de progressão de um guardião (Sigilo, reputação, ponto de talento, festa),
  usada pelo covil e pela guardiã da campanha; `itens.fazer_unico` monta um único do catálogo pelo id.
- Cada coisa visível vira um **lance** estruturado (`acao`, `golpe`, `erro`, `cura`, `buff`, `salva`, `fim_acao`...)
  que a tela anima (`rpg/web/static/batalha.js`) e a telemetria contabiliza.
- O espólio da vitória (ouro, XP, contratos que andaram, o que se acha nos corpos, e o que o evento ainda der logo
  depois) é juntado pelo motor (`Recompensas.abrir_espolio`/`fechar_espolio`): na tela gráfica vira um quadro só,
  mostrado antes da próxima pergunta ao jogador ou no fim do evento; no texto, cada ganho é dito na hora.
  O mesmo quadro abre um baú (`abrir_espolio(titulo="baú aberto")`). Com vários na bolsa, a pilha abre inteira
  (`Inventario.abrir_baus`): cada baú com o próprio sorteio (`sortear_bau`, o mesmo de um baú sozinho, na mesma ordem),
  um quadro só ("Baús ×N", com `baus` e a lista `equipamentos`) e depois a janela de cada equipamento.
- Saque (`Confronto.saque_de_combate`, números `SAQUE_*` e `BAU_*` em `balanceamento.py`): luta comum dá
  equipamento mais vezes, mas quase sempre comum; o raro vem de elite, guardião e baú. O Baú Trancado é um
  consumível da bolsa que só abre em lugar seguro (`Inventario.lugar_seguro`: numa vila ou com `na_fogueira`, que
  `comitiva.fogueira` liga enquanto a cena da fogueira está aberta).
- Estados (veneno, queimadura, guarda, provocando...) ficam em `efeitos` de cada combatente. O **catálogo**
  `rpg/estados.py` (Etapa C) declara, para cada um: nome, ícone e cor na tela, se é um mal, dano por turno,
  perda de turno, imunidade, resistência, camadas e como o Grimório o descreve. `aplicar()` e
  `processar_efeitos()` são genéricos: só leem o catálogo. A tela recebe ícones e dicas pelo estado (`"estados"`)
  e, em cada carta, a frase do agora com o número (`agora`: "+60% de dano por 2 turnos", não "causa mais dano").
- Acúmulo de bônus, como nos jogos do gênero: **a mesma fonte renova** (aplicar o mesmo estado de novo fica com o
  maior valor e o maior prazo) e **fontes diferentes somam lado a lado**, cada uma com o seu estado (`fortalecido`
  do Grito de Guerra, `furia` da Fúria Cega, `frenesi` do talento): cada uma multiplica o dano na sua vez. Bônus novo
  de outra fonte é um estado novo, nunca o valor de um que já existe.
- A iniciativa (emboscada a favor) é o estado `iniciativa` do herói: o primeiro golpe do turno sai mais forte e o
  estado some no fim do primeiro turno. A tela vê o lance `surpresa` (as cartas pegas de surpresa tremem).

### Habilidades: dados, não código (Etapa A)

`rpg/habilidades.py` tem o catálogo. Cada habilidade é uma ficha + uma lista de **passos** (blocos):

```python
"sede_sangue": hab("Sede de Sangue", 12, "inimigo", "140% de dano, rouba vida e causa sangramento.", [
    Dano(1.4, rotulo="Sede de Sangue", depois=[
        Se("acertou", Roubo(0.4, rotulo="Sede de Sangue"),
           Aplicar("sangramento", 3, valor=Escala(minimo=2, atk=0.3)),
           Dizer("Você bebe a fúria do golpe. (+{cura} vida)", "verde", se="cura"))])]),
```

Cada bloco sabe **executar** (na luta) e **se descrever** (no Grimório). O número existe num lugar só.
Habilidades muito particulares (Redemoinho, Ordem da Fera, Combustão, Execução, Meditar, Barreira, Erguer
Servo, Fúria Cega) usam `fn` + `linhas` escritas à mão, lado a lado no mesmo arquivo.

### Talentos e passivas: modificadores e gatilhos (Etapa B)

Ninguém no combate pergunta "você tem o talento X?". Perguntam por **chaves**:

```python
m *= 1 + mod(u, "dano_corpo")              # Golpe Brutal (e qualquer fonte futura de dano corpo a corpo)
disparar(self, j, "abate", alvo=c, tipo=tipo)   # Frenesi, Assassino, Coração Ardente...
```

`rpg/modificadores.py` junta as **fontes** de um combatente (a passiva da especialização e os talentos comprados) e
responde. Cada talento declara `mods`, `mults` e `gatilhos` ao lado da própria definição em `rpg/talentos.py`.
Itens ainda usam `especial()` (crítico, roubo de vida, espinhos) e entram como fonte numa etapa futura.

O **Grimório** (`rpg/grimorio.py`) monta o livro a partir dessas descrições (e o modo texto mostra o mesmo, em
`grimorio.texto`), e é também onde mora a conta de
crítico (`chance_critico`, `mult_critico`) que o combate, a ficha e o livro usam.

## Dados e números

| Onde | O quê |
|---|---|
| `rpg/balanceamento.py` | todos os números de dificuldade e generosidade, inclusive a curva por nível (inimigos, equipamento, XP, defesa) |
| `rpg/dev.py` | herói de nível N com equipamento de acordo (`--dev N` e o simulador de equilíbrio) |
| `rpg/classes.py` | classes, especializações (com os `limites` que a escolha mostra), animais do Patrulheiro |
| `rpg/especializacao.py` | aplicar uma especialização (`aplicar_bonus`, o animal) e a prévia da escolha: os números de cada caminho são a conta feita numa cópia do herói (`copia_especializada`), com o que dá, os limites e os talentos; a mesma página entra no Grimório (`pagina_grimorio`) |
| `rpg/missoes.py` | missões da campanha escrita: id estável, etapas (objetivo e lugar), pistas; as cenas e ações declaram lugar e etapa e só valem no menu do lugar (`cena_pendente`, `opcoes`, `executar`); `confirmar` faz o texto terminar num Continuar explícito (`ui.continuar(confirmar=True)`, a mensagem `continuar` leva `confirmar`); uma ação pode pedir classe, um preparo que falte e uma condição. A masmorra é uma sequência de ações no menu do lugar (uma sala por etapa; só a vitória avança), sem mapa interno. O estado vai em `mundo.missoes` (`etapa`, `cenas`, `pistas` = o que se sabe, `preparos` = o que se fez ou se tem, `desfecho` = o fim único da guardiã, `dia_desfecho`, `concluida` = o dia em que terminou; concluída, sai do rastreador e do mapa e fica no Diário; `historico` = o que cada ação ou cena mudou, com o dia, desde a 1.60). Depois de cada ação ou cena, `anotar_novidades` compara a missão com o retrato de antes, anota o histórico e manda um cartão só (`ui.missao_atualizada`: o que se descobriu ou fez, pelos `titulos` curtos, e o objetivo novo); carregar um save não passa por aí. Uma ação pode abrir uma escolha interna e voltar sem efeito (a função devolve `False`: sem Continuar). No Diário, `cartoes` dá `recente`, `historico` (sem data o que um save antigo já sabia) e `aguardando` |
| `rpg/caspar.py` | a segunda missão do Vale do Turvo, "A Vigília de Caspar" (E4), nos mesmos moldes (MISSOES, CENAS, ACOES, que `missoes.py` junta às dela no fim): a acusação na investigação, a praça depois da guardiã, a prova (o lodo e o canal; a análise do mago ou as ervas da Yara), as posturas (`desfecho`: apoiar, denunciado, denuncia_falhou, calar), a situação da Yara, a frase da praça e a fogueira do brejo (`fogueira_possivel`). Os cartões das missões declaram `requisitos`, `linhas`, `pendente` e `aguardando` (a resposta a Caspar espera a febre) |
| `rpg/consequencias.py` | consequências locais da campanha (E4): o estado da Fonte Nova pelo desfecho e pelos dias desde ele (`estado_fonte`), quem atende na curandeira do Vau (`atendente`: Pita, ou Marta depois que a água limpa), a frase do Vau (`frase_da_vila`) e a linha da Fonte no Diário. Nada de simulação: dois números da missão e `g.dia` |
| `rpg/campanha.py` | a campanha escrita (protótipo): regiões de mapa fixo no mesmo formato do mundo gerado (`chave` estável, `nivel` fixo, saída `fechado`), e os eventos do mundo gerado que ficam de fora (`EVENTOS_FORA`) |
| `rpg/habilidades.py` | habilidades (execução + descrição) |
| `rpg/talentos.py` | árvores de talentos e passivas de especialização, cada um declarando o próprio efeito |
| `rpg/estados.py` | catálogo de estados (veneno, guarda, atordoado...): regras, tela e descrição |
| `rpg/modificadores.py` | `mod`/`mult`/`disparar`: como talentos e passivas mudam o jogo (as chaves e eventos válidos) |
| `rpg/inimigos.py`, `rpg/dados.py` | famílias de inimigos, biomas, climas, traços |
| `rpg/itens.py` | consumíveis, equipamento, afixos, únicos |
| `rpg/comitiva/` | companheiros: `catalogo` (quem são, reações), `grupo` (entrar, sair, aprovação; `junto`/`fora`: quem anda com você mas não está aqui, por regras em `AUSENCIAS` que a campanha registra), `conversas` (a história de cada um e as `avulsas`, de uma vez só), `luta` (a ação de cada um em `ACOES`), `fogueira`, `tela` |

## Saves

`rpg/sistemas/persistencia.py` grava JSON (a campanha escrita grava como `<região>_<nome>.json` e leva `mundo.campanha`; sem esse campo, é o mundo gerado. Save da campanha sem `mundo.missoes`, de antes da 1.50, ganha a missão na primeira etapa ao carregar: `campanha.ajustar_save`); `rpg/migracoes.py` leva saves antigos para a versão atual
(`VERSAO_SAVE`). Toda mudança de formato ganha uma migração.

## A interface web

`rpg/web/servidor.py` (HTTP + SSE em 127.0.0.1, com token) → `rpg/web/static/`:

- `app/nucleo.js` conexão e fila de mensagens · `app/pagina.js` texto e cenas · `app/escolhas.js` menus,
  doca de atalhos, roda de ações da luta · `app/paineis.js` ficha e mapa laterais · `app/controles.js` teclado
- `app/vila.js` a vila como lugar: os serviços moram nos prédios da paisagem. O motor marca cada opção da vila com
  `predio` (e `curto`, `tempo`) e diz, no estado (`local.predios_fechados`), por que um prédio está sem serviço
  agora; `vista.js` desenha os prédios e registra a área de cada um e o ponto do balão (`Vista.predios()`), acende as
  luzes do que está sob o mouse (`destacar`) e leva a câmera ao escolhido (`focar`: troca de enquadramento num
  pontilhado, sempre em pixel inteiro); `vila.js` põe os botões e os balões de nome por cima e toca o som do prédio.
  Diante da taverna e do templo, o balcão mostra os serviços em cartões (o motor marca cada opção com `servico`,
  `curto`, `preco`, `efeito`, `tempo`), ou o porquê de estar fechado; a forja e a curandeira são telas desenhadas
  como o mercado (`painel` "ferreiro" e "curandeira", com `reforcar` e `tratar` nas opções). O que não é de prédio
  (passear) fica em texto.
- A paisagem (`vista.js`) compõe a arte em 320×72 e a desenha no canvas já no tamanho em que aparece, pixel a pixel
  da tela (o enquadramento vem do CSS: `object-fit`, `object-position`). Deixar o navegador esticar numa escala
  quebrada fazia colunas da arte parada tremerem de um quadro para o outro.
- O fim de um evento ou de uma luta não pede Continuar: a ponte manda a cena do lugar com `virar`, a tela deixa o
  que aconteceu o tempo de ler (um fio se enche; clique ou tecla adianta) e vira para a página limpa do lugar, no
  topo. Vale também para o evento que termina sem escolha nenhuma (o "Exausto", a noite no acampamento): o
  `pausar()` do motor marca a página como lida-antes-de-seguir. O que aconteceu fica no histórico (H). O clique que adiantava o texto não pula a leitura nem as celebrações
  (contrato pago, espólio): a página só aceita virar depois de `GUARDA_LEITURA`, e celebração só se dispensa na
  velocidade "instantâneo".
- `telas/` as telas desenhadas, uma por arquivo (inventário, mercado, talentos, Grimório, fogueira, mural...), mais as
  dicas, os menus de item e as celebrações. `base.js` cria o nome `Telas` e o painel: cada tela se registra com o tipo
  que o motor manda (`Telas.registrar("loja", loja, { ligar, esquecer })`), e o painel acha a tela pelo tipo. Cada
  arquivo tira de `Telas` o que usa dos outros (`const { h, S, dica } = Telas;`, no começo) e põe o que oferece
  (`Object.assign(Telas, {...})`, no fim); a ordem dos `<script>` no `index.html` é a das dependências. Pedir a
  `Telas` um nome que ninguém pôs é erro na hora, com o nome. Tela nova: um arquivo em `telas/`, o `registrar` no fim
  e o `<script>` antes de quem a usa.
- `batalha.js` o palco da luta (o jeito de animar vem do motor: `anim` nos lances). A arena só cresce durante a luta e cresce devagar; quando uma carta entra ou ganha a linha de efeitos, as outras deslizam até o lugar novo (`acomodar`, desvio em `top`/`left` e em pixel inteiro: `transform` e `translate` são do foco e dos golpes) · `realce.js` cores dos termos de
  jogo (os nomes de habilidades e talentos chegam do motor no `glossario` do estado) · `sprites*.js`, `vista.js`, `mapa.js`, `som.js`
- `sensacao.js` o peso dos momentos (parada no impacto, tremor, câmera lenta no golpe final...): as telas dizem o
  que aconteceu e perguntam a ele como aquilo se sente; os números ficam numa tabela só (`AJUSTES`). Os fatos vêm
  do motor (no lance do golpe: `crit`, `abate`, `final`). A câmera lenta mexe no relógio da arena: prazos de
  animação na batalha usam `Sensacao.depois(ms, fn)` (não `setTimeout`), para andarem no mesmo ritmo.
- A coluna do meio: HUD, a **cena** e a doca. A cena (`#cena`) tem três andares: a arte do lugar (`#vista`, presa
  no topo; recolhe numa faixa quando o texto passa a rolar), a barra das telas de menu (`#barra-tela`: título e
  Voltar, fora da área que rola) e a página (`#pagina`, a única parte que rola). Cena de tipo `menu` (mercado,
  inventário, mural...) não mostra a arte, abre no topo e leva o Voltar para a barra; numa cena da história um
  "Voltar por onde veio" é uma escolha como as outras. Na luta, a arte vira o chão da arena e depois volta; a
  arena e o log ficam num painel só (o quadro se abre entre os dois e o chão continua pontilhado no log).
- O histórico (H) é o diário da jornada: entram as cenas da história, as escolhas e o que elas deram. Navegação
  (Voltar, telas da doca, menu do título), cliques da luta e títulos de telas de menu ficam de fora; o nome do
  lugar só volta quando o lugar muda.
- Perguntas que moram numa janela por cima, e não no pé da página, vêm marcadas nos metadados das opções: a
  confirmação de algo pedido pela tela (`Jogo.confirmar`: abandonar contrato, viagem perigosa) e o item achado
  (`achado`: o cartão e os botões numa janela própria, fora do log)
- `css/01..13-*.css` por componente. A identidade é pixel art em paleta indexada (a dos sprites, publicada por
  `Sprites.publicar()` como `--p-<letra>`): toda caixa é um dos materiais de `01-base.css` (`m-painel`, `m-janela`,
  `m-placa`, `m-nicho`, `m-sulco`, `m-etiqueta`): os painéis num quadro de bronze com rebites (`quadro_j`), o resto
  com um anel só, de 1 texel (`--P`) e canto chanfrado. Pedra, pergaminho, fuligem e luz são ladrilhos pontilhados
  gerados em `sprites.js`; nada de gradiente liso, desfoque, canto redondo ou cor translúcida
  (`tests/test_estilo_pixel.py` trava isso, arquivo por arquivo). Títulos em Alagard (`fontes/alagard-pt.ttf`, com os
  acentos desenhados por `ferramentas/acentuar_alagard.py`), em múltiplos de 16 px de arte; interface, números e prosa
  em Alegreya ("Fonte: pixel" troca só a prosa, para Pixelify Sans).

## Telemetria

`rpg/telemetria.py` registra a partida em `<saves>/runs/` (um `.jsonl` completo e um `.md` legível; reler um registro:
`python -m rpg.telemetria arquivo.jsonl`). A versão 3 do registro mede a escala de poder do meio e do fim de jogo:
de onde vem cada atributo a cada nível (base, equipamento, talentos, eventos) e a força do equipamento; em cada
luta, o tipo de encontro (comum, elite, campeões, único, chefe), se era noite, a vida mínima e o dano por
habilidade; o ouro por fonte (`ganhar_ouro(fonte=)`) e por destino (`perder_ouro(destino=)`); baús e atributos
ganhos em eventos. O resumo traz as tabelas "De onde vem o poder", "Ritmo das lutas" (dano por turno dos dois
lados, turnos até cair) e "Encontros por tipo".

## Rede de segurança

| Teste | O que garante |
|---|---|
| `python -m tests.gabarito` | 24 partidas com sementes fixas saem **idênticas** (refatorar não muda o jogo): 18 partidas do robô e 6 sequências de lutas com a comitiva. Nas 9 partidas da tela gráfica, cada escolha anota também o `estado` que a tela recebe (linhas `ESTADO parte {...}`, só quando a parte mudou) e cada árvore de talentos aberta (`ARVORE {...}`) |
| `python -m unittest discover -s tests` | sistemas, saves antigos, catálogo de habilidades, Grimório, gabarito |
| `python -m unittest tests.test_conteudo` | o validador de conteúdo: toda referência entre catálogos existe (habilidades de famílias, afixos e fases de guardião; famílias dos biomas; traços; lore; títulos e reações da comitiva apontando para eventos; ícones de habilidade, talento, item e traço com desenho; cor, animação e realce de cada habilidade entre os que a tela sabe fazer) |
| `tests/navegador/fumaca.mjs` | a interface web de ponta a ponta (Playwright) |
| `python -m tests.equilibrio` | não é teste, é régua: heróis típicos por especialização e nível lutando (`tests/arena.py`) |
| `python -m tests.replay` | régua humana: as partidas de `tests/runs/` refeitas com os números de agora |

Mudou o jogo de propósito? `python -m tests.gabarito --atualizar` e diga no commit o que mudou.
