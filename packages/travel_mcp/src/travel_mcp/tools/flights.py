from travel_mcp.services.flight_service import FlightService
from fastmcp import FastMCP
from travel_shared.schema.flight import FlightSearchRequest, FlightSearchResponse

flight_service = FlightService()

def register_flight_tool(mcp: FastMCP):
    @mcp.tool
    def search_flights(req:FlightSearchRequest) -> list[FlightSearchResponse]:
        return flight_service.search_flights(
            source=req.source,
            destination=req.destination,
            date=req.date,
            budget=req.budget
        )


