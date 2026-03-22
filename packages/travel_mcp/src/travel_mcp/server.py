from fastmcp import FastMCP
from travel_mcp.tools.flights import register_flight_tool
from travel_mcp.tools.hotels  import register_hotels_tool
from travel_mcp.tools.weather import register_weather_tool
from travel_mcp.tools.places  import register_place_tool

mcp = FastMCP("TravelMCPServer")

register_flight_tool(mcp)
register_weather_tool(mcp)
register_hotels_tool(mcp)
register_place_tool(mcp)

if __name__ == "__main__":
    mcp.run()