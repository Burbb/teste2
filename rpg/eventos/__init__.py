"""Eventos procedurais. Importar este pacote registra todos os eventos."""

from . import comuns, biomas, classe, noite, vila  # noqa: F401  (registro por efeito colateral)
from .motor import REGISTRO, disparar  # noqa: F401
