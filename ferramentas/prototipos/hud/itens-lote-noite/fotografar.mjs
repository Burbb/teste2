// O lote de itens da noite (proposta, nada no jogo): fotografa cada desenho novo nos lugares onde ele fica parado,
// atual × proposta, nas janelas normal (1500×950) e baixa (1280×720), com o jogo intacto. A página recebe os arquivos
// da proposta no lugar dos do jogo (page.route em /static/hud/icones/<peça>-*.png, como fotografar_escudo.mjs); uma
// peça que ainda não tem papel em icones.js (a calça de couro) ganha o papel só nesta página.
//   PLAYWRIGHT_MODULO=<caminho>/index.mjs node ferramentas/prototipos/hud/itens-lote-noite/fotografar.mjs <peça>
// peça: calca_couro | aljava | atributos | ataque_defesa | agilidade_poder | agilidade | aljava_ref | poder | doca_r2 | doca_r3 | doca_r3_luta | doca_r4 | doca_r4_telas | doca_r5 | doca
//       | vida_mana | vigor_foco | vigor_foco_arqueiro | ouro_provisoes | moeda | tocha | tocha16 | tocha16_risco | tocha_apagada
//       | bandagem_pocao | bandagem_pocao_luta | tonico_antidoto | calca_manto | calca_manto_saque_calca
//       | frasco_vazio | frasco_cheio | antidoto_base | anel_amuleto | anel_amuleto_saque_amuleto | sandalia_chapeu | sandalia_chapeu_saque_chapeu
//       | chapeu_no_jogo | sandalia_r2 | besta | diadema | coroa_afogados | espada | espada_luta | maca
import { spawn } from "child_process";
import { readFileSync, existsSync, mkdirSync } from "fs";
import { fileURLToPath } from "url";
import path from "path";
const { chromium } = await import(process.env.PLAYWRIGHT_MODULO || "playwright");
const aqui = path.dirname(fileURLToPath(import.meta.url)), raiz = path.resolve(aqui, "../../../..");
const peca = process.argv[2];
const PY = process.env.PYTHON || (process.platform === "win32" ? "python" : "python3");
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
// JANELAS=1920x945 (a janela principal do Jean) ou a lista padrão: a normal e a baixa
const JANELAS = process.env.JANELAS ? process.env.JANELAS.split(",").map((j) => j.split("x").map(Number)) : [[1500, 950], [1280, 720]];
const VISTAS = "A1,A0,AL,V2,V5,N1,D1,K1,M1,L1,F1,F2,F3,F4";

// cada peça: a pasta da proposta, os nomes de arquivo que ela troca, o papel novo (se houver) e as fotos
const PECAS = {
  calca_couro: { pasta: "calca_couro/proposta", nomes: ["calca_couro"], papel: { item: "calca_couro", tamanhos: [32, 40, 48, 64] },
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "calca_couro", VESTIDO: "calca_couro" }] },
  aljava: { pasta: "aljava/proposta", nomes: ["aljava"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo", "ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "aljava", VESTIDO: "aljava" }] },
  atributos: { pasta: "atributos/proposta", nomes: ["attr-ataque", "attr-defesa", "attr-agilidade", "attr-poder"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "luta"] },
  // Ataque e Defesa (a rodada nova, depois da proposta recusada de "atributos"): a ficha e o Inventário (24) e o selo da
  // festa de atributo permanente (64), pelo mesmo caminho do jogo (Telas.celebrar com a mensagem "atributo")
  ataque_defesa: { pasta: "ataque_defesa/proposta", nomes: ["attr-ataque", "attr-defesa"], papel_tamanhos: [24, 32, 64],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario", "selo"] },
  // Agilidade e Poder (a rodada nova): a ficha e o Inventário (24), os selos (64) e o comando Fugir da luta (32: a
  // Agilidade é também a ação de fugir, ACAO.fuga)
  agilidade_poder: { pasta: "agilidade_poder/proposta", nomes: ["attr-agilidade", "attr-poder"], papel_tamanhos: [24, 32, 64],
    selos: [["agi", "Agilidade"], ["poder", "Poder"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "inventario", "selo", "luta"] },
  // a rodada das referências (agilidade_aljava_ref/): a bota nova de Agilidade (ficha 24, Fugir 32, selo 64) e a aljava
  // nova (topo 24, ficha 32, Inventário 40 e o saque com o 48 ao lado do 64)
  agilidade: { pasta: "agilidade_aljava_ref/proposta", saida: "agilidade_aljava_ref/capturas", nomes: ["attr-agilidade"],
    papel_tamanhos: [24, 32, 64], selos: [["agi", "Agilidade"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "selo", "luta"] },
  aljava_ref: { pasta: "agilidade_aljava_ref/proposta", saida: "agilidade_aljava_ref/capturas", nomes: ["aljava"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo", "ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "aljava", VESTIDO: "aljava" }] },
  // o Poder em avaliação (35262ca, agilidade_poder/): só ele trocado, ao lado de Ataque, Defesa e Agilidade do jogo
  poder: { pasta: "agilidade_poder/proposta", saida: "agilidade_poder/capturas", nomes: ["attr-poder"], papel_tamanhos: [24, 32, 64], selos: [["poder", "Poder"]],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["ficha", "selo"] },
  // a doca, rodada 2 (doca_r2/): dois atalhos por vez; agora o Inventário e o Mapa, também com a tela aberta
  doca_r2: { pasta: "doca_r2/proposta", saida: "doca_r2/capturas", nomes: ["atalho-inventario", "atalho-mapa"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "doca-inventario", "doca-mapa"] },
  // a doca, rodada 3 (doca_r3/): o Grimório e o Diário, também com a tela aberta; o Grimório é também o comando
  // Habilidades da roda da luta (ACAO.grimorio, 32), fotografado no tutorial
  doca_r3: { pasta: "doca_r3/proposta", saida: "doca_r3/capturas", nomes: ["atalho-grimorio", "atalho-diario"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "doca-grimorio", "doca-diario"] },
  doca_r3_luta: { pasta: "doca_r3/proposta", saida: "doca_r3/capturas", nomes: ["atalho-grimorio", "atalho-diario"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["luta"] },
  // a doca, rodada 4 (doca_r4/): a Comitiva (um papel novo, só nesta página) e os Talentos. No tutorial, com um
  // companheiro e pontos de talento (o selo ★ sobre os Talentos); na fogueira, com as telas abertas
  doca_r4: { pasta: "doca_r4/proposta", saida: "doca_r4/capturas", nomes: ["atalho-comitiva", "atalho-talentos"],
    papel_atalho: { rotulo: "Comitiva", peca: "atalho-comitiva", tamanhos: [32, 36] },
    cena: ["tutorial", { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", COMITIVA: "morel", PONTOS: "2" }], fotos: ["doca"] },
  doca_r4_telas: { pasta: "doca_r4/proposta", saida: "doca_r4/capturas", nomes: ["atalho-comitiva", "atalho-talentos"],
    papel_atalho: { rotulo: "Comitiva", peca: "atalho-comitiva", tamanhos: [32, 36] },
    cena: ["fogueira", { COMITIVA: "morel,odete" }], fotos: ["doca", "doca-comitiva", "doca-talentos"] },
  // a doca, rodada 5 (doca_r5/): o Bestiário, o Salvar e o Sair, na doca inteira (com companheiro e pontos de talento,
  // ao lado dos atalhos já aprovados); Salvar e Sair não são clicados (não mudam nada na foto)
  doca_r5: { pasta: "doca_r5/proposta", saida: "doca_r5/capturas", nomes: ["atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["tutorial", { TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", COMITIVA: "morel", PONTOS: "2" }], fotos: ["doca"] },
  doca_r5_telas: { pasta: "doca_r5/proposta", saida: "doca_r5/capturas", nomes: ["atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["fogueira", { COMITIVA: "morel,odete" }], fotos: ["doca", "doca-bestiario"] },
  doca: { pasta: "doca/proposta", nomes: ["atalho-talentos", "atalho-grimorio", "atalho-inventario", "atalho-mapa", "atalho-diario", "atalho-bestiario", "atalho-salvar", "atalho-sair"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["doca", "luta-doca"] },
  // Vida e Mana (o grupo Vida e recursos): o topo (20), o único uso; uma partida de Mago, que mostra as duas
  vida_mana: { pasta: "vida_mana/proposta", saida: "vida_mana/capturas", nomes: ["vital-vida", "vital-mana"],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo"] },
  // Vigor e Foco: o topo (20), o único uso; o Guerreiro mostra o Vigor, o Arqueiro, o Foco
  vigor_foco: { pasta: "vigor_foco/proposta", saida: "vigor_foco/capturas/guerreiro", nomes: ["vital-vigor", "vital-foco"],
    cena: ["capela", { CLASSE: "guerreiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo"] },
  vigor_foco_arqueiro: { pasta: "vigor_foco/proposta", saida: "vigor_foco/capturas/arqueiro", nomes: ["vital-vigor", "vital-foco"],
    cena: ["capela", { CLASSE: "arqueiro", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["topo"] },
  // Ouro e Provisões: o topo (24) e o mercado (as Provisões em 32, no cartão "Provisões (1 dia)")
  ouro_provisoes: { pasta: "ouro_provisoes/proposta", saida: "ouro_provisoes/capturas", nomes: ["moedas", "provisoes"], papel_tamanhos: [24, 32],
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["topo", "mercado"] },
  // a moeda avulsa (moeda_tocha/): os preços do mercado e de um serviço (16), o chip de ouro e as moedas que voam até o
  // topo (16), o espólio e o pagamento de contratos (32) e o prêmio dos cartazes do mural (16), com os mesmos dados nos
  // dois modos. A moeda não tem papel em
  // Icones (é o sprite 16×16 do jogo): só nesta página, o Sprites.img("moeda") serve o arquivo da proposta
  moeda: { pasta: "moeda_tocha/proposta", saida: "moeda_tocha/capturas/moeda", nomes: ["moeda"], papel_sprite: { moeda: [16, 32] },
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["precos", "servico", "chip-voo", "espolio", "contratos", "mural"] },
  // a tocha (moeda_tocha/): o topo (24), o cartão do mercado e a bolsa do Inventário (32); só esses tamanhos
  tocha: { pasta: "moeda_tocha/proposta", saida: "moeda_tocha/capturas/tocha", nomes: ["tocha"], papel_tamanhos: [24, 32],
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["topo", "mercado", "inventario"] },
  // as variantes da tocha (moeda_tocha/variantes/): o 16 (o sprite "tocha" em 16, só nesta página) no aviso flutuante
  // e no chip de um item ganho, e no risco "−1 tocha" da escolha que entra numa sala escura da capela, à noite
  tocha16: { pasta: "moeda_tocha/variantes/proposta", saida: "moeda_tocha/variantes/capturas/tocha16", nomes: ["tocha"], papel_sprite: { tocha: [16] },
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["aviso-tocha", "chip-tocha"] },
  tocha16_risco: { pasta: "moeda_tocha/variantes/proposta", saida: "moeda_tocha/variantes/capturas/tocha16", nomes: ["tocha"], papel_sprite: { tocha: [16] },
    cena: ["capela", { CLASSE: "guerreiro", NIVEL: "5", ETAPA: "capela", SALA: "exterior", PERIODO: "3", TOCHAS: "2" }], fotos: ["riscos"] },
  // a apagada: o topo sem tochas (24, o recurso só nesta página: hoje é o sprite em 32) e o risco "Sem luz" (16)
  tocha_apagada: { pasta: "moeda_tocha/variantes/proposta", saida: "moeda_tocha/variantes/capturas/apagada", nomes: ["tocha_apagada"],
    papel_sprite: { tocha_apagada: [16] }, papel_recurso: { tocha_apagada: [16, 24] },
    cena: ["capela", { CLASSE: "guerreiro", NIVEL: "5", ETAPA: "capela", SALA: "exterior", PERIODO: "3", TOCHAS: "0" }], fotos: ["topo", "riscos"] },
  // lote 1 (bandagem_pocao/): a Bandagem e a Poção de Vida. O topo (24), os cartões do mercado e a bolsa do Inventário
  // (32), o aviso e o chip de um item ganho (16, o sprite só nesta página); na luta, o comando Itens da roda (a poção, 32)
  bandagem_pocao: { pasta: "bandagem_pocao/proposta", saida: "bandagem_pocao/capturas", nomes: ["bandagem", "pocao"],
    papel_sprite: { bandagem: [16], pocao: [16] }, itens: [["pocao_vida", "+1 Poção de Vida"], ["bandagem", "+1 Bandagem"]],
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["topo", "mercado", "aviso-item", "chip-item", "inventario"] },
  bandagem_pocao_luta: { pasta: "bandagem_pocao/proposta", saida: "bandagem_pocao/capturas", nomes: ["bandagem", "pocao"],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7" }],
    fotos: ["luta"] },
  // lote 2 (tonico_antidoto/): o Tônico Restaurador e o Antídoto. Os cartões do mercado e o espólio (32), o aviso e o
  // chip de um item ganho (16: os sprites pocao_azul e folha, só nesta página; fora dela eles têm outros papéis)
  tonico_antidoto: { pasta: "tonico_antidoto/proposta", saida: "tonico_antidoto/capturas", nomes: ["tonico", "antidoto"],
    papel_sprite: { pocao_azul: { peca: "tonico", tamanhos: [16] }, folha: { peca: "antidoto", tamanhos: [16] } },
    itens: [["tonico", "+1 Tônico Restaurador"], ["antidoto", "+1 Antídoto"]],
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["mercado", "espolio-itens", "aviso-item", "chip-item"] },
  // lote 3 (calca_manto/): a Calça de Viagem (calca_tecido) e o Manto (manto) do Mago, sem papel em Icones hoje (o sprite
  // do jogo): os papéis só nesta página. A ficha (32) e o Inventário (40) do Mago vestindo as duas; o cartão do saque de
  // cada uma (64 e o 48 do "você usa")
  calca_manto: { pasta: "calca_manto/proposta", saida: "calca_manto/capturas", nomes: ["calca_tecido", "manto"],
    papeis: [{ item: "calca_tecido", tamanhos: [32, 40, 48, 64] }, { item: "manto", tamanhos: [32, 40, 48, 64] }],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior", VESTIR: "manto,calca_tecido" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "manto", VESTIDO: "manto" }] },
  calca_manto_saque_calca: { pasta: "calca_manto/proposta", saida: "calca_manto/capturas/saque_calca", nomes: ["calca_tecido", "manto"],
    papeis: [{ item: "calca_tecido", tamanhos: [32, 40, 48, 64] }, { item: "manto", tamanhos: [32, 40, 48, 64] }],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: [],
    saque: ["vila", { CLASSE: "mago", ACHADO: "calca_tecido", VESTIDO: "calca_tecido" }] },
  // o frasco vazio (bandagem_pocao/variantes/): o topo sem poções (24, o recurso só nesta página; hoje o sprite em 32)
  // e, para comparar, o topo com poções (a Poção de Vida do jogo, SO_ATUAL)
  // o Antídoto com a base plana (tonico_antidoto/): antes (PASTA=tonico_antidoto/recusados/antidoto-base-redonda, ROTULO=antes)
  // e depois (ROTULO=depois), os dois com SO_PROPOSTA=1, nos mesmos lugares da proposta
  antidoto_base: { pasta: "tonico_antidoto/proposta", saida: "tonico_antidoto/capturas/base", nomes: ["antidoto"],
    papel_sprite: { folha: { peca: "antidoto", tamanhos: [16] } }, itens: [["antidoto", "+1 Antídoto"]],
    cena: ["mercado", { CLASSE: "guerreiro" }], fotos: ["mercado", "espolio-itens", "aviso-item", "chip-item"] },
  // o anel e o amuleto (anel_amuleto/): a ficha (32) e o Inventário (40) do Mago, com um anel vestido e o outro espaço
  // vazio (a silhueta do vazio é o mesmo arquivo, apagado); o saque de cada um (64 e o 48 do "você usa")
  anel_amuleto: { pasta: "anel_amuleto/proposta", saida: "anel_amuleto/capturas", nomes: ["anel", "amuleto"],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "anel", VESTIDO: "anel" }] },
  anel_amuleto_saque_amuleto: { pasta: "anel_amuleto/proposta", saida: "anel_amuleto/capturas/saque_amuleto", nomes: ["anel", "amuleto"],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: [],
    saque: ["vila", { CLASSE: "mago", ACHADO: "amuleto", VESTIDO: "amuleto" }] },
  // a Sandália e o Chapéu Pontudo do Mago (sandalia_chapeu/), sem papel em Icones hoje (o sprite do jogo): os papéis só
  // nesta página. A ficha (32) e o Inventário (40) do Mago vestindo os dois, com o manto, a calça e a luva de seda
  // aprovados (no tutorial, que veste por VESTIR; a capela não veste); o cartão do saque de cada um (64 e o 48 do "você usa")
  sandalia_chapeu: { pasta: "sandalia_chapeu/proposta", saida: "sandalia_chapeu/capturas", nomes: ["sandalia", "chapeu"],
    papeis: [{ item: "sandalia", tamanhos: [32, 40, 48, 64] }, { item: "chapeu", tamanhos: [32, 40, 48, 64] }],
    cena: ["tutorial", { CLASSE: "mago", TUTORIAL: "0", PERIODO: "0", VESTIR: "chapeu,manto,calca_tecido,sandalia,luva_seda" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "sandalia", VESTIDO: "sandalia" }] },
  sandalia_chapeu_saque_chapeu: { pasta: "sandalia_chapeu/proposta", saida: "sandalia_chapeu/capturas/saque_chapeu", nomes: ["sandalia", "chapeu"],
    papeis: [{ item: "sandalia", tamanhos: [32, 40, 48, 64] }, { item: "chapeu", tamanhos: [32, 40, 48, 64] }],
    cena: ["capela", { CLASSE: "mago", NIVEL: "5", PERIODO: "0", SALA: "exterior" }], fotos: [],
    saque: ["vila", { CLASSE: "mago", ACHADO: "chapeu", VESTIDO: "chapeu" }] },
  // o Chapéu Pontudo no jogo (1.141.0): com SO_ATUAL=1, os arquivos reais na ficha, no Inventário e no saque
  chapeu_no_jogo: { pasta: "sandalia_chapeu/proposta", saida: "sandalia_chapeu/capturas/integracao", nomes: ["chapeu"],
    cena: ["tutorial", { CLASSE: "mago", TUTORIAL: "0", PERIODO: "0", VESTIR: "chapeu,manto,calca_tecido,sandalia,luva_seda" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "chapeu", VESTIDO: "chapeu" }] },
  // a Sandália, rodada 2 (o par em três quartos, pela referência ferramentas/arte/referencias/botas/): o papel só nesta
  // página (o chapéu já está no jogo). Atual (SO_ATUAL), rodada 1 (PASTA=sandalia_chapeu/rodada1/proposta
  // ROTULO=rodada1 SO_PROPOSTA=1) e rodada 2 (ROTULO=rodada2 SO_PROPOSTA=1), com os mesmos dados
  sandalia_r2: { pasta: "sandalia_chapeu/rodada2/proposta", saida: "sandalia_chapeu/capturas/r2", nomes: ["sandalia", "chapeu"],
    papeis: [{ item: "sandalia", tamanhos: [32, 40, 48, 64] }],
    cena: ["tutorial", { CLASSE: "mago", TUTORIAL: "0", PERIODO: "0", VESTIR: "chapeu,manto,calca_tecido,sandalia,luva_seda" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "sandalia", VESTIDO: "sandalia" }] },
  // a Besta Leve e o Diadema (besta_diadema/), sem papel em Icones hoje (o sprite do jogo): os papéis só nesta página (o
  // Diadema é o desenho "coroa" nos dados; o arquivo, "diadema"). A besta: o Arqueiro com ela na mão (ARMA, no
  // tutorial), a ficha (32), o Inventário (40) e o saque (64 e 48). O diadema: o Mago com ele na cabeça, a ficha, o
  // Inventário e o saque; e o cartão da Coroa dos Afogados (o único, base Diadema), com o mesmo desenho
  besta: { pasta: "besta_diadema/proposta", saida: "besta_diadema/capturas/besta", nomes: ["besta", "diadema"],
    papeis: [{ item: "besta", tamanhos: [32, 40, 48, 64] }, { item: "coroa", peca: "diadema", tamanhos: [32, 40, 48, 64] }],
    cena: ["tutorial", { CLASSE: "arqueiro", TUTORIAL: "0", PERIODO: "0", ARMA: "besta" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "arqueiro", ACHADO: "besta", VESTIDO: "besta" }] },
  // o Diadema, rodada 2 (a besta já no jogo, 1.143.0): antes (PASTA=besta_diadema/diadema_r1/proposta ROTULO=antes
  // SO_PROPOSTA=1) e depois (ROTULO=depois SO_PROPOSTA=1), com os mesmos dados
  diadema: { pasta: "besta_diadema/proposta", saida: "besta_diadema/capturas/diadema", nomes: ["besta", "diadema"],
    papeis: [{ item: "coroa", peca: "diadema", tamanhos: [32, 40, 48, 64] }],
    cena: ["tutorial", { CLASSE: "mago", TUTORIAL: "0", PERIODO: "0", VESTIR: "coroa,manto,calca_tecido,sandalia,luva_seda" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "mago", ACHADO: "coroa", VESTIDO: "coroa" }] },
  coroa_afogados: { pasta: "besta_diadema/proposta", saida: "besta_diadema/capturas/coroa_afogados", nomes: ["besta", "diadema"],
    papeis: [{ item: "coroa", peca: "diadema", tamanhos: [32, 40, 48, 64] }],
    cena: ["tutorial", { CLASSE: "mago", TUTORIAL: "0" }], fotos: [],
    saque: ["vila", { CLASSE: "mago", ACHADO_ID: "coroa_dos_afogados", VESTIDO: "coroa" }] },
  // a espada e a maça (espada_maca/, o começo do remake do ferro): só o 32 e o 64 (= 32 x2) na proposta, então os
  // tamanhos ficam [32, 64] nesta página (o 40 do Inventário e o 48 do "você usa" mostram o mais perto, como o jogo faz
  // com um tamanho sem arquivo). A espada: o Guerreiro com ela na mão (ARMA, no tutorial), a ficha, o Inventário, o
  // saque e a roda da luta (o Atacar do Guerreiro é o desenho "espada"); a maça: a ficha, o Inventário e o saque.
  // Rodada 2 (a vigente: ROTULO=rodada2) e rodada 1 (PASTA=espada_maca/rodada1/proposta ROTULO=rodada1 SO_PROPOSTA=1)
  espada: { pasta: "espada_maca/proposta", saida: "espada_maca/capturas/espada", nomes: ["espada", "maca"], papel_tamanhos: [32, 64],
    cena: ["tutorial", { CLASSE: "guerreiro", TUTORIAL: "0", PERIODO: "0", ARMA: "espada" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "guerreiro", ACHADO: "espada", VESTIDO: "espada" }] },
  espada_luta: { pasta: "espada_maca/proposta", saida: "espada_maca/capturas/espada", nomes: ["espada", "maca"], papel_tamanhos: [32, 64],
    cena: ["tutorial", { LUTA_APOS_ESCOLHA: "1", TUTORIAL: "0", VISTAS, CLASSE: "guerreiro", NIVEL: "8", ESPEC: "paladino", COMITIVA: "morel", LUTA: "lobo", QUANTOS: "3", NIVEL_LUTA: "7", ARMA: "espada" }],
    fotos: ["luta"] },
  maca: { pasta: "espada_maca/proposta", saida: "espada_maca/capturas/maca", nomes: ["espada", "maca"], papel_tamanhos: [32, 64],
    cena: ["tutorial", { CLASSE: "guerreiro", TUTORIAL: "0", PERIODO: "0", ARMA: "maca" }], fotos: ["ficha", "inventario"],
    saque: ["vila", { CLASSE: "guerreiro", ACHADO: "maca", VESTIDO: "maca" }] },
  frasco_vazio: { pasta: "bandagem_pocao/variantes/proposta", saida: "bandagem_pocao/variantes/capturas/vazia", nomes: ["frasco_vazio"],
    papel_recurso: { frasco_vazio: [24] }, cena: ["covil", { LUGAR: "vila", BOLSA: "pocao_vida=0" }], fotos: ["topo"] },
  frasco_cheio: { pasta: "bandagem_pocao/variantes/proposta", saida: "bandagem_pocao/variantes/capturas/cheia", nomes: ["frasco_vazio"],
    cena: ["covil", { LUGAR: "vila", BOLSA: "pocao_vida=2" }], fotos: ["topo"] },
};
const P = PECAS[peca];
if (!P) throw new Error(`peça desconhecida: ${peca}`);
// PASTA=<pasta relativa> troca a proposta (aljava/rodada4: a anterior); ROTULO=<nome> no lugar de "proposta" nas fotos
const PROPOSTA = path.join(aqui, process.env.PASTA || P.pasta), SAIDA = path.join(aqui, P.saida || path.join(peca, "capturas"));
const ROTULO = process.env.ROTULO || "proposta";
mkdirSync(SAIDA, { recursive: true });

async function anexar(p) {
  await p.route(/\/static\/hud\/icones\/([a-z_-]+)-(\d+)(@2x)?\.png/, async (r) => {
    const nome = decodeURIComponent(new URL(r.request().url()).pathname.split("/").pop());
    const base = nome.replace(/-\d+(@2x)?\.png$/, "");
    const arquivo = path.join(PROPOSTA, nome);
    if (P.nomes.includes(base) && existsSync(arquivo)) return r.fulfill({ body: readFileSync(arquivo), contentType: "image/png" });
    return r.continue();
  });
  if (P.papel_tamanhos) {   // os tamanhos novos de um desenho que já tem papel (o 64 do selo)
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      for (const n of P.nomes) { const i = js.indexOf(`"${n}": [`), j = js.indexOf("]", i); if (i >= 0) js = js.slice(0, i) + `"${n}": ${JSON.stringify(P.papel_tamanhos)}` + js.slice(j + 1); }
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel_recurso) {  // um recurso do topo que ainda não tem desenho (a tocha apagada): o papel só nesta página
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      for (const [nome, tamanhos] of Object.entries(P.papel_recurso)) {
        js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${nome}": ${JSON.stringify(tamanhos)}, `);
        js = js.replace('const RECURSO = {', `const RECURSO = { ${nome}: "${nome}", `);
      }
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel_atalho) {   // um atalho que ainda não tem desenho próprio no jogo (a Comitiva): o papel só nesta página
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      const { rotulo, peca: nome, tamanhos } = P.papel_atalho;
      js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${nome}": ${JSON.stringify(tamanhos)}, `);
      js = js.replace('const ATALHO = {', `const ATALHO = { "${rotulo}": "${nome}", `);
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel_sprite) {   // sprites do jogo sem papel em Icones ({sprite: tamanhos} ou {sprite: {peca, tamanhos}}, quando o
    // arquivo tem outro nome): só nesta página, o desenho da proposta nos tamanhos que ela tem; nos outros, o sprite
    await p.route(/\/static\/sprites\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      const js = (await res.text()) + `
;(() => { const orig = Sprites.img, T = ${JSON.stringify(P.papel_sprite)};
  Sprites.img = (nome, escala = 2, classe = "", o = {}) => {
    const lado = 16 * escala, d = T[nome];
    const peca = d && !Array.isArray(d) ? d.peca : nome, tam = d && (Array.isArray(d) ? d : d.tamanhos);
    if (!d || !tam.includes(lado)) return orig(nome, escala, classe, o);
    const t = lado, f = "/static/hud/icones/" + peca + "-" + t;
    return '<img class="sprite desenho ' + classe + '" src="' + f + '.png" srcset="' + f + '@2x.png 2x" width="' + lado + '" height="' + lado + '" style="--s:' + lado + '" alt="" draggable="false">';
  }; })();`;
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papeis) {  // várias peças sem papel em Icones (a calça de tecido e o manto): os papéis só nesta página
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      for (const { item, peca: arq = item, tamanhos } of P.papeis) {   // peca: o arquivo, quando não é o nome do desenho
        js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${arq}": ${JSON.stringify(tamanhos)}, `);
        js = js.replace('const ITEM = {', `const ITEM = { ${item}: "${arq}", `);
      }
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
  if (P.papel) {
    await p.route(/\/static\/icones\.js(\?|$)/, async (r) => {
      const res = await r.fetch();
      let js = await res.text();
      js = js.replace('const TAMANHOS = {', `const TAMANHOS = {"${P.papel.item}": ${JSON.stringify(P.papel.tamanhos)}, `);
      js = js.replace('const ITEM = {', `const ITEM = { ${P.papel.item}: "${P.papel.item}", `);
      r.fulfill({ response: res, body: js, headers: { ...res.headers(), "content-type": "application/javascript" } });
    });
  }
}
async function subir() {
  const [cenario, amb] = P.cena;
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null;
  proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  if (!url) throw new Error("o cenário não subiu");
  return { proc, url };
}

const b = await chromium.launch();
const rel = [];
// SO_ATUAL=1: só o jogo como está (sem trocar arquivo nenhum), para conferir uma integração
for (const modo of (process.env.SO_ATUAL ? ["atual"] : process.env.SO_PROPOSTA ? [ROTULO] : ["atual", ROTULO])) for (const [W, H] of JANELAS) {
  const { proc, url } = await subir();
  try {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo !== "atual") await anexar(p);
    await p.goto(url); await p.waitForFunction(() => !processando && pergunta, null, { timeout: 30000 }); await espera(1200);
    const nome = (f) => path.join(SAIDA, `${modo}-${W}x${H}-${f}.png`);
    const clipDe = async (sel, m = 8) => { const bb = await (await p.$(sel)).boundingBox(); return { x: Math.max(0, bb.x - m), y: Math.max(0, bb.y - m), width: bb.width + 2 * m, height: bb.height + 2 * m }; };
    // o que os desenhos da peça carregaram (o arquivo e o tamanho na tela)
    const desenhos = async () => p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
      .map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}px`), P.nomes);
    const visto = new Set();
    for (const f of P.fotos) {
      if (f === "ficha") { await p.screenshot({ path: nome("ficha"), clip: await clipDe("#heroi", 0) }); }
      if (f === "topo") { await p.screenshot({ path: nome("topo"), clip: await clipDe("#hud", 0) }); }
      // o mercado: a tela inteira e um recorte em volta de cada desenho da peça fora do topo (o cartão onde ele está)
      if (f === "mercado") {
        await p.screenshot({ path: nome("mercado") });
        const caixas = await p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => !i.closest("#hud") && nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
          .map((i) => { const c = (i.closest(".slot, .carta-loja, .item-loja, li, .cartao") || i).getBoundingClientRect(); return { x: c.x, y: c.y, width: c.width, height: c.height }; }), P.nomes);
        for (const [k, c] of caixas.entries()) await p.screenshot({ path: nome(`mercado-${k}`), clip: { x: Math.max(0, c.x - 12), y: Math.max(0, c.y - 12), width: c.width + 24, height: c.height + 24 } });
      }
      if (f === "selo") {
        for (const [stat, nomeAttr] of (P.selos || [["atk", "Ataque"], ["defesa", "Defesa"]])) {
          await p.evaluate(([st, nm]) => { Telas.celebrar({ tipo: "atributo", dados: { stat: st, nome: nm, valor: 2, total: 27 } }, false); }, [stat, nomeAttr]);
          await espera(350);
          const sel = await p.$(".selo-atributo");
          if (sel) { const bb = await sel.boundingBox(); await p.screenshot({ path: nome(`selo-${stat}`), clip: { x: bb.x - 10, y: bb.y - 10, width: bb.width + 20, height: bb.height + 20 } }); }
          (await desenhos()).forEach((d) => visto.add(d));
          await espera(2600);
        }
      }
      if (f === "doca") { await p.screenshot({ path: nome("doca"), clip: await clipDe("#doca", 0) }); }
      // a moeda: a união das caixas de um seletor, para recortar os cartões
      const uniao = (sel, n = 8) => p.evaluate(([s, n]) => {
        const cs = [...document.querySelectorAll(s)].slice(0, n).map((e) => e.getBoundingClientRect()).filter((r) => r.width);
        const x = Math.min(...cs.map((r) => r.left)), y = Math.min(...cs.map((r) => r.top));
        return { x: x - 6, y: y - 6, width: Math.max(...cs.map((r) => r.right)) - x + 12, height: Math.max(...cs.map((r) => r.bottom)) - y + 12 };
      }, [sel, n]);
      if (f === "precos") {   // os preços dos cartões do mercado
        await p.screenshot({ path: nome("precos") });
        await p.screenshot({ path: nome("precos-cartoes"), clip: await uniao(".mercadoria") });
      }
      if (f === "servico") {  // o preço dos cartões do ferreiro
        await p.keyboard.press("Escape");
        await (await p.waitForSelector('#predios .predio[data-predio="ferreiro"]', { timeout: 8000 })).click();
        await p.waitForSelector(".servico", { timeout: 8000 }); await espera(1000);
        await p.screenshot({ path: nome("servico") });
        await p.screenshot({ path: nome("servico-cartoes"), clip: await uniao(".servico") });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(800);
        if (!(await p.$('#predios:not(.focado) .predio[data-predio="mercado"]'))) { await p.keyboard.press("Escape"); await espera(800); }
      }
      if (f === "chip-voo") { // o chip de ouro no texto e as moedas que voam dele até o ouro do topo (a animação do jogo)
        await p.evaluate(() => { efeito({ tipo: "ouro", texto: "+25 de ouro" }); });
        await espera(150); await p.screenshot({ path: nome("voo-1") });
        await espera(150); await p.screenshot({ path: nome("voo-2") });
        await espera(1500);
        await p.screenshot({ path: nome("chip"), clip: await clipDe("#texto .chip.ouro", 10) });
      }
      if (f === "espolio") {  // o espólio de uma luta, com ouro e experiência
        p.evaluate(() => { Telas.celebrar({ tipo: "espolio", dados: { ouro: 37, xp: 24, nivel: 3, trechos: [[10, 34, 60]] } }, false); });
        await espera(3500);
        await p.screenshot({ path: nome("espolio"), clip: await clipDe("#celebracao .festa-espolio", 10) });
        (await desenhos()).forEach((d) => visto.add(d));
        const c = await p.$("#celebracao .continuar"); if (c) await c.click();
        await espera(1200);
      }
      if (f === "contratos") { // o pagamento de um contrato e, ao receber, as moedas voando até o topo
        p.evaluate(() => { Telas.celebrar({ tipo: "contratos", dados: { ouro: 45, xp: 30, reputacao: 3, contratos: [{ id: 1, tipo: "caca",
          desc: "Eliminar 4 Lobos em Bosque do Lobo Branco", lugar: "Bosque do Lobo Branco", lugar_tipo: "floresta", bioma: "floresta", ouro: 45, xp: 30, nivel: 2 }] } }, false); });
        await espera(3000);
        await p.screenshot({ path: nome("contratos"), clip: await clipDe("#celebracao .festa-contratos", 10) });
        (await desenhos()).forEach((d) => visto.add(d));
        const c = await p.$("#celebracao .continuar"); if (c) { await c.click(); await espera(160); await p.screenshot({ path: nome("contratos-voo") }); }
        await espera(1500);
      }
      if (f === "aviso-tocha") {   // numa tela (o mercado), um item ganho vira o aviso flutuante perto do último clique
        await p.mouse.click(1100, 700); await espera(300);
        await p.evaluate(() => { efeito({ tipo: "item", texto: "+1 Tocha", item: "tocha" }); });
        await espera(400);
        await p.screenshot({ path: nome("aviso"), clip: await clipDe(".aviso-flutuante", 12) });
        (await desenhos()).forEach((d) => visto.add(d));
        await espera(1800);
      }
      if (f === "chip-tocha") {    // na vila, o chip no texto (o ícone dele; a tocha que voa é a de 32, já no jogo)
        await p.keyboard.press("Escape"); await p.waitForSelector('#predios:not(.focado) .predio[data-predio="mercado"]', { timeout: 8000 }); await espera(800);
        await p.evaluate(() => { efeito({ tipo: "item", texto: "+1 Tocha", item: "tocha" }); });
        await espera(1500);
        await p.screenshot({ path: nome("chip"), clip: await clipDe("#texto .chip.item", 10) });
        (await desenhos()).forEach((d) => visto.add(d));
      }
      if (f === "espolio-itens") {  // o espólio com os itens achados (32)
        p.evaluate((itens) => { Telas.celebrar({ tipo: "espolio", dados: { itens: itens.map(([id, t]) => ({ id, nome: t.replace(/^\+1 /, ""), qtd: 1 })) } }, false); }, P.itens);
        await espera(3000);
        await p.screenshot({ path: nome("espolio"), clip: await clipDe("#celebracao .festa-espolio", 10) });
        (await desenhos()).forEach((d) => visto.add(d));
        const c = await p.$("#celebracao .continuar"); if (c) await c.click();
        await espera(1200);
      }
      if (f === "aviso-item") {   // numa tela (o mercado), cada item ganho vira o aviso flutuante perto do clique
        for (const [id, texto] of P.itens) {
          await p.mouse.click(1100, 700); await espera(300);
          await p.evaluate(([i, t]) => { efeito({ tipo: "item", texto: t, item: i }); }, [id, texto]);
          await espera(400);
          await p.screenshot({ path: nome(`aviso-${id}`), clip: await clipDe(".aviso-flutuante", 12) });
          (await desenhos()).forEach((d) => visto.add(d));
          await espera(2000);
        }
      }
      if (f === "chip-item") {    // na vila, o chip de cada item ganho no texto (16)
        if (await p.$(".tela.loja")) { await p.keyboard.press("Escape"); await p.waitForSelector('#predios:not(.focado) .predio[data-predio="mercado"]', { timeout: 8000 }); await espera(800); }
        for (const [id, texto] of P.itens) {
          await p.evaluate(([i, t]) => { efeito({ tipo: "item", texto: t, item: i }); }, [id, texto]);
          await espera(1500);
        }
        await p.screenshot({ path: nome("chips"), clip: await clipDe("#texto .chips:last-of-type", 10) });
        (await desenhos()).forEach((d) => visto.add(d));
      }
      if (f === "riscos") {        // os riscos da escolha que entra na sala escura (a tocha que ela gasta, ou sem luz)
        await p.screenshot({ path: nome("riscos"), clip: await clipDe("#prompt .escolha:has(.op-riscos)", 10) });
        await p.screenshot({ path: nome("pagina") });
      }
      if (f === "mural") {    // o prêmio nos cartazes do mural (o prédio da vila)
        await (await p.waitForSelector('#predios .predio[data-predio="mural"]', { timeout: 8000 })).click();
        await p.waitForSelector("[data-aceitar]", { timeout: 10000 }); await p.mouse.move(4, 400); await espera(800);
        await p.screenshot({ path: nome("mural") });
        await p.screenshot({ path: nome("mural-cartazes"), clip: await uniao(".mural .contrato", 3) });
      }
      // a doca com a tela do atalho aberta (o estado selecionado, .atual): "doca-inventario", "doca-mapa"
      if (f.startsWith("doca-")) {
        const rotulo = { inventario: "Inventário", mapa: "Mapa", grimorio: "Grimório", diario: "Diário", comitiva: "Comitiva", talentos: "Talentos", bestiario: "Bestiário" }[f.slice(5)];
        await p.evaluate((r) => pedirAtalho(r), rotulo); await espera(900);
        await p.screenshot({ path: nome(f), clip: await clipDe("#doca", 0) });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(500);
      }
      if (f === "inventario") {
        if (await p.$(".tela.loja")) { await p.keyboard.press("Escape"); await espera(900); }   // do mercado, sai antes
        await p.evaluate(() => pedirAtalho("Inventário")); await espera(900);
        await p.screenshot({ path: nome("inventario"), clip: await clipDe("#palco", 0) });
        (await desenhos()).forEach((d) => visto.add(d));
        await p.keyboard.press("Escape"); await espera(500);
      }
      if (f === "luta" || f === "luta-doca") {
        const comecar = await p.$('#prompt .escolha:has-text("Começar a luta")');
        if (comecar) {
          await comecar.click();
          await p.waitForFunction(() => document.querySelector('#roda .roda-botao[data-slot="atacar"]') && !processando, null, { timeout: 30000 }); await espera(1200);
          await p.screenshot({ path: nome("luta"), clip: await clipDe("#palco", 0) });
          if (f === "luta") { await p.screenshot({ path: nome("luta-ficha"), clip: await clipDe("#heroi", 0) }); }
        }
      }
      (await desenhos()).forEach((d) => visto.add(d));
    }
    rel.push({ modo, janela: `${W}x${H}`, desenhos: [...visto].sort(), erros });
    await p.close();
  } finally { proc.kill(); }
}
// o cartão do saque (64 e 48: o achado e o "você usa") e o voo ao equipar, quando a peça tem cena de saque
if (P.saque) for (const modo of (process.env.SO_ATUAL ? ["atual"] : process.env.SO_PROPOSTA ? [ROTULO] : ["atual", ROTULO])) for (const [W, H] of JANELAS) {
  const [cenario, amb] = P.saque;
  const proc = spawn(PY, ["-m", "tests.navegador.cenarios", cenario], { cwd: raiz, env: { ...process.env, PYTHONPATH: raiz, PYTHONIOENCODING: "utf-8", VELOCIDADE: "rapido", ...amb } });
  let url = null; proc.stdout.on("data", (d) => { const m = String(d).match(/http:\S+/); if (m) url = m[0]; });
  for (let k = 0; k < 300 && !url; k++) await espera(100);
  try {
    const p = await b.newPage({ viewport: { width: W, height: H } });
    const erros = []; p.on("pageerror", (e) => erros.push(String(e)));
    if (modo !== "atual") await anexar(p);
    await p.goto(url);
    await p.waitForSelector(".janela-achado", { timeout: 30000 }); await espera(2500);
    const bb = await (await p.$(".janela-achado")).boundingBox();
    await p.screenshot({ path: path.join(SAIDA, `${modo}-${W}x${H}-saque.png`), clip: { x: bb.x - 6, y: bb.y - 6, width: bb.width + 12, height: bb.height + 12 } });
    const desenhos = await p.evaluate((nomes) => [...document.querySelectorAll("img")].filter((i) => nomes.some((n) => (i.currentSrc || i.src).includes(`/${n}-`)))
      .map((i) => `${(i.currentSrc || i.src).split("/").pop()} ${Math.round(i.getBoundingClientRect().width)}px`), P.nomes);
    rel.push({ modo, janela: `${W}x${H}`, saque: [...new Set(desenhos)].sort(), erros });
    await p.close();
  } finally { proc.kill(); }
}
await b.close();
for (const r of rel) console.log(JSON.stringify(r));
