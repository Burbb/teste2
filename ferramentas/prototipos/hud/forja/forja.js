/* A forja com ambiente, as duas direções no jogo (protótipo, 25/10/2026; nada no jogo). Vale com
   html[data-forja="a"] ou "b" (auxiliares/cenario_forja.py, que faz o motor mandar o painel "cena" da forja antes do
   balcão, e serve telas/cenas.js com o registro das cenas à vista: window.__CENAS). Registra forja_a e forja_b (o
   desenho em forja-arte.js) no mesmo sistema dos ambientes da capela: a arte no quadro de cima, os pontos por cima.
   Os dois pontos: "Ferreiro" (leva o foco aos cartões de reforço, embaixo: é com ele que se reforça) e "Saída" (o
   Voltar da forja, a mesma ação do menu). Os nomes dos dois ficam à vista, sem depender do mouse. */
"use strict";

(() => {
  const versao = document.documentElement.dataset.forja;
  if (!versao || !window.__CENAS || !window.ForjaArte) return;
  window.__CENAS.forja_a = window.ForjaArte.a;
  window.__CENAS.forja_b = window.ForjaArte.b;
  if (window.ForjaArte.r) window.__CENAS.forja_r = window.ForjaArte.r;  // a B refinada (forja-r.js)
  if (window.ForjaArte.f) window.__CENAS.forja_f = window.ForjaArte.f;  // a transposição fiel (forja-f.js)
  if (window.ForjaArte.g) window.__CENAS.forja_g = window.ForjaArte.g;  // a F corrigida, na arte do jogo (forja-g.js), a candidata

  // O ponto do ferreiro não tem uma ação só (são até três peças): o clique, o Enter ou o espaço nele levam o foco ao
  // primeiro cartão de reforço que se pode pagar (ou ao primeiro), com a página rolando até ele. Só no protótipo: na
  // integração, as cenas ganhariam esse tipo de ponto ("ir aos serviços").
  document.addEventListener("click", (ev) => {
    const bt = ev.target.closest && ev.target.closest('#pontos-cena .ci-ponto[data-ponto="ferreiro"]');
    if (!bt) return;
    ev.stopPropagation(); ev.preventDefault();
    const cartoes = [...document.querySelectorAll(".forja .servico")];
    const alvo = cartoes.find((c) => !c.classList.contains("caro") && !c.classList.contains("limite")) || cartoes[0];
    if (!alvo) return;
    alvo.scrollIntoView({ block: "nearest" });
    alvo.focus({ preventScroll: true });
    alvo.classList.add("forja-chamado");
    setTimeout(() => alvo.classList.remove("forja-chamado"), 900);
  }, true);
  // o nome lido pelo leitor de tela diz o que o ponto faz aqui
  new MutationObserver(() => {
    const bt = document.querySelector('#pontos-cena .ci-ponto[data-ponto="ferreiro"]');
    if (bt && bt.getAttribute("aria-label") !== "Ferreiro: reforçar o que você usa") bt.setAttribute("aria-label", "Ferreiro: reforçar o que você usa");
  }).observe(document.body, { childList: true, subtree: true });
})();
