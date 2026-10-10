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

  // Ruído filtrado com envelope e varredura de frequência (fogo, vento, magia).
  function sopro(t, dur, f0, f1, vol, q = 1, tipo = "bandpass") {
    const src = ctx.createBufferSource();
    src.buffer = ruido(dur + 0.05);
    const f = ctx.createBiquadFilter();
    f.type = tipo; f.Q.value = q;
    f.frequency.setValueAtTime(f0, t); f.frequency.exponentialRampToValueAtTime(f1, t + dur);
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + dur * 0.25);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(f).connect(g).connect(mestre);
    src.start(t); src.stop(t + dur + 0.05);
  }

  // Uma voz de soldado: serra grave passando por dois formantes de "a" (o "HA!" de um coro).
  function voz(t, f0, dur, vol) {
    const o = ctx.createOscillator();
    o.type = "sawtooth";
    o.frequency.setValueAtTime(f0 * 1.06, t);
    o.frequency.exponentialRampToValueAtTime(f0 * 0.9, t + dur);
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.025);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    [[720, 5], [1180, 6], [2500, 8]].forEach(([fr, q], i) => {
      const f = ctx.createBiquadFilter();
      f.type = "bandpass"; f.frequency.value = fr; f.Q.value = q;
      const gf = ctx.createGain(); gf.gain.value = [1, 0.6, 0.25][i];
      o.connect(f).connect(gf).connect(g);
    });
    g.connect(mestre);
    o.start(t); o.stop(t + dur + 0.05);
  }

  const efeitos = {
    // Erguer Escudo: um pelotão responde "HA!" em coro e bate os escudos no chão ao mesmo tempo.
    falange() {
      const t = ctx.currentTime;
      for (let i = 0; i < 7; i++) voz(t + Math.random() * 0.03, 92 + Math.random() * 60, 0.2, 0.05);
      const b = t + 0.17;
      for (let i = 0; i < 8; i++) {
        const j = b + Math.random() * 0.028;
        tom(j, 66 + Math.random() * 22, 0.1, 0.28, "sine", 38);
        estalo(j, 1500 + Math.random() * 1400, 0.09, 0.07);
      }
      tom(b, 1260, 0.035, 0.45, "triangle"); tom(b + 0.01, 1890, 0.02, 0.35, "triangle");
      sopro(b, 0.3, 900, 300, 0.12, 0.8, "lowpass");
    },
    dado() {
      const t = ctx.currentTime;
      let x = 0;
      for (let i = 0; i < 9; i++) {
        x += 0.04 + Math.random() * 0.07 * (1 + i * 0.15);
        estalo(t + x, 1800 + Math.random() * 2200, 0.35 * (1 - i / 11), 0.035);
      }
    },
    // Os prédios da vila: o som de cada um ao clicar, curto e baixo, para combinar com o tom da paisagem.
    predio_templo() {  // o sino: parciais de sino, longos, sumindo devagar
      const t = ctx.currentTime;
      [[392, 0.07, 2.2], [784, 0.035, 1.6], [941, 0.03, 1.4], [1176, 0.02, 1.1], [1647, 0.012, 0.8]].forEach(([f, v, d]) => tom(t, f, v, d, "sine"));
      tom(t, 196, 0.04, 2.4, "sine");
    },
    predio_taverna() {  // o burburinho do salão, como nos jogos antigos: sílabas de ruído abafado e resmungos graves
      const t = ctx.currentTime;
      for (let i = 0; i < 14; i++) {  // a falação: rajadas curtas de ruído na faixa da voz, sem voz nenhuma
        const d = i * 0.075 + Math.random() * 0.05, v = 0.05 * Math.sin(Math.PI * (i + 0.5) / 14);
        sopro(t + d, 0.12 + Math.random() * 0.1, 260 + Math.random() * 260, 200 + Math.random() * 160, v, 2.5);
      }
      [0.18, 0.52, 0.86].forEach((d) => {  // resmungos: um tom grave que desce e volta, abafado
        const f = 95 + Math.random() * 45;
        tom(t + d + Math.random() * 0.05, f, 0.03, 0.16, "triangle", f * 0.78);
      });
      estalo(t + 0.62, 2900, 0.04, 0.03); tom(t + 0.62, 2900, 0.008, 0.2, "triangle");  // uma caneca lá no fundo
    },
    predio_mercado() {  // a moeda jogada para cima: o tinido girando no ar e os quiques no balcão
      const t = ctx.currentTime;
      for (let i = 0; i < 5; i++) tom(t + i * 0.06, 2400 + (i % 2) * 700, 0.03, 0.09, "triangle");
      [0.42, 0.55, 0.64, 0.7].forEach((d, i) => { estalo(t + d, 3000, 0.12 * (1 - i * 0.22), 0.02); tom(t + d, 2700, 0.02 * (1 - i * 0.2), 0.12, "triangle"); });
    },
    predio_ferreiro() {  // o martelo na bigorna
      const t = ctx.currentTime;
      estalo(t, 3200, 0.25, 0.025); tom(t, 1760, 0.07, 0.7, "triangle"); tom(t, 2640, 0.035, 0.5, "triangle"); tom(t, 110, 0.15, 0.12, "sine", 60);
      estalo(t + 0.32, 3000, 0.12, 0.02); tom(t + 0.32, 1760, 0.03, 0.4, "triangle");
    },
    predio_mural() {  // papel pregado sendo mexido
      const t = ctx.currentTime;
      sopro(t, 0.18, 2500, 6000, 0.05, 1.4, "highpass"); sopro(t + 0.16, 0.14, 3000, 5000, 0.035, 1.4, "highpass");
    },
    predio_curandeiro() {  // um frasco de vidro e um borbulhar
      const t = ctx.currentTime;
      tom(t, 1980, 0.035, 0.35, "sine"); tom(t + 0.02, 2970, 0.015, 0.25, "sine");
      for (let i = 0; i < 4; i++) tom(t + 0.2 + i * 0.07, 380 + Math.random() * 300, 0.025, 0.08, "sine", 700 + Math.random() * 300);
    },
    predio_estrada() {  // passos no cascalho
      const t = ctx.currentTime;
      [0, 0.3, 0.6].forEach((d) => { sopro(t + d, 0.12, 1800, 500, 0.06, 0.9, "lowpass"); estalo(t + d + 0.02, 900, 0.03, 0.03); });
    },
    surpresa() {  // o "!" de quem foi pego desprevenido: duas notas agudas e secas, e um baque
      const t = ctx.currentTime;
      tom(t, 988, 0.06, 0.09, "square"); tom(t + 0.08, 1480, 0.06, 0.16, "square");
      estalo(t, 1200, 0.08, 0.04); tom(t, 110, 0.08, 0.18, "sine", 70);
    },
    buff() {  // um estado bom: duas notas que sobem e um brilho
      const t = ctx.currentTime;
      tom(t, 523, 0.07, 0.22, "triangle", 659); tom(t + 0.09, 784, 0.07, 0.4, "triangle", 1046);
      sopro(t + 0.05, 0.35, 3000, 7000, 0.025, 1, "highpass");
    },
    debuff() {  // um mal: duas notas que descem, ásperas e quase juntas
      const t = ctx.currentTime;
      tom(t, 330, 0.06, 0.35, "sawtooth", 233); tom(t + 0.07, 311, 0.05, 0.45, "square", 196);
      sopro(t, 0.4, 900, 250, 0.03, 1.2, "lowpass");
    },
    bau() {  // a recompensa, não a fechadura: um arpejo que sobe (dó, mi, sol) até o dó de cima, que fica, e um brilho
      const t = ctx.currentTime;
      [523, 659, 784].forEach((f, i) => tom(t + i * 0.075, f, 0.06, 0.16, "square"));
      tom(t + 0.225, 1047, 0.07, 0.6, "square");
      [1319, 1568, 2093].forEach((f, i) => tom(t + 0.27 + i * 0.05, f, 0.03, 0.55, "triangle"));
      sopro(t + 0.22, 0.6, 3000, 9000, 0.025, 0.7, "highpass");
    },
    exausto() {  // um suspiro longo e grave: o corpo que não vai mais
      const t = ctx.currentTime;
      sopro(t, 1.1, 700, 180, 0.07, 0.7, "lowpass");
      tom(t + 0.05, 130, 0.05, 1.2, "triangle", 82);
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
    amanhecer() {
      const t = ctx.currentTime;
      [262, 330, 392, 523].forEach((f, i) => tom(t + i * 0.18, f, 0.05, 1.4, "sine"));
      sopro(t + 0.35, 1.4, 2000, 7000, 0.02, 0.5, "highpass");
    },
    nivel() { const t = ctx.currentTime; [392, 494, 587, 784].forEach((f, i) => tom(t + i * 0.11, f, 0.09, 0.9, "triangle")); },
    // Aprender talento: "plim" de moeda + um brilho mágico que sobe (curto: é para viciar, não para cansar).
    aprender() {
      const t = ctx.currentTime;
      tom(t, 1568, 0.07, 0.10, "square"); tom(t + 0.045, 2349, 0.06, 0.16, "square");
      [1047, 1319, 1568, 2093].forEach((f, i) => tom(t + 0.06 + i * 0.035, f, 0.035, 0.22, "triangle"));
      sopro(t + 0.04, 0.28, 3000, 9000, 0.025, 0.7, "highpass");
    },
    // Subir de nível: impacto grave, acorde que sobe e brilho longo.
    subir() {
      const t = ctx.currentTime;
      tom(t, 98, 0.18, 0.5, "sine", 60);
      [262, 330, 392, 523, 659, 784].forEach((f, i) => tom(t + 0.05 + i * 0.07, f, 0.06, 0.9, "triangle"));
      [523, 659, 784].forEach((f) => tom(t + 0.5, f, 0.045, 1.4, "sine"));
      sopro(t + 0.45, 1.2, 2500, 8000, 0.03, 0.6, "highpass");
    },
    // Item encontrado: baú que se abre (baque + tilintar); quanto mais raro, mais longo o brilho.
    achado() {
      const t = ctx.currentTime;
      tom(t, 120, 0.16, 0.18, "sine", 70); estalo(t, 1800, 0.18, 0.04);
      [784, 1047, 1319].forEach((f, i) => tom(t + 0.08 + i * 0.05, f, 0.05, 0.3, "triangle"));
    },
    achado_raro() {
      const t = ctx.currentTime;
      tom(t, 110, 0.2, 0.25, "sine", 60); estalo(t, 1800, 0.2, 0.05);
      [523, 659, 784, 1047, 1319, 1568].forEach((f, i) => tom(t + 0.08 + i * 0.06, f, 0.05, 0.7, "triangle"));
      [1047, 1319, 1568].forEach((f) => tom(t + 0.5, f, 0.03, 1.2, "sine"));
      sopro(t + 0.3, 1.0, 3000, 9000, 0.03, 0.6, "highpass");
    },
    tique() { estalo(ctx.currentTime, 3600, 0.18, 0.02); },
    moeda() { const t = ctx.currentTime; tom(t, 1900, 0.06, 0.12, "square"); tom(t + 0.05, 2600, 0.05, 0.2, "square"); },
    equipar() { const t = ctx.currentTime; estalo(t, 3200, 0.25, 0.06); estalo(t + 0.05, 2200, 0.2, 0.08); tom(t, 180, 0.12, 0.15, "square", 120); },
    item() { const t = ctx.currentTime; tom(t, 660, 0.07, 0.12, "square"); tom(t + 0.07, 990, 0.06, 0.18, "square"); },
    aprova() { const t = ctx.currentTime; tom(t, 523, 0.06, 0.2, "triangle"); tom(t + 0.08, 659, 0.06, 0.3, "triangle"); },
    desaprova() { const t = ctx.currentTime; tom(t, 330, 0.07, 0.25, "triangle", 290); tom(t + 0.1, 262, 0.07, 0.35, "triangle", 230); },
    golpe_leve() { const t = ctx.currentTime; tom(t, 140, 0.25, 0.14, "sine", 60); estalo(t, 1200, 0.15, 0.05); },
    critico_golpe() {
      const t = ctx.currentTime;
      tom(t, 160, 0.6, 0.3, "sine", 40); estalo(t, 700, 0.45, 0.12); estalo(t + 0.03, 2400, 0.25, 0.08);
      tom(t + 0.02, 880, 0.06, 0.25, "square", 1320);
    },
    // O feixe do saque raro: um ar que sobe e um acorde que se abre (o tilintar vem quando o cartão aparece).
    feixe() {
      const t = ctx.currentTime;
      sopro(t, 0.9, 400, 6000, 0.05, 0.7, "bandpass");
      [196, 294, 392, 587].forEach((f, i) => tom(t + 0.1 + i * 0.12, f, 0.045, 1.1, "sine"));
    },
    // Vida por um fio: o coração (tum-tum, grave e curto).
    batimento() {
      const t = ctx.currentTime;
      tom(t, 58, 0.55, 0.13, "sine", 40); tom(t + 0.17, 52, 0.42, 0.15, "sine", 36);
    },
    // O golpe que encerra a luta: um baque fundo, o estalo do impacto e um ar que se esvai.
    golpe_final() {
      const t = ctx.currentTime;
      tom(t, 72, 0.7, 0.9, "sine", 34); estalo(t, 600, 0.5, 0.16); estalo(t + 0.04, 2600, 0.3, 0.1);
      sopro(t + 0.05, 0.9, 1200, 200, 0.12, 0.8, "lowpass");
    },
    dor_leve() { const t = ctx.currentTime; tom(t, 110, 0.25, 0.2, "sine", 60); },
    chama() { const t = ctx.currentTime; sopro(t, 0.45, 300, 2400, 0.35, 0.7); for (let i = 0; i < 6; i++) estalo(t + 0.05 + Math.random() * 0.35, 3000 + Math.random() * 2000, 0.12, 0.02); tom(t, 90, 0.3, 0.3, "sine", 50); },
    gelo() { const t = ctx.currentTime; [2093, 2637, 3136, 2349].forEach((f, i) => tom(t + i * 0.035, f, 0.05, 0.35, "triangle")); estalo(t, 5000, 0.25, 0.06); tom(t, 120, 0.25, 0.18, "sine", 60); },
    sagrado() { const t = ctx.currentTime; [784, 988, 1175, 1568].forEach((f, i) => tom(t + i * 0.03, f, 0.05, 0.6, "sine")); tom(t, 140, 0.3, 0.2, "sine", 60); },
    sombra() { const t = ctx.currentTime; tom(t, 180, 0.12, 0.5, "sawtooth", 70); tom(t + 0.02, 186, 0.1, 0.5, "sawtooth", 66); sopro(t, 0.4, 800, 200, 0.2, 2); },
    arcano() { const t = ctx.currentTime; tom(t, 660, 0.07, 0.3, "square", 1760); tom(t + 0.05, 990, 0.05, 0.3, "triangle", 2200); tom(t, 130, 0.25, 0.16, "sine", 60); },
    veneno() { const t = ctx.currentTime; for (let i = 0; i < 5; i++) tom(t + i * 0.06, 300 + Math.random() * 400, 0.06, 0.1, "sine", 600 + Math.random() * 300); },
    mana() { const t = ctx.currentTime; [392, 587, 784, 1175].forEach((f, i) => tom(t + i * 0.07, f, 0.045, 0.55, "triangle", f * 1.01)); tom(t, 196, 0.08, 0.5, "sine", 220); sopro(t, 0.5, 3000, 7000, 0.02, 0.7, "highpass"); },
    cura() { const t = ctx.currentTime; [523, 659, 784, 1046, 1318].forEach((f, i) => tom(t + i * 0.06, f, 0.05, 0.5, "sine")); sopro(t, 0.6, 2000, 6000, 0.03, 0.8, "highpass"); },
    roubo() { const t = ctx.currentTime; tom(t, 520, 0.09, 0.45, "sawtooth", 140); tom(t + 0.1, 330, 0.06, 0.4, "triangle", 110); sopro(t, 0.45, 1600, 300, 0.12, 3); },
    esquiva() { const t = ctx.currentTime; sopro(t, 0.22, 600, 3200, 0.18, 1.5); },
    disparo() { const t = ctx.currentTime; estalo(t, 1500, 0.2, 0.04); sopro(t + 0.02, 0.18, 2500, 900, 0.12, 2); },
    lancar() { const t = ctx.currentTime; sopro(t, 0.25, 400, 1800, 0.18, 1.2); },
    atordoar() { const t = ctx.currentTime; [1568, 1318, 1568, 1318].forEach((f, i) => tom(t + i * 0.08, f, 0.04, 0.12, "square")); },
    feitico() { const t = ctx.currentTime; tom(t, 392, 0.06, 0.35, "triangle", 262); tom(t + 0.06, 311, 0.05, 0.4, "triangle", 196); },
    protecao() { const t = ctx.currentTime; [392, 523, 659].forEach((f, i) => tom(t + i * 0.05, f, 0.05, 0.6, "triangle")); sopro(t, 0.5, 3000, 5000, 0.03, 1, "highpass"); },
    rugido() { const t = ctx.currentTime; tom(t, 70, 0.5, 0.9, "sawtooth", 45); tom(t, 73, 0.4, 0.9, "sawtooth", 48); sopro(t, 0.9, 300, 120, 0.4, 0.8, "lowpass"); },
    risada() {  // "he-he-he" de encrenqueiro: três sílabas nasais descendo
      const t = ctx.currentTime;
      [0, 0.13, 0.26, 0.41].forEach((d, i) => {
        const f = 620 - i * 60;
        tom(t + d, f, 0.07, 0.1, "square", f * 0.82);
        tom(t + d, f * 1.5, 0.025, 0.08, "sawtooth", f * 1.2);
        sopro(t + d, 0.08, 1800, 900, 0.05, 3);
      });
    },
    fala() { const t = ctx.currentTime; [0, 0.06, 0.12].forEach((d) => tom(t + d, 520 + Math.random() * 260, 0.03, 0.06, "square")); },
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
