# =============================================================================
# Ejercicio A-1 — Identificar tipo de sensor  ★☆☆
# Bloque A · T03 Cadenas de caracteres
# =============================================================================
#
# CONTEXTO:
#   En world_model.py (líneas 19-20) el código busca qué sensor es PIR y cuál
#   es LUX dentro del diccionario de sensores de una habitación.
#   Para distinguirlos usa startswith(), porque el nombre cambia según la sala:
#     "pir_salon", "pir_bedroom", "pir_hall" ...
#
# TAREA:
#   Recorre el diccionario `sensores` con un bucle for.
#   Para cada clave, comprueba si empieza por "pir_" o por "lux_" y
#   muestra la línea correspondiente.
#
# SALIDA ESPERADA:
#   PIR encontrado: pir_salon  → valor 1
#   LUX encontrado: lux_salon  → valor 35.0
# =============================================================================

sensores = {
    "pir_salon": {"value": 1,    "unit": "bool"},
    "lux_salon": {"value": 35.0, "unit": "lux"},
}

# --- ESCRIBE TU CÓDIGO AQUÍ ---


