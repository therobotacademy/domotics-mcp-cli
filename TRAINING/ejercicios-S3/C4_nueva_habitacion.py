# =============================================================================
# Ejercicio C-4 — Añadir una habitación nueva al servidor  ★★★
# Bloque C · Comprensión del código Domotics-MCP-cli
# =============================================================================
#
# CONTEXTO:
#   El estado del servidor MCP se define en el diccionario STATE de
#   mcp_server/server.py. Cada habitación sigue exactamente esta estructura:
#
#     "nombre_habitacion": {
#         "sensors": {
#             "pir_nombre":  {"value": 0,     "unit": "bool"},
#             "lux_nombre":  {"value": 0.0,   "unit": "lux"},
#         },
#         "devices": {
#             "light_nombre": {"is_on": False, "brightness": 0}
#         },
#         "meta": {
#             "last_manual_override_ts": None,
#             "last_action_ts":          None,
#             "absence_since_ts":        None,
#         },
#     }
#
# TAREA — PARTE 1 (aquí, en este fichero):
#   Añade la habitación "cocina" al diccionario STATE_AMPLIADO de abajo.
#   Valores iniciales:
#     - pir_cocina:   0
#     - lux_cocina:   120.0 lux  (cocina bien iluminada de día)
#     - light_cocina: apagada
#
# TAREA — PARTE 2 (respuesta en comentario al final):
#   Responde las preguntas de comprensión sin modificar server.py todavía.
#
# COMPROBACIÓN AUTOMÁTICA al final del script.
# =============================================================================

STATE_AMPLIADO = {
    "salon": {
        "sensors": {
            "pir_salon": {"value": 0,     "unit": "bool"},
            "lux_salon": {"value": 180.0, "unit": "lux"},
        },
        "devices":  {"light_salon_main": {"is_on": False, "brightness": 0}},
        "meta":     {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
    },
    "dormitorio": {
        "sensors": {
            "pir_bedroom": {"value": 0,    "unit": "bool"},
            "lux_bedroom": {"value": 60.0, "unit": "lux"},
        },
        "devices":  {"light_bedroom_main": {"is_on": False, "brightness": 0}},
        "meta":     {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
    },
    "pasillo": {
        "sensors": {
            "pir_hall": {"value": 0,    "unit": "bool"},
            "lux_hall": {"value": 25.0, "unit": "lux"},
        },
        "devices":  {"light_hall": {"is_on": False, "brightness": 0}},
        "meta":     {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
    },

    # --- AÑADE LA HABITACIÓN "cocina" AQUÍ ---

}


# --- NO MODIFICAR DESDE AQUÍ ---
def verificar_habitacion(rooms, room_id):
    errores = []
    if room_id not in rooms:
        return [f"'{room_id}' no existe en STATE_AMPLIADO"]

    hab = rooms[room_id]

    # Sensores esperados
    sensores = hab.get("sensors", {})
    pir_keys = [k for k in sensores if k.startswith("pir_")]
    lux_keys = [k for k in sensores if k.startswith("lux_")]
    if not pir_keys:
        errores.append("Falta sensor pir_*")
    if not lux_keys:
        errores.append("Falta sensor lux_*")
    if lux_keys and sensores[lux_keys[0]]["value"] != 120.0:
        errores.append(f"lux_cocina debe ser 120.0, es {sensores[lux_keys[0]]['value']}")

    # Dispositivos
    devices = hab.get("devices", {})
    if not devices:
        errores.append("Falta al menos un dispositivo")
    for dev in devices.values():
        if dev.get("is_on") is not False:
            errores.append("El dispositivo debe estar apagado (is_on=False)")

    # Meta
    meta = hab.get("meta", {})
    for campo in ["last_manual_override_ts", "last_action_ts", "absence_since_ts"]:
        if campo not in meta:
            errores.append(f"Falta meta.{campo}")

    return errores


errores = verificar_habitacion(STATE_AMPLIADO, "cocina")
if errores:
    print("FALLO en la habitación 'cocina':")
    for e in errores:
        print(f"  - {e}")
else:
    print("[OK] La habitación 'cocina' está bien definida.")
    print()
    print("Verificando que world_model NO necesita cambios...")
    # Simula lo que hace world_model.py para encontrar sensores
    hab = STATE_AMPLIADO["cocina"]
    try:
        pir_key = next(k for k in hab["sensors"] if k.startswith("pir_"))
        lux_key = next(k for k in hab["sensors"] if k.startswith("lux_"))
        print(f"[OK] world_model encuentra pir → '{pir_key}' y lux → '{lux_key}'")
        print("     Conclusión: world_model usa startswith(), funciona con cualquier nombre.")
    except StopIteration:
        print("[FALLO] world_model no puede encontrar los sensores con startswith()")


# =============================================================================
# PARTE 2 — Preguntas de comprensión (escribe tus respuestas en los comentarios)
# =============================================================================

# P1: ¿Necesitas modificar world_model.py para que funcione con la cocina?
#     ¿Por qué sí o por qué no?
# R:

# P2: ¿Qué endpoint del servidor devuelve la lista de habitaciones?
#     (Mira server.py líneas 119-130)
# R:

# P3: Si lux_cocina = 120 y hay presencia, ¿qué decisión tomará el planner?
#     (Pista: LUX_ON_THRESHOLD=80, LUX_OFF_THRESHOLD=200)
# R:
