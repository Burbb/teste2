/* PROTÓTIPO da etapa 2, segunda rodada, direção relicario2 (montado por auxiliares/montar_v2.py; nada no jogo). */
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

/* PROTÓTIPO, direção A2: RELICÁRIO REFINADO (24/10/2026). O sol de raios e a medalha da A, com o que o Jean pediu:
   - os itens no tamanho de uso do cartão do saque (o arquivo de 64 da produção, sem ampliar); o sol conduz o olhar;
   - a informação sem molduras repetidas: os raios passam por trás dela num poço escuro em pontilhado (o alto e o pé
     viram uma peça só), os ganhos alinhados numa linha (ícone, valor, nome), o ponto de talento na mesma composição com
     o atalho, a habilidade pelo ícone do Grimório, nome e descrição, e o Continuar dos botões do jogo;
   - a especialização com o nome como protagonista (o sol atrás do nome, sem a medalha);
   - o achado: o item, a raridade e o nome no alto; embaixo, numa composição só, o prêmio, a troca e o que você usa;
   - o comum entra sem aura (desce ao altar com um pouco de poeira e um brilho só); o mágico tem um brilho breve e
     localizado; raro, lendário e Sigilo continuam com o sol inteiro;
   - depois da entrada, o efeito continua vivo e um pouco mais baixo (os raios em pontilhado mais aberto), para ler. */
"use strict";

(() => {
  const { h, ganhos, talento, habilidades, continuar, fichaItem, arteItem } = Festa;
  const P = FX.PALETAS;
  const SUSTENTA = 1400;  // ms: depois da entrada, o sol baixa um pouco

  function medalha(p, cx, cy, R, pal) {
    const [, claro, meio, escuro, fundo] = pal.map(FX.cor);
    const k = FX.cor("k"), q = FX.cor("z"), Q = FX.cor("q");
    for (let y = cy - R - 1; y <= cy + R + 1; y++) for (let x = cx - R - 1; x <= cx + R + 1; x++) {
      const dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy);
      if (d > R + 0.5) continue;
      if (d > R - 0.7) { p.por(x, y, k); continue; }
      const luz = (-dx - dy) / (d || 1);
      if (d > R - 3.5) p.por(x, y, luz > 0.45 ? claro : luz < -0.45 ? escuro : meio);
      else if (d > R - 4.5) p.por(x, y, luz > 0 ? fundo : k);
      else p.por(x, y, Sprites.pontilha(x, y, d < R * 0.55 ? 3 : 1) ? Q : q);
    }
  }
  const ALCANCE = (a) => 1 - 0.35 * Math.max(0, Math.sin(a));
  /** O sol: os raios largos e os finos girando ao contrário; `vis` baixa na sustentação. */
  function sol(p, { cx, cy, R, r1, ang, n = 14, pal, fino = true, vis = 16 }) {
    FX.raios(p, { cx, cy, n, ang, larg: 0.4, r0: R, r1, pal: pal.slice(1), esbate: 0.4, vis, alterna: 0.68, alcance: ALCANCE });
    if (fino) FX.raios(p, { cx, cy, n: n * 2, ang: -ang * 1.7 + 0.11, larg: 0.09, r0: R, r1: R + (r1 - R) * 0.78, pal, esbate: 0.3, fio: false, vis: Math.min(vis, 14), alcance: ALCANCE });
  }
  const vivo = (t, parado) => (parado ? 12 : Math.round(FX.rampa(t, SUSTENTA, 900, 16, 12)));
  function faiscas(enx, cx, cy, R, n, pal) {
    enx.soltar(n, (i) => {
      const a = (i / n) * Math.PI * 2 + FX.aleatorio(-0.2, 0.2), v = FX.aleatorio(2.2, 4.2);
      return { x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R, vx: Math.cos(a) * v, vy: Math.sin(a) * v, arrasto: 0.86,
        vida: Math.round(FX.aleatorio(9, 16)), desenho: i % 4 ? "cruz" : "brilho", pal };
    });
  }
  function cintilar(enx, cx, cy, R, r1, pal) {
    const a = FX.aleatorio(0, Math.PI * 2), d = FX.aleatorio(R * 1.4, r1 * 0.8);
    enx.soltar(1, () => ({ x: cx + Math.cos(a) * d, y: cy + Math.sin(a) * d, vx: 0, vy: 0, vida: 9, desenho: Math.random() < 0.5 ? "brilho" : "estrela", pal }));
  }
  /** O poço escuro atrás da informação: os raios passam por trás dela, apagados. */
  function poco(p, el, folga = 90, forca = 16) {
    if (!el) return;
    const i = p.de(el);
    FX.poco(p, { cx: i.x, cy: i.y, rx: i.rx + p.t(folga), ry: i.ry + p.t(folga * 0.6), forca });
  }

  /** A festa: no alto, o que celebra (a medalha, ou o nome na especialização) no sol; embaixo, a informação. */
  function festa({ classe, sobre, palavra, numero, titulo, info, pal, som }) {
    const alto = titulo
      ? `<div class="fa2-coroa fa2-centro"><span class="fa2-sobre">${sobre}</span><b class="fa2-titulo">${titulo}</b></div>`
      : `<div class="fa2-coroa"><span class="fa2-sobre">${sobre}</span>
          <div class="fa2-medalha fa2-centro">${palavra ? `<span class="fa2-palavra">${palavra}</span>` : ""}<span class="fa2-numero">${numero}</span></div></div>`;
    const html = `<div class="festa fa2 ${classe}">${alto}<div class="fa2-info"><i class="fa2-fio"></i>${info}${continuar()}</div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), centro = el.querySelector(".fa2-centro"), inf = el.querySelector(".fa2-info");
      App.som(som);
      const ctl = FX.animar(p, (t, q, parado) => {
        const m = p.de(centro), R = titulo ? Math.round(Math.min(m.rx, m.ry) * 0.5) : Math.round(m.rx * 0.92);
        const r1 = Math.max(R + 10, p.t(Math.min(innerHeight * 0.7, 600))), abre = parado ? 1 : FX.rampa(t, 0, 520);
        sol(p, { cx: m.x, cy: m.y, R, r1: R + (r1 - R) * abre, ang: parado ? 0.12 : q * 0.035, pal, vis: vivo(t, parado) });
        if (!parado && t < 330) FX.halo(p, { cx: m.x, cy: m.y, r: R * (2.6 - (t / 330) * 1.2), pal: ["W", "W", "Y", pal[1]], vis: Math.round(16 * (1 - t / 330)) });
        poco(p, inf);
        poco(p, el.querySelector(".fa2-sobre"), 50, 16);  // o rótulo de cima, legível sobre os raios
        if (!titulo) medalha(p, m.x, m.y, R, pal);
        if (parado) return;
        if (q === 1) faiscas(enx, m.x, m.y, R, 18, ["W", "Y", pal[2], pal[3]]);
        if (q > 10 && q % 5 === 0) cintilar(enx, m.x, m.y, R, r1, ["W", "Y", pal[2]]);
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(520); el.classList.add("pulou"); } };
    };
    return { html, efeito };
  }

  const linhaGanhos = (d) => `<div class="fa2-ganhos">${ganhos(d).map((x) => `<span class="fa2-ganho">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("")}</div>`;
  const linhaTalento = () => `<div class="fa2-talento">${talento(32)}<b>+1</b><span>ponto de talento</span><kbd>T</kbd></div>`;
  const blocoHabs = (lista) => habilidades(lista).map((x) => `<div class="fa2-hab"><span class="fa2-hab-icone">${x.icone}</span>
    <div><span class="fa2-rotulo">nova habilidade</span><b>${x.nome}</b><p>${x.desc}</p></div></div>`).join("");

  const direcao = {
    nome: "relicario2",
    nivel: (d) => festa({ classe: "fa2-nivel", sobre: "você subiu de nível", palavra: "Nível", numero: d.nivel, pal: P.ouro, som: "subir",
      info: `${linhaGanhos(d)}${linhaTalento()}${blocoHabs(d.habilidades)}
        ${d.especializacao ? '<p class="fa2-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</p>' : ""}` }),
    sigilo: (d) => festa({ classe: "fa2-sigilo", sobre: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, som: "fanfarra",
      info: `<div class="fa2-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>
        <p class="fa2-texto">Uma runa ardente se grava na sua mão.</p>${linhaTalento()}` }),
    spec: (d) => festa({ classe: "fa2-spec", sobre: "você agora é", titulo: h(d.nome), pal: P.arcano, som: "fanfarra",
      info: `<p class="fa2-texto">${h(d.desc)}</p>${blocoHabs(d.habilidades)}` }),

    achado(d) {
      const f = fichaItem(d);
      return `<div class="tela achado fa2-achado rar-${f.rar}">
        <div class="achado-cartao novo rar-${f.rar}">
          <div class="fa2-altar"><div class="achado-arte">${arteItem(d.item, 64)}</div></div>
          <div class="fa2-cabeca"><span class="achado-selo">Você encontrou</span>${f.raridade}${f.nome}</div>
        </div>
        <div class="fa2-ficha${f.compara ? " compara" : ""}">${f.premio}${f.troca}${f.usa ? `<div class="fa2-usa">${f.usa}</div>` : ""}</div>
        ${f.lore}${f.aviso}</div>`;
    },
    SOL: {
      raro: { n: 12, raio: 260, pal: P.raro, fino: true, faiscas: 14 },
      lendario: { n: 14, raio: 380, pal: P.lendario, fino: true, faiscas: 26, clarao: true, brasas: true },
    },
    async cerimonia({ fundo, janela, d, parado, esperar }) {
      const rar = d.item.raridade, cfg = direcao.SOL[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte"), ficha = janela.querySelector(".fa2-ficha"), cabeca = janela.querySelector(".fa2-cabeca");
      if (!parado) App.som(["raro", "lendario"].includes(rar) ? "achado_raro" : "achado");
      fundo.classList.add("entrando");
      const brasa = ["Y", "O", "o", "r", "D"];
      FX.animar(p, (t, q, quieto) => {
        const a = p.de(arte), R = Math.round(a.rx * 1.05);
        if (cfg) {
          const abre = quieto ? 1 : FX.rampa(t, 60, 520), r1 = p.t(cfg.raio);
          sol(p, { cx: a.x, cy: a.y, R: R + 2, r1: R + 2 + (r1 - R) * abre, ang: quieto ? 0.1 : q * (rar === "lendario" ? 0.04 : 0.03), n: cfg.n, pal: cfg.pal, fino: cfg.fino, vis: vivo(t, quieto) });
          poco(p, ficha);
          poco(p, cabeca, 60, 15);
        }
        if (quieto) return;
        if (cfg) {
          if (cfg.clarao && t < 200) FX.clarao(p, Math.round(9 * (1 - t / 200)), "Y");
          if (q === 2) faiscas(enx, a.x, a.y, R, cfg.faiscas, ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]]);
          if (q > 10 && q % 6 === 0) cintilar(enx, a.x, a.y, R, p.t(cfg.raio), ["W", cfg.pal[1], cfg.pal[2]]);
          if (cfg.brasas && q % 2 === 0) enx.soltar(1, () => ({ x: a.x + Math.round(FX.aleatorio(-R * 3, R * 3)), y: a.y + R + Math.round(FX.aleatorio(0, 10)),
            vx: FX.aleatorio(-0.2, 0.2), vy: FX.aleatorio(-1.1, -0.6), vida: Math.round(FX.aleatorio(14, 24)), desenho: "brasa", pal: brasa }));
        } else if (rar === "magico") {
          // um brilho breve, só em volta do item: um anel curto, raios que piscam e somem, sem nada que fique
          if (t < 640) {
            FX.raios(p, { cx: a.x, cy: a.y, n: 8, ang: 0.2, larg: 0.18, r0: R + 1, r1: R + 2 + Math.round(FX.rampa(t, 0, 300) * p.t(46)), pal: P.magico.slice(1), esbate: 0.3, vis: Math.round(16 * (1 - FX.rampa(t, 260, 380))) });
            FX.anel(p, { cx: a.x, cy: a.y, r: R + Math.round(FX.rampa(t, 0, 420) * p.t(40)), esp: 1, pal: ["W", "M", "U"], rastro: 2, vis: Math.round(14 * (1 - t / 640)) });
          }
          if (q === 3) faiscas(enx, a.x, a.y, R, 6, ["W", "M", "U", "u"]);
        } else if (q === 3) {
          // comum: o item pousa e levanta um pouco de poeira; um brilho só no metal, e mais nada
          enx.soltar(10, (i) => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + R - 1, vx: (i % 2 ? 1 : -1) * FX.aleatorio(0.4, 1.6), vy: FX.aleatorio(-0.9, -0.2),
            g: 0.08, arrasto: 0.9, vida: Math.round(FX.aleatorio(8, 13)), desenho: "ponto", pal: ["G", "g", "d"] }));
          enx.soltar(1, () => ({ x: a.x + Math.round(R * 0.4), y: a.y - Math.round(R * 0.4), vx: 0, vy: 0, vida: 6, desenho: "brilho", pal: ["W", "w", "G"] }));
        }
        enx.passo(); enx.desenhar(p);
      });
      if (parado) return;
      await esperar({ comum: 240, magico: 320, raro: 480, lendario: 620 }[rar] || 300);
    },
  };

  const PRETO = "#0d0b0a";
  const contorno = (px, c = PRETO) => [[px, 0], [-px, 0], [0, px], [0, -px], [px, px], [-px, px], [px, -px], [-px, -px]].map(([x, y]) => `${x}px ${y}px 0 ${c}`).join(", ");
  const css = `
  /* ---- A2: Relicário refinado ---- */
  #celebracao.dir-relicario2 { background: rgba(4, 3, 2, 0.9); }
  .festa.fa2 { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; width: min(920px, 96vw);
    background: none; border: 0; box-shadow: none; padding: 0; text-align: center; }
  .fa2-coroa { display: flex; flex-direction: column; align-items: center; gap: 22px; margin-bottom: 40px; }
  .fa2-sobre { font: 700 15px/1 var(--texto); letter-spacing: 0.34em; text-transform: uppercase; color: #fff3a0; text-shadow: ${contorno(2)}; }
  .fa2-medalha { width: 160px; height: 160px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .fa2-palavra { font: 22px/1 var(--titulo); color: #c0b8a8; text-shadow: 2px 2px 0 #000; margin-top: 6px; }
  .fa2-numero { font: 84px/0.9 var(--titulo); color: #ffe27a; text-shadow: ${contorno(3)}, 0 6px 0 #000; }
  .fa2-sigilo .fa2-numero { font-size: 54px; }
  .fa2-titulo { display: block; padding: 6px 18px; font: 400 92px/1 var(--titulo); color: #f1e4ff; text-shadow: ${contorno(4, "#1c0f2a")}, 0 8px 0 #000; }
  .fa2-spec .fa2-coroa { gap: 14px; margin: 40px 0 34px; }
  .fa2-info { display: flex; flex-direction: column; align-items: center; gap: 14px; width: 100%; }
  /* o fio de latão com o losango no meio: separa o alto da leitura sem moldura */
  .fa2-fio { position: relative; display: block; width: min(560px, 80%); height: 2px; background: #6b4b31; box-shadow: 0 1px 0 #000; }
  .fa2-fio::before { content: ""; position: absolute; left: 50%; top: -3px; width: 4px; height: 4px; translate: -2px 0;
    background: #f2c94c; box-shadow: -2px 2px 0 #d4af37, 2px 2px 0 #d4af37, 0 4px 0 #f2c94c, 0 2px 0 #8a6a14; }
  .fa2-ganhos { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px 0; }
  .fa2-ganho { display: inline-flex; align-items: center; gap: 6px; padding: 0 11px; }
  .fa2-ganho + .fa2-ganho { border-left: 1px solid #3a3128; }
  .fa2-ganho b { font: 30px/1 var(--titulo); color: #8fbf6a; text-shadow: 2px 2px 0 #000; }
  .fa2-ganho > span { font: 700 12px/1 var(--texto); letter-spacing: 0.16em; text-transform: uppercase; color: #c0b8a8; }
  .fa2-talento { display: inline-flex; align-items: center; gap: 9px; font: 20px/1 var(--texto); color: #f2d27a; text-shadow: 1px 1px 0 #000; }
  .fa2-talento b { font: 30px/1 var(--titulo); color: #fff3a0; text-shadow: 2px 2px 0 #000; }
  .fa2 kbd, .dir-relicario2 kbd { font: 13px/1 var(--num); color: #c0b8a8; border: 1px solid #4a4d53; background: #0b0c0e; padding: 2px 5px; margin-left: 4px; }
  .fa2-hab { display: flex; align-items: flex-start; gap: 14px; max-width: 620px; text-align: left; margin-top: 2px; }
  .fa2-hab-icone { flex: none; display: grid; place-items: center; width: 44px; height: 44px; margin-top: 4px; background: #120c1a; box-shadow: inset 0 0 0 1px #5a2a6e; }
  .fa2-hab b { display: block; font: 28px/1.05 var(--titulo); color: #e4d8ff; text-shadow: 2px 2px 0 #000; }
  .fa2-hab p { margin: 3px 0 0; font: 16px/1.4 var(--texto); color: #e8dcbe; }
  .fa2-rotulo { font: 700 11px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase; color: #8e6fd8; }
  .fa2-aviso { margin: 0; font: italic 16px/1.4 var(--texto); color: #c8b0ff; }
  .fa2-texto { margin: 0; max-width: 620px; font: 17px/1.45 var(--texto); color: #e8dcbe; }
  .fa2-losangos { display: flex; gap: 14px; } .fa2-losangos i { width: 16px; height: 16px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; }
  .fa2-losangos i.tem { background: #e2574c; border-color: #ffb35c; }
  :root body .fa2 .continuar { margin-top: 6px; display: inline-flex; align-items: center; gap: 6px; }
  .fa2 .fa2-medalha { animation: fa2-carimbo 0.27s steps(4) both; }
  @keyframes fa2-carimbo { from { scale: 1.45; } to { scale: 1; } }
  .fa2 .fa2-titulo { animation: fa2-carimbo 0.27s steps(4) both; }
  .fa2 .fa2-info { animation: fa2-sobe 0.2s 0.08s steps(3) both; }
  @keyframes fa2-sobe { from { translate: 0 16px; } to { translate: 0 0; } }
  .fa2.pulou :is(.fa2-medalha, .fa2-titulo, .fa2-info) { animation: none; }

  /* o achado: o item no tamanho do saque, a ficha numa peça só */
  :root body #sobre-achado.dir-relicario2 { background: rgba(4, 3, 2, 0.88); }
  :root body #sobre-achado.dir-relicario2 .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0;
    max-height: none; overflow: visible; width: min(900px, 96vw); }
  :root body #sobre-achado .fa2-achado.tela.achado { display: flex; flex-direction: column; align-items: center; gap: 12px; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo { display: flex; flex-direction: column; align-items: center; gap: 8px; width: auto;
    background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo .achado-arte { width: 64px; height: 64px; margin: 0; }
  .fa2-cabeca { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .fa2-altar { display: grid; place-items: center; height: 150px; }
  #sobre-achado.dir-relicario2:is(.rar-comum, .rar-magico) .fa2-altar { height: 84px; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo > .achado-selo { font: 700 13px/1 var(--texto); letter-spacing: 0.32em; text-transform: uppercase; color: #f2d27a; text-shadow: ${contorno(2)}; }
  .ficha-raridade { display: inline-flex; align-items: center; gap: 10px; font: 700 13px/1 var(--texto); letter-spacing: 0.26em; text-transform: uppercase; }
  .ficha-raridade::before, .ficha-raridade::after { content: ""; width: 34px; height: 2px; background: currentColor; box-shadow: 0 1px 0 #000; }
  .ficha-raridade.rar-comum { color: #c0b8a8; } .ficha-raridade.rar-magico { color: #7fb0ff; } .ficha-raridade.rar-raro { color: #f2c94c; } .ficha-raridade.rar-lendario { color: #ffb35c; }
  .ficha-nome { display: block; max-width: 820px; font: 400 40px/1.05 var(--titulo); text-shadow: ${contorno(2)}, 0 4px 0 #000; text-wrap: balance; }
  .ficha-nome.r-comum { color: #f1e4c4; }
  .fa2-ficha { display: grid; grid-template-columns: 1fr; justify-items: center; gap: 0 26px; padding-top: 12px; width: 100%; box-shadow: inset 0 2px 0 #2b2219; }
  .fa2-ficha.compara { grid-template-columns: 1fr auto 1fr; align-items: start; justify-items: stretch; }
  .ficha-premio, .fa2-ficha .ficha-troca, .fa2-usa { display: flex; flex-direction: column; gap: 3px; }
  .ficha-premio { align-items: center; } .fa2-ficha.compara .ficha-premio { align-items: flex-end; text-align: right; }
  .ficha-rotulo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .ficha-linhas { display: flex; flex-direction: column; font: 19px/1.25 var(--num, var(--texto)); color: #f1e4c4; }
  .ficha-linhas .efeito { color: #c8b0ff; font-size: 16px; }
  .fa2-ficha .ficha-troca { align-items: center; padding: 0 22px; border-left: 1px solid #3a3128; border-right: 1px solid #3a3128; font: 17px/1.3 var(--num, var(--texto)); }
  .ficha-troca .melhor { color: #8fbf6a; } .ficha-troca .pior { color: #e2574c; }
  :root body #sobre-achado .fa2-usa .achado-cartao.atual { width: auto; padding: 0; background: none; border: 0; box-shadow: none; text-align: left; overflow: visible; animation: none; opacity: 0.92; }
  .fa2-usa { gap: 10px; } .fa2-usa .achado-selo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .ficha-usa-nome { display: flex; align-items: center; gap: 8px; } .ficha-usa-nome b { font: 400 22px/1.05 var(--titulo); }
  .fa2-usa .ficha-linhas { font-size: 17px; } .fa2-usa .ficha-troca { border: 0; padding: 0; align-items: flex-start; font-size: 15px; }
  .ficha-lore { max-width: 620px; font: italic 15px/1.4 var(--texto); color: #a89878; }
  .dir-relicario2 .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 16px; }
  .dir-relicario2.entrando .fa2-altar .achado-arte { animation: fa2-desce 0.27s steps(4) both; }
  @keyframes fa2-desce { from { translate: 0 -40px; } 75% { translate: 0 3px; } to { translate: 0 0; } }
  .dir-relicario2.adiantado .fa2-altar .achado-arte { animation: none; }
  @media (max-height: 760px) {
    .fa2-coroa { gap: 14px; margin-bottom: 14px; } .fa2-medalha { width: 128px; height: 128px; } .fa2-numero { font-size: 64px; }
    .fa2-titulo { font-size: 70px; } .fa2-info { gap: 10px; } .fa2-hab b { font-size: 24px; } .fa2-hab p { font-size: 15px; }
    .fa2-altar { height: 112px; } .ficha-nome { font-size: 32px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fa2 :is(.fa2-medalha, .fa2-titulo, .fa2-info), .dir-relicario2 .fa2-altar .achado-arte { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-relicario2">${css}</style>`);
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
