/* As famílias de desenhos do protótipo (experimento): cada uma põe os desenhos de uma rodada de folhas no lugar dos
   ícones do jogo, pelo papel e pelo tipo que o motor já manda. Cada tabela diz o que tem desenho; o que não está nela
   continua com o ícone atual do jogo (as lacunas estão no LEIA-ME). Um sprite do jogo pode ter mais de um papel (a
   "chama" é o Vigor no topo, o Poder nos atributos e a Pena de Fênix na bolsa): por isso a troca é pelo papel, nunca
   só pelo nome.
     Icones4c: HUD 4 completa (assets4c/, preparar_hud4c.py), como foi avaliada.
     Icones4p: HUD 4 pixel (assets4p/, preparar_hud4p.py), a família de ferro com contorno duro. */
"use strict";

/** De onde os desenhos vêm: no protótipo, a própria pasta; no jogo com a HUD experimental (jogo/ligar.js),
 *  "/experimento/". */
const RAIZ_ICONES = window.HUD_RAIZ || "";

function familiaDeIcones(cfg) {
  const DIR = RAIZ_ICONES + cfg.DIR;
  const { ITEM, VAZIO, BOLSA, ATRIBUTO, RECURSO, VITAL, ATALHO, LUGAR, RETRATO } = cfg;
  const CABECA = cfg.CABECA || {}, RODA = cfg.RODA || {};
  const src = (peca, lado) => `${DIR}${peca}-${lado}.png`;
  const srcset = (peca, lado) => `${DIR}${peca}-${lado}@2x.png 2x`;
  /** A marcação de um desenho no tamanho de uso (um arquivo por tamanho, e o dobro para telas densas). Com `estreito`,
   *  outro tamanho (outro arquivo) quando a janela tem até 1400 px de largura. */
  const img = (peca, lado, alt = "", estreito = 0) => {
    const i = `<img class="novo4c" src="${src(peca, lado)}" srcset="${srcset(peca, lado)}" width="${lado}" height="${lado}" alt="${alt}" draggable="false">`;
    return estreito ? `<picture class="novo4c"><source media="(max-width: 1400px)" srcset="${src(peca, estreito)}, ${srcset(peca, estreito)}">${i}</picture>` : i;
  };
  /** O retrato da ficha: 80 px, 64 em telas baixas (o mesmo corte do quadro da HUD 4). Só a classe que tem retrato. */
  const retrato = (classe, alt) => RETRATO[classe] ? `<picture class="novo4c">
      <source media="(max-height: 800px)" srcset="${DIR}${RETRATO[classe]}-64.png, ${DIR}${RETRATO[classe]}-64@2x.png 2x">
      <img class="original" src="${DIR}${RETRATO[classe]}-80.png" srcset="${DIR}${RETRATO[classe]}-80@2x.png 2x" alt="${alt}" draggable="false"></picture>` : "";
  /** A cabeça do mesmo retrato, para os lugares pequenos (o topo, a carta da luta). */
  const cabeca = (classe, lado) => (CABECA[classe] ? img(CABECA[classe], lado) : "");

  // ------------------------------------------------------------ a fotografia do jogo (doca, caminhos, janela, luta)
  // O sprite de uma imagem fotografada, reconhecido pelo próprio desenho (o mesmo data URL que Sprites.url gera).
  let porUrl = null;
  function nomeDoSprite(s) {
    if (!porUrl) {
      porUrl = {};
      for (const n of [...Object.keys(LUGAR), ...Object.keys(ITEM), ...Object.keys(RODA), ...Object.keys(CABECA)]) {
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
  /** Liga os desenhos desta família no que veio fotografado do jogo (depois de `Icones.desligar`). */
  function aplicar() {
    document.querySelectorAll("#doca .atalho").forEach((b) => {
      const nome = ((b.querySelector(".atalho-nome") || {}).textContent || "").trim(), el = b.querySelector(".atalho-icone img");
      if (el && ATALHO[nome]) trocar(el, ATALHO[nome], cfg.ladoAtalho);
    });
    document.querySelectorAll("#mundo .caminho > img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src"));
      if (LUGAR[n]) trocar(el, LUGAR[n], 40);
    });
    // a janela do anel achado: os itens dos cartões (o achado e o que está vestido em cada espaço)
    document.querySelectorAll("#sobre-achado img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src")), w = Number(el.getAttribute("width"));
      if (ITEM[n]) trocar(el, ITEM[n], [64, 48, 32].find((l) => w >= l) || 32);
    });
    // a luta: as ações da roda (pelo desenho que o jogo pôs nelas) e o rosto do herói na carta dele
    document.querySelectorAll("#roda .rb-icone img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src"));
      if (RODA[n]) trocar(el, RODA[n], 32);
    });
    document.querySelectorAll(".carta.heroi .icone img").forEach((el) => {
      const n = nomeDoSprite(el.getAttribute("src"));
      if (CABECA[n]) trocar(el, CABECA[n], 32);
    });
  }

  return { img, retrato, cabeca, aplicar, src, srcset, nomeDoSprite, ladoAtalho: cfg.ladoAtalho,
    ITEM, VAZIO, BOLSA, ATRIBUTO, RECURSO, VITAL, ATALHO, LUGAR, RETRATO, CABECA, RODA };
}

const Icones = {
  /** Volta tudo o que foi trocado na fotografia ao desenho do jogo. */
  desligar() {
    document.querySelectorAll("img[data-orig]").forEach((el) => {
      el.src = el.dataset.orig;
      el.removeAttribute("srcset");
      if (el.dataset.origLado) el.width = el.height = Number(el.dataset.origLado);
      el.setAttribute("style", el.dataset.origEstilo);
      el.classList.remove("novo4c");
      delete el.dataset.orig; delete el.dataset.origLado; delete el.dataset.origEstilo;
    });
  },
};

const ATALHOS = (pref) => ({ Talentos: `${pref}talentos`, "Grimório": `${pref}grimorio`, "Inventário": `${pref}inventario`,
  Mapa: `${pref}mapa`, "Diário": `${pref}diario`, "Bestiário": `${pref}bestiario`, Salvar: `${pref}salvar`, Sair: `${pref}sair` });

// HUD 4 completa: as peças novas são de couro, então vão só para os tipos de couro (o jogo separa couro de ferro pela
// cor do mesmo desenho: calca e calca_couro, bota e bota_ferro, armadura e gibao). O espaço vazio mostra a silhueta
// apagada (sem cor) do que vai nele: aí o material não aparece. O topo troca só os recursos com estoque; o Vigor ganha o
// raio dourado, da cor da barra dele. Os caminhos seguem o desenho que o jogo escolhe para o destino (MapaPx.sprite).
const Icones4c = familiaDeIcones({
  DIR: "assets4c/exibicao/", ladoAtalho: 36,
  ITEM: { espada: "espada", escudo: "escudo", capuz: "capuz", gibao: "armadura-couro", calca_couro: "calca-couro",
    bota: "botas", amuleto: "amuleto", anel: "anel-azul", aljava: "aljava" },
  VAZIO: { cabeca: "capuz", armadura: "armadura-couro", pernas: "calca-couro", pes: "botas", arma: "espada",
    secundaria: "escudo", amuleto: "amuleto", anel1: "anel-azul", anel2: "anel-azul" },
  BOLSA: { pocao_vida: "pocao", bandagem: "bandagem", tocha: "tocha" },
  ATRIBUTO: { Ataque: "attr-ataque", Defesa: "attr-defesa", Agilidade: "attr-agilidade", Poder: "attr-poder" },
  RECURSO: { pernil: "provisoes", tocha: "tocha", moedas: "moedas", pocao: "pocao", bandagem: "bandagem" },
  VITAL: { Vida: "vital-vida", Vigor: "vital-vigor" },
  ATALHO: ATALHOS("atalho-"),
  LUGAR: { vila: "lugar-vila", floresta: "lugar-floresta", pantano: "lugar-pantano", ruinas: "lugar-ruinas",
    montanha: "lugar-montanha" },
  RETRATO: { guerreiro: "retrato-guerreiro" },
});

// HUD 4 pixel: a família de ferro. Cada desenho vai para o tipo de ferro que o jogo já tem (elmo, armadura, manopla,
// calca = perneira, bota_ferro, maca); couro (capuz, gibão, calça de couro, bota de caça, luva) e as armas sem desenho
// (machado, martelo, arco...) ficam com o do jogo. O anel tem uma pérola branca: não lembra nenhuma cor de raridade.
// Sem comida, o osso (o desenho de "acabou" que o jogo já usa); a tocha apagada, a bolsa vazia e o frasco vazio ficam.
// O covil (a toca do guardião) ganha a caverna; o covil vencido continua a bandeira do jogo. O retrato é do Guerreiro:
// o busto na ficha e a cabeça no topo e na carta da luta; as outras classes ficam com o desenho delas.
const Icones4p = familiaDeIcones({
  DIR: "assets4p/exibicao/", ladoAtalho: 36,
  ITEM: { elmo: "elmo", armadura: "cota", manopla: "manopla", calca: "perneiras", bota_ferro: "botas-ferro",
    maca: "maca", espada: "espada", escudo: "escudo", amuleto: "amuleto", anel: "anel", aljava: "aljava" },
  VAZIO: { cabeca: "elmo", armadura: "cota", maos: "manopla", pernas: "perneiras", pes: "botas-ferro", arma: "espada",
    secundaria: "escudo", amuleto: "amuleto", anel1: "anel", anel2: "anel" },
  BOLSA: { pocao_vida: "pocao", tonico: "tonico", antidoto: "antidoto", bandagem: "bandagem", bau: "bau", tocha: "tocha" },
  ATRIBUTO: { Ataque: "attr-ataque", Defesa: "attr-defesa", Agilidade: "attr-agilidade", Poder: "attr-poder" },
  RECURSO: { pernil: "provisoes", osso_diag: "osso", tocha: "tocha", moedas: "moedas", pocao: "pocao", bandagem: "bandagem",
    aljava: "aljava" },  // a aljava: as flechas do Patrulheiro
  VITAL: { Vida: "vital-vida", Vigor: "vital-vigor", Mana: "vital-mana", Foco: "vital-foco" },
  ATALHO: ATALHOS("atalho-"),
  LUGAR: { vila: "lugar-vila", floresta: "lugar-floresta", pantano: "lugar-pantano", ruinas: "lugar-ruinas",
    montanha: "lugar-montanha", planicie: "lugar-planicie", cidadela: "lugar-cidadela", covil: "lugar-caverna" },
  RETRATO: { guerreiro: "retrato-guerreiro" },
  CABECA: { guerreiro: "cabeca-guerreiro" },
  // a roda da luta: o ataque da classe (a espada do Guerreiro), Habilidades (o grimório), Itens (a poção) e Fugir (a
  // bota com os riscos de movimento, a mesma da Agilidade: correr, não a porta do Sair do jogo)
  RODA: { espada: "espada", grimorio: "atalho-grimorio", pocao: "pocao", fuga: "attr-agilidade" },
});
