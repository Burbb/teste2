# O teste do pen.dev: compor no canvas e levar ao CSS (experimento)

**Pedido de Jean (17/10/2026):** testar o pen.dev no plano gratuito para ver se trabalhar numa composição visual
editável facilita chegar ao resultado e levá-lo ao CSS existente. O mesmo ajuste em dois fluxos: direto no
navegador e no CSS (A) e no canvas do pen.dev pelo MCP, depois no CSS (B).

**Nada disto entrou no jogo.** Os arquivos `a-ajuste.css` e `b-ajuste.css` só valem na bancada. O jogo, as regras e a
versão não mudaram.

## A composição

Duas faixas do seletor de Habilidades: Flecha Envenenada, com nome longo e custo duplo (10 de Foco e 1 flecha), e
Chuva de Flechas, indisponível ("Foco insuficiente"). Embaixo, a descrição. São três estados: a normal, a destacada e a
indisponível destacada. Duas janelas: 1280×720 (seletor de 684 px, descrição embaixo das duas colunas) e 1500×950
(800 px, descrição embaixo da coluna).

- `extrair.mjs` tira o seletor de verdade do jogo, no cenário tutorial com o Arqueiro sombra no nível 12, e grava em
  `dados/` o DOM, as posições e as descrições que o motor escreveu.
- `bancada.html` e `bancada.js` montam a composição parada com as folhas do jogo, sem cópia: `servir.py` entrega o
  static do jogo em `/static/`. Os estados são forçados repetindo as regras de `:hover` da folha com a classe
  `.x-destaque`. Parâmetros: `?versao=atual|a|b`, `?janela=` e `?estado=`.
- `fotografar.mjs` fotografa cada quadro em tamanho real e mede a folga entre o nome e o custo, as linhas do nome, a
  distância e a borda da descrição e os textos cortados. Grava em `capturas/` e em `capturas/medidas.json`.
- `comparar.py` monta as comparações `capturas/comparacao-*.png`.

Na 1.114.0, que entrou durante o teste, o seletor ganhou o arranjo lateral (sobre a ficha) para as lutas cheias de
janela baixa. O arranjo de duas colunas embaixo da arena, que é o desta bancada, não mudou.

## O ajuste pedido, igual nos dois fluxos

1. **Custo duplo:** cada ícone colado ao seu número e os dois pares separados. Hoje: "👁10⟋1", com o 10 encostado
   na flecha.
2. **Nome e custo:** pelo menos 12 px entre eles, sem quebrar nome que hoje cabe numa linha.
3. **Alinhamento:** uma borda esquerda só para o título, as teclas e a descrição. A descrição começava 12 px depois.
4. **Respiro na descrição:** 12 px até as faixas (eram 4), 10 px entre o fio e o texto (eram 7) e 28 px entre os
   dois blocos da janela baixa (eram 18).

## O resultado

Os dois fluxos chegaram ao mesmo CSS e às mesmas medidas (`capturas/medidas.json`):

| | hoje | A e B |
|---|---|---|
| 1280×720, Chuva de Flechas | 1 linha, folga 18 px | 1 linha, folga 17 px |
| 1280×720, Flecha Envenenada | 2 linhas (já era) | 2 linhas |
| custo duplo | pares a 2 px um do outro | pares a 7 px; ícone e número a 2 px |
| descrição até as faixas | 4 px | 12 px |
| borda esquerda da descrição | 14 px depois do título | alinhada ao título |

Não há texto cortado nem erro no console, nas duas janelas e nos três estados. O material (faixas, pontas, grão,
cores) é o mesmo nas três versões.

## Como foi cada fluxo

**A, direto no CSS (cerca de 7 min, duas rodadas).**
- A primeira rodada atendeu os quatro pontos, mas quebrou "Chuva de Flechas" em duas linhas em 1280×720 (o custo
  ficou mais largo). A medida da bancada pegou o problema.
- A segunda rodada foi feita ao vivo no navegador embutido, com três variações medidas em segundos: a coluna do
  ícone em 32 px e a grade em 8 px. Os 16 px da ponta direita do pincel continuam livres.

**B, no canvas do pen.dev (cerca de 18 min).**
- **Importação do localhost (30 s).** Trouxe camadas editáveis com a tipografia certa (Alegreya, tamanhos, cores), a
  descrição e o fundo. Perdeu justamente o acabamento:
  - as pontas de pincel (a máscara): a faixa virou retângulo;
  - a inclinação de 2°;
  - o paralelogramo da tecla, e o número saiu do lugar;
  - o grão do pincel, que virou um retângulo preto opaco e deixou a faixa destacada ilegível
    (`capturas/comparacao-importacao.png`).
- **Reconstrução (cerca de 9 min).**
  - `pecas.mjs` renderiza a faixa e a tecla de cada estado com o CSS do jogo, como PNG transparente, em
    `images/pecas/`.
  - No canvas: um componente "Faixa" reutilizável, com a pincelada e a tecla como imagem, e a tecla, o ícone, o
    nome, o motivo e o custo como camadas com layout.
  - 25 variáveis tiradas do CSS: cores, fonte e as folgas da composição.
  - Seis quadros (2 janelas × 3 estados) feitos de instâncias do componente.
  - Fidelidade: cerca de 95% dos pixels iguais à foto do jogo (diferença acima de 40 em 3% a 7% dos pixels). As linhas
    da descrição ficam até 12 px mais baixas em 1500×950. O "veneno" em verde não existe, porque o `.pen` não tem
    trechos de cor dentro de um parágrafo. A textura do fundo fica esticada, não repetida.
- **O ajuste no canvas (cerca de 5 min).** Mudar as variáveis foi direto. Três defeitos apareceram no caminho:
  - reorganizar o componente (o custo em dois "pares") **apagou as personalizações das instâncias** daquelas peças:
    a Chuva mostrou o custo da Flecha, e o custo da faixa destacada ficou claro sobre marfim;
  - uma atualização que usava uma variável criada na mesma chamada se perdeu sem aviso;
  - a descrição deslocada pela margem interna ficou sem largura e o texto saiu letra por letra (erro de montagem
    meu; o pen.dev não acusou).
- **Para o CSS (cerca de 2 min).** As variáveis viraram as mesmas regras do fluxo A (`b-ajuste.css`). O par do custo
  não tem invólucro no HTML do jogo e foi imitado com flex e margem, como no A.
  - A exportação de código do pen.dev (`exportado/`) não serve além de referência: `div` com estilo inline, sem
    classes, cores fixas em vez das variáveis e a fonte carregada do Google Fonts, o que não funciona num jogo
    offline.

Atenção ao comparar os tempos: o fluxo A veio primeiro, então no B eu já sabia que a coluna do ícone em 32 px evitava
a quebra do nome. O B teve essa vantagem e, mesmo assim, levou mais que o dobro do tempo.

## Instalação e ambiente

- **Instalação:** download (384 MB) em 21 s e instalador em 66 s (Pen 1.2.18, Windows, assinatura válida da High
  Agency Inc.). Backup das configurações do Claude em `C:\Users\Jean Wress\Tools\backups-config\`.
- **MCP:** servidor `pencil` (`mcp-server-windows-x64.exe --app desktop`) registrado só neste projeto, no escopo local
  do Claude Code, ao lado do `aseprite-bridge`, que foi preservado. O próprio botão do pen.dev escreveria na
  configuração global.
- **Sessão já aberta:** uma sessão do Claude Code não carrega um servidor configurado depois de começar. Por isso o
  teste usou `mcp.mjs`, um cliente MCP mínimo (stdio) com as mesmas ferramentas: `browser`, `execute`,
  `get_app_state`, `get_style` e `read_skill`. Uma sessão nova já o terá direto.
- **Bloqueios:**
  - a tela de boas-vindas do app ("Connect your account") trava as capturas e a importação do navegador interno
    ("A capture is already running") até ser fechada. Isso precisou de Jean. Não é preciso conectar conta: a conta
    serve ao agente interno do pen.dev, não ao MCP;
  - o documento ativo é o que está aberto no app: o `filePath` não abre outro arquivo, e o app não troca de documento
    pela linha de comando. O trabalho foi feito no documento aberto e salvo aqui no fim (`seletor.pen`, com
    `images/` e `fonts/`), lendo a árvore pelo MCP, porque o app guarda as edições na memória até alguém salvar;
  - `TakeScreenshot` sai reduzido; para conferir em tamanho real, `Export` em PNG com `scale: 1`. O relatório de corte
    com instâncias expandidas acusou camadas visíveis como cortadas e não serviu.
- **Custo:** plano gratuito. Nenhum serviço pago. O MCP de um agente externo gasta um "dia de agente" (5 por mês no
  gratuito).

## Avaliação

- **Fidelidade ao visual aprovado:** a importação sozinha não serve (perde a tinta). A reconstrução com as peças do
  jogo como imagem fica fiel, com as perdas acima.
- **Experimentar e corrigir:** no canvas, mudar uma folga é trocar uma variável, e todas as instâncias acompanham. Mas
  o CSS ao vivo no navegador embutido foi mais rápido e mediu o resultado real na hora (a quebra do nome, a folga).
  Mudar a estrutura do componente no canvas foi frágil.
- **Levar ao CSS:** tradução manual, número por número. O canvas não sabe as regras do jogo: o par do custo, a
  posição da descrição calculada pelo `escolhas.js` e os 16 px reservados à ponta do pincel.
- **O que só o canvas deu:** uma composição que Jean pode abrir e mexer à mão, com nomes legíveis ("Faixa", "Custo",
  "Par A") e variáveis com os nossos nomes. Isso não foi testado: neste teste quem mexeu fui eu, pelo MCP.

**Recomendação: restringir.** Não adotar o pen.dev como etapa do fluxo de composição da HUD. Para mim, ele somou uma
tradução e não tirou retrabalho: o CSS ao vivo com a bancada e as medidas chegou ao mesmo resultado em menos da metade
do tempo. Vale manter instalado, sem custo, para um uso só: quando Jean quiser propor um arranjo mexendo à mão.
O próximo teste, se interessar, é esse: Jean abre `seletor.pen`, mexe em algo, e eu leio a mudança e levo ao CSS.
Se não houver interesse, o pen.dev pode ser desinstalado (Configurações do Windows → Aplicativos → Pen) e a entrada
`pencil` removida do projeto.

O que fica útil daqui sem o pen.dev: a **bancada** (um componente parado, com as folhas do jogo, os estados forçados
e as medidas) é o que fez o fluxo A ser rápido. Ela serve para outros ajustes de composição.

## Como refazer

```
python ferramentas/prototipos/hud/pen-composicao/servir.py          # deixe rodando
PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/pen-composicao/fotografar.mjs
python ferramentas/prototipos/hud/pen-composicao/comparar.py
```

`extrair.mjs` refaz `dados/` a partir do jogo e `pecas.mjs` refaz as peças de `images/pecas/`. `seletor.pen` abre no
pen.dev (File → Open) e tem a importação crua, o componente "Faixa" e os seis quadros já ajustados.
