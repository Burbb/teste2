// O lote de itens da noite (proposta, nada no jogo): fotografa cada desenho novo nos lugares onde ele fica parado,
// atual × proposta, nas janelas normal (1500×950) e baixa (1280×720), com o jogo intacto. A página recebe os arquivos
// da proposta no lugar dos do jogo (page.route em /static/hud/icones/<peça>-*.png, como fotografar_escudo.mjs); uma
// peça que ainda não tem papel em icones.js (a calça de couro) ganha o papel só nesta página.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs <peça>
// peça: calca_couro | aljava | atributos | doca
import { spawn } from "child_process";
import { readFileSync, existsSync, mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const peca = process.argv[2];
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const JANELAS = [[1500, 950], [1280, 720]];
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";

// cada peça: a pasta da proposta, os nomes de arquivo que ela troca, o papel novo (se houver) e as fotos
const PECAS = {
  calca_couro: { pasta: "calca_couro/proposta", nomes: ["calca_couro"], papel: { item: "calca_couro", tamanhos: [32, 64] },
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario"] },
  aljava: { pasta: "aljava/proposta", nomes: ["aljava"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo", "ficha", "inventario"] },
  atributos: { pasta: "atributos/proposta", nomes: ["attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "luta"] },
  doca: { pasta: "doca/proposta", nomes: ["atalho-talentos", "atalho-grimorio", "atalho-inventario", "atalho-mapa", "atalho-diario", "atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "luta-doca"] },
};
const P = PECAS[peca];
if (!P) throw new Error(`peça desconhecida: ${peca}`);
const PROPOSTA = path.join(aqui, P.pasta), SAIDA = path.join(aqui, peca, "capturas");
mkdirSync(SAIDA, { recursive: true });

async function anexar(p) {
  await p.route(/\/static\/hud\/icones\/([a-z_-]+)-(\d+)(@2x)?\.png/, async (r) => {
    const nome = decodeURIComponent(new URL(r.request().url()).pathname.split("/").pop());
    const base = nome.replace(/-\d+(@2x)?\.png$/, "");
    const arquivo = path.join(PROPOSTA, nome);
    if (P.nomes.includes(base) && existsSync(arquivo)) return r.fulfill({ body: readFileSync(arquivo), contentType: "image/png" });
    return r.continue();
  });
  if (P.papel) {
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${P.papel.item}": ${JSON.stringify(P.papel.tamanhos)}, `);
      js = js.replace('const ITEM = {', `const ITEM = { ${P.papel.item}: "${P.papel.item}", `);
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
}
async function subir() {
  const [cenario, amb] = P.cena;
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

const b = await chromium.launch();
const rel = [];
for (const modo of ["atual", "proposta"]) for (const [W, H] of JANELAS) {
  const { proc, url } = await subir();
  try {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo === "proposta") await anexar(p);
    await p.goto(url); await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1200);
    const nome = (f) => path.join(SAIDA, `${modo}-${W}x${H}-${f}.png`);
    const clipDe = async (sel, m = 8) => { const bb = await (await p.$(sel)).boundingBox(); return { x: Math.max(0, bb.x - m), y: Math.max(0, bb.y - m), width: bb.width + 2 * m, height: bb.height + 2 * m }; };
    // o que os desenhos da peça carregaram (o arquivo e o tamanho na tela)
    const desenhos = async () => p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
      .map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}px`), P.nomes);
    const visto = new Set();
    for (const f of P.fotos) {
      if (f === "ficha") { await p.screenshot({ path: nome("ficha"), clip: await clipDe("#heroi", 0) }); }
      if (f === "topo") { await p.screenshot({ path: nome("topo"), clip: await clipDe("#hud", 0) }); }
      if (f === "doca") { await p.screenshot({ path: nome("doca"), clip: await clipDe("#doca", 0) }); }
      if (f === "inventario") {
        await p.evaluate(() => pedirAtalho("Inventário")); await espera(900);
        await p.screenshot({ path: nome("inventario"), clip: await clipDe("#palco", 0) });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(500);
      }
      if (f === "luta" || f === "luta-doca") {
        const comecar = await p.$('#prompt .escolha:has-text("Começar a luta")');
        if (comecar) {
          await comecar.click();
          await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 }); await espera(1200);
          await p.screenshot({ path: nome("luta"), clip: await clipDe("#palco", 0) });
          if (f === "luta") { await p.screenshot({ path: nome("luta-ficha"), clip: await clipDe("#heroi", 0) }); }
        }
      }
      (await desenhos()).forEach((d) => visto.add(d));
    }
    rel.push({ modo, janela: `${W}x${H}`, desenhos: [...visto].sort(), erros });
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
for (const r of rel) console.log(JSON.stringify(r));
