from langgraph.graph import StateGraph, END, START
from travel_agent.state import AgentState

from travel_agent.nodes        import parser_input, validate_input, ask_clarifying_node
from travel_agent.think_node   import think_node
from travel_agent.tool_node    import tool_node
from travel_agent.routing      import should_call_tool
from travel_agent.optimize_node import OptimizeNode
from travel_agent.combine_node  import CombineNode
from travel_agent.filter_node   import FilterNode
from travel_agent.generate_node import GenerateNode

optimize_node = OptimizeNode()
combine_node  = CombineNode()
filter_node   = FilterNode()
generate_node = GenerateNode()


from travel_agent.mcp_client import load_tools
tools, _client = load_tools()


def think_step(state):    return think_node(state)
def tool_step(state):     return tool_node(state, tools)
def optimize_step(state): return optimize_node.process(state)
def combine_step(state):  return combine_node.process(state)
def filter_step(state):   return filter_node.process(state)
def generate_step(state): return generate_node.process(state)


workflow = StateGraph(AgentState)

workflow.add_node("parser",         parser_input)
workflow.add_node("ask_clarifying", ask_clarifying_node)
workflow.add_node("think",          think_step)
workflow.add_node("tool",           tool_step)
workflow.add_node("optimize",       optimize_step)
workflow.add_node("combine",        combine_step)
workflow.add_node("filter",         filter_step)
workflow.add_node("generate",       generate_step)

workflow.add_edge(START, "parser")

workflow.add_conditional_edges(
    "parser",
    validate_input,
    {"ask_clarifying": "ask_clarifying", "think": "think"}
)

workflow.add_edge("ask_clarifying", END)

workflow.add_conditional_edges(
    "think",
    should_call_tool,
    {"tool": "tool", "filter": "optimize"}
)

workflow.add_edge("tool",     "think")
workflow.add_edge("optimize", "combine")
workflow.add_edge("combine",  "filter")
workflow.add_edge("filter",   "generate")
workflow.add_edge("generate", END)

app = workflow.compile()