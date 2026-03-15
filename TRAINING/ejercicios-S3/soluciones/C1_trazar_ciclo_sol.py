# Solución — Ejercicio C-1

from datetime import datetime

# Predicciones correctas
mi_time_bucket      = "night"
mi_occupied         = True
mi_lux_menor_umbral = True    # 35.0 < 80
mi_decision         = "turn_on"
mi_brightness       = 25      # DEFAULT_PREFS["night"]=25, NIGHT_MAX=30 → min(25,30)=25


# Cálculo real (igual que en el fichero del alumno)
def get_time_bucket(ts):
    h = datetime.fromisoformat(ts).hour
    if 7 <= h < 12:   return "morning"
    if 12 <= h < 20:  return "afternoon"
    return "night"

NIGHT_MAX_BRIGHTNESS = 30
DEFAULT_PREFS        = {"morning": 60, "afternoon": 70, "night": 25}
LUX_ON_THRESHOLD     = 80.0
LUX_OFF_THRESHOLD    = 200.0

ts   = "2026-03-08T21:00:00"
pir  = 1
lux  = 35.0
is_on = False

real_time_bucket = get_time_bucket(ts)
real_occupied    = pir > 0
real_lux_menor   = lux < LUX_ON_THRESHOLD
pref_brillo      = DEFAULT_PREFS[real_time_bucket]
real_brightness  = min(pref_brillo, NIGHT_MAX_BRIGHTNESS)

if not real_occupied:
    real_decision = "do_nothing"
elif lux >= LUX_OFF_THRESHOLD and is_on:
    real_decision   = "turn_off"
    real_brightness = 0
elif lux < LUX_ON_THRESHOLD:
    real_decision = "turn_on"
else:
    real_decision   = "do_nothing"
    real_brightness = 0

checks = [
    ("time_bucket",       mi_time_bucket,       real_time_bucket),
    ("occupied",          mi_occupied,           real_occupied),
    ("lux < umbral (80)", mi_lux_menor_umbral,   real_lux_menor),
    ("decision",          mi_decision,           real_decision),
    ("brightness",        mi_brightness,         real_brightness),
]

print("=" * 55)
print("COMPARACIÓN: predicción vs valor real")
print("=" * 55)
errores = 0
for nombre, tuyo, real in checks:
    ok = tuyo == real
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {nombre:22} tuyo={str(tuyo):12} real={real}")

print()
print("Prediccion perfecta." if errores == 0 else f"{errores} error(es).")
