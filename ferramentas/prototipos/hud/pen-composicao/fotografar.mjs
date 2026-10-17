// O teste do pen.dev (experimento): fotografa a bancada em tamanho real (1 px de tela por px de CSS), cada quadro
// (janela × estado) em cada versão (atual, a: o ajuste direto no CSS, b: o ajuste vindo do canvas do pen.dev), e mede
// a composição: a folga entre o nome e o custo, as linhas do nome, o alinhamento vertical do nome, do custo, do ícone e
// da tecla, o respiro da descrição e qualquer texto cortado. Precisa do servir.py no ar.
//   PLAYWRIGHT_MODULO=<caminho do playwright>/index.mjs node ferramentas/prototipos/hud/pen-composicao/fotografar.mjs
// (VERSOES=atual,a,b e BANCADA=<url> para escolher)
import { mkdirSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url));
const SAIDA = path.join(aqui, "capturas");
mkdirSync(SAIDA, { recursive: true });
const BANCADA = process.env.BANCADA || "http://localhost:8771/bancada.html";
const VERSOES = (process.env.VERSOES || "atual,a,b").split(",");
const b = await chromium.launch();
const medidas = {}, erros = [];
for (const versao of VERSOES) {
  const p = await b.newPage({ viewport: { width: 1000, height: 900 }, deviceScaleFactor: 1 });
  p.on("pageerror", (e) => erros.push(`${versao}: ${e}`));
  p.on("console", (m) => { if (m.type() === "error") erros.push(`${versao}: ${m.text()}`); });
  await p.goto(`${BANCADA}?versao=${versao}`);
  await p.waitForSelector("body[data-pronta]");
  for (const q of await p.$$(".bq-quadro")) {
    const nome = `${await q.getAttribute("data-janela")}-${await q.getAttribute("data-estado")}-${versao}`;
    await (await q.$(".roda-janela")).screenshot({ path: path.join(SAIDA, `${nome}.png`) });
    medidas[nome] = await q.evaluate((q) => {
      const j = q.querySelector(".roda-janela"), r = (e) => e.getBoundingClientRect(), cy = (e) => Math.round(r(e).top + r(e).height / 2);
      const faixas = [...j.querySelectorAll(".rj-linha")].map((l) => {
        const nome = l.querySelector(".rj-nome"), info = l.querySelector(".rj-info"), alt = parseFloat(getComputedStyle(nome).lineHeight);
        // a folga entre o fim do texto do nome (a linha mais larga) e o começo do custo
        const rg = document.createRange(); rg.selectNodeContents(nome);
        const fimNome = Math.max(...[...rg.getClientRects()].map((x) => x.right));
        return { nome: nome.textContent, linhas_do_nome: Math.round(r(nome).height / alt),
          folga_nome_custo: Math.round(r(info).left - fimNome), altura_faixa: Math.round(r(l).height),
          centro_y: { tecla: cy(l.querySelector(".tecla")) - cy(l), icone: cy(l.querySelector(".rj-icone")) - cy(l), nome: cy(l.querySelector(".rj-texto")) - cy(l), custo: cy(info) - cy(l) },
          custo_largura: Math.round(r(info).width) };
      });
      const caixa = j.querySelector(".rj-desc-caixa"), zona = j.querySelector(".rj-descricao"), lista = j.querySelector(".rj-lista");
      const cortados = [...j.querySelectorAll(".rj-nome, .rj-info, .rj-motivo, .rj-desc-caixa *")].filter((e) => e.scrollWidth > e.clientWidth + 1 || r(e).right > r(j).right + 0.5).map((e) => e.textContent.trim().slice(0, 30));
      return { seletor: `${Math.round(r(j).width)}×${Math.round(r(j).height)}`, faixas,
        descricao: { distancia_da_faixa: Math.round(r(caixa).top - r(lista).bottom), largura: Math.round(r(caixa).width), altura: Math.round(r(zona).height),
          esquerda_relativa_ao_nome: Math.round(r(caixa).left - r(j.querySelector(".rj-nome")).left) }, cortados };
    });
  }
  await p.close();
}
await b.close();
writeFileSync(path.join(SAIDA, "medidas.json"), JSON.stringify(medidas, null, 1));
for (const [n, m] of Object.entries(medidas)) console.log(n, m.seletor, m.faixas.map((f) => `${f.nome}: ${f.linhas_do_nome} linha(s), folga ${f.folga_nome_custo}`).join(" | "), "· desc", JSON.stringify(m.descricao), m.cortados.length ? `CORTADOS ${m.cortados}` : "");
console.log(erros.length ? erros.join("\n") : "sem erros");
