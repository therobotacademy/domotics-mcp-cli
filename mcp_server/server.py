from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from shared.schemas import ToolCallRequest, ToolSpec

app = FastAPI(title="MCP Lighting PoC Server", version="0.1.0")

DEFAULT_NOW = datetime(2026, 3, 8, 21, 0, 0)

STATE: Dict[str, Any] = {
    "now": DEFAULT_NOW,
    "rooms": {
        "salon": {
            "sensors": {
                "pir_salon": {"value": 0, "unit": "bool"},
                "lux_salon": {"value": 180.0, "unit": "lux"},
            },
            "devices": {
                "light_salon_main": {"is_on": False, "brightness": 0}
            },
            "meta": {
                "last_manual_override_ts": None,
                "last_action_ts": None,
                "absence_since_ts": None,
            },
        },
        "dormitorio": {
            "sensors": {
                "pir_bedroom": {"value": 0, "unit": "bool"},
                "lux_bedroom": {"value": 60.0, "unit": "lux"},
            },
            "devices": {
                "light_bedroom_main": {"is_on": False, "brightness": 0}
            },
            "meta": {
                "last_manual_override_ts": None,
                "last_action_ts": None,
                "absence_since_ts": None,
            },
        },
        "pasillo": {
            "sensors": {
                "pir_hall": {"value": 0, "unit": "bool"},
                "lux_hall": {"value": 25.0, "unit": "lux"},
            },
            "devices": {
                "light_hall": {"is_on": False, "brightness": 0}
            },
            "meta": {
                "last_manual_override_ts": None,
                "last_action_ts": None,
                "absence_since_ts": None,
            },
        },
    },
    "events": [],
}

TOOLS = [
    ToolSpec(name="list_tools", description="Return all available tools."),
    ToolSpec(name="describe_home", description="Describe rooms, sensors and actuators."),
    ToolSpec(name="get_room_state", description="Return full raw state for one room.", input_schema={"room_id": "str"}),
    ToolSpec(name="read_sensor", description="Read a sensor by id.", input_schema={"sensor_id": "str"}),
    ToolSpec(name="get_device_state", description="Read a device by id.", input_schema={"device_id": "str"}),
    ToolSpec(name="set_light", description="Set one light on/off and optional brightness.", input_schema={"device_id": "str", "on": "bool", "brightness": "int?"}),
    ToolSpec(name="set_room_lights", description="Set all lights in a room.", input_schema={"room_id": "str", "on": "bool", "brightness": "int?"}),
    ToolSpec(name="report_manual_override", description="Register a human override for a room.", input_schema={"room_id": "str", "brightness": "int?", "source": "str"}),
    ToolSpec(name="set_sensor_value", description="Simulation helper: set a sensor value.", input_schema={"sensor_id": "str", "value": "int|float"}),
    ToolSpec(name="advance_time", description="Simulation helper: advance simulated clock.", input_schema={"minutes": "int"}),
]


def _append_event(kind: str, payload: Dict[str, Any]) -> None:
    STATE["events"].append({
        "ts": STATE["now"].isoformat(),
        "kind": kind,
        "payload": payload,
    })


def _find_room_by_sensor(sensor_id: str):
    for room_id, room in STATE["rooms"].items():
        if sensor_id in room["sensors"]:
            return room_id, room
    raise HTTPException(status_code=404, detail=f"Unknown sensor: {sensor_id}")


def _find_room_by_device(device_id: str):
    for room_id, room in STATE["rooms"].items():
        if device_id in room["devices"]:
            return room_id, room
    raise HTTPException(status_code=404, detail=f"Unknown device: {device_id}")


def _serialize_room(room_id: str, room: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "room_id": room_id,
        "now": STATE["now"].isoformat(),
        "sensors": deepcopy(room["sensors"]),
        "devices": deepcopy(room["devices"]),
        "meta": {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in room["meta"].items()
        },
    }


@app.get("/list_tools")
def list_tools():
    return [tool.model_dump() for tool in TOOLS]


@app.get("/describe_home")
def describe_home():
    rooms = []
    for room_id, room in STATE["rooms"].items():
        rooms.append(
            {
                "room_id": room_id,
                "sensors": list(room["sensors"].keys()),
                "actuators": list(room["devices"].keys()),
                "capabilities": ["dimmable_light"],
            }
        )
    return {"now": STATE["now"].isoformat(), "rooms": rooms}


@app.get("/get_room_state/{room_id}")
def get_room_state(room_id: str):
    room = STATE["rooms"].get(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Unknown room: {room_id}")
    return _serialize_room(room_id, room)


@app.post("/call_tool")
def call_tool(req: ToolCallRequest):
    tool = req.tool
    args = req.args

    if tool == "list_tools":
        return list_tools()
    if tool == "describe_home":
        return describe_home()
    if tool == "get_room_state":
        room_id = args["room_id"]
        return get_room_state(room_id)
    if tool == "read_sensor":
        room_id, room = _find_room_by_sensor(args["sensor_id"])
        return {"room_id": room_id, "sensor_id": args["sensor_id"], **room["sensors"][args["sensor_id"]], "ts": STATE["now"].isoformat()}
    if tool == "get_device_state":
        room_id, room = _find_room_by_device(args["device_id"])
        return {"room_id": room_id, "device_id": args["device_id"], **room["devices"][args["device_id"]], "ts": STATE["now"].isoformat()}
    if tool == "set_light":
        return _set_light(args["device_id"], args["on"], args.get("brightness"))
    if tool == "set_room_lights":
        return _set_room_lights(args["room_id"], args["on"], args.get("brightness"))
    if tool == "report_manual_override":
        return _report_manual_override(args["room_id"], args.get("brightness"), args.get("source", "unknown"))
    if tool == "set_sensor_value":
        return _set_sensor_value(args["sensor_id"], args["value"])
    if tool == "advance_time":
        return _advance_time(args["minutes"])

    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")


def _set_light(device_id: str, on: bool, brightness: int | None = None):
    room_id, room = _find_room_by_device(device_id)
    device = room["devices"][device_id]
    device["is_on"] = bool(on)
    device["brightness"] = max(0, min(int(brightness if brightness is not None else device["brightness"]), 100)) if on else 0
    room["meta"]["last_action_ts"] = STATE["now"]
    _append_event("set_light", {"room_id": room_id, "device_id": device_id, "on": on, "brightness": device["brightness"]})
    return {"ok": True, "room_id": room_id, "device_id": device_id, "state": deepcopy(device)}


def _set_room_lights(room_id: str, on: bool, brightness: int | None = None):
    room = STATE["rooms"].get(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Unknown room: {room_id}")
    results = []
    for device_id in room["devices"]:
        results.append(_set_light(device_id, on, brightness))
    return {"ok": True, "room_id": room_id, "results": results}


def _report_manual_override(room_id: str, brightness: int | None, source: str):
    room = STATE["rooms"].get(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail=f"Unknown room: {room_id}")
    room["meta"]["last_manual_override_ts"] = STATE["now"]
    if brightness is not None:
        for device in room["devices"].values():
            device["is_on"] = brightness > 0
            device["brightness"] = max(0, min(int(brightness), 100))
    _append_event("manual_override", {"room_id": room_id, "brightness": brightness, "source": source})
    return {"ok": True, "room_id": room_id, "brightness": brightness, "source": source}


def _set_sensor_value(sensor_id: str, value: float):
    room_id, room = _find_room_by_sensor(sensor_id)
    room["sensors"][sensor_id]["value"] = value
    if sensor_id.startswith("pir_"):
        if int(value) == 0:
            if room["meta"]["absence_since_ts"] is None:
                room["meta"]["absence_since_ts"] = STATE["now"]
        else:
            room["meta"]["absence_since_ts"] = None
    _append_event("sensor_update", {"room_id": room_id, "sensor_id": sensor_id, "value": value})
    return {"ok": True, "room_id": room_id, "sensor_id": sensor_id, "value": value}


def _advance_time(minutes: int):
    if minutes < 0:
        raise HTTPException(status_code=400, detail="minutes must be >= 0")
    STATE["now"] = STATE["now"] + timedelta(minutes=minutes)
    _append_event("time_advanced", {"minutes": minutes, "now": STATE["now"].isoformat()})
    return {"ok": True, "now": STATE["now"].isoformat()}


@app.get("/events")
def get_events(limit: int = 50):
    return STATE["events"][-limit:]


@app.post("/reset")
def reset_state():
    global STATE
    STATE = {
        "now": DEFAULT_NOW,
        "rooms": {
            "salon": {
                "sensors": {
                    "pir_salon": {"value": 0, "unit": "bool"},
                    "lux_salon": {"value": 180.0, "unit": "lux"},
                },
                "devices": {
                    "light_salon_main": {"is_on": False, "brightness": 0}
                },
                "meta": {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
            },
            "dormitorio": {
                "sensors": {
                    "pir_bedroom": {"value": 0, "unit": "bool"},
                    "lux_bedroom": {"value": 60.0, "unit": "lux"},
                },
                "devices": {
                    "light_bedroom_main": {"is_on": False, "brightness": 0}
                },
                "meta": {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
            },
            "pasillo": {
                "sensors": {
                    "pir_hall": {"value": 0, "unit": "bool"},
                    "lux_hall": {"value": 25.0, "unit": "lux"},
                },
                "devices": {
                    "light_hall": {"is_on": False, "brightness": 0}
                },
                "meta": {"last_manual_override_ts": None, "last_action_ts": None, "absence_since_ts": None},
            },
        },
        "events": [],
    }
    return {"ok": True}
