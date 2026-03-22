from travel_agent.state import AgentState
from travel_agent.extract_action import extract_action

MAX_TOOL_CALLS = 10

def should_call_tool(state: AgentState) -> str:
    msgs = state.get("messages", [])

    tool_count = sum(1 for m in msgs
                     if (hasattr(m, "content") and
                         isinstance(m.content, str) and
                         m.content.startswith("[TOOL RESULT]")))

    if tool_count >= MAX_TOOL_CALLS:
        print(f"[routing] Max tool calls reached. Forcing stop.")
        return "filter"

    last = ""
    for m in reversed(msgs):
        if hasattr(m, "type") and m.type == "ai":
            last = m.content
            break
        if isinstance(m, dict) and m.get("role") == "assistant":
            last = m["content"]
            break

    if not last:
        return "tool"

    action = extract_action(last)
    print(f"[routing] tool_count={tool_count} action={action}")

    if action == "finalize":
        return "filter"

    return "tool"