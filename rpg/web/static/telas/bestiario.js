/* Bestiário: as criaturas que você já enfrentou, com traços, fraquezas e resistências (depois de abater algumas). */
"use strict";

(() => {
  const { h, S, barra } = Telas;

  function bestiario(d) {
    if (!d.fichas.length) return '<div class="tela"><span class="vazio">Você ainda não enfrentou nenhuma criatura.</span></div>';
    const cartas = d.fichas.map((f) => {
      const tags = f.conhecido
        ? f.tracos_nomes.map((t) => `<span class="tag">${h(t)}</span>`).join("") + f.fraquezas.map((t) => `<span class="tag fraco">fraco: ${h(t)}</span>`).join("") +
          f.resiste.map((t) => `<span class="tag forte">resiste: ${h(t)}</span>`).join("")
        // o que ainda não se sabe: um estado de conteúdo bloqueado (o cadeado e o que falta, pelo motor), não um botão
        : `<span class="besti-bloqueado">${S("cadeado", 1)}<span>Traços e fraquezas ocultos. ${h(f.falta || "")}</span></span>`;
      return `<div class="cartao${f.conhecido ? "" : " desconhecido"}${f.mestre ? " mestre" : ""}"><div class="cab">${Icones.criatura(f.retrato, 48) || S(f.retrato || "caveira", 3)}
        <div><b>${h(f.nome)}</b><span class="sub">${Texto.plural(f.abates, "abate")}</span></div></div>
        <span class="lore">${h(f.lore)}</span><div class="tags">${f.mestre ? '<span class="tag mestre">mestre caçador +10% dano</span>' : ""}${tags}</div></div>`;
    }).join("");
    return `<div class="tela"><div class="meter" style="margin-bottom:10px">Criaturas conhecidas ${barra("xp", d.fichas.length, d.total)} ${d.fichas.length}/${d.total}</div><div class="cartas">${cartas}</div></div>`;
  }

  Telas.registrar("bestiario", bestiario);
})();
