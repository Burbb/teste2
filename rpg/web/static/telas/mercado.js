/* Mercado: a banca do mercador numa faixa em cima e, embaixo, o ouro, três abas (Suprimentos, Equipamentos, Vender) e
   a lista da aba, a única parte que rola. Trocar de aba é só da tela: não fala
   com o motor, não passa tempo nem mexe no estoque. A aba, a rolagem de cada lista e a quantidade escolhida em cada
   suprimento sobrevivem ao redesenho depois de cada compra ou venda (não à saída do mercado). */
"use strict";

(() => {
  const { h, S, dica, dicaItem, equiparDaMochila, esconderDica, fecharMenuItem, iconeItem, moedasPara } = Telas;

  const ABAS = [["suprimentos", "Suprimentos"], ["equipamentos", "Equipamentos"], ["vender", "Vender"]];
  const qtdLoja = {};  // quantidade escolhida em cada suprimento
  let aba = "suprimentos";
  const rolagem = {};  // onde cada lista estava
  let visitaNova = true;  // a banca se revela só ao entrar (não a cada compra nem troca de aba)

  function maxCompra(c, ouro) { return Math.max(0, Math.min(99, c.limite ?? 99, Math.floor(ouro / c.preco))); }
  // o ícone do motivo: o próprio dele pelo `motivo_id` do motor (o Esgotado, o caixote), senão o cadeado
  const motivoHtml = (m, id) => `<span class="merc-motivo">${(id && Icones.motivo(id)) || S("cadeado", 1)}${h(m)}</span>`;

  function suprimento(c, ouro) {
    const max = maxCompra(c, ouro);
    const q = Math.max(1, Math.min(qtdLoja[c.id] || 1, max || 1));
    const tem = c.teto ? `${c.tem}/${c.teto}` : c.tem;
    const cheio = c.teto && c.tem >= c.teto;
    const motivo = c.motivo ? h(c.motivo) + (c.detalhe ? `. ${h(c.detalhe)}` : "") : "";
    return `<div role="button" tabindex="0" class="mercadoria suprimento${c.motivo ? " caro" : ""}" data-comprar="${h(c.id)}" data-preco="${c.preco}" data-max="${max}"
        ${dica(`<b>${h(c.nome)}</b><div>${Realce.texto(c.desc)}</div>${motivo ? `<div class="rodape">${motivo}</div>` : ""}`)}>
      <span class="slot-px">${Icones.consumivel(c.id) || Icones.porDesenho(c.icone) || S(c.icone || "pocao", 2)}</span>
      <span class="merc-nome">${h(c.nome)}</span>
      <span class="merc-contas"><span class="merc-bolsa${cheio ? " cheio" : ""}">Na bolsa: <b>${tem}</b></span><span class="merc-estoque${c.estoque ? "" : " esgotado"}">Estoque: <b>${c.estoque}</b></span></span>
      <span class="merc-acao"><span class="qtd-ctrl"><button type="button" data-q="-1" aria-label="menos ${h(c.nome)}">−</button><b aria-label="quantidade">${q}</b><button type="button" data-q="1" aria-label="mais ${h(c.nome)}">+</button></span>
        <span class="merc-total${c.sem_ouro ? " falta" : ""}" title="Preço total">${Icones.moeda() || S("moeda", 1)}<span class="total">${c.preco * q}</span></span></span>
      ${c.motivo ? motivoHtml(c.motivo, c.motivo_id) : ""}</div>`;
  }

  function equipamento(it, i) {
    return `<button type="button" class="mercadoria equip${it.motivo ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, it.motivo ? h(it.motivo) : "Se o espaço do corpo estiver vazio, você já sai vestindo.")}>
      <span class="slot-px r-${h(it.raridade)}">${Icones.item(iconeItem(it)) || S(iconeItem(it), 2)}</span>
      <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span>
      <span class="preco${it.sem_ouro ? " falta" : ""}">${Icones.moeda() || S("moeda", 1)}${it.preco}</span>${it.motivo ? motivoHtml(it.motivo) : ""}</button>`;
  }

  // Vender: a mochila como no inventário, uma grade com todos os espaços (os vazios também, apagados e fora do Tab).
  // Cada item mostra o ícone, a raridade e o que o mercador paga; a ficha (e a comparação, com Shift) vem na dica.
  // Clique vende na hora (o vendido vai para "Recomprar", pelo mesmo preço, até sair do mercado); o botão direito
  // equipa; arrastar até a banca também vende.
  //
  // Durante a visita, cada peça fica no espaço em que estava (arranjo): vender deixa o espaço vazio e as outras não
  // escorregam para ele; o que chega (a recompra, a peça que sai do corpo ao equipar) ocupa o primeiro espaço vazio.
  // Cada peça da grade tem uma ficha (data-peca) que não muda enquanto ela estiver no espaço: é ela que o pedido de
  // venda guarda, nunca a posição. data-mochila-loja é a posição de verdade na mochila do motor, refeita a cada
  // desenho. Ao sair do mercado, o arranjo some e a mochila volta à ordem de sempre.
  let arranjo = null;  // [{ n, a, i } | null] por espaço: n a ficha, a a assinatura (o que a peça é), i a posição na mochila
  let fichas = 0;
  const assinatura = (it) => JSON.stringify([it.nome, it.nivel, it.raridade, it.base, it.slot, it.bonus_bruto]);
  /** Encaixa a mochila de agora no arranjo da visita: cada espaço ocupado fica com a mesma peça, o que saiu deixa o
   *  espaço vazio e o que chegou vai para o primeiro vazio. A peça que a tela sabe que saiu (a vendida, a equipada)
   *  sai primeiro, pela ficha: entre peças iguais (três Martelos Enferrujados), o espaço que esvazia é o clicado. As
   *  outras se acham pelo que são, na ordem da mochila, que o motor não embaralha (tira do meio e põe no fim). */
  function arrumar(mochila, limite, sairam) {
    const novas = mochila.map((it, i) => ({ i, a: assinatura(it) }));
    const novo = Array.from({ length: Math.max(limite, mochila.length) }, () => null);
    const quantas = (lista, a) => lista.filter((x) => x && x.a === a).length;
    let antes = (arranjo || []).map((e, s) => e && { ...e, s }).filter(Boolean);
    for (const n of sairam) {  // só se de fato saiu uma daquelas (um pedido cancelado não tira nada)
      const e = antes.find((x) => x.n === n);
      if (e && quantas(novas, e.a) < quantas(antes, e.a)) antes = antes.filter((x) => x !== e);
    }
    let k = 0;
    for (const e of antes.sort((x, y) => x.i - y.i)) {  // a ordem de antes, casada em sequência com a de agora
      let j = k;
      while (j < novas.length && novas[j].a !== e.a) j++;
      if (j < novas.length && e.s < novo.length) { novo[e.s] = { n: e.n, a: e.a, i: novas[j].i }; novas[j] = { a: null }; k = j + 1; }
    }
    novas.forEach((l) => { if (l.a !== null) novo[novo.indexOf(null)] = { n: ++fichas, a: l.a, i: l.i }; });
    arranjo = novo;
  }
  const espacoDa = (n) => (arranjo || []).find((e) => e && e.n === n);
  function paraVender(it, e) {
    const venda = `<div class="preco-venda">${Icones.moeda() || S("moeda", 1)} O mercador paga <b>${it.preco}</b></div>` +
      (it.usavel ? "" : "Não é para a sua classe.");
    return `<div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.usavel ? "" : " inutil"}" draggable="true" data-mochila-loja="${e.i}" data-peca="${e.n}"
        aria-label="Vender ${h(it.nome)} por ${it.preco} de ouro" ${dicaItem(it, venda)}>${Icones.item(iconeItem(it)) || S(iconeItem(it), 2)}<span class="preco-canto">${it.preco}</span></div>`;
  }
  const VAZIA = '<div class="slot-px celula vazia" aria-hidden="true"></div>';
  function gradeVenda(d) {
    // a peça já pedida (vendida e esperando a resposta) aparece como o espaço vazio que vai ser
    const celulas = arranjo.map((e) => (e && !vendida(e.n) ? paraVender(d.mochila[e.i], e) : VAZIA));
    return `<div class="mochila-grade mochila-loja" role="group" aria-label="Mochila">${celulas.join("")}</div>`;
  }

  // Recomprar: só depois da primeira venda da visita; cada vendido com o preço que você recebeu (é o que ele cobra).
  function recompra(d) {
    if (!(d.recompra || []).length) return "";
    const itens = d.recompra.map((it, i) => `<div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.motivo ? " caro" : ""}" data-recomprar="${i}"
        aria-label="Recomprar ${h(it.nome)} por ${it.preco} de ouro" ${dicaItem(it, `<div class="preco-venda">${Icones.moeda() || S("moeda", 1)} Recomprar por <b>${it.preco}</b></div>${it.motivo ? h(it.motivo) : "Clique para desfazer a venda."}`)}>${Icones.item(iconeItem(it)) || S(iconeItem(it), 2)}<span class="preco-canto">${it.preco}</span></div>`).join("");
    return `<section class="loja-recompra" aria-label="Recomprar"><h5>Recomprar</h5><div class="mochila-grade mochila-loja recompra">${itens}</div></section>`;
  }

  function loja(d) {
    arrumar(d.mochila, d.limite, [emVoo, equipando]);
    emVoo = equipando = null;  // um mercado novo é a resposta do pedido que tinha ido
    const listas = {
      suprimentos: d.consumiveis.map((c) => suprimento(c, d.ouro)).join(""),
      equipamentos: d.equipamentos.map(equipamento).join("") || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>',
      vender: gradeVenda(d) + recompra(d),
    };
    const conta = { equipamentos: d.equipamentos.length, vender: d.mochila.length };
    const mochila = `<span class="loja-mochila">${S("saco", 1)} Mochila <b>${d.ocupado}/${d.limite}</b></span>`;
    const sub = {
      suprimentos: "",
      equipamentos: mochila,
      vender: `${mochila}<span class="loja-dica">${d.mochila.length ? "" : "Nada para vender."}</span>`,
    };
    const abas = ABAS.map(([id, nome]) => `<button type="button" role="tab" id="aba-${id}" class="loja-aba" data-aba="${id}" aria-controls="lista-${id}"
        aria-selected="${id === aba}" tabindex="${id === aba ? 0 : -1}">${nome}${conta[id] !== undefined ? ` <small>${conta[id]}</small>` : ""}</button>`).join("");
    const paineis = ABAS.map(([id]) => `<div class="loja-painel" role="tabpanel" id="lista-${id}" aria-labelledby="aba-${id}" data-painel="${id}"${id === aba ? "" : " hidden"}>
        ${sub[id] ? `<div class="loja-sub">${sub[id]}</div>` : ""}<div class="loja-lista${id === "vender" ? " venda" : " vitrine"}" data-lista="${id}">${listas[id]}</div></div>`).join("");
    return `<div class="tela loja${visitaNova ? " chegando" : ""}">
      <div class="loja-banca"><canvas class="banca-cena"></canvas></div>
      <div class="loja-lado">
        <div class="loja-topo"><span class="npc-retrato"><img src="${retratoMercador(2)}" srcset="${retratoMercador(4)} 2x" width="48" height="48" alt="O mercador" draggable="false"></span><div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
          <span class="ouro-loja" aria-label="seu ouro">${Icones.ouro() || S("moedas", 2)}${d.ouro}</span></div>
        <div class="loja-abas" role="tablist" aria-label="Mercado">${abas}</div>
        ${paineis}
      </div></div>`;
  }

  // ---------------------------------------------------------------- a banca
  /** Dentro do mercado, de frente para o balcão, numa faixa em cima dos produtos (em qualquer largura): uma vendinha
   *  de vila do Vale. A parede de tábuas velhas é dividida em vãos por postes, e cada vão mostra um grupo do que o
   *  mercado vende (curativos e frascos, provisões, uma peça de proteção, o arco e a aljava, tochas, sacos,
   *  ferramentas, cestos, caixotes e um barril), com paredes vazias entre eles para descansar o olho; a porta dos
   *  fundos e uma janela (dia ou noite). Os objetos são só ambientação: nada na faixa é clicável.
   *  Mais largura mostra mais vãos, nunca o desenho esticado. A luz de dentro é a da lamparina, à esquerda do mercador;
   *  a de fora (janela e porta) segue o período do jogo, e à noite o que fica longe da lamparina escurece. Atrás do balcão, o mercador: um homem mais velho, careca de franja grisalha,
   *  nariz comprido e sobrancelha desconfiada, túnica de lã crua com o capuz caído, avental de couro gasto e manchado,
   *  cinto com bolsa e chaves. Ele se apoia numa mão sobre o balcão; respira, pisca e, a cada oito segundos, pega um
   *  frasco, ergue contra a luz e devolve. Pixel art no estilo das paisagens, em escala inteira (pixel 2×). Ao entrar,
   *  a faixa se revela num pontilhado que se fecha; comprar ou trocar de aba não recomeça nada. Com movimento
   *  reduzido, fica parada. */
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  let relogio0 = 0;  // quando a visita começou: o ritmo do mercador segue o mesmo entre um redesenho e outro
  const COR = {
    parede: "#1e1712", tabuas: ["#211913", "#1b140f", "#241b14", "#1d1611"], fresta: "#130e0a", no: "#15100b",
    viga: "#2e2216", vigaLuz: "#3e2e1e", poste: "#2a1e14", posteLuz: "#3a2a1c", posteSombra: "#120c08",
    prateleira: "#4a3624", prateleiraLuz: "#6a5034", prateleiraSombra: "#24190f",
    caixa: "#5a4630", caixaLuz: "#6e5638", caixaSombra: "#3a2c1c",
    pano: "#8a7e66", panoLuz: "#a89a7c", panoSombra: "#5e5444", barbante: "#3a2c1c",
    couro: "#5a3c24", couroLuz: "#704c2e", couroSombra: "#3a2616", ferro: "#4a4a50", ferroLuz: "#8a8a92",
    pao: "#a07a44", paoLuz: "#c09a5a", queijo: "#b89a4a", carne: "#5a2a1e", carneLuz: "#7a3a2a",
    bandagem: "#d8d0bc", bandagemSombra: "#a8a090", barro: "#7a4a2e", barroLuz: "#9a6040", barroSombra: "#4e2e1c",
    haste: "#8a6a44", pena: "#c8c0b0", penaCor: "#9a3a2a", corda: "#9a845a", piche: "#2a2018",
    saco: "#8a7454", sacoSombra: "#5a4a34", cortina: "#5a2a22", cortinaSombra: "#3e1c16", cortinaRemendo: "#6a4a2e",
    balcao: "#5a4028", balcaoLuz: "#7a5a38", balcaoFundo: "#3e2c1a", balcaoBorda: "#2a1c10",
    frente: ["#3a2818", "#34241a", "#3e2c1c"], frenteLinha: "#22160c",
    pele: "#b07a56", peleLuz: "#d09a70", peleSombra: "#7e5236", olho: "#120c08", boca: "#3a2418",
    cabelo: "#8a8478", cabeloSombra: "#5e5a52", cabeloLuz: "#a8a296", barbaLuz: "#9a9488", capuzLuz: "#5e6850", sobrancelha: "#4a463e", barba: "#7a7266", barbaSombra: "#5a544a",
    capuz: "#4e5640", capuzSombra: "#363c2c", tunica: "#6e6046", tunicaLuz: "#8a7a5a", tunicaSombra: "#4a402e",
    avental: "#5a3e28", aventalSombra: "#3e2a1a", mancha: "#4a3220", cinto: "#2a1c12", fivela: "#a89a62",
    bolsa: "#7a5634", bolsaSombra: "#5a3e24",
  };
  // A luz de fora, pelo período do jogo (0 manhã, 1 tarde, 2 anoitecer, 3 noite): o vidro da janela, o brilho em cima
  // dele, a fresta embaixo da porta, a força da lamparina e o quanto a loja escurece longe dela. Só a janela, a porta
  // e o escuro mudam; o resto da loja guarda as cores.
  const LUZ_DE_FORA = [
    { vidro: "#b4ae8c", brilho: "#d4ceb0", fresta: "rgba(220,214,180,0.25)", lamparina: 0.55, escuro: 0 },
    { vidro: "#dccb92", brilho: "#f4e8c4", fresta: "rgba(240,224,170,0.4)", lamparina: 0.5, escuro: 0 },
    { vidro: "#b0683e", brilho: "#d08850", fresta: "rgba(220,130,70,0.28)", lamparina: 0.8, escuro: 0.5 },
    { vidro: "#1a2640", brilho: "#22304e", fresta: null, lamparina: 1, escuro: 1 },
  ];
  // O mercador, da careca ao peito (21 colunas; o meio é a coluna 10). O resto do tronco repete a última linha até o
  // balcão; o cinto, a bolsa e as chaves entram na altura da cintura. Letras: L/s/d pele (luz, meio, sombra), k/K
  // franja grisalha, w sobrancelha, e olho, n nariz, B/b barba, M boca, c/C capuz caído, u/t/T túnica de lã,
  // a/A avental de couro, x mancha no couro.
  const FIGURA = [
    "........LLssd........",
    ".......LLsssdd.......",
    "......kLssssddk......",
    "......kwwsswwdk......",
    "......kLeLsedKk......",
    "......KLssnsddK......",
    "......KBLnnsbBK......",
    ".......BBMMBbb.......",
    ".......BBBBBbb.......",
    "........BBBbb........",
    ".....ccccBbbCCC......",
    "....ccttttttttCCC....",
    "...uuttaaaaaaAttTT...",
    "...uuttaaaaaaAttTT...",
    "...uuttaaxaaaAttTT...",
    "...uuttaaaaaaAttTT...",
    "...uuttaaaaxaAttTT...",
  ];
  const TINTA = {
    L: "peleLuz", s: "pele", d: "peleSombra", k: "cabelo", K: "cabeloSombra", w: "sobrancelha", e: "olho",
    n: "peleSombra", B: "barba", b: "barbaSombra", M: "boca", c: "capuz", C: "capuzSombra", u: "tunicaLuz",
    t: "tunica", T: "tunicaSombra", a: "avental", A: "aventalSombra", x: "mancha",
  };
  // O mesmo homem de perto, no balcão da loja (busto de 24×24, mostrado a 48 px): a figura da banca com as mesmas
  // cores e um pouco mais de desenho, onde o tamanho deixa (a luz na franja, na barba e no capuz, as rugas da testa, os
  // olhos sob a sobrancelha pesada, a alça do avental). A luz vem da esquerda, como a lamparina. Letras da FIGURA e
  // mais: h/H/g a luz da franja, da barba e do capuz; y a alça de couro.
  const RETRATO = [
    "........................",
    "..........LLLsd.........",
    "........LLLLLssdd.......",
    ".......LLLLsssssdd......",
    ".......LLssssssssd......",
    "......hLsssddssddsdK....",
    "......kLsssssssssdK.....",
    "......kwwwLssssLwwwK....",
    ".....dkLweesssseewdKd...",
    ".....dkLsssLsnsssddKd...",
    "......kLssssLnnssddK....",
    "......kKsssLsnnsddKK....",
    "......KBBsdLnnndBbbK....",
    ".......BHBBdMMMdBbb.....",
    ".......BHBBBBBBBbbb.....",
    "........BHBBBBBbbb......",
    ".........BBBBBbbb.......",
    ".......ccgBBBbbCCC......",
    ".....ccgcccdddCCCCCC....",
    "...uuuuccgcccCCCCCttTT..",
    "..uuuuttayaaaaaaAAttTTT.",
    "..uuuttaayaaaaaaAAtttTT.",
    ".uuuuttaaaaaxaaaAAtttTTT",
    ".uuuuttaaaaaaaaaAAtttTTT",
  ];
  const TINTA_RETRATO = { ...TINTA, h: "cabeloLuz", H: "barbaLuz", g: "capuzLuz", y: "couroLuz" };
  const CORES_RETRATO = Object.fromEntries(Object.entries(TINTA_RETRATO).map(([letra, tinta]) => [letra, COR[tinta]]));
  /** O busto pintado com `escala` pixels de tela por pixel da arte (×2 no balcão, ×4 para telas densas). */
  const retratoMercador = (escala) => Sprites.grade("mercador", RETRATO, CORES_RETRATO, escala);

  // Os vãos da parede, do mercador para fora (o primeiro de cada lado encosta nele). Larguras em pixels da arte.
  const VAOS = {
    esquerda: [["curativos", 28], ["descanso", 10], ["protecao", 22], ["janela", 18], ["sacos", 30], ["descanso", 12],
      ["tochas", 20], ["ferramentas", 26], ["descanso", 10], ["caixas", 26], ["curativos", 28], ["porta", 18], ["descanso", 14]],
    direita: [["provisoes", 30], ["descanso", 10], ["arco", 24], ["cestos", 26], ["porta", 18], ["caixas", 26],
      ["descanso", 12], ["tochas", 20], ["janela", 18], ["protecao", 22], ["descanso", 10], ["provisoes", 30], ["descanso", 14]],
  };

  function banca(caixa, revelar) {
    const canvas = caixa.querySelector(".banca-cena"), c = canvas.getContext("2d");
    const cw = Math.max(1, caixa.clientWidth), ch = Math.max(1, caixa.clientHeight);
    const W = Math.max(160, Math.round(cw / 2)), H = Math.max(40, Math.min(56, Math.round(ch / 2)));
    canvas.width = W; canvas.height = H;
    const px = (x, y, w, hh, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
    const periodo = (App.estado && App.estado.mundo && App.estado.mundo.periodo_n) || 0, noite = periodo === 3;
    const fora = LUZ_DE_FORA[periodo] || LUZ_DE_FORA[0];
    const topo = H - 11;        // a borda de trás do tampo do balcão (o balcão fica sempre embaixo)
    const frente = topo + 4;    // a quina da frente
    const S1 = topo - 18, S2 = topo - 8;  // as duas prateleiras
    const mx = Math.round(W / 2);
    const lampada = [mx - 30, Math.max(1, S1 - 12)];
    if (revelar || !relogio0) relogio0 = performance.now();
    let timer = null;

    // ------------------------------------------------ pequenas coisas
    function prateleira(y, x0, x1) {
      px(x0, y, x1 - x0, 1, COR.prateleiraLuz); px(x0, y + 1, x1 - x0, 1, COR.prateleira); px(x0, y + 2, x1 - x0, 1, COR.prateleiraSombra);
      px(x0, y + 3, x1 - x0, 1, "rgba(0,0,0,0.25)");
      px(x0 + 1, y + 3, 1, 2, COR.prateleiraSombra); px(x1 - 2, y + 3, 1, 2, COR.prateleiraSombra);  // as mãos-francesas
    }
    function frasco(x, y, cor) { px(x + 1, y, 1, 1, "#6a5034"); px(x + 1, y + 1, 1, 1, "#9a9aa0"); px(x, y + 2, 3, 3, cor); px(x, y + 2, 1, 1, "rgba(255,255,255,0.35)"); px(x + 2, y + 4, 1, 1, "rgba(0,0,0,0.35)"); }
    function pote(x, y, w, alto) {
      px(x + 1, y, w - 2, 1, COR.barroSombra); px(x, y + 1, w, alto - 1, COR.barro); px(x, y + 1, 1, alto - 1, COR.barroLuz);
      px(x + w - 1, y + 1, 1, alto - 1, COR.barroSombra); px(x, y + 2, w, 1, COR.barroSombra);
    }
    function saco(x, y) { px(x + 1, y, 3, 1, COR.sacoSombra); px(x + 2, y - 1, 1, 1, COR.barbante); px(x, y + 1, 5, 4, COR.saco); px(x + 4, y + 1, 1, 4, COR.sacoSombra); px(x + 1, y + 1, 1, 1, "#a8946c"); }
    function caixote(x, y, w, alto) {
      px(x, y, w, alto, COR.caixa); px(x, y, w, 1, COR.caixaLuz); px(x, y + alto - 1, w, 1, COR.caixaSombra);
      for (let k = x + 3; k < x + w - 1; k += 4) px(k, y + 1, 1, alto - 2, COR.caixaSombra);
      px(x, y, 1, alto, COR.caixaSombra); px(x + w - 1, y, 1, alto, COR.caixaSombra);
    }
    function embrulho(x, y) {  // provisão embrulhada em pano, amarrada em cruz
      px(x, y, 6, 4, COR.pano); px(x, y, 6, 1, COR.panoLuz); px(x + 5, y + 1, 1, 3, COR.panoSombra);
      px(x + 3, y, 1, 4, COR.barbante); px(x, y + 2, 6, 1, COR.barbante);
    }
    function poste(x) { px(x, 2, 3, topo - 2, COR.poste); px(x, 2, 1, topo - 2, COR.posteLuz); px(x + 2, 2, 1, topo - 2, COR.posteSombra); }
    const quadro = () => Math.floor((performance.now() - relogio0) / 100);

    // ------------------------------------------------ os vãos
    const VAO = {
      descanso(x, w) { poste(x + Math.floor(w / 2) - 1); },
      curativos(x, w, v) {
        prateleira(S1, x + 1, x + w - 1); prateleira(S2, x + 1, x + w - 1);
        // em cima: os rolos de bandagem empilhados e dois frascos
        [[3, 0], [8, 0], [5, -3]].forEach(([dx, dy]) => { px(x + dx, S1 - 3 + dy, 4, 3, COR.bandagem); px(x + dx + 3, S1 - 3 + dy, 1, 3, COR.bandagemSombra); px(x + dx + 1, S1 - 2 + dy, 1, 1, COR.bandagemSombra); });
        frasco(x + 16, S1 - 5, "#8a2a26"); frasco(x + 21, S1 - 5, v % 2 ? "#2a5a7a" : "#3a6a3a");
        // embaixo: os potes de barro e um frasco de antídoto
        pote(x + 3, S2 - 6, 5, 6); pote(x + 10, S2 - 4, 4, 4); frasco(x + 18, S2 - 5, "#3a6a3a");
      },
      provisoes(x, w, v) {
        prateleira(S1, x + 1, x + w - 1); prateleira(S2, x + 1, x + w - 1);
        // em cima: os pães e o queijo; embaixo: as provisões embrulhadas e um saquinho
        [[3, 0], [10, 0]].forEach(([dx]) => { px(x + dx, S1 - 3, 6, 3, COR.pao); px(x + dx + 1, S1 - 3, 4, 1, COR.paoLuz); px(x + dx, S1 - 1, 6, 1, "#7a5a30"); });
        px(x + 18, S1 - 3, 6, 3, COR.queijo); px(x + 18, S1 - 3, 6, 1, "#d8ba6a"); px(x + 22, S1 - 2, 2, 2, "#8a6a2a");
        embrulho(x + 3, S2 - 4); embrulho(x + 11, S2 - 4); if (v % 2 === 0) saco(x + 20, S2 - 5);
        // penduradas na viga: tiras de carne seca e o odre de água
        for (let k = 0; k < 3; k++) { px(x + 5 + k * 2, 2, 1, 1, COR.barbante); px(x + 5 + k * 2, 3, 1, 4 + (k % 2), COR.carne); px(x + 5 + k * 2, 3, 1, 1, COR.carneLuz); }
        const ox = x + w - 8;
        px(ox + 2, 2, 1, 2, COR.barbante); px(ox + 1, 4, 3, 1, COR.couroSombra); px(ox, 5, 5, 5, COR.couro); px(ox, 5, 1, 4, COR.couroLuz); px(ox + 4, 6, 1, 4, COR.couroSombra); px(ox + 1, 10, 3, 1, COR.couroSombra);
      },
      protecao(x, w, v) {
        // a peça de proteção pendurada: um gibão de couro num cabide; ao lado, um broquel de madeira com aro de ferro
        px(x + 1, S1 - 10, w - 2, 1, COR.prateleiraSombra);  // a régua dos cabides
        const gx = x + 3, gy = S1 - 9;
        px(gx + 4, gy, 1, 2, COR.ferro);
        px(gx, gy + 2, 9, 3, COR.couro); px(gx + 1, gy + 5, 7, 8, COR.couro); px(gx, gy + 2, 2, 2, COR.couroLuz);
        px(gx + 1, gy + 5, 1, 8, COR.couroLuz); px(gx + 7, gy + 5, 1, 8, COR.couroSombra); px(gx + 3, gy + 2, 3, 1, COR.couroSombra);
        for (let y = gy + 5; y < gy + 13; y += 2) px(gx + 4, y, 1, 1, COR.corda);  // os cordões da frente
        const bx = x + w - 7, by = S2 - 7, r = v % 2 ? 4 : 3;
        for (let y = -r; y <= r; y++) for (let k = -r; k <= r; k++) {
          const d = k * k + y * y;
          if (d <= r * r) px(bx + k, by + y, 1, 1, d > (r - 1) * (r - 1) ? COR.ferro : (k + y < 0 ? COR.caixaLuz : COR.caixa));
        }
        px(bx, by, 1, 1, COR.ferroLuz);
      },
      arco(x, w) {
        // o arco pendurado (a madeira curva e a corda reta) e a aljava com as penas para fora
        const ax = x + 4, ay0 = S1 - 9, alto = 18;
        for (let y = 0; y <= alto; y++) { const dx = Math.round(Math.sin((y / alto) * Math.PI) * 3); px(ax - dx, ay0 + y, 1, 1, y % 6 === 0 ? COR.couroLuz : "#6a4a2a"); }
        px(ax, ay0 + 1, 1, alto - 1, "#c8c0a8"); px(ax, ay0 - 1, 1, 1, COR.ferro);
        const qx = x + 10, qy = S1 - 5;
        px(qx, qy, 4, 10, COR.couro); px(qx, qy, 1, 10, COR.couroLuz); px(qx + 3, qy, 1, 10, COR.couroSombra); px(qx, qy + 3, 4, 1, COR.couroSombra);
        [[0, COR.pena], [1, COR.penaCor], [2, COR.pena]].forEach(([k, cor]) => { px(qx + k + 0.5, qy - 3 + (k % 2), 1, 3, COR.haste); px(qx + k + 0.5, qy - 4 + (k % 2), 1, 2, cor); });
        px(qx + 1, qy - 7, 1, 2, COR.couroSombra); px(qx + 1, qy - 8, 1, 1, COR.ferro);
        // na prateleira de baixo, um feixe de flechas amarrado, deitado
        prateleira(S2, x + w - 12, x + w - 1);
        for (let k = 0; k < 3; k++) px(x + w - 11, S2 - 1 - k, 9, 1, COR.haste);
        px(x + w - 11, S2 - 3, 1, 3, COR.ferroLuz); px(x + w - 3, S2 - 3, 2, 3, COR.pena); px(x + w - 2, S2 - 2, 1, 1, COR.penaCor);
        px(x + w - 7, S2 - 3, 1, 3, COR.barbante);
      },
      tochas(x, w) {
        prateleira(S2, x + 1, x + w - 1);
        // um caixote de tochas na prateleira de baixo, os cabos para cima e as cabeças de piche
        caixote(x + 3, S2 - 4, 11, 4);
        [[4, 7], [6, 6], [8, 8], [10, 6], [12, 7]].forEach(([dx, h]) => { px(x + dx, S2 - 4 - h, 1, h, COR.haste); px(x + dx, S2 - 4 - h, 2, 2, COR.piche); });
        // uma tocha apagada no suporte de ferro da parede
        const sx = x + w - 5, sy = S1 - 4;
        px(sx - 1, sy + 3, 3, 1, COR.ferro); px(sx, sy - 2, 1, 6, COR.haste); px(sx - 1, sy - 3, 3, 2, COR.piche);
      },
      sacos(x, w, v) {
        prateleira(S1, x + 1, x + w - 1);
        // em cima: um rolo de corda e as ferramentas (machadinha, martelo); embaixo: sacos e um caixote
        const rx = x + 5, ry = S1 - 3;
        for (let a = 0; a < 16; a++) px(Math.round(rx + Math.cos(a / 16 * Math.PI * 2) * 3), Math.round(ry + Math.sin(a / 16 * Math.PI * 2) * 2), 1, 1, a % 3 ? COR.corda : "#7a6a46");
        px(x + 13, S1 - 6, 1, 6, COR.haste); px(x + 12, S1 - 6, 3, 2, COR.ferroLuz);
        px(x + 19, S1 - 5, 1, 5, COR.haste); px(x + 17, S1 - 6, 5, 2, COR.ferro);
        saco(x + 3, S2 + 2); saco(x + 9, S2 + 2); saco(x + 6, S2 - 2);
        caixote(x + 16, S2 - 1, 10, topo - S2 + 1);
        if (v % 2) saco(x + 18, S2 - 6);
      },
      cestos(x, w) {
        prateleira(S2, x + 1, x + w - 1);
        // uma réstia de alho pendurada na viga; na prateleira, dois cestos de vime (maçãs e nabos)
        px(x + 5, 2, 1, 2, COR.barbante);
        for (let y = 4; y < 4 + 9; y += 2) { px(x + 4 + (y % 4 ? 1 : 0), y, 2, 2, "#d8d0bc"); px(x + 5 + (y % 4 ? 1 : 0), y + 1, 1, 1, "#a8a090"); }
        [[x + 3, "#8a2a22", "#b04a3a"], [x + 14, "#d8d0bc", "#7a4a7a"]].forEach(([cx, a1, a2]) => {
          for (let k = 0; k < 4; k++) { px(cx + k * 2 + 1, S2 - 5, 2, 2, k % 2 ? a1 : a2); }
          for (let y = S2 - 4; y < S2; y++) for (let k = 0; k < 10; k++) px(cx + k, y, 1, 1, (k + y) % 2 ? "#8a6a3a" : "#6a4e2a");
          px(cx, S2 - 4, 10, 1, "#a07a44");
        });
      },
      ferramentas(x, w) {
        prateleira(S2, x + 1, x + w - 1);
        // a régua das ferramentas: martelo, torquês e um serrote; embaixo, uma lanterna apagada e a caixa de pregos
        px(x + 1, S1 - 9, w - 2, 1, COR.prateleiraSombra);
        px(x + 4, S1 - 8, 1, 7, COR.haste); px(x + 3, S1 - 8, 3, 2, COR.ferroLuz);
        px(x + 9, S1 - 8, 1, 6, COR.ferro); px(x + 11, S1 - 8, 1, 6, COR.ferro); px(x + 10, S1 - 5, 1, 1, COR.ferroLuz);
        px(x + 15, S1 - 8, 2, 3, COR.haste); px(x + 17, S1 - 7, 6, 3, COR.ferroLuz);
        for (let k = 0; k < 6; k += 2) px(x + 17 + k, S1 - 4, 1, 1, COR.ferro);
        px(x + 4, S2 - 6, 4, 1, COR.ferro); px(x + 4, S2 - 5, 4, 4, "#3a3428"); px(x + 5, S2 - 4, 2, 2, "#6a6050"); px(x + 4, S2 - 1, 4, 1, COR.ferro);
        caixote(x + 13, S2 - 3, 9, 3);
      },
      caixas(x, w) {
        // caixotes empilhados no chão atrás do balcão e um barril de tampa
        caixote(x + 2, topo - 7, 12, 7); caixote(x + 4, topo - 13, 9, 6);
        const bx = x + 16;
        px(bx, topo - 11, 8, 11, COR.couro); px(bx, topo - 11, 1, 11, COR.couroLuz); px(bx + 7, topo - 11, 1, 11, COR.couroSombra);
        px(bx, topo - 9, 8, 1, COR.ferro); px(bx, topo - 3, 8, 1, COR.ferro); px(bx - 1, topo - 12, 10, 1, COR.caixaLuz);
      },
      porta(x, w) {
        // a porta dos fundos, com a cortina gasta e remendada; de dia, a luz escapa embaixo
        px(x + 1, 3, w - 2, topo - 3, "#0e0a07"); px(x + 1, 3, w - 2, 1, COR.poste);
        px(x + 3, 4, w - 6, topo - 4, COR.cortina);
        for (let y = 4; y < topo; y++) { px(x + 5 + (y % 4 === 0 ? 1 : 0), y, 1, 1, COR.cortinaSombra); px(x + w - 7, y, 1, 1, COR.cortinaSombra); }
        px(x + 7, Math.round(topo * 0.5), 3, 3, COR.cortinaRemendo);
        if (fora.fresta) px(x + 3, topo - 1, w - 6, 1, fora.fresta);
      },
      janela(x, w) {
        // a janela com as folhas abertas: a luz de fora pelo período (à noite, o azul com uma estrela)
        const jx = x + 4, jy = S1 - 9, jw = w - 8, jh = 11;
        px(jx - 1, jy - 1, jw + 2, jh + 2, COR.poste);
        px(jx, jy, jw, jh, fora.vidro); px(jx, jy, jw, 2, fora.brilho);
        if (noite) px(jx + 2, jy + 3, 1, 1, "#c8d8f0");
        px(jx + Math.floor(jw / 2), jy, 1, jh, COR.poste); px(jx, jy + 5, jw, 1, COR.poste);
        px(jx - 3, jy, 2, jh, COR.caixaSombra); px(jx + jw + 1, jy, 2, jh, COR.caixaSombra);  // as folhas abertas
        px(jx - 2, jy + jh + 1, jw + 4, 1, COR.prateleiraLuz);  // o parapeito
      },
    };

    // ------------------------------------------------ a cena
    function parede() {
      px(0, 0, W, topo, COR.parede);
      for (let x = 0, k = 0; x < W; x += 6, k++) {  // tábuas de larguras e tons diferentes, com frestas e nós
        px(x, 0, 6, topo, COR.tabuas[(k * 7 + (k >> 2)) % 4]); px(x, 0, 1, topo, COR.fresta);
        if (k % 5 === 2) px(x + 3, 6 + (k * 11) % Math.max(1, topo - 10), 2, 1, COR.no);
      }
      // os vãos, para os dois lados a partir do mercador; atrás dele, parede lisa com a prateleira de baixo vazia
      prateleira(S2, mx - 13, mx + 13);
      poste(mx - 15); poste(mx + 13);
      for (const [lado, sinal] of [["esquerda", -1], ["direita", 1]]) {
        let x = sinal < 0 ? mx - 15 : mx + 16, v = 0;
        for (let i = 0; ; i++) {
          const [tipo, w] = VAOS[lado][i % VAOS[lado].length];
          const x0 = sinal < 0 ? x - w : x;
          if (x0 > W || x0 + w < 0) break;
          VAO[tipo](x0, w, v++ + (sinal > 0 ? 1 : 0));
          x += sinal * w;
        }
      }
      // a viga do teto
      px(0, 0, W, 2, COR.viga); px(0, 1, W, 1, COR.vigaLuz); px(0, 2, W, 1, "rgba(0,0,0,0.3)");
    }
    function lamparina() {
      const [lx, ly] = lampada, forca = fora.lamparina, raio = Math.round(10 + forca * 6) + (reduzido() ? 0 : (quadro() % 3) - 1);
      for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
        const d2 = (x * x + y * y) / (raio * raio);
        if (d2 < 1 && Sprites.pontilha(lx + x, ly + 6 + y, Math.round((1 - d2) * 8 * forca))) px(lx + x, ly + 6 + y, 1, 1, "rgba(255,190,110,0.22)");
      }
      px(lx, 0, 1, ly + 3, "#2a2016"); px(lx - 2, ly + 3, 5, 6, "#3a2a18"); px(lx - 1, ly + 4, 3, 4, forca > 0.7 ? "#ffd27a" : "#e8a050");
      px(lx, ly + 5, 1, 2, "#fff0b0");
    }
    // À noite (e, mais de leve, ao anoitecer), longe da lamparina, a loja escurece em degraus (anéis de pixel inteiro,
    // como a luz das paisagens).
    function escuro() {
      if (!fora.escuro) return;
      const [lx, ly] = lampada, degraus = [[0.55, 0.18], [0.85, 0.3], [1.25, 0.42]];
      for (let y = 0; y < H; y++) {
        let x0 = 0, nivel = -1;
        for (let x = 0; x <= W; x++) {
          const d = x < W ? Math.hypot(x - lx, (y - ly) * 1.6) / 80 : Infinity;
          const n = x < W ? degraus.filter(([lim]) => d > lim).length - 1 : -2;
          if (n !== nivel) { if (nivel >= 0) px(x0, y, x - x0, 1, `rgba(6,8,18,${degraus[nivel][1] * fora.escuro})`); x0 = x; nivel = n; }
        }
      }
    }
    function mercador(t) {
      const quieto = reduzido(), respira = quieto ? 0 : Math.floor(t / 1.4) % 2;
      const y0 = topo - 26 + respira, ox = mx - 10;
      const pisca = !quieto && t % 4.3 < 0.15;
      const cinto = topo - 3 - y0;
      for (let r = 0; r <= topo - y0; r++) {
        const linha = FIGURA[Math.min(r, FIGURA.length - 1)], inclina = r <= 9 ? -1 : 0;  // a cabeça pende para a mão apoiada
        for (let k = 0; k < linha.length; k++) {
          let ch = linha[k];
          if (ch === ".") continue;
          if (r >= FIGURA.length && ch === "x") ch = "a";
          if (ch === "e" && pisca) ch = "d";
          const cor = r === cinto ? (k === 9 ? COR.fivela : COR.cinto) : COR[TINTA[ch]];
          px(ox + k + inclina, y0 + r, 1, 1, cor);
        }
      }
      // a bolsa no cinto e as chaves
      px(ox + 4, y0 + cinto + 1, 3, 3, COR.bolsa); px(ox + 4, y0 + cinto + 1, 3, 1, COR.bolsaSombra); px(ox + 6, y0 + cinto + 2, 1, 2, COR.bolsaSombra);
      px(ox + 15, y0 + cinto + 1, 1, 2, COR.ferroLuz); px(ox + 14, y0 + cinto + 3, 2, 1, COR.ferro);
      // o braço do lado da luz: desce do ombro, a manga arregaçada, até a mão espalmada no tampo (desenhada depois)
      const ombro = y0 + 12;
      for (let y = ombro; y < topo - 3; y++) { px(ox + 1, y, 2, 1, y < topo - 7 ? COR.tunicaLuz : COR.tunica); px(ox + 3, y, 1, 1, COR.tunicaSombra); }
      px(ox + 1, topo - 3, 3, 1, COR.tunicaSombra);  // a manga arregaçada, no cotovelo
    }
    function maos(t) {
      const ox = mx - 10;
      // a mão apoiada: o antebraço desce do cotovelo, o punho encosta no tampo e a palma fica espalmada nele, com os
      // dedos para a frente e a sombra embaixo
      px(ox + 1, topo - 2, 2, 2, COR.pele); px(ox + 1, topo - 2, 1, 2, COR.peleLuz);
      px(ox + 1, topo, 2, 1, COR.peleSombra);
      px(ox, topo + 1, 4, 1, COR.peleLuz); px(ox, topo + 2, 4, 1, COR.pele); px(ox + 3, topo + 1, 1, 2, COR.peleSombra);
      px(ox, topo + 3, 4, 1, "rgba(0,0,0,0.35)");
      const quieto = reduzido(), respira = quieto ? 0 : Math.floor(t / 1.4) % 2;
      const ombro = [mx + 6, topo - 26 + respira + 12];
      const ciclo = quieto ? 0 : t % 8;
      const alvo = [mx + 13, topo + 1];
      let mao = [mx + 6, topo + 1], ergue = 0;
      if (ciclo > 4.6 && ciclo < 7.6) {
        const ida = Math.min(1, (ciclo - 4.6) / 0.6), volta = Math.min(1, Math.max(0, (7.6 - ciclo) / 0.6));
        mao = [Math.round(mao[0] + (alvo[0] - mao[0]) * Math.min(ida, volta)), mao[1]];
        if (ciclo > 5.3 && ciclo < 6.9) ergue = Math.round(Math.min(1, (ciclo - 5.3) / 0.3, (6.9 - ciclo) / 0.3) * 9);
      }
      const [hx, hy] = [mao[0], mao[1] - ergue];
      for (let k = 0; k <= 8; k++) {
        const x = Math.round(ombro[0] + (hx - ombro[0]) * (k / 8)), y = Math.round(ombro[1] + (hy - ombro[1]) * (k / 8));
        px(x, y, 2, 2, k < 5 ? COR.tunicaSombra : COR.peleSombra);
      }
      px(hx, hy, 3, 2, COR.pele); px(hx, hy, 1, 1, COR.peleLuz);
      const fx = ergue ? hx : alvo[0], fy = ergue ? hy - 5 : topo - 3;
      frasco(fx, fy, "#8a2a26");
      if (ergue > 3) px(fx + 1, fy + 3, 1, 1, "#ff9a8a");  // a luz da lamparina atravessa o vidro
    }
    function bancada() {
      // o tampo: a borda de trás no escuro, as tábuas com os veios, a quina da frente pegando a luz
      px(0, topo, W, 1, COR.balcaoFundo); px(0, topo + 1, W, 2, COR.balcao);
      for (let x = 2; x < W; x += 9) px(x, topo + 1 + (x % 2), 4, 1, COR.balcaoLuz);
      for (let x = 17; x < W; x += 31) px(x, topo + 1, 1, 2, COR.balcaoFundo);
      px(0, frente - 1, W, 1, COR.balcaoLuz); px(0, frente, W, 1, COR.balcaoBorda);
      // a frente: tábuas de tons diferentes, a sombra embaixo da quina e as ferragens (cantoneiras com rebites)
      for (let x = 0, k = 0; x < W; x += 9, k++) { px(x, frente + 1, 9, H - frente - 1, COR.frente[(k * 5) % 3]); px(x, frente + 2, 1, H - frente - 2, COR.frenteLinha); }
      px(0, frente + 1, W, 1, "#22160c");
      px(0, frente + 3, W, 1, "#2a2a2c");  // a cinta de ferro, com os rebites
      for (let x = (mx % 18); x < W; x += 18) px(x, frente + 3, 1, 1, "#5a5a60");
      // em cima do tampo: o livro de contas, a balança, as moedas, um embrulho, a faca e o feixe de flechas
      const lx = mx - 46;
      px(lx, topo + 1, 9, 2, "#d8ccaa"); px(lx + 4, topo + 1, 1, 2, COR.couroSombra); px(lx + 1, topo + 1, 2, 1, "#8a7e66"); px(lx + 6, topo + 2, 2, 1, "#8a7e66");
      const bx = mx - 30;
      px(bx + 3, topo - 6, 1, 8, "#5a4a3a"); px(bx, topo - 6, 7, 1, "#8a7a5a");
      const pesa = reduzido() ? 0 : Math.round(Math.sin(quadro() / 11));
      px(bx - 1, topo - 5 + pesa, 3, 1, "#8a7a5a"); px(bx + 5, topo - 5 - pesa, 3, 1, "#8a7a5a");
      px(bx + 1, topo + 2, 5, 1, "#3a2a1a");
      const mo = mx + 22;
      [[0, 0], [1, -1], [0, -2], [1, -3]].forEach(([dx, dy]) => { px(mo + dx, topo + 2 + dy, 4, 1, "#e2bd63"); px(mo + dx + 3, topo + 2 + dy, 1, 1, "#a07a2a"); });
      embrulho(mx + 32, topo - 2);
      px(mx - 60, topo + 2, 5, 1, COR.ferroLuz); px(mx - 55, topo + 2, 3, 1, COR.couroSombra);
      for (let k = 0; k < 2; k++) px(mx + 44, topo + 1 + k, 10, 1, COR.haste);
      px(mx + 44, topo + 1, 1, 2, COR.ferroLuz); px(mx + 52, topo + 1, 2, 2, COR.pena);
      saco(mx + 64, topo - 3); saco(mx - 74, topo - 3);
    }
    function cena() {
      if (!canvas.isConnected) { clearInterval(timer); return; }
      const t = (performance.now() - relogio0) / 1000;
      parede();
      lamparina();
      mercador(t);
      bancada();
      maos(t);
      escuro();
      if (revelar && !reduzido()) {
        // a entrada: o pontilhado que se fecha (os pixels ainda não revelados ficam na cor do papel)
        const p = Math.min(1, (performance.now() - relogio0) / 420);
        if (p < 1) { const nivel = Math.floor(p * 16); for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!Sprites.pontilha(x, y, nivel)) px(x, y, 1, 1, "#120e0b"); }
      }
    }
    if (caixa._timer) clearInterval(caixa._timer);
    cena();
    if (reduzido()) return;
    const ritmo = (ms) => { clearInterval(timer); timer = caixa._timer = setInterval(() => { if (!document.hidden) cena(); }, ms); };
    if (revelar) { ritmo(40); setTimeout(() => { if (canvas.isConnected) ritmo(100); }, 460); } else ritmo(100);
  }

  // ---------------------------------------------------------------- tamanho e rolagem
  /** A tela ocupa a altura visível da página: título, ouro, abas e Voltar ficam parados; só a lista rola. */
  function ajustar(raiz) {
    const t = raiz.querySelector(".tela.loja"), pg = document.querySelector("#pagina");
    if (!t || !pg || !t.isConnected) return;
    const topo = t.getBoundingClientRect().top - pg.getBoundingClientRect().top + pg.scrollTop;
    let alt = Math.max(280, pg.clientHeight - topo - 10);
    t.style.height = alt + "px";
    const sobra = pg.scrollHeight - pg.clientHeight;  // o que ainda passa (o prompt, margens): sai da altura da tela
    if (sobra > 0 && alt - sobra >= 280) { alt -= sobra; t.style.height = alt + "px"; }
  }

  let repeticao = null;  // o "segurar +/−" em andamento
  function pararRepeticao() { clearTimeout(repeticao); repeticao = null; }
  ["pointerup", "pointercancel", "blur"].forEach((t) => window.addEventListener(t, pararRepeticao));

  function mostrarAba(raiz, id, foco) {
    aba = id;
    raiz.querySelectorAll(".loja-aba").forEach((b) => {
      const sim = b.dataset.aba === id;
      b.setAttribute("aria-selected", sim); b.tabIndex = sim ? 0 : -1;
      if (sim && foco) b.focus();
    });
    raiz.querySelectorAll(".loja-painel").forEach((p) => { p.hidden = p.dataset.painel !== id; });
    esconderDica();
  }

  function ligarLoja(raiz, dados) {
    pararRepeticao();
    const tela = raiz.querySelector(".tela.loja");
    // A aba e a rolagem de cada lista voltam como estavam (a lista se mede depois de entrar na página).
    queueMicrotask(() => {
      ajustar(raiz);
      raiz.querySelectorAll("[data-lista]").forEach((l) => { l.scrollTop = rolagem[l.dataset.lista] || 0; });
      banca(raiz.querySelector(".loja-banca"), visitaNova);
      visitaNova = false;
      if (typeof ResizeObserver !== "undefined") {
        let largura = raiz.querySelector(".loja-banca").clientWidth, altura = raiz.querySelector(".loja-banca").clientHeight;
        const obs = new ResizeObserver(() => {
          if (!tela.isConnected) { obs.disconnect(); return; }
          ajustar(raiz);
          const b = raiz.querySelector(".loja-banca");
          if (Math.abs(b.clientWidth - largura) > 2 || Math.abs(b.clientHeight - altura) > 2) { largura = b.clientWidth; altura = b.clientHeight; banca(b, false); }
        });
        obs.observe(document.querySelector("#pagina"));
      }
    });
    raiz.querySelectorAll("[data-lista]").forEach((l) => l.addEventListener("scroll", () => { rolagem[l.dataset.lista] = l.scrollTop; }, { passive: true }));
    // As abas: clique, e as setas (e Home/End) com o foco nelas, como numa lista de abas.
    const abas = [...raiz.querySelectorAll(".loja-aba")];
    abas.forEach((b, k) => {
      b.addEventListener("click", () => { if (aba !== b.dataset.aba) App.som("escolha"); mostrarAba(raiz, b.dataset.aba); });
      b.addEventListener("keydown", (ev) => {
        const ir = { ArrowRight: k + 1, ArrowLeft: k - 1, Home: 0, End: abas.length - 1 }[ev.key];
        if (ir === undefined) return;
        ev.preventDefault();
        const alvo = abas[(ir + abas.length) % abas.length];
        mostrarAba(raiz, alvo.dataset.aba, true);
      });
    });
    raiz.querySelectorAll("[data-comprar]").forEach((el) => {
      const preco = Number(el.dataset.preco), max = Number(el.dataset.max), id = el.dataset.comprar;
      const num = el.querySelector(".qtd-ctrl b"), total = el.querySelector(".total");
      const mudar = (q) => {
        q = Math.max(1, Math.min(max || 1, q));
        qtdLoja[id] = q; num.textContent = q; total.textContent = preco * q;
      };
      el.querySelectorAll("[data-q]").forEach((b) => {
        const passo = () => mudar(Math.min(qtdLoja[id] || 1, max || 1) + Number(b.dataset.q));
        b.addEventListener("click", (ev) => { ev.stopPropagation(); if (ev.detail === 0) passo(); });  // Enter/espaço no botão
        b.addEventListener("keydown", (ev) => { if (ev.key === "Enter") ev.stopPropagation(); });
        b.addEventListener("pointerdown", (ev) => {
          ev.stopPropagation(); pararRepeticao(); passo(); App.som("escolha");
          // Segurar acelera. A repetição para ao soltar em qualquer lugar, ao sair da janela, ao chegar no
          // limite e se o botão sumir (a tela se redesenhou): nunca fica rodando sozinha.
          repeticao = setTimeout(function repetir() {
            const antes = qtdLoja[id];
            if (!b.isConnected) { pararRepeticao(); return; }
            passo();
            repeticao = qtdLoja[id] === antes ? null : setTimeout(repetir, 70);
          }, 380);
        });
        ["pointerup", "pointerleave", "pointercancel"].forEach((t) => b.addEventListener(t, pararRepeticao));
      });
      // O mouse compra no soltar (ver "apertado"); o clique que sobra é o de quem não usa mouse (leitor de tela).
      el.addEventListener("pointerdown", (ev) => { if (ev.button === 0 && !ev.target.closest(".qtd-ctrl")) apertado = id; });
      el.addEventListener("click", (ev) => { if (ev.detail === 0 && !ev.target.closest(".qtd-ctrl")) pedirCompra(el, ev.shiftKey); });
      el.addEventListener("keydown", (ev) => {
        if (ev.target !== el || !Gesto.teclaVale(ev)) return;
        if (ev.key === "Enter") pedirCompra(el, ev.shiftKey);
        else if (ev.key === "+" || ev.key === "=" || ev.key === "-") { ev.preventDefault(); if (num) mudar((qtdLoja[id] || 1) + (ev.key === "-" ? -1 : 1)); }
      });
    });
    raiz.querySelectorAll("[data-comprar-item]").forEach((el) => el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (el.classList.contains("caro")) { const it = dados && dados.equipamentos[Number(el.dataset.comprarItem)]; App.recusar(el, it && it.motivo); return; }
      App.acao({ comprar_item: Number(el.dataset.comprarItem) }, "moeda");
    }));
    // Vender: clique vende na hora (as moedas voam até o ouro do topo); o botão direito equipa; arrastar até a banca
    // também vende.
    let vendendo = null;
    const balcao = raiz.querySelector(".loja-banca");
    raiz.querySelectorAll("[data-peca]").forEach((el) => {
      const i = Number(el.dataset.mochilaLoja), n = Number(el.dataset.peca);
      const it = dados && dados.mochila[i];
      const vender = () => { if (it) venderPeca(el, n); };
      el.addEventListener("click", (ev) => { ev.stopPropagation(); vender(); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" && Gesto.teclaVale(ev)) vender(); });
      el.addEventListener("contextmenu", (ev) => {
        ev.preventDefault(); fecharMenuItem(); esconderDica();
        if (!it || vendida(n)) return;
        if (!it.usavel) { App.som("falha"); App.avisar("Não é para a sua classe.", "equipar"); return; }
        equipando = n;  // ao voltar, o espaço desta peça é o que esvazia (a que sai do corpo vai para um vazio)
        equiparDaMochila(el, it, i);
      });
      el.addEventListener("dragstart", (ev) => { esconderDica(); fecharMenuItem(); vendendo = el; ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    raiz.querySelectorAll("[data-recomprar]").forEach((el) => {
      const recomprar = () => {
        esconderDica();
        const it = dados && dados.recompra[Number(el.dataset.recomprar)];
        if (el.classList.contains("caro")) { App.recusar(el, it && it.motivo); return; }
        App.acao({ recomprar: Number(el.dataset.recomprar) }, "moeda");
      };
      el.addEventListener("click", (ev) => { ev.stopPropagation(); recomprar(); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" && Gesto.teclaVale(ev)) recomprar(); });
    });
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null) venderPeca(vendendo, Number(vendendo.dataset.peca), false);
      vendendo = null;
    });
  }

  /* Compras de suprimento em sequência. Cada clique é um pedido, guardado pelo id do suprimento (nunca pela posição na
     lista), e os pedidos vão ao motor um de cada vez: o seguinte sai quando o mercado volta a perguntar, já redesenhado
     com o ouro, o estoque e a bolsa de depois da compra anterior. O motor confere preço, estoque, ouro e espaço em cada
     um; se o cartão voltou bloqueado (o ouro ou o estoque acabou no meio), o aviso diz o motivo dele, e os pedidos que
     restavam desse suprimento caem juntos. Sair do mercado (ou qualquer pergunta que não seja ele) descarta a fila. */
  const fila = [];
  let apertado = null;  // o suprimento em que o botão do mouse desceu (o id: a lista se redesenha entre o descer e o soltar)
  function descartarCompras() { fila.length = 0; apertado = null; vendas.length = 0; apertoVenda = null; }
  /* Vendas em sequência, do mesmo jeito: cada clique numa peça é a venda daquela peça, guardada pela ficha dela (o
     espaço da grade parada, ver arranjo), e não pela posição na mochila, que muda a cada venda. A primeira vai na hora;
     as outras saem uma a uma, quando o mercado volta a perguntar, cada uma com a posição de verdade daquele momento.
     A peça pedida some da grade na hora (o espaço fica vazio e não aceita outro clique): o clique duplo vende uma, e
     clicar sem parar em peças diferentes vende cada uma. Uma ficha que já não está na grade (a peça saiu por outro
     caminho) cai sem atingir outra peça. */
  const vendas = [];
  let emVoo = null;  // a ficha da venda que foi ao motor e ainda não voltou
  let equipando = null;  // a ficha da peça que o botão direito mandou vestir
  let apertoVenda = null;  // { el, n }: a peça em que o botão desceu (ver o pointerup)
  const vendida = (n) => n === emVoo || vendas.includes(n);
  function venderPeca(el, n, moedas = true) {
    const e = espacoDa(n);
    if (!e || vendida(n)) return;
    fecharMenuItem(); esconderDica();
    if (moedas) moedasPara(el, document.querySelector('.recurso[data-rec="ouro"]'));
    if (!vendas.length && App.acao({ vender: e.i })) emVoo = n;
    else vendas.push(n);
    if (el.isConnected) el.outerHTML = VAZIA;  // o espaço fica vazio já: o item vendido não fica clicável
  }
  function proximaVenda(opcoes) {
    while (vendas.length) {
      const n = vendas.shift(), e = espacoDa(n);
      const i = e ? opcoes.findIndex((o) => o.meta && o.meta.vender === e.i) : -1;
      if (i >= 0) { emVoo = n; return i; }
    }
    return null;
  }
  function pedirCompra(el, shift) {
    const id = el.dataset.comprar, max = Number(el.dataset.max);
    if (!fila.length && el.classList.contains("caro")) {
      const c = App.ultimaLoja && App.ultimaLoja.consumiveis.find((x) => x.id === id);
      App.recusar(el, c && c.motivo);
      return;
    }
    const qtd = shift ? Math.min(5, max) : Math.min(qtdLoja[id] || 1, max);
    qtdLoja[id] = 1;
    if (fila.length || !App.acao({ comprar: id }, "moeda", { qtd })) fila.push({ id, qtd });
  }
  /** Chamada a cada menu novo (escolhas.js): a resposta da próxima compra da fila ({ i, qtd }) ou da próxima venda
   *  (o índice da opção), ou null. */
  function proximaCompra(opcoes) {
    if (!fila.length && vendas.length) return proximaVenda(opcoes);
    while (fila.length) {
      const p = fila[0];
      const i = opcoes.findIndex((o) => o.meta && o.meta.comprar === p.id);
      if (i < 0) { descartarCompras(); return null; }
      const c = App.ultimaLoja && App.ultimaLoja.consumiveis.find((x) => x.id === p.id);
      if (c && c.motivo) {
        for (let k = fila.length - 1; k >= 0; k--) if (fila[k].id === p.id) fila.splice(k, 1);
        App.recusar(document.querySelector(`.tela.loja [data-comprar="${CSS.escape(p.id)}"]`), c.motivo);
        continue;
      }
      fila.shift();
      return { i, qtd: p.qtd };
    }
    return null;
  }
  // O soltar do botão compra se cair no mesmo suprimento em que ele desceu, ainda que o cartão tenha sido redesenhado
  // no meio (a compra anterior voltou): o clique do navegador se perderia, e a proteção de clique entre telas (Gesto,
  // nucleo.js) não vale aqui, porque o pedido vai pelo id e nunca acerta outro item.
  // A peça é a mesma, mas a grade foi redesenhada entre o descer e o subir do botão (a venda anterior voltou): o clique
  // do navegador não sai (são dois elementos). Com a grade parada, o espaço é o mesmo e a ficha também: se o botão
  // subir na mesma peça em que desceu, a venda vale aqui.
  document.addEventListener("pointerdown", (ev) => {
    const el = ev.button === 0 && ev.target.closest && ev.target.closest(".tela.loja [data-peca]");
    apertoVenda = el ? { el, n: Number(el.dataset.peca) } : null;
  }, true);
  document.addEventListener("pointerup", (ev) => {
    const v = apertoVenda;
    apertoVenda = null;
    if (!v || v.el.isConnected || ev.button !== 0 || !ev.target.closest) return;
    const el = ev.target.closest(".tela.loja [data-peca]");
    if (el && Number(el.dataset.peca) === v.n) venderPeca(el, v.n);
  }, true);
  document.addEventListener("pointerup", (ev) => {
    const id = apertado;
    apertado = null;
    if (!id || ev.button !== 0 || !ev.target.closest) return;
    const el = ev.target.closest(".tela.loja [data-comprar]");
    if (el && el.dataset.comprar === id && !ev.target.closest(".qtd-ctrl")) pedirCompra(el, ev.shiftKey);
  }, true);

  // Quem pede para sair (Esc, a seta de voltar) já não quer o que esperava a vez: a fila cai ali, mesmo que a tela ainda
  // esteja recebendo a compra anterior (aí o Esc só adianta a animação, e o próximo sai do mercado).
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") descartarCompras(); }, true);
  document.addEventListener("click", (ev) => { if (ev.target.closest && ev.target.closest("#barra-tela .voltar-seta")) descartarCompras(); }, true);

  Object.assign(Telas, { proximaCompra, descartarCompras });

  Telas.registrar("loja", loja, {
    ligar: (raiz, d) => { App.ultimaLoja = d; ligarLoja(raiz, d); },
    esquecer: () => {
      descartarCompras();
      arranjo = null; emVoo = equipando = null;
      for (const k in qtdLoja) delete qtdLoja[k];
      for (const k in rolagem) delete rolagem[k];
      aba = "suprimentos"; visitaNova = true;
    },
  });
})();
