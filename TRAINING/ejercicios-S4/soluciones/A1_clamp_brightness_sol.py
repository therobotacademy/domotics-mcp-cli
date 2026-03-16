# Solución — Ejercicio A-1

NIGHT_MAX_BRIGHTNESS = 30


def clamp_brightness(time_bucket: str, brightness: int) -> int:
    if time_bucket == "night":
        return min(brightness, NIGHT_MAX_BRIGHTNESS)
    return max(0, min(brightness, 100))


# Verificación
casos = [
    ("night",     50,  30), ("night",    25,  25), ("night",    -5,   0),
    ("morning",  120, 100), ("morning",  70,  70), ("morning",  -3,   0),
    ("afternoon", 30,  30),
]
errores = 0
for tb, entrada, esperado in casos:
    r = clamp_brightness(tb, entrada)
    ok = r == esperado
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] clamp_brightness({tb!r:12}, {entrada:4}) → {r}  (esperado {esperado})")
print("\nTodos correctos." if errores == 0 else f"{errores} error(es).")
