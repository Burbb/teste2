/* Itens: os espaços do equipamento (nome, desenho vazio, área no boneco), o ícone de cada item e a ficha dele, com
   a diferença para o que você usa no mesmo espaço. */
"use strict";

(() => {
  const { h } = Telas;

  const ESPACOS = { cabeca: ["cabeca"], amuleto: ["amuleto"], armadura: ["armadura"], maos: ["maos"], arma: ["arma"],
    secundaria: ["secundaria"], pernas: ["pernas"], pes: ["pes"], anel: ["anel1", "anel2"] };
  // A outra mão leva coisas diferentes em cada classe: o nome do espaço segue o que cabe nele.
  const SECUNDARIA = { guerreiro: "Escudo", arqueiro: "Aljava", mago: "Grimório" };
  const NOME_ESPACO = { cabeca: "Cabeça", amuleto: "Amuleto", armadura: "Peito", maos: "Mãos", arma: "Arma",
    get secundaria() { return SECUNDARIA[App.estado && App.estado.heroi && App.estado.heroi.classe] || "Apoio"; },
    pernas: "Pernas", pes: "Pés", anel: "Anel", anel1: "Anel 1", anel2: "Anel 2" };
  const VAZIO = { cabeca: "elmo", amuleto: "amuleto", armadura: "armadura", maos: "manopla", arma: "espada",
    secundaria: "escudo", pernas: "calca", pes: "bota", anel1: "anel", anel2: "anel" };
  const AREA = { cabeca: "cab", amuleto: "amu", armadura: "pei", maos: "mao", arma: "arm", secundaria: "sec",
    pernas: "per", pes: "pes", anel1: "an1", anel2: "an2" };
  const RARIDADE = { comum: "comum", magico: "mágico", raro: "raro", lendario: "LENDÁRIO" };
  const NOMES_STAT = { max_hp: "Vida", atk: "Ataque", defesa: "Defesa", agi: "Agilidade", poder: "Poder", get max_rec() { return (App.estado && App.estado.heroi && App.estado.heroi.recurso) || "Mana/Vigor/Foco"; },
    roubo_vida: "% roubo de vida", critico: "% crítico", espinhos: "Espinhos", regen_vida: "Vida por turno", vida_abate: "Vida por abate" };
  const CLASSE_NOME = { guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" };

  /** O desenho de um equipamento: vem do motor (itens.py: a base ou o único diz o ícone). */
  function iconeItem(it) {
    return (it && it.icone) || "saco";
  }

  /** A troca de `alvo` (o que você usa) por `it`: a diferença de cada atributo e a regra de um único (ganha a dele, ou
   *  perde a do que você usa). */
  function linhasTroca(it, alvo) {
    const chaves = new Set([...Object.keys(it.bonus_bruto), ...Object.keys(alvo.bonus_bruto)]);
    const linhas = [...chaves].map((k) => {
      const d = (it.bonus_bruto[k] || 0) - (alvo.bonus_bruto[k] || 0);
      return d ? `<span class="${d > 0 ? "melhor" : "pior"}">${d > 0 ? "▲ +" : "▼ "}${d} ${NOMES_STAT[k] || k}</span>` : "";
    }).filter(Boolean);
    if (it.efeito_nome !== alvo.efeito_nome) {
      if (it.efeito_nome) linhas.push(`<span class="melhor">▲ ${h(it.efeito_nome)}</span>`);
      if (alvo.efeito_nome) linhas.push(`<span class="pior">▼ sem ${h(alvo.efeito_nome)}</span>`);
    }
    return linhas.join("") || "<span>igual</span>";
  }
  function comparar(it) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi || !it.bonus_bruto) return "";
    const espacos = ESPACOS[it.slot] || [it.slot];
    // O anel tem dois espaços: a troca com cada um, separada, pelo nome do espaço e do anel que está nele (ou vazio).
    // Qual sai é escolha de quem joga: um efeito pode valer mais para a build do que a soma dos números.
    if (espacos.length > 1 && espacos.some((s) => heroi.equip[s])) {
      return `<div class="comparacao por-espaco">${espacos.map((s) => {
        const alvo = heroi.equip[s];
        return alvo ? `<div class="troca"><small>${NOME_ESPACO[s]} · no lugar de ${h(alvo.nome)}:</small>${linhasTroca(it, alvo)}</div>`
          : `<div class="troca"><small>${NOME_ESPACO[s]} · vazio:</small><span class="melhor">▲ tudo é ganho</span></div>`;
      }).join("")}</div>`;
    }
    const alvo = heroi.equip[espacos[0]];
    if (!alvo) return '<div class="comparacao"><span class="melhor">▲ espaço vazio: tudo é ganho</span></div>';
    return `<div class="comparacao"><small>contra ${h(alvo.nome)}:</small>${linhasTroca(it, alvo)}</div>`;
  }

  /** Os itens que o herói está usando onde `it` iria (o anel tem dois espaços), cada um com o `espaco` em que está. */
  function equipadosPara(it) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi || !it || !it.slot) return [];
    return (ESPACOS[it.slot] || [it.slot]).filter((s) => heroi.equip[s]).map((s) => ({ ...heroi.equip[s], espaco: s }));
  }
  function htmlItem(it, rodape = "", comparando = true) {
    const heroi = App.estado && App.estado.heroi;
    const naoUsa = it.classe && heroi && it.classe !== heroi.classe ? `<div class="pior">Só ${CLASSE_NOME[it.classe] || it.classe} sabem usar isto.</div>` : "";
    return `<b class="r-${h(it.raridade)}">${h(it.nome)}</b><div class="tipo">${NOME_ESPACO[it.slot] || ""} · ${RARIDADE[it.raridade] || ""}</div>
      <div class="bonus">${h(it.bonus).split(", ").join("<br>")}</div>${it.efeito ? `<div class="efeito-item">${h(it.efeito)}</div>` : ""}${comparando ? comparar(it) : ""}${naoUsa}
      ${it.lore ? `<div class="lore">"${h(it.lore)}"</div>` : ""}${rodape ? `<div class="rodape">${rodape}</div>` : ""}
      ${comparando && equipadosPara(it).length ? '<div class="atalho-shift">Segure <kbd>Shift</kbd> para ver o seu.</div>' : ""}`;
  }

  Object.assign(Telas, { AREA, equipadosPara, ESPACOS, htmlItem, iconeItem, linhasTroca, NOME_ESPACO, VAZIO });
})();
