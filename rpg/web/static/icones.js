/* Os desenhos da interface (hud/icones/): a família de ferro da HUD, pelo papel de cada imagem. As telas pedem aqui o
   desenho de um papel (o item pelo desenho que o motor dá, o consumível pelo id, o atributo, o recurso do topo, o
   vital, o atalho da doca, o lugar de um caminho, a ação da roda, o retrato do herói ou de um companheiro) e recebem a
   <img> pronta, ou ""
   quando a família não tem aquele desenho: aí a tela usa o sprite do jogo, como sempre. O retrato e a cabeça do herói
   vêm de retratos.js (desenhados em código, como as cenas), não de arquivo. É o único lugar que sabe qual
   desenho vai em cada papel; a origem e o destino de uma animação (o item que voa da mochila para o corpo, o baú que
   cai na bolsa) pedem o mesmo e saem iguais.
   Um sprite pode ter mais de um papel (a "chama" é o Vigor no topo, o Poder nos atributos e a Pena de Fênix na bolsa):
   por isso a escolha é pelo papel, nunca só pelo nome. Os desenhos vêm prontos nos tamanhos de uso (reduzidos das
   folhas aprovadas por ferramentas/prototipos/hud/preparar_hud4p.py), cada um com o dobro para telas densas; pedido um
   lado sem arquivo igual, vai o mais perto. As lacunas (o que ainda não tem desenho) estão em docs/ARQUITETURA.md. */
"use strict";

const Icones = (() => {
  const DIR = "/static/hud/icones/";
  // os lados que existem de cada peça (sem os @2x, que existem para todos)
  const TAMANHOS = {"aljava": [24, 32, 48, 64], "amuleto": [32, 48, 64], "anel": [32, 48, 64], "antidoto": [32, 48, 64],
    "atalho-bestiario": [32, 36], "atalho-diario": [32, 36], "atalho-grimorio": [32, 36], "atalho-inventario": [32, 36],
    "atalho-mapa": [32, 36], "atalho-sair": [32, 36], "atalho-salvar": [32, 36], "atalho-talentos": [32, 36],
    "attr-agilidade": [24, 32], "attr-ataque": [24, 32], "attr-defesa": [24, 32], "attr-poder": [24, 32],
    "bandagem": [24, 32, 48, 64], "bau": [32, 48, 64], "botas-ferro": [32, 48, 64],
    "cota": [32, 48, 64], "elmo": [32, 48, 64], "escudo": [32, 48, 64], "espada": [32, 48, 64], "lugar-caverna": [32, 40],
    "lugar-cidadela": [32, 40], "lugar-floresta": [32, 40], "lugar-montanha": [32, 40], "lugar-pantano": [32, 40],
    "lugar-planicie": [32, 40], "lugar-ruinas": [32, 40], "lugar-vila": [32, 40], "maca": [32, 48, 64],
    "manopla": [32, 48, 64], "moedas": [24], "osso": [24], "perneiras": [32, 48, 64], "pocao": [24, 32, 48, 64],
    "provisoes": [24], "tocha": [24, 32, 48, 64], "tonico": [32, 48, 64],
    "vital-foco": [20], "vital-mana": [20], "vital-vida": [20], "vital-vigor": [20]};

  // Cada desenho vai para o tipo de ferro que o jogo já tem (elmo, armadura, manopla, calca = perneira, bota_ferro, maca);
  // couro (capuz, gibão, calça de couro, bota de caça, luva) e as armas sem desenho (machado, martelo, arco...) ficam
  // com o do jogo. O anel tem uma pérola branca: não lembra nenhuma cor de raridade.
  const ITEM = { elmo: "elmo", armadura: "cota", manopla: "manopla", calca: "perneiras", bota_ferro: "botas-ferro",
    maca: "maca", espada: "espada", escudo: "escudo", amuleto: "amuleto", anel: "anel", aljava: "aljava" };
  // o espaço vazio: a silhueta apagada do que vai nele (o material não aparece)
  const VAZIO = { cabeca: "elmo", armadura: "cota", maos: "manopla", pernas: "perneiras", pes: "botas-ferro", arma: "espada",
    secundaria: "escudo", amuleto: "amuleto", anel1: "anel", anel2: "anel" };
  // os consumíveis, pelo id do motor (o Baú Trancado é sempre o baú de madeira e latão)
  const CONSUMIVEL = { pocao_vida: "pocao", tonico: "tonico", antidoto: "antidoto", bandagem: "bandagem", bau: "bau", tocha: "tocha" };
  const ATRIBUTO = { Ataque: "attr-ataque", Defesa: "attr-defesa", Agilidade: "attr-agilidade", Poder: "attr-poder" };
  // os recursos do topo, pelo desenho que o jogo escolhe (sem comida, o osso; a tocha apagada, a bolsa vazia e o
  // frasco vazio ficam com o do jogo); a aljava são as flechas do Patrulheiro
  const RECURSO = { pernil: "provisoes", osso_diag: "osso", tocha: "tocha", moedas: "moedas", pocao: "pocao", bandagem: "bandagem",
    aljava: "aljava" };
  const VITAL = { Vida: "vital-vida", Vigor: "vital-vigor", Mana: "vital-mana", Foco: "vital-foco" };
  const ATALHO = { Talentos: "atalho-talentos", "Grimório": "atalho-grimorio", "Inventário": "atalho-inventario", Mapa: "atalho-mapa",
    "Diário": "atalho-diario", "Bestiário": "atalho-bestiario", Salvar: "atalho-salvar", Sair: "atalho-sair" };
  // o desenho que o jogo escolhe para o destino (MapaPx.sprite); o covil vencido continua a bandeira do jogo
  const LUGAR = { vila: "lugar-vila", floresta: "lugar-floresta", pantano: "lugar-pantano", ruinas: "lugar-ruinas",
    montanha: "lugar-montanha", planicie: "lugar-planicie", cidadela: "lugar-cidadela", covil: "lugar-caverna" };
  // a roda da luta: o ataque da classe (a espada do Guerreiro), Habilidades (o grimório), Itens (a poção) e Fugir (a
  // bota com os riscos de movimento, a mesma da Agilidade: correr, não a porta do Sair)
  const ACAO = { espada: "espada", grimorio: "atalho-grimorio", pocao: "pocao", fuga: "attr-agilidade" };

  /** O arquivo de `peca` para mostrar em `lado` px: o tamanho igual ou o mais perto; maior que o maior, o dobro dele. */
  function arquivos(peca, lado) {
    const ha = TAMANHOS[peca];
    const t = ha.includes(lado) ? lado : ha.reduce((m, x) => (Math.abs(x - lado) < Math.abs(m - lado) ? x : m));
    const um = `${DIR}${peca}-${t}.png`, dois = `${DIR}${peca}-${t}@2x.png`;
    return lado > t && 2 * t >= lado ? { src: dois, srcset: "" } : { src: um, srcset: `${dois} 2x` };
  }
  /** A <img> de uma peça em `lado` px (com a classe "sprite" do jogo, para as regras de tamanho e de lugar dele). */
  function img(peca, lado, classe = "", alt = "") {
    if (!peca || !TAMANHOS[peca]) return "";
    const { src, srcset } = arquivos(peca, lado);
    return `<img class="sprite desenho ${classe}" src="${src}"${srcset ? ` srcset="${srcset}"` : ""} width="${lado}" height="${lado}" style="--s:${lado}" alt="${alt}" draggable="false">`;
  }
  /** O consumível pelo desenho que o catálogo do motor dá a ele (itens.py: icone), quando a tela só tem o desenho. */
  function consumivelDoDesenho(sprite) {
    const itens = typeof App !== "undefined" && App.estado && App.estado.itens;
    if (!itens) return "";
    const id = Object.keys(CONSUMIVEL).find((k) => itens[k] && itens[k].icone === sprite);
    return id ? CONSUMIVEL[id] : "";
  }
  /** Um endereço só (para um canvas ou uma imagem de arrasto): o do lado pedido, ou "" sem desenho. */
  function url(peca, lado) {
    return peca && TAMANHOS[peca] ? arquivos(peca, lado).src : "";
  }

  return {
    /** O equipamento, pelo desenho que o motor dá a ele (itens.py: icone). */
    item: (sprite, lado = 32, classe = "") => img(ITEM[sprite], lado, classe),
    /** A silhueta de um espaço vazio do corpo. */
    vazio: (espaco, lado = 32, classe = "fantasma") => img(VAZIO[espaco], lado, classe),
    /** Um consumível da bolsa, pelo id do motor (pocao_vida, bau...). */
    consumivel: (id, lado = 32, classe = "") => img(CONSUMIVEL[id], lado, classe),
    /** Quando a tela só tem o desenho (mercado, serviços): equipamento, consumível ou recurso, nessa ordem. */
    porDesenho: (sprite, lado = 32, classe = "") => img(ITEM[sprite] || consumivelDoDesenho(sprite) || RECURSO[sprite], lado, classe),
    atributo: (nome, lado = 24) => img(ATRIBUTO[nome], lado),
    recurso: (sprite, lado = 24) => img(RECURSO[sprite], lado),
    vital: (recurso, lado = 20) => img(VITAL[recurso], lado),
    atalho: (nome, lado = 36) => img(ATALHO[nome], lado),
    lugar: (sprite, lado = 32) => img(LUGAR[sprite], lado),
    acao: (sprite, lado = 32) => img(ACAO[sprite], lado),
    /** A cabeça de alguém com retrato (retratos.js: o herói pela classe, o companheiro pelo id): em 48 px (o topo, os
     *  cartões da Comitiva e da reação, a faixa de quem chega) a cabeça; em 32 px (a carta da luta, o painel, o aviso) a
     *  versão da carta; em 16 px (o chip de aprovação no texto) a figura de 16×16. Pixel a pixel, sem suavizar. */
    cabeca(nome, lado = 48) {
      if (!Retratos.tem(nome)) return "";
      const papel = lado <= 16 ? "figura" : lado <= 32 ? "carta" : "cabeca", e = lado / Retratos.lado(nome, papel);
      return `<img class="sprite desenho pixel" src="${Retratos.url(nome, papel, e)}" srcset="${Retratos.url(nome, papel, 2 * e)} 2x" ` +
        `width="${lado}" height="${lado}" style="--s:${lado}" alt="" draggable="false">`;
    },
    /** A figura pequena de alguém (16×16, num canvas, para quem pinta em canvas: a fogueira): o herói pela classe e o
     *  companheiro pelo id, com a figura desenhada (retratos.js) quando há; senão, o sprite do jogo. O mesmo lugar que
     *  escolhe o busto e a cabeça, para nenhuma tela ficar com o desenho antigo. */
    figura: (nome) => (Retratos.tem(nome) ? Retratos.canvas(nome, "figura") : Sprites.canvas(nome)),
    /** O busto da ficha (retratos.js): 80 px, e 64 em telas baixas (até 800 px de altura), o recorte na mesma escala. */
    retrato(nome, alt = "") {
      if (!Retratos.tem(nome)) return "";
      const u = (papel, lado, x) => Retratos.url(nome, papel, (x * lado) / Retratos.lado(nome, papel));
      return `<picture class="desenho pixel"><source media="(max-height: 800px)" srcset="${u("bustoBaixo", 64, 1)}, ${u("bustoBaixo", 64, 2)} 2x">` +
        `<img class="original" src="${u("busto", 80, 1)}" srcset="${u("busto", 80, 2)} 2x" alt="${alt}" draggable="false"></picture>`;
    },
    urlItem: (sprite, lado = 32) => url(ITEM[sprite], lado),
    urlConsumivel: (id, lado = 32) => url(CONSUMIVEL[id], lado),
  };
})();
