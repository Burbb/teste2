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
  /** A caixa de dica é uma só; ela lembra quem a abriu. Se esse dono sai da tela (a cena trocou, o combate
   *  acabou) sem o mouse "sair" dele, um vigia fecha a dica em vez de deixá-la presa. */
  function caixaDica() {
    let caixa = document.getElementById("dica-item");
    if (!caixa) { caixa = document.createElement("div"); caixa.id = "dica-item"; caixa.className = "moldura"; caixa.hidden = true; document.body.appendChild(caixa); }
    return caixa;
  }
  let vigia = 0;
  function abrirDica(dono) {
    const caixa = caixaDica();
    caixa._dono = dono;
    caixa.hidden = false;
    clearInterval(vigia);
    vigia = setInterval(() => {
      if (caixa.hidden || !caixa._dono || !caixa._dono.isConnected || !caixa._dono.matches(":hover")) esconderDica();
    }, 250);
    return caixa;
  }
  function ligarDicas(raiz) {
    const caixa = caixaDica();
    raiz.querySelectorAll("[data-dica]").forEach((el) => {
      el.addEventListener("mouseenter", () => {
        caixa.innerHTML = dicas[Number(el.dataset.dica)] || "";
        caixa.classList.remove("ficha-inimigo");
        abrirDica(el);
        const r = el.getBoundingClientRect();
        const esq = r.right + 10 + 290 > window.innerWidth ? r.left - 300 : r.right + 10;
        caixa.style.left = Math.max(6, esq) + "px";
        caixa.style.top = Math.max(6, Math.min(window.innerHeight - caixa.offsetHeight - 6, r.top - 6)) + "px";
      });
      el.addEventListener("mouseleave", esconderDica);
    });
  }
  function esconderDica() {
    clearInterval(vigia);
    const c = document.getElementById("dica-item");
    if (c) { c.hidden = true; c._dono = null; c.classList.remove("ficha-inimigo"); }
  }

  // ------------------------------------------------------------------ inventário (boneco + mochila)
  function personagem(d) {
    const e = App.estado;
    if (!e) return "";
    const p = e.heroi;
    const limite = (d && d.limite) || p.limite_mochila || 12;
    const icAttr = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
    const attrs = atributosHtml(p);
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

  const ICONE_ATTR = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
  /** Atributos com dica: para que servem e o que você ganha com cada ponto. */
  function atributosHtml(p) {
    const info = p.atributos_info || {};
    return Object.entries(p.atributos).map(([k, v]) => {
      const linhas = (info[k] || []).map((l) => `<li>${h(l)}</li>`).join("");
      return `<div class="atributo" ${dica(`<b>${h(k)} ${v}</b><ul class="dica-lista">${linhas}</ul>`)}>${S(ICONE_ATTR[k] || "estrela", 1)}<span class="nome">${h(k)}</span><span class="valor">${v}</span></div>`;
    }).join("");
  }
  function reputacaoHtml(p) {
    const r = p.reputacao_info || { titulo: "", linhas: [] };
    return `<div class="linha reputacao" ${dica(`<b>Reputação ${p.reputacao > 0 ? "+" : ""}${p.reputacao}</b><div class="tipo">${h(r.titulo)}</div><ul class="dica-lista">${r.linhas.map((l) => `<li>${h(l)}</li>`).join("")}</ul>`)}>
      <span>Reputação</span><b>${p.reputacao > 0 ? "+" : ""}${p.reputacao} <small>${h(r.titulo)}</small></b></div>`;
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
  const qtdLoja = {};  // quantidade escolhida em cada suprimento (sobrevive ao redesenho da tela)
  function maxCompra(c, ouro) { return Math.max(0, Math.min(99, c.limite ?? 99, Math.floor(ouro / c.preco))); }
  function loja(d) {
    const cons = d.consumiveis.map((c) => {
      const max = maxCompra(c, d.ouro);
      const q = Math.max(1, Math.min(qtdLoja[c.id] || 1, max || 1));
      const caro = max < 1;
      const icone = c.id === "provisoes" ? "pernil" : c.id === "flechas" ? "aljava" : (ICONE_ITEM[c.id] || "pocao");
      return `<div role="button" tabindex="0" class="mercadoria suprimento${caro ? " caro" : ""}" data-comprar="${h(c.id)}" data-preco="${c.preco}" data-max="${max}" ${dica(`<b>${h(c.nome)}</b><div>${h(c.desc)}</div><div class="rodape">${caro ? (c.limite === 0 ? "Você não carrega mais." : "Ouro insuficiente.") : "Escolha a quantidade e clique para comprar. Shift+clique compra 5."}</div>`)}>
        <span class="slot-px">${S(icone, 2)}${c.tem ? `<span class="qtd">${c.tem}</span>` : ""}</span>
        <span class="merc-nome">${h(c.nome)}</span>
        <span class="preco">${S("moeda", 1)}<span class="total">${c.preco * q}</span></span>
        <span class="qtd-ctrl"><button type="button" data-q="-1" aria-label="menos">−</button><b>${q}</b><button type="button" data-q="1" aria-label="mais">+</button></span></div>`;
    }).join("");
    const equips = d.equipamentos.map((it, i) => {
      const caro = it.preco > d.ouro;
      return `<button type="button" class="mercadoria equip${caro ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, caro ? "Ouro insuficiente." : "Clique para comprar. Se o espaço do corpo estiver vazio, você já sai vestindo.")}>
        <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
        <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span><span class="preco">${S("moeda", 1)}${it.preco}</span></button>`;
    }).join("");
    const mochila = d.mochila.map((it, i) => `<div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.usavel ? "" : " inutil"}" draggable="true" data-mochila-loja="${i}" ${dicaItem(it, "Clique para equipar ou vender.")}>${S(iconeItem(it), 2)}</div>`);
    for (let i = d.mochila.length; i < d.limite; i++) mochila.push('<div class="slot-px celula vazia"></div>');
    return `<div class="tela loja">
      <div class="loja-topo">${S("saco", 3)}<div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
        <span class="ouro-loja">${S("moedas", 2)}${d.ouro}</span></div>
      <div class="balcao">
        <h4>Suprimentos</h4><div class="vitrine">${cons}</div>
        <h4>Equipamentos</h4><div class="vitrine">${equips || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>'}</div>
      </div>
      <h4>Sua mochila <small>${d.ocupado}/${d.limite} · clique num item para equipar ou vender (o mercador paga metade)</small></h4>
      <div class="mochila-grade mochila-loja">${mochila.join("")}</div></div>`;
  }

  function fecharMenuItem() { document.querySelectorAll(".menu-item").forEach((m) => m.remove()); }
  function menuItem(ancora, it, i) {
    fecharMenuItem();
    esconderDica();
    const m = document.createElement("div");
    m.className = "menu-item moldura";
    m.innerHTML = `<b class="r-${h(it.raridade)}">${h(it.nome)}</b>
      ${it.usavel ? `<button type="button" data-a="equipar">${S("armadura", 1)} Equipar</button>` : '<span class="pior">Não é para a sua classe.</span>'}
      <button type="button" data-a="vender" class="vender">${S("moeda", 1)} Vender por ${it.preco}</button>
      <button type="button" data-a="nada" class="secundaria">Cancelar</button>`;
    document.body.appendChild(m);
    const r = ancora.getBoundingClientRect();
    m.style.left = Math.max(8, Math.min(innerWidth - m.offsetWidth - 8, r.left)) + "px";
    m.style.top = (r.bottom + 6 + m.offsetHeight > innerHeight ? r.top - m.offsetHeight - 6 : r.bottom + 6) + "px";
    m.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b) return;
      ev.stopPropagation();
      fecharMenuItem();
      if (b.dataset.a === "equipar") App.acao({ equipar: i }, "equipar");
      else if (b.dataset.a === "vender") App.acao({ vender: i }, "moeda");
    });
    setTimeout(() => document.addEventListener("click", fecharMenuItem, { once: true }), 0);
  }

  function ligarLoja(raiz) {
    const dados = App.ultimaLoja;
    raiz.querySelectorAll("[data-comprar]").forEach((el) => {
      const preco = Number(el.dataset.preco), max = Number(el.dataset.max), id = el.dataset.comprar;
      const num = el.querySelector(".qtd-ctrl b"), total = el.querySelector(".total");
      const mudar = (q) => {
        q = Math.max(1, Math.min(max || 1, q));
        qtdLoja[id] = q; num.textContent = q; total.textContent = preco * q;
      };
      el.querySelectorAll("[data-q]").forEach((b) => {
        let rep = null;
        const passo = () => mudar((qtdLoja[id] || 1) + Number(b.dataset.q));
        b.addEventListener("click", (ev) => { ev.stopPropagation(); });
        b.addEventListener("pointerdown", (ev) => {
          ev.stopPropagation(); passo(); App.som("escolha");
          rep = setTimeout(function repetir() { passo(); rep = setTimeout(repetir, 70); }, 380);  // segurar acelera
        });
        ["pointerup", "pointerleave", "pointercancel"].forEach((t) => b.addEventListener(t, () => clearTimeout(rep)));
      });
      el.addEventListener("wheel", (ev) => { if (max > 1) { ev.preventDefault(); mudar((qtdLoja[id] || 1) + (ev.deltaY < 0 ? 1 : -1)); } }, { passive: false });
      const comprar = (ev) => {
        if (el.classList.contains("caro")) { App.som("falha"); return; }
        const q = ev.shiftKey ? Math.min(5, max) : Math.min(qtdLoja[id] || 1, max);
        qtdLoja[id] = 1;
        App.acao({ comprar: id }, "moeda", { qtd: q });
      };
      el.addEventListener("click", (ev) => { if (!ev.target.closest(".qtd-ctrl")) comprar(ev); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") comprar(ev); });
    });
    raiz.querySelectorAll("[data-comprar-item]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); if (!el.classList.contains("caro")) App.acao({ comprar_item: Number(el.dataset.comprarItem) }, "moeda"); else App.som("falha"); }));
    // Mochila: clique abre um menu (equipar / vender); arrastar só vende se soltar no balcão do mercador.
    let vendendo = null;
    const balcao = raiz.querySelector(".balcao");
    raiz.querySelectorAll("[data-mochila-loja]").forEach((el) => {
      const i = Number(el.dataset.mochilaLoja);
      const it = dados && dados.mochila[i];
      el.addEventListener("click", (ev) => { ev.stopPropagation(); if (it) menuItem(el, it, i); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter" && it) menuItem(el, it, i); });
      el.addEventListener("dragstart", (ev) => { esconderDica(); fecharMenuItem(); vendendo = i; ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null) App.acao({ vender: vendendo }, "moeda");
      vendendo = null;
    });
  }

  function diario(d) {
    const contratos = d.contratos.map((c) => cartaz(c, true, false, d.nivel_heroi)).join("");
    const rumores = d.rumores.map((r) => `<div class="bilhete"><span class="prego"></span>${S("olho", 1)} ${h(r.texto)}<small>${r.expira > 0 ? `some em ${r.expira} dia${r.expira === 1 ? "" : "s"}` : "some hoje"}</small></div>`).join("");
    const losangos = [0, 1, 2].map((i) => `<i class="sigilo${i < d.sigilos ? " tem" : ""}"></i>`).join("");
    return `<div class="tela diario">
      <div class="faixa-jornada"><span>Dia ${d.dia}</span><span class="sigilos-diario" title="Sigilos dos guardiões">${losangos} ${d.sigilos}/3</span>
        <span title="Corrupção do reino">Corrupção ${barra("corrupcao", d.corrupcao, 100)} ${d.corrupcao}%</span></div>
      <div class="quadro"><div class="quadro-cab"><b>Contratos</b><span>${d.contratos.length}/${d.limite} · os lugares ficam marcados no mapa</span></div>
        <div class="cartazes">${contratos || '<span class="vazio">Nenhum contrato. Procure o mural de uma vila.</span>'}</div></div>
      ${rumores ? `<h4>Rumores</h4><div class="bilhetes">${rumores}</div>` : ""}
      ${d.nemesis ? `<h4>Quem te persegue</h4><div class="bilhete inimigo">${S("fera", 1)} ${h(d.nemesis.nome)}, ${h(d.nemesis.familia)}. Ele não esqueceu de você.</div>` : ""}
    </div>`;
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

  function cartaoMembro(m, reserva) {
    return `<div class="cartao clicavel${reserva ? " na-reserva" : ""}" data-cid="${h(m.id)}"><div class="cab">${S(m.id, 3)}<div><b>${h(m.nome)}</b><span class="sub">${h(m.titulo)}${m.ferido ? " · ferido, fora de combate" : ""}${reserva ? " · no acampamento" : ""}</span></div></div>
      <span class="lore">${h(m.desc)}</span>
      <div class="meter" style="margin-top:6px">Vida ${barra("vida", m.hp, m.max_hp)} ${m.hp}/${m.max_hp}</div>
      ${aprovacao(m)}${m.conversa && !reserva ? '<div class="tag aviso-conversa">✉ quer conversar · clique</div>' : ""}</div>`;
  }
  function comitiva(d) {
    const cartas = d.membros.map((m) => cartaoMembro(m, false)).join("");
    const reserva = (d.reserva || []).map((m) => cartaoMembro(m, true)).join("");
    return `<div class="tela"><div class="cartas">${cartas}</div>
      ${reserva ? `<h4>No acampamento <small>chame de volta quando montar a fogueira</small></h4><div class="cartas">${reserva}</div>` : ""}
      <div class="dica-uso">Clique num companheiro para conversar ou mandar para o acampamento.</div></div>`;
  }

  // ------------------------------------------------------------------ mural de contratos
  const TIPO_CONTRATO = { caca: "Caça", alvo: "Procurado", entrega: "Entrega" };
  function cartaz(c, ativo, cheio, nivelHeroi) {
    const arte = c.tipo === "entrega" ? "saco" : iconeCriatura(c.tracos, c.familia || "");
    const titulo = c.tipo === "alvo" ? c.alvo : c.tipo === "entrega" ? (c.objeto || "Entrega") : c.desc.replace(/^Eliminar /, "").replace(/ em .*$/, "");
    const perigo = c.nivel == null ? "" : c.nivel - nivelHeroi >= 2 ? "alto" : c.nivel >= nivelHeroi ? "medio" : "baixo";
    const lugar = `${S(MapaPx.sprite({ tipo: c.lugar_tipo, bioma: c.bioma }), 1)} ${h(c.lugar)}${c.distancia != null ? ` · ${c.distancia} trecho${c.distancia === 1 ? "" : "s"}` : ""}${c.nivel != null ? ` <span class="perigo-tag ${perigo}">Nv.${c.nivel}</span>` : ""}`;
    let progresso = "";
    if (ativo && c.tipo === "caca" && c.progresso) {
      const [feito, total] = c.progresso.split("/").map(Number);
      progresso = `<div class="contrato-progresso">${barra("xp", feito, total)}<span>${feito}/${total}</span></div>`;
    }
    let botao;
    if (ativo) botao = c.concluido ? '<span class="contrato-feito">Feito! Volte a uma vila para receber</span>'
      : `<button type="button" class="contrato-botao abandonar" data-abandonar="${c.id}" title="Reputação −${c.penalidade}">Abandonar</button>`;
    else botao = `<button type="button" class="contrato-botao" data-aceitar="${c.id}"${cheio ? " disabled title=\"Você já tem 3 contratos\"" : ""}>Aceitar</button>`;
    return `<div class="contrato tipo-${h(c.tipo)}${ativo ? " ativo" : ""}${c.concluido ? " concluido" : ""}">
      <span class="prego"></span><div class="contrato-tipo">${TIPO_CONTRATO[c.tipo] || h(c.tipo)}</div>
      <div class="contrato-arte">${S(arte, 3)}</div>
      <div class="contrato-titulo">${h(titulo)}</div>
      <div class="contrato-desc">${h(c.desc)}</div>
      <div class="contrato-lugar">${lugar}</div>${progresso}
      <div class="contrato-premio"><span>${S("moeda", 1)} ${c.ouro}</span><span>${S("estrela", 1)} ${c.xp} XP</span></div>
      ${botao}</div>`;
  }
  function mural(d) {
    const cheio = d.ativos.length >= d.limite;
    const oferta = d.oferta.map((c) => cartaz(c, false, cheio, d.nivel_heroi)).join("");
    const ativos = d.ativos.map((c) => cartaz(c, true, cheio, d.nivel_heroi)).join("");
    return `<div class="tela mural">
      <div class="quadro"><div class="quadro-cab"><b>Contratos</b><span>${d.renova ? `novos cartazes em ${d.renova} dia${d.renova === 1 ? "" : "s"}` : "cartazes novos amanhã"}</span></div>
        <div class="cartazes">${oferta || '<span class="vazio">O mural está vazio. Volte em alguns dias.</span>'}</div></div>
      <h4>Seus contratos <small>${d.ativos.length}/${d.limite}</small></h4>
      <div class="cartazes seus">${ativos || '<span class="vazio">Nenhum. Pegue um cartaz do mural.</span>'}</div></div>`;
  }
  function ligarMural(raiz) {
    raiz.querySelectorAll("[data-aceitar]").forEach((b) => b.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ aceitar: Number(b.dataset.aceitar) }, "pagina"); }));
    raiz.querySelectorAll("[data-abandonar]").forEach((b) => b.addEventListener("click", (ev) => { ev.stopPropagation(); App.acao({ abandonar: Number(b.dataset.abandonar) }, "escolha"); }));
  }

  /** Rastreador sempre à vista: alvo, lugar, distância e progresso de cada contrato. */
  function rastreador(contratos, nivelHeroi) {
    if (!contratos || !contratos.length) return "";
    return `<div class="secao rastreador"><h3>Contratos</h3>${contratos.map((c) => {
      const arte = c.tipo === "entrega" ? "saco" : iconeCriatura(c.tracos, c.familia || "");
      const alvo = c.tipo === "alvo" ? c.alvo : c.tipo === "entrega" ? `Levar ${c.objeto}` : c.desc.replace(/^Eliminar /, "").replace(/ em .*$/, "");
      let prog = "";
      if (c.tipo === "caca" && c.progresso) { const [f, t] = c.progresso.split("/").map(Number); prog = `${barra("xp", f, t)}<small>${f}/${t}</small>`; }
      const perigo = c.nivel == null ? "" : c.nivel - nivelHeroi >= 2 ? "alto" : c.nivel >= nivelHeroi ? "medio" : "baixo";
      return `<div class="rastro-contrato${c.concluido ? " feito" : ""}" data-local="${c.lugar_id}" data-contrato="${c.id}" title="${h(c.desc)}">
        <span class="rastro-arte">${S(arte, 2)}</span>
        <span class="rastro-info"><b>${h(alvo)}</b>
          <span class="rastro-lugar">${c.concluido ? "Feito! Receba numa vila" : `${h(c.lugar)}${c.distancia ? ` · ${c.distancia} trecho${c.distancia === 1 ? "" : "s"}` : c.distancia === 0 ? " · você está aqui" : ""}`}${c.nivel != null && !c.concluido ? ` <span class="perigo-tag ${perigo}">Nv.${c.nivel}</span>` : ""}</span>
          ${prog ? `<span class="rastro-prog">${prog}</span>` : ""}</span></div>`;
    }).join("")}</div>`;
  }

  // ------------------------------------------------------------------ acampamento (fogueira)
  const PONTOS_ATIVOS = [[198, 93], [176, 104]];
  const PONTOS_RESERVA = [[256, 98], [284, 102], [270, 108]];
  function acampamento(d) {
    const figuras = [];
    d.ativos.forEach((m, i) => figuras.push({ ...m, onde: "ativo", p: PONTOS_ATIVOS[i % 2] }));
    d.reserva.forEach((m, i) => figuras.push({ ...m, onde: "reserva", p: PONTOS_RESERVA[i % 3] }));
    const botoes = figuras.map((f) => `<button type="button" class="figura ${f.onde}${f.conversa ? " tem-conversa" : ""}" data-cid="${h(f.id)}"
        style="left:${(f.p[0] / 320) * 100}%;top:${((f.p[1] + 8) / 120) * 100}%">
        ${f.conversa ? '<i class="carta-aviso">✉</i>' : ""}<span class="figura-nome">${h(f.nome.split(" ").pop())}</span>
        <span class="figura-estado">${f.onde === "ativo" ? "vai com você" : "no acampamento"}</span></button>`).join("");
    return `<div class="tela acampamento"><div class="fogueira-palco"><canvas class="fogueira-cena" width="320" height="120"></canvas>${botoes}</div>
      <div class="dica-uso">Clique em alguém para conversar ou decidir quem vai com você amanhã. Quem fica no acampamento descansa, não come das suas provisões e não opina nas suas escolhas. ${d.ativos.length}/${d.limite} na comitiva.</div></div>`;
  }

  function desenharFogueira(canvas, d) {
    const x = canvas.getContext("2d");
    const W = 320, H = 120;
    const px = (cx, cy, w, hh, cor) => { x.fillStyle = cor; x.fillRect(cx | 0, cy | 0, w, hh); };
    const heroi = App.estado && App.estado.heroi;
    const quem = [[heroi ? heroi.classe : "guerreiro", 128, 93]];
    d.ativos.forEach((m, i) => quem.push([m.id, ...PONTOS_ATIVOS[i % 2]]));
    d.reserva.forEach((m, i) => quem.push([m.id, ...PONTOS_RESERVA[i % 3]]));
    let quadro = 0, timer = null;
    function cena(primeira) {
      if (!primeira && !canvas.isConnected) { clearInterval(timer); return; }  // a tela saiu: para de animar
      quadro++;
      const vista = document.getElementById("vista");
      if (vista) x.drawImage(vista, 0, 0, W, 72); else px(0, 0, W, 72, "#080b1a");
      // chão escuro com pontilhado
      for (let y = 72; y < H; y++) px(0, y, W, 1, y < 76 ? "#14100c" : "#0d0b09");
      for (let y = 78; y < H; y += 2) for (let i = (y * 7) % 5; i < W; i += 5) px(i, y, 1, 1, "#1a140f");
      // luz da fogueira: anéis pontilhados que tremem
      const raio = 46 + Math.sin(quadro / 2) * 2 + (Math.random() * 2);
      for (let y = 74; y < H; y++) for (let i = 80; i < 240; i++) {
        const dx = (i - 160) / raio, dy = (y - 98) / (raio * 0.45), d2 = dx * dx + dy * dy;
        if (d2 < 1 && ((i + y) % 2 === 0 || d2 < 0.45)) px(i, y, 1, 1, d2 < 0.2 ? "#5a2e12" : d2 < 0.5 ? "#3a2010" : "#24160c");
      }
      // barraca do acampamento
      for (let k = 0; k < 18; k++) px(262 - k, 80 + k, k * 2 + 1 > 36 ? 36 : 1, 1, "#2a2016");
      for (let k = 0; k < 18; k++) { px(262 - k, 80 + k, 1, 1, "#4a3a28"); px(262 + k, 80 + k, 1, 1, "#4a3a28"); px(263 - k, 80 + k, k * 2 - 1 > 0 ? k * 2 - 1 : 0, 1, "#1a140e"); }
      px(259, 90, 6, 8, "#0d0b0a");
      // toras e fogo
      px(148, 100, 24, 3, "#4a2c14"); px(152, 98, 16, 2, "#5a3a1c");
      for (let i = 0; i < 9; i++) {
        const fx = 150 + i * 2.4, alt = 6 + Math.random() * 10 + (i > 2 && i < 7 ? 6 : 0);
        px(fx, 98 - alt, 2, alt, "#b3262b"); px(fx, 98 - alt * 0.75, 2, alt * 0.75, "#e0782f");
        if (i > 1 && i < 8) px(fx, 98 - alt * 0.45, 2, alt * 0.45, "#ffd27a");
      }
      for (let i = 0; i < 4; i++) {  // fagulhas e fumaça
        const t = (quadro * 2 + i * 13) % 40;
        px(158 + Math.sin((quadro + i * 7) / 3) * 4, 80 - t, 1, 1, t < 20 ? "#ffb35c" : "rgba(160,150,140,0.5)");
      }
      // figuras, iluminadas pelo fogo
      quem.forEach(([nomeSpr, fx, fy]) => {
        const spr = Sprites.canvas(nomeSpr);
        px(fx - 7, fy + 6, 14, 2, "rgba(0,0,0,0.5)");
        if (spr) x.drawImage(spr, fx - 8, fy - 9, 16, 16);
      });
    }
    cena(true);
    timer = setInterval(() => { if (!document.hidden) cena(); }, 125);
  }

  function menuFigura(ancora, cid) {
    fecharMenuItem();
    const ops = App.opcoes() || [];
    const nomeDe = (id) => (App.estado.heroi.comitiva.concat(App.ultimaFogueira ? App.ultimaFogueira.reserva : []).find((m) => m.id === id) || {}).nome || id;
    const itens = [];
    ops.forEach((o) => {
      const m = o.meta || {};
      if (m.conversar === cid) itens.push([`${S("pergaminho", 1)} Conversar${/✉/.test(o.texto) ? " ✉" : ""}`, { conversar: cid }]);
      if (m.chamar === cid && !m.sai) itens.push([`${S("espada", 1)} Levar amanhã`, { chamar: cid }]);
      if (m.chamar === cid && m.sai) itens.push([`${S("espada", 1)} Levar no lugar de ${h(nomeDe(m.sai).split(" ").pop())}`, { chamar: cid, sai: m.sai }]);
      if (m.reservar === cid) itens.push([`${S("fogueira", 1)} Deixar no acampamento`, { reservar: cid }]);
      if (m.acampamento === cid) itens.push([`${S("fogueira", 1)} Mandar para o acampamento`, { acampamento: cid }]);
    });
    if (!itens.length) return;
    const menu = document.createElement("div");
    menu.className = "menu-item moldura";
    menu.innerHTML = `<b>${h(nomeDe(cid))}</b>` + itens.map(([t], i) => `<button type="button" data-i="${i}">${t}</button>`).join("") +
      '<button type="button" class="secundaria" data-i="-1">Cancelar</button>';
    document.body.appendChild(menu);
    const r = ancora.getBoundingClientRect();
    menu.style.left = Math.max(8, Math.min(innerWidth - menu.offsetWidth - 8, r.left)) + "px";
    menu.style.top = (r.bottom + 6 + menu.offsetHeight > innerHeight ? r.top - menu.offsetHeight - 6 : r.bottom + 6) + "px";
    menu.addEventListener("click", (ev) => {
      const b = ev.target.closest("button");
      if (!b) return;
      ev.stopPropagation();
      fecharMenuItem();
      const i = Number(b.dataset.i);
      if (i >= 0) App.acao(itens[i][1], "escolha");
    });
    setTimeout(() => document.addEventListener("click", fecharMenuItem, { once: true }), 0);
  }

  function ligarFigurasComitiva(raiz) {
    raiz.querySelectorAll("[data-cid].figura, .cartao[data-cid]").forEach((el) => {
      el.addEventListener("click", (ev) => { ev.stopPropagation(); menuFigura(el, el.dataset.cid); });
    });
  }

  function barra(classe, atual, maximo) {
    const p = maximo ? Math.max(0, Math.min(100, (100 * atual) / maximo)) : 0;
    return `<span class="barra-px ${classe}"><span class="enchimento" style="width:${p}%"></span></span>`;
  }
  function aprovacao(m) {
    const info = (m.aprovacao_info || []).map((l) => `<li>${h(l)}</li>`).join("");
    return `<div class="aprovacao ${h(m.classe)}" ${dica(`<b>Aprovação de ${h(m.nome.split(" ").pop())}</b><div class="tipo">${h(m.nivel)} · ${m.aprovacao > 0 ? "+" : ""}${m.aprovacao}</div><ul class="dica-lista">${info}</ul><div class="rodape">Roxo: desconfiança · verde: confiança.</div>`)}><span class="trilho"><span class="marca" style="left:${(m.aprovacao + 100) / 2}%"></span></span><span class="rotulo">${h(m.nivel)}</span></div>`;
  }

  function painel(m) {
    esconderDica();  // a tela foi redesenhada: a dica antiga ficaria órfã
    const div = document.createElement("div");
    div.innerHTML = ({ personagem, diario, bestiario, comitiva, loja, acampamento, mural }[m.tipo] || (() => ""))(m.dados);
    if (m.tipo === "acampamento") { App.ultimaFogueira = m.dados; desenharFogueira(div.querySelector(".fogueira-cena"), m.dados); }
    if (m.tipo === "acampamento" || m.tipo === "comitiva") ligarFigurasComitiva(div);
    if (m.tipo === "mural" || m.tipo === "diario") ligarMural(div);
    if (m.tipo === "personagem") ligarInventario(div);
    if (m.tipo === "loja") { App.ultimaLoja = m.dados; ligarLoja(div); }
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

  return { rastreador, atributosHtml, reputacaoHtml, dica, abrirDica, fecharMenuItem, guardarArvore, abrirTalentos, fecharTalentos, painel, celebrar, toast, iconeCriatura, iconeItem, dicaItem, ligarDicas, esconderDica,
    ICONE_ITEM, ARMA, VAZIO, NOME_ESPACO, AREA, barra, aprovacao };
})();
