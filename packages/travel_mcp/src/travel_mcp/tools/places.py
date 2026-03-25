from travel_mcp.services.place_service import PlaceService
from fastmcp import FastMCP
from travel_shared.schema.places import PlaceSearchRequest, PlaceSearchResponse
from typing import Optional

place_service = PlaceService()

def register_place_tool(mcp: FastMCP):
    @mcp.tool()
    def search_places(req: PlaceSearchRequest) -> list[PlaceSearchResponse]:
        """
        Search for points of interest, attractions, or things to do in a specific city.
        
        Use this when a user asks for recommendations on what to see, visit, or do.
        You can filter by category (e.g., 'museum', 'park', 'landmark') and budget.
        """
        places = place_service.search_places(
            city=req.city,
            category=req.category,
            budget=req.budget,
        )

        return [
            PlaceSearchResponse(
                place_id=place["place_id"],
                city=place["city"],
                name=place["name"],
                category=place["category"],
                avg_time_spent=place["avg_time_spent"],
                cost=place["cost"],
                rating=float(place.get("rating", 4.0)),
            )
            for place in places
        ]