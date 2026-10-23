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
  dar descanso encerra a luta; desistir tira o piso e o retido cai na hora. Sem piso, nada muda. `ao_vencer`, se o
  inimigo vencido tiver, roda na vitória antes da faixa (só mostra: a resolução de Ilse entra na arte com ela ali).
- `Chefes.receber_sigilo` é a recompensa de progressão de um guardião (Sigilo, reputação, ponto de talento, festa),
  usada pelo covil e pela guardiã da campanha; `itens.fazer_unico` monta um único do catálogo pelo id.
- Cada coisa visível vira um **lance** estruturado (`acao`, `golpe`, `erro`, `cura`, `buff`, `salva`, `fim_acao`...)
  que a tela anima (`rpg/web/static/batalha.js`) e a telemetria contabiliza.
  Os lances não levam o estado: a ponte o manda junto dos textos e de `ui.atualizar()`. Por isso, quando o motor
  muda algo que a tela precisa ver antes da animação seguinte (o custo de uma habilidade, a flecha do ataque),
  ele chama `ui.atualizar()` logo depois (1.114.1: o recurso pago chega antes do lance `acao`).
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
  O ícone de um estado é o sprite que o catálogo dá; um estado com desenho próprio na família (`Icones.estado`, papel
  `ESTADO` em `icones.js`) usa o arquivo no chip da carta e no selo do estado que chega: desde a 1.155.0, o Firme (a
  corrente rompida, `estado-firme-16.png`), enquanto o sprite `cadeado` fica nos outros papéis; desde a 1.156.0, o Em
  guarda (o escudo de ferro, `estado-guarda-16.png`), enquanto o sprite `escudo` fica no Erguer Escudo, nos talentos e
  no espaço vazio; desde a 1.157.0, a Esquiva (a figura em movimento, `estado-esquiva-16.png`), enquanto o sprite
  `folha` fica na Fúria da Natureza, no Pés Leves, no Antídoto e na Agilidade das celebrações; desde a 1.158.0, o
  Sangramento (`estado-sangramento-16.png`), a Maldição (`estado-maldito-16.png`), o Marcado (`estado-marcado-16.png`),
  o Furtivo (`estado-furtivo-16.png`) e a Fúria (`estado-furia-16.png`), enquanto os sprites `gota`, `gota_roxa`,
  `flecha`, `olho` e `machado` ficam nas habilidades, nos talentos, nos ferimentos e nos outros usos; desde a 1.159.0,
  as Chamas (`estado-queimadura-16.png`), o Fortalecido (`estado-fortalecido-16.png`), o Enfraquecido
  (`estado-enfraquecido-16.png`) e o Frenesi (`estado-frenesi-16.png`), enquanto os sprites `chama`, `espada`, `osso` e
  `raio` ficam nos outros usos; desde a 1.160.0, o Veneno (`estado-veneno-16.png`, a gota verde), o Atordoado
  (`estado-atordoado-16.png`, as três estrelinhas, também no congelado) e a Barreira (`estado-barreira-16.png`, o golpe
  na película), enquanto os sprites `gota_verde`, `estrela` e `escudo_azul` ficam nos outros usos. desde a
  1.161.0, o Provocando (`estado-provocando-16.png`, a figura branca com as setas convergindo) e a Iniciativa
  (`estado-iniciativa-16.png`, a exclamação de barra larga), enquanto a `caveira` e a `bota` ficam nos outros usos. Os
  17 estados do catálogo (`rpg/estados.py`) têm ícone próprio desde a 1.161.0. A flecha ao lado da
  quantidade de flechas na carta do Arqueiro também tem papel próprio (`Icones.contadorFlechas`, 1.155.0); o sprite
  `flecha` fica no custo das habilidades, na orientação, no elemento "à distância" e nos projéteis.
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

Uma **variante** (E6, a Prisão de Gelo) é outra ficha para uma habilidade que o herói já tem: mora em `VARIANTES`,
fora do catálogo aprendível, e um talento a libera (`transforma`). Cada herói resolve a sua ficha com
`efetiva(u, h_id)`; o menu da luta, o custo, o Grimório, a tela e a execução passam por ela, e o catálogo nunca muda.
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
| `rpg/missoes.py` | missões da campanha escrita: id estável, etapas (objetivo e lugar; o objetivo pode ser uma função do jogo, lida por `objetivo(g, mid, etapa)`, quando o texto depende do que o personagem sabe), pistas; as cenas e ações declaram lugar e etapa e só valem no menu do lugar (`cena_pendente`, `opcoes`, `executar`); `confirmar` faz o texto terminar num Continuar explícito (`ui.continuar(confirmar=True)`, a mensagem `continuar` leva `confirmar`); uma ação pode pedir classe, um preparo que falte e uma condição. A masmorra é uma sequência de ações no menu do lugar (uma sala por etapa; só a vitória avança), sem mapa interno. O estado vai em `mundo.missoes` (`etapa`, `cenas`, `pistas` = o que se sabe, `preparos` = o que se fez ou se tem, `desfecho` = o fim único da guardiã, `dia_desfecho`, `concluida` = o dia em que terminou; concluída, sai do rastreador e do mapa e fica no Diário; `historico` = o que cada ação ou cena mudou, com o dia, desde a 1.60). Depois de cada ação ou cena, `anotar_novidades` compara a missão com o retrato de antes, anota o histórico e manda um cartão só (`ui.missao_atualizada`: o que se descobriu ou fez, pelos `titulos` curtos, e o objetivo novo); carregar um save não passa por aí. Uma ação pode abrir uma escolha interna e voltar sem efeito (a função devolve `False`: sem Continuar); uma opção de menu pode levar `nota` na meta (custo e risco: a tela mostra embaixo da ação, o texto junta depois de um travessão) e `abre` (leva a outra escolha, de onde se volta: seta na tela, "›" no texto). Meta `indisponivel` (o motivo): a opção aparece mas não se escolhe; `Jogo.custo_item` monta a nota do consumível que ela gasta, ou a indisponível sem ele. Uma ação de missão declara `abre` e `avanca` (o passo adiante fica por último entre as da missão); a tela agrupa o menu do lugar em Missão, Contratos e o de sempre. O que o Diário mostra segue o que o personagem sabe: o rito só depois de Vó Berta (`sabe_do_rito`), e antes disso as `perguntas` da missão. No Diário, `cartoes` dá `recente`, `historico` (sem data o que um save antigo já sabia) e `aguardando` |
| `rpg/caspar.py` | a segunda missão do Vale do Turvo, "A Vigília de Caspar" (E4), nos mesmos moldes (MISSOES, CENAS, ACOES, que `missoes.py` junta às dela no fim): a acusação na investigação, a praça depois da guardiã, a prova (o lodo e o canal; a análise do mago ou as ervas da Yara), as posturas (`desfecho`: apoiar, denunciado, denuncia_falhou, calar), a situação da Yara, a frase da praça e a fogueira do brejo (`fogueira_possivel`). Os cartões das missões declaram `requisitos`, `linhas`, `pendente` e `aguardando` (a resposta a Caspar espera a febre) |
| `rpg/consequencias.py` | consequências locais da campanha (E4): o estado da Fonte Nova pelo desfecho e pelos dias desde ele (`estado_fonte`), quem atende na curandeira do Vau (`atendente`: Pita, ou Marta depois que a água limpa), a frase do Vau (`frase_da_vila`) e a linha da Fonte no Diário. Nada de simulação: dois números da missão e `g.dia` |
| `rpg/abertura.py` | a abertura guiada da campanha (E9, roadmapIDEIAS/18): a despensa da taverna do Vau (dois ratos da despensa, uma luta curta, sem ouro nem saque: `combate(..., saque=False)`), a caneca por conta da casa (uma vez o serviço de bebida e rumores, sem pagar), a ação "sentar com o homem do canto" (o evento `morel_na_taverna` pelo motor de eventos, `eventos.disparar_id`, só enquanto ele nunca apareceu e está livre) e as orientações que a caixa "Mostrar tutorial" liga: a sequência da primeira luta (C1–C4: o motor manda os textos, pelas regras da classe; a tela avança pelos passos) e o Mural (V1). O estado vai em `mundo.abertura` (`tutorial`, `despensa`, `caneca`, `vistas`, `lutas_sem_habilidade`); o que se marca como visto não depende da caixa, então o jogo é o mesmo com ela ligada ou não. `para_tela` dá `estado["orientacao"]` (a de agora, as da apresentação que ainda valem, `apresentacao`: revelar o texto e acelerar a animação, cuja ocasião a tela acha, as `contextuais`, que a tela mostra quando o alvo aparece, como o cartão Dormir da taverna, e a Ajuda). Ali também mora `curandeira_gratis` (o primeiro tratamento de ferimento, grátis, uma vez, na campanha); o que um descanso devolve vem de `Tempo.linhas_descanso` (as linhas do cartão Dormir e do quadro da fogueira, pela conta de `Tempo.descansar`, em `Tempo.previsao_descanso`); a tela desliga e religa por `POST /orientacao` |
| `rpg/capitulo.py` | o fim do primeiro capítulo (E9): a cena curta no Vau depois da febre e da resposta a Caspar, uma vez (registrada no fim de `missoes.CENAS`, guardada nas cenas vistas da Vigília), com uma frase do estado de agora para a Fonte, Ilse, Caspar e Yara; `para_tela` dá a linha "Primeiro capítulo concluído" ao rastreador (`estado["capitulo"]`) e ao Diário |
| Queda e resgate | `Derrota` leva a `causa` ("combate", "fome" ou "infeccao"). No combate, `Confronto.combate` levanta a derrota; a fome e a infecção que zeram a vida passam por `Finais.cair_sem_luta`: no hardcore e no mundo gerado, `fim_de_jogo`; na campanha com resgate, a queda fica pendente e `Tempo.novo_dia` a levanta depois do quadro do amanhecer. `Jogo.rodar` chama `resgate(causa)`; na campanha, `resgate_campanha` (Marta ou Pita, dois dias com refeição, fome, infecção e feridas abertas tratadas, `resgatando` impede queda dentro da queda) |
| Toques e proteção (interface) | O Continuar das cenas de missão tem uma guarda de leitura (escolhas.js: `mostrarContinuar`): toques dentro dela a estendem, e o botão fica apagado (`contido`) enquanto ela segura. As ações do acampamento tocadas enquanto a página ainda apresenta a anterior ficam guardadas (`acaoGuardada`, nucleo.js) e valem quando o menu volta |
| A bolsa e o que trata | `Inventario.o_que_trata` diz o que um item trata agora (`trata`: a bandagem, a ferida que ela vai enfaixar, `sobrevivencia.ferida_para_bandagem`); a bolsa do painel pulsa e mostra na dica (paineis.js); sem nada a tratar, o `motivo` apaga o espaço |
| Os dois anéis | Um anel tem dois espaços (`itens.espacos`: `anel1`, `anel2`, "Anel 1" e "Anel 2"). O item achado com algum anel vestido oferece um botão por espaço (`Inventario.rotulo_espaco`: "Substituir {anel} (Anel 1)" ou "Equipar no Anel 2 (vazio)") e manda `espacos` ao painel (cada espaço com o que tem); a escolha é sempre da pessoa. Da mochila: no texto, `escolher_espaco` pergunta qual substituir com os dois ocupados; na tela, o inventário e o mercado têm uma opção por espaço (`destino`) e `Telas.equiparDaMochila` usa o vazio ou abre o menu de qual substituir. A comparação (`itens.js`, `comparar`) mostra a troca com cada espaço |
| As condições do herói | `sobrevivencia.condicoes` monta a fome (texto, ícone, a dica do efeito de agora) para a linha embaixo das barras do topo (paineis.js), que tem sempre a mesma altura |
| A vida máxima bloqueada | `sobrevivencia.vida_bloqueio` (1.115.0): a vida saudável (`Jogador.totais`: base, talentos, equipamento), o limite de agora (`max_hp`, com os fatores de ferimentos e fome multiplicados e arredondados em `recalcular`), as fontes na ordem da conta (a perda de cada uma; a soma fecha com o bloqueado) e as frases da dica. Só lê. Vai no estado (`heroi.vida_bloqueio`, None sem bloqueio). A barra do herói mede a vida saudável, no topo (`paineis.js`, `barra(..., bloqueado)`) e na carta (`batalha.js`, `barra`, que troca o limite que o golpe e a cura trazem pela saudável), com o fim em hachura e a marca de limite (`02-hud.css`); o número é vida/saudável; a etiqueta "−N de vida máxima" fica na linha das condições, e o lugar da gota dos ferimentos é guardado sem ferimento, para as barras do topo terem sempre o mesmo comprimento. O motivo da poção no limite, o efeito do Templo e a linha "Em você" (`telas/menus.js`) dizem o limite pelo nome. As regras não mudam: a Curandeira (`curar_ferimento`) devolve a parte do ferimento também como vida; o ferimento que sara com descanso só libera a capacidade; a fome também, quando passa: no amanhecer ou na comida comprada ou achada (`dar_provisoes`, que recalcula na hora desde a 1.174.5; antes, a vida seguia bloqueada, já sem causa, até dormir) |
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
(`VERSAO_SAVE`). Toda mudança de formato ganha uma migração. Um nome de espécie ou de guardião que muda também (o save
guarda texto: o nome do guardião, os rumores, a descrição dos contratos): na 1.181.0, o ent jovem virou a árvore
desperta e o Ent Ancião, a Árvore Anciã; os ids ficam, e o v5 → v6 refaz esses textos pelo catálogo (o guardião pelo
id, `ficha_guardiao`; os contratos por `contratos.desc_caca` e `desc_alvo`, os mesmos que geram os novos).

## A interface web

`rpg/web/servidor.py` (HTTP + SSE em 127.0.0.1, com token) → `rpg/web/static/`:

- `app/nucleo.js` conexão e fila de mensagens (e o `Gesto`: um clique ou tecla só vale na tela em que começou; o segundo clique de um clique duplo e a tecla segurada não escolhem nada; os botões que só abrem e fecham uma janelinha na mesma tela, `data-alterna`, aceitam cliques seguidos, e a venda da mochila no mercado vai por uma fila pela peça, como a compra de suprimentos (ver `telas/mercado.js`, abaixo); as cartas ✉ da comitiva tocadas no meio de outra coisa esperam o próximo menu do lugar, na ordem dos cliques) · `app/pagina.js` texto e cenas · `app/escolhas.js` menus,
  doca de atalhos, roda de ações da luta · `app/paineis.js` ficha e mapa laterais · `app/controles.js` teclado
- `app/orientacao.js` as orientações da abertura guiada (abertura.py: C1–C4 na luta; fora dela, uma por vez pela
  `proxima`, com o contexto da tela que pede a sua: o item achado, a escolha do destino): acha o controle (a roda, a janelinha, a mira, a
  barra de recurso, o prédio do Mural), põe o contorno em volta, o quadro com a seta (na luta, parado numa faixa
  reservada abaixo da arena, ou acima das cartas se couber, para nunca cobrir cartas, ações nem texto; na vila, o V1
  numa faixa abaixo do cenário, sem cobrir o prédio; recalculado só quando o passo ou o tamanho da tela muda; o que mora
  nas colunas, no topo ou no Mural, encostado no controle, com a ponta da seta nele, acompanhando a rolagem; o ícone de
  efeito numa carta, com uma haste da seta até ele) e um véu leve só nas colunas laterais e na doca; tudo sem receber clique,
  menos os botões do quadro ("Entendi" no C4, que fecha só ele, e "Encerrar tutorial"). A Ajuda (topo, F1) lista o que já foi visto e liga ou desliga, pela rota `/orientacao`
  (fora da fila das perguntas). Uma caixa marcável pode ir junto de uma escolha (`caixa` na pergunta; a resposta vem
  como `{"i", "caixa"}`; no texto, `UI.ler_caixa` faz uma pergunta de sim ou não).
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
  quebrada fazia colunas da arte parada tremerem de um quadro para o outro. O que fica por cima da arte (os prédios
  da vila com a área de clique, o balão e a ponta; os pontos de uma cena, como os da capela; o clique no próprio
  cenário) usa a mesma conta do desenho, `Vista.caixaDaArte()`, e se refaz por `Vista.aoRedimensionar`, que dispara a
  cada mudança de tamanho do canvas, inclusive durante a animação da altura (1.93.2: antes, a vila calculava no evento
  `resize` da janela, ainda com a altura de antes, e os balões ficavam no lugar do tamanho anterior;
  `tests/navegador/redimensionar.mjs` confere). A superfície da leitura é a da cena inteira (`14-hud.css`), não só a
  da página: o pontilhado do chão, a faixa reservada pela orientação e qualquer vão entre a arte e o texto terminam
  nela.
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
  O mercado (`telas/mercado.js`) é a tela com abas: elas são só da tela (não falam com o motor); a tela ocupa a altura
  visível da página e só a lista da aba rola; a banca é uma faixa em cima (em qualquer largura), desenhada em canvas
  no estilo das paisagens, com vãos de mercadoria que aparecem conforme a largura. O que não se compra vem com o
  `motivo` do motor (`Loja.dados_loja`), desenhado na linha do motivo com o `cadeado` do jogo; desde a 1.180.0, o
  suprimento esgotado vem com `motivo_id` "esgotado" e ganha o ícone próprio (`Icones.motivo`, o papel `MOTIVO`: o
  caixote vazio, `motivo-esgotado-16.png`), e os outros motivos continuam no cadeado. Ver roadmapIDEIAS/19. Tentar o que não se compra (ou um serviço da forja, da
  curandeira, da taverna e do templo sem ouro: o motor manda `motivo` nos dados e nas metas, `Servicos.motivo_pagar`) é
  recusado na tela (`App.recusar`, pagina.js): o som de falha e um aviso só, preso ao controle, com o motivo do motor;
  clique, Enter e as teclas de número passam por ali, e a escolha não chega ao motor (nem tempo, nem sorteio).
  A cena interativa (`telas/cenas.js`, painel `cena`) troca a arte do topo por um ambiente desenhado
  (`Vista.usarAmbiente`: o mesmo canvas, a mesma câmera, o mesmo chão de arena na luta) e põe os pontos clicáveis numa
  camada por cima dela (`#pontos-cena`, como os prédios da vila); nada vai para o texto. Uma página nova sem painel de
  cena devolve a paisagem (`Cenas.virou`/`conferirPendente` em `tratar`). O motor manda o estado e,
  em cada ponto, a `acao` (a mesma meta de uma opção do menu: o clique só aproxima a câmera e escolhe aquela opção) ou
  o `estado` escrito. Mudança de estado se anima por uma celebração mandada depois de o motor gravar o resultado. Hoje
  há cinco, da Capela Afogada: o exterior, o salão alagado, a sacristia, o ossuário e o fundo (`missoes.cena_exterior`,
  `cena_salao`, `cena_sacristia`, `cena_ossuario`, `cena_fundo`; `mostrar_cena` escolhe o da página do lugar pela
  sala). Um ambiente pode ter momentos que o motor manda explícitos (a sacristia: `momento` entrada, luta, vitória,
  visita; `luz`; o fundo: descida, visita, luta, descanso, destruída, com `ilse`, `correntes` e `agua`, e os momentos de
  Ilse pela celebração `ilse`, logo depois do texto que os conta); a base
  do desenho recebe o painel (`base(W, d)`). Na luta, as figuras da sala continuam nela (1.90.0): cada inimigo que é
  uma figura da arte leva a `figura` (os dois da sacristia: `missoes.FIGURAS_SACRISTIA`), a carta dele a manda
  (`estado.combate`), e a cena desenha o vulto enquanto aquela carta está de pé, pela identidade, não pela posição nem
  pelo nome; caído, ele se desfaz no tempo da carta; fuga e derrota não o tiram (vale o último estado visto até a página
  virar). Ilse fica na água a luta inteira e só sai pelas cenas do desfecho; na mistura curta de uma troca de momento
  ela é desenhada por cima (`frente` do ambiente), para não sumir por baixo da base de antes. Um painel novo da mesma sala não recomeça a cena (no mesmo acontecimento
  a animação continua; nos outros, a base de antes some numa mistura curta). Um ponto pode ser só "de olhar"
  (aproxima e afasta, sem falar com o motor; o texto curto do que se vê vem do motor) ou "de ler" (`ler`: abre um
  livro aberto com o texto pronto do motor). De perto, nada da vista geral fica à vista; o destaque do F4, o do mouse
  e o do foco de teclado são separados. O canto de Ilse (`Som.canto`) é um canal só, decidido pela cena do fundo
  (`Som.gravarCanto` grava a mesma música offline; `tests/navegador/ouvir_canto.html` toca fora do jogo). O livro da
  sacristia abre por uma celebração (`livro`) que a ação de ler manda: a leitura é do motor, que registra a descoberta. O céu do exterior vem de
  `Vista.ceuDo`. Na capela, a sala em que se está (`missoes.sala_atual`) é separada da etapa: as passagens entre salas
  vencidas são opções do menu (`("capela", sala)`, meta `capela_ir`) e pontos da cena; cada ação da capela tem a sua
  sala (`onde`). Ver roadmapIDEIAS/20.
  A fogueira (1.98.0) também é uma cena do topo: o painel `acampamento` (o mesmo do motor, `comitiva.fogueira`) monta
  a cena em `telas/acampamento.js` (`Acampamento.montar`: o lugar ao fundo, o teso com o fogo, a luz e a roda, o
  barranco na frente) e a passa à `Vista.usarAmbiente`; `telas/fogueira.js` desenha embaixo só a frase, a instrução e
  quem vai e quem fica, e põe os pontos por cima da arte (`#acampamento-pontos`, um por companheiro e pelo animal,
  com o menu de sempre, `Telas.ligarFigurasComitiva`, e o "Dormir até o amanhecer" no canto). A tela é de menu para
  o motor e para a ponte (redesenha no lugar, sem Continuar); com `#cena.acampando`, a arte fica à vista e a barra do
  título sai, para o chão da cena descer em pontilhado direto até a leitura. O fundo vem do lugar: um entorno
  desenhado à mão pela chave que o motor manda nos dados (`lugar`; hoje só `capela_afogada`, a capela pequena no
  brejo, em `ENTORNOS`) ou, nos outros lugares, a própria paisagem (`Vista.paisagem`, o céu e as silhuetas do bioma,
  com nuvens e corvos; a chuva por cima, `Vista.chuva`). As vagas da roda são fixas (`HEROI`, `ATIVOS`, `RESERVA`,
  `FERA`); quem fica no acampamento senta na beira da luz. O animal do patrulheiro entra pela figura do tipo
  (`Icones.figuraAnimal`, o papel `FIGURA_ANIMAL`: desde a 1.170.0 o Lobo Cinzento deitado, `figura-lobo-16`;
  desde a 1.176.0 o Urso Pardo sentado e o Falcão Peregrino no toco, `figura-urso-16` e `figura-falcao-16`), senão
  pelo sprite (`fera`, `voador`), aquecido pela luz do fogo como os outros. O nome aparece só com o mouse, o foco do teclado ou o F4
  (o balão da HUD, junto do contorno dourado das salas da capela, `Cenas.cantos`), acomodado como se todos
  aparecessem juntos (`acomodarNomes`: sem cobrir rosto, fogo nem o Dormir). Com movimento reduzido, as chamas
  ficam paradas. A orientação do Dormir (D3) fica na faixa logo abaixo da cena, com a haste até o botão, como a dos
  prédios da vila.
- `turnos.js` (1.116.0) a iniciativa e a passagem dos turnos: o anúncio em faixa ("Turno N", "Iniciativa!" com o bônus
  real, "Emboscada!", e o turno que você perde por um estado com `perde_turno`, como atordoado ou preso na teia) e a placa com o
  turno de agora e a iniciativa enquanto vale ("usada"/"passou"). Só lê o motor: a mensagem `turno` (`ui.novo_turno`,
  uma vez por volta, no começo da sua vez; comitiva, animal e servos não a geram), `estado.combate.turno`, o lance
  `surpresa`, o estado `iniciativa` da sua carta e o golpe com `bonus_motivo`. Chamado por `paineis.aplicarEstado`,
  `pagina.turno` (refazendo a página, só a placa) e a fila de lances (`nucleo.js`). Camada fixa sem mouse. O anúncio
  (1.116.1) fica num lugar só, numa linha: no centro da arena, na borda de cima, acima das cartas e dos comandos; a
  placa, no pé da faixa dos comandos ou presa à borda de baixo da arena. Os dois se medem pelo layout (`offsetTop`),
  não pelo retângulo na tela, e por isso ficam parados enquanto a arena chega perto e treme no golpe final
  (`sensacao.js`) (`19-turnos.css`).
- `app/rolagem.js` (1.117.0) a rolagem dos testes de atributo: fora da luta, o grupo no centro de `#palco` (o palco
  escurece; o nome do teste e a dificuldade, o dado 2×, a tirinha em pincel com a conta e "precisa de N ou mais", a
  faixa de resultado: Sucesso inteira em marfim, Falha rasgada em carvão), que desce até a tirinha do texto antes da
  consequência, no tempo de sempre (950 ms + `ritmo(650)`). No texto instantâneo, refazendo a página e na luta, só a
  tirinha. Lê a mensagem `rolagem` (`Testes.teste`: `atributo, cd, d20, mod, total, sucesso` e `precisa`, o menor d20
  que passa, de `Testes.precisa_no_dado`) e as parcelas de `heroi.testes` (`20-rolagem.css`).
- Os testes de atributo na ficha (1.118.0): a linha "Testes do d20" embaixo dos atributos (`telas/inventario.js`,
  `testesHtml`), com a dica dos seis testes. Tudo vem de `heroi.testes` (`web/estado.py`, `explicar_testes`): o total
  de agora, as partes fixas (`Testes.partes_fixas_teste`: nível, atributo, classe), as da situação
  (`situacao_teste`: sem luz), o uso (`USO_TESTE`), a chance numa dificuldade típica (`chance_teste_media`) e o
  atributo de origem abaixo do normal. As dicas dos atributos dizem só a parte de cada um nos testes.
- `batalha.js` o palco da luta (o jeito de animar vem do motor: `anim` nos lances). Os avisos de passagem (números, faixas como o "AAARGH!", os selos dos estados) não moram nas cartas: nascem numa camada da página (`.avisos-luta`, 1.103.1), numa sombra do tamanho e no lugar da carta que os disparou, que a acompanha quadro a quadro; assim passam por cima da moldura do palco (que recorta o resto) e ficam dentro da janela. A sombra some com o último aviso e todas saem com a luta. A arena só cresce durante a luta e cresce devagar; quando uma carta entra ou ganha a linha de efeitos, as outras deslizam até o lugar novo (`acomodar`, desvio em `top`/`left` e em pixel inteiro: `transform` e `translate` são do foco e dos golpes). As áreas da arena (1.111.0) estão em "As lutas cheias", abaixo · `realce.js` cores dos termos de
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
- `css/01..13-*.css` por componente: a estrutura, os estados e as animações (os materiais vêm da HUD de ferro, no
  item seguinte, por cima). A base é pixel art em paleta indexada (a dos sprites, publicada por
  `Sprites.publicar()` como `--p-<letra>`): toda caixa é um dos materiais de `01-base.css` (`m-painel`, `m-janela`,
  `m-placa`, `m-nicho`, `m-sulco`, `m-etiqueta`): os painéis num quadro de bronze com rebites (`quadro_j`), o resto
  com um anel só, de 1 texel (`--P`) e canto chanfrado. Pedra, pergaminho, fuligem e luz são ladrilhos pontilhados
  gerados em `sprites.js`; nada de gradiente liso, desfoque, canto redondo ou cor translúcida
  (`tests/test_estilo_pixel.py` trava isso, arquivo por arquivo). Títulos em Alagard (`fontes/alagard-pt.ttf`, com os
  acentos desenhados por `ferramentas/acentuar_alagard.py`), em múltiplos de 16 px de arte; interface, números e prosa
  em Alegreya, a única fonte da prosa (a "Fonte: pixel" do topo saiu na 1.137.0).
- A HUD de ferro (1.89.0; o caminho até ela está em `ferramentas/prototipos/hud/`, que fica como histórico). Os
  materiais da interface por cima da estrutura de 01 a 13, em três folhas: `css/14-hud.css` (as três molduras
  principais da ficha, da coluna do centro e do mundo, as superfícies de carvão, o topo, a doca, os botões, a ficha, os
  espaços de item, a janela do achado), `15-hud-luta.css` (cartas, roda, mira) e `16-hud-telas.css` (janelas, menus,
  mercado e serviços, Diário, Talentos, avisos), mais `17-titulo.css` (1.93.1: o menu inicial aberto sobre a
  paisagem, sem a moldura do palco, o véu da página nem as placas das opções; só em `body.modo-titulo`) e
  `18-seletor-habilidades.css` (1.103.0 e 1.105.0, abaixo). As imagens moram em `static/hud/` (moldura, texturas, barras) e
  `static/hud/icones/` (a família de ícones, cada um no tamanho de uso e com o dobro). Toda regra começa por
  `:root body`, a mesma força de `body.<estado>`: é a que elas tinham no experimento, e vencem o material antigo sem
  depender de uma classe no corpo. Essas folhas ficam fora da trava de pixel (`FORA_DA_TRAVA`): o material é
  pintado, com véus translúcidos, relevo e sombra suaves. `Sprites.publicar()` pinta os anéis, bicos e fios da
  interface em ferro (as mesmas grades; o bronze continua nos sprites e, com `{ bronze: true }`, no protótipo).
- O seletor das ações da luta, Habilidades (1.103.0) e Itens (1.105.0) (o caminho, das propostas A, B e C à D
  refinada aprovada e ao menu de Itens em faixas, está em `ferramentas/prototipos/hud/LEIA-ME.md`). Um componente só, com material próprio (faixas de tinta, marfim, latão
  envelhecido) que não vale para outras telas. As peças, para reaproveitar se um dia outro seletor pedir o mesmo:
  - *onde mora:* `abrirJanela` em `app/escolhas.js` monta o seletor (`.roda-janela.seletor`) para os dois menus;
    `data-tipo` diz qual é ("habilidades" ou "itens"). O visual inteiro está em `css/18-seletor-habilidades.css`, com
    o que é só de Itens no fim; nada vem de `ferramentas/`;
  - *o menu de Itens:* a quantidade no lugar do custo ("×2"), na cor normal mesmo quando o item não serve (o motivo do
    motor fica escrito na faixa); a troca de arma é uma faixa com "turno" à direita e a ficha da arma na descrição;
    a poção que pode ir num aliado abre a mira dos aliados, como antes; sem nada que sirva, o seletor abre com "Nada
    na bolsa serve agora." no lugar das faixas. A descrição do consumível vem do motor (`itens.descricao`: o Tônico
    diz só o recurso da classe, pelo `artigo_recurso` de `classes.py`);
  - *composição:* `dispor` decide onde. Da largura da arena, colado embaixo dela, por cima do registro (posição
    absoluta na camada da roda: abrir e fechar não mexe nas cartas nem na rolagem), em duas colunas na ordem das
    teclas (`--filas`, `--fila`), quando cabem a lista inteira e 60 px de descrição; título pequeno e "Esc · Voltar"
    (o mesmo fechar). Senão (a luta cheia numa janela baixa; 1.114.0), sobre a coluna da ficha do herói
    (`.lateral`, fixo, logo depois de `#heroi` no DOM: o Tab segue para a arena), numa coluna só, com o custo numa
    linha própria embaixo do nome, o Voltar no título e a descrição embaixo; a ficha fica `inert` até ele fechar
    (`soltarFicha`; `limparRoda` o tira junto ao entrar na mira). Sem a ficha à vista (abaixo de 920 px), embaixo, e a
    lista rola dentro. Redimensionar dispõe de novo sem fechar (fechar o submenu de Itens responderia "Voltar" ao
    motor), com a mesma examinada (`_examinada`, `_mostrar`) e o mesmo foco;
  - *marcação:* a tecla, o ícone, o nome com o motivo da indisponível (o texto do motor) e o custo, cada um no seu
    elemento: a tradução troca só o texto; um nome longo quebra em duas linhas em vez de ser cortado;
  - *a faixa:* o `::before` de cada linha (a cor do estado, um grão de pincel em SVG fixo e um degradê de volume),
    recortado por uma máscara de três peças: as pontas, desenhadas em SVG e escaladas só pela altura (o desenho não
    estica com a largura), e o meio esticado entre elas. Três pontas de cada lado, combinadas pela posição
    (`li[data-forma]`, 0 a 2): a mesma borda a cada abertura. O desgaste fica nos ~12 px das pontas e nas beiradas,
    longe do texto, do ícone e do custo. Só o `::before` inclina (2°): texto, números e ícones ficam retos;
  - *fundo:* a superfície da leitura da página (os véus de `14-hud.css` e a textura de carvão, alinhada à da página
    por `--fundo-cena` e `--fundo-palco`), opaca, com um fio fino embaixo; `bordaLimpa` faz o seletor descer até o pé
    da linha do registro que a borda cortaria ao meio (e refaz a conta se o registro rolar), sem mexer no registro;
  - *estados:* normal carvão; examinada (mouse ou foco) marfim com texto escuro e a tecla em latão; foco do teclado
    com o fio de latão e o anel na tecla; pressionado afunda 2 px; indisponível cinza riscada, com nome, custo e
    motivo legíveis (o clique treme e avisa, como antes);
  - *teclado:* aberto pela tecla, já chega com o foco na primeira faixa; as setas andam (cima e baixo na ordem, os
    lados trocam de coluna); 1 a 9 escolhem; Esc fecha e devolve o foco ao botão; o foco mostra a prévia dos alvos;
    o botão Habilidades (e o Itens) alterna a cada clique, mesmo seguidos (`data-alterna`, ver o `Gesto`);
  - *descrição (1.104.0):* a habilidade examinada (mouse ou teclado) mostra, dentro do seletor e embaixo da coluna
    dela, o que a dica de antes mostrava (custo, alvo, o que faz, o dano, o motivo de não poder); uma por vez, e ela
    fica na última examinada. O lugar é reservado ao abrir, na altura da maior descrição (`descricoes`): trocar de
    habilidade não mexe em nada. Se por coluna não couber na janela, vira uma área só embaixo das duas colunas (e o
    "Esc · Voltar" sobe para a linha do título); se nem assim, a descrição rola dentro e as faixas ficam inteiras. A dica flutuante não abre nas faixas (continua nas outras telas);
  - *movimento:* as faixas entram de 12 px em 150 ms, 18 ms uma depois da outra, sem segurar os controles; com
    movimento reduzido, sem deslocamento.
  A conferência: `ferramentas/prototipos/hud/fotografar_seletor_d.mjs` com `VERSOES=atual RODADA=1` (as três classes
  com comitiva, o teste de 10 habilidades, as interações, a borda de baixo com o registro em várias rolagens) e
  `fotografar_itens_faixas.mjs` (o menu de Itens nas três classes, a bolsa vazia, a troca, a poção e a mira).
- Os comandos da luta (1.111.0) e as escolhas da página (1.111.0 no lugar selvagem, 1.113.0 em todas) na linguagem do
  seletor (o caminho em `ferramentas/prototipos/hud/LEIA-ME.md` e em `ferramentas/prototipos/hud/escolhas-faixas/`).
  As pontas e o meio das faixas são as mesmas peças do seletor, declaradas em `18-seletor-habilidades.css` para
  `.roda-janela.seletor`, `#roda` e `#prompt`:
  - *os comandos* (`15-hud-luta.css`, "a roda de ações"): Atacar, Habilidades, Itens e Fugir como faixas curtas de
    pincel coladas à direita da carta do herói (`arcoDeBotoes`); tecla, ícone e nome numa peça só, sem nicho; o normal
    num carvão quase opaco com um fio de luz no alto (a forma não some no cenário da noite); os estados do seletor
    (marfim examinado, latão aberto, afundar, o fio e o anel do foco); com movimento reduzido, sem entrada nem afundar;
  - *as cartas* (`15-hud-luta.css`): a vez do herói com uma aresta só de latão e a barra em cima; a vez de outro
    pulsa a própria barra, sem anel por fora;
  - *o aviso da cena na luta* ("Inimigos +1 nível", os do clima): a arena cresce 14 px embaixo só quando há aviso, e
    ele fica no canto direito dessa faixa, sob os inimigos, fora do caminho dos comandos;
  - *as escolhas da página* (`18-seletor-habilidades.css`, no fim; 1.113.0, a regra pela função na 1.113.1):
    `escolhas.js` dá a classe `.faixas` às escolhas narrativas, as da partida em andamento fora da luta: o lugar, a
    vila (Passear, a ação da missão), os eventos e os diálogos (com os testes de atributo), as cenas da missão, a
    viagem ("Para onde?"). O critério é a função: há partida quando o motor manda o estado dela (`estado.py` só o
    monta com herói e mundo); antes disso (o título, a lista de saves, a criação do personagem, que terá a etapa
    própria) não há escolha narrativa. Não depende do lugar, do texto nem de marca do motor (a marca `explorar` da
    1.111.0 saiu). Ficam com o tratamento próprio: a roda, o seletor e a mira da luta, a confirmação e a janela do
    achado (por cima), a doca, os caminhos, os prédios da vila e as telas desenhadas (o mercado, o Inventário, a
    fogueira, os serviços): os controles operacionais delas nunca chegam a esta lista (`ACOES_OCULTAS`). As pontas
    escalam pela altura (a opção de várias linhas é uma pincelada só, com mais folga quando há riscos ou nota); as
    etiquetas (riscos, o teste de atributo) ficam escuras com a cor delas também no marfim; a indisponível fica cinza
    riscada, com o nome claro e o motivo no vermelho de perigo, também sob o mouse; a seta › e a opção secundária
    leem nos dois fundos. O conteúdo, a ordem, as teclas e as regras de cada opção não mudam.
- As lutas cheias (1.111.0): `batalha.js` (`distribuir`) divide a arena em três áreas, cada uma só sua: a sua fileira
  (você em cima e a comitiva, o animal e os servos embaixo, sempre numa coluna), a faixa dos comandos (a roda e, na
  mira, o lembrete com o Voltar, que `rodaMira` põe ao lado da sua carta, onde a roda estava; nenhuma carta entra ali:
  `FAIXA_COMANDOS`) e a dos inimigos, à direita. Até três inimigos, uma coluna (a composição de sempre); com mais,
  duas colunas só quando cabem fora da faixa dos comandos (janela larga), enchendo de cima para baixo e a da direita
  primeiro (o reforço que entra vai para o fim; a luta não volta para uma coluna); senão, uma coluna mais alta, e a
  arena cresce (`acomodar`). Numa arena estreita, a coluna dos inimigos cede (`--coluna`, mínimo 150 px) antes de
  entrar na faixa. Quem sai no meio da luta (o ladrão que foge, o invocado que cai) deixa uma vaga do tamanho da carta
  (`vagar`): ninguém salta sob o mouse enquanto você escolhe; a vaga fecha no próximo lance (`fecharVagas`). Quem foi
  invocado e cai sai da arena depois de cair, dos dois lados (o servo do herói, o reforço que o guardião chama, que o
  motor marca com `invocado`); os outros caídos ficam, apagados. Os maiores grupos reais (medidos com o robô de
  `tests/arena.py`): 6 aliados (o necromante com a comitiva de 2, dois esqueletos da Legião de Ossos e o servo do Rei
  dos Mortos) e 6 inimigos (o bando de caídos à noite com a comitiva e a escolta do xamã); a comitiva tem no máximo 2
  companheiros (`comitiva/catalogo.py`, `LIMITE`); o Rei dos Mortos age uma vez por combate (`uma_vez_por_luta`,
  1.113.2: antes, o xamã reviver um caído abria uma segunda vez). Seis de cada lado é o limite das regras, e é também o
  maior grupo que o robô viu (`ferramentas/prototipos/hud/compacta/efeitos_reais.py`, 1.200 lutas). Uma linha de
  efeitos em cada carta é comum numa luta cheia (a Maldição, o enfraquecer, as chamas ou o sangramento em área), e em
  1280×720 a arena cresce até o registro sumir. Por isso (1.114.0, `acomodarRegistro` em `app/paineis.js`): no começo
  da luta e a cada novo tamanho de janela, se a coluna mais alta com uma linha de efeitos em cada carta deixasse menos
  de 140 px ao registro, ele (`#cena`, fixo) vai para a coluna do mundo, embaixo do nome do lugar, do nível e dos
  avisos (por cima do minimapa, da missão e dos caminhos, inertes); sem ela (abaixo de 1100 px), para a da ficha,
  embaixo do nome e da experiência; sem nenhuma (abaixo de 920 px), fica embaixo com 240 px e a página rola
  (`registro-rola`). No mesmo tamanho, efeitos que entram e saem não mudam nada de lugar; o fim da luta devolve tudo.
  A conferência: `ferramentas/prototipos/hud/fotografar_lutas_cheias.mjs` (o jogo de antes, num checkout do commit
  anterior, e o de agora, com os mesmos dados) e `comparar_lutas_cheias.py`.
- A aba Vender do mercado (`telas/mercado.js`, 1.105.1): durante a visita, cada peça fica no espaço da grade em que
  estava (`arranjo`); vender deixa o espaço vazio, as outras não escorregam, e o que chega (a recompra, a peça que
  sai do corpo ao equipar) vai para o primeiro vazio. Cada peça tem uma ficha (`data-peca`) que o pedido de venda
  guarda; a posição de verdade na mochila do motor (`data-mochila-loja`) é refeita a cada desenho e só vai ao motor
  na hora de responder, com o menu daquele momento. A peça pedida some da grade na hora (não aceita outro clique);
  ao redesenhar, a que a tela sabe que saiu (vendida ou equipada) sai pela ficha, e as outras se acham pelo que são,
  na ordem da mochila. Sair do mercado esquece o arranjo: a mochila volta à ordem de sempre.
- `icones.js` (`Icones`) é o único lugar que decide o desenho de cada papel: o item pelo desenho que o motor dá,
  o consumível pelo id, o atributo, o recurso do topo, o vital, o atalho da doca, o lugar de um caminho, a ação da
  roda, o retrato, a cabeça e a figura do herói e dos companheiros (de `retratos.js`, abaixo). Devolve a `<img>` pronta ou `""` quando a família não tem aquele desenho; a
  tela usa então o sprite do jogo (`Icones.item(s) || S(s, 2)`). A origem e o destino de uma animação pedem o mesmo
  papel (o item que voa ao equipar, o selo de atributo, o consumível que cai na bolsa). Lacunas (desenho do jogo no
  lugar, sem trocar por desenho de outro tipo de item): o chapéu de couro (usa o capuz por ora), a Coroa dos Afogados
  (usa o Diadema por ora; pede arte própria), os
  itens únicos com desenho próprio, a bolsa vazia e o frasco vazio no topo, os inimigos e as cartas deles (menos o
  Afogado e a Ilse, abaixo), os
  ícones de habilidade e de efeito, o covil vencido. O mercador da banca tem o busto no balcão (`telas/mercado.js`,
  com as cores da figura da banca).
- As cabeças próprias das criaturas (1.162.0): o motor dá o retrato (`dados.retrato(tracos, familia, chave)`): a
  chave da criatura única (`RETRATO_CHAVE`: a Ilse da capela, `chefe.chave = "ilse"` em `missoes.py`), senão a
  família (`RETRATO_FAMILIA`: o afogado, com o Afogado Inchado e os afogados que a Ilse invoca; desde a 1.163.0, o
  lobo e o bandido, com os líderes e os invocados; desde a 1.166.0, o troll da montanha; desde a 1.167.0, a aranha,
  com as que a Rainha Aracnídea invoca; desde a 1.171.0, o sapo-touro gigante e a sanguessuga gigante; desde a 1.172.0, o cultista, a bruxa do pântano e o
  rato gigante; desde a 1.173.0, o javali selvagem e o carniçal;
  desde a 1.174.0, o espectro; desde a 1.175.0, o esqueleto, com os que o Lich invoca; desde a 1.179.0, o mercenário,
  com o Invicto da ponte e o Theodore, e o lobo gélido; desde a 1.182.0, o caído, com os que o xamã ergue; desde a 1.183.0, o grifo; desde a 1.184.0, a harpia e o xamã caído; desde a 1.185.0, a cria do Vazio, com as que o antagonista invoca; desde a 1.186.0, o cão infernal; desde a 1.187.0, o cavaleiro sombrio, com o Último Guarda; desde a 1.188.0, a abominação; desde a 1.189.0, a árvore desperta e o golem de pedra, menos quem só reaproveita os números da família: o Espantalho Possuído e o Mímico, que o evento marca com a `origem` do inimigo; o Espantalho segue pelos traços e, desde a 1.192.0, o Mímico tem o dele pela origem, `RETRATO_ORIGEM`), senão os
  traços. Um guardião pelo id do catálogo (`RETRATO_GUARDIAO`, 1.167.0:
  o Rei Troll; 1.168.0: a Rainha Aracnídea; 1.190.0: a Árvore Anciã, o id `ent_anciao`, só o 16 e o 32 da carta; 1.191.0: o Golem Primordial, o mesmo (e, pela origem, o Mímico na 1.192.0); 1.193.0: o Dragão de Gelo, o mesmo; `instanciar_guardiao` guarda o id em `guardiao`, porque a chave do guardião
  muda com o lugar); os outros guardiões continuam pelos traços, como antes (a caveira dos outros mortos-vivos, o
  `fera` do animal do herói e dos guardiões feras e o `humano` dos guardiões humanos e do antagonista continuam). A luta, o Bestiário, o mural e o rastro dos contratos e a
  faixa do mestre caçador pedem `Icones.criatura(retrato, lado)` (o papel `CRIATURA`) antes do sprite: o 16×16 a 2×
  (32) e a 3× (48), em arquivos (`retrato-afogado`, `retrato-ilse`, `retrato-lobo`, `retrato-bandido`, `retrato-troll`, `retrato-rei-troll`, `retrato-aranha`, `retrato-sapo`, `retrato-sanguessuga`, `retrato-cultista`, `retrato-bruxa`, `retrato-rato`, `retrato-javali`, `retrato-carnical`, `retrato-espectro`, `retrato-esqueleto`, `retrato-mercenario`, `retrato-lobo-gelido`, `retrato-caido`, `retrato-grifo`, `retrato-harpia`, `retrato-xama-caido`, `retrato-cria-vazio`, `retrato-cao-infernal`, `retrato-cavaleiro-sombrio`, `retrato-abominacao`, `retrato-arvore-desperta`, `retrato-golem`; os guardiões e o Mímico, `retrato-rainha-aracnidea`, `retrato-arvore-ancia`, `retrato-golem-primordial`, `retrato-mimico` e `retrato-dragao-de-gelo`, só o 32 da carta; fontes em
  `ferramentas/arte/aseprite/`). O animal do patrulheiro (1.164.0) tem o papel `ANIMAL` (`Icones.animal(tipo, 32)`,
  pelo `tipo` de `classes.COMPANHEIROS`): o Urso Pardo e o Falcão Peregrino na carta aliada e no painel da comitiva
  (`retrato-urso`, `retrato-falcao`); desde a 1.165.0, o Lobo Cinzento com o mesmo arquivo do Lobo inimigo
  (`retrato-lobo`, sem cópia). O nome
  da carta não entra na escolha. As outras criaturas seguem pelos traços (o levantamento em
  `ferramentas/prototipos/hud/criaturas/LEIA-ME.md`).
- A Calça de Couro do Arqueiro (1.119.0): desenho próprio do conjunto de couro, para todas as calças de couro dele
  (Rasgada, Curtida, Reforçada e as raras com nome; os saves já guardam `icone: "calca_couro"`). Fontes em camadas
  em `ferramentas/arte/aseprite/calca_couro/` (32, 40, 48; o 64 é o 32 ampliado 2×, `DERIVADOS`), exportadas por
  `exportar_aseprite.py calca_couro`. Os quatro atributos são pixel art: Ataque e Defesa (1.120.0), Agilidade (1.121.0) e
  Poder (1.123.0), com fontes em `ferramentas/arte/aseprite/attr-ataque/`, `attr-defesa/`, `attr-agilidade/` e
  `attr-poder/` (24 e 32; o 64 do selo da festa de atributo permanente é o 32 ampliado 2×). A Agilidade é também o
  Fugir da roda da luta (`ACAO.fuga`); a bota do equipamento é outro desenho. A aljava (1.122.0) também tem fontes em camadas (`ferramentas/arte/aseprite/
  aljava/`: 24 do topo, 32, 40 do Inventário, 48 do saque; o 64 é o 32 ampliado 2×), para toda Aljava do Patrulheiro
  (a comum e a única) e o recurso de flechas do topo. O Poder é só o atributo: a "chama" do Vigor, da Pena de Fênix e das
  habilidades de fogo é outro desenho.
  Na doca, são pixel art, com fontes em `ferramentas/arte/aseprite/atalho-*/` (36 e 32):
  - o Inventário (a mochila de couro) e o Mapa (o mapa dobrado), da 1.124.0;
  - o Diário (o livro aberto), da 1.125.0;
  - o Grimório (o livro fechado), da 1.126.0, que é também o Habilidades da roda da luta (`ACAO.grimorio`);
  - os Talentos (a árvore de latão) e a Comitiva (três viajantes), da 1.127.0. A Comitiva só aparece com
    companheiro e tem papel próprio; o sprite `humano` que ela usava continua o de personagem e de inimigo.
  - o Bestiário (o crânio de fera com chifres), da 1.128.0. A "caveira" 16×16 dos retratos, da derrota e da fome é
    outro desenho.
  - o Salvar (o baú aberto com a seta de aço) e o Sair (o arco de pedra com a seta laranja), da 1.129.0. Com eles,
    os nove atalhos da doca estão em pixel art (plano 23, 1D).
- A Vida (o coração) e a Mana (a gota de energia líquida, no azul da barra) do topo, em 20, da 1.130.0, e o Vigor
  (o punho cerrado) e o Foco (o alvo, no verde da barra), da 1.131.0 (`ferramentas/arte/aseprite/vital-*/`): os
  quatro ícones das barras do topo em pixel art. O custo das habilidades continua com os sprites do jogo.
- O Ouro (a pilha de moedas) e as Provisões (o pernil) do topo, da 1.132.0 (`ferramentas/arte/aseprite/moedas/`,
  `provisoes/`): o Ouro em 24, só no topo (`Icones.recurso`); as Provisões em 24 no topo e em 32 nativo no cartão
  "Provisões (1 dia)" do mercado (`Icones.porDesenho`), no lugar do @2x do 24 reduzido. Sem comida, o topo continua com
  o osso. Desde a 1.133.0, o seu ouro no balcão do mercado e dos serviços (ferreiro, curandeira, templo, taverna;
  `.ouro-loja`) é a mesma pilha em 32 (`Icones.ouro`, fonte `moedas-32.aseprite`, a construção do 24 na grade de 32);
  o sprite `moedas` do jogo fica como está.
- A moeda avulsa (1.134.0, `ferramentas/arte/aseprite/moeda/`, 16 e 32; `Icones.moeda`), a que acompanha preços e
  ganhos, distinta da pilha do saldo: os preços do mercado e dos serviços, a linha "Custo", a dica de venda e
  recompra, o prêmio do contrato, os ganhos do pagamento de contratos, o chip e o aviso de ouro e as moedas que voam
  até o topo (16); a linha de Ouro do espólio e a moeda que o ladrão leva na luta (32). Onde a tela só tem o nome do
  desenho (o chip, o aviso, os ganhos, a linha "Custo", o projétil), `"moeda"` vai para o `Icones.moeda`; o sprite
  `moeda` do jogo continua no resto.
- A tocha (1.135.0, `ferramentas/arte/aseprite/tocha/`, 24 e 32): o cabo de madeira, o pano enrolado e a chama em
  línguas, no topo (24) e no cartão do mercado, na bolsa, no espólio e no voo até a bolsa (32). Os 48 e 64 da família
  de ferro saíram do jogo (nenhum lugar os usava); no `familia_ferro.py` a tocha continua na conta da escala do grupo,
  mas o arquivo não sai mais de lá (como o escudo e a aljava: as peças do grupo com fonte no Aseprite são achadas pelas
  pastas das fontes e conferidas pelo `exportar_aseprite.py`). Desde a 1.136.0, também a tocha em 16 (o chip e o aviso
  de um item ganho, o ícone das escolhas que a gastam, o risco "−1 tocha", o aviso de escuro do painel do lugar) e a
  tocha apagada (`tocha_apagada`: 24 no topo sem tochas, no lugar do sprite em 32, e 16 no risco "Sem luz" e no aviso
  do lugar sem tocha), com fontes em `aseprite/tocha/` e
  `aseprite/tocha_apagada/`. Os ícones de 16 que a tela pede pelo nome do desenho (o chip, o aviso, o item e os riscos
  de uma escolha) passam pelo `Icones.miudo` (a moeda, a tocha e a apagada); os outros nomes ficam com o sprite.
- Desde a 1.138.0, em pixel art (fontes em `ferramentas/arte/aseprite/`): a Bandagem e a Poção de Vida (16, 24, 32: o
  topo, os usos de consumível, o chip, o aviso e as escolhas; a Poção é também o comando Itens da roda da luta), o
  Tônico Restaurador (16 e 32) e, de equipamento, a Calça de Viagem e o Manto do Mago (32, 40, 48; o 64 é o 32 ampliado
  2×; o Manto vale para o Manto, a Túnica, a Veste Rúnica e o Manto de Cinzas). Os 48 e 64 antigos da bandagem, da
  poção e do tônico saíram (sem uso). O 16 de um consumível vem pelo id do item quando a tela sabe qual é
  (`Icones.pequeno`: o chip, o aviso, o item e o gasto de uma escolha), e só no tamanho nativo; o sprite do Tônico
  (`pocao_azul`) continua a Mana e o Unguento nos outros lugares. A bandagem e a poção entram também no `Icones.miudo`
  (esses sprites só significam esses itens). Desde a 1.139.0, também o Antídoto (16 e 32; o tubo verde de base plana,
  lacrado com cera; o 16 pelo item, porque o sprite dele, `folha`, é a Agilidade em outros lugares) e o frasco vazio
  (24, o topo sem poções, no lugar do sprite em 32; a Poção de Vida sem o líquido). Desde a 1.140.0, o anel (o aro
  de ouro em pé, de três quartos, com o ziguezague gravado; o Anel, o Sinete, o Aro e o Anel do Último Rei) e o amuleto
  (a gema violeta no engaste de latão; o Amuleto, o Talismã, o Pingente e o Medalhão), 32, 40, 48 e o 64 = 32 ×2, fontes
  em `aseprite/anel/` e `amuleto/`; os espaços vazios do anel e do amuleto usam as mesmas imagens, apagadas. As
  referências permanentes dos anéis estão em `ferramentas/arte/referencias/aneis/`. Desde a 1.141.0, o Chapéu Pontudo
  do Mago (a aba larga em perspectiva, a copa de lã com a ponta tombada, a fita de linho; 32, 40, 48 e o 64 = 32 ×2,
  fontes em `aseprite/chapeu/`); o espaço vazio da cabeça continua com o elmo de ferro. Desde a 1.142.0, a Sandália do
  Mago (o par de couro em três quartos, com a palmilha e as tiras, pela referência em `ferramentas/arte/referencias/
  botas/`; 32, 40, 48 e o 64 = 32 ×2, fontes em `aseprite/sandalia/`); o espaço vazio dos pés continua com as botas de
  ferro. Os nomes da Sandália vêm dos materiais de tecido ("Sandália de Lã Negra"), embora o desenho seja de couro:
  pendência de nomenclatura no plano 23. Desde a 1.143.0, a Besta Leve do Arqueiro (deitada na diagonal: a coronha de
  madeira, o arco de aço atravessado, a corda em V até a noz; 32, 40, 48 e o 64 = 32 ×2, fontes em `aseprite/besta/`); a
  arma vazia continua com a espada de ferro. Desde a 1.144.0, o Diadema do Mago (o aro de latão de frente, a ponta com a
  gema violeta; 32, 40, 48 e o 64 = 32 ×2, fontes em `aseprite/diadema/`), o papel do desenho `coroa` do equipamento
  (`ITEM`: `coroa` → `diadema`): a base Diadema e, por ora, o único Coroa dos Afogados. O símbolo da reputação continua
  com o sprite `coroa` (`S` e `MIUDO`, fora de `ITEM`); a cabeça vazia continua com o elmo de ferro. Desde a 1.145.0, o
  remake do ferro começou pela espada (a lâmina regular de gumes contínuos e a ponta no eixo, a guarda de latão; também
  o Montante, a silhueta da arma vazia e o Atacar do Guerreiro) e pela maça (o bulbo de aço com as aletas curtas), 32,
  40, 48 e o 64 = 32 ×2, fontes em `aseprite/espada/` e `maca/`; o `familia_ferro.py` as reconhece pelas fontes e não as
  grava mais. O ícone do atributo Ataque é outro desenho. Desde a 1.146.0, a cota (a camisa de malha de aço, a gola na
  malha, as mangas e a barra em dentes, o cinto de couro; 32, 40, 48 e o 64 = 32 ×2, fontes em `aseprite/cota/`), o
  desenho `armadura` (`ITEM`: `armadura` → `cota`): a Cota de Malha, o Peitoral, a Couraça e a Brigantina, e a silhueta
  do peito vazio; o compartilhamento representa pior o Peitoral e a Couraça, que são de placa. Desde a 1.151.0, a
  manopla é a L7 (o par de luvas de couro com a malha nas costas da mão e nos punhos, a transposição da referência que
  o Jean escolheu; a origem e a licença do recorte de referência pendentes; a fonte `aseprite/manopla/manopla-32.aseprite`;
  o 40 e o 48 são o 32 centrado num quadro transparente e o 64 = 32 ×2, pelo `DERIVADOS` do exportador): a Manopla do
  Guerreiro e os raros dela, e a silhueta das mãos vazias. A M5 (1.147.0, adaptada da `glove_04` da Dungeon Crawl
  Stone Soup, CC0) é histórico, em `aseprite/historico/manopla-m5/`. A habilidade Grito de Guerra continua com o sprite "manopla" do jogo. Desde a 1.153.0, o elmo é o
  capacete com malha C1 (a calota arredondada com a crista, a faixa da testa e a nasal de aço, a malha envolvendo os
  lados e a nuca, a abertura do rosto vazia, as tiras de couro; a transposição da imagem gerada do Jean): o Elmo, o
  Capacete e a Barbuta, a cabeça vazia e a reserva da cabeça (`ICONE_ESPACO`); a fonte `aseprite/elmo/elmo-32.aseprite`;
  o 40 e o 48 são o 32 centrado num quadro transparente e o 64 = 32 ×2, pelo `DERIVADOS`; o elmo de frente da 1.148.0 é
  histórico, em `aseprite/historico/elmo-r4/`. Desde a 1.152.0, as perneiras são a P7 (a calça de malha com o cinto de couro e a fivela, as
  laterais no volume da malha, as joelheiras em cúpula com as juntas, as caneleiras e os punhos de couro; a
  transposição da segunda imagem gerada do Jean): o desenho `calca`, a Perneira e a Greva, as pernas vazias e a reserva
  das pernas (`ICONE_ESPACO`); a fonte `aseprite/perneiras/perneiras-32.aseprite`; o 40 e o 48 são o 32 centrado num
  quadro transparente e o 64 = 32 ×2, pelo `DERIVADOS`; a P4 (1.148.0) é histórico, em `aseprite/historico/perneiras-p4/`. Desde a 1.150.0, as botas de ferro (o par em três
  quartos: o cano moldado com a boca escura, as tiras de couro com fivela, as placas do tornozelo até a biqueira, a
  sola de couro; a transposição da referência gerada do Jean, `ferramentas/arte/referencias/botas/`; 32, 40, 48 e o
  64 = 32 ×2, fontes em `aseprite/botas-ferro/`; desde a 1.154.0 com o acabamento A1, os reflexos contidos e o aço
  no tom médio, a mesma forma; as fontes da B3 em `aseprite/historico/botas-ferro-b3/`): a Bota Ferrada e a silhueta
  dos pés vazios. Nenhuma peça de ferro do
  equipamento sai mais do `familia_ferro.py` (só o baú da bolsa): os 31 desenhos-base de equipamento das classes
  estão no padrão atual.
- O escudo e o Unguento de Prata (1.94.0), o machado e a Bomba de Fumaça (1.99.0) o arco (1.101.0,
  `desenhar_arco_pixel.py`; desde a 1.169.0 também o Atacar do Arqueiro na roda, pela classe, com a Besta
  inclusive; o Tiro Duplo e o contrato continuam com o sprite) e o cajado (1.106.0,
  `desenhar_cajado_pixel.py`; desde a 1.177.0 também o Atacar do Mago na roda, pela classe, qualquer que seja a
  arma; o traço Conjurador continua com o sprite) e o orbe (1.107.0,
  `desenhar_orbe_pixel.py`; a arma Orbe, o Foco Arcano e o Olho do Abismo) e o grimório fechado (1.108.0,
  `desenhar_grimorio_fechado_pixel.py`; a arma Grimório, o apoio Tomo e o Tomo do Nome Esquecido; o talento Mente
  Vasta, os atalhos do Diário e do Grimório e o livro da capela continuam com os deles) e a varinha (1.109.0; a arma
  Varinha, o único equipamento com o desenho "varinha") e o gibão e as botas de couro (1.110.0; o peito do Arqueiro, a
  Bota de Caça e os únicos Pele do Penitente e Botas do Andarilho Morto) são desenhados em pixel art, cada
  tamanho na própria grade, por `ferramentas/arte/` (`desenhar_escudo_pixel.py`, `desenhar_unguento_pixel.py`,
  `desenhar_machado_pixel.py`, `desenhar_bomba_pixel.py`, com as etapas comuns em `pixel_comum.py`), que grava os
  arquivos prontos em `static/hud/icones/`; o jogo só lê os arquivos. A varinha é a primeira com a fonte num
  `.aseprite` em camadas (`ferramentas/arte/aseprite/varinha/`), desenhada no Aseprite pelo MCP; os PNGs saem de
  `ferramentas/arte/exportar_aseprite.py varinha` (`--conferir` compara com os do jogo). O gibão e as botas de couro
  também (`aseprite/gibao/`, `aseprite/bota/`), com o 64 sendo o 32 ampliado 2× (`DERIVADOS` no exportador; os 64
  desenhados à parte ficam em `aseprite/historico/`). O estado Iniciativa continua com o sprite "bota" e o espaço vazio
  dos pés com a bota de ferro. A cabeça e as mãos de couro e de tecido (1.112.0; `aseprite/capuz/`, `luva/`,
  `capuz_tecido/`, `luva_seda/`, o 64 também derivado do 32): o capuz e a luva de couro para o Arqueiro (Capuz, Chapéu
  de Couro, Braçadeira) e as Mãos do Estrangulador; o capuz de tecido e a luva de seda para o Capuz e a Luva de Seda do
  Mago. O desenho vem do item (`itens.py`; `icone_de`, num item sem desenho guardado, decide pela classe para a qual a
  peça foi feita); os itens guardados antes recebem o de tecido pela migração do save v4 → v5 (`migracoes.py`). A
  habilidade Desaparecer continua com o sprite "capuz"; os espaços vazios da cabeça e das mãos, com o elmo e a manopla. O unguento e a bomba se acham só pelo id do
  consumível: o desenho "unguento" do jogo é também o da Curandeira, e a "caveira" da bomba é também retrato,
  Bestiário, derrota, fome e a lixeira, que ficam com o deles. O machado vale para todo equipamento com o desenho
  "machado" (os únicos Lamento de Gharbad e O Açougueiro também); o Redemoinho e a Fúria continuam com o sprite. A
  escolha de evento que gasta um item (`escolhas.js`, `meta.gasta`) ainda mostra o sprite de 1×, não o `Icones`. A
  conferência no jogo, nos lugares de cada item: `ferramentas/arte/fotografar_itens.mjs`; em tamanho real sobre o
  carvão: `ferramentas/arte/prancha.py`. O processo de desenhar e avaliar um item está na skill do projeto
  `.claude/skills/arte-itens-fenda/` (`/arte-itens-fenda`).
- O equipamento no corpo e na mochila do Inventário aparece em 40 px (1.95.0), com arquivos nativos de 40
  (`Icones.equipamento`): a família de ferro pintada sai de `ferramentas/arte/familia_ferro.py` (as peças aprovadas em
  `familia-ferro/`, o mesmo processo dos tamanhos de sempre: a escala do grupo e a redução "paleta"; `--conferir`
  refaz todos e compara com os do jogo) e o escudo das regras dele. As peças do grupo que passaram para fontes no
  Aseprite (a aljava, a tocha) continuam na conta da escala, mas saem e são conferidas pelo `exportar_aseprite.py`. O que não tem arquivo de 40 (os sprites 16×16 das armas
  e peças de couro) fica em 32 px, nítido e centrado no mesmo espaço. As silhuetas
  dos espaços vazios, a bolsa, a ficha, os atributos, a doca, o mercado e a luta continuam em 32.
- `desenhos.js` (`Desenhos`): os itens desenhados em código, pelo mesmo método (desde a 1.93.0): o martelo e a Pena de
  Fênix, em 32×32, o tamanho em que vivem (bolsa, mochila, mercado, espólio). `Icones` os entrega como os outros
  desenhos: em 32 e 64 px pixel a pixel; em 48 (o item que voa para o corpo, o cartão compacto do saque) a versão a 2×
  reduzida pelo navegador, como os outros ícones da HUD. Desde a 1.149.0 o martelo tem o 40 e o 48 em arquivo
  (`hud/icones/martelo-40.png` e `-48`, fontes em `ferramentas/arte/aseprite/martelo/`, a mesma construção na grade de
  cada tamanho): nesses lados `Icones` usa o arquivo (`TAMANHOS`), no Inventário e no "você usa" do saque; o 32 e o
  64 continuam a grade daqui. A Pena de Fênix só se acha pelo id do consumível, nunca pelo
  desenho: no jogo ela usa a "chama", que também é o Vigor, o Poder e as habilidades de fogo.
- `retratos.js` (`Retratos`): os retratos do herói e dos companheiros desenhados em código, pelo método das cenas
  (uma grade de letras com a paleta do desenho, pintada por `Sprites.grade`, o mesmo pintor do busto do mercador). As
  três classes: o Guerreiro (1.90.0: o capacete fechado, sem rosto), o Mago e o Arqueiro (1.91.0: o capuz alto azul; o
  capuz curto verde com a aljava, que desde a 1.97.1 fica nas costas na diagonal da correia). Os companheiros, pelo id do motor (1.92.0): Morel, Odette (`odete`) e Yara. Cada um
  tem um desenho por papel, sempre mostrado no mesmo tamanho: o busto da ficha (80 px), o da janela baixa (64), a
  cabeça (48: o topo, os cartões da Comitiva e da reação, a faixa de quem chega), a carta (32: a luta, o painel, o
  aviso) e a figura de 16×16 (a fogueira e o chip de aprovação no texto). A escala sai do tamanho do desenho: o busto
  dos heróis, de Odette e de Yara é de 40×40 a ×2 (a janela baixa e a cabeça são recortes na mesma escala), a carta de
  16×16 a ×2; o do Morel é de 80×80 a ×1, com a ficha baixa e a cabeça em 64 e 48 a ×1, e a carta é a figura de 16×16
  da fogueira a ×2, com a espada num eixo só (1.96.0; antes, o busto de 40×40 reduzido a 32). O critério entre eles é a leitura, a identidade e o peso parecidos no tamanho em que aparecem,
  não a mesma resolução de origem nem a mesma proporção entre cabeça e ombros. Quem escolhe é sempre `Icones`:
  `retrato` (ficha, Inventário), `cabeca` (48, 32 ou 16 px, conforme o lugar) e `figura` (o canvas de 16×16 da
  fogueira, com o papel `fogueira` de quem tem um desenho próprio ali: o Mago sentado, desde a 1.97.0; para quem não tem, o sprite do jogo). Nenhuma tela pede o sprite da classe nem do companheiro direto. O
  retrato não depende do equipamento nem dos atributos.
- Na vez do herói a carta dele é ampliada 1,12× (`.carta.foco`), mas o nicho do retrato desfaz a ampliação (o rosto em
  32 px exatos) e `Batalha.foco` o põe no pixel inteiro da tela, depois que os movimentos da arena acabam (as
  propriedades `scale` e `translate`, que não brigam com as animações da carta). Os companheiros não recebem foco.

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
| `tests/navegador/redimensionar.mjs` | a mesma página alternando o tamanho da janela, sem recarregar: os prédios da vila e os pontos da capela (área, balão, ponta) ficam onde estariam numa página aberta naquele tamanho; mouse, teclado, clique e F4 depois das alternâncias |
| `python -m tests.equilibrio` | não é teste, é régua: heróis típicos por especialização e nível lutando (`tests/arena.py`) |
| `python -m tests.replay` | régua humana: as partidas de `tests/runs/` refeitas com os números de agora |
| `python -m tests.broquel` | régua do Broquel do Vigia: lutas inteiras do Guerreiro com cinco jeitos de usar o escudo, o Broquel contra o mesmo escudo sem o efeito, um raro e a Égide (`--exp vale\|talentos\|comitiva\|posterior`) |
| `python -m tests.saque_vale` | régua do saque: o Vale do Turvo inteiro jogado por um robô (roteiro no topo do arquivo), contando baús, suprimentos, equipamento, vendas e ouro; também a trajetória de cada percurso, as estratégias do começo (`--estrategia`) e a conta de uma luta (`--economia`) |

Mudou o jogo de propósito? `python -m tests.gabarito --atualizar` e diga no commit o que mudou.
