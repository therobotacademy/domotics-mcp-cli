# Solución — Ejercicio B-3

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
    "INSERT INTO room_preferences VALUES (?,?,?)",
    [("salon", "night", 18), ("salon", "morning", 55), ("dormitorio", "night", 12)],
)
conn.commit()


def get_room_preferences(conn, room_id: str) -> dict:
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
    current   = get_room_preferences(conn, room_id)[time_bucket]
    new_value = round((1 - alpha) * current + alpha * observed)
    conn.execute(
        """
        INSERT INTO room_preferences (room_id, time_bucket, brightness)
        VALUES (?, ?, ?)
        ON CONFLICT(room_id, time_bucket) DO UPDATE SET brightness = excluded.brightness
        """,
        (room_id, time_bucket, new_value),
    )
    conn.commit()
    return new_value


# Verificación
nuevo1 = update_preference(conn, "salon",   "night", observed=5)   # 18 → 14
nuevo2 = update_preference(conn, "salon",   "night", observed=5)   # 14 → 11
nuevo3 = update_preference(conn, "pasillo", "night", observed=10)  # 25 → 21 (o 20)
esperado3 = round(0.7 * 25 + 0.3 * 10)

errores = 0
for desc, obtenido, esperado in [
    ("salon/night 1er update (18→obs5)",     nuevo1, 14),
    ("salon/night 2do update (14→obs5)",     nuevo2, 11),
    (f"pasillo/night 1er update (25→obs10)", nuevo3, esperado3),
]:
    ok = obtenido == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {obtenido} (esperado {esperado})")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
