from pydantic import BaseModel, Field

class HotelSearchRequest(BaseModel):
    destination: str = Field(
        ...,
        description="City name where the hotel is located"
    )
    budget: int = Field(
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



