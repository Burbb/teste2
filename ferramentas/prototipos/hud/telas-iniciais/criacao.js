/* A criação do personagem em cartões, a candidata R (protótipo, 24/10/2026; nada no jogo). Vale com
   html[data-telas="r"] (cenarios_telas.py, que manda os dados de cada opção no meta, como o motor faria). Só desenha:
   a escolha, as teclas, o Voltar e a caixa do tutorial são os de sempre (app/escolhas.js). Na classe, o busto da ficha
   (Icones.retrato), o ataque da roda (Icones.acao), o recurso e as duas especializações; no modo, dois cartões. */
"use strict";

(() => {
  if (document.documentElement.dataset.telas !== "r") return;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  function decorar() {
    const lista = document.querySelector("#prompt .escolhas:not(.escolhido)");
    if (!lista || lista.dataset.criacao || typeof pergunta === "undefined" || !pergunta || !pergunta.opcoes) return;
    const ops = pergunta.opcoes;
    const classes = ops.some((o) => o.meta && o.meta.classe), modos = ops.some((o) => o.meta && o.meta.modo);
    if (!classes && !modos) return;
    lista.dataset.criacao = "1";
    lista.classList.add(classes ? "criacao-classes" : "criacao-modo");
    lista.querySelectorAll("button.escolha").forEach((b) => {
      const texto = b.querySelector(".op-texto") && b.querySelector(".op-texto").textContent;
      const o = ops.find((x) => x.texto === texto);
      if (!o || !o.meta) return;
      b.closest("li").classList.add("criacao-cartao");
      if (o.meta.classe) {
        const m = o.meta, rot = b.querySelector(".rotulo");
        rot.insertAdjacentHTML("afterbegin", `<span class="cc-busto">${Icones.retrato(m.classe) || ""}</span>`);
        b.querySelector(".op-texto").insertAdjacentHTML("afterend",
          `<span class="cc-linha"><span class="cc-ataque">${Icones.acao(m.icone, 24) || ""}</span>${esc(m.recurso)}</span>` +
          `<span class="cc-specs"><small>No nível ${esc(m.nivel_spec)}</small>${m.specs.map(esc).join('<i aria-hidden="true">·</i>')}</span>`);
      }
    });
  }

  new MutationObserver(decorar).observe(document.body, { childList: true, subtree: true });
})();
