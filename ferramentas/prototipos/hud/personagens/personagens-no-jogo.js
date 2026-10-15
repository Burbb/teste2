/* A proposta no jogo de verdade, só para as fotografias (fotografar_personagens.mjs acrescenta este arquivo e
   personagens-teste.js ao fim de /static/retratos.js na página; o jogo não os carrega). window.PERSONAGENS =
   { versao: "atual" | "candidata" }. Na candidata, só três papéis mudam, e só onde a tela pede aquele papel:
   - a carta do Morel (32 px: a carta da luta, o painel da comitiva, o aviso): a de 16×16, a 2×;
   - a cabeça do Morel (48 px: os cartões da Comitiva, de quem chega e da reação): a de 24×24, a 2×;
   - a figura do Mago na fogueira (o canvas de 16×16): a sentada. O chip de 16 px do texto (Retratos.url) não muda.
   O busto, a ficha baixa e a figura do Morel, e todos os outros retratos, ficam como estão. */
"use strict";
(() => {
  if (!window.PERSONAGENS || window.PERSONAGENS.versao !== "candidata") return;
  const T = window.PersonagensTeste, R = Retratos;
  const tem = (n, p) => !!(T[n] && T[n][p]);
  const { url, canvas, lado } = R;
  R.lado = (n, p) => (tem(n, p) ? T[n][p].length : lado(n, p));
  R.url = (n, p, e) => (tem(n, p) && p !== "figura" ? Sprites.grade(`teste-${n}-${p}`, T[n][p], T[n].cores, e) : url(n, p, e));
  R.canvas = (n, p, e = 1) => (tem(n, p) && p === "figura" ? Sprites.gradeCanvas(`teste-${n}-${p}`, T[n][p], T[n].cores, e) : canvas(n, p, e));
})();
