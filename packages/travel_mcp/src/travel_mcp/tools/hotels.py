from travel_mcp.services.hotel_service import HotelService
from fastmcp import FastMCP
<<<<<<< HEAD
from pydantic import BaseModel, Field
from typing import Optional

hotel_service = HotelService()

class HotelSearchRequest(BaseModel):
    city:             str            = Field(..., description="City to search hotels in")
    budget_per_night: Optional[int]  = Field(None, description="Max price per night in INR")
    min_rating:       Optional[float]= Field(None, description="Minimum hotel rating")

def register_hotels_tool(mcp: FastMCP):
    @mcp.tool
    def search_hotels(req: HotelSearchRequest) -> list:
        return hotel_service.search_hotels(
            city=req.city,
            budget_per_night=req.budget_per_night,
            min_rating=req.min_rating
        )
=======
from travel_shared.schema.hotel import HotelSearchRequest, HotelSearchResponse

hotel_service= HotelService()

def register_hotels_tool(mcp: FastMCP):
    
    @mcp.tool
    def search_hotels(req:HotelSearchRequest ) -> list[HotelSearchResponse]:
        hotels = hotel_service.search_hotels(
            destination = req.destination,
            budget= req.budget if req.budget is not None else None
        )
        return [
            HotelSearchResponse(
                hotel_id=hotel["hotel_id"],
                name=hotel["name"],
                city=hotel["city"],
                location=hotel["location"],
                price=hotel["price_per_night"],
                rating=hotel["rating"],
                amenities=hotel["amenities"],
            )
            for hotel in hotels
        ]
    
>>>>>>> c1cba09d19d71fcbe1eee273856dbeecffc70215
