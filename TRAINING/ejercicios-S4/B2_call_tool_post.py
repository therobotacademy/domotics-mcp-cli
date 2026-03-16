# =============================================================================
# Ejercicio B-2 — Llamar a POST /call_tool y verificar el efecto  ★★☆
# Bloque B · FastAPI cliente-servidor
# =============================================================================
#
# PREREQUISITO: el servidor MCP debe estar corriendo en localhost:8000.
#
# CONTEXTO:
#   MCPClient.call_tool() en agent.py (líneas 35-38) hace exactamente esto:
#       resp = requests.post(
#           f"{self.base_url}/call_tool",
#           json={"tool": tool, "args": args},
#           timeout=5
#       )
#       resp.raise_for_status()
#       return resp.json()
#
#   El endpoint POST /call_tool es el dispatcher universal: recibe el nombre
#   de la tool y sus argumentos, y ejecuta la función correspondiente.
#
# TAREA — PARTE 1: resetear y leer estado inicial
#   1. Llama a POST /reset para resetear el servidor.
#   2. Llama a GET /get_room_state/salon y guarda el estado.
#   3. Imprime el valor de lux_salon y pir_salon.
#
# TAREA — PARTE 2: modificar sensores y avanzar tiempo
#   Usando POST /call_tool, ejecuta las siguientes tools en orden:
#   a) set_sensor_value: pir_salon = 1
#   b) set_sensor_value: lux_salon = 20.0
#   c) advance_time: 5 minutos
#
# TAREA — PARTE 3: verificar el efecto
#   Llama de nuevo a GET /get_room_state/salon y comprueba que:
#   - pir_salon vale 1
#   - lux_salon vale 20.0
#   - La hora del servidor avanzó 5 minutos respecto al estado inicial
#
# =============================================================================

import requests

BASE_URL = "http://127.0.0.1:8000"


def call_tool(tool: str, args: dict) -> dict:
    """Helper: llama al dispatcher POST /call_tool."""
    resp = requests.post(f"{BASE_URL}/call_tool", json={"tool": tool, "args": args}, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_room_state(room_id: str) -> dict:
    """Helper: obtiene el estado de una habitación."""
    resp = requests.get(f"{BASE_URL}/get_room_state/{room_id}", timeout=5)
    resp.raise_for_status()
    return resp.json()


# --- PARTE 1: reset y estado inicial ---

# --- ESCRIBE TU CÓDIGO AQUÍ ---


# --- PARTE 2: modificar sensores y tiempo ---

# --- ESCRIBE TU CÓDIGO AQUÍ ---


# --- PARTE 3: verificar y reportar ---

# --- ESCRIBE TU CÓDIGO AQUÍ ---
