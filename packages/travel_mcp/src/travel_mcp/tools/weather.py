from travel_mcp.services.weather_service import WeatherService
from fastmcp import FastMCP
from travel_shared.schema.weather import WeatherRequest, WeatherResponse

weather_service = WeatherService()

def register_weather_tool(mcp: FastMCP):
    @mcp.tool()
    async def fetch_weather(req: WeatherRequest) -> WeatherResponse:
        """
        Get the current weather and forecast for a specific destination.
        
        Use this when a user asks about the temperature, conditions, or 
        what to pack for a specific location.
        """
        
        return await weather_service.fetch_weather(req)