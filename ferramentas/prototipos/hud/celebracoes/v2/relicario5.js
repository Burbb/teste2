/* PROTÓTIPO, direção A5: RELICÁRIO (o A4 aprovado; só a especialização usa as identidades da segunda rodada, versão 1 ou 2) (24/10/2026). O sol de raios e a medalha da A, com o que o Jean pediu:
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
  function festa({ classe, sobre, palavra, numero, titulo, info, pal, som, identidade = null }) {
    const alto = titulo
      ? `<div class="fa2-coroa fa2-centro"><span class="fa2-sobre${identidade ? ` idn-sobre-${identidade}` : ""}">${sobre}</span><b class="fa2-titulo${identidade ? ` idn-${identidade}` : ""}">${titulo}</b></div>`
      : `<div class="fa2-coroa"><span class="fa2-sobre">${sobre}</span>
          <div class="fa2-medalha fa2-centro">${palavra ? `<span class="fa2-palavra">${palavra}</span>` : ""}<span class="fa2-numero">${numero}</span></div></div>`;
    const html = `<div class="festa fa2 ${classe}">${alto}<div class="fa2-info"><i class="fa2-fio"></i>${info}${continuar()}</div></div>`;
    const efeito = (el, caixa) => {
      const p = FX.palco(caixa), enx = FX.enxame(), centro = el.querySelector(".fa2-centro"), inf = el.querySelector(".fa2-info");
      const nome = el.querySelector(".fa2-titulo"), ident = identidade ? (Identidades2.suporta(identidade) && typeof IDENTIDADE_VARIANTE !== "undefined" ? Identidades2.criar(identidade, nome, IDENTIDADE_VARIANTE) : Identidades.criar(identidade, nome)) : null;
      App.som(som);
      const claros = (ident && ident.claros) || ["W", "Y"];
      if (ident && ident.versao === "c") pal = ident.pal;  // as finais trazem a paleta delas (as antigas tinham marrom e roxo)
      const ctl = FX.animar(p, (t, q, parado) => {
        if (ident && ident.antes) ident.antes(p, t, q, parado);
        const m = p.de(centro), R = titulo ? Math.round(Math.min(m.rx, m.ry) * 0.5) : Math.round(m.rx * 0.92);
        const r1 = Math.max(R + 10, p.t(Math.min(innerHeight * 0.7, 600))), abre = parado ? 1 : FX.rampa(t, 0, 520);
        // o fogo: os raios tremulam (um nível a menos de vez em quando) e o calor fica atrás do nome
        const treme = ident && !parado ? ident.treme(q) : 0;
        sol(p, { cx: m.x, cy: m.y, R, r1: R + (r1 - R) * abre, ang: parado ? 0.12 : q * (ident && ident.id === "fogo" ? 0.045 : 0.035), pal, vis: vivo(t, parado) - treme - (ident ? Math.round((ident.atenua || 0) * 1.5) : 0) });  // no Relicário, o sol baixa mais: a identidade conduz
        if (!parado && t < 330) FX.halo(p, { cx: m.x, cy: m.y, r: R * (2.6 - (t / 330) * 1.2), pal: [claros[0], claros[0], claros[1], pal[1]], vis: Math.round(16 * (1 - t / 330)) });
        poco(p, inf);
        if (!(ident && ident.semPocoRotulo)) poco(p, el.querySelector(".fa2-sobre"), 50, 16);  // o rótulo de cima, legível sobre os raios
        if (!titulo) medalha(p, m.x, m.y, R, pal);
        if (ident) ident.quadro(p, t, q, parado);  // a identidade da especialização, em volta do nome
        if (parado) return;
        if (q === 1) faiscas(enx, m.x, m.y, R, 18, [...claros, pal[2], pal[3]]);
        if (q > 10 && q % 5 === 0) cintilar(enx, m.x, m.y, R, r1, [...claros, pal[2]]);
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
    nome: "relicario5",
    nivel: (d) => festa({ classe: "fa2-nivel", sobre: "você subiu de nível", palavra: "Nível", numero: d.nivel, pal: P.ouro, som: "subir",
      info: `${linhaGanhos(d)}${linhaTalento()}${blocoHabs(d.habilidades)}
        ${d.especializacao ? '<p class="fa2-aviso">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</p>' : ""}` }),
    sigilo: (d) => festa({ classe: "fa2-sigilo", sobre: `${h(d.guardiao)} caiu`, palavra: "Sigilo", numero: `${d.sigilos}/3`, pal: P.sigilo, som: "fanfarra",
      info: `<div class="fa2-losangos">${[0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}"></i>`).join("")}</div>
        <p class="fa2-texto">Uma runa ardente se grava na sua mão.</p>${linhaTalento()}` }),
    spec: (d) => festa({ classe: "fa2-spec", sobre: "você agora é", titulo: h(d.nome), som: "fanfarra", identidade: Identidades.qual(d.nome),
      pal: Identidades.PAL[Identidades.qual(d.nome)] || P.arcano,
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
          if (cfg.clarao) FX.claraoLocal(p, { cx: a.x, cy: a.y, r: R * 4, t, dur: 220, espalha: 2, pal: ["W", "Y", "Y", "O"] });
          FX.poco(p, { cx: a.x, cy: a.y, rx: R + 5, ry: R + 5, forca: 16 });
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
  #celebracao.dir-relicario5 { background: rgba(4, 3, 2, 0.9); }
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
  .fa2 kbd, .dir-relicario5 kbd { font: 13px/1 var(--num); color: #c0b8a8; border: 1px solid #4a4d53; background: #0b0c0e; padding: 2px 5px; margin-left: 4px; }
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
  :root body #sobre-achado.dir-relicario5 { background: rgba(4, 3, 2, 0.88); }
  :root body #sobre-achado.dir-relicario5 .janela-achado { position: relative; z-index: 1; background: none; border: 0; box-shadow: none; padding: 0;
    max-height: none; overflow: visible; width: min(900px, 96vw); }
  :root body #sobre-achado .fa2-achado.tela.achado { display: flex; flex-direction: column; align-items: center; gap: 12px; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo { display: flex; flex-direction: column; align-items: center; gap: 8px; width: auto;
    background: none; border: 0; box-shadow: none; padding: 0; overflow: visible; animation: none; }
  :root body #sobre-achado .fa2-achado .achado-cartao.novo .achado-arte { width: 64px; height: 64px; margin: 0; }
  .fa2-cabeca { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .fa2-altar { display: grid; place-items: center; height: 150px; }
  #sobre-achado.dir-relicario5:is(.rar-comum, .rar-magico) .fa2-altar { height: 84px; }
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
  .dir-relicario5 .achado-acoes { display: flex; justify-content: center; gap: 10px; margin-top: 16px; }
  .dir-relicario5.entrando .fa2-altar .achado-arte { animation: fa2-desce 0.27s steps(4) both; }
  @keyframes fa2-desce { from { translate: 0 -40px; } 75% { translate: 0 3px; } to { translate: 0 0; } }
  .dir-relicario5.adiantado .fa2-altar .achado-arte { animation: none; }

  /* os botões destas apresentações: ferro escuro com aresta de latão, sem o cinza em degradê; o foco do teclado
     num anel claro; a área, os estados e as teclas iguais */
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)) { border: 1px solid #6b5426; border-radius: 0;
    background: #120e0b; color: #eadbb4; text-shadow: 0 1px 0 #000; font: 700 17px/1.1 var(--texto); padding: 9px 16px 9px 12px; min-width: 0;
    box-shadow: inset 0 1px 0 #3a2c18, inset 0 -2px 0 #070504, 0 0 0 1px #000, 0 3px 0 #000; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):hover { border-color: #d4af37; background: #1d1610; color: #fff3d6; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):focus-visible { border-color: #f2d27a; color: #fff3d6; outline: 2px solid #f2d27a; outline-offset: 3px; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela:not(.reserva)):active { translate: 0 1px; box-shadow: inset 0 1px 0 #2b2219, 0 0 0 1px #000, 0 2px 0 #000; }
  :root body :is(#celebracao, #sobre-achado).dir-relicario5 :is(.continuar, .botao-janela) kbd { font: 13px/1 var(--num); color: #f2d27a; border: 1px solid #6b5426; background: #070504; padding: 2px 5px; margin: 0 2px; }
  /* o mágico: um acento azul parado junto do item (o fio com o losango, em azul), sem aura */
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte { position: relative; }
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte::after { content: ""; position: absolute; left: 50%; bottom: -10px; width: 64px; height: 3px;
    translate: -50% 0; background: #3d63c9; box-shadow: 0 1px 0 #000; }
  #sobre-achado.dir-relicario5.rar-magico .achado-cartao.novo .achado-arte::before { content: ""; position: absolute; left: 50%; bottom: -14px; width: 4px; height: 4px; z-index: 1;
    translate: -2px 0; background: #c8e0ff; box-shadow: -2px 2px 0 #7fb0ff, 2px 2px 0 #7fb0ff, 0 4px 0 #c8e0ff, 0 2px 0 #3d63c9; }
  @media (max-height: 760px) {
    .fa2-coroa { gap: 14px; margin-bottom: 14px; } .fa2-medalha { width: 128px; height: 128px; } .fa2-numero { font-size: 64px; }
    .fa2-titulo { font-size: 70px; } .fa2-info { gap: 10px; } .fa2-hab b { font-size: 24px; } .fa2-hab p { font-size: 15px; }
    .fa2-altar { height: 112px; } .ficha-nome { font-size: 32px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .fa2 :is(.fa2-medalha, .fa2-titulo, .fa2-info), .dir-relicario5 .fa2-altar .achado-arte { animation: none !important; }
  }`;
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-relicario5">${css}</style>`);
  Festa.usar(direcao);
})();
