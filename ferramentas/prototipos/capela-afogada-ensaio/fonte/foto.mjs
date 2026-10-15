import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const S = process.argv[2], O = S + "/fotos";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const erros = [];
const p = await b.newPage({ viewport: { width: 1340, height: 900 } });
p.on("pageerror", (e) => erros.push(String(e)));
p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
await p.goto("file://" + S + "/capela.html");
await p.waitForTimeout(600);
const q = (n) => p.locator(".quadro").screenshot({ path: `${O}/${n}.png` });
for (const h of [0, 1, 2, 3]) { await p.click(`#hora-${h}`); await p.waitForTimeout(600); await q(`fora-h${h}`); }
await p.click("#hora-2"); await p.waitForTimeout(600);
await p.hover("#ponto-fora-buraco"); await p.waitForTimeout(150); await q("fora-hover-buraco");
await p.click("#ponto-fora-sapos"); await p.waitForTimeout(700); await q("fora-sapos");
await p.click("#opcao-fora-afastar"); await p.waitForTimeout(600);
await p.click("#ponto-fora-torre"); await p.waitForTimeout(700); await q("fora-torre");
await p.keyboard.press("Escape"); await p.waitForTimeout(600);
await p.click("#ponto-fora-buraco"); await p.waitForTimeout(800);
for (const h of [0, 2, 3]) { await p.click(`#hora-${h}`); await p.waitForTimeout(600); await q(`dentro-h${h}`); }
await p.click("#hora-2"); await p.waitForTimeout(600);
await p.hover("#ponto-dentro-sarilho"); await p.waitForTimeout(150); await q("dentro-hover-sarilho");
await p.click("#ponto-dentro-sarilho"); await p.mouse.move(0, 0); await p.waitForTimeout(1300); await q("dentro-soltando");
await p.waitForTimeout(2000); await q("dentro-solto");
await p.screenshot({ path: `${O}/pagina-solto.png`, fullPage: true });
await p.setViewportSize({ width: 400, height: 900 }); await p.waitForTimeout(500);
await p.screenshot({ path: `${O}/fone.png`, fullPage: true });
console.log("scrollWidth 400:", await p.evaluate(() => document.documentElement.scrollWidth));
console.log("erros:", erros);
await b.close();
