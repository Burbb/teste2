# Protótipo: o interior do templo (candidatas A e B)

28/10/2026. **Só no protótipo, esperando a avaliação do Jean.** O jogo não carrega esta pasta: diante do templo, a
vila continua aproximada, com o balcão. Segundo interior da etapa 5 (Curandeira → Templo → Taverna; a taverna não foi
começada). Feito pelo fluxo da skill `arte-cenas-fenda`.

## Abrir

Dê dois cliques em `demo.bat` (ou `python ferramentas/prototipos/templo/demo.py` na raiz). O jogo abre no navegador
num **save temporário** (uma pasta nova a cada vez; os saves do Jean não são lidos nem tocados), na porta 8794: o
Guerreiro no Vau, com a vida em 40%, Odette na comitiva e ferida, 120 de ouro e o primeiro atendimento do templo por
usar. Clique no **Templo** na vila: a vista mostra o interior no lugar da vila aproximada, e o balcão de sempre fica
embaixo.

A faixa do alto:

| Botão | O que faz |
|---|---|
| **Candidata A / Candidata B** | troca o interior (os pontos da cena acompanham) |
| **Ferido, 1º grátis** | o herói com 40% da vida e o primeiro atendimento por usar (o estado de abertura) |
| **Sem ouro** | o herói ferido, sem ouro e com o grátis já usado: o cartão apagado com o motivo |
| **Odette ferida** | só Odette precisa: o cartão "Cuidar de Odette" |
| **Ninguém precisa** | o balcão abre com "O templo está em silêncio. Ninguém aqui precisa de cuidados agora.", e o interior também |
| **Pose parada** | o movimento reduzido (o mesmo que a preferência do sistema) |

A troca de estado vale com a vila à vista (diante do templo, a faixa sai, troca e entra de novo).

## O levantamento (o que o jogo estabelece)

- **Quem atende:** "um clérigo" (masculino, sem nome), "cansado, de mãos firmes"; o balcão diz "Velas, incenso e um
  clérigo cansado, de mãos firmes." (`app/vila.js`). Ele trata "com unguentos e orações" (`servicos.templo`).
- **Os serviços:** cuidar da vida do herói (até o limite de agora, com os ferimentos) e de cada companheiro, um cartão
  por pessoa, cada um com o seu preço (`servicos.opcoes_templo`); o **primeiro atendimento do herói é grátis** na
  campanha ("O clérigo não cobra: é o seu primeiro atendimento aqui."). Depois de cuidar de alguém, o balcão continua
  aberto ("Mais alguém precisa de cuidados?") até a pessoa voltar à vila.
- **Sem ninguém precisando:** o prédio continua clicável e o balcão diz "O templo está em silêncio. Ninguém aqui
  precisa de cuidados agora." (`estado.predios_fechados`). Sem ouro: o cartão apagado com "Ouro insuficiente.".
- **Entrada, saída, tutorial:** o prédio da vila (o sino toca ao entrar), o Voltar à vila e o Esc; o quadro V2 do
  tutorial aponta o prédio ("O Templo recupera sua vida. Seu primeiro atendimento é grátis."). Nenhuma condição da
  campanha fecha o templo.
- **O exterior na vila** (`vista.js`): a igreja pequena, a nave de telhado de duas águas, o campanário à direita com
  o sino e a cruz no alto, a porta escura e **duas janelas estreitas e altas, acesas em amarelo quente** (a cor das
  janelas da vila; não há vitral colorido).
- **Para não confundir:** a capela afogada é outra igreja (abandonada, a água, as colunas, o altar com a cruz raspada,
  a janela grande atrás); o padre dela fugiu. O templo da vila é vivo, seco e cuidado.

Nada disso mudou: o protótipo não toca o motor nem o balcão.

## As duas candidatas (escolhas visuais, não fatos)

**A (a minha direção):** a nave vista de lado, com a câmera um pouco mais aberta que a da curandeira (o clérigo tem
~42 px): a entrada com a luz fria e o velário de ferro, os bancos (as cabeceiras de lado), as duas janelas altas da
fachada jogando o feixe de luz com pó, o canto de atendimento entre a nave e o presbitério (o catre, a mesa dos
unguentos), o presbitério um degrau acima com o altar, a cruz simples de madeira (a do campanário) e o incensário
pendurado, a base do campanário com a corda do sino. **O clérigo enrola ataduras** na mesa: as mãos giram o rolo, o
tronco recua no puxão de apertar, vai à frente para alisar a tira mais adiante (o braço não alcança sozinho) e, a cada
volta da rotina, ele pousa o rolo, endireita as costas e olha a nave (o cansaço).

**B (da referência do Jean):** a composição de `ferramentas/arte/referencias/cenarios internos/Interior do Templo da
Vila.png` (pedido do Jean, 28/10/2026), medida na escala do jogo com uma grade por cima e redesenhada na grade de
320×96: a nave de frente, o arco de pedra entre duas colunas, o presbitério dois degraus acima com o altar, a janela
alta e o castiçal de muitos braços; os bancos em dois blocos vistos por trás e a passadeira no corredor; a porta da rua
à esquerda com a luz do dia, a arandela e o banquinho; à direita, a mesa, o armário de potes, a porta lateral e a
mesinha do incenso; as silhuetas da frente. O clérigo tem ~31 px. **Não vieram da imagem:** os estandartes com cruz e
a cruz no avental (símbolos gerados; o jogo só tem a cruz do campanário), o vidro azul e amarelo (as janelas da igreja
são amarelo quente), as texturas, as sombras suaves e a aparência gerada do clérigo. **O clérigo dobra os panos
limpos** na ponta da mesa: pega um pano do monte (o tronco vai à frente), ergue, sacode, dobra, assenta na pilha,
alisa; a cada duas vezes, as mãos na beira da mesa, as costas sobem e ele olha a nave.

As duas: o clérigo é o mesmo do jogo (cansado, de mãos firmes, sem nome); a roupa (o hábito, o avental da B) é
escolha. A atividade é o trabalho do lugar (ataduras e panos para os unguentos), sem ritual nem efeito mágico. O
movimento do ambiente é discreto: as chamas a 200 ms, o incenso a 200 ms, o pó dos feixes (A) a 300 ms.

## A atividade pela skill (5b)

| | A: enrolar ataduras | B: dobrar panos |
|---|---|---|
| fica | os pés, a barra do hábito, a mesa, a tira estendida | os pés, a barra, a mesa, o monte e a pilha |
| conduz | as mãos girando o rolo | as mãos (pegar, erguer, dobrar, assentar, alisar) |
| acompanha | os cotovelos (comprimento fixo), a cabeça nas mãos, o tronco no puxão e no alcance | os cotovelos, o tronco (à frente para pegar), a cabeça |
| alcance | o rolo na ponta da mesa, junto do corpo; alisar a tira pede o tronco à frente e embaixo | o braço tem ~13 px: o trabalho fica na ponta da mesa; o monte pede o tronco à frente |
| ritmo | voltas de 4 poses de 2 tiques; apertar (4); alisar (5); a pausa de olhar (1,4 s); 8,5 s | cada pano em 21 tiques (pegar 3, erguer 3, sacudir 4, dobrar 3, assentar 3, alisar 5); a pausa (1,4 s); 6,2 s |
| pose parada | endireitado, as mãos na beira da mesa, olhando a nave | a mesma |

A conferência de alcance é uma conta no código (`cotovelo` falha se a mão não alcança): ela pegou o rolo longe demais
na A (mudou para a ponta da mesa, e o braço passou a ter a proporção humana).

## A interface

Diante do templo, a cena entra no lugar da vila aproximada (a vista mostra o interior; os balões dos prédios saem); o
balcão é o mesmo (os cartões, os preços, o Voltar, o Esc, as teclas 1, 2...). Os pontos da cena: **Clérigo** (leva
aos cartões, como o ferreiro) e **Saída** (faz o que o Voltar à vila faz). Na demonstração, a troca é feita pela
página (`tela/faixa.js`), sem mudar o motor: o templo não tem estado de história, e o balcão já é montado na tela.
Para integrar, a cena poderia vir do motor (como a da curandeira) ou ficar nessa troca da página: decisão para a
integração.

## Conferido

No navegador (Playwright), na demonstração, a 1920×945 e a 1280×720: o interior no lugar da vila com o balcão e os
pontos; cuidar da vida (o primeiro atendimento, grátis) e o balcão continuando com o interior; a candidata B; a Saída
da cena voltando à vila; ninguém precisando (o interior e o balcão abrem, com a frase); o Esc; sem ouro (o cartão
apagado); sair e voltar três vezes com um relógio só, a 100 ms; a pose parada sem mudar; sem erros no console.

## Limites (reais)

- Desenho em código, como a curandeira antes da aprovação: a fonte em Aseprite vem depois que uma candidata for
  aprovada (skill, seção 6).
- A B tem o clérigo pequeno (~31 px, a escala da referência): o rosto e as mãos são poucos pixels; a leitura da
  atividade vem do pano claro mudando de forma.
- A 1280×720, com o primeiro atendimento e Odette, o balcão leva os dois cartões e o Voltar à vista; com mais
  companheiros feridos, pediria rolagem (como hoje).
- Sem som novo (adiado). O tutorial V2 continua apontando o prédio na vila.

## As fontes

- `a/desenho.py`, `a/figura.py`: a candidata A (o ambiente, o clérigo, as poses e a rotina).
- `b/desenho.py`, `b/figura.py`: a candidata B (o ambiente reaproveita as cores e o pincel da A).
- `exportar.py`: as camadas de `camadas/a`, `camadas/b` e o `rotina.json`.
- `demo.py`, `demo.bat`, `tela/` (`cena-templo.js`, `faixa.js`, `templo.css`): a demonstração.
