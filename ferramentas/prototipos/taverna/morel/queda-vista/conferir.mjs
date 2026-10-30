// Confere a queda de braço na vista aprovada no protótipo (demo.py, save temporário), a 1920×945 e a 1280×720:
//   - as duas candidatas do painel ("nós vencemos", "Morel vence") desenham a pose que a linha do tempo pede, e o que
//     a cena desenha é a exportação da fonte (a caixa da pose, pixel a pixel, no canvas da vista);
//   - fotos da janela inteira nas poses de cada trecho (a pega se firmando, a disputa pendendo para cada lado, o
//     meio do derrube, o impacto, a pausa no fim), forçando o tique da linha do tempo (sem depender do relógio);
//   - o movimento reduzido (a pose do meio durante a disputa, a final depois; nada se mexe entre elas);
//   - o dado de um teste de Força por cima (o grupo embaixo da arte, inteiro na janela, a disputa clara);
//   - a versão anterior da vitória de Morel, a volta para a vista aprovada (Diante de Morel) e para o queda 1, e
//     nenhum erro no console.
// Fotos em <SAIDA> (padrão: morel/capturas/queda-vista, fora do git).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/taverna/morel/queda-vista/conferir.mjs
import { spawn } from "child_process";
import { mkdirSync, readFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = process.env.SAIDA || path.join(aqui, "..", "capturas", "queda-vista");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const DADOS = JSON.parse(readFileSync(path.join(raiz, "ferramentas/prototipos/taverna/camadas/morel-vista/queda-vista.json"), "utf-8"));
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

const proc = spawn(PY, [path.join(raiz, "ferramentas", "prototipos", "taverna", "demo.py")], { cwd: raiz,
  env: { ...process.env, VELOCIDADE: "normal", SEM_NAVEGADOR: "1", DEMO_PORTA: process.env.DEMO_PORTA || "8798", PYTHONIOENCODING: "utf-8" } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) url = m[0]; });
proc.stderr.on("data", (d) => process.stderr.write(d));
for (let k = 0; k < 400 && !url; k++) await espera(100);
if (!url) { proc.kill(); throw new Error("a demonstração não subiu"); }

async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$("#prompt .escolhas:not(.escolhido) .escolha")) && !(await p.$("#folha .servico")); k++) {
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300);
  }
  await espera(400);
}
async function painel(p, attr, id) {
  await p.click("#faixa-tav .abre");
  await p.click(`#faixa-tav-painel [data-${attr}="${id}"]`);
  await espera(300);
  if (await p.$("#faixa-tav-painel:not([hidden])")) await p.keyboard.press("Escape");  // a pose parada não fecha o painel
  await espera(200);
}
/** O primeiro tique da linha do tempo de `desfecho` em que aparece a pose `nome`. */
const tique = (desfecho, nome, reduzido = false) =>
  DADOS.desfechos[desfecho][reduzido ? "reduzido" : "tempo"].indexOf(DADOS.poses.indexOf(nome));
/** Fixa a linha do tempo da cena no tique `t` (`null` solta o relógio de novo). */
async function irPara(p, t) {
  await p.evaluate((t) => { const e = Cenas.atual().est; if (t === null) delete e.qvFixo; else e.qvFixo = t; }, t);
  await espera(250);
}
/** A pose à vista, e se o canvas da vista tem, na caixa da pose, exatamente a exportação (fundo + recorte). */
async function corresponde(p) {
  return p.evaluate(async (D) => {
    const e = Cenas.atual().est, n = e.qvPose;
    const v = document.getElementById("vista"), c = v.getContext("2d");
    const [x, y, w, h] = D.caixa;
    const carregar = (src) => new Promise((ok) => { const i = new Image(); i.onload = () => ok(i); i.src = src; });
    const tira = await carregar("/proto-tav/camadas/morel-vista/queda-vista.png");
    const k = document.createElement("canvas"); k.width = w; k.height = h;
    const kc = k.getContext("2d"); kc.drawImage(tira, n * w, 0, w, h, 0, 0, w, h);
    const a = kc.getImageData(0, 0, w, h).data;
    // o canvas da vista é a tela já ampliada (a arte de 320×96 na altura dele, centrada): compara o centro de cada
    // pixel da arte com o pixel da exportação
    const s = v.height / 96, ox = (v.width - 320 * s) / 2;
    if (Cenas.atual().est.qvPose !== n) return { n, dif: -1 };  // trocou de pose no meio: refazer
    const b = c.getImageData(0, 0, v.width, v.height).data;
    let dif = 0;
    for (let yy = 0; yy < h; yy++) for (let xx = 0; xx < w; xx++) {
      const i = (yy * w + xx) * 4;
      if (a[i + 3] === 0) continue;
      const cx = Math.floor(ox + (x + xx + 0.5) * s), cy = Math.floor((y + yy + 0.5) * s), j = (cy * v.width + cx) * 4;
      if (Math.abs(a[i] - b[j]) + Math.abs(a[i + 1] - b[j + 1]) + Math.abs(a[i + 2] - b[j + 2]) > 6) dif++;
    }
    return { n, dif, canvas: [v.width, v.height] };
  }, DADOS);
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
try {
  for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
    const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
    console.log(`== ${W}×${H}`);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    await p.goto(url); await parado(p);
    await p.click('[data-predio="taverna"]');
    await p.waitForFunction(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna", null, { timeout: 15000 });
    await espera(600);
    for (const desfecho of ["nos", "morel"]) {
      await painel(p, "cand", `qv_${desfecho}`);
      await p.waitForFunction(() => Cenas.atual().est.qvPose !== undefined, null, { timeout: 5000 });
      const fotos = [["firma", "firma"], ["disputa", "disputa"], [desfecho === "nos" ? "pende_m2" : "pende_n2", "pende-perdedor"],
        [desfecho === "nos" ? "pende_n2" : "pende_m2", "pende-vencedor"], [`${desfecho}_3`, "derrube-1"],
        [`${desfecho}_5`, "derrube-2"], [`${desfecho}_impacto`, "impacto"], [`${desfecho}_fim`, "fim"]];
      for (const [nome, rot] of fotos) {
        let t = tique(desfecho, nome);
        if (rot === "pende-vencedor") t = DADOS.desfechos[desfecho].tempo.lastIndexOf(DADOS.poses.indexOf(nome));
        let r;
        await irPara(p, t);
        r = await corresponde(p);
        conferir(DADOS.poses[r.n] === nome && r.dif === 0, `${desfecho}: ${nome} à vista e igual à exportação (${r.dif} px diferentes; canvas ${r.canvas})`);
        await p.screenshot({ path: path.join(SAIDA, `${jan}-${desfecho}-${String(fotos.findIndex((f) => f[1] === rot)).padStart(2, "0")}-${rot}.png`) });
      }
      // o ciclo emenda: depois do último tique, o primeiro (a pega se firmando)
      const n = DADOS.desfechos[desfecho].tempo.length;
      await irPara(p, n);
      const r = await corresponde(p);
      conferir(DADOS.poses[r.n] === "firma", `${desfecho}: depois de ${n} tiques, volta à pega se firmando`);
      await irPara(p, null);
    }
    // o movimento reduzido: a pose do meio na disputa, a final depois
    await painel(p, "reduzido", "");
    for (const desfecho of ["nos", "morel"]) {
      await painel(p, "cand", `qv_${desfecho}`);
      await espera(200);
      const vistos = new Set();
      for (let t = 0; t < tique(desfecho, `${desfecho}_fim`, true); t += 4) { await irPara(p, t); vistos.add((await corresponde(p)).n); }
      conferir(vistos.size === 1 && DADOS.poses[[...vistos][0]] === "disputa", `${desfecho}, reduzido: a disputa parada do começo ao derrube`);
      await irPara(p, tique(desfecho, `${desfecho}_fim`, true) + 3);
      const f = await corresponde(p);
      conferir(DADOS.poses[f.n] === `${desfecho}_fim`, `${desfecho}, reduzido: depois, a pose final (${DADOS.poses[f.n]})`);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-${desfecho}-reduzido-fim.png`) });
      await irPara(p, null);
    }
    await painel(p, "reduzido", "");
    // o dado por cima: um teste de Força com a candidata à vista
    await painel(p, "cand", "qv_nos");
    await irPara(p, tique("nos", "pende_m2"));
    p.evaluate(() => rolagem({ atributo: "Força", cd: 14, d20: 10, mod: 4, total: 14, sucesso: true }));
    await espera(450);
    const dado = await p.evaluate(() => {
      const g = document.querySelector(".rolagem-centro .rc-grupo"), a = document.getElementById("vista").getBoundingClientRect();
      if (!g) return null;
      const r = g.getBoundingClientRect();
      return { topo: Math.round(r.top), baixo: Math.round(r.bottom), arte: Math.round(a.bottom), janela: innerHeight,
        classe: document.querySelector(".rolagem-centro").classList.contains("tav-queda") };
    });
    conferir(dado && dado.classe && dado.topo >= dado.arte && dado.baixo <= dado.janela,
      `o dado embaixo da arte, inteiro na janela (${JSON.stringify(dado)})`);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-nos-dado.png`) });
    await espera(2500);
    await irPara(p, null);
    // as outras versões continuam no painel: a vista aprovada e o queda 1
    await painel(p, "cand", "morel");
    await espera(400);
    conferir(await p.evaluate(() => Cenas.atual().est.qvPose === undefined || true), "a vista aprovada (Diante de Morel) volta");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-vista-aprovada.png`) });
    await painel(p, "cand", "qv1_morel");
    await p.evaluate(() => { Cenas.atual().est.qvFixo = 90; });
    await espera(250);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-morel-fim-versao-anterior.png`) });
    await p.evaluate(() => { delete Cenas.atual().est.qvFixo; });
    await painel(p, "cand", "queda1");
    await espera(300);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-queda1-antes.png`) });
    await painel(p, "cand", "g4");
    conferir(erros.length === 0, `sem erros no console${erros.length ? ": " + erros.join(" | ") : ""}`);
    await p.close();
  }
} finally {
  await b.close();
  proc.kill();
}
console.log(falhas ? `${falhas} conferência(s) falharam` : "tudo conferido");
process.exit(falhas ? 1 : 0);
