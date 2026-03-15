# Solución — Ejercicio C-3

import json
from pathlib import Path
from collections import defaultdict

LOG_REAL = Path("../../../Domotics-MCP-cli/data/agent_log.jsonl")
LOG_DEMO = Path("datos_demo/agent_log_ejemplo.jsonl")


def resumir_log(path: Path) -> dict:
    conteo = defaultdict(int)
    with path.open("r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            datos  = json.loads(linea)
            status = datos.get("status", "unknown")
            if status in ("executed", "noop"):
                clave = datos.get("plan", {}).get("decision", "unknown")
            else:
                clave = status
            conteo[clave] += 1
    return dict(conteo)


# Selección del fichero
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
