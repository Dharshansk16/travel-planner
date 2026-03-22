import json
<<<<<<< HEAD
import os

class HotelService:
    def __init__(self):
        data_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'hotels.json'
        )
        with open(os.path.normpath(data_path), 'r') as f:
            self.hotels_data = json.load(f)

    def search_hotels(self, city, budget_per_night=None, min_rating=None):
        city_map = {
            "bengaluru": "Bangalore", "bangalore": "Bangalore",
            "bombay": "Mumbai", "mumbai": "Mumbai",
        }
        city = city_map.get(city.lower(), city.title())
        res = [h for h in self.hotels_data
            if h['city'].lower() == city.lower()]
        if budget_per_night is not None:
            res = [h for h in res if h['price_per_night'] <= budget_per_night]
        if min_rating is not None:
            res = [h for h in res if h['rating'] >= min_rating]
        res.sort(key=lambda x: -x['rating'])
        return res
=======
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
>>>>>>> c1cba09d19d71fcbe1eee273856dbeecffc70215
