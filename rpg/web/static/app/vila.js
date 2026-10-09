"use strict";

/* ------------------------------------------------------------------ a vila como lugar
   Na vila, os serviços moram nos prédios da paisagem (vista.js desenha e registra cada um; o motor diz, em cada
   opção, a que prédio ela pertence). Cada prédio tem o nome num balão acima dele; passar o mouse acende o balão e as
   luzes do prédio; clicar toca o som dele, a câmera chega perto e o texto mostra só as opções dali, com um "Voltar à
   vila". Prédio sem serviço agora (o templo com a vida cheia) continua clicável e diz por quê (estado.local
   .predios_fechados). O que não é de prédio nenhum (passear) segue em texto. */
const predioEl = $("#predios");
let vilaAberta = null;  // { m, grupos, predio } enquanto a vila está na tela
let predioPedido = null;  // clicado enquanto a página ainda virava: entra assim que a vila se remonta

/** A pergunta é o menu da vila? (o lugar é uma vila, a cena é a do lugar, e há opções de prédio) */
function ehMenuDaVila(m) {
  return !!(estado && !estado.combate && estado.local.tipo === "vila" && cenaEl.dataset.tipo === "local"
    && m.opcoes.some((o) => o.meta && o.meta.predio) && Vista.predios().length);
}

function fecharVila() {
  vilaAberta = null;
  predioPedido = null;
  predioEl.innerHTML = "";
  predioEl.hidden = true;
  cenaEl.classList.remove("vila-hub");
  Vista.destacar(null);
}

/** Onde cada prédio cai na tela: a arte é desenhada com object-fit: cover (centro, 80% para baixo). */
function posicionarPredios() {
  if (!vilaAberta) return;
  const vista = $("#vista"), cs = getComputedStyle(vista);
  const larg = vista.clientWidth, alt = vista.clientHeight - parseFloat(cs.paddingBottom);
  const esc = Math.max(larg / Vista.LARGURA, alt / Vista.ALTURA);
  const dx = (larg - Vista.LARGURA * esc) * 0.5, dy = (alt - Vista.ALTURA * esc) * 0.8;
  predioEl.style.left = vista.offsetLeft + "px"; predioEl.style.top = vista.offsetTop + "px";
  predioEl.style.width = larg + "px"; predioEl.style.height = alt + "px";
  predioEl.querySelectorAll(".predio").forEach((b) => {
    const p = Vista.predios().find((x) => x.id === b.dataset.predio);
    if (!p) return;
    Object.assign(b.style, { left: dx + p.x * esc + "px", top: dy + p.y * esc + "px", width: p.w * esc + "px", height: p.h * esc + "px" });
    // o bico do balão aponta para o telhado (pixel inteiro da tela, para o balão não ficar borrado)
    const [bx, by] = p.balao || [p.x + p.w / 2, p.y];
    Object.assign(b.querySelector(".balao-nome").style, { left: Math.round((bx - p.x) * esc) + "px", top: Math.round((by - p.y) * esc) + "px" });
  });
}
window.addEventListener("resize", posicionarPredios);

/** Monta a vila: os prédios com opção (ou com um porquê de estarem sem serviço) viram botões com balão; os outros
 *  ficam só de cenário. */
function montarVila(m, grupos) {
  vilaAberta = { m, grupos, predio: null };
  cenaEl.classList.add("vila-hub");
  predioEl.hidden = false;
  predioEl.classList.remove("focado");
  predioEl.innerHTML = "";
  Vista.focar(null);
  const fechados = (estado && estado.local.predios_fechados) || {};
  Vista.predios().forEach((p) => {
    const g = grupos[p.id];
    if (!g && !fechados[p.id]) return;
    const b = el("button", "predio", `<span class="balao-nome">${esc(p.nome)}</span>`);
    b.type = "button";
    b.dataset.predio = p.id;
    b.title = g ? g.map(({ o }) => o.texto).join(" · ") : fechados[p.id];
    b.setAttribute("aria-label", p.nome);
    b.addEventListener("mouseenter", () => Vista.destacar(p.id));
    b.addEventListener("mouseleave", () => Vista.destacar(null));
    b.addEventListener("focus", () => Vista.destacar(p.id));
    b.addEventListener("blur", () => Vista.destacar(null));
    b.addEventListener("click", (ev) => { ev.stopPropagation(); entrarNoPredio(p.id); });
    predioEl.appendChild(b);
  });
  requestAnimationFrame(posicionarPredios);
  $("#vista").addEventListener("transitionend", posicionarPredios, { once: true });
  const pedido = predioPedido;
  predioPedido = null;
  if (pedido && predioEl.querySelector(`[data-predio="${pedido}"]`)) entrarNoPredio(pedido, true);
}

/** Clicou num prédio: o som dele e a câmera chegando perto. Uma opção só, sem nada a confirmar (o mercado, o mural, a
 *  forja, a estrada): vai direto. Mais de uma, ou que custa (a taverna, o templo): o texto mostra as opções de lá.
 *  Sem serviço agora: o porquê, e o Voltar. */
function entrarNoPredio(id, pedido = false) {
  const v = vilaAberta;
  if (!v) return;
  // Com o texto ainda correndo (a página do que aconteceu esperando para virar), o clique adianta e fica guardado.
  if (processando && !pedido) { predioPedido = id; pular = true; return; }
  const g = v.grupos[id] || [];
  Som.tocar("predio_" + id);
  Vista.focar(id);
  predioEl.classList.add("focado");  // com a câmera perto, os balões da vila inteira saem na hora
  Vista.destacar(null);
  if (g.length === 1 && !g[0].o.meta.curto) { responder(v.m.id, g[0].i); return; }
  v.predio = id;
  const nome = (Vista.predios().find((p) => p.id === id) || {}).nome || "";
  promptEl.innerHTML = "";
  promptEl.appendChild(el("div", "pergunta-rotulo", esc(nome)));
  const motivo = !g.length && ((estado && estado.local.predios_fechados) || {})[id];
  if (motivo) promptEl.appendChild(el("p", "predio-fechado", esc(motivo)));
  const lista = el("ol", "escolhas");
  pergunta = { id: v.m.id, tipo: "opcoes", n: v.m.opcoes.length, opcoes: v.m.opcoes, numeros: [], letras: {}, voltar: -1, voltarLocal: sairDoPredio };
  g.forEach(({ o, i }) => {
    pergunta.numeros.push(i);
    const pos = pergunta.numeros.length;
    const tempo = o.meta.tempo ? `<span class="tempo-acao">⧗ ${esc(o.meta.tempo)}</span>` : "";
    const b = el("button", "escolha", `<span class="tecla">${pos}</span><span class="rotulo">${esc(o.meta.curto || o.texto)}</span>${tempo}`);
    b.type = "button";
    b.addEventListener("click", (ev) => { ev.stopPropagation(); responder(v.m.id, i); });
    const li = el("li"); li.appendChild(b); lista.appendChild(li);
  });
  const li = el("li");
  const volta = el("button", "escolha secundaria voltar-vila", `<span class="rotulo">◀ Voltar à vila</span>`);
  volta.type = "button";
  volta.addEventListener("click", (ev) => { ev.stopPropagation(); sairDoPredio(); });
  li.appendChild(volta); lista.appendChild(li);
  promptEl.appendChild(lista);
  pagina.scrollTop = pagina.scrollHeight;
}

/** Voltar à vila: a câmera se afasta e o texto volta a ser o do lugar. */
function sairDoPredio() {
  const v = vilaAberta;
  if (!v) return;
  Som.tocar("escolha");
  mostrarOpcoes(v.m);
}
