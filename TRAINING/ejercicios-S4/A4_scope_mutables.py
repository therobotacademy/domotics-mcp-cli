# =============================================================================
# Ejercicio A-4 — Alcance y mutables: la trampa del dict  ★★★
# Bloque A · T05 Funciones
# =============================================================================
#
# CONTEXTO:
#   En la sesión 3 (Ejercicio C-2) implementaste _log() usando payload.copy()
#   para no modificar el dict original. Ahora vamos a ENTENDER por qué.
#
#   En Python, cuando pasas un dict (o lista) a una función, no se copia:
#   la función recibe una referencia al MISMO objeto en memoria.
#   Esto se llama "paso por referencia" para objetos mutables.
#   Los tipos inmutables (int, str, float) sí se pasan por valor.
#
# TAREA — PARTE 1: predecir el comportamiento
#   Lee cada bloque de código y escribe tu predicción en la variable
#   correspondiente ANTES de ejecutar el script.
#
# TAREA — PARTE 2: corregir la función buggy
#   La función enriquecer_y_loggear tiene un bug: modifica el dict original.
#   Corrígela para que el llamador no vea cambios no deseados.
#
# =============================================================================

# ─────────────────────────────────────────────
# PARTE 1: PREDICCIONES (modifica estos valores)
# ─────────────────────────────────────────────

# Caso A: ¿qué vale evento_a["ts"] después de llamar a añadir_ts()?
def añadir_ts(payload):
    payload["ts"] = "2026-03-22T10:00:00"

evento_a = {"room_id": "salon"}
añadir_ts(evento_a)

prediccion_A = "???"   # ¿existe "ts" en evento_a? ¿cuál es su valor?
# Opciones: "no existe", "2026-03-22T10:00:00", otra cosa

# Caso B: ¿qué vale x fuera de la función?
def incrementar(x):
    x = x + 1
    return x

x = 10
incrementar(x)

prediccion_B = 0   # ¿cuánto vale x aquí? (escribe el número)

# Caso C: ¿qué vale lista_c después de llamar a añadir_elemento()?
def añadir_elemento(lista):
    lista.append(99)

lista_c = [1, 2, 3]
añadir_elemento(lista_c)

prediccion_C = []   # ¿cómo queda lista_c? (escribe la lista completa)


# ─────────────────────────────────────────────
# PARTE 2: CORRIGE esta función
# ─────────────────────────────────────────────

import json
from pathlib import Path

LOG_PATH = Path("test_scope.jsonl")

def enriquecer_y_loggear(payload: dict, log_path: Path) -> None:
    """
    BUG: esta función añade "source" al payload original.
    El llamador no espera que su dict cambie.

    TAREA: arréglala para que funcione sin mutar el dict original.
    Escribe en el fichero el payload enriquecido, pero deja intacto
    el dict que recibiste como argumento.
    """
    payload["source"] = "agent_v1"   # ← BUG: muta el original
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


# --- NO MODIFICAR DESDE AQUÍ ---
LOG_PATH.unlink(missing_ok=True)

# Verificación Parte 1
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

# Verificación Parte 2
print("\n=== PARTE 2: Función corregida ===")
evento_original = {"room_id": "salon", "status": "executed"}
copia_antes = dict(evento_original)

enriquecer_y_loggear(evento_original, LOG_PATH)

if evento_original == copia_antes:
    print("  [OK] El dict original no fue modificado.")
else:
    print(f"  [FALLO] El dict original fue modificado:")
    print(f"          antes:  {copia_antes}")
    print(f"          después: {evento_original}")

# Verificar que sí se escribió en el fichero
if LOG_PATH.exists():
    with LOG_PATH.open() as f:
        linea = json.loads(f.readline())
    if linea.get("source") == "agent_v1":
        print("  [OK] El fichero contiene 'source: agent_v1'.")
    else:
        print("  [FALLO] El fichero no contiene el campo 'source'.")
    LOG_PATH.unlink(missing_ok=True)
else:
    print("  [FALLO] No se creó el fichero de log.")
