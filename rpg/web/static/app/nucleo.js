/* Crônicas da Fenda — cliente web (tema pixel art).
   Recebe as mensagens do motor (SSE) e as processa em fila: texto com ritmo, dado animado,
   HUD que reage a cada mudança, combate golpe a golpe, mapa clicável e telas visuais. */
"use strict";

const $ = (s, r = document) => r.querySelector(s);
const esc = Texto.html;
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const spr = Telas.S;  // o desenho de um sprite (o mesmo S das telas)
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
// A doca: [id da meta `sistema` que o motor manda, rótulo, tecla, ícone, grupo]. A opção é reconhecida pela meta,
// nunca pelo texto.
const SISTEMA = [
  ["inventario", "Inventário", "i", "saco", 0], ["talentos", "Talentos", "t", "estrela", 0],
  ["comitiva", "Comitiva", "c", "humano", 0], ["mapa", "Mapa", "m", "pergaminho", 1], ["diario", "Diário", "d", "livro", 1],
  ["bestiario", "Bestiário", "b", "caveira", 1], ["salvar", "Salvar", "g", "cadeado", 2], ["sair", "Sair", "q", "fuga", 2],
];

const corpo = document.body;
const cenaEl = $("#cena"), barraTela = $("#barra-tela");
const pagina = $("#pagina"), folha = $("#folha"), cab = $("#cena-cab"), textoEl = $("#texto"), promptEl = $("#prompt");
const histLista = $("#historico-lista");

let velocidade = ler("cdf-velocidade") || "normal";
const fila = [];
let processando = false, pular = false, replay = false;
// Um pedido deliberado de seguir (o Voltar, o Esc, um prédio clicado na paisagem) enquanto a página ainda corre ou
// espera a leitura: adianta como o clique na tela, mas não se perde na guarda de leitura (vira a página quando ela
// acaba).
let pularPedido = false;
function pedirPular() { pular = true; pularPedido = true; }
let estado = null, pergunta = null, pendente = null;
let ultimaResposta = 0;  // quando a última escolha saiu: a leitura do que veio depois começa aí
let capitular = false, seguir = true;
let ultimosRecursos = {};

const App = {
  get estado() { return estado; },
  get ultimoClique() { return ultimoClique; },
  responder: (id, valor) => responder(id, valor),
  pedir: (rotulo, chave, valor) => pedir(rotulo, chave, valor),
  acao: (filtro, som, extra) => acao(filtro, som, extra),
  ultimaLoja: null,
  ultimaFogueira: null,
  opcoes: () => (pergunta && pergunta.tipo === "opcoes" ? pergunta.opcoes : null),
  som: (n) => Som.tocar(n),
  avisar: (texto, chave) => aviso(texto, "info", "pergaminho", typeof chave === "string" ? chave : undefined),
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
  ultimaResposta = performance.now();
  presoNoTopo = false;  // o que a escolha trouxer aparece embaixo, à vista
  fecharConfirmacao();     // a janela de confirmação some com a resposta (botão, tecla, Esc ou clique fora)
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
const ACOES_OCULTAS = ["equipar", "tirar", "usar", "largar", "comprar", "comprar_item", "vender", "recomprar", "aceitar", "abandonar",
  "conversar", "chamar", "reservar", "acampamento", "save", "carinho", "dormir", "reforcar", "tratar"];

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
  pularPedido = false;
}

function instantaneo() { return pular || replay || velocidade === "instantaneo"; }
function cps() { return VELOCIDADES[velocidade] * (estado && estado.combate ? 2.5 : 1); }
function ritmo(ms) { return instantaneo() ? 0 : ms * (velocidade === "lento" ? 1.4 : velocidade === "rapido" ? 0.5 : 1); }

async function tratar(m) {
  switch (m.t) {
    case "estado": aplicarEstado(m.estado); break;
    case "sincronizado": replay = false; break;
    case "nova_cena": await novaCena(m); break;
    case "cabecalho": tituloAtual = m.titulo; cabecalho(m); break;  // a tela que se redesenha depois reconhece o título
    case "texto": await texto(m); break;
    case "efeito": await efeito(m); break;
    case "rolagem": await rolagem(m); break;
    case "combate":
      // Luta nova: nada da anterior (a câmera lenta de um golpe final que não terminou) nem da vila fica na arena.
      Sensacao.repor(); fecharVila();
      cenaInterrompida = true; faixaCombate(m); break;
    case "lance": if (!replay) await Batalha.lance(m); break;
    case "fala": await fala(m); break;
    case "opiniao": await opiniao(m); break;
    case "turno": turno(m); break;
    case "fim_combate": if (!instantaneo()) await espera(m.resultado === "vitoria" ? 800 : 400); break;
    // Celebração não se pula com o clique que adiantava o texto (o contrato pago, o espólio, a vitória): ela tem as
    // próprias teclas e o próprio tempo. Só a velocidade "instantâneo" e o replay a dispensam.
    case "celebrar": { const r = Telas.resumoCelebracao(m); if (r) historico("h-chip", r); await Telas.celebrar(m, replay || velocidade === "instantaneo"); break; }
    case "talentos": Telas.guardarArvore(m.arvore); break;
    case "painel": {
      if (m.tipo === "achado") {
        // O item achado abre numa janela própria, fora do log; o registro guarda só o fato.
        historico("h-chip", `▸ Encontrou: ${m.dados.item.nome}`);
        // Refazendo a página (replay), a janela abre sem cerimônia: a pergunta pode estar esperando; se não estiver,
        // a próxima mensagem (o voo, outra pergunta) a fecha.
        await Telas.abrirAchado(m.dados, replay);
        break;
      }
      if (emMenu()) seguir = false;  // a tela desenhada (inventário, mercado, mural) se lê de cima: a página não desce
      anexar(Telas.painel(m));
      break;
    }
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
