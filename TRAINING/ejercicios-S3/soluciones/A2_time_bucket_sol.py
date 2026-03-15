# Solución — Ejercicio A-2

from datetime import datetime


def get_time_bucket(ts: str) -> str:
    now = datetime.fromisoformat(ts)
    h = now.hour
    if 7 <= h < 12:
        return "morning"
    if 12 <= h < 20:
        return "afternoon"
    return "night"


# Verificación
casos = [
    ("2026-03-08T21:00:00", "night"),
    ("2026-03-08T09:30:00", "morning"),
    ("2026-03-08T15:00:00", "afternoon"),
    ("2026-03-08T07:00:00", "morning"),
    ("2026-03-08T19:59:00", "afternoon"),
    ("2026-03-08T06:59:00", "night"),
    ("2026-03-08T00:00:00", "night"),
]

errores = 0
for ts, esperado in casos:
    resultado = get_time_bucket(ts)
    estado = "OK" if resultado == esperado else "FALLO"
    if estado == "FALLO":
        errores += 1
    print(f"  [{estado}] get_time_bucket('{ts}') → '{resultado}'  (esperado: '{esperado}')")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
