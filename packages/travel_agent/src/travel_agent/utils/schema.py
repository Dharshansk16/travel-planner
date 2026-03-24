from pydantic import BaseModel, Field
from typing import Optional

class TravelQuery(BaseModel):
    destination: Optional[str] = Field(
        None,
        description="The specific city. If vague, return null."
    )
    budget: Optional[int] = Field(
        None,
        description="Total budget in INR. If not mentioned, return null."
    )
    min_rating: Optional[float] = Field(
        None,
        description="Minimum rating 1-5. If not mentioned, return null."
    )
    weather: Optional[str] = Field(
        None,
        description="Weather preference. If not mentioned, return null."
    )
    duration: Optional[int] = Field(
        None,
        description="Number of days for the trip. If not mentioned, return null."
    )
    travel_date: Optional[str] = Field(
        None,
        description="Travel date in YYYY-MM-DD. If not mentioned, return null."
    )
    source: Optional[str] = Field(
        None,
        description="Departure city. Default to Bangalore if not mentioned."
    )