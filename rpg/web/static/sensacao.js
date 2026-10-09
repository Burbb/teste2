/* Sensação: o peso dos momentos do jogo. As telas (batalha.js, telas/) dizem O QUE aconteceu; aqui mora
   COMO aquilo se sente: quanto o tempo para no impacto, quanto a arena treme, como a câmera chega perto do
   golpe que encerra a luta. Os números ficam todos em AJUSTES, para afinar sem caçar setTimeout pelo código.

   O motor marca os fatos no lance do golpe (crit, abate, final); quem anima só pergunta Sensacao.golpe(). */
"use strict";

const Sensacao = (() => {
  const AJUSTES = {
    // Quanto tempo tudo congela no quadro do impacto (hit-stop, como em Hades e Dead Cells), em ms. O golpe final
    // não congela: tem câmera lenta (abaixo).
    parada: { critico: 80, abate: 70 },
    // Quanto a arena treme, em px (e por quanto tempo, em ms).
    tremor: { leve: 3, critico: 5, abate: 7, final: 11 },
    tremorMs: 340,
    // O golpe final: em vez de congelar, o tempo da arena desacelera enquanto o golpe chega (ritmo `lento`, em
    // `entradaMs`), segue devagar no choque (`seguraMs`) e volta acelerando (`saidaMs`). A câmera chega perto de
    // quem cai em tempo real, e o resto escurece.
    final: { lento: 0.3, entradaMs: 220, seguraMs: 380, saidaMs: 450, zoom: 1.08, zoomMs: 520 },
    // Números que contam subindo (ouro do espólio): duração e o máximo de tiques de som.
    contarMs: 650, tiquesMax: 10,
    // A barra de XP enchendo (por trecho de nível) e quanto o espólio fica na tela depois de tudo.
    barraMs: 700, espolioEsperaMs: 450, espolioEntreMs: 180, espolioFicaMs: 900, espolioAchadoMs: 350,
    // Vida por um fio: o compasso do pulso (ms entre batidas), mais rápido quanto mais perto do fim, e quantas
    // vezes o coração soa ao entrar na faixa (depois só a tela pulsa: som contínuo cansa e angustia).
    batimentoLentoMs: 1150, batimentoRapidoMs: 700, batidasAoEntrar: 3,
    // Saque com cerimônia: por raridade, quanto o feixe de luz demora antes de o cartão aparecer (sem entrada,
    // o item aparece direto). O lendário ainda ganha um clarão na tela inteira.
    saque: { raro: { ms: 1000 }, lendario: { ms: 1400, clarao: true } },
  };
  // O que pesa mais, quando vários golpes caem de uma vez (uma salva em área): o mais pesado dá o tom.
  const ORDEM = ["final", "abate", "critico"];

  let rapido = () => false, pausa = (ms) => ms;
  function configurar(opts) { rapido = opts.rapido; pausa = opts.pausa; }
  const dormir = (ms) => (ms > 0 ? new Promise((r) => setTimeout(r, ms)) : Promise.resolve());

  /** O peso de um golpe pelo que o motor diz dele: o golpe que encerra a luta, o que derruba, o crítico. */
  function peso(m) { return m.final ? "final" : m.abate ? "abate" : m.crit ? "critico" : null; }
  function maisPesado(lances) {
    let melhor = null, nivel = ORDEM.length;
    for (const x of lances) {
      const i = ORDEM.indexOf(peso(x));
      if (i >= 0 && i < nivel) { melhor = x; nivel = i; }
    }
    return melhor;
  }

  /** A arena treme: de um lado para o outro, cada vez menos. */
  function tremor(palco, px, ms = AJUSTES.tremorMs) {
    if (rapido() || !palco || !px) return;
    const passos = [];
    for (let i = 0; i <= 8; i++) {
      const f = px * (1 - i / 8);
      passos.push({ translate: `${(i % 2 ? -1 : 1) * f}px ${(i % 3 - 1) * f * 0.4}px` });
    }
    palco.animate(passos, { duration: pausa(ms), easing: "linear" });
  }

  /** Tudo congela um instante no quadro do impacto; quem levou o golpe pisca em branco. */
  async function parada(palco, alvo, ms) {
    if (rapido() || !palco || !ms) return;
    palco.classList.add("parado");
    if (alvo) alvo.classList.add("lampejo");
    await dormir(pausa(ms));
    palco.classList.remove("parado");
    if (alvo) alvo.classList.remove("lampejo");
  }

  /* ------------------------------------------------------------ o relógio da arena */
  // Na câmera lenta o tempo da arena anda devagar: as animações dela (as que estão rodando e as que nascerem) e os
  // prazos que a batalha marca com depois() (tirar o tremor da carta, sumir com o número), para nada ser cortado no
  // meio. Fora dela, tudo anda a 1 e depois() é um setTimeout comum. A câmera (TEMPO_REAL) anda no tempo de fora.
  const TEMPO_REAL = "tempo-real";
  let ritmo = 1, palcoLento = null, quadro = null, ultimo = 0;
  const prazos = new Set();
  function tique(t) {
    const dt = t - ultimo;
    ultimo = t;
    if (palcoLento) {
      for (const a of palcoLento.getAnimations({ subtree: true })) if (a.id !== TEMPO_REAL && a.playbackRate !== ritmo) a.playbackRate = ritmo;
    }
    for (const p of [...prazos]) { p.resta -= dt * ritmo; if (p.resta <= 0) { prazos.delete(p); p.fn(); } }
    quadro = palcoLento || prazos.size ? requestAnimationFrame(tique) : null;
  }
  function andar() { if (!quadro) { ultimo = performance.now(); quadro = requestAnimationFrame(tique); } }
  /** Faz `fn` depois de `ms` do tempo da arena. */
  function depois(ms, fn) {
    if (!palcoLento) return setTimeout(fn, ms);
    prazos.add({ resta: ms, fn });
    andar();
  }
  /** Leva o ritmo da arena até `alvo` em `ms` (tempo de fora), suave. Voltando a 1, a arena se solta. */
  function mudarRitmo(palco, alvo, ms, curva = (k) => 1 - (1 - k) * (1 - k)) {
    palcoLento = palco;
    andar();
    const de = ritmo, t0 = performance.now();
    return new Promise((fim) => {
      const passo = (t) => {
        const k = ms > 0 ? Math.min(1, (t - t0) / ms) : 1;
        ritmo = de + (alvo - de) * curva(k);
        if (k < 1) return requestAnimationFrame(passo);
        if (alvo === 1) soltar();
        fim();
      };
      requestAnimationFrame(passo);
    });
  }
  function soltar() {
    for (const a of palcoLento.getAnimations({ subtree: true })) if (a.id !== TEMPO_REAL) a.playbackRate = 1;
    palcoLento = null;
    ritmo = 1;
    for (const p of prazos) setTimeout(p.fn, Math.max(0, p.resta));  // o que faltava, agora em tempo normal
    prazos.clear();
  }

  /* ------------------------------------------------------------ o golpe final */
  // Câmera lenta, como nos jogos de luta: o tempo desacelera enquanto o golpe chega (a investida, a flecha no ar),
  // segue devagar no choque e volta acelerando; a câmera chega perto de quem cai e o resto escurece. Nada para de
  // vez: congelar a tela no impacto parecia o jogo travando.
  let foco = null;
  function aproximar(palco, alvo) {
    if (foco) return;
    const cfg = AJUSTES.final;
    const p = palco.getBoundingClientRect(), a = alvo.getBoundingClientRect();
    palco.style.transformOrigin = `${a.left + a.width / 2 - p.left}px ${a.top + a.height / 2 - p.top}px`;
    palco.classList.add("foco-final");
    alvo.classList.add("alvo-final");
    const zoom = palco.animate([{ transform: "scale(1)" }, { transform: `scale(${cfg.zoom})` }],
      { duration: pausa(cfg.zoomMs), easing: "cubic-bezier(.2,.7,.3,1)", fill: "forwards", id: TEMPO_REAL });
    foco = { palco, alvo, zoom };
    mudarRitmo(palco, cfg.lento, pausa(cfg.entradaMs));
  }
  async function afastar() {
    if (!foco) return;
    const { palco, alvo, zoom } = foco, cfg = AJUSTES.final;
    foco = null;
    const volta = palco.animate([{ transform: `scale(${cfg.zoom})` }, { transform: "scale(1)" }],
      { duration: pausa(cfg.saidaMs), easing: "ease-in-out", fill: "forwards", id: TEMPO_REAL });
    zoom.cancel();
    palco.classList.remove("foco-final");
    await mudarRitmo(palco, 1, pausa(cfg.saidaMs), (k) => k * k);
    volta.cancel();
    alvo.classList.remove("alvo-final");
  }

  /** Antes de o golpe sair (a carta ainda vai avançar, a flecha ainda vai voar): se é o golpe que encerra a luta,
   *  a câmera chega perto e o tempo desacelera primeiro, para a investida e o choque acontecerem em câmera lenta. */
  async function antesDoGolpe(m, palco, alvo) {
    if (!m || peso(m) !== "final" || rapido() || !palco || !alvo) return;
    aproximar(palco, alvo);
    await dormir(pausa(AJUSTES.final.entradaMs));
  }

  async function golpeFinal(palco, alvo) {
    aproximar(palco, alvo);  // numa salva não há "antes": a câmera lenta começa no impacto
    Som.tocar("golpe_final");
    alvo.classList.add("lampejo");
    setTimeout(() => alvo.classList.remove("lampejo"), pausa(110));
    tremor(palco, AJUSTES.tremor.final, AJUSTES.tremorMs * 1.4);
    await dormir(pausa(AJUSTES.final.seguraMs));
    await afastar();
  }

  /** Depois que o golpe acertou (o número já subiu): o momento que ele merece. */
  async function golpe(m, palco, alvo) {
    const tipo = m && peso(m);
    if (!tipo || rapido() || !palco || !alvo) return;
    if (tipo === "final") return golpeFinal(palco, alvo);
    await parada(palco, alvo, AJUSTES.parada[tipo]);
    tremor(palco, AJUSTES.tremor[tipo]);
  }

  /* ------------------------------------------------------------ vida por um fio */
  // Abaixo do limiar (o motor diz qual: heroi.vida_por_um_fio), a borda da tela e a barra de vida pulsam em
  // vermelho no compasso de um coração, mais depressa quanto menos vida resta. O coração só SOA ao entrar na
  // faixa (o aviso, umas poucas batidas) e se cala; o pulso na tela continua. Acima do limiar, ou caído, nada.
  let limiar = 0.3, desde = null, batidas = null;
  function vidaDoHeroi(hp, max, novoLimiar) {
    if (novoLimiar) limiar = novoLimiar;
    const fracao = max ? hp / max : 1, corpo = document.body;
    if (!(hp > 0 && fracao <= limiar)) {
      if (desde !== null) { desde = null; clearTimeout(batidas); corpo.classList.remove("por-um-fio"); }
      return;
    }
    const urgencia = Math.max(0, Math.min(1, 1 - fracao / limiar));
    const ms = Math.round(AJUSTES.batimentoLentoMs - (AJUSTES.batimentoLentoMs - AJUSTES.batimentoRapidoMs) * urgencia);
    corpo.style.setProperty("--batimento", ms + "ms");
    if (desde === null) {  // acabou de entrar na faixa
      desde = performance.now();
      corpo.classList.add("por-um-fio");
      bater(AJUSTES.batidasAoEntrar, ms);
    }
    // A barra de vida nasce de novo a cada redesenho da HUD; o atraso negativo a põe no compasso da borda.
    corpo.style.setProperty("--fio-fase", -Math.round(performance.now() - desde) + "ms");
  }
  function bater(n, ms) {
    if (!document.hidden) Som.tocar("batimento");
    batidas = n > 1 ? setTimeout(() => bater(n - 1, ms), ms) : null;
  }

  /* ------------------------------------------------------------ saque com cerimônia */
  /** Antes de o cartão de um item raro aparecer: a tela escurece, um feixe de luz na cor da raridade desce do
   *  alto até onde o cartão vai surgir (como os feixes de saque do Diablo), e só então ele aparece. */
  /* O saque raro chega com cerimônia, em pixel art como a paisagem: a tela escurece num pontilhado, um feixe em
     bandas de cor (o miolo claro, a cor da raridade, a borda pontilhada) desce do alto e bate no chão onde o cartão vai
     surgir; um anel se abre em degraus e fagulhas de um texel sobem. Tudo num canvas de baixa resolução ampliado sem
     suavizar, a 15 quadros por segundo. (O feixe liso, com desfoque e degradê, destoava da arte.) */
  const { pontilha } = Sprites;  // pontilha(x, y, n): o texel acende em n de cada 16
  function corP(letra) {
    const h = getComputedStyle(document.documentElement).getPropertyValue("--p-" + letra).trim() || "#ffffff";
    const v = parseInt(h.slice(1), 16);
    return (255 << 24) | ((v & 255) << 16) | (v & 0xff00) | (v >> 16);  // ABGR, como o ImageData guarda
  }
  async function cerimoniaSaque(raridade, onde) {
    const cfg = AJUSTES.saque[raridade];
    if (!cfg || rapido()) return;
    // O feixe cai no meio de `onde` (o cartão, ainda escondido no lugar em que vai surgir).
    if (onde) onde.scrollIntoView({ block: "nearest" });
    const r = onde ? onde.getBoundingClientRect() : { left: 0, width: innerWidth, top: innerHeight * 0.4, height: 0 };
    const px = r.left + r.width / 2, py = Math.max(140, Math.min(r.top + r.height * 0.45, innerHeight - 60));
    const dpr = window.devicePixelRatio || 1, T = 3 * Math.max(1, Math.round(dpr));  // um texel do efeito, em pixels do aparelho
    const W = Math.ceil((innerWidth * dpr) / T), H = Math.ceil((innerHeight * dpr) / T);
    const c = document.createElement("canvas");
    c.width = W; c.height = H;
    c.className = "cerimonia-saque";
    c.style.width = (W * T) / dpr + "px"; c.style.height = (H * T) / dpr + "px";
    document.body.appendChild(c);
    const ctx = c.getContext("2d"), img = ctx.createImageData(W, H), buf = new Uint32Array(img.data.buffer);
    const lend = raridade === "lendario";
    const pal = lend ? { miolo: corP("Y"), claro: corP("O"), cor: corP("o"), borda: corP("r") }
      : { miolo: corP("W"), claro: corP("Y"), cor: corP("y"), borda: corP("C") };
    const PRETO = 255 << 24;
    const cx = Math.round((px * dpr) / T), chao = Math.round((py * dpr) / T);
    const miolo = lend ? 3 : 2, raio = lend ? 34 : 24, veuMax = lend ? 11 : 9;
    const ms = pausa(cfg.ms), saida = 400, total = ms + saida;
    const faiscas = [];
    const por = (x, y, cor) => { if (x >= 0 && y >= 0 && x < W && y < H) buf[y * W + x] = cor; };

    function desenhar(t, q) {
      buf.fill(0);
      const vis = Math.min(1, t / 250) * (t > ms ? Math.max(0, 1 - (t - ms) / saida) : 1);
      const nVis = Math.round(16 * vis);
      // o véu: preto em pontilhado ordenado, que fecha na entrada e abre na saída
      const nVeu = Math.round(veuMax * vis);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (pontilha(x, y, nVeu)) buf[y * W + x] = PRETO;
      // o feixe: desce do alto até o chão; listras um texel mais largas escorrem para baixo
      const desce = Math.max(0, Math.min(1, (t - 80) / 320)), comp = Math.round(chao * (1 - Math.pow(1 - desce, 3)));
      for (let y = 0; y < comp; y++) {
        const largo = miolo + ((((y >> 2) - q) % 6 + 6) % 6 === 0 ? 1 : 0);
        for (let d = -(largo + 7); d <= largo + 7; d++) {
          const x = cx + d, a = Math.abs(d);
          if (!pontilha(x, y, nVis)) continue;
          if (a <= largo) por(x, y, pal.miolo);
          else if (a <= largo + 2) por(x, y, pal.claro);
          else if (a <= largo + 4) por(x, y, pal.cor);
          else if (pontilha(x, y, 16 - (a - largo - 4) * 5)) por(x, y, pal.borda);
        }
      }
      const tc = t - 400;  // o feixe bateu no chão
      if (tc < 0) return;
      // o chão: um brilho pontilhado e um anel que se abre em degraus (depois pulsa um texel)
      const rx = Math.min(raio, 3 + Math.floor(tc / 30)) + (tc > 900 && q % 4 < 2 ? 1 : 0), ry = Math.max(2, Math.round(rx * 0.3));
      for (let dy = -ry; dy <= ry; dy++) for (let dx = -rx; dx <= rx; dx++) {
        const e = (dx * dx) / (rx * rx) + (dy * dy) / (ry * ry);
        if (e > 1) continue;
        const x = cx + dx, y = chao + dy;
        if (!pontilha(x, y, nVis)) continue;
        const dentro = ((dx * dx) / ((rx - 1) * (rx - 1)) + (dy * dy) / Math.max(1, (ry - 1) * (ry - 1))) <= 1;
        if (!dentro) por(x, y, pal.claro);
        else if (pontilha(x, y, Math.round(14 * (1 - e)))) por(x, y, e < 0.25 ? pal.miolo : pal.cor);
      }
      // fagulhas: um texel (às vezes uma cruzinha) subindo e apagando de cor em cor
      if (t < ms) for (let i = 0; i < (lend ? 3 : 2); i++) {
        faiscas.push({ x: cx + Math.round((Math.random() - 0.5) * 2 * (miolo + 8)), y: chao - Math.floor(Math.random() * 3),
          v: 1 + Math.floor(Math.random() * 2), vida: 10 + Math.floor(Math.random() * 8), cruz: Math.random() < 0.25 });
      }
      for (const f of faiscas) {
        if (f.vida-- <= 0) continue;
        f.y -= f.v;
        if (q % 3 === 0) f.x += Math.random() < 0.5 ? -1 : 1;
        const cor = f.vida > 8 ? pal.miolo : f.vida > 4 ? pal.claro : pal.cor;
        if (!pontilha(f.x, f.y, nVis)) continue;
        por(f.x, f.y, cor);
        if (f.cruz && f.vida > 6) { por(f.x - 1, f.y, pal.cor); por(f.x + 1, f.y, pal.cor); por(f.x, f.y - 1, pal.cor); por(f.x, f.y + 1, pal.cor); }
      }
      // lendário: um clarão na cor dele cobre a tela num pontilhado que se desfaz
      if (lend && tc < 330) {
        const n = Math.round(4 * (1 - tc / 330));
        for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (pontilha(x + 2, y + 1, n)) buf[y * W + x] = pal.claro;
      }
    }

    Som.tocar("feixe");
    await new Promise((fim) => {
      const inicio = performance.now();
      let ultimo = -1;
      const passo = (agora) => {
        const t = agora - inicio, q = Math.floor(t / 66);  // 15 quadros por segundo
        if (q !== ultimo) { ultimo = q; desenhar(t, q); ctx.putImageData(img, 0, 0); }
        if (t < total) requestAnimationFrame(passo); else fim();
      };
      requestAnimationFrame(passo);
    });
    c.remove();
  }

  /* ------------------------------------------------------------ contar e encher */
  /** Um número que sobe contando até o valor (a partir de `de`), com um tique a cada passo (poucos tiques, para não
   *  cansar; `tiques: false` conta calado). */
  function contar(el, ate, ms = AJUSTES.contarMs, { de = 0, tiques = true } = {}) {
    if (rapido() || ate === de) { el.textContent = ate; return Promise.resolve(); }
    const passos = tiques ? Math.min(AJUSTES.tiquesMax, ate - de) : 0;
    return new Promise((fim) => {
      const inicio = performance.now();
      let dado = 0;
      const passo = (agora) => {
        const t = Math.min(1, (agora - inicio) / pausa(ms));
        el.textContent = Math.round(de + (ate - de) * (1 - Math.pow(1 - t, 2)));
        const n = Math.floor(t * passos);
        if (n > dado) { dado = n; Som.tocar("tique"); }
        if (t < 1) requestAnimationFrame(passo); else fim();
      };
      requestAnimationFrame(passo);
    });
  }
  /** Uma barra (o preenchimento é o primeiro filho) indo de uma fração a outra. */
  function encher(barra, de, ate, ms) {
    const fill = barra.firstElementChild;
    if (rapido()) { fill.style.width = ate * 100 + "%"; return Promise.resolve(); }
    return fill.animate([{ width: de * 100 + "%" }, { width: ate * 100 + "%" }],
      { duration: pausa(ms), easing: "cubic-bezier(.3,.7,.4,1)", fill: "forwards" }).finished.catch(() => {});
  }

  /* ------------------------------------------------------------ o espólio da vitória */
  // O que se acha (o motor manda o id; a tela escolhe o ícone e escreve a quantidade do jeito de cada coisa).
  const quantoAchou = (x) => (x.id === "comida" ? `+${Texto.plural(x.qtd, "dia")}` : x.id === "flechas" ? `+${x.qtd}` : `×${x.qtd}`);
  const esc = Texto.html;

  /** Como a tela de resultado dos jogos, tudo o que a vitória deu num quadro só: uma linha por recompensa (o ouro,
   *  depois a experiência com a barra de nível presa embaixo dela), e por fim o que se achou (comida, bandagem,
   *  flechas; o equipamento tem a janela dele, logo depois) e os contratos que andaram. O ouro conta e voa
   *  até a bolsa; a barra enche (se o nível vira: enche, brilha e recomeça). Some sozinho no fim; um clique ou uma
   *  tecla adianta. Os trechos da barra vêm do motor. */
  async function espolio(caixa, d) {
    const S = (n, e = 1) => Sprites.img(n, e);
    const trechos = d.trechos || [], ultimo = trechos[trechos.length - 1] || [0, 0, 1], primeiro = trechos[0] || ultimo;
    const achados = (d.itens || []).map((x) => `<span class="achado-espolio">${S(Telas.iconeConsumivel(x.id, "saco"), 2)}${esc(x.nome)}<b>${quantoAchou(x)}</b></span>`);
    const contratos = (d.contratos || []).map((c) => `<div class="espolio-contrato${c.concluido ? " feito" : ""}">${S("pergaminho", 2)}
      <span>${c.concluido ? "Contrato cumprido" : "Contrato"}</span><b>${esc(c.concluido ? "receba em qualquer vila" : c.progresso)}</b></div>`).join("");
    const extras = achados.length || contratos;
    caixa.innerHTML = `<div class="festa festa-espolio">
      <div class="rotulo-festa">${esc(d.titulo || "espólio")}</div>
      ${d.ouro ? `<div class="espolio-linha ouro">${S("moeda", 2)}<span class="nome">Ouro</span><b>+<span class="conta">0</span></b></div>` : ""}
      ${d.xp ? `<div class="espolio-xp${d.ouro ? " esperando" : ""}">
        <div class="espolio-linha xp">${S("estrela", 2)}<span class="nome">Experiência</span><b>+<span class="conta">0</span> <small>XP</small></b></div>
        <div class="espolio-nivel"><span>Nível <b>${d.nivel}</b></span><div class="espolio-barra"><i></i></div>
          <span class="espolio-faltam"><span class="conta">${primeiro[0]}</span>/<span class="total">${primeiro[2]}</span></span></div>
      </div>` : ""}
      ${extras ? `<div class="espolio-extras${d.ouro || d.xp ? " esperando" : ""}">${achados.length ? `<div class="espolio-achados">${achados.join("")}</div>` : ""}${contratos}</div>` : ""}
    </div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    const festa = caixa.querySelector(".festa-espolio");
    Telas.noPalco(festa);
    let pular = false;
    const adiantar = (ev) => { if (ev.type === "keydown" && ![" ", "Enter", "Escape"].includes(ev.key)) return; ev.preventDefault(); ev.stopPropagation(); pular = true; };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    const mostrar = (el) => el && el.classList.remove("esperando");
    if (d.titulo) Som.tocar("bau");  // um baú aberto: a tampa range antes das moedas
    await dormir(pausa(AJUSTES.espolioEsperaMs));  // a faixa de "Vitória" sai antes
    if (d.ouro) {
      Som.tocar("moeda");
      await contar(caixa.querySelector(".espolio-linha.ouro .conta"), d.ouro);
      Telas.moedasPara(caixa.querySelector(".espolio-linha.ouro"), document.querySelector('.recurso[data-rec="ouro"]'));
      await dormir(pausa(AJUSTES.espolioEntreMs));
    }
    if (d.xp) {
      mostrar(caixa.querySelector(".espolio-xp"));  // a experiência chega depois do ouro, numa linha dela
      const barra = caixa.querySelector(".espolio-barra"), nivelEl = caixa.querySelector(".espolio-nivel b");
      const noNivel = caixa.querySelector(".espolio-faltam .conta"), totalEl = caixa.querySelector(".espolio-faltam .total");
      barra.firstElementChild.style.width = (primeiro[0] / primeiro[2]) * 100 + "%";
      contar(caixa.querySelector(".espolio-linha.xp .conta"), d.xp, AJUSTES.barraMs * trechos.length, { tiques: false });
      let nivel = d.nivel;
      for (const [de, ate, total] of trechos) {
        if (pular) break;
        totalEl.textContent = total;
        contar(noNivel, ate, AJUSTES.barraMs, { de, tiques: false });
        await encher(barra, de / total, ate / total, AJUSTES.barraMs);
        if (ate >= total) {  // o nível virou: a barra brilha, o número sobe, e ela recomeça
          nivel += 1;
          nivelEl.textContent = nivel;
          festa.classList.remove("subiu"); void festa.offsetWidth; festa.classList.add("subiu");
          Som.tocar("nivel");
          await dormir(pausa(350));
        }
      }
      if (pular) {  // adiantou: os números vão direto ao fim
        caixa.querySelector(".espolio-linha.xp .conta").textContent = d.xp;
        noNivel.textContent = ultimo[1]; totalEl.textContent = ultimo[2];
      }
    }
    if (extras) {
      if (!pular) await dormir(pausa(AJUSTES.espolioEntreMs));
      mostrar(caixa.querySelector(".espolio-extras"));
      Som.tocar("item");
    }
    const fica = AJUSTES.espolioFicaMs + (extras ? AJUSTES.espolioAchadoMs * (achados.length + (d.contratos || []).length) : 0);
    if (!pular) await Promise.race([dormir(pausa(fica)), new Promise((r) => { const t = setInterval(() => { if (pular) { clearInterval(t); r(); } }, 50); })]);
    document.removeEventListener("pointerdown", adiantar, true);
    document.removeEventListener("keydown", adiantar, true);
    festa.classList.add("saindo");
    await dormir(220);
    caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve");
  }

  return { AJUSTES, configurar, peso, maisPesado, tremor, parada, antesDoGolpe, golpe, depois, contar, encher, espolio,
    vidaDoHeroi, cerimoniaSaque };
})();
