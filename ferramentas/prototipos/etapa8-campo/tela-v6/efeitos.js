// PROTÓTIPO de campo livre: os efeitos visuais, só de tela. Lê os eventos de cada passo da simulação (sim.js) e
// cria o que se vê: os corpos arremessados (efeito, não física: quem morre já saiu da luta), as partículas de fogo,
// poeira e faíscas, os cortes, as explosões, as marcas no chão. Também diz quanto a câmera treme e quanto o tempo
// para no impacto (main.js aplica, com as opções do jogador). Nada aqui muda a batalha.
import { IMPACTO, CAMPO } from "./conteudo.js";

export function criarEfeitos(sorteio) {
  const marcas = document.createElement("canvas");
  marcas.width = CAMPO.largura;
  marcas.height = CAMPO.altura;
  return { voadores: [], particulas: [], cortes: [], aneis: [], explosoes: [], avisos: [], marcas, numeros: [], raios: [],
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

// estilhaços de gelo e gotas de sangue
function gelo(E, x, y, n, raio) {
  for (let i = 0; i < n; i++) {
    const a = E.rng() * Math.PI * 2, r = Math.sqrt(E.rng()) * raio, v = 20 + E.rng() * 40;
    E.particulas.push({ x: x + Math.cos(a) * r, y: y + Math.sin(a) * r * 0.8, z: 2, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.7,
      vz: 15 + E.rng() * 25, vida: 0, max: 0.3 + E.rng() * 0.25, cor: E.rng() < 0.5 ? "#ffffff" : "#9fd8ff", tam: 1, g: 70, atrito: 3 });
  }
}
function sangue(E, x, y, n) {
  for (let i = 0; i < n; i++) {
    const a = E.rng() * Math.PI * 2, v = 20 + E.rng() * 40;
    E.particulas.push({ x, y: y - 3, z: 3, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.6, vz: 10 + E.rng() * 20, vida: 0,
      max: 0.3 + E.rng() * 0.2, cor: E.rng() < 0.6 ? "#c8282a" : "#7a1416", tam: 1, g: 80, atrito: 3 });
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

// Os números de dano do herói. Um por acerto, com o valor que saiu da vida; o crítico é maior e laranja, o golpe forte
// amarelo, o básico branco. O dano contínuo (fogo, sangramento) soma por alvo: um tique que chega até 0,6 s depois do
// anterior entra no mesmo número, que se renova; parado mais que isso, o próximo começa outro.
export const NUMEROS = { vida: 0.7, somaContinuo: 0.6, maximo: 70 };
function numeroDeDano(E, e) {
  if (e.sofrido) {
    // o dano que o herói levou: vermelho, em cima dele (o valor que saiu da vida); o que chega até 0,35 s depois do
    // último entra no mesmo número, que se renova
    const j = E.numeros.find((n) => n.tipo === "sofrido" && n.t < 0.35);
    if (j) { j.valor += e.valor; j.t = 0; j.x = e.x; j.y = e.y - 16; return; }
    E.numeros.push({ id: -1, x: e.x + (E.rng() - 0.5) * 4, y: e.y - 16, dx: e.dx || 0, valor: e.valor, tipo: "sofrido", t: 0,
      ultimo: 0, continuo: null });
    return;
  }
  if (e.sutil) {
    const j = E.numeros.find((n) => n.id === e.id && n.continuo === e.elemento && n.t - n.ultimo < NUMEROS.somaContinuo);
    if (j) { j.valor += e.valor; j.ultimo = j.t; j.t = Math.min(j.t, 0.15); j.ultimo = j.t; return; }
  }
  const tipo = e.sutil ? e.elemento || "fogo" : e.critico ? "critico" : e.forte ? "forte" : "normal";
  E.numeros.push({ id: e.id, x: e.x + (E.rng() - 0.5) * 6, y: e.y - 13, dx: e.dx || 0, valor: e.valor, tipo, t: 0, ultimo: 0,
    continuo: e.sutil ? e.elemento : null });
  if (E.numeros.length > NUMEROS.maximo) E.numeros.splice(0, E.numeros.length - NUMEROS.maximo);
}

/** Consome os eventos do passo: o que aparece, quanto treme, quanto para, que sons tocam. */
export function receber(E, eventos, m) {
  for (const e of eventos) {
    switch (e.tipo) {
      case "dano":
        numeroDeDano(E, e);
        if (e.fagulha) brasas(E, e.x, e.y - 4, 8, 40);   // a Fagulha consumida: um estouro de brasas no alvo
        break;
      case "heroiAtingido": {
        // de onde veio e quanto pesou: a marca vermelha no anel do herói, do lado de quem bateu; o número vermelho (os
        // golpes que chegam juntos somam num número só, para um enxame não encher a tela); o som pelo peso (o golpe de
        // uma ameaça tem o próprio); a câmera proporcional ao golpe
        const forca = Math.min(1, e.valor / 30);
        E.golpeHeroi = { ang: Math.atan2(-(e.dy || 0), -(e.dx || 0)), t: 0, dur: 0.35 + 0.3 * forca, forca, sem: !e.dx && !e.dy };
        numeroDeDano(E, { ...e, sofrido: true });
        E.sons.push(e.fonte === "lider" || e.fonte === "campeao" ? "golpeAmeaca" : e.valor >= 15 ? "choque" : "dor");
        tremer(E, Math.min(0.5, 0.04 + e.valor / 70), e.dx || 0, e.dy || 0);
        break;
      }
      case "liderRodopio":
        E.cortes.push({ forma: e.forma, t: 0, dur: 0.2, forte: true, inimigo: true });
        E.aneis.push({ x: e.x, y: e.y, r0: 8, r1: e.raio + 4, t: 0, dur: 0.3, cor: "#ff8a78" });
        poeira(E, e.x, e.y, 16, 60);
        tremer(E, e.heroi ? 0.4 : 0.15);
        E.sons.push("varredura");
        break;
      case "resiste": E.mensagens.push({ texto: "firme", t: 0, x: e.x, y: e.y - 20 }); break;
      case "carga": tremer(E, 0.2); poeira(E, e.x, e.y, 12, 40); E.sons.push("investida"); break;
      case "liderSalto": poeira(E, e.x, e.y, 10, 35); E.sons.push("investida"); break;
      case "liderPouso":
        E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio + 6, t: 0, dur: 0.35, cor: "#ff8a78" });
        poeira(E, e.x, e.y, 20, 60);
        marcaRachada(E, e.x, e.y, e.raio);
        tremer(E, e.heroi ? 0.45 : 0.2);
        E.sons.push("aterrissa");
        break;
      case "bloqueio": faiscas(E, e.x, e.y - 4, e.dx, e.dy, 3, "#d8f4ff"); E.sons.push("bloqueio"); break;
      case "fimCarga": poeira(E, e.x, e.y, 10, 35); E.sons.push("aterrissa"); break;
      case "liderCaiu":
        E.aneis.push({ x: e.x, y: e.y, r0: 8, r1: e.raio, t: 0, dur: 0.7, cor: "#ff6a4a" });
        tremer(E, 0.5); E.pausaPedida = Math.max(E.pausaPedida, 90); E.sons.push("trompa");
        break;
      case "acerto": {
        if (e.forte) faiscas(E, e.x, e.y - 4, e.dx, e.dy, 3);
        else faiscas(E, e.x, e.y - 4, e.dx, e.dy, 2, "#ffffff");
        if (!(e.lado === 0 && e.alvo === "heroi")) E.sons.push(e.forte ? "impacto" : "acerto");
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
        if (e.id === "varredura" || e.id === "corteSangrento" || e.id === "salto" || e.id === "terremoto") E.sons.push("preparo");
        else if (e.id === "escudo") E.sons.push("escudo");
        else if (e.id === "investida") { E.sons.push("investida"); poeira(E, m.heroi.x, m.heroi.y, 6, 25); }
        break;
      case "contato": {
        const forte = e.id !== "basico" || e.arremate;
        if (e.forma && e.forma.tipo === "arco") E.cortes.push({ forma: e.forma, t: 0, dur: forte ? 0.16 : 0.09, forte });
        if (e.turbilhao) {
          // o Turbilhão: o giro em volta do herói e a poeira do monte que ele juntou
          E.cortes.push({ forma: e.forma, t: 0, dur: 0.18, forte: true });
          E.aneis.push({ x: e.x, y: e.y, r0: e.puxa, r1: e.raio, t: 0, dur: 0.2, cor: "#e9dcb8" });
          poeira(E, e.x, e.y, 16, 55);
          E.sons.push("varredura");
        } else if (e.id === "salto") {
          E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio + 6, t: 0, dur: 0.35, cor: "#e9dcb8" });
          poeira(E, e.x, e.y, 26, 70);
          marcaRachada(E, e.x, e.y, e.raio);
          E.sons.push("aterrissa");
        }
        if (e.id === "investida") { E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: e.raio, t: 0, dur: 0.2, cor: "#e9dcb8" }); poeira(E, e.x, e.y, 8, 40); }
        if (e.raios) {
          // a Corrente de Raios: o traço que salta de alvo em alvo e uma faísca em cada um
          E.raios.push({ pontos: e.pontos, t: 0, dur: 0.24, semente: Math.floor(E.rng() * 1000) });
          for (const p of e.pontos.slice(1)) faiscas(E, p.x, p.y, 0, -1, 3, "#d8f4ff");
          E.sons.push("raio");
        } else if (e.id === "bola" || e.meteoro) {
          E.explosoes.push({ x: e.x, y: e.y, raio: e.raio, t: 0, dur: 0.32 });
          brasas(E, e.x, e.y, 22, 70);
          fumaca(E, e.x, e.y, 6, e.raio);
          marcaQueimada(E, e.x, e.y, e.raio * 0.9);
          E.sons.push("explosao");
        } else if (e.estilhacante) {
          // a Lança Estilhaçante: a explosão de gelo
          E.explosoes.push({ x: e.x, y: e.y, raio: e.raio, t: 0, dur: 0.28, cor: "gelo" });
          gelo(E, e.x, e.y, 16, e.raio);
          E.sons.push("gelo");
        } else if (e.implosao) {
          E.explosoes.push({ x: e.x, y: e.y, raio: e.raio, t: 0, dur: 0.3, cor: "arcano" });
          E.aneis.push({ x: e.x, y: e.y, r0: e.raio * 2, r1: 4, t: 0, dur: 0.25, cor: "#c9a0ff" });
          E.sons.push("explosao");
        }
        if (e.id === "vortice" && !e.implosao) { E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: e.raio, t: 0, dur: 0.3, cor: "#c9a0ff" }); E.sons.push("piscar"); }
        if (e.id === "ignicao") { E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio, t: 0, dur: 0.3, cor: "#ffb15a" }); brasas(E, e.x, e.y, 14, 50); E.sons.push("fogo"); }
        if (e.id === "ruptura") { E.aneis.push({ x: e.x, y: e.y, r0: 8, r1: e.raio, t: 0, dur: 0.3, cor: "#ff5a5a" }); E.sons.push("varredura"); }
        if (e.id === "furia") { E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: 40, t: 0, dur: 0.4, cor: "#ff6a4a" }); E.sons.push("trompa"); }
        if (e.id === "corteSangrento") E.sons.push("varredura");
        if (e.id === "piscar") {
          E.aneis.push({ x: e.x, y: e.y, r0: 4, r1: e.raio, t: 0, dur: 0.25, cor: "#ffb15a" });
          brasas(E, e.x, e.y, 10, 50);
          E.aneis.push({ x: e.x1, y: e.y1, r0: 10, r1: 2, t: 0, dur: 0.18, cor: "#fff1c4" });
          E.sons.push("piscar");
        }
        if (e.gelo) {
          E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio, t: 0, dur: 0.3, cor: "#d8f4ff" });
          for (let i = 0; i < 18; i++) {
            const a = E.rng() * Math.PI * 2, r = Math.sqrt(E.rng()) * e.raio;
            E.particulas.push({ x: e.x + Math.cos(a) * r, y: e.y + Math.sin(a) * r * 0.8, z: 1, vx: 0, vy: 0, vz: 18 + E.rng() * 20,
              vida: 0, max: 0.35 + E.rng() * 0.25, cor: E.rng() < 0.5 ? "#ffffff" : "#9fd8ff", tam: 1, g: 60, atrito: 2 });
          }
          E.sons.push("gelo");
        } else if (e.id === "muralha" || e.id === "anel") E.sons.push("fogo");
        if (e.id === "grito") { E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.raio, t: 0, dur: 0.4, cor: "#f0cb62" }); E.sons.push("trompa"); }
        if (e.id === "varredura") E.sons.push("varredura");
        if (e.tremor) tremer(E, e.tremor, Math.cos(e.dir || 0), Math.sin(e.dir || 0));
        if (e.pausa) E.pausaPedida = Math.max(E.pausaPedida, e.pausa);
        if (e.abates >= 6) E.mensagens.push({ texto: `${e.abates} derrubados`, t: 0, x: e.x ?? m.heroi.x, y: (e.y ?? m.heroi.y) - 18 });
        break;
      }
      case "disparo":
        E.sons.push(e.id === "lanca" ? "gelo" : e.id === "sismico" ? "aterrissa" : "lanca");
        if (e.id === "sismico") tremer(E, 0.12, Math.cos(e.dir), Math.sin(e.dir));
        break;
      case "linhaAcerto":
        if (e.id === "lanca") gelo(E, e.x, e.y, 4, 4); else poeira(E, e.x, e.y, 4, 30);
        E.sons.push("acerto");
        break;
      case "linhaFim": if (e.id === "lanca") gelo(E, e.x, e.y, 3, 3); else poeira(E, e.x, e.y, 6, 30); break;
      case "terremotoAnel":
        E.aneis.push({ x: e.x, y: e.y, r0: Math.max(4, e.raio - 40), r1: e.raio, t: 0, dur: 0.3, cor: "#e9dcb8" });
        poeira(E, e.x, e.y, 18, 40 + e.raio * 0.4);
        marcaRachada(E, e.x, e.y, e.raio * 0.6);
        tremer(E, e.ultimo ? 0.5 : 0.25);
        E.sons.push("aterrissa");
        break;
      case "explosao": {
        // as explosões dos talentos: a cor diz de onde vêm (gelo, fogo, sangue); o som tem intervalo mínimo
        const cor = e.de === "estilhacar" ? "gelo" : e.de === "ignicao" ? null : "sangue";
        E.explosoes.push({ x: e.x, y: e.y, raio: e.raio, t: 0, dur: 0.26, cor });
        if (cor === "gelo") gelo(E, e.x, e.y, 8, e.raio * 0.6);
        else if (cor === "sangue") sangue(E, e.x, e.y, 8);
        else brasas(E, e.x, e.y, 10, 50);
        E.sons.push(cor === "gelo" ? "gelo" : "explosao");
        break;
      }
      case "congela": gelo(E, e.x, e.y, 6, 5); break;
      case "estilhaca": gelo(E, e.x, e.y, 10, 6); break;
      case "flechaChao": {
        const g = E.gm;
        g.fillStyle = "rgba(90,62,34,0.8)";
        g.fillRect(Math.round(e.x), Math.round(e.y) - 1, 1, 2);
        break;
      }
      case "aviso": E.sons.push(e.lider ? "trompa" : "aviso"); break;
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
      case "horda": E.sons.push("trompa"); poeira(E, e.x, e.y, 14, 40); break;
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
  for (const lista of [E.cortes, E.aneis, E.explosoes, E.mensagens, E.numeros, E.raios]) for (const c of lista) c.t += dt;
  if (E.golpeHeroi) { E.golpeHeroi.t += dt; if (E.golpeHeroi.t >= E.golpeHeroi.dur) E.golpeHeroi = null; }
  E.raios = E.raios.filter((c) => c.t < c.dur);
  E.numeros = E.numeros.filter((n) => n.t < NUMEROS.vida);
  E.cortes = E.cortes.filter((c) => c.t < c.dur);
  E.aneis = E.aneis.filter((c) => c.t < c.dur);
  E.explosoes = E.explosoes.filter((c) => c.t < c.dur);
  E.mensagens = E.mensagens.filter((c) => c.t < 0.9);
  if (E.ordem) { E.ordem.t += dt; if (E.ordem.t > 2.5 && E.ordem.tipo !== "defender") E.ordem = null; }
}

const apagados = new Map();
function apagado(img) {
  let c = apagados.get(img);
  if (!c) {
    c = document.createElement("canvas");
    c.width = img.width; c.height = img.height;
    const g = c.getContext("2d");
    g.filter = "saturate(0.3) brightness(0.55)";
    g.drawImage(img, 0, 0);
    apagados.set(img, c);
  }
  return c;
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
    // o corpo no chão: apagado e escuro, para não se ler como alguém de pé (feito uma vez por sprite e guardado: o
    // filtro a cada corpo pesava quando uma área derrubava quinze de uma vez)
    g.globalAlpha = 0.7;
    g.drawImage(apagado(v.giroDir > 0 ? s.d : s.e), Math.round(v.x - s.ax), Math.round(v.y - s.ay));
    g.restore();
  }
  E.voadores = ficam;
}

export { COR_EQUIPE };
