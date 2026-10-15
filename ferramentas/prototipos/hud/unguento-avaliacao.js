/* A avaliação do método em dois objetos (itens-icones-teste.html mostra): o escudo com o acabamento final e a proposta
   do Unguento de Prata, olhados juntos no tamanho real e no jogo (capturas-escudo/, capturas-unguento/). É a leitura
   de quem desenhou; a decisão é do Jean. */
"use strict";

window.AVALIACAO_UNGUENTO = (() => {
  const L = [
    ["Reconhecer no tamanho real",
      "Sem mudança em 32 (ficou igual ao aprovado). Em 48 e 64 o gomo da luz acende mais e o lado de trás afunda: o volume do disco lê mais rápido no cartão do saque.",
      "Lê como o pote do atual (louça clara, paredes retas, rótulo azul-esverdeado com a tira clara), agora aberto: em 32 a parede escura de dentro marca a boca e a pasta aparece dentro dela. O risco: o bloco quase quadrado com rótulo pode lembrar uma lata, como o atual já lembra."],
    ["Volume",
      "O mesmo do aprovado: aro com espessura e lateral, gomos como planos, cúpula com sombra.",
      "Cilindro: o lado esquerdo aceso, o direito na sombra, o fundo arredondado; a borda é uma elipse com o lábio claro e a espessura na frente; as bordas do rótulo curvam com as voltas do pote (é o que mais dá o volume em 32)."],
    ["Materiais",
      "Metal: ferro e latão com reflexo especular (o arco curto do aro, a mancha no gomo, o ponto da cúpula).",
      "Louça vidrada: poucos tons largos e um reflexo macio (uma faixa estreita um degrau acima, sem branco), que para no rótulo. Papel: fosco, só a luz da forma. Pasta: cinza frio (a louça é quente), luz macia em volta de um ponto, sem especular."],
    ["Contraste",
      "Escuro e brilhante: vai do quase preto ao branco do reflexo.",
      "Mais claro e mais baixo que o escudo (a louça clara do atual); o escuro fica na boca e no lado direito. Junto do escudo, os dois pesam diferente, como pesam os atuais."],
    ["Organização dos pixels",
      "Rampas, um tom por gomo, contorno de 1 pixel, cravos sem ruído.",
      "Rampas por material (louça, pasta, rótulo, papel), luz em faixas e grupos, contorno de 1 pixel; 24 cores nos três tamanhos. Nenhum ajuste manual foi preciso."],
  ];
  return `<table><tr><th></th><th>escudo final</th><th>unguento proposta</th></tr>${L.map(([c, e, u]) =>
    `<tr><td><b>${c}</b></td><td>${e}</td><td>${u}</td></tr>`).join("")}</table>` +
    `<p class="nota" style="margin-top:10px"><b>O que os dois compartilham:</b> a mesma luz (de cima e da esquerda, um
    pouco de frente), o mesmo contorno de 1 pixel quase preto, a limpeza de pixels soltos, a paleta em rampas, a luz em
    grupos decididos, cada tamanho na própria grade e o @2x por duplicação (pixel_comum.py). <b>O que é de cada
    material:</b> o metal ganha reflexos fortes e localizados; a louça, um reflexo largo e baixo; o papel e a pasta,
    nenhum. <b>Onde a proposta ainda pode perder:</b> em 32 o monte da pasta quase não aparece (lê como superfície); a
    silhueta reta herdada do atual pode lembrar uma lata; o 48 não tem uso no jogo hoje (o unguento só aparece em 32) e
    está aqui pela coerência.</p>`;
})();
