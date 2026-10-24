/* PROTÓTIPO, direção B2: ESTOURO REFINADO (24/10/2026). O golpe da B (clarão, tremor, anéis, linhas de velocidade,
   estilhaços) com o que o Jean pediu:
   - o selo do impacto com miolo escuro e aro de ouro (a mesma silhueta de pontas): o número em ouro lê no escuro, sem
     o contorno grosso; a fita vermelha virou uma faixa de ferro com fios de latão, reta;
   - a informação sem caixas: os ganhos numa linha, o ponto de talento e a habilidade lado a lado, um fio entre eles;
     o efeito passa por trás num poço escuro; o Continuar dos botões do jogo;
   - a especialização com o nome como protagonista (o estouro atrás do nome, sem o selo);
   - o achado em composição horizontal: o item no tamanho de uso (64) no selo, ao lado da ficha (o nome, a raridade,
     o prêmio, a troca e o que você usa); o comum pousa com poeira, sem aura; o mágico tem um estalo breve e local;
   - depois do impacto, o efeito continua mais baixo: o selo respira, um pulso fino a cada 2,2 s e poucas brasas. */
"use strict";

(() => {
  const { h, ganhos, talento, habilidades, continuar, fichaItem, arteItem } = Festa;
  const P = FX.PALETAS;
  const CACOS = ["lasca", "caco", "cruz", "duplo", "ponto"];
  // o selo: miolo, meio, aro, luz do aro (por paleta de festa)
  const SELO = { ouro: ["z", "j", "c", "Y"], sigilo: ["z", "D", "r", "O"], arcano: ["z", "x", "m", "M"],
    raro: ["z", "j", "c", "Y"], lendario: ["z", "D", "o", "O"], magico: ["z", "v", "u", "U"] };

  function estilhacos(enx, cx, cy, r, n, pal, forca = 1) {
    enx.soltar(n, (i) => {
      const a = FX.aleatorio(0, Math.PI * 2), v = FX.aleatorio(2.5, 6.5) * forca;
      return { x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r * 0.8, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 2.2 * forca,
        g: 0.36, arrasto: 0.97, vida: Math.round(FX.aleatorio(18, 32)), desenho: CACOS[i % CACOS.length], pal, piscar: i % 5 === 0 };
    });
  }
  const brasas = (enx, cx, cy, larg, pal) => enx.soltar(1, () => ({ x: cx + Math.round(FX.aleatorio(-larg, larg)), y: cy,
    vx: FX.aleatorio(-0.3, 0.3), vy: FX.aleatorio(-1.4, -0.7), vida: Math.round(FX.aleatorio(12, 20)), desenho: Math.random() < 0.3 ? "cruz" : "brasa", pal }));

  /** O golpe (clarão, anéis, linhas de velocidade) e, depois, a sustentação (um pulso fino de tempos em tempos). */
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
    const tp = (t - 1200) % 2200;
    if (t > 1200 && tp < 460) FX.anel(p, { cx, cy, r: r + Math.round((tp / 460) * p.t(130)), esp: 1, pal: [pal[1], pal[2], pal[3]], achata: 0.62, rastro: 3, vis: Math.round(10 * (1 - tp / 460)) });
  }
  /** O selo: a aura de raios curtos atrás (girando devagar; mais baixa depois do golpe) e a estrela de miolo escuro. */
  function selo(p, { cx, cy, re, q, t, pal, cores, quieto, pontas = 14, aura = 1.6 }) {
    const resp = quieto ? 0 : (q >> 1) % 2, vis = quieto ? 12 : Math.round(FX.rampa(t, 900, 800, 16, 11));
    FX.raios(p, { cx, cy, n: 16, ang: 0.2 + (quieto ? 0 : q * 0.012), larg: 0.3, r0: Math.round(re * 0.7), r1: Math.round(re * aura), pal: pal.slice(1), esbate: 0.32, achata: 0.85, vis });
    FX.estrela(p, { cx, cy, pontas, ri: Math.round(re * 0.74) + resp, re: re + resp, pal, cores });
  }
  function poco(p, el, folga = 80, forca = 16) {
    if (!el) return;
    const i = p.de(el);
    FX.poco(p, { cx: i.x, cy: i.y, rx: i.rx + p.t(folga), ry: i.ry + p.t(folga * 0.55), forca });
  }

  function festa({ classe, faixa, palavra, numero, titulo, info, pal, cores, som }) {
    const alto = titulo
      ? `<div class="fb2-impacto fb2-titulo-alto"><div class="fb2-faixa"><span>${faixa}</span></div><b class="fb2-titulo">${titulo}</b></div>`
      : `<div class="fb2-impacto"><div class="fb2-numero">${palavra ? `<small>${palavra}</small>` : ""}<b>${numero}</b></div></div>
         <div class="fb2-faixa"><span>${faixa}</span></div>`;
    const html = `<div class="festa fb2 ${classe}">${alto}<div class="fb2-info">${info}${continuar()}</div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), alvo = el.querySelector(titulo ? ".fb2-titulo" : ".fb2-impacto"), inf = el.querySelector(".fb2-info");
      App.som(som);
      FX.tremer(8);
      const ctl = FX.animar(p, (t, q, parado) => {
        const c = p.de(alvo), baixa = innerHeight < 760;
        const re = titulo ? Math.round(c.rx * 0.6) : p.t(baixa ? 100 : 128);
        if (titulo) {  // a especialização: o estouro atrás do nome, sem o selo
          const vis = parado ? 14 : Math.round(FX.rampa(t, 900, 800, 16, 13));
          FX.raios(p, { cx: c.x, cy: c.y, n: 22, ang: 0.1 + (parado ? 0 : q * 0.01), larg: 0.32, r0: Math.round(c.ry * 0.5), r1: Math.round(c.rx * 1.7), pal: pal.slice(1), esbate: 0.4, achata: 0.55, vis, alterna: 0.6 });
        } else selo(p, { cx: c.x, cy: c.y, re, q, t, pal, cores, quieto: parado });
        poco(p, inf);
        if (parado) return;
        golpe(p, { cx: c.x, cy: c.y, r: titulo ? Math.round(c.ry) : re, t, pal });
        if (q === 1) estilhacos(enx, c.x, c.y, (titulo ? c.ry : re) * 0.8, 40, ["W", "Y", pal[2], "o", "r", "D"]);
        if (q > 8 && q % 3 === 0) brasas(enx, c.x, c.y + Math.round((titulo ? c.ry : re) * 0.7), titulo ? c.rx : re, ["Y", "O", "o", "r", "D"]);
        if (q > 12 && q % 9 === 0) { const a = FX.aleatorio(0, Math.PI * 2), rr = titulo ? c.rx * 0.8 : re; enx.soltar(1, () => ({ x: c.x + Math.cos(a) * rr, y: c.y + Math.sin(a) * rr * (titulo ? 0.5 : 1), vx: 0, vy: 0, vida: 7, desenho: "brilho", pal: ["W", "Y", pal[2]] })); }
        enx.passo(); enx.desenhar(p);
      });
      return { parar: ctl.parar, revelar: () => { ctl.pular(700); el.classList.add("pulou"); } };
    };
    return { html, efeito };
  }

  const linhaGanhos = (d) => `<div class="fb2-ganhos">${ganhos(d).map((x, i) => `<span class="fb2-ganho" style="--i:${i}">${x.icone}<b>+${x.v}</b><span>${h(x.k)}</span></span>`).join("")}</div>`;
  const talentoHTML = () => `<div class="fb2-talento">${talento(32)}<div><b>+1</b> ponto de talento<small>no livro de Talentos <kbd>T</kbd></small></div></div>`;
  const habsHTML = (lista) => habilidades(lista).map((x) => `<div class="fb2-hab"><span class="fb2-hab-icone">${x.icone}</span>
    <div><span class="fb2-rotulo">nova habilidade</span><b>${x.nome}</b><p>${x.desc}</p></div></div>`).join("");
  /** O talento e as habilidades lado a lado, com um fio entre eles. */
  const lado = (esq, dir) => (dir ? `<div class="fb2-lado"><div class="fb2-lado-esq">${esq}</div><div class="fb2-lado-dir">${dir}</div></div>` : `<div class="fb2-lado so">${esq}</div>`);

  const direcao = {
    nome: "estouro2",
    nivel: (d) => festa({ classe: "fb2-nivel", faixa: "Você subiu de nível", palavra: "Nível", numero: d.nivel, pal: P.ouro, cores: SELO.ouro, som: "subir",
      info: `${linhaGanhos(d)}${lado(talentoHTML(), habsHTML(d.habilidades))}
        ${d.especializacao ? '<p class="fb2-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</p>' : ""}` }),
    sigilo: (d) => festa({ classe: "fb2-sigilo", faixa: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, cores: SELO.sigilo, som: "fanfarra",
      info: `${lado(`<div class="fb2-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div><p class="fb2-texto">Uma runa ardente se grava na sua mão.</p>`, talentoHTML())}` }),
    spec: (d) => festa({ classe: "fb2-spec", faixa: "Você agora é", titulo: h(d.nome), pal: P.arcano, cores: SELO.arcano, som: "fanfarra",
      info: `<p class="fb2-texto">${h(d.desc)}</p><div class="fb2-habs">${habsHTML(d.habilidades)}</div>` }),

    achado(d) {
      const f = fichaItem(d);
      return `<div class="tela achado fb2-achado rar-${f.rar}">
        <div class="achado-cartao novo rar-${f.rar}">
          <div class="fb2-selo-item"><div class="achado-arte">${arteItem(d.item, 64)}</div></div>
          <div class="fb2-cabeca"><span class="achado-selo">Você encontrou</span>${f.raridade}${f.nome}</div>
        </div>
        <div class="fb2-ficha${f.compara ? " compara" : ""}">${f.premio}${f.troca}${f.usa ? `<div class="fb2-usa">${f.usa}</div>` : ""}</div>
        ${f.lore}${f.aviso}</div>`;
    },
    GOLPE: {
      comum: null,
      magico: { pal: P.magico, cores: SELO.magico },
      raro: { pal: P.raro, cores: SELO.raro, coluna: 4, tremor: 4, cacos: 22, forte: false, re: 70 },
      lendario: { pal: P.lendario, cores: SELO.lendario, coluna: 7, tremor: 10, cacos: 44, forte: true, re: 86 },
    },
    async cerimonia({ fundo, janela, d, parado, esperar, adiantou }) {
      const rar = d.item.raridade, cfg = direcao.GOLPE[rar], p = FX.palco(fundo), enx = FX.enxame();
      const arte = janela.querySelector(".achado-cartao.novo .achado-arte"), info = janela.querySelector(".fb2-ficha"), cabeca = janela.querySelector(".fb2-cabeca");
      const queda = cfg && cfg.coluna && !parado && !FX.reduzido() ? 160 : 0;
      fundo.classList.add("entrando");
      if (FX.reduzido() || parado || !queda) fundo.classList.add("bateu");
      if (!parado && !queda) App.som(rar === "comum" ? "achado" : "achado_raro");
      let bateu = !queda;
      FX.animar(p, (t, q, quieto) => {
        const a = p.de(arte), R = Math.round(a.rx), ti = t - queda;
        if (!quieto && !bateu && (ti >= 0 || adiantou())) { bateu = true; App.som("achado_raro"); FX.tremer(cfg.tremor); fundo.classList.add("bateu"); }
        poco(p, info, 50, 15); poco(p, cabeca, 40, 14);
        if (cfg && cfg.coluna) {
          const re = p.t(cfg.re);
          if (quieto || bateu) selo(p, { cx: a.x, cy: a.y, re, q, t: Math.max(0, ti), pal: cfg.pal, cores: cfg.cores, quieto, aura: rar === "lendario" ? 2.3 : 1.8 });
          if (!quieto) {
            if (ti < 0) FX.coluna(p, { cx: a.x, base: Math.round(a.y * FX.rampa(t, 0, queda)), larg: cfg.coluna, pal: ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]], q });
            else if (ti < 600) FX.coluna(p, { cx: a.x, base: a.y, larg: Math.max(1, Math.round(cfg.coluna * (1 - ti / 600))), pal: ["W", cfg.pal[1], cfg.pal[2], cfg.pal[3]], q, vis: Math.round(16 * (1 - ti / 600)) });
            if (bateu) {
              golpe(p, { cx: a.x, cy: a.y, r: re, t: Math.max(0, ti), pal: cfg.pal, forte: cfg.forte });
              if (Math.round(Math.max(0, ti) / FX.QUADRO) === 1) estilhacos(enx, a.x, a.y, re * 0.7, cfg.cacos, ["W", "Y", cfg.pal[2], cfg.pal[3], cfg.pal[4]], cfg.forte ? 1.2 : 0.8);
              if (rar === "lendario" && q % 3 === 0) brasas(enx, a.x, a.y + re, re * 1.4, ["Y", "O", "o", "r", "D"]);
            }
          }
        } else if (!quieto && rar === "magico") {
          // um estalo breve e local: o selo pisca dois quadros, um anel curto e faíscas; depois, nada fica
          if (q < 3) FX.estrela(p, { cx: a.x, cy: a.y, pontas: 10, ri: R + 4, re: R + p.t(22), pal: cfg.pal, cores: ["v", "u", "U", "W"] });
          if (t < 520) FX.anel(p, { cx: a.x, cy: a.y, r: R + Math.round(FX.rampa(t, 0, 520) * p.t(70)), esp: 2, pal: ["W", "U", "u"], achata: 0.8, rastro: 3, vis: Math.round(14 * (1 - t / 520)) });
          if (q === 1) estilhacos(enx, a.x, a.y, R * 0.8, 10, ["W", "M", "U", "u"], 0.5);
        } else if (!quieto && q === 2) {
          // comum: pousa e levanta poeira
          enx.soltar(14, (i) => ({ x: a.x + FX.aleatorio(-R, R), y: a.y + R - 1, vx: (i % 2 ? 1 : -1) * FX.aleatorio(0.5, 2.2), vy: FX.aleatorio(-1.4, -0.3),
            g: 0.12, arrasto: 0.92, vida: Math.round(FX.aleatorio(10, 16)), desenho: i % 3 ? "ponto" : "duplo", pal: ["w", "G", "g", "d"] }));
        }
        if (!quieto) { enx.passo(); enx.desenhar(p); }
      });
      if (parado) return;
      await esperar({ comum: 220, magico: 300, raro: 440, lendario: 580 }[rar] || 300);
    },
  };

  const css = `
  /* ---- B2: Estouro refinado ---- */
  #celebracao.dir-estouro2 { background: rgba(6, 3, 2, 0.92); }
  .festa.fb2 { position: relative; z-index: 1; display: flex; flex-direction: column; align-items: center; width: min(940px, 96vw);
    background: none; border: 0; box-shadow: none; padding: 0; text-align: center; }
  .fb2-impacto { width: 320px; height: 270px; display: grid; place-items: center; }
  .fb2-numero { display: flex; flex-direction: column; align-items: center; animation: fb2-bate 0.27s steps(1) both; }
  .fb2-numero small { font: 20px/1 var(--titulo); color: #c0b8a8; text-shadow: 2px 2px 0 #000; }
  .fb2-numero b { font: 96px/0.9 var(--titulo); color: #ffe27a; text-shadow: 0 4px 0 #8a6a14, 0 8px 0 #000; }
  .fb2-sigilo .fb2-numero b { font-size: 60px; color: #ffb35c; text-shadow: 0 4px 0 #6e0d0d, 0 8px 0 #000; }
  @keyframes fb2-bate { 0% { scale: 2.1; } 25% { scale: 0.86; } 50% { scale: 1.08; } 75%, 100% { scale: 1; } }
  /* a faixa: ferro escuro com fios de latão, reta */
  .fb2-faixa { margin: 4px 0 18px; animation: fb2-abre 0.2s 0.07s steps(3) both; }
  .fb2-faixa span { display: inline-block; padding: 7px 30px 6px; font: 700 15px/1 var(--texto); letter-spacing: 0.32em; text-transform: uppercase; color: #f2d27a;
    background: #120d0a; border-top: 2px solid #8a6a14; border-bottom: 2px solid #8a6a14; box-shadow: 0 -1px 0 #000, 0 1px 0 #000, inset 0 2px 0 #2b2219; }
  @keyframes fb2-abre { from { clip-path: inset(0 50% 0 50%); } to { clip-path: inset(0 0 0 0); } }
  .fb2-titulo-alto { width: auto; height: auto; padding: 46px 0 34px; display: flex; flex-direction: column; align-items: center; }
  .fb2-titulo-alto .fb2-faixa { margin: 0 0 10px; }
  .fb2-titulo { font: 400 96px/1 var(--titulo); color: #f1e4ff; text-shadow: 0 4px 0 #5a2a6e, 0 8px 0 #000; animation: fb2-bate 0.27s steps(1) both; }
  .fb2-info { display: flex; flex-direction: column; align-items: center; gap: 16px; width: 100%; }
  .fb2-ganhos { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px 0; }
  .fb2-ganho { display: inline-flex; align-items: center; gap: 6px; padding: 0 14px; position: relative; animation: fb2-estala 0.2s calc(0.2s + var(--i, 0) * 0.06s) steps(1) both; }
  .fb2-ganho + .fb2-ganho::before { content: ""; position: absolute; left: -2px; top: 50%; width: 4px; height: 4px; translate: 0 -2px; background: #8a6a14; }
  .fb2-ganho b { font: 36px/1 var(--titulo); color: #8fbf6a; text-shadow: 0 3px 0 #1f4a25, 0 5px 0 #000; }
  .fb2-ganho > span { font: 700 12px/1 var(--texto); letter-spacing: 0.16em; text-transform: uppercase; color: #c0b8a8; }
  @keyframes fb2-estala { 0% { scale: 1.3; } 34% { scale: 0.94; } 67%, 100% { scale: 1; } }
  .fb2-lado { display: grid; grid-template-columns: auto auto; align-items: start; gap: 0; max-width: 860px; text-align: left; }
  .fb2-lado.so { display: flex; justify-content: center; }
  .fb2-lado-esq { padding-right: 24px; } .fb2-lado-dir { padding-left: 24px; border-left: 1px solid #3a3128; }
  .fb2-talento { display: flex; align-items: center; gap: 10px; font: 19px/1.15 var(--texto); color: #f2d27a; }
  .fb2-talento b { font: 32px/1 var(--titulo); color: #fff3a0; text-shadow: 0 3px 0 #8a6a14, 0 5px 0 #000; }
  .fb2-talento small { display: block; font: 13px/1.4 var(--texto); color: #a89878; }
  .fb2 kbd, .dir-estouro2 kbd { font: 13px/1 var(--num); color: #c0b8a8; border: 1px solid #4a4d53; background: #0b0c0e; padding: 2px 5px; margin-left: 4px; }
  .fb2-hab { display: flex; align-items: flex-start; gap: 12px; max-width: 520px; }
  .fb2-habs { display: flex; flex-direction: column; gap: 12px; text-align: left; }
  .fb2-hab-icone { flex: none; display: grid; place-items: center; width: 44px; height: 44px; margin-top: 4px; background: #120c1a; box-shadow: inset 0 0 0 1px #5a2a6e; }
  .fb2-hab b { display: block; font: 28px/1.05 var(--titulo); color: #e4d8ff; text-shadow: 0 3px 0 #2a1d3a, 0 5px 0 #000; }
  .fb2-hab p { margin: 3px 0 0; font: 16px/1.4 var(--texto); color: #e8dcbe; }
  .fb2-rotulo { font: 700 11px/1 var(--texto); letter-spacing: 0.24em; text-transform: uppercase; color: #8e6fd8; }
  .fb2-aviso { margin: 0; font: italic 16px/1.4 var(--texto); color: #c8b0ff; }
  .fb2-texto { margin: 0; max-width: 640px; font: 17px/1.45 var(--texto); color: #e8dcbe; }
  .fb2-losangos { display: flex; gap: 14px; margin: 4px 0 8px; } .fb2-losangos i { width: 16px; height: 16px; rotate: 45deg; border: 3px solid #6e0d0d; background: #17120f; }
  .fb2-losangos i.tem { background: #e2574c; border-color: #ffb35c; }
  :root body .fb2 .continuar { margin-top: 4px; display: inline-flex; align-items: center; gap: 6px; }
  .fb2.pulou :is(.fb2-numero, .fb2-faixa, .fb2-ganho, .fb2-titulo) { animation: none; }

  /* o achado: o item no selo, ao lado da ficha */
  :root body #sobre-achado.dir-estouro2 { background: rgba(6, 3, 2, 0.9); }
  :root body #sobre-achado.dir-estouro2 .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0; max-height: none; overflow: visible; width: min(1100px, 96vw); }
  :root body #sobre-achado .fb2-achado.tela.achado { display: grid; grid-template-columns: auto 1fr; grid-template-areas: "novo novo" "ficha ficha" "lore lore"; justify-items: center; gap: 12px 0; }
  :root body #sobre-achado .fb2-achado .achado-cartao.novo { grid-area: novo; display: flex; align-items: center; gap: 40px; width: auto; background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  :root body #sobre-achado .fb2-achado .achado-cartao.novo .achado-arte { width: 64px; height: 64px; margin: 0; }
  .fb2-selo-item { display: grid; place-items: center; width: 190px; height: 190px; }
  #sobre-achado.dir-estouro2:is(.rar-comum, .rar-magico) .fb2-selo-item { width: 84px; height: 84px; }
  .fb2-cabeca { display: flex; flex-direction: column; align-items: flex-start; gap: 8px; text-align: left; max-width: 640px; }
  :root body #sobre-achado .fb2-achado .achado-cartao.novo .achado-selo { font: 700 13px/1 var(--texto); letter-spacing: 0.32em; text-transform: uppercase; color: #f2d27a; }
  .dir-estouro2 .ficha-raridade { display: inline-block; padding: 4px 14px 3px; font: 700 13px/1 var(--texto); letter-spacing: 0.26em; text-transform: uppercase; color: #120d0a; }
  .dir-estouro2 .ficha-raridade.rar-comum { background: #8a8070; } .dir-estouro2 .ficha-raridade.rar-magico { background: #7fb0ff; }
  .dir-estouro2 .ficha-raridade.rar-raro { background: #f2c94c; } .dir-estouro2 .ficha-raridade.rar-lendario { background: #ffb35c; }
  .dir-estouro2 .ficha-nome { display: block; font: 400 40px/1.05 var(--titulo); text-shadow: 0 3px 0 #000; text-wrap: balance; }
  .dir-estouro2 .ficha-nome.r-comum { color: #f1e4c4; }
  .fb2-ficha { grid-area: ficha; display: grid; grid-template-columns: 1fr; justify-items: center; gap: 0 26px; padding-top: 12px; min-width: min(760px, 92vw); border-top: 1px solid #3a3128; }
  .fb2-ficha.compara { grid-template-columns: 1fr auto 1fr; align-items: start; justify-items: stretch; }
  .fb2-ficha .ficha-premio { display: flex; flex-direction: column; gap: 3px; align-items: center; }
  .fb2-ficha.compara .ficha-premio { align-items: flex-end; text-align: right; }
  .dir-estouro2 .ficha-rotulo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .dir-estouro2 .ficha-linhas { display: flex; flex-direction: column; font: 19px/1.25 var(--num, var(--texto)); color: #f1e4c4; }
  .dir-estouro2 .ficha-linhas .efeito { color: #c8b0ff; font-size: 16px; }
  .fb2-ficha > .ficha-troca { display: flex; flex-direction: column; align-items: center; padding: 0 22px; border-left: 1px solid #3a3128; border-right: 1px solid #3a3128; font: 17px/1.3 var(--num, var(--texto)); }
  .dir-estouro2 .ficha-troca .melhor { color: #8fbf6a; } .dir-estouro2 .ficha-troca .pior { color: #e2574c; }
  .fb2-usa { display: flex; flex-direction: column; gap: 10px; }
  :root body #sobre-achado .fb2-usa .achado-cartao.atual { width: auto; padding: 0; background: none; border: 0; box-shadow: none; text-align: left; overflow: visible; animation: none; opacity: 0.92; }
  .fb2-usa .achado-selo { font: 700 11px/1.4 var(--texto); letter-spacing: 0.22em; text-transform: uppercase; color: #8a8070; }
  .dir-estouro2 .ficha-usa-nome { display: flex; align-items: center; gap: 8px; } .dir-estouro2 .ficha-usa-nome b { font: 400 22px/1.05 var(--titulo); }
  .fb2-usa .ficha-troca { display: flex; flex-direction: column; font-size: 15px; }
  .dir-estouro2 .ficha-lore { grid-area: lore; max-width: 640px; font: italic 15px/1.4 var(--texto); color: #a89878; }
  .dir-estouro2 .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 16px; }
  :root body #sobre-achado.dir-estouro2.entrando:is(.rar-raro, .rar-lendario):not(.bateu):not(.adiantado) .fb2-selo-item > * { visibility: hidden; }
  .dir-estouro2.bateu .fb2-selo-item .achado-arte, .dir-estouro2.entrando:is(.rar-comum, .rar-magico) .fb2-selo-item .achado-arte { animation: fb2-pousa 0.27s steps(1) both; }
  @keyframes fb2-pousa { 0% { translate: 0 -18px; } 34% { translate: 0 3px; } 67%, 100% { translate: 0 0; } }
  @media (max-height: 760px) {
    .fb2-impacto { width: 260px; height: 210px; } .fb2-numero b { font-size: 76px; } .fb2-faixa { margin-bottom: 12px; }
    .fb2-titulo { font-size: 72px; } .fb2-titulo-alto { padding: 28px 0 22px; } .fb2-info { gap: 10px; }
    .fb2-hab b { font-size: 24px; } .fb2-hab p { font-size: 15px; } .fb2-selo-item { width: 180px; height: 170px; } .dir-estouro2 .ficha-nome { font-size: 32px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fb2 :is(.fb2-numero, .fb2-faixa, .fb2-ganho, .fb2-titulo), .dir-estouro2 .fb2-selo-item .achado-arte { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-estouro2">${css}</style>`);
  Festa.usar(direcao);
})();
