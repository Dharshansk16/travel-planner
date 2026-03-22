from travel_mcp.services.place_service import PlaceService
from fastmcp import FastMCP
from travel_shared.schema.places import PlaceSearchRequest, PlaceSearchResponse
from typing import Optional

place_service = PlaceService()

def register_place_tool(mcp: FastMCP):
    @mcp.tool
    def search_places(
        city: Optional[str] = None,
        category: Optional[str] = None,
        budget: Optional[int] = None,
        req: Optional[PlaceSearchRequest] = None,
    ) -> list[PlaceSearchResponse]:
        payload = req if req is not None else PlaceSearchRequest(
            city=city or "",
            category=category,
            budget=budget,
        )

        places = place_service.search_places(
            city=payload.city,
            category=payload.category,
            budget=payload.budget,
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