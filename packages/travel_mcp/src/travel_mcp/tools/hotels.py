from travel_mcp.services.hotel_service import HotelService
from fastmcp import FastMCP
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