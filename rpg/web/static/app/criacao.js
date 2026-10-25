/* A criação do personagem em etapas (a R2 aprovada pelo Jean, 1.208.0; o acabamento em 24-criacao.css). O motor manda
   a criação numa pergunta só, "criacao" (criacao.py), com tudo o que a tela mostra: os textos, as classes, os modos e o
   tutorial. A tela só desenha e anda pelas etapas (Nome → Classe → Modo) guardando as escolhas; nada vai ao motor até o
   "Começar campanha" (ou o Voltar da primeira etapa, que volta ao título), e então vai uma vez só.

   Escolher e avançar são gestos separados: o clique num cartão, as teclas 1–3, as setas e o espaço só escolhem; o
   Avançar (ou Enter) leva à etapa seguinte. Contra a tecla segurada e o clique duplo, o controle dos gestos (Gesto, em
   nucleo.js), sem espera por tempo: a tecla que vinha apertada da etapa anterior e as repetições não contam (um Enter
   novo, solto e apertado de novo, vale na hora), e o segundo clique de um clique duplo não avança de novo. */
"use strict";

const Criacao = (() => {
  const ETAPAS = ["Nome", "Classe", "Modo"];
  let m = null, st = null, etapa = 0, enviado = false, painel = null;

  const h = (s) => esc(String(s ?? ""));
  const vivo = () => painel.querySelector(".cr-etapa.atual");

  function mostrar(msg) {
    m = msg;
    st = { nome: "", classe: null, modo: msg.modo.padrao, tutorial: !!msg.tutorial.marcada };
    enviado = false;
    pergunta = { id: msg.id, tipo: "criacao" };
    corpo.classList.add("criando");
    promptEl.innerHTML = "";
    painel = el("section", "cr m-janela");
    painel.setAttribute("aria-label", "Criação de personagem");
    promptEl.appendChild(painel);
    irPara(0);
  }

  /** O que vier do motor depois da criação (o título de novo, a abertura da campanha) desmonta a tela. */
  function aoMensagem(msg) {
    if (!painel || !["nova_cena", "cabecalho"].includes(msg.t)) return;
    painel.remove();
    painel = null;
    corpo.classList.remove("criando");
  }

  const nomeVisto = () => st.nome.trim() || m.nome.padrao;
  const classeEscolhida = () => m.classes.find((c) => c.id === st.classe);
  const modoEscolhido = () => m.modo.opcoes.find((o) => o.id === st.modo);
  const pronto = () => (etapa === 1 ? !!st.classe : etapa === 2 ? !!st.modo : true);

  function irPara(n) {
    etapa = n;
    Gesto.novaTela();  // a tecla que trouxe até aqui (o Enter, o Esc) não vale nesta etapa enquanto não for solta
    // As três etapas na mesma célula, as outras invisíveis e inertes: o painel tem sempre a altura da maior (não pula).
    const corpos = [corpoNome, corpoClasse, corpoModo].map((f, i) =>
      `<div class="cr-etapa${i === n ? " atual" : ""}"${i === n ? "" : ' inert aria-hidden="true"'}>${f()}</div>`).join("");
    painel.innerHTML = cabecalho() + `<div class="cr-corpo">${corpos}</div>` + rodape();
    ligar();
    focar();
  }

  function cabecalho() {
    const passos = ETAPAS.map((nome, i) => {
      const estado = i < etapa ? "feita" : i === etapa ? "atual" : "";
      const dentro = `<span class="cr-n">${i + 1}</span>${nome}`;
      // As feitas voltam com o clique (o Esc e o Voltar fazem o mesmo, uma por vez); fora do Tab, para ele seguir a tela.
      return i < etapa ? `<li class="${estado}"><button type="button" tabindex="-1" data-etapa="${i}">${dentro}</button></li>`
        : `<li class="${estado}"${i === etapa ? ' aria-current="step"' : ""}>${dentro}</li>`;
    }).join('<li class="cr-seta" aria-hidden="true">→</li>');
    return `<header class="cr-cab"><div class="cr-titulo"><h1>Criação de personagem</h1><span>${h(m.regiao)}</span></div>` +
      `<ol class="cr-etapas" aria-label="Etapas">${passos}</ol></header>`;
  }

  function corpoNome() {
    return `<div class="cr-nome"><label for="cr-campo">${h(m.nome.pergunta)}</label>` +
      `<input id="cr-campo" maxlength="${m.nome.max}" autocomplete="off" spellcheck="false" placeholder="${h(m.nome.padrao)}" value="${h(st.nome)}">` +
      `<small>Em branco, fica ${h(m.nome.padrao)}.</small></div>`;
  }

  function cartaoClasse(c, i) {
    const marcado = st.classe === c.id;
    const rec = Icones.vital(c.recurso.nome, 20) || spr(RECURSO_ICONE[c.recurso.nome] || "estrela", 1);
    return `<button type="button" class="cr-cartao cr-classe" role="radio" aria-checked="${marcado}" data-valor="${h(c.id)}" tabindex="${marcado || (!st.classe && i === 0) ? 0 : -1}">` +
      `<span class="cr-tecla">${i + 1}</span><span class="cr-marca" aria-hidden="true">Escolhida</span>` +
      `<span class="cr-busto">${Icones.retrato(c.id, `Retrato: ${c.nome}`) || spr(c.id, 3)}</span>` +
      `<span class="cr-titulo-cartao">${h(c.nome)}</span>` +
      `<span class="cr-frase">${h(c.frase)}</span>` +
      `<span class="cr-dados"><span class="cr-dado">${Icones.acao(c.ataque.icone, 24) || ""}<span><b>${h(c.ataque.nome)}</b> · ${h(c.ataque.alcance)}</span></span>` +
      `<span class="cr-dado">${rec}<span><b>${h(c.recurso.nome)} ${c.recurso.total}</b> · recupera ${c.recurso.regen} por turno</span></span></span>` +
      `<span class="cr-specs">No nível ${c.nivel_spec}: ${c.specs.map(h).join(" ou ")}</span></button>`;
  }
  function corpoClasse() {
    return `<div class="cr-pergunta"><h2>Sua classe</h2><span class="cr-dica">Clique num cartão ou tecle 1–${m.classes.length} para escolher.</span></div>` +
      `<div class="cr-grade cr-grade-classes" role="radiogroup" aria-label="Classe">${m.classes.map(cartaoClasse).join("")}</div>`;
  }

  function cartaoModo(o, i) {
    const marcado = st.modo === o.id;
    return `<button type="button" class="cr-cartao cr-modo" role="radio" aria-checked="${marcado}" data-valor="${h(o.id)}" tabindex="${marcado ? 0 : -1}">` +
      `<span class="cr-tecla">${i + 1}</span><span class="cr-marca" aria-hidden="true">Escolhido</span>` +
      `<span class="cr-titulo-cartao">${h(o.nome)}</span>` +
      `<span class="cr-linhas">${o.linhas.map((t) => `<span>${h(t)}</span>`).join("")}</span></button>`;
  }
  function corpoModo() {
    const t = m.tutorial;
    return `<div class="cr-pergunta"><h2>${h(m.modo.pergunta)}</h2><span class="cr-dica">Tecle 1–${m.modo.opcoes.length} para escolher.</span></div>` +
      `<div class="cr-grade cr-grade-modos" role="radiogroup" aria-label="Se você cair">${m.modo.opcoes.map(cartaoModo).join("")}</div>` +
      `<label class="cr-tutorial"><input type="checkbox" id="cr-tutorial"${st.tutorial ? " checked" : ""}>` +
      `<span><b>${h(t.rotulo)}</b><small>${h(t.nota)}</small></span></label>`;
  }

  /** O resumo do que já se escolheu ("Ana · Arqueiro · Resgate"), no rodapé, junto do botão que avança. */
  function partesResumo() {
    const partes = [];
    if (etapa >= 1) partes.push(nomeVisto());
    if (etapa >= 2) { partes.push(classeEscolhida().nome); if (modoEscolhido()) partes.push(modoEscolhido().nome); }
    return partes;
  }
  const resumo = () => partesResumo().map((p) => `<span>${h(p)}</span>`).join('<i aria-hidden="true">·</i>');
  function rodape() {
    const fim = etapa === ETAPAS.length - 1;
    return `<footer class="cr-rodape"><button type="button" class="cr-voltar"><span aria-hidden="true">◀</span> Voltar <kbd>Esc</kbd></button>` +
      `<div class="cr-resumo" aria-live="polite" title="${h(partesResumo().join(" · "))}">${resumo()}</div>` +
      `<button type="button" class="cr-avancar${fim ? " cr-comecar" : ""}"${pronto() ? "" : " disabled"}>` +
      `${fim ? "Começar campanha" : "Avançar"} <span aria-hidden="true">▸</span> <kbd>Enter</kbd></button></footer>`;
  }

  function ligar() {
    // o segundo clique de um clique duplo (detail 2) não volta nem avança outra etapa
    painel.querySelector(".cr-voltar").addEventListener("click", (ev) => { if (ev.detail < 2) voltar(); });
    painel.querySelector(".cr-avancar").addEventListener("click", (ev) => { if (ev.detail < 2) avancar(); });
    painel.querySelectorAll("[data-etapa]").forEach((b) => b.addEventListener("click", () => irPara(Number(b.dataset.etapa))));
    painel.querySelectorAll(".cr-cartao").forEach((b) => b.addEventListener("click", () => escolher(b.dataset.valor)));
    const campo = painel.querySelector("#cr-campo");
    if (campo) campo.addEventListener("input", () => { st.nome = campo.value; });
    const tut = painel.querySelector("#cr-tutorial");
    if (tut) tut.addEventListener("change", () => { st.tutorial = tut.checked; });
  }

  function focar() {
    requestAnimationFrame(() => {
      const alvo = vivo().querySelector("#cr-campo") || vivo().querySelector('.cr-cartao[tabindex="0"]');
      if (!alvo) return;
      alvo.focus({ preventScroll: true });
      if (alvo.select) alvo.select();
    });
  }

  /** Escolher (o clique, a tecla, a seta): marca o cartão e libera o Avançar; não muda de etapa. */
  function escolher(valor, focarCartao = false) {
    if (etapa === 1) st.classe = valor; else if (etapa === 2) st.modo = valor; else return;
    vivo().querySelectorAll(".cr-cartao").forEach((b) => {
      const sim = b.dataset.valor === valor;
      b.setAttribute("aria-checked", String(sim));
      b.tabIndex = sim ? 0 : -1;
      if (sim && focarCartao) b.focus({ preventScroll: true });
    });
    const av = painel.querySelector(".cr-avancar");
    av.disabled = !pronto();
    const r = painel.querySelector(".cr-resumo");
    r.innerHTML = resumo();
    r.title = partesResumo().join(" · ");
    Som.tocar("escolha");
  }

  function avancar() {
    if (enviado || !pronto()) return;
    if (etapa < ETAPAS.length - 1) { irPara(etapa + 1); return; }
    enviado = true;
    const b = painel.querySelector(".cr-avancar");
    b.disabled = true;
    b.innerHTML = "Começando…";
    responder(pergunta.id, { nome: st.nome.trim(), classe: st.classe, modo: st.modo, tutorial: st.tutorial });
  }

  function voltar() {
    if (enviado) return;
    if (etapa > 0) { irPara(etapa - 1); return; }
    enviado = true;
    responder(pergunta.id, { voltar: true });
  }

  document.addEventListener("keydown", (ev) => {
    if (!painel || !pergunta || pergunta.tipo !== "criacao" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    if (!document.getElementById("sobre-ajuda").hidden) return;  // a Ajuda aberta por cima: as teclas são dela
    const k = ev.key, noCampo = ev.target.id === "cr-campo";
    const parar = () => { ev.preventDefault(); ev.stopPropagation(); };
    const vale = Gesto.teclaVale(ev);  // nem repetição, nem a tecla que vinha apertada da etapa anterior
    if (k === "Escape") { parar(); if (vale) voltar(); return; }
    if (k === "Enter") {
      // Enter num botão da barra de etapas ou no Voltar faz o que o botão faz; em qualquer outro lugar, avança.
      if (ev.target.closest && ev.target.closest(".cr-voltar, .cr-etapas button")) return;
      parar();
      if (vale) avancar();
      return;
    }
    if (noCampo) return;  // no campo do nome, as outras teclas são do texto
    const cartoes = [...vivo().querySelectorAll(".cr-cartao")];
    if (!cartoes.length) return;
    if (/^[1-9]$/.test(k)) {
      parar();
      const b = cartoes[Number(k) - 1];
      if (b && vale) escolher(b.dataset.valor, true);
      return;
    }
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(k)) {
      parar();
      const atual = Math.max(0, cartoes.findIndex((b) => b.getAttribute("aria-checked") === "true"));
      const passo = k === "ArrowLeft" || k === "ArrowUp" ? -1 : 1;
      escolher(cartoes[(atual + passo + cartoes.length) % cartoes.length].dataset.valor, true);
    }
  }, true);

  return { mostrar, aoMensagem };
})();
