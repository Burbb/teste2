# As escolhas da página em faixas (1.113.0)

Pedido do Jean: as faixas, que a 1.111.0 limitou ao menu de um lugar selvagem por escopo, passam a ser a apresentação
comum das escolhas narrativas e das ações da página. Sem lista de exceções por lugar, sem identificar pelo texto,
sem marca nova espalhada nos eventos; o conteúdo e as regras de cada opção não mudam.

## O mapa dos usos (antes de mudar)

`levantar.mjs` percorreu os cenários do jogo e registrou cada lista de escolhas da página (o `<ol class="escolhas">` de
`app/escolhas.js`), com a pergunta, as opções, as metas que o motor manda, os testes e o contexto
(`levantamento/levantamento.json`). O que aparece nessa lista, fora da luta e do título:

| Onde | Exemplos | O que as opções levam |
|---|---|---|
| lugar selvagem | Explorar, Acampar, Viajar; a ação da missão; o contrato | grupos Missão e Contratos, a marca à esquerda, os riscos da sala |
| viagem | "Para onde?" | o ícone do destino, textos longos (duas linhas em 1280×720) |
| vila | Passear pela vila, a ação da missão | os serviços ficam nos prédios (`vila.js`), fora da lista |
| eventos e diálogos | os enfermos, o mendigo, a criança perdida, a madeira, os bandidos, o mercador, Odette na estrada | nota (custo, tempo), o item que a opção gasta (ícone), o teste de atributo ("CAR +0", "VON +2"), indisponível com o motivo ("Ouro insuficiente", "Você não tem..."), a secundária ("Ignorar") |
| cenas da missão | a capela (salas, correntes, fundo) | a seta › de quem abre outra escolha, os riscos |
| criação do personagem | "Sua classe:" | texto simples (fica de fora desde a 1.113.1: antes da partida; terá a etapa própria) |

O que não usa essa lista (e continua com o próprio tratamento): a roda, o seletor e a mira da luta; o menu do título
e "Qual jogo?"; a confirmação e a janela do achado (por cima); a doca (os atalhos do sistema); os caminhos; os prédios
da vila; as telas desenhadas (o mercado, o Inventário, a fogueira, os serviços), cujos controles operacionais (comprar,
vender, equipar, dormir, tratar...) o jogo já tira da lista (`ACOES_OCULTAS`).

## A mudança

- `app/escolhas.js`: as escolhas narrativas ganham `.faixas`: as da partida em andamento, fora da luta (1.113.1; na
  1.113.0 a regra era "a lista que não é da luta nem do título" e pegava também a criação do personagem). A partida
  existe quando o motor manda o estado dela (só com herói e mundo): o título, a lista de saves e a criação ficam de
  fora pela função, sem exceção escrita. A marca `{"explorar": True}` do motor (1.111.0) saiu: não é mais preciso.
- `css/18-seletor-habilidades.css` ("as escolhas da página"): o acabamento aprovado (as pontas que escalam pela altura,
  os estados do seletor) e o que as outras listas pediam: a etiqueta do teste escura com a cor dela também no marfim
  (como as de risco), a seta › e a opção secundária legíveis nos dois fundos, a indisponível cinza riscada também sob
  o mouse, com o nome claro e riscado e o motivo no vermelho de perigo do seletor (o vermelho escuro sumia no carvão).

## Conferido (`fotografar.mjs`, `comparar.py`; a produção de antes num checkout do `31d56c0`)

14 casos reais (nada alongado nem simulado) em 1500×950 e 1280×720, antes e depois: o lugar selvagem, a viagem, a
vila, Passear, a fogueira (tela própria: nenhuma faixa ali), os enfermos com e sem poção, o mercador sem ouro, os
bandidos (teste de Carisma), Odette na estrada (teste de Vontade, nota, item gasto), a missão no canal, a Capela à noite
com e sem tocha, as correntes no ossuário (a seta ›).
- o conteúdo de cada opção (texto, tecla, teste, nota, riscos, motivo, ícone, seta, bloqueio, classes) igual antes e
  depois nas 26 comparações;
- nada cortado, nada sobreposto; cada ponto de cada opção à vista responde por ela; soltar o clique fora não escolhe;
  o Tab chega com o foco visível; a tecla do número escolhe a opção certa (o mendigo: o 3 é "Ignorar");
- contraste sobre o marfim: o teste 8,6, os riscos 8,6 a 8,8, a seta 12,7; o motivo da indisponível 7,1 (antes, 3,2);
- sem erro no console. As comparações em `capturas/comparacoes/`, algumas telas inteiras em `capturas/telas/`, as
  medidas em `capturas/relatorio.json`, os logs (a bateria, a suíte, a fumaça) em `capturas/logs/`.

## A correção 1.113.1 e o tempo das baterias

- **A regra pela função:** a 1.113.0 dava faixas à criação do personagem (uma lista da página fora da luta e do
  título). Na 1.113.1 a regra é a da função narrativa: as escolhas da partida em andamento. Conferido
  (`capturas/logs/conferencia-1.113.1.log`, só o depois em 1500×950: a troca só pode tirar faixas onde não há partida, e
  o conteúdo de cada opção já estava provado igual): os 13 casos com lista continuam em faixas; a fogueira sem lista; a
  tecla do número; o título e a classe na criação com 0 listas em faixas; sem erro no console.
- **O tempo:** cada cenário da bateria leva ~6 s (subir o cenário e gerar o mundo, chegar à lista, as fotos e as
  medidas; as esperas de 0,4 a 0,8 s cobrem a entrada das faixas, 150 ms mais 40 ms por opção, e o mouse). A bateria
  completa tem 14 casos × 2 janelas × 2 versões, mais a tecla e a criação nas duas versões: 60 cenários, ~7 min. A
  conferência da 1.113.1: 16 cenários, 1 min 28 s.
