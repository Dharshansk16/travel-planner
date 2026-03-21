from pydantic import BaseModel , Field
from typing import Optional

class TravelQuery(BaseModel):
    destination : Optional[str] = Field(
        None , 
        description="The specific city or country. If the user is vague (e.g., 'somewhere fun') , return null"
    )
    
    budget : Optional[int] = Field(
        None , 
        description = "The maximum budget in numbers. If not explicitly mentioned by the user, return null. Do not guess."
        )
    
    min_rating : Optional[float] = Field(
        None , 
        description = "Minimum star rating. Only fill if the user provides a number. Otherwise return null."
    )
    
    weather : Optional [str] = Field (
        None , 
        description="Weather preference. Only fill if stated. Otherwise return null."
    )
    
    