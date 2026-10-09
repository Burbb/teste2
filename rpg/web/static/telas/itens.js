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
    pernas: "Pernas", pes: "Pés", anel: "Anel", anel1: "Anel", anel2: "Anel" };
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

  function comparar(it) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi || !it.bonus_bruto) return "";
    const espacos = ESPACOS[it.slot] || [it.slot];
    const eq = espacos.map((s) => heroi.equip[s]).filter(Boolean);
    if (espacos.length > 1 && eq.length < espacos.length) return '<div class="comparacao"><span class="melhor">▲ há um espaço livre</span></div>';
    if (!eq.length) return '<div class="comparacao"><span class="melhor">▲ espaço vazio: tudo é ganho</span></div>';
    const alvo = eq.reduce((a, b) => (Object.values(a.bonus_bruto).reduce((x, y) => x + y, 0) <= Object.values(b.bonus_bruto).reduce((x, y) => x + y, 0) ? a : b));
    const chaves = new Set([...Object.keys(it.bonus_bruto), ...Object.keys(alvo.bonus_bruto)]);
    const linhas = [...chaves].map((k) => {
      const d = (it.bonus_bruto[k] || 0) - (alvo.bonus_bruto[k] || 0);
      return d ? `<span class="${d > 0 ? "melhor" : "pior"}">${d > 0 ? "▲ +" : "▼ "}${d} ${NOMES_STAT[k] || k}</span>` : "";
    }).filter(Boolean);
    return `<div class="comparacao"><small>contra ${h(alvo.nome)}:</small>${linhas.join("") || "<span>igual</span>"}</div>`;
  }

  /** Os itens que o herói está usando onde `it` iria (o anel tem dois espaços). */
  function equipadosPara(it) {
    const heroi = App.estado && App.estado.heroi;
    if (!heroi || !it || !it.slot) return [];
    return (ESPACOS[it.slot] || [it.slot]).map((s) => heroi.equip[s]).filter(Boolean);
  }
  function htmlItem(it, rodape = "", comparando = true) {
    const heroi = App.estado && App.estado.heroi;
    const naoUsa = it.classe && heroi && it.classe !== heroi.classe ? `<div class="pior">Só ${CLASSE_NOME[it.classe] || it.classe} sabem usar isto.</div>` : "";
    return `<b class="r-${h(it.raridade)}">${h(it.nome)}</b><div class="tipo">${NOME_ESPACO[it.slot] || ""} · ${RARIDADE[it.raridade] || ""}</div>
      <div class="bonus">${h(it.bonus).split(", ").join("<br>")}</div>${comparando ? comparar(it) : ""}${naoUsa}
      ${it.lore ? `<div class="lore">"${h(it.lore)}"</div>` : ""}${rodape ? `<div class="rodape">${rodape}</div>` : ""}
      ${comparando && equipadosPara(it).length ? '<div class="atalho-shift">Segure <kbd>Shift</kbd> para ver o seu.</div>' : ""}`;
  }

  Object.assign(Telas, { AREA, equipadosPara, ESPACOS, htmlItem, iconeItem, NOME_ESPACO, VAZIO });
})();
