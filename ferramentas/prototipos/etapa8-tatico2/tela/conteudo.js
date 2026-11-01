// PROTÓTIPO tático por turnos da etapa 8 (nada no jogo): todos os números e textos de regra. A referência principal é
// Dofus (casas, PA e PM, alcance e linha de visão, áreas, bloqueio, empurrão com dano de colisão); de Baldur's Gate 3
// entram só o chão que reage (fogo, barril de óleo) e a ideia de um efeito sustentado. O estudo está no
// roadmapIDEIAS/31. regras.js aplica tudo; a tela só desenha o que regras.js decide.

export const VERSAO = "Tático 2";
export const SEMENTE = 20261101;

// A vez: cada combatente recupera os PA e os PM no começo da própria vez; gasta-os na ordem que quiser (andar, agir,
// andar de novo, como em Dofus). Sair do contato com inimigos custa PM a mais (o bloqueio, determinístico).
export const REGRAS = {
  bloqueio: 1,          // PM a mais por inimigo em contato, ao sair de uma casa vizinha a ele (os "pesados" contam 2)
  colisao: 4,           // dano por casa que faltou no empurrão; quem foi atingido pela colisão leva a metade
  fogoChao: 5,          // dano do chão em chamas ao entrar ou ao começar a vez nele
  venenoChao: 4,
  marcado: 0.3,         // Marcado: +30% de dano recebido
  protegido: 0.5,       // Escudo Erguido: metade do dano
  inspirado: 0.25,      // Inspirado: +25% de dano causado
  coberto: 0.5,         // Cobrir (Morel): metade do dano vai para ele
};

// Estados: `ate` diz quando a duração conta (no começo ou no fim da vez de quem o carrega). Os textos são os da dica.
export const ESTADOS = {
  lento: { nome: "Lento", ate: "fim", ruim: true, texto: (v) => `Perde ${v} PM no começo da vez.` },
  imobilizado: { nome: "Imobilizado", ate: "fim", ruim: true, texto: () => "Fica sem PM na vez." },
  desequilibrado: { nome: "Desequilibrado", ate: "fim", ruim: true, texto: () => "Perde 2 PM no começo da vez." },
  marcado: { nome: "Marcado", ate: "fim", ruim: true, texto: () => "Recebe 30% a mais de dano." },
  congelado: { nome: "Congelado", ate: "fim", ruim: true, texto: () => "Perde 2 PM no começo da vez. Dano de fogo o consome." },
  ofuscado: { nome: "Ofuscado", ate: "fim", ruim: true, texto: () => "Alcance das habilidades 2 casas menor (mínimo 1)." },
  provocado: { nome: "Provocado", ate: "fim", ruim: true, texto: () => "Só pode atacar quem o provocou, se puder alcançá-lo." },
  protegido: { nome: "Escudo Erguido", ate: "inicio", texto: () => "Recebe metade do dano." },
  coberto: { nome: "Coberto", ate: "inicio", texto: () => "Metade do dano que recebe vai para Morel, se ele estiver vivo." },
  inspirado: { nome: "Inspirado", ate: "fim", texto: () => "Causa 25% a mais de dano." },
  abencoado: { nome: "Abençoado", ate: "inicio", texto: (v) => `Absorve os próximos ${v} de dano.` },
  barreira: { nome: "Barreira Arcana", ate: "inicio", texto: (v) => `Absorve os próximos ${v} de dano.` },
  olhoAguia: { nome: "Olho de Águia", ate: "fim", texto: () => "Alcance das habilidades 2 casas maior." },
};

// ------------------------------------------------------------------------------------------------ habilidades
// Campos: pa (custo), alcance [mín, máx], linha (só na mesma linha ou coluna), visao (precisa de linha de visão;
// padrão sim), alvo (inimigo, aliado, unidade, casa, livre, si), area ({f: alvo | cruz | circulo | raio | perp, r}),
// efeitos, esp (efeito especial em regras.js), porTurno, porAlvo, recarga (turnos seus), papel (para a montagem).
// `texto(k)`: a descrição, com os números do kit montado.
const H = {};

H.guerreiro = {
  golpe: { nome: "Golpe de Espada", pa: 3, alcance: [1, 1], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 12 }],
    papel: "dano", texto: (k) => `Causa ${k.efeitos[0].v} de dano.` },
  investida: { nome: "Investida", pa: 3, alcance: [2, 4], linha: true, alvo: "inimigo", recarga: 2, esp: "investida",
    efeitos: [{ t: "dano", v: 7 }], papel: "aproximação",
    texto: (k) => `Avança em linha reta até a casa vizinha do alvo e causa ${k.efeitos[0].v} de dano. O caminho precisa estar livre; avançar não sofre bloqueio.` },
  escudo: { nome: "Escudo Erguido", pa: 2, alcance: [0, 0], alvo: "si", recarga: 2, esp: "escudo",
    efeitos: [{ t: "estado", e: "protegido", turnos: 1 }], papel: "proteção",
    texto: (k) => `Você recebe metade do dano até o começo da sua próxima vez${k.raioProtege ? `, e os aliados a até ${k.raioProtege} casas também` : ""}.` },
  empurrao: { nome: "Golpe de Escudo", pa: 3, alcance: [1, 1], alvo: "inimigo", recarga: 1,
    efeitos: [{ t: "dano", v: 5 }, { t: "empurra", n: 3 }], papel: "deslocamento",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e empurra o alvo ${k.efeitos[1].n} casas. Cada casa que faltar por bater em algo causa ${k.colisao} de dano; quem for atingido pela colisão leva a metade.` },
  corrente: { nome: "Corrente", pa: 3, alcance: [2, 5], linha: true, alvo: "inimigo", recarga: 2,
    efeitos: [{ t: "puxa", n: 4 }, { t: "dano", v: 4 }], papel: "deslocamento",
    texto: (k) => `Puxa o alvo até ${k.efeitos[0].n} casas na sua direção e causa ${k.efeitos[1].v} de dano.` },
  redemoinho: { nome: "Redemoinho", pa: 4, alcance: [0, 0], alvo: "si", area: { f: "circulo", r: 1 }, recarga: 1,
    efeitos: [{ t: "dano", v: 9 }], papel: "área",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano em cada casa vizinha (aliados também).${k.curaPorAlvo ? ` Cura você em ${k.curaPorAlvo} por inimigo atingido.` : ""}` },
  provocar: { nome: "Provocar", pa: 2, alcance: [0, 0], alvo: "si", area: { f: "circulo", r: 3 }, recarga: 3, esp: "provocar",
    efeitos: [{ t: "estado", e: "provocado", turnos: 1 }], papel: "proteção",
    texto: () => "Os inimigos a até 3 casas ficam Provocados por 1 vez deles: só podem atacar você, se puderem alcançá-lo." },
  fenda: { nome: "Fenda no Chão", pa: 4, alcance: [1, 1], alvo: "casa", area: { f: "raio", r: 3 }, recarga: 2,
    efeitos: [{ t: "dano", v: 8 }, { t: "estado", e: "lento", turnos: 1, v: 1 }], papel: "linha",
    texto: (k) => `Abre o chão em linha reta por ${k.area.r} casas a partir da casa vizinha escolhida: causa ${k.efeitos[0].v} de dano e Lento 1 (perde 1 PM) por 1 vez do alvo.` },
  grito: { nome: "Grito de Guerra", pa: 2, alcance: [0, 0], alvo: "si", area: { f: "circulo", r: 2 }, recarga: 3, soAliados: true,
    efeitos: [{ t: "estado", e: "inspirado", turnos: 2 }], papel: "suporte",
    texto: () => "Você e os aliados a até 2 casas ficam Inspirados (+25% de dano) por 2 vezes de cada um." },
  atordoar: { nome: "Golpe no Joelho", pa: 3, alcance: [1, 1], alvo: "inimigo", recarga: 2,
    efeitos: [{ t: "dano", v: 6 }, { t: "estado", e: "desequilibrado", turnos: 1 }], papel: "controle",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e deixa o alvo Desequilibrado (perde 2 PM) na próxima vez dele.` },
};

H.mago = {
  faisca: { nome: "Faísca", pa: 2, alcance: [1, 6], alvo: "inimigo", porTurno: 3, efeitos: [{ t: "dano", v: 6, el: "fogo" }],
    papel: "dano", texto: (k) => `Causa ${k.efeitos[0].v} de dano de fogo.` },
  bola: { nome: "Bola de Fogo", pa: 4, alcance: [2, 6], alvo: "casa", area: { f: "circulo", r: 1 }, recarga: 1,
    efeitos: [{ t: "dano", v: 9, el: "fogo" }, { t: "chao", e: "fogo", turnos: 2 }], papel: "área",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano de fogo na casa e nas 4 vizinhas e deixa o chão em chamas por ${k.efeitos[1].turnos} rodadas (quem entra ou começa a vez nele leva ${k.fogoChao}).` },
  lanca: { nome: "Lança de Gelo", pa: 3, alcance: [1, 1], alvo: "casa", area: { f: "raio", r: 5 },
    efeitos: [{ t: "dano", v: 8, el: "gelo" }, { t: "estado", e: "congelado", turnos: 1 }], papel: "linha", porTurno: 2,
    texto: (k) => `Atravessa ${k.area.r} casas em linha reta a partir da casa vizinha escolhida: causa ${k.efeitos[0].v} de dano de gelo e Congela (perde 2 PM) por 1 vez do alvo.` },
  raios: { nome: "Corrente de Raios", pa: 4, alcance: [1, 5], alvo: "inimigo", recarga: 2, esp: "raios",
    efeitos: [{ t: "dano", v: 9, el: "raio" }], saltos: 2, salto: 2, papel: "área",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano no alvo e salta para o inimigo mais perto ainda não atingido, a até ${k.salto} casas, ${k.saltos} vezes; cada salto causa 2 a menos.` },
  muralha: { nome: "Muralha de Fogo", pa: 3, alcance: [2, 5], alvo: "casa", area: { f: "perp", r: 1 }, recarga: 3, livreArea: true,
    efeitos: [{ t: "chao", e: "fogo", turnos: 2 }], papel: "controle de espaço",
    texto: (k) => `Põe fogo em 3 casas lado a lado, atravessadas à sua linha de mira, por ${k.efeitos[0].turnos} rodadas (quem entra ou começa a vez nelas leva ${k.fogoChao}).` },
  piscar: { nome: "Piscar", pa: 2, alcance: [1, 4], alvo: "livre", recarga: 2, esp: "piscar", papel: "aproximação",
    efeitos: [], texto: () => "Reaparece na casa livre escolhida. Não sofre bloqueio." },
  repulsao: { nome: "Repulsão", pa: 3, alcance: [0, 0], alvo: "si", area: { f: "circulo", r: 1 }, recarga: 2,
    efeitos: [{ t: "dano", v: 4 }, { t: "empurra", n: 2 }], papel: "deslocamento",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e empurra ${k.efeitos[1].n} casas quem está nas casas vizinhas (aliados também).` },
  congelar: { nome: "Toque Gélido", pa: 3, alcance: [1, 5], alvo: "inimigo", porAlvo: 1,
    efeitos: [{ t: "dano", v: 4, el: "gelo" }, { t: "estado", e: "congelado", turnos: 2 }], papel: "preparação",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano de gelo e Congela o alvo por 2 vezes dele (perde 2 PM no começo da vez).` },
  combustao: { nome: "Combustão", pa: 3, alcance: [1, 6], alvo: "casa", area: { f: "circulo", r: 2 }, recarga: 2, esp: "combustao",
    efeitos: [{ t: "dano", v: 11, el: "fogo" }], papel: "consumo",
    texto: (k) => `Apaga o chão em chamas na área (casa e até 2 de distância): cada combatente sobre uma casa apagada leva ${k.efeitos[0].v} de dano de fogo.` },
  barreira: { nome: "Barreira Arcana", pa: 3, alcance: [0, 4], alvo: "aliado", recarga: 2,
    efeitos: [{ t: "estado", e: "barreira", turnos: 2, v: 12 }], papel: "suporte",
    texto: () => "O aliado (ou você) absorve os próximos 12 de dano, até o começo da 2ª vez dele." },
};

H.arqueiro = {
  flecha: { nome: "Flecha", pa: 3, alcance: [2, 7], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 9 }],
    papel: "dano", texto: (k) => `Causa ${k.efeitos[0].v} de dano.${k.porDistancia ? ` +${k.porDistancia} por casa de distância além de 4.` : ""}` },
  perfurante: { nome: "Tiro Perfurante", pa: 4, alcance: [2, 7], linha: true, alvo: "inimigo", recarga: 1, esp: "perfurante",
    efeitos: [{ t: "dano", v: 9 }], atravessa: 2, papel: "linha",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano no primeiro combatente da linha e continua até o alcance, atingindo até ${k.atravessa} combatentes (aliados também).` },
  chuva: { nome: "Chuva de Flechas", pa: 4, alcance: [3, 7], alvo: "casa", area: { f: "cruz", r: 1 }, recarga: 2,
    efeitos: [{ t: "dano", v: 7 }], papel: "área", texto: (k) => `Causa ${k.efeitos[0].v} de dano na casa e nas 4 vizinhas.` },
  repulsiva: { nome: "Flecha Repulsiva", pa: 3, alcance: [1, 6], alvo: "inimigo", recarga: 1,
    efeitos: [{ t: "dano", v: 5 }, { t: "empurra", n: 2 }], papel: "deslocamento",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e empurra o alvo ${k.efeitos[1].n} casas para longe de você.` },
  recuo: { nome: "Salto para Trás", pa: 2, alcance: [0, 0], alvo: "si", recarga: 2, esp: "recuo", distancia: 3, papel: "aproximação",
    efeitos: [], texto: (k) => `Salta até ${k.distancia} casas para longe do inimigo mais perto, em linha reta. Não sofre bloqueio.` },
  marca: { nome: "Marca do Caçador", pa: 2, alcance: [1, 8], alvo: "inimigo", recarga: 2,
    efeitos: [{ t: "estado", e: "marcado", turnos: 2 }], papel: "preparação",
    texto: (k) => `O alvo fica Marcado (recebe 30% a mais de dano de todos) por 2 vezes dele.${k.marcaLento ? " Também perde 1 PM (Lento) na próxima vez." : ""}` },
  armadilha: { nome: "Armadilha", pa: 3, alcance: [1, 4], alvo: "livre", esp: "armadilha", porTurno: 1, recarga: 1,
    efeitos: [{ t: "dano", v: 8 }, { t: "estado", e: "imobilizado", turnos: 1 }], papel: "controle de espaço",
    texto: (k) => `Arma a casa: o primeiro inimigo que entrar nela para, leva ${k.efeitos[0].v} de dano e fica Imobilizado (sem PM) na próxima vez dele. Até ${k.maxArmadilhas} armadilhas suas no campo.` },
  parabola: { nome: "Tiro em Parábola", pa: 4, alcance: [4, 8], visao: false, alvo: "inimigo", recarga: 1,
    efeitos: [{ t: "dano", v: 8 }], papel: "dano", texto: (k) => `Causa ${k.efeitos[0].v} de dano. Não precisa de linha de visão.` },
  olho: { nome: "Olho de Águia", pa: 1, alcance: [0, 0], alvo: "si", recarga: 3,
    efeitos: [{ t: "estado", e: "olhoAguia", turnos: 1 }], papel: "suporte",
    texto: () => "Até o fim desta vez, suas habilidades alcançam 2 casas a mais." },
  imobilizar: { nome: "Flecha nas Pernas", pa: 3, alcance: [2, 6], alvo: "inimigo", recarga: 2,
    efeitos: [{ t: "dano", v: 4 }, { t: "estado", e: "imobilizado", turnos: 1 }], papel: "controle",
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e deixa o alvo Imobilizado (sem PM) na próxima vez dele.` },
};

// Morel: o mercenário dos Cães de Ferro, escudo da comitiva. Odette: a clériga desertora, a cura e a luz. Kits
// próprios e fixos (os dois não escolhem habilidades neste protótipo); o jogador os controla nas vezes deles.
H.morel = {
  espada: { nome: "Lâmina Curta", pa: 3, alcance: [1, 1], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 10 }],
    texto: (k) => `Causa ${k.efeitos[0].v} de dano.` },
  ombro: { nome: "Avanço de Ombro", pa: 3, alcance: [2, 3], linha: true, alvo: "inimigo", recarga: 2, esp: "investida",
    efeitos: [{ t: "dano", v: 5 }, { t: "empurra", n: 1 }],
    texto: (k) => `Avança em linha reta até a casa vizinha do alvo, causa ${k.efeitos[0].v} de dano e o empurra 1 casa. Avançar não sofre bloqueio.` },
  cobrir: { nome: "Cobrir", pa: 2, alcance: [1, 2], alvo: "aliado", recarga: 1, soOutro: true,
    efeitos: [{ t: "estado", e: "coberto", turnos: 1 }],
    texto: () => "Até o começo da próxima vez de Morel, metade do dano que o aliado receber vai para Morel." },
  cao: { nome: "Grito dos Cães de Ferro", pa: 2, alcance: [0, 0], alvo: "si", area: { f: "circulo", r: 2 }, recarga: 3, esp: "provocar",
    efeitos: [{ t: "estado", e: "provocado", turnos: 1 }],
    texto: () => "Os inimigos a até 2 casas ficam Provocados por 1 vez deles: só podem atacar Morel, se puderem alcançá-lo." },
  baixo: { nome: "Golpe Baixo", pa: 2, alcance: [1, 1], alvo: "inimigo", porAlvo: 1,
    efeitos: [{ t: "dano", v: 4 }, { t: "estado", e: "desequilibrado", turnos: 1 }],
    texto: (k) => `Causa ${k.efeitos[0].v} de dano e deixa o alvo Desequilibrado (perde 2 PM) na próxima vez dele.` },
};

H.odette = {
  luz: { nome: "Luz Ardente", pa: 3, alcance: [1, 6], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 7, el: "luz" }],
    texto: (k) => `Causa ${k.efeitos[0].v} de dano de luz.` },
  prece: { nome: "Prece de Cura", pa: 3, alcance: [0, 4], alvo: "aliado", porAlvo: 1, porTurno: 2, efeitos: [{ t: "cura", v: 12 }],
    texto: (k) => `Cura ${k.efeitos[0].v} de vida do aliado (ou de Odette). Uma vez por alvo a cada vez.` },
  bencao: { nome: "Bênção", pa: 2, alcance: [0, 4], alvo: "aliado", recarga: 1,
    efeitos: [{ t: "estado", e: "abencoado", turnos: 2, v: 8 }],
    texto: () => "O aliado absorve os próximos 8 de dano, até o começo da 2ª vez dele." },
  clarao: { nome: "Clarão", pa: 4, alcance: [1, 5], alvo: "casa", area: { f: "cruz", r: 1 }, recarga: 2,
    efeitos: [{ t: "dano", v: 4, el: "luz" }, { t: "estado", e: "ofuscado", turnos: 1 }], soInimigos: true,
    texto: (k) => `Causa ${k.efeitos[0].v} de dano de luz aos inimigos na casa e nas 4 vizinhas e os deixa Ofuscados (alcance 2 menor) na próxima vez deles. Não atinge aliados.` },
  purificar: { nome: "Purificar", pa: 2, alcance: [0, 4], alvo: "aliado", recarga: 1, esp: "purificar", efeitos: [{ t: "cura", v: 4 }],
    texto: () => "Remove os estados ruins do aliado (Lento, Imobilizado, Desequilibrado, Marcado, Congelado, Ofuscado) e cura 4." },
};

// Os inimigos (kits fixos). `ia`: o papel para a IA (perto, longe, apoio, area, pesado).
H.bandido = {
  faca: { nome: "Faca", pa: 3, alcance: [1, 1], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 7 }], texto: (k) => `Causa ${k.efeitos[0].v} de dano.` },
  rasteira: { nome: "Rasteira", pa: 2, alcance: [1, 1], alvo: "inimigo", recarga: 2,
    efeitos: [{ t: "dano", v: 2 }, { t: "estado", e: "desequilibrado", turnos: 1 }], texto: () => "Causa 2 de dano e Desequilibra (perde 2 PM)." },
};
H.lobo = {
  mordida: { nome: "Mordida", pa: 3, alcance: [1, 1], alvo: "inimigo", porTurno: 2, esp: "matilha", efeitos: [{ t: "dano", v: 6 }],
    texto: () => "Causa 6 de dano; +3 se outro inimigo do alvo estiver vizinho dele (a matilha)." },
};
H.brutamontes = {
  soco: { nome: "Soco", pa: 3, alcance: [1, 1], alvo: "inimigo", porTurno: 1, efeitos: [{ t: "dano", v: 9 }], texto: () => "Causa 9 de dano." },
  esmagar: { nome: "Golpe Esmagador", pa: 3, alcance: [1, 1], alvo: "casa", area: { f: "perp", r: 1 }, recarga: 2, esp: "preparar",
    efeitos: [{ t: "dano", v: 16 }, { t: "empurra", n: 1 }],
    texto: () => "Marca 3 casas à frente; no começo da próxima vez dele, quem estiver nelas leva 16 de dano e é empurrado 1 casa." },
};
H.atirador = {
  flecha: { nome: "Flecha", pa: 3, alcance: [2, 7], alvo: "inimigo", porTurno: 2, efeitos: [{ t: "dano", v: 7 }], texto: () => "Causa 7 de dano." },
  prender: { nome: "Flecha nas Pernas", pa: 3, alcance: [2, 6], alvo: "inimigo", recarga: 3,
    efeitos: [{ t: "dano", v: 3 }, { t: "estado", e: "imobilizado", turnos: 1 }], texto: () => "Causa 3 de dano e Imobiliza (sem PM) na próxima vez." },
};
H.xama = {
  cura: { nome: "Seiva", pa: 3, alcance: [0, 5], alvo: "aliado", porAlvo: 1, porTurno: 2, efeitos: [{ t: "cura", v: 10 }], texto: () => "Cura 10 de vida de um aliado." },
  casca: { nome: "Pele de Casca", pa: 2, alcance: [0, 4], alvo: "aliado", recarga: 2, efeitos: [{ t: "estado", e: "barreira", turnos: 2, v: 8 }],
    texto: () => "O aliado absorve os próximos 8 de dano." },
  espinhos: { nome: "Espinhos", pa: 3, alcance: [1, 5], alvo: "inimigo", porTurno: 1, efeitos: [{ t: "dano", v: 6 }], texto: () => "Causa 6 de dano." },
};
H.bruxa = {
  nuvem: { nome: "Nuvem Venenosa", pa: 4, alcance: [2, 6], alvo: "casa", area: { f: "circulo", r: 1 }, recarga: 2,
    efeitos: [{ t: "dano", v: 5 }, { t: "chao", e: "veneno", turnos: 2 }], texto: () => "Causa 5 de dano na casa e nas 4 vizinhas e envenena o chão por 2 rodadas (4 a quem entra ou começa a vez nele)." },
  maldicao: { nome: "Maldição", pa: 2, alcance: [1, 6], alvo: "inimigo", recarga: 2, efeitos: [{ t: "estado", e: "marcado", turnos: 1 }],
    texto: () => "Marca o alvo (+30% de dano recebido) na próxima vez dele." },
  dardo: { nome: "Dardo Sombrio", pa: 3, alcance: [1, 6], alvo: "inimigo", porTurno: 1, efeitos: [{ t: "dano", v: 6 }], texto: () => "Causa 6 de dano." },
};
export const HABILIDADES = H;

// ------------------------------------------------------------------------------------------------ talentos
// Dois por luta, escolhidos entre cinco. Cada um muda o uso de uma habilidade ou do espaço; a regra fica em regras.js
// (`tem(u, id)`) ou no kit montado (`mod`).
export const MAX_TALENTOS = 2;
export const TALENTOS = {
  guerreiro: {
    muralhaViva: { nome: "Muralha Viva", texto: "Inimigos vizinhos pagam 2 PM a mais (em vez de 1) para sair do contato com você." },
    impacto: { nome: "Impacto", texto: "Seus empurrões causam o dobro de dano de colisão." },
    guardiao: { nome: "Guardião", requer: "escudo", texto: "Escudo Erguido também protege os aliados a até 2 casas.", mod: (k) => { if (k.escudo) k.escudo.raioProtege = 2; } },
    embalo: { nome: "Embalo", requer: "investida", texto: "Depois da Investida, o próximo Golpe de Espada nesta vez causa +6." },
    sede: { nome: "Sede de Batalha", requer: "redemoinho", texto: "O Redemoinho cura você em 3 por inimigo atingido.", mod: (k) => { if (k.redemoinho) k.redemoinho.curaPorAlvo = 3; } },
  },
  mago: {
    seletivas: { nome: "Chamas Seletivas", texto: "Seu dano de fogo e o seu chão em chamas não ferem aliados." },
    estilhacar: { nome: "Estilhaçar", texto: "Dano direto de fogo ou de raio num alvo Congelado consome o gelo e causa +8." },
    labareda: { nome: "Labareda", requer: "bola", texto: "O chão em chamas que você cria dura 1 rodada a mais.", mod: (k) => { for (const h of Object.values(k)) for (const e of h.efeitos) if (e.t === "chao") e.turnos += 1; } },
    condutor: { nome: "Condutor", requer: "raios", texto: "A Corrente de Raios salta 1 vez a mais.", mod: (k) => { if (k.raios) k.raios.saltos += 1; } },
    mente: { nome: "Mente Ágil", requer: "piscar", texto: "Piscar custa 1 PA." , mod: (k) => { if (k.piscar) k.piscar.pa = 1; } },
  },
  arqueiro: {
    distancia: { nome: "Olho Treinado", requer: "flecha", texto: "A Flecha causa +1 por casa de distância além de 4.", mod: (k) => { if (k.flecha) k.flecha.porDistancia = 1; } },
    perseguidor: { nome: "Perseguidor", requer: "marca", texto: "A Marca do Caçador também deixa o alvo Lento 1 na próxima vez dele.", mod: (k) => { if (k.marca) k.marca.marcaLento = true; } },
    armadilheiro: { nome: "Armadilheiro", requer: "armadilha", texto: "Até 3 armadilhas suas no campo (em vez de 1), e a Armadilha custa 2 PA.", mod: (k) => { if (k.armadilha) { k.armadilha.maxArmadilhas = 3; k.armadilha.pa = 2; } } },
    emboscada: { nome: "Emboscada", texto: "Seu dano é 25% maior em inimigos que não estão vizinhos de nenhum aliado deles." },
    leveza: { nome: "Pés Leves", texto: "Você não sofre bloqueio ao sair do contato com inimigos." },
  },
};

// ------------------------------------------------------------------------------------------------ combatentes
// pv, pa, pm, ini (iniciativa: ordena a fila de cada lado), modelo (sprite), papel (IA), pesado (conta 2 no bloqueio),
// agil (não sofre bloqueio).
export const CLASSES = {
  guerreiro: { nome: "Guerreiro", pv: 64, pa: 6, pm: 3, ini: 10, modelo: "guerreiro", tamKit: 6 },
  mago: { nome: "Mago", pv: 44, pa: 6, pm: 3, ini: 12, modelo: "mago", tamKit: 6 },
  arqueiro: { nome: "Arqueiro", pv: 48, pa: 6, pm: 4, ini: 14, modelo: "arqueiroHeroi", tamKit: 6 },
};
export const COMPANHEIROS = {
  morel: { nome: "Morel", pv: 72, pa: 6, pm: 3, ini: 8, modelo: "morel", pesado: true, kit: ["espada", "ombro", "cobrir", "cao", "baixo"] },
  odette: { nome: "Odette", pv: 46, pa: 6, pm: 3, ini: 9, modelo: "odette", kit: ["luz", "prece", "bencao", "clarao", "purificar"] },
};
export const INIMIGOS = {
  bandido: { nome: "Bandido", pv: 30, pa: 6, pm: 4, ini: 11, modelo: "soldado", papel: "perto", kit: ["faca", "rasteira"] },
  lobo: { nome: "Lobo", pv: 22, pa: 6, pm: 5, ini: 13, modelo: "lobo", papel: "perto", agil: true, kit: ["mordida"] },
  brutamontes: { nome: "Brutamontes", pv: 62, pa: 6, pm: 3, ini: 6, modelo: "campeao", papel: "pesado", pesado: true, kit: ["soco", "esmagar"] },
  atirador: { nome: "Atirador", pv: 26, pa: 6, pm: 3, ini: 10, modelo: "arqueiro", papel: "longe", kit: ["flecha", "prender"] },
  xama: { nome: "Xamã", pv: 28, pa: 6, pm: 3, ini: 8, modelo: "xama", papel: "apoio", kit: ["cura", "casca", "espinhos"] },
  bruxa: { nome: "Bruxa", pv: 26, pa: 6, pm: 3, ini: 9, modelo: "bruxa", papel: "area", kit: ["nuvem", "maldicao", "dardo"] },
};

// As montagens prontas (dois caminhos por classe; tudo continua editável na preparação).
export const BUILDS = {
  guerreiro: {
    "Muralha": { kit: ["golpe", "escudo", "provocar", "empurrao", "atordoar", "grito"], talentos: ["muralhaViva", "guardiao"] },
    "Arremesso": { kit: ["golpe", "investida", "empurrao", "corrente", "redemoinho", "fenda"], talentos: ["impacto", "embalo"] },
  },
  mago: {
    "Piromante": { kit: ["faisca", "bola", "muralha", "combustao", "piscar", "barreira"], talentos: ["seletivas", "labareda"] },
    "Criomante": { kit: ["faisca", "lanca", "congelar", "raios", "repulsao", "piscar"], talentos: ["estilhacar", "condutor"] },
  },
  arqueiro: {
    "Atirador": { kit: ["flecha", "perfurante", "chuva", "olho", "recuo", "parabola"], talentos: ["distancia", "emboscada"] },
    "Caçador": { kit: ["flecha", "marca", "armadilha", "imobilizar", "repulsiva", "recuo"], talentos: ["perseguidor", "armadilheiro"] },
  },
};

// ------------------------------------------------------------------------------------------------ arenas
// Uma letra por casa: "." chão, "#" pilar alto (bloqueia passagem e visão), "r" rocha baixa (bloqueia passagem, deixa
// ver), "~" água (bloqueia passagem, deixa ver), "o" barril de óleo (bloqueia passagem e visão; dano de fogo o
// explode: 8 de dano na cruz em volta e chão em chamas), "a" e "e": chão onde começam aliados e inimigos (na ordem),
// " " fora da arena. A vista é em losangos: x cresce para baixo e à direita, y para baixo e à esquerda.
export const ARENAS = {
  aberto: { nome: "Campo aberto", mapa: [
    "  ..........  ",
    " ............ ",
    "..e.....e.....",
    "........r.....",
    "...e.......e..",
    "......e.......",
    "..r......#....",
    "..............",
    "....#.....r...",
    "..............",
    "...a....a.....",
    "......a.......",
    " ............ ",
    "  ..........  ",
  ] },
  passagem: { nome: "A passagem", mapa: [
    "  ..........  ",
    " ...e..e..... ",
    "....e....e....",
    "..........e...",
    "###r##..##o###",
    "..............",
    "..~~......o...",
    "..~~..#.......",
    "....o.........",
    "###.##..##r###",
    "..............",
    "...a...a......",
    " .....a...... ",
    "  ..........  ",
  ] },
  misto: { nome: "Perto, longe e apoio", mapa: [
    "  ...e..e...  ",
    " ..........e. ",
    "...e....#.....",
    ".#......e.....",
    "......r....#..",
    "...~~~........",
    "...~~~...o....",
    "..........r...",
    "..#.....#.....",
    "......o.......",
    "....r.........",
    "..a....a......",
    " .....a...... ",
    "  ..........  ",
  ] },
};

// Os encontros: cinco inimigos cada, na ordem das casas "e" da arena.
export const ENCONTROS = {
  aberto: { nome: "Campo aberto", arena: "aberto", inimigos: ["lobo", "lobo", "atirador", "lobo", "bandido"],
    texto: "Três lobos rápidos, um bandido e um atirador num campo quase sem cobertura." },
  passagem: { nome: "A passagem", arena: "passagem", inimigos: ["brutamontes", "bandido", "bruxa", "bandido", "atirador"],
    texto: "Dois muros com três aberturas e barris de óleo. Um brutamontes segura a passagem; a bruxa envenena o chão." },
  misto: { nome: "Perto, longe e apoio", arena: "misto", inimigos: ["atirador", "atirador", "brutamontes", "bandido", "xama"],
    texto: "Um brutamontes e um bandido na frente, dois atiradores atrás dos pilares e uma xamã que cura e protege." },
};
