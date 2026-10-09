# Crônicas da Fenda: guia para o Claude

RPG de texto offline em português, feito com o Jean (designer e jogador; ele testa jogando e manda o que achou).
Motor em Python puro (só biblioteca padrão) + interface web local (`python jogar.py`).

Leia antes de mexer:
- [docs/ARQUITETURA.md](docs/ARQUITETURA.md): como o motor funciona e onde cada coisa mora.
- [docs/COMO_CRIAR.md](docs/COMO_CRIAR.md): receitas para habilidade, talento, estado, evento, balanceamento.
- [docs/ROADMAP.md](docs/ROADMAP.md): onde estamos (Etapas A, B e C feitas; a D é a próxima) e ideias guardadas.

## Combinados

- Converse com o Jean **em português**, de forma direta. Ele escreve rápido e com erros de digitação; entenda a
  intenção. Quando ele pede opinião ("como os profissionais fariam?"), dê uma recomendação, não um cardápio.
- Código, comentários, nomes e commits em português, no estilo do código em volta.
- Nomes no jogo como numa localização profissional: o que descreve é traduzido e soa natural ("Bosque do Lobo
  Branco", "Kalra, o Rei Troll"); nome inventado (Kalra, Varn, Theodore) fica como está.
- O motor decide as regras; a tela só desenha. Número que aparece na tela vem pronto do motor.
- Conteúdo é dado: habilidades (`rpg/habilidades.py`), talentos e passivas (`rpg/talentos.py`, com `mod`/`disparar`
  de `rpg/modificadores.py`), estados (`rpg/estados.py`). Nada de perguntar "tem o talento X?" no combate.
- Mudou algo visual? Suba o jogo num cenário e **veja** (Playwright tira captura); o Jean percebe pulos, sobreposições
  e textos cortados. `tests/navegador/cenarios.py` mostra como montar uma situação.
- Versão em `rpg/__init__.py`: correção sobe o último número, conjunto de mudanças sobe o do meio.

## Antes de cada commit

```
python -m unittest discover -s tests          # inclui o gabarito
python -m tests.gabarito                       # 24 partidas com semente fixa saem idênticas
python -m pyflakes rpg tests                   # ignore o aviso de import em rpg/eventos/__init__.py
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node tests/navegador/fumaca.mjs   # interface de ponta a ponta
```

**O gabarito é a rede de segurança.** Refatoração: tem que passar sem atualizar. Mudança de jogo de propósito:
`python -m tests.gabarito --mostrar` para ver as transcrições, confira que só mudou o esperado,
`--atualizar`, e diga no commit o que mudou e por quê. Em refatoração de combate, preserve a ordem das contas
de ponto flutuante e a ordem das chamadas ao sorteio (`rng`): trocar a ordem muda partidas.

Mexer em dificuldade: o ciclo está em [docs/COMO_CRIAR.md](docs/COMO_CRIAR.md) ("Um número de balanceamento"):
`python -m tests.equilibrio` e `python -m tests.replay` antes e depois, e as tabelas no commit.

Na nuvem, o Playwright costuma estar em `/opt/node22/lib/node_modules/playwright/index.mjs` (não rode
`playwright install`).
