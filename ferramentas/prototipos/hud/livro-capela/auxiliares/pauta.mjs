// Confere a escrita da A refinada apoiada na pauta, no jogo de verdade (cenarios_livro.py, PROPOSTA=a2, ou outra como
// PROPOSTA=capela), a 1920×945 e
// a 1280×720: em cada linha escrita das duas páginas, a linha de base (medida por uma sonda depois de cada palavra)
// cai em cima de uma linha da pauta (a 30 + 33·k px do alto do bloco; tolerância de 1 px). Primeiro com o texto real
// (o livro aberto pelo menu); depois, na mesma página, com textos de teste mais longos (outros acentos, palavras
// longas, outras quebras, um texto maior que a página) entregues ao mesmo Telas.lerLivro, sem mudar nada do jogo.
// Guarda as fotos dos testes em ../capturas/pauta-<janela>-<caso>.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/livro-capela/auxiliares/pauta.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

// textos de teste (não são do jogo): só para ver a pauta com outras quebras
const TESTES = {
  longo: { titulo: "O livro da capela", paginas: [
    "Ação, coração, pântano, água, órgão, açúcar, último, à noite: é só uma frase de prova com acentos e cedilha.\n\n" +
    "Outra linha, com palavras compridíssimas e inconstitucionalíssimas, para quebrar em outro lugar.",
    "Uma segunda entrada de prova, também com acentos (é, ê, ô, õ, ú), vírgulas, dois-pontos: e pontos finais.\n\n" +
    "Mais um parágrafo curto.\n\nE outro, para a página ter mais linhas do que antes."] },
  transborda: { titulo: "O livro da capela", paginas: [
    "Um texto de prova curto.",
    Array.from({ length: 9 }, (_, i) => `Parágrafo de prova ${i + 1}, com algumas palavras a mais para ocupar a linha inteira.`).join("\n\n")] },
};

async function subir() {
  const proc = spawn(PY, [path.join(aqui, "cenarios_livro.py"), "releitura"],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PROPOSTA: process.env.PROPOSTA || "a2" } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

// cada linha escrita: a distância da linha de base à pauta mais próxima (0 = apoiada nela)
const medir = (p) => p.evaluate(() => [...document.querySelectorAll("#sobre-leitura .lv-texto")].map((t) => {
  const sondas = [];
  for (const par of t.querySelectorAll("p")) {
    const w = document.createTreeWalker(par, NodeFilter.SHOW_TEXT);
    const nos = []; while (w.nextNode()) nos.push(w.currentNode);
    for (const n of nos) {
      const partes = n.textContent.split(/(\s+)/);
      const frag = document.createDocumentFragment();
      for (const x of partes) {
        frag.appendChild(document.createTextNode(x));
        if (x.trim()) { const s = document.createElement("span"); s.className = "sonda"; s.style.cssText = "display:inline-block;width:0;height:0"; frag.appendChild(s); sondas.push(s); }
      }
      n.replaceWith(frag);
    }
  }
  const topo = t.getBoundingClientRect().top;
  const bases = [...new Set(sondas.map((s) => Math.round(s.getBoundingClientRect().bottom - topo)))].sort((a, b) => a - b);
  sondas.forEach((s) => s.remove());
  const desvio = bases.map((b) => { const k = Math.round((b - 30) / 33); return b - (30 + 33 * k); });
  const caixa = t.parentElement;
  return { linhas: bases.length, desvio, rola: caixa.scrollHeight > caixa.clientHeight + 1 };
}));

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
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
  await p.waitForSelector("#sobre-leitura:not([hidden])", { timeout: 20000 });
  await p.evaluate(() => document.fonts.ready); await espera(500);
  const real = await medir(p);
  conferir(real.every((x) => x.desvio.every((d) => Math.abs(d) <= 1)), `texto real: cada linha de base na pauta (linhas ${real.map((x) => x.linhas).join(" e ")}; desvios ${JSON.stringify(real.map((x) => x.desvio))})`);
  conferir(real.every((x) => !x.rola), "texto real: cabe nas páginas, sem rolar");
  conferir(await p.evaluate(() => document.activeElement.classList.contains("lv-fechar")), "o foco no Fechar");
  await p.keyboard.press("2"); await espera(200);
  conferir(!!(await p.$("#sobre-leitura:not([hidden])")), "a tecla 2 não escolhe nada embaixo do livro");
  await p.keyboard.press("Escape"); await espera(300);
  conferir(!(await p.$("#sobre-leitura:not([hidden])")), "Esc fecha");
  for (const [nome, d] of Object.entries(TESTES)) {
    await p.evaluate((d) => { Telas.lerLivro(d, false); }, d);
    await p.waitForSelector("#sobre-leitura:not([hidden])"); await espera(400);
    await p.mouse.move(2, 2);
    await p.screenshot({ path: path.join(SAIDA, `pauta-${process.env.PROPOSTA || "a2"}-${jan}-${nome}.png`) });
    const m = await medir(p);
    conferir(m.every((x) => x.desvio.every((dd) => Math.abs(dd) <= 1)), `texto de teste "${nome}": cada linha na pauta (linhas ${m.map((x) => x.linhas).join(" e ")})`);
    if (nome === "transborda") {
      const r = await p.evaluate(() => { const c = document.querySelectorAll("#sobre-leitura .lv-regua")[1]; c.scrollTop = c.scrollHeight; return c.scrollTop; });
      await espera(200);
      const m2 = await medir(p);
      conferir(m[1].rola && r > 0 && m2[1].desvio.every((dd) => Math.abs(dd) <= 1), `"${nome}": a página rola, e a pauta rola junto (rolada ${r} px, ainda alinhada)`);
    }
    await p.keyboard.press("Escape"); await espera(300);
  }
  conferir(erros.length === 0, "sem erros na página" + (erros.length ? ": " + erros[0] : ""));
  await p.close(); proc.kill();
}
await b.close();
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
