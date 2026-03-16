# =============================================================================
# Ejercicio C-4 — Añadir GET /status al servidor  ★★★
# Bloque C · Policy + Executor + Servidor
# =============================================================================
#
# CONTEXTO:
#   El servidor FastAPI expone sus endpoints mediante decoradores @app.get()
#   y @app.post(). Añadir uno nuevo es tan sencillo como definir una función
#   y decorarla.
#
#   El patrón es siempre:
#     @app.get("/mi_ruta")
#     def mi_funcion():
#         return { ... }   # FastAPI serializa el dict a JSON automáticamente
#
# TAREA — PARTE 1 (aquí, sin tocar server.py):
#   Implementa la función get_status(state) que calcula el resumen.
#   Recibe el dict STATE del servidor y devuelve:
#     {
#       "now":          "2026-03-08T21:00:00",   ← isoformat del tiempo actual
#       "total_rooms":  3,                        ← número de habitaciones
#       "total_events": 7,                        ← número de eventos registrados
#       "rooms": {
#         "salon":      {"sensors": 2, "devices": 1},
#         "dormitorio": {"sensors": 2, "devices": 1},
#         ...
#       }
#     }
#
# TAREA — PARTE 2 (instrucciones en comentario al final):
#   Explica qué líneas añadirías en mcp_server/server.py para que
#   este endpoint sea accesible en http://127.0.0.1:8000/status
#
# COMPROBACIÓN AUTOMÁTICA al ejecutar el script.
# =============================================================================

from datetime import datetime

# Copia del STATE del servidor para el ejercicio (no importamos server.py)
STATE_EJEMPLO = {
    "now": datetime(2026, 3, 8, 21, 7, 0),
    "rooms": {
        "salon": {
            "sensors": {"pir_salon": {}, "lux_salon": {}},
            "devices": {"light_salon_main": {}},
            "meta":    {},
        },
        "dormitorio": {
            "sensors": {"pir_bedroom": {}, "lux_bedroom": {}},
            "devices": {"light_bedroom_main": {}},
            "meta":    {},
        },
        "pasillo": {
            "sensors": {"pir_hall": {}, "lux_hall": {}},
            "devices": {"light_hall": {}},
            "meta":    {},
        },
    },
    "events": [
        {"kind": "sensor_update"}, {"kind": "sensor_update"},
        {"kind": "set_light"},     {"kind": "time_advanced"},
        {"kind": "manual_override"},{"kind": "sensor_update"},
        {"kind": "set_light"},
    ],
}


def get_status(state: dict) -> dict:
    """
    Calcula el resumen del estado del servidor.
    Devuelve el dict descrito en la TAREA PARTE 1.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
resultado = get_status(STATE_EJEMPLO)

errores = 0
checks = [
    ("now es string ISO",        isinstance(resultado.get("now"), str) and "T" in resultado.get("now", "")),
    ("total_rooms == 3",         resultado.get("total_rooms") == 3),
    ("total_events == 7",        resultado.get("total_events") == 7),
    ("rooms contiene salon",     "salon" in resultado.get("rooms", {})),
    ("salon.sensors == 2",       resultado.get("rooms", {}).get("salon", {}).get("sensors") == 2),
    ("salon.devices == 1",       resultado.get("rooms", {}).get("salon", {}).get("devices") == 1),
    ("pasillo.sensors == 2",     resultado.get("rooms", {}).get("pasillo", {}).get("sensors") == 2),
]
for desc, ok in checks:
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")

if resultado:
    print(f"\n  Resultado completo: {resultado}")

print()
print("get_status() correcta." if errores == 0 else f"{errores} check(s) fallido(s).")


# =============================================================================
# PARTE 2 — Instrucciones para integrar en server.py
# =============================================================================
# Escribe aquí las líneas que añadirías en mcp_server/server.py
# para exponer esta función como GET /status.
#
# PISTA: sólo necesitas el decorador y llamar a get_status(STATE).
# Recuerda que STATE en server.py es el dict global del módulo,
# y que STATE["now"] es un objeto datetime, no un string.
#
# R:
#
#   @app.get("/status")
#   def ...
