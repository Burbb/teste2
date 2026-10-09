/* Serviços da vila: a forja (reforçar) e a cabana da curandeira (tratar), em cartões com preço, tempo e o motivo
   quando não dá. O templo e a taverna usam os mesmos cartões (vila.js). */
"use strict";

(() => {
  const { h, S, dica, dicaItem, iconeItem } = Telas;

  /* A forja e a cabana da curandeira são telas como o mercado; o templo e a taverna usam os mesmos cartões diante do
     prédio (vila.js monta, com as opções que o motor marca com preço e efeito). */
  /** O topo de um balcão: o ícone, quem atende e o que diz, e o seu ouro. */
  function topoBalcao(icone, quem, fala, ouro) {
    return `<div class="loja-topo">${S(icone, 3)}<div><b>${h(quem)}</b><span class="lore">${h(fala)}</span></div>` +
      (ouro === undefined ? "" : `<span class="ouro-loja">${S("moedas", 2)}${ouro}</span>`) + "</div>";
  }
  /** Um serviço num cartão: o ícone, o nome, o que dá, o preço e o tempo. Com `motivo` (sem ouro), apagado; sem preço
   *  nem motivo e com `limite`, é só mostruário. `attrs`: o que identifica a ação (data-...). */
  function cartaoServico({ icone, raridade, nome, efeito, preco, tempo, motivo, limite, attrs = "", dicaAttr = "" }) {
    const r = raridade ? ` r-${h(raridade)}` : "";
    const fim = (preco != null ? `<span class="preco">${S("moeda", 1)}${preco}</span>` : "") + (tempo ? `<small class="serv-tempo">⧗ ${h(tempo)}</small>` : "");
    return `<button type="button" class="servico${motivo ? " caro" : ""}${limite ? " limite" : ""}" ${attrs} ${dicaAttr}${motivo ? ` aria-disabled="true"` : ""}>
      <span class="slot-px${r}">${S(icone, 2)}</span>
      <span class="serv-texto"><b class="serv-nome${r}">${h(nome)}</b>${efeito ? `<span class="serv-efeito">${Realce.texto(efeito)}</span>` : ""}</span>
      <span class="serv-fim">${fim}</span></button>`;
  }
  function ferreiro(d) {
    const cartoes = d.pecas.map((p) => cartaoServico({
      icone: iconeItem(p.item), raridade: p.item.raridade, nome: p.item.nome, preco: p.custo, limite: p.custo == null,
      efeito: p.custo == null ? "No limite (+5): a forja não tira mais nada dela" : p.ganho,
      motivo: p.custo != null && !p.pode ? "Ouro insuficiente." : "",
      attrs: p.custo == null ? "" : `data-reforcar="${h(p.slot)}"`,
      dicaAttr: dicaItem(p.item, p.custo == null ? "No limite do reforço." : p.pode ? "Clique para reforçar." : "Ouro insuficiente.", false),
    }));
    return `<div class="tela balcao-servico forja">${topoBalcao("martelo", "O ferreiro", "Um homem sem dois dedos cospe na forja. \"Ouro primeiro.\"", d.ouro)}
      <h4>Reforçar o que você usa</h4><div class="servicos">${cartoes.join("") || '<span class="vazio">Nada no corpo que valha a forja.</span>'}</div></div>`;
  }
  function curandeira(d) {
    const cartoes = d.ferimentos.map((f) => cartaoServico({
      icone: f.id === "infeccao" ? "gota_verde" : "gota", nome: f.nome, efeito: (f.explica || [])[0] || "", preco: f.custo,
      motivo: f.pode ? "" : "Ouro insuficiente.", attrs: `data-tratar="${h(f.id)}"`,
      dicaAttr: dica(`<b>${h(f.nome)}</b>${(f.explica || []).map((l, i) => `<div class="${i ? "" : "bonus pior"}">${h(l)}</div>`).join("")}<div class="rodape">${f.pode ? "Clique para tratar na hora." : "Ouro insuficiente."}</div>`),
    }));
    return `<div class="tela balcao-servico curandeira">${topoBalcao("unguento", "A curandeira", "Uma velha de mãos manchadas de sangue seco examina você. \"O que vai ser?\"", d.ouro)}
      <h4>Tratar</h4><div class="servicos">${cartoes.join("")}</div></div>`;
  }
  /** Clique num cartão: a ação, ou o "não" de quem não tem ouro. */
  function ligarServicos(raiz, chave, som) {
    raiz.querySelectorAll(`[data-${chave}]`).forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (b.classList.contains("caro")) { App.som("falha"); return; }
      App.acao({ [chave]: b.dataset[chave] }, som);
    }));
  }

  Telas.registrar("ferreiro", ferreiro, { ligar: (raiz) => ligarServicos(raiz, "reforcar", "predio_ferreiro") });
  Telas.registrar("curandeira", curandeira, { ligar: (raiz) => ligarServicos(raiz, "tratar", "cura") });

  Object.assign(Telas, { cartaoServico, topoBalcao });
})();
