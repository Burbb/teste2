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

/* Diante de um prédio: o balcão (o ícone, quem atende e o que diz) e um cartão por serviço, com preço e tempo. */
const BALCOES = {
  taverna: ["pernil", "A taverna", "Fumaça, palha no chão e conversa baixa. O taverneiro nem levanta os olhos."],
  templo: ["lanterna", "O templo", "Velas, incenso e um clérigo cansado, de mãos firmes."],
  curandeiro: ["unguento", "A curandeira", ""],
};
const ICONE_SERVICO = { dormir: "lua", rumores: "pergaminho", templo: "coracao" };

/** Clicou num prédio: o som dele e a câmera chegando perto. Uma opção só, sem nada a escolher ali (o mercado, o mural,
 *  a forja, a curandeira, a estrada): vai direto para a tela dele. A taverna e o templo mostram o balcão com os
 *  serviços em cartões; sem serviço agora, o balcão diz por quê. Embaixo, o Voltar à vila (também no Esc). */
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
  const [icone, quem, fala] = BALCOES[id] || ["estrela", nome, ""];
  const motivo = !g.length && ((estado && estado.local.predios_fechados) || {})[id];
  const ouro = estado ? estado.heroi.ouro : 0;
  promptEl.innerHTML = "";
  const caixa = el("div", "tela balcao-predio");
  caixa.innerHTML = Telas.topoBalcao(icone, quem, motivo || fala, ouro) + (g.length ? `<div class="servicos">${g.map(({ o, i }) => Telas.cartaoServico({
    icone: ICONE_SERVICO[o.meta.servico] || icone, nome: o.meta.curto || o.texto, efeito: o.meta.efeito, preco: o.meta.preco,
    tempo: o.meta.tempo, motivo: o.meta.preco > ouro ? "Ouro insuficiente." : "", attrs: `data-i="${i}"`,
  })).join("")}</div>` : "");
  caixa.querySelectorAll(".servico").forEach((b) => b.addEventListener("click", (ev) => {
    ev.stopPropagation();
    if (b.classList.contains("caro")) { Som.tocar("falha"); return; }
    responder(v.m.id, Number(b.dataset.i));
  }));
  const volta = el("button", "escolha secundaria voltar-vila", `<span class="rotulo">◀ Voltar à vila</span>`);
  volta.type = "button";
  volta.addEventListener("click", (ev) => { ev.stopPropagation(); sairDoPredio(); });
  caixa.appendChild(volta);
  promptEl.appendChild(caixa);
  // As teclas 1, 2... escolhem os cartões, na ordem; Esc volta à vila.
  pergunta = { id: v.m.id, tipo: "opcoes", n: v.m.opcoes.length, opcoes: v.m.opcoes, numeros: g.map(({ i }) => i), letras: {}, voltar: -1, voltarLocal: sairDoPredio };
  // o balcão inteiro à vista: o topo dele no alto da página, se ele não couber embaixo do texto
  const sobra = caixa.getBoundingClientRect().bottom - pagina.getBoundingClientRect().bottom + 12;
  if (sobra > 0) pagina.scrollTop += Math.min(sobra, caixa.getBoundingClientRect().top - pagina.getBoundingClientRect().top - 8);
}

/** Voltar à vila: a câmera se afasta e o texto volta a ser o do lugar. */
function sairDoPredio() {
  const v = vilaAberta;
  if (!v) return;
  Som.tocar("escolha");
  mostrarOpcoes(v.m);
}
