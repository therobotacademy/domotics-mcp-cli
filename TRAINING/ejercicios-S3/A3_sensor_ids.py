# =============================================================================
# Ejercicio A-3 — Construir sensor_id dinámicamente  ★★☆
# Bloque A · T03 Cadenas de caracteres
# =============================================================================
#
# CONTEXTO:
#   El servidor MCP nombra los sensores siguiendo siempre el mismo patrón:
#     pir_{room_id}   →  "pir_salon", "pir_dormitorio", "pir_pasillo"
#     lux_{room_id}   →  "lux_salon", "lux_dormitorio", "lux_pasillo"
#
#   Si queremos añadir una habitación nueva ("cocina") necesitamos
#   generar esos IDs automáticamente, no escribirlos a mano.
#
# TAREA:
#   Usando f-strings, genera e imprime los IDs de sensor para cada habitación
#   de la lista `habitaciones`.
#
# SALIDA ESPERADA (alineada con espacios):
#   salon       → pir_salon        / lux_salon
#   dormitorio  → pir_dormitorio   / lux_dormitorio
#   pasillo     → pir_pasillo      / lux_pasillo
#   cocina      → pir_cocina       / lux_cocina
#
# PISTA:
#   Usa f"{variable:12}" para alinear columnas con ancho fijo de 12 caracteres.
# =============================================================================

habitaciones = ["salon", "dormitorio", "pasillo", "cocina"]

# --- ESCRIBE TU CÓDIGO AQUÍ ---


