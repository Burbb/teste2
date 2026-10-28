# Referências dos cenários internos

A pasta era `referencias/forja/` e o Jean a renomeou em 28/10/2026 para guardar as referências de todos os interiores.
As imagens ficam sem alteração. Cada uma é **referência de composição**: o acabamento vem das cenas aprovadas do jogo
(skill `arte-cenas-fenda`, seção 2).

| Arquivo | Origem | Papel |
|---|---|---|
| `A forja sombria do ferreiro.png` (2172×724, RGB) | **Imagem gerada** na conversa do Jean que abriu a candidata F da forja (25/10/2026), mandada por ele como a referência principal. Guardada sem alteração (SHA-256 `d1cc4b24757d8d90be5aa3b1ce483da3f08ca9844d84fd18a84627af97ba275c`). | **A principal da aparência** do interior da forja: o enquadramento (a oficina de frente, a leve vista de cima das superfícies), a profundidade por sobreposição, a porta fria à esquerda, a fornalha atrás e à esquerda da área de trabalho, o ferreiro no meio, um pouco à direita, voltado para a espada, a bigorna no toco, o armazém e a bancada à direita, as silhuetas da frente, a luz quente do fogo contra o frio e o escuro, e o ferreiro: careca, gordo e forte, a barba ruiva que afunila numa trança com uma presilha, inspirado na construção de um ferreiro anão (só a aparência: a espécie e a história do personagem não mudam). |
| `A herbalista e o almofariz.png` (2172×724, RGB) | **Imagem gerada**, mandada pelo Jean em 28/10/2026 com o pedido do interior da curandeira. Guardada sem alteração (SHA-256 `4dd6dcdc575d4c25eef912d551b78da5f9ca7b188c35c895eaa80d20800638dc`). | **Composição** da cabana da curandeira, ainda sujeita à adaptação: a proximidade e a perspectiva, a bancada como foco, a organização por função (a pia e os panos junto da porta, as ervas secando, a bancada com o almofariz, as prateleiras de potes, o fogo baixo com a panela, o armário), a entrada de luz pela porta e a passagem discreta para os fundos com a cortina. **Não se copia:** o rosto, o cabelo e a identidade da mulher gerada (Pita e Marta vêm da história), a arquitetura de fora vista pela porta, a quantidade de objetos, as texturas miúdas, a luz suave e o acabamento da geração. Uso: a candidata A (`ferramentas/prototipos/curandeira`). |

## A forja

Ela substitui a aparência da R como referência artística; a R (`ferramentas/prototipos/hud/forja/forja-r.js`) continua a
referência do ritmo da animação e do funcionamento da demonstração.

A imagem é ampliada e não é uma grade nativa: a F usa a redução proporcional dela (320 de largura) só como guia do
fundo (`ferramentas/prototipos/hud/forja/f/base_f.py`) e a lê ampliada, com a grade do jogo por cima, para desenhar o
ferreiro, a bigorna e o resto à mão. Uso registrado: a candidata F (`ferramentas/prototipos/hud/forja/LEIA-ME.md`, a
seção "A transposição fiel (F)").

## A curandeira

A candidata A não usa a redução da imagem nem como guia de fundo: a imagem foi lida ampliada para a composição e a
escala, e cada objeto foi construído em código na grade de 320×96 (`ferramentas/prototipos/curandeira/desenho.py`).
