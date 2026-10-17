// A bancada do seletor (teste do pen.dev): monta, com o DOM que extrair.mjs tirou do jogo, uma composição pequena e
// parada: duas faixas (Flecha Envenenada, nome longo e custo duplo; Chuva de Flechas, indisponível) e a descrição, na
// largura real do seletor em cada janela, nos três estados lado a lado (o pen.dev importa uma página parada; o mouse
// não existe lá). Parâmetros: ?janela=1280x720|1500x950, ?estado=parado|destaque|indisponivel, ?versao=atual|a|b.
const JANELAS = (P.get("janela") || "1280x720,1500x950").split(",");
const ESTADOS = (P.get("estado") || "parado,destaque,indisponivel").split(",");
const HABS = ["flecha_envenenada", "chuva_flechas"];
const ROTULO = { parado: "normal (a descrição da última examinada)", destaque: "destacada (mouse ou teclado)", indisponivel: "indisponível destacada" };

// Os estados à força: as regras do mouse do seletor ("…:is(:hover, :focus-visible)") repetidas com a classe
// .x-destaque, tiradas da folha do jogo na hora (nada copiado à mão; o fio do foco do teclado fica de fora)
async function estadosAForca() {
  const folhas = ["/static/css/18-seletor-habilidades.css"];
  if (VERSAO !== "atual") folhas.push(`${VERSAO}-ajuste.css`);
  let css = "";
  for (const f of folhas) {
    const t = await (await fetch(f)).text();
    for (const regra of t.replace(/\/\*[\s\S]*?\*\//g, "").split("}")) {
      if (!/:is\(:hover, :focus-visible\)/.test(regra) || /@/.test(regra)) continue;
      css += regra.replace(/:is\(:hover, :focus-visible\)/g, ".x-destaque") + "}\n";
    }
  }
  const s = document.createElement("style");
  s.textContent = css;
  document.head.appendChild(s);
}

function montar(d, estado) {
  const S = d.seletor;
  const j = document.createElement("div");
  j.className = S.classes;
  j.dataset.tipo = S.tipo;
  j.style.cssText = `width: ${S.largura}px; --fundo-cena: ${S.fundo.cena}; --fundo-palco: ${S.fundo.palco};`;
  j.insertAdjacentHTML("beforeend", S.titulo);
  const lista = document.createElement("ul");
  lista.className = "rj-lista";
  lista.style.setProperty("--filas", 1);
  HABS.forEach((hab, i) => {
    const item = S.itens.find((x) => x.html.includes(`data-hab="${hab}"`));
    const li = document.createElement("li");
    li.dataset.forma = i % 3;
    li.style.cssText = `--i: ${i}; --fila: 0;`;
    li.innerHTML = item.html;
    li.querySelector(".tecla").textContent = i + 1;
    const b = li.querySelector(".rj-linha");
    if ((estado === "destaque" && i === 0) || (estado === "indisponivel" && b.classList.contains("bloqueada"))) b.classList.add("x-destaque");
    lista.appendChild(li);
  });
  j.appendChild(lista);
  // a descrição: embaixo da coluna da examinada, ou embaixo das duas ("junto"), como o jogo escolheu nessa janela
  const zona = document.createElement("div"), caixa = document.createElement("div");
  zona.className = "rj-descricao"; caixa.className = "rj-desc-caixa";
  zona.appendChild(caixa);
  j.appendChild(zona);
  if (S.voltar) j.insertAdjacentHTML("beforeend", S.voltar);
  return { j, lista, zona, caixa, hab: estado === "indisponivel" ? HABS[1] : HABS[0] };
}

// depois de estar na página: as medidas da caixa como em escolhas.js (descricoes): a faixa começa 12 px depois da tecla
function posicionar(m, d) {
  const lado = d.desc[m.hab].lado, Z = m.zona.getBoundingClientRect(), lis = [...m.lista.children];
  const coluna = (li) => { const r = li.getBoundingClientRect(); return { esq: r.left - Z.left + 12, larg: r.width - 12 }; };
  const esq = coluna(lis[0]), dir = coluna(lis[1]);
  const geo = lado === "junto" ? { esq: esq.esq, larg: dir.esq + dir.larg - esq.esq } : esq;  // as duas na mesma posição de coluna (a esquerda)
  const ladoAqui = lado === "junto" ? "junto" : m.hab === HABS[0] ? "esquerda" : "direita";
  const g = ladoAqui === "direita" ? dir : geo;
  m.caixa.dataset.lado = ladoAqui;
  m.caixa.style.cssText = `width: ${g.larg}px; left: ${g.esq}px; top: 0px;`;
  // a altura reservada: a maior das duas descrições nesse arranjo
  let h = 0;
  for (const hab of HABS) { m.caixa.innerHTML = d.desc[hab].html; h = Math.max(h, m.caixa.offsetHeight); }
  m.caixa.innerHTML = d.desc[m.hab].html;
  m.zona.style.height = `${h}px`;
}

(async () => {
  await estadosAForca();
  const raiz = document.getElementById("quadros");
  for (const jan of JANELAS) {
    const d = await (await fetch(`dados/seletor-${jan}.json`)).json();
    for (const estado of ESTADOS) {
      const q = document.createElement("section");
      q.className = "bq-quadro";
      q.dataset.janela = jan; q.dataset.estado = estado;
      q.innerHTML = `<p class="bq-rotulo">${jan.replace("x", "×")} · ${ROTULO[estado]} · versão ${VERSAO}</p>`;
      const palco = document.createElement("div");
      palco.className = "bq-palco";
      palco.style.width = `${d.seletor.largura}px`;
      const m = montar(d, estado);
      palco.appendChild(m.j);
      q.appendChild(palco);
      raiz.appendChild(q);
      posicionar(m, d);
    }
  }
  await document.fonts.ready;
  document.body.dataset.pronta = "1";
})();
