/* HUD 4 completa (experimento): os desenhos das quatro folhas novas (assets4c/, preparar_hud4c.py) no lugar dos ícones
   do jogo, pelo papel e pelo tipo que o motor já manda. Cada tabela diz o que tem desenho; o que não está nela continua
   com o ícone atual do jogo (as lacunas estão no LEIA-ME). Um sprite do jogo pode ter mais de um papel (a "chama" é o
   Vigor no topo, o Poder nos atributos e a Pena de Fênix na bolsa): por isso a troca é pelo papel, nunca só pelo nome. */
"use strict";

const Icones4c = (() => {
  const DIR = "assets4c/exibicao/";
  // Os itens pelo ícone que o motor manda (itens.py: icone_de). O jogo separa couro de ferro pela cor do mesmo
  // desenho (calca e calca_couro, bota e bota_ferro, armadura e gibao): as peças novas são de couro, então vão só para
  // os tipos de couro. Elmo, cota, manopla, perneira de ferro, bota ferrada, maça, machado e martelo não têm desenho.
  const ITEM = { espada: "espada", escudo: "escudo", capuz: "capuz", gibao: "armadura-couro", calca_couro: "calca-couro",
    bota: "botas", amuleto: "amuleto", anel: "anel-azul", aljava: "aljava" };
  // O espaço vazio mostra a silhueta apagada (sem cor) do que vai nele: aí o material não aparece.
  const VAZIO = { cabeca: "capuz", armadura: "armadura-couro", pernas: "calca-couro", pes: "botas", arma: "espada",
    secundaria: "escudo", amuleto: "amuleto", anel1: "anel-azul", anel2: "anel-azul" };
  const BOLSA = { pocao_vida: "pocao", bandagem: "bandagem", tocha: "tocha" };
  const ATRIBUTO = { Ataque: "attr-ataque", Defesa: "attr-defesa", Agilidade: "attr-agilidade", Poder: "attr-poder" };
  // O topo: só os recursos com estoque (o desenho de "acabou" continua o do jogo: osso, tocha apagada, bolsa vazia,
  // frasco vazio). O Vigor ganha o raio dourado, da cor da barra dele; Mana e Foco ficam como estão.
  const RECURSO = { pernil: "provisoes", tocha: "tocha", moedas: "moedas", pocao: "pocao", bandagem: "bandagem" };
  const VITAL = { Vida: "vital-vida", Vigor: "vital-vigor" };
  const ATALHO = { Talentos: "atalho-talentos", "Grimório": "atalho-grimorio", "Inventário": "atalho-inventario",
    Mapa: "atalho-mapa", "Diário": "atalho-diario", "Bestiário": "atalho-bestiario", Salvar: "atalho-salvar",
    Sair: "atalho-sair" };
  // Os caminhos pelo desenho que o jogo escolhe para o destino (mapa.js: MapaPx.sprite). Planície, cidadela, covil
  // (a caveira do perigo) e vencido (a bandeira) não têm par; a cripta da folha não tem destino que a use.
  const LUGAR = { vila: "lugar-vila", floresta: "lugar-floresta", pantano: "lugar-pantano", ruinas: "lugar-ruinas",
    montanha: "lugar-montanha" };
  // O retrato de demonstração é do Guerreiro: as outras classes ficam com o desenho delas.
  const RETRATO = { guerreiro: "retrato-guerreiro" };

  // A doca: 36 px dentro da caixa de 38 do ícone (a barra não cresce); em 32 os desenhos escuros (a mochila, o
  // grimório, a carteira) somem no carvão.
  let LADO_ATALHO = 36;
  const src = (peca, lado) => `${DIR}${peca}-${lado}.png`;
  const srcset = (peca, lado) => `${DIR}${peca}-${lado}@2x.png 2x`;
  /** A marcação de um desenho no tamanho de uso (um arquivo por tamanho, e o dobro para telas densas). Com `estreito`,
   *  outro tamanho (outro arquivo) quando a janela tem até 1400 px de largura. */
  const img = (peca, lado, alt = "", estreito = 0) => {
    const i = `<img class="novo4c" src="${src(peca, lado)}" srcset="${srcset(peca, lado)}" width="${lado}" height="${lado}" alt="${alt}" draggable="false">`;
    return estreito ? `<picture class="novo4c"><source media="(max-width: 1400px)" srcset="${src(peca, estreito)}, ${srcset(peca, estreito)}">${i}</picture>` : i;
  };
  /** O retrato: 80 px, 64 em telas baixas (o mesmo corte do quadro da HUD 4). */
  const retrato = (classe, alt) => RETRATO[classe] ? `<picture class="novo4c">
      <source media="(max-height: 800px)" srcset="${DIR}${RETRATO[classe]}-64.png, ${DIR}${RETRATO[classe]}-64@2x.png 2x">
      <img class="original" src="${DIR}${RETRATO[classe]}-80.png" srcset="${DIR}${RETRATO[classe]}-80@2x.png 2x" alt="${alt}" draggable="false"></picture>` : "";

  // ------------------------------------------------------------ a fotografia do jogo (doca, caminhos, janela)
  // O sprite de uma imagem fotografada, reconhecido pelo próprio desenho (o mesmo data URL que Sprites.url gera).
  let porUrl = null;
  function nomeDoSprite(s) {
    if (!porUrl) {
      porUrl = {};
      for (const n of [...Object.keys(LUGAR), ...Object.keys(ITEM)]) {
        if (!Sprites.existe(n)) continue;
        porUrl[Sprites.url(n)] = n;
        porUrl[Sprites.url(n, true)] = n;
      }
    }
    return porUrl[s];
  }
  function trocar(el, peca, lado) {
    if (!el.dataset.orig) {
      el.dataset.orig = el.getAttribute("src");
      el.dataset.origLado = el.getAttribute("width") || "";
      el.dataset.origEstilo = el.getAttribute("style") || "";
    }
    el.src = src(peca, lado);
    el.srcset = srcset(peca, lado);
    el.width = el.height = lado;
    el.style.setProperty("--s", String(lado));
    el.classList.add("novo4c");
  }
  function restaurar(el) {
    el.src = el.dataset.orig;
    el.removeAttribute("srcset");
    if (el.dataset.origLado) { el.width = el.height = Number(el.dataset.origLado); }
    el.setAttribute("style", el.dataset.origEstilo);
    el.classList.remove("novo4c");
    delete el.dataset.orig; delete el.dataset.origLado; delete el.dataset.origEstilo;
  }
  /** Liga (ou desliga) os desenhos novos no que veio fotografado do jogo. */
  function aplicar(ligado) {
    document.querySelectorAll("img[data-orig]").forEach(restaurar);
    if (!ligado) return;
    document.querySelectorAll("#doca .atalho").forEach((b) => {
      const nome = (b.querySelector(".atalho-nome") || {}).textContent, el = b.querySelector(".atalho-icone img");
      if (el && ATALHO[(nome || "").trim()]) trocar(el, ATALHO[nome.trim()], LADO_ATALHO);
    });
    document.querySelectorAll("#mundo .caminho > img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src"));
      if (LUGAR[n]) trocar(el, LUGAR[n], 40);
    });
    // a janela do anel achado: os itens dos cartões (o achado e o que está vestido em cada espaço)
    document.querySelectorAll("#sobre-achado img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src"));
      const w = Number(el.getAttribute("width"));
      if (ITEM[n]) trocar(el, ITEM[n], [64, 48, 32].find((l) => w >= l) || 32);
    });
  }

  return { img, retrato, aplicar, set ladoAtalho(v) { LADO_ATALHO = v; }, ITEM, VAZIO, BOLSA, ATRIBUTO, RECURSO, VITAL };
})();
