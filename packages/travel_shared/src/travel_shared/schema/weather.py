from pydantic import BaseModel , Field

class WeatherRequest(BaseModel):
    destination : str = Field(description="Name of the city or the destination")

class WeatherResponse(BaseModel):
    destination: str
    temperature : float
    description : str