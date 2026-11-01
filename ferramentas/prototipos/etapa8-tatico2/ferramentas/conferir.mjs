// Playwright, Tático 2: abre a tela de verdade, monta pela preparação, luta pela arena e tira capturas pontuais nas
// duas janelas de referência (1920 × 1080 e 1280 × 720). Confere: a preparação monta (encontros, classes,
// habilidades, talentos, companheiros), a luta começa, a barra mostra o kit, andar mostra o custo e anda, mirar mostra
// alcance e prévia, lançar aplica o que a prévia disse, a vez passa por Morel e Odette, os inimigos jogam, nada fica
// fora da tela, e nenhum erro no console.
// Uso: PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs node ferramentas/conferir.mjs [porta] [pasta de capturas]
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const PORTA = process.argv[2] || "8807", SAIDA = process.argv[3] || new URL("../capturas", import.meta.url).pathname.replace(/^\/([A-Z]:)/, "$1");
const BASE = `http://127.0.0.1:${PORTA}/`;
const nav = await chromium.launch();
const falhas = [];
const ok = (c, msg) => { if (!c) falhas.push(msg); console.log(c ? "  ok " : "  FALHA ", msg); };

for (const [w, h] of [[1920, 1080], [1280, 720]]) {
  const p = await nav.newPage({ viewport: { width: w, height: h } });
  const erros = [];
  p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  p.on("pageerror", (e) => erros.push("pageerror: " + e.message));
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.goto(BASE, { waitUntil: "networkidle" });
  console.log(`== ${w}×${h}`);
  const prep = await p.evaluate(() => ({
    encontros: document.querySelectorAll("#encontros .cartao").length, classes: document.querySelectorAll("#classes .cartao").length,
    habs: document.querySelectorAll("#montagem [data-hab]").length, tals: document.querySelectorAll("#montagem [data-tal]").length,
    comp: document.querySelectorAll("#companheiros .item").length, titulo: document.title,
    topo: document.querySelector("#tela-preparar .caixa").getBoundingClientRect().top,
  }));
  ok(prep.encontros === 3 && prep.classes === 3 && prep.habs === 10 && prep.tals === 5 && prep.comp === 10, `preparação monta ${JSON.stringify(prep)}`);
  ok(prep.titulo.startsWith("Tático 2"), "versão Tático 2 no título");
  // a classe Mago pela tela, a montagem pronta Criomante, o encontro misto
  await p.click("#classes .cartao:nth-child(2)");
  await p.click('#montagem button[data-build="Criomante"]');
  await p.click("#encontros .cartao:nth-child(3)");
  await p.screenshot({ path: `${SAIDA}/t2-preparar-${w}.png` });
  await p.click("#lutar");
  await p.waitForTimeout(400);
  // espera a vez de um aliado controlado pelo jogador
  await p.waitForFunction(() => window.tatico.atual() && window.tatico.atual().lado === 0 && !window.tatico.st.animando, null, { timeout: 30000 });
  const quem = await p.evaluate(() => window.tatico.atual().nome);
  const barra = await p.evaluate(() => [...document.querySelectorAll("#barra .hab")].map((b) => b.querySelector(".nome").textContent));
  ok(barra.length >= 5, `a barra mostra o kit de ${quem}: ${barra.join(", ")}`);
  // a arena cabe na janela e nada da HUD passa da borda
  const caber = await p.evaluate(() => {
    const fora = [...document.querySelectorAll("#hud *")].filter((e) => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.bottom > innerHeight + 1 || r.left < -1); }).map((e) => e.id || e.className);
    const st = window.tatico.st;
    return { fora, escala: st.escala, larg: st.ox >= 0, alto: st.oy >= 0 };
  });
  ok(!caber.fora.length && caber.larg && caber.alto, `tudo dentro da janela (escala ${caber.escala}) ${caber.fora.join(",")}`);
  // andar: o custo aparece no caminho e o movimento gasta os PM
  const andar = await p.evaluate(async () => {
    const st = window.tatico.st, u = window.tatico.atual();
    const { alcancaveis } = await import("/regras.js");
    const r = [...alcancaveis(st.m, u).values()].filter((c) => c.caminho.length).sort((a, b) => b.custo - a.custo)[0];
    return r ? { x: r.x, y: r.y, custo: r.custo, pm: u.pm } : null;
  });
  const tela = async (x, y) => p.evaluate(([x, y]) => {
    const st = window.tatico.st, sx = (x - y) * 16, sy = (x + y) * 8 + 8;
    return [st.ox + (sx + st.orig[0]) * st.escala, st.oy + (sy + st.orig[1]) * st.escala];
  }, [x, y]);
  if (andar) {
    const [mx, my] = await tela(andar.x, andar.y);
    await p.mouse.move(mx, my);
    await p.waitForTimeout(150);
    const custo = await p.evaluate(() => window.tatico.st.custoCaminho);
    ok(custo === andar.custo, `o caminho mostra ${custo} PM (esperado ${andar.custo})`);
    await p.screenshot({ path: `${SAIDA}/t2-andar-${w}.png` });
    await p.mouse.click(mx, my);
    await p.waitForFunction(() => !window.tatico.st.animando);
    await p.waitForTimeout(300);
    const depois = await p.evaluate(() => { const u = window.tatico.atual(); return { x: u.x, y: u.y, pm: u.pm }; });
    ok(depois.x === andar.x && depois.y === andar.y && depois.pm === andar.pm - andar.custo, `andou e gastou ${andar.custo} PM`);
  }
  // mirar: alcance, prévia igual ao efeito (assim que houver um inimigo ao alcance)
  const mirarELancar = async () => {
    const mira = await p.evaluate(async () => {
      const st = window.tatico.st, u = window.tatico.atual(), { alvosValidos, prever } = await import("/regras.js");
      for (const [i, id] of Object.keys(u.kit).entries()) {
        const alvos = alvosValidos(st.m, u, id).filter(([x, y]) => st.m.unidades.some((w) => w.vivo && w.lado === 1 && w.x === x && w.y === y));
        if (alvos.length) { const p = prever(st.m, u.id, id, ...alvos[0]); return { tecla: i + 1, id, alvo: alvos[0], mud: p.mud.map((d) => ({ id: d.id, dPv: d.dPv, para: d.para, antes: st.m.unidades.find((w) => w.id === d.id).pv })) }; }
      }
      return null;
    });
    if (mira) {
      await p.keyboard.press(String(mira.tecla));
      const [mx, my] = await tela(...mira.alvo);
      await p.mouse.move(mx, my);
      await p.waitForTimeout(200);
      const prev = await p.evaluate(() => window.tatico.st.prev && window.tatico.st.prev.mud.map((d) => ({ id: d.id, dPv: d.dPv })));
      ok(prev && prev.length > 0, `a prévia aparece sobre o alvo (${mira.id})`);
      await p.screenshot({ path: `${SAIDA}/t2-mirar-${w}.png` });
      await p.mouse.click(mx, my);
      await p.waitForFunction(() => !window.tatico.st.animando);
      const real = await p.evaluate((ids) => ids.map((id) => window.tatico.st.m.unidades.find((u) => u.id === id).pv), mira.mud.map((d) => d.id));
      const esperado = mira.mud.map((d) => Math.max(0, d.antes + d.dPv));
      ok(real.every((v, i) => Math.max(0, v) === esperado[i]), `lançou ${mira.id}: a vida depois (${real.join(", ")}) é a da prévia (${esperado.join(", ")})`);
      return true;
    }
    return false;
  };
  let mirou = await mirarELancar();
  // passa a vez até chegarem Morel e Odette; os inimigos jogam entre elas
  const vistos = new Set([quem]);
  for (let i = 0; i < 10 && (vistos.size < 3 || (await p.evaluate(() => window.tatico.st.m.rodada)) < 2); i++) {
    await p.keyboard.press("Space");
    await p.waitForFunction(() => { const a = window.tatico.atual(); const st = window.tatico.st; return !st.m || st.m.fim || (a && a.lado === 0 && !st.animando); }, null, { timeout: 60000 });
    const n = await p.evaluate(() => window.tatico.st.m.fim ? null : window.tatico.atual().nome);
    if (!n) break;
    vistos.add(n);
    if (n === "Morel" || n === "Odette") await p.screenshot({ path: `${SAIDA}/t2-vez-${n.toLowerCase()}-${w}.png` });
  }
  for (let i = 0; i < 6 && !mirou; i++) {
    const fim = await p.evaluate(() => window.tatico.st.m.fim);
    if (fim) break;
    mirou = await mirarELancar();
    if (!mirou) {
      await p.keyboard.press("Space");
      await p.waitForFunction(() => { const a = window.tatico.atual(); const st = window.tatico.st; return !st.m || st.m.fim || (a && a.lado === 0 && !st.animando); }, null, { timeout: 60000 });
    }
  }
  ok(mirou, "a mira e a prévia foram conferidas num alvo de verdade");
  ok(vistos.has("Morel") && vistos.has("Odette"), `a vez passou por ${[...vistos].join(", ")}`);
  const agiram = await p.evaluate(() => { const st = window.tatico.st; return st.m.unidades.filter((u) => u.lado === 1 && (st.inicio[u.id] !== `${u.x},${u.y}` || u.pv < u.pvMax || st.m.registro.some((r) => r.texto.startsWith(u.nome + ":")))).length; });
  ok(agiram >= 4, `os inimigos agiram na primeira rodada: ${agiram} de 5 andaram ou lançaram`);
  ok(!erros.length, `sem erros no console ${erros.join(" | ")}`);
  await p.close();
}
await nav.close();
console.log(falhas.length ? `${falhas.length} FALHAS` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
