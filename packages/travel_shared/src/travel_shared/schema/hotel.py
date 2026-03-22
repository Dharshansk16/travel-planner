from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from typing import Optional

class HotelSearchRequest(BaseModel):
    destination: str = Field(
        ...,
        validation_alias=AliasChoices("destination", "city"),
        description="City name where the hotel is located"
    )
    budget: Optional[int] = Field(
        None,
        ge=0,
        validation_alias=AliasChoices("budget", "budget_per_night"),
        description="Users Maximum budget for the hotel"
    )
    
class HotelSearchResponse(BaseModel):
    hotel_id: str
    name: str
    city: str
    location: str
    price_per_night: float
    price: float
    rating: float
    amenities: list[str]



