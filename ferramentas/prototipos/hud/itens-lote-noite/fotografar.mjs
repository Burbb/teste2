// O lote de itens da noite (proposta, nada no jogo): fotografa cada desenho novo nos lugares onde ele fica parado,
// atual × proposta, nas janelas normal (1500×950) e baixa (1280×720), com o jogo intacto. A página recebe os arquivos
// da proposta no lugar dos do jogo (page.route em /static/hud/icones/<peça>-*.png, como fotografar_escudo.mjs); uma
// peça que ainda não tem papel em icones.js (a calça de couro) ganha o papel só nesta página.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs <peça>
// peça: calca_couro | aljava | atributos | ataque_defesa | agilidade_poder | agilidade | aljava_ref | poder | doca_r2 | doca_r3 | doca_r3_luta | doca_r4 | doca_r4_telas | doca_r5 | doca
import { spawn } from "child_process";
import { readFileSync, existsSync, mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const peca = process.argv[2];
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
// JANELAS=1920x945 (a janela principal do Jean) ou a lista padrão: a normal e a baixa
const JANELAS = process.env.JANELAS ? process.env.JANELAS.split(",").map((j) => j.split("x").map(Number)) : [[1500, 950], [1280, 720]];
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";

// cada peça: a pasta da proposta, os nomes de arquivo que ela troca, o papel novo (se houver) e as fotos
const PECAS = {
  calca_couro: { pasta: "calca_couro/proposta", nomes: ["calca_couro"], papel: { item: "calca_couro", tamanhos: [32, 40, 48, 64] },
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "calca_couro", VESTIDO: "calca_couro" }] },
  aljava: { pasta: "aljava/proposta", nomes: ["aljava"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo", "ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "aljava", VESTIDO: "aljava" }] },
  atributos: { pasta: "atributos/proposta", nomes: ["attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "luta"] },
  // Ataque e Defesa (a rodada nova, depois da proposta recusada de "atributos"): a ficha e o Inventário (24) e o selo da
  // festa de atributo permanente (64), pelo mesmo caminho do jogo (Telas.celebrar com a mensagem "atributo")
  ataque_defesa: { pasta: "ataque_defesa/proposta", nomes: ["attr-ataque", "attr-defesa"], papel_tamanhos: [24, 32, 64],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario", "selo"] },
  // Agilidade e Poder (a rodada nova): a ficha e o Inventário (24), os selos (64) e o comando Fugir da luta (32: a
  // Agilidade é também a ação de fugir, ACAO.fuga)
  agilidade_poder: { pasta: "agilidade_poder/proposta", nomes: ["attr-agilidade", "attr-poder"], papel_tamanhos: [24, 32, 64],
    selos: [["agi", "Agilidade"], ["poder", "Poder"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "inventario", "selo", "luta"] },
  // a rodada das referências (agilidade_aljava_ref/): a bota nova de Agilidade (ficha 24, Fugir 32, selo 64) e a aljava
  // nova (topo 24, ficha 32, Inventário 40 e o saque com o 48 ao lado do 64)
  agilidade: { pasta: "agilidade_aljava_ref/proposta", saida: "agilidade_aljava_ref/capturas", nomes: ["attr-agilidade"],
    papel_tamanhos: [24, 32, 64], selos: [["agi", "Agilidade"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "selo", "luta"] },
  aljava_ref: { pasta: "agilidade_aljava_ref/proposta", saida: "agilidade_aljava_ref/capturas", nomes: ["aljava"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo", "ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "aljava", VESTIDO: "aljava" }] },
  // o Poder em avaliação (35262ca, agilidade_poder/): só ele trocado, ao lado de Ataque, Defesa e Agilidade do jogo
  poder: { pasta: "agilidade_poder/proposta", saida: "agilidade_poder/capturas", nomes: ["attr-poder"], papel_tamanhos: [24, 32, 64], selos: [["poder", "Poder"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "selo"] },
  // a doca, rodada 2 (doca_r2/): dois atalhos por vez; agora o Inventário e o Mapa, também com a tela aberta
  doca_r2: { pasta: "doca_r2/proposta", saida: "doca_r2/capturas", nomes: ["atalho-inventario", "atalho-mapa"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "doca-inventario", "doca-mapa"] },
  // a doca, rodada 3 (doca_r3/): o Grimório e o Diário, também com a tela aberta; o Grimório é também o comando
  // Habilidades da roda da luta (ACAO.grimorio, 32), fotografado no tutorial
  doca_r3: { pasta: "doca_r3/proposta", saida: "doca_r3/capturas", nomes: ["atalho-grimorio", "atalho-diario"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "doca-grimorio", "doca-diario"] },
  doca_r3_luta: { pasta: "doca_r3/proposta", saida: "doca_r3/capturas", nomes: ["atalho-grimorio", "atalho-diario"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["luta"] },
  // a doca, rodada 4 (doca_r4/): a Comitiva (um papel novo, só nesta página) e os Talentos. No tutorial, com um
  // companheiro e pontos de talento (o selo ★ sobre os Talentos); na fogueira, com as telas abertas
  doca_r4: { pasta: "doca_r4/proposta", saida: "doca_r4/capturas", nomes: ["atalho-comitiva", "atalho-talentos"],
    papel_atalho: { rotulo: "Comitiva", peca: "atalho-comitiva", tamanhos: [32, 36] },
    cena: ["tutorial", { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", COMITIVA: "morel", PONTOS: "2" }], fotos: ["doca"] },
  doca_r4_telas: { pasta: "doca_r4/proposta", saida: "doca_r4/capturas", nomes: ["atalho-comitiva", "atalho-talentos"],
    papel_atalho: { rotulo: "Comitiva", peca: "atalho-comitiva", tamanhos: [32, 36] },
    cena: ["fogueira", { COMITIVA: "morel,odete" }], fotos: ["doca", "doca-comitiva", "doca-talentos"] },
  // a doca, rodada 5 (doca_r5/): o Bestiário, o Salvar e o Sair, na doca inteira (com companheiro e pontos de talento,
  // ao lado dos atalhos já aprovados); Salvar e Sair não são clicados (não mudam nada na foto)
  doca_r5: { pasta: "doca_r5/proposta", saida: "doca_r5/capturas", nomes: ["atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["tutorial", { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", COMITIVA: "morel", PONTOS: "2" }], fotos: ["doca"] },
  doca_r5_telas: { pasta: "doca_r5/proposta", saida: "doca_r5/capturas", nomes: ["atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["fogueira", { COMITIVA: "morel,odete" }], fotos: ["doca", "doca-bestiario"] },
  doca: { pasta: "doca/proposta", nomes: ["atalho-talentos", "atalho-grimorio", "atalho-inventario", "atalho-mapa", "atalho-diario", "atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "luta-doca"] },
};
const P = PECAS[peca];
if (!P) throw new Error(`peça desconhecida: ${peca}`);
// PASTA=<pasta relativa> troca a proposta (aljava/rodada4: a anterior); ROTULO=<nome> no lugar de "proposta" nas fotos
const PROPOSTA = path.join(aqui, process.env.PASTA || P.pasta), SAIDA = path.join(aqui, P.saida || path.join(peca, "capturas"));
const ROTULO = process.env.ROTULO || "proposta";
mkdirSync(SAIDA, { recursive: true });

async function anexar(p) {
  await p.route(/\/static\/hud\/icones\/([a-z_-]+)-(\d+)(@2x)?\.png/, async (r) => {
    const nome = decodeURIComponent(new URL(r.request().url()).pathname.split("/").pop());
    const base = nome.replace(/-\d+(@2x)?\.png$/, "");
    const arquivo = path.join(PROPOSTA, nome);
    if (P.nomes.includes(base) && existsSync(arquivo)) return r.fulfill({ body: readFileSync(arquivo), contentType: "image/png" });
    return r.continue();
  });
  if (P.papel_tamanhos) {   // os tamanhos novos de um desenho que já tem papel (o 64 do selo)
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      for (const n of P.nomes) { const i = js.indexOf(`"${n}": [`), j = js.indexOf("]", i); if (i >= 0) js = js.slice(0, i) + `"${n}": ${JSON.stringify(P.papel_tamanhos)}` + js.slice(j + 1); }
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel_atalho) {   // um atalho que ainda não tem desenho próprio no jogo (a Comitiva): o papel só nesta página
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      const { rotulo, peca: nome, tamanhos } = P.papel_atalho;
      js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${nome}": ${JSON.stringify(tamanhos)}, `);
      js = js.replace('const ATALHO = {', `const ATALHO = { "${rotulo}": "${nome}", `);
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel) {
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${P.papel.item}": ${JSON.stringify(P.papel.tamanhos)}, `);
      js = js.replace('const ITEM = {', `const ITEM = { ${P.papel.item}: "${P.papel.item}", `);
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
}
async function subir() {
  const [cenario, amb] = P.cena;
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

const b = await chromium.launch();
const rel = [];
// SO_ATUAL=1: só o jogo como está (sem trocar arquivo nenhum), para conferir uma integração
for (const modo of (process.env.SO_ATUAL ? ["atual"] : process.env.SO_PROPOSTA ? [ROTULO] : ["atual", ROTULO])) for (const [W, H] of JANELAS) {
  const { proc, url } = await subir();
  try {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo !== "atual") await anexar(p);
    await p.goto(url); await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1200);
    const nome = (f) => path.join(SAIDA, `${modo}-${W}x${H}-${f}.png`);
    const clipDe = async (sel, m = 8) => { const bb = await (await p.$(sel)).boundingBox(); return { x: Math.max(0, bb.x - m), y: Math.max(0, bb.y - m), width: bb.width + 2 * m, height: bb.height + 2 * m }; };
    // o que os desenhos da peça carregaram (o arquivo e o tamanho na tela)
    const desenhos = async () => p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
      .map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}px`), P.nomes);
    const visto = new Set();
    for (const f of P.fotos) {
      if (f === "ficha") { await p.screenshot({ path: nome("ficha"), clip: await clipDe("#heroi", 0) }); }
      if (f === "topo") { await p.screenshot({ path: nome("topo"), clip: await clipDe("#hud", 0) }); }
      if (f === "selo") {
        for (const [stat, nomeAttr] of (P.selos || [["atk", "Ataque"], ["defesa", "Defesa"]])) {
          await p.evaluate(([st, nm]) => { Telas.celebrar({ tipo: "atributo", dados: { stat: st, nome: nm, valor: 2, total: 27 } }, false); }, [stat, nomeAttr]);
          await espera(350);
          const sel = await p.$(".selo-atributo");
          if (sel) { const bb = await sel.boundingBox(); await p.screenshot({ path: nome(`selo-${stat}`), clip: { x: bb.x - 10, y: bb.y - 10, width: bb.width + 20, height: bb.height + 20 } }); }
          (await desenhos()).forEach((d) => visto.add(d));
          await espera(2600);
        }
      }
      if (f === "doca") { await p.screenshot({ path: nome("doca"), clip: await clipDe("#doca", 0) }); }
      // a doca com a tela do atalho aberta (o estado selecionado, .atual): "doca-inventario", "doca-mapa"
      if (f.startsWith("doca-")) {
        const rotulo = { inventario: "Inventário", mapa: "Mapa", grimorio: "Grimório", diario: "Diário", comitiva: "Comitiva", talentos: "Talentos", bestiario: "Bestiário" }[f.slice(5)];
        await p.evaluate((r) => pedirAtalho(r), rotulo); await espera(900);
        await p.screenshot({ path: nome(f), clip: await clipDe("#doca", 0) });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(500);
      }
      if (f === "inventario") {
        await p.evaluate(() => pedirAtalho("Inventário")); await espera(900);
        await p.screenshot({ path: nome("inventario"), clip: await clipDe("#palco", 0) });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(500);
      }
      if (f === "luta" || f === "luta-doca") {
        const comecar = await p.$('#prompt .escolha:has-text("Começar a luta")');
        if (comecar) {
          await comecar.click();
          await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 }); await espera(1200);
          await p.screenshot({ path: nome("luta"), clip: await clipDe("#palco", 0) });
          if (f === "luta") { await p.screenshot({ path: nome("luta-ficha"), clip: await clipDe("#heroi", 0) }); }
        }
      }
      (await desenhos()).forEach((d) => visto.add(d));
    }
    rel.push({ modo, janela: `${W}x${H}`, desenhos: [...visto].sort(), erros });
    await p.close();
  } finally { proc.kill(); }
}
// o cartão do saque (64 e 48: o achado e o "você usa") e o voo ao equipar, quando a peça tem cena de saque
if (P.saque) for (const modo of ["atual", "proposta"]) for (const [W, H] of JANELAS) {
  const [cenario, amb] = P.saque;
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo === "proposta") await anexar(p);
    await p.goto(url);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
    const bb = await (await p.$(".janela-achado")).boundingBox();
    await p.screenshot({ path: path.join(SAIDA, `${modo}-${W}x${H}-saque.png`), clip: { x: bb.x - 6, y: bb.y - 6, width: bb.width + 12, height: bb.height + 12 } });
    const desenhos = await p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
      .map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}px`), P.nomes);
    rel.push({ modo, janela: `${W}x${H}`, saque: [...new Set(desenhos)].sort(), erros });
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
for (const r of rel) console.log(JSON.stringify(r));
