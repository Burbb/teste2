"use strict";

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
function alternarFonte(forcar) {
  const pixel = forcar === undefined ? !corpo.classList.contains("fonte-pixel") : forcar;
  corpo.classList.toggle("fonte-pixel", pixel);
  $("#fonte-rotulo").textContent = pixel ? "pixel" : "livro";
  if (forcar === undefined) guardar("cdf-fonte", pixel ? "pixel" : "livro");
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
  $("#sobre-grimorio").hidden = true;
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
    else if (a === "fonte") alternarFonte();
    else if (a === "heroi") corpo.classList.toggle("mostrar-heroi");
    else if (a === "mundo") corpo.classList.toggle("mostrar-mundo");
    else if (a === "fechar-talentos") fecharTudo();
    else if (a === "fechar-grimorio") $("#sobre-grimorio").hidden = true;
    return;
  }
  // Clique fora da caixa (no véu escuro em volta) fecha, como Esc: livro, mapa e árvore de talentos.
  if (ev.target.id === "sobre-grimorio") { ev.target.hidden = true; return; }
  if (ev.target.id === "sobre-mapa") { alternarMapa(false); return; }
  if (ev.target.id === "sobre-talentos") { fecharTudo(); return; }
  if (ev.target.closest(".talento-aviso")) { pedir("Talentos", "_", null); return; }
  const carta = ev.target.closest("[data-conversar]");
  if (carta) {
    const cid = carta.dataset.conversar;
    const direta = pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => o.meta && o.meta.conversar === cid);
    if (direta || (pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => o.texto.startsWith("Comitiva")))) pedir("Comitiva", "conversar", cid);
    else Telas.toast("", "Dá para conversar quando estiver num lugar seguro (vila ou acampamento).", cid, true);
    return;
  }
  if (processando && ev.target.closest("#cena")) pular = true;
});

document.addEventListener("keydown", (ev) => {
  primeiraInteracao();
  if (ev.target.tagName === "INPUT") { if (ev.key === "Escape") ev.target.blur(); return; }
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
  const k = ev.key;
  if (k === "Escape" || k === "Backspace") {
    if (fecharJanela()) { ev.preventDefault(); return; }  // a janelinha de habilidades/itens da luta fecha primeiro
    const aberto = !$("#gaveta-historico").hidden || !$("#sobre-mapa").hidden || !$("#sobre-talentos").hidden || !$("#sobre-grimorio").hidden || document.querySelector(".menu-item");
    if (!aberto && pergunta && pergunta.voltar !== undefined && !processando) { ev.preventDefault(); voltarPergunta(); return; }
    if (k === "Escape") { Telas.fecharMenuItem(); fecharTudo(); }
    return;
  }
  if (pergunta && pergunta.letras && pergunta.letras[k.toLowerCase()] !== undefined && !processando) {
    ev.preventDefault(); responder(pergunta.id, pergunta.letras[k.toLowerCase()]); return;
  }
  if (k.length === 1 && /[a-z]/i.test(k) && estado && !estado.combate && !corpo.classList.contains("modo-titulo")) {
    // As teclas dos atalhos (I, C, T...) valem dentro das telas da doca e também com texto correndo (o pedido fica
    // guardado). Salvar e Sair só dentro das telas: uma tecla solta no meio da leitura não deve sair do jogo.
    const at = SISTEMA.find((x) => x[2] === k.toLowerCase() && x[1] !== "Mapa");
    if (at && (docaTela || !["Salvar", "Sair"].includes(at[1]))) { ev.preventDefault(); pedirAtalho(at[1]); return; }
  }
  if (k === "F2" || k === "h" || k === "H") { ev.preventDefault(); alternarHistorico(); return; }
  if (k === "m" || k === "M") { alternarMapa(); return; }
  if (k === "F3" || k === "v" || k === "V") { ev.preventDefault(); mudarVelocidade(); return; }
  if (k === "s" || k === "S") { alternarSom(); return; }
  if (k === "i" || k === "I") { corpo.classList.toggle("mostrar-heroi"); return; }
  if (k === "n" || k === "N") { corpo.classList.toggle("mostrar-mundo"); return; }
  if ((k === "p" || k === "P") && estado && !corpo.classList.contains("modo-titulo")) { Telas.alternarGrimorio(); return; }
  if (processando && !pergunta) { if (k.length === 1 || k === "Enter") { ev.preventDefault(); pular = true; } return; }
  if (!pergunta) return;
  if (pergunta.tipo === "continuar" && (k === " " || k === "Enter")) { ev.preventDefault(); responder(pergunta.id, null); return; }
  if (pergunta.tipo !== "opcoes" || !pergunta.numeros) return;
  const botoes = [...promptEl.querySelectorAll(".escolha, .atalho")];
  if (/^[0-9]$/.test(k) && pergunta.teclasNum) {  // barra de ações da luta: cada tecla faz o que o botão faz
    const f = pergunta.teclasNum[k === "0" ? 9 : Number(k) - 1];
    if (f) { ev.preventDefault(); f(); }
    return;
  }
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


// As tochas da HUD tremulam: troca de quadro a cada 400 ms.
setInterval(() => {
  const a = Sprites.url("tocha"), b = Sprites.url("tocha2");
  document.querySelectorAll('.recurso[data-rec="tochas"] img').forEach((img) => {
    if (img.src === a) img.src = b; else if (img.src === b) img.src = a;
  });
}, 400);

async function iniciar() {
  Batalha.configurar({ rapido: instantaneo, pausa: ritmo });
  Sensacao.configurar({ rapido: instantaneo, pausa: ritmo });
  try {
    const r = await fetch(`/config?token=${encodeURIComponent(TOKEN)}`);
    const cfg = await r.json();
    if (!ler("cdf-velocidade") && VELOCIDADES[cfg.velocidade] !== undefined) velocidade = cfg.velocidade;
  } catch (e) { /* usa o padrão */ }
  $("#vel-rotulo").textContent = NOME_VEL[velocidade];
  alternarFonte(ler("cdf-fonte") === "pixel");
  $("#botao-som").classList.toggle("desligado", !Som.ligado);
  brasas();
  conectar();
}
iniciar();
