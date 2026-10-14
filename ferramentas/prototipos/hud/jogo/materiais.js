/* HUD experimental no jogo: os materiais de pixel do jogo na família de ferro. O jogo desenha os anéis, os bicos dos
   balões e as divisórias com pequenas grades de pixel (sprites-dados.js), publicadas como variáveis de CSS (--anel-j,
   --bico-a, --fio...). Aqui as mesmas grades são pintadas com as cores do ferro e publicadas no <body>, por cima das
   do jogo: tudo o que ainda usa o bronze (um cartão, um balão de prédio, uma dica) passa a usar o ferro, e os estados
   que o jogo troca pela variável (o mouse, o convite do mural, o destaque) continuam funcionando sozinhos. O ouro dos
   destaques (--anel-Y, --anel-y) e as cores de estado (vermelho, verde, raridades) ficam como estão. */
"use strict";

(() => {
  if (typeof SPRITES_GRADES === "undefined") return;
  const S = SPRITES_GRADES;
  const FERRO = "#3a3d43", FERRO_VIVO = "#6f737b", CANTO = "#4a4e56", FIO = "#2b2d31";

  /** A grade pintada com as cores dadas (o resto pela paleta do jogo; "." é transparente), como url() de CSS. */
  function pintar(grade, cores) {
    const c = document.createElement("canvas");
    c.width = grade[0].length; c.height = grade.length;
    const ctx = c.getContext("2d");
    grade.forEach((linha, y) => [...linha].forEach((ch, x) => {
      const cor = cores[ch] || (ch !== "." && Sprites.PALETA[ch]);
      if (cor) { ctx.fillStyle = cor; ctx.fillRect(x, y, 1, 1); }
    }));
    return `url(${c.toDataURL()})`;
  }

  const corpo = document.body.style;
  const publicar = (nome, valor) => corpo.setProperty(nome, valor);
  // o anel dos cartões e dos balões: ferro em repouso, ferro claro com o mouse (o "ouro velho" do jogo)
  publicar("--anel-j", pintar(S.anel_j, { j: FERRO }));
  publicar("--anel-a", pintar(S.anel_a, { a: FERRO_VIVO }));
  publicar("--bico-j", pintar(S.bico_j, { j: FERRO }));
  publicar("--bico-a", pintar(S.bico_a, { a: FERRO_VIVO }));
  // o nicho de retrato: o filete de ferro, com os cantos um passo mais claros no lugar dos esquadros de ouro
  publicar("--retrato-a", pintar(S.retrato_a, { J: FERRO, a: CANTO }));
  // as divisórias: só o fio (luz apagada e sombra), sem as pontas de ouro nem o losango do fim
  publicar("--fio", pintar(S.fio, { J: FIO }));
  publicar("--fio-v", pintar(S.fio_v, { J: FIO }));
  publicar("--fio-cabeca", pintar(S.fio_cabeca, { J: FIO, j: "#000000" }));
  for (const n of ["--ponta", "--estrelinha", "--fim-cabeca", "--ornamento"]) publicar(n, "none");
})();
