from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolSpec(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any] = Field(default_factory=dict)


class ToolCallRequest(BaseModel):
    tool: str
    args: Dict[str, Any] = Field(default_factory=dict)


class RoomState(BaseModel):
    room_id: str
    occupied: bool
    occupied_confidence: float
    lux: float
    time_bucket: str
    light_state: Dict[str, Any]
    preferred_brightness: Dict[str, int]
    last_manual_override_ts: Optional[str] = None


class PlanAction(BaseModel):
    tool: str
    args: Dict[str, Any]


class Plan(BaseModel):
    room_id: str
    decision: str
    reason: str
    actions: List[PlanAction] = Field(default_factory=list)
