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
   pequena. O lugar é medido para nunca cobrir carta, comando, mira, seletor ou o aviso da cena: dentro da faixa dos
   comandos quando ela tem vão (a luta cheia); senão, logo abaixo da arena (a luta pequena). Nada espera: a camada não
   recebe o mouse, e a fila de mensagens e a vez seguem no tempo delas. Com movimento reduzido (19-turnos.css), nada se
   desloca e o anúncio fica mais tempo. */
"use strict";

const Turnos = (() => {
  const $ = (s, r = document) => r.querySelector(s);
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const VARS = ["--sh-ponta-e1", "--sh-ponta-d2", "--sh-meio", "--sh-grao", "--sh-texto", "--sh-latao"];
  let camada = null, placa = null, anuncio = null, ultimoTurno = 0;
  let ini = { ativa: false, texto: "", usada: false, mostrandoFim: false };
  let fundoRoda = 0;  // o pé da roda de comandos (a última vez que ela esteve à vista), em px da arena
  let lugarPlaca = null;  // {chave: o tamanho da janela, nome: dentro|fora}, decidido uma vez por luta
  let ajuste = 0;

  // A camada mora na página (fixa), acima da arena e do registro: o anúncio e a placa podem ficar dentro da arena (onde
  // houver vão) ou logo abaixo dela, e passam por cima da roda de comandos sem ficar atrás dela.
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
  // o que não pode ser coberto: as cartas (no lugar final: enquanto a arena se acomoda, elas deslizam com um desvio
  // _acX/_acY de batalha.js), os comandos, a mira, o seletor e o aviso da cena
  function obstaculos() {
    return [...document.querySelectorAll("#batalha .carta, #roda .roda-botao, .roda-mira, .roda-janela, #arena > .mods-arena .mod")]
      .map((e) => {
        const q = e.getBoundingClientRect(), dx = e._acX || 0, dy = e._acY || 0;
        return { left: q.left - dx, right: q.right - dx, top: q.top - dy, bottom: q.bottom - dy, width: q.width, height: q.height };
      }).filter((q) => q.width && q.height);
  }
  const toca = (a, q) => a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1;
  // a faixa dos comandos, entre a sua fileira e a dos inimigos (nenhuma carta entra ali: batalha.js, distribuir), pelas
  // colunas e não pelas cartas: a sua carta cresce na sua vez (1,06×, como em batalha.js) e as cartas deslizam quando a
  // arena se acomoda; as colunas ficam paradas. A altura é a final da arena (ela cresce devagar: batalha.js, acomodar).
  function faixaComandos() {
    const arena = $("#arena"), R = arena.getBoundingClientRect(), al = $("#batalha .aliados"), inim = $("#batalha .inimigos");
    const alto = arena._altura || R.height;
    const A = { left: R.left, right: R.right, top: R.top, width: R.width, height: alto, bottom: R.top + alto };
    const ra = al && al.getBoundingClientRect(), ri = inim && inim.getBoundingClientRect();
    const esq = ra && ra.width ? ra.left + ra.width * 1.06 : A.left + A.width * 0.33;
    const dir = ri && ri.width ? ri.left : A.left + A.width * 0.66;
    const botoes = [...document.querySelectorAll("#roda .roda-botao")].map((c) => c.getBoundingClientRect());
    if (botoes.length) fundoRoda = Math.max(...botoes.map((r) => r.bottom)) - A.top;
    return { A, meio: (esq + dir) / 2, larg: dir - esq, fundoRoda: A.top + (fundoRoda || A.height * 0.3), rodaMedida: !!fundoRoda };
  }
  function faixa(classe, html) {
    const f = document.createElement("div");
    f.className = `turnos-faixa ${classe}`;
    f.innerHTML = html;
    return f;
  }
  // põe o elemento no primeiro lugar da lista que não cobre nada; sem nenhum livre, no último (o de fora da arena)
  function posicionar(el, lugares, fixo) {
    const w = el.offsetWidth, h = el.offsetHeight, obs = obstaculos();
    let escolhido = (fixo && lugares.find((l) => l.nome === fixo)) || lugares[lugares.length - 1];
    if (!fixo) for (const l of lugares) {
      const q = { left: l.x - w / 2, right: l.x + w / 2, top: l.y, bottom: l.y + h };
      if (l.ok !== false && q.top >= 0 && q.bottom <= innerHeight && !obs.some((o) => toca(q, o))) { escolhido = l; break; }
    }
    el.style.left = Math.round(escolhido.x - w / 2) + "px";
    el.style.top = Math.round(Math.min(innerHeight - h - 2, escolhido.y)) + "px";
    el.dataset.lugar = escolhido.nome;
  }
  // o anúncio: dentro da arena, no meio do vão embaixo da roda (só com a roda já vista nesta luta e se couber na largura
  // da faixa dos comandos, com folga); senão, logo abaixo da arena, sobre o começo do registro. Um por vez.
  function anunciar(classe, titulo, linhas = []) {
    if (!garantirCamada()) return;
    if (anuncio) anuncio.remove();
    const g = faixaComandos();
    anuncio = faixa(`turnos-anuncio ${classe}`, `<b>${esc(titulo)}</b>${linhas.map((l) => `<small>${esc(l)}</small>`).join("")}<span class="fio"></span>`);
    camada.appendChild(anuncio);
    const h = anuncio.offsetHeight, placaAlto = placa && placa.dataset.lugar === "dentro" ? placa.offsetHeight + 14 : 8;
    const livreTopo = g.fundoRoda + 10, livreFim = g.A.bottom - placaAlto;
    const y = livreTopo + Math.max(0, (livreFim - livreTopo - h) / 2);
    const cabe = g.rodaMedida && y + h <= livreFim && anuncio.offsetWidth <= g.larg - 12;
    posicionar(anuncio, [{ nome: "dentro", x: g.meio, y, ok: cabe }, { nome: "fora", x: g.meio, y: g.A.bottom + 10 }]);
    const este = anuncio;
    setTimeout(() => { if (este.isConnected) este.remove(); if (anuncio === este) anuncio = null; }, reduzido() ? 1800 : 1100);
  }
  // a placa: no pé da faixa dos comandos, dentro da arena; sem lugar ali (a luta pequena), presa à borda de baixo dela.
  // O lugar é decidido uma vez por luta e tamanho de janela, com a roda já medida (ela some na vez dos inimigos).
  function desenharPlaca(turno, pisca) {
    if (!garantirCamada()) return;
    if (!placa) { placa = faixa("turnos-placa", ""); camada.appendChild(placa); }
    const linhaIni = ini.ativa ? `<span class="ini">Iniciativa: ${esc(ini.curto)}</span>`
      : ini.mostrandoFim ? `<span class="ini ${ini.usada ? "usada" : "acabou"}">${ini.usada ? `Iniciativa usada (${esc(ini.pct)})` : "Iniciativa passou"}</span>` : "";
    placa.innerHTML = `<span class="t">Turno<b>${turno}</b></span>${linhaIni}`;
    const g = faixaComandos(), y = g.A.bottom - placa.offsetHeight - 10;
    placa.style.visibility = g.rodaMedida ? "" : "hidden";  // o lugar depende da roda: a placa entra quando ela aparece
    const chave = `${innerWidth}x${innerHeight}`;
    const fixo = lugarPlaca && lugarPlaca.chave === chave ? lugarPlaca.nome : null;
    posicionar(placa, [{ nome: "dentro", x: g.meio, y, ok: y >= g.fundoRoda + 8 }, { nome: "fora", x: g.meio, y: g.A.bottom - 4 }], fixo);
    if (!fixo && g.rodaMedida) lugarPlaca = { chave, nome: placa.dataset.lugar };
    placa.classList.toggle("pisca", !!pisca);
    if (pisca) setTimeout(() => placa && placa.classList.remove("pisca"), 650);
  }
  function limpar() {
    if (camada) camada.remove();
    camada = placa = anuncio = null;
    ultimoTurno = 0; fundoRoda = 0; lugarPlaca = null;
    ini = { ativa: false, texto: "", usada: false, mostrandoFim: false };
    clearInterval(ajuste); ajuste = 0;
  }
  function iniciativaAcabou() {
    ini.ativa = false; ini.mostrandoFim = true;
    desenharPlaca(ultimoTurno || (estado && estado.combate && estado.combate.turno) || 1);
    setTimeout(() => { ini.mostrandoFim = false; if (estado && estado.combate) desenharPlaca(estado.combate.turno || ultimoTurno); }, reduzido() ? 2400 : 1600);
  }
  const maiuscula = (t) => (t ? t[0].toUpperCase() + t.slice(1) : t);

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
      if (trava) anunciar("perde", `Turno ${n}`, [`${maiuscula(trava.nome)}: você perde este turno`]);
      else if (n === 1 && ini.ativa) anunciar("iniciativa", "Iniciativa!", ["Turno 1 · só você age agora", maiuscula(ini.texto)].filter(Boolean));
      else anunciar("", `Turno ${n}`);
    }
    desenharPlaca(n, !refazendo);
  }
  /** Os lances (fora do replay): a emboscada deles; o golpe que usa a iniciativa (também numa salva em área). */
  function aoLance(m) {
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
