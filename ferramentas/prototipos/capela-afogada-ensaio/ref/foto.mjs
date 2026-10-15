import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const D = process.argv[2];
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 1300, height: 320 } });
p.on("pageerror", (e) => console.log(String(e)));
await p.goto("file://" + D + "/ref.html");
for (const [bioma, per, tipo] of [["pantano", 2, "selvagem"], ["pantano", 3, "selvagem"], ["planicie", 2, "vila"]]) {
  await p.evaluate(([bioma, per, tipo]) => Vista.atualizar({ local: { id: 7, tipo, bioma }, mundo: { periodo_n: per, clima_id: "limpo", escuro: false } }), [bioma, per, tipo]);
  await p.waitForTimeout(400);
  await p.locator("#vista").screenshot({ path: `${D}/${bioma}-${per}.png` });
}
await b.close();
