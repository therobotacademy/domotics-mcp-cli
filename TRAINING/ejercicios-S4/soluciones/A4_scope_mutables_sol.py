# Solución — Ejercicio A-4

# ─────────────────────────────────────────────
# PARTE 1: Predicciones correctas
# ─────────────────────────────────────────────

def añadir_ts(payload):
    payload["ts"] = "2026-03-22T10:00:00"

evento_a = {"room_id": "salon"}
añadir_ts(evento_a)

prediccion_A = "2026-03-22T10:00:00"  # ← dict mutable: la función SÍ lo modifica
# evento_a["ts"] == "2026-03-22T10:00:00"

def incrementar(x):
    x = x + 1     # x es int (inmutable): se crea una variable LOCAL nueva
    return x

x = 10
incrementar(x)
prediccion_B = 10   # ← x fuera de la función NO cambia (int es inmutable)

def añadir_elemento(lista):
    lista.append(99)

lista_c = [1, 2, 3]
añadir_elemento(lista_c)
prediccion_C = [1, 2, 3, 99]   # ← lista mutable: sí se modifica


# ─────────────────────────────────────────────
# PARTE 2: Función corregida
# ─────────────────────────────────────────────

import json
from pathlib import Path

LOG_PATH = Path("test_scope.jsonl")


def enriquecer_y_loggear(payload: dict, log_path: Path) -> None:
    entry = payload.copy()           # ← COPIA para no mutar el original
    entry["source"] = "agent_v1"    # modificamos la copia, no el original
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# Verificación
LOG_PATH.unlink(missing_ok=True)

print("=== PARTE 1: Predicciones ===")
real_A = evento_a.get("ts", "no existe")
real_B = x
real_C = lista_c

for nombre, pred, real in [
    ("A (evento_a['ts'])", prediccion_A, real_A),
    ("B (x tras incrementar)", str(prediccion_B), str(real_B)),
    ("C (lista_c)", str(prediccion_C), str(real_C)),
]:
    ok = str(pred) == str(real)
    print(f"  [{'OK' if ok else 'FALLO'}] Caso {nombre}: predijiste={pred!r}  real={real!r}")

print("\n=== PARTE 2: Función corregida ===")
evento_original = {"room_id": "salon", "status": "executed"}
copia_antes = dict(evento_original)
enriquecer_y_loggear(evento_original, LOG_PATH)

if evento_original == copia_antes:
    print("  [OK] El dict original no fue modificado.")
else:
    print(f"  [FALLO] Mutación detectada: {evento_original}")

if LOG_PATH.exists():
    with LOG_PATH.open() as f:
        linea = json.loads(f.readline())
    if linea.get("source") == "agent_v1":
        print("  [OK] El fichero contiene 'source: agent_v1'.")
    LOG_PATH.unlink(missing_ok=True)
