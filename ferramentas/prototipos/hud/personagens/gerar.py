"""Escreve personagens-teste.js (os candidatos, com as paletas do jogo) a partir de candidatos.py, para a página de
comparação e para a troca no jogo (personagens-no-jogo.js). As cores vêm de retratos.js pelo extrair.mjs: nenhuma
cor nova.
    python ferramentas/prototipos/hud/personagens/gerar.py"""
import json, pathlib, subprocess
import candidatos

AQUI = pathlib.Path(__file__).resolve().parent
atuais = json.loads(subprocess.run(["node", str(AQUI / "extrair.mjs")], capture_output=True, text=True, check=True).stdout)
dados = {
    "morel": {"cores": atuais["morel-carta"]["cores"], "carta": candidatos.MOREL_CARTA, "cabeca": candidatos.MOREL_CABECA},
    "mago": {"cores": atuais["mago-carta"]["cores"], "figura": candidatos.MAGO_FIGURA},
}
for n, d in dados.items():
    for p, g in d.items():
        if p == "cores":
            continue
        assert len({len(l) for l in g}) == 1 and len(g) == len(g[0]), f"{n}-{p}: grade não é quadrada"
        sobra = {c for l in g for c in l} - set(d["cores"]) - {"."}
        assert not sobra, f"{n}-{p}: letras sem cor {sobra}"
(AQUI / "personagens-teste.js").write_text(
    "// Gerado por gerar.py a partir de candidatos.py: as propostas (a carta e a cabeça do Morel, a figura do Mago na\n"
    "// fogueira), com as paletas de retratos.js. O jogo não lê este arquivo.\n"
    "window.PersonagensTeste = " + json.dumps(dados, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
(AQUI / "atuais.json").write_text(json.dumps(atuais, ensure_ascii=False))
print("ok")
