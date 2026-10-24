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
