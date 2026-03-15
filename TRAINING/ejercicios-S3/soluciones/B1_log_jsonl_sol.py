# Solución — Ejercicio B-1

import json

eventos = [
    {"room_id": "salon",      "status": "executed",  "decision": "turn_on"},
    {"room_id": "dormitorio", "status": "noop",       "decision": "do_nothing"},
    {"room_id": "pasillo",    "status": "blocked",    "decision": None},
]

FICHERO = "mi_log.jsonl"

# PARTE 1: Escritura
with open(FICHERO, "w", encoding="utf-8") as f:
    for ev in eventos:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")

print(f"Fichero '{FICHERO}' escrito con {len(eventos)} líneas.")

# PARTE 2: Lectura y filtrado
print("\nHabitaciones con acción ejecutada:")
with open(FICHERO, "r", encoding="utf-8") as f:
    for linea in f:
        datos = json.loads(linea.strip())
        if datos["status"] == "executed":
            print(f"  {datos['room_id']}")
