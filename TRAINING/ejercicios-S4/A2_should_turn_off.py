# =============================================================================
# Ejercicio A-2 — Implementar should_turn_off_after_absence  ★★☆
# Bloque A · T05 Funciones
# =============================================================================
#
# CONTEXTO:
#   Esta es la función should_turn_off_after_absence de policy.py (líneas 30-37).
#   El agente NO apaga la luz en cuanto detecta que una habitación queda vacía.
#   Espera ABSENCE_OFF_DELAY_MIN minutos (3) antes de decidir apagar.
#   Esto evita apagar la luz si alguien sale un momento y vuelve enseguida.
#
# LÓGICA:
#   1. Si la habitación está ocupada → devuelve False (no hay que apagar).
#   2. Si no hay timestamp de ausencia registrado → devuelve False
#      (acabamos de detectar la ausencia, aún no ha empezado el contador).
#   3. Si la ausencia dura >= ABSENCE_OFF_DELAY_MIN minutos → True (apagar ya).
#   4. Si aún no ha pasado ese tiempo → False (esperar más).
#
# NOTA sobre _parse_ts:
#   Es una función auxiliar (privada, por eso empieza con _) que convierte
#   un string ISO o None en datetime o None. Ya está implementada: úsala.
#
# COMPROBACIÓN AUTOMÁTICA al ejecutar el script.
# =============================================================================

from datetime import datetime, timedelta

ABSENCE_OFF_DELAY_MIN = 3


def _parse_ts(ts):
    """Convierte string ISO a datetime, o None si ts es None."""
    return datetime.fromisoformat(ts) if ts else None


def should_turn_off_after_absence(room_state: dict) -> bool:
    """
    Devuelve True si la habitación lleva ausente suficiente tiempo
    como para apagar la luz.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
now = "2026-03-08T21:10:00"

casos = [
    # descripción, room_state, esperado
    (
        "Ocupada → no apagar",
        {"occupied": True,  "now": now, "absence_since_ts": None},
        False
    ),
    (
        "Vacía, sin timestamp de ausencia → no apagar",
        {"occupied": False, "now": now, "absence_since_ts": None},
        False
    ),
    (
        "Vacía 2 min (< 3) → no apagar todavía",
        {"occupied": False, "now": now,
         "absence_since_ts": "2026-03-08T21:08:00"},
        False
    ),
    (
        "Vacía exactamente 3 min → apagar",
        {"occupied": False, "now": now,
         "absence_since_ts": "2026-03-08T21:07:00"},
        True
    ),
    (
        "Vacía 10 min → apagar",
        {"occupied": False, "now": now,
         "absence_since_ts": "2026-03-08T21:00:00"},
        True
    ),
]

errores = 0
for desc, state, esperado in casos:
    resultado = should_turn_off_after_absence(state)
    ok = resultado == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")
    if not ok:
        print(f"          → obtenido {resultado}, esperado {esperado}")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
