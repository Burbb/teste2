// A composição compacta INTEGRADA (o jogo como está, sem nenhuma troca na página): os mesmos casos e momentos da
// rodada 2 (../rodada2/fotografar.mjs, a versão "r" aprovada) e a passagem entre tamanhos de janela.
//   casos     Arqueiro patrulheiro (custos de Foco e flechas) e necromante com a comitiva e 3 servos, contra 5 caídos e
//             o xamã, à noite no Charco, em 1280×720: a tela, Habilidades (a descrição mais longa), Itens, a mira
//             (o seletor sai, a ficha volta) e os EFEITOS REAIS (../capturas/efeitos-reais.json, o pior momento de cada
//             especialização contra esse bando), com Habilidades aberto. O necromante também em 1500×950.
//   janelas   o necromante: a luta começa em 1500×950 (o registro embaixo) → 1280×720 (o registro vai para a coluna
//             do mundo) → 1050×720 (a coluna do mundo some: o registro vai para a da ficha; o seletor por cima dela)
//             → 900×720 (sem colunas: embaixo, a página rola) → 1280×720 → 1500×950. Em cada uma: onde está o
//             registro e quantas linhas se leem, se as cartas inimigas estão inteiras à vista (os alvos), a mira; e,
//             no mesmo tamanho, que os efeitos entrando e saindo não mudam o registro de lugar.
//   teclado   o necromante, 1280×720 e 1050×720, movimento reduzido: a tecla 2, as setas, o Tab (nunca a ficha), Esc.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/compacta/integracao/fotografar.mjs
import { spawn } from "child_process";
import { mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const REAIS = JSON.parse(readFileSync(path.join(aqui, "../capturas/efeitos-reais.json"), "utf8")).pior_por_spec;
const BASE = { TUTORIAL: "0", VISTAS: "A1,V2,N1,D1,K1,M1,L1", NIVEL: "12", NIVEL_LUTA: "9", REC: "0.6", LUGAR: "charco", PERIODO: "3",
  GRUPO: "caido:5,xama_caido:1", BOLSA: "pocao_vida=3,tonico=2,bandagem=2,antidoto=1,bomba_fumaca=1,unguento=1,pena_fenix=1" };
const LUTAS = {
  arqueiro: { amb: { ...BASE, CLASSE: "arqueiro", ESPEC: "patrulheiro", ANIMAL: "lobo", COMITIVA: "morel,odete" }, real: "patrulheiro" },
  maior: { amb: { ...BASE, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", SERVOS: "3" }, real: "necromante" },
};
const UM_ALVO = ["bola_fogo", "drenar_vida", "lanca_gelo", "marcar_presa", "tiro_certeiro", "comando_fera", "tiro_duplo"];

async function subir(amb) {
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", "tutorial"], { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[tutorial] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}
const relatorio = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, tam, nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: tam[0], height: tam[1] }, ...opcoes });
  const anotar = (t) => { erros.push(t); console.log(`ERRO NO CONSOLE ${t}`); };
  p.on("pageerror", (e) => anotar(`${nome}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) anotar(`${nome}: ${m.text()}`); });
  await p.goto(url);
  return p;
}
const naVez = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && !!document.querySelector('#roda .roda-botao[data-slot="atacar"]'));
async function vez(p) {
  for (let k = 0; k < 240; k++) {
    if (await naVez(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("a vez do herói não chegou");
}
const slot = (p, s) => p.$(`#roda .roda-botao[data-slot="${s}"]`);
const posicoes = (p) => p.evaluate(() => JSON.stringify([...document.querySelectorAll("#batalha .carta")].map((c) => { const r = c.getBoundingClientRect(); return [c.dataset.uid, Math.round(r.left), Math.round(r.top)]; })));
// a arena e o registro: onde ele está, o tamanho, quantas linhas se leem, as cartas inimigas inteiras à vista
const arena = (p) => p.evaluate(() => {
  const a = document.getElementById("arena").getBoundingClientRect(), pg = document.getElementById("pagina"), r = pg.getBoundingClientRect();
  const lh = parseFloat(getComputedStyle(document.getElementById("texto")).lineHeight) || 24;
  const visivel = Math.max(0, Math.min(r.bottom, innerHeight) - Math.max(r.top, 0));
  const ini = [...document.querySelectorAll("#batalha .inimigos .carta")];
  const inteiras = ini.filter((c) => { const q = c.getBoundingClientRect(); return q.top >= 0 && q.bottom <= innerHeight && q.left >= 0 && q.right <= innerWidth; }).length;
  const nomes = [...document.querySelectorAll("#batalha .carta .carta-nome span")];
  return { janela: `${innerWidth}×${innerHeight}`, arena: Math.round(a.height), registro_em: document.body.dataset.registro || "embaixo da arena",
    registro: `${Math.round(r.width)}×${Math.round(r.height)} px, ${Math.round(visivel)} px à vista (~${Math.floor(visivel / lh)} linhas)`,
    pagina_rola: document.scrollingElement.scrollHeight > innerHeight + 1, inimigos_inteiros_a_vista: `${inteiras} de ${ini.length}`,
    nomes_cortados: nomes.filter((e) => e.scrollWidth > e.clientWidth + 1).map((e) => e.textContent).join("; ") || "nenhum",
    efeitos: document.querySelectorAll("#batalha .carta .ef").length,
    inertes: ["heroi", "mundo"].map((id) => `${id}: ${[...document.getElementById(id).querySelectorAll(":scope > *")].filter((x) => x.inert).length || (document.getElementById(id).inert ? "inteira" : 0)}`).join(", ") };
});
const seletor = (p) => p.evaluate(() => {
  const j = document.querySelector(".roda-janela"); if (!j) return "fechado";
  const l = j.querySelector(".rj-lista"), m = l.getBoundingClientRect();
  const fs = [...l.querySelectorAll(".rj-linha")];
  const inteiras = fs.filter((e) => { const q = e.getBoundingClientRect(); return q.top >= m.top - 1 && q.bottom <= m.bottom + 1 && q.bottom <= innerHeight; }).length;
  const faixas = fs.map((e) => {
    const n = e.querySelector(".rj-nome"), i = e.querySelector(".rj-info"), lh = parseFloat(getComputedStyle(n).lineHeight);
    const nr = n.getBoundingClientRect(), ir = i.getBoundingClientRect();
    return { nome: n.textContent, linhas_do_nome: Math.round(nr.height / lh), custo: i.textContent.trim() ? (ir.top >= nr.bottom - 2 ? "embaixo" : "ao lado") : "—", custo_x: Math.round(ir.left), estoura: n.scrollWidth > n.clientWidth + 1 };
  });
  const d = j.querySelector(".rj-descricao"), c = j.querySelector(".rj-desc-caixa"), t = c && c.querySelector("b");
  return { lugar: j.classList.contains("lateral") ? "sobre a ficha" : "embaixo", faixas_inteiras: `${inteiras} de ${fs.length}`, lista_rola: l.scrollHeight > l.clientHeight + 1, lista: Math.round(m.height),
    nomes_em_3_linhas: faixas.filter((f) => f.linhas_do_nome >= 3).map((f) => f.nome), nomes_estouram: faixas.filter((f) => f.estoura).map((f) => f.nome),
    custos: [...new Set(faixas.filter((f) => f.custo !== "—").map((f) => f.custo))].join(", "), custos_alinhados: new Set(faixas.filter((f) => f.custo !== "—").map((f) => f.custo_x)).size <= 1,
    voltar: j.querySelector(".rj-titulo .rj-voltar") ? "no título" : "embaixo",
    descricao: d ? `${Math.round(d.getBoundingClientRect().height)} px${c.scrollHeight > c.clientHeight + 1 ? " (rola)" : ""}` : "—",
    examinada: t ? t.textContent : "nenhuma", ficha: document.getElementById("heroi").inert ? "inerte" : "livre" };
});
const porEfeitos = (p, m, vazio = false) => p.evaluate(([m, vazio]) => {
  const cb = JSON.parse(JSON.stringify(estado.combate));
  const vivosA = cb.aliados.filter((a) => a.vivo), vivosI = cb.inimigos.filter((e) => e.vivo);
  cb.heroi.efeitos = vazio ? [] : (m.heroi && m.heroi.efeitos) || [];
  vivosA.forEach((a, k) => { a.efeitos = vazio ? [] : (m.aliados[k] && m.aliados[k].efeitos) || []; });
  vivosI.forEach((e, k) => { e.efeitos = vazio ? [] : (m.inimigos[k] && m.inimigos[k].efeitos) || []; });
  Batalha.desenhar(cb, estado.heroi);
}, [m, vazio]);
const foto = (p, nome) => p.screenshot({ path: path.join(SAIDA, `${nome}.png`) });
async function mira(p, H) {
  await (await slot(p, "habilidades")).click(); await espera(500);
  const hab = await p.evaluate((um) => (document.querySelector(um.map((h) => `.roda-janela .rj-linha:not(.bloqueada)[data-hab="${h}"]`).join(", ")) || {}).dataset?.hab || null, UM_ALVO);
  if (hab) await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click();
  await espera(900); await p.mouse.move(5, H - 5); await espera(250);
  return p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor na tela; ficha ${document.getElementById("heroi").inert ? "INERTE" : "livre"}; ${document.querySelector(".roda-mira") ? "a mira à vista" : "SEM MIRA"}; alvos acesos ${document.querySelectorAll("#batalha .carta.alvejavel").length}`);
}
async function voltarDaMira(p) {
  const v = await p.$(".mira-voltar"); if (v) await v.click(); else await p.keyboard.press("Escape");
  await vez(p); await espera(400);
}

// 1. os casos, como na rodada 2
for (const [luta, tam] of [["arqueiro", [1280, 720]], ["maior", [1280, 720]], ["maior", [1500, 950]]]) {
  const nome = `${tam[0] === 1280 ? "baixa" : "normal"}-${luta}-jogo`, H = tam[1], r = { nome }, real = REAIS[LUTAS[luta].real];
  const { proc, url } = await subir(LUTAS[luta].amb);
  try {
    const p = await pagina(url, tam, nome);
    await vez(p);
    if (tam[0] === 1280) {
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
      const alvo = await p.$("#batalha .carta.alvejavel"); if (alvo) await alvo.click();
      await espera(700); await vez(p); await p.mouse.move(5, H - 5); await espera(800);
      r.parado = await arena(p);
      await foto(p, `${nome}-1-tela`);
      const antes = await posicoes(p);
      await (await slot(p, "habilidades")).click(); await espera(600);
      const linhas = await p.$$(".roda-janela .rj-linha");
      let maior = { k: 0, h: 0 };
      for (let k = 0; k < linhas.length; k++) {
        await linhas[k].hover(); await espera(120);
        const h = await p.evaluate(() => { const c = document.querySelector(".rj-desc-caixa"); return c ? c.scrollHeight : 0; });
        if (h > maior.h) maior = { k, h };
      }
      await linhas[maior.k].hover(); await espera(300);
      r.habilidades = await seletor(p);
      r.abrir_mexe = antes === (await posicoes(p)) ? "nada se mexe" : "MUDOU";
      await foto(p, `${nome}-2-habilidades`);
      await p.mouse.move(5, H - 5);
      await (await slot(p, "itens")).click(); await espera(600); await p.mouse.move(5, H - 5); await espera(200);
      r.itens = await seletor(p);
      await foto(p, `${nome}-3-itens`);
      await (await slot(p, "itens")).click(); await espera(400);
      r.fechar_mexe = antes === (await posicoes(p)) ? "nada se mexe" : "MUDOU";
      r.mira = await mira(p, H);
      await foto(p, `${nome}-4-mira`);
      await voltarDaMira(p);
    }
    await porEfeitos(p, real.momento); await espera(700); await p.mouse.move(5, H - 5); await espera(300);
    r.com_efeitos = await arena(p);
    await foto(p, `${nome}-5-efeitos-reais`);
    await (await slot(p, "habilidades")).click(); await espera(600);
    const ls = await p.$$(".roda-janela .rj-linha"); if (ls.length) { await ls[Math.min(4, ls.length - 1)].hover(); await espera(300); }
    r.efeitos_habilidades = await seletor(p);
    await foto(p, `${nome}-6-efeitos-reais-habilidades`);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}

// 2. a passagem entre tamanhos, com a luta em andamento (o necromante e os efeitos reais)
{
  const r = { nome: "janelas-maior-jogo", passos: [] }, real = REAIS.necromante;
  const { proc, url } = await subir(LUTAS.maior.amb);
  try {
    const p = await pagina(url, [1500, 950], r.nome);
    await vez(p); await espera(600);
    await porEfeitos(p, real.momento); await espera(700);
    const tamanhos = [[1500, 950], [1280, 720], [1050, 720], [900, 720], [1280, 720], [1500, 950]];
    for (const [W, H] of tamanhos) {
      await p.setViewportSize({ width: W, height: H }); await espera(900); await p.mouse.move(5, H - 5);
      const passo = { tamanho: `${W}×${H}`, ...(await arena(p)) };
      // no mesmo tamanho: os efeitos saem e voltam; o registro não muda de lugar nem de tamanho
      const reg = () => p.evaluate(() => { const q = document.getElementById("pagina").getBoundingClientRect(); return `${document.body.dataset.registro || "embaixo"} ${Math.round(q.left)},${Math.round(q.top)} ${Math.round(q.width)}×${Math.round(q.height)}`; });
      const r0 = await reg();
      await porEfeitos(p, real.momento, true); await espera(600);
      const r1 = await reg();
      await porEfeitos(p, real.momento); await espera(600);
      const r2 = await reg();
      passo.efeitos_saem_e_voltam = r0 === r1 && r1 === r2 ? "o registro fica onde está" : `MUDOU: ${r0} → ${r1} → ${r2}`;
      await foto(p, `janelas-${W}x${H}-${r.passos.length + 1}-tela`);
      // o seletor e a mira neste tamanho
      await (await slot(p, "habilidades")).click(); await espera(600);
      const ls = await p.$$(".roda-janela .rj-linha"); if (ls.length) { await ls[1].hover(); await espera(300); }
      passo.habilidades = await seletor(p);
      passo.habilidades_cobre_registro = await p.evaluate(() => { const j = document.querySelector(".roda-janela"), pg = document.getElementById("pagina"); if (!j) return "—"; const a = j.getBoundingClientRect(), q = pg.getBoundingClientRect(); return a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1 ? "o seletor cobre o registro enquanto aberto" : "o registro continua à vista"; });
      await foto(p, `janelas-${W}x${H}-${r.passos.length + 1}-habilidades`);
      await p.keyboard.press("Escape"); await espera(300);
      passo.mira = await mira(p, H);
      await voltarDaMira(p);
      r.passos.push(passo);
    }
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}

// 3. o teclado e o movimento reduzido, em 1280×720 e em 1050×720 (o registro e o seletor na coluna da ficha)
for (const [W, H] of [[1280, 720], [1050, 720]]) {
  const r = { nome: `teclado-${W}x${H}-jogo` };
  const { proc, url } = await subir(LUTAS.maior.amb);
  try {
    const p = await pagina(url, [W, H], r.nome, { reducedMotion: "reduce" });
    await vez(p); await espera(500);
    await porEfeitos(p, REAIS.necromante.momento); await espera(500);
    r.registro_em = await p.evaluate(() => document.body.dataset.registro || "embaixo da arena");
    await p.keyboard.press("2"); await espera(500);
    r.tecla_2 = await p.evaluate(() => { const a = document.activeElement, j = document.querySelector(".roda-janela"); return `${j ? (j.classList.contains("lateral") ? "seletor sobre a ficha" : "seletor embaixo") : "sem seletor"}; foco: ${a.closest(".rj-linha") ? a.querySelector(".rj-nome").textContent : a.tagName}`; });
    r.animacao = await p.evaluate(() => getComputedStyle(document.querySelector(".roda-janela .rj-linha")).animationName);
    for (let k = 0; k < 4; k++) await p.keyboard.press("ArrowDown");
    await espera(200);
    r.setas = await p.evaluate(() => { const a = document.activeElement, q = a.getBoundingClientRect(), l = a.closest(".rj-lista")?.getBoundingClientRect(), t = document.querySelector(".rj-desc-caixa b");
      return `foco na ${[...document.querySelectorAll(".rj-linha")].indexOf(a) + 1}ª (${a.querySelector(".rj-nome")?.textContent}); ${l && q.top >= l.top - 1 && q.bottom <= l.bottom + 1 && q.bottom <= innerHeight ? "inteira à vista" : "FORA DA VISTA"}; ${a.matches(":focus-visible") ? "foco visível" : "sem foco visível"}; descrição: ${t ? t.textContent : "nenhuma"}`; });
    await foto(p, `teclado-${W}x${H}-setas`);
    r.ficha_coberta = await p.evaluate(() => { const f = document.getElementById("heroi"), q = f.getBoundingClientRect();
      const em = [[q.left + q.width / 2, q.top + 60], [q.left + q.width / 2, q.top + q.height / 2], [q.left + 30, q.bottom - 40]].map(([x, y]) => (document.elementFromPoint(x, y)?.closest(".roda-janela") ? "seletor" : "FICHA")).join(", ");
      return `pontos da ficha: ${em}; ficha ${f.inert ? "inerte" : "LIVRE"}`; });
    const tabs = [];
    for (let k = 0; k < 12; k++) { await p.keyboard.press("Tab"); tabs.push(await p.evaluate(() => (document.activeElement.closest("#heroi") ? "FICHA" : document.activeElement.closest(".roda-janela") ? "seletor" : document.activeElement.closest("#cena") ? "registro" : document.activeElement.closest("#mundo") ? "mundo" : document.activeElement.closest("#batalha, #roda") ? "arena" : document.activeElement.tagName.toLowerCase()))); }
    r.tab_12_vezes = tabs.join(" → ");
    await p.keyboard.press("2"); await espera(300);
    if (!(await p.$(".roda-janela"))) { await p.keyboard.press("2"); await espera(300); }
    await p.keyboard.press("Escape"); await espera(300);
    r.esc = await p.evaluate(() => `${document.querySelectorAll(".roda-janela").length} seletor; foco: ${document.activeElement.dataset.slot || document.activeElement.tagName}; ficha ${document.getElementById("heroi").inert ? "INERTE" : "livre"}`);
    relatorio.push(r); console.log(JSON.stringify(r));
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, "relatorio.json"), JSON.stringify({ relatorio, erros }, null, 1));
