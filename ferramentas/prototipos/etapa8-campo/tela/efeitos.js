// PROTÓTIPO de campo livre: os efeitos visuais, só de tela. Lê os eventos de cada passo da simulação (sim.js) e
// cria o que se vê: os corpos arremessados (efeito, não física: quem morre já saiu da luta), as partículas de fogo,
// poeira e faíscas, os cortes, as explosões, as marcas no chão. Também diz quanto a câmera treme e quanto o tempo
// para no impacto (main.js aplica, com as opções do jogador). Nada aqui muda a batalha.
import { IMPACTO, CAMPO } from "./conteudo.js";

export function criarEfeitos(sorteio) {
  const marcas = document.createElement("canvas");
  marcas.width = CAMPO.largura;
  marcas.height = CAMPO.altura;
  return { voadores: [], particulas: [], cortes: [], aneis: [], explosoes: [], avisos: [], marcas,
    gm: marcas.getContext("2d"), trauma: 0, chute: { x: 0, y: 0 }, pausaPedida: 0, rng: sorteio, mensagens: [],
    sons: [], ordem: null };
}

const COR_EQUIPE = [["#76a8ea", "#4778c2"], ["#de6a58", "#ad4237"]];

function poeira(E, x, y, n, forca = 30, cor = "#b8a27a") {
  for (let i = 0; i < n; i++) {
    const a = E.rng() * Math.PI * 2, v = forca * (0.3 + E.rng() * 0.7);
    E.particulas.push({ x, y, z: 0.5, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.6, vz: 8 + E.rng() * 14,
      vida: 0, max: 0.35 + E.rng() * 0.3, cor, tam: E.rng() < 0.3 ? 2 : 1, g: 40, atrito: 4 });
  }
}

function brasas(E, x, y, n, forca) {
  for (let i = 0; i < n; i++) {
    const a = E.rng() * Math.PI * 2, v = forca * (0.4 + E.rng() * 0.8);
    E.particulas.push({ x, y, z: 2, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.7, vz: 20 + E.rng() * 50,
      vida: 0, max: 0.3 + E.rng() * 0.4, cor: E.rng() < 0.5 ? "#ffe08a" : "#ff8a30", tam: E.rng() < 0.25 ? 2 : 1,
      g: 90, atrito: 2.5, brilha: true });
  }
}

function fumaca(E, x, y, n, raio) {
  for (let i = 0; i < n; i++) {
    const a = E.rng() * Math.PI * 2, r = E.rng() * raio * 0.6;
    E.particulas.push({ x: x + Math.cos(a) * r, y: y + Math.sin(a) * r * 0.8, z: 3, vx: Math.cos(a) * 6,
      vy: Math.sin(a) * 4, vz: 10 + E.rng() * 8, vida: 0, max: 0.6 + E.rng() * 0.3, cor: "#3a342e", tam: 3,
      g: -4, atrito: 1, fumaca: true });
  }
}

function faiscas(E, x, y, dx, dy, n, cor = "#fff6d0") {
  for (let i = 0; i < n; i++) {
    const a = Math.atan2(dy, dx) + (E.rng() - 0.5) * 1.6, v = 50 + E.rng() * 60;
    E.particulas.push({ x, y, z: 5, vx: Math.cos(a) * v, vy: Math.sin(a) * v, vz: 10 + E.rng() * 20, vida: 0,
      max: 0.12 + E.rng() * 0.1, cor, tam: 1, g: 60, atrito: 6 });
  }
}

function tremer(E, valor, dx = 0, dy = 0) {
  E.trauma = Math.min(1, E.trauma + valor);
  E.chute.x += dx * valor * 3;
  E.chute.y += dy * valor * 3;
}

function marcaQueimada(E, x, y, raio) {
  // a marca do fogo: um miolo escuro e respingos, discreta (o chão não pode competir com quem ainda luta)
  const g = E.gm;
  for (let i = 0; i < raio * 2.2; i++) {
    const a = E.rng() * Math.PI * 2, r = Math.pow(E.rng(), 1.6) * raio;
    g.fillStyle = r < raio * 0.45 ? "rgba(34,26,18,0.35)" : "rgba(52,38,22,0.22)";
    g.fillRect(Math.round(x + Math.cos(a) * r), Math.round(y + Math.sin(a) * r * 0.8), r < raio * 0.45 ? 2 : 1, 1);
  }
}

function marcaRachada(E, x, y, raio) {
  const g = E.gm;
  g.fillStyle = "rgba(40,32,22,0.35)";
  for (let k = 0; k < 7; k++) {
    let a = (k / 7) * Math.PI * 2 + E.rng() * 0.5, px = x, py = y;
    for (let i = 0; i < raio * 0.5; i++) {
      a += (E.rng() - 0.5) * 0.5;
      px += Math.cos(a); py += Math.sin(a);
      g.fillRect(Math.round(px), Math.round(py), 1, 1);
    }
  }
}

/** Consome os eventos do passo: o que aparece, quanto treme, quanto para, que sons tocam. */
export function receber(E, eventos, m) {
  for (const e of eventos) {
    switch (e.tipo) {
      case "acerto": {
        if (e.forte) faiscas(E, e.x, e.y - 4, e.dx, e.dy, 3);
        else faiscas(E, e.x, e.y - 4, e.dx, e.dy, 2, "#ffffff");
        if (e.lado === 0 && e.alvo === "heroi") { E.sons.push("dor"); tremer(E, 0.05); }
        else E.sons.push(e.forte ? "impacto" : "acerto");
        break;
      }
      case "morte": {
        const voa = e.voa;
        E.voadores.push({ tipo: e.unidade, eq: e.lado, x: e.x, y: e.y, z: voa ? 2 : 0, vx: e.dx * e.vel,
          vy: e.dy * e.vel * 0.8, vz: e.sobe, t: 0, girando: voa, quiques: voa ? 1 : 0, virado: e.virado,
          giroDir: e.dx >= 0 ? 1 : -1 });
        if (voa) poeira(E, e.x, e.y, 3, 20);
        break;
      }
      case "inicio":
        if (e.id === "basico" && e.heroi === "guerreiro") E.sons.push(e.arremate ? "corteForte" : "corte");
        else if (e.id === "varredura" || e.id === "salto") E.sons.push("preparo");
        else if (e.id === "investida") { E.sons.push("investida"); poeira(E, m.heroi.x, m.heroi.y, 6, 25); }
        break;
      case "contato": {
        const forte = e.id !== "basico" || e.arremate;
        if (e.forma && e.forma.tipo === "arco") E.cortes.push({ forma: e.forma, t: 0, dur: forte ? 0.16 : 0.09, forte });
        if (e.id === "salto") {
          E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio + 6, t: 0, dur: 0.35, cor: "#e9dcb8" });
          poeira(E, e.x, e.y, 26, 70);
          marcaRachada(E, e.x, e.y, e.raio);
          E.sons.push("aterrissa");
        }
        if (e.id === "investida") { E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: e.raio, t: 0, dur: 0.2, cor: "#e9dcb8" }); poeira(E, e.x, e.y, 8, 40); }
        if (e.id === "bola") {
          E.explosoes.push({ x: e.x, y: e.y, raio: e.raio, t: 0, dur: 0.32 });
          brasas(E, e.x, e.y, 22, 70);
          fumaca(E, e.x, e.y, 6, e.raio);
          marcaQueimada(E, e.x, e.y, e.raio * 0.9);
          E.sons.push("explosao");
        }
        if (e.id === "piscar") {
          E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: e.raio, t: 0, dur: 0.25, cor: "#ffb15a" });
          brasas(E, e.x, e.y, 10, 50);
          E.aneis.push({ x: e.x1, y: e.y1, r0: 10, r1: 2, t: 0, dur: 0.18, cor: "#fff1c4" });
          E.sons.push("piscar");
        }
        if (e.id === "muralha") E.sons.push("fogo");
        if (e.id === "varredura") E.sons.push("varredura");
        if (e.tremor) tremer(E, e.tremor, Math.cos(e.dir || 0), Math.sin(e.dir || 0));
        if (e.pausa) E.pausaPedida = Math.max(E.pausaPedida, e.pausa);
        if (e.abates >= 4) E.mensagens.push({ texto: `${e.abates} derrubados`, t: 0, x: e.x ?? m.heroi.x, y: (e.y ?? m.heroi.y) - 18 });
        break;
      }
      case "disparo":
        E.sons.push(e.id === "bola" ? "lanca" : "faisca");
        break;
      case "faiscaAcerto": brasas(E, e.x, e.y, 4, 30); break;
      case "faiscaFim": brasas(E, e.x, e.y, 2, 15); break;
      case "flechaChao": {
        const g = E.gm;
        g.fillStyle = "rgba(90,62,34,0.8)";
        g.fillRect(Math.round(e.x), Math.round(e.y) - 1, 1, 2);
        break;
      }
      case "aviso": E.sons.push("aviso"); break;
      case "golpeCampeao":
        E.cortes.push({ forma: e.forma, t: 0, dur: 0.14, forte: true, inimigo: true });
        poeira(E, e.x + Math.cos(e.forma.ang) * 14, e.y + Math.sin(e.forma.ang) * 14, 10, 45);
        E.sons.push("aterrissa");
        if (e.heroi) tremer(E, 0.35);
        else tremer(E, 0.08);
        break;
      case "interrompe":
        E.mensagens.push({ texto: "interrompido", t: 0, x: e.x, y: e.y - 20 });
        E.sons.push("choque");
        break;
      case "choque": tremer(E, 0.25); E.sons.push("choque"); break;
      case "decolagem": E.sons.push("investida"); poeira(E, e.x, e.y, 10, 35); break;
      case "abalo": E.aneis.push({ x: e.x, y: e.y, r0: 8, r1: e.raio, t: 0, dur: 0.5, cor: "#f0cb62" }); E.sons.push("trompa"); break;
      case "reforco": E.sons.push("trompa"); break;
      case "ordem": E.ordem = { tipo: e.ordem, x: e.x, y: e.y, t: 0 }; E.sons.push("ordem"); break;
    }
  }
}

/** Avança os efeitos (fora da pausa de impacto e da pausa do jogo). */
export function avancar(E, dt) {
  E.trauma = Math.max(0, E.trauma - IMPACTO.tremorQueda * dt);
  const q = Math.exp(-18 * dt);
  E.chute.x *= q; E.chute.y *= q;
  const fica = [];
  for (const v of E.voadores) {
    v.t += dt;
    if (v.z > 0 || v.vz > 0) {
      v.vz -= 260 * dt;
      v.x += v.vx * dt; v.y += v.vy * dt; v.z += v.vz * dt;
      if (v.z <= 0) {
        v.z = 0;
        if (v.quiques > 0) {
          v.quiques--; v.vz = Math.abs(v.vz) * 0.28; v.vx *= 0.45; v.vy *= 0.45;
          poeira(E, v.x, v.y, 4, 18);
        } else {
          v.vz = 0;
        }
      }
      fica.push(v);
      continue;
    }
    // no chão: desliza um pouco e vira marca
    v.x += v.vx * dt; v.y += v.vy * dt;
    const a = Math.exp(-12 * dt);
    v.vx *= a; v.vy *= a;
    if (Math.hypot(v.vx, v.vy) <= 3 || v.t >= 1.5) v.pousar = true;
    fica.push(v);
  }
  E.voadores = fica;
  for (const p of E.particulas) {
    p.vida += dt;
    p.vx *= Math.exp(-p.atrito * dt); p.vy *= Math.exp(-p.atrito * dt);
    p.vz -= p.g * dt;
    p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
    if (p.z < 0) { p.z = 0; p.vz = 0; p.vx *= 0.5; p.vy *= 0.5; }
  }
  E.particulas = E.particulas.filter((p) => p.vida < p.max);
  if (E.particulas.length > 900) E.particulas.splice(0, E.particulas.length - 900);
  for (const lista of [E.cortes, E.aneis, E.explosoes, E.mensagens]) for (const c of lista) c.t += dt;
  E.cortes = E.cortes.filter((c) => c.t < c.dur);
  E.aneis = E.aneis.filter((c) => c.t < c.dur);
  E.explosoes = E.explosoes.filter((c) => c.t < c.dur);
  E.mensagens = E.mensagens.filter((c) => c.t < 0.9);
  if (E.ordem) { E.ordem.t += dt; if (E.ordem.t > 2.5 && E.ordem.tipo !== "defender") E.ordem = null; }
}

/** Os corpos que pousaram viram marca no chão (o caído, mais escuro); chamado pelo desenho, que tem os sprites. */
export function pousarCorpos(E, Q, todos) {
  const g = E.gm, ficam = [];
  for (const v of E.voadores) {
    if (!v.pousar && !todos) { ficam.push(v); continue; }
    const tipo = v.tipo === "heroi" ? null : v.tipo;
    if (!tipo || !Q[tipo]) continue;
    const s = Q[tipo][v.eq].caido;
    g.save();
    // o corpo no chão: apagado e escuro, para não se ler como alguém de pé
    g.globalAlpha = 0.7;
    g.filter = "saturate(0.3) brightness(0.55)";
    g.drawImage(v.giroDir > 0 ? s.d : s.e, Math.round(v.x - s.ax), Math.round(v.y - s.ay));
    g.filter = "none";
    g.restore();
  }
  E.voadores = ficam;
}

export { COR_EQUIPE };
