// Confere a taverna no jogo (1.220.0), pela entrada normal da vila, num servidor novo por caso (tests.navegador.cenarios
// taverna: o Vau com Morel à espera; OURO e DADO, o d20 só do teste de Força do encontro):
//   - o balcão: a cena da taverna com o taverneiro animado e o ponto dele;
//   - pagar 40: uma cobrança só (clique duplo e tecla repetida), um lançamento de moedas, a reação de Morel, e de volta
//     ao balcão depois do encontro;
//   - a queda de braço perdida (DADO=1) com 30 de ouro: a preparação, o dado só depois da pega firmada (e embaixo da
//     arte), o desfecho de Morel antes do texto dele, a pergunta dos 25, as moedas na composição de depois;
//   - perdida com 10 de ouro: sem a pergunta dos 25; vencida (DADO=20): o nosso desfecho, sem moedas;
//   - o Vazio: sem queda nem moedas; o movimento reduzido: a mesma ordem, com poses paradas;
//   - as duas janelas (1920×945 e 1280×720) e o console.
// Fotos em <SAIDA> (padrão: tests/navegador/capturas-taverna, fora do git).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node tests/navegador/taverna.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), RAIZ = path.resolve(aqui, "../..");
const SAIDA = process.env.SAIDA || path.join(aqui, "capturas-taverna");
mkdirSync(SAIDA, { recursive: true });
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

async function subir(ambiente) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "taverna"], { cwd: RAIZ,
    env: { ...process.env, VELOCIDADE: "rapido", ...ambiente, PYTHONPATH: RAIZ, PYTHONIOENCODING: "utf-8" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(d));
  for (let k = 0; k < 200 && !url; k++) await espera(100);
  if (!url) { proc.kill(); throw new Error("o cenário da taverna não subiu"); }
  return { proc, url };
}

const ouro = (p) => p.evaluate(() => App.estado.heroi.ouro);
const cena = (p) => p.evaluate(() => { const a = window.Cenas && Cenas.atual(); return a ? { cena: a.d.cena, titulo: a.d.titulo,
  pagamentos: a.d.pagamentos || 0, lances: (a.est.lances || []).length, queda: a.d.queda || null, pose: a.est.qcPose || null,
  pontos: (a.d.pontos || []).map((x) => x.id) } : null; });
const opcoes = (p) => p.$$eval(MENU, (es) => es.map((e) => e.textContent.replace(/\s+/g, " ").trim()));
const cartoes = (p) => p.$$eval("#folha .servico", (es) => es.map((e) => e.dataset.servico));
async function parado(p) {  // até haver o que escolher (o menu ou os cartões do balcão), passando os Continuar
  for (let k = 0; k < 120 && !(await p.$(MENU)) && !(await p.$("#folha .servico")); k++) {
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(250);
  }
  await espera(300);
}
const naCena = (p, nome, ms = 15000) => p.waitForFunction((n) => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === n,
  nome, { timeout: ms }).then(() => true, () => false);
async function naPose(p, nome, ms = 20000) {
  for (let k = 0; k < ms / 100; k++) {
    if (await p.evaluate((n) => { const a = window.Cenas && Cenas.atual(); return !!a && a.est.qcPose === n; }, nome)) return true;
    await espera(100);
  }
  return false;
}
async function balcao(p) {  // entra na taverna pela vila: o balcão com o interior
  await parado(p);
  await p.waitForSelector('#predios .predio[data-predio="taverna"]', { timeout: 20000 });
  await p.click('#predios .predio[data-predio="taverna"]');
  return naCena(p, "taverna");
}
async function sentar(p) {
  const card = await p.$('#folha .servico[data-servico="morel"]');
  if (!card) return false;
  await card.click();
  return (await naCena(p, "taverna_mesa")) && !!(await p.waitForSelector(MENU, { timeout: 15000 }).catch(() => null));
}
async function escolher(p, ini, duplo = false) {
  const i = (await opcoes(p)).findIndex((t) => t.includes(ini));
  if (i < 0) return false;
  const el = (await p.$$(MENU))[i];
  if (duplo) { await el.dblclick(); await p.keyboard.press(String(i + 1)); await p.keyboard.press(String(i + 1)); } else await el.click();
  return true;
}
/** Acompanha a queda de braço até as próximas opções: a pose quando o dado aparece, onde ele fica, a pose quando o
 *  texto do desfecho chega. */
async function acompanharQueda(p) {
  return p.evaluate(() => new Promise((fim) => {
    const r = { dado: null, poseNoDado: null, poseNoTexto: null, rolagens: 0 };
    const vistos = new Set(), limite = performance.now() + 60000;
    const olhar = () => {
      if (performance.now() > limite) { r.esgotou = true; return fim(r); }
      const a = Cenas.atual(), pose = a && a.est.qcPose;
      const rc = document.querySelector(".rolagem-centro");
      if (rc && !vistos.has(rc)) {
        vistos.add(rc); r.rolagens++;
        if (!r.dado) {
          r.poseNoDado = pose;
          const g = rc.querySelector(".rc-grupo").getBoundingClientRect(), v = rc.querySelector(".rc-veu").getBoundingClientRect();
          const arte = document.getElementById("vista").getBoundingClientRect();
          r.dado = { inteiro: g.top >= 0 && g.bottom <= innerHeight && g.left >= 0 && g.right <= innerWidth,
            embaixo: g.top >= arte.bottom - 1, veu: v.top >= arte.bottom - 1 };
        }
      }
      const t = document.getElementById("texto").textContent;
      if (r.poseNoTexto === null && /bate na mesa/.test(t)) r.poseNoTexto = pose;
      if (document.querySelector("#prompt .escolhas:not(.escolhido) .escolha") || document.querySelector("#prompt .continuar")
        || document.querySelector("#folha .servico")) {
        if (r.poseNoTexto !== null || r.rolagens) return fim(r);
      }
      setTimeout(olhar, 40);
    };
    olhar();
  }));
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const servidores = [];
async function pagina(W, H, ambiente, reduzido = false) {
  const s = await subir(ambiente); servidores.push(s.proc);
  const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: reduzido ? "reduce" : "no-preference" });
  p.erros = []; p.on("pageerror", (e) => p.erros.push(String(e)));
  p.on("console", (m) => { if (m.type() === "error") p.erros.push(m.text()); });
  await p.goto(s.url);
  p.proc = s.proc;
  return p;
}
async function fechar(p) { conferir(!p.erros.length, `o console sem erro${p.erros.length ? ": " + p.erros.join(" | ") : ""}`); await p.close(); p.proc.kill(); }

try {
  for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
    const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
    console.log(`== ${W}×${H}`);

    // 1. o balcão e o pagamento dos 40
    const caso = (n) => !process.env.CASOS || process.env.CASOS.split(",").includes(String(n));
    let p, c, ops;
    if (caso(1)) {
    p = await pagina(W, H, { OURO: "60", DESPENSA: "adiada" });
    conferir(await balcao(p), "a taverna pela vila: a cena do balcão");
    c = await cena(p);
    conferir(c.pontos.join() === "taverneiro,despensa", `os pontos que a cena desenha: o Taverneiro e a Despensa (${c.pontos})`);
    const v1 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    await espera(900);
    conferir(v1 !== await p.evaluate(() => document.getElementById("vista").toDataURL()), "o balcão se mexe (o taverneiro, o fogo)");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-balcao.png`) });
    await p.click('#pontos-cena .ci-ponto[data-ponto="taverneiro"]').catch(() => {});
    await espera(300);
    conferir(await p.evaluate(() => { const e = document.activeElement; return !!e && e.dataset.servico === "rumores"; }),
      "o Taverneiro leva ao cartão da bebida");
    await p.close(); p.proc.kill();

    p = await pagina(W, H, { OURO: "60" });
    await balcao(p);
    conferir((await cartoes(p)).includes("morel"), "o cartão Sentar com o homem do canto no balcão");
    conferir(await sentar(p), "sentar com o homem do canto abre a mesa de Morel");
    c = await cena(p);
    conferir(c.titulo === "A mesa do homem do canto", `a mesa do homem do canto (${c.titulo})`);
    ops = await opcoes(p);
    conferir(ops.some((t) => t.includes("Pagar 40")) && ops.some((t) => t.includes("Queda de braço")) && ops.some((t) => t.includes("Vazio"))
      && ops.some((t) => t.includes("Recusar")), "as quatro opções do evento");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa.png`) });
    await escolher(p, "Pagar 40", true);
    await espera(450);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-40-voando.png`) });
    await parado(p);
    c = await cena(p);
    conferir(await ouro(p) === 20 && c.pagamentos === 1 && c.lances === 1, `pagar 40: 60 → ${await ouro(p)}, um pagamento, um lance (${c.pagamentos}, ${c.lances})`);
    await espera(1500);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-40-assentadas.png`) });
    await escolher(p, "Aceitar");
    await parado(p);
    conferir((await cena(p)).cena === "taverna" && !!(await p.$("#prompt .voltar-vila")), "depois do encontro, o balcão da taverna continua aberto");
    conferir(!(await cartoes(p)).includes("morel") && await ouro(p) === 20, `recrutado: sem o cartão dele, nada cobrado de novo (${await ouro(p)})`);
    await p.click("#prompt .voltar-vila"); await espera(600);
    conferir(!(await cena(p)) && !!(await p.$('#predios .predio[data-predio="mercado"]')), "Voltar à vila: a praça, sem cena");
    await fechar(p);

    }

    // 2. a queda de braço perdida, com 30 de ouro: a pega, o dado, o desfecho, os 25
    if (caso(2)) {
    p = await pagina(W, H, { OURO: "30", DADO: "1" });
    await balcao(p);
    await sentar(p);
    ops = await opcoes(p);
    conferir(!ops.some((t) => t.includes("Pagar 40")), "com 30 de ouro, sem a opção dos 40");
    await escolher(p, "Queda de braço", true);
    const q = await acompanharQueda(p);
    conferir(q.rolagens === 1, `uma rolagem só, com clique duplo e tecla repetida (${q.rolagens})`);
    conferir(["firma", "disputa", "pende_m1", "pende_n1"].includes(q.poseNoDado), `o dado aparece com a pega firmada (${q.poseNoDado})`);
    conferir(q.dado && q.dado.inteiro && q.dado.embaixo && q.dado.veu, `o dado inteiro, embaixo da arte, o véu fora dela (${JSON.stringify(q.dado)})`);
    conferir(["morel_fim", "morel_solta", "morel_sai", "depois"].includes(q.poseNoTexto), `o texto da derrota depois do derrube (${q.poseNoTexto})`);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-queda-morel-vence.png`) });
    await parado(p);
    ops = await opcoes(p);
    conferir(ops.some((t) => t.includes("Pagar 25")) && ops.some((t) => t.includes("Recusar")), "perdeu: a pergunta dos 25, com o Recusar");
    conferir((await cena(p)).lances === 0, "nenhuma moeda antes de pagar");
    await escolher(p, "Pagar 25", true);
    await espera(450);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-25-voando.png`) });
    await parado(p);
    c = await cena(p);
    conferir(await ouro(p) === 5 && c.pagamentos === 1 && c.lances === 1, `pagar 25: 30 → ${await ouro(p)}, um lance (${c.lances})`);
    conferir(c.queda === "morel" && ["morel_fim", "morel_solta", "morel_sai", "depois"].includes(c.pose), `as moedas na composição de depois da disputa (${c.pose})`);
    await naPose(p, "depois", 6000); await espera(1200);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-25-assentadas.png`) });
    await escolher(p, "Recusar");
    await parado(p);
    conferir((await cena(p)).cena === "taverna" && await ouro(p) === 5, `de volta ao balcão, sem outra cobrança (${await ouro(p)})`);
    await fechar(p);

    }

    // 3. perdida sem os 25; 4. vencida; 5. o Vazio
    if (caso(3)) {
    p = await pagina(W, H, { OURO: "10", DADO: "1" });
    conferir(await balcao(p) && await sentar(p), "10 de ouro: senta com o homem do canto");
    await escolher(p, "Queda de braço");
    const s3 = await acompanharQueda(p);
    conferir(!s3.esgotou && ["morel_fim", "morel_solta", "morel_sai", "depois"].includes(s3.poseNoTexto), `perdeu: o texto depois do derrube (${JSON.stringify(s3)})`);
    await parado(p);
    conferir((await cena(p)).cena === "taverna" && await ouro(p) === 10, "perdeu sem os 25: nada cobrado, de volta ao balcão");
    await fechar(p);
    }

    if (caso(4)) {
    p = await pagina(W, H, { OURO: "60", DADO: "20" });
    await balcao(p); await sentar(p);
    await escolher(p, "Queda de braço");
    const v = await acompanharQueda(p);
    conferir(["nos_fim", "nos_solta", "nos_sai", "depois"].includes(v.poseNoTexto), `venceu: o texto depois do nosso derrube (${v.poseNoTexto})`);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-queda-nos-vencemos.png`) });
    await parado(p);
    c = await cena(p);
    conferir((await opcoes(p)).some((t) => t.includes("Aceitar")) && c.lances === 0 && await ouro(p) === 60, "venceu: a vaga, sem moedas nem cobrança");
    await fechar(p);
    }

    if (caso(5)) {
    p = await pagina(W, H, { OURO: "60" });
    await balcao(p); await sentar(p);
    await escolher(p, "Vazio");
    await espera(300);
    conferir(!(await cena(p)).queda, "o Vazio: sem preparação nem disputa");
    await parado(p);
    if ((await opcoes(p)).some((t) => t.includes("Aceitar"))) { await escolher(p, "Recusar"); await parado(p); }
    c = await cena(p);
    conferir(c && c.lances === 0 && await ouro(p) === 60, "o Vazio: sem moedas nem cobrança");
    await fechar(p);
    }

    // 6. o movimento reduzido: a mesma ordem, parada (a pega, o dado, o fim, a opção)
    if (caso(6)) {
    p = await pagina(W, H, { OURO: "30", DADO: "1" }, true);
    await balcao(p); await sentar(p);
    await escolher(p, "Queda de braço");
    const r = await acompanharQueda(p);
    conferir(r.rolagens === 1 && r.poseNoDado === "disputa" && r.poseNoTexto === "morel_fim", `reduzido: a disputa parada no dado, o fim parado no texto (${r.poseNoDado}, ${r.poseNoTexto})`);
    await parado(p);
    conferir((await opcoes(p)).some((t) => t.includes("Pagar 25")), "reduzido: a opção dos 25 chega");
    await escolher(p, "Pagar 25");
    await parado(p);
    const f1 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    await espera(700);
    conferir(f1 === await p.evaluate(() => document.getElementById("vista").toDataURL()) && (await cena(p)).lances === 1,
      "reduzido: as moedas assentadas e nada se mexe");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-reduzido-25.png`) });
    await fechar(p);
    }
  }
} finally {
  await b.close();
  servidores.forEach((s) => s.kill());
}
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
