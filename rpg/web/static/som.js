/* Som sintetizado com Web Audio: nada de arquivos, tudo gerado na hora.
   Ambiente (vento/brejo/fogo) por bioma, dado, golpes, virar de página. */
"use strict";

const Som = (() => {
  let ctx = null, mestre = null, ambiente = null, ambienteBioma = null;
  let ligado = true;
  try { ligado = localStorage.getItem("cdf-som") !== "0"; } catch (e) { /* armazenamento indisponível */ }

  function iniciar() {
    if (ctx) { if (ctx.state === "suspended") ctx.resume(); return true; }
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return false;
    ctx = new AC();
    mestre = ctx.createGain();
    mestre.gain.value = ligado ? 0.9 : 0;
    mestre.connect(ctx.destination);
    return true;
  }

  function ruido(segundos, cor = "branco") {
    const n = Math.floor(ctx.sampleRate * segundos);
    const buf = ctx.createBuffer(1, n, ctx.sampleRate);
    const d = buf.getChannelData(0);
    let ultimo = 0;
    for (let i = 0; i < n; i++) {
      const b = Math.random() * 2 - 1;
      if (cor === "marrom") { ultimo = (ultimo + 0.02 * b) / 1.02; d[i] = ultimo * 3.5; }
      else d[i] = b;
    }
    return buf;
  }

  function estalo(t, freq, vol, dur = 0.05) {
    const src = ctx.createBufferSource();
    src.buffer = ruido(dur + 0.02);
    const f = ctx.createBiquadFilter();
    f.type = "bandpass"; f.frequency.value = freq; f.Q.value = 6;
    const g = ctx.createGain();
    g.gain.setValueAtTime(vol, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(f).connect(g).connect(mestre);
    src.start(t); src.stop(t + dur + 0.02);
  }

  function tom(t, freq, vol, dur, tipo = "sine", freqFim = null) {
    const o = ctx.createOscillator();
    o.type = tipo;
    o.frequency.setValueAtTime(freq, t);
    if (freqFim) o.frequency.exponentialRampToValueAtTime(freqFim, t + dur);
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g).connect(mestre);
    o.start(t); o.stop(t + dur + 0.05);
  }

  const efeitos = {
    dado() {
      const t = ctx.currentTime;
      let x = 0;
      for (let i = 0; i < 9; i++) {
        x += 0.04 + Math.random() * 0.07 * (1 + i * 0.15);
        estalo(t + x, 1800 + Math.random() * 2200, 0.35 * (1 - i / 11), 0.035);
      }
    },
    sucesso() { const t = ctx.currentTime; tom(t, 523, 0.12, 0.35, "triangle"); tom(t + 0.09, 784, 0.1, 0.5, "triangle"); },
    falha() { const t = ctx.currentTime; tom(t, 196, 0.14, 0.5, "sawtooth", 130); },
    critico() { const t = ctx.currentTime; [523, 659, 784, 1046].forEach((f, i) => tom(t + i * 0.07, f, 0.1, 0.6, "triangle")); },
    golpe() {
      const t = ctx.currentTime;
      tom(t, 120, 0.5, 0.22, "sine", 45);
      estalo(t, 900, 0.3, 0.09);
    },
    dor() { const t = ctx.currentTime; tom(t, 90, 0.6, 0.35, "sine", 40); estalo(t, 400, 0.4, 0.15); },
    pagina() {
      const t = ctx.currentTime;
      const src = ctx.createBufferSource();
      src.buffer = ruido(0.4);
      const f = ctx.createBiquadFilter();
      f.type = "bandpass"; f.Q.value = 1.2;
      f.frequency.setValueAtTime(600, t); f.frequency.exponentialRampToValueAtTime(3500, t + 0.3);
      const g = ctx.createGain();
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.09, t + 0.08);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.35);
      src.connect(f).connect(g).connect(mestre);
      src.start(t); src.stop(t + 0.4);
    },
    escolha() { estalo(ctx.currentTime, 2500, 0.12, 0.03); },
    nivel() { const t = ctx.currentTime; [392, 494, 587, 784].forEach((f, i) => tom(t + i * 0.11, f, 0.09, 0.9, "triangle")); },
    moeda() { const t = ctx.currentTime; tom(t, 1900, 0.06, 0.12, "square"); tom(t + 0.05, 2600, 0.05, 0.2, "square"); },
    item() { const t = ctx.currentTime; tom(t, 660, 0.07, 0.12, "square"); tom(t + 0.07, 990, 0.06, 0.18, "square"); },
    aprova() { const t = ctx.currentTime; tom(t, 523, 0.06, 0.2, "triangle"); tom(t + 0.08, 659, 0.06, 0.3, "triangle"); },
    desaprova() { const t = ctx.currentTime; tom(t, 330, 0.07, 0.25, "triangle", 290); tom(t + 0.1, 262, 0.07, 0.35, "triangle", 230); },
    morte() {
      const t = ctx.currentTime;
      tom(t, 220, 0.25, 0.5, "sawtooth", 55);
      estalo(t, 300, 0.5, 0.3);
      estalo(t + 0.08, 180, 0.4, 0.35);
    },
    vitoria() {
      const t = ctx.currentTime;
      [[392, 0], [523, 0.12], [659, 0.24], [784, 0.36]].forEach(([f, d]) => tom(t + d, f, 0.1, 0.35, "square"));
      tom(t + 0.48, 1046, 0.1, 0.9, "square");
    },
    fanfarra() {
      const t = ctx.currentTime;
      const notas = [[523, 0, 0.18], [523, 0.15, 0.18], [523, 0.3, 0.18], [659, 0.45, 0.5], [587, 0.95, 0.18], [659, 1.1, 0.18], [784, 1.25, 1.1]];
      notas.forEach(([f, d, dur]) => { tom(t + d, f, 0.09, dur, "square"); tom(t + d, f / 2, 0.06, dur, "triangle"); });
      for (let i = 0; i < 14; i++) tom(t + 1.3 + i * 0.05, 1500 + Math.random() * 1500, 0.025, 0.25, "sine");
    },
  };

  const AMBIENTES = {
    floresta: { freq: 500, q: 0.6, vol: 0.05, lfo: 0.07 },
    pantano: { freq: 260, q: 1.4, vol: 0.06, lfo: 0.05 },
    montanha: { freq: 900, q: 0.4, vol: 0.06, lfo: 0.11 },
    planicie: { freq: 700, q: 0.5, vol: 0.045, lfo: 0.09 },
    ruinas: { freq: 340, q: 2.2, vol: 0.05, lfo: 0.04 },
    cidadela: { freq: 180, q: 3.0, vol: 0.07, lfo: 0.03 },
    vila: { freq: 420, q: 0.7, vol: 0.03, lfo: 0.06 },
  };

  function trocarAmbiente(bioma) {
    if (!ctx || bioma === ambienteBioma) return;
    ambienteBioma = bioma;
    const p = AMBIENTES[bioma] || AMBIENTES.vila;
    const t = ctx.currentTime;
    if (ambiente) {
      const velho = ambiente;
      velho.g.gain.setTargetAtTime(0.0001, t, 0.8);
      setTimeout(() => { try { velho.src.stop(); velho.lfo.stop(); } catch (e) { /* já parou */ } }, 4000);
    }
    const src = ctx.createBufferSource();
    src.buffer = ruido(6, "marrom"); src.loop = true;
    const f = ctx.createBiquadFilter();
    f.type = "bandpass"; f.frequency.value = p.freq; f.Q.value = p.q;
    const lfo = ctx.createOscillator(); lfo.frequency.value = p.lfo;
    const lfoG = ctx.createGain(); lfoG.gain.value = p.freq * 0.45;
    lfo.connect(lfoG).connect(f.frequency);
    const g = ctx.createGain(); g.gain.value = 0.0001;
    g.gain.setTargetAtTime(p.vol, t, 1.5);
    src.connect(f).connect(g).connect(mestre);
    src.start(); lfo.start();
    ambiente = { src, lfo, g };
  }

  return {
    iniciar,
    tocar(nome) { if (!ligado || !ctx || !efeitos[nome]) return; try { efeitos[nome](); } catch (e) { /* sem som */ } },
    ambiente(bioma) { if (ctx) trocarAmbiente(bioma); else ambienteBioma = null; this._pendente = bioma; },
    alternar() {
      ligado = !ligado;
      try { localStorage.setItem("cdf-som", ligado ? "1" : "0"); } catch (e) { /* ok */ }
      if (ctx) mestre.gain.setTargetAtTime(ligado ? 0.9 : 0, ctx.currentTime, 0.1);
      return ligado;
    },
    get ligado() { return ligado; },
    _pendente: null,
  };
})();
