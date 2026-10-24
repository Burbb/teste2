// Confere o livro INTEGRADO (1.204.0), no jogo como ele é (cenarios_livro.py sem PROPOSTA: nada do protótipo na
// página), a 1920×945 e a 1280×720:
// - a página carrega só arquivos de produção (/static/livros/, /static/fontes/fondamento...), nenhum do protótipo;
// - o acabamento da capela (o documento manda "capela"); a etiqueta, o Fechar com o foco;
// - cada linha de base na pauta (desvio 0), com o texto real e com um texto de teste maior que rola;
// - o dano: as palavras essenciais intactas no texto real, nenhuma palavra perde mais de 40% (também rolando);
// - fecha por Esc, as teclas do menu não escolhem nada embaixo; o texto segue para o Continuar.
// Fotos em ../capturas/jogo-<janela>[-rolado].png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/livro-capela/auxiliares/conferir_jogo.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const ESSENCIAIS = ["Ilse", "Sigilo", "Turvo", "Igreja", "Fenda", "guardiã", "água"];
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };
const MAIOR = { titulo: "O livro da capela", acabamento: "capela", paginas: [
  Array.from({ length: 4 }, (_, i) => `Linha de prova ${i + 1} com acentos: ação, água, órgão, pântano.`).join("\n\n"),
  Array.from({ length: 9 }, (_, i) => `Parágrafo de prova ${i + 1}, com algumas palavras a mais para ocupar a linha.`).join("\n\n")] };

async function subir() {
  const proc = spawn(PY, [path.join(aqui, "cenarios_livro.py"), "primeira"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: "" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

// a pauta: cada linha de base a 30 + 33·k px do alto do bloco (uma sonda depois de cada palavra, como no pauta.mjs)
const pauta = (p) => p.evaluate(() => [...document.querySelectorAll("#sobre-leitura .livro-texto")].map((t) => {
  const sondas = [];
  for (const par of t.querySelectorAll("p")) {
    const w = document.createTreeWalker(par, NodeFilter.SHOW_TEXT);
    const nos = []; while (w.nextNode()) nos.push(w.currentNode);
    for (const n of nos) {
      const frag = document.createDocumentFragment();
      for (const x of n.textContent.split(/(\s+)/)) {
        frag.appendChild(document.createTextNode(x));
        if (x.trim()) { const s = document.createElement("span"); s.style.cssText = "display:inline-block;width:0;height:0"; frag.appendChild(s); sondas.push(s); }
      }
      n.replaceWith(frag);
    }
  }
  const topo = t.getBoundingClientRect().top;
  const bases = [...new Set(sondas.map((s) => Math.round(s.getBoundingClientRect().bottom - topo)))];
  sondas.forEach((s) => s.remove());
  t.querySelectorAll("p").forEach((par) => par.normalize());
  return bases.map((b) => b - (30 + 33 * Math.round((b - 30) / 33)));
}));
// o dano: quanto de cada palavra cai onde a máscara tirou o papel
const dano = (p) => p.evaluate(async () => {
  const out = [];
  for (const cx of document.querySelectorAll("#sobre-leitura .livro-mascarada")) {
    const url = getComputedStyle(cx).getPropertyValue("--mascara").trim().replace(/^url\(['"]?|['"]?\)$/g, "");
    const img = new Image(); img.src = url; await img.decode();
    const cv = document.createElement("canvas"); cv.width = img.width; cv.height = img.height;
    const g = cv.getContext("2d"); g.drawImage(img, 0, 0);
    const dd = g.getImageData(0, 0, img.width, img.height).data, caixa = cx.getBoundingClientRect();
    const alfa = (x, y) => { const i = Math.floor(x), j = Math.floor(y); return i < 0 || j < 0 || i >= img.width || j >= img.height ? 255 : dd[(j * img.width + i) * 4 + 3]; };
    const w = document.createTreeWalker(cx, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const n = w.currentNode, re = /[^\s]+/g; let m;
      while ((m = re.exec(n.textContent))) {
        let tot = 0, fora = 0;
        for (let k = m.index; k < m.index + m[0].length; k++) {
          const r = document.createRange(); r.setStart(n, k); r.setEnd(n, k + 1); const b = r.getBoundingClientRect();
          if (b.bottom < caixa.top || b.top > caixa.bottom) continue;
          for (let a = 0; a < 6; a++) for (let c = 0; c < 8; c++) { tot++; if (alfa(b.left - caixa.left + (a + 0.5) * b.width / 6, b.top - caixa.top + (c + 0.5) * b.height / 8) < 128) fora++; }
        }
        if (tot) out.push({ p: m[0], f: fora / tot });
      }
    }
  }
  return out;
});

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const tocadas = {};
for (const [jan, W, H] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
  console.log(`== ${jan}`);
  const { proc, url } = await subir();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const erros = [], pedidos = [];
  p.on("pageerror", (e) => erros.push(String(e)));
  p.on("response", (r) => { if (r.status() >= 400 && !/favicon/.test(r.url())) erros.push(`${r.status()} ${r.url()}`); });
  p.on("request", (r) => pedidos.push(new URL(r.url()).pathname));
  await p.goto(url);
  for (let k = 0; k < 80 && !(await p.$(`${MENU}:has-text("Ler o livro da capela")`)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await p.click(`${MENU}:has-text("Ler o livro da capela")`);
  await p.waitForSelector("#sobre-leitura:not([hidden])"); await p.evaluate(() => document.fonts.ready); await espera(600);
  await p.mouse.move(2, 2);
  await p.screenshot({ path: path.join(SAIDA, `jogo-${jan}.png`) });
  const fundo = await p.$eval("#sobre-leitura .livro-livro", (e) => e.style.backgroundImage);
  conferir(/\/static\/livros\/capela\.png/.test(fundo) && (await p.$$("#sobre-leitura .livro-mascarada")).length === 2, "o acabamento da capela, com a máscara nas duas páginas");
  conferir(/O livro da capela/.test(await p.textContent(".livro-rotulo")) && await p.evaluate(() => document.activeElement.classList.contains("livro-fechar")), "a etiqueta e o foco no Fechar");
  const desvios = await pauta(p);
  conferir(desvios.flat().length >= 16 && desvios.flat().every((d) => Math.abs(d) <= 1), `a escrita na pauta (desvios ${JSON.stringify(desvios)})`);
  const real = await dano(p);
  const ess = real.filter((x) => ESSENCIAIS.includes(x.p.replace(/[.,:;]/g, "")));
  conferir(ess.length >= 7 && ess.every((x) => x.f === 0) && real.every((x) => x.f <= 0.4), `o dano só tira trechos; as essenciais intactas (tocadas: ${real.filter((x) => x.f > 0).map((x) => `${x.p} ${Math.round(100 * x.f)}%`).join(" · ")})`);
  tocadas[jan] = real.filter((x) => x.f > 0).map((x) => x.p).join(",");
  await p.keyboard.press("2"); await espera(200);
  conferir(!!(await p.$("#sobre-leitura:not([hidden])")), "a tecla 2 não escolhe nada embaixo do livro");
  await p.keyboard.press("Escape"); await espera(300);
  conferir(!(await p.$("#sobre-leitura:not([hidden])")) && !!(await p.waitForSelector("#prompt .continuar", { timeout: 20000 })), "Esc fecha e o texto segue para o Continuar");
  // um texto de teste maior, pelo mesmo Telas.lerLivro: rola com a pauta e o dano presos à página
  await p.evaluate((d) => { Telas.lerLivro(d, false); }, MAIOR);
  await p.waitForSelector("#sobre-leitura:not([hidden])"); await espera(400);
  await p.evaluate(() => document.querySelectorAll("#sobre-leitura .livro-regua").forEach((c) => { c.scrollTop = c.scrollHeight; }));
  await espera(300); await p.mouse.move(2, 2);
  await p.screenshot({ path: path.join(SAIDA, `jogo-${jan}-rolado.png`) });
  const rolou = await p.$$eval("#sobre-leitura .livro-regua", (cs) => cs.map((c) => c.scrollTop));
  const d2 = await pauta(p), m2 = await dano(p);
  conferir(rolou[1] > 0 && d2.flat().every((d) => Math.abs(d) <= 1) && m2.every((x) => x.f <= 0.4 && x.f < 1),
    `texto maior: rola (${rolou[1]} px), a pauta alinhada e o dano só tira trechos`);
  await p.keyboard.press("Escape"); await espera(200);
  conferir(!pedidos.some((u) => /prototipo/.test(u)) && pedidos.includes("/static/livros/capela.png") && pedidos.some((u) => /fondamento/.test(u)),
    "só arquivos de produção (livros/, fontes/), nada do protótipo");
  conferir(erros.length === 0, "sem erros na página" + (erros.length ? ": " + erros[0] : ""));
  await p.close(); proc.kill();
}
conferir(tocadas["1920"] === tocadas["1280"], "as mesmas letras tocadas nas duas janelas");
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
