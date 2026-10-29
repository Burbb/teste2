/* A demonstração da taverna (protótipo): um botão "Protótipo" na barra do alto, entre os sigilos e o menu (no fluxo
   da barra: o clima, a hora e os sigilos não ficam embaixo dele), abre o painel que troca a candidata (a F, o estudo
   estático em avaliação; da E à A, o histórico), o estado do save temporário (a despensa esperando, o homem do canto, Morel já
   conhecido, Morel recrutado, sem ouro) e liga a pose parada. Escolhido, o painel fecha. O interior entra pelo caminho
   do templo (vila.js, estado.local.interiores, com a taverna acrescentada pelo demo.py). */
"use strict";

(() => {
  if (typeof ACOES_OCULTAS !== "undefined" && !ACOES_OCULTAS.includes("tav_estado")) ACOES_OCULTAS.push("tav_estado");
  const naTaverna = () => !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna");
  const ESTADOS = [["despensa", "Despensa esperando"], ["homem_do_canto", "Homem do canto"], ["conhecido", "Morel conhecido"],
    ["recrutado", "Morel recrutado"], ["sem_ouro", "Sem ouro"]];
  const f = document.createElement("div");
  f.id = "faixa-tav";
  document.body.dataset.tavCand = document.body.dataset.tavCand || "f";  // a F, o estudo em avaliação (as outras, histórico)
  const CANDS = [["f", "Candidata F (estudo estático)"], ["e", "Candidata E (histórico)"], ["d", "Candidata D (histórico)"],
    ["c", "Candidata C (histórico)"], ["b", "Candidata B (histórico)"], ["a", "Candidata A (histórico)"]];
  f.innerHTML = `<button type="button" class="abre" aria-expanded="false" aria-controls="faixa-tav-painel">Protótipo: F · Homem do canto</button>
    <div id="faixa-tav-painel" hidden><b>Taverna (protótipo): a candidata</b>
    ${CANDS.map(([id, nome]) => `<button type="button" data-cand="${id}" aria-pressed="${id === "f"}">${nome}</button>`).join("")}
    <b>O estado do save temporário</b>
    ${ESTADOS.map(([id, nome]) => `<button type="button" data-tav="${id}" aria-pressed="${id === "homem_do_canto"}">${nome}</button>`).join("")}
    <button type="button" data-reduzido aria-pressed="false">Pose parada</button></div><span class="aviso"></span>`;
  const topo = document.getElementById("topo");
  topo.insertBefore(f, document.getElementById("acoes-topo"));
  const abre = f.querySelector(".abre"), painel = f.querySelector("#faixa-tav-painel"), aviso = f.querySelector(".aviso");
  document.body.appendChild(painel);  // o painel fica fora da barra (que rola na janela estreita) e cai embaixo do botão
  const abrir = (sim) => {
    const r = abre.getBoundingClientRect();
    Object.assign(painel.style, { left: Math.round(r.left) + "px", top: Math.round(r.bottom + 3) + "px" });
    painel.hidden = !sim; abre.setAttribute("aria-expanded", String(sim));
  };
  abre.addEventListener("click", () => abrir(painel.hidden));
  const rotulo = () => {
    const e = painel.querySelector('[data-tav][aria-pressed="true"]');
    abre.textContent = `Protótipo: ${document.body.dataset.tavCand.toUpperCase()} · ${e ? e.textContent : ""}`;
  };
  painel.querySelectorAll("[data-cand]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    document.body.dataset.tavCand = b.dataset.cand;
    painel.querySelectorAll("[data-cand]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    rotulo();
    if (naTaverna()) Cenas.mostrar(Cenas.atual().d);  // a outra sala, com os pontos dela
  }));
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !painel.hidden) { ev.stopPropagation(); abrir(false); abre.focus(); } }, true);
  painel.querySelectorAll("[data-tav]").forEach((b) => b.addEventListener("click", () => {
    abrir(false);
    const volta = naTaverna();
    if (volta && pergunta && pergunta.voltarLocal) pergunta.voltarLocal();
    setTimeout(() => {
      const ok = App.acao({ tav_estado: b.dataset.tav });
      aviso.textContent = ok ? "" : "Volte à vila para trocar o estado.";
      if (!ok) return;
      painel.querySelectorAll("[data-tav]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      rotulo();
      if (volta) predioPedido = "taverna";  // a vila se remonta e entra de novo na taverna
    }, volta ? 60 : 0);
  }));
  painel.querySelector("[data-reduzido]").addEventListener("click", (ev) => {
    const sim = document.body.dataset.tavReduzido !== "1";
    document.body.dataset.tavReduzido = sim ? "1" : "";
    ev.currentTarget.setAttribute("aria-pressed", String(sim));
  });
})();
