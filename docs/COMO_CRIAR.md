# Como criar

Receitas para crescer o jogo sem quebrar nada. Cada receita termina com o que rodar para conferir.

## Uma habilidade

1. Em `rpg/habilidades.py`, acrescente no catálogo `HABILIDADES`:

```python
"lamina_gelida": hab("Lâmina Gélida", 12, "inimigo", "130% de dano de gelo; pode congelar.", [
    Dano(1.3, tipo="gelo", rotulo="Lâmina Gélida", depois=[
        Se("acertou", Aplicar("atordoado", 1, chance=0.3, rotulo="congelado"))])],
    icone="gelo", familia="gelo", realce="gelo"),
```

2. Dê a habilidade a uma classe ou especialização em `rpg/classes.py` (`"habilidades": [(nível, "lamina_gelida")]`).

Como ela aparece na tela também é dado, na própria ficha:

| Campo | O quê |
|---|---|
| `icone` | o desenho (um nome de `sprites-dados.js`) |
| `familia` | a cor da carta de ação (`FAMILIAS_TELA`: fisico, forca, protecao, sagrado, sangue, natureza, sombra, veneno, fogo, gelo, arcano, cura) |
| `anim` | opcional: um jeito próprio de animar (`ANIMACOES`: grito, falange, rugido, redemoinho, rajada). Sem ele, a tela anima pelo tipo (golpe, magia, bênção) |
| `realce` | opcional: a cor do nome quando ele aparece num texto de regra ("a **Lâmina Gélida** congela") |

Pronto: a luta executa, o Grimório mostra o dano de agora (faixa, crítico, fórmula, escala), a janelinha de
habilidades mostra a dica com o ícone e a cor. Não escreva os números nem os ícones em outro lugar: a tela não tem
mais lista de habilidades. Um jeito de animar novo é a única coisa que pede JS: acrescente o nome em `ANIMACOES` e
o caso em `batalha.js` (`m.anim === "..."`); o validador cobra os dois.

### Os blocos

| Bloco | Faz | Exemplo |
|---|---|---|
| `Dano(mult, stat, tipo, alcance, crit_extra, bonus, rotulo, esquiva, em, depois)` | um golpe; `em="todos"` acerta todos; `depois` roda para cada alvo | `Dano(1.0, alcance="distancia", em="todos")` |
| `Se(condicao, *passos)` | `"acertou"`, `"vivo"`, `"acertou_vivo"` | `Se("acertou", ...)` |
| `Aplicar(estado, turnos, valor, chance, rotulo, acumula, em, direto)` | um estado no inimigo | `Aplicar("sangramento", 3, valor=Escala(minimo=2, atk=0.3))` |
| `Buff(estado, turnos, valor)` | um estado em você | `Buff("fortalecido", 3, 0.3)` |
| `Acender(chance, garantido)` | queimadura do mago (camadas); `garantido`: chave que torna certo | `Acender(0.6, garantido="acender_garantido")` |
| `Roubo(fracao, rotulo)` | cura parte do dano, com o sangue voltando na tela | `Roubo(0.4, rotulo="Sede de Sangue")` |
| `CurarPeloDano(fracao, bonus)` / `Curar(quanto, bonus)` | cura (luz, não roubo); `bonus`: chave que aumenta | `Curar(Escala(max_hp=0.3), bonus="cura_luz")` |
| `LimparMales()` | remove os estados ruins | |
| `Dizer(texto, cor, se)` | a frase; aceita `{alvo}`, `{cura}`, `{turnos}` | `Dizer("Você brilha. (+{cura} vida)", "verde", se="cura")` |
| `Salva(hab, *passos)` | os golpes saem juntos na tela (rajada) | o Tiro Duplo |
| `Codigo(fn, linhas)` | escape para um passo em código | curar o animal na Fúria da Natureza |

Valores que crescem com o herói: `Escala(minimo, atk=..., poder=..., agi=..., max_hp=...)` (sabe se escrever:
"Ataque × 30%") e `Mod(base, chave)` (base + o que os modificadores somam: `Mod(2, "escudo_turnos")` dura 2 turnos,
e a Muralha, que declara `escudo_turnos: 1`, aumenta). Habilidade nunca pergunta por um talento pelo nome: pergunta por
uma chave, e qualquer talento, item ou passiva pode mexer nela.

### Quando não cabe nos blocos

Escreva `fn(cb, u, alvo)` e `linhas(u)` lado a lado, logo acima do catálogo, e use
`hab(..., fn=_minha, linhas=_linhas_minha)`. Se o mesmo padrão aparecer em duas habilidades, ele merece virar
um bloco.

### Conferir

```
python -m unittest tests.test_habilidades tests.test_grimorio tests.test_conteudo
python -m tests.gabarito        # deve passar se você só ACRESCENTOU (habilidade nova não muda partidas antigas)
```

`tests/test_habilidades.py` garante que todo estado aplicado existe no combate e que cada golpe aparece no
Grimório com o mesmo multiplicador.

## Um talento

Em `rpg/talentos.py`, na árvore da classe, o talento diz onde mora (ramo e camada) e o que faz:

```python
_t("olho_aguia", "Olho de Águia", "base", 1, 3, "+4% de chance de crítico por ponto.",
   mods={"critico": 0.04}, icone="olho"),
_t("muralha", "Muralha", "tronco", 3, 1, "Erguer Escudo dura 1 turno a mais e custa 4 a menos.",
   mods={"escudo_turnos": 1, "custo:erguer_escudo": Fixo(-4)}, icone="escudo"),
_t("frenesi", "Frenesi", "berserker", 3, 2, "Cada inimigo que você abate dá +10% de dano por ponto (acumula 3x).",
   gatilhos={"abate": _frenesi}, icone="chama"),
```

Os argumentos na ordem: id, nome, **ramo**, **camada**, pontos máximos, descrição.

- **Ramo**: `"base"` (para todos, antes da especialização, na faixa de cima), `"tronco"` (para todos, depois) ou o id
  de uma especialização da classe (o talento fica exclusivo dela).
- **Camada**: o nível que ela pede está em `NIVEL_CAMADA`. Camada nova = uma linha lá.
- A árvore não tem teto: dois talentos no mesmo ramo e na mesma camada ficam lado a lado, na ordem do catálogo, e a
  tela (e o desenho em texto) abre colunas e fileiras sozinha.

| Campo | O quê |
|---|---|
| `icone` | o desenho do nó (de `sprites-dados.js`) |
| `realce` | opcional: a cor do nome nos textos de regra (como nas habilidades) |
| `stats` | somados aos atributos, por ponto (`{"defesa": 2, "max_hp": 6}`) |
| `mods` | modificadores por ponto; `Fixo(v)` vale uma vez (`{"dano_corpo": 0.06}`) |
| `mults` | multiplicadores (`{"barreira_mult": 1.3}`) |
| `gatilhos` | `{evento: função(cb, u, pontos, dados)}`, com `ordem=` quando dois reagem ao mesmo evento |

As chaves e os eventos existentes estão listados no topo de `rpg/modificadores.py` (`CHAVES`, `MULTS`, `EVENTOS`).
**Chave nova** (ex.: "dano_contra_mortos_vivos"): acrescente em `CHAVES` e faça o lugar do jogo que decide aquilo
perguntar `mod(u, "dano_contra_mortos_vivos")` uma vez; daí em diante qualquer talento, item ou passiva usa.

A passiva de uma especialização (`PASSIVAS`, no mesmo arquivo) segue o mesmo formato, sem pontos.

### Conferir

```
python -m unittest tests.test_modificadores tests.test_conteudo  # chaves e eventos conhecidos; ramo, camada e ícone
python -m tests.gabarito
```

## Um item com efeito especial

Item é fonte de modificadores, como talento. Os bônus especiais (`ESPECIAIS` em `rpg/itens.py`: crítico, roubo de
vida, espinhos, vida por turno, vida por abate) já viram mods do item sozinhos; crítico e roubo ficam no item em %
e viram fração (`PERCENTUAIS`). Um **único** (`UNICOS`) pode ir além e declarar, no catálogo, os mesmos campos de
um talento (`mods`, `mults`, `gatilhos`, `ordem`), sem pontos:

```python
dict(nome="Coração do Carrasco", slot="amuleto", classe=None, base="Amuleto",
     bonus={"atk": 1.2, "critico": 4},                 # o que aparece na ficha e entra nos atributos
     mods={"mult_critico": 0.3},                       # crítico ×0,3 a mais
     gatilhos={"abate": _carrasco},                    # função(cb, u, 1, dados), como num talento
     lore="..."),
```

O item vestido entra em `mod`, `nomes` e `disparar` na ordem dos espaços, depois dos talentos. O Grimório diz de onde
vem cada pedaço (`contribuicoes`). Atributo novo de item (ex.: "dano_fogo"): acrescente em `ESPECIAIS`, em `CHAVES` de
`rpg/modificadores.py`, em `NOME_STAT` (`rpg/entidades.py`) e em `PESO_PRECO`; o lugar do jogo que decide pergunta
`mod(u, "dano_fogo")`.

`python -m unittest tests.test_modificadores` recusa chave, mult ou evento desconhecido num único.

## Um estado

Em `rpg/estados.py`, no catálogo `ESTADOS`:

```python
"congelado": estado(
    "congelado", "gelo", "frio", negativo=True, perde_turno=True,
    imune=lambda a: a.resist.get("gelo", 1) < 0.5,
    resiste=lambda cb, a: a.chefe and cb.rng.random() < 0.5,
    dica="perde o próximo turno",
    descrever=lambda t, v, esc, ch, todos, rot: f"{ch:.0%} de chance de congelar o alvo por {t} turno(s)."),
```

| Campo | O quê |
|---|---|
| `nome`, `icone`, `familia` | como aparece ("congelado"), o desenho (de `sprites-dados.js`) e a cor do brilho na carta |
| `negativo` | é um mal (a Prece e o antídoto tiram) |
| `tique=(rótulo, cor)` | dano por turno igual ao valor do estado; `ajuste_tique(cb, dano)` muda (a chuva apaga as chamas) |
| `perde_turno` | quem está assim não age |
| `imune(alvo)` / `resiste(cb, alvo)` | quem não pega / quem resiste na hora (com sorteio) |
| `camadas`, `rotulo_camadas` | acumula (`"em chamas ×{s}"`) quando aplicado com `acumula=True` |
| `dica`, `descrever`, `buff` | a frase do ícone; a linha do Grimório num inimigo; a linha num estado seu |
| `agora` | a frase com o número, para a carta: `lambda v: f"+{_pct(v)} de dano"` (sem ela, vale a `dica`) |
| `golpe` | o que muda na conta de um golpe, por etapa: `{"dano_causado": lambda v: 1 + v}` |

Tique, perda de turno, imunidade, resistência e camadas já funcionam sozinhos. Um estado que mexe na **conta de
dano** declara em `golpe` as etapas em que entra (a lista, na ordem da conta, é `GOLPE_ETAPAS` em `rpg/estados.py`):
`dano_causado`/`dano_recebido` multiplicam (quem bate / quem apanha), `defesa` multiplica a defesa do alvo, `esquiva`
soma à esquiva, `sem_esquiva` tira a esquiva, `dano_final` multiplica depois do crítico, `critico_garantido` e
`absorve` gastam o estado. `Combate.atacar` pergunta cada etapa (`no_golpe`) e não conhece estado nenhum pelo nome.
Dentro de uma etapa, as contas seguem a ordem do catálogo (bênçãos antes dos males). Etapa nova: acrescente em
`GOLPE_ETAPAS` e pergunte por ela uma vez no lugar certo de `atacar`.

Conferir: `python -m unittest tests.test_estados` (todo estado aplicado no código existe no catálogo; todo
ícone tem desenho).

## Uma habilidade de inimigo

Em `rpg/inimigos.py`, a função (`fn(cb, inimigo, alvo)`, devolve False se não deu para usar) e a entrada no
catálogo `HABS`:

```python
"uivo": hab_inimigo(_uivo, "Uivo", "uivo de matilha", quando=_alguem_sem("fortalecido")),
"mordida_sangrenta": hab_inimigo(_mordida_sangrenta, "Mordida Sangrenta", "garras que fazem sangrar", golpe=True),
```

`quando(cb, e, alvo)` é o juízo: a habilidade só entra no sorteio quando faz sentido (`_sem("maldito")`: o alvo
ainda não está assim; `_alguem_sem("fortalecido")`: alguém do bando ainda sem o bônus). `golpe=True` marca o
que fere: com o alvo a um golpe comum da morte (`Combate.dano_previsto`), o inimigo só escolhe entre esses.
Depois é só pôr o id em `habs` da família (`rpg/dados.py`). `tests/test_inimigos.py` confere que todo id existe.

## Um evento

Em `rpg/eventos/<tema>.py`:

```python
@evento(contextos=("explorar", "viagem"), peso=6, cooldown=10,
        cond=lambda g: g.clima == "nevoa")
def vulto_na_nevoa(g):
    g.dizer("Um vulto atravessa a névoa.", "magenta")
    op = g.menu("O que faz?", [("Seguir", "seguir"), ("Deixar ir", "nao")])
    ...
```

Título da cena em `rpg/eventos/titulos.py`; reações da comitiva em `REACOES` (`rpg/comitiva.py`).

Texto sobre um grupo que pode ter um inimigo só (`g.grupo()` sorteia o tamanho): não escreva "eles". Marque a
frase e deixe `tx.concordar` acertar número e gênero, como as localizações profissionais fazem:

```python
grupo = g.grupo()   # sorteie antes de narrar
g.dizer(tx.concordar("Um galho estala. {Grupo} se {vira|viram}, e {eles} {olha|olham} para você.", grupo))
# um lobo:       "Um galho estala. Um lobo se vira, e ele olha para você."
# duas aranhas:  "Um galho estala. Duas aranhas gigantes se viram, e elas olham para você."
```

Marcadores: `{eles}`, `{os}`, `{deles}`, `{-los}` (distraí{-los}), `{singular|plural}`, `{grupo}` e campos por nome
(`{abertura}`); maiúscula no marcador dá maiúscula no texto.

Número com palavra: nunca "dia(s)". `tx.plural(n, "dia")` dá "1 dia" / "0 dias"; quando o plural não é só pôr s,
ele vai junto: `tx.plural(n, "flecha intacta", "flechas intactas")`. Na tela, o mesmo: `Texto.plural(n, "trecho")`.
Um teste procura "(s)" nos textos do motor e da tela.
(A Etapa D vai trazer eventos e diálogos como dados, com condições e consequências declaradas.)

## Um número de balanceamento

Todos moram em `rpg/balanceamento.py`, com o que cada um faz ao lado. A curva do jogo (herói × inimigos ×
equipamento × XP) fica na seção "a curva". O ciclo:

1. **Meça antes.** Guarde a saída das duas réguas:
   - `python -m tests.equilibrio`: heróis típicos de cada especialização, níveis 1 a 12, contra o que o jogo
     sorteia numa região um nível abaixo, e contra guardiões (`--spec`, `--lutas`, `--atraso`, `--sozinho`).
   - `python -m tests.replay`: as partidas de verdade guardadas em `tests/runs/` (o .jsonl que o jogo grava em
     `<saves>/runs/`), refeitas luta a luta com os números de agora (`--lutas` mostra uma por uma; `--ficha`
     confere o herói remontado).
2. **Mude o número** e meça de novo. As colunas que mais dizem: *Vida perdida* (quanto uma luta custa),
   *Golpes p/ você cair* (quantos golpes inimigos você aguenta) e *Seus turnos p/ matar*. O robô joga um pouco
   diferente de uma pessoa: compare antes com depois, não com um número absoluto.
3. **Sinta jogando:** `python jogar.py --dev 8` começa um jogo novo já no nível 8, com equipamento de acordo.
4. `python -m tests.gabarito --mostrar` para conferir que só mudou o esperado, `--atualizar`, e o motivo (com as
   tabelas de antes e depois) no commit.

Partida nova que mostra um problema? Copie o .jsonl para `tests/runs/`: ela vira régua para as próximas mudanças.

### As metas (o padrão é hardcore)

O jogo é difícil de propósito, mas a morte deve vir do desgaste e das decisões (emendar lutas sem descansar,
encarar campeões, únicos e guardiões), não de uma luta comum sorteada. No simulador, média das especializações:

| Fase | Vida perdida por luta comum | Lutas até descansar | Vitórias em luta comum, de vida cheia | Guardião da região |
|---|---|---|---|---|
| Começo (nv 1–3) | ~20–35% | 2–4 | ≥ 90% | perigoso cedo demais |
| Meio (nv 4–8) | ~20–30% | 3–5 | ≥ 89% | 55–70% de vitórias, sai com dois terços da vida a menos |
| Fim (nv 9–12) | ~30% | ~3,5 | ≥ 85% | idem |

Os botões mais diretos: `DANO_HEROI` e `DANO_INIMIGOS` (todo golpe, físico e mágico), `DANO_COMITIVA` e
`DANO_ANIMAL` (quem luta ao seu lado), `INIMIGO_VIDA`, os de grupo (`GRUPO_*`, `COMITIVA_*`) e os de descanso
(`TAVERNA_VIDA`, `ACAMPAR_VIDA`; o templo cura por ouro).

Nenhuma especialização deve ficar muito longe da média: hoje o Paladino é a mais tolerante e Sombra, Piromante
e Necromante as mais duras (veja o ROADMAP).
