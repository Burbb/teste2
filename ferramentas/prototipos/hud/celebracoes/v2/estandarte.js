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
