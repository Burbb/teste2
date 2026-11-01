// As conferências do Campo Livre 4 no navegador (Playwright, Chromium sem janela), com teclado e mouse de verdade:
// a ordem de atacar um alvo (Shift + botão direito num inimigo), a marca do alvo do básico, o golpe no herói, a horda
// (a tecla H) com o custo de uma batalha grande, e capturas pontuais. Precisa do servidor no ar:
//   PLAYWRIGHT_MODULO=file:///.../playwright/index.mjs CAMPO_URL=http://127.0.0.1:8802/ node ferramentas/conferir4.mjs [partes]
// partes: alvo, golpe, horda (sem nada, todas). Escreve no terminal e em capturas/conferir4.json (somando ao que já há).
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
const saidaJson = path.join(CAPT, "conferir4.json");
const R = fs.existsSync(saidaJson) ? JSON.parse(fs.readFileSync(saidaJson, "utf-8")) : {}, erros = [];
const espiar = (p, rot) => {
  p.on("pageerror", (e) => erros.push(`${rot}: ${e.message}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${rot}: ${m.text()}`); });
};
// o ponto da tela (CSS px) de um ponto do campo
const naTela = (p, x, y) => p.evaluate(([x, y]) => { const s = __campo.st; return { x: (x - s.cam.x) * s.escala, y: (y - s.cam.y) * s.escala }; }, [x, y]);

if (quer("alvo")) {
  const p = await nav.newPage({ viewport: { width: 1920, height: 945 } });
  espiar(p, "alvo");
  await p.goto(`${ENDERECO}?heroi=mago&enc=original&auto=1`);
  await p.waitForTimeout(8000);
  await p.keyboard.press("KeyP");   // pausado: o mouse comanda e o alvo fica parado para o clique
  await p.keyboard.press("F2");
  // o alvo: o veterano inimigo mais perto do herói que está na tela
  const est = await p.evaluate(() => {
    const s = __campo.st, m = __campo.mundo(), h = m.heroi;
    const naTela = (u) => u.x > s.cam.x + 10 && u.x < s.cam.x + s.W - 10 && u.y > s.cam.y + 20 && u.y < s.cam.y + s.H - 40;
    const e = m.lados[1].filter((u) => u.tipo === "veterano" && naTela(u)).sort((a, b) => Math.hypot(a.x - h.x, a.y - h.y) - Math.hypot(b.x - h.x, b.y - h.y))[0];
    return { id: e.id, x: e.x, y: e.y - 4 };
  });
  const ponto = await naTela(p, est.x, est.y);
  await p.mouse.move(ponto.x, ponto.y);
  await p.mouse.down({ button: "right" }); await p.mouse.up({ button: "right" });
  const ordem = await p.evaluate((id) => {
    const m = __campo.mundo(), arq = m.lados[0].filter((u) => u.tipo === "arqueiro");
    return { arqueiros: arq.length, noAlvo: arq.filter((u) => u.ordem.alvoU && u.ordem.alvoU.id === id).length,
      soldadosNoAlvo: m.lados[0].filter((u) => u.tipo === "soldado" && u.ordem.alvoU).length, placar: document.querySelector("#p-ordens").textContent,
      faixa: document.querySelector("#faixa").textContent };
  }, est.id);
  await p.screenshot({ path: path.join(CAPT, "cl4-alvo-ordem-1920.png") });
  await p.keyboard.press("KeyP");
  // até o alvo cair (ou 25 s): a ordem se encerra e eles voltam ao que tinham
  await p.waitForFunction((id) => !__campo.mundo().lados[1].some((u) => u.id === id) || __campo.mundo().t > 28, est.id, { timeout: 40000 });
  await p.waitForTimeout(300);
  const depois = await p.evaluate(() => {
    const m = __campo.mundo(), arq = m.lados[0].filter((u) => u.tipo === "arqueiro");
    return { comAlvo: arq.filter((u) => u.ordem.alvoU && !u.ordem.encerrada).length, ordens: [...new Set(arq.map((u) => u.ordem.tipo))],
      registro: m.registro.filter((r) => r.texto.includes("Ordem de atacar")).map((r) => r.texto) };
  });
  R.alvo = { ...ordem, depois };
  console.log("alvo", R.alvo);
  await p.close();
}

if (quer("golpe")) {
  // o golpe do Capitão no herói: a marca no anel, o número vermelho e a borda da tela (captura pausada no quadro dele)
  const p = await nav.newPage({ viewport: { width: 1920, height: 945 } });
  espiar(p, "golpe");
  await p.goto(`${ENDERECO}?heroi=guerreiro&enc=capitao&auto=1`);
  await p.evaluate(() => { window.__golpes = []; });
  // o herói parado perto do Capitão: o primeiro golpe dele (sem esquiva) é capturado
  await p.waitForTimeout(500);
  await p.evaluate(() => { const m = __campo.mundo(), h = m.heroi, l = m.lider; h.x = h.px = l.x - 60; h.y = h.py = l.y; });
  await p.waitForFunction(() => __campo.efeitos().golpeHeroi && __campo.efeitos().golpeHeroi.forca >= 0.9 && __campo.efeitos().golpeHeroi.t > 0.05, null, { timeout: 20000, polling: "raf" });
  await p.keyboard.press("KeyP");
  const g = await p.evaluate(() => ({ vida: __campo.mundo().heroi.vida, golpe: { ...__campo.efeitos().golpeHeroi }, borda: document.querySelector("#golpe").className,
    numeros: __campo.efeitos().numeros.filter((n) => n.tipo === "sofrido").map((n) => n.valor), dano: __campo.mundo().stats.liderHeroi }));
  R.golpe = g;
  console.log("golpe", g);
  await p.screenshot({ path: path.join(CAPT, "cl4-golpe-no-heroi-1920.png") });
  await p.close();
}

if (quer("horda")) {
  // a horda em 4×, com o jogador automático e H apertado algumas vezes: o custo da batalha grande
  R.horda = [];
  for (const [w, h] of [[1920, 945], [1280, 720]]) {
    const p = await nav.newPage({ viewport: { width: w, height: h } });
    espiar(p, `horda ${w}`);
    await p.goto(`${ENDERECO}?heroi=guerreiro&enc=horda&qtd=4&auto=1&robo=1`);
    await p.waitForTimeout(3000);
    for (let i = 0; i < 3; i++) { await p.keyboard.press("KeyH"); await p.waitForTimeout(400); }
    await p.evaluate(() => { const d = __campo.st.diag; d.quadros = []; d.sim = []; d.desenho = []; });
    let maxU = 0;
    for (let i = 0; i < 20; i++) { await p.waitForTimeout(1000); maxU = Math.max(maxU, await p.evaluate(() => __campo.mundo().unidades.length)); }
    const d = await p.evaluate(() => __campo.diagnostico()), z = await p.evaluate(() => ({ heroi: __campo.mundo().stats.abatesHeroi, maior: __campo.mundo().stats.maiorGolpe }));
    const r1 = (v) => +v.toFixed(2);
    R.horda.push({ janela: `${w}×${h}`, combatentes_max: maxU, qps: r1(d.fps), quadro_p95: r1(d.quadroP95), quadro_max: r1(d.quadroMax),
      sim_media: r1(d.simMedio), sim_p95: r1(d.simP95), desenho_media: r1(d.desenhoMedio), desenho_p95: r1(d.desenhoP95), derrubados_heroi: z.heroi, maior_golpe: z.maior });
    console.log("horda", R.horda[R.horda.length - 1]);
    if (w === 1920) await p.screenshot({ path: path.join(CAPT, "cl4-horda-4x-1920.png") });
    await p.close();
  }
}

R.erros = erros;
fs.writeFileSync(saidaJson, JSON.stringify(R, null, 2));
console.log(erros.length ? `erros: ${erros.join(" | ")}` : "sem erros no console");
await nav.close();
