/* Palco de batalha: as cartas da luta (você, a comitiva e os inimigos) em pé sobre a paisagem do lugar.
   Cada lance do motor (ação, golpe, cura, efeito) vira uma animação curta: quem age dá um passo à frente,
   avança até o alvo, o alvo treme e brilha na cor do elemento. Aqui também nascem os balões de fala
   e os selos de "aprova/desaprova" da comitiva. */
"use strict";

const Batalha = (() => {
  const cartas = new Map();  // uid -> elemento da carta
  const recentes = {};       // uid -> instante do último lance (o estado que chega depois não repete o efeito)
  let anteriores = {};       // uid -> ficha do estado anterior
  let arena = null, colAliados = null, colInimigos = null, camadaFx = null;
  let rapido = () => false, pausa = (ms) => ms;
  let emArea = false;

  // Ícone e família de cada efeito de estado (a família dá a cor do brilho na carta).
  const EFEITO = {
    guarda: ["escudo", "protecao"], barreira: ["escudo_azul", "protecao"], esquiva: ["folha", "protecao"],
    fortalecido: ["espada", "forca"], furtivo: ["olho", "sombra"], veneno: ["gota_verde", "veneno"],
    sangramento: ["gota", "sangue"], queimadura: ["chama", "fogo"], atordoado: ["estrela", "atordoado"],
    maldito: ["gota_roxa", "maldicao"], enfraquecido: ["osso", "maldicao"], marcado: ["flecha", "marca"],
  };
  const SOM_ELEMENTO = { fisico: "golpe", fogo: "chama", gelo: "gelo", sagrado: "sagrado", sombra: "sombra",
    arcano: "arcano", veneno: "veneno" };
  const PROJETIL = { fisico: "flecha", fogo: "chama", gelo: "gelo", sagrado: "orbe_luz", sombra: "orbe_sombra",
    arcano: "orbe_arcano", veneno: "gota_verde" };
  const COR_PARTICULA = { fogo: ["#ffb35c", "#e0782f", "#fff3a0"], gelo: ["#ffffff", "#7fb0ff", "#c8e0ff"],
    sagrado: ["#fff3a0", "#f2c94c", "#ffffff"], sombra: ["#8e6fd8", "#5a2a6e", "#2a1f3a"], arcano: ["#c8b0ff", "#8e6fd8", "#7fb0ff"],
    veneno: ["#8fbf6a", "#4f9a5b", "#c8f0a0"], cura: ["#8fbf6a", "#c8f0a0", "#4f9a5b"], roubo: ["#e2574c", "#b3262b", "#6e0d0d"],
    sangue: ["#e2574c", "#b3262b"], protecao: ["#7fb0ff", "#c8e0ff", "#3d63c9"], forca: ["#ffb35c", "#f2c94c"],
    maldicao: ["#8e6fd8", "#5a2a6e"], atordoado: ["#fff3a0", "#f2c94c"], marca: ["#f2c94c", "#e0782f"] };

  const S = (n, e = 2, c = "") => Sprites.img(n, e, c);
  const agora = () => performance.now();
  const dormir = (ms) => (ms > 0 ? new Promise((r) => setTimeout(r, ms)) : Promise.resolve());
  const som = (n) => { if (!rapido()) Som.tocar(n); };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = (a, b) => (b ? Math.max(0, Math.min(100, (100 * a) / b)) : 0);

  function configurar(opts) { rapido = opts.rapido; pausa = opts.pausa; }

  /* ------------------------------------------------------------ montagem */
  function montar() {
    if (arena) return;
    const raiz = document.getElementById("batalha");
    raiz.innerHTML = `<div id="arena"><div class="fileira aliados"></div><div class="fileira inimigos"></div><div class="camada-fx"></div></div>`;
    arena = raiz.firstElementChild;
    colAliados = arena.querySelector(".aliados");
    colInimigos = arena.querySelector(".inimigos");
    camadaFx = arena.querySelector(".camada-fx");
  }

  /** A paisagem (canvas da vista) vira o chão da batalha enquanto ela dura. */
  function paisagem(naArena) {
    const v = document.getElementById("vista");
    if (!v) return;
    if (naArena && v.parentElement !== arena) arena.prepend(v);
    if (!naArena && arena && v.parentElement === arena) document.getElementById("pagina").prepend(v);
  }

  function icone(c) {
    if (c.uid === "j") return c.classe;
    if (c.lado === "aliado") return c.cid || (c.tipo === "servo" ? "caveira" : "fera");
    return Telas.iconeCriatura(c.tracos, c.familia || "");
  }

  function criarCarta(c) {
    const e = document.createElement("div");
    e.dataset.uid = c.uid;
    if (c.cid) e.dataset.cid = c.cid;
    e.innerHTML = `<div class="carta-fx"></div><div class="icone">${S(icone(c), 2)}</div>
      <div class="carta-nome"><span></span><small></small></div>
      <div class="carta-hp"><span class="barra-px ${c.lado === "aliado" ? (c.uid === "j" ? "vida" : "aliado") : "vida"}"><span class="rastro"></span><span class="enchimento"></span></span><span class="num"></span></div>
      ${c.uid === "j" ? '<div class="carta-rec"><span class="barra-px mana"><span class="enchimento"></span></span><span class="num"></span></div>' : ""}
      <div class="carta-efeitos"></div><div class="preparando" hidden>⚠ prepara um golpe devastador</div>`;
    const b = e.querySelector(".carta-hp .barra-px");
    [...b.children].forEach((x) => { x.style.width = pct(c.hp, c.max_hp) + "%"; });
    return e;
  }

  function barra(carta, hp, max) {
    const b = carta.querySelector(".carta-hp .barra-px");
    if (!b) return;
    b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = pct(hp, max) + "%"; });
    carta.querySelector(".carta-hp .num").textContent = hp > 0 ? `${hp}/${max}` : "caído";
  }

  function efeitosHtml(lista) {
    return lista.map((f) => {
      const [ic, fam] = EFEITO[f.id] || ["estrela", "forca"];
      return `<span class="ef fam-${fam}" data-ef="${esc(f.id)}" title="${esc(f.nome)} (${f.turnos} turno${f.turnos === 1 ? "" : "s"})">${S(ic, 1)}<b>${f.turnos > 9 ? "∞" : f.turnos}</b></span>`;
    }).join("");
  }

  function atualizarCarta(el, c, heroi) {
    const classes = ["carta", c.lado];
    if (c.uid === "j") classes.push("heroi");
    if (c.chefe) classes.push("chefe");
    if (c.unico) classes.push("unico");
    if (!c.vivo) classes.push("morta");
    const fams = new Set(c.efeitos.map((f) => (EFEITO[f.id] || [])[1]).filter(Boolean));
    fams.forEach((f) => classes.push("com-" + f));
    // preserva as classes de animação em curso
    ["morrendo", "agindo", "vez", "alvejavel", "atingida"].forEach((k) => { if (el.classList.contains(k)) classes.push(k); });
    el.className = classes.join(" ");
    el.querySelector(".carta-nome span").textContent = c.nome;
    el.querySelector(".carta-nome small").textContent = c.nivel ? `Nv.${c.nivel}` : "";
    barra(el, c.hp, c.max_hp);
    if (c.uid === "j" && heroi) {
      const r = el.querySelector(".carta-rec");
      const tipo = { Vigor: "vigor", Mana: "mana", Foco: "foco" }[heroi.recurso] || "mana";
      r.querySelector(".barra-px").className = "barra-px fina " + tipo;
      r.querySelector(".enchimento").style.width = pct(heroi.rec, heroi.max_rec) + "%";
      r.querySelector(".num").textContent = `${heroi.rec}/${heroi.max_rec}`;
      el.title = `${c.nome} · ${heroi.recurso} ${heroi.rec}/${heroi.max_rec}`;
    } else el.title = c.nome;
    const ef = el.querySelector(".carta-efeitos");
    const html = c.vivo ? efeitosHtml(c.efeitos) : "";
    if (ef.innerHTML !== html) ef.innerHTML = html;
    el.querySelector(".preparando").hidden = !(c.preparando && c.vivo);
  }

  /** Desenha (ou atualiza no lugar) as cartas a partir do estado do combate. */
  function desenhar(cb, heroi, replay) {
    if (!cb) {
      if (arena) paisagem(false);
      cartas.clear(); anteriores = {}; emArea = false;
      if (arena) { colAliados.innerHTML = ""; colInimigos.innerHTML = ""; camadaFx.innerHTML = ""; }
      return;
    }
    montar();
    paisagem(true);
    const aliados = [cb.heroi, ...cb.aliados.filter((a) => a.vivo || a.cid || (anteriores[a.uid] && anteriores[a.uid].vivo))];
    const lista = [...aliados, ...cb.inimigos];
    const vistos = new Set();
    let morte = false, golpe = false;
    for (const c of lista) {
      if (!c || !c.uid) continue;
      vistos.add(c.uid);
      let el = cartas.get(c.uid);
      const ant = anteriores[c.uid];
      const nova = !el;
      if (nova) { el = criarCarta(c); cartas.set(c.uid, el); }
      atualizarCarta(el, c, heroi);
      const col = c.lado === "aliado" ? colAliados : colInimigos;
      if (el.parentElement !== col) { col.appendChild(el); if (!replay && ant === undefined && anteriores.__iniciado) entrar(el, c.lado); }
      if (!ant || replay) continue;
      const fresco = recentes[c.uid] && agora() - recentes[c.uid] < 1500;
      if (ant.vivo && !c.vivo) { morrer(el); morte = true; continue; }
      if (!ant.vivo && c.vivo) el.classList.remove("morta", "morrendo");
      if (!fresco && c.hp < ant.hp) { tremer(el); numero(el, `−${ant.hp - c.hp}`, "menos"); golpe = true; }
      if (!fresco && c.hp > ant.hp && c.max_hp === ant.max_hp) { brilho(el, "cura"); numero(el, `+${c.hp - ant.hp}`, "cura"); }
      const tinha = new Set(ant.efeitos.map((f) => f.id));
      c.efeitos.filter((f) => !tinha.has(f.id)).forEach((f) => {
        const fam = (EFEITO[f.id] || [])[1] || "forca";
        brilho(el, fam);
        const tag = el.querySelector(`.ef[data-ef="${f.id}"]`);
        if (tag) { tag.classList.add("novo"); tag.onanimationend = () => tag.classList.remove("novo"); }
        if (!fresco) som(["protecao", "forca"].includes(fam) ? "protecao" : "feitico");
      });
    }
    for (const [uid, el] of cartas) {
      if (!vistos.has(uid)) { el.remove(); cartas.delete(uid); }
    }
    // ordem: você primeiro, depois a comitiva; inimigos na ordem do motor.
    // Só mexe no DOM se a ordem mudou: reinserir um nó reinicia as animações dele.
    [[colAliados, aliados], [colInimigos, cb.inimigos]].forEach(([col, grupo]) => {
      const desejada = grupo.map((c) => c && cartas.get(c.uid)).filter((e) => e && e.parentElement === col);
      const atual = [...col.children];
      if (desejada.some((e, i) => atual[i] !== e)) desejada.forEach((e) => col.appendChild(e));
    });
    colInimigos.classList.toggle("duas", cb.inimigos.length > 3);
    colAliados.classList.toggle("duas", aliados.length > 4);
    anteriores = { __iniciado: true };
    lista.forEach((c) => { if (c && c.uid) anteriores[c.uid] = c; });
    if (!replay) { if (morte) som("morte"); else if (golpe) som("golpe"); }
  }

  /* ------------------------------------------------------------ movimento */
  function pos(el) {
    const r = el.getBoundingClientRect();
    return { x: r.left - (el._x || 0) + r.width / 2, y: r.top - (el._y || 0) + r.height / 2, w: r.width, h: r.height };
  }
  function ir(el, x, y, ms, curva = "ease-out") {
    const de = `${el._x || 0}px ${el._y || 0}px`;
    el._x = Math.round(x); el._y = Math.round(y);
    const para = `${el._x}px ${el._y}px`;
    el.style.translate = para;
    if (!ms || rapido()) return Promise.resolve();
    return el.animate([{ translate: de }, { translate: para }], { duration: ms, easing: curva }).finished.catch(() => {});
  }
  function lado(el) { return el.classList.contains("inimigo") ? -1 : 1; }
  function entrar(el, l) {
    el.animate([{ opacity: 0, translate: `${l === "aliado" ? -30 : 30}px 0px` }, { opacity: 1, translate: "0px 0px" }], { duration: 300, easing: "steps(5)" });
  }

  async function passoFrente(el, area) {
    el.classList.add("agindo");
    if (area) {
      const a = pos(el), ra = arena.getBoundingClientRect();
      await ir(el, (ra.left + ra.width / 2 - a.x) * 0.55, 0, pausa(200), "ease-in-out");
    } else await ir(el, 26 * lado(el), 0, pausa(130));
  }
  async function voltar(el) {
    el.classList.remove("agindo");
    await ir(el, 0, 0, pausa(160));
    el.style.translate = "";
  }
  async function investir(ator, alvo) {
    const a = pos(ator), b = pos(alvo);
    const dx = b.x - a.x, dy = b.y - a.y;
    const folga = (a.w + b.w) / 2 - 10;
    const f = Math.abs(dx) > folga ? (Math.abs(dx) - folga) / Math.abs(dx) : 0.35;
    await ir(ator, dx * f, dy * f, pausa(120), "cubic-bezier(.55,0,1,.45)");
  }

  async function projetil(de, para, sprite) {
    if (rapido()) return;
    const ra = arena.getBoundingClientRect(), a = de.getBoundingClientRect(), b = para.getBoundingClientRect();
    const x0 = a.left + a.width / 2 - ra.left - 16, y0 = a.top + a.height / 2 - ra.top - 16;
    const x1 = b.left + b.width / 2 - ra.left - 16, y1 = b.top + b.height / 2 - ra.top - 16;
    const ang = sprite === "flecha" ? Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI + 45 : 0;
    const p = document.createElement("div");
    p.className = "projetil" + (sprite === "flecha" ? "" : " brilhante");
    p.innerHTML = S(sprite, 2);
    camadaFx.appendChild(p);
    const quadros = [{ transform: `translate(${x0}px, ${y0}px) rotate(${ang}deg) scale(0.6)` },
      { transform: `translate(${(x0 + x1) / 2}px, ${(y0 + y1) / 2 - 14}px) rotate(${ang}deg) scale(1.1)` },
      { transform: `translate(${x1}px, ${y1}px) rotate(${ang}deg) scale(1)` }];
    await p.animate(quadros, { duration: pausa(240), easing: "linear" }).finished.catch(() => {});
    p.remove();
  }

  /* ------------------------------------------------------------ efeitos visuais */
  function reiniciar(el, classe, ms) {
    el.classList.remove(classe); void el.offsetWidth; el.classList.add(classe);
    setTimeout(() => el.classList.remove(classe), ms);
  }
  function tremer(el, forte) { reiniciar(el, forte ? "atingida-forte" : "atingida", 420); }
  function clarao(el, elemento) {
    const fx = el.querySelector(".carta-fx");
    if (!fx || rapido()) return;
    fx.className = "carta-fx"; void fx.offsetWidth; fx.className = "carta-fx el-" + elemento;
    fx.onanimationend = () => { fx.className = "carta-fx"; };
  }
  function brilho(el, fam) { reiniciar(el, "aura-" + fam, 900); particulas(el, fam, fam === "cura" || fam === "roubo" ? 12 : 7); }
  function numero(el, texto, classe) {
    if (rapido()) return;
    const n = document.createElement("span");
    n.className = "flutua " + classe;
    n.textContent = texto;
    n.style.left = 30 + Math.random() * 40 + "%";
    el.appendChild(n);
    setTimeout(() => n.remove(), 1300);
  }
  function rotulo(el, texto, classe = "") {
    if (!texto || rapido()) return;
    const velho = el.querySelector(".faixa-acao");
    if (velho) velho.remove();
    const f = document.createElement("div");
    f.className = "faixa-acao " + classe;
    f.textContent = texto;
    el.appendChild(f);
    setTimeout(() => f.remove(), 1500);
  }
  function particulas(el, fam, n = 7) {
    if (rapido()) return;
    const cores = COR_PARTICULA[fam] || COR_PARTICULA.forca;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "particula-carta" + (fam === "roubo" ? " desce" : "");
      p.style.left = 8 + Math.random() * 84 + "%";
      p.style.background = cores[i % cores.length];
      p.style.animationDelay = Math.random() * 300 + "ms";
      el.appendChild(p);
      setTimeout(() => p.remove(), 1300);
    }
  }
  function labaredas(el) {
    if (rapido()) return;
    for (let i = 0; i < 5; i++) {
      const f = document.createElement("span");
      f.className = "labareda";
      f.innerHTML = S("chama", 1);
      f.style.left = 6 + i * 19 + Math.random() * 8 + "%";
      f.style.animationDelay = i * 60 + "ms";
      el.appendChild(f);
      setTimeout(() => f.remove(), 1100);
    }
  }
  function morrer(el) { reiniciar(el, "morrendo", 900); }

  /* ------------------------------------------------------------ lances do motor */
  const carta = (uid) => (uid ? cartas.get(uid) : null);
  function marcar(...uids) { uids.forEach((u) => { if (u) recentes[u] = agora(); }); }

  async function lance(m) {
    if (!arena) return;
    const de = carta(m.de), em = carta(m.em);
    switch (m.tipo) {
      case "acao": {
        if (!de) return;
        emArea = !!m.area;
        rotulo(de, m.nome, de.classList.contains("inimigo") ? "inimiga" : "");
        await passoFrente(de, m.area);
        if (m.hab === "redemoinho") de.classList.add("girando");
        return;
      }
      case "fim_acao": {
        if (!de) return;
        de.classList.remove("girando");
        emArea = false;
        await voltar(de);
        return;
      }
      case "golpe": return golpe(m, de, em);
      case "giro": {
        if (!de) return;
        reiniciar(de, "giro", 320);
        som("esquiva");
        await dormir(pausa(180));
        return;
      }
      case "erro": {
        marcar(m.em);
        if (de && em) { if (m.alcance === "distancia" || emArea) await projetil(de, em, "flecha"); else await investir(de, em); }
        if (em) {
          if (m.motivo === "esquiva") reiniciar(em, "esquivou", 420);
          numero(em, m.motivo === "imune" ? "imune" : "esquiva", "info");
        }
        som("esquiva");
        if (de && !emArea) ir(de, 26 * lado(de), 0, pausa(150));
        await dormir(pausa(260));
        return;
      }
      case "cura": {
        marcar(m.em);
        if (de && de !== em) { brilho(de, "cura"); await dormir(pausa(160)); }
        if (em) {
          barra(em, m.hp, m.max_hp);
          brilho(em, m.modo === "roubo" ? "roubo" : "cura");
          numero(em, `+${m.valor}`, m.modo === "roubo" ? "roubo" : "cura");
          if (m.rotulo && m.modo !== "roubo" && !de) rotulo(em, m.rotulo);
        }
        som(m.modo === "roubo" ? "roubo" : "cura");
        await dormir(pausa(420));
        return;
      }
      case "tique": {
        if (!em) return;
        marcar(m.em);
        barra(em, m.hp, m.max_hp);
        const fam = (EFEITO[m.efeito] || [])[1] || "sangue";
        clarao(em, fam === "fogo" ? "fogo" : fam === "veneno" ? "veneno" : fam === "maldicao" ? "sombra" : "fisico");
        tremer(em);
        if (fam === "fogo") labaredas(em); else particulas(em, fam, 6);
        numero(em, `−${m.dano}`, "menos");
        som(fam === "fogo" ? "chama" : fam === "veneno" ? "veneno" : "dor_leve");
        if (m.em === "j") App.doer();
        await dormir(pausa(380));
        return;
      }
      case "efeito": {
        if (!em) return;
        marcar(m.em);
        const fam = (EFEITO[m.efeito] || [])[1] || "maldicao";
        brilho(em, fam);
        if (m.efeito === "queimadura") labaredas(em);
        numero(em, m.rotulo, "info");
        som(m.efeito === "atordoado" ? "atordoar" : "feitico");
        await dormir(pausa(300));
        return;
      }
      case "feitico": {
        if (de && em) { brilho(de, "maldicao"); rotulo(de, m.rotulo); await projetil(de, em, PROJETIL[m.elemento] || "orbe_sombra"); }
        som("sombra");
        return;
      }
      case "atordoado": {
        if (!em) return;
        reiniciar(em, "tonto", 900);
        numero(em, m.rotulo || "atordoado", "info");
        som("atordoar");
        await dormir(pausa(420));
        return;
      }
      case "fase": {
        if (!em) return;
        reiniciar(em, "furia", 1200);
        som("rugido");
        await dormir(pausa(700));
        return;
      }
    }
  }

  async function golpe(m, de, em) {
    if (!em) return;
    marcar(m.em);
    const el = m.elemento || "fisico";
    const distancia = m.alcance === "distancia";
    if (de && de !== em) {
      if (de.classList.contains("girando")) {
        await dormir(pausa(40));
      } else if (emArea && !distancia) {
        reiniciar(de, "giro", 300);
        await dormir(pausa(140));
      } else if (distancia || emArea) {
        som(el === "fisico" ? "disparo" : "lancar");
        await projetil(de, em, PROJETIL[el] || "flecha");
      } else await investir(de, em);
    }
    // impacto
    barra(em, m.hp, m.max_hp);
    clarao(em, el);
    tremer(em, m.crit);
    if (el === "fogo") labaredas(em);
    else if (el !== "fisico") particulas(em, el, 8);
    if (m.crit) numero(em, `${m.dano}!`, "crit");
    else numero(em, `−${m.dano}`, "menos");
    if (m.absorvido) numero(em, `(${m.absorvido})`, "escudo");
    if (m.eficacia === "super") rotulo(em, "fraqueza!", "boa");
    else if (m.eficacia === "pouco") rotulo(em, "resiste", "ruim");
    som(m.crit ? "critico_golpe" : SOM_ELEMENTO[el] || "golpe");
    if (el !== "fisico" && !m.crit) setTimeout(() => som("golpe_leve"), 60);
    if (m.em === "j") { App.doer(); som("dor"); }
    if (de && de !== em && !de.classList.contains("girando") && !distancia && !emArea) ir(de, 26 * lado(de), 0, pausa(170));
    await dormir(pausa(de && de.classList.contains("girando") ? 110 : m.crit ? 420 : 300));
  }

  /* ------------------------------------------------------------ vez e alvos */
  function vez(uid) {
    cartas.forEach((el, u) => el.classList.toggle("vez", u === uid));
  }
  function alvos(opcoes, escolher) {
    limparAlvos();
    opcoes.forEach((o, i) => {
      const el = o.meta && carta(o.meta.alvo);
      if (!el) return;
      el.classList.add("alvejavel");
      el._escolher = () => escolher(i);
      el.addEventListener("click", el._escolher);
    });
  }
  function limparAlvos() {
    cartas.forEach((el) => {
      el.classList.remove("alvejavel", "mirando");
      if (el._escolher) { el.removeEventListener("click", el._escolher); el._escolher = null; }
    });
  }
  function mirar(uid, ligado) { const el = carta(uid); if (el) el.classList.toggle("mirando", ligado); }

  /* ------------------------------------------------------------ comitiva: falas e opiniões */
  function ancora(cid) {
    const vis = (e) => e && e.offsetParent !== null;
    const opcoes = [document.querySelector(`#arena .carta[data-cid="${cid}"]`), document.querySelector(`.hud-membro[data-cid="${cid}"]`),
      document.querySelector(`#heroi .membro[data-cid="${cid}"]`)];
    return opcoes.find(vis) || null;
  }
  const baloes = {};
  function balao(cid, nome, texto) {
    const alvo = ancora(cid);
    if (!alvo) { Telas.toast(nome, texto, cid, true); return 1600; }
    if (baloes[cid]) baloes[cid].remove();
    const b = document.createElement("div");
    const narrado = !/^["“«—]/.test(texto.trim());
    b.className = "balao" + (narrado ? " narrado" : "");
    b.innerHTML = `<b>${esc(nome)}</b><span>${esc(texto.replace(/^["“]|["”]$/g, ""))}</span>`;
    document.body.appendChild(b);
    const r = alvo.getBoundingClientRect(), w = b.offsetWidth, h = b.offsetHeight;
    let x = r.left + r.width / 2 - w / 2;
    x = Math.max(8, Math.min(innerWidth - w - 8, x));
    let y = r.top - h - 12;
    if (y < 52) { y = r.bottom + 12; b.classList.add("abaixo"); }
    b.style.left = x + "px"; b.style.top = y + "px";
    b.style.setProperty("--rabo", Math.max(14, Math.min(w - 14, r.left + r.width / 2 - x)) + "px");
    baloes[cid] = b;
    alvo.classList.remove("falando"); void alvo.offsetWidth; alvo.classList.add("falando");
    const dur = Math.min(8000, 2600 + texto.length * 45);
    b.addEventListener("click", () => b.remove());
    setTimeout(() => { b.classList.add("sumindo"); setTimeout(() => { b.remove(); alvo.classList.remove("falando"); }, 300); }, dur);
    som("fala");
    return Math.min(1600, 500 + texto.length * 18);
  }
  function opiniao(cid, nome, delta) {
    const bom = delta > 0, forte = Math.abs(delta) >= 8;
    const alvo = ancora(cid);
    som(bom ? "aprova" : "desaprova");
    const texto = `${nome} ${bom ? "aprova" : "desaprova"}${forte ? " muito" : ""}`;
    if (!alvo) { Telas.toast("", texto, cid, bom); return; }
    const s = document.createElement("div");
    s.className = `selo ${bom ? "aprova" : "desaprova"}${forte ? " forte" : ""}`;
    s.innerHTML = `<i>${bom ? "▲" : "▼"}</i>${esc(texto)}`;
    document.body.appendChild(s);
    const r = alvo.getBoundingClientRect();
    s.style.left = Math.max(8, Math.min(innerWidth - s.offsetWidth - 8, r.left + r.width / 2 - s.offsetWidth / 2)) + "px";
    s.style.top = Math.max(50, r.top - 6) + "px";
    setTimeout(() => s.remove(), 2300);
    alvo.classList.remove("reagiu-bem", "reagiu-mal"); void alvo.offsetWidth;
    alvo.classList.add(bom ? "reagiu-bem" : "reagiu-mal");
    setTimeout(() => alvo.classList.remove("reagiu-bem", "reagiu-mal"), 900);
  }

  return { configurar, desenhar, lance, vez, alvos, limparAlvos, mirar, balao, opiniao };
})();
