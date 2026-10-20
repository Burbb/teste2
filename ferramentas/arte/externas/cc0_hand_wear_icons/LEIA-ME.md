# CC0 Hand Wear Icons (arte externa, CC0)

- **Coleção:** "CC0 Hand Wear Icons", montada por AntumDeluge no OpenGameArt,
  https://opengameart.org/content/cc0-hand-wear-icons; baixada em 20/10/2026 (os oito pacotes `.zip` da página), a
  pedido do Jean, para escolher uma base de luva.
- **Licença:** CC0 (Creative Commons Zero, http://creativecommons.org/publicdomain/zero/1.0/), declarada na página para
  todos os conjuntos; cada conjunto vem de uma fonte CC0 (o `.txt` de cada pasta tem a origem). O montador avisa que as
  imagens de fontes maiores que 32×32 foram reduzidas por ele.
- **Conteúdo:** `original/<conjunto>/` como veio de cada `.zip` (os PNGs e o `.txt` de origem; sem alteração). Ficou de
  fora só o `glove-DCSS.xcf` (o arquivo do GIMP do montador, não necessário). Não editar: adaptações, se houver,
  trabalham sobre cópias.

| Conjunto (pasta) | Fonte / autor | Resolução original |
|---|---|---|
| `glove-dcss` | "Dungeon Crawl 32x32 tiles", https://opengameart.org/node/12210: os tiles do jogo Dungeon Crawl Stone Soup, esforço coletivo de muitos artistas (mantenedor Chris Hamons; a lista completa de artistas no pacote original, `utility/FilteredList.txt`), CC0 | 32×32 nativo |
| `glove-yd` | "Pointers: part 5", https://opengameart.org/node/12516, autor yd, CC0 | 72×72 (o 32 é redução do montador) |
| `glove-7soul1_20201212` | https://www.deviantart.com/7soul1/art/129892453, autor 7Soul1 | ver a fonte |
| `glove-babysamurai` | https://opengameart.org/node/96388, autor babysamurai | 32 e 24 no pacote |
| `glove-fleurman` | https://opengameart.org/node/77730, autor Fleurman | 32 e 24 no pacote |
| `hand-flare_20201217` | os conjuntos de armadura do Flare (https://opengameart.org/node/12815, 13879, 12818) | 64×64 (o 32 é redução) |
| `glove-scratchio` | ScratchIO (https://opengameart.org/node/108781, 108295, 108448) | ver a fonte |
| `glove-ocal_0` | OpenClipart (vetores; os endereços no `glove-OCAL.txt`) | vetor reduzido |

**Adaptações (20/10/2026, só no protótipo, não aprovadas):** `glove-dcss/32x32/glove/glove_03.png` (a base B4) e
`glove_04.png` (a B5) foram adaptadas para malha de ferro (M4 e M5), sobre cópias, em
`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/malha_dcss/`: a silhueta, o contorno, a pose, os dedos,
o polegar e o punho são os do original (artistas do Dungeon Crawl Stone Soup, CC0); mudou o material. Se uma entrar no
jogo, este registro e o crédito acompanham a integração.

**No jogo (1.147.0):** a M5 (da `glove_04.png`) aprovada pelo Jean é a manopla do Guerreiro: as fontes em
`ferramentas/arte/aseprite/manopla/manopla-32.aseprite`, `-40`, `-48` (a camada `original` guarda o sprite da Dungeon
Crawl, oculta e fora da exportação) e os PNGs `rpg/web/static/hud/icones/manopla-*.png`. Crédito: arte original dos
artistas do Dungeon Crawl Stone Soup ("Dungeon Crawl 32x32 tiles", https://opengameart.org/node/12210, CC0), via a
coleção CC0 Hand Wear Icons de AntumDeluge; adaptada (o material) para The Unquiet. A M4 ficou no protótipo.

Uso registrado: a prancha de escolha de base das luvas, em
`ferramentas/prototipos/hud/itens-lote-noite/manopla_perneiras/escolha_base/` (o registro no `LEIA-ME.md` do lote).
