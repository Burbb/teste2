# Estudo de caso: a forja do Vau (25 a 28/10/2026)

O histórico completo está em `ferramentas/prototipos/hud/forja/LEIA-ME.md` (uma seção por candidata). Aqui, o que cada
passo ensinou e onde ficam as fontes. Nada disto é regra para outros lugares: as medidas, a altura de 96, os 53
quadros e a martelada são da forja.

## As candidatas

| Candidata | O que era | O que o Jean disse | O que ficou de lição |
|---|---|---|---|
| A e B (`forja-arte.js`) | duas direções em grades e código, no quadro de 72 | escolheu a B (o espaço), mas vazia e esquemática | o levantamento e as direções antes de refinar |
| R (`forja-r.js`) | a B por zonas, o ferreiro por juntas, o ciclo de 53 quadros | **o ritmo aprovado**; o desenho do ferreiro não (anatomia, barba em placa, caricato) | ritmo e poses são coisas separadas |
| F (`f/`, `forja-f.js`) | a transposição de uma imagem gerada: o fundo pela redução, o ferreiro em grades | não aprovada: pés e pernas, a mão e a tenaz, o fundo derivado demais da redução | a redução não é fundo; os apoios vêm antes |
| G (`g/`, `forja-g.js`) | a oficina redesenhada na linguagem do jogo, os apoios corrigidos | a oficina sim; o corpo "fatiado" (a metade de cima deslizando) e o ferreiro fora do estilo, não | o corpo se anima inteiro; o estilo vale também para o personagem |
| H (`h/`, `forja-h.js`) | o ferreiro no estilo das figuras do jogo, cada pose redesenhada a partir dos apoios | **aprovada** em oficina, enquadramento, corpo, barriga, estilo e movimento; o olho a ajustar | — |
| H2 (`h2/`, `forja-h2.js`) | a H com o olho um pixel mais para trás e a órbita entre a ponte e o olho | aprovada; no jogo na 1.210.0 | o rosto se decide no tamanho real |

## As fontes da H/H2

- `h2/oficina_h2.py`: o fundo inteiro em código (a parede, o teto, o chão, os esteios, a porta, a fornalha, o suporte,
  a lanterna, a tina, o armazém, a bancada, as silhuetas da frente) e a luz por cima (`luz`). A comparação com as cenas
  do jogo: `folha-estilo-g.png`, `folha-estilo-h.png`; as fotos das cenas: `auxiliares/estilo.mjs`.
- `h2/ferreiro_h2.py`: o ferreiro por pose (`POSES`: os ombros, o quadril, a cabeça, a barriga, a trança e o braço do
  martelo), os apoios fixos (as botas, a luva na tenaz), a cabeça, a barba e a trança em grades à mão.
- `h2/ambiente_h2.py`: a bigorna e o toco, a lâmina em brasa, o fogo em 4 quadros. `h2/cena_h2.py`: a linha do tempo e
  as faíscas.
- A fonte em camadas: `h2/aseprite/forja-h2.aseprite` (`desenhar_h2.py` só gera se não existir, ou com `--refazer`;
  `exportar_h2.py --conferir` tira dela as camadas do jogo e compara com o código). No jogo: `forja-h2.js`, pelo cenário
  `auxiliares/cenario_forja.py` (`PROPOSTA=h2`).
- A conferência: `auxiliares/fotografar.mjs` (a interface nas duas janelas), `auxiliares/ciclo_f.mjs` (dois ciclos
  quadro a quadro, um relógio só); as folhas: `auxiliares/folha_g.py`, `folha_h.py`, `folha_h2.py`.

## A referência do movimento

O ritmo veio do André de Dark Souls (um GIF do Tenor, observado quadro a quadro) e da animação de demonstração do
Blacksmith Craft da Craftpix (observada quadro a quadro); outras páginas só foram lidas (o LEIA-ME da forja diz quais).
O que se aproveitou: o martelo segurado no alto, a descida rápida, o peso no golpe, as faíscas no contato, o assentar
e a pausa da tenaz.

## O golpe do ferreiro (27 e 28/10/2026)

O gesto da H2 terminava o golpe com a mão junto do corpo. Quatro passadas numa candidata em código
(`h2/candidata_gesto.py`, "Ferreiro" no painel da demonstração da forja), sem tocar a fonte até a aprovação:

| Avaliação do Jean (sobre a passada) | Causa | A passada seguinte |
|---|---|---|
| 1ª (18ª rodada): o fim do golpe parece guidão de moto, a mão rente ao corpo | cotovelo para trás, cabo de pé | 2ª: o braço estendido à frente, o cabo descendo em ângulo até a lâmina |
| 2ª: melhorou; o ombro ainda sobe no fim (o martelo grande ou o corpo perto) | o contato a 7 px abaixo e 21 px à frente do ombro; braço + cabo de 12,5 px passavam disso | 3ª: o cabo a 10 px; duas variantes, **Corpo desce** (o quadril e os joelhos descem, o ombro 2 px abaixo) e Braço reto |
| 3ª: "Corpo desce" bom; a cabeça do martelo com pixels fora e o cabo desalinhado no contato | a cabeça girada em código em qualquer ângulo | 4ª: nas quatro poses de contato, a cabeça à mão, alinhada à grade, o cabo reto no olho |
| 4ª: aprovada, com a integração autorizada | o gesto só existia no código do protótipo | a consolidação: `h2/consolidar_gesto.py` troca a camada "ferreiro" da fonte (`aseprite/trocar_camada.lua`) e confere; a exportação igual à candidata pixel a pixel, as outras camadas iguais às de antes; `desenhar_h2.py --refazer` agora exige `--sem-os-retoques` |

A subida, o ritmo, os apoios, a tenaz, o contato com a espada e o enquadramento aprovados não mudaram em nenhuma
passada: cada correção mexeu só no que foi apontado.
