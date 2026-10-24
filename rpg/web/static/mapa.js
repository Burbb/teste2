/* Mapa em pixel art: terreno colorido pelo bioma de cada região conhecida (o resto é névoa), estradas por estado,
   os símbolos dos lugares, o herói na plaqueta, as marcas da missão e dos contratos, e botões clicáveis por cima para
   viajar. Desde a 1.200.0 (a 1E.4): a escala inteira (o canvas na resolução do pixel do mapa, ×2 no minimapa e ×3 no
   mapa grande e no da Viagem, exibido em pixels inteiros); os cinco lugares da campanha em grade nativa (32 no minimapa
   e fora do mapa, 48 no mapa grande), as peças em 1:1 sobre o canvas; o bloqueio vindo da regra da viagem (o campo
   `bloqueio` do motor: a cancela, a estrada apagada e o destino sem convite); o nome de cada lugar num lugar livre. As
   fontes estão em ferramentas/arte/aseprite/mapa-*; o estudo, as alternativas (a seta) e as fotos, em
   ferramentas/prototipos/hud/mapa/. As áreas de clique (28 e 40 px), os destinos, a dica e as regras são as de antes. */
"use strict";

const MapaPx = (() => {
  // Mesma paleta e mesmo pontilhado da vista: três tons por bioma, tingidos pela hora do dia.
  const PALETA = {
    floresta: ["#142618", "#24402a", "#3e6236"], pantano: ["#122624", "#1f3d38", "#3d6052"],
    montanha: ["#2e2f3a", "#4d4f5e", "#858b9c"], planicie: ["#3e3618", "#5e5326", "#8a7c40"],
    ruinas: ["#251d2e", "#3d3046", "#5e5068"], cidadela: ["#240606", "#420c0e", "#7a1c16"],
    vila: ["#33240f", "#523a1e", "#7e6034"],
  };
  const TINTA = [["#c09a80", 0.12], [null, 0], ["#82363e", 0.2], ["#0d1328", 0.5]];  // manhã, tarde, crepúsculo, noite
  const NEVOA = "#0f0c0a";
  let ambiente = { periodo_n: 1, clima_id: "limpo" };
  const cache = {};
  const { BAYER4, rgb, misturar } = Sprites;
  const DIR = "/static/hud/icones/";
  const arquivo = (nome) => `src="${DIR}${nome}.png" srcset="${DIR}${nome}@2x.png 2x"`;
  // os cinco lugares da campanha em grade nativa: 32 no minimapa e fora do mapa, 48 no mapa grande e no da Viagem; os que
  // só o mundo gerado tem (a montanha, a cidadela, o covil) ficam com os ícones de lugar da família (32 e 40), e o covil
  // vencido com o sprite do jogo
  const NATIVOS = new Set(["vila", "floresta", "pantano", "ruinas", "planicie"]);
  function simbolo(n, grande) {
    const s = sprite(n), nativo = NATIVOS.has(s), lado = grande ? (nativo ? 48 : 40) : 32;
    return { lado, html: nativo ? `<img class="sprite desenho pixel" ${arquivo(`mapa-${s}-${lado}`)} alt="">` : Icones.lugar(s, lado) };
  }
  // as peças do mapa, uma para cada tamanho (o minimapa e o que vai fora do mapa; o mapa grande)
  const PECAS = { missao: ["mapa-missao-9", "mapa-missao-11"], contrato: ["mapa-contrato-9", "mapa-contrato-11"],
    cancela: ["mapa-cancela-13", "mapa-cancela-19"] };
  const MEDIDAS = { "mapa-cancela-13": [13, 11], "mapa-cancela-19": [19, 15] };

  function tons(n) {
    const b = n.tipo === "vila" ? "vila" : n.bioma;
    let t = (PALETA[b] || PALETA.planicie).slice();
    const [cor, f] = TINTA[ambiente.periodo_n] || TINTA[1];
    if (cor) t = t.map((c) => misturar(c, cor, f));
    if (!n.visitado && !n.atual) t = t.map((c) => misturar(c, NEVOA, 0.35));
    return t;
  }
  function ruido(x, y, sem) {
    const h = (a, b) => { let v = Math.sin(a * 127.1 + b * 311.7 + sem * 74.7) * 43758.5453; return v - Math.floor(v); };
    const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi;
    const a = h(xi, yi), b = h(xi + 1, yi), c = h(xi, yi + 1), d = h(xi + 1, yi + 1);
    const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
  }

  function sprite(n) {
    if (n.covil === "ativo") return "covil";
    if (n.covil === "vencido") return "vencido";
    if (n.tipo === "vila") return "vila";
    return n.bioma;
  }
  // a viagem não chega lá agora (a saída fechada da campanha, a cidadela sem os Sigilos): o motor diz (mapa.bloqueio)
  const bloqueado = (n) => !!n.bloqueio;

  function enquadrar(nos, grande) {
    let vb = [-6, -5, 112, 64];
    if (nos.length) {
      const xs = nos.map((n) => n.x * 100), ys = nos.map((n) => n.y * 50);
      const minW = grande ? 70 : 46, minH = grande ? 40 : 26;
      let w = Math.max(Math.max(...xs) - Math.min(...xs) + 20, minW), h = Math.max(Math.max(...ys) - Math.min(...ys) + 16, minH);
      if (w / h > 1.75) h = w / 1.75; else w = h * 1.75;
      const cx = (Math.max(...xs) + Math.min(...xs)) / 2, cy = (Math.max(...ys) + Math.min(...ys)) / 2;
      vb = [cx - w / 2, cy - h / 2, w, h];
    }
    return vb;
  }

  function enfeite(x, b, px, py, t, r) {
    const p = (dx, dy, w, h, c) => { x.fillStyle = c; x.fillRect(px + dx, py + dy, w, h); };
    if (b === "floresta") { p(0, -4, 1, 1, t[0]); p(-1, -3, 3, 1, t[0]); p(-1, -2, 3, 1, t[0]); p(-2, -1, 5, 1, t[0]); p(0, 0, 1, 1, t[0]); p(0, -3, 1, 1, t[2]); }
    else if (b === "montanha") {
      for (let i = 0; i < 4; i++) p(-i, -3 + i, 1 + i * 2, 1, i < 2 ? "#dfe4ee" : t[0]);
      p(1, -1, 2, 2, t[1]);
    } else if (b === "pantano") { if (r < 0.5) { p(-2, 0, 4, 1, t[2]); p(0, 2, 3, 1, t[2]); } else { p(0, -3, 1, 4, t[0]); p(2, -2, 1, 3, t[0]); p(-1, -1, 1, 2, t[0]); } }
    else if (b === "planicie") { p(0, -1, 1, 1, t[2]); p(-1, -2, 1, 1, t[2]); p(1, -2, 1, 1, t[2]); }
    else if (b === "ruinas") { p(0, -4, 2, 5, t[0]); p(-1, -4, 4, 1, t[0]); if (r < 0.4) { p(2, -3, 3, 1, t[0]); p(4, -3, 1, 4, t[0]); } }
    else if (b === "cidadela") { p(0, -4, 1, 5, "#120303"); p(2, -2, 1, 3, "#120303"); p(1, -1, 1, 1, "#ff3020"); }
    else if (b === "vila") { p(-2, -2, 5, 3, t[0]); p(-1, -3, 3, 1, "#5a1a10"); p(0, -1, 1, 1, ambiente.periodo_n >= 2 ? "#ffc860" : t[1]); }
  }

  // livre: o raio, em pixels do mapa, em volta de cada lugar sem enfeite (o símbolo fica limpo)
  function terreno(nos, vb, W, H, livre) {
    const chave = nos.map((n) => `${n.id}${n.bioma}${n.tipo}${n.visitado ? 1 : 0}`).join(",") + vb.map((v) => v.toFixed(1)).join(",") + W +
      ambiente.periodo_n + ambiente.clima_id;
    if (cache[chave]) return cache[chave];
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    const x = c.getContext("2d");
    const img = x.createImageData(W, H);
    const pos = nos.map((n) => [(n.x * 100 - vb[0]) / vb[2] * W, (n.y * 50 - vb[1]) / vb[3] * H, n]);
    const paletas = pos.map((p) => tons(p[2]).map(rgb));
    const nevoa = rgb(NEVOA);
    const alcance = (W / vb[2]) * 13;
    const escala = W / 14;
    const dono = new Int16Array(W * H).fill(-1);
    for (let py = 0; py < H; py++) {
      for (let px = 0; px < W; px++) {
        let i1 = -1, d1 = Infinity, d2 = Infinity;
        pos.forEach((p, i) => {
          const dx = p[0] - px, dy = p[1] - py, d = dx * dx + dy * dy;
          if (d < d1) { d2 = d1; d1 = d; i1 = i; } else if (d < d2) d2 = d;
        });
        const k = (py * W + px) * 4;
        const bayer = BAYER4[(py % 4) * 4 + (px % 4)] / 16;
        let cor = nevoa;
        if (i1 >= 0) {
          const t = Math.max(0, 1 - Math.sqrt(d1) / alcance + (ruido(px / escala * 1.6, py / escala * 1.6, 99) - 0.5) * 0.45);
          if (t * 2.2 > bayer + 0.05) {
            const tom = paletas[i1];
            const n = ruido(px / escala, py / escala, pos[i1][2].id) * 0.8 + ruido(px / (escala / 2.5), py / (escala / 2.5), 7) * 0.2;
            const v = n + (bayer - 0.5) * 0.1;
            cor = v > 0.64 ? tom[2] : v > 0.34 ? tom[1] : tom[0];
            if (Math.sqrt(d2) - Math.sqrt(d1) < 1.2) cor = tom[0];
            dono[py * W + px] = t > 0.35 ? i1 : -1;
          }
        }
        img.data[k] = cor[0]; img.data[k + 1] = cor[1]; img.data[k + 2] = cor[2]; img.data[k + 3] = 255;
      }
    }
    x.putImageData(img, 0, 0);
    let s = 4242;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const passo = Math.max(6, Math.round(W / 40));
    for (let py = 4; py < H - 1; py += passo) {
      for (let px = 3; px < W - 3; px += passo) {
        const jx = px + Math.floor(rnd() * passo), jy = py + Math.floor(rnd() * passo);
        if (jx >= W || jy >= H) continue;
        const i = dono[jy * W + jx];
        if (i < 0 || rnd() < 0.35) continue;
        const n = pos[i][2];
        if (Math.hypot(pos[i][0] - jx, pos[i][1] - jy) < livre) continue;
        enfeite(x, n.tipo === "vila" ? "vila" : n.bioma, jx, jy, tons(n), rnd());
      }
    }
    if (ambiente.clima_id === "neve") {
      x.fillStyle = "rgba(240,244,255,0.55)";
      for (let i = 0; i < W * H / 260; i++) x.fillRect(Math.floor(rnd() * W), Math.floor(rnd() * H), 1, 1);
    }
    cache[chave] = c;
    return c;
  }

  // a linha de Bresenham; `padrao` diz quais passos pintam (o tracejado), a partir de `pula` passos de cada ponta
  function linha(x, x0, y0, x1, y1, cor, padrao, pula0, pula1) {
    x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
    const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0), sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    const total = Math.max(dx, -dy);
    let err = dx + dy, i = 0;
    x.fillStyle = cor;
    for (;;) {
      if (i >= pula0 && i <= total - pula1 && (!padrao || padrao(i - pula0))) x.fillRect(x0, y0, 1, 1);
      if (x0 === x1 && y0 === y1) break;
      const e2 = 2 * err;
      if (e2 >= dy) { err += dy; x0 += sx; }
      if (e2 <= dx) { err += dx; y0 += sy; }
      i++;
    }
  }
  // os estados da estrada: a que sai daqui (dá para ir), a percorrida (as duas pontas visitadas), a só conhecida e a
  // que leva à saída fechada. Cor do traço e o tracejado; a sombra vai um pixel abaixo, no mesmo tracejado.
  const ESTRADA = {
    daqui: { cor: "#e8b84a", padrao: null },
    percorrida: { cor: "#a8957a", padrao: null },
    conhecida: { cor: "#8a7a62", padrao: (i) => i % 3 !== 2 },
    fechada: { cor: "#7a5a50", padrao: (i) => i % 2 === 0 },
  };

  // as marcas da missão e dos contratos, separadas (o jogo junta as duas em `opts.marcas`)
  function marcasPorTipo(opts) {
    const e = typeof estado !== "undefined" ? estado : null;
    if (!e) return { missao: opts.marcas || new Set(), contrato: new Set() };
    return { missao: new Set((e.missoes || []).map((m) => m.lugar_id).filter((id) => id !== null && id !== undefined)),
      contrato: new Set((e.contratos || []).filter((c) => !c.concluido).map((c) => c.lugar_id)) };
  }
  function peca(nome, classe, esq, topo) {
    const im = document.createElement("img");
    im.src = `${DIR}${nome}.png`; im.srcset = `${DIR}${nome}@2x.png 2x`; im.alt = ""; im.draggable = false;
    im.className = "peca-mapa " + classe;
    im.style.left = esq + "px"; im.style.top = topo + "px";
    return im;
  }

  /** Cria o mapa. opts: grande, caixa (o elemento onde ele entra, para medir a largura), clicaveis (Set de ids),
   *  aoClicar(id), nivelHeroi, marcas, dicaDe */
  function criar(mapa, opts = {}) {
    const grande = !!opts.grande;
    const K = grande ? 3 : 2;  // pixels de tela por pixel do mapa
    // a largura útil da caixa onde o mapa entra (sem o respiro dela e a borda de 1 px do mapa), em pixels inteiros
    const alvo = opts.caixa, est = alvo && alvo.clientWidth ? getComputedStyle(alvo) : null;
    const largura = est ? alvo.clientWidth - parseFloat(est.paddingLeft) - parseFloat(est.paddingRight) - 2 : (grande ? 928 : 284);
    const W = Math.floor(largura / K), H = Math.round(W / 1.75);
    const SIM = grande ? 48 : 32;  // o lado dos símbolos da campanha na tela
    const vb = enquadrar(mapa.nos, grande);
    const conv = (n) => [Math.round((n.x * 100 - vb[0]) / vb[2] * W), Math.round((n.y * 50 - vb[1]) / vb[3] * H)];
    const caixa = document.createElement("div");
    // o minimapa estreito (a janela menor): os nomes um pouco menores, para caberem perto do próprio lugar
    caixa.className = "mapa-px" + (grande ? " grande" : "") + (!grande && W * K < 260 ? " estreito" : "");
    caixa.style.width = W * K + "px";
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    c.style.width = W * K + "px"; c.style.height = H * K + "px";
    const x = c.getContext("2d");
    const raio = SIM / 2 / K;  // o símbolo, em pixels do mapa
    x.drawImage(terreno(mapa.nos, vb, W, H, raio + 2), 0, 0);
    const porId = {};
    mapa.nos.forEach((n) => { porId[n.id] = n; });
    const cancelas = [];
    mapa.estradas.forEach((e) => {
      const a = porId[e.a], b = porId[e.b];
      if (!a || !b) return;
      const [x0, y0] = conv(a), [x1, y1] = conv(b);
      const fech = bloqueado(a) ? a : bloqueado(b) ? b : null;
      const tipo = fech ? "fechada" : e.atual ? "daqui" : e.percorrida ? "percorrida" : "conhecida";
      const { cor, padrao } = ESTRADA[tipo];
      // a estrada começa e acaba na borda do símbolo (um pixel de folga), não por cima dele
      const pula = Math.ceil(raio * 0.8) + 1;
      linha(x, x0, y0 + 1, x1, y1 + 1, "#0d0b0a", padrao, pula, pula);
      linha(x, x0, y0, x1, y1, cor, padrao, pula, pula);
      if (fech) {
        // a cancela fica na estrada, logo antes do símbolo da saída
        const [fx, fy] = fech === a ? [x0, y0] : [x1, y1], [ox, oy] = fech === a ? [x1, y1] : [x0, y0];
        const d = Math.hypot(ox - fx, oy - fy) || 1, r = pula + 3;
        cancelas.push([fx + (ox - fx) / d * r, fy + (oy - fy) / d * r]);
      }
    });
    const legado = [];  // o que não tem ícone da família (o covil vencido, só do procedural): o sprite do jogo
    mapa.nos.forEach((n) => {
      if (NATIVOS.has(sprite(n)) || Icones.lugar(sprite(n), SIM)) return;
      const [px, py] = conv(n);
      const spr = Sprites.canvas(sprite(n)), l = Math.round(SIM / K);
      x.globalAlpha = n.visitado || n.atual ? 1 : 0.6;
      x.imageSmoothingEnabled = false;
      if (spr) x.drawImage(spr, px - Math.floor(l / 2), py - Math.floor(l / 2), l, l);
      x.globalAlpha = 1;
      legado.push(n.id);
    });
    caixa.appendChild(c);
    const clic = opts.clicaveis || new Set();
    const marcas = opts.marcas || new Set();
    const { missao, contrato } = marcasPorTipo(opts);
    const tam = grande ? 1 : 0;  // as peças têm um tamanho para cada mapa
    mapa.nos.forEach((n) => {
      const [px, py] = conv(n);
      const sx = px * K, sy = py * K;  // o centro do lugar na tela, em pixel inteiro
      const apagado = !n.visitado && !n.atual;
      const sim = simbolo(n, grande), L = sim.lado;  // o lado deste símbolo na tela
      // o símbolo da família, 1:1, por baixo do botão (o botão continua sendo a área de clique)
      if (!legado.includes(n.id)) {
        const holder = document.createElement("span");
        holder.innerHTML = sim.html;
        const im = holder.firstElementChild;
        if (im) {
          im.classList.add("simbolo-lugar");
          im.dataset.id = n.id;
          if (apagado) im.classList.add("apagado");
          im.style.left = sx - L / 2 + "px"; im.style.top = sy - L / 2 + "px";
          im.style.width = im.style.height = L + "px";
          caixa.appendChild(im);
        }
      }
      const b = document.createElement("button");
      b.type = "button";
      b.className = "no-btn" + (n.atual ? " atual" : "") + (clic.has(n.id) ? " clicavel" : "") + (marcas.has(n.id) ? " tem-contrato" : "") +
        (bloqueado(n) ? " bloqueado" : "");
      b.dataset.id = n.id;
      b.style.left = sx + "px"; b.style.top = sy + "px";
      const nv = n.nivel ? ` · ${n.tipo === "vila" ? "arredores" : "inimigos"} Nv.${n.nivel}` : "";
      b.setAttribute("aria-label", `${n.nome} — ${n.descricao}${nv}${n.distancia ? ` · ${Texto.plural(n.distancia, "trecho")} daqui` : ""}${marcas.has(n.id) ? " · você tem um contrato aqui" : ""}`);
      if (opts.dicaDe) b.dataset.dica = Telas.guardarDica(opts.dicaDe(n));
      if (clic.has(n.id) && opts.aoClicar) b.addEventListener("click", (ev) => { ev.stopPropagation(); opts.aoClicar(n.id); });
      caixa.appendChild(b);
      // a direção B: o herói na plaqueta, acima do símbolo; sem espaço acima (perto da borda de cima), ao lado, com a
      // ponta virada para ele (à esquerda; sem espaço à esquerda, espelhada à direita)
      const heroi = n.atual && typeof estado !== "undefined" && estado && Retratos.tem(estado.heroi.classe);
      let plaqueta = null;
      if (heroi) {
        const e2 = grande ? 2 : 1, cima = sy - Math.round(L / 2) - 19 * e2;
        if (cima >= 2) plaqueta = { lado: "cima", x: sx - 10 * e2, y: cima, w: 20 * e2, h: 22 * e2, e2 };
        else {
          const esq = sx - Math.round(L / 2) - 21 * e2;
          plaqueta = esq >= 2 ? { lado: "esq", x: esq, y: sy - 10 * e2, w: 22 * e2, h: 20 * e2, e2 }
            : { lado: "dir", x: sx + Math.round(L / 2) - e2, y: sy - 10 * e2, w: 22 * e2, h: 20 * e2, e2 };
        }
      }
      // as marcas no canto de cima à direita do símbolo (não do botão): a missão primeiro, o contrato ao lado; com a
      // plaqueta em cima, vão para o lado dela; com a plaqueta à direita, para o canto de cima à esquerda
      const canto = [sx + Math.round(L / 2) - (grande ? 6 : 5), sy - Math.round(L / 2) - (grande ? 5 : 4)];
      if (plaqueta && plaqueta.lado === "cima") canto[0] = Math.max(canto[0], plaqueta.x + plaqueta.w + 2);
      const passo = grande ? 12 : 10;
      const marcasAqui = [missao.has(n.id) && "missao", contrato.has(n.id) && "contrato"].filter(Boolean);
      if (plaqueta && plaqueta.lado === "dir") canto[0] = sx - Math.round(L / 2) - (grande ? 5 : 4) - passo * (marcasAqui.length - 1);
      marcasAqui.forEach((m, i) => caixa.appendChild(peca(PECAS[m][tam], "marca", canto[0] + passo * i, canto[1])));
      if (plaqueta) {
        const { e2 } = plaqueta, t = document.createElement("span"), deLado = plaqueta.lado !== "cima";
        t.className = "pos-heroi" + (deLado ? " lado" : "") + (plaqueta.lado === "dir" ? " dir" : "");
        t.dataset.id = n.id;
        Object.assign(t.style, { left: plaqueta.x + "px", top: plaqueta.y + "px", width: plaqueta.w + "px", height: plaqueta.h + "px" });
        const moldura = deLado ? `mapa-posicao_lado-${22 * e2}` : `mapa-posicao-${20 * e2}`;
        const fx = (plaqueta.lado === "dir" ? 4 : 2) * e2;
        t.innerHTML = `<img class="moldura" ${arquivo(moldura)} alt="" draggable="false">` +
          `<img class="fig" src="${Retratos.url(estado.heroi.classe, "figura", e2)}" srcset="${Retratos.url(estado.heroi.classe, "figura", 2 * e2)} 2x" alt="" draggable="false" ` +
          `style="left:${fx}px;top:${2 * e2}px;width:${16 * e2}px;height:${16 * e2}px">`;
        caixa.appendChild(t);
        b.classList.add("com-plaqueta");  // a plaqueta é o "você está aqui"; o anel que some fica só sem ela
      }
      if (grande || n.atual) {
        const r = document.createElement("span");
        const perigo = n.nivel && opts.nivelHeroi && n.nivel >= opts.nivelHeroi + 2;
        r.className = "rotulo-mapa" + (n.atual ? " atual" : "") + (perigo ? " perigo" : "") + (apagado ? " apagado" : "");
        r.dataset.id = n.id;
        r.textContent = n.nome + (grande && n.nivel ? ` · Nv.${n.nivel}` : "");
        r.style.left = sx + "px";
        r.style.top = sy + Math.round(L / 2) + (grande ? 0 : -1) + "px";
        caixa.appendChild(r);
      }
    });
    cancelas.forEach(([cx, cy]) => {
      const nome = PECAS.cancela[tam], [w, h] = MEDIDAS[nome];
      caixa.appendChild(peca(nome, "cancela", Math.round(cx * K - w / 2), Math.round(cy * K - h / 2)));
    });
    requestAnimationFrame(() => encaixarRotulos(caixa));
    if (opts.dicaDe) Telas.ligarDicas(caixa);
    return caixa;
  }

  /** O nome de cada lugar: embaixo do símbolo, como no jogo; senão em cima, e nos dois casos deslizando para os lados até
   *  ficar livre (ainda sob ou sobre o próprio símbolo); senão à esquerda (antes da plaqueta, quando ela está à esquerda)
   *  ou à direita. Entre as livres, a mais longe dos outros lugares. Livre quer dizer dentro do mapa, longe (FOLGAS px) do símbolo, do botão e do tracejado dos outros
   *  lugares, e fora da plaqueta, das marcas e dos outros nomes: o nome fica claramente do próprio lugar. Sem nenhum
   *  livre numa linha, tenta em duas linhas; sem nenhum, faz como antes (desliza para dentro da borda e desce até sair
   *  de cima de outro nome). Só o desenho muda; a área de clique é o botão. */
  function encaixarRotulos(caixa) {
    if (!caixa.isConnected) return;
    const FOLGAS = [12, 4, 0], LONGE = 30;  // a folga dos outros lugares conta do botão; o tracejado passa 2 px dele
    const c = caixa.getBoundingClientRect();
    const cruza = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
    const ret = (el) => el.getBoundingClientRect();
    const larga = (r, f) => ({ left: r.left - f, right: r.right + f, top: r.top - f, bottom: r.bottom + f });
    const mover = (b, dx, dy) => ({ left: b.left + dx, right: b.right + dx, top: b.top + dy, bottom: b.bottom + dy });
    const dentro = (r) => r.left >= c.left + 2 && r.right <= c.right - 2 && r.top >= c.top + 1 && r.bottom <= c.bottom - 1;
    const postos = [];
    [...caixa.querySelectorAll(".rotulo-mapa")].sort((a, b) => a.offsetTop - b.offsetTop).forEach((r) => {
      const id = r.dataset.id;
      let b = ret(r);
      const proprio = (el) => el.dataset.id === id;
      const caixas = [...caixa.querySelectorAll(".no-btn, .simbolo-lugar")].filter((el) => !proprio(el)).map(ret);
      const fixos = [...caixa.querySelectorAll(".pos-heroi, .peca-mapa.marca")].map(ret).concat(postos);
      const sim = caixa.querySelector(`.simbolo-lugar[data-id="${id}"]`), pl = caixa.querySelector(`.pos-heroi[data-id="${id}"]`);
      const s = sim ? ret(sim) : b, meio = s.top + s.height / 2 - b.height / 2 - b.top;
      const esq = pl && pl.classList.contains("lado") && !pl.classList.contains("dir") ? ret(pl).left : s.left;
      const dir = pl && pl.classList.contains("dir") ? ret(pl).right : s.right;
      // embaixo e em cima, do centro para os lados, enquanto o nome ainda cobre parte do símbolo na horizontal
      const lados = [0];
      for (let d = 2; d <= b.width / 2 + s.width / 2 - 8; d += 2) lados.push(d, -d);
      const opcoes = [...lados.map((dx) => [dx, 0]), ...lados.map((dx) => [dx, s.top - 2 - b.bottom]),
        [esq - 4 - b.right, meio], [dir + 4 - b.left, meio]];
      const longe = (m) => Math.min(LONGE, ...caixas.map((o) => Math.hypot(Math.max(0, o.left - m.right, m.left - o.right),
        Math.max(0, o.top - m.bottom, m.top - o.bottom))));
      // entre as posições livres de cima e de baixo, a mais longe dos outros lugares (até LONGE px), e, empatando, a mais
      // centrada no próprio símbolo; os lados só sem nenhuma livre em cima ou embaixo. A folga dos outros lugares baixa em
      // degraus (FOLGAS) quando nenhuma posição cabe com a maior
      const procurar = (opcoes) => {
        for (const folga of FOLGAS) {
          const obst = caixas.map((r) => larga(r, folga)).concat(fixos);
          const ok = ([dx, dy]) => { const m = mover(b, dx, dy); return dentro(m) && !obst.some((o) => cruza(m, o)); };
          const verticais = opcoes.slice(0, -2).filter(ok);
          const achada = verticais.length ? verticais.reduce((x, y) => {
            const lx = longe(mover(b, ...x)), ly = longe(mover(b, ...y));
            return ly > lx || (ly === lx && Math.abs(y[0]) < Math.abs(x[0])) ? y : x;
          }) : opcoes.slice(-2).find(ok);
          if (achada) return achada;
        }
        return null;
      };
      let livre = procurar(opcoes);
      if (!livre && /\s/.test(r.textContent)) {  // só um nome com espaço quebra
        // nenhum lugar livre numa linha (o lugar apertado na borda, com um vizinho perto): o nome em duas linhas, mais
        // estreito, centrado sob ou sobre o próprio símbolo
        // quebra no espaço mais perto do meio (a caixa fica do tamanho da linha mais larga, não de uma largura fixa)
        const nome = r.textContent, meioNome = nome.length / 2;
        const corte = [...nome].map((ch, i) => (ch === " " ? i : -1)).filter((i) => i >= 0)
          .reduce((x, y) => (Math.abs(y - meioNome) < Math.abs(x - meioNome) ? y : x));
        r.textContent = "";
        r.append(nome.slice(0, corte), document.createElement("br"), nome.slice(corte + 1));
        r.classList.add("duas-linhas");
        b = ret(r);
        const meio2 = s.top + s.height / 2 - b.height / 2 - b.top;
        const lados2 = [0];
        for (let d = 2; d <= b.width / 2 + s.width / 2 - 8; d += 2) lados2.push(d, -d);
        livre = procurar([...lados2.map((dx) => [dx, 0]), ...lados2.map((dx) => [dx, s.top - 2 - b.bottom]),
          [esq - 4 - b.right, meio2], [dir + 4 - b.left, meio2]]);
        if (!livre) { r.classList.remove("duas-linhas"); r.textContent = nome; b = ret(r); }
      }
      let [dx, dy] = livre || [b.right > c.right - 4 ? c.right - 4 - b.right : b.left < c.left + 4 ? c.left + 4 - b.left : 0, 0];
      if (!livre) {
        for (let k = 0; k < 4; k++) {
          const outro = postos.find((p) => cruza(mover(b, dx, dy), p));
          if (!outro) break;
          dy += outro.bottom - (b.top + dy) + 1;
        }
      }
      if (dx || dy) r.style.transform = `translate(calc(-50% + ${Math.round(dx)}px), ${Math.round(dy)}px)`;
      postos.push(mover(b, dx, dy));
    });
  }

  /** A legenda do mapa grande: só o que o mapa conhecido mostra (os lugares, pelo símbolo de 32) e as marcas (o herói
   *  na plaqueta, a missão, o contrato, o destino bloqueado). */
  const NOMES = { floresta: "floresta", pantano: "pântano", montanha: "montanha", planicie: "planície", ruinas: "ruínas",
    cidadela: "cidadela", vila: "vila", covil: "covil de guardião", vencido: "covil vencido" };
  function legenda(e) {
    if (!e) return "";
    const it = (desenho, nome) => `<span>${desenho} ${nome}</span>`;
    const im = (nome) => `<img class="peca-legenda" ${arquivo(nome)} alt="">`;
    const { missao, contrato } = marcasPorTipo({});
    const desenho = (s) => (NATIVOS.has(s) ? `<img class="sprite desenho pixel peca-legenda" ${arquivo(`mapa-${s}-32`)} alt="">`
      : Icones.lugar(s, 32) || Telas.S(s, 2));
    return [...new Set(e.mapa.nos.map(sprite))].map((s) => it(desenho(s), NOMES[s] || s)).join("") +
      (Retratos.tem(e.heroi.classe) ? it(`<span class="leg-plaqueta">${im("mapa-posicao-20")}<img class="fig" src="${Retratos.url(e.heroi.classe, "figura", 1)}" alt=""></span>`, "você está aqui") : "") +
      (missao.size ? it(im(PECAS.missao[0]), "missão") : "") + (contrato.size ? it(im(PECAS.contrato[0]), "contrato") : "") +
      (e.mapa.nos.some(bloqueado) ? it(im(PECAS.cancela[0]), "destino bloqueado") : "");
  }
  /** O símbolo de um lugar fora do mapa (as opções de viagem, o Diário): o mesmo desenho do minimapa, 1:1, em `lado`
   *  (32: o tamanho de leitura parada da família nova que serve a uma linha de texto sem reduzir o desenho). `n` é um nó do mapa
   *  ou {tipo, bioma}. */
  function simboloHTML(n) {
    const s = simbolo(n, false);
    return s.html.replace("<img ", `<img width="${s.lado}" height="${s.lado}" `).replace('class="', 'class="simbolo-texto ');
  }
  /** As marcas de um lugar fora do mapa: a plaqueta da missão e o cartaz do contrato do minimapa, 1:1 (as peças do
   *  mapa, no lugar do "!" de texto). `quais`: "missao", "contrato" ou os dois, pelo id do lugar no estado. */
  function marcasHTML(id, quais) {
    const { missao, contrato } = marcasPorTipo({});
    const lista = quais ? [quais] : [missao.has(id) && "missao", contrato.has(id) && "contrato"].filter(Boolean);
    const nome = { missao: "objetivo da missão, marcado no mapa", contrato: "contrato aceito, marcado no mapa" };
    return lista.map((m) => `<img class="marca-texto" ${arquivo(PECAS[m][0])} width="9" height="11" alt="${nome[m]}" title="${nome[m][0].toUpperCase() + nome[m].slice(1)}">`).join("");
  }
  return { criar, sprite, legenda, simboloHTML, marcasHTML, ambiente(m) { if (m) ambiente = m; } };
})();
