// PROTÓTIPO de campo livre: sons sintetizados na hora com Web Audio (ruído filtrado e osciladores), como o som.js do
// jogo: nenhum arquivo de áudio, nenhuma licença de terceiros. Volume e mudo nas opções. O som acompanha; nenhum
// acerto depende dele para ser entendido. Cada som tem um intervalo mínimo, para uma área com doze acertos não virar
// doze estalos empilhados.
let ctx = null, mestre = null, ruido = null, volume = 0.5, mudo = false;
const ultimo = {};
const INTERVALO = { acerto: 0.05, impacto: 0.06, dor: 0.12, faisca: 0.05, aviso: 0.2, choque: 0.1, bloqueio: 0.06 };

export function iniciarSom() {
  if (ctx) { if (ctx.state === "suspended") ctx.resume(); return; }
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  ctx = new AC();
  mestre = ctx.createGain();
  mestre.gain.value = mudo ? 0 : volume;
  mestre.connect(ctx.destination);
  ruido = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
  const d = ruido.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
}

export function ajustarSom(v, m) {
  volume = v;
  mudo = m;
  if (mestre) mestre.gain.value = mudo ? 0 : volume;
}

function chiado(t0, dur, freq, q, ganho, tipo = "bandpass", freqFim) {
  const s = ctx.createBufferSource(), f = ctx.createBiquadFilter(), gn = ctx.createGain();
  s.buffer = ruido;
  f.type = tipo; f.frequency.value = freq; f.Q.value = q;
  if (freqFim) f.frequency.exponentialRampToValueAtTime(freqFim, t0 + dur);
  gn.gain.setValueAtTime(ganho, t0);
  gn.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
  s.connect(f); f.connect(gn); gn.connect(mestre);
  s.start(t0, Math.random() * 0.5, dur + 0.05);
}

function tom(t0, dur, f0, f1, ganho, forma = "sine") {
  const o = ctx.createOscillator(), gn = ctx.createGain();
  o.type = forma;
  o.frequency.setValueAtTime(f0, t0);
  o.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t0 + dur);
  gn.gain.setValueAtTime(ganho, t0);
  gn.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
  o.connect(gn); gn.connect(mestre);
  o.start(t0); o.stop(t0 + dur + 0.02);
}

export function tocar(nome) {
  if (!ctx || mudo || volume <= 0) return;
  const t = ctx.currentTime;
  const iv = INTERVALO[nome] ?? 0.03;
  if (ultimo[nome] && t - ultimo[nome] < iv) return;
  ultimo[nome] = t;
  switch (nome) {
    case "corte": chiado(t, 0.07, 3200, 1.2, 0.25, "bandpass", 1800); break;
    case "corteForte": chiado(t, 0.11, 2600, 1, 0.35, "bandpass", 900); break;
    case "acerto": chiado(t, 0.04, 1500, 2, 0.22); break;
    case "impacto": tom(t, 0.09, 150, 55, 0.35); chiado(t, 0.06, 900, 1, 0.25); break;
    case "dor": tom(t, 0.08, 220, 120, 0.18, "triangle"); break;
    case "preparo": chiado(t, 0.16, 600, 0.8, 0.12, "bandpass", 2400); break;
    case "varredura": chiado(t, 0.18, 2000, 0.8, 0.4, "bandpass", 500); tom(t, 0.14, 120, 50, 0.3); break;
    case "investida": chiado(t, 0.2, 400, 0.7, 0.25, "lowpass", 1500); break;
    case "aterrissa": tom(t, 0.25, 90, 35, 0.6); chiado(t, 0.3, 500, 0.7, 0.4, "lowpass", 150); break;
    case "explosao": tom(t, 0.3, 80, 30, 0.5); chiado(t, 0.45, 1400, 0.6, 0.5, "lowpass", 120); break;
    case "lanca": chiado(t, 0.12, 900, 1.5, 0.15, "bandpass", 300); break;
    case "faisca": tom(t, 0.05, 1300, 700, 0.08, "square"); break;
    case "piscar": tom(t, 0.12, 400, 1600, 0.12, "triangle"); chiado(t, 0.15, 3000, 1, 0.12); break;
    case "fogo": chiado(t, 0.5, 700, 0.5, 0.25, "lowpass", 300); break;
    case "aviso": tom(t, 0.3, 70, 90, 0.18, "sawtooth"); break;
    case "choque": tom(t, 0.12, 200, 80, 0.4, "square"); chiado(t, 0.08, 1200, 1, 0.3); break;
    case "trompa": tom(t, 0.7, 147, 140, 0.18, "sawtooth"); tom(t, 0.7, 220, 210, 0.08, "sawtooth"); break;
    case "ordem": tom(t, 0.08, 660, 660, 0.08, "square"); tom(t + 0.09, 0.08, 880, 880, 0.08, "square"); break;
    case "raio": chiado(t, 0.14, 4200, 0.6, 0.3, "highpass"); tom(t, 0.1, 1800, 300, 0.1, "square"); break;
    case "gelo": chiado(t, 0.3, 5200, 2, 0.22, "bandpass", 2200); tom(t, 0.2, 1400, 900, 0.06, "triangle"); break;
    case "escudo": tom(t, 0.12, 330, 300, 0.2, "square"); chiado(t, 0.1, 1800, 2, 0.2); break;
    case "bloqueio": tom(t, 0.05, 1500, 1100, 0.12, "square"); break;
  }
}
