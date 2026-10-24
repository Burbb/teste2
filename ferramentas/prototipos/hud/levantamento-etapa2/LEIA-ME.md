# Etapa 2: os componentes antigos que restam (levantamento, 24/10/2026; nada mudado)

Sobre a 1.204.1, no jogo de verdade a 1920×945: as telas e janelas da campanha abertas como o jogador abre
(`fotografar.mjs`: o Vau de teste, as teclas da doca, F1, H, os prédios, a viagem, a abertura guiada, o título) e as
faixas de passagem (`faixas.mjs`: o componente real, chamado só para desenhar). Em `capturas/` ficam as que sustentam o
levantamento (o Vau de referência, o Diário, os Talentos, os saves, a orientação e as faixas); as outras telas
conferidas, já substituídas, saem de novo pelo `fotografar.mjs`. A folha compacta em `folha-levantamento.png`. Critério de "antigo": o componente não tem acabamento da HUD de ferro nem da
pixel art aprovada (as regras dele só existem nos arquivos de antes da HUD, `css/01` a `13`) e destoa na tela.

**A etapa 2 não está concluída:** o livro entrou, mas restam as faixas e a orientação (abaixo), além do adiado.

## Já substituído (não volta à fila)

A subida de nível, as celebrações e a raridade (1.201.0), o d20 (1.202.0), o baú (1.203.0), o livro da capela (1.204.0);
e, de antes, a HUD de ferro inteira: os painéis, a doca, o mapa e o minimapa, o Diário (o cartão de papel é o mesmo
papel dos cartazes do mural, de propósito), o Bestiário, a Comitiva, o Inventário, o mercado, o mural, os serviços da
vila (o Templo), a Ajuda (F1), o Histórico (H), a janela de confirmação, a viagem com o d20, a fogueira e a luta.

## Ainda aparece na campanha e destoa

| componente | onde aparece | o problema concreto | alcance |
|---|---|---|---|
| **as faixas de passagem** (`telas/celebracoes.js`, `faixa`; CSS só em `06`) | "Vitória" no fim de **toda luta**; "Guardião derrotado!", "Você caiu/morreu", "Exausto", "Saindo da capela", "X se junta a você", "Mestre caçador" | uma tarja translúcida que cruza a janela inteira, por cima das colunas da HUD; o ícone é o sprite antigo de 16×16 (a espada, a caveira, a lua) e não a família de ícones; o subtítulo é miúdo (o "+10% de dano" do Mestre caçador); não conversa com as celebrações novas (o Estouro) | a mais frequente de todas: uma por luta, mais as passagens raras |
| **os quadros de orientação** da abertura guiada (`app/orientacao.js`; CSS só em `04` e `06`) | os primeiros minutos de quem começa: os quadros da abertura guiada (C1–C4, V1–V5, E1, T1, N1, B1, um por vez) | uma caixa lisa com fio dourado e um botão "Entendi" amarelo chapado (`filter: brightness` no hover): outra família de botão, ao lado dos botões de ferro | uma vez por jogador, mas é a primeira impressão |
| detalhes menores (`04`): a dica "qualquer tecla adianta o texto", o fio de leitura | o texto narrado | sem acabamento próprio; discretos | baixo; entram junto de um lote maior, se couber |

## Adiado (depende da retirada do procedural)

O título ("Novo jogo", "Campanha", "Carregar jogo"), a lista e as fichas dos saves, a criação de personagem: o menu do
título muda com a retirada do procedural (o plano 23 já diz isso).

## De etapas posteriores

O Grimório (a tela) e a árvore de Talentos: etapa 8, com os sistemas de habilidades e talentos.

## Recomendação: o próximo lote

**As faixas de passagem**, num lote só: Vitória, Guardião derrotado, Você caiu/morreu, Exausto, Saindo da capela, a
chegada à comitiva e o Mestre caçador. É o componente antigo mais visto da campanha (uma vez por luta), e o pedaço que
falta para as celebrações falarem uma língua só. Escopo: a faixa contida no palco (sem cruzar as colunas), a letra do
título e um subtítulo legível, os ícones da família (`Icones`, a espada e a caveira já existem), intensidade
proporcional (a Vitória comum discreta; o Guardião e a morte maiores), o movimento reduzido e os sons de hoje; o tempo
e o que cada uma diz ficam (vêm do motor). Protótipo com duas variantes, as fotos a 1920×945 e 1280×720, e a escolha do
Jean. **Depois:** os quadros de orientação (a mesma família de botões da HUD, sem mudar o roteiro da abertura).
