// Os GESTOS do d20 (protótipo; nada no jogo): o jogo atual e as propostas com os mesmos casos e os mesmos gestos; as
// propostas têm de se comportar como o atual (o ritmo, pular, nada atravessar para a tela seguinte) e mostrar o d20
// do motor. Escreve uma linha por verificação e capturas/gestos.json.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/d20/auxiliares/gestos.mjs
// O que confere, em cada versão:
//  - o ritmo: da tirinha à consequência (o mesmo do atual, 950 ms + ritmo(650) + o texto);
//  - o número: o canvas do resultado é, pixel a pixel, o dado desenhado com o d20 da mensagem (A e B);
//  - pular com um clique e com o Esc no meio do giro: o centro some logo e o resultado é o mesmo;
//  - cliques rápidos (quatro, a 90 ms) e uma tecla segurada (Enter, repetida) durante a rolagem: nenhuma resposta sai
//    sozinha na tela seguinte (a pausa depois do baú continua esperando);
//  - movimento reduzido: o mesmo tempo, nenhum efeito de pouso nem animação no dado;
//  - texto instantâneo: nada no centro, a tirinha com o d20 do motor;
//  - nada acumula: depois de cada rolagem, nenhum centro nem efeito de pouso na página.
import { writeFileSync } from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { subir, rolar, resultado, medirRitmo } from "./fotografar.mjs";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const JANELA = { width: 1920, height: 945 };
const VERSOES = (process.env.VERSOES ?? ",a,b").split(",");
const rel = [];
const conta = (v, nome, ok, dados = {}) => { const r = { versao: v || "atual", nome, ok, ...dados }; rel.push(r); console.log(JSON.stringify(r)); };

async function pagina(b, caso, v, { reduzido = false, velocidade = "normal" } = {}) {
  const { proc, url } = await subir(caso, v, velocidade);
  const ctx = await b.newContext({ viewport: JANELA, reducedMotion: reduzido ? "reduce" : "no-preference" });
  const p = await ctx.newPage();
  const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
  await p.goto(url);
  await medirRitmo(p);
  // as respostas que a página manda (as duas do caso: "Começar" e a escolha no baú; o resto seria um gesto que atravessou)
  await p.evaluate(() => { window.__resp = []; const r = window.responder; window.responder = (...a) => { window.__resp.push(a); return r(...a); }; });
  return { p, erros, fechar: async () => { await ctx.close(); proc.kill(); } };
}
const respostasDepois = (p) => p.evaluate(() => window.__resp.length - 2);
const limpo = (p) => p.evaluate(() => !document.querySelector(".rolagem-centro") && !document.querySelector(".d20p-pouso"));

const b = await chromium.launch();
for (const v of VERSOES) {
  // o ritmo, o número e nada acumulado (sucesso e falha)
  for (const caso of ["sucesso", "falha", "critico"]) {
    const { p, erros, fechar } = await pagina(b, caso, v);
    try {
      await rolar(p, caso);
      await p.waitForSelector(".rolagem-centro.pousou", { timeout: 5000 });
      const numero = v ? await p.evaluate(() => {
        const cv = document.querySelector(".rolagem-centro .d20p-centro"), msg = /d20 (\d+)\)/.exec([...document.querySelectorAll("#historico-lista p")].map((e) => e.textContent).pop());
        const d20 = +msg[1], sucesso = / sucesso /.test([...document.querySelectorAll("#historico-lista p")].pop().textContent);
        const est = d20 === 20 ? "critico" : d20 === 1 ? "desastre" : sucesso ? "sucesso" : "falha";
        const ref = D20Proto.tela(D20Proto.qual === "a" ? "marfim" : "vidro", "centro");
        D20Proto.desenhar(ref, D20Proto.qual === "a" ? "marfim" : "vidro", "centro", { n: d20, estado: est });
        const a = cv.getContext("2d").getImageData(0, 0, cv.width, cv.height).data, r = ref.getContext("2d").getImageData(0, 0, ref.width, ref.height).data;
        return { d20, iguais: a.length === r.length && a.every((x, i) => x === r[i]) };
      }) : null;
      await p.waitForFunction(() => window.__t.depois, null, { timeout: 6000 });
      await espera(400);
      conta(v, `${caso}: ritmo e resultado`, !erros.length && (!numero || numero.iguais), { resultado: await resultado(p),
        tirinha_a_consequencia_ms: await p.evaluate(() => Math.round(window.__t.depois - window.__t.rolagem)), numero, limpo: await limpo(p), erros });
    } finally { await fechar(); }
  }
  // pular: um clique e o Esc no meio do giro
  for (const gesto of ["clique", "Escape"]) {
    const { p, erros, fechar } = await pagina(b, "sucesso", v);
    try {
      await rolar(p, "sucesso");
      await p.waitForSelector(".rolagem-centro", { timeout: 5000 }); await espera(300);
      const t = Date.now();
      if (gesto === "clique") await p.mouse.click(960, 600); else await p.keyboard.press("Escape");
      await p.waitForFunction(() => !document.querySelector(".rolagem-centro"), null, { timeout: 5000 });
      const ms = Date.now() - t;
      await espera(1500);
      const n = await respostasDepois(p);
      conta(v, `pular (${gesto})`, ms < 400 && n === 0 && !erros.length, { centro_some_ms: ms, resultado: await resultado(p), respostas_depois_do_baú: n, limpo: await limpo(p) });
    } finally { await fechar(); }
  }
  // cliques rápidos e tecla segurada durante a rolagem: nada responde a tela seguinte
  for (const gesto of ["cliques", "tecla segurada"]) {
    const { p, erros, fechar } = await pagina(b, "sucesso", v);
    try {
      await rolar(p, "sucesso");
      await p.waitForSelector(".rolagem-centro", { timeout: 5000 }); await espera(200);
      if (gesto === "cliques") for (let i = 0; i < 4; i++) { await p.mouse.click(960, 600); await espera(90); }
      else { for (let i = 0; i < 12; i++) { await p.keyboard.down("Enter"); await espera(60); } await p.keyboard.up("Enter"); }
      await espera(2500);
      const n = await respostasDepois(p);
      const esperando = await p.evaluate(() => !!pergunta);
      conta(v, `${gesto} durante a rolagem`, n === 0 && esperando && !erros.length, { respostas_depois_do_baú: n, tela_seguinte_esperando: esperando, resultado: await resultado(p), limpo: await limpo(p) });
    } finally { await fechar(); }
  }
  // movimento reduzido
  {
    const { p, erros, fechar } = await pagina(b, "falha", v, { reduzido: true });
    try {
      await rolar(p, "falha");
      await p.waitForSelector(".rolagem-centro.pousou", { timeout: 5000 });
      await espera(80);
      const anim = await p.evaluate(() => ({ pouso: !!document.querySelector(".d20p-pouso"),
        animacoes_no_dado: [...document.querySelectorAll(".rolagem-centro .d20p, .rolagem-centro .rc-dado svg")].reduce((s, e) => s + e.getAnimations().length, 0) }));
      await p.waitForFunction(() => window.__t.depois, null, { timeout: 6000 });
      conta(v, "movimento reduzido", !anim.pouso && !anim.animacoes_no_dado && !erros.length, { ...anim, resultado: await resultado(p),
        tirinha_a_consequencia_ms: await p.evaluate(() => Math.round(window.__t.depois - window.__t.rolagem)) });
    } finally { await fechar(); }
  }
  // texto instantâneo
  {
    const { p, erros, fechar } = await pagina(b, "sucesso", v, { velocidade: "instantaneo" });
    try {
      await p.evaluate(() => { window.__centro = false; new MutationObserver(() => { if (document.querySelector(".rolagem-centro")) window.__centro = true; }).observe(document.body, { childList: true }); });
      await rolar(p, "sucesso"); await espera(1500);
      const centro = await p.evaluate(() => window.__centro);
      conta(v, "texto instantâneo", !centro && !erros.length, { apareceu_no_centro: centro, resultado: await resultado(p) });
    } finally { await fechar(); }
  }
}
await b.close();
writeFileSync(path.join(aqui, "..", "capturas", "gestos.json"), JSON.stringify(rel, null, 1));
console.log(`${rel.filter((r) => r.ok).length}/${rel.length} ok`);
