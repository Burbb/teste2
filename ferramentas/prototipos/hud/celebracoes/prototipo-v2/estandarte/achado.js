/* PROTÓTIPO da etapa 2, segunda rodada, direção estandarte (montado por auxiliares/montar_v2.py; nada no jogo). */
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

/* PROTÓTIPO, direção C: ESTANDARTE (apresentação de palco). Em vez de uma janela no meio, uma faixa atravessa a tela
   de lado a lado, como o título de um ato: abre a partir de um corte de luz horizontal, as barras de cinema escurecem o
   alto e o pé da tela, e holofotes em pixel nascem atrás da faixa e varrem o alto, cruzando-se devagar. Na faixa, da
   esquerda para a direita, quem (o retrato do herói, ou o item no pedestal sob a sua coluna de luz), o quê (o nível,
   ou o nome e a raridade) e o quanto (os ganhos, ou os números e a comparação). A raridade é a luz do palco: o comum,
   a faixa sem holofotes; o mágico, uma coluna fria; o raro, a coluna de ouro e dois holofotes; o lendário, a coluna de
   brasa, quatro holofotes, as barras de cinema, o corte de luz e as brasas. */
"use strict";

(() => {
  const { h, RARIDADE, CLASSE, ganhos, talento, habilidades, textoItem, arteItem, equipados, aviso, heroi } = Festa;
  const P = FX.PALETAS;

  /** O retrato do herói em 160 px (o busto ampliado por fator inteiro), ou o da HUD. */
  function retrato() {
    const c = heroi().classe;
    if (!c || !Retratos.tem(c)) return "";
    const lado = Retratos.lado(c, "busto"), x = Math.max(1, Math.round(160 / lado));
    return `<img class="desenho pixel" src="${Retratos.url(c, "busto", x)}" width="${lado * x}" height="${lado * x}" alt="" draggable="false">`;
  }

  /** Os holofotes: `n` feixes nascendo em (cx, cy) e varrendo o alto, cada um no seu compasso. */
  function holofotes(p, { cx, cy, n, t, r1, pal, abertura = 1.05, meia = 0.075, vis = 16, quieto, para = -Math.PI / 2 }) {
    const angs = [];
    for (let i = 0; i < n; i++) {
      const base = para + (n === 1 ? 0 : (i / (n - 1) - 0.5) * abertura);
      const vai = quieto ? 0 : Math.sin(t / 1400 + i * 1.7) * 0.16;
      angs.push(base + Math.round(vai * 60) / 60);  // em degraus (1°)
    }
    FX.feixes(p, { cx, cy, angs, meia, r1, pal, vis });
  }
  /** A luz que vaza pelos fios da faixa: uma franja em pontilhado acima e abaixo, mais forte no meio. */
  function franja(p, f, pal, vis = 16) {
    const cs = [FX.cor(pal[2]), FX.cor(pal[3])], meio = (f.esq + f.dir) / 2, larg = (f.dir - f.esq) / 2;
    for (let d = 1; d <= 7; d++) for (let x = Math.max(0, f.esq); x < Math.min(p.W, f.dir); x++) {
      const perto = 1 - Math.abs(x - meio) / larg, nivel = Math.min(vis, Math.round(13 * perto - d * 1.6));
      if (nivel <= 0) continue;
      if (Sprites.pontilha(x, f.topo - d, nivel)) p.por(x, f.topo - d, cs[d < 3 ? 0 : 1]);
      if (Sprites.pontilha(x, f.base + d, nivel)) p.por(x, f.base + d, cs[d < 3 ? 0 : 1]);
    }
  }
  /** As barras de cinema: o alto e o pé da tela escurecem em pontilhado. */
  function barras(p, abre) {
    const alt = Math.round(p.H * 0.09 * abre), k = FX.cor("k");
    for (let y = 0; y < alt; y++) for (let x = 0; x < p.W; x++) {
      const nivel = y < alt - 3 ? 16 : 16 - (y - (alt - 3)) * 5;
      if (Sprites.pontilha(x, y, nivel)) { p.buf[y * p.W + x] = k; p.buf[(p.H - 1 - y) * p.W + x] = k; }
    }
  }
  /** O corte de luz: uma linha branca na altura da faixa, que abre e some nos primeiros quadros. */
  function corte(p, y, t) {
    if (t > 200) return;
    const esp = t < 70 ? 1 : t < 140 ? 3 : 2, vis = t < 140 ? 16 : 8;
    FX.clarao(p, vis, "W", [0, y - esp, p.W, y + esp + 1]);
  }
  /** O brilho que corre pelos fios da faixa (de tempos em tempos). */
  function lampejo(p, f, t, pal) {
    const ciclo = 1800, u = (t % ciclo) / 700;
    if (u > 1) return;
    const x = Math.round(f.esq + (f.dir - f.esq) * u), cs = [FX.cor("W"), FX.cor(pal[1]), FX.cor(pal[2])];
    for (const y of [f.topo, f.base - 1]) for (let d = -8; d <= 8; d++) p.por(x + d, y, cs[Math.min(2, Math.floor(Math.abs(d) / 3))]);
  }
  /** Poeira no ar, subindo devagar na luz. */
  const poeira = (enx, cx, cy, larg, pal) => enx.soltar(1, () => ({ x: cx + Math.round(FX.aleatorio(-larg, larg)), y: cy,
    vx: FX.aleatorio(-0.25, 0.25), vy: FX.aleatorio(-0.7, -0.3), vida: Math.round(FX.aleatorio(18, 30)), desenho: "ponto", pal }));

  function festa({ classe, esquerda, sobre, grande, sub, direita, pal, som }) {
    const html = `<div class="festa fc ${classe}">
      <div class="fc-faixa"><div class="fc-miolo">
        <div class="fc-esq">${esquerda}</div>
        <div class="fc-meio"><span class="fc-sobre">${sobre}</span><span class="fc-grande">${grande}</span>${sub ? `<span class="fc-sub">${sub}</span>` : ""}</div>
        <div class="fc-dir">${direita}</div>
      </div><div class="fc-rodape"><button class="continuar" type="button">Continuar <span>▸</span></button></div></div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), faixa = el.querySelector(".fc-faixa");
      App.som(som);
      const ctl = FX.animar(p, (t, q, quieto) => {
        const f = p.de(faixa), abre = quieto ? 1 : FX.rampa(t, 60, 520);
        barras(p, quieto ? 1 : FX.rampa(t, 0, 260));
        holofotes(p, { cx: f.x, cy: f.y, n: 6, t, r1: Math.round(f.y * abre), pal, quieto, abertura: 1.35 });
        holofotes(p, { cx: f.x, cy: f.y, n: 4, t: t + 3100, r1: Math.round((p.H - f.y) * abre * 0.9), pal, quieto, abertura: 1.1, para: Math.PI / 2, vis: 9 });
        franja(p, f, pal, quieto ? 12 : Math.round(FX.rampa(t, 80, 400, 0, 16)));
        holofotes(p, { cx: f.x - p.t(innerWidth * 0.3), cy: f.y, n: 1, t: t + 900, r1: Math.round(f.y * 0.95 * abre), pal, quieto, meia: 0.04 });
        holofotes(p, { cx: f.x + p.t(innerWidth * 0.3), cy: f.y, n: 1, t: t + 2300, r1: Math.round(f.y * 0.95 * abre), pal, quieto, meia: 0.04 });
        if (quieto) return;
        corte(p, f.y, t);
        lampejo(p, f, t + 600, pal);
        if (q % 2 === 0) poeira(enx, f.x, f.topo - 2, p.t(innerWidth * 0.42), ["W", pal[1], pal[2], pal[3]]);
        if (q === 2) enx.soltar(24, (i) => ({ x: f.x + FX.aleatorio(-p.t(innerWidth * 0.4), p.t(innerWidth * 0.4)), y: f.topo + (i % 2 ? 0 : f.base - f.topo),
          vx: FX.aleatorio(-1, 1), vy: i % 2 ? FX.aleatorio(-3, -1) : FX.aleatorio(1, 3), arrasto: 0.9, vida: Math.round(FX.aleatorio(8, 14)), desenho: i % 3 ? "ponto" : "cruz", pal: ["W", "Y", pal[2]] }));
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(600); el.classList.add("pulou"); } };
    };
    return { html, efeito, revelaEm: 900 };
  }

  function direitaNivel(d) {
    const g = ganhos(d).map((x, i) => `<span class="fc-ganho" style="--i:${i}">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("");
    const habs = habilidades(d.habilidades).map((x) => `<div class="fc-hab"><span class="fc-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join("");
    return `<div class="fc-ganhos">${g}</div><div class="fc-talento">${talento(32)}<b>+1</b> ponto de talento <small>Talentos (T)</small></div>${habs}
      ${d.especializacao ? '<div class="fc-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}`;
  }

  const direcao = {
    nome: "estandarte",
    nivel(d) {
      const hr = heroi();
      return festa({ classe: "fc-nivel", esquerda: `<div class="fc-retrato">${retrato()}</div>`, sobre: "você subiu de nível",
        grande: `Nível <b>${d.nivel}</b>`, sub: [h(hr.nome), CLASSE[hr.classe]].filter(Boolean).join(" · "), direita: direitaNivel(d), pal: P.ouro, som: "subir" });
    },
    sigilo: (d) => festa({ classe: "fc-sigilo", esquerda: `<div class="fc-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>`,
      sobre: `${h(d.guardiao)} caiu`, grande: `Sigilo <b>${d.sigilos}/3</b>`, sub: "Uma runa ardente se grava na sua mão.",
      direita: `<div class="fc-talento">${talento(32)}<b>+1</b> ponto de talento <small>Talentos (T)</small></div>`, pal: P.sigilo, som: "fanfarra" }),
    spec: (d) => festa({ classe: "fc-spec", esquerda: `<div class="fc-retrato">${retrato()}</div>`, sobre: "você agora é", grande: `<b>${h(d.nome)}</b>`,
      sub: h(d.desc), direita: habilidades(d.habilidades).map((x) => `<div class="fc-hab"><span class="fc-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join(""),
      pal: P.arcano, som: "fanfarra" }),

    achado(d) {
      const it = d.item, rar = h(it.raridade);
      return `<div class="tela achado fc-achado rar-${rar}">
        <div class="achado-cartao novo rar-${rar}">
          <div class="fc-pedestal"><div class="achado-arte">${arteItem(it, 64)}</div></div>
          <div class="fc-ficha"><span class="achado-selo">Você encontrou</span><span class="fc-raridade rar-${rar}">${RARIDADE[it.raridade] || rar}</span>${textoItem(it)}${aviso(d)}</div>
        </div>
        <div class="fc-usa">${equipados(d)}</div></div>`;
    },
    PALCO: {
      comum: { pal: P.comum, coluna: 0, holofotes: 0 },
      magico: { pal: P.magico, coluna: 2, holofotes: 0 },
      raro: { pal: P.raro, coluna: 3, holofotes: 2 },
      lendario: { pal: P.lendario, coluna: 5, holofotes: 5, barras: true, corte: true, brasas: true },
    },
    async cerimonia({ fundo, janela, d, parado, esperar }) {
      const rar = d.item.raridade, cfg = direcao.PALCO[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte");
      if (!parado) App.som(["raro", "lendario"].includes(rar) ? "achado_raro" : "achado");
      fundo.classList.add("entrando");
      FX.animar(p, (t, q, quieto) => {
        const f = p.de(janela), a = p.de(arte), abre = quieto ? 1 : FX.rampa(t, 40, 460);
        if (cfg.barras) barras(p, quieto ? 1 : FX.rampa(t, 0, 260));
        if (cfg.holofotes) {
          holofotes(p, { cx: f.x, cy: f.y, n: cfg.holofotes, t, r1: Math.round(f.y * abre), pal: cfg.pal, quieto, abertura: 1.3 });
          if (rar === "lendario") holofotes(p, { cx: f.x, cy: f.y, n: 3, t: t + 3100, r1: Math.round((p.H - f.y) * abre * 0.9), pal: cfg.pal, quieto, abertura: 1, para: Math.PI / 2, vis: 9 });
        }
        if (rar !== "comum") franja(p, f, cfg.pal, rar === "magico" ? 7 : rar === "raro" ? 11 : 16);
        if (cfg.coluna) FX.coluna(p, { cx: a.x, base: f.topo, larg: cfg.coluna, pal: ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]], q: quieto ? 0 : q, vis: quieto ? 12 : 16 });
        if (quieto) return;
        if (cfg.corte) corte(p, f.y, t);
        lampejo(p, f, t + 300, cfg.pal);
        if (rar !== "comum" && q % 3 === 0) poeira(enx, a.x, f.topo - 1, cfg.coluna + 4, ["W", cfg.pal[1], cfg.pal[2]]);
        if (cfg.brasas && q % 2 === 0) poeira(enx, f.x, f.topo - 1, p.t(innerWidth * 0.4), ["Y", "O", "o", "r", "D"]);
        enx.passo(); enx.desenhar(p);
      });
      if (parado) return;
      await esperar({ comum: 220, magico: 300, raro: 420, lendario: 560 }[rar] || 300);
    },
  };

  const regua = (c1, c2) => `0 -3px 0 ${c1}, 0 -6px 0 #000, 0 -9px 0 ${c2}, 0 3px 0 ${c1}, 0 6px 0 #000, 0 9px 0 ${c2}`;
  const css = `
  /* ---- C: Estandarte ---- */
  #celebracao.dir-estandarte { background: rgba(4, 3, 2, 0.8); }
  .festa.fc { position: relative; z-index: 1; width: 100vw; max-width: none; background: none; border: 0; box-shadow: none; padding: 0; }
  .fc-faixa { position: relative; width: 100%; padding: 22px 0 16px; background: linear-gradient(rgba(8, 7, 6, 0.93), rgba(8, 7, 6, 0.97)), var(--t-painel) 0 0 / 128px;
    border-top: 3px solid #d4af37; border-bottom: 3px solid #d4af37; box-shadow: ${regua("#d4af37", "#8a6a14")};
    animation: fc-abre 0.27s steps(4) both; }
  @keyframes fc-abre { from { clip-path: inset(50% 0 50% 0); } to { clip-path: inset(-12px 0 -12px 0); } }
  .fc-miolo { display: grid; grid-template-columns: 200px auto minmax(320px, 520px); align-items: center; justify-content: center; gap: 36px; padding: 0 32px; }
  .fc-esq { display: grid; place-items: center; }
  .fc-retrato { width: 168px; height: 168px; display: grid; place-items: center; background: #17120f; border: 3px solid #8a6a14;
    box-shadow: 0 0 0 3px #000, inset 0 0 0 3px #2b2219; overflow: hidden; animation: fc-entra-esq 0.27s 0.13s steps(4) both; }
  .fc-retrato img { width: 160px; height: 160px; image-rendering: pixelated; }
  @keyframes fc-entra-esq { from { translate: -60px 0; opacity: 0; } 25% { opacity: 1; } to { translate: 0 0; } }
  .fc-meio { display: flex; flex-direction: column; align-items: flex-start; min-width: 280px; }
  .fc-sobre { font: 700 15px/1 var(--texto); letter-spacing: 0.3em; text-transform: uppercase; color: #f2d27a; }
  .fc-grande { font: 72px/1 var(--titulo); color: #f1e4c4; text-shadow: 3px 3px 0 #000; margin: 6px 0 4px; white-space: nowrap; }
  .fc-grande b { font-weight: 400; font-size: 116px; color: #ffe27a; text-shadow: 3px 0 #0d0b0a, -3px 0 #0d0b0a, 0 3px #0d0b0a, 0 -3px #0d0b0a, 0 7px #000; }
  .fc-spec .fc-grande b { font-size: 60px; } .fc-sigilo .fc-grande b { font-size: 76px; }
  .fc-sub { font: 18px/1.3 var(--texto); color: #c0b8a8; max-width: 420px; }
  .fc-dir { display: flex; flex-direction: column; gap: 10px; animation: fc-entra-dir 0.27s 0.2s steps(4) both; }
  @keyframes fc-entra-dir { from { translate: 60px 0; opacity: 0; } 25% { opacity: 1; } to { translate: 0 0; } }
  .fc-ganhos { display: grid; grid-template-columns: repeat(3, auto); justify-content: start; gap: 6px 18px; }
  .fc-ganho { display: flex; align-items: center; gap: 6px; }
  .fc-ganho b { font: 30px/1 var(--titulo); color: #8fbf6a; text-shadow: 2px 2px 0 #000; min-width: 44px; }
  .fc-ganho > span { font: 700 12px/1 var(--texto); letter-spacing: 0.14em; text-transform: uppercase; color: #c0b8a8; }
  .fc-talento { display: flex; align-items: center; gap: 8px; font: 19px/1 var(--texto); color: #f2d27a; padding-top: 8px; border-top: 2px solid #2b2219; }
  .fc-talento b { font: 30px/1 var(--titulo); color: #fff3a0; text-shadow: 2px 2px 0 #000; }
  .fc-talento small { font-size: 12px; color: #c0b8a8; }
  .fc-hab { padding: 6px 12px 8px; border-left: 3px solid #8e6fd8; background: #120c1a; }
  .fc-hab b { display: block; font: 26px/1.05 var(--titulo); color: #e4d8ff; text-shadow: 2px 2px 0 #000; }
  .fc-hab > div { font: 15px/1.35 var(--texto); color: #f1e4c4; }
  .fc-rotulo { font: 700 11px/1 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #c8b0ff; }
  .fc-aviso { font: italic 15px/1.35 var(--texto); color: #c8b0ff; }
  .fc-losangos { display: flex; gap: 18px; } .fc-losangos i { width: 26px; height: 26px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; box-shadow: 0 0 0 3px #000; }
  .fc-losangos i.tem { background: #e2574c; border-color: #fff3a0; }
  .fc-rodape { display: flex; justify-content: flex-end; padding: 10px max(32px, calc(50vw - 560px)) 0; }
  .fc.pulou :is(.fc-faixa, .fc-retrato, .fc-dir) { animation: none; }
  .fc-sigilo .fc-faixa { border-color: #e2574c; box-shadow: ${regua("#e2574c", "#6e0d0d")}; }
  .fc-spec .fc-faixa { border-color: #8e6fd8; box-shadow: ${regua("#8e6fd8", "#5a2a6e")}; }

  /* o achado: a faixa é a janela */
  :root body #sobre-achado.dir-estandarte { background: rgba(4, 3, 2, 0.78); }
  :root body #sobre-achado.dir-estandarte .janela-achado { position: relative; z-index: 1; width: 100vw; box-sizing: border-box; max-height: none; overflow: visible;
    padding: 20px max(32px, calc(50vw - 560px)) 14px; border: 0; border-image: none; border-top: 3px solid var(--fc-fio); border-bottom: 3px solid var(--fc-fio);
    background: linear-gradient(rgba(8, 7, 6, 0.93), rgba(8, 7, 6, 0.97)), var(--t-painel) 0 0 / 128px; box-shadow: 0 -3px 0 var(--fc-fio), 0 -6px 0 #000, 0 -9px 0 var(--fc-fio2), 0 3px 0 var(--fc-fio), 0 6px 0 #000, 0 9px 0 var(--fc-fio2); }
  #sobre-achado.dir-estandarte { --fc-fio: #8a8070; --fc-fio2: #4a4038; }
  #sobre-achado.dir-estandarte.rar-magico { --fc-fio: #7fb0ff; --fc-fio2: #3d63c9; }
  #sobre-achado.dir-estandarte.rar-raro { --fc-fio: #f2c94c; --fc-fio2: #8a6a14; }
  #sobre-achado.dir-estandarte.rar-lendario { --fc-fio: #ffb35c; --fc-fio2: #b3262b; }
  #sobre-achado.dir-estandarte.entrando .janela-achado { animation: fc-abre 0.27s steps(4) both; }
  #sobre-achado.dir-estandarte.adiantado .janela-achado { animation: none; }
  :root body #sobre-achado .fc-achado.tela.achado { display: flex; align-items: center; justify-content: center; gap: 32px; }
  :root body #sobre-achado .fc-achado .achado-cartao.novo { display: flex; align-items: center; gap: 28px; width: auto; background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  .fc-pedestal { width: 170px; height: 170px; display: grid; place-items: center; background: #0d0b0a; border: 3px solid var(--fc-fio); box-shadow: 0 0 0 3px #000, inset 0 -18px 0 #17120f; }
  .fc-pedestal .achado-arte img, .fc-pedestal .achado-arte canvas { width: 128px !important; height: 128px !important; image-rendering: pixelated; }
  .fc-ficha { display: flex; flex-direction: column; align-items: flex-start; text-align: left; width: 360px; }
  .fc-ficha .achado-selo { font: 700 13px/1 var(--texto); letter-spacing: 0.3em; text-transform: uppercase; color: #f2d27a; }
  .fc-ficha > b { font-size: 34px; margin: 6px 0 2px; }
  .fc-raridade { margin-top: 8px; padding: 3px 12px 2px; font: 700 13px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase; color: var(--fc-fio); border: 2px solid var(--fc-fio); background: #0d0b0a; }
  :root body #sobre-achado .fc-usa .achado-cartao { width: 250px; overflow: visible; animation: none; text-align: center; padding: 10px 14px 12px; background: #120e0b; border: 2px solid #3a3128; box-shadow: none; }
  .fc-usa:empty { display: none; } .fc-usa .achado-aneis { display: flex; flex-direction: column; gap: 8px; }
  .dir-estandarte .achado-acoes { display: flex; justify-content: flex-end; gap: 10px; margin-top: 12px; }
  @media (prefers-reduced-motion: reduce) {
    .fc :is(.fc-faixa, .fc-retrato, .fc-dir), #sobre-achado.dir-estandarte .janela-achado { animation: none !important; }
  }
  @media (max-height: 760px) {
    .fc-retrato { width: 136px; height: 136px; } .fc-retrato img { width: 128px; height: 128px; }
    .fc-grande b { font-size: 76px; } .fc-faixa { padding: 14px 0 10px; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-estandarte">${css}</style>`);
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
