# Solución — Ejercicio C-4

from datetime import datetime


STATE_EJEMPLO = {
    "now": datetime(2026, 3, 8, 21, 7, 0),
    "rooms": {
        "salon":      {"sensors": {"pir_salon": {}, "lux_salon": {}},
                       "devices": {"light_salon_main": {}}, "meta": {}},
        "dormitorio": {"sensors": {"pir_bedroom": {}, "lux_bedroom": {}},
                       "devices": {"light_bedroom_main": {}}, "meta": {}},
        "pasillo":    {"sensors": {"pir_hall": {}, "lux_hall": {}},
                       "devices": {"light_hall": {}}, "meta": {}},
    },
    "events": [{}] * 7,
}


def get_status(state: dict) -> dict:
    rooms_summary = {}
    for room_id, room in state["rooms"].items():
        rooms_summary[room_id] = {
            "sensors": len(room["sensors"]),
            "devices": len(room["devices"]),
        }
    return {
        "now":          state["now"].isoformat(),
        "total_rooms":  len(state["rooms"]),
        "total_events": len(state["events"]),
        "rooms":        rooms_summary,
    }


# Verificación
resultado = get_status(STATE_EJEMPLO)
checks = [
    ("now es string ISO",    isinstance(resultado.get("now"), str) and "T" in resultado.get("now", "")),
    ("total_rooms == 3",     resultado.get("total_rooms") == 3),
    ("total_events == 7",    resultado.get("total_events") == 7),
    ("rooms tiene salon",    "salon" in resultado.get("rooms", {})),
    ("salon.sensors == 2",   resultado["rooms"]["salon"]["sensors"] == 2),
    ("salon.devices == 1",   resultado["rooms"]["salon"]["devices"] == 1),
]
errores = 0
for desc, ok in checks:
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")
print("\nTodos correctos." if errores == 0 else f"{errores} error(es).")


# ─────────────────────────────────────────────
# PARTE 2: Líneas a añadir en mcp_server/server.py
# ─────────────────────────────────────────────
#
# Al final del fichero server.py, después del endpoint /events:
#
#   @app.get("/status")
#   def status():
#       rooms_summary = {}
#       for room_id, room in STATE["rooms"].items():
#           rooms_summary[room_id] = {
#               "sensors": len(room["sensors"]),
#               "devices": len(room["devices"]),
#           }
#       return {
#           "now":          STATE["now"].isoformat(),
#           "total_rooms":  len(STATE["rooms"]),
#           "total_events": len(STATE["events"]),
#           "rooms":        rooms_summary,
#       }
#
# Nota: STATE["now"] es datetime → .isoformat() para convertir a string JSON.
# No hay que importar nada nuevo: FastAPI y STATE ya están en el módulo.
