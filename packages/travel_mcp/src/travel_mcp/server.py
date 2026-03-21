from fastmcp import FastMCP
import httpx
from travel_shared.schema.weather import WeatherRequest, WeatherResponse
from travel_mcp.tools.flights import register_flight_tool
from travel_mcp.tools.hotels import register_hotels_tool
from travel_mcp.tools.weather import register_weather_tool
from travel_mcp.tools.places import register_place_tool

mcp=FastMCP("TravelMCPServer")

#register all tools
register_flight_tool(mcp)
register_weather_tool(mcp)
register_hotels_tool(mcp)
register_place_tool(mcp)    

if __name__ == "__main__":
    mcp.run()