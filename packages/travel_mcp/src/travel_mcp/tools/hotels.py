from travel_mcp.services.hotel_service import HotelService
from fastmcp import FastMCP
from travel_shared.schema.hotel import HotelSearchRequest, HotelSearchResponse

hotel_service = HotelService()

def register_hotels_tool(mcp: FastMCP):
    
    @mcp.tool()
    def search_hotels(req: HotelSearchRequest) -> list[HotelSearchResponse]:
        """
        Search for available hotels and accommodations in a specific destination.
        
        Use this when the user needs a place to stay, is looking for lodging, or wants to check hotel prices.
        Optionally filters by the user's budget.
        Returns a list of hotels including their rating, price per night, and amenities.
        """
        hotels = hotel_service.search_hotels(
            destination=req.destination,
            budget=req.budget if req.budget is not None else None
        )
        return [
            HotelSearchResponse(
                hotel_id=hotel["hotel_id"],
                name=hotel["name"],
                city=hotel["city"],
                location=hotel["location"],
                price_per_night=hotel["price_per_night"],
                rating=hotel["rating"],
                amenities=hotel["amenities"],
            )
            for hotel in hotels
        ]