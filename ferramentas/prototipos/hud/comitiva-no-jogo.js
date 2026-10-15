/* Teste da comitiva (experimento): veste Morel, Odette e Yara no jogo de verdade com os candidatos de arte-teste.js, só
   para a comparação (fotografar_comitiva.mjs põe este arquivo na página depois de abrir um cenário). O jogo não carrega
   este arquivo: em produção eles seguem com os sprites de sempre. Toda <img> do sprite de um deles (o painel, a tela
   da Comitiva, a carta da luta, o cartão da reação, a faixa de quem chega, o selo da aprovação) troca pelo candidato no
   mesmo tamanho: até 40 px, a versão de 16×16 (a carta); maior, a cabeça (o recorte de 24×24). Na fogueira, a figura
   de 16×16 que Icones.figura dá passa a ser a carta do candidato. Um observador refaz a troca a cada redesenho. */
"use strict";

(() => {
  const PECA = { morel: "morel", odete: "odette", yara: "yara" };  // o id do companheiro no jogo → a peça do teste
  const srcs = {};
  Object.keys(PECA).forEach((id) => { srcs[Sprites.url(id)] = id; srcs[Sprites.url(id, true)] = id; });
  function vestir() {
    document.querySelectorAll("img:not(.arte-teste)").forEach((i) => {
      const id = srcs[i.getAttribute("src")];
      if (!id) return;
      const lado = i.width || parseInt(i.getAttribute("width"), 10) || 32;
      const peca = lado <= 40 ? `${PECA[id]}-carta` : `${PECA[id]}-cabeca`;
      const base = ArteTeste.PECAS[peca].grade.length, e = Math.max(1, Math.round(lado / base));
      i.src = ArteTeste.url(peca, e);
      i.srcset = `${ArteTeste.url(peca, e * 2)} 2x`;
      i.width = i.height = base * e;
      i.style.setProperty("--s", base * e);
      i.classList.add("arte-teste");
    });
  }
  // a fogueira pinta em canvas: a figura de 16×16 de cada um passa a ser a carta do candidato
  const figura = Icones.figura, telas = {};
  Icones.figura = (nome) => (PECA[nome] ? (telas[nome] = telas[nome] || ArteTeste.canvas(`${PECA[nome]}-carta`, 1)) : figura(nome));
  document.head.insertAdjacentHTML("beforeend", "<style>img.arte-teste { image-rendering: pixelated; }</style>");
  new MutationObserver(vestir).observe(document.body, { childList: true, subtree: true });
  vestir();
})();
