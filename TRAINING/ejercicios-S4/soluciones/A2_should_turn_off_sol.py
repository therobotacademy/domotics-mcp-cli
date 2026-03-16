# Solución — Ejercicio A-2

from datetime import datetime, timedelta

ABSENCE_OFF_DELAY_MIN = 3


def _parse_ts(ts):
    return datetime.fromisoformat(ts) if ts else None


def should_turn_off_after_absence(room_state: dict) -> bool:
    if room_state["occupied"]:
        return False
    absence_since = _parse_ts(room_state.get("absence_since_ts"))
    now = _parse_ts(room_state["now"])
    if absence_since is None:
        return False
    return now - absence_since >= timedelta(minutes=ABSENCE_OFF_DELAY_MIN)


# Verificación
now = "2026-03-08T21:10:00"
casos = [
    ("Ocupada → False",
     {"occupied": True,  "now": now, "absence_since_ts": None}, False),
    ("Vacía sin ts → False",
     {"occupied": False, "now": now, "absence_since_ts": None}, False),
    ("Vacía 2 min → False",
     {"occupied": False, "now": now, "absence_since_ts": "2026-03-08T21:08:00"}, False),
    ("Vacía 3 min exactos → True",
     {"occupied": False, "now": now, "absence_since_ts": "2026-03-08T21:07:00"}, True),
    ("Vacía 10 min → True",
     {"occupied": False, "now": now, "absence_since_ts": "2026-03-08T21:00:00"}, True),
]
errores = 0
for desc, state, esp in casos:
    r = should_turn_off_after_absence(state)
    ok = r == esp
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")
print("\nTodos correctos." if errores == 0 else f"{errores} error(es).")
