/* Estudo da nova direção visual da HUD (plano 23; em avaliação): o único ajuste de marcação, na dica "Testes do d20"
   (telas/inventario.js, testesHtml). O nome em marfim e o total à parte (em latão), as parcelas mais claras, as
   penalidades em vermelho queimado; no rodapé, só "20 sempre passa" e "1 sempre falha" em destaque. Os números e os
   textos são os mesmos do motor (estado.heroi.testes). O resto do estudo é só CSS (direcao.css). */
"use strict";

(() => {
  const n = (v) => `${v >= 0 ? "+" : "−"}${Math.abs(v)}`;
  Telas.testesHtml = function testesHtml(p) {
    const t = p.testes || {};
    const linhas = Object.entries(t).map(([nome, x]) => {
      const de = x.fixas.length ? x.fixas.map(([r, v]) => `${esc(r)} ${n(v)}`).join(" · ") : "sem bônus";
      const agora = x.situacao.length ? `<div class="pior">Agora: ${x.situacao.map(([r, v]) => `${esc(r)} ${n(v)}`).join(", ")} → ${n(x.mod)}</div>` : "";
      const abaixo = x.abaixo.map((l) => `<div class="pior">${esc(l)}</div>`).join("");
      return `<li><b>${esc(nome)}</b><span class="total">${n(x.fixo)}</span> <small>${de}</small>${agora}${abaixo}<div class="uso">${esc(x.uso)}</div></li>`;
    }).join("");
    const extra = p.dificuldade_extra ? ` (agora +${p.dificuldade_extra})` : "";
    return `<div class="testes-ficha" tabindex="0" ${Telas.dica(`<b>Testes do d20</b><div class="tipo">d20 + bônus contra a dificuldade</div>
      <ul class="dica-lista testes-lista">${linhas}</ul>
      <div class="rodape testes-regra"><em>20 sempre passa</em>; <em>1 sempre falha</em>. A dificuldade depende da situação e sobe 1 a cada dois níveis seus${extra}.</div>`)}>
      <span class="d20">${D20}</span><span class="nome">Testes do d20</span><span class="seta" aria-hidden="true">›</span></div>`;
  };
})();
