/* O experimento de itens e ícones: veste o jogo de verdade com os candidatos de itens-icones-teste.js, só para as
   fotografias (fotografar_itens_icones.mjs e fotografar_roda.mjs põem este arquivo na página; o jogo não o carrega).
   Troca a <img> pelo papel, como o Icones faria, sem mexer em tamanho, lugar, nome, atalho nem área clicável:
   - espada, escudo, anel: o desenho do item onde ele aparecer (bolsa, corpo, prateleira, saque, e a espada também no
     Atacar do Guerreiro, que é o mesmo desenho);
   - machado: o sprite do jogo nos espaços de item;
   - unguento e bomba de fumaça: só onde o item é o assunto (o espaço da bolsa, a linha da janelinha de Itens, a
     prateleira), porque o jogo usa o mesmo sprite para a curandeira (unguento) e para a morte, o bestiário e o Largar
     (caveira);
   - Grimório e Talentos: o atalho da doca e o Habilidades da roda; Ataque e Defesa: os atributos da ficha; Fugir: a
     bota da roda (a da Agilidade, na ficha, fica).
   Cada candidato vai na escala inteira do desenho quando cabe (32 em 32, 64 em 64), e na de 2× reduzida pelo navegador
   nos outros tamanhos (48), como o Icones faz com o martelo e a Pena. */
"use strict";

(() => {
  const ARQ = (nome) => new RegExp(`/hud/icones/${nome}-\\d+(@2x)?\\.png$`);
  const tem = (n) => !!ArteTeste.PECAS[n];
  const lado = (i) => i.width || parseInt(i.getAttribute("width"), 10) || 32;
  // o candidato de `nome` mais perto de `l` px (Ataque e Defesa têm 24 e 32; Grimório e Talentos, 32 e 36)
  const peca = (nome, l) => [`cand-${nome}-${l}`, `cand-${nome}-32`, `cand-${nome}-24`, `cand-${nome}-36`].find(tem);
  function vestir(i, nome) {
    const l = lado(i), p = peca(nome, l), n = ArteTeste.PECAS[p].grade.length;
    const inteira = l % n === 0, e = inteira ? l / n : Math.ceil(l / n);
    i.src = ArteTeste.url(p, e);
    i.srcset = `${ArteTeste.url(p, 2 * e)} 2x`;
    i.width = i.height = l;
    i.style.imageRendering = inteira ? "pixelated" : "auto";
    i.classList.add("arte-teste");
  }
  const DO_ITEM = ".slot-px:not(.lixeira), .rj-linha, .mercadoria, .prateleira *, .item-cartao, .saque *, .espolio *";
  const assunto = (i, texto) => {
    const c = i.closest(DO_ITEM);
    if (!c) return false;
    // quem diz o item: o id na bolsa, no uso ou na compra; senão a linha ou o espaço em volta
    const alvo = i.closest("[data-bolsa], [data-usar], [data-comprar], .rj-linha, .mercadoria") || i.closest(".slot-px, li, [title]") || c;
    return texto.test(`${alvo.textContent} ${alvo.getAttribute("title") || ""} ${i.alt || ""} ${alvo.dataset ? Object.values(alvo.dataset).join(" ") : ""}`);
  };
  // o sprite do jogo, com ou sem a sombra (o mercado usa a versão com sombra)
  const sprite = (s, nome) => s === Sprites.url(nome) || s === Sprites.url(nome, true);
  function trocar(i) {
    const s = i.getAttribute("src") || "";
    const naRoda = !!i.closest(".roda-botao");
    if (ARQ("espada").test(s)) return vestir(i, "espada");
    if (ARQ("escudo").test(s)) return vestir(i, "escudo");
    if (ARQ("anel").test(s)) return vestir(i, "anel");
    if (ARQ("atalho-grimorio").test(s)) return vestir(i, "grimorio");
    if (ARQ("atalho-talentos").test(s)) return vestir(i, "talentos");
    if (ARQ("attr-ataque").test(s)) return vestir(i, "ataque");
    if (ARQ("attr-defesa").test(s)) return vestir(i, "defesa");
    if (naRoda && ARQ("attr-agilidade").test(s)) return vestir(i, "fugir");
    if (sprite(s, "machado") && i.closest(DO_ITEM)) return vestir(i, "machado");
    if (sprite(s, "unguento") && assunto(i, /unguento/i)) return vestir(i, "unguento");
    if (sprite(s, "caveira") && assunto(i, /bomba de fumaça|bomba_fumaca/i)) return vestir(i, "bomba");
  }
  const tudo = () => document.querySelectorAll("img:not(.arte-teste)").forEach(trocar);
  new MutationObserver(tudo).observe(document.body, { childList: true, subtree: true });
  tudo();
})();
