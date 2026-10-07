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
// [padrão, rótulo, tecla, ícone, grupo]: personagem · mundo · sistema
const SISTEMA = [
  [/^Personagem e inventário/, "Inventário", "i", "saco", 0], [/^Talentos/, "Talentos", "t", "estrela", 0],
  [/^Comitiva/, "Comitiva", "c", "humano", 0], [/^Mapa$/, "Mapa", "m", "pergaminho", 1], [/^Diário/, "Diário", "d", "livro", 1],
  [/^Bestiário/, "Bestiário", "b", "caveira", 1], [/^Salvar jogo/, "Salvar", "g", "cadeado", 2], [/^Sair do jogo/, "Sair", "q", "fuga", 2],
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
  acao: (filtro, som, extra) => acao(filtro, som, extra),
  ultimaLoja: null,
  ultimaFogueira: null,
  opcoes: () => (pergunta && pergunta.tipo === "opcoes" ? pergunta.opcoes : null),
  som: (n) => Som.tocar(n),
  avisar: (texto) => aviso(texto, "info", "pergaminho"),
  doer: () => doer(),
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
  Telas.fecharMenuItem();  // um menu de figura aberto não sobrevive à escolha (inclusive Voltar)
  Telas.esconderDica();  // nem a dica de um item que estava sob o mouse
  // O que já está na página foi lido: se a mesma tela se redesenhar, só o que vier depois vira aviso.
  textoEl.querySelectorAll(":scope > p").forEach((p) => p.classList.add("lido"));
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

/** Responde à opção cujos metadados batem com o filtro (ações de arrastar, comprar, usar...). */
function acao(filtro, som, extra) {
  if (!pergunta || pergunta.tipo !== "opcoes" || !pergunta.opcoes) return false;
  const i = pergunta.opcoes.findIndex((o) => o.meta && Object.entries(filtro).every(([k, v]) => o.meta[k] === v));
  if (i < 0) return false;
  Telas.esconderDica();
  if (som) Som.tocar(som);
  responder(pergunta.id, extra ? { i, ...extra } : i);  // extra: dados que vão junto (ex.: quantidade)
  return true;
}
const ACOES_OCULTAS = ["equipar", "tirar", "usar", "largar", "comprar", "comprar_item", "vender", "aceitar", "abandonar",
  "conversar", "chamar", "reservar", "acampamento", "save"];

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
    case "lance": if (!replay) await Batalha.lance(m); break;
    case "fala": await fala(m); break;
    case "opiniao": await opiniao(m); break;
    case "turno": turno(m); break;
    case "fim_combate": if (!instantaneo()) await espera(m.resultado === "vitoria" ? 800 : 400); break;
    case "celebrar": await Telas.celebrar(m, instantaneo()); break;
    case "talentos": Telas.guardarArvore(m.arvore); break;
    case "painel": anexar(Telas.painel(m)); break;
    case "subtitulo": anexar(el("div", "subtitulo", esc(suavizar(m.texto)))); break;
    case "separador": anexar(el("hr")); break;
    case "bloco": bloco(m); break;
    case "mapa": mapaNaPagina(m); break;
    case "escolhido": eco(m); break;
    case "opcoes": mostrarOpcoes(m); soltarRolagem(); break;
    case "continuar": mostrarContinuar(m); soltarRolagem(); break;
    case "pergunta": mostrarPergunta(m); soltarRolagem(); break;
    case "erro": anexar(el("p", "erro", "Algo deu errado: " + esc(m.texto))); break;
    case "fim": $("#aviso-fim").hidden = false; break;
  }
}
