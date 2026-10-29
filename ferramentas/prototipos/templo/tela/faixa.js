/* A demonstração do templo (protótipo): o interior no lugar da vila aproximada enquanto o jogador está diante do
   templo, e a faixa do alto (a candidata A ou B, o estado do save temporário, a pose parada).

   O balcão do templo é o de sempre (vila.js: os cartões que o motor marca, o Voltar à vila, o Esc, as teclas 1, 2...);
   só a vista muda. Ao entrar no templo, a tela mostra a cena "templo" (Cenas.mostrar, como a forja e a curandeira
   fazem pelo motor); ao sair dele (Voltar, Esc, a Saída da cena), a vila volta. Depois de cuidar de alguém, o motor
   mantém o balcão aberto e a vila se remonta já diante dele: a cena volta junto. */
"use strict";

(() => {
  if (typeof ACOES_OCULTAS !== "undefined" && !ACOES_OCULTAS.includes("tpl_estado")) ACOES_OCULTAS.push("tpl_estado");
  document.body.dataset.tplCand = document.body.dataset.tplCand || "b";  // a B é a direção escolhida (a A fica como histórico)

  const DADOS = () => ({ cena: "templo", titulo: "O templo", pagina: true, pontos: [
    { id: "clerigo", nome: "Clérigo", faz: "cuidar da vida", estado: "O clérigo, na mesa dos panos.", servicos: true },
    { id: "saida", nome: "Saída", faz: "voltar à vila", estado: "A porta para a rua do Vau.", acao: { tpl_saida: true } },
  ] });
  const noTemplo = () => !!(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "templo");

  // ---- o interior no lugar da vila aproximada
  const entrar0 = window.entrarNoPredio, montar0 = window.montarVila, fechar0 = window.fecharVila, sair0 = window.sairDoPredio;
  window.entrarNoPredio = function (id, ...resto) {
    const r = entrar0.call(this, id, ...resto);
    if (id === "templo" && vilaAberta && vilaAberta.predio === "templo") Cenas.mostrar(DADOS());
    return r;
  };
  window.montarVila = function (...a) { if (noTemplo()) Cenas.limpar(); return montar0.apply(this, a); };
  window.fecharVila = function (...a) { if (noTemplo()) Cenas.limpar(); return fechar0.apply(this, a); };
  window.sairDoPredio = function (...a) { if (noTemplo()) Cenas.limpar(); return sair0.apply(this, a); };
  // a Saída da cena faz o que o Voltar à vila do balcão faz (o local, ou o do motor quando ele mantém o balcão)
  document.addEventListener("click", (ev) => {
    const bt = ev.target.closest && ev.target.closest('#pontos-cena .ci-ponto[data-ponto="saida"]');
    if (!bt || !noTemplo()) return;
    ev.stopPropagation(); ev.preventDefault();
    if (pergunta && pergunta.voltarLocal) pergunta.voltarLocal();
  }, true);

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
    if (noTemplo()) Cenas.mostrar(DADOS());  // os pontos da outra candidata
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
