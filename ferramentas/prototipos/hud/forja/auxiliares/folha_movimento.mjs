// A folha do movimento do ferreiro (a R): as poses-chave ampliadas 5× com a duração de cada uma, o ciclo inteiro quadro a
// quadro (53 quadros de 100 ms, a 2×: as esperas no alto e no repouso se veem pela repetição), a pose parada do
// movimento reduzido e um trecho da cena em tamanho de uso (3×, perto do jogo a 1920). Só diagnóstico: o jogo mostra
// a cena no tamanho dela. Grava ../folha-movimento.png.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/forja/auxiliares/folha_movimento.mjs
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const p = await b.newPage({ viewport: { width: 1800, height: 1200 } });
await p.goto(pathToFileURL(path.join(aqui, "bancada-r.html")).href);
await p.evaluate(() => {
  const R = ForjaArte.r, base = R.base(320, {}), REC = [108, 10, 78, 60];
  const quadro = (q, reduzido = false) => {
    const mm = window.matchMedia; if (reduzido) window.matchMedia = () => ({ matches: true });
    const c = document.createElement("canvas"); c.width = 320; c.height = 72; R.desenhar(c.getContext("2d"), 320, base, {}, q, null);
    window.matchMedia = mm; return c;
  };
  const corte = (c, rec, e) => { const [x, y, w, h] = rec, g = document.createElement("canvas"); g.width = w * e; g.height = h * e; const gc = g.getContext("2d"); gc.imageSmoothingEnabled = false; gc.drawImage(c, x, y, w, h, 0, 0, w * e, h * e); return g; };
  document.body.innerHTML = ""; document.body.style.cssText = "background:#16120e;color:#dcc896;font:14px Georgia,serif;margin:12px";
  const titulo = (t) => { const d = document.createElement("div"); d.textContent = t; d.style.margin = "10px 0 4px"; document.body.appendChild(d); };
  titulo("A forja R · o ferreiro forjando: as poses-chave (5×, só diagnóstico), na ordem do golpe, com a duração no ciclo");
  const linha = document.createElement("div"); linha.style.cssText = "display:flex;flex-wrap:wrap;gap:8px"; document.body.appendChild(linha);
  const durs = {}; R.CICLO.forEach(([n, d]) => { (durs[n] = durs[n] || []).push(d * 100); });
  const ordem = ["repouso", "sobe1", "sobe2", "alto", "desce", "golpe", "volta", "ajuste"];
  ordem.forEach((nome) => {
    let q = 0; while (R.poseDe(q).nome !== nome) q++;
    const d = document.createElement("div"); d.style.textAlign = "center"; d.style.fontSize = "13px";
    d.appendChild(corte(quadro(nome === "volta" || nome === "golpe" ? q : q), REC, 5));
    d.append(`${nome} · ${[...new Set(durs[nome])].join(" / ")} ms`); linha.appendChild(d);
  });
  titulo(`o ciclo inteiro, quadro a quadro (${R.DURACAO} × 100 ms = ${R.DURACAO / 10} s; 2×): quatro golpes com o alto e o repouso variando, e a pausa da tenaz; o último quadro emenda no primeiro`);
  const tira = document.createElement("div"); tira.style.cssText = "display:flex;flex-wrap:wrap;gap:2px;width:1760px"; document.body.appendChild(tira);
  for (let q = 0; q < R.DURACAO; q++) { const k = corte(quadro(q), [116, 8, 60, 62], 2); k.title = R.poseDe(q).nome; tira.appendChild(k); }
  titulo("com movimento reduzido: a pose do alto, parada, sem faíscas (5×) · e a cena no tamanho de uso (3×), no golpe");
  const fim = document.createElement("div"); fim.style.cssText = "display:flex;gap:12px;align-items:flex-start"; document.body.appendChild(fim);
  fim.appendChild(corte(quadro(0, true), REC, 5));
  let qg = 0; while (R.poseDe(qg).nome !== "golpe") qg++;
  fim.appendChild(corte(quadro(qg), [0, 0, 320, 72], 3));
});
await p.screenshot({ path: path.join(aqui, "..", "folha-movimento.png"), fullPage: true });
await b.close();
console.log("ok");
