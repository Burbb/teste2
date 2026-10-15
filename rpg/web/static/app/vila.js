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
const MURAL_VISTO = "cdf-mural-visto";  // o mural já foi aberto uma vez: o convite dele não pisca mais

/** A pergunta é o menu da vila? (o lugar é uma vila, a cena é a do lugar, e há opções de prédio) */
function ehMenuDaVila(m) {
  return !!(estado && !estado.combate && estado.local.tipo === "vila" && cenaEl.dataset.tipo === "local"
    && m.opcoes.some((o) => o.meta && (o.meta.predio || o.meta.balcao)) && Vista.predios().length);
}

function fecharVila() {
  vilaAberta = null;
  predioPedido = null;
  predioEl.innerHTML = "";
  predioEl.hidden = true;
  cenaEl.classList.remove("vila-hub");
  Vista.destacar(null);
}

/** Onde cada prédio cai na tela: a caixa da arte (Vista.caixaDaArte, a mesma conta do desenho), aplicada à
 *  camada inteira, a cada botão (a área clicável e o contorno), ao balão e à ponta dele. Refeito a cada mudança de
 *  tamanho da vista, inclusive durante a animação da altura (Vista.aoRedimensionar): com uma conta só no evento
 *  "resize" da janela, a altura ainda era a de antes e os balões ficavam no lugar do tamanho anterior. */
function posicionarPredios() {
  if (!vilaAberta) return;
  const q = Vista.caixaDaArte();
  if (!q) return;
  Object.assign(predioEl.style, { left: q.esq + "px", top: q.topo + "px", width: q.larg + "px", height: q.alt + "px" });
  predioEl.querySelectorAll(".predio").forEach((b) => {
    const p = Vista.predios().find((x) => x.id === b.dataset.predio);
    if (!p) return;
    Object.assign(b.style, { left: q.dx + p.x * q.ex + "px", top: q.dy + p.y * q.ey + "px", width: p.w * q.ex + "px", height: p.h * q.ey + "px" });
    // o bico do balão aponta para o telhado (pixel inteiro da tela, para o balão não ficar borrado)
    const [bx, by] = p.balao || [p.x + p.w / 2, p.y];
    Object.assign(b.querySelector(".balao-nome").style, { left: Math.round((bx - p.x) * q.ex) + "px", top: Math.round((by - p.y) * q.ey) + "px" });
  });
}
Vista.aoRedimensionar(posicionarPredios);

/** O prédio da vila sob um ponto da tela (ou null): a mesma conta de posicionarPredios, ao contrário. */
function predioNoPonto(x, y) {
  if (!estado || estado.combate || estado.local.tipo !== "vila") return null;
  const q = Vista.caixaDaArte();
  if (!q) return null;
  const r = $("#cena").getBoundingClientRect(), c = $("#cena");
  const ax = (x - r.left - c.clientLeft - q.esq - q.dx) / q.ex, ay = (y - r.top - c.clientTop - q.topo - q.dy) / q.ey;
  const p = Vista.predios().find((k) => ax >= k.x && ax < k.x + k.w && ay >= k.y && ay < k.y + k.h);
  return p ? p.id : null;
}

/** Monta a vila: os prédios com opção (ou com um porquê de estarem sem serviço) viram botões com balão; os outros
 *  ficam só de cenário. */
function montarVila(m, grupos) {
  // O motor manteve um balcão aberto (o templo, depois de cuidar de alguém): a pergunta traz o Voltar dele, com a meta
  // `balcao`. A vila se remonta já diante do prédio, sem afastar e reaproximar a câmera.
  const bi = m.opcoes.findIndex((o) => o.meta && o.meta.balcao);
  const balcao = bi >= 0 ? { id: m.opcoes[bi].meta.balcao, i: bi } : null;
  vilaAberta = { m, grupos, predio: null, balcao };
  cenaEl.classList.add("vila-hub");
  predioEl.hidden = false;
  predioEl.classList.remove("focado");
  predioEl.innerHTML = "";
  Vista.focar(balcao ? balcao.id : null);
  const fechados = (estado && estado.local.predios_fechados) || {};
  Vista.predios().forEach((p) => {
    const g = grupos[p.id];
    if (!g && !fechados[p.id]) return;
    // Quem ainda não abriu o mural (neste navegador): o balão dele pisca como sob o mouse até a primeira visita. Mostra
    // que o cenário se clica e por onde há trabalho a pegar. Com o tutorial ligado, o quadro da orientação (V1,
    // orientacao.js) aponta o Mural no lugar do convite (e, enquanto ele está à vista, o convite não pisca junto).
    const convite = p.id === "mural" && !ler(MURAL_VISTO) && !(estado && estado.orientacao && estado.orientacao.ligado);
    const b = el("button", "predio" + (convite ? " convite" : ""), `<span class="balao-nome">${esc(p.nome)}</span>`);
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
  posicionarPredios();
  const pedido = predioPedido;
  predioPedido = null;
  if (balcao && predioEl.querySelector(`[data-predio="${balcao.id}"]`)) entrarNoPredio(balcao.id, true, true);
  else if (pedido && predioEl.querySelector(`[data-predio="${pedido}"]`)) entrarNoPredio(pedido, true);
}

/* Diante de um prédio: o balcão (o ícone, quem atende e o que diz) e um cartão por serviço, com preço e tempo. */
const BALCOES = {
  taverna: ["pernil", "A taverna", "Fumaça, palha no chão e conversa baixa. O taverneiro nem levanta os olhos."],
  templo: ["lanterna", "O templo", "Velas, incenso e um clérigo cansado, de mãos firmes."],
  curandeiro: ["unguento", "A curandeira", ""],
  ferreiro: ["martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja."],
};
const ICONE_SERVICO = { dormir: "lua", rumores: "pergaminho", templo: "coracao", broquel: "escudo" };

/** Clicou num prédio: o som dele e a câmera chegando perto. Uma opção só, sem nada a escolher ali (o mercado, o mural,
 *  a forja, a curandeira, a estrada): vai direto para a tela dele. A taverna e o templo mostram o balcão com os
 *  serviços em cartões; sem serviço agora, o balcão diz por quê. Embaixo, o Voltar à vila (também no Esc). */
function entrarNoPredio(id, pedido = false, continua = false) {
  const v = vilaAberta;
  if (!v) return;
  // Com o texto ainda correndo (a página do que aconteceu esperando para virar), o clique adianta e fica guardado.
  if (processando && !pedido) { predioPedido = id; pedirPular(); return; }
  // Só o menu da vila responde: se a pergunta da tela já é outra (uma tela da doca abriu, um evento começou), a vila
  // que sobrou na paisagem sai em vez de responder por uma pergunta que o motor não espera mais.
  if (!pergunta || pergunta.id !== v.m.id) { fecharVila(); return; }
  const g = v.grupos[id] || [];
  if (id === "mural" && !ler(MURAL_VISTO)) {
    guardar(MURAL_VISTO, "1");
    predioEl.querySelectorAll(".predio.convite").forEach((b) => b.classList.remove("convite"));
  }
  if (!continua) Som.tocar("predio_" + id);  // de volta ao mesmo balcão (o templo depois de cuidar de alguém): sem o som de entrar
  Vista.focar(id);
  predioEl.classList.add("focado");  // com a câmera perto, os balões da vila inteira saem na hora
  Vista.destacar(null);
  if (g.length === 1 && !g[0].o.meta.curto) { responder(v.m.id, g[0].i); return; }
  v.predio = id;
  const nome = (Vista.predios().find((p) => p.id === id) || {}).nome || "";
  const [icone, quemPadrao, fala] = BALCOES[id] || ["estrela", nome, ""];
  const quem = (estado && estado.local.atendentes && estado.local.atendentes[id]) || quemPadrao;  // o motor diz quem atende
  const motivo = !g.length && ((estado && estado.local.predios_fechados) || {})[id];
  const ouro = estado ? estado.heroi.ouro : 0;
  promptEl.innerHTML = "";
  const caixa = el("div", "tela balcao-predio");
  caixa.innerHTML = Telas.topoBalcao(icone, quem, motivo || fala, ouro) + (g.length ? `<div class="servicos">${g.map(({ o, i }) => Telas.cartaoServico({
    icone: o.meta.alvo || ICONE_SERVICO[o.meta.servico] || icone, nome: o.meta.curto || o.texto, efeito: o.meta.efeito, preco: o.meta.preco,
    tempo: o.meta.tempo, linhas: o.meta.linhas, motivo: o.meta.motivo || "", attrs: `data-i="${i}"${o.meta.servico ? ` data-servico="${o.meta.servico}"` : ""}`,
  })).join("")}</div>` : "");
  caixa.querySelectorAll(".servico").forEach((b) => b.addEventListener("click", (ev) => {
    ev.stopPropagation();
    if (b.classList.contains("caro")) { App.recusar(b, b.dataset.motivo); return; }
    responder(v.m.id, Number(b.dataset.i));
  }));
  const cartoes = [...caixa.querySelectorAll(".servico")];
  // Voltar à vila: com o balcão mantido pelo motor, é a resposta à pergunta dele; senão, só a tela volta para a vila.
  const sair = v.balcao && v.balcao.id === id ? () => { Som.tocar("escolha"); responder(v.m.id, v.balcao.i); } : sairDoPredio;
  const volta = el("button", "escolha secundaria voltar-vila", `<span class="rotulo">◀ Voltar à vila</span>`);
  volta.type = "button";
  volta.addEventListener("click", (ev) => { ev.stopPropagation(); sair(); });
  caixa.appendChild(volta);
  promptEl.appendChild(caixa);
  // As teclas 1, 2... escolhem os cartões, na ordem; Esc volta à vila.
  // Cada tecla faz o que o clique no cartão faz (o sem ouro recusa ali, sem a escolha chegar ao motor).
  pergunta = { id: v.m.id, tipo: "opcoes", n: v.m.opcoes.length, opcoes: v.m.opcoes, numeros: g.map(({ i }) => i), letras: {}, voltar: -1, voltarLocal: sair,
    teclasNum: cartoes.map((b) => () => b.click()) };
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
