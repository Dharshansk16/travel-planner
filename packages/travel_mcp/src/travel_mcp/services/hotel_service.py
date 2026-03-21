import json
from pathlib import Path

class HotelService:
    def __init__(self):
        data_file = Path(__file__).resolve().parent.parent / "data" / "hotels.json"
        with data_file.open("r", encoding="utf-8") as f:
            self.fetched_hotels = json.load(f)
    
    def search_hotels(self, destination: str, budget=None):
        
        res = [
            hotel for hotel in self.fetched_hotels
            if hotel["city"].lower()== destination.lower()
        ]
        if budget is not None:
            res = [hotel for hotel in res if hotel["price_per_night"] <= budget]
        return res
