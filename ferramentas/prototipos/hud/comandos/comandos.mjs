// Os comandos da luta e as escolhas da exploração na linguagem do seletor D refinado (protótipo): o que a página da
// foto recebe além das folhas desta pasta. O jogo não muda; fotografar_comandos.mjs serve isto só na página.
//
// 1. ponte(css18): as pontas e o meio das faixas moram hoje só dentro do seletor (`:root body .roda-janela.seletor
//    { --sh-ponta-e0 ... --sh-meio }`, em css/18-seletor-habilidades.css). Os comandos da roda e as escolhas da
//    exploração precisam das mesmas peças: em vez de copiar os desenhos, a ponte lê aquele bloco do arquivo do jogo e o
//    declara também para #roda e #prompt. Numa integração, o bloco subiria para um lugar comum (:root) e a ponte sai.
// 2. escolhas(js): uma troca no app/escolhas.js, só para marcar a amostra: a lista de um menu de lugar selvagem
//    (o que tem "Explorar a região" e "Viajar") ganha a classe "amostra-faixas". Nenhuma outra tela recebe o estilo;
//    o que as opções fazem (teclas, clique, indisponível, dica) é o código do jogo.
// Cada troca procura o texto exato do jogo e para se ele mudou. O checkout do Windows traz CRLF: tudo é comparado em LF.
const LF = (t) => t.split("\r\n").join("\n");

export function ponte(css18) {
  const m = LF(css18).match(/:root body \.roda-janela\.seletor \{\n(\s+--sh-ponta-e0:[\s\S]*?--sh-meio:[^\n]*\n)\}/);
  if (!m) throw new Error("18-seletor-habilidades.css mudou: não achei o bloco das pontas (--sh-ponta-e0 ... --sh-meio)");
  return `/* gerado por comandos/comandos.mjs a partir de css/18-seletor-habilidades.css: as mesmas pontas do seletor */\n` +
    `:root body :is(#roda, #prompt) {\n${m[1]}}\n`;
}

const TROCAS = [
  ['  const lista = el("ol", "escolhas");\n',
    `  const lista = el("ol", "escolhas");
  // [protótipo] a amostra fora da luta: só as escolhas de um lugar selvagem (Explorar, Acampar, Viajar)
  if (!emLuta && m.opcoes.some((o) => /^Explorar a região/.test(o.texto)) && m.opcoes.some((o) => o.texto === "Viajar")) lista.classList.add("amostra-faixas");
`],
];

export function escolhas(js) {
  return TROCAS.reduce((t, [a, b]) => {
    if (!t.includes(a)) throw new Error(`escolhas.js mudou: não achei ${a.slice(0, 60)}...`);
    return t.replace(a, b);
  }, LF(js));
}
