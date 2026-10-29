/* A demonstração da taverna (protótipo): com o interior à vista, o balcão inteiro (os cartões e o Voltar à vila) fica
   acima da doca. O jogo (app/vila.js) rola a página uma vez, quando o balcão monta; o texto da página ainda cresce
   depois disso, e a 1280×720 a última linha do balcão ficava 42 px atrás da doca. Aqui a mesma conta se repete quando
   a página muda, só para a frente (nunca volta a rolagem de quem rolou para cima) e só enquanto o balcão couber: o
   topo dele nunca sai da página. Se a taverna for integrada, a conta vai para o vila.js e vale para todo balcão. */
"use strict";

(() => {
  const pagina = document.getElementById("pagina");
  if (!pagina) return;
  function ajustar() {
    const c = document.querySelector(".balcao-predio");
    if (!c || !(window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna")) return;
    const pb = pagina.getBoundingClientRect(), cb = c.getBoundingClientRect();
    const sobra = cb.bottom - pb.bottom + 8;
    if (sobra > 0) pagina.scrollTop += Math.min(sobra, cb.top - pb.top - 4);
  }
  new MutationObserver(() => requestAnimationFrame(ajustar)).observe(pagina, { childList: true, subtree: true });
  new ResizeObserver(() => requestAnimationFrame(ajustar)).observe(pagina);
})();
