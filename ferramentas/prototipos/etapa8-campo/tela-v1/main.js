// CONGELADA: a primeira versão jogável (Campo Livre 1, commit b1d95e1c), aprovada pelo Jean; servida em /v1/ só para comparar.
// PROTÓTIPO de campo livre da etapa 8 (nada no jogo): o laço, os comandos, a câmera, a pausa de impacto, a HUD e as
// telas. A batalha avança em passos fixos de 1/60 s (sim.js); o desenho interpola entre dois passos. A pausa de
// impacto para a simulação e os efeitos por alguns milissegundos; os comandos apertados nesse meio-tempo esperam e
// saem no passo seguinte. Parâmetros de URL (para testes, medição e vídeos): ?heroi=mago&qtd=maior&auto=1&robo=1.
import { VERSAO, HEROIS, ORDENS, IMPACTO, CAMPO, CONTINGENTES } from "./conteudo.js";
import { criarMundo, passo, entradaVazia, ordenar, resumo, sorteio, PASSO } from "./sim.js";
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
const PADRAO = { tremor: 100, pausa: true, volume: 50, mudo: false, areas: true, heroi: "guerreiro", quantidade: "normal" };
const opcoes = { ...PADRAO };
try { Object.assign(opcoes, JSON.parse(localStorage.getItem("campo-livre-opcoes") || "{}")); } catch { /* sem armazenamento */ }
if (url.get("heroi")) opcoes.heroi = url.get("heroi");
if (url.get("qtd")) opcoes.quantidade = url.get("qtd");
function guardar() { try { localStorage.setItem("campo-livre-opcoes", JSON.stringify(opcoes)); } catch { /* idem */ } }

const TECLAS = {
  guerreiro: { direito: "varredura", espaco: "investida", q: "salto" },
  mago: { direito: "bola", espaco: "piscar", q: "muralha" },
};

// ------------------------------------------------------------------------------------------------ estado
const st = {
  tela: "inicio", m: null, E: null, ent: entradaVazia(), robo: null, pausado: false, acumulado: 0,
  pausaAte: 0, refratarioAte: 0, cam: { x: 0, y: 0 }, escala: 2, W: 640, H: 360, mouseTela: { x: 320, y: 180 },
  relogio: 0, ultimo: performance.now(), faixaAte: 0,
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
  st.m = criarMundo({ heroi: opcoes.heroi, quantidade: opcoes.quantidade });
  st.E = criarEfeitos(sorteio(77));
  st.ent = entradaVazia();
  st.robo = url.get("robo") ? criarRobo({ nivel: url.get("robo") === "medio" ? "medio" : "forte" }) : null;
  st.acumulado = 0;
  st.pausaAte = st.refratarioAte = 0;
  st.pausado = false;
  st.diag = { quadros: [], sim: [], desenho: [], passos: 0, pausas: 0, pausaMs: 0 };
  const h = st.m.heroi;
  st.cam = alvoCamera(true);
  st.cam.x = Math.max(-BORDA, st.cam.x);
  montarKit();
  mostrar("luta");
  ultimaVida = h.vida;
  faixa("A primeira leva espera em formação. 1 Acompanhar · 2 Atacar · 3 Defender", 3.5);
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
}

// ------------------------------------------------------------------------------------------------ comandos
const teclasMov = { KeyW: "cima", ArrowUp: "cima", KeyS: "baixo", ArrowDown: "baixo", KeyA: "esq", ArrowLeft: "esq", KeyD: "dir", ArrowRight: "dir" };
addEventListener("keydown", (e) => {
  iniciarSom();
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
    const tipo = { Digit1: "acompanhar", Digit2: "atacar", Digit3: "defender" }[e.code];
    const p = mouseMundo();
    ordenar(st.m, tipo, tipo === "defender" ? Math.max(8, Math.min(CAMPO.largura - 8, p.x)) : undefined,
      tipo === "defender" ? Math.max(8, Math.min(CAMPO.altura - 8, p.y)) : undefined);
    // a ordem vale na hora, também pausado: a bandeira e a HUD não esperam o próximo passo
    receber(st.E, st.m.eventos, st.m);
    for (const ev of st.m.eventos) eventoNaTela(ev);
    st.m.eventos.length = 0;
    for (const som of st.E.sons) tocar(som);
    st.E.sons.length = 0;
    return;
  }
  if (teclasMov[e.code]) { st.ent[teclasMov[e.code]] = true; e.preventDefault(); return; }
  if (e.repeat) return;
  const t = TECLAS[st.m.nomeHeroi];
  if (e.code === "Space") { e.preventDefault(); if (!st.pausado) apertar(t.espaco); }
  if (e.code === "KeyQ" || e.code === "KeyE") { if (!st.pausado) apertar(t.q); }
});
addEventListener("keyup", (e) => { if (teclasMov[e.code]) st.ent[teclasMov[e.code]] = false; });
addEventListener("blur", () => { for (const k of ["cima", "baixo", "esq", "dir", "atacar"]) st.ent[k] = false; });

function apertar(id) {
  st.ent.apertos.push(id);
  st.diag.ultimoAperto = { id, t: performance.now() };
}

canvas.addEventListener("mousemove", (e) => { st.mouseTela = { x: e.clientX, y: e.clientY }; });
canvas.addEventListener("contextmenu", (e) => e.preventDefault());
canvas.addEventListener("mousedown", (e) => {
  iniciarSom();
  st.mouseTela = { x: e.clientX, y: e.clientY };
  if (st.tela !== "luta" || st.pausado) return;
  if (e.button === 0) { st.ent.atacar = true; st.diag.ultimoAperto = { id: "basico", t: performance.now() }; }
  if (e.button === 2) apertar(TECLAS[st.m.nomeHeroi].direito);
});
addEventListener("mouseup", (e) => { if (e.button === 0) st.ent.atacar = false; });

// ------------------------------------------------------------------------------------------------ câmera
function alvoCamera(inicio) {
  const m = st.m, h = m.heroi, mm = st.robo ? { x: st.ent.mx, y: st.ent.my } : mouseMundo();
  let fx = h.x, fy = h.y;
  if (m.fase === "formacao" || inicio) {
    // na formação, a câmera mostra os dois exércitos; depois, segue o herói olhando para onde o mouse aponta
    const c = m.centros[1] || h;
    fx = (h.x + c.x) / 2 - 20; fy = (h.y + c.y) / 2;
  } else {
    fx += Math.max(-110, Math.min(110, (mm.x - h.x) * 0.35));
    fy += Math.max(-60, Math.min(60, (mm.y - h.y) * 0.35));
  }
  const x = fx - st.W / 2, y = fy - st.H / 2;
  const lim = (v, tam, campo) => (tam >= campo + BORDA * 2 ? (campo - tam) / 2 : Math.max(-BORDA, Math.min(campo + BORDA - tam, v)));
  return { x: lim(x, st.W, CAMPO.largura), y: lim(y, st.H, CAMPO.altura) };
}

function tremor() {
  const E = st.E, k = opcoes.tremor / 100;
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
    if (!st.pausado) {
      const alvo = alvoCamera(false), k = 1 - Math.exp(-7 * dtReal);
      st.cam.x += (alvo.x - st.cam.x) * k;
      st.cam.y += (alvo.y - st.cam.y) * k;
    }
    const tr = tremor();
    desenhar(g, { m, E, Q, chao, cam: { x: st.cam.x + tr.x, y: st.cam.y + tr.y }, W: st.W, H: st.H,
      alfa: agora < st.pausaAte || st.pausado ? 1 : Math.min(1, st.acumulado / PASSO), opcoes, mouse: st.robo ? { x: st.ent.mx, y: st.ent.my } : mouseMundo(),
      relogio: st.relogio, pausado: st.pausado, semMira: st.tela !== "luta" });
    const t2 = performance.now();
    D.sim.push(t1 - t0); D.desenho.push(t2 - t1);
    if (D.sim.length > 600) { D.sim.shift(); D.desenho.shift(); }
    atualizarHud();
  } else {
    // atrás da escolha do herói, o campo parado com os dois exércitos
    if (!st.fundo) st.fundo = { m: criarMundo({ heroi: opcoes.heroi, quantidade: opcoes.quantidade }), E: criarEfeitos(sorteio(1)) };
    const m = st.fundo.m, c = m.centros[1];
    desenhar(g, { m, E: st.fundo.E, Q, chao, cam: { x: (m.heroi.x + c.x) / 2 - st.W / 2, y: c.y - st.H / 2 }, W: st.W, H: st.H, alfa: 1,
      opcoes: { ...opcoes, areas: false }, mouse: null, relogio: st.relogio, semMira: true });
  }
  requestAnimationFrame(quadro);
}

function eventoNaTela(ev) {
  if (ev.tipo === "avanco") faixa("A primeira leva avança.", 2);
  if (ev.tipo === "reforco") faixa("A segunda leva chega pela direita, com o campeão.", 3.5);
  if (ev.tipo === "fuga") faixa("Os inimigos que restam fogem.", 2.5);
  if (ev.tipo === "abalo") faixa("O porta-estandarte caiu: os inimigos em volta recuam.", 2.5);
  if (ev.tipo === "ordem") marcarOrdem();
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
    ["Aliados perdidos", `${r.perdas} de ${r.aliados}`], ["Maior golpe (derrubados de uma vez)", r.maiorGolpe]];
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
export function textos(heroi) {
  const k = HEROIS[heroi].kit, rec = HEROIS[heroi].recurso.nome;
  const custo = (h) => [h.custo ? `${h.custo} de ${rec}` : "", h.recarga ? `Recarga ${numero(h.recarga)} s` : ""].filter(Boolean).join(" · ");
  if (heroi === "guerreiro") return [
    { id: "basico", tecla: "Botão esquerdo", nome: k.basico.nome, custo: "Segure para repetir",
      desc: `Causa ${k.basico.dano} de dano num arco curto à frente (${k.basico.raio} px). O ${k.basico.arremate.cada}º corte seguido causa ${k.basico.arremate.dano}, num arco maior, e arremessa quem cai.` },
    { id: "varredura", tecla: "Botão direito", nome: k.varredura.nome, custo: custo(k.varredura),
      desc: `Prende os pés por ${numero(k.varredura.preparo)} s e varre ${k.varredura.abertura}° à frente (${k.varredura.raio} px): causa ${k.varredura.dano} de dano, arremessa quem cai, empurra e atordoa os outros.` },
    { id: "investida", tecla: "Espaço", nome: k.investida.nome, custo: custo(k.investida),
      desc: `Avança ${k.investida.distancia} px na direção do mouse sem receber dano. Joga para os lados quem está no caminho (${k.investida.dano} de dano). O campeão para a investida.` },
    { id: "salto", tecla: "Q", nome: k.salto.nome, custo: `${k.salto.custo} de Fúria`,
      desc: `Salta até o mouse (até ${k.salto.alcance} px) sem receber dano e cai num círculo de ${k.salto.raio} px: causa ${k.salto.dano} de dano, arremessa e atordoa. A Fúria sobe ${k.salto ? HEROIS.guerreiro.recurso.porAcerto : 0} por acerto e ${numero(HEROIS.guerreiro.recurso.porAbate)} por inimigo derrubado.` },
  ];
  return [
    { id: "basico", tecla: "Botão esquerdo", nome: k.basico.nome, custo: "Segure para repetir",
      desc: `Lança uma faísca na direção do mouse (até ${k.basico.alcance} px): causa ${k.basico.dano} de dano no primeiro inimigo que encontra.` },
    { id: "bola", tecla: "Botão direito", nome: k.bola.nome, custo: custo(k.bola),
      desc: `Explode no ponto do mouse (até ${k.bola.alcance} px) num círculo de ${k.bola.raio} px: causa ${k.bola.dano} de dano e arremessa quem cai. O chão queima por ${k.bola.chao.duracao} s (${k.bola.chao.dps} de dano por segundo).` },
    { id: "piscar", tecla: "Espaço", nome: k.piscar.nome, custo: custo(k.piscar),
      desc: `Reaparece até ${k.piscar.distancia} px na direção do mouse. Onde estava, uma onda de ${k.piscar.raio} px causa ${k.piscar.dano} de dano, empurra e atordoa.` },
    { id: "muralha", tecla: "Q", nome: k.muralha.nome, custo: custo(k.muralha),
      desc: `Ergue uma parede de fogo de ${k.muralha.comprimento} px no ponto do mouse (até ${k.muralha.alcance} px), de lado para você, por ${k.muralha.duracao} s. Desvia os inimigos e causa ${k.muralha.dps} de dano por segundo a quem entra.` },
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
  marcarOrdem();
}

function marcarOrdem() {
  const o = st.m.ordem.tipo;
  $("#p-ordens").innerHTML = Object.entries(ORDENS).map(([id, d]) =>
    `<span class="${id === o ? "atual" : ""}"><kbd>${d.tecla}</kbd>${d.nome}</span>`).join("");
}

let ultimoHud = "";
function atualizarHud() {
  const m = st.m, h = m.heroi;
  const vida = Math.max(0, h.vida), rec = h.recurso;
  const chave = [Math.ceil(vida), Math.floor(rec), m.lados[0].length, m.lados[1].length,
    ...slots.map((s) => Math.ceil((h.cds[s.id] || 0) * 10))].join(",");
  if (st.faixaAte && st.relogio > st.faixaAte) { $("#faixa").classList.remove("ver"); st.faixaAte = 0; }
  if (vida < ultimaVida - 4) { const b = $("#ficha .vida"); b.classList.remove("dor"); void b.offsetWidth; b.classList.add("dor"); }
  ultimaVida = vida;
  if (chave === ultimoHud) return;
  ultimoHud = chave;
  $("#ficha .vida i").style.width = (100 * vida) / h.vidaMax + "%";
  $("#ficha .vida span").textContent = `${Math.ceil(vida)}/${h.vidaMax}`;
  $("#ficha .recurso i").style.width = (100 * rec) / h.recursoMax + "%";
  $("#ficha .recurso span").textContent = `${HEROIS[h.nomeHeroi].recurso.nome} ${Math.floor(rec)}/${h.recursoMax}`;
  $("#p-aliados").textContent = m.lados[0].length - (h.morto ? 0 : 1);
  $("#p-inimigos").textContent = m.lados[1].length + (m.reforco.chegou ? 0 : Object.values(m.reforco.comp).reduce((a, b) => a + b, 0));
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

function montarInicio() {
  $("#versao-inicio").textContent = "· protótipo";
  $("#selo").textContent = `${VERSAO} · protótipo da etapa 8, nada no jogo`;
  document.title = `${VERSAO} · protótipo da etapa 8`;
  document.querySelector(".caixa h1").firstChild.textContent = VERSAO + " ";
  const raiz = $("#herois");
  for (const id of ["guerreiro", "mago"]) {
    const d = HEROIS[id], b = document.createElement("div");
    b.className = "heroi";
    b.dataset.heroi = id;
    b.tabIndex = 0;
    const sp = Q[id][0].parado.d, c = document.createElement("canvas");
    c.width = sp.width; c.height = sp.height;
    c.getContext("2d").drawImage(sp, 0, 0);
    b.innerHTML = `<h3></h3><div class="info">Vida ${d.vida} · ${d.recurso.nome} ${d.recurso.max}${d.recurso.regen ? ` (recupera ${d.recurso.regen} por segundo)` : " (começa em 0)"} · tecla ${id === "guerreiro" ? 1 : 2}</div>` +
      textos(id).map((t) => `<div class="hab"><div class="cab"><b>${t.tecla} · ${t.nome}</b><span>${t.custo}</span></div><p>${t.desc}</p></div>`).join("");
    b.querySelector("h3").append(c, d.nome);
    b.addEventListener("click", () => escolherHeroi(id));
    b.addEventListener("keydown", (e) => { if (e.key === "Enter") { escolherHeroi(id); novaBatalha(); } });
    raiz.append(b);
  }
  escolherHeroi(opcoes.heroi);
  $("#op-quantidade").value = opcoes.quantidade;
  $("#op-quantidade").addEventListener("change", (e) => { opcoes.quantidade = e.target.value; guardar(); st.fundo = null; });
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
  st, opcoes, diagnostico, novaBatalha, pausar, textos,
  mundo: () => st.m, efeitos: () => st.E,
  configurar: (o) => { Object.assign(opcoes, o); sincronizarOpcoes(); },
};
export { CONTINGENTES };
