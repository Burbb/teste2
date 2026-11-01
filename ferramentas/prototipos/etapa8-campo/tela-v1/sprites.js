// PROTÓTIPO de campo livre: os combatentes em pixel, desenhados à mão numa grade (uma letra por pixel), virados para a
// direita; a esquerda é o espelho. Arte provisória para testar a escala: poucas poses funcionais e reaproveitadas
// (parado, duas passadas, preparo, golpe, recuo; caído é o recuo girado 90°, exato na grade). As mãos são pontinhos de
// pele, como nas figuras de cena. Sem contorno escuro nos soldados (a sombra no chão e o valor separam do piso); o
// herói tem contorno, a cor mais clara do campo e um anel no chão.
const PALETA = {
  k: "#1c1a24", K: "#34303c",
  h: "#d2d5db", H: "#959aa6", M: "#5d6170",
  s: "#e6b089", S: "#b97c55",
  p: "#4d3d33", P: "#2c231e",
  b: "#a0703f", B: "#6a4521",
  w: "#f4f6f8",
  y: "#f0cb62", Y: "#b08530",
  c: "#f3ead2", C: "#c9b78a",
  v: "#ece4cf", V: "#bfb196", X: "#2e3a52", Z: "#46577a",
  f: "#ffe08a", F: "#ff8a30", r: "#d2402c",
};
export const EQUIPES = [
  { t: "#76a8ea", T: "#4778c2", u: "#2d4f8a" },   // aliados: azul
  { t: "#de6a58", T: "#ad4237", u: "#6f2a29" },   // inimigos: vermelho
];

// as pernas, trocadas embaixo de qualquer tronco (3 linhas)
const PERNAS = {
  juntas: ["...p..p...", "...p..p...", "...P..P..."],
  abertas: ["..p....p..", "..p....p..", ".P......P."],
  cruzadas: ["....pp....", "....pp....", "....PP...."],
};
const PERNAS_HEROI = {
  juntas: ["....pp.pp....", "....pp.pp....", "....PP.PP...."],
  abertas: ["...pp...pp...", "..pp.....pp..", "..PP.....PP.."],
  cruzadas: [".....ppp.....", ".....ppp.....", ".....PPP....."],
};

// Os troncos (sem as pernas). Largura fixa por tipo; o pé fica na coluna `pe` da última linha.
const SOLDADO = {
  largura: 13, pe: 5,
  parado: [
    ".............",
    ".........w...",
    "....HHH..w...",
    "...HhhhH.w...",
    "...Hssk..w...",
    "....sSs.HHH..",
    "..tTtttTTs...",
    ".tuTtttT.....",
    ".tuTtttT.....",
    "..uuTTT......",
  ],
  preparo: [
    "........w....",
    "........w....",
    "...HHH..w....",
    "..HhhhH.w....",
    "..Hssk.HHH...",
    "...sSs.Ts....",
    ".tTtttTT.....",
    "tuTtttT......",
    "tuTtttT......",
    ".uuTTT.......",
  ],
  golpe: [
    ".............",
    ".............",
    ".....HHH.....",
    "....HhhhH....",
    "....Hssk.....",
    ".....sSs.....",
    "...tTtttTsHww",
    "..tuTtttT....",
    "..tuTtttT....",
    "...uuTTT.....",
  ],
  recuo: [
    ".............",
    ".............",
    "...HHH.......",
    "..HhhhH......",
    "..Hkks.......",
    "...sSs..w....",
    ".tTtttTsw....",
    "tuTtttT.w....",
    "tuTtttT......",
    ".uuTTT.......",
  ],
};

const ARQUEIRO = {
  largura: 13, pe: 5,
  parado: [
    ".............",
    ".............",
    "....uuu..b...",
    "...uTTTu.Bb..",
    "...usskT..b..",
    "....sSs...b..",
    "...TtttTsHb..",
    "...TtttT..b..",
    "...TtttT.b...",
    "...uTTTu.....",
  ],
  preparo: [
    ".............",
    ".............",
    "...uuu....b..",
    "..uTTTu...Bb.",
    "..usskT..w.b.",
    "...sSs..w..b.",
    "..TtttTsw.Hb.",
    "..TtttT..w.b.",
    "..TtttT...b..",
    "..uTTTu......",
  ],
  golpe: [
    ".............",
    ".............",
    "....uuu...b..",
    "...uTTTu..Bb.",
    "...usskT...b.",
    "....sSs....b.",
    "...TtttTTTsb.",
    "...TtttT...b.",
    "...TtttT..b..",
    "...uTTTu.....",
  ],
  recuo: [
    ".............",
    ".............",
    "...uuu.......",
    "..uTTTu..b...",
    "..ukksT..Bb..",
    "...sSs....b..",
    "..TtttTs..b..",
    "..TtttT...b..",
    "..TtttT..b...",
    "..uTTTu......",
  ],
};

const VETERANO = {
  largura: 13, pe: 5,
  parado: [
    ".............",
    "....MMM......",
    "...MhhhM.....",
    "...MHkkMw....",
    "...HsSsHw....",
    "..TTttTtTt...",
    ".uTTtttTtTt..",
    ".uTTtttTuTu..",
    ".uTTtttTuTu..",
    "..uTTTTu.u...",
  ],
  preparo: [
    "........w....",
    "...MMM..w....",
    "..MhhhM.w....",
    "..MHkkMHHH...",
    "..HsSsH.s....",
    ".TTttTtTt....",
    "uTTtttTtTt...",
    "uTTtttTuTu...",
    "uTTtttTuTu...",
    ".uTTTTu.u....",
  ],
  golpe: [
    ".............",
    ".....MMM.....",
    "....MhhhM....",
    "....MHkkM....",
    "....HsSsH....",
    "...TTttTtTsHw",
    "..uTTtttTtTt.",
    "..uTTtttTuTu.",
    "..uTTtttTuTu.",
    "...uTTTTu.u..",
  ],
  recuo: [
    ".............",
    "...MMM.......",
    "..MhhhM......",
    "..MHkkM......",
    "..HsSsH..w...",
    ".TTttTtTtw...",
    "uTTtttTtTt...",
    "uTTtttTuTu...",
    "uTTtttTuTu...",
    ".uTTTTu.u....",
  ],
};

// o porta-estandarte: o soldado com uma haste e a bandeira (duas posições do pano)
const ESTANDARTE = {
  largura: 13, pe: 5, pernas: "juntas",
  parado: [
    "........TTtt.",
    "........uTTt.",
    "....HHH.Ttt..",
    "...HhhhHb....",
    "...Hssk.b....",
    "....sSs.b....",
    "..tTtttTsb...",
    ".tuTtttT.b...",
    ".tuTtttT.b...",
    "..uuTTT..b...",
  ],
  preparo: [
    "........tTTt.",
    "........TTuT.",
    "....HHH.tTT..",
    "...HhhhHb....",
    "...Hssk.b....",
    "....sSs.b....",
    "..tTtttTsb...",
    ".tuTtttT.b...",
    ".tuTtttT.b...",
    "..uuTTT..b...",
  ],
};
ESTANDARTE.golpe = ESTANDARTE.parado;
ESTANDARTE.recuo = SOLDADO.recuo;

const CAMPEAO = {
  largura: 19, pe: 8, pernasLargura: true,
  parado: [
    "............hh.....",
    "...........hhHh....",
    "...........hHHb....",
    "......k.k...hhb....",
    "......MMM.....b....",
    ".....MhhhM....b....",
    ".....MkkkM....b....",
    "....uHsSsHu...b....",
    "...uTTtttTTu..b....",
    "..uTTttttTTTssb....",
    "..uTtTtttTtTu.b....",
    "..uTtTtttTtTu......",
    "...uTTTTTTTu.......",
    "....uuTTTuu........",
  ],
  preparo: [
    "......hh...........",
    ".....hHhh..........",
    ".....bHHh..........",
    "......bh...........",
    ".....k.bk..........",
    ".....MMMb..........",
    "....MhhhMb.........",
    "....MkkkM.b........",
    "...uHsSsHuss.......",
    "..uTTtttTTTu.......",
    ".uTTttttTTTu.......",
    ".uTtTtttTtTu.......",
    "..uTTTTTTTu........",
    "...uuTTTuu.........",
  ],
  golpe: [
    "...................",
    "...................",
    "...................",
    ".......k.k.........",
    ".......MMM.........",
    "......MhhhM........",
    "......MkkkM........",
    ".....uHsSsHu.......",
    "....uTTtttTTu......",
    "...uTTttttTTTssbbbh",
    "...uTtTtttTtTu..hHh",
    "...uTtTtttTtTu...hh",
    "....uTTTTTTTu......",
    ".....uuTTTuu.......",
  ],
};
CAMPEAO.recuo = CAMPEAO.parado;

const GUERREIRO = {
  largura: 17, pe: 6, heroi: true,
  parado: [
    "......yy.........",
    ".....yYy.....w...",
    "....hhhh.....w...",
    "...hhwhhh....w...",
    "...hsskhh....w...",
    "...csSsh.....w...",
    "..cChhhhhy..yYy..",
    ".cChhwhhhhhss....",
    ".cChhhhhhh.......",
    ".cChYyyYhh.......",
    "..CMhhhhM........",
    "...MMhhMM........",
  ],
  preparo: [
    ".........w.......",
    ".....yy..w.......",
    "....yYy..w.......",
    "...hhhh..w.......",
    "..hhwhhhyYy......",
    "..hsskhh.s.......",
    "..csSsh.hs.......",
    ".cChhhhhh........",
    "cChhwhhhh........",
    "cChhhhhhh........",
    "cChYyyYhh........",
    ".CMhhhhM.........",
  ],
  golpe: [
    ".................",
    ".......yy........",
    "......yYy........",
    "......hhhh.......",
    ".....hhwhhh......",
    ".....hsskhh......",
    "....ccsSsh.......",
    "...cChhhhhhssyYwww",
    "..cChhwhhhh..y...",
    "..cChhhhhhh......",
    "..cChYyyYhh......",
    "...CMhhhhM.......",
  ],
  recuo: [
    ".................",
    "....yy...........",
    "...yYy...........",
    "..hhhh...........",
    ".hhwhhh..........",
    ".hkkkhh....w.....",
    ".csSsh....w......",
    "cChhhhhhsw.......",
    "cChhwhhh.y.......",
    "cChhhhhh.........",
    "cChYyyYh.........",
    ".CMhhhhM.........",
  ],
};

const MAGO = {
  largura: 17, pe: 6, heroi: true,
  parado: [
    "......X......f...",
    ".....XZ.....fFf..",
    ".....XZX.....f...",
    "....XXZXX....b...",
    "..yYYYYYYYy..b...",
    "....vsskv....b...",
    "....vsSsv....b...",
    "...VvvvvvV..sb...",
    "..VvvyvvvvVs.b...",
    "..VvvyvvvvV..b...",
    "..VvvyvvvvV..b...",
    "..XVvvvvvVX..b...",
  ],
  preparo: [
    "......X...fFf....",
    ".....XZ..fFfFf...",
    ".....XZX..fFf....",
    "....XXZXX..b.....",
    "..yYYYYYYYyb.....",
    "....vsskv.sb.....",
    "....vsSsvs.b.....",
    "...VvvvvvV.......",
    "..VvvyvvvvV......",
    "..VvvyvvvvV......",
    "..VvvyvvvvV......",
    "..XVvvvvvVX......",
  ],
  golpe: [
    ".................",
    ".......X.........",
    "......XZ.........",
    "......XZX........",
    ".....XXZXX.......",
    "...yYYYYYYYy.....",
    ".....vsskv.......",
    ".....vsSsv.......",
    "....VvvvvvVssbbfF",
    "...VvvyvvvvV...ff",
    "...VvvyvvvvV.....",
    "...XVvvvvvVX.....",
  ],
  recuo: [
    ".................",
    "....X............",
    "...XZ............",
    "...XZX...........",
    "..XXZXX..........",
    "yYYYYYYYy....f...",
    "..vkksv.....fFf..",
    "..vsSsv....sb....",
    ".VvvvvvV..s.b....",
    "VvvyvvvvV...b....",
    "VvvyvvvvV...b....",
    "XVvvvvvVX........",
  ],
};

export const MODELOS = { soldado: SOLDADO, arqueiro: ARQUEIRO, veterano: VETERANO, estandarte: ESTANDARTE,
  campeao: CAMPEAO, guerreiro: GUERREIRO, mago: MAGO };

function montar(modelo, pose, pernas) {
  const tronco = modelo[pose];
  const lp = modelo.heroi || modelo.pernasLargura ? PERNAS_HEROI[pernas] : PERNAS[pernas];
  const desl = modelo.pe - (modelo.heroi || modelo.pernasLargura ? 6 : 4);
  const linhas = tronco.map((l) => l.padEnd(modelo.largura, "."));
  for (const l of lp) {
    let s = "";
    for (let x = 0; x < modelo.largura; x++) s += l[x - desl] || ".";
    linhas.push(s);
  }
  return linhas;
}

function pintar(linhas, cores, branco) {
  const w = linhas[0].length, h = linhas.length;
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  const g = c.getContext("2d");
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const ch = linhas[y][x];
    if (ch === "." || ch === undefined) continue;
    g.fillStyle = branco || cores[ch] || PALETA[ch] || "#f0f";
    g.fillRect(x, y, 1, 1);
  }
  return c;
}

// contorno de 1 px (só no herói): cada pixel vazio vizinho de um cheio
function contornar(c, cor) {
  const w = c.width + 2, h = c.height + 2;
  const o = document.createElement("canvas");
  o.width = w; o.height = h;
  const g = o.getContext("2d");
  const dados = c.getContext("2d").getImageData(0, 0, c.width, c.height).data;
  const cheio = (x, y) => x >= 0 && y >= 0 && x < c.width && y < c.height && dados[(y * c.width + x) * 4 + 3] > 0;
  g.fillStyle = cor;
  for (let y = -1; y <= c.height; y++) for (let x = -1; x <= c.width; x++) {
    if (cheio(x, y)) continue;
    if (cheio(x - 1, y) || cheio(x + 1, y) || cheio(x, y - 1) || cheio(x, y + 1)) g.fillRect(x + 1, y + 1, 1, 1);
  }
  g.drawImage(c, 1, 1);
  return o;
}

function espelhar(c) {
  const o = document.createElement("canvas");
  o.width = c.width; o.height = c.height;
  const g = o.getContext("2d");
  g.translate(c.width, 0);
  g.scale(-1, 1);
  g.drawImage(c, 0, 0);
  return o;
}

function girar(c, quartos) {
  const q = ((quartos % 4) + 4) % 4, o = document.createElement("canvas");
  o.width = q % 2 ? c.height : c.width;
  o.height = q % 2 ? c.width : c.height;
  const g = o.getContext("2d");
  g.translate(o.width / 2, o.height / 2);
  g.rotate((q * Math.PI) / 2);
  g.drawImage(c, -c.width / 2, -c.height / 2);
  return o;
}

/**
 * Todas as imagens prontas: Q[tipo][equipe][pose] = { d, e, branco_d, branco_e, ax, ay } (direita, esquerda, as
 * versões brancas do clarão de acerto e o ponto do pé). Poses: parado, andarA, andarB, preparo, golpe, recuo; e
 * caido (o recuo girado), giro0..giro3 (o corpo arremessado girando).
 */
export function prepararSprites() {
  const Q = {};
  for (const [tipo, mod] of Object.entries(MODELOS)) {
    Q[tipo] = [];
    for (let eq = 0; eq < 2; eq++) {
      const cores = EQUIPES[eq], poses = {};
      const def = mod.pernas || "juntas";
      const quadros = {
        parado: montar(mod, "parado", def), andarA: montar(mod, "parado", mod.pernas ? def : "abertas"),
        andarB: montar(mod, "parado", mod.pernas ? def : "cruzadas"), preparo: montar(mod, "preparo", def),
        golpe: montar(mod, "golpe", mod.heroi ? "abertas" : def), recuo: montar(mod, "recuo", def),
      };
      for (const [pose, linhas] of Object.entries(quadros)) {
        let img = pintar(linhas, cores), br = pintar(linhas, cores, "#ffffff");
        let ax = mod.pe + 0.5, ay = linhas.length;
        if (mod.heroi) { img = contornar(img, "#16131c"); br = contornar(br, "#16131c"); ax += 1; ay += 1; }
        poses[pose] = { d: img, e: espelhar(img), bd: br, be: espelhar(br), ax, ay, w: img.width, h: img.height };
      }
      const r = poses.recuo;
      for (let q = 0; q < 4; q++) {
        const g = girar(r.d, q);
        poses["giro" + q] = { d: g, e: espelhar(g), bd: g, be: g, ax: g.width / 2, ay: g.height / 2 + 2, w: g.width, h: g.height };
      }
      // caído: deitado de costas, a cabeça para o lado de onde veio o golpe
      const cd = girar(r.d, 3);
      poses.caido = { d: cd, e: espelhar(cd), bd: cd, be: cd, ax: cd.width / 2, ay: cd.height - 1, w: cd.width, h: cd.height };
      Q[tipo][eq] = poses;
    }
  }
  return Q;
}
