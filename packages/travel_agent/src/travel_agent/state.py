from typing import TypedDict , Annotated , List , Optional
from langgraph.graph import add_messages

class AgentState(TypedDict):
    messages:Annotated[list , add_messages]
    user_input : str
    dest: Optional[str]
    budget: Optional[int]
    weather: Optional[str]
    rating:Optional[float]
    
    flight:List[dict]
    hotels:List[dict]
    places:List[dict]