/* PROTÓTIPO da etapa 2, segunda rodada, direção relicario (montado por auxiliares/montar_v2.py; nada no jogo). */
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
  function estrela(p, { cx, cy, pontas, ri, re, ang = 0, pal, contorno = "k" }) {
    const cs = pal.map(cor), ck = cor(contorno), passo = (2 * Math.PI) / pontas;
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

  return { cor, reduzido, FPS, QUADRO, PALETAS, DESENHOS, palco, animar, raios, feixes, halo, anel, coluna, clarao, estrela,
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
  const habilidades = (lista) => (lista || []).map((x) => ({ nome: h(x.nome), desc: Realce.texto(x.desc) }));
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

  return {
    h, RARIDADE, CLASSE, icone, ganhos, talento, habilidades, heroi, abrir, celebrar, abrirAchado, textoItem, arteItem,
    equipados, aviso,
    usar(d) { direcao = d; },
    get direcao() { return direcao; },
  };
})();

/* PROTÓTIPO, direção A: RELICÁRIO (cerimonial). O que se ganhou é posto num altar: uma medalha (o nível) ou o próprio
   item, ampliado, no centro de um sol de raios em pixel que gira devagar enquanto a janela está aberta; embaixo, uma
   placa de pedra com o que mudou. A entrada é uma consagração: o clarão na medalha, os raios se abrindo, as faíscas, e
   depois só o giro e um cintilar de vez em quando. A raridade é o tamanho do sol: o comum só tem o halo; o mágico,
   oito raios frios; o raro, doze de ouro; o lendário, dois sóis de brasa girando ao contrário, o clarão e as brasas. */
"use strict";

(() => {
  const { h, RARIDADE, ganhos, talento, habilidades, textoItem, arteItem, equipados, aviso } = Festa;
  const P = FX.PALETAS;

  /** A medalha em pixel: o disco escuro, o aro de metal com luz de cima e da esquerda e o contorno. */
  function medalha(p, cx, cy, R, pal) {
    const [, claro, meio, escuro, fundo] = pal.map(FX.cor);
    const k = FX.cor("k"), q = FX.cor("z"), Q = FX.cor("q");
    for (let y = cy - R - 1; y <= cy + R + 1; y++) for (let x = cx - R - 1; x <= cx + R + 1; x++) {
      const dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy);
      if (d > R + 0.5) continue;
      if (d > R - 0.7) { p.por(x, y, k); continue; }
      const luz = (-dx - dy) / (d || 1);  // 1 no alto à esquerda, -1 embaixo à direita
      if (d > R - 3.5) p.por(x, y, luz > 0.45 ? claro : luz < -0.45 ? escuro : meio);
      else if (d > R - 4.5) p.por(x, y, luz > 0 ? fundo : k);
      else p.por(x, y, Sprites.pontilha(x, y, d < R * 0.55 ? 3 : 1) ? Q : q);
    }
  }

  /** O sol: os raios largos e os finos girando ao contrário, saindo de `R` até `r1`. */
  // os raios que descem (para a placa) são mais curtos: as pontas não aparecem soltas embaixo dela
  const ALCANCE = (a) => 1 - 0.5 * Math.max(0, Math.sin(a));
  function sol(p, { cx, cy, R, r1, ang, n = 14, pal, fino = true, vis = 16, alcance = ALCANCE }) {
    FX.raios(p, { cx, cy, n, ang, larg: 0.4, r0: R, r1, pal: pal.slice(1), esbate: 0.4, vis, alterna: 0.68, alcance });
    if (fino) FX.raios(p, { cx, cy, n: n * 2, ang: -ang * 1.7 + 0.11, larg: 0.09, r0: R, r1: R + (r1 - R) * 0.78, pal, esbate: 0.3, fio: false, vis, alcance });
    FX.halo(p, { cx, cy, r: R + Math.round((r1 - R) * 0.1), pal: [pal[1], pal[2], pal[3]], vis: Math.min(vis, 7) });
  }

  /** Faíscas de consagração saindo do aro, e o cintilar que fica (um brilho de cada vez, num raio). */
  function faiscas(enx, cx, cy, R, n, pal) {
    enx.soltar(n, (i) => {
      const a = (i / n) * Math.PI * 2 + FX.aleatorio(-0.2, 0.2), v = FX.aleatorio(2.2, 4.2);
      return { x: cx + Math.cos(a) * R, y: cy + Math.sin(a) * R, vx: Math.cos(a) * v, vy: Math.sin(a) * v, arrasto: 0.86,
        vida: Math.round(FX.aleatorio(9, 16)), desenho: i % 4 ? "cruz" : "brilho", pal };
    });
  }
  function cintilar(enx, cx, cy, R, r1, pal) {
    const a = FX.aleatorio(0, Math.PI * 2), d = FX.aleatorio(R * 1.3, r1 * 0.8);
    enx.soltar(1, () => ({ x: cx + Math.cos(a) * d, y: cy + Math.sin(a) * d, vx: 0, vy: 0, vida: 9, desenho: Math.random() < 0.5 ? "brilho" : "estrela", pal }));
  }

  /** A festa: a medalha com o título, a placa com o corpo. */
  function festa({ classe, sobre, palavra, numero, grande, corpo, pal, som }) {
    const html = `<div class="festa fa ${classe}">
      <div class="fa-coroa"><div class="fa-sobre"><span>${sobre}</span></div>
        <div class="fa-medalha">${palavra ? `<span class="fa-palavra">${palavra}</span>` : ""}<span class="fa-numero${grande ? " grande" : ""}">${numero}</span></div></div>
      <div class="fa-placa">${corpo}<button class="continuar" type="button">Continuar <span>▸</span></button></div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), med = el.querySelector(".fa-medalha");
      App.som(som);
      const ctl = FX.animar(p, (t, q, parado) => {
        const m = p.de(med), R = Math.round(m.rx * 0.92), r1 = Math.max(R + 10, p.t(Math.min(innerHeight * 0.66, 560)));
        const abre = parado ? 1 : FX.rampa(t, 0, 520);
        sol(p, { cx: m.x, cy: m.y, R, r1: R + (r1 - R) * abre, ang: parado ? 0.12 : q * 0.035, pal });
        if (!parado && t < 330) FX.halo(p, { cx: m.x, cy: m.y, r: R * (2.6 - (t / 330) * 1.2), pal: ["W", "W", "Y", pal[1]], vis: Math.round(16 * (1 - t / 330)) });
        medalha(p, m.x, m.y, R, pal);
        if (parado) return;
        if (q === 1) faiscas(enx, m.x, m.y, R, 18, ["W", "Y", pal[2], pal[3]]);
        if (q > 10 && q % 5 === 0) cintilar(enx, m.x, m.y, R, r1, ["W", "Y", pal[2]]);
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(520); el.classList.add("pulou"); } };
    };
    return { html, efeito };
  }

  function corpoNivel(d) {
    const g = ganhos(d).map((x, i) => `<span class="fa-ganho" style="--i:${i}">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("");
    const habs = habilidades(d.habilidades).map((x) => `<div class="fa-hab"><span class="fa-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join("");
    return `<div class="fa-ganhos">${g}</div>
      <div class="fa-talento">${talento(32)}<span>+1 ponto de talento</span><small>Talentos (T)</small></div>${habs}
      ${d.especializacao ? '<div class="fa-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}`;
  }

  const direcao = {
    nome: "relicario",
    nivel: (d) => festa({ classe: "fa-nivel", sobre: "você subiu de nível", palavra: "Nível", numero: d.nivel, corpo: corpoNivel(d), pal: P.ouro, som: "subir" }),
    sigilo: (d) => festa({ classe: "fa-sigilo", sobre: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, som: "fanfarra",
      corpo: `<div class="fa-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>
        <div class="fa-texto">Uma runa ardente se grava na sua mão.</div>
        <div class="fa-talento">${talento(32)}<span>+1 ponto de talento</span><small>Talentos (T)</small></div>` }),
    spec: (d) => festa({ classe: "fa-spec", sobre: "você agora é", palavra: "", numero: h(d.nome), grande: true, pal: P.arcano, som: "fanfarra",
      corpo: `<div class="fa-texto">${h(d.desc)}</div>${habilidades(d.habilidades).map((x) => `<div class="fa-hab"><span class="fa-rotulo">nova habilidade</span><b>${x.nome}</b><div>${x.desc}</div></div>`).join("")}` }),

    achado(d) {
      const it = d.item, rar = h(it.raridade);
      return `<div class="tela achado fa-achado rar-${rar}">
        <div class="achado-cartao novo rar-${rar}">
          <span class="achado-selo fa-sobre"><span>Você encontrou</span></span>
          <div class="fa-altar"><div class="achado-arte">${arteItem(it, 64)}</div></div>
          <div class="fa-ficha"><span class="fa-raridade rar-${rar}">${RARIDADE[it.raridade] || rar}</span>${textoItem(it)}${aviso(d)}</div>
        </div>
        <div class="fa-usa">${equipados(d)}</div></div>`;
    },
    // a força do sol por raridade
    SOL: {
      comum: null,
      magico: { n: 8, raio: 150, pal: P.magico, fino: false, faiscas: 8 },
      raro: { n: 12, raio: 240, pal: P.raro, fino: true, faiscas: 14 },
      lendario: { n: 14, raio: 360, pal: P.lendario, fino: true, faiscas: 26, clarao: true, brasas: true },
    },
    async cerimonia({ fundo, janela, d, parado, esperar }) {
      const rar = d.item.raridade, cfg = direcao.SOL[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte");
      if (!parado) App.som(["raro", "lendario"].includes(rar) ? "achado_raro" : "achado");
      fundo.classList.add("entrando");
      const brasa = ["Y", "O", "o", "r", "D"];
      FX.animar(p, (t, q, quieto) => {
        const a = p.de(arte), R = Math.round(a.rx * 0.9);
        if (!cfg) {  // comum: só o halo pálido
          FX.halo(p, { cx: a.x, cy: a.y, r: R + 10, pal: ["w", "G", "g", "d"], vis: quieto ? 10 : Math.round(FX.rampa(t, 0, 300, 4, 10)) });
        } else {
          const abre = quieto ? 1 : FX.rampa(t, 60, 520), r1 = p.t(cfg.raio);
          sol(p, { cx: a.x, cy: a.y, R: R + 2, r1: R + 2 + (r1 - R) * abre, ang: quieto ? 0.1 : q * (rar === "lendario" ? 0.04 : 0.03), n: cfg.n, pal: cfg.pal, fino: cfg.fino });
          FX.halo(p, { cx: a.x, cy: a.y, r: R + 4, pal: [cfg.pal[2], cfg.pal[3]], vis: 6 });
        }
        if (quieto) return;
        if (cfg && cfg.clarao && t < 200) FX.clarao(p, Math.round(9 * (1 - t / 200)), "Y");
        if (q === 2) faiscas(enx, a.x, a.y, R, cfg ? cfg.faiscas : 5, cfg ? ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]] : ["W", "w", "G", "g"]);
        if (cfg && q > 10 && q % 6 === 0) cintilar(enx, a.x, a.y, R, p.t(cfg.raio), ["W", cfg.pal[1], cfg.pal[2]]);
        if (cfg && cfg.brasas && q % 2 === 0) enx.soltar(1, () => ({ x: a.x + Math.round(FX.aleatorio(-R * 2.4, R * 2.4)), y: a.y + R + Math.round(FX.aleatorio(0, 12)),
          vx: FX.aleatorio(-0.2, 0.2), vy: FX.aleatorio(-1.1, -0.6), vida: Math.round(FX.aleatorio(14, 24)), desenho: "brasa", pal: brasa }));
        enx.passo(); enx.desenhar(p);
      });
      if (parado) return;
      // a entrada: o item desce ao altar e o sol se abre; os botões chegam depois (o adiantar encurta)
      await esperar({ comum: 220, magico: 320, raro: 480, lendario: 620 }[rar] || 300);
    },
  };

  const css = `
  /* ---- A: Relicário ---- */
  #celebracao.dir-relicario { background: rgba(4, 3, 2, 0.9); }
  .festa.fa { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; gap: 4px;
    width: min(780px, 94vw); background: none; border: 0; box-shadow: none; padding: 0; text-align: center; }
  .fa-coroa { display: flex; flex-direction: column; align-items: center; margin-bottom: 26px; }
  .fa-sobre { margin-bottom: 30px; }
  .fa-sobre span { display: inline-block; padding: 7px 18px 6px 22px; font: 700 15px/1 var(--texto); letter-spacing: 0.32em; text-transform: uppercase;
    color: #fff3a0; background: #0d0b0a; border: 2px solid #8a6a14; box-shadow: 0 0 0 2px #000, inset 0 2px 0 #2b2219; }
  .fa-medalha { width: 168px; height: 168px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .fa-palavra { font: 22px/1 var(--titulo); color: #c0b8a8; text-shadow: 2px 2px 0 #000; margin-top: 6px; }
  .fa-numero { font: 84px/0.9 var(--titulo); color: #ffe27a;
    text-shadow: 3px 0 #0d0b0a, -3px 0 #0d0b0a, 0 3px #0d0b0a, 0 -3px #0d0b0a, 3px 3px #0d0b0a, -3px 3px #0d0b0a, 3px -3px #0d0b0a, -3px -3px #0d0b0a, 0 6px #000; }
  .fa-numero.grande { font-size: 30px; line-height: 1.05; max-width: 150px; overflow-wrap: anywhere; }
  .fa-sigilo .fa-numero { font-size: 54px; }
  .fa-placa { position: relative; width: 100%; box-sizing: border-box; padding: 16px 22px 18px;
    border: 12px solid transparent; border-image: var(--m-principal) 24 / 24px round;
    background: linear-gradient(rgba(8, 9, 11, 0.84), rgba(8, 9, 11, 0.92)), var(--t-painel) 0 0 / 128px; background-clip: padding-box;
    box-shadow: 0 10px 0 rgba(0, 0, 0, 0.55); }
  .fa-ganhos { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px 10px; }
  .fa-ganho { position: relative; overflow: hidden; display: grid; grid-template-columns: auto auto; grid-template-rows: auto auto; align-items: center;
    column-gap: 8px; min-width: 86px; padding: 7px 10px 6px; background: #17120f; border: 2px solid #48311f; box-shadow: inset 0 2px 0 #2b2219, 0 2px 0 #000; }
  .fa-ganho img { grid-row: span 2; }
  .fa-ganho b { font: 30px/1 var(--titulo); color: #8fbf6a; text-shadow: 2px 2px 0 #000; text-align: left; }
  .fa-ganho > span { font: 700 11px/1.1 var(--texto); letter-spacing: 0.14em; text-transform: uppercase; color: #c0b8a8; text-align: left; }
  .fa-ganho::after { content: ""; position: absolute; top: 0; bottom: 0; left: -40%; width: 18%; background: rgba(255, 243, 160, 0.28);
    translate: -100% 0; animation: fa-lampejo 0.6s calc(0.45s + var(--i) * 0.09s) steps(6) both; }
  @keyframes fa-lampejo { to { translate: 900% 0; } }
  .fa-talento { display: inline-flex; align-items: center; gap: 10px; margin-top: 12px; padding: 5px 16px 5px 8px; font: 20px/1 var(--texto); color: #f2d27a;
    border: 2px solid #8a6a14; background: #1d1608; box-shadow: inset 0 2px 0 #3a2c0c, 0 2px 0 #000; }
  .fa-talento small { font-size: 12px; color: #c0b8a8; letter-spacing: 0.04em; }
  .fa-hab { margin: 12px auto 0; max-width: 560px; padding: 8px 14px; text-align: left; border: 2px solid #5a2a6e; background: #150f1d; box-shadow: inset 0 2px 0 #241830; }
  .fa-hab b { display: block; font: 26px/1.1 var(--titulo); color: #c8b0ff; text-shadow: 2px 2px 0 #000; }
  .fa-hab > div { font: 16px/1.35 var(--texto); color: #e8dcbe; }
  .fa-rotulo { font: 700 11px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase; color: #8e6fd8; }
  .fa-aviso, .fa-texto { margin-top: 10px; font: italic 16px/1.4 var(--texto); color: #c8b0ff; }
  .fa-texto { color: #e8dcbe; font-style: normal; }
  .fa-losangos { display: flex; justify-content: center; gap: 12px; margin: 2px 0 4px; }
  .fa-losangos i { width: 18px; height: 18px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; }
  .fa-losangos i.tem { background: #e2574c; border-color: #ffb35c; box-shadow: 0 0 0 2px #000; }
  .festa.fa .continuar { margin-top: 14px; }
  #celebracao.dir-relicario :is(.festa, .continuar) { user-select: none; }
  /* a entrada: a medalha carimba, a placa sobe; em degraus */
  .fa .fa-medalha { animation: fa-carimbo 0.27s steps(4) both; }
  @keyframes fa-carimbo { from { scale: 1.45; } to { scale: 1; } }
  .fa .fa-placa { animation: fa-sobe 0.2s 0.08s steps(3) both; }
  @keyframes fa-sobe { from { translate: 0 18px; } to { translate: 0 0; } }
  .fa.pulou :is(.fa-medalha, .fa-placa), .fa.pulou .fa-ganho::after { animation: none; }

  /* o achado */
  #sobre-achado.dir-relicario { background: rgba(4, 3, 2, 0.84); }
  :root body #sobre-achado.dir-relicario .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0; max-height: none; overflow: visible; }
  :root body #sobre-achado .fa-achado.tela.achado { display: flex; align-items: flex-end; justify-content: center; gap: 22px; }
  :root body #sobre-achado .fa-achado .achado-cartao.novo { display: flex; flex-direction: column; align-items: center; width: 360px;
    background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  :root body #sobre-achado .fa-usa .achado-cartao { width: auto; overflow: visible; animation: none; }
  .fa-achado .achado-cartao.novo > .achado-selo { font: 700 13px/1 var(--texto); letter-spacing: 0.3em; text-transform: uppercase; color: #fff3a0;
    text-shadow: 2px 0 #000, -2px 0 #000, 0 2px #000, 0 -2px #000; }
  .fa-altar { height: 210px; display: grid; place-items: center; }
  .fa-altar .achado-arte img, .fa-altar .achado-arte canvas { width: 128px !important; height: 128px !important; image-rendering: pixelated; }
  :root body #sobre-achado :is(.fa-ficha, .fa-usa > .achado-cartao, .fa-usa .achado-cartao.compacto) { box-sizing: border-box; padding: 12px 16px 14px; text-align: center;
    border: 12px solid transparent; border-image: var(--m-principal) 24 / 24px round; box-shadow: 0 8px 0 rgba(0, 0, 0, 0.5);
    background: linear-gradient(rgba(8, 9, 11, 0.86), rgba(8, 9, 11, 0.94)), var(--t-painel) 0 0 / 128px; background-clip: padding-box; }
  .fa-ficha { width: 100%; }
  .fa-usa { width: 270px; }
  .fa-usa:empty { display: none; }
  :root body #sobre-achado.dir-relicario { background: rgba(4, 3, 2, 0.86); }
  :root body #sobre-achado .fa-achado .achado-cartao.novo > .achado-selo.fa-sobre { margin: 0; text-shadow: none; }
  .fa-usa .achado-cartao.atual { opacity: 0.92; }
  .fa-ficha > b, .fa-ficha .r-comum, .fa-ficha [class^="r-"] { font-size: 26px; }
  .fa-raridade { display: inline-block; margin: -2px 0 6px; padding: 3px 12px 2px; font: 700 13px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase;
    border: 2px solid currentColor; background: #0d0b0a; box-shadow: 0 2px 0 #000; }
  .fa-raridade.rar-comum { color: #c0b8a8; } .fa-raridade.rar-magico { color: #7fb0ff; }
  .fa-raridade.rar-raro { color: #f2c94c; } .fa-raridade.rar-lendario { color: #ffb35c; }
  /* a cor da raridade num fio por dentro da moldura */
  :root body #sobre-achado.dir-relicario.rar-magico .fa-ficha { box-shadow: inset 0 0 0 2px #3d63c9, 0 8px 0 rgba(0, 0, 0, 0.5); }
  :root body #sobre-achado.dir-relicario.rar-raro .fa-ficha { box-shadow: inset 0 0 0 2px #d4af37, 0 8px 0 rgba(0, 0, 0, 0.5); }
  :root body #sobre-achado.dir-relicario.rar-lendario .fa-ficha { box-shadow: inset 0 0 0 2px #e0782f, inset 0 0 0 4px #6e0d0d, 0 8px 0 rgba(0, 0, 0, 0.5); }
  .fa-usa .achado-aneis { display: flex; flex-direction: column; gap: 8px; }
  .dir-relicario .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 16px; }
  .dir-relicario.entrando .fa-altar .achado-arte { animation: fa-desce 0.24s steps(4) both; }
  @keyframes fa-desce { from { translate: 0 -36px; } to { translate: 0 0; } }
  .dir-relicario.adiantado .fa-altar .achado-arte { animation: none; }
  @media (max-height: 760px) {
    .fa-sobre { margin-bottom: 18px; } .fa-coroa { margin-bottom: 14px; }
    .fa-medalha { width: 128px; height: 128px; } .fa-numero { font-size: 64px; } .fa-palavra { font-size: 18px; }
    .fa-placa { padding: 10px 18px 12px; } .fa-hab { margin-top: 8px; padding: 6px 12px; } .fa-hab b { font-size: 22px; }
    .fa-talento { margin-top: 8px; } .festa.fa .continuar { margin-top: 8px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fa :is(.fa-medalha, .fa-placa), .fa-ganho::after, .dir-relicario .fa-altar .achado-arte { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-relicario">${css}</style>`);
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
