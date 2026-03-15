# Solución — Ejercicio C-2

import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("test_log_ts.jsonl")


def _log(payload: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = payload.copy()                          # copia para no mutar el original
    entry["ts"] = datetime.utcnow().isoformat()    # añade timestamp
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def leer_log(path: Path) -> list:
    resultado = []
    with path.open("r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                resultado.append(json.loads(linea))
    return resultado


# Verificación
LOG_PATH.unlink(missing_ok=True)

evento1 = {"room_id": "salon",      "status": "executed"}
evento2 = {"room_id": "dormitorio", "status": "blocked"}

_log(evento1)
_log(evento2)

assert "ts" not in evento1, "Error: modificaste el dict original de evento1"
assert "ts" not in evento2, "Error: modificaste el dict original de evento2"

registros = leer_log(LOG_PATH)

errores = 0
if len(registros) != 2:
    print(f"  [FALLO] Se esperaban 2 registros, hay {len(registros)}")
    errores += 1
else:
    for i, reg in enumerate(registros, 1):
        ok = "ts" in reg and "room_id" in reg
        if not ok:
            errores += 1
        print(f"  [{'OK' if ok else 'FALLO'}] Registro {i}: room_id={reg.get('room_id')}  ts={'presente' if 'ts' in reg else 'AUSENTE'}")

print()
if errores == 0:
    print("Correcto.")
    LOG_PATH.unlink(missing_ok=True)
else:
    print(f"{errores} error(es).")
