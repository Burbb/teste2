// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): o laço, os comandos, a câmera, a pausa de impacto, a HUD e as
// telas. A batalha avança em passos fixos de 1/60 s (sim.js); o desenho interpola entre dois passos. A pausa de
// impacto para a simulação e os efeitos por alguns milissegundos; os comandos apertados nesse meio-tempo esperam e
// saem no passo seguinte. Parâmetros de URL (para testes, medição e vídeos):
// ?heroi=mago&qtd=maior&enc=capitao&kit=sangrenta,grito&auto=1&robo=1.
//
// O modo de comando (Campo Livre 2): com Shift segurado, ou com o jogo pausado, o botão esquerdo deixa de atacar e
// arrasta um retângulo que seleciona tropas; o direito manda a seleção defender o ponto. F1/F2 selecionam por tipo,
// F4 todas, X limpa; 1/2/3 ordenam a seleção (sem seleção, o exército inteiro). A mira, o retângulo e a seleção usam a
// câmera sem tremor: o tremor é só visual, e o mouse aponta para o mesmo lugar com ou sem ele.
//
// A câmera no modo de comando (Campo Livre 3): o mouse deixa de deslocar a câmera (o quanto ela olhava para o lado do
// mouse fica parado); durante o arrasto, a câmera não se mexe nem para seguir o herói, e o retângulo seleciona
// exatamente o que está mostrado; o tremor se acalma (a intensidade escolhida não muda). Ao sair, o olhar volta para o
// mouse em ~0,5 s e o tremor volta em ~0,3 s, sem salto.
import { VERSAO, HEROIS, ORDENS, IMPACTO, CAMPO, CONTINGENTES, ENCONTROS, VARIANTES, TIPOS } from "./conteudo.js";
import { criarMundo, passo, entradaVazia, ordenar, resumo, sorteio, PASSO, selecionar, tropasDoTipo, montarKit as kitDoHeroi,
  escalaDe } from "./sim.js";
import { criarEfeitos, receber, avancar } from "./efeitos.js";
import { prepararSprites } from "./sprites.js";
import { criarChao, desenhar, BORDA } from "./desenho.js";
import { criarRobo, pensar } from "./robo.js";
import { iniciarSom, ajustarSom, tocar } from "./som.js";

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const url = new URLSearchParams(location.search);
const canvas = $("#campo"), g = canvas.getContext("2d", { alpha: false });
const Q = prepararSprites();
const chao = criarChao(sorteio(4242));

// ------------------------------------------------------------------------------------------------ opções
// o tremor começa no máximo (150%), a intensidade de que o Jean gostou; 0 desliga
const PADRAO = { tremor: 150, pausa: true, volume: 50, mudo: false, areas: true, heroi: "guerreiro", quantidade: "1",
  encontro: "original", kits: { guerreiro: {}, mago: {} } };
const opcoes = structuredClone(PADRAO);
try { Object.assign(opcoes, JSON.parse(localStorage.getItem("campo-livre-2-opcoes") || "{}")); } catch { /* sem armazenamento */ }
if (url.get("heroi")) opcoes.heroi = url.get("heroi");
if (url.get("qtd")) opcoes.quantidade = url.get("qtd");
opcoes.quantidade = String(escalaDe(opcoes.quantidade));   // "normal" e "maior", guardados pela v2, viram 1 e 2
if (url.get("enc")) opcoes.encontro = url.get("enc");
if (url.get("kit")) {
  // ?kit=sangrenta,grito: as versões pelo nome, para o herói escolhido
  const kit = {};
  for (const v of url.get("kit").split(",")) for (const [slot, vs] of Object.entries(VARIANTES[opcoes.heroi] || {})) if (vs[v]) kit[slot] = v;
  opcoes.kits = { ...opcoes.kits, [opcoes.heroi]: kit };
}
function guardar() { try { localStorage.setItem("campo-livre-2-opcoes", JSON.stringify(opcoes)); } catch { /* idem */ } }

const TECLAS = {
  guerreiro: { direito: "varredura", espaco: "investida", q: "salto" },
  mago: { direito: "bola", espaco: "piscar", q: "muralha" },
};

// ------------------------------------------------------------------------------------------------ estado
const st = {
  tela: "inicio", m: null, E: null, ent: entradaVazia(), robo: null, pausado: false, acumulado: 0,
  pausaAte: 0, refratarioAte: 0, cam: { x: 0, y: 0 }, escala: 2, W: 640, H: 360, mouseTela: { x: 320, y: 180 },
  relogio: 0, ultimo: performance.now(), faixaAte: 0, shift: false, arrasto: null,
  olhar: { x: 0, y: 0 }, retorno: 0, calma: 1, estavaComando: false,
  diag: { quadros: [], sim: [], desenho: [], passos: 0, pausas: 0, pausaMs: 0 },
};

function dimensionar() {
  st.escala = Math.max(1, Math.floor(Math.min(innerWidth / 600, innerHeight / 300)));
  st.W = Math.ceil(innerWidth / st.escala);
  st.H = Math.ceil(innerHeight / st.escala);
  canvas.width = st.W;
  canvas.height = st.H;
  canvas.style.width = st.W * st.escala + "px";
  canvas.style.height = st.H * st.escala + "px";
  g.imageSmoothingEnabled = false;
}
addEventListener("resize", dimensionar);
dimensionar();

function mouseMundo() {
  return { x: st.cam.x + st.mouseTela.x / st.escala, y: st.cam.y + st.mouseTela.y / st.escala };
}

// ------------------------------------------------------------------------------------------------ batalha
function novaBatalha() {
  st.m = criarMundo({ heroi: opcoes.heroi, quantidade: opcoes.quantidade, encontro: opcoes.encontro,
    kit: opcoes.kits[opcoes.heroi] || {} });
  st.E = criarEfeitos(sorteio(77));
  st.ent = entradaVazia();
  st.robo = url.get("robo") ? criarRobo({ nivel: url.get("robo") === "medio" ? "medio" : "forte" }) : null;
  st.acumulado = 0;
  st.pausaAte = st.refratarioAte = 0;
  st.pausado = false;
  st.diag = { quadros: [], sim: [], desenho: [], passos: 0, pausas: 0, pausaMs: 0 };
  const h = st.m.heroi;
  st.olhar = { x: 0, y: 0 }; st.retorno = 0; st.calma = 1;
  st.cam = alvoCamera(true);
  st.cam.x = Math.max(-BORDA, st.cam.x);
  montarKit();
  mostrar("luta");
  ultimaVida = h.vida;
  st.arrasto = null;
  faixa(`${ENCONTROS[opcoes.encontro].nome}. Shift: modo de comando · F1 F2 F4 seleção · 1 2 3 ordens`, 4);
}

/** O modo de comando está ligado: Shift segurado ou o jogo pausado. */
function emComando() { return st.tela === "luta" && (st.shift || st.pausado); }

/** Aplica os eventos do mundo na hora (ordens e seleção funcionam pausados). */
function processarEventos() {
  receber(st.E, st.m.eventos, st.m);
  for (const ev of st.m.eventos) eventoNaTela(ev);
  st.m.eventos.length = 0;
  for (const som of st.E.sons) tocar(som);
  st.E.sons.length = 0;
}

function darOrdem(tipo) {
  const p = mouseMundo();
  const n = ordenar(st.m, tipo, tipo === "defender" ? Math.max(8, Math.min(CAMPO.largura - 8, p.x)) : undefined,
    tipo === "defender" ? Math.max(8, Math.min(CAMPO.altura - 8, p.y)) : undefined);
  processarEventos();
  faixa(`${ORDENS[tipo].nome}: ${st.m.selecao.size ? `${n} selecionados` : `todo o exército (${n})`}.`, 1.8);
  atualizarSelecao();
}

const TIPO_POR_TECLA = { F1: "soldado", F2: "arqueiro", F3: null };
function selecionarTipo(tecla, somar) {
  if (tecla === "F4") { selecionar(st.m, tropasDoTipo(st.m, null), somar); atualizarSelecao(); return; }
  const tipo = TIPO_POR_TECLA[tecla];
  const ids = tipo ? tropasDoTipo(st.m, tipo) : [];
  // F3 fica sem tipo: este exército só tem soldados e arqueiros (não se cria um terceiro só para a tecla)
  if (!tipo || !ids.length) { faixa(`${tecla}: nenhuma tropa ${tipo ? `do tipo ${TIPOS[tipo].nome.toLowerCase()}` : "neste lugar (não há um terceiro tipo)"}.`, 2); return; }
  selecionar(st.m, ids, somar);
  atualizarSelecao();
}

function terminarArrasto(ctrl) {
  const a = st.arrasto;
  st.arrasto = null;
  if (!a || st.tela !== "luta") return;
  const e = st.escala, w = (x) => st.cam.x + x / e, h = (y) => st.cam.y + y / e;
  const x0 = Math.min(a.x0, a.x1), x1 = Math.max(a.x0, a.x1), y0 = Math.min(a.y0, a.y1), y1 = Math.max(a.y0, a.y1);
  const tropas = st.m.lados[0].filter((u) => u !== st.m.heroi);
  let ids;
  if (x1 - x0 < 5 && y1 - y0 < 5) {
    // um clique: a tropa sob o mouse (até 7 px); no vazio, limpa (com Ctrl, não mexe)
    const px = w(a.x1), py = h(a.y1);
    let melhor = null, dm = 7 * 7;
    for (const u of tropas) { const d = (u.x - px) ** 2 + (u.y - 4 - py) ** 2; if (d < dm) { dm = d; melhor = u; } }
    ids = melhor ? [melhor.id] : [];
    if (!melhor && ctrl) return;
  } else {
    ids = tropas.filter((u) => u.x >= w(x0) && u.x <= w(x1) && u.y - 4 >= h(y0) && u.y - 4 <= h(y1)).map((u) => u.id);
  }
  selecionar(st.m, ids, ctrl);
  atualizarSelecao();
}

function mostrar(tela) {
  st.tela = tela;
  $("#tela-inicio").hidden = tela !== "inicio";
  $("#tela-fim").hidden = tela !== "fim";
  $("#tela-pausa").hidden = !(tela === "luta" && st.pausado);
  $("#hud").hidden = tela === "inicio";
  document.body.classList.toggle("menu", tela !== "luta" || st.pausado);
  document.body.classList.toggle("em-luta", tela === "luta");
}

function pausar(sim) {
  if (st.tela !== "luta") return;
  st.pausado = sim ?? !st.pausado;
  st.ent.atacar = false;
  mostrar("luta");
  atualizarModo();
}

// ------------------------------------------------------------------------------------------------ comandos
const teclasMov = { KeyW: "cima", ArrowUp: "cima", KeyS: "baixo", ArrowDown: "baixo", KeyA: "esq", ArrowLeft: "esq", KeyD: "dir", ArrowRight: "dir" };
// F1 abre a ajuda do navegador e F3 a busca: as teclas da seleção não podem chegar até eles
addEventListener("help", (e) => e.preventDefault());
addEventListener("keydown", (e) => {
  iniciarSom();
  if (/^F[1-4]$/.test(e.code)) e.preventDefault();
  if (e.code === "ShiftLeft" || e.code === "ShiftRight") { st.shift = true; st.ent.atacar = false; atualizarModo(); return; }
  if (e.code === "Tab") { e.preventDefault(); alternarPainel(); return; }
  if (e.code === "KeyM") { opcoes.mudo = !opcoes.mudo; ajustarSom(opcoes.volume / 100, opcoes.mudo); guardar(); sincronizarOpcoes(); return; }
  if (st.tela === "inicio") {
    if (e.code === "Enter") novaBatalha();
    if (e.code === "Digit1") escolherHeroi("guerreiro");
    if (e.code === "Digit2") escolherHeroi("mago");
    return;
  }
  if (e.code === "KeyR") { e.preventDefault(); novaBatalha(); return; }
  if (st.tela === "fim") { if (e.code === "Enter") novaBatalha(); return; }
  if (e.code === "KeyP" || e.code === "Escape" || e.code === "Pause") { pausar(); return; }
  if (e.code === "Digit1" || e.code === "Digit2" || e.code === "Digit3") {
    darOrdem({ Digit1: "acompanhar", Digit2: "atacar", Digit3: "defender" }[e.code]);
    return;
  }
  if (/^F[1-4]$/.test(e.code)) { selecionarTipo(e.code, e.ctrlKey); return; }
  if (e.code === "KeyX") { selecionar(st.m, []); atualizarSelecao(); return; }
  if (teclasMov[e.code]) { st.ent[teclasMov[e.code]] = true; e.preventDefault(); return; }
  if (e.repeat) return;
  const t = TECLAS[st.m.nomeHeroi];
  if (e.code === "Space") { e.preventDefault(); if (!st.pausado) apertar(t.espaco); }
  if (e.code === "KeyQ" || e.code === "KeyE") { if (!st.pausado) apertar(t.q); }
});
addEventListener("keyup", (e) => {
  if (teclasMov[e.code]) st.ent[teclasMov[e.code]] = false;
  if (e.code === "ShiftLeft" || e.code === "ShiftRight") { st.shift = false; atualizarModo(); }
});
addEventListener("blur", () => { for (const k of ["cima", "baixo", "esq", "dir", "atacar"]) st.ent[k] = false; st.shift = false; atualizarModo(); });

function apertar(id) {
  st.ent.apertos.push(id);
  st.diag.ultimoAperto = { id, t: performance.now() };
}

addEventListener("mousemove", (e) => {
  st.mouseTela = { x: e.clientX, y: e.clientY };
  if (st.arrasto) { st.arrasto.x1 = e.clientX; st.arrasto.y1 = e.clientY; }
});
canvas.addEventListener("contextmenu", (e) => e.preventDefault());
canvas.addEventListener("mousedown", (e) => {
  iniciarSom();
  st.mouseTela = { x: e.clientX, y: e.clientY };
  if (st.tela !== "luta") return;
  if (emComando()) {
    // no modo de comando o botão esquerdo seleciona (nunca ataca) e o direito manda defender ali
    st.ent.atacar = false;
    if (e.button === 0) st.arrasto = { x0: e.clientX, y0: e.clientY, x1: e.clientX, y1: e.clientY };
    if (e.button === 2) darOrdem("defender");
    return;
  }
  if (e.button === 0) { st.ent.atacar = true; st.diag.ultimoAperto = { id: "basico", t: performance.now() }; }
  if (e.button === 2) apertar(TECLAS[st.m.nomeHeroi].direito);
});
addEventListener("mouseup", (e) => {
  if (e.button !== 0) return;
  st.ent.atacar = false;
  if (st.arrasto) terminarArrasto(e.ctrlKey);
});

// ------------------------------------------------------------------------------------------------ câmera
/** O quanto a câmera olha para o lado do mouse (fora do modo de comando). */
function olharDoMouse() {
  const h = st.m.heroi, mm = st.robo ? { x: st.ent.mx, y: st.ent.my } : mouseMundo();
  return { x: Math.max(-110, Math.min(110, (mm.x - h.x) * 0.35)), y: Math.max(-60, Math.min(60, (mm.y - h.y) * 0.35)) };
}

/** O olhar da câmera neste quadro: segue o mouse no combate; parado no comando; ao sair do comando, volta suave. */
function atualizarOlhar(comando, dt) {
  if (comando) { st.retorno = 0; return; }
  if (st.estavaComando) st.retorno = 0.6;
  const o = olharDoMouse();
  if (st.retorno > 0) {
    st.retorno -= dt;
    const k = 1 - Math.exp(-6 * dt);
    st.olhar.x += (o.x - st.olhar.x) * k;
    st.olhar.y += (o.y - st.olhar.y) * k;
  } else st.olhar = o;
}

function alvoCamera(inicio) {
  const m = st.m, h = m.heroi;
  let fx = h.x, fy = h.y;
  if (m.fase === "formacao" || inicio) {
    // na formação, a câmera mostra os dois exércitos; depois, segue o herói olhando para onde o mouse aponta
    const c = m.centros[1] || h;
    fx = (h.x + c.x) / 2 - 20; fy = (h.y + c.y) / 2;
  } else {
    fx += st.olhar.x;
    fy += st.olhar.y;
  }
  const x = fx - st.W / 2, y = fy - st.H / 2;
  const lim = (v, tam, campo) => (tam >= campo + BORDA * 2 ? (campo - tam) / 2 : Math.max(-BORDA, Math.min(campo + BORDA - tam, v)));
  return { x: lim(x, st.W, CAMPO.largura), y: lim(y, st.H, CAMPO.altura) };
}

function tremor() {
  // no modo de comando o tremor se acalma (st.calma vai a 0); a intensidade escolhida nas opções não muda
  const E = st.E, k = (opcoes.tremor / 100) * st.calma;
  if (!k) return { x: 0, y: 0 };
  const a = E.trauma * E.trauma * IMPACTO.tremorMaxPx * k, t = st.relogio;
  const nx = Math.sin(t * 47.3) * 0.6 + Math.sin(t * 83.1 + 1.3) * 0.4;
  const ny = Math.sin(t * 52.7 + 2.1) * 0.6 + Math.sin(t * 71.9 + 0.7) * 0.4;
  return { x: Math.round(nx * a + E.chute.x * k), y: Math.round(ny * a + E.chute.y * k) };
}

// ------------------------------------------------------------------------------------------------ laço
let ultimaVida = 0;
function quadro(agora) {
  const dtReal = Math.min(0.1, (agora - st.ultimo) / 1000);
  st.ultimo = agora;
  st.relogio += dtReal;
  const D = st.diag;
  D.quadros.push(dtReal * 1000);
  if (D.quadros.length > 600) D.quadros.shift();
  if (st.tela === "luta" || st.tela === "fim") {
    const m = st.m, E = st.E;
    const t0 = performance.now();
    if (st.tela === "luta" && !st.pausado) {
      if (agora < st.pausaAte) { D.pausaMs += dtReal * 1000; }
      else {
        st.acumulado += dtReal;
        let n = 0;
        while (st.acumulado >= PASSO && n < 5) {
          if (st.robo) { const ap = st.ent.apertos; pensar(st.robo, m, st.ent); st.ent.apertos.push(...ap); }
          else { const p = mouseMundo(); st.ent.mx = p.x; st.ent.my = p.y; }
          const apertos = st.ent.apertos.slice();
          passo(m, st.ent);
          if (apertos.length && D.ultimoAperto && m.heroi.acao) D.respostaMs = performance.now() - D.ultimoAperto.t;
          st.ent.apertos = [];
          receber(E, m.eventos, m);
          for (const ev of m.eventos) eventoNaTela(ev);
          m.eventos.length = 0;
          for (const s of E.sons) tocar(s);
          E.sons.length = 0;
          avancar(E, PASSO);
          st.acumulado -= PASSO;
          D.passos++;
          n++;
          if (E.pausaPedida) {
            const p = Math.min(E.pausaPedida, IMPACTO.pausaMax);
            E.pausaPedida = 0;
            if (opcoes.pausa && agora >= st.refratarioAte) {
              st.pausaAte = agora + p;
              st.refratarioAte = st.pausaAte + IMPACTO.pausaRefratario;
              D.pausas++;
              st.acumulado = 0;
              break;
            }
          }
        }
        if (n === 5) st.acumulado = 0;
        if (m.fase === "fim" && st.tela === "luta") setTimeout(() => fim(), 400);
      }
    }
    const t1 = performance.now();
    const comando = emComando() || !!st.arrasto;
    if (!st.pausado) {
      atualizarOlhar(comando, dtReal);
      // durante o arrasto a câmera fica parada: o retângulo na tela é exatamente a região do campo selecionada
      if (!st.arrasto) {
        const alvo = alvoCamera(false), k = 1 - Math.exp(-7 * dtReal);
        st.cam.x += (alvo.x - st.cam.x) * k;
        st.cam.y += (alvo.y - st.cam.y) * k;
      }
    }
    st.estavaComando = comando;
    st.calma += ((comando ? 0 : 1) - st.calma) * (1 - Math.exp(-(comando ? 25 : 8) * dtReal));
    const tr = tremor();
    desenhar(g, { m, E, Q, chao, cam: { x: st.cam.x + tr.x, y: st.cam.y + tr.y }, W: st.W, H: st.H,
      alfa: agora < st.pausaAte || st.pausado ? 1 : Math.min(1, st.acumulado / PASSO), opcoes, mouse: st.robo ? { x: st.ent.mx, y: st.ent.my } : mouseMundo(),
      relogio: st.relogio, pausado: st.pausado, semMira: true });
    if (st.tela === "luta") desenharMira();
    const t2 = performance.now();
    D.sim.push(t1 - t0); D.desenho.push(t2 - t1);
    if (D.sim.length > 600) { D.sim.shift(); D.desenho.shift(); }
    atualizarHud();
  } else {
    // atrás da escolha do herói, o campo parado com os dois exércitos
    if (!st.fundo) st.fundo = { m: criarMundo({ heroi: opcoes.heroi, quantidade: opcoes.quantidade, encontro: opcoes.encontro }), E: criarEfeitos(sorteio(1)) };
    const m = st.fundo.m, c = m.centros[1] || m.heroi;
    desenhar(g, { m, E: st.fundo.E, Q, chao, cam: { x: (m.heroi.x + c.x) / 2 - st.W / 2, y: c.y - st.H / 2 }, W: st.W, H: st.H, alfa: 1,
      opcoes: { ...opcoes, areas: false }, mouse: null, relogio: st.relogio, semMira: true });
  }
  requestAnimationFrame(quadro);
}

// A mira e o retângulo da seleção ficam na tela, fora do tremor (o canvas já está em pixels nativos)
function desenharMira() {
  const e = st.escala, x = Math.round((st.robo ? st.ent.mx - st.cam.x : st.mouseTela.x / e)), y = Math.round(st.robo ? st.ent.my - st.cam.y : st.mouseTela.y / e);
  if (st.arrasto) {
    const a = st.arrasto, x0 = Math.round(Math.min(a.x0, a.x1) / e), y0 = Math.round(Math.min(a.y0, a.y1) / e);
    const w = Math.round(Math.abs(a.x1 - a.x0) / e), h = Math.round(Math.abs(a.y1 - a.y0) / e);
    g.fillStyle = "rgba(190,244,255,0.10)"; g.fillRect(x0, y0, w, h);
    g.fillStyle = "#bff4ff";
    g.fillRect(x0, y0, w, 1); g.fillRect(x0, y0 + h, w + 1, 1); g.fillRect(x0, y0, 1, h); g.fillRect(x0 + w, y0, 1, h);
  }
  if (emComando()) {
    // a mira de comando: quatro cantos claros (não é a cruz do ataque)
    g.fillStyle = "#15121a"; g.fillRect(x - 5, y - 5, 11, 11);
    g.clearRect(x - 3, y - 3, 7, 7);
    g.fillStyle = "#bff4ff";
    for (const [dx, dy] of [[-4, -4], [2, -4], [-4, 2], [2, 2]]) { g.fillRect(x + dx, y + dy, 3, 1); g.fillRect(x + dx + (dx < 0 ? 0 : 2), y + dy, 1, 3); }
    return;
  }
  g.fillStyle = "#15121a";
  g.fillRect(x - 4, y - 1, 9, 3); g.fillRect(x - 1, y - 4, 3, 9);
  g.fillStyle = "#fff6dc";
  g.fillRect(x - 3, y, 2, 1); g.fillRect(x + 2, y, 2, 1); g.fillRect(x, y - 3, 1, 2); g.fillRect(x, y + 2, 1, 2);
}

function eventoNaTela(ev) {
  if (ev.tipo === "avanco") faixa("A primeira leva avança.", 2);
  if (ev.tipo === "reforco") faixa(ev.texto || "A segunda leva chega pela direita, com o campeão.", 3.5);
  if (ev.tipo === "liderCaiu") faixa(`${TIPOS.lider.nome} caiu: ${ev.fogem} fogem; os outros se abalam.`, 3.5);
  if (ev.tipo === "aviso" && ev.lider && ev.arremetida) faixa(`${TIPOS.lider.nome} vai saltar no círculo vermelho: saia dele ou interrompa com um golpe forte.`, 1.6);
  else if (ev.tipo === "aviso" && ev.lider) faixa(`${TIPOS.lider.nome} reúne ${ev.reunidos} para a carga${ev.heroi ? " contra você" : ""}: saia da faixa ou interrompa com um golpe forte.`, 2.2);
  if (ev.tipo === "liderFoco") faixa(`${TIPOS.lider.nome} vem atrás de você.`, 1.8);
  if (ev.tipo === "fuga") faixa("Os inimigos que restam fogem.", 2.5);
  if (ev.tipo === "abalo") faixa("O porta-estandarte caiu: os inimigos em volta recuam.", 2.5);
  if (ev.tipo === "ordem") marcarOrdem();
  if (ev.tipo === "morte" && ev.lado === 0) atualizarSelecao();
}

function faixa(texto, s) {
  const f = $("#faixa");
  f.textContent = texto;
  f.classList.add("ver");
  st.faixaAte = st.relogio + s;
}

function fim() {
  if (st.tela !== "luta") return;
  const r = resumo(st.m), vit = r.resultado === "vitoria";
  $("#fim-titulo").textContent = vit ? "Vitória" : "Derrota";
  const min = Math.floor(r.t / 60), seg = Math.floor(r.t % 60).toString().padStart(2, "0");
  $("#fim-resumo").textContent = `${HEROIS[st.m.nomeHeroi].nome} · ${min}:${seg} · vida ${Math.ceil(r.vida)}/${st.m.heroi.vidaMax}`;
  const k = st.m.heroi.kit, linhas = [["Inimigos derrubados por você", r.abatesHeroi],
    ["Inimigos derrubados pelas tropas", r.abatesAliados], ["Inimigos que fugiram", r.fugiram + r.inimigosVivos],
    ["Aliados perdidos", `${r.perdas} de ${r.aliados}`], ["Maior golpe (derrubados de uma vez)", r.maiorGolpe],
    ["Inimigos ocupados pelas tropas (inimigo × segundo)", Math.round(r.ocupados)],
    ["Dano que as tropas seguraram", Math.round(r.danoTropas)],
    ["Flechas inimigas nas tropas / em você", `${r.flechasTropas} / ${r.flechasHeroi}`]];
  if (r.flechasBarradas) linhas.push(["Flechas barradas pelo escudo", r.flechasBarradas]);
  if (st.m.encontro === "capitao") linhas.push([`Dano de ${TIPOS.lider.nome} em você / nas tropas`, `${Math.round(r.liderHeroi)} / ${Math.round(r.liderTropas)}`]);
  let html = linhas.map(([a, b]) => `<tr><td>${a}</td><td>${b}</td><td></td><td></td></tr>`).join("");
  html += `<tr><th>Habilidade</th><th>Usos</th><th>Atingidos</th><th>Derrubados</th></tr>`;
  for (const id of Object.keys(k)) {
    const u = r.usos[id] || { usos: 0, acertos: 0, abates: 0 };
    html += `<tr><td>${k[id].nome}</td><td>${u.usos}</td><td>${u.acertos}</td><td>${u.abates}</td></tr>`;
  }
  $("#fim-tabela").innerHTML = html;
  mostrar("fim");
}

// ------------------------------------------------------------------------------------------------ HUD
function numero(v) { return String(v).replace(".", ","); }

/** As linhas de cada habilidade, com os números de conteudo.js (a tela não calcula regra nenhuma). */
export function textos(heroi, escolha) {
  const k = kitDoHeroi(heroi, escolha || opcoes.kits[heroi] || {}), rec = HEROIS[heroi].recurso.nome;
  const custo = (h) => [h.custo ? `${h.custo} de ${rec}` : "", h.recarga ? `Recarga ${numero(h.recarga)} s` : ""].filter(Boolean).join(" · ");
  if (heroi === "guerreiro") return [
    { id: "basico", tecla: "Botão esquerdo", nome: k.basico.nome, custo: "Segure para repetir",
      desc: `Causa ${k.basico.dano} de dano num arco curto à frente (${k.basico.raio} px). O ${k.basico.arremate.cada}º corte seguido causa ${k.basico.arremate.dano}, num arco maior, e arremessa quem cai.` },
    k.varredura.sangra ? { id: "varredura", tecla: "Botão direito", nome: k.varredura.nome, custo: custo(k.varredura),
      desc: `Prende os pés por ${numero(k.varredura.preparo)} s e varre ${k.varredura.abertura}° à frente (${k.varredura.raio} px): causa ${k.varredura.dano} de dano e aplica Sangramento (${k.varredura.sangra.tique} a cada 0,5 s por ${k.varredura.sangra.duracao} s). Quase não empurra nem interrompe: os inimigos ficam onde estão.` }
      : { id: "varredura", tecla: "Botão direito", nome: k.varredura.nome, custo: custo(k.varredura),
        desc: `Prende os pés por ${numero(k.varredura.preparo)} s e varre ${k.varredura.abertura}° à frente (${k.varredura.raio} px): causa ${k.varredura.dano} de dano, arremessa quem cai, empurra e atordoa os outros.` },
    k.investida.escudo ? { id: "investida", tecla: "Espaço", nome: k.investida.nome, custo: custo(k.investida),
      desc: `Ergue o escudo por ${numero(k.investida.escudo)} s, virado para o mouse, andando a ${Math.round(k.investida.mover * 100)}% da velocidade: barra as flechas inimigas que cruzam o arco (${k.investida.raio} px, ${k.investida.abertura}°) vindo da frente e empurra quem está nele (${k.investida.dano} de dano na primeira vez). Os aliados a até ${k.investida.protege} px levam ${Math.round((1 - k.investida.reducao) * 100)}% menos dano. Outra habilidade o encerra.` }
    : k.investida.inspira ? { id: "investida", tecla: "Espaço", nome: k.investida.nome, custo: custo(k.investida),
      desc: `Inspira os aliados a até ${k.investida.raio} px por ${k.investida.inspira} s (atacam ${Math.round((1 / k.investida.ritmo - 1) * 100)}% mais rápido e recuperam ${k.investida.cura} de vida por segundo) e abala por ${numero(k.investida.abala)} s os inimigos comuns a até ${k.investida.raioAbala} px.` }
      : { id: "investida", tecla: "Espaço", nome: k.investida.nome, custo: custo(k.investida),
        desc: `Avança ${k.investida.distancia} px na direção do mouse sem receber dano. Joga para os lados quem está no caminho (${k.investida.dano} de dano). O campeão e o Capitão param a investida.` },
    k.salto.puxa ? { id: "salto", tecla: "Q", nome: k.salto.nome, custo: `${k.salto.custo} de Fúria`,
      desc: `Prende os pés por ${numero(k.salto.preparo)} s e puxa para perto de você os inimigos comuns a até ${k.salto.puxa} px (o campeão e o Capitão, não); no fim, causa ${k.salto.dano} de dano num círculo de ${k.salto.raio} px, arremessa quem cai e atordoa os outros. A Fúria sobe ${HEROIS.guerreiro.recurso.porAcerto} por acerto e ${numero(HEROIS.guerreiro.recurso.porAbate)} por inimigo derrubado.` }
    : { id: "salto", tecla: "Q", nome: k.salto.nome, custo: `${k.salto.custo} de Fúria`,
      desc: `Salta até o mouse (até ${k.salto.alcance} px) sem receber dano e cai num círculo de ${k.salto.raio} px: causa ${k.salto.dano} de dano, arremessa e atordoa. A Fúria sobe ${k.salto ? HEROIS.guerreiro.recurso.porAcerto : 0} por acerto e ${numero(HEROIS.guerreiro.recurso.porAbate)} por inimigo derrubado.` },
  ];
  return [
    { id: "basico", tecla: "Botão esquerdo", nome: k.basico.nome, custo: "Segure para repetir",
      desc: `Lança uma faísca na direção do mouse (até ${k.basico.alcance} px): causa ${k.basico.dano} de dano no primeiro inimigo que encontra.` },
    k.bola.alvos ? { id: "bola", tecla: "Botão direito", nome: k.bola.nome, custo: custo(k.bola),
      desc: `Lança um raio na direção do mouse (até ${k.bola.alcance} px): acerta o primeiro inimigo da linha e salta para o inimigo mais perto ainda não atingido (até ${k.bola.salto} px), até ${k.bola.alvos} alvos. Causa ${k.bola.dano} de dano no primeiro e ${k.bola.queda} a menos a cada salto (no mínimo ${k.bola.danoMin}); arremessa quem cai.` }
    : k.bola.chao.repele ? { id: "bola", tecla: "Botão direito", nome: k.bola.nome, custo: custo(k.bola),
      desc: `Explode no ponto do mouse (até ${k.bola.alcance} px): causa ${k.bola.dano} de dano num círculo de ${k.bola.raio} px, sem arremessar, e deixa um chão em chamas de ${k.bola.chao.raio} px por ${k.bola.chao.duracao} s (${k.bola.chao.tique} a cada 0,5 s). Os inimigos contornam o fogo.` }
      : { id: "bola", tecla: "Botão direito", nome: k.bola.nome, custo: custo(k.bola),
        desc: `Explode no ponto do mouse (até ${k.bola.alcance} px) num círculo de ${k.bola.raio} px: causa ${k.bola.dano} de dano e arremessa quem cai. O chão queima por ${k.bola.chao.duracao} s (${k.bola.chao.tique} a cada 0,5 s).` },
    { id: "piscar", tecla: "Espaço", nome: k.piscar.nome, custo: custo(k.piscar),
      desc: `Reaparece até ${k.piscar.distancia} px na direção do mouse. Onde estava, uma onda de ${k.piscar.raio} px causa ${k.piscar.dano} de dano, empurra e atordoa.` },
    k.muralha.variante === "gelo" ? { id: "muralha", tecla: "Q", nome: k.muralha.nome, custo: custo(k.muralha),
      desc: `Cobre de gelo um círculo de ${k.muralha.raio} px no ponto do mouse (até ${k.muralha.alcance} px) por ${k.muralha.duracao} s. Ao surgir, causa ${k.muralha.dano} de dano e atordoa por ${numero(k.muralha.atordoa)} s. Dentro dele, os inimigos andam a ${Math.round(k.muralha.lento * 100)}% da velocidade e atacam com ${Math.round(k.muralha.ritmo * 100)}% da frequência (o campeão e o Capitão, ${Math.round(k.muralha.lentoElite * 100)}% e ${Math.round(k.muralha.ritmoElite * 100)}%).` }
    : k.muralha.variante === "anel" ? { id: "muralha", tecla: "Q", nome: k.muralha.nome, custo: custo(k.muralha),
      desc: `Ergue um anel de fogo de ${k.muralha.raio} px de raio no ponto do mouse (até ${k.muralha.alcance} px) por ${k.muralha.duracao} s. Ninguém atravessa a linha: quem está dentro fica dentro. A linha causa ${k.muralha.tique} a cada 0,5 s.` }
      : { id: "muralha", tecla: "Q", nome: k.muralha.nome, custo: custo(k.muralha),
        desc: `Ergue uma parede de fogo de ${k.muralha.comprimento} px no ponto do mouse (até ${k.muralha.alcance} px), de lado para você, por ${k.muralha.duracao} s. Desvia os inimigos e causa ${k.muralha.tique} a cada 0,5 s a quem entra.` },
  ];
}

let slots = [];
function montarKit() {
  const heroi = st.m.nomeHeroi, kit = $("#kit");
  kit.innerHTML = "";
  slots = textos(heroi).map((t) => {
    const d = document.createElement("div");
    d.className = "slot";
    d.innerHTML = `<span class="tecla">${t.tecla}</span><span class="nome">${t.nome}</span><span class="custo">${t.custo}</span><span class="espera"></span><span class="segundos"></span>`;
    kit.append(d);
    return { id: t.id, el: d, espera: d.querySelector(".espera"), seg: d.querySelector(".segundos"), custo: d.querySelector(".custo"), pronto: true };
  });
  $("#h-nome").textContent = HEROIS[heroi].nome;
  $("#ficha .recurso").classList.toggle("mana", heroi === "mago");
  $("#ficha .recurso").title = HEROIS[heroi].recurso.nome;
  atualizarSelecao();
  atualizarModo();
}

// As ordens com quantos cumprem cada uma (as tropas podem estar divididas)
function marcarOrdem() {
  const n = { acompanhar: 0, atacar: 0, defender: 0 };
  for (const u of st.m.lados[0]) if (u !== st.m.heroi) n[(u.ordem || st.m.ordem).tipo]++;
  $("#p-ordens").innerHTML = Object.entries(ORDENS).map(([id, d]) =>
    `<span class="${n[id] ? "atual" : ""}"><kbd>${d.tecla}</kbd>${d.nome}<small>${n[id]}</small></span>`).join("");
}

function atualizarModo() {
  const el = $("#modo"), c = emComando();
  el.classList.toggle("comando", c);
  el.textContent = c ? (st.pausado ? "Comando (pausado): arraste para selecionar" : "Comando: arraste para selecionar · botão direito, Defender ali")
    : "Combate · segure Shift para comandar";
}

function atualizarSelecao() {
  if (!st.m) return;
  const m = st.m, tropas = m.lados[0].filter((u) => u !== m.heroi), sel = m.selecao;
  const conta = (tipo) => tropas.filter((u) => u.tipo === tipo).length, contaSel = (tipo) => tropas.filter((u) => u.tipo === tipo && sel.has(u.id)).length;
  const tipos = [["F1", "soldado", "Soldados"], ["F2", "arqueiro", "Arqueiros"]];
  $("#p-tipos").innerHTML = tipos.map(([k, t, nome]) => `<span class="${contaSel(t) ? "sel" : ""}"><kbd>${k}</kbd>${nome} ${conta(t)}</span>`).join("") +
    `<span class="vazio" title="Não há um terceiro tipo de tropa"><kbd>F3</kbd>—</span><span><kbd>F4</kbd>Todos</span>`;
  $("#p-selecao").innerHTML = sel.size
    ? `Seleção: <b>${sel.size}</b> (${tipos.filter(([, t]) => contaSel(t)).map(([, t, nome]) => `${nome.toLowerCase()} ${contaSel(t)}`).join(", ")}) · <kbd>X</kbd> limpa`
    : "Sem seleção: as ordens valem para todos";
  marcarOrdem();
}

let ultimoHud = "";
function atualizarHud() {
  const m = st.m, h = m.heroi;
  const vida = Math.max(0, h.vida), rec = h.recurso;
  const chave = [Math.ceil(vida), Math.floor(rec), m.lados[0].length, m.lados[1].length, m.lider && Math.ceil(m.lider.vida),
    m.lider && (m.lider.acao ? m.lider.acao.tipo + m.lider.acao.fase : m.lider.ofegante > 0), m.lider && m.lider.focoHeroi, m.reforco.chegou,
    ...slots.map((s) => Math.ceil((h.cds[s.id] || 0) * 10))].join(",");
  if (st.faixaAte && st.relogio > st.faixaAte) { $("#faixa").classList.remove("ver"); st.faixaAte = 0; }
  if (vida < ultimaVida - 4) { const b = $("#ficha .vida"); b.classList.remove("apanhou"); void b.offsetWidth; b.classList.add("apanhou"); }
  ultimaVida = vida;
  if (chave === ultimoHud) return;
  ultimoHud = chave;
  $("#ficha .vida i").style.width = (100 * vida) / h.vidaMax + "%";
  $("#ficha .vida span").textContent = `${Math.ceil(vida)}/${h.vidaMax}`;
  $("#ficha .recurso i").style.width = (100 * rec) / h.recursoMax + "%";
  $("#ficha .recurso span").textContent = `${HEROIS[h.nomeHeroi].recurso.nome} ${Math.floor(rec)}/${h.recursoMax}`;
  $("#p-aliados").textContent = m.lados[0].length - (h.morto ? 0 : 1);
  $("#p-inimigos").textContent = m.lados[1].length + resumo(m).inimigosPorVir;
  marcarOrdem();
  const l = m.lider || (m.encontro === "capitao" ? { morto: true, def: TIPOS.lider, vida: 0, vidaMax: TIPOS.lider.vida } : null);
  $("#chefe").hidden = !l;
  if (l) {
    $("#chefe b").textContent = l.def.nome;
    $("#chefe .barra i").style.width = (100 * Math.max(0, l.vida)) / l.vidaMax + "%";
    $("#chefe .barra span").textContent = l.morto ? "caiu" : `${Math.ceil(l.vida)}/${l.vidaMax}`;
    const a = l.acao, firmes = () => m.lados[1].filter((u) => u.firme).length;
    $("#chefe small").textContent = l.morto ? "A tropa perto dele fugiu; ninguém mais segura o resto." : a && a.tipo === "reunir" ? `Reúne ${a.reunidos.length} para a carga!`
      : a && a.tipo === "carga" ? "Carga!" : a && a.tipo === "arremetida" ? (a.fase === "voo" ? "Salta!" : "Vai saltar no círculo!")
      : l.ofegante > 0 ? (l.cravado > 0 ? "Machado cravado: leva +50% de dano" : "Ofegante: leva +50% de dano")
      : l.focoHeroi ? `Atrás de você · presença: ${firmes()} firmes` : `Com as tropas · presença: ${firmes()} firmes`;
  }
  for (const s of slots) {
    const k = h.kit[s.id], cd = h.cds[s.id] || 0, falta = k.custo && rec < k.custo;
    const frac = k.recarga ? cd / k.recarga : 0;
    s.espera.style.height = (frac * 100).toFixed(1) + "%";
    s.seg.textContent = cd > 0 ? Math.ceil(cd) : "";
    s.custo.classList.toggle("falta", !!falta);
    const pronto = cd <= 0 && !falta;
    s.el.classList.toggle("pronto", pronto && s.id !== "basico");
    if (pronto && !s.pronto && s.id !== "basico") { s.el.classList.remove("acendeu"); void s.el.offsetWidth; s.el.classList.add("acendeu"); }
    s.pronto = pronto;
  }
}

function alternarPainel() {
  const p = $("#painel");
  p.hidden = !p.hidden;
  if (!p.hidden) atualizarPainel();
}
setInterval(() => { if (!$("#painel").hidden) atualizarPainel(); }, 500);
$("#abrir-painel").addEventListener("click", alternarPainel);

function atualizarPainel() {
  if (!st.m) return;
  const tempo = (t) => `${Math.floor(t / 60)}:${Math.floor(t % 60).toString().padStart(2, "0")}`;
  $("#registro").innerHTML = st.m.registro.slice(-30).reverse().map((r) => `<li><time>${tempo(r.t)}</time>${r.texto}</li>`).join("");
  $("#diag").textContent = textoDiag();
}

function estatistica(v) {
  if (!v.length) return { media: 0, p95: 0, max: 0 };
  const o = [...v].sort((a, b) => a - b);
  return { media: v.reduce((a, b) => a + b, 0) / v.length, p95: o[Math.floor(o.length * 0.95)], max: o[o.length - 1] };
}
export function diagnostico() {
  const q = estatistica(st.diag.quadros), s = estatistica(st.diag.sim), d = estatistica(st.diag.desenho);
  return { fps: q.media ? 1000 / q.media : 0, quadroMedio: q.media, quadroP95: q.p95, quadroMax: q.max, simMedio: s.media,
    simP95: s.p95, desenhoMedio: d.media, desenhoP95: d.p95, unidades: st.m ? st.m.unidades.length : 0,
    particulas: st.E ? st.E.particulas.length : 0, voadores: st.E ? st.E.voadores.length : 0, pausas: st.diag.pausas,
    pausaMs: st.diag.pausaMs, respostaMs: st.diag.respostaMs, escala: st.escala, W: st.W, H: st.H };
}
function textoDiag() {
  const d = diagnostico(), f = (v) => v.toFixed(1);
  return `quadro ${f(d.quadroMedio)} ms (p95 ${f(d.quadroP95)}, máx ${f(d.quadroMax)}) · ${f(d.fps)} qps
simulação ${f(d.simMedio)} ms (p95 ${f(d.simP95)}) · desenho ${f(d.desenhoMedio)} ms (p95 ${f(d.desenhoP95)})
unidades ${d.unidades} · partículas ${d.particulas} · corpos no ar ${d.voadores}
pausas de impacto ${d.pausas} (${Math.round(d.pausaMs)} ms no total)
campo ${d.W}×${d.H} px nativos, ampliado ${d.escala}×`;
}

// ------------------------------------------------------------------------------------------------ telas
function escolherHeroi(id) {
  opcoes.heroi = id;
  guardar();
  st.fundo = null;
  $$(".heroi").forEach((b) => b.classList.toggle("escolhido", b.dataset.heroi === id));
}

function escolherEncontro(id) {
  opcoes.encontro = id;
  guardar();
  st.fundo = null;
  $$(".encontro").forEach((b) => b.classList.toggle("escolhido", b.dataset.enc === id));
  const e = ENCONTROS[id];
  $("#enc-info").innerHTML = `<b>${e.nome}.</b> ${e.descricao} ${e.regra}`;
  contagem();
}

// As quantidades reais da escala escolhida, contadas no mundo que a batalha vai usar (nada de conta à parte)
function contagem() {
  const el = $("#contagem");
  if (!el) return;
  const m = criarMundo({ heroi: opcoes.heroi, quantidade: opcoes.quantidade, encontro: opcoes.encontro });
  const agora = m.lados[1].length, depois = m.stats.inimigos - agora;
  el.textContent = `Aliados ${m.stats.aliados} · Inimigos ${m.stats.inimigos}${depois ? `: ${agora} no começo e ${depois} depois` : ""}.` +
    (m.escala > 1 ? " Capitão, campeão e porta-estandarte continuam um só." : "");
}

function escolherVersao(heroi, slot, v) {
  opcoes.kits = { ...opcoes.kits, [heroi]: { ...(opcoes.kits[heroi] || {}), [slot]: v } };
  guardar();
  montarHerois();
}

function montarHerois() {
  const raiz = $("#herois");
  raiz.innerHTML = "";
  for (const id of ["guerreiro", "mago"]) {
    const d = HEROIS[id], b = document.createElement("div");
    b.className = "heroi" + (opcoes.heroi === id ? " escolhido" : "");
    b.dataset.heroi = id;
    b.tabIndex = 0;
    const sp = Q[id][0].parado.d, c = document.createElement("canvas");
    c.width = sp.width; c.height = sp.height;
    c.getContext("2d").drawImage(sp, 0, 0);
    const escolha = opcoes.kits[id] || {};
    b.innerHTML = `<h3></h3><div class="info">Vida ${d.vida} · ${d.recurso.nome} ${d.recurso.max}${d.recurso.regen ? ` (recupera ${d.recurso.regen} por segundo)` : " (começa em 0)"} · crítico ${Math.round(d.critico.chance * 100)}% (×${numero(d.critico.mult)}) · tecla ${id === "guerreiro" ? 1 : 2}</div>` +
      textos(id, escolha).map((t) => {
        const vs = VARIANTES[id][t.id];
        const versoes = vs ? `<span class="versoes">${[["original", d.kit[t.id].nome], ...Object.entries(vs).map(([v, def]) => [v, def.nome])]
          .map(([v, nome]) => `<button type="button" data-v="${v}" data-slot="${t.id}" class="${(escolha[t.id] || "original") === v ? "atual" : ""}">${nome}</button>`).join("")}</span>` : "";
        return `<div class="hab"><div class="cab"><b>${t.tecla} · ${vs ? "" : t.nome}${versoes}</b><span>${t.custo}</span></div><p>${t.desc}</p></div>`;
      }).join("");
    b.querySelector("h3").append(c, d.nome);
    b.addEventListener("click", (e) => {
      const v = e.target.closest("button[data-v]");
      if (v) { opcoes.heroi = id; escolherVersao(id, v.dataset.slot, v.dataset.v); return; }
      escolherHeroi(id);
    });
    b.addEventListener("keydown", (e) => { if (e.key === "Enter" && !e.target.closest("button")) { escolherHeroi(id); novaBatalha(); } });
    raiz.append(b);
  }
}

function montarInicio() {
  $("#versao-inicio").textContent = "· protótipo";
  $("#selo").textContent = `${VERSAO} · protótipo da etapa 8, nada no jogo`;
  document.title = `${VERSAO} · protótipo da etapa 8`;
  document.querySelector(".caixa h1").firstChild.textContent = VERSAO + " ";
  for (const [id, e] of Object.entries(ENCONTROS)) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "encontro";
    b.dataset.enc = id;
    b.innerHTML = `<b>${e.nome}</b>${e.original ? "a batalha do Campo Livre 1" : id === "capitao" ? "o líder e a retaguarda" : id === "duasFrentes" ? "pressão dos dois lados" : "grupos longe uns dos outros"}`;
    b.addEventListener("click", () => escolherEncontro(id));
    $("#encontros").append(b);
  }
  escolherEncontro(ENCONTROS[opcoes.encontro] ? opcoes.encontro : "original");
  montarHerois();
  escolherHeroi(opcoes.heroi);
  $("#op-quantidade").value = opcoes.quantidade;
  $("#op-quantidade").addEventListener("change", (e) => { opcoes.quantidade = e.target.value; guardar(); st.fundo = null; contagem(); });
  contagem();
  $("#lutar").addEventListener("click", () => { iniciarSom(); novaBatalha(); });
  $("#continuar").addEventListener("click", () => pausar(false));
  $$("[data-recomecar]").forEach((b) => b.addEventListener("click", () => novaBatalha()));
  $$("[data-trocar]").forEach((b) => b.addEventListener("click", () => { st.pausado = false; mostrar("inicio"); }));
  for (const raizOp of $$("[data-opcoes]")) {
    raizOp.innerHTML = `
      <label>Tremor da câmera <input type="range" min="0" max="150" step="25" data-op="tremor"> <span data-ver="tremor"></span></label>
      <label><input type="checkbox" data-op="pausa"> Pausa no impacto</label>
      <label><input type="checkbox" data-op="areas"> Mostrar a área do botão direito</label>
      <label>Som <input type="range" min="0" max="100" step="10" data-op="volume"> <span data-ver="volume"></span></label>
      <label><input type="checkbox" data-op="mudo"> Mudo (M)</label>`;
  }
  for (const el of $$("[data-op]")) {
    el.addEventListener("input", () => {
      const k = el.dataset.op;
      opcoes[k] = el.type === "checkbox" ? el.checked : Number(el.value);
      ajustarSom(opcoes.volume / 100, opcoes.mudo);
      guardar();
      sincronizarOpcoes();
    });
  }
  sincronizarOpcoes();
}

function sincronizarOpcoes() {
  for (const el of $$("[data-op]")) {
    const v = opcoes[el.dataset.op];
    if (el.type === "checkbox") el.checked = !!v; else el.value = v;
  }
  for (const el of $$("[data-ver]")) {
    const v = opcoes[el.dataset.ver];
    el.textContent = el.dataset.ver === "tremor" ? (v ? v + "%" : "Desligado") : v ? v + "%" : "0%";
  }
  ajustarSom(opcoes.volume / 100, opcoes.mudo);
}

try { if (typeof Sprites !== "undefined") Sprites.publicar(); } catch { /* sem a paleta do jogo: as cores de reserva do CSS */ }
montarInicio();
mostrar("inicio");
requestAnimationFrame(quadro);
if (url.get("auto")) novaBatalha();

// para os testes, a medição e os vídeos (Playwright)
window.__campo = {
  st, opcoes, diagnostico, novaBatalha, pausar, textos, emComando,
  mundo: () => st.m, efeitos: () => st.E, mouseMundo,
  configurar: (o) => { Object.assign(opcoes, o); sincronizarOpcoes(); },
};
export { CONTINGENTES };
