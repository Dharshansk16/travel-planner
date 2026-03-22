from fastmcp import FastMCP
<<<<<<< HEAD
import httpx
from travel_shared.schema.weather import WeatherRequest, WeatherResponse

mcp=FastMCP("TravelMCPServer")

@mcp.tool()
async def fetch_weather(req: WeatherRequest) -> WeatherResponse:
    async with httpx.AsyncClient() as client:    
        geo = (await client.get(f"https://geocoding-api.open-meteo.com/v1/search?name={req.destination}&count=1")).json()
        
        if not geo.get("results"): 
            raise ValueError(f"Could not find {req.destination}.")
        
        lat, lon = geo["results"][0]["latitude"], geo["results"][0]["longitude"]
        weather = (await client.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true")).json()
        
    cur = weather.get("current_weather", {})
    
    return WeatherResponse(
        destination=req.destination,
        temperature=cur.get("temperature", 0.0),
        description=""
    )
=======
from travel_mcp.tools.flights import register_flight_tool
from travel_mcp.tools.hotels  import register_hotels_tool
from travel_mcp.tools.weather import register_weather_tool
from travel_mcp.tools.places  import register_place_tool

mcp = FastMCP("TravelMCPServer")

register_flight_tool(mcp)
register_weather_tool(mcp)
register_hotels_tool(mcp)
register_place_tool(mcp)
>>>>>>> origin/devika

if __name__ == "__main__":
    mcp.run()