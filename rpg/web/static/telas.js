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
  const ICONE_ITEM = { pocao_vida: "pocao", tonico: "pocao_azul", antidoto: "folha", bandagem: "bandagem", unguento: "unguento",
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
    ranksAntes = Object.fromEntries(a.nos.map((n) => [n.id, n.rank]));
    const info = document.getElementById("talento-info");
    document.querySelectorAll("#arvore .no-talento").forEach((el) => {
      const n = a.nos.find((x) => x.id === el.dataset.id);
      el.addEventListener("mouseenter", () => {
        info.innerHTML = `<b>${h(n.nome)}</b><div class="r">Grau ${n.rank} de ${n.max}${n.spec ? " · " + h(n.spec) : ""}</div><div>${Realce.texto(n.desc)}</div>` +
          (n.motivo ? `<div class="req">${h(n.motivo[0].toUpperCase() + n.motivo.slice(1))}</div>` : "") +
          (n.estado === "comprado" ? '<div class="acao">Aprendido por completo.</div>' :
            n.estado === "disponivel" ? (a.pontos ? '<div class="acao">Clique para aprender (1 ponto).</div>' : '<div class="req">Sem pontos de talento.</div>') : "");
        info.hidden = false;
        const r = el.getBoundingClientRect();
        info.style.left = Math.min(window.innerWidth - 320, r.right + 12) + "px";
        info.style.top = Math.max(10, r.top - 10) + "px";
      });
      el.addEventListener("mouseleave", () => { info.hidden = true; });
      if (el.classList.contains("pode")) el.addEventListener("click", () => {
        info.hidden = true;
        // Resposta na hora do clique, como no mercado: pop, faíscas, som e o ganho subindo perto do nó.
        App.som("aprender");
        el.animate([{ scale: 1 }, { scale: 1.28, filter: "brightness(2.2)" }, { scale: 1 }], { duration: 260, easing: "cubic-bezier(.2,.8,.3,1.2)" });
        faiscas(el, ["#f2c94c", "#fff3a0", "#8fbf6a"], 18);
        App.avisar(`+1 ${n.nome} (${n.rank + 1}/${n.max})`);
        const pontos = document.querySelector("#arvore .pontos");
        if (pontos) pontos.animate([{ scale: 1 }, { scale: 0.8, filter: "brightness(2)" }, { scale: 1 }], { duration: 220 });
        App.responder(m.id, idx[n.id]);
      });
    });
    caixa.hidden = false;
    return true;
  }
  /** Faíscas que saem de um elemento (talento aprendido, compra...). */
  function faiscas(el, cores, n = 14) {
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "faisca";
      p.style.left = cx + "px"; p.style.top = cy + "px";
      p.style.background = cores[i % cores.length];
      document.body.appendChild(p);
      const ang = (i / n) * Math.PI * 2 + Math.random() * 0.4, dist = 40 + Math.random() * 46;
      p.animate([{ transform: "translate(-50%, -50%) scale(1)", opacity: 1 },
        { transform: `translate(calc(-50% + ${Math.cos(ang) * dist}px), calc(-50% + ${Math.sin(ang) * dist}px)) scale(0.4)`, opacity: 0 }],
        { duration: 420 + Math.random() * 180, easing: "cubic-bezier(.15,.7,.3,1)" }).finished.then(() => p.remove(), () => p.remove());
    }
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
  const NOMES_STAT = { max_hp: "Vida", atk: "Ataque", defesa: "Defesa", agi: "Agilidade", poder: "Poder", get max_rec() { return (App.estado && App.estado.heroi && App.estado.heroi.recurso) || "Mana/Vigor/Foco"; },
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

  const dicas = new Map();
  let proximaDica = 0;
  /** Guarda o HTML de uma dica e devolve o id (para elementos montados via DOM). Os ids nunca se repetem;
   *  as dicas mais antigas (que já não estão na tela) são esquecidas aos poucos. */
  function guardarDica(html) {
    if (dicas.size > 3000) {
      for (const k of [...dicas.keys()].slice(0, 2000)) { dicas.delete(k); itensDica.delete(k); dicasCurtas.delete(k); }
    }
    dicas.set(proximaDica, html);
    return proximaDica++;
  }
  const dicasCurtas = new Set();  // dicas de uma linha (ouro, barras do HUD): caixinha preta sutil em cima do elemento
  function dica(html, curta = false) {
    const id = guardarDica(html);
    if (curta) dicasCurtas.add(id);
    return `data-dica="${id}"`;
  }
  const itensDica = new Map();  // id da dica → item, para o Shift mostrar o equipado ao lado
  function dicaItem(it, rodape = "", comparando = true) {
    const id = guardarDica(htmlItem(it, rodape, comparando));
    if (comparando) itensDica.set(id, it);
    return `data-dica="${id}"`;
  }
  /** Os itens que o herói está usando no(s) espaço(s) onde `it` iria. */
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
  /** A caixa de dica é uma só; ela lembra quem a abriu. Se esse dono sai da tela (a cena trocou, o combate
   *  acabou) sem o mouse "sair" dele, um vigia fecha a dica em vez de deixá-la presa. */
  function caixaDica() {
    let caixa = document.getElementById("dica-item");
    if (!caixa) { caixa = document.createElement("div"); caixa.id = "dica-item"; caixa.className = "moldura"; caixa.hidden = true; document.body.appendChild(caixa); }
    return caixa;
  }
  let vigia = 0;
  const mouse = { x: -1, y: -1 };
  window.addEventListener("mousemove", (ev) => { mouse.x = ev.clientX; mouse.y = ev.clientY; }, { capture: true, passive: true });
  /** `presa`: a dica fica presa ao LUGAR onde o dono estava quando o mouse chegou (a carta de um inimigo avança
   *  para atacar e volta; a ficha não vai atrás dela). Some quando o mouse sai daquele lugar. */
  function abrirDica(dono, presa = false) {
    const caixa = caixaDica();
    caixa._dono = dono;
    caixa._area = presa ? dono.getBoundingClientRect() : null;
    caixa.hidden = false;
    clearInterval(vigia);
    vigia = setInterval(() => {
      const dentro = caixa._area ? mouseNaArea() : caixa._dono && caixa._dono.matches(":hover");
      if (caixa.hidden || !caixa._dono || !caixa._dono.isConnected || !dentro) esconderDica();
    }, 250);
    return caixa;
  }
  function mouseNaArea() {
    const c = document.getElementById("dica-item"), r = c && c._area;
    return !!r && mouse.x >= r.left && mouse.x <= r.right && mouse.y >= r.top && mouse.y <= r.bottom;
  }
  function dicaAbertaPor(el) {
    const c = document.getElementById("dica-item");
    return !!c && !c.hidden && c._dono === el;
  }
  function ligarDicas(raiz) {
    const caixa = caixaDica();
    raiz.querySelectorAll("[data-dica]").forEach((el) => {
      el.addEventListener("mouseenter", (ev) => {
        const id = Number(el.dataset.dica);
        caixa.innerHTML = dicas.get(id) || "";
        caixa.classList.remove("ficha-inimigo");
        caixa.classList.toggle("curta", dicasCurtas.has(id));
        caixa._item = itensDica.get(id) || null;
        caixa._esquerda = false;
        abrirDica(el);
        const r = el.getBoundingClientRect();
        if (dicasCurtas.has(id)) {  // centrada logo abaixo do elemento, sem cobrir o que ele mostra
          caixa.style.left = Math.max(6, Math.min(window.innerWidth - caixa.offsetWidth - 6, r.left + r.width / 2 - caixa.offsetWidth / 2)) + "px";
          caixa.style.top = Math.min(window.innerHeight - caixa.offsetHeight - 6, r.bottom + 6) + "px";
          return;
        }
        caixa._esquerda = r.right + 10 + 290 > window.innerWidth;
        const esq = caixa._esquerda ? r.left - 300 : r.right + 10;
        caixa.style.left = Math.max(6, esq) + "px";
        caixa.style.top = Math.max(6, Math.min(window.innerHeight - caixa.offsetHeight - 6, r.top - 6)) + "px";
        mostrarEquipado(ev.shiftKey);
      });
      el.addEventListener("mouseleave", esconderDica);
    });
  }
  /** Com Shift seguro, o item que você usa naquele espaço abre ao lado da dica, inteiro (não só a diferença). */
  function mostrarEquipado(ligado) {
    const caixa = document.getElementById("dica-item");
    let lado = document.getElementById("dica-equipado");
    const eq = ligado && caixa && !caixa.hidden && caixa._item ? equipadosPara(caixa._item) : [];
    if (!eq.length) { if (lado) lado.hidden = true; return; }
    if (!lado) { lado = document.createElement("div"); lado.id = "dica-equipado"; lado.className = "moldura"; document.body.appendChild(lado); }
    lado.innerHTML = eq.map((it, i) => `<div class="${i ? "outro" : ""}"><span class="selo-equipado">Equipado</span>${htmlItem(it, "", false)}</div>`).join("");
    lado.hidden = false;
    const r = caixa.getBoundingClientRect();
    const larg = lado.offsetWidth || 280;
    // Fica do lado oposto ao do item, para não cobrir o que você está olhando.
    let esq = caixa._esquerda ? r.left - larg - 8 : r.right + 8;
    if (esq + larg > window.innerWidth - 6) esq = r.left - larg - 8;
    if (esq < 6) esq = r.right + 8;
    lado.style.left = Math.max(6, esq) + "px";
    lado.style.top = Math.max(6, Math.min(window.innerHeight - lado.offsetHeight - 6, r.top)) + "px";
  }
  window.addEventListener("keydown", (e) => { if (e.key === "Shift" && !e.repeat) mostrarEquipado(true); });
  window.addEventListener("keyup", (e) => { if (e.key === "Shift") mostrarEquipado(false); });
  window.addEventListener("blur", () => mostrarEquipado(false));
  function esconderDica() {
    clearInterval(vigia);
    const c = document.getElementById("dica-item");
    if (c) { c.hidden = true; c._dono = null; c._item = null; c._area = null; c.classList.remove("ficha-inimigo", "curta"); }
    const lado = document.getElementById("dica-equipado");
    if (lado) lado.hidden = true;
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
    const bolsa = p.bolsa.map((b) => `<div class="slot-px clicavel" data-usar="${h(b.id)}" ${dica(`<b>${h(b.nome)}</b><div>${Realce.texto(b.desc)}</div>${b.id === "tocha" ? "" : '<div class="rodape">Clique para usar · botão direito: usar em você.</div>'}`)}>${S(ICONE_ITEM[b.id] || "pocao", 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
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

  // ------------------------------------------------------------------ grimório
  const COR_ELEMENTO = { "físico": "#e8dcc0", fogo: "#ff9a4a", gelo: "#8fc4ff", sagrado: "#f2c94c", sombra: "#b08ae0", arcano: "#c8b0ff", veneno: "#8fbf6a" };
  let paginaGrimorio = "ataque";
  /** O livro de habilidades: índice à esquerda; à direita, a habilidade aberta com o dano de agora, de onde ele vem
   *  e como cresce. Os números chegam prontos do motor (grimorio.py), no estado do herói. */
  function abrirGrimorio(id) {
    const g = App.estado && App.estado.heroi && App.estado.heroi.grimorio;
    if (!g) return;
    if (id) paginaGrimorio = id;
    const todas = [g.basico, ...g.habilidades];
    if (!todas.some((x) => x.id === paginaGrimorio)) paginaGrimorio = "ataque";
    const heroi = App.estado.heroi;
    const icone = (x) => x.id === "ataque" ? ({ guerreiro: "espada", arqueiro: "arco", mago: "cajado" }[heroi.classe] || "espada") : (HAB_ICONE[x.id] || ["estrela"])[0];
    const custo = (x) => x.custo ? `${x.custo} ${h(g.recurso.toLowerCase())}` : "grátis";
    document.getElementById("grimorio-indice").innerHTML = `
      <div class="grimorio-cab"><b>Grimório</b><small>${h(heroi.titulo)} · nível ${heroi.nivel}</small></div>
      <ul class="grimorio-lista">${todas.map((x) => `<li><button type="button" class="grimorio-item${x.id === paginaGrimorio ? " aberto" : ""}" data-pagina="${h(x.id)}">
        <span class="gi-icone">${S(icone(x), 2)}</span><span class="gi-nome">${h(x.nome)}</span><span class="gi-custo">${custo(x)}</span></button></li>`).join("")}</ul>
      <div class="grimorio-atributos">${Object.entries(g.atributos).map(([k, v]) => `<span><small>${h(k)}</small><b>${v}</b></span>`).join("")}</div>
      <ul class="grimorio-gerais">${g.gerais.map((l) => `<li>${Realce.texto(l)}</li>`).join("")}</ul>`;
    const x = todas.find((t) => t.id === paginaGrimorio);
    const linhas = x.linhas.map((l) => l.tipo === "efeito" ? `<li class="g-efeito">${Realce.texto(l.texto)}</li>` : `
      <li class="g-dano"><div class="g-rotulo">${h(l.rotulo)} <i style="color:${COR_ELEMENTO[l.elemento] || "#e8dcc0"}">${h(l.elemento)}</i></div>
        <div class="g-faixa"><b>${l.min}–${l.max}</b><span class="rx rx-crit">crítico <b>${l.critico}</b> · ${l.chance_critico}% de chance</span></div>
        <div class="g-formula">${h(l.formula)}</div>
        <div class="g-escala">${l.escala.map((e) => `<span>▲ ${h(e)}</span>`).join("")}</div>
        ${l.nota ? `<div class="g-nota">${h(l.nota)}</div>` : ""}</li>`).join("");
    const det = document.getElementById("grimorio-detalhe");
    det.innerHTML = `<div class="g-topo"><span class="g-icone">${S(icone(x), 4)}</span>
        <div><b class="g-nome">${h(x.nome)}</b><div class="g-meta">${custo(x)}${x.flechas_por_alvo ? ` · ${x.flechas_por_alvo} flecha por inimigo` : x.flechas ? ` · ${x.flechas} flecha${x.flechas > 1 ? "s" : ""}` : ""} · Alvo: ${h(x.alvo)}</div></div></div>
      <p class="g-desc">${Realce.texto(x.desc)}</p><ul class="g-linhas">${linhas}</ul>
      <p class="g-rodape">Números antes da defesa do inimigo e de efeitos do momento (fortalecido, clima, alvo marcado).</p>`;
    det.classList.remove("virando"); void det.offsetWidth; det.classList.add("virando");
    const caixa = document.getElementById("sobre-grimorio");
    if (caixa.hidden) { caixa.hidden = false; App.som("pagina"); }
    caixa.querySelectorAll("[data-pagina]").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      if (b.dataset.pagina !== paginaGrimorio) { App.som("pagina"); abrirGrimorio(b.dataset.pagina); }
    }));
  }
  function alternarGrimorio() {
    const caixa = document.getElementById("sobre-grimorio");
    if (caixa.hidden) abrirGrimorio(); else caixa.hidden = true;
  }

  // ------------------------------------------------------------------ carregar jogo
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

  // ------------------------------------------------------------------ saque
  const BRILHO_RARIDADE = { comum: ["#f1e4c4", "#c0b8a8"], magico: ["#7fb0ff", "#c8e0ff", "#ffffff"],
    raro: ["#f2c94c", "#fff3a0", "#ffffff"], lendario: ["#ffb35c", "#e0782f", "#fff3a0", "#ffffff"] };
  /** Item encontrado: o cartão dele (sprite, raridade, bônus, diferença para o seu) e, ao lado, o que você usa. */
  function achado(d) {
    const it = d.item;
    const rar = h(it.raridade);
    const eq = (d.equipados || []).map((e) => `<div class="achado-cartao atual rar-${h(e.raridade)}">
        <span class="achado-selo">Você usa</span>
        <div class="achado-arte pequena">${S(iconeItem(e), 3)}</div>${htmlItem(e, "", false)}</div>`).join("");
    const aviso = !d.pode_usar ? "" : !d.cabe ? '<div class="pior">Mochila cheia: equipar deixa o item antigo para trás.</div>' : "";
    return `<div class="tela achado rar-${rar}">
      <div class="achado-cartao novo rar-${rar}">
        <div class="achado-raios" aria-hidden="true"></div>
        <span class="achado-selo">Você encontrou</span>
        <div class="achado-arte">${S(iconeItem(it), 4)}</div>
        ${htmlItem(it, "", true)}${aviso}
      </div>${eq}</div>`;
  }
  /** O item achado abre numa janela própria, por cima do jogo e fora do log: o cartão dele, o que você usa ao lado e,
   *  logo abaixo, o que fazer (os botões vêm da pergunta do motor, ver escolhas.js). Raro e lendário: o feixe de luz
   *  cai antes no lugar do cartão. A janela fecha quando o ícone pousa (no corpo ou na mochila), ou ao deixar o item. */
  async function abrirAchado(d, semCerimonia = false) {
    fecharAchado();
    const fundo = document.createElement("div");
    fundo.id = "sobre-achado";
    fundo.className = "sobreposicao";
    fundo.innerHTML = `<div class="janela-achado">${achado(d)}<div class="achado-acoes"></div></div>`;
    document.body.appendChild(fundo);
    const janela = fundo.firstElementChild, tela = janela.querySelector(".tela.achado");
    noPalco(janela);
    if (semCerimonia) return;
    tela.classList.add("esperando-feixe");
    await Sensacao.cerimoniaSaque(d.item.raridade, tela.querySelector(".achado-cartao.novo"));
    tela.classList.remove("esperando-feixe");
    revelarAchado(tela, d);
  }
  /** Onde a pergunta "o que fazer com o item?" põe os botões (null se a janela não está aberta). */
  function acoesDoAchado() { return document.querySelector("#sobre-achado .achado-acoes"); }
  function fecharAchado() {
    const f = document.getElementById("sobre-achado");
    if (!f) return;
    f.id = "";  // a próxima janela (outro item logo em seguida) já pode abrir enquanto esta some
    f.classList.add("saindo");
    setTimeout(() => f.remove(), 220);
  }

  /** O cartão do item aparece de vez: o som da raridade e as faíscas (depois da cerimônia, se houve uma). */
  function revelarAchado(raiz, d) {
    const cartao = raiz.querySelector(".achado-cartao.novo");
    if (!cartao) return;
    const raro = ["raro", "lendario"].includes(d.item.raridade);
    App.som(raro ? "achado_raro" : "achado");
    setTimeout(() => { if (cartao.isConnected) faiscas(cartao.querySelector(".achado-arte"), BRILHO_RARIDADE[d.item.raridade] || BRILHO_RARIDADE.comum, raro ? 22 : 12); }, 260);
  }

  // ------------------------------------------------------------------ mercado
  const qtdLoja = {};  // quantidade escolhida em cada suprimento (sobrevive ao redesenho, não à saída do mercado)
  function novaVisita() { for (const k in qtdLoja) delete qtdLoja[k]; contratosVistos = null; }
  function maxCompra(c, ouro) { return Math.max(0, Math.min(99, c.limite ?? 99, Math.floor(ouro / c.preco))); }
  function loja(d) {
    // Na vitrine, o número no canto do ícone é o que o mercador tem (como nos jogos do gênero); o que você carrega
    // está na bolsa e no topo.
    const cons = d.consumiveis.map((c) => {
      const max = maxCompra(c, d.ouro);
      const q = Math.max(1, Math.min(qtdLoja[c.id] || 1, max || 1));
      const caro = max < 1;
      const icone = c.id === "provisoes" ? "pernil" : c.id === "flechas" ? "aljava" : (ICONE_ITEM[c.id] || "pocao");
      return `<div role="button" tabindex="0" class="mercadoria suprimento${caro ? " caro" : ""}" data-comprar="${h(c.id)}" data-preco="${c.preco}" data-max="${max}" ${dica(`<b>${h(c.nome)}</b><div>${Realce.texto(c.desc)}</div><div class="rodape">${caro ? (c.estoque === 0 ? "Esgotado: o mercador reabastece amanhã cedo." : c.limite === 0 ? "Você não carrega mais." : "Ouro insuficiente.") : "Escolha a quantidade e clique para comprar. Shift+clique compra 5."}</div>`)}>
        <span class="slot-px">${S(icone, 2)}${c.estoque ? `<span class="qtd">${c.estoque}</span>` : ""}</span>
        <span class="merc-nome">${h(c.nome)}${c.estoque === 0 ? '<small class="merc-estoque esgotado">esgotado</small>' : ""}</span>
        <span class="preco">${S("moeda", 1)}<span class="total">${c.preco * q}</span></span>
        <span class="qtd-ctrl"><button type="button" data-q="-1" aria-label="menos">−</button><b>${q}</b><button type="button" data-q="1" aria-label="mais">+</button></span></div>`;
    }).join("");
    const equips = d.equipamentos.map((it, i) => {
      const caro = it.preco > d.ouro;
      return `<button type="button" class="mercadoria equip${caro ? " caro" : ""}" data-comprar-item="${i}" ${dicaItem(it, caro ? "Ouro insuficiente." : "Clique para comprar. Se o espaço do corpo estiver vazio, você já sai vestindo.")}>
        <span class="slot-px r-${h(it.raridade)}">${S(iconeItem(it), 2)}</span>
        <span class="merc-nome r-${h(it.raridade)}">${h(it.nome)}</span><span class="merc-bonus">${h(it.bonus)}</span><span class="preco">${S("moeda", 1)}${it.preco}</span></button>`;
    }).join("");
    const mochila = d.mochila.map((it, i) => `<div role="button" tabindex="0" class="slot-px celula r-${h(it.raridade)}${it.usavel ? "" : " inutil"}" draggable="true" data-mochila-loja="${i}" ${dicaItem(it, "Clique para equipar ou vender · botão direito: vender na hora.")}>${S(iconeItem(it), 2)}</div>`);
    for (let i = d.mochila.length; i < d.limite; i++) mochila.push('<div class="slot-px celula vazia"></div>');
    return `<div class="tela loja">
      <div class="loja-topo">${S("saco", 3)}<div><b>O mercador</b><span class="lore">"Tudo tem preço. Até você."</span></div>
        <span class="ouro-loja">${S("moedas", 2)}${d.ouro}</span></div>
      <div class="balcao">
        <h4>Suprimentos</h4><div class="vitrine">${cons}</div>
        <h4>Equipamentos</h4><div class="vitrine">${equips || '<span class="vazio">Nada que preste hoje. Volte em alguns dias.</span>'}</div>
      </div>
      <h4>Sua mochila <small>${d.ocupado}/${d.limite} · clique num item para equipar ou vender; botão direito vende na hora (o mercador paga metade)</small></h4>
      <div class="mochila-grade mochila-loja">${mochila.join("")}</div></div>`;
  }

  /** Poção ou bandagem com a comitiva por perto: em quem usar? (só fora de combate) */
  function menuUso(ancora, b) {
    fecharMenuItem();
    esconderDica();
    const heroi = App.estado.heroi;
    const linha = (rotulo, vida, motivo, attr) => `<button type="button" ${attr}${motivo ? ` disabled title="${h(motivo)}"` : ""}>${rotulo}<small>${vida}</small></button>`;
    const m = document.createElement("div");
    m.className = "menu-item moldura menu-uso";
    m.innerHTML = `<b>${h(b.nome)}</b>
      ${linha("Em você", `${heroi.hp}/${heroi.max_hp}`, b.motivo, 'data-em=""')}
      ${b.alvos.map((a) => linha(`Em ${h(a.nome)}`, a.ferido ? h(a.caido) : `${a.hp}/${a.max_hp}`, a.motivo, `data-em="${h(a.id)}"`)).join("")}
      <button type="button" data-em="-" class="secundaria">Cancelar</button>`;
    document.body.appendChild(m);
    const r = ancora.getBoundingClientRect();
    m.style.left = Math.max(8, Math.min(innerWidth - m.offsetWidth - 8, r.left)) + "px";
    m.style.top = (r.bottom + 6 + m.offsetHeight > innerHeight ? r.top - m.offsetHeight - 6 : r.bottom + 6) + "px";
    m.addEventListener("click", (ev) => {
      const bt = ev.target.closest("button");
      if (!bt || bt.disabled) return;
      ev.stopPropagation();
      fecharMenuItem();
      if (bt.dataset.em === "-") return;
      App.acao(bt.dataset.em ? { usar: b.id, em: bt.dataset.em } : { usar: b.id }, "item");
    });
    fecharAoClicarFora();
  }

  /* Os menus de item fecham com um clique fora deles. Um só "vigia" por vez: antes, cada abertura deixava um
     ouvinte pendurado e o clique seguinte fechava o menu recém-aberto (a bolsa "às vezes não abria"). */
  let vigiaFora = null;
  function fecharAoClicarFora() {
    setTimeout(() => {
      if (vigiaFora || !document.querySelector(".menu-item")) return;
      vigiaFora = (ev) => { if (!ev.target.closest(".menu-item")) fecharMenuItem(); };
      document.addEventListener("pointerdown", vigiaFora, true);
    }, 0);
  }
  function fecharMenuItem() {
    document.querySelectorAll(".menu-item").forEach((m) => m.remove());
    if (vigiaFora) { document.removeEventListener("pointerdown", vigiaFora, true); vigiaFora = null; }
  }
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
      else if (b.dataset.a === "vender") App.acao({ vender: i });  // o tilintar vem do ouro recebido: um som só
    });
    fecharAoClicarFora();
  }

  let repeticao = null;  // o "segurar +/−" do mercado em andamento
  function pararRepeticao() { clearTimeout(repeticao); repeticao = null; }
  ["pointerup", "pointercancel", "blur"].forEach((t) => window.addEventListener(t, pararRepeticao));
  function ligarLoja(raiz) {
    pararRepeticao();
    const dados = App.ultimaLoja;
    raiz.querySelectorAll("[data-comprar]").forEach((el) => {
      const preco = Number(el.dataset.preco), max = Number(el.dataset.max), id = el.dataset.comprar;
      const num = el.querySelector(".qtd-ctrl b"), total = el.querySelector(".total");
      const mudar = (q) => {
        q = Math.max(1, Math.min(max || 1, q));
        qtdLoja[id] = q; num.textContent = q; total.textContent = preco * q;
      };
      el.querySelectorAll("[data-q]").forEach((b) => {
        const passo = () => mudar(Math.min(qtdLoja[id] || 1, max || 1) + Number(b.dataset.q));
        b.addEventListener("click", (ev) => { ev.stopPropagation(); });
        b.addEventListener("pointerdown", (ev) => {
          ev.stopPropagation(); pararRepeticao(); passo(); App.som("escolha");
          // Segurar acelera. A repetição para ao soltar em qualquer lugar, ao sair da janela, ao chegar no
          // limite e se o botão sumir (a tela se redesenhou): nunca fica rodando sozinha.
          repeticao = setTimeout(function repetir() {
            const antes = qtdLoja[id];
            if (!b.isConnected) { pararRepeticao(); return; }
            passo();
            repeticao = qtdLoja[id] === antes ? null : setTimeout(repetir, 70);
          }, 380);
        });
        ["pointerup", "pointerleave", "pointercancel"].forEach((t) => b.addEventListener(t, pararRepeticao));
      });
      // A roda do mouse só mexe na quantidade em cima do controle (rolar a página não pode mudar a compra).
      const ctrl = el.querySelector(".qtd-ctrl");
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
      // Botão direito vende na hora, sem abrir o menu (o tilintar vem do ouro recebido: um som só).
      el.addEventListener("contextmenu", (ev) => { ev.preventDefault(); fecharMenuItem(); esconderDica(); if (it) App.acao({ vender: i }); });
      el.addEventListener("dragstart", (ev) => { esconderDica(); fecharMenuItem(); vendendo = i; ev.dataTransfer.setData("text/plain", "item"); balcao.classList.add("alvo"); });
      el.addEventListener("dragend", () => { balcao.classList.remove("alvo"); setTimeout(() => { vendendo = null; }, 0); });
    });
    balcao.addEventListener("dragover", (ev) => { if (vendendo !== null) ev.preventDefault(); });
    balcao.addEventListener("drop", (ev) => {
      ev.preventDefault(); balcao.classList.remove("alvo");
      if (vendendo !== null) App.acao({ vender: vendendo });  // um som só: o do ouro recebido
      vendendo = null;
    });
  }

  function diario(d) {
    const contratos = d.contratos.map((c) => cartaz(c, true, false, d.nivel_heroi)).join("");
    const rumores = d.rumores.map((r) => `<div class="bilhete"><span class="prego"></span>${S("olho", 1)} ${h(r.texto)}<small>${r.expira > 0 ? `some em ${r.expira} dia${r.expira === 1 ? "" : "s"}` : "some hoje"}</small></div>`).join("");
    const losangos = [0, 1, 2].map((i) => `<i class="sigilo${i < d.sigilos ? " tem" : ""}"></i>`).join("");
    return `<div class="tela diario">
      <div class="faixa-jornada"><span>Dia ${d.dia}</span><span class="sigilos-diario" title="Sigilos dos guardiões">${losangos} ${d.sigilos}/3</span></div>
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
      ${aprovacao(m)}${m.conversa && !reserva ? '<button type="button" class="tag aviso-conversa">✉ quer conversar · clique aqui</button>' : ""}</div>`;
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
    if (ativo && c.tipo === "caca" && c.progresso && !c.recebendo) {
      const [feito, total] = c.progresso.split("/").map(Number);
      progresso = `<div class="contrato-progresso">${barra("xp", feito, total)}<span>${feito}/${total}</span></div>`;
    }
    let botao;
    if (c.recebendo) botao = '<span class="carimbo">Cumprido</span>';  // no quadro de pagamento: o carimbo bate
    else if (ativo) botao = c.concluido ? '<span class="contrato-feito">Feito! Volte a uma vila para receber</span>'
      : `<button type="button" class="contrato-botao abandonar" data-abandonar="${c.id}" title="Reputação −${c.penalidade}">Abandonar</button>`;
    else botao = `<button type="button" class="contrato-botao" data-aceitar="${c.id}"${cheio ? " disabled title=\"Você já tem 3 contratos\"" : ""}>Aceitar</button>`;
    const recem = ativo && contratosVistos && !contratosVistos.has(c.id);
    return `<div class="contrato tipo-${h(c.tipo)}${ativo ? " ativo" : ""}${c.concluido && !c.recebendo ? " concluido" : ""}${recem ? " recem" : ""}">
      <span class="prego"></span><div class="contrato-tipo">${TIPO_CONTRATO[c.tipo] || h(c.tipo)}</div>
      <div class="contrato-arte">${S(arte, 3)}</div>
      <div class="contrato-titulo">${h(titulo)}</div>
      <div class="contrato-desc">${h(c.desc)}</div>
      <div class="contrato-lugar">${lugar}</div>${progresso}
      <div class="contrato-premio"><span>${S("moeda", 1)} ${c.ouro}</span><span>${S("estrela", 1)} ${c.xp} XP</span></div>
      ${botao}</div>`;
  }
  let contratosVistos = null;  // os contratos que você já tinha: o recém-aceito chega pregado com destaque
  function mural(d) {
    const cheio = d.ativos.length >= d.limite;
    const oferta = d.oferta.map((c) => cartaz(c, false, cheio, d.nivel_heroi)).join("");
    const ativos = d.ativos.map((c) => cartaz(c, true, cheio, d.nivel_heroi)).join("");
    contratosVistos = new Set(d.ativos.map((c) => c.id));
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
  const PONTO_FERA = [108, 104];  // o animal do patrulheiro, deitado ao lado do herói
  const BARRACA = [262, 76];       // o alto da barraca, onde fica o "Dormir"
  function acampamento(d) {
    const figuras = [];
    d.ativos.forEach((m, i) => figuras.push({ ...m, onde: "ativo", p: PONTOS_ATIVOS[i % 2] }));
    d.reserva.forEach((m, i) => figuras.push({ ...m, onde: "reserva", p: PONTOS_RESERVA[i % 3] }));
    const botoes = figuras.map((f) => `<button type="button" class="figura ${f.onde}${f.conversa ? " tem-conversa" : ""}" data-cid="${h(f.id)}"
        style="left:${(f.p[0] / 320) * 100}%;top:${((f.p[1] + 8) / 120) * 100}%">
        ${f.conversa ? '<i class="carta-aviso">✉</i>' : ""}<span class="figura-nome">${h(f.nome.split(" ").pop())}</span>
        <span class="figura-estado">${f.onde === "ativo" ? "vai com você" : "no acampamento"}</span></button>`).join("");
    const fera = d.fera ? `<span class="figura fera" role="button" tabindex="0" data-fera="1" style="left:${(PONTO_FERA[0] / 320) * 100}%;top:${((PONTO_FERA[1] + 8) / 120) * 100}%"
        ${dica(`<b>${h(d.fera.nome)}</b><div>Seu ${h({ lobo: "lobo", urso: "urso", falcao: "falcão" }[d.fera.tipo] || "animal")} dorme perto do fogo. Vida ${d.fera.hp}/${d.fera.max_hp}.</div>`, true)}>
        <span class="figura-nome">${h(d.fera.nome.split(" ").pop())}</span></span>` : "";
    // Dormir: um selo sobre a barraca, que balança de leve (o fim da noite fica onde a gente dorme, não numa lista).
    const dormir = `<button type="button" class="dormir-barraca" style="left:${(BARRACA[0] / 320) * 100}%;top:${(BARRACA[1] / 120) * 100}%">${S("lua", 1)} Dormir até o amanhecer</button>`;
    return `<div class="tela acampamento">${d.intro ? `<p class="sussurro">${h(d.intro)}</p>` : ""}<div class="fogueira-palco"><canvas class="fogueira-cena" width="320" height="120"></canvas>${botoes}${fera}${dormir}</div>
      <div class="dica-uso">${figuras.length ? `Clique em alguém para conversar ou decidir quem vai com você amanhã. Quem fica no acampamento descansa, não come das suas provisões e não opina nas suas escolhas. ${d.ativos.length}/${d.limite} na comitiva.` : "Só você, o fogo e os barulhos da mata. Quem você encontrar pelo caminho pode se sentar aqui um dia."}</div></div>`;
  }

  function desenharFogueira(canvas, d) {
    const x = canvas.getContext("2d");
    const W = 320, H = 120;
    const px = (cx, cy, w, hh, cor) => { x.fillStyle = cor; x.fillRect(cx | 0, cy | 0, w, hh); };
    const heroi = App.estado && App.estado.heroi;
    const quem = [[heroi ? heroi.classe : "guerreiro", 128, 93]];
    d.ativos.forEach((m, i) => quem.push([m.id, ...PONTOS_ATIVOS[i % 2]]));
    d.reserva.forEach((m, i) => quem.push([m.id, ...PONTOS_RESERVA[i % 3]]));
    if (d.fera) quem.push([d.fera.tipo === "falcao" ? "voador" : "fera", ...PONTO_FERA]);
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

  /** O animal do patrulheiro na fogueira: carinho, poção, bandagem (o que estiver disponível agora). */
  function menuFera(ancora) {
    fecharMenuItem();
    const ops = App.opcoes() || [];
    const f = App.estado && App.estado.heroi.companheiro;
    if (!f) return;
    const itens = [];
    ops.forEach((o) => {
      const m = o.meta || {};
      if (m.carinho === "fera") itens.push([`${S("coracao", 1)} Fazer carinho`, { carinho: "fera" }]);
      if (m.em === "fera" && m.usar) itens.push([`${S(ICONE_ITEM[m.usar] || "pocao", 1)} ${m.usar === "bandagem" ? "Enfaixar" : "Dar a Poção de Vida"}`, { usar: m.usar, em: "fera" }]);
    });
    if (!itens.length) return;
    const menu = document.createElement("div");
    menu.className = "menu-item moldura";
    menu.innerHTML = `<b>${h(f.nome)}</b><small class="menu-sub">vida ${Math.max(0, f.hp)}/${f.max_hp}</small>` + itens.map(([t], i) => `<button type="button" data-i="${i}">${t}</button>`).join("") +
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
      if (i >= 0) App.acao(itens[i][1], itens[i][1].carinho ? "escolha" : "item");
    });
    fecharAoClicarFora();
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
    fecharAoClicarFora();
  }

  function ligarFigurasComitiva(raiz) {
    raiz.querySelectorAll(".dormir-barraca").forEach((b) => b.addEventListener("click", (ev) => {
      ev.stopPropagation(); fecharMenuItem(); App.acao({ dormir: true }, "escolha");
    }));
    raiz.querySelectorAll(".figura.fera").forEach((el) => {
      el.addEventListener("click", (ev) => { ev.stopPropagation(); menuFera(el); });
      el.addEventListener("keydown", (ev) => { if (ev.key === "Enter") menuFera(el); });
    });
    raiz.querySelectorAll("[data-cid].figura, .cartao[data-cid]").forEach((el) => {
      el.addEventListener("click", (ev) => {
        ev.stopPropagation();
        // Clicou no aviso de conversa (✉ do retrato ou "quer conversar"): abre a conversa direto, sem menu.
        if (ev.target.closest(".aviso-conversa, .carta-aviso") && App.acao({ conversar: el.dataset.cid }, "escolha")) return;
        menuFigura(el, el.dataset.cid);
      });
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
    div.innerHTML = ({ personagem, diario, bestiario, comitiva, loja, acampamento, mural, achado, saves }[m.tipo] || (() => ""))(m.dados);
    if (m.tipo === "saves") ligarSaves(div);
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

  /** Um atributo para sempre (+2 Ataque de um evento): um selo surge no meio da tela, voa até o atributo (no painel;
   *  vida e recurso máximos, na barra da HUD), que brilha e conta até o valor novo. Não segura o jogo: o texto segue
   *  enquanto o selo voa. */
  const ICONE_SELO = { atk: "espada", defesa: "escudo", agi: "folha", poder: "chama", max_hp: "coracao", max_rec: "estrela" };
  function destinoAtributo(d) {
    if (d.stat === "max_hp" || d.stat === "max_rec") return document.querySelector(`#hud .vital[data-vital="${d.stat === "max_hp" ? "hp" : "rec"}"]`);
    return document.querySelector(`#heroi .atributo[data-atributo="${d.nome}"]`);
  }
  function seloAtributo(d) {
    const selo = document.createElement("div");
    selo.className = "selo-atributo";
    selo.innerHTML = `${S(ICONE_SELO[d.stat] || "estrela", 4)}<b>+${d.valor}</b><span>${h(d.nome)}<small>permanente</small></span>`;
    document.body.appendChild(selo);
    selo.style.left = (innerWidth - selo.offsetWidth) / 2 + "px";  // centrado sem transform: o voo usa translate e scale
    App.som("aprender");
    const antes = d.total - d.valor, noPainel = !["max_hp", "max_rec"].includes(d.stat);
    if (noPainel) {  // o painel espera o selo chegar para mostrar o valor novo
      chegando.set(d.nome, antes);
      const v = destinoAtributo(d)?.querySelector(".valor");
      if (v) v.textContent = antes;
    }
    const voar = async () => {
      await new Promise((r) => setTimeout(r, 900));  // o selo fica um instante no meio, para ser lido
      const alvo = destinoAtributo(d), visivel = alvo && alvo.offsetParent;
      if (visivel) {
        const a = selo.getBoundingClientRect(), b = alvo.getBoundingClientRect();
        const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
        await selo.animate([{ translate: "0 0", scale: 1, opacity: 1 }, { translate: `${dx}px ${dy}px`, scale: 0.25, opacity: 0.6 }],
          { duration: 520, easing: "cubic-bezier(.5,0,.75,0)", fill: "forwards" }).finished.catch(() => {});
      } else await selo.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: "forwards" }).finished.catch(() => {});
      selo.remove();
      if (noPainel) chegando.delete(d.nome);
      const aqui = destinoAtributo(d);  // o painel pode ter sido redesenhado enquanto o selo voava
      if (!aqui) return;
      aqui.classList.remove("ganhou"); void aqui.offsetWidth; aqui.classList.add("ganhou");
      setTimeout(() => aqui.classList.remove("ganhou"), 1100);
      const valor = aqui.querySelector(".valor");
      if (valor && noPainel) Sensacao.contar(valor, d.total, 520, { de: antes });
    };
    voar();
    return new Promise((r) => setTimeout(r, 450));
  }

  /** Chegar a um lugar: o nome surge no meio da tela entre dois fios dourados, como o título de área dos jogos
   *  (Elden Ring, Diablo). Na primeira vez, "lugar descoberto", som e um pouco mais de tempo; na volta, curto. O nível
   *  da região vem na cor do perigo (o aviso por extenso fica no texto). Some sozinho; um clique ou uma tecla adianta. */
  function chegada(d) {
    const el = document.createElement("div");
    el.className = "chegada" + (d.primeira ? " primeira" : "");
    const tag = d.nivel ? `<span class="perigo-tag ${nivelPerigo(d.nivel)}">${d.tipo === "vila" ? "arredores" : "inimigos"} Nv.${d.nivel}</span>` : "";
    el.innerHTML = `${d.primeira ? '<div class="rotulo-festa">lugar descoberto</div>' : ""}<i class="linha-ouro"></i>
      <div class="nome-lugar">${h(d.nome)}</div><i class="linha-ouro"></i>
      <div class="sub-lugar">${h(d.sub)}${tag}</div>`;
    document.body.appendChild(el);
    if (d.primeira) App.som("achado");
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        el.classList.add("saindo");
        setTimeout(() => { el.remove(); resolver(); }, 420);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 300);
      setTimeout(fechar, d.primeira ? 2400 : 1300);
    });
  }

  function faixa(titulo, sub, icone) {
    const f = document.createElement("div");
    f.className = "faixa-festa";
    f.innerHTML = `<b>${icone ? S(icone, 3) : ""}${h(titulo)}${icone ? S(icone, 3) : ""}</b>${sub ? `<span>${h(sub)}</span>` : ""}`;
    document.body.appendChild(f);
    setTimeout(() => f.remove(), 1700);
  }

  /** Mostra a celebração. Devolve uma Promise que resolve quando o jogador fecha (ou na hora, se rápida). */
  /** Os ganhos do nível contam de 0 até o valor, cada um com um tique. */
  function contarGanhos(caixa) {
    caixa.querySelectorAll(".conta").forEach((b) => {
      const alvo = Number(b.dataset.alvo), atraso = Number(b.dataset.atraso);
      setTimeout(() => {
        App.som("tique");
        const inicio = performance.now(), dur = 320;
        const passo = (agora) => {
          const t = Math.min(1, (agora - inicio) / dur);
          b.textContent = "+" + Math.round(alvo * (1 - Math.pow(1 - t, 3)));
          if (t < 1) requestAnimationFrame(passo);
        };
        requestAnimationFrame(passo);
      }, atraso);
    });
  }

  /** O ícone de um item voando de um ponto da tela até um elemento (o espaço do corpo, a mochila), num arco. */
  function voarIcone(item, origem, alvo) {
    const r = alvo.getBoundingClientRect();
    const voo = document.createElement("div");
    voo.className = "voo-item";
    voo.innerHTML = S(iconeItem(item), 3);
    document.body.appendChild(voo);
    const dx = r.left + r.width / 2 - origem.x, dy = r.top + r.height / 2 - origem.y;
    voo.style.left = origem.x - 24 + "px"; voo.style.top = origem.y - 24 + "px";
    return voo.animate([{ transform: "translate(0, 0) scale(1.2)", opacity: 1 },
      { transform: `translate(${dx * 0.5}px, ${dy * 0.5 - 60}px) scale(1)`, opacity: 1 },
      { transform: `translate(${dx}px, ${dy}px) scale(.45)`, opacity: 0.9 }],
      { duration: 560, easing: "cubic-bezier(.4,0,.2,1)" }).finished.catch(() => {}).then(() => voo.remove());
  }
  /** O cartão do item achado (na janela) recebe o selo do destino; devolve de onde o ícone sai. */
  function seloDoAchado(texto, classe, velhoTexto) {
    const tela = document.querySelector("#sobre-achado .tela.achado");
    if (!tela) return null;
    const novo = tela.querySelector(".achado-cartao.novo"), velho = tela.querySelector(".achado-cartao.atual");
    if (novo) { novo.classList.add(classe); const selo = novo.querySelector(".achado-selo"); if (selo) selo.textContent = texto; }
    if (velho && velhoTexto) { velho.classList.add("guardado"); const selo = velho.querySelector(".achado-selo"); if (selo) selo.textContent = velhoTexto; }
    const a = novo && novo.querySelector(".achado-arte").getBoundingClientRect();
    return a && a.width ? { x: a.left + a.width / 2, y: a.top + a.height / 2 } : null;
  }
  /** Vestiu (comprou no mercado ou achou): o ícone voa até o espaço do corpo no painel, que brilha ao receber. Achado:
   *  o cartão vira "Vestido", o antigo "Foi para a mochila", o ícone sai do próprio cartão e a janela fecha. */
  async function voarParaEspaco(d) {
    const alvo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
    let origem = App.ultimoClique && performance.now() - App.ultimoClique.t < 4000 ? App.ultimoClique : { x: innerWidth / 2, y: innerHeight / 2 };
    if (d.achado) origem = seloDoAchado("Vestido", "vestido", "Foi para a mochila") || origem;
    if (alvo) {
      App.som("equipar");
      await voarIcone(d.item, origem, alvo);
      const novo = document.querySelector(`#heroi [data-mini="${d.espaco}"]`);
      if (novo) { novo.classList.remove("recebeu"); void novo.offsetWidth; novo.classList.add("recebeu"); setTimeout(() => novo.classList.remove("recebeu"), 900); }
    }
    if (d.achado) fecharAchado();
  }
  /** Guardou o item achado: o cartão vira "Na mochila", o ícone voa até o Inventário e a janela fecha. */
  async function voarParaMochila(d) {
    const origem = seloDoAchado("Na mochila", "na-mochila");
    const alvo = document.querySelector('.atalho[data-rotulo="Inventário"]');
    App.som("item");
    if (origem && alvo && alvo.offsetParent) {
      await voarIcone(d.item, origem, alvo);
      alvo.classList.remove("recebeu"); void alvo.offsetWidth; alvo.classList.add("recebeu");
      setTimeout(() => alvo.classList.remove("recebeu"), 900);
    } else await new Promise((r) => setTimeout(r, 500));
    fecharAchado();
  }

  /** O balão da reação do animal: acima dele, no palco da fogueira. Some sozinho ou com qualquer clique. */
  function balaoFera(alvo, d) {
    document.querySelectorAll(".balao.da-fera").forEach((b) => b.remove());
    const b = document.createElement("div");
    b.className = "balao narrado da-fera";
    b.innerHTML = `<i>${h(d.texto)}</i>${d.efeito ? `<small class="balao-efeito">${h(d.efeito)}</small>` : ""}`;
    document.body.appendChild(b);
    const r = alvo.getBoundingClientRect();
    // Sobre o animal, alinhado pela esquerda (o rabicho aponta para ele): o meio do palco e a barraca ficam livres.
    b.style.left = Math.max(8, r.left + r.width / 2 - 22) + "px";
    b.style.top = Math.max(8, r.top + r.height * 0.35 - b.offsetHeight - 10) + "px";
    const nasceu = performance.now();
    const sair = () => { b.classList.add("sumindo"); setTimeout(() => b.remove(), 300); document.removeEventListener("pointerdown", aoClicar, true); };
    const aoClicar = () => { if (performance.now() - nasceu > 300) sair(); };
    document.addEventListener("pointerdown", aoClicar, true);
    setTimeout(sair, Math.min(9000, 3000 + d.texto.length * 45));
  }

  function celebrar(m, instantaneo) {
    const d = m.dados;
    if (m.tipo === "equipou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaEspaco(d);
    if (m.tipo === "guardou") return instantaneo ? (fecharAchado(), Promise.resolve()) : voarParaMochila(d);
    if (m.tipo === "carinho") {
      // corações subindo do animal na fogueira, e a reação num balão sobre ele (não tampa nada; um clique dispensa)
      if (instantaneo) return Promise.resolve();
      const alvos = document.querySelectorAll("#texto .figura.fera");
      const alvo = alvos[alvos.length - 1];
      if (alvo && d.texto) balaoFera(alvo, d);
      if (d.repetido) return Promise.resolve();
      App.som("cura");
      if (alvo) for (let i = 0; i < 6; i++) {
        const c = document.createElement("span");
        c.className = "coracao-carinho";
        c.textContent = "♥";
        c.style.left = 20 + Math.random() * 60 + "%";
        c.style.animationDelay = i * 110 + "ms";
        alvo.appendChild(c);
        setTimeout(() => c.remove(), 1600);
      }
      return new Promise((r) => setTimeout(r, 700));
    }
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
    if (m.tipo === "contratos") return instantaneo ? Promise.resolve() : pagarContratos(caixa, d);
    if (m.tipo === "amanhecer") return instantaneo ? Promise.resolve() : amanhecer(caixa, d);
    if (m.tipo === "espolio") return instantaneo ? Promise.resolve() : Sensacao.espolio(caixa, d);
    if (m.tipo === "atributo") return instantaneo ? Promise.resolve() : seloAtributo(d);
    if (m.tipo === "chegada") return instantaneo ? Promise.resolve() : chegada(d);
    let html = "";
    if (m.tipo === "nivel") {
      const icones = { Vida: "coracao", Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama", Mana: "pocao_azul", Vigor: "chama", Foco: "olho" };
      const ganhos = Object.entries(d.ganhos).map(([k, v], i) => `<span class="ganho" style="animation-delay:${0.75 + i * 0.12}s">${S(icones[k] || "estrela", 1)}<b class="conta" data-alvo="${v}" data-atraso="${750 + i * 120}">+0</b>${h(k)}</span>`).join("");
      const atraso = 0.75 + Object.keys(d.ganhos).length * 0.12;
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${atraso + 0.35 + i * 0.2}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
      html = `<div class="festa festa-nivel moldura"><div class="raios"></div><div class="anel"></div>
        <div class="rotulo-festa">você subiu de nível</div>
        <div class="nivel-bloco"><span class="nivel-palavra">Nível</span><span class="nivel-numero">${d.nivel}</span></div>
        <div class="lista">${ganhos}<span class="ganho ouro" style="animation-delay:${atraso + 0.08}s">${S("estrela", 1)}+1 ponto de talento</span></div>${habs}
        ${d.especializacao ? '<div class="texto-festa" style="color:var(--arcano)">Uma encruzilhada se aproxima: em breve você escolherá sua especialização.</div>' : ""}
        ${d.nota ? `<div class="texto-festa">${h(d.nota)}</div>` : ""}
        <div class="dica">Seus pontos de talento: ${d.pontos}. Gaste em Talentos (tecla T no menu de um local).</div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("subir");
      particulas(["#f2c94c", "#fff3a0", "#ff9d4d", "#8fbf6a"], 90);
      setTimeout(() => contarGanhos(caixa), 0);
    } else if (m.tipo === "sigilo") {
      const los = [0, 1, 2].map((i) => `<i class="${i < d.sigilos ? "tem" : ""}${i === d.sigilos - 1 ? " novo" : ""}"></i>`).join("");
      html = `<div class="festa moldura"><div class="rotulo-festa">${h(d.guardiao)} caiu</div><div class="grande">Sigilo ${d.sigilos}/3</div>
        <div class="losangos">${los}</div><div class="texto-festa">Uma runa ardente se grava na sua mão.</div>
        <div class="lista"><span class="ganho ouro">${S("estrela", 1)}+1 ponto de talento</span></div>
        <button class="continuar" type="button">Continuar <span>▸</span></button></div>`;
      App.som("fanfarra");
      particulas(["#f2c94c", "#ff4020", "#fff3a0"], 110);
    } else if (m.tipo === "spec") {
      const habs = d.habilidades.map((x, i) => `<div class="habilidade-nova" style="animation-delay:${0.6 + i * 0.25}s"><span class="rotulo-festa">nova habilidade</span><b>${h(x.nome)}</b>${Realce.texto(x.desc)}</div>`).join("");
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

  /** Contratos cumpridos: os cartazes chegam, o carimbo bate em cada um, o total aparece, e "Receber" faz as
   *  moedas voarem até o seu ouro. Um momento só, em vez de três blocos de texto no registro. */
  function pagarContratos(caixa, d) {
    const um = d.contratos.length === 1;
    const cartazes = d.contratos.map((c, i) => `<div class="pago" style="--i:${i}">${cartaz({ ...c, recebendo: true }, true, false, App.estado ? App.estado.heroi.nivel : 1)}</div>`).join("");
    const atraso = 0.5 + d.contratos.length * 0.35;
    const ganhos = [[d.ouro, "moeda", "ouro", "ouro"], [d.xp, "estrela", "XP", ""], [d.reputacao, "coroa", "reputação", "rep"]]
      .filter(([v]) => v > 0)
      .map(([v, ic, nome, cls], i) => `<span class="ganho ${cls}" style="animation-delay:${atraso + i * 0.15}s">${S(ic, 1)}+${v} ${nome}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-contratos moldura">
      <div class="rotulo-festa">${um ? "contrato cumprido" : `${d.contratos.length} contratos cumpridos`}</div>
      <div class="cartazes-pagos">${cartazes}</div>
      <div class="lista">${ganhos}</div>
      <button class="continuar" type="button">Receber recompensa <span>▸</span></button></div>`;
    caixa.hidden = false;
    App.som("achado");
    d.contratos.forEach((_, i) => setTimeout(() => App.som("equipar"), (0.45 + i * 0.35) * 1000));
    return new Promise((resolver) => {
      let feito = false;
      const receber = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        App.som("moeda");
        moedasPara(caixa.querySelector(".ganho.ouro") || caixa.querySelector(".continuar"), document.querySelector('.recurso[data-rec="ouro"]'));
        particulas(["#f2c94c", "#fff3a0", "#d4af37"], 40);
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; resolver(); }, 650);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); receber(); } };
      setTimeout(() => document.addEventListener("keydown", tecla, true), 600);
      caixa.querySelector(".continuar").addEventListener("click", (ev) => { ev.stopPropagation(); receber(); });
    });
  }

  /** A virada do dia: a aurora na paisagem, a faixa "Dia N" e o que a noite fez, em ícones (verde o que fez bem,
   *  amarelo o que pede atenção, vermelho o que dói). Noite tranquila: some sozinho; noite ruim: espera o clique. */
  const ICONE_NOITE = { bom: "bom", neutro: "", aviso: "aviso", perigo: "perigo" };
  /** Os quadros rápidos sobre o jogo (amanhecer, espólio) ficam no meio da coluna do jogo, e não no meio da janela:
   *  os painéis dos lados têm larguras diferentes, e o quadro ficava torto em relação à cena. `sobreTitulo`: na altura
   *  em que o título do lugar fica no quadro da página (o amanhecer, curto); senão, no meio da coluna. A altura vem do
   *  quadro da página, que não rola: o título rola junto com o texto, e o quadro saía fora do lugar. Numa tela estreita,
   *  sem a coluna, ficam no meio da janela. */
  function noPalco(festa, sobreTitulo = false) {
    const palco = document.getElementById("palco"), p = palco && palco.getBoundingClientRect();
    if (!festa || !p || !p.width) return;
    const pg = document.getElementById("pagina").getBoundingClientRect();
    const y = sobreTitulo && pg.height ? pg.top + Math.min(pg.height * 0.4, 230) : p.top + p.height * 0.45;
    const meio = festa.offsetHeight / 2 + 8;
    festa.classList.add("no-palco");
    festa.style.left = p.left + p.width / 2 + "px";
    festa.style.top = Math.max(meio, Math.min(innerHeight - meio, y)) + "px";
  }

  function amanhecer(caixa, d) {
    if (typeof Vista !== "undefined") Vista.amanhecer(1800);
    App.som("amanhecer");
    const ruim = d.itens.some((x) => x.tipo === "perigo");
    const itens = d.itens.map((x, i) => `<span class="noite-item ${ICONE_NOITE[x.tipo] || ""}" style="animation-delay:${0.55 + i * 0.12}s"${x.texto && x.texto !== x.curto ? ` title="${h(x.texto)}"` : ""}>${S(x.icone, 1)}${h(x.curto)}</span>`).join("");
    caixa.innerHTML = `<div class="festa festa-amanhecer">
      <div class="rotulo-festa">amanhece</div>
      <div class="dia-numero">Dia ${d.dia}</div>
      <div class="dia-clima">${h(d.clima)}</div>
      ${itens ? `<div class="noite">${itens}</div>` : ""}
      ${ruim ? '<button class="continuar" type="button">Continuar <span>▸</span></button>' : ""}</div>`;
    caixa.classList.add("leve");
    caixa.hidden = false;
    noPalco(caixa.querySelector(".festa-amanhecer"), true);
    return new Promise((resolver) => {
      let feito = false;
      const fechar = () => {
        if (feito) return;
        feito = true;
        document.removeEventListener("keydown", tecla, true);
        document.removeEventListener("pointerdown", clique, true);
        const festa = caixa.querySelector(".festa-amanhecer");
        if (festa) festa.classList.add("saindo");
        setTimeout(() => { caixa.hidden = true; caixa.innerHTML = ""; caixa.classList.remove("leve"); resolver(); }, 260);
      };
      const tecla = (ev) => { if ([" ", "Enter", "Escape"].includes(ev.key)) { ev.preventDefault(); ev.stopPropagation(); fechar(); } };
      const clique = (ev) => { ev.preventDefault(); ev.stopPropagation(); fechar(); };
      setTimeout(() => { document.addEventListener("keydown", tecla, true); document.addEventListener("pointerdown", clique, true); }, 500);
      if (!ruim) setTimeout(fechar, 2400 + d.itens.length * 350);
    });
  }

  /** Moedas voando de um ponto da tela até outro (o ouro do topo). */
  function moedasPara(de, para) {
    if (!de || !para) return;
    const a = de.getBoundingClientRect(), b = para.getBoundingClientRect();
    for (let i = 0; i < 10; i++) {
      const m = document.createElement("span");
      m.className = "moeda-voando";
      m.innerHTML = S("moeda", 1);
      m.style.left = a.left + a.width / 2 + (Math.random() - 0.5) * 40 + "px";
      m.style.top = a.top + a.height / 2 + "px";
      document.body.appendChild(m);
      m.animate([{ transform: "translate(0, 0) scale(1)", opacity: 1 },
        { transform: `translate(${b.left + b.width / 2 - a.left - a.width / 2}px, ${b.top + b.height / 2 - a.top - a.height / 2}px) scale(0.6)`, opacity: 0.9 }],
        { duration: 520 + i * 40, delay: i * 35, easing: "cubic-bezier(.5,0,.8,.6)", fill: "forwards" }).finished
        .then(() => { m.remove(); para.classList.remove("ganhou"); void para.offsetWidth; para.classList.add("ganhou"); }).catch(() => m.remove());
    }
  }

  /** Uma linha curta para o registro (histórico) de cada festa: o registro guarda o fato, a festa mostra. */
  function resumoCelebracao(m) {
    const d = m.dados || {};
    if (m.tipo === "nivel") return `▸ Nível ${d.nivel}: +1 ponto de talento${(d.habilidades || []).length ? ", " + d.habilidades.map((x) => x.nome).join(", ") : ""}`;
    if (m.tipo === "contratos") return `▸ ${d.contratos.length === 1 ? "Contrato cumprido" : d.contratos.length + " contratos cumpridos"}: +${d.ouro} ouro, +${d.xp} XP`;
    if (m.tipo === "sigilo") return `▸ Sigilo ${d.sigilos}/3 (${d.guardiao}): +1 ponto de talento`;
    if (m.tipo === "spec") return `▸ Você agora é ${d.nome}`;
    if (m.tipo === "espolio") return `▸ Espólio: ${d.ouro ? `+${d.ouro} ouro, ` : ""}+${d.xp} XP`;
    if (m.tipo === "atributo") return `▸ +${d.valor} ${d.nome} permanente`;
    if (m.tipo === "chegada") return `▸ ${d.primeira ? "Descoberto" : "Chegada"}: ${d.nome}`;
    if (m.tipo === "equipou" && d.achado) return `▸ Vestiu: ${d.item.nome}`;
    if (m.tipo === "guardou") return `▸ Na mochila: ${d.item.nome}`;
    if (m.tipo === "amanhecer") return `▸ Dia ${d.dia} · ${d.clima}${d.itens.length ? " · " + d.itens.map((x) => x.curto).join(", ") : ""}`;
    return "";
  }

  function toast(titulo, texto, icone, bom) {
    const t = document.createElement("div");
    t.className = "toast" + (bom ? " bom" : "");
    t.innerHTML = `${S(icone, 2)}<div>${titulo ? `<b>${h(titulo)}</b>` : ""}${h(texto || "")}</div>`;
    document.getElementById("toasts").appendChild(t);
    setTimeout(() => t.remove(), 3300);
  }

  return { rastreador, atributosHtml, reputacaoHtml, dica, guardarDica, htmlItem, menuUso, abrirGrimorio, alternarGrimorio, abrirDica, dicaAbertaPor, mouseNaArea, novaVisita, fecharMenuItem, guardarArvore, abrirTalentos, fecharTalentos, painel, revelarAchado, celebrar, resumoCelebracao, toast, moedasPara, iconeCriatura, iconeItem, dicaItem, ligarDicas, esconderDica,
    ICONE_ITEM, ARMA, VAZIO, NOME_ESPACO, AREA, barra, aprovacao, noPalco, abrirAchado, acoesDoAchado, fecharAchado };
})();
