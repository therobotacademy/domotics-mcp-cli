# =============================================================================
# Ejercicio A-4 — Parsear una línea de log JSONL  ★★☆
# Bloque A · T03 Cadenas de caracteres
# =============================================================================
#
# CONTEXTO:
#   El agente escribe cada decisión como una línea de texto JSON
#   en data/agent_log.jsonl. Cada línea es una cadena que contiene
#   un objeto JSON completo. Para procesar el log necesitamos:
#     1. Convertir la cadena en diccionario Python  →  json.loads()
#     2. Navegar por el diccionario para extraer los campos que nos interesan.
#
#   Ejemplo de línea real:
#     {"room_id": "salon", "status": "executed", "plan": {"decision": "turn_on",
#      "reason": "Presence detected with low ambient light (35.0 lux)."}}
#
# TAREA:
#   Para CADA línea del log de ejemplo:
#     1. Conviértela en diccionario con json.loads()
#     2. Extrae: room_id, status, y la decision dentro de plan (si existe).
#        Si "plan" no está en el diccionario, usa la cadena "-" como decisión.
#     3. Imprime el resultado con el formato:
#          Sala: salon      | Estado: executed | Decisión: turn_on
#
# SALIDA ESPERADA:
#   Sala: salon       | Estado: executed | Decisión: turn_on
#   Sala: dormitorio  | Estado: noop     | Decisión: do_nothing
#   Sala: pasillo     | Estado: blocked  | Decisión: -
# =============================================================================

import json

lineas_log = [
    '{"room_id": "salon",      "status": "executed", "plan": {"decision": "turn_on",    "reason": "Presencia con poca luz."}}',
    '{"room_id": "dormitorio", "status": "noop",     "plan": {"decision": "do_nothing", "reason": "Iluminacion correcta."}}',
    '{"room_id": "pasillo",    "status": "blocked",  "policy_reason": "Override reciente"}',
]

# --- ESCRIBE TU CÓDIGO AQUÍ ---


