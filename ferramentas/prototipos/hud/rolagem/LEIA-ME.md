# A rolagem narrativa no centro (plano 23, item 1.4: protótipo, nada no jogo)

Pedido do Jean: mais destaque e expectativa para o sucesso ou a falha dos testes de atributo (escolhas, diálogos e
eventos), preservando o dado, a tirinha e a animação atuais. Referências: Baldur's Gate 3 pela hierarquia (o teste,
o dado, o resultado) e Disco Elysium pela apresentação compacta sobre o cenário. Uma alternativa só.

## O que existe hoje (a fonte de tudo)

- **O motor** (`rpg/sistemas/testes.py`, `teste`): sorteia o d20, soma o bônus do atributo, aplica a dificuldade da
  região (`dificuldade`: +1 a cada dois níveis) e decide (20 sempre passa, 1 sempre falha). Chama
  `ui.rolagem(atributo, cd, d20, mod, total, sucesso)`; a ponte manda a mensagem `rolagem` com esses seis campos.
- **As parcelas do bônus** não vêm na mensagem, mas estão no estado: `heroi.testes[atributo]` (`mod` e `partes`, as
  mesmas da dica dos botões de escolha).
- **A tela** (`app/pagina.js`, `rolagem`): anexa a tirinha ao texto (o dado de 60 px, "Teste de Percepção", "d20 + 2
  contra dificuldade 12"), toca o dado e gira 950 ms com números ao acaso (enfeite; o resultado é o do motor). Pousa no
  d20, fecha a conta ("9 + 2 = 11 contra 12"), escreve Sucesso, Falha, Crítico! ou Desastre e toca o som. Espera
  `ritmo(650)` e só então a fila de mensagens segue para a consequência.
  - Pular (tecla ou clique) corta o giro; no texto instantâneo e ao refazer a página não há giro.
  - Com movimento reduzido, o dado gira do mesmo jeito (não há regra para isso).

## A proposta (`rolagem.js`, `rolagem.css`)

Troca só a função `rolagem` da página; recebe a mesma mensagem e não sorteia nada.

1. **O teste:** a área principal (`#palco`, sem as colunas do herói e do mundo) escurece, mais no meio que nas bordas
   (o cenário continua reconhecível). No centro: "TESTE DE PERCEPÇÃO", e logo abaixo "Dificuldade 12".
2. **A rolagem:** o dado de sempre, com o dobro do tamanho, gira e pisca. Embaixo, a tirinha em faixa de pincel: "d20 + 2",
   "precisa de 10 ou mais" e as parcelas ("Agilidade 3 +2").
3. **O resultado:** o dado pousa no d20 do motor (verde, vermelho ou dourado, como hoje). A tirinha fecha a conta
   ("9 + 2 = 11", "contra 12") e a faixa de resultado aparece:
   - **Sucesso:** faixa de marfim inteira, tinta escura; entra como um carimbo, e o contorno de latão, até então com
     trechos em falta, se fecha.
   - **Falha:** faixa de carvão rasgada no meio, o texto torto e caído; o contorno fica tracejado.
   - **Crítico!:** a de Sucesso, dourada. **Desastre:** a de Falha, mais caída.

   Os dois se distinguem pelo texto, pelo material (claro × escuro) e pela forma (inteira × rasgada), não só pela cor.
4. **A consequência:** no fim do tempo do resultado, o grupo desce e encolhe até a tirinha de sempre no texto, que
   aparece no lugar dela e fica como registro. Só então vem a consequência ("A tampa cede."): a fila espera, como hoje.

O pincel é o aprovado dos comandos e das escolhas (as pontas gastas, o meio ondulado e o grão de
`18-seletor-habilidades.css`), com um contorno de latão incompleto e o centro limpo. Os sons são os de hoje (dado;
sucesso, falha ou crítico).

**O ritmo é o de hoje:** 950 ms de giro e `ritmo(650)` no resultado, com a descida dentro desse tempo (até 220 ms). Não
há clique a mais.
- **Pular:** a tecla ou o clique corta o giro e agora também o tempo do resultado.
- **Texto instantâneo e refazer a página:** a tirinha de sempre, sem o centro.
- **Luta:** a rolagem de sempre (fora do escopo).
- **Movimento reduzido:** sem giro, sem entrada, sem carimbo nem rasgo animado e sem descida (o grupo aparece e sai).
  O tempo é o mesmo.

**Um número calculado pela tela:** "precisa de 10 ou mais" é `cd − mod` com a regra do 1 e do 20. Na integração ele
viria pronto do motor na mensagem (CLAUDE.md: número na tela vem do motor). As parcelas só aparecem se somam o `mod` da
mensagem.

## Como foi conferido (`fotografar.mjs`)

**O caso:** o baú abandonado (`bau_abandonado`), "Abrir com cuidado" (Percepção, dificuldade 12), forçado pelo cenário
`relatorio` com `EVENTO` e `SEMENTE`. Guerreiro de nível 1; a semente decide o d20 do motor (`fotografar.mjs procurar`
lista de 1 a 20). Sucesso por 1 (semente 11: 11 + 2 = 13 contra 12) e falha por 1 (semente 4: 9 + 2 = 11 contra 12).
Mesmos dados nos dois modos.

**A janela:** 1920×945, a área do jogo numa janela maximizada no monitor de 1920×1080 do Jean (sem a barra de tarefas e
a do navegador). Não houve bateria de resoluções.

| caso | resultado (histórico) | da tirinha à consequência |
|---|---|---|
| sucesso, atual | Percepção 13 contra 12 — sucesso (d20 11) | 1631 ms |
| sucesso, proposta | o mesmo | 1629 ms |
| falha, atual | Percepção 11 contra 12 — falha (d20 9) | 1627 ms |
| falha, proposta | o mesmo | 1631 ms |
| falha, proposta, movimento reduzido | o mesmo | 1628 ms |

- **Pular no meio do giro (um clique):** o centro some ~110 ms depois, com o resultado certo.
- **Texto instantâneo:** nada aparece no centro; a tirinha de sempre.
- **Erros na página:** nenhum.

**Capturas** (`capturas/representativas/`):
- `1-proposta-rolando.png`: o teste e a tirinha com o que é preciso tirar.
- `2-proposta-sucesso.png` e `3-proposta-falha.png`.
- `4-atual-falha.png`: a de hoje, no mesmo instante.

**A gravação** (`capturas/videos/proposta-sucesso-e-falha.webm`): o sucesso e a falha seguidos, para avaliar o ritmo.

**Para jogar:** `abrir.mjs [semente] [producao]` (`producao` abre sem o protótipo).

## Em aberto para a avaliação

- O grupo cobre o texto da cena por ~1,6 s (não há decisão pendente nesse tempo; a tirinha e a consequência ficam no
  texto depois).
- O "precisa de N ou mais" ajuda a expectativa, mas é informação nova na tela; pode sair se pesar.
- O tempo continua o de hoje; se a expectativa pedir mais, um alongamento curto só no resultado (não no giro) seria a
  próxima coisa a testar.
- Não conferido nesta rodada: outras resoluções e a HUD em geral (ficam para a consolidação).
