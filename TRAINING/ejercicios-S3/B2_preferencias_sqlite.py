# =============================================================================
# Ejercicio B-2 — Leer preferencias de SQLite  ★★☆
# Bloque B · T04 Ficheros
# =============================================================================
#
# CONTEXTO:
#   El agente guarda el brillo preferido por habitación y franja horaria
#   en una base de datos SQLite (preferences.db).
#   La función get_room_preferences() de preferences.py (líneas 36-44)
#   lee esa tabla y rellena con los valores por defecto los huecos que
#   aún no tienen registro personalizado.
#
#   Tabla: room_preferences
#     room_id     TEXT   → "salon", "dormitorio", "pasillo"
#     time_bucket TEXT   → "morning", "afternoon", "night"
#     brightness  INTEGER → 0..100
#
#   Valores por defecto (DEFAULT_PREFS):
#     morning   → 60
#     afternoon → 70
#     night     → 25
#
# TAREA:
#   Implementa la función get_room_preferences(conn, room_id).
#   Debe devolver un diccionario con las tres franjas horarias.
#   Si hay un registro en la BD para esa combinación (room, franja),
#   usa ese valor; si no, usa el valor por defecto.
#
# COMPROBACIÓN AUTOMÁTICA al final del script.
# =============================================================================

import sqlite3

DEFAULT_PREFS = {"morning": 60, "afternoon": 70, "night": 25}

# --- Base de datos de ejemplo (no modificar) ---
conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE room_preferences (
        room_id     TEXT,
        time_bucket TEXT,
        brightness  INTEGER,
        PRIMARY KEY (room_id, time_bucket)
    )
""")
conn.executemany(
    "INSERT INTO room_preferences VALUES (?, ?, ?)",
    [
        ("salon",      "night",     18),
        ("salon",      "morning",   55),
        ("dormitorio", "night",     12),
    ]
)
conn.commit()


def get_room_preferences(conn, room_id: str) -> dict:
    """
    Devuelve {"morning": int, "afternoon": int, "night": int}
    con los valores de la BD o los defaults si no hay registro.
    """
    prefs = DEFAULT_PREFS.copy()

    # --- ESCRIBE TU CÓDIGO AQUÍ ---

    return prefs


# --- NO MODIFICAR DESDE AQUÍ ---
salon_prefs   = get_room_preferences(conn, "salon")
pasillo_prefs = get_room_preferences(conn, "pasillo")
dorm_prefs    = get_room_preferences(conn, "dormitorio")

esperado_salon   = {"morning": 55, "afternoon": 70, "night": 18}
esperado_pasillo = {"morning": 60, "afternoon": 70, "night": 25}
esperado_dorm    = {"morning": 60, "afternoon": 70, "night": 12}

errores = 0
for nombre, obtenido, esperado in [
    ("salon",      salon_prefs,   esperado_salon),
    ("pasillo",    pasillo_prefs, esperado_pasillo),
    ("dormitorio", dorm_prefs,    esperado_dorm),
]:
    ok = obtenido == esperado
    if not ok:
        errores += 1
    estado = "OK" if ok else "FALLO"
    print(f"  [{estado}] {nombre}: {obtenido}")
    if not ok:
        print(f"          esperado: {esperado}")

print()
if errores == 0:
    print("Todos los casos correctos.")
else:
    print(f"{errores} caso(s) incorrecto(s).")
