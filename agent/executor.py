from __future__ import annotations

from typing import Any, Dict, List


class PlanExecutor:
    SUPPORTED_TOOLS = {"set_room_lights", "set_light"}

    def execute(self, mcp_client, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for action in plan["actions"]:
            tool = action["tool"]
            if tool not in self.SUPPORTED_TOOLS:
                raise ValueError(f"Unsupported tool in executor: {tool}")
            res = mcp_client.call_tool(tool, action["args"])
            results.append(res)
        return results
