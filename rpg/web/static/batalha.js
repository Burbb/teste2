/* Palco de batalha: as cartas da luta (você, a comitiva e os inimigos) em pé sobre a paisagem do lugar.
   Cada lance do motor (ação, golpe, cura, efeito) vira uma animação curta: quem age dá um passo à frente,
   avança até o alvo, o alvo treme e brilha na cor do elemento. Aqui também nascem os balões de fala
   e os selos de "aprova/desaprova" da comitiva. */
"use strict";

const Batalha = (() => {
  const cartas = new Map();  // uid -> elemento da carta
  const recentes = {};       // uid -> instante do último lance (o estado que chega depois não repete o som do efeito)
  let anteriores = {};       // uid -> ficha do estado anterior
  let arena = null, colAliados = null, colInimigos = null, camadaFx = null;
  let rapido = () => false, pausa = (ms) => ms;
  let emArea = false;

  // Ícone, família (a cor do brilho na carta) e dica de cada estado: vêm do motor (catálogo em rpg/estados.py).
  let ESTADOS = {};
  function catalogo(c) { if (c) ESTADOS = c; }
  const efeito = (id) => { const e = ESTADOS[id]; return e ? [e.icone, e.familia] : ["estrela", "forca"]; };
  const SOM_ELEMENTO = { fisico: "golpe", fogo: "chama", gelo: "gelo", sagrado: "sagrado", sombra: "sombra",
    arcano: "arcano", veneno: "veneno" };
  const PROJETIL = { fisico: "flecha", fogo: "chama", gelo: "gelo", sagrado: "orbe_luz", sombra: "orbe_sombra",
    arcano: "orbe_arcano", veneno: "gota_verde" };
  const COR_PARTICULA = { fogo: ["#ffb35c", "#e0782f", "#fff3a0"], gelo: ["#ffffff", "#7fb0ff", "#c8e0ff"],
    sagrado: ["#fff3a0", "#f2c94c", "#ffffff"], sombra: ["#8e6fd8", "#5a2a6e", "#2a1f3a"], arcano: ["#c8b0ff", "#8e6fd8", "#7fb0ff"],
    veneno: ["#8fbf6a", "#4f9a5b", "#c8f0a0"], cura: ["#8fbf6a", "#c8f0a0", "#4f9a5b"], roubo: ["#e2574c", "#b3262b", "#6e0d0d"],
    sangue: ["#e2574c", "#b3262b"], protecao: ["#7fb0ff", "#c8e0ff", "#3d63c9"], forca: ["#ffb35c", "#f2c94c"],
    maldicao: ["#8e6fd8", "#5a2a6e"], mana: ["#a8c4ff", "#4d74e0", "#ffffff"], vigor: ["#ffb35c", "#f2c94c", "#fff3a0"],
    foco: ["#c8f0a0", "#8fbf6a", "#ffffff"], atordoado: ["#fff3a0", "#f2c94c"], marca: ["#f2c94c", "#e0782f"] };

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
    // #roda: na sua vez, as ações aparecem ali, em volta da sua carta (ver escolhas.js).
    raiz.innerHTML = `<div id="arena"><div class="fileira aliados"></div><div class="fileira inimigos"></div><div class="camada-fx"></div><div id="roda"></div></div>`;
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
    if (c.lado === "aliado") return c.cid || (c.tipo === "servo" ? "caveira" : c.tipo === "falcao" ? "voador" : "fera");
    return Telas.iconeCriatura(c.tracos, c.familia || "");
  }

  function criarCarta(c) {
    const e = document.createElement("div");
    e.dataset.uid = c.uid;
    if (c.cid) e.dataset.cid = c.cid;
    if (c.tipo) e.dataset.tipo = c.tipo;
    e.innerHTML = `<div class="carta-fx"></div><div class="icone">${S(icone(c), 2)}</div>
      <div class="carta-nome"><span></span><small></small></div>
      <div class="carta-hp"><span class="barra-px vida"><span class="rastro"></span><span class="enchimento"></span></span><span class="num"></span></div>
      ${c.uid === "j" ? '<div class="carta-rec"><span class="barra-px mana"><span class="enchimento"></span></span><span class="num"></span></div><div class="carta-flechas" hidden></div>' : ""}
      <div class="carta-efeitos"></div><div class="preparando" hidden>⚠ prepara um golpe devastador</div>`;
    barra(e, c.hp, c.max_hp);
    if (c.lado === "inimigo") {  // a ficha do inimigo aparece ao passar o mouse (no lugar do antigo "Analisar")
      e.addEventListener("mouseenter", () => mostrarFicha(e));
      // A carta sair de baixo do mouse (avançando para atacar) não fecha a ficha: só o mouse sair do lugar.
      e.addEventListener("mouseleave", () => { if (!Telas.mouseNaArea()) esconderFicha(); });
    }
    return e;
  }

  /** A vida na carta. A carta lembra o que mostra (_hp): quando o estado chega depois dos lances, só o que eles
   *  ainda não mostraram vira número (o Redemoinho não "apanha de novo" depois do roubo de vida). */
  function barra(carta, hp, max) {
    carta._hp = hp;
    const b = carta.querySelector(".carta-hp .barra-px");
    if (!b) return;
    b.querySelectorAll(".rastro, .enchimento").forEach((x) => { x.style.width = pct(hp, max) + "%"; });
    carta.querySelector(".carta-hp .num").textContent = hp > 0 ? `${hp}/${max}` : "caído";
  }

  function efeitosHtml(lista) {
    return lista.map((f) => {
      const [ic, fam] = efeito(f.id);
      const dano = f.por_turno ? ` · ${f.por_turno} de dano por turno` : "";
      const extra = ESTADOS[f.id] && ESTADOS[f.id].dica ? ` · ${ESTADOS[f.id].dica}` : "";
      const camadas = f.camadas ? `<i class="camadas">×${f.camadas}</i>` : "";
      return `<span class="ef fam-${fam}${f.camadas ? " acumulado" : ""}" data-ef="${esc(f.id)}" title="${esc(f.nome)} (${f.turnos} turno${f.turnos === 1 ? "" : "s"})${dano}${extra}">${S(ic, 1)}<b>${f.turnos > 9 ? "∞" : f.turnos}</b>${camadas}</span>`;
    }).join("");
  }

  const ICONE_TRACO = { fera: "fera", humano: "humano", voador: "voador", blindado: "escudo", "morto-vivo": "caveira",
    etereo: "etereo", planta: "planta", construto: "construto", gigante: "martelo", corrompido: "corrompido",
    conjurador: "cajado", demonio: "demonio" };
  const ELEMENTO = { fisico: ["espada", "corpo a corpo"], distancia: ["flecha", "à distância"], fogo: ["chama", "fogo"],
    gelo: ["gelo", "gelo"], sagrado: ["orbe_luz", "sagrado"], sombra: ["orbe_sombra", "sombra"], arcano: ["orbe_arcano", "arcano"],
    veneno: ["gota_verde", "veneno"] };
  function mostrarFicha(el) {
    const c = el._ficha;
    if (!c || !c.ficha || !escolhendo) return;
    if (Telas.dicaAbertaPor(el)) return;  // já aberta (a carta voltou para baixo do mouse): fica onde está
    const f = c.ficha;
    const caixa = Telas.abrirDica(el, true);
    const tracos = f.tracos.map((t) => `<span class="ficha-traco" title="${esc(t.texto)}">${S(ICONE_TRACO[t.id] || "estrela", 2)}<small>${esc(t.id)}</small></span>`).join("");
    let corpo;
    const linha = (filtro, classe) => Object.entries(f.mult).filter(([, v]) => filtro(v)).map(([k, v]) => {
      const [ic, nome] = ELEMENTO[k] || ["estrela", k];
      return `<span class="ficha-mult ${classe}">${S(ic, 2)}<b>${v === 0 ? "imune" : "×" + String(v).replace(".", ",")}</b><small>${nome}</small></span>`;
    }).join("");
    // O bestiário da espécie libera aos poucos: primeiro as fraquezas, depois as resistências.
    const fracos = f.conhecido ? linha((v) => v >= 1.15, "fraco") : "";
    const fortes = f.resistencias ? linha((v) => v <= 0.85, "forte") : "";
    corpo = (f.conhecido ? (fracos ? `<div class="ficha-titulo bom">Fraco contra</div><div class="ficha-linha">${fracos}</div>`
        : '<div class="ficha-titulo">Sem fraquezas</div>') : '<div class="ficha-titulo">Fraquezas: ???</div>') +
      (f.resistencias ? (fortes ? `<div class="ficha-titulo ruim">Resiste a</div><div class="ficha-linha">${fortes}</div>`
        : '<div class="ficha-titulo">Sem resistências</div>') : f.conhecido ? '<div class="ficha-titulo">Resistências: ???</div>' : "") +
      (f.progresso ? `<div class="pior ficha-progresso">${esc(f.progresso)}</div>` : "");
    caixa.innerHTML = `<b>${esc(c.nome)}</b><div class="tipo">Nível ${c.nivel}${c.chefe ? " · chefe" : ""} · ataque ${f.atk} · defesa ${f.defesa}</div>
      <div class="ficha-tracos">${tracos}</div>${corpo}${f.ponto_fraco ? '<div class="rodape">Você conhece o ponto fraco: +25% de dano!</div>' : ""}`;
    caixa.classList.add("ficha-inimigo");
    const r = el.getBoundingClientRect();
    const esq = r.left - 300 < 6 ? r.right + 10 : r.left - 300;
    caixa.style.left = Math.max(6, Math.min(innerWidth - 296, esq)) + "px";
    // Nunca por cima da barra de atalhos: na mira, o lembrete e o Voltar precisam ficar à vista.
    const barra = document.getElementById("barra-luta");
    const limite = barra && barra.offsetParent ? barra.getBoundingClientRect().top - 6 : innerHeight - 6;
    caixa.style.top = Math.max(6, Math.min(limite - caixa.offsetHeight, r.top)) + "px";
  }
  function esconderFicha() { Telas.esconderDica(); }

  function atualizarCarta(el, c, heroi) {
    el._ficha = c;
    const classes = ["carta", c.lado];
    if (c.uid === "j") classes.push("heroi");
    if (c.chefe) classes.push("chefe");
    if (c.unico) classes.push("unico");
    if (!c.vivo) classes.push("morta");
    const fams = new Set(c.efeitos.map((f) => efeito(f.id)[1]));
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
      // Arqueiro: as flechas ficam à vista na própria carta, e piscam quando estão acabando.
      const fl = el.querySelector(".carta-flechas");
      if (fl) {
        const tem = heroi.flechas !== null && heroi.flechas !== undefined;
        fl.hidden = !tem;
        if (tem) {
          const txt = `${Math.max(0, heroi.flechas)}`;  // zerada fica vermelha; a explicação vai na dica
          if (fl.dataset.v !== txt) { fl.dataset.v = txt; fl.innerHTML = `${S("flecha", 1)}<b>${txt}</b>`; }
          fl.classList.toggle("poucas", heroi.flechas <= 8);
          fl.classList.toggle("zerada", heroi.flechas <= 0);
          fl.title = `Flechas: ${heroi.flechas} (a aljava leva ${heroi.max_flechas || 30}). Sem flechas, o ataque vira um golpe de adaga fraco e as habilidades de tiro ficam bloqueadas.`;
        }
      }
    } else el.title = c.nome;
    const ef = el.querySelector(".carta-efeitos");
    const html = c.vivo ? efeitosHtml(c.efeitos) : "";
    if (ef.innerHTML !== html) ef.innerHTML = html;
    el.querySelector(".preparando").hidden = !(c.preparando && c.vivo);
  }

  /** Desenha (ou atualiza no lugar) as cartas a partir do estado do combate. */
  function desenhar(cb, heroi, replay) {
    if (!cb) {
      esconderFicha();  // a carta sob o mouse some com a arena; a ficha não pode ficar presa
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
      const naTela = el ? el._hp : undefined;  // antes de atualizarCarta, que põe a vida nova na barra
      const nova = !el;
      if (nova) { el = criarCarta(c); cartas.set(c.uid, el); }
      atualizarCarta(el, c, heroi);
      const col = c.lado === "aliado" ? colAliados : colInimigos;
      if (el.parentElement !== col) { col.appendChild(el); if (!replay && ant === undefined && anteriores.__iniciado) entrar(el, c.lado); }
      if (!ant || replay) continue;
      const fresco = recentes[c.uid] && agora() - recentes[c.uid] < 1500;
      if (ant.vivo && !c.vivo) { morrer(el); morte = true; continue; }
      if (!ant.vivo && c.vivo) el.classList.remove("morta", "morrendo");
      const mostrava = naTela ?? ant.hp;
      if (c.hp < mostrava) { tremer(el); numero(el, `−${mostrava - c.hp}`, "menos"); golpe = true; }
      if (c.hp > mostrava && c.max_hp === ant.max_hp) { brilho(el, "cura"); numero(el, `+${c.hp - mostrava}`, "cura"); }
      const tinha = new Set(ant.efeitos.map((f) => f.id));
      c.efeitos.filter((f) => !tinha.has(f.id)).forEach((f) => {
        const fam = efeito(f.id)[1];
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
    if (el._x || el._y) await ir(el, 0, 0, pausa(160));  // quem já voltou depois do golpe não espera de novo
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
    Sensacao.depois(ms, () => el.classList.remove(classe));
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
    n.addEventListener("animationend", () => n.remove());  // o do golpe final dura mais
    Sensacao.depois(4000, () => n.remove());
  }
  function rotulo(el, texto, classe = "") {
    if (!texto || rapido()) return;
    const velho = el.querySelector(".faixa-acao");
    if (velho) velho.remove();
    const f = document.createElement("div");
    f.className = "faixa-acao " + classe;
    f.textContent = texto;
    el.appendChild(f);
    Sensacao.depois(1500, () => f.remove());
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
      Sensacao.depois(1300, () => p.remove());
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
      Sensacao.depois(1100, () => f.remove());
    }
  }
  function morrer(el) { reiniciar(el, "morrendo", 900); }

  /* ------------------------------------------------------------ lances do motor */
  const carta = (uid) => (uid ? cartas.get(uid) : null);
  function marcar(...uids) { uids.forEach((u) => { if (u) recentes[u] = agora(); }); }

  /* Quem está em cena fica por cima: quando o herói manda outro agir (Ordem da Fera, poção na comitiva), a carta
     dele continua grande, mas a do urso que ruge (e a faixa "Provocando") passa à frente por um instante. */
  let camadaCena = 10;
  function emCena(el) {
    if (!el) return;
    el.style.zIndex = String(++camadaCena);
    clearTimeout(el._cena);
    el._cena = setTimeout(() => { el.style.zIndex = ""; }, 1700);
  }

  async function lance(m) {
    if (!arena) return;
    const de = carta(m.de), em = carta(m.em);
    if (["buff", "cura", "recurso", "golpe", "erro"].includes(m.tipo)) { emCena(de); emCena(em); }
    switch (m.tipo) {
      case "acao": {
        if (!de) return;
        emArea = !!m.area;
        rotulo(de, m.nome, de.classList.contains("inimigo") ? "inimiga" : "");
        await passoFrente(de, m.area);
        if (m.hab === "grito_guerra") {
          // O grito vem antes de tudo: a arena treme e o herói brilha; só então os inimigos se encolhem.
          som("rugido");
          Sensacao.tremor(arena, Sensacao.AJUSTES.tremor.leve, 420);
          brilho(de, "forca");
          rotulo(de, "AAARGH!", "boa");
          await dormir(pausa(520));
        }
        return;
      }
      case "buff": {
        if (!em) return;
        marcar(m.em);
        const fams = [...new Set((m.efeitos || []).map((id) => (ESTADOS[id] ? ESTADOS[id].familia : "protecao")))];
        fams.forEach((f, i) => setTimeout(() => brilho(em, f), i * 160));
        if (m.hab !== "grito_guerra") rotulo(em, m.rotulo);
        som(m.hab === "erguer_escudo" ? "falange" : fams.includes("sombra") ? "sombra" : fams.includes("forca") ? "feitico" : "protecao");
        if (m.hab === "erguer_escudo") Sensacao.tremor(arena, Sensacao.AJUSTES.tremor.leve, 300);  // o baque dos escudos no chão
        if (m.hab === "provocar") { som("rugido"); Sensacao.tremor(arena, Sensacao.AJUSTES.tremor.leve, 360); }  // o urso ruge e todos olham para ele
        await dormir(pausa(560 + 160 * Math.max(0, fams.length - 1)));
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
      case "salva": return salva(m);
      case "roubo_ouro": {
        // moedas saem da sua carta e voam para a do ladrão, que ri
        if (de && em && !rapido()) {
          await investir(de, em);
          som("risada");
          for (let i = 0; i < Math.min(6, 2 + Math.floor(m.valor / 6)); i++) {
            projetil(em, de, "moeda");
            await dormir(70);
          }
          ir(de, 0, 0, pausa(170));
        }
        if (em) numero(em, `−${m.valor} ouro`, "roubo");
        if (de) { rotulo(de, "Hehehe!", "inimiga"); reiniciar(de, "gargalha", 900); }
        await dormir(pausa(500));
        return;
      }
      case "fuga": {
        if (!de) return;
        som("esquiva");
        de.classList.add("fugindo");
        await ir(de, 160, 0, pausa(420), "ease-in");
        return;
      }
      case "giro": {
        if (!de) return;
        reiniciar(de, "giro", 320);
        som("esquiva");
        await dormir(pausa(180));
        return;
      }
      case "erro": {
        marcar(m.em);
        if (de && em) { if (aDistancia(m, de) || emArea) await projetil(de, em, "flecha"); else await investir(de, em); }
        if (em) {
          if (m.motivo === "esquiva") reiniciar(em, "esquivou", 560);
          numero(em, m.motivo === "imune" ? "imune" : "esquiva", "info");
        }
        som("esquiva");
        if (de && !emArea) ir(de, 0, 0, pausa(170));
        await dormir(pausa(260));
        return;
      }
      case "cura": {
        marcar(m.em);
        if (m.modo === "roubo") return roubo(m, em, carta(m.fonte));
        if (de && de !== em) { brilho(de, "cura"); await dormir(pausa(160)); }
        if (em) {
          barra(em, m.hp, m.max_hp);
          brilho(em, "cura");
          numero(em, `+${m.valor}`, "cura");
          if (m.rotulo && !de) rotulo(em, m.rotulo);
        }
        som("cura");
        await dormir(pausa(420));
        return;
      }
      case "recurso": {
        // Mana (ou vigor/foco) voltando: a barra de recurso da carta enche, brilha e sobe "+N".
        if (!em) return;
        marcar(m.em);
        const fam = { Vigor: "vigor", Foco: "foco" }[m.recurso] || "mana";
        const r = em.querySelector(".carta-rec");
        if (r) {
          r.querySelector(".enchimento").style.width = pct(m.rec, m.max_rec) + "%";
          r.querySelector(".num").textContent = `${m.rec}/${m.max_rec}`;
          reiniciar(r, "enchendo", 900);
        }
        numero(em, `+${m.valor} ${m.recurso ? m.recurso.toLowerCase() : "mana"}`, fam + (m.discreto ? " pequeno" : ""));
        if (m.discreto) return;  // o pouco que o ataque básico devolve: número e barra, sem pausa
        reiniciar(em, "aura-" + fam, 900);
        particulas(em, fam, 14);
        if (m.rotulo) rotulo(em, m.rotulo);
        som("mana");
        await dormir(pausa(480));
        return;
      }
      case "tique": {
        if (!em) return;
        marcar(m.em);
        barra(em, m.hp, m.max_hp);
        const fam = ESTADOS[m.efeito] ? ESTADOS[m.efeito].familia : "sangue";
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
        const fam = ESTADOS[m.efeito] ? ESTADOS[m.efeito].familia : "maldicao";
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
      case "efeito_negado": {  // firme: acabou de se soltar e não perde o turno de novo
        if (!em) return;
        marcar(m.em);
        brilho(em, "protecao");
        numero(em, m.rotulo || "firme", "info");
        await dormir(pausa(300));
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

  function impacto(m, em) {
    const el = m.elemento || "fisico";
    barra(em, m.hp, m.max_hp);
    if (m.em === "j") Sensacao.vidaDoHeroi(m.hp, m.max_hp);  // no instante do golpe, não quando o estado chegar
    clarao(em, el);
    tremer(em, m.crit);
    if (el === "fogo") labaredas(em);
    else if (el !== "fisico") particulas(em, el, 8);
    // O número cresce com o peso do golpe: crítico, o que derruba, e o que encerra a luta.
    const peso = (m.abate ? " abate" : "") + (m.final ? " final" : "");
    if (m.crit) numero(em, `${m.dano}!`, "crit" + peso);
    else numero(em, `−${m.dano}`, "menos" + peso);
    if (m.crit && m.crit_motivo) numero(em, m.crit_motivo, "motivo");  // crítico garantido: de onde ele veio
    else if (m.bonus_motivo) numero(em, m.bonus_motivo, "motivo");  // golpe reforçado (iniciativa): de onde veio
    if (m.absorvido) numero(em, `(${m.absorvido})`, "escudo");
    if (m.eficacia === "super") rotulo(em, "fraqueza!", "boa");
    else if (m.eficacia === "pouco") rotulo(em, "resiste", "ruim");
  }

  /** Roubo de vida: gotas de sangue saem de quem apanhou e correm até quem bateu; só então a vida sobe.
      É o momento de a build "sentir" que funciona, então tem caminho, brilho, número e o nome da fonte. */
  async function roubo(m, em, fonte) {
    if (!em) return;
    if (fonte && fonte !== em && !rapido()) {
      const ra = arena.getBoundingClientRect(), a = fonte.getBoundingClientRect(), b = em.getBoundingClientRect();
      const x0 = a.left + a.width / 2 - ra.left, y0 = a.top + a.height * 0.4 - ra.top;
      const x1 = b.left + b.width / 2 - ra.left, y1 = b.top + b.height * 0.45 - ra.top;
      const n = Math.min(8, 4 + Math.floor(m.valor / 4));
      som("roubo");
      const voos = [];
      for (let i = 0; i < n; i++) {
        const g = document.createElement("i");
        g.className = "gota-roubo";
        camadaFx.appendChild(g);
        const arco = -30 - Math.random() * 40, dx = (Math.random() - 0.5) * 30;
        voos.push(g.animate([
          { transform: `translate(${x0 + dx}px, ${y0}px) scale(.6)`, opacity: 0 },
          { transform: `translate(${(x0 + x1) / 2 + dx}px, ${(y0 + y1) / 2 + arco}px) scale(1.15)`, opacity: 1, offset: 0.45 },
          { transform: `translate(${x1}px, ${y1}px) scale(.5)`, opacity: 0.9 },
        ], { duration: pausa(420), delay: i * 45, easing: "cubic-bezier(.4,0,.6,1)", fill: "backwards" }).finished
          .catch(() => {}).then(() => g.remove()));
      }
      await Promise.all(voos);
    } else som("roubo");
    barra(em, m.hp, m.max_hp);
    brilho(em, "roubo");
    numero(em, `+${m.valor} ♥`, "roubo");
    if (m.rotulo) numero(em, m.rotulo, "motivo roubo-fonte");
    await dormir(pausa(360));
  }

  /** Vários roubos seguidos (Redemoinho, chuva) viram um só: um caminho de sangue e o total, sem fila lenta. */
  function juntarRoubos(lances) {
    const fora = [], somas = new Map();
    lances.forEach((x) => {
      if (x.tipo === "cura" && x.modo === "roubo") {
        const s = somas.get(x.em);
        if (s) { s.valor += x.valor; s.hp = x.hp; s.max_hp = x.max_hp; return; }
        const novo = { ...x };
        somas.set(x.em, novo); fora.push(novo);
        return;
      }
      fora.push(x);
    });
    return fora;
  }

  /** Um projétil que cai do alto sobre a carta (chuva de flechas, luz do julgamento). `erra`: quem se esquivou
   *  saiu do lugar, e o projétil crava no chão ao lado da carta. */
  async function queda(para, sprite, atraso, erra = false) {
    if (rapido()) return;
    await dormir(atraso);
    const ra = arena.getBoundingClientRect(), b = para.getBoundingClientRect();
    const x1 = erra ? b.left + b.width * (0.55 + Math.random() * 0.4) - ra.left - 16
      : b.left + b.width * (0.2 + Math.random() * 0.6) - ra.left - 16;
    const y1 = erra ? b.bottom - ra.top - 22 + Math.random() * 8 : b.top + b.height / 2 - ra.top - 16;
    const x0 = x1 - 50 - Math.random() * 30, y0 = -30;
    const ang = sprite === "flecha" ? Math.atan2(y1 - y0, x1 - x0) * 180 / Math.PI + 45 : 0;
    const p = document.createElement("div");
    p.className = "projetil" + (sprite === "flecha" ? "" : " brilhante");
    p.innerHTML = S(sprite, 2);
    camadaFx.appendChild(p);
    await p.animate([{ transform: `translate(${x0}px, ${y0}px) rotate(${ang}deg)`, opacity: 0.4 },
      { transform: `translate(${x1}px, ${y1}px) rotate(${ang}deg)`, opacity: 1 }],
      { duration: pausa(420), easing: "cubic-bezier(.45,0,.9,.6)" }).finished.catch(() => {});
    p.remove();
  }

  /** Golpes em área: tudo voa e acerta ao mesmo tempo; depois o resto (efeitos, curas) segue em ordem. */
  /** Um corte em pixel atravessando a carta (o Redemoinho deixa vários, em ângulos diferentes). */
  function corte(el, angulo) {
    if (rapido()) return;
    const c = document.createElement("i");
    c.className = "corte";
    c.style.rotate = angulo + "deg";
    c.style.top = 30 + Math.random() * 40 + "%";
    el.appendChild(c);
    Sensacao.depois(420, () => c.remove());
  }

  async function redemoinho(m) {
    // Rodadas separadas pelos marcadores "giro": cada uma corta todos os alvos ao mesmo tempo, bem rápido.
    const rodadas = [];
    m.lances.forEach((x) => {
      if (x.tipo === "giro") rodadas.push([]);
      else if (rodadas.length && (x.tipo === "golpe" || x.tipo === "erro")) rodadas[rodadas.length - 1].push(x);
    });
    const resto = juntarRoubos(m.lances.filter((x) => !["giro", "golpe", "erro"].includes(x.tipo)));
    const de = carta((m.lances.find((x) => x.de) || {}).de);
    if (de) { reiniciar(de, "aura-forca", 700); clarao(de, "fisico"); }
    som("esquiva");
    await dormir(pausa(160));
    const soma = {};  // o número sobe uma vez só por inimigo, com o total dos giros
    for (let r = 0; r < rodadas.length; r++) {
      rodadas[r].forEach((x) => {
        const em = carta(x.em);
        if (!em) return;
        marcar(x.em);
        corte(em, (r % 2 ? -1 : 1) * (12 + Math.random() * 18));
        if (x.tipo === "golpe") {
          barra(em, x.hp, x.max_hp); clarao(em, "fisico"); tremer(em, x.crit);
          const s = soma[x.em] || (soma[x.em] = { dano: 0, crit: false, em });
          s.dano += x.dano; s.crit = s.crit || x.crit;
        }
      });
      som(r === rodadas.length - 1 ? "golpe" : "golpe_leve");
      if (rodadas[r].some((x) => x.crit)) som("critico_golpe");
      await dormir(pausa(150));
    }
    Object.values(soma).forEach((s) => numero(s.em, s.crit ? `${s.dano}!` : `−${s.dano}`, s.crit ? "crit" : "menos"));
    await pesoDaSalva(rodadas.flat());
    await dormir(pausa(420));
    for (const x of resto) await lance(x);
  }

  /** Tiro Duplo: as duas flechas saem quase juntas (a segunda logo atrás da primeira), dois impactos seguidos. */
  async function rajada(m) {
    const tiros = m.lances.filter((x) => x.tipo === "golpe" || x.tipo === "erro");
    const resto = juntarRoubos(m.lances.filter((x) => !tiros.includes(x)));
    await Promise.all(tiros.map(async (x, k) => {
      await dormir(k * pausa(230));  // a segunda sai quando a primeira está chegando: dois acertos, um atrás do outro
      som("disparo");
      const de = carta(x.de), em = carta(x.em);
      if (de && em) await projetil(de, em, "flecha");
      if (!em) return;
      marcar(x.em);
      if (x.tipo === "golpe") { impacto(x, em); som(x.crit ? "critico_golpe" : "golpe"); }
      else { reiniciar(em, "esquivou", 560); numero(em, "esquiva", "info"); som("esquiva"); }
    }));
    await pesoDaSalva(tiros);
    await dormir(pausa(tiros.some((x) => x.crit) ? 460 : 360));
    for (const x of resto) await lance(x);
  }

  /** Vários golpes de uma vez: o mais pesado (o que encerra a luta, o que derruba, o crítico) dá o tom. */
  async function pesoDaSalva(golpes) {
    const pior = Sensacao.maisPesado(golpes.filter((x) => x.tipo === "golpe"));
    if (pior) await Sensacao.golpe(pior, arena, carta(pior.em));
  }

  async function salva(m) {
    if (m.hab === "redemoinho") return redemoinho(m);
    if (m.hab === "tiro_duplo") return rajada(m);
    const golpes = m.lances.filter((x) => x.tipo === "golpe" || x.tipo === "erro");
    const resto = juntarRoubos(m.lances.filter((x) => !golpes.includes(x)));
    if (!golpes.length) { for (const x of resto) await lance(x); return; }
    const de = carta(golpes[0].de);
    const el = golpes.find((x) => x.elemento)?.elemento || "fisico";
    const distancia = golpes.some((x) => x.alcance === "distancia");
    const alvosEl = [...new Set(golpes.map((x) => x.em))].map(carta).filter(Boolean);
    // Quem se esquiva sai do lugar enquanto a salva cai (o projétil crava no chão ao lado), não depois dela.
    const esquivas = new Set(golpes.filter((x) => x.tipo === "erro" && x.motivo === "esquiva").map((x) => carta(x.em)));
    const desviar = (ms) => esquivas.forEach((a) => a && setTimeout(() => reiniciar(a, "esquivou", 560), ms));
    // 1) a salva no ar
    if (el === "fisico" && distancia) {
      som("disparo");
      await dormir(pausa(180));  // a saraivada sobe antes de cair
      desviar(pausa(200));
      await Promise.all(alvosEl.flatMap((a) => [0, 1, 2].map((k) => queda(a, "flecha", k * 110 + Math.random() * 60, esquivas.has(a)))));
    } else if (el === "fisico") {
      if (de) reiniciar(de, "giro", 300);
      await dormir(pausa(160));
    } else if (["sagrado", "sombra", "arcano", "gelo", "veneno"].includes(el)) {
      som("lancar");
      desviar(pausa(150));
      await Promise.all(alvosEl.map((a, k) => queda(a, PROJETIL[el] || "orbe_arcano", k * 40, esquivas.has(a))));
    } else {
      // fogo (Inferno): o chão se abre sob todos de uma vez
      som("lancar");
      alvosEl.forEach((a) => { brilho(a, "fogo"); labaredas(a); });
      await dormir(pausa(240));
    }
    // 2) todos os impactos juntos
    golpes.forEach((x) => {
      const em = carta(x.em);
      if (!em) return;
      marcar(x.em);
      if (x.tipo === "golpe") impacto(x, em);
      else {
        if (x.motivo === "esquiva" && !em.classList.contains("esquivou")) reiniciar(em, "esquivou", 560);
        numero(em, x.motivo === "imune" ? "imune" : "esquiva", "info");
      }
    });
    if (esquivas.size) som("esquiva");
    const critou = golpes.some((x) => x.crit);
    som(critou ? "critico_golpe" : SOM_ELEMENTO[el] || "golpe");
    setTimeout(() => som("golpe_leve"), 70);
    await pesoDaSalva(golpes);
    if (golpes.some((x) => x.em === "j" && x.tipo === "golpe")) { App.doer(); som("dor"); }
    await dormir(pausa(critou ? 520 : 420));
    // 3) o que veio depois (queimaduras, curas...) em sequência
    for (const x of resto) await lance(x);
  }

  /** O golpe vem de longe (projétil) ou de perto (a carta avança)? O falcão conta como "à distância" na regra
   *  (voa: bom contra voadores), mas na tela ele dá um rasante até o alvo. */
  function aDistancia(m, de) { return m.alcance === "distancia" && !(de && de.dataset.tipo === "falcao"); }
  async function golpe(m, de, em) {
    if (!em) return;
    marcar(m.em);
    const el = m.elemento || "fisico";
    const distancia = aDistancia(m, de);
    await Sensacao.antesDoGolpe(m, arena, em);  // o golpe que encerra a luta já chega em câmera lenta
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
    if (m.refletido) return espinhos(m, em);
    impacto(m, em);
    som(m.crit ? "critico_golpe" : SOM_ELEMENTO[el] || "golpe");
    if (el !== "fisico" && !m.crit) setTimeout(() => som("golpe_leve"), 60);
    if (m.em === "j") { App.doer(); som("dor"); }
    await Sensacao.golpe(m, arena, em);
    // Golpeou: volta direto para o lugar (não para o "passo à frente"). Roubo de vida, sangramento e passivas
    // que vêm depois já aparecem com a carta em casa; um contra-ataque, fora da própria vez, também não fica adiantado.
    if (de && de !== em && !de.classList.contains("girando") && !emArea) ir(de, 0, 0, pausa(distancia ? 140 : 190));
    await dormir(pausa(de && de.classList.contains("girando") ? 110 : m.crit ? 460 : 380));
  }

  /** Dano devolvido pelos espinhos da armadura: o agressor só sente (sem farpas voando), e "Espinhos" sobe nele. */
  async function espinhos(m, em) {
    await dormir(pausa(90));
    barra(em, m.hp, m.max_hp);
    tremer(em, false);
    numero(em, `−${m.dano}`, "espinhos");
    rotulo(em, "Espinhos", "espinhos");
    som("golpe_leve");
    await dormir(pausa(320));
  }

  /* ------------------------------------------------------------ vez e alvos */
  // A pessoa está escolhendo (a ação, ou o alvo dela)? Só aí a ficha do inimigo abre ao passar o mouse: enquanto os
  // golpes animam, as cartas passam voando por baixo do mouse parado perto da sua, e a ficha pulava na frente.
  let escolhendo = false;
  function podeEscolher(sim) {
    escolhendo = sim;
    if (!sim) cartas.forEach((el) => { if (Telas.dicaAbertaPor(el)) esconderFicha(); });
  }
  function vez(uid) {
    cartas.forEach((el, u) => el.classList.toggle("vez", u === uid));
    podeEscolher(uid === "j");
  }
  /** A carta de quem escolhe a ação vem para a frente e cresce. */
  function foco(uid) {
    cartas.forEach((el, u) => el.classList.toggle("foco", u === uid));
  }
  function elCarta(uid) { return cartas.get(uid) || null; }
  function alvos(opcoes, escolher) {
    limparAlvos();
    podeEscolher(true);
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
  // Na luta, a fala sai num balão da carta de quem falou. Fora dela, cada reação vira um cartão
  // que surge no canto de baixo da página (onde você está lendo), fica um pouco e some.
  function separarFala(texto, nome) {
    const falas = [];
    let acao = texto.replace(/["“]([^"”]+)["”]/g, (_, f) => { falas.push(f.trim()); return " "; });
    acao = acao.replace(/\s+/g, " ").replace(/\s+([,.!?;:])/g, "$1").replace(/^[\s,.;:—–-]+|[\s,;:—–-]+$/g, "").trim();
    if (/^(diz|sussurra|murmura|responde|resmunga|completa|acrescenta|fala)\b/i.test(acao) && acao.length < 50) acao = "";
    const curto = String(nome || "").split(" ").pop();
    if (curto && acao.startsWith(curto + " ")) acao = acao.slice(curto.length + 1);
    acao = acao.replace(/\.$/, "");
    return { acao, fala: falas.join(" … ") };
  }
  function pilha() {
    let p = document.getElementById("comitiva-avisos");
    if (!p) { p = document.createElement("div"); p.id = "comitiva-avisos"; document.body.appendChild(p); }
    // Fica logo acima do trecho mais recente: cobre o que você já leu, nunca a linha nova.
    const r = document.getElementById("pagina").getBoundingClientRect();
    const ultimo = document.querySelector("#texto > :last-child");
    let base = ultimo ? ultimo.getBoundingClientRect().top - 10 : r.bottom - 22;
    if (base < r.top + 140) base = Math.min(r.bottom - 12, (ultimo ? ultimo.getBoundingClientRect().bottom : r.bottom) + 10 + 140);
    base = Math.max(r.top + 140, Math.min(r.bottom - 12, innerHeight - 12, base));
    p.style.right = Math.max(8, innerWidth - r.right + 22) + "px";
    p.style.bottom = Math.max(10, innerHeight - base) + "px";
    return p;
  }
  const cartoesAbertos = {};
  function cartao(cid, nome, { delta, texto }) {
    let c = cartoesAbertos[cid];
    if (!c || !c.isConnected) {
      c = document.createElement("div");
      c.className = "cartao-comitiva";
      c.innerHTML = `<div class="cc-retrato">${S(cid, 3)}</div><div class="cc-corpo"><div class="cc-topo"><b>${esc(nome)}</b></div></div>`;
      c.addEventListener("click", () => fechar(c));
      pilha().appendChild(c);
      cartoesAbertos[cid] = c;
      c.classList.add("chegou");
    } else {
      c.classList.remove("atualizou"); void c.offsetWidth; c.classList.add("atualizou");
    }
    const corpo = c.querySelector(".cc-corpo");
    if (delta) {
      const bom = delta > 0, forte = Math.abs(delta) >= 8;
      const velho = c.querySelector(".cc-selo");
      if (velho) velho.remove();
      c.querySelector(".cc-topo").insertAdjacentHTML("beforeend",
        `<span class="cc-selo ${bom ? "aprova" : "desaprova"}${forte ? " forte" : ""}">${bom ? "▲ aprova" : "▼ desaprova"}${forte ? " muito" : ""}</span>`);
      c.classList.toggle("aprova", bom); c.classList.toggle("desaprova", !bom);
    }
    if (texto) {
      const { acao, fala } = separarFala(texto, nome);
      corpo.querySelectorAll(".cc-acao, .cc-fala").forEach((x) => x.remove());
      if (acao) corpo.insertAdjacentHTML("beforeend", `<div class="cc-acao">${esc(acao)}</div>`);
      if (fala) corpo.insertAdjacentHTML("beforeend", `<div class="cc-fala">${esc(fala)}</div>`);
    }
    const letras = (c.textContent || "").length;
    clearTimeout(c._timer);
    c._timer = setTimeout(() => fechar(c), Math.min(6500, 1700 + letras * 30));
    return c;
  }
  function fechar(c) {
    clearTimeout(c._timer);
    c.classList.add("sumindo");
    setTimeout(() => c.remove(), 260);
  }

  function balao(cid, nome, texto) {
    const naLuta = document.querySelector(`#arena .carta[data-cid="${cid}"]`);
    som("fala");
    if (!naLuta || naLuta.offsetParent === null) {
      cartao(cid, nome, { texto });
      return Math.min(1600, 500 + texto.length * 18);
    }
    if (baloes[cid]) baloes[cid].remove();
    const { acao, fala } = separarFala(texto, nome);
    const b = document.createElement("div");
    b.className = "balao" + (fala ? "" : " narrado");
    b.innerHTML = `<b>${esc(nome)}</b>${fala ? `<span>${esc(fala)}</span>` : ""}${acao ? `<i>${esc(acao)}</i>` : ""}`;
    document.body.appendChild(b);
    posicionarBalao(b, naLuta);
    baloes[cid] = b;
    setTimeout(() => { b.classList.add("sumindo"); setTimeout(() => b.remove(), 300); }, Math.min(8000, 2600 + texto.length * 45));
    return Math.min(1600, 500 + texto.length * 18);
  }
  const baloes = {};
  /** Onde o balão cabe sem cobrir ninguém. Como os quadros de tooltip dos jogos: tenta os lugares em ordem
   *  (ao lado de quem fala, virado para o meio do palco; depois acima; depois abaixo) e fica com o primeiro
   *  que não encobre outra carta, as ações da roda ou outro balão. Se todos encobrem, o que encobre menos. */
  function posicionarBalao(b, quem) {
    const r = quem.getBoundingClientRect(), w = b.offsetWidth, h = b.offsetHeight, folga = 12;
    const obstaculos = [...document.querySelectorAll("#arena .carta, #roda > *, .balao")]
      .filter((o) => o !== quem && o !== b && o.offsetParent !== null).map((o) => o.getBoundingClientRect());
    const arena = (document.getElementById("arena") || document.body).getBoundingClientRect();
    const meio = arena.left + arena.width / 2;
    const paraDireita = r.left + r.width / 2 < meio;  // aliados à esquerda falam para a direita, e vice-versa
    const ladoX = paraDireita ? r.right + folga : r.left - folga - w;
    const cy = r.top + r.height / 2;
    const candidatos = [
      { x: ladoX, y: cy - h / 2, tipo: "lado" },
      { x: ladoX, y: r.top, tipo: "lado" },
      { x: ladoX, y: r.bottom - h, tipo: "lado" },
      { x: r.left + r.width / 2 - w / 2, y: r.top - h - folga, tipo: "acima" },
      { x: r.left + r.width / 2 - w / 2, y: r.bottom + folga, tipo: "abaixo" },
    ].map((c) => {
      c.x = Math.max(8, Math.min(innerWidth - w - 8, c.x));
      c.y = Math.max(52, Math.min(innerHeight - h - 8, c.y));
      c.cobre = obstaculos.reduce((s, o) => s + Math.max(0, Math.min(c.x + w, o.right) - Math.max(c.x, o.left))
        * Math.max(0, Math.min(c.y + h, o.bottom) - Math.max(c.y, o.top)), 0)
        + Math.max(0, Math.min(c.x + w, r.right) - Math.max(c.x, r.left)) * Math.max(0, Math.min(c.y + h, r.bottom) - Math.max(c.y, r.top));
      return c;
    });
    const c = candidatos.find((k) => !k.cobre) || candidatos.reduce((a, k) => (k.cobre < a.cobre ? k : a));
    b.style.left = c.x + "px"; b.style.top = c.y + "px";
    if (c.tipo === "lado") {
      b.classList.add("lado", paraDireita ? "a-direita" : "a-esquerda");
      b.style.setProperty("--rabo-y", Math.max(12, Math.min(h - 12, cy - c.y)) + "px");
    } else {
      if (c.tipo === "abaixo") b.classList.add("abaixo");
      b.style.setProperty("--rabo", Math.max(14, Math.min(w - 14, r.left + r.width / 2 - c.x)) + "px");
    }
  }
  /** A roda de ações acabou de aparecer: um balão que caiu por cima dela (a fala veio antes da sua vez) muda de
   *  lugar; se não houver lugar livre, some. A vez é sua, e as suas ações não ficam atrás de ninguém. */
  function abrirCaminho() {
    const acoes = [...document.querySelectorAll("#roda > *, .roda-janela")].filter((o) => o.offsetParent !== null)
      .map((o) => o.getBoundingClientRect());
    const cobre = (b) => { const r = b.getBoundingClientRect(); return acoes.some((o) => r.left < o.right && o.left < r.right && r.top < o.bottom && o.top < r.bottom); };
    for (const [cid, b] of Object.entries(baloes)) {
      if (!b.isConnected || !cobre(b)) continue;
      const quem = document.querySelector(`#arena .carta[data-cid="${cid}"]`);
      if (quem) { b.classList.remove("lado", "a-direita", "a-esquerda", "abaixo"); posicionarBalao(b, quem); }
      if (cobre(b)) { b.classList.add("sumindo"); setTimeout(() => b.remove(), 300); }
    }
  }
  function opiniao(cid, nome, delta) {
    som(delta > 0 ? "aprova" : "desaprova");
    cartao(cid, nome, { delta });
    const carta = document.querySelector(`#arena .carta[data-cid="${cid}"]`);
    if (carta) reiniciar(carta, delta > 0 ? "reagiu-bem" : "reagiu-mal", 900);
  }

  return { configurar, catalogo, desenhar, lance, vez, foco, elCarta, alvos, limparAlvos, mirar, balao, opiniao, abrirCaminho };
})();
