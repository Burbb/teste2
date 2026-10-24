/* PROTÓTIPO da etapa 2, segunda rodada, direção estouro (montado por auxiliares/montar_v2.py; nada no jogo). */
/* PROTÓTIPO da etapa 2, segunda rodada (24/10/2026; nada no jogo): FX, os efeitos em pixel das celebrações.
   Um palco de baixa resolução (um canvas em texels de 3 px do aparelho, ampliado sem suavização) e as peças que as três
   direções compõem: raios que giram, feixes, halos, anéis de choque, colunas de luz, clarões e partículas desenhadas à
   mão (grades de texto, como os sprites do jogo). Cor só da paleta do jogo (Sprites.PALETA); degradê só por pontilhado
   ordenado (Sprites.pontilha) e por faixas de cor; movimento em quadros (15 por segundo), sem interpolação suave. */
"use strict";

const FX = (() => {
  const { PALETA, pontilha } = Sprites;
  const cache = {};
  /** "#rrggbb" (ou a letra da paleta) em ABGR, como o ImageData guarda. */
  function cor(c) {
    if (cache[c] !== undefined) return cache[c];
    const hex = c.length === 1 ? PALETA[c] : c;
    const v = parseInt(hex.slice(1), 16);
    return (cache[c] = ((255 << 24) | ((v & 255) << 16) | (v & 0xff00) | (v >> 16)) >>> 0);
  }
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const FPS = 15, QUADRO = 1000 / FPS;

  // As paletas, do miolo (mais claro) para a borda, todas da paleta do jogo.
  const PALETAS = {
    ouro: ["W", "Y", "y", "c", "C"], lendario: ["W", "Y", "O", "o", "r"], raro: ["W", "Y", "y", "c", "C"],
    magico: ["W", "M", "U", "u", "v"], comum: ["W", "w", "G", "g", "d"], sigilo: ["Y", "O", "R", "r", "D"],
    arcano: ["W", "M", "m", "x", "v"],
  };

  // ------------------------------------------------------------------ o palco
  /** Um canvas de baixa resolução cobrindo o `host` (fixo na tela inteira por padrão). */
  function palco(host, { z = 0, classe = "" } = {}) {
    const dpr = window.devicePixelRatio || 1, T = 3 * Math.max(1, Math.round(dpr));
    const W = Math.ceil((innerWidth * dpr) / T), H = Math.ceil((innerHeight * dpr) / T);
    const el = document.createElement("canvas");
    el.width = W; el.height = H;
    el.className = "fx-palco " + classe;
    el.setAttribute("aria-hidden", "true");
    el.style.cssText = `position:fixed;left:0;top:0;width:${(W * T) / dpr}px;height:${(H * T) / dpr}px;` +
      `image-rendering:pixelated;pointer-events:none;z-index:${z}`;
    host.prepend(el);
    const ctx = el.getContext("2d"), img = ctx.createImageData(W, H), buf = new Uint32Array(img.data.buffer);
    const p = {
      el, W, H, buf,
      /** O texel do ponto (x, y) da tela, em px de CSS. */
      tx: (x) => Math.round((x * dpr) / T), ty: (y) => Math.round((y * dpr) / T),
      /** O texel do meio de um elemento (e a meia largura e a meia altura dele, em texels). */
      de(elemento) {
        const r = elemento.getBoundingClientRect();
        return { x: p.tx(r.left + r.width / 2), y: p.ty(r.top + r.height / 2), rx: p.tx(r.width / 2), ry: p.ty(r.height / 2),
          topo: p.ty(r.top), base: p.ty(r.bottom), esq: p.tx(r.left), dir: p.tx(r.right) };
      },
      /** Quantos texels cabem em `px` de CSS. */
      t: (px) => Math.round((px * dpr) / T),
      por(x, y, c) { if (x >= 0 && y >= 0 && x < W && y < H) buf[y * W + x] = c; },
      limpar() { buf.fill(0); },
      mostrar() { ctx.putImageData(img, 0, 0); },
    };
    return p;
  }

  /** Roda `desenhar(t, quadro, parado)` a 15 quadros por segundo até `parar`. `pular(ms)` leva a linha do tempo até
   *  `ms` (o gesto que adianta a entrada). Com o movimento reduzido, um quadro só, em `parado` (a composição fica). */
  function animar(p, desenhar, { parado = 1500 } = {}) {
    let fim = false, t0 = performance.now(), q = -1;
    const um = (t) => { p.limpar(); desenhar(t, Math.round(t / QUADRO), reduzido()); p.mostrar(); };
    if (reduzido()) { um(parado); return { parar() { fim = true; }, pular() {}, agora: () => parado }; }
    const passo = (agora) => {
      if (fim || !p.el.isConnected) return;
      const n = Math.floor((agora - t0) / QUADRO);
      if (n !== q) { q = n; um(n * QUADRO); }
      requestAnimationFrame(passo);
    };
    um(0); q = 0;
    requestAnimationFrame(passo);
    return {
      parar() { fim = true; },
      pular(ms) { const ja = performance.now() - t0; if (ja < ms) t0 = performance.now() - ms; },
      agora: () => performance.now() - t0,
    };
  }

  // ------------------------------------------------------------------ as peças
  const nivelFade = (u, de) => (u <= de ? 16 : Math.max(0, Math.round(16 * (1 - (u - de) / (1 - de)))));

  /** Raios de sol em volta de (cx, cy): `n` cunhas de bordas duras, `larg` (0 a 1) acesa de cada passo, do raio `r0`
   *  ao `r1`, em faixas da paleta (miolo perto do centro, borda longe), com o fio do meio de cada raio mais claro e o
   *  fim apagando em pontilhado a partir de `esbate` (fração de r1). `vis` (0 a 16) apaga tudo por igual. */
  function raios(p, { cx, cy, n, ang = 0, larg = 0.5, r0 = 0, r1, pal, esbate = 0.55, vis = 16, fio = true, achata = 1,
    alterna = 1, alcance = null }) {
    if (r1 <= r0 || vis <= 0) return;
    const passo = (2 * Math.PI) / n, cs = pal.map(cor);
    const y0 = Math.max(0, Math.floor(cy - r1 * achata)), y1 = Math.min(p.H - 1, Math.ceil(cy + r1 * achata));
    const x0 = Math.max(0, Math.floor(cx - r1)), x1 = Math.min(p.W - 1, Math.ceil(cx + r1));
    const r12 = r1 * r1, r02 = r0 * r0;
    for (let y = y0; y <= y1; y++) {
      const dy = (y - cy) / achata;
      for (let x = x0; x <= x1; x++) {
        const dx = x - cx, d2 = dx * dx + dy * dy;
        if (d2 > r12 || d2 < r02) continue;
        const d = Math.sqrt(d2), at = Math.atan2(dy, dx);
        let f = (at - ang) / passo;
        const k = Math.floor(f);
        f -= k;
        if (f > larg) continue;
        // o comprimento deste raio: os ímpares mais curtos (`alterna`) e, se pedido, pela direção (`alcance`)
        const r1e = r1 * (k & 1 ? alterna : 1) * (alcance ? alcance(at) : 1), u = d / r1e;
        if (u > 1) continue;
        if (!pontilha(x, y, Math.min(vis, nivelFade(u, esbate)))) continue;
        const borda = Math.min(f, larg - f) * passo * d;  // texels até a aresta do raio
        let i = u < 0.28 ? 1 : u < 0.55 ? 2 : 3;
        if (fio && Math.abs(f - larg / 2) * passo * d < 0.6 && u < 0.8) i -= 1;  // o fio claro do meio
        else if (borda < 1) i += 1;  // a aresta, um tom abaixo
        p.buf[y * p.W + x] = cs[Math.max(0, Math.min(cs.length - 1, i))];
      }
    }
  }

  /** Feixes de holofote saindo de (cx, cy) nos ângulos `angs` (radianos; 0 = para a direita, -π/2 = para cima), cada um
   *  com meia abertura `meia`, até `r1`; a luz mais forte no eixo, a borda em pontilhado. */
  function feixes(p, { cx, cy, angs, meia, r1, pal, vis = 16, esbate = 0.5 }) {
    const cs = pal.map(cor);
    for (const a of angs) {
      const ca = Math.cos(a), sa = Math.sin(a);
      // a caixa do feixe: a ponta e o fim aberto
      const fx = cx + ca * r1, fy = cy + sa * r1, w = Math.tan(meia) * r1;
      const x0 = Math.max(0, Math.floor(Math.min(cx, fx) - w)), x1 = Math.min(p.W - 1, Math.ceil(Math.max(cx, fx) + w));
      const y0 = Math.max(0, Math.floor(Math.min(cy, fy) - w)), y1 = Math.min(p.H - 1, Math.ceil(Math.max(cy, fy) + w));
      for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
        const dx = x - cx, dy = y - cy, ao = dx * ca + dy * sa;  // ao longo do eixo
        if (ao <= 0 || ao > r1) continue;
        const lado = Math.abs(-dx * sa + dy * ca), meiaAqui = Math.tan(meia) * ao + 0.5;
        if (lado > meiaAqui) continue;
        const u = ao / r1, v = lado / meiaAqui;
        if (!pontilha(x, y, Math.min(vis, nivelFade(u, esbate), v > 0.7 ? 9 : 16))) continue;
        const i = v < 0.2 ? 0 : v < 0.5 ? 1 : v < 0.8 ? 2 : 3;
        p.buf[y * p.W + x] = cs[Math.min(cs.length - 1, i + (u > 0.6 ? 1 : 0))];
      }
    }
  }

  /** Um halo em faixas concêntricas (a mais clara no meio), a última em pontilhado. */
  function halo(p, { cx, cy, r, pal, vis = 16, achata = 1, faixas = null }) {
    if (r <= 0) return;
    const cs = pal.map(cor), nf = faixas || cs.length;
    for (let y = Math.floor(cy - r * achata); y <= cy + r * achata; y++) for (let x = Math.floor(cx - r); x <= cx + r; x++) {
      const dx = x - cx, dy = (y - cy) / achata, u = Math.sqrt(dx * dx + dy * dy) / r;
      if (u > 1) continue;
      const i = Math.min(nf - 1, Math.floor(u * nf));
      const nivel = i === nf - 1 ? 6 : i === nf - 2 ? 11 : 16;
      if (pontilha(x, y, Math.min(vis, nivel))) p.por(x, y, cs[Math.min(cs.length - 1, i)]);
    }
  }

  /** Um anel (a onda de choque): raio `r`, espessura `esp`, achatado em y por `achata`; o rastro por dentro em
   *  pontilhado. */
  function anel(p, { cx, cy, r, esp = 2, pal, achata = 1, rastro = 4, vis = 16 }) {
    const cs = pal.map(cor), ext = r + esp;
    for (let y = Math.floor(cy - ext * achata); y <= cy + ext * achata; y++) for (let x = Math.floor(cx - ext); x <= cx + ext; x++) {
      const dx = x - cx, dy = (y - cy) / achata, d = Math.sqrt(dx * dx + dy * dy);
      if (d > ext || d < r - rastro) continue;
      if (d >= r) { if (pontilha(x, y, vis)) p.por(x, y, cs[d - r < esp / 2 ? 0 : 1]); }
      else if (pontilha(x, y, Math.min(vis, Math.round(10 * (1 - (r - d) / rastro))))) p.por(x, y, cs[2] ?? cs[1]);
    }
  }

  /** Uma coluna de luz de cima até `base`, centrada em `cx`: o miolo, as bordas em faixas e listras que escorrem. */
  function coluna(p, { cx, base, larg, pal, q = 0, vis = 16, topo = 0 }) {
    const cs = pal.map(cor);
    for (let y = Math.max(0, topo); y < Math.min(base, p.H); y++) {
      const extra = ((((y >> 2) - q) % 6) + 6) % 6 === 0 ? 1 : 0, m = larg + extra;
      for (let d = -(m + 6); d <= m + 6; d++) {
        const x = cx + d, a = Math.abs(d);
        if (!pontilha(x, y, vis)) continue;
        if (a <= m * 0.4) p.por(x, y, cs[0]);
        else if (a <= m) p.por(x, y, cs[1]);
        else if (a <= m + 2) p.por(x, y, cs[2]);
        else if (pontilha(x, y, 16 - (a - m - 2) * 4)) p.por(x, y, cs[3]);
      }
    }
  }

  /** Um clarão na tela inteira (ou num retângulo), em pontilhado de `nivel` (0 a 16). */
  function clarao(p, nivel, c = "W", r = null) {
    const v = cor(c), [x0, y0, x1, y1] = r || [0, 0, p.W, p.H];
    for (let y = Math.max(0, y0); y < Math.min(p.H, y1); y++) for (let x = Math.max(0, x0); x < Math.min(p.W, x1); x++)
      if (pontilha(x, y, nivel)) p.buf[y * p.W + x] = v;
  }

  /** Uma estrela de pontas (a placa do estouro): `pontas` pontas entre os raios `ri` e `re`, girada `ang`, preenchida
   *  em faixas da paleta de fora para dentro, com contorno escuro de um texel e o lado de cima-esquerda mais claro. */
  function estrela(p, { cx, cy, pontas, ri, re, ang = 0, pal, contorno = "k", cores = null }) {
    // `cores` ([miolo, meio, aro, luz do aro]) troca as faixas da paleta: o selo de miolo escuro e aro de metal
    const cs = cores ? [cores[3], cores[0], cores[1], cores[2]].map(cor) : pal.map(cor), ck = cor(contorno), passo = (2 * Math.PI) / pontas;
    const raioEm = (a) => {
      let f = (a - ang) / passo; f -= Math.floor(f);
      const t = Math.abs(f - 0.5) * 2;  // 1 na ponta, 0 no vale
      return ri + (re - ri) * t;
    };
    for (let y = Math.floor(cy - re - 1); y <= cy + re + 1; y++) for (let x = Math.floor(cx - re - 1); x <= cx + re + 1; x++) {
      const dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy), a = Math.atan2(dy, dx), r = raioEm(a);
      if (d > r + 1) continue;
      if (d > r) { p.por(x, y, ck); continue; }
      const u = d / r;
      let i = u < 0.45 ? 1 : u < 0.75 ? 2 : 3;
      if (u > 0.82 && (dx + dy) < 0) i -= 1;  // a luz de cima e da esquerda na borda
      p.por(x, y, cs[Math.max(0, Math.min(cs.length - 1, i))]);
    }
  }

  /** Um poço escuro (uma elipse de raios rx, ry) que apaga em pontilhado do meio para a borda: o efeito passa por
   *  trás da área de leitura sem disputar com o texto. `forca` (0 a 16) é o escuro no meio. */
  function poco(p, { cx, cy, rx, ry, forca = 14, c = "N" }) {
    const v = cor(c);
    for (let y = Math.max(0, Math.floor(cy - ry)); y <= Math.min(p.H - 1, cy + ry); y++)
      for (let x = Math.max(0, Math.floor(cx - rx)); x <= Math.min(p.W - 1, cx + rx); x++) {
        const dx = (x - cx) / rx, dy = (y - cy) / ry, u = Math.sqrt(dx * dx + dy * dy);
        if (u > 1) continue;
        if (pontilha(x, y, Math.round(forca * Math.min(1, (1 - u) * 4)))) p.buf[y * p.W + x] = v;  // cheio até 3/4, depois apaga
      }
  }

  /** O clarão concentrado na origem: um halo claro que abre e apaga em `dur` ms em volta de (cx, cy), e só um
   *  pontilhado baixo (`espalha`, 0 a 16) na tela inteira nos dois primeiros quadros. O prêmio e a leitura continuam
   *  reconhecíveis. */
  function claraoLocal(p, { cx, cy, r, t, dur = 180, espalha = 2, pal = ["W", "W", "Y", "O"] }) {
    if (t > dur) return;
    const u = t / dur;
    if (t < 140 && espalha) clarao(p, espalha, "W");
    halo(p, { cx, cy, r: Math.round(r * (0.7 + u * 0.6)), pal, vis: Math.round(15 * (1 - u)) });
  }

  // ------------------------------------------------------------------ partículas desenhadas à mão
  // Cada grade: "a" é a cor da idade da partícula, "b" a um tom mais claro; "." vazio.
  const DESENHOS = {
    ponto: ["a"],
    duplo: ["ab"],
    cruz: [".a.", "aba", ".a."],
    estrela: ["..a..", "..a..", "aabaa", "..a..", "..a.."],
    brilho: ["...a...", "...a...", "..aba..", "aabbbaa", "..aba..", "...a...", "...a..."],
    losango: ["..a..", ".aba.", "abbba", ".aba.", "..a.."],
    lasca: ["ab", "a."],
    caco: [".ab", "aba", "a.."],
    brasa: ["b", "a"],
    moeda: [".aa.", "abba", "abba", ".aa."],
  };
  /** Um enxame: `soltar(n, gerar)` cria partículas ({x, y, vx, vy, g, arrasto, vida, desenho, pal, piscar}); `passo()`
   *  move um quadro; `desenhar(p)` pinta cada uma pela idade (o tom vai do claro ao escuro da paleta). */
  function enxame() {
    const lista = [];
    return {
      lista,
      soltar(n, gerar) { for (let i = 0; i < n; i++) lista.push({ idade: 0, g: 0, arrasto: 1, piscar: false, ...gerar(i) }); },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const s = lista[i];
          s.idade++;
          if (s.idade > s.vida) { lista.splice(i, 1); continue; }
          s.vx *= s.arrasto; s.vy = s.vy * s.arrasto + s.g;
          s.x += s.vx; s.y += s.vy;
        }
      },
      desenhar(p) {
        for (const s of lista) {
          if (s.piscar && s.idade % 3 === 2) continue;
          const g = DESENHOS[s.desenho] || DESENHOS.ponto, cs = s.pal;
          const k = Math.min(cs.length - 1, Math.floor((s.idade / (s.vida + 1)) * cs.length) + (s.tom || 0));
          const a = cor(cs[k]), b = cor(cs[Math.max(0, k - 1)]);
          const ox = Math.round(s.x) - (g[0].length >> 1), oy = Math.round(s.y) - (g.length >> 1);
          for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
            const ch = g[y][x];
            if (ch === "a") p.por(ox + x, oy + y, a);
            else if (ch === "b") p.por(ox + x, oy + y, b);
          }
        }
      },
    };
  }

  /** A tela inteira treme alguns quadros (em pixels inteiros, cada vez menos). */
  function tremer(px) {
    if (reduzido() || !px) return;
    const passos = [1, -0.8, 0.6, -0.45, 0.3, -0.15, 0];
    passos.forEach((f, i) => setTimeout(() => {
      document.body.style.translate = f ? `${Math.round(px * f)}px ${Math.round(px * f * -0.5)}px` : "";
    }, i * QUADRO));
  }

  /** Um valor que sai de `a` e chega a `b` em `ms`, em degraus (ease-out), para a linha do tempo dos efeitos. */
  const rampa = (t, de, ms, a = 0, b = 1) => (t <= de ? a : t >= de + ms ? b : a + (b - a) * (1 - Math.pow(1 - (t - de) / ms, 3)));
  const aleatorio = (a, b) => a + Math.random() * (b - a);

  return { cor, reduzido, FPS, QUADRO, PALETAS, DESENHOS, palco, animar, raios, feixes, halo, anel, coluna, clarao, claraoLocal, estrela, poco,
    enxame, tremer, rampa, aleatorio };
})();

/* PROTÓTIPO da etapa 2, segunda rodada (24/10/2026; nada no jogo): Festa, o que as três direções têm em comum.
   - os dados de cada festa já em pedaços (os ganhos com os ícones da HUD, o ponto de talento, as habilidades);
   - a regra dos gestos: o Continuar, o Enter, o Espaço e o Esc fecham a qualquer momento; um clique fora durante a
     entrada só a adianta; não contam o toque que começou antes de a festa abrir, o 2º clique de um clique duplo nem a
     tecla segurada; o gesto que fecha não atravessa para a página (nem para a festa seguinte);
   - o achado: a janela, o adiantar (um clique ou tecla durante a entrada leva ao fim dela; não escolhe nada, os botões
     ainda não estão lá) e a ordem do motor (os botões chegam quando a entrada termina).
   Cada direção (Festa.direcao) só diz o desenho: o HTML e o efeito. */
"use strict";

const Festa = (() => {
  const h = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const VITAIS = ["Vida", "Mana", "Vigor", "Foco"];
  const RARIDADE = { comum: "Comum", magico: "Mágico", raro: "Raro", lendario: "Lendário" };
  const CLASSE = { guerreiro: "Guerreiro", arqueiro: "Arqueiro", mago: "Mago" };
  let direcao = null;

  /** O ícone de um ganho de nível (o da HUD: os vitais e os atributos). */
  function icone(k, lado = 24) {
    return (VITAIS.includes(k) ? Icones.vital(k, lado === 24 ? 20 : lado) : Icones.atributo(k, lado)) || "";
  }
  const ganhos = (d) => Object.entries(d.ganhos || {}).map(([k, v]) => ({ k, v, icone: icone(k) }));
  const talento = (lado = 32) => Icones.atalho("Talentos", lado) || "";
  const habilidades = (lista) => (lista || []).map((x) => ({ nome: h(x.nome), desc: Realce.texto(x.desc), icone: Telas.S(x.icone || "estrela", 2) }));
  /** O Continuar no acabamento dos botões do jogo (a face e a aresta da HUD), com a tecla. */
  const continuar = (rotulo = "Continuar") => `<button class="continuar" type="button">${rotulo}<kbd>Enter</kbd></button>`;
  const heroi = () => (App.estado && App.estado.heroi) || {};

  /** A janela da festa aberta em `caixa` (#celebracao) com `html`; `efeito(el)` liga o efeito e devolve o controle dele
   *  ({ parar, revelar }). Resolve quando o jogador fecha. */
  function abrir(caixa, html, efeito, { revelaEm = 900 } = {}) {
    caixa.innerHTML = html;
    caixa.hidden = false;
    caixa.classList.add("festa-v2", "dir-" + direcao.nome);
    const el = caixa.querySelector(".festa"), botao = caixa.querySelector(".continuar");
    const sel = window.getSelection(); if (sel) sel.removeAllRanges();  // a seleção que um clique duplo deixou
    const ctl = efeito ? efeito(el, caixa) || {} : {};
    const nasceu = performance.now();
    let toque = 0, revelado = false;
    const revelar = () => { if (revelado) return; revelado = true; el.classList.add("revelada"); if (ctl.revelar) ctl.revelar(); };
    const auto = setTimeout(revelar, revelaEm);
    botao.focus({ preventScroll: true });
    return new Promise((resolver) => {
      const fechar = () => {
        clearTimeout(auto);
        if (ctl.parar) ctl.parar();
        caixa.hidden = true; caixa.innerHTML = "";
        caixa.classList.remove("festa-v2", "dir-" + direcao.nome);
        document.body.style.translate = "";
        document.removeEventListener("pointerdown", tocou, true);
        document.removeEventListener("click", clique, true);
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tocou = () => { toque = performance.now(); };
      const clique = (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        if (ev.detail > 1 || toque < nasceu) return;
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

  /** O nível, o Sigilo e a especialização, pela direção escolhida. */
  function celebrar(m, caixa, instantaneo) {
    if (!["nivel", "sigilo", "spec"].includes(m.tipo) || instantaneo) return Promise.resolve();
    const d = m.dados, f = direcao[m.tipo](d);
    return abrir(caixa, f.html, f.efeito, f);
  }

  // ------------------------------------------------------------------ o achado
  const adiar = (ms, cancelado) => new Promise((r) => {
    const fim = performance.now() + App.ritmo(ms);
    const ver = () => (cancelado() || performance.now() >= fim ? r() : setTimeout(ver, 20));
    ver();
  });

  /** A janela do achado (no lugar de Telas.abrirAchado): o HTML da direção, os botões reservados (os rótulos que vêm
   *  com o cartão, invisíveis: a janela já nasce no tamanho final) e a entrada da direção. */
  async function abrirAchado(d, semCerimonia = false) {
    Telas.fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = `sobreposicao achado-v2 dir-${direcao.nome} rar-${h(d.item.raridade)}`;
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${direcao.achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild;
    if (direcao.noPalco) Telas.noPalco(janela);
    if (semCerimonia) { fundo.classList.add("pronto"); direcao.cerimonia({ fundo, janela, d, parado: true, adiantou: () => true }); return; }
    let adiantou = false;
    const adiantar = (ev) => {
      if (ev.type === "keydown" && (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key))) return;
      ev.preventDefault(); ev.stopPropagation();
      if (!adiantou) { adiantou = true; fundo.classList.add("adiantado"); }
    };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    try {
      await direcao.cerimonia({ fundo, janela, d, adiantou: () => adiantou, esperar: (ms) => adiar(ms, () => adiantou) });
    } finally {
      document.removeEventListener("pointerdown", adiantar, true);
      document.removeEventListener("keydown", adiantar, true);
    }
    fundo.classList.add("pronto");
  }

  /** O texto do item como o jogo escreve (htmlItem), com a raridade fora da linha do tipo: ela tem o selo próprio. */
  const textoItem = (it, comparando = true) => Telas.htmlItem(it, "", comparando).replace(/(<div class="tipo">[^<]*?) · [^<]*<\/div>/, "$1</div>");
  /** O desenho do item: o arquivo de 64 da interface ampliado 2× (fator inteiro), ou o sprite do jogo. */
  const arteItem = (it, lado = 64) => Icones.porDesenho(Telas.iconeItem(it), lado) || Telas.S(Telas.iconeItem(it), lado / 16);
  /** Os cartões do que você usa (um, ou os dois espaços de anel), como no jogo. */
  function equipados(d, classe = "") {
    const aneis = d.espacos && (d.equipados || []).length;
    if (aneis) return `<div class="achado-aneis ${classe}">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arteItem(e.item, 48)}</div><div>${textoItem(e.item, false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || ""}</div></div></div>`).join("")}</div>`;
    return (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)} ${classe}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arteItem(e, 48)}</div>${textoItem(e, false)}</div>`).join("");
  }
  /** O aviso da mochila cheia, como no jogo. */
  function aviso(d) {
    const aneis = d.espacos && (d.equipados || []).length;
    return !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
  }

  // As imagens da HUD por caminho absoluto: o estilo das direções é injetado na página, e o url() relativo das variáveis
  // (../hud/...) passaria a contar da página. O gesto não seleciona texto nas janelas.
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-festa-v2">
    :is(#celebracao, #sobre-achado, .achado-v2) { --m-principal: url(/static/hud/moldura-nove.png); --t-painel: url(/static/hud/textura-painel.png); }
    #celebracao.festa-v2 :is(.festa, .continuar) { user-select: none; }
    #celebracao.festa-v2 { overflow-y: auto; place-items: safe center; }
    .fx-palco { image-rendering: pixelated; }
    /* o item ampliado 2× ocupa a caixa dele (o efeito mira no meio dela); sem o brilho borrado e o pulo suave da produção */
    .achado-v2 .achado-arte { filter: none; animation: none; }
    .achado-v2 .achado-cartao.novo .achado-arte:not(.pequena) { width: 128px; height: 128px; margin: 0; }</style>`);

  /** A ficha do achado em pedaços, para as direções compor sem molduras: o nome, o tipo, os números do prêmio, a troca
   *  (o que muda, linha a linha, pelo Telas.linhasTroca do jogo) e o que você usa (cartões .achado-cartao.atual, que
   *  as celebrações de vestir e guardar procuram). Sem nada no espaço, a troca e o "você usa" ficam vazios. */
  function fichaItem(d) {
    const it = d.item, rar = h(it.raridade), hr = heroi();
    const linhas = (x) => h(x.bonus || "").split(", ").filter(Boolean).map((l) => `<span>${l}</span>`).join("") +
      (x.efeito ? `<span class="efeito">${h(x.efeito)}</span>` : "");
    const naoUsa = it.classe && hr.classe && it.classe !== hr.classe ? `<div class="pior">Só ${h({ guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" }[it.classe] || it.classe)} sabem usar isto.</div>` : "";
    const premio = `<div class="ficha-premio"><span class="ficha-rotulo">${h(Telas.NOME_ESPACO[it.slot] || "")}</span><div class="ficha-linhas">${linhas(it)}</div>${naoUsa}</div>`;
    const aneis = d.espacos && (d.equipados || []).length;
    let troca = "", usa = "";
    if (aneis) {
      usa = d.espacos.map((e) => e.item
        ? `<div class="achado-cartao atual rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
            <div class="ficha-usa-nome">${arteItem(e.item, 32)}<b class="r-${h(e.item.raridade)}">${h(e.item.nome)}</b></div>
            <div class="ficha-troca">${Telas.linhasTroca(it, e.item)}</div></div>`
        : `<div class="achado-cartao atual vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span></div>`).join("");
    } else if ((d.equipados || []).length) {
      const e = d.equipados[0];
      troca = `<div class="ficha-troca"><span class="ficha-rotulo">na troca</span>${Telas.linhasTroca(it, e)}</div>`;
      usa = `<div class="achado-cartao atual rar-${h(e.raridade)}"><span class="achado-selo">Você usa</span>
        <div class="ficha-usa-nome">${arteItem(e, 32)}<b class="r-${h(e.raridade)}">${h(e.nome)}</b></div>
        <div class="ficha-linhas">${linhas(e)}</div></div>`;
    }
    return {
      rar, nome: `<b class="ficha-nome r-${rar}">${h(it.nome)}</b>`, raridade: `<span class="ficha-raridade rar-${rar}">${RARIDADE[it.raridade] || rar}</span>`,
      premio, troca, usa, compara: !!(troca || usa),
      lore: it.lore ? `<div class="ficha-lore">"${h(it.lore)}"</div>` : "", aviso: aviso(d),
    };
  }

  return {
    h, RARIDADE, fichaItem, CLASSE, icone, ganhos, talento, habilidades, continuar, heroi, abrir, celebrar, abrirAchado, textoItem, arteItem,
    equipados, aviso,
    usar(d) { direcao = d; },
    get direcao() { return direcao; },
  };
})();

/* PROTÓTIPO (24/10/2026; nada no jogo): IDENTIDADE da especialização, separada da APRESENTAÇÃO. A apresentação
   (Relicário ou Estouro) faz a composição e a entrada; a identidade diz as cores e o comportamento visual da
   especialização. Piloto só com o Piromante (fogo); as outras especializações ficam para depois da avaliação.
   - o nome em ouro quente e laranja, em faixas duras (sem degradê suave), com a borda incandescente (um contorno
     vermelho e brasa que pisca em dois tons) e uma sombra escura para o contraste;
   - chamas pequenas desenhadas à mão (grades de texto, em quatro idades) nascem do contorno de cima das letras e
     sobem pouco: o corpo das letras fica parado e legível, e as chamas não descem sobre a descrição nem os botões;
   - a paleta do fogo para o fundo (os raios, as brasas). Com o movimento reduzido, um quadro parado das chamas. */
"use strict";

const Identidade = (() => {
  const POR_ESPECIALIZACAO = { Piromante: "fogo" };  // a festa da especialização manda o nome (o motor não manda o id)
  const FOGO = { pal: ["W", "Y", "O", "o", "r"], brasas: ["Y", "O", "o", "r", "D"] };
  // As chamas, da mais nova à que se apaga ("b" o miolo claro, "a" a borda); desenhadas à mão, em texels.
  const CHAMAS = [
    ["...a...", "...a...", "..aba..", "..aba..", ".abba..", ".abbba.", "abbbbba", "abbbbba", ".aaaaa."],
    ["..a..", "..a..", ".aba.", ".abba", "abbba", "abbba", ".aaa."],
    ["..a..", ".aba.", ".aba.", "abbba", ".aaa."],
    [".a.", "aba", "aba", ".a."],
    ["a", "a"],
  ];
  const CORES = [["Y", "W"], ["O", "Y"], ["O", "Y"], ["o", "O"], ["r", "o"]];  // [borda, miolo] por idade

  const qual = (nomeEspecializacao) => POR_ESPECIALIZACAO[nomeEspecializacao] || null;

  /** Os pontos do contorno de cima das letras de `el` (em texels do palco): o texto desenhado num canvas com a mesma
   *  fonte e, em cada coluna de um texel, onde a tinta começa (e os topos de dentro das letras, como o da curva). */
  function contorno(el, p) {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    const faixa = document.createRange(); faixa.selectNodeContents(el);
    const tr = faixa.getBoundingClientRect();
    const c = document.createElement("canvas");
    c.width = Math.ceil(tr.width) + 8; c.height = Math.ceil(tr.height) + 8;
    const x = c.getContext("2d");
    x.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    x.textBaseline = "alphabetic"; x.fillStyle = "#fff";
    const texto = el.textContent, m = x.measureText(texto);
    // a linha de base como o navegador põe: a meia entrelinha mais a subida da fonte (a métrica da fonte, não a da tinta)
    const fa = m.fontBoundingBoxAscent, fd = m.fontBoundingBoxDescent, asc = m.actualBoundingBoxAscent;
    const base = 4 + (tr.height - (fa + fd)) / 2 + fa;
    x.fillText(texto, 4 + (tr.width - m.width) / 2, base);
    const d = x.getImageData(0, 0, c.width, c.height).data, passo = Math.max(1, (r.width / Math.max(1, p.t(r.width))));
    const tinta = (px, py) => px >= 0 && py >= 0 && px < c.width && py < c.height && d[(Math.round(py) * c.width + Math.round(px)) * 4 + 3] > 120;
    const pontos = [];
    for (let px = 0; px < c.width; px += passo) for (let py = passo; py < c.height; py += passo)
      if (tinta(px, py) && !tinta(px, py - passo)) pontos.push({ x: p.tx(tr.left - 4 + px), y: p.ty(tr.top - 4 + py), alto: py < base - asc * 0.55 });
    return pontos;
  }

  /** As chamas: nascem nos pontos do contorno (mais nos topos das letras), sobem devagar balançando e envelhecem. */
  function chamas() {
    const lista = [];
    return {
      soltar(pontos, n) {
        if (!pontos.length) return;
        for (let i = 0; i < n; i++) {
          const altos = pontos.filter((q) => q.alto), de = altos.length && Math.random() < 0.7 ? altos : pontos;
          const q = de[Math.floor(Math.random() * de.length)];
          lista.push({ x: q.x, y: q.y + 2, vida: Math.round(FX.aleatorio(8, 13)), idade: 0, fase: Math.random() * 6 });
        }
      },
      passo() {
        for (let i = lista.length - 1; i >= 0; i--) {
          const f = lista[i];
          if (++f.idade > f.vida) { lista.splice(i, 1); continue; }
          f.y -= 0.55;
        }
      },
      /** `parado`: um quadro de chamas em idades variadas, para o movimento reduzido. */
      desenhar(p, parado = false) {
        for (const f of lista) {
          const k = Math.min(CHAMAS.length - 1, Math.floor((f.idade / (f.vida + 1)) * CHAMAS.length));
          const g = CHAMAS[k], [ca, cb] = CORES[k].map(FX.cor);
          const balanco = parado ? 0 : Math.round(Math.sin(f.idade * 0.9 + f.fase) * 0.6);
          const ox = Math.round(f.x) - (g[0].length >> 1) + balanco, oy = Math.round(f.y) - g.length + 1;
          for (let y = 0; y < g.length; y++) for (let x = 0; x < g[y].length; x++) {
            const ch = g[y][x];
            if (ch === "a") p.por(ox + x, oy + y, ca); else if (ch === "b") p.por(ox + x, oy + y, cb);
          }
        }
      },
      lista,
    };
  }

  /** O calor atrás do nome: um poço escuro logo atrás das letras (os raios ficam em volta; as letras e as chamas leem
   *  no escuro) e, na borda dele, um brilho baixo de brasa em pontilhado que tremula entre dois níveis. */
  function calor(p, el, q, parado) {
    const r = p.de(el), vis = parado ? 6 : 5 + ((q >> 1) % 2);
    FX.halo(p, { cx: r.x, cy: r.y + Math.round(r.ry * 0.2), r: Math.round(r.rx * 1.15), achata: 0.5, pal: ["o", "r", "D"], vis });
    FX.poco(p, { cx: r.x, cy: r.y, rx: r.rx + 18, ry: r.ry + 16, forca: 16 });
  }

  const css = `
  /* o nome do Piromante: ouro quente em faixas, borda incandescente, sombra para o contraste */
  .id-fogo { color: #ffd27a; background: linear-gradient(#fff3a0 0 34%, #ffb35c 34% 66%, #f0882f 66% 100%); -webkit-background-clip: text;
    background-clip: text; -webkit-text-fill-color: transparent; text-shadow: none !important;
    filter: drop-shadow(2px 0 0 #b3262b) drop-shadow(-2px 0 0 #b3262b) drop-shadow(0 -2px 0 #e0782f) drop-shadow(0 2px 0 #6e0d0d) drop-shadow(0 5px 0 #120604);
    animation: id-fogo-borda 0.53s steps(1) infinite; }
  @keyframes id-fogo-borda {
    50% { filter: drop-shadow(2px 0 0 #e0782f) drop-shadow(-2px 0 0 #b3262b) drop-shadow(0 -2px 0 #ffb35c) drop-shadow(0 2px 0 #6e0d0d) drop-shadow(0 5px 0 #120604); } }
  .id-fogo-sobre { color: #ffb35c !important; }
  @media (prefers-reduced-motion: reduce) { .id-fogo { animation: none; } }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-identidade">${css}</style>`);

  return { qual, FOGO, contorno, chamas, calor };
})();

/* PROTÓTIPO, direção B: ESTOURO (explosivo). O ganho chega como um golpe: o clarão de dois quadros, a tela treme, a onda
   de choque corre para fora, as linhas de velocidade e os estilhaços voam e caem; o número do nível bate no meio de uma
   estrela de pontas em pixel (como um selo carimbado) e uma fita atravessa a estrela. Os ganhos são fichas grossas que
   estalam uma a uma. Depois do golpe, a estrela respira e solta brasas. A raridade é a força do golpe: o comum levanta
   poeira; o mágico, um anel e faíscas; o raro, uma coluna de luz que cai no item, o choque e os cacos; o lendário, a
   coluna larga de brasa, a tela inteira piscando e tremendo, dois anéis e uma chuva de estilhaços. */
"use strict";

(() => {
  const { h, RARIDADE, ganhos, talento, habilidades, textoItem, arteItem, equipados, aviso } = Festa;
  const P = FX.PALETAS;
  const CACOS = ["lasca", "caco", "cruz", "duplo", "ponto"];

  /** Estilhaços saindo de (cx, cy) por um anel de raio r, com gravidade. */
  function estilhacos(enx, cx, cy, r, n, pal, forca = 1) {
    enx.soltar(n, (i) => {
      const a = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(2.5, 6.5) * forca;
      return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r * 0.8, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 2.2 * forca,
        g: 0.36, arrasto: 0.97, vida: Math.round(FX.aleatorio(18, 32)), desenho: CACOS[i % CACOS.length], pal, piscar: i % 5 === 0 };
    });
  }
  /** Brasas que sobem de uma faixa embaixo de (cx, cy). */
  const brasas = (enx, cx, cy, larg, pal) => enx.soltar(1, () => ({ x: cx + Math.round(FX.aleatorio(-larg, larg)), y: cy,
    vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.6, -0.8), vida: Math.round(FX.aleatorio(12, 22)), desenho: Math.random() < 0.3 ? "cruz" : "brasa", pal }));

  /** O golpe: o clarão, os anéis, as linhas de velocidade. `t` desde o impacto. */
  function golpe(p, { cx, cy, r, t, pal, forte = true }) {
    if (t < 0) return;
    if (forte && t < 140) FX.clarao(p, t < 70 ? 11 : 5, "W");
    const r1 = r + FX.rampa(t, 0, 520) * p.t(forte ? 620 : 380);
    if (t < 560) FX.anel(p, { cx, cy, r: r1, esp: 3, pal: ["W", pal[1], pal[2]], achata: 0.62, rastro: 6, vis: Math.round(16 * (1 - t / 560)) });
    if (forte && t > 110 && t < 700) { const r2 = r + FX.rampa(t, 110, 520) * p.t(440);
      FX.anel(p, { cx, cy, r: r2, esp: 2, pal: [pal[1], pal[2], pal[3]], achata: 0.62, rastro: 4, vis: Math.round(16 * (1 - (t - 110) / 590)) }); }
    if (t < 480) {
      const r0 = r * 1.15 + FX.rampa(t, 0, 480) * p.t(260);
      FX.raios(p, { cx, cy, n: 40, ang: 0.07, larg: 0.05, r0, r1: r0 + p.t(90), pal: ["W", "W", pal[1], pal[2]], esbate: 0.5, fio: false, vis: Math.round(16 * (1 - t / 480)), achata: 0.75 });
    }
  }

  /** Depois do golpe, o laço: um pulso de choque fino a cada 1,6 s, saindo da estrela. */
  function pulso(p, { cx, cy, r, t, pal }) {
    const tp = t % 1600;
    if (t < 1000 || tp > 420) return;
    FX.anel(p, { cx, cy, r: r + Math.round((tp / 420) * p.t(150)), esp: 2, pal: [pal[1], pal[2], pal[3]], achata: 0.62, rastro: 3, vis: Math.round(13 * (1 - tp / 420)) });
  }

  function festa({ classe, fita, palavra, numero, longo, corpo, pal, som }) {
    const html = `<div class="festa fb ${classe}">
      <div class="fb-impacto">
        <div class="fb-numero">${palavra ? `<small>${palavra}</small>` : ""}<b class="${longo ? "longo" : ""}">${numero}</b></div>
        <div class="fb-fita"><span>${fita}</span></div>
      </div>
      <div class="fb-corpo">${corpo}<button class="continuar" type="button">Continuar <span>▸</span></button></div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), alvo = el.querySelector(".fb-impacto");
      const fichas = [...el.querySelectorAll(".fb-ficha")];
      App.som(som);
      FX.tremer(10);
      const ctl = FX.animar(p, (t, q, parado) => {
        const baixa = innerHeight < 760, c = p.de(alvo), re = p.t((longo ? 165 : 138) * (baixa ? 0.8 : 1)), ri = Math.round(re * 0.7);
        const resp = parado ? 0 : (q >> 1) % 2;
        // a aura atrás da estrela, os raios curtos e a estrela
        FX.raios(p, { cx: c.x, cy: c.y, n: 16, ang: 0.2 + (parado ? 0 : q * 0.012), larg: 0.32, r0: ri, r1: re * 1.55, pal: pal.slice(1), esbate: 0.35, achata: 0.82 });
        FX.estrela(p, { cx: c.x, cy: c.y, pontas: 14, ri: ri + resp, re: re + resp, ang: parado ? 0 : Math.sin(q / 5) * 0.03, pal });
        if (parado) return;
        golpe(p, { cx: c.x, cy: c.y, r: re, t, pal });
        pulso(p, { cx: c.x, cy: c.y, r: re, t, pal });
        if (q === 1) estilhacos(enx, c.x, c.y, re * 0.8, 40, ["W", "Y", pal[2], "o", "r", "D"]);
        fichas.forEach((f, i) => { if (q === 3 + i) { const b = p.de(f); enx.soltar(6, (k) => ({ x: b.x + (k % 2 ? b.rx : -b.rx), y: b.y + (k < 2 ? -b.ry : k < 4 ? 0 : b.ry),
          vx: (k % 2 ? 1 : -1) * FX.aleatorio(0.8, 2), vy: FX.aleatorio(-1.5, 0.5), arrasto: 0.85, vida: 8, desenho: "ponto", pal: ["W", "Y", pal[2]] })); } });
        if (q > 8 && q % 2 === 0) brasas(enx, c.x, c.y + Math.round(re * 0.6), re, ["Y", "O", "o", "r", "D"]);
        if (q > 10 && q % 7 === 0) { const a = FX.aleatorio(0, Math.PI * 2); enx.soltar(1, () => ({ x: c.x + Math.cos(a) * re, y: c.y + Math.sin(a) * re, vx: 0, vy: 0, vida: 7, desenho: "brilho", pal: ["W", "Y", pal[2]] })); }
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(700); el.classList.add("pulou"); } };
    };
    return { html, efeito };
  }

  function corpoNivel(d) {
    const g = ganhos(d).map((x, i) => `<span class="fb-ficha" style="--i:${i}">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("");
    const habs = habilidades(d.habilidades).map((x) => `<div class="fb-hab"><span class="fb-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join("");
    return `<div class="fb-ganhos">${g}</div>
      <div class="fb-linha"><div class="fb-talento">${talento(32)}<b>+1</b><span>ponto de talento<small>Talentos (T)</small></span></div></div>${habs}
      ${d.especializacao ? '<div class="fb-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}`;
  }

  const direcao = {
    nome: "estouro",
    nivel: (d) => festa({ classe: "fb-nivel", fita: "Você subiu de nível!", palavra: "Nível", numero: d.nivel, corpo: corpoNivel(d), pal: P.ouro, som: "subir" }),
    sigilo: (d) => festa({ classe: "fb-sigilo", fita: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, som: "fanfarra",
      corpo: `<div class="fb-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>
        <div class="fb-texto">Uma runa ardente se grava na sua mão.</div>
        <div class="fb-linha"><div class="fb-talento">${talento(32)}<b>+1</b><span>ponto de talento<small>Talentos (T)</small></span></div></div>` }),
    spec: (d) => festa({ classe: "fb-spec", fita: "Você agora é", palavra: "", numero: h(d.nome), longo: true, pal: P.arcano, som: "fanfarra",
      corpo: `<div class="fb-texto">${h(d.desc)}</div>${habilidades(d.habilidades).map((x) => `<div class="fb-hab"><span class="fb-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join("")}` }),

    achado(d) {
      const it = d.item, rar = h(it.raridade);
      return `<div class="tela achado fb-achado rar-${rar}">
        <div class="achado-cartao novo rar-${rar}">
          <div class="fb-palco-item"><div class="achado-arte">${arteItem(it, 64)}</div>
            <div class="fb-fita fb-fita-item rar-${rar}"><span>${RARIDADE[it.raridade] || rar}</span></div></div>
          <div class="fb-carta"><span class="achado-selo">Você encontrou</span>${textoItem(it)}${aviso(d)}</div>
        </div>
        <div class="fb-usa">${equipados(d)}</div></div>`;
    },
    GOLPE: {
      comum: null,
      magico: { pal: P.magico, coluna: 0, tremor: 0, cacos: 12, forte: false, estrela: 0.62 },
      raro: { pal: P.raro, coluna: 4, tremor: 4, cacos: 22, forte: false, estrela: 0.85 },
      lendario: { pal: P.lendario, coluna: 7, tremor: 11, cacos: 46, forte: true, estrela: 1.1 },
    },
    async cerimonia({ fundo, janela, d, parado, esperar, adiantou }) {
      const rar = d.item.raridade, cfg = direcao.GOLPE[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte");
      const queda = cfg && cfg.coluna && !parado && !FX.reduzido() ? 160 : 0;  // a coluna leva 160 ms para cair; o impacto é aí
      fundo.classList.add("entrando");
      if (FX.reduzido() || parado) fundo.classList.add("bateu");  // sem a queda da coluna: o item já está lá
      if (!parado && !queda) App.som(rar === "comum" ? "achado" : "achado_raro");
      let bateu = !queda;
      FX.animar(p, (t, q, quieto) => {
        const a = p.de(arte), R = Math.round(a.rx * 0.95), ti = t - queda;
        if (!quieto && !bateu && (ti >= 0 || adiantou())) {
          bateu = true; App.som("achado_raro"); FX.tremer(cfg.tremor); fundo.classList.add("bateu");
        }
        if (!cfg) {  // comum: a poeira
          if (!quieto && q === 1) enx.soltar(14, (i) => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + R, vx: (i % 2 ? 1 : -1) * FX.aleatorio(0.5, 2.2), vy: FX.aleatorio(-1.6, -0.3),
            g: 0.12, arrasto: 0.92, vida: Math.round(FX.aleatorio(10, 18)), desenho: i % 3 ? "ponto" : "duplo", pal: ["w", "G", "g", "d"] }));
          FX.halo(p, { cx: a.x, cy: a.y, r: R + 6, pal: ["G", "g", "d"], vis: 6 });
        } else {
          const re = Math.round(R * 1.45 * cfg.estrela + 6), aberto = quieto || bateu ? 1 : 0;
          if (aberto) {
            const resp = quieto ? 0 : (q >> 1) % 2;
            FX.raios(p, { cx: a.x, cy: a.y, n: 16, ang: 0.2 + (quieto ? 0 : q * 0.012), larg: 0.3, r0: Math.round(re * 0.7), r1: Math.round(re * (rar === "lendario" ? 2.4 : 1.7)), pal: cfg.pal.slice(1), esbate: 0.3, achata: 0.85 });
            FX.estrela(p, { cx: a.x, cy: a.y, pontas: rar === "magico" ? 10 : 14, ri: Math.round(re * 0.72) + resp, re: re + resp, pal: cfg.pal });
          }
          if (!quieto) {
            if (cfg.coluna && ti < 0) {  // a coluna caindo
              const base = Math.round(a.y * FX.rampa(t, 0, queda));
              FX.coluna(p, { cx: a.x, base, larg: cfg.coluna, pal: ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]], q });
            } else if (cfg.coluna && ti < 600) FX.coluna(p, { cx: a.x, base: a.y, larg: Math.max(1, Math.round(cfg.coluna * (1 - ti / 600))), pal: ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]], q, vis: Math.round(16 * (1 - ti / 600)) });
            if (bateu) {
              golpe(p, { cx: a.x, cy: a.y, r: re, t: ti < 0 ? 0 : ti, pal: cfg.pal, forte: cfg.forte });
              if (rar !== "magico") pulso(p, { cx: a.x, cy: a.y, r: re, t: ti, pal: cfg.pal });
              if (Math.round((ti < 0 ? 0 : ti) / FX.QUADRO) === 1) estilhacos(enx, a.x, a.y, re * 0.7, cfg.cacos, ["W", "Y", cfg.pal[2], cfg.pal[3], cfg.pal[4]], cfg.forte ? 1.2 : 0.8);
              if (rar === "lendario" && q % 2 === 0) brasas(enx, a.x, a.y + re, re * 1.4, ["Y", "O", "o", "r", "D"]);
              if (q % 8 === 0) { const g = FX.aleatorio(0, Math.PI * 2); enx.soltar(1, () => ({ x: a.x + Math.cos(g) * re, y: a.y + Math.sin(g) * re, vx: 0, vy: 0, vida: 7, desenho: "brilho", pal: ["W", cfg.pal[1], cfg.pal[2]] })); }
            }
          }
        }
        if (!quieto) { enx.passo(); enx.desenhar(p); }
      });
      if (parado) return;
      await esperar({ comum: 200, magico: 280, raro: 420, lendario: 560 }[rar] || 300);
    },
  };

  const PRETO = "#0d0b0a";
  const contorno = (px, c = PRETO) => `${px}px 0 ${c}, -${px}px 0 ${c}, 0 ${px}px ${c}, 0 -${px}px ${c}, ${px}px ${px}px ${c}, -${px}px ${px}px ${c}, ${px}px -${px}px ${c}, -${px}px -${px}px ${c}`;
  const css = `
  /* ---- B: Estouro ---- */
  #celebracao.dir-estouro { background: rgba(6, 3, 2, 0.94); }
  .festa.fb { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; width: min(760px, 94vw);
    background: none; border: 0; box-shadow: none; padding: 0; text-align: center; }
  .fb-impacto { position: relative; width: 420px; height: 300px; display: grid; place-items: center; margin-bottom: 18px; }
  .fb-numero { display: flex; flex-direction: column; align-items: center; animation: fb-bate 0.27s steps(1) both; }
  .fb-numero small { font: 26px/1 var(--titulo); color: #2a2420; text-shadow: none; margin-bottom: -2px; }
  .fb-numero b { font: 112px/0.86 var(--titulo); color: #fff; text-shadow: ${contorno(4, "#6e0d0d")}, 0 8px 0 #2a0a0a; }
  .fb-numero b.longo { font-size: 44px; line-height: 1; max-width: 300px; }
  .fb-sigilo .fb-numero b { font-size: 76px; }
  .fb-spec .fb-fita { top: 10px; bottom: auto; }  /* "você agora é" vem antes do nome */
  @keyframes fb-bate { 0% { scale: 2.3; } 25% { scale: 0.84; } 50% { scale: 1.1; } 75%, 100% { scale: 1; } }
  .fb-fita { position: absolute; left: 50%; bottom: 6px; translate: -50% 0; rotate: -4deg; white-space: nowrap; animation: fb-fita 0.2s 0.07s steps(3) both; }
  .fb-fita span { display: inline-block; padding: 8px 26px 7px; font: 700 20px/1 var(--texto); letter-spacing: 0.16em; text-transform: uppercase; color: #fff3a0;
    background: #b3262b; border: 3px solid #6e0d0d; box-shadow: 0 0 0 3px #0d0b0a, inset 0 3px 0 #e2574c, 0 7px 0 #000; text-shadow: 2px 2px 0 #4a0808; }
  @keyframes fb-fita { from { clip-path: inset(0 50% 0 50%); } to { clip-path: inset(0 0 0 0); } }
  .fb-corpo { display: flex; flex-direction: column; align-items: center; gap: 10px; width: 100%; }
  .fb-ganhos { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
  .fb-ficha { display: grid; grid-template-columns: auto auto; align-items: center; column-gap: 6px; padding: 6px 12px 5px 10px; min-width: 92px;
    background: ${PRETO}; border: 3px solid #f2c94c; box-shadow: 0 0 0 3px #000, inset 0 3px 0 #3a2c0c, 0 7px 0 #000;
    animation: fb-ficha 0.2s calc(0.2s + var(--i) * 0.067s) steps(1) both; }
  .fb-ficha img { grid-row: span 2; }
  .fb-ficha b { font: 34px/1 var(--titulo); color: #8fbf6a; text-shadow: ${contorno(2)}; text-align: left; }
  .fb-ficha > span { font: 700 11px/1 var(--texto); letter-spacing: 0.14em; text-transform: uppercase; color: #f1e4c4; text-align: left; }
  @keyframes fb-ficha { 0% { scale: 1.35; } 34% { scale: 0.92; } 67%, 100% { scale: 1; } }
  .fb-linha { display: flex; justify-content: center; }
  .fb-talento { display: inline-flex; align-items: center; gap: 10px; padding: 6px 16px 6px 10px; background: #2a1d06; border: 3px solid #f2c94c;
    box-shadow: 0 0 0 3px #000, inset 0 3px 0 #5a420e, 0 7px 0 #000; }
  .fb-talento b { font: 34px/1 var(--titulo); color: #fff3a0; text-shadow: ${contorno(2)}; }
  .fb-talento span { display: flex; flex-direction: column; align-items: flex-start; font: 700 18px/1.1 var(--texto); color: #fff3a0; }
  .fb-talento small { font: 12px/1.2 var(--texto); color: #c0b8a8; }
  .fb-hab { max-width: 600px; padding: 8px 16px 10px; text-align: left; background: #120c1a; border: 3px solid #8e6fd8; box-shadow: 0 0 0 3px #000, inset 0 3px 0 #2a1d3a, 0 7px 0 #000; }
  .fb-hab b { display: block; font: 30px/1.05 var(--titulo); color: #e4d8ff; text-shadow: ${contorno(2)}; }
  .fb-hab > div { font: 16px/1.35 var(--texto); color: #f1e4c4; }
  .fb-rotulo { font: 700 12px/1 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #c8b0ff; }
  .fb-aviso, .fb-texto { max-width: 600px; font: 17px/1.4 var(--texto); color: #f1e4c4; text-shadow: 2px 2px 0 #000; }
  .fb-aviso { color: #c8b0ff; font-style: italic; }
  .fb-losangos { display: flex; justify-content: center; gap: 14px; }
  .fb-losangos i { width: 20px; height: 20px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; box-shadow: 0 0 0 3px #000; }
  .fb-losangos i.tem { background: #e2574c; border-color: #fff3a0; }
  .festa.fb .continuar { margin-top: 6px; }
  .fb.pulou :is(.fb-numero, .fb-fita, .fb-ficha) { animation: none; }

  /* o achado */
  :root body #sobre-achado.dir-estouro { background: rgba(6, 3, 2, 0.9); }
  :root body #sobre-achado.dir-estouro .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0; max-height: none; overflow: visible; }
  :root body #sobre-achado .fb-achado.tela.achado { display: flex; align-items: flex-end; justify-content: center; gap: 18px; }
  :root body #sobre-achado .fb-achado .achado-cartao.novo { display: flex; flex-direction: column; align-items: center; width: 340px; background: none; border: 0;
    box-shadow: none; padding: 0; overflow: visible; animation: none; }
  .fb-palco-item { position: relative; height: 236px; width: 100%; display: grid; place-items: center; }
  .fb-palco-item .achado-arte img, .fb-palco-item .achado-arte canvas { width: 128px !important; height: 128px !important; image-rendering: pixelated; }
  .fb-fita-item { bottom: 0; animation-delay: 0.05s; }
  .fb-fita-item span { font-size: 18px; padding: 7px 22px 6px; }
  .fb-fita-item.rar-comum span { background: #4a4038; border-color: #2a2420; box-shadow: 0 0 0 3px #0d0b0a, inset 0 3px 0 #8a8070, 0 7px 0 #000; color: #f1e4c4; text-shadow: 2px 2px 0 #000; }
  .fb-fita-item.rar-magico span { background: #3d63c9; border-color: #1c2a6b; box-shadow: 0 0 0 3px #0d0b0a, inset 0 3px 0 #7fb0ff, 0 7px 0 #000; color: #fff; text-shadow: 2px 2px 0 #1c2a6b; }
  .fb-fita-item.rar-raro span { background: #d4af37; border-color: #8a6a14; box-shadow: 0 0 0 3px #0d0b0a, inset 0 3px 0 #fff3a0, 0 7px 0 #000; color: #2a1d06; text-shadow: none; }
  .fb-fita-item.rar-lendario span { background: #e0782f; border-color: #6e0d0d; box-shadow: 0 0 0 3px #0d0b0a, inset 0 3px 0 #ffb35c, 0 7px 0 #000; color: #fff3a0; text-shadow: 2px 2px 0 #6e0d0d; }
  :root body #sobre-achado :is(.fb-carta, .fb-usa .achado-cartao) { box-sizing: border-box; width: 100%; padding: 12px 16px 14px; text-align: center; overflow: visible;
    background: ${PRETO}; border: 3px solid #8a8070; box-shadow: 0 0 0 3px #000, inset 0 3px 0 #2a2420, 0 8px 0 #000; border-image: none; animation: none; }
  :root body #sobre-achado.dir-estouro.rar-magico .fb-carta { border-color: #7fb0ff; }
  :root body #sobre-achado.dir-estouro.rar-raro .fb-carta { border-color: #f2c94c; }
  :root body #sobre-achado.dir-estouro.rar-lendario .fb-carta { border-color: #ffb35c; box-shadow: 0 0 0 3px #000, 0 0 0 6px #b3262b, inset 0 3px 0 #2a2420, 0 10px 0 #000; }
  .fb-carta .achado-selo { display: block; font: 700 12px/1 var(--texto); letter-spacing: 0.28em; text-transform: uppercase; color: #c0b8a8; margin-bottom: 6px; }
  .fb-usa { width: 260px; } .fb-usa:empty { display: none; }
  .fb-usa .achado-aneis { display: flex; flex-direction: column; gap: 10px; }
  .dir-estouro .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 18px; }
  /* a entrada: com coluna, o item só aparece quando ela bate; o resto (o texto) já está lá */
  :root body #sobre-achado.dir-estouro.entrando:is(.rar-raro, .rar-lendario):not(.bateu):not(.adiantado) .fb-palco-item > * { visibility: hidden; }
  .dir-estouro.bateu .fb-palco-item .achado-arte, .dir-estouro.entrando:is(.rar-comum, .rar-magico) .fb-palco-item .achado-arte { animation: fb-bate 0.27s steps(1) both; }
  @media (max-height: 760px) {
    .fb-impacto { width: 340px; height: 226px; margin-bottom: 10px; } .fb-numero b { font-size: 84px; } .fb-numero b.longo { font-size: 36px; }
    .fb-fita span { font-size: 16px; padding: 6px 20px 5px; } .fb-corpo { gap: 7px; }
    .fb-hab { padding: 6px 12px 7px; } .fb-hab b { font-size: 24px; } .fb-ficha b { font-size: 28px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fb :is(.fb-numero, .fb-fita, .fb-ficha), .dir-estouro .fb-palco-item .achado-arte, .dir-estouro .fb-fita { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-estouro">${css}</style>`);
  Festa.usar(direcao);
})();

/* Item achado: a janela do saque, por cima do jogo e fora do log, com o feixe na cor da raridade antes do cartão
   (raro e lendário). */
"use strict";

(() => {
  const { h, S, faiscas, htmlItem, iconeItem, noPalco, VAZIO } = Telas;

  const BRILHO_RARIDADE = { comum: ["#f1e4c4", "#c0b8a8"], magico: ["#7fb0ff", "#c8e0ff", "#ffffff"],
    raro: ["#f2c94c", "#fff3a0", "#ffffff"], lendario: ["#ffb35c", "#e0782f", "#fff3a0", "#ffffff"] };
  /** O desenho de um item no cartão: o da interface (Icones), ou o sprite do jogo, no mesmo tamanho. */
  const arte = (sprite, escala) => Icones.porDesenho(sprite, 16 * escala) || S(sprite, escala);
  /** Item encontrado: o cartão dele (sprite, raridade, bônus, diferença para o seu) e, ao lado, o que você usa. */
  function achado(d) {
    const it = d.item;
    const rar = h(it.raridade);
    // O anel: os dois espaços empilhados numa coluna ao lado do achado, cada um com o nome do espaço e o anel que está
    // nele (ou vazio), em cartões baixos: três cartões lado a lado não cabiam e o terceiro quebrava de linha.
    const aneis = d.espacos && (d.equipados || []).length;
    const eq = aneis ? `<div class="achado-aneis">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arte(iconeItem(e.item), 3)}</div><div>${htmlItem(e.item, "", false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || S(VAZIO[e.espaco], 3, "fantasma")}</div></div></div>`).join("")}</div>`
      : (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arte(iconeItem(e), 3)}</div>${htmlItem(e, "", false)}</div>`).join("");
    // Mochila cheia: o que sai do corpo fica para trás (o anel que vai para o espaço vazio não tira nada).
    const aviso = !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
    return `<div class="tela achado rar-${rar}">
      <div class="achado-cartao novo rar-${rar}">
        <div class="achado-raios" aria-hidden="true"></div>
        <span class="achado-selo">Você encontrou</span>
        <div class="achado-arte">${arte(iconeItem(it), 4)}</div>
        ${htmlItem(it)}${aviso}
      </div>${eq}</div>`;
  }
  /** O item achado abre numa janela própria, por cima do jogo e fora do log. Como nos ARPGs, o achado é a estrela:
   *  primeiro ele sozinho, no meio da janela (raro e lendário: o feixe de luz cai ali antes); depois ele abre espaço,
   *  o que você usa entra ao lado com a comparação e aparecem os botões (que vêm da pergunta do motor, ver
   *  escolhas.js). A janela já nasce no tamanho final: nada pula, o cartão só começa deslocado para o meio. Ela fecha
   *  quando o ícone pousa (no corpo ou na mochila), ou ao deixar o item. */
  async function abrirAchado(d, semCerimonia = false) {
    fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = "sobreposicao";
    // Os botões chegam com a pergunta, depois da revelação; até lá, os mesmos rótulos (que vêm com o cartão) guardam o
    // lugar deles, invisíveis: a moldura já nasce no tamanho final e não cresce quando eles chegam.
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild, tela = janela.querySelector(".tela.achado");
    const novo = tela.querySelector(".achado-cartao.novo");
    noPalco(janela);
    if (semCerimonia) return;
    janela.classList.add("so-o-achado");
    const j = janela.getBoundingClientRect(), c = novo.getBoundingClientRect();
    const desvio = Math.round(j.left + j.width / 2 - (c.left + c.width / 2));  // do lugar dele até o meio da janela
    novo.style.translate = `${desvio}px 0`;
    tela.classList.add("esperando-feixe");
    await Sensacao.cerimoniaSaque(d.item.raridade, novo);
    tela.classList.remove("esperando-feixe");
    revelarAchado(tela, d);
    // Um instante só com o achado; então ele vai para o lado dele e a comparação entra.
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    await new Promise((r) => setTimeout(r, App.ritmo(raro ? 900 : 550)));
    if (!janela.isConnected) return;
    janela.classList.remove("so-o-achado");
    novo.style.translate = "";
    if (desvio) novo.animate([{ translate: `${desvio}px 0` }, { translate: "0 0" }], { duration: App.ritmo(380), easing: "cubic-bezier(.3,.7,.3,1)" });
  }
  /** Onde a pergunta "o que fazer com o item?" põe os botões (null se a janela não está aberta). */
  function acoesDoAchado() { return document.querySelector("#sobre-achado .achado-acoes"); }
  function fecharAchado() {
    const f = document.getElementById("sobre-achado");
    if (!f) return;
    f.id = "";  // a próxima janela (outro item logo em seguida) já pode abrir enquanto esta some
    f.classList.add("saindo");
    setTimeout(() => f.remove(), 220);
  }

  /** O cartão do item aparece de vez: o som da raridade e as faíscas (depois da cerimônia, se houve uma). */
  function revelarAchado(raiz, d) {
    const cartao = raiz.querySelector(".achado-cartao.novo");
    if (!cartao) return;
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    App.som(raro ? "achado_raro" : "achado");
    setTimeout(() => { if (cartao.isConnected) faiscas(cartao.querySelector(".achado-arte"), BRILHO_RARIDADE[d.item.raridade] || BRILHO_RARIDADE.comum, raro ? 22 : 12); }, 260);
  }

  Telas.registrar("achado", achado);

  Object.assign(Telas, { abrirAchado: Festa.abrirAchado, acoesDoAchado, fecharAchado, revelarAchado });  // PROTÓTIPO: a direção
})();
