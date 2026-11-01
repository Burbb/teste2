// PROTÓTIPO tático por turnos da etapa 8 (nada no jogo): a tela. Monta a preparação, desenha a arena, mostra o que
// cada ação vai fazer antes de confirmar (a prévia vem de regras.prever, a mesma conta da ação) e anima o que aconteceu
// (os eventos de regras.js), sem decidir regra nenhuma. Os inimigos jogam pela IA (ia.js), uma ação de cada vez.
// Parâmetros de endereço (testes e demonstração): ?classe=mago&build=Piromante&enc=passagem&auto=1&robo=1
// (auto: começa a luta direto; robo: a IA também joga pelos aliados; rapido=1: animações curtas).
import { VERSAO, HABILIDADES, TALENTOS, CLASSES, COMPANHEIROS, ENCONTROS, BUILDS, ESTADOS, MAX_TALENTOS, ARENAS } from "./conteudo.js";
import { criarLuta, atual, alcancaveis, alvosValidos, podeLancar, lancar, mover, encerrarVez, prever, areaDe, unidade,
  unidadeEm, alcanceDe, dist, visao, naArena, descricao, montarKit, talentosValidos } from "./regras.js";
import { melhorOpcao, melhorCasa } from "./ia.js";
import { prepararSprites } from "./sprites.js";
import { desenharArena, desenharFantasmas, casaEm, proj, TW, TH } from "./desenho.js";

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const url = new URLSearchParams(location.search);
const canvas = $("#arena"), g = canvas.getContext("2d", { alpha: false });
const nat = document.createElement("canvas"), gn = nat.getContext("2d");
const Q = prepararSprites();
const RAPIDO = !!url.get("rapido");

// ------------------------------------------------------------------------------------------------ opções
const PADRAO = { classe: "guerreiro", encontro: "aberto", montagem: {} };
for (const c of Object.keys(CLASSES)) { const [nome] = Object.keys(BUILDS[c]); PADRAO.montagem[c] = structuredClone(BUILDS[c][nome]); }
const opcoes = structuredClone(PADRAO);
try { Object.assign(opcoes, JSON.parse(localStorage.getItem("tatico2-opcoes") || "{}")); } catch { /* sem armazenamento */ }
if (url.get("classe") && CLASSES[url.get("classe")]) opcoes.classe = url.get("classe");
if (url.get("enc") && ENCONTROS[url.get("enc")]) opcoes.encontro = url.get("enc");
if (url.get("build") && BUILDS[opcoes.classe][url.get("build")]) opcoes.montagem[opcoes.classe] = structuredClone(BUILDS[opcoes.classe][url.get("build")]);
function guardar() { try { localStorage.setItem("tatico2-opcoes", JSON.stringify(opcoes)); } catch { /* idem */ } }

// ------------------------------------------------------------------------------------------------ estado da tela
const st = {
  tela: "preparar", m: null, disp: {}, mirando: null, hover: null, prev: null, animando: false, fila: [],
  efeitos: [], numeros: [], t: 0, escala: 2, ox: 0, oy: 0, robo: !!url.get("robo"), registroAberto: false,
};

function mostrar(tela) {
  st.tela = tela;
  $("#tela-preparar").hidden = tela !== "preparar";
  $("#tela-fim").hidden = tela !== "fim";
  $("#hud").hidden = tela === "preparar";
  document.body.classList.toggle("em-luta", tela !== "preparar");
}

// ------------------------------------------------------------------------------------------------ a luta
function novaLuta() {
  const mt = opcoes.montagem[opcoes.classe];
  st.m = criarLuta({ heroi: { classe: opcoes.classe, kit: mt.kit, talentos: mt.talentos }, encontro: opcoes.encontro });
  st.m.eventos = [];
  st.disp = {};
  for (const u of st.m.unidades) st.disp[u.id] = { x: u.x, y: u.y, pv: u.pv, vivo: true, mostrar: true, pose: "parado", dir: u.lado === 0 ? "d" : "e", clarao: 0 };
  st.mirando = null; st.prev = null; st.efeitos = []; st.numeros = []; st.fila = [];
  st.inicio = Object.fromEntries(st.m.unidades.map((u) => [u.id, `${u.x},${u.y}`]));
  dimensionar();
  mostrar("luta");
  montarOrdem();
  faixa(`${ENCONTROS[opcoes.encontro].nome}. ${ENCONTROS[opcoes.encontro].texto}`, 5);
  aposMudanca();
  proximaVez();
}

/** Depois de cada vez: se é da IA (inimigo, ou aliado no modo robô), ela joga; senão, espera o jogador. */
async function proximaVez() {
  const m = st.m;
  while (!m.fim && st.tela === "luta" && (atual(m).lado === 1 || st.robo)) {
    await vezDaIA();
    if (m.fim || st.tela !== "luta") break;
    encerrarVez(m);
    await animar();
    aposMudanca();
  }
  if (m.fim) return fimDaLuta();
  aposMudanca();
}

async function vezDaIA() {
  const m = st.m, u = atual(m);
  await esperar(RAPIDO ? 0.05 : 0.35);
  for (let i = 0; i < 6 && !m.fim && u.vivo; i++) {
    const op = melhorOpcao(m, u);
    if (!op) break;
    if (op.casa[0] !== u.x || op.casa[1] !== u.y) { mover(m, u, ...op.casa); await animar(); aposMudanca(); }
    if (!u.vivo || m.fim) break;
    if (!lancar(m, u, op.hab, ...op.alvo)) break;
    await animar(); aposMudanca();
    await esperar(RAPIDO ? 0.02 : 0.2);
  }
  if (u.vivo && !m.fim && u.pm > 0) {
    const c = melhorCasa(m, u);
    if (c && (c[0] !== u.x || c[1] !== u.y)) { mover(m, u, ...c); await animar(); aposMudanca(); }
  }
}

function fimDaLuta() {
  const m = st.m, vivos = (l) => m.unidades.filter((u) => u.lado === l && u.vivo);
  $("#fim-titulo").textContent = m.fim === "vitoria" ? "Vitória" : "Derrota";
  const caidos = m.unidades.filter((u) => u.lado === 0 && !u.vivo).map((u) => u.nome);
  $("#fim-resumo").textContent = `${ENCONTROS[m.encontro].nome}, ${m.rodada} ${m.rodada === 1 ? "rodada" : "rodadas"}. ` +
    (m.fim === "vitoria" ? `Os cinco inimigos caíram. ${caidos.length ? `Caíram do seu lado: ${caidos.join(", ")}.` : "Ninguém do seu lado caiu."}`
      : `Inimigos de pé: ${vivos(1).map((u) => u.nome).join(", ")}.`);
  setTimeout(() => { if (st.m === m) mostrar("fim"); }, 600);
}

// ------------------------------------------------------------------------------------------------ ações do jogador
function vezDoJogador() { return st.m && !st.m.fim && !st.animando && atual(st.m).lado === 0 && !st.robo && st.tela === "luta"; }

function mirar(id) {
  if (!vezDoJogador()) return;
  const u = atual(st.m);
  if (!u.kit[id]) return;
  if (!podeLancar(st.m, u, id).ok) { faixa(podeLancar(st.m, u, id).motivo, 1.5); return; }
  st.mirando = st.mirando === id ? null : id;
  st.prev = null;
  aposMudanca();
}

function cancelar() { st.mirando = null; st.prev = null; aposMudanca(); }

async function clicarCasa(x, y) {
  if (!vezDoJogador()) return;
  const m = st.m, u = atual(m);
  if (st.mirando) {
    const id = st.mirando;
    if (!alvosValidos(m, u, id).some(([a, b]) => a === x && b === y)) { cancelar(); return; }
    st.mirando = null; st.prev = null;
    lancar(m, u, id, x, y);
    await animar();
    aposMudanca();
    if (m.fim) fimDaLuta();
    return;
  }
  const r = alcancaveis(m, u).get(`${x},${y}`);
  if (r && r.caminho.length) { mover(m, u, x, y); await animar(); aposMudanca(); if (m.fim) fimDaLuta(); }
}

async function encerrar() {
  if (!vezDoJogador()) return;
  st.mirando = null; st.prev = null;
  encerrarVez(st.m);
  await animar();
  aposMudanca();
  proximaVez();
}

// ------------------------------------------------------------------------------------------------ animação
// Os eventos de regras.js viram passos de animação; a posição e a vida mostradas (disp) andam junto, e no fim tudo
// volta a bater com a luta.
const esperar = (s) => new Promise((r) => setTimeout(r, s * 1000));
const dur = (s) => (RAPIDO ? s * 0.25 : s);

async function animar() {
  const m = st.m;
  if (!m) return;
  const evs = m.eventos.splice(0);
  st.animando = true;
  for (const e of evs) await animarEvento(e);
  // tudo volta a bater com a luta
  for (const u of m.unidades) {
    const d = st.disp[u.id];
    d.x = u.x; d.y = u.y; d.pv = u.pv; d.pose = u.vivo ? "parado" : "caido";
    if (!u.vivo && d.vivo) d.vivo = false;
  }
  st.animando = false;
}

function tween(segundos, f) {
  return new Promise((r) => {
    const t0 = performance.now();
    const passo = () => {
      const k = Math.min(1, (performance.now() - t0) / (segundos * 1000));
      f(k);
      if (k < 1) requestAnimationFrame(passo); else r();
    };
    requestAnimationFrame(passo);
  });
}

function virar(d, de, para) {
  const [ax] = proj(...de), [bx] = proj(...para);
  if (bx > ax) d.dir = "d"; else if (bx < ax) d.dir = "e";
}

const COR_EL = { fogo: "#ffb040", gelo: "#bfe8ff", raio: "#d8ecff", luz: "#fff2b0", veneno: "#9fe070", fisico: "#ffffff", colisao: "#ffd0a0" };

async function animarEvento(e) {
  const m = st.m, d = e.id ? st.disp[e.id] : null;
  switch (e.t) {
    case "andar": {
      let [px, py] = [d.x, d.y];
      for (const [x, y] of e.caminho) {
        virar(d, [px, py], [x, y]);
        const ax = px, ay = py;
        await tween(dur(0.13), (k) => { d.x = ax + (x - ax) * k; d.y = ay + (y - ay) * k; d.pose = k < 0.5 ? "andarA" : "andarB"; });
        px = x; py = y;
      }
      d.pose = "parado";
      break;
    }
    case "salto": case "empurra": {
      const [ax, ay] = e.de, [bx, by] = e.para;
      if (e.t === "salto") virar(d, e.de, e.para);
      if (e.piscar) { await tween(dur(0.12), (k) => { d.alfa = 1 - k; }); d.x = bx; d.y = by; await tween(dur(0.12), (k) => { d.alfa = k; }); d.alfa = null; break; }
      const alto = e.t === "salto" ? 8 : 0;
      await tween(dur(e.t === "salto" ? 0.22 : 0.16), (k) => { d.x = ax + (bx - ax) * k; d.y = ay + (by - ay) * k; d.salto = -Math.round(Math.sin(k * Math.PI) * alto); d.pose = e.t === "empurra" ? "recuo" : "golpe"; });
      d.salto = 0; d.pose = "parado";
      if (e.bateu) efeito({ tipo: "estouro", c: e.bateu, cor: "#ffd0a0", dur: 0.3, r: 8 });
      break;
    }
    case "lanca": {
      const k = unidade(m, e.id).kit[e.hab];
      virar(d, [d.x, d.y], [e.x, e.y]);
      d.pose = "preparo";
      await esperar(dur(0.12));
      d.pose = "golpe";
      const longe = dist(Math.round(d.x), Math.round(d.y), e.x, e.y) > 1 && !k.esp?.match(/investida|piscar|recuo|raios|perfurante/);
      const el = k.efeitos.find((x) => x.el)?.el || "fisico";
      if (longe && k.alvo !== "si") { efeito({ tipo: "linha", de: [d.x, d.y], para: [e.x, e.y], cor: COR_EL[el], dur: dur(0.18) }); await esperar(dur(0.18)); }
      if (k.area && k.alvo !== "si") efeito({ tipo: "casas", celulas: areaDe(m, unidade(m, e.id), k, e.x, e.y), cor: el === "fogo" ? "rgba(255,150,60,0.6)" : "rgba(255,255,255,0.35)", dur: 0.35 });
      if (k.alvo === "si" && k.area) efeito({ tipo: "estouro", c: [d.x, d.y], cor: "#ffe08a", dur: 0.3, r: 18 });
      await esperar(dur(0.1));
      d.pose = "parado";
      break;
    }
    case "raio": efeito({ tipo: "raio", de: e.de || e.para, para: e.para, dur: 0.2 }); await esperar(dur(0.08)); break;
    case "flecha": efeito({ tipo: "linha", de: e.de, para: e.para, cor: "#ffffff", dur: dur(0.16) }); await esperar(dur(0.16)); break;
    case "dano": {
      d.pv -= e.v; d.clarao = 0.25;
      numero(e.id, `-${e.v}`, e.el === "colisao" ? "#ffcf9a" : e.el === "fogo" ? "#ffb35a" : "#ff6a5a");
      await esperar(dur(0.06));
      break;
    }
    case "cura": if (e.v > 0) { d.pv += e.v; numero(e.id, `+${e.v}`, "#9bf08a"); } break;
    case "estado": numero(e.id, ESTADOS[e.e].nome, ESTADOS[e.e].ruim ? "#ffb0a0" : "#bcd8ff", true); break;
    case "morre": d.vivo = false; d.pose = "caido"; await esperar(dur(0.25)); setTimeout(() => { d.mostrar = false; }, 900); break;
    case "explode": efeito({ tipo: "estouro", c: [e.x, e.y], cor: "#ff9a30", dur: 0.45, r: e.pequeno ? 10 : 22 }); await esperar(dur(0.12)); break;
    case "esmaga": efeito({ tipo: "casas", celulas: e.celulas, cor: "rgba(255,80,60,0.7)", dur: 0.5 }); d.pose = "golpe"; await esperar(dur(0.3)); d.pose = "parado"; break;
    case "armadilha": efeito({ tipo: "estouro", c: [e.x, e.y], cor: "#e8d070", dur: 0.4, r: 12 }); await esperar(dur(0.15)); break;
    case "vez": faixaVez(e.id); break;
    default: break;
  }
}

function efeito(e) { st.efeitos.push({ ...e, t0: st.t }); }
function numero(id, texto, cor, pequeno = false) {
  const d = st.disp[id];
  const ja = st.numeros.filter((n) => n.id === id && st.t - n.t0 < 0.4).length;
  st.numeros.push({ id, texto, cor, t0: st.t, x: d.x, y: d.y, pequeno, deslocY: ja * 12 });
}

// ------------------------------------------------------------------------------------------------ HUD
function faixa(texto, segundos = 2.5) {
  const el = $("#faixa");
  el.textContent = texto;
  el.classList.add("ver");
  clearTimeout(faixa.t);
  faixa.t = setTimeout(() => el.classList.remove("ver"), segundos * 1000);
}
function faixaVez(id) {
  const u = unidade(st.m, id);
  if (!u || !u.vivo) return;
  faixa(u.lado === 0 ? (st.robo ? `Vez de ${u.nome}` : `Sua vez: ${u.nome}`) : `Vez de ${u.nome}`, 1.4);
}

// o retrato da ordem é o próprio sprite (de corpo inteiro, sem moldura redonda)
const miniaturas = {};
function miniatura(u) {
  const chave = `${u.modelo}:${u.lado}`;
  if (!miniaturas[chave]) {
    const img = Q[u.modelo][u.lado === 0 ? 0 : 1].parado, c = document.createElement("canvas");
    c.width = img.w; c.height = img.h;
    c.getContext("2d").drawImage(u.lado === 0 ? img.d : img.e, 0, 0);
    miniaturas[chave] = c;
  }
  return miniaturas[chave];
}

function montarOrdem() {
  const raiz = $("#ordem");
  raiz.innerHTML = "";
  for (const id of st.m.ordem) {
    const u = unidade(st.m, id), d = document.createElement("div"), c = document.createElement("canvas"), img = miniatura(u);
    d.className = `vez ${u.lado === 0 ? "aliado" : "inimigo"}`;
    d.dataset.id = id;
    c.width = img.width * 2; c.height = img.height * 2;
    const gc = c.getContext("2d"); gc.imageSmoothingEnabled = false; gc.drawImage(img, 0, 0, c.width, c.height);
    c.style.width = `${img.width * 2}px`; c.style.height = `${Math.min(36, img.height * 2)}px`; c.style.objectFit = "contain";
    d.append(c);
    const barra = document.createElement("i"); barra.append(document.createElement("b")); d.append(barra);
    d.title = u.nome;
    d.addEventListener("mouseenter", () => { st.infoId = id; atualizarInfo(); });
    d.addEventListener("mouseleave", () => { st.infoId = null; atualizarInfo(); });
    raiz.append(d);
  }
}

function atualizarOrdem() {
  const m = st.m;
  for (const el of $$("#ordem .vez")) {
    const u = unidade(m, el.dataset.id), d = st.disp[u.id];
    el.classList.toggle("atual", m.ordem[m.vez] === u.id && !m.fim);
    el.classList.toggle("morto", !d.vivo);
    el.querySelector("b").style.width = `${Math.max(0, (100 * d.pv) / u.pvMax)}%`;
  }
  $("#rodada").textContent = `Rodada ${m.rodada}`;
}

/** A linha de regra de uma habilidade, no formato comum: "3 PA · Alcance 1–6 · Em linha · Recarga 2 turnos". */
export function linhaRegra(k, u) {
  const p = [`${k.pa} PA`];
  if (k.alvo === "si" && !k.area) p.push("Em si");
  else if (k.alvo === "si") p.push("Em volta de si");
  else {
    const [a, b] = u ? alcanceDe(u, k) : k.alcance;
    p.push(a === b ? `Alcance ${a}` : `Alcance ${a}–${b}`);
  }
  if (k.linha) p.push("Em linha");
  if (k.visao === false) p.push("Sem linha de visão");
  if (k.porTurno) p.push(`${k.porTurno}× por turno`);
  if (k.porAlvo) p.push(`${k.porAlvo}× por alvo`);
  if (k.recarga && k.recarga > 1) p.push(`Recarga ${k.recarga} turnos`);
  else if (k.recarga === 1) p.push("1× por turno");
  return p.join(" · ");
}

function estadosHtml(u) {
  return u.estados.map((s) => {
    const e = ESTADOS[s.e];
    return `<span class="${e.ruim ? "ruim" : "bom"}" title="${e.texto(s.v)}">${e.nome}${s.v && s.e !== "lento" ? ` ${s.v}` : ""} · ${s.turnos}</span>`;
  }).join("");
}

function atualizarFicha() {
  const m = st.m, u = atual(m), d = st.disp[u.id];
  $("#ficha").innerHTML = `<div class="nome">${u.nome}<small>${u.lado === 0 ? (st.robo ? "jogador automático" : "sua vez") : "inimigo"}</small></div>` +
    `<div class="pontos"><span class="pa">PA <b>${u.pa}</b>/${u.paMax}</span><span class="pm">PM <b>${u.pm}</b>/${u.pmMax}</span></div>` +
    `<div class="vida"><i style="width:${Math.max(0, (100 * d.pv) / u.pvMax)}%"></i><span>${Math.max(0, d.pv)}/${u.pvMax}</span></div>` +
    `<div class="estados">${estadosHtml(u)}</div>`;
  $("#encerrar").disabled = !vezDoJogador();
}

function atualizarBarra() {
  const m = st.m, u = atual(m), raiz = $("#barra");
  raiz.innerHTML = "";
  if (u.lado !== 0 || st.robo) return;
  Object.values(u.kit).forEach((k, i) => {
    const b = document.createElement("button"), pode = podeLancar(m, u, k.id);
    b.type = "button";
    b.className = "hab" + (st.mirando === k.id ? " mirando" : "") + (pode.ok ? "" : " indisponivel");
    b.innerHTML = `<span class="tecla">${i + 1}</span><span class="nome">${k.nome}</span><span class="custo">${k.pa} PA</span>${pode.ok ? "" : `<span class="motivo">${pode.motivo}</span>`}`;
    b.addEventListener("click", () => mirar(k.id));
    b.addEventListener("mouseenter", () => { st.dicaHab = k.id; atualizarDica(); });
    b.addEventListener("mouseleave", () => { st.dicaHab = null; atualizarDica(); });
    raiz.append(b);
  });
}

function atualizarDica() {
  const el = $("#dica"), m = st.m;
  const id = st.dicaHab || st.mirando;
  if (!m || !id || atual(m).lado !== 0) { el.hidden = true; return; }
  const u = atual(m), k = u.kit[id], pode = podeLancar(m, u, id);
  el.hidden = false;
  el.innerHTML = `<b>${k.nome}</b><div class="regra">${linhaRegra(k, u)}</div><p>${descricao(u.dono, k)}</p>` +
    (pode.ok ? "" : `<p class="motivo">${pode.motivo}</p>`);
}

function atualizarInfo() {
  const el = $("#info"), m = st.m;
  if (!m || st.registroAberto) { el.hidden = true; return; }
  let u = st.infoId ? unidade(m, st.infoId) : st.hover ? unidadeEm(m, ...st.hover) : null;
  if (!u || !u.vivo) { el.hidden = true; return; }
  el.hidden = false;
  const kit = Object.values(u.kit).map((k) => k.nome).join(", ");
  el.innerHTML = `<b>${u.nome}</b> <span class="linha">· ${u.lado === 0 ? "aliado" : "inimigo"}</span>` +
    `<div class="linha">Vida ${u.pv}/${u.pvMax} · PA ${u.paMax} · PM ${u.pmMax}${u.pesado ? " · pesado (bloqueio 2)" : ""}${u.agil ? " · não sofre bloqueio" : ""}</div>` +
    `<div class="linha">${kit}</div>` +
    u.estados.map((s) => `<div class="estado"><b>${ESTADOS[s.e].nome}</b> · ${s.turnos} ${s.turnos === 1 ? "turno" : "turnos"}: ${ESTADOS[s.e].texto(s.v)}</div>`).join("");
}

function atualizarRegistro() {
  const el = $("#registro");
  el.hidden = !st.registroAberto;
  if (!st.registroAberto || !st.m) return;
  el.querySelector("ol").innerHTML = st.m.registro.slice(-60).map((r) => `<li><small>R${r.rodada}</small>${r.texto}</li>`).join("");
  el.scrollTop = el.scrollHeight;
}

/** Depois de qualquer mudança: as marcas da arena (andar, mirar) e a HUD. */
function aposMudanca() {
  if (!st.m) return;
  atualizarMarcas();
  atualizarOrdem();
  atualizarFicha();
  atualizarBarra();
  atualizarDica();
  atualizarInfo();
  atualizarRegistro();
}

// ------------------------------------------------------------------------------------------------ marcas na arena
const hl = {};
function atualizarMarcas() {
  for (const k of Object.keys(hl)) delete hl[k];
  st.prev = null; st.custoCaminho = null;
  if (!vezDoJogador()) return;
  const m = st.m, u = atual(m);
  if (st.mirando) {
    const k = u.kit[st.mirando], [a, b] = alcanceDe(u, k), validos = alvosValidos(m, u, st.mirando);
    const ehValido = (x, y) => validos.some(([p, q]) => p === x && q === y);
    hl.alcance = []; hl.semVisao = []; hl.alvos = [];
    for (let y = 0; y < m.h; y++) for (let x = 0; x < m.w; x++) {
      if (!naArena(m, x, y)) continue;
      const d = dist(u.x, u.y, x, y);
      if (d < a || d > b || (k.linha && x !== u.x && y !== u.y)) continue;
      if (ehValido(x, y)) (unidadeEm(m, x, y) ? hl.alvos : hl.alcance).push([x, y]);
      else if (k.visao !== false && !visao(m, u.x, u.y, x, y)) hl.semVisao.push([x, y]);
      else hl.alcance.push([x, y]);
    }
    if (k.alvo === "si") { hl.alcance = []; hl.alvos = []; }
    const alvo = k.alvo === "si" ? [u.x, u.y] : st.hover;
    if (alvo && ehValido(...alvo)) {
      st.prev = prever(m, u.id, st.mirando, ...alvo);
      const cel = areaDe(m, u, k, ...alvo);
      hl.area = cel.filter(([x, y]) => { const w = unidadeEm(m, x, y); return !w || w.lado !== u.lado; });
      hl.areaAliado = cel.filter(([x, y]) => { const w = unidadeEm(m, x, y); return w && w.lado === u.lado; });
      if (k.esp === "raios" || k.esp === "perfurante" || k.esp === "investida" || k.esp === "recuo") hl.area = [...hl.area, ...st.prev.mud.map((d) => d.de)];
    }
    return;
  }
  const r = alcancaveis(m, u);
  hl.alcanc = [...r.values()].filter((c) => c.caminho.length).map((c) => [c.x, c.y]);
  if (st.hover) {
    const c = r.get(`${st.hover[0]},${st.hover[1]}`);
    if (c && c.caminho.length) { hl.caminho = c.caminho; st.custoCaminho = c.custo; } else st.custoCaminho = null;
  }
}

// ------------------------------------------------------------------------------------------------ desenho
function dimensionar() {
  const W = innerWidth, H = innerHeight;
  canvas.width = W; canvas.height = H;
  if (!st.m) return;
  const m = st.m, natW = (m.w + m.h) * (TW / 2) + 8, natH = (m.w + m.h) * (TH / 2) + 44;
  nat.width = natW; nat.height = natH;
  const topo = 64, baixo = 84;
  st.escala = Math.max(1, Math.floor(Math.min((W - 20) / natW, (H - topo - baixo) / natH)));
  st.ox = Math.round((W - natW * st.escala) / 2);
  st.oy = Math.round(topo + (H - topo - baixo - natH * st.escala) / 2);
  st.orig = [m.h * (TW / 2) + 4, 36];   // a origem da casa 0,0 no buffer nativo
}

function quadro(agora) {
  st.t = agora / 1000;
  const W = canvas.width, H = canvas.height;
  g.fillStyle = "#23301f"; g.fillRect(0, 0, W, H);
  if (st.m && st.tela !== "preparar") {
    gn.setTransform(1, 0, 0, 1, 0, 0);
    gn.fillStyle = "#23301f"; gn.fillRect(0, 0, nat.width, nat.height);
    gn.setTransform(1, 0, 0, 1, ...st.orig);
    for (const d of Object.values(st.disp)) if (d.clarao > 0) d.clarao = Math.max(0, d.clarao - 1 / 60);
    st.efeitos = st.efeitos.filter((e) => st.t - e.t0 < e.dur);
    const view = { m: st.m, disp: st.disp, Q, hl, hover: st.hover, atual: st.m.fim ? null : atual(st.m), prev: st.prev, t: st.t, efeitos: st.efeitos };
    desenharArena(gn, view);
    desenharFantasmas(gn, view);
    g.imageSmoothingEnabled = false;
    g.drawImage(nat, st.ox, st.oy, nat.width * st.escala, nat.height * st.escala);
    desenharTextos();
  }
  requestAnimationFrame(quadro);
}

// os números e as etiquetas, na resolução da tela (nítidos), por cima da arena
function naTela(x, y) { const [sx, sy] = proj(x, y); return [st.ox + (sx + st.orig[0]) * st.escala, st.oy + (sy + st.orig[1] + TH / 2) * st.escala]; }
function desenharTextos() {
  g.textAlign = "center"; g.textBaseline = "middle";
  // a prévia: o dano ou a cura em cada um, e quem cai
  if (st.prev) for (const d of st.prev.mud) {
    const u = unidade(st.m, d.id), disp = st.disp[u.id], [x, y] = naTela(disp.x, disp.y);
    const alt = 30 * st.escala;
    const partes = [];
    if (d.dPv) partes.push([d.dPv < 0 ? `${d.dPv}` : `+${d.dPv}`, d.dPv < 0 ? "#ff7a66" : "#9bf08a"]);
    if (d.morre) partes.push(["cai", "#ffd36a"]);
    for (const e of d.estados) partes.push([ESTADOS[e].nome, ESTADOS[e].ruim ? "#ffb0a0" : "#bcd8ff"]);
    partes.forEach(([t, cor], i) => texto(t, x, y - alt - i * 15, cor, i === 0 ? 15 : 12));
  }
  if (st.custoCaminho != null && hl.caminho && st.hover) {
    const [x, y] = naTela(...st.hover);
    texto(`${st.custoCaminho} PM`, x, y - 4 * st.escala, "#fff4b0", 13);
  }
  st.numeros = st.numeros.filter((n) => st.t - n.t0 < 1.1);
  for (const n of st.numeros) {
    const k = (st.t - n.t0) / 1.1, [x, y] = naTela(n.x, n.y);
    texto(n.texto, x, y - (26 + k * 14) * st.escala - n.deslocY, n.cor, n.pequeno ? 12 : 17, 1 - Math.max(0, k - 0.6) * 2.5);
  }
}
function texto(t, x, y, cor, tam, alfa = 1) {
  g.globalAlpha = Math.max(0, alfa);
  g.font = `${tam}px "Pixeloid Sans", monospace`;
  g.lineWidth = 3; g.strokeStyle = "#120e14"; g.strokeText(t, x, y);
  g.fillStyle = cor; g.fillText(t, x, y);
  g.globalAlpha = 1;
}

// ------------------------------------------------------------------------------------------------ entrada
canvas.addEventListener("mousemove", (e) => {
  if (!st.m) return;
  const px = (e.clientX - st.ox) / st.escala - st.orig[0], py = (e.clientY - st.oy) / st.escala - st.orig[1];
  const [x, y] = casaEm(px, py);
  const h = naArena(st.m, x, y) ? [x, y] : null;
  if (String(h) !== String(st.hover)) { st.hover = h; atualizarMarcas(); atualizarInfo(); }
});
canvas.addEventListener("mouseleave", () => { st.hover = null; atualizarMarcas(); atualizarInfo(); });
canvas.addEventListener("click", () => { if (st.hover) clicarCasa(...st.hover); });
canvas.addEventListener("contextmenu", (e) => { e.preventDefault(); cancelar(); });
addEventListener("resize", () => dimensionar());
addEventListener("keydown", (e) => {
  if (st.tela === "preparar") { if (e.key === "Enter") { e.preventDefault(); novaLuta(); } return; }
  if (st.tela === "fim") {
    if (e.key === "r" || e.key === "R") novaLuta();
    if (e.key === "p" || e.key === "P") irPreparar();
    return;
  }
  if (e.key === "Escape") cancelar();
  else if (e.key === " " || e.key === "e" || e.key === "E") { e.preventDefault(); encerrar(); }
  else if (e.key === "Tab") { e.preventDefault(); st.registroAberto = !st.registroAberto; atualizarRegistro(); atualizarInfo(); }
  else if (e.key === "p" || e.key === "P") irPreparar();
  else if (/^[1-6]$/.test(e.key) && st.m) { const ids = Object.keys(atual(st.m).kit); if (ids[+e.key - 1]) mirar(ids[+e.key - 1]); }
});
$("#encerrar").addEventListener("click", encerrar);
$("#abrir-registro").addEventListener("click", () => { st.registroAberto = !st.registroAberto; atualizarRegistro(); atualizarInfo(); });
$("#ir-preparar").addEventListener("click", () => irPreparar());
$("#repetir").addEventListener("click", () => novaLuta());
$("#voltar").addEventListener("click", () => irPreparar());
$("#lutar").addEventListener("click", () => novaLuta());
function irPreparar() { st.m = null; montarPreparar(); mostrar("preparar"); }

// ------------------------------------------------------------------------------------------------ preparação
function sprite(modelo, lado = 0) {
  const img = Q[modelo][lado].parado, c = document.createElement("canvas");
  c.width = img.w * 2; c.height = img.h * 2;
  const gc = c.getContext("2d"); gc.imageSmoothingEnabled = false; gc.drawImage(img.d, 0, 0, c.width, c.height);
  return c;
}

function montarPreparar() {
  const enc = $("#encontros");
  enc.innerHTML = "";
  for (const [id, e] of Object.entries(ENCONTROS)) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "cartao" + (opcoes.encontro === id ? " escolhido" : "");
    b.innerHTML = `<b>${e.nome}</b><p>${e.texto}</p>`;
    b.addEventListener("click", () => { opcoes.encontro = id; guardar(); montarPreparar(); });
    enc.append(b);
  }
  const cls = $("#classes");
  cls.innerHTML = "";
  for (const [id, c] of Object.entries(CLASSES)) {
    const b = document.createElement("button");
    b.type = "button"; b.className = "cartao classe" + (opcoes.classe === id ? " escolhido" : "");
    b.append(sprite(c.modelo));
    const t = document.createElement("div");
    t.innerHTML = `<b>${c.nome}</b>Vida ${c.pv} · PA ${c.pa} · PM ${c.pm}`;
    b.append(t);
    b.addEventListener("click", () => { opcoes.classe = id; guardar(); montarPreparar(); });
    cls.append(b);
  }
  montarMontagem();
  const comp = $("#companheiros");
  comp.innerHTML = "";
  for (const [id, c] of Object.entries(COMPANHEIROS)) {
    const kit = montarKit(id, c.kit), d = document.createElement("div");
    d.innerHTML = `<h3>${c.nome} · Vida ${c.pv} · PA ${c.pa} · PM ${c.pm}${c.pesado ? " · pesado (bloqueio 2)" : ""}</h3>` +
      Object.values(kit).map((k) => `<div class="item"><div class="cab"><b>${k.nome}</b><span>${linhaRegra(k)}</span></div><p>${descricao(id, k)}</p></div>`).join("");
    comp.append(d);
  }
}

function montarMontagem() {
  const c = opcoes.classe, mt = opcoes.montagem[c], cat = HABILIDADES[c], raiz = $("#montagem"), tam = CLASSES[c].tamKit;
  const kit = montarKit(c, Object.keys(cat), talentosValidos(c, mt.kit, mt.talentos));
  const atalhos = Object.keys(BUILDS[c]).map((n) => `<button type="button" data-build="${n}">${n}</button>`).join("");
  const habs = Object.entries(cat).map(([id]) => {
    const k = kit[id], marcado = mt.kit.includes(id), cheio = !marcado && mt.kit.length >= tam;
    return `<div class="item${marcado ? " marcado" : ""}"><button type="button" class="marca" data-hab="${id}" aria-pressed="${marcado}" ${cheio ? "disabled" : ""}>${marcado ? "✓" : ""}</button>` +
      `<div class="cab"><b>${k.nome}</b><span>${linhaRegra(k)}</span></div><p>${descricao(c, k)}</p><small>${k.papel}</small></div>`;
  }).join("");
  const tals = Object.entries(TALENTOS[c]).map(([id, t]) => {
    const marcado = mt.talentos.includes(id), falta = t.requer && !mt.kit.includes(t.requer), cheio = !marcado && mt.talentos.length >= MAX_TALENTOS;
    const motivo = falta ? `Requer ${cat[t.requer].nome}` : cheio ? "Já há 2" : "";
    return `<div class="item${marcado ? " marcado" : ""}"><button type="button" class="marca" data-tal="${id}" aria-pressed="${marcado}" ${(falta || cheio) && !marcado ? "disabled" : ""}>${marcado ? "✓" : ""}</button>` +
      `<div class="cab"><b>${t.nome}</b>${motivo ? `<em>${motivo}</em>` : ""}</div><p>${t.texto}</p></div>`;
  }).join("");
  raiz.innerHTML = `<div><h3>Habilidades: escolha ${tam} (${mt.kit.length}/${tam}) <span class="atalhos">· Montagens prontas: ${atalhos}</span></h3>${habs}</div>` +
    `<div><h3>Talentos: escolha ${MAX_TALENTOS} (${mt.talentos.length}/${MAX_TALENTOS})</h3>${tals}</div>`;
  raiz.onclick = (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.build) opcoes.montagem[c] = structuredClone(BUILDS[c][b.dataset.build]);
    if (b.dataset.hab) {
      const id = b.dataset.hab;
      mt.kit = mt.kit.includes(id) ? mt.kit.filter((x) => x !== id) : mt.kit.length < tam ? [...mt.kit, id] : mt.kit;
      // na ordem do catálogo (as teclas 1-6 seguem essa ordem)
      mt.kit = Object.keys(cat).filter((x) => mt.kit.includes(x));
      mt.talentos = talentosValidos(c, mt.kit, mt.talentos);
    }
    if (b.dataset.tal) {
      const id = b.dataset.tal;
      mt.talentos = mt.talentos.includes(id) ? mt.talentos.filter((x) => x !== id) : [...mt.talentos, id];
      mt.talentos = talentosValidos(c, mt.kit, mt.talentos);
    }
    guardar();
    montarMontagem();
    $("#lutar").disabled = opcoes.montagem[c].kit.length !== tam;
  };
  $("#lutar").disabled = mt.kit.length !== tam;
}

// ------------------------------------------------------------------------------------------------ começo
document.title = `${VERSAO} · protótipo da etapa 8`;
$("#selo").textContent = `${VERSAO} · protótipo da etapa 8, nada no jogo`;
document.querySelector(".caixa h1").firstChild.textContent = VERSAO + " ";
try { if (typeof Sprites !== "undefined") Sprites.publicar(); } catch { /* sem a paleta do jogo: as cores de reserva do CSS */ }
montarPreparar();
mostrar("preparar");
dimensionar();
requestAnimationFrame(quadro);
if (url.get("auto")) novaLuta();

// para os testes de navegador: o estado de agora, sem mexer em nada
window.tatico = { st, atual: () => st.m && atual(st.m), ARENAS };
