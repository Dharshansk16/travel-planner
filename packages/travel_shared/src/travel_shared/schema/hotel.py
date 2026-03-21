from pydantic import BaseModel, Field
from typing import Optional

class HotelSearchRequest(BaseModel):
    destination: str = Field(
        ...,
        description="City name where the hotel is located"
    )
    budget: Optional[int] = Field(
        None,
        ge=0,
        description="Users Maximum budget for the hotel"
    )
    
class HotelSearchResponse(BaseModel):
    hotel_id: str
    name: str
    city: str
    location: str
    price: float
    rating: float
    amenities: list[str]



