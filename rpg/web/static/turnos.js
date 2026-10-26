/* A iniciativa e a passagem dos turnos na luta (1.116.0; o caminho em ferramentas/prototipos/hud/turnos/). Só mostra o
   que o motor diz, sem deduzir nada de quantas mensagens ou animações passaram:
   - a mensagem "turno" (ui.novo_turno: uma vez por volta do laço da luta, no começo da sua vez; a comitiva, o animal,
     os servos e os inimigos agem dentro da volta e não a geram): o anúncio "Turno N" (Turnos.aoTurno);
   - estado.combate.turno: a placa com o turno de agora, para consulta (vale também ao recarregar a página no meio da luta);
   - o lance "surpresa": de "j" é a sua iniciativa; de um inimigo, a emboscada deles (o golpe livre do mais ágil, antes do
     turno 1) (Turnos.aoLance);
   - o estado "iniciativa" na sua carta, com o texto do motor ("+25% de dano no primeiro golpe deste turno"): enquanto
     existe, a linha da iniciativa na placa; o golpe com bonus_motivo "Iniciativa!" (combate/golpe.py a consome) a marca
     como usada; se o estado some sem esse golpe (o turno livre gasto noutra coisa), ela passou;
   - um estado seu que tira o turno (o catálogo do motor: perde_turno, como atordoado ou preso na teia), no começo do
     turno: o anúncio diz que você perde este turno, para não parecer a sua vez de agir.
   O anúncio é uma faixa de pincel (as pontas do seletor e dos comandos) que entra e sai em ~1,1 s; a placa, uma faixa
   pequena na borda da arena (no pé da faixa dos comandos; na luta pequena, presa à borda de baixo dela). O anúncio fica
   num lugar só (1.116.1): no centro da área de combate, na borda de cima, logo acima das cartas e dos comandos, numa
   linha; nunca cobre comando, carta, a placa ou o registro. Os dois
   são interface: medidos pelo layout, ficam parados enquanto a arena chega perto e treme no impacto. Nada espera: a
   camada não recebe o mouse, e a fila de mensagens e a vez seguem no tempo delas. Com movimento reduzido (19-turnos.css), nada se
   desloca e o anúncio fica mais tempo. */
"use strict";

const Turnos = (() => {
  const $ = (s, r = document) => r.querySelector(s);
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const VARS = ["--sh-ponta-e1", "--sh-ponta-d2", "--sh-meio", "--sh-grao", "--sh-texto", "--sh-latao"];
  let camada = null, placa = null, anuncio = null, ultimoTurno = 0;
  let ini = { ativa: false, texto: "", usada: false, mostrandoFim: false };
  let fundoRoda = 0;  // o pé da roda de comandos (a última vez que ela esteve à vista), em px da arena
  let lugarPlaca = null;  // {chave: o tamanho da janela, nome: dentro|fora}, decidido uma vez por luta (a placa)
  let ajuste = 0;
  let perde = null;  // o estado que tira o turno de agora ("preso na teia"), para a placa: até o turno seguinte
  // A ordem fixa da luta (etapa 4): a do motor (estado.combate.ordem) e, entre um estado e outro, quem começa a agir
  // pelos lances ("acao", "pula"); o lance "rodada" recomeça a fila. Só o que o motor diz: ninguém é deduzido.
  let ordem = [];

  // A camada mora na página (fixa), acima da arena: a placa e o anúncio são interface, não fazem parte da cena. Ficam
  // parados enquanto a arena chega perto no golpe final (transform) e treme no impacto (translate): a medida é feita com
  // a arena parada e guardada (medir); enquanto ela se mexe, vale a última, e a placa não se move.
  function garantirCamada() {
    const arena = $("#arena");
    if (!arena) return null;
    if (!camada || !camada.isConnected) {
      camada = document.createElement("div");
      camada.className = "turnos-camada";
      const cs = getComputedStyle($("#roda") || arena);
      VARS.forEach((v) => { const x = cs.getPropertyValue(v); if (x) camada.style.setProperty(v, x); });  // as pontas do seletor
      document.body.appendChild(camada);
      placa = null;
    }
    return camada;
  }
  // A caixa de um elemento na janela; dx/dy: um desvio a descontar (o deslizar das cartas quando a arena se acomoda,
  // _acX/_acY de batalha.js: vale o lugar final).
  function caixa(el, dx = 0, dy = 0) {
    const q = el.getBoundingClientRect();
    return { left: q.left - dx, top: q.top - dy, right: q.right - dx, bottom: q.bottom - dy, width: q.width, height: q.height };
  }
  // a arena se mexendo: chegando perto no golpe final (foco-final, transform) ou tremendo no impacto (translate)
  function arenaMexendo() {
    const a = $("#arena");
    if (!a) return false;
    const cs = getComputedStyle(a);
    return a.classList.contains("foco-final") || (cs.transform && cs.transform !== "none") || (cs.translate && cs.translate !== "none");
  }
  let medida = null;
  function medir() {
    if (medida && arenaMexendo()) return medida;  // a última medida com a arena parada
    medida = { g: faixaComandos(), obs: obstaculos() };
    return medida;
  }
  const toca = (a, q) => a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1;
  // o que não pode ser coberto: as cartas (no lugar final), a mira, o seletor e o aviso da cena; os comandos à parte
  function obstaculos() {
    const visiveis = (s) => [...document.querySelectorAll(s)].filter((e) => e.getClientRects().length);
    return {
      firmes: [...visiveis("#batalha .carta").map((e) => caixa(e, e._acX || 0, e._acY || 0)),
        ...visiveis(".roda-mira, #arena > .mods-arena .mod").map((e) => caixa(e)),
        ...visiveis(".roda-janela").map((e) => (e.classList.contains("lateral") ? e.getBoundingClientRect() : caixa(e)))],
      comandos: visiveis("#roda .roda-botao").map((e) => caixa(e)),
    };
  }
  // a área de combate, entre a sua fileira e a dos inimigos (a faixa dos comandos: nenhuma carta entra ali), pelas
  // colunas e não pelas cartas: a sua carta cresce na sua vez (1,06×, como em batalha.js); as colunas ficam paradas.
  // A altura é a final da arena (ela cresce devagar: batalha.js, acomodar).
  function faixaComandos() {
    const arena = $("#arena"), R = caixa(arena), al = $("#batalha .aliados"), inim = $("#batalha .inimigos");
    const alto = arena._altura || R.height;
    const A = { ...R, height: alto, bottom: R.top + alto };
    const ra = al && caixa(al), ri = inim && caixa(inim);
    const esq = ra && ra.width ? ra.left + ra.width * 1.06 : A.left + A.width * 0.33;
    const dir = ri && ri.width ? ri.left : A.left + A.width * 0.66;
    const botoes = [...document.querySelectorAll("#roda .roda-botao")].map((c) => caixa(c));
    if (botoes.length) fundoRoda = Math.max(...botoes.map((r) => r.bottom)) - A.top;
    return { A, esq, dir, meio: (esq + dir) / 2, larg: dir - esq, fundoRoda: A.top + (fundoRoda || A.height * 0.3), rodaMedida: !!fundoRoda };
  }
  function faixa(classe, html) {
    const f = document.createElement("div");
    f.className = `turnos-faixa ${classe}`;
    f.innerHTML = html;
    return f;
  }
  // a placa: no pé da faixa dos comandos, dentro da arena; sem lugar ali (a luta pequena), presa à borda de baixo dela.
  // O lugar é decidido uma vez por luta e tamanho de janela, com a roda já medida (ela some na vez dos inimigos).
  function posicionarPlaca(g) {
    const w = placa.offsetWidth, h = placa.offsetHeight, { firmes, comandos } = medir().obs;
    const dentro = { nome: "dentro", y: g.A.bottom - h - 10 }, fora = { nome: "fora", y: g.A.bottom - 4 };
    const chave = `${innerWidth}x${innerHeight}`;
    let l = lugarPlaca && lugarPlaca.chave === chave ? (lugarPlaca.nome === "dentro" ? dentro : fora) : null;
    if (!l) {
      const q = { left: g.meio - w / 2, right: g.meio + w / 2, top: dentro.y, bottom: dentro.y + h };
      l = dentro.y >= g.fundoRoda + 8 && ![...firmes, ...comandos].some((o) => toca(q, o)) ? dentro : fora;
      if (g.rodaMedida) lugarPlaca = { chave, nome: l.nome };
    }
    placa.style.left = Math.round(g.meio - w / 2) + "px";
    placa.style.top = Math.round(Math.min(innerHeight - h - 2, l.y)) + "px";
    placa.dataset.lugar = l.nome;
  }
  // o anúncio: um lugar só, previsível, no centro da área de combate, na borda de cima: termina logo abaixo da borda da
  // arena, acima da primeira carta e do primeiro comando (que começam uns 7 px abaixo dela), e longe da placa e do
  // registro, embaixo. Entre os grupos não serve: na luta pequena a roda ocupa a faixa inteira, e qualquer altura ali
  // esconde algum comando. Medido pelo layout (o zoom e a tremida não o movem). Um por vez, numa linha (19-turnos.css).
  function posicionarAnuncio(g) {
    anuncio.style.left = Math.round(g.A.left + g.A.width / 2 - anuncio.offsetWidth / 2) + "px";
    anuncio.style.top = Math.max(2, Math.round(g.A.top + 4 - anuncio.offsetHeight)) + "px";
  }
  function anunciar(classe, titulo, linhas = []) {
    if (!garantirCamada()) return;
    if (anuncio) anuncio.remove();
    const { g } = medir();
    anuncio = faixa(`turnos-anuncio ${classe}`, `<b>${esc(titulo)}</b>${linhas.map((l) => `<small>${esc(l)}</small>`).join("")}`);
    anuncio.style.maxWidth = Math.floor(g.A.width - 16) + "px";
    camada.appendChild(anuncio);
    posicionarAnuncio(g);
    anuncio.classList.add("entrando");
    const este = anuncio;
    setTimeout(() => { if (este.isConnected) este.remove(); if (anuncio === este) anuncio = null; }, reduzido() ? 1800 : 1100);
  }
  function desenharPlaca(turno, pisca) {
    if (!garantirCamada()) return;
    if (!placa) { placa = faixa("turnos-placa", ""); camada.appendChild(placa); }
    const linhaIni = perde ? `<span class="ini perde">${esc(perde)}: perde esta vez</span>`
      : ini.ativa ? `<span class="ini">Iniciativa: ${esc(ini.curto)}</span>`
      : ini.mostrandoFim ? `<span class="ini ${ini.usada ? "usada" : "acabou"}">${ini.usada ? `Iniciativa usada (${esc(ini.pct)})` : "Iniciativa passou"}</span>` : "";
    const fila = ordem.length > 1 ? `<span class="ordem">${ordem.map((o) => `<span class="o${o.vez ? " vez" : ""}${o.passou ? " passou" : ""}${o.fora ? " fora" : ""}${o.entra ? " espera" : ""}">${esc(curto(o.nome))}</span>`).join('<i>›</i>')}</span>` : "";
    const html = `<span class="t">Rodada<b>${turno}</b></span>${fila}${linhaIni}`;
    if (placa._html !== html) { placa._html = html; placa.innerHTML = html; }
    placa.classList.toggle("pisca", !!pisca);
    if (pisca) setTimeout(() => placa && placa.classList.remove("pisca"), 650);
    if (arenaMexendo() && placa.style.top) return;  // o impacto: a placa fica onde está
    const { g } = medir();
    placa.style.visibility = g.rodaMedida ? "" : "hidden";  // o lugar depende da roda: a placa entra quando ela aparece
    posicionarPlaca(g);
  }
  function limpar() {
    if (camada) camada.remove();
    camada = placa = anuncio = medida = null;
    ultimoTurno = 0; fundoRoda = 0; lugarPlaca = null; perde = null; ordem = [];
    ini = { ativa: false, texto: "", usada: false, mostrandoFim: false };
    clearInterval(ajuste); ajuste = 0;
  }
  function iniciativaAcabou() {
    ini.ativa = false; ini.mostrandoFim = true;
    desenharPlaca(ultimoTurno || (estado && estado.combate && estado.combate.turno) || 1);
    setTimeout(() => { ini.mostrandoFim = false; if (estado && estado.combate) desenharPlaca(estado.combate.turno || ultimoTurno); }, reduzido() ? 2400 : 1600);
  }
  const maiuscula = (t) => (t ? t[0].toUpperCase() + t.slice(1) : t);
  // o nome na fila: inteiro quando é curto ("Lobo Cinzento"); senão, a primeira palavra e a letra de quem tem igual
  // ("Rato da despensa A" → "Rato A")
  const curto = (n) => {
    const t = String(n || "");
    if (t.length <= 14) return t;
    const p = t.split(/[ ,(]+/).filter(Boolean), l = p[p.length - 1];
    return p.length > 1 && /^[A-Z]$/.test(l) ? `${p[0]} ${l}` : p[0] || "";
  };
  function marcarVez(uid) {
    const i = ordem.findIndex((o) => o.uid === uid);
    if (i < 0) return false;
    ordem.forEach((o, k) => { o.vez = k === i; o.passou = k < i; });
    return true;
  }

  /** O estado: a placa acompanha o turno do motor; a iniciativa entra e sai pelo estado da sua carta. */
  function aoEstado(e) {
    if (!e || !e.combate) { if (camada || ultimoTurno) limpar(); return; }
    const ef = ((e.combate.heroi && e.combate.heroi.efeitos) || []).find((x) => x.id === "iniciativa");
    const texto = ef ? ef.texto || "" : null;
    if (texto !== null && !ini.ativa && !ini.usada) {
      const pct = (texto.match(/[+−-]\d+%/) || [""])[0];
      ini = { ativa: true, texto, pct, curto: pct ? `${pct} no 1º golpe` : texto, usada: false, mostrandoFim: false };
    } else if (texto === null && ini.ativa) {
      iniciativaAcabou();  // passou sem golpe (o golpe que a usa já a marcou: aoLance)
    }
    if (e.combate.ordem) ordem = e.combate.ordem.map((o) => ({ ...o }));
    if (e.combate.turno) { ultimoTurno = Math.max(ultimoTurno, e.combate.turno); desenharPlaca(ultimoTurno); }
    // a arena cresce devagar quando uma carta entra ou ganha efeitos (batalha.js, acomodar): a placa acompanha
    if (!ajuste) ajuste = setInterval(() => { if (placa && placa.isConnected && estado && estado.combate) desenharPlaca(ultimoTurno || estado.combate.turno); }, 400);
  }
  /** A mensagem do turno. O turno 1 com a iniciativa é um anúncio só (a iniciativa e o turno livre); um turno que você
   *  perde (um estado que tira o turno, pelo catálogo do motor) diz isso. Refazendo a página (replay), só a placa. */
  function aoTurno(n, refazendo) {
    ultimoTurno = n;
    if (!refazendo) {
      const efs = (estado && estado.combate && estado.combate.heroi && estado.combate.heroi.efeitos) || [];
      const trava = efs.find((x) => estado.estados && estado.estados[x.id] && estado.estados[x.id].perde_turno);
      perde = trava ? maiuscula(trava.nome) : null;
      if (trava) anunciar("perde", `Rodada ${n}`, [`${maiuscula(trava.nome)}: você perde esta vez`]);
      // o bônus fica na placa ("Iniciativa: +25% no 1º golpe"); o anúncio só diz que a vez é sua
      else if (n === 1 && ini.ativa) anunciar("iniciativa", "Iniciativa!", ["Rodada 1 · Só você age"]);
      else anunciar("", `Rodada ${n}`);
    }
    desenharPlaca(n, !refazendo);
  }
  /** Os lances (fora do replay): alguém começando a agir tira o anúncio (a atenção vai para o golpe; o turno segue na
   *  placa); a emboscada deles; o golpe que usa a iniciativa (também numa salva em área). */
  function aoLance(m) {
    if (m.tipo === "rodada") { ordem.forEach((o) => { o.vez = false; o.passou = false; }); if (camada) desenharPlaca(m.n || ultimoTurno); }
    if ((m.tipo === "acao" || m.tipo === "pula") && m.de && marcarVez(m.de) && camada) desenharPlaca(ultimoTurno);
    if ((m.tipo === "acao" || m.tipo === "salva") && anuncio) {
      const este = anuncio;
      anuncio = null;
      este.classList.add("saindo");
      setTimeout(() => este.remove(), 140);
    }
    if (m.tipo === "surpresa" && m.de && m.de !== "j") {
      const c = Batalha.elCarta(m.de), nome = c ? c.querySelector(".carta-nome span").textContent : "Um inimigo";
      anunciar("emboscada", "Emboscada!", [`${nome} ataca antes de você`]);
    }
    const usa = (g) => g && g.tipo === "golpe" && g.de === "j" && g.bonus_motivo === "Iniciativa!";
    if ((usa(m) || (m.tipo === "salva" && (m.lances || []).some(usa))) && ini.ativa) {
      ini.usada = true;
      iniciativaAcabou();
    }
  }
  addEventListener("resize", () => { if (placa && estado && estado.combate) desenharPlaca(ultimoTurno || estado.combate.turno); });
  return { aoEstado, aoTurno, aoLance };
})();
