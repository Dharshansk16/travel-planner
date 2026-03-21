from state import AgentState
from schema import TravelQuery
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage

load_dotenv()

llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0 
        ).with_structured_output(TravelQuery)

def parser_input(state: AgentState):
    
    result = llm.invoke(state["messages"])
    return {
        "dest": result.destination,
        "budget": result.budget,
        # "rating": result.min_rating,
        "weather":result.weather,
    }
    

def validate_input(state : AgentState):
    destination = state.get("dest")
    budget = state.get("budget")
    # rating = state.get("rating")
    weather = state.get("weather")
    
    if not destination or not budget or not weather:
        print("--- Missing info , heading to Clarifying node")
        return "ask_clarifying"
    
    print("---All info present , heading to Planner node")
    return "planner"


def ask_clarifying_node(state : AgentState):
    missing_info = []
    
    if not state.get("dest") : missing_info.append("destination")
    if not state.get("budget") : missing_info.append("budget")
    # if not state.get("rating") : missing_info.append("rating")
    if not state.get("weather") : missing_info.append("weather")
    
    needs = " and ".join(missing_info)
    question = f"I'm ready to plan your trip, but I need to know your {needs}. Could you please tell me?"
    
    return {
        "messages": [AIMessage(content=question)]
    }