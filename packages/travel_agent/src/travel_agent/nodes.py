
from state import AgentState
from schema import TravelQuery
import os

from .state import AgentState
from .schema import TravelQuery
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
    
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
).with_structured_output(TravelQuery)

def parser_input(state: AgentState):
    # Merge with memory if exists
    memory = state.get("memory") or {}

    result = llm.invoke(state["messages"])

    return {
        "dest":         result.destination or memory.get("dest"),
        "budget":       result.budget      or memory.get("budget"),
        "rating":       result.min_rating  or memory.get("rating"),
        "weather":      result.weather     or memory.get("weather"),
        "duration":     result.duration    or memory.get("duration"),
        "travel_date":  result.travel_date or "2026-04-10",
        "source":       result.source      or memory.get("source", "Bangalore"),
    }

def validate_input(state: AgentState):
    missing = []
    if not state.get("dest"):     missing.append("destination")
    if not state.get("budget"):   missing.append("budget")
    if not state.get("duration"): missing.append("number of days")

    if missing:
        print(f"--- Missing: {missing}, asking user")
        return "ask_clarifying"

    print("--- All info present, heading to think node")
    return "think"

def ask_clarifying_node(state: AgentState):
    missing = []
    if not state.get("dest"):     missing.append("destination")
    if not state.get("budget"):   missing.append("total budget in INR")
    if not state.get("duration"): missing.append("number of days")

    needs    = " and ".join(missing)
    question = (f"I'd love to help plan your trip! "
                f"Could you please tell me your {needs}?")

    return {"messages": [AIMessage(content=question)]}

