/* HUD experimental no jogo de verdade (teste, fora da interface padrão). O servidor só põe este script na página com
   o pedido explícito (python jogar.py --hud-experimental, ou HUD=experimental nos cenários de teste); a escolha não vai
   para o save. Tudo continua sendo o jogo: o motor, as telas e os componentes de sempre. Daqui saem só os estilos da
   HUD 4 pixel (os mesmos do protótipo) e a troca dos desenhos pelo papel de cada um (icones.js: Icones4p). */
"use strict";
window.HUD_RAIZ = "/experimento/";
(() => {
  const ESTILOS = ["hud3.css", "hud4.css", "hud4c.css", "hud4p.css", "hud4p-luta.css",
    "jogo/jogo.css", "jogo/telas.css", "jogo/superficies.css"];
  for (const arquivo of ESTILOS) {
    const l = document.createElement("link");
    l.rel = "stylesheet"; l.href = window.HUD_RAIZ + arquivo;
    document.head.appendChild(l);
  }
  // v3 v4 v4c v4p: a HUD 4 pixel parte da completa, que parte da 4, que parte da 3 (como no protótipo)
  document.body.classList.add("v3", "v4", "v4c", "v4p", "hud-experimental");
  // os materiais de ferro (jogo/materiais.js), os controles de teste (jogo/desenvolvimento.js), icones.js (as
  // famílias), o índice dos tamanhos que existem e, por fim, a troca pelos papéis (jogo/papeis.js)
  const carregar = (arquivos) => {
    if (!arquivos.length) return;
    const s = document.createElement("script");
    s.src = window.HUD_RAIZ + arquivos[0];
    s.onload = () => carregar(arquivos.slice(1));
    document.head.appendChild(s);
  };
  carregar(["jogo/materiais.js", "jogo/desenvolvimento.js", "icones.js", "assets4p/exibicao/indice.js",
    "jogo/papeis.js"]);
})();
