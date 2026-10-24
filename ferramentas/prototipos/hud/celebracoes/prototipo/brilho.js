/* PROTÓTIPO da etapa 2 (23/10/2026; nada no jogo): o brilho em pixel das celebrações e da raridade, um motor só para a
   subida de nível, o Sigilo, a especialização, o achado por raridade e as fagulhas das vitórias. Desenha num canvas de
   baixa resolução (um texel = 3 px), ampliado sem suavizar, a 15 quadros por segundo, como o feixe do saque
   (sensacao.js: cerimoniaSaque) e a paisagem: uma coluna de luz que sobe do centro, um anel que se abre em degraus e
   fagulhas de um texel subindo. Dura menos de 1 s e para num quadro estático discreto (o brilho que fica enquanto a
   janela está aberta); nada em laço. O canvas fica atrás do conteúdo da janela: o texto, os itens e os botões nunca
   ficam por baixo do efeito. Com o movimento reduzido, só o quadro estático. */
"use strict";

const Brilho = (() => {
  // as rampas, do claro ao escuro: o miolo, o claro, a cor, a sombra e a borda pontilhada
  const PALETAS = {
    ouro: ["#fff6c8", "#f6d86a", "#e0b83a", "#b08418", "#6b4a0e"],
    magico: ["#e8f2ff", "#a8ccff", "#6a9cf0", "#3a5ab0", "#1e2c60"],
    raro: ["#fff6c8", "#f6d86a", "#e0b83a", "#b08418", "#6b4a0e"],
    lendario: ["#fff3c0", "#ffb35c", "#e0782f", "#a8441c", "#5a2010"],
    arcano: ["#f0e8ff", "#c8b0ff", "#9a7ae0", "#5a3a8a", "#2a1a48"],
    sigilo: ["#fff3a0", "#f2c94c", "#ff6a3a", "#b02a18", "#4a0a06"],
  };
  // a intensidade: a largura da coluna (0 = sem coluna), o raio do anel em texels, as fagulhas por quadro e o brilho
  // que fica (de 16)
  const NIVEIS = [
    { coluna: 0, raio: 9, fagulhas: 1, fica: 2 },   // 0: um brilho leve (o mágico)
    { coluna: 1, raio: 14, fagulhas: 1, fica: 2 },  // 1: o raro, a vitória
    { coluna: 2, raio: 20, fagulhas: 2, fica: 3 },  // 2: a subida de nível, a especialização
    { coluna: 3, raio: 26, fagulhas: 3, fica: 3 },  // 3: o lendário, o Sigilo
  ];
  const DURACAO = 900, QUADRO = 66;
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const { pontilha } = Sprites;
  const rgba = (h) => { const v = parseInt(h.slice(1), 16); return (255 << 24) | ((v & 255) << 16) | (v & 0xff00) | (v >> 16); };

  /** O brilho dentro de `host` (posicionado), centrado em (fx, fy) (frações do host). Devolve { parar }: parar() pula
   *  para o quadro estático. */
  function explosao(host, { paleta = "ouro", intensidade = 2, fx = 0.5, fy = 0.3, coluna = true, centro = null, tamanho = null } = {}) {
    const caixa = host.getBoundingClientRect();
    // tamanho: um canvas menor que o host, centrado no `centro` (a arte do item no cartão do achado)
    let r = caixa;
    if (tamanho && centro) {
      const e = centro.getBoundingClientRect(), cxp = e.left + e.width / 2, cyp = e.top + e.height / 2;
      r = { left: cxp - tamanho[0] / 2, top: cyp - tamanho[1] / 2, width: tamanho[0], height: tamanho[1] };
    }
    const dpr = window.devicePixelRatio || 1, T = 3 * Math.max(1, Math.round(dpr));
    const W = Math.ceil((r.width * dpr) / T), H = Math.ceil((r.height * dpr) / T);
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    c.className = "brilho-px";
    c.style.width = (W * T) / dpr + "px"; c.style.height = (H * T) / dpr + "px";
    // o canvas acompanha o centro (a arte do item muda de lugar quando a comparação entra ao lado)
    const posicionar = () => {
      if (!(tamanho && centro)) { c.style.left = "0px"; c.style.top = "0px"; return; }
      const h = host.getBoundingClientRect(), e = centro.getBoundingClientRect();
      c.style.left = Math.round(e.left + e.width / 2 - tamanho[0] / 2 - h.left - host.clientLeft) + "px";
      c.style.top = Math.round(e.top + e.height / 2 - tamanho[1] / 2 - h.top - host.clientTop) + "px";
    };
    posicionar();
    host.prepend(c);
    const ctx = c.getContext("2d"), img = ctx.createImageData(W, H), buf = new Uint32Array(img.data.buffer);
    const [miolo, claro, cor, sombra, borda] = (PALETAS[paleta] || PALETAS.ouro).map(rgba);
    // sem coluna (as festas: a coluna passaria por trás do texto do alto), o brilho que fica é mínimo
    const n = { ...NIVEIS[Math.max(0, Math.min(3, intensidade))], ...(coluna ? {} : { coluna: 0, fica: 0 }) };
    // centro: um elemento (o número do nível) em vez das frações
    if (centro) { const e = centro.getBoundingClientRect(); fx = (e.left + e.width / 2 - r.left) / r.width; fy = (e.top + e.height / 2 - r.top) / r.height; }
    const cx = Math.round(W * fx), cy = Math.round(H * fy);
    const fag = [];
    const por = (x, y, v) => { if (x >= 0 && y >= 0 && x < W && y < H) buf[y * W + x] = v; };
    function desenhar(t, q, final) {
      posicionar();
      buf.fill(0);
      const k = final ? 1 : Math.min(1, t / DURACAO);
      const some = final ? 0 : Math.max(0, 1 - Math.max(0, t - 450) / 450);  // o que se mexe apaga na segunda metade
      // o que fica: um disco pontilhado na cor, fraco, e o anel inteiro mais fraco ainda
      const rf = n.raio + 2;
      for (let dy = -rf; dy <= rf; dy++) for (let dx = -rf * 2; dx <= rf * 2; dx++) {
        const e = (dx * dx) / (4 * rf * rf) + (dy * dy) / (rf * rf);
        if (e > 1) continue;
        const x = cx + dx, y = cy + dy, dens = Math.round(n.fica * (1 - e) * 1.6 * Math.min(1, k * 2));
        if (pontilha(x, y, dens)) por(x, y, e < 0.3 ? cor : sombra);
      }
      // a coluna: sobe do centro até o alto, em bandas (o miolo, o claro, a cor, a borda pontilhada)
      if (n.coluna) {
        const sobe = Math.min(1, t / 260), topo = final ? 0 : Math.round(cy * (1 - sobe));
        const alpha = final ? 3 : Math.round(16 * Math.max(0.25, some));
        for (let y = topo; y < cy; y++) {
          const larg = n.coluna + (((y >> 2) - q) % 5 === 0 ? 1 : 0);
          for (let d = -(larg + 5); d <= larg + 5; d++) {
            const x = cx + d, a = Math.abs(d);
            if (!pontilha(x, y, final ? (a <= larg ? 3 : 1) : alpha)) continue;
            por(x, y, a <= larg ? miolo : a <= larg + 2 ? claro : a <= larg + 3 ? cor : borda);
          }
        }
      }
      // o anel: abre em degraus e fica; o miolo dele clareia no começo
      const rx = final ? n.raio : Math.min(n.raio, 2 + Math.floor(t / 28)), ry = Math.max(2, Math.round(rx * 0.55));
      for (let dy = -ry; dy <= ry; dy++) for (let dx = -rx; dx <= rx; dx++) {
        const e = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry);
        if (e > 1) continue;
        const borda1 = (dx * dx) / ((rx - 1) * (rx - 1)) + (dy * dy) / Math.max(1, (ry - 1) * (ry - 1)) > 1;
        const x = cx + dx, y = cy + dy;
        if (borda1) { if (pontilha(x, y, final ? (n.fica ? 6 : 3) : 14)) por(x, y, claro); }
        else if (!final && pontilha(x, y, Math.round(10 * (1 - e) * some))) por(x, y, e < 0.2 ? miolo : cor);
      }
      // as fagulhas: um texel (às vezes uma cruzinha) subindo e apagando de cor em cor
      if (!final) {
        if (t < DURACAO - 250) for (let i = 0; i < n.fagulhas; i++) {
          const ang = Math.random() * Math.PI;
          fag.push({ x: cx + Math.round(Math.cos(ang) * rx), y: cy + Math.round(Math.sin(ang) * ry * 0.6), v: 1 + Math.floor(Math.random() * 2),
            vida: 8 + Math.floor(Math.random() * 7), cruz: Math.random() < 0.2 });
        }
        for (const f of fag) {
          if (f.vida-- <= 0) continue;
          f.y -= f.v;
          if (q % 3 === 0) f.x += Math.random() < 0.5 ? -1 : 1;
          const v = f.vida > 8 ? miolo : f.vida > 4 ? claro : cor;
          por(f.x, f.y, v);
          if (f.cruz && f.vida > 5) { por(f.x - 1, f.y, cor); por(f.x + 1, f.y, cor); por(f.x, f.y - 1, cor); por(f.x, f.y + 1, cor); }
        }
      }
      ctx.putImageData(img, 0, 0);
    }
    let parado = false;
    const parar = () => { if (parado) return; parado = true; desenhar(DURACAO, 0, true); setTimeout(posicionar, 700); };
    if (reduzido()) { parar(); return { parar }; }
    const inicio = performance.now();
    let ultimo = -1;
    const passo = (agora) => {
      if (parado || !c.isConnected) return;
      const t = agora - inicio, q = Math.floor(t / QUADRO);
      if (q !== ultimo) { ultimo = q; desenhar(t, q, false); }
      if (t < DURACAO) requestAnimationFrame(passo); else parar();
    };
    requestAnimationFrame(passo);
    return { parar };
  }

  /** As fagulhas soltas pela tela (a vitória, os contratos pagos): texels que voam do meio para fora e apagam em
   *  degraus, num canvas da tela inteira por cima do jogo, sem pegar clique. Breve (menos de 1 s). */
  function estouro(paleta = "ouro", quantas = 30) {
    if (reduzido()) return;
    const dpr = window.devicePixelRatio || 1, T = 3 * Math.max(1, Math.round(dpr));
    const W = Math.ceil((innerWidth * dpr) / T), H = Math.ceil((innerHeight * dpr) / T);
    const c = document.createElement("canvas");
    c.width = W; c.height = H; c.className = "estouro-px";
    c.style.width = (W * T) / dpr + "px"; c.style.height = (H * T) / dpr + "px";
    document.body.appendChild(c);
    const ctx = c.getContext("2d"), img = ctx.createImageData(W, H), buf = new Uint32Array(img.data.buffer);
    const cores = (PALETAS[paleta] || PALETAS.ouro).slice(0, 4).map(rgba);
    const cx = W / 2, cy = H * 0.42;
    const ps = Array.from({ length: quantas }, () => {
      const a = Math.random() * Math.PI * 2, v = 1.2 + Math.random() * 2.2;
      return { x: cx, y: cy, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.7 - 0.6, vida: 9 + Math.floor(Math.random() * 6) };
    });
    const inicio = performance.now();
    let ultimo = -1;
    const passo = (agora) => {
      const t = agora - inicio, q = Math.floor(t / QUADRO);
      if (q !== ultimo) {
        ultimo = q; buf.fill(0);
        for (const p of ps) {
          if (p.vida-- <= 0) continue;
          p.x += p.vx; p.y += p.vy; p.vy += 0.12;
          const x = Math.round(p.x), y = Math.round(p.y);
          if (x >= 0 && y >= 0 && x < W && y < H) buf[y * W + x] = cores[Math.min(3, Math.floor((14 - p.vida) / 4))];
        }
        ctx.putImageData(img, 0, 0);
      }
      if (t < 950) requestAnimationFrame(passo); else c.remove();
    };
    requestAnimationFrame(passo);
  }

  // o estilo da proposta (na integração, iria para o CSS das celebrações)
  const css = document.createElement("style");
  css.textContent = `
    /* o canvas fica fora do fluxo, atrás de tudo (o cartão do achado põe position: relative em todos os filhos) */
    :is(.achado-cartao, .festa) > .brilho-px { position: absolute !important; z-index: 0 !important; pointer-events: none; image-rendering: pixelated; }
    .estouro-px { position: fixed; left: 0; top: 0; z-index: 41; pointer-events: none; image-rendering: pixelated; }
    /* a festa: o brilho atrás, o conteúdo por cima; sem os raios girando e o anel desfocado de antes */
    .festa.festa-px { overflow: hidden; isolation: isolate; animation: festa-px-entra 0.2s steps(3) both; }
    @keyframes festa-px-entra { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
    .festa.festa-px > :not(.brilho-px) { position: relative; z-index: 1; }
    .festa.festa-px .raios, .festa.festa-px .anel { display: none; }
    .festa-px .nivel-bloco { display: flex; align-items: baseline; justify-content: center; gap: 16px; margin: 2px 0 0; }
    .festa-px .nivel-palavra { font-family: var(--titulo); font-size: calc(var(--px) * 64); color: #e8dcc0; text-shadow: 3px 3px 0 #000; }
    .festa-px .nivel-numero { font-family: var(--num); font-size: 128px; line-height: 0.85; color: var(--ouro); text-shadow: 5px 5px 0 #000;
      animation: numero-carimbo 0.24s steps(3) 0.06s both; }
    @keyframes numero-carimbo { from { transform: scale(1.5); opacity: 0; } to { transform: none; opacity: 1; } }
    .festa-px .grande { animation: none; text-shadow: 4px 4px 0 #000; }
    /* os ganhos: um bloco por ganho, o ícone da HUD, o valor grande e o nome embaixo; chegam juntos, em cascata curta */
    .festa-px .ganhos-px { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 14px 0 4px; }
    .festa-px .ganho-px { display: grid; grid-template-columns: auto auto; grid-template-rows: auto auto; column-gap: 6px; align-items: center;
      min-width: 92px; padding: 5px 10px 5px 8px; background: #120e0b; border: 3px solid #3d6a2a; box-shadow: 3px 3px 0 #000;
      animation: ganho-px 0.18s steps(2) calc(0.1s + var(--i) * 0.04s) both; }
    .festa-px .ganho-px > img { grid-row: span 2; width: 24px; height: 24px; image-rendering: pixelated; }
    .festa-px .ganho-px b { font-family: var(--num); font-size: 26px; line-height: 1; color: var(--bom); font-weight: normal; text-align: left; }
    .festa-px .ganho-px span { font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--tinta-2); text-align: left; }
    @keyframes ganho-px { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
    .festa-px .talento-px { display: inline-flex; align-items: center; gap: 10px; margin-top: 8px; padding: 5px 14px 5px 8px; background: #1a1408;
      border: 3px solid #8a6a14; box-shadow: 3px 3px 0 #000; color: var(--ouro); font-family: var(--num); font-size: 22px;
      animation: ganho-px 0.18s steps(2) calc(0.1s + var(--i) * 0.04s) both; }
    .festa-px .talento-px img { width: 32px; height: 32px; image-rendering: pixelated; }
    .festa-px .talento-px small { font-family: var(--corpo, inherit); font-size: 13px; color: var(--tinta-2); }
    .festa-px .habilidade-nova { animation: ganho-px 0.18s steps(2) calc(0.16s + var(--i) * 0.04s) both; opacity: 1; }
    .festa-px .continuar { margin-top: 14px; }
    /* o 2º clique de um clique duplo selecionava o texto do botão da festa seguinte (no jogo também): fora */
    #celebracao .festa, #celebracao .continuar { user-select: none; }
    /* o achado: o selo da raridade (o nome por extenso, na cor dela) e a aura em pixel no lugar dos raios girando */
    .achado-cartao .achado-raios.px { display: none; }
    .achado-cartao.novo .selo-raridade { display: inline-block; margin: 2px auto 4px; padding: 1px 10px; font-family: var(--num); font-size: 15px;
      letter-spacing: 0.12em; text-transform: uppercase; border: 2px solid; box-shadow: 2px 2px 0 #000; background: #0d0b0a; }
    .selo-raridade.rar-comum { color: #c0b8a8; border-color: #6a6258; }
    .selo-raridade.rar-magico { color: #c8dcff; border-color: #3a5ab0; }
    .selo-raridade.rar-raro { color: #fff0b8; border-color: #b08418; }
    .selo-raridade.rar-lendario { color: #ffd2a0; border-color: #e0782f; background: #1a0e06; }
    @media (prefers-reduced-motion: reduce) {
      .festa.festa-px, .festa-px .nivel-numero, .festa-px .ganho-px, .festa-px .talento-px, .festa-px .habilidade-nova { animation: none; }
    }
  `;
  document.head.appendChild(css);
  return { explosao, estouro, reduzido };
})();
