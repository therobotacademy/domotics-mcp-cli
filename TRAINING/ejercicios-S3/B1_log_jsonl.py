# =============================================================================
# Ejercicio B-1 — Escribir y leer un log JSONL  ★☆☆
# Bloque B · T04 Ficheros
# =============================================================================
#
# CONTEXTO:
#   El método _log() de agent.py (líneas 106-109) escribe cada evento del
#   agente en data/agent_log.jsonl usando modo "a" (append).
#   El formato es: una línea por evento, cada línea es JSON válido.
#
#   Este formato se llama JSONL (JSON Lines) y es muy común en logs de
#   sistemas de IA porque es fácil de escribir y de leer línea a línea
#   sin cargar todo el fichero en memoria.
#
# TAREA — PARTE 1: Escritura
#   Escribe los tres eventos de `eventos` en el fichero "mi_log.jsonl".
#   Usa modo "w" (sobreescribir) y encoding="utf-8".
#   Cada evento debe ocupar una línea terminada en \n.
#
# TAREA — PARTE 2: Lectura y filtrado
#   Vuelve a abrir el mismo fichero en modo "r".
#   Lee línea a línea e imprime solo las habitaciones cuyo status sea "executed".
#
# SALIDA ESPERADA:
#   Habitación con acción ejecutada: salon
# =============================================================================

import json

eventos = [
    {"room_id": "salon",      "status": "executed",  "decision": "turn_on"},
    {"room_id": "dormitorio", "status": "noop",       "decision": "do_nothing"},
    {"room_id": "pasillo",    "status": "blocked",    "decision": None},
]

FICHERO = "mi_log.jsonl"

# --- PARTE 1: Escribe los eventos en el fichero ---


# --- PARTE 2: Lee línea a línea e imprime solo las ejecutadas ---


