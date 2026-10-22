// O levantamento do animal no acampamento e do comando Atacar (21/10/2026; nada no jogo), a 1920×945:
//  - a fogueira com o lobo, o urso e o falcão do patrulheiro (o cenário fogueira, FERA=<tipo>): a cena e o desenho que
//    cada um recebe (o canvas da arte de 320×72 e a escala dele na tela);
//  - a roda da luta das três classes (o cenário tutorial): o Arqueiro como está, com o arco aprovado trocado só na
//    página (rpg/web/static/hud/icones/arco-32.png, no lugar do sprite) e com uma Besta equipada (ARMA=besta, sem
//    troca: o desenho que o jogo escolhe); o Guerreiro e o Mago como estão.
//  - a proposta dos animais (fogueira-<tipo>-proposta): a figura que a cena pede para o animal (Icones.figura de "fera"
//    ou "voador") vira, só na página, a proposta do tipo (bancada/animal-<tipo>-16.png ou proposta/, o que existir);
//  - o cajado aprovado (cajado-32) no Atacar do Mago, trocado só na página.
//   [SO=<nome>,<nome>] PLAYWRIGHT_MODULO=<file:// do index.mjs> node fotografar.mjs <raiz> <pasta das fotos>
import { spawn } from "child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const [raiz, saida] = process.argv.slice(2);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const aqui = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
// ANIMAIS=<pasta>: as figuras de outra pasta (uma rodada na bancada), no lugar da proposta
const animal = (t) => { const a = (process.env.ANIMAIS ? [process.env.ANIMAIS] : ["proposta", "bancada"].map((d) => path.join(aqui, d)))
  .map((d) => path.join(d, `animal-${t}-16.png`)).find(existsSync);
  return a && "data:image/png;base64," + readFileSync(a).toString("base64"); };
const SO = process.env.SO ? process.env.SO.split(",") : null;
const LUTA = { TUTORIAL: "0", NIVEL_LUTA: "2", GRUPO: "lobo:1" };
const SITUACOES = [
  ...["lobo", "urso", "falcao"].map((t) => ({ nome: `fogueira-${t}`, cenario: "fogueira",
    amb: { CLASSE: "arqueiro", COMITIVA: "morel", RESERVA: "", FERA: t }, acampar: true })),
  ...["lobo", "urso", "falcao"].map((t) => ({ nome: `fogueira-${t}-proposta`, cenario: "fogueira",
    amb: { CLASSE: "arqueiro", COMITIVA: "morel", RESERVA: "", FERA: t }, acampar: true, animal: t })),
  ...["lobo", "urso"].map((t) => ({ nome: `fogueira-${t}-r2`, cenario: "fogueira",   // a segunda rodada
    amb: { CLASSE: "arqueiro", COMITIVA: "morel", RESERVA: "", FERA: t }, acampar: true, animal: `${t}-r2` })),
  ...["lobo", "urso"].map((t) => ({ nome: `fogueira-${t}-r3`, cenario: "fogueira",   // a terceira, pelas referências
    amb: { CLASSE: "arqueiro", COMITIVA: "morel", RESERVA: "", FERA: t }, acampar: true, animal: `${t}-r3` })),
  ...["lobo", "urso"].map((t) => ({ nome: `fogueira-${t}-r4`, cenario: "fogueira",   // a quarta, o refinamento
    amb: { CLASSE: "arqueiro", COMITIVA: "morel", RESERVA: "", FERA: t }, acampar: true, animal: `${t}-r4` })),
  { nome: "roda-arqueiro", cenario: "tutorial", amb: { ...LUTA, CLASSE: "arqueiro" } },
  { nome: "roda-arqueiro-arco", cenario: "tutorial", amb: { ...LUTA, CLASSE: "arqueiro" }, troca: "arco" },
  { nome: "roda-arqueiro-besta", cenario: "tutorial", amb: { ...LUTA, CLASSE: "arqueiro", ARMA: "besta" } },
  { nome: "roda-guerreiro", cenario: "tutorial", amb: { ...LUTA, CLASSE: "guerreiro" } },
  { nome: "roda-mago", cenario: "tutorial", amb: { ...LUTA, CLASSE: "mago" } },
  { nome: "roda-mago-cajado", cenario: "tutorial", amb: { ...LUTA, CLASSE: "mago" }, troca: "cajado" },
];
mkdirSync(saida, { recursive: true });
const b = await chromium.launch();
const arqRegistro = path.join(saida, "registro.json");
const registro = existsSync(arqRegistro) ? JSON.parse(readFileSync(arqRegistro, "utf-8")) : {};
for (const sit of SITUACOES.filter((x) => !SO || SO.includes(x.nome))) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", sit.cenario], { cwd: raiz,
    env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...sit.amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: 1920, height: 945 } });
    const erros = [];
    p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") erros.push(m.text()); });
    await p.goto(url);
    if (sit.acampar) {
      await p.waitForSelector('#prompt .escolha:has-text("Acampar")', { timeout: 30000 });
      if (sit.animal) await p.evaluate(async (src) => {   // a figura da proposta no lugar do sprite, só nesta página
        const im = new Image(); im.src = src; await im.decode();
        const tela = document.createElement("canvas"); tela.width = tela.height = 16; tela.getContext("2d").drawImage(im, 0, 0);
        const original = Icones.figura;
        Icones.figura = (nome) => (nome === "fera" || nome === "voador" ? tela : original(nome));
      }, animal(sit.animal));
      await p.click('#prompt .escolha:has-text("Acampar")');
      await p.waitForSelector(".fogueira-rodape", { timeout: 20000 });
      await espera(1500);
      // o canvas da arte (o maior da página) e a escala dele
      const info = await p.evaluate(() => {
        const c = [...document.querySelectorAll("canvas")].sort((a, z) => z.width * z.height - a.width * a.height)[0];
        const r = c.getBoundingClientRect();
        c.id = c.id || "arte-fogueira";
        return { id: c.id, arte: [c.width, c.height], tela: [Math.round(r.width), Math.round(r.height)], caixa: [r.left, r.top, r.right, r.bottom].map(Math.round) };
      });
      await p.locator(`#${info.id}`).screenshot({ path: path.join(saida, `${sit.nome}.png`) });
      registro[sit.nome] = { erros, ...info };
    } else {
      await p.waitForSelector('#roda .roda-botao[data-slot="atacar"]', { timeout: 30000 });
      await espera(1200);
      if (sit.troca) await p.evaluate((peca) => {
        const im = document.querySelector('#roda .roda-botao[data-slot="atacar"] .rb-icone img');
        im.src = `/static/hud/icones/${peca}-32.png`; im.srcset = `/static/hud/icones/${peca}-32@2x.png 2x`;
        im.classList.add("desenho"); im.setAttribute("width", 32); im.setAttribute("height", 32);
      }, sit.troca);
      await espera(600);
      const info = await p.evaluate(() => {
        const im = document.querySelector('#roda .roda-botao[data-slot="atacar"] .rb-icone img'), r = im.getBoundingClientRect();
        const roda = document.querySelector("#roda").getBoundingClientRect();
        const j = (window.estado || (window.App && App.estado) || {}).heroi || {};
        return { src: (im.getAttribute("src") || "").slice(0, 60), classe: im.className, tela: [Math.round(r.width), Math.round(r.height)],
                 natural: [im.naturalWidth, im.naturalHeight], icone: [r.left - roda.left, r.top - roda.top, r.right - roda.left, r.bottom - roda.top].map(Math.round),
                 arma: (j.equip && j.equip.arma && j.equip.arma.nome) || null };
      });
      await p.locator("#roda").screenshot({ path: path.join(saida, `${sit.nome}.png`) });
      registro[sit.nome] = { erros, ...info };
    }
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(arqRegistro, JSON.stringify(registro, null, 1));
for (const [k, v] of Object.entries(registro)) if (!SO || SO.includes(k)) console.log(k, JSON.stringify(v));
