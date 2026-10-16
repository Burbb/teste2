// Os ícones pequenos das escolhas de evento (experimento): a opção que gasta um consumível mostra hoje o sprite 16×16
// do jogo em 1× (escolhas.js: meta.gasta e meta.item). Fotografa o jogo de verdade com os mesmos dados em três versões:
//   atual  o jogo como está;
//   p16    a proposta com os desenhos de 16 px (escolhas-pixel/: a bomba desenhada na grade de 16, a poção e a bandagem
//          pela redução da família);
//   p24    a mesma proposta em 24 px (os de 24 do topo e a bomba de 24).
// A proposta, só nesta página: o icones.js ganha o papel Icones.escolha(id, lado), que devolve o desenho do
// consumível só quando existe o arquivo NATIVO daquele tamanho (nunca um 32 reduzido) e "" no resto (o sprite do jogo
// continua); o escolhas.js troca as duas linhas de meta.item e meta.gasta pela chamada. Os desenhos compartilhados
// (a caveira, o sprite da bandagem, a poção do topo) não mudam nos outros papéis.
// Os lugares (cenário covil, o evento tocado na hora):
//   odete_na_estrada com bandagens: "Estancar o sangue com uma bandagem" (meta.gasta: bandagem);
//   os_enfermos com uma poção e sem poção: "Deixar remédios na porta" (meta.gasta: pocao_vida, disponível e não);
//   a bomba, simulada: nenhum evento de hoje gasta a Bomba de Fumaça; a foto troca, na página, o id da opção da poção
//   pelo da bomba e redesenha o ícone pela mesma chamada (marcada "simulada" no nome do arquivo).
// Em janela normal (1500×950) e baixa (1280×720); mede a altura de cada opção (a proposta não pode mudar a altura).
// Guarda em capturas-escolhas/; comparar_escolhas.py monta as comparações.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_escolhas.mjs
// (VERSOES=atual,p24 escolhe as versões; SAIDA=<pasta> troca a pasta das fotos)
import { spawn } from "child_process";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-escolhas")), AMOSTRAS = path.join(aqui, "escolhas-pixel");
rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const trocar = (texto, trocas, arquivo) => trocas.reduce((t, [a, b]) => {
  if (!t.includes(a)) throw new Error(`${arquivo} mudou: não achei ${a}`);
  return t.replace(a, b);
}, texto);
// a proposta: o papel novo no Icones e a chamada no escolhas.js (o lado vem da versão)
const icones = (lados) => trocar(readFileSync(path.join(raiz, "rpg/web/static/icones.js"), "utf8"), [
  ['"bandagem": [24, 32, 48, 64]', `"bandagem": [${[...new Set([...lados, 24, 32, 48, 64])].sort((a, b) => a - b).join(", ")}]`],
  ['"bomba": [32]', `"bomba": [${[...new Set([...lados, 32])].sort((a, b) => a - b).join(", ")}]`],
  ['"pocao": [24, 32, 48, 64]', `"pocao": [${[...new Set([...lados, 24, 32, 48, 64])].sort((a, b) => a - b).join(", ")}]`],
  ["    /** Um consumível da bolsa, pelo id do motor (pocao_vida, bau...). */",
    `    /** O consumível que uma escolha de evento usa ou gasta, pelo id, no lado pequeno da opção: só com o arquivo nativo
     *  daquele lado (um desenho de 32 reduzido no navegador perde o desenho); sem ele, "" e a opção fica com o sprite. */
    escolha: (id, lado = ${lados[0]}) => (CONSUMIVEL[id] && TAMANHOS[CONSUMIVEL[id]] && TAMANHOS[CONSUMIVEL[id]].includes(lado) ? img(CONSUMIVEL[id], lado, "na-escolha") : ""),
    /** Um consumível da bolsa, pelo id do motor (pocao_vida, bau...). */`],
], "icones.js");
const escolhas = trocar(readFileSync(path.join(raiz, "rpg/web/static/app/escolhas.js"), "utf8"), [
  ["    if (o.meta && o.meta.item) icone = spr(Telas.iconeConsumivel(o.meta.item), 1);\n    if (o.meta && o.meta.gasta) icone = spr(Telas.iconeConsumivel(o.meta.gasta), 1);  // o item que a escolha usa",
    "    const doItem = (id) => Icones.escolha(id) || spr(Telas.iconeConsumivel(id), 1);  // o desenho do item, ou o sprite\n    if (o.meta && o.meta.item) icone = doItem(o.meta.item);\n    if (o.meta && o.meta.gasta) icone = doItem(o.meta.gasta);  // o item que a escolha usa"],
], "escolhas.js");
const VERSOES = Object.fromEntries(Object.entries({ atual: null, p16: [16], p24: [24] })
  .filter(([v]) => !process.env.VERSOES || process.env.VERSOES.split(",").includes(v)));
async function subir(cenario, amb = {}) {
  const proc = spawn("python3", ["-m", "tests.navegador.cenarios", cenario],
    { cwd: raiz, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} não subiu`);
  return { proc, url };
}
const JANELAS = { normal: [1500, 950], baixa: [1280, 720] };
const erros = [], medidas = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, jan, versao) {
  const [W, H] = JANELAS[jan];
  const p = await b.newPage({ viewport: { width: W, height: H } });
  if (VERSOES[versao]) {
    await p.route(/\/static\/icones\.js(\?|$)/, (r) => r.fulfill({ body: icones(VERSOES[versao]), contentType: "application/javascript" }));
    await p.route(/\/static\/app\/escolhas\.js(\?|$)/, (r) => r.fulfill({ body: escolhas, contentType: "application/javascript" }));
    await p.route(/\/static\/hud\/icones\/(bomba|pocao|bandagem)-(16|24)(@2x)?\.png/, (r) => r.fulfill({
      path: path.join(AMOSTRAS, path.basename(new URL(r.request().url()).pathname)), contentType: "image/png" }));
  }
  p.on("pageerror", (e) => erros.push(`${jan} ${versao}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error" && !/favicon/.test(m.location().url || "")) erros.push(`${jan} ${versao}: ${m.text()}`); });
  await p.goto(url);
  return p;
}
// espera a opção com o texto aparecer (passando os "continuar" do evento)
async function opcao(p, texto) {
  for (let k = 0; k < 80; k++) {
    const e = await p.evaluateHandle((t) => [...document.querySelectorAll("#prompt .escolha")].find((x) => x.textContent.includes(t)) || null, texto).then((h) => h.asElement());
    if (e) return e;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const c = await p.$(s); if (c) await c.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error(`a opção "${texto}" não apareceu`);
}
async function fotos(p, el, nome) {
  await p.mouse.move(3, 3); await espera(500);
  await el.scrollIntoViewIfNeeded(); await espera(200);
  const lista = await p.evaluateHandle((e) => e.closest(".escolhas") || e, el);
  await lista.screenshot({ path: path.join(SAIDA, `${nome}-opcoes.png`) });
  await el.screenshot({ path: path.join(SAIDA, `zoom-${nome}.png`) });
  medidas.push({ nome, ...(await p.evaluate((e) => {
    const i = e.querySelector("img"), alturas = [...e.closest(".escolhas").querySelectorAll(".escolha")].map((x) => Math.round(x.getBoundingClientRect().height));
    return { opcao: Math.round(e.getBoundingClientRect().height), outras: alturas.join(","), icone: i ? `${(i.getAttribute("src") || "").replace(/^data:.*/, "sprite").replace(/.*\/icones\//, "")} ${Math.round(i.getBoundingClientRect().width)}px` : "nenhum" };
  }, el)) });
}
const CASOS = [
  ["bandagem", { EVENTO: "odete_na_estrada", BOLSA: "bandagem=2" }, "uma bandagem"],
  ["pocao", { EVENTO: "os_enfermos", BOLSA: "pocao_vida=1" }, "Deixar remédios"],
  ["pocao-sem", { EVENTO: "os_enfermos", BOLSA: "pocao_vida=0" }, "Deixar remédios"],
];
for (const [caso, amb, texto] of CASOS) for (const jan of Object.keys(JANELAS)) for (const versao of Object.keys(VERSOES)) {
  const { proc, url } = await subir("covil", { LUGAR: "vila", ...amb });
  try {
    const p = await pagina(url, jan, versao), nome = `${jan}-${versao}-${caso}`;
    const el = await opcao(p, texto);
    await p.mouse.move(3, 3); await espera(500);
    if (caso === "bandagem") await p.screenshot({ path: path.join(SAIDA, `${nome}-tela.png`) });
    await fotos(p, el, nome);
    if (caso === "pocao") {  // a bomba, simulada: o mesmo caminho do ícone, com o id da bomba
      await p.evaluate((e) => {
        const i = e.querySelector("img"), novo = (typeof Icones.escolha === "function" && Icones.escolha("bomba_fumaca")) || Sprites.img(Telas.iconeConsumivel("bomba_fumaca"), 1);
        const t = document.createElement("template"); t.innerHTML = novo.trim(); i.replaceWith(t.content.firstChild);
        e.querySelector(".op-texto").textContent = "Jogar a bomba de fumaça e sumir (simulada)";
        const n = e.querySelector(".op-nota"); if (n) n.textContent = "Usa 1 bomba de fumaça da bolsa (você tem 1).";
      }, el);
      await fotos(p, el, `${jan}-${versao}-bomba-simulada`);
    }
    await p.close();
  } finally { proc.kill(); }
  console.log(caso, jan, versao, "ok");
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
for (const m of medidas) console.log(JSON.stringify(m));
console.log(erros.length ? erros.join("\n") : "sem erros");
