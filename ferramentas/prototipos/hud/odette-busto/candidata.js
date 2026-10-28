/* Candidata do busto da Odette (40×40): o rosto, a touca e a cruz iguais aos de retratos.js; mudam só os ombros, o
   véu e a base (linhas 21 a 39). Os ombros caem do véu um pixel por linha em vez de dois (a largura vai de 38 para 32
   pixels), o hábito abre devagar em vez do salto da linha 31 e os cantos de baixo recolhem um pixel. O jogo não
   carrega este arquivo: fotografar.mjs o põe na página depois de abrir o cenário e troca o busto do boneco do
   Inventário (80 px; 64 em janela baixa, pelo mesmo recorte de retratos.js), para comparar com os mesmos dados. */
"use strict";

(() => {
  const CORES = { P: "#c8a088", Q: "#58402c", U: "#18140f", V: "#4a423c", W: "#d8ccb2", Y: "#a68c48", e: "#20160f", o: "#76584a", p: "#a47e68", q: "#8a806c", u: "#26211d", v: "#352f2a", w: "#b4a890", y: "#6e5c32" };
  const GRADE = [
    "........................................",
    "........................................",
    "........................................",
    "...............vvvvvvvvuu...............",
    ".............VVvvvvvvvvuuuU.............",
    "............VVVWWWWwwwwwquUU............",
    "............VVWWWWWwwwwwqqUU............",
    "............VVWWWWWwwwwwqqUU............",
    "............VVWWPPppppooqqUU............",
    "............VVWPPPppppoooqUU............",
    "............VVWPppppppoooqUU............",
    "............VVWPPeppppeooqUU............",
    "............VVWPPPpPppoooqUU............",
    "............VVWPPPppopoooqUU............",
    "............VVWPPPppppoooqUU............",
    "............VVWPPPpoopoooqUU............",
    "...........VVVWWPPppppooqqUUU...........",
    "...........VVVWWWPppppowqqUUU...........",
    "...........VVVWWWWppppwwqqUUU...........",
    "...........VVVWWWqqqqqqwqqUUU...........",
    "..........VVVVWWWWWwwwwwqqUUUU..........",
    ".........VVVVVVWWWWWwwwwwuUUUUU.........",
    "........VVvVVVVvWWWWwwwwuuUUUUuU........",
    ".......VVvVVVVVvWWWWwwwwuuUUUUuUU.......",
    "......VVVvVVVVVvvWWWwwwuuuUUUUuUUU......",
    ".....VVVVvVVVVVvvvWWwwuuuuUUUUuUUUU.....",
    ".....VVVVvVVVVVvvvvvvvuuuuUUUUuUUUU.....",
    "....QVVVVvVVVVVvvvvYvvuuuuUUUUuUUUUU....",
    ".....QVVVVVVVVVvvvYYyvuuuuUUUUuUUUUU....",
    "....QVVVVVVVVVVvvvvYvvuuuuUUUUuUUUUU....",
    "....QQVVVVVVVVVvvvvyvvuuuuUUUUuUUUUU....",
    "....VVVVVVVVVVvvvvvvvvuuuuuUUUuUUUUU....",
    "....VVVVVVVVVvvvvvvvvvuuuuuuUUuUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    "....VVVVVVVVvvvvvvvvvvuuuuuuuUUUUUUU....",
    ".....VVVVVVVvvvvvvvvvvuuuuuuuUUUUUU.....",
  ];
  const baixo = GRADE.slice(1, 33).map((l) => l.slice(4, 36));
  const url = (nome, grade, lado, x) => Sprites.grade(`odette-cand-${nome}`, grade, CORES, (x * lado) / grade.length);
  function vestir() {
    const aba = document.querySelector('.grupo-abas .grupo-aba[data-aba="odete"]');
    if (!aba || !aba.classList.contains("ativa")) return;
    const r = document.querySelector(".boneco-retrato");
    if (!r || r.querySelector(".candidata")) return;
    const alt = (r.querySelector("img") || {}).alt || "";
    r.innerHTML = `<picture class="desenho pixel candidata"><source media="(max-height: 800px)" srcset="${url("baixo", baixo, 64, 1)}, ${url("baixo", baixo, 64, 2)} 2x">` +
      `<img class="original" src="${url("busto", GRADE, 80, 1)}" srcset="${url("busto", GRADE, 80, 2)} 2x" alt="${alt}" draggable="false"></picture>`;
  }
  new MutationObserver(vestir).observe(document.body, { childList: true, subtree: true });
  vestir();
  window.OdetteCandidata = { GRADE, CORES };
})();
