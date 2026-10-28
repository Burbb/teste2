# Protótipo: reforço, materiais, desmontagem e encantamento (laboratório)

A demonstração jogável da seção 5 do [25](../../../roadmapIDEIAS/25-ETAPA4-REFORCO-E-ENCANTAMENTO.md) (26/10/2026).
**Não é integração.** O jogo de produção não carrega esta pasta (um teste confere); a forja, o mercado e os saves do
jogo não mudaram. Os números são hipóteses desta rodada, não balanceamento.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/reforco/demo.py` na raiz). O jogo de sempre abre no
navegador num **save temporário** (uma pasta nova a cada vez; os saves pessoais não são lidos nem tocados): o Guerreiro
no nível 4, no Vau, com Morel e Odette, 380 de ouro, dois baús e as peças dos exemplos. Feche a janela do terminal
para parar. A 18ª não tem folhas: tudo se compara na própria demonstração, pelo **Painel de testes** da faixa do
alto (seção da 18ª). Folhas da 17ª: `folha-acabamento-armaduras.png`, `folha-paleta.png` e `folha-telas.png`. Das
versões anteriores: `folha-botoes.png` (16ª, A × B), `folha-comparacao.png` e `folha-estados.png` (15ª),
`folha.png` (o resultado do reforço) e `folha-acabamento.png` (o acabamento do +1 ao +12). A especificação do sistema
inteiro: [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md).

Só nesta execução, `demo.py` troca a forja (o balcão novo), o baú (que pode dar fragmento ou essência), a seção
"Materiais" do Inventário, a venda da peça reforçada, a ficha das peças nas telas (as gravações) e liga os efeitos das
gravações na luta. O resto é o jogo: o Inventário do grupo, o mercado, a luta, a estrada.

## 18ª versão: as armaduras A, B e C, a desmontagem fluida, remover a gravação, as placas da bancada e o gesto do ferreiro (em avaliação)

**O sistema inteiro está no [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)** (3.3, 9, 10, 11 e 12). Chances,
custos, limite +12, distribuição de essências e regras de transferência não mudaram. A nova forja continua só aqui.
Som adiado. Sem vídeos nem folhas: as candidatas estão na demonstração, e o **Painel de testes** troca cada uma na
hora (fica lembrado neste navegador).

### No Painel de testes ("Comparação visual")
- **Armaduras +9 a +12:** A · Alternadas, B · Gradual, C · Secundário (as candidatas), Feixe 17ª e Veio (para
  comparar). Embaixo, a **vitrine**: as cinco peças que o herói veste (cabeça, peito, mãos, pernas, pés), cada uma do
  +8 ao +12, no tamanho de uso ou ampliadas (2×), com a alternativa escolhida. Nas telas do jogo (a esteira da forja, o
  Inventário, o Equipado), "Níveis altos (teste)" dá peças de +9 a +12.
- **Botões e painéis:** Como no jogo × Placas da bancada (a candidata de interface).
- **Ferreiro (recarrega):** Como no jogo × Gesto candidato (a página recarrega; a tira do ferreiro vem da candidata).
- **Festa da especialização: Mostrar:** a festa "Você agora é Paladino" com dados de exemplo, para ver o Continuar
  dela (só a tela; a partida não muda). A escolha de verdade (Olhar de perto, Confirmar e essa festa): na taverna,
  Dormir até o amanhecer, com o herói no nível 4 ainda sem especialização (o cenário inicial da demonstração; o painel
  "Aplicar e reiniciar cenário" volta a ele).

### Armaduras do +9 ao +12: três alternativas
O feixe da 17ª ficou discreto demais. As três partem da faixa do +8, que **fica exatamente como está** (a mesma força,
3 pixels e o pixel claro atrás, uma faixa a cada 18 diagonais, o passo de 70 ms), e a passada periódica do reflexo
volta, na cor da alternativa (A: uma cor por passada; B: a cor do momento; C: a principal com o fio na secundária):
- **A · passadas alternadas:** uma cor por faixa, na ordem do nível (+9 rubi, âmbar; +10 mais o azul; +11 mais a
  esmeralda; +12 mais o violeta);
- **B · cor gradual:** todas as faixas na mesma cor, que passa devagar para a seguinte (três faixas por cor, ~3,8 s);
- **C · reflexo principal e secundário:** a faixa na cor principal e, logo atrás, um fio de 1 px (2 no +11 e +12) na
  secundária: as duas cores da celebração do nível.
O nível cresce pelas cores, pela força (+11, +12) e pelos pontos de brilho (1 a 4, como nas armas); o +12 tem o pixel
claro em marfim. Armas e joias não mudam; a celebração (aceita por enquanto) também não. Com movimento reduzido,
paradas (conferido: dois quadros iguais). Cada passo é um quadro pronto, como o veio (sem mistura no CSS): a 125%, as
camadas caem nos mesmos pixels da peça.

### Desmontagem: a fluidez
As causas (o efeito a 15 quadros por segundo; as animações do CSS em degraus; os redesenhos da volta do motor parando
o efeito no meio e recomeçando as animações) e a correção estão no 27, seção 9. Medido no navegador: 56 quadros com
efeito, 16 ms entre eles (no máximo 30); o +N aparece quando os fragmentos chegam (~0,5 s), o saldo troca logo depois e
acende uma vez; a cobrança é uma só (o resultado 1, fragmentos 20 → 30, com clique duplo na confirmação). Com movimento
reduzido, o recebido aparece parado: "+14" e "Fragmentos: 34" com o contorno de latão.

### Remover a gravação (candidata)
No Encantar, escolha um sulco ocupado: "Remover gravação" embaixo dos sulcos. A confirmação no pé ("Remover? Brasa I
se perde."), a prévia do que cai e, ao confirmar, o sulco vazio. A essência se perde, nada volta, não custa nada; um
pedido só (o motor recusa o repetido e o de uma gravação que mudou). A regra e o que se recalcula: 27, seção 3.3.
Testes: `TestRemover` (3).

### Placas de metal da bancada (candidata de interface)
`tela/placas.css`, só com "Placas da bancada" no painel. A regra (o que se aperta tem espessura; o que informa é
fixado com rebites; número e tecla em nicho), os estados e os componentes: 27, seção 10. O botão A de produção
continua no jogo como está; esta candidata não é aplicada lá.

### Ferreiro: o gesto do martelo (candidata)
`ferramentas/prototipos/hud/forja/h2/candidata_gesto.py` grava `candidata-gesto/ferreiro.png` (a candidata da 17ª
continua em `candidata/`). A leitura de guidão vinha da cadeia ombro → cotovelo → punho → cabo: na preparação, o braço
ia para a frente na altura do ombro com o antebraço e o cabo em pé; a mão pegava o cabo pelo meio (um toco de 5 a 7 px
atrás do punho); a descida era quase vertical. Agora a pegada fica na ponta do cabo; na preparação, o cotovelo sobe
na diagonal à frente do rosto e o martelo fica armado atrás da cabeça (sem passar da altura de antes); na descida, o
braço estica para a frente e o martelo vem em arco até o mesmo contato. Os apoios, o corpo, o enquadramento e o ritmo
não mudam. Mantém a nuca e o calcanhar da bigorna da 17ª. Nada integrado: a fonte `aseprite/forja-h2.aseprite` e o
jogo não mudaram.

### Conferido
- 1920×945 e 1280×720: a vitrine, a remoção (o fluxo inteiro, com teclado: Enter abre a confirmação com o foco no
  Cancelar, Esc fecha, o foco volta ao Remover), as placas (a taverna, a entrada da forja, os Caminhos, o aviso de
  talento, a doca, o Inventário, a Comitiva; a Encruzilhada e a festa no cenário "encruzilhada" com a candidata
  injetada). A 1280, o balcão da taverna com as placas fica 7 px menor que hoje (o Voltar à vila não
  desce).
- Estados das placas um a um: normal, mouse, pressionado e foco (Voltar à vila, aviso de talento, abas, Caminho, Olhar
  de perto, Confirmar, Continuar), selecionado (a aba, o atalho da tela aberta) e indisponível (o serviço sem ouro).
- Movimento reduzido: as armaduras paradas, o recebimento parado. 125%: a vitrine das armaduras (as camadas alinhadas
  à peça).
- O ferreiro candidato no tamanho de uso, na forja da demonstração (a cena inteira, 30 quadros seguidos).
- **Não conferido:** o Bestiário com criaturas (a demonstração começa sem nenhuma; o cartão fixado segue a regra dos
  cabeçalhos) e o Caminho fechado (o painel do mundo se redesenha e desfez a marca posta à mão para a captura).
- **O pixel azul** continua registrado como não reproduzido (17ª), sem declarar resolvido.

## 17ª versão: a vida na entrada, o feixe nas armaduras, a celebração ligada ao acabamento, o recebimento e o botão A (histórico)

**O sistema inteiro está no [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)** (6, 9, 10, 11 e 12). Chances,
custos, limite +12, distribuição de essências e regras de transferência não mudaram. A 16ª está em
`tela/historico/v16` (`?tela=v16`). Folhas desta versão: `folha-acabamento-armaduras.png` (o veio anterior × o feixe
candidato, três quadros, com o +8 de referência na primeira coluna), `folha-paleta.png` (a celebração anterior × a
candidata do +9 ao +12, a 1,25 s e a 2,3 s) e `folha-telas.png` (a entrada com os quatro serviços, o atalho do
Inventário dentro da forja e a desmontagem: a prévia e o recebido).

### O defeito: vinte de vida ao entrar no ferreiro
Entrar no ferreiro do protótipo tirava vida (Jean 65 → 60, Morel 85 → 79). **Causa:** a ficha das peças compara com o
que se veste (`comparar`, que veste e desveste a peça para medir a diferença); sem a peça, o máximo de vida caía e a
vida era cortada nele, e ao vestir de volta o máximo voltava, mas a vida não. **Correção na origem:** a comparação
hipotética guarda a vida de quem veste antes de mudar e a repõe depois de desfazer. **Teste pelo caminho real**
(`TestEntrarNaForja`): entra pelo ferreiro da demonstração e sai; falha sem a correção (65 → 60 e 85 → 79). A forja de
produção não tem o defeito (três entradas e saídas sem mudar vida, máximo, dia nem período).

### Visual (candidatas e aprovado)
- **Botão A [aprovado]:** o B saiu do protótipo; a forja usa o A também nas abas, nos donos, nas famílias, nos tiers e
  nos sulcos. Na produção (1.214.0) ele foi aplicado em separado (`rpg/web/static/css/27-ferro.css`), sem depender
  desta pasta: os Caminhos, os serviços dos lugares, a doca, o Bestiário, a Comitiva, as abas e os botões do
  Inventário.
- **Armaduras do +9 ao +12 [candidata]:** o feixe: linhas diagonais de 1 px na força do veio do +8, estreito, com as
  cores do nível (+9 rubi e âmbar, uma cor a mais por nível até as seis do +12). O A e o B da 16ª foram rejeitados; o
  +8 não mudou. O veio anterior fica no painel ("Feixe" × "Veio anterior").
- **Celebração do +9 ao +12 [candidata]:** as cores ligadas ao acabamento da peça (+9 rubi e âmbar; +10 laranja e
  azul; +11 âmbar e esmeralda; +12 âmbar e violeta). A paleta da 16ª (violeta e ouro) foi rejeitada. O ouro do +12 da
  16ª fica no painel ("Ouro ref. +13") como referência, caso um dia exista o +13; nenhum +13 foi criado.
- **Desmontar:** depois da transformação, o encaixe fica vazio, o título diz "Desmontado" e, ao lado do material, o
  que chegou ("+10") e o saldo novo ("Fragmentos: 30"), parados no movimento reduzido. A prévia ("×10") e o recebido
  se distinguem pelo sinal, pelo encaixe vazio e pelo título.
- **Entrada:** os quatro serviços numa grade 2 × 2.

### Texto
- **Encantar:** o limite aparece no valor ("Brasa 40% → 60% · limite"); "Limite 60%: 8% não valem" saiu. Só quando
  nada muda porque já estava no limite, a nota curta "Brasa já está no limite (60%)".
- **Substituir:** a confirmação numa frase ("Substituir? Carrasco I se perde."), sem repetir a perda na nota.
- **Materiais:** o título é só "Materiais" (a explicação saiu); a dica do material vale também no "Requer:".
- **Recompensa:** o texto em cima do "Ir para a vila" saiu.

### Fora do protótipo (produção 1.214.0, em commits separados)
A doca dentro das telas de serviço (o pedido do Jean: o Inventário dentro da forja), o preço do Mercado à vista sem
ouro, o nível dos companheiros na luta, o achado nítido a 125%, os textos (sem "brejo", sem "Curas param em N", sem os
rodapés que explicam o clique) e o acabamento A. Registro no [00](../../../roadmapIDEIAS/00-COMECE-AQUI.md).

### Não reproduzido: o pixel azul
O pixel azul que ficava perto do item depois do achado não apareceu: os dois caminhos (equipar e guardar) a 100% e
125%, a varredura dos pixels da página e a do DOM depois de fechar a janela (o canvas da festa sai com ela).
Hipóteses: um estilhaço da festa desenhado no último quadro antes de o canvas sair, numa máquina mais lenta; o
contorno do +N (azul no +6) de uma dica que ficou para trás. Se voltar, uma captura com a escala do Windows ajuda.

### Conferido
- **Testes do protótipo (62).** Suíte do jogo (728), gabarito, pyflakes e a fumaça do navegador na versão final.
- **A 1920×945:** o atalho Inventário da doca dentro da forja abre o "Inventário do grupo"; a tira das armaduras (o
  anterior, o feixe e o +8 na mesma peça e no mesmo fundo); a celebração candidata × anterior; a desmontagem com o
  recebido. O acabamento A na produção a 1920 e a 1280 (antes e depois com os mesmos dados).
- **Não conferido nesta rodada:** a bateria de resoluções e escalas inteira (só os componentes afetados), e os estados
  de mouse, pressionado e foco de cada componente A da produção um a um (vistos no Caminho e nos atalhos).

### Roteiro (uns 5 minutos)
1. **Ferreiro:** veja a vida no topo antes e depois de entrar e sair (não muda). A entrada tem os quatro serviços 2 × 2.
2. **Dentro da forja, doca → Inventário:** volta ao lugar e abre o Inventário do grupo.
3. **Níveis altos (teste) → Reforçar** as armaduras de Jean (+9 a +12): o feixe; troque no painel para o veio
   anterior e compare com o +8.
4. **Sucesso (teste):** reforce a arma da bolsa do +8 ao +12 com a celebração candidata, depois a anterior e o
   "Ouro ref. +13".
5. **Essências (teste) → Encantar** a arma de Jean, 3º sulco, Brasa II: "Brasa 40% → 60% · limite"; Substituir: a
   pergunta numa frase.
6. **Desmontar** uma peça da bolsa: a prévia "×N" e, depois, "+N" com o saldo novo.

## 16ª versão: ganho real em todo reforço, formatos comuns, candidatas visuais e o painel de testes (histórico)

**O sistema inteiro está no [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)** (1.1, 1.2, 3.3, 9, 10 e 11).
Chances, custos, limite +12, sucesso +1 e falha −1 sem quebra, tiers, requisitos e transferência não mudaram. A 15ª
está em `tela/historico/v15` (`?tela=v15`). Folhas desta versão: `folha-botoes.png` (A × B nos mesmos estados e o
preço pequeno e grande), `folha-acabamento-armaduras.png` (A × B, quatro quadros seguidos de cada peça),
`folha-paleta.png` (anterior × candidata do +9 ao +12, mesma peça e mesmos instantes) e `folha-telas.png` (as quatro
abas a 1920×945 e 1280×720, com as confirmações).

### Regra (motor)
- **Todo sucesso melhora a peça de verdade.** A causa do "passa níveis sem ganho": o ganho de cada linha era
  arredondado a inteiro. Varrendo o gerador (todos os espaços, níveis 1 a 13, quatro raridades, +0 a +12), nenhum passo
  tinha ganho zero na conta; o arredondamento escondia o ganho em um quarto a um terço dos passos de acessórios,
  elmos, luvas e botas (o Cajado de Ferro do +10 ao +11: Poder 8,6 → 9,2, os dois viravam 9). Agora cada propriedade
  tem a precisão que o motor usa: Ataque, Poder, Defesa, Agilidade, Espinhos, Vida por turno e Vida por abate com uma
  casa; Crítico e Roubo de vida em décimos de ponto; Vida e Mana inteiras. Continua em forma fechada da peça original,
  arredondada uma vez (cair e subir volta ao mesmo número). Um passo que ainda não mudaria nada (só peças de Vida e Mana
  chegam perto) adianta um degrau na linha mais perto dele; nunca mais de um degrau à frente da conta. A principal da
  arma continua com +1 por passo até o +4.
- **A cadeia inteira:** a casa das peças chega aos atributos do herói e dos companheiros (a ficha mostra "Defesa
  20,8") e à luta (dano, defesa e esquiva usam o número com a casa). Espinhos, Vida por turno e Vida por abate são pontos
  de vida inteiros: a fração se acumula a cada disparo (2,6 por turno cura 2, 3, 3, 2, 3…). Sem peça fracionária, os
  números são os de antes.
- **Peça toda no teto:** nenhuma do gerador chega lá (o teto é por peça, 15% de Crítico e 10% de Roubo de vida). Se
  chegar, o reforço é recusado sem cobrar ("Sem ganho: Crítico no máximo desta peça."). Proposta, sem implementar: a
  peça nessa situação passa a crescer pela linha fixa mais próxima da base (Ataque na arma, Defesa no resto).
- **Reforço sem portador:** classe e nível restringem vestir, não o serviço. A peça de arqueiro na bolsa de um grupo
  sem arqueiro recebe reforço, com a prévia vinda da própria peça; vestir continua recusado.

| Peça | +0 | +4 | +8 | +12 |
|---|---|---|---|---|
| Barbuta de Ferro (nível 4) | Defesa/Vida 1/2 | 2/4 | 2,7/5 | 3,2/6 |
| Cajado de Ferro do +10 ao +11 (Poder 3, nível 2) | — | — | — | Poder 9,2 → 9,8 (antes: 9 → 9, prévia vazia) |
| Aljava Rasgada (nível 2) | Agilidade/Ataque 1/1 | 2,5/2,5 | 3,5/3,5 | 4,2/4,2 |
| Aro do Carniceiro (nível 3) | Vida por abate 5 | 11 | 15 | 18 |
| Brasa Faminta (nível 8, raro) | Agilidade/Crítico 4/4% | 6,4/5,5% | 8/6,5% | 9,2/7,2% |

### Texto e HUD
- **Formatos comuns** (a skill `texto-regras-fenda`, "O fluxo de toda entrega com texto novo"): "Requer:" com cada
  material como disponível/necessário ("14/2") e o nível no mesmo grupo, vermelho quando impede; o ouro dentro do
  botão; a confirmação sem mover a ação. Componentes `requerHtml`, `botaoAcao` e `peAcao`, usados nas quatro abas.
- **Encantar:** "Requer: [Brasa II] 3/1 · Nível 5" no lugar de "Requer nível 5 (Jean: 4). Na bolsa, pode gravar.";
  "Carrasco 15% → —" no lugar de "Carrasco nesta peça"; o total de quem veste só quando o limite corta; na bolsa, "A
  peça passa a requerer nível 9" quando sobe o requisito. Saíram "tem N" e os custos espalhados.
- **Etiqueta do tier:** I, II, III numa placa escura de aresta de latão no canto de cima à direita (a linguagem do +N),
  maior e fora do desenho; a quantidade no canto de baixo.
- **Fichas:** "Brasa I ×2", "Brasa II + Brasa I", a descrição com o valor somado embaixo; cada sulco segue na fila.
- **Botões (candidatas, sem escolha):** A · ferro encaixado (planos chapados, cantos em degrau, luz curta na aresta de
  cima, base escura) e B · ferro com presilhas de latão. Normal, hover, pressionado (a face afunda e o rótulo desce 1 px
  dentro do botão), foco (anel de latão por dentro) e indisponível. Aplicadas no Reforçar, Gravar/Substituir,
  Transferir, Desmontar, Cancelar, OK e Fechar da forja. Outros usos do jogo, para quando uma for escolhida: as
  confirmações (`app/escolhas.js`, Sim/Não e perigo), a Ajuda (`app/orientacao.js`, as chaves e o dado), a
  especialização (`telas/especializacao.js`, Confirmar e Olhar de perto), o achado (`celebracoes/festa.js`), as
  celebrações (`estouro.js`, `relicario.js`), os Fechar das janelas grandes (Histórico, Mapa, Talentos, Grimório) e o
  mercado (comprar e vender: o caso do preço dentro do botão).
- **Preço dentro do botão:** "Transferir · [moeda] 335", o valor numa área de largura fixa (de 5 a 4600 o rótulo não
  se move). Na confirmação, o Transferir fica no mesmo lugar e tamanho (medido: 330 × 47 px antes e durante a 1920,
  268 × 38 a 1280); o Cancelar aparece num espaço reservado à direita. Desmontar e Substituir seguem o mesmo pé.
- **Referências examinadas:** a janela do ferreiro do Grim Dawn (a captura do wiki oficial, aberta e vista): o
  material como "9 / 3" (tem/precisa) num encaixe, o custo num nicho próprio acima do botão "Combine". Lost Ark: só a
  descrição em texto de guias ("a interface mostra quanto a transferência vai custar" ao escolher origem e destino); as
  páginas com capturas pediram verificação anti-robô e não foram abertas. Diablo IV, Path of Exile e Elden Ring: as
  buscas não trouxeram captura da tela de serviço. O preço dentro do botão não foi visto numa captura desta rodada: é
  decisão de desenho (o pedido do Jean), não cópia de referência.

### Os defeitos
- **A piscada ao reforçar.** Reproduzida com uma sonda a cada quadro e capturas contínuas, num servidor com 80 ms de
  atraso artificial (simulando uma máquina mais lenta): em toda tentativa, de 65 a 130 ms depois do clique, a janela
  some e a oficina aparece (6 quadros). **Causa:** a cada pedido, o motor redesenhava a forja como uma cena nova (a
  página se limpa) e só depois calculava e mandava o painel; se as duas mensagens não caem no mesmo quadro, o
  navegador pinta a página vazia. Aqui o cálculo leva 10 a 16 ms (um quadro), por isso "às vezes". **Correção:** o
  motor calcula o painel antes de anunciar a cena, e a tela segura a janela antiga, parada, até a nova estar montada
  (sem espera adicionada). Conferido com 80 ms entre a cena nova e o painel (o pior caso para a tela): a v15 perdeu a
  janela por 4 e 5 quadros; a 16ª, por nenhum, em 4 tentativas.
- **Gestos**, conferidos por cobrança (o ouro) e por resultado (o número): clique duplo no Reforçar compra uma vez; o
  OK com clique duplo e triplo no mesmo ponto fecha e não compra; o Reforçar logo depois do OK compra na hora; quatro
  cliques seguidos compram uma vez e o resultado fica até o OK; depois disso, um clique novo compra; Enter segurado
  fecha o resultado e não compra; Enter segurado no Reforçar compra uma vez.

### Celebração e acabamento (candidatas, sem escolha)
- **Paleta do +9 ao +12** (o +8 e os de baixo não mudam): uma cor dominante e uma secundária, o prisma só em um a cada
  nove estilhaços. +9 violeta; +10 violeta com um leque fino azul; +11 ouro quente e âmbar; +12 ouro, âmbar e brilhos de
  marfim, com dois leques. A grandeza sobe pela forma (leques, alcance, estrela, anéis). A anterior fica no painel.
- **Armaduras do +9 ao +12** (capacete, peito, luvas, pernas, botas; armas, joias, escudos, tomos e aljavas como
  estavam): A · brilho nas bordas (sem faixas; uma orla baixa na cor do nível por dentro da silhueta e 1 a 4 pontos de
  luz que percorrem a borda) e B · reflexo estreito (uma passada de 1 px, 2 no +11 e +12, menos opaca). O contorno
  aprovado continua; a passada larga do reflexo não passa nessas peças. O +9 e o +12 se distinguem pela cor da orla e
  pela quantidade de pontos. Cada passo é um quadro pronto (como o veio da 15ª): nítido a 100%, 125% e 150%; parado no
  movimento reduzido; o ciclo vem de um relógio comum com um desvio fixo pelo lugar da peça, então um redesenho não o
  recomeça (medido: a fase de cada peça igual antes e depois).

### O painel de testes
"Painel de testes" na faixa abre e fecha o painel. **Personagem** (nível, classe, especialização) só muda com
"Aplicar e reiniciar cenário", que descarta a sessão temporária e reconstrói pelo caminho do jogo (`dev.subir_ate`, a
comitiva recrutada no nível dele, as peças do cenário na classe). **Sessão** (ouro, fragmentos e cada essência por
tier) aplica sem reiniciar. Mexer num campo não aplica nada (o campo editado fica marcado); o motor valida e recusa o
que não cabe (nível fora de 1 a 12, especialização de outra classe ou abaixo do nível 4, materiais acima de 99). Com
uma tentativa, uma cena ou uma confirmação em andamento, o painel não aplica e diz por quê. **Comparação visual**
(botões A/B, armaduras A/B, celebração candidata/anterior) troca na hora e fica lembrada neste navegador. Nada disto
existe no jogo nem toca os saves pessoais.

### Conferido
- **Testes do protótipo (61):** os de antes e os novos (todo passo de todo espaço melhora alguma linha, sem casa que o
  motor não usa e sem passar um degrau da conta; o elmo pequeno e o Cajado; o teto e a peça sem ganho sem cobrar; cair
  e subir com casas; a fração na ficha e na luta; a Vida por turno acumulando; o painel validando e reconstruindo as
  três classes; salvar e carregar as casas e os materiais).
- **A 1920×945 e 1280×720:** as quatro abas com o "Requer:", o preço no botão e as confirmações; os bloqueios por
  material, nível e "Já gravado"; o resultado; a dica da ficha com "Brasa I ×2"; o painel de testes.
- **A piscada** (servidor com atraso), **os gestos**, **os acabamentos** a 100%, 125% e 150% e no movimento reduzido.
- **Não conferido nesta rodada:** a tela inteira do Inventário (de dentro da forja ela não abre; a ficha foi
  conferida pelas dicas do Equipado) e a seção Materiais do Inventário com a etiqueta nova.

### Roteiro (uns 6 minutos)
1. **Ferreiro → Reforçar** o Peitoral de Jean: "Requer: 12/1", o botão "Reforçar +0 → +1 · 20", a prévia "Defesa 2 →
   2,7". Reforce e veja os atributos da ficha com a casa.
2. **Painel de testes → Comparação visual:** troque os botões A e B e passe o mouse, aperte sem soltar, use Tab.
3. **Essências (teste) → Encantar** a arma de Jean, 3º sulco, Brasa II: "Requer: [II] 3/1 · Nível 5" em vermelho, o
   botão bloqueado, "Brasa 40% → 60%", "Carrasco 15% → —" e o limite. Passe o mouse na arma no Equipado: "Brasa I ×2".
4. **Transferência (teste) → Transferir:** escolha origem e destino, clique Transferir: o botão fica onde estava, a
   pergunta e o Cancelar aparecem.
5. **Níveis altos (teste) → Reforçar** as armaduras de Jean (+9 a +12): troque o acabamento A/B no painel. Reforce a
   arma da bolsa no +8 com "Sucesso (teste)" até o +12, com a celebração candidata e depois a anterior.
6. **Reforçar** com cliques rápidos e o OK: uma compra por tentativa, sem pausa.
7. **Painel de testes → Personagem:** Mago, nível 6, Piromante → Aplicar e reiniciar cenário.

## 15ª versão: tiers com potência própria, requisitos de nível, fichas reorganizadas e os dois defeitos (histórico)

**O sistema inteiro está no [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)** (3.2 a 3.4, 4, 7, 9 e 10). Chances e
custos do reforço, a perda de dois níveis da transferência e a compatibilidade não mudaram. A 14ª está em
`tela/historico/v14` (`?tela=v14`; as versões guardadas desenham com os dados novos, então os números de gravação nelas
não são os da época). Folhas:
- `folha-comparacao.png`: a 14ª × a 15ª nos mesmos passos, nas duas resoluções (Encantar, o resultado do reforço com
  três gravações, a dica do Peitoral, a transferência);
- `folha-estados.png`: os estados novos (tiers, requisito atendido e não atendido, limite, bolsa, companheira,
  substituição idêntica, Inventário) e o tremor antes × depois.

### Regras novas (o modelo de soma até o nível 5 foi substituído)
- **Tiers com potência própria:** Brasa I, II e III são o mesmo efeito com valores diferentes (20%, 28%, 36%). Repetir
  soma só a propriedade que cresce, até o limite de cada efeito (Brasa 60%, Carrasco 50%, Eco 35%, Vigília 25%, Revide
  e Geada 40%). Cada efeito dispara uma vez por personagem; as regras por rodada e por luta continuam. Tabelas
  provisórias no 27, seção 4.
- **Requisito de nível:** equipamento = nível da base − 1 (mínimo 1); Essência I, II, III = níveis 1, 5, 9 (a faixa do
  conteúdo que dá cada tier); a peça gravada pede o maior. Bloqueado em todos os caminhos de vestir, para o herói e os
  companheiros, com "Requer nível N.". Numa peça vestida, a gravação que passaria do nível de quem veste é recusada
  sem cobrar; na bolsa, pode ser preparada. O reforço não muda o requisito.
- **"Nível +4 (teste)"**, botão novo na faixa: sobe o grupo pelo caminho do jogo, sem a festa (4 → 8 → 12).

### A tela
- **Tier no símbolo:** I, II ou III num selo de latão no canto de cima à direita, nos materiais, na seleção, nos
  sulcos, nas fichas e no espólio; a quantidade fica noutro canto.
- **Encantar:** a prévia vem pronta do motor (`demo.previsao`): o efeito do tier escolhido, o requisito, só os valores
  que mudam numa troca, a linha de quem veste quando outra peça dele soma e o limite antes de pagar. Saíram "+1
  nível", "no lugar de +1", "nível em Jean" e o teto antigo.
- **Fichas** (a ordem das três fichas do Diablo IV que o Jean mandou, com a arte do jogo): nome e reforço; tipo e
  raridade (a base sai dos parênteses do título); atributos; sulcos e efeitos (o nome numa linha pequena, a descrição
  embaixo: nada de "Revide 3 Ao receber"); "Requer nível N" à direita; o resto. A ficha mostra o que a peça fornece; o
  total de quem veste fica na prévia. As dicas sobem até caber acima da doca e, maiores que o espaço, rolam por dentro.
- **Inventário:** as peças acima do nível ficam apagadas e o Equipar delas, bloqueado com o motivo.
- **Resultado do reforço:** nome e nível, a peça com os efeitos, atributos com a mudança, os símbolos dos sulcos (as
  descrições ficam na inspeção), SUCESSO e OK. O SUCESSO e o OK desceram e o OK não cai mais sobre o Reforçar atrás
  (conferido a 1920 e a 1280); "OK" é o rótulo, o Enter é uma marca discreta. Na gravação, a gravação nova em
  destaque.
- **Transferir:** a etiqueta do ícone mostra o reforço de agora; embaixo, "Após transferir" e só o nível previsto (a
  origem +0 em vermelho, o destino em verde). A moeda e o preço ao lado do Transferir; o "tem N" do ouro saiu (o saldo
  está no cabeçalho). A confirmação: os dois cartões, a pergunta, o preço, Cancelar e Transferir. O resultado num véu
  fechado, o destino em destaque. As regras saíram da tela (ficam no 27 e na ajuda).

### Os dois defeitos
- **Reforçar não respondia depois do OK.** Reproduzido: dispensando no ponto do Reforçar e clicando de novo a cada
  250 ms, nenhum clique comprava; só depois de uma pausa. **Causa:** o botão (e o OK) descartava todo clique com
  `event.detail > 1`; o Windows segue contando 2, 3, 4… enquanto os cliques caem no mesmo ponto a menos de meio
  segundo, então a proteção se renovava a cada clique; e 450 ms de "calma" depois de dispensar engoliam qualquer
  clique. **Correção:** só o 2º clique de um clique duplo (`detail` 2) e o clique que o Espaço gera ao soltar a tecla
  que dispensou são o resto do gesto; do 3º em diante é uma ação nova; sem pausa por tempo. Conferido: dispensar e
  clicar compra no 3º clique; clique duplo no Reforçar compra uma vez; Enter segurado dispensa e não compra; o OK não
  fica mais no lugar do Reforçar.
- **A peça tremia no resultado.** Não era o defeito da Manopla. **Causa:** o veio (+5 a +12) era misturado pelo CSS
  (`mix-blend-mode: overlay`); com isso, o navegador reamostrava a peça e ela ficava borrada no resultado, mais ou
  menos conforme o reflexo, os brilhos e o passo do veio entravam, o que parecia tremor. A 100% a Couraça +10 também
  borrava; a 125% e a 150% quase todas as peças com veio. **Correção:** cada passo do veio é um quadro pronto (a
  mistura feita num canvas fora da tela) mostrado como imagem; o contorno também. Medido (blocos borrados do desenho,
  mediana): a 125%, Couraça +10 89% → 1%, Martelo +12 83% → 0%, Machado +5 68% → 0%; a 150%, Couraça 90% → 0%; a 100%,
  Couraça 65% → 0%. O anel e as peças sem veio já estavam nítidas e seguem iguais.

### Conferido
- **Testes do protótipo (52):** os de antes, no modelo novo, e os novos: cada tier com o seu valor, repetição igual e
  misturada até o limite, textos por tier, a ficha com o que a peça fornece, a prévia da troca e do limite, os
  requisitos (tabela, peça gravada, vestir bloqueado no herói e no companheiro, achado, gravação em peça vestida sem
  cobrar e preparada na bolsa), salvar e carregar.
- **A 1920×945 e 1280×720:** Encantar com requisito atendido e não atendido, limite, bolsa, companheira e substituição
  idêntica; o resultado do reforço com três gravações; a transferência inteira; as dicas do Equipado nos slots de
  baixo e do Inventário; o Inventário com as peças acima do nível.
- **O tremor** a 100%, 125% e 150% (Couraça +10, Martelo +12, Machado +5, anel +1), antes e depois.

### Roteiro (uns 5 minutos)
1. **Ferreiro → Essências (teste) → Encantar.** A arma de Jean, 3º sulco (Carrasco I), Brasa, tier II: a prévia mostra
   28%, "Requer nível 5" em vermelho, "Brasa nesta peça 40% → 60%" e o limite; o botão fica bloqueado. Escolha o
   1º sulco e Brasa I: "Já gravado".
2. **Aba Bolsa:** o Martelo de Aço (Brasa III + II): grave mais uma Brasa III. Na bolsa, pode; a prévia avisa o limite.
3. **Nível +4 (teste)** e volte à arma de Jean: o tier II agora passa.
4. **Reforçar** o Peitoral de Jean (três gravações): o resultado só com os símbolos dos sulcos; clique OK e, logo,
   Reforçar de novo várias vezes: ele responde.
5. **Níveis altos (teste) → Reforçar** a Couraça (+9 → +10) com a tela a 125%: a peça fica nítida durante o reflexo.
6. **Transferência (teste) → Transferir:** o Machado +10 para o Martelo de Aço: "Após transferir" +0 e +8, o preço ao
   lado do botão, a confirmação e o resultado.
7. **Inventário:** passe o mouse nas peças dos slots de baixo do Equipado e na Martelo de Aço da bolsa (apagada,
   "Requer nível 9").

## 14ª versão: uma janela só, o Encantar em duas áreas, a transferência entre duas peças (histórico)

**O sistema inteiro está no [27](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)** (seções 3.3, 8, 9 e 10). Regras,
chances e custos não mudaram; a única regra nova é a recusa da mesma gravação. A 13ª está em `tela/historico/v13`
(`?tela=v13`). As folhas desta versão (`folha-comparacao.png` e `folha-transferir.png` da 14ª) estão no git.

### Correções pedidas pelo Jean
- **Reforçar sem cena:** depois dos botões de teste, o reforço às vezes acontecia sem animação. Os cenários de teste
  zeravam o último resultado e a numeração recomeçava; a tela, que espera um número maior que o último visto, ignorava
  o resultado. Agora o número só cresce (`forja_seq`) e o motor diz à tela qual vem (`proximo_id`). Reproduzido antes
  (o Gharbad caiu de +4 a +3 sem cena) e conferido depois.
- **Contorno do anel por dentro:** o contorno do +4 em diante era uma sombra do desenho inteiro e contornava também o
  furo do anel. Agora é desenhado só pela silhueta de fora (o furo conta como dentro).
- **A Manopla de Ferro +2 se mexendo na passada do reflexo verde:** a 125% e 150% de escala, o modo de mistura do
  reflexo fazia o navegador amostrar o desenho de outro jeito durante a passada. O reflexo passa sem mistura; medido
  quadro a quadro, só a faixa do reflexo muda.

### A tela
- **Uma janela para as quatro abas:** mesma moldura, mesmo tamanho, o Fechar no mesmo lugar (antes ele era cortado).
  O cabeçalho leva só as abas, o ouro e o Fechar; o material aparece junto da operação, com "tem N".
- **Encantar em duas áreas, sem ficha lateral:**
  - a peça (nome, dono, desenho) e os sulcos como botões, com o ícone e o tier da essência dentro;
  - a família, depois o tier ("III ×3"), e a prévia com os números do motor: a contribuição, o nível do efeito em
    quem veste (na bolsa, só a peça), o valor antes → depois, o que sai e o que entra numa troca, e a nota do teto;
  - a mesma gravação sobre ela mesma: "Já gravado", sem cobrar (o motor recusa; teste novo).
- **Transferir entre duas peças:** origem e destino do mesmo tamanho, com o conduto entre eles; a lista de escolha
  com ícone, nome, raridade, reforço e dono; os destinos possíveis primeiro, os outros com o motivo; trocar a origem
  limpa o destino que deixou de servir, com uma linha dizendo isso; a confirmação com os dois resultados e o preço.
- **A cena da transferência (1,4 s):** a origem acende, a luz corre pelo conduto, a origem perde o acabamento e o
  destino o recebe; depois "Transferência concluída", até o OK. Movimento reduzido: o resultado parado. Adiantar não
  dispensa; fechar a janela no meio não desfaz nem cobra de novo; depois do OK as escolhas se limpam e o foco volta à
  origem.
- **Desmontar:** o nome da peça como título e a venda no mercado numa linha.
- **Fichas:** o tier dentro do sulco (sem a linha de nomes); a parte da peça e o teto entre parênteses ("2 desta peça
  · teto 5"), nunca um nível acima do teto como o ativo; "Detalhes" no lugar de "Como funcionam", com uma frase por
  essência (o que não dispara de novo, o que não soma, quem resiste) conferida contra o código. Sem os rodapés
  "Clique para…" nas dicas (os gestos continuam); no Inventário, a peça marcada não abre a dica por cima da ficha.
- **Referências:** o Todd's Hammer do MapleStory SEA (as duas imagens do aviso oficial, a janela e a confirmação,
  examinadas). Last Epoch e Grim Dawn não foram reexaminados nesta rodada; valem as notas da 13ª. Os critérios gerais
  foram para a skill `texto-regras-fenda`.

### Conferido
- **Testes do protótipo (47):** os de antes e a mesma gravação recusada sem cobrar.
- **A 1920×945 e 1280×720:** as quatro abas com o Fechar dentro da janela; o Encantar com a mesma gravação, troca,
  teto e peça na bolsa; a transferência inteira (listas, sem destino, destino invalidado, confirmação, clique duplo
  numa cobrança só, cena, resultado, Enter segurado dispensando uma vez, foco de volta, Fechar no meio da cena com uma
  cobrança só, movimento reduzido); a ficha do Inventário com os Detalhes abertos pelo teclado e a dica da peça
  marcada sem repetir.
- **A Manopla de Ferro +2** a 100%, 125% e 150% de escala: a peça parada durante a passada.

### Roteiro (uns 5 minutos)
1. **Ferreiro → Essências (teste) → Encantar.** O martelo de Jean: o 3º sulco (Carrasco I), Brasa, tier III. A
   prévia: +3 níveis, Brasa em Jean 3 → 5, a chance, Carrasco 1 → 0, "Sai Carrasco I · entra Brasa III" e o teto.
   Escolha Carrasco I no mesmo sulco: "Já gravado", sem botão.
2. **Transferência (teste) → Transferir.** Clique na origem: o Machado de Ferro +2 diz "Nenhum destino". Escolha o
   Machado Enferrujado +10, depois um destino; troque a origem para o Peitoral +6 e veja o destino limpo com o aviso.
   Volte ao machado, escolha o Martelo de Aço, Transferir, confirme. Veja a cena e o resultado; OK.
3. **Níveis altos (teste) → Reforçar** um anel: o contorno só por fora. Depois os botões de teste e outro reforço: a
   cena aparece.
4. **Inventário:** clique na arma de Jean; Tab até "Detalhes" e Enter. Passe o mouse na peça marcada (sem dica por
   cima) e numa da bolsa (sem "Clique para…").
5. **Reforce uma Manopla** (Mãos) a +2 e olhe a passada do reflexo verde.

## 13ª versão: reforço em todo espaço, essências com tiers, transferência e fichas compactas (histórico)

**O sistema inteiro está no [27 — especificação da forja](../../../roadmapIDEIAS/27-FORJA-ESPECIFICACAO.md)**, conferido
contra este código. Esta seção registra só o que mudou. A 12ª está em `tela/historico/v12`. As folhas desta versão
(`folha-fichas.png` e `folha-encantar.png`) estão no git.

### Decisões do Jean nesta rodada
- **Reforço em todo espaço:** inclusive aljava, as outras armaduras, anéis e amuletos. A peça inteira melhora, mas
  não as gravações. Sem Fio ou Runas.
- **Mantidos:** o limite +12, as chances e os custos (sem recalibrar pelas simulações), o +1 garantido, a falha −1 até
  +0, a peça que nunca quebra e a cobrança única.
- **Essências com tiers (I, II e III = 1, 2 e 3 níveis) e repetição permitida.** Cada efeito é resolvido uma vez pelo
  nível total das peças que o personagem veste, com teto de 5 (hipótese).
- **Sulcos de 1 a 3, sorteados uma vez.** Os materiais vêm de lutas, chefes, baús e da desmontagem. Sem fusão de
  essências.
- **Transferência de reforço** (regras para testar): mesma raridade e mesmo espaço; a origem fica +0; o destino
  recebe o nível da origem menos 2, que substitui o dele; garantida e paga.

### O ganho revisado (correção matemática, separada do equilíbrio)
- **Forma fechada** a partir da peça original: cair e subir dá o mesmo número, sem deriva (testado).
- **Sem +1 imposto:** só a linha principal da arma sobe ao menos 1 por passo, e só do +1 ao +4.
- **Meio para baixo nos valores pequenos:** uma aljava de Agilidade 1 ia a 3 no +4; agora vai a 2.
- **Porcentagens:** crítico e roubo de vida sobem 0,25 ponto por nível de peça, com teto por peça (15% e 10%).
- **O dobro dos apoios saiu:** o Tomo da Coruja ia de Poder 5 a 13 no +4; agora vai a 9.
- **Exemplos reais** do +0 ao +12 em todos os espaços, com substitutas: no 27, seção 1.2. Leitura: o Martelo
  Enferrujado +12 (Ataque 11) fica abaixo do Machado Rúnico do nível 13 (14).

### As essências
- **Tabelas de 1 a 5,** uma dimensão crescendo por efeito: as chances da Brasa, do Revide e da Geada; o dano a mais do
  Carrasco; o recurso do Eco; a barreira da Vigília. O resto fica.
- **Novos limites:**
  - o Revide responde no máximo 2 vezes por rodada (sem ciclo com muitos atacantes);
  - o Eco segue em 2 vezes por luta (sem recurso sem fim).
- **Texto corrigido:** a Brasa dizia "1 vez por turno seu", mas a regra contava a rodada. Agora diz "1 vez por
  rodada".
- **Fonte identificável:** a essência vem da criatura (Geada de lobos gélidos e afogados, Brasa de cães infernais e
  cultistas…), no tier do nível dela; o chefe dá um tier acima. Os fragmentos vêm do saque real das lutas e dos
  chefes. Os botões de teste continuam separados.

### A tela
- **Encantar:**
  - um botão por essência; o tier (I, II, III, com as quantidades) se escolhe ao lado da previsão;
  - a previsão diz "Nesta peça 3 → 6 · Jean 3 → 5", o efeito no nível novo e o aviso quando parte (ou tudo) passa do
    teto;
  - o topo mostra um contador por essência, com os tiers na dica: dezoito contadores não cabiam.
- **Transferir** (aba e cartão novos, no estilo da forja):
  - a origem no molde e os destinos possíveis à direita, cada um com "+2 → +8" ou o motivo;
  - a confirmação com os dois resultados e o preço;
  - a volta com "Transferido".
- **Desmontar:** a confirmação lista as gravações que se perdem.
- **Fichas** (Inventário, Equipado, dicas, achado, forja e resultado):
  - os sulcos com os nomes e o tier numa linha;
  - um efeito por linha, com o nível total de quem veste ("Eco 5 … (5 desta peça · 7 em Odette, teto 5)");
  - os detalhes em "Como funcionam", que abre por clique e teclado (não nas dicas).
- **Correções de exibição:** as regras do jogo para `<b>` nas fichas e nas dicas faziam o nome do efeito sair como
  título. Corrigido, com o seletor que vence, achado no próprio navegador.
- **Pesquisa das fichas:** Last Epoch, Path of Exile, Grim Dawn e Diablo IV, com as imagens que de fato foram
  examinadas, na skill `texto-regras-fenda`.

### Conferido
- **Testes do protótipo (46):**
  - todo espaço cresce sem cair;
  - forma fechada sem deriva;
  - tetos de %;
  - transferência (cobrança única, nada se cria, cadeia, recusas);
  - tiers que somam, e só o que se veste conta;
  - teto;
  - textos por nível;
  - ficha com o total;
  - saque real dando materiais pela criatura;
  - Brasa em área uma vez por rodada;
  - Revide no máximo 2 por rodada, pelo nível total;
  - Carrasco pela tabela;
  - lutas de verdade;
  - salvar e carregar.
- **A 1920×945 e 1280×720:**
  - encantar com tiers e teto;
  - transferência inteira, incluindo o clique duplo na confirmação (uma cobrança);
  - o anel no resultado em destaque;
  - as fichas no Inventário, nas dicas e na ficha lateral, com "Como funcionam" aberto pelo teclado (a ficha
    lateral rola);
  - o achado de um saque real;
  - a dica do mercado (o Broquel com o sulco vazio, dentro da tela).

### Roteiro (uns 5 minutos)
1. **Ferreiro → Encantar → Essências (teste).** Jean, o martelo: escolha o 3º sulco, Brasa e o tier III. A previsão
   diz "3 → 6 · Jean 3 → 5" e avisa o teto. Passe o mouse no martelo e no tomo de Odette (Eco 5, 7 em Odette).
2. **Inventário:** clique na arma de Jean. Na ficha lateral, Tab até "Como funcionam" e Enter.
3. **Transferir → Transferência (teste) → Bolsa:** a arma +10, um destino, Transferir. Confira a confirmação e o
   resultado; depois venda ou desmonte e compare.
4. **Reforçar** um anel ou uma aljava (todo espaço) e veja o ganho na oferta.
5. **Desmontar** uma peça gravada: a confirmação lista as gravações perdidas.

## 12ª versão: o resultado em destaque, o encantamento, o reforço até +12 e o acabamento (histórico)

Pedidos do Jean (27/10/2026): separar a tentativa (a bancada) da apresentação do resultado; o mesmo destaque na
gravação; **autorizado** trocar o limite candidato +4 por **+12**, com as mesmas regras; uma progressão visual do +1 ao
+12 (referência: os itens coloridos do MU Online); a explosão do sucesso em outras cores e mais "barulho" nos níveis
altos; e, no meio da rodada, **a peça inteira melhora** (sem escolher Ataque ou Poder). Nada integrado; som adiado. A
11ª está em `tela/historico/v11` (a faixa abre "v11"; ela roda com as regras novas). Folhas: `folha.png` (o resultado
do reforço), `folha-encantar.png` (a gravação) e `folha-acabamento.png` (do +1 ao +12).

### Decisões desta rodada (do Jean)

- **Limite candidato +12** (substitui o +4). Mantidos: o +1 garantido; sucesso +1; falha −1, mínimo +0; a peça não
  quebra; cada tentativa cobra uma vez; afixos, gravações e sulcos ficam. Nada de proteção, garantia acumulada,
  destruição ou material novo.
- **A peça inteira melhora.** Acabou a escolha da arma do Guerreiro (Fio ou Runas): todas as linhas da peça crescem,
  da base e dos afixos, cada uma "condizente com o atributo" (abaixo).

### Números provisórios

**Chances e custos.** Do +1 ao +4, os mesmos da 5ª versão. Do +5 ao +12, a curva provisória:

| Tentar | Chance (comum / incomum / raro / lendário) | Ouro | Fragmentos |
|---|---|---|---|
| +5 | 52 / 50 / 48 / 46% | 110 | 3 |
| +6 | 50 / 48 / 46 / 44% | 145 | 3 |
| +7 | 48 / 46 / 44 / 42% | 185 | 4 |
| +8 | 46 / 44 / 42 / 40% | 230 | 4 |
| +9 | 44 / 42 / 40 / 38% | 280 | 5 |
| +10 | 42 / 40 / 38 / 36% | 335 | 5 |
| +11 | 40 / 38 / 36 / 34% | 395 | 6 |
| +12 | 38 / 36 / 34 / 32% | 460 | 6 |

A raridade tira **2/4/6 pontos** acima do +4 (4/8/12 até o +4). Motivo: com a queda de um nível, a diferença se
compõe a cada passo. Com a pena inteira e a curva dura abaixo, o +12 de um lendário pede em média umas 50 vezes as
tentativas de um comum; com a curva atual e a metade, umas 4 vezes. A raridade continua influindo.

**O ganho: cada + vale "a mesma peça alguns níveis acima", linha por linha.** Os passos valem 1,5 nível de peça do +1
ao +4, 1 do +5 ao +8 e 0,75 do +9 ao +12 (o +12 soma 13 níveis). As linhas fixas (Ataque, Poder, Defesa, Vida, recurso,
Agilidade, Espinhos, Regeneração, Vida por abate) crescem na proporção do próprio valor, pela escala que o gerador usa
para o nível da peça; Crítico e Roubo de vida, em %, crescem como no gerador, 0,25 ponto por nível de peça (+3 no
+12). A linha principal da arma ganha pelo menos 1 por passo, e todo passo melhora alguma linha. Nas linhas da base dos
apoios (escudo e tomo), os passos do +1 ao +4 valem o dobro, como antes. Os afixos dos apoios não ganham esse dobro:
com ele, o Tomo do Urso ia a +26 de Vida no +4.

Efeito colateral do "peça inteira", do +1 ao +4: as peças de uma linha não mudam. Nas de duas linhas, o valor sai
agora do próprio número da peça, e não do material: a Cota de Malha Enferrujada no +4 fica com Vida +6 (antes +7). Os
afixos, que antes não cresciam, agora crescem (a Brasa Sem Nome no +4: Crítico +2, Espinhos +5).

Em peças reais do gerador (`simular.py`), comparadas com uma base comum nova mais adiante:

| Peça | Base | +4 | +8 | +12 | Base comum nova do gerador, nível +6 / +12 |
|---|---|---|---|---|---|
| Martelo Enferrujado (nível 1, comum) | Ataque 2 | 6 | 10 | 14 | Machado de Aço: 7; Machado Rúnico: 14 |
| Martelo de Aço (nível 6, comum) | Ataque 6 | 11 | 15 | 19 | Machado Rúnico: 13; Machado Rúnico: 18 |
| Pranto Sangrento (nível 12, raro) | Ataque/Crítico/Defesa 12/6/5 | 17/8/7 | 21/9/9 | 25/9/10 | Machado Rúnico: 18/0/0; Machado Rúnico: 23/0/0 |
| Grimório de Aço do Vampiro (nível 6, incomum) | Poder/Roubo de vida 6/4 | 11/6 | 15/7 | 19/7 | Varinha Rúnica: 13/0; Varinha Rúnica: 18/0 |
| Peitoral Enferrujado (nível 1, comum) | Defesa/Vida 1/3 | 3/9 | 4/13 | 5/17 | Peitoral de Aço: 5/14; Peitoral Rúnico: 9/27 |
| Presa da Forca (nível 6, raro) | Defesa/Vida/Ataque/Regeneração 5/13/3/2 | 9/23/5/4 | 11/29/7/5 | 13/34/8/5 | Peitoral Rúnico: 9/25/0/0; Peitoral Rúnico: 13/36/0/0 |
| Broquel Enferrujado (nível 3, comum) | Defesa/Vida 1/1 | 4/4 | 5/7 | 5/11 | Escudo Temperado: 3/5; Escudo Rúnico: 5/8 |
| Foco Arcano da Regeneração (nível 6, incomum) | Poder/Mana/Regeneração 2/6/2 | 5/15/4 | 6/18/5 | 7/21/5 | Tomo: 4/12/0; Tomo: 5/18/0 |

**Leitura:** uma arma do começo (Martelo Enferrujado) no +12 empata com a base do gerador 12 níveis acima, que ainda
pode ser reforçada. A peça antiga dura, mas não fica à frente para sempre, e uma peça melhor ganha mais por passo
(Pranto Sangrento). O escudo pequeno (Broquel Enferrujado, nível 3) no +12 fica um pouco acima do Escudo Rúnico do
nível 15 ainda no +0, porque o piso de "todo passo melhora" pesa em linhas de 1. É um ponto para olhar.

### A simulação até +8, +10 e +12

`python ferramentas/prototipos/reforco/simular.py`: 4.000 caminhos por raridade, de +0 até o alvo, com as quedas e a
recuperação dos níveis perdidos. O orçamento é de 20.000 tentativas por caminho. Quem não chega dentro dele é contado à
parte, e os percentis são só de quem chegou. Preços sem a reputação. Mediana · 90% · 99%:

| Raridade | Alvo | Média exata | Tentativas | Ouro | Fragmentos | Quedas | Não chegou |
|---|---|---|---|---|---|---|---|
| Comum | +8 | 44 | 34 · 88 · 160 | 3.415 · 9.040 · 16.380 | 83 · 221 · 405 | 13 · 40 · 76 | 0 de 4000 |
| Comum | +10 | 93 | 70 · 190 · 382 | 9.430 · 24.895 · 49.570 | 207 · 552 · 1.113 | 30 · 90 · 186 | 0 de 4000 |
| Comum | +12 | 219 | 164 · 480 · 954 | 26.615 · 78.110 · 152.250 | 536 · 1.597 · 3.079 | 76 · 234 · 471 | 0 de 4000 |
| Incomum | +8 | 54 | 40 · 108 · 214 | 3.975 · 10.545 · 21.145 | 98 · 262 · 533 | 16 · 50 · 103 | 0 de 4000 |
| Incomum | +10 | 125 | 92 · 260 · 512 | 11.590 · 33.265 · 63.865 | 262 · 747 · 1.432 | 41 · 125 · 251 | 0 de 4000 |
| Incomum | +12 | 333 | 236 · 758 · 1.492 | 35.360 · 112.070 · 222.820 | 738 · 2.352 · 4.609 | 112 · 373 · 740 | 0 de 4000 |
| Raro | +8 | 70 | 52 · 144 · 296 | 4.960 · 13.280 · 26.760 | 125 · 337 · 686 | 22 · 68 · 144 | 0 de 4000 |
| Raro | +10 | 178 | 128 · 382 · 736 | 14.990 · 43.520 · 82.745 | 343 · 1.015 · 1.942 | 59 · 186 · 363 | 0 de 4000 |
| Raro | +12 | 543 | 388 · 1.212 · 2.550 | 51.990 · 159.115 · 326.385 | 1.128 · 3.478 · 7.221 | 188 · 600 · 1.269 | 0 de 4000 |
| Lendário | +8 | 94 | 70 · 198 · 368 | 5.980 · 16.910 · 32.120 | 155 · 443 · 830 | 31 · 95 · 180 | 0 de 4000 |
| Lendário | +10 | 267 | 184 · 568 · 1.132 | 19.630 · 58.820 · 114.740 | 472 · 1.413 · 2.775 | 87 · 279 · 561 | 0 de 4000 |
| Lendário | +12 | 957 | 676 · 2.162 · 4.160 | 79.165 · 250.085 · 474.750 | 1.793 · 5.699 · 10.996 | 332 · 1.075 · 2.074 | 0 de 4000 |

Caminho feliz (sem falhar nenhuma vez): +8 custa 860 de ouro e 20 fragmentos; +10, 1.475 e 30; +12, 2.330 e 42.

**A alternativa dura, para comparar** (`simular.py --dura`): 50% no +5, caindo 3 pontos por nível até 30% no +12,
com a pena inteira 4/8/12:

| Raridade | Alvo | Média exata | Tentativas | Ouro | Fragmentos | Quedas | Não chegou |
|---|---|---|---|---|---|---|---|
| Comum | +8 | 55 | 42 · 114 · 214 | 4.365 · 11.870 · 22.520 | 107 · 291 · 551 | 17 · 53 · 103 | 0 de 4000 |
| Comum | +10 | 163 | 122 · 356 · 710 | 15.700 · 46.135 · 90.515 | 351 · 1.033 · 2.040 | 56 · 173 · 350 | 0 de 4000 |
| Comum | +12 | 680 | 464 · 1.526 · 2.966 | 67.965 · 223.235 · 426.130 | 1.454 · 4.727 · 9.166 | 226 · 757 · 1.477 | 0 de 4000 |
| Incomum | +8 | 84 | 62 · 178 · 352 | 6.105 · 17.455 · 34.430 | 152 · 435 · 862 | 27 · 85 · 172 | 0 de 4000 |
| Incomum | +10 | 327 | 238 · 756 · 1.556 | 27.465 · 86.280 · 179.480 | 642 · 2.020 · 4.170 | 114 · 373 · 773 | 0 de 4000 |
| Incomum | +12 | 2.011 | 1.388 · 4.572 · 8.748 | 172.130 · 560.525 · 1.080.295 | 3.884 · 12.741 · 24.526 | 688 · 2.280 · 4.368 | 0 de 4000 |
| Raro | +8 | 141 | 102 · 308 · 608 | 9.170 · 27.665 · 53.785 | 235 · 712 · 1.395 | 47 · 150 · 300 | 0 de 4000 |
| Raro | +10 | 768 | 544 · 1.708 · 3.408 | 54.655 · 171.965 · 343.975 | 1.346 · 4.254 · 8.482 | 267 · 849 · 1.699 | 0 de 4000 |
| Raro | +12 | 7.399 | 4.524 · 13.418 · 19.164 | 470.025 · 1.404.525 · 2.004.550 | 11.365 · 33.824 · 48.319 | 2.256 · 6.703 · 9.576 | 267 de 4000 (6,7%) |
| Lendário | +8 | 262 | 184 · 598 · 1.216 | 15.025 · 48.380 · 98.090 | 398 · 1.292 · 2.634 | 88 · 295 · 604 | 0 de 4000 |
| Lendário | +10 | 2.144 | 1.490 · 4.970 · 10.020 | 131.075 · 431.320 · 868.165 | 3.381 · 11.162 · 22.497 | 740 · 2.480 · 5.005 | 0 de 4000 |
| Lendário | +12 | 34.408 | 8.428 · 17.304 · 19.782 | 744.650 · 1.532.980 · 1.755.755 | 19.088 · 39.377 · 45.079 | 4.208 · 8.646 · 9.885 | 2233 de 4000 (55,8%) |

**Avaliação honesta:**
- **A curva atual torna o +12 muito difícil, sem ficar impossível.** Um comum leva umas 160 tentativas na mediana, um
  lendário umas 680. O +8 fica entre 34 e 70.
- **A dura passa do ponto.** O lendário no +12 não chega em 56% dos caminhos, mesmo com 20.000 tentativas, porque abaixo
  de 50% de chance a queda de um nível faz o custo crescer em progressão geométrica. Foi descartada.
- **O ouro é o número desproporcional.** O +12 custa de 27 mil (comum, mediana) a 475 mil (lendário, 99%) de ouro, e a
  campanha curta de hoje rende centenas. O preço por tentativa precisa ser ligado à renda da campanha ampliada e à
  oferta de material, que ainda estão em definição. Não calibrei pela campanha curta.
- **Os fragmentos na mesma escala** (536 na mediana do comum no +12) pedem fontes que hoje não existem. A pilha de 99
  não impede (cada tentativa pede até 6), mas a fonte precisa existir.
- **Duas alternativas fundamentadas, se o custo incomodar:**
  - o ouro do +5 ao +12 crescendo menos (o mesmo +80 de hoje, constante);
  - ou as chances do +9 ao +12 subindo para 50%, o ponto em que a falha deixa de compor. Assim o +12 vira questão de
    custo, e não de sorte.

  As duas são decisão de design, não de tela.

### O resultado em destaque (reforço)

- **A bancada é a tela da tentativa**, como estava: a seleção, os materiais, a previsão do ganho, a chance, o botão e
  o aquecimento pelos condutos.
- **Na revelação, o resultado sai da bancada** para uma apresentação própria, na linguagem do achado:
  - o véu na tela inteira, com a força do véu do achado (0,9), e sem moldura;
  - o nome com o nível no alto, na cor da raridade, com a marca quente no número novo (o antigo apaga no mesmo lugar);
  - a peça no tamanho atual, com o acabamento e as gravações do nível novo, sem o quadrado do molde;
  - as propriedades ao lado, como na ficha do achado: as que mudaram em "antes → depois", com o novo em verde; as outras
    secundárias, sem seta;
  - os sulcos, com o nome de cada gravação, sem as descrições longas;
  - "SUCESSO" grande e o OK no acabamento do jogo.
- **O que fica atrás:** materiais e controles, escurecidos e sem interação. O nome, a peça e a ficha da bancada saem
  do fundo, para não aparecerem duas vezes.
- **O efeito acompanha o marco sem durar mais:**
  - do +1 ao +4, o ouro já aprovado;
  - do +5 ao +8, a cor do nível (turquesa, safira, ametista, rubi);
  - do +9, o prisma: os raios repartidos em 2, 3, 4 e 6 cores.

  A força sobe por faixa (+3, +5, +9, +12): raios mais longos, mais pontas na estrela, dois e depois três anéis de
  impacto, mais estilhaços, tremor de tela do +3 em diante e brilhos depois do golpe. O golpe e o clarão acontecem uma
  vez; depois os raios acomodam e continuam girando até o OK.
- **A falha** tem a mesma organização: "FALHOU", "+9 → +8" embaixo do nome e a propriedade que caiu em vermelho. A peça
  aparece inteira, esfriando, com cinzas e um anel cinza, sem dourado.
- **O máximo:** "Reforço máximo" embaixo do nome; a volta mostra a bancada no máximo. Não existe tentativa acima de
  +12, então não existe queda de +12 para +11.
- **Controles:**
  - OK, Enter e Esc dispensam e devolvem a mesma bancada, com a peça e a próxima oferta (ou o máximo);
  - o foco fica no OK enquanto a apresentação está aberta (o Tab fica dentro dela) e volta ao Reforçar ou à peça;
  - o gesto que adianta não dispensa;
  - o resto do gesto que dispensa (o segundo clique, o Espaço que solta) não chega à bancada por 450 ms;
  - a tecla segurada e o clique duplo continuam protegidos;
  - fechar a janela durante o aquecimento não refaz nem desfaz a compra;
  - encerrar limpa o efeito e o véu.
- **Movimento reduzido:** a mesma composição, parada.

### A gravação em destaque (encantamento)

- **A inscrição continua na bancada** (a luz percorre a borda do molde, 0,9 s). Depois, a mesma apresentação:
  - o nome da peça;
  - a peça com as bordas das gravações e o acabamento do reforço;
  - os sulcos ao lado, com a gravação nova em destaque: o encaixe aceso, o símbolo, o nome e o efeito dela; as outras
    só pelo nome;
  - na substituição, "Saiu Brasa", riscado;
  - "GRAVADO" na cor da essência e o OK.
- **Sem sorteio, sem suspense:** um anel curto na cor da essência, brilhos e, até o OK, um anel fino de tempos em
  tempos. Sem raios.
- **Permanência e controles:** o resultado fica até OK, Enter ou Esc, com as mesmas proteções. A confirmação da
  substituição não mudou.
- **A desmontagem continua com o retorno curto**, sem celebração e sem OK.

### O acabamento do +1 ao +12

**A referência.** Pesquisei o MU Online, onde o reforço também vai além do +9.
- O guia oficial da Webzen descreve um tom vermelho-escuro nos +3/+4 e azul-escuro nos +5/+6, um brilho leve "na cor do
  item" nos +7/+8 e mais forte no +9. Do +10 ao +15, diz só que cada dois níveis têm um efeito de luz diferente, sem
  descrever.
- Wikis de servidores descrevem o Excellent com um brilho multicolorido, "arco-íris", e com variações por temporada.
- Não achei fonte que ligue "Ruby" ou "Diamond" a uma regra do jogo. Tratei esses nomes como impressão de cor (pedra
  vermelha, pedra lapidada) e não como mecânica.
- O que aproveitei: a cor ganhando força por faixa, a energia passando sobre a peça, o multicolorido nos níveis altos.

**O que fiz.**
- **+1 a +4:** como aprovado. O reflexo passa a cada poucos segundos, e o +4 tem o contorno dourado.
- **+5 a +8, uma cor por nível:** turquesa, safira, ametista e rubi. Cada nível tem o contorno de 1 px, o reflexo e um
  veio da mesma cor atravessando a peça, cada vez mais presente; o +8 ganha um ponto de brilho.
- **+9 a +12:**
  - o veio multicolorido contínuo: 2, 3, 4 cores e, no +12, todas, com fios claros entre elas, como pedra lapidada;
  - o contorno trocando de cor continuamente;
  - pontos de brilho em cruz de pixel (1 a 4) acendendo em lugares diferentes da peça.
- **Pixel art de verdade:**
  - o veio é pintado num canvas do tamanho do desenho e ampliado sem suavização: as cores andam um pixel do desenho por
    passo, sem degradê nem borrão;
  - tudo é mascarado pelo desenho, então os pixels transparentes ficam vazios;
  - o veio tinge sem apagar o sombreado, e a silhueta e os detalhes continuam legíveis.
- **O +12 tem mais presença sem ser mais rápido:** mais cores, mais brilhos e o contorno mudando. O ritmo é o mesmo
  em todos os níveis, e cada peça começa num ponto dele, então nada pisca em sincronia.
- **Informação separada:**
  - a raridade fica na borda do encaixe;
  - o reforço, no desenho;
  - as gravações, nos rastros da borda;
  - a seleção e o foco, como estavam.
- **Em todas as telas:**
  - bancada, esteira, Inventário (equipado e bolsa), Equipado da ficha lateral e o achado;
  - nas dicas, que não têm o desenho, o +N do nome na cor do nível.
- **Persistência e desempenho:**
  - a aparência entra no mesmo instante em que a tela redesenha o slot;
  - não some ao trocar de equipamento, ao apertar Continuar nem ao salvar e carregar;
  - um relógio só, de 70 ms, pinta todos os veios;
  - medido: depois de várias tentativas, nenhuma camada duplicada e nenhum palco de efeito sobrando.
- **Movimento reduzido:** a mesma aparência, parada (o veio, o contorno e os brilhos fixos).

### Depois do primeiro retorno do Jean

- **O efeito contínuo a 30 quadros por segundo.** A biblioteca de efeitos das celebrações roda a 15, e com o resultado
  parado na tela o giro dos raios parecia lento perto do resto do jogo. A apresentação tem um relógio próprio, de 30:
  os raios, anéis e clarões andam a cada quadro, e as partículas seguem no compasso de 15, com a mesma física. A
  biblioteca do jogo não mudou. Medido: 30 quadros por segundo no +5 e no prisma do +12.
- **A peça nítida no resultado.** Eram três causas:
  - a ampliação de 40 para 80 px estava sem `pixelated` (outra regra vencia);
  - o conjunto centrado caía em meio pixel (x = 757,98);
  - o contorno do acabamento tinha 1 px de tela, meio pixel do desenho.

  Agora a renderização é sem suavização, a peça fica em pixel inteiro e o contorno tem um pixel do desenho (2 px onde
  a peça aparece a 2×, no resultado e no molde a 1920; 1 px a 1280 e na esteira).
- **O acabamento contínuo no ritmo do jogo** (o que o Jean apontou na armadura +6):
  - o veio andava um passo a cada 250 ms (4 por segundo) e parecia parado e aos saltos; agora anda a cada 70 ms (14 por
    segundo), ainda um pixel do desenho por passo;
  - o contorno do +9 ao +12 trocava de cor em saltos lentos (0,8 s por cor); agora corre pelas cores continuamente
    (3 s a volta; 2 s no +9);
  - os pontos de brilho acendem a cada 1,6 s (antes 2,4).

  Medido na demonstração: 14 passos por segundo e o contorno mudando entre um quadro e outro.
- **O reflexo contínuo no resultado:** a peça do resultado tinha uma passada só, na entrada (e o redesenho da forja às
  vezes a cancelava). Agora ela entra no mesmo ciclo das peças do jogo: passa na entrada e depois a cada ~3 s até o OK
  (medido: 0,3 s, 3,3 s, 6,5 s).
- **Sem o rastro das gravações no resultado do reforço:** a borda quadrada cortava o selo. As gravações continuam
  em "Sulcos", ao lado; na gravação, onde o rastro novo é a notícia, ele fica. O visor de ganho da bancada, que
  aparecia fraco atrás da ficha, também sai do fundo.
- **A peça tremia na passada do reflexo** (Jean: a Montante de Ferro, do +1 ao +3), numa tela com escala de 125% ou
  150%.
  - **Causa, medida pixel a pixel numa Montante +2:** a animação do reflexo usava opacidade, e o navegador a leva para
    a placa de vídeo numa camada própria. A partir daí, a peça ampliada embaixo passava a ser desenhada suavizada e
    deslocada, inclusive depois da passada (462 pixels do desenho diferentes antes × depois). Do +4 em diante, o
    filtro do contorno já punha a peça noutro caminho, por isso lá não acontecia.
  - **Correção:** o reflexo aparece e some por visibilidade, que não vai para a placa. Na apresentação do resultado,
    a peça usa uma ampliação inteira em pixels reais da tela e fica alinhada a um pixel inteiro do aparelho (a 125%,
    566 px de CSS caíam em 707,5).
  - **Medido a 100%, 125% e 150%:** depois da passada, o desenho fica idêntico ao de antes, e durante ela só a faixa
    de luz muda.
- **O texto do visor de ganho saía da caixa** ("Vida por abate 14 → 16", com a peça inteira melhorando). O visor
  agora cabe na coluna: o nome quebra em até duas linhas e os números ficam inteiros. A 1280, a letra é um pouco menor
  e os espaços, mais curtos. Medido: dentro do leito nas duas resoluções.

### Casos de teste

O botão **"Níveis altos (teste)"** na faixa da demonstração (com a forja aberta) prepara o save temporário da
demonstração; nada disso é conteúdo, e os saves pessoais não são tocados:
- a arma de Jean no +11, com três gravações (para tentar o +12);
- a peça de Morel no +12, com três gravações;
- na bolsa, peças no +8, +4, +9 e +12;
- as peças de Odette no +5 e no +7;
- ouro e fragmentos de sobra.

### Conferido

Os 39 testes do protótipo. A 1920×945 e a 1280×720:
- **a sequência da mesma tentativa:** oferta, aquecimento, contenção, impacto, resultado mantido e volta à bancada;
- **os casos de reforço:** +4 → +5 (peça única, nome longo, três propriedades), +9 → +10, +11 → +12 (o máximo, três
  gravações), falha +9 → +8 e o movimento reduzido;
- **a gravação:** num sulco vazio, e a substituição com a confirmação;
- **os gestos:** Enter segurado 12 vezes dispensa uma vez e não compra; clique duplo no OK dispensa sem comprar;
  clique duplo no Reforçar compra uma vez; Esc dispensa, e o foco volta ao Reforçar;
- **a desmontagem:** inalterada;
- **salvar pela interface e carregar:** as peças voltam com o acabamento;
- **a folha:** os doze níveis em seis peças (clara, escura, fina e vazada, o anel pequeno), no tamanho do molde e no da
  esteira.

### Pendências

- **Os números são candidatos.** O preço do +5 ao +12 e as fontes de fragmento dependem da campanha ampliada (ver a
  avaliação acima).
- **O piso de "todo passo melhora"** em linhas de 1 (o escudo pequeno) e o crescimento dos afixos especiais (Espinhos,
  Vida por abate) merecem um olhar na luta.
- **A aljava continua sem reforço** (linhas de 1 e 2). Com "a peça inteira", a pergunta volta.
- **Som adiado para a 1.0.** O impacto mais forte nos níveis altos ainda não tem som próprio.
- **Ícones das essências** em 16 e 24 px; a demonstração não tem tela de carregar.

### Roteiro (uns 4 minutos)

1. **Ferreiro → Reforçar → Níveis altos (teste)**: a esteira com peças do +4 ao +12, cada nível com o seu acabamento.
   Passe o mouse e veja o +N colorido na dica.
2. **Bolsa → Lamento de Gharbad +4 → Sucesso (teste)**: o resultado em destaque em turquesa (o +5). Enter.
3. **Jean → a arma +11 → Sucesso (teste)**: o +12, com o prisma, "Reforço máximo" e as três gravações; OK. **Falha
   (teste)** numa peça +9: a falha sóbria.
4. **Encantar → Martelo**: grave uma essência e depois substitua: "Gravado" e "Saiu ...".
5. **Inventário**: o acabamento nas peças; salve, se quiser, e confira depois de carregar.

## 11ª versão: o resultado em destaque (histórico)

Pedido do Jean depois de ver a 10ª: o sucesso escurecia junto com o resto da tela, os feixes paravam, o OK tinha a
estética antiga, o "Sucesso" era pequeno e o quadrado do molde cortava o efeito. Regras, chances, custos e o +4 iguais;
a 10ª está em `tela/historico/v10`. As folhas desta versão estão no git.

- **A bancada clara.** Causa: o recorte do véu da cena era medido antes de a janela ser desenhada e ficava 0×0 no
  canto; o véu cobria a tela inteira, bancada incluída (na captura da 10ª a ordem saiu favorável por acaso). Agora é
  medido no quadro seguinte ao desenho (e ao redimensionar): só o entorno escurece; o título, a peça, o ganho e o
  efeito ficam claros.
- **Os feixes continuam até o OK.** Abrem no impacto e seguem girando, mais curtos e achatados depois do primeiro
  segundo, por trás do título, do ganho e do pé (a leitura fica por cima); as brasas continuam subindo. O selo de
  raios é proporcional ao molde (a 1280 não invade "Sulcos").
- **"Sucesso" grande, no pé**, entre a peça e o OK, no lugar da chance e da falha (o OK continua onde estava o
  Reforçar): entra com um impacto curto e brilho. "Falhou" no mesmo lugar, sóbrio. A faixa do alto saiu.
- **O molde sem corte seco:** no sucesso, o quadrado do encaixe dá lugar a um disco escuro em degraus, como o item no
  achado; o selo de raios aparece inteiro em volta.
- **Os botões do jogo atual** (`.botao-janela`, o mesmo do achado e das janelas) em todas as ações da forja: Reforçar,
  OK, Gravar, Substituir, Desmontar, Cancelar e Fechar. Junto, uma colisão de nome: a janela mora em `#texto`, e a
  regra `#texto .perigo` pintava de vermelho o Desmontar bloqueado; corrigido.
- **A linha de raridade do encaixe** (a faixa fina embaixo da peça: cinza comum, azul mágico, latão raro, laranja
  lendário) sai no resultado de sucesso, onde cortava o selo de raios; a raridade continua na cor do título. As cores
  passaram às do jogo (14-hud.css): o lendário do protótipo era roxo, um resto antigo; agora é o laranja do jogo.
- **O nome do recurso na oferta:** a oferta escrevia sempre "Mana" (uma tabela fixa do protótipo), e o resultado, o
  recurso de quem leva a peça (o tomo na bolsa do Guerreiro: "Mana 5 → 7" na oferta, "Vigor 5 → 7" no resultado).
  Agora a oferta usa o mesmo nome da ficha e do resultado; um teste confere oferta e resultado em todas as peças.
- **Conferido:** a 1920×945 e 1280×720, a sequência contínua da mesma tentativa, o +3 aos 4,0 e 4,6 s (os raios em
  outra posição: continuam girando), a falha, o movimento reduzido (o resultado parado com o OK), os gestos (Enter
  segurado compra uma vez e não dispensa; clique duplo no OK dispensa sem comprar; clique duplo no Reforçar compra uma
  vez; Esc dispensa), a desmontagem e o encantamento com os botões novos.

## 10ª versão: a bancada com o título, o resultado até o OK e as pendências de dados (histórico)

Regras, chances, custos e o limite +4 iguais; o sprite continua em escala inteira (2× a 1920), sem ampliar a 3×. A 9ª
está em `tela/historico/v9` (a faixa abre "v9"). A `folha-encantar.png` é desta versão (casos, identidade das peças,
sulcos e encantamento); a folha da sequência da 10ª está no git.

### A composição do Reforçar

- **Sem a ficha lateral.** No topo da bancada, o nome inteiro da peça com o nível ("Martelo de Ferro +2"), na cor da
  raridade do jogo; embaixo, menores, o dono e os sulcos. A peça no centro do molde, os materiais à esquerda e o ganho à
  direita. A chance e a consequência da falha junto da ação ("Falha: +2 → +1"); o botão diz "Reforçar +2 → +3". A
  ficha completa continua na dica da peça (mouse e foco do teclado).
- **O mesmo eixo e as mesmas dimensões** na oferta, na cena, no resultado e no máximo (700 × 489 a 1920; a 1280 cabe
  sem rolagem). Nome longo, peça única e peça bloqueada conferidos (no máximo duas linhas no título).

### O impacto do nível e o foco

- **O entorno escurece** durante a cena (moderado, sem desfoque nem clarão de tela inteira); a bancada fica clara. O
  véu é a sombra em volta de um recorte do tamanho da janela: a janela mora num contexto de camadas da HUD (a mesa), e
  um véu de tela inteira escurecia a bancada junto (achado na sequência contínua e corrigido).
- **Contenção:** no fim do aquecimento, a luz do molde se fecha num instante antes do impacto, dentro da mesma duração.
- **Sucesso:** o nível antigo fica no título até a revelação; então o número novo entra como uma marca quente (impacto
  breve, brilho e fagulhas pequenas saindo do número); o antigo some. Só o número anima; o nome, a peça e o ganho
  continuam legíveis. **Falha:** sóbria, sem a marca (o número novo em cinza claro).

### O resultado até o OK

- O resultado do reforço fica na tela até **OK**, **Enter** ou **Esc**. A chance, a falha e a nota somem do resultado
  (o espaço fica); o botão vira OK no mesmo lugar. Depois do OK, a próxima oferta ou o máximo. Sem espera forçada.
- O gesto que adianta a animação não dispensa o resultado; tecla segurada e clique duplo não dispensam nem compram de
  novo (testado: Enter compra, Enter adianta, Enter dispensa; Enter segurado 15 vezes compra uma vez; clique duplo no
  Reforçar compra uma vez; clique duplo no OK dispensa uma vez; clique fora do OK no resultado não faz nada).
- Fechar a janela continua possível e não altera a compra. Movimento reduzido: o resultado parado, com o mesmo OK. A
  desmontagem não ganhou confirmação extra.

### Corrigido

- **Retirar pela miniatura:** clicar de novo na miniatura selecionada tira a peça da bancada (como clicar na peça do
  molde).
- **O texto de compatibilidade:** a dica da essência diz "Compatível com: armas, focos e escudos"; junto do Gravar
  bloqueado, o caso da peça: "Incompatível com peitorais". O padrão está na skill `texto-regras-fenda`.
- **Os rastros da borda** das gravações mais longos (a mesma espessura): com três essências, quase se encontram, cada
  um na sua cor, em degraus de pixel.
- **O efeito que piscava** na ficha ao apertar Continuar ou numa ação que não muda o equipamento. Causa: a tela do jogo
  redesenha os painéis a cada atualização, e a aparência da peça (a borda das gravações, a luz do +4) só voltava no
  próximo ciclo do protótipo (até 200 ms depois), com a borda recomeçando a volta. Agora a aparência entra no mesmo
  instante em que o slot é redesenhado, e a borda continua a volta pelo relógio. Medido quadro a quadro num slot com
  gravação ao longo de 5 redesenhos: 27 quadros sem a borda na 9ª, 0 agora.
- **A identidade das peças:** as dicas não acham mais a peça pelo nome. Cada elemento diz qual peça mostra (a forja, o
  Equipado, o Inventário pela aba do personagem e o espaço, a bolsa pela posição, o mercado pela posição na lista da
  loja). Conferido com dois "Martelo de Ferro" (o de Jean com Brasa, o de Morel com 1 sulco vazio) e dois "Broquel
  Enferrujado" no mercado.
- **Quando os sulcos nascem:** com a peça, uma vez (o drop, o mercado, o saque, a recompensa, o único), pela semente
  da própria peça, sem gastar o sorteio do jogo; as peças que já existiam ganham os delas ao começar e ao carregar um
  save antigo. Abrir uma ficha só lê (antes, a primeira ficha decidia). O mercado e o saque importavam a criação pelo
  nome e ficavam sem sulcos: corrigido, com um teste que confere todos os módulos que criam peças.
- **Os sulcos no achado:** a janela "Você encontrou" monta a ficha em pedaços, sem a função das outras telas; os
  sulcos da peça achada entram embaixo das linhas dela (conferido com um saque real de chefe, nas duas resoluções).

### Conferido

- 37 testes do protótipo; a 1920×945 e 1280×720: a sequência contínua da mesma tentativa (oferta, aquecimento,
  contenção, impacto, resultado mantido, próxima oferta), falha, máximo, falta de recursos, nome longo, peça única,
  movimento reduzido; os gestos acima; retirar pela miniatura e pelo molde; Continuar sem piscar; peças homônimas;
  saque real; **salvar pela interface e carregar** (o Martelo +2 com Brasa e os sulcos de cada peça voltam iguais, na
  dica e na forja).

### Pendências

- **Revisão de som adiada:** fica para quando a interface estiver satisfatória como 1.0 (a cena e o resultado mantido
  não tiveram o som revisto; os sons não foram ouvidos nas conferências).
- Os ícones das essências em 16 e 24 px ainda são reduzidos pelo navegador (desenho próprio por tamanho, com a arte).
- A demonstração não tem tela de carregar: o carregamento foi conferido com um lançador de conferência que abre, pelo
  `carregar` do jogo, o save gravado pelo botão Salvar.

### Roteiro (uns 3 minutos)

1. Ferreiro → **Reforçar** → o martelo com **Sucesso (teste)**: o entorno escurece, o número novo entra quente no
   título, o resultado espera o **OK** (Enter). Experimente segurar Enter e o clique duplo.
2. **Falha (teste)**: a falha sóbria. Clique de novo na miniatura selecionada: a peça sai da bancada.
3. **Encantar** no peitoral: passe o mouse na Brasa ("Compatível com: armas") e veja "Incompatível com peitorais"
   junto do Gravar. Grave duas essências no martelo e aperte Continuar na vila: a borda não pisca.

## 9ª versão: consistência visual e de interação (histórico; as folhas desta versão estão no git)

Regras, chances, custos, o limite +4 e as regras candidatas do encantamento iguais; a bancada não foi redesenhada. A 8ª
está em `tela/historico/v8` (a faixa abre "v8").

### Corrigido

- **O sprite borrado.** Causa real, isolada por partes (o normal, um `filter` como o da falha, o deslocamento do tremor,
  o quadro real): não era a falha nem o tremor. A HUD declara `:root body img.desenho { image-rendering: auto }` (os
  desenhos feitos à mão aparecem no tamanho nativo) e essa regra vencia a do protótipo; no molde, o desenho de 40 px
  era esticado a 72 (1,8×) a 1920 e a 44 a 1280, e o navegador o suavizava em todos os estados (no escuro da falha, ficava
  evidente). Agora: escala inteira (80 px = 2× a 1920; 40 px = 1× a 1280), `pixelated` com uma regra que vence a da HUD
  só dentro da janela, e a janela em coordenadas inteiras. Conferido nítido no aquecimento, na falha, no impacto com o
  golpe e na volta à oferta, nas duas resoluções.
- **O efeito do reforço que sumia.** As representações fora da forja descobriam o nível pelo "+N" no fim do nome; a
  peça única tem o rótulo "★ Lamento de Gharbad +2 (Machado)", que não termina em "+N", e ficava sem o efeito (na forja,
  o nível vinha da própria peça, por isso ele "voltava" lá). Agora a ficha das telas leva o `reforco` da peça e todas as
  representações leem dela. Reproduzido: reforçar até +4 → guardar na bolsa → equipar → trocar pela outra arma → abrir e
  fechar o Inventário → trocar de personagem → voltar à forja: em cada passo, a ficha lateral, o Inventário (corpo e
  bolsa) e a forja com o efeito; a peça única equipada, com o reflexo no Equipado. Salvar e carregar: testado nos dados
  (a peça volta com o reforço, os sulcos e as gravações).
- **O tremor que não reiniciava.** O golpe só saía quando o temporizador do desfecho chegava com atraso zero; chega
  alguns milissegundos depois, e às vezes o +4 não tremia. E um redesenho no meio cancelava os passos. Agora o impacto
  sai uma vez por resultado (inclusive adiantado), num relógio próprio que um redesenho não corta; um golpe novo cancela
  o anterior e a volta à oferta zera o deslocamento.
- **Os sulcos nas fichas.** Encaixes quadrados (o vazio escuro com contorno; o ocupado com o símbolo da essência), na
  quantidade real da peça, na dica e na ficha: achado, Inventário (a ficha e as dicas da bolsa e do corpo), Equipado,
  mercado e forja; na forja, os mesmos encaixes são os botões de escolher o sulco. A dica de cada slot pequeno os mostra;
  o ícone da bolsa não. Os sulcos são sorteados uma vez, na primeira ficha em que a peça aparece (no lugar do drop),
  pela própria peça; consultar ou redesenhar não sorteia de novo (testado).
- **O texto do encantamento** (a skill `texto-regras-fenda` ganhou os critérios gerais): a regra num bloco à esquerda,
  de largura controlada, com o nome, o efeito e o limite; a dica da essência "Brasa ×2" (sem o "Tem 2" avulso); a ficha
  com a seção de encantamentos (o nome de cada essência como título, o efeito e o limite embaixo; saiu
  "GravaçãoCarrasco"); a essência que entra como símbolo num encaixe, o nome só no bloco; o motivo de indisponível
  sempre junto do botão; a substituição "Sai Brasa · Entra Carrasco" / "Brasa se perde."; o sucesso em latão ("Gravado"),
  com a cor da essência só no nome (o vermelho do Carrasco lia como falha). O bloco da regra tem altura fixa: a
  bancada do encantamento não muda de tamanho entre essências, peças e confirmações (500 px a 1920; 320 a 1280).
- **Retirar a peça da bancada.** Clique (ou Enter/Espaço) na peça do molde: o encaixe fica vazio, a peça continua onde
  estava, o foco volta para ela na esteira. Durante uma cena, o clique só adianta; o segundo clique de um clique duplo
  não faz nada.
- **A borda luminosa.** Um núcleo claro de 2 px, três tons, um rastro curto em degraus, sem brilho difuso, seguindo a
  borda do slot (os cantos também); sem o tom de base na borda inteira (a quantidade de sulcos está nas fichas).
  Conferida numa bolsa com reforço, gravação, raridade, seleção e foco juntos; parada com movimento reduzido.
- **A desmontagem:** a peça que se desfaz não deixa a linha de raridade no encaixe vazio (duas desmontagens seguidas,
  12 → 13 → 14).
- **A luta de teste:** durante a luta, os cartões da forja ficam apagados e não respondem ("Durante a luta, a forja
  espera."); o botão da faixa fecha a janela antes de começar.

### Investigado, sem mudança

- O tremor em si (`top` na chapa, não `translate`) não borrava o sprite; o filtro da falha também não (o borrão estava
  em todos os estados). O brilho difuso do impacto do sucesso (`drop-shadow` de 4 px) é o clarão da peça, não do
  sprite: ficou.
- O achado (o espólio de uma luta com saque) usa o mesmo caminho das dicas que foi conferido no Equipado, na bolsa e
  no mercado; não foi exercitado na tela nesta rodada (a luta de teste não tem saque).

### Pendências

- Os ícones das essências em tamanhos pequenos (16 e 24 px a partir de desenhos de 32) ainda são reduzidos pelo
  navegador; um desenho próprio por tamanho fica com a arte das essências.
- Na dica por nome, duas peças com o mesmo nome e sulcos diferentes podem trocar a seção (a forja, o Equipado e a bolsa
  usam a peça do dono; o mercado e o achado usam o nome).
- Sons não ouvidos (sem saída de áudio nas conferências).

### Roteiro (uns 3 minutos)

1. Ferreiro → **Reforçar** → o martelo até o +4 com **Sucesso (teste)**: o sprite nítido, o golpe do +3 e o do +4.
2. Clique na peça do molde: ela sai da bancada. Feche a forja; no Inventário (`i`), guarde e equipe o martelo, troque
   pelo Martelo de Aço, mude para Morel e volte: o efeito do +4 em todos os lugares.
3. Passe o mouse no Equipado e na bolsa: os sulcos na dica. No **Encantar**: a regra à esquerda, "Brasa ×2", os sulcos
   como encaixes, uma substituição ("Sai · Entra") e a ficha com a seção de encantamentos.

## 8ª versão: acabamento do reforço, desmontagem refeita e o Encantar de laboratório (histórico; as folhas desta versão estão no git)

Duas frentes, cada uma com a sua folha: `folha.png` (Lote 1: reforço e desmontagem, v7 × v8 com os mesmos dados) e
`folha-encantar.png` (Lote 2: o encantamento). A 7ª está em `tela/historico/v7` (a faixa abre "v7"). As regras,
chances, custos e o limite +4 do reforço são os da 5ª versão; o +5 continua só registrado.

### Lote 1: reforço e desmontagem

**Desmontagem (refeita):** a mesma bancada do reforço, com as mesmas dimensões (640 × 342 a 1920; 404 × 238 a 1280): a
peça no molde, no eixo do botão; à direita, o conduto e o encaixe do que ela rende (ícone e quantidade). Saíram o
título "Desmontar" na borda, o conduto solto e a faixa "Desmontado · material · nome". A confirmação fica no pé, com o
nome da peça e "O equipamento será destruído.". Depois de confirmar, uma transformação de 0,7 s (hipótese): um toque na
bancada e um clarão pequeno, a peça clareia e se parte, fragmentos de pixel voam ao encaixe do material, que aparece com
a quantidade; o saldo de Fragmentos acende em verde. A seleção fica vazia (nada é escolhido sozinho) e o encaixe
do material mostra o que chegou até a próxima ação. Achado e corrigido: desmontar uma peça única (o Lamento) falhava
com "A peça mudou desde a confirmação" (a tela mandava o rótulo com ★; o motor esperava o nome).

**Reforço:**
- Golpe seco na bancada no +3 e no +4, só a chapa e só na vertical (+3: desce e volta; +4: desce mais, um rebote menor
  e assenta), na mesma duração; a página não treme.
- O máximo: no sucesso que chega ao +4, o contorno do molde se completa barra a barra e fica aceso ~1,5 s.
- A falha mais legível a 1280 ("+3 → +2" claro, maior; "Falhou" num vermelho apagado; nada dourado).
- No desfecho, os dados da tentativa (materiais, chance, botão, nota) ficam no lugar, apagados: o resultado domina.
- Movimento reduzido: um quadro assentado (selo pequeno, raios curtos e apagados), não o pico do efeito.
- Os saldos acendem quando mudam (a cobrança em cor de custo; o que entra em verde); o +N da peça na esteira acende no
  desfecho, sem perder a seleção.
- A janela nasce já no lugar: antes, num redesenho, ela passava um quadro sem posição e o segundo clique de um clique
  duplo atravessava para o balcão atrás (o cartão Desmontar). Achado nesta rodada; corrigido.

**Reflexo e acabamento:**
- Conferido nos níveis reais, lado a lado (`CASOS=1` agora põe peças da bolsa no +1, +2 e +3, além da armadura de Morel
  no +4): +1 claro e discreto, +2 verde, +3 azul, +4 dourado, cada peça na sua vez (as passadas registradas aos 1,6 s,
  2,2 s e 2,6 s, depois em ciclo; nunca juntas).
- A faixa como luz que atravessa o material: o miolo claro, as bordas na cor do nível, a textura por baixo (mistura
  "screen"), mascarada pelo desenho da peça.
- O +4 tem também uma luz baixa e permanente na própria peça (um contorno de 1 px dourado, sem borrão).
- O ciclo só anima o que está à vista, para em aba oculta e esquece o que saiu da tela há 8 s; a raridade, o +N, a
  seleção e o foco não mudam.
- Sons do jogo (sintetizados, respeitam o som desligado): o martelo na bigorna no sucesso, o golpe junto no +3 e no +4,
  o golpe leve na falha, os estalos de metal na desmontagem. **Não ouvidos:** as conferências rodam sem saída de áudio;
  o jogo não tem um som de fragmentação (usei os estalos de metal, que existem).

**Produção (separado, 1.213.2):** o Inventário não mostra mais "Clique numa peça da bolsa ou num espaço do corpo…";
sem peça marcada, a caixa da ficha fica oculta (a coluna mantém a largura).

### Lote 2: encantamento (gravação), proposta de laboratório

**Não é regra aprovada nem integração.** O código é `encanto.py` (regras e a ligação com a luta) e a janela Encantar em
`tela/reforco.js`; o jogo não carrega nada disso (o teste de isolamento confere).

**Pesquisa (capturas observadas):** a Forja do Last Epoch (wiki oficial, captura da tela): a peça no centro, os
modificadores dos lados, um canal aceso ligando o escolhido à peça, o custo e um botão, e o resultado escrito no
próprio painel; aproveitei o canal aceso (os condutos da bancada) e o resultado no painel. O item encantado do Diablo
III (wiki, captura da ficha): a propriedade encantada fica na lista da peça, com um marcador diferente; aproveitei a
gravação dentro da ficha da peça, com a cor da essência. Sem captura de interface nesta rodada: Maxroll (404), UESP
(Skyrim) e Fextralife (Elden Ring) só tinham ícones e guias. Nada foi copiado; o acabamento é o da bancada e o efeito é
o do jogo.

**Decisão do Jean (27/10):** uma peça pode ter mais de um espaço de gravação, sorteado no drop como os outros
efeitos; a ordem dos serviços é Reforçar, Encantar, Desmontar.

**Hipóteses desta rodada (provisórias):**

| Assunto | Hipótese |
|---|---|
| Sulcos | 1 a 3 por peça, sorteados pela raridade (comum 1–2; incomum 1–3; raro 1–3; lendário 2–3). No laboratório, o sorteio acontece na primeira vez que a peça aparece (semeado pela peça); a arma do herói tem 2 no cenário |
| Elegíveis | As peças que aceitam reforço (arma, peito, escudo, foco), de qualquer um do grupo ou da bolsa; cada essência diz em que tipo entra |
| Custo | 1 essência + 30 de ouro (com a reputação); nunca falha; não rebaixa nada; não herda a chance do reforço |
| Substituir | Gravar num sulco ocupado custa o mesmo e apaga a gravação daquele sulco; a essência antiga não volta. Confirmação no pé: "Substituir X por Y? A gravação X se perde." |
| Repetição | A mesma essência não entra duas vezes na mesma peça; o mesmo efeito conta uma vez por corpo |
| Essências | Materiais do grupo, fora da bolsa. Fontes: recompensa de teste (2 de cada, marcada teste); baú (25%, 1 aleatória) |
| A peça | A gravação vai junto quando a peça troca de dono; desmontar perde a gravação (não devolve essência); vender não muda o preço |
| Coexistência | Reforço na superfície (o reflexo); gravação na borda própria do slot (a luz que percorre a borda, um trecho por gravação, defasados), sem níveis de encantamento |

**As seis essências:**

| Essência | Alvo | Gatilho | Magnitude | Duração | Limite | Interação |
|---|---|---|---|---|---|---|
| Brasa | arma | golpe do portador que acerta (não reações nem tiques) | 35%: 1 camada de Queimadura (até 3), valor 25% do maior entre Ataque e Poder (mín. 2) | a da Queimadura | 1 por rodada | soma com a Queimadura do Mago; o tique não dispara nada |
| Carrasco | arma | golpe num inimigo abaixo de 35% da vida | +30% de dano | — | — | multiplica com os outros bônus; não vale em tiques nem reações |
| Eco | arma, foco, escudo | inimigo abatido pelo portador | 25% da Mana, Vigor ou Foco máximos | — | 2 por luta | soma com Colheita e Assassino |
| Vigília | peito, escudo, foco | começo da luta | barreira de 15% da vida máxima | 3 turnos do portador | 1 por luta | não soma com outra barreira: vale a maior |
| Revide | peito, escudo | golpe corpo a corpo de um inimigo que acerta | 25%: golpe de 60% do Ataque | — | 1 resposta por golpe | o revide não aciona revide nem Brasa |
| Geada | peito | golpe corpo a corpo de um inimigo que acerta | 30%: congela o atacante (perde a próxima vez) | 1 turno dele | 1 por luta | chefes e gigantes resistem metade das vezes |

Sem ciclos: os efeitos secundários (o revide, o tique da Queimadura) não passam pelo gatilho. Na luta, os efeitos
valem para o herói e para os companheiros (os envoltórios do golpe, do início da luta e da morte de um inimigo, só
nesta demonstração); o que dura fica na memória da luta e some com ela.

**A janela:** a bancada (a essência escolhida e o ouro à esquerda, a peça no eixo, a essência que entra à direita), os
sulcos em cima da peça ("Vazio" ou o nome, na cor da essência; escolher é clicar), o trilho das seis essências com a
quantidade no canto, a regra curta da escolhida e, no pé, Gravar ou Substituir com a nota (falta, inelegível). A
gravação (2,3 s, adiantável): as barras do molde acendem na cor da essência uma a uma, um ponto de luz percorre a
borda soltando fagulhas, um anel curto, "GRAVADO" e o nome junto da peça; a borda de luz fica. O saldo, a ficha (cada
gravação com a regra), a esteira, o Inventário e o Equipado da ficha lateral mostram o resultado. A 1280, as essências
saem do cabeçalho (a quantidade está no trilho) e a bancada encolhe para caber sem rolar.

**Luta de teste:** o botão "Luta de teste" na faixa do protótipo (com a forja aberta): dois Esqueletos do nível do
herói; o grupo volta com a vida, o recurso, a experiência e o ouro de antes. Um aviso resume o que disparou.

### Conferido (8ª versão)

- 34 testes do protótipo (22 do reforço, 12 do encantamento): uma cobrança por gravação; o mesmo pedido de novo não
  grava; substituir pede a gravação vista e apaga a anterior; os sulcos sorteados (1 a 3) e o segundo sulco; a mesma
  essência recusada no outro sulco; elegibilidade e falta sem cobrança; a gravação vai com a peça a Morel; desmontar
  não devolve essência; Brasa, Vigília, Revide e Geada disparando em lutas de verdade (o robô); Carrasco (+30% abaixo de
  35%) e Eco (2 por luta) numa luta montada; uma barreira por luta, nada acumulando entre lutas; a luta de teste devolve o
  grupo como estava.
- Na tela, 1920×945 e 1280×720: o eixo e as dimensões medidos iguais no reforço e na desmontagem; a desmontagem (12 →
  15, uma vez, nada selecionado depois); o reforço até o máximo; o encantamento com quatro gravações e quatro cobranças
  (380 → 350 → 320 → 290 → 260), dois sulcos e uma substituição; fechar no meio da gravação mantém a gravação e não
  cobra de novo; Enter grava, adianta e assenta; Esc adianta e cancela a confirmação; Enter segurado e clique duplo sem
  repetir; movimento reduzido nos três serviços; a borda de luz no Inventário e na ficha lateral; a luta de teste.

### Roteiros (uns 3 minutos cada)

**Lote 1:** `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar**: o martelo, Ataque, Reforçar; na faixa,
**Sucesso (teste)** até o +3 (o golpe seco) e o +4 (o rebote e o contorno aceso); uma **Falha (teste)** no caminho.
**Desmontar**: o Lamento de Gharbad → Desmontar → confirme (a peça se desfaz, ×3 chega, o saldo acende). Com
`CASOS=1`, a bolsa mostra o reflexo em +1, +2, +3 e a armadura de Morel em +4.

**Lote 2:** Ferreiro → **Encantar**: o Peitoral, **Vigília**, Gravar; o Martelo (2 sulcos): **Brasa** no primeiro,
**Eco** no segundo; clique no sulco da Brasa, escolha **Carrasco** e Substituir (a confirmação diz o que se perde).
Feche: o Inventário (`i`) e o Equipado mostram a borda de luz. Volte à forja e use **Luta de teste** na faixa.

### Pendências

- As regras do encantamento são candidatas: a quantidade e a distribuição dos sulcos, os custos, as fontes de
  essência, a recuperação ao desmontar, a remoção sem substituir (não há) e o equilíbrio dos seis efeitos.
- Os ícones das essências são desenhos que o jogo já tem (chama, caveira, poção azul, escudo, espada, gota); arte
  própria fica para depois da aprovação das regras.
- Sons não ouvidos (sem saída de áudio nas conferências); um som de fragmentação próprio não existe.
- Ideias registradas, não feitas: laranja para um eventual +5; os níveis de encantamento não existem.

## 7ª versão: eixo central, bancada fixa, efeitos soltos e reflexo (histórico)

Só a tela mudou: regras, chances, custos, consequências e o limite +4 são os da 5ª versão. A 6ª está em
`tela/historico/v6` (a faixa abre "v6"). A folha desta versão (v6 × v7 com os mesmos itens e saldos; a sequência real até o
máximo a 1920×945 e a 1280×720; os casos; as quatro cores do reflexo) foi substituída pela da 8ª (está no histórico do
git). A tela desta versão está em `tela/historico/v7`.

### A candidata

- **Um eixo:** o nível, o centro da peça, a chance e o Reforçar ficam na mesma vertical. O leito tem três colunas, as
  dos lados de largura igual (os materiais à esquerda, o ganho à direita), e a largura delas não desloca a peça; o pé
  empilha a chance, o botão e a nota também a 1280, e a ajuda (i) fica ao lado da chance, fora do eixo. Medido em
  todos os estados: a 1920, x = 852 e a bancada 640 × 342; a 1280, x = 560 e 404 × 238.
- **A mesma bancada em todos os estados:** oferta, aquecimento, desfecho, falta, reforço máximo, peça que ninguém usa e
  sem peça escolhida. No máximo, a bancada inteira fica, com "+4", as quatro marcas, os encaixes de material apagados e
  o botão indisponível "Reforço máximo". O Reforçar não se desloca nem some durante a cena (fica indisponível).
- **A cena mostra a tentativa, não o resultado:** no aquecimento, a bancada tem o nível, o custo pago, o ganho e a
  chance da tentativa, e a ficha, o nome, o +N da esteira e o valor do atributo de antes ("Ataque" nunca fica sem
  número). No desfecho, a ficha passa aos valores novos e a propriedade que mudou acende um instante; depois, a
  próxima oferta. Nada mostra antes da hora o sucesso, a falha ou a chegada ao máximo (a dica da peça na esteira
  também espera).
- **Sem a faixa do resultado:** "Reforço bem-sucedido · +N · Ataque…" saiu; o resultado é a cena. A placa ficou só na
  desmontagem.
- **A ficha:** um cartão compacto no alto da coluna (mais estreita: 260 px a 1920, 196 a 1280) com o nome, o dono e as
  propriedades, cada valor junto do nome.
- **A comparação de teste** ("Esqueleto nível 4…") saiu da tela: é o botão "Comparação (teste)" da faixa do
  protótipo, que abre um painel com a peça escolhida.
- **O desfecho:** o efeito (FX do Estouro) não é mais recortado no leito: os raios, os estilhaços e as fagulhas passam
  da bancada e um pouco da moldura (recorte: a janela com 22 px de folga; nada na tela inteira). O halo intenso fica
  junto da peça e o anel é achatado, para não descer até a chance. A peça, o conjunto do resultado, o pé, o cabeçalho,
  a ficha e a esteira ficam por cima do efeito; o canvas não recebe cliques nem muda o tamanho de nada. Um poço escuro
  atrás do conjunto do resultado mantém a leitura sobre os raios. O sprite tem o tamanho de antes.
- **Sucesso:** "SUCESSO", o +N grande e o ganho (o valor novo em verde) num conjunto à direita da peça.
- **Falha:** "FALHOU" num vermelho apagado, a queda "+3 → +2" e o ganho perdido em cinza, menores; nada dourado nem
  grande.
- **Movimento reduzido:** o desfecho parado com o selo de raios e o contorno do molde, sem tremor nem movimento; o
  reflexo parado e discreto.
- **O reflexo do reforço:** uma faixa diagonal curta atravessa a silhueta da peça (o próprio desenho é a máscara: só os
  pixels da peça brilham), na cor do nível: +1 claro e discreto, +2 verde, +3 azul, +4 dourado. A borda de raridade
  não muda. **Em todo slot onde a peça reforçada aparece** (na forja, a esteira e o molde; no Inventário, o corpo, a
  bolsa e as opções de um espaço; na ficha lateral, o Equipado), ele passa sozinho: a primeira vez 2 s depois de a peça
  aparecer, depois a cada ~3 s, cada peça na sua vez (defasadas). Também passa ao concluir um sucesso, ao escolher a
  peça e no mouse ou no foco do teclado. Durante a cena do reforço, nenhuma brilha (a cor do nível novo esperaria o
  desfecho). Com movimento reduzido, fica parado e discreto em todos esses slots. Só na demonstração: o código está no
  script do protótipo, e o jogo não muda.

**Referências:** Epic Seven (a estrutura mantida no máximo), Ragnarok Origin (a peça perto do resultado) e Guardian
Tales (o ganho compacto), pelas indicações do Jean. Não achei capturas dessas telas nesta rodada (as buscas só deram
guias de regra), então apliquei esses princípios sem copiar nada; o acabamento e os efeitos seguem o jogo e o Estouro.

### Conferido (7ª versão)

- A sequência real até o máximo, a 1920×945 (mouse) e a 1280×720 (teclado): +1, +2, +3, falha (+3 → +2), +3, +4 e o
  "Reforço máximo". Em cada quadro (oferta, aquecimento, impacto, desfecho, próxima oferta), nível, atributo, saldos e
  custo da mesma tentativa; uma cobrança por tentativa (380/12 → 360/11 → 325/10 → 270/8 → 190/6 → 135/4 → 55/2).
- O eixo e as dimensões, medidos (acima), iguais em todos os estados nas duas resoluções, sem rolar a mesa.
- Gestos: Enter compra, adianta e volta à oferta com o foco no Reforçar; 15 repetições seguradas e o clique duplo
  compram uma vez; Esc adianta e depois fecha; o Fechar funciona no meio da cena; no centro do desfecho, o elemento
  sob o ponteiro é a bancada, não o efeito.
- `CASOS=1`: a falta ("Falta 1 Fragmento", a ajuda) e a armadura de Morel no +4; o arco que ninguém usa; o movimento
  reduzido em toda a sequência; o reflexo no mouse, no foco do teclado, na escolha e no sucesso.
- O reflexo em ciclo (registro das passadas): na forja, o molde, a esteira e a ficha lateral; no Inventário, o espaço
  Arma aos 3,2 s (2 s + a defasagem) e depois a cada ~3 s, alternando com a ficha lateral; durante a cena, só a passada
  do próprio sucesso, no desfecho; com movimento reduzido, parado (sem animação) no Inventário e na ficha lateral.

### Roteiro (uns 3 minutos)

1. `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar** → o **Martelo de Ferro** (o reflexo passa se ele
   já tiver reforço). Escolha **Ataque** e Reforçar.
2. Na faixa, **Sucesso (teste)** duas vezes: o +2 (reflexo verde) e o +3 (efeito forte, reflexo azul). Repare que a
   peça, a chance e o botão não mudam de lugar e que a ficha só muda no desfecho.
3. **Falha (teste)**: "FALHOU", +3 → +2, sóbrio. Depois **Sucesso (teste)** até o +4: a bancada fica inteira, com
   "Reforço máximo".
4. Espere uns segundos: as peças reforçadas brilham sozinhas na cor do nível, uma de cada vez. Feche a forja e abra o
   **Inventário** (`i`): o mesmo no espaço da arma e no Equipado da ficha lateral.
5. **Comparação (teste)** na faixa abre a medição de laboratório da peça escolhida.

### Para depois (ideias, não feitas)

- **+5 em laranja:** a cor do reflexo para um eventual +5. O nível não existe; o limite continua +4.
- **Encantamento:** uma luz percorrendo uma borda própria da peça, distinta do reflexo do reforço. Depende da definição
  do sistema de encantamento.
- O reflexo no resto do jogo (mercado, loot, comitiva) e de verdade na produção, só depois de aprovado aqui.

## 6ª versão: a informação reorganizada e o desfecho (histórico)

Só a tela mudou: as regras, as chances, os custos e as consequências são os da 5ª versão (abaixo). A estrutura da
bancada, o molde, os encaixes e a seleção das peças ficaram. A 5ª versão está em `tela/historico/v5` (a faixa abre
"v5"). A folha desta versão foi substituída pela da 7ª (está no histórico do git).

- **Os dados, na ordem de leitura** (referências: Soul Knight Prequel e MapleStory M): os saldos no cabeçalho; na
  bancada, os materiais como ícone e quantidade (o nome e quanto o grupo tem na dica, por mouse e teclado; faltando, o
  número fica vermelho e o pé diz "Falta 1 Fragmento"); o nível junto da peça ("+1 → +2"); o ganho no visor ("Ataque
  4 → 5"); no pé, a chance numa linha ("Sucesso 85%") e o Reforçar. O que a falha faz, que a tentativa custa o mesmo
  e que o atributo escolhido fica com a arma estão na ajuda (i). Saíram a tabela Custo/Tem, "Próxima tentativa" e
  "Cada tentativa consome o custo.". Na arma do Guerreiro, a escolha aparece como **Ataque** ou **Poder** (o ganho de
  cada um), não Fio e Runas.
- **A cena (1,05 s de aquecimento + 1,7 s de desfecho):** os condutos e o molde aquecem; no impacto, o desfecho ocupa a
  região da peça com a biblioteca FX das celebrações aprovadas do Estouro: no sucesso, o selo de raios, o clarão, um
  anel curto e os estilhaços, "SUCESSO" sobre a peça e o +N grande com o ganho; na falha, o calor que se desfaz, as
  cinzas e "FALHOU" com o nível que ficou. No +3 e no +4, a paleta lendária, mais estilhaços e a chapa treme. Depois, a
  bancada volta sozinha para a próxima oferta, com a placa resumindo o resultado.
- **O impacto fica na peça:** o efeito é recortado no leito (a área funda da peça e do resultado); o clarão é um halo
  em volta da peça, sem o pontilhado sobre a bancada inteira que a primeira montagem desta versão tinha no +3 e no +4,
  e o anel não passa muito do selo. O tremor é só da chapa (o do Estouro sacode a página).
- **Uma tentativa por quadro:** durante a cena, os encaixes mostram o custo pago (o motor já calculou a próxima), a
  ficha mantém o nome e os valores de antes (o +N novo só aparece no desfecho) e o cabeçalho já mostra os saldos
  cobrados; no fim, a bancada é redesenhada com a próxima oferta.
- **Gestos:** clique duplo e tecla segurada compram uma tentativa; durante a cena, um clique, Enter ou Espaço (com o
  foco em qualquer lugar) adianta: do aquecimento ao desfecho, do desfecho à oferta; Esc faz o mesmo e, na oferta,
  fecha. Com movimento reduzido, o desfecho aparece parado e a bancada volta depois de 1,7 s; o foco volta ao
  Reforçar (ou à peça, se o Reforçar ficou indisponível).

### Conferido (6ª versão)

Na demonstração, a 1920×945 (mouse) e a 1280×720 (teclado), uma sequência contínua cada: +0 → +1 garantido, sucesso
no +2, sucesso no +3, falha no +4. Em cada quadro (oferta, aquecimento, impacto, desfecho, próxima oferta), o nível, o
atributo, os saldos e o custo são da mesma tentativa: 380/12 → 360/11 → 325/10 → 270/8 → 190/6, uma cobrança por
tentativa. Também: 15 repetições de Enter seguradas compram uma vez; clique duplo, uma; Enter e clique durante a cena
adiantam sem comprar; Esc → desfecho → oferta → fecha; `CASOS=1` para a falta (o Reforçar indisponível, "Falta 1
Fragmento", a ajuda) e o reforço máximo (o nome longo em duas linhas, sem corte); movimento reduzido nas duas.

**Achados e corrigidos nesta conferência:** o nome da ficha mostrava o nível novo já no aquecimento (até na falha); o
Enter durante a cena não adiantava porque o foco caía na página; o clarão pontilhado cobria a bancada no +3 e no +4.

### Roteiro (uns 3 minutos)

1. `demo.bat` → Continuar → Ir para a vila → Ferreiro → **Reforçar**. Na aba Jean, o **Martelo de Ferro**: escolha
   **Ataque** e Reforçar (o +1 é garantido).
2. Na faixa, **Sucesso (teste)** e Reforçar: o aquecimento, "SUCESSO +2" e a volta à oferta (+2 → +3, 70%).
3. **Sucesso (teste)** de novo: o +3, com o efeito mais forte e a chapa tremendo.
4. **Falha (teste)**: "FALHOU +2" e a oferta de novo em +2 → +3. Repare nos saldos do topo: uma cobrança por vez.
5. Pelo teclado: Tab até o Reforçar, Enter; Enter de novo adianta, Esc volta à oferta, outro Esc fecha.
6. Passe o mouse no (i) e nos materiais. Com `CASOS=1`: a falta de fragmento e a armadura de Morel no +4.

## 5ª versão: o reforço com chance (direção aprovada; números e tela em avaliação)

**Decisões aprovadas (25, 5.6):** o +1 é garantido; depois a chance cai com o nível pretendido e, menos, com a
raridade; sucesso +1; falha −1, sem passar de +0; a peça nunca quebra; afixos, especiais e Fio/Runas ficam, também no
+0; a tela mostra antes de pagar a chance, o nível, a falha, o custo e o que o grupo tem; cada tentativa consome o
custo; a desmontagem conta o reforço conservado; sem proteção paga, failstacks ou garantia acumulada. O reforço
garantido das versões 1 a 4 fica **substituído** (histórico em `tela/historico/v4`, com as regras daquela versão).

### Hipóteses numéricas desta rodada

| Tentar | Chance (comum / incomum / raro / lendário) | Ouro | Fragmentos |
|---|---|---|---|
| +1 | 100% (todas) | 20 | 1 |
| +2 | 85 / 81 / 77 / 73% | 35 | 1 |
| +3 | 70 / 66 / 62 / 58% | 55 | 2 |
| +4 | 55 / 51 / 47 / 43% | 80 | 2 |

A raridade tira 4 pontos por degrau (12 no lendário), menos que os 15 que separam um nível do seguinte. Os preços
ficaram **mais baixos** que os da 4ª versão (25/50/90/140 e 1/2/3/4) porque agora se paga por tentativa: o caminho
feliz até o +4 custa 190 de ouro e 6 fragmentos (antes 305 e 10).

**Custo real de +0 a +4** (simulação, 40.000 caminhos por raridade, preços sem a reputação; mediana · 90% · 99%):

| Raridade | Tentativas | Ouro | Fragmentos | Quedas |
|---|---|---|---|---|
| Comum | 6 · 14 · 24 | 325 · 695 · 1.235 | 10 · 22 · 39 | 1 · 5 · 10 |
| Incomum | 8 · 16 · 28 | 335 · 820 · 1.460 | 11 · 25 · 46 | 2 · 6 · 12 |
| Raro | 8 · 20 · 34 | 390 · 955 · 1.725 | 13 · 30 · 55 | 2 · 8 · 15 |
| Lendário | 10 · 24 · 44 | 460 · 1.135 · 2.120 | 14 · 36 · 68 | 3 · 10 · 20 |

Leitura: a mediana fica entre 1,7 e 2,4 vezes o caminho feliz; 1 em 10 jogadores paga de 3,7 a 6 vezes; o pior 1%
de um lendário passa de 2.000 de ouro. Uma primeira hipótese mais dura (80/60/45 no comum) dava 48 tentativas no 90%
de um lendário: repetição demais; ficou a atual. O +4 continua sendo uma aposta (43–55%); parar no +3 é uma escolha
legítima. Para avaliar: se o pior caso do lendário é aceitável quando a campanha crescer, ou se o +4 de raros e
lendários pede mais chance.

**Recuperação:** desmontar devolve metade dos fragmentos **nominais** dos níveis que a peça conserva (+1: 1, +2: 1,
+3: 2, +4: 3), mais o da peça (comum 0, incomum 1, raro 2, lendário 3); vender devolve 25% do ouro nominal desses
níveis (+4: 47). As tentativas perdidas não contam. Testado: qualquer sequência de sucessos e falhas seguida de
desmontar ou vender deixa o grupo com menos ouro e com no máximo o material da própria peça a mais.

### A tela e a cena

- **Antes de pagar:** "Próxima tentativa +2 → +3 · Sucesso: 70% · Falha: +2 → +1"; no +1, "Sucesso garantido"; o
  custo em encaixes com Custo e Tem; "Cada tentativa consome o custo." sob o botão.
- **A cena (1,35 s):** os condutos aquecem (vermelho fundo → laranja → amarelo); a luz percorre as quatro barras do
  molde com fagulhas; no sucesso, o contorno fecha, pulsa e acende a peça; na falha, a luz apaga em trechos e caem
  cinzas, sem quebrar nada. No +3 e no +4 há mais fagulhas, na mesma duração. Durante a cena, a oferta, o botão, as
  marcas e o valor da ficha esperam (sem deslocar nada). Um clique, Enter, Espaço ou Esc revela; com movimento
  reduzido, o resultado aparece direto.
- **O resultado** fica numa placa de altura fixa acima da bancada: "Reforço bem-sucedido · +3" ou "Reforço falhou ·
  +2 → +1", com o ganho ou a perda real. A próxima oferta fica embaixo, separada.
- **Uma vez só:** o motor resolve e cobra no pedido; a tela só encena. Cada pedido leva um id; repetido, não tenta de
  novo. Fechar, trocar de aba, adiantar ou repetir a entrada não cancela, não rerrola e não compra outra vez.
- **Acabamento:** a chapa em três planos (a oferta, o leito afundado onde a operação acontece, o pé); o molde é um
  berço de ferro com garras e barras, não um pedestal; os condutos têm colares e o canal que aquece; os botões seguem
  a família da HUD; o indisponível mantém o corpo do botão, apagado. "Escolha Fio ou Runas" em cor neutra, com "O
  caminho fica com a peça." Desmontar mostra "Fragmento de Têmpera ×N"; depois, "Desmontado · Fragmento de Têmpera ×1
  · [peça]" e a seleção vazia. A seleção vazia mostra só "Escolha uma peça".
- **Casos de teste:** na faixa, "Próxima tentativa: Sorteio / Sucesso (teste) / Falha (teste)", uma vez; a placa
  marca "teste". `CASOS=1` abre com a armadura de Morel no +4 e 1 fragmento.

### Resultados observados

- 22 testes: chance exibida = calculada; o +1 garantido mesmo forçando a falha; cobrança na falha; queda até +0 com a
  base, os afixos e o nome restaurados; Fio/Runas preservado no +0; pedido repetido; o sorteio dentro de 3 pontos da
  chance em 2.000 tentativas; o único cresce pela base original; limite; falta de recurso sem cobrança; recuperação
  pelo nível conservado; ciclos; o jogo não carrega o protótipo.
- Na tela, 1920×945 e 1280×720: duplo clique, tecla segurada (15 repetições) e clique durante a cena compraram um passo
  só; Esc revela, cancela e fecha nessa ordem; fechar no meio da cena manteve a cobrança e o resultado. Achados e
  corrigidos: o foco do teclado sumia depois da compra (o botão ficava oculto na cena; agora volta ao Reforçar na
  revelação) e a tentativa quebrava depois do `CASOS=1`. A 1280 a bancada cabe sem rolar.

### Pendências

Calibrar as chances com partida de verdade (o robô não representa); decidir o pior caso dos lendários; elevação de
base e encantamento; arte do material (o saco segue provisório); som; integração.

## A tela, 4ª versão: a A · Bancada refinada (candidata em avaliação)

**Direção escolhida pelo Jean: A · Bancada.** Esta versão é a candidata refinada dela, ainda não aprovada nem
integrada. A A anterior e a B ficam em `tela/historico/v3` (a faixa da demonstração abre: "v3 (A e B)", com a troca
entre elas). Folha: `folha.png` (A anterior × A refinada com os mesmos dados, e o fluxo com recursos).

- **A bancada é um objeto:** uma chapa de ferro rebitada com espessura e sombra. Nela, da esquerda para a direita, os
  materiais (ouro e Fragmentos em encaixes, o custo grande e "Tem" embaixo), um conduto, a peça num encaixe sobre um
  pé de ferro com sombra de contato, as marcas do reforço sob ela, outro conduto com a seta e o visor do resultado; no
  pé da chapa, a ação. Princípio tirado da Forja de Stardew Valley ([wiki](https://stardewvalleywiki.com/Forge),
  captura da interface examinada): os encaixes ligados por canos e uma seta numa chapa única fazem a operação parecer
  parte de uma máquina. Não copiei a máquina nem a paleta.
- **Papéis separados:** o centro tem o próximo reforço, o ganho ("Ataque 4 → 5"), o custo e a ação; a ficha (mais
  larga: 360 px a 1920, 270 a 1280) tem o nome, o dono e todas as propriedades; a que o reforço muda tem o valor
  destacado num nicho de latão, sem repetir o "→".
- **Fio e Runas:** o visor do resultado vira duas opções ("Fio · Ataque 3 → 4", "Runas · Poder 0 → 1"); escolher é
  clicar numa; o custo é o mesmo.
- **Símbolos:** as marcas sob a peça são só o reforço; o material aparece pelo ícone com a quantidade (no canto das
  peças ao desmontar e no visor "Recebe"); a propriedade afetada é destacada pelo valor. O losango saiu.
- **Limite:** "Reforço máximo +4", as quatro marcas cheias, sem botão.
- **Desmontar:** a peça → "Recebe" (o ícone com a quantidade); a confirmação no ferro da chapa: "Desmontar [nome]?",
  "O equipamento será destruído." (em vermelho), Cancelar · Desmontar (o Desmontar em vermelho). A proteção continua
  (a confirmação arma depois de um instante; Cancelar não muda peça, recursos nem seleção).
- **Resultado do reforço:** um clique compra um passo; o custo cai, o próximo preço aparece, a peça continua
  escolhida e o foco volta ao Reforçar; a peça, a marca nova e o valor na ficha acendem por um instante (passos de
  pixel, 0,9 s, sem som, sem espera). Com movimento reduzido, o contorno da marca e do valor fica até a próxima ação.
  Os avisos genéricos "−N ouro" e "Peça +N" do jogo não aparecem por cima da janela (o topo conta).

## A tela, 3ª versão: duas direções (A · Bancada, B · Arsenal)

A estrutura da 2ª versão continua (uma janela por serviço, sem rolar a página, ouro e Fragmentos no topo, a ação
sempre à vista, Esc fecha). Mudam a apresentação e a escrita. A **faixa da demonstração**, no alto da tela, troca a
direção na hora (A ou B) e abre as versões antigas (v2, v1), guardadas em `tela/historico/`. Folha comparativa:
`folha.png` (os mesmos itens e recursos nas duas, a 1920×945 e a 1280×720, com o Mercado aprovado ao lado).

- **A · Bancada:** a peça num encaixe afundado no centro, o passo em cima ("+1 → +2"), as quatro marcas do reforço
  embaixo, os ganhos, o custo e o botão logo abaixo dela; a esteira das peças embaixo; os donos (retratos) à esquerda;
  a ficha completa à direita. Desmontar: a peça → o que recebe, a confirmação embaixo.
- **B · Arsenal:** as peças de todos numa grade por dono, com o +N no canto; a ficha compacta à direita (cabeçalho,
  passo, propriedades, venda, teste) e, fixos no pé dela, o custo e o botão. Desmontar: só a grade da bolsa, cada peça
  com o que rende no canto (◆1, ◆3; "—" não rende).
- **Em comum:** planos de ferro chapados com a textura dos botões do jogo e arestas duras (luz em cima, sombra embaixo),
  encaixes escuros para as peças, a raridade no fio de baixo do encaixe, a seleção pelos quatro cantos de latão,
  botões com quatro estados com forma (mouse clareia, pressionado afunda 1 px, indisponível tracejado, foco no anel de
  latão), a ação principal em latão. Tab fica dentro da janela; as setas andam entre as peças.
- **Escrita:** "+1 → +2", "Ataque 4 → 5", custo com rótulos ("Ouro · Custo 50 · Tem 355"), "Falta 1 Fragmento",
  "Recebe 1 Fragmento de Têmpera", "Destrói a peça." / "A peça é destruída.", "Venda: [moeda] 42" como dado
  secundário. "Encantar" saiu. A comparação contra o Esqueleto está numa área fechada, marcada **teste**. A ficha mostra
  todas as propriedades; as que o reforço faz crescer têm o ◆. Os casos estão na skill `texto-regras-fenda`.
- `CASOS=1` no `demo.py` abre a conferência: a armadura de Morel já no limite (+4) e 2 fragmentos (material
  insuficiente no segundo passo).

### Pesquisa visual (capturas abertas e examinadas)

| Captura | O que aproveitei | O que não |
|---|---|---|
| Soul Knight Prequel, Forja · Reforjar ([anúncio oficial](https://prequel.chillyroom.com/et/article/base/135), imagem 11) | A peça num encaixe no alto do painel central, sobre um suporte (A); a grade de equipamentos à direita com o "+N" no canto de cada peça (B); a quantidade de material "1/10" logo acima do botão | As abas laterais de muitos serviços, a paleta marrom e laranja, as barras verdes |
| Soul Knight Prequel, confirmação de Fundir (imagem 9) | A confirmação por cima da operação, com Cancelar e Confirmar lado a lado e o aviso de que não se desfaz | O texto longo explicando a regra |
| Soul Knight Prequel, ficha da peça (imagem 4) | As ações da peça juntas no pé da ficha | — |
| Elona Mobile, fornalha de encantamento ([blog](https://pzdl-hiraku.hatenablog.com/entry/2021/08/12/185946), a 3ª captura) | Peça à esquerda, material à direita, o resultado no meio: "a peça → o que vem" (o desmontar de A); o valor de agora e o ganho na mesma linha ("耐久 + 8 → +4") | A densidade (duas listas cheias de números e capacidades), a moeda paga (diamantes) |

O acabamento seguiu a HUD aprovada, não esses jogos: nada da paleta alegre, da monetização ou dos sistemas deles.

## A tela (2ª versão, depois do primeiro teste do Jean)

O primeiro balcão punha tudo na página da forja, embaixo da oficina: a página rolava, a arte piscava ao rolar (o
recolhimento ia e voltava em torno do mesmo ponto) e o ouro e os fragmentos sumiam do alto. Pesquisei como Elden
Ring, Diablo IV, Last Epoch e Darkest Dungeon organizam esses serviços (registrado no 25, seção 5.5) e refiz assim:

- **O balcão** tinha três serviços: **Reforçar**, **Desmontar** e **Encantar** (reservado, apagado; saiu na 3ª versão).
- **Cada serviço abre uma janela própria** sobre a coluna do meio, com a moldura das janelas principais do jogo. A
  página não rola; o pisca acabou porque o recolhimento da arte saiu.
- **No topo, sempre à vista:** as abas dos serviços, o ouro e os Fragmentos de Têmpera, e o Fechar (Esc).
- **À esquerda:** em Reforçar, as abas de quem (Jean, Morel, Odette, Bolsa) e a lista das peças; em Desmontar, só as
  peças da bolsa que rendem, cada uma com o retorno. Só a lista rola.
- **À direita:** a peça grande, o passo seguinte linha por linha ("Ataque 4 → 5"), a luta, e "Comparar com uma peça
  da bolsa" (as substitutas que quem usa poderia vestir). **Embaixo, fixo:** o custo como "50 (tem 355) · 2 (tem 7)",
  em vermelho o que falta, e o botão.
- **Esc:** cancela a confirmação; depois fecha a janela (o foco volta ao cartão do serviço); depois sai da forja.

## Decisões aprovadas (seção 5 do 25)

Reforço garantido, sem falha, quebra ou perda; melhora a função principal da peça e não os afixos nem os especiais;
qualidade da base separada do nível de reforço; desmontar devolve parte dos materiais investidos e não transfere o +N;
ouro e material no custo; materiais do grupo, em pilhas, fora dos 12 espaços; exploração e recompensas também dão
material; poucos materiais, de função clara.

## Hipóteses desta rodada (provisórias)

### O que cada peça reforça

| Peça | O que cresce | Por quê |
|---|---|---|
| Arma do Guerreiro | **Fio**: Ataque; ou **Runas**: Poder (escolhido no primeiro reforço, fixo depois) | O caminho arcano (Lâmina Rúnica, Golpe Sagrado, Julgamento Divino) usa Poder; as armas do Guerreiro só têm Ataque na base. A escolha dá identidade à peça sem material por classe |
| Arma do Arqueiro | Ataque | A Agilidade da arma é secundária |
| Arma do Mago (Odette e Yara também) | Poder | — |
| Peito (todas as classes) | Defesa e Vida | As duas linhas da base: a proteção |
| Escudo (apoio do Guerreiro, Morel) | Defesa e Vida | Idem |
| Tomo / Foco Arcano (apoio do Mago) | Poder e Mana | Idem |
| Aljava | **Não neste teste** | Linhas de 1 e 2: qualquer passo inteiro dobra ou triplica o valor. A propriedade dela (por exemplo, a capacidade de flechas) fica para decidir |
| Cabeça, mãos, pernas, pés | Não | Peças complementares, linhas pequenas (65% da força, divididas em duas) |
| Anel, amuleto | Não | A identidade deles são os afixos |

Afixos (do Lobo, da Coruja, da Tartaruga...) e especiais (crítico, roubo de vida, espinhos, vida por turno e por
abate) **não crescem**. A Couraça da Regeneração reforçada ganha Defesa e Vida; a regeneração fica igual.

### A fórmula

Cada + vale **1,5 nível de peça** na linha da base, na mesma proporção que a base tem (o material e o peso da linha
no gerador do jogo): `ganho total no +N = arredonda(qualidade × 0,75 × K × N)`, com `K = 1,5` em arma e peito e
`K = 3` nos apoios (linhas menores). Na arma, a linha única ganha **pelo menos +1 por passo** (senão uma arma
Enferrujada ficava igual do +3 para o +4). Arredondamento meio para cima. Uma base melhor ganha mais por passo; um +4
equivale a uma base do mesmo material uns 6 níveis acima.

| Peça (do gerador) | +1 | +2 | +3 | +4 |
|---|---|---|---|---|
| Martelo Enferrujado, nível 1 (Ataque 2) | +1 | +2 | +3 | +4 → 6 |
| Martelo de Aço, nível 6 (Ataque 6) | +1 | +2 | +3 | +5 → 11 |
| Brigantina de Ferro, nível 1 (Defesa 1, Vida 4) | +1/+2 | +1/+4 | +2/+6 | +3/+8 |
| Manto de Lã Negra, nível 6 (Defesa 2, Vida 12) | +2 Vida | +1/+5 | +1/+7 | +2/+9 |
| Escudo de Aço, nível 3 (Defesa 1, Vida 2) | +1/+1 | +2/+2 | +2/+4 | +3/+5 |
| Tomo, nível 6 (Poder 2, Mana 6) | +1/+2 | +1/+4 | +2/+7 | +3/+9 |
| Lamento de Gharbad, nível 3 (lendário, Ataque 7) | +2 | +4 | +6 | +8 → 15 |

Todo passo melhora pelo menos uma linha (testado do nível 1 ao 12, nos materiais do jogo).

### Custos, limite e materiais

- **Limite:** +4 (o +5 de hoje não é decisão).
- **Custo por passo:** 25 / 50 / 90 / 140 de ouro (com o desconto ou acréscimo da reputação) e 1 / 2 / 3 / 4
  **Fragmentos de Têmpera**. Do +0 ao +4: 305 de ouro e 10 fragmentos. O custo não sobe com o nível da peça:
  reforçar uma base nova rende mais pelo mesmo preço, o que empurra a troca.
- **Um material só nesta rodada:** o Fragmento de Têmpera, para o reforço comum (a função 1 da seção 5.2). Ícone
  provisório (o saco do jogo); sem arte nova. Pilha de até 99, fora da bolsa.
- **Fontes nesta demonstração:** a recompensa de teste no começo (8, identificada como cenário de teste); o baú (metade
  das vezes, 1); a desmontagem. Contratos, chefes e eventos ficam como fontes possíveis, sem números.

### Desmontar, vender e o que fica com a peça

- **Desmontar** (só na forja, só peça da bolsa): devolve **metade dos fragmentos investidos, arredondada para cima**
  (+1: 1 de 1; +2: 2 de 3; +3: 3 de 6; +4: 5 de 10), mais o **material da própria peça** pela raridade (comum 0,
  incomum 1, raro 2, lendário 3). Não devolve ouro. A peça comum sem reforço não rende nada ("venda ou largue").
- **Vender** (no mercado de sempre): a peça reforçada vende por metade do preço, e o preço subiu metade do ouro
  investido: a venda devolve **25% do ouro investido**. Não devolve fragmentos.
- **Equipada:** reforça no corpo de quem usa (herói ou companheiro); para vender ou desmontar, guarda-se na bolsa antes
  (o Inventário do grupo, com as regras de troca da comitiva). A peça que ninguém do grupo usa (o arco, com Morel e
  Odette) não recebe reforço: "Ninguém do grupo usa peças de arqueiro. Venda ou desmonte."
- **Passar a outro integrante:** a peça leva o reforço junto (é a mesma peça), pelo Inventário do grupo.

### Os ciclos (sem criação de recurso)

Reforçar e depois desmontar ou vender sempre deixa o grupo com menos ouro e menos fragmentos do que antes (testado de
+1 a +4, nos dois caminhos). Comprar uma peça no mercado e desmontar troca ouro por no máximo 1 a 3 fragmentos, ao
preço inteiro da peça, limitado ao estoque do mercado (4 peças a cada 3 dias, quase todas comuns, que não rendem).
Nenhum ciclo devolve ouro e fragmentos juntos.

## Resultados observados (na demonstração)

O mesmo alvo em todas as comparações: um Esqueleto do nível do herói (nível 4, defesa 6), sorteio fixo, dano médio do
golpe comum, sem crítico.

- **Investimento inicial:** o Martelo de Ferro do herói (Ataque 3) com Fio: +1 → 8,0 para 8,7; +2 → 9,3 (Ataque do
  herói 12 para 14 na ficha); +3 → 10,0; +4 → 10,7. Custo até o +2: 75 de ouro e 3 fragmentos.
- **A substituta:** o Martelo de Aço do nível 7 (Ataque 7, sem reforço) dá 10,7 no lugar do Martelo de Ferro +2
  (9,3): a base nova já vale mais que o investimento de 75 de ouro. Com o Martelo de Ferro no +4, empatam; reforçar a
  nova passa à frente (+5 no +4). É o "competir por um tempo".
- **A peça especializada:** o Lamento de Gharbad (lendário, nível 3) dá 10,7 contra o Martelo +2, e ainda tem roubo de
  vida e vida por abate, que o reforço não mexe. Ganha +2 de Ataque por passo (a base dele é forte). Vale manter e
  reforçar; a comparação mostra o Ataque, e a ficha mostra os especiais.
- **Companheiros:** o Cajado de Odette (Poder 3) ganha +1 de Poder por passo; Morel compara a substituta pelo golpe
  dele (8,3 → 10,4).
- **Desmontar:** o Arco Curto do Carniceiro (incomum, ninguém usa) rende 1 fragmento; a confirmação nomeia a peça e o
  que volta.

## Para depois (registrado, não feito)

- **Elevar a base de uma peça excepcional** (função 2 dos materiais): um material mais raro ligado a avanço e
  desafios. **Exemplo numérico, simulação:** o Lamento de Gharbad do nível 3 (Ataque 7, roubo 7%, vida por abate 6)
  elevado ao nível 9 viraria Ataque 16, roubo 9%, vida por abate 8, a mesma identidade. Elegibilidade, marcos, custo,
  o material e o que acontece com o reforço que ela já tem (manter, rebaixar, converter) seguem abertos.
- **Encantamento:** efeitos, quantidade por peça, receitas, consumo e substituição, em conversa própria.
- Arte final do material, celebração da melhoria, som novo.
- A propriedade da aljava; o texto do prédio do Ferreiro na vila ("até +5"), que é o da produção.
- Fontes concretas na campanha (contratos, chefes, eventos), coleta, revisão do loot.

## Conferido

- 15 testes (`testes/test_reforco.py`): todo passo melhora algo e nunca cai, do nível 1 ao 12; afixos não crescem;
  peças sem reforço; pagar e aplicar juntos; o veio uma vez; falta de ouro ou de fragmento não cobra nada; o limite;
  companheiro; peça que ninguém usa; desmontar (a conta, a seleção antiga, a peça vestida, a comum que não rende, a
  pilha cheia, a bolsa cheia); os ciclos; o jogo não carrega o protótipo.
- Na tela (1920×945 e 1280×720): a janela cabe sem rolar a página; o duplo clique em "Reforçar" compra um passo só; a confirmação da desmontagem só arma
  depois de um instante e ignora o clique que a abriu; depois de desmontar, nada fica selecionado; a tecla segurada
  não repete; Esc cancela a confirmação.

```bash
python -m unittest discover -s ferramentas/prototipos/reforco/testes -t ferramentas/prototipos/reforco
```

## Roteiro (uns 5 minutos)

1. **Recompensa de teste:** o quadro mostra 8 Fragmentos de Têmpera. "Ir para a vila".
2. **Inventário** (`i`): a seção "Materiais" embaixo da bolsa, com 8; a bolsa continua 6/12.
3. **Forja** (Ferreiro → o ferreiro na oficina) → **Reforçar**. Na aba Jean, o **Martelo de Ferro**: os dois
   caminhos (Fio e Runas), "Ataque 3 → 4", a luta, e embaixo o custo com quanto o grupo tem. **Reforçar · Fio** duas
   vezes (tente o duplo clique: compra um passo só). A ficha lateral mostra o Ataque subir; o topo da janela, o ouro e
   os fragmentos caírem.
4. Ainda no martelo, **Comparar com uma peça da bolsa**: o Martelo de Aço e o Lamento de Gharbad no lugar dele.
5. Aba **Bolsa**, o **Lamento de Gharbad**: a especializada (os especiais na ficha; +2 por passo).
6. Esc fecha a janela. No **Inventário**, vista o Martelo de Aço em você e passe o Martelo de Ferro +2 para Morel (o
   reforço vai junto); na forja, a aba Morel mostra a peça com ele.
7. **Desmontar**: escolha uma peça (cada uma diz quanto rende) → Desmontar… → a confirmação nomeia a peça. Esc ou
   Cancelar desfaz; Esc de novo fecha a janela.
8. **Mercado:** venda uma peça reforçada (o preço inclui 25% do ouro investido). Abra um **baú** (às vezes 1
   fragmento). Tente reforçar sem fragmento suficiente: o botão diz o que falta e não cobra.
