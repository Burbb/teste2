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
    sons: [], ordem: null, pecas: [], violencia: 2, arte: "atual", lampejos: [], correntes: [] };
}

// ------------------------------------------------------------------------------------------------ a carnificina
// Campo Livre 7: a batalha deixa marcas, só na tela (nada disto muda a luta). `E.violencia` (0 desligada, 1 contida,
// 2 normal, 3 intensa) multiplica o sangue e decide o desmembramento; os corpos, as armas caídas e as queimaduras ficam
// em qualquer nível. Tudo vai para a camada de marcas do chão (E.marcas), desenhada embaixo dos vivos e dos avisos: uma
// mancha nunca cobre uma ameaça nem parece alguém de pé. Cada gota e cada peça é carimbada uma vez, ao pousar.
export const VIOLENCIA = [
  { nome: "Desligada", sangue: 0, poca: 0, pedaco: 0 },
  { nome: "Contida", sangue: 0.5, poca: 0.6, pedaco: 0 },
  { nome: "Normal", sangue: 1, poca: 1, pedaco: 0.3 },
  { nome: "Intensa", sangue: 1.6, poca: 1.4, pedaco: 0.6 },
];
const SANGUE_COR = { atual: ["rgba(150,22,24,0.85)", "rgba(96,14,16,0.85)"], sobria: ["rgba(132,24,24,0.85)", "rgba(84,14,16,0.85)"],
  sombria: ["rgba(110,18,18,0.9)", "rgba(66,10,12,0.9)"] };
const corSangue = (E, k = 0) => (SANGUE_COR[E.arte] || SANGUE_COR.atual)[k];
const nivel = (E) => VIOLENCIA[E.violencia] || VIOLENCIA[2];

// gotas que saem na direção do golpe e mancham o chão onde caem
function borrifo(E, x, y, dx, dy, n, forca = 50) {
  n = Math.round(n * nivel(E).sangue);
  for (let i = 0; i < n; i++) {
    const a = Math.atan2(dy || E.rng() - 0.5, dx || E.rng() - 0.5) + (E.rng() - 0.5) * 0.9, v = forca * (0.4 + E.rng() * 0.8);
    E.particulas.push({ x, y, z: 4, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.7, vz: 6 + E.rng() * 16, vida: 0, max: 1.2,
      cor: E.rng() < 0.6 ? "#b8201f" : "#7a1416", tam: 1, g: 90, atrito: 2.5, mancha: true });
  }
}

// a poça embaixo de um corpo: um borrão irregular, mais escuro no meio
function poca(E, x, y, r) {
  r *= nivel(E).poca;
  if (r < 1) return;
  const g = E.gm;
  for (let i = 0; i < r * r * 2.2; i++) {
    const a = E.rng() * Math.PI * 2, d = Math.pow(E.rng(), 0.7) * r;
    g.fillStyle = corSangue(E, d < r * 0.5 ? 1 : 0);
    g.fillRect(Math.round(x + Math.cos(a) * d * 1.4), Math.round(y + Math.sin(a) * d * 0.8), 1, 1);
  }
}

// as peças que caem de quem morre: a arma, o elmo; no golpe forte, às vezes a cabeça ou um braço. [cor, x, y]
const PECAS = {
  espada: [["#c8ccd2", 0, 0], ["#c8ccd2", 1, 0], ["#c8ccd2", 2, 0], ["#6a4521", 3, 0]],
  lanca: [["#6a4521", 0, 0], ["#6a4521", 1, 0], ["#6a4521", 2, 0], ["#6a4521", 3, 0], ["#c8ccd2", 4, 0]],
  arco: [["#7a5734", 0, 0], ["#7a5734", 1, 1], ["#7a5734", 2, 1], ["#7a5734", 3, 0]],
  elmo: [["#8a8e98", 0, 0], ["#8a8e98", 1, 0], ["#5d6170", 0, 1], ["#5d6170", 1, 1]],
  cabeca: [["#c99a7a", 0, 0], ["#c99a7a", 1, 0], ["#8a8e98", 0, -1], ["#8f6249", 1, 1]],
  braco: [["#8f6249", 0, 0], ["#c99a7a", 1, 0], ["#5d6170", 2, 0]],
};
const ARMA_DE = { soldado: "espada", veterano: "espada", arqueiro: "arco", pesado: "lanca", cavaleiro: "lanca", estandarte: "lanca", magoBatalha: "lanca" };
function peca(E, forma, x, y, dx, dy, forca, sangra) {
  const a = Math.atan2(dy, dx) + (E.rng() - 0.5) * 1.2, v = forca * (0.5 + E.rng() * 0.7);
  E.pecas.push({ forma, x, y, z: 6, vx: Math.cos(a) * v, vy: Math.sin(a) * v * 0.7, vz: 30 + E.rng() * 40, giro: E.rng() < 0.5 ? 1 : 3, sangra, t: 0 });
}
function carimbar(E, p) {
  const g = E.gm, q = p.giro % 2;
  for (const [cor, i, j] of PECAS[p.forma]) { g.fillStyle = cor; g.fillRect(Math.round(p.x + (q ? j : i)), Math.round(p.y + (q ? i : j)), 1, 1); }
  if (p.sangra) poca(E, p.x + 1, p.y + 1, 1.6);
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
  const tipo = e.abertura && !e.sutil ? "abertura" : e.sutil ? e.elemento || "fogo" : e.critico ? "critico" : e.forte ? "forte" : "normal";
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
        // Campo Livre 8: em Harg, cada acerto confirma (faíscas e o som de impacto, sem pará-lo); na abertura ou com a
        // postura quebrada, a confirmação forte: o anel dourado, brasas e um tremor curto
        if (e.chefe) {
          faiscas(E, e.x, e.y - 5, e.dx || 0, e.dy || 0, e.abertura ? 7 : 4, e.abertura ? "#ffe08a" : "#fff6d0");
          E.sons.push("impacto");
          if (e.abertura) { E.aneis.push({ x: e.x, y: e.y - 3, r0: 4, r1: 16, t: 0, dur: 0.22, cor: "#ffd84a" }); tremer(E, 0.16, e.dx || 0, e.dy || 0); }
        }
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
        // o golpe fraco só respinga na violência intensa: o chão fica com borrifos na direção dos golpes, não pontilhado
        borrifo(E, e.x, e.y - 3, e.dx, e.dy, e.forte ? 4 : E.violencia >= 3 ? 1 : 0, e.forte ? 60 : 35);
        if (!(e.lado === 0 && e.alvo === "heroi")) E.sons.push(e.forte ? "impacto" : "acerto");
        break;
      }
      case "morte": {
        const voa = e.voa;
        E.voadores.push({ tipo: e.unidade, eq: e.lado, x: e.x, y: e.y, z: voa ? 2 : 0, vx: e.dx * e.vel,
          vy: e.dy * e.vel * 0.8, vz: e.sobe, t: 0, girando: voa, quiques: voa ? 1 : 0, virado: e.virado,
          giroDir: e.dx >= 0 ? 1 : -1 });
        if (voa) poeira(E, e.x, e.y, 3, 20);
        // a carnificina: o sangue na direção do golpe, a arma (às vezes o elmo) caindo e, no golpe forte, às vezes a
        // cabeça ou um braço (só nas tropas comuns e no nível de violência que pede)
        const dx = e.dx || 0, dy = e.dy || 0, arma = ARMA_DE[e.unidade];
        borrifo(E, e.x, e.y - 3, dx, dy, voa ? 8 : 4, voa ? 80 : 45);
        if (arma && E.rng() < 0.7) peca(E, arma, e.x, e.y - 3, dx, dy, 30 + (e.vel || 0) * 0.4, false);
        if (arma && arma !== "arco" && E.rng() < 0.25) peca(E, "elmo", e.x, e.y - 6, dx, dy, 25, false);
        if (voa && arma && e.unidade !== "cavaleiro" && E.rng() < nivel(E).pedaco) {
          peca(E, E.rng() < 0.5 ? "cabeca" : "braco", e.x, e.y - 6, dx, dy, 70 + (e.vel || 0) * 0.5, true);
          borrifo(E, e.x, e.y - 6, dx, dy, 6, 90);
        }
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
        else if (cor === "sangue") { sangue(E, e.x, e.y, 8); poca(E, e.x, e.y, 3); }
        else { brasas(E, e.x, e.y, 10, 50); marcaQueimada(E, e.x, e.y, e.raio * 0.8); }   // as magias de fogo também queimam o chão
        E.sons.push(cor === "gelo" ? "gelo" : "explosao");
        break;
      }
      case "congela": gelo(E, e.x, e.y, 6, 5); break;
      case "hargContato":
        // Campo Livre 9: o estouro de cada forma exata (a faixa da Estocada, os anéis, a cruz, o leque); o anel do
        // Terremoto racha o chão e levanta poeira na borda
        for (const f of e.formas || (e.forma && e.forma.tipo === "faixa" ? [e.forma] : [])) {
          E.lampejos.push({ forma: f, t: 0, dur: f.tipo === "anel" ? 0.22 : 0.16 });
          if (f.tipo === "anel") { poeira(E, f.x + f.raio * 0.7, f.y, 6, 40); poeira(E, f.x - f.raio * 0.7, f.y, 6, 40); marcaRachada(E, f.x, f.y, f.raio * 0.5); }
        }
        if (e.formas && e.quem === "general") tremer(E, e.heroi ? 0.5 : 0.25);
        if (e.forma && e.forma.tipo === "arco") E.cortes.push({ forma: e.forma, t: 0, dur: 0.16, forte: true, inimigo: true });
        if (e.forma && e.forma.tipo === "circulo") { E.aneis.push({ x: e.forma.x, y: e.forma.y, r0: 6, r1: e.forma.raio + 4, t: 0, dur: 0.28, cor: "#ff8a78" }); marcaRachada(E, e.forma.x, e.forma.y, e.forma.raio); poeira(E, e.forma.x, e.forma.y, 18, 60); }
        if (e.onda) E.aneis.push({ x: e.onda.x, y: e.onda.y, r0: e.forma.raio, r1: e.onda.raio, t: 0, dur: 0.35, cor: "#ffb08a" });
        if (e.golpe === "investida") poeira(E, e.x, e.y, 14, 50);
        tremer(E, e.heroi ? 0.4 : 0.12 + Math.min(0.2, (e.mortos || 0) * 0.03));
        E.sons.push(e.golpe === "martelada" || e.golpe === "rugido" ? "aterrissa" : "golpeAmeaca");
        if (e.mortos >= 4) E.mensagens.push({ texto: `${e.mortos} derrubados`, t: 0, x: e.x, y: e.y - 22 });
        break;
      case "hargExec":
        if (e.golpe === "investida" || e.golpe === "salto") { E.sons.push("investida"); poeira(E, e.x, e.y, 10, 40); }
        break;
      // ---- Campo Livre 9: a guerra nova
      case "puxao": {
        // a corrente fica entre ele e quem foi puxado enquanto a pessoa está presa
        const fonte = m.unidades.find((u) => u.id === e.fonte), alvo = m.unidades.find((u) => u.id === e.id);
        E.correntes.push({ fonte, alvo, t: 0, dur: 0.5 });
        poeira(E, e.de.x, e.de.y, 6, 30); poeira(E, e.para.x, e.para.y, 8, 40);
        E.sons.push("bloqueio");
        break;
      }
      case "recuo9": fumaca(E, e.de.x, e.de.y, 6, 6); fumaca(E, e.para.x, e.para.y, 4, 5); E.sons.push("piscar"); break;
      case "pavio9": E.sons.push("fogo"); break;
      case "barril9": E.mensagens.push({ texto: "barril caído", t: 0, x: e.x, y: e.y - 14 }); E.sons.push("aviso"); break;
      case "cura9": if (e.valor >= 3) E.mensagens.push({ texto: `+${Math.round(e.valor)}`, t: 0, x: e.x, y: e.y - 22 }); break;
      case "congela9": gelo(E, e.x, e.y, 10, 6); E.sons.push("gelo"); break;
      case "veneno9":
        E.particulas.push({ x: e.x + (E.rng() - 0.5) * 6, y: e.y, z: 6, vx: 0, vy: 0, vz: 10, vida: 0, max: 0.4, cor: "#8fe06a", tam: 1, g: 30, atrito: 2 });
        break;
      case "heroi9Entra": case "general9Entra":
        E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: e.tipo === "general9Entra" ? 70 : 34, t: 0, dur: 0.6, cor: "#ff6a4a" });
        tremer(E, e.tipo === "general9Entra" ? 0.5 : 0.2); E.sons.push("trompa");
        break;
      case "general9Vem": E.sons.push("trompa"); break;
      case "pelotao9": poeira(E, e.x, e.y, 14, 40); break;
      case "heroi9Caiu":
        E.aneis.push({ x: e.x, y: e.y, r0: 8, r1: e.general ? 90 : 40, t: 0, dur: 0.7, cor: "#ffd84a" });
        E.mensagens.push({ texto: "caiu", t: 0, x: e.x, y: e.y - 24 });
        tremer(E, e.general ? 0.6 : 0.35); E.pausaPedida = Math.max(E.pausaPedida, e.general ? 140 : 80); E.sons.push("trompa");
        break;
      case "hargQuebra":
        E.aneis.push({ x: e.x, y: e.y - 4, r0: 4, r1: 30, t: 0, dur: 0.45, cor: "#ffe08a" });
        brasas(E, e.x, e.y - 6, 24, 70);
        E.mensagens.push({ texto: "postura quebrada", t: 0, x: e.x, y: e.y - 26 });
        tremer(E, 0.5); E.pausaPedida = Math.max(E.pausaPedida, 90); E.sons.push("choque");
        break;
      case "hargFase":
        E.aneis.push({ x: e.x, y: e.y, r0: 6, r1: 64, t: 0, dur: 0.5, cor: "#ff5a48" });
        E.mensagens.push({ texto: "fúria", t: 0, x: e.x, y: e.y - 26 });
        tremer(E, 0.35); E.sons.push("trompa");
        break;
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
    // no chão: desliza um pouco e vira marca; o arrasto deixa um rastro curto de sangue
    if (Math.hypot(v.vx, v.vy) > 8 && nivel(E).sangue > 0) { E.gm.fillStyle = corSangue(E, 0); E.gm.fillRect(Math.round(v.x), Math.round(v.y - 1), 1, 1); }
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
    if (p.z < 0) {
      // a gota de sangue que pousa vira mancha (e sai das partículas)
      if (p.mancha) { E.gm.fillStyle = corSangue(E, p.cor === "#7a1416" ? 1 : 0); E.gm.fillRect(Math.round(p.x), Math.round(p.y), 1, 1); p.vida = p.max; }
      p.z = 0; p.vz = 0; p.vx *= 0.5; p.vy *= 0.5;
    }
  }
  const pecasNoAr = [];
  for (const p of E.pecas) {
    p.vz -= 220 * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.z += p.vz * dt;
    if (p.sangra && E.rng() < 0.3) E.particulas.push({ x: p.x, y: p.y, z: p.z, vx: 0, vy: 0, vz: 0, vida: 0, max: 1, cor: "#b8201f", tam: 1, g: 90, atrito: 1, mancha: true });
    if (p.z <= 0) { carimbar(E, p); continue; }
    if ((p.t += dt) > 0.1) { p.t = 0; p.giro++; }
    pecasNoAr.push(p);
  }
  E.pecas = pecasNoAr;
  E.particulas = E.particulas.filter((p) => p.vida < p.max);
  if (E.particulas.length > 900) E.particulas.splice(0, E.particulas.length - 900);
  for (const lista of [E.cortes, E.aneis, E.explosoes, E.mensagens, E.numeros, E.raios, E.lampejos, E.correntes]) for (const c of lista) c.t += dt;
  E.lampejos = E.lampejos.filter((c) => c.t < c.dur);
  E.correntes = E.correntes.filter((c) => c.t < c.dur);
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
    poca(E, v.x, v.y - 1, v.girando ? 3.2 : 2.4);   // a poça embaixo do corpo, antes dele
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
