# =============================================================================
# Ejercicio A-3 — Argumentos por defecto y por nombre  ★★☆
# Bloque A · T05 Funciones
# =============================================================================
#
# CONTEXTO:
#   update_preference (preferences.py línea 46) tiene un argumento por defecto:
#       def update_preference(room_id, time_bucket, observed, alpha=0.3)
#   Esto hace que alpha sea opcional: si no se pasa, vale 0.3.
#
#   Los argumentos por nombre (keyword args) permiten pasar parámetros
#   en cualquier orden y hacen el código más legible:
#       json.dumps(payload, ensure_ascii=False, indent=2)
#
# TAREA — PARTE 1: implementa format_log_line()
#   La función debe construir una cadena de texto con el resumen de una
#   acción del agente. El separador entre campos es opcional (default: " | ").
#
#   Firma:
#     def format_log_line(room_id: str, status: str, decision: str = "-",
#                         sep: str = " | ") -> str
#
#   Ejemplos:
#     format_log_line("salon", "executed", "turn_on")
#       → "salon | executed | turn_on"
#     format_log_line("pasillo", "blocked")
#       → "pasillo | blocked | -"
#     format_log_line("salon", "executed", "turn_on", sep=" :: ")
#       → "salon :: executed :: turn_on"
#
# TAREA — PARTE 2: llamadas con argumentos por nombre
#   Llama a format_log_line usando argumentos por nombre para que
#   el código sea autodocumentado. Completa las líneas marcadas.
#
# COMPROBACIÓN AUTOMÁTICA al ejecutar el script.
# =============================================================================


def format_log_line(room_id: str, status: str,
                    decision: str = "-", sep: str = " | ") -> str:
    """Construye una línea de resumen del log del agente."""
    # --- ESCRIBE TU CÓDIGO AQUÍ (Parte 1) ---
    pass


# --- PARTE 2: llama a format_log_line usando argumentos por nombre ---
# Completa las llamadas. No uses argumentos posicionales en estas líneas.

linea_a = format_log_line(...)   # salon, executed, turn_on
linea_b = format_log_line(...)   # dormitorio, blocked  (sin decision explícita)
linea_c = format_log_line(...)   # pasillo, noop, do_nothing, separador " :: "


# --- NO MODIFICAR DESDE AQUÍ ---
esperados = [
    (linea_a, "salon | executed | turn_on"),
    (linea_b, "dormitorio | blocked | -"),
    (linea_c, "pasillo :: noop :: do_nothing"),
]

errores = 0
for obtenido, esperado in esperados:
    ok = obtenido == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] '{obtenido}'")
    if not ok:
        print(f"          esperado: '{esperado}'")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
