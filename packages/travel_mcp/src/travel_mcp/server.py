from fastmcp import FastMCP
import httpx
from .schemas.weather import WeatherRequest, WeatherResponse

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

if __name__ == "__main__":
    mcp.run()