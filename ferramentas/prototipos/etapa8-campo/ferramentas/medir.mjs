// Medição, capturas e vídeos do protótipo de campo livre (Playwright, Chromium sem janela). Precisa do servidor no ar:
//   PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs CAMPO_URL=http://127.0.0.1:8801/ node ferramentas/medir.mjs [partes]
// partes: resposta, pausa, selecao, desempenho, capturas, sequencias, videos (sem nada, todas). Grava capturas/medicao.json, capturas/*.png e
// videos/*.webm. Os vídeos e o desempenho usam o jogador automático (?robo=1): a mesma entrada que o teclado e o mouse
// preenchem, decidida por robo.js; a resposta e a pausa usam teclado e mouse de verdade.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const ENDERECO = process.env.CAMPO_URL || "http://127.0.0.1:8801/";
const AQUI = path.dirname(fileURLToPath(import.meta.url));
const CAPT = path.join(AQUI, "..", "capturas"), VIDS = path.join(AQUI, "..", "videos");
const partes = process.argv.slice(2);
const quer = (p) => !partes.length || partes.includes(p);
const saidaJson = path.join(CAPT, "medicao.json");
const R = fs.existsSync(saidaJson) ? JSON.parse(fs.readFileSync(saidaJson, "utf-8")) : {};
const nav = await chromium.launch();
const erros = [];
const espiar = (p, rot) => {
  p.on("pageerror", (e) => erros.push(`${rot}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${rot}: ${m.text()}`); });
};
R.condicoes = {
  data: new Date().toISOString(), navegador: `Chromium ${nav.version()} (Playwright, sem janela)`,
  maquina: process.env.COMPUTERNAME || "", nota: "Chromium headless desenha o canvas na CPU; 60 qps é o teto do rAF.",
};

// ---------------------------------------------------------------------------------------------- resposta
if (quer("resposta")) {
  const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
  espiar(p, "resposta");
  await p.goto(`${ENDERECO}?heroi=guerreiro&auto=1`);
  await p.waitForTimeout(800);
  await p.evaluate(() => {
    window.__ev = []; window.__q = [];
    for (const tipo of ["keydown", "keyup", "mousedown"]) addEventListener(tipo, (e) => __ev.push({ tipo, code: e.code || e.button, t: performance.now(), st: __campo.mundo().t }), true);
    const laco = () => { const h = __campo.mundo().heroi; __q.push({ t: performance.now(), st: __campo.mundo().t, vx: h.vx, acao: h.acao && h.acao.id, fase: h.acao && h.acao.fase }); requestAnimationFrame(laco); };
    requestAnimationFrame(laco);
  });
  const caixa = { x: 640, y: 360 };
  await p.mouse.move(caixa.x + 200, caixa.y);
  await p.keyboard.down("KeyD"); await p.waitForTimeout(500); await p.keyboard.up("KeyD");
  await p.waitForTimeout(400);
  await p.mouse.move(caixa.x + 200, caixa.y);
  await p.mouse.down({ button: "right" }); await p.mouse.up({ button: "right" });
  await p.waitForTimeout(700);
  await p.keyboard.press("Space");
  await p.waitForTimeout(500);
  const { ev, q, vel } = await p.evaluate(() => ({ ev: __ev, q: __q, vel: __campo.mundo().heroi.def.vel }));
  // duas medidas: o tempo de relógio até o primeiro quadro com a mudança (inclui as travadas do Playwright ao injetar
  // a tecla, ~85 ms no Chromium sem janela) e o tempo de jogo (passos de 16,7 ms) entre o evento e a mudança
  const primeiro = (e0, f) => { const x = q.find((k) => k.t >= e0.t && f(k)); return x ? [+(x.t - e0.t).toFixed(1), +((x.st - e0.st) * 1000).toFixed(1)] : null; };
  const kd = ev.find((e) => e.tipo === "keydown" && e.code === "KeyD"), ku = ev.find((e) => e.tipo === "keyup" && e.code === "KeyD");
  const md = ev.find((e) => e.tipo === "mousedown"), sp = ev.find((e) => e.tipo === "keydown" && e.code === "Space");
  R.resposta = {
    andar_primeiro_quadro: primeiro(kd, (k) => k.vx > 0.1), andar_velocidade_maxima: primeiro(kd, (k) => k.vx >= vel * 0.99),
    parar: primeiro(ku, (k) => Math.abs(k.vx) < 0.01),
    varredura_comeca: primeiro(md, (k) => k.acao === "varredura"), varredura_contato: primeiro(md, (k) => k.acao === "varredura" && k.fase === "rec"),
    investida_comeca: primeiro(sp, (k) => k.acao === "investida"),
    nota: "[ms de relógio até o quadro, ms de jogo]; o relógio inclui a travada do Playwright ao injetar teclas",
  };
  console.log("resposta", R.resposta);
  await p.close();
}

// ---------------------------------------------------------------------------------------------- pausa, retomada, reinício
if (quer("pausa")) {
  const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
  espiar(p, "pausa");
  await p.goto(`${ENDERECO}?heroi=mago&auto=1&robo=1`);
  await p.waitForTimeout(4000);
  const t = () => p.evaluate(() => __campo.mundo().t);
  await p.keyboard.press("KeyP");
  const a = await t(); await p.waitForTimeout(600); const b = await t();
  const telaPausa = await p.isVisible("#tela-pausa");
  await p.keyboard.press("Digit3");   // ordem dada pausado
  const ordem = await p.evaluate(() => __campo.mundo().ordem.tipo);
  await p.screenshot({ path: path.join(CAPT, "pausa-1280.png") });
  await p.keyboard.press("KeyP");
  await p.waitForTimeout(600); const c = await t();
  await p.keyboard.press("KeyR");
  await p.waitForTimeout(300); const d = await t();
  await p.keyboard.press("Tab"); await p.waitForTimeout(700);
  const painel = await p.isVisible("#painel");
  await p.screenshot({ path: path.join(CAPT, "registro-1280.png") });
  R.pausa = { parado_durante_pausa: +(b - a).toFixed(3), tela_de_pausa: telaPausa, ordem_pausado: ordem,
    andou_depois: +(c - b).toFixed(2), reinicio_t: +d.toFixed(2), painel_abre: painel };
  console.log("pausa", R.pausa);
  await p.close();
}

// ---------------------------------------------------------------------------------------------- seleção e ordens
// Com teclado e mouse de verdade: F2 seleciona os arqueiros, 3 os manda defender um ponto, Shift + arrasto seleciona
// soldados sem atacar, 2 os manda atacar, X limpa; pausado, o arrasto seleciona sem Shift; com o tremor no máximo e
// trauma 1, o mouse aponta para o mesmo lugar do mundo e o arrasto pega as mesmas tropas.
if (quer("selecao")) {
  const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
  espiar(p, "seleção");
  const paginas = () => p.context().pages().length;
  await p.goto(`${ENDERECO}?heroi=guerreiro&enc=duasFrentes&auto=1`);
  await p.waitForTimeout(700);
  const ver = () => p.evaluate(() => {
    const m = __campo.mundo(), t = m.lados[0].filter((u) => u !== m.heroi);
    return { sel: [...m.selecao], ordens: Object.fromEntries(t.map((u) => [u.id, u.ordem.tipo])), tipos: Object.fromEntries(t.map((u) => [u.id, u.tipo])),
      usosBasico: (m.stats.usos[m.heroi.slots.principal] || { usos: 0 }).usos, hud: document.querySelector("#p-selecao").textContent };
  });
  const tela = (x, y) => p.evaluate(([x, y]) => { const st = __campo.st; return [(x - st.cam.x) * st.escala, (y - st.cam.y) * st.escala]; }, [x, y]);
  const R2 = {};
  await p.keyboard.press("F2");
  let v = await ver();
  R2.f2_seleciona_arqueiros = v.sel.length === 12 && v.sel.every((id) => v.tipos[id] === "arqueiro");
  R2.f2_hud = v.hud;
  const [px, py] = await tela(480, 110);
  await p.mouse.move(px, py);
  await p.keyboard.press("Digit3");
  v = await ver();
  R2.ordem_so_na_selecao = Object.entries(v.ordens).every(([id, o]) => (v.tipos[id] === "arqueiro") === (o === "defender"));
  await p.keyboard.press("F3");
  R2.f3_indisponivel = (await p.textContent("#faixa")).includes("F3");
  // Shift + arrasto em volta dos soldados da metade de cima
  const caixa = await p.evaluate(() => {
    const m = __campo.mundo(), s = m.lados[0].filter((u) => u.tipo === "soldado" && u.y < 280);
    return [Math.min(...s.map((u) => u.x)) - 4, Math.min(...s.map((u) => u.y)) - 10, Math.max(...s.map((u) => u.x)) + 4, 279 - 4, s.length];
  });
  const [ax, ay] = await tela(caixa[0], caixa[1]), [bx, by] = await tela(caixa[2], caixa[3]);
  await p.keyboard.down("Shift");
  await p.mouse.move(ax, ay); await p.mouse.down(); await p.mouse.move((ax + bx) / 2, (ay + by) / 2, { steps: 4 }); await p.mouse.move(bx, by, { steps: 4 });
  await p.screenshot({ path: path.join(CAPT, "selecao-arrasto-1280.png") });
  await p.mouse.up();
  await p.keyboard.up("Shift");
  v = await ver();
  R2.arrasto_seleciona = v.sel.length > 5 && v.sel.every((id) => v.tipos[id] === "soldado");
  R2.arrasto_selecionados = v.sel.length;
  R2.arrasto_nao_ataca = v.usosBasico === 0;
  await p.keyboard.press("Digit2");
  v = await ver();
  R2.duas_ordens = { defender: Object.values(v.ordens).filter((o) => o === "defender").length, atacar: Object.values(v.ordens).filter((o) => o === "atacar").length,
    acompanhar: Object.values(v.ordens).filter((o) => o === "acompanhar").length };
  await p.waitForTimeout(1500);
  await p.screenshot({ path: path.join(CAPT, "duas-ordens-1280.png") });
  await p.keyboard.press("KeyX");
  R2.x_limpa = (await ver()).sel.length === 0;
  // pausado: o arrasto seleciona sem Shift; F4 todos
  await p.keyboard.press("KeyP");
  await p.mouse.move(ax, ay); await p.mouse.down(); await p.mouse.move(bx, by, { steps: 5 }); await p.mouse.up();
  v = await ver();
  R2.pausado_arrasta = v.sel.length > 5;
  await p.keyboard.press("F4");
  R2.f4_todos = (await ver()).sel.length === 42;
  await p.keyboard.press("Digit1");
  v = await ver();
  R2.pausado_ordena = Object.values(v.ordens).every((o) => o === "acompanhar");
  await p.keyboard.press("KeyP");
  // o tremor: com trauma 1 e intensidade 150%, o ponto do mundo sob o mouse é o mesmo
  await p.keyboard.press("KeyX");
  const semTremor = await p.evaluate(() => __campo.mouseMundo());
  const comTremor = await p.evaluate(() => { __campo.efeitos().trauma = 1; __campo.configurar({ tremor: 150 }); return new Promise((ok) => requestAnimationFrame(() => ok(__campo.mouseMundo()))); });
  R2.mira_igual_no_tremor = Math.abs(semTremor.x - comTremor.x) < 2 && Math.abs(semTremor.y - comTremor.y) < 2;
  // o mesmo arrasto, pausado (a câmera parada), sem e com o tremor no máximo: as mesmas tropas
  await p.keyboard.press("KeyP");
  const c2 = await p.evaluate(() => { const s = __campo.mundo().lados[0].filter((u) => u.tipo === "soldado"); return [Math.min(...s.map((u) => u.x)) - 4, Math.min(...s.map((u) => u.y)) - 10, Math.max(...s.map((u) => u.x)) + 4, 280]; });
  const [cx0, cy0] = await tela(c2[0], c2[1]), [cx1, cy1] = await tela(c2[2], c2[3]);
  const arrastar = async () => { await p.mouse.move(cx0, cy0); await p.mouse.down(); await p.mouse.move(cx1, cy1, { steps: 5 }); await p.mouse.up(); return (await ver()).sel.sort(); };
  await p.evaluate(() => { __campo.efeitos().trauma = 0; });
  const semT = await arrastar();
  await p.keyboard.press("KeyX");
  await p.evaluate(() => { __campo.efeitos().trauma = 1; });
  const comT = await arrastar();
  R2.arrasto_no_tremor = { sem: semT.length, com: comT.length, iguais: JSON.stringify(semT) === JSON.stringify(comT) };
  await p.keyboard.press("KeyP");
  R2.atalhos_do_navegador = paginas() === 1;
  R.selecao = R2;
  console.log("seleção", R2);
  await p.close();
}

// ---------------------------------------------------------------------------------------------- desempenho
if (quer("desempenho")) {
  R.desempenho = [];
  for (const [w, h] of [[1280, 720], [1920, 945]]) for (const qtd of ["normal", "maior"]) for (const [heroi, enc] of [["guerreiro", "original"], ["mago", "capitao"]]) {
    const p = await nav.newPage({ viewport: { width: w, height: h } });
    espiar(p, `desempenho ${w} ${qtd} ${heroi} ${enc}`);
    await p.goto(`${ENDERECO}?heroi=${heroi}&qtd=${qtd}&enc=${enc}&auto=1&robo=1`);
    let maxU = 0, maxP = 0;
    for (let i = 0; i < 20; i++) {
      await p.waitForTimeout(1000);
      const d = await p.evaluate(() => __campo.diagnostico());
      maxU = Math.max(maxU, d.unidades); maxP = Math.max(maxP, d.particulas);
    }
    const d = await p.evaluate(() => __campo.diagnostico());
    const linha = { janela: `${w}×${h}`, tropas: qtd, heroi, encontro: enc, unidades_max: maxU, particulas_max: maxP,
      qps: +d.fps.toFixed(1), quadro_p95_ms: +d.quadroP95.toFixed(1), quadro_max_ms: +d.quadroMax.toFixed(1),
      sim_media_ms: +d.simMedio.toFixed(2), sim_p95_ms: +d.simP95.toFixed(2), desenho_media_ms: +d.desenhoMedio.toFixed(2),
      desenho_p95_ms: +d.desenhoP95.toFixed(2), escala: d.escala, campo_visivel: `${d.W}×${d.H}` };
    R.desempenho.push(linha);
    console.log("desempenho", JSON.stringify(linha));
    await p.close();
  }
}

// ---------------------------------------------------------------------------------------------- capturas
if (quer("capturas")) {
  for (const [w, h] of [[1280, 720], [1920, 945]]) {
    const p = await nav.newPage({ viewport: { width: w, height: h } });
    espiar(p, `capturas ${w}`);
    await p.goto(ENDERECO);
    await p.waitForTimeout(500);
    await p.screenshot({ path: path.join(CAPT, `inicio-${w}.png`) });
    for (const [heroi, enc, kit] of [["guerreiro", "original", ""], ["mago", "original", ""], ["guerreiro", "capitao", ""],
      ["mago", "espalhados", "ignicao,vortice,muralha,meteoros"], ["guerreiro", "duasFrentes", "corteSangrento,grito,ruptura,terremoto"]]) {
      await p.goto(`${ENDERECO}?heroi=${heroi}&enc=${enc}&hab=${kit}&auto=1&robo=1`);
      for (const t of [1.5, 7, 10, 14]) {
        await p.waitForFunction((tt) => __campo.mundo().t >= tt, t, { timeout: 30000 });
        await p.screenshot({ path: path.join(CAPT, `${enc}-${heroi}-${w}-${String(t).replace(".", "_")}s.png`) });
      }
      await p.waitForFunction(() => __campo.st.tela === "fim", null, { timeout: 120000 });
      await p.waitForTimeout(300);
      await p.screenshot({ path: path.join(CAPT, `${enc}-${heroi}-${w}-fim.png`) });
    }
    await p.goto(`${ENDERECO}?heroi=guerreiro&qtd=maior&auto=1&robo=1`);
    await p.waitForFunction(() => __campo.mundo().t >= 9, null, { timeout: 30000 });
    await p.screenshot({ path: path.join(CAPT, `maior-${w}-9s.png`) });
    await p.close();
  }
}

// ---------------------------------------------------------------------------------------------- sequências
// Quadro a quadro (o canvas nativo, ampliado 2×) a partir do contato de um golpe forte que pega um grupo: para ver a
// antecipação, o contato, a pausa, o arremesso, a poeira e o fogo sem depender do vídeo.
if (quer("sequencias")) {
  for (const [heroi, gatilho, rotulo, extra] of [["guerreiro", "varredura", "varredura", ""], ["guerreiro", "salto", "salto", ""],
    ["mago", "bola", "bola", ""], ["guerreiro", "lider", "lider", "&enc=capitao"]]) {
    const p = await nav.newPage({ viewport: { width: 1280, height: 720 } });
    espiar(p, `sequência ${rotulo}`);
    await p.goto(`${ENDERECO}?heroi=${heroi}&auto=1&robo=1${extra}`);
    const folha = await p.evaluate((gat) => new Promise((ok) => {
      const quadros = [], c = document.querySelector("#campo");
      let gravando = false, n = 0, foco = null, passoQ = 1, conta = 0;
      const laco = () => {
        const m = __campo.mundo(), h = m.heroi;
        if (!gravando && gat === "lider" && m.lider && m.lider.acao && m.lider.acao.tipo === "reunir") { gravando = true; foco = { x: m.lider.x + 40, y: m.lider.y }; passoQ = 3; }
        if (!gravando && h.acao && h.acao.id === gat && (h.acao.fase === "preparo" || h.acao.fase === "voo")) {
          const alvoX = h.acao.forma ? (h.acao.forma.x ?? h.x) : h.x;
          const perto = m.lados[1].filter((u) => Math.hypot(u.x - (gat === "varredura" ? h.x : alvoX), u.y - (gat === "varredura" ? h.y : h.acao.forma.y)) < 40).length;
          if (perto >= 4) gravando = true;
        }
        if (gravando && n < 30 && conta++ % passoQ === 0) {
          const k = document.createElement("canvas"); k.width = 220; k.height = 150;
          const g = k.getContext("2d"); g.imageSmoothingEnabled = false;
          if (!foco) { const hh = __campo.mundo().heroi, f = hh.acao && hh.acao.forma; foco = gat === "varredura" || !f ? { x: hh.x, y: hh.y } : { x: (f.x + hh.x) / 2, y: f.y }; }
          const hx = foco.x - __campo.st.cam.x, hy = foco.y - __campo.st.cam.y;
          g.drawImage(c, Math.round(hx - 110), Math.round(hy - 80), 220, 150, 0, 0, 220, 150);
          quadros.push({ k, t: __campo.mundo().t, pausa: performance.now() < __campo.st.pausaAte });
          n++;
        }
        if (n >= 30) {
          const Z = 2, col = 6, F = document.createElement("canvas");
          F.width = 220 * Z * col; F.height = 150 * Z * Math.ceil(quadros.length / col);
          const g = F.getContext("2d"); g.imageSmoothingEnabled = false; g.font = "16px sans-serif";
          quadros.forEach((q, i) => {
            const x = (i % col) * 220 * Z, y = Math.floor(i / col) * 150 * Z;
            g.drawImage(q.k, x, y, 220 * Z, 150 * Z);
            g.fillStyle = "#000"; g.fillRect(x, y, 150, 20);
            g.fillStyle = q.pausa ? "#ff8" : "#fff"; g.fillText(`${i} · t ${q.t.toFixed(3)}${q.pausa ? " · pausa" : ""}`, x + 4, y + 15);
            g.strokeStyle = "#000"; g.strokeRect(x, y, 220 * Z, 150 * Z);
          });
          ok(F.toDataURL("image/png"));
          return;
        }
        requestAnimationFrame(laco);
      };
      requestAnimationFrame(laco);
    }), gatilho);
    fs.writeFileSync(path.join(CAPT, `sequencia-${rotulo}.png`), Buffer.from(folha.split(",")[1], "base64"));
    console.log("sequência", rotulo);
    await p.close();
  }
}

// ---------------------------------------------------------------------------------------------- vídeos
if (quer("videos")) {
  fs.mkdirSync(VIDS, { recursive: true });
  // os três primeiros com o jogador automático; o da seleção com teclado e mouse de verdade (roteiro abaixo)
  for (const [nome, q, dur] of [["area-numeros-mago", "heroi=mago", 24], ["area-numeros-guerreiro", "heroi=guerreiro", 20],
    ["lider-capitao", "heroi=guerreiro&enc=capitao", 40], ["selecao-e-duas-ordens", "heroi=guerreiro&enc=duasFrentes", 0]]) {
    const ctx = await nav.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: VIDS, size: { width: 1280, height: 720 } } });
    const p = await ctx.newPage();
    espiar(p, `video ${nome}`);
    await p.goto(`${ENDERECO}?${q}&auto=1${dur ? "&robo=1" : ""}`);
    if (dur) await p.waitForTimeout(dur * 1000);
    else await roteiroSelecao(p);
    const v = p.video();
    await ctx.close();
    const destino = path.join(VIDS, `${nome}-1280x720.webm`);
    if (fs.existsSync(destino)) fs.unlinkSync(destino);
    fs.renameSync(await v.path(), destino);
    console.log("vídeo", destino);
  }
}

R.erros = erros;

// O roteiro do vídeo da seleção: F2 (arqueiros) e Defender um ponto ao norte; Shift + arrasto nos soldados do oeste e
// Atacar; pausa, F4 e Acompanhar; e o herói andando entre uma coisa e outra.
async function roteiroSelecao(p) {
  const tela = (x, y) => p.evaluate(([x, y]) => { const st = __campo.st; return [(x - st.cam.x) * st.escala, (y - st.cam.y) * st.escala]; }, [x, y]);
  await p.waitForTimeout(1500);
  await p.keyboard.press("F2");
  await p.waitForTimeout(900);
  let [x, y] = await tela(480, 130);
  await p.mouse.move(x, y, { steps: 10 });
  await p.waitForTimeout(400);
  await p.keyboard.press("Digit3");
  await p.waitForTimeout(1500);
  const c = await p.evaluate(() => { const s = __campo.mundo().lados[0].filter((u) => u.tipo === "soldado" && u.x < 488); return [Math.min(...s.map((u) => u.x)) - 5, Math.min(...s.map((u) => u.y)) - 12, Math.max(...s.map((u) => u.x)) + 5, Math.max(...s.map((u) => u.y)) + 4]; });
  const [ax, ay] = await tela(c[0], c[1]), [bx, by] = await tela(c[2], c[3]);
  await p.keyboard.down("Shift");
  await p.waitForTimeout(500);
  await p.mouse.move(ax, ay, { steps: 8 }); await p.mouse.down(); await p.mouse.move(bx, by, { steps: 20 });
  await p.waitForTimeout(300); await p.mouse.up();
  await p.keyboard.up("Shift");
  await p.waitForTimeout(700);
  [x, y] = await tela(200, 280);
  await p.mouse.move(x, y, { steps: 10 });
  await p.keyboard.press("Digit2");
  await p.waitForTimeout(400);
  await p.keyboard.down("KeyD"); await p.waitForTimeout(900); await p.keyboard.up("KeyD");
  await p.mouse.down(); await p.waitForTimeout(1500); await p.mouse.up();
  await p.waitForTimeout(4000);
  await p.keyboard.press("KeyP");
  await p.waitForTimeout(1200);
  await p.keyboard.press("F4");
  await p.waitForTimeout(900);
  await p.keyboard.press("Digit1");
  await p.waitForTimeout(1200);
  await p.keyboard.press("KeyP");
  await p.keyboard.down("KeyA"); await p.waitForTimeout(800); await p.keyboard.up("KeyA");
  await p.waitForTimeout(5000);
}
fs.writeFileSync(saidaJson, JSON.stringify(R, null, 1));
console.log(erros.length ? "ERROS:\n" + erros.join("\n") : "sem erros no console");
await nav.close();
