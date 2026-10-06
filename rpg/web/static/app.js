/* Crônicas da Fenda — cliente web (tema pixel art).
   Recebe as mensagens do motor (SSE) e as processa em fila: texto com ritmo, dado animado,
   HUD que reage a cada mudança, combate golpe a golpe, mapa clicável e telas visuais. */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const spr = (nome, escala = 2, classe = "") => Sprites.img(nome, escala, classe);
function el(tag, classe, html) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (html !== undefined) e.innerHTML = html;
  return e;
}
function guardar(chave, valor) { try { localStorage.setItem(chave, valor); } catch (e) { /* sem armazenamento */ } }
function ler(chave) { try { return localStorage.getItem(chave); } catch (e) { return null; } }

const TOKEN = new URLSearchParams(location.search).get("token") || "";
const VELOCIDADES = { lento: 60, normal: 120, rapido: 300, instantaneo: 0 };
const ORDEM_VEL = ["lento", "normal", "rapido", "instantaneo"];
const NOME_VEL = { lento: "lento", normal: "normal", rapido: "rápido", instantaneo: "instantâneo" };
const SIGLA = { "Força": "FOR", "Destreza": "DES", "Arcano": "ARC", "Percepção": "PER", "Vontade": "VON", "Carisma": "CAR" };
const COR_PROSA = { cinza: "sussurro", vermelho: "perigo", verde: "bom", amarelo: "destaque", magenta: "arcano",
  ciano: "nota", azul: "frio", branco: "destaque" };
const RECURSO_BARRA = { Vigor: "vigor", Mana: "mana", Foco: "foco" };
const RECURSO_ICONE = { Vigor: "chama", Mana: "pocao_azul", Foco: "olho" };
const D20 = '<svg viewBox="-30 -30 60 60"><polygon class="face" points="0,-27 23,-13 23,13 0,27 -23,13 -23,-13"/>' +
  '<path class="aresta" d="M0,-15 L13,8 L-13,8 Z M0,-27 L0,-15 M0,-15 L23,-13 M0,-15 L-23,-13 M13,8 L23,-13 M13,8 L23,13 M13,8 L0,27 M-13,8 L-23,-13 M-13,8 L-23,13 M-13,8 L0,27"/>' +
  '<text x="0" y="1">20</text></svg>';
const SISTEMA = [
  [/^Talentos/, "Talentos", "t", "estrela"], [/^Personagem e inventário/, "Personagem", "p", "armadura"],
  [/^Comitiva/, "Comitiva", "c", "escudo"], [/^Mapa$/, "Mapa", "", "pergaminho"], [/^Diário/, "Diário", "d", "livro"],
  [/^Bestiário/, "Bestiário", "b", "caveira"], [/^Salvar jogo/, "Salvar", "g", "pergaminho"], [/^Sair do jogo/, "Sair", "q", "bolsa_vazia"],
];

const corpo = document.body;
const pagina = $("#pagina"), folha = $("#folha"), cab = $("#cena-cab"), textoEl = $("#texto"), promptEl = $("#prompt");
const histLista = $("#historico-lista");

let velocidade = ler("cdf-velocidade") || "normal";
const fila = [];
let processando = false, pular = false, replay = false;
let estado = null, pergunta = null, pendente = null;
let capitular = false, seguir = true;
let ultimosRecursos = {};

const App = {
  get estado() { return estado; },
  responder: (id, valor) => responder(id, valor),
  pedir: (rotulo, chave, valor) => pedir(rotulo, chave, valor),
  som: (n) => Som.tocar(n),
  acaoFecharTalentos: null,
};

/* ------------------------------------------------------------------ conexão */
function conectar() {
  const fonte = new EventSource(`/eventos?token=${encodeURIComponent(TOKEN)}`);
  fonte.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.t === "fim") fonte.close();
    fila.push(m);
    processar();
  };
}

async function responder(id, valor) {
  if (!pergunta || pergunta.id !== id) return;
  pergunta = null;
  promptEl.querySelectorAll(".escolhas").forEach((u) => u.classList.add("escolhido"));
  Som.tocar("escolha");
  try {
    await fetch("/responder", { method: "POST", headers: { "Content-Type": "application/json", "X-Token": TOKEN },
      body: JSON.stringify({ id, valor }) });
  } catch (e) { console.error(e); }
}

/** Escolhe uma opção do menu atual pelo rótulo e deixa um pedido para o menu seguinte (ex.: "Viajar" → destino). */
function pedir(rotulo, chave, valor) {
  if (!pergunta || pergunta.tipo !== "opcoes") return;
  const direta = pergunta.opcoes.findIndex((o) => o.meta && o.meta[chave] === valor);
  if (direta >= 0) { responder(pergunta.id, direta); return; }
  const i = pergunta.opcoes.findIndex((o) => o.texto.startsWith(rotulo));
  if (i < 0) return;
  pendente = valor === null ? null : { chave, valor };
  responder(pergunta.id, i);
}

/* ------------------------------------------------------------------ fila */
async function processar() {
  if (processando) return;
  processando = true;
  while (fila.length) {
    const m = fila.shift();
    if (m.replay) replay = true;
    if (!["estado", "sincronizado", "talentos"].includes(m.t)) {
      const primeiro = promptEl.firstElementChild;
      if (primeiro && !primeiro.classList.contains("dica-pular")) limparPrompt();
    }
    try { await tratar(m); } catch (e) { console.error("falha ao tratar", m, e); }
  }
  processando = false;
  pular = false;
}

function instantaneo() { return pular || replay || velocidade === "instantaneo"; }
function cps() { return VELOCIDADES[velocidade] * (estado && estado.combate ? 2.5 : 1); }
function ritmo(ms) { return instantaneo() ? 0 : ms * (velocidade === "lento" ? 1.4 : velocidade === "rapido" ? 0.5 : 1); }

async function tratar(m) {
  switch (m.t) {
    case "estado": aplicarEstado(m.estado); break;
    case "sincronizado": replay = false; break;
    case "nova_cena": await novaCena(m); break;
    case "cabecalho": cabecalho(m); break;
    case "texto": await texto(m); break;
    case "efeito": await efeito(m); break;
    case "rolagem": await rolagem(m); break;
    case "combate": faixaCombate(m); break;
    case "turno": turno(m); break;
    case "fim_combate": if (!instantaneo()) await espera(m.resultado === "vitoria" ? 800 : 400); break;
    case "celebrar": await Telas.celebrar(m, instantaneo()); break;
    case "talentos": Telas.guardarArvore(m.arvore); break;
    case "painel": anexar(Telas.painel(m)); break;
    case "subtitulo": anexar(el("div", "subtitulo", esc(m.texto))); break;
    case "separador": anexar(el("hr")); break;
    case "bloco": bloco(m); break;
    case "mapa": mapaNaPagina(m); break;
    case "escolhido": eco(m); break;
    case "opcoes": mostrarOpcoes(m); break;
    case "continuar": mostrarContinuar(m); break;
    case "pergunta": mostrarPergunta(m); break;
    case "erro": anexar(el("p", "erro", "Algo deu errado: " + esc(m.texto))); break;
    case "fim": $("#aviso-fim").hidden = false; break;
  }
}

/* ------------------------------------------------------------------ página */
function anexar(no) { textoEl.appendChild(no); rolarFim(); return no; }
function rolarFim() { if (seguir) pagina.scrollTop = pagina.scrollHeight; }
pagina.addEventListener("scroll", () => { seguir = pagina.scrollTop + pagina.clientHeight >= pagina.scrollHeight - 80; }, { passive: true });

function cabecalho(m) {
  cab.dataset.tipo = m.tipo || "evento";
  cab.innerHTML = `<h1 class="cena-titulo">${esc(m.titulo)}</h1>` + (m.subtitulo ? `<div class="cena-sub">${esc(m.subtitulo)}</div>` : "") +
    `<div class="ornamento"><i></i><b></b><i></i></div>`;
  corpo.classList.toggle("modo-titulo", m.tipo === "titulo");
  if (m.tipo === "titulo") { corpo.classList.add("sem-heroi"); corpo.classList.remove("em-combate"); estado = null; }
  capitular = ["evento", "local", "chefe", "vitoria", "morte"].includes(m.tipo);
  historico("h-cena", m.titulo);
  if (m.titulo !== "Talentos") Telas.fecharTalentos();
}

async function novaCena(m) {
  if (!instantaneo() && textoEl.childElementCount) { folha.classList.add("saindo"); await espera(200); }
  textoEl.innerHTML = "";
  promptEl.innerHTML = "";
  folha.classList.remove("saindo");
  cabecalho(m);
  folha.classList.remove("entrando"); void folha.offsetWidth; folha.classList.add("entrando");
  pagina.scrollTop = 0;
  seguir = true;
  if (!replay) Som.tocar("pagina");
}

async function revelar(no, texto) {
  if (instantaneo() || !cps()) { no.textContent = texto; rolarFim(); return; }
  await new Promise((fim) => {
    let i = 0, antes = performance.now();
    function passo(agora) {
      if (pular) { no.textContent = texto; rolarFim(); fim(); return; }
      i = Math.min(texto.length, i + Math.max(0.5, ((agora - antes) / 1000) * cps()));
      antes = agora;
      no.textContent = texto.slice(0, Math.floor(i));
      rolarFim();
      if (i >= texto.length) fim(); else requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  });
}

async function texto(m) {
  if (m.mono) {
    let pre = textoEl.lastElementChild;
    if (!pre || !pre.classList.contains("mono")) pre = anexar(el("pre", "mono"));
    pre.textContent += (pre.textContent ? "\n" : "") + m.texto;
    historico("", m.texto);
    return;
  }
  const p = el("p");
  const [base, ...mods] = (m.cor || "").split("+");
  if (COR_PROSA[base]) p.classList.add(COR_PROSA[base]);
  if (mods.includes("negrito")) p.classList.add("forte");
  const limpo = m.texto.trim();
  if (/^["“—«]/.test(limpo)) p.classList.add("fala");
  if (capitular && !m.cor && limpo.length > 80 && /^[A-ZÀ-Ý]/.test(limpo)) { p.classList.add("capitular"); capitular = false; }
  anexar(p);
  mostrarDica();
  await revelar(p, m.texto);
  historico("", m.texto);
  if (!instantaneo()) await espera(Math.min(240, 20000 / (cps() || 120)));
}

function iconeChip(m) {
  const t = m.texto;
  const porNome = ["Odete", "Morel", "Yara"].find((n) => t.includes(n));
  if ((m.tipo === "aprova" || m.tipo === "desaprova") && porNome) return porNome.toLowerCase();
  if (m.tipo === "item") {
    if (/comida|Provis/i.test(t)) return "pernil";
    if (/Tocha/.test(t)) return "tocha";
    if (/Bandagem/.test(t)) return "bandagem";
    if (/Tônico|Unguento/.test(t)) return "pocao_azul";
    if (/Poção/.test(t)) return "pocao";
    if (/[Ff]lecha/.test(t)) return "aljava";
    return "saco";
  }
  return { ouro: "moeda", perda: "bolsa_vazia", xp: "estrela", dano: "gota", cura: "coracao", rep: "escudo",
    ferimento: "gota", nivel: "estrela", info: "pergaminho" }[m.tipo] || "pergaminho";
}

async function efeito(m) {
  let linha = textoEl.lastElementChild;
  if (!linha || !linha.classList.contains("chips") || linha.classList.contains("passado")) linha = anexar(el("div", "chips"));
  linha.appendChild(el("span", `chip ${m.tipo || "info"}`, spr(iconeChip(m), 1) + esc(m.texto)));
  rolarFim();
  historico("h-chip", "▸ " + m.texto);
  if (replay) return;
  if (m.tipo === "ouro") Som.tocar("moeda");
  else if (m.tipo === "nivel") Som.tocar("nivel");
  else if (m.tipo === "item" || m.tipo === "cura") Som.tocar("item");
  else if (m.tipo === "aprova") Som.tocar("aprova");
  else if (m.tipo === "desaprova") Som.tocar("desaprova");
  else if (m.tipo === "ferimento") { Som.tocar("dor"); doer(); Telas.toast("Ferimento", m.texto, "gota"); }
  else if (m.tipo === "dano" || m.tipo === "perda") { Som.tocar("dor"); doer(); }
  await espera(ritmo(m.tipo === "ferimento" ? 700 : 320));
}

async function rolagem(m) {
  const caixa = el("div", "rolagem rolando");
  const sinal = m.mod >= 0 ? "+" : "−";
  caixa.innerHTML = `<div class="d20">${D20}</div><div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
    <div class="rol-conta">d20 ${sinal} ${Math.abs(m.mod)} contra dificuldade <b>${m.cd}</b></div></div><div class="rol-res"></div>`;
  anexar(caixa);
  const num = caixa.querySelector("text");
  if (!instantaneo()) {
    Som.tocar("dado");
    const fim = performance.now() + 950;
    while (performance.now() < fim && !pular) { num.textContent = 1 + Math.floor(Math.random() * 20); await espera(60); }
  }
  num.textContent = m.d20;
  caixa.classList.remove("rolando");
  const critico = m.d20 === 20, desastre = m.d20 === 1;
  caixa.classList.add("pousou", m.sucesso ? "ok" : "falha");
  if (critico) caixa.classList.add("critico");
  caixa.querySelector(".rol-conta").innerHTML = `<b>${m.d20}</b> ${sinal} ${Math.abs(m.mod)} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
  caixa.querySelector(".rol-res").textContent = critico ? "Crítico!" : desastre ? "Desastre" : m.sucesso ? "Sucesso" : "Falha";
  historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
  if (!replay) Som.tocar(critico ? "critico" : m.sucesso ? "sucesso" : "falha");
  if (!instantaneo()) await espera(ritmo(650));
}

function faixaCombate(m) {
  anexar(el("div", "faixa-combate", `⚔ ${esc(m.titulo)}`));
  if (m.subtitulo) anexar(el("div", "faixa-combate-sub", esc(m.subtitulo)));
  historico("h-cena", "⚔ " + m.titulo);
  if (!replay) Som.tocar("golpe");
}

function turno(m) {
  if (m.n > 1) for (const filho of textoEl.children) filho.classList.add("passado");
  while (textoEl.childElementCount > 70) textoEl.firstElementChild.remove();
  anexar(el("div", "divisor-turno", `turno ${m.n}`));
}

function bloco(m) {
  const pre = el("pre");
  pre.innerHTML = m.linhas.map((linha) => linha.map(([t, cor]) => cor ? `<span class="${cor.split("+").map((c) => "c-" + c).join(" ")}">${esc(t)}</span>` : esc(t)).join("")).join("\n");
  anexar(pre);
}

function eco(m) { anexar(el("p", "eco", esc(m.texto))); historico("h-eco", "› " + m.texto); }

function historico(classe, t) {
  const p = el("p", classe);
  p.textContent = t;
  histLista.appendChild(p);
  while (histLista.childElementCount > 4000) histLista.firstElementChild.remove();
}

function mostrarDica() {
  if (replay || velocidade === "instantaneo" || promptEl.childElementCount) return;
  if (Number(ler("cdf-dica") || 0) > 25) return;
  promptEl.innerHTML = '<div class="dica-pular">qualquer tecla ou clique adianta o texto</div>';
}

let ultimaDor = 0;
function doer() {
  const agora = performance.now();
  if (agora - ultimaDor < 400) return;
  ultimaDor = agora;
  const d = $(".camada.dor");
  d.classList.remove("ativa"); void d.offsetWidth; d.classList.add("ativa");
}

/* ------------------------------------------------------------------ escolhas */
function limparPrompt() { promptEl.innerHTML = ""; pergunta = null; }
function atalhoDe(t) { return SISTEMA.find(([re]) => re.test(t)); }

function mostrarOpcoes(m) {
  // Pedido pendente (ex.: clicou num destino do mapa a partir do menu do local): responde sozinho.
  if (pendente) {
    const p = pendente;
    pendente = null;
    const i = m.opcoes.findIndex((o) => o.meta && o.meta[p.chave] === p.valor);
    if (i >= 0) { pergunta = { id: m.id, tipo: "opcoes", opcoes: m.opcoes }; responder(m.id, i); return; }
  }
  promptEl.innerHTML = "";
  pergunta = { id: m.id, tipo: "opcoes", n: m.opcoes.length, opcoes: m.opcoes, numeros: [], letras: {} };
  if (m.opcoes.some((o) => o.meta && o.meta.talento) && Telas.abrirTalentos(m)) {
    const b = el("button", "continuar", "Abrir a árvore de talentos <span>▸</span>");
    b.addEventListener("click", (ev) => { ev.stopPropagation(); Telas.abrirTalentos(m); });
    promptEl.appendChild(b);
    return;
  }
  Telas.fecharTalentos();
  if (m.pergunta) promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const lista = el("ol", "escolhas");
  const sistema = m.opcoes.filter((o) => atalhoDe(o.texto)).length >= 4;
  const atalhos = el("div", "atalhos");
  m.opcoes.forEach((o, i) => {
    const at = sistema && atalhoDe(o.texto);
    if (at) {
      const pontos = /★\s*(\d+)/.exec(o.texto);
      const carta = /✉/.test(o.texto);
      const qtd = /^Comitiva \((\d+)\)/.exec(o.texto);
      const b = el("button", "atalho" + (pontos || carta ? " destaque" : ""));
      b.type = "button";
      b.innerHTML = spr(at[3], 1) + esc(at[1]) + (qtd ? ` ${qtd[1]}` : "") + (pontos ? ` <b>★${pontos[1]}</b>` : "") + (carta ? " <b>✉</b>" : "") +
        (at[2] ? `<kbd>${at[2].toUpperCase()}</kbd>` : "");
      b.title = o.texto;
      b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
      atalhos.appendChild(b);
      if (at[2]) pergunta.letras[at[2]] = i;
      return;
    }
    pergunta.numeros.push(i);
    const li = el("li");
    const b = el("button", "escolha");
    b.type = "button";
    b.style.animationDelay = `${replay ? 0 : i * 40}ms`;
    if (/^(Voltar|Sair|Cancelar|Nada|Ignorar|Fechar)/.test(o.texto)) b.classList.add("secundaria");
    const pos = pergunta.numeros.length - 1;
    const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
    let teste = "", icone = "";
    if (o.teste) {
      const nivel = o.teste.mod >= 4 ? "bom" : o.teste.mod >= 1 ? "medio" : "ruim";
      const sinal = o.teste.mod >= 0 ? "+" : "−";
      teste = `<span class="teste ${nivel}" title="Teste de ${esc(o.teste.atributo)}: você rola um d20 e soma ${sinal}${Math.abs(o.teste.mod)} contra uma dificuldade que só o mundo conhece.">${SIGLA[o.teste.atributo] || esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</span>`;
    }
    if (o.meta && o.meta.local !== undefined && estado) {
      const n = estado.mapa.nos.find((x) => x.id === o.meta.local);
      if (n) icone = spr(MapaPx.sprite(n), 1);
    }
    if (o.meta && o.meta.item) icone = spr(Telas.ICONE_ITEM[o.meta.item] || "pocao", 1);
    b.innerHTML = `<span class="tecla">${tecla}</span>${icone}<span class="rotulo">${esc(o.texto)}</span>${teste}`;
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
    li.appendChild(b);
    lista.appendChild(li);
  });
  if (lista.childElementCount) promptEl.appendChild(lista);
  if (atalhos.childElementCount) promptEl.appendChild(atalhos);
  if (!replay) guardar("cdf-dica", String(Number(ler("cdf-dica") || 0) + 1));
  if (estado) { desenharMundo(estado); atualizarMapasDaPagina(); }
  rolarFim();
}

function mostrarContinuar(m) {
  promptEl.innerHTML = "";
  const b = el("button", "continuar", "Continuar <span>▸</span>");
  b.type = "button";
  b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, null); });
  promptEl.appendChild(b);
  pergunta = { id: m.id, tipo: "continuar" };
  rolarFim();
}

function mostrarPergunta(m) {
  promptEl.innerHTML = "";
  promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const linha = el("div", "entrada-texto");
  const input = el("input");
  input.placeholder = m.padrao || "";
  input.maxLength = 40;
  input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); responder(m.id, input.value || m.padrao || ""); } });
  const ok = el("button", "continuar", "Confirmar <span>▸</span>");
  ok.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, input.value || m.padrao || ""); });
  linha.append(input, ok);
  promptEl.appendChild(linha);
  pergunta = { id: m.id, tipo: "pergunta" };
  setTimeout(() => input.focus(), 50);
  rolarFim();
}

/* ------------------------------------------------------------------ viagem pelo mapa */
function destinosClicaveis() {
  if (!pergunta || pergunta.tipo !== "opcoes" || !estado) return new Set();
  const diretos = pergunta.opcoes.filter((o) => o.meta && o.meta.local !== undefined).map((o) => o.meta.local);
  if (diretos.length) return new Set(diretos);
  if (pergunta.opcoes.some((o) => o.texto === "Viajar")) return new Set(estado.mapa.nos.filter((n) => n.distancia).map((n) => n.id));
  return new Set();
}
function viajarPara(id) { pedir("Viajar", "local", id); }

function mapaNaPagina() {
  if (!estado) return;
  const caixa = el("div", "mapa-pagina");
  caixa.dataset.mapa = "1";
  anexar(caixa);
  atualizarMapasDaPagina();
}
function atualizarMapasDaPagina() {
  if (!estado) return;
  textoEl.querySelectorAll("[data-mapa]").forEach((caixa) => {
    const clic = destinosClicaveis();
    caixa.innerHTML = "";
    caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, clicaveis: clic, aoClicar: viajarPara, nivelHeroi: estado.heroi.nivel }));
    if (clic.size) caixa.appendChild(el("div", "mapa-dica", "Clique num destino no mapa para viajar"));
  });
}

/* ------------------------------------------------------------------ estado e painéis */
function pct(a, b) { return b ? Math.max(0, Math.min(100, (100 * a) / b)) : 0; }
function barra(classe, atual, maximo, anterior) {
  const de = anterior === undefined ? pct(atual, maximo) : pct(anterior, maximo);
  return `<span class="barra-px ${classe}" data-alvo="${pct(atual, maximo)}"><span class="rastro" style="width:${de}%"></span><span class="enchimento" style="width:${de}%"></span></span>`;
}
function animarBarras(raiz) {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    raiz.querySelectorAll(".barra-px[data-alvo]").forEach((b) => b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = b.dataset.alvo + "%"; }));
  }));
}
function flutuar(alvo, texto, classe) {
  if (!alvo || replay) return;
  const f = el("span", "flutua " + classe, esc(texto));
  alvo.appendChild(f);
  setTimeout(() => f.remove(), 1300);
}

function aplicarEstado(e) {
  const antes = estado;
  estado = e;
  corpo.classList.remove("sem-heroi");
  const bioma = e.local.tipo === "vila" ? "vila" : e.local.bioma;
  corpo.dataset.bioma = bioma;
  corpo.dataset.periodo = e.mundo.periodo_n;
  corpo.classList.toggle("escuro", !!e.mundo.escuro);
  corpo.classList.toggle("em-combate", !!e.combate);
  corpo.style.setProperty("--corrupcao", (e.mundo.corrupcao / 100).toFixed(2));
  Som.ambiente(bioma);
  Vista.atualizar(e);
  $("#tempo").textContent = `Dia ${e.mundo.dia} · ${e.mundo.periodo} · ${e.mundo.clima}`;
  $("#corrupcao-topo .enchimento").style.width = e.mundo.corrupcao + "%";
  $("#corrupcao-topo .valor").textContent = e.mundo.corrupcao + "%";
  $("#sigilos-topo").innerHTML = [0, 1, 2].map((i) => `<i class="sigilo${i < e.heroi.sigilos ? " tem" : ""}"></i>`).join("");
  desenharHud(e.heroi, antes && antes.heroi);
  desenharBatalha(e.combate, antes && antes.combate);
  desenharHeroi(e.heroi);
  const mudouMapa = !antes || antes.local.id !== e.local.id || JSON.stringify(antes.mapa) !== JSON.stringify(e.mapa) || antes.heroi.nivel !== e.heroi.nivel;
  if (mudouMapa) desenharMundo(e);
  if (!$("#sobre-mapa").hidden && mudouMapa) desenharMapaGrande();
}

function recurso(id, icones, qtd, opts = {}) {
  const imgs = icones.map((n) => spr(n, 2)).join("");
  return `<div class="recurso${opts.alerta ? " alerta" : ""}${opts.vazio ? " vazio" : ""}" data-rec="${id}" title="${esc(opts.titulo || "")}">
    <div class="icones">${imgs}</div><div class="qtd">${qtd}</div></div>`;
}
function repetir(nome, n) { return Array.from({ length: n }, () => nome); }

function desenharHud(h, antes) {
  const comida = h.provisoes === 0 ? ["osso"] : repetir("pernil", h.provisoes <= 2 ? 1 : h.provisoes <= 5 ? 2 : 3);
  const tochas = h.tochas === 0 ? ["tocha_apagada"] : repetir("tocha", h.tochas <= 2 ? 1 : 2);
  const ouro = h.ouro === 0 ? ["bolsa_vazia"] : h.ouro < 60 ? ["moeda"] : h.ouro < 200 ? ["moedas"] : ["saco"];
  const pocoes = h.pocoes === 0 ? ["frasco_vazio"] : repetir("pocao", Math.min(3, h.pocoes));
  const vidaCritica = h.hp <= h.max_hp * 0.3;
  const feridas = h.ferimentos.length ? `<div class="recurso alerta" data-rec="feridas" title="${esc(h.males.join(" · "))}"><div class="icones">${spr("gota", 2)}</div><div class="qtd">${h.ferimentos.length}</div></div>` : "";
  $("#hud-linha").innerHTML = `
    <div class="hud-retrato" title="${esc(h.titulo)} nível ${h.nivel}">${spr(h.classe, 3)}<span class="nivel">${h.nivel}</span></div>
    <div class="hud-vitais">
      <div class="hud-nome"><b>${esc(h.nome)}</b><span>${esc(h.titulo)}${h.fome ? " · com fome" : ""}</span></div>
      <div class="vital${vidaCritica ? " critico" : ""}" data-vital="hp">${spr("coracao", 1)}${barra("vida", h.hp, h.max_hp, antes ? antes.hp : undefined)}<span class="num">${h.hp}/${h.max_hp}</span></div>
      <div class="vital" data-vital="rec">${spr(RECURSO_ICONE[h.recurso] || "estrela", 1)}${barra(RECURSO_BARRA[h.recurso] || "mana", h.rec, h.max_rec, antes ? antes.rec : undefined)}<span class="num">${h.rec}/${h.max_rec}</span></div>
    </div>
    <div class="hud-recursos">
      ${recurso("provisoes", comida, `${h.provisoes}<small>d</small>`, { alerta: h.provisoes <= 1, vazio: !h.provisoes, titulo: h.provisoes ? `Comida para ${h.provisoes} dia(s). Cada dia consome 1 (e cada companheiro come também).` : "Sem comida! Você vai passar fome." })}
      ${recurso("tochas", tochas, h.tochas, { alerta: h.tochas === 0, vazio: !h.tochas, titulo: "Tochas: luz para a noite, ruínas e a cidadela." })}
      ${recurso("ouro", ouro, h.ouro, { vazio: !h.ouro, titulo: "Ouro" })}
      ${recurso("pocoes", pocoes, h.pocoes, { vazio: !h.pocoes, titulo: "Poções de vida (35% da vida)" })}
      ${recurso("bandagens", ["bandagem"], h.bandagens, { vazio: !h.bandagens, alerta: !h.bandagens && h.ferimentos.some((f) => f.aberto), titulo: "Bandagens: estancam sangramento e tratam feridas abertas" })}
      ${h.flechas !== null && h.flechas !== undefined ? recurso("flechas", ["aljava"], h.flechas, { alerta: h.flechas <= 5, titulo: "Flechas" }) : ""}
      ${feridas}
    </div>`;
  animarBarras($("#hud-linha"));
  // Feedback: o que mudou desde o último estado
  const agora = { provisoes: h.provisoes, tochas: h.tochas, ouro: h.ouro, pocoes: h.pocoes, bandagens: h.bandagens, flechas: h.flechas };
  if (antes && !replay) {
    for (const [k, v] of Object.entries(agora)) {
      const velho = ultimosRecursos[k];
      if (velho === undefined || v === null || v === undefined || v === velho) continue;
      const alvo = $(`.recurso[data-rec="${k}"]`);
      if (!alvo) continue;
      alvo.classList.add(v > velho ? "ganhou" : "perdeu");
      flutuar(alvo, `${v > velho ? "+" : "−"}${Math.abs(v - velho)}`, v > velho ? "mais" : "menos");
    }
    if (h.hp !== antes.hp) flutuar($('.vital[data-vital="hp"]'), `${h.hp > antes.hp ? "+" : "−"}${Math.abs(h.hp - antes.hp)}`, h.hp > antes.hp ? "cura" : "menos");
    if (h.hp < antes.hp) { doer(); Som.tocar("dor"); }
  }
  ultimosRecursos = agora;
}

function iconeCarta(c) {
  if (c.lado === "aliado") return c.cid || (c.tipo === "servo" ? "caveira" : "fera");
  return Telas.iconeCriatura(c.tracos, "");
}

function desenharBatalha(cb, antes) {
  const raiz = $("#batalha");
  if (!cb) { raiz.innerHTML = ""; return; }
  const anteriores = {};
  if (antes) [...antes.inimigos, ...antes.aliados].forEach((c) => { anteriores[c.lado + ":" + c.nome] = c; });
  let golpe = false, morte = false;
  const carta = (c) => {
    const ant = anteriores[c.lado + ":" + c.nome];
    const dano = ant ? ant.hp - c.hp : 0;
    const classes = ["carta", c.lado];
    if (c.chefe) classes.push("chefe");
    if (c.unico) classes.push("unico");
    if (!c.vivo) { classes.push("morta"); if (ant && ant.vivo && !replay) { classes.push("morrendo"); morte = true; } }
    else if (dano > 0 && !replay) { classes.push("atingida"); golpe = true; }
    const efeitos = c.efeitos.length ? `<div class="carta-efeitos">${c.efeitos.map((f) => `<span class="efeito-tag">${esc(f.nome)} ${f.turnos}</span>`).join("")}</div>` : "";
    const num = dano && !replay ? `<span class="flutua ${dano > 0 ? "menos" : "cura"}">${dano > 0 ? "−" : "+"}${Math.abs(dano)}</span>` : "";
    return `<div class="${classes.join(" ")}" title="${esc(c.nome)}">${num}
      <div class="icone">${spr(iconeCarta(c), 2)}</div>
      <div class="carta-nome"><span>${esc(c.nome)}</span>${c.nivel ? `<small>Nv.${c.nivel}</small>` : ""}</div>
      <div class="carta-hp">${barra(c.lado === "aliado" ? "aliado" : "vida", c.hp, c.max_hp, ant ? ant.hp : undefined)}<span>${c.vivo ? `${c.hp}/${c.max_hp}` : "morto"}</span></div>
      ${c.preparando && c.vivo ? '<div class="preparando">⚠ prepara um golpe devastador</div>' : ""}${c.vivo ? efeitos : ""}</div>`;
  };
  const aliados = cb.aliados.filter((a) => a.vivo || (anteriores["aliado:" + a.nome] && anteriores["aliado:" + a.nome].vivo));
  raiz.innerHTML = `<div class="lado aliados">${aliados.map(carta).join("")}</div><div class="versus">vs</div>
    <div class="lado inimigos">${cb.inimigos.map(carta).join("")}</div>`;
  animarBarras(raiz);
  if (morte) Som.tocar("morte"); else if (golpe) Som.tocar("golpe");
}

function desenharHeroi(h) {
  const icAttr = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
  const attrs = Object.entries(h.atributos).map(([k, v]) => `<div class="atributo">${spr(icAttr[k] || "estrela", 1)}<span class="nome">${esc(k)}</span><span class="valor">${v}</span></div>`).join("");
  const slot = (it, padrao) => {
    if (!it) return `<div class="slot-px vazio" title="vazio">${spr(padrao, 2)}</div>`;
    const ic = it.slot === "arma" ? Telas.ARMA[h.classe] : it.slot === "armadura" ? "armadura" : "amuleto";
    return `<div class="slot-px r-${esc(it.raridade)}" title="${esc(it.nome)}\n${esc(it.bonus)}">${spr(ic, 2)}</div>`;
  };
  const feridas = h.ferimentos.length ? h.ferimentos.map((f) => `<div class="ferimento">${spr("gota", 1)}${esc(f.nome)} <small>${f.dias ? f.dias + "d" : ""}${f.aberto ? " · aberto" : ""}</small></div>`).join("")
    : '<div class="vazio">nenhum, por enquanto</div>';
  const habs = h.habilidades.map((x) => `<div class="habilidade" title="${esc(x.desc)}"><span>${esc(x.nome)}</span><small>${x.custo} ${esc(h.recurso)}</small></div>`).join("");
  const bolsa = h.bolsa.filter((b) => b.id !== "tocha").map((b) => `<div class="slot-px" title="${esc(b.nome)}: ${esc(b.desc)}">${spr(Telas.ICONE_ITEM[b.id] || "pocao", 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
  const comitiva = h.comitiva && h.comitiva.length ? `<div class="secao"><h3>Comitiva</h3>${h.comitiva.map((m) =>
    `<div class="membro${m.ferido ? " ferido" : ""}" title="${esc(m.titulo)} · aprovação ${m.aprovacao > 0 ? "+" : ""}${m.aprovacao}${m.ferido ? " · ferido, fora de combate até descansar" : ""}">
      <div class="icone">${spr(m.id, 2)}</div>
      <div class="membro-nome"><span>${esc(m.nome)}</span>${m.conversa ? '<span class="membro-carta" title="Quer conversar">✉</span>' : ""}</div>
      ${barra("aliado fina", m.hp, m.max_hp)}${Telas.aprovacao(m)}</div>`).join("")}</div>` : "";
  $("#heroi").innerHTML = `
    <div class="identidade"><div class="retrato-grande">${spr(h.classe, 3)}</div>
      <div><div class="heroi-nome">${esc(h.nome)}</div><div class="heroi-titulo">${esc(h.titulo)} · nível ${h.nivel}</div></div></div>
    <div class="xp-linha"><div class="legenda-linha"><span>Experiência</span><span>${h.xp}/${h.xp_proximo}</span></div>${barra("xp", h.xp, h.xp_proximo)}</div>
    ${h.pontos_talento ? `<div class="talento-aviso" title="Abra Talentos (T) num local">${spr("estrela", 1)} ${h.pontos_talento} ponto(s) de talento</div>` : ""}
    <div class="secao"><h3>Atributos</h3><div class="atributos">${attrs}</div></div>
    <div class="secao"><h3>Equipado</h3><div class="slots">${slot(h.equip.arma, Telas.ARMA[h.classe])}${slot(h.equip.armadura, "armadura")}${slot(h.equip.amuleto, "amuleto")}</div></div>
    ${comitiva}
    <div class="secao"><h3>Ferimentos</h3>${feridas}</div>
    <div class="secao"><h3>Habilidades</h3>${habs}</div>
    <div class="secao"><h3>Bolsa</h3><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div></div>
    <div class="secao"><div class="linhas"><div class="linha"><span>Reputação</span><b>${h.reputacao > 0 ? "+" : ""}${h.reputacao}</b></div></div></div>`;
  animarBarras($("#heroi"));
}

function nivelPerigo(nivel) {
  if (nivel === null || nivel === undefined || !estado) return "";
  const d = nivel - estado.heroi.nivel;
  return d >= 2 ? "alto" : d >= 0 ? "medio" : "baixo";
}

function desenharMundo(e) {
  const l = e.local;
  const clic = destinosClicaveis();
  const caminhos = e.mapa.nos.filter((n) => n.distancia).sort((a, b) => a.distancia - b.distancia || a.nome.localeCompare(b.nome))
    .map((n) => `<div class="caminho${clic.has(n.id) ? " clicavel" : ""}" data-local="${n.id}">${spr(MapaPx.sprite(n), 2)}
      <span class="nome">${esc(n.nome)} ${n.nivel ? `<span class="perigo-tag ${nivelPerigo(n.nivel)}">Nv.${n.nivel}</span>` : ""}<small>${esc(n.descricao)}</small></span>
      <span class="dist">${n.distancia} trecho${n.distancia > 1 ? "s" : ""}</span></div>`).join("");
  const raiz = $("#mundo");
  raiz.innerHTML = `<div class="local-nome">${esc(l.nome)}</div><div class="local-desc">${esc(l.descricao)}</div>
    ${l.nivel ? `<span class="perigo-tag ${nivelPerigo(l.nivel)}">inimigos Nv.${l.nivel}</span>` : ""}<div id="mapa-mini"></div>
    <div class="secao"><h3>Caminhos</h3><div class="caminhos">${caminhos || '<div class="vazio">nenhum</div>'}</div></div>`;
  const mini = MapaPx.criar(e.mapa, { clicaveis: clic, aoClicar: viajarPara, nivelHeroi: e.heroi.nivel });
  mini.title = "Abrir o mapa (M)";
  mini.addEventListener("click", (ev) => { if (!ev.target.closest(".clicavel")) alternarMapa(true); });
  $("#mapa-mini").appendChild(mini);
  if (clic.size) $("#mapa-mini").appendChild(el("div", "mapa-dica", "Clique num destino para viajar"));
  raiz.querySelectorAll(".caminho.clicavel").forEach((c) => c.addEventListener("click", () => viajarPara(Number(c.dataset.local))));
}

function legendaMapa() {
  return [["floresta", "floresta"], ["pantano", "pântano"], ["montanha", "montanha"], ["planicie", "planície"], ["ruinas", "ruínas"],
    ["cidadela", "cidadela"], ["vila", "vila"], ["covil", "covil de guardião"], ["vencido", "covil vencido"]]
    .map(([s, n]) => `<span>${spr(s, 1)} ${n}</span>`).join("");
}
function desenharMapaGrande() {
  if (!estado) return;
  const caixa = $("#mapa-grande");
  caixa.innerHTML = "";
  caixa.appendChild(MapaPx.criar(estado.mapa, { grande: true, clicaveis: destinosClicaveis(), nivelHeroi: estado.heroi.nivel,
    aoClicar: (id) => { alternarMapa(false); viajarPara(id); } }));
  $("#mapa-legenda").innerHTML = legendaMapa();
}

/* ------------------------------------------------------------------ controles */
function alternarHistorico(forcar) {
  const g = $("#gaveta-historico");
  g.hidden = forcar === undefined ? !g.hidden : !forcar;
  if (!g.hidden) histLista.scrollTop = histLista.scrollHeight;
}
function alternarMapa(forcar) {
  const s = $("#sobre-mapa");
  s.hidden = forcar === undefined ? !s.hidden : !forcar;
  if (!s.hidden) desenharMapaGrande();
}
function mudarVelocidade() {
  velocidade = ORDEM_VEL[(ORDEM_VEL.indexOf(velocidade) + 1) % ORDEM_VEL.length];
  guardar("cdf-velocidade", velocidade);
  $("#vel-rotulo").textContent = NOME_VEL[velocidade];
}
function alternarSom() {
  Som.iniciar();
  const ligado = Som.alternar();
  $("#botao-som").classList.toggle("desligado", !ligado);
  if (ligado && estado) Som.ambiente(corpo.dataset.bioma);
}
function fecharTudo() {
  if (!$("#sobre-talentos").hidden && App.acaoFecharTalentos) { Telas.fecharTalentos(); App.acaoFecharTalentos(); return; }
  $("#gaveta-historico").hidden = true;
  $("#sobre-mapa").hidden = true;
  corpo.classList.remove("mostrar-heroi", "mostrar-mundo");
}

let audioPronto = false;
function primeiraInteracao() {
  if (audioPronto) return;
  audioPronto = Som.iniciar();
  if (audioPronto && estado) Som.ambiente(corpo.dataset.bioma);
}

document.addEventListener("click", (ev) => {
  primeiraInteracao();
  const acao = ev.target.closest("[data-acao]");
  if (acao) {
    const a = acao.dataset.acao;
    if (a === "historico") alternarHistorico();
    else if (a === "mapa") alternarMapa();
    else if (a === "velocidade") mudarVelocidade();
    else if (a === "som") alternarSom();
    else if (a === "heroi") corpo.classList.toggle("mostrar-heroi");
    else if (a === "fechar-talentos") fecharTudo();
    return;
  }
  if (ev.target.closest(".talento-aviso")) { pedir("Talentos", "_", null); return; }
  if (processando && ev.target.closest("#pagina")) pular = true;
});

document.addEventListener("keydown", (ev) => {
  primeiraInteracao();
  if (ev.target.tagName === "INPUT") { if (ev.key === "Escape") ev.target.blur(); return; }
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
  const k = ev.key;
  if (k === "Escape") { fecharTudo(); return; }
  if (pergunta && pergunta.letras && pergunta.letras[k.toLowerCase()] !== undefined && !processando) {
    ev.preventDefault(); responder(pergunta.id, pergunta.letras[k.toLowerCase()]); return;
  }
  if (k === "F2" || k === "h" || k === "H") { ev.preventDefault(); alternarHistorico(); return; }
  if (k === "m" || k === "M") { alternarMapa(); return; }
  if (k === "F3" || k === "v" || k === "V") { ev.preventDefault(); mudarVelocidade(); return; }
  if (k === "s" || k === "S") { alternarSom(); return; }
  if (k === "i" || k === "I") { corpo.classList.toggle("mostrar-heroi"); return; }
  if (processando && !pergunta) { if (k.length === 1 || k === "Enter") { ev.preventDefault(); pular = true; } return; }
  if (!pergunta) return;
  if (pergunta.tipo === "continuar" && (k === " " || k === "Enter")) { ev.preventDefault(); responder(pergunta.id, null); return; }
  if (pergunta.tipo !== "opcoes" || !pergunta.numeros) return;
  const botoes = [...promptEl.querySelectorAll(".escolha, .atalho")];
  if (/^[0-9]$/.test(k)) {
    const i = k === "0" ? 9 : Number(k) - 1;
    if (i < pergunta.numeros.length) { ev.preventDefault(); responder(pergunta.id, pergunta.numeros[i]); }
    return;
  }
  const foco = botoes.indexOf(document.activeElement);
  if (k === "ArrowDown" || k === "ArrowUp") {
    ev.preventDefault();
    const n = botoes.length;
    if (!n) return;
    botoes[foco < 0 ? (k === "ArrowDown" ? 0 : n - 1) : (foco + (k === "ArrowDown" ? 1 : -1) + n) % n].focus();
    return;
  }
  if ((k === "Enter" || k === " ") && foco < 0 && pergunta.n === 1) { ev.preventDefault(); responder(pergunta.id, 0); }
});

/* ------------------------------------------------------------------ início */
function brasas() {
  const raiz = $("#brasas");
  for (let i = 0; i < 18; i++) {
    const b = el("span", "brasa");
    b.style.left = (Math.random() * 100).toFixed(1) + "%";
    b.style.animationDuration = (9 + Math.random() * 12).toFixed(1) + "s";
    b.style.animationDelay = (-Math.random() * 20).toFixed(1) + "s";
    b.style.setProperty("--deriva", ((Math.random() - 0.5) * 160).toFixed(0) + "px");
    raiz.appendChild(b);
  }
}

function tema() {
  const raiz = document.documentElement.style;
  raiz.setProperty("--moldura", `url(${Sprites.moldura("#1b1511", "#5a4632", "#8a6e4a", "#c9a227")})`);
  raiz.setProperty("--textura-fundo", `url(${Sprites.textura(["#120e0b", "#16110d", "#0e0b09", "#1a140f"], 64, 11)})`);
  raiz.setProperty("--caveira", `url(${Sprites.url("caveira")})`);
  raiz.setProperty("--cadeado", `url(${Sprites.url("cadeado")})`);
}

// As tochas da HUD tremulam: troca de quadro a cada 400 ms.
setInterval(() => {
  const a = Sprites.url("tocha"), b = Sprites.url("tocha2");
  document.querySelectorAll('.recurso[data-rec="tochas"] img').forEach((img) => {
    if (img.src === a) img.src = b; else if (img.src === b) img.src = a;
  });
}, 400);

async function iniciar() {
  tema();
  try {
    const r = await fetch(`/config?token=${encodeURIComponent(TOKEN)}`);
    const cfg = await r.json();
    if (!ler("cdf-velocidade") && VELOCIDADES[cfg.velocidade] !== undefined) velocidade = cfg.velocidade;
  } catch (e) { /* usa o padrão */ }
  $("#vel-rotulo").textContent = NOME_VEL[velocidade];
  $("#botao-som").classList.toggle("desligado", !Som.ligado);
  brasas();
  conectar();
}
iniciar();
