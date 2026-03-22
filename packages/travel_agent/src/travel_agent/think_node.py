from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage
from travel_agent.state import AgentState

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

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

    # Force finalize if all 3 tools called regardless of results
    if ("search_places"  in tools_called and
        "search_flights" in tools_called and
        "search_hotels"  in tools_called):
        msgs.append(AIMessage(
            content="THOUGHT: All data collected.\nACTION: finalize"))
        return {**state, "messages": msgs}

    prompt = f"""You are a travel planning agent.

USER REQUEST:
- Destination: {dest}
- From: {source}
- Budget: INR {budget}
- Duration: {duration} days
- Weather preference: {weather}
- Minimum rating: {rating}

Tools already called: {tools_called}
Places found so far: {len(places)}

AVAILABLE TOOLS:
- search_places    (find tourist places at destination)
- search_flights   (find flights from source to destination)
- search_hotels    (find hotels at destination)
- finalize         (when all 3 tools are done)

RULES:
- Call each tool ONLY ONCE
- Do not repeat a tool already in tools_called
- Call finalize only when search_places, search_flights and search_hotels are all done

Reply ONLY in this exact format:
THOUGHT: <one sentence>
ACTION: <tool_name>"""

    response = llm.invoke(prompt).content
    msgs.append(AIMessage(content=response))
    return {**state, "messages": msgs}