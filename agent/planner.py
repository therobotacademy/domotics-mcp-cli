from __future__ import annotations

from typing import Any, Dict

from .policy import clamp_brightness, should_turn_off_after_absence


class LightingPlanner:
    """Heuristic planner intentionally structured so a future LLM planner can replace it."""

    LUX_ON_THRESHOLD = 80.0
    LUX_OFF_THRESHOLD = 200.0

    def plan(self, room_state: Dict[str, Any]) -> Dict[str, Any]:
        room_id = room_state["room_id"]
        occupied = room_state["occupied"]
        lux = room_state["lux"]
        tb = room_state["time_bucket"]
        current_on = bool(room_state["light_state"]["is_on"])
        current_brightness = int(room_state["light_state"]["brightness"])
        preferred = int(room_state["preferred_brightness"][tb])
        target_brightness = clamp_brightness(tb, preferred)

        if not occupied:
            if current_on and should_turn_off_after_absence(room_state):
                return {
                    "room_id": room_id,
                    "decision": "turn_off",
                    "reason": "Room has been unoccupied for at least the configured absence window.",
                    "actions": [
                        {"tool": "set_room_lights", "args": {"room_id": room_id, "on": False}}
                    ],
                }
            return {
                "room_id": room_id,
                "decision": "do_nothing",
                "reason": "Room is unoccupied but absence delay has not elapsed yet.",
                "actions": [],
            }

        if lux >= self.LUX_OFF_THRESHOLD and current_on:
            return {
                "room_id": room_id,
                "decision": "turn_off",
                "reason": "Ambient light is already high; artificial lighting is unnecessary.",
                "actions": [
                    {"tool": "set_room_lights", "args": {"room_id": room_id, "on": False}}
                ],
            }

        if lux < self.LUX_ON_THRESHOLD:
            if (not current_on) or abs(current_brightness - target_brightness) >= 10:
                return {
                    "room_id": room_id,
                    "decision": "turn_on",
                    "reason": f"Presence detected with low ambient light ({lux} lux).",
                    "actions": [
                        {
                            "tool": "set_room_lights",
                            "args": {
                                "room_id": room_id,
                                "on": True,
                                "brightness": target_brightness,
                            },
                        }
                    ],
                }

        return {
            "room_id": room_id,
            "decision": "do_nothing",
            "reason": "Current lighting already matches context.",
            "actions": [],
        }
