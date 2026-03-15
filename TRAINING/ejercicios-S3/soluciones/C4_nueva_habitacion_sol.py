# Solución — Ejercicio C-4

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
    "cocina": {
        "sensors": {
            "pir_cocina": {"value": 0,     "unit": "bool"},
            "lux_cocina": {"value": 120.0, "unit": "lux"},
        },
        "devices":  {"light_cocina": {"is_on": False, "brightness": 0}},
        "meta":     {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
    },
}


# Verificación (igual que en el fichero del alumno)
def verificar_habitacion(rooms, room_id):
    errores = []
    if room_id not in rooms:
        return [f"'{room_id}' no existe en STATE_AMPLIADO"]
    hab = rooms[room_id]
    sensores = hab.get("sensors", {})
    pir_keys = [k for k in sensores if k.startswith("pir_")]
    lux_keys = [k for k in sensores if k.startswith("lux_")]
    if not pir_keys:
        errores.append("Falta sensor pir_*")
    if not lux_keys:
        errores.append("Falta sensor lux_*")
    if lux_keys and sensores[lux_keys[0]]["value"] != 120.0:
        errores.append(f"lux_cocina debe ser 120.0, es {sensores[lux_keys[0]]['value']}")
    devices = hab.get("devices", {})
    if not devices:
        errores.append("Falta al menos un dispositivo")
    for dev in devices.values():
        if dev.get("is_on") is not False:
            errores.append("El dispositivo debe estar apagado (is_on=False)")
    meta = hab.get("meta", {})
    for campo in ["last_manual_override_ts", "last_action_ts", "absence_since_ts"]:
        if campo not in meta:
            errores.append(f"Falta meta.{campo}")
    return errores


errores = verificar_habitacion(STATE_AMPLIADO, "cocina")
if errores:
    print("FALLO:")
    for e in errores:
        print(f"  - {e}")
else:
    print("[OK] La habitación 'cocina' está bien definida.")
    hab = STATE_AMPLIADO["cocina"]
    pir_key = next(k for k in hab["sensors"] if k.startswith("pir_"))
    lux_key = next(k for k in hab["sensors"] if k.startswith("lux_"))
    print(f"[OK] world_model encuentra pir → '{pir_key}' y lux → '{lux_key}'")


# =============================================================================
# RESPUESTAS A PARTE 2
# =============================================================================

# P1: ¿Necesitas modificar world_model.py?
# R: NO. world_model.py usa startswith("pir_") y startswith("lux_") para
#    localizar los sensores, por lo que funciona con cualquier nombre que
#    siga el patrón. Solo hay que añadir la habitación en STATE de server.py.

# P2: ¿Qué endpoint devuelve la lista de habitaciones?
# R: GET /describe_home  (server.py líneas 119-130)
#    Recorre STATE["rooms"] y devuelve lista de {room_id, sensors, actuators}.

# P3: Con lux_cocina=120 y presencia, ¿qué decisión toma el planner?
# R: "do_nothing"
#    120 NO es < LUX_ON_THRESHOLD (80) → no enciende.
#    120 NO es >= LUX_OFF_THRESHOLD (200) → no apaga.
#    Resultado: la luz ya está bien sin intervención del agente.
