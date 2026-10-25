/* Carregar jogo (a R aprovada pelo Jean, 1.209.0; o acabamento em css/25-carregar.css): uma janela da família da
   criação, com as partidas numa coluna que rola e o Voltar no rodapé, fora da rolagem, desde a abertura. O motor manda
   os saves do mais recente ao mais antigo (resumo_save). O clique (ou Enter) no cartão carrega; o Voltar responde a
   opção "Voltar" da pergunta; Esc continua o de sempre. As setas e Home/End andam pelos cartões; o Tab vai dos cartões
   (um ponto só) ao Voltar. O foco começa na partida mais recente que abre; sem nenhuma, no Voltar. Os que não abrem
   continuam clicáveis: o motor responde com o motivo, e nada carrega. */
"use strict";

(() => {
  const { h } = Telas;

  function haQuanto(seg) {
    const m = Math.floor((Date.now() / 1000 - seg) / 60);
    if (m < 2) return "agora há pouco";
    if (m < 60) return `há ${m} min`;
    const hs = Math.floor(m / 60);
    if (hs < 24) return `há ${hs} h`;
    const d = Math.floor(hs / 24);
    return d === 1 ? "ontem" : `há ${d} dias`;
  }
  const naoAbre = (s) => !!(s.ilegivel || s.incompativel);

  /** Um cartão: à esquerda o retrato, o nome e "classe · especialização · nível"; à direita, menores, o lugar e o dia,
   *  a missão em andamento, o modo e quando. O que não abre diz por quê, em texto, no lugar do resto. */
  function cartao(s, i, primeiro) {
    const alvo = `data-save="${i}" tabindex="${i === primeiro ? 0 : -1}"`;
    if (naoAbre(s)) {
      const motivo = s.ilegivel ? "Save danificado: o arquivo não pôde ser lido." : "Do mundo gerado, o modo que saiu do jogo.";
      return `<button type="button" class="sv-cartao sv-nao-abre" ${alvo}>
        <span class="sv-busto">${s.classe ? Icones.retrato(s.classe) || "" : ""}</span>
        <span class="sv-quem"><b class="sv-nome">${h(s.nome)}</b>
          <span class="sv-classe">${s.ilegivel ? "" : `${h(s.classe_nome)} · nível ${s.nivel}`}</span></span>
        <span class="sv-onde"><span class="sv-aviso"><i aria-hidden="true">⊘</i> Não abre</span><span>${motivo}</span>
          <small>${haQuanto(s.modificado)}</small></span></button>`;
    }
    const classe = [s.classe_nome, s.spec_nome, `nível ${s.nivel}`].filter(Boolean).map(h).join(" · ");
    return `<button type="button" class="sv-cartao" ${alvo}>
      <span class="sv-busto">${Icones.retrato(s.classe, `Retrato: ${s.classe_nome}`) || ""}</span>
      <span class="sv-quem"><b class="sv-nome">${h(s.nome)}</b><span class="sv-classe">${classe}</span></span>
      <span class="sv-onde"><span>${h(s.lugar)} · Dia ${s.dia}</span>${s.progresso ? `<span>${h(s.progresso)}</span>` : ""}
        <small><i class="sv-modo">${s.hardcore === false ? "Resgate" : "Hardcore"}</i> ${haQuanto(s.modificado)}</small></span></button>`;
  }

  function saves(d) {
    const n = d.saves.length, ruins = d.saves.filter(naoAbre).length;
    const conta = n ? `${n} ${n === 1 ? "partida salva" : "partidas salvas"}${ruins ? ` · ${ruins} não ${ruins === 1 ? "abre" : "abrem"}` : ""}` : "";
    const primeiro = d.saves.findIndex((s) => !naoAbre(s));  // -1: nenhuma abre (o foco fica no Voltar)
    const lista = n ? d.saves.map((s, i) => cartao(s, i, primeiro < 0 ? 0 : primeiro)).join("") : '<p class="sv-vazia">Nenhuma partida salva.</p>';
    return `<section class="sv m-janela" aria-label="Carregar jogo" data-primeiro="${primeiro}">
      <header class="sv-cab"><h1>Carregar jogo</h1><span>${conta}</span></header>
      <div class="sv-lista" role="list">${lista}</div>
      <footer class="sv-rodape"><button type="button" class="sv-voltar"><span aria-hidden="true">◀</span> Voltar <kbd>Esc</kbd></button>
        ${n ? '<span class="sv-dica">↑ ↓ escolhe · Enter ou clique carrega · a mais recente primeiro</span>' : ""}</footer></section>`;
  }

  /** O nome cortado (reticências) ganha a dica com ele inteiro, no mouse e no foco do teclado. Só depois de desenhado
   *  se sabe se cortou. */
  function dicasDosNomes(sv) {
    let algum = false;
    sv.querySelectorAll(".sv-cartao").forEach((c) => {
      const nome = c.querySelector(".sv-nome");
      if (nome.scrollWidth <= nome.clientWidth + 1) return;
      c.setAttribute("data-dica", Telas.dica(h(nome.textContent), true).match(/\d+/)[0]);
      algum = true;
    });
    if (algum) Telas.ligarDicas(sv);
    // A rolagem fecha as dicas (a posição delas ficaria errada); quando a lista para, a do cartão com o foco do teclado
    // volta, no lugar novo.
    sv.querySelector(".sv-lista").addEventListener("scrollend", () => {
      const c = document.activeElement;
      if (c && c.matches(".sv-cartao[data-dica]:focus-visible")) c.dispatchEvent(new FocusEvent("focus"));
    });
  }

  function ligar(raiz) {
    const sv = raiz.querySelector(".sv");
    document.body.classList.add("sv-aberto");
    raiz.querySelectorAll("[data-save]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (ev.detail > 1 || sv.dataset.enviado) return;  // o segundo clique de um clique duplo não carrega de novo
      sv.dataset.enviado = "1";
      App.acao({ save: Number(b.dataset.save) }, "pagina");
    }));
    raiz.querySelector(".sv-voltar").addEventListener("click", (ev) => {
      ev.stopPropagation();
      const i = pergunta && pergunta.opcoes ? pergunta.opcoes.findIndex((o) => o.meta && o.meta.voltar) : -1;
      if (i >= 0) responder(pergunta.id, i);
    });
    const cartoes = [...raiz.querySelectorAll(".sv-cartao")];
    sv.addEventListener("keydown", (ev) => {
      const k = ev.key, at = cartoes.indexOf(document.activeElement);
      if (at < 0 || !["ArrowDown", "ArrowUp", "Home", "End"].includes(k)) return;
      ev.preventDefault(); ev.stopPropagation();
      const j = k === "Home" ? 0 : k === "End" ? cartoes.length - 1 : Math.max(0, Math.min(cartoes.length - 1, at + (k === "ArrowDown" ? 1 : -1)));
      cartoes.forEach((c, x) => { c.tabIndex = x === j ? 0 : -1; });
      cartoes[j].focus();
      cartoes[j].scrollIntoView({ block: "nearest" });
    });
    requestAnimationFrame(() => {
      // o foco: a partida mais recente que abre (as setas já andam, o Enter já carrega); sem nenhuma, o Voltar
      const alvo = cartoes[Number(sv.dataset.primeiro)] || raiz.querySelector(".sv-voltar");
      alvo.focus({ preventScroll: true });
      alvo.scrollIntoView({ block: "nearest" });
      dicasDosNomes(sv);
      // a página seguiu (a mensagem do save que não abre, o título de novo, a partida): a janela sai da frente
      const fim = () => { document.body.classList.remove("sv-aberto"); obs.disconnect(); };
      const obs = new MutationObserver(() => { if (!sv.isConnected || document.getElementById("texto").lastElementChild !== raiz) fim(); });
      obs.observe(document.getElementById("texto"), { childList: true });
      obs.observe(document.getElementById("cena-cab"), { childList: true });
    });
  }

  Telas.registrar("saves", saves, { ligar });
})();
