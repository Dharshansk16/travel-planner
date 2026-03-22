from travel_mcp.services.weather_service import WeatherService
from fastmcp import FastMCP
from travel_shared.schema.weather import WeatherRequest, WeatherResponse
from typing import Optional

weather_service = WeatherService()

def register_weather_tool(mcp: FastMCP):
    @mcp.tool
    async def fetch_weather(
        destination: Optional[str] = None,
        req: Optional[WeatherRequest] = None,
    ) -> WeatherResponse:
        payload = req if req is not None else WeatherRequest(destination=destination or "")
        return await weather_service.fetch_weather(payload)