import httpx
from travel_shared.schema.weather import WeatherRequest, WeatherResponse

class WeatherService:

    @staticmethod
    async def fetch_weather(req: WeatherRequest) -> WeatherResponse:
        async with httpx.AsyncClient() as client:
            geo = (await client.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={req.destination}&count=1"
            )).json()

            if not geo.get("results"):
                raise ValueError(f"Could not find {req.destination}.")

            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            weather = (await client.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            )).json()

        cur = weather.get("current_weather", {})

        return WeatherResponse(
            destination=req.destination,
            temperature=cur.get("temperature", 0.0),
            description=""
        )