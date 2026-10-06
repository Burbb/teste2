"""Telemetria da partida: registra o que aconteceu para analisar o equilíbrio do jogo.

Durante o jogo, `registrar(g, tipo, **dados)` acrescenta um evento em g.registro.
No fim da partida (ou ao salvar), `exportar(g)` grava:
  - <pasta_saves>/runs/<data>_<nome>.jsonl  (um evento por linha, completo)
  - <pasta_saves>/runs/<data>_<nome>.md     (resumo legível com tabelas)

Nada sai do seu computador: os arquivos ficam na pasta de saves.
"""

import datetime
import json
import os
import re

VERSAO = 1


def registrar(g, tipo, **dados):
    j = g.j
    evento = {"t": tipo, "dia": g.dia, "periodo": g.periodo, "passo": g.passos}
    if j:
        evento.update(nv=j.nivel, hp=j.hp, hp_max=j.max_hp, rec=j.rec, rec_max=j.max_rec, ouro=j.ouro)
    evento.update(dados)
    g.registro.append(evento)


def instantaneo(j):
    return {"atk": j.atk, "defesa": j.defesa, "agi": j.agi, "poder": j.poder, "max_hp": j.max_hp,
            "max_rec": j.max_rec, "regen": j.regen}


def novo_combate(cb):
    j = cb.j
    cb.tel = {"hp_inicio": j.hp, "rec_inicio": j.rec, "dano_causado": 0, "dano_aliados": 0, "dano_recebido": 0,
              "maior_golpe": 0, "habilidades": {}, "rec_gasto": 0, "itens": [], "esquivas": 0,
              "criticos_recebidos": 0}


def contabilizar_dano(cb, u, alvo, dano, critico):
    tel = getattr(cb, "tel", None)
    if tel is None:
        return
    if u is cb.j:
        tel["dano_causado"] += dano
    elif u in cb.aliados:
        tel["dano_aliados"] += dano
    if alvo is cb.j:
        tel["dano_recebido"] += dano
        tel["maior_golpe"] = max(tel["maior_golpe"], dano)
        if critico:
            tel["criticos_recebidos"] += 1


def fim_combate(cb, resultado):
    tel = getattr(cb, "tel", None)
    if tel is None:
        return
    g, j = cb.g, cb.j
    inimigos = [{"nome": e.nome, "familia": e.familia, "nivel": e.nivel, "afixo": e.afixo, "chefe": e.chefe,
                 "hp_max": e.max_hp, "atk": round(e.atk, 1), "poder": round(e.poder, 1), "morto": not e.vivo}
                for e in cb.inimigos]
    registrar(g, "combate", resultado=resultado, titulo=cb.titulo, emboscada=cb.emboscada,
              nivel_regiao=g.nivel_local(), local=g.loc["nome"], clima=g.clima, inimigos=inimigos,
              turnos=cb.turno, hp_fim=j.hp, rec_fim=j.rec, sem_luz=g.sem_luz, **tel)


def _nome_arquivo(g):
    if not getattr(g, "arquivo_run", None):
        data = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
        slug = re.sub(r"[^a-z0-9]+", "_", g.j.nome.lower()).strip("_") or "heroi"
        g.arquivo_run = f"{data}_{slug}_{g.j.classe}"
    return g.arquivo_run


def exportar(g):
    """Grava o registro completo e o resumo. Devolve o caminho do resumo (ou None se falhar)."""
    if not g.registro or not g.j:
        return None
    pasta = os.path.join(g.pasta_saves, "runs")
    base = os.path.join(pasta, _nome_arquivo(g))
    try:
        os.makedirs(pasta, exist_ok=True)
        with open(base + ".jsonl", "w", encoding="utf-8") as f:
            f.write(json.dumps({"t": "cabecalho", "versao": VERSAO, "seed": g.seed, "classe": g.j.classe,
                                "hardcore": g.hardcore}, ensure_ascii=False) + "\n")
            for ev in g.registro:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        with open(base + ".md", "w", encoding="utf-8") as f:
            f.write(resumo(g.registro))
    except OSError:
        return None
    return base + ".md"


# ---------------------------------------------------------------------- resumo
def _pct(a, b):
    return f"{100 * a / b:.0f}%" if b else "-"


def resumo(registro):
    ev = [e for e in registro if e["t"] != "cabecalho"]
    linhas = []
    w = linhas.append
    inicio = next((e for e in ev if e["t"] == "inicio"), {})
    fim = next((e for e in reversed(ev) if e["t"] == "fim"), None)
    spec = next((e["spec"] for e in ev if e["t"] == "spec"), None)
    ultimo = ev[-1] if ev else {}
    w(f"# Run: {inicio.get('nome', '?')} — {inicio.get('classe', '?')}" + (f" / {spec}" if spec else ""))
    w("")
    w(f"- Semente: {inicio.get('seed')} · Hardcore: {inicio.get('hardcore')} · Versão do registro: {VERSAO}")
    if fim:
        w(f"- Resultado: **{fim['resultado']}** — {fim.get('causa', '')}")
    else:
        w("- Resultado: partida em andamento")
    w(f"- Dias: {ultimo.get('dia')} · Nível final: {ultimo.get('nv')} · Passos: {ultimo.get('passo')}")
    w("")

    w("## Progressão")
    w("")
    w("| Nível | Dia | Ataque | Defesa | Agilidade | Poder | Vida máx | Recurso máx |")
    w("|---|---|---|---|---|---|---|---|")
    for e in ev:
        if e["t"] == "nivel":
            s = e["stats"]
            w(f"| {e['nv']} | {e['dia']} | {s['atk']} | {s['defesa']} | {s['agi']} | {s['poder']} | {s['max_hp']} | "
              f"{s['max_rec']} |")
    w("")
    talentos = [e for e in ev if e["t"] == "talento"]
    if spec:
        dia_spec = next(e["dia"] for e in ev if e["t"] == "spec")
        w(f"Especialização: **{spec}** (dia {dia_spec})")
        w("")
    if talentos:
        w("Talentos, na ordem: " + " → ".join(f"{e['nome']} {e['rank']} (nv {e['nv']})" for e in talentos))
        w("")

    combates = [e for e in ev if e["t"] == "combate"]
    w("## Combates por nível do herói")
    w("")
    w("| Nv herói | Lutas | Nv inimigo médio | Turnos | Dano causado/luta | Dano recebido/luta | "
      "Vida perdida/luta | Maior golpe | Recurso no fim | Derrotas | Fugas |")
    w("|---|---|---|---|---|---|---|---|---|---|---|")
    por_nivel = {}
    for c in combates:
        por_nivel.setdefault(c["nv"], []).append(c)
    for nv in sorted(por_nivel):
        cs = por_nivel[nv]
        n = len(cs)
        nv_ini = sum(sum(i["nivel"] for i in c["inimigos"]) / max(1, len(c["inimigos"])) for c in cs) / n
        perda = sum((c["hp_inicio"] - c["hp_fim"]) / max(1, c["hp_max"]) for c in cs) / n
        rec_fim = sum(c["rec_fim"] / max(1, c["rec_max"]) for c in cs) / n
        w(f"| {nv} | {n} | {nv_ini:.1f} | {sum(c['turnos'] for c in cs) / n:.1f} | "
          f"{sum(c['dano_causado'] for c in cs) / n:.0f} | {sum(c['dano_recebido'] for c in cs) / n:.0f} | "
          f"{perda:.0%} | {max(c['maior_golpe'] for c in cs)} | {rec_fim:.0%} | "
          f"{sum(c['resultado'] == 'derrota' for c in cs)} | {sum(c['resultado'] == 'fuga' for c in cs)} |")
    w("")
    habs = {}
    for c in combates:
        for h, q in c["habilidades"].items():
            habs[h] = habs.get(h, 0) + q
    if habs:
        w("Habilidades usadas: " + ", ".join(f"{h} ×{q}" for h, q in sorted(habs.items(), key=lambda x: -x[1])))
        w("")
    secos = sum(1 for c in combates if c["rec_fim"] < 0.2 * c["rec_max"])
    w(f"Lutas que terminaram com recurso abaixo de 20%: {secos} de {len(combates)} ({_pct(secos, len(combates))})")
    w("")

    chefes = [c for c in combates if any(i["chefe"] for i in c["inimigos"])]
    if chefes:
        w("## Chefes")
        w("")
        w("| Chefe | Nv chefe | Nv herói | Resultado | Turnos | Vida perdida | Maior golpe |")
        w("|---|---|---|---|---|---|---|")
        for c in chefes:
            ch = next(i for i in c["inimigos"] if i["chefe"])
            w(f"| {ch['nome']} | {ch['nivel']} | {c['nv']} | {c['resultado']} | {c['turnos']} | "
              f"{_pct(c['hp_inicio'] - c['hp_fim'], c['hp_max'])} | {c['maior_golpe']} |")
        w("")

    w("## Sobrevivência e itens")
    w("")
    ferimentos = [e for e in ev if e["t"] == "ferimento"]
    w(f"- Ferimentos sofridos: {len(ferimentos)}"
      + (f" ({', '.join(e['id'] for e in ferimentos)})" if ferimentos else ""))
    w(f"- Dias com fome: {sum(1 for e in ev if e['t'] == 'dia' and e.get('fome'))}")
    usados = {}
    for e in ev:
        if e["t"] == "consumivel":
            usados[e["item"]] = usados.get(e["item"], 0) + 1
    w("- Consumíveis usados: " + (", ".join(f"{k} ×{v}" for k, v in usados.items()) if usados else "nenhum"))
    equipados = [e for e in ev if e["t"] == "equipar"]
    if equipados:
        w("- Itens equipados: " + "; ".join(f"{e['item']} [{e['raridade']}] (nv {e['nv']})" for e in equipados))
    w("")
    com = [e for e in ev if e["t"] == "comitiva"]
    if com:
        w("## Comitiva")
        w("")
        w("| Companheiro | Entrou (dia) | Saída | Aprovação final | Reações + / − | Conversas |")
        w("|---|---|---|---|---|---|")
        for cid in dict.fromkeys(e["id"] for e in com):
            meus = [e for e in com if e["id"] == cid]
            entrou = next((e["dia"] for e in meus if e.get("acao") == "entra"), "—")
            saida = next((f"{e['acao']} (dia {e['dia']})" for e in meus
                          if e.get("acao") in ("morto", "partiu", "entregue", "dispensado", "traiu")), "ficou")
            opinioes = [e for e in meus if e.get("acao") == "opiniao"]
            final = opinioes[-1]["aprovacao"] if opinioes else 0
            pos = sum(1 for e in opinioes if e["delta"] > 0)
            neg = sum(1 for e in opinioes if e["delta"] < 0)
            conversas = sum(1 for e in meus if e.get("acao") == "conversa")
            w(f"| {cid} | {entrou} | {saida} | {final:+d} | {pos} / {neg} | {conversas} |")
        dano = sum(e.get("dano_aliados", 0) for e in ev if e["t"] == "combate")
        w("")
        w(f"Dano causado por aliados (comitiva, animal e servos): {dano}")
        w("")
    eventos = {}
    for e in ev:
        if e["t"] == "evento":
            eventos[e["id"]] = eventos.get(e["id"], 0) + 1
    if eventos:
        w("## Eventos vistos")
        w("")
        w(", ".join(f"{k} ×{v}" for k, v in sorted(eventos.items(), key=lambda x: -x[1])))
        w("")
    dias = [e for e in ev if e["t"] == "dia"]
    if dias:
        w("## Por dia")
        w("")
        w("| Dia | Nv | Vida | Ouro | Provisões | Corrupção | Ferimentos |")
        w("|---|---|---|---|---|---|---|")
        for e in dias:
            w(f"| {e['dia']} | {e['nv']} | {e['hp']}/{e['hp_max']} | {e['ouro']} | {e.get('provisoes')} | "
              f"{e.get('corrupcao')}% | {e.get('ferimentos', 0)} |")
        w("")
    return "\n".join(linhas)


def main():
    """python -m rpg.telemetria ARQUIVO.jsonl  → imprime o resumo."""
    import sys
    if len(sys.argv) < 2:
        print("uso: python -m rpg.telemetria ARQUIVO.jsonl")
        return
    with open(sys.argv[1], encoding="utf-8") as f:
        registro = [json.loads(linha) for linha in f if linha.strip()]
    print(resumo(registro))


if __name__ == "__main__":
    main()
