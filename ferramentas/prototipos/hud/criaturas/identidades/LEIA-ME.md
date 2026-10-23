# Identidades pendentes: o guardião do brejo, o antagonista e o `esqueleto_servo` (23/10/2026; só texto, nada no jogo)

**Pedido do Jean:** antes de qualquer desenho, (1) desenvolver o Barqueiro do Charco como substituto da Bruxa Afogada nos
covis e medir o escopo de separar a Ilse da campanha do guardião do covil; (2) levantar o que o jogo estabelece sobre o
antagonista do mundo gerado e propor três direções visuais; (3) investigar a família `esqueleto_servo` e recomendar
manter, remover ou reaproveitar. Nada desenhado, nenhuma mudança de produção, de save ou de mapa. Tudo conferido no
código da 1.199.0. O levantamento anterior da Bruxa (o uso duplo da ficha, os três conceitos) fica em
`../chefes_e_especiais/LEIA-ME.md`; aqui está o passo seguinte.

## 1. O Barqueiro do Charco (proposta; as regras de hoje preservadas)

**O que não muda:** a ficha inteira em números e regras: 110 de vida, ataque 6, defesa 3, agilidade 6, poder 12;
`morto-vivo` e `conjurador`; Maldição, Bola de Sombra, Invocar (`invoca="afogado"`), Drenar; `ataque="sombra"`; a fase a
50% (poder ×1,3, mais o Grito de Terror). As mensagens das habilidades são as genéricas do combate (as mesmas de qualquer
inimigo) e continuam; a identidade só entra na `base`, no `g`, na `intro`, no texto da fase, no rumor e no retrato.

- **Natureza:** o barqueiro que atravessava gente pelo brejo, quando havia estrada do outro lado. Afundou com o barco e
  não parou de trabalhar: agora atravessa os afogados, que não têm cova nem quem pague a travessia. Não é vítima de
  ninguém, não tem história com a vila nem com a Igreja, não canta. É um ofício que continuou depois da morte. O texto de
  ambiente do pântano já prepara isso ("Luzes pálidas dançam sobre a água parada. Os afogados também se lembram de
  casa."): a luz é a lanterna dele.
- **Aparência:** um homem velho, alto e magro, encharcado. **O rosto, parcialmente encoberto:** um pano de rede de pesca
  e trapo enrolado no pescoço e subindo até o nariz, pesado de água; um gorro de pano molhado e colado à cabeça, sem aba
  (o chapéu de aba é do Espantalho). Ficam à vista a testa vincada, as sobrancelhas pesadas, os olhos claros e aguados,
  fixos, sem piscar, e o nariz comprido. A pele cinza-esverdeada, inchada da água. **A lanterna:** pequena, de ferro,
  com uma chama verde-pálida; é a única luz forte do quadro e ilumina o rosto de baixo (o nariz, as maçãs e as
  sobrancelhas acesos; as órbitas fundas). A vara do barco fica para a cena futura (o barco de fundo chato, a vara, a
  água parada), não para o retrato.
- **A expressão:** cansada, paciente, inexpressiva no começo (olha o herói como um passageiro), nada de careta nem de
  boca aberta. É o olhar que carrega o retrato.
- **Comportamento:** calado. Bate a vara na água em vez de falar. Trata o herói como passageiro que deve a travessia: a
  Maldição é marcar quem deve, o Drenar é cobrar, o Invocar chama os passageiros que ele já leva (os afogados, a família
  que já tem retrato e lore), a Bola de Sombra sai da lanterna.
- **A entrada na luta** (a `intro`, lida pelo `sistemas/chefes.py` só no covil): "Uma lanterna verde atravessa a névoa
  sobre o charco. De pé num barco de fundo chato, um velho encharcado apoia-se na vara e olha para você como quem espera
  o pagamento."
- **A segunda fase** (o texto da fase; as regras dela continuam): "O barqueiro abre a lanterna. A luz verde se espalha
  pela água, e os afogados sobem pela borda!" (os afogados já vinham pelo Invocar; a fase só torna isso uma cena.)
- **O rumor** (`sinais_do_guardiao`, pela `base` nova): "Uma lanterna verde atravessa o charco à noite, sem barulho de
  remo."
- **Nome e artigo:** `base="Barqueiro do Charco"`, `g="m"`: "Irdor, o Barqueiro do Charco".
- **Distância dos vizinhos:** da **Ilse** (mulher, flutua, canta, cabelos de algas, pele azulada, vítima da vila): homem,
  de pé, calado, coberto, a luz verde. Do **Lich Menor** (crânio, coroa, violeta): carne inchada, sem coroa, a cor é o
  verde da lanterna. Do **Profeta das Cinzas** (os olhos vendados, cinza e brasa, cântico): o contrário dele, os olhos à
  mostra e a boca coberta. Da **Hidra** (fera): humano. Do **Espantalho**: sem chapéu de aba.
- **Para 32→16:** o que precisa sobreviver é o par de olhos claros sob as sobrancelhas acesas e a mancha verde da
  lanterna embaixo; a rede vira dois ou três nós no pano, e o gorro, uma faixa. Risco: o pano até o nariz pode ler como
  máscara de bandido; a pele cinza-esverdeada e a luz de baixo é o que separa.

### O escopo de separar a Ilse do guardião do covil (para a entrega futura; nada feito)

Hoje a ficha `bruxa_afogada` (`GUARDIOES["pantano"][1]`) serve aos dois: o covil a sorteia, e a missão da capela monta o
`spec` dela (`missoes.py`, `id="bruxa_afogada"`, `idx=1`, `chave="ilse"`). O que a investigação conferiu e o que a
mudança pede:

1. **A ficha do covil:** a entrada `bruxa_afogada` da lista do pântano dá lugar, **na mesma posição**, a
   `barqueiro_do_charco` com os mesmos números, habilidades, `invoca` e `ataque`, e os textos acima. A lista continua com
   dois sorteáveis, então o `rng.randrange(len(GUARDIOES["pantano"]))` de `inimigos.gerar_guardiao` não muda e os mundos
   saem iguais; o gabarito só mudaria se uma das 24 partidas mostrasse o nome ou a intro do guardião do pântano (o
   levantamento anterior não achou a Bruxa em nenhuma; conferir com `--mostrar`).
2. **A ficha da Ilse:** sai do sorteio e vai para um catálogo à parte de guardiões únicos (a campanha monta o `spec` na
   hora, não o grava). `ficha_guardiao` procura por id e, sem achar, cai no `idx`: com a Bruxa fora da lista, o `idx=1`
   do `spec` da Ilse apontaria para o Barqueiro. Ou `ficha_guardiao` consulta os únicos primeiro, ou o `spec` da Ilse
   deixa de ter `idx`. O `idx` dos saves de antes do id, no covil do pântano, passa a dar no Barqueiro, o que é o certo
   (eram covis).
3. **Os textos compartilhados:** a `intro` da ficha só é lida pelo covil (`sistemas/chefes.py`; a capela narra a cena
   dela); vira a do Barqueiro. O texto da fase ("O canto vira um grito. Mãos podres emergem...") é lido pelos dois
   (`Combate.checar_fase`): a Ilse fica com o dela, o Barqueiro ganha o novo. O rumor de `sinais_do_guardiao` ganha a
   chave "Barqueiro do Charco" (a de "Bruxa Afogada" pode sair depois da migração). O exemplo de `texto.py` é só
   docstring. `tests/replay.py` traduz "Drowned Witch" de runs antigas e pode ficar.
4. **A migração de save (v6→v7):** os covis do mundo gerado com `id="bruxa_afogada"` passam a `barqueiro_do_charco`, com
   o `base`, o `g` e o nome com o artigo refeitos ("Irdor, a Bruxa Afogada" → "Irdor, o Barqueiro do Charco") e os
   rumores guardados que citam o nome antigo, como a `_v5_para_v6` das árvores já faz (aquela refaz pelo catálogo; esta
   precisa trocar o id antes). Vencidos ou não: o `derrotado` fica, o Sigilo guarda o bioma, as lendas guardam o
   antagonista. A campanha não precisa de migração (a missão não guarda a ficha). Sem a migração, um covil antigo cairia
   na ficha da Ilse se ela continuasse achável pelo id: as regras iguais, mas a intro e o nome errados.
5. **O retrato:** `RETRATO_GUARDIAO["barqueiro_do_charco"]`, quando houver desenho; a Ilse continua pela chave `ilse`
   (`RETRATO_CHAVE`, antes do id). Hoje o covil da Bruxa sai na `caveira` (pelos traços).
6. **Os testes:** os da Ilse (`test_guardia.py`, `broquel.py`, `test_cenas_capela.py`) continuam com o `spec` dela; entram
   o Barqueiro no sorteio, a Ilse fora do sorteio e achável pelo id, a migração (e rodar duas vezes dá o mesmo save) e o
   retrato pelo id. O `test_conteudo` (ids únicos, lore do que aparece: o `afogado` já tem) cobre a ficha nova.
7. **Preservado:** a história, a luta (números, rito do descanso pelo limiar da fase), os textos e a arte da Ilse.

## 2. O antagonista do mundo gerado

### O que o jogo estabelece (conferido)

- **Onde existe:** só no mundo gerado. `mundo.gerar_mundo` sorteia o antagonista; na campanha `mundo["antagonista"]` é `None`
  (`campanha.py`), e os eventos que o citam ficam fora dela (`eventos/vila.py`: "a campanha ainda não tem vilão").
- **O que é sorteado por partida** (`mundo.gerar_mundo`, três sorteios independentes, gravados no save como texto:
  `{"nome", "curto", "g", "origem"}`):
  - o título e o gênero, entre 8 (`dados.ANTAGONISTAS`): Senhor do Terror, Rainha das Moscas, Devorador de Almas,
    Arcebispo Profanado, Mãe das Ninhadas, Arauto do Vazio, Noiva da Peste, Rei Enforcado (3 femininos, 5 masculinos);
  - o nome próprio (`tx.nome_proprio`, 3 sílabas; o nome completo fica "<nome>, <título>");
  - a origem, entre 5 (`ORIGENS_ANTAGONISTA`): o herói que cravou uma pedra do Inferno na testa para prender um demônio,
    e perdeu; quem vendeu a cidade ao Vazio para não morrer; nascido do último suspiro de um deus esquecido; o bispo que
    abriu as catacumbas procurando Deus; quem abriu a Fenda há cem anos e quer atravessá-la por completo;
  - a cidadela final, entre 5 nomes (Torre Negra, Cidadela Partida, Trono do Vazio, Bastião das Cinzas, Coroa de
    Obsidiana).
- **O que é fixo:**
  - **A relação com a Fenda:** a Fenda se abriu há cem anos sob a catedral; "do outro lado fala" o antagonista
    (`introducao`). Três guardiões deformados pela Fenda guardam os Sigilos do caminho até a cidadela. Na vitória, ele
    "se desfaz como cinza ao vento" e a Fenda se fecha.
  - **O objetivo implícito:** atrair (os sussurros na fogueira: "Junte-se a mim e nunca mais terá medo"; o pregador da
    vila: "não é o fim, é o começo! Abram-se ao Vazio!") e esperar no trono.
  - **A aparência descrita:** quase nada concreto. Foi gente: as paredes da cidadela o mostram "jovem, sorrindo; depois
    ajoelhado diante da Fenda; depois algo que não é mais gente" (`eco_do_vazio`). Espera "num trono de pedra rachada" no
    alto de uma escadaria (`batalha_final`); na visão, "um trono rachado, um céu sem estrelas", olhando direto para o
    herói. Na fase 3, "a forma se desfaz e se refaz, imensa, um rasgo vivo no mundo".
  - **As falas:** pela classe ("Eu também empunhei uma espada, um dia"; "como se acerta o que não tem coração?";
    "Somos iguais"), pela reputação, a da fase 2 ("Você ainda não entendeu? Eu SOU o Vazio."), "Eu vejo você".
  - **A luta** (`inimigos.instanciar_antagonista`, nível 11): só o traço `conjurador` (não é morto-vivo), ataque de
    sombra, resistente à sombra e fraco ao sagrado; Bola de Sombra, Drenar, Grito de Terror, Maldição, Varredura; três
    fases (a 66%: as sombras ganham forma, ele passa a invocar crias do Vazio; a 33%: a forma imensa, mais o Esmagar).
    Antes, o Último Guarda (cavaleiro sombrio); junto, a Yara se traiu o grupo.
  - **Na tela hoje:** a carta da luta (32), no sprite `humano` (família `antagonista`, sem papel em `RETRATO_FAMILIA`).
- **O que é interpretação** (não está no jogo): qualquer rosto, roupa, coroa, idade, cor e o que a Fenda fez com o corpo.
  O canon visual é: foi humano, já não é por inteiro, tem um trono rachado, fala pelo Vazio, termina imenso e desfeito.

### Por que um retrato único tem limite

Os títulos sorteados prometem imagens que se contradizem: a Rainha das Moscas pede moscas, a Mãe das Ninhadas um corpo
de ninhada, o Rei Enforcado a corda no pescoço, o Arcebispo Profanado a mitra, a Noiva da Peste o véu e a doença. Um
retrato com qualquer um desses atributos contradiz sete dos oito títulos (a corda numa "Noiva da Peste"; a mitra numa
"Mãe das Ninhadas"). E 3 dos 8 são femininos: um rosto claramente masculino contradiz a Rainha, a Mãe e a Noiva. Um
retrato único só funciona **neutro de título e de gênero**: o que é comum a todos (o humano tomado pelo Vazio, o trono
rachado), não o que é do título. Se o Jean quiser um retrato por título, a chave já está no save (o `curto`), sem
migração, mas são 8 desenhos e cada um precisa de um título que seja imagem.

**Achados de texto, independentes, para outra entrega:** os sorteios não combinam gênero com o título. "Dizem que ele
ainda sente falta de quem foi" (`eventos/vila.py`, o lore da taverna) e "ajoelhado" (`eco_do_vazio`) são sempre
masculinos; a origem "o bispo que abriu as catacumbas" e "nascido do último suspiro" podem cair numa Rainha das Moscas ou
numa Noiva da Peste.

### Três direções visuais (em texto)

1. **A. O que a Fenda está apagando.** Um busto humano de frente, o rosto magro e sem idade, metade ainda gente (um olho
   cansado, a pele pálida, a boca fechada) e metade rachada como vidro escuro, com o Vazio por trás (o preto e o violeta
   da Cria do Vazio, sem brilho de estrela); a rachadura sobe pela testa e quebra um diadema simples de pedra. Gola alta e
   manto escuro gasto, de quem já teve posto. **Silhueta:** cabeça e ombros, a coroa partida como único recorte. **Liga
   a:** o `eco_do_vazio` (gente que virou outra coisa), as origens (todas são de alguém que foi humano ou que tomou forma
   humana), "Eu SOU o Vazio", o trono de pedra rachada, a Cria do Vazio que ele invoca (a mesma cor). **32→16:** o corte
   vertical entre a metade humana e a metade escura sobrevive bem (é um contraste de massa); as ramificações da
   rachadura viram uma ou duas linhas, e o diadema, três pixels.
2. **B. O rasgo.** A forma da fase final, sem rosto humano: um capuz ou um vulto alto cujo rosto é uma fenda vertical
   aberta, com uma borda de luz fria e, dentro, um único olho. **Silhueta:** um vulto pontudo com um rasgo no meio.
   **Liga a:** "um rasgo vivo no mundo", "como se acerta o que não tem coração?". Neutro de título e de gênero por
   natureza. **32→16:** fácil (uma forma escura e uma fenda clara). **Limite:** sem expressão, o contrário do que o Jean
   pede para retrato; encosta no Caído, na Cria do Vazio e no espectro; e perde o "foi gente", que é o que o jogo mais diz
   dele.
3. **C. O soberano de pedra.** O rosto coberto por uma máscara de pedra lisa e rachada, da mesma pedra do trono, com os
   olhos ocos e o Vazio atrás; uma coroa que parece continuar o encosto do trono, em pontas de obsidiana; o manto pesado
   de gola alta. **Silhueta:** coroa alta e larga, ombros quadrados. **Liga a:** o trono de pedra rachada, os nomes da
   cidadela (Coroa de Obsidiana, Trono do Vazio). A máscara esconde gênero e título. **32→16:** a coroa e a máscara clara
   leem bem. **Limite:** a máscara tira a expressão; coroa mais morto e frio encosta no Lich Menor e no Senhor da Guerra.

**A minha recomendação: A, o que a Fenda está apagando.** É a única que mostra o que o jogo afirma (foi humano, deixou de
ser), guarda um olho e uma boca para a expressão, liga o antagonista à Cria do Vazio pela cor e lê em 16 pelo contraste
das duas metades. **A principal limitação:** o rosto tem de ficar neutro de gênero e de título (magro, sem barba, sem
cabelo marcado, sem mitra, corda ou moscas), o que o deixa menos específico que um retrato por título; e o diadema
precisa ser discreto para não disputar com a coroa do Lich. **Para a integração futura:** o papel pela família
(`RETRATO_FAMILIA["antagonista"]`, já marcada em `instanciar_antagonista`), sem mudança de save; um retrato diferente na
fase 3 não existe hoje para nenhum chefe e seria outra decisão.

## 3. A família `esqueleto_servo`

- **O que é:** `FAMILIAS["esqueleto_servo"]` em `rpg/dados.py` (servo esquelético, 18 de vida, ataque 6, defesa 3,
  agilidade 3, `morto-vivo`, sem habilidades, sem XP nem ouro, sem lore).
- **A história** (`git log -S`): está no catálogo desde o primeiro commit (`db9cd0a7`, 05/10/2026). Já ali o Erguer Servo
  não a usava: `classes._erguer_servo` chamava `cb.invocar_aliado("Servo Esquelético", hp=..., atk=...)` com números pelo
  poder do herói, e nada chamava `criar(..., "esqueleto_servo")`. Ficou como sobra de um plano inicial (o servo como
  família) que não foi seguido. Os commits seguintes que citam o nome são registros de arte que constatam que ela não é
  usada.
- **As referências hoje:** nenhuma no código do jogo. Não está em nenhum bioma, noite, escolta, criaturas da Fenda nem em
  `invoca` de guardião; não entra no Bestiário (sem lore); nenhum contrato a sorteia. Os saves não a guardam (nada a
  cria, então nenhum bestiário nem contrato a registra). Nenhum sorteio percorre `FAMILIAS` inteiro, então tirá-la não
  mexe no `rng`. Restam: um teste (`tests/test_retratos.py`, `test_esqueleto_pela_familia`, que confere que ela fica na
  `caveira`), o `levantamento.py` das criaturas (que lista o catálogo) e os registros.
- **O servo de verdade** (o "Esqueleto (Invocado)" do Erguer Servo e o inimigo erguido pelo Rei dos Mortos) é um aliado
  de `tipo="servo"`, sem família, com o retrato pelo `Aliado.retrato` desde a 1.196.0. Não depende dela.

**A minha recomendação: remover, numa correção pequena (um número de versão de correção), não agora.** Não guarda nada,
não alimenta nada, e confunde quem lê o catálogo. Reaproveitar para
guardar os números do servo seria criar uma abstração que o Erguer Servo não precisa (os números dele saem do poder do
herói). **O impacto:** apagar a entrada; o `test_esqueleto_pela_familia` perde a asserção dela (as do esqueleto inimigo
continuam); o gabarito deve sair idêntico sem atualizar; nenhuma migração.

## As decisões abertas (do Jean)

1. Aprovar o Barqueiro do Charco (o conceito e os textos) e autorizar a separação da Ilse com a migração v6→v7.
2. A direção do antagonista (a recomendação: A), e se o retrato é único e neutro ou se um dia é por título.
3. Autorizar a remoção do `esqueleto_servo` numa correção.
4. Os achados de texto do antagonista (o gênero que não acompanha o título) para outra entrega.
