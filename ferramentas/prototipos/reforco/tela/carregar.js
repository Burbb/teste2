/* A demonstração do reforço: a faixa no alto (o que é protótipo fica aqui, fora da tela do jogador) e a tela da forja
   escolhida pelo endereço (?tela=v1 ou v2: as versões antigas, guardadas como histórico; sem ele, a atual, com as
   direções A e B). Trocar de versão recarrega a página; a partida continua (ela mora no servidor). */
"use strict";

(() => {
  const params = new URLSearchParams(location.search);
  const versao = ["v1", "v2"].includes(params.get("tela")) ? params.get("tela") : "atual";
  const base = versao === "atual" ? "/proto/" : `/proto/historico/${versao}/`;
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = `${base}reforco.css`;
  document.head.appendChild(css);
  const js = document.createElement("script");
  js.src = `${base}reforco.js`;
  js.onload = () => faixa();
  document.body.appendChild(js);

  const para = (v) => { const q = new URLSearchParams(location.search); if (v === "atual") q.delete("tela"); else q.set("tela", v); return `?${q}`; };
  function faixa() {
    const f = document.createElement("div");
    f.id = "faixa-demo";
    const direcoes = versao === "atual" && window.ReforcoProto
      ? `<span>Forja:</span>${[["A", "A · Bancada"], ["B", "B · Arsenal"]].map(([id, nome]) =>
        `<button type="button" data-direcao="${id}" aria-pressed="${window.ReforcoProto.direcao() === id}">${nome}</button>`).join("")}` : "";
    const versoes = [["atual", "atual"], ["v2", "v2"], ["v1", "v1"]].map(([id, nome]) =>
      id === versao ? `<b>${nome}</b>` : `<a href="${para(id)}">${nome}</a>`).join(" · ");
    f.innerHTML = `<strong>Protótipo do reforço</strong>${direcoes}<span class="faixa-hist">histórico: ${versoes}</span>`;
    document.body.appendChild(f);
    f.querySelectorAll("[data-direcao]").forEach((b) => b.addEventListener("click", () => {
      window.ReforcoProto.direcao(b.dataset.direcao);
      f.querySelectorAll("[data-direcao]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    }));
  }
  const estilo = document.createElement("style");
  estilo.textContent = `#faixa-demo { position: fixed; z-index: 90; top: 6px; left: 50%; translate: -50% 0; display: flex; align-items: center;
    gap: 8px; padding: 3px 10px; font: 13px/1.3 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px solid #8a6a2a;
    box-shadow: 0 2px 6px rgba(0,0,0,.6); }
  #faixa-demo strong { color: #f2d27a; letter-spacing: .06em; text-transform: uppercase; font-size: 12px; }
  #faixa-demo button { font: inherit; color: #cfc6b2; background: #2a2116; border: 1px solid #5a4632; padding: 1px 8px; cursor: pointer; }
  #faixa-demo button[aria-pressed="true"] { color: #1d1407; background: #f2d27a; border-color: #f2d27a; }
  #faixa-demo button:focus-visible { outline: 2px solid #f2d27a; outline-offset: 1px; }
  #faixa-demo a { color: #f2d27a; }
  #faixa-demo .faixa-hist { color: #9d978b; }`;
  document.head.appendChild(estilo);
})();
