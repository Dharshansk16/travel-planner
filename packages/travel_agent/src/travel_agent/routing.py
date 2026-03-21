from travel_agent.state import AgentState
from travel_agent.extract_action import extract_action

MAX_TOOL_CALLS = 8

def should_call_tool(state: AgentState) -> str:
    msgs = state.get("messages", [])

    # Count tool calls so far — safety limit
    tool_count = sum(1 for m in msgs if isinstance(m, dict) and m.get("role") == "tool")
    if tool_count >= MAX_TOOL_CALLS:
        print(f"[routing] Max tool calls ({MAX_TOOL_CALLS}) reached. Forcing stop.")
        return "filter"

    # Get last assistant message
    last = next(
        (m["content"] for m in reversed(msgs)
         if isinstance(m, dict) and m.get("role") == "assistant"),
        ""
    )

    if not last:
        return "tool"

    action = extract_action(last)
    print(f"[routing] tool_count={tool_count} action={action}")

    if action == "finalize":
        return "filter"

    return "tool"