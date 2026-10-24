/* Festa: o que as apresentações das celebrações têm em comum (etapa 2, 1.201.0): a subida de nível, o Sigilo, a
   especialização e a janela do item achado.
   - os dados de cada festa em pedaços (os ganhos com os ícones da HUD, o ponto de talento, as habilidades novas com o
     ícone do Grimório);
   - a regra dos gestos: o Continuar, o Enter, o Espaço e o Esc fecham a qualquer momento; um clique fora durante a
     entrada só a adianta; não contam o toque que começou antes de a festa abrir, o 2º clique de um clique duplo nem a
     tecla segurada; o gesto que fecha não atravessa para a página (nem para a festa seguinte);
   - o achado: a janela, o adiantar (um clique ou tecla durante a entrada leva ao fim dela; não escolhe nada, os botões
     ainda não estão lá) e a ordem do motor (os botões chegam quando a entrada termina).
   Cada apresentação (Festa.registrar) só diz o desenho: o HTML e o efeito. */
"use strict";

const Festa = (() => {
  const h = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const VITAIS = ["Vida", "Mana", "Vigor", "Foco"];
  const RARIDADE = { comum: "Comum", magico: "Incomum", raro: "Raro", lendario: "Lendário" };
  const CLASSE = { guerreiro: "Guerreiro", arqueiro: "Arqueiro", mago: "Mago" };
  // As apresentações (Estouro e Relicário) se registram aqui; o Estouro é o padrão. A escolha entre as duas é uma
  // futura opção do jogo (sem tela por enquanto): Festa.usar("relicario") troca.
  const PADRAO = "estouro", apresentacoes = {};
  let direcao = null;

  /** O ícone de um ganho de nível (o da HUD: os vitais e os atributos). */
  function icone(k, lado = 24) {
    return (VITAIS.includes(k) ? Icones.vital(k, lado === 24 ? 20 : lado) : Icones.atributo(k, lado)) || "";
  }
  const ganhos = (d) => Object.entries(d.ganhos || {}).map(([k, v]) => ({ k, v, icone: icone(k) }));
  const talento = (lado = 32) => Icones.atalho("Talentos", lado) || "";
  const habilidades = (lista) => (lista || []).map((x) => ({ nome: h(x.nome), desc: Realce.texto(x.desc), icone: Telas.S(x.icone || "estrela", 2) }));
  /** O Continuar no acabamento dos botões do jogo (a face e a aresta da HUD), com a tecla. */
  const continuar = (rotulo = "Continuar") => `<button class="continuar" type="button">${rotulo}<kbd>Enter</kbd></button>`;
  const heroi = () => (App.estado && App.estado.heroi) || {};

  /** A janela da festa aberta em `caixa` (#celebracao) com `html`; `efeito(el)` liga o efeito e devolve o controle dele
   *  ({ parar, revelar }). Resolve quando o jogador fecha. */
  function abrir(caixa, html, efeito, { revelaEm = 900 } = {}) {
    caixa.innerHTML = html;
    caixa.hidden = false;
    caixa.classList.add("festa-v2", "dir-" + direcao.nome);
    const el = caixa.querySelector(".festa"), botao = caixa.querySelector(".continuar");
    const sel = window.getSelection(); if (sel) sel.removeAllRanges();  // a seleção que um clique duplo deixou
    const ctl = efeito ? efeito(el, caixa) || {} : {};
    const nasceu = performance.now();
    let toque = 0, revelado = false;
    const revelar = () => { if (revelado) return; revelado = true; el.classList.add("revelada"); if (ctl.revelar) ctl.revelar(); };
    const auto = setTimeout(revelar, revelaEm);
    botao.focus({ preventScroll: true });
    return new Promise((resolver) => {
      const fechar = () => {
        clearTimeout(auto);
        if (ctl.parar) ctl.parar();
        caixa.hidden = true; caixa.innerHTML = "";
        caixa.classList.remove("festa-v2", "dir-" + direcao.nome);
        document.body.style.translate = "";
        document.removeEventListener("pointerdown", tocou, true);
        document.removeEventListener("click", clique, true);
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tocou = () => { toque = performance.now(); };
      const clique = (ev) => {
        ev.preventDefault(); ev.stopPropagation();
        if (ev.detail > 1 || toque < nasceu) return;
        if (ev.target.closest(".continuar") || revelado) fechar(); else revelar();
      };
      const tecla = (ev) => {
        if (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key)) return;
        ev.preventDefault(); ev.stopPropagation(); fechar();
      };
      document.addEventListener("pointerdown", tocou, true);
      document.addEventListener("click", clique, true);
      document.addEventListener("keydown", tecla, true);
    });
  }

  /** O nível, o Sigilo e a especialização, pela direção escolhida. */
  function celebrar(m, caixa, instantaneo) {
    if (!["nivel", "sigilo", "spec"].includes(m.tipo) || instantaneo) return Promise.resolve();
    const d = m.dados, f = direcao[m.tipo](d);
    return abrir(caixa, f.html, f.efeito, f);
  }

  // ------------------------------------------------------------------ o achado
  const adiar = (ms, cancelado) => new Promise((r) => {
    const fim = performance.now() + App.ritmo(ms);
    const ver = () => (cancelado() || performance.now() >= fim ? r() : setTimeout(ver, 20));
    ver();
  });

  /** A janela do achado (no lugar de Telas.abrirAchado): o HTML da direção, os botões reservados (os rótulos que vêm
   *  com o cartão, invisíveis: a janela já nasce no tamanho final) e a entrada da direção. */
  async function abrirAchado(d, semCerimonia = false) {
    Telas.fecharAchado(true);  // a anterior, mesmo esmaecendo, sai já: só uma #sobre-achado na página
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = `sobreposicao achado-v2 dir-${direcao.nome} rar-${h(d.item.raridade)}`;
    const reserva = (d.acoes || []).map((t, i) => `<button type="button" class="botao-janela reserva" tabindex="-1" aria-hidden="true"><kbd>${i + 1}</kbd>${h(t)}</button>`).join("");
    fundo.innerHTML = `<div class="janela-achado">${direcao.achado(d)}<div class="achado-acoes">${reserva}</div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild;
    if (direcao.noPalco) Telas.noPalco(janela);
    if (semCerimonia) { fundo.classList.add("pronto"); direcao.cerimonia({ fundo, janela, d, parado: true, adiantou: () => true }); return; }
    let adiantou = false;
    const adiantar = (ev) => {
      if (ev.type === "keydown" && (ev.repeat || ![" ", "Enter", "Escape"].includes(ev.key))) return;
      ev.preventDefault(); ev.stopPropagation();
      if (!adiantou) { adiantou = true; fundo.classList.add("adiantado"); }
    };
    document.addEventListener("pointerdown", adiantar, true);
    document.addEventListener("keydown", adiantar, true);
    try {
      await direcao.cerimonia({ fundo, janela, d, adiantou: () => adiantou, esperar: (ms) => adiar(ms, () => adiantou) });
    } finally {
      document.removeEventListener("pointerdown", adiantar, true);
      document.removeEventListener("keydown", adiantar, true);
    }
    fundo.classList.add("pronto");
  }

  /** O texto do item como o jogo escreve (htmlItem), com a raridade fora da linha do tipo: ela tem o selo próprio. */
  const textoItem = (it, comparando = true) => Telas.htmlItem(it, "", comparando).replace(/(<div class="tipo">[^<]*?) · [^<]*<\/div>/, "$1</div>");
  /** O desenho do item: o arquivo de 64 da interface ampliado 2× (fator inteiro), ou o sprite do jogo. */
  const arteItem = (it, lado = 64) => Icones.porDesenho(Telas.iconeItem(it), lado) || Telas.S(Telas.iconeItem(it), lado / 16);
  /** Os cartões do que você usa (um, ou os dois espaços de anel), como no jogo. */
  function equipados(d, classe = "") {
    const aneis = d.espacos && (d.equipados || []).length;
    if (aneis) return `<div class="achado-aneis ${classe}">${d.espacos.map((e) => e.item
      ? `<div class="achado-cartao atual compacto rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${arteItem(e.item, 48)}</div><div>${textoItem(e.item, false)}</div></div></div>`
      : `<div class="achado-cartao atual compacto vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span>
          <div class="compacto-corpo"><div class="achado-arte pequena">${Icones.vazio(e.espaco, 48) || ""}</div></div></div>`).join("")}</div>`;
    return (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)} ${classe}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${arteItem(e, 48)}</div>${textoItem(e, false)}</div>`).join("");
  }
  /** O aviso da mochila cheia, como no jogo. */
  function aviso(d) {
    const aneis = d.espacos && (d.equipados || []).length;
    return !d.pode_usar || d.cabe ? "" : aneis && d.espacos.some((e) => !e.item)
      ? '<div class="pior">Mochila cheia: substituir um anel deixa o antigo para trás.</div>'
      : '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>';
  }

  // As imagens da HUD por caminho absoluto: o estilo das direções é injetado na página, e o url() relativo das variáveis
  // (../hud/...) passaria a contar da página. O gesto não seleciona texto nas janelas.
  document.head.insertAdjacentHTML("beforeend", `<style id="estilo-festa-v2">
    :is(#celebracao, #sobre-achado, .achado-v2) { --m-principal: url(/static/hud/moldura-nove.png); --t-painel: url(/static/hud/textura-painel.png); }
    #celebracao.festa-v2 :is(.festa, .continuar) { user-select: none; }
    #celebracao.festa-v2 { overflow-y: auto; place-items: safe center; }
    .fx-palco { image-rendering: pixelated; }
    /* o item ampliado 2× ocupa a caixa dele (o efeito mira no meio dela); sem o brilho borrado e o pulo suave da produção */
    .achado-v2 .achado-arte { filter: none; animation: none; }
    .achado-v2 .achado-cartao.novo .achado-arte:not(.pequena) { width: 128px; height: 128px; margin: 0; }</style>`);

  /** A ficha do achado em pedaços, para as direções compor sem molduras: o nome, o tipo, os números do prêmio, a troca
   *  (o que muda, linha a linha, pelo Telas.linhasTroca do jogo) e o que você usa (cartões .achado-cartao.atual, que
   *  as celebrações de vestir e guardar procuram). Sem nada no espaço, a troca e o "você usa" ficam vazios. */
  function fichaItem(d) {
    const it = d.item, rar = h(it.raridade), hr = heroi();
    const linhas = (x) => h(x.bonus || "").split(", ").filter(Boolean).map((l) => `<span>${l}</span>`).join("") +
      (x.efeito ? `<span class="efeito">${h(x.efeito)}</span>` : "");
    const naoUsa = it.classe && hr.classe && it.classe !== hr.classe ? `<div class="pior">Só ${h({ guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" }[it.classe] || it.classe)} sabem usar isto.</div>` : "";
    const premio = `<div class="ficha-premio"><span class="ficha-rotulo">${h(Telas.NOME_ESPACO[it.slot] || "")}</span><div class="ficha-linhas">${linhas(it)}</div>${naoUsa}</div>`;
    const aneis = d.espacos && (d.equipados || []).length;
    let troca = "", usa = "";
    if (aneis) {
      usa = d.espacos.map((e) => e.item
        ? `<div class="achado-cartao atual rar-${h(e.item.raridade)}" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · você usa</span>
            <div class="ficha-usa-nome">${arteItem(e.item, 32)}<b class="r-${h(e.item.raridade)}">${h(e.item.nome)}</b></div>
            <div class="ficha-troca">${Telas.linhasTroca(it, e.item)}</div></div>`
        : `<div class="achado-cartao atual vazio" data-espaco="${h(e.espaco)}"><span class="achado-selo">${h(e.nome)} · vazio</span></div>`).join("");
    } else if ((d.equipados || []).length) {
      const e = d.equipados[0];
      troca = `<div class="ficha-troca"><span class="ficha-rotulo">na troca</span>${Telas.linhasTroca(it, e)}</div>`;
      usa = `<div class="achado-cartao atual rar-${h(e.raridade)}"><span class="achado-selo">Você usa</span>
        <div class="ficha-usa-nome">${arteItem(e, 32)}<b class="r-${h(e.raridade)}">${h(e.nome)}</b></div>
        <div class="ficha-linhas">${linhas(e)}</div></div>`;
    }
    return {
      rar, nome: `<b class="ficha-nome r-${rar}">${h(it.nome)}</b>`, raridade: `<span class="ficha-raridade rar-${rar}">${RARIDADE[it.raridade] || rar}</span>`,
      premio, troca, usa, compara: !!(troca || usa),
      lore: it.lore ? `<div class="ficha-lore">"${h(it.lore)}"</div>` : "", aviso: aviso(d),
    };
  }

  return {
    h, RARIDADE, fichaItem, CLASSE, icone, ganhos, talento, habilidades, continuar, heroi, abrir, celebrar, abrirAchado, textoItem, arteItem,
    equipados, aviso,
    registrar(d) { apresentacoes[d.nome] = d; if (!direcao || d.nome === PADRAO) direcao = d; },
    usar(nome) { if (apresentacoes[nome]) direcao = apresentacoes[nome]; return direcao.nome; },
    get apresentacoes() { return Object.keys(apresentacoes); },
    get direcao() { return direcao; },
  };
})();
