# Solución — Ejercicio B-1  (requiere servidor en localhost:8000)

import requests

BASE_URL = "http://127.0.0.1:8000"

# PARTE 1: llamada y código HTTP
respuesta = requests.get(f"{BASE_URL}/describe_home", timeout=5)
print(f"Estado HTTP: {respuesta.status_code}")

datos = respuesta.json()
print(f"Hora del servidor: {datos['now']}")

# PARTE 2: extraer habitaciones
print("Habitaciones:")
for room in datos["rooms"]:
    sensores   = ", ".join(room["sensors"])
    actuadores = ", ".join(room["actuators"])
    print(f"  {room['room_id']:<12} | sensores: {sensores:<35} | actuadores: {actuadores}")
