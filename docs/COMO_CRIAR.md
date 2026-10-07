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

`rpg/balanceamento.py`. Depois: `python -m tests.gabarito --atualizar` e o motivo no commit.
