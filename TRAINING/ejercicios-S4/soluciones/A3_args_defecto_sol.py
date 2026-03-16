# Solución — Ejercicio A-3


def format_log_line(room_id: str, status: str,
                    decision: str = "-", sep: str = " | ") -> str:
    return sep.join([room_id, status, decision])


# Llamadas con argumentos por nombre
linea_a = format_log_line(room_id="salon",      status="executed", decision="turn_on")
linea_b = format_log_line(room_id="dormitorio", status="blocked")
linea_c = format_log_line(room_id="pasillo",    status="noop", decision="do_nothing", sep=" :: ")

# Verificación
esperados = [
    (linea_a, "salon | executed | turn_on"),
    (linea_b, "dormitorio | blocked | -"),
    (linea_c, "pasillo :: noop :: do_nothing"),
]
errores = 0
for obtenido, esperado in esperados:
    ok = obtenido == esperado
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] '{obtenido}'")
print("\nTodos correctos." if errores == 0 else f"{errores} error(es).")
