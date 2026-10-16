// Cliques seguidos, como o navegador conta (o 2º e o 3º clique rápidos chegam com detail 2 e 3): cada clique
// deliberado tem de valer. Confere, no jogo de verdade:
//   - a roda da luta: Habilidades abre e fecha a cada clique (a cada 120, 250 e 700 ms), a troca entre Habilidades e
//     Itens, a tecla 2 segurada (abre uma vez), o Esc, e o clique duplo numa habilidade (uma escolha só: a mira);
//   - o mercado: quatro cliques seguidos na primeira peça da mochila vendem quatro peças;
//   - a comitiva: as cartas ✉ de dois companheiros clicadas uma logo depois da outra abrem as duas conversas, em ordem.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node tests/navegador/cliques_seguidos.mjs
import { spawn } from "child_process";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const raiz = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
let falhas = 0;
const conferir = (ok, texto) => { console.log(`${ok ? "  ok " : "FALHA"}  ${texto}`); if (!ok) falhas++; };
function subir(cenario, amb) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, VELOCIDADE: "normal", PYTHONPATH: raiz, ...amb } });
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

// 2. o mercado: vender em sequência
{
  const { proc, url } = await subir("mercado", { CLASSE: "guerreiro", SEMENTE: "1" });
  const p = await pagina(url);
  await ate(p, () => !!document.querySelector('[data-aba="vender"]'));
  await espera(600);
  await (await p.$('[data-aba="vender"]')).click(); await espera(700);
  const n0 = await p.$$eval(".tela.loja [data-mochila-loja]", (x) => x.length);
  await cliques(p, await p.$(".tela.loja [data-mochila-loja]"), 4, 150);
  await espera(3000);
  const n1 = await p.$$eval(".tela.loja [data-mochila-loja]", (x) => x.length);
  conferir(n1 === n0 - 4, `quatro cliques seguidos na mochila vendem quatro peças (${n0} → ${n1})`);
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

await b.close();
conferir(!erros.length, erros.length ? `erros no console: ${erros.join(" | ")}` : "sem erros no console");
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
