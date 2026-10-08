/* Sensação: o peso dos momentos do jogo. As telas (batalha.js, telas.js) dizem O QUE aconteceu; aqui mora
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
    barraMs: 700, espolioEsperaMs: 450, espolioFicaMs: 900,
    // Vida por um fio: o compasso do pulso (ms entre batidas), mais rápido quanto mais perto do fim, e quantas
    // vezes o coração soa ao entrar na faixa (depois só a tela pulsa: som contínuo cansa e angustia).
    batimentoLentoMs: 1150, batimentoRapidoMs: 700, batidasAoEntrar: 3,
    // Saque com cerimônia: por raridade, quanto o feixe de luz demora antes de o cartão aparecer (sem entrada,
    // o item aparece direto). O lendário ainda ganha um clarão na tela inteira.
    saque: { raro: { ms: 750 }, lendario: { ms: 1150, clarao: true } },
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
  async function cerimoniaSaque(raridade, onde) {
    const cfg = AJUSTES.saque[raridade];
    if (!cfg || rapido()) return;
    // O feixe cai no meio de `onde` (o cartão, ainda escondido no lugar em que vai surgir).
    if (onde) onde.scrollIntoView({ block: "nearest" });
    const r = onde ? onde.getBoundingClientRect() : { left: 0, width: innerWidth, top: innerHeight * 0.4, height: 0 };
    const x = r.left + r.width / 2, y = Math.max(140, Math.min(r.top + r.height * 0.45, innerHeight - 60));
    const veu = document.createElement("div");
    veu.className = `cerimonia-saque rar-${raridade}`;
    veu.innerHTML = `<i class="feixe" style="left:${x}px;height:${y}px"></i><i class="chao" style="left:${x}px;top:${y}px"></i>` +
      (cfg.clarao ? '<i class="clarao"></i>' : "");
    document.body.appendChild(veu);
    Som.tocar("feixe");
    await dormir(pausa(cfg.ms));
    veu.classList.add("saindo");
    setTimeout(() => veu.remove(), 400);
  }

  /* ------------------------------------------------------------ contar e encher */
  /** Um número que sobe contando até o valor, com um tique a cada passo (poucos tiques, para não cansar). */
  function contar(el, ate, ms = AJUSTES.contarMs) {
    if (rapido() || !ate) { el.textContent = ate; return Promise.resolve(); }
    const passos = Math.min(AJUSTES.tiquesMax, ate);
    return new Promise((fim) => {
      const inicio = performance.now();
      let dado = 0;
      const passo = (agora) => {
        const t = Math.min(1, (agora - inicio) / pausa(ms));
        el.textContent = Math.round(ate * (1 - Math.pow(1 - t, 2)));
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
  /** O ouro conta subindo e voa até a bolsa; a barra de XP enche (e, se o nível vira, enche, brilha e
   *  recomeça). Some sozinho no fim; um clique ou uma tecla adianta. Os trechos da barra vêm do motor. */
  async function espolio(caixa, d) {
    const S = (n, e = 1) => Sprites.img(n, e);
    caixa.innerHTML = `<div class="festa festa-espolio">
      <div class="rotulo-festa">espólio</div>
      ${d.ouro ? `<div class="espolio-ouro">${S("moeda", 2)}<b>+<span class="conta">0</span></b><small>ouro</small></div>` : ""}
      <div class="espolio-xp"><div class="espolio-nivel">Nível <b>${d.nivel}</b></div>
        <div class="espolio-barra"><i></i></div><div class="espolio-mais">+${d.xp} XP</div></div></div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    let pular = false;
    const adiantar = (ev) => { if (ev.type === "keydown" && ![" ", "Enter", "Escape"].includes(ev.key)) return; ev.preventDefault(); ev.stopPropagation(); pular = true; };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    const festa = caixa.querySelector(".festa-espolio");
    const barra = caixa.querySelector(".espolio-barra"), nivelEl = caixa.querySelector(".espolio-nivel b");
    const primeiro = d.trechos[0];
    if (primeiro) barra.firstElementChild.style.width = (primeiro[0] / primeiro[2]) * 100 + "%";
    await dormir(pausa(AJUSTES.espolioEsperaMs));  // a faixa de "Vitória" sai antes
    if (d.ouro) {
      Som.tocar("moeda");
      await contar(caixa.querySelector(".espolio-ouro .conta"), d.ouro);
      Telas.moedasPara(caixa.querySelector(".espolio-ouro"), document.querySelector('.recurso[data-rec="ouro"]'));
    }
    let nivel = d.nivel;
    for (const [de, ate, total] of d.trechos) {
      if (pular) break;
      await encher(barra, de / total, ate / total, AJUSTES.barraMs);
      if (ate >= total) {  // o nível virou: a barra brilha, o número sobe, e ela recomeça
        nivel += 1;
        nivelEl.textContent = nivel;
        festa.classList.remove("subiu"); void festa.offsetWidth; festa.classList.add("subiu");
        Som.tocar("nivel");
        await dormir(pausa(350));
      }
    }
    if (!pular) await Promise.race([dormir(pausa(AJUSTES.espolioFicaMs)), new Promise((r) => { const t = setInterval(() => { if (pular) { clearInterval(t); r(); } }, 50); })]);
    document.removeEventListener("pointerdown", adiantar, true);
    document.removeEventListener("keydown", adiantar, true);
    festa.classList.add("saindo");
    await dormir(220);
    caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve");
  }

  return { AJUSTES, configurar, peso, maisPesado, tremor, parada, antesDoGolpe, golpe, depois, contar, encher, espolio,
    vidaDoHeroi, cerimoniaSaque };
})();
