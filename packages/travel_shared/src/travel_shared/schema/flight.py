from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as date_type

class FlightSearchRequest(BaseModel):
    source: str = Field(
        ...,
        description="Departure airport or city code Bangalore"
    )
    destination: str = Field(
        ...,
        description="Arrival airport or city code Delhi"
    )
    date: Optional[str] = Field(
        None,
        description="Travel date in YYYY-MM-DD format"
    )
    budget: Optional[int] = Field(
        None,
        ge=0,
        description="Maximum ticket price user is willing to pay (in INR)"
    )

class FlightSearchResponse(BaseModel):
    flight_id:      str
    source:         str
    destination:    str
    date:           str
    airline:        str
    departure_time: str
    price:          float