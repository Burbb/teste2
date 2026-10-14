/* O topo da HUD (a linha da vida, do recurso e dos recursos da bolsa) desenhado a partir do MESMO estado de
   demonstração da ficha, com a marcação do jogo (paineis.js: desenharHud), para o topo e a ficha mostrarem os mesmos
   números. Antes, o topo era a fotografia fixa do herói de nível 1. */
"use strict";

const Topo = (() => {
  const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const RECURSO_BARRA = { Vigor: "vigor", Mana: "mana", Foco: "foco" }, RECURSO_ICONE = { Vigor: "chama", Mana: "pocao_azul", Foco: "olho" };
  const pct = (a, m) => Math.max(0, Math.min(100, Math.round((100 * a) / Math.max(1, m))));
  const barra = (classe, a, m) => `<span class="barra-px ${classe}" data-alvo="${pct(a, m)}"><span class="rastro" style="width:${pct(a, m)}%"></span><span class="enchimento" style="width:${pct(a, m)}%"></span></span>`;
  const dica = (html) => ` data-dica="${esc(html)}" tabindex="0"`;
  let familia = null;  // a família de desenhos da versão (icones.js), ou nenhuma
  /** O ícone de um papel do topo (`tabela`: RECURSO pelo sprite do jogo, VITAL pelo recurso): o desenho novo, se a
   *  família tem um; senão, o sprite do jogo. */
  const ico = (sprite, escala, tabela, chave, lado) => {
    const peca = familia && familia[tabela][chave];
    return peca ? familia.img(peca, lado) : Sprites.img(sprite, escala);
  };
  function recurso(id, icone, qtd, titulo, { alerta = false, vazio = false } = {}) {
    return `<div class="recurso f-foco${alerta ? " alerta" : ""}${vazio ? " vazio" : ""}" data-rec="${id}"${dica(`<b class="t">${esc(titulo)}</b>`)}>
      <div class="icones">${ico(icone, 2, "RECURSO", icone, 24)}</div><div class="qtd">${qtd}</div></div>`;
  }
  function desenhar(alvo, h) {
    const q = (id) => (h.bolsa.find((b) => b.id === id) || { qtd: 0 }).qtd;
    const tochas = q("tocha"), pocoes = q("pocao_vida"), bandagens = q("bandagem");
    const cond = (h.condicoes || []).map((c) => `<span class="condicao${c.grave ? " grave" : ""}" data-condicao="${esc(c.id)}">${Sprites.img(c.icone, 1)}${esc(c.texto)}</span>`).join("");
    const feridas = h.ferimentos.length ? `<div class="recurso alerta f-foco" data-rec="feridas"${dica(h.ferimentos.map((f) => `<b class="t">${esc(f.nome)}</b><div class="pior">${esc((f.explica || [""])[0])}</div>`).join(""))}><div class="icones">${Sprites.img("gota", 2)}</div><div class="qtd">${h.ferimentos.length}</div></div>` : "";
    alvo.innerHTML = `
      <div class="hud-retrato" title="${esc(h.titulo)} nível ${h.nivel}">${(familia && familia.cabeca(h.classe, 48)) || Sprites.img(h.classe, 3)}<span class="nivel">${h.nivel}</span></div>
      <div class="hud-vitais">
        <div class="vital f-foco" data-vital="hp"${dica("<b class=\"t\">Vida</b>")}>${ico("coracao", 1, "VITAL", "Vida", 20)}${barra("vida", h.hp, h.max_hp)}<span class="num">${h.hp}/${h.max_hp}</span></div>
        <div class="vital f-foco" data-vital="rec"${dica(`<b class="t">${esc(h.recurso)}</b>`)}>${ico(RECURSO_ICONE[h.recurso] || "estrela", 1, "VITAL", h.recurso, 20)}${barra(RECURSO_BARRA[h.recurso] || "mana", h.rec, h.max_rec)}<span class="num">${h.rec}/${h.max_rec}</span></div>
        <div class="hud-condicoes">${cond}</div>
      </div>
      <div class="hud-recursos">
        ${recurso("provisoes", h.provisoes ? "pernil" : "osso_diag", `${h.provisoes}<small>d</small>`, h.provisoes ? `Comida para ${h.provisoes} ${h.provisoes === 1 ? "dia" : "dias"}. Cada dia consome 1 (e cada companheiro come também).` : "Sem comida! Você vai passar fome.", { alerta: h.provisoes <= 1, vazio: !h.provisoes })}
        ${recurso("tochas", tochas ? "tocha" : "tocha_apagada", tochas, "Tochas: luz para a noite, ruínas e a cidadela.", { alerta: tochas === 0, vazio: !tochas })}
        ${recurso("ouro", h.ouro ? "moedas" : "bolsa_vazia", h.ouro, h.ouro ? `Ouro: ${h.ouro} moedas` : "Sem ouro", { vazio: !h.ouro })}
        ${recurso("pocoes", pocoes ? "pocao" : "frasco_vazio", pocoes, "Poções de vida (35% da vida)", { vazio: !pocoes })}
        ${recurso("bandagens", "bandagem", bandagens, "Bandagens: enfaixam feridas abertas contra infecção", { vazio: !bandagens, alerta: !bandagens && h.ferimentos.some((f) => f.aberto) })}
        ${feridas}
      </div>`;
  }
  return { desenhar, set familia(f) { familia = f; } };
})();
