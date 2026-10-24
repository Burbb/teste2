/* PROTÓTIPO da etapa 2 (23/10/2026; nada no jogo): rpg/web/static/telas/celebracoes.js da 1.200.1 com a proposta da
   subida de nível, do Sigilo, da especialização e das fagulhas (marcado "PROTÓTIPO etapa 2"), precedido do Brilho
   (brilho.js). Servido no lugar do do jogo só nas fotos (../auxiliares/fotografar.mjs, PROTOTIPO=1). */
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

/* Celebrações: as festas por cima do jogo (nível, Sigilo, especialização, espólio, contratos pagos, atributo
   permanente, chegada, amanhecer), os itens que voam até onde moram e a linha que cada festa deixa no histórico. */
"use strict";

(() => {
  const { h, S, cartaz, chegando, fecharAchado, iconeItem, moedasPara, noPalco } = Telas;

  // PROTÓTIPO etapa 2: as fagulhas soltas viram o estouro em pixel do Brilho (texels que voam e apagam em degraus),
  // na paleta da festa e com metade das peças; o resto da função antiga fica sem uso no protótipo
  function particulas(cores, n = 60) {
    const paleta = cores.includes("#b49cff") ? "arcano" : cores.includes("#ff4020") ? "sigilo" : "ouro";
    return Brilho.estouro(paleta, Math.round(n / 2));
  }
  function particulasAntigas(cores, n = 60) {
    const cx = window.innerWidth / 2, cy = window.innerHeight * 0.42;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "particula";
      const ang = Math.random() * Math.PI * 2, dist = 120 + Math.random() * 320;
      p.style.left = cx + "px"; p.style.top = cy + "px";
      p.style.background = cores[i % cores.length];
      p.style.setProperty("--dx", Math.cos(ang) * dist + "px");
      p.style.setProperty("--dy", Math.sin(ang) * dist * 0.7 + "px");
      p.style.animationDelay = Math.random() * 0.25 + "s";
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1600);
    }
  }

  /** Um atributo para sempre (+2 Ataque de um evento): um selo surge no meio da tela, voa até o atributo (no painel;
   *  vida e recurso máximos, na barra da HUD), que brilha e conta até o valor novo. Não segura o jogo: o texto segue
   *  enquanto o selo voa. */
  const ICONE_SELO = { atk: "espada", defesa: "escudo", agi: "folha", poder: "chama", max_hp: "coracao", max_rec: "estrela" };
  function destinoAtributo(d) {
    if (d.stat === "max_hp" || d.stat === "max_rec") return document.querySelector(`#hud .vital[data-vital="${d.stat === "max_hp" ? "hp" : "rec"}"]`);
    return document.querySelector(`#heroi .atributo[data-atributo="${d.nome}"]`);
  }
  function seloAtributo(d) {
    const selo = document.createElement("div");
    selo.className = "selo-atributo";
    selo.innerHTML = `${Icones.atributo(d.nome, 64) || S(ICONE_SELO[d.stat] || "estrela", 4)}<b>+${d.valor}</b><span>${h(d.nome)}<small>permanente</small></span>`;
    document.body.appendChild(selo);
    selo.style.left = (innerWidth - selo.offsetWidth) / 2 + "px";  // centrado sem transform: o voo usa translate e scale
    App.som("aprender");
    const antes = d.total - d.valor, noPainel = !["max_hp", "max_rec"].includes(d.stat);
    if (noPainel) {  // o painel espera o selo chegar para mostrar o valor novo
      chegando.set(d.nome, antes);
      const v = destinoAtributo(d)?.querySelector(".valor .num");
      if (v) v.textContent = antes;
    }
    const voar = async () => {
      await new Promise((r) => setTimeout(r, 900));  // o selo fica um instante no meio, para ser lido
      const alvo = destinoAtributo(d), visivel = alvo && alvo.offsetParent;
      if (visivel) {
        const a = selo.getBoundingClientRect(), b = alvo.getBoundingClientRect();
        const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
        await selo.animate([{ translate: "0 0", scale: 1, opacity: 1 }, { translate: `${dx}px ${dy}px`, scale: 0.25, opacity: 0.6 }],
          { duration: 520, easing: "cubic-bezier(.5,0,.75,0)", fill: "forwards" }).finished.catch(() => {});
      } else await selo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: "forwards" }).finished.catch(() => {});
      selo.remove();
      if (noPainel) chegando.delete(d.nome);
      const aqui = destinoAtributo(d);  // o painel pode ter sido redesenhado enquanto o selo voava
      if (!aqui) return;
      aqui.classList.remove("ganhou"); void aqui.offsetWidth; aqui.classList.add("ganhou");
      setTimeout(() => aqui.classList.remove("ganhou"), 1100);
      const valor = aqui.querySelector(".valor .num");
      if (valor && noPainel) Sensacao.contar(valor, d.total, 520, { de: antes });
    };
    // O próximo só aparece quando este chega ao painel (dois seguidos, +1 Poder e +4 Vida, um tampava o outro
    // enquanto o primeiro ainda saía do meio).
    return voar().then(() => new Promise((r) => setTimeout(r, 150)));
  }

  /** Chegar a um lugar: o nome surge no meio da tela entre dois fios dourados, como o título de área dos jogos
   *  (Elden Ring, Diablo). Na primeira vez, "lugar descoberto", som e um pouco mais de tempo; na volta, curto. O nível
   *  da região vem na cor do perigo (o aviso por extenso fica no texto). Some sozinho; um clique ou uma tecla adianta. */
  function chegada(d) {
    const el = document.createElement("div");
    el.className = "chegada" + (d.primeira ? " primeira" : "");
    const tag = d.nivel ? `<span class="perigo-tag ${nivelPerigo(d.nivel)}">${d.tipo === "vila" ? "Arredores" : "Inimigos"} Nv.${d.nivel}</span>` : "";
    el.innerHTML = `${d.primeira ? '<div class="rotulo-festa">lugar descoberto</div>' : ""}<i class="linha-ouro"></i>
      <div class="nome-lugar">${h(d.nome)}</div><i class="linha-ouro"></i>
      <div class="sub-lugar">${h(d.sub)}${tag}</div>`;
    document.body.appendChild(el);
    if (d.primeira) App.som("achado");
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        el.classList.add("saindo");
        setTimeout(() => { el.remove(); resolver(); }, 420);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 300);
      setTimeout(fechar, d.primeira ? 2400 : 1300);
    });
  }

  function faixa(titulo, sub, icone, classe = "") {
    const f = document.createElement("div");
    f.className = "faixa-festa " + classe;
    // quem chega à comitiva: a cabeça do retrato; a espécie do mestre caçador: a cabeça própria dela, se tem
    const arte = icone ? Icones.cabeca(icone, 48) || Icones.criatura(icone, 48) || S(icone, 3) : "";
    f.innerHTML = `<b>${arte}${h(titulo)}${arte}</b>${sub ? `<span>${h(sub)}</span>` : ""}`;
    document.body.appendChild(f);
    // Sai quando a animação acaba (a sombria, do exausto, dura mais: um tempo fixo a cortava no meio da frase).
    f.addEventListener("animationend", (ev) => { if (ev.target === f) f.remove(); });
    setTimeout(() => f.remove(), 4000);
  }

  /** Mostra a celebração. Devolve uma Promise que resolve quando o jogador fecha (ou na hora, se rápida). */
  /** Os ganhos do nível contam de 0 até o valor, cada um com um tique. */
  function contarGanhos(caixa) {
    caixa.querySelectorAll(".conta").forEach((b) => {
      const alvo = Number(b.dataset.alvo), atraso = Number(b.dataset.atraso);
      setTimeout(() => {
        App.som("tique");
        const inicio = performance.now(), dur = 320;
        const passo = (agora) => {
          const t = Math.min(1, (agora - inicio) / dur);
          b.textContent = "+" + Math.round(alvo * (1 - Math.pow(1 - t, 3)));
          if (t < 1) requestAnimationFrame(passo);
        };
        requestAnimationFrame(passo);
      }, atraso);
    });
  }

  /** O ícone de um item voando de um ponto da tela até um elemento (o espaço do corpo, a mochila), num arco. */
  function voarIcone(item, origem, alvo) {
    const r = alvo.getBoundingClientRect();
    const voo = document.createElement("div");
    voo.className = "voo-item";
    voo.innerHTML = Icones.item(iconeItem(item), 48) || S(iconeItem(item), 3);
    document.body.appendChild(voo);
    const dx = r.left + r.width / 2 - origem.x, dy = r.top + r.height / 2 - origem.y;
    voo.style.left = origem.x - 24 + "px"; voo.style.top = origem.y - 24 + "px";
    return voo.animate([{ transform: "translate(0, 0) scale(1.2)", opacity: 1 },
      { transform: `translate(${dx * 0.5}px, ${dy * 0.5 - 60}px) scale(1)`, opacity: 1 },
      { transform: `translate(${dx}px, ${dy}px) scale(.45)`, opacity: 0.9 }],
      { duration: 560, easing: "cubic-bezier(.4,0,.2,1)" }).finished.catch(() => {}).then(() => voo.remove());
  }
  /** O cartão do item achado (na janela) recebe o selo do destino; devolve de onde o ícone sai. */
  function seloDoAchado(texto, classe, velhoTexto, espaco) {
    const tela = document.querySelector("#sobre-achado .tela.achado");
    if (!tela) return null;
    // o cartão do que estava no espaço que recebeu o achado (os anéis têm um cartão por espaço; os outros, um só)
    const novo = tela.querySelector(".achado-cartao.novo");
    const velho = tela.querySelector(`.achado-cartao.atual[data-espaco="${espaco}"]`) || tela.querySelector(".achado-cartao.atual:not([data-espaco])");
    if (novo) { novo.classList.add(classe); const selo = novo.querySelector(".achado-selo"); if (selo) selo.textContent = texto; }
    if (velho && velhoTexto) { velho.classList.add("guardado"); const selo = velho.querySelector(".achado-selo"); if (selo) selo.textContent = velhoTexto; }
    const a = novo && novo.querySelector(".achado-arte").getBoundingClientRect();
    return a && a.width ? { x: a.left + a.width / 2, y: a.top + a.height / 2 } : null;
  }
  /** Vestiu (comprou no mercado ou achou): o ícone voa até o espaço do corpo no painel, que brilha ao receber. Achado:
   *  o cartão vira "Vestido" e o do que estava naquele espaço diz para onde ele foi, como o motor contou ("Foi para a
   *  mochila", ou "Ficou para trás" com a mochila cheia; espaço vazio, nada); o ícone sai do cartão e a janela fecha. */
  async function voarParaEspaco(d) {
    const alvo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
    let origem = App.ultimoClique && performance.now() - App.ultimoClique.t < 4000 ? App.ultimoClique : { x: innerWidth / 2, y: innerHeight / 2 };
    const velho = { mochila: "Foi para a mochila", ficou: "Ficou para trás" }[d.antigo] || null;
    if (d.achado) origem = seloDoAchado("Vestido", "vestido", velho, d.espaco) || origem;
    if (alvo) {
      App.som("equipar");
      await voarIcone(d.item, origem, alvo);
      const novo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
      if (novo) { novo.classList.remove("recebeu"); void novo.offsetWidth; novo.classList.add("recebeu"); setTimeout(() => novo.classList.remove("recebeu"), 900); }
    }
    if (d.achado) fecharAchado();
  }
  /** Guardou o item achado: o cartão vira "Na mochila", o ícone voa até o Inventário e a janela fecha. */
  async function voarParaMochila(d) {
    const origem = seloDoAchado("Na mochila", "na-mochila");
    const alvo = document.querySelector('.atalho[data-rotulo="Inventário"]');
    App.som("item");
    if (origem && alvo && alvo.offsetParent) {
      await voarIcone(d.item, origem, alvo);
      alvo.classList.remove("recebeu"); void alvo.offsetWidth; alvo.classList.add("recebeu");
      setTimeout(() => alvo.classList.remove("recebeu"), 900);
    } else await new Promise((r) => setTimeout(r, 500));
    fecharAchado();
  }

  /** O balão da reação do animal: acima dele, no palco da fogueira. Some sozinho ou com qualquer clique. */
  function balaoFera(alvo, d) {
    document.querySelectorAll(".balao.da-fera").forEach((b) => b.remove());
    const b = document.createElement("div");
    b.className = "balao narrado da-fera";
    b.innerHTML = `<i>${h(d.texto)}</i>${d.efeito ? `<small class="balao-efeito">${h(d.efeito)}</small>` : ""}`;
    document.body.appendChild(b);
    const r = alvo.getBoundingClientRect();
    // Sobre o animal, alinhado pela esquerda (o rabicho aponta para ele): o meio do palco e a barraca ficam livres.
    b.style.left = Math.max(8, r.left + r.width / 2 - 22) + "px";
    b.style.top = Math.max(8, r.top + r.height * 0.35 - b.offsetHeight - 10) + "px";
    const nasceu = performance.now();
    const sair = () => { b.classList.add("sumindo"); setTimeout(() => b.remove(), 300); document.removeEventListener("pointerdown", aoClicar, true); };
    const aoClicar = () => { if (performance.now() - nasceu > 300) sair(); };
    document.addEventListener("pointerdown", aoClicar, true);
    setTimeout(sair, Math.min(9000, 3000 + d.texto.length * 45));
  }

  /** A derrota que encerra a luta (o motor só a manda nessa hora: a Pena de Fênix e a proteção não chegam aqui): a
   *  carta do herói cai e se apaga, a tela pulsa vermelho, a faixa diz o resultado ("Você caiu": vem o resgate; "Você
   *  morreu": modo hardcore) e um som curto. Depois, o cenário fica escuro (sem os prédios da vila) até o herói
   *  acordar (o amanhecer do resgate) ou o próximo menu: a vila não aparece como se ele já estivesse de pé. Cerca de
   *  2 s, adiantável pelo clique ou tecla de sempre; em seguida, a página nova do resgate (ou da morte), sem Continuar
   *  no meio (ponte.py: depois_da_queda). No replay e no instantâneo, só o escuro. */
  const QUEDA_MS = 2200;  // a queda inteira (a faixa dura um pouco mais e some sobre a página nova)
  function queda(d, instantaneo) {
    document.body.classList.add("derrotado");
    if (instantaneo) return Promise.resolve();
    document.querySelector('#arena .carta[data-uid="j"]')?.classList.add("caida");
    App.som("derrota");
    doer();
    faixa(d.morte ? "Você morreu" : "Você caiu", null, "caveira", "derrota");
    return (async () => { for (let t = 0; t < QUEDA_MS && !pular; t += 50) await new Promise((r) => setTimeout(r, 50)); })();
  }
  /** O herói acordou (o amanhecer do resgate) ou um menu chegou: o cenário volta à luz de sempre. */
  function fimDaQueda() { document.body.classList.remove("derrotado"); }

  function celebrar(m, instantaneo) {
    const d = m.dados;
    if (m.tipo === "equipou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaEspaco(d);
    if (m.tipo === "guardou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaMochila(d);
    if (m.tipo === "carinho") {
      // corações subindo do animal na cena da fogueira, e a reação num balão sobre ele (não tampa nada; um clique dispensa)
      if (instantaneo) return Promise.resolve();
      const alvos = document.querySelectorAll("#acampamento-pontos .figura.fera");
      const alvo = alvos[alvos.length - 1];
      if (alvo && d.texto) balaoFera(alvo, d);
      if (d.repetido) return Promise.resolve();
      App.som("cura");
      if (alvo) for (let i = 0; i < 6; i++) {
        const c = document.createElement("span");
        c.className = "coracao-carinho";
        c.textContent = "♥";
        c.style.left = 20 + Math.random() * 60 + "%";
        c.style.animationDelay = i * 110 + "ms";
        alvo.appendChild(c);
        setTimeout(() => c.remove(), 1600);
      }
      return new Promise((r) => setTimeout(r, 700));
    }
    if (m.tipo === "derrota") return queda(d, instantaneo);
    if (m.tipo === "correntes") return Telas.soltarCorrentes(instantaneo);  // o preparo gravado: a corrente desce
    if (m.tipo === "ilse") return Telas.momentoIlse(d, instantaneo);  // o que o texto acabou de contar de Ilse, no fundo
    if (m.tipo === "livro") return Telas.lerLivro(d, instantaneo);  // o livro da capela aberto, até o jogador fechar
    if (m.tipo === "vitoria") {
      if (instantaneo) return Promise.resolve();
      App.som("vitoria");
      faixa(d.chefe ? "Guardião derrotado!" : "Vitória", null, "espada");
      particulas(["#f2c94c", "#fff3a0", "#d4af37"], d.chefe ? 70 : 30);
      return new Promise((r) => setTimeout(r, d.chefe ? 1500 : 1000));
    }
    if (m.tipo === "mestre") {  // mestre caçador de uma espécie: a faixa de ouro com a criatura dos dois lados
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa("Mestre caçador", `${d.plural.charAt(0).toUpperCase() + d.plural.slice(1)}: +10% de dano contra eles`, d.retrato || "caveira");
      return new Promise((r) => setTimeout(r, 1800));
    }
    if (m.tipo === "exausto") {  // o dia acabou à força: uma faixa sombria, devagar, e a fogueira (ou o feno) em seguida
      if (instantaneo) return Promise.resolve();
      App.som("exausto");
      faixa("Exausto", d.texto, "lua", "sombria");
      return new Promise((r) => setTimeout(r, 2300));
    }
    if (m.tipo === "retirada") {  // a saída da capela antes de acampar (a arte do topo já passou ao lado de fora)
      if (instantaneo) return Promise.resolve();
      App.som(d.exausto ? "exausto" : "retirada");  // os passos que se afastam
      faixa(d.exausto ? "Exausto" : "Saindo da capela", d.texto, d.exausto ? "lua" : "fuga", "sombria");
      return new Promise((r) => setTimeout(r, 2600));
    }
    if (m.tipo === "comitiva") {
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa(`${d.nome} se junta a você`, d.titulo, d.id);
      return new Promise((r) => setTimeout(r, 1500));
    }
    const caixa = document.getElementById("celebracao");
    if (m.tipo === "contratos") return instantaneo ? Promise.resolve() : pagarContratos(caixa, d);
    if (m.tipo === "amanhecer") { fimDaQueda(); return instantaneo ? Promise.resolve() : amanhecer(caixa, d); }
    if (m.tipo === "espolio") return instantaneo ? Promise.resolve() : Sensacao.espolio(caixa, d);
    if (m.tipo === "atributo") return instantaneo ? Promise.resolve() : seloAtributo(d);
    if (m.tipo === "chegada") return instantaneo ? Promise.resolve() : chegada(d);
    let html = "", festa = null;
    if (m.tipo === "nivel") {
      // PROTÓTIPO etapa 2: os ganhos com os ícones da HUD (os vitais em 20, os atributos em 24), o valor final já escrito
      // (sem contar de zero: o ganho se lê na hora), em cascata curta; o ponto de talento com o ícone dos Talentos
      const VITAIS = ["Vida", "Mana", "Vigor", "Foco"];
      const iconeGanho = (k) => (VITAIS.includes(k) ? Icones.vital(k, 20) : Icones.atributo(k, 24)) || S({ Vida: "coracao", Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" }[k] || "estrela", 1);
      const lista = Object.entries(d.ganhos);
      const ganhos = lista.map(([k, v], i) => `<span class="ganho-px" style="--i:${i}">${iconeGanho(k)}<b>+${v}</b><span>${h(k)}</span></span>`).join("");
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="--i:${lista.length + 1 + i}"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
      html = `<div class="festa festa-nivel festa-px m-janela">
        <div class="rotulo-festa">você subiu de nível</div>
        <div class="nivel-bloco"><span class="nivel-palavra">Nível</span><span class="nivel-numero">${d.nivel}</span></div>
        <div class="ganhos-px">${ganhos}</div>
        <div class="talento-px" style="--i:${lista.length}">${Icones.atalho("Talentos", 32) || S("estrela", 2)}+1 ponto de talento <small>Talentos (T)</small></div>${habs}
        ${d.especializacao ? '<div class="texto-festa" style="color:var(--arcano)">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      festa = () => { App.som("subir"); return Brilho.explosao(caixa.querySelector(".festa"), { paleta: "ouro", intensidade: 2, coluna: false, centro: caixa.querySelector(".nivel-numero") }); };
    } else if (m.tipo === "sigilo") {
      const los = [0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}${i === d.sigilos - 1 ? " novo" : ""}"></i>`).join("");
      html = `<div class="festa festa-px m-janela"><div class="rotulo-festa">${h(d.guardiao)} caiu</div><div class="grande">Sigilo ${d.sigilos}/3</div>
        <div class="losangos">${los}</div><div class="texto-festa">Uma runa ardente se grava na sua mão.</div>
        <div class="lista"><span class="ganho ouro">${S("estrela", 1)}+1 ponto de talento</span></div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      festa = () => { App.som("fanfarra"); return Brilho.explosao(caixa.querySelector(".festa"), { paleta: "sigilo", intensidade: 3, coluna: false, centro: caixa.querySelector(".grande") }); };
    } else if (m.tipo === "spec") {
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${0.6 + i * 0.25}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
      html = `<div class="festa festa-px m-janela"><div class="rotulo-festa">você agora é</div><div class="grande arcano">${h(d.nome)}</div>
        <div class="texto-festa">${h(d.desc)}</div>${habs}<button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      festa = () => { App.som("fanfarra"); return Brilho.explosao(caixa.querySelector(".festa"), { paleta: "arcano", intensidade: 2, coluna: false, centro: caixa.querySelector(".grande") }); };
    } else {
      return Promise.resolve();
    }
    // Sem cerimônia (refazendo a página ou no texto instantâneo), a festa não aparece: nem a janela, nem o som e o estouro
    // de partículas dela. Antes eles saíam assim mesmo, e a página refeita soltava um estouro por nível ganho de uma vez.
    if (instantaneo) return Promise.resolve();
    caixa.innerHTML = html;
    caixa.hidden = false;
    const el = caixa.querySelector(".festa"), botao = caixa.querySelector(".continuar");
    const efeito = festa ? festa() : null;
    // PROTÓTIPO etapa 2: sem a espera de 600 ms das teclas. A revelação (a cascata dos ganhos, o brilho) leva uns 0,6 s;
    // durante ela, um clique fora do botão só a completa; o Continuar, o Enter, o Espaço e o Esc fecham a qualquer
    // momento. Como no quadro do espólio (Gesto): não contam o toque que começou antes de a festa abrir, o 2º clique de
    // um clique duplo nem a tecla segurada; o gesto que fecha não atravessa para a página (nem para a festa seguinte).
    const nasceu = performance.now();
    let toque = 0, revelado = false;
    const revelar = () => { if (revelado) return; revelado = true; el.classList.add("revelada"); if (efeito) efeito.parar(); };
    const auto = setTimeout(revelar, 650);
    const sel = window.getSelection(); if (sel) sel.removeAllRanges();  // a seleção que o clique duplo deixou
    botao.focus({ preventScroll: true });
    return new Promise((resolver) => {
      const fechar = () => {
        clearTimeout(auto);
        caixa.hidden = true; caixa.innerHTML = "";
        document.removeEventListener("pointerdown", tocou, true);
        document.removeEventListener("click", clique, true);
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tocou = () => { toque = performance.now(); };
      const clique = (ev) => {
        if (ev.detail > 1 || toque < nasceu) { ev.preventDefault(); ev.stopPropagation(); return; }
        ev.preventDefault(); ev.stopPropagation();
        if (ev.target.closest(".continuar") || revelado) fechar(); else revelar();
      };
      const tecla = (ev) => {
        if (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key)) return;
        ev.preventDefault(); ev.stopPropagation(); fechar();
      };
      document.addEventListener("pointerdown", tocou, true);
      document.addEventListener("click", clique, true);
      document.addEventListener("keydown", tecla, true);
    });
  }

  /** Contratos cumpridos: os cartazes chegam, o carimbo bate em cada um, o total aparece, e "Receber" faz as
   *  moedas voarem até o seu ouro. Um momento só, em vez de três blocos de texto no registro. */
  function pagarContratos(caixa, d) {
    const um = d.contratos.length === 1;
    const cartazes = d.contratos.map((c, i) => `<div class="pago" style="--i:${i}">${cartaz({ ...c, recebendo: true }, true, false, App.estado ? App.estado.heroi.nivel : 1)}</div>`).join("");
    const atraso = 0.5 + d.contratos.length * 0.35;
    const ganhos = [[d.ouro, "moeda", "ouro", "ouro"], [d.xp, "estrela", "XP", ""], [d.reputacao, "coroa", "reputação", "rep"]]
      .filter(([v]) => v > 0)
      .map(([v, ic, nome, cls], i) => `<span class="ganho ${cls}" style="animation-delay:${atraso + i * 0.15}s">${Icones.miudo(ic) || S(ic, 1)}+${v} ${nome}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-contratos m-janela">
      <div class="rotulo-festa">${um ? "contrato cumprido" : `${d.contratos.length} contratos cumpridos`}</div>
      <div class="cartazes-pagos">${cartazes}</div>
      <div class="lista">${ganhos}</div>
      <button class="continuar" type="button">Receber recompensa <span>▸</span></button></div>`;
    caixa.hidden = false;
    App.som("achado");
    d.contratos.forEach((_, i) => setTimeout(() => App.som("equipar"), (0.45 + i * 0.35) * 1000));
    return new Promise((resolver) => {
      let feito = false;
      const receber = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        App.som("moeda");
        moedasPara(caixa.querySelector(".ganho.ouro") || caixa.querySelector(".continuar"), document.querySelector('.recurso[data-rec="ouro"]'));
        particulas(["#f2c94c", "#fff3a0", "#d4af37"], 40);
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; resolver(); }, 650);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); receber(); } };
      setTimeout(() => document.addEventListener("keydown", tecla, true), 600);
      caixa.querySelector(".continuar").addEventListener("click", (ev) => { ev.stopPropagation(); receber(); });
    });
  }

  /** A virada do dia: a aurora na paisagem, a faixa "Dia N" e o que a noite fez, em ícones (verde o que fez bem,
   *  amarelo o que pede atenção, vermelho o que dói). Noite tranquila: some sozinho; noite ruim: espera o clique. */
  const ICONE_NOITE = { bom: "bom", neutro: "", aviso: "aviso", perigo: "perigo" };

  function amanhecer(caixa, d) {
    if (typeof Vista !== "undefined") Vista.amanhecer(1800);
    App.som("amanhecer");
    const ruim = d.itens.some((x) => x.tipo === "perigo");
    const itens = d.itens.map((x, i) => `<span class="noite-item ${ICONE_NOITE[x.tipo] || ""}" style="animation-delay:${0.55 + i * 0.12}s"${x.texto && x.texto !== x.curto ? ` title="${h(x.texto)}"` : ""}>${S(x.icone, 1)}${h(x.curto)}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-amanhecer">
      <div class="rotulo-festa">amanhece</div>
      <div class="dia-numero">Dia ${d.dia}</div>
      <div class="dia-clima">${h(d.clima)}</div>
      ${itens ? `<div class="noite">${itens}</div>` : ""}
      ${ruim ? '<button class="continuar" type="button">Continuar <span>▸</span></button>' : ""}</div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    noPalco(caixa.querySelector(".festa-amanhecer"), true);
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        const festa = caixa.querySelector(".festa-amanhecer");
        if (festa) festa.classList.add("saindo");
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve"); resolver(); }, 260);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 500);
      if (!ruim) setTimeout(fechar, 2400 + d.itens.length * 350);
    });
  }

  /** Uma linha curta para o registro (histórico) de cada festa: o registro guarda o fato, a festa mostra. */
  function resumoCelebracao(m) {
    const d = m.dados || {};
    if (m.tipo === "nivel") return `▸ Nível ${d.nivel}: +1 ponto de talento${(d.habilidades || []).length ? ", " + d.habilidades.map((x) => x.nome).join(", ") : ""}`;
    if (m.tipo === "contratos") return `▸ ${d.contratos.length === 1 ? "Contrato cumprido" : d.contratos.length + " contratos cumpridos"}: +${d.ouro} ouro, +${d.xp} XP`;
    if (m.tipo === "sigilo") return `▸ Sigilo ${d.sigilos}/3 (${d.guardiao}): +1 ponto de talento`;
    if (m.tipo === "spec") return `▸ Você agora é ${d.nome}`;
    if (m.tipo === "espolio") return `▸ Espólio: ${d.ouro ? `+${d.ouro} ouro, ` : ""}+${d.xp} XP`;
    if (m.tipo === "atributo") return `▸ +${d.valor} ${d.nome} permanente`;
    if (m.tipo === "chegada") return `▸ ${d.primeira ? "Descoberto" : "Chegada"}: ${d.nome}`;
    if (m.tipo === "exausto") return `▸ Exausto: ${d.texto}`;
    if (m.tipo === "retirada") return `▸ ${d.exausto ? "Exausto: " : ""}${d.texto}`;
    if (m.tipo === "derrota") return d.morte ? "▸ Você morreu" : "▸ Você caiu";
    if (m.tipo === "livro") return "▸ Leu o livro da capela";
    if (m.tipo === "mestre") return `▸ Mestre caçador: ${d.plural} (+10% de dano contra eles)`;
    if (m.tipo === "equipou" && d.achado) return `▸ Vestiu: ${d.item.nome}`;
    if (m.tipo === "guardou") return `▸ Na mochila: ${d.item.nome}`;
    if (m.tipo === "amanhecer") return `▸ Dia ${d.dia} · ${d.clima}${d.itens.length ? " · " + d.itens.map((x) => x.curto).join(", ") : ""}`;
    return "";
  }

  Object.assign(Telas, { celebrar, resumoCelebracao, fimDaQueda });
})();
