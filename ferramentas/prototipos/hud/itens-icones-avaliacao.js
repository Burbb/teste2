/* A avaliação do experimento de itens e ícones (itens-icones-teste.html mostra): cada peça nos seis critérios, olhada
   no tamanho real, no jogo (capturas-itens-icones/ e capturas-roda/), e a recomendação. É a leitura de quem desenhou;
   a decisão é do Jean. */
"use strict";

window.AVALIACAO = (() => {
  const C = ["Reconhecimento imediato", "Contraste", "Coerência com o mundo", "Acabamento", "Perda de detalhe (32 px)", "Convivência com o que fica"];
  const PECAS = [
    ["Machado", ["Bom: a meia-lua com o fio claro diz machado de longe; hoje é o sprite pequeno do jogo a 2×.",
      "Bom: o fio claro e o cabo de madeira saem do carvão.", "Bom: os mesmos materiais e a mesma luz do martelo.",
      "Razoável: a lâmina ainda é um pouco reta embaixo.", "Nenhuma que importe.",
      "Bom ao lado do martelo; na mochila, ao lado da espada pintada, fica mais pixelado."],
      "Integrar."],
    ["Unguento de Prata", ["Bom: um pote aberto com algo prateado, diferente de todos os frascos.",
      "Bom: o barro claro e a prata saem do fundo.", "Bom: barro e madeira, como a curandeira e a feira.",
      "Bom.", "O cordão do gargalo quase some.",
      "Bom: separa o unguento das poções e deixa o sprite antigo só para a curandeira."],
      "Integrar."],
    ["Bomba de Fumaça", ["Muito melhor que a caveira (que hoje também é morte, bestiário e Largar).",
      "Fraco: a bola de barro escuro some no nicho escuro; só a fumaça e a faísca a recortam.",
      "Bom.", "A fumaça ainda sai em blocos.", "A faísca vira dois pixels.",
      "Bom."],
      "Integrar depois de clarear a bola um degrau e arredondar a fumaça."],
    ["Espada (candidata)", ["Igual à atual.", "Bom.", "Mais perto do estilo dos cenários que a pintada.",
      "Bom.", "Nenhuma.", "Sozinha, briga com o resto da família pintada (elmo, cota, manopla, botas)."],
      "Não trocar sozinha: só se a família inteira de equipamento migrar para o estilo dos cenários."],
    ["Escudo (candidato)", ["Bom: tábuas, aro e bossa dizem escudo de madeira.",
      "Bom.", "Muito bom: é o escudo das vilas e dos guardas.", "Bom.", "Os cravos ficam pequenos.",
      "Bom, e resolve uma confusão: hoje o escudo do item e o da Defesa são quase o mesmo desenho."],
      "Integrar (pede também a silhueta do espaço vazio)."],
    ["Anel (candidato)", ["Em 48 e 64, bom; em 32, o selo vira uma mancha dourada.",
      "Bom.", "Bom.", "Razoável.", "Grande: o selo gravado não sobrevive em 32.",
      "No espaço vazio (o anel 2), a silhueta vira uma bolha; a atual, com a pérola, lê melhor."],
      "Manter o atual por ora."],
    ["Grimório", ["Bom: um livro fechado, com fecho; em 36 e 32.", "Bom.",
      "Melhor que o roxo com a pedra: couro e latão, como o livro da capela.", "Bom.", "Nenhuma.",
      "Bom ao lado do Diário (livro aberto com a pena): os dois não se confundem."],
      "Integrar (vale para a doca e para Habilidades na roda)."],
    ["Talentos", ["Melhor que os três nós soltos: uma árvore com os nós nas pontas.", "Bom.",
      "Bom (madeira e latão).", "Razoável: de relance, lembra um candelabro.", "Nenhuma.", "Bom."],
      "Integrar, ou testar uma variante com folhas nos galhos."],
    ["Ataque", ["Bom: as espadas cruzadas são a força do golpe, não a espada do item.",
      "Bom em 32; em 24 as lâminas ficam finas.", "Bom.", "Bom.", "Em 24, as guardas viram pontos.",
      "Bom: deixa de repetir o desenho do item."],
      "Integrar; se 24 incomodar, engrossar as lâminas só nele."],
    ["Defesa", ["Igual à atual (escudo de bico).", "Bom.", "Bom.", "Bom.", "Nenhuma.",
      "Ganho pequeno; só faz sentido junto do escudo de madeira no item."],
      "Opcional: trocar junto do escudo do item."],
    ["Fugir", ["Bom: a bota em passo largo, com poeira e rastros.", "Bom.", "Bom.", "Bom.",
      "Os rastros viram três traços, o que basta.", "Resolve a repetição: hoje Fugir e Agilidade são a mesma bota com o raio."],
      "Integrar."],
    ["Roda: acabamento alternativo", ["Igual: a disposição, os nomes e as teclas são os de hoje.",
      "Placas mais escuras, texto creme com a mesma leitura; o mouse agora aparece (placa clareia e fio de latão).",
      "Ferro escuro e carvão, como o resto da HUD; o latão só no que está aberto ou sob o mouse.",
      "A tecla encaixada no canto do nicho, sem caixa solta; o indisponível com o desenho em cinza; o foco fino, separado do aberto.",
      "—", "A janelinha de Habilidades e Itens ganhou o mesmo carvão e o mesmo mouse."],
      "Integrar."],
  ];
  const linha = ([nome, notas, rec]) => `<tr><td><b>${nome}</b></td>${notas.map((n) => `<td>${n}</td>`).join("")}<td><b>${rec}</b></td></tr>`;
  return `<table><tr><th>peça</th>${C.map((c) => `<th>${c}</th>`).join("")}<th>recomendação</th></tr>${PECAS.map(linha).join("")}</table>`;
})();
