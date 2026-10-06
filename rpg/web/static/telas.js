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

  // ------------------------------------------------------------------ painéis
  function slotItem(it, padrao, extra = "") {
    if (!it) return `<div class="slot-px vazio" title="vazio">${S(padrao, 2)}</div>`;
    const icone = it.slot === "arma" ? (App.estado ? ARMA[App.estado.heroi.classe] : "espada") : it.slot === "armadura" ? "armadura" : it.slot === "amuleto" ? "amuleto" : padrao;
    return `<div class="slot-px r-${h(it.raridade)} ${extra}" title="${h(it.nome)}\n${h(it.bonus)}">${S(icone, 2)}</div>`;
  }

  function personagem() {
    const e = App.estado;
    if (!e) return "";
    const p = e.heroi;
    const icAttr = { Ataque: "espada", Defesa: "escudo", Agilidade: "folha", Poder: "chama" };
    const attrs = Object.entries(p.atributos).map(([k, v]) => `<div class="atributo">${S(icAttr[k] || "estrela", 1)}<span class="nome">${h(k)}</span><span class="valor">${v}</span></div>`).join("");
    const bolsa = p.bolsa.map((b) => `<div class="slot-px clicavel" data-item="${h(b.id)}" title="${h(b.nome)}: ${h(b.desc)}\nClique para usar">${S(ICONE_ITEM[b.id] || "pocao", 2)}<span class="qtd">${b.qtd}</span></div>`).join("");
    const mochila = p.mochila.map((it, i) => slotItem(it, "pergaminho", `clicavel" data-mochila="${i}`)).join("");
    return `<div class="tela">
      <div class="ficha-topo"><div class="retrato-grande">${S(p.classe, 6)}</div>
        <div><div class="heroi-nome">${h(p.nome)}</div><div class="heroi-titulo">${h(p.titulo)} · nível ${p.nivel} · ${p.xp}/${p.xp_proximo} XP</div>
        <div class="heroi-titulo">Reputação ${p.reputacao > 0 ? "+" : ""}${p.reputacao}${p.reputacao_txt ? " · " + h(p.reputacao_txt) : ""}</div></div></div>
      <div class="ficha-colunas">
        <div><h4>Atributos</h4><div class="atributos">${attrs}</div>
          <h4>Equipado</h4><div class="slots">${slotItem(p.equip.arma, ARMA[p.classe])}${slotItem(p.equip.armadura, "armadura")}${slotItem(p.equip.amuleto, "amuleto")}</div>
          <div class="linhas" style="margin-top:6px">${["arma", "armadura", "amuleto"].map((s) => p.equip[s] ? `<div class="linha"><span class="r-${h(p.equip[s].raridade)}">${h(p.equip[s].nome)}</span><b style="font-size:15px">${h(p.equip[s].bonus)}</b></div>` : "").join("")}</div></div>
        <div><h4>Bolsa</h4><div class="slots">${bolsa || '<span class="vazio">vazia</span>'}</div>
          <h4>Mochila ${p.mochila.length}/8</h4><div class="slots">${mochila || '<span class="vazio">nada para trocar</span>'}</div>
          <div class="vazio" style="margin-top:6px">Clique num item da bolsa para usar, ou num da mochila para equipar.</div></div>
      </div></div>`;
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
    const div = document.createElement("div");
    div.innerHTML = ({ personagem, diario, bestiario, comitiva }[m.tipo] || (() => ""))(m.dados);
    div.querySelectorAll("[data-item]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); App.pedir("Usar item da bolsa", "item", el.dataset.item); }));
    div.querySelectorAll("[data-mochila]").forEach((el) => el.addEventListener("click", (ev) => { ev.stopPropagation(); App.pedir("Equipar item da mochila", "mochila", Number(el.dataset.mochila)); }));
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
    t.innerHTML = `${S(icone, 2)}<div><b>${h(titulo)}</b>${h(texto || "")}</div>`;
    document.getElementById("toasts").appendChild(t);
    setTimeout(() => t.remove(), 3300);
  }

  return { guardarArvore, abrirTalentos, fecharTalentos, painel, celebrar, toast, iconeCriatura, ICONE_ITEM, ARMA, barra, aprovacao };
})();
