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
