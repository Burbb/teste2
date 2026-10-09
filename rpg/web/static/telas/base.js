/* Telas: o que o motor manda desenhar fora da luta, uma tela por arquivo nesta pasta (inventário, mercado, diário,
   fogueira...), mais as dicas, os menus de item e as celebrações. Aqui ficam as peças comuns: o nome Telas, onde cada
   arquivo põe o que oferece; o painel, que acha a tela pelo tipo; e o que várias telas usam (barra, ícones, efeitos). */
"use strict";

/** Cada arquivo de telas/ põe aqui o que oferece (Object.assign, no fim dele) e tira daqui o que usa dos outros
 *  (const { ... } = Telas, no começo), na ordem dos <script> do index.html. Pedir um nome que ninguém pôs é erro na
 *  hora, com o nome, em vez de um undefined que só estoura no clique. */
const Telas = new Proxy({}, {
  get(alvo, nome) {
    if (typeof nome === "string" && !(nome in alvo) && nome !== "then" && nome !== "toJSON") {
      throw new Error(`Telas.${nome} não existe (nome errado, ou o arquivo que o põe carrega depois)`);
    }
    return alvo[nome];
  },
});

(() => {
  const h = Texto.html;
  const S = (nome, escala = 2, classe = "") => Sprites.img(nome, escala, classe);

  /** O ícone de um consumível ou recurso (comida, flechas): vem do catálogo do motor (itens.py), no estado. */
  function iconeConsumivel(id, padrao = "pocao") {
    const c = App.estado && App.estado.itens && App.estado.itens[id];
    return (c && c.icone) || padrao;
  }

  /** Quanto `atual` é de `maximo`, de 0 a 100: a largura de uma barra. */
  function pct(atual, maximo) {
    return maximo ? Math.max(0, Math.min(100, (100 * atual) / maximo)) : 0;
  }
  function barra(classe, atual, maximo) {
    const p = pct(atual, maximo);
    return `<span class="barra-px ${classe}"><span class="enchimento" style="width:${p}%"></span></span>`;
  }

  /** Faíscas que saem de um elemento (talento aprendido, compra...). */
  function faiscas(el, cores, n = 14) {
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    for (let i = 0; i < n; i++) {
      const p = document.createElement("i");
      p.className = "faisca";
      p.style.left = cx + "px"; p.style.top = cy + "px";
      p.style.background = cores[i % cores.length];
      document.body.appendChild(p);
      const ang = (i / n) * Math.PI * 2 + Math.random() * 0.4, dist = 40 + Math.random() * 46;
      p.animate([{ transform: "translate(-50%, -50%) scale(1)", opacity: 1 },
        { transform: `translate(calc(-50% + ${Math.cos(ang) * dist}px), calc(-50% + ${Math.sin(ang) * dist}px)) scale(0.4)`, opacity: 0 }],
        { duration: 420 + Math.random() * 180, easing: "cubic-bezier(.15,.7,.3,1)" }).finished.then(() => p.remove(), () => p.remove());
    }
  }

  /** Moedas voando de um ponto da tela até outro (o ouro do topo). */
  function moedasPara(de, para) {
    if (!de || !para) return;
    const a = de.getBoundingClientRect(), b = para.getBoundingClientRect();
    for (let i = 0; i < 10; i++) {
      const m = document.createElement("span");
      m.className = "moeda-voando";
      m.innerHTML = S("moeda", 1);
      m.style.left = a.left + a.width / 2 + (Math.random() - 0.5) * 40 + "px";
      m.style.top = a.top + a.height / 2 + "px";
      document.body.appendChild(m);
      m.animate([{ transform: "translate(0, 0) scale(1)", opacity: 1 },
        { transform: `translate(${b.left + b.width / 2 - a.left - a.width / 2}px, ${b.top + b.height / 2 - a.top - a.height / 2}px) scale(0.6)`, opacity: 0.9 }],
        { duration: 520 + i * 40, delay: i * 35, easing: "cubic-bezier(.5,0,.8,.6)", fill: "forwards" }).finished
        .then(() => { m.remove(); para.classList.remove("ganhou"); void para.offsetWidth; para.classList.add("ganhou"); }).catch(() => m.remove());
    }
  }

  /** Os quadros rápidos sobre o jogo (amanhecer, espólio) ficam no meio da coluna do jogo, e não no meio da janela:
   *  os painéis dos lados têm larguras diferentes, e o quadro ficava torto em relação à cena. `sobreTitulo`: na altura
   *  em que o título do lugar fica no quadro da página (o amanhecer, curto); senão, no meio da coluna. A altura vem do
   *  quadro da página, que não rola: o título rola junto com o texto, e o quadro saía fora do lugar. Numa tela estreita,
   *  sem a coluna, ficam no meio da janela. */
  function noPalco(festa, sobreTitulo = false) {
    const palco = document.getElementById("palco"), p = palco && palco.getBoundingClientRect();
    if (!festa || !p || !p.width) return;
    const pg = document.getElementById("cena").getBoundingClientRect();
    const y = sobreTitulo && pg.height ? pg.top + Math.min(pg.height * 0.4, 230) : p.top + p.height * 0.45;
    const meio = festa.offsetHeight / 2 + 8;
    festa.classList.add("no-palco");
    festa.style.left = p.left + p.width / 2 + "px";
    festa.style.top = Math.max(meio, Math.min(innerHeight - meio, y)) + "px";
  }

  function toast(titulo, texto, icone, bom) {
    const t = document.createElement("div");
    t.className = "toast" + (bom ? " bom" : "");
    t.innerHTML = `${S(icone, 2)}<div>${titulo ? `<b>${h(titulo)}</b>` : ""}${h(texto || "")}</div>`;
    document.getElementById("toasts").appendChild(t);
    setTimeout(() => t.remove(), 3300);
  }

  // ------------------------------------------------------------------ painel
  /* As telas de painel: cada arquivo registra a sua com o tipo que o motor manda (ponte.py, "painel").
     `desenhar(dados)` devolve o HTML; `ligar(raiz, dados)` põe os ouvintes depois de desenhada; `esquecer()` apaga o
     que a tela lembra entre um redesenho e outro, quando você sai dela (novaVisita). */
  const TELAS = {};
  function registrar(tipo, desenhar, { ligar = null, esquecer = null } = {}) {
    TELAS[tipo] = { desenhar, ligar, esquecer };
  }
  function painel(m) {
    Telas.esconderDica();  // a tela foi redesenhada: a dica antiga ficaria órfã
    const div = document.createElement("div");
    const tela = TELAS[m.tipo];
    div.innerHTML = tela ? tela.desenhar(m.dados) : "";
    if (tela && tela.ligar) tela.ligar(div, m.dados);
    Telas.ligarDicas(div);
    return div;
  }
  /** Saiu da tela: cada uma esquece o que lembrava (a quantidade do mercado volta a 1; o contrato recém-aceito
   *  deixa de ser novidade). */
  function novaVisita() {
    Object.values(TELAS).forEach((t) => t.esquecer && t.esquecer());
  }

  Object.assign(Telas, { barra, faiscas, h, iconeConsumivel, moedasPara, noPalco, novaVisita, painel, pct, registrar,
                         S, toast });
})();
