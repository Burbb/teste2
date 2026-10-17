// Protótipo da etapa 1C: a iniciativa e a passagem dos turnos (nada disto está no jogo). Só escuta o que o jogo já
// recebe do motor, sem deduzir nada de quantas mensagens ou animações passaram:
//   - a mensagem "turno" (ui.novo_turno, uma vez por volta do laço da luta, no começo da sua vez; a comitiva, o animal e
//     os servos não a geram): o anúncio "Turno N";
//   - estado.combate.turno: a placa com o turno de agora (vale também ao recarregar a página no meio da luta);
//   - o lance "surpresa": de="j" é a sua iniciativa (os inimigos pegos de surpresa); de um inimigo, a emboscada deles
//     (o golpe livre do mais rápido, antes do turno 1);
//   - o estado "iniciativa" na sua carta (estado.combate.heroi.efeitos, com o texto do motor: "+25% de dano no primeiro
//     golpe deste turno"): enquanto existe, a linha da iniciativa na placa;
//   - o golpe com bonus_motivo "Iniciativa!" (combate/golpe.py consome o estado): a iniciativa foi usada; se o estado
//     some sem esse golpe (uma poção, um buff no turno livre: luta.py a remove no fim da sua vez), ela passou.
// Nada espera por nada: os anúncios não seguram a fila de mensagens nem o clique (a camada não recebe o mouse).
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const reduzido = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
  const VARS = ["--sh-ponta-e1", "--sh-ponta-d2", "--sh-meio", "--sh-grao", "--sh-texto", "--sh-latao"];
  let camada = null, placa = null, anuncio = null, ultimoTurno = 0;
  let ini = { ativa: false, texto: "", usada: false, mostrandoFim: false };
  let fundoRoda = 0;  // o pé da roda de comandos (a última vez que ela esteve à vista), em px da arena
  let lugarPlaca = null;  // {chave: o tamanho da janela, nome: dentro|fora}, decidido uma vez por luta

  // A camada mora na página (fixa), acima da arena e do registro: assim o anúncio e a placa podem ficar dentro da arena
  // (onde houver lugar livre) ou logo abaixo dela, e passam por cima da roda de comandos sem ficar atrás dela.
  function garantirCamada() {
    const arena = $("#arena");
    if (!arena) return null;
    if (!camada || !camada.isConnected) {
      camada = document.createElement("div");
      camada.className = "turnos-camada";
      const roda = $("#roda") || arena;
      const cs = getComputedStyle(roda);
      VARS.forEach((v) => { const x = cs.getPropertyValue(v); if (x) camada.style.setProperty(v, x); });  // as pontas do seletor
      document.body.appendChild(camada);
      placa = null;
    }
    return camada;
  }
  // o que não pode ser coberto: as cartas, os comandos, a mira, o seletor e o aviso da cena
  // (as cartas no lugar final: enquanto a arena se acomoda, elas deslizam com um desvio _acX/_acY de batalha.js)
  function obstaculos() {
    return [...document.querySelectorAll("#batalha .carta, #roda .roda-botao, .roda-mira, .roda-janela, #arena > .mods-arena .mod")]
      .map((e) => {
        const q = e.getBoundingClientRect(), dx = e._acX || 0, dy = e._acY || 0;
        return { left: q.left - dx, right: q.right - dx, top: q.top - dy, bottom: q.bottom - dy, width: q.width, height: q.height };
      }).filter((q) => q.width && q.height);
  }
  const toca = (a, q) => a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1;
  // a faixa dos comandos: entre a sua fileira e a dos inimigos (nenhuma carta entra ali: batalha.js, distribuir)
  // pelas colunas, não pelas cartas: a sua carta cresce na sua vez (1,06×, como em batalha.js) e as cartas deslizam
  // quando a arena se acomoda; as colunas ficam paradas
  function faixaComandos() {
    const arena = $("#arena"), R = arena.getBoundingClientRect(), al = $("#batalha .aliados"), ini = $("#batalha .inimigos");
    // a altura final da arena (ela cresce devagar quando uma carta entra ou ganha efeitos: batalha.js, acomodar)
    const A = { left: R.left, right: R.right, top: R.top, width: R.width, height: arena._altura || R.height, bottom: R.top + (arena._altura || R.height) };
    const ra = al && al.getBoundingClientRect(), ri = ini && ini.getBoundingClientRect();
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
  // o anúncio: dentro da arena, no meio do que sobra embaixo da roda; senão, logo abaixo da arena, sobre o registro
  function anunciar(classe, titulo, linhas = []) {
    if (!garantirCamada()) return;
    if (anuncio) anuncio.remove();
    const g = faixaComandos();
    anuncio = faixa(`turnos-anuncio ${classe}`, `<b>${titulo}</b>${linhas.map((l) => `<small>${l}</small>`).join("")}<span class="fio"></span>`);
    camada.appendChild(anuncio);
    const h = anuncio.offsetHeight, placaAlto = placa && placa.dataset.lugar === "dentro" ? placa.offsetHeight + 14 : 8;
    const livreTopo = g.fundoRoda + 10, livreFim = g.A.bottom - placaAlto;
    const y = livreTopo + Math.max(0, (livreFim - livreTopo - h) / 2);
    // dentro da arena só com a roda já vista nesta luta (o primeiro turno ainda não a tem: sem saber onde ela fica, fora)
    // e só se o anúncio couber na largura da faixa dos comandos, com folga
    const cabe = g.rodaMedida && y + h <= livreFim && anuncio.offsetWidth <= g.larg - 12;
    posicionar(anuncio, [{ nome: "dentro", x: g.meio, y, ok: cabe }, { nome: "fora", x: g.meio, y: g.A.bottom + 10 }]);
    const este = anuncio;
    setTimeout(() => { if (este.isConnected) este.remove(); if (anuncio === este) anuncio = null; }, reduzido() ? 1800 : 1100);
  }
  // a placa: no pé da faixa dos comandos, dentro da arena; sem lugar ali (a luta pequena), presa à borda de baixo dela
  function desenharPlaca(turno, pisca) {
    if (!garantirCamada()) return;
    if (!placa) { placa = faixa("turnos-placa", ""); camada.appendChild(placa); }
    const linhaIni = ini.ativa ? `<span class="ini">Iniciativa: ${ini.curto}</span>`
      : ini.mostrandoFim ? `<span class="ini ${ini.usada ? "usada" : "acabou"}">${ini.usada ? `Iniciativa usada (${ini.pct})` : "Iniciativa passou"}</span>` : "";
    placa.innerHTML = `<span class="t">Turno<b>${turno}</b></span>${linhaIni}`;
    const g = faixaComandos(), y = g.A.bottom - placa.offsetHeight - 10;
    placa.style.visibility = g.rodaMedida ? "" : "hidden";  // o lugar depende da roda: a placa entra quando ela aparece
    // o lugar da placa é decidido uma vez por luta e tamanho de janela, com a roda já medida: sem trocar de lugar
    // quando a roda some na vez dos inimigos e volta na sua
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
  }
  function lerIniciativa(cb) {
    const ef = ((cb && cb.heroi && cb.heroi.efeitos) || []).find((e) => e.id === "iniciativa");
    return ef ? (ef.texto || "") : null;
  }
  function iniciativaAcabou() {
    ini.ativa = false; ini.mostrandoFim = true;
    desenharPlaca(ultimoTurno || (estado.combate && estado.combate.turno) || 1);
    setTimeout(() => { ini.mostrandoFim = false; if (estado && estado.combate) desenharPlaca(estado.combate.turno || ultimoTurno); }, reduzido() ? 2400 : 1600);
  }

  // o estado: a placa acompanha o turno do motor; a iniciativa entra e sai pelo estado da sua carta
  function aoEstado(e) {
    try {
      if (!e || !e.combate) { limpar(); return; }
      const texto = lerIniciativa(e.combate);
      if (texto !== null && !ini.ativa && !ini.usada) {
        const pct = (texto.match(/[+−-]\d+%/) || [""])[0];
        ini = { ativa: true, texto, pct, curto: pct ? `${pct} no 1º golpe` : texto, usada: false, mostrandoFim: false };
      } else if (texto === null && ini.ativa) {
        iniciativaAcabou();  // passou sem golpe (o golpe que a usa já a marcou, abaixo)
      }
      if (e.combate.turno) { ultimoTurno = Math.max(ultimoTurno, e.combate.turno); desenharPlaca(ultimoTurno); }
    } catch (err) { console.warn("turnos (protótipo):", err); }
  }
  const aplicar = window.aplicarEstado;
  window.aplicarEstado = (e, ...x) => { const r = aplicar(e, ...x); aoEstado(e); return r; };
  // a mensagem do turno: o anúncio. O turno 1 com a iniciativa vira um anúncio só (a iniciativa e o turno livre)
  const turnoOriginal = window.turno;
  window.turno = (m, ...x) => {
    const r = turnoOriginal(m, ...x);
    try {
      ultimoTurno = m.n;
      if (m.n === 1 && ini.ativa) {
        anunciar("iniciativa", "Iniciativa!", ["Turno 1 · só você age agora", ini.texto ? ini.texto[0].toUpperCase() + ini.texto.slice(1) : ""].filter(Boolean));
      } else {
        anunciar("", `Turno ${m.n}`);
      }
      desenharPlaca(m.n, true);
    } catch (err) { console.warn("turnos (protótipo):", err); }
    return r;
  };
  // os lances: a emboscada deles; o golpe que usa a iniciativa
  const lanceOriginal = Batalha.lance;
  Batalha.lance = (m, ...x) => {
    try {
      if (m.tipo === "surpresa" && m.de && m.de !== "j") {
        const c = Batalha.elCarta(m.de), nome = c ? c.querySelector(".carta-nome span").textContent : "Um inimigo";
        anunciar("emboscada", "Emboscada!", [`${nome} ataca antes de você`]);
      }
      const usa = (g) => g && g.tipo === "golpe" && g.de === "j" && g.bonus_motivo === "Iniciativa!";
      if ((usa(m) || (m.tipo === "salva" && (m.lances || []).some(usa))) && ini.ativa) {  // também numa salva em área
        ini.usada = true;
        iniciativaAcabou();
      }
    } catch (err) { console.warn("turnos (protótipo):", err); }
    return lanceOriginal(m, ...x);  // a fila segue no tempo dela: nada aqui espera
  };
  // redimensionar: a placa acompanha a faixa dos comandos
  addEventListener("resize", () => { if (placa && estado && estado.combate) desenharPlaca(ultimoTurno || estado.combate.turno); });
  // a arena cresce devagar quando uma carta entra ou ganha efeitos (batalha.js, acomodar): a placa acompanha
  setInterval(() => { if (placa && placa.isConnected && estado && estado.combate) desenharPlaca(ultimoTurno || estado.combate.turno); }, 400);
  if (typeof estado !== "undefined" && estado) aoEstado(estado);  // injetado com a luta já em andamento
})();
