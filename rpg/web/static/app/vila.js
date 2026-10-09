"use strict";

/* ------------------------------------------------------------------ a vila como lugar
   Na vila, os serviços moram nos prédios da paisagem (vista.js desenha e registra cada um; o motor diz, em cada
   opção, a que prédio ela pertence). Passar o mouse acende o prédio; clicar toca o som dele, a câmera chega perto e o
   texto mostra só as opções dali, com um "Voltar à vila". O que não é de prédio nenhum (passear) segue em texto. */
const predioEl = $("#predios");
let vilaAberta = null;  // { m, grupos, predio } enquanto a vila está na tela

/** A pergunta é o menu da vila? (o lugar é uma vila, a cena é a do lugar, e há opções de prédio) */
function ehMenuDaVila(m) {
  return !!(estado && !estado.combate && estado.local.tipo === "vila" && cenaEl.dataset.tipo === "local"
    && m.opcoes.some((o) => o.meta && o.meta.predio) && Vista.predios().length);
}

function fecharVila() {
  vilaAberta = null;
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
  });
}
window.addEventListener("resize", posicionarPredios);

/** Monta a vila: os prédios com opção viram botões (com plaquinha); os outros ficam só de cenário. */
function montarVila(m, grupos) {
  vilaAberta = { m, grupos, predio: null };
  cenaEl.classList.add("vila-hub");
  predioEl.hidden = false;
  predioEl.classList.remove("focado");
  predioEl.innerHTML = "";
  Vista.focar(null);
  Vista.predios().forEach((p) => {
    const g = grupos[p.id];
    if (!g) return;
    const b = el("button", "predio", `<span class="placa-nome">${esc(p.nome)}</span>`);
    b.type = "button";
    b.dataset.predio = p.id;
    b.title = g.map(({ o }) => o.texto).join(" · ");
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
}

/** Clicou num prédio: o som dele e a câmera chegando perto. Uma opção só, sem nada a confirmar (o mercado, o mural, a
 *  forja, a estrada): vai direto. Mais de uma, ou que custa (a taverna, o templo): o texto mostra as opções de lá. */
function entrarNoPredio(id) {
  const v = vilaAberta;
  if (!v || processando) return;
  const g = v.grupos[id];
  Som.tocar("predio_" + id);
  Vista.focar(id);
  if (g.length === 1 && !g[0].o.meta.curto) { responder(v.m.id, g[0].i); return; }
  v.predio = id;
  predioEl.classList.add("focado");  // com a câmera perto, as plaquinhas da vila inteira saem
  const nome = (Vista.predios().find((p) => p.id === id) || {}).nome || "";
  promptEl.innerHTML = "";
  promptEl.appendChild(el("div", "pergunta-rotulo", esc(nome)));
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
