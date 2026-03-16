# =============================================================================
# Ejercicio A-1 — Implementar clamp_brightness  ★☆☆
# Bloque A · T05 Funciones
# =============================================================================
#
# CONTEXTO:
#   Esta es EXACTAMENTE la función clamp_brightness de policy.py (líneas 40-43).
#   El planner calcula un brillo preferido; la policy lo "sujeta" (clamps) para
#   que nunca supere el máximo permitido según el momento del día.
#
#   Reglas:
#     - Si es "night", el brillo máximo es NIGHT_MAX_BRIGHTNESS (30).
#     - En cualquier otro momento, el rango válido es 0..100.
#     - En ambos casos, nunca devuelve un valor negativo.
#
# TAREA:
#   Implementa clamp_brightness usando las dos constantes de módulo.
#   No uses números mágicos en la función: usa las constantes.
#
# COMPROBACIÓN AUTOMÁTICA al ejecutar el script.
# =============================================================================

# Constantes de módulo (scope de módulo — visibles dentro de la función)
NIGHT_MAX_BRIGHTNESS = 30


def clamp_brightness(time_bucket: str, brightness: int) -> int:
    """
    Ajusta 'brightness' al rango permitido según 'time_bucket'.
    Devuelve el valor corregido.
    """
    # --- ESCRIBE TU CÓDIGO AQUÍ ---
    pass


# --- NO MODIFICAR DESDE AQUÍ ---
casos = [
    # (time_bucket, brightness_entrada, resultado_esperado)
    ("night",     50,   30),   # supera el máximo nocturno → se recorta a 30
    ("night",     25,   25),   # dentro del rango nocturno → sin cambio
    ("night",     -5,    0),   # negativo → 0  (max(0, min(-5, 30)))
    ("morning",  120,  100),   # supera 100 → se recorta
    ("morning",   70,   70),   # rango normal → sin cambio
    ("morning",   -3,    0),   # negativo → 0
    ("afternoon", 30,   30),   # dentro de rango → sin cambio
]

errores = 0
for tb, entrada, esperado in casos:
    resultado = clamp_brightness(tb, entrada)
    ok = resultado == esperado
    if not ok:
        errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] clamp_brightness({tb!r:12}, {entrada:4}) "
          f"→ {str(resultado):4}  (esperado {esperado})")

print()
print("Todos los casos correctos." if errores == 0 else f"{errores} caso(s) incorrecto(s).")
