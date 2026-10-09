/* Carregar jogo: os saves como cartões, do mais recente ao mais antigo. */
"use strict";

(() => {
  const { h, S } = Telas;

  function haQuanto(seg) {
    const m = Math.floor((Date.now() / 1000 - seg) / 60);
    if (m < 2) return "agora há pouco";
    if (m < 60) return `há ${m} min`;
    const hs = Math.floor(m / 60);
    if (hs < 24) return `há ${hs} h`;
    const d = Math.floor(hs / 24);
    return d === 1 ? "ontem" : `há ${d} dias`;
  }
  /** Os saves como cartões: retrato da classe, nome, nível, dia, lugar e quando foi jogado (o mais recente primeiro). */
  function saves(d) {
    const cartoes = d.saves.map((s, i) => `<button type="button" class="save-cartao${s.ilegivel ? " ilegivel" : ""}" data-save="${i}">
        <span class="save-retrato">${S(s.classe || "pergaminho", 3)}</span>
        <span class="save-info"><b>${h(s.nome)}</b>
          <span class="save-classe">${s.ilegivel ? "save danificado" : `${h(s.classe_nome)} · nível ${s.nivel}`}${s.hardcore === false ? ' <i class="save-tag">brando</i>' : ""}</span>
          <small>${s.ilegivel ? "" : `Dia ${s.dia} · ${h(s.lugar)} · `}${haQuanto(s.modificado)}</small></span></button>`).join("");
    return `<div class="tela saves"><div class="saves-lista">${cartoes}</div></div>`;
  }
  function ligarSaves(raiz) {
    raiz.querySelectorAll("[data-save]").forEach((b) => b.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ save: Number(b.dataset.save) }, "pagina"); }));
  }

  Telas.registrar("saves", saves, { ligar: ligarSaves });
})();
