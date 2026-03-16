# =============================================================================
# Ejercicio C-1 — Implementar apply_policy  ★★☆
# Bloque C · Policy + Executor + Servidor
# =============================================================================
#
# CONTEXTO:
#   Esta es la función apply_policy de policy.py (líneas 16-27).
#   El agente la llama antes de planificar cada habitación.
#   Devuelve {"allowed": True/False, "reason": "..."}.
#
#   Dos condiciones bloquean al agente:
#   1. Override manual reciente: si el usuario ajustó la luz manualmente
#      hace menos de MANUAL_OVERRIDE_WINDOW_MIN (10) minutos, el agente
#      respeta esa decisión y no interfiere.
#   2. Cooldown: si el agente mismo actuó hace menos de ROOM_COOLDOWN_SEC (60)
#      segundos, no vuelve a actuar (evita oscilaciones rápidas).
#   Si ninguna condición se cumple, devuelve allowed=True.
#
# NOTA sobre timedelta:
#   from datetime import timedelta
#   timedelta(minutes=10)  → representa 10 minutos como duración
#   timedelta(seconds=60)  → representa 60 segundos
#   (ahora - ts_pasado) < timedelta(minutes=10)  → True si pasaron < 10 min
#
# COMPROBACIÓN AUTOMÁTICA al ejecutar el script.
# =============================================================================

from datetime import datetime, timedelta

MANUAL_OVERRIDE_WINDOW_MIN = 10
ROOM_COOLDOWN_SEC          = 60


def _parse_ts(ts):
    return datetime.fromisoformat(ts) if ts else None


def apply_policy(room_state: dict) -> dict:
    """
    Evalúa si el agente tiene permitido actuar en esta habitación.
    Devuelve {"allowed": bool, "reason": str}.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
now = "2026-03-08T21:10:00"

casos = [
    (
        "Sin override ni cooldown → permitido",
        {"now": now, "last_manual_override_ts": None, "last_action_ts": None},
        {"allowed": True, "reason": "ok"},
    ),
    (
        "Override hace 5 min (< 10) → bloqueado",
        {"now": now, "last_manual_override_ts": "2026-03-08T21:05:00", "last_action_ts": None},
        {"allowed": False, "reason": "manual_override_window"},
    ),
    (
        "Override hace 11 min (> 10) → permitido",
        {"now": now, "last_manual_override_ts": "2026-03-08T20:59:00", "last_action_ts": None},
        {"allowed": True, "reason": "ok"},
    ),
    (
        "Acción hace 30 seg (< 60) → cooldown",
        {"now": now, "last_manual_override_ts": None, "last_action_ts": "2026-03-08T21:09:30"},
        {"allowed": False, "reason": "cooldown"},
    ),
    (
        "Acción hace 2 min (> 60 seg) → permitido",
        {"now": now, "last_manual_override_ts": None, "last_action_ts": "2026-03-08T21:08:00"},
        {"allowed": True, "reason": "ok"},
    ),
    (
        "Override reciente Y acción reciente → override tiene prioridad",
        {"now": now,
         "last_manual_override_ts": "2026-03-08T21:05:00",
         "last_action_ts":          "2026-03-08T21:09:30"},
        {"allowed": False, "reason": "manual_override_window"},
    ),
]

errores = 0
for desc, state, esperado in casos:
    resultado = apply_policy(state)
    ok = resultado == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}")
    if not ok:
        print(f"          → obtenido  {resultado}")
        print(f"          → esperado  {esperado}")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
