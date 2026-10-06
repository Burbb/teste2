/* Crônicas da Fenda — cliente web.
   Recebe mensagens do motor (SSE), processa uma de cada vez (texto com ritmo, dado animado,
   estado nos painéis) e só mostra as escolhas quando a cena terminou de ser contada. */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
function el(tag, classe, html) {
  const e = document.createElement(tag);
  if (classe) e.className = classe;
  if (html !== undefined) e.innerHTML = html;
  return e;
}
function guardar(chave, valor) { try { localStorage.setItem(chave, valor); } catch (e) { /* sem armazenamento */ } }
function ler(chave) { try { return localStorage.getItem(chave); } catch (e) { return null; } }

const TOKEN = new URLSearchParams(location.search).get("token") || "";
const VELOCIDADES = { lento: 70, normal: 140, rapido: 320, instantaneo: 0 };
const ORDEM_VEL = ["lento", "normal", "rapido", "instantaneo"];
const NOME_VEL = { lento: "lento", normal: "normal", rapido: "rápido", instantaneo: "instantâneo" };
const SIGLA = { "Força": "FOR", "Destreza": "DES", "Arcano": "ARC", "Percepção": "PER", "Vontade": "VON", "Carisma": "CAR" };
const COR_PROSA = { cinza: "sussurro", vermelho: "perigo", verde: "bom", amarelo: "destaque", magenta: "arcano",
  ciano: "nota", azul: "frio", branco: "destaque" };
const GLIFO = { floresta: "♣", pantano: "≈", montanha: "▲", planicie: "∴", ruinas: "Π", cidadela: "♜", vila: "⌂" };
const NOME_BIOMA = { floresta: "floresta", pantano: "pântano", montanha: "montanha", planicie: "planície",
  ruinas: "ruínas", cidadela: "cidadela", vila: "vila" };
const BRASAO = {
  guerreiro: '<path d="M25 7 L11 21"/><path d="M25 7 L21.5 7.5 M25 7 L24.5 10.5"/><path d="M8 18 L14 24"/><path d="M10.5 21.5 L6 26"/><circle cx="5.3" cy="26.7" r="1.3"/>',
  arqueiro: '<path d="M10 4 Q27 16 10 28"/><path d="M10 4 L10 28"/><path d="M5 16 L27 16 M27 16 L23.5 12.8 M27 16 L23.5 19.2 M5 16 L7.5 13.5 M5 16 L7.5 18.5"/>',
  mago: '<path d="M10 29 L19.5 10.5"/><circle cx="21.5" cy="7" r="4"/><path d="M21.5 1 L21.5 2.3 M27.5 7 L26.2 7 M15.5 7 L16.8 7 M25.7 2.8 L24.8 3.7"/>',
};
const D20 = '<svg viewBox="-30 -30 60 60"><polygon class="face" points="0,-27 23.4,-13.5 23.4,13.5 0,27 -23.4,13.5 -23.4,-13.5"/>' +
  '<path class="aresta" d="M0,-15 L13,8 L-13,8 Z M0,-27 L0,-15 M0,-15 L23.4,-13.5 M0,-15 L-23.4,-13.5 M13,8 L23.4,-13.5 M13,8 L23.4,13.5 M13,8 L0,27 M-13,8 L-23.4,-13.5 M-13,8 L-23.4,13.5 M-13,8 L0,27"/>' +
  '<text x="0" y="1" style="font-size:15px">20</text></svg>';

const corpo = document.body;
const pagina = $("#pagina"), folha = $("#folha"), cab = $("#cena-cab"), textoEl = $("#texto"), promptEl = $("#prompt");
const histLista = $("#historico-lista");

let velocidade = ler("cdf-velocidade") || "normal";
const fila = [];
let processando = false;
let pular = false;
let replay = false;
let estado = null;
let pergunta = null; // {id, tipo}
let capitular = false;
let seguir = true;
let cenas = 0;

/* ------------------------------------------------------------------ conexão */
function conectar() {
  const fonte = new EventSource(`/eventos?token=${encodeURIComponent(TOKEN)}`);
  fonte.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.t === "fim") fonte.close();
    fila.push(m);
    processar();
  };
  return fonte;
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

/* ------------------------------------------------------------------ fila */
async function processar() {
  if (processando) return;
  processando = true;
  while (fila.length) {
    const m = fila.shift();
    if (m.replay) replay = true;
    if (m.t !== "estado" && m.t !== "sincronizado") {
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

async function tratar(m) {
  switch (m.t) {
    case "estado": aplicarEstado(m.estado); break;
    case "sincronizado": replay = false; break;
    case "nova_cena": await novaCena(m); break;
    case "cabecalho": cabecalho(m); break;
    case "texto": await texto(m); break;
    case "efeito": efeito(m); break;
    case "rolagem": await rolagem(m); break;
    case "combate": faixaCombate(m); break;
    case "turno": turno(m); break;
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
function anexar(no) {
  textoEl.appendChild(no);
  rolarFim();
  return no;
}
function rolarFim() { if (seguir) pagina.scrollTop = pagina.scrollHeight; }
pagina.addEventListener("scroll", () => {
  seguir = pagina.scrollTop + pagina.clientHeight >= pagina.scrollHeight - 80;
}, { passive: true });

function cabecalho(m) {
  cab.dataset.tipo = m.tipo || "evento";
  cab.innerHTML = `<h1 class="cena-titulo">${esc(m.titulo)}</h1>` +
    (m.subtitulo ? `<div class="cena-sub">${esc(m.subtitulo)}</div>` : "") +
    `<div class="ornamento"><span>◆</span></div>`;
  corpo.classList.toggle("modo-titulo", m.tipo === "titulo");
  if (m.tipo === "titulo") { corpo.classList.add("sem-heroi"); corpo.classList.remove("em-combate"); estado = null; }
  capitular = ["evento", "local", "chefe", "vitoria", "morte"].includes(m.tipo);
  historico("h-cena", m.titulo);
}

async function novaCena(m) {
  if (!instantaneo() && textoEl.childElementCount) {
    folha.classList.add("saindo");
    await espera(220);
  }
  textoEl.innerHTML = "";
  promptEl.innerHTML = "";
  folha.classList.remove("saindo");
  cabecalho(m);
  folha.classList.remove("entrando");
  void folha.offsetWidth;
  folha.classList.add("entrando");
  pagina.scrollTop = 0;
  seguir = true;
  cenas += 1;
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
  if (!instantaneo()) await espera(Math.min(260, 22000 / (cps() || 140)));
}

function chipsAtuais() {
  const ultimo = textoEl.lastElementChild;
  if (ultimo && ultimo.classList.contains("chips") && !ultimo.classList.contains("passado")) return ultimo;
  return anexar(el("div", "chips"));
}

function efeito(m) {
  chipsAtuais().appendChild(el("span", `chip ${m.tipo || "info"}`, esc(m.texto)));
  rolarFim();
  historico("h-chip", "▸ " + m.texto);
  if (replay) return;
  if (m.tipo === "ouro") Som.tocar("moeda");
  else if (m.tipo === "nivel") Som.tocar("nivel");
  else if (m.tipo === "ferimento" || m.tipo === "dano") { Som.tocar("dor"); doer(); }
}

async function rolagem(m) {
  const caixa = el("div", "rolagem rolando");
  const sinal = m.mod >= 0 ? "+" : "−";
  caixa.innerHTML = `<div class="d20">${D20}</div>
    <div class="rol-info"><div class="rol-attr">Teste de ${esc(m.atributo)}</div>
    <div class="rol-conta">d20 ${sinal} ${Math.abs(m.mod)} contra dificuldade <b>${m.cd}</b></div></div>
    <div class="rol-res"></div>`;
  anexar(caixa);
  const num = caixa.querySelector("text");
  if (!instantaneo()) {
    Som.tocar("dado");
    const fim = performance.now() + 900;
    while (performance.now() < fim && !pular) {
      num.textContent = 1 + Math.floor(Math.random() * 20);
      await espera(55);
    }
  }
  num.textContent = m.d20;
  caixa.classList.remove("rolando");
  const critico = m.d20 === 20, desastre = m.d20 === 1;
  caixa.classList.add("pousou", m.sucesso ? "ok" : "falha");
  if (critico) caixa.classList.add("critico");
  if (desastre) caixa.classList.add("desastre");
  caixa.querySelector(".rol-conta").innerHTML =
    `<b>${m.d20}</b> ${sinal} ${Math.abs(m.mod)} = <b>${m.total}</b> contra <b>${m.cd}</b>`;
  caixa.querySelector(".rol-res").textContent = critico ? "Crítico!" : desastre ? "Desastre" : m.sucesso ? "Sucesso" : "Falha";
  historico("h-chip", `▸ ${m.atributo} ${m.total} contra ${m.cd} — ${m.sucesso ? "sucesso" : "falha"} (d20 ${m.d20})`);
  if (!replay) Som.tocar(critico ? "critico" : m.sucesso ? "sucesso" : "falha");
  if (!instantaneo()) await espera(500);
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
  pre.innerHTML = m.linhas.map((linha) => linha.map(([t, cor]) => {
    if (!cor) return esc(t);
    const classes = cor.split("+").map((c) => "c-" + c).join(" ");
    return `<span class="${classes}">${esc(t)}</span>`;
  }).join("")).join("\n");
  anexar(pre);
}

function eco(m) {
  anexar(el("p", "eco", esc(m.texto)));
  historico("h-eco", "› " + m.texto);
}

function historico(classe, texto) {
  const p = el("p", classe);
  p.textContent = texto;
  histLista.appendChild(p);
  while (histLista.childElementCount > 4000) histLista.firstElementChild.remove();
}

function mostrarDica() {
  if (replay || velocidade === "instantaneo" || promptEl.childElementCount) return;
  const vistas = Number(ler("cdf-dica") || 0);
  if (vistas > 25) return;
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

const SISTEMA = [
  [/^Talentos/, "Talentos", "t"], [/^Personagem e inventário/, "Personagem", "p"], [/^Comitiva/, "Comitiva", "c"],
  [/^Mapa$/, "Mapa", ""],
  [/^Diário/, "Diário", "d"], [/^Bestiário/, "Bestiário", "b"], [/^Salvar jogo/, "Salvar", "g"], [/^Sair do jogo/, "Sair", "q"],
];
function atalhoDe(texto) { return SISTEMA.find(([re]) => re.test(texto)); }

function mostrarOpcoes(m) {
  promptEl.innerHTML = "";
  if (m.pergunta) promptEl.appendChild(el("div", "pergunta-rotulo", esc(m.pergunta)));
  const lista = el("ol", "escolhas");
  // Nos menus principais, as opções "de sistema" viram atalhos compactos: a história fica em primeiro plano.
  const sistema = m.opcoes.filter((o) => atalhoDe(o.texto)).length >= 4;
  const numeros = [], letras = {};
  const atalhos = el("div", "atalhos");
  m.opcoes.forEach((o, i) => {
    const at = sistema && atalhoDe(o.texto);
    if (at) {
      const pontos = /★\s*(\d+)/.exec(o.texto);
      const carta = /✉/.test(o.texto);
      const qtd = /^Comitiva \((\d+)\)/.exec(o.texto);
      const b = el("button", "atalho" + (pontos || carta ? " destaque" : ""));
      b.type = "button";
      b.innerHTML = esc(at[1]) + (qtd ? ` ${qtd[1]}` : "") + (pontos ? ` <b>★${pontos[1]}</b>` : "") + (carta ? " <b>✉</b>" : "") +
        (at[2] ? `<kbd>${at[2].toUpperCase()}</kbd>` : "");
      b.title = o.texto;
      b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
      atalhos.appendChild(b);
      if (at[2]) letras[at[2]] = i;
      return;
    }
    numeros.push(i);
    const li = el("li");
    const b = el("button", "escolha");
    b.type = "button";
    b.style.animationDelay = `${replay ? 0 : i * 45}ms`;
    if (/^(Voltar|Sair|Cancelar|Nada|Ignorar)/.test(o.texto)) b.classList.add("secundaria");
    const pos = numeros.length - 1;
    const tecla = pos < 9 ? String(pos + 1) : pos === 9 ? "0" : "";
    let teste = "";
    if (o.teste) {
      const nivel = o.teste.mod >= 4 ? "bom" : o.teste.mod >= 1 ? "medio" : "ruim";
      const sinal = o.teste.mod >= 0 ? "+" : "−";
      teste = `<span class="teste ${nivel}" title="Teste de ${esc(o.teste.atributo)}: você rola um d20 e soma ${sinal}${Math.abs(o.teste.mod)} contra uma dificuldade que só o mundo conhece.">${SIGLA[o.teste.atributo] || esc(o.teste.atributo)} ${sinal}${Math.abs(o.teste.mod)}</span>`;
    }
    b.innerHTML = `<span class="tecla">${tecla}</span><span class="rotulo">${esc(o.texto)}</span>${teste}`;
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, i); });
    li.appendChild(b);
    lista.appendChild(li);
  });
  promptEl.appendChild(lista);
  if (atalhos.childElementCount) promptEl.appendChild(atalhos);
  pergunta = { id: m.id, tipo: "opcoes", n: m.opcoes.length, numeros, letras };
  if (!replay) guardar("cdf-dica", String(Number(ler("cdf-dica") || 0) + 1));
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
  input.addEventListener("keydown", (ev) => {
    if (ev.key === "Enter") { ev.preventDefault(); responder(m.id, input.value || m.padrao || ""); }
  });
  const ok = el("button", "continuar", "Confirmar <span>▸</span>");
  ok.addEventListener("click", (ev) => { ev.stopPropagation(); responder(m.id, input.value || m.padrao || ""); });
  linha.append(input, ok);
  promptEl.appendChild(linha);
  pergunta = { id: m.id, tipo: "pergunta" };
  setTimeout(() => input.focus(), 50);
  rolarFim();
}

/* ------------------------------------------------------------------ estado e painéis */
function pct(a, b) { return b ? Math.max(0, Math.min(100, (100 * a) / b)) : 0; }
function barra(classe, atual, maximo, anterior) {
  const de = anterior === undefined ? pct(atual, maximo) : pct(anterior, maximo);
  return `<span class="barra ${classe}" data-alvo="${pct(atual, maximo)}"><span class="rastro" style="width:${de}%"></span><span class="enchimento" style="width:${de}%"></span></span>`;
}
function animarBarras(raiz) {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    raiz.querySelectorAll(".barra[data-alvo]").forEach((b) => {
      b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = b.dataset.alvo + "%"; });
    });
  }));
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

  $("#tempo").textContent = `Dia ${e.mundo.dia} · ${e.mundo.periodo} · ${e.mundo.clima}`;
  $("#corrupcao-topo .enchimento").style.width = e.mundo.corrupcao + "%";
  $("#corrupcao-topo .valor").textContent = e.mundo.corrupcao + "%";
  $("#sigilos-topo").innerHTML = [0, 1, 2].map((i) => i < e.heroi.sigilos ? '<span class="tem">◆</span>' : "◇").join("");

  desenharHeroi(e.heroi);
  desenharCondicao(e.heroi, antes && antes.heroi);
  desenharMundo(e);
  desenharCombate(e.combate, antes && antes.combate);
  if (!$("#sobre-mapa").hidden) desenharMapaGrande();

  if (antes && !replay && e.heroi.hp < antes.heroi.hp) { doer(); Som.tocar("dor"); }
}

function desenharCondicao(h, antes) {
  const recurso = (h.recurso || "").toLowerCase();
  const orbe = (classe, rotulo, atual, maximo) => `
    <div class="orbe ${classe}${classe === "vida" && atual <= maximo * 0.35 ? " critico" : ""}">
      <div class="orbe-globo"><div class="orbe-liquido" style="height:${pct(atual, maximo)}%"></div><div class="orbe-brilho"></div></div>
      <div><div class="orbe-rotulo">${esc(rotulo)}</div><div class="orbe-valor">${atual}<small> / ${maximo}</small></div></div>
    </div>`;
  const itens = [];
  const sup = (rotulo, valor, alerta) => itens.push(`<span class="item${alerta ? " alerta" : ""}">${rotulo} <b>${valor}</b></span>`);
  sup("Comida", `${h.provisoes}d`, h.provisoes <= 1);
  sup("Tochas", h.tochas, h.tochas === 0);
  sup("Poções", h.pocoes, false);
  if (h.flechas !== null && h.flechas !== undefined) sup("Flechas", h.flechas, h.flechas <= 5);
  sup("Ouro", h.ouro, false);
  if (h.companheiro) sup(esc(h.companheiro.nome), `${h.companheiro.hp}/${h.companheiro.max_hp}`, h.companheiro.hp < h.companheiro.max_hp * 0.3);
  const males = h.males.length ? `<div class="males">⚠ ${h.males.map(esc).join(" · ")}</div>` : "";
  $("#condicao").innerHTML = orbe("vida", "Vida", h.hp, h.max_hp) +
    `<div class="suprimentos">${itens.join("")}${males}</div>` +
    orbe(`recurso direita ${recurso}`, h.recurso, h.rec, h.max_rec);
}

function desenharHeroi(h) {
  const attrs = Object.entries(h.atributos).map(([k, v]) =>
    `<div class="atributo"><div class="nome">${esc(k)}</div><div class="valor">${v}</div></div>`).join("");
  const slots = { arma: "Arma", armadura: "Armadura", amuleto: "Amuleto" };
  const equip = Object.entries(slots).map(([k, nome]) => {
    const it = h.equip[k];
    if (!it) return `<div class="slot"><div class="slot-tipo">${nome}</div><div class="vazio">vazio</div></div>`;
    return `<div class="slot"><div class="slot-tipo">${nome}</div><div class="slot-nome r-${esc(it.raridade)}">${esc(it.nome)}</div>` +
      (it.bonus ? `<div class="slot-bonus">${esc(it.bonus)}</div>` : "") + `</div>`;
  }).join("");
  const feridas = h.ferimentos.length ? h.ferimentos.map((f) =>
    `<div class="ferimento">${esc(f.nome)} <small>${f.dias ? f.dias + " dia(s)" : ""}${f.aberto ? " · aberto" : ""}</small></div>`).join("")
    : '<div class="vazio">nenhum, por enquanto</div>';
  const habs = h.habilidades.map((x) => `<div class="habilidade" title="${esc(x.desc)}"><span>${esc(x.nome)}</span><small>${x.custo} ${esc(h.recurso)}</small></div>`).join("");
  const bolsa = h.bolsa.length ? h.bolsa.map((b) => `<div class="linha" title="${esc(b.desc)}"><span>${esc(b.nome)}</span><b>×${b.qtd}</b></div>`).join("")
    : '<div class="vazio">vazia</div>';
  const comitivaHtml = h.comitiva && h.comitiva.length ? `<div class="secao"><h3>Comitiva</h3>${h.comitiva.map((m) => {
    const pos = (m.aprovacao + 100) / 2;
    return `<div class="membro${m.ferido ? " ferido" : ""}" title="${esc(m.titulo)} · aprovação ${m.aprovacao > 0 ? "+" : ""}${m.aprovacao}">
      <div class="membro-topo"><span class="membro-nome">${esc(m.nome)}</span>${m.conversa ? '<span class="membro-carta" title="Quer conversar">✉</span>' : ""}</div>
      <div class="membro-sub">${esc(m.titulo)}${m.ferido ? " · fora de combate até descansar" : ""}</div>
      ${barra("aliado fina", m.hp, m.max_hp)}
      <div class="aprovacao ${m.classe}"><span class="trilho"><span class="marca" style="left:${pos}%"></span></span><span class="rotulo">${esc(m.nivel)}</span></div>
    </div>`;
  }).join("")}</div>` : "";
  const mochila = h.mochila.length ? `<div class="secao"><h3>Mochila ${h.mochila.length}/8</h3>${h.mochila.map((it) =>
    `<div class="slot"><div class="slot-nome r-${esc(it.raridade)}">${esc(it.nome)}</div><div class="slot-bonus">${esc(it.bonus)}</div></div>`).join("")}</div>` : "";
  $("#heroi").innerHTML = `
    <div class="identidade">
      <div class="brasao"><svg viewBox="0 0 32 32">${BRASAO[h.classe] || ""}</svg></div>
      <div><div class="heroi-nome">${esc(h.nome)}</div><div class="heroi-titulo">${esc(h.titulo)} · nível ${h.nivel}</div></div>
    </div>
    <div class="xp-linha"><div class="legenda"><span>Experiência</span><span>${h.xp} / ${h.xp_proximo}</span></div>${barra("xp fina", h.xp, h.xp_proximo)}</div>
    ${h.pontos_talento ? `<div class="talento-aviso">★ ${h.pontos_talento} ponto(s) de talento</div>` : ""}
    <div class="secao"><h3>Atributos</h3><div class="atributos">${attrs}</div></div>
    <div class="secao"><div class="linhas">
      <div class="linha"><span>Ouro</span><b>${h.ouro}</b></div>
      <div class="linha"><span>Reputação</span><b>${h.reputacao > 0 ? "+" : ""}${h.reputacao}</b></div>
    </div></div>
    ${comitivaHtml}
    <div class="secao"><h3>Ferimentos</h3>${feridas}</div>
    <div class="secao"><h3>Equipamento</h3>${equip}</div>
    <div class="secao"><h3>Habilidades</h3>${habs}</div>
    <div class="secao"><h3>Bolsa</h3><div class="linhas">${bolsa}</div></div>
    ${mochila}`;
  animarBarras($("#heroi"));
}

function nivelPerigo(nivel) {
  if (nivel === null || nivel === undefined || !estado) return "";
  const d = nivel - estado.heroi.nivel;
  return d >= 2 ? "alto" : d >= 0 ? "medio" : "baixo";
}
function glifoNo(n) {
  if (n.covil === "ativo") return "☠";
  if (n.covil === "vencido") return "✓";
  if (n.tipo === "vila") return GLIFO.vila;
  return GLIFO[n.bioma] || "•";
}

function svgMapa(mapa, grande) {
  const W = 100, H = 50;
  const pos = {};
  mapa.nos.forEach((n) => { pos[n.id] = [n.x * W, n.y * H]; });
  // Enquadra só o que você conhece: o mapa "cresce" conforme você explora.
  let vb = [-6, -5, 112, 64];
  if (mapa.nos.length) {
    const xs = mapa.nos.map((n) => pos[n.id][0]), ys = mapa.nos.map((n) => pos[n.id][1]);
    const minW = grande ? 84 : 56, minH = grande ? 48 : 32;
    let w = Math.max(Math.max(...xs) - Math.min(...xs) + 22, minW), h = Math.max(Math.max(...ys) - Math.min(...ys) + 20, minH);
    if (w / h > 1.75) h = w / 1.75; else w = h * 1.75;
    const cx = (Math.max(...xs) + Math.min(...xs)) / 2, cy = (Math.max(...ys) + Math.min(...ys)) / 2;
    vb = [cx - w / 2, cy - h / 2, w, h];
  }
  const escala = vb[2] / 112;
  const r = (grande ? 2.6 : 3.3) * escala, fg = (grande ? 2.8 : 3.7) * escala;
  const estradas = mapa.estradas.map((e) => {
    const [x1, y1] = pos[e.a], [x2, y2] = pos[e.b];
    const classe = e.atual ? "estrada atual" : e.percorrida ? "estrada percorrida" : "estrada";
    return `<line class="${classe}" x1="${x1.toFixed(2)}" y1="${y1.toFixed(2)}" x2="${x2.toFixed(2)}" y2="${y2.toFixed(2)}"/>`;
  }).join("");
  const nos = mapa.nos.map((n) => {
    const [x, y] = pos[n.id];
    const classes = ["no"];
    if (n.visitado) classes.push("visitado");
    if (n.atual) classes.push("atual");
    if (n.distancia) classes.push("vizinho");
    if (n.covil === "ativo") classes.push("covil-ativo");
    const gClasse = n.covil ? "" : ` g-${n.tipo === "vila" ? "vila" : n.bioma}`;
    const mostrarRotulo = grande || n.atual;
    const nv = n.nivel ? ` · Nv.${n.nivel}` : "";
    const fr = (grande ? 2.2 : 3.6) * escala;
    const estilo = ` style="font-size:${fr.toFixed(2)}px;stroke-width:${(fr / 4).toFixed(2)}px"`;
    const rotulo = mostrarRotulo ? `<text class="rotulo"${estilo} x="${x.toFixed(2)}" y="${(y + r + fr * 0.95).toFixed(2)}">${esc(n.nome)}${grande ? esc(nv) : ""}</text>` : "";
    const titulo = `${n.nome} — ${n.descricao}${nv}${n.distancia ? ` · ${n.distancia} trecho(s) daqui` : ""}`;
    return `<g class="${classes.join(" ")}"><title>${esc(titulo)}</title>` +
      (n.atual ? `<circle class="anel" cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${(r + 0.2).toFixed(2)}"/>` : "") +
      `<circle class="base" cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${r.toFixed(2)}" style="stroke-width:${(0.4 * escala).toFixed(2)}px"/>` +
      `<text class="glifo${gClasse}" x="${x.toFixed(2)}" y="${(y + 0.15).toFixed(2)}" style="font-size:${fg.toFixed(2)}px">${glifoNo(n)}</text>${rotulo}</g>`;
  }).join("");
  return `<svg class="mapa-svg ${grande ? "grande" : "mini"}" viewBox="${vb.map((v) => v.toFixed(2)).join(" ")}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Mapa do reino">${estradas}${nos}</svg>`;
}

function desenharMundo(e) {
  const l = e.local;
  const perigo = nivelPerigo(l.nivel);
  const caminhos = e.mapa.nos.filter((n) => n.distancia).sort((a, b) => a.distancia - b.distancia || a.nome.localeCompare(b.nome))
    .map((n) => {
      const nv = n.nivel ? ` <span class="perigo-tag ${nivelPerigo(n.nivel)}">Nv.${n.nivel}</span>` : "";
      return `<div class="caminho"><span class="glifo">${glifoNo(n)}</span><span class="nome">${esc(n.nome)}${nv}<br><small>${esc(n.descricao)}</small></span>` +
        `<span class="dist">${n.distancia} trecho${n.distancia > 1 ? "s" : ""}</span></div>`;
    }).join("");
  $("#mundo").innerHTML = `
    <div class="local-nome">${esc(l.nome)}</div>
    <div class="local-desc">${esc(l.descricao)}</div>
    ${l.nivel ? `<span class="perigo-tag ${perigo}">inimigos Nv.${l.nivel}</span>` : ""}
    <div class="mapa-mini" title="Abrir o mapa (M)">${svgMapa(e.mapa, false)}</div>
    <div class="secao"><h3>Caminhos daqui</h3><div class="caminhos">${caminhos || '<div class="vazio">nenhum</div>'}</div></div>`;
  $("#mundo .mapa-mini").addEventListener("click", () => alternarMapa(true));
}

function legendaMapa() {
  return Object.entries(GLIFO).map(([k, g]) => `<span>${g} ${NOME_BIOMA[k]}</span>`).join("") +
    "<span>☠ covil de guardião</span><span>✓ covil vencido</span>" +
    '<span style="color:var(--ouro)">- - - caminhos daqui</span>';
}

function desenharMapaGrande() {
  if (!estado) return;
  $("#mapa-grande").innerHTML = svgMapa(estado.mapa, true);
  $("#mapa-legenda").innerHTML = legendaMapa();
}

function mapaNaPagina(m) {
  if (!estado) return;
  const caixa = el("div", "mapa-pagina");
  caixa.innerHTML = svgMapa(estado.mapa, true) + `<div id="legenda-pagina" class="legenda-pagina">${legendaMapa()}</div>`;
  anexar(caixa);
}

function desenharCombate(cb, antes) {
  const raiz = $("#combate");
  if (!cb) { raiz.innerHTML = ""; return; }
  const anteriores = {};
  if (antes) [...antes.inimigos, ...antes.aliados].forEach((c, i) => { anteriores[c.lado + ":" + c.nome] = c; });
  const carta = (c) => {
    const ant = anteriores[c.lado + ":" + c.nome];
    const dano = ant ? ant.hp - c.hp : 0;
    const classes = ["carta", c.lado];
    if (c.chefe) classes.push("chefe");
    if (c.unico) classes.push("unico");
    if (dano > 0 && !replay) classes.push("atingida");
    const efeitos = c.efeitos.length ? `<div class="carta-efeitos">${c.efeitos.map((f) => `<span class="efeito">${esc(f.nome)} ${f.turnos}</span>`).join("")}</div>` : "";
    const flutuante = dano && !replay ? `<span class="numero-flutuante${dano < 0 ? " cura" : ""}">${dano > 0 ? "−" : "+"}${Math.abs(dano)}</span>` : "";
    return `<div class="${classes.join(" ")}">${flutuante}
      <div class="carta-nome"><span>${esc(c.nome)}</span>${c.nivel ? `<span class="carta-nivel">Nv.${c.nivel}</span>` : ""}</div>
      ${barra(c.lado === "aliado" ? "aliado" : "vida", c.hp, c.max_hp, ant ? ant.hp : undefined)}
      <div class="carta-hp"><span>${c.hp} / ${c.max_hp}</span>${c.chefe ? "<span>guardião</span>" : ""}</div>
      ${c.preparando ? '<div class="preparando">⚠ prepara um golpe devastador</div>' : ""}${efeitos}</div>`;
  };
  raiz.innerHTML = cb.inimigos.map(carta).join("") + cb.aliados.map(carta).join("");
  animarBarras(raiz);
  if (antes && !replay && cb.inimigos.some((c) => { const a = anteriores["inimigo:" + c.nome]; return a && a.hp > c.hp; })) Som.tocar("golpe");
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
    return;
  }
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
  if (processando && !pergunta) {
    if (k.length === 1 || k === "Enter") { ev.preventDefault(); pular = true; }
    return;
  }
  if (!pergunta) return;
  if (pergunta.tipo === "continuar" && (k === " " || k === "Enter")) { ev.preventDefault(); responder(pergunta.id, null); return; }
  if (pergunta.tipo !== "opcoes") return;
  const botoes = [...promptEl.querySelectorAll(".escolha, .atalho")];
  if (/^[0-9]$/.test(k)) {
    const i = k === "0" ? 9 : Number(k) - 1;
    if (i < pergunta.numeros.length) { ev.preventDefault(); responder(pergunta.id, pergunta.numeros[i]); }
    return;
  }
  if (pergunta.letras[k.toLowerCase()] !== undefined) { ev.preventDefault(); responder(pergunta.id, pergunta.letras[k.toLowerCase()]); return; }
  const foco = botoes.indexOf(document.activeElement);
  if (k === "ArrowDown" || k === "ArrowUp") {
    ev.preventDefault();
    const n = botoes.length;
    const prox = foco < 0 ? (k === "ArrowDown" ? 0 : n - 1) : (foco + (k === "ArrowDown" ? 1 : -1) + n) % n;
    botoes[prox].focus();
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
    const s = (1.5 + Math.random() * 2.5).toFixed(1) + "px";
    b.style.width = s; b.style.height = s;
    raiz.appendChild(b);
  }
}

async function iniciar() {
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
