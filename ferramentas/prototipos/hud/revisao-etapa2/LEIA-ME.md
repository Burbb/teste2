# Etapa 2: a revisão delimitada para o fechamento (25/10/2026, sobre a 1.209.0)

O objetivo: concluir a frente da etapa 2 do plano 23 ("Telas de leitura, criação, carregamento e celebrações"), não
uma renovação geral. Cruzei o plano (o escopo da etapa 2 e o levantamento de 24/10/2026,
`../levantamento-etapa2/LEIA-ME.md`) com o jogo de hoje: as telas da campanha abertas como o jogador abre, a 1920×945 e
a 1280×720 (`fotografar.mjs`, o roteiro do levantamento nas duas janelas, com uma auditoria do foco pelo Tab), mais as
conferências próprias de cada entrega recente (`telas-iniciais/auxiliares/criacao.mjs`,
`carregar-jogo/auxiliares/conferir.mjs`, `orientacao/auxiliares/gestos.mjs`).

## A · Entregas concluídas

| item do plano | no jogo desde |
|---|---|
| a subida de nível, as celebrações e a raridade (o Estouro como padrão; o Relicário implementado, sem tela) e as seis identidades de especialização | 1.201.0 |
| o d20 (o Clássico, o Marfim e o Vidro, à escolha na Ajuda) | 1.202.0 |
| o baú | 1.203.0 |
| o livro narrativo da capela | 1.204.0 |
| as faixas de passagem (a original refinada) | 1.205.0 |
| os quadros de orientação (a R) e o aviso de ponto de talento (a R) | 1.207.0 |
| o título (mantido como estava, depois da retirada do procedural) e o save recusado (a mensagem curta) | 1.206.0 |
| a criação de personagem em etapas (a R2) | 1.208.0 |
| o Carregar jogo e os cartões dos saves (a R) | 1.209.0 |
| os componentes antigos restantes, por evidência | revistos aqui: nenhum outro destoa nas telas da etapa |

## B · Defeitos que impediam o fechamento (reproduzidos antes de corrigir)

| defeito | como se reproduzia | situação |
|---|---|---|
| depois de abrir um save que não abre, a janela do Carregar jogo ficava na página com a altura cheia e empurrava a mensagem ("Este save não abre…") e o Continuar para fora da vista, a 1920 e a 1280 | Carregar jogo → o save do mundo gerado (conferido em `carregar-jogo/auxiliares/conferir.mjs`: a mensagem e o Continuar à vista) | corrigido na integração da 1.209.0, antes do commit dela: respondida a lista, a janela sai da página |
| a dica do nome cortado sumia quando o foco do teclado levava a lista a rolar (a rolagem fecha as dicas) | 22 saves, as setas até o nome longo | corrigido na mesma integração: quando a lista para, a dica volta |

Não achei outro defeito funcional ou de leitura nas telas da etapa: nada cortado ou sobreposto nas duas janelas; o foco
visível em todas (a auditoria marcou as opções da página e do título, mas o foco delas é a pincelada clara e o número
aceso, conferido nas fotos com e sem o foco: falso alarme da auditoria, que só reconhece anel e sombra); nenhuma
dependência de protótipo no código do jogo (só comentários que apontam a origem); nenhuma transição mostrando acabamento
antigo.

## C · Opcionais e reservados

- **Opcional (baixo):** a dica "qualquer tecla adianta o texto" e o fio de leitura do texto narrado, sem acabamento
  próprio (o levantamento de 24/10 já os dava como discretos). Ficam para um lote maior, se couber.
- **Medido e registrado, sem mudança (decisão do Jean):** a lista de saves cresce ~9 ms por save no motor (~0,2 s com
  22); sem índice ou resumo paralelo neste lote.
- **Adiados por decisão do Jean (fora do escopo da etapa 2):** o botão "Continuar" da subida de nível; os tempos das
  faixas de passagem e adiantá-las; o menu completo de configurações (com ele, a escolha Estouro ou Relicário e o d20,
  hoje na Ajuda); a compatibilidade por migração dos saves do mundo gerado.
- **Reservados para outras etapas:** o Grimório e os Talentos (a etapa 8, com os sistemas de habilidades e talentos);
  a revisão narrativa e a expansão da campanha (a etapa 9); retratos adicionais por classe e recoloração na criação
  (em aberto, sem pedido).

## A situação: a etapa 2 concluída no escopo acordado

Os critérios da etapa 2 estão atendidos: as telas de leitura, criação, carregamento e celebrações do plano estão na
linguagem aprovada, e os defeitos achados na revisão foram corrigidos. **Exceções explícitas:** as da lista C (os
adiados e os reservados), que não são esquecidas nem resolvidas aqui.
