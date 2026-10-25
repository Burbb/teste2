// Fotografa e confere o "Carregar jogo" no jogo de verdade (cenarios_saves.py, saves temporários), hoje e na proposta R
// (VERSOES=atual,r), a 1920×945 e a 1280×720, nos casos vazia (o título sem "Carregar jogo"), uma, várias e muitas.
// Mede quanto o Voltar demora a aceitar o clique e a ficar opaco, se a lista rola, os cartões cortados, a ordem do
// teclado e o foco visível; abre o save do mundo gerado (a mensagem) e carrega uma campanha (a ficha dela).
// Guarda ../capturas/<janela>-<versão>-<caso>.png e ../capturas/medidas.json.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/carregar-jogo/auxiliares/fotografar.mjs
// (VERSOES=atual,r; CASOS=vazia,uma,varias,muitas; JANELAS=1920,1280)
import { spawn } from "child_process";
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../../..");
const SAIDA = path.join(aqui, "..", "capturas");
mkdirSync(SAIDA, { recursive: true });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
let falhas = 0;
const conferir = (ok, msg) => { console.log(`  ${ok ? "ok" : "FALHOU"}  ${msg}`); if (!ok) falhas++; };
const medidas = {};

async function subir(caso, proposta) {
  const proc = spawn(PY, [path.join(aqui, "cenarios_saves.py")], { cwd: raiz,
    env: { ...process.env, VELOCIDADE: "rapido", PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", PROPOSTA: proposta, CASO: caso } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 400 && !url; k++) await espera(100);
  if (!url) throw new Error(`o caso ${caso} não subiu`);
  return { proc, url };
}
const b = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const jan of (process.env.JANELAS || "1920,1280").split(",")) {
  const [W, H] = jan === "1920" ? [1920, 945] : [1280, 720];
  for (const caso of (process.env.CASOS || "vazia,uma,varias,muitas").split(",")) for (const v of (process.env.VERSOES || "atual,r").split(",")) {
    console.log(`== ${jan} ${v} ${caso}`);
    const { proc, url } = await subir(caso, v === "atual" ? "" : v);
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    const chave = `${jan}-${v}-${caso}`;
    try {
      await p.goto(url);
      await p.waitForSelector('#prompt .escolha:has-text("Novo jogo")', { timeout: 30000 });
      const titulo = await p.$$eval("#prompt .escolhas:not(.escolhido) .escolha", (bs) => bs.map((x) => x.textContent.trim()));
      if (caso === "vazia") {
        conferir(!titulo.some((t) => /Carregar/.test(t)), `sem saves, o título não oferece "Carregar jogo" (${titulo.join(" | ")})`);
        await p.screenshot({ path: path.join(SAIDA, `${chave}.png`) });
        await p.close(); proc.kill(); continue;
      }
      await p.mouse.move(2, 2);
      // medido dentro da página, a partir do envio da escolha (o fetch /responder): a lista chega; o Voltar usável (na
      // tela, com a pergunta pronta para ele); o Voltar opaco (passada a entrada da página)
      await p.evaluate((sel) => {
        window.__t = {};
        const voltar = () => sel === "r" ? document.querySelector(".sv-voltar")
          : [...document.querySelectorAll("#prompt .escolhas:not(.escolhido) .escolha")].find((e) => /Voltar/.test(e.textContent));
        const f = window.fetch;
        window.fetch = (...a) => { if (String(a[0]).includes("/responder") && !__t.envio) __t.envio = performance.now(); return f(...a); };
        const passo = () => {
          const n = performance.now(), e = voltar();
          if (!__t.lista && document.querySelector(".sv, .saves-lista")) __t.lista = n;
          if (e && __t.envio) {
            const r = e.getBoundingClientRect(); let o = 1; for (let x = e; x; x = x.parentElement) o *= parseFloat(getComputedStyle(x).opacity);
            const pronta = pergunta && pergunta.opcoes && pergunta.opcoes.some((q) => (q.meta && q.meta.voltar) || q.texto === "Voltar");
            if (!__t.usavel && pronta && r.width > 0 && r.bottom <= innerHeight) __t.usavel = n;
            if (!__t.opaco && pronta && o > 0.95 && r.bottom <= innerHeight) __t.opaco = n;
          }
          if (!__t.opaco) requestAnimationFrame(passo);
        };
        requestAnimationFrame(passo);
      }, v);
      await p.click('#prompt .escolha:has-text("Carregar")');
      await p.waitForFunction(() => __t.opaco, null, { timeout: 10000 }).catch(() => {});
      const tempos = await p.evaluate(() => ({ lista: __t.lista - __t.envio, usavel: __t.usavel - __t.envio, opaco: __t.opaco - __t.envio }));
      const [tLista, tUsa, tVer] = [tempos.lista, tempos.usavel, tempos.opaco].map((x) => Number.isFinite(x) ? Math.round(x) : null);
      await espera(900);
      await p.mouse.move(2, 2);
      await p.screenshot({ path: path.join(SAIDA, `${chave}.png`) });
      if (caso !== "uma") {  // o fim da lista (os que não abrem ficam lá embaixo, pela data)
        await p.evaluate(() => { const l = document.querySelector(".saves-lista, .sv-lista"); if (l) l.scrollTop = 1e6; });
        await espera(200);
        await p.screenshot({ path: path.join(SAIDA, `${chave}-fim.png`) });
        await p.evaluate(() => { const l = document.querySelector(".saves-lista, .sv-lista"); if (l) l.scrollTop = 0; });
      }
      const m = await p.evaluate(() => {
        const cartoes = [...document.querySelectorAll(".save-cartao, .sv-cartao")];
        const lista = document.querySelector(".saves-lista, .sv-lista");
        const cortados = cartoes.filter((c) => [...c.querySelectorAll("*")].some((e) => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).textOverflow !== "ellipsis" && getComputedStyle(e).overflow !== "visible")).length;
        return { cartoes: cartoes.length, rola: lista ? lista.scrollHeight > lista.clientHeight + 1 : false,
          alturaLista: lista ? Math.round(lista.getBoundingClientRect().height) : 0, cortados,
          larguraCartao: cartoes[0] ? Math.round(cartoes[0].getBoundingClientRect().width) : 0, rolaPagina: document.querySelector("#pagina").scrollHeight > document.querySelector("#pagina").clientHeight + 1 };
      });
      m.listaMs = tLista; m.voltarUsavelMs = tUsa; m.voltarOpacoMs = tVer;
      medidas[chave] = m;
      console.log("  ", JSON.stringify(m));
      conferir(tUsa !== null && tUsa - tLista < 50, `a lista em ${tLista} ms; o Voltar usável em ${tUsa} ms, opaco em ${tVer} ms`);
      // o teclado: o primeiro Tab (ou seta) chega a um cartão, com o foco visível; Esc volta ao título
      await p.keyboard.press(v === "r" ? "ArrowDown" : "Tab"); await espera(150);
      const foco = await p.evaluate(() => { const e = document.activeElement; const c = getComputedStyle(e);
        return { cartao: !!e.closest(".save-cartao, .sv-cartao"), anel: (c.outlineStyle !== "none" && parseFloat(c.outlineWidth) >= 2) || c.borderColor }; });
      conferir(foco.cartao, `o teclado chega a um cartão (foco: ${JSON.stringify(foco.anel)})`);
      await p.screenshot({ path: path.join(SAIDA, `${chave}-foco.png`) });
      await p.keyboard.press("Escape");
      await p.waitForSelector('#prompt .escolhas:not(.escolhido) .escolha:has-text("Novo jogo")', { timeout: 10000 });
      conferir(true, "Esc volta ao título");
      // o save do mundo gerado: a mensagem; depois, uma campanha carrega
      await p.click('#prompt .escolha:has-text("Carregar")'); await espera(800);
      if (caso !== "uma") {
        await p.click(':is(.save-cartao, .sv-cartao):has-text("Jean")');
        conferir(!!(await p.waitForSelector('#texto :text("Este save não abre")', { timeout: 10000 }).catch(() => null)), "o save do mundo gerado: a mensagem curta");
        for (let t = 0; t < 40 && !(await p.$('#prompt .escolhas:not(.escolhido) .escolha:has-text("Carregar")')); t++) {
          const c = await p.$("#prompt .continuar"); if (c) await c.click().catch(() => {}); await espera(200);
        }
        await p.click('#prompt .escolha:has-text("Carregar")'); await espera(800);
      }
      await p.click(':is(.save-cartao, .sv-cartao):has-text("Maria")');
      await p.waitForFunction(() => document.querySelector("#heroi .heroi-nome")?.innerText === "Maria", null, { timeout: 20000 });
      conferir(true, "a campanha de Maria carrega (a ficha dela)");
    } catch (e) { conferir(false, `${chave}: ${e.message.split("\n")[0]}`); }
    conferir(erros.length === 0, `sem erros na página ${erros.join(" ")}`);
    await p.close(); proc.kill();
  }
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
console.log(falhas ? `${falhas} falha(s)` : "tudo certo");
process.exit(falhas ? 1 : 0);
