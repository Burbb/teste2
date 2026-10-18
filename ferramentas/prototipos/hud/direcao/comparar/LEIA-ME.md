# Comparação jogável: produção × protótipo da HUD (em avaliação, nada no jogo)

**Pedido de Jean (18/10/2026):** pausar a integração da nova HUD para avaliar jogando. A dúvida é se a pintura
permanente combina com a pixel art ou chama mais atenção que o mundo. Os menus de pincelada continuam aprovados.

## Como abrir (PowerShell)

```powershell
cd "C:\Users\Jean Wress\Desktop\packs\teste2"
python ferramentas\prototipos\hud\direcao\comparar\jogar_comparacao.py producao
python ferramentas\prototipos\hud\direcao\comparar\jogar_comparacao.py prototipo
```

**Cada comando abre o jogo como o `python jogar.py`:** na janela própria de sempre (pywebview), com o menu do título.
Escolha *Carregar jogo* e o save.

**Opções:**
- **`--recomecar`:** volta o save do teste ao ponto de partida (copia o original de novo).
- **`--save turvo_chimpa`:** usa outro save da pasta de sempre (o nome do arquivo, sem `.json`).
- **`--navegador`:** abre no navegador em vez da janela própria.
- **`--sem-abrir`:** só mostra o endereço.

## Os dados

**O save atual de Jean:** o mais recente da pasta de sempre (`%USERPROFILE%\.cronicas_da_fenda`) é
`turvo_dadad.json`, de 18/10, às 01:55. É o padrão:
- dadad, arqueiro (sombra), nível 5, dia 19;
- com Bastian Morel e a Irmã Odette;
- na Capela Afogada.

**A alternativa:** `turvo_chimpa.json` (mago piromante, nível 6, dia 34).

**Os saves do teste**, um por versão. As duas começam do mesmo ponto e não se misturam:

```
%USERPROFILE%\.cronicas_da_fenda_teste_hud\producao\
%USERPROFILE%\.cronicas_da_fenda_teste_hud\prototipo\
```

- **Na primeira vez**, o lançador copia o save para a pasta de cada versão.
- **Depois**, continua de onde o teste parou (`--recomecar` volta ao original).
- **O original só é lido.** Conferido pelo hash, ele saiu igual.

## O que cada versão mostra

- **`producao`:** o jogo como está (1.118.0), sem nada acrescentado.
- **`prototipo`:** o estudo completo por cima do jogo, só no processo do teste:
  - a ficha com a pintura (`../ficha/ficha.css`, `pintura.css`);
  - o conjunto (`../conjunto/conjunto.css`): o centro, o mundo, as cartas, a mira, a doca e o seletor;
  - o topo pintado (`../topo/topo.css`);
  - a marcação da dica dos testes (`../direcao.js`).

  Ao entregar `app/controles.js`, o servidor acrescenta as folhas e os scripts, e entrega a arte em `/proto-ficha`,
  `/proto-conjunto` e `/proto-topo`. Nenhum arquivo do jogo muda.

## Conferido

**O lançador:**
- a cópia do save, idêntica, com o original intacto (hash);
- em produção, `controles.js` sai igual ao arquivo do jogo;
- no protótipo, o estudo é acrescentado e as cinco imagens são entregues.

**O save real, nas duas versões:** abre pelo menu (*Carregar jogo*) com o herói, a comitiva e o lugar certos, e
nenhum erro na página. As cópias do teste voltaram ao original depois da conferência.

**O que não fiz:** nova arte, capturas nem vídeos (a avaliação é de Jean, jogando).

## Para experimentar

- **Exploração:** na Capela Afogada, explorar ou viajar.
- **Acampamento:** *Acampar e descansar*, num lugar selvagem.
- **Combate:** os encontros da exploração.

O protótipo foi feito e conferido na janela de 1920×945 (maximizada). Em outros tamanhos, as pinturas da ficha e do
mundo têm altura fixa e a do topo acompanha a largura (ver os LEIA-ME de `../ficha`, `../conjunto` e `../topo`).
