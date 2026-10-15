/* A avaliação do teste do escudo (itens-icones-teste.html mostra), olhada no tamanho real, no jogo
   (capturas-escudo/): o atual, o candidato anterior (o relevo renderizado e reduzido) e o refinado em pixel art. É a
   leitura de quem desenhou; a decisão é do Jean. */
"use strict";

window.AVALIACAO_ESCUDO = (() => {
  const L = [
    ["Volume e materiais",
      "O reflexo grande do gomo e a cúpula dão o volume; o ferro lê como metal polido e o latão brilha; o aro é uma linha fina, sem espessura.",
      "O mais volumoso: o aro com rolo e lateral, a sombra da peça central, os gomos como planos. Os materiais leem, mas o acabamento é de render.",
      "Guarda o volume do anterior (o aro com espessura e lateral, o sulco e a sombra da peça, os gomos) com a luz em grupos. O latão lê bem. O ferro lê como metal, mas em 64 a face ficou mais clara e mais chapada que a do atual."],
    ["Presença em 32 px",
      "A maior: o reflexo grande e a cúpula fazem o escudo ler de longe.",
      "Carregada: o aro claro, o degrau e o sulco escuros viram anéis demais.",
      "Boa e limpa: a silhueta é a mais firme das três (o aro e a lateral), o reflexo é uma mancha definida e a cúpula ficou redonda; ainda um pouco menos de presença que o atual, porque o reflexo dele é maior."],
    ["Clareza dos reflexos",
      "Clara e forte: uma cunha clara do pé da peça até o aro; a cúpula com um ponto de luz.",
      "O reflexo corre dentro do gomo, mas apagado; a cúpula tem pouco brilho.",
      "Organizados: o brilho do aro é um arco curto em cima à esquerda, a parede do aro acende só num toque embaixo à direita, a cúpula tem um grupo de brilho. O reflexo do gomo é menor que o do atual, sobretudo em 64."],
    ["Organização dos pixels",
      "Pintado e reduzido: tons misturados nas bordas, pixels de transição.",
      "Reduzido do render: centenas de tons, bordas macias, nenhum pixel decidido.",
      "Cada pixel decidido: 17 a 18 cores em rampas, cada gomo num tom, o contorno de 1 pixel com degraus regulares, os cravos como pinos (1 pixel em 32, 2×2 em 48, uma cabeça de 3×3 em 64), nenhum ponto solto."],
    ["Coerência entre pequeno e grande",
      "Boa: é o mesmo desenho reduzido.",
      "Boa: a mesma conta em cada tamanho.",
      "Boa: as mesmas regras em 32, 48 e 64, com a simplificação de cada um (sem emendas em 32, cravos por tamanho, o brilho da cúpula desenhado por tamanho)."],
    ["Convivência com a HUD e o mundo",
      "É da família pintada da HUD (o elmo, a cota, a espada).",
      "Parece de outro conjunto (render), sobretudo em 64.",
      "Mais perto do mundo (pixel art de verdade, como os cenários e os retratos); ao lado dos ícones pintados que ficam, destoa pela nitidez, menos que o anterior."],
  ];
  return `<table><tr><th></th><th>atual</th><th>anterior</th><th>refinado</th></tr>${L.map(([c, a, b, r]) =>
    `<tr><td><b>${c}</b></td><td>${a}</td><td>${b}</td><td>${r}</td></tr>`).join("")}</table>` +
    `<p class="nota" style="margin-top:10px"><b>Onde o refinado melhorou:</b> a organização dos pixels (rampas, gomos em
    tons únicos, contorno regular, cravos sem ruído), a silhueta e a espessura do aro em todos os tamanhos, os reflexos
    localizados no aro, a cúpula com brilho em grupo, e a leitura limpa em 32 px, onde o anterior ficava carregado.
    <b>Onde ainda perde para as referências:</b> o reflexo do gomo é menor que a cunha clara do atual (em 64 isso pesa
    mais); a face em 64 ficou mais clara e mais chapada que o azul-escuro do atual, e as emendas a deixam um pouco
    técnica; a peça central perdeu a base separada em 32 (ficou só a cúpula com o sulco). O próximo passo, se a
    direção servir: um reflexo de gomo maior em 64 e 48, com o gradiente do atual, e a face um degrau mais escura nos
    gomos de trás.</p>`;
})();
