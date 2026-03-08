from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import requests

from .executor import PlanExecutor
from .planner import LightingPlanner
from .policy import apply_policy
from .preferences import PreferenceStore
from .world_model import build_room_state

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "preferences.db"
LOG_PATH = BASE_DIR / "data" / "agent_log.jsonl"


@dataclass
class MCPClient:
    base_url: str

    def list_tools(self) -> List[Dict[str, Any]]:
        return requests.get(f"{self.base_url}/list_tools", timeout=5).json()

    def describe_home(self) -> Dict[str, Any]:
        return requests.get(f"{self.base_url}/describe_home", timeout=5).json()

    def get_room_state(self, room_id: str) -> Dict[str, Any]:
        return requests.get(f"{self.base_url}/get_room_state/{room_id}", timeout=5).json()

    def call_tool(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        resp = requests.post(f"{self.base_url}/call_tool", json={"tool": tool, "args": args}, timeout=5)
        resp.raise_for_status()
        return resp.json()


class LightingAgent:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.client = MCPClient(base_url)
        self.planner = LightingPlanner()
        self.executor = PlanExecutor()
        self.prefs = PreferenceStore(DB_PATH)
        self.tool_registry = []

    def discover_tools(self) -> List[str]:
        self.tool_registry = self.client.list_tools()
        return [tool["name"] for tool in self.tool_registry]

    def inspect_home(self) -> Dict[str, Any]:
        return self.client.describe_home()

    def process_once(self) -> List[Dict[str, Any]]:
        actions_summary = []
        home = self.inspect_home()
        for room in home["rooms"]:
            room_id = room["room_id"]
            raw = self.client.get_room_state(room_id)
            prefs = self.prefs.get_room_preferences(room_id)
            world = build_room_state(raw, prefs)
            policy = apply_policy(world)

            if not policy["allowed"]:
                record = {
                    "room_id": room_id,
                    "status": "blocked",
                    "policy_reason": policy["reason"],
                    "world": world,
                }
                self._log(record)
                actions_summary.append(record)
                continue

            plan = self.planner.plan(world)
            results = self.executor.execute(self.client, plan) if plan["actions"] else []
            record = {
                "room_id": room_id,
                "status": "executed" if results else "noop",
                "world": world,
                "plan": plan,
                "results": results,
            }
            self._log(record)
            actions_summary.append(record)
        return actions_summary

    def learn_from_manual_override(self, room_id: str, brightness: int) -> int:
        raw = self.client.get_room_state(room_id)
        prefs = self.prefs.get_room_preferences(room_id)
        world = build_room_state(raw, prefs)
        new_pref = self.prefs.update_preference(room_id, world["time_bucket"], brightness)
        self._log(
            {
                "room_id": room_id,
                "status": "learned_preference",
                "time_bucket": world["time_bucket"],
                "new_preference": new_pref,
                "observed_brightness": brightness,
            }
        )
        return new_pref

    def _log(self, payload: Dict[str, Any]) -> None:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def main():
    agent = LightingAgent()
    tools = agent.discover_tools()
    print("Tools descubiertas:", tools)
    print("Iniciando loop del agente. Ctrl+C para salir.")
    try:
        while True:
            summary = agent.process_once()
            for item in summary:
                print(json.dumps(item, ensure_ascii=False, indent=2))
            time.sleep(5)
    except KeyboardInterrupt:
        print("Agente detenido.")


if __name__ == "__main__":
    main()
