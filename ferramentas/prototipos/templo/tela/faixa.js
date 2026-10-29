/* A demonstração do templo (protótipo): a faixa do alto (a candidata A ou B, o estado do save temporário, a pose
   parada). Desde a 1.219.0 o jogo mostra o interior sozinho diante do templo (vila.js, estado.local.interiores, e a
   Saída da cena pelo Voltar à vila do balcão); a demonstração só troca o desenho de produção pelo do protótipo
   (tela/cena-templo.js, com as duas candidatas). */
"use strict";

(() => {
  if (typeof ACOES_OCULTAS !== "undefined" && !ACOES_OCULTAS.includes("tpl_estado")) ACOES_OCULTAS.push("tpl_estado");
  document.body.dataset.tplCand = document.body.dataset.tplCand || "b";  // a B, aprovada (a A fica como histórico)
  const noTemplo = () => !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "templo");

  // ---- a faixa
  const ESTADOS = [["ferido", "Ferido, 1º grátis"], ["sem_ouro", "Sem ouro"], ["comitiva", "Odette ferida"], ["ninguem", "Ninguém precisa"]];
  const f = document.createElement("div");
  f.id = "faixa-tpl";
  f.innerHTML = `<b>Templo (protótipo)</b>
    <button type="button" data-cand="b" aria-pressed="true">Candidata B</button>
    <button type="button" data-cand="a" aria-pressed="false" title="A primeira direção, guardada como histórico">A (histórico)</button>
    <span class="sep"></span>${ESTADOS.map(([id, nome]) => `<button type="button" data-tpl="${id}">${nome}</button>`).join("")}
    <button type="button" data-reduzido aria-pressed="false">Pose parada</button><span class="aviso"></span>`;
  document.body.appendChild(f);
  const aviso = f.querySelector(".aviso");
  f.querySelectorAll("[data-cand]").forEach((b) => b.addEventListener("click", () => {
    document.body.dataset.tplCand = b.dataset.cand;
    f.querySelectorAll("[data-cand]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    if (noTemplo()) Cenas.mostrar(Cenas.atual().d);  // os pontos da outra candidata
  }));
  f.querySelectorAll("[data-tpl]").forEach((b) => b.addEventListener("click", () => {
    const volta = noTemplo();
    if (volta && pergunta && pergunta.voltarLocal) pergunta.voltarLocal();
    setTimeout(() => {
      const ok = App.acao({ tpl_estado: b.dataset.tpl });
      aviso.textContent = ok ? "" : "Volte à vila para trocar o estado.";
      if (ok && volta) predioPedido = "templo";  // a vila se remonta e entra de novo no templo
    }, volta ? 60 : 0);
  }));
  f.querySelector("[data-reduzido]").addEventListener("click", (ev) => {
    const sim = document.body.dataset.tplReduzido !== "1";
    document.body.dataset.tplReduzido = sim ? "1" : "";
    ev.currentTarget.setAttribute("aria-pressed", String(sim));
  });
})();
