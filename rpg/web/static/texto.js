"use strict";
/* Pequenas utilidades de texto da tela (as do motor ficam em rpg/texto.py). */
const Texto = (() => {
  /** "1 trecho", "3 trechos", "0 trechos": o plural certo, nunca com o s entre parênteses. Quando o plural não é só
   *  acrescentar s, ele vai junto: plural(n, "ponto de talento", "pontos de talento"). */
  const plural = (n, um, varios) => `${n} ${n === 1 ? um : varios || um + "s"}`;
  return { plural };
})();
