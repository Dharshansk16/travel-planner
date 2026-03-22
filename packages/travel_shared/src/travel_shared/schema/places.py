from pydantic import BaseModel, Field
from typing import Optional


class PlaceSearchRequest(BaseModel):
    city: str = Field(
        ...,
        description="City to search places in like Delhi, Mumbai etc"
    )
    category: Optional[str] = Field(
        None,
        description="Type of place can be food,shopping etc"
    )
    budget: Optional[int] = Field(
        None,
        ge=0,
        description="Maximum cost user is willing to spend at the place (in INR)"
    )


class PlaceSearchResponse(BaseModel):
    place_id: str
    city: str
    name: str
    category: str
    avg_time_spent: float
    cost: int
    rating: float