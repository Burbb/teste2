// Cliques seguidos, como o navegador conta (o 2º e o 3º clique rápidos chegam com detail 2 e 3): cada clique
// deliberado tem de valer. Confere, no jogo de verdade:
//   - a roda da luta: Habilidades e Itens abrem e fecham a cada clique (a cada 120, 250 e 700 ms), a troca entre os
//     dois, a tecla 2 segurada (abre uma vez), o Esc, e o clique duplo numa habilidade (uma escolha só: a mira);
//   - o mercado: peças diferentes clicadas sem parar vendem cada uma; a grade fica parada durante a visita (o espaço
//     vendido fica vazio, o clique nele não faz nada, o clique duplo vende uma, a troca de aba e a recompra não
//     embaralham; equipar e arrastar até a banca também não) e volta à ordem de sempre na visita seguinte;
//   - a comitiva: as cartas ✉ de dois companheiros clicadas uma logo depois da outra abrem as duas conversas, em ordem;
//     a carta ✉ com o Inventário ou o Bestiário aberto fecha a tela e abre a conversa na hora;
//   - o relatório da luta: o primeiro clique no Continuar fecha; a rajada de antes do botão não fecha sozinha.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node tests/navegador/cliques_seguidos.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
// O Python que sobe os cenários: PYTHON=<executável>, se não for o de sempre (python no Windows, python3 nos outros).
const PYTHON = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
let falhas = 0;
const conferir = (ok, texto) => { console.log(`${ok ? "  ok " : "FALHA"}  ${texto}`); if (!ok) falhas++; };
function subir(cenario, amb) {
  const proc = spawn(PYTHON, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, VELOCIDADE: "normal", PYTHONPATH: raiz, ...amb } });
  return new Promise((ok, falha) => {
    let url = null;
    proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m && !url) { url = m[0]; ok({ proc, url }); } });
    setTimeout(() => { if (!url) falha(new Error(`o cenário ${cenario} não subiu`)); }, 30000);
  });
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const erros = [];
async function pagina(url) {
  const p = await b.newPage({ viewport: { width: 1500, height: 950 } });
  p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  return p;
}
async function ate(p, cond, max = 120) {
  for (let k = 0; k < max; k++) {
    if (await p.evaluate(cond)) return true;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  return false;
}
// cliques no mesmo ponto, contados como o navegador conta (1, 2, 3...) quando vêm a menos de 500 ms um do outro
async function cliques(p, el, vezes, intervalo, depois) {
  const r = await el.boundingBox(), x = r.x + r.width / 2, y = r.y + r.height / 2;
  await p.mouse.move(x, y);
  const estados = [];
  for (let k = 1; k <= vezes; k++) {
    const n = intervalo < 500 ? k : 1;
    await p.mouse.down({ clickCount: n }); await p.mouse.up({ clickCount: n });
    await espera(intervalo);
    if (depois) estados.push(await depois());
  }
  return estados;
}

// 1. a roda da luta
{
  const { proc, url } = await subir("tutorial", { TUTORIAL: "0", LUTA: "lobo", NIVEL: "12", CLASSE: "guerreiro", ESPEC: "berserker", VISTAS: "A1,V2,N1,D1,K1,M1,L1" });
  const p = await pagina(url);
  const naVez = () => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="habilidades"]');
  await ate(p, naVez);
  await espera(500);
  const aberto = () => p.evaluate(() => (document.querySelector(".roda-janela") || {}).dataset?.tipo || "fechado");
  for (const intervalo of [120, 250, 700]) {
    const seq = await cliques(p, await p.$('#roda .roda-botao[data-slot="habilidades"]'), 4, intervalo, aberto);
    conferir(seq.join(" ") === "habilidades fechado habilidades fechado", `Habilidades a cada ${intervalo} ms: ${seq.join(" → ")}`);
  }
  for (const intervalo of [120, 700]) {
    const seq = await cliques(p, await p.$('#roda .roda-botao[data-slot="itens"]'), 4, intervalo, aberto);
    conferir(seq.join(" ") === "itens fechado itens fechado", `Itens a cada ${intervalo} ms: ${seq.join(" → ")}`);
  }
  const hb = await p.$('#roda .roda-botao[data-slot="habilidades"]'), ib = await p.$('#roda .roda-botao[data-slot="itens"]');
  await hb.click(); await espera(150); await ib.click(); await espera(150);
  const a = await aberto(); await ib.click(); await espera(150); const f = await aberto(); await hb.click(); await espera(150); const h = await aberto();
  conferir(a === "itens" && f === "fechado" && h === "habilidades", `Habilidades → Itens → Itens → Habilidades: ${a}, ${f}, ${h}`);
  await p.keyboard.press("Escape"); await espera(200);
  conferir((await aberto()) === "fechado", "Esc fecha");
  await p.keyboard.down("2"); for (let k = 0; k < 6; k++) { await espera(35); await p.keyboard.down("2"); } await p.keyboard.up("2"); await espera(250);
  conferir((await p.$$eval(".roda-janela", (x) => x.length)) === 1, "a tecla 2 segurada abre uma vez");
  await p.keyboard.press("Escape"); await espera(200);
  await hb.click(); await espera(300);
  const linha = await p.$('.roda-janela .rj-linha[data-hab="golpe_pesado"]');
  await cliques(p, linha, 2, 60);
  await espera(900);
  conferir(!!(await p.$(".roda-mira")) && (await p.evaluate(() => !!pergunta && !processando)), "clique duplo numa habilidade: uma escolha, a mira, a vez continua");
  const v = await p.$(".mira-voltar"); if (v) await v.click();
  conferir(await ate(p, naVez, 40), "o Voltar da mira devolve a roda");
  await p.close(); proc.kill();
}

// 2. o mercado: vender em sequência, com a grade parada durante a visita
{
  const { proc, url } = await subir("mercado", { CLASSE: "guerreiro", SEMENTE: "1" });
  const p = await pagina(url);
  await ate(p, () => !!document.querySelector('[data-aba="vender"]'));
  await espera(600);
  await (await p.$('[data-aba="vender"]')).click(); await espera(700);
  // a grade: a ficha de cada espaço ("" no vazio), o ouro, a mochila do motor e o contador da aba
  const grade = () => p.evaluate(() => ({
    pecas: [...document.querySelectorAll('[data-painel="vender"] .mochila-grade:not(.recompra) .celula')].map((c) => c.dataset.peca || ""),
    ouro: App.estado.heroi.ouro, mochila: App.estado.heroi.mochila.length, ocupado: document.querySelector('[data-painel="vender"] .loja-mochila b').textContent,
    precos: Object.fromEntries([...document.querySelectorAll("[data-peca]")].map((c) => [c.dataset.peca, Number(c.querySelector(".preco-canto").textContent)])),
    recompra: document.querySelectorAll("[data-recomprar]").length }));
  const centro = (k) => p.evaluate((k) => { const c = document.querySelectorAll('[data-painel="vender"] .mochila-grade:not(.recompra) .celula')[k].getBoundingClientRect(); return [c.left + c.width / 2, c.top + c.height / 2]; }, k);
  const assentar = async () => { for (let k = 0; k < 60; k++) { if (await p.evaluate(() => !processando && !!pergunta)) break; await espera(100); } await espera(400); };
  const g0 = await grade();
  // quatro peças diferentes, um clique em cada, a 150 ms um do outro (as respostas chegam no meio)
  const pontos = []; for (let k = 0; k < 4; k++) pontos.push(await centro(k));
  for (const pt of pontos) { await p.mouse.click(...pt); await espera(150); }
  await assentar(); await espera(1500);
  const g1 = await grade();
  const pagos = g0.pecas.slice(0, 4).reduce((s, n) => s + g0.precos[n], 0);
  conferir(g1.mochila === g0.mochila - 4 && g1.ouro === g0.ouro + pagos, `quatro peças diferentes, clicadas sem parar, vendem as quatro (${g0.mochila} → ${g1.mochila}, ouro +${g1.ouro - g0.ouro} de ${pagos})`);
  conferir(g1.pecas.slice(0, 4).every((x) => x === "") && g1.pecas.slice(4).join() === g0.pecas.slice(4).join(),
    `os espaços vendidos ficam vazios e as outras peças não se mexem (${g0.pecas.join(",")} → ${g1.pecas.join(",")})`);
  conferir(g1.ocupado === `${g1.mochila}/12` && g1.recompra === 4, `contador e recompra acompanham (${g1.ocupado}, ${g1.recompra} para recomprar)`);
  await p.mouse.click(...(await centro(0))); await assentar();
  conferir((await grade()).mochila === g1.mochila, "clique num espaço vazio não faz nada");
  const pt4 = await centro(4);
  await p.mouse.dblclick(...pt4); await assentar(); await espera(500);
  const g2 = await grade();
  conferir(g2.mochila === g1.mochila - 1 && g2.pecas[4] === "" && g2.pecas.slice(5).join() === g1.pecas.slice(5).join(), `clique duplo vende uma peça só (${g1.mochila} → ${g2.mochila})`);
  // um clique e a troca de aba logo em seguida, com a venda ainda a caminho: volta igual
  await p.mouse.click(...(await centro(5)));
  await (await p.$('[data-aba="suprimentos"]')).click(); await espera(60); await (await p.$('[data-aba="vender"]')).click();
  await assentar(); await (await p.$('[data-aba="suprimentos"]')).click(); await espera(300); await (await p.$('[data-aba="vender"]')).click(); await espera(300);
  const g3 = await grade();
  conferir(g3.mochila === g2.mochila - 1 && g3.pecas[5] === "" && g3.pecas.slice(6).join() === g2.pecas.slice(6).join(), `trocar de aba com a venda a caminho: vendida, e a grade igual (${g3.pecas.join(",")})`);
  // recomprar: a peça volta ao primeiro espaço vazio, sem cobrir nenhuma
  await (await p.$("[data-recomprar]")).click(); await assentar(); await espera(500);
  const g4 = await grade();
  const ocupados = g4.pecas.filter(Boolean).length;
  conferir(g4.mochila === g3.mochila + 1 && ocupados === g4.mochila && g4.pecas[0] !== "" && g4.pecas.slice(1).join() === g3.pecas.slice(1).join() && g4.pecas.length === 12,
    `recomprar ocupa o primeiro espaço vazio (${g4.pecas.join(",")})`);
  // equipar pelo botão direito: a peça vestida sai do espaço dela, e o que sai do corpo vai para o primeiro vazio (o
  // mesmo espaço, se ele for o primeiro: uma troca no lugar); o resto fica parado
  const usavel = await p.evaluate(() => { const c = [...document.querySelectorAll('[data-painel="vender"] .mochila-grade:not(.recompra) .celula')];
    return c.findIndex((x) => x.dataset.peca && !x.classList.contains("inutil") && !/Anel/.test(x.getAttribute("aria-label"))); });
  if (usavel >= 0) {
    await p.mouse.click(...(await centro(usavel)), { button: "right" }); await assentar(); await espera(500);
    const g5 = await grade(), primeiro = Math.min(usavel, g4.pecas.findIndex((x) => x === ""));
    const fora = (g) => g.pecas.map((x, s) => (s === usavel || s === primeiro ? "" : x)).join();
    conferir(fora(g5) === fora(g4) && g5.pecas[usavel] !== g4.pecas[usavel] && g5.pecas.filter(Boolean).length === g5.mochila,
      `equipar pelo botão direito não embaralha a grade (${g4.pecas.join(",")} → ${g5.pecas.join(",")})`);
  }
  // arrastar até a banca também vende, a peça arrastada, e o espaço dela fica vazio
  const ga = await grade(), sa = ga.pecas.findIndex((x, s) => x && s > 0);
  await p.dragAndDrop(`[data-peca="${ga.pecas[sa]}"]`, ".loja-banca"); await assentar(); await espera(500);
  const gb = await grade();
  conferir(gb.mochila === ga.mochila - 1 && gb.pecas[sa] === "" && gb.pecas.filter((x, s) => s !== sa).join() === ga.pecas.filter((x, s) => s !== sa).join(),
    `arrastar até a banca vende a peça arrastada (${ga.pecas.join(",")} → ${gb.pecas.join(",")})`);
  // sair e voltar: a mochila na ordem de sempre (as peças juntas no começo)
  await p.keyboard.press("Escape");
  await ate(p, () => !!document.querySelector('#predios .predio[data-predio="mercado"]'));
  await espera(600);
  await (await p.$('#predios .predio[data-predio="mercado"]')).click();
  await ate(p, () => !!document.querySelector('[data-aba="vender"]'));
  await espera(600); await (await p.$('[data-aba="vender"]')).click(); await espera(500);
  const g6 = await grade();
  conferir(g6.pecas.slice(0, g6.mochila).every(Boolean) && g6.pecas.slice(g6.mochila).every((x) => x === ""), `ao voltar ao mercado, a ordem de sempre (${g6.pecas.map((x) => (x ? "■" : "·")).join("")})`);
  await p.close(); proc.kill();
}

// 3. a comitiva: duas conversas seguidas
{
  const { proc, url } = await subir("fogueira", { LUGAR: "vau", CONVERSA: "1", COMITIVA: "morel,odete", RESERVA: "" });
  const p = await pagina(url);
  await ate(p, () => document.querySelectorAll("[data-conversar]").length >= 2 && !!pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some(atalhoDe));
  await espera(600);
  const caixas = await p.$$eval("[data-conversar]", (x) => x.map((e) => { const r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }));
  await p.mouse.click(...caixas[0]); await espera(250); await p.mouse.click(...caixas[1]);  // no mesmo lugar, mesmo que a carta se redesenhe
  const vistas = [];
  for (let k = 0; k < 300 && vistas.length < 2; k++) {
    const t = await p.evaluate(() => (document.getElementById("cena-cab") || {}).textContent || "");
    for (const nome of ["Morel", "Odette"]) if (new RegExp("Conversa com[^•]*" + nome).test(t) && !vistas.includes(nome)) vistas.push(nome);
    if (await p.evaluate(() => pergunta && pergunta.tipo === "opcoes" && !pergunta.opcoes.some(atalhoDe))) { const e = await p.$("#prompt .escolha"); if (e) await e.click().catch(() => {}); }
    const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
    await espera(150);
  }
  conferir(vistas.join(",") === "Morel,Odette", `as cartas ✉ de dois companheiros, uma logo depois da outra: ${vistas.join(", ") || "nenhuma"}`);
  await p.close(); proc.kill();
}

// 4. a carta ✉ com uma tela da doca aberta: a tela fecha e a conversa abre na hora, sem outro clique (antes ela
// ficava guardada até a pessoa fechar a tela)
for (const tela of ["Inventário", "Bestiário"]) {
  const { proc, url } = await subir("fogueira", { LUGAR: "vau", CONVERSA: "1", COMITIVA: "odete", RESERVA: "" });
  const p = await pagina(url);
  await ate(p, () => !!document.querySelector('[data-conversar="odete"]') && !!pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some(atalhoDe));
  await espera(600);
  await p.click(`#doca .atalho[data-rotulo="${tela}"]`);
  let aberta = false;  // sem o ate(): ele clicaria no Continuar do Bestiário
  for (let k = 0; k < 80 && !aberta; k++) { aberta = await p.evaluate((t) => docaTela === t && !!pergunta && !processando, tela); await espera(100); }
  await espera(300);
  const c = await p.$('[data-conversar="odete"]');
  await cliques(p, c, 2, 120);  // um clique duplo: a conversa abre uma vez
  let conversa = false;
  for (let k = 0; k < 60 && !conversa; k++) {
    conversa = await p.evaluate(() => /Conversa com[^•]*Odette/.test((document.getElementById("cena-cab") || {}).textContent || ""));
    await espera(100);
  }
  const fim = await p.evaluate(() => ({ docaTela, guardadas: conversasGuardadas.length, atual: !!document.querySelector("#doca .atalho.atual") }));
  conferir(aberta && conversa && fim.docaTela === null && !fim.guardadas && !fim.atual,
    `a carta ✉ com o ${tela} aberto: ele fecha e a conversa com a Odette abre na hora (${JSON.stringify({ aberta, conversa, ...fim })})`);
  await p.close(); proc.kill();
}

// 5. o Continuar do relatório da luta (o espólio): o primeiro clique logo que ele aparece fecha; a rajada que vinha
// adiantando os números não fecha sozinha, e o clique novo depois dela fecha uma vez
{
  const { proc, url } = await subir("relatorio", { VEZES: "3" });
  const p = await pagina(url);
  let respostas = 0;
  p.on("request", (r) => { if (r.url().includes("/responder")) respostas++; });
  const luta = async () => {
    await ate(p, () => !processando && !!pergunta && pergunta.tipo === "opcoes" && pergunta.opcoes.some((o) => /^Explorar/.test(o.texto)));
    await espera(500);
    await p.click("#prompt .escolha");
    for (let k = 0; k < 3000 && !(await p.$(".festa-espolio")); k++) {
      await p.evaluate(() => {
        if (processando || !pergunta || pergunta.tipo !== "opcoes") return;
        const i = pergunta.opcoes.findIndex((o) => !(o.meta && o.meta.indisponivel) && !/^Explorar/.test(o.texto));
        if (i >= 0 && !pergunta.opcoes.some((o) => /^Explorar/.test(o.texto))) responder(pergunta.id, i);
      });
      await espera(30);
    }
  };
  const aberto = () => p.$(".festa-espolio .continuar").then(Boolean);
  const fechou = async (ms) => { for (let t = 0; t < ms; t += 20) { if (!(await p.$(".festa-espolio"))) return true; await espera(20); } return false; };
  const fecharNivel = async () => { for (let k = 0; k < 5; k++) { const c = await p.$("#celebracao button.continuar"); if (!c) return; await c.click(); await espera(600); } };
  await luta();
  for (let k = 0; k < 400 && !(await aberto()); k++) await espera(20);
  const bt = await (await p.$(".festa-espolio .continuar")).boundingBox();
  respostas = 0;
  await p.mouse.click(bt.x + bt.width / 2, bt.y + bt.height / 2);
  conferir(await fechou(600) && respostas === 0, `um clique no Continuar logo que ele aparece fecha o relatório (${respostas} respostas)`);
  await espera(800); await fecharNivel();
  await luta();
  const q = await (await p.$(".festa-espolio")).boundingBox(), x = q.x + q.width / 2, y = q.y + q.height / 2;
  await p.mouse.move(x, y);
  let n = 1, depois = 0;
  while (depois < 4) {  // cliques no mesmo ponto a cada 150 ms (detail 1, 2, 3...), até 600 ms depois de o botão aparecer
    await p.mouse.down({ clickCount: n }); await p.mouse.up({ clickCount: n }); n++;
    await espera(150);
    if (await aberto()) depois++;
  }
  conferir(await aberto(), "a rajada que adiantava os números não fecha o relatório sozinha");
  await espera(700);
  respostas = 0;
  await p.mouse.click(x, y);
  conferir(await fechou(600) && respostas === 0, `depois da rajada, um clique novo fecha (uma vez: ${respostas} respostas)`);
  await p.close(); proc.kill();
}

await b.close();
conferir(!erros.length, erros.length ? `erros no console: ${erros.join(" | ")}` : "sem erros no console");
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
