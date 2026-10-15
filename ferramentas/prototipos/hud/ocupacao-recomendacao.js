/* A recomendação do estudo da ocupação dos ícones (itens-icones-teste.html mostra): o que deve ser comum à família de
   ícones e o que pode variar por objeto ou por contexto. É a leitura de quem desenhou; a decisão é do Jean. */
"use strict";

window.RECOMENDACAO_OCUPACAO = `
<p><b>Recomendo a alternativa de 40 px no corpo e na mochila do Inventário.</b> No tamanho real, os três objetos ganham
leitura e peso sem encostar na borda, e a raridade, o foco e os nomes continuam onde estão. A folga vinha do tamanho
pedido para a imagem, não dos desenhos; por isso o ajuste é no tamanho de exibição, com arquivos nativos.</p>
<p><b>Comum a toda a família:</b> cada tamanho de exibição tem o seu arquivo nativo (nunca uma ampliação, nunca uma
redução feita pelo navegador como solução) e o dobro por duplicação; o desenho usa o quadro, com 1 a 2 px de margem
no arquivo; a mesma luz, o mesmo contorno e as rampas por material.</p>
<p><b>Pode variar por objeto:</b> a área que o desenho ocupa dentro do quadro. O anel é alto e estreito, a armadura
larga e baixa, o escudo redondo e cheio: cada um lê pela forma e pela proporção, sem que todos preencham a mesma área,
e sem encolher um tipo para reservar lugar a outro.</p>
<p><b>Pode variar por contexto:</b> o tamanho de exibição, pelo tipo de espaço. Os espaços grandes do Inventário (56 e 60
px) pedem 40; a bolsa (52), a ficha e a prateleira do mercado continuam em 32 até um estudo próprio; o voo usa 48 e o
saque 64. A doca, os atributos e a luta não entram nisto.</p>
<p><b>O que falta para adotar:</b> os arquivos de 40 de todo o equipamento da família pintada (saem pelo mesmo caminho
dos tamanhos de hoje); a passagem de acabamento do escudo em 40; e uma decisão para os itens que ainda usam o sprite
16×16 do jogo (o machado, por exemplo): 40 não é múltiplo de 16, então eles ficam em 32 ou precisam de um desenho
próprio. Na produção, o Inventário pediria 40 ao Icones e a regra que fixa 32 px (14-hud.css) deixaria de valer
nesses dois espaços.</p>`;
