# Solución — Ejercicio B-2

import sqlite3

DEFAULT_PREFS = {"morning": 60, "afternoon": 70, "night": 25}

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE room_preferences (
        room_id TEXT, time_bucket TEXT, brightness INTEGER,
        PRIMARY KEY (room_id, time_bucket)
    )
""")
conn.executemany(
    "INSERT INTO room_preferences VALUES (?, ?, ?)",
    [("salon", "night", 18), ("salon", "morning", 55), ("dormitorio", "night", 12)],
)
conn.commit()


def get_room_preferences(conn, room_id: str) -> dict:
    prefs = DEFAULT_PREFS.copy()
    cur = conn.execute(
        "SELECT time_bucket, brightness FROM room_preferences WHERE room_id = ?",
        (room_id,),
    )
    for time_bucket, brightness in cur.fetchall():
        prefs[time_bucket] = int(brightness)
    return prefs


# Verificación
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
    print(f"  [{'OK' if ok else 'FALLO'}] {nombre}: {obtenido}")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
