// A fogueira na cena do topo (telas/acampamento.js e telas/fogueira.js), no jogo de verdade, em janela normal
// (1500×950) e baixa (1280×720), com movimento normal e reduzido. Fotografa e conta o que importa em cada caso:
//   - as três classes, sozinhas e com a comitiva mais cheia (dois na roda, um no acampamento, um ferido, o lobo);
//   - a Capela Afogada (o entorno desenhado), o Charco e o Bosque (a paisagem do lugar), de dia, no crepúsculo e na chuva;
//   - o mouse, o F4 e o teclado sobre um companheiro; deixar alguém no acampamento e levá-lo de volta; conversar;
//   - o Dormir (a paisagem volta), a entrada por exaustão, recarregar a página na fogueira (a cena volta igual);
//   - o tutorial com o D3 pendente (o quadro abaixo da cena, a haste no Dormir).
// Guarda em SAIDA (padrão: capturas-acampamento/, ao lado deste arquivo).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/arte/fotografar_acampamento.mjs
// (CHROMIUM=<executável>; SO=classes,lugares,interacoes,fluxos,tutorial)
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-acampamento"));
const SO = new Set((process.env.SO || "classes,lugares,interacoes,fluxos,tutorial").split(","));
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function subir(cenario, amb) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const fechar = async (p) => { for (let k = 0; k < 6; k++) { const e = await p.$(".orientacao:not([hidden]) .orientacao-entendi"); if (!e) break; await e.click().catch(() => {}); await espera(250); } };
async function abrir(nome, W, H, cenario, amb, { reduzido = false, manterOrientacao = false } = {}) {
  const { proc, url } = await subir(cenario, amb);
  const p = await b.newPage({ viewport: { width: W, height: H }, reducedMotion: reduzido ? "reduce" : "no-preference" });
  p.on("pageerror", (e) => erros.push(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon|404/.test(m.text())) erros.push(`${nome}: ${m.text()}`); });
  await p.goto(url);
  if (!amb.EXAUSTO) {
    await p.waitForSelector('#prompt .escolha:has-text("camp")', { timeout: 30000 });
    if (!manterOrientacao) await fechar(p);
    await (await p.$('#prompt .escolha:has-text("camp")')).click();
  }
  for (let k = 0; k < 80 && !(await p.$("#acampamento-pontos")); k++) {
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
    await espera(250);
  }
  await espera(1500);
  if (!manterOrientacao) await fechar(p);
  return { p, proc };
}
const foto = (p, nome) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
const topo = async (p, nome) => { const v = await p.$("#vista"); if (v) await p.screenshot({ path: path.join(SAIDA, `${nome}-topo.png`), clip: await v.boundingBox() }); };
const quem = (p) => p.evaluate(() => ({
  pontos: [...document.querySelectorAll("#acampamento-pontos [data-ponto]")].map((e) => e.dataset.ponto + (e.classList.contains("reserva") ? "(fica)" : "")).join(" "),
  rodape: ((document.querySelector(".fogueira-rodape") || document.querySelector(".tela.acampamento .dica-uso") || {}).innerText || "").replace(/\s+/g, " "),
  lugar: App.ultimaFogueira && App.ultimaFogueira.lugar,
}));
const JANELAS = [[1500, 950, "normal"], [1280, 720, "baixa"]];
for (const [W, H, jan] of JANELAS) {
  if (SO.has("classes")) for (const classe of ["guerreiro", "arqueiro", "mago"]) for (const [rot, amb] of [["sozinho", { COMITIVA: "", RESERVA: "" }],
    ["cheia", { COMITIVA: "morel,odete", RESERVA: "yara", FERIDO: "odete", ...(classe === "arqueiro" ? { FERA: "1" } : {}) }]]) {
    const nome = `${jan}-${classe}-${rot}`;
    const { p, proc } = await abrir(nome, W, H, "fogueira", { CLASSE: classe, LUGAR: "capela", ...amb });
    await foto(p, nome); await topo(p, nome);
    console.log(nome, JSON.stringify(await quem(p)));
    await p.close(); proc.kill();
  }
  if (SO.has("lugares")) for (const [rot, amb, reduzido] of [["charco", { LUGAR: "charco" }], ["bosque", { LUGAR: "bosque" }],
    ["capela-manha", { LUGAR: "capela", PERIODO: "0" }], ["capela-crepusculo", { LUGAR: "capela", PERIODO: "2" }],
    ["capela-chuva", { LUGAR: "capela", CLIMA: "chuva" }], ["charco-chuva", { LUGAR: "charco", CLIMA: "chuva" }],
    ["capela-reduzido", { LUGAR: "capela" }, true]]) {
    const nome = `${jan}-lugar-${rot}`;
    const { p, proc } = await abrir(nome, W, H, "fogueira", { CLASSE: "mago", ...amb }, { reduzido });
    await topo(p, nome);
    if (rot === "charco" || rot === "capela-reduzido") await foto(p, nome);
    console.log(nome, JSON.stringify(await quem(p)));
    await p.close(); proc.kill();
  }
  if (SO.has("interacoes")) {
    const nome = `${jan}-interacoes`;
    const { p, proc } = await abrir(nome, W, H, "fogueira", { CLASSE: "arqueiro", LUGAR: "capela", FERA: "1" });
    await p.hover('#acampamento-pontos [data-ponto="morel"]'); await espera(400); await topo(p, `${nome}-1-mouse`);
    await p.mouse.move(5, 5); await p.keyboard.press("F4"); await espera(500); await topo(p, `${nome}-2-f4`);
    await p.keyboard.press("F4"); await espera(1500);
    await p.focus('#acampamento-pontos [data-ponto="morel"]'); await p.keyboard.press("Tab"); await espera(400); await topo(p, `${nome}-3-teclado`);  // do Morel, o Tab vai à Odette
    await p.keyboard.press("Enter"); await espera(500); await foto(p, `${nome}-4-menu-pelo-teclado`);
    await p.keyboard.press("Escape"); await p.mouse.click(5, 5); await espera(300);
    await p.click('#acampamento-pontos [data-cid="morel"]'); await espera(400);
    await p.click('.menu-item button:has-text("Deixar no acampamento")'); await espera(1800); await fechar(p);
    await foto(p, `${nome}-5-morel-fica`); console.log(nome, "Morel deixado:", JSON.stringify(await quem(p)));
    await p.click('#acampamento-pontos [data-cid="morel"]'); await espera(400);
    await p.click('.menu-item button:has-text("Levar")'); await espera(1800); await fechar(p);
    await foto(p, `${nome}-6-morel-volta`); console.log(nome, "Morel de volta:", JSON.stringify(await quem(p)));
    await p.click('#acampamento-pontos [data-cid="yara"]'); await espera(400);
    const conv = await p.$('.menu-item button:has-text("Conversar")');
    if (conv) { await conv.click(); await espera(1500); await foto(p, `${nome}-7-conversa`);
      for (let k = 0; k < 40; k++) { const c = await p.$("#prompt .continuar"); if (!c) break; await c.click().catch(() => {}); await espera(500); }
      await espera(1000); console.log(nome, "depois da conversa:", JSON.stringify(await quem(p))); }
    await p.close(); proc.kill();
  }
  if (SO.has("fluxos")) {
    // recarregar a página na fogueira: a cena volta igual, com os mesmos pontos
    let { p, proc } = await abrir(`${jan}-recarregar`, W, H, "fogueira", { CLASSE: "guerreiro", LUGAR: "capela" });
    const antes = JSON.stringify(await quem(p));
    await p.reload(); await p.waitForSelector("#acampamento-pontos", { timeout: 20000 }); await espera(1500);
    await foto(p, `${jan}-recarregada`);
    console.log(`${jan} recarregar:`, antes === JSON.stringify(await quem(p)) ? "igual" : "DIFERENTE", antes);
    // dormir: a paisagem (a capela de fora) volta ao topo, sem o acampamento
    await p.click("#acampamento-pontos .dormir-barraca"); await espera(500);
    for (let k = 0; k < 60 && (await p.$("#acampamento-pontos")); k++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300); }
    await espera(3000); await fechar(p); await foto(p, `${jan}-amanhecer`);
    console.log(`${jan} amanhecer:`, await p.evaluate(() => ({ acampando: document.getElementById("cena").classList.contains("acampando"), capela: !!(window.Cenas && Cenas.atual()) })));
    await p.close(); proc.kill();
    ({ p, proc } = await abrir(`${jan}-exausto`, W, H, "fogueira", { CLASSE: "arqueiro", LUGAR: "charco", EXAUSTO: "1" }));
    await foto(p, `${jan}-exausto`); console.log(`${jan} exausto:`, JSON.stringify(await quem(p)));
    await p.close(); proc.kill();
    ({ p, proc } = await abrir(`${jan}-sair-da-capela`, W, H, "fogueira", { CLASSE: "mago", LUGAR: "capela", SALA: "salao" }));
    await foto(p, `${jan}-sair-da-capela`); console.log(`${jan} sair da capela:`, JSON.stringify(await quem(p)));
    await p.close(); proc.kill();
  }
  if (SO.has("tutorial")) {
    const { p, proc } = await abrir(`${jan}-d3`, W, H, "tutorial", { LUGAR: "charco", PERIODO: "3", VIDA: "0.5", COMITIVA: "morel,odete", RESERVA: "yara", CLASSE: "mago" }, { manterOrientacao: true });
    await espera(1000); await foto(p, `${jan}-tutorial-d3`);
    console.log(`${jan} D3:`, await p.evaluate(() => (document.querySelector(".orientacao:not([hidden])") || {}).innerText));
    await p.close(); proc.kill();
  }
}
await b.close();
console.log(erros.length ? `erros:\n${erros.join("\n")}` : "sem erros no console");
