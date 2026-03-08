from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

MANUAL_OVERRIDE_WINDOW_MIN = 10
ROOM_COOLDOWN_SEC = 60
ABSENCE_OFF_DELAY_MIN = 3
NIGHT_MAX_BRIGHTNESS = 30


def _parse_ts(ts: str | None):
    return datetime.fromisoformat(ts) if ts else None


def apply_policy(room_state: Dict[str, Any]) -> Dict[str, Any]:
    now = _parse_ts(room_state["now"])
    last_override = _parse_ts(room_state.get("last_manual_override_ts"))
    last_action = _parse_ts(room_state.get("last_action_ts"))

    if last_override and now - last_override < timedelta(minutes=MANUAL_OVERRIDE_WINDOW_MIN):
        return {"allowed": False, "reason": "manual_override_window"}

    if last_action and now - last_action < timedelta(seconds=ROOM_COOLDOWN_SEC):
        return {"allowed": False, "reason": "cooldown"}

    return {"allowed": True, "reason": "ok"}


def should_turn_off_after_absence(room_state: Dict[str, Any]) -> bool:
    if room_state["occupied"]:
        return False
    absence_since = _parse_ts(room_state.get("absence_since_ts"))
    now = _parse_ts(room_state["now"])
    if absence_since is None:
        return False
    return now - absence_since >= timedelta(minutes=ABSENCE_OFF_DELAY_MIN)


def clamp_brightness(time_bucket: str, brightness: int) -> int:
    if time_bucket == "night":
        return min(brightness, NIGHT_MAX_BRIGHTNESS)
    return max(0, min(brightness, 100))
