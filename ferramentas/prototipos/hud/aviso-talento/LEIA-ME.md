# O aviso de ponto de talento na ficha: conferência e uma candidata (24/10/2026; protótipo, nada no jogo)

O aviso fica na coluna do herói, logo abaixo da experiência, quando há ponto de talento para gastar
(`app/paineis.js`, `.talento-aviso`; regras em `05-paineis.css` e `14-hud.css`). O Jean achou que ele estava no
acabamento antigo; a conferência abaixo confirma. A folha: `folha-aviso.png` (hoje × R, parado e com o foco do Tab, a
1920×945 e a 1280×720, tamanho real). As fotos saem de novo por `auxiliares/fotografar.mjs` (a pasta `capturas/`
guarda só o que o roteiro grava, fora do git).

## Hoje (a evidência)

- **O desenho:** a estrela é o sprite 16×16 do jogo ampliado 2× (amarelo chapado, com o pulso de brilho borrado em
  volta), e a seta de fora é o sprite `seta_esq`, também amarelo chapado, balançando; um brilho atravessa o botão de
  tempos em tempos. Nenhum dos três é da família pintada aprovada (a doca já mostra os Talentos com o ícone pintado,
  `atalho-talentos`, e o ponto com o selo ★1).
- **A caixa:** a borda de latão de 1 px e o fundo com transparência (o `14-hud.css` por cima do anel antigo do
  `05-paineis.css`); o foco do Tab só clareia a borda, sem o contorno de 2 px dos outros botões.
- **A 1280×720:** "1 ponto de talento" quebra em duas linhas (a seta de fora come a largura).
- **O teclado:** o Tab chega ao aviso, mas Enter nele não abre os Talentos (é um `div` com `role="button"`, sem quem
  trate a tecla); o clique e a tecla T abrem.
- **A dica:** não há dica no aviso hoje (nem `title`, nem `data-dica`); nada a preservar além do texto.

## A candidata R

- O componente é o botão principal da HUD (a família do Continuar, na altura de uma linha da ficha): a face de ferro,
  a aresta de latão, a letra da interface; acende com o mouse e o foco (o contorno de 2 px dos outros botões).
- O ícone é o dos Talentos da doca (`Icones.atalho("Talentos", 32)`), o mesmo do lugar para onde o aviso leva; o número
  em latão claro; o texto, o mesmo ("1 ponto de talento", "2 pontos de talento").
- A seta pequena fica dentro do botão (a do Continuar), avançando 3 px em dois passos devagar: o ponto continua
  chamando o olho, sem piscar o texto; parada com o movimento reduzido. Saem a estrela ampliada, a seta de fora e o
  brilho que atravessa.
- Um `<button>` de verdade no lugar do `div`: Enter e espaço abrem os Talentos, como o clique.
- Cabe numa linha a 1280×720.

Conferido no jogo (`fotografar.mjs`, hoje e R, nas duas janelas): o Tab chega ao aviso com o foco visível; Enter e o
clique abrem os Talentos (na R; hoje, só o clique); sem erros na página.

**Na integração** (se aprovada): o HTML do aviso em `app/paineis.js` (o `cenario_aviso.py` mostra a troca exata),
as regras de `aviso.css` no lugar das de `05-paineis.css`/`14-hud.css` (já sem transparência nem borrado, passam na
trava do estilo) e a `.seta-pendencia` sem uso sai. A subida de nível (o "Continuar" dela) fica fora deste lote.
