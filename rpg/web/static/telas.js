/* Telas visuais: árvore de talentos, ficha do personagem, diário, bestiário, comitiva,
   celebrações (nível, Sigilo, especialização, vitória) e avisos. Usa o objeto App (app.js). */
"use strict";

const Telas = (() => {
  const h = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const S = (nome, escala = 2, classe = "") => Sprites.img(nome, escala, classe);

  const ICONE_TALENTO = {
    pele_ferro: "escudo", golpe_brutal: "espada", folego: "coracao", luz_curativa: "estrela", contra_ataque: "espada",
    sede_insaciavel: "gota", aura_protecao: "escudo", muralha: "escudo", frenesi: "chama", martirio: "coracao",
    imortal: "caveira", olho_aguia: "olho", pes_leves: "folha", aljava_funda: "aljava", laco_animal: "fera",
    tiro_abertura: "flecha", laminas_envenenadas: "gota", armadilheiro: "cadeado", mira_firme: "flecha",
    golpe_sombras: "caveira", matilha: "fera", assassino: "caveira", mente_vasta: "livro", potencia_arcana: "pocao_azul",
    canalizacao: "olho", brasas: "chama", escudo_reflexo: "escudo", pacto_sombrio: "gota", ignicao: "chama",
    eficiencia: "estrela", exercito: "caveira", coracao_ardente: "chama", senhor_mortos: "caveira",
  };
  const ICONE_ITEM = { pocao_vida: "pocao", tonico: "pocao_azul", antidoto: "folha", bandagem: "bandagem", unguento: "pocao_azul",
    tocha: "tocha", bomba_fumaca: "caveira", pena_fenix: "chama" };
  const ARMA = { guerreiro: "espada", arqueiro: "arco", mago: "cajado" };

  function iconeCriatura(tracos = [], familia = "") {
    const t = new Set(tracos);
    if (t.has("demonio")) return "demonio";
    if (t.has("etereo")) return "etereo";
    if (t.has("corrompido")) return "corrompido";
    if (t.has("morto-vivo")) return "caveira";
    if (t.has("construto")) return "construto";
    if (t.has("voador")) return "voador";
    if (t.has("planta")) return "planta";
    if (t.has("fera")) return "fera";
    if (t.has("humano") || t.has("conjurador")) return "humano";
    if (/bandid|mercen|cultis|cavaleiro/.test(familia)) return "humano";
    return "caveira";
  }

  // ------------------------------------------------------------------ talentos
  let arvore = null, ranksAntes = {};
  function guardarArvore(a) { arvore = a; }
  function abrirTalentos(m) {
    if (!arvore) return false;
    const caixa = document.getElementById("sobre-talentos");
    const idx = {};
    let voltar = null;
    m.opcoes.forEach((o, i) => { if (o.meta && o.meta.talento) idx[o.meta.talento] = i; if (o.meta && o.meta.voltar) voltar = i; });
    App.acaoFecharTalentos = () => App.responder(m.id, voltar);
    const a = arvore;
    document.getElementById("talentos-titulo").textContent = `Talentos · ${a.classe}`;
    const colunas = a.colunas.map((nome, i) => {
      const trancada = i !== 1 && (!a.spec || nome.toLowerCase() !== a.spec);
      const sub = i === 1 ? "para todos" : !a.spec ? "especialização no nível 4" : trancada ? "caminho não escolhido" : "sua especialização";
      return `<div class="arvore-col-titulo${trancada ? " trancada" : ""}">${h(nome)}<small>${sub}</small></div>`;
    }).join("");
    let html = `<div class="arvore-topo"><span>Nível ${a.nivel} · passe o mouse num talento para ver o que ele faz</span>
      <span class="pontos${a.pontos ? "" : " zero"}">${S("estrela", 2)} ${a.pontos} ponto${a.pontos === 1 ? "" : "s"}</span></div>
      <div class="arvore-grade"><div></div>${colunas}`;
    for (let camada = 1; camada <= 4; camada++) {
      const nivelReq = a.camadas[String(camada)];
      html += `<div class="arvore-nivel${a.nivel >= nivelReq ? " ok" : ""}">Nv.${nivelReq}</div>`;
      for (let col = 0; col < 3; col++) {
        const n = a.nos.find((x) => x.camada === camada && x.coluna === col);
        const acima = a.nos.find((x) => x.camada === camada - 1 && x.coluna === col);
        const conecta = n && acima ? " conecta" + (acima.rank > 0 ? " aceso" : "") : "";
        if (!n) { html += `<div class="arvore-celula${conecta}"></div>`; continue; }
        const pode = n.estado === "disponivel" && a.pontos > 0 && idx[n.id] !== undefined;
        const classe = n.estado === "comprado" ? "comprado" : n.estado === "disponivel" ? "disponivel" : n.estado === "bloqueado" ? "bloqueado" : "trancado";
        const novo = ranksAntes[n.id] !== undefined && n.rank > ranksAntes[n.id] ? " aprendeu" : "";
        html += `<div class="arvore-celula${conecta}"><div class="no-talento ${classe}${pode ? " pode" : ""}${novo}" data-id="${h(n.id)}">
          ${S(ICONE_TALENTO[n.id] || "estrela", 3)}<span class="rank">${n.rank}/${n.max}</span></div></div>`;
      }
    }
    html += "</div>";
    document.getElementById("arvore").innerHTML = html;
    if (Object.values(ranksAntes).length && a.nos.some((n) => ranksAntes[n.id] !== undefined && n.rank > ranksAntes[n.id])) App.som("nivel");
    ranksAntes = Object.fromEntries(a.nos.map((n) => [n.id, n.rank]));
    const info = document.getElementById("talento-info");
    document.querySelectorAll("#arvore .no-talento").forEach((el) => {
      const n = a.nos.find((x) => x.id === el.dataset.id);
      el.addEventListener("mouseenter", () => {
        info.innerHTML = `<b>${h(n.nome)}</b><div class="r">Grau ${n.rank} de ${n.max}${n.spec ? " · " + h(n.spec) : ""}</div><div>${h(n.desc)}</div>` +
          (n.motivo ? `<div class="req">${h(n.motivo[0].toUpperCase() + n.motivo.slice(1))}</div>` : "") +
          (n.estado === "comprado" ? '<div class="acao">Aprendido por completo.</div>' :
            n.estado === "disponivel" ? (a.pontos ? '<div class="acao">Clique para aprender (1 ponto).</div>' : '<div class="req">Sem pontos de talento.</div>') : "");
        info.hidden = false;
        const r = el.getBoundingClientRect();
        info.style.left = Math.min(window.innerWidth - 320, r.right + 12) + "px";
        info.style.top = Math.max(10, r.top - 10) + "px";
      });
      el.addEventListener("mouseleave", () => { info.hidden = true; });
      if (el.classList.contains("pode")) el.addEventListener("click", () => { info.hidden = true; App.responder(m.id, idx[n.id]); });
    });
    caixa.hidden = false;
    return true;
  }
  function fecharTalentos() {
    document.getElementById("sobre-talentos").hidden = true;
    document.getElementById("talento-info").hidden = true;
  }

  // ------------------------------------------------------------------ itens e dicas
  const ESPACOS = { cabeca: ["cabeca"], amuleto: ["amuleto"], armadura: ["armadura"], maos: ["maos"], arma: ["arma"],
    secundaria: ["secundaria"], pernas: ["pernas"], pes: ["pes"], anel: ["anel1", "anel2"] };
  const NOME_ESPACO = { cabeca: "Cabeça", amuleto: "Amuleto", armadura: "Peito", maos: "Mãos", arma: "Arma",
    secundaria: "Mão secundária", pernas: "Pernas", pes: "Pés", anel: "Anel", anel1: "Anel", anel2: "Anel" };
  const VAZIO = { cabeca: "elmo", amuleto: "amuleto", armadura: "armadura", maos: "manopla", arma: "espada",
    secundaria: "escudo", pernas: "calca", pes: "bota", anel1: "anel", anel2: "anel" };
  const AREA = { cabeca: "cab", amuleto: "amu", armadura: "pei", maos: "mao", arma: "arm", secundaria: "sec",
    pernas: "per", pes: "pes", anel1: "an1", anel2: "an2" };
  const RARIDADE = { comum: "comum", magico: "mágico", raro: "raro", lendario: "LENDÁRIO" };
  const NOMES_STAT = { max_hp: "Vida", atk: "Ataque", defesa: "Defesa", agi: "Agilidade", poder: "Poder", max_rec: "Recurso",
    roubo_vida: "% roubo de vida", critico: "% crítico", espinhos: "Espinhos", regen_vida: "Vida por turno", vida_abate: "Vida por abate" };
  const CLASSE_NOME = { guerreiro: "guerreiros", arqueiro: "arqueiros", mago: "magos" };

  function iconeItem(it) {
    const b = `${it.base || ""} ${it.nome || ""}`;
    switch (it.slot) {
      case "arma":
        if (/Machado|Cutelo/.test(b)) return "machado";
        if (/Maça/.test(b)) return "maca";
        if (/Martelo/.test(b)) return "martelo";
        if (/Besta/.test(b)) return "besta";
        if (/Arco/.test(b)) return "arco";
        if (/Varinha/.test(b)) return "varinha";
        if (/Orbe/.test(b)) return "orbe";
        if (/Grimório/.test(b)) return "livro";
        if (/Cajado/.test(b)) return "cajado";
        return "espada";
      case "cabeca": return /Diadema|Coroa/.test(b) ? "coroa" : /Pontudo/.test(b) ? "chapeu" : /Capuz|Couro/.test(b) ? "capuz" : "elmo";
      case "armadura": return /Manto|Túnica|Veste/.test(b) ? "manto" : /Gibão|Capa|Colete|Couro/.test(b) ? "gibao" : "armadura";
      case "maos": return /Manopla/.test(b) ? "manopla" : "luva";
      case "pernas": return /Couro/.test(b) ? "calca_couro" : /Viagem/.test(b) ? "calca_tecido" : "calca";
      case "pes": return /Ferrada/.test(b) ? "bota_ferro" : /Sandália/.test(b) ? "sandalia" : "bota";
      case "secundaria": return /Aljava/.test(b) ? "aljava" : /Foco/.test(b) ? "orbe" : /Tomo/.test(b) ? "livro" : "escudo";
      case "anel": return "anel";
      default: return "amuleto";
    }
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

  const dicas = [];
  function dica(html) {
    if (dicas.length > 3000) dicas.splice(0, 2000);  // antigas não estão mais na tela
    dicas.push(html);
    return `data-dica="${dicas.length - 1}"`;
  }
  function dicaItem(it, rodape = "", comparando = true) {
    const heroi = App.estado && App.estado.heroi;
    const naoUsa = it.classe && heroi && it.classe !== heroi.classe ? `<div class="pior">Só ${CLASSE_NOME[it.classe] || it.classe} sabem usar isto.</div>` : "";
    return dica(`<b class="r-${h(it.raridade)}">${h(it.nome)}</b><div class="tipo">${NOME_ESPACO[it.slot] || ""} · ${RARIDADE[it.raridade] || ""}</div>
      <div class="bonus">${h(it.bonus).split(", ").join("<br>")}</div>${comparando ? comparar(it) : ""}${naoUsa}
      ${it.lore ? `<div class="lore">"${h(it.lore)}"</div>` : ""}${rodape ? `<div class="rodape">${rodape}</div>` : ""}`);
  }
  function ligarDicas(raiz) {
    let caixa = document.getElementById("dica-item");
    if (!caixa) { caixa = document.createElement("div"); caixa.id = "dica-item"; caixa.className = "moldura"; caixa.hidden = true; document.body.appendChild(caixa); }
    raiz.querySelectorAll("[data-dica]").forEach((el) => {
      el.addEventListener("mouseenter", () => {
        caixa.innerHTML = dicas[Number(el.dataset.dica)] || "";
        caixa.hidden = false;
        const r = el.getBoundingClientRect();
        const esq = r.right + 10 + 290 > window.innerWidth ? r.left - 300 : r.right + 10;
        caixa.style.left = Math.max(6, esq) + "px";
        caixa.style.top = Math.max(6, Math.min(window.innerHeight - caixa.offsetHeight - 6, r.top - 6)) + "px";
      });
      el.addEventListener("mouseleave", () => { caixa.hidden = true; });
    });
  }
  function esconderDica() { const c = document.getElementById("dica-item"); if (c) c.hidden = true; }

  // ------------------------------------------------------------------ inventário (boneco + mochila)
  function personagem(d) {
    const e = App.estado;
    if (!e) return "";
    const p = e.heroi;
    const limite = (d && d.limite) || p.limite_mochila || 12;
    const icAttr = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
    const attrs = Object.entries(p.atributos).map(([k, v]) => `<div class="atributo">${S(icAttr[k] || "estrela", 1)}<span class="nome">${h(k)}</span><span class="valor">${v}</span></div>`).join("");
    const espacos = Object.keys(AREA).map((s) => {
      const it = p.equip[s];
      const conteudo = it ? S(iconeItem(it), 2) : S(VAZIO[s], 2, "fantasma");
      const extra = it ? `draggable="true" ${dicaItem(it, "Arraste para a mochila ou dê dois cliques para tirar.", false)}` : `title="${NOME_ESPACO[s]} (vazio)"`;
      return `<div class="espaco slot-px ${it ? "r-" + h(it.raridade) : "vazio"}" data-espaco="${s}" style="grid-area:${AREA[s]}" ${extra}>${conteudo}<span class="espaco-nome">${NOME_ESPACO[s]}</span></div>`;
    }).join("");
    const celulas = [];
    for (let i = 0; i < limite; i++) {
      const it = p.mochila[i];
      celulas.push(it
        ? `<div class="slot-px celula r-${h(it.raridade)}${it.classe && it.classe !== p.classe ? " inutil" : ""}" draggable="true" data-mochila="${i}" ${dicaItem(it, "Arraste para o corpo ou dê dois cliques para equipar.")}>${S(iconeItem(it), 2)}</div>`
        : '<div class="slot-px celula vazia"></div>');
    }
    const bolsa = p.bolsa.map((b) => `<div class="slot-px clicavel" data-usar="${h(b.id)}" ${dica(`<b>${h(b.nome)}</b><div>${h(b.desc)}</div>${b.id === "tocha" ? "" : '<div class="rodape">Clique para usar.</div>'}`)}>${S(ICONE_ITEM[b.id] || "pocao", 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
    return `<div class="tela inventario">
      <div class="boneco">${espacos}<div class="boneco-retrato">${S(p.classe, 6)}</div></div>
      <div class="inv-lado">
        <div class="ficha-mini"><div class="heroi-nome">${h(p.nome)}</div><div class="heroi-titulo">${h(p.titulo)} · nível ${p.nivel} · ${p.xp}/${p.xp_proximo} XP</div></div>
        <div class="atributos">${attrs}</div>
        <h4>Mochila <small>${p.mochila.length}/${limite}</small></h4>
        <div class="mochila-grade">${celulas.join("")}<div class="slot-px lixeira" title="Arraste um item aqui para largar">${S("caveira", 2, "fantasma")}<span class="espaco-nome">Largar</span></div></div>
        <h4>Bolsa</h4><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div>
        <div class="dica-uso">Arraste itens entre a mochila e o corpo. Dois cliques também funcionam. Passe o mouse para comparar.</div>
      </div></div>`;
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
    raiz.querySelectorAll("[data-mochila]").forEach((el) => el.addEventListener("dblclick", () => App.acao({ equipar: Number(el.dataset.mochila) }, "equipar")));
    raiz.querySelectorAll("[data-usar]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ usar: el.dataset.usar }, "item"); }));
  }

  // ------------------------------------------------------------------ mercado
  function loja(d) {
    const cons = d.consumiveis.map((c) => {
      const caro = c.preco > d.ouro;
      const icone = c.id === "provisoes" ? "pernil" : c.id === "flechas" ? "aljava" : (ICONE_ITEM[c.id] || "pocao");
      return `<button type="button" class="mercadoria${caro ? " caro" : ""}" data-comprar="${h(c.id)}" ${dica(`<b>${h(c.nome)}</b><div>${h(c.desc)}</div><div class="rodape">${caro ? "Ouro insuficiente." : "Clique para comprar."}</div>`)}>
        <span class="slot-px">${S(icone, 2)}${c.tem ? `<span class="qtd">${c.tem}</span>` : ""}</span>
        <span class="merc-nome">${h(c.nome)}</span><span class="preco">${S("moeda", 1)}${c.preco}</span></button>`;
    }).join("");
    const equips = d.equipamentos.map((it, i) => {
      const caro = it.preco > d.ouro;
      return `<button type="button" class="mercadoria equip${caro ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, caro ? "Ouro insuficiente." : "Clique para comprar (vai para a mochila).")}>
        <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
        <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span><span class="preco">${S("moeda", 1)}${it.preco}</span></button>`;
    }).join("");
    const venda = d.mochila.map((it, i) => `<div role="button" tabindex="0" class="mercadoria equip venda" draggable="true" data-vender="${i}" ${dicaItem(it, "Clique (ou arraste para o balcão) para vender.")}>
        <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
        <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span><span class="preco ganho">+${S("moeda", 1)}${it.preco}</span></div>`).join("");
    return `<div class="tela loja">
      <div class="loja-topo">${S("saco", 3)}<div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
        <span class="ouro-loja">${S("moedas", 2)}${d.ouro}</span></div>
      <div class="balcao">
        <h4>Suprimentos</h4><div class="vitrine">${cons}</div>
        <h4>Equipamentos</h4><div class="vitrine">${equips || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>'}</div>
      </div>
      <h4>Sua mochila <small>${d.ocupado}/${d.limite} · o mercador paga metade</small></h4>
      <div class="vitrine vitrine-venda">${venda || '<span class="vazio">Nada para vender.</span>'}</div></div>`;
  }

  function ligarLoja(raiz) {
    raiz.querySelectorAll("[data-comprar]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); if (!el.classList.contains("caro")) App.acao({ comprar: el.dataset.comprar }, "moeda"); else App.som("falha"); }));
    raiz.querySelectorAll("[data-comprar-item]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); if (!el.classList.contains("caro")) App.acao({ comprar_item: Number(el.dataset.comprarItem) }, "moeda"); else App.som("falha"); }));
    let vendendo = null;
    const balcao = raiz.querySelector(".loja");  // solte em qualquer lugar do balcão do mercador
    const vendas = raiz.querySelector(".vitrine-venda");
    raiz.querySelectorAll("[data-vender]").forEach((el) => {
      el.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ vender: Number(el.dataset.vender) }, "moeda"); });
      el.addEventListener("dragstart", (ev) => { esconderDica(); vendendo = Number(el.dataset.vender); ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null && !vendas.contains(ev.target)) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null && !vendas.contains(ev.target)) App.acao({ vender: vendendo }, "moeda");
      vendendo = null;
    });
  }

  function diario(d) {
    const contratos = d.contratos.map((c) => `<div class="cartao${c.concluido ? " feito" : ""}"><div class="cab">${S(c.tipo === "caca" || c.tipo === "alvo" ? "espada" : "pergaminho", 2)}<div><b>Contrato</b><span class="sub">${c.ouro ? c.ouro + " de ouro" : ""}${c.progresso ? " · " + c.progresso : ""}</span></div></div>${h(c.desc)}</div>`).join("");
    const rumores = d.rumores.map((r) => `<div class="cartao"><div class="cab">${S("olho", 2)}<div><b>Rumor</b><span class="sub">${r.expira > 0 ? `some em ${r.expira} dia(s)` : "some hoje"}</span></div></div><span class="lore">${h(r.texto)}</span></div>`).join("");
    const aliados = d.aliados.map((a) => `<div class="cartao"><div class="cab">${S("escudo", 2)}<div><b>${h(a.nome)}</b><span class="sub">aliado na batalha final</span></div></div><span class="lore">${h(a.texto)}</span></div>`).join("");
    const losangos = [0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}" style="display:inline-block;width:18px;height:18px;border:3px solid #4a4038;transform:rotate(45deg);margin:0 8px;background:${i < d.sigilos ? "var(--ouro)" : "#1b1511"}"></i>`).join("");
    return `<div class="tela"><div class="cartas">
      <div class="cartao inimigo" style="grid-column:1/-1"><div class="cab">${S("corrompido", 3)}<div><b>${h(d.antagonista.nome)}</b><span class="sub">${h(d.antagonista.origem)}</span></div></div>
        <div class="meter">Corrupção ${barra("corrupcao", d.corrupcao, 100)} ${d.corrupcao}%</div>
        <div class="meter" style="margin-top:6px">Sigilos <span style="margin-left:8px">${losangos}</span> ${d.sigilos}/3 · dia ${d.dia}</div></div>
      ${d.nemesis ? `<div class="cartao inimigo"><div class="cab">${S("fera", 2)}<div><b>${h(d.nemesis.nome)}</b><span class="sub">nêmesis · ${h(d.nemesis.familia)}</span></div></div><span class="lore">Ele não esqueceu de você.</span></div>` : ""}
    </div>
    <h4>Contratos</h4><div class="cartas">${contratos || '<span class="vazio">Nenhum contrato. Procure o mural de uma vila.</span>'}</div>
    <h4>Rumores</h4><div class="cartas">${rumores || '<span class="vazio">Nenhum rumor. Pague uma bebida numa taverna.</span>'}</div>
    ${aliados ? `<h4>Aliados para o fim</h4><div class="cartas">${aliados}</div>` : ""}</div>`;
  }

  function bestiario(d) {
    if (!d.fichas.length) return '<div class="tela"><span class="vazio">Você ainda não enfrentou nenhuma criatura.</span></div>';
    const cartas = d.fichas.map((f) => {
      const tags = f.conhecido
        ? f.tracos_nomes.map((t) => `<span class="tag">${h(t)}</span>`).join("") + f.fraquezas.map((t) => `<span class="tag fraco">fraco: ${h(t)}</span>`).join("") +
          f.resiste.map((t) => `<span class="tag forte">resiste: ${h(t)}</span>`).join("")
        : '<span class="tag">??? derrote mais destas para aprender</span>';
      return `<div class="cartao${f.conhecido ? "" : " desconhecido"}${f.mestre ? " mestre" : ""}"><div class="cab">${S(iconeCriatura(f.tracos, f.id), 3)}
        <div><b>${h(f.nome)}</b><span class="sub">${f.abates} abate${f.abates === 1 ? "" : "s"}</span></div></div>
        <span class="lore">${h(f.lore)}</span><div class="tags">${f.mestre ? '<span class="tag mestre">mestre caçador +10% dano</span>' : ""}${tags}</div></div>`;
    }).join("");
    return `<div class="tela"><div class="meter" style="margin-bottom:10px">Criaturas conhecidas ${barra("xp", d.fichas.length, d.total)} ${d.fichas.length}/${d.total}</div><div class="cartas">${cartas}</div></div>`;
  }

  function comitiva(d) {
    const cartas = d.membros.map((m) => `<div class="cartao"><div class="cab">${S(m.id, 3)}<div><b>${h(m.nome)}</b><span class="sub">${h(m.titulo)}${m.ferido ? " · ferido, fora de combate" : ""}</span></div></div>
      <span class="lore">${h(m.desc)}</span>
      <div class="meter" style="margin-top:6px">Vida ${barra("aliado", m.hp, m.max_hp)} ${m.hp}/${m.max_hp}</div>
      ${aprovacao(m)}${m.conversa ? `<div class="tag" style="margin-top:6px;color:var(--ouro);border-color:#8a6a14">✉ quer conversar</div>` : ""}</div>`).join("");
    return `<div class="tela"><div class="cartas">${cartas}</div></div>`;
  }

  function barra(classe, atual, maximo) {
    const p = maximo ? Math.max(0, Math.min(100, (100 * atual) / maximo)) : 0;
    return `<span class="barra-px ${classe}"><span class="enchimento" style="width:${p}%"></span></span>`;
  }
  function aprovacao(m) {
    return `<div class="aprovacao ${h(m.classe)}"><span class="trilho"><span class="marca" style="left:${(m.aprovacao + 100) / 2}%"></span></span><span class="rotulo">${h(m.nivel)}</span></div>`;
  }

  function painel(m) {
    esconderDica();  // a tela foi redesenhada: a dica antiga ficaria órfã
    const div = document.createElement("div");
    div.innerHTML = ({ personagem, diario, bestiario, comitiva, loja }[m.tipo] || (() => ""))(m.dados);
    if (m.tipo === "personagem") ligarInventario(div);
    if (m.tipo === "loja") ligarLoja(div);
    ligarDicas(div);
    return div;
  }

  // ------------------------------------------------------------------ celebrações
  function particulas(cores, n = 60) {
    const cx = window.innerWidth / 2, cy = window.innerHeight * 0.42;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "particula";
      const ang = Math.random() * Math.PI * 2, dist = 120 + Math.random() * 320;
      p.style.left = cx + "px"; p.style.top = cy + "px";
      p.style.background = cores[i % cores.length];
      p.style.setProperty("--dx", Math.cos(ang) * dist + "px");
      p.style.setProperty("--dy", Math.sin(ang) * dist * 0.7 + "px");
      p.style.animationDelay = Math.random() * 0.25 + "s";
      document.body.appendChild(p);
      setTimeout(() => p.remove(), 1600);
    }
  }

  function faixa(titulo, sub, icone) {
    const f = document.createElement("div");
    f.className = "faixa-festa";
    f.innerHTML = `<b>${icone ? S(icone, 3) : ""}${h(titulo)}${icone ? S(icone, 3) : ""}</b>${sub ? `<span>${h(sub)}</span>` : ""}`;
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 1700);
  }

  /** Mostra a celebração. Devolve uma Promise que resolve quando o jogador fecha (ou na hora, se rápida). */
  function celebrar(m, instantaneo) {
    const d = m.dados;
    if (m.tipo === "vitoria") {
      if (instantaneo) return Promise.resolve();
      App.som("vitoria");
      faixa(d.chefe ? "Guardião derrotado!" : "Vitória", null, "espada");
      particulas(["#f2c94c", "#fff3a0", "#d4af37"], d.chefe ? 70 : 30);
      return new Promise((r) => setTimeout(r, d.chefe ? 1500 : 1000));
    }
    if (m.tipo === "comitiva") {
      if (instantaneo) return Promise.resolve();
      App.som("nivel");
      faixa(`${d.nome} se junta a você`, d.titulo, d.id);
      return new Promise((r) => setTimeout(r, 1500));
    }
    const caixa = document.getElementById("celebracao");
    let html = "";
    if (m.tipo === "nivel") {
      const icones = { Vida: "coracao", Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama", Mana: "pocao_azul", Vigor: "chama", Foco: "olho" };
      const ganhos = Object.entries(d.ganhos).map(([k, v], i) => `<span class="ganho" style="animation-delay:${0.5 + i * 0.18}s">${S(icones[k] || "estrela", 1)}+${v} ${h(k)}</span>`).join("");
      const atraso = 0.5 + Object.keys(d.ganhos).length * 0.18;
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${atraso + 0.4 + i * 0.25}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${h(x.desc)}</div>`).join("");
      html = `<div class="festa moldura"><div class="rotulo-festa">você subiu de nível</div><div class="grande">Nível ${d.nivel}</div>
        <div class="lista">${ganhos}<span class="ganho ouro" style="animation-delay:${atraso + 0.1}s">${S("estrela", 1)}+1 ponto de talento</span></div>${habs}
        ${d.especializacao ? '<div class="texto-festa" style="color:var(--arcano)">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}
        <div class="dica">Seus pontos de talento: ${d.pontos}. Gaste em Talentos (tecla T no menu de um local).</div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#f2c94c", "#fff3a0", "#ff9d4d", "#8fbf6a"], 90);
    } else if (m.tipo === "sigilo") {
      const los = [0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}${i === d.sigilos - 1 ? " novo" : ""}"></i>`).join("");
      html = `<div class="festa moldura"><div class="rotulo-festa">${h(d.guardiao)} caiu</div><div class="grande">Sigilo ${d.sigilos}/3</div>
        <div class="losangos">${los}</div><div class="texto-festa">Uma runa ardente se grava na sua mão. A corrupção recua.</div>
        <div class="lista"><span class="ganho ouro">${S("estrela", 1)}+1 ponto de talento</span></div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#f2c94c", "#ff4020", "#fff3a0"], 110);
    } else if (m.tipo === "spec") {
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${0.6 + i * 0.25}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${h(x.desc)}</div>`).join("");
      html = `<div class="festa moldura"><div class="rotulo-festa">você agora é</div><div class="grande arcano">${h(d.nome)}</div>
        <div class="texto-festa">${h(d.desc)}</div>${habs}<button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#b49cff", "#c8b0ff", "#ffffff"], 90);
    } else {
      return Promise.resolve();
    }
    if (instantaneo) return Promise.resolve();
    caixa.innerHTML = html;
    caixa.hidden = false;
    return new Promise((resolver) => {
      const fechar = () => {
        caixa.hidden = true; caixa.innerHTML = "";
        document.removeEventListener("keydown", tecla, true);
        resolver();
      };
      const tecla = (ev) => {
        if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); }
      };
      setTimeout(() => document.addEventListener("keydown", tecla, true), 600);
      caixa.querySelector(".continuar").addEventListener("click", (ev) => { ev.stopPropagation(); fechar(); });
    });
  }

  function toast(titulo, texto, icone, bom) {
    const t = document.createElement("div");
    t.className = "toast" + (bom ? " bom" : "");
    t.innerHTML = `${S(icone, 2)}<div>${titulo ? `<b>${h(titulo)}</b>` : ""}${h(texto || "")}</div>`;
    document.getElementById("toasts").appendChild(t);
    setTimeout(() => t.remove(), 3300);
  }

  return { guardarArvore, abrirTalentos, fecharTalentos, painel, celebrar, toast, iconeCriatura, iconeItem, dicaItem, ligarDicas, esconderDica,
    ICONE_ITEM, ARMA, VAZIO, NOME_ESPACO, AREA, barra, aprovacao };
})();
