# =============================================================================
# Ejercicio B-3 — Actualizar preferencia con suavizado  ★★★
# Bloque B · T04 Ficheros
# =============================================================================
#
# CONTEXTO:
#   Cuando el usuario ajusta manualmente la luz (override), el agente
#   no adopta inmediatamente el nuevo valor: lo mezcla con el valor
#   anterior usando una media ponderada exponencial (suavizado).
#
#   Fórmula (preferences.py línea 48):
#
#     nuevo = round( (1 - alpha) * valor_actual  +  alpha * valor_observado )
#
#   Con alpha = 0.3:
#     - 70% del valor anterior (memoria del sistema)
#     - 30% del nuevo override  (aprendizaje gradual)
#
#   Esto evita que un gesto accidental cambie drásticamente el comportamiento.
#
# TAREA:
#   Implementa update_preference(conn, room_id, time_bucket, observed, alpha).
#   Pasos dentro de la función:
#     1. Lee el brillo actual para (room_id, time_bucket) de la BD.
#        Si no existe, usa DEFAULT_PREFS[time_bucket].
#     2. Calcula new_value con la fórmula de suavizado.
#     3. Guarda new_value en la BD con INSERT OR REPLACE.
#     4. Devuelve new_value.
#
# COMPROBACIÓN AUTOMÁTICA al final del script.
# =============================================================================

import sqlite3

DEFAULT_PREFS = {"morning": 60, "afternoon": 70, "night": 25}

# --- Base de datos de ejemplo (no modificar) ---
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE room_preferences (
        room_id TEXT, time_bucket TEXT, brightness INTEGER,
        PRIMARY KEY (room_id, time_bucket)
    )
""")
conn.executemany(
    "INSERT INTO room_preferences VALUES (?,?,?)",
    [("salon", "night", 18), ("salon", "morning", 55), ("dormitorio", "night", 12)]
)
conn.commit()


def get_room_preferences(conn, room_id: str) -> dict:
    """Ya implementada — puedes usarla dentro de update_preference."""
    prefs = DEFAULT_PREFS.copy()
    cur = conn.execute(
        "SELECT time_bucket, brightness FROM room_preferences WHERE room_id = ?",
        (room_id,),
    )
    for tb, br in cur.fetchall():
        prefs[tb] = int(br)
    return prefs


def update_preference(conn, room_id: str, time_bucket: str,
                      observed: int, alpha: float = 0.3) -> int:
    """
    Calcula el nuevo brillo con suavizado y lo persiste en la BD.
    Devuelve el nuevo valor.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
# salon/night actual = 18, override = 5
# nuevo = round(0.7*18 + 0.3*5) = round(12.6 + 1.5) = round(14.1) = 14
nuevo1 = update_preference(conn, "salon", "night", observed=5)

# Tras el update, volver a aplicar: actual = 14, override = 5
# nuevo = round(0.7*14 + 0.3*5) = round(9.8 + 1.5) = round(11.3) = 11
nuevo2 = update_preference(conn, "salon", "night", observed=5)

# pasillo/night no tiene registro → usa default 25, override = 10
# nuevo = round(0.7*25 + 0.3*10) = round(17.5 + 3.0) = round(20.5) = 21 (o 20 según redondeo)
nuevo3 = update_preference(conn, "pasillo", "night", observed=10)
esperado3 = round(0.7 * 25 + 0.3 * 10)

errores = 0
for desc, obtenido, esperado in [
    ("salon/night 1er update (18→obs5)",    nuevo1, 14),
    ("salon/night 2do update (14→obs5)",    nuevo2, 11),
    (f"pasillo/night 1er update (25→obs10)", nuevo3, esperado3),
]:
    ok = obtenido == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {obtenido} (esperado {esperado})")

print()
if errores == 0:
    print("Todos los casos correctos.")
else:
    print(f"{errores} caso(s) incorrecto(s).")
