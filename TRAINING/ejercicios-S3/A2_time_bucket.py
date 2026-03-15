# =============================================================================
# Ejercicio A-2 — Clasificar la hora del día  ★☆☆
# Bloque A · T03 Cadenas de caracteres
# =============================================================================
#
# CONTEXTO:
#   Esta es EXACTAMENTE la función get_time_bucket de world_model.py (líneas 7-14).
#   Recibe un timestamp en formato ISO (string) y devuelve uno de tres valores:
#     "morning"   → si la hora está entre  7:00 y 11:59
#     "afternoon" → si la hora está entre 12:00 y 19:59
#     "night"     → cualquier otra hora (20:00-6:59)
#
#   El agente usa este valor ("time_bucket") para decidir qué brillo aplicar:
#   por la noche nunca más de 30 de brillo (política NIGHT_MAX_BRIGHTNESS).
#
# TAREA:
#   Completa el cuerpo de la función. No cambies la firma.
#
# COMPROBACIÓN AUTOMÁTICA:
#   Si tu implementación es correcta, al ejecutar el script no habrá errores.
# =============================================================================

from datetime import datetime


def get_time_bucket(ts: str) -> str:
    """Dado un timestamp ISO, devuelve 'morning', 'afternoon' o 'night'."""
    now = datetime.fromisoformat(ts)
    h = now.hour

    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
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
if errores == 0:
    print("Todos los casos correctos.")
else:
    print(f"{errores} caso(s) incorrecto(s). Revisa la lógica.")
