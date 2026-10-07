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

`Combate` (`rpg/combate.py`) roda turnos: sua ação → aliados (comitiva, animal, servos) → inimigos.

- `atacar()` é **a** conta de dano (esquiva, eficácia, modificadores, defesa, crítico, barreira, roubo de vida).
- Cada coisa visível vira um **lance** estruturado (`acao`, `golpe`, `erro`, `cura`, `buff`, `salva`, `fim_acao`...)
  que a tela anima (`rpg/web/static/batalha.js`) e a telemetria contabiliza.
- Estados (veneno, queimadura, guarda, provocando...) ficam em `efeitos` de cada combatente; `aplicar()` anuncia,
  `processar_efeitos()` faz o efeito por turno.

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

O **Grimório** (`rpg/grimorio.py`) monta o livro a partir dessas descrições, e é também onde mora a conta de
crítico (`chance_critico`, `mult_critico`) que o combate, a ficha e o livro usam.

## Dados e números

| Onde | O quê |
|---|---|
| `rpg/balanceamento.py` | todos os números de dificuldade e generosidade |
| `rpg/classes.py` | classes, especializações, animais do Patrulheiro |
| `rpg/habilidades.py` | habilidades (execução + descrição) |
| `rpg/talentos.py` | árvores de talentos e passivas de especialização, cada um declarando o próprio efeito |
| `rpg/modificadores.py` | `mod`/`mult`/`disparar`: como talentos e passivas mudam o jogo (as chaves e eventos válidos) |
| `rpg/inimigos.py`, `rpg/dados.py` | famílias de inimigos, biomas, climas, traços |
| `rpg/itens.py` | consumíveis, equipamento, afixos, únicos |
| `rpg/comitiva.py` | companheiros: valores, aprovação, conversas, combate |

## Saves

`rpg/sistemas/persistencia.py` grava JSON; `rpg/migracoes.py` leva saves antigos para a versão atual
(`VERSAO_SAVE`). Toda mudança de formato ganha uma migração.

## A interface web

`rpg/web/servidor.py` (HTTP + SSE em 127.0.0.1, com token) → `rpg/web/static/`:

- `app/nucleo.js` conexão e fila de mensagens · `app/pagina.js` texto e cenas · `app/escolhas.js` menus,
  doca de atalhos, roda de ações da luta · `app/paineis.js` ficha e mapa laterais · `app/controles.js` teclado
- `telas.js` telas desenhadas (inventário, mercado, talentos, Grimório, fogueira, mural...)
- `batalha.js` o palco da luta · `realce.js` cores dos termos de jogo · `sprites*.js`, `vista.js`, `mapa.js`, `som.js`
- `css/01..13-*.css` por componente

## Rede de segurança

| Teste | O que garante |
|---|---|
| `python -m tests.gabarito` | 18 partidas com sementes fixas saem **idênticas** (refatorar não muda o jogo) |
| `python -m unittest discover -s tests` | sistemas, saves antigos, catálogo de habilidades, Grimório, gabarito |
| `tests/navegador/fumaca.mjs` | a interface web de ponta a ponta (Playwright) |

Mudou o jogo de propósito? `python -m tests.gabarito --atualizar` e diga no commit o que mudou.
