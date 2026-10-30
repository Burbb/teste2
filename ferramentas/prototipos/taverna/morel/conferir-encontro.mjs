// Confere o encontro com Morel no protótipo (demo.py, save temporário), a 1920×945 e a 1280×720, pelo caminho normal:
// entra na taverna (o balcão), senta com o homem do canto (a vista da mesa, com as opções do evento embaixo), e em cada
// caso de teste da faixa confere o que o motor decide e o que a tela mostra:
//   - pagar 40 (60 de ouro): a cobrança única mesmo com clique duplo e tecla repetida, as moedas lançadas uma vez,
//     a colher parando, as moedas na mesa até o fim, e a volta ao balcão sem o cartão do homem do canto;
//   - perder a queda de braço e pagar 25 (30 de ouro, o dado em 1): sem a opção dos 40, a mesma animação, 30 → 5;
//   - perder sem os 25 (10 de ouro): a pergunta dos 25 não aparece, nada é cobrado, volta ao balcão;
//   - vencer (o dado em 20): nada cobrado, nenhuma moeda;
//   - recusar e, já conhecido, Morel pela bebida: o nome da mesa ("do homem do canto" / "de Morel");
//   - o vazio: a apresentação normal; o teclado (os números), o movimento reduzido (as moedas já assentadas, Morel parado).
// Fotos em <SAIDA> (padrão: morel/capturas, fora do git).
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/taverna/morel/conferir-encontro.mjs
import { spawn } from "child_process";
import { mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const SAIDA = process.env.SAIDA || path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const MENU = "#prompt .escolhas:not(.escolhido) .escolha";
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };

const proc = spawn(PY, [path.join(raiz, "ferramentas", "prototipos", "taverna", "demo.py")], { cwd: raiz,
  env: { ...process.env, VELOCIDADE: "rapido", SEM_NAVEGADOR: "1", DEMO_PORTA: process.env.DEMO_PORTA || "8797", PYTHONIOENCODING: "utf-8" } });
let url = null;
proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) url = m[0]; });
proc.stderr.on("data", (d) => process.stderr.write(d));
for (let k = 0; k < 400 && !url; k++) await espera(100);
if (!url) { proc.kill(); throw new Error("a demonstração não subiu"); }

const ouro = (p) => p.evaluate(() => App.estado.heroi.ouro);
const cena = (p) => p.evaluate(() => { const a = window.Cenas && Cenas.atual(); return a ? { cena: a.d.cena,
  titulo: a.d.titulo, pagamentos: a.d.pagamentos || 0, lances: (a.est.tavLances || []).length } : null; });
const opcoes = (p) => p.$$eval(MENU, (es) => es.map((e) => e.textContent.replace(/\s+/g, " ").trim()));
const cartoes = (p) => p.$$eval("#folha .servico", (es) => es.map((e) => e.dataset.servico));
async function parado(p) {
  for (let k = 0; k < 80 && !(await p.$(MENU)) && !(await p.$("#folha .servico")); k++) {
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(300);
  }
  await espera(400);
}
const naTaverna = (p) => p.waitForFunction(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna"
  && document.querySelectorAll("#folha .servico").length > 0, null, { timeout: 15000 }).then(() => true, () => false);
const naMesa = (p) => p.waitForFunction(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna_mesa"
  && document.querySelectorAll("#prompt .escolhas:not(.escolhido) .escolha").length > 0, null, { timeout: 15000 }).then(() => true, () => false);
async function entrar(p) {
  if (await p.evaluate(() => window.Cenas && Cenas.atual() && Cenas.atual().d.cena === "taverna")) return true;
  await parado(p);
  await p.click('[data-predio="taverna"]');
  const ok = await naTaverna(p);
  await espera(600);
  return ok;
}
async function faixa(p, attr, id) {
  await p.click("#faixa-tav .abre");
  await p.click(`#faixa-tav-painel [data-${attr}="${id}"]`);
  await espera(700);
  const aviso = await p.$eval("#faixa-tav .aviso", (e) => e.textContent);
  if (aviso) console.log(`   (a faixa: ${aviso})`);
  await parado(p);
  return entrar(p);
}
/** Escolhe a opção do menu cujo texto começa com `ini`; `duplo`: dois cliques seguidos e a tecla repetida. */
async function escolher(p, ini, duplo = false) {
  const i = (await opcoes(p)).findIndex((t) => t.includes(ini));
  if (i < 0) return false;
  const el = (await p.$$(MENU))[i];
  if (duplo) { await el.dblclick(); await p.keyboard.press(String(i + 1)); await p.keyboard.press(String(i + 1)); } else await el.click();
  return true;
}
async function proxima(p) {  // espera a próxima pergunta (as opções do evento) ou o balcão
  for (let k = 0; k < 60; k++) {
    await espera(250);
    const c = await p.$("#prompt .continuar"); if (c) { await c.click().catch(() => {}); continue; }
    if ((await p.$(MENU)) || (await p.$("#folha .servico"))) break;
  }
  await espera(300);
}
async function sentar(p) {
  const card = await p.$('#folha .servico[data-servico="morel"]');
  if (!card) return false;
  await card.click();
  return naMesa(p);
}

const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
try {
  for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
    const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
    console.log(`== ${W}×${H}`);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    p.on("console", (m) => { if (m.type() === "error") erros.push(m.text()); });
    await p.goto(url); await parado(p);
    conferir(await entrar(p), "entra na taverna: o balcão");
    await faixa(p, "tav", "homem_do_canto");  // a mesma demonstração serve as duas janelas: o começo de novo
    conferir((await cartoes(p)).includes("morel"), "o cartão Sentar com o homem do canto no balcão");

    // 1. pagar 40, com clique duplo e tecla repetida
    conferir(await sentar(p), "sentar com o homem do canto abre a mesa de Morel");
    let c = await cena(p);
    conferir(c.titulo === "A mesa do homem do canto", `antes de conhecê-lo, a mesa do homem do canto (${c.titulo})`);
    let ops = await opcoes(p);
    console.log("   opções:", JSON.stringify(ops));
    conferir(ops.some((t) => t.includes("Pagar 40")) && ops.some((t) => t.includes("Queda de braço")) && ops.some((t) => t.includes("Vazio"))
      && ops.some((t) => t.includes("Recusar")), "as quatro opções do evento");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-opcoes.png`) });
    const antes = await ouro(p);
    await escolher(p, "Pagar 40", true);
    await espera(450);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-moedas-voando.png`) });
    await proxima(p);
    c = await cena(p);
    conferir(await ouro(p) === antes - 40, `pagar 40: ${antes} → ${await ouro(p)}`);
    conferir(c.cena === "taverna_mesa" && c.pagamentos === 1 && c.lances === 1, `um pagamento, um lance (${JSON.stringify(c)})`);
    await espera(1500);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-moedas-assentadas.png`) });
    ops = await opcoes(p);
    console.log("   depois:", JSON.stringify(ops));
    await escolher(p, "Aceitar");
    await proxima(p);
    conferir(await naTaverna(p), "depois da conversa, de volta ao balcão");
    conferir(!(await cartoes(p)).includes("morel"), "recrutado, o cartão do homem do canto sai do balcão");
    conferir(await ouro(p) === antes - 40, `nada cobrado de novo (${await ouro(p)})`);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-balcao-depois.png`) });

    // 2. perder a queda de braço e pagar 25 (30 de ouro, o dado em 1): pela tecla do número
    await faixa(p, "tav", "pouco_ouro");
    await faixa(p, "dado", "perder");
    conferir(await sentar(p), "30 de ouro: senta com o homem do canto");
    ops = await opcoes(p);
    conferir(!ops.some((t) => t.includes("Pagar 40")), "com 30 de ouro, sem a opção dos 40");
    await p.keyboard.press(String(ops.findIndex((t) => t.includes("Queda de braço")) + 1));
    await proxima(p);
    ops = await opcoes(p);
    console.log("   depois de perder:", JSON.stringify(ops));
    conferir(ops.some((t) => t.includes("Pagar 25")), "perdeu: a pergunta dos 25");
    conferir((await cena(p)).lances === 0, "nenhuma moeda antes de pagar");
    await escolher(p, "Pagar 25", true);
    await espera(450);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-25-voando.png`) });
    await proxima(p);
    c = await cena(p);
    conferir(await ouro(p) === 5 && c.pagamentos === 1 && c.lances === 1, `pagar 25: 30 → ${await ouro(p)}, um lance (${JSON.stringify(c)})`);
    await espera(1500);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-25-assentadas.png`) });
    await escolher(p, "Recusar");  // recusa a vaga: o ouro já foi (a regra do evento), nada mais acontece
    await proxima(p);
    conferir(await naTaverna(p) && await ouro(p) === 5, `de volta ao balcão, sem outra cobrança (${await ouro(p)})`);

    // 3. perder sem os 25 (10 de ouro): a pergunta não aparece
    await faixa(p, "tav", "quase_sem_ouro");
    conferir(await sentar(p), "10 de ouro: senta com o homem do canto");
    await escolher(p, "Queda de braço");
    await proxima(p);
    conferir(await naTaverna(p), "perdeu sem os 25: a conversa acaba e volta ao balcão");
    conferir(await ouro(p) === 10, `nada cobrado (${await ouro(p)})`);
    conferir(!(await cartoes(p)).includes("morel"), "já apresentado, o cartão do homem do canto sai (a regra da abertura)");

    // 4. vencer (o dado em 20): nenhuma moeda
    await faixa(p, "tav", "homem_do_canto");
    await faixa(p, "dado", "ganhar");
    conferir(await sentar(p), "60 de ouro: senta de novo");
    await escolher(p, "Queda de braço");
    await proxima(p);
    c = await cena(p);
    ops = await opcoes(p);
    conferir(ops.some((t) => t.includes("Aceitar")) && c.lances === 0 && await ouro(p) === 60, `venceu: a vaga, sem moedas nem cobrança (${JSON.stringify(c)})`);
    await escolher(p, "Recusar");
    await proxima(p);
    conferir(await naTaverna(p), "de volta ao balcão");
    await faixa(p, "dado", "sorteio");

    // 5. o vazio: a apresentação normal (a regra e a consequência do evento)
    await faixa(p, "tav", "homem_do_canto");
    conferir(await sentar(p), "senta para o vazio");
    await escolher(p, "Vazio");
    await proxima(p);
    if ((await opcoes(p)).some((t) => t.includes("Aceitar"))) { await escolher(p, "Recusar"); await proxima(p); }
    conferir(await naTaverna(p) && await ouro(p) === 60, "o vazio: sem moedas nem cobrança, de volta ao balcão");

    // 6. Morel já conhecido, pela bebida: o nome da mesa; recusar volta ao balcão
    await faixa(p, "tav", "conhecido");
    conferir(!(await cartoes(p)).includes("morel"), "conhecido: sem o cartão do homem do canto");
    await faixa(p, "bebida", "morel");
    await (await p.$('#folha .servico[data-servico="rumores"]')).click();
    await proxima(p);  // o Continuar depois da bebida paga, como no jogo
    conferir(await naMesa(p), "a bebida chama Morel: a mesa dele");
    c = await cena(p);
    conferir(c.titulo === "A mesa de Morel", `conhecido, a mesa de Morel (${c.titulo})`);
    await p.keyboard.press("Escape");  // sair pelo Esc não responde por uma opção do evento
    await espera(300);
    conferir(await naMesa(p), "o Esc não tira da conversa");
    await escolher(p, "Recusar");
    await proxima(p);
    conferir(await naTaverna(p), "recusar volta ao balcão");
    await faixa(p, "bebida", "sorteio");

    // 7. movimento reduzido: as moedas já assentadas, Morel e o fogo parados
    await faixa(p, "tav", "homem_do_canto");
    await p.click("#faixa-tav .abre"); await p.click("#faixa-tav-painel [data-reduzido]"); await p.click("#faixa-tav .abre");
    conferir(await sentar(p), "pose parada: senta");
    await escolher(p, "Pagar 40");
    await proxima(p);
    const r1 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    await espera(700);
    const r2 = await p.evaluate(() => document.getElementById("vista").toDataURL());
    conferir(r1 === r2 && (await cena(p)).lances === 1, "pose parada: as moedas assentadas e nada se mexe");
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-pose-parada.png`) });
    await escolher(p, "Recusar");
    await proxima(p);
    await p.click("#faixa-tav .abre"); await p.click("#faixa-tav-painel [data-reduzido]"); await p.click("#faixa-tav .abre");

    // 7b. a primeira candidata do canto, no mesmo estado do encontro (a faixa "A mesa do encontro")
    await faixa(p, "tav", "homem_do_canto");
    await p.click("#faixa-tav .abre"); await p.click('#faixa-tav-painel [data-mesa="canto1"]'); await espera(200);
    conferir(await sentar(p), "a primeira candidata do canto: senta com o homem do canto");
    await espera(800);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-canto-v1.png`) });
    await p.click("#faixa-tav .abre"); await p.click('#faixa-tav-painel [data-mesa="canto"]'); await espera(800);
    await p.screenshot({ path: path.join(SAIDA, `${jan}-mesa-canto-revisada.png`) });
    await escolher(p, "Recusar");
    await proxima(p);

    // 8. as três poses da queda de braço na área de cena da HUD (pelo painel), e as folhas de inspeção
    await entrar(p);
    for (const [cand, nome] of [["q3", "q3-disputa"], ["qd1", "disputa"], ["qd2", "vitoria-jogador"], ["qd3", "vitoria-morel"],
                                ["queda1", "v1-disputa"], ["queda2", "v1-vitoria-jogador"], ["queda3", "v1-vitoria-morel"]]) {
      await p.click("#faixa-tav .abre"); await p.click(`#faixa-tav-painel [data-cand="${cand}"]`); await espera(500);
      const v = await p.evaluate(() => { const c = document.getElementById("vista"), r = c.getBoundingClientRect();
        const d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data; let n = 0;
        for (let i = 3; i < d.length; i += 4) if (d[i]) n++;
        return { cheia: n / (d.length / 4), larg: Math.round(r.width), alt: Math.round(r.height) }; });
      conferir(v.cheia > 0.99, `${nome}: a pose desenhada na área de cena (${v.larg}×${v.alt})`);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-queda-${nome}.png`) });
    }
    // o dado rolando com a disputa à vista (a terceira proposta): o grupo inteiro na janela, embaixo da arte, e o véu
    // só na página (tela/rolagem-queda.js); a disputa clara enquanto ele gira
    await p.click("#faixa-tav .abre"); await p.click('#faixa-tav-painel [data-cand="q3"]'); await espera(400);
    const dado = await p.evaluate(async () => {
      const pr = rolagem({ atributo: "Força", cd: 14, d20: 10, mod: 4, total: 14, sucesso: true });
      await new Promise((r) => setTimeout(r, 350));
      const g = document.querySelector(".rolagem-centro .rc-grupo").getBoundingClientRect();
      const v = document.querySelector(".rolagem-centro .rc-veu").getBoundingClientRect();
      const arte = document.getElementById("vista").getBoundingClientRect();
      window.__dadoFim = pr;
      return { inteiro: g.top >= 0 && g.bottom <= innerHeight && g.left >= 0 && g.right <= innerWidth,
        embaixo: g.top >= arte.bottom - 1, veu: v.top >= arte.bottom - 1,
        grupo: [g.left, g.top, g.right, g.bottom].map(Math.round), arte: Math.round(arte.bottom) };
    });
    await p.screenshot({ path: path.join(SAIDA, `${jan}-q3-com-dado.png`) });
    await p.evaluate(() => window.__dadoFim);
    conferir(dado.inteiro && dado.embaixo && dado.veu, `com o dado rolando: o dado inteiro, embaixo da arte, o véu fora da disputa (${JSON.stringify(dado)})`);
    for (const [vista, larg] of [["queda3", 640], ["queda2", 960], ["queda2Estudo", 320], ["queda", 480], ["quedaEstudo", 320]]) {
      await p.click("#faixa-tav .abre"); await p.click(`#faixa-tav-painel [data-estudo="${vista}"]`); await espera(600);
      const est = await p.evaluate(() => { const i = document.querySelector("#estudo-morel img");
        return { aberto: !document.getElementById("estudo-morel").hidden, nat: i.naturalWidth, largura: i.getBoundingClientRect().width }; });
      conferir(est.aberto && est.nat === larg && est.largura % larg === 0, `${vista}: a folha em ampliação inteira (${est.largura / larg}×)`);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-inspecao-${vista}.png`) });
      await p.keyboard.press("Escape"); await espera(200);
    }
    // as folhas da revisão do canto (a mastigação, o tronco, a parede): abrem e carregam (as mais largas que a janela
    // entram na prévia reduzida, dita na legenda)
    for (const [vista, larg] of [["cantoMastigacao", 1028], ["cantoTronco", 1476], ["cantoParede", 1088]]) {
      await p.click("#faixa-tav .abre"); await p.click(`#faixa-tav-painel [data-estudo="${vista}"]`); await espera(600);
      const est = await p.evaluate(() => { const i = document.querySelector("#estudo-morel img");
        return { aberto: !document.getElementById("estudo-morel").hidden, nat: i.naturalWidth }; });
      conferir(est.aberto && est.nat === larg, `${vista}: a folha da revisão abre e carrega`);
      await p.screenshot({ path: path.join(SAIDA, `${jan}-inspecao-${vista}.png`) });
      await p.keyboard.press("Escape"); await espera(200);
    }
    await p.click("#faixa-tav .abre"); await p.click('#faixa-tav-painel [data-cand="g4"]'); await espera(300);
    conferir(erros.length === 0, `o console sem erro${erros.length ? ": " + erros.join(" | ") : ""}`);
    await p.close();
  }
} finally {
  await b.close();
  proc.kill();
}
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
