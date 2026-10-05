"""Legado: o que heróis de partidas anteriores deixam para os próximos."""

import json
import os

ARQUIVO = "legado.json"


def carregar(pasta):
    try:
        with open(os.path.join(pasta, ARQUIVO), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def registrar(pasta, registro):
    lista = carregar(pasta)
    lista.append(registro)
    try:
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, ARQUIVO), "w", encoding="utf-8") as f:
            json.dump(lista[-20:], f, ensure_ascii=False)
    except OSError:
        pass
