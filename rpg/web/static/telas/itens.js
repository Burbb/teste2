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
  const RARIDADE = { comum: "comum", magico: "incomum", raro: "raro", lendario: "LENDÁRIO" };
  const NOMES_STAT = { max_hp: "Vida", atk: "Ataque", defesa: "Defesa", agi: "Agilidade", poder: "Poder", get max_rec() { return (App.estado && App.estado.heroi && App.estado.heroi.recurso) || "Mana/Vigor/Foco"; },
    roubo_vida: "% roubo de vida", critico: "% crítico", espinhos: "Espinhos", regen_vida: "Vida por turno", vida_abate: "Vida por abate" };
  const CLASSE_NOME = { guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" };
  // Quem a ficha do item compara: o personagem selecionado na janela do grupo (1.213.0) ou, sem ele, o herói. A ficha
  // de um companheiro (web/estado.py, ficha_companheiro) tem o mesmo formato: id, nome, classe (das peças), equip.
  const heroi = () => App.estado && App.estado.heroi;
  const ehHeroi = (quem) => !quem || !quem.id || quem.id === "heroi";
  /** O nome do espaço para quem veste: a outra mão segue a classe das peças dele. */
  const nomeEspaco = (s, classe) => (s === "secundaria" ? SECUNDARIA[classe] || "Apoio" : NOME_ESPACO[s]);

  /** O desenho de um equipamento: vem do motor (itens.py: a base ou o único diz o ícone). */
  function iconeItem(it) {
    return (it && it.icone) || "saco";
  }

  /** A troca de `alvo` (o que você usa) por `it`: a diferença de cada atributo e a regra de um único (ganha a dele, ou
   *  perde a do que você usa). */
  function linhasTroca(it, alvo, quem = heroi()) {
    const chaves = new Set([...Object.keys(it.bonus_bruto), ...Object.keys(alvo.bonus_bruto)]);
    const linhas = [...chaves].map((k) => {
      const d = (it.bonus_bruto[k] || 0) - (alvo.bonus_bruto[k] || 0);
      const nome = k === "max_rec" && quem && quem.recurso ? quem.recurso : NOMES_STAT[k] || k;
      return d ? `<span class="${d > 0 ? "melhor" : "pior"}">${d > 0 ? "▲ +" : "▼ "}${d} ${nome}</span>` : "";
    }).filter(Boolean);
    if (it.efeito_nome !== alvo.efeito_nome) {
      if (it.efeito_nome) linhas.push(`<span class="melhor">▲ ${h(it.efeito_nome)}</span>`);
      if (alvo.efeito_nome) linhas.push(`<span class="pior">▼ sem ${h(alvo.efeito_nome)}</span>`);
    }
    return linhas.join("") || "<span>igual</span>";
  }
  /** O espaço vazio não ganha linha: os atributos do item já dizem o que ele traz, sem nada para comparar. */
  function comparar(it, quem = heroi()) {
    if (!quem || !it.bonus_bruto) return "";
    const de = ehHeroi(quem) ? "" : `, de ${h(quem.nome)}`;
    const espacos = ESPACOS[it.slot] || [it.slot];
    // O anel tem dois espaços: a troca com cada um, separada, pelo nome do espaço e do anel que está nele (ou vazio).
    // Qual sai é escolha de quem joga: um efeito pode valer mais para a build do que a soma dos números.
    if (espacos.length > 1 && espacos.some((s) => quem.equip[s])) {
      return `<div class="comparacao por-espaco">${espacos.filter((s) => quem.equip[s]).map((s) => {
        const alvo = quem.equip[s];
        return `<div class="troca"><small>${NOME_ESPACO[s]} · no lugar de ${h(alvo.nome)}${de}:</small>${linhasTroca(it, alvo, quem)}</div>`;
      }).join("")}</div>`;
    }
    const alvo = quem.equip[espacos[0]];
    if (!alvo) return "";
    return `<div class="comparacao"><small>contra ${h(alvo.nome)}${de}:</small>${linhasTroca(it, alvo, quem)}</div>`;
  }

  /** Os itens que o herói está usando onde `it` iria (o anel tem dois espaços), cada um com o `espaco` em que está. */
  function equipadosPara(it, quem = heroi()) {
    if (!quem || !it || !it.slot) return [];
    return (ESPACOS[it.slot] || [it.slot]).filter((s) => quem.equip[s]).map((s) => ({ ...quem.equip[s], espaco: s }));
  }
  /** O motivo de quem não usa a peça (ou ""): o herói, "Só magos sabem usar isto."; o companheiro, pelo nome. */
  function naoUsa(it, quem = heroi()) {
    if (!it.classe || !quem || it.classe === quem.classe) return "";
    return ehHeroi(quem) ? `Só ${CLASSE_NOME[it.classe] || it.classe} sabem usar isto.`
      : `${quem.nome} não usa peças de ${(CLASSE_NOME[it.classe] || it.classe).replace(/s$/, "")}.`;
  }
  function htmlItem(it, rodape = "", comparando = true, quem = heroi()) {
    const motivo = naoUsa(it, quem);
    const tipo = it.slot === "secundaria" && it.classe ? nomeEspaco("secundaria", it.classe) : NOME_ESPACO[it.slot] || "";
    return `<b class="r-${h(it.raridade)}">${h(it.nome)}</b><div class="tipo">${tipo} · ${RARIDADE[it.raridade] || ""}</div>
      <div class="bonus">${h(it.bonus).split(", ").join("<br>")}</div>${it.efeito ? `<div class="efeito-item">${h(it.efeito)}</div>` : ""}${comparando ? comparar(it, quem) : ""}${motivo ? `<div class="pior">${h(motivo)}</div>` : ""}
      ${it.lore ? `<div class="lore">"${h(it.lore)}"</div>` : ""}${rodape ? `<div class="rodape">${rodape}</div>` : ""}
      ${comparando && equipadosPara(it, quem).length ? `<div class="atalho-shift">Segure <kbd>Shift</kbd> para ver ${ehHeroi(quem) ? "o seu" : "o de " + h(quem.nome)}.</div>` : ""}`;
  }

  Object.assign(Telas, { AREA, equipadosPara, ESPACOS, htmlItem, iconeItem, linhasTroca, naoUsa, NOME_ESPACO, nomeEspaco, VAZIO });
})();
