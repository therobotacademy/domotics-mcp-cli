# =============================================================================
# Ejercicio B-1 — Llamar a GET /describe_home con requests  ★☆☆
# Bloque B · FastAPI cliente-servidor
# =============================================================================
#
# PREREQUISITO: el servidor MCP debe estar corriendo en localhost:8000.
#   cd Domotics-MCP-cli
#   uvicorn mcp_server.server:app --reload --port 8000
#
# CONTEXTO:
#   MCPClient en agent.py hace exactamente esto (líneas 29-30):
#       def describe_home(self) -> dict:
#           return requests.get(f"{self.base_url}/describe_home", timeout=5).json()
#
#   Vamos a reproducirlo paso a paso para entender qué pasa en cada línea.
#
# TAREA — PARTE 1: llamada básica
#   Llama a GET http://127.0.0.1:8000/describe_home con requests.get().
#   Imprime:
#     - El código de estado HTTP de la respuesta (200 si todo va bien).
#     - El contenido JSON convertido a dict de Python.
#
# TAREA — PARTE 2: extraer información
#   A partir del dict obtenido, imprime:
#     - La hora simulada del servidor ("now").
#     - Una línea por habitación con: nombre, sensores y actuadores.
#
# SALIDA ESPERADA (puede variar según estado del servidor):
#   Estado HTTP: 200
#   Hora del servidor: 2026-03-08T21:00:00
#   Habitaciones:
#     salon       | sensores: pir_salon, lux_salon       | actuadores: light_salon_main
#     dormitorio  | sensores: pir_bedroom, lux_bedroom   | actuadores: light_bedroom_main
#     pasillo     | sensores: pir_hall, lux_hall         | actuadores: light_hall
# =============================================================================

import requests

BASE_URL = "http://127.0.0.1:8000"


# --- PARTE 1: llamada y estado HTTP ---

# --- ESCRIBE TU CÓDIGO AQUÍ ---


# --- PARTE 2: extraer y mostrar la información ---

# --- ESCRIBE TU CÓDIGO AQUÍ ---
