from travel_mcp.services.place_service import PlaceService
from fastmcp import FastMCP
from travel_shared.schema.places import PlaceSearchRequest, PlaceSearchResponse

place_service = PlaceService()

def register_place_tool(mcp: FastMCP):
    @mcp.tool
    def search_places(req: PlaceSearchRequest) -> list[PlaceSearchResponse]:
        return place_service.search_places(
            city=req.city,
            category=req.category,
            budget=req.budget
        )