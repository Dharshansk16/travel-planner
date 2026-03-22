import asyncio
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from travel_agent.state import AgentState
from travel_agent.extract_action import extract_action

load_dotenv()

def invoke_tool(tool, args):
    try:
        return tool.invoke(args)
    except NotImplementedError:
        return asyncio.run(tool.ainvoke(args))

def parse_mcp_result(result):
    if not result:
        return []
    if isinstance(result, list) and len(result) > 0:
        first = result[0]
        if isinstance(first, dict) and first.get("type") == "text":
            try:
                return json.loads(first["text"])
            except Exception:
                return []
        return [item.model_dump() if hasattr(item, "model_dump") else item
                for item in result]
    return []

class ToolNode:
    def __init__(self, tools: dict):
        self.tools = tools

    def _last_thought(self, msgs: list) -> str:
        for m in reversed(msgs):
            if hasattr(m, "type") and m.type == "ai":
                return m.content
            if isinstance(m, dict) and m.get("role") == "assistant":
                return m["content"]
        return ""

    def _add_message(self, msgs: list, content: str):
        msgs.append(HumanMessage(content=f"[TOOL RESULT] {content}"))

    def _search_places(self, state: AgentState, msgs: list) -> AgentState:
        try:
            result = invoke_tool(self.tools["search_places"], {
                "req": {
                    "city":     state.get("dest", ""),
                    "category": None,
                    "budget":   None
                }
            })
            places = parse_mcp_result(result)
        except Exception as e:
            print(f"[ToolNode] Error in search_places: {e}")
            places = []
        print(f"[ToolNode] Places: {len(places)} found")
        self._add_message(msgs, f"Places found: {places}")
        return {**state, "messages": msgs, "places": places}

    def _search_flights(self, state: AgentState, msgs: list) -> AgentState:
        try:
            result = invoke_tool(self.tools["search_flights"], {
                "req": {
                    "source":      state.get("source", "Bangalore"),
                    "destination": state.get("dest", ""),
                    "date":        state.get("travel_date", "2026-04-10"),
                    "budget":      None
                }
            })
            flights = parse_mcp_result(result)
        except Exception as e:
            print(f"[ToolNode] Error in search_flights: {e}")
            flights = []
        print(f"[ToolNode] Flights: {len(flights)} found")
        self._add_message(msgs, f"Flights found: {flights}")
        return {**state, "messages": msgs, "flight": flights}

    def _search_hotels(self, state: AgentState, msgs: list) -> AgentState:
        try:
            result = invoke_tool(self.tools["search_hotels"], {
                "req": {
                    "city":             state.get("dest", ""),
                    "budget_per_night": None,
                    "min_rating":       None
                }
            })
            hotels = parse_mcp_result(result)
        except Exception as e:
            print(f"[ToolNode] Error in search_hotels: {e}")
            hotels = []
        print(f"[ToolNode] Hotels: {len(hotels)} found")
        self._add_message(msgs, f"Hotels found: {hotels}")
        return {**state, "messages": msgs, "hotels": hotels}

    def _fetch_weather(self, state: AgentState, msgs: list) -> AgentState:
        try:
            result = invoke_tool(self.tools["fetch_weather"], {
                "req": {
                    "destination": state.get("dest", "")   # ← was "city", now "destination"
                }
            })
            weather_data = parse_mcp_result(result)
            weather_str  = str(weather_data) if weather_data else "unknown"
        except Exception as e:
            print(f"[ToolNode] Error in fetch_weather: {e}")
            weather_str = "unknown"
        print(f"[ToolNode] Weather: fetched")
        self._add_message(msgs, f"Weather found: {weather_str}")
        return {**state, "messages": msgs, "weather": weather_str}

    def run(self, state: AgentState) -> AgentState:
        msgs      = list(state.get("messages", []))
        tool_name = extract_action(self._last_thought(msgs))
        print(f"[ToolNode] Calling: {tool_name}")

        if tool_name == "search_places":
            return self._search_places(state, msgs)
        elif tool_name == "search_flights":
            return self._search_flights(state, msgs)
        elif tool_name == "search_hotels":
            return self._search_hotels(state, msgs)
        elif tool_name == "fetch_weather":
            return self._fetch_weather(state, msgs)

        return {**state, "messages": msgs}

def tool_node(state: AgentState, tools: dict) -> AgentState:
    return ToolNode(tools).run(state)