from __future__ import annotations

import json
import sys
import time

import requests

from agent.agent import LightingAgent

BASE_URL = "http://127.0.0.1:8000"


def call(tool: str, args: dict):
    r = requests.post(f"{BASE_URL}/call_tool", json={"tool": tool, "args": args}, timeout=5)
    r.raise_for_status()
    return r.json()


def reset():
    requests.post(f"{BASE_URL}/reset", timeout=5).raise_for_status()


def show(title: str, payload):
    print(f"\n=== {title} ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main():
    try:
        reset()
    except Exception as e:
        print("No puedo conectar con el servidor MCP-like en http://127.0.0.1:8000")
        print("Lánzalo primero con: uvicorn mcp_server.server:app --reload --port 8000")
        print(f"Detalle: {e}")
        sys.exit(1)

    agent = LightingAgent(BASE_URL)
    show("Tools descubiertas", agent.discover_tools())
    show("Casa", agent.inspect_home())

    # Escenario 1: salón de noche con poca luz y presencia.
    call("set_sensor_value", {"sensor_id": "lux_salon", "value": 35})
    call("set_sensor_value", {"sensor_id": "pir_salon", "value": 1})
    show("Escenario 1 - antes", requests.get(f"{BASE_URL}/get_room_state/salon", timeout=5).json())
    show("Escenario 1 - decisión agente", agent.process_once())
    show("Escenario 1 - después", requests.get(f"{BASE_URL}/get_room_state/salon", timeout=5).json())

    # Espera para evitar cooldown artificial en siguientes tests.
    call("advance_time", {"minutes": 2})

    # Escenario 2: dormitorio de noche, brillo limitado por política nocturna.
    call("set_sensor_value", {"sensor_id": "lux_bedroom", "value": 10})
    call("set_sensor_value", {"sensor_id": "pir_bedroom", "value": 1})
    show("Escenario 2 - decisión agente", agent.process_once())
    show("Escenario 2 - dormitorio", requests.get(f"{BASE_URL}/get_room_state/dormitorio", timeout=5).json())

    # Escenario 3: ausencia sostenida en salón.
    call("set_sensor_value", {"sensor_id": "pir_salon", "value": 0})
    call("advance_time", {"minutes": 4})
    show("Escenario 3 - decisión agente", agent.process_once())
    show("Escenario 3 - salón", requests.get(f"{BASE_URL}/get_room_state/salon", timeout=5).json())

    # Escenario 4: override manual y congelación temporal.
    call("report_manual_override", {"room_id": "dormitorio", "brightness": 12, "source": "wall_switch"})
    learned = agent.learn_from_manual_override("dormitorio", 12)
    show("Escenario 4 - preferencia aprendida", {"new_night_preference": learned})
    call("set_sensor_value", {"sensor_id": "pir_bedroom", "value": 1})
    call("set_sensor_value", {"sensor_id": "lux_bedroom", "value": 5})
    show("Escenario 4 - agente bloqueado por override", agent.process_once())

    # Avanzar tiempo para salir de la ventana de override.
    call("advance_time", {"minutes": 11})
    show("Escenario 5 - agente tras override", agent.process_once())
    show("Estado final dormitorio", requests.get(f"{BASE_URL}/get_room_state/dormitorio", timeout=5).json())

    events = requests.get(f"{BASE_URL}/events", timeout=5).json()
    show("Eventos recientes", events)


if __name__ == "__main__":
    main()
