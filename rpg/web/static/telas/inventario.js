/* Inventário: o boneco com o equipamento (arrastar da mochila para o corpo e de volta), a mochila, os atributos com
   a dica de cada um e a reputação. */
"use strict";

(() => {
  const { h, S, AREA, dica, dicaItem, esconderDica, ESPACOS, iconeConsumivel, iconeItem, menuUso, NOME_ESPACO,
          VAZIO } = Telas;

  function personagem(d) {
    const e = App.estado;
    if (!e) return "";
    const p = e.heroi;
    const limite = (d && d.limite) || p.limite_mochila || 12;
    const attrs = atributosHtml(p);
    const espacos = Object.keys(AREA).map((s) => {
      const it = p.equip[s];
      const conteudo = it ? S(iconeItem(it), 2) : S(VAZIO[s], 2, "fantasma");
      const extra = it ? `draggable="true" ${dicaItem(it, "Arraste para a mochila, dê dois cliques ou use o botão direito para tirar.", false)}` : `title="${NOME_ESPACO[s]} (vazio)"`;
      return `<div class="espaco slot-px ${it ? "r-" + h(it.raridade) : "vazio"}" data-espaco="${s}" style="grid-area:${AREA[s]}" ${extra}>${conteudo}<span class="espaco-nome">${NOME_ESPACO[s]}</span></div>`;
    }).join("");
    const celulas = [];
    for (let i = 0; i < limite; i++) {
      const it = p.mochila[i];
      celulas.push(it
        ? `<div class="slot-px celula r-${h(it.raridade)}${it.classe && it.classe !== p.classe ? " inutil" : ""}" draggable="true" data-mochila="${i}" ${dicaItem(it, "Arraste para o corpo, dê dois cliques ou use o botão direito para equipar.")}>${S(iconeItem(it), 2)}</div>`
        : '<div class="slot-px celula vazia"></div>');
    }
    const bolsa = p.bolsa.map((b) => `<div class="slot-px clicavel" data-usar="${h(b.id)}" ${dica(`<b>${h(b.nome)}</b><div>${Realce.texto(b.desc)}</div>${b.id === "tocha" ? "" : '<div class="rodape">Clique para usar · botão direito: usar em você.</div>'}`)}>${S(iconeConsumivel(b.id), 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
    return `<div class="tela inventario">
      <div class="boneco">${espacos}<div class="boneco-retrato">${S(p.classe, 6)}</div></div>
      <div class="inv-lado">
        <div class="ficha-mini"><div class="heroi-nome">${h(p.nome)}</div><div class="heroi-titulo">${h(p.titulo)} · nível ${p.nivel} · ${p.xp}/${p.xp_proximo} XP</div></div>
        <div class="atributos">${attrs}</div>
        <h4>Mochila <small>${p.mochila.length}/${limite}</small></h4>
        <div class="mochila-grade">${celulas.join("")}<div class="slot-px lixeira" title="Arraste um item aqui para largar">${S("caveira", 2, "fantasma")}<span class="espaco-nome">Largar</span></div></div>
        <h4>Bolsa</h4><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div>
        <div class="dica-uso">Arraste itens entre a mochila e o corpo. Dois cliques ou o botão direito também funcionam. Passe o mouse para comparar.</div>
      </div></div>`;
  }

  const ICONE_ATTR = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
  /** Atributos com dica: para que servem e o que você ganha com cada ponto. */
  // Atributos a caminho: enquanto o selo de "+2 Ataque" voa, o painel mostra o valor de antes (ver seloAtributo).
  const chegando = new Map();
  function atributosHtml(p) {
    const info = p.atributos_info || {}, penal = p.atributos_penal || {};
    return Object.entries(p.atributos).map(([k, v]) => {
      const linhas = (info[k] || []).map((l, i) => `<li${penal[k] && !i ? ' class="pior"' : ""}>${h(l)}</li>`).join("");
      // Abaixo do normal (ferimento, fome): o número já vem com a penalidade, em vermelho, e a dica diz quanto.
      const pen = penal[k] ? ` <span class="penal">(−${penal[k].pct}%)</span>` : "";
      return `<div class="atributo${penal[k] ? " abaixo" : ""}" data-atributo="${h(k)}" ${dica(`<b>${h(k)} ${v}${pen}</b><ul class="dica-lista">${linhas}</ul>`)}>${S(ICONE_ATTR[k] || "estrela", 1)}<span class="nome">${h(k)}</span><span class="valor">${chegando.has(k) ? chegando.get(k) : v}</span></div>`;
    }).join("");
  }
  function reputacaoHtml(p) {
    const r = p.reputacao_info || { titulo: "", linhas: [] };
    const valor = Realce.sinais(`${p.reputacao > 0 ? "+" : p.reputacao < 0 ? "−" : ""}${Math.abs(p.reputacao)}`);
    return `<div class="reputacao" ${dica(`<b>Reputação</b><div class="aprov-agora">${h(r.titulo)} <span class="aprov-num">${valor}</span></div><ul class="dica-lista">${r.linhas.map((l) => `<li>${Realce.sinais(l)}</li>`).join("")}</ul>`)}>
      <span class="rep-icone">${S("coroa", 2)}</span><b>${p.reputacao > 0 ? "+" : ""}${p.reputacao}</b><span class="rep-titulo">${h(r.titulo)}</span></div>`;
  }

  function ligarInventario(raiz) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi) return;
    let arrastando = null;
    const limpar = () => { raiz.querySelectorAll(".alvo").forEach((x) => x.classList.remove("alvo")); arrastando = null; };
    raiz.querySelectorAll("[draggable=true]").forEach((el) => {
      el.addEventListener("dragstart", (ev) => {
        esconderDica();
        arrastando = el.dataset.mochila !== undefined ? { de: "mochila", i: Number(el.dataset.mochila) } : { de: "espaco", espaco: el.dataset.espaco };
        ev.dataTransfer.setData("text/plain", "item");
        ev.dataTransfer.effectAllowed = "move";
        if (arrastando.de === "mochila") {
          const it = heroi.mochila[arrastando.i];
          (ESPACOS[it.slot] || []).forEach((s) => { const alvo = raiz.querySelector(`[data-espaco="${s}"]`); if (alvo) alvo.classList.add("alvo"); });
          raiz.querySelector(".lixeira").classList.add("alvo");
        } else raiz.querySelector(".mochila-grade").classList.add("alvo");
      });
      el.addEventListener("dragend", limpar);
    });
    const aceitar = (alvo, ok) => {
      alvo.addEventListener("dragover", (ev) => { if (arrastando && ok(arrastando)) ev.preventDefault(); });
    };
    raiz.querySelectorAll("[data-espaco]").forEach((alvo) => {
      aceitar(alvo, (a) => a.de === "mochila" && (ESPACOS[heroi.mochila[a.i].slot] || []).includes(alvo.dataset.espaco));
      alvo.addEventListener("drop", (ev) => { ev.preventDefault(); const a = arrastando; limpar(); App.acao({ equipar: a.i, destino: alvo.dataset.espaco }, "equipar"); });
      alvo.addEventListener("dblclick", () => { if (heroi.equip[alvo.dataset.espaco]) App.acao({ tirar: alvo.dataset.espaco }, "equipar"); });
      alvo.addEventListener("contextmenu", (ev) => { ev.preventDefault(); if (heroi.equip[alvo.dataset.espaco]) App.acao({ tirar: alvo.dataset.espaco }, "equipar"); });
    });
    const grade = raiz.querySelector(".mochila-grade");
    aceitar(grade, (a) => a.de === "espaco");
    grade.addEventListener("drop", (ev) => { if (ev.target.closest(".lixeira")) return; ev.preventDefault(); const a = arrastando; limpar(); if (a && a.de === "espaco") App.acao({ tirar: a.espaco }, "equipar"); });
    const lixo = raiz.querySelector(".lixeira");
    aceitar(lixo, (a) => a.de === "mochila");
    lixo.addEventListener("drop", (ev) => {
      ev.preventDefault(); ev.stopPropagation();
      const a = arrastando; limpar();
      if (a && a.de === "mochila" && window.confirm(`Largar ${heroi.mochila[a.i].nome}? Não há volta.`)) App.acao({ largar: a.i });
    });
    raiz.querySelectorAll("[data-mochila]").forEach((el) => {
      el.addEventListener("dblclick", () => App.acao({ equipar: Number(el.dataset.mochila) }, "equipar"));
      el.addEventListener("contextmenu", (ev) => { ev.preventDefault(); App.acao({ equipar: Number(el.dataset.mochila) }, "equipar"); });
    });
    raiz.querySelectorAll("[data-usar]").forEach((el) => el.addEventListener("click", (ev) => {
      ev.stopPropagation();
      const b = (App.estado.heroi.bolsa || []).find((x) => x.id === el.dataset.usar);
      if (b && b.alvos && b.alvos.length) { menuUso(el, b); return; }
      if (b && b.motivo) { App.som("falha"); App.avisar(b.motivo, el); return; }
      App.acao({ usar: el.dataset.usar }, "item");
    }));
    // Botão direito num consumível: usa em você, sem o menu de "em quem".
    raiz.querySelectorAll("[data-usar]").forEach((el) => el.addEventListener("contextmenu", (ev) => {
      ev.preventDefault();
      const b = (App.estado.heroi.bolsa || []).find((x) => x.id === el.dataset.usar);
      if (b && b.motivo) { App.som("falha"); App.avisar(b.motivo, el); return; }
      App.acao({ usar: el.dataset.usar }, "item");
    }));
  }

  Telas.registrar("personagem", personagem, { ligar: ligarInventario });

  Object.assign(Telas, { atributosHtml, chegando, reputacaoHtml });
})();
