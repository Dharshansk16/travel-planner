# --- Core Imports ---
from typing import Literal
from langgraph.graph import StateGraph, END, START
# --- State ---
from travel_agent.state import AgentState
# --- Person 1 Nodes ---
from travel_agent.nodes import (
    parser_input,
    validate_input,
    ask_clarifying_node,
    query_parser_node
)
# --- Person 2 Nodes ---
from travel_agent.think_node import think_node
from travel_agent.tool_node import tool_node
from travel_agent.routing import should_call_tool
# --- Your Nodes ---
from travel_agent.optimize_node import OptimizeNode
from travel_agent.combine_node import CombineNode
from travel_agent.filter_node import FilterNode
from travel_agent.generate_node import GenerateNode
# --- Node Instances (wrap class-based nodes) ---
optimize_node = OptimizeNode()
combine_node = CombineNode()
filter_node = FilterNode()
generate_node = GenerateNode()
# --- Tool Dictionary ---
tools = {
    "get_nearby_locations": lambda x: "[{'name':'Paris','rating':5,'weather':'sunny','cost':500}]",
    "estimate_cost": lambda x: 500,
    "fetch_weather": lambda x: "sunny",
    "get_rating": lambda x: 5,
    "finalize": lambda x: None
}
# --- Wrap functions for LangGraph compatibility ---
def think_step(state: AgentState):
    return think_node(state)

def tool_step(state: AgentState):
    return tool_node(state, tools)

def optimize_step(state: AgentState):
    return optimize_node.process(state)

def combine_step(state: AgentState):
    return combine_node.process(state)

def filter_step(state: AgentState):
    return filter_node.process(state)

def generate_step(state: AgentState):
    return generate_node.process(state)

# --- Build Workflow ---
workflow = StateGraph(AgentState)
# --- Add Nodes ---
workflow.add_node("parser", parser_input)
workflow.add_node("ask_clarifying", ask_clarifying_node)
workflow.add_node("think", think_step)
workflow.add_node("tool", tool_step)
workflow.add_node("optimize", optimize_step)
workflow.add_node("combine", combine_step)
workflow.add_node("filter", filter_step)
workflow.add_node("generate", generate_step)
# --- Flow ---
workflow.add_edge(START, "parser")
# Input validation
workflow.add_conditional_edges(
    "parser",
    validate_input,
    {
        "ask_clarifying": "ask_clarifying",
        "think": "think"
    }
)
# If clarification needed → END
workflow.add_edge("ask_clarifying", END)
# Core agent loop
workflow.add_edge("think", "tool")
# Decision after tool
workflow.add_conditional_edges(
    "tool",
    should_call_tool,
    {
        "filter": "optimize",
        "finalize": "generate"
    }
)
# Processing pipeline
workflow.add_edge("optimize", "combine")
workflow.add_edge("combine", "filter")
workflow.add_edge("filter", "generate")
# End
workflow.add_edge("generate", END)
# --- Compile ऐप ---
app = workflow.compile()