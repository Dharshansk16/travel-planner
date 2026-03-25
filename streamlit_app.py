import sys
sys.path.insert(0, "packages/travel_agent/src")

import streamlit as st
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="Travel Planner AI",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.main .block-container { padding: 2rem 3rem; max-width: 1100px; }

.hero {
    background: linear-gradient(135deg, #1B3A6B 0%, #1E7FC2 100%);
    border-radius: 20px;
    padding: 40px;
    color: white;
    margin-bottom: 24px;
    text-align: center;
}
.hero h1 { font-size: 42px; font-weight: 700; margin: 0; }
.hero p  { font-size: 16px; opacity: 0.85; margin-top: 8px; }

.chat-wrap  { padding: 8px 0; }
.msg-user   { text-align: right; margin: 6px 0; }
.msg-agent  { text-align: left;  margin: 6px 0; }
.bubble-user {
    display: inline-block;
    background: #1E7FC2;
    color: white;
    padding: 10px 16px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 14px;
}
.bubble-agent {
    display: inline-block;
    background: #F0F4F8;
    color: #1a1a2e;
    padding: 10px 16px;
    border-radius: 18px 18px 18px 4px;
    max-width: 75%;
    font-size: 14px;
}

.plan-header {
    background: linear-gradient(135deg, #1B3A6B, #1E7FC2);
    color: white;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
}
.plan-header h2 { margin: 0; font-size: 26px; }
.plan-meta      { margin-top: 10px; font-size: 14px; opacity: 0.88; }

.card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
}
.card-title {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 2px solid #f0f0f0;
}

.flight-pill {
    background: #EBF5FB;
    border-left: 4px solid #1E7FC2;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
}
.hotel-pill {
    background: #EAFAF1;
    border-left: 4px solid #1A7A4A;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 13px;
    margin-bottom: 8px;
}
.place-pill {
    background: #FEF9E7;
    border-left: 4px solid #C9862A;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    margin-bottom: 6px;
}
.badge {
    display: inline-block;
    background: #fff3e0;
    color: #C9862A;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 20px;
    margin-left: 6px;
}

.sidebar-dest {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 6px;
    font-size: 13px;
}
.example-chip {
    background: #EBF5FB;
    border-radius: 20px;
    padding: 6px 12px;
    font-size: 12px;
    color: #1E7FC2;
    margin-bottom: 6px;
    display: block;
}
.stButton button {
    width: 100%;
    background: #1E7FC2;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner="Connecting to AI agent...")
def load_graph():
    from travel_agent.graph import app
    return app

for k, v in {
    "chat":           [],
    "memory":         {},
    "pending_query":  None,
    "waiting_for":    None,
    "travel_result":  None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def run_agent(query: str):
    graph = load_graph()
    return graph.invoke({
        "messages":    [HumanMessage(content=query)],
        "user_input":  query,
        "dest":        None, "budget":      None,
        "weather":     None, "rating":      None,
        "duration":    None, "travel_date": None,
        "source":      None, "flight":      [],
        "hotels":      [], "places":       [],
        "final_data":  None, "final_answer": None,
        "memory":      st.session_state.memory,
    })

def get_clarification_msg(result):
    for m in reversed(result.get("messages", [])):
        if hasattr(m, "type") and m.type == "ai":
            c = m.content
            if "ACTION" not in c and "THOUGHT" not in c:
                return c
    return None

def render_plan(result):
    data     = result.get("final_data", {})
    dest     = data.get("destination", "")
    source   = data.get("source", "Bangalore")
    duration = data.get("duration", 1)
    budget   = data.get("budget", 0)
    weather  = data.get("weather") or result.get("weather") or "Not specified"
    flight   = data.get("flight", {})
    hotels   = data.get("hotels", [])
    places   = data.get("places", [])

    st.markdown(f"""
    <div class="plan-header">
        <h2>{source} to {dest}</h2>
        <div class="plan-meta">
            {duration} day(s) &nbsp;·&nbsp;
            INR {budget:,} total budget &nbsp;·&nbsp;
            {weather}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="card"><div class="card-title">Flight</div>', unsafe_allow_html=True)
        if flight and flight.get("airline"):
            st.markdown(f"""
            <div class="flight-pill">
                <b>{flight.get('airline')}</b><br>
                {flight.get('departure_time', '?')} to {flight.get('arrival_time', '?')}<br>
                INR {flight.get('price', 0):,}
                &nbsp;·&nbsp; {flight.get('duration', 0)} min
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No direct flights found in database.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">Hotels</div>', unsafe_allow_html=True)
        if hotels:
            for h in hotels[:3]:
                rating = h.get('rating', 0)
                amenities = ", ".join(h.get("amenities", []))
                st.markdown(f"""
                <div class="hotel-pill">
                    <b>{h.get('name', 'N/A')}</b><br>
                    {h.get('location', '')} &nbsp;·&nbsp; {rating} Rating<br>
                    INR {h.get('price_per_night', 0):,}/night<br>
                    {amenities}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hotels found.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">Places to Visit</div>', unsafe_allow_html=True)
        if places:
            for p in places:
                rating = p.get("rating", 0)
                st.markdown(f"""
                <div class="place-pill">
                    <b>{p.get('name', 'N/A')}</b>
                    <span class="badge">{p.get('category', '')}</span><br>
                    Approx {p.get('avg_time_spent', 0)}hrs
                    &nbsp;·&nbsp; INR {p.get('cost', 0)}
                    &nbsp;·&nbsp; {rating} Rating
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No places found.")
        st.markdown('</div>', unsafe_allow_html=True)

        if flight or hotels:
            st.markdown('<div class="card"><div class="card-title">Budget Estimate</div>', unsafe_allow_html=True)
            flight_cost = flight.get("price", 0) if flight else 0
            hotel_cost  = hotels[0].get("price_per_night", 0) * duration if hotels else 0
            place_cost  = sum(p.get("cost", 0) for p in places[:3])
            total_est   = flight_cost + hotel_cost + place_cost

            st.markdown(f"""
            | Item | Cost |
            |---|---|
            | Flight | INR {flight_cost:,} |
            | Hotel ({duration} nights) | INR {hotel_cost:,} |
            | Places (top 3) | INR {place_cost:,} |
            | **Total estimate** | **INR {total_est:,}** |
            """)
            if total_est > budget:
                st.warning(f"Estimated cost (INR {total_est:,}) exceeds budget (INR {budget:,})")
            else:
                remaining = budget - total_est
                st.success(f"Within budget! INR {remaining:,} remaining for food and misc.")
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>Travel Planner AI</h1>
    <p>Powered by ReAct Agent and MCP. Ask in plain English</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Destinations")
    for dest, desc in [
        ("Goa",       "Beaches, Nightlife, History"),
        ("Manali",    "Mountains, Adventure, Snow"),
        ("Mumbai",    "City, Beaches, Food"),
        ("Delhi",     "History, Culture, Food"),
        ("Kochi",     "Backwaters, History"),
        ("Bangalore", "Gardens, Tech, Food"),
    ]:
        st.markdown(f"""
        <div class="sidebar-dest">
            <b>{dest}</b><br>
            <span style="color:#888;font-size:11px;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Try These")
    for ex in [
        "Plan a trip to Goa for 4 days, budget 8000",
        "Manali trip, 5 days, 15000 rupees",
        "Trip to Mumbai, 3 days, budget 10000, sunny",
        "Plan Delhi trip for 2 days, 6000 budget",
    ]:
        st.markdown(f'<span class="example-chip">{ex}</span>', unsafe_allow_html=True)

    st.divider()
    if st.button("Clear Chat"):
        for k in ["chat", "memory", "pending_query", "waiting_for", "travel_result"]:
            st.session_state[k] = [] if k == "chat" else {} if k == "memory" else None
        st.rerun()

left, right = st.columns([1.2, 1])

with left:
    st.markdown("### Chat")
    chat_container = st.container(height=350)
    with chat_container:
        for msg in st.session_state.chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user"><span class="bubble-user">{msg["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-agent"><span class="bubble-agent">{msg["content"]}</span></div>', unsafe_allow_html=True)

    with st.form("input_form", clear_on_submit=True):
        placeholder = (f"Answer: {st.session_state.waiting_for[:50]}..."
                       if st.session_state.waiting_for
                       else "e.g. Plan a trip to Goa for 4 days, budget 8000")
        user_input = st.text_input("", placeholder=placeholder, label_visibility="collapsed")
        send       = st.form_submit_button("Send", use_container_width=True)

with right:
    st.markdown("### Your Plan")
    if st.session_state.travel_result:
        render_plan(st.session_state.travel_result)
    else:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#aaa;">
            <div style="margin-top:12px;font-size:14px;">
                Your travel plan will appear here
            </div>
        </div>
        """, unsafe_allow_html=True)

if send and user_input.strip():
    text = user_input.strip()
    st.session_state.chat.append({"role": "user", "content": text})

    with st.spinner("Planning your trip..."):
        if st.session_state.waiting_for and st.session_state.pending_query:
            combined = f"{st.session_state.pending_query}. {text}"
            st.session_state.waiting_for   = None
            st.session_state.pending_query = None
        else:
            combined = text

        result = run_agent(combined)
        answer = result.get("final_answer")

        if answer:
            st.session_state.travel_result = result
            st.session_state.memory = {"source": "Bangalore"}
            st.session_state.chat.append({
                "role": "agent",
                "content": "Your travel plan is ready! Check the right panel."
            })
        else:
            clarification = get_clarification_msg(result)
            if clarification:
                st.session_state.chat.append({"role": "agent", "content": clarification})
                st.session_state.waiting_for   = clarification
                st.session_state.pending_query = combined

    st.rerun()