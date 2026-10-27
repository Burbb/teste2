/* A demonstração do reforço: a faixa no alto (o que é protótipo fica aqui, fora da tela do jogador) e a tela da forja
   escolhida pelo endereço (?tela=v9, v8, v7, v6, v5, v4, v3, v2 ou v1: as versões antigas, guardadas como histórico;
   sem ele, a atual, a 9ª, com o Encantar do laboratório). A v3 tem a A anterior e a B, trocadas aqui. Na atual, a faixa também escolhe o caso de teste da próxima
   tentativa (sucesso ou falha forçados, uma vez), separado do sorteio normal, e abre a comparação de teste da peça
   escolhida (o dano contra um alvo fixo: medição do laboratório, fora da tela do jogador). Trocar de versão
   recarrega a página; a partida continua (ela mora no servidor). */
"use strict";

(() => {
  const params = new URLSearchParams(location.search);
  const versao = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9"].includes(params.get("tela")) ? params.get("tela") : "atual";
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
    const P = window.ReforcoProto;
    let extra = "";
    if (versao === "v3" && P && P.direcao) {
      extra = `<span>Forja:</span>${[["A", "A · Bancada"], ["B", "B · Arsenal"]].map(([id, nome]) =>
        `<button type="button" data-direcao="${id}" aria-pressed="${P.direcao() === id}">${nome}</button>`).join("")}`;
    } else if (versao === "atual" && P && P.teste) {
      extra = `<span>Próxima tentativa:</span>${[["", "Sorteio"], ["sucesso", "Sucesso (teste)"], ["falha", "Falha (teste)"]].map(([id, nome]) =>
        `<button type="button" data-teste="${id}" aria-pressed="${(P.teste() || "") === id}">${nome}</button>`).join("")}`;
      if (P.comparacao) extra += `<button type="button" data-comparar aria-pressed="false">Comparação (teste)</button>`;
      if (P.lutaTeste) extra += `<button type="button" data-luta>Luta de teste</button>`;
    }
    const versoes = [["atual", "atual"], ["v9", "v9"], ["v8", "v8"], ["v7", "v7"], ["v6", "v6"], ["v5", "v5"], ["v4", "v4"], ["v3", "v3 (A e B)"], ["v2", "v2"], ["v1", "v1"]].map(([id, nome]) =>
      id === versao ? `<b>${nome}</b>` : `<a href="${para(id)}">${nome}</a>`).join(" · ");
    f.innerHTML = `<strong>Protótipo do reforço</strong>${extra}<span class="faixa-hist">versões: ${versoes}</span>`;
    document.body.appendChild(f);
    f.querySelectorAll("[data-direcao]").forEach((b) => b.addEventListener("click", () => {
      P.direcao(b.dataset.direcao);
      f.querySelectorAll("[data-direcao]").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
    }));
    const marcarTeste = () => f.querySelectorAll("[data-teste]").forEach((x) => x.setAttribute("aria-pressed", String((P.teste() || "") === x.dataset.teste)));
    f.querySelectorAll("[data-teste]").forEach((b) => b.addEventListener("click", () => { P.teste(b.dataset.teste); marcarTeste(); }));
    window.addEventListener("reforco-teste", marcarTeste);  // usado uma vez, o caso volta para o sorteio
    // a luta de teste do encantamento: dois Esqueletos, e o grupo volta como estava (só com a forja aberta)
    const luta = f.querySelector("[data-luta]");
    if (luta) luta.addEventListener("click", () => { if (!P.lutaTeste()) aviso("Abra a forja para a luta de teste.", "info", "pergaminho"); });
    // a comparação de teste: um painel embaixo da faixa, com a peça escolhida (atualizado a cada desenho da forja)
    const comparar = f.querySelector("[data-comparar]");
    if (comparar) {
      const painel = document.createElement("div");
      painel.id = "faixa-comparacao";
      painel.hidden = true;
      document.body.appendChild(painel);
      const encher = () => { painel.innerHTML = P.comparacao() || "<p>Escolha uma peça com reforço disponível.</p>"; };
      comparar.addEventListener("click", () => {
        painel.hidden = !painel.hidden;
        comparar.setAttribute("aria-pressed", String(!painel.hidden));
        encher();
      });
      window.addEventListener("reforco-comparacao", () => { if (!painel.hidden) encher(); });
    }
  }
  const estilo = document.createElement("style");
  estilo.textContent = `#faixa-demo { position: fixed; z-index: 90; top: 6px; left: 50%; translate: -50% 0; display: flex; align-items: center;
    gap: 8px; padding: 3px 10px; font: 13px/1.3 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px solid #8a6a2a;
    box-shadow: 0 2px 6px rgba(0,0,0,.6); white-space: nowrap; }
  #faixa-demo strong { color: #f2d27a; letter-spacing: .06em; text-transform: uppercase; font-size: 12px; }
  #faixa-demo button { font: inherit; color: #cfc6b2; background: #2a2116; border: 1px solid #5a4632; padding: 1px 8px; cursor: pointer; }
  #faixa-demo button[aria-pressed="true"] { color: #1d1407; background: #f2d27a; border-color: #f2d27a; }
  #faixa-demo button:focus-visible { outline: 2px solid #f2d27a; outline-offset: 1px; }
  #faixa-demo a { color: #f2d27a; }
  #faixa-demo .faixa-hist { color: #9d978b; }
  #faixa-comparacao { position: fixed; z-index: 90; top: 34px; left: 50%; translate: -50% 0; width: 340px; padding: 8px 12px;
    font: 13px/1.35 var(--texto, sans-serif); color: #cfc6b2; background: #1d1407; border: 1px dashed #8a6a2a; box-shadow: 0 2px 6px rgba(0,0,0,.6); }
  #faixa-comparacao .rf-teste { margin: 0; padding: 0; border: 0; }
  #faixa-comparacao b { color: #f2d27a; }
  #faixa-comparacao p { margin: 2px 0 6px; color: #9d978b; }
  #faixa-comparacao .rf-teste-bloco small { color: #9d978b; }
  #faixa-comparacao .rf-teste-linha { display: flex; justify-content: space-between; gap: 8px; }
  #faixa-comparacao .melhor { color: #9fe07c; } #faixa-comparacao .pior { color: #ff8c78; }`;
  document.head.appendChild(estilo);
})();
