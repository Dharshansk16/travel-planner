import httpx
from travel_shared.schema.weather import WeatherRequest, WeatherResponse

class WeatherService:

    @staticmethod
    async def fetch_weather(req: WeatherRequest) -> WeatherResponse:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"https://wttr.in/{req.destination}",
                params={"format": "j1"}
            )

            data = res.json()

            current = data["current_condition"][0]

            description = current["weatherDesc"][0]["value"]
            temp = float(current["temp_C"])

        return WeatherResponse(
            destination=req.destination,
            temperature=temp,
            description=description
        )