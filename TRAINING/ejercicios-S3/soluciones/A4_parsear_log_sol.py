# Solución — Ejercicio A-4

import json

lineas_log = [
    '{"room_id": "salon",      "status": "executed", "plan": {"decision": "turn_on",    "reason": "Presencia con poca luz."}}',
    '{"room_id": "dormitorio", "status": "noop",     "plan": {"decision": "do_nothing", "reason": "Iluminacion correcta."}}',
    '{"room_id": "pasillo",    "status": "blocked",  "policy_reason": "Override reciente"}',
]

for linea in lineas_log:
    datos    = json.loads(linea)
    sala     = datos["room_id"]
    estado   = datos["status"]
    decision = datos.get("plan", {}).get("decision", "-")
    print(f"Sala: {sala:<12} | Estado: {estado:<8} | Decisión: {decision}")
