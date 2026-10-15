/* O teste do Unguento de Prata (experimento): veste o jogo de verdade com o primeiro candidato (desenhar_itens.py, pela
   ArteTeste) ou com uma proposta em pixel art (a pasta e os lados dela), só para as fotografias (fotografar_unguento.mjs
   põe este arquivo na página; o jogo não o carrega). window.UNGUENTO_TESTE diz qual: { versao, pasta, lados }.
   Troca a <img> só onde o unguento é o assunto (o espaço da bolsa, a prateleira do mercado, a linha da janelinha de
   Itens): o mesmo sprite é o da curandeira, que fica. Sem mexer em tamanho, lugar, nome nem área clicável.
   A proposta vai no arquivo do tamanho quando ele existe e o dobro no srcset; nos outros tamanhos, o
   arquivo maior mais perto, reduzido pelo navegador (como o Icones faz com o martelo e a Pena). */
"use strict";

(() => {
  const versao = (window.UNGUENTO_TESTE || {}).versao;
  if (!versao) return;
  const DO_ITEM = ".slot-px:not(.lixeira), .rj-linha, .mercadoria, .prateleira *, .item-cartao, .saque *, .espolio *";
  const assunto = (i) => {
    const c = i.closest(DO_ITEM);
    if (!c) return false;
    const alvo = i.closest("[data-bolsa], [data-usar], [data-comprar], .rj-linha, .mercadoria") || i.closest(".slot-px, li, [title]") || c;
    return /unguento/i.test(`${alvo.textContent} ${alvo.getAttribute("title") || ""} ${i.alt || ""} ${alvo.dataset ? Object.values(alvo.dataset).join(" ") : ""}`);
  };
  const sprite = (s) => s === Sprites.url("unguento") || s === Sprites.url("unguento", true);
  const lado = (i) => i.width || parseInt(i.getAttribute("width"), 10) || 32;
  function vestir(i) {
    const l = lado(i);
    if (versao === "primeiro") {
      const n = ArteTeste.PECAS["cand-unguento-32"].grade.length, inteira = l % n === 0, e = inteira ? l / n : Math.ceil(l / n);
      i.src = ArteTeste.url("cand-unguento-32", e);
      i.srcset = `${ArteTeste.url("cand-unguento-32", 2 * e)} 2x`;
      i.style.imageRendering = inteira ? "pixelated" : "auto";
    } else {
      const { pasta, lados } = window.UNGUENTO_TESTE, f = lados.find((t) => t >= l) || lados[lados.length - 1];
      i.src = `/__prototipo/${pasta}/unguento-${f}.png`;
      i.srcset = `/__prototipo/${pasta}/unguento-${f}@2x.png 2x`;
      i.style.imageRendering = f === l ? "pixelated" : "auto";
    }
    i.width = i.height = l;
    i.classList.add("unguento-teste");
    (window.__unguentos = window.__unguentos || []).push(l);
  }
  const tudo = () => document.querySelectorAll("img:not(.unguento-teste)").forEach((i) => {
    if (sprite(i.getAttribute("src") || "") && assunto(i)) vestir(i);
  });
  new MutationObserver(tudo).observe(document.body, { childList: true, subtree: true });
  tudo();
})();
