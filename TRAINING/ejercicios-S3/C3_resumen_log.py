# =============================================================================
# Ejercicio C-3 — Leer el log real y resumir decisiones  ★★☆
# Bloque C · Comprensión del código Domotics-MCP-cli
# =============================================================================
#
# CONTEXTO:
#   Después de ejecutar run_demo.py, el agente habrá escrito sus decisiones
#   en Domotics-MCP-cli/data/agent_log.jsonl.
#
#   Cada línea tiene un campo "status" con uno de estos valores:
#     "executed"  → el agente tomó una acción (plan con decisión turn_on/turn_off)
#     "noop"      → el agente decidió no hacer nada (do_nothing)
#     "blocked"   → la política bloqueó al agente (override reciente, cooldown...)
#     "learned_preference" → el agente actualizó una preferencia
#
#   Cuando status es "executed" o "noop", el campo "plan.decision" indica
#   qué decisión tomó el planner.
#
# TAREA:
#   Implementa la función resumir_log(path) que:
#     1. Lee el fichero línea a línea.
#     2. Cuenta las ocurrencias de cada (status, decision).
#        - Si status es "executed" o "noop", decision = plan["decision"]
#        - Si status es "blocked" o "learned_preference", decision = "-"
#     3. Devuelve un dict  { "turn_on": n, "turn_off": n, ... }
#        usando la decision como clave (o el status si no hay decision).
#
#   Luego imprime el resumen ordenado.
#
# SALIDA ESPERADA (los números dependen de la ejecución de run_demo.py):
#   turn_on            : 2
#   do_nothing         : 4
#   blocked            : 1
#   learned_preference : 1
#   (o similar según tu run_demo)
#
# NOTA:
#   Si aún no has ejecutado run_demo.py, el script usa un log de ejemplo
#   incluido a continuación para que puedas probar tu implementación.
# =============================================================================

import json
from pathlib import Path
from collections import defaultdict

LOG_REAL  = Path("../../../Domotics-MCP-cli/data/agent_log.jsonl")
LOG_DEMO  = Path("datos_demo/agent_log_ejemplo.jsonl")   # fallback incluido


def resumir_log(path: Path) -> dict:
    """Lee un log JSONL y devuelve conteo de decisiones."""
    conteo = defaultdict(int)

    # --- ESCRIBE TU CÓDIGO AQUÍ ---

    return dict(conteo)


# --- NO MODIFICAR DESDE AQUÍ ---
# Elige el fichero: el real si existe, el de ejemplo si no.
log_path = LOG_REAL if LOG_REAL.exists() else LOG_DEMO
print(f"Leyendo: {log_path}\n")

resumen = resumir_log(log_path)

if not resumen:
    print("El log está vacío o no se pudo leer.")
else:
    print(f"{'Decisión / Estado':<25} {'N':>5}")
    print("-" * 32)
    for clave, n in sorted(resumen.items(), key=lambda x: -x[1]):
        print(f"  {clave:<23} {n:>5}")
    print("-" * 32)
    print(f"  {'TOTAL':<23} {sum(resumen.values()):>5}")
