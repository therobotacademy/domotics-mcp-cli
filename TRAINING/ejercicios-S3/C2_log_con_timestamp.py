# =============================================================================
# Ejercicio C-2 — Añadir timestamp al log sin mutar el original  ★★☆
# Bloque C · Comprensión del código Domotics-MCP-cli
# =============================================================================
#
# CONTEXTO:
#   El método _log() de agent.py (líneas 106-109) escribe el payload tal cual.
#   Queremos enriquecerlo añadiendo siempre un campo "ts" con la hora UTC.
#
#   REGLA IMPORTANTE: no modifiques el diccionario que llega como argumento.
#   El llamador puede necesitar ese dict después; si lo mutamos causamos
#   un bug difícil de detectar. Usa .copy() para trabajar con una copia.
#
# TAREA:
#   Completa la función _log() para que:
#     1. Cree una copia del payload.
#     2. Añada "ts": datetime.utcnow().isoformat() a la copia.
#     3. Escriba la copia (no el original) en el fichero como línea JSON.
#
#   También implementa leer_log(path) que:
#     - Lee el fichero línea a línea.
#     - Devuelve una lista de diccionarios.
#
# COMPROBACIÓN AUTOMÁTICA al final del script.
# =============================================================================

import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("test_log_ts.jsonl")


def _log(payload: dict) -> None:
    """Escribe payload enriquecido con 'ts' en LOG_PATH (modo append)."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    # --- ESCRIBE TU CÓDIGO AQUÍ ---


def leer_log(path: Path) -> list:
    """Lee el fichero JSONL y devuelve lista de dicts."""
    resultado = []

    # --- ESCRIBE TU CÓDIGO AQUÍ ---

    return resultado


# --- NO MODIFICAR DESDE AQUÍ ---
LOG_PATH.unlink(missing_ok=True)   # limpia fichero anterior

evento1 = {"room_id": "salon",      "status": "executed"}
evento2 = {"room_id": "dormitorio", "status": "blocked"}

_log(evento1)
_log(evento2)

# El dict original NO debe haber sido modificado
assert "ts" not in evento1, "Error: modificaste el dict original de evento1"
assert "ts" not in evento2, "Error: modificaste el dict original de evento2"

registros = leer_log(LOG_PATH)

errores = 0
if len(registros) != 2:
    print(f"  [FALLO] Se esperaban 2 registros, hay {len(registros)}")
    errores += 1
else:
    for i, reg in enumerate(registros, 1):
        tiene_ts     = "ts" in reg
        tiene_roomid = "room_id" in reg
        ok = tiene_ts and tiene_roomid
        if not ok:
            errores += 1
        print(f"  [{'OK' if ok else 'FALLO'}] Registro {i}: room_id={reg.get('room_id')}  ts={'presente' if tiene_ts else 'AUSENTE'}")

print()
if errores == 0:
    print("Correcto: timestamp añadido, dict original intacto.")
    LOG_PATH.unlink(missing_ok=True)
else:
    print(f"{errores} error(es). Revisa la implementación.")
