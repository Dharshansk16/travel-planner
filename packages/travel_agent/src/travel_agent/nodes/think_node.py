from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from travel_agent.agent.state import AgentState

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def get_llm_with_tools():
    from travel_agent.utils.mcp_client import get_tool_list
    tools = get_tool_list()
    if tools:
        print(f"[think_node] Binding {len(tools)} real MCP tools to LLM")
        return llm.bind_tools(tools)
    return llm

# Load once at import time
llm_with_tools = get_llm_with_tools()

def think_node(state: AgentState) -> AgentState:
    dest     = state.get("dest", "unknown")
    budget   = state.get("budget", 0)
    weather  = state.get("weather", "any")
    rating   = state.get("rating", 0)
    duration = state.get("duration", 1)
    source   = state.get("source", "Bangalore")
    places   = state.get("places", [])
    msgs     = list(state.get("messages", []))

    # Track which tools have been called
    tools_called = []
    for m in msgs:
        content = ""
        if hasattr(m, "content") and isinstance(m.content, str):
            content = m.content
        if "[TOOL RESULT] Places found"  in content: tools_called.append("search_places")
        if "[TOOL RESULT] Flights found" in content: tools_called.append("search_flights")
        if "[TOOL RESULT] Hotels found"  in content: tools_called.append("search_hotels")

    # Force finalize if all 3 tools called
    if ("search_places"  in tools_called and
        "search_flights" in tools_called and
        "search_hotels"  in tools_called):
        msgs.append(AIMessage(
            content="THOUGHT: All data collected.\nACTION: finalize"))
        return {**state, "messages": msgs}

    system = f"""You are a travel planning agent.

USER REQUEST:
- Destination: {dest}
- From: {source}
- Budget: INR {budget}
- Duration: {duration} days
- Weather: {weather}
- Min rating: {rating}

Tools already called: {tools_called}
Places found so far: {len(places)}

RULES:
- Call each tool ONLY ONCE
- Do not repeat tools already in tools_called
- Call search_places first
- Call finalize when search_places, search_flights and search_hotels are all done"""

    response = llm_with_tools.invoke([
        {"role": "system", "content": system},
        {"role": "user",   "content": f"Plan trip to {dest} for {duration} days, budget INR {budget}"}
    ])

    # LLM made a native tool call
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_name = response.tool_calls[0]["name"]
        print(f"[think_node] LLM natively chose MCP tool: {tool_name}")
        msgs.append(AIMessage(
            content=f"THOUGHT: Calling {tool_name}\nACTION: {tool_name}"))
    else:
        msgs.append(AIMessage(content=response.content))

    return {**state, "messages": msgs}