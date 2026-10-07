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
| `Acender(chance, chance_talento)` | queimadura do mago (camadas) | `Acender(0.6, chance_talento="ignicao")` |
| `Roubo(fracao, rotulo)` | cura parte do dano, com o sangue voltando na tela | `Roubo(0.4, rotulo="Sede de Sangue")` |
| `CurarPeloDano(fracao, talento)` / `Curar(quanto, talento)` | cura (luz, não roubo) | `Curar(Escala(max_hp=0.2))` |
| `LimparMales()` | remove os estados ruins | |
| `Dizer(texto, cor, se)` | a frase; aceita `{alvo}`, `{cura}`, `{turnos}` | `Dizer("Você brilha. (+{cura} vida)", "verde", se="cura")` |
| `Salva(hab, *passos)` | os golpes saem juntos na tela (rajada) | o Tiro Duplo |
| `Codigo(fn, linhas)` | escape para um passo em código | curar o animal na Fúria da Natureza |

Valores que crescem com o herói: `Escala(minimo, atk=..., poder=..., agi=..., max_hp=...)` (sabe se escrever:
"Ataque × 30%") e `Tal(base, talento, por_ponto)` (ex.: 2 turnos + 1 por ponto de Muralha).

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
