// As conferências do Campo Livre 3 no navegador (Playwright, Chromium sem janela), com teclado e mouse de verdade:
// a câmera no modo de comando (entrar e sair, durante um golpe e pausado), a seleção com o tremor no máximo, nenhum
// ataque ao selecionar, o custo do 4× e algumas capturas pontuais. Precisa do servidor no ar:
//   PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs CAMPO_URL=http://127.0.0.1:8802/ node ferramentas/conferir3.mjs [partes]
// partes: camera, escalas, capturas (sem nada, todas). Escreve o resultado no terminal e em capturas/conferir3.json.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const ENDERECO = process.env.CAMPO_URL || "http://127.0.0.1:8801/";
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const CAPT = path.join(AQUI, "..", "capturas");
const partes = process.argv.slice(2);
const quer = (p) => !partes.length || partes.includes(p);
const nav = await chromium.launch();
const saidaJson = path.join(CAPT, "conferir3.json");
const R = fs.existsSync(saidaJson) ? JSON.parse(fs.readFileSync(saidaJson, "utf-8")) : {}, erros = [];
const espiar = (p, rot) => {
  p.on("pageerror", (e) => erros.push(`${rot}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${rot}: ${m.text()}`); });
};
// grava a câmera e o modo a cada quadro, para medir saltos
const gravar = (p) => p.evaluate(() => {
  window.__cam = [];
  const laco = () => { const s = __campo.st; __cam.push({ x: s.cam.x, y: s.cam.y, calma: s.calma, cmd: __campo.emComando(), arr: !!s.arrasto }); requestAnimationFrame(laco); };
  requestAnimationFrame(laco);
});
const trecho = async (p) => p.evaluate(() => { const c = __cam; window.__cam = []; return c; });
const maiorPasso = (q) => q.slice(1).reduce((mx, c, i) => Math.max(mx, Math.hypot(c.x - q[i].x, c.y - q[i].y)), 0);
const deslocou = (q) => (q.length ? Math.hypot(q[q.length - 1].x - q[0].x, q[q.length - 1].y - q[0].y) : 0);
const r1 = (v) => +v.toFixed(2);

if (quer("camera")) {
  const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
  espiar(p, "camera");
  await p.goto(`${ENDERECO}?heroi=guerreiro&enc=original&qtd=1&auto=1`);
  await p.evaluate(() => __campo.configurar({ tremor: 150 }));
  await p.waitForTimeout(3200);   // depois da formação: a câmera segue o herói olhando para o mouse
  await gravar(p);
  // tremor máximo o tempo todo
  await p.evaluate(() => { window.__trauma = setInterval(() => { __campo.efeitos().trauma = 1; }, 16); });

  // 1. sem Shift, o mouse desloca a câmera (a referência)
  await p.mouse.move(1180, 360); await p.waitForTimeout(700); await trecho(p);
  await p.mouse.move(100, 360, { steps: 20 }); await p.waitForTimeout(500);
  const semShift = await trecho(p);

  // 2. com Shift, o mesmo movimento não desloca a câmera; o tremor se acalma
  await p.mouse.move(1180, 360); await p.waitForTimeout(800);
  await p.keyboard.down("Shift"); await p.waitForTimeout(250); await trecho(p);
  await p.mouse.move(100, 360, { steps: 20 }); await p.waitForTimeout(500);
  const comShift = await trecho(p);

  // 3. arrasto com Shift: a câmera parada; a seleção = as tropas dentro do retângulo mostrado; nenhum golpe
  const antes = await p.evaluate(() => ({ usos: (__campo.mundo().stats.usos.basico || { usos: 0 }).usos, acao: !!__campo.mundo().heroi.acao }));
  await p.mouse.move(80, 120); await p.mouse.down();
  const camIni = await p.evaluate(() => ({ ...__campo.st.cam }));
  await p.mouse.move(700, 620, { steps: 25 }); await p.waitForTimeout(300);
  const noArrasto = await p.evaluate(() => {
    const s = __campo.st, a = s.arrasto, e = s.escala, m = __campo.mundo();
    const x0 = s.cam.x + Math.min(a.x0, a.x1) / e, x1 = s.cam.x + Math.max(a.x0, a.x1) / e;
    const y0 = s.cam.y + Math.min(a.y0, a.y1) / e, y1 = s.cam.y + Math.max(a.y0, a.y1) / e;
    const dentro = m.lados[0].filter((u) => u !== m.heroi && u.x >= x0 && u.x <= x1 && u.y - 4 >= y0 && u.y - 4 <= y1).map((u) => u.id);
    return { cam: { ...s.cam }, calma: s.calma, dentro };
  });
  await p.mouse.up();
  const depois = await p.evaluate(() => ({ sel: [...__campo.mundo().selecao], usos: (__campo.mundo().stats.usos.basico || { usos: 0 }).usos }));
  const arrasto = await trecho(p);
  const iguais = noArrasto.dentro.length === depois.sel.length && noArrasto.dentro.every((id) => depois.sel.includes(id));

  // 4. soltar o Shift: o olhar volta para o mouse sem salto
  await p.mouse.move(100, 360);
  await p.keyboard.up("Shift"); await p.waitForTimeout(900);
  const saida = await trecho(p);

  // 5. Shift durante um golpe (a Varredura): o golpe continua até o contato, nenhum ataque depois, a câmera não anda
  await p.mouse.move(900, 360); await p.waitForTimeout(600); await trecho(p);
  await p.mouse.down({ button: "right" }); await p.mouse.up({ button: "right" });
  await p.keyboard.down("Shift");
  await p.mouse.move(200, 300, { steps: 15 }); await p.waitForTimeout(500);
  const golpe = await p.evaluate(() => ({ varredura: (__campo.mundo().stats.usos.varredura || { usos: 0 }).usos, basico: (__campo.mundo().stats.usos.basico || { usos: 0 }).usos }));
  const duranteGolpe = await trecho(p);
  await p.keyboard.up("Shift"); await p.waitForTimeout(900);
  const saidaGolpe = await trecho(p);

  // 6. pausado: o mouse não mexe a câmera; o arrasto seleciona; ao continuar, sem salto
  await p.keyboard.press("KeyP"); await p.waitForTimeout(200); await trecho(p);
  await p.mouse.move(1200, 600, { steps: 15 }); await p.mouse.move(300, 200); await p.mouse.down();
  await p.mouse.move(800, 500, { steps: 10 }); await p.mouse.up();
  const pausado = await trecho(p);
  const selPausado = await p.evaluate(() => __campo.mundo().selecao.size);
  await p.keyboard.press("KeyP"); await p.waitForTimeout(900);
  const saidaPausa = await trecho(p);
  await p.evaluate(() => clearInterval(window.__trauma));

  R.camera = {
    sem_shift_mouse_desloca_px: r1(deslocou(semShift)),
    com_shift_mouse_desloca_px: r1(deslocou(comShift)), com_shift_calma_final: r1(comShift[comShift.length - 1].calma),
    arrasto_camera_mexeu_px: r1(Math.hypot(noArrasto.cam.x - camIni.x, noArrasto.cam.y - camIni.y)), arrasto_calma: r1(noArrasto.calma),
    arrasto_selecionados: depois.sel.length, arrasto_mesmos_do_retangulo: iguais, arrasto_golpes: depois.usos - antes.usos,
    saida_maior_passo_px: r1(maiorPasso(saida)), saida_deslocamento_px: r1(deslocou(saida)), saida_calma_final: r1(saida[saida.length - 1].calma),
    golpe_varreduras: golpe.varredura, golpe_basicos_durante_shift: golpe.basico - depois.usos,
    golpe_shift_camera_px: r1(deslocou(duranteGolpe)), golpe_saida_maior_passo_px: r1(maiorPasso(saidaGolpe)),
    pausado_camera_px: r1(deslocou(pausado)), pausado_selecionados: selPausado, pausa_saida_maior_passo_px: r1(maiorPasso(saidaPausa)),
    referencia_sem_shift_maior_passo_px: r1(maiorPasso(semShift)),
  };
  console.log("camera", R.camera);
  await p.close();
}

if (quer("escalas")) {
  R.escalas = [];
  for (const [w, h] of [[1920, 945], [1280, 720]]) for (const [heroi, enc, kit] of [["guerreiro", "original", "escudo,turbilhao"], ["mago", "capitao", "raios,gelo"]]) {
    const p = await nav.newPage({ viewport: { width: w, height: h } });
    espiar(p, `escala ${w} ${enc}`);
    await p.goto(`${ENDERECO}?heroi=${heroi}&enc=${enc}&qtd=4&kit=${kit}&auto=1&robo=1`);
    await p.waitForTimeout(3000);
    await p.evaluate(() => { const d = __campo.st.diag; d.quadros = []; d.sim = []; d.desenho = []; });
    let maxU = 0, maxN = 0;
    for (let i = 0; i < 20; i++) {
      await p.waitForTimeout(1000);
      const v = await p.evaluate(() => ({ u: __campo.mundo().unidades.length, n: __campo.efeitos().numeros.length }));
      maxU = Math.max(maxU, v.u); maxN = Math.max(maxN, v.n);
    }
    const d = await p.evaluate(() => __campo.diagnostico());
    R.escalas.push({ janela: `${w}×${h}`, heroi, enc, kit, combatentes_max: maxU, numeros_max: maxN, qps: r1(d.fps),
      quadro_p95: r1(d.quadroP95), quadro_max: r1(d.quadroMax), sim_media: r1(d.simMedio), sim_p95: r1(d.simP95),
      desenho_media: r1(d.desenhoMedio), desenho_p95: r1(d.desenhoP95) });
    console.log("escala 4×", R.escalas[R.escalas.length - 1]);
    await p.close();
  }
}

// a escolha com as quantidades e as habilidades novas, nas duas janelas
if (quer("escolha") || quer("capturas")) for (const [w, h] of [[1920, 945], [1280, 720]]) {
  const p = await nav.newPage({ viewport: { width: w, height: h } });
  espiar(p, `escolha ${w}`);
  await p.goto(`${ENDERECO}`);
  await p.selectOption("#op-quantidade", "4");
  await p.click('button.encontro[data-enc="capitao"]');
  await p.click('.heroi[data-heroi="guerreiro"] button[data-v="escudo"]');
  await p.click('.heroi[data-heroi="guerreiro"] button[data-v="turbilhao"]');
  await p.click('.heroi[data-heroi="mago"] button[data-v="raios"]');
  await p.click('.heroi[data-heroi="mago"] button[data-v="gelo"]');
  await p.waitForTimeout(300);
  R.contagem = await p.textContent("#contagem");
  await p.screenshot({ path: path.join(CAPT, `cl3-escolha-${w}.png`) });
  await p.close();
}

if (quer("capturas")) {
  const p = await nav.newPage({ viewport: { width: 1920, height: 945 } });
  espiar(p, "capturas");
  // a batalha 4× no meio do choque
  await p.goto(`${ENDERECO}?heroi=guerreiro&enc=original&qtd=4&kit=escudo,turbilhao&auto=1&robo=1`);
  await p.waitForTimeout(9000);
  await p.screenshot({ path: path.join(CAPT, "cl3-4x-1920-9s.png") });
  // a Arremetida do Capitão marcada no chão (o primeiro quadro com ela)
  await p.goto(`${ENDERECO}?heroi=mago&enc=capitao&qtd=1&kit=raios,gelo&auto=1&robo=1`);
  await p.waitForFunction(() => { const l = __campo.mundo().lider; return l && l.acao && l.acao.tipo === "arremetida" && l.acao.t < 0.45; }, null, { timeout: 40000 });
  await p.keyboard.press("KeyP");
  await p.screenshot({ path: path.join(CAPT, "cl3-arremetida-1920.png") });
  await p.close();
}

// as habilidades novas: um quadro pausado de cada, recortado em volta do herói (1280×720, ampliação 2×)
if (quer("habilidades")) {
  const casos = [
    ["escudo", "guerreiro", "escudo,turbilhao", "capitao", () => { const a = __campo.mundo().heroi.acao; return a && a.fase === "escudo" && a.t < 1.8; }],
    ["turbilhao", "guerreiro", "escudo,turbilhao", "original", () => { const a = __campo.mundo().heroi.acao; return a && a.id === "salto" && a.fase === "preparo" && a.t < 0.12; }],
    ["raios", "mago", "raios,gelo", "original", () => __campo.efeitos().raios.some((r) => r.t > 0.03)],
    ["gelo", "mago", "gelo", "original", () => __campo.mundo().zonas.some((z) => z.tipo === "gelo" && z.t < z.dur - 0.6)],
  ];
  for (const [nome, heroi, kit, enc, cond] of casos) {
    const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
    espiar(p, `habilidade ${nome}`);
    await p.goto(`${ENDERECO}?heroi=${heroi}&enc=${enc}&kit=${kit}&auto=1&robo=1`);
    // o jogador automático quase não usa o gelo (foge antes de juntar cinco perto): aqui, Q apertado no meio da luta
    if (nome === "gelo") { await p.waitForTimeout(7000); await p.keyboard.press("KeyQ"); }
    try {
      await p.waitForFunction(cond, null, { timeout: 60000, polling: "raf" });
      await p.keyboard.press("KeyP");
      const c = await p.evaluate(() => { const s = __campo.st, h = __campo.mundo().heroi; return { x: (h.x - s.cam.x) * s.escala, y: (h.y - s.cam.y) * s.escala }; });
      const clip = { x: Math.max(0, Math.min(1280 - 520, c.x - 260)), y: Math.max(0, Math.min(720 - 340, c.y - 170)), width: 520, height: 340 };
      await p.screenshot({ path: path.join(CAPT, `cl3-${nome}.png`), clip });
      console.log("habilidade", nome, "ok");
    } catch (e) { erros.push(`${nome}: não apareceu (${e.message.split("\n")[0]})`); }
    await p.close();
  }
}

R.erros = erros;
fs.writeFileSync(saidaJson, JSON.stringify(R, null, 2));
console.log(erros.length ? `erros: ${erros.join(" | ")}` : "sem erros no console");
await nav.close();
