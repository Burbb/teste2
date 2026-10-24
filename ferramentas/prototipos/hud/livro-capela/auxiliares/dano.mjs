// Confere a leitura no livro da capela deteriorado (cenarios_livro.py, PROPOSTA=capela), a 1920×945 e a 1280×720:
// para cada letra escrita, quanto dela cai onde a máscara da página tirou o papel (alfa abaixo de 0,5), amostrando
// a caixa da letra numa grade de 6×8 pontos. Exige: no texto real, as palavras essenciais intactas (Ilse, Sigilo,
// Turvo, Igreja, Fenda, guardiã, água); em todos, nenhuma palavra perde mais de 40% e nenhuma some. Lista as palavras tocadas (o que o
// rasgo tira de propósito). Também com textos de teste maiores (rolando), para ver que o dano fica preso à página e
// continua só tirando trechos. Guarda as fotos em ../capturas/dano-<janela>-<caso>.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/livro-capela/auxiliares/dano.mjs
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

const TESTES = {
  longo: { titulo: "O livro da capela", paginas: [
    Array.from({ length: 4 }, (_, i) => `Linha de prova ${i + 1} com acentos: ação, água, órgão, pântano e Ilse.`).join("\n\n"),
    Array.from({ length: 8 }, (_, i) => `Parágrafo de prova ${i + 1}, com o Sigilo e a Igreja no meio da frase.`).join("\n\n")] },
};

async function subir() {
  const proc = spawn(PY, [path.join(aqui, "cenarios_livro.py"), "releitura"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: "capela" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

// as palavras de cada página, com a fração de cada uma que o dano tira
const medir = (p) => p.evaluate(async () => {
  const saida = [];
  for (const cx of document.querySelectorAll("#sobre-leitura .lv-mascarada")) {
    const url = getComputedStyle(cx).getPropertyValue("--mascara").trim().replace(/^url\(['"]?|['"]?\)$/g, "");
    const img = new Image(); img.src = url; await img.decode();
    const cv = document.createElement("canvas"); cv.width = img.width; cv.height = img.height;
    const g = cv.getContext("2d"); g.drawImage(img, 0, 0);
    const dados = g.getImageData(0, 0, img.width, img.height).data;
    const caixa = cx.getBoundingClientRect();
    const alfa = (x, y) => { const i = Math.floor(x), j = Math.floor(y); if (i < 0 || j < 0 || i >= img.width || j >= img.height) return 255; return dados[(j * img.width + i) * 4 + 3]; };
    const palavras = [];
    const w = document.createTreeWalker(cx, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const n = w.currentNode, t = n.textContent;
      const re = /[^\s]+/g; let m;
      while ((m = re.exec(t))) {
        let tot = 0, fora = 0;
        for (let k = m.index; k < m.index + m[0].length; k++) {
          const r = document.createRange(); r.setStart(n, k); r.setEnd(n, k + 1);
          const b = r.getBoundingClientRect();
          if (b.bottom < caixa.top || b.top > caixa.bottom) continue;  // rolou para fora da vista
          for (let a = 0; a < 6; a++) for (let c = 0; c < 8; c++) {
            const x = b.left - caixa.left + (a + 0.5) * b.width / 6, y = b.top - caixa.top + (c + 0.5) * b.height / 8;
            tot++; if (alfa(x, y) < 128) fora++;
          }
        }
        if (tot) palavras.push({ p: m[0], f: fora / tot });
      }
    }
    saida.push(palavras);
  }
  return saida;
});

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const tocadas = {};
for (const [jan, W, H] of [["1920", 1920, 945], ["1280", 1280, 720]]) {
  console.log(`== ${jan}`);
  const { proc, url } = await subir();
  const p = await b.newPage({ viewport: { width: W, height: H } });
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  for (let k = 0; k < 80 && !(await p.$(`${MENU}:has-text("Ler o livro da capela")`)); k++) {
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(300);
  }
  await p.click(`${MENU}:has-text("Ler o livro da capela")`);
  await p.waitForSelector("#sobre-leitura:not([hidden])"); await p.evaluate(() => document.fonts.ready); await espera(500);
  const casos = [["real", null], ...Object.entries(TESTES)];
  for (const [nome, d] of casos) {
    if (d) { await p.evaluate((d) => { Telas.lerLivro(d, false); }, d); await p.waitForSelector("#sobre-leitura:not([hidden])"); await espera(400); }
    await p.mouse.move(2, 2);
    for (const rolar of nome === "real" ? [false] : [false, true]) {
      if (rolar) { await p.evaluate(() => document.querySelectorAll("#sobre-leitura .lv-regua").forEach((c) => { c.scrollTop = c.scrollHeight; })); await espera(200); }
      await p.screenshot({ path: path.join(SAIDA, `dano-${jan}-${nome}${rolar ? "-rolado" : ""}.png`) });
      const pags = await medir(p);
      const todas = pags.flat();
      const tocou = todas.filter((x) => x.f > 0);
      const ess = todas.filter((x) => ESSENCIAIS.some((e) => x.p.replace(/[.,:;]/g, "") === e));
      const rot = `${nome}${rolar ? " (rolado)" : ""}`;
      // as essenciais intactas: no texto real. Num texto de teste (um texto futuro qualquer), o rasgo preso à página
      // pode cair em qualquer palavra: ali vale só o limite de 40% e a lista das tocadas, para quem revisar o texto
      if (nome === "real") conferir(ess.length > 0 && ess.every((x) => x.f === 0), `${rot}: as palavras essenciais intactas (${ess.map((x) => x.p).join(", ")})`);
      else if (ess.some((x) => x.f > 0)) console.log(`      (aviso) ${rot}: o rasgo toca ${ess.filter((x) => x.f > 0).map((x) => x.p).join(", ")}: um texto novo pede esta conferência`);
      conferir(todas.every((x) => x.f <= 0.4), `${rot}: nenhuma palavra perde mais de 40% (a maior: ${Math.round(100 * Math.max(0, ...todas.map((x) => x.f)))}%)`);
      conferir(todas.every((x) => x.f < 1), `${rot}: nenhuma palavra some`);
      console.log(`      tocadas: ${tocou.map((x) => `${x.p} ${Math.round(100 * x.f)}%`).join(" · ") || "nenhuma"}`);
      if (nome === "real") tocadas[jan] = tocou.map((x) => `${x.p} ${Math.round(100 * x.f)}%`).join(" · ");
    }
    await p.keyboard.press("Escape"); await espera(300);
  }
  conferir(erros.length === 0, "sem erros na página" + (erros.length ? ": " + erros[0] : ""));
  await p.close(); proc.kill();
}
conferir(tocadas["1920"] === tocadas["1280"], "as mesmas letras tocadas nas duas janelas (as quebras são as mesmas)");
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
