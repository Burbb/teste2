// A HUD aprovada integrada ao jogo (1.111.0) e as lutas cheias: o jogo de antes (o commit ANTES, padrão 5795a9a, a
// 1.110.0 com o protótipo só na pasta dele) e o de agora, com os mesmos dados (um jogo novo com a mesma semente por
// foto). O "antes" roda de uma cópia de trabalho separada do commit (git worktree, criada aqui se faltar), com o
// cenarios.py de agora (as opções novas das lutas cheias; o resto do jogo é o daquele commit).
//
// As lutas (cenário tutorial, depois de uma rodada de Atacar):
//   poucos   Guerreiro paladino com Morel, um rato e 2 lobos, de manhã no Vau: a composição de sempre; a rodada
//            derruba o rato (o alvo derrotado fica, apagado, e ninguém sai do lugar);
//   noite    Mago necromante com Morel e Odette, 3 lobos, à noite no Charco: o aviso da noite; Erguer Servo (uma
//            invocação real entrando no meio da luta);
//   cinco    Arqueiro patrulheiro com o lobo, Morel e Odette (4 aliados), 5 lobos, à tarde no Bosque;
//   maior    Mago necromante com Morel, Odette e 3 servos invocados (6 aliados: o máximo real, com a Legião de Ossos e o
//            Rei dos Mortos), contra 5 caídos e o xamã (6 inimigos: o maior bando real, caídos à noite com a comitiva e
//            a escolta), à noite no Charco;
//   longos   Guerreiro berserker com Morel e Odette, 4 esqueletos com os nomes mais longos do jogo (um único de 49
//            letras e os reforços com a letra e "(invocado)"), de manhã no Vau.
// Em 1280×720, 1500×950 e 1920×1080: a tela inteira; a roda parada, o mouse, o pressionado, o foco do teclado; abrir
// Habilidades, alternar para Itens e fechar (as cartas e as rolagens não podem mexer); a mira e o Voltar (o lembrete não
// cobre carta); o golpe no meio (o número e o efeito que passam da moldura). Mede o que cobre o quê entre as áreas
// (aliados, comandos, inimigos, mira, aviso), as cartas fora da arena, os nomes cortados e a altura que sobra para o
// registro. Só no depois (o antes não tem as vagas): a saída de um inimigo durante a mira e a entrada de outro, as duas
// SIMULADAS na tela (o estado da luta com um inimigo a menos ou a mais, desenhado pelo jogo; no motor, quem sai é o
// ladrão que foge com o ouro e quem entra é o reforço invocado), com as posições das outras cartas antes e depois.
// Comportamentos (poucos, 1500×950, nas duas versões): cinco cliques depressa, a tecla segurada, Habilidades ↔ Itens
// depressa, o movimento reduzido.
// A exploração (as escolhas de um lugar selvagem; o antes não tem as faixas): o Bosque, o Charco com contrato, a
// Capela à noite com e sem tocha (a ação real "Entrar na capela pelo buraco do canal", com os riscos embaixo), o covil
// e o teste de esforço (TEXTO SIMULADO: a primeira opção do covil alongada só na foto), em 1500×950, 1280×720,
// 1920×1080 e 1280×720 a 125%; e a escolha da ação real da Capela (o fluxo segue como no jogo); a vila não ganha faixas.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/fotografar_lutas_cheias.mjs
// (VERSOES=antes,depois, LUTAS=..., EXPLORA=..., JANELAS=baixa,normal,grande, JANELAS_EXPLORA=..., SAIDA=<pasta>,
// ANTES=<commit>, ANTES_RAIZ=<pasta de um checkout do antes>, PYTHON=<executável>, MANTER=1)
import { execFileSync, spawn } from "child_process";
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync, writeFileSync } from "fs";
import { tmpdir } from "os";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../..");
const SAIDA = path.resolve(process.env.SAIDA || path.join(aqui, "capturas-lutas-cheias"));
mkdirSync(SAIDA, { recursive: true });
// sem MANTER, saem só as fotos soltas e o relatório (o .gitignore e comparacoes/, versionados, ficam)
if (!process.env.MANTER) for (const f of readdirSync(SAIDA)) if (/\.(png|json)$/.test(f)) rmSync(path.join(SAIDA, f));
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const filtro = (nome, todos) => (process.env[nome] ? process.env[nome].split(",") : todos);
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");

// o antes: uma cópia de trabalho do commit, com o cenarios.py de agora
const ANTES = process.env.ANTES || "5795a9a";
const RAIZ_ANTES = process.env.ANTES_RAIZ || path.join(tmpdir(), `unquiet-antes-${ANTES}`);
if (!existsSync(path.join(RAIZ_ANTES, "rpg"))) execFileSync("git", ["worktree", "add", "--detach", RAIZ_ANTES, ANTES], { cwd: raiz, stdio: "inherit" });
copyFileSync(path.join(raiz, "tests/navegador/cenarios.py"), path.join(RAIZ_ANTES, "tests/navegador/cenarios.py"));
const RAIZES = { antes: RAIZ_ANTES, depois: raiz };
const VERSOES = filtro("VERSOES", ["antes", "depois"]);
const JANELAS = Object.entries({ baixa: [1280, 720], normal: [1500, 950], grande: [1920, 1080], escala: [1024, 576] });
const JANELAS_LUTA = JANELAS.filter(([j]) => filtro("JANELAS", ["baixa", "normal", "grande"]).includes(j));
const JANELAS_EXPLORA = JANELAS.filter(([j]) => filtro("JANELAS_EXPLORA", ["baixa", "normal", "grande", "escala"]).includes(j));
const ESCALA = { escala: { deviceScaleFactor: 1.25 } };
const VISTAS = "A1,V2,N1,D1,K1,M1,L1";
const BASE = { TUTORIAL: "0", VISTAS, NIVEL: "12", NIVEL_LUTA: "9", REC: "0.6" };
const TODAS_LUTAS = {
  poucos: { ...BASE, CLASSE: "guerreiro", ESPEC: "paladino", COMITIVA: "morel", GRUPO: "rato:1,lobo:2", NIVEL_LUTA: "4", LUGAR: "vau", PERIODO: "0" },
  noite: { ...BASE, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", LUTA: "lobo", QUANTOS: "3", LUGAR: "charco", PERIODO: "3", REC: "1" },
  cinco: { ...BASE, CLASSE: "arqueiro", ESPEC: "patrulheiro", ANIMAL: "lobo", COMITIVA: "morel,odete", LUTA: "lobo", QUANTOS: "5", LUGAR: "bosque", PERIODO: "2" },
  maior: { ...BASE, CLASSE: "mago", ESPEC: "necromante", COMITIVA: "morel,odete", SERVOS: "3", GRUPO: "caido:5,xama_caido:1", LUGAR: "charco", PERIODO: "3" },
  longos: { ...BASE, CLASSE: "guerreiro", ESPEC: "berserker", COMITIVA: "morel,odete", LUTA: "esqueleto", QUANTOS: "4", LONGOS: "1", LUGAR: "vau", PERIODO: "0" },
};
const LUTAS = Object.entries(TODAS_LUTAS).filter(([l]) => filtro("LUTAS", Object.keys(TODAS_LUTAS)).includes(l));
const TODAS_EXPLORA = {
  bosque: ["tutorial", { TUTORIAL: "0", VISTAS, COMITIVA: "morel", LUGAR: "bosque", PERIODO: "0" }],
  charco: ["tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "charco", PERIODO: "3", CONTRATO: "aceito", CONTRATO_EM: "charco" }],
  capela: ["capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "2" }],
  escura: ["capela", { ETAPA: "capela", PERIODO: "3", TOCHAS: "0" }],
  covil: ["covil", { PERIODO: "1" }],
  esforco: ["covil", { PERIODO: "1" }, "Enfrentar Sarric, o Profeta das Cinzas (guardião), que guarda o covil desde a queda da cidadela e não aceita rendição"],
};
const EXPLORA = Object.entries(TODAS_EXPLORA).filter(([l]) => filtro("EXPLORA", Object.keys(TODAS_EXPLORA)).includes(l));

async function subir(versao, cenario, amb) {
  const cwd = RAIZES[versao];
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario],
    { cwd, env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: cwd, PYTHONIOENCODING: "utf-8", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  proc.stderr.on("data", (d) => process.stderr.write(`[${versao} ${cenario}] ${d}`));
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error(`o cenário ${cenario} (${versao}) não subiu`);
  return { proc, url };
}
const relatorio = [], comportamentos = [], erros = [];
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
async function pagina(url, [W, H], nome, opcoes = {}) {
  const p = await b.newPage({ viewport: { width: W, height: H }, ...opcoes });
  // cada erro vai para a lista e também para a saída na hora (uma execução que pare no meio não os perde)
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
const noMenu = (p) => p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando && pergunta.tipo === "opcoes" && !!document.querySelector("#prompt .escolha"));
async function menu(p) {
  for (let k = 0; k < 120; k++) {
    if (await noMenu(p)) return;
    for (const s of [".orientacao:not([hidden]) .orientacao-entendi", "#prompt .continuar"]) { const e = await p.$(s); if (e) await e.click().catch(() => {}); }
    await espera(250);
  }
  throw new Error("o menu do lugar não chegou");
}
async function recortar(p, sels, nome, folga = 10) {
  const c = await p.evaluate(([ss, f]) => {
    const rs = ss.flatMap((s) => [...document.querySelectorAll(s)]).filter((e) => e.getClientRects().length && getComputedStyle(e).visibility !== "hidden")
      .map((e) => e.getBoundingClientRect()).filter((r) => r.width);
    if (!rs.length) return null;
    const x0 = Math.max(0, Math.min(...rs.map((r) => r.left)) - f), y0 = Math.max(0, Math.min(...rs.map((r) => r.top)) - f);
    return { x: Math.floor(x0), y: Math.floor(y0), width: Math.ceil(Math.min(innerWidth, Math.max(...rs.map((r) => r.right)) + f) - x0),
      height: Math.ceil(Math.min(innerHeight, Math.max(...rs.map((r) => r.bottom)) + f) - y0) };
  }, [[].concat(sels), folga]);
  if (c) await p.screenshot({ path: path.join(SAIDA, `${nome}.png`), clip: c });
}
const disposicao = (p) => p.evaluate(() => JSON.stringify({
  cartas: [...document.querySelectorAll("#batalha .carta")].map((c) => { const r = c.getBoundingClientRect(); return [c.dataset.uid, Math.round(r.left), Math.round(r.top)]; }),
  rolagem: [document.scrollingElement, ...document.querySelectorAll("*")].filter((e) => e && e.scrollTop > 0).map((e) => `${e.id || e.className}:${Math.round(e.scrollTop)}`),
}));
function diferenca(a, b) {
  if (a === b) return "nada se mexe";
  const A = JSON.parse(a), B = JSON.parse(b), d = [];
  const pb = Object.fromEntries(B.cartas.map(([u, x, y]) => [u, [x, y]]));
  A.cartas.forEach(([u, x, y]) => { if (!pb[u]) d.push(`${u} saiu`); else if (pb[u][0] !== x || pb[u][1] !== y) d.push(`${u}: ${x},${y} → ${pb[u]}`); });
  if (JSON.stringify(A.rolagem) !== JSON.stringify(B.rolagem)) d.push(`rolagem: ${A.rolagem} → ${B.rolagem}`);
  return d.length ? "MUDOU: " + d.join("; ") : "nada se mexe (só entrou carta)";
}
// as áreas: o que cobre o quê (comandos, mira e aviso contra as cartas; as cartas entre si), o que sai da arena, os
// nomes cortados (com reticências: a ficha mostra o nome inteiro) e a altura que sobra para o registro
const medir = (p) => p.evaluate(() => {
  const arena = document.getElementById("arena").getBoundingClientRect();
  const nome = (e) => (e.dataset.uid || "") + ":" + (e.querySelector(".carta-nome span")?.textContent.trim() || "");
  const cartas = [...document.querySelectorAll("#batalha .carta")].map((c) => [nome(c), c.getBoundingClientRect(), c]);
  const outros = [...[...document.querySelectorAll("#roda .roda-botao")].map((b) => ["cmd:" + b.dataset.slot, b.getBoundingClientRect()]),
    ...[...document.querySelectorAll(".roda-mira")].map((m) => ["mira", m.getBoundingClientRect()]),
    ...[...document.querySelectorAll("#arena > .mods-arena .mod")].map((m) => ["aviso", m.getBoundingClientRect()])];
  const toca = (a, q) => a.right > q.left + 1 && a.left < q.right - 1 && a.bottom > q.top + 1 && a.top < q.bottom - 1;
  const cobre = [];
  for (const [n, r] of outros) for (const [m, q] of cartas) if (toca(r, q)) cobre.push(`${n}×${m}`);
  for (let i = 0; i < cartas.length; i++) for (let k = i + 1; k < cartas.length; k++) if (toca(cartas[i][1], cartas[k][1])) cobre.push(`${cartas[i][0]}×${cartas[k][0]}`);
  const folgas = [];
  for (const [n, r] of outros.filter(([n]) => n.startsWith("cmd") || n === "mira")) for (const [, q, c] of cartas) if (c.classList.contains("inimigo") && r.bottom > q.top && r.top < q.bottom) folgas.push(Math.round(q.left - r.right));
  return { arena: `${Math.round(arena.width)}×${Math.round(arena.height)}`, registro_px: Math.round(document.getElementById("pagina").getBoundingClientRect().height),
    cartas_n: `${cartas.filter(([, , c]) => c.classList.contains("aliado")).length} aliados, ${cartas.filter(([, , c]) => c.classList.contains("inimigo")).length} inimigos`,
    cobre: cobre.join(", ") || "nada",
    folga_inimigos: folgas.length ? Math.min(...folgas) + " px" : "nenhum na mesma altura",
    fora_da_arena: cartas.filter(([, q]) => q.right > arena.right + 0.5 || q.left < arena.left - 0.5 || q.bottom > arena.bottom + 0.5 || q.top < arena.top - 0.5).map(([n]) => n).join(", ") || "nenhuma",
    nomes_cortados: cartas.map(([, , c]) => c.querySelector(".carta-nome span")).filter((e) => e && e.scrollWidth > e.clientWidth + 1).length };
});
const slot = (p, s) => p.$(`#roda .roda-botao[data-slot="${s}"]`);
const recArena = ["#arena"];
const UM_ALVO = ["bola_fogo", "drenar_vida", "execucao", "flecha_envenenada", "golpe_pesado", "golpe_sagrado", "investida", "lanca_gelo", "marcar_presa", "tiro_certeiro", "comando_fera", "furia_cega", "sede_sangue"];
const primeiraUmAlvo = (p) => p.evaluate((um) => (document.querySelector(um.map((h) => `.roda-janela .rj-linha:not(.bloqueada)[data-hab="${h}"]`).join(", ")) || {}).dataset?.hab || null, UM_ALVO);

for (const [luta, amb] of LUTAS) {
  for (const [jan, tam] of JANELAS_LUTA) for (const versao of VERSOES) {
    const H = tam[1], n = (c) => `${jan}-${luta}-${versao}-${c}`, r = { nome: `${jan}-${luta}-${versao}` };
    const { proc, url } = await subir(versao, "tutorial", amb);
    try {
      const p = await pagina(url, tam, r.nome);
      await vez(p);
      // uma rodada de Atacar no primeiro inimigo, com o golpe fotografado no meio
      const antesDaRodada = await disposicao(p);
      await (await slot(p, "atacar")).click();
      for (let k = 0; k < 40 && !(await p.$("#batalha .carta.alvejavel")); k++) await espera(100);
      const alvo = await p.$("#batalha .carta.alvejavel");
      if (alvo) await alvo.click();
      await espera(260);
      await recortar(p, recArena, n("0-golpe"), 40);
      await espera(500);
      await vez(p);
      await p.mouse.move(5, H - 5); await espera(800);
      r.caidos = await p.$$eval("#batalha .carta.inimigo.morta", (x) => x.length);
      r.rodada_mexe = diferenca(antesDaRodada, await disposicao(p));
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, recArena, n("1-normal"), 2);
      Object.assign(r, await medir(p));
      const atk = await slot(p, "atacar");
      await atk.hover(); await espera(400);
      await recortar(p, recArena, n("2-mouse"), 2);
      await p.mouse.down(); await espera(120);
      await recortar(p, recArena, n("3-pressionado"), 2);
      await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(250);
      r.soltar_fora = (await naVez(p)) && !(await p.$(".roda-mira")) ? "nada escolhido" : "ERRO";
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      for (let k = 0; k < 40 && !(await p.evaluate(() => document.activeElement?.dataset?.slot === "atacar")); k++) await p.keyboard.press("Tab");
      r.tab_chega = await p.evaluate(() => document.activeElement?.dataset?.slot === "atacar" && document.activeElement.matches(":focus-visible") ? "Atacar, foco visível" : "ERRO");
      await recortar(p, recArena, n("4-foco"), 2);
      const ref = await disposicao(p);
      await p.mouse.move(5, H - 5);
      await (await slot(p, "habilidades")).click(); await espera(450);
      await p.mouse.move(5, H - 5); await espera(200);
      r.abrir_mexe = diferenca(ref, await disposicao(p));
      await p.screenshot({ path: path.join(SAIDA, `${n("tela-aberto")}.png`) });
      await (await slot(p, "itens")).click(); await espera(450);
      await p.mouse.move(5, H - 5); await espera(200);
      r.alternar = `${await p.$eval(".roda-janela", (j) => j.dataset.tipo).catch(() => "nenhum")} aberto, ${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es)`;
      r.alternar_mexe = diferenca(ref, await disposicao(p));
      await recortar(p, [...recArena, ".roda-janela"], n("5-itens"), 2);
      await (await slot(p, "itens")).click(); await espera(300);
      r.fechar_mexe = diferenca(ref, await disposicao(p));
      // a mira (uma habilidade de um alvo, ou o Atacar), o lembrete e o Voltar
      await (await slot(p, "habilidades")).click(); await espera(450);
      const hab = await primeiraUmAlvo(p);
      if (hab) await (await p.$(`.roda-janela .rj-linha[data-hab="${hab}"]`)).click();
      else { await p.keyboard.press("Escape"); await espera(250); await (await slot(p, "atacar")).click(); }
      await espera(900);
      await p.mouse.move(5, H - 5); await espera(250);
      const mira = await medir(p);
      r.mira = `${hab || "atacar"}: ${mira.cobre}`;
      await recortar(p, recArena, n("6-mira"), 2);
      // passar o mouse por um alvo (a seta e o contorno)
      const alvos = await p.$$("#batalha .carta.alvejavel");
      if (alvos.length) { await alvos[alvos.length - 1].hover(); await espera(350); await recortar(p, recArena, n("7-mira-mouse"), 2); }
      // a saída e a entrada SIMULADAS (só no depois: o antes não tem vagas)
      if (versao === "depois") {
        const sim = await p.evaluate(() => {
          const pos = () => Object.fromEntries([...document.querySelectorAll("#batalha .carta")].map((c) => { const q = c.getBoundingClientRect(); return [c.dataset.uid, [Math.round(q.left), Math.round(q.top)]]; }));
          const cb = JSON.parse(JSON.stringify(estado.combate));
          const vivos = cb.inimigos.filter((e) => e.vivo);
          if (vivos.length < 2) return "menos de dois vivos";
          const sai = vivos[0].uid;
          const p0 = pos();
          Batalha.desenhar({ ...cb, inimigos: cb.inimigos.filter((e) => e.uid !== sai) }, estado.heroi);
          const p1 = pos();
          const mexeu = Object.keys(p1).filter((u) => p0[u] && (p0[u][0] !== p1[u][0] || p0[u][1] !== p1[u][1]));
          window.__simulado = { cb, sai };
          return `sai ${sai}; vaga: ${document.querySelectorAll("#batalha .vaga-carta").length}; outras cartas que mexeram: ${mexeu.join(", ") || "nenhuma"}`;
        });
        r.saida_simulada = sim;
        await espera(300);
        await recortar(p, recArena, n("8-saida-simulada"), 2);
      }
      const v = await p.$(".mira-voltar");
      if (v) await v.click(); else await p.keyboard.press("Escape");
      await vez(p); await espera(400);
      r.voltar = (await slot(p, "habilidades")) && !(await p.$(".roda-janela")) ? "a roda de volta" : "ERRO";
      await recortar(p, recArena, n("9-volta"), 2);
      if (versao === "depois") {
        // a vaga fecha no próximo lance (aqui, um lance vazio); depois, um reforço SIMULADO entra no fim
        r.vaga_fecha = await p.evaluate(async () => {
          await Batalha.lance({ tipo: "nada" });
          await new Promise((res) => setTimeout(res, 500));
          return `vagas depois do lance: ${document.querySelectorAll("#batalha .vaga-carta").length}`;
        });
        r.entrada_simulada = await p.evaluate(() => {
          const pos = () => Object.fromEntries([...document.querySelectorAll("#batalha .carta")].map((c) => { const q = c.getBoundingClientRect(); return [c.dataset.uid, [Math.round(q.left), Math.round(q.top)]]; }));
          const { cb, sai } = window.__simulado;
          const base = cb.inimigos.filter((e) => e.uid !== sai);
          const novo = { ...base.find((e) => e.vivo), uid: "reforco-simulado", nome: "Lobo A (invocado)", invocado: true };
          const p0 = pos();
          Batalha.desenhar({ ...cb, inimigos: [...base, novo] }, estado.heroi);
          const p1 = pos();
          const mexeu = Object.keys(p0).filter((u) => p1[u] && (p0[u][0] !== p1[u][0] || p0[u][1] !== p1[u][1]));
          return `entrou no fim da coluna (${[...document.querySelectorAll("#batalha .inimigos > .carta")].pop()?.dataset.uid}); as outras que mexeram: ${mexeu.join(", ") || "nenhuma"}`;
        });
        await espera(500);
        await recortar(p, recArena, n("9b-entrada-simulada"), 2);
      }
      // a invocação real: Erguer Servo (necromante), quando a luta tem
      if (luta === "noite" && versao === "depois") {
        await vez(p);
        const ref2 = await disposicao(p);
        await (await slot(p, "habilidades")).click(); await espera(450);
        const erguer = await p.$('.roda-janela .rj-linha:not(.bloqueada)[data-hab="erguer_servo"]');
        if (erguer) {
          await erguer.click(); await espera(400);
          await vez(p); await p.mouse.move(5, H - 5); await espera(600);
          r.invocacao_real = `Erguer Servo: ${diferenca(ref2, await disposicao(p))}; ${JSON.stringify((await medir(p)).cobre)}`;
          await recortar(p, recArena, n("10-invocacao"), 2);
        } else r.invocacao_real = "Erguer Servo indisponível";
      }
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
    } finally { proc.kill(); }
  }
  // os comportamentos: a luta de poucos, 1500×950
  if (luta === "poucos") for (const versao of VERSOES) {
    const c = { versao }, tam = [1500, 950];
    const { proc, url } = await subir(versao, "tutorial", amb);
    try {
      let p = await pagina(url, tam, `comportamentos-${versao}`);
      await vez(p); await espera(500);
      const hb = await slot(p, "habilidades");
      for (let k = 0; k < 5; k++) { await hb.click(); await espera(40); }
      await espera(300);
      c.depressa = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) depois de 5 cliques (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      await p.keyboard.down("2"); for (let k = 0; k < 6; k++) { await espera(35); await p.keyboard.down("2"); } await p.keyboard.up("2"); await espera(300);
      c.tecla_segurada = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es) (esperado 1)`;
      await p.keyboard.press("Escape"); await espera(300);
      for (const s of ["habilidades", "itens", "habilidades", "itens"]) { await (await slot(p, s)).click(); await espera(30); }
      await espera(300);
      c.alternar_depressa = `${await p.$$eval(".roda-janela", (x) => x.length)} seletor(es), ${await p.$eval(".roda-janela", (j) => j.dataset.tipo).catch(() => "nenhum")} (esperado 1, itens)`;
      await p.close();
      p = await pagina(url, tam, `reduzido-${versao}`, { reducedMotion: "reduce" });
      await vez(p);
      await recortar(p, recArena, `comportamento-${versao}-reduzido-entrada`, 2);
      const atk = await slot(p, "atacar");
      await atk.hover(); await p.mouse.down(); await espera(100);
      c.reduzido_pressionado = await p.evaluate(() => getComputedStyle(document.querySelector('#roda .roda-botao[data-slot="atacar"]')).translate);
      c.reduzido_animacao = await p.evaluate(() => getComputedStyle(document.querySelector('#roda .roda-botao[data-slot="atacar"]')).animationName);
      await p.mouse.move(5, 940); await p.mouse.up();
      await p.close();
      comportamentos.push(c);
      console.log(JSON.stringify(c));
    } finally { proc.kill(); }
  }
}

for (const [lugar, [cenario, amb, alongar]] of EXPLORA) {
  for (const [jan, tam] of JANELAS_EXPLORA) for (const versao of VERSOES) {
    const H = tam[1], n = (c) => `${jan}-explora-${lugar}-${versao}-${c}`, r = { nome: `${jan}-explora-${lugar}-${versao}` };
    const { proc, url } = await subir(versao, cenario, amb);
    try {
      const p = await pagina(url, tam, r.nome, ESCALA[jan]);
      await menu(p);
      if (alongar) await p.evaluate((t) => { document.querySelector("#prompt .escolha .op-texto").textContent = t; }, alongar);
      r.simulado = alongar ? "SIM: a primeira opção recebe um texto que o jogo não tem (teste de esforço)" : "não: texto real do jogo";
      await p.mouse.move(5, H - 5); await espera(800);
      await p.screenshot({ path: path.join(SAIDA, `${n("tela")}.png`) });
      await recortar(p, ["#prompt"], n("1-normal"));
      Object.assign(r, await p.evaluate(() => {
        const l = document.querySelector("#prompt .escolhas"), bs = [...l.querySelectorAll(".escolha")];
        return { faixas: l.classList.contains("faixas"), opcoes: bs.map((e) => `${e.querySelector(".op-texto")?.textContent.trim()} (${Math.round(e.getBoundingClientRect().height)} px)`),
          riscos: [...l.querySelectorAll(".op-risco")].map((x) => x.textContent.trim()).join(" | ") || "nenhum",
          fonte: getComputedStyle(bs[0]).fontSize, cortados: bs.map((e) => e.querySelector(".rotulo")).filter((e) => e.scrollWidth > e.clientWidth + 1).length,
          sobrepostas: bs.some((e, i) => i && e.getBoundingClientRect().top < bs[i - 1].getBoundingClientRect().bottom - 0.5) };
      }));
      const bs = await p.$$("#prompt .escolha");
      const alta = await p.evaluate(() => { const bs = [...document.querySelectorAll("#prompt .escolha")]; let k = 0; bs.forEach((e, i) => { if (e.offsetHeight > bs[k].offsetHeight) k = i; }); return k; });
      await bs[alta].hover(); await espera(400);
      await recortar(p, ["#prompt"], n("2-mouse"));
      await p.mouse.down(); await espera(120);
      await recortar(p, ["#prompt"], n("3-pressionado"));
      await p.mouse.move(5, H - 5); await p.mouse.up(); await espera(300);
      r.soltar_fora = (await noMenu(p)) ? "nada escolhido" : "ERRO";
      await p.evaluate(() => document.activeElement && document.activeElement.blur());
      for (let k = 0; k < 40 && !(await p.evaluate(() => !!document.activeElement.closest("#prompt .escolha"))); k++) await p.keyboard.press("Tab");
      await recortar(p, ["#prompt"], n("4-foco"));
      r.clique = await p.evaluate(() => {
        const pg = document.getElementById("pagina").getBoundingClientRect(), doca = document.getElementById("doca")?.getBoundingClientRect();
        const pe = Math.min(pg.bottom, innerHeight, doca && doca.height ? doca.top : Infinity);
        const vistas = [...document.querySelectorAll("#prompt .escolha")].filter((e) => { const q = e.getBoundingClientRect(); return q.top >= pg.top && q.bottom <= pe; });
        const ruins = vistas.filter((e) => { const q = e.getBoundingClientRect(); return ![[0.5, 0.5], [0.08, 0.5], [0.95, 0.5], [0.5, 0.1], [0.5, 0.9]].every(([fx, fy]) => document.elementFromPoint(q.left + q.width * fx, q.top + q.height * fy)?.closest(".escolha") === e); });
        return `${vistas.length - ruins.length} de ${vistas.length} opções à vista respondem em todos os pontos${ruins.length ? "; AMBÍGUAS" : ""}`;
      });
      // o fluxo da Capela: escolher a ação real (o clique na faixa) segue como no jogo: entra no salão, gasta a tocha
      // (ou entra no escuro) e a luta começa; a tela inteira fica fotografada
      if (lugar === "capela" || lugar === "escura") {
        await p.mouse.move(5, H - 5);
        await (await p.$$("#prompt .escolha"))[0].click();
        for (let k = 0; k < 60 && !(await naVez(p)); k++) {
          const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {});
          await espera(250);
        }
        r.fluxo = await p.evaluate(() => `${document.getElementById("janela-confirmar") ? "abriu a confirmação" : "sem confirmação"}; ` +
          `${estado && estado.combate ? `a luta começou (${estado.combate.inimigos.length} inimigos)` : "SEM LUTA"}; ` +
          `${[...document.querySelectorAll("#texto p")].map((x) => x.textContent).find((t) => /tocha|escuro/i.test(t)) || ""}`);
        await p.mouse.move(5, H - 5); await espera(500);
        await p.screenshot({ path: path.join(SAIDA, `${n("5-escolheu")}.png`) });
      }
      relatorio.push(r);
      console.log(JSON.stringify(r));
      await p.close();
    } finally { proc.kill(); }
  }
}
// a vila não ganha faixas (o escopo aprovado é só o lugar selvagem)
if (filtro("EXPLORA", ["vila"]).includes("vila") || !process.env.EXPLORA) {
  const { proc, url } = await subir("depois", "tutorial", { TUTORIAL: "0", VISTAS, LUGAR: "vau", PERIODO: "1" });
  try {
    const p = await pagina(url, [1500, 950], "vila");
    for (let k = 0; k < 60 && !(await p.evaluate(() => typeof pergunta !== "undefined" && pergunta && !processando)); k++) await espera(250);
    await espera(800);
    relatorio.push({ nome: "vila", faixas_na_vila: await p.$$eval(".faixas", (x) => x.length) });
    await p.screenshot({ path: path.join(SAIDA, "normal-vila-depois-tela.png") });
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
writeFileSync(path.join(SAIDA, process.env.MANTER ? "relatorio-parcial.json" : "relatorio.json"),
  JSON.stringify({ antes: ANTES, versoes: VERSOES, relatorio, comportamentos, erros }, null, 1));
console.log(erros.length ? erros.join("\n") : "sem erros");
