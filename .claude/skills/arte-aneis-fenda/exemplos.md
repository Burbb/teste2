# Os anéis aprovados e os recusados

Exemplos de raciocínio, não regras: o ouro e o ziguezague são escolhas deste anel.

## O anel comum (aprovado; no jogo desde a 1.140.0)

A rodada 3 com a gravação, aprovada pelo Jean no `9ae59a9`. Vale para as bases Anel, Sinete e Aro e para o único Anel do
Último Rei, e é também a silhueta apagada dos espaços vazios. Fontes em `ferramentas/arte/aseprite/anel/` (32, 40, 48;
o 64 é o 32 ×2); o histórico em `ferramentas/prototipos/hud/itens-lote-noite/anel_amuleto/`.

- **A construção:** o aro como um cilindro curto (`auxiliares/aro.py`), com o ângulo e as proporções da referência
  principal (`sample (2).png`) achados pelo `ajuste_aro.py`: a silhueta e o vão reduzidos a 32 sobrepõem 0,93 e 0,97.
  Das duas famílias de eixo com a mesma silhueta, ficou a que põe a faixa de fora larga em cima e à esquerda e a parede
  de dentro embaixo e à direita. A parede foi afinada à mão (1,4 no quadro de 32) para a borda ser a linha fina da
  referência, mesmo com a sobreposição do vão caindo: a comparação visual decidiu.
- **O metal:** o ouro das moedas aprovadas (claro e saturado, como o sample), a face de fora em três planos largos, o
  chanfro de 1 px nas beiras, a face de dentro escura em cima e clara embaixo, as bordas claras, o reflexo agrupado;
  limpo face a face.
- **O ornamento leve:** um ziguezague gravado no meio da face de fora (o Jean liberou "uns ornamentos leves"), que
  acompanha a curva da faixa; feito numa segunda passada, para sair contínuo. É um eco simples da gravação entrelaçada
  do sample, que no 32 viraria ruído.
- **A comparação:** `anel_amuleto/anel-referencia-r2-r3.png` (a referência × a rodada 2 × a rodada 3).

### A alternativa lisa (histórico)

A mesma rodada 3 sem a gravação (`aro.py <N> liso`), em `anel_amuleto/rodada3_liso/`. Funciona; ficou como
alternativa quando o Jean preferiu o ornamento leve.

### As rodadas recusadas

- **Rodada 1** (`anel_amuleto/rodada1/`): um aro de latão achatado, visto de cima em três quartos, com uma granada num
  engaste. O ângulo não agradou e o aro ficou achatado; antes dela, uma versão com o aro ainda menor
  (`anel_amuleto/recusados/anel-menor/`) tinha pouca presença no espaço de 32.
- **Rodada 2** (`anel_amuleto/rodada2/`): o aro em pé, já modelado como cilindro, mas com a abertura inclinada para o
  lado oposto ao da referência (o eixo espelhado). No caminho até ela, o eixo virado demais para o lado fez uma fresta
  (um bracelete grosso) e a primeira luz saiu barrenta. Foi também a primeira com o ouro e o chanfro do sample.
