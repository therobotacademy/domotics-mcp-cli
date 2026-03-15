# =============================================================================
# Ejercicio C-1 — Trazar a mano un ciclo del agente  ★☆☆
# Bloque C · Comprensión del código Domotics-MCP-cli
# =============================================================================
#
# CONTEXTO:
#   Antes de ejecutar run_demo.py, intenta predecir qué hará el agente.
#   Leer el código y razonar sobre él es más valioso que ejecutarlo sin entender.
#
#   Archivos a consultar:
#     - agent/world_model.py   → get_time_bucket, build_room_state
#     - agent/planner.py       → LightingPlanner.plan  (umbrales LUX_ON=80, LUX_OFF=200)
#     - agent/policy.py        → NIGHT_MAX_BRIGHTNESS = 30
#     - agent/preferences.py   → DEFAULT_PREFS = {morning:60, afternoon:70, night:25}
#
# ESTADO DEL SERVIDOR en este momento:
#   Habitación: salon
#   Timestamp:  "2026-03-08T21:00:00"
#   pir_salon:  1   (hay presencia)
#   lux_salon:  35.0 lux
#   Luz:        apagada (is_on=False, brightness=0)
#   Sin overrides recientes
#
# TAREA:
#   Sin ejecutar el agente, rellena las variables de abajo con el valor
#   que crees que tendrán en cada paso del ciclo.
#   Luego ejecuta el script: calculará las respuestas reales y comparará.
#
# =============================================================================

from datetime import datetime

# ---- TUS PREDICCIONES (modifica estos valores) ----

mi_time_bucket = "???"          # "morning", "afternoon" o "night"
mi_occupied    = None           # True o False
mi_lux_menor_umbral = None      # ¿35.0 < 80?  → True o False
mi_decision    = "???"          # "turn_on", "turn_off" o "do_nothing"
mi_brightness  = 0              # brillo que el agente ordenará (0 si apaga)

# ---------------------------------------------------


# --- CÁLCULO REAL (no modificar) ---
def get_time_bucket(ts):
    h = datetime.fromisoformat(ts).hour
    if 7 <= h < 12:   return "morning"
    if 12 <= h < 20:  return "afternoon"
    return "night"

NIGHT_MAX_BRIGHTNESS = 30
DEFAULT_PREFS = {"morning": 60, "afternoon": 70, "night": 25}
LUX_ON_THRESHOLD  = 80.0
LUX_OFF_THRESHOLD = 200.0

ts      = "2026-03-08T21:00:00"
pir     = 1
lux     = 35.0
is_on   = False

real_time_bucket = get_time_bucket(ts)
real_occupied    = pir > 0
real_lux_menor   = lux < LUX_ON_THRESHOLD

pref_brillo = DEFAULT_PREFS[real_time_bucket]
real_brightness = min(pref_brillo, NIGHT_MAX_BRIGHTNESS) if real_time_bucket == "night" else pref_brillo

if not real_occupied:
    real_decision = "do_nothing"
elif lux >= LUX_OFF_THRESHOLD and is_on:
    real_decision = "turn_off"
    real_brightness = 0
elif lux < LUX_ON_THRESHOLD:
    if not is_on or abs(0 - real_brightness) >= 10:
        real_decision = "turn_on"
    else:
        real_decision = "do_nothing"
        real_brightness = 0
else:
    real_decision = "do_nothing"
    real_brightness = 0

# --- COMPARACIÓN ---
print("=" * 55)
print("COMPARACIÓN: tu predicción vs valor real")
print("=" * 55)
checks = [
    ("time_bucket",       mi_time_bucket,       real_time_bucket),
    ("occupied",          mi_occupied,           real_occupied),
    ("lux < umbral (80)", mi_lux_menor_umbral,   real_lux_menor),
    ("decision",          mi_decision,           real_decision),
    ("brightness",        mi_brightness,         real_brightness),
]
errores = 0
for nombre, tuyo, real in checks:
    ok = tuyo == real
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {nombre:22} tuyo={str(tuyo):12} real={real}")

print()
if errores == 0:
    print("Prediccion perfecta. Comprendes el ciclo del agente.")
else:
    print(f"{errores} prediccion(es) incorrecta(s). Revisa los archivos indicados.")
