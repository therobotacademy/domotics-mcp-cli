# Solución — Ejercicio B-2  (requiere servidor en localhost:8000)

import requests

BASE_URL = "http://127.0.0.1:8000"


def call_tool(tool: str, args: dict) -> dict:
    resp = requests.post(f"{BASE_URL}/call_tool", json={"tool": tool, "args": args}, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_room_state(room_id: str) -> dict:
    resp = requests.get(f"{BASE_URL}/get_room_state/{room_id}", timeout=5)
    resp.raise_for_status()
    return resp.json()


# PARTE 1: reset y estado inicial
requests.post(f"{BASE_URL}/reset", timeout=5).raise_for_status()
estado_inicial = get_room_state("salon")
lux_inicial  = estado_inicial["sensors"]["lux_salon"]["value"]
pir_inicial  = estado_inicial["sensors"]["pir_salon"]["value"]
hora_inicial = estado_inicial["now"]
print(f"Estado inicial → lux={lux_inicial}  pir={pir_inicial}  now={hora_inicial}")

# PARTE 2: modificar sensores y tiempo
call_tool("set_sensor_value", {"sensor_id": "pir_salon",  "value": 1})
call_tool("set_sensor_value", {"sensor_id": "lux_salon",  "value": 20.0})
call_tool("advance_time",     {"minutes": 5})
print("Cambios aplicados: pir=1, lux=20.0, +5 min")

# PARTE 3: verificar
estado_nuevo = get_room_state("salon")
pir_nuevo  = estado_nuevo["sensors"]["pir_salon"]["value"]
lux_nuevo  = estado_nuevo["sensors"]["lux_salon"]["value"]
hora_nueva = estado_nuevo["now"]

print(f"\nEstado nuevo  → lux={lux_nuevo}  pir={pir_nuevo}  now={hora_nueva}")

errores = 0
for desc, real, esperado in [
    ("pir_salon == 1",     pir_nuevo,  1),
    ("lux_salon == 20.0",  lux_nuevo,  20.0),
    ("hora avanzó 5 min",  "21:05" in hora_nueva, True),
]:
    ok = real == esperado
    if not ok: errores += 1
    print(f"  [{'OK' if ok else 'FALLO'}] {desc}: {real}")

print("\nVerificación correcta." if errores == 0 else f"{errores} error(es).")
