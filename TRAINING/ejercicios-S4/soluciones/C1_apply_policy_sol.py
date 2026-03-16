# Solución — Ejercicio C-1

from datetime import datetime, timedelta

MANUAL_OVERRIDE_WINDOW_MIN = 10
ROOM_COOLDOWN_SEC          = 60


def _parse_ts(ts):
    return datetime.fromisoformat(ts) if ts else None


def apply_policy(room_state: dict) -> dict:
    now           = _parse_ts(room_state["now"])
    last_override = _parse_ts(room_state.get("last_manual_override_ts"))
    last_action   = _parse_ts(room_state.get("last_action_ts"))

    if last_override and now - last_override < timedelta(minutes=MANUAL_OVERRIDE_WINDOW_MIN):
        return {"allowed": False, "reason": "manual_override_window"}

    if last_action and now - last_action < timedelta(seconds=ROOM_COOLDOWN_SEC):
        return {"allowed": False, "reason": "cooldown"}

    return {"allowed": True, "reason": "ok"}


# Verificación
now = "2026-03-08T21:10:00"
casos = [
    ("Sin override ni cooldown → permitido",
     {"now": now, "last_manual_override_ts": None,                    "last_action_ts": None},
     {"allowed": True,  "reason": "ok"}),
    ("Override hace 5 min → bloqueado",
     {"now": now, "last_manual_override_ts": "2026-03-08T21:05:00",   "last_action_ts": None},
     {"allowed": False, "reason": "manual_override_window"}),
    ("Override hace 11 min → permitido",
     {"now": now, "last_manual_override_ts": "2026-03-08T20:59:00",   "last_action_ts": None},
     {"allowed": True,  "reason": "ok"}),
    ("Cooldown 30 seg → bloqueado",
     {"now": now, "last_manual_override_ts": None,                    "last_action_ts": "2026-03-08T21:09:30"},
     {"allowed": False, "reason": "cooldown"}),
    ("Cooldown expirado → permitido",
     {"now": now, "last_manual_override_ts": None,                    "last_action_ts": "2026-03-08T21:08:00"},
     {"allowed": True,  "reason": "ok"}),
    ("Override Y cooldown → override primero",
     {"now": now, "last_manual_override_ts": "2026-03-08T21:05:00",   "last_action_ts": "2026-03-08T21:09:30"},
     {"allowed": False, "reason": "manual_override_window"}),
]
errores = 0
for desc, state, esp in casos:
    r = apply_policy(state)
    ok = r == esp
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")
    if not ok: print(f"          → {r}  esperado {esp}")
print("\nTodos correctos." if errores == 0 else f"{errores} error(es).")
