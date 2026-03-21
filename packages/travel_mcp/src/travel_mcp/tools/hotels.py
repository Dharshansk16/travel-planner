from travel_mcp.services.hotel_service import HotelService
from fastmcp import FastMCP
from travel_shared.schema.hotel import HotelSearchRequest, HotelSearchResponse

hotel_service= HotelService()

def register_hotels_tool(mcp: FastMCP):
    
    @mcp.tool
    def search_hotels(req:HotelSearchRequest ) -> HotelSearchResponse:
        hotels = hotel_service.search_hotels(
            destination = req.destination,
            budget= req.budget if req.budget is not None else None
        )
        return HotelSearchResponse(hotels)
    