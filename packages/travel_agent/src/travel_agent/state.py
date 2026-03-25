from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages:     Annotated[list, add_messages]
    user_input:   str
    dest:         Optional[str]
    budget:       Optional[int]
    weather:      Optional[str]
    weather_data: Optional[dict]
    rating:       Optional[float]
    duration:     Optional[int]       
    travel_date:  Optional[str]       
    source:       Optional[str]       
    flight:       List[dict]
    hotels:       List[dict]
    places:       List[dict]
    final_data:   Optional[dict]
    final_answer: Optional[str]
    memory:       Optional[dict]      