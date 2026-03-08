from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


def get_time_bucket(ts: str) -> str:
    now = datetime.fromisoformat(ts)
    h = now.hour
    if 7 <= h < 12:
        return "morning"
    if 12 <= h < 20:
        return "afternoon"
    return "night"


def build_room_state(raw_room: Dict[str, Any], prefs: Dict[str, int]) -> Dict[str, Any]:
    room_id = raw_room["room_id"]
    pir_sensor = next(k for k in raw_room["sensors"] if k.startswith("pir_"))
    lux_sensor = next(k for k in raw_room["sensors"] if k.startswith("lux_"))
    device_id = next(iter(raw_room["devices"].keys()))
    now = raw_room["now"]

    occupied = int(raw_room["sensors"][pir_sensor]["value"]) > 0
    lux = float(raw_room["sensors"][lux_sensor]["value"])
    light_state = raw_room["devices"][device_id]

    return {
        "room_id": room_id,
        "occupied": occupied,
        "occupied_confidence": 0.9 if occupied else 0.1,
        "lux": lux,
        "time_bucket": get_time_bucket(now),
        "light_state": light_state,
        "preferred_brightness": prefs,
        "last_manual_override_ts": raw_room["meta"].get("last_manual_override_ts"),
        "last_action_ts": raw_room["meta"].get("last_action_ts"),
        "absence_since_ts": raw_room["meta"].get("absence_since_ts"),
        "now": now,
    }
