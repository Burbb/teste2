# Como criar

Receitas para crescer o jogo sem quebrar nada. Cada receita termina com o que rodar para conferir.

## Uma habilidade

1. Em `rpg/habilidades.py`, acrescente no catálogo `HABILIDADES`:

```python
"lamina_gelida": hab("Lâmina Gélida", 12, "inimigo", "130% de dano de gelo; pode congelar.", [
    Dano(1.3, tipo="gelo", rotulo="Lâmina Gélida", depois=[
        Se("acertou", Aplicar("atordoado", 1, chance=0.3, rotulo="congelado"))])]),
```

2. Dê a habilidade a uma classe ou especialização em `rpg/classes.py` (`"habilidades": [(nível, "lamina_gelida")]`).
3. Ícone na tela: `HAB_ICONE` em `rpg/web/static/app/escolhas.js` (sem ícone, usa uma estrela).

Pronto: a luta executa, o Grimório mostra o dano de agora (faixa, crítico, fórmula, escala), a janelinha de
habilidades mostra a dica. Não escreva os números em outro lugar.

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
python -m unittest tests.test_habilidades tests.test_grimorio
python -m tests.gabarito        # deve passar se você só ACRESCENTOU (habilidade nova não muda partidas antigas)
```

`tests/test_habilidades.py` garante que todo estado aplicado existe no combate e que cada golpe aparece no
Grimório com o mesmo multiplicador.

## Um talento

Em `rpg/talentos.py`, na árvore da classe, o talento declara o que faz:

```python
_t("olho_aguia", "Olho de Águia", 1, 0, 3, "+4% de chance de crítico por ponto.",
   mods={"critico": 0.04}),
_t("muralha", "Muralha", 3, 1, 1, "Erguer Escudo dura 1 turno a mais e custa 4 a menos.",
   mods={"escudo_turnos": 1, "custo:erguer_escudo": Fixo(-4)}),
_t("frenesi", "Frenesi", 3, 2, 2, "Cada inimigo que você abate dá +10% de dano por ponto (acumula 3x).",
   "berserker", gatilhos={"abate": _frenesi}),
```

| Campo | O quê |
|---|---|
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
python -m unittest tests.test_modificadores    # chaves e eventos conhecidos, todo talento faz algo
python -m tests.gabarito
```

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

Tique, perda de turno, imunidade, resistência e camadas já funcionam sozinhos. Se o estado muda a **conta de
dano** (como fortalecido ou guarda), falta perguntar por ele no lugar certo de `Combate.atacar`; numa etapa futura
isso também vira modificador.

Conferir: `python -m unittest tests.test_estados` (todo estado aplicado no código existe no catálogo; todo
ícone tem desenho).

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
