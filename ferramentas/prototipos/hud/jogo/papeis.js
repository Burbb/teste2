/* HUD experimental no jogo de verdade: a família de ferro (icones.js: Icones4p) no lugar dos sprites, pelo papel de
   cada imagem nas telas reais (o topo, a ficha, o inventário, a doca, os caminhos, a janela do achado, a luta). O jogo
   continua desenhando tudo como sempre; a cada vez que ele redesenha uma parte, esta passada troca só a imagem (o
   endereço e o tamanho), sem mexer em nada que se clica, arrasta ou lê. O que não tem desenho fica o do jogo. */
"use strict";

(() => {
  const F = Icones4p;
  const VITAL = { coracao: "Vida", chama: "Vigor", pocao_azul: "Mana", olho: "Foco" };  // o sprite do topo, pelo recurso
  const RETRATOS = Object.keys(F.RETRATO);  // as classes com retrato (só o Guerreiro)

  /** O estado que o motor mandou por último (a variável global do jogo, app/nucleo.js). */
  const atual = () => (typeof estado !== "undefined" && estado) || null;

  // O nome de um sprite do jogo, pelo próprio desenho (o data URL que Sprites.url gera). Os consumíveis entram pelo
  // desenho que o motor dá a cada um (estado.itens), quando ele chega.
  let porUrl = null, consumiveis = null;
  function nome(el) {
    if (!porUrl) {
      porUrl = {};
      const nomes = [...Object.keys(F.ITEM), ...Object.keys(F.LUGAR), ...Object.keys(F.RECURSO), ...Object.keys(F.RODA),
        ...RETRATOS, ...Object.keys(VITAL), "pocao_azul", "folha", "bau"];  // os desenhos de consumível que o jogo usa
      for (const n of nomes) if (Sprites.existe(n)) { porUrl[Sprites.url(n)] = n; porUrl[Sprites.url(n, true)] = n; }
    }
    return porUrl[el.dataset.hudOrig || el.getAttribute("src")];
  }
  /** O desenho novo de um consumível pelo sprite dele (a poção, o tônico, o antídoto...), pelo catálogo do motor. */
  function consumivel(sprite) {
    const itens = (atual() && atual().itens) || null;
    if (itens && !consumiveis) {
      consumiveis = {};
      for (const [id, peca] of Object.entries(F.BOLSA)) if (itens[id] && itens[id].icone) consumiveis[itens[id].icone] = peca;
    }
    return consumiveis && consumiveis[sprite];
  }
  /** O tamanho que existe da peça mais perto do pedido (assets4p/exibicao/indice.js), ou nenhum. */
  function tamanho(peca, lado) {
    const ha = (window.ASSETS4P || {})[peca];
    if (!ha) return 0;
    return ha.includes(lado) ? lado : ha.reduce((m, t) => (Math.abs(t - lado) < Math.abs(m - lado) ? t : m));
  }
  function trocar(el, peca, pedido) {
    const lado = peca && tamanho(peca, pedido);
    if (!lado || el.dataset.hud === `${peca}-${lado}`) return;
    if (!el.dataset.hudOrig) el.dataset.hudOrig = el.getAttribute("src");
    el.src = F.src(peca, lado);
    el.srcset = F.srcset(peca, lado);
    el.width = el.height = lado;
    el.style.setProperty("--s", String(lado));
    el.classList.add("novo4c");
    el.dataset.hud = `${peca}-${lado}`;
  }
  // o teste de arte (arte-teste.js): o baú da sacristia na bolsa e o mercador no balcão; Ctrl+Alt+A ou &arte=jogo
  // voltam ao que era (jogo/desenvolvimento.js)
  const arteLigada = () => typeof ArteTeste !== "undefined" && document.body.dataset.arte !== "jogo";
  function trocarArte(el, peca, escala) {
    const marca = `arte-${peca}`;
    if (el.dataset.hud === marca) return;
    if (!el.dataset.hudOrig) el.dataset.hudOrig = el.getAttribute("src");
    const lado = ArteTeste.PECAS[peca].grade[0].length * escala;
    el.src = ArteTeste.url(peca, escala);
    el.srcset = `${ArteTeste.url(peca, escala * 2)} 2x`;
    el.width = el.height = lado;
    el.style.setProperty("--s", String(lado));
    el.classList.add("novo4c");
    el.dataset.hud = marca;
  }
  /** O tamanho em que o jogo mostra a imagem, arredondado para um dos arquivos que existem. */
  const lado = (el, tamanhos) => { const w = Number(el.getAttribute("width")) || 32; return tamanhos.find((t) => w >= t) || tamanhos[tamanhos.length - 1]; };
  const q = (sel, f) => document.querySelectorAll(sel).forEach(f);

  function passar() {
    // o topo: a cabeça do retrato, a vida e o recurso, os recursos da bolsa
    q("#hud-linha .hud-retrato img.sprite", (el) => { if (RETRATOS.includes(nome(el))) trocar(el, F.CABECA[nome(el)], 48); });
    q("#hud-linha .vital img", (el) => trocar(el, F.VITAL[VITAL[nome(el)]], 20));
    q("#hud-linha .recurso .icones img", (el) => trocar(el, F.RECURSO[nome(el)], 24));
    // a ficha: o retrato (busto) e a penalidade ao lado do valor, que o motor já manda (atributos_penal)
    q("#heroi .retrato-grande img.sprite", (el) => {
      const classe = nome(el);
      if (!RETRATOS.includes(classe)) return;
      el.outerHTML = F.retrato(classe, "Retrato do herói");
      // o retrato novo é maior que o sprite: o nome se mede de novo ao lado dele (paineis.js: acomodarNome)
      if (typeof acomodarNome === "function") acomodarNome();
    });
    const penal = (atual() && atual().heroi && atual().heroi.atributos_penal) || {};
    q("#heroi .atributo.abaixo", (el) => {
      const p = penal[el.dataset.atributo];
      if (p && !el.querySelector(".hud-penal")) el.querySelector(".valor").insertAdjacentHTML("beforeend", ` <small class="hud-penal">−${p.pct}%</small>`);
    });
    // atributos, espaços do corpo, mochila e bolsa: na ficha e no inventário
    q(".atributo[data-atributo] > img", (el) => trocar(el, F.ATRIBUTO[el.parentElement.dataset.atributo], 24));
    q("[data-mini] > img, .espaco[data-espaco] > img", (el) => {
      const s = el.parentElement.dataset.mini || el.parentElement.dataset.espaco;
      // a arma e a secundária dependem da classe (o grimório do Mago, a aljava do Patrulheiro): a silhueta nova só
      // entra onde o próprio jogo já desenha um tipo que a família tem (espada, escudo)
      const porClasse = (s === "arma" || s === "secundaria") && !F.ITEM[nome(el)];
      trocar(el, el.parentElement.classList.contains("vazio") ? (porClasse ? null : F.VAZIO[s]) : F.ITEM[nome(el)], 32);
    });
    q("[data-mochila] > img", (el) => trocar(el, F.ITEM[nome(el)], 32));
    q("[data-bolsa] > img, [data-usar] > img", (el) => {
      const id = el.parentElement.dataset.bolsa || el.parentElement.dataset.usar;
      if (id === "bau" && arteLigada()) trocarArte(el, "bau", 2);
      else trocar(el, F.BOLSA[id], 32);
    });
    // a doca, os caminhos e a janela do item achado (e as comparações dela)
    q("#doca .atalho", (b) => {
      const n = ((b.querySelector(".atalho-nome") || {}).textContent || "").trim(), el = b.querySelector(".atalho-icone img");
      if (el) trocar(el, F.ATALHO[n], F.ladoAtalho);
    });
    q("#mundo .caminho > img", (el) => trocar(el, F.LUGAR[nome(el)], lado(el, [40, 32])));
    q("#sobre-achado img.sprite, .achado-arte img.sprite", (el) => trocar(el, F.ITEM[nome(el)] || consumivel(nome(el)), lado(el, [64, 48, 32])));
    // o mercado (suprimentos, equipamentos, venda) e qualquer outro espaço de item que sobrou: pelo desenho do jogo
    q(".slot-px > img.sprite:not(.novo4c)", (el) => { const n = nome(el); trocar(el, F.ITEM[n] || consumivel(n) || F.RECURSO[n], lado(el, [64, 48, 32])); });
    // o baú que voa até a bolsa quando é recolhido (sensação do jogo): o mesmo desenho que vai estar nela
    q(".item-voando img", (el) => { if (nome(el) === "bau" && arteLigada()) trocarArte(el, "bau", 2); });
    // o mercador da banca, no balcão do mercado (só o retrato: o nome, a frase e o ouro são os do jogo)
    q(".tela.loja .loja-topo", (t) => {
      const tem = t.querySelector(".npc-retrato");
      if (arteLigada() && !tem) t.insertAdjacentHTML("afterbegin", `<span class="npc-retrato">${ArteTeste.img("mercador", 2, "", "O mercador")}</span>`);
      else if (!arteLigada() && tem) tem.remove();
    });
    // a luta: as ações da roda e o rosto do herói na carta dele
    q("#roda .rb-icone img", (el) => trocar(el, F.RODA[nome(el)], 32));
    q(".carta.heroi .icone img", (el) => { if (RETRATOS.includes(nome(el))) trocar(el, F.CABECA[nome(el)], 32); });
    // o lembrete da mira, em duas linhas no vão da arena (hud4p-luta.css): o nome da ação em cima, "escolha o alvo"
    // embaixo, sem o ponto que os separava numa linha só
    q(".roda-mira > span > b", (b) => { const t = b.nextSibling; if (t && t.nodeType === 3 && t.data.startsWith(" · ")) t.data = t.data.slice(3); });
  }

  let pedido = false;
  const agendar = () => { if (!pedido) { pedido = true; requestAnimationFrame(() => { pedido = false; passar(); }); } };
  new MutationObserver(agendar).observe(document.body, { childList: true, subtree: true });
  agendar();
  window.HUD_PASSAR = agendar;  // os controles de desenvolvimento pedem outra passada depois de trocar o teste de arte
})();
