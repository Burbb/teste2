// Playwright, Campo Livre 6: abre a tela de verdade e confere o fluxo nas duas janelas de referência (1920 × 1080 e
// 1280 × 720): a escolha monta (os oito encontros, as composições), a vila começa com as construções, Morel e Odette e
// os tipos novos no placar; a seleção por tipo (F3, F5, F6, F7) e o modo de comando funcionam; o encontro de Harg e
// Ardis mostra as duas barras; o Campo Livre 5 continua abrindo em /v5/; nenhum erro no console. Capturas pontuais.
// Uso: PLAYWRIGHT_MODULO=file:///.../index.mjs node ferramentas/conferir6.mjs [porta] [pasta]
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO);
const PORTA = process.argv[2] || "8801", SAIDA = process.argv[3] || "capturas";
const BASE = `http://127.0.0.1:${PORTA}/`;
const nav = await chromium.launch();
const falhas = [];
const ok = (c, msg) => { if (!c) falhas.push(msg); console.log(c ? "  ok " : "  FALHA ", msg); };

for (const [w, h] of [[1920, 1080], [1280, 720]]) {
  const p = await nav.newPage({ viewport: { width: w, height: h } });
  const erros = [];
  p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
  p.on("pageerror", (e) => erros.push("pageerror: " + e.message));
  console.log(`== ${w}×${h}`);
  await p.goto(BASE, { waitUntil: "networkidle" });
  await p.evaluate(() => localStorage.clear());
  await p.goto(BASE, { waitUntil: "networkidle" });
  const ini = await p.evaluate(() => ({
    titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length,
    comps: document.querySelectorAll("#op-comp-aliados option").length, herois: document.querySelectorAll("#herois .heroi").length,
    topo: document.querySelector("#tela-inicio .caixa").getBoundingClientRect().top,
  }));
  ok(ini.titulo.startsWith("Campo Livre 6") && ini.encontros === 8 && ini.comps === 4 && ini.herois === 2 && ini.topo >= 0, `a escolha monta ${JSON.stringify(ini)}`);
  // a vila pela tela: o encontro, as composições completas dos dois lados, Lutar
  await p.click('#encontros .encontro[data-enc="vila"]');
  await p.selectOption("#op-comp-aliados", "completa");
  await p.selectOption("#op-comp-inimigos", "completa");
  if (w === 1920) await p.screenshot({ path: `${SAIDA}/cl6-escolha-${w}.png` });
  await p.click("#lutar");
  await p.waitForTimeout(2500);
  const luta = await p.evaluate(() => {
    const m = window.__campo ? window.__campo.st.m : null;
    const tipos = [...document.querySelectorAll("#p-tipos span")].map((s) => s.textContent.trim());
    return { tipos, comp: !document.querySelector("#comp").hidden, compTxt: document.querySelector("#comp").textContent };
  });
  ok(luta.tipos.some((t) => t.includes("Cavalaria")) && luta.tipos.some((t) => t.includes("Pesados")) && luta.tipos.some((t) => t.includes("Magos")) && luta.tipos.some((t) => t.includes("Morel")),
    `o placar mostra os tipos novos: ${luta.tipos.join(" | ")}`);
  ok(luta.comp && /Morel/.test(luta.compTxt) && /Odette/.test(luta.compTxt), `a vida de Morel e Odette aparece: ${luta.compTxt}`);
  // a seleção por tipo e o modo de comando
  for (const [tecla, nome] of [["F3", "cavaleiros"], ["F5", "pesados"], ["F6", "magos"], ["F7", "Morel e Odette"]]) {
    await p.keyboard.press(tecla);
    await p.waitForTimeout(120);
    const sel = await p.textContent("#p-selecao");
    ok(/Seleção: \d+/.test(sel), `${tecla} seleciona ${nome}: ${sel.trim()}`);
    await p.keyboard.press("x");
  }
  await p.keyboard.press("F4");
  await p.keyboard.down("Shift");
  await p.waitForTimeout(120);
  const modo = await p.textContent("#modo");
  await p.mouse.click(w * 0.45, h * 0.5, { button: "right" });
  await p.waitForTimeout(200);
  const ordens = await p.textContent("#p-ordens");
  await p.keyboard.up("Shift");
  ok(/Comando/.test(modo) && /Defender aqui\D*\d+/.test(ordens), `modo de comando e Defender: ${ordens.trim()}`);
  await p.keyboard.press("1");
  await p.waitForTimeout(5000);
  await p.screenshot({ path: `${SAIDA}/cl6-vila-${w}.png` });
  // Harg e Ardis: as duas barras
  await p.goto(BASE + "?enc=herois&compA=pesada&compI=completa&auto=1&robo=1", { waitUntil: "networkidle" });
  await p.waitForTimeout(9000);
  const chefes = await p.evaluate(() => ({ harg: !document.querySelector("#chefe").hidden, ardis: !document.querySelector("#chefe2").hidden,
    t1: document.querySelector("#chefe b").textContent, t2: document.querySelector("#chefe2 b").textContent,
    r1: document.querySelector("#chefe").getBoundingClientRect(), r2: document.querySelector("#chefe2").getBoundingClientRect() }));
  ok(chefes.harg && chefes.ardis && chefes.r1.right <= chefes.r2.left + 1, `as barras de Harg e Ardis, lado a lado: ${chefes.t1} | ${chefes.t2}`);
  await p.screenshot({ path: `${SAIDA}/cl6-herois-${w}.png` });
  // a carga de cavalaria, no campo aberto
  if (w === 1920) {
    await p.goto(BASE + "?enc=carga&compA=pesada&auto=1&robo=1", { waitUntil: "networkidle" });
    await p.waitForTimeout(6500);
    await p.screenshot({ path: `${SAIDA}/cl6-carga-${w}.png` });
  }
  // o Campo Livre 5 ainda abre em /v5/
  await p.goto(BASE + "v5/", { waitUntil: "networkidle" });
  const v5 = await p.evaluate(() => ({ titulo: document.title, encontros: document.querySelectorAll("#encontros .encontro").length }));
  ok(v5.titulo.startsWith("Campo Livre 5") && v5.encontros === 5, `o Campo Livre 5 abre em /v5/ (${v5.titulo}, ${v5.encontros} encontros)`);
  ok(!erros.length, `sem erros no console ${erros.slice(0, 3).join(" | ")}`);
  await p.close();
}
await nav.close();
console.log(falhas.length ? `${falhas.length} FALHAS` : "tudo certo");
process.exit(falhas.length ? 1 : 0);
