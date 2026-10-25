# A retirada do modo procedural (24/10/2026)

O Jean autorizou a retirada do modo procedural (o "Novo jogo" do mundo gerado): só a campanha existe. O pedido
separa o **modo de jogo** (a geração do mundo e o fluxo que só ele tinha) do **conteúdo reutilizável** (criaturas,
chefes, retratos, itens, habilidades, biomas e os sistemas compartilhados), que fica para a expansão da campanha.
Compatibilidade de save não é exigida: nada de migração para jogos antigos, mas os arquivos pessoais de save não se
apagam, e um save incompatível não trava a tela (uma mensagem curta).

## O levantamento (onde o procedural morava)

| parte | o que era | decisão |
|---|---|---|
| o título (`rpg/__main__.py`) | "Novo jogo" (o mundo gerado) e "Campanha" lado a lado; `--brando` mudava o modo do mundo gerado | um "Novo jogo" só, que começa a campanha; o modo (resgate ou hardcore) segue na criação; `--brando` sai |
| a criação (`Jogo.novo_jogo`) | sem região, o mundo gerado e o prólogo do reino (`introducao`); com região, o modo, a caixa do tutorial e a abertura | só o caminho da campanha (nome, classe, modo, tutorial); o prólogo do reino sai |
| a geração (`rpg/mundo.py`) | `gerar_mundo`: posições, biomas, estradas, nomes de vila e de lugar, três covis com guardião sorteado, a cidadela e o antagonista sorteado | sai a geração; ficam `vizinhos`, `distancias` e `nivel_regiao` (o nível declarado do lugar), que a campanha usa |
| os nomes sorteados (`dados.py`) | `VILA_QUALIFICA`, `VILA_LUGARES`, `SUFIXOS_LUGAR`, `NOMES_CIDADELA` (só a geração usava) | saem com a geração |
| o antagonista | `ANTAGONISTAS`, `ORIGENS_ANTAGONISTA` (o catálogo), `instanciar_antagonista` (a ficha de luta); o sorteio dele no mundo, o prólogo, a batalha final, a vitória e os eventos que falam dele | **fica o catálogo e a ficha** (chefes para a expansão); sai o que dependia do vilão sorteado (abaixo). A campanha não depende dele |
| os covis e a cidadela | o tipo de lugar `covil` (guardião, Sigilo, menu "Enfrentar"), a `cidadela` selada pelos três Sigilos, o salão do trono, o mapa com ☠/✓/♜ | sai o fluxo (lugar, menu, viagem selada, glifos, textos de chegada); **fica o catálogo de guardiões** (`GUARDIOES`, `ficha_guardiao`, `instanciar_guardiao`) e `receber_sigilo`, que a guardiã da campanha usa. O bioma `cidadela` (em `BIOMAS` e nos climas) fica como bioma |
| o legado (`rpg/legado.py`) | túmulo, estátua e baladas de heróis anteriores, gravados em `legado.json` e lidos no mundo gerado | sai (a campanha nunca o usou). O `legado.json` que já existe na pasta dos saves não se apaga e continua fora da lista de saves |
| a traição na batalha final (`comitiva.antes_da_batalha_final`) | Yara pode virar inimiga no salão do trono | sai com a batalha final; o resto da comitiva (missões pessoais, aprovação, conversas, a fogueira) fica |
| eventos | `visao_do_vazio`, `sonho_profetico`, `sussurros_do_vazio`, `pregador_do_vazio`, `veterano_cicatrizes` (já fora da campanha: falam do vilão sorteado), `eco_do_vazio` (só na cidadela), `sinais_do_guardiao` (só no covil); nos outros, os ramos que achavam covis ou o vilão (o diário do morto, o falcão, o cultista, Yara à noite, os rumores de fraqueza, de covil, de lenda e de lore) | saem os eventos que só existiam pelo vilão, pelo covil ou pela cidadela, e os ramos que nunca aconteciam na campanha (a lista vazia de covis não sorteava nada: a campanha não muda). O texto deles fica no histórico do git (o commit da retirada), se a expansão quiser algum de volta. A lista `EVENTOS_FORA` sai junto |
| ramos `if g.campanha` | textos e regras com uma versão para cada modo (Caspar com nome, o baú com um suprimento, o templo e a curandeira grátis, o diário com a missão, o resgate na casa de Marta...) | fica só a versão da campanha |
| saves | o arquivo do mundo gerado (sem `campanha` no mundo) | carregar recusa com uma mensagem curta ("é do mundo gerado, que saiu do jogo"); a lista de saves mostra o cartão como incompatível; nada é apagado |

## O que fica para a expansão (catálogo, sem uso novo)

Criaturas e famílias (`dados.FAMILIAS`, `inimigos.py`), os dez guardiões (`dados.GUARDIOES` e as fichas), os
antagonistas (`dados.ANTAGONISTAS`, `ORIGENS_ANTAGONISTA`, `instanciar_antagonista`), os biomas todos (inclusive
montanha, ruínas e cidadela, que a campanha de hoje não visita), itens, habilidades, talentos, estados, retratos e os
desenhos de lugar (`lugar-caverna`, `lugar-cidadela`). Nenhum deles foi distribuído pela campanha atual: nenhum
encontro, região ou história nova. O Barqueiro e os estudos de antagonista (arte) ficam como estão, sem integração.

## Os testes

- **O gabarito** jogava as 24 partidas no mundo gerado. Agora joga as mesmas sementes e classes na campanha, como o
  jogo começa (a abertura no Vau; o tutorial ligado nas partidas da tela gráfica, para o motor das orientações entrar
  na rede). As transcrições mudam todas, de propósito: o mundo é outro.
- **Os testes de unidade** que montavam um jogo com `iniciar(nome, classe)` ganham a campanha (o padrão novo). Os
  que testavam a geração, o covil, a cidadela, a batalha final e o legado saem com eles; os que testavam o catálogo
  (guardiões, antagonistas como ficha de luta) ficam.
- **A fumaça e os cenários** do navegador que dependiam do título com dois modos ou de um save do mundo gerado passam
  a conferir o título de um modo só e o cartão do save incompatível.
