from dotenv import load_dotenv
from langchain_groq import ChatGroq
from travel_agent.state import AgentState

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

def think_node(state: AgentState) -> AgentState:
    dest    = state.get("dest", "unknown")
    budget  = state.get("budget", 0)
    weather = state.get("weather", "any")
    rating  = state.get("rating", 0)
    places  = state.get("places", [])
    msgs    = list(state.get("messages", []))

    # Count how many tool calls already happened
    tools_used = [
        m["content"] for m in msgs
        if isinstance(m, dict) and m.get("role") == "assistant"
    ]

    prompt = f"""You are a travel planning agent.

USER REQUEST:
- Destination: {dest}
- Budget: INR {budget}
- Weather preference: {weather}
- Minimum rating: {rating}

Tools already called: {len(tools_used)}
Places found so far: {len(places)}

AVAILABLE TOOLS:
- get_nearby_locations  (call FIRST to find places)
- estimate_cost         (call to check costs)
- fetch_weather           (call to verify weather)
- get_rating            (call to check ratings)
- finalize              (call when you have enough data)

RULES:
- Always call get_nearby_locations first
- Call each tool only once
- Call finalize when you have locations + costs + weather

Reply ONLY in this exact format:
THOUGHT: <one sentence explaining what you will do>
ACTION: <tool_name>"""

    response = llm.invoke(prompt).content
    msgs.append({"role": "assistant", "content": response})

    return {**state, "messages": msgs}