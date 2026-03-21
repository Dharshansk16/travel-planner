import ast
from dotenv import load_dotenv
from travel_agent.state import AgentState
from travel_agent.extract_action import extract_action

load_dotenv()

class ToolNode:
    LOCATION_TOOLS = {"estimate_cost", "get_weather", "get_rating"}

    def __init__(self, tools: dict):
        self.tools = tools

    def _last_thought(self, msgs: list) -> str:
        return next(
            (m["content"] for m in reversed(msgs)
             if isinstance(m, dict) and m.get("role") == "assistant"),
            ""
        )

    def _add_message(self, msgs: list, content: str):
        msgs.append({"role": "tool", "content": content})

    def _get_nearby(self, state: AgentState, msgs: list) -> AgentState:
        try:
            result = self.tools["get_nearby_locations"].invoke({"destination": state.get("dest", "")})
            places = ast.literal_eval(result) if isinstance(result, str) else result
            if not isinstance(places, list):
                places = []
        except Exception as e:
            print(f"[ToolNode] Error in get_nearby_locations: {e}")
            places, result = [], "[]"

        self._add_message(msgs, f"Nearby locations: {result}")
        return {**state, "messages": msgs, "places": places}

    def _run_per_place(self, tool_name: str, state: AgentState, msgs: list) -> AgentState:
        if not state.get("places"):
            self._add_message(msgs, f"No places found yet to run {tool_name}")
            return {**state, "messages": msgs}

        for place in state["places"]:
            try:
                result = self.tools[tool_name].invoke({"location": place.get("name", "")})
                self._add_message(msgs, f"{tool_name} for {place['name']}: {result}")
            except Exception as e:
                print(f"[ToolNode] Error in {tool_name} for {place.get('name')}: {e}")

        return {**state, "messages": msgs}

    def run(self, state: AgentState) -> AgentState:
        msgs      = list(state.get("messages", []))
        tool_name = extract_action(self._last_thought(msgs))
        print(f"[ToolNode] Calling: {tool_name}")

        if tool_name == "get_nearby_locations":
            return self._get_nearby(state, msgs)
        elif tool_name in self.LOCATION_TOOLS:
            return self._run_per_place(tool_name, state, msgs)

        return {**state, "messages": msgs}


def tool_node(state: AgentState, tools: dict) -> AgentState:
    return ToolNode(tools).run(state)