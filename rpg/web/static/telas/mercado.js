/* Mercado: a banca do mercador (à esquerda, ou numa faixa em cima quando falta largura) e, ao lado, o ouro, três abas
   (Suprimentos, Equipamentos, Vender) e a lista da aba, a única parte que rola. Trocar de aba é só da tela: não fala
   com o motor, não passa tempo nem mexe no estoque. A aba, a rolagem de cada lista e a quantidade escolhida em cada
   suprimento sobrevivem ao redesenho depois de cada compra ou venda (não à saída do mercado). */
"use strict";

(() => {
  const { h, S, dica, dicaItem, esconderDica, fecharMenuItem, iconeItem, moedasPara } = Telas;

  const ABAS = [["suprimentos", "Suprimentos"], ["equipamentos", "Equipamentos"], ["vender", "Vender"]];
  const qtdLoja = {};  // quantidade escolhida em cada suprimento
  let aba = "suprimentos";
  const rolagem = {};  // onde cada lista estava
  let visitaNova = true;  // a banca se revela só ao entrar (não a cada compra nem troca de aba)

  function maxCompra(c, ouro) { return Math.max(0, Math.min(99, c.limite ?? 99, Math.floor(ouro / c.preco))); }
  const motivoHtml = (m) => `<span class="merc-motivo">${S("cadeado", 1)}${h(m)}</span>`;

  function suprimento(c, ouro) {
    const max = maxCompra(c, ouro);
    const q = Math.max(1, Math.min(qtdLoja[c.id] || 1, max || 1));
    const tem = c.teto ? `${c.tem} de ${c.teto}` : c.tem;
    return `<div role="button" tabindex="0" class="mercadoria suprimento${c.motivo ? " caro" : ""}" data-comprar="${h(c.id)}" data-preco="${c.preco}" data-max="${max}"
        ${dica(`<b>${h(c.nome)}</b><div>${Realce.texto(c.desc)}</div><div class="rodape">${c.motivo ? h(c.motivo) : "Clique para comprar a quantidade escolhida. Shift+clique compra 5."}</div>`)}>
      <span class="slot-px">${S(c.icone || "pocao", 2)}</span>
      <span class="merc-nome">${h(c.nome)}</span>
      <span class="merc-contas"><span>Você tem <b>${tem}</b></span><span class="merc-estoque${c.estoque ? "" : " esgotado"}">À venda <b>${c.estoque}</b></span></span>
      ${c.motivo ? motivoHtml(c.motivo) : `<span class="merc-acao"><span class="qtd-ctrl"><button type="button" data-q="-1" aria-label="menos ${h(c.nome)}">−</button><b aria-label="quantidade">${q}</b><button type="button" data-q="1" aria-label="mais ${h(c.nome)}">+</button></span>
        <span class="merc-total" title="Preço total">${S("moeda", 1)}<span class="total">${c.preco * q}</span></span></span>`}</div>`;
  }

  function equipamento(it, i) {
    return `<button type="button" class="mercadoria equip${it.motivo ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, it.motivo ? h(it.motivo) : "Clique para comprar. Se o espaço do corpo estiver vazio, você já sai vestindo.")}>
      <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
      <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span>
      ${it.motivo ? motivoHtml(it.motivo) : `<span class="preco">${S("moeda", 1)}${it.preco}</span>`}</button>`;
  }

  // Vender: cada item da mochila com o que o mercador paga, à vista (sem depender da dica). Clique vende na hora (o que
  // você vendeu fica no balcão para recomprar pelo mesmo preço até sair do mercado); o botão direito equipa.
  function paraVender(it, i) {
    const venda = `<div class="preco-venda">${S("moeda", 1)} O mercador paga <b>${it.preco}</b></div>` +
      `Clique: vender${it.usavel ? " · botão direito: equipar" : " · não é para a sua classe"}`;
    return `<div role="button" tabindex="0" class="mercadoria venda${it.usavel ? "" : " outra-classe"}" draggable="true" data-mochila-loja="${i}" ${dicaItem(it, venda)}>
      <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
      <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}${it.usavel ? "" : '<small class="merc-classe">Não é para a sua classe</small>'}</span>
      <span class="preco ganho">Vende por ${S("moeda", 1)}${it.preco}</span></div>`;
  }

  function recompra(d) {
    const itens = (d.recompra || []).map((it, i) => `<div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.motivo ? " caro" : ""}" data-recomprar="${i}"
        ${dicaItem(it, `<div class="preco-venda">${S("moeda", 1)} Recomprar por <b>${it.preco}</b></div>${it.motivo ? h(it.motivo) : "Clique para desfazer a venda."}`)}>${S(iconeItem(it), 2)}<span class="preco-canto">${it.preco}</span></div>`).join("");
    return `<div class="loja-recompra"><span class="lr-rotulo">Vendidos agora</span>${itens || '<span class="lr-vazio">Recompre aqui pelo mesmo preço o que vender, até sair do mercado.</span>'}</div>`;
  }

  function loja(d) {
    const listas = {
      suprimentos: d.consumiveis.map((c) => suprimento(c, d.ouro)).join(""),
      equipamentos: d.equipamentos.map(equipamento).join("") || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>',
      vender: d.mochila.map(paraVender).join("") || '<span class="vazio">A mochila está vazia: nada para vender.</span>',
    };
    const conta = { equipamentos: d.equipamentos.length, vender: d.mochila.length };
    const mochila = `<span class="loja-mochila">${S("saco", 1)} Mochila <b>${d.ocupado}/${d.limite}</b></span>`;
    const sub = {
      suprimentos: "",
      equipamentos: mochila,
      vender: `${mochila}${recompra(d)}`,
    };
    const abas = ABAS.map(([id, nome]) => `<button type="button" role="tab" id="aba-${id}" class="loja-aba" data-aba="${id}" aria-controls="lista-${id}"
        aria-selected="${id === aba}" tabindex="${id === aba ? 0 : -1}">${nome}${conta[id] !== undefined ? ` <small>${conta[id]}</small>` : ""}</button>`).join("");
    const paineis = ABAS.map(([id]) => `<div class="loja-painel" role="tabpanel" id="lista-${id}" aria-labelledby="aba-${id}" data-painel="${id}"${id === aba ? "" : " hidden"}>
        ${sub[id] ? `<div class="loja-sub">${sub[id]}</div>` : ""}<div class="loja-lista vitrine" data-lista="${id}">${listas[id]}</div></div>`).join("");
    return `<div class="tela loja${visitaNova ? " chegando" : ""}">
      <div class="loja-banca"><canvas class="banca-cena"></canvas></div>
      <div class="loja-lado">
        <div class="loja-topo"><div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
          <span class="ouro-loja" aria-label="seu ouro">${S("moedas", 2)}${d.ouro}</span></div>
        <div class="loja-abas" role="tablist" aria-label="Mercado">${abas}</div>
        ${paineis}
      </div></div>`;
  }

  // ---------------------------------------------------------------- a banca
  /** Dentro do mercado, de frente para o balcão: a parede de tábuas com as prateleiras (potes, sacos, frascos), as
   *  ervas penduradas, a lamparina que treme (mais forte à noite) e, atrás do balcão, o mercador, que respira, pisca e
   *  de tempos em tempos pega um frasco da bancada, olha contra a luz e devolve. É outro lugar que não o mercado da
   *  vila (aquele é o prédio; isto é o lado de dentro). Pixel art no estilo das paisagens, em escala inteira: o retrato
   *  (ao lado dos produtos) em 58×78, a faixa (em cima, quando falta largura) com a mesma cena, mais larga. Ao entrar,
   *  revela-se num pontilhado que se fecha; com movimento reduzido, fica parada. */
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const COR = {
    parede: "#1e1712", fresta: "#15100c", prateleira: "#4a3624", prateleiraLuz: "#6a5034", prateleiraSombra: "#24190f",
    balcao: "#5a4028", balcaoLuz: "#7a5a38", balcaoBorda: "#2a1c10", frente: "#3a2818", frenteLinha: "#2a1c12",
    pele: "#b07a56", peleLuz: "#c8946a", peleSombra: "#8a5a3c", cabelo: "#2a1c14", barba: "#4a3020", olho: "#120c08",
    tunica: "#3a4a5a", tunicaSombra: "#2a3644", avental: "#8a7454", aventalSombra: "#6a5840", saco: "#8a7454", sacoSombra: "#5a4a34",
  };
  function banca(caixa, revelar) {
    const canvas = caixa.querySelector(".banca-cena"), c = canvas.getContext("2d");
    const cw = Math.max(1, caixa.clientWidth), ch = Math.max(1, caixa.clientHeight);
    const faixa = cw > ch * 1.6;
    const W = faixa ? Math.max(120, Math.round(cw / 2)) : 58, H = faixa ? 40 : 78;
    canvas.width = W; canvas.height = H;
    const px = (x, y, w, hh, cor) => { c.fillStyle = cor; c.fillRect(Math.round(x), Math.round(y), w, hh); };
    const noite = ((App.estado && App.estado.mundo && App.estado.mundo.periodo_n) || 0) === 3;
    const topo = faixa ? 30 : 58;               // o tampo do balcão
    const mx = Math.round(W / 2);               // o meio do mercador
    const lampada = faixa ? [mx - 46, 1] : [9, 1];
    const inicio = performance.now();
    let quadro = 0, timer = null;

    function pote(x, y, cor, alto = 5) {
      px(x, y + 1, 4, alto - 1, cor); px(x, y + 1, 1, alto - 1, "rgba(255,255,255,0.18)"); px(x + 3, y + 1, 1, alto - 1, "rgba(0,0,0,0.35)");
      px(x + 1, y, 2, 1, "#6a5034"); px(x, y + alto, 4, 1, "rgba(0,0,0,0.4)");
    }
    function frasco(x, y, cor) { px(x + 1, y, 1, 2, "#9a9aa0"); px(x, y + 2, 3, 3, cor); px(x, y + 2, 1, 1, "rgba(255,255,255,0.35)"); }
    function saco(x, y) { px(x + 1, y, 3, 1, COR.sacoSombra); px(x, y + 1, 5, 4, COR.saco); px(x + 4, y + 1, 1, 4, COR.sacoSombra); px(x + 1, y + 1, 1, 1, "#a8946c"); }
    function prateleira(y, x0, x1) { px(x0, y, x1 - x0, 1, COR.prateleiraLuz); px(x0, y + 1, x1 - x0, 1, COR.prateleira); px(x0, y + 2, x1 - x0, 1, COR.prateleiraSombra); }
    function parede() {
      px(0, 0, W, topo, COR.parede);
      for (let x = 3; x < W; x += 7) px(x, 0, 1, topo, COR.fresta);
      for (let y = 0; y < topo; y++) for (let x = 0; x < W; x++) if (Sprites.pontilha(x, y, 1)) px(x, y, 1, 1, "#241c16");
      // a viga do teto e as ervas penduradas nela (balançam de leve)
      px(0, 0, W, 2, COR.prateleiraSombra);
      const vento = reduzido() ? 0 : Math.round(Math.sin(quadro / 9) * 0.6);
      (faixa ? [mx + 26, mx + 34, mx + 70, mx - 80] : [40, 46, 52]).forEach((x, k) => {
        for (let y = 2; y < 2 + 6 + (k % 2) * 2; y++) px(x + (y > 5 ? vento : 0), y, 1, 1, k % 2 ? "#4a6a32" : "#5a7a3a");
        px(x - 1 + (vento > 0 ? 1 : 0), 7 + (k % 2) * 2, 3, 1, "#3a5226");
      });
      // as prateleiras, com a mercadoria
      const fileiras = faixa ? [11, 21] : [14, 30];
      fileiras.forEach((y, f) => prateleira(y, faixa ? 0 : 1, faixa ? W : W - 1));
      const cores = ["#7a2a26", "#2a5a7a", "#3a6a3a", "#8a6a2a", "#5a3a6a"];
      const passo = faixa ? 11 : 7;
      fileiras.forEach((y, f) => {
        for (let x = (faixa ? 4 : 3) + f * 3, k = 0; x < W - 5; x += passo, k++) {
          if (Math.abs(x + 2 - mx) < (faixa ? 12 : 10) && f === fileiras.length - 1) continue;  // atrás da cabeça dele, vazio
          if (faixa && (k * 7 + f * 3) % 5 === 4) continue;  // na faixa, larga, a prateleira tem vãos
          const tipo = (k + f * 2) % 4;
          if (tipo === 0) pote(x, y - 6, cores[(k + f) % cores.length]);
          else if (tipo === 1) saco(x, y - 5);
          else if (tipo === 2) frasco(x + 1, y - 5, cores[(k * 2 + f) % cores.length]);
          else { pote(x, y - 4, "#6a5a4a", 3); }
        }
      });
    }
    function lamparina() {
      const [lx, ly] = lampada, forca = noite ? 1 : 0.6, raio = (faixa ? 11 : 12) + (noite ? 4 : 0) + (reduzido() ? 0 : (quadro % 3) - 1);
      for (let y = -raio; y <= raio; y++) for (let x = -raio; x <= raio; x++) {
        const d2 = (x * x + y * y) / (raio * raio);
        if (d2 < 1 && Sprites.pontilha(lx + x, ly + 6 + y, Math.round((1 - d2) * 8 * forca))) px(lx + x, ly + 6 + y, 1, 1, "rgba(255,190,110,0.22)");
      }
      px(lx, ly, 1, 3, "#2a2016"); px(lx - 2, ly + 3, 5, 6, "#3a2a18"); px(lx - 1, ly + 4, 3, 4, noite ? "#ffd27a" : "#e8a050");
      px(lx, ly + 5, 1, 2, "#fff0b0");
    }
    // O mercador: a cabeça, o tronco com o avental e os braços; o direito vai até o frasco da bancada, ergue e devolve.
    function mercador(t) {
      const quieto = reduzido(), respira = quieto ? 0 : Math.floor(t / 1.4) % 2;
      const cabeca = topo - 26 + respira, ombro = topo - 17 + respira;
      // o tronco (o balcão corta da cintura para baixo)
      px(mx - 8, ombro, 17, topo - ombro, COR.tunica); px(mx + 5, ombro, 4, topo - ombro, COR.tunicaSombra);
      px(mx - 5, ombro + 3, 11, topo - ombro - 3, COR.avental); px(mx + 3, ombro + 3, 3, topo - ombro - 3, COR.aventalSombra);
      px(mx - 5, ombro + 3, 1, 1, COR.aventalSombra); px(mx + 5, ombro + 3, 1, 1, COR.aventalSombra);  // as alças
      // a cabeça: o cabelo, o rosto, a barba, os olhos (pisca a cada tanto)
      px(mx - 2, ombro - 1, 5, 1, COR.peleSombra);  // o pescoço
      px(mx - 4, cabeca, 9, 9, COR.pele); px(mx - 4, cabeca + 1, 2, 5, COR.peleLuz); px(mx + 3, cabeca + 2, 2, 6, COR.peleSombra);
      px(mx - 4, cabeca - 1, 9, 2, COR.cabelo); px(mx - 5, cabeca, 1, 4, COR.cabelo); px(mx + 5, cabeca, 1, 4, COR.cabelo);
      px(mx - 4, cabeca + 6, 9, 3, COR.barba); px(mx - 3, cabeca + 9, 7, 1, COR.barba); px(mx - 1, cabeca + 6, 3, 1, COR.peleSombra);
      const pisca = !quieto && t % 4.3 < 0.15;
      if (!pisca) { px(mx - 2, cabeca + 4, 1, 1, COR.olho); px(mx + 2, cabeca + 4, 1, 1, COR.olho); }
      else { px(mx - 2, cabeca + 4, 1, 1, COR.peleSombra); px(mx + 2, cabeca + 4, 1, 1, COR.peleSombra); }
      px(mx - 2, cabeca + 3, 2, 1, COR.cabelo); px(mx + 1, cabeca + 3, 2, 1, COR.cabelo);  // as sobrancelhas
      // o braço esquerdo, apoiado no balcão
      px(mx - 10, ombro + 1, 3, topo - ombro - 2, COR.tunica); px(mx - 11, topo - 2, 4, 2, COR.pele);
      // o braço direito: parado, ou indo até o frasco, erguendo, devolvendo (um ciclo de 8 s)
      const ciclo = quieto ? 0 : t % 8;
      const alvo = [mx + 14, topo - 3];
      let mao = [mx + 9, topo - 2], ergue = 0;
      if (ciclo > 4.6 && ciclo < 7.6) {
        const ida = Math.min(1, (ciclo - 4.6) / 0.6), volta = Math.min(1, Math.max(0, (7.6 - ciclo) / 0.6));
        const f = Math.min(ida, volta);
        mao = [Math.round(mao[0] + (alvo[0] - mao[0]) * f), mao[1]];
        if (ciclo > 5.3 && ciclo < 6.9) ergue = Math.round(Math.min(1, (ciclo - 5.3) / 0.3, (6.9 - ciclo) / 0.3) * (faixa ? 5 : 7));
      }
      const [hx, hy] = [mao[0], mao[1] - ergue];
      for (let k = 0; k <= 6; k++) {  // do ombro até a mão
        const x = Math.round(mx + 8 + (hx - mx - 8) * (k / 6)), y = Math.round(ombro + 1 + (hy - ombro - 1) * (k / 6));
        px(x, y, 3, 2, COR.tunica);
      }
      px(hx, hy, 3, 2, COR.pele);
      // o frasco que ele mexe: na bancada, ou na mão, erguido contra a luz
      const fx = ergue ? hx : alvo[0], fy = ergue ? hy - 5 : topo - 5;
      frasco(fx, fy, "#2a7a5a");
      if (ergue > 3) px(fx + 1, fy + 3, 1, 1, "#9ae8c0");  // a luz da lamparina atravessa o vidro
    }
    function bancada() {
      px(0, topo, W, 2, COR.balcaoLuz); px(0, topo + 2, W, 1, COR.balcao); px(0, topo + 3, W, 1, COR.balcaoBorda);
      px(0, topo + 4, W, H - topo - 4, COR.frente);
      for (let x = 4; x < W; x += faixa ? 11 : 9) px(x, topo + 4, 1, H - topo - 4, COR.frenteLinha);
      // em cima da bancada: a balança, a pilha de moedas e um saco aberto
      const bx = faixa ? mx - 30 : 3;
      px(bx + 3, topo - 7, 1, 7, "#5a4a3a"); px(bx, topo - 7, 7, 1, "#8a7a5a");
      const pesa = reduzido() ? 0 : Math.round(Math.sin(quadro / 11));
      px(bx - 1, topo - 6 + pesa, 3, 1, "#8a7a5a"); px(bx + 5, topo - 6 - pesa, 3, 1, "#8a7a5a");
      px(bx + 1, topo - 1, 5, 1, "#3a2a1a");
      const mo = faixa ? mx + 24 : W - 9;
      [[0, 0], [1, -1], [0, -2], [1, -3]].forEach(([dx, dy]) => { px(mo + dx, topo - 2 + dy, 4, 1, "#e2bd63"); px(mo + dx + 3, topo - 2 + dy, 1, 1, "#a07a2a"); });
      if (faixa) { saco(mx + 40, topo - 5); saco(mx - 52, topo - 5); }
    }
    function cena() {
      if (!canvas.isConnected) { clearInterval(timer); return; }
      quadro++;
      const t = (performance.now() - inicio) / 1000;
      parede();
      lamparina();
      mercador(t);
      bancada();
      if (revelar && !reduzido()) {
        // a entrada: o pontilhado que se fecha (os pixels ainda não revelados ficam na cor do papel)
        const p = Math.min(1, (performance.now() - inicio) / 420);
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
        let largura = raiz.querySelector(".loja-banca").clientWidth;
        const obs = new ResizeObserver(() => {
          if (!tela.isConnected) { obs.disconnect(); return; }
          ajustar(raiz);
          const b = raiz.querySelector(".loja-banca");
          if (Math.abs(b.clientWidth - largura) > 2) { largura = b.clientWidth; banca(b, false); }
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
      const comprar = (ev) => {
        if (el.classList.contains("caro")) { App.som("falha"); return; }
        const q = ev.shiftKey ? Math.min(5, max) : Math.min(qtdLoja[id] || 1, max);
        qtdLoja[id] = 1;
        App.acao({ comprar: id }, "moeda", { qtd: q });
      };
      el.addEventListener("click", (ev) => { if (!ev.target.closest(".qtd-ctrl")) comprar(ev); });
      el.addEventListener("keydown", (ev) => {
        if (ev.target !== el || !Gesto.teclaVale(ev)) return;
        if (ev.key === "Enter") comprar(ev);
        else if (ev.key === "+" || ev.key === "=" || ev.key === "-") { ev.preventDefault(); if (num) mudar((qtdLoja[id] || 1) + (ev.key === "-" ? -1 : 1)); }
      });
    });
    raiz.querySelectorAll("[data-comprar-item]").forEach((el) => el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (el.classList.contains("caro")) { App.som("falha"); return; }
      App.acao({ comprar_item: Number(el.dataset.comprarItem) }, "moeda");
    }));
    // Vender: clique vende na hora (as moedas voam até o ouro do topo); o botão direito equipa; arrastar até a banca
    // também vende.
    let vendendo = null;
    const balcao = raiz.querySelector(".loja-banca");
    raiz.querySelectorAll("[data-mochila-loja]").forEach((el) => {
      const i = Number(el.dataset.mochilaLoja);
      const it = dados && dados.mochila[i];
      const vender = () => {
        if (!it) return;
        fecharMenuItem(); esconderDica();
        if (App.acao({ vender: i })) moedasPara(el, document.querySelector('.recurso[data-rec="ouro"]'));
      };
      el.addEventListener("click", (ev) => { ev.stopPropagation(); vender(); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" && Gesto.teclaVale(ev)) vender(); });
      el.addEventListener("contextmenu", (ev) => {
        ev.preventDefault(); fecharMenuItem(); esconderDica();
        if (!it) return;
        if (!it.usavel) { App.som("falha"); App.avisar("Não é para a sua classe.", "equipar"); return; }
        App.acao({ equipar: i }, "equipar");
      });
      el.addEventListener("dragstart", (ev) => { esconderDica(); fecharMenuItem(); vendendo = i; ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    raiz.querySelectorAll("[data-recomprar]").forEach((el) => {
      const recomprar = () => {
        esconderDica();
        const it = dados && dados.recompra[Number(el.dataset.recomprar)];
        if (el.classList.contains("caro")) { App.som("falha"); App.avisar((it && it.motivo) || "Ouro insuficiente.", "recomprar"); return; }
        App.acao({ recomprar: Number(el.dataset.recomprar) }, "moeda");
      };
      el.addEventListener("click", (ev) => { ev.stopPropagation(); recomprar(); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" && Gesto.teclaVale(ev)) recomprar(); });
    });
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null) App.acao({ vender: vendendo });
      vendendo = null;
    });
  }

  Telas.registrar("loja", loja, {
    ligar: (raiz, d) => { App.ultimaLoja = d; ligarLoja(raiz, d); },
    esquecer: () => {
      for (const k in qtdLoja) delete qtdLoja[k];
      for (const k in rolagem) delete rolagem[k];
      aba = "suprimentos"; visitaNova = true;
    },
  });
})();
