// Fotografa as telas iniciais no jogo de verdade, depois da retirada do mundo gerado (1.206.0): o título, a lista de
// saves (um da campanha e um do mundo gerado, que não abre mais), a mensagem do save incompatível e a criação do
// personagem (o nome, a classe, o modo com a caixa do tutorial), a 1920×945 e a 1280×720, hoje e na proposta R da
// criação (VERSOES=atual,r). cenarios_telas.py, com saves numa pasta temporária. Guarda
// ../capturas/<janela>-<versão>-<tela>.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/telas-iniciais/auxiliares/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const erros = [];

async function subir(proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_telas.py")], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: proposta } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) for (const v of (process.env.VERSOES || "atual,r").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  const { proc, url } = await subir(v === "atual" ? "" : v);
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on("pageerror", (e) => erros.push(`${jan}-${v}: ${e}`));
  const foto = async (nome) => { await p.mouse.move(2, 2); await espera(500); await p.screenshot({ path: path.join(SAIDA, `${jan}-${v}-${nome}.png`) }); console.log(jan, v, nome); };
  const continuarAte = async (sel) => {
    for (let t = 0; t < 80 && !(await p.$(sel)); t++) { const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(200); }
  };
  await p.goto(url);
  await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
  await foto("1-titulo");
  await p.click('#prompt .escolha:has-text("Carregar")');
  await p.waitForSelector(".save-cartao");
  await foto("2-saves");
  await p.click('.save-cartao:has-text("Jean")');
  await p.waitForSelector('#texto :text("Este save não abre")', { timeout: 15000 });
  await foto("3-save-incompativel");
  await continuarAte('#prompt .escolhas:not(.escolhido) .escolha:has-text("Novo jogo")');
  await p.click('#prompt .escolha:has-text("Novo jogo")');
  await p.waitForSelector(".entrada-texto input", { timeout: 20000 });
  await foto("4-nome");
  await p.fill(".entrada-texto input", "Ana");
  await p.keyboard.press("Enter");
  await p.waitForSelector('#prompt .escolha:has-text("Arqueiro")', { timeout: 20000 });
  await foto("5-classe");
  await p.click('#prompt .escolha:has-text("Arqueiro")');
  await p.waitForSelector('#prompt .escolha:has-text("Resgate")', { timeout: 20000 });
  await foto("6-modo");
  await p.close(); proc.kill();
}
await b.close();
console.log(erros.length ? erros : "sem erros");
